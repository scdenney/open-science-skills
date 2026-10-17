#!/usr/bin/env python3
"""
Resumable page OCR against any OpenAI-compatible vision endpoint.

Works with a local vLLM or SGLang server, llama.cpp `llama-server`, Ollama
(`/v1`), LM Studio, or a hosted API. Each page is rendered in memory (PyMuPDF
applies the PDF /Rotate flag) and sent with one prompt; every result is
appended to one JSONL file per document, so a crashed or cancelled run resumes
where it stopped. The last record for a page wins, and a page counts as done
only if that record was made with the same model, prompt, dpi and decoding
settings, so changing any of them re-reads the page instead of mixing
configurations. Pages that end in a repetition loop or hit max_tokens are
re-run once with a repetition penalty.

Manifest CSV columns: doc_id (unique), path (a PDF or a folder of single-page
images, relative to --root), and optionally pages ("1-20;25;30-31") and dpi.
Images in a folder are sent at their own resolution; convert multi-page TIFFs
to PDF or single pages first.

    python ocr_client.py --manifest manifest.csv --root pdfs/ --output out/ \\
        --prompt-file prompt.txt --model Qwen/Qwen3-VL-8B-Instruct \\
        --api-url http://127.0.0.1:8000/v1 --no-thinking

Several --api-url values spread pages round-robin over servers (one per GPU).
For a hosted API pass --api-key-env with the variable holding the key, and
--retry-penalty 0 if the API rejects unknown sampling fields.

Each record keeps the raw response, the parsed page type and text, the finish
reason, a loop flag and the settings; runs.jsonl holds the full run settings
under the record's run_id. This is a reduced form of the per-page schema in
reference/prompt-and-schema.md (b): no uncertain spans or layout markers.

Exit status: 0 when every requested page has an accepted record; 1 when pages
are missing, failed or refused (run the same command again); 2 when the only
problems are pages still looping or truncated after the retry, or empty
pages not tagged blank (review them).

Needs: pymupdf, openai.
"""

import argparse
import base64
import csv
import hashlib
import json
import os
import platform
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import pymupdf as fitz
from openai import OpenAI

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}
PAGE_TAG_RE = re.compile(r"^\s*\[\s*PAGE_TYPE\s*:\s*(\w+)\s*\]\s*\n?", re.IGNORECASE)
# A word-initial unit of 1-3 characters repeated 10+ times with spaces, or a
# word-initial unit up to 20 characters repeated 10+ times. Dotted leaders in
# tables of contents (". . . ." or "……") do not start with a word character.
LOOP_RES = [re.compile(r"((\w\S{0,2}) )\1{9,}"), re.compile(r"(\w.{0,19}?)\1{9,}")]
# Settings a record must share with the current run to count as done.
CONFIG_KEYS = ("model", "prompt_sha", "dpi", "temperature", "seed", "max_tokens")

_render_lock = threading.Lock()
_write_lock = threading.Lock()
_docs: dict[str, fitz.Document] = {}


def has_loop(text: str) -> bool:
    return any(r.search(text) for r in LOOP_RES)


def image_files(folder: Path) -> list[Path]:
    def natural(p: Path):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]
    return sorted((p for p in folder.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES), key=natural)


def page_count(path: Path) -> int:
    if path.is_dir():
        files = image_files(path)
        for f in files:
            if f.suffix.lower() in {".tif", ".tiff"}:
                with fitz.open(f) as doc:
                    if doc.page_count > 1:
                        sys.exit(f"{f}: multi-page TIFF ({doc.page_count} frames); convert it to PDF "
                                 "or single-page images first")
        return len(files)
    with fitz.open(path) as doc:
        return doc.page_count


def render(path: Path, page_no: int, dpi: int) -> tuple[str, str]:
    """Return (mime, base64) for a 1-based page. get_pixmap applies /Rotate."""
    if path.is_dir():
        f = image_files(path)[page_no - 1]
        if f.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            mime = "image/png" if f.suffix.lower() == ".png" else "image/jpeg"
            return mime, base64.b64encode(f.read_bytes()).decode()
        pix = fitz.Pixmap(str(f))
        if pix.n - pix.alpha >= 4:  # CMYK TIFF: PNG needs RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        return "image/png", base64.b64encode(pix.tobytes("png")).decode()
    with _render_lock:
        key = str(path)
        if key not in _docs:
            _docs[key] = fitz.open(path)
        pix = _docs[key][page_no - 1].get_pixmap(dpi=dpi)
        return "image/png", base64.b64encode(pix.tobytes("png")).decode()


def parse_pages(spec: str, n: int) -> list[int]:
    """Pages to read, in order, without repeats. Rejects anything out of range."""
    if not spec.strip():
        return list(range(1, n + 1))
    pages = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        a, _, b = part.partition("-")
        lo, hi = int(a), int(b or a)
        if not 1 <= lo <= hi <= n:
            raise ValueError(f"page range {part!r} is outside 1-{n} or descending")
        pages += [p for p in range(lo, hi + 1) if p not in pages]
    if not pages:
        raise ValueError(f"page selection {spec!r} is empty")
    return pages


def load_records(path: Path) -> dict[int, dict]:
    """Last record per page."""
    done: dict[int, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[rec["page"]] = rec
    return done


def quarantine_truncated_tail(path: Path) -> None:
    """A write killed mid-record leaves a partial last line; move it aside.
    Corruption anywhere else still raises in load_records."""
    if not path.exists() or not path.stat().st_size:
        return
    data = path.read_bytes()
    body, _, last = data.rstrip(b"\n").rpartition(b"\n")
    try:
        json.loads(last)
    except json.JSONDecodeError:
        with open(path.with_suffix(".truncated"), "ab") as f:
            f.write(last + b"\n")
        path.write_bytes(body + b"\n" if body else b"")
        print(f"{path.name}: moved a truncated last record to {path.with_suffix('.truncated').name}", flush=True)
        return
    if not data.endswith(b"\n"):
        with open(path, "ab") as f:
            f.write(b"\n")


def status(rec: dict | None, cfg: dict) -> str:
    """missing | failed | review | empty | ok for the current configuration."""
    if rec is None or any(rec.get(k) != cfg[k] for k in CONFIG_KEYS):
        return "missing"
    if rec["finish_reason"] not in ("stop", "length"):  # error, content_filter, recitation, ...
        return "failed"
    if rec["loop"] or rec["finish_reason"] == "length":
        return "review"
    if not rec["text"].strip() and rec["page_type"] != "blank":
        return "empty"
    return "ok"


def call(client, args, mime, img, penalty):
    image = {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img}"}}
    text = {"type": "text", "text": args.prompt_text}
    content = [image, text] if args.image_first else [text, image]
    extra = dict(args.extra_body)
    if penalty:
        extra["repetition_penalty"] = penalty
    resp = client.chat.completions.create(
        model=args.model, messages=[{"role": "user", "content": content}],
        max_tokens=args.max_tokens, temperature=args.temperature, seed=args.seed,
        extra_body=extra or None)
    choice = resp.choices[0]
    raw = choice.message.content or ""
    ntok = resp.usage.completion_tokens if resp.usage else None
    return raw, choice.finish_reason or "unknown", ntok


def process(task, client, args, attempt, penalty):
    doc_id, path, page_no, dpi, out_path = task
    t0, err = time.time(), None
    raw, finish, ntok = "", "error", None
    for k in range(args.tries):
        try:
            mime, img = render(path, page_no, dpi)
            raw, finish, ntok = call(client, args, mime, img, penalty)
            err = None
            break
        except Exception as e:  # rate limits, timeouts; the page is retried on resume
            err = repr(e)
            time.sleep(2 ** k)
    answer = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    m = PAGE_TAG_RE.match(answer)
    page_type, text = (m.group(1).lower(), answer[m.end():].strip()) if m else ("untagged", answer)
    rec = {"doc_id": doc_id, "page": page_no, "page_type": page_type, "text": text,
           "finish_reason": finish, "completion_tokens": ntok, "attempt": attempt,
           "loop": has_loop(text), "secs": round(time.time() - t0, 2),
           "repetition_penalty": penalty, "error": err, "run_id": args.run_id,
           **{k: args.cfg[k] if k != "dpi" else dpi for k in CONFIG_KEYS}, "raw": raw}
    with _write_lock, open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def run_pass(tasks, clients, args, attempt, penalty):
    n, t_start = len(tasks), time.time()
    with ThreadPoolExecutor(max_workers=args.concurrency * len(clients)) as pool:
        futs = [pool.submit(process, t, clients[i % len(clients)], args, attempt, penalty)
                for i, t in enumerate(tasks)]
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            if i % 25 == 0 or i == n or rec["error"]:
                rate = i / max(1e-6, time.time() - t_start)
                print(f"  [{i}/{n}] {rec['doc_id']} p{rec['page']} {rec['page_type']} "
                      f"{len(rec['text'])}ch {rec['finish_reason']} {rec['secs']}s "
                      f"({rate:.2f} pages/s){' ERROR ' + rec['error'] if rec['error'] else ''}",
                      flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root", default=".", help="directory the manifest paths are relative to")
    ap.add_argument("--output", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--model", required=True, help="model id as the server knows it")
    ap.add_argument("--api-url", nargs="+", default=["http://127.0.0.1:8000/v1"])
    ap.add_argument("--api-key-env", help="environment variable holding the API key (hosted APIs)")
    ap.add_argument("--dpi", type=int, default=200, help="render dpi for PDFs; a manifest dpi column wins")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=2025)
    ap.add_argument("--concurrency", type=int, default=16, help="requests in flight per server")
    ap.add_argument("--retry-penalty", type=float, default=1.05,
                    help="repetition_penalty for the retry pass; 0 disables the pass")
    ap.add_argument("--no-thinking", action="store_true",
                    help="send chat_template_kwargs enable_thinking=false (Qwen3.x hybrid models)")
    ap.add_argument("--extra-body", default="{}", help="JSON merged into every request body")
    ap.add_argument("--image-first", action="store_true", help="put the image before the prompt")
    ap.add_argument("--tries", type=int, default=3, help="attempts per request before recording an error")
    ap.add_argument("--timeout", type=float, default=900)
    args = ap.parse_args()

    args.prompt_text = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    prompt_sha = hashlib.sha256(args.prompt_text.encode("utf-8")).hexdigest()[:12]
    args.extra_body = json.loads(args.extra_body)
    if args.no_thinking:
        args.extra_body.setdefault("chat_template_kwargs", {})["enable_thinking"] = False
    args.cfg = {"model": args.model, "prompt_sha": prompt_sha, "dpi": args.dpi,
                "temperature": args.temperature, "seed": args.seed, "max_tokens": args.max_tokens}
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    args.run_id = f"{started}_{prompt_sha}"
    key = os.environ[args.api_key_env] if args.api_key_env else "EMPTY"
    clients = [OpenAI(api_key=key, base_url=u, timeout=args.timeout) for u in args.api_url]

    with open(args.manifest, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    dup = sorted({r["doc_id"] for r in rows if sum(x["doc_id"] == r["doc_id"] for x in rows) > 1})
    if dup:
        sys.exit(f"duplicate doc_id in {args.manifest}: {dup[:10]}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_info = {k: v for k, v in vars(args).items() if k not in {"prompt_text", "cfg"}}
    run_info.update(prompt_sha=prompt_sha, prompt_text=args.prompt_text, started=started,
                    python=platform.python_version(), pymupdf=fitz.VersionBind)
    with open(out_dir / "runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(run_info, ensure_ascii=False) + "\n")

    docs, tasks = [], []
    for row in rows:
        path = Path(args.root) / row["path"]
        n = page_count(path)
        try:
            pages = parse_pages(row.get("pages", "") or "", n)
        except ValueError as e:
            sys.exit(f"{row['doc_id']}: {e}")
        dpi = "native" if path.is_dir() else (int(row["dpi"]) if row.get("dpi") else args.dpi)
        cfg = {**args.cfg, "dpi": dpi}
        out_path = out_dir / f"{row['doc_id']}.jsonl"
        quarantine_truncated_tail(out_path)
        recs = load_records(out_path)
        todo = [p for p in pages if status(recs.get(p), cfg) in ("missing", "failed")]
        other = sum(1 for p in pages if p in recs and status(recs[p], cfg) == "missing")
        docs.append((row["doc_id"], path, pages, dpi, cfg, out_path))
        print(f"{row['doc_id']}: {n} pages, {len(pages)} requested, {len(todo)} to do (dpi {dpi})"
              + (f"; {other} recorded under other settings will be re-read" if other else ""), flush=True)
        tasks += [(row["doc_id"], path, p, dpi, out_path) for p in todo]

    print(f"Pass 1: {len(tasks)} pages, {len(clients)} server(s) x {args.concurrency} in flight, "
          f"prompt {prompt_sha}", flush=True)
    run_pass(tasks, clients, args, attempt=1, penalty=None)

    if args.retry_penalty:
        retry = []
        for doc_id, path, pages, dpi, cfg, out_path in docs:
            recs = load_records(out_path)
            retry += [(doc_id, path, p, dpi, out_path) for p in pages
                      if status(recs.get(p), cfg) == "review" and recs[p]["attempt"] == 1]
        print(f"Pass 2 (repetition_penalty={args.retry_penalty}): {len(retry)} pages", flush=True)
        if retry:
            run_pass(retry, clients, args, attempt=2, penalty=args.retry_penalty)

    totals = {"missing": 0, "failed": 0, "review": 0, "empty": 0, "ok": 0}
    for doc_id, path, pages, dpi, cfg, out_path in docs:
        recs = load_records(out_path)
        st = {p: status(recs.get(p), cfg) for p in pages}
        for s in st.values():
            totals[s] += 1
        bad = {s: [p for p, v in st.items() if v == s] for s in ("missing", "failed", "review", "empty")}
        if any(bad.values()):
            print(f"{doc_id}: " + ", ".join(f"{len(v)} {s} {v[:8]}" for s, v in bad.items() if v), flush=True)
    print("Done: " + ", ".join(f"{v} {k}" for k, v in totals.items()) + " pages", flush=True)
    if totals["missing"] or totals["failed"]:
        sys.exit(1)  # run the same command again to retry them
    sys.exit(2 if totals["review"] or totals["empty"] else 0)


if __name__ == "__main__":
    main()
