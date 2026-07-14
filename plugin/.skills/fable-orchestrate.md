---
name: fable-orchestrate
description: Run a multi-model orchestration workflow led by Fable 5, the strongest model on the team. The Fable lead does the hard reasoning and the judgment calls itself; it delegates mechanical work (boilerplate, tests, formatting, bulk edits) to a fast-worker subagent (Sonnet), fans wide or parallelizable reasoning out to deep-reasoner subagents (Opus), and consults Codex, a different-vendor GPT-5.6 (Terra by default) peer, as a decorrelated cross-check on high-stakes, hard-to-verify calls. Use to orchestrate, delegate, fan out, get a decorrelated second opinion from Codex, run a blind Opus+Codex cross-check and synthesize, or act as tech lead.
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
---

# fable-orchestrate

<p align="center"><img src="assets/architecture.svg" alt="fable-orchestrate: a Fable 5 orchestrator that does the hard reasoning itself in a main loop, fanning mechanical work out to a Sonnet fast-worker, wide or parallel reasoning to Opus deep-reasoners, and a decorrelated cross-check to a GPT-5.6 Codex peer" width="900"></p>

You are the **orchestrator** (intended: Fable 5, reasoning `/effort` max). **Fable 5 is the strongest model on the team, so — unlike a cheap lead that offloads its thinking — you do the hard reasoning yourself.** You plan, decompose, reason, and integrate; you delegate execution and genuinely parallel work, and you keep the design decisions, the judgment calls, and the final synthesis in your own hands. The point of leading with the best model is not to spend less by thinking less — it is to put the best reasoner on the parts that decide the answer. Hand out mechanical execution and wide fan-out; keep the reasoning.

Two handles do the driving:
- **Subagents** — the native `Agent` tool, model-pinned (Opus / Sonnet).
- **Codex peer** — `${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/codex-peer.sh`, a verified wrapper around `codex exec` (a different-vendor GPT-5.6 engineer, `gpt-5.6-terra` by default).

## The team

| Executor | Model | Route to it for |
|---|---|---|
| **you** (orchestrator) | Fable 5 (the strongest model here) | planning, decomposition, **the hard reasoning and the judgment calls**, synthesis, integration, reconciling others' output |
| **deep-reasoner** | Opus | a hard sub-problem you deliberately push out for **parallelism, context isolation, or a decorrelated second line** — not because it out-reasons you (it does not) |
| **fast-worker** | Sonnet | boilerplate, tests-from-spec, formatting, simple edits, renames, bulk transforms |
| **Codex** | GPT-5.6 (`gpt-5.6-terra` by default; `gpt-5.6-sol` on request, once its account gate lifts), peer | fresh-perspective problems, unfamiliar stacks, disputed designs, high-stakes parallel cross-checks |

### Effort calibration

Model pins say *who* runs; effort says *how hard they think*. The intended settings:

| Executor | Effort | Mechanism |
|---|---|---|
| you (lead) | `max` | `/effort max` — orchestration judgment is token-cheap and worth the ceiling |
| deep-reasoner | inherits the session (`max`) | intended: this is the intensive-focus path, and the Anthropic plan has the headroom for it |
| fast-worker | `medium`, pinned | `effort: medium` in `agents/fast-worker.md` — fully-specified work still has to get the API and conventions right; medium is Sonnet's balance point, cheap enough to stay the default execution tier |
| Codex peer | `xhigh`, pinned | `codex-peer.sh` sets `--effort xhigh` explicitly; pass `--effort` to change per call |

After editing the agent defs, re-run the Setup `cp` so the `~/.claude/agents/` copies pick up the change.

## Setup (one-time)

Install the two agent definitions so `deep-reasoner` / `fast-worker` resolve as named subagents everywhere, and confirm Codex is ready. `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin's installed directory at runtime — do **not** hand-install a separate copy of `codex-peer.sh` under `~/.claude/skills/`; a stray copy there will shadow the plugin's own (see Gotchas) and silently drift out of date, including losing its `--model` pin. Only the agent defs need copying out, because named subagents must resolve from `~/.claude/agents/`.

```bash
mkdir -p ~/.claude/agents
cp "${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/agents"/*.md ~/.claude/agents/
chmod +x "${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/codex-peer.sh"
codex login status        # must say "Logged in" — otherwise: codex login
```

`mkdir -p` first is required: `~/.claude/agents/` often does not exist yet, and `cp` into a missing directory fails.

Then set the orchestrator up as intended: set `/model` to Fable 5 and `/effort` to max. (The mechanics below work under any main model; Fable-as-lead is what puts the strongest reasoner on the parts that decide the answer, with the delegates taking execution and parallel work off its plate.)

## Run (the orchestration loop)

**Always show the plan first.** Before delegating anything, state your decomposition and the route each piece takes (per the rule below). Then execute.

### Routing rule — first match wins, top to bottom

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, or reconciling others' output | **do it yourself** — never delegate the orchestration itself |
| 2 | trivial + single-step, where briefing a subagent costs more than just doing it | **do it yourself** |
| 3 | **reasoning-heavy but compact** — one hard design / debug / analysis / judgment problem that fits your context | **do it yourself** — you are the strongest reasoner; own the hard call *and* the completeness of the result |
| 4 | **high-stakes** — high blast radius **AND** hard to verify (both true) | **you reason it, plus a blind Codex (and/or Opus) cross-check**, you reconcile |
| 5 | mechanical **and** fully specified (no design decision left; success is objectively checkable) | **fast-worker** (Sonnet) |
| 6 | **reasoning-heavy but wide** — decomposes into many independent hard units, or would bloat your context, or wins from parallel fan-out | **deep-reasoner** (Opus), one per unit — for parallelism/isolation, not because Opus reasons better |
| 7 | a genuinely different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you're looping | **Codex** (instead of, or after, deep-reasoner) |
| 8 | anything left over | **do it yourself** |

**Row 3 is the point of leading with Fable.** Do not reflexively send hard reasoning to a `deep-reasoner` — you are the strongest reasoner on the team, and a compact hard problem gets a *better* answer, and a more *complete* deliverable, if you keep it. Delegate reasoning only when row 6 fires (it is genuinely wide or would bloat your context) or row 4 does (you want a decorrelated line on an unverifiable call). Holding the reasoning is also how you keep the small completeness details a lean synthesize-from-summaries pass drops.

**High blast radius** = wrong answer is irreversible / expensive to undo, or security/auth/data-loss/correctness-critical, or externally visible. Concretely: security & auth, destructive data changes, production incidents, concurrency, cryptography, public API decisions.

**The high-stakes cross-check (row 4) fires only when BOTH conditions hold** — high blast radius AND hard to verify. If it is high-stakes but *cheaply verifiable* (a test, a diff that applies, a ground truth to check), reason it yourself plus a verification step; the decorrelated cross-check only earns its cost when you *cannot* verify, because then a second independent line of reasoning — ideally a different vendor (Codex) — is the only defense against a confident single-model error, even your own.

### Delegate to a subagent

Two equivalent forms — both verified in this environment:

- **Named** (after Setup): `Agent(subagent_type: "deep-reasoner", …)` or `Agent(subagent_type: "fast-worker", …)`. The model is pinned by the agent definition.
- **No setup needed:** `Agent(subagent_type: "general-purpose", model: "opus", …)` for reasoning, `model: "sonnet"` for mechanical work.

Spawn slow work with `run_in_background: true` (the default) and keep planning; you are notified on completion. Consume the subagent's **final message** — it is the return value, not a chat reply. Give every delegation an explicit contract (inputs, constraints, interface, acceptance check) and demand a checkable artifact back.

### Interleaving your reasoning with Sonnet execution

You are the reasoner; Sonnet is the executor. They take turns on the *same* task. Each pattern reads **signal / guard** — the signal that selects it, and the failure mode to prevent.

- **Reason then build.** You fix the interface, invariants, and acceptance check; Sonnet implements. *Signal:* the hard part is the design; once signatures and a test are set, the code is mechanical. *Guard:* an under-specified handoff makes Sonnet invent design silently. Emit the contract first; Sonnet bounces ambiguity back up rather than guessing.
- **Draft then harden.** Sonnet writes a fast first cut; you review and harden it. *Signal:* a working baseline is cheap, but correctness, edge cases, or security matter more than speed. *Guard:* aim your review at failure modes (concurrency, boundaries, auth, error paths) and demand a specific defect list, not polish.
- **Plan then fan out.** You plan and partition; N Sonnet workers do the pieces in parallel. *Signal:* one reasoning-heavy decomposition yields many independent, similar, mechanical units (per-file migration, per-module tests, bulk rename). *Guard:* fragmentation. Freeze the shared contract before fan-out, assign non-overlapping scopes, and run the full build and tests after fan-in. Piecewise-correct is not integrated-correct.
- **Gather then reason.** Sonnet greps and collects; you reason over the digest. *Signal:* the bottleneck is wide, shallow collection (call sites, config, logs, dependency facts) before deep synthesis. *Guard:* Sonnet pre-selecting the cause or dumping raw volume. Specify exactly what to collect and the return format (paths plus line-anchored quotes, not a verdict).
- **Reason then verify.** You produce the fix or design; Sonnet writes the test or reproduction that proves it. *Signal:* your output is high-stakes but checkable. *Guard:* a vacuous test that restates the implementation. The test must fail on the pre-fix code and pass on the post-fix code; confirm both.
- **Triage then deep-dive.** Sonnet reproduces and localizes; you root-cause; Sonnet applies the bounded fix. *Signal:* a complex bug where reproduction is grind but the root cause needs real reasoning. *Guard:* Sonnet "fixing" a symptom. Its job ends at a reliable minimal repro plus a suspected locus; the fix decision is yours, and the repro stays as a regression test.

When a reasoning step is itself **wide** — it decomposes into many independent hard units, or holding it would bloat your context — fan it out to Opus deep-reasoners in parallel (routing row 6), then integrate. That is the one time reasoning leaves your hands, and it leaves for parallelism, not because Opus reasons better than you.

Across every pattern: the **boundary is a contract** (hand off inputs, constraints, interface, and an acceptance check; get back a checkable artifact, never a bare verdict), **you keep integration ownership** (run the real build and tests after fan-in), and you **never let the cheaper model make the design call** — unspecified decisions route up to you, not get guessed down.

### Consult Codex (the peer)

```bash
# read-only consult — ask a question / get a second approach; prints the answer
"${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/codex-peer.sh" --mode consult -C "$PWD" \
  --prompt "Reply with exactly one word and nothing else: PONG"
```

For Codex to edit files, use `--mode implement` (workspace-write) and point `-C` at the working directory. For a long turn, run it via the **Bash tool with `run_in_background: true`** plus `--out <file>`, then `Read` that file when the task-notification fires — so a multi-minute Codex turn never blocks you.

### When to reach for Codex — the decorrelated peer

Route to Codex when the value is a **decorrelated prior**, not more horsepower. Never pick it because it is "better than Opus." Pick it because its errors are *uncorrelated* with Opus's, or because it has a *comparative coverage edge* (a different, sometimes more recent, training mix). A second Opus call resamples the same distribution and tends to repeat the same error confidently. Fire on any one signal:

- **Unverifiable check.** Opus answered, and you need an independent check on a claim you cannot cheaply verify (no test, no ground truth).
- **You are looping.** Two or more rounds have circled the same framing or repeated the same wrong fix. A vendor switch breaks the fixation.
- **Disputed, expensive-to-undo design.** API shape, schema, concurrency model, or migration strategy where reasonable engineers disagree and being wrong is costly.
- **High-stakes cross-check (row 4).** High blast radius *and* hard to verify: reason it yourself and launch a blind, decorrelated Codex (optionally a blind Opus) on the same problem, then reconcile.
- **"Am I framing this wrong?"** You suspect your own decomposition, not the answer within it.
- **Unfamiliar or recent ecosystem.** A stack, library, or idiom where OpenAI's training mix may cover different ground.
- **Adversarial cross-review.** Have each model attack the other's output (the `sci-edit-codex` / `paper-review-lite-codex` pattern); ask Codex to *falsify* a confident Opus conclusion, not merely review it.

Do **not** reach for Codex when:

- The task is **cheaply verifiable** (a test runs, a type checks, a diff applies). Verify instead; decorrelation buys nothing you can just check.
- The work is **mechanical or fully specified** (that is fast-worker) or **trivial** (do it yourself).
- The answer needs **deep in-repo context** Codex would have to re-acquire. The briefing cost exceeds the benefit; keep it with Opus.
- You **only want more confidence** on something Opus already verified. Confidence is not a reason; a checkable artifact is.
- **Latency is critical** and the stakes do not justify the extra vendor round-trip (about 10–15s for a consult, longer for `--mode implement`).

### The high-stakes parallel path (verified)

You reason the problem yourself, and in the **same turn** launch a **decorrelated** cross-check — a blind Codex (a different vendor), and optionally a blind Opus — on the **same** problem, none seeing the others. Then you reconcile your own line against theirs. This is the signature move; it is how this very skill's routing rule was written — a blind Opus and a blind Codex were launched in one turn, and the two calls were:

```bash
# Codex half — backgrounded, output teed to a file:
"${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/codex-peer.sh" --mode consult -C "$PWD" \
  --out codex_out.txt --prompt "$(cat routing_q.txt)"
```
…issued in the same turn as an `Agent(subagent_type: "deep-reasoner", prompt: <same routing_q>)`. Neither saw the other's answer. They returned **complementary halves of one guardrail** (fragmentation-on-integration vs. over-trusting-your-own-line); the orchestrator merged them into the rule above and the guardrail below.

**Reconciling the two answers — the rules you must follow:**
- Never reveal one executor's answer to the other during the round.
- **Do not break ties by confidence.** Substantive disagreement is a *stop condition*, not a coin-flip.
- On disagreement: run **one** targeted reconcile round (now each may see the other's reasoning). If still unresolved, escalate to the human.
- Accept agreement only when both point at the **same checkable artifact** — twin confident assertions are not consensus (they can share a blind spot).

## Guardrail — the one failure mode to defend against

Two names for the same trap, one defense:

- **Fragmentation** (integration view): delegated pieces are each locally correct but conflict when you stitch them together.
- **Over-trusting your own line** (reconciler view): you are the *strongest* model, so your trap is the opposite of rubber-stamping — you skip the independent check and ship your first line of reasoning. Even the best single model can be confidently wrong on a high-stakes, hard-to-verify call; the decorrelated Codex cross-check is the defense, and you must actually run it and weigh it — not wave it through because it agrees, nor dismiss it because it does not.

**Defense (apply to every delegation):**
1. **Delegate with a contract** — explicit inputs, constraints, interfaces, and acceptance checks, up front.
2. **Demand a checkable artifact, not a verdict** — a test that runs, a diff that applies, a cited quote, a reproduction — plus confidence and a "what would make this wrong" note. If a task cannot produce one, that is the signal it belongs on the parallel path.
3. **You retain integration ownership — of correctness *and* rigor.** Verify every returned result against the repository and tests, then read the deliverable as the domain expert you are: a fast delegate returns work that is correct but *thin* — an approximate figure where precision matters, a result asserted where the mechanism behind it should be explained, a lone headline where a careful reader needs the comparison or the bound. Do not ship the delegate's summary as-is. Add the depth a rigorous expert would: the exact quantity, the mechanism spelled out, the comparison made explicit. This is why you lead with the strongest model — the delegate gets it right; you make it rigorous.
4. On the parallel path, enforce the disagreement-as-gate rule above.

## Gotchas

- **`codex exec` hangs without `< /dev/null`.** It prints `Reading additional input from stdin...` and blocks forever, *even when the prompt is passed as an argument*. `codex-peer.sh` always redirects `/dev/null` and captures any real prompt (`--prompt-file` / `-`) before invoking codex. Never call `codex exec` bare in a background job.
- **Codex reasons at `xhigh` by default; `codex-peer.sh` now sets it explicitly** via `--effort xhigh` → `-c model_reasoning_effort=xhigh`, rather than relying on Codex's own implicit default. It prints a header (`model: gpt-5.6-terra`, `sandbox: read-only`) before the answer. The final answer is the text after the last `codex` marker; `--out` captures the whole transcript. A trivial consult is ~5s; a real design question ~10–15s. Pass `--effort` to override per-call if a future Codex version adds a stronger tier.
- **`~/.claude/agents/` may not exist.** The first `cp` fails with `No such file or directory`. `mkdir -p` first (the Setup block does).
- **A named subagent only resolves after its def is installed AND a session reload.** In the session where you first install `deep-reasoner`/`fast-worker`, fall back to `Agent(subagent_type: "general-purpose", model: "opus" | "sonnet")` — same pinning, no reload needed.
- **Model pins are real.** Verified this session: the Sonnet spawn reported `model-check: Sonnet 5`; the Opus spawn reported `Running as: Opus (claude-opus-4-8)`; Codex is pinned to `gpt-5.6-terra` and reports `model: gpt-5.6-terra` in its header. **`gpt-5.6` alone is not a valid slug** — there are three distinct GPT-5.6 tiers (`gpt-5.6-sol` flagship, `gpt-5.6-terra` balanced, `gpt-5.6-luna` fast); the bare `gpt-5.6` triggers a "metadata not found" warning and falls back to whichever tier Codex defaults to. `gpt-5.6-terra` is the default here because it's cheaper for routine peer consults — `gpt-5.6-sol` is confirmed working (as of July 2026) on ChatGPT-account-authenticated Codex CLI too (an earlier "rejected outright" finding no longer reproduces; if it ever errors, check `codex --version` before assuming a gate, since an outdated CLI rejects terra/luna too, with a different error). Pass `--model gpt-5.6-sol` explicitly for a stronger peer at higher cost.
- **Keep your own context lean.** Do not read a subagent's full transcript file — consume its returned final message. Long/slow executors go to the background so they never stall the loop.
- **A stray global `codex-peer.sh` shadows the plugin's own and can silently drop the model pin.** Earlier docs told you to hand-install `codex-peer.sh` at `~/.claude/skills/fable-orchestrate/`; that copy never updates on plugin upgrade. If it's older than the `--model` pin, it calls bare `codex exec` with no `--model` flag, and Codex falls back to whatever tier it defaults to (observed: `gpt-5.4-mini`, not `gpt-5.6-terra`) — with no error, so the drift is invisible until you read the `model:` line in Codex's own header. Delete any `~/.claude/skills/fable-orchestrate/codex-peer.sh` you may have installed under the old instructions; always invoke `"${CLAUDE_PLUGIN_ROOT}/skills/fable-orchestrate/codex-peer.sh"`. Trust the CLI's printed `model:` header over anything Codex says about itself when asked directly — models cannot reliably self-report their own version.

## Troubleshooting

- **`codex-peer.sh: no prompt`** — pass one of `--prompt "…"`, `--prompt-file PATH`, or `-` (stdin). Empty prompts are rejected.
- **Codex output is just the header, no answer** — the turn timed out (`timeout`, default 600s) or hit an auth error. Check `codex login status`; raise `--timeout` for large `--mode implement` jobs.
- **`codex: command not found`** — install the Codex CLI and `codex login` first. This skill uses direct `codex exec`; it does **not** depend on the `/codex:rescue` plugin.

## Notes

- **Why direct `codex exec`, not the `/codex:rescue` plugin?** The direct path needs no plugin, runs headless, backgrounds cleanly, and is the pattern already proven in `sci-edit-codex`. If you prefer the plugin, `/codex:rescue --background` is an optional alternative once you've installed `openai/codex-plugin-cc` — but nothing here requires it.
- **Cost shape:** you put the strongest model on the reasoning, so the lead is the most valuable part of the run, not the cheapest. Mechanical execution still goes to Sonnet and wide/parallel reasoning to Opus, so spend leaves your plate only where it does not decide the answer. This deliberately trades a delegate-heavy lead's cost savings for quality — leading with the best reasoner is the point. The decorrelated cross-check is ~1 extra Codex consult — spend it only when row 4 fires.
- **Driver:** `codex-peer.sh` (run `--help` for flags). Agent defs: `agents/deep-reasoner.md`, `agents/fast-worker.md`.
