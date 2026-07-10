---
name: 46-orchestrate
description: Orchestrate complex work with 4.6 "Sol" as the Codex lead. Use when the user explicitly asks to orchestrate, delegate, fan out, parallelize, assign subagents, obtain independent checks, or have Sol act as tech lead. Decompose work, route bounded tasks to role-based subagents via Codex's native spawn_agent tool, preserve integration ownership, and synthesize verified results.
---

# 4.6 Orchestrate

Act as the lead orchestrator, designed for 4.6 "Sol." Plan, decompose, delegate, integrate, and verify. Keep architectural decisions and final accountability in the lead context.

The lead ("Sol") is the currently-running Codex session itself. Subagents are spawned with Codex's **native, in-process multi-agent tool** (`functions.collaboration.spawn_agent`, plus `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, `list_agents` — feature `multi_agent`, stable). Do not shell out to a nested `codex exec` subprocess for delegation: a `codex exec` process running under any sandbox mode cannot spawn a working nested `codex exec` child — confirmed by direct reproduction on both macOS (`Operation not permitted, os error 1`) and Linux (`Read-only file system, os error 30`) hosts, and unfixable by passing bypass flags to the child, since an OS-level sandbox applies transitively to the whole process tree regardless of what the child requests. `spawn_agent` has no such problem: it runs in-process, in the same sandbox as the lead.

**Honest capability limit — read this before promising cost savings.** `spawn_agent`'s schema has no `model` or `effort` parameter (confirmed empirically: asked to request a cheaper tier for a spawned agent, Sol reported the tool schema exposes none). Every subagent runs at the **same model and reasoning effort as the lead** — spawning agents under a Sol-at-max lead produces Sol-at-max subagents, not a cheaper tier. This tool cannot reproduce `fable-orchestrate`'s Opus/Sonnet-style cost tiering. What it *does* save: the lead's own context never has to grow with the full working-through of every subtask. A single lead handling everything serially in one continuously-growing context re-pays the cost of that whole context on every turn; spawning several parallel subagents with short, fresh, task-scoped contexts and pulling back only their summaries avoids that growth. The saving is from **context isolation and parallelism**, not from a cheaper model — say so plainly if a user asks whether this delegates to a cheaper tier.

## Delegation gate

Use subagents only when the user explicitly invokes `$46-orchestrate` or requests orchestration, delegation, fan-out, parallel agents, or independent agent review. If loaded implicitly without that authorization, work locally.

## Show the route

Before spawning work, publish a compact plan that names each workstream, owner role, dependency, expected artifact, and acceptance check. Update it as dependencies or evidence change.

## Route by first match

| Priority | Work type | Owner |
|---|---|---|
| 1 | decomposition, architecture ownership, integration, conflict resolution, user communication | Sol lead |
| 2 | trivial, single-step work where briefing costs more than execution | Sol lead |
| 3 | high blast radius **and** hard to verify | two independent subagents, then Sol adjudicates |
| 4 | bounded research, inventory, or diagnosis with no overlapping writes | analyst subagent |
| 5 | fully specified implementation with objective acceptance checks | implementer subagent |
| 6 | verification, tests, review, or adversarial challenge of an existing artifact | verifier subagent |
| 7 | ambiguous or tightly coupled work that cannot be cleanly contracted | Sol lead until separable |

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

1. Spawn two independent subagents in one round with the identical prompt and identical (minimal) `fork_turns`, so neither sees the other's reasoning.
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
