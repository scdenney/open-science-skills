#!/usr/bin/env bash
# claude-peer.sh — invoke Claude Code (Anthropic) as a cross-vendor peer for /46-orchestrate.
#
# This is the mechanism 46-orchestrate's SKILL.md previously only described in prose
# ("step outside to a cross-vendor check that brings Claude in as the decorrelated
# vendor") without ever giving a way to do it. Without this script, the only
# "decorrelated" check a Sol lead had was a same-vendor, weaker-tier Terra one-shot —
# not a real cross-vendor line, unlike fable-orchestrate's Codex peer or
# opus-orchestrate's Codex peer. This script closes that gap in the other direction:
# it is codex-peer.sh's mirror image, a Codex lead calling out to Claude instead of
# a Claude lead calling out to Codex.
#
# VERIFIED pattern (this is the whole reason the wrapper exists):
#   claude -p "<prompt>" --output-format json < /dev/null
# Headless `claude -p` needs no stdin and exits after one turn; it does not hang
# the way a bare `codex exec` does, but redirecting /dev/null keeps behavior
# identical to codex-peer.sh's own defensive pattern and avoids any TTY surprises
# when this runs backgrounded.
#
# The lead runs this via a backgrounded out-of-band call (same discipline as a Terra
# one-shot: fire it, keep working, read --out when it returns) for the high-stakes
# path — launch this AND a Terra out-of-band one-shot on the SAME prompt in one
# round, blind to each other, then reconcile. That is a genuine cross-vendor,
# cross-tier check: Claude's model family is fully decorrelated from anything in the
# GPT-5.6 family, the same value fable-/opus-orchestrate get from their Codex peer,
# now available in the other direction.
#
# Usage:
#   claude-peer.sh [-C DIR] [--timeout SEC] [--model ID] [--effort LEVEL]
#                  [--out FILE] (--prompt TEXT | --prompt-file PATH | -)
#
#   -C DIR          working dir Claude sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --model ID      Claude model to pin (default: fable — flagship for flagship,
#                   matching how codex-peer.sh defaults to Sol, the flagship Codex
#                   tier; confirmed in a same-brief benchmark rerun, 2026-07-19,
#                   where a Sol/xhigh lead with a Fable peer reached Distinction on
#                   5 of 6 tiers. Pass --model sonnet or --model opus for a cheaper
#                   check on a routine, lower-stakes consult)
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
