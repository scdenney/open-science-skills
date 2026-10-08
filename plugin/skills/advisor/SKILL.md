---
disable-model-invocation: true
name: advisor
description: Consults Fable as an independent, read-only reviewer at an effort the caller matches to the question. The calling session (usually Opus, or Haiku) holds the task and escalates one decision point. Use before committing to an interpretation or a substantial piece of writing or analysis, when stuck or not converging, when changing approach, or as a final check on a finished task. Fallback for when the native advisor tool is unavailable. Not for a session already running Fable.
allowed-tools:
- Read
- Write
- Bash
---

# advisor — escalate a decision point to Fable

`fable-advisor.sh` starts an isolated Fable session that reviews one decision point and returns. If the session has the native advisor tool (`/advisor fable`), use that; this skill is the fallback for when it is off or reports itself unavailable.

<p align="center"><img src="https://raw.githubusercontent.com/scdenney/open-science-skills/main/plugin/skills/advisor/assets/architecture.svg" alt="advisor: the main model (Opus, or Haiku) composes one self-contained briefing, sends it to an isolated Fable advisor running at an effort chosen for the question, and receives one decisive read-only review in return" width="900"></p>

## The two seats

| Seat | Model | Role |
|---|---|---|
| Main | **Opus**, or Haiku for cheap sustained work | Holds the task, the context, and the decision. Does the work. |
| Advisor | **Fable** | Reads one briefing, returns one review. Never edits files. |

This is an escalation, not a peer review: a working model reaches up to the premier model when a decision point is worth it. The script pins the advisor to Fable and never falls back to another family, since a same-family fallback defeats the point. Inside `orchestrate`, an Opus lead is the main seat and the consult is one bounded call, not a delegation.

**A session running Fable does not use this skill.** A second, isolated Fable is the same model answering the same question. A Fable session that wants an independent read goes cross-vendor: `orchestrate`'s Codex peer (`codex-peer.sh --mode cross-check`) or `/model-committee`. Decide from the model line Claude Code injects into the session ("You are powered by the model named …"), say so, and stop.

## Choose Fable's effort

The caller picks the effort for each consult and tells the user the level and the reason in one line ("advisor at xhigh: choosing between two identification strategies"). It is never inherited from the session.

| Effort | Use for |
|---|---|
| `high` (default) | a completion check; a bounded question whose answer you can check; a sanity read before writing |
| `xhigh` | an interpretation or design decision; stuck or non-converging work; a proposed change of approach |
| `max` | high-stakes and hard to verify: an identification strategy, a publication-facing claim, an irreversible choice |

Anthropic recommends starting Fable 5.1 at `high` and stepping up to `xhigh` or `max` for the most capability-sensitive work; that is the basis for this ladder. A cheap session can still buy a `max` consult when the question warrants it.

## Compose the briefing

The script starts a new `claude` process with no memory of this conversation, so the briefing carries everything: the task, what has been done, the current approach or the exact claim, and the precise question, with file paths and line numbers.

The consult runs with `--safe-mode`: no `CLAUDE.md`, skills, plugins, hooks, MCP servers, custom commands, or agents load (org-managed policy still applies). It sees the files in the `-C` directory and nothing else. Quote any project convention, methodological requirement, or house style the answer depends on into the briefing; asking "does this meet our reporting standard?" without stating the standard gets a confident generic answer.

## When to consult

- **Before substantive work** — before writing, committing to an interpretation, or building on an assumption. Orientation does not count.
- **When you believe a task is complete.** Make the deliverable durable first; a consult takes real time.
- **When stuck** — recurring errors, an approach that will not converge, results that do not fit.
- **When considering a change of approach.**

On work longer than a few steps, consult once before the approach sets and once before declaring done. On short tasks, once or not at all.

Weigh the advice as evidence, not authority: primary sources and empirical failure outrank it. If your evidence and Fable's advice conflict, one more consult stating the conflict plainly ("I found X, you suggest Y — which constraint breaks the tie?") is cheaper than committing to the wrong branch.

## Run a consult

```bash
OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)
"${OSS_ROOT}skills/advisor/scripts/fable-advisor.sh" \
  --prompt-file <briefing-path> \
  --out <output-path> \
  --effort <high|xhigh|max> \
  -C "$PWD"
```

Give the Bash call `timeout: 900000` as a backstop; the script has its own timeout (`--timeout`, default 900 s — raise it for a `max` consult on a large briefing). Read the output and act on it; if you diverge from it, be able to say why. The Codex plugin's "stop after presenting findings" guidance applies to code-review handoffs, not here.

## Notes

- `fable-advisor.sh --check` confirms the `claude` CLI is on PATH and reports the default effort. A hand-installed copy under `~/.claude/skills/` shadows the plugin's and drifts out of date.
- The consult runs `--permission-mode plan` and `--no-session-persistence`: advisory only, not resumable.
- The script clears `ANTHROPIC_API_KEY`, so the consult bills the subscription even if the shell exports a key.
- The model defaults to the `fable` alias; `--model <id>` pins a version. If the alias is unavailable, report it and ask rather than substituting another family.
- Companion: `codex/advisor/` is the same pattern for a Codex session, with `gpt-6-astra` in the advisor seat and the same effort ladder.
