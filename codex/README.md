<p align="center">
  <img src="https://img.shields.io/badge/OpenAI_Codex-37_open--science_skills-111111?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Codex — 37 open-science skills">
</p>

# Codex skills

This directory contains 37 Codex-native Open Science Skills. They mirror the Claude Code library with three intentional differences:

- `presubmit` is omitted.
- `opus-orchestrate` is omitted because it depends on Claude Code's `Workflow` tool for dynamic multi-agent orchestration, which has no Codex equivalent.
- [`46-orchestrate`](46-orchestrate/SKILL.md) replaces `fable-orchestrate`. `gpt-5.6-sol` at xhigh effort owns orchestration, routing bounded work to Terra and reserving Luna for tightly specified mechanical work.

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
| Orchestration | [`46-orchestrate`](46-orchestrate/SKILL.md), [`advisor`](advisor/SKILL.md), [`spawn`](spawn/SKILL.md) |
| Ideation | [`diverge`](diverge/SKILL.md), [`diverge-codex`](diverge-codex/SKILL.md) |
| Research design | [`conjoint-cleaning`](conjoint-cleaning/SKILL.md), [`conjoint-design`](conjoint-design/SKILL.md), [`conjoint-diagnostics`](conjoint-diagnostics/SKILL.md), [`cross-national-design`](cross-national-design/SKILL.md), [`list-experiment`](list-experiment/SKILL.md), [`research-wayfinder`](research-wayfinder/SKILL.md), [`survey-design`](survey-design/SKILL.md) |
| Analysis | [`llm-calibration-logprobs`](llm-calibration-logprobs/SKILL.md), [`model-committee`](model-committee/SKILL.md), [`model-council-voting`](model-council-voting/SKILL.md), [`text-classification`](text-classification/SKILL.md), [`topic-modeling`](topic-modeling/SKILL.md) |
| Corpus processing | [`post-ocr-cleanup`](post-ocr-cleanup/SKILL.md), [`vlm-ocr-evaluation`](vlm-ocr-evaluation/SKILL.md), [`vlm-ocr-pipeline`](vlm-ocr-pipeline/SKILL.md) |
| Writing and reporting | [`hypothesis-building`](hypothesis-building/SKILL.md), [`literature-review`](literature-review/SKILL.md), [`methods-reporting`](methods-reporting/SKILL.md), [`narrative-building`](narrative-building/SKILL.md), [`paper-tex`](paper-tex/SKILL.md), [`pre-registration-writing`](pre-registration-writing/SKILL.md) |
| Figures and tables | [`figure-table-audit`](figure-table-audit/SKILL.md), [`figures`](figures/SKILL.md), [`tables`](tables/SKILL.md) |
| Manuscript QA | [`citation-check`](citation-check/SKILL.md), [`fact-check`](fact-check/SKILL.md), [`fair-check`](fair-check/SKILL.md), [`replication-package`](replication-package/SKILL.md) |
| Review and submission | [`journal-review`](journal-review/SKILL.md), [`paper-review-lite`](paper-review-lite/SKILL.md), [`paper-review-lite-codex`](paper-review-lite-codex/SKILL.md) |

## Variant notes

**`$model-committee` and its chairs.** The committee runs a GPT-5.6 member and Claude Opus 5 (high) as members through their read-only CLIs, after first checking that deliberation is the right instrument for the task. One skill carries all three chairs as a parameter — `opus` (default), `fable`, or `sol` — replacing the former `$model-committee-fable` and `$model-committee-sol`. Under `opus` and `fable` the GPT member is `gpt-5.6-sol` at xhigh; `fable` hands the post-round-3 tally and compatible-component synthesis to Fable 5 at `max` through the bundled `claude-member.sh`. The `sol` chair is the exception — since the chair is Sol, the GPT debater drops to `gpt-5.6-terra`, so the chair is never grading its own family's twin, and under a Codex/Sol session it chairs natively.

One sandbox constraint applies to every chair. `codex-member.sh` (GPT-5.6 Sol, or Terra under `chair: sol`) needs an unsandboxed or escalated call under a live Codex session, since a nested `codex exec` under sandbox fails structurally (see the `SKILL.md`). `claude-member.sh` was observed to hang under sandbox for the same reason (network access), less rigorously confirmed.

**`$diverge-codex`** uses a fresh Codex subagent context. It does not claim a second model family.

**`$paper-review-lite-codex`** keeps cross-model review by using Codex as lead and Claude Code's `claude -p` interface as the independent peer. It discloses and confirms external-credit use before running. Under sandbox, a `claude -p` call was observed to hang rather than complete, because network access is restricted. Read the `SKILL.md` before assuming a stalled call will resolve on its own.

**`$46-orchestrate`** is explicit-invocation only. Its default is a `gpt-5.6-sol` lead at `xhigh` effort, which its fail-closed preflight enforces. The lead owns decomposition, hard decisions, integration, and final verification. It delegates bounded, independently checkable work down to `gpt-5.6-terra` through explicit out-of-band one-shots. `gpt-5.6-luna` is reserved for fully specified mechanical work with objective checks. Do not use Ultra. Native in-process `spawn_agent` children inherit the lead's model and effort and cannot be assigned Terra or Luna, so they are useful only for live coordination or context isolation — not cost-tier routing. Nested cross-tier calls need an interactive or escalated parent session, and in headless mode the skill must not promise them.

**`$spawn`** drives full peer sessions through the herdr socket (`~/.config/herdr/herdr.sock`), which lives outside the workspace. Verified 2026-08-06 on the Codex CLI (gpt-5.6-sol): under `workspace-write` the socket connect fails with `PermissionDenied: Operation not permitted`. Under `danger-full-access`, `herdr status` connects and reports the server. A Codex lead therefore needs an explicitly authorized full-access session to spawn, or it prints the exact command sequence for the user to run in a normal shell. The skill's preflight gate encodes this, fail-closed. Explicit-invocation only.

**`$advisor`** is this library's single-turn, independent, read-only GPT-5.6 advisor. It always runs `gpt-5.6-sol` at `xhigh` (Extra high) effort, the flagship tier at its strongest routine setting, because the point of the consult is a stronger reviewer rather than a cheap one. It does not inherit the caller's effort and never uses Max/Ultra. The consult needs an unsandboxed or escalated live Codex session because it launches a nested `codex exec`. A headless session must report that the independent review is unavailable rather than silently self-reviewing.
