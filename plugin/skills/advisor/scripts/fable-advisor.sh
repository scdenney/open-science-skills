#!/usr/bin/env bash
# fable-advisor.sh — consult Fable 5 as an independent second reviewer.
#
# Read-only advisory consult, not implementation. Spawns a fresh, isolated
# `claude` session (--permission-mode plan: no edits) at the SAME reasoning
# effort as the calling session, via the $CLAUDE_EFFORT env var (confirmed
# live and inherited by child processes — see advisor/SKILL.md for how it
# was verified). This is the fallback for when the native advisor() tool is
# unavailable; unlike that tool, this spawns an ISOLATED session with no
# automatic access to the calling conversation, so the caller must compose
# a self-contained briefing and pass it as --prompt-file. See SKILL.md.
#
# Usage:
#   fable-advisor.sh --prompt-file FILE --out FILE [-C DIR] [--model ID]
#                     [--effort LEVEL] [--timeout SEC]
#   fable-advisor.sh --check
#
#   --prompt-file FILE  the self-contained briefing (task, progress, question)
#   --out FILE          where Fable's advice is written
#   -C DIR              working dir Fable sees (default: $PWD)
#   --model ID          model alias or full name (default: fable)
#   --effort LEVEL      low|medium|high|xhigh|max (default: $CLAUDE_EFFORT if
#                        set, else "high" — never silently guess higher)
#   --timeout SEC        hard kill after SEC seconds (default: 900)
set -euo pipefail

MODEL="fable"
WORKDIR="$PWD"
PROMPT_FILE=""
OUT=""
EFFORT="${CLAUDE_EFFORT:-high}"
TIMEOUT_SECONDS=900

usage() {
  printf '%s\n' \
    'Usage: fable-advisor.sh --prompt-file FILE --out FILE [-C DIR] [--model ID] [--effort LEVEL] [--timeout SEC]' \
    '       fable-advisor.sh --check'
}

die() { printf 'fable-advisor: %s\n' "$*" >&2; exit 2; }

if [[ "${1:-}" == "--check" ]]; then
  command -v claude >/dev/null || die 'Claude Code CLI not found'
  claude --version
  printf 'CLAUDE_EFFORT=%s\n' "${CLAUDE_EFFORT:-<unset>}"
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

command -v claude >/dev/null || die 'Claude Code CLI not found'
[[ -n "$PROMPT_FILE" && -r "$PROMPT_FILE" ]] || die 'readable --prompt-file is required (the self-contained briefing)'
[[ -n "$OUT" ]] || die '--out is required'
[[ -d "$WORKDIR" ]] || die "working directory not found: $WORKDIR"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || die '--timeout must be a positive integer'
case "$EFFORT" in low|medium|high|xhigh|max) ;; *) die "bad --effort: $EFFORT (low|medium|high|xhigh|max)" ;; esac
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
WORKDIR="$(cd "$WORKDIR" && pwd -P)"
mkdir -p "$(dirname "$OUT")"

# ANTHROPIC_API_KEY= : force subscription billing for the spawned session even
# if the caller's shell happens to export a live API key (it would otherwise
# be inherited and silently switch this consult to API billing).
cmd=(env ANTHROPIC_API_KEY= claude --safe-mode -p --model "$MODEL" --effort "$EFFORT" --permission-mode plan --output-format text --no-session-persistence \
  'You are consulted as an independent, stronger second reviewer for one specific decision point — not a co-implementer. Read the self-contained briefing supplied on stdin (the task, what has been done so far, the current approach or findings, and the specific question). You have no access to the original conversation beyond this briefing, so if it seems to be missing something you need, say what is missing rather than guessing. Give direct, decisive advice on the specific question asked. If you disagree with the stated approach, say so plainly and explain the specific failure mode, do not hedge into a survey of options. Do not edit any files — you are read-only advisory only. Return only your advice, no preamble.')

if command -v timeout >/dev/null; then
  (cd "$WORKDIR" && timeout "${TIMEOUT_SECONDS}s" "${cmd[@]}" < "$PROMPT_FILE" > "$OUT")
else
  (cd "$WORKDIR" && "${cmd[@]}" < "$PROMPT_FILE" > "$OUT")
fi

[[ -s "$OUT" ]] || die 'Fable returned no output'
