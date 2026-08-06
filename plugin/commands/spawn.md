# Spawn

Spawn one or more full Claude Code peer sessions (real sessions in their own terminal panes and git worktrees, not subagents), each on a directed task. Detect the environment first (herdr if `HERDR_ENV` is set, else tmux, else a native `claude --bg` background agent), create a worktree on branch `spawn/<slug>` per task, write the delegation-contract brief to `.spawn/brief.md` in the worktree, start the agent in a new pane, and send one kickoff prompt pointing at the brief.

Monitor without babysitting: background a bounded `herdr agent wait`, spot-check with `agent read`, and answer or refocus a blocked peer. Keep integration ownership — the peer commits to its branch and stops, you review the branch, have the peer rebase if main moved, merge from the main checkout, then remove the worktree. See the `spawn` skill for the verified herdr sequence, the brief template, the monitoring idiom, the merge-back protocol, and the tmux and `claude --bg` fallbacks.

$ARGUMENTS
