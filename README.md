<p align="center">
  <img src="assets/hero.jpg" alt="Open Science Skills — vintage typewriter, globe, and books labeled Open Access, Collaboration, Transparency, Reproducibility, beneath a framed title sign." width="900">
</p>

# Open Science Skills

[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://code.claude.com/docs/en/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-library-111111?logo=openai&logoColor=white)](codex/README.md)
[![version](https://img.shields.io/badge/version-2.23.0-blue)](https://github.com/scdenney/open-science-skills/releases)
[![license](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](LICENSE)
[![Claude skills](https://img.shields.io/badge/Claude_skills-42-D97757?logo=anthropic&logoColor=white)](#skills)
[![Codex skills](https://img.shields.io/badge/Codex_skills-40-111111?logo=openai&logoColor=white)](#skills)
[![updated](https://img.shields.io/badge/updated-August%202026-green)](https://github.com/scdenney/open-science-skills/commits/main)
[![sources](https://img.shields.io/badge/sources-150%2B-purple)](SOURCES.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](#contributing)

Open Science Skills is a library of 42 agentic skills for Claude Code, with a parallel 40-skill library for OpenAI Codex, written for computational social scientists and digital humanists. Each skill is meant to work the way the field expects. Identify the data-generating process before proposing an estimator, and design experiments and instruments to a standard. Drafts are held to established reporting norms.

The library follows the research lifecycle. It covers survey design, list experiments, topic modeling, LLM text classification, VLM-based OCR pipelines, manuscript QA, multi-model orchestration, and transparent reporting under APSA, JARS, DA-RT, TOP, and FAIR expectations. Every skill is grounded in published methods sources and based on best practices for writing skills. See [SOURCES.md](SOURCES.md) for the bibliography of 150+ works consulted.

This is the toolkit I use in my own research, and it grows as I add sources and skills. The authoring is mine, with editing help from Opus 5, Fable 5, and ChatGPT 5.5/6.

| Platform | Skills | Invoke |
|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | 44, as the [`oss` plugin](plugin/skills) | `/oss:skill-name` |
| [OpenAI Codex](https://developers.openai.com/codex/skills) | 42, as the [`codex/` library](codex/README.md) | `$skill-name` |

The two libraries differ only in invocation and tooling. The Codex side omits `presubmit`, `fable-orchestrate`, and `opus-orchestrate`, and adds `46-orchestrate`. See [`codex/README.md`](codex/README.md).

[Quick start](#quick-start) · [Skills](#skills) · [Recommended](#recommended-companion-skills) · [How skills trigger](#how-skills-trigger) · [Installation](#installation) · [Sources](#knowledge-base-and-sources) · [Contributing](#contributing) · [License](#license)

---

## Quick start

Install the plugin from the marketplace, user-wide across all projects, or add `--scope project` for one project only:

```bash
# Step 1: Register the marketplace (one-time)
claude plugin marketplace add scdenney/open-science-skills

# Step 2: Install the plugin
claude plugin install oss@open-science-skills

# Project-only install
claude plugin install oss@open-science-skills --scope project
```

Then invoke a skill explicitly, for example `/oss:conjoint-design`, or just describe your task in plain language and let the matching skill load on its own.

On Codex there is no plugin. Install the skills library instead (see [Codex](#codex)).

---

## Skills

Skills are grouped by where they fall in a project. Unless the Platform column says otherwise, a skill runs on both Claude Code (`/oss:name`) and Codex (`$name`). One row, `46-orchestrate`, belongs to the Codex library only and is not part of the 44-skill plugin.

### Project Setup

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [research-repo](plugin/skills/research-repo/SKILL.md) | Both | `/oss:research-repo` | Scaffold a new research project around its source library, or audit an existing one. The sources folder is the spine. From there it builds the references file and the intake tooling, plus the analysis and manuscript folders and a place for reviews. |

### Workflow & Orchestration

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [fable-orchestrate](plugin/skills/fable-orchestrate/SKILL.md) | Claude Code | `/oss:fable-orchestrate` | Run a multi-model workflow with Fable 5 as lead. As the strongest model on the team it keeps the hard reasoning itself. Mechanical work goes to a Sonnet subagent and wide or parallel reasoning to Opus subagents. Calls with a high blast radius that it cannot cheaply verify go to a GPT-5.6 Codex peer for a decorrelated cross-check. |
| [opus-orchestrate](plugin/skills/opus-orchestrate/SKILL.md) | Claude Code | `/oss:opus-orchestrate` | The same workflow with Opus 5 as lead, at medium reasoning effort by default (raise to high for a reasoning-heavy session). Workflow fan-out comes with the skill's own opt-in, so ultracode is not required. Opus reasons on hard problems itself and delegates only to fan out. The Codex peer is gpt-5.6-sol. |
| [spawn](plugin/skills/spawn/SKILL.md) | Both | `/oss:spawn` | Spawn full peer sessions in new terminal panes — real sessions, not subagents — each in its own git worktree on a directed task with a contract brief. Detects herdr, tmux, or a plain terminal and takes the strongest path; the lead monitors without babysitting and merges each branch back. |
| [advisor](plugin/skills/advisor/SKILL.md) | Both | `/oss:advisor` / `$advisor` | Consult an independent second reviewer before committing to an interpretation or calling a task done. Your session is the main seat, on Opus 5 or on Sonnet 5 for cheaper sustained work. The advisor seat is Fable 5, pinned to max reasoning effort. The [Codex counterpart](codex/advisor/SKILL.md) always runs Sol/xhigh. |
| [46-orchestrate](codex/46-orchestrate/SKILL.md) | Codex | `$46-orchestrate` | Sol at high effort owns orchestration and sign-off. It routes bounded work to Terra workers and reserves Luna for tightly specified mechanical work. |

### Ideation

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [diverge](plugin/skills/diverge/SKILL.md) | Both | `/oss:diverge` | Before implementing, generate three to five distinct approaches labeled by how they differ, then pause for you to choose, instead of defaulting to the first obvious solution. |
| [diverge-codex](plugin/skills/diverge-codex/SKILL.md) | Both | `/oss:diverge-codex` | The same brainstorm-then-select, but Codex (GPT-5.6 Sol at xhigh, from Claude Code) generates the alternatives, so a second model family widens the range. |

### Research Design

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [research-wayfinder](plugin/skills/research-wayfinder/SKILL.md) | Both | `/oss:research-wayfinder` | Plan a study as a decision map that outlives any single session — typed tickets for estimand, identification, power, and measurement, resolved one per session until the design is pre-registerable. Adapted from Matt Pocock's wayfinder. |
| [conjoint-design](plugin/skills/conjoint-design/SKILL.md) | Both | `/oss:conjoint-design` | Design conjoint experiments, including the attribute architecture and the statistical power that architecture implies. Covers AMCE and AMIE estimation. |
| [conjoint-diagnostics](plugin/skills/conjoint-diagnostics/SKILL.md) | Both | `/oss:conjoint-diagnostics` | Check a conjoint design and its analysis for integrity, measurement error, external validity, and sound interpretation. |
| [conjoint-cleaning](plugin/skills/conjoint-cleaning/SKILL.md) | Both | `/oss:conjoint-cleaning` | Reshape a Qualtrics conjoint export into analysis-ready long format, with choice mapping, translation, pilot detection, and validation. |
| [survey-design](plugin/skills/survey-design/SKILL.md) | Both | `/oss:survey-design` | Write survey instruments. Covers question wording, scales, flow, pretesting, respondent burden, and social-desirability mitigation. |
| [qualtrics-ops](plugin/skills/qualtrics-ops/SKILL.md) | Both | `/oss:qualtrics-ops` | Operate a live Qualtrics survey via the v3 APIs without breaking fielding. Covers publish gating, quotas, flow routing, embedded data, panel-vendor redirects, and read-back verification. |
| [survey-flow-audit](plugin/skills/survey-flow-audit/SKILL.md) | Both | `/oss:survey-flow-audit` | Pre-fielding audit of a live survey over the platform API, with an optional browser walk. Covers consent-before-anything gates, publish state, force-response completeness, quotas, vendor redirects, anti-bot instrumentation, and language-arm symmetry. |
| [survey-data-audit](plugin/skills/survey-data-audit/SKILL.md) | Both | `/oss:survey-data-audit` | Audit fielded survey response data for registered elements, data quality, bot and AI-automation screening, and sample integrity. Emits an appendix-ready quality report. |
| [cross-national-design](plugin/skills/cross-national-design/SKILL.md) | Both | `/oss:cross-national-design` | Design survey experiments that run across countries, with per-country power and measurement equivalence checks. Includes instrument localization. |
| [list-experiment](plugin/skills/list-experiment/SKILL.md) | Both | `/oss:list-experiment` | Design and diagnose list experiments (the item count technique), from sensitivity assessment through estimation and placebo checks. |

### Analysis

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [topic-modeling](plugin/skills/topic-modeling/SKILL.md) | Both | `/oss:topic-modeling` | Fit structural topic models, choosing the topic count by coherence and exclusivity rather than by eye. Covers covariate specification and what to report. |
| [text-classification](plugin/skills/text-classification/SKILL.md) | Both | `/oss:text-classification` | Classify text with LLMs. Covers codebook design, human-in-the-loop workflows, validation, and agreement statistics. |
| [model-council-voting](plugin/skills/model-council-voting/SKILL.md) | Both | `/oss:model-council-voting` | Use a panel of models as independent coders under a consensus rule stated in advance, then read their disagreement with chance-corrected agreement statistics (the kappa and alpha families). Includes checks for correlated errors across jurors. |
| [model-committee](plugin/skills/model-committee/SKILL.md) | Both | `/oss:model-committee`, `/oss:model-committee-fable`, `/oss:model-committee-sol` | Have GPT-5.6 and Claude Opus 5 deliberate toward one decision. They propose independently, critique each other, revise, and converge under a rule fixed before they start. The chair is a parameter: Opus 5 by default, Fable 5 for a lighter chair outside the vote, or GPT-5.6 Sol, which also drops the GPT member to Terra so the chair is not also a member. |
| [llm-calibration-logprobs](plugin/skills/llm-calibration-logprobs/SKILL.md) | Both | `/oss:llm-calibration-logprobs` | Turn token log-probabilities into per-decision confidence, then measure calibration against human labels (ECE and Brier scores, plus reliability diagrams). |

### Corpus Processing

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [vlm-ocr-pipeline](plugin/skills/vlm-ocr-pipeline/SKILL.md) | Both | `/oss:vlm-ocr-pipeline` | Build an OCR pipeline on vision-language models. Covers model choice, image handling, prompts, batching, evaluation, and reproducibility. |
| [post-ocr-cleanup](plugin/skills/post-ocr-cleanup/SKILL.md) | Both | `/oss:post-ocr-cleanup` | Clean OCR output with LLM and rule-based correction, quality diagnostics, multilingual handling, and provenance tracking. |
| [vlm-ocr-evaluation](plugin/skills/vlm-ocr-evaluation/SKILL.md) | Both | `/oss:vlm-ocr-evaluation` | Compare OCR systems before a bulk run, using stratified ground truth and CER/WER reported per language and per stratum. |

### Writing & Reporting

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [hypothesis-building](plugin/skills/hypothesis-building/SKILL.md) | Both | `/oss:hypothesis-building` | Turn a research question into falsifiable causal hypotheses using DAGs, counterfactuals, equivalence testing, and a stated smallest effect size of interest. |
| [literature-review](plugin/skills/literature-review/SKILL.md) | Both | `/oss:literature-review` | Build or audit a literature review. Produces an evidence map, an assessment of the closest prior work, gap verdicts, and a synthesis plan. |
| [narrative-building](plugin/skills/narrative-building/SKILL.md) | Both | `/oss:narrative-building` | Draft or audit a paper's introduction so it gets from the "why" to the "if-then," and keep multi-experiment papers coherent. |
| [pre-registration-writing](plugin/skills/pre-registration-writing/SKILL.md) | Both | `/oss:pre-registration-writing` | Write a pre-analysis plan. Covers structure, registry choice, analysis strategy, and how to document any deviations. |
| [methods-reporting](plugin/skills/methods-reporting/SKILL.md) | Both | `/oss:methods-reporting` | Check a methods section against a 40-item reporting checklist drawn from CONSORT and JARS, plus the DA-RT transparency standards. |
| [paper-tex](plugin/skills/paper-tex/SKILL.md) | Both | `/oss:paper-tex` | Typeset a draft as house-style LaTeX from Markdown, Word, or other formats. Builds the PDF and prepares it for a specific journal. |

### Figures & Tables

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [figures](plugin/skills/figures/SKILL.md) | Both | `/oss:figures` | Design publication-quality figures. Covers chart choice, scales, color, legend order, self-contained captions, and reproducible code. |
| [tables](plugin/skills/tables/SKILL.md) | Both | `/oss:tables` | Design publication-quality tables. Covers column order, row grouping, precision and uncertainty, self-contained notes, and reproducible code. |

### Manuscript QA

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [fair-check](plugin/skills/fair-check/SKILL.md) | Both | `/oss:fair-check` | Audit a finished manuscript against FAIR principles. Checks that data, code, materials, and prompts are available under stated licenses and persistent identifiers, with reuse conditions spelled out. |
| [citation-check](plugin/skills/citation-check/SKILL.md) | Both | `/oss:citation-check` | Check citations for in-text and reference parity, then for working DOIs and fabrication risk (via Crossref and OpenAlex). Also checks citation style. |
| [fact-check](plugin/skills/fact-check/SKILL.md) | Both | `/oss:fact-check` | Verify that each in-text claim is actually supported by its cited source, reading the source's Markdown in the project's knowledge base. Runs citation-check first. |
| [figure-table-audit](plugin/skills/figure-table-audit/SKILL.md) | Both | `/oss:figure-table-audit` | Audit the finished figure and table set for cross-references, text consistency, accessibility, and links to supplementary and replication materials. |
| [replication-package](plugin/skills/replication-package/SKILL.md) | Both | `/oss:replication-package` | Scaffold or audit a replication package. Generates the folder structure, README, master script, figure/table crosswalk, codebook, license, and pre-release checklist. |

### Review & Submission

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [paper-review-lite](plugin/skills/paper-review-lite/SKILL.md) | Both | `/oss:paper-review-lite` | Run a pre-submission self-audit of your own manuscript across argument, numbers, references, writing, figures, and replication. |
| [paper-review-lite-codex](plugin/skills/paper-review-lite-codex/SKILL.md) | Both | `/oss:paper-review-lite-codex` | The same audit run across two model families. Claude and Codex (GPT-5.6 Sol at xhigh) review independently, then cross-check each other, and every surviving issue is tagged by confidence. |
| [presubmit](plugin/skills/presubmit/SKILL.md) | Claude Code | `/oss:presubmit` | Set up and run the standalone [presubmit CLI](https://github.com/scdenney/presubmit), a heavier 30-plus-stage adversarial review pipeline driven by the Anthropic API. |
| [journal-review](plugin/skills/journal-review/SKILL.md) | Both | `/oss:journal-review` | Draft a senior referee report on someone else's manuscript, using parallel finder agents and a chief-reviewer synthesis to produce a structured report. |

---

## Recommended companion skills

Third-party skills this library recommends and builds on — credited, not claimed, and not counted in the badges. From [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): **grill-me** (a frontier-rounds design interview; pairs with `diverge`, settling the question before the approaches diverge), **wayfinder** (decision-map planning for software work; the source concept for `research-wayfinder`), and **handoff / claude-handoff** (handoff documents for a successor session; the seed of `spawn`). See [RECOMMENDED.md](RECOMMENDED.md) for the full write-up and [`third-party/mattpocock/`](third-party/mattpocock) for pinned, unmodified reference copies.

---

## How skills trigger

Most skills load on their own. When your prompt matches a skill's description, Claude Code or Codex reads that skill into context and follows it, so you usually don't need to name anything. You can also invoke any skill explicitly, with `/oss:skill-name` in Claude Code or `$skill-name` in Codex.

The orchestration and delegated-review skills (`fable-orchestrate`, `opus-orchestrate`, `46-orchestrate`, `spawn`, `advisor`, `model-committee` and its chair variants, `diverge-codex`, and `paper-review-lite-codex`) run only when invoked explicitly, because they start subagents, full peer sessions, or an external model.

---

## Installation

### Claude Code

The recommended install is the plugin, shown in [Quick start](#quick-start). It registers the marketplace and installs all 42 skills and their slash commands. The command prefix is `oss:`, for open science skills. The marketplace and the repository are both named `open-science-skills`.

To try the plugin for one session without installing:

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills && claude --plugin-dir ./plugin
```

<details>
<summary><b>Selective install</b> — pick specific skills (auto-trigger only, no slash commands)</summary>

Clone the repository and run the interactive installer, which lists the skills and installs your choices to `./.claude/skills/` (current project) by default:

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills
bash plugin/scripts/install.sh
```

Other targets and non-interactive selection:

```bash
# Install to user-wide skills directory (all projects)
bash plugin/scripts/install.sh --target ~/.claude/skills

# Install specific skills non-interactively
bash plugin/scripts/install.sh --skill conjoint-design survey-design list-experiment

# Install all skills
bash plugin/scripts/install.sh --all --target ~/.claude/skills
```

Restart Claude Code after installing.

</details>

<details>
<summary><b>Manual copy</b> — a single skill by hand (auto-trigger only)</summary>

Copy the whole skill folder, since many skills ship reference, asset, or script files their `SKILL.md` points at (replace `your-project` with your project's path):

```bash
git clone https://github.com/scdenney/open-science-skills.git

# Project-level (current project only) — copy the whole skill folder:
# many skills ship reference/, assets/, or scripts/ files their SKILL.md points at
mkdir -p your-project/.claude/skills
cp -R open-science-skills/plugin/skills/conjoint-design \
   your-project/.claude/skills/

# User-wide (all projects)
mkdir -p ~/.claude/skills
cp -R open-science-skills/plugin/skills/list-experiment ~/.claude/skills/
```

Manual copy gives auto-trigger only. Slash commands require the plugin.

</details>

### Codex

Codex discovers skills under `.agents/skills` (repository) and `~/.agents/skills` (user-wide). From the repository root, install all 40 skills user-wide:

```bash
mkdir -p "$HOME/.agents/skills"
for skill in "$PWD"/codex/*/; do
  ln -sfn "${skill%/}" "$HOME/.agents/skills/$(basename "$skill")"
done
```

For selective and repository-scoped install, plus the Codex catalog, see [`codex/README.md`](codex/README.md).

---

## Knowledge base and sources

The skills are built from a curated corpus of methods texts rather than the model's built-in knowledge. [SOURCES.md](SOURCES.md) is the full bibliography (150+ works). The [`knowledge_base/`](knowledge_base) folder holds Markdown conversions of those sources that the skills read directly when a task needs chapter-and-verse support, as `fact-check` does when it verifies a claim against its citation.

---

## Contributing

Pull requests are welcome. To add a skill:

1. Write `plugin/skills/<name>/SKILL.md`, following the [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
2. Add `plugin/commands/<name>.md` (a one-paragraph activation prompt plus `$ARGUMENTS`, following the existing examples).
3. Mirror the skill to `plugin/.skills/<name>.md`, byte-identical.
4. Add the Codex package at `codex/<name>/` (`SKILL.md` and `agents/openai.yaml`), unless the skill is intentionally platform-specific.
5. Add sources to `SOURCES.md`.
6. Update the catalogs and badges, then run `bash plugin/scripts/check.sh`.

## License

This project is licensed under [Creative Commons Attribution-NonCommercial 4.0 International](LICENSE). The skills are intended for noncommercial scholarly and educational use.

The `citation-check`, `literature-review`, `figures`, `tables`, and `figure-table-audit` skills remix workflow ideas from [Cheng-I Wu's Academic Research Skills for Claude Code](https://github.com/Imbad0202/academic-research-skills), also licensed CC BY-NC 4.0. The instructions here are rewritten for this repository's open-science and experimental-social-science scope.

The `replication-package` skill adapts the structural conventions in [Yusaku Horiuchi's replication-package-guide](https://github.com/yhoriuchi/replication-package-guide) (the source for single-entry-point, compact vs. build/analyze layouts, figure/table crosswalk, paper-consistency check, correction workflow, and pre-release checklist). FAIR-principle integration and Claude Code/Codex skill packaging are added on top. Harvard Dataverse and other platform-specific upload mechanics are not included. Cite Horiuchi's guide if you publish a package built with this skill.

The `spawn` and `research-wayfinder` skills adapt concepts from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): `spawn` generalizes his `claude-handoff` from one background successor to managed multi-session peers, and `research-wayfinder` reworks his `wayfinder` decision map from software specs to experimental design. Unmodified reference copies of the originals are vendored under [`third-party/mattpocock/`](third-party/mattpocock) with his MIT license; see [RECOMMENDED.md](RECOMMENDED.md).
