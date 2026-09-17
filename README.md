<p align="center">
  <img src="assets/hero.jpg" alt="Open Science Skills, vintage typewriter, globe, and books labeled Open Access, Collaboration, Transparency, Reproducibility, beneath a framed title sign." width="900">
</p>

# Open Science Skills

[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://code.claude.com/docs/en/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-library-111111?logo=openai&logoColor=white)](codex/README.md)
[![version](https://img.shields.io/badge/version-2.29.1-blue)](https://github.com/scdenney/open-science-skills/releases)
[![license](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](LICENSE)
[![Claude skills](https://img.shields.io/badge/Claude_skills-43-D97757?logo=anthropic&logoColor=white)](#skills)
[![Codex skills](https://img.shields.io/badge/Codex_skills-42-111111?logo=openai&logoColor=white)](#skills)
[![updated](https://img.shields.io/badge/updated-September%202026-green)](https://github.com/scdenney/open-science-skills/commits/main)
[![sources](https://img.shields.io/badge/sources-150%2B-purple)](SOURCES.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](#contributing)

Open Science Skills is a library of 41 agentic skills for Claude Code, with a parallel 40-skill library for OpenAI Codex, written for computational social scientists and digital humanists. Each skill is meant to work the way the field expects. Identify the data-generating process before proposing an estimator, and design experiments and instruments to a standard. Drafts are held to established reporting norms.

The library follows the research lifecycle. It covers survey design, list experiments, topic modeling, LLM text classification, VLM-based OCR pipelines, manuscript QA, multi-model orchestration, and transparent reporting under APSA, JARS, DA-RT, TOP, and FAIR expectations. Every skill is grounded in published methods sources and based on best practices for writing skills. See [SOURCES.md](SOURCES.md) for the bibliography of 150+ works consulted.

This is the toolkit I use in my own research, and it grows as I add sources and skills. The authoring is mine, with editing help from Opus 5, Fable 5.1, and ChatGPT 5.5/6.

| Platform | Skills | Invoke |
|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | 43, as the [`oss` plugin](plugin/skills) | `/oss:skill-name` |  
| [OpenAI Codex](https://developers.openai.com/codex/skills) | 42, as the [`codex/` library](codex/README.md) | `$skill-name` |  

The two libraries differ only in invocation and tooling. The Codex side omits `presubmit`; its `orchestrate` is the Codex-native version led by the active GPT-6 Astra or GPT-5.6 Sol session, with mode-aware routing between them. See [`codex/README.md`](codex/README.md).

Model selection and reusable migration practices are documented in [MODEL-POLICY.md](MODEL-POLICY.md).

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

Then invoke a skill by name, for example `/oss:conjoint-design`. Every skill is on demand, so nothing loads into a session until you ask for it (see *On-demand skills* under [Skills](#skills)).

On Codex there is no plugin. Install the skills library instead (see [Codex](#codex)).

---

## Skills

**On-demand skills.** Every skill in the library is on demand. None loads from context, none is suggested unprompted, and none costs a session anything until you invoke it by name (`/oss:conjoint-design`). That holds a research session's always-on cost near zero instead of the roughly 10k tokens a fully implicit library carries. The tradeoff is deliberate. A skill that fires on its own has to earn its context in every session, and a specialist that fires rarely is cheaper to name than to carry. Claude Code enforces this with `disable-model-invocation: true` in each skill's frontmatter, and the Codex library states the same policy as `allow_implicit_invocation: false` (see [`codex/README.md`](codex/README.md)). `plugin/scripts/check.sh` fails if a skill on either platform is missing its flag.

Skills are grouped by where they fall in a project. Unless the Platform column says otherwise, a skill runs on both Claude Code (`/oss:name`) and Codex (`$name`). Names retired in v2.25.0 (`diverge-codex`, `paper-review-lite-codex`, `survey-flow-audit`, `vlm-ocr-evaluation`, `vlm-ocr-pipeline`, `post-ocr-cleanup`, `fair-check`) still work as aliases that call the merged skill with its mode set.

### Project Setup

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [research-repo](plugin/skills/research-repo/SKILL.md) | Both | `/oss:research-repo` | Scaffold a research project around its source library, or audit an existing one. Builds references, intake tools, analysis and manuscript folders, and a review area. |

### Repo Hygiene

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [sitrep](plugin/skills/sitrep/SKILL.md) | Both | `/oss:sitrep` | Report where a project actually stands. Reads the handoff and log files the repository keeps, checks live git state, and flags where the documents and the repository disagree. |
| [finished](plugin/skills/finished/SKILL.md) | Both | `/oss:finished` | Close a session. Records what changed into the project's own handoff and log, separating verified work from work merely attempted, and reports what was left uncommitted. |

### Workflow & Orchestration

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [orchestrate](plugin/skills/orchestrate/SKILL.md) | Both | `/oss:orchestrate` · `$orchestrate` | Run a multi-model workflow. Claude selects Fable 5.1 or Opus 5. Codex selects GPT-6 Astra or GPT-5.6 Sol. Astra leads hard reasoning, while Sol escalates difficult work to Astra. Both route bounded work to lower GPT-5.6 tiers and can use a Claude peer. |
| [spawn](plugin/skills/spawn/SKILL.md) | Both | `/oss:spawn` | Spawn peer sessions in new terminal panes, each in its own git worktree with a directed task and contract brief. Detects herdr, tmux, or a plain terminal. The lead monitors and merges branches. |
| [advisor](plugin/skills/advisor/SKILL.md) | Both | `/oss:advisor` / `$advisor` | Escalate one decision to an independent second reviewer before committing to an interpretation or completing a task. Your session leads on Opus 5 or Sonnet 5. The Fable 5.1 advisor uses max reasoning. A Fable lead uses `orchestrate`'s Astra peer or the committee. The [Codex counterpart](codex/advisor/SKILL.md) uses Astra/xhigh. |

### Deliverable pipeline

The architecture behind these three skills is written up, with a diagram, in [`docs/deliverable-pipeline.md`](docs/deliverable-pipeline.md). It rests on one wiki per piece of research, one manifest per deliverable, and one profile per kind, with a deterministic gate before any model review, detection in parallel and revision in series, and both vendors working on the same files.

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [deliverable-open](plugin/skills/deliverable-open/SKILL.md) | Claude | `/oss:deliverable-open` | Open a talk, module, paper, chapter, or review as a pipeline unit. A rounds interview creates `deliverable.yml`, `HANDOFF.md`, a `planning/` wiki, and an `inbox/` for dictated notes. Talks use the house deck template. |
| [deliverable-intake](plugin/skills/deliverable-intake/SKILL.md) | Claude | `/oss:deliverable-intake` | Convert dictated or typed notes into a unified diff against the planning wiki. Classify and trace each statement. Keep uncertain names and citations UNRESOLVED. Apply decisions only on assent. |
| [deliverable-lint](plugin/skills/deliverable-lint/SKILL.md) | Claude | `/oss:deliverable-lint` | Run whole-deliverable editorial review in detection mode. Start with build, citations, numbers, facts, and leaks. Add a cheap finder per section and a strong global pass. Produce anchored P0/P1/P2 findings and honest NOT-CHECKED coverage within a dollar budget. The night shift runs headless. |

### Ideation

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [research-grill](plugin/skills/research-grill/SKILL.md) | Both | `/oss:research-grill` | Interview the researcher in rounds until assumptions are explicit. Move from idea to falsifiable question, full design, and reviewer objections. Ask plain-language questions with a recommended answer. Fetch facts and record decisions in a wayfinder ticket or `decisions.md`. Works for a BA thesis or grant. |
| [research-wayfinder](plugin/skills/research-wayfinder/SKILL.md) | Both | `/oss:research-wayfinder` | Plan a study as a decision map that outlives a session. Resolve typed tickets for estimand, identification, power, and measurement until the design is pre-registerable. Adapted from Matt Pocock's wayfinder. |
| [diverge](plugin/skills/diverge/SKILL.md) | Both | `/oss:diverge` · `/oss:diverge-codex` | Before implementing, generate three to five distinct approaches labeled by their differences, then pause for your choice. `--codex` (or the alias) uses Codex (GPT-6 Astra at xhigh) to generate and implement the selected approach. |

### Research Design

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [conjoint-design](plugin/skills/conjoint-design/SKILL.md) | Both | `/oss:conjoint-design` | Design conjoint experiments, including attribute architecture and its implied statistical power. Covers AMCE and AMIE estimation. |
| [conjoint-diagnostics](plugin/skills/conjoint-diagnostics/SKILL.md) | Both | `/oss:conjoint-diagnostics` | Check a conjoint design and analysis for integrity, measurement error, external validity, and interpretation. |
| [conjoint-cleaning](plugin/skills/conjoint-cleaning/SKILL.md) | Both | `/oss:conjoint-cleaning` | Reshape a Qualtrics conjoint export into analysis-ready long format, with choice mapping, translation, pilot detection, and validation. |
| [survey-design](plugin/skills/survey-design/SKILL.md) | Both | `/oss:survey-design` | Write survey instruments. Covers wording, scales, flow, pretesting, respondent burden, and social-desirability mitigation. |
| [qualtrics-ops](plugin/skills/qualtrics-ops/SKILL.md) | Both | `/oss:qualtrics-ops` · `/oss:survey-flow-audit` | Operate a live Qualtrics survey through the v3 APIs without disrupting fielding. Covers publish gates, quotas, flow routing, embedded data, panel-vendor redirects, and read-back verification. `audit` (or the alias) performs a read-only pre-fielding audit of consent, required responses, quotas, redirects, anti-bot measures, language arms, and optional browser checks. |
| [survey-data-audit](plugin/skills/survey-data-audit/SKILL.md) | Both | `/oss:survey-data-audit` | Audit fielded survey data for registered elements, data quality, bot and AI-automation screening, and sample integrity. Produces an appendix-ready quality report. |
| [cross-national-design](plugin/skills/cross-national-design/SKILL.md) | Both | `/oss:cross-national-design` | Design cross-national survey experiments, with per-country power and measurement-equivalence checks. Includes instrument localization. |
| [list-experiment](plugin/skills/list-experiment/SKILL.md) | Both | `/oss:list-experiment` | Design and diagnose list experiments, from sensitivity assessment through estimation and placebo checks. |

### Analysis

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [topic-modeling](plugin/skills/topic-modeling/SKILL.md) | Both | `/oss:topic-modeling` | Fit structural topic models. Choose topic count by coherence and exclusivity. Covers covariates and reporting. |
| [text-classification](plugin/skills/text-classification/SKILL.md) | Both | `/oss:text-classification` | Classify text with LLMs. Covers codebook design, human-in-the-loop workflows, validation, and agreement statistics. |
| [model-council-voting](plugin/skills/model-council-voting/SKILL.md) | Both | `/oss:model-council-voting` | Use a model panel as independent coders under a pre-stated consensus rule. Assess disagreement with chance-corrected kappa and alpha statistics. Checks correlated juror errors. |
| [model-committee](plugin/skills/model-committee/SKILL.md) | Both | `/oss:model-committee`, `/oss:model-committee-astra`, `/oss:model-committee-opus`, `/oss:model-committee-sol` | Have GPT-6 Astra and Claude Opus 5 deliberate toward one decision. They propose independently, critique, revise, and converge under a pre-set rule. Fable 5.1 chairs by default and is not a member. With `-astra`, GPT-6 Astra chairs and Sol replaces it as a member. `-opus` uses the in-session Opus chair. `-sol` uses the legacy GPT-5.6 chair and Terra. |
| [llm-calibration-logprobs](plugin/skills/llm-calibration-logprobs/SKILL.md) | Both | `/oss:llm-calibration-logprobs` | Turn token log-probabilities into per-decision confidence. Measure calibration against human labels with ECE, Brier scores, and reliability diagrams. |

### Corpus Processing

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [vlm-ocr](plugin/skills/vlm-ocr/SKILL.md) | Both | `/oss:vlm-ocr` · `/oss:vlm-ocr-evaluation` · `/oss:vlm-ocr-pipeline` · `/oss:post-ocr-cleanup` | OCR scanned material in three phases. `evaluate` compares systems on stratified ground truth with CER/WER by language and script. `run` builds the vision-language-model pipeline. `clean` corrects output with LLM and rule-based passes, diagnostics, and multilingual handling. The aliases select a phase. |
| [doc-to-markdown](plugin/skills/doc-to-markdown/SKILL.md) | Both | `/oss:doc-to-markdown` | Read or convert any document in a research workflow. Selects direct reading or conversion, the right converter for the document structure, and whether Markdown is tracked or scratch. |

### Writing & Reporting

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [hypothesis-building](plugin/skills/hypothesis-building/SKILL.md) | Both | `/oss:hypothesis-building` | Turn a research question into falsifiable causal hypotheses using DAGs, counterfactuals, equivalence testing, and a stated smallest effect size of interest. |
| [literature-review](plugin/skills/literature-review/SKILL.md) | Both | `/oss:literature-review` | Build or audit a literature review. Produces an evidence map, an assessment of the closest prior work, gap verdicts, and a synthesis plan. |
| [narrative-building](plugin/skills/narrative-building/SKILL.md) | Both | `/oss:narrative-building` | Draft or audit a paper's introduction from the "why" to the "if-then," while keeping multi-experiment papers coherent. |
| [pre-registration-writing](plugin/skills/pre-registration-writing/SKILL.md) | Both | `/oss:pre-registration-writing` | Write a pre-analysis plan. Covers structure, registry choice, analysis strategy, and deviation documentation. |
| [methods-reporting](plugin/skills/methods-reporting/SKILL.md) | Both | `/oss:methods-reporting` | Check a methods section against a 40-item reporting checklist from CONSORT, JARS, and DA-RT transparency standards. |
| [paper-tex](plugin/skills/paper-tex/SKILL.md) | Both | `/oss:paper-tex` | Typeset a draft as house-style LaTeX from Markdown, Word, or other formats. Builds a PDF and prepares it for a specific journal. |

### Figures & Tables

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [figures](plugin/skills/figures/SKILL.md) | Both | `/oss:figures` | Design publication-quality figures. Covers chart choice, scales, color, legend order, self-contained captions, and reproducible code. |
| [tables](plugin/skills/tables/SKILL.md) | Both | `/oss:tables` | Design publication-quality tables. Covers column order, row grouping, precision, uncertainty, self-contained notes, and reproducible code. |

### Manuscript QA

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [citation-check](plugin/skills/citation-check/SKILL.md) | Both | `/oss:citation-check` | Check in-text and reference-list parity, working DOIs, fabrication risk through Crossref and OpenAlex, and citation style. |
| [fact-check](plugin/skills/fact-check/SKILL.md) | Both | `/oss:fact-check` | Verify that each in-text claim is supported by its cited source in the project's Markdown knowledge base. Runs citation-check first. |
| [figure-table-audit](plugin/skills/figure-table-audit/SKILL.md) | Both | `/oss:figure-table-audit` | Audit finished figures and tables for cross-references, text consistency, accessibility, and links to supplementary and replication materials. |
| [replication-package](plugin/skills/replication-package/SKILL.md) | Both | `/oss:replication-package` · `/oss:fair-check` | Scaffold or audit a replication package. Scaffold creates the folder structure, README, master script, figure/table crosswalk, codebook, license, and pre-release checklist. `audit` (or the alias) checks a finished package and manuscript, including FAIR availability, licenses, persistent identifiers, and reuse conditions. |

### Review & Submission

| Skill | Platform | Command | What it does |
|---|---|---|---|
| [paper-review-lite](plugin/skills/paper-review-lite/SKILL.md) | Both | `/oss:paper-review-lite` · `/oss:paper-review-lite-codex` | Run a pre-submission self-audit of your manuscript across argument, numbers, references, writing, figures, and replication. `--codex` (or the alias) runs Claude and Codex (GPT-6 Astra) independently and cross-checks findings with a confidence column. |
| [presubmit](plugin/skills/presubmit/SKILL.md) | Claude Code | `/oss:presubmit` | Set up and run the standalone [presubmit CLI](https://github.com/scdenney/presubmit), a 30-plus-stage adversarial review pipeline driven by the Anthropic API. |
| [referee-response](plugin/skills/referee-response/SKILL.md) | Both | `/oss:referee-response` | Organize and format a response to reviewers. Extract each referee point with severity and type, order revisions by dependency, flag defensible pushbacks as questions, and build the response letter with substantive answers left to you. Never writes the science. |
| [journal-review](plugin/skills/journal-review/SKILL.md) | Both | `/oss:journal-review` | Draft a senior referee report on someone else's manuscript. Uses parallel finder agents and a chief-reviewer synthesis to produce a structured report. |

---

## Recommended companion skills

Third-party skills this library recommends and builds on, credited, not claimed, and not counted in the badges. From [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): **grill-me** (a frontier-rounds design interview, the seed of `research-grill`, and pairs with `diverge`), **wayfinder** (decision-map planning for software work, the source concept for `research-wayfinder`), and **handoff / claude-handoff** (handoff documents for a successor session, the seed of `spawn`). See [RECOMMENDED.md](RECOMMENDED.md) for the full write-up and [`third-party/mattpocock/`](third-party/mattpocock) for pinned, unmodified reference copies.

---

## How skills trigger

No skill loads on its own. Name one, with `/oss:skill-name` in Claude Code or `$skill-name` in Codex, and it reads into context and runs. Nothing is suggested unprompted, so the library costs an idle session nothing.

The orchestration and delegated-review skills (`orchestrate`, `spawn`, `advisor`, `model-committee` and its chair variants, `diverge --codex`, and `paper-review-lite --codex`) start subagents, full peer sessions, or an external model. Every skill is on demand (see *On-demand skills* above), but for these the rule is load-bearing rather than economical.

---

## Installation

### Claude Code

The recommended install is the plugin, shown in [Quick start](#quick-start). It registers the marketplace and installs all 41 skills, their slash commands, and the alias commands for retired names. The command prefix is `oss:`, for open science skills. The marketplace and the repository are both named `open-science-skills`.

To try the plugin for one session without installing:

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills && claude --plugin-dir ./plugin
```

<details>
<summary><b>Selective install</b> – pick specific skills, outside the `/oss:` namespace</summary>

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
<summary><b>Manual copy</b> – a single skill by hand</summary>

Copy the whole skill folder, since many skills ship reference, asset, or script files their `SKILL.md` points at (replace `your-project` with your project's path):

```bash
git clone https://github.com/scdenney/open-science-skills.git

# Project-level (current project only) – copy the whole skill folder:
# many skills ship reference/, assets/, or scripts/ files their SKILL.md points at
mkdir -p your-project/.claude/skills
cp -R open-science-skills/plugin/skills/conjoint-design \
   your-project/.claude/skills/

# User-wide (all projects)
mkdir -p ~/.claude/skills
cp -R open-science-skills/plugin/skills/list-experiment ~/.claude/skills/
```

A copied skill is invoked by its own name. The `/oss:` namespace and the alias commands require the plugin.

</details>

### Codex

Codex discovers skills under `.agents/skills` (repository) and `~/.agents/skills` (user-wide). From this repository's root, preview and install all 40 Codex skills without replacing existing paths:

```bash
python3 plugin/scripts/install-codex.py --all --dry-run
python3 plugin/scripts/install-codex.py --all
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
6. Update the catalogs and badges. Install check dependencies with `python3 -m pip install -r plugin/scripts/requirements-check.txt`, then run `bash plugin/scripts/check.sh` and `python3 plugin/scripts/test-codex-wrappers.py`.

## License

This project is licensed under [Creative Commons Attribution-NonCommercial 4.0 International](LICENSE). The skills are intended for noncommercial scholarly and educational use.

The `citation-check`, `literature-review`, `figures`, `tables`, and `figure-table-audit` skills remix workflow ideas from [Cheng-I Wu's Academic Research Skills for Claude Code](https://github.com/Imbad0202/academic-research-skills), also licensed CC BY-NC 4.0. The instructions here are rewritten for this repository's open-science and experimental-social-science scope.

The `replication-package` skill adapts the structural conventions in [Yusaku Horiuchi's replication-package-guide](https://github.com/yhoriuchi/replication-package-guide) (the source for single-entry-point, compact vs. build/analyze layouts, figure/table crosswalk, paper-consistency check, correction workflow, and pre-release checklist). FAIR-principle integration and Claude Code/Codex skill packaging are added on top. Harvard Dataverse and other platform-specific upload mechanics are not included. Cite Horiuchi's guide if you publish a package built with this skill.

The `spawn` and `research-wayfinder` skills adapt concepts from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): `spawn` generalizes his `claude-handoff` from one background successor to managed multi-session peers, and `research-wayfinder` reworks his `wayfinder` decision map from software specs to experimental design. Unmodified reference copies of the originals are vendored under [`third-party/mattpocock/`](third-party/mattpocock) with his MIT license; see [RECOMMENDED.md](RECOMMENDED.md).
