#!/usr/bin/env python3
"""check_deliverable.py -- the deterministic gate for one deliverable.

A deliverable is a directory holding `deliverable.yml` (the manifest) and
`HANDOFF.md`. This script runs the cheap checks the manifest asks for and
exits 1 on any FAIL. It never calls a language model.

    check_deliverable.py                       # every enabled check, no build
    check_deliverable.py --fast [--staged]     # pre-commit profile: offline-tolerant, staged files only
    check_deliverable.py --build               # also run the manifest's build command
    check_deliverable.py ship                  # build + every check + checks/release.json
    check_deliverable.py sections              # the section manifest as JSON
    check_deliverable.py hash                  # sha256 over the deliverable's inputs
    check_deliverable.py accept ID --note TXT  # accept an UNRESOLVED citation by id
    check_deliverable.py --root DIR --json OUT

Checks, each enabled by its key under `checks:` in the manifest:

  manifest     required fields present, sources of truth and handoff exist
  credentials  token patterns in text files
  citations    cite keys resolve in the .bib; author-year and reading-list
               references verified against the .bib, Crossref, and OpenAlex,
               cached in checks/citations.json; a new entry nobody can verify
               blocks the commit until it is accepted with a note
  numbers      the snapshot id matches everywhere it is named; every float in
               the named data tables occurs in the numbers source
  deck_budget  slide text budgets measured from the rendered deck
  facts        expectations against a YAML data file (Jekyll _data)
  leaks        forbidden patterns in sources; unreleased content absent from
               the build (build checks skipped under --fast)
  prose_tells  AI-tell patterns in changed prose; WARN only
  build        the build command exits 0 and its artifacts exist

Manifest sketch (paths are relative to the manifest's directory):

  schema: 1
  id: nwo26-p2-apsa-2026-talk
  kind: talk                    # talk | course | paper | chapter | review
  title: ...
  audience: ...
  deadline: 2026-09-04
  claim: ...
  done: ...
  sources_of_truth: [content.md, notes.md]
  planning_dir: planning
  handoff: HANDOFF.md
  knowledge_base: sources/md        # research-repo layout; warns on cited works with no source file
  sections_from: content-keys   # content-keys | latex | markdown-headings | rmd-chunks | explicit
  sections_files: [content.md]
  build: {command: "python3 src/build.py --html", artifacts: [index.html]}
  checks:
    credentials: true
    citations: {bib: ../../manuscript/references.bib, scan: [content.md], cite_fields: true}
    numbers: {source: ../../manuscript/numbers.tex, snapshot: 2026-08-31T1349Z,
              snapshot_in: [src/build.py], tables: [{file: src/build.py, names: [H1]}]}
    deck_budget: {file: index.html}
    prose_tells: {scan: [notes.md]}
  night_shift: {enabled: false, budget_usd: 3}
"""
import argparse
import ast
import datetime as dt
import difflib
import fnmatch
import hashlib
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("check_deliverable: PyYAML is required (python3 -m pip install pyyaml)")

VERSION = "1.0.0"
MANIFEST_NAME = "deliverable.yml"
TEXT_EXT = {".md", ".tex", ".txt", ".html", ".yml", ".yaml", ".js", ".css", ".rb",
            ".py", ".qmd", ".Rmd", ".rmd", ".bib", ".json", ".toml"}
PROSE_EXT = {".md", ".tex", ".qmd", ".Rmd", ".rmd", ".txt"}
DEFAULT_EXCLUDE = [".git/", "vendor/", "_site", "node_modules/", "checks/", ".venv/",
                   "__pycache__/", "inbox/", ".jekyll-cache/"]
NET_TIMEOUT = 8
MAILTO = os.environ.get("CHECK_DELIVERABLE_MAILTO", "")
USER_AGENT = "check-deliverable/%s%s" % (VERSION, (" (mailto:%s)" % MAILTO) if MAILTO else "")

CRED_PATTERNS = [
    r"gho_[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"AIza[0-9A-Za-z_\-]{30,}", r"sk-[A-Za-z0-9]{20,}", r"xox[baprs]-[A-Za-z0-9\-]{10,}",
    r"QUALTRICS_API_TOKEN\s*[:=]\s*\S+", r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
]

# A short, conservative list. The full catalog lives in writing-toolkit's
# avoid-ai-writing.md; point `prose_tells.patterns_file` at a file with one
# regex per line to extend this.
TELL_PATTERNS = [
    (r"\bdelve[sd]?\b", "delve"), (r"\btapestry\b", "tapestry"),
    (r"\bit(?:'|\u2019)?s worth noting\b", "it's worth noting"), (r"\bin today(?:'|\u2019)?s\b", "in today's"),
    (r"\bearns its keep\b", "earns its keep"), (r"\bat the end of the day\b", "at the end of the day"),
    (r"\ba testament to\b", "a testament to"), (r"\bunderscores? the\b", "underscores the"),
    (r"\bcrucial role\b", "crucial role"), (r"\bmultifaceted\b", "multifaceted"),
    (r"\bthe landscape of\b", "the landscape of"), (r"\bseamlessly\b", "seamlessly"),
    (r"\bleverag(?:e|es|ed|ing)\b", "leverage"), (r"\bgame[- ]changer\b", "game-changer"),
    (r"\bnot only\b[^.\n]{0,80}\bbut also\b", "not only ... but also"),
    (r"^\s*(?:Furthermore|Moreover|Additionally),", "paragraph-opening connective"),
    (r"\u2014", "em dash (house style is a spaced en dash)"),
]

DECK_BUDGET_DEFAULT = {"c2x2": 24, "c2": 46, "rows": 32, "ask": 30, "note": 24, "lede": 30, "h3": 5}


# ----------------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.items = []

    def add(self, check, status, msg, file=None, line=None, **extra):
        item = {"check": check, "status": status, "msg": msg}
        if file is not None:
            item["file"] = str(file)
        if line is not None:
            item["line"] = line
        item.update(extra)
        self.items.append(item)

    def failed(self):
        return any(i["status"] == "FAIL" for i in self.items)

    def summary(self):
        out = {}
        for i in self.items:
            out[i["status"]] = out.get(i["status"], 0) + 1
        return out

    def print(self, root):
        order = {"FAIL": 0, "WARN": 1, "PASS": 2, "SKIP": 3, "INFO": 4}
        for i in sorted(self.items, key=lambda x: (order.get(x["status"], 9), x["check"])):
            loc = ""
            if i.get("file"):
                try:
                    f = os.path.relpath(i["file"], root)
                except ValueError:
                    f = i["file"]
                loc = " [%s%s]" % (f, (":%d" % i["line"]) if i.get("line") else "")
            print("%-4s %-12s %s%s" % (i["status"], i["check"], i["msg"], loc))
        s = self.summary()
        print("--- %s" % ", ".join("%s %d" % (k, v) for k, v in sorted(s.items())))


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def find_manifest(start):
    p = Path(start).resolve()
    for d in [p] + list(p.parents):
        m = d / MANIFEST_NAME
        if m.is_file():
            return m
    return None


def load_manifest(path):
    with open(path, encoding="utf-8") as f:
        m = yaml.safe_load(f) or {}
    if not isinstance(m, dict):
        sys.exit("check_deliverable: %s is not a mapping" % path)
    return m


def rel(root, p):
    return (root / p).resolve() if not os.path.isabs(str(p)) else Path(p)


def read_text(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def git(root, *args):
    try:
        r = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def git_toplevel(root):
    top = git(root, "rev-parse", "--show-toplevel")
    return Path(top) if top else None


def staged_files(root):
    top = git_toplevel(root)
    if not top:
        return set()
    out = git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR") or ""
    return {(top / line).resolve() for line in out.splitlines() if line.strip()}


def excluded(path, root, excludes):
    s = str(path.relative_to(root)) if str(path).startswith(str(root)) else str(path)
    s = s.replace(os.sep, "/") + ("/" if path.is_dir() else "")
    return any(e in s or s.startswith(e) for e in excludes)


def expand_globs(root, patterns, excludes=None, only=None):
    """Files matching any glob under root; `only` restricts to a set of absolute paths."""
    excludes = excludes or DEFAULT_EXCLUDE
    files = []
    for pat in patterns or []:
        pat = str(pat)
        for p in sorted(root.glob(pat)):
            if p.is_file() and not excluded(p, root, excludes):
                files.append(p.resolve())
    files = list(dict.fromkeys(files))
    if only is not None:
        files = [f for f in files if f in only]
    return files


LATEX_ACCENT = re.compile(r"\\[`'^\"~=.uvHtcdbr]\s*\{?\s*([A-Za-z])\s*\}?")


def normalize(s):
    s = LATEX_ACCENT.sub(r"\1", s or "")          # Avi{\~n}a -> Avina before NFKD
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_match(a, b):
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na in nb or nb in na:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=NET_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ----------------------------------------------------------------------------
# checks: manifest, credentials
# ----------------------------------------------------------------------------

def check_manifest(m, root, rep):
    for k in ("id", "kind", "title"):
        if not m.get(k):
            rep.add("manifest", "FAIL", "missing required field `%s`" % k, file=root / MANIFEST_NAME)
    for k in ("audience", "deadline", "claim", "done"):
        if not m.get(k):
            rep.add("manifest", "WARN", "field `%s` is empty" % k, file=root / MANIFEST_NAME)
    for p in m.get("sources_of_truth") or []:
        if not rel(root, p).exists():
            rep.add("manifest", "FAIL", "source of truth missing: %s" % p)
    h = rel(root, m.get("handoff") or "HANDOFF.md")
    if not h.exists():
        rep.add("manifest", "FAIL", "handoff file missing: %s" % h.name)
    else:
        text = read_text(h)
        if not re.search(r"^## ", text, re.M):
            rep.add("manifest", "WARN", "HANDOFF.md has no dated `## ` entry yet", file=h)
    pd = m.get("planning_dir")
    if pd and not rel(root, pd).is_dir():
        rep.add("manifest", "WARN", "planning_dir does not exist: %s" % pd)
    if not rep.failed():
        rep.add("manifest", "PASS", "manifest ok: %s (%s)" % (m.get("id"), m.get("kind")))


def check_credentials(cfg, m, root, rep, only):
    pats = [re.compile(p) for p in CRED_PATTERNS]
    files = expand_globs(root, (cfg.get("scan") if isinstance(cfg, dict) else None) or ["**/*"], only=only)
    hits = 0
    for f in files:
        if f.suffix not in TEXT_EXT or f.name == MANIFEST_NAME:
            continue
        try:
            text = read_text(f)
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for p in pats:
                if p.search(line):
                    hits += 1
                    rep.add("credentials", "FAIL", "possible credential or token", file=f, line=i)
                    break
    if not hits:
        rep.add("credentials", "PASS", "no credential patterns in %d files" % len(files))


# ----------------------------------------------------------------------------
# checks: citations
# ----------------------------------------------------------------------------

CITE_LATEX = re.compile(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}")
CITE_PANDOC_BRACKET = re.compile(r"\[([^\]]*@[^\]]*)\]")
CITE_PANDOC_KEY = re.compile(r"@([A-Za-z][\w:.\-/]*[\w])")
YEAR = re.compile(r"\b((?:19|20)\d{2})[a-z]?\b")
DOI = re.compile(r"\b(10\.\d{4,9}/[^\s\"'<>]+)")


def parse_bib(text):
    """Crude but brace-aware: key -> {author, year, title, doi}."""
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        etype = m.group(1).lower()
        if etype in ("comment", "preamble", "string"):
            continue
        key = m.group(2)
        # body: from after the key to the matching closing brace
        i = m.end()
        depth = 1
        j = i
        while j < len(text) and depth:
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            j += 1
        body = text[i:j - 1]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            name = fm.group(1).lower()
            k = fm.end()
            if k >= len(body):
                break
            if body[k] == "{":
                d, s = 1, k + 1
                e = s
                while e < len(body) and d:
                    if body[e] == "{":
                        d += 1
                    elif body[e] == "}":
                        d -= 1
                    e += 1
                val = body[s:e - 1]
            elif body[k] == '"':
                e = body.find('"', k + 1)
                val = body[k + 1:e if e > 0 else len(body)]
            else:
                e = re.search(r"[,\n]", body[k:])
                val = body[k:k + e.start()] if e else body[k:]
            fields[name] = re.sub(r"\s+", " ", val.replace("{", "").replace("}", "")).strip()
        entries[key] = {
            "author": fields.get("author", fields.get("editor", "")),
            "year": (YEAR.search(fields.get("year", "") + " " + fields.get("date", "")) or [None, ""])[1]
            if YEAR.search(fields.get("year", "") + " " + fields.get("date", "")) else "",
            "title": fields.get("title", ""),
            "doi": fields.get("doi", ""),
            "type": etype,
        }
    return entries


def surnames(author_field):
    """['Sniderman', 'Hagendoorn', 'Prior'] from a bib author field or a deck cite string."""
    out = []
    for part in re.split(r"\s+and\s+|;|&|,\s*(?=[A-Z])", author_field):
        part = part.strip().strip(",")
        if not part or part.lower() in ("et al.", "et al", "others"):
            continue
        if "," in part:  # Last, First
            out.append(part.split(",")[0].strip())
        else:            # First Last
            toks = [t for t in part.split() if t.lower() not in ("et", "al.", "al")]
            if toks:
                out.append(toks[-1])
    return [normalize(s) for s in out if s]


def parse_author_year(ref):
    """'Sniderman, Hagendoorn & Prior 2004' -> ('Sniderman, Hagendoorn & Prior', ['2004'])."""
    years = YEAR.findall(ref)
    if not years:
        return None, []
    first = YEAR.search(ref)
    authors = ref[:first.start()].strip().rstrip(",;")
    return authors, years


def parse_reading_list(text):
    """Reading-list entries from Markdown: bullets with a year and a quoted or italic title.
    A parent bullet `- **Author** ...` supplies the author for indented child bullets."""
    entries = []
    current_author = None
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$", line)
        if not m:
            continue
        indent, body = len(m.group(1)), m.group(2)
        bold = re.match(r"^\\?\*?\s*\*\*([^*]+)\*\*", body)
        if bold and not YEAR.search(re.sub(r"\(.*?\)", "", body)):
            current_author = bold.group(1).strip()
            continue
        if indent == 0:
            current_author = None if not bold else bold.group(1).strip()
        year = None
        ym = YEAR.search(body)
        if ym:
            year = ym.group(1)
        title = None
        q = re.search(r"[\"\u201c]([^\"\u201d]{6,})[\"\u201d]", body)
        it = re.search(r"(?<![*\w])\*([^*]{6,})\*(?!\*)|(?<![_\w])_([^_]{6,})_(?!\w)", body)
        if q:
            title = q.group(1)
        elif it:
            title = it.group(1) or it.group(2)
        if not (year and title):
            continue
        author = None
        if bold:
            author = bold.group(1).strip()
        else:
            pre = body.split(title)[0]
            pre = re.sub(r"[\*_\"\u201c\u201d\\]", "", pre).strip(" ,.:;-\u2013\u2014")
            if pre and not YEAR.fullmatch(pre):
                author = pre
        author = author or current_author
        entries.append({"line": i, "title": title.strip(), "year": year,
                        "author": (author or "").strip(), "doi": (DOI.search(body) or [None, ""])[1]
                        if DOI.search(body) else "", "raw": body.strip()})
    return entries


class CitationCache:
    def __init__(self, path):
        self.path = path
        self.data = {"version": 1, "entries": {}}
        if path.exists():
            try:
                self.data = json.loads(read_text(path))
            except json.JSONDecodeError:
                pass
        self.dirty = False

    @staticmethod
    def ident(kind, ref):
        return hashlib.sha1(("%s|%s" % (kind, normalize(ref))).encode()).hexdigest()[:12]

    def get(self, ident):
        return self.data["entries"].get(ident)

    def put(self, ident, **fields):
        e = self.data["entries"].setdefault(ident, {"first_seen": dt.date.today().isoformat()})
        e.update(fields)
        self.dirty = True
        return e

    def save(self):
        if not self.dirty:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                             encoding="utf-8")


def verify_online(title, year, surname, doi, cache_state):
    """Return (status, doi, matched_title, source). status in VERIFIED/MISMATCH/UNRESOLVED/OFFLINE."""
    if cache_state.get("offline"):
        return "OFFLINE", "", "", ""
    try:
        if doi:
            data = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))
            msg = data.get("message", {})
            t = " ".join(msg.get("title") or [])
            if title and title_match(title, t) < 0.6:
                return "MISMATCH", doi, t, "crossref"
            return "VERIFIED", doi, t, "crossref"
        if not title:
            return "UNRESOLVED", "", "", ""
        q = "https://api.crossref.org/works?rows=4&query.bibliographic=" + urllib.parse.quote(title)
        if surname:
            q += "&query.author=" + urllib.parse.quote(surname)
        data = fetch_json(q)
        for it in data.get("message", {}).get("items", []):
            t = " ".join(it.get("title") or [])
            if title_match(title, t) < 0.85:
                continue
            y = None
            for k in ("issued", "published-print", "published-online", "created"):
                parts = (it.get(k) or {}).get("date-parts") or [[None]]
                if parts and parts[0] and parts[0][0]:
                    y = parts[0][0]
                    break
            if year and y and abs(int(year) - int(y)) > 1:
                continue
            fams = [normalize(a.get("family", "")) for a in it.get("author", [])]
            if surname and fams and normalize(surname) not in fams:
                continue
            return "VERIFIED", it.get("DOI", ""), t, "crossref"
        q = "https://api.openalex.org/works?per-page=4&search=" + urllib.parse.quote(title)
        if MAILTO:
            q += "&mailto=" + urllib.parse.quote(MAILTO)
        data = fetch_json(q)
        for it in data.get("results", []):
            t = it.get("display_name") or ""
            if title_match(title, t) < 0.85:
                continue
            y = it.get("publication_year")
            if year and y and abs(int(year) - int(y)) > 1:
                continue
            names = [normalize(a.get("author", {}).get("display_name", "")) for a in it.get("authorships", [])]
            if surname and names and not any(normalize(surname) in n for n in names):
                continue
            d = (it.get("doi") or "").replace("https://doi.org/", "")
            return "VERIFIED", d, t, "openalex"
        return "UNRESOLVED", "", "", ""
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        cache_state["offline"] = True
        return "OFFLINE", "", "", ""


def check_citations(cfg, m, root, rep, only, fast, warn_unresolved):
    cfg = cfg if isinstance(cfg, dict) else {}
    bib_path = rel(root, cfg["bib"]) if cfg.get("bib") else None
    bib = {}
    if bib_path:
        if not bib_path.exists():
            rep.add("citations", "FAIL", "bib not found: %s" % cfg["bib"])
            return
        bib = parse_bib(read_text(bib_path))
    cache = CitationCache(rel(root, cfg.get("cache") or "checks/citations.json"))
    state = {}
    scan = expand_globs(root, cfg.get("scan") or [], only=only)
    n_keys = n_ok = 0
    problems = 0
    resolved_keys = set()

    def policy(status, ident, ref, f, line, kind):
        nonlocal problems
        e = cache.get(ident) or {}
        if status == "VERIFIED":
            return
        if status == "MISMATCH":
            problems += 1
            rep.add("citations", "FAIL", "%s: DOI resolves to a different work: %s" % (kind, ref), file=f, line=line, id=ident)
        elif status == "OFFLINE":
            rep.add("citations", "WARN", "%s: could not verify (offline): %s" % (kind, ref), file=f, line=line, id=ident)
        elif e.get("accepted"):
            return
        else:
            sev = "WARN" if warn_unresolved else "FAIL"
            if sev == "FAIL":
                problems += 1
            rep.add("citations", sev, "%s: unverified, accept with `check_deliverable.py accept %s --note \"...\"`: %s"
                    % (kind, ident, ref), file=f, line=line, id=ident)

    for f in scan:
        text = read_text(f)
        lines = text.splitlines()
        # 1. keys
        keys = []
        for mm in CITE_LATEX.finditer(text):
            for k in mm.group(1).split(","):
                k = k.strip()
                if k and k != "*":
                    keys.append((k, text.count("\n", 0, mm.start()) + 1))
        if cfg.get("pandoc", True) and f.suffix in (".md", ".qmd", ".Rmd", ".rmd"):
            for mm in CITE_PANDOC_BRACKET.finditer(text):
                for k in CITE_PANDOC_KEY.findall(mm.group(1)):
                    keys.append((k, text.count("\n", 0, mm.start()) + 1))
        for k, line in keys:
            n_keys += 1
            if bib and k not in bib:
                problems += 1
                rep.add("citations", "FAIL", "cite key not in bib: %s" % k, file=f, line=line)
            else:
                n_ok += 1
        # 2. deck cite fields (content-keys files): `@N.x.cite` -> "Author Year; Author & Author Year"
        if cfg.get("cite_fields") and f.suffix == ".md":
            key = None
            for i, line in enumerate(lines, 1):
                if line.startswith("@"):
                    key = line[1:].strip()
                    continue
                if key and line.strip() and not line.startswith(("##", "//")):
                    if key.endswith(".cite"):
                        refs = re.split(r";", htmlmod.unescape(line))
                    else:
                        # author-year citations embedded in a text field, e.g. "(Ogura et al. 2026)"
                        refs = [r for grp in re.findall(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*)\)", htmlmod.unescape(line))
                                for r in grp.split(";") if re.search(r"[A-Z][A-Za-z\u00C0-\u024F'\-]+.*\b(?:19|20)\d{2}", r)]
                    for ref in refs:
                        ref = ref.strip()
                        if not ref:
                            continue
                        authors, years = parse_author_year(ref)
                        if not years:
                            continue
                        sn = surnames(authors)
                        for y in years:
                            ident = cache.ident("author-year", "%s %s" % (authors, y))
                            hit = None
                            for bk, be in bib.items():
                                if be["year"] == y and sn and surnames(be["author"])[:1] == sn[:1]:
                                    hit = bk
                                    break
                            if hit:
                                status = "VERIFIED"
                                resolved_keys.add(hit)
                                cache.put(ident, ref="%s %s" % (authors, y), kind="author-year", status=status,
                                          bib_key=hit, source="bib", checked_at=dt.date.today().isoformat(),
                                          file=str(f.relative_to(root)), line=i)
                                n_ok += 1
                            else:
                                e = cache.get(ident)
                                status = e.get("status", "UNRESOLVED") if e else "UNRESOLVED"
                                if status not in ("VERIFIED",):
                                    status = "UNRESOLVED"
                                cache.put(ident, ref="%s %s" % (authors, y), kind="author-year", status=status,
                                          source="bib" if bib else "none", checked_at=dt.date.today().isoformat(),
                                          file=str(f.relative_to(root)), line=i)
                            n_keys += 1
                            policy(status, ident, "%s %s" % (authors, y), f, i, "author-year")
        # 3. reading lists
        if cfg.get("reading_lists") and f.suffix in (".md", ".qmd"):
            for ent in parse_reading_list(text):
                ident = cache.ident("reading-list", "%s|%s|%s" % (ent["author"], ent["year"], ent["title"]))
                e = cache.get(ident)
                n_keys += 1
                if e and e.get("status") == "VERIFIED":
                    n_ok += 1
                    continue
                if e and e.get("accepted"):
                    continue
                sn = surnames(ent["author"])
                status, doi, mt, src = verify_online(ent["title"], ent["year"], sn[0] if sn else "", ent["doi"], state)
                if status != "OFFLINE":
                    cache.put(ident, ref=ent["raw"][:200], kind="reading-list", status=status, doi=doi,
                              matched_title=mt, source=src, checked_at=dt.date.today().isoformat(),
                              file=str(f.relative_to(root)), line=ent["line"], title=ent["title"],
                              year=ent["year"], author=ent["author"])
                if status == "VERIFIED":
                    n_ok += 1
                policy(status, ident, ent["raw"][:120], f, ent["line"], "reading-list")
    # 4. the bib itself
    if bib and cfg.get("verify_bib"):
        for k, be in bib.items():
            if not be["title"]:
                continue
            ident = cache.ident("bib-entry", "%s|%s|%s" % (be["author"], be["year"], be["title"]))
            e = cache.get(ident)
            if e and (e.get("status") == "VERIFIED" or e.get("accepted")):
                continue
            sn = surnames(be["author"])
            status, doi, mt, src = verify_online(be["title"], be["year"], sn[0] if sn else "", be["doi"], state)
            if status != "OFFLINE":
                cache.put(ident, ref=k, kind="bib-entry", status=status, doi=doi, matched_title=mt, source=src,
                          checked_at=dt.date.today().isoformat(), file=str(bib_path.relative_to(root))
                          if str(bib_path).startswith(str(root)) else str(bib_path))
            policy(status, ident, "%s (%s %s, %s)" % (k, sn[0] if sn else "?", be["year"], be["title"][:60]), bib_path, None, "bib-entry")
    # 5. knowledge base coverage: a cited, resolved bib key with no Markdown source file
    kb = m.get("knowledge_base")
    if kb and bib:
        kbdir = rel(root, kb)
        if not kbdir.is_dir():
            rep.add("citations", "WARN", "knowledge_base dir not found: %s" % kb)
        else:
            have = {f.stem.lower() for f in kbdir.glob("*.md")}
            cited = {k for f in scan for k in re.findall(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}", read_text(f)) for k in k.split(",")}
            cited = {k.strip() for k in cited if k.strip() in bib} | resolved_keys
            missing_kb = sorted(k for k in cited if not any(h.startswith(k.lower()) for h in have))
            for k in missing_kb[:40]:
                rep.add("citations", "WARN", "cited but not in the knowledge base (run process-source): %s" % k)
            rep.add("citations", "INFO", "knowledge base: %d of %d cited works have a source file in %s" % (len(cited) - len(missing_kb), len(cited), kb))
    cache.save()
    if not problems:
        rep.add("citations", "PASS", "%d references checked, %d resolved" % (n_keys, n_ok))
    if state.get("offline"):
        rep.add("citations", "WARN", "network unavailable; online verification deferred")


def cmd_accept(args, m, root):
    cfg = (m.get("checks") or {}).get("citations") or {}
    cache = CitationCache(rel(root, cfg.get("cache") or "checks/citations.json"))
    matches = [k for k in cache.data["entries"] if k.startswith(args.ident)]
    if len(matches) != 1:
        sys.exit("accept: %d entries match %r" % (len(matches), args.ident))
    cache.put(matches[0], accepted=True, note=args.note, accepted_at=dt.date.today().isoformat())
    cache.save()
    print("accepted %s: %s" % (matches[0], cache.get(matches[0]).get("ref")))


# ----------------------------------------------------------------------------
# checks: numbers
# ----------------------------------------------------------------------------

NUM = re.compile(r"-?\d+(?:\.\d+)?|-?\.\d+")


def numbers_from_tex(text):
    vals = set()
    for mm in re.finditer(r"\\csname\s+rr@[^\\]+\\endcsname\s*\{(.*)\}\s*$|\\(?:re)?newcommand\*?\{\\[\w@]+\}\s*(?:\[\d\])?\{(.*)\}\s*$",
                          text, re.M):
        raw = (mm.group(1) or mm.group(2) or "").replace("\u2212", "-").replace("$", "").replace("{", "").replace("}", "")
        for n in NUM.findall(raw):
            try:
                vals.add(round(float(n), 6))
            except ValueError:
                pass
    return vals


def walk_numbers(obj, path, out):
    if isinstance(obj, bool):
        return
    if isinstance(obj, float):
        out.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk_numbers(v, "%s.%s" % (path, k), out)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            walk_numbers(v, "%s[%d]" % (path, i), out)


def check_numbers(cfg, m, root, rep):
    cfg = cfg if isinstance(cfg, dict) else {}
    srcs = cfg.get("source", "")
    srcs = srcs if isinstance(srcs, list) else [srcs]
    files = []
    for s_ in srcs:
        hits = sorted(root.glob(str(s_))) if any(ch in str(s_) for ch in "*?[") else [rel(root, s_)]
        files.extend(h for h in hits if h.exists())
    if not files:
        rep.add("numbers", "FAIL", "numbers source not found: %s" % cfg.get("source"))
        return
    src = next((f for f in files if f.name == "numbers.tex"), files[0])
    text = "\n".join(read_text(f) for f in files)
    snap = str(cfg.get("snapshot") or "")
    if snap:
        pat = cfg.get("snapshot_pattern") or r"Snapshot of record:\s*(\S+)"
        mm = re.search(pat, text)
        if not mm:
            rep.add("numbers", "WARN", "no snapshot line in %s" % src.name, file=src)
        elif mm.group(1) != snap:
            rep.add("numbers", "FAIL", "snapshot mismatch: manifest %s, source %s" % (snap, mm.group(1)), file=src)
        for p in cfg.get("snapshot_in") or []:
            fp = rel(root, p)
            if not fp.exists():
                rep.add("numbers", "WARN", "snapshot_in file missing: %s" % p)
            elif snap not in read_text(fp):
                rep.add("numbers", "FAIL", "snapshot id %s not named in %s" % (snap, p), file=fp)
    vals = numbers_from_tex(text)
    if not vals:
        rep.add("numbers", "WARN", "no numeric macros found in %s" % src.name, file=src)
        return
    checked = missing = 0
    for t in cfg.get("tables") or []:
        fp = rel(root, t.get("file", ""))
        if not fp.exists():
            rep.add("numbers", "FAIL", "table file missing: %s" % t.get("file"))
            continue
        try:
            tree = ast.parse(read_text(fp))
        except SyntaxError as e:
            rep.add("numbers", "FAIL", "cannot parse %s: %s" % (fp.name, e), file=fp)
            continue
        wanted = set(t.get("names") or [])
        found = set()
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                    and node.targets[0].id in wanted:
                name = node.targets[0].id
                found.add(name)
                try:
                    val = ast.literal_eval(node.value)
                except (ValueError, SyntaxError):
                    rep.add("numbers", "WARN", "%s is not a literal; skipped" % name, file=fp, line=node.lineno)
                    continue
                leaves = []
                walk_numbers(val, name, leaves)
                for path, v in leaves:
                    checked += 1
                    if round(v, 6) not in vals:
                        missing += 1
                        rep.add("numbers", "FAIL", "%s = %s not in %s" % (path, v, src.name), file=fp, line=node.lineno)
        for name in wanted - found:
            rep.add("numbers", "WARN", "table %s not found in %s" % (name, fp.name), file=fp)
    if not missing:
        rep.add("numbers", "PASS", "%d table values present in %s (snapshot %s)" % (checked, src.name, snap or "n/a"))


# ----------------------------------------------------------------------------
# checks: deck budget (from lint_deck.py)
# ----------------------------------------------------------------------------

def _words(s):
    s = re.sub(r"<span class=\"cite\">.*?</span>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s).replace("\u2019", "'")
    return len([w for w in s.split() if any(c.isalnum() for c in w)])


def check_deck_budget(cfg, m, root, rep):
    cfg = cfg if isinstance(cfg, dict) else {}
    fp = rel(root, cfg.get("file") or "index.html")
    if not fp.exists():
        rep.add("deck_budget", "SKIP", "deck not built yet: %s" % fp.name)
        return
    budget = dict(DECK_BUDGET_DEFAULT)
    budget.update(cfg.get("budgets") or {})
    src = read_text(fp)
    slides = re.findall(r'<section class="slide[^"]*">(.*?)</section>', src, re.S)
    bad = 0
    for n, sl in enumerate(slides, 1):
        title = re.search(r"<h2[^>]*>(.*?)</h2>", sl, re.S)
        title = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else "(title slide)"
        for grid in re.finditer(r'<div class="cards ([a-z0-9 ]+)">(.*?)\n\s*</div>', sl, re.S):
            kind = grid.group(1).split()[0]
            cap = budget.get(kind, budget["c2"])
            for card in re.findall(r'<div class="card">(.*?)</div>', grid.group(2), re.S):
                h3 = re.search(r"<h3[^>]*>(.*?)</h3>", card, re.S)
                label = re.sub(r"<[^>]+>", "", h3.group(1)).strip() if h3 else "?"
                body = re.sub(r"<h3[^>]*>.*?</h3>", "", card, flags=re.S)
                w = _words(body)
                if w > cap:
                    bad += 1
                    rep.add("deck_budget", "FAIL", "slide %d %s: card '%s' %dw > %dw" % (n, title[:24], label[:24], w, cap), file=fp)
                if h3 and len(label.split()) > budget["h3"]:
                    bad += 1
                    rep.add("deck_budget", "FAIL", "slide %d %s: heading '%s' %d words > %d" % (n, title[:24], label, len(label.split()), budget["h3"]), file=fp)
        for cls in ("ask", "note", "lede"):
            for mm in re.finditer(r'<(?:p|span) class="%s[^"]*"[^>]*>(.*?)</(?:p|span)>' % cls, sl, re.S):
                w = _words(mm.group(1))
                if w > budget[cls]:
                    bad += 1
                    rep.add("deck_budget", "FAIL", "slide %d %s: .%s %dw > %dw" % (n, title[:24], cls, w, budget[cls]), file=fp)
    if not bad:
        rep.add("deck_budget", "PASS", "%d slides within text budgets" % len(slides))


# ----------------------------------------------------------------------------
# checks: facts, leaks, prose tells, build
# ----------------------------------------------------------------------------

def eval_path(data, path):
    cur = data
    for tok in path.split("."):
        if tok == "length":
            return len(cur)
        if tok == "sum":
            return sum(cur)
        star = tok.endswith("[*]")
        name = tok[:-3] if star else tok
        if name:
            if isinstance(cur, list):
                cur = [c.get(name) if isinstance(c, dict) else None for c in cur]
            else:
                cur = cur.get(name) if isinstance(cur, dict) else None
        if star and not isinstance(cur, list):
            cur = list(cur) if cur is not None else []
    return cur


def norm_val(v):
    if isinstance(v, list):
        return [norm_val(x) for x in v]
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    return str(v) if not isinstance(v, (int, float, bool)) or isinstance(v, bool) else v


def check_facts(cfg, m, root, rep):
    cfg = cfg if isinstance(cfg, dict) else {}
    fp = rel(root, cfg.get("data", ""))
    if not fp.exists():
        rep.add("facts", "FAIL", "data file not found: %s" % cfg.get("data"))
        return
    with open(fp, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    bad = 0
    for ex in cfg.get("expect") or []:
        path, want = ex.get("path"), ex.get("equals")
        try:
            got = eval_path(data, path)
        except (AttributeError, TypeError, KeyError) as e:
            bad += 1
            rep.add("facts", "FAIL", "%s: cannot evaluate (%s)" % (path, e), file=fp)
            continue
        g, w = norm_val(got), norm_val(want)
        if isinstance(g, (int, float)) and isinstance(w, str):
            w = type(g)(w) if re.fullmatch(r"-?\d+(\.\d+)?", w) else w
        if g != w:
            bad += 1
            rep.add("facts", "FAIL", "%s = %r, expected %r" % (path, got, want), file=fp)
    if not bad:
        rep.add("facts", "PASS", "%d expectations hold in %s" % (len(cfg.get("expect") or []), fp.name))


def check_leaks(cfg, m, root, rep, only, fast):
    cfg = cfg if isinstance(cfg, dict) else {}
    excludes = DEFAULT_EXCLUDE + [str(e) for e in cfg.get("exclude") or []]
    pats = [(re.compile(p), p) for p in cfg.get("forbidden_patterns") or []]
    bad = 0
    if pats:
        files = expand_globs(root, cfg.get("source_globs") or ["**/*.md", "**/*.html", "**/*.yml", "**/*.yaml", "**/*.js", "**/*.css", "**/*.rb"],
                             excludes=excludes, only=only)
        for f in files:
            text = read_text(f)
            for i, line in enumerate(text.splitlines(), 1):
                for p, raw in pats:
                    if p.search(line):
                        bad += 1
                        rep.add("leaks", "FAIL", "forbidden pattern /%s/" % raw, file=f, line=i)
    build_dir = rel(root, cfg["build_dir"]) if cfg.get("build_dir") else None
    if build_dir and not fast:
        if not build_dir.is_dir():
            rep.add("leaks", "SKIP", "build dir absent: %s" % cfg["build_dir"])
        else:
            for p in cfg.get("forbidden_paths") or []:
                for hit in build_dir.glob(str(p)):
                    bad += 1
                    rep.add("leaks", "FAIL", "forbidden path in build: %s" % hit.relative_to(build_dir))
            g = cfg.get("gated")
            if g:
                with open(rel(root, g["data"]), encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                items = data.get(g["list"]) or []
                if isinstance(items, dict):
                    items = [items]
                for it in items:
                    slug = it.get(g.get("slug", "slug"))
                    released = bool(it.get(g.get("flag", "released")))
                    page = build_dir / g["build_path"].format(slug=slug)
                    if released and not page.exists():
                        bad += 1
                        rep.add("leaks", "FAIL", "released item missing from build: %s" % slug)
                    if not released and page.exists():
                        bad += 1
                        rep.add("leaks", "FAIL", "unreleased item leaked into build: %s" % slug)
            for p in cfg.get("required_paths") or []:
                if not (build_dir / str(p)).exists():
                    bad += 1
                    rep.add("leaks", "FAIL", "required build path missing: %s" % p)
    if not bad:
        rep.add("leaks", "PASS", "no leaks%s" % (" (build checks deferred under --fast)" if fast and build_dir else ""))


def check_prose_tells(cfg, m, root, rep, only):
    cfg = cfg if isinstance(cfg, dict) else {}
    pats = list(TELL_PATTERNS)
    pf = cfg.get("patterns_file")
    if pf and rel(root, pf).exists():
        for line in read_text(rel(root, pf)).splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pats.append((line, line))
    files = [f for f in expand_globs(root, cfg.get("scan") or ["**/*.md", "**/*.tex", "**/*.qmd", "**/*.Rmd"], only=only)
             if f.suffix in PROSE_EXT]
    n = 0
    for f in files:
        for i, line in enumerate(read_text(f).splitlines(), 1):
            if line.lstrip().startswith(("//", "%", "@")):
                continue
            for p, label in pats:
                if re.search(p, line, re.I | re.M):
                    n += 1
                    if n <= int(cfg.get("max_report", 30)):
                        rep.add("prose_tells", "WARN", "tell: %s" % label, file=f, line=i)
                    break
    rep.add("prose_tells", "PASS" if not n else "INFO", "%d tell%s in %d prose files" % (n, "" if n == 1 else "s", len(files)))


def check_build(m, root, rep):
    b = m.get("build") or {}
    cmd = b.get("command")
    if not cmd:
        rep.add("build", "SKIP", "no build command in manifest")
        return
    try:
        r = subprocess.run(cmd, shell=True, cwd=str(root), capture_output=True, text=True, timeout=int(b.get("timeout", 600)))
    except subprocess.TimeoutExpired:
        rep.add("build", "FAIL", "build timed out: %s" % cmd)
        return
    if r.returncode != 0:
        tail = (r.stderr or r.stdout).strip().splitlines()[-3:]
        rep.add("build", "FAIL", "build failed (%d): %s" % (r.returncode, " | ".join(tail)))
        return
    missing = [a for a in b.get("artifacts") or [] if not rel(root, a).exists()]
    if missing:
        rep.add("build", "FAIL", "artifacts missing after build: %s" % ", ".join(missing))
    else:
        rep.add("build", "PASS", "build ok: %s" % cmd)


# ----------------------------------------------------------------------------
# sections, hash, ship
# ----------------------------------------------------------------------------

def sections(m, root):
    mode = m.get("sections_from") or ("explicit" if m.get("sections") else "markdown-headings")
    files = [rel(root, f) for f in (m.get("sections_files") or m.get("sources_of_truth") or [])]
    out = []
    if mode == "explicit":
        for i, s in enumerate(m.get("sections") or [], 1):
            out.append(s if isinstance(s, dict) else {"id": "s%02d" % i, "title": str(s)})
        return out
    for fp in files:
        if not fp.exists():
            continue
        lines = read_text(fp).splitlines()
        marks = []
        if mode == "content-keys":
            for i, line in enumerate(lines, 1):
                mm = re.match(r"^##\s*(\d+[A-Za-z]?|[A-Za-z]+\s+\d+[A-Za-z]?)\s*[\u00b7\-\u2013:]?\s*(.*)$", line)
                if mm:
                    marks.append((i, mm.group(1).replace(" ", "-"), mm.group(2).strip() or mm.group(1)))
        elif mode == "latex":
            for i, line in enumerate(lines, 1):
                mm = re.match(r"^\s*\\(?:section|subsection|chapter)\*?\{([^}]*)\}", line)
                if mm:
                    marks.append((i, None, mm.group(1)))
        elif mode == "rmd-chunks":
            for i, line in enumerate(lines, 1):
                mm = re.match(r"^```\{r\s*([\w\-]*)", line)
                if mm:
                    marks.append((i, mm.group(1) or None, mm.group(1) or "chunk"))
        else:  # markdown-headings
            for i, line in enumerate(lines, 1):
                mm = re.match(r"^(#{1,3})\s+(.*)$", line)
                if mm:
                    marks.append((i, None, mm.group(2).strip()))
        for k, (line, ident, title) in enumerate(marks):
            end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(lines)
            out.append({"id": ident or "s%02d" % (len(out) + 1), "title": title,
                        "file": str(fp.relative_to(root)) if str(fp).startswith(str(root)) else str(fp),
                        "line": line, "end_line": end})
    return out


def input_files(m, root):
    files = [root / MANIFEST_NAME]
    for p in m.get("sources_of_truth") or []:
        files.append(rel(root, p))
    ch = m.get("checks") or {}
    cit = ch.get("citations") if isinstance(ch.get("citations"), dict) else {}
    for p in cit.get("scan") or []:
        files.extend(expand_globs(root, [p]))
    if cit.get("bib"):
        files.append(rel(root, cit["bib"]))
    num = ch.get("numbers") if isinstance(ch.get("numbers"), dict) else {}
    if num.get("source"):
        files.append(rel(root, num["source"]))
    return sorted({f for f in files if f.exists()})


def input_hash(m, root):
    h = hashlib.sha256()
    for f in input_files(m, root):
        h.update(str(f).encode())
        h.update(sha256_file(f).encode())
    return h.hexdigest()


def write_receipt(m, root, rep, args=None):
    top = git_toplevel(root)
    receipt = {
        "id": m.get("id"), "kind": m.get("kind"), "written": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "manifest_sha256": sha256_file(root / MANIFEST_NAME),
        "git": {"head": git(root, "rev-parse", "HEAD"), "dirty": bool(git(root, "status", "--porcelain", "--", ".")),
                "submodules": (git(top, "submodule", "status") or "").splitlines() if top else []},
        "inputs": {str(f.relative_to(root)) if str(f).startswith(str(root)) else str(f): sha256_file(f) for f in input_files(m, root)},
        "artifacts": {a: sha256_file(rel(root, a)) for a in (m.get("build") or {}).get("artifacts") or [] if rel(root, a).exists()},
        "input_hash": input_hash(m, root),
        "checks": rep.summary(), "lint_waived": bool(getattr(args, "no_lint", False)) or not (m.get("ship") or {}).get("require_lint", m.get("kind") != "module"),
        "items": [i for i in rep.items if i["status"] in ("FAIL", "WARN")],
    }
    out = root / "checks" / "release.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return out


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def run_checks(m, root, rep, fast, staged, build, warn_unresolved):
    only = staged_files(root) if staged else None
    if staged and not only:
        rep.add("manifest", "INFO", "nothing staged under this deliverable")
    ch = m.get("checks") or {}
    check_manifest(m, root, rep)
    if ch.get("credentials", True):
        check_credentials(ch.get("credentials"), m, root, rep, only)
    if ch.get("citations"):
        check_citations(ch["citations"], m, root, rep, only, fast, warn_unresolved)
    if ch.get("numbers"):
        check_numbers(ch["numbers"], m, root, rep)
    if build:
        check_build(m, root, rep)
    if ch.get("deck_budget"):
        check_deck_budget(ch["deck_budget"], m, root, rep)
    if ch.get("facts"):
        check_facts(ch["facts"], m, root, rep)
    if ch.get("leaks"):
        check_leaks(ch["leaks"], m, root, rep, only, fast)
    if ch.get("prose_tells"):
        check_prose_tells(ch["prose_tells"], m, root, rep, only)


def main(argv=None):
    ap = argparse.ArgumentParser(description="deterministic gate for one deliverable")
    ap.add_argument("command", nargs="?", default="check", choices=["check", "ship", "sections", "hash", "accept"])
    ap.add_argument("ident", nargs="?", help="citation id for `accept`")
    ap.add_argument("--root", help="deliverable directory (default: nearest deliverable.yml upward from cwd)")
    ap.add_argument("--fast", action="store_true", help="pre-commit profile: no build, offline-tolerant")
    ap.add_argument("--staged", action="store_true", help="restrict scans to files staged in git")
    ap.add_argument("--build", action="store_true", help="run the manifest's build command")
    ap.add_argument("--warn-unresolved", action="store_true", help="report unverified citations as WARN, not FAIL")
    ap.add_argument("--json", help="write the report as JSON to this path")
    ap.add_argument("--no-lint", action="store_true", help="ship without an editorial lint (recorded in the receipt)")
    ap.add_argument("--note", default="", help="note for `accept`")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args(argv)

    mpath = (Path(args.root).resolve() / MANIFEST_NAME) if args.root else find_manifest(os.getcwd())
    if not mpath or not mpath.exists():
        sys.exit("check_deliverable: no %s found%s" % (MANIFEST_NAME, " under " + args.root if args.root else " upward from cwd"))
    root = mpath.parent
    m = load_manifest(mpath)

    if args.command == "sections":
        print(json.dumps(sections(m, root), indent=1, ensure_ascii=False))
        return 0
    if args.command == "hash":
        print(input_hash(m, root))
        return 0
    if args.command == "accept":
        if not args.ident:
            sys.exit("accept needs an id")
        cmd_accept(args, m, root)
        return 0

    rep = Report()
    ship = args.command == "ship"
    run_checks(m, root, rep, fast=args.fast and not ship, staged=args.staged and not ship,
               build=(args.build or ship), warn_unresolved=args.warn_unresolved)
    receipt = None
    if ship:
        # a release needs a current, complete lint with no open P0 (or an explicit --no-lint)
        runs = [p for p in (root / "checks").glob("*/findings.json")] if (root / "checks").is_dir() else []
        def run_key(p):
            mm = re.match(r"(\d{4}-\d{2}-\d{2})(?:-(\d+))?$", p.parent.name)
            return (mm.group(1), int(mm.group(2) or 1)) if mm else ("", 0)
        runs.sort(key=run_key)
        require = (m.get("ship") or {}).get("require_lint", m.get("kind") != "module")
        waived = args.no_lint or not require
        if not runs:
            rep.add("ship", "WARN" if waived else "FAIL", "no lint run under checks/%s" % ("; lint not required for this deliverable (run deliverable-lint if you want one)" if not require else ("; shipping without editorial review (--no-lint)" if args.no_lint else "; run deliverable-lint or pass --no-lint")))
        else:
            try:
                fj = json.loads(read_text(runs[-1])); v = fj.get("meta", {}).get("verdict") or {}
                name = runs[-1].parent.name
                sev = "WARN" if waived else "FAIL"
                if fj.get("meta", {}).get("input_hash") != input_hash(m, root):
                    rep.add("ship", sev, "latest lint (%s) predates the current inputs; rerun deliverable-lint" % name)
                if v and not v.get("coverage_complete", True):
                    rep.add("ship", sev, "latest lint (%s) has incomplete coverage" % name)
                p0 = [f for f in fj.get("findings", []) if f.get("severity") == "P0" and f.get("disposition", "open") == "open"]
                if p0:
                    rep.add("ship", "FAIL", "%d open P0 finding(s) in %s" % (len(p0), name))
            except (json.JSONDecodeError, OSError):
                rep.add("ship", "FAIL", "could not read %s" % runs[-1])
    if ship and not rep.failed():
        receipt = write_receipt(m, root, rep, args)
        rep.add("ship", "PASS", "release receipt written: %s" % receipt.relative_to(root))
    elif ship:
        rep.add("ship", "FAIL", "no receipt: fix the failures above")
    rep.print(root)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps({
            "root": str(root), "id": m.get("id"), "written": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "mode": args.command + (" --fast" if args.fast else "") + (" --staged" if args.staged else ""),
            "items": rep.items, "summary": rep.summary(), "exit_code": 1 if rep.failed() else 0,
            "receipt": str(receipt) if receipt else None,
        }, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return 1 if rep.failed() else 0


if __name__ == "__main__":
    sys.exit(main())
