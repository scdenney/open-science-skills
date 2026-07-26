---
name: model-committee
description: Run a deliberative two-model committee between GPT-5.6 "Sol" and Claude Opus 5. Use when the user needs one consequential decision from multiple defensible options and wants the two model families to propose independently, inspect each other's reasoning, revise, cross-rank, and converge under a predeclared rubric. Suitable for architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability, open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
---

# Model Committee

Run GPT-5.6 "Sol" and Claude Opus 5 as a deliberating committee. Keep the line to `$model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`references/protocol.md`](references/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

The two sibling skills deliberate the same pairing and differ only in who chairs after round 3: [`model-committee-sol`](../model-committee-sol/SKILL.md) (GPT-5.6 "Sol" chairs, with the GPT member dropped to `gpt-5.6-terra` so the chair is not also a member) and [`model-committee-fable`](../model-committee-fable/SKILL.md) (Fable 5 chairs). Score aggregation and the tie rule are mechanical whoever chairs; schema validation and compatible-component synthesis carry the chair's own judgment, which is what the choice of variant buys.

## Gate the workflow

Run only when the user invokes `$model-committee` or asks for Sol and Opus to deliberate. Six external calls draw plan credits or API spend on both providers — surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call neither model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers.
3. Precommit the evaluation criteria, weights, and tie rule.

## Sandbox constraint — read before the first call

`scripts/codex-member.sh` shells out to a nested `codex exec` process. Confirmed by direct reproduction (July 2026, both hosts this repo runs on): a `codex exec` process running under **any** sandbox mode cannot spawn a working nested `codex exec` child — it fails immediately with `Error: failed to initialize in-process app-server client: Operation not permitted` (macOS) or `Read-only file system` (Linux). This is structural, since the OS sandbox applies transitively to the whole process tree, and bypass flags on the nested call do not fix it. Running non-interactively (`approval: never` in your own session banner), this call cannot succeed — report the failure rather than fabricating the GPT member's response yourself. If interactive, request escalation (`sandbox_permissions: require_escalated`) for that one call.

`scripts/claude-member.sh` shells out to `claude -p`, a different binary, so it does not hit the identical `codex exec` IPC failure — but under `workspace-write` sandbox its outbound network call was observed to hang rather than complete, network access being restricted by the sandbox. That observation is less rigorously isolated than the `codex-member.sh` one; treat a hanging `claude-member.sh` call the same way and escalate or move to an unsandboxed session.

## Preflight both members

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default pins:

- GPT member: `gpt-5.6-sol` (reasoning effort: `xhigh`)
- Claude member: `claude-opus-5` (reasoning effort: `high`)

These are exact pins, not moving aliases. If one is unavailable, report it and ask whether to stop or use a named replacement — never substitute silently.

## Run the committee

Create a temporary working directory such as `.committee-tmp/<slug>/`. Follow the protocol's prompt contracts and produce these artifacts:

```text
brief.md
round-1-gpt.prompt.md       round-1-gpt.md
round-1-opus.prompt.md      round-1-opus.md
round-2-gpt.prompt.md       round-2-gpt.md
round-2-opus.prompt.md      round-2-opus.md
round-3-gpt.prompt.md       round-3-gpt.md
round-3-opus.prompt.md      round-3-opus.md
decision.md
```

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort high -C <working-directory>
```

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair without becoming a third debater

Chair after round 3, procedurally: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity — chairing from a session that shares a family with one member is precisely why it must not vote a third time. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule;
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user wants the full transcript kept. Implement only once the decision is accepted.
