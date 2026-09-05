#!/usr/bin/env bash
# Verify the model and reasoning effort actually running the current Codex turn.
set -euo pipefail

ASTRA_MODEL="gpt-6-astra"
SOL_MODEL="gpt-5.6-sol"
CODEX_STATE_ROOT="${CODEX_HOME:-$HOME/.codex}"
THREAD_ID="${CODEX_THREAD_ID:-}"

die() {
  printf 'orchestrate preflight: %s\n' "$*" >&2
  exit 2
}

[[ -n "$THREAD_ID" ]] || die 'cannot verify the active runtime because CODEX_THREAD_ID is unset; stop and report this instead of assuming the lead model'
[[ -d "$CODEX_STATE_ROOT/sessions" ]] || die "cannot verify the active runtime because the Codex sessions directory is unavailable: $CODEX_STATE_ROOT/sessions"

shopt -s nullglob
session_files=("$CODEX_STATE_ROOT"/sessions/*/*/*/*"$THREAD_ID".jsonl)
shopt -u nullglob

[[ ${#session_files[@]} -eq 1 ]] || die "expected exactly one rollout for current thread $THREAD_ID, found ${#session_files[@]}; stop rather than guessing"

python3 - "${session_files[0]}" "$ASTRA_MODEL" "$SOL_MODEL" <<'PY'
import json
import sys

session_path, astra_model, sol_model = sys.argv[1:]
allowed_models = (astra_model, sol_model)
latest = None
reroute = None

try:
    with open(session_path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(
                    f"orchestrate preflight: invalid JSON in current rollout at line {line_number}: {exc}"
                )
            if event.get("type") == "turn_context":
                latest = event.get("payload") or {}
                reroute = None
            elif (
                event.get("type") == "model_reroute"
                or (
                    event.get("type") == "event_msg"
                    and (event.get("payload") or {}).get("type") == "model_reroute"
                )
            ):
                reroute = event.get("payload") or event
except OSError as exc:
    raise SystemExit(f"orchestrate preflight: cannot read current rollout: {exc}")

if latest is None:
    raise SystemExit(
        "orchestrate preflight: current rollout has no turn_context; stop rather than guessing"
    )

if reroute is not None:
    raise SystemExit(
        "orchestrate preflight: Codex recorded a model reroute for the current turn; "
        f"details={json.dumps(reroute, sort_keys=True)}. Do not proceed as if Astra were the lead."
    )

model = latest.get("model")
effort = latest.get("effort")
if not model or not effort:
    raise SystemExit(
        "orchestrate preflight: current turn_context does not expose both model and effort; "
        "stop rather than guessing"
    )

if model not in allowed_models:
    raise SystemExit(
        "orchestrate preflight mismatch: "
        f"current runtime is {model} at {effort}; supported leads are "
        f"{astra_model} and {sol_model}. Do not proceed. Ask the operator to select "
        "Astra or Sol in /model while keeping the selected reasoning effort, verify with /status, "
        "and invoke $orchestrate again."
    )

print(f"orchestrate preflight OK: {model} at {effort}")
PY
