---
name: paper-review-lite
description: Pre-submission audit of a manuscript — argument, numerical consistency, references and DOIs, writing, figures, CONSORT flow, pre-registration, replication archive. Use before submitting a paper, or whenever a draft needs an adversarial, quote-grounded review with a journal-readiness checklist. Add `--codex` to run the same specification independently on Claude and on Codex (GPT-5.6 "Sol") and cross-check the two sets of findings.
argument-hint: "[path to paper or describe manuscript to review] [--codex]"
context: fork  # Claude Code: run skill in a forked subagent context (isolated from conversation history). See https://code.claude.com/docs/en/skills#frontmatter-reference
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Agent
---

# Paper Pre-Submission Review (Lite)

## Heritage and scope

An 11-sub-agent pre-submission review that runs inside a Claude Code session — no extra install, billable against your Claude Code plan. Nine parallel dimension agents find issues, two cross-checkers verify each finding against the manuscript before it reaches the report, and the orchestrator synthesizes. This is the Claude-Code-native counterpart to [`presubmit`](https://github.com/scdenney/presubmit), our port of the [reviewer2](https://github.com/isitcredible/reviewer2) adversarial peer-review pipeline, and it inherits that lineage's two commitments: a critical-reviewer posture, and a verification cascade that drops any finding not pinned to a quoted passage. It is the fast in-flow check, not the full pipeline — see the last section for when to reach for `presubmit` instead.

Two modes share one specification. The default mode runs the whole review inside one model family. **Cross-model mode (`--codex`)** runs the same nine dimensions twice — once on Claude, once on Codex — and has each model verify the other's findings. Everything through § 4 applies to both modes; the cross-model section at the end adds only what is specific to running two model families.

## Instructions

Nine agents each audit a different dimension; two cross-check agents then audit those Phase 2 findings for hallucinations, false positives, and missed issues. The deliverable is a severity-ranked Pre-Submit Report with a journal-readiness checklist.

**Critical-Reviewer posture (required for every sub-agent).** Brutally honest on the work, fair to the people. Attack the *argument or the data*, never the *authors* — "the claim on line X is not supported by the evidence on line Y" is in scope; framing like "fraudulent" or "incompetent" is not. Prestige carries no weight: reputation, journal status, citation counts, and prior peer review are not evidence.

**Orchestration lead.** Whatever model you are running — Claude Opus 5 or Fable 5.1 — orchestrates: orientation, launching the dimension sub-agents, the cross-check cascade, the synthesis. The sub-agents do the reading. **If you are on Opus, run at medium reasoning effort by default** (raise to high for the Phase 4 adjudication, deduplication, and Editor's Note — a bounded judgment call, not the sustained orchestration role), and fan Phase 2 (nine parallel dimensions) and Phase 3 (cross-check) out. If the `Workflow` tool is listed among your tools this session, express those two phases as a `Workflow`; otherwise — the common case, since dynamic Workflows are gated per session by org policy, the launch gate, or the "Dynamic workflows" setting in `/config`, and invoking a skill does not grant them — launch each phase's agents with parallel `Agent` calls in a single message and start the next phase once their outputs land. The fallback is the default, not a degraded mode; branch on tool availability, not on which model is leading. On the Workflow path, use a `pipeline()` so each dimension's findings go to cross-check as soon as that dimension completes; on the `Agent` path, launch all nine Phase 2 agents in one message and start Phase 3 once the nine files exist.

**Sub-agent model and effort assignment.** Route by task type, not by agent number — argument-level dimensions (evaluating logical structure, cross-referencing claims, detecting silent discrepancies) go to Opus at `high`, pinned; mechanical dimensions (matching, existence checks, checklist audits) go to Sonnet at `medium`, pinned. The one exception is the argument-level cross-checker (Agent 10). It verifies Opus's own findings, so it runs on Fable rather than Opus — a same-model checker grading its own kind of work is the weakest link in this design, the same failure mode `presubmit`'s Red Team/Blue Team split and `journal-review`'s Chief Reviewer synthesis are built to avoid. This is a bounded single-shot call per sub-agent, not a sustained role, so set the effort explicitly rather than letting it inherit the orchestrator's own (lower, sustained-role) effort — noting that the standalone `Agent` tool has no effort field, so on the `Agent` path the effort instruction goes into the prompt text itself; only `agent()` inside a `Workflow` accepts `opts.effort` — see [`orchestrate`](../orchestrate/SKILL.md) for the mechanical-vs-argument-level routing pattern and the same effort reasoning. The Phase 3 cross-checker groupings track this split exactly:

| Sub-agent | Model | Effort | Why |
|---|---|---|---|
| Agent 1 — Content & Argument | Opus | `high`, pinned | evaluates logical structure and argument quality |
| Agent 2 — Numbers & Internal Consistency | Opus | `high`, pinned | cross-references quantitative claims across the paper and audits forking-paths risk |
| Agent 3 — References & Citations | Sonnet | `medium`, pinned | matches bibliography entries against in-text citations — mechanical |
| Agent 4 — DOI Audit | Sonnet | `medium`, pinned | lookup and verification against bibliography entries — mechanical |
| Agent 5 — Writing Quality & Journal Compliance | Sonnet | `medium`, pinned | style/craft review plus a completeness checklist — no argument evaluation |
| Agent 6 — CONSORT / Randomization & Flow | Opus | `high`, pinned | detects silent discrepancies across N's, arms, and stages |
| Agent 7 — Pre-Registration Verification | Opus | `high`, pinned | PAP-to-paper hypothesis mapping and forking-paths audit |
| Agent 8 — Figures, Tables & Formatting | Sonnet | `medium`, pinned | existence, numbering, and formatting checks — mechanical |
| Agent 9 — Replication Archive | Sonnet | `medium`, pinned | documentation-completeness audit against a checklist — mechanical |
| Agent 10 — Content/Numbers/Design Cross-Checker | Fable | `high`, pinned | re-verifies Agents 1, 2, 6, 7's argument-level findings and steel-mans the paper — deliberately off Opus so the checker isn't the same model as what it's checking |
| Agent 11 — Technical Cross-Checker | Sonnet | `medium`, pinned | re-verifies Agents 3, 4, 5, 8, 9's mechanical findings — same tier as its source agents |

### 1. Orientation (do this yourself before launching agents)

Read the paper yourself to understand its structure before writing agent prompts. Determine:

- Where the paper source lives (LaTeX `.tex` vs Pandoc `.md` vs Word) and what the build command is
- Whether a Supplementary Information file exists and where it lives
- Where figures are stored and how they are referenced (relative paths, figure directories)
- Whether a replication archive exists (look for `replication/`, `archive/`, `data/`, README files)
- The paper's rough structure: section names, approximate page count, key claims in the abstract
- The bibliography format and location (`.bib`, inline, etc.)
- **Design family.** Is this a conjoint/factorial-vignette paper, a list experiment, a topic-modeling or LLM-classification study, or a VLM-OCR corpus paper? If so, also invoke the relevant sibling skill (`conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr`) and fold its domain-specific checklist into Agent 9's deliverable. For any experimental manuscript, also run `methods-reporting` in audit mode so its 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8.

Use this knowledge to write **specific** agent prompts that reference actual file paths, section names, and relevant files. Generic prompts produce shallow results.

**Orchestration contract.** Before Phase 2, create a scratch directory `.review-tmp/` in the paper's working directory. Each Phase 2 agent writes its structured findings to a dedicated file — `agent-1-content.md`, `agent-2-numbers.md`, `agent-3-references.md`, `agent-4-dois.md`, `agent-5-writing.md`, `agent-6-consort.md`, `agent-7-prereg.md`, `agent-8-figures.md`, `agent-9-archive.md` — using the output format specified below. Use these exact filenames; Phase 3 cross-checkers read them directly rather than having findings pasted into their prompts. Run the nine Phase 2 agents concurrently: under a `Workflow` pipeline each cross-check fires as its inputs land; with parallel `Agent` calls, launch all nine in a single message and start Phase 3 once the nine files exist. For experimental manuscripts, Agents 6 (CONSORT/randomization-and-flow) and 7 (pre-registration verification) are mandatory; for non-experimental manuscripts they can be skipped and their checklist rows marked `NA`. After the Pre-Submit Report has been delivered, delete `.review-tmp/` — it is workflow scratch, not a deliverable — unless the user asks to keep it.

### 2. Parallel Deep Review (nine agents, concurrent)

**Agent 1 — Content & Argument (Red Team primary)**: Read the full paper. Your posture is adversarial but fair: find every place the argument is weaker than the paper presents it to be. Check logical flow from introduction through conclusion. Identify unsupported claims, logical gaps, missing caveats, and places where the argument is unclear or circular. Flag any claims in the abstract not backed up in the body. Note missing discussion of limitations. Check whether the framing accurately positions the contribution relative to cited prior work.

**Agent 2 — Numbers & Internal Consistency**: Check every quantitative claim against JARS-Quant reporting expectations (Appelbaum et al. 2018). Do numbers in the abstract match the body? Do table values match in-text references? Do SI cross-references point to the right appendices/tables? Are confidence intervals, p-values, N counts, and effect sizes reported consistently throughout? Flag multiple-comparisons issues (many tests without correction or discussion). Verify that significance thresholds are defined and used consistently. For experimental papers, verify denominator consistency across ITT and any complier/compliance-adjusted analyses and flag any manipulation-check that is present in the design but missing from the results. Flag forking-paths risks explicitly: DV switching between primary and secondary outcomes, covariate-set changes across models, transformation or subsetting decisions not traceable to a pre-registration, and any analysis whose choice was visibly made after seeing outcome data (Wicherts et al. 2016; Gelman & Loken 2014; Simmons et al. 2011). Do NOT audit the CONSORT flow, baseline balance, attrition-by-arm, or PAP-to-paper mapping — those are Agents 6 and 7.

**Agent 3 — References & Citations**: Audit the bibliography file. Are all cited works present? Are there uncited entries? Check for stale working papers (2025+) that may now be published — flag entries that need author verification. Check formatting consistency (journal names, author encoding, entry types). Do NOT check DOIs — that is Agent 4's job.

**Agent 4 — DOI Audit**: Check every bibliography entry for a DOI. For entries missing a DOI, attempt to locate one via web search (title + author + "doi"). Report which entries are missing DOIs and, where found, provide the correct DOI. Verify that existing DOIs resolve to the correct paper — wrong-paper DOIs are a common copy-paste error.

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

**Agent 10 — Content, Numbers & Design Cross-Checker (Blue Team / verification, Fable)**: Read `.review-tmp/agent-1-content.md`, `.review-tmp/agent-2-numbers.md`, `.review-tmp/agent-6-consort.md`, and `.review-tmp/agent-7-prereg.md`. For each `[CRITICAL]` or `[RECOMMENDED]` item: (a) verify the cited quote appears verbatim at the cited location in the manuscript; drop items whose quote is missing, paraphrased, or does not support the claim made — these are hallucinations; (b) verify the issue itself against the actual paper text and flag false positives (issue doesn't exist or is already addressed); (c) steel-man the paper — for each retained finding, briefly note whether the paper anticipates or partially addresses the concern, since a partial response may downgrade severity. Add any issues missed — pay particular attention to: abstract vs. conclusion claims that drift from body evidence, significance thresholds, multiple comparisons, denominator consistency (e.g., percentages computed with vs. without a residual category), ITT vs. per-protocol mismatches, CONSORT-number vs. table-N mismatches, and silent pre-registration deviations (registered analyses not reported, reported analyses not registered).

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

Every issue in the report carries a file path and line number (or section name), and objective errors (wrong numbers, broken references) are distinguished from subjective suggestions (writing style, framing). `reference/example-report.md` is a filled example of the whole report.

## Cross-model mode (`--codex`)

Everything above still holds. This section replaces only the *who runs what* half of the workflow.

Two reviewers — Claude (the orchestrator) and Codex (GPT-5.6 "Sol" at `xhigh` reasoning effort, invoked via Bash `codex exec`) — independently apply the § 2 specification to the same paper, then each plays Blue Team to the other's Red Team. Two model families have different blind spots, so both their agreements and their disagreements carry information; Phase 4 scores each combination. Neither team sees the other's findings during Phase 2.

Roughly 22 model calls total (9 Claude Red Team, 9 Codex Red Team, 4 cross-model Blue Team) plus orientation and synthesis by the orchestrator. Reach for it before submission when you want maximum adversarial pressure and a second model family's blind spots.

The Claude orchestrator is whatever model you are running — Opus 5 or Fable 5.1 — and its role is unchanged from § "Orchestration lead": orientation, launching both Red Teams, spawning the cross-checkers, adjudicating. Raise to high effort for the Phase-4 cross-team adjudication and Editor's Note. Fan the 18 Phase-2 calls and 4 Phase-3 cross-checks out the same way — a `Workflow` if that tool is listed this session, parallel `Agent` calls otherwise. The Codex-side calls are `Bash` invocations either way. See [`orchestrate`](../orchestrate/SKILL.md) for the decorrelated-peer rationale.

### Codex invocation mechanism

Claude Code has no native `codex:codex-rescue` subagent. Every "spawn Codex" reference below means: use the `Bash` tool to invoke `codex exec` directly. Pattern (substitute `OUTPUT_PATH` with the agent's output file path and inline the prompt body inside the heredoc):

```bash
codex exec \
  --model gpt-5.6-sol \
  -c model_reasoning_effort=xhigh \
  --sandbox workspace-write \
  --skip-git-repo-check \
  -C "$(dirname OUTPUT_PATH)" \
  "$(cat <<'CODEXEOF'
<the XML prompt template for this agent, with PAPER_PATH and OUTPUT_PATH substituted as literals>
CODEXEOF
)" < /dev/null
```

**Required:**

- **`--model gpt-5.6-sol -c model_reasoning_effort=xhigh`** — pins the peer explicitly rather than relying on `codex exec`'s own implicit default, so it does not silently drift if that default changes upstream.
- **`< /dev/null`** — closes stdin. Without it, `codex exec` hangs indefinitely on "Reading additional input from stdin..." even when the prompt is passed as a CLI argument. This is the single most common failure mode.
- **`run_in_background: true`** on every `Bash` call. Eleven parallel Codex calls per run (9 Phase 2 + 2 Phase 3) make foreground execution impractical.
- **`timeout: 600000`** (10 minutes) as a harness backstop. If a call hangs for any reason, the harness kills it.

After each Codex Bash task notifies completion, `Read` its output file. Treat any of the following as a Codex agent failure (skip that finding's contribution in adjudication, log the failure in the report):

- Exit code ≠ 0.
- No session file appeared in `~/.codex/sessions/` (Codex did not actually start).
- The `OUTPUT_PATH` file is missing or empty.

### Orientation and orchestration contract

Run § 1 verbatim, including the sibling-skill hand-offs: `methods-reporting` in audit mode for experimental manuscripts, whose 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8 **on both teams**; the matching design-family skill folded into Agent 9 **on both teams**. Generic prompts produce shallow reviews from both model families.

Replace the flat `.review-tmp/` layout with:

```
.review-tmp/
├── claude/
│   ├── agent-1-content.md
│   ├── agent-2-numbers.md
│   ├── agent-3-references.md
│   ├── agent-4-dois.md
│   ├── agent-5-writing.md
│   ├── agent-6-consort.md
│   ├── agent-7-prereg.md
│   ├── agent-8-figures.md
│   └── agent-9-archive.md
├── codex/
│   ├── agent-1-content.md   (same dimensions, Codex output)
│   ├── ...
│   └── agent-9-archive.md
└── cross-check/
    ├── claude-checks-codex-content.md     (covers Codex agents 1, 2, 6, 7)
    ├── claude-checks-codex-technical.md   (covers Codex agents 3, 4, 5, 8, 9)
    ├── codex-checks-claude-content.md
    └── codex-checks-claude-technical.md
```

Both teams write independently to their own subdirectory. Cross-checkers read the *other* team's subdirectory. Use absolute paths when spawning Codex sub-agents — `codex exec`'s `-C` flag sets the working directory, but absolute `PAPER_PATH` and `OUTPUT_PATH` values in the prompt remove ambiguity when the paper lives outside that CWD.

### Phase 2 — dual independent Red Team (18 parallel calls)

Launch all 18 review calls in a single message.

- **9 Claude sub-agents** via the `Agent` tool (default `subagent_type`). Use the § 2 agent prompts (Agents 1–9) verbatim, but redirect output to `.review-tmp/claude/agent-N-*.md`. Carry over the § "Sub-agent model and effort assignment" pins rather than defaulting all nine to one model: Opus `high` for the argument-level dimensions (1, 2, 6, 7), Sonnet `medium` for the mechanical ones (3, 4, 5, 8, 9).
- **9 Codex sub-agents** via the `Bash` tool, following § "Codex invocation mechanism". Use the Codex Phase 2 template below as the prompt body, one call per dimension. Output to `.review-tmp/codex/agent-N-*.md`.

Both teams apply the same dimension definitions, the same Critical-Reviewer posture, and the same severity rubric from § 2. The point of running two model families on one specification is to compare independent applications of one standard, not to give them different jobs.

**One carve-out — Codex Agent 4 (DOI audit) has no web access.** The `codex exec` sandbox cannot perform the web searches that the Agent 4 prompt asks for. Tell Codex's Agent 4 to limit itself to offline checks (DOI present/absent, format validity, internal consistency with the entry) and to tag entries `NEEDS WEB VERIFICATION` instead of attempting lookups; live DOI resolution and missing-DOI searches are the Claude team's Agent 4's job (it has WebSearch/WebFetch).

Agents 6 (CONSORT) and 7 (pre-registration) are required for experimental manuscripts and marked `NA` for non-experimental ones on both teams.

### Phase 3 — cross-model adversarial verification (4 parallel calls)

Each model verifies the other's findings. Cross-checkers do not add new findings; that was Phase 2's job. They verify, refute, or downgrade.

**Claude cross-checks Codex (2 sub-agents via `Agent`).**

- Sub-agent A reads `.review-tmp/codex/agent-{1,2,6,7}-*.md` and the manuscript. Writes `.review-tmp/cross-check/claude-checks-codex-content.md`.
- Sub-agent B reads `.review-tmp/codex/agent-{3,4,5,8,9}-*.md` plus the manuscript, bibliography, and archive. Writes `.review-tmp/cross-check/claude-checks-codex-technical.md`.

For each Codex `[CRITICAL]` or `[RECOMMENDED]` finding, the cross-checker verifies the cited verbatim quote appears at the cited location, verifies the issue against the actual paper, flags any Codex finding that Claude also flagged independently in `.review-tmp/claude/` (mutual catch — note for synthesis), and steel-mans the paper. When the paper anticipates or partially addresses the concern, note it for severity downgrade.

**Codex cross-checks Claude (2 sub-agents via `Bash` following § "Codex invocation mechanism").**

- Sub-agent C reads `.review-tmp/claude/agent-{1,2,6,7}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-content.md`.
- Sub-agent D reads `.review-tmp/claude/agent-{3,4,5,8,9}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-technical.md`.

Use the Codex Phase 3 template below. Same verification protocol.

### Phase 4 — adjudication and synthesis (orchestrator, direct)

The Codex plugin's result-handling guidance — stop after presenting review findings and change nothing — governs code-review handoffs, not this skill: here the adjudication step below *is* the instructed work, and it produces a report, not a code change.

Build the consolidated Pre-Submit Report by adjudicating across teams.

- **Mutual.** Both teams flagged it; both cross-checkers confirmed. Mark `[CRITICAL ✓✓]` or `[RECOMMENDED ✓✓]`. Highest-confidence findings.
- **Asymmetric, cross-confirmed.** One team flagged; the other team's cross-checker confirmed against the paper. Retain at original severity. Mark `[CRITICAL ✓]` or `[RECOMMENDED ✓]`. These often surface real but easy-to-miss problems.
- **Asymmetric, cross-refuted.** One team flagged; the other team's cross-checker refuted against the paper. Default action is to drop. The orchestrator can override by re-reading the manuscript directly, in which case retain at one tier below original severity with the note "single-team finding, cross-refuted, retained after orchestrator re-read at <file:line>".
- **Quote-failed.** The cross-checker could not find the cited verbatim span. Drop as hallucination on the finder's side.

Apply the § 4 synthesis rules in order. Deduplicate within-team first (multiple agents on the same team flagging the same underlying issue), then across-team (a mutual catch is one entry, not two), then demote self-conceded critiques. The report format is § 4 exactly — single-line Recommendation at the top, then the Editor's Note, then Critical / Recommended / Minor lists, then Strengths, then the Journal-Readiness Checklist, then "What Still Needs Your Input" — with one extra column on the Critical Issues and Recommended Changes tables.

```
| Severity | Confidence                                      | Location | Issue | Fix |
|----------|-------------------------------------------------|----------|-------|-----|
| CRITICAL | Mutual (Claude + Codex)                         | …        | …     | …   |
| CRITICAL | Asymmetric: Codex only, confirmed by Claude     | …        | …     | …   |
| CRITICAL | Asymmetric: Claude only, cross-refuted, retained after orchestrator re-read | … | … | … |
```

### Codex Phase 2 template (one per dimension, 9 total)

Use the XML block below as the prompt body inside the Bash invocation from § "Codex invocation mechanism". Substitute `DIMENSION_INSTRUCTIONS` with the verbatim text of the corresponding agent from § 2 (the full text of Agent 1, Agent 2, …, Agent 9 — do not paraphrase), and `SEVERITY_RUBRIC` with the verbatim § 2 severity rubric. Substitute `PAPER_PATH` with the absolute manuscript path and `OUTPUT_PATH` with the absolute path to the Codex agent's output file under `.review-tmp/codex/`.

```xml
<task>
You are a Critical Reviewer auditing the manuscript at PAPER_PATH for the dimension below.

Posture (required): adversarial but fair. Find every place the argument is weaker than the paper presents it to be. Attack the argument and the evidence, not the authors — "the claim on line X is not supported by the evidence on line Y", never "the authors are incompetent".

Dimension:

DIMENSION_INSTRUCTIONS

Write your findings to OUTPUT_PATH.

A second model (Claude) is independently performing the same review on the same paper for the same dimension. You will not see its findings. After both passes complete, each model's findings will be verified by the other. Findings without a verbatim quote will be dropped as hallucinations during cross-check.
</task>

<output_format>
Structured list, not prose. For each issue:
- Severity: [CRITICAL] / [RECOMMENDED] / [MINOR]
- Location: file path and line number, or section name
- Issue: one sentence describing the problem
- Fix: one sentence describing what to do
- Quote: a verbatim span (≤ 2 sentences) from the manuscript that supports the finding. REQUIRED for every [CRITICAL] and [RECOMMENDED] finding. Optional for [MINOR].

Severity rubric (apply consistently):

SEVERITY_RUBRIC
</output_format>

<action_safety>
Read PAPER_PATH and any files it references (bibliography, archive, SI). Write only to OUTPUT_PATH; do not edit the manuscript or any other file.
</action_safety>

<default_follow_through_policy>
Apply the dimension end-to-end without stopping for confirmation.
If the finding is unambiguous, record it.
If the finding requires author knowledge to confirm (embargo status, IRB number), record it as [RECOMMENDED] with the caveat "requires author confirmation".
Do not ask clarifying questions mid-run.
</default_follow_through_policy>
```

### Codex Phase 3 template (cross-check Claude's findings)

Used for sub-agents C and D in Phase 3. Substitute `PAPER_PATH`, `INPUT_FILES` (a comma-separated list of `.review-tmp/claude/agent-N-*.md` paths the cross-checker should read), and `OUTPUT_PATH`.

```xml
<task>
You are a verification cross-checker. Another model (Claude) has produced findings about the manuscript at PAPER_PATH. Your job is to verify each finding against the actual manuscript.

Read the findings file(s) at INPUT_FILES. For each [CRITICAL] or [RECOMMENDED] finding, output one verdict entry.

1. QUOTE CHECK. Does the cited verbatim quote appear at the cited location in PAPER_PATH? If not, verdict is "QUOTE FAILED — drop as hallucination".
2. ISSUE CHECK. Does the issue itself hold up against the actual paper text? If the issue does not exist, is already addressed elsewhere in the paper, or is a misreading, verdict is "REFUTED" with a one-sentence explanation citing the paper line that refutes it.
3. STEEL-MAN. If the issue is real, note whether the paper anticipates or partially addresses the concern. If it does, verdict is "CONFIRMED, downgrade one severity tier — partially addressed at <file:line>".
4. OTHERWISE. Verdict is "CONFIRMED".

Do not add new findings of your own. You are verifying, not reviewing.

Write your verdicts to OUTPUT_PATH.
</task>

<inputs>
Findings to verify: INPUT_FILES
Manuscript: PAPER_PATH
</inputs>

<output_format>
For each finding in the input files, one entry.
- Source finding: <Claude agent N, severity, location>
- Quote check: PASS / FAIL
- Issue check: CONFIRMED / REFUTED / DOWNGRADE
- Evidence: one sentence citing the paper line that supports the verdict.
- Original severity vs. recommended severity (if downgrade)
</output_format>

<action_safety>
Read PAPER_PATH and the files listed in INPUT_FILES. Write only to OUTPUT_PATH; do not edit the manuscript or the input files.
</action_safety>

<default_follow_through_policy>
Process every finding in the input files end-to-end. Do not ask clarifying questions mid-run.
</default_follow_through_policy>
```

### Cross-model quality checks

- [ ] For experimental manuscripts, `methods-reporting` invoked in audit mode and its 45-item checklist made the baseline for Agents 1, 2, 6, 7, and 8 on both teams. For conjoint, list-experiment, topic-modeling, text-classification, or VLM-OCR manuscripts, the sibling skill's checklist folded into Agent 9 on both teams.
- [ ] Codex sub-agents called via `Bash` following § "Codex invocation mechanism" (`codex exec ... < /dev/null`, `run_in_background: true`, `timeout: 600000`). Absolute paths used for `PAPER_PATH` and `OUTPUT_PATH` in the prompt.
- [ ] Agents 6 and 7 marked `NA` on both teams for non-experimental or non-preregistered manuscripts.
- [ ] All 4 Phase 3 cross-checks launched only after all 18 Phase 2 output files exist. Any Codex agent failure logged in the report rather than silently reducing coverage.
- [ ] Quote-failed findings dropped as hallucinations on the finder's side. Asymmetric, cross-refuted findings dropped unless the orchestrator re-read the manuscript and noted the override on the entry.
- [ ] Adjudication produces one entry per underlying issue, each retained Critical / Recommended issue carrying a confidence label and a file path with line number, or a section name.
- [ ] `.review-tmp/` deleted after the final report was delivered, unless the user asked to keep it.

## When to reach for `presubmit` instead

This skill covers most in-flow review needs. The heavier [`presubmit`](https://github.com/scdenney/presubmit) Python CLI runs ~30 stages and is the right tool when:

- You want **full adversarial pressure** — a dedicated Red Team whose personas (Breaker, Butcher, Shredder, Collector, Void) each attack the paper from a different angle, a Blue Team defence, separate numbers/fact-check/citation-verification cascades, and a legal pass; this skill compresses that into Agent 1 plus the two cross-checkers.
- You want a **standalone deliverable** — a single `report.txt` and optional editor's note, produced outside your Claude Code session. Useful when the review is the product: feedback to a co-author, a pre-print critique, or a final pass before external peer review.
- You want **resumability + cost tracking** — `presubmit` checkpoints every stage to disk; deleting a stage file forces that stage to re-run. Tracks per-stage API cost.
- You want a **math audit** — `presubmit` has an optional Mathpix-backed equation audit (`--math`); this skill doesn't.
- You want a **code-replication audit** — `presubmit` can ingest a replication archive and compare claims against the code (`--code`); this skill stops at the "does the archive look complete" question in Agent 9.

Trade-off: `presubmit` bills per-token against an Anthropic API key (separate from your Claude Code subscription). See `presubmit/README.md` for install, cost considerations, and known trade-offs vs. the upstream Gemini implementation.

| Mode | Adversarial depth | Cost | When |
|-------|-------------------|------|------|
| Default | Single-model, 11 agents, in-session verification cascade | Lightest | Fast in-flow review during writing |
| `--codex` | Cross-model, 18 agents plus 4 cross-checks, dual verification cascade | ~2× the calls of the default mode | Before submission, when you want maximum pressure and a second model family's blind spots |
| [`presubmit`](https://github.com/scdenney/presubmit) | ~30 stages, dedicated Red Team personas, Blue Team defence, math and code-replication audits, resumable, cost-tracked | Heaviest, separate Anthropic API key | The review is the deliverable. Co-author feedback, pre-print critique, final pre-submission pass. |
