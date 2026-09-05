---
disable-model-invocation: true
name: model-committee
description: Runs a deliberative two-model committee — GPT-6 Astra and Claude Opus 5 as members, under a selectable chair. Chair defaults to Fable 5.1; `/model-committee-astra` selects Astra with a Sol member, `/model-committee-opus` selects Opus, and `/model-committee-sol` retains the Sol chair with a Terra member. Use when one consequential decision must come out of several defensible options and the two model families should propose independently, critique each other, revise, and cross-rank under a predeclared rubric before converging. Fits architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, plan reconciliation, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability (use model-council-voting), open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
argument-hint: "[decision or problem for the committee to deliberate; optionally name the chair]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Model Committee

Run GPT-6 Astra and Claude Opus 5 as a deliberating committee under a chair that is chosen per run. Keep the line to `model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`reference/protocol.md`](reference/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

## Pick the chair

The chair is a parameter, not a separate workflow. Five slash commands select it; the protocol, the drivers, and all three rounds are identical whichever chair runs. A GPT-family chair uses a different GPT member tier. Fable and Astra are distinct from both member models; the explicitly selected Opus chair is the same-model exception. That is the only thing that changes between rows besides the chair itself.

| Chair | Invoked by | Chair pin | Chair effort | GPT member | Chair invocation |
| --- | --- | --- | --- | --- | --- |
| Fable 5.1 (default) | `/model-committee`, `/model-committee-fable` | `claude-fable-5-1` | `high` | `gpt-6-astra` | `claude-member.sh --model claude-fable-5-1 --effort high` |
| Opus 5 | `/model-committee-opus` | `claude-opus-5` | `high` | `gpt-6-astra` | `claude-member.sh --model claude-opus-5 --effort high` |
| Astra | `/model-committee-astra` | `gpt-6-astra` | `xhigh` | `gpt-5.6-sol` | `codex-member.sh --model gpt-6-astra --effort xhigh` |
| Sol | `/model-committee-sol` | `gpt-5.6-sol` | `xhigh` | `gpt-5.6-terra` | `codex-member.sh --model gpt-5.6-sol --effort xhigh` |

If the user did not name a chair, use Fable 5.1. The premier models orchestrate: a committee is chaired by a frontier model that sits outside both members, and the two premier chairs — Fable on the Claude side, Astra on the GPT side — are the ones to reach for on a consequential call. `/model-committee-fable` is kept as an alias of the default so every earlier name still resolves.

Score aggregation and the tie rule are mechanical whoever chairs; schema validation and compatible-component synthesis carry the chair's own judgment, which is what the choice of chair buys.

- **Fable 5.1** (default) is the premier Claude model and is neither member, so it cannot vote its own prior a third time and it brings the strongest synthesis to the one step that needs judgment rather than arithmetic. Its cost is one external Fable call per committee, unless the session is verifiably running Fable already. Its arithmetic still needs checking (below) — a strong chair is not exempt from the mechanical audit.
- **Opus 5** is normally the model already running in-session, so the chair step usually costs no extra external call — that is the reason to choose it. Its cost is dependence: the chair is the *same model* as the Claude member, which is precisely why it must not vote a third time. Prefer it for a cheap committee on a decision that is consequential but not close.
- **Astra** is the premier GPT model chairing from outside the Claude-family member. Because a chair identical to a member would defeat the point, under an Astra chair the GPT member steps down one tier to `gpt-5.6-sol` — still near-frontier, so the GPT side of the deliberation stays strong. This is the GPT-side mirror of the Fable default, and the row to use when the deliberation should be adjudicated by the *other* vendor's premier model.
- **Sol** is cross-family to the Opus member and a distinct 5.6 tier from the Terra member. It is *not* independent of the GPT-family member. Under a Sol chair the GPT member uses `gpt-5.6-terra` — the *balanced* 5.6 tier. Kept for continuity now that Astra is the GPT flagship; prefer the Astra chair for new work.

## Gate the workflow

Run only when the user invokes one of the five commands or asks for the two model families to deliberate. Six external member calls draw plan credits or API spend on both providers — seven when the chair step is delegated rather than run in-session. Surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call no model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers — under an Astra or Sol chair, the chair step is an external Codex call too; under the default Fable chair it is an external Claude call unless the session is already Fable.
3. Precommit the evaluation criteria, weights, and tie rule.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default member pins:

- GPT member: `gpt-6-astra` (reasoning effort: `xhigh`) — `gpt-5.6-sol` under an Astra chair and `gpt-5.6-terra` under a Sol chair, per the table above
- Claude member: `claude-opus-5` (reasoning effort: `high`)

These are explicit model IDs; they are not necessarily immutable snapshots. `--check` above only confirms the CLI is installed; whether a specific pin such as `gpt-5.6-sol` or `claude-fable-5-1` is actually available surfaces on the first real call, not at preflight — the chair pin in particular is untested until the chair step runs. If a pin is unavailable, report it and ask whether to stop or use a named replacement — never substitute silently. If `gpt-5.6-sol` is missing on this machine, stop and ask rather than falling back to `gpt-5.6-terra` for the chair.

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

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort high -C <working-directory>
```

Under an Astra chair, pass `--model gpt-5.6-sol` on every GPT member call; under a Sol chair, pass `--model gpt-5.6-terra`.

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair without becoming a third debater

Chair in-session only when the session is verifiably running the chair model; otherwise delegate. Verify rather than assume: Claude Code injects a line into every session's context naming the model actually running (e.g. "You are powered by the model named …"); read it before picking a branch. This is fail-closed — if the running model is not the selected chair, or you cannot confirm it, take the delegate branch and do not label the output as chaired by that model. The failure is not hypothetical: a sibling orchestration skill (`orchestrate`, then named `fable-orchestrate`) recorded benchmark runs as one model that had silently executed under another, because nothing checked.

- Fable 5.1 chair (default), session verified as Fable 5.1: chair directly at `/effort` high. Aggregation and the tie rule are mechanical, but the compatible-component synthesis and the escalate-or-synthesize call are where the effort earns its cost.
- Opus 5 chair, session verified as Opus 5: chair directly at `/effort` high.
- Astra chair: always delegate. This SKILL.md loads inside Claude Code, so the session is never Astra.
- Sol chair: always delegate — the session is never Sol either.
- Any other case: delegate.

Delegation covers **only** the post-round-3 chair step — the members stay at their own pins. Bundle the brief and all round outputs into `chair.prompt.md` under the protocol's decision-rule and output contracts, then run the chair invocation from the table:

```bash
# Fable chair (default):
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-fable-5-1 --effort high -C <working-directory>

# Opus chair:  --model claude-opus-5 --effort high
# Astra chair: "$SKILL_DIR/scripts/codex-member.sh" \
#                --prompt-file chair.prompt.md --out decision.md --model gpt-6-astra --effort xhigh -C <working-directory>
# Sol chair:   "$SKILL_DIR/scripts/codex-member.sh" \
#                --prompt-file chair.prompt.md --out decision.md --model gpt-5.6-sol --effort xhigh -C <working-directory>
```

The Codex plugin's result-handling guidance (stop after presenting review findings, change nothing) applies to code-review handoffs, not to the Codex member or the Astra and Sol chairs here: the chair step below is instructed to aggregate and synthesize per the protocol, and its output is a decision record, not an applied change.

Chairing is procedural: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity — under the Opus chair, the chair being the same model as the Claude member is precisely why it must not vote a third time. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

Delegating the chair does not delegate the process. Check the chair's arithmetic against the round-3 score tables and confirm the decision matches the precommitted rule before delivering. Apply this check to every chair.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule (name which model chaired);
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user wants the full transcript kept. Implement only once the decision is accepted.
