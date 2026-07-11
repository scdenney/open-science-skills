<p align="center">
  <img src="https://img.shields.io/badge/OpenAI_Codex-37_open--science_skills-111111?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Codex — 37 open-science skills">
</p>

# Codex skills

This directory contains 37 Codex-native Open Science Skills. They mirror the Claude Code library with three intentional differences:

- `presubmit` is omitted.
- `opus-orchestrate` is omitted: it depends on Claude Code's ultracode Workflow orchestration, which has no Codex equivalent.
- [`46-orchestrate`](46-orchestrate/SKILL.md) replaces `fable-orchestrate` and is designed for a GPT-5.6 lead — `gpt-5.6-terra` by default for token economy, `gpt-5.6-sol` for intensive focus.

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
| Writing and reporting | [`hypothesis-building`](hypothesis-building/SKILL.md), [`literature-review`](literature-review/SKILL.md), [`methods-reporting`](methods-reporting/SKILL.md), [`narrative-building`](narrative-building/SKILL.md), [`paper-tex`](paper-tex/SKILL.md), [`pre-registration-writing`](pre-registration-writing/SKILL.md) |
| Figures and tables | [`figure-table-audit`](figure-table-audit/SKILL.md), [`figures`](figures/SKILL.md), [`tables`](tables/SKILL.md) |
| Manuscript QA | [`citation-check`](citation-check/SKILL.md), [`fact-check`](fact-check/SKILL.md), [`fair-check`](fair-check/SKILL.md), [`replication-package`](replication-package/SKILL.md) |
| Review and submission | [`journal-review`](journal-review/SKILL.md), [`paper-review-lite`](paper-review-lite/SKILL.md), [`paper-review-lite-codex`](paper-review-lite-codex/SKILL.md) |

## Variant notes

**`$model-committee` and its chairs.** The committee runs the exact GPT-5.5 and Claude Opus 4.8 members through their read-only CLIs, after first checking that deliberation is the right instrument for the task. It is the **Opus-chaired** member of a three-variant family: `$model-committee-sol` and `$model-committee-fable` deliberate the same two members but hand the post-round-3 tally and compatible-component synthesis to a chair that is not a member, GPT-5.6 "Sol" or Fable 5. Under Codex, `$model-committee-sol` chairs natively with Sol, while `$model-committee-fable` delegates the chair step to Fable 5 through the bundled `claude-member.sh`.

Sandbox constraint: all three variants' `codex-member.sh` (GPT-5.5) needs an unsandboxed or escalated call under a live Codex session, since a nested `codex exec` under sandbox fails structurally (see each `SKILL.md`). `claude-member.sh` was observed to hang under sandbox for the same reason (network access), less rigorously confirmed.

**`$diverge-codex`** uses a fresh Codex subagent context. It does not claim a second model family.

**`$paper-review-lite-codex`** keeps cross-model review by using Codex as lead and Claude Code's `claude -p` interface as the independent peer. It discloses and confirms external-credit use before running. Under sandbox, a `claude -p` call was observed to hang rather than complete (network access restricted); see the `SKILL.md` before assuming a stalled call will resolve on its own.

**`$46-orchestrate`** is explicit-invocation only, because it fans work out to subagents. Model/effort calibration (2026-07-11): subagents inherit the lead's model and effort unconditionally — re-verified on v0.144.1, the newest published release; the override fields existed around v0.137 but current releases hide them from the schema and v2 forks reject them (openai/codex#31814, #20077, #26363). The skill therefore prescribes a `gpt-5.6-terra` lead at `medium` effort as the default (the whole spawn tree becomes Terra), with escalated out-of-band one-shots for cross-tier work: `gpt-5.6-sol` at `xhigh` for the hardest compact problems, `gpt-5.6-luna` at `low` for cheap bulk. Rule of thumb: escalate effort before tier. It routes by role, risk, and verifiability, and spawns subagents with Codex's **native, in-process `spawn_agent` tool** (feature `multi_agent`, stable), confirmed working end-to-end in July 2026: two implementer subagents plus a verifier completed a real task on both hosts this repo runs on. An earlier design instead shelled out to a nested `codex exec` per subagent (`scripts/codex-worker.sh`, now removed) to pin each subagent to a cheaper `gpt-5.6` tier. That approach is broken rather than merely buggy: a `codex exec` process under any sandbox mode cannot spawn a working nested `codex exec` child (reproduced on macOS and Linux, different OS-level errors but the same cause, since an OS sandbox applies to the whole process tree). `spawn_agent` avoids this by running in-process, but it exposes **no `model` or `effort` parameter** (confirmed empirically), so every subagent runs at the lead's own model and effort; there is no `fable-orchestrate`-style cost tiering. The saving is context isolation and parallelism, short task-scoped subagent contexts instead of one continuously growing lead context, within a 4-slot concurrency limit (including the lead) that the tool itself declares.

**`$advisor`** is a single-turn independent second-reviewer consult with GPT-5.6: `gpt-5.6-terra` (balanced tier) by default, or `gpt-5.6-sol` (flagship tier) via `--model gpt-5.6-sol` for a stronger, costlier review, confirmed working (some ChatGPT-account Codex auth setups have rejected `sol` in the past, so confirm on your own account). The caller reads its effort level from its own session banner and passes it explicitly, since Codex has no inheritable effort environment variable the way Claude Code does. Read-only; never edits files. It **needs an unsandboxed or escalated call** under a live Codex session, because `sol-advisor.sh` shells out to a nested `codex exec` that fails under any sandbox mode (see the `SKILL.md`). The Claude-side `advisor` is the companion: it consults Fable 5 and reads effort from `$CLAUDE_EFFORT` automatically.
