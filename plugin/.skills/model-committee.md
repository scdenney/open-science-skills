---
name: model-committee
description: Runs a deliberative two-model committee — GPT-5.6 Sol and Claude Opus 5 as members, under a selectable chair. Chair defaults to Claude Opus 5; `/model-committee-fable` chairs with Fable 5.1, and `/model-committee-sol` chairs with GPT-5.6 Sol via Codex, which also drops the GPT member to Terra so the chair is not also a member. Use when one consequential decision must come out of several defensible options and the two model families should propose independently, critique each other, revise, and cross-rank under a predeclared rubric before converging. Fits architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, plan reconciliation, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability (use model-council-voting), open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
argument-hint: "[decision or problem for the committee to deliberate; optionally name the chair]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Model Committee

Run GPT-5.6 and Claude Opus 5 as a deliberating committee under a chair that is chosen per run. Keep the line to `model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`reference/protocol.md`](reference/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

## Pick the chair

The chair is a parameter, not a separate workflow. Three slash commands select it; the protocol, the drivers, and all three rounds are identical whichever chair runs, with exactly one exception the table below states — under a Sol chair the GPT member drops to Terra.

| Chair | Invoked by | Chair pin | Chair effort | GPT member | Chair invocation |
| --- | --- | --- | --- | --- | --- |
| Opus 5 (default) | `/model-committee` | `claude-opus-5` | `high` | `gpt-5.6-sol` | `claude-member.sh --model claude-opus-5 --effort high` |
| Fable 5.1 | `/model-committee-fable` | `claude-fable-5-1` | `high` | `gpt-5.6-sol` | `claude-member.sh --model claude-fable-5-1 --effort high` |
| Sol | `/model-committee-sol` | `gpt-5.6-sol` | `xhigh` | `gpt-5.6-terra` | `codex-member.sh --model gpt-5.6-sol --effort xhigh` |

If the user did not name a chair, use Opus 5.

Score aggregation and the tie rule are mechanical whoever chairs; schema validation and compatible-component synthesis carry the chair's own judgment, which is what the choice of chair buys.

- **Opus 5** is normally the model already running in-session, so the chair step usually costs no extra external call. Its cost is dependence: the chair is the *same model* as the Claude member, which is precisely why it must not vote a third time.
- **Fable 5.1** is a deliberate cost choice. The heavy reasoning is already spent inside the members' three rounds and what remains is mostly mechanical, and being neither member it cannot vote its own prior a third time. A lean chair is likelier to defer where it should synthesize, so its arithmetic needs checking (below).
- **Sol** is cross-family to the Opus member and a distinct 5.6 tier from the Terra member, so of the three chairs it is the least entangled with the Claude-family member's reasoning. It is *not* independent of the GPT-family member. Under a Sol chair the GPT member drops to `gpt-5.6-terra` — the *balanced* 5.6 tier — because a chair identical to a member would defeat the point. This is the one case where two things change at once: the chair and the GPT member's tier.

## Gate the workflow

Run only when the user invokes one of the three commands or asks for the two model families to deliberate. Six external member calls draw plan credits or API spend on both providers — seven when the chair step is delegated rather than run in-session. Surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call no model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers — under a Sol chair, the chair step is an external call too.
3. Precommit the evaluation criteria, weights, and tie rule.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default member pins:

- GPT member: `gpt-5.6-sol` (reasoning effort: `xhigh`) — `gpt-5.6-terra` under a Sol chair, per the table above
- Claude member: `claude-opus-5` (reasoning effort: `high`)

These are exact pins, not moving aliases. `--check` above only confirms the CLI is installed; whether a specific pin such as `gpt-5.6-sol` or `claude-fable-5-1` is actually available surfaces on the first real call, not at preflight — the chair pin in particular is untested until the chair step runs. If a pin is unavailable, report it and ask whether to stop or use a named replacement — never substitute silently. If `gpt-5.6-sol` is missing on this machine, stop and ask rather than falling back to `gpt-5.6-terra` for the chair.

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

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort high -C <working-directory>
```

Under a Sol chair, pass `--model gpt-5.6-terra` on the GPT member calls so the member does not run on the chair's pin.

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair without becoming a third debater

Chair in-session only when the session is verifiably running the chair model; otherwise delegate. Verify rather than assume: Claude Code injects a line into every session's context naming the model actually running (e.g. "You are powered by the model named …"); read it before picking a branch. This is fail-closed — if the running model is not the selected chair, or you cannot confirm it, take the delegate branch and do not label the output as chaired by that model. The failure is not hypothetical: a sibling orchestration skill (`orchestrate`, then named `fable-orchestrate`) recorded benchmark runs as one model that had silently executed under another, because nothing checked.

- Opus 5 chair, session verified as Opus 5: chair directly at `/effort` high. Aggregation and the tie rule are mechanical, but the compatible-component synthesis and the escalate-or-synthesize call are where the effort earns its cost.
- Fable 5.1 chair, session verified as Fable 5.1: chair directly at `/effort` high.
- Sol chair: always delegate. This SKILL.md loads inside Claude Code, so the session is never Sol.
- Any other case: delegate.

Delegation covers **only** the post-round-3 chair step — the members stay at their own pins. Bundle the brief and all round outputs into `chair.prompt.md` under the protocol's decision-rule and output contracts, then run the chair invocation from the table:

```bash
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-opus-5 --effort high -C <working-directory>

# Fable chair: --model claude-fable-5-1 --effort high
# Sol chair:   "$SKILL_DIR/scripts/codex-member.sh" \
#                --prompt-file chair.prompt.md --out decision.md --model gpt-5.6-sol --effort xhigh -C <working-directory>
```

The Codex plugin's result-handling guidance (stop after presenting review findings, change nothing) applies to code-review handoffs, not to the Codex member or the Sol chair here: the chair step below is instructed to aggregate and synthesize per the protocol, and its output is a decision record, not an applied change.

Chairing is procedural: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity — under the default chair, the chair being the same model as the Claude member is precisely why it must not vote a third time. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

Delegating the chair does not delegate the process. Check the chair's arithmetic against the round-3 score tables and confirm the decision matches the precommitted rule before delivering — with a lean chair such as Fable, this check is the backstop, since the mechanical steps are exactly where a lightweight chair needs verifying.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule (name which model chaired);
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user wants the full transcript kept. Implement only once the decision is accepted.
