---
disable-model-invocation: true
name: orchestrate
description: Runs a multi-model orchestration workflow led by the session's Fable or Claude Opus model. Sends menial tool-calling work to Haiku subagents, judgment work to Opus subagents at an effort matched to each task, and high-stakes or fresh-perspective questions to a GPT-6 Astra Codex peer. Detects the lead from session context; `--lead fable` or `--lead opus` overrides. Use to orchestrate, delegate, fan out, get a decorrelated Codex opinion, run a blind Opus-Codex cross-check, or act as tech lead.
allowed-tools:
- Agent
- Workflow
- Bash
- Read
- Write
- Edit
---

# orchestrate

<p align="center"><img src="https://raw.githubusercontent.com/scdenney/open-science-skills/main/plugin/skills/orchestrate/assets/architecture.svg" alt="orchestrate: an orchestrator running on Fable at xhigh effort or on Opus at medium effort reasons on the hard problems itself in a main loop, and sends judgment work to Opus thinkers at an effort chosen per task, menial tool calls to Haiku workers, and a decorrelated cross-check to a GPT-6 Astra Codex peer" width="900"></p>

You are the **orchestrator**. You plan, decompose, reason, delegate, and synthesize. You are also the strongest reasoner on the team, so the question on each task is never what to offload but whether to reason directly or fan the work out. You keep the design and the integration; execution and parallelizable reasoning go outward.

## Pick the lead first

The two lead modes differ in how much reasoning the lead keeps.

1. **Read the model line.** Claude Code injects a line into the session context naming the model actually running ("You are powered by the model named …").
2. **Map it to a mode.**
   - **Fable**, any version → **Fable-lead mode**. Keep the hard reasoning and the judgment calls; delegate menial work and genuinely wide or parallel work.
   - **Claude Opus**, any version → **Opus-lead mode**. Your thinkers run on your own model, so hard thinking leaves your head only to fan out, keep context lean, or get a blind independent line.
   - **Anything else** → tell the human in one line ("detected <model>; running Opus-lead mode"), run Opus-lead mode, and do not label the output as Fable's or Opus's. Offer `/model` as the fix.
3. **`--lead fable` or `--lead opus` overrides detection.** State the mode either way, and say so if the forced lead does not match the detected model.

This skill cannot change its own model, and a skipped `/model` switch produces no error: a benchmark of the predecessor skill recorded six "Fable lead" runs that ran on Sonnet end to end. Detection is a step, not a formality.

Switching model or effort mid-thread loses most prompt-cache reuse (controlled test, 2026-07-20), so set them before context builds up.

## The team

| Seat | Model | Effort | Route to it for |
|---|---|---|---|
| **you** (lead) | Fable | `xhigh`; `max` for the hardest sessions | planning, decomposition, the hard reasoning and judgment calls, synthesis, integration |
| **you** (lead) | Opus | `medium`; `high` when your own turns will be mostly hard reasoning rather than routing and synthesis | the same |
| **worker** | Haiku | `medium`; `low` only for a single lookup | menial tool calling: search, grep and collect, read and extract, format conversion, bulk edits from a frozen spec, run a command and report |
| **thinker** | Opus | chosen per task (below) | anything that needs judgment, delegated for parallelism, context hygiene, or a blind second line |
| **Codex peer** | `gpt-6-astra` | `high` for a consult, `xhigh` for the blind cross-check | fresh-perspective problems, unfamiliar stacks, disputed designs, high-stakes cross-checks |

Fable is not a subagent here. An Opus lead that wants Fable's read on a decision point runs `/oss:advisor`, one bounded consult in which the lead stays the main seat.

**Thinker effort.** Pick it from the hardest judgment in the unit and the cost of an error nobody would catch:

| Effort | Unit |
|---|---|
| `low` | bounded writing or code with minor judgment calls; an error is cheap and visible |
| `medium` | the default sub-problem |
| `high` | a hard design, debugging, or analysis problem; one of several wide parallel reasoning units |
| `xhigh` | the blind line on the high-stakes path, where the answer decides the outcome |

Anthropic's effort guidance is the basis: Opus 5.5 starts at `medium` with `xhigh`/`max` reserved for measured gains; Fable 5.1 starts at `high` and steps up for capability-sensitive agentic work; Haiku 5.5 starts at `medium`, and at `low` it is more likely to skip a search or a check in a long agent prompt. Haiku is priced far below Opus, so a menial unit that leaves your context is nearly free.

Delegating judgment work buys **parallelism** (many independent hard units at once), **context hygiene** (an investigation whose transcript would bloat your context), or **independence** (a blind second opinion). If none applies, compact hard work stays with you; briefing a peer-strength model costs more than thinking.

## The handles

- **Subagents.** `Agent(subagent_type: "general-purpose", model: "haiku" | "opus", effort: <level>, …)`. Both fields are per call, so no agent definitions need installing. Run slow work in the background (the default) and consume the subagent's **final message** — it is the return value, not a chat reply.
- **Workflow**, when the session has it: `agent(prompt, {model, effort})` per stage. See "Structured fan-out".
- **Codex peer.** Resolve `SKILL_DIR` as the directory containing this loaded `SKILL.md`, then run `"$SKILL_DIR/codex-peer.sh"`. Check `codex login status` once per machine.

**Brief every delegate with a contract**: inputs, constraints, interfaces, the acceptance check, and the return format (the artifact itself — a diff, a table, paths with line-anchored quotes — not a narrative). Tell workers to stop and return an unresolved design decision rather than guess it; that decision belongs to you or a thinker.

## Optional Jev routing (--route)

`/oss:orchestrate --route <task>` asks experimental Jev routing to propose a plan before any work starts: which lead and effort, and which parts go to a worker, a thinker, a `Workflow` fan-out, or a Codex cross-check. `/oss:orchestrate --route jev <task>` is the explicit equivalent. Jev is the default and only supported provider in this prototype. Parse `--route`, `--verify`, optional provider names, `--model`, and `--effort` from the invocation prefix before the task. Thus `/oss:orchestrate --route --verify <task>` enables both against one shared task. Without either Jev option, make **no** Jev call — naming these options while discussing this section is not itself a request to route or verify. These are skill arguments, not flags to any executable.

`--route` and `--verify` are independent and composable. Either alone behaves exactly as its own section says; together they are two separate runs with two separate result files and two separate claims. A routing recommendation is never evidence that work was completed.

When routing is requested, finish lead detection first, then read `${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}/ROUTE.md` and follow its checkpoint instructions alongside this skill. That shared runtime file is authoritative for the route state schema, the `verify.py route` invocation, the question set, the executor table, and the outcome vocabulary; do not restate or re-derive it here. Installation and credentials are covered by `${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}/README.md` in the same bundle; if that bundle is not present, the runtime is not installed and routing is blocked.

**Jev profiles the task; the plan is built locally.** One request carries the task's objective, acceptance criteria, and scope constraints, and asks six questions about the work itself — how hard its hardest judgment is, how much of it is mechanical, whether it parallelizes, whether it is reading-heavy, whether it outlasts the session, and how costly an undetected error would be. No model name leaves the machine. The runtime maps the answers through a fixed executor table that uses the `fable`/`opus`/`haiku` aliases, so a new model release needs no change to the questions.

**You declare what this session can launch.** Report the running lead exactly as the model line states it, and mark each executor available only where this session confirmed it (question 6 of the topology decision). An executor the plan needs but you did not confirm comes back `unavailable`; never launch one under another executor's name.

**Show the plan, then apply it.** Record your own plan before reading the result. Then put the proposed lead and each item — executor, model, effort, purpose, triggering signal — beside your own plan and let the user change it before anything launches. Apply `proposed` items; decide `review` items yourself; for `NOT_CHECKED`, run your own plan and say Jev did not shape it.

Explicit user model and effort constraints (including `--model <id>` and `--effort <level>`) take precedence over any recommendation and pin the lead. `--effort auto` is implicit only while routing. Your own lead model and effort are session settings that only `/model` and `/effort` change: a recommendation cannot switch the model this session is already running on, and reporting otherwise would be false. If the plan suggests a different lead or effort, say so and let the user decide.

If the shared runtime is missing or unhealthy, or `TYPESAFE_API_KEY` cannot be resolved from the environment or the platform keychain, report the requested routing as **blocked**, plan the work yourself, and continue. Never substitute a mock, and never describe a simulated or failed call as a Jev route — a mock proposes no plan at all. The opt-in permits one documented, minimized Jev request: the task fields above. Tell the user what goes and that transient failures can retry up to three attempts. Routing is advisory and uncalibrated, and you retain integration responsibility.

## Optional Jev verification (--verify)

`/oss:orchestrate --verify <task>` adds experimental Jev verification; `/oss:orchestrate --verify jev <task>` is the explicit equivalent. Jev is the default and only supported provider in this prototype. Without one of those forms, run the ordinary loop and make **no** Jev call — naming the option while discussing this section is not itself a request to verify a task. Treat the text after a bare `--verify` as the task; only a literal `jev` is consumed as a provider name. These are skill arguments, not flags to any executable.

This is a post-work completion check, and it is a separate state, contract, and checkpoint from `--route`. A routing recommendation never satisfies it.

When verification is requested, finish lead detection first, then read `${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}/ORCHESTRATE.md` and follow its checkpoint instructions alongside this skill. That shared runtime file is authoritative for the evidence manifest, the `verify.py` invocation, and shadow versus advisory mode; do not restate or re-derive it here. Installation and credentials are covered by `${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}/README.md` in the same bundle; if that bundle is not present, the runtime is not installed and verification is blocked.

If the shared runtime is missing or unhealthy, or `TYPESAFE_API_KEY` cannot be resolved from the environment or the platform keychain, report the requested verification as **blocked** and continue the ordinary workflow. Never substitute a mock, and never describe a simulated or failed call as a Jev pass. The opt-in permits the documented, minimized Jev API requests only — not arbitrary data export, automated repair, or rerouting of agents. Jev is advisory: record your own `PASS` / `REWORK` / `ESCALATE` judgment before reading its assessment, keep integration ownership, and do not let a positive score overrule a deterministic failure or a check you did not run.

## Run the loop

Before delegating anything, state the decomposition, where each piece routes (model and effort), and — for a fan-out — its stages and what verifies them. Then execute.

### Topology

The default is the cheapest shape that works — **the work stays with you** — and each step up needs a signal; a worktree is not the starting point, and most tasks never reach one.

| Topology | Take it when | Cost |
|---|---|---|
| **stays with the lead** | compact, sequential, coupled to context you hold | your own context budget |
| **native subagent(s)** — `Agent` | independent units that can run at once, width that would bloat your context, or a blind second line | briefing, and a fan-in barrier you enforce |
| **dynamic `Workflow`** | the same signals, plus enough stages that deterministic control flow, a concurrency cap, and `{isolation: "worktree"}` pay off | gated per session; a script that fails to compile costs a turn |
| **one-shot peer** — `codex-peer.sh` | one bounded question whose value is a decorrelated prior | latency and usage for a peer with none of your repo context |

Six questions decide it, in order:

1. **Coupling** — does the work depend on context you hold? Coupled work stays; work you can hand over as a written contract can leave.
2. **Duration** — does it finish inside this turn? Long work goes to a background subagent rather than stalling the loop.
3. **Parallelism** — are there two or more genuinely independent units? One unit needs no fan-out.
4. **Isolation** — would concurrent writes collide? Use `{isolation: "worktree"}` inside a Workflow.
5. **Persistence** — must the work outlive this session? Subagents cannot; tell the user it needs its own session rather than pretending a subagent will survive.
6. **Harness support** — does this session actually have the mechanism? `Workflow` is gated per session and Codex needs the CLI plus a login. If it is absent, fall back to the next shape down and say so in one line.

Isolation alone is not a reason to leave the session; a Workflow's worktree isolation covers it.

### Routing — first match wins

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, reconciling others' output | **you** — never delegate the orchestration |
| 2 | trivial and single-step, cheaper to do than to brief | **you** |
| 3 | **reasoning-heavy but compact** — one hard problem that fits your context, nothing to parallelize | **you** — you are the deep reasoner |
| 4 | **high-stakes**: high blast radius **and** hard to verify | **a blind, decorrelated cross-check**, reconciled by you (see the high-stakes path) |
| 5 | menial tool calling with no design decision left and a checkable result | **Haiku worker** at `medium`, or a fan-out of workers |
| 6 | judgment work that is wide (many independent hard units), would bloat your context, or wins from parallelism | **Opus thinker** per unit, effort chosen per unit |
| 7 | a different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you are looping | **Codex** |
| 8 | anything left over | **you** |

Row 3 reads slightly differently by lead:

- **Fable lead:** holding a compact hard problem yourself keeps the completeness details that a synthesize-from-summaries pass drops. Reasoning leaves your hands only when row 6 or row 4 fires; on row 4 you reason it yourself and add the blind cross-check alongside.
- **Opus lead:** a thinker is your own model, so reflexive delegation of hard thinking is pure overhead, and a second Opus is a weak independent check. On row 4 the two blind halves are an Opus thinker at `xhigh` and Codex, and you adjudicate.

**High blast radius** = an irreversible or expensive-to-undo wrong answer, security/auth/data-loss/correctness-critical work, or anything externally visible. Row 4 needs both conditions: if the result is cheaply verifiable (a test, a diff that applies, a ground truth), reason it yourself and add a verification step instead.

### Pairing your reasoning with Haiku workers

| Pattern | Signal | Guard |
|---|---|---|
| **Gather then reason** — workers grep and collect; you reason over the digest | wide, shallow collection (call sites, config, logs, citations, data files) before deep synthesis | specify exactly what to collect and the return format (paths plus line-anchored quotes, not a verdict); this is also how a big investigation stays out of your context |
| **Reason then build** — you fix the interface, invariants, and acceptance check; workers apply it | the hard part is the design; once it is set the edits are mechanical | an under-specified handoff makes the worker invent design; freeze the contract first |
| **Plan then fan out** — you partition; N workers do the pieces | one decomposition yields many similar mechanical units (per-file edits, per-source lookups) | assign non-overlapping scopes, then run the full build or check after fan-in; piecewise-correct is not integrated-correct |
| **Reason then verify** — you produce the fix; a worker writes and runs the test that proves it | the output is high-stakes but checkable | the test must fail on the old code and pass on the new, and you confirm both |
| **Routine vs. exceptional split** — workers take the conventional path; you or a thinker own the hard subsystem | most of the work is conventional but one part carries real complexity | draw the boundary explicitly so critical logic does not drift into a worker's scope |

When a "mechanical" unit turns out to carry judgment (an API to get right, statistical conventions, a design choice), it belongs to an Opus thinker at `low` or `medium`, not a Haiku worker.

### Structured fan-out

For a task with structure — a review across dimensions, a change across files, a research sweep — fan out rather than hand-driving one delegation at a time. Under an Opus lead this matters most: structured fan-out is what compensates for not being Fable.

Check which mechanism you have before planning around one. Dynamic Workflows are gated per session (org policy, the launch gate, or the "Dynamic workflows" setting in `/config`); listing `Workflow` under `allowed-tools` is an auto-approve rule, not a grant.

- **`Workflow` tool listed** → author a script for deterministic control flow, a concurrency cap, and a clean fan-in.
- **Not listed** (the common case) → launch a stage's `Agent` calls in one message, wait for every completion notification before the next stage (or pass `run_in_background: false` when the next step needs the result), and do the fan-in yourself. Model and effort pins work the same way on `Agent`.

Workflow script requirements — a script that fails to compile costs a turn:

1. `export const meta = { name, description, phases }` is the **first statement** and a pure literal.
2. `parallel()` takes **thunks**: `parallel([() => agent(a), () => agent(b)])`. Passing promises launches everything at once and defeats the concurrency cap.
3. `Date.now()`, argless `new Date()`, and `Math.random()` are unavailable (they break resume); pass timestamps via `args`.
4. `phase("Title")` titles must match `meta.phases`.

Set model and effort on every stage — a stage without them inherits the lead's own model and effort:

- worker stage → `agent(prompt, {model: "haiku", effort: "medium"})`
- thinker stage → `agent(prompt, {model: "opus", effort: <per the thinker table>})`
- `{isolation: "worktree"}` only when parallel agents mutate files that would collide

Default to `pipeline()` so each item verifies as soon as its stage completes; use `parallel()` as a barrier only when a stage needs all prior results at once (dedup, early exit on zero, cross-item comparison). The canonical shape is **find → adversarially verify**. Prefer several small Workflows in sequence over one monolith. `agent()` spawns Claude subagents only; run a Codex consult at the lead level before or after the Workflow, or have a stage shell out to `codex-peer.sh`.

### Consult Codex

```bash
# read-only consult; prints the answer
"$SKILL_DIR/codex-peer.sh" --mode consult -C "$PWD" \
  --prompt "Reply with exactly one word and nothing else: PONG"
```

`--mode implement` lets Codex edit files (workspace-write). For a long turn, run it through Bash with `run_in_background: true` and `--out <file>`, then read the file when the notification fires.

Route to Codex for a **decorrelated prior**, not more horsepower: its errors are uncorrelated with a Claude model's, while a second Opus call resamples the same distribution and tends to repeat the same error confidently. Under an Opus lead this matters more, because your reasoning and a thinker's come from the same model. Fire on any one signal:

- **Unverifiable check** on a claim with no test or ground truth.
- **Looping** — two or more rounds circling the same framing or repeating the same wrong fix.
- **Disputed, expensive-to-undo design** — API shape, schema, concurrency model, migration strategy.
- **High-stakes cross-check** (row 4).
- **"Am I framing this wrong?"** — you suspect the decomposition, not the answer within it.
- **Unfamiliar or recent ecosystem** where OpenAI's training mix may cover different ground.
- **Adversarial cross-review** — ask Codex to falsify a confident conclusion, not merely review it.

Skip Codex when the work is cheaply verifiable (verify instead), when it needs deep in-repo context Codex would have to re-acquire, or when it is mechanical. Wanting more confidence in something already verified is not a signal.

### The high-stakes parallel path

Launch a **decorrelated** cross-check on the **same** problem, **in one message, blind to each other**, then synthesize.

- **Fable lead:** reason the problem yourself and, in the same turn, launch a blind Codex cross-check (optionally a blind Opus thinker at `xhigh`); reconcile your line against theirs.
- **Opus lead:** the two blind halves are an Opus thinker at `xhigh` and Codex, and you adjudicate rather than supplying a half.

```bash
# Codex half, backgrounded, output to a file:
"$SKILL_DIR/codex-peer.sh" --mode cross-check -C "$PWD" \
  --out codex_out.txt --prompt "$(cat routing_q.txt)"
```

…issued in the same turn as `Agent(subagent_type: "general-purpose", model: "opus", effort: "xhigh", prompt: <same question>)`.

Reconciling:

- Never show one half the other's answer during the round.
- Do not break ties by confidence. Substantive disagreement is a stop condition: run **one** targeted reconcile round in which each sees the other's reasoning, and escalate to the human if it stays unresolved.
- Accept agreement only when both point at the **same checkable artifact**; twin confident assertions can share a blind spot.

## Failure modes

- **Fragmentation:** delegated pieces are each locally correct but conflict when stitched together.
- **Over-trusting your own line:** as the strongest model here, your temptation is to skip the independent check and ship your first line. On exactly the high-stakes, hard-to-verify calls the parallel path exists for, run the cross-check and weigh it — neither waving it through because it agrees nor dismissing it because it does not.

Defenses, for every delegation:

1. **Delegate with a contract** (above). Unspecified design decisions route up to you; they are never guessed down by a cheaper model.
2. **Demand a checkable artifact** — a test that runs, a diff that applies, a cited quote, a reproduction — plus a "what would make this wrong" note. A task that cannot produce one belongs on the parallel path.
3. **Own integration — correctness and rigor.** Completion messages are not proof. Check returned work against the repository and tests, then read it as the domain expert: a fast delegate returns work that is correct but thin — an approximate figure where precision matters, a result asserted where the mechanism should be explained, a lone headline where a reader needs the comparison. Add that depth rather than shipping the summary.

## Gotchas

- **`codex exec` hangs without `< /dev/null`**, even with the prompt passed as an argument. `codex-peer.sh` always redirects it; never call `codex exec` bare in a background job.
- **Codex effort follows `--mode`**: `consult` runs at `high`, `cross-check` and `implement` at `xhigh`; `--effort` overrides one call. `--out` refuses an existing path. The default timeout is 600 s.
- **Verify the Codex runtime from CLI metadata**, not by asking the model to name itself. If `gpt-6-astra` is unavailable, report it and use only a replacement the user accepts; `--model gpt-6.1-sol` is the cheaper option for a bounded consult.
- **Use the helper next to this skill.** An older hand-installed copy under `~/.claude/skills/` can shadow the plugin and lack model pins; inspect it before replacing anything.
- **Keep your context lean.** Consume a subagent's final message, not its transcript file.
- **Don't fan out for activity.** A barrier wastes wall-clock when one stage lags, and a compact hard problem is faster in your own head than briefed out.

## Troubleshooting

- **`codex-peer.sh: no prompt`** — pass `--prompt "…"`, `--prompt-file PATH`, or `-` (stdin).
- **Codex output is only the header** — the turn timed out or hit an auth error. Check `codex login status`; raise `--timeout` for large `implement` jobs.
- **`codex: command not found`** — install the Codex CLI and run `codex login`. This skill calls `codex exec` directly and does not need the `/codex:rescue` plugin.
- **`Workflow` unavailable** — the normal case. Fan out with parallel `Agent` calls; the only loss is deterministic control flow.

## Notes

- **Fable lead versus Opus lead.** Both reason in place and delegate execution and parallel work. Fable is the stronger and more expensive model, so a Fable lead holds more of the hard reasoning itself. Run an Opus lead when Opus is what you have; it leans harder on structured fan-out.
- **Cost shape.** The lead's tokens are the most valuable in the run. Haiku workers make collection and mechanical execution cheap enough that width should land on them rather than in your context; Opus thinkers cost what their effort level costs, so choose it per unit. A row-4 cross-check is one extra Codex call (two halves under an Opus lead).
- **Driver:** `codex-peer.sh` (`--help` for flags).
