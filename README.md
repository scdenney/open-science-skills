# Open Science Skills Library

This repository contains a collection of **Agentic Skills** (formatted as `.md` documents) designed for use with systems like **Claude Code**. These skills "teach" an AI assistant how to adhere to the high standards of experimental social science, from initial hypothesis generation to final methods reporting. This can be used to evaluate and otherwise support the writing and evaluation of pre-registered reports and research writing.

## Development
These skills were developed with some machine assistance from Gemini 3.0, specifically using a personally curated library of foundational methodological texts, and Opus 4.6. This is my first attempt at "skills" development. I will iteratively improve and expand the files here as needed. 

_As of now (Feb. 2026), this is more of a test. I don't consider the skills files fully developed -- yet._

## Usage
To use these skills with **Claude Code**:
1. Clone this repository or copy the `.skills/` folder into your research project.
2. When running Claude Code in that directory, you can activate these skills manually (e.g., `/transparent-methods-reporter`) or allow Claude to auto-invoke them based on your prompts.

## Core Idea
Scientific research is a "slow-moving process" that requires carving problems at their "analytical joints." This library prevents "methods-driven" AI assistance by forcing the agent to:
- Identify the **Data Generating Process (DGP)** before suggesting analyses.
- Move from a theoretical **"Why"** to an experimental **"If-Then."**
- Adhere to the **APSA Experimental Section** 19-item reporting checklist.

## Repository Structure
The repository is organized into a `.skills` directory. Each sub-folder represents a specific domain of expertise containing a `SKILL.md` file.

* **`.skills/scientific-narrative-builder/`** – Logic for introductions, literature reviews, and uncovering "invisible" factors.
* **`.skills/causal-hypothesis-architect/`** – Guidance on falsifiability, counterfactuals, and Directed Acyclic Graphs (DAGs).
* **`.skills/transparent-methods-reporter/`** – Implementation of the 19-item checklist and CONSORT standards.
* **`.skills/design-conjoint-expert/`** – Specialized logic for multidimensional choice experiments and AMCE estimation.

---

## Sources & Bibliography
The instructions within these skills are drawn from the following sources:

* **Berinsky, A. J.** (2017). Measuring Public Opinion with Surveys. *Annual Review of Political Science*.
* **Blair, G., Coppock, A., & Moor, M.** (2020). When to Worry about Sensitivity Bias: A Social Reference Theory and Evidence from 30 Years of List Experiments. *APSR*.
* **Christensen, G., Freese, J., & Miguel, E.** (2019). *Transparent and Reproducible Social Science Research: How to Do Open Science*. University of California Press.
* **Druckman, J. N.** (2022). *Experimental Thinking: A Primer on Social Science Experiments*. Cambridge University Press.
* **Druckman, J. N., & Green, D. P.** (Eds.). (2021). *Advances in Experimental Political Science*. Cambridge University Press.
* **Freitag, M.** (2021). *cjpowR: A package for power analysis for conjoint experiments*.
* **Gerber, A. S., et al.** (2014). "Reporting Guidelines for Experimental Research." *Journal of Experimental Political Science*.
* **Huntington-Klein, N.** (2025). *The Effect: An Introduction to Research Design and Causality*. CRC Press.
* **Lakens, D.** (2025). *Improving Your Statistical Inferences*.
* **Mutz, D. C.** (2011). *Population-Based Survey Experiments*. Princeton University Press.
* **Sniderman, P. M.** (2018). "Some Advances in the Design of Survey Experiments." *Annual Review of Political Science*.
* **Stantcheva, S.** (2023). "How to Run Surveys: A Guide to Creating Your Own Identifying Variation." *Annual Review of Economics*.
* **Stefanelli, A., & Lukac, M.** (2020). "Subjects, Trials, and Levels: Statistical Power in Conjoint Experiments."
