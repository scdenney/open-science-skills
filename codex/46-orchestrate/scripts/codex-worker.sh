#!/usr/bin/env bash
# codex-worker.sh — spawn a tier-pinned Codex subagent for /46-orchestrate.
#
# The lead of $46-orchestrate ("Sol") is the currently-running Codex session
# itself; it is NOT spawned via this script. This script exists only to pin
# a model to SUBAGENTS, since Codex's native in-process subagent tool
# (built-in explorer/worker/default types) has no way in this repo's
# experience to pin a model per call. Shelling out via `codex exec --model`
# is the proven mechanism (see plugin/skills/fable-orchestrate/codex-peer.sh
# and codex/advisor/scripts/sol-advisor.sh, which use the identical pattern).
#
# Two roles, three tiers:
#   consult   (default) — read-only. Analyst / verifier work: inspect,
#                          diagnose, adversarial review, high-stakes cross-check.
#   implement            — workspace-write. Implementer role: fully-specified
#                          work with objective acceptance checks, bounded edits.
#
# Tiers (--tier {luna,terra,sol}, maps to gpt-5.6-<tier>):
#   terra (default) — balanced. Use for analyst/verifier consult calls.
#   luna            — fast/cheap. Use for implementer calls (the actual
#                     token-saving tier).
#   sol             — flagship. Confirmed working (smoke-tested directly,
#                     July 2026) on both hosts this repo runs on. Some
#                     ChatGPT-based Codex auth setups have rejected it in the
#                     past ("not supported when using Codex with a ChatGPT
#                     account") — if you hit that error on your own account,
#                     fall back to terra. Not the default (terra is cheaper
#                     for routine consults) but a real option, not a gated one.
#
# EFFORT MATTERS AS MUCH AS TIER — do not skip --effort. If the caller's own
# ~/.codex/config.toml sets a global model_reasoning_effort (e.g. "max" for
# an interactive Sol-max session), `codex exec` on a spawned subagent
# INHERITS that same global default unless overridden here with `-c
# model_reasoning_effort=...`. A cheap tier (luna) run at an inherited "max"
# effort is not cheap — this was confirmed empirically: a terra call with no
# --effort flag came back reporting "reasoning effort: max" on a host whose
# config.toml pinned max globally. Pass --effort explicitly (or rely on the
# tier-based default below) so delegation actually saves tokens instead of
# silently running every subagent at the lead's own effort level.
#
# Tier-based --effort default when not passed explicitly: luna -> low,
# terra -> medium, sol -> high. Override with --effort none|minimal|low|
# medium|high|xhigh for a specific call.
#
# VERIFIED pattern (this is the whole reason the wrapper exists):
#   codex exec --model <id> --sandbox <mode> --skip-git-repo-check -C <dir> "<prompt>" < /dev/null
# The `< /dev/null` is LOAD-BEARING: without it, codex exec prints
# "Reading additional input from stdin..." and hangs forever even when the
# prompt is passed as an argument. `timeout` is a second backstop.
#
# The lead should run this via a backgroundable shell invocation
# (e.g. run_in_background:true, or `&` plus a PID wait) for long tier calls,
# so a multi-minute Codex turn never blocks the orchestration loop — then
# read the --out file once the call completes. For the two-independent-check
# high-stakes path, launch two `--tier terra` calls on the SAME prompt in one
# round, blind to each other, then reconcile.
#
# Usage:
#   codex-worker.sh [--mode consult|implement] [--tier luna|terra|sol]
#                    [--effort none|minimal|low|medium|high|xhigh]
#                    [-C DIR] [--timeout SEC] [--out FILE]
#                    (--prompt TEXT | --prompt-file PATH | -)
#
#   --mode MODE     consult (read-only) | implement (workspace-write). Default: consult.
#   --tier TIER     luna | terra | sol -> maps to gpt-5.6-<tier>. Default: terra.
#   --effort LEVEL  none|minimal|low|medium|high|xhigh. Default: tier-based
#                    (luna->low, terra->medium, sol->high). ALWAYS set
#                    explicitly via `-c model_reasoning_effort=` — never left
#                    to inherit the caller's own config.toml default.
#   -C DIR          working dir Codex sees (default: $PWD)
#   --timeout SEC   hard kill after SEC seconds (default: 600)
#   --out FILE      also tee Codex's stdout+stderr here (for background reads)
#   --prompt TEXT   prompt as a single argument
#   --prompt-file P read prompt from file P
#   -               read prompt from stdin (the wrapper handles the /dev/null dance)
set -euo pipefail

MODE="consult"; TIER="terra"; EFFORT=""; DIR="$PWD"; TIMEOUT=600; OUT=""; PROMPT=""; PROMPT_SET=0

die(){ echo "codex-worker: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --mode)        MODE="${2:?}"; shift 2 ;;
    --tier)        TIER="${2:?}"; shift 2 ;;
    --effort)      EFFORT="${2:?}"; shift 2 ;;
    -C|--dir)      DIR="${2:?}"; shift 2 ;;
    --timeout)     TIMEOUT="${2:?}"; shift 2 ;;
    --out)         OUT="${2:?}"; shift 2 ;;
    --prompt)      PROMPT="${2:?}"; PROMPT_SET=1; shift 2 ;;
    --prompt-file) PROMPT="$(cat "${2:?}")"; PROMPT_SET=1; shift 2 ;;
    -)             PROMPT="$(cat)"; PROMPT_SET=1; shift ;;   # read stdin NOW, before codex runs
    -h|--help)     sed -n '2,58p' "$0"; exit 0 ;;
    *)             die "unknown arg: $1 (see --help)" ;;
  esac
done

[ "$PROMPT_SET" = 1 ] || die "no prompt (use --prompt, --prompt-file, or -)"
[ -n "$PROMPT" ] || die "empty prompt"
[ -d "$DIR" ] || die "no such dir: $DIR"
command -v codex >/dev/null || die "codex CLI not on PATH — install it first"

case "$TIER" in
  luna)  MODEL="gpt-5.6-luna";  [ -n "$EFFORT" ] || EFFORT="low" ;;
  terra) MODEL="gpt-5.6-terra"; [ -n "$EFFORT" ] || EFFORT="medium" ;;
  sol)   MODEL="gpt-5.6-sol";   [ -n "$EFFORT" ] || EFFORT="high" ;;
  *)     die "bad --tier: $TIER (luna|terra|sol)" ;;
esac

case "$EFFORT" in
  none|minimal|low|medium|high|xhigh) ;;
  *) die "bad --effort: $EFFORT (none|minimal|low|medium|high|xhigh)" ;;
esac

case "$MODE" in
  consult)   SANDBOX="read-only" ;;
  implement) SANDBOX="workspace-write" ;;
  *)         die "bad --mode: $MODE (consult|implement)" ;;
esac

run(){
  # `< /dev/null` is mandatory: prompt is already captured above; feeding
  # /dev/null gives codex an immediate EOF on stdin so it does not block.
  # `-c model_reasoning_effort=` is equally mandatory: without it, this
  # subagent silently inherits the CALLER's global config.toml effort
  # (which may be "max" for an interactive Sol-max lead session), and the
  # cheap tier stops being cheap.
  local cmd=(codex exec --model "$MODEL" -c model_reasoning_effort="$EFFORT" --sandbox "$SANDBOX" --skip-git-repo-check -C "$DIR" "$PROMPT")
  # `timeout` is not preinstalled on macOS (only via GNU coreutils) — guard
  # rather than assume, matching codex-peer.sh / sol-advisor.sh, which
  # already learned this the hard way.
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
