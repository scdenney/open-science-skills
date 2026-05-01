# Presubmit Activator

Activate the standalone [`presubmit`](https://github.com/scdenney/presubmit) Python CLI — a 30+ stage adversarial peer-review pipeline (Red Team, Blue Team, verification cascade, legal pass, copyedit, Writer Mode) that calls the Anthropic API directly and writes a consolidated review report to disk. Walks first-time users through install (clone + venv + pip), API key setup, and output location, then orchestrates per-paper runs with the right slug-based file-naming convention.

For the in-session lightweight counterpart that runs parallel sub-agents inside Claude Code (no API key, no per-token cost), use [`/paper-review-lite`](../skills/paper-review-lite/SKILL.md) instead.

$ARGUMENTS
