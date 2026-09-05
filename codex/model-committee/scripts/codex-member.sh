#!/usr/bin/env bash
# Separate read-only CLI session; parent sandbox and network permissions apply.
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

cmd=(codex exec --ephemeral --model "$MODEL" -c "model_reasoning_effort=$EFFORT" --sandbox read-only --skip-git-repo-check -C "$WORKDIR" --output-last-message "$RESULT" 'Follow the complete committee instructions supplied on stdin. Return only the requested structured response.')

run_with_timeout "$TIMEOUT_SECONDS" "${cmd[@]}" < "$PROMPT_FILE" >/dev/null

[[ -s "$RESULT" ]] || die 'model returned no final message'
# link(2) fails if another run has claimed OUT, preserving that run's result.
python3 -c 'import os, sys; os.link(sys.argv[1], sys.argv[2])' "$RESULT" "$OUT" || die "cannot publish output without replacing an existing file: $OUT"
