#!/usr/bin/env bash
# claude-peer.sh — invoke Claude Code (Anthropic) as a cross-vendor peer for /orchestrate.
#
# Runs a separate Claude CLI consult using a self-contained prompt.
# The caller may pair it with an OpenAI worker for a blind cross-vendor review.
# Different vendors can still share errors; compare their checkable evidence.
# Parent sandbox, authentication, and network permissions apply.
#
# Usage:
#   claude-peer.sh [-C DIR] [--timeout SEC] [--model ID] [--effort LEVEL]
#                  [--out FILE] (--prompt TEXT | --prompt-file PATH | -)
#
#   -C DIR          working dir Claude sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --model ID      default: fable; select a different Claude model explicitly
#   --effort LEVEL  reasoning effort, passed as CLAUDE_EFFORT=LEVEL in the child's
#                   environment (default: high)
#   --out FILE      also tee Claude's stdout+stderr here (for background reads)
#   --prompt TEXT   prompt as a single argument
#   --prompt-file P read prompt from file P
#   -               read prompt from stdin
set -euo pipefail

DIR="$PWD"; TIMEOUT=600; MODEL="fable"; EFFORT="high"; OUT=""; PROMPT=""; PROMPT_SET=0

die(){ echo "claude-peer: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    -C|--dir)      DIR="${2:?}"; shift 2 ;;
    --timeout)     TIMEOUT="${2:?}"; shift 2 ;;
    --model)       MODEL="${2:?}"; shift 2 ;;
    --effort)      EFFORT="${2:?}"; shift 2 ;;
    --out)         OUT="${2:?}"; shift 2 ;;
    --prompt)      PROMPT="${2:?}"; PROMPT_SET=1; shift 2 ;;
    --prompt-file) PROMPT="$(cat "${2:?}")"; PROMPT_SET=1; shift 2 ;;
    -)             PROMPT="$(cat)"; PROMPT_SET=1; shift ;;
    -h|--help)     grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)             die "unknown argument: $1" ;;
  esac
done

[ "$PROMPT_SET" -eq 1 ] || die "no prompt — pass --prompt, --prompt-file, or -"
[ -n "$PROMPT" ] || die "empty prompt rejected"

command -v claude >/dev/null 2>&1 || die "claude CLI not found on PATH"

run() {
  cd "$DIR"
  local cmd=(claude -p "$PROMPT" --model "$MODEL" --output-format text)
  # `timeout` is not preinstalled on macOS (only via GNU coreutils) — guard
  # rather than assume, matching codex-peer.sh's own fix for the identical
  # problem (confirmed missing on this machine 2026-07-18: neither `timeout`
  # nor `gtimeout` is on PATH).
  if command -v timeout >/dev/null 2>&1; then
    CLAUDE_EFFORT="$EFFORT" timeout "${TIMEOUT}s" "${cmd[@]}" < /dev/null
  elif command -v gtimeout >/dev/null 2>&1; then
    CLAUDE_EFFORT="$EFFORT" gtimeout "${TIMEOUT}s" "${cmd[@]}" < /dev/null
  else
    CLAUDE_EFFORT="$EFFORT" "${cmd[@]}" < /dev/null
  fi
}

if [ -n "$OUT" ]; then
  run 2>&1 | tee "$OUT"
else
  run
fi
