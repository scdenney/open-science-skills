# Optional routing for orchestrate (experimental)

This is a shared runtime reference, not a separate skill, and not a calibrated model router. The active `orchestrate` skill remains authoritative for how work is decomposed, delegated, and integrated. This file covers only the opt-in routing checkpoint: before any work starts, Jev profiles the task, the runtime maps that profile to a proposed plan, and the lead shows the plan to the user.

Routing and completion verification are separate. They have different contracts, different state schemas, different result schemas, and different checkpoints. A routing recommendation says nothing about whether any work was finished, and `ROUTE.md` never substitutes for `ORCHESTRATE.md`.

## Activation and setup

- Invoking `orchestrate` with `--route <task>` selects Jev by default.
- `--route jev <task>` means exactly the same thing.
- `--route` and `--verify` are independent and composable. Either may be used alone; used together they produce two separate runs, two separate result files, and two separate claims.
- Parse `--route`, `--verify`, optional provider names, `--model`, and `--effort` from the invocation prefix before the task text. Thus `--route --verify <task>` enables both; the first remaining text is the shared task.
- Plain `orchestrate`, with neither option, does not load or call Jev. Mentioning these examples while discussing the interface is not itself a request to route a task.
- Each library states its own invocation syntax; this runtime is shared and does not prefer one.
- Only a literal `jev` immediately after `--route` is consumed as the provider name. No other provider is supported in this prototype.

Resolve the bundle from `JEV_VERIFIER_HOME` if set, otherwise `~/.local/share/oss-experiments/jev-verifier/current`. Set `JEV_VERIFY` to its `tools/jev/verify.py`. Read the bundled `tools/jev/README.md` and `tools/jev/contracts/route.json` before preparing a route state. Run `python3 "$JEV_VERIFY" doctor --contract route`; stop the routing path and report a missing or unhealthy runtime, or a missing `TYPESAFE_API_KEY`, as **blocked**. Never silently fall back to a mock. The ordinary work continues under the lead's own plan; report the requested Jev route as blocked, not as applied.

Before calling, disclose what goes to `https://api.typesafe.ai/v1/systemone`: **the task only** — its objective, acceptance criteria, and scope constraints — in one request, with up to three bounded attempts on transient failure. Nothing about models is sent: not the lead's model, not the executor table, not what this session can launch, and not your own pre-recorded plan. Credentials come from the environment, not the state file or the prompt.

## What Jev is asked

Six questions about the task, each answered as a probability. None mentions a model, so the answers do not depend on Jev knowing a model released after it was trained.

| Question id | Asks whether the task… |
|---|---|
| `task_needs_deep_judgment` | has a hardest part that needs open-ended judgment the specification does not settle |
| `task_mostly_mechanical` | is mostly fully specified work with objectively checkable output |
| `task_parallelizable` | splits into substantial units that can run at the same time |
| `task_context_heavy` | needs a large body of material read that the integrator only needs summarized |
| `task_outlives_session` | must outlast one session or needs its own isolated workspace |
| `task_high_stakes` | would be costly or hard to reverse if an error went undetected |

Each answer reads **yes** at or above `pass_min`, **no** at or below `fail_max`, and **unclear** between them.

## How the plan is built

The mapping is local arithmetic over a fixed executor table in `verify.py` (`ROUTE_EXECUTOR_MAP`). Claude entries are CLI aliases (`fable`, `opus`, `haiku`), so they follow the current release; Codex entries are the explicit IDs its model policy requires.

- **Lead.** `task_needs_deep_judgment` yes → the premier lead at its ceiling (Fable/`xhigh`, or Astra/`xhigh` under Codex). Unclear → the current lead at `high`. No → the current lead at `medium`. The recommendation cannot change the running session: `switch_suggested` and `change_effort` are suggestions for the user, who changes the model with `/model` (or a new session) and the effort with `/effort`.
- **Mechanical** yes → the fast worker carries out the specified work.
- **Parallelizable** yes → fan out through `Workflow` when available, otherwise through deep reasoners (hard units) or fast workers (easy units).
- **Context-heavy** yes → a subagent reads in its own context and reports back.
- **Outlives session** yes → a spawned peer in its own worktree, on the lead's model.
- **High stakes** yes → a blind cross-vendor check before the result is final (Astra for a Claude lead, Fable for a Codex lead, matching each side's peer script).

No item at all means the work stays with the lead.

## The availability declaration is yours

Declare, under `available`, which executors this session can actually launch: `premier_lead`, `fast_worker`, `deep_reasoner`, `workflow`, `spawn_peer`, `cross_vendor_peer`. Mark one `true` only where you checked it this session; a listed tool is not a granted one. Report the running lead under `lead` exactly as the session's model line states it. An executor the plan needs but you did not confirm comes back `unavailable`; the runtime never substitutes another one.

## Checkpoint

Route before the work, not after it.

1. Write down your own plan first and put a one-line summary in `blind_baseline.lead_choice`. Only its hash is retained; the plan is never sent to Jev.
2. Build a route state using the `jev-route-state-v2` schema and `tools/jev/samples/route-state.json`: the real objective, acceptance criteria, and scope constraints, the harness (`claude` or `codex`), the running lead, the availability you confirmed, and any explicit user pin under `constraints`.
3. Choose a fresh result path and run in advisory mode:

```bash
python3 "$JEV_VERIFY" route --state "$ROUTE_STATE" --out "$ROUTE_RESULT" --mode advisory --allow-network
```

4. Read the result only after recording your own plan. Show the user the proposed lead and each item — executor, model, effort, purpose, and the signal that triggered it — next to your own plan, and let them edit it before anything launches. Report whether the call actually succeeded. A simulated or failed call is not a routing result.

## What the outcomes mean

| `recommendation.outcome` | Meaning |
|---|---|
| `PLAN_PROPOSED` | every signal that shapes the plan is clear; items may still be `unavailable` or `excluded_by_pin` |
| `REVIEW_REQUIRED` | at least one signal is unclear; its items are marked `review` and you decide them |
| `NOT_CHECKED` | the run did not produce a routing result (no backend, a simulation, or a failure) |

Item statuses: `proposed`, `review` (its signal is unclear), `unavailable` (you did not confirm the executor), `excluded_by_pin` (a user topology pin rules it out). Lead statuses: `keep`, `change_effort`, `switch_suggested`, `unavailable`, `pinned`.

## Judgment and limits

The recommendation is a file. `recommendation.applied` is always `false`: this runtime launches nothing, changes no session setting, and cannot switch the model a live session is already running on. Apply only `proposed` items, through the harness's native mechanism, after checking them against the task; decide `review` items yourself; never launch an `unavailable` one under another executor's name.

Explicit user model and effort constraints (`--model`, `--effort`) pin the lead and win over the recommendation. `--effort auto`, the default while routing, leaves the lead's effort to the plan. A topology pin keeps only items of that topology.

The standalone CLI defaults to shadow, which is appropriate for smoke tests. The skill uses advisory for an explicit `--route` request; the lead still adjudicates before applying anything.

The six questions, the thresholds, and the executor table are experimental and **uncalibrated**; nothing here is a measured claim about routing quality, and no claim is made that the plan beats your own. The table encodes this library's orchestration policy; when that policy changes, change the table in the same commit.

Offline tests may use `--mock-response` instead of `--allow-network`, but a mock is a simulation: its result proposes no plan (`outcome: "NOT_CHECKED"`, `lead: null`, no items), and the hypothetical sits only under `jev.simulated_plan`. Nothing may launch work from one. Keep the route state, the route result, and any completion-verification evidence distinct in the handoff.
