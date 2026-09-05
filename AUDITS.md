# Audits

## 2026-08-08 — full library audit and Opus 5 upgrade (v2.22.0)

Full best-practices audit and upgrade of every installed skill: 41 plugin + 39 codex + 13 personal
+ 4 thesis + 4 third-party + legacy Codex-home copies (~105 units). Twelve independent auditors —
ten Opus family batches, one Sonnet integrity matrix, one Codex (gpt-5.6-sol) self-audit of the
codex library — judged against three rubrics: Anthropic's skill authoring best practices (including
its MCP rules), OpenAI's Codex skills spec, and an Opus 5 compatibility lens (over-constraint,
stale model/tool mechanics, trigger-budget crowding, unverifiable harness claims). Findings:
4 critical / ~113 major / ~172 minor. Fixes landed via two worktree peers (plugin, codex), two
fixer agents (thesis, personal), and a lead pass; the orchestration-family diff was blind
cross-checked by Codex before merge (5 findings, all applied).

## What changed (this repo)

- **Committee collapse**: model-committee-fable/-sol were 71–78% drift-prone copies of
  model-committee (three maintenance passes had each landed in a subset). Now one chair-
  parameterized skill + three thin command wrappers. Counts: 41→39 Claude, 39→37 Codex.
- **False harness claims removed**: "invoking this skill satisfies the Workflow opt-in" (4 skills)
  — the gate is session-level and no skill can grant it; replaced with a check-then-branch on
  actual tool availability, with the Agent-fan-out fallback specified (no implicit stage barrier;
  effort pins soft in the fallback).
- **journal-review routing**: the Void→Fable "cheaper than Opus" premise was inverted (Fable 5 is
  2× Opus 5 per MTok); Void→Opus, explicit Fable→Opus→Sonnet→Haiku fallback ladder; Codex twin
  reworked for the 4-slot runtime (two finder waves).
- **list-experiment**: precision cost unified on the sourced figure — BCM 2020 p.1312 says ~14×
  (verified against the paper; the two April 2026 in-repo reviews recording ~10× were themselves
  wrong); sensitivity gate aligned to the paper's four conditions.
- **Verified-live paper-tex fixes**: SI cross-references rendered `??` (missing
  `\externaldocument` + missing third build pass); bib-less builds printed an empty BUILD FAILED
  (`.blg` never read). Both reproduced, fixed, re-verified with latexmk.
- **Private-path leaks** stripped from vlm-ocr-evaluation, model-council-voting,
  llm-calibration-logprobs (published plugin cited author-private files); empirical content kept.
- **Hub-spoke wiring**: vlm-ocr-pipeline now routes through the vlm-ocr-evaluation gate;
  text-classification names llm-calibration-logprobs and model-council-voting.
- **`${CLAUDE_PLUGIN_ROOT}` retired from skill bodies** (advisor, both orchestrators; thesis
  plugin as well): live-verified the variable is neither substituted into skill bodies nor
  exported to Bash. Replaced with deterministic newest-cache resolution
  (`ls -d …/oss/*/ | sort -V | tail -1`).
- **spawn**: the permission-mode self-read now covers all six modes, reads wide, and takes the
  last match (the first can be the reader's own echoed command).
- **Descriptions**: restored the "when to use" halves cut in 985a114; fable/opus-orchestrate now
  lead with the session-model discriminator; codex-side trimmed to 7,123 chars (under the ~8k
  selector budget) with negative scopes truncation-safe; codex reference/ → references/ (spec
  layout); codex advisor set explicit-invocation-only.
- **check.sh**: alias allowlist (commands may wrap a parameterized skill without their own dir).

Outside this repo, same effort: thesis plugin 0.2.0→0.3.1 (broken `_shared` resolution + an
orphaned 0.1.0 cache silently serving an older rubric contract; a transcription error in the MAIR
grade table corrected against the faculty source; source dir now git-tracked), personal skills
(sci-edit manuscript mode could not execute — allowed-tools lacked Bash; description was over the
1024 hard cap; prose-family trigger partition rebuilt), omarchy compliance (retired humanizer
removed; substack pair reconciled and de-macOS-ified), Codex install hygiene (~/.agents/skills
completed, legacy ~/.codex/skills shadow copies retired).

Evidence: `~/.claude/skill-audit/` (rubrics, per-batch findings JSON, decision memo, cross-check).
Frozen pre-audit copies of every skill: `~/.claude/skill-gauntlet/originals/`.


## 2026-09-05 — Codex and OpenAI model audit

Prepared v2.26.0 locally. The working tree was clean at intake. Existing historical audit records, changelog entries, source material, and dated research examples were preserved.

### Call inventory and disposition

| Surface | Result |
|---|---|
| `plugin/skills/orchestrate/codex-peer.sh` and its skill, command, and diagram | Astra/xhigh default for demanding Claude-to-Codex consults; explicit Terra and effort overrides retained. |
| `plugin/skills/diverge` and `plugin/skills/paper-review-lite`, including alias commands | Direct `codex exec` examples now select Astra/xhigh. |
| `plugin/skills/model-committee/scripts/codex-member.sh` and its Codex counterpart | Default member now Astra/xhigh. Explicit `chair: sol` remains Sol/xhigh with a Terra member. Fable chair effort aligned to the plugin’s existing high setting. |
| `codex/advisor/scripts/sol-advisor.sh`, skill, metadata, and diagram | Legacy path retained; default advisor now Astra/xhigh, with explicit model and effort overrides. |
| `codex/orchestrate`, runtime preflight, metadata, and diagram | Lead now Astra/xhigh; Terra and Luna roles retained. Native overrides follow the exposed tool schema; CLI availability follows actual permissions. |
| `codex/diverge` and `codex/paper-review-lite` | Prefer Astra for demanding reviewers where runtime overrides are available. Do not claim skill prose switches the running model. |
| `text-classification`, `llm-calibration-logprobs`, `model-council-voting`, and `vlm-ocr` in both libraries | Research guidance rather than an executable OpenAI SDK pipeline. Preserve historical model identifiers, provider diversity, and validated production choices. Add model/endpoint compatibility and representative-validation gates to classification and logprobs. |
| Remaining Codex skills | Run in the selected session; no separate OpenAI model default to migrate. |
| Source library, third-party material, previous audits, and historical changelog | Provenance and examples retained; not treated as current runtime defaults. |

No executable OpenAI SDK or direct HTTP inference pipeline was found in the maintained scripts. Active inference is through CLI drivers and command examples. `MODEL-POLICY.md` records reusable practices for other repositories without rewriting unrelated global settings or installed skill copies.

### Reliability and validation

- CLI tests use a mock executable, with no authentication, network access, or model spend. They cover four wrappers across defaults, explicit overrides, literal prompts, read-only versus implementation routing, existing output protection, invalid effort/timeout rejection, empty answers, exit-code propagation, and timeouts. The runtime gate is tested against synthetic matching, mismatching, and rerouted turns.
- Advisor and committee outputs are staged and published exclusively after success. Peer transcripts stream into newly created paths. Python enforces deadlines on both macOS and Linux, including termination of the child process group.
- Package validation passes for 38 Claude skills and 37 Codex skills, strict YAML, byte-identical flat mirrors, manifest/version/count parity, shell syntax, and executable modes on the Codex helpers. CI now runs these checks and the offline regression suite.
- Astra account availability, live response quality, latency, and cost were not tested. The xhigh setting preserves the demanding-review policy; it is not presented as an Astra benchmark result.

### GitHub and standalone-site follow-up

No push or deployment was performed. The AI for Research checkout was inspected read-only and remains unchanged. Its `scripts/sync-skills.mjs` preserves hand-authored descriptions, so a dispatch alone will not update their model names. Update `docs/skills/index.html` descriptions and search metadata for advisor, orchestrate, and model-committee, plus any other model references found in the publication pass; preserve the explicitly named Sol chair. Then run the site sync for release metadata, review the rendered page, and publish after the repository push. The source notification trigger now includes Codex files, command wrappers, release metadata, and the model policy.

Sources checked: [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model), [Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra), and [Codex CLI reference](https://developers.openai.com/codex/cli/reference).


## 2026-09-05 — Codex installation and native routing verification

Implemented the follow-up plan while preserving the prior audit and coordinated Claude-side edits.

- Installed the missing `~/.agents/skills/orchestrate` link to this checkout. Existing committee, council, advisor, and spawn links were already correct and were preserved. The new `plugin/scripts/install-codex.py` supports selected/all skills, repository/user targets, dry-run, and non-overwriting conflict reporting. Documentation no longer uses force-replacement symlinks.
- Preserved explicit invocation and the user's selected Astra effort. The lead check still rejects a different model, missing runtime evidence, or a current-turn reroute. A live check passed at medium. Regression cases cover low, medium, high, xhigh, and max, plus missing effort and reroutes.
- Added Sol/high for demanding separable work alongside Terra/medium and Luna/low. Native model overrides with self-contained briefs are preferred; CLI workers remain the permitted fallback.
- Ran three read-only native worker checks with `fork_turns="none"`. Their current-thread rollout metadata confirmed Sol/high, Terra/medium, and Luna/low, with no recorded reroutes. These prove runtime routing, not general quality rankings. Terra misread an absent implicit-invocation policy as disabled; the lead corrected that against the documented default of true.
- After installation, a force-reloaded CLI app-server `skills/list` reported orchestrate, model-committee, model-council-voting, advisor, and spawn enabled, with no discovery errors. The installed orchestrate runtime helper also executed successfully. Desktop picker rendering is not verified by that API check; refresh/restart the app if its picker remains stale. The app was not terminated during this working session.
- Mirrored the coordinated committee policy to Codex: Fable default, Astra chair with Sol member, explicit Opus chair, and legacy Sol chair with Terra member. Codex uses `chair: astra|opus|fable|sol` parameters rather than additional suffixed skills. Corrected stale plugin wording and the Astra member-call override to match the chair table, preserving the added aliases.
- Package, wrapper, and installer checks passed. Installer tests cover preview, repeat runs, missing paths, conflicting directories/files/broken links, unknown names, and full-catalog installation. CI runs the installer suite as well.

GitHub publication, the installed Claude plugin update, and the standalone-site publication remain pending. No global model configuration or permissions were changed.
