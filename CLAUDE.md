# CLAUDE.md - Project Guide

## Project Overview

This is the **Open Science Skills Library** - a collection of agentic skills (`.md` documents) designed for Claude Code. These skills teach Claude how to adhere to high standards of experimental social science research methodology.

## Purpose

The skills support:
- Evaluating and writing pre-registered reports
- Research methodology guidance
- Methods reporting standards compliance

## Core Principles

1. **Identify the Data Generating Process (DGP)** before suggesting analyses
2. **Move from theoretical "Why" to experimental "If-Then"**
3. **Adhere to APSA Experimental Section 19-item reporting checklist**

The goal is to prevent "methods-driven" AI assistance by forcing proper methodological reasoning.

## Repository Structure

```
.skills/
├── scientific-narrative-builder/   # Introductions, literature reviews, uncovering "invisible" factors
├── causal-hypothesis-architect/    # Falsifiability, counterfactuals, DAGs
├── transparent-methods-reporter/   # 19-item checklist, CONSORT standards
└── design-conjoint-expert/         # Conjoint experiments, AMCE estimation
```

Each skill folder contains a `SKILL.md` file with the skill definition.

## Usage

Skills can be invoked manually (e.g., `/transparent-methods-reporter`) or auto-invoked based on prompts.

## Key Terminology

- **DGP**: Data Generating Process
- **DAG**: Directed Acyclic Graph
- **AMCE**: Average Marginal Component Effect (conjoint analysis)
- **CONSORT**: Consolidated Standards of Reporting Trials
- **APSA**: American Political Science Association

## Working with This Repository

When editing or creating skills:
- Each skill lives in `.skills/<skill-name>/SKILL.md`
- Skills should enforce methodological rigor, not just provide shortcuts
- Reference the bibliography sources in README.md for authoritative guidance
