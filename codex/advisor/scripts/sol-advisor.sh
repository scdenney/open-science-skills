#!/usr/bin/env bash
# sol-advisor.sh — consult GPT-5.6 "Sol" as an independent second reviewer.
#
# Read-only advisory consult, not implementation. Spawns a fresh, ephemeral
# `codex exec` session (--sandbox read-only: no edits) at an explicit
# reasoning effort level, since (unlike Claude Code's $CLAUDE_EFFORT) Codex
# does not expose its own live effort as an inheritable environment variable
# to subprocesses — confirmed empirically by dumping env inside a running
# codex exec call. The caller must therefore READ its own effort level from
# its own visible session context (the "reasoning effort: <level>" line
# shown at session start) and pass it explicitly via --effort. See SKILL.md.
#
# This spawns an ISOLATED session with no automatic access to the calling
# conversation, so the caller must compose a self-contained briefing and
# pass it as --prompt-file.
#
# Usage:
#   sol-advisor.sh --prompt-file FILE --out FILE [-C DIR] [--model ID]
#                   [--effort LEVEL] [--timeout SEC]
#   sol-advisor.sh --check
#
#   --prompt-file FILE  the self-contained briefing (task, progress, question)
#   --out FILE          where Sol's advice is written
#   -C DIR              working dir Sol sees (default: $PWD)
#   --model ID          Codex model to pin (default: gpt-5.6 — "Sol")
#   --effort LEVEL      none|minimal|low|medium|high|xhigh (default: high —
#                        the caller should pass its own actual level; this
#                        default is a fallback only, not a substitute for it)
#   --timeout SEC        hard kill after SEC seconds (default: 900)
set -euo pipefail

MODEL="gpt-5.6"
WORKDIR="$PWD"
PROMPT_FILE=""
OUT=""
EFFORT="high"
TIMEOUT_SECONDS=900

usage() {
  printf '%s\n' \
    'Usage: sol-advisor.sh --prompt-file FILE --out FILE [-C DIR] [--model ID] [--effort LEVEL] [--timeout SEC]' \
    '       sol-advisor.sh --check'
}

die() { printf 'sol-advisor: %s\n' "$*" >&2; exit 2; }

if [[ "${1:-}" == "--check" ]]; then
  command -v codex >/dev/null || die 'codex CLI not found'
  codex --version
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt-file) PROMPT_FILE="${2:-}"; shift 2 ;;
    --out) OUT="${2:-}"; shift 2 ;;
    -C) WORKDIR="${2:-}"; shift 2 ;;
    --model) MODEL="${2:-}"; shift 2 ;;
    --effort) EFFORT="${2:-}"; shift 2 ;;
    --timeout) TIMEOUT_SECONDS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

command -v codex >/dev/null || die 'codex CLI not found'
[[ -n "$PROMPT_FILE" && -r "$PROMPT_FILE" ]] || die 'readable --prompt-file is required (the self-contained briefing)'
[[ -n "$OUT" ]] || die '--out is required'
[[ -d "$WORKDIR" ]] || die "working directory not found: $WORKDIR"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || die '--timeout must be a positive integer'
case "$EFFORT" in none|minimal|low|medium|high|xhigh) ;; *) die "bad --effort: $EFFORT (none|minimal|low|medium|high|xhigh)" ;; esac
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
WORKDIR="$(cd "$WORKDIR" && pwd -P)"
mkdir -p "$(dirname "$OUT")"

cmd=(codex exec --ephemeral --model "$MODEL" -c model_reasoning_effort="$EFFORT" --sandbox read-only --skip-git-repo-check -C "$WORKDIR" --output-last-message "$OUT" \
  'You are consulted as an independent, stronger second reviewer for one specific decision point — not a co-implementer. Read the self-contained briefing supplied on stdin (the task, what has been done so far, the current approach or findings, and the specific question). You have no access to the original conversation beyond this briefing, so if it seems to be missing something you need, say what is missing rather than guessing. Give direct, decisive advice on the specific question asked. If you disagree with the stated approach, say so plainly and explain the specific failure mode, do not hedge into a survey of options. Do not edit any files — you are read-only advisory only. Return only your advice, no preamble.')

if command -v timeout >/dev/null; then
  timeout "${TIMEOUT_SECONDS}s" "${cmd[@]}" < "$PROMPT_FILE" >/dev/null
else
  "${cmd[@]}" < "$PROMPT_FILE" >/dev/null
fi

[[ -s "$OUT" ]] || die 'Sol returned no output'
