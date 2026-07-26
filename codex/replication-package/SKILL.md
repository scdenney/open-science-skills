---
name: replication-package
description: Scaffold or audit a social-science replication package at a target directory. Generates folder structure, README, master.R, figure/table crosswalk, codebook template, LICENSE placeholder, .gitignore, and pre-release checklist. Adapted from Yusaku Horiuchi's replication-package-guide with FAIR-principle integration; platform-neutral (Harvard Dataverse, OSF, Zenodo, GitHub releases, institutional archives).
---

# Replication Package Scaffold

## Heritage and attribution

The structural conventions here — single entry point, compact vs. build/analyze layouts, the figure/table crosswalk, the paper-consistency check, the pre-release checklist — come from **Yusaku Horiuchi**'s [replication-package-guide](https://github.com/yhoriuchi/replication-package-guide), whose README explicitly authorizes agent consumption: it is "designed to be read by humans and by coding agents such as Codex or Claude Code before they prepare, audit, or repair a replication package."

This skill modifies rather than copies that guide. The FAIR principles are folded in (Findable, Accessible, Interoperable, Reusable; [Wilkinson et al. 2016](https://doi.org/10.1038/sdata.2016.18); [GO FAIR](https://www.go-fair.org/fair-principles/)) so the scaffolded package is platform-neutral, and platform-specific upload mechanics are dropped: build and audit the local package, generate no upload code. Uploading to Harvard Dataverse, OSF, Zenodo, a journal repository, or an institutional archive belongs to the user and the platform's own tools.

Horiuchi's caveat carries over: "AI is useful for checking, reorganizing, documenting, and catching inconsistencies, but it should not be treated as a substitute for the author's judgment about which files, scripts, data sources, and results are actually part of the replication record." If the user publishes a package built with this skill, cite Horiuchi's guide as the methodological source.

## Standard

A replication package is ready when a competent reader can download it, open the package root, run one documented command, and regenerate the published results without hidden manual steps. `master.R` is the entry-point convention; `run_replication.R` is acceptable where that is already the project's convention. The **Pre-Release Checklist** below enumerates what "ready" requires.

## Instructions

### Step 1. Resolve the target directory

Treat the path supplied with the invocation as the replication folder, whether relative or absolute. If no path is supplied, ask once; if the user declines, default to `./replication` relative to the current working directory.

Normalize the path. Confirm whether the directory exists and whether it is empty.

### Step 2. Decide on structure

Ask the user one question. Is data construction complex (restricted sources, scraping, API pulls, or expensive upstream work that produces analysis-ready data)?

- **No** → use **compact**.
- **Yes** → use **build/analyze**.

When in doubt, choose compact. Build/analyze is justified only when the build stage creates real complexity for users.

### Step 3. Decide between scaffold and audit

- If the target directory is empty or does not exist → **scaffold mode**. Create the directory if needed, write the full skeleton.
- If the target directory contains files → **audit mode**. Read everything, compare against the pre-release checklist, report what is present, partial, or missing. Offer to fill in only the missing scaffolding (files that do not yet exist). Never overwrite an existing file without explicit user confirmation.

### Step 4. Scaffold the tree

**Compact structure** (default):

```text
<root>/
|-- README.md
|-- master.R
|-- LICENSE
|-- .gitignore
|-- data/
|-- code/
|-- docs/
|   |-- crosswalk.md
|   `-- codebook.md
`-- outputs/
    |-- figures/
    |-- tables/
    `-- logs/
```

**Build/analyze structure**:

```text
<root>/
|-- README.md
|-- master.R
|-- LICENSE
|-- .gitignore
|-- build/
|   |-- data/
|   |-- scripts/
|   `-- output/
`-- analyze/
    |-- data/
    |-- scripts/
    |-- figures/
    |-- tables/
    |-- docs/
    |   |-- crosswalk.md
    |   `-- codebook.md
    `-- logs/
```

Leave `data/`, `code/`, `scripts/`, `figures/`, `tables/`, and `logs/` empty — the user fills them with project content.

### Step 5. Write template files

Use the templates in the **Templates** section below. Fill in placeholder fields (`<paper title>`, `<authors>`, etc.) with values the user provides; if a placeholder cannot be resolved from context, leave it as written and flag it in the final report so the user knows what to edit.

The templates are written for the **compact** layout. When scaffolding **build/analyze**, adapt the paths as you write them: `code/` → `build/scripts/` and `analyze/scripts/`, `outputs/` → `analyze/`, `docs/` → `analyze/docs/` — in the README's file descriptions and in every `source()` line of `master.R`.

### Step 6. Report

After scaffolding, output a short report with:

1. The directory tree created (or the audit diff for audit mode).
2. A list of placeholder fields the user must fill in.
3. The next three actions the user should take (typically: fill in README placeholders, drop data into `data/`, add scripts under `code/` or `build/scripts/` and `analyze/scripts/`).

## Templates

### `README.md`

````markdown
# <paper title>

**Authors.** <author 1>, <author 2>, ...

**Journal.** <journal name>, <year>. DOI: <article DOI>

**Data DOI.** <data archive DOI>

**Verified.** <YYYY-MM-DD>

## What this package reproduces

<one paragraph: which figures, tables, and in-text numbers this package generates from which data.>

## How to run

From a fresh R session in the package root:

```r
source("master.R")
```

`master.R` runs the full public path end-to-end and writes session information and per-script logs to `outputs/logs/` (compact) or `analyze/logs/` (build/analyze).

## Software requirements

- R <version>
- Required packages: <list>
- Operating system tested on: <list>
- Approximate runtime on the listed environment: <time>

A `session_info.log` is written by `master.R` on a successful run and records the exact package versions used.

## Folder structure

<paste the actual tree from `tree -L 2` or list manually>

## Data sources

- **<dataset 1>** — <source, license, public or restricted, citation>.
- **<dataset 2>** — ...

If any input is restricted, document how a reader with access can obtain it and which files in this package depend on it.

## File descriptions

- `master.R` — public entry point.
- `code/01_*.R` — <what it does>.
- `code/02_*.R` — <what it does>.
- `data/<file>.csv` — <one-line description; see `docs/codebook.md` for variables>.
- `docs/crosswalk.md` — paper-order map from figures/tables to scripts and outputs.
- `outputs/figures/`, `outputs/tables/`, `outputs/logs/` — generated by `master.R`.

## Figure and table crosswalk

See `docs/crosswalk.md`. Every figure and table in the paper and its appendix appears there with the script that generates it and the output path.

## Citation

<paper citation in journal style.>

## License

See `LICENSE`. <one sentence: data license, code license, any restrictions>.

## Attribution

This package follows the structural conventions in Yusaku Horiuchi's [replication-package-guide](https://github.com/yhoriuchi/replication-package-guide) and the FAIR principles (Wilkinson et al. 2016, doi:10.1038/sdata.2016.18).
````

### `master.R`

```r
# master.R — public entry point for <paper title> replication package.
# Running this script regenerates every figure, table, and reported number
# from the public input data.

# Reproducibility
set.seed(20260101)              # change to the seed used in the paper

# Capture the start time and prepare the log directory
.start_time <- Sys.time()
log_dir <- "outputs/logs"        # change to "analyze/logs" if build/analyze
if (!dir.exists(log_dir)) dir.create(log_dir, recursive = TRUE)

# Run scripts in order. Add or remove as the project grows.
source("code/01_load.R")         # load and validate inputs
source("code/02_clean.R")        # clean and recode
source("code/03_analysis.R")     # estimate models
source("code/04_figures.R")      # produce figures
source("code/05_tables.R")       # produce tables

# Session info
writeLines(
  capture.output(sessionInfo()),
  file.path(log_dir, "session_info.log")
)

# Runtime
.end_time <- Sys.time()
cat(
  sprintf("Replication complete. Elapsed: %s.\n",
          format(round(.end_time - .start_time, 2)))
)
```

### `docs/crosswalk.md`

```markdown
# Figure and Table Crosswalk

In paper order. Every figure and table in the article and supplementary information must appear in this table. Mark conceptual or hand-made items explicitly.

| # | Type | Label / Caption (short) | Script | Output path |
|---|------|-------------------------|--------|-------------|
| 1 | Figure | <short caption> | `code/04_figures.R` | `outputs/figures/fig01.pdf` |
| 2 | Table | <short caption> | `code/05_tables.R` | `outputs/tables/tab01.tex` |
| 3 | Figure (conceptual) | <short caption> | — | `docs/concept_fig.pdf` (hand-drawn; not generated) |
```

### `docs/codebook.md`

```markdown
# Codebook

One entry per public analysis-ready dataset. List every variable.

## `data/<dataset>.csv`

Source: <where this dataset comes from; raw input, derived, or restricted>.
N rows: <count>.
N cols: <count>.

| Variable | Type | Values / range | Description |
|----------|------|----------------|-------------|
| `id` | integer | 1–N | Respondent identifier. Anonymized. |
| `treatment` | factor | control / T1 / T2 | Experimental assignment. |
| `outcome` | numeric | 0–100 | Primary outcome (see paper §2.1). |
```

### `LICENSE`

```text
# LICENSE — fill this in before publishing.
#
# Common choices for replication materials:
#  - Code: MIT, BSD-3-Clause, or Apache-2.0.
#  - Data: CC0 (waiver) for fully public data, or CC BY 4.0 for attribution-required.
#  - Whole package: CC BY 4.0 is a common single-license choice when code and data ship together.
#
# Restricted-data files cannot be licensed here. Document them in the README.
#
# Replace this file with the chosen license text. Update the README's License section to match.
```

### `.gitignore`

```text
# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
*~

# R
.Rhistory
.RData
.Ruserdata
.Rproj.user/
*.Rcheck/
*.tar.gz

# Python
__pycache__/
*.pyc
.venv/
venv/

# Secrets and local config
.env
.env.*
*.pem
*.key

# Logs from local runs that should not be committed
*.tmp

# Large generated artifacts; comment out if outputs should be tracked
# outputs/figures/*.pdf
# outputs/tables/*.tex
```

## Pre-Release Checklist

Run this after scaffolding is done and the user has filled in placeholders, dropped in data, and written scripts.

- [ ] The package runs in a clean temporary directory.
- [ ] One public entry point runs the full public path with one command.
- [ ] Public scripts are numbered or otherwise ordered.
- [ ] All paths are relative.
- [ ] One authoritative `README.md`, current and matching the files on disk.
- [ ] `docs/codebook.md` has a data dictionary for every public analysis-ready dataset.
- [ ] Figure/table crosswalk in `docs/crosswalk.md` is complete and in paper order.
- [ ] `master.R` produces `session_info.log` and per-script logs recording inputs, sample sizes, and warnings.
- [ ] No credentials, tokens, personal paths, caches, or obsolete exploratory scripts in the public path.
- [ ] Data inputs are public, or restricted inputs are documented in the README with access instructions and the files that depend on them.
- [ ] `LICENSE` is filled in.
- [ ] The final archive has been downloaded from the destination repository and re-run from a clean directory.

The repository copy is the truth. A local run is necessary but not sufficient.

## Paper Consistency Check

When the manuscript source or final PDF is available, verify:

- Every figure and table cited in the paper and appendix appears in `docs/crosswalk.md`.
- Every generated figure or table path in the crosswalk exists on disk.
- All in-text sample sizes, estimates, confidence intervals, p-values, field dates, and descriptive numbers can be traced to logs, scripts, generated tables, or generated figures.
- Conceptual or hand-made items are marked as such in the crosswalk.
- The public archive reproduces the figures and tables actually reported in the published article.

If paper source files cannot be included publicly, document whether they were used during package preparation.

## When to reach for this skill vs. siblings

- `replication-package` (this) — scaffold or audit a replication package at a target directory before upload to any repository.
- `fair-check` — audit a finished manuscript and its accompanying package against the FAIR principles end-to-end. Use after this skill, before submission.
- `methods-reporting` — check that the manuscript's methods section reports what the package documents (CONSORT, JARS, DA-RT).
