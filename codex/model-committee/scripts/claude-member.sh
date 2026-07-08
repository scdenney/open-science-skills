#!/usr/bin/env bash
set -euo pipefail

MODEL="claude-opus-4-8"
WORKDIR="$PWD"
PROMPT_FILE=""
OUT=""
TIMEOUT_SECONDS=900

usage() {
  printf '%s\n' \
    'Usage: claude-member.sh --prompt-file FILE --out FILE [-C DIR] [--model ID] [--timeout SEC]' \
    '       claude-member.sh --check'
}

die() { printf 'claude-member: %s\n' "$*" >&2; exit 2; }

if [[ "${1:-}" == "--check" ]]; then
  command -v claude >/dev/null || die 'Claude Code CLI not found'
  claude --version
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt-file) PROMPT_FILE="${2:-}"; shift 2 ;;
    --out) OUT="${2:-}"; shift 2 ;;
    -C) WORKDIR="${2:-}"; shift 2 ;;
    --model) MODEL="${2:-}"; shift 2 ;;
    --timeout) TIMEOUT_SECONDS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

command -v claude >/dev/null || die 'Claude Code CLI not found'
[[ -n "$PROMPT_FILE" && -r "$PROMPT_FILE" ]] || die 'readable --prompt-file is required'
[[ -n "$OUT" ]] || die '--out is required'
[[ -d "$WORKDIR" ]] || die "working directory not found: $WORKDIR"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || die '--timeout must be a positive integer'
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
WORKDIR="$(cd "$WORKDIR" && pwd -P)"
mkdir -p "$(dirname "$OUT")"

cmd=(claude --safe-mode -p --model "$MODEL" --permission-mode plan --output-format text --no-session-persistence 'Follow the complete committee instructions supplied on stdin. Return only the requested structured response.')

if command -v timeout >/dev/null; then
  (cd "$WORKDIR" && timeout "${TIMEOUT_SECONDS}s" "${cmd[@]}" < "$PROMPT_FILE" > "$OUT")
else
  (cd "$WORKDIR" && "${cmd[@]}" < "$PROMPT_FILE" > "$OUT")
fi

[[ -s "$OUT" ]] || die 'model returned no final message'
