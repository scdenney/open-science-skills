---
name: advisor
description: Consult Fable 5.1 as an independent second reviewer, always at max reasoning effort. The calling session is the main model — Opus 5 or Sonnet 5 — and Fable holds the advisor seat. Use before committing to an interpretation or a substantial piece of writing/analysis, when stuck (recurring errors, a non-converging approach, results that do not fit), when considering a change of approach, or when you believe a task is complete and want a check before finalizing. Fallback for when the native advisor tool is unavailable. Not a co-implementer — read-only advisory only, does not edit files.
allowed-tools:
  - Read
  - Write
  - Bash
---

# advisor — an independent second reviewer

`fable-advisor.sh` spawns an isolated Fable 5.1 session that reviews one decision point and returns. This is the fallback for when the native `advisor()` tool reports itself unavailable mid-session ("The advisor tool is unavailable. Do not try to use it again.").

<p align="center"><img src="assets/architecture.svg" alt="advisor: the main model (Opus 5 or Sonnet 5) composes one self-contained briefing, sends it to an isolated Fable 5.1 advisor running at max reasoning effort, and receives one decisive read-only review in return" width="900"></p>

## The two seats

| Seat | Model | Role |
|---|---|---|
| Main | **Opus 5**, or Sonnet 5 for cheaper sustained work | Holds the task, the context, and the decision. Does the work. |
| Advisor | **Fable 5.1**, always | Reads one briefing, returns one review. Never edits files. |

The asymmetry is the design. The advisor seat is pinned to Fable and the script guards it — no silent fallback to another model family, since a same-family fallback would defeat the point of asking. The main seat is whichever model the session is already running; a Fable session gets a fresh, isolated Fable instance with no anchoring from the conversation. Nothing carries over from the caller except the working directory (`-C`) — not the conversation, and not the effort level. The consult also runs `--safe-mode`, which starts the advisor with **user and project customizations disabled**: no `CLAUDE.md`, no skills, no plugins, no user/project hooks, no MCP servers, no custom commands or agents. (Org-managed policy settings, where present, still apply — safe mode does not override managed configuration.) It sees the files in that directory and nothing else — not a normal session scoped to the directory, which would load `CLAUDE.md`.

When this skill is called from inside an orchestration (`orchestrate`), the orchestrating lead is the main seat and Fable's consult is one bounded advisory call — not a delegation.

## Compose the briefing yourself

The native tool forwards your whole transcript automatically. This script cannot: it starts a brand-new `claude` process with no memory of this conversation. Everything the advisor needs has to be in the briefing — the task, what you have done, the current approach or the specific claim, and the precise question. File paths and line numbers, the actual claim, not "does this look right?"

- **Inline the standards the advice depends on.** Because of `--safe-mode` the advisor never reads the repository's `CLAUDE.md` or any installed skill, so a project convention, a methodological requirement, or a house style the answer turns on has to be quoted into the briefing. Asking "does this meet our reporting standard?" without stating the standard gets you a generic answer that looks confident.

That is the only real difference from the native tool. Independent judgment, read-only scope, and the timing of the call are all meant to match.

## When to consult

- **Before substantive work** — before writing, before committing to an interpretation, before building on an assumption. Orientation (finding files, reading a source) does not count; writing, editing, and declaring an answer do.
- **When you believe a task is complete.** Make the deliverable durable first — a consult takes real time, and a written result survives a session that ends mid-consult.
- **When stuck** — recurring errors, an approach that will not converge, results that do not fit.
- **When considering a change of approach.**

On work longer than a few steps, consult once before the approach crystallizes and once before declaring done. On short reactive tasks, one consult or none.

Weigh the advice as evidence, not authority: primary-source evidence and empirical failure outrank it. But if your evidence points one way and Fable points another, one more consult stating the conflict plainly ("I found X, you suggest Y, which constraint breaks the tie?") is cheaper than committing to the wrong branch.

## Effort

Fable always runs at `max`. This is an owned policy, not an inherited setting: the consult exists to get a stronger read than the main seat can produce on its own, and a cheap consult under a hard question wastes the reason for asking. A `low`-effort session still gets a `max`-effort advisor.

The script pins it, so there is nothing to pass. `--effort <level>` overrides it only if you deliberately want a cheaper consult on something routine.

## Run a consult

```bash
OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)
"${OSS_ROOT}skills/advisor/scripts/fable-advisor.sh" \
  --prompt-file <briefing-path> \
  --out <output-path> \
  -C "$PWD"
```

Use `timeout: 900000` on the Bash call as a backstop; the script has its own internal timeout. Then read the output file and integrate it — if you diverge from it, be able to say why. The Codex plugin's result-handling guidance (stop after presenting review findings, change nothing) applies to code-review handoffs, not here: this is an advisory consult, and acting on the advice in your own work is the point of running it.

## Notes

- `fable-advisor.sh --check` verifies the `claude` CLI is on PATH and reports the pinned effort — run it after install, or when a consult behaves unexpectedly. the resolved plugin root (`$OSS_ROOT`) resolves to the installed plugin directory at runtime; a hand-installed copy under `~/.claude/skills/` shadows the plugin's own and silently drifts out of date.
- The spawned session runs `--permission-mode plan` and `--no-session-persistence`: advisory only, not resumable.
- The script clears `ANTHROPIC_API_KEY`, so the consult bills the subscription plan even if the calling shell exports a live key.
- Effort enum: `low, medium, high, xhigh, max`, matching `/effort`.
- Model defaults to the `fable` alias. `--model <id>` pins a specific version. If the alias is ever unavailable, report it and ask — do not substitute another family.
- Companion skill: `codex/advisor/` — the same pattern for a Codex-native session, with `gpt-5.6-sol` in the advisor seat at a fixed `xhigh`. Both libraries pin the advisor's effort rather than inheriting the caller's, for the same reason.
