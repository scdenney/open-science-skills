# The Jev verifier in Claude Code (experimental)

Setup for the opt-in Jev paths in `orchestrate`, `fact-check`, and `citation-check` under Claude Code — completion verification in all three, plus experimental routing in `orchestrate`. It is an **experiment**: it is not part of the published `oss` plugin surface, nothing here auto-triggers, and no skill calls Jev unless the user explicitly invokes `--route` or `--verify` (Jev is their default provider).

The behavior contract lives in the shared runtime, not in this file and not in the skills. Each skill points at the runtime for its own contract and at the installed bundle's `README.md` for setup, so a skill installed on its own never depends on this repository. This page is the complementary Claude-side walkthrough of that setup; where the two differ, the installed bundle wins.

## Opt-in syntax

| Invocation | What happens |
|---|---|
| `/oss:orchestrate <task>`, `/oss:fact-check <task>`, `/oss:citation-check <task>` | the ordinary workflow, unchanged, with **no** Jev call |
| `/oss:<skill> --verify <task>` | the ordinary workflow plus the skill's Jev checkpoint; Jev is the default provider |
| `/oss:<skill> --verify jev <task>` | the explicit equivalent of the line above |
| `/oss:orchestrate --route <task>` (or `--route jev <task>`) | the ordinary workflow plus an experimental Jev **routing** recommendation, before the work |
| `/oss:orchestrate --route --verify <task>` | both, as two separate runs with two separate result files and two separate claims |

Only a literal `jev` after `--verify` or `--route` is read as a provider name; everything else is the task. Jev is the only supported provider in this prototype.

`--route` exists on `orchestrate` only. Before any work starts, Jev profiles the task and the runtime turns that profile into a proposed plan — the lead and its effort, plus which parts go to a fast worker, a deep reasoner, a `Workflow` fan-out, a spawned peer, or a Codex cross-check — written to a file for you to review and edit. It is a local prototype, not a calibrated model router, and it makes no claim to plan better than you would. A routing recommendation is not a completion check, and `--verify` is not a routing decision; the two use different contracts, different state schemas, different result schemas, and different checkpoints.

## Install the shared runtime

Run the installer from a checkout of this repository. It installs a content-addressed bundle under `~/.local/share/oss-experiments/jev-verifier/<hash>` and links `current` at it. It installs no dependencies, no model weights, and no credentials, and it never rewrites a skill. Point `--target` at the skills directory you install into; the installer validates that a complete `orchestrate` skill is there, falling back to `plugin/skills/orchestrate` in the checkout it runs from.

```bash
cd experiments/jev-verifier
python3 install.py --dry-run --target ~/.claude/skills
python3 install.py --target ~/.claude/skills
python3 "$HOME/.local/share/oss-experiments/jev-verifier/current/tools/jev/verify.py" doctor
```

Use `--data-dir /path/to/dir` for a custom location, and set `JEV_VERIFIER_HOME` to that directory's `current` path in the environment Claude Code runs in. The skills resolve the bundle from `JEV_VERIFIER_HOME` first and fall back to the default path.

Start a fresh Claude Code session after installing or after editing a skill; skill text is loaded into context at session start.

## Credentials

A live call needs a TypeSafe API key. Provide it through the environment or your platform's secret store — never in a prompt, a skill file, a shell startup file, or a commit. Nothing in this repository stores a key, and no skill asks you to paste one.

Lookup order, as implemented by the runtime:

| Platform | Order |
|---|---|
| macOS | `TYPESAFE_API_KEY` in the environment, then the current user's **`TypeSafe Jev API` Login Keychain item** |
| Linux | `TYPESAFE_API_KEY` in the environment, then **Secret Service via `secret-tool`**, service `typesafe-jev`, account `<your username>` |
| anything else | `TYPESAFE_API_KEY` in the environment |

Store the key once, out of band, in the keychain (macOS Keychain Access, or `secret-tool store` on Linux) so no agent session ever sees it in a prompt or a file. If the key cannot be resolved, the requested check is reported **blocked** — it is never quietly downgraded to a mock or reported as a pass.

## What the opt-in does and does not authorize

- **Does:** the documented, minimized request to the fixed TypeSafe endpoint — selected task requirements or claim/entry fields, the worker claim, lead observations, and deliberately selected, hash-verified artifact excerpts. `--route` sends the task objective, acceptance criteria, and scope constraints, plus one minimized profile per eligible candidate, in one request each.
- **Does not:** whole-transcript export, a corpus or bibliography scan, unrelated file reads, automated repair, or any write to your credentials. The Jev request itself launches nothing; after receiving a valid `RECOMMENDED` route, the orchestrator may apply it using Claude's own supported mechanism and within the user's task authorization.

### The routing boundary

Jev is never asked about models. One request sends only the task — objective, acceptance criteria, and scope constraints — with no model name, and Jev answers six questions about the work: how hard its hardest judgment is, how much of it is mechanical, whether it parallelizes, whether it is reading-heavy, whether it outlasts the session, and how costly an undetected error would be. The runtime maps those answers to executors through a fixed local table that uses the `fable`, `opus`, and `sonnet` aliases, so a new model release changes nothing on the wire.

**Claude Code declares which executors it can launch** this session — the premier lead, the fast worker, the deep reasoner, `Workflow`, a spawned peer, and the Codex peer — and reports the running lead as its model line states it. That declaration stays on the machine. An executor the plan needs but the session did not confirm comes back `unavailable`, never swapped for another one; an unclear signal marks its item for review.

The runtime writes a file; it launches nothing. `recommendation.applied` is always `false`, and a recommendation cannot change the model or effort a running session is using — only `/model` and `/effort` do that. Explicit `--model` and `--effort` pins fix the lead and win over the plan. The six questions, thresholds, and executor table are **uncalibrated** prototype settings.

Jev is advisory. Verification shadow mode is the default: the lead records its own judgment or report label *before* reading Jev's assessment, and still owns the decision. For explicit `/oss:orchestrate --route`, the skill uses route advisory mode; the lead shows the proposed plan beside its own and applies only `proposed` items the user accepts. Deterministic failures and unperformed checks cannot be overruled by a positive verification score, thresholds are uncalibrated, and the lead's baseline is not human ground truth. Mock responses are simulations and must be described as such; a simulated or failed call is not verification or routing.

## Checks

```bash
cd experiments/jev-verifier
python3 tools/jev/verify.py doctor
python3 tools/jev/verify.py doctor --contract route
python3 -m unittest discover -s tools/jev/tests -v
python3 -m unittest discover -s tests -v
python3 ../../plugin/scripts/test-jev-verifier-integration.py
```

The last of these is the Claude-side check: it asserts that each skill documents the opt-in, points at the matching shared-runtime contract rather than restating it, keeps its default invocation Jev-free, and treats a missing runtime or credential as blocked — for the routing section as well as the verification one.
