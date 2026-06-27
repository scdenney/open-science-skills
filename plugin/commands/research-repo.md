# Research Repository Scaffold & Audit

Scaffold a new research project repository, or audit an existing one, organized around its source library. The source library (`sources/`) is the spine: original PDFs in `og/` (gitignored), LLM-readable Markdown in `md/` (tracked), a drop zone in `unprocessed/`, and a `references.bib` keyed to it. From that spine the skill builds outward — a PDF→Markdown convert script (OpenDataLoader PDF), a `process-source` intake command, `CLAUDE.md`/`AGENTS.md`, `.gitignore`, `.venv`, and the analysis, manuscript, and review folders the project actually needs.

New or empty directory → **scaffold mode**: initialize the spine and the archetype-appropriate folders, set up the conversion toolchain, and smoke-test it. Existing repo → **audit mode**: report what is present, partial, or missing, with detection recipes for orphan PDFs, bib drift, and naming violations. Corpus-free repos (a theory paper with just a `.bib`) are handled without forcing a `sources/` tree.

Pairs with `process-source` (per-PDF intake into this structure) and `replication-package` (the public reproducibility package built near submission).

Pass a target directory as an argument. The skill defaults to the current directory if no path is given.

$ARGUMENTS
