<p align="center">
  <img src="https://img.shields.io/badge/OpenAI_Codex-37_open--science_skills-111111?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Codex — 37 open-science skills">
</p>

# Codex skills

This directory contains 37 Codex-native Open Science Skills. They mirror the Claude Code library with two intentional differences:

- `presubmit` is omitted.
- [`orchestrate`](orchestrate/SKILL.md) is the Codex-native version of the plugin's lead-detecting `orchestrate`: `gpt-6-astra` at the selected effort owns orchestration, routing demanding work to Sol and bounded work to Terra and reserving Luna for tightly specified mechanical work. It was named `46-orchestrate` before v2.25.0.

The Claude Code aliases for retired names (`diverge-codex`, `paper-review-lite-codex`, `survey-flow-audit`, `fair-check`, the three OCR names, the two orchestrate leads) have no Codex counterpart; use the merged skill and name the mode (`$diverge --codex`, `$qualtrics-ops audit`, `$vlm-ocr clean`, and so on).

Every skill is a self-contained directory with `SKILL.md`, `agents/openai.yaml`, and only the references, scripts, or assets it needs. Codex supports these skills in the CLI, IDE extension, and app.

## Install

From the repository root, preview and install user-wide symlinks:

```bash
python3 plugin/scripts/install-codex.py --all --dry-run
python3 plugin/scripts/install-codex.py --all
```

The installer creates missing links, accepts correct existing links, and reports conflicting files, directories, or links without replacing them. A conflict returns a nonzero exit code; inspect it before making any change. Links follow this checkout's edits, including uncommitted changes.

For selected skills or a single repository:

```bash
python3 plugin/scripts/install-codex.py --skill orchestrate model-committee model-council-voting advisor spawn
python3 plugin/scripts/install-codex.py --skill orchestrate --target /absolute/path/to/repo/.agents/skills
```

Invoke a skill as `$citation-check`, `$survey-design`, or another `$skill-name`. Codex can also load most skills implicitly from the task description. Restart Codex only if a new or changed skill does not appear automatically.

`$orchestrate` delegates work; `$model-committee` deliberates toward a decision; `$model-council-voting` designs independent research coding and voting. Explicit-only means a skill requires a direct invocation, not that it should be absent from the picker. If an installed skill is missing, refresh discovery, then restart Codex if needed. Use the exact `$skill-name`; do not enable implicit invocation to work around a stale picker.

See the official [Codex skills documentation](https://developers.openai.com/codex/skills) for discovery scopes and invocation behavior.

## Catalog

| Area | Skills |
|---|---|
| Project setup | [`research-repo`](research-repo/SKILL.md) |
| Orchestration | [`orchestrate`](orchestrate/SKILL.md), [`advisor`](advisor/SKILL.md), [`spawn`](spawn/SKILL.md) |
| Ideation | [`diverge`](diverge/SKILL.md), [`research-grill`](research-grill/SKILL.md) |
| Research design | [`conjoint-cleaning`](conjoint-cleaning/SKILL.md), [`conjoint-design`](conjoint-design/SKILL.md), [`conjoint-diagnostics`](conjoint-diagnostics/SKILL.md), [`cross-national-design`](cross-national-design/SKILL.md), [`list-experiment`](list-experiment/SKILL.md), [`qualtrics-ops`](qualtrics-ops/SKILL.md), [`research-wayfinder`](research-wayfinder/SKILL.md), [`survey-data-audit`](survey-data-audit/SKILL.md), [`survey-design`](survey-design/SKILL.md) |
| Analysis | [`llm-calibration-logprobs`](llm-calibration-logprobs/SKILL.md), [`model-committee`](model-committee/SKILL.md), [`model-council-voting`](model-council-voting/SKILL.md), [`text-classification`](text-classification/SKILL.md), [`topic-modeling`](topic-modeling/SKILL.md) |
| Corpus processing | [`doc-to-markdown`](doc-to-markdown/SKILL.md), [`vlm-ocr`](vlm-ocr/SKILL.md) |
| Writing and reporting | [`hypothesis-building`](hypothesis-building/SKILL.md), [`literature-review`](literature-review/SKILL.md), [`methods-reporting`](methods-reporting/SKILL.md), [`narrative-building`](narrative-building/SKILL.md), [`paper-tex`](paper-tex/SKILL.md), [`pre-registration-writing`](pre-registration-writing/SKILL.md) |
| Figures and tables | [`figure-table-audit`](figure-table-audit/SKILL.md), [`figures`](figures/SKILL.md), [`tables`](tables/SKILL.md) |
| Manuscript QA | [`citation-check`](citation-check/SKILL.md), [`fact-check`](fact-check/SKILL.md), [`replication-package`](replication-package/SKILL.md) |
| Review and submission | [`journal-review`](journal-review/SKILL.md), [`paper-review-lite`](paper-review-lite/SKILL.md), [`referee-response`](referee-response/SKILL.md) |

## Variant notes

**`$model-committee` and its chairs.** The default members are Astra/xhigh and Claude Opus 5/high, chaired by Fable 5.1/high. Use `chair: astra` for an Astra/xhigh chair with Sol/xhigh as the GPT member; `chair: opus` for the explicit Opus chair; or `chair: sol` for the legacy Sol chair with a Terra member. Claude’s `-astra`, `-opus`, `-fable`, and `-sol` command aliases map to these parameters in Codex. Chairs aggregate under the predeclared rule without adding a third vote; different tiers do not establish independence.

Member drivers need authentication and the network/process access permitted by the parent. Restricted sandboxes have blocked earlier nested calls; headless execution or approval `never` alone does not prohibit them. Report real errors and never fabricate a member response.

**`$diverge --codex`** uses a fresh Codex subagent context. It does not claim a second model family.

**`$paper-review-lite --codex`** keeps cross-model review by using Codex as lead and Claude Code's `claude -p` interface as the independent peer. It discloses and confirms external-credit use before running. Under sandbox, a `claude -p` call was observed to hang rather than complete, because network access is restricted. Read the `SKILL.md` before assuming a stalled call will resolve on its own.

**`$orchestrate`** is explicit-invocation only. Astra leads at the session's selected effort, verified against current-thread metadata. Sol/high handles demanding separable work, Terra/medium handles bounded work, and Luna/low handles mechanical tasks. Prefer native model overrides with self-contained briefs and `fork_turns="none"`; use permitted CLI workers when native routing is unavailable. Keep trivial work local and inspect worker evidence.

**`$spawn`** drives full peer sessions through the herdr socket (`~/.config/herdr/herdr.sock`), which lives outside the workspace. Verified 2026-08-06 on the Codex CLI (gpt-5.6-sol): under `workspace-write` the socket connect fails with `PermissionDenied: Operation not permitted`. Under `danger-full-access`, `herdr status` connects and reports the server. A Codex lead therefore needs an explicitly authorized full-access session to spawn, or it prints the exact command sequence for the user to run in a normal shell. The skill's preflight gate encodes this, fail-closed. Explicit-invocation only.

**`$advisor`** defaults to Astra at `xhigh` for a separate, read-only review of a demanding decision. Lower effort or explicitly choose Terra for a routine consult. The legacy `sol-advisor.sh` path remains compatible. The driver refuses existing output paths and publishes a final response only after a successful call.
