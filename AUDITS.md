# Audits

## 2026-08-08 — full library audit and Opus 5 upgrade (v2.22.0)

Full best-practices audit and upgrade of every installed skill: 41 plugin + 39 codex + 13 personal
+ 4 thesis + 4 third-party + legacy Codex-home copies (~105 units). Twelve independent auditors —
ten Opus family batches, one Sonnet integrity matrix, one Codex (gpt-5.6-sol) self-audit of the
codex library — judged against three rubrics: Anthropic's skill authoring best practices (including
its MCP rules), OpenAI's Codex skills spec, and an Opus 5 compatibility lens (over-constraint,
stale model/tool mechanics, trigger-budget crowding, unverifiable harness claims). Findings:
4 critical / ~113 major / ~172 minor. Fixes landed via two worktree peers (plugin, codex), two
fixer agents (thesis, personal), and a lead pass; the orchestration-family diff was blind
cross-checked by Codex before merge (5 findings, all applied).

## What changed (this repo)

- **Committee collapse**: model-committee-fable/-sol were 71–78% drift-prone copies of
  model-committee (three maintenance passes had each landed in a subset). Now one chair-
  parameterized skill + three thin command wrappers. Counts: 41→39 Claude, 39→37 Codex.
- **False harness claims removed**: "invoking this skill satisfies the Workflow opt-in" (4 skills)
  — the gate is session-level and no skill can grant it; replaced with a check-then-branch on
  actual tool availability, with the Agent-fan-out fallback specified (no implicit stage barrier;
  effort pins soft in the fallback).
- **journal-review routing**: the Void→Fable "cheaper than Opus" premise was inverted (Fable 5 is
  2× Opus 5 per MTok); Void→Opus, explicit Fable→Opus→Sonnet→Haiku fallback ladder; Codex twin
  reworked for the 4-slot runtime (two finder waves).
- **list-experiment**: precision cost unified on the sourced figure — BCM 2020 p.1312 says ~14×
  (verified against the paper; the two April 2026 in-repo reviews recording ~10× were themselves
  wrong); sensitivity gate aligned to the paper's four conditions.
- **Verified-live paper-tex fixes**: SI cross-references rendered `??` (missing
  `\externaldocument` + missing third build pass); bib-less builds printed an empty BUILD FAILED
  (`.blg` never read). Both reproduced, fixed, re-verified with latexmk.
- **Private-path leaks** stripped from vlm-ocr-evaluation, model-council-voting,
  llm-calibration-logprobs (published plugin cited author-private files); empirical content kept.
- **Hub-spoke wiring**: vlm-ocr-pipeline now routes through the vlm-ocr-evaluation gate;
  text-classification names llm-calibration-logprobs and model-council-voting.
- **`${CLAUDE_PLUGIN_ROOT}` retired from skill bodies** (advisor, both orchestrators; thesis
  plugin as well): live-verified the variable is neither substituted into skill bodies nor
  exported to Bash. Replaced with deterministic newest-cache resolution
  (`ls -d …/oss/*/ | sort -V | tail -1`).
- **spawn**: the permission-mode self-read now covers all six modes, reads wide, and takes the
  last match (the first can be the reader's own echoed command).
- **Descriptions**: restored the "when to use" halves cut in 985a114; fable/opus-orchestrate now
  lead with the session-model discriminator; codex-side trimmed to 7,123 chars (under the ~8k
  selector budget) with negative scopes truncation-safe; codex reference/ → references/ (spec
  layout); codex advisor set explicit-invocation-only.
- **check.sh**: alias allowlist (commands may wrap a parameterized skill without their own dir).

Outside this repo, same effort: thesis plugin 0.2.0→0.3.1 (broken `_shared` resolution + an
orphaned 0.1.0 cache silently serving an older rubric contract; a transcription error in the MAIR
grade table corrected against the faculty source; source dir now git-tracked), personal skills
(sci-edit manuscript mode could not execute — allowed-tools lacked Bash; description was over the
1024 hard cap; prose-family trigger partition rebuilt), omarchy compliance (retired humanizer
removed; substack pair reconciled and de-macOS-ified), Codex install hygiene (~/.agents/skills
completed, legacy ~/.codex/skills shadow copies retired).

Evidence: `~/.claude/skill-audit/` (rubrics, per-batch findings JSON, decision memo, cross-check).
Frozen pre-audit copies of every skill: `~/.claude/skill-gauntlet/originals/`.
