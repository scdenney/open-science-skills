# Optional Jev verification for citation-check

This experimental opt-in path is a one-entry, lead-first check of ambiguity in an
actually fetched record. It does not replace citation inventory, provider lookups,
DOI resolution, existence/fabrication checks, or style checks.

## Use and disclosure

Invoking `citation-check` with `--verify <task>` or `--verify jev <task>`
requests Jev; plain `citation-check` is unchanged. Each library states its own
invocation syntax; this runtime is shared. Resolve the bundle from
`JEV_VERIFIER_HOME` or `~/.local/share/oss-experiments/jev-verifier/current` and
set `JEV_VERIFY` to `<bundle>/tools/jev/verify.py`. Read `tools/jev/README.md`,
current `tools/jev/contracts/citation-check.json`, and
`tools/jev/samples/citation-check-manifest.json`, then run:

```sh
python3 "$JEV_VERIFY" doctor --contract citation-check
```

Before live use, disclose that the bounded entry, fetched metadata, and selected
hash-verified excerpts go to `https://api.typesafe.ai/v1/systemone`. This opt-in
does not authorize a broad bibliography, corpus, or transcript scan. Use
`TYPESAFE_API_KEY` only from the environment; never solicit or write it.

## Lead-first checkpoint

Use Jev only after a successful actual fetched record leaves identity or version
relationship ambiguous. Do not infer existence or fabrication from model
knowledge. A prior result may be manually reused only for the same complete
evaluation input and model/contract version; no automatic cache or batch exists.

Create a fresh state and output from
`tools/jev/samples/citation-check-manifest.json`. It records one rendered entry,
retrieved record with hash-verified excerpt, deterministic identity finding, and
blind lead baseline. `different_work` remains the deterministic `DIFFERENT_WORK`
outcome; `match` with successful evidence is verified; only genuine ambiguity
reaches Jev. A DOI difference alone may be a preprint/publication relationship,
not a wrong work. `NOT CHECKED` remains `NOT CHECKED`.

```sh
python3 "$JEV_VERIFY" verify --contract citation-check --state "$STATE" \
  --out "$RESULT" --mode shadow --allow-network
```

Shadow is default: record the lead's report status before reading Jev. `--mode
advisory` requires an explicit user request; the lead still adjudicates from
fetched evidence. Mocks are simulations, never live verification. Missing key,
runtime, malformed state, or service means blocked/not checked, never a fabricated
verification. Treat any Jev result as an advisory annotation, never automatic
report evidence or a replacement for existing report labels.
