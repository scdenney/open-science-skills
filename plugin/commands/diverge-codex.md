# Diverge → Codex

Delegate creative divergence to Codex (GPT-5.4). Compose a brainstorm prompt from the task below and run it through `codex exec` (read-only sandbox, stdin closed with `< /dev/null`); Codex returns 3–5 conceptually distinct approaches labeled by creativity dimension, with at least one [Surprising] and one [Novel]. Present Codex's approaches to the user verbatim and ask which to pursue. Then run the chosen approach back through `codex exec` (workspace-write) to implement it. Never let Codex implement on the first delegation. If Codex is unavailable or errors, offer to fall back to `/diverge` (Claude-only).

$ARGUMENTS
