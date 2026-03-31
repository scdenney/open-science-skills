---
name: paper-review
description: Runs a comprehensive pre-submission audit using parallel review agents. Covers content/argument, numerical consistency, references/DOIs, writing quality, figures/formatting, and replication archive. Use when (1) preparing a manuscript for journal submission, (2) checking internal consistency of numbers across abstract, body, tables, and SI, (3) auditing a bibliography for missing DOIs or formatting issues, (4) reviewing a replication archive for completeness, (5) verifying data availability, ethics/IRB, and funding statements, (6) running a cross-check on figures, tables, and formatting, or (7) assessing writing quality and terminology consistency.
argument-hint: "[path to paper or describe manuscript to review]"
context: fork
---

# Paper Pre-Submission Review

## Instructions

Run a comprehensive pre-submission review of the academic paper using parallel review agents. Each agent examines a different dimension; cross-check agents audit Phase 1 findings for false positives and missed issues. The final output is a structured pre-submit report with severity-ranked findings and a journal-readiness checklist.

This review can be re-run after fixes to verify issues are resolved.

### 1. Orientation (do this yourself before launching agents)

Read the paper yourself to understand its structure before writing agent prompts. Determine:

- Where the paper source lives (LaTeX `.tex` vs Pandoc `.md` vs Word) and what the build command is
- Whether a Supplementary Information file exists and where it lives
- Where figures are stored and how they are referenced (relative paths, figure directories)
- Whether a replication archive exists (look for `replication/`, `archive/`, `data/`, README files)
- The paper's rough structure: section names, approximate page count, key claims in the abstract
- The bibliography format and location (`.bib`, inline, etc.)

Use this knowledge to write **specific** agent prompts that reference actual file paths, section names, and relevant files. Generic prompts produce shallow results.

### 2. Parallel Deep Review (launch all 7 agents simultaneously)

**Agent 1 — Content & Argument**: Read the full paper. Check logical flow from introduction through conclusion. Identify unsupported claims, logical gaps, missing caveats, and places where the argument is unclear or circular. Flag any claims in the abstract not backed up in the body. Note missing discussion of limitations. Check whether the framing accurately positions the contribution relative to cited prior work.

**Agent 2 — Numbers & Internal Consistency**: Check every quantitative claim. Do numbers in the abstract match the body? Do table values match in-text references? Do SI cross-references point to the right appendices/tables? Are confidence intervals, p-values, N counts, and effect sizes reported consistently throughout? Flag multiple-comparisons issues (many tests without correction or discussion). Verify that significance thresholds are defined and used consistently.

**Agent 3 — References & Citations**: Audit the bibliography file. Are all cited works present? Are there uncited entries? Check for stale working papers (2025+) that may now be published — flag entries that need author verification. Check formatting consistency (journal names, author encoding, entry types). Do NOT check DOIs — that is Agent 4's job.

**Agent 4 — DOI Audit**: Check every bibliography entry for a DOI. For entries missing a DOI, attempt to locate one via web search (title + author + "doi"). Report which entries are missing DOIs and, where found, provide the correct DOI. Verify that existing DOIs resolve to the correct paper — wrong-paper DOIs are a common copy-paste error. This agent runs separately because DOI lookup is slow.

**Agent 5 — Writing Quality & Completeness**: Check for redundancy, passive voice overuse, unclear antecedents, jargon without definition on first use, overly long sentences (60+ words), and inconsistent terminology for the same concept. Also explicitly check for these pre-submission completeness items:
- Anonymization / double-blind compliance: no self-identifying information, self-citations in third person, no "unpublished manuscript by [author]" references, no author names in file metadata or acknowledgments
- Data availability statement (present and accurate?)
- Ethics/IRB statement (present and sufficient for human subjects research?)
- Preregistration disclosure (if experimental: is a PAP referenced or its absence justified?)
- AI use disclosure (required by some journals — flag if absent and suggest adding)
- Conflict of interest declaration
- Funding/acknowledgment statement
- Author ORCID (if journal requires)
- Abstract word count (most journals cap at 150 words)
- Keywords (some journals require 4-5 keywords)
- Word/page count against journal limits (if known)

Flag each completeness item as present, missing, or insufficient.

**Agent 6 — Figures, Tables & Formatting**: Verify all figures referenced in text exist on disk. Check captions for self-containedness (a reader should understand the figure from the caption alone). Verify figure and table numbering for gaps or duplicates. Check for LaTeX/build warnings (undefined references, overfull/underfull boxes). Verify SI is internally consistent and all SI cross-references in the main text point to the correct appendix/table/figure numbers. Check for formatting inconsistencies (e.g., mixed `\hline` and booktabs, inconsistent float placement).

**Agent 7 — Replication Archive**: Review the replication archive independently. Does the README document the full pipeline? Are all data files present (or documented as embargoed/restricted)? Do script paths in the README match what actually exists? Are software dependencies and versions documented? Is there a codebook for each dataset (variable definitions, coding)? Does a table/figure-to-script mapping exist (which script produces which output)? Are PRNG seeds documented for any simulation or bootstrap procedures? Is data provenance documented (source, license, redistribution rights)? Could a competent researcher reproduce the main results from the archive alone? Flag missing files, undocumented steps, or broken path references.

**Output format for each agent**: Use structured lists, not prose. For each issue:
- Severity: `[CRITICAL]`, `[RECOMMENDED]`, or `[MINOR]`
- Location: file path and line number or section name
- Issue: one sentence describing the problem
- Fix: one sentence describing what to do

### 3. Cross-Check (launch after Phase 2 completes)

Both cross-check agents receive the structured findings from Phase 2.

**Agent 8 — Content & Numbers Cross-Checker**: Review findings from Agents 1 and 2. For each `[CRITICAL]` or `[RECOMMENDED]` item, verify it against the actual paper text. Flag false positives (issue doesn't exist or is already addressed). Add any issues missed — pay particular attention to: abstract vs. conclusion claims that drift from body evidence, significance thresholds, multiple comparisons, and denominator consistency (e.g., percentages computed with vs. without a residual category).

**Agent 9 — Technical Cross-Checker**: Review findings from Agents 3, 4, 6, and 7. Verify each flagged item against the actual files — check the bibliography, figure files, and archive directory. Confirm or refute each finding. Add any issues missed.

### 4. Synthesis

Compile all validated findings (false positives removed) into a single **Pre-Submit Report**:

```
## Pre-Submit Report: [Paper Title]
Date: [today]
Issues: [N critical, N recommended, N minor]

### Critical Issues (must fix before submission)
### Recommended Changes (should fix, not blocking)
### Minor Issues (nice to have)
### Strengths (what is working well)
### Journal-Readiness Checklist

| Dimension                        | Status            | Notes |
|----------------------------------|-------------------|-------|
| Compiles cleanly                 | PASS/FAIL         |       |
| Anonymized for double-blind      | PASS/FAIL         |       |
| Argument & logic                 | PASS/FAIL/PARTIAL |       |
| Internal numerical consistency   | PASS/FAIL/PARTIAL |       |
| References complete              | PASS/FAIL/PARTIAL |       |
| DOIs present                     | PASS/FAIL/PARTIAL |       |
| Writing quality                  | PASS/FAIL/PARTIAL |       |
| Figures/tables correct           | PASS/FAIL/PARTIAL |       |
| Formatting consistent            | PASS/FAIL/PARTIAL |       |
| Abstract & keywords              | PASS/FAIL/PARTIAL |       |
| Word/page count compliant        | PASS/FAIL/NA      |       |
| Replication archive ready        | PASS/FAIL/PARTIAL |       |
| Data availability statement      | PASS/MISSING      |       |
| Ethics/IRB statement             | PASS/MISSING      |       |
| Preregistration disclosure       | PASS/MISSING/NA   |       |
| AI use disclosure                | PASS/MISSING      |       |
| COI declaration                  | PASS/MISSING      |       |
| Funding/acknowledgments          | PASS/MISSING      |       |

### What Still Needs Your Input
```

The "What Still Needs Your Input" section lists items the review cannot resolve because they require author knowledge: ethics approval numbers, funding grant details, journal-specific formatting requirements, embargo status of data, or factual claims only the author can verify.

Cite file paths and line numbers for every issue. Distinguish between objective errors (wrong numbers, broken references) and subjective suggestions (writing style, framing).

## Quality Checks

- [ ] Orientation phase completed: paper structure, build system, SI location, archive location all identified before agent prompts were written
- [ ] All 7 Phase 2 agents launched in parallel to maximize efficiency
- [ ] Agent prompts reference specific file paths, not generic placeholders
- [ ] Cross-check agents verified every CRITICAL and RECOMMENDED finding against actual files
- [ ] False positives identified and removed from the final report
- [ ] Every issue in the report includes a file path and line number (or section name)
- [ ] The journal-readiness checklist covers all 18 dimensions
- [ ] The "What Still Needs Your Input" section is populated with items requiring author knowledge
- [ ] Report distinguishes objective errors from subjective suggestions
- [ ] Report includes a Strengths section (not just problems)
