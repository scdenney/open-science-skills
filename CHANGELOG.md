# Changelog

Versions are the `version` field shared by `plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; `plugin/scripts/check.sh` fails if they differ or if this file has no entry for the current version. Earlier history is in commit subjects and in `AUDITS.md`.

## [2.28.0] — 2026-09-05

- Codex `$orchestrate` now detects and accepts either an active GPT-6 Astra or GPT-5.6 Sol lead. Astra remains the preferred lead and keeps compact hard reasoning in-session. Sol-lead mode retains decomposition, coordination, integration, and verification while escalating unusually difficult units to Astra; both modes route bounded and mechanical work to Terra and Luna and can use a Claude peer.
- The fail-closed runtime gate still rejects missing metadata, reroutes, and unsupported lead models. Regression tests cover both accepted leads, a rejected Terra lead, missing effort, and reroutes under Astra and Sol.

## [2.27.0] — 2026-09-05

- On-demand skills. Twenty-seven of the 38 Claude skills now carry `disable-model-invocation: true`: they add nothing to a session until invoked by name, and Claude does not auto-trigger them. The auto-triggering core is citation-check, doc-to-markdown, fact-check, figures, literature-review, paper-review-lite, qualtrics-ops, referee-response, replication-package, research-repo, and spawn (kept visible because orchestrate and research-wayfinder call it). The set comes from six months of invocation evidence plus the six skills whose docs already require explicit invocation. A hidden skill still loads through its alias commands (verified: `/oss:model-committee-opus` reaches `model-committee`). Always-on cost in a research session falls from about 9.9k to about 3.4k tokens.
- Codex library: sixteen skills gain `policy.allow_implicit_invocation: false` on the same evidence rule — conjoint-cleaning, conjoint-design, cross-national-design, doc-to-markdown, list-experiment, llm-calibration-logprobs, methods-reporting, model-council-voting, qualtrics-ops, referee-response, replication-package, research-grill, research-wayfinder, survey-data-audit, topic-modeling, vlm-ocr — and `codex/README.md` marks them invoke-by-name. The two platforms differ because their evidence differs.

## [2.26.0] — 2026-09-05

- Default demanding Codex peer, advisor, ideation, manuscript-review, committee-member, and orchestration routes to GPT-6 Astra. Keep Terra/Luna work roles, the explicit Sol committee chair, and the legacy `sol-advisor.sh` entrypoint.
- Codex orchestration preserves the selected Astra effort; the runtime gate checks model identity and reroutes without requiring xhigh. Sol/high handles demanding separable work, Terra/medium bounded work, and Luna/low mechanical work. Use native worker model overrides when exposed, and base nested-call availability on actual permissions. Remove outdated blanket claims about headless execution, fixed subagent schemas, and guaranteed model independence.
- Preserve existing CLI output files, publish advisor/committee results only after success, validate effort and timeout values, and enforce deadlines on macOS and Linux using Python 3.
- Add offline wrapper regression tests and CI; extend package checks to strict YAML, helper syntax, and tracked executable modes. Install check dependencies with `python3 -m pip install -r plugin/scripts/requirements-check.txt`.
- Document reusable migration practices in `MODEL-POLICY.md`; retain frozen research examples and add compatibility gates for classification and logprob workflows.
- Include Codex changes in the AI for Research notification trigger. Existing site descriptions still require editorial updates; the sync script deliberately preserves them.
- Premier models chair. `model-committee` now defaults to the Fable 5.1 chair, distinct from both member models. `/model-committee-opus` keeps the cheap in-session Opus chair; `/model-committee-astra` adds the GPT-side mirror (Astra chairs, the GPT member steps down to Sol). `/model-committee-fable` is an alias of the default; `/model-committee-sol` is retained as legacy.
- `codex-peer.sh` gains a `cross-check` mode and an effort ladder: `consult` defaults to `high`, `cross-check` and `implement` to `xhigh`; `--effort` still overrides per call.
- `advisor` is documented as an escalation from a working model up to Fable and refuses to run from a Fable session, since a second Fable is not a check; a Fable lead goes cross-vendor through `orchestrate`'s Astra peer or the committee instead.

- Add an idempotent Codex skill installer with dry-run and conflict reporting; preserve existing paths and document discovery and explicit invocation. Add installation regression tests.

## [2.25.1] — 2026-09-02

`spawn` corrected after a live dry run on herdr 0.8.0: `--cwd "$PWD"` is mandatory on `worktree create` and `worktree open` (herdr resolves the repository from the calling workspace, and the bare form checked out an unrelated repository); a fresh peer always blocks first on Claude Code's workspace-trust dialog and needs `agent send-keys`, which the `auto` classifier may refuse; `agent explain` prints five text lines with the detection rule, not a hook/screen label; `wait` can settle on `done` while `explain` says `idle`; `worktree remove` succeeds without `--force` on a running peer; the fold-back checklist now also closes the source workspace `worktree create` opens and removes the empty per-repo directory.

## [2.25.0] — 2026-09-02

Consolidation release: 43 skills become 38. Every pre-2.25 skill name still resolves; the absorbed names are alias commands that call the merged skill with its mode forced (`plugin/commands/<old-name>.md`, whitelisted in `check.sh`).

### Merged

- `orchestrate` replaces `fable-orchestrate` and `opus-orchestrate`. The skill reads the session model from the system prompt and takes the Fable 5.1 or Opus 5 lead role; `--lead fable|opus` and the two alias commands force it. `codex/46-orchestrate` is renamed `codex/orchestrate`.
- `paper-review-lite` absorbs `paper-review-lite-codex` as `--codex` cross-model mode; the drifted copies of the review specification are reconciled into one.
- `diverge` absorbs `diverge-codex` as `--codex` mode.
- `qualtrics-ops` absorbs `survey-flow-audit` as the read-only `audit` mode. The Codex twin is rebuilt from the plugin version, which carries four correctness fixes from August 2026 that had never been ported.
- `vlm-ocr` replaces `vlm-ocr-evaluation`, `vlm-ocr-pipeline`, and `post-ocr-cleanup` as one skill with `evaluate`, `run`, and `clean` phases.
- `replication-package` absorbs `fair-check` as a FAIR block inside its `audit` mode.

### Added

- `research-grill`: a rounds-based research interview (idea → question, question → design, design or draft → reviewer objections) with plain-language questions, a recommended answer each, facts fetched rather than asked, and every settled decision written to a wayfinder ticket or `decisions.md`. Student-safe. Credited to Matt Pocock's `grill-me`.
- `referee-response`: author-side response to peer review. Extracts every referee point, orders the revision by dependency, flags defensible pushbacks as questions, and builds the response letter with the substantive answers left to the author. Never writes the science.
- `text-classification` gains a resumable batch pipeline and rule-based baseline section (from the retired personal `llm-classification-audit`).
- `check.sh` asserts that both manifests state the directory skill count, that their versions match, and that this file has an entry for the version.

### Changed

- Model currency: "Fable 5" is "Fable 5.1" wherever it names the current model. Literature citations to older models are untouched.
- `journal-review` Phase 5 no longer depends on a personal `~/.claude/skills/sci-edit` install; it uses the linter when present and otherwise runs an inline tell-removal pass.
- `research-wayfinder` and `diverge` point at `research-grill` for the pre-planning interview instead of the third-party `grill-me`.
- Seventeen terse skill descriptions gained a "use when" half so the skill selector triggers on the task, not only the topic.
- Skill counts reconciled across README, both manifests, and the Codex README.

## [2.24.0] — 2026-08-17

- `doc-to-markdown`: read or convert PDFs and office documents, routing scanned material to the OCR skills and bulk intake to `research-repo`; the conversion script hardened.
- `qualtrics-ops`: five correctness fixes from live fielding (compound quota logic, EmbeddedField verdict and Cross quotas, EndSurveyOptions/QuotaMet at build time, ActionInfo as the quota trigger).
- Codex variants for the 2.23.0 skills.

## [2.23.0] — 2026-08-12

- Three new skills: `qualtrics-ops`, `survey-flow-audit`, `survey-data-audit`.

## [2.22.0] — 2026-08-08

- Audit pass recorded in `AUDITS.md`: `model-committee` chair variants collapsed into one skill with `/model-committee-fable` and `/model-committee-sol` aliases; 26 descriptions rewritten with a "use when" half; hub-and-spoke wiring for the text-analysis skills.
