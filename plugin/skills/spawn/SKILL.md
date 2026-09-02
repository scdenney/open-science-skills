---
name: spawn
description: Spawn full Claude Code peer sessions in their own terminal panes and git worktrees — real sessions, not subagents — each on a directed task with a contract brief, monitored and merged back by the spawning lead. Detects the environment and takes the strongest path — herdr first, then tmux, then a native claude background agent. Use when work must outlive or run beside the current session, needs its own worktree or its own permission settings, should stay steerable by the user in a visible pane, or when the user asks to spawn, hand off, or parallelize across full sessions. Also spawns Codex peers into the same panes. Not for bounded consults or work a subagent covers.
argument-hint: "[describe the task(s) to run in spawned peer sessions; one worktree and brief per task]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Spawn

<p align="center"><img src="assets/architecture.svg" alt="spawn: a lead session detects its environment (herdr, tmux, or plain terminal), creates a git worktree per task, starts full peer sessions in new panes, briefs each by contract, monitors without babysitting, and merges each branch back." width="900"></p>

You are the **lead**. A spawned peer is a **full Claude Code session** — its own context window, its own permission prompts, its own lifetime, steerable by the user in a visible pane (a split of the terminal window the user can watch and type into). That makes it a third kind of delegate, above the two the library already has:

| Tier | What it is | Lifetime | Reach it via |
|---|---|---|---|
| subagent | in-session worker inside your context budget | dies with your turn | `Agent` tool (orchestrate skills) |
| one-shot | fresh `claude -p` / `codex exec` process | one turn, deliberately not resumable | advisor and peer scripts |
| **spawned peer** | full interactive session, own pane + worktree | survives you; user-steerable | this skill |

## When to spawn — and when not

Fire on any one signal:

- the work must **survive this session** or run long beside it
- it needs **its own git worktree** (a separate working copy of the repository on its own branch, so nothing it edits collides with yours) — large parallel edits where sessions would otherwise keep touching the same files
- the user should be able to **watch and steer it live** in its own pane
- it needs **different permission settings or a different model** than your session (say, allowed to edit files without asking)

Do not spawn for a bounded consult (`advisor`), mechanical bounded work (a `fast-worker` subagent), or a read-only question (a `claude -p` one-shot). A peer costs a worktree, a pane, and a merge — spend that only when the lifetime, the pane, or the isolation is the point.

## Detect the environment

| Check, in order | You are in | Path |
|---|---|---|
| `HERDR_ENV` is set | herdr | full path below — worktree, tab, agent lifecycle |
| `$TMUX` is set | tmux | worktree + pane, manual monitoring (Fallbacks) |
| neither | plain terminal | `claude --bg` background agent, no pane (Fallbacks) |

## Spawn a peer — herdr, the verified path

Each command emits JSON carrying the ids the next one needs. `worktree create` returns the workspace id, the checkout path, and a root pane already open at a shell prompt, so a fresh spawn needs no `tab create` at all (`herdr tab create --workspace <WS_ID> --cwd <WT_PATH> --no-focus` is for additional tabs, each with its own root pane). If you lose an id, re-find it with `herdr worktree list`, `herdr agent list`, or `herdr api snapshot`. Parse the JSON — never scrape human-readable output, since the CLI drifts across stable and preview channels. Each Bash call is also a fresh shell: `$slug` and captured ids do not persist between calls, so redeclare them per call or substitute literally.

```bash
slug=fix-ingest    # short dashed name, 2–4 lowercase words, e.g. fix-ingest — names the branch, the workspace label, and the agent
herdr worktree create --cwd "$PWD" --branch "spawn/$slug" --label "$slug"   # JSON — workspace_id, checkout path, root pane_id
# write the brief before starting the agent (next section) → <WT_PATH>/.spawn/brief.md
herdr agent start "$slug" --kind claude --pane <PANE_ID>       # the root pane; agent flags go after --  (e.g. -- --model opus)
herdr agent wait "$slug" --until blocked --timeout 15000 || true # a fresh peer always blocks first: Claude Code's workspace-trust dialog
herdr agent read "$slug" --lines 20                              # expect "Is this a project you created or one you trust?"
herdr agent send-keys "$slug" Down Enter                         # select "Yes, I trust this folder"; agent prompt cannot clear a dialog
herdr agent prompt "$slug" "Read .spawn/brief.md and begin. Reply here when the acceptance checks pass."
```

**`--cwd "$PWD"` is not optional.** herdr resolves the repository from the calling workspace, not from the shell's directory, and every Bash call is a fresh shell, so without `--cwd` it branches and checks out whatever repository the workspace is associated with. Verified 2026-09-02: from a scratch repo, the bare form created a worktree of an unrelated repository. Check `repo_root` in the JSON before going on. `--base <ref>` pins the baseline when main is moving under you.

Permissions match yours, not a hardcoded default. Before starting the peer, read your own pane to see your live mode, and read wide enough to actually find it:

```bash
herdr agent read "$HERDR_PANE_ID" --lines 30 | grep -iE "bypass permissions|accept edits|plan mode|auto|manual|don.t ask" | tail -1
```

The status line names the mode directly (for example, `⏵⏵ bypass permissions on (shift+tab to cycle)`). Match whichever mode phrase the status line shows — the six modes render as distinct phrases and the exact strings beyond the verified ones may differ by version, one more reason never to guess. A tight read such as `--lines 3` is unreliable here: it works only when the status line is the last thing rendered, and this skill is routed to from leads with background subagents running — exactly the state whose task list pushes the status line out of the last few rows. If the grep returns nothing, widen it with `--source visible` before concluding anything. **Do not pass a mode you did not actually read** — guessing reintroduces the default-fallback bug this self-read exists to prevent. Pass the matching flag after `--`, `--permission-mode <mode>`, one of `acceptEdits | auto | bypassPermissions | manual | dontAsk | plan`. Skip this and the peer falls back to Claude Code's own configured default (`~/.claude/settings.json`'s `permissions.defaultMode`), which can silently diverge from what you're actually running. This very session, for instance, is configured to `auto` but its live status line currently reads `bypassPermissions`, because the mode was cycled mid-session — only the self-read catches that gap. The visible pane is still the safety net either way, since herdr surfaces `blocked` the moment the peer asks for something its mode doesn't cover. If your own mode already grants broad access, the peer inherits that same exposure: worktree isolation confines its *file* edits, never its shell commands.

## Write the brief first

The brief is a file (`<WT_PATH>/.spawn/brief.md`), not an inline prompt. A real brief is too long to pass on the command line, survives the peer's own compaction for re-reading, and sits in the worktree at merge-review time as the audit record. The kickoff prompt is one line pointing at it.

Use the delegation contract the library already runs on — the same fields you would give any delegate: **Objective · Inputs and authoritative paths · In scope · Out of scope · Constraints and invariants · Write ownership · Expected artifact · Acceptance checks · Return format** (conclusion, evidence, changed files, residual risk). Then three spawn-specific lines:

```markdown
Branch etiquette — commit to spawn/<slug>; never merge, never push; do not commit .spawn/.
Suggested skills — the /oss: skills the peer should invoke, so it does not rediscover them.
Baseline — the commit this worktree was cut from. Reference artifacts by path at that commit; never paste secrets into the brief.
```

Once per repo, add `.spawn/` to `.git/info/exclude` — worktrees share it, so every peer's brief stays untracked with no `.gitignore` churn.

## Monitor without babysitting

One Bash call with `run_in_background: true` — you are notified when it exits, and your context never grows from polling:

```bash
herdr agent wait "$slug" --until working --timeout 15000 || true   # confirm launch; times out harmlessly if the peer already finished
herdr agent wait "$slug" --timeout 3600000                         # settles on idle | blocked | done
```

When the notification fires, judge the true state — the agent's word is not the artifact:

```bash
herdr agent explain "$slug"                 # what herdr thinks the state is and why (hook-reported vs. screen-inferred)
herdr agent read "$slug" --lines 60
git -C <WT_PATH> status --porcelain && git -C <WT_PATH> log --oneline -3
```

`agent explain` prints five plain-text lines, not JSON: `agent`, `state` (`blocked` | `idle` | `working`), `manifest`, `rule` (the detection rule that fired, with its screen region and priority), and `evidence` (the captured text). Observed on 0.8.0: the trust dialog is `live_blocked_form`, a settled prompt box is `live_prompt_box`, and a running turn is `osc_title_working`. `integration status` tells you whether the hook is current; `explain` tells you which rule fired. A current hook registers the peer's `agent_session` id (visible in `agent get`), which is what makes `wait` reliable; the state itself is usually resolved by a screen rule either way. `herdr agent get "$slug"` returns the agent's ids and pane when you have lost them.

A blocked peer: `agent read` first. A question you can answer → `herdr agent prompt`. A TUI dialog (a permission menu) → `herdr agent send-keys`. A judgment call → `herdr agent focus` and tell the user which pane and why. Spot-check anytime with `agent read` and a small `--lines`; do not stream panes into your context.

## Fold back in

Run this checklist per peer, in order. Skipping the last two steps is how orphaned checkouts accumulate under `~/.herdr/worktrees/<repo>/`.

1. **Peer commits and stops.** It commits on `spawn/<slug>` and never merges (the brief says so). Confirm: `git -C <WT_PATH> status --porcelain` is empty and `git -C <WT_PATH> log --oneline -3` shows its work.
2. **Review from the main checkout.** `git log main..spawn/<slug>` and `git diff main...spawn/<slug>`; worktree branches are visible with no fetch. Substitute the repo's integration branch when it is not `main`.
3. **If main moved, the peer rebases** and re-runs its acceptance checks: `herdr agent prompt "$slug" "Rebase onto main, re-run the acceptance checks, and report."` It holds the conflict context; you do not.
4. **Merge from the main checkout and run the acceptance checks yourself.** You retain integration ownership, of correctness and of rigor.
5. **Remove the checkout.** `herdr worktree remove --workspace <WS_ID>`. `--force` only when the agent is idle or done AND the checkout is clean, or the work is deliberately abandoned. A checkout that holds submodules cannot be removed by `git worktree remove`; delete the directory and run `git worktree prune` in the main checkout.
6. **Delete the branch.** `git branch -d spawn/<slug>` from the main checkout, after the worktree is gone (the same branch cannot be checked out twice, and `-d` refuses an unmerged branch, which is the safety you want).
7. **Confirm nothing is left**, in three places. `git worktree list` in the main checkout shows only the main checkout and any peers still running. `ls ~/.herdr/worktrees/<repo>/` shows no directory for this slug; `rmdir` the parent if it is now empty, since `worktree remove` leaves it. `herdr worktree list` and `herdr workspace list` show no workspace for this spawn; `worktree create` also opens a workspace for the source checkout, which nothing else closes, so `herdr workspace close <id>` (positional, not `--workspace`) when the spawn opened one.

With several peers, merge one at a time and rebase the next between merges: worktrees prevent write collisions, not merge collisions.

### Sweep orphans

Run at the start of a spawn session, or whenever `~/.herdr/worktrees/` looks crowded:

```bash
for wt in ~/.herdr/worktrees/*/*/; do
  b=$(git -C "$wt" branch --show-current 2>/dev/null) || { echo "$wt: not a checkout"; continue; }
  main=$(git -C "$wt" worktree list --porcelain | head -1 | sed 's/^worktree //')
  echo "$wt  branch=$b  dirty=$(git -C "$wt" status --porcelain | wc -l | tr -d ' ')  unmerged=$(git -C "$main" log --oneline main..$b | wc -l | tr -d ' ')"
done
```

A checkout with `dirty=0` and `unmerged=0` is done: remove it (`herdr worktree remove`, or `git worktree remove` from the main checkout) and delete its branch. A checkout with dirty files or unmerged commits is not yours to delete; put it to the user with the branch name and the counts. A directory that is no longer a checkout at all (`.git` file pointing at a pruned worktree) is a leftover: `git worktree prune` in the main repo, then delete the directory. Finish with `herdr worktree list` and `herdr workspace list` so herdr's own records agree with git; empty per-repo directories under `~/.herdr/worktrees/` are leftovers of `worktree remove` and can be removed with `rmdir`.
## Fallbacks — tmux, then claude --bg

**tmux** (`$TMUX` set): same brief, manual lifecycle.

```bash
git worktree add "../$(basename "$PWD")-spawn-$slug" -b "spawn/$slug"
pane=$(tmux split-window -P -F '#{pane_id}' -c "<WT_PATH>")   # or new-window -n "$slug"
tmux send-keys -t "$pane" 'claude' Enter
# wait for the REPL to draw, then:
tmux send-keys -t "$pane" 'Read .spawn/brief.md and begin.' Enter
```

Monitor with `tmux capture-pane -p -t "$pane" | tail -30`. There is no agent-state detection — the pane is your `agent read`, and the human is your `blocked` detector.

**Plain terminal** (neither): same worktree, no pane.

```bash
git worktree add "../$(basename "$PWD")-spawn-$slug" -b "spawn/$slug"
( cd <WT_PATH> && claude --bg --name "$slug" "Read .spawn/brief.md and begin." )
```

Manage with `claude agents` — coarser steering, same brief, same merge-back.

## Gotchas

- `agent prompt --wait` from an idle agent demands an observed state change within 5000 ms or returns `agent_prompt_stalled` — and it matches *states*, not turns, so an already-working agent's current turn can satisfy it. Use the two-step wait idiom instead.
- `agent wait` (and `agent prompt --wait`) are **indefinite without `--timeout`**. Always bound them.
- **A worktree sees only committed state.** Uncommitted lead-side edits are invisible to the peer — commit first, or copy the file into the worktree, and name the baseline commit in the brief.
- A peer whose mode still prompts (e.g. `manual`, `dontAsk`, plain `auto`) sits `blocked` at its first permission prompt until someone answers. Attend its first minute, or pass the lead's own live mode (see Permissions above) so the peer starts already matched to what you're running.
- Forgot to pass a mode? The peer used Claude Code's configured default, not yours — check with `herdr agent read <name> --lines 30` (grep for the mode string as above) and restart it with the right `--permission-mode` if the two diverge.
- `agent prompt` submits a *turn*; TUI dialogs need `agent send-keys`.
- **A fresh peer's first state is `blocked`**, on Claude Code's workspace-trust dialog, because the worktree path is new. Clear it with `agent send-keys "$slug" Down Enter`; no `--permission-mode` skips it. In `auto` permission mode the lead's own classifier may refuse `agent send-keys`, `workspace close`, and `worktree remove --force`; hand those to the user rather than retrying.
- `wait` can settle on `done` while a follow-up `explain` reports `idle`; `done` is transient. Judge from git, not from either word.
- `worktree remove --workspace <id>` succeeds without `--force` even while a peer is still running in the pane, and takes the agent and pane down silently. Check `agent explain` first.
- A peer starts on the **user's** default model and effort, not yours — pin with `-- --model … --effort …` when the tier matters (observed 2026-08-06: a Fable lead spawned a Sonnet-default peer).
- Lost an id → `herdr worktree list`, `herdr agent list`, `herdr agent get <name>`, `herdr api snapshot`.
- **Reattaching after a restart.** A peer's checkout survives a herdr or terminal restart; its pane and agent do not. `herdr worktree open --cwd <REPO_ROOT> --path <WT_PATH>` (or `--branch spawn/<slug>`) reopens the checkout as a workspace with a fresh root pane (the checkout must still exist; after `worktree remove` there is nothing to reopen); then `herdr agent start` again and prompt it to read `.spawn/brief.md` and continue from the last commit.
- `HERDR_*` variables exist only inside herdr — and spawned tabs inherit them, so peers can themselves spawn.
- The same branch cannot be checked out in two worktrees. Merge from the main checkout; delete the branch only after `worktree remove`.

## Troubleshooting

- **`agent start` times out** — the pane was not at an interactive shell prompt, or the agent binary is not on PATH in that shell. `herdr pane read <PANE_ID>` to see what the pane shows; raise `--timeout` (default 30000, max 300000) for slow cold starts.
- **`worktree create` fails** — usually an existing branch of the same name (`git branch --list 'spawn/*'`) or a repo state that cannot branch; create from a clean HEAD or pass `--base`.
- **Socket errors on every `herdr` command** — you are not inside herdr (`HERDR_ENV` unset) or the server restarted. Check `herdr status`, then fall back to tmux or `claude --bg`.

## Notes

- The library's other cross-model calls (`fable-advisor.sh`, `codex-peer.sh`, the committee members) are deliberately isolated one-shots with session persistence off; a spawned peer is the opposite — persistent, steerable, resumable. Choose by whether the work needs a lifetime.
- A **Codex peer** is one flag: `herdr agent start "$slug" --kind codex --pane <PANE_ID>` — same brief; the contract is Codex's own from `orchestrate`. herdr detects 21 agent kinds, so the same move spawns other agents too. State detection for a kind depends on its integration hook being current (`herdr integration status`; install or update with `herdr integration install <kind>`), otherwise `wait` falls back to screen inference.
- Heritage: generalizes Matt Pocock's `claude-handoff` (MIT, [mattpocock/skills](https://github.com/mattpocock/skills)) — handoff compacts one conversation into a document for one `claude --bg` successor; spawn adds environment detection, worktree isolation, directed contract briefs, and lifecycle management for N peers. See [`RECOMMENDED.md`](../../../RECOMMENDED.md).
- Routed to by `orchestrate` routing row 8; standalone via `/oss:spawn`.
- herdr surface verified 2026-08-06 by live run on herdr 0.7.5; re-verified 2026-09-02 by a live dry run on herdr 0.8.0 (protocol 19, Claude and Codex integration hooks v7), which added `agent explain`, `agent get`, `worktree open`, and `integration`. The dry run is what established the `--cwd` requirement, the trust-dialog block, and the `explain` output shape above. Flag names above match the 0.8.0 schema (`worktree create`: `--branch --label --base --path --cwd`; `worktree remove`: `--workspace --force`; `agent start`: `--kind --pane --timeout`; `agent wait`: `--until --timeout`). The fold-back checklist and orphan sweep were written after a sweep found ten orphaned checkouts across three repos.
