#!/usr/bin/env bash
# codex-peer.sh — invoke Codex (GPT-5 family) as a peer engineer for /fable-orchestrate.
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
#   codex-peer.sh [--mode consult|implement] [-C DIR] [--timeout SEC]
#                 [--out FILE] (--prompt TEXT | --prompt-file PATH | -)
#
#   -C DIR          working dir Codex sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --out FILE      also tee Codex's stdout+stderr here (for background reads)
#   --prompt TEXT   prompt as a single argument
#   --prompt-file P read prompt from file P
#   -               read prompt from stdin (the wrapper handles the /dev/null dance)
set -euo pipefail

MODE="consult"; DIR="$PWD"; TIMEOUT=600; OUT=""; PROMPT=""; PROMPT_SET=0

die(){ echo "codex-peer: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --mode)        MODE="${2:?}"; shift 2 ;;
    -C|--dir)      DIR="${2:?}"; shift 2 ;;
    --timeout)     TIMEOUT="${2:?}"; shift 2 ;;
    --out)         OUT="${2:?}"; shift 2 ;;
    --prompt)      PROMPT="${2:?}"; PROMPT_SET=1; shift 2 ;;
    --prompt-file) PROMPT="$(cat "${2:?}")"; PROMPT_SET=1; shift 2 ;;
    -)             PROMPT="$(cat)"; PROMPT_SET=1; shift ;;   # read stdin NOW, before codex runs
    -h|--help)     sed -n '2,33p' "$0"; exit 0 ;;
    *)             die "unknown arg: $1 (see --help)" ;;
  esac
done

[ "$PROMPT_SET" = 1 ] || die "no prompt (use --prompt, --prompt-file, or -)"
[ -n "$PROMPT" ] || die "empty prompt"
[ -d "$DIR" ] || die "no such dir: $DIR"
command -v codex >/dev/null || die "codex CLI not on PATH — install it first"

case "$MODE" in
  consult)   SANDBOX="read-only" ;;
  implement) SANDBOX="workspace-write" ;;
  *)         die "bad --mode: $MODE (consult|implement)" ;;
esac

run(){
  # `< /dev/null` is mandatory: prompt is already captured above; feeding
  # /dev/null gives codex an immediate EOF on stdin so it does not block.
  timeout "${TIMEOUT}s" codex exec \
    --sandbox "$SANDBOX" \
    --skip-git-repo-check \
    -C "$DIR" \
    "$PROMPT" < /dev/null
}

if [ -n "$OUT" ]; then
  run 2>&1 | tee "$OUT"
else
  run
fi
