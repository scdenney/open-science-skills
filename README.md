# Open Science Skills

![skills](https://img.shields.io/badge/skills-11-blue)
![plugin](https://img.shields.io/badge/Claude%20Code-plugin-orange)
![updated](https://img.shields.io/badge/updated-Mar%202026-green)
![sources](https://img.shields.io/badge/sources-65%2B-purple)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

A library of [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) for experimental social science. Install as a plugin to get methodologically rigorous AI assistance — from hypothesis generation through final reporting — available both as auto-triggered context and as explicit `/skill-name` slash commands.

Skills were developed using a curated library of methodology texts, with machine assistance from Gemini 3.0 and Opus 4.6. They are iteratively expanded as new sources are incorporated. This is a living and breathing kind of repo.

Design follows the [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): concise procedural guidance (no textbook definitions), trigger-rich YAML descriptions for auto-invocation, and progressive disclosure (instructions in skills, bibliography in SOURCES.md).

> These skills support, not supplant, the research and writing process. They adhere to APSA, JARS, and DA-RT reporting standards. All guidance is grounded in 65+ published sources — see [**SOURCES.md**](SOURCES.md) for the full bibliography.

---

## How Skills Work

Each skill is available in two ways:

| Mode | How | When to use |
|------|-----|-------------|
| **Auto-trigger** | Claude reads your prompt and loads the relevant skill silently | Working naturally — Claude detects context |
| **Slash command** | Type `/skill-name` (optionally with a task description) | When you want to invoke a skill explicitly |

Both modes are available when installed as a plugin. Individual skills can also be installed manually (auto-trigger only).

---

## Installation

### Option 1 — Plugin (recommended, installs all skills + slash commands)

**Permanent install** (user-wide, persists across all projects):

```bash
# Step 1: Register the marketplace (one-time)
claude plugin marketplace add scdenney/open-science-skills

# Step 2: Install the plugin
claude plugin install open-science-skills

# Project-only install
claude plugin install open-science-skills --scope project
```

**Session-only** (no install required, active for the current session):

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills && claude --plugin-dir .
```

All 11 skills auto-trigger based on your prompts. All 11 slash commands (`/conjoint-design`, `/list-experiment`, etc.) are immediately available.

### Option 2 — Selective install (choose specific skills, auto-trigger only)

Use the interactive install script to pick only the skills you want:

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills
bash scripts/install.sh
```

The script lists available skills and lets you choose interactively. Skills are installed to `./.claude/skills/` by default (current project only). Options:

```bash
# Install to user-wide skills directory (all projects)
bash scripts/install.sh --target ~/.claude/skills

# Install specific skills non-interactively
bash scripts/install.sh --skill conjoint-design survey-design list-experiment

# Install all skills
bash scripts/install.sh --all --target ~/.claude/skills
```

Restart Claude Code after installing to load the new skills.

### Option 3 — Manual copy (single skill, auto-trigger only)

```bash
git clone https://github.com/scdenney/open-science-skills.git

# Project-level (current project only)
mkdir -p your-project/.claude/skills/conjoint-design
cp open-science-skills/skills/conjoint-design/SKILL.md \
   your-project/.claude/skills/conjoint-design/SKILL.md

# User-wide (all projects)
mkdir -p ~/.claude/skills/list-experiment
cp open-science-skills/skills/list-experiment/SKILL.md \
   ~/.claude/skills/list-experiment/SKILL.md
```

> **Note:** Manual install gives you auto-trigger only. Slash commands (`/skill-name`) require the plugin.

---

## Skills

### Research Design

| Skill | Slash command | What it does |
|-------|--------------|-------------|
| [**conjoint-design**](skills/conjoint-design/SKILL.md) | `/conjoint-design` | Attribute architecture, AMCE/AMIE estimation, power analysis (`cjpowR`), BART heterogeneity detection, design variants |
| [**conjoint-diagnostics**](skills/conjoint-diagnostics/SKILL.md) | `/conjoint-diagnostics` | Diagnostic checklist: design, estimation, measurement error (IRR), external validity, interpretation |
| [**survey-design**](skills/survey-design/SKILL.md) | `/survey-design` | Question construction, scale design, survey flow, pretesting, respondent burden, social desirability mitigation |
| [**cross-national-design**](skills/cross-national-design/SKILL.md) | `/cross-national-design` | Cross-national survey experiments: per-country power, sensitivity bias auditing, instrument localization |
| [**list-experiment**](skills/list-experiment/SKILL.md) | `/list-experiment` | Item count technique: pre-design sensitivity assessment, control list design, NLSreg/MLreg estimation, assumption testing, placebo diagnostics |

### Analysis

| Skill | Slash command | What it does |
|-------|--------------|-------------|
| [**topic-modeling**](skills/topic-modeling/SKILL.md) | `/topic-modeling` | STM with metadata covariates, topic count selection via coherence-exclusivity diagnostics, reporting |
| [**text-classification**](skills/text-classification/SKILL.md) | `/text-classification` | LLM-based classification: codebook design, learning regime selection, human-LLM hybrid workflows, validation |

### Writing & Reporting

| Skill | Slash command | What it does |
|-------|--------------|-------------|
| [**hypothesis-building**](skills/hypothesis-building/SKILL.md) | `/hypothesis-building` | Falsifiability, counterfactuals, DAGs, FPCI, three-level hypothesis specification, equivalence testing, SESOI |
| [**narrative-building**](skills/narrative-building/SKILL.md) | `/narrative-building` | Introduction logic, literature reviews, the "Why-to-If-Then" funnel, cumulative framing, multi-experiment coherence |
| [**pre-registration-writing**](skills/pre-registration-writing/SKILL.md) | `/pre-registration-writing` | PAP structure, registry selection, analytical strategy specification, code pre-registration, deviation documentation |
| [**methods-reporting**](skills/methods-reporting/SKILL.md) | `/methods-reporting` | 40-item reporting checklist: CONSORT standards, JARS preregistration elements, DA-RT transparency |

---

## Slash Command Examples

```
/conjoint-design I'm deciding between 4 and 6 attributes — what are the trade-offs?

/list-experiment is a list experiment appropriate for measuring social desirability bias on this topic?

/survey-design review this draft question for leading language and double-barreling

/text-classification I have 5,000 open-text responses — should I use zero-shot or few-shot classification?

/hypothesis-building help me sharpen this hypothesis and identify testable observable implications

/pre-registration-writing draft the analytical strategy section for my PAP

/methods-reporting run a reporting checklist on my methods section [paste text]
```

---

## Contributing

PRs welcome. To add a new skill:

1. Create `skills/<name>/SKILL.md` following the [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
2. Copy to `.skills/<name>.md` (flat format for direct project use)
3. Add `commands/<name>.md` (see existing examples — one paragraph activation prompt + `$ARGUMENTS`)
4. Add sources to `SOURCES.md` under a new or existing section
5. Update badges and table in this README
