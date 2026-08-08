---
name: diverge
description: Before implementing, generate 3-5 conceptually distinct approaches labeled by creativity dimension (Novel, Surprising, Diverse, Conventional), then hold for selection. Brainstorm-then-select to resist defaulting to the most obvious solution.
---

# Diverge

Interrupt the default path of jumping to the most probable — and least creative — solution.

## Heritage and scope

An original Open Science Skills workflow grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`references/creative-preference-optimization.md`](references/creative-preference-optimization.md)). Standard preference alignment (RLHF/DPO) optimizes for the most human-expected output, which is by construction the least surprising one. The paper's most accessible remedy — its own "brainstorm-then-select" baseline — needs no fine-tuning: force divergence before convergence, require that at least one approach is surprising and one is novel, and defer quality and implementation until after selection.

Use it wherever more than one non-obvious solution exists — creative, architectural, or analytical work — and not for rote tasks with one correct answer (fix this syntax error).

When the task itself is still underspecified (goal, constraints, success criteria unsettled), interview before diverging. Matt Pocock's `grill-me` (see [`RECOMMENDED.md`](../../RECOMMENDED.md)) resolves the decision tree the approaches must answer to. Grilling settles the question, and diverge generates genuinely distinct answers to a settled one.

**Model.** No separate model call: this runs in whatever model and reasoning effort the current Codex session is already using, not a fixed pin. `$diverge-codex` spawns a fresh subagent for a clean context, but that subagent is still Codex, at the same model and effort — it is not a cross-model pin. A genuinely separate, explicitly pinned model (`gpt-5.6-sol` at `xhigh`) only happens from the Claude Code side, via `/oss:diverge-codex`.

## Behavior

Given the task supplied with the invocation:

### Step 1 — Clarify if needed

If the task is ambiguous about what "good" looks like, ask **one round** of goal questions — the frontier of what blocks generation now, numbered, each with your recommended answer; questions about the goal, never the implementation. One round, then generate: a task that needs a second round needs the full interview (`grill-me`, see Heritage), not this skill. Skip this entirely if the goal is clear.

### Step 2 — Generate approaches

Produce **3–5 approaches** that differ in underlying mechanism, not surface vocabulary. At least one must be **[Surprising]** and at least one **[Novel]**. Label each with its primary creativity dimension:

- **[Novel]** — semantically far from the conventional solution; different conceptual basis
- **[Surprising]** — violates the obvious assumption about how this should work; would not be the first answer
- **[Diverse]** — maximally different from the other approaches in this list
- **[Conventional]** — the expected path, included as a reference point

For each approach provide:
1. Core mechanism — one sentence naming the key insight
2. How it works — two to three sentences on the mechanism and what makes it distinct
3. Main tradeoff — one sentence

No markdown header per approach — keep the list scannable.

### Step 3 — Hold

Do not implement. Present all approaches, then ask:

> "Which approach should I pursue? Or should I synthesize elements from multiple?"

## After selection

Implement the selected approach directly. If the user asks to synthesize, identify which elements are mechanically compatible and propose a brief hybrid plan before implementing.
