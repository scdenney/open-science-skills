---
name: diverge
description: Generate 3-5 conceptually distinct approaches labeled by creativity dimension (Novel, Surprising, Diverse, Conventional) and hold for selection instead of implementing the first idea; the --codex mode delegates the brainstorm to a fresh Codex subagent for a clean, unanchored context and hands it the selected approach to implement. Use when a task has more than one non-obvious solution — creative, architectural, or analytical work — and before committing to an approach; use --codex when the user explicitly asks for a subagent, an independent context, or a delegated brainstorm.
---

# Diverge

Interrupt the default path of jumping to the most probable — and least creative — solution.

## Heritage and scope

An original Open Science Skills workflow grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`references/creative-preference-optimization.md`](references/creative-preference-optimization.md)). Standard preference alignment (RLHF/DPO) optimizes for the most human-expected output, which is by construction the least surprising one. The paper's most accessible remedy — its own "brainstorm-then-select" baseline — needs no fine-tuning: force divergence before convergence, require that at least one approach is surprising and one is novel, and defer quality and implementation until after selection.

Read the background note only when the user asks for the rationale or when refining the creativity criteria.

Use it wherever more than one non-obvious solution exists — creative, architectural, or analytical work — and not for rote tasks with one correct answer (fix this syntax error).

When the task itself is still underspecified (goal, constraints, success criteria unsettled), interview before diverging. For research tasks, `research-grill` resolves the decision tree the approaches must answer to; it descends from Matt Pocock's `grill-me` (see [`RECOMMENDED.md`](../../RECOMMENDED.md)). Grilling settles the question, and diverge generates genuinely distinct answers to a settled one.

**Model.** The default mode runs in the current session. For a demanding `--codex` brainstorm, use `gpt-6-astra` at `xhigh` for the fresh worker if the tool exposes model and effort overrides; pass a self-contained brief with `fork_turns="none"` where supported. Otherwise the worker inherits the lead, and the report must name that limitation. A routine brainstorm can retain the current model. A fresh context reduces anchoring but does not establish independent model-family evidence. Claude Code's `/oss:diverge --codex` explicitly launches Astra through the CLI.

## Behavior

Given the task supplied with the invocation:

### Step 1 — Clarify if needed

If the task is ambiguous about what "good" looks like, ask **one round** of goal questions — the frontier of what blocks generation now, numbered, each with your recommended answer; questions about the goal, never the implementation. One round, then generate: a task that needs a second round needs the full interview (`research-grill`, see Heritage), not this skill. Skip this entirely if the goal is clear.

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

## Codex mode (--codex)

A fresh subagent reduces anchoring from the lead agent's conversation history. The specification above is unchanged — the subagent generates the approaches and, after selection, implements the chosen one.

### Gate the delegation

Delegate only when the user explicitly passes `--codex` or asks for a subagent, an independent context, or a delegated brainstorm. If the skill was loaded implicitly without such a request, run the ordinary local workflow.

### Phase 1: brief the brainstormer

Extract the task, hard constraints, existing artifacts, and acceptance criteria. Spawn one fresh Codex subagent with only the task-local context it needs, withholding your own preferred solution or likely implementation. Give it this contract:

```text
Generate 3–5 conceptually distinct approaches to TASK. Do not implement.

Label every approach [Novel], [Surprising], [Diverse], or [Conventional].
Include at least one [Novel] and one [Surprising] approach. For each, provide:
1. Core mechanism — one sentence.
2. How it works and why it differs — two or three sentences.
3. Main tradeoff — one sentence.

Do not restate one idea with different vocabulary. Return only the approaches.
```

### Phase 2: present and pause

Check that the response contains 3–5 mechanically distinct approaches and satisfies the required labels. If it does not, send one focused correction to the same subagent.

Present the approaches without silently ranking, filtering, or rewriting them. Ask the user to select one approach or request a compatible synthesis. Stop before implementation.

### Phase 3: implement after selection

Send the selected approach, original task, constraints, and acceptance checks back to the same subagent when possible. Require it to implement the user's selected mechanism rather than substituting another, preserve unrelated user changes, run proportionate checks, and return changed files, verification evidence, and any residual risk.

The lead agent owns integration. Inspect the resulting diff and verification output, fix integration defects, and report the final outcome.

Codex-plugin result-handling guidance (stop after presenting review findings) applies to code-review handoffs, not here: Phase 3 begins only after the user has selected an approach, and the selected approach is meant to be implemented and integrated, not merely reported.

### Fallbacks

- If subagents are unavailable, state that the independent-context path is unavailable and run the local workflow.
- If the brainstorm subagent fails or returns empty output, retry once with a shorter brief, then fall back locally.
- If the selected approaches cannot be combined without changing the requested behavior, explain the incompatibility before proposing a hybrid.
