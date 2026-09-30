# Optional verification for orchestrate

This is a shared runtime reference, not a separate skill. The active `orchestrate` skill remains authoritative for lead-runtime checks, delegation, routing, integration, and completion.

This file covers completion verification only. The separate, experimental `--route` path has its own contract, state schema, result schema, and checkpoint in `ROUTE.md`; the two are composable but never interchangeable, and a routing recommendation does not satisfy a completion check.

## Activation and setup

- Invoking `orchestrate` with `--verify <task>` selects Jev by default.
- `--verify jev <task>` means exactly the same thing.
- Plain `orchestrate`, with neither option, does not load or call Jev. Mentioning these examples while discussing the interface is not itself a request to verify a task.
- Each library states its own invocation syntax; this runtime is shared and does not prefer one.
- Parse `--route`, `--verify`, optional provider names, `--model`, and `--effort` from the invocation prefix before the task; for example, `--route --verify <task>` enables both against the same task. Only a literal `jev` immediately following a provider option is consumed as a provider name. No other provider is supported in this prototype.

Resolve the bundle from `JEV_VERIFIER_HOME` if set, otherwise `~/.local/share/oss-experiments/jev-verifier/current`. Set `JEV_VERIFY` to its `tools/jev/verify.py`. Read the bundled `tools/jev/README.md` and `tools/jev/contracts/orchestrate.json` before preparing evidence. Run `python3 "$JEV_VERIFY" doctor`; stop the verification path and report missing/unhealthy runtime or missing `TYPESAFE_API_KEY`. Never silently fall back to mock verification. The ordinary work may continue if appropriate, but report the requested Jev check as blocked, not passed.

Both activation forms request live verification. Before calling, disclose that the selected task requirements, worker claim, observations, and deliberately selected artifact excerpts/hashes go to `https://api.typesafe.ai/v1/systemone`. Use only task-relevant evidence; do not scan/export whole transcripts or unrelated files. Credentials come from the environment, not the manifest or prompt.

## Checkpoints

At each substantive worker return, inspect its artifacts and create a worker checkpoint before integration. Make a separate final checkpoint after the lead's integrated checks. For each checkpoint:

1. Record the lead's own `PASS`, `REWORK`, or `ESCALATE` judgment and rationale before seeing Jev's assessment.
2. Prepare an evidence manifest using the runtime schema and bundled samples. Include the actual objective, acceptance criteria, scope constraints, worker claim, blind lead label, and selected artifact evidence. Hashes and excerpts must match the actual files. Mark an unperformed check `not_checked`, never `pass`.
3. Choose a fresh result path and run:

```bash
python3 "$JEV_VERIFY" verify --contract orchestrate \
  --state "$STATE" --out "$RESULT" --mode shadow --allow-network
```

4. Read the result only after recording the lead baseline. Report disagreements and whether the API call actually succeeded. A simulated or failed call is not live verification.

## Judgment and limits

Shadow is the default: Jev is an observer and does not automatically change the lead's recorded judgment, approve completion, repair artifacts, retry work, or reroute agents. Use `--mode advisory` only when the user explicitly asks; the lead still adjudicates against actual evidence and owns the decision.

Deterministic failures and missing checks cannot be overruled by positive Jev scores. Thresholds are experimental and uncalibrated. The lead's baseline is not human ground truth.

Offline tests may explicitly use `--mock-response` instead of `--allow-network`, but must be described as simulations. Keep worker evidence, baseline judgment, Jev result, and final integrated evidence distinct in the handoff. Report verification as blocked if credentials or the service are unavailable.
