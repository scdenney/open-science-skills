---
name: model-committee
description: Run one consequential, contestable decision through a deliberative committee of GPT-5.6 and Claude Opus 5, chaired by opus (default), fable, or sol. Not for factual lookups, brainstorming, routine implementation, independent-coder reliability, or final professional judgment. Use when several options are defensible and the two model families should propose, critique, revise, and cross-rank under a predeclared rubric.
---

# Model Committee

Run a GPT-5.6 member and a Claude Opus 5 member as a deliberating committee, then chair the result. Keep the line to `$model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`references/protocol.md`](references/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

## Pick the chair

One skill, three chairs. The chair is a parameter, not a separate skill — the former `$model-committee-fable` and `$model-committee-sol` are now the `fable` and `sol` rows below. The protocol, the drivers, and all three rounds are identical whichever chair runs, with exactly one exception the table states: under a Sol chair the GPT member drops to Terra. Ask the user which chair they want if they did not say; default to `opus`.

| chair | GPT member | Claude member | Chair pin | Why this chair |
|---|---|---|---|---|
| `opus` (default) | `gpt-5.6-sol`, effort `xhigh` | `claude-opus-5`, effort `high` | the running session, or `claude-opus-5` at effort `high` | Strongest available synthesis. Shares a family with the Opus member, which is exactly why it must not vote a third time. |
| `fable` | `gpt-5.6-sol`, effort `xhigh` | `claude-opus-5`, effort `high` | `claude-fable-5`, effort `max`, through `claude-member.sh` | The heavy reasoning is already spent in the three rounds and what remains is mostly mechanical, so a lean chair is a deliberate cost choice. Being neither member, it cannot vote its own prior again. |
| `sol` | `gpt-5.6-terra`, effort `xhigh` | `claude-opus-5`, effort `high` | `gpt-5.6-sol`, effort `xhigh` — the running session under Codex/Sol, else through `codex-member.sh` | Sol is neither deliberating member: cross-family to the Opus member and a distinct 5.6 tier from the Terra member. |

Under `chair: sol` the GPT member drops to `gpt-5.6-terra`, the balanced 5.6 tier, precisely because the chair is Sol; a chair identical to a member defeats the point. Never fall back to `gpt-5.6-terra` for the chair itself for the same reason.

Score aggregation and the tie rule are mechanical whoever chairs; schema validation and compatible-component synthesis carry the chair's own judgment, which is what the choice of chair buys.

## Gate the workflow

Run only when the user invokes `$model-committee` or asks for these models to deliberate. Six external calls (seven with a delegated chair) draw plan credits or API spend on both providers — surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call no model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers.
3. Precommit the evaluation criteria, weights, and tie rule.
4. Confirm the chair.

## Sandbox constraint — read before the first call

`scripts/codex-member.sh` shells out to a nested `codex exec` process. Confirmed by direct reproduction (July 2026, both hosts this repo runs on): a `codex exec` process running under **any** sandbox mode cannot spawn a working nested `codex exec` child — it fails immediately with `Error: failed to initialize in-process app-server client: Operation not permitted` (macOS) or `Read-only file system` (Linux). This is structural, since the OS sandbox applies transitively to the whole process tree, and bypass flags on the nested call do not fix it. Running non-interactively (`approval: never` in your own session banner), this call cannot succeed — report the failure rather than fabricating the GPT member's response yourself. If interactive, request escalation (`sandbox_permissions: require_escalated`) for that one call.

`scripts/claude-member.sh` shells out to `claude -p`, a different binary, so it does not hit the identical `codex exec` IPC failure — but under `workspace-write` sandbox its outbound network call was observed to hang rather than complete, network access being restricted by the sandbox. That observation is less rigorously isolated than the `codex-member.sh` one; treat a hanging `claude-member.sh` call the same way and escalate or move to an unsandboxed session. Under `chair: fable` it carries both the Opus member and the Fable chair, so a hang blocks two of the three seats.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

`--check` only confirms the CLI is installed and prints its version. It does not verify that the pinned model or effort level is available to this account, so treat a passing check as necessary, not sufficient.

The pins in the chair table are exact, not moving aliases, and they hold for every chair value. If one is unavailable, report it and ask whether to stop or use a named replacement — never substitute silently. This preflight is fail-closed: if either `--check` fails, do not start the committee and do not simulate a member's response.

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
chair.prompt.md             decision.md
```

`chair.prompt.md` is written only when the chair is delegated rather than chaired by the running session.

Invoke each member through the bundled read-only driver, passing the GPT model the chair table names:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --model gpt-5.6-sol --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --model claude-opus-5 --effort high -C <working-directory>
```

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair without becoming a third debater

Chair after round 3. If the running session is the chair (`opus` in a Claude Opus 5 session, `sol` in a Codex/Sol session), chair directly. Otherwise bundle the brief and all round outputs into `chair.prompt.md` under the protocol's decision-rule and output contracts, then delegate that one step:

```bash
# chair: fable
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-fable-5 --effort max -C <working-directory>

# chair: sol, from outside a Sol session
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model gpt-5.6-sol --effort xhigh -C <working-directory>
```

Either way, chairing is procedural: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

Under `chair: fable`, check the chair's arithmetic against the round-3 score tables and confirm the decision matches the precommitted rule before delivering — a lean chair is likelier to defer where it should synthesize, and the mechanical steps are exactly where it needs verifying.

Codex-plugin result-handling guidance (stop after presenting review findings) applies to code-review handoffs, not here: in this skill the chair step is instructed to aggregate and decide per the protocol above.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision, decision rule, and which chair ran;
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user wants the full transcript kept. Implement only once the decision is accepted.
