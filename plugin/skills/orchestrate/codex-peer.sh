#!/usr/bin/env bash
# codex-peer.sh — invoke Codex (GPT-6 Astra) as a peer engineer for /orchestrate.
#
# Codex is a different-vendor peer, not a reviewer. Use it two ways:
#   consult   (default) — read-only. Ask a question / get a second approach. Prints the answer.
#   implement           — workspace-write. Let Codex edit files in a directory.
#
# VERIFIED pattern (this is the whole reason the wrapper exists):
#   codex exec --sandbox <mode> --skip-git-repo-check -C <dir> "<prompt>" < /dev/null
# The `< /dev/null` is LOAD-BEARING: without it, codex exec prints
# "Reading additional input from stdin..." and hangs forever even when the
# prompt is passed as an argument. `timeout` is a second backstop.
#
# The orchestrator runs this via the Bash tool with run_in_background:true so a
# long Codex turn does not block the loop — then reads the --out file when the
# task-notification fires. For the high-stakes path, launch this AND a
# deep-reasoner (Opus) subagent on the SAME prompt in one message, blind to
# each other, then synthesize.
#
# Usage:
#   codex-peer.sh [--mode consult|cross-check|implement] [-C DIR] [--timeout SEC]
#                 [--model ID] [--out FILE] (--prompt TEXT | --prompt-file PATH | -)
#
#   --mode          consult     read-only, a routine fresh-perspective consult   (default effort: high)
#                   cross-check read-only, the blind high-stakes cross-check     (default effort: xhigh)
#                   implement   workspace-write                                  (default effort: xhigh)
#   -C DIR          working dir Codex sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --model ID      default: gpt-6-astra; use gpt-5.6-terra for bounded routine work
#   --effort LEVEL  low|medium|high|xhigh|max for Astra; overrides the mode default above
#   --out FILE      also tee Codex's stdout+stderr here (for background reads)
#   --prompt TEXT   prompt as a single argument
#   --prompt-file P read prompt from file P
#   -               read prompt from stdin (the wrapper handles the /dev/null dance)
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


MODE="consult"; DIR="$PWD"; TIMEOUT=600; MODEL="gpt-6-astra"; EFFORT=""; OUT=""; PROMPT=""; PROMPT_SET=0

die(){ echo "codex-peer: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --mode)        MODE="${2:?}"; shift 2 ;;
    -C|--dir)      DIR="${2:?}"; shift 2 ;;
    --timeout)     TIMEOUT="${2:?}"; shift 2 ;;
    --model)       MODEL="${2:?}"; shift 2 ;;
    --effort)      EFFORT="${2:?}"; shift 2 ;;
    --out)         OUT="${2:?}"; shift 2 ;;
    --prompt)      PROMPT="${2:?}"; PROMPT_SET=1; shift 2 ;;
    --prompt-file) PROMPT="$(cat "${2:?}")"; PROMPT_SET=1; shift 2 ;;
    -)             PROMPT="$(cat)"; PROMPT_SET=1; shift ;;   # read stdin NOW, before codex runs
    -h|--help)     sed -n '2,/^set -euo pipefail/{ /^set -euo pipefail/!p; }' "$0"; exit 0 ;;
    *)             die "unknown arg: $1 (see --help)" ;;
  esac
done

[ "$PROMPT_SET" = 1 ] || die "no prompt (use --prompt, --prompt-file, or -)"
[ -n "$PROMPT" ] || die "empty prompt"
[[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]] || die '--timeout must be a positive integer'
command -v python3 >/dev/null || die 'python3 is required to enforce --timeout'
[ -d "$DIR" ] || die "no such dir: $DIR"
command -v codex >/dev/null || die "codex CLI not on PATH — install it first"

# The mode sets the sandbox and the default effort: a routine consult runs at
# `high`; the blind high-stakes cross-check and any write-capable run at `xhigh`.
# --effort overrides the default for one call.
case "$MODE" in
  consult)     SANDBOX="read-only";       DEFAULT_EFFORT="high" ;;
  cross-check) SANDBOX="read-only";       DEFAULT_EFFORT="xhigh" ;;
  implement)   SANDBOX="workspace-write"; DEFAULT_EFFORT="xhigh" ;;
  *)           die "bad --mode: $MODE (consult|cross-check|implement)" ;;
esac
EFFORT="${EFFORT:-$DEFAULT_EFFORT}"
case "$EFFORT" in none|low|medium|high|xhigh|max) ;; *) die "bad --effort: $EFFORT" ;; esac
[[ "$MODEL" != gpt-6-astra || "$EFFORT" != none ]] || die 'Astra does not support effort none'

run(){
  # `< /dev/null` is mandatory: prompt is already captured above; feeding
  # /dev/null gives codex an immediate EOF on stdin so it does not block.
  local cmd=(codex exec --model "$MODEL" -c "model_reasoning_effort=$EFFORT" --sandbox "$SANDBOX" --skip-git-repo-check -C "$DIR" "$PROMPT")
  run_with_timeout "$TIMEOUT" "${cmd[@]}" < /dev/null
}

if [ -n "$OUT" ]; then
  mkdir -p "$(dirname "$OUT")"
  (set -o noclobber; : > "$OUT") || die "output already exists or cannot be created: $OUT"
  run 2>&1 | tee -a "$OUT"
else
  run
fi
