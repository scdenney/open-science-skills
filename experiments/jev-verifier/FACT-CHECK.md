# Optional Jev verification for fact-check

This experimental, opt-in, one-pair second look follows the ordinary
`fact-check` workflow. It is not web fact-checking or source evidence: the lead
reads the local source, retains exact quotations and explanations, and preserves
the ordinary report verdict. An audit that finds errors can be complete.

## Use and disclosure

Invoking `fact-check` with `--verify <task>` or `--verify jev <task>` requests
Jev; plain `fact-check` is unchanged. Each library states its own invocation
syntax; this runtime is shared. Resolve the bundle from `JEV_VERIFIER_HOME` or
`~/.local/share/oss-experiments/jev-verifier/current`, set `JEV_VERIFY` to
`<bundle>/tools/jev/verify.py`, read `tools/jev/README.md`, current
`tools/jev/contracts/fact-check.json`, and
`tools/jev/samples/fact-check-manifest.json`, then run:

```sh
python3 "$JEV_VERIFY" doctor --contract fact-check
```

Before live use, disclose that selected claim/source fields and small selected,
hash-verified excerpts go to `https://api.typesafe.ai/v1/systemone`. This opt-in
does not authorize a private corpus, source-file, or transcript scan. Use
`TYPESAFE_API_KEY` only from the environment; never ask for, print, or write it.

## Lead-first checkpoint

Run fact-check pre-flight before **any** Jev action, then run citation-check first
and carry its findings forward. One invocation covers one claim/source pair. Do
not duplicate claim-support verification in citation-check; where it resolved
identity, refer to the same audit. A prior result may be manually reused only for
the same complete evaluation input and model/contract version.

Record the lead's actual report label before verification. Create a fresh state
and output from `tools/jev/samples/fact-check-manifest.json`: it binds one claim,
source type, applicability flags, a source quotation with enough context, citation
integrity, evidence sufficiency, and blind baseline. A summary can support a coarse
claim; set sufficiency from the selected evidence, not source type alone. The
runtime checks local hashes but sends no local paths or blind baseline.

Do not call Jev for failed pre-flight, absent KB, invalid/unchecked citation
integrity, or insufficient/unchecked evidence. Report that requested check as
blocked, not verified.

```sh
python3 "$JEV_VERIFY" verify --contract fact-check --state "$STATE" \
  --out "$RESULT" --mode shadow --allow-network
```

Shadow is default: save the lead decision before reading Jev. `--mode advisory`
requires the user's explicit request and still leaves final adjudication with the
lead. Mocks are simulations, never live verification. Missing credentials,
unhealthy runtime, malformed state, or service failure is blocked, never fake
verification. Jev returns an advisory (`SUPPORTED`, `CONTRADICTED`,
`REVIEW_REQUIRED`, `NOT_CHECKED`, or invalid-citation outcome), never a report
replacement; low support is not contradiction without contrary source evidence.
