---
name: 46-orchestrate
description: Orchestrate complex work as the Codex lead on the GPT-5.6 family — gpt-5.6-terra by default for token economy, gpt-5.6-sol reserved for intensive focus. Use when the user explicitly asks to orchestrate, delegate, fan out, parallelize, assign subagents, obtain independent checks, or have Codex act as tech lead. Decompose work, route bounded tasks to role-based subagents via Codex's native spawn_agent tool (subagents inherit the lead's model and effort), escalate the hardest compact problems to a one-shot Sol consult, preserve integration ownership, and synthesize verified results.
---

# 4.6 Orchestrate

<p align="center"><img src="assets/architecture.svg" alt="46-orchestrate: a GPT-5.6 Terra Codex orchestrator in a main loop fans work out to researcher, implementer, and verifier subagents that inherit the lead's model, and escalates the hardest problems to a one-shot gpt-5.6-sol consult at xhigh" width="900"></p>

Act as the lead orchestrator for the GPT-5.6 family. Plan, decompose, delegate, integrate, and verify. Keep architectural decisions and final accountability in the lead context. The intended lead tier is **`gpt-5.6-terra`** — because subagents inherit the lead's model, a Terra lead makes the entire spawn tree token-economical by construction; `gpt-5.6-sol` is reserved for the moments that need intensive focus (see *Model and effort calibration*).

The lead is the currently-running Codex session itself. Subagents are spawned with Codex's **native, in-process multi-agent tool** (`functions.collaboration.spawn_agent`, plus `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, `list_agents` — feature `multi_agent`, stable). Do not shell out to a nested `codex exec` subprocess for delegation: a `codex exec` process running under any sandbox mode cannot spawn a working nested `codex exec` child — confirmed by direct reproduction on both macOS (`Operation not permitted, os error 1`) and Linux (`Read-only file system, os error 30`) hosts, and unfixable by passing bypass flags to the child, since an OS-level sandbox applies transitively to the whole process tree regardless of what the child requests. `spawn_agent` has no such problem: it runs in-process, in the same sandbox as the lead.

**Honest capability limit — read this before promising cost savings.** `spawn_agent`'s model-visible schema has exactly three fields — `task_name`, `message`, `fork_turns` — and no `model` or `effort` parameter (re-verified 2026-07-11 on Codex CLI v0.144.1, which is also the newest published release; three differently-flagged live probes, including `multi_agent_v2` forced on). Every subagent runs at the **same model and reasoning effort as the lead**. This is a regression-by-default rather than a permanent absence: override fields existed and worked around v0.137 (openai/codex#26948), but current releases hide them from the schema (`hide_spawn_agent_metadata`, openai/codex#31814), v2 full-history forks reject them (openai/codex#20077), and the TOML custom-agent path is broken (openai/codex#26363) — community reports agree (community.openai.com, 2026-07-10). An "unhide + `fork_turns=\"none\"`" escape hatch circulates but is unconfirmed and reportedly still drops overrides; do not build on it without re-verifying on the installed version. In-process spawning therefore cannot reproduce `fable-orchestrate`'s cost tiering — the calibration section below is how this skill approximates it instead. What spawning *does* save: the lead's own context never has to grow with the full working-through of every subtask. A single lead handling everything serially in one continuously-growing context re-pays the cost of that whole context on every turn; spawning several parallel subagents with short, fresh, task-scoped contexts and pulling back only their summaries avoids that growth. The saving is from **context isolation and parallelism**, not from a cheaper model — say so plainly if a user asks whether a spawn delegates to a cheaper tier.

## Model and effort calibration

The lead's `--model` and `model_reasoning_effort` are the only reliable cost levers — they set the price of the whole spawn tree. Calibrate them the way `fable-orchestrate` calibrates its cheap lead:

| Choice | Setting | Why |
|---|---|---|
| **Default lead** | `gpt-5.6-terra`, effort `medium` (raise to `high` when the orchestration itself is hard) | the whole in-process tree becomes Terra by construction — the balanced tier (about half of Sol's per-token price) with current multi-agent (v2) support |
| **Intensive focus** | one-shot `codex exec --model gpt-5.6-sol -c model_reasoning_effort=xhigh --sandbox read-only --skip-git-repo-check "<self-contained brief>" < /dev/null` | pays Sol only for the compact hardest problems — architecture calls, gnarly debugging, the decorrelated half of a high-stakes check; Sol sees only the brief, so write a complete one |
| **Cheap bulk** | one-shot `codex exec --model gpt-5.6-luna -c model_reasoning_effort=low …` | Luna (about 2.5× cheaper than Terra) for fully-specified mechanical work worth taking out of process |
| **Sol lead** | only when lead quality is the bottleneck for the whole task | every spawn is then Sol at the lead's effort — the economics invert; spawn sparingly, only for context isolation or blind parallel checks |

Rules of thumb: **escalate effort before escalating tier**, and never leave the session at `xhigh` while fanning out routine work — the effort propagates to every subagent.

**Environment caveat for the cross-tier one-shots:** a nested `codex exec` fails under any sandbox mode (the OS sandbox applies to the whole process tree), so they must run as escalated or unsandboxed calls under a live session; when escalation is unavailable, keep the hard problem in the lead instead. The `< /dev/null` on the nested call is load-bearing — without it `codex exec` hangs waiting on stdin.

## Delegation gate

Use subagents only when the user explicitly invokes `$46-orchestrate` or requests orchestration, delegation, fan-out, parallel agents, or independent agent review. If loaded implicitly without that authorization, work locally.

## Show the route

Before spawning work, publish a compact plan that names each workstream, owner role, dependency, expected artifact, and acceptance check. Update it as dependencies or evidence change.

## Route by first match

| Priority | Work type | Owner |
|---|---|---|
| 1 | decomposition, architecture ownership, integration, conflict resolution, user communication | lead |
| 2 | trivial, single-step work where briefing costs more than execution | lead |
| 3 | high blast radius **and** hard to verify | two independent lines, then the lead adjudicates |
| 4 | a compact problem that outclasses the lead's tier (hard architecture call, gnarly debug) | out-of-band Sol one-shot (calibration table), briefed self-contained |
| 5 | bounded research, inventory, or diagnosis with no overlapping writes | analyst subagent |
| 6 | fully specified implementation with objective acceptance checks | implementer subagent |
| 7 | verification, tests, review, or adversarial challenge of an existing artifact | verifier subagent |
| 8 | ambiguous or tightly coupled work that cannot be cleanly contracted | lead until separable |

High blast radius includes security/authentication, destructive data operations, public API compatibility, concurrency, cryptography, production incidents, privacy, and externally visible irreversible changes. "Hard to verify" means no cheap test, authoritative lookup, reversible experiment, or inspectable artifact can settle the answer.

Do not use multiple agents merely to increase activity. Parallelize independent work or genuinely independent judgments — since spawning does not reduce per-call cost here, an unnecessary spawn is pure overhead, not a cheap experiment.

## Spawn subagents correctly

Every subagent is created with `spawn_agent`. Confirmed parameters: `task_name` (a short identifier other calls use to address this agent), `message` (the task brief — this is the subagent's entire starting context unless `fork_turns` adds more), and `fork_turns` (how much of the lead's own conversation to propagate — `"all"` gives the subagent full history; for a bounded, fully-specified task, propagate the minimum needed, since a large `fork_turns` value defeats the context-isolation saving this tool exists for). Consult the tool's own schema at call time for any parameters not listed here — this list reflects what has been directly exercised, not a full spec.

| Role | Behavior | fork_turns |
|---|---|---|
| analyst / verifier | inspect, inventory, diagnose, adversarially review, or high-stakes cross-check without editing | minimal — pass only the artifact path and the specific question, not the lead's full history |
| implementer | make bounded, fully-specified edits with objective acceptance checks and run them | minimal — a complete delegation contract (below) should make full history unnecessary |
| high-stakes independent check | two agents spawned in the same round on the identical prompt, blind to each other's reasoning | minimal, identical for both, so neither is anchored by the other |

All agents share the same container, filesystem, and working directory as the lead — edits by one are immediately visible to all others, including the lead. This makes write-collision discipline (below) load-bearing, not optional.

**Concurrency is real and bounded.** The tool itself states 4 available concurrency slots, including the lead — so at most 3 subagents run at once regardless of how many are queued. Batch additional work after prior agents finish; do not assume unlimited fan-out.

Use `wait_agent` to block on a spawned agent's result, `send_message` to pass it a message without triggering a new turn, `followup_task` to give a *running* agent a new task, `list_agents` to check what's active, and `interrupt_agent` to reclaim a stalled one.

## Write a delegation contract

Every subagent brief (the `message` passed to `spawn_agent`) must specify:

```text
Objective:
Inputs and authoritative paths:
In scope:
Out of scope:
Constraints and invariants:
Write ownership:
Expected artifact:
Acceptance checks:
Return format: conclusion, evidence, changed files, residual risk
```

Give each worker the minimum task-local context required. Do not leak another worker's conclusions into an independent round. Ask for evidence and artifacts, not confidence alone.

## Prevent write collisions

- Assign disjoint files or directories to concurrent implementers.
- Use read-only agents for overlapping analysis or review.
- State that the shared workspace may change while an agent runs; require rereading before edits.
- Never let two agents edit the same file concurrently.
- Preserve user changes and unrelated worktree modifications.
- Keep commits, pushes, deployments, destructive operations, and external messages under the same authorization rules as the lead.

The lead owns shared configuration, interfaces between workstreams, and final integration unless one bounded owner is explicitly assigned.

## Run the orchestration loop

1. Inspect authoritative workspace state.
2. Decompose work and identify dependencies.
3. Publish the route and acceptance checks.
4. Spawn all ready, independent workstreams concurrently within the 3-subagent capacity.
5. Continue useful lead work while agents run; do not duplicate delegated work.
6. Use `wait_agent` to consume each agent's final response and inspect its artifact directly.
7. Send a focused `followup_task` to the same agent when its artifact is incomplete, rather than spawning a fresh one that repeats the briefing cost.
8. Integrate in dependency order.
9. Run end-to-end checks at the lead level.
10. Report the outcome, verification evidence, and unresolved risk.

Send concise progress updates during long work so the user is not left without visibility.

## Use the high-stakes path

For work that is both high blast radius and hard to verify:

1. Spawn two independent subagents in one round with the identical prompt and identical (minimal) `fork_turns`, so neither sees the other's reasoning. Note the correlation limit: both inherit the lead's model, so they resample the same distribution. For the highest stakes, make one half the out-of-band Sol one-shot from the calibration table instead — then the two lines differ by model, not just by sampling.
2. Keep them blind to each other's reasoning — do not relay one's output into the other's task.
3. Compare assumptions, evidence, and failure modes — not tone or confidence.
4. Accept agreement only when both point to the same checkable evidence.
5. On substantive disagreement, run one targeted reconciliation round where each can see the competing reasoning.
6. If disagreement survives or evidence remains insufficient, stop and ask the user; do not break the tie by confidence.

Use one worker plus a direct verification step when the task is high impact but cheaply verifiable.

## Integrate rigorously

Treat subagent results as untrusted until inspected. Check:

- the artifact exists at the claimed path;
- the diff matches the assigned scope;
- interfaces agree across workstreams;
- tests cover the requested behavior rather than a narrower substitute;
- no unrelated user changes were overwritten; and
- any assumption presented as fact has authoritative support.

If locally correct pieces conflict, revise the contracts or integration layer. Do not paper over incompatible assumptions.

## Completion rule

Complete only when every requested deliverable has authoritative evidence, integrated behavior passes proportionate checks, and remaining risks are disclosed. Agent completion messages are not proof of overall completion.

## Failure handling

- If an agent stalls, use `interrupt_agent` to reclaim it, then send one narrower `followup_task` or reassign.
- If an agent fails after editing, inspect the shared worktree before retrying.
- If capacity is exhausted (3 subagents already active), queue dependent work rather than spawning redundant agents.
- If a spawn fails outright, report the exact error rather than silently falling back to doing the work in the lead context — a silent fallback is what causes runaway lead-context token growth. If the failure looks environmental (not a task-brief problem), stop and ask rather than spending tokens on unbounded self-diagnosis.
