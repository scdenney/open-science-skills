#!/usr/bin/env python3
"""
Inventory a corpus of scans before choosing an OCR model.

`scan` reads every PDF (and every folder of page images) under the given
paths and writes triage.csv with one row per document: page count, a content
hash for spotting duplicate scans, whether a text layer exists and whether
it sits on top of page-sized images (a scan with an earlier OCR layer) or
is born-digital, /Rotate flags, landscape pages (often two-page spreads
that need splitting), page size, the scan resolution, the script
mix of any text layer, and a Latin-diacritics language hint. It renders
sample body pages to samples/ and draws contact sheets (twelve documents per
sheet) to sheets/, which are what a person or a vision model looks at to
name the script, language, era and layout. A text layer drawn invisibly
(render mode 3, or zero opacity) is an earlier OCR, not born-digital text.

`profile` reports the script mix and language of OCR output (.txt, or
.jsonl with a "text" field). Run it on a pilot read of the sample pages to
name the language of scans without a text layer, and on a finished run to
find pages whose script does not match the rest of the book.

    python triage.py scan corpus/ --out triage/ [--lid]
    python triage.py profile pilot/*.jsonl --lid

Needs: pymupdf. --lid needs fasttext (pip: fasttext-wheel, with numpy<2) and
huggingface_hub for GlotLID v3 (cis-lmu/glotlid, Apache-2.0), or falls back to
lingua-language-detector.
"""

import argparse
import csv
import hashlib
import json
import re
import statistics
import unicodedata
from collections import Counter
from pathlib import Path

import pymupdf as fitz

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}  # PyMuPDF cannot read WebP
# Letters that mark a Latin-script language. A hint, not an identification.
DIACRITICS = {
    "Polish": "ąćęłńśźż", "Czech": "ěřůťďň", "Slovak": "ľĺŕô", "Hungarian": "őű",
    "German": "äöüß", "French": "àâçèêëîïœù", "Spanish": "ñ¿¡", "Portuguese": "ãõ",
    "Romanian": "ășțşţ", "Turkish": "ğış", "Vietnamese": "ơưđạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ",
    "Croatian/Serbian/Bosnian": "đ", "Lithuanian": "ėįų", "Latvian": "āēģīķļņ",
    "Nordic": "åæø", "Icelandic": "ðþ",
}


MULTIWORD = {"OLD", "LINEAR", "CANADIAN", "NEW", "INSCRIPTIONAL", "MEROITIC", "CAUCASIAN", "PSALTER"}


def script_of(ch: str) -> str:
    """Approximate script from the Unicode character name (the standard library
    has no Script property). Good for the common scripts this is used for."""
    name = unicodedata.name(ch, "")
    if not name:
        return "OTHER"
    words = name.split()
    if words[0] == "CJK":
        return "HAN"
    return " ".join(words[:2]) if words[0] in MULTIWORD and len(words) > 1 else words[0]


def script_profile(text: str) -> dict[str, float]:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return {}
    counts = Counter(script_of(c) for c in letters)
    return {s: round(n / len(letters), 3) for s, n in counts.most_common(4)}


def diacritic_hint(text: str) -> str:
    low = text.lower()
    latin = sum(1 for c in low if c.isalpha() and script_of(c) == "LATIN")
    if latin < 200:
        return ""
    scores = {lang: sum(low.count(c) for c in chars) / latin for lang, chars in DIACRITICS.items()}
    lang, best = max(scores.items(), key=lambda kv: kv[1])
    return f"{lang} ({best:.1%})" if best >= 0.002 else "no distinctive diacritics"


def lid(text: str) -> str:
    """Top languages of a page-length text: GlotLID v3 if installed, else lingua."""
    global _LID
    text = " ".join(text.split())[:5000]
    if "_LID" not in globals():
        try:
            import fasttext
            from huggingface_hub import hf_hub_download
            _LID = ("glotlid", fasttext.load_model(hf_hub_download("cis-lmu/glotlid", "model.bin")))
        except Exception:
            try:
                from lingua import LanguageDetectorBuilder
                _LID = ("lingua", LanguageDetectorBuilder.from_all_languages().build())
            except ImportError:
                _LID = (None, None)
    kind, model = _LID
    if kind == "glotlid":
        labels, probs = model.predict(text, k=3)
        return "; ".join(f"{l.removeprefix('__label__')} {p:.2f}" for l, p in zip(labels, probs) if p >= 0.05)
    if kind == "lingua":
        out = model.compute_language_confidence_values(text)[:3]
        return "; ".join(f"{c.language.name.title()} {c.value:.2f}" for c in out if c.value >= 0.05)
    return "no LID package (pip install fasttext huggingface_hub, or lingua-language-detector)"


def sample_pages(n: int, k: int) -> list[int]:
    """k pages spread over the middle of the book (covers, front matter and
    indexes skipped; they are sparse or in another language)."""
    if n <= k:
        return list(range(1, n + 1))
    lo, hi = max(1, round(n * 0.2)), min(n, round(n * 0.8))
    return sorted({lo + round(i * (hi - lo) / max(1, k - 1)) for i in range(k)})


def sha16(path: Path) -> str:
    h = hashlib.sha256()
    files = [path] if path.is_file() else image_files(path)
    for f in files:
        with open(f, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
    return h.hexdigest()[:16]


def image_files(folder: Path) -> list[Path]:
    def natural(p: Path):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]
    return sorted((p for p in folder.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES), key=natural)


def find_documents(paths: list[str], exclude: Path) -> list[Path]:
    """PDFs (any case of .pdf) and folders of page images, skipping the output folder."""
    exclude = exclude.resolve()
    docs = []
    for p in map(Path, paths):
        if p.is_file() and p.suffix.lower() == ".pdf":
            docs.append(p)
        elif p.is_dir():
            files = [f for f in sorted(p.rglob("*")) if f.is_file()
                     and exclude not in f.resolve().parents]
            docs += [f for f in files if f.suffix.lower() == ".pdf"]
            docs += sorted({f.parent for f in files if f.suffix.lower() in IMAGE_SUFFIXES})
    return docs


def safe(name: str) -> str:
    return re.sub(r"[^\w.,()-]+", "_", name)


def unique_ids(docs: list[Path]) -> list[str]:
    """File stems, made unique with the parent folder name and then a counter."""
    ids = [safe(p.stem if p.is_file() else p.name) for p in docs]
    ids = [f"{safe(p.parent.name)}__{d}" if ids.count(d) > 1 else d for p, d in zip(docs, ids)]
    seen: dict[str, int] = {}
    for i, d in enumerate(ids):
        seen[d] = seen.get(d, 0) + 1
        if seen[d] > 1:
            ids[i] = f"{d}__{seen[d]}"
    return ids



def scan_pdf(path: Path, k: int, samples_dir: Path, doc_id: str, dpi: int):
    doc = fitz.open(path)
    n = doc.page_count
    chars, rotated, landscape, sizes, texts = [], 0, 0, [], []
    hidden = visible = 0
    for page in doc:
        t = page.get_text()
        if t.strip() and page.number % 10 == 0:  # every tenth page is enough
            for span in page.get_texttrace():
                n_chars = len(span["chars"])
                if span["type"] == 3 or span["opacity"] == 0:
                    hidden += n_chars
                else:
                    visible += n_chars
        chars.append(len(t.strip()))
        texts.append(t)
        rotated += page.rotation != 0
        landscape += page.rect.width > 1.15 * page.rect.height  # two-page spreads?
        sizes.append((page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4))
    picks = sample_pages(n, k)
    scan_dpis, full_image, pngs = [], 0, []
    for p in picks:
        page = doc[p - 1]
        area = abs(page.rect)
        best = None
        for img in page.get_images(full=True):
            for r in page.get_image_rects(img[0]):
                if best is None or abs(r) > abs(best[1]):
                    best = (img[2], r)
        if best and abs(best[1]) >= 0.8 * area:
            full_image += 1
            scan_dpis.append(round(best[0] / (best[1].width / 72)))
        png = samples_dir / f"{doc_id}_p{p}.png"
        page.get_pixmap(dpi=dpi).save(png)
        pngs.append(png)
    med = statistics.median(chars) if chars else 0
    if med < 50:
        kind = "scan"
    elif hidden > visible or full_image >= len(picks) / 2:
        kind = "scan with OCR layer" if hidden > visible else "scan with text layer"
    else:
        kind = "born-digital" if med >= 300 else "mixed or sparse text layer"
    text = "\n".join(texts)
    return {
        "n_pages": n, "kind": kind, "text_chars_median": int(med),
        "text_pages_share": round(sum(c >= 200 for c in chars) / max(1, n), 2),
        "rotated_pages": rotated, "landscape_pages": landscape,
        "page_mm": "{:.0f}x{:.0f}".format(*map(statistics.median, zip(*sizes))) if sizes else "",
        "scan_dpi": int(statistics.median(scan_dpis)) if scan_dpis else "",
        "sample_pages": ";".join(map(str, picks)),
        "text_script": json.dumps(script_profile(text)) if med >= 50 else "",
        "text_lang_hint": diacritic_hint(text) if med >= 50 else "",
        "_text": text if med >= 50 else "",
    }, pngs


def scan_images(folder: Path, k: int, samples_dir: Path, doc_id: str, dpi: int):
    files = image_files(folder)
    picks = sample_pages(len(files), k)
    pngs = []
    multi = 0
    for f in files:
        if f.suffix.lower() in {".tif", ".tiff"}:
            with fitz.open(f) as d:
                multi += d.page_count > 1
    for p in picks:
        pix = fitz.Pixmap(str(files[p - 1]))
        if pix.n - pix.alpha >= 4:  # CMYK
            pix = fitz.Pixmap(fitz.csRGB, pix)
        scale = dpi / (pix.xres or 300)
        if scale < 1:
            pix = fitz.Pixmap(pix, int(pix.width * scale), int(pix.height * scale), None)
        png = samples_dir / f"{doc_id}_p{p}.png"
        pix.save(png)
        pngs.append(png)
    first = fitz.Pixmap(str(files[0])) if files else None
    return {"n_pages": len(files), "kind": "scan (images)" + (f", {multi} multi-page TIFFs: split them" if multi else ""), "text_chars_median": 0,
            "text_pages_share": 0, "rotated_pages": 0, "landscape_pages": "", "page_mm": "",
            "scan_dpi": first.xres if first and first.xres else "",
            "sample_pages": ";".join(map(str, picks)), "text_script": "", "text_lang_hint": "",
            "_text": ""}, pngs


def contact_sheets(entries: list[tuple[str, Path]], out: Path, per_sheet: int = 12):
    """Grid of one sample page per document, labelled with its id."""
    cols, cell_w, cell_h, label = 4, 300, 420, 14
    for s in range(0, len(entries), per_sheet):
        chunk = entries[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        sheet = fitz.open()
        page = sheet.new_page(width=cols * cell_w, height=rows * (cell_h + label))
        for i, (doc_id, png) in enumerate(chunk):
            x, y = (i % cols) * cell_w, (i // cols) * (cell_h + label)
            page.insert_text((x + 4, y + 11), doc_id[:48], fontsize=9)
            page.insert_image(fitz.Rect(x + 2, y + label, x + cell_w - 2, y + label + cell_h),
                              filename=str(png), keep_proportion=True)
        page.get_pixmap(dpi=110).save(out / f"sheet_{s // per_sheet + 1:03d}.png")


def cmd_scan(args):
    out = Path(args.out)
    (out / "samples").mkdir(parents=True, exist_ok=True)
    (out / "sheets").mkdir(exist_ok=True)
    docs = find_documents(args.paths, out)
    rows, firsts, seen = [], [], {}
    for path, doc_id in zip(docs, unique_ids(docs)):
        info, pngs = (scan_pdf if path.is_file() else scan_images)(
            path, args.samples, out / "samples", doc_id, args.dpi)
        digest = sha16(path)
        row = {"doc_id": doc_id, "path": str(path), "mb": round(
            (path.stat().st_size if path.is_file() else sum(f.stat().st_size for f in image_files(path))) / 1e6, 1),
            "sha256_16": digest, "duplicate_of": seen.get(digest, "")}
        seen.setdefault(digest, doc_id)
        text = info.pop("_text")
        row.update(info)
        if args.lid and text:
            row["text_lid"] = lid(text)
        rows.append(row)
        if pngs:
            firsts.append((doc_id, pngs[len(pngs) // 2]))
        print(f"{doc_id}: {row['n_pages']} pages, {row['kind']}"
              f"{', dup of ' + row['duplicate_of'] if row['duplicate_of'] else ''}"
              f"{', landscape ' + str(row['landscape_pages']) if row['landscape_pages'] else ''}"
              f"{', LID ' + row['text_lid'] if row.get('text_lid') else ''}", flush=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(out / "triage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    contact_sheets(firsts, out / "sheets")
    kinds = Counter(r["kind"] for r in rows)
    print(f"\n{len(rows)} documents, {sum(r['n_pages'] for r in rows):,} pages: "
          + ", ".join(f"{k} {v}" for k, v in kinds.items())
          + f"; {sum(1 for r in rows if r['duplicate_of'])} exact duplicates")
    print(f"Wrote {out / 'triage.csv'}, samples/ and sheets/ (look at the sheets).")


def cmd_profile(args):
    for f in map(Path, args.files):
        if f.suffix == ".jsonl":
            recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
            pages = {r.get("page", i): r.get("text", "") for i, r in enumerate(recs)}  # last wins
            text = "\n".join(pages.values())
            prof = {p: script_profile(t) for p, t in pages.items() if len(t) >= 200}
            main = Counter(next(iter(v), "") for v in prof.values()).most_common(1)
            odd = [p for p, v in prof.items() if main and next(iter(v), "") != main[0][0]]
        else:
            text, odd = f.read_text(encoding="utf-8"), []
        hint = diacritic_hint(text)
        extra = f" | lid {lid(text)}" if args.lid else ""
        print(f"{f.name}: {script_profile(text)} | {hint or '-'}{extra}"
              + (f" | pages with another main script: {sorted(odd)[:15]}" if odd else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("paths", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--samples", type=int, default=3, help="sample pages per document")
    s.add_argument("--dpi", type=int, default=100, help="dpi of the sample renders")
    s.add_argument("--lid", action="store_true", help="language of the text layer (GlotLID, else lingua)")
    s.set_defaults(func=cmd_scan)
    p = sub.add_parser("profile")
    p.add_argument("files", nargs="+")
    p.add_argument("--lid", action="store_true")
    p.set_defaults(func=cmd_profile)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
