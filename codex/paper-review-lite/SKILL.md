---
name: paper-review-lite
description: "Run a pre-submission manuscript audit covering argument, numerics, references, writing, figures, methods, preregistration, and replication readiness. Add --codex for a cross-model pass in which Codex and Claude review independently and verify each other's findings."
---

# Paper Pre-Submission Review (Lite)

Use a new output path or directory for each run; preserve earlier results and existing user edits.

## Heritage and scope

An 11-subagent pre-submission review that runs inside a Codex session with no extra review tool to install. Nine parallel dimension agents find issues, two cross-checkers verify each finding against the manuscript before it reaches the report, and the lead synthesizes. This is the Codex-native counterpart to [`presubmit`](https://github.com/scdenney/presubmit), itself descended from the [reviewer2](https://github.com/isitcredible/reviewer2) adversarial peer-review pipeline, and it inherits that lineage's two commitments: a critical-reviewer posture, and a verification cascade that drops any finding not pinned to a quoted passage. It is the fast in-flow check, not the full pipeline — see the last section for when to reach for `presubmit` instead.

Two modes share one specification. The default mode runs the whole review inside Codex. **Cross-model mode (`--codex`)** runs the same dimensions in two cohorts — one Codex, one Claude via the `claude -p` CLI — and has each cohort verify the other's findings. Everything through § 4 applies to both modes; the cross-model section at the end adds only what is specific to running two model families.

## Delegation gate

Run the subagent workflow only when the user explicitly invokes `$paper-review-lite` or asks for parallel/subagent review. If the skill loads implicitly, either perform the dimensions sequentially in the lead context or ask before spawning agents. Cross-model mode has its own additional gate — see § "Cross-model mode".

## Instructions

Nine agents each audit a different dimension; two cross-check agents then audit those Phase 2 findings for hallucinations, false positives, and missed issues. The deliverable is a severity-ranked Pre-Submit Report with a journal-readiness checklist.

**Critical-Reviewer posture (required for every sub-agent).** Brutally honest on the work, fair to the people. Attack the *argument or the data*, never the *authors* — "the claim on line X is not supported by the evidence on line Y" is in scope; framing like "fraudulent" or "incompetent" is not. Prestige carries no weight: reputation, journal status, citation counts, and prior peer review are not evidence.

### 1. Orientation (do this yourself before launching agents)

Read the paper yourself to understand its structure before writing agent prompts. Determine:

- Where the paper source lives (LaTeX `.tex` vs Pandoc `.md` vs Word) and what the build command is
- Whether a Supplementary Information file exists and where it lives
- Where figures are stored and how they are referenced (relative paths, figure directories)
- Whether a replication archive exists (look for `replication/`, `archive/`, `data/`, README files)
- The paper's rough structure: section names, approximate page count, key claims in the abstract
- The bibliography format and location (`.bib`, inline, etc.)
- **Design family.** Is this a conjoint/factorial-vignette paper, a list experiment, a topic-modeling or LLM-classification study, or a VLM-OCR corpus paper? If so, also invoke the relevant sibling skill (`conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr`) and fold its domain-specific checklist into Agent 9's deliverable. For any experimental manuscript, also run `methods-reporting` in audit mode so its 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8.

Record actual absolute paths, design family, source format, target journal, and missing inputs. Use this knowledge to write **specific** agent prompts that reference actual file paths, section names, and relevant files. Generic prompts produce shallow results.

**Orchestration contract.** Before Phase 2, create a scratch directory `.review-tmp/` in the paper's working directory. Each Phase 2 agent writes its structured findings to a dedicated file — `agent-1-content.md`, `agent-2-numbers.md`, `agent-3-references.md`, `agent-4-dois.md`, `agent-5-writing.md`, `agent-6-consort.md`, `agent-7-prereg.md`, `agent-8-figures.md`, `agent-9-archive.md` — using the output format specified below. Use these exact filenames; Phase 3 cross-checkers read them directly rather than having findings pasted into their prompts. Launch the Phase 2 agents in parallel batches that respect the runtime's concurrency limit, and start Phase 3 once every required output file exists. For experimental manuscripts, Agents 6 (CONSORT/randomization-and-flow) and 7 (pre-registration verification) are mandatory; for non-experimental manuscripts they can be skipped and their checklist rows marked `NA`. After the Pre-Submit Report has been delivered, delete `.review-tmp/` — it is workflow scratch, not a deliverable — unless the user asks to keep it.

Each subagent receives only the relevant dimension block, the manuscript and related absolute paths, the common severity and quote requirements, and its assigned output path. Keep agents blind to one another. A non-zero exit, an empty output file, or a refusal is a failed reviewer, not evidence that the manuscript passed.

### 2. Parallel Deep Review (nine agents)

**Agent 1 — Content & Argument (Red Team primary)**: Read the full paper. Your posture is adversarial but fair: find every place the argument is weaker than the paper presents it to be. Check logical flow from introduction through conclusion. Identify unsupported claims, logical gaps, missing caveats, and places where the argument is unclear or circular. Flag any claims in the abstract not backed up in the body. Note missing discussion of limitations. Check whether the framing accurately positions the contribution relative to cited prior work.

**Agent 2 — Numbers & Internal Consistency**: Check every quantitative claim against JARS-Quant reporting expectations (Appelbaum et al. 2018). Do numbers in the abstract match the body? Do table values match in-text references? Do SI cross-references point to the right appendices/tables? Are confidence intervals, p-values, N counts, and effect sizes reported consistently throughout? Flag multiple-comparisons issues (many tests without correction or discussion). Verify that significance thresholds are defined and used consistently. For experimental papers, verify denominator consistency across ITT and any complier/compliance-adjusted analyses and flag any manipulation-check that is present in the design but missing from the results. Flag forking-paths risks explicitly: DV switching between primary and secondary outcomes, covariate-set changes across models, transformation or subsetting decisions not traceable to a pre-registration, and any analysis whose choice was visibly made after seeing outcome data (Wicherts et al. 2016; Gelman & Loken 2014; Simmons et al. 2011). Do NOT audit the CONSORT flow, baseline balance, attrition-by-arm, or PAP-to-paper mapping — those are Agents 6 and 7.

**Agent 3 — References & Citations**: Audit the bibliography file. Are all cited works present? Are there uncited entries? Check for stale working papers (2025+) that may now be published — flag entries that need author verification. Check formatting consistency (journal names, author encoding, entry types). Do NOT check DOIs — that is Agent 4's job.

**Agent 4 — DOI Audit**: Check every bibliography entry for a DOI. For entries missing a DOI, attempt to locate one via web search (title + author + "doi"). Report which entries are missing DOIs and, where found, provide the correct DOI. Verify that existing DOIs resolve to the correct paper — wrong-paper DOIs are a common copy-paste error. Where the sandbox blocks network access, limit yourself to offline checks (DOI present/absent, format validity, internal consistency with the entry) and tag entries `NEEDS WEB VERIFICATION` rather than guessing.

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
- Quote: a verbatim span (≤ 2 sentences) from the manuscript that supports the finding — **required** for every `[CRITICAL]` and `[RECOMMENDED]` item, optional for `[MINOR]`. Findings without a quote will be dropped by the Phase 3 cross-checker as likely hallucinations.

**Severity rubric** (apply consistently across all agents):
- `[CRITICAL]` — blocks submission: wrong numbers, broken references, missing ethics/data-availability statement when required, silent deviation from a pre-registration, anonymization failure, unreproducible main result.
- `[RECOMMENDED]` — will draw reviewer complaint: unsupported claim, missing robustness check, undefined threshold, missing limitation, insufficient figure caption, undocumented exclusion.
- `[MINOR]` — polish: style, typography, citation format, wording consistency.

### 3. Cross-Check

Tell each cross-checker which `.review-tmp/` files to read, and where to write its own validated output — `.review-tmp/agent-10-content-numbers.md` and `.review-tmp/agent-11-technical.md`.

**Agent 10 — Content, Numbers & Design Cross-Checker (Blue Team / verification)**: Read `.review-tmp/agent-1-content.md`, `.review-tmp/agent-2-numbers.md`, `.review-tmp/agent-6-consort.md`, and `.review-tmp/agent-7-prereg.md`. For each `[CRITICAL]` or `[RECOMMENDED]` item: (a) verify the cited quote appears verbatim at the cited location in the manuscript; drop items whose quote is missing, paraphrased, or does not support the claim made — these are hallucinations; (b) verify the issue itself against the actual paper text and flag false positives (issue doesn't exist or is already addressed); (c) steel-man the paper — for each retained finding, briefly note whether the paper anticipates or partially addresses the concern, since a partial response may downgrade severity. Add any issues missed — pay particular attention to: abstract vs. conclusion claims that drift from body evidence, significance thresholds, multiple comparisons, denominator consistency (e.g., percentages computed with vs. without a residual category), ITT vs. per-protocol mismatches, CONSORT-number vs. table-N mismatches, and silent pre-registration deviations (registered analyses not reported, reported analyses not registered).

**Agent 11 — Technical Cross-Checker (Blue Team / verification)**: Read `.review-tmp/agent-3-references.md`, `agent-4-dois.md`, `agent-5-writing.md`, `agent-8-figures.md`, and `agent-9-archive.md`. For each flagged item: (a) verify the cited location actually contains the described issue (drop hallucinations); (b) verify the finding itself against the actual files — check the bibliography, figure files, figure/table numbering, and archive directory; (c) confirm or refute each finding. Add any issues missed.

### 4. Synthesis

**Before listing anything, consolidate.** If two or more Phase 2 agents independently flagged the same underlying issue, present it once with the strongest supporting quote — the same complaint restated five times under five headings is an artifact of the parallel-agent structure and it erodes trust in the report. If a finder's own description includes language conceding the point ("does not in itself indicate a deviation from common practice," "while a real concern, this is standard in the literature," "the paper acknowledges this on p. X"), demote the issue one severity tier — or drop it if the concession negates the critique.

Compile validated, deduplicated findings into a single **Pre-Submit Report**:

```
## Pre-Submit Report: [Paper Title]
Date: [today]
Recommendation: [Submit as-is | Minor revisions before submit | Major revisions before submit | Hold for new analysis | Substantial restructuring needed]
Issues: [N critical, N recommended, N minor]

### Editor's Note (revision strategy — read first)

A 3–6 paragraph prose memo, in your own voice, summarizing the path to a revised version that defends the contribution. Not a punch list — the punch list is below. This section should:

- Open with the single most consequential addition that would *strengthen* rather than weaken the paper. (Often a small analytical addition, a missing robustness check, or a missing comparison whose result would convert the strongest critique into a supporting result.)
- Identify which Critical Issues require new analysis (cannot be addressed by rewriting alone) versus which are textual/framing fixes.
- Where the manuscript already concedes a point that a critique missed, name the concession and note that the fix may be a small expansion of the existing acknowledgement rather than a new section.
- Where two Critical Issues are coupled (fixing one resolves the other), say so.
- End with a short paragraph on what could be deferred to a future paper without weakening the current contribution.

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

"What Still Needs Your Input" lists items the review cannot resolve because they require author knowledge: ethics approval numbers, funding grant details, journal-specific formatting requirements, embargo status of data, or factual claims only the author can verify.

Every issue in the report carries a file path and line number (or section name), and objective errors (wrong numbers, broken references) are distinguished from subjective suggestions (writing style, framing). `references/example-report.md` is a filled example of the whole report. The final report is self-contained and does not expose scratch prompts or agent chatter.

## Cross-model mode (`--codex`)

Everything above still holds. This section replaces only the *who runs what* half of the workflow.

For demanding manuscript audits, prefer an Astra lead (`gpt-6-astra`, `xhigh`) or explicitly configured Astra reviewers when the runtime supports overrides. A skill cannot switch the running lead by declaration; retain an explicitly chosen model and record the actual runtime.

Codex stays the lead and Claude Code's non-interactive CLI supplies the second model family. Two cohorts independently apply the § 2 specification to the same paper, then each verifies the other's findings. Two model families have different blind spots, so both their agreements and their disagreements carry information; the adjudication step scores each combination. Neither cohort sees the other's findings during the Red Team phase.

### Sandbox constraint — read before the first `claude -p` call

`claude -p` requires working authentication and network access. Earlier restricted runs hung, but sandbox behavior depends on the current permissions profile. Use a bounded call under existing authorization; escalate only when the runtime supports it and access is needed. Report a failed reviewer call without simulating its findings.

### Preflight

1. Confirm that the user explicitly requested cross-model mode (`--codex`, `$paper-review-lite --codex`, or a cross-model audit). Otherwise run the default mode.
2. Locate the manuscript, supplement, bibliography, figures, preregistration, and replication archive.
3. Check `command -v claude` and run a harmless authentication/status check supported by the installed CLI. Do not print credentials.
4. Before the first call, confirm the user accepts an external model call that may consume separate credits — unless they already authorized Claude or cross-model execution.
5. If Claude is unavailable or authorization is declined, offer the fallback in § "Reduced-diversity mode".

Claude Code documents `claude -p` as its non-interactive interface. Use `--output-format text`, `--no-session-persistence`, and read-only tools for review calls. See [Run Claude Code programmatically](https://code.claude.com/docs/en/headless).

### Orient once

Follow § 1 verbatim, including the sibling-skill hand-offs: `methods-reporting` in audit mode for experimental manuscripts, whose 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8 **in both cohorts**; the matching design-family skill folded into Agent 9 **in both cohorts**. Generic prompts produce shallow reviews from both model families. Record absolute paths and create:

```text
.review-tmp/
├── codex/
├── claude/
└── cross-check/
```

Each cohort writes to its own subdirectory; cross-checkers read the *other* cohort's subdirectory. Use absolute paths for the manuscript and every output file — relative paths are ambiguous once a call runs with a different working directory.

### Phase 1 — independent Red Teams

**Codex cohort.** Run the nine § 2 review dimensions in parallel batches that respect the runtime's agent limit. Each subagent receives only the relevant dimension block, the manuscript and related absolute paths, the common severity and quote requirements, and its assigned output path under `.review-tmp/codex/`. Keep agents blind to one another. Require direct manuscript evidence for every critical or recommended issue.

**Claude cohort.** Run three independent Claude CLI calls concurrently when safe:

1. argument, claims, and numerical consistency;
2. references, DOI status, writing, figures, and tables;
3. methods, CONSORT/preregistration where applicable, and replication readiness.

Construct each prompt from the matching § 2 dimension blocks; do not paraphrase away requirements. Tell Claude to read the named files, print structured Markdown only, and never edit them. Redirect stdout to the assigned file under `.review-tmp/claude/`.

Use this command shape, substituting absolute paths and a complete prompt file:

```bash
claude -p \
  --output-format text \
  --no-session-persistence \
  --allowedTools "Read" \
  "$(< /absolute/path/to/prompt.txt)" \
  > /absolute/path/to/.review-tmp/claude/review-N.md
```

Do not use `--bare` unless API-key authentication is configured explicitly; bare mode skips normal OAuth and keychain discovery.

Live DOI resolution and missing-DOI web searches belong to whichever cohort actually has network access. Under sandbox that is neither, in which case both tag entries `NEEDS WEB VERIFICATION` and the report says so.

Validate every output file. A non-zero exit, empty file, or refusal is a failed reviewer, not evidence that the manuscript passed.

### Phase 2 — blind cross-check

After both cohorts finish, launch four verification passes:

- two Codex subagents verify Claude's content/methods and technical findings;
- two Claude CLI calls verify Codex's corresponding findings.

For each critical or recommended issue, require this sequence:

1. Find the quoted span at the cited location. If absent, mark `QUOTE FAILED` and drop it.
2. Check whether the manuscript already answers the concern elsewhere. If yes, mark `REFUTED` or `DOWNGRADE` with the contradicting location.
3. Check the issue on its merits. Mark `CONFIRMED`, `REFUTED`, or `DOWNGRADE`.
4. Do not add new issues during cross-checking.

Cross-checkers read the manuscript plus the other cohort's files, never their own cohort's findings. Where a cross-checker finds that its own cohort independently flagged the same issue, note the mutual catch for synthesis.

### Phase 3 — adjudicate

Apply these rules in order:

- **Mutual and confirmed:** both cohorts flagged it and both cross-checks confirmed. Retain at the stronger justified severity; label `Mutual (Codex + Claude)`. Highest-confidence findings.
- **Single-cohort and cross-confirmed:** retain at original severity; label the originating cohort and the confirmation. These often surface real but easy-to-miss problems.
- **Single-cohort and cross-refuted:** drop unless the lead rereads the source and records specific contrary evidence. If retained, demote one tier and note "cross-refuted, retained after lead re-read at <file:line>".
- **Quote failed:** drop as a hallucination on the finder's side.
- **Reviewer failed:** record reduced coverage; never convert missing output into a pass.

Codex-plugin result-handling guidance (stop after presenting review findings) applies to code-review handoffs, not here: the adjudication rules above are instructions to merge the two cohorts into one report, so stopping at the raw cohort findings leaves the skill unfinished.

Deduplicate by underlying issue, not wording — within cohort first, then across cohorts (a mutual catch is one entry, not two) — then demote self-conceded critiques per § 4. Then follow § 4 to write the recommendation, editor's note, severity-ranked issues, strengths, readiness checklist, and "What Still Needs Your Input", with one extra `Confidence` column on the critical and recommended tables:

```
| Severity | Confidence                                      | Location | Issue | Fix |
|----------|-------------------------------------------------|----------|-------|-----|
| CRITICAL | Mutual (Codex + Claude)                         | …        | …     | …   |
| CRITICAL | Asymmetric: Claude only, confirmed by Codex     | …        | …     | …   |
| CRITICAL | Asymmetric: Codex only, cross-refuted, retained after lead re-read | … | … | … |
```

### Reduced-diversity mode

If Claude cannot run, ask whether to continue with two blind Codex cohorts. If approved:

- give each cohort fresh context and identical specifications;
- keep cohorts blind until cross-checking;
- label the report `same-model independent review`, never `cross-model`; and
- state that agreement is weaker evidence because model-family blind spots are shared.

If the user declines, run the default mode or stop as requested.

### Cross-model completion checks

- Every retained critical or recommended issue has a verified quote, a location, and a confidence label.
- Both directions of cross-check completed, or reduced coverage is stated explicitly alongside any failed or empty reviewer output.
- Agents 6 and 7 marked `NA` in both cohorts for non-experimental or non-preregistered manuscripts.
- No agent edited the manuscript.
- The final report is self-contained and does not expose scratch prompts or agent chatter.
- `.review-tmp/` is removed after delivery unless the user asked to keep it.

## When to reach for `presubmit` instead

This skill covers most in-flow review needs. The heavier [`presubmit`](https://github.com/scdenney/presubmit) Python CLI runs ~30 stages and is the right tool when:

- You want **full adversarial pressure** — a dedicated Red Team whose personas (Breaker, Butcher, Shredder, Collector, Void) each attack the paper from a different angle, a Blue Team defence, separate numbers/fact-check/citation-verification cascades, and a legal pass; this skill compresses that into Agent 1 plus the two cross-checkers.
- You want a **standalone deliverable** — a single `report.txt` and optional editor's note, produced outside your Codex session. Useful when the review is the product: feedback to a co-author, a pre-print critique, or a final pass before external peer review.
- You want **resumability + cost tracking** — `presubmit` checkpoints every stage to disk; deleting a stage file forces that stage to re-run. Tracks per-stage API cost.
- You want a **math audit** — `presubmit` has an optional Mathpix-backed equation audit (`--math`); this skill doesn't.
- You want a **code-replication audit** — `presubmit` can ingest a replication archive and compare claims against the code (`--code`); this skill stops at the "does the archive look complete" question in Agent 9.

Trade-off: `presubmit` bills per-token against an Anthropic API key (separate from your Claude Code subscription). See `presubmit/README.md` for install, cost considerations, and known trade-offs vs. the upstream Gemini implementation.

| Mode | Adversarial depth | Cost | When |
|-------|-------------------|------|------|
| Default | Single-model, 11 agents, in-session verification cascade | Lightest | Fast in-flow review during writing |
| `--codex` | Cross-model, two blind cohorts plus four cross-checks | Roughly 2× the default, and Claude CLI calls may bill separately | Before submission, when you want maximum pressure and a second model family's blind spots |
| [`presubmit`](https://github.com/scdenney/presubmit) | ~30 stages, dedicated Red Team personas, Blue Team defence, math and code-replication audits, resumable, cost-tracked | Heaviest, separate Anthropic API key | The review is the deliverable. Co-author feedback, pre-print critique, final pre-submission pass. |
