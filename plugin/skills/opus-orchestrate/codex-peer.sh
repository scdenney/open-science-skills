#!/usr/bin/env bash
# codex-peer.sh — invoke Codex (GPT-5.6 "Sol") as a peer engineer for /opus-orchestrate.
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
#                 [--model ID] [--out FILE] (--prompt TEXT | --prompt-file PATH | -)
#
#   -C DIR          working dir Codex sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --model ID      Codex model to pin (default: gpt-5.6-sol — the flagship
#                   5.6 tier, confirmed working as of July 2026 on
#                   ChatGPT-account Codex auth; an earlier "rejected outright"
#                   finding no longer reproduces — if it ever errors, check
#                   `codex --version` before assuming a gate, since an
#                   outdated CLI rejects sol/luna too, with a different
#                   error). There are three distinct 5.6 tiers, not one
#                   model: gpt-5.6-sol (flagship), gpt-5.6-terra (balanced),
#                   gpt-5.6-luna (fast). Pass --model gpt-5.6-terra for a
#                   cheaper peer on routine consults.
#   --effort LEVEL  Codex reasoning effort, passed as
#                   -c model_reasoning_effort=LEVEL (default: xhigh — Sol's
#                   "Extra high" tier, one below Max/Ultra, which consume
#                   usage limits faster; stated explicitly so it does not
#                   silently drift if Codex's own defaults change upstream).
#   --out FILE      also tee Codex's stdout+stderr here (for background reads)
#   --prompt TEXT   prompt as a single argument
#   --prompt-file P read prompt from file P
#   -               read prompt from stdin (the wrapper handles the /dev/null dance)
set -euo pipefail

MODE="consult"; DIR="$PWD"; TIMEOUT=600; MODEL="gpt-5.6-sol"; EFFORT="xhigh"; OUT=""; PROMPT=""; PROMPT_SET=0

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
    -h|--help)     sed -n '2,45p' "$0"; exit 0 ;;
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
  local cmd=(codex exec --model "$MODEL" -c "model_reasoning_effort=$EFFORT" --sandbox "$SANDBOX" --skip-git-repo-check -C "$DIR" "$PROMPT")
  # `timeout` is not preinstalled on macOS (only via GNU coreutils) — guard
  # rather than assume, matching model-committee-sol's claude-member.sh /
  # codex-member.sh, which already learned this the hard way.
  if command -v timeout >/dev/null; then
    timeout "${TIMEOUT}s" "${cmd[@]}" < /dev/null
  else
    "${cmd[@]}" < /dev/null
  fi
}

if [ -n "$OUT" ]; then
  run 2>&1 | tee "$OUT"
else
  run
fi
