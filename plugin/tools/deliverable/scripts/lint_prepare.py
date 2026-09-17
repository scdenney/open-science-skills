#!/usr/bin/env python3
"""lint_prepare.py -- reserve a lint run and write everything the workers need.

    lint_prepare.py --root DIR [--budget USD] [--mode manual|headless] [--sections a,b]
                    [--skip-fast] [--no-build] [--check PATH]

Creates checks/YYYY-MM-DD[-N]/ (never reuses a directory), runs the fast gate
into <run>/fast.json (absolute path; --skip-fast writes {"skipped": true}),
freezes the input hash and start time in <run>/inputs/run.json, writes
<run>/inputs/index.json (every manifest section, with absolute worker output
paths, including sections omitted by --sections, marked so), and one
<run>/inputs/section-<id>.md per selected section (manifest fields, argument
map, gate citation status for its lines, voice summary, neighbours, the
line-numbered section text, speaker notes for decks, knowledge-base source
paths when the manifest names one). Prints the run directory. Both vendors
call this before launching finders; lint_adjudicate.py consumes the result.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys
from pathlib import Path
import yaml

VOICE_CANDIDATES = [Path.home() / ".claude/skills/sci-edit/voice.md",
                    Path.home() / "Documents/GitHub/resources/writing-toolkit/voice.md",
                    Path.home() / "Documents/github/resources/writing-toolkit/voice.md",
                    Path.home() / ".agents/skills/sci-edit/voice.md"]

def voice_summary():
    for p in VOICE_CANDIDATES:
        if p.exists():
            rules = re.findall(r"^### (R\d+\. [^\n]+)", p.read_text(encoding="utf-8", errors="replace"), re.M)
            if rules:
                return "Voice rules (%s; slide text is fragmentary by design, judge sentences and notes):\n" % p + "\n".join("- " + r for r in rules)
    return None

def reserve(root):
    today = dt.date.today().isoformat(); base = root / "checks"; base.mkdir(exist_ok=True)
    n = 0
    while True:
        cand = base / (today if n == 0 else "%s-%d" % (today, n + 1))
        try:
            cand.mkdir(); return cand
        except FileExistsError:
            n += 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--budget", type=float, default=3.0); ap.add_argument("--mode", default="manual")
    ap.add_argument("--sections"); ap.add_argument("--skip-fast", action="store_true"); ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--check", default=str(Path(__file__).with_name("check_deliverable.py")))
    a = ap.parse_args()
    root = Path(a.root).resolve(); m = yaml.safe_load((root / "deliverable.yml").read_text(encoding="utf-8")) or {}
    run = reserve(root); (run / "inputs").mkdir(); (run / "finders").mkdir()
    py = sys.executable
    h = subprocess.run([py, a.check, "hash", "--root", str(root)], capture_output=True, text=True).stdout.strip()
    started = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    # fast gate
    fast_path = run / "fast.json"
    build = not a.no_build and a.mode != "headless"
    if a.skip_fast:
        fast_path.write_text(json.dumps({"skipped": True, "items": [], "summary": {}}, indent=2) + "\n", encoding="utf-8"); fast_state = "skipped"
    else:
        cmd = [py, a.check, "--root", str(root), "--json", str(fast_path)] + (["--build"] if build else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        fast_state = "failed" if r.returncode else "passed"
    sections = json.loads(subprocess.run([py, a.check, "sections", "--root", str(root)], capture_output=True, text=True).stdout or "[]")
    want = set(s.strip() for s in a.sections.split(",")) if a.sections else None
    kb = m.get("knowledge_base"); kbdir = (root / kb).resolve() if kb else None
    index = []
    for s in sections:
        sid = str(s.get("id")); sel = want is None or sid in want
        index.append({"id": sid, "title": s.get("title"), "file": s.get("file"), "line": s.get("line"), "end_line": s.get("end_line"),
                      "selected": sel, "input": str(run / "inputs" / ("section-%s.md" % sid)) if sel else None,
                      "out": str(run / "finders" / ("section-%s.json" % sid))})
    (run / "inputs" / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (run / "inputs" / "run.json").write_text(json.dumps({"schema": 1, "id": m.get("id"), "root": str(root), "run": str(run), "started": started,
        "input_hash": h, "mode": a.mode, "budget_usd": a.budget, "fast_gate": fast_state, "build_checked": build and not a.skip_fast,
        "knowledge_base": str(kbdir) if kbdir else None, "required_dimensions": ["clarity", "claim_source", "consistency"] + (["support"] if kbdir else []),
        "global_out": str(run / "finders" / "global.json")}, indent=2) + "\n", encoding="utf-8")
    # per-section inputs
    fast = json.loads(fast_path.read_text(encoding="utf-8")); cites = [i for i in fast.get("items", []) if i.get("check") == "citations"]
    pd = root / (m.get("planning_dir") or "planning"); amap = ""
    for name in ("00-README.md", "01-brief.md"):
        p = pd / name
        if p.exists(): amap += p.read_text(encoding="utf-8", errors="replace") + "\n\n"
    voice = voice_summary() or "(voice rules not found on this machine; clarity question limited to plain readability)"
    files = {}
    def lines_of(f):
        if f not in files: files[f] = (root / f).read_text(encoding="utf-8", errors="replace").splitlines() if (root / f).exists() else []
        return files[f]
    notes = (root / "notes.md").read_text(encoding="utf-8", errors="replace") if (root / "notes.md").exists() else ""
    fields = "audience: %s\nclaim: %s\ndone: %s" % (str(m.get("audience", "")).strip(), str(m.get("claim", "")).strip(), str(m.get("done", "")).strip())
    kind_file = Path(__file__).resolve().parent.parent / "kinds" / ("%s.md" % m.get("kind", ""))
    kind_q = ""
    if kind_file.exists():
        kt = kind_file.read_text(encoding="utf-8")
        mm = re.search(r"^## Lint questions\n(.*?)(?=^## |\Z)", kt, re.S | re.M)
        if mm: kind_q = "\n## Kind-specific questions (%s)\n%s\n" % (m.get("kind"), mm.group(1).strip())
    for k, s in enumerate(index):
        if not s["selected"]: continue
        L = lines_of(s["file"]); lo, hi = int(s["line"] or 1), int(s["end_line"] or len(L))
        block = "\n".join("%5d  %s" % (n, L[n - 1]) for n in range(lo, min(hi, len(L)) + 1))
        prev = "\n".join(lines_of(index[k-1]["file"])[index[k-1]["line"]-1:index[k-1]["line"]+2]) if k else "(none)"
        nxt = "\n".join(lines_of(index[k+1]["file"])[index[k+1]["line"]-1:index[k+1]["line"]+2]) if k + 1 < len(index) else "(none)"
        cs = [c for c in cites if (c.get("file") or "").endswith(s["file"].split("/")[-1]) and lo <= (c.get("line") or 0) <= hi]
        cstat = "\n".join("- line %s: %s: %s" % (c.get("line"), c.get("status"), c.get("msg")) for c in cs) or "- no citation problems reported by the gate in this section"
        nb = ""
        if notes:
            mm = re.search(r"^## %s\.\s.*?(?=^## |\Z)" % re.escape(s["id"].split("-")[-1]), notes, re.S | re.M)
            nb = "\n## Speaker notes for this section (notes.md)\n" + (mm.group(0).strip() if mm else "(none found)") + "\n"
        kbtxt = ""
        if kbdir and kbdir.is_dir():
            keys = set(re.findall(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}", "\n".join(L[lo-1:hi])))
            paths = [str(p) for key in keys for k2 in key.split(",") for p in kbdir.glob(k2.strip() + "*.md")]
            kbtxt = "\n## Knowledge-base sources for this section's citations\n" + ("\n".join("- " + p for p in paths) if paths else "- none found; support question is NOT CHECKED for this section") + "\n"
        support_q = "\n4. Support: for each claim attributed to a cited source, does the source's Markdown say it? Quote the passage with its file. Unsupported = P1 (dimension support); contradicted = P0 with the passage as verification; source file missing = report once as `not in knowledge base` (P2).\n" if kbdir else ""
        text = f"""# Lint input: section {s['id']} — {s['title']}

Deliverable: {m.get('id')} ({m.get('kind')}): {m.get('title')}
{fields}

## Argument map (planning wiki)
{amap or '(no planning index found)'}
## Citation status from the deterministic gate (this section's lines)
{cstat}
(A citation the gate resolved is not listed; treat unlisted citations as resolved.)

## {voice}

## Previous section (first lines)
{prev}

## SECTION TEXT ({s['file']}, line-numbered; `@key` lines are field names, not prose)
{block}

## Next section (first lines)
{nxt}
{nb}{kbtxt}{kind_q}
## Questions to answer for the SECTION TEXT only
1. Clarity and voice: sentences a first reader would read twice; the tells in the voice rules; jargon used before it is defined here or earlier.
2. Claim-to-source: every factual or empirical claim: does it name a source, and is that source resolved (see the gate's status list)? Unsourced claim = P1. A claim whose named source the gate listed as unverified = P0 (quote the gate line as the verification).
3. Consistency: numbers that disagree with the notes or another section; a term used for two things, or two terms for one thing.{support_q}
## Output contract
Write ONE JSON object to {s['out']}:
{{"section": "{s['id']}", "coverage": {{"clarity": true, "claim_source": true, "consistency": true{', "support": true' if kbdir else ''}}}, "findings": [{{"severity": "P0|P1|P2", "dimension": "clarity|claim-source|consistency{'|support' if kbdir else ''}", "rule": "...", "file": "{s['file']}", "line": <int>, "quote": "<verbatim from the section, max 120 chars>", "finding": "...", "action": "...", "verification": "<gate line or source passage for a P0, else n/a>"}}]}}
Set a coverage value to false if you could not answer that question. Quotes verbatim from the section text only; never invent a source or a number; an empty findings list is valid.
"""
        Path(s["input"]).write_text(text, encoding="utf-8")
    print(run)

if __name__ == "__main__":
    main()
