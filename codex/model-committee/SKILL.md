---
name: model-committee
description: Run one consequential, contestable decision through a deliberative committee of GPT-6 Astra and Claude Opus 5, chaired by fable (default), astra, opus, or sol. Not for factual lookups, brainstorming, routine implementation, independent-coder reliability, or final professional judgment. Use when several options are defensible and the two model families should propose, critique, revise, and cross-rank under a predeclared rubric.
---

# Model Committee

Run a GPT-6 Astra member and a Claude Opus 5 member as a deliberating committee, then chair the result. Keep the line to `$model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`references/protocol.md`](references/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

## Pick the chair

One skill, four chairs. Use `$model-committee` with `chair: fable` (the default), `chair: astra`, `chair: opus`, or `chair: sol`. The Claude slash-command suffixes `-astra`, `-opus`, `-fable`, and `-sol` select these same rows; in Codex they are parameters, not additional skill names. Keep the protocol and the three rounds unchanged. Select the GPT member from the table before creating any member prompt.

| chair | GPT member | Claude member | Chair pin | Use |
|---|---|---|---|---|
| `fable` (default) | `gpt-6-astra`, `xhigh` | `claude-opus-5`, `high` | `claude-fable-5-1`, `high` | Fable synthesizes from outside both member models. |
| `astra` | `gpt-5.6-sol`, `xhigh` | `claude-opus-5`, `high` | `gpt-6-astra`, `xhigh` | Astra chairs; Sol supplies the GPT member's deliberation. |
| `opus` | `gpt-6-astra`, `xhigh` | `claude-opus-5`, `high` | `claude-opus-5`, `high` | Retains the cheaper in-session option where Opus is already running; it shares the Claude member's model. |
| `sol` | `gpt-5.6-terra`, `xhigh` | `claude-opus-5`, `high` | `gpt-5.6-sol`, `xhigh` | Legacy Sol chair with a distinct GPT member tier. |

Default to Fable when no chair is named. Fable and Astra provide chairs distinct from both member models; Opus is the explicit same-model exception. No chair adds a third vote. Separate models or tiers do not establish statistical independence.

Score aggregation and the tie rule are mechanical whoever chairs; schema validation and compatible-component synthesis carry the chair's own judgment, which is what the choice of chair buys.

## Gate the workflow

Run only when the user invokes `$model-committee` or asks for these models to deliberate. Six external calls (seven with a delegated chair) draw plan credits or API spend on both providers — surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call no model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers.
3. Precommit the evaluation criteria, weights, and tie rule.
4. Confirm the chair.

## Sandbox constraint — read before the first call

The drivers launch separate CLI processes. Check actual sandbox, network, and authentication access. Restricted parents have blocked nested Codex initialization or Claude networking in earlier runs; approval `never` and headless execution alone do not establish that restriction. A child cannot bypass its parent's sandbox. Use existing authorization; request escalation only if supported and needed. If a member cannot run, report the error and do not simulate its response.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

`--check` only confirms the CLI is installed and prints its version. It does not verify that the pinned model or effort level is available to this account, so treat a passing check as necessary, not sufficient.

The model IDs in the chair table are explicit, but are not necessarily immutable snapshots, and they hold for every chair value. If one is unavailable, report it and ask whether to stop or use a named replacement — never substitute silently. This preflight is fail-closed: if either `--check` fails, do not start the committee and do not simulate a member's response.

## Run the committee

Create a new per-run working directory such as `.committee-tmp/<unique-run-id>/`; preserve existing runs. Follow the protocol's prompt contracts and produce these artifacts:

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
  --prompt-file <prompt.md> --out <output.md> --model gpt-6-astra --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --model claude-opus-5 --effort high -C <working-directory>
```

For `chair: astra`, pass `--model gpt-5.6-sol` on every GPT member call; for `chair: sol`, pass `--model gpt-5.6-terra`.

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair without becoming a third debater

Chair after round 3. Chair directly only when current runtime metadata verifies both the selected chair model and its specified effort. In Codex this can be Astra or Sol; an Astra lead using another effort keeps that setting and delegates the chair step at `xhigh`. A skill must not claim it changed the running model or effort. Otherwise bundle the brief and all round outputs into `chair.prompt.md`, then delegate the selected row:

```bash
# Default Fable chair; Opus uses --model claude-opus-5 with the same effort.
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-fable-5-1 --effort high -C <working-directory>

# Astra chair; the legacy Sol chair uses --model gpt-5.6-sol.
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model gpt-6-astra --effort xhigh -C <working-directory>
```

Either way, chairing is procedural: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

For every chair, check the arithmetic against the round-3 score tables and confirm that the decision follows the precommitted rule before delivering.

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
