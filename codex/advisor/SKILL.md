---
name: advisor
description: Consult GPT-5.6 "Sol" as an independent, stronger second reviewer, matched to your current reasoning-effort level. Use before committing to an interpretation or a substantial piece of writing/analysis, when stuck (recurring errors, a non-converging approach, results that do not fit), when considering a change of approach, or when you believe a task is complete and want a check before finalizing. Not a co-implementer — read-only advisory only, does not edit files.
---

# Advisor (Sol-consulted)

Consult **GPT-5.6 "Sol"** as an independent second reviewer for one specific decision point, at the same reasoning effort you are currently running at. This is the Codex-side counterpart of the Claude-side `advisor` skill (`plugin/skills/advisor/` in `open-science-skills`), built the same session for the same reason: a single-turn advisory consult, not a delegated implementation.

Read [`scripts/sol-advisor.sh`](scripts/sol-advisor.sh) before the first run — the flags and the effort-handling note there are load-bearing.

## When to use

- **Before substantive work** — before writing, before committing to an interpretation, before building on an assumption. Orientation (finding files, reading a source) is not substantive; writing, editing, and declaring an answer are.
- **When you believe a task is complete.** Make the deliverable durable first (write the file, save the result, commit the change) — the consult takes real time.
- **When stuck** — errors recurring, an approach not converging, results that do not fit.
- **When considering a change of approach.**

On tasks longer than a few steps, consult at least once before committing to an approach and once before declaring done. Give the advice serious weight: if a step you followed on Sol's advice fails empirically, or you have primary-source evidence contradicting a specific claim, adapt. If your own evidence and Sol's advice point different directions, surface the conflict in one more consult rather than silently picking a side.

## Effort calibration — read this before running

Sol should run at the **same reasoning effort you are currently running at**, not a hardcoded default. Codex does not expose its own live reasoning-effort setting as an environment variable inheritable by subprocesses (confirmed empirically: dumping `env` inside a running `codex exec` call shows no `CODEX_REASONING_EFFORT` or equivalent — only Claude Code's own `$CLAUDE_EFFORT` leaked through from an enclosing Claude Code process, which is not your effort level when you are the one running as Codex).

What Codex *does* expose: the "reasoning effort: `<level>`" line shown in your own session banner at startup, visible in your own context. Before running the consult, **read that value from your own session context** and pass it explicitly:

```bash
scripts/sol-advisor.sh --prompt-file <briefing-path> --out <output-path> -C "$PWD" --effort <your-own-level>
```

Do not omit `--effort` and let it silently default to the script's fallback (`high`) unless `high` genuinely is your own current level — the fallback exists so the script never errors on a missing flag, not as a substitute for checking your own level.

## Steps

1. **Compose the briefing.** A self-contained document: the task, what you have done so far (key steps, findings, decisions), your current approach or the specific claim to check, and the precise question. Concrete — file paths, line numbers, the actual claim. Save to a scratch file. Sol has no access to your conversation beyond this file.

2. **If declaring a task complete, make the deliverable durable first.**

3. **Read your own current reasoning-effort level from your session context**, then run:

   ```bash
   scripts/sol-advisor.sh --prompt-file <briefing-path> --out <output-path> -C "$PWD" --effort <your-level>
   ```

4. **Read the output file** and weigh the advice. Integrate it; if you diverge from it, be able to say why.

## Notes

- `scripts/sol-advisor.sh --check` verifies the `codex` CLI is on PATH.
- The spawned Sol session runs `--sandbox read-only` and `--ephemeral` — advisory only, no edits, not saved as a resumable session.
- Default model is `gpt-5.6`. **Confirmed failure mode (live-tested, not hypothetical):** on a Codex CLI authenticated via `codex login` with a ChatGPT account (as opposed to an API key), `gpt-5.6` is rejected outright — `"The 'gpt-5.6' model is not supported when using Codex with a ChatGPT account."` `gpt-5.5` works fine under the same auth. Check `codex login status`: `Logged in using ChatGPT` is the failure case; API-key auth may not have this restriction (not verified either way). If Sol is unreachable for this or any other reason, report it and ask whether to stop or use a named replacement — do not silently fall back to `gpt-5.5` for what is supposed to be a genuinely independent second opinion (a reviewer identical to the executor defeats the point of this specific skill; if a same-model consult is actually fine for the task at hand, the calling agent should use its own judgment directly rather than spend a Sol-branded consult on it).
- Effort enum: `none, minimal, low, medium, high, xhigh` (Codex's scale — no `max`; Claude Code's `max` has no Codex equivalent).
- Companion skill: `plugin/skills/advisor/` (Claude-side) — same pattern, Fable 5 instead of Sol, effort read from `$CLAUDE_EFFORT` instead of the session banner.
