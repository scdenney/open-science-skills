---
name: diverge
description: Before implementing, generate 3-5 conceptually distinct approaches labeled by creativity dimension (Novel, Surprising, Diverse, Conventional), then hold for selection. Brainstorm-then-select to resist defaulting to the most obvious solution.
argument-hint: "[describe the task, problem, or design question to diverge on]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# Diverge

Interrupt the default path of jumping to the most probable — and least creative — solution.

## Heritage and scope

An original Open Science Skills workflow grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`reference/creative-preference-optimization.md`](reference/creative-preference-optimization.md)). Standard preference alignment (RLHF/DPO) optimizes for the most human-expected output, which is by construction the least surprising one. The paper's most accessible remedy — its own "brainstorm-then-select" baseline — needs no fine-tuning: force divergence before convergence, require that at least one approach is surprising and one is novel, and defer quality and implementation until after selection.

Use it wherever more than one non-obvious solution exists — creative, architectural, or analytical work — and not for rote tasks with one correct answer (fix this syntax error).

**Model.** No external model call: this runs in whatever model and reasoning effort the session is already using, not a fixed pin. The sibling `diverge-codex` differs by host. From Claude Code (`/oss:diverge-codex`) it shells out to a genuinely separate model, pinned to `gpt-5.6-sol` at `xhigh` effort. From the Codex CLI (`$diverge-codex`) it spawns a fresh same-family Codex subagent — a clean context, not a cross-model check — so it too runs at the session's own model and effort.

## Behavior

Given `$ARGUMENTS`:

### Step 1 — Clarify if needed

If the task is ambiguous about what "good" looks like, ask **one** focused question about the goal, not about implementation. Skip this if the goal is clear.

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
