<p align="center">
  <img src="https://img.shields.io/badge/OpenAI_Codex-37_open--science_skills-111111?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Codex — 37 open-science skills">
</p>

# Codex skills

This directory contains 37 Codex-native Open Science Skills. They mirror the Claude Code library with three intentional differences:

- `presubmit` is omitted.
- `opus-orchestrate` is omitted: it depends on Claude Code's ultracode Workflow orchestration, which has no Codex equivalent.
- [`46-orchestrate`](46-orchestrate/SKILL.md) replaces `fable-orchestrate` and is designed for 4.6 “Sol” as the lead.

Every skill is a self-contained directory with `SKILL.md`, `agents/openai.yaml`, and only the references, scripts, or assets it needs. Codex supports these skills in the CLI, IDE extension, and app.

## Install

From the repository root, symlink all skills for the current user:

```bash
mkdir -p "$HOME/.agents/skills"
for skill in "$PWD"/codex/*/; do
  ln -sfn "${skill%/}" "$HOME/.agents/skills/$(basename "$skill")"
done
```

For one repository only, replace `$HOME/.agents/skills` with `<repo>/.agents/skills`. Install one skill by linking or copying only its directory:

```bash
mkdir -p "$HOME/.agents/skills"
ln -sfn "$PWD/codex/citation-check" "$HOME/.agents/skills/citation-check"
```

Invoke a skill as `$citation-check`, `$survey-design`, or another `$skill-name`. Codex can also load most skills implicitly from the task description. Restart Codex only if a new or changed skill does not appear automatically.

See the official [Codex skills documentation](https://developers.openai.com/codex/skills) for discovery scopes and invocation behavior.

## Catalog

| Area | Skills |
|---|---|
| Project setup | [`research-repo`](research-repo/SKILL.md) |
| Orchestration | [`46-orchestrate`](46-orchestrate/SKILL.md), [`advisor`](advisor/SKILL.md) |
| Ideation | [`diverge`](diverge/SKILL.md), [`diverge-codex`](diverge-codex/SKILL.md) |
| Research design | [`conjoint-cleaning`](conjoint-cleaning/SKILL.md), [`conjoint-design`](conjoint-design/SKILL.md), [`conjoint-diagnostics`](conjoint-diagnostics/SKILL.md), [`cross-national-design`](cross-national-design/SKILL.md), [`list-experiment`](list-experiment/SKILL.md), [`survey-design`](survey-design/SKILL.md) |
| Analysis | [`llm-calibration-logprobs`](llm-calibration-logprobs/SKILL.md), [`model-committee`](model-committee/SKILL.md), [`model-committee-fable`](model-committee-fable/SKILL.md), [`model-committee-sol`](model-committee-sol/SKILL.md), [`model-council-voting`](model-council-voting/SKILL.md), [`text-classification`](text-classification/SKILL.md), [`topic-modeling`](topic-modeling/SKILL.md) |
| Corpus processing | [`post-ocr-cleanup`](post-ocr-cleanup/SKILL.md), [`vlm-ocr-evaluation`](vlm-ocr-evaluation/SKILL.md), [`vlm-ocr-pipeline`](vlm-ocr-pipeline/SKILL.md) |
| Writing and reporting | [`hypothesis-building`](hypothesis-building/SKILL.md), [`literature-review`](literature-review/SKILL.md), [`methods-reporting`](methods-reporting/SKILL.md), [`narrative-building`](narrative-building/SKILL.md), [`pre-registration-writing`](pre-registration-writing/SKILL.md) |
| Figures and tables | [`figure-table-audit`](figure-table-audit/SKILL.md), [`figures`](figures/SKILL.md), [`tables`](tables/SKILL.md) |
| Manuscript QA | [`citation-check`](citation-check/SKILL.md), [`fact-check`](fact-check/SKILL.md), [`fair-check`](fair-check/SKILL.md), [`replication-package`](replication-package/SKILL.md) |
| Review and submission | [`journal-review`](journal-review/SKILL.md), [`paper-review-lite`](paper-review-lite/SKILL.md), [`paper-review-lite-codex`](paper-review-lite-codex/SKILL.md), [`paper-tex`](paper-tex/SKILL.md) |

## Variant notes

- `$model-committee` runs exact GPT-5.5 and Claude Opus 4.8 members through their read-only CLIs, after first checking that deliberation is the right instrument for the task. It is the **Opus-chaired** member of a three-variant family; `$model-committee-sol` and `$model-committee-fable` deliberate the same two members but hand the post-round-3 synthesis to GPT-5.6 “Sol” or Fable 5, so the chair (not one of the members) runs the tally and the compatible-component synthesis. Under Codex, `$model-committee-sol` chairs natively with Sol; `$model-committee-fable` delegates the chair step to Fable 5 through the bundled `claude-member.sh`.
- `$diverge-codex` uses a fresh Codex subagent context. It does not claim a second model family.
- `$paper-review-lite-codex` preserves cross-model review by using Codex as lead and Claude Code's documented `claude -p` interface as the independent peer. It discloses and confirms external credit use before running.
- `$46-orchestrate` is explicit-invocation only because it fans work out to subagents. It routes by role, risk, and verifiability, and pins each subagent to a GPT-5.6 tier and reasoning effort through the bundled `scripts/codex-worker.sh` — `gpt-5.6-luna` at `low` effort for fully-specified implementer work (the actual token-saving combination), `gpt-5.6-terra` at `medium` effort for analyst/verifier consults and as the default, and two parallel `terra` calls (swappable for `gpt-5.6-sol` at `high` effort) for the two-independent-check high-stakes path. The lead ("Sol") is the running Codex session itself and is never spawned via the script. All three tiers are confirmed working as of July 2026 (smoke-tested on both hosts this repo runs on) — the script always passes `-c model_reasoning_effort=` explicitly per call, since a subagent that omits it silently inherits the *caller's* config.toml default instead of its own tier-appropriate effort, which was found to defeat the cheap tier's purpose in practice.
- `$advisor` is a single-turn independent second-reviewer consult with GPT-5.6 — `gpt-5.6-terra` (balanced tier) by default for routine consults; `gpt-5.6-sol` (flagship tier) is confirmed working via `--model gpt-5.6-sol` for a stronger reviewer when the extra cost is worth it (some ChatGPT-account Codex auth setups have rejected `sol` in the past — confirm on your own account) — at an effort level the caller reads from its own session banner and passes explicitly (Codex has no inheritable effort environment variable the way Claude Code does). Read-only — never edits files. Companion to the Claude-side `advisor` skill, which consults Fable 5 instead and reads effort from `$CLAUDE_EFFORT` automatically.
