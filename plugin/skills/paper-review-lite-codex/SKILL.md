---
name: paper-review-lite-codex
description: Cross-model adversarial pre-submission audit. Claude and Codex independently apply the paper-review-lite specification, then each cross-checks the other's findings; surviving issues are annotated by confidence.
argument-hint: "[path to paper or describe manuscript to review]"
context: fork  # Claude Code: run skill in a forked subagent context (isolated from conversation history). See https://code.claude.com/docs/en/skills#frontmatter-reference
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
---

# Paper Pre-Submission Review (Lite, Cross-Model Adversarial)

This is the cross-model sibling of [`paper-review-lite`](../paper-review-lite/SKILL.md), itself the in-session, Claude-Code-native counterpart to [`presubmit`](https://github.com/scdenney/presubmit) (our port of the [reviewer2](https://github.com/isitcredible/reviewer2) adversarial peer-review pipeline). The heritage carries over wholesale. Sub-agents adopt a Critical-Reviewer posture, every finding is grounded in a verbatim quote, and a verification cascade filters hallucinations before they reach the final report.

The new mechanic is cross-model adversarial verification. Two reviewers — Claude (the orchestrator) and Codex (GPT-5.6 "Sol" at `xhigh` reasoning effort, invoked via Bash `codex exec`) — independently apply the same `paper-review-lite` specification to the same paper, then each plays Blue Team to the other's Red Team. Two model families have different blind spots, so both their agreements and their disagreements carry information. Phase 4 scores each combination.

Roughly 22 model calls total (9 Claude Red Team, 9 Codex Red Team, 4 cross-model Blue Team) plus orientation and synthesis by the orchestrator. Reach for it before submission when you want maximum adversarial pressure and a second model family's blind spots.

The Claude orchestrator is whatever model you are running — Opus 5 or Fable 5. It runs orientation, launches both Red Teams, spawns the cross-checkers, and adjudicates. The Codex peer is pinned to `gpt-5.6-sol` at `xhigh` reasoning effort (§ Codex invocation mechanism). On Opus, run at medium reasoning effort by default, raising to high for the Phase-4 cross-team adjudication and Editor's Note — a bounded judgment call, not the sustained orchestration role — and fan the 18 Phase-2 calls and 4 Phase-3 cross-checks out. If the `Workflow` tool is listed among your tools this session, express those calls as a `Workflow`; otherwise — the common case, since dynamic Workflows are gated per session by org policy, the launch gate, or the "Dynamic workflows" setting in `/config`, and invoking a skill does not grant them — launch each phase's agents with parallel `Agent` calls in a single message and start the next phase once their outputs land. The fallback is the default, not a degraded mode; branch on tool availability, not on which model is leading. The Codex-side calls are `Bash` invocations either way. See [`opus-orchestrate`](../opus-orchestrate/SKILL.md) / [`fable-orchestrate`](../fable-orchestrate/SKILL.md) for the routing and the decorrelated-peer rationale.

## Codex invocation mechanism

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

## Instructions

### 1. Orientation (orchestrator, before any review agent launches)

Run the orientation step from `paper-review-lite` § 1 verbatim. Read the paper yourself to determine source format (LaTeX, Pandoc, Word), SI location, figure paths, replication archive, bibliography format, and design family. Use this to write specific review prompts that name actual file paths and section names. Generic prompts produce shallow reviews from both model families.

For experimental manuscripts, also invoke `methods-reporting` in audit mode so its 45-item checklist becomes the baseline for Agents 1, 2, 6, 7, and 8 on both teams (matching `paper-review-lite` § 1). For conjoint, list-experiment, topic-modeling, LLM-classification, or VLM-OCR manuscripts, invoke the matching sibling skill and fold its checklist into Agent 9 on both teams.

### 2. Orchestration contract

Create this scratch layout in the paper's working directory.

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

### 3. Phase 2 — Dual independent Red Team (18 parallel calls)

Launch all 18 review calls in a single message.

- **9 Claude sub-agents** via the `Agent` tool (default `subagent_type`). Use the agent prompts from `paper-review-lite` § 2 (Agents 1–9) verbatim, but redirect output to `.review-tmp/claude/agent-N-*.md` instead of the original `.review-tmp/agent-N-*.md`. Also carry over that skill's per-agent model/effort pins rather than defaulting all nine to one model: Opus `high` for the argument-level dimensions (1, 2, 6, 7), Sonnet `medium` for the mechanical ones (3, 4, 5, 8, 9). The standalone `Agent` tool has no effort field — fold the effort instruction into the prompt text itself; only `agent()` inside a `Workflow` accepts `opts.effort`. See `paper-review-lite` § "Sub-agent model and effort assignment" for the full table and rationale.
- **9 Codex sub-agents** via the `Bash` tool, following the pattern in § Codex invocation mechanism. Use the Codex Phase 2 template below as the prompt body, one call per dimension. Output to `.review-tmp/codex/agent-N-*.md`.

Both teams apply the same dimension definitions, the same Critical-Reviewer posture, and the same severity rubric (`[CRITICAL]`, `[RECOMMENDED]`, `[MINOR]`) from `paper-review-lite` § 2. The point of running two model families on one specification is to compare independent applications of one standard, not to give them different jobs. Neither team sees the other's findings during Phase 2.

**One carve-out — Codex Agent 4 (DOI audit) has no web access.** The `codex exec` sandbox cannot perform the web searches that the Agent 4 prompt asks for. Tell Codex's Agent 4 to limit itself to offline checks (DOI present/absent, format validity, internal consistency with the entry) and to tag entries `NEEDS WEB VERIFICATION` instead of attempting lookups; live DOI resolution and missing-DOI searches are the Claude team's Agent 4's job (it has WebSearch/WebFetch).

Agents 6 (CONSORT) and 7 (pre-registration) are required for experimental manuscripts and marked `NA` for non-experimental ones on both teams.

### 4. Phase 3 — Cross-model adversarial verification (4 parallel calls)

Each model verifies the other's findings. Cross-checkers do not add new findings; that was Phase 2's job. They verify, refute, or downgrade.

**Claude cross-checks Codex (2 sub-agents via `Agent`).**

- Sub-agent A reads `.review-tmp/codex/agent-{1,2,6,7}-*.md` and the manuscript. Writes `.review-tmp/cross-check/claude-checks-codex-content.md`.
- Sub-agent B reads `.review-tmp/codex/agent-{3,4,5,8,9}-*.md` plus the manuscript, bibliography, and archive. Writes `.review-tmp/cross-check/claude-checks-codex-technical.md`.

For each Codex `[CRITICAL]` or `[RECOMMENDED]` finding, the cross-checker verifies the cited verbatim quote appears at the cited location, verifies the issue against the actual paper, flags any Codex finding that Claude also flagged independently in `.review-tmp/claude/` (mutual catch — note for synthesis), and steel-mans the paper. When the paper anticipates or partially addresses the concern, note it for severity downgrade.

**Codex cross-checks Claude (2 sub-agents via `Bash` following § Codex invocation mechanism).**

- Sub-agent C reads `.review-tmp/claude/agent-{1,2,6,7}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-content.md`.
- Sub-agent D reads `.review-tmp/claude/agent-{3,4,5,8,9}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-technical.md`.

Use the Codex Phase 3 template below. Same verification protocol.

### 5. Phase 4 — Adjudication and synthesis (orchestrator, direct)

Build the consolidated Pre-Submit Report by adjudicating across teams.

- **Mutual.** Both teams flagged it; both cross-checkers confirmed. Mark `[CRITICAL ✓✓]` or `[RECOMMENDED ✓✓]`. Highest-confidence findings.
- **Asymmetric, cross-confirmed.** One team flagged; the other team's cross-checker confirmed against the paper. Retain at original severity. Mark `[CRITICAL ✓]` or `[RECOMMENDED ✓]`. These often surface real but easy-to-miss problems.
- **Asymmetric, cross-refuted.** One team flagged; the other team's cross-checker refuted against the paper. Default action is to drop. The orchestrator can override by re-reading the manuscript directly, in which case retain at one tier below original severity with the note "single-team finding, cross-refuted, retained after orchestrator re-read at <file:line>".
- **Quote-failed.** The cross-checker could not find the cited verbatim span. Drop as hallucination on the finder's side.

Apply the synthesis rules from `paper-review-lite` § 4 in order. Deduplicate within-team first (multiple agents on the same team flagging the same underlying issue), then across-team (a mutual catch is one entry, not two), then demote self-conceded critiques (any finding whose own description includes language conceding the point). The report format is `paper-review-lite` § 4 exactly — single-line Recommendation at the top, then the Editor's Note (3–6 paragraph prose memo), then Critical / Recommended / Minor lists, then Strengths, then the Journal-Readiness Checklist, then "What Still Needs Your Input" — with one extra column on the Critical Issues and Recommended Changes tables.

```
| Severity | Confidence                                      | Location | Issue | Fix |
|----------|-------------------------------------------------|----------|-------|-----|
| CRITICAL | Mutual (Claude + Codex)                         | …        | …     | …   |
| CRITICAL | Asymmetric: Codex only, confirmed by Claude     | …        | …     | …   |
| CRITICAL | Asymmetric: Claude only, cross-refuted, retained after orchestrator re-read | … | … | … |
```

## Codex Phase 2 template (one per dimension, 9 total)

Use the XML block below as the prompt body inside the Bash invocation from § Codex invocation mechanism. Substitute `DIMENSION_INSTRUCTIONS` with the verbatim text of the corresponding agent from `paper-review-lite` § 2 (the full text of Agent 1, Agent 2, …, Agent 9 — do not paraphrase). Substitute `PAPER_PATH` with the absolute manuscript path and `OUTPUT_PATH` with the absolute path to the Codex agent's output file under `.review-tmp/codex/`.

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
- [CRITICAL] — blocks submission. Wrong numbers, broken references, missing ethics or data-availability statement when required, silent pre-registration deviation, anonymization failure, unreproducible main result.
- [RECOMMENDED] — will draw reviewer complaint. Unsupported claim, missing robustness check, undefined threshold, missing limitation, insufficient figure caption, undocumented exclusion.
- [MINOR] — polish. Style, typography, citation format, wording consistency.
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

## Codex Phase 3 template (cross-check Claude's findings)

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

## Quality Checks

- [ ] For experimental manuscripts, `methods-reporting` invoked in audit mode and its 45-item checklist made the baseline for Agents 1, 2, 6, 7, and 8 on both teams. For conjoint, list-experiment, topic-modeling, text-classification, or VLM-OCR manuscripts, the sibling skill's checklist folded into Agent 9 on both teams.
- [ ] Codex sub-agents called via `Bash` following § Codex invocation mechanism (`codex exec ... < /dev/null`, `run_in_background: true`, `timeout: 600000`). Absolute paths used for `PAPER_PATH` and `OUTPUT_PATH` in the prompt.
- [ ] Agents 6 and 7 marked `NA` on both teams for non-experimental or non-preregistered manuscripts.
- [ ] All 4 Phase 3 cross-checks launched only after all 18 Phase 2 output files exist. Any Codex agent failure logged in the report rather than silently reducing coverage.
- [ ] Quote-failed findings dropped as hallucinations on the finder's side. Asymmetric, cross-refuted findings dropped unless the orchestrator re-read the manuscript and noted the override on the entry.
- [ ] Adjudication produces one entry per underlying issue, each retained Critical / Recommended issue carrying a confidence label and a file path with line number, or a section name.
- [ ] `.review-tmp/` deleted after the final report was delivered, unless the user asked to keep it.

## When to reach for this skill vs. siblings

| Skill | Adversarial depth | Cost | When |
|-------|-------------------|------|------|
| `paper-review-lite` | Single-model, 11 agents, in-session verification cascade | Lightest | Fast in-flow review during writing |
| `paper-review-lite-codex` (this) | Cross-model, 18 agents plus 4 cross-checks, dual verification cascade | ~2× the calls of `paper-review-lite` | Before submission, when you want maximum pressure and a second model family's blind spots |
| [`presubmit`](https://github.com/scdenney/presubmit) | ~30 stages, dedicated Red Team personas, Blue Team defence, math and code-replication audits, resumable, cost-tracked | Heaviest, separate Anthropic API key | The review is the deliverable. Co-author feedback, pre-print critique, final pre-submission pass. |
