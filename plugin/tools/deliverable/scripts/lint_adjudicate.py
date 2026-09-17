#!/usr/bin/env python3
"""lint_adjudicate.py -- merge finder and global-pass outputs into findings.json and report.md.

    lint_adjudicate.py --root DIR --run checks/YYYY-MM-DD[-N] --models finders=M,global=M,adjudicator=M
                       [--check PATH]

Reads <run>/inputs/run.json (frozen start hash, mode, budget, fast-gate state),
<run>/inputs/index.json, <run>/fast.json, <run>/finders/section-*.json and
finders/global.json. Verifies every anchor (file + line + verbatim quote),
dedupes across dimensions, ranks, keeps the frozen hash and marks the run
stale if the inputs changed, records honest coverage (a section counts as
checked only when its worker's coverage has every required dimension true),
and derives the verdict from all of: fast gate passed, coverage complete, not
stale, zero open P0. Both vendors call this so the files serialize identically
(UTF-8, LF, two-space JSON, trailing newline).
"""
import argparse, json, re, subprocess, sys, datetime as dt
from pathlib import Path
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True); ap.add_argument("--run", required=True)
ap.add_argument("--models", default="finders=unknown,global=unknown,adjudicator=unknown")
ap.add_argument("--check", default=str(Path(__file__).with_name("check_deliverable.py")))
A = ap.parse_args()
D = Path(A.root).resolve(); OUT = (D / A.run).resolve() if not Path(A.run).is_absolute() else Path(A.run)
MODELS = dict(kv.split("=", 1) for kv in A.models.split(","))
RUN = json.loads((OUT / "inputs" / "run.json").read_text(encoding="utf-8"))
index = json.loads((OUT / "inputs" / "index.json").read_text(encoding="utf-8"))
fast = json.loads((OUT / "fast.json").read_text(encoding="utf-8")) if (OUT / "fast.json").exists() else {"skipped": True, "items": []}
REQ = RUN.get("required_dimensions") or ["clarity", "claim_source", "consistency"]
order = {"P0": 0, "P1": 1, "P2": 2}
files = {}
def load(fn):
    if fn not in files:
        p = D / fn; files[fn] = p.read_text(encoding="utf-8", errors="replace").splitlines() if p.exists() else None
    return files[fn]
def norm(s): return re.sub(r"\s+", " ", (s or "")).strip().lower()
def anchor(f):
    fn = f.get("file") or ""; lines = load(fn)
    if not lines: return None
    q = norm(f.get("quote", ""))
    if not q: return None
    ln = int(f.get("line") or 0)
    cand = list(range(max(1, ln - 3), min(len(lines), ln + 3) + 1)) + list(range(1, len(lines) + 1))
    for n in cand:
        L = norm(lines[n - 1])
        if q in L or (len(q) > 25 and L and L in q): return fn, n
    return None
def relfile(path):
    try: return str(Path(path).resolve().relative_to(D))
    except (ValueError, OSError): return str(path)

findings, coverage, dropped = [], [], 0
gate_fail_lines = set()
for it in fast.get("items", []):
    if it.get("status") == "FAIL":
        fn = relfile(it["file"]) if it.get("file") else "deliverable.yml"
        if it.get("check") == "citations" and it.get("line"): gate_fail_lines.add((fn, it["line"]))
        findings.append({"severity": "P0", "dimension": "gate", "rule": it["check"], "file": fn, "section": None, "line": it.get("line"), "end_line": it.get("line"),
                         "quote": "", "finding": it["msg"], "action": "resolve the gate failure", "verification": "gate: " + it["msg"], "source": "gate"})
for sec in index:
    if not sec.get("selected", True):
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "NOT CHECKED", "reason": "omitted by --sections"}); continue
    p = Path(sec["out"]); p = p if p.is_absolute() else OUT / p
    if not p.exists():
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "NOT CHECKED", "reason": "finder produced no file"}); continue
    try: data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "NOT CHECKED", "reason": "finder JSON invalid: %s" % e}); continue
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "NOT CHECKED", "reason": "finder output is not one object with a findings list"}); continue
    cov = data.get("coverage") or {}
    missing = [d for d in REQ if not cov.get(d)]
    if missing:
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "NOT CHECKED", "reason": "worker did not cover: %s" % ", ".join(missing), "finder": MODELS.get("finders")})
    else:
        coverage.append({"id": sec["id"], "title": sec["title"], "status": "checked", "finder": MODELS.get("finders"), "coverage": cov})
    for f in data["findings"]:
        f.setdefault("file", sec.get("file"))
        a = anchor(f)
        if not a: dropped += 1; continue
        f["file"], f["line"] = a; f.setdefault("end_line", f["line"]); f["section"] = sec["id"]; f["source"] = "finder"
        if f.get("severity") not in order: f["severity"] = "P2"
        if f["severity"] == "P0" and f.get("dimension") == "claim-source" and (f["file"], f["line"]) not in gate_fail_lines:
            f["severity"] = "P1"; f["finding"] = (f.get("finding", "") + " (downgraded: no gate evidence for an unresolved citation at this line)").strip()
        if f["severity"] == "P0" and f.get("dimension") in ("support", "consistency") and not (f.get("verification") and f["verification"] != "n/a"):
            f["severity"] = "P1"; f["finding"] = (f.get("finding", "") + " (downgraded: P0 needs a verification passage)").strip()
        findings.append(f)
gp = Path(RUN.get("global_out") or (OUT / "finders" / "global.json"))
gcov = {"status": "NOT CHECKED", "reason": "global pass produced no file"}
if gp.exists():
    try:
        g = json.loads(gp.read_text(encoding="utf-8")); gc = g.get("coverage") or {}
        gmiss = [d for d in ("order", "spec", "repetition", "release") if not gc.get(d)]
        gcov = {"status": "checked" if not gmiss else "NOT CHECKED", "model": MODELS.get("global"), "coverage": gc, **({"reason": "global pass did not cover: " + ", ".join(gmiss)} if gmiss else {})}
        for f in g.get("findings", []):
            a = anchor(f)
            if not a: dropped += 1; continue
            f["file"], f["line"] = a; f.setdefault("end_line", f["line"]); f["section"] = None; f["source"] = "global"
            if f.get("severity") not in order: f["severity"] = "P2"
            findings.append(f)
    except json.JSONDecodeError as e:
        gcov = {"status": "NOT CHECKED", "reason": "global JSON invalid: %s" % e}
merged = []
for f in findings:
    q = norm(f.get("quote", "")); hit = None
    fam = lambda x: "claim" if x["dimension"] in ("claim-source", "gate") else x["dimension"]
    for g in merged:
        if g["file"] != f["file"] or g["line"] != f["line"]: continue
        gq = norm(g.get("quote", ""))
        if fam(g) == fam(f) or (q and gq and (q in gq or gq in q)): hit = g; break
    if hit is None: merged.append(f); continue
    keep, drop = (hit, f) if (hit["source"] == "gate" or order[hit["severity"]] < order[f["severity"]] or (hit["severity"] == f["severity"] and len(hit.get("finding", "")) >= len(f.get("finding", "")))) else (f, hit)
    keep["also"] = keep.get("also", []) + [drop["source"] + ":" + drop["dimension"]]
    if drop is hit: merged[merged.index(hit)] = keep
findings = merged
findings.sort(key=lambda f: (order[f["severity"]], f["file"], f["line"] or 0))
for i, f in enumerate(findings, 1): f["id"] = "F%03d" % i; f["disposition"] = "open"
h_now = subprocess.run([sys.executable, A.check, "hash", "--root", str(D)], capture_output=True, text=True).stdout.strip()
stale = h_now != RUN.get("input_hash")
n_sections = len(index); checked = sum(1 for c in coverage if c["status"] == "checked")
complete = checked == n_sections and gcov["status"] == "checked"
p0 = sum(1 for f in findings if f["severity"] == "P0")
fast_state = "skipped" if fast.get("skipped") else RUN.get("fast_gate") or ("failed" if any(i.get("status") == "FAIL" for i in fast.get("items", [])) else "passed")
may_ship = fast_state == "passed" and complete and not stale and p0 == 0
meta = {"id": RUN.get("id"), "input_hash": RUN.get("input_hash"), "input_hash_now": h_now, "stale": stale, "started": RUN.get("started"),
        "finished": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"), "mode": RUN.get("mode"), "models": MODELS,
        "cost": {"allowance_usd": round(sum(1 for s in index if s.get("selected", True)) * 0.10 + 1.0 + 0.5, 2), "reported_usd": None, "budget_usd": RUN.get("budget_usd")},
        "verdict": {"may_ship": may_ship, "fast_gate": fast_state, "coverage_complete": complete, "stale": stale, "open_p0": p0}}
cov = {"fast_gate": fast_state, "build_checked": bool(RUN.get("build_checked")), "sections": coverage, "global": gcov,
       "dimensions": REQ + ["order", "spec", "repetition", "release"], "dropped_unanchored": dropped}
(OUT / "findings.json").write_text(json.dumps({"meta": meta, "coverage": cov, "findings": findings}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {k: sum(1 for f in findings if f["severity"] == k) for k in ("P0", "P1", "P2")}
reasons = [r for r, bad in (("fast gate %s" % fast_state, fast_state != "passed"), ("coverage incomplete", not complete), ("inputs changed during the run", stale), ("%d open P0" % p0, p0 > 0)) if bad]
rep = ["# Lint report — %s — %s" % (meta["id"], OUT.name), "", ("**May ship.**" if may_ship else "**May not ship: %s.**" % "; ".join(reasons)), "",
       "Mode %s; fast gate %s (build %s); %d/%d sections checked (%s finders), global pass %s (%s); %d unanchored findings dropped; planning allowance $%.2f of a $%.2f budget, metered cost %s." %
       (meta["mode"], fast_state, "checked" if cov["build_checked"] else "NOT CHECKED", checked, n_sections, MODELS.get("finders"), gcov["status"], MODELS.get("global"), dropped, meta["cost"]["allowance_usd"], meta["cost"]["budget_usd"] or 0, "unmetered"), ""]
for sev in ("P0", "P1", "P2"):
    fs = [f for f in findings if f["severity"] == sev]; rep.append("## %s (%d)" % (sev, len(fs))); rep.append("")
    for f in fs:
        rep.append("- **%s** `%s:%s` [%s/%s] %s" % (f["id"], f["file"], f["line"] or "?", f["dimension"], f["source"], ("“%s” " % f["quote"]) if f.get("quote") else ""))
        rep.append("  %s" % f.get("finding", "")); rep.append("  Action: %s" % f.get("action", ""))
        if f.get("verification") and f["verification"] not in ("n/a", ""): rep.append("  Verification: %s" % f["verification"])
    rep.append("")
nc = [c for c in coverage if c["status"] != "checked"]
rep.append("## NOT CHECKED (%d)" % (len(nc) + (0 if gcov["status"] == "checked" else 1))); rep.append("")
for c in nc: rep.append("- %s %s: %s" % (c["id"], c["title"], c["reason"]))
if gcov["status"] != "checked": rep.append("- global pass: %s" % gcov.get("reason"))
rep += ["", "## For the author", "", "Dictate reactions into `inbox/` and run intake: accepted findings become tasks; rejected ones go under `Rejected findings` in the wiki's `08-open-questions.md` so the next run does not raise them again. Fix the P0s first; nothing else blocks."]
(OUT / "report.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print("findings: %s | sections checked %d/%d | global %s | stale %s | may_ship %s" % (counts, checked, n_sections, gcov["status"], stale, may_ship))
