---
name: model-committee-fable
description: Run a deliberative two-model committee between GPT-5.6 "Sol" and Claude Opus 5, chaired by Fable 5. Same two deliberating members as model-committee; the difference is the chair — Fable 5 aggregates the scores, applies the tie rule, and synthesizes the decision, so a lightweight, fast Claude-family chair handles the tally and synthesis while the heavier reasoning stays with the two members. Use when the user needs one consequential decision from multiple defensible options and wants a Fable-chaired deliberation. Suitable for architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability, open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
argument-hint: "[decision or problem for GPT-5.6 Sol and Opus 5 to deliberate, Fable 5 to chair]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Model Committee (Fable-chaired)

Run GPT-5.6 "Sol" and Claude Opus 5 as a deliberating committee with **Fable 5 as the chair**. Keep the line to `model-council-voting` sharp: a council measures independent disagreement, while this committee deliberately exposes each member to the other's argument and returns one decision.

Read [`reference/protocol.md`](reference/protocol.md) completely before running a committee. It carries the use-case gate, the brief template, the three round contracts, the decision rule, and the `decision.md` schema.

Fable chairs here because the heavy reasoning is already spent inside the members' three rounds and what remains is mostly mechanical — a lean chair is a deliberate cost choice, and being neither member it cannot vote its own prior a third time. Siblings: [`model-committee`](../model-committee/SKILL.md) (Opus 5 chairs) and [`model-committee-sol`](../model-committee-sol/SKILL.md) (GPT-5.6 "Sol" chairs, with the GPT member dropped to `gpt-5.6-terra` so the chair is not also a member).

## Gate the workflow

Run only when the user invokes `/model-committee-fable` or asks for a Fable-chaired Sol / Opus deliberation. The external calls draw plan credits or API spend on both providers — surface that and get confirmation unless the user has already accepted it. Apply the protocol's use-case gate first; if the task does not qualify, name the right alternative and call no model.

Before the first call:

1. Confirm the decision that must be returned.
2. Confirm the material may be sent to both providers.
3. Precommit the evaluation criteria, weights, and tie rule.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default pins:

- GPT member: `gpt-5.6-sol` (reasoning effort: `xhigh`)
- Claude member: `claude-opus-5` (reasoning effort: `high`)
- Chair: `claude-fable-5` (Fable 5)

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
chair.prompt.md             decision.md
```

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort xhigh -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> --effort high -C <working-directory>
```

Launch both calls in a round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived — otherwise round 1 stops being blind.

## Chair with Fable, without becoming a third debater

Inside a Fable session, chair directly. Otherwise delegate **only** the post-round-3 chair step, bundling the brief and all round outputs into `chair.prompt.md` under the protocol's decision-rule and output contracts:

```bash
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-fable-5 -C <working-directory>
```

Chairing is procedural: validate the round outputs against the protocol's schemas, aggregate the predeclared weighted scores, apply the precommitted tie rule, and synthesize only components both revisions explicitly marked compatible. Never introduce a new substantive option, and never break a tie by confidence, eloquence, or model identity. If the evidence stays genuinely unresolved, return the exact fork to the user; a forced but unsupported answer is not committee consensus.

A lean chair is likelier to defer where it should synthesize, so check its arithmetic against the round-3 score tables and confirm the decision matches the precommitted rule before delivering — the mechanical steps are exactly where a lightweight chair needs verifying.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule (note that Fable 5 chaired);
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user wants the full transcript kept. Implement only once the decision is accepted.
