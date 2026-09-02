---
name: diverge
description: Generate 3-5 conceptually distinct approaches labeled by creativity dimension (Novel, Surprising, Diverse, Conventional) and hold for selection instead of implementing the first idea; the --codex mode runs the same brainstorm on GPT-5.6 Sol via codex exec, then has Codex implement the selected approach. Use when a task has more than one non-obvious solution — creative, architectural, or analytical work — and before committing to an approach; use --codex when a second model family should widen the range of approaches.
argument-hint: "[describe the task, problem, or design question to diverge on] [--codex]"
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

When the task itself is still underspecified (goal, constraints, success criteria unsettled), interview before diverging. For research tasks, `research-grill` resolves the decision tree the approaches must answer to; it descends from Matt Pocock's `grill-me` (see [`RECOMMENDED.md`](../../../RECOMMENDED.md)). Grilling settles the question, and diverge generates genuinely distinct answers to a settled one.

**Model.** The default mode makes no external model call: it runs in whatever model and reasoning effort the session is already using, not a fixed pin. `--codex` is the exception — it shells out to a genuinely separate model, pinned to `gpt-5.6-sol` at `xhigh` effort.

## Behavior

Given `$ARGUMENTS`:

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

With `--codex`, the specification above is unchanged — Codex generates the approaches instead of you, and implements the selected one. Running the brainstorm on a second model family widens the space of approaches beyond what one model proposes. You structure the prompt and present the results; you do not add approaches of your own.

### Invocation mechanism

Plain Claude Code has no native `codex:codex-rescue` subagent. Every "ask Codex" step means calling `codex exec` through the `Bash` tool (the same mechanism `paper-review-lite --codex` uses):

- **`--model gpt-5.6-sol -c model_reasoning_effort=xhigh`** — pins Codex explicitly rather than relying on `codex exec`'s own implicit default, which can drift upstream.
- **`< /dev/null`** — closes stdin. Without it, `codex exec` hangs on "Reading additional input from stdin…" even when the prompt is passed as a CLI argument. This is the single most common failure mode.
- **`--skip-git-repo-check`** so it runs regardless of git state, and **`--sandbox`** set per phase: `read-only` for brainstorming, `workspace-write` for implementation.
- **`timeout: 600000`** (10 min) on the Bash call as a backstop.

The result returns on stdout — read it directly from the Bash output. Treat a non-zero exit, or empty output, as a Codex failure: report it and offer to fall back to plain `/diverge` (Claude-only).

### Steps

1. **Take the task** from `$ARGUMENTS` with `--codex` stripped; if empty, ask the user what they want to solve. Step 1 above (one round of goal questions) still applies before delegating.

2. **Brainstorm via Codex**, substituting `TASK` with the user's request verbatim and adding none of your own implementation preferences:

   ```bash
   codex exec --model gpt-5.6-sol -c model_reasoning_effort=xhigh --sandbox read-only --skip-git-repo-check "$(cat <<'CODEXEOF'
   <brainstorm prompt template below, with TASK substituted>
   CODEXEOF
   )" < /dev/null
   ```

3. **Present the approaches** to the user verbatim — do not paraphrase, filter, or reorder them. Ask which to pursue, or whether to synthesize.

4. **Implement via Codex** only after selection, switching the sandbox to `workspace-write` and setting `-C` to the project directory. The Codex plugin's result-handling guidance (stop after presenting findings, apply nothing) applies to code-review handoffs, not here — this step runs only on an explicit user selection, which is the same consent that guidance exists to protect:

   ```bash
   codex exec --model gpt-5.6-sol -c model_reasoning_effort=xhigh --sandbox workspace-write --skip-git-repo-check -C "<project dir>" "$(cat <<'CODEXEOF'
   <implementation prompt template below, with TASK and SELECTED_APPROACH substituted>
   CODEXEOF
   )" < /dev/null
   ```

### Brainstorm prompt template

```xml
<task>
Before implementing, generate 3–5 conceptually distinct approaches to:

TASK

Label each approach:
  [Novel]       — different conceptual basis from the conventional solution
  [Surprising]  — violates the obvious assumption; not the first answer
  [Diverse]     — maximally different from the other options in this list
  [Conventional]— the expected path, for contrast

For each approach provide:
- Core mechanism (1 sentence)
- How it works and what makes it distinct (2–3 sentences)
- Main tradeoff (1 sentence)
</task>

<constraints>
At least one approach must be [Surprising].
At least one must be [Novel].
Approaches must differ in underlying mechanism, not just vocabulary.
Prioritize novelty and surprise over immediate quality.
</constraints>

<structured_output_contract>
Numbered list only. No preamble, no implementation code.
Format each: number, label, mechanism line, explanation, tradeoff line.
Present all approaches and stop.
</structured_output_contract>
```

### Implementation prompt template

```xml
<task>
Implement the following approach to: TASK

Selected approach: SELECTED_APPROACH

Implement it fully. Edit files in place where applicable.
</task>
```
