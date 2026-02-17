# Open Science Skills Library

This repository contains a collection of **Agentic Skills** (formatted as `.md` documents) designed for use with systems like **Claude Code**. These skills "teach" an AI assistant how to adhere to the high standards of experimental social science, from initial hypothesis generation to final methods reporting. This can be used to evaluate and otherwise support the writing and evaluation of pre-registered reports and research writing.

## Development
These skills were developed with some machine assistance from Gemini 3.0, specifically using a personally curated library of foundational methodological texts, and Opus 4.6. This is my first attempt at "skills" development. I will iteratively improve and expand the files here as needed. 

_As of now (Feb. 2026), this is more of a test. I don't consider the skills files fully developed -- yet._

## Usage
To use these skills with **Claude Code**:
1. Clone this repository or copy the `.skills/` folder into your research project.
2. When running Claude Code in that directory, you can activate these skills manually (e.g., `/methods-reporting`) or allow Claude to auto-invoke them based on your prompts.

## Core Idea
Scientific research is a "slow-moving process" that requires carving problems at their "analytical joints." This library prevents "methods-driven" AI assistance by forcing the agent to:
- Identify the **Data Generating Process (DGP)** before suggesting analyses.
- Move from a theoretical **"Why"** to an experimental **"If-Then."**
- Adhere to the **APSA Experimental Section** reporting checklist, **JARS** preregistration standards, and **DA-RT** transparency principles (40-item checklist).

## Repository Structure
The repository is organized into a `.skills` directory containing six skill files.

* **`.skills/narrative-building.md`** – Logic for introductions, literature reviews, the "Why-to-If-Then" funnel, cumulative research framing, and multi-experiment narrative coherence.
* **`.skills/hypothesis-building.md`** – Guidance on falsifiability, counterfactuals, DAGs, the FPCI, three-level hypothesis specification, equivalence testing, SESOI requirements, and multi-experiment hypothesis architecture.
* **`.skills/methods-reporting.md`** – Implementation of a 40-item reporting checklist covering CONSORT standards, JARS preregistration elements, DA-RT transparency, and conjoint-specific reporting.
* **`.skills/conjoint-design.md`** – Specialized logic for multidimensional choice experiments, including closed-form power formulas, empirical AMCE benchmarks, treatment validation, and simulation tools (cjpowR).
* **`.skills/conjoint-diagnostics.md`** – Systematic diagnostic checklist for evaluating conjoint experiments, covering design, estimation, measurement error, external validity, and interpretation.
* **`.skills/cross-national-design.md`** – Guides cross-national survey experiment design with per-country power analysis, sensitivity bias auditing, instrument localization, and cross-national analytical strategies.

---

## Sources & Bibliography
See [SOURCES.md](SOURCES.md) for the full bibliography, organized by topic area.
