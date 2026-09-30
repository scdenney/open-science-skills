# Shared Jev verifier prototype

Supported skill integrations are `orchestrate`, `fact-check`, and
`citation-check`. Use the existing skills in either library, each with its own
invocation syntax:

```text
orchestrate     --verify <task>
fact-check      --verify <task>
citation-check  --verify <task>
orchestrate     --route <task>     # experimental; orchestrate only
```

Jev is the default. Appending `jev` after `--verify` or `--route` is an
equivalent explicit form. Plain skill invocation is unchanged. There is no
separate verifier skill.

`--verify` is a post-work completion check; `--route` is an experimental
pre-work recommendation of an execution topology. They are independent and
composable, and they keep separate contracts, state schemas, result schemas, and
checkpoints — a routing recommendation is never a completion claim.

## Local installation

This experimental bundle contains a Python 3.10+ stdlib runtime and the shared integration references. It does not install model weights, dependencies, or API keys. Jev is a hosted service.

`--target` is the skills directory you install into. The installer validates that
a complete `orchestrate` skill is reachable there, falling back to either
library's copy in this checkout; neither library is required.

```bash
# Claude Code
python3 install.py --dry-run --target ~/.claude/skills
python3 install.py --target ~/.claude/skills

# Codex (~/.agents/skills is the default target, so --target may be omitted)
python3 install.py --dry-run --target ~/.agents/skills
python3 install.py --target ~/.agents/skills
```

The installer validates the existing `orchestrate` dependency, installs a content-addressed bundle under `~/.local/share/oss-experiments/jev-verifier/<hash>`, and links `current` to it. It removes the old `orchestrate-ver` discovery link only when verified as owned by the previous installer. Historical bundles remain recoverable; user-owned links and files are not replaced. Base-skill integrations are validated independently on deployment.

Each supported base skill needs its small optional-verification section. That local integration is separate from this runtime installer, which never rewrites a base skill. Nothing here publishes or updates the production plugin. Copy the complete runtime bundle to another host and run the same installer there; apply the same optional section to that host's base skill.

Custom locations are supported through `install.py --target /path/to/skills --data-dir /path/to/jev-verifier`. For a custom data directory, set `JEV_VERIFIER_HOME` to its `current` directory in the environment the agent runs in.

On macOS, the verifier accepts `TYPESAFE_API_KEY` from the environment or reads the `TypeSafe Jev API` item for the current macOS user from Login Keychain. On Linux, it falls back to Secret Service (`secret-tool`) using service `typesafe-jev` and the current username. This works from either agent without putting the key in a prompt, shell startup file, or Git. On other hosts, configure `TYPESAFE_API_KEY` in the environment used by the agent. Store the key out of band, in the keychain or the environment; never paste it into a prompt, a skill file, or a commit. Start a fresh session after changing skill instructions.

## Checks and behavior

```bash
python3 tools/jev/verify.py doctor
python3 -m unittest discover -s tools/jev/tests -v
python3 -m unittest discover -s tests -v
```

See `tools/jev/README.md` for direct CLI usage and offline smoke fixtures, and
`ORCHESTRATE.md`, `FACT-CHECK.md`, `CITATION-CHECK.md`, or `ROUTE.md` for the
relevant integration. Choose fresh output paths; existing results cannot be
overwritten.

Verification defaults to shadow mode: the lead records its judgment before reading Jev's assessment. Jev does not automatically repair, reroute, or approve work. Advisory mode requires an explicit request. Live calls deliberately export selected task requirements, worker claims, observations, and artifact excerpts/hashes to the fixed TypeSafe endpoint. No whole transcripts are exported.

Mock responses are simulations, never live verification. Missing credentials block the requested check rather than silently replacing it. The baseline is the lead's judgment, not human ground truth; decision thresholds are uncalibrated. A successful offline test does not validate the live API or prove research-quality or cost improvements.

The route path adds its own boundary. The caller declares every candidate, its model, effort, capabilities, relative cost rank, and whether the harness can actually apply it; this runtime cannot enumerate models or entitlements and never infers one. Ineligible candidates are filtered out before any request. Each remaining candidate is judged in its own bounded request, carrying that one profile and the task; the availability flags and the caller's own pre-recorded pick are withheld. The cheapest suitable candidate by the caller's declared rank wins, as local arithmetic — per-candidate answers are not comparable and never order the list. It writes a recommendation file, launches nothing, and cannot change a running session's model or effort. Its thresholds and suitability questions are uncalibrated prototype settings, not a measured routing-quality claim.

## Future skill integrations

Candidates for small integrations and their own contracts include `advisor`,
`deliverable-lint`, `referee-response`, and `research-wayfinder`.

Their definitions of done differ: a referee-response skeleton may retain author placeholders, a detection-only lint audit may finish with unresolved findings, and research-wayfinder closure may require live researcher assent that a verifier cannot provide.
