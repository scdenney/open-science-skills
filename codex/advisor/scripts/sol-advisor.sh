#!/usr/bin/env bash
# sol-advisor.sh — legacy entrypoint for a separate Astra advisory session.
# Defaults: gpt-6-astra, xhigh, read-only, ephemeral. Model and effort are overridable.
# Supply a self-contained brief; the child has no automatic parent conversation.
# Parent sandbox and network permissions still apply to nested calls.
# Requires Python 3 to enforce the timeout on macOS and Linux.
# Usage: sol-advisor.sh --prompt-file FILE --out NEW_FILE [-C DIR]
#                      [--model ID] [--effort LEVEL] [--timeout SEC]
#        sol-advisor.sh --check
set -euo pipefail

# Python is already required by the library; enforce deadlines on macOS and Linux.
run_with_timeout() {
  python3 -c '
import os, signal, subprocess, sys
seconds = int(sys.argv[1])
process = subprocess.Popen(sys.argv[2:], start_new_session=True)
try:
    code = process.wait(timeout=seconds)
except subprocess.TimeoutExpired:
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()
    sys.exit(124)
sys.exit(code if code >= 0 else 128 - code)
' "$@"
}


MODEL="gpt-6-astra"
WORKDIR="$PWD"
PROMPT_FILE=""
OUT=""
EFFORT="xhigh"
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
case "$EFFORT" in none|low|medium|high|xhigh|max) ;; *) die "bad --effort: $EFFORT" ;; esac
[[ "$MODEL" != gpt-6-astra || "$EFFORT" != none ]] || die 'Astra does not support effort none'
command -v python3 >/dev/null || die 'python3 is required to enforce --timeout'
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
WORKDIR="$(cd "$WORKDIR" && pwd -P)"
[[ ! -e "$OUT" && ! -L "$OUT" ]] || die "output already exists: $OUT"
mkdir -p "$(dirname "$OUT")"
RESULT_DIR="$(mktemp -d "$(dirname "$OUT")/.codex-result.XXXXXX")"
trap 'rm -rf "$RESULT_DIR"' EXIT
RESULT="$RESULT_DIR/answer.md"

cmd=(codex exec --ephemeral --model "$MODEL" -c model_reasoning_effort="$EFFORT" --sandbox read-only --skip-git-repo-check -C "$WORKDIR" --output-last-message "$RESULT" \
  'You are consulted as an independent advisor for one specific decision point — not a co-implementer. Read the self-contained briefing supplied on stdin (the task, what has been done so far, the current approach or findings, and the specific question). You have no access to the original conversation beyond this briefing, so if it seems to be missing something you need, say what is missing rather than guessing. Give direct, decisive advice on the specific question asked. If you disagree with the stated approach, say so plainly and explain the specific failure mode, do not hedge into a survey of options. Do not edit any files — you are read-only advisory only. Return only your advice, no preamble.')

run_with_timeout "$TIMEOUT_SECONDS" "${cmd[@]}" < "$PROMPT_FILE" >/dev/null

[[ -s "$RESULT" ]] || die 'model returned no final message'
# link(2) fails if another run has claimed OUT, preserving that run's result.
python3 -c 'import os, sys; os.link(sys.argv[1], sys.argv[2])' "$RESULT" "$OUT" || die "cannot publish output without replacing an existing file: $OUT"
