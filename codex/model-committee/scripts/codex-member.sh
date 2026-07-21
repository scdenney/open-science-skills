#!/usr/bin/env bash
# SANDBOX WARNING (confirmed by direct reproduction, July 2026): this script
# nests a `codex exec` process inside whatever process runs it. If the
# CALLER is itself a sandboxed `codex exec`/Codex session, this nested call
# fails immediately with "failed to initialize in-process app-server
# client: Operation not permitted" (macOS) or "Read-only file system"
# (Linux) -- an OS-level sandbox applies transitively to the whole process
# tree, and bypass flags on THIS call do not help, since the restriction is
# imposed on the parent, not requested by the child. Only an unsandboxed
# caller, or an interactive caller that requests escalation
# (sandbox_permissions: require_escalated) for this specific call, can
# succeed. See SKILL.md's "Sandbox constraint" section.
set -euo pipefail

MODEL="gpt-5.6-sol"
EFFORT="xhigh"
WORKDIR="$PWD"
PROMPT_FILE=""
OUT=""
TIMEOUT_SECONDS=900

usage() {
  printf '%s\n' \
    'Usage: codex-member.sh --prompt-file FILE --out FILE [-C DIR] [--model ID] [--effort LEVEL] [--timeout SEC]' \
    '       codex-member.sh --check'
}

die() { printf 'codex-member: %s\n' "$*" >&2; exit 2; }

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
[[ -n "$PROMPT_FILE" && -r "$PROMPT_FILE" ]] || die 'readable --prompt-file is required'
[[ -n "$OUT" ]] || die '--out is required'
[[ -d "$WORKDIR" ]] || die "working directory not found: $WORKDIR"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || die '--timeout must be a positive integer'
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
WORKDIR="$(cd "$WORKDIR" && pwd -P)"
mkdir -p "$(dirname "$OUT")"

cmd=(codex exec --ephemeral --model "$MODEL" -c "model_reasoning_effort=$EFFORT" --sandbox read-only --skip-git-repo-check -C "$WORKDIR" --output-last-message "$OUT" 'Follow the complete committee instructions supplied on stdin. Return only the requested structured response.')

if command -v timeout >/dev/null; then
  timeout "${TIMEOUT_SECONDS}s" "${cmd[@]}" < "$PROMPT_FILE" >/dev/null
else
  "${cmd[@]}" < "$PROMPT_FILE" >/dev/null
fi

[[ -s "$OUT" ]] || die 'model returned no final message'
