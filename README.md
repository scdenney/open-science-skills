# Open Science Skills

![skills](https://img.shields.io/badge/skills-10-blue)
![updated](https://img.shields.io/badge/updated-Mar%202026-green)
![sources](https://img.shields.io/badge/sources-45%2B-purple)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

A library of [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) for experimental social science. Drop the `.skills/` folder into any research project to get methodologically rigorous AI assistance — from hypothesis generation through final reporting.

Skills were developed using a curated library of methodology texts, with machine assistance from Gemini 3.0 and Opus 4.6. They are iteratively expanded as new sources are incorporated. This is a living and breathing kind of repo.

Design follows the [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): concise context (no textbook definitions), trigger-rich YAML descriptions for auto-invocation, and progressive disclosure (instructions in skills, bibliography in SOURCES.md).

> These skills are meant to support, not supplant, the writing process and ahere to standards for good social science standards as per APSA, JARS, and DA-RT reporting standards. Skills writing is based on 45+ published sources. See [**SOURCES.md**](SOURCES.md) for the full bibliography.

## Quick Start

```bash
# Clone into your project
git clone https://github.com/scdenney/open-science-skills.git
cp -r open-science-skills/.skills/ your-project/.skills/

# Or clone and work directly
cd open-science-skills
claude
```

Skills activate automatically based on your prompts, or invoke manually (e.g., `/conjoint-design`).

---

## Skills

### Research Design

| Skill | What it does |
|-------|-------------|
| [**conjoint-design**](.skills/conjoint-design.md) | Attribute architecture, AMCE/AMIE estimation, power analysis (`cjpowR`), BART heterogeneity detection, design variants |
| [**conjoint-diagnostics**](.skills/conjoint-diagnostics.md) | Diagnostic checklist for reviewing conjoint studies: design, estimation, measurement error (IRR), external validity, interpretation |
| [**survey-design**](.skills/survey-design.md) | Question construction, scale design, survey flow, pretesting, respondent burden, social desirability mitigation |
| [**cross-national-design**](.skills/cross-national-design.md) | Cross-national survey experiments: per-country power, sensitivity bias auditing, instrument localization |

### Analysis

| Skill | What it does |
|-------|-------------|
| [**topic-modeling**](.skills/topic-modeling.md) | STM specification with metadata covariates, topic count selection via coherence-exclusivity diagnostics, reporting |
| [**text-classification**](.skills/text-classification.md) | LLM-based classification: codebook design, learning regime selection, human-LLM hybrid workflows, validation |

### Writing & Reporting

| Skill | What it does |
|-------|-------------|
| [**hypothesis-building**](.skills/hypothesis-building.md) | Falsifiability, counterfactuals, DAGs, FPCI, three-level hypothesis specification, equivalence testing, SESOI |
| [**narrative-building**](.skills/narrative-building.md) | Introduction logic, literature reviews, the "Why-to-If-Then" funnel, cumulative framing, multi-experiment coherence |
| [**pre-registration-writing**](.skills/pre-registration-writing.md) | PAP structure, registry selection, analytical strategy specification, code pre-registration, deviation documentation |
| [**methods-reporting**](.skills/methods-reporting.md) | 40-item reporting checklist: CONSORT standards, JARS preregistration elements, DA-RT transparency |
