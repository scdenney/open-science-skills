# Knowledge Base

Source materials for the open-science skills — original PDFs and LLM-readable Markdown conversions of everything cited in `/SOURCES.md`.

## Structure

```
knowledge_base/
├── og/              # Original PDFs (gitignored; local-only)
│   ├── general/
│   ├── conjoint-design/
│   ├── conjoint-diagnostics/
│   ├── conjoint-data-cleaning/
│   ├── survey-design/
│   ├── cross-national-design/
│   ├── hypothesis-building/
│   ├── narrative-building/
│   ├── pre-registration/
│   ├── methods-reporting/
│   ├── topic-modeling/
│   ├── text-classification/
│   ├── list-experiment/
│   ├── vlm-ocr/
│   └── post-ocr-cleanup/
├── md/              # Markdown conversions (tracked in git) — mirrors og/ categories
├── unprocessed/     # Staging area for new PDFs (gitignored)
├── TODO_ACQUIRE.md  # Sources that could not be auto-downloaded; user must fetch
└── README.md
```

## Naming convention

All files use `author-year-slug` format, lowercase with hyphens:
- Up to three authors, then year, then a 2–4 word content slug
- Example: `hainmueller-hopkins-yamamoto-2014-causal-inference-conjoint.pdf`
- Name the PDF this way when placing it in `og/<category>/`; conversion keeps the name for the `.md`

## Categories

Categories mirror the sections in `/SOURCES.md`. A single paper may be relevant to more than one skill; place it in its primary category and reference from others via `SOURCES.md`.

## Adding a new source

1. Place the PDF in `knowledge_base/og/<category>/` using the naming convention
2. Run `./scripts/convert-sources.sh` from the repo root
3. The script only converts files that don't already have a `.md` counterpart
4. Commit the new `.md` (and any `_images/` folder) under `knowledge_base/md/<category>/`

## Reconverting everything

```bash
./scripts/convert-sources.sh --all
```

## Requirements

- Python venv at repo root `.venv/` with `opendataloader-pdf` installed
- `pandoc` (for `.docx` files)
- Java 11+ (required by opendataloader-pdf)

## Why Markdown?

PDFs are poorly suited for LLM consumption. Markdown conversions preserve text, headings, and references in a format LLMs can read directly — enabling source-grounded skill authoring, fact-checking, and citation.

## What's tracked in git

- `md/` (Markdown conversions, including `*_images/` subfolders)
- `README.md`, `TODO_ACQUIRE.md`

## What's NOT tracked (local-only)

- `og/` (original PDFs — copyrighted material)
- `unprocessed/` (staging)
- `.venv/`
