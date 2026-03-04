# Open Science Skills

![skills](https://img.shields.io/badge/skills-10-blue)
![plugin](https://img.shields.io/badge/Claude%20Code-plugin-orange)
![updated](https://img.shields.io/badge/updated-Mar%202026-green)
![sources](https://img.shields.io/badge/sources-45%2B-purple)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

A library of [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) for experimental social science. Install as a plugin or copy manually into any research project to get methodologically rigorous AI assistance — from hypothesis generation through final reporting.

Skills were developed using a curated library of methodology texts, with machine assistance from Gemini 3.0 and Opus 4.6. They are iteratively expanded as new sources are incorporated. This is a living and breathing kind of repo.

Design follows the [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): concise context (no textbook definitions), trigger-rich YAML descriptions for auto-invocation, and progressive disclosure (instructions in skills, bibliography in SOURCES.md).

> These skills are meant to support, not supplant, the writing process and ahere to standards for good social science standards as per APSA, JARS, and DA-RT reporting standards. Skills writing is based on 45+ published sources. See [**SOURCES.md**](SOURCES.md) for the full bibliography.

## Installation

### Plugin (recommended)

```bash
claude plugin install open-science-skills --plugin-dir /path/to/open-science-skills
```

Skills are namespaced: invoke as `/open-science-skills:conjoint-design`, or let Claude auto-invoke based on your prompts.

### Manual

```bash
git clone https://github.com/scdenney/open-science-skills.git

# Copy into your project's Claude skills directory
for dir in open-science-skills/skills/*/; do
  skill=$(basename "$dir")
  mkdir -p your-project/.claude/skills/$skill
  cp "$dir/SKILL.md" your-project/.claude/skills/$skill/SKILL.md
done
```

Skills invoke as `/conjoint-design`, `/survey-design`, etc.

### Work directly in this repo

```bash
git clone https://github.com/scdenney/open-science-skills.git
cd open-science-skills && claude --plugin-dir .
```

---

## Skills

### Research Design

| Skill | What it does |
|-------|-------------|
| [**conjoint-design**](skills/conjoint-design/SKILL.md) | Attribute architecture, AMCE/AMIE estimation, power analysis (`cjpowR`), BART heterogeneity detection, design variants |
| [**conjoint-diagnostics**](skills/conjoint-diagnostics/SKILL.md) | Diagnostic checklist for reviewing conjoint studies: design, estimation, measurement error (IRR), external validity, interpretation |
| [**survey-design**](skills/survey-design/SKILL.md) | Question construction, scale design, survey flow, pretesting, respondent burden, social desirability mitigation |
| [**cross-national-design**](skills/cross-national-design/SKILL.md) | Cross-national survey experiments: per-country power, sensitivity bias auditing, instrument localization |

### Analysis

| Skill | What it does |
|-------|-------------|
| [**topic-modeling**](skills/topic-modeling/SKILL.md) | STM specification with metadata covariates, topic count selection via coherence-exclusivity diagnostics, reporting |
| [**text-classification**](skills/text-classification/SKILL.md) | LLM-based classification: codebook design, learning regime selection, human-LLM hybrid workflows, validation |

### Writing & Reporting

| Skill | What it does |
|-------|-------------|
| [**hypothesis-building**](skills/hypothesis-building/SKILL.md) | Falsifiability, counterfactuals, DAGs, FPCI, three-level hypothesis specification, equivalence testing, SESOI |
| [**narrative-building**](skills/narrative-building/SKILL.md) | Introduction logic, literature reviews, the "Why-to-If-Then" funnel, cumulative framing, multi-experiment coherence |
| [**pre-registration-writing**](skills/pre-registration-writing/SKILL.md) | PAP structure, registry selection, analytical strategy specification, code pre-registration, deviation documentation |
| [**methods-reporting**](skills/methods-reporting/SKILL.md) | 40-item reporting checklist: CONSORT standards, JARS preregistration elements, DA-RT transparency |
