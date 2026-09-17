#!/usr/bin/env python3
"""Deterministic checks for a replication package.

Two tiers, deliberately separated.

  Static (default, always safe): reads files only. Seed, session-info, and
  lockfile presence; absolute paths that will not resolve on another machine;
  credential-shaped strings; a sha256 manifest of the data directory.

  Execution (--run, never the default): copies the package to a temporary
  directory and executes its master script there, then compares what appeared
  against the figure/table crosswalk.

The execution tier runs code the package's author wrote, which is arbitrary
code execution on this machine. It is off unless asked for, and the calling
skill must obtain the user's explicit authorization first.

Emits JSON on stdout (--json) or a short human summary, and exits non-zero if
any check fails, so it can gate a pipeline.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MASTERS = ["master.R", "master.r", "run_all.R", "master.py", "run_all.py", "Makefile"]
CODE_SUFFIXES = {".R", ".r", ".py", ".Rmd", ".qmd", ".do", ".ipynb"}
LOCKFILES = ["renv.lock", "requirements.txt", "environment.yml", "Pipfile.lock", "uv.lock", "DESCRIPTION"]
SEED_PAT = re.compile(r"set\.seed\s*\(|np\.random\.seed\s*\(|random\.seed\s*\(|default_rng\s*\(|set\s+seed\s", re.I)
SESSION_PAT = re.compile(r"sessionInfo\s*\(|session_info\s*\(|sessioninfo::|pip\s+freeze|platform\.platform\s*\(", re.I)
ABS_PAT = re.compile(r"""["'](/(?:Users|home|mnt|media)/[^"']+|[A-Z]:\\\\[^"']+)["']""")
CRED_PAT = re.compile(
    r"(?:api[_-]?key|secret|passwd|password|token|bearer)\s*[=:]\s*[\"'][^\"']{8,}[\"']"
    r"|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}", re.I)


def add(findings, ok, check, detail, severity="fail"):
    findings.append({"check": check, "status": "pass" if ok else severity, "detail": detail})
    return ok


def code_files(root):
    skip = {".git", "renv", "node_modules", "__pycache__", ".venv"}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix in CODE_SUFFIXES and not (skip & set(p.parts)):
            yield p


def static_checks(root, findings):
    code = list(code_files(root))
    add(findings, bool(code), "code-present", f"{len(code)} analysis files found" if code
        else "no analysis code found under the package root")

    master = next((m for m in MASTERS if (root / m).exists()), None)
    add(findings, master is not None,
        "master-script", f"master script is {master}" if master
        else f"no master script; looked for {', '.join(MASTERS)}")

    blob = ""
    for p in code:
        try:
            blob += p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

    add(findings, bool(SEED_PAT.search(blob)), "seed",
        "a random seed is set" if SEED_PAT.search(blob)
        else "no seed found; stochastic results will not reproduce exactly")
    add(findings, bool(SESSION_PAT.search(blob)), "session-info",
        "session or environment info is recorded" if SESSION_PAT.search(blob)
        else "nothing records the session or environment", severity="warn")

    locks = [l for l in LOCKFILES if (root / l).exists()]
    add(findings, bool(locks), "lockfile",
        f"dependency manifest present: {', '.join(locks)}" if locks
        else f"no dependency manifest; looked for {', '.join(LOCKFILES)}")

    abs_hits = []
    for p in code:
        try:
            for m in ABS_PAT.finditer(p.read_text(encoding="utf-8", errors="replace")):
                abs_hits.append(f"{p.relative_to(root)}: {m.group(1)[:60]}")
        except OSError:
            pass
    add(findings, not abs_hits, "relative-paths",
        "no machine-specific absolute paths" if not abs_hits
        else f"{len(abs_hits)} absolute path(s), first: {abs_hits[0]}")

    cred_hits = []
    for p in code:
        try:
            if CRED_PAT.search(p.read_text(encoding="utf-8", errors="replace")):
                cred_hits.append(str(p.relative_to(root)))
        except OSError:
            pass
    add(findings, not cred_hits, "no-credentials",
        "no credential-shaped strings" if not cred_hits
        else f"possible credential in: {', '.join(cred_hits[:3])}")
    return master


def data_manifest(root):
    manifest = {}
    for name in ("data", "Data", "input", "inputs"):
        d = root / name
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file():
                h = hashlib.sha256()
                with p.open("rb") as f:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        h.update(chunk)
                manifest[str(p.relative_to(root))] = {"sha256": h.hexdigest(), "bytes": p.stat().st_size}
    return manifest


def crosswalk_targets(root):
    """Filenames the package claims it produces, read from a crosswalk if present."""
    for name in ("docs/crosswalk.md", "crosswalk.md", "docs/figure-table-crosswalk.md"):
        p = root / name
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="replace")
            return sorted(set(re.findall(r"[\w./-]+\.(?:pdf|png|tex|csv|rds|html)", text))), name
    return [], None


def execute(root, master, findings, timeout):
    if master is None:
        add(findings, False, "clean-room-run", "no master script to run")
        return
    with tempfile.TemporaryDirectory(prefix="replication-verify-") as tmp:
        dest = Path(tmp) / root.name
        shutil.copytree(root, dest, ignore=shutil.ignore_patterns(".git", "renv/library", "__pycache__", ".venv"))
        before = {p for p in dest.rglob("*") if p.is_file()}
        if master == "Makefile":
            cmd = ["make"]
        elif master.lower().endswith(".r"):
            cmd = ["Rscript", master]
        else:
            cmd = [sys.executable, master]
        if shutil.which(cmd[0]) is None:
            add(findings, False, "clean-room-run", f"interpreter not installed: {cmd[0]}")
            return
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, cwd=dest, capture_output=True, text=True, timeout=timeout,
                                  env={**os.environ, "CI": "1"})
        except subprocess.TimeoutExpired:
            add(findings, False, "clean-room-run", f"timed out after {timeout}s")
            return
        secs = round(time.time() - t0, 1)
        ok = proc.returncode == 0
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        add(findings, ok, "clean-room-run",
            f"{' '.join(cmd)} exited {proc.returncode} in {secs}s"
            + ("" if ok else f"; last line: {tail[-1][:200] if tail else '(no output)'}"))

        produced = sorted(str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file() and p not in before)
        add(findings, bool(produced), "outputs-produced",
            f"{len(produced)} new file(s) written" if produced else "the run wrote no new files",
            severity="warn")

        targets, src = crosswalk_targets(root)
        if targets:
            names = {Path(p).name for p in produced}
            missing = [t for t in targets if Path(t).name not in names]
            add(findings, not missing, "crosswalk",
                f"all {len(targets)} outputs in {src} were produced" if not missing
                else f"{len(missing)} of {len(targets)} missing from the run, first: {missing[0]}")
        else:
            add(findings, True, "crosswalk", "no crosswalk found; output coverage NOT CHECKED", severity="warn")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, type=Path, help="the replication package directory")
    ap.add_argument("--run", action="store_true",
                    help="also execute the master script in a temp copy (arbitrary code execution)")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds before the run is abandoned")
    ap.add_argument("--json", action="store_true", help="emit findings.json to stdout")
    a = ap.parse_args()

    root = a.root.expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")

    findings = []
    master = static_checks(root, findings)
    manifest = data_manifest(root)
    add(findings, True, "data-manifest",
        f"{len(manifest)} data file(s) hashed" if manifest else "no data directory found", severity="warn")
    if a.run:
        execute(root, master, findings, a.timeout)
    else:
        add(findings, True, "clean-room-run", "not run; pass --run to execute (NOT CHECKED)", severity="warn")

    failed = [f for f in findings if f["status"] == "fail"]
    report = {"root": str(root), "executed": a.run, "verdict": "fail" if failed else "pass",
              "findings": findings, "data_manifest": manifest}
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        for f in findings:
            print(f"  {f['status'].upper():5} {f['check']:18} {f['detail']}")
        print(f"\nverdict: {report['verdict']} ({len(failed)} failed)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
