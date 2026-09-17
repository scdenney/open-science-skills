# Changelog

Versions are the `version` field shared by `plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; `plugin/scripts/check.sh` fails if they differ or if this file has no entry for the current version. Earlier history is in commit subjects and in `AUDITS.md`.

## [2.32.0] — 2026-09-17

- **The deliverable toolchain now ships with the library**, at `plugin/tools/deliverable/`: the deterministic gate, the run-preparation and adjudication scripts, the hook installer, and the five kind profiles. `deliverable-open` and `deliverable-lint` previously drove scripts from a separate `project_hygiene` checkout that existed on two machines and was published nowhere, so anyone installing the plugin got three deliverable skills of which two could not run. They now resolve `$DTOOL` from `$DELIVERABLE_TOOLS`, `${CLAUDE_PLUGIN_ROOT}/tools/deliverable`, a repository checkout, and only then a legacy `project_hygiene`. `check.sh` asserts the toolchain's layout, because `lint_prepare.py` resolves kind profiles relative to its own directory and the two directories must stay siblings.
- The old location keeps working. `project_hygiene/scripts/` now holds relative symlinks into the library, so the seven repositories and the installed git hooks that hardcode those paths keep resolving against a single copy rather than a fork. `install-hooks.sh` probes the bundled location first and the legacy paths last.
- **The deliverable pipeline is marked experimental and moved to the end of the catalog.** It is the one part of the library that does not enforce a methodological standard. It manages the writing project around an output, and only one of its five kinds is a research paper; the others are talks, course modules, book chapters, and referee reports. The section now says so, states that it composes with `research-repo` rather than competing with it and sits earlier than `paper-review-lite` rather than replacing it, credits the ideas it borrows, and warns that its interfaces may change without an alias. The three table entries are rewritten in the plain register the rest of the catalog uses.
- The three deliverable skills were listed as Claude-only. All three ship a complete Codex package, and the skills site already showed them as both, so the README was the wrong half of that contradiction. Corrected, and the Platform column audited in both directions across all 43 skills.

## [2.31.0] — 2026-09-17

- **Every skill is now on demand.** The eleven Claude skills and seventeen Codex skills that still matched implicitly now carry `disable-model-invocation: true` and `policy.allow_implicit_invocation: false` respectively. Nothing loads from context and nothing is suggested unprompted, so an idle session carries none of the library. The two platforms had also drifted apart on which skills matched implicitly (`tables`, `narrative-building`, `text-classification`, and `paper-tex` fired on Codex but not on Claude); they now agree because neither fires. `check.sh` asserts the flag on both sides.
- **The duplicate slash commands are gone.** Claude Code registers a plugin skill as `/oss:<name>` by itself, so the per-skill wrapper in `plugin/commands/` had been registering a second, identical menu entry for every skill, one showing the SKILL.md description and one showing only the H1. The 41 colliding wrappers are removed. `plugin/commands/` now holds only the eleven alias commands. `check.sh` asserts the inverse of what it used to: no command may share a skill's name, and every command must be a declared alias.
- **New skills `sitrep` and `finished`** under a new Repo Hygiene category, on both platforms. `sitrep` reports where a project actually stands, reading whatever handoff and log files the repository keeps, checking live git state, and flagging where the two disagree. `finished` records what changed into those same files at session close, separating verified work from work merely attempted. Both defer to a repository's own `.claude/commands/` or `.codex/prompts/` file when one exists. Claude 43 skills, Codex 42.
- `check.sh` hardening: the executable-bit assertion now globs every bundled `.sh` under `plugin/skills/` and `codex/` instead of checking five hardcoded paths, so a newly added helper is guarded the day it lands.
- **`deliverable-open` and `deliverable-lint` no longer hardcode a machine path.** Both pointed at `~/Documents/GitHub/resources/project_hygiene`, which does not exist on a Linux box where the directory is `github`, so the skills failed outright there. They now resolve `$GH`, `$RES`, and `$HYG` from `$OSS_GITHUB_ROOT` and both casings, and stop with a clear message when none exists instead of guessing.
- **`replication-package` can now verify a package instead of only reading it.** A new bundled `scripts/verify_package.py` checks seed, session info, lockfile, machine-specific absolute paths, and committed credentials, and hashes the data directory. With `--run` it copies the package to a temporary directory, executes the master script, and compares what appeared against the figure-table crosswalk. Execution is off by default and Step 6b requires explicit user authorization before it, because it runs code the package's author wrote. A declined or impossible run is recorded as NOT CHECKED rather than passed.
- **`/oss:verify`**, a new alias command, runs `verify_package.py` on its own: the fast "does my analysis still work and does it produce what I claim" pass, without the package grade, the FAIR block, or the audit report. `paper-review-lite` now runs the static tier automatically in orientation and hands the result to its Numbers and Replication Archive agents, which otherwise can only compare a manuscript against itself. A table that disagrees with what the code now produces is invisible to nine agents reading carefully, because the truth is not in the manuscript. Execution still needs explicit authorization everywhere it is offered, and on Claude that authorization is an `AskUserQuestion` prompt rather than a line of prose, because a clean-room run can take a long time and a question buried in a paragraph is easy to scroll past. Codex keeps the prose form, having no such tool.

- `check.sh` now covers bundled `.py` as well as `.sh` (tracked mode plus a compile check) and asserts the 1024-character description cap. Both caught live bugs: `paper-tex`'s `format_paper.py` was tracked `100644` on both platforms despite declaring a shebang, and `codex/research-grill`'s description was 1086 characters.


## [2.30.0] — 2026-09-14

- Three redundant alias commands removed: `/oss:fable-orchestrate`, `/oss:opus-orchestrate`, and `/oss:model-committee-fable`. The two orchestrate aliases only forced a lead that `/oss:orchestrate` already detects from the session model, and both told the user not to force it on a session running something else, so they were useful only in the case they warned against. `/oss:model-committee-fable` named the chair that `/oss:model-committee` already uses by default. `--lead fable|opus` still overrides detection. The skill count is unchanged at 41 Claude and 40 Codex; only commands were removed.
- README and `codex/README.md` corrected: the Codex library is 40 skills, not 37, in the platform table and the badge.

## [2.29.1] — 2026-09-09

- Copyedit pass over every skill description, the README skill tables and prose, and the pipeline guide, under the house rules (no em dashes or arrows, no colons or semicolons in running prose, one term per concept, no filler). Quoted trigger phrases, skill and model names, and code spans are unchanged, so triggering is unaffected. `research-grill` and `research-wayfinder` now sit under Ideation in the README.

## [2.29.0] — 2026-09-09

- Deliverable pipeline, three new Claude skills (41 total). `deliverable-open` interviews the author in rounds and writes the house files for a unit of work with a deadline and an audience: `deliverable.yml` (audience, deadline, claim, done-test, sources of truth, logical sections, which deterministic checks apply, a night-shift opt-in that defaults off), an append-only `HANDOFF.md`, a numbered `planning/` wiki, an `inbox/` for dictated braindumps, and for a talk the house deck template. `deliverable-intake` turns captures (inbox files, or chosen entries from the macwhspr dictation log) into one unified diff against the wiki, classifying and tracing every statement, leaving uncertain names and citations UNRESOLVED, and applying decisions only on assent. `deliverable-lint` is the whole-deliverable editorial review, detection only: the deterministic gate first and stop on failure, one Sonnet finder per section in parallel, one Opus global pass, adjudication with verified anchors, evidence-backed fabrication flags, and honest NOT-CHECKED coverage under a dollar budget; it never rewrites (that stays with `sci-edit manuscript`, serial and guarded).
- All three pipeline skills are on-demand (typed by name; the repo's `AGENTS.md` says when): auto-triggering was tried for intake and lint on 2026-09-09 and reverted the same day at the user's request. A manifest `knowledge_base:` field (a `research-repo` `sources/md/`) makes the gate warn on cited works with no source file, routes intake's unknown sources to `process-source`, and gives lint a fourth finder question, claim support against the source text.
- Codex parity, designed jointly with a Codex session on 2026-09-09: the manifest routing block is vendor-neutral (`agent:`), both vendors read the same session-start context from `project_hygiene/scripts/deliverable_context.py` (Claude via its SessionStart hook, Codex via an `AGENTS.md` paragraph) and write identical lint files through `lint_adjudicate.py`; the Codex library gains the same three skills. `check_deliverable.py ship` now refuses a release when the latest lint is stale or has an open P0. Intake never edits an existing HANDOFF entry; rejected lint findings live in `08-open-questions.md`.
- Lint contract, after the Codex review: `lint_prepare.py` reserves the run directory, freezes the input hash, and writes every worker input and the JSON output contract; `lint_adjudicate.py` keeps the frozen hash, marks a run stale, counts a section as checked only with full required coverage, downgrades unevidenced P0s, and derives the verdict from four conditions; `check_deliverable.py ship` blocks on a missing, stale, incomplete, or P0-carrying lint unless `--no-lint` is recorded in the receipt.
- Kind profiles (`project_hygiene/kinds/{talk,paper,module,chapter,review}.md`): interview, manifest defaults, lint questions, ship step, related skills per kind; one wiki per piece of research, one manifest per deliverable, one profile per kind.
- `docs/deliverable-pipeline.md` explains the architecture (principles, steps, files, kind profiles, integration with the rest of the library, the two-vendor setup, the commons) with a diagram that the three skills also show.
- The gate the skills call is `check_deliverable.py` in `scdenney/project_hygiene` (citations against the bib, Crossref and OpenAlex with a per-deliverable cache and an accept-with-note path; number snapshots; Jekyll facts and leaks; deck text budgets; credential and prose-tell scans; build; release receipts), installed as a tracked pre-commit hook by `install-hooks.sh`.

## [2.28.2] — 2026-09-08

- `paper-review-lite` calibrated for a Fable 5.1 lead. The orchestration effort rule now covers both leads (medium sustained, high for the Phase 4 adjudication). When Fable leads, Agent 1 (Content & Argument) runs on Fable at high instead of Opus, since it is the one Red Team dimension where reasoning quality dominates reading volume; Agents 2, 6, 7 stay on Opus and the mechanical agents on Sonnet. Agent 10 then checks Agent 1's findings on Opus and the rest on Fable so checker and checked never share a model.
- New `--codex-effort <low|medium|high|xhigh>` argument (default `xhigh`) for `--codex` mode and the `paper-review-lite-codex` alias sets the reasoning effort for every Codex call in the run.

## [2.28.1] — 2026-09-08

- `spawn` re-verified by a live dry run on herdr 0.9.0 (protocol 22, Claude hook v9, Codex hook v8). Four observed changes are now documented in the Claude and Codex skills: `agent start` exits 1 with `agent_not_ready` while a fresh peer sits on the workspace-trust dialog (the peer is running; clear the dialog and poll `agent explain` for `idle` before prompting, since the agent record lags the screen); checkouts are named `spawn-<slug>` rather than `worktree-<adjective>-<noun>-<hex>`; `workspace close` on a source workspace is refused with `workspace_group_close_required` while worktree workspaces are open and `--group` closes the group without removing checkouts; `worktree` commands gained `--trust-repository` and `--focus|--no-focus`. A note records that `herdr machine add` aggregates remote servers in the client but the `agent`, `worktree`, and `workspace` CLI still address only the local server, so peers stay local.

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
