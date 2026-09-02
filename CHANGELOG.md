# Changelog

Versions are the `version` field shared by `plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; `plugin/scripts/check.sh` fails if they differ or if this file has no entry for the current version. Earlier history is in commit subjects and in `AUDITS.md`.

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
