---
name: diverge-codex
description: Delegate creative divergence to Codex (GPT-5.6 "Sol" at xhigh effort). Codex generates 3-5 conceptually distinct approaches before any implementation; Claude presents them for selection, then has Codex implement the chosen one. Cross-model brainstorm-then-select.
argument-hint: "[describe the task to delegate to Codex for divergent brainstorming]"
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# Diverge → Codex

Run the brainstorm on a second model family, which widens the space of approaches beyond what one model proposes. Claude structures the prompt; Codex (GPT-5.6 "Sol" at xhigh effort) brainstorms; Claude presents the options for selection; Codex implements the chosen approach.

## Heritage and scope

Cross-model sibling of [`diverge`](../diverge/SKILL.md), grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`../diverge/reference/creative-preference-optimization.md`](../diverge/reference/creative-preference-optimization.md)). Same brainstorm-then-select discipline, run on a model whose blind spots differ from Claude's.

## Codex invocation mechanism

Plain Claude Code has no native `codex:codex-rescue` subagent. Every "ask Codex" step below means calling `codex exec` through the `Bash` tool (the same mechanism `paper-review-lite-codex` uses):

- **`--model gpt-5.6-sol -c model_reasoning_effort=xhigh`** — pins Codex explicitly rather than relying on `codex exec`'s own implicit default, which can drift upstream.
- **`< /dev/null`** — closes stdin. Without it, `codex exec` hangs on "Reading additional input from stdin…" even when the prompt is passed as a CLI argument. This is the single most common failure mode.
- **`--skip-git-repo-check`** so it runs regardless of git state, and **`--sandbox`** set per phase: `read-only` for brainstorming, `workspace-write` for implementation.
- **`timeout: 600000`** (10 min) on the Bash call as a backstop.

The result returns on stdout — read it directly from the Bash output. Treat a non-zero exit, or empty output, as a Codex failure: report it and offer to fall back to `/diverge` (Claude-only).

## Steps

1. **Take the task** from `$ARGUMENTS`; if empty, ask the user what they want to solve. If the goal (not the implementation) is ambiguous, ask one focused question before delegating.

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

## Brainstorm prompt template

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

## Implementation prompt template

```xml
<task>
Implement the following approach to: TASK

Selected approach: SELECTED_APPROACH

Implement it fully. Edit files in place where applicable.
</task>
```
