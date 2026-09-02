---
name: replication-package
description: Scaffold or audit a social-science replication package, and audit the manuscript and its archived research objects against the FAIR principles. Scaffold mode writes the folder structure, README, master.R, figure/table crosswalk, codebook template, LICENSE placeholder, .gitignore, and pre-release checklist. Audit mode grades an existing package against that checklist and runs the FAIR block over data, code, materials, prompts, preregistrations, DOIs, metadata, licenses, access restrictions, and availability statements. Use when setting up or repairing a replication package, checking one before submission, auditing research objects against FAIR (Findable, Accessible, Interoperable, Reusable), or drafting and verifying data-, code-, and materials-availability statements. Adapted from Yusaku Horiuchi's replication-package-guide; platform-neutral (Harvard Dataverse, OSF, Zenodo, GitHub releases, institutional archives).
argument-hint: "[path to replication folder, plus manuscript path or availability statements when auditing; package path defaults to ./replication]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Replication Package

## Heritage and attribution

The structural conventions here — single entry point, compact vs. build/analyze layouts, the figure/table crosswalk, the paper-consistency check, the pre-release checklist — come from **Yusaku Horiuchi**'s [replication-package-guide](https://github.com/yhoriuchi/replication-package-guide), whose README explicitly authorizes agent consumption: it is "designed to be read by humans and by coding agents such as Codex or Claude Code before they prepare, audit, or repair a replication package."

This skill modifies rather than copies that guide. The FAIR principles are folded in (Findable, Accessible, Interoperable, Reusable; [Wilkinson et al. 2016](https://doi.org/10.1038/sdata.2016.18); [GO FAIR](https://www.go-fair.org/fair-principles/)) so the scaffolded package is platform-neutral, and platform-specific upload mechanics are dropped: build and audit the local package, generate no upload code. Uploading to Harvard Dataverse, OSF, Zenodo, a journal repository, or an institutional archive belongs to the user and the platform's own tools.

Horiuchi's caveat carries over: "AI is useful for checking, reorganizing, documenting, and catching inconsistencies, but it should not be treated as a substitute for the author's judgment about which files, scripts, data sources, and results are actually part of the replication record." If the user publishes a package built with this skill, cite Horiuchi's guide as the methodological source.

## Standard

A replication package is ready when a competent reader can download it, open the package root, run one documented command, and regenerate the published results without hidden manual steps. `master.R` is the entry-point convention; `run_replication.R` is acceptable where that is already the project's convention. The **Pre-Release Checklist** below enumerates what "ready" requires.

The FAIR principles are the second standard, applied to every research object the manuscript depends on. FAIR does **not** mean everything must be openly downloadable. Sensitive or restricted data can be FAIR when metadata, access conditions, identifiers, and reuse terms are explicit. The practical standard is "as open as possible, as restricted as necessary." Core references for the FAIR block: Wilkinson et al. (2016) for the principles, GO FAIR for the F/A/I/R subprinciples, OSF documentation for repository metadata and data archiving, FORCE11 for data citation principles, and TOP/DA-RT for manuscript transparency expectations.

## Instructions

### Step 1. Resolve the target directory

Use `$ARGUMENTS` if provided. Treat the argument as the path to the replication folder (relative or absolute). If the argument is empty, ask the user once for a path. If they decline, default to `./replication` relative to the current working directory.

Normalize the path. Confirm whether the directory exists and whether it is empty.

If the user also supplied a manuscript, a repository URL, or pasted availability statements, note them — the audit mode's FAIR block needs them.

### Step 2. Choose scaffold or audit

- Target directory is empty or does not exist → **scaffold mode**. Go to Step 3.
- Target directory contains files, or the user asked for a FAIR check, a pre-submission audit, or a review of an existing package → **audit mode**. Go to Step 6.

In audit mode, never overwrite an existing file without explicit user confirmation. Offer to fill in only the missing scaffolding — files that do not yet exist.

## Scaffold mode

### Step 3. Decide on structure

Ask the user one question. Is data construction complex (restricted sources, scraping, API pulls, or expensive upstream work that produces analysis-ready data)?

- **No** → use **compact**.
- **Yes** → use **build/analyze**.

When in doubt, choose compact. Build/analyze is justified only when the build stage creates real complexity for users.

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

### Step 5. Write template files and report

Use the templates in the **Templates** section below. Fill in placeholder fields (`<paper title>`, `<authors>`, etc.) with values the user provides; if a placeholder cannot be resolved from context, leave it as written and flag it in the final report so the user knows what to edit.

The templates are written for the **compact** layout. When scaffolding **build/analyze**, adapt the paths as you write them: `code/` → `build/scripts/` and `analyze/scripts/`, `outputs/` → `analyze/`, `docs/` → `analyze/docs/` — in the README's file descriptions and in every `source()` line of `master.R`.

Then output a short report with:

1. The directory tree created.
2. A list of placeholder fields the user must fill in.
3. The next three actions the user should take (typically: fill in README placeholders, drop data into `data/`, add scripts under `code/` or `build/scripts/` and `analyze/scripts/`).

## Audit mode

One audit, two blocks. The **package block** grades the local package against the Pre-Release Checklist and the Paper Consistency Check. The **FAIR block** grades the manuscript and every archived research object against Findable, Accessible, Interoperable, and Reusable. Run both when a manuscript is available; run the package block alone when only the directory was supplied.

### Step 6. Package block

Read everything in the target directory. Grade it against the **Pre-Release Checklist** and, when manuscript source or a final PDF is available, the **Paper Consistency Check** below. Report each item as present, partial, or missing, with the file or path that supports the verdict.

### Step 7. FAIR block — inventory research objects

Before judging FAIR compliance, list every research object the manuscript depends on, whether or not it is inside the package:

- Raw data, cleaned data, derived data, and analysis-ready data.
- Analysis code, simulation code, randomization scripts, package lockfiles, and notebooks.
- Survey instruments, treatments, vignettes, questionnaires, prompts, codebooks, classification labels, OCR prompts, and annotation guidelines.
- Figures, tables, model outputs, topic models, classifiers, trained weights, dictionaries, and corpora.
- Preregistrations, PAPs, IRB/ethics protocols, consent language, and data-use agreements.
- Third-party data or proprietary inputs that cannot be redistributed.

If an object is not shareable, it still needs metadata and a clear access or non-availability explanation.

### Step 8. FAIR block — Findable

For each research object, verify:

- Repository or landing page exists and is public or publicly discoverable.
- Persistent identifier exists or is planned: DOI, ARK, Handle, OSF registration DOI, Zenodo DOI, Dataverse DOI, ICPSR study ID, or equivalent.
- Metadata includes title, creators/contributors, description, date/version, resource type, keywords/tags, funder when relevant, related publication DOI, and related object links.
- Data/code/materials are cited in the manuscript or reference list, not only mentioned in prose.
- File names are interpretable and map to manuscript tables, figures, or analyses — the crosswalk checked in the package block is the evidence for this.

Prompt the author if missing: repository URL, DOI/identifier, title, contributors, version/date, and how each object maps to manuscript claims.

### Step 9. FAIR block — Accessible

Verify:

- Access route is clear: open download, embargoed release date, controlled access, data-use agreement, request email/form, or legal/ethical non-availability.
- Protocol is standard and durable: repository landing page, HTTPS, institutional repository, OSF, Dataverse, Zenodo, ICPSR, Dryad, GitHub+Zenodo, or discipline repository.
- Restricted data have public metadata and explicit criteria for access.
- Sensitive data are not uploaded to unsuitable repositories; OSF should not be used for sensitive or personally identifiable health information.
- Availability statements match actual repository state.
- Embargoes and anonymous peer-review links are handled without breaking post-publication access.

Prompt the author if missing: access restrictions, embargo date, contact process, data-use agreement, privacy constraints, and post-acceptance public URL.

### Step 10. FAIR block — Interoperable

Verify that others can read and combine the materials:

- Data use non-proprietary or widely readable formats where possible: CSV/TSV, TXT, JSON, Parquet, RDS with fallback, Stata with codebook, PDF/A for documents.
- Variables, labels, missing values, scales, treatment arms, weights, and derived variables are documented — `docs/codebook.md`, checked in the package block, is where this lives.
- Code has an environment file or setup notes: `renv.lock`, `requirements.txt`, `environment.yml`, Dockerfile, session info, package versions, or OS notes. `session_info.log` from `master.R` satisfies the session-info half but not the lockfile.
- Metadata follows a discipline-appropriate standard where available: DDI for social-science survey data, DataCite metadata, repository community schemas, or structured README.
- Cross-links connect raw data, cleaned data, code, figures/tables, and manuscript claims.

Prompt the author if missing: codebook, README, variable dictionary, software environment, data provenance, or mapping from files to outputs.

### Step 11. FAIR block — Reusable

Verify:

- License is explicit for each shareable object: data, code, text/materials, and figures may need different licenses. The package block checks that `LICENSE` is filled in; this check asks whether one license covers objects that need several.
- Reuse conditions are clear for third-party, proprietary, copyrighted, or restricted materials.
- Provenance is documented: collection method, source, cleaning steps, transformations, exclusions, and version history.
- Minimal replication path is documented: what script to run, in what order, and what output it produces — the single-entry-point requirement in the Pre-Release Checklist.
- Ethics and consent allow the claimed sharing level.
- Data/code/material citations give credit to creators and make reuse citable.

Prompt the author if missing: license choices, consent/sharing compatibility, restrictions on reuse, provenance notes, and replication instructions.

### Step 12. FAIR block — manuscript statements

Check these sections, or draft them if absent:

- Data Availability Statement.
- Code Availability Statement.
- Materials/Stimuli Availability Statement.
- Preregistration/PAP Statement.
- Ethics/IRB and consent language.
- Funding and conflicts where tied to repository metadata.
- Data/code/material citations in references.

Statements must be specific enough for a reader to find and reuse objects. "Available upon request" is weak unless privacy, legal, or contractual constraints justify it and the access process is concrete.

### Step 13. Audit report

Produce a `Replication Package Audit`. Drop the FAIR sections when no manuscript or repository information was supplied, and say so in the scope line.

```
# Replication Package Audit

Scope:
Package path:
Manuscript files:
Repository/package links checked:
Summary: <N blocking, N recommended, N minor, N author prompts>

## Package Checklist
| Item | PASS/FAIL/PARTIAL/NA | Evidence | Notes |

## Paper Consistency
| Figure/table | In crosswalk | Script | Output on disk | Notes |

## Research Object Inventory
| Object | Location in manuscript | Repository/identifier | Share status | Notes |

## FAIR Checklist
| Object | Findable | Accessible | Interoperable | Reusable | Main gap |

## Blocking Issues
| Location | Dimension | Issue | Fix |

## Recommended Fixes
| Location | Dimension | Issue | Fix |

## Author Prompts
1. <question the author must answer before the statement can be finalized>

## Draft Availability Statements
### Data
### Code
### Materials
### Preregistration

## Missing Scaffolding
<files this skill can create on request; never overwrite existing files>
```

Severity:

- **Blocking:** package does not run from a clean directory; no single entry point; no repository or access route for essential data/code/materials; missing or false availability statement; missing license for reusable data/code; restricted data without access conditions; repository link absent for a claimed open object; sensitive data or credentials exposed inappropriately.
- **Recommended:** DOI pending, metadata thin, README incomplete, codebook missing details, crosswalk incomplete, proprietary format without fallback, no formal data/code citation.
- **Minor:** inconsistent file names, weak tags, style problems in availability statements, minor README clarity issues.

### Audit quality checks

- [ ] The package was graded against the full Pre-Release Checklist, not a subset.
- [ ] All research objects were inventoried before FAIR scoring.
- [ ] FAIR was not treated as identical to open access.
- [ ] Restricted or sensitive data were checked for transparent access conditions rather than forced open sharing.
- [ ] Data, code, and materials were checked as separately licensable objects.
- [ ] Persistent identifiers and repository metadata were checked when links were available.
- [ ] Missing author knowledge was surfaced as explicit prompts.
- [ ] Draft statements are specific enough to locate and reuse the objects.
- [ ] No existing file was overwritten without confirmation.
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

## Compose with sibling skills

- `citation-check` — when repository objects need formal citation or DOI checks.
- `figure-table-audit` — to verify figures and tables trace to repository files or scripts.
- `methods-reporting` — for DA-RT, TOP, JARS, and CONSORT integration, so the methods section reports what the package documents.
- `text-classification`, `topic-modeling`, `vlm-ocr` — when FAIRness depends on prompts, models, corpora, or other derived computational objects.
- `research-repo` — for the surrounding project repository rather than the publication archive.
- `paper-review-lite` or `presubmit` — for full pre-submission review after the audit's fixes are made.
