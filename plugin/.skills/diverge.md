---
disable-model-invocation: true
name: diverge
description: Generates 3-5 conceptually distinct approaches labeled Novel, Surprising, Diverse, or Conventional, and holds for the user's selection before implementing. The --codex mode runs the brainstorm on GPT-6 Astra via codex exec, then has Codex implement the selected approach. Use before committing to an approach when a creative, architectural, or analytical task has more than one non-obvious solution; use --codex when another model family should widen the range.
argument-hint: '[describe the task, problem, or design question to diverge on] [--codex]'
allowed-tools:
- Bash
- Read
- Write
- Edit
- AskUserQuestion
---

# Diverge

Interrupt the default path of jumping to the most probable — and least creative — solution.

Use a new output path or directory for each run; preserve earlier results and existing user edits.

## Heritage and scope

An original Open Science Skills workflow grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`reference/creative-preference-optimization.md`](reference/creative-preference-optimization.md)). Standard preference alignment (RLHF/DPO) optimizes for the most human-expected output, which is by construction the least surprising one. The paper's most accessible remedy — its own "brainstorm-then-select" baseline — needs no fine-tuning: force divergence before convergence, require that at least one approach is surprising and one is novel, and defer quality and implementation until after selection.

Use it wherever more than one non-obvious solution exists — creative, architectural, or analytical work — and not for rote tasks with one correct answer (fix this syntax error).

When the task itself is still underspecified (goal, constraints, success criteria unsettled), interview before diverging. For research tasks, `research-grill` resolves the decision tree the approaches must answer to; it descends from Matt Pocock's `grill-me` (see `RECOMMENDED.md` in the library repository). Grilling settles the question, and diverge generates genuinely distinct answers to a settled one.

**Model.** The default mode makes no external model call: it runs in whatever model and reasoning effort the session is already using, not a fixed pin. `--codex` is the exception — it shells out to a separate model family, pinned to `gpt-6-astra`: `high` effort for the brainstorm (a fresh-perspective consult whose output the user selects from) and `xhigh` for the write-capable implementation run.

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

### Step 3 — Hold

Do not implement. Present all approaches, then ask:

> "Which approach should I pursue? Or should I synthesize elements from multiple?"

## After selection

Implement the selected approach directly. If the user asks to synthesize, identify which elements are mechanically compatible and propose a brief hybrid plan before implementing.

## Codex mode (--codex)

With `--codex`, the specification above is unchanged — Codex generates the approaches instead of you, and implements the selected one. Running the brainstorm on a second model family widens the space of approaches beyond what one model proposes. You structure the prompt and present the results; you do not add approaches of your own.

### Invocation mechanism

Plain Claude Code has no native `codex:codex-rescue` subagent. Every "ask Codex" step means calling `codex exec` through the `Bash` tool (the same mechanism `paper-review-lite --codex` uses):

- **`--model gpt-6-astra -c model_reasoning_effort=<effort>`** — pins Codex explicitly (`high` to brainstorm, `xhigh` to implement) rather than relying on `codex exec`'s implicit default, which can drift upstream.
- **`< /dev/null`** — closes stdin. Without it, `codex exec` hangs on "Reading additional input from stdin…" even when the prompt is passed as a CLI argument; this is the most common failure.
- **`--skip-git-repo-check`** so it runs regardless of git state, and **`--sandbox`** set per phase: `read-only` for brainstorming, `workspace-write` for implementation.
- **`timeout: 600000`** (10 min) on the Bash call as a backstop.

The result returns on stdout — read it directly from the Bash output. Treat a non-zero exit, or empty output, as a Codex failure: report it and offer to fall back to plain `/diverge` (Claude-only).

### Steps

1. **Take the task** from `$ARGUMENTS` with `--codex` stripped; if empty, ask the user what they want to solve. Step 1 above (one round of goal questions) still applies before delegating.

2. **Brainstorm via Codex**, substituting `TASK` with the user's request verbatim and adding none of your own implementation preferences:

   ```bash
   codex exec --model gpt-6-astra -c model_reasoning_effort=high --sandbox read-only --skip-git-repo-check "$(cat <<'CODEXEOF'
   <brainstorm prompt template below, with TASK substituted>
   CODEXEOF
   )" < /dev/null
   ```

3. **Present the approaches** to the user verbatim — do not paraphrase, filter, or reorder them. Ask which to pursue, or whether to synthesize.

4. **Implement via Codex** only after selection, switching the sandbox to `workspace-write` and setting `-C` to the project directory. The user's selection is the authorization for this write; the Codex plugin's "stop after presenting findings" guidance covers code-review handoffs, not this step:

   ```bash
   codex exec --model gpt-6-astra -c model_reasoning_effort=xhigh --sandbox workspace-write --skip-git-repo-check -C "<project dir>" "$(cat <<'CODEXEOF'
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
