#!/usr/bin/env python3
r"""
format_paper.py — turn a draft in any common format into a house-style working
paper (or journal submission) in LaTeX, and optionally build the PDF.

Pipeline:  INPUT (.md/.docx/.odt/.rtf/.html/.tex)
              -> pandoc -> LaTeX body
              -> wrapped in the house template (assets/) with the EB Garamond
                 preamble, single-spaced title block, intro on its own page,
                 \figcap caption macro, [H] float placement
              -> latexmk -> PDF
              -> latexmk/bibtex byproducts removed (--keep-aux to keep them)

The driver does the mechanical 80%. The house-specific finishing (upgrading
\caption to \figcap with a real note, disclosure sections, SI cross-refs) is
done by hand afterward — see the skill's SKILL.md.

Examples
--------
  # Markdown draft -> single-spaced submission PDF, intro on its own page
  python3 format_paper.py draft.md --out build --title "My Paper" \
      --author "Jane Doe" --abstract "We show ..." --keywords "a; b; c" --build

  # Anonymous submission (blank author), double-spaced, intro on the cover page
  python3 format_paper.py draft.docx --out build --anon --spacing double \
      --cover-page --build

  # Main text + SI together (SI gets SI-A/figure numbering and an xr cross-ref)
  python3 format_paper.py main.md --si si.md --out build --build

The bibliography (`references.bib` by default) and any figures the draft
references by a relative path are copied into the out dir automatically when
they sit next to the input; docx/odt media are extracted there too.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PANDOC_FMT = {
    ".md": "markdown", ".markdown": "markdown", ".txt": "markdown",
    ".docx": "docx", ".odt": "odt", ".rtf": "rtf",
    ".html": "html", ".htm": "html", ".org": "org", ".rst": "rst",
}
# latexmk/bibtex byproducts removed after a successful build (see clean_aux).
AUX_EXTS = ("aux", "bbl", "blg", "fdb_latexmk", "fls", "log", "out", "toc",
            "lof", "lot", "nav", "snm", "vrb", "bcf", "run.xml",
            "synctex.gz", "xdv", "spl")


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def need(tool: str) -> None:
    if shutil.which(tool) is None:
        sys.exit(f"error: required tool not found on PATH: {tool}")


def to_latex_body(src: Path, out_dir: Path, body_name: str) -> None:
    """Convert any supported source to a LaTeX body fragment at out_dir/body_name.
    Pandoc runs with cwd=out_dir so extracted-media paths resolve at build time."""
    out_body = out_dir / body_name
    ext = src.suffix.lower()
    if ext == ".tex":
        text = src.read_text(encoding="utf-8")
        if "\\begin{document}" in text:
            body = text.split("\\begin{document}", 1)[1].rsplit("\\end{document}", 1)[0]
            for pat in (r"\\maketitle", r"\\begin\{abstract\}.*?\\end\{abstract\}",
                        r"\\bibliography\{[^}]*\}", r"\\bibliographystyle\{[^}]*\}",
                        r"\\thispagestyle\{[^}]*\}"):
                body = re.sub(pat, "", body, flags=re.DOTALL)
            print("note: extracted body from a full .tex document")
        else:
            body = text
        out_body.write_text(body, encoding="utf-8")
        return
    fmt = PANDOC_FMT.get(ext)
    if fmt is None:
        sys.exit(f"error: unsupported input extension {ext!r}. "
                 f"Supported: {', '.join(sorted(PANDOC_FMT))}, .tex")
    need("pandoc")
    cmd = ["pandoc", str(src.resolve()), "-f", fmt, "-t", "latex", "--natbib",
           "--wrap=preserve", "-o", body_name]
    if fmt in ("docx", "odt"):
        cmd += ["--extract-media=media"]   # relative to out_dir
    run(cmd, cwd=out_dir)


def here_floats(body_path: Path) -> None:
    """Pin figures and tables exactly where written ([H])."""
    t = body_path.read_text(encoding="utf-8")
    t = re.sub(r"\\begin\{figure\}(?!\[)", r"\\begin{figure}[H]", t)
    t = re.sub(r"\\begin\{table\}(?!\[)", r"\\begin{table}[H]", t)
    body_path.write_text(t, encoding="utf-8")


def stage_local_graphics(body_path: Path, src_dir: Path, out_dir: Path) -> None:
    """Copy figures the body references by a relative path (next to the source)."""
    t = body_path.read_text(encoding="utf-8")
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", t):
        rel = m.group(1)
        if rel.startswith(("/", "media/")) or "media/media" in rel:
            continue
        cand = (src_dir / rel)
        dest = (out_dir / rel)
        if cand.is_file() and not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(cand, dest)
            print(f"staged figure: {rel}")


def fill(template: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def copy_bib(bib: str, search_dirs: list[Path], out_dir: Path) -> None:
    if (out_dir / f"{bib}.bib").exists():
        return
    for d in search_dirs:
        cand = d / f"{bib}.bib"
        if cand.is_file():
            shutil.copy(cand, out_dir / f"{bib}.bib")
            print(f"staged bibliography: {cand}")
            return


def build(out: Path, stem: str, engine: str) -> bool:
    need("latexmk")
    pdf_engine = "-pdfxe" if engine == "xelatex" else "-pdf"
    try:
        run(["latexmk", pdf_engine, "-bibtex", "-interaction=nonstopmode",
             "-halt-on-error", f"{stem}.tex"], cwd=out)
    except subprocess.CalledProcessError:
        log = (out / f"{stem}.log")
        tail = ""
        if log.exists():
            errs = [ln for ln in log.read_text(errors="ignore").splitlines()
                    if ln.startswith("! ") or "Error" in ln or "not found" in ln]
            tail = "\n".join(errs[:8])
        print(f"BUILD FAILED for {stem}.tex:\n{tail or '(see ' + str(log) + ')'}", file=sys.stderr)
        return False
    pdf = out / f"{stem}.pdf"
    pages = "?"
    if shutil.which("pdfinfo"):
        m = re.search(r"^Pages:\s+(\d+)", run(["pdfinfo", str(pdf)]).stdout, re.MULTILINE)
        pages = m.group(1) if m else "?"
    print(f"built {pdf}  ({pages} pages)")
    return True


def clean_aux(out: Path, stems: list[str], keep: tuple[str, ...] = ()) -> None:
    """Remove latexmk/bibtex byproducts so the out dir holds only sources,
    staged assets, and PDFs. With an SI, si.aux is kept (passed via `keep`):
    xr-hyper reads it to resolve SI cross-refs when main is rebuilt by hand."""
    removed = 0
    for stem in stems:
        for ext in AUX_EXTS:
            f = out / f"{stem}.{ext}"
            if f.name not in keep and f.exists():
                f.unlink()
                removed += 1
    if removed:
        kept = f" (kept {', '.join(keep)} for SI cross-refs)" if keep else ""
        print(f"cleaned {removed} LaTeX build artifacts{kept}; pass --keep-aux to keep them")


def main() -> None:
    ap = argparse.ArgumentParser(description="Format a draft as a house-style LaTeX paper.")
    ap.add_argument("input", type=Path, nargs="?", help="draft: .md/.docx/.odt/.rtf/.html/.tex")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--si", type=Path, help="supplementary-information source (same formats)")
    ap.add_argument("--title", default="TITLE")
    ap.add_argument("--author", default="")
    ap.add_argument("--abstract", default="")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--date", default="\\today")
    ap.add_argument("--spacing", choices=["single", "double"], default="single",
                    help="body spacing (the title block is always single)")
    ap.add_argument("--anon", action="store_true", help="blank the author (double-anonymous)")
    ap.add_argument("--cover-page", action="store_true",
                    help="keep the intro on the title page (default: intro starts on its own page)")
    ap.add_argument("--bib", default="references", help="bibliography base name (no .bib)")
    ap.add_argument("--no-here-floats", action="store_true", help="do not inject [H] on floats")
    ap.add_argument("--engine", choices=["pdflatex", "xelatex"], default="pdflatex")
    ap.add_argument("--build", action="store_true", help="run latexmk after writing the .tex")
    ap.add_argument("--keep-aux", action="store_true",
                    help="keep latexmk byproducts (.aux/.log/.fls/...) after a successful build")
    ap.add_argument("--clean", action="store_true",
                    help="remove latexmk byproducts from --out and exit (run after hand rebuilds)")
    args = ap.parse_args()

    out: Path = args.out
    if args.clean:
        if not out.is_dir():
            sys.exit(f"error: --out directory not found: {out}")
        stems = sorted({p.stem for p in out.glob("*.tex")}) or ["main", "si"]
        clean_aux(out, stems)
        return
    if args.input is None:
        ap.error("input is required (or pass --clean to tidy an existing --out directory)")
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(ASSETS / "preamble.tex", out / "preamble.tex")
    src_dir = args.input.resolve().parent

    # --- main body ---
    to_latex_body(args.input, out, "body.tex")
    body = out / "body.tex"
    if not args.no_here_floats:
        here_floats(body)
    stage_local_graphics(body, src_dir, out)

    spacing = "\\singlespacing" if args.spacing == "single" else "\\doublespacing"
    titlebreak = "" if args.cover_page else "\\newpage"
    externaldoc = "\\externaldocument{si}" if args.si else ""
    main_tex = fill((ASSETS / "main.template.tex").read_text(encoding="utf-8"), {
        "TITLE": args.title, "AUTHOR": "" if args.anon else args.author, "DATE": args.date,
        "ABSTRACT": args.abstract, "KEYWORDS": args.keywords, "SPACING": spacing,
        "TITLEBREAK": titlebreak, "EXTERNALDOC": externaldoc, "BODYFILE": "body",
        "DISCLOSURES": "", "BIB": args.bib,
    })
    (out / "main.tex").write_text(main_tex, encoding="utf-8")
    print(f"wrote {out/'main.tex'} and {body}")

    # --- optional SI ---
    if args.si:
        to_latex_body(args.si, out, "si_body.tex")
        si_body = out / "si_body.tex"
        if not args.no_here_floats:
            here_floats(si_body)
        stage_local_graphics(si_body, args.si.resolve().parent, out)
        si_tex = fill((ASSETS / "si.template.tex").read_text(encoding="utf-8"), {
            "TITLE": args.title, "AUTHOR": "" if args.anon else args.author,
            "DATE": args.date, "BODYFILE": "si_body", "BIB": args.bib,
        })
        (out / "si.tex").write_text(si_tex, encoding="utf-8")
        print(f"wrote {out/'si.tex'} and {si_body}")

    copy_bib(args.bib, [src_dir, Path.cwd()], out)

    if args.build:
        # SI first: main's \externaldocument{si} reads si.aux, so SI cross-refs
        # resolve on main's first build instead of printing ??.
        ok = build(out, "si", args.engine) if args.si else True
        ok = build(out, "main", args.engine) and ok
        if not ok:
            sys.exit(1)   # keep the .log files for diagnosis
        if not args.keep_aux:
            stems = ["main"] + (["si"] if args.si else [])
            clean_aux(out, stems, keep=("si.aux",) if args.si else ())

    print("\nnext (house-finishing by hand — see SKILL.md):")
    print("  - upgrade each \\caption{...} to \\figcap{title}{note}; put CI/N/source in the note")
    print("  - add disclosure \\section*{Data availability}/{Ethics}/{Funding} as full sentences")
    print("  - thread SI cross-references; remove any bold-period run-in subheaders")


if __name__ == "__main__":
    main()
