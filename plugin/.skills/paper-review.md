---
name: paper-review
description: Runs a comprehensive pre-submission audit using parallel review agents. Covers content/argument, numerical consistency, references/DOIs, writing quality, figures/formatting, and replication archive. Use when (1) preparing a manuscript for journal submission, (2) checking internal consistency of numbers across abstract, body, tables, and SI, (3) auditing a bibliography for missing DOIs or formatting issues, (4) reviewing a replication archive for completeness, (5) verifying data availability, ethics/IRB, and funding statements, (6) running a cross-check on figures, tables, and formatting, or (7) assessing writing quality and terminology consistency.
argument-hint: "[path to paper or describe manuscript to review]"
context: fork  # Claude Code: run skill in a forked subagent context (isolated from conversation history). See https://code.claude.com/docs/en/skills#frontmatter-reference
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
- **Design family.** Is this a conjoint/factorial-vignette paper, a list experiment, a topic-modeling or LLM-classification study, or a VLM-OCR corpus paper? If so, also invoke the relevant sibling skill (`conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr-pipeline`) and fold its domain-specific checklist into Agent 9's deliverable. For any experimental manuscript, also run `methods-reporting` in audit mode so its 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8.

Use this knowledge to write **specific** agent prompts that reference actual file paths, section names, and relevant files. Generic prompts produce shallow results.

**Orchestration contract.** Before Phase 2, create a scratch directory `.review-tmp/` in the paper's working directory. Each Phase 2 agent writes its structured findings to a dedicated file (`agent-1-content.md`, `agent-2-numbers.md`, ..., `agent-9-archive.md`) using the output format specified below. Phase 3 cross-checkers read these files directly; you do not need to paste findings back into their prompts. Launch all Phase 2 agents in a single message with parallel sub-agent tool calls (one call per agent) so they run concurrently; launch Phase 3 after all nine output files exist. For experimental manuscripts, Agents 6 (CONSORT/randomization-and-flow) and 7 (pre-registration verification) are mandatory; for non-experimental manuscripts they can be skipped and their checklist rows marked `NA`.

### 2. Parallel Deep Review (launch all 9 agents simultaneously)

**Agent 1 — Content & Argument**: Read the full paper. Check logical flow from introduction through conclusion. Identify unsupported claims, logical gaps, missing caveats, and places where the argument is unclear or circular. Flag any claims in the abstract not backed up in the body. Note missing discussion of limitations. Check whether the framing accurately positions the contribution relative to cited prior work.

**Agent 2 — Numbers & Internal Consistency**: Check every quantitative claim against JARS-Quant reporting expectations (Appelbaum et al. 2018). Do numbers in the abstract match the body? Do table values match in-text references? Do SI cross-references point to the right appendices/tables? Are confidence intervals, p-values, N counts, and effect sizes reported consistently throughout? Flag multiple-comparisons issues (many tests without correction or discussion). Verify that significance thresholds are defined and used consistently. For experimental papers, verify denominator consistency across ITT and any complier/compliance-adjusted analyses and flag any manipulation-check that is present in the design but missing from the results. Flag forking-paths risks explicitly: DV switching between primary and secondary outcomes, covariate-set changes across models, transformation or subsetting decisions not traceable to a pre-registration, and any analysis whose choice was visibly made after seeing outcome data (Wicherts et al. 2016; Gelman & Loken 2014; Simmons et al. 2011). Do NOT audit the CONSORT flow, baseline balance, attrition-by-arm, or PAP-to-paper mapping — those are Agents 6 and 7.

**Agent 3 — References & Citations**: Audit the bibliography file. Are all cited works present? Are there uncited entries? Check for stale working papers (2025+) that may now be published — flag entries that need author verification. Check formatting consistency (journal names, author encoding, entry types). Do NOT check DOIs — that is Agent 4's job.

**Agent 4 — DOI Audit**: Check every bibliography entry for a DOI. For entries missing a DOI, attempt to locate one via web search (title + author + "doi"). Report which entries are missing DOIs and, where found, provide the correct DOI. Verify that existing DOIs resolve to the correct paper — wrong-paper DOIs are a common copy-paste error. This agent runs separately because DOI lookup is slow.

**Agent 5 — Writing Quality & Journal Compliance**: Check for redundancy, passive voice overuse, unclear antecedents, jargon without definition on first use, overly long sentences (60+ words), and inconsistent terminology for the same concept. Audit journal-level transparency compliance against the TOP Guidelines (Nosek et al. 2015): data citation, data/code/materials transparency, design and analysis transparency, preregistration of studies and analysis plans, replication standards. Check reporting conformance against JARS-Quant (Appelbaum et al. 2018) and the reproducibility manifesto (Munafò et al. 2017). Explicitly check these pre-submission completeness items:
- Anonymization / double-blind compliance: no self-identifying information, self-citations in third person, no "unpublished manuscript by [author]" references, no author names in file metadata or acknowledgments
- Data availability statement (present and accurate per TOP Level 2+ and DA-RT; Lupia & Elman 2014)
- Ethics/IRB statement (present and sufficient for human subjects research; judge against APSA 2020 *Principles and Guidance for Human Subjects Research* — protocol number, exempt vs. expedited vs. full review, consent language, and any minor/vulnerable-population flags)
- AI use disclosure (required by some journals — flag if absent and suggest adding)
- Conflict of interest declaration
- Funding/acknowledgment statement
- Author ORCID (if journal requires)
- Abstract word count (most journals cap at 150 words)
- Keywords (some journals require 4-5 keywords)
- Word/page count against journal limits (if known)

Flag each completeness item as present, missing, or insufficient. Do NOT audit the preregistration itself — that is Agent 7.

**Agent 6 — CONSORT / Randomization & Flow** (experimental papers only): Audit randomization and participant flow against the CONSORT 2010 Statement (Schulz, Altman & Moher 2010) and Gerber et al. (2014) Appendix 1. Verify a participant-flow diagram is present and documents, at every stage: number assessed for eligibility; number excluded pre-randomization and reasons; number randomized per arm; number receiving the intended condition per arm; number lost to follow-up or excluded post-randomization (by arm, with reasons); number analyzed per arm for the primary outcome. Verify that: (a) a baseline-balance table across treatment arms is reported with standardized mean differences or equivalent, and imbalances are discussed; (b) **intention-to-treat (ITT)** is the primary analysis — per-protocol or complier-average analyses, if reported, are clearly labeled as secondary; (c) attrition rates are reported by arm and differential attrition (magnitude and composition) is explicitly addressed, including any sensitivity analysis (e.g., Lee bounds, Manski bounds); (d) the randomization procedure (unit, block structure, stratification, allocation concealment, mechanism) is described; (e) blinding / masking status is stated for participants, experimenters, and analysts, or its absence is justified. Flag any discrepancy between the CONSORT diagram numbers and the N's reported in the main tables. For non-experimental manuscripts, write `NA — non-experimental` to the output file and exit.

**Agent 7 — Pre-Registration Verification** (experimental / pre-registered papers only): Audit the manuscript against its pre-analysis plan (PAP) end-to-end. Steps: (1) **Registry verification** — locate the registration on OSF, AsPredicted, EGAP, or the journal registry; record the registry ID, registration timestamp, and whether the PAP is embargoed or public; flag any registration that post-dates data collection or data access. (2) **PAP-to-paper hypothesis mapping** — produce a table with columns `PAP ID | Registered hypothesis | Registered estimator | Registered outcome | Reported in paper? | Location | Deviation?`. Every registered hypothesis must appear; every reported confirmatory analysis must trace back to a registered hypothesis. (3) **Confirmatory vs. exploratory classification** — every reported analysis must be explicitly labeled confirmatory (registered) or exploratory (not registered); flag analyses presented as confirmatory that are not in the PAP. (4) **Silent-deviation audit** — flag registered analyses not reported; reported analyses not registered; changes in DV, covariate set, subgroup, estimator, sample filter, or pre-processing step that are not disclosed in a deviations section. Judge the PAP against Waldron & Allen (2022): is it specific, precise, and exhaustive? (5) **Forking-paths check** — Gelman & Loken (2014) and Simmons et al. (2011): list every branch point (DV choice, covariate set, exclusion rule, transformation, subgroup definition) and confirm each is resolved by the PAP or acknowledged as exploratory. Nosek et al. (2018) "Preregistration Revolution" is the benchmark for what counts as a credible pre-registration. For non-preregistered manuscripts, write `NA — no preregistration` to the output file, note whether the manuscript justifies the absence, and exit.

**Agent 8 — Figures, Tables & Formatting**: Verify all figures referenced in text exist on disk. Check captions for self-containedness (a reader should understand the figure from the caption alone). Verify figure and table numbering for gaps or duplicates. Check for LaTeX/build warnings (undefined references, overfull/underfull boxes). Verify SI is internally consistent and all SI cross-references in the main text point to the correct appendix/table/figure numbers. Check for formatting inconsistencies (e.g., mixed `\hline` and booktabs, inconsistent float placement). Flag accessibility issues in figures (alt text, color-blind-safe palettes, contrast). Do NOT audit the CONSORT participant-flow diagram itself — that is Agent 6; but if Agent 6 reports a CONSORT diagram is missing, still verify that a placeholder or substitute figure is not mis-numbered.

**Agent 9 — Replication Archive**: Review the replication archive independently against TOP Level 2+ (Nosek et al. 2015) and DA-RT (Lupia & Elman 2014). Does the README document the full pipeline? Are all data files present (or documented as embargoed/restricted)? Do script paths in the README match what actually exists? Are software dependencies and versions documented? Is there a codebook for each dataset (variable definitions, coding)? Does a table/figure-to-script mapping exist (which script produces which output)? Are PRNG seeds documented for any simulation or bootstrap procedures? Is data provenance documented (source, license, redistribution rights)? Could a competent researcher reproduce the main results from the archive alone? Flag missing files, undocumented steps, or broken path references.

**Output format for each agent**: Write findings to the agent's assigned file under `.review-tmp/` (see Orchestration contract above). Use structured lists, not prose. For each issue:
- Severity: `[CRITICAL]`, `[RECOMMENDED]`, or `[MINOR]`
- Location: file path and line number or section name
- Issue: one sentence describing the problem
- Fix: one sentence describing what to do

**Severity rubric** (apply consistently across all agents):
- `[CRITICAL]` — blocks submission: wrong numbers, broken references, missing ethics/data-availability statement when required, silent deviation from a pre-registration, anonymization failure, unreproducible main result.
- `[RECOMMENDED]` — will draw reviewer complaint: unsupported claim, missing robustness check, undefined threshold, missing limitation, insufficient figure caption, undocumented exclusion.
- `[MINOR]` — polish: style, typography, citation format, wording consistency.

### 3. Cross-Check (launch after Phase 2 completes)

Both cross-check agents read the Phase 2 output files from `.review-tmp/` directly. They do not need findings pasted into their prompts — tell each cross-checker which files to read and write their own validated output to `.review-tmp/agent-10-content-numbers.md` and `.review-tmp/agent-11-technical.md`.

**Agent 10 — Content, Numbers & Design Cross-Checker**: Read `.review-tmp/agent-1-content.md`, `.review-tmp/agent-2-numbers.md`, `.review-tmp/agent-6-consort.md`, and `.review-tmp/agent-7-prereg.md`. For each `[CRITICAL]` or `[RECOMMENDED]` item, verify it against the actual paper text. Flag false positives (issue doesn't exist or is already addressed). Add any issues missed — pay particular attention to: abstract vs. conclusion claims that drift from body evidence, significance thresholds, multiple comparisons, denominator consistency (e.g., percentages computed with vs. without a residual category), ITT vs. per-protocol mismatches, CONSORT-number vs. table-N mismatches, and silent pre-registration deviations (registered analyses not reported, reported analyses not registered).

**Agent 11 — Technical Cross-Checker**: Read `.review-tmp/agent-3-references.md`, `agent-4-dois.md`, `agent-5-writing.md`, `agent-8-figures.md`, and `agent-9-archive.md`. Verify each flagged item against the actual files — check the bibliography, figure files, figure/table numbering, and archive directory. Confirm or refute each finding. Add any issues missed.

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
| CONSORT participant flow         | PASS/FAIL/NA      |       |
| ITT & baseline balance reported  | PASS/FAIL/NA      |       |
| Attrition-by-arm reported        | PASS/FAIL/NA      |       |
| Pre-registration deviations disclosed | PASS/FAIL/NA |       |
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
- [ ] Design family identified and, when applicable, the relevant sibling skill (`conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr-pipeline`, `methods-reporting`) was invoked and its output folded into Agent 9
- [ ] `.review-tmp/` scratch directory created and all Phase 2 agents wrote to their assigned file
- [ ] All 9 Phase 2 agents launched in parallel in a single message (Agents 6 and 7 marked `NA` for non-experimental / non-preregistered papers)
- [ ] Phase 3 cross-checkers read Phase 2 output files directly from `.review-tmp/`
- [ ] Severity rubric (CRITICAL / RECOMMENDED / MINOR) applied consistently across all agents
- [ ] Agent prompts reference specific file paths, not generic placeholders
- [ ] For experimental papers: Agent 6 audited CONSORT participant flow, ITT primacy, baseline balance, attrition-by-arm, randomization procedure, and blinding
- [ ] For experimental papers: Agent 7 produced a PAP-to-paper hypothesis mapping table and classified every reported analysis as confirmatory or exploratory
- [ ] Forking-paths audit (DV/covariate/sample/transformation choices) was completed by Agent 7
- [ ] Cross-check agents verified every CRITICAL and RECOMMENDED finding against actual files
- [ ] False positives identified and removed from the final report
- [ ] Every issue in the report includes a file path and line number (or section name)
- [ ] The journal-readiness checklist covers all dimensions present in the table
- [ ] The "What Still Needs Your Input" section is populated with items requiring author knowledge
- [ ] Report distinguishes objective errors from subjective suggestions
- [ ] Report includes a Strengths section (not just problems)
- [ ] For a worked example of a filled Pre-Submit Report, see `reference/example-report.md`
