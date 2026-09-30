# Jev verifier prototype runtime

This is a manually invoked, advisory prototype for macOS and Linux. It is not a
hook, does not run an agent loop, and never performs network I/O unless the caller
passes `--allow-network`. The only live endpoint is the fixed HTTPS URL
`https://api.typesafe.ai/v1/systemone`; the model is pinned to `jev-1.13.0`.

## Interface

```sh
python3 verify.py doctor [--contract orchestrate|fact-check|citation-check|route]
python3 verify.py verify --contract orchestrate|fact-check|citation-check --state MANIFEST.json \
  --out NEW_RESULT.json [--mode shadow|advisory] \
  [--mock-response RESPONSE.json | --allow-network]
python3 verify.py route --state ROUTE_STATE.json \
  --out NEW_RESULT.json [--mode shadow|advisory] \
  [--mock-response RESPONSE.json | --allow-network]
python3 verify.py adjudicate --result RESULT.json --label PASS \
  --out NEW_ADJUDICATION.json
```

`route` is a separate subcommand rather than a `verify --contract`, because routing
and completion verification are different claims: separate state schema, separate
result schema, separate checkpoint. A route state cannot be read as a completion
manifest, a completion manifest cannot be read as a route state, and `adjudicate`
rejects a route result.

Live verification requires an API key. On macOS the runtime checks
`TYPESAFE_API_KEY`, then the current user's `TypeSafe Jev API` Login Keychain
item. Linux uses the environment variable, then Secret Service through
`secret-tool` (`service=typesafe-jev`, `account=<username>`). Output paths are
caller-selected and must not already exist. Result files are created mode `0600`.
Shadow mode does not print the decision. `adjudicate` records a lead's label and
the result-file hash without displaying or copying the Jev decision, so the lead
can label first and inspect the verifier result later. `adjudicate` is currently
for orchestration results only; research states carry their own hashed blind
baseline.

`--mock-response` is offline testing only. Its result has
`verification_status: "simulation"`, `live_verified: false`, and top-level
`decision: "ESCALATE"`; its hypothetical routing is only
`jev.simulated_decision`.

Research mocks likewise remain nonlive and keep
`assessment.proposed_outcome: "NOT_CHECKED"`; their hypothetical assessment is
only `jev.simulated_outcome`.

## Evidence manifest (`jev-evidence-v1`)

The JSON root has exactly seven fields: `schema_version`, `contract`, `run_id`,
`task`, `worker_claim`, `lead_decision`, and `evidence`. `task` supplies the
objective plus non-empty `acceptance_criteria` and `scope_constraints` arrays;
`worker_claim` is the bounded completion claim to assess. `lead_decision` contains exactly one `label`
(`PASS`, `REWORK`, or `ESCALATE`) recorded before verification. Its label and
canonical SHA-256 are retained for calibration, but the field is excluded from
the Jev payload to prevent anchoring. Evidence must contain each of the four checks in
`contracts/orchestrate.json` exactly once. Every entry has:

- `check_id`: one required check ID.
- `result`: `pass`, `fail`, or `not_checked`.
- `observation`: a bounded, non-empty lead-authored statement based on actual
  artifacts. It is sent to Jev but never copied into the result/audit log.
- `artifacts`: zero entries for `not_checked`; otherwise one or more objects with
  exactly `path`, `sha256`, and `excerpt`. Relative paths resolve from the manifest
  directory. The verifier reads each bounded regular file once, validates its hash,
  and requires the selected excerpt to occur in those same bytes. Paths are never
  sent to Jev; bounded excerpts are deliberately sent as substantive evidence.

Start from `samples/evidence-manifest.json`. Missing or malformed evidence can
never pass. An explicit deterministic failure yields `REWORK`; `not_checked`
yields `ESCALATE`, regardless of a positive model answer.

## Decision policy and audit minimization

The positive Noul questions are intentionally narrow. All probabilities at least
`0.80` yield `PASS`; any probability at most `0.20` yields `REWORK`; intermediate
or mixed answers yield `ESCALATE`. These prototype thresholds are **uncalibrated**
and must be validated on labeled local cases before operational use.

Result JSON contains hashes, the lead's blind baseline label, deterministic
statuses, the pinned/requested and returned model IDs, question version, latency, token usage, and Noul
probabilities. It omits artifact paths, evidence observations, source text, the
API key, and server error bodies. Schema errors, non-finite/out-of-range values,
wrong or unknown answer types, endpoint failures, redirects, and missing inputs
all produce or preserve an `ESCALATE` outcome and a sanitized reason code.

The client uses a 10-second timeout and at most three attempts. Only HTTP 429,
529, and transport failures are retried with short bounded backoff. Redirects are
refused so credentials cannot be forwarded to another endpoint.

The shared engine loads questions, required check IDs, model, thresholds, and
question version from the selected file under `contracts/`; the result records a
canonical question hash so contract changes are auditable.

## Fact-check contract (`jev-fact-check-state-v1`)

This contract evaluates one claim/source pair. The root has exactly
`schema_version`, `contract`, `run_id`, `claim`, `source`, `evidence`, and
`blind_baseline`.

- `claim`: bounded `text`; `kind` (`empirical` or `theoretical`); and boolean
  `strength_applicable`, `direction_magnitude_applicable`, and
  `omission_applicable` flags. Inapplicable dimensions do not affect the outcome.
- `source`: bounded `identity`, `kind` (`fulltext` or `summary`), and
  `knowledge_base_status` (`available` or `missing`). Summary status is not itself
  a gate; the caller declares actual adequacy separately.
- `evidence`: `readiness` (`ready` or `not_ready`), `citation_integrity`
  (`valid`, `invalid`, or `not_checked`), `sufficiency` (`sufficient`,
  `insufficient`, or `not_checked`), and zero to ten hash/excerpt artifacts.
- `blind_baseline.label`: one existing fact-check label. Only its hash is retained;
  the label is neither sent to Jev nor emitted in the result.

Not-ready research, invalid or unchecked citation integrity, a missing
knowledge-base source, insufficient/unchecked evidence, and absent passage
evidence each gate independently before any backend. These yield `NOT_CHECKED`
(or `INVALID_CITATION`), never `UNSUPPORTED` merely because a selected excerpt
omits a statement.

The configured Noul questions assess support and explicit contradiction
separately, followed by scope, strength, direction/magnitude, and material
omission. Low support is not contradiction. `CONTRADICTED` requires a strong
explicit contradiction signal; conflicting strong support and contradiction
signals require review. `SUPPORTED` requires strong support, scope, every
applicable dimension, and a low contradiction probability. All other model
patterns are `REVIEW_REQUIRED`. These are advisory categories, not fact-check
report verdicts.

## Citation-check contract (`jev-citation-check-state-v1`)

This contract compares one bibliographic entry with one retrieved record. The root
has exactly `schema_version`, `contract`, `run_id`, `bibliographic_entry`,
`retrieved_record`, and `blind_baseline`.

- `bibliographic_entry`: required bounded `rendered` text and nullable structured
  `title`, `authors`, `year`, `doi`, and `version`.
- `retrieved_record`: the same comparison fields; `deterministic_identity`
  (`match`, `different_work`, `ambiguous`, or `not_checked`); `retrieval` with
  `provider`, `url`, `retrieved_at`, and status (`success`, `not_found`, or
  `error`); and hash/excerpt-checked artifacts.
- `blind_baseline.label`: an existing citation-check label, or `AMBIGUOUS`,
  `VERIFIED`, or `NOT CHECKED`. Only its hash is retained.

The caller owns retrieval and the deterministic identity classification; this
runtime performs no provider lookup. Successful retrieval still needs hashed
evidence and structured title/author fields on both sides. `match` yields local
`VERIFIED`, `different_work` yields `DIFFERENT_WORK`, and unchecked identity,
failed retrieval, missing evidence, or missing core metadata yields `NOT_CHECKED`.
Differing DOIs alone are ambiguous because preprint and publication versions may
have different identifiers. Only `ambiguous` reaches Jev. Jev does not guess
existence, declare fabrication, or upgrade a deterministic finding.

## Route contract (`jev-route-state-v2`) — experimental

This contract proposes an execution plan for one task, before the work starts. It
is a local prototype, not a calibrated model router, and it makes no efficacy
claim. The root requires `schema_version`, `contract: "route"`, `run_id`, `task`,
`harness`, `lead`, `available`, `constraints`, and `blind_baseline`.

- `task`: `objective`, `acceptance_criteria`, and `scope_constraints`.
- `harness`: `claude` or `codex`; it selects the executor table.
- `lead`: the running session's `model`, as its model line states it, and `effort`.
- `available`: one boolean per executor (`premier_lead`, `fast_worker`,
  `deep_reasoner`, `workflow`, `spawn_peer`, `cross_vendor_peer`), each `true`
  only where the harness confirmed it this session.
- `constraints`: optional user `model`, `effort`, and `topology` pins. A model or
  effort pin fixes the lead; a topology pin keeps only items of that topology.
- `blind_baseline.lead_choice`: the lead's own plan, recorded first; only its
  hash is kept.

**One request, about the task only.** The request carries `task` and nothing
else: no harness, no lead, no model name, no availability, no baseline. Jev
answers six fixed questions about the work (`task_needs_deep_judgment`,
`task_mostly_mechanical`, `task_parallelizable`, `task_context_heavy`,
`task_outlives_session`, `task_high_stakes`). Each probability reads `yes` at or
above `pass_min`, `no` at or below `fail_max`, and `unclear` between them;
`jev.signals` records both.

**The plan is local.** `ROUTE_EXECUTOR_MAP` maps each signal to an executor for
the declared harness. Claude entries use the `fable`, `opus`, and `sonnet`
aliases, so they follow the current release; Codex entries use the explicit IDs
its model policy requires. `recommendation.lead` suggests a lead and effort
(`keep`, `change_effort`, `switch_suggested`, `unavailable`, `pinned`), and
`recommendation.items` lists each proposed delegation with its executor, topology,
model, effort, purpose, triggering signal, and status (`proposed`, `review`,
`unavailable`, `excluded_by_pin`). An executor the harness did not confirm is
reported `unavailable` and never replaced.

| Situation | Outcome and reason code |
|---|---|
| every signal that shapes the plan is clear | `PLAN_PROPOSED` (`task_profile_mapped`, or the codes below) |
| an unclear signal behind any item | `REVIEW_REQUIRED`, `unclear_task_signal` |
| the plan suggests a different lead or effort | `lead_change_suggested` |
| a needed executor was not confirmed | `some_executors_unavailable` |
| the premier lead is needed but unavailable | `premier_lead_unavailable` |
| a user pin applied | `user_pin_applied`, `topology_pin_excluded_items` |
| a mock, no backend, or a failed call | `NOT_CHECKED` |

`recommendation.applied` is always `false`. The runtime launches nothing and
changes no session setting, and a route result is never evidence that any work
was finished. A mock proposes no plan (`outcome: "NOT_CHECKED"`, `lead: null`,
no items); the hypothetical sits only under `jev.simulated_outcome` and
`jev.simulated_plan`.

## Research result minimization

Research results use `jev-research-result-v1`. They retain input, blind-baseline,
and evidence hashes; model/question pins; sanitized reasons; probabilities; and
bounded signal categories. They omit excerpts, quotes, paths, the baseline label,
and retrieval-provider content. The remote state excludes the baseline and local
paths and contains only the single comparison's structured fields, verified
excerpts/hashes, and citation retrieval provenance.

`runtime_status: "completed"` means the audit operation completed, not that the
content is clean. `verification_status` distinguishes deterministic, simulated,
and live handling. `content_certified` is always false.

## Offline smoke fixtures

Run from this directory (choose result names that do not already exist):

```sh
./verify.py verify --contract orchestrate \
  --state samples/mock-pass-manifest.json \
  --mock-response samples/mock-pass-response.json --out /tmp/jev-pass.json
./verify.py verify --contract orchestrate \
  --state samples/mock-deterministic-fail-manifest.json \
  --mock-response samples/mock-pass-response.json --out /tmp/jev-override.json

./verify.py verify --contract fact-check \
  --state samples/fact-check-manifest.json \
  --mock-response samples/fact-check-mock-response.json \
  --out /tmp/jev-fact-simulation.json
./verify.py verify --contract fact-check \
  --state samples/fact-check-not-checked-manifest.json \
  --out /tmp/jev-fact-not-checked.json
./verify.py verify --contract citation-check \
  --state samples/citation-check-manifest.json \
  --mock-response samples/citation-check-mock-response.json \
  --out /tmp/jev-citation-simulation.json

./verify.py route --state samples/route-state.json \
  --mock-response samples/route-mock-response.json \
  --out /tmp/jev-route-simulation.json
./verify.py route --state samples/route-unavailable-state.json \
  --mock-response samples/route-mock-response.json \
  --out /tmp/jev-route-unavailable.json
```

Both top-level decisions are `ESCALATE` because mocks are simulations. The first
has `jev.simulated_decision: "PASS"`; the second has `"REWORK"`, demonstrating
that a deterministic failure overrides a positive model fixture.

The research fixtures are wholly synthetic. Their mock outputs test dispatch only:
the top-level proposed outcome stays `NOT_CHECKED`, and the hypothetical result is
under `jev.simulated_outcome`. The gate fixture is deterministically
`NOT_CHECKED` without reading a mock or making a request.

The route fixtures behave the same way: each proposes no plan. The mock profiles
a mechanical, high-stakes task. Against the first state the hypothetical
`jev.simulated_plan` keeps the Opus lead at `medium` and proposes a Sonnet fast
worker and an Astra cross-check. The second state declares no Codex peer, so the
same profile returns the cross-check as `unavailable` rather than substituting
another executor.

## Limitations

The thresholds are prototype settings, not human-gold performance claims. The
runtime neither retrieves sources nor proves that caller-supplied provenance is
truthful; hashes only bind selected excerpts to supplied local files, and an
excerpt may omit relevant context. Noul values are advisory signals, not
calibrated posterior probabilities. No result automatically edits, approves, or
certifies a manuscript, and a successful runtime audit does not mean an underlying
citation or claim is correct.

The route contract adds its own limits. Its six questions, thresholds, and
executor table are settings chosen by hand, not measured routing quality; no
claim is made that a proposed plan outperforms the caller's own. The runtime
cannot observe the harness, so a wrong `available` flag or lead report produces a
confidently wrong plan. It launches nothing and applies nothing, and a
recommendation is never evidence that any work was completed.