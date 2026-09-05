# Model selection and migration

Reviewed against [OpenAI’s current model guidance](https://developers.openai.com/api/docs/guides/latest-model) and [Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) on 2026-09-05.

Use `gpt-6-astra` for demanding orchestration, research judgments, manuscript review, and cross-vendor consults. Effort follows the job, not the model: a routine fresh-perspective consult runs at `high`; the blind high-stakes cross-check, the committee member, the advisor seat, and any write-capable run at `xhigh` (`codex-peer.sh` sets this from `--mode`). These are library choices, not benchmarked optima for Astra. Reserve `max` for demonstrated need. Astra supports `low`, `medium`, `high`, `xhigh`, and `max`; it does not support `none`.

For Codex orchestration, preserve the lead's selected Astra effort. Route demanding independent units to Sol/high, bounded work to Terra/medium, and mechanical tasks to Luna/low. Prefer native model overrides with self-contained briefs; full-history inheritance is not cheaper routing.

The premier models orchestrate. Fable 5.1 and GPT-6 Astra are the two frontier tiers; each leads its own vendor's orchestration, reaches the *other* for a cross-vendor check, and chairs the committee from outside both members (Fable by default, Astra via `/model-committee-astra`, in which case the GPT member steps down to `gpt-5.6-sol`). The advisor is the opposite shape — an escalation from a working model up to its vendor's premier — so a premier session does not call it.

Keep `gpt-5.6-terra` for bounded work and `gpt-5.6-luna` for mechanical or validated high-volume tasks. Preserve user-selected models, named compatibility modes, frozen research runs, and historical examples. `/model-committee-sol` still selects Sol with a Terra member. The legacy `sol-advisor.sh` filename now defaults to Astra and accepts explicit overrides.

For other repositories, apply the same task-based migration:

1. Inventory executable calls, defaults, wrappers, model selectors, skill instructions, examples, and tests. Distinguish active defaults from research provenance and deliberately named alternatives.
2. Verify the exact model and needed capabilities against current official documentation. Model IDs do not necessarily identify immutable snapshots, and documentation does not prove account access.
3. Change only the routes that benefit. Prefer Responses for new OpenAI API integrations; check reasoning, output schemas, tools, and logprobs before migrating an existing endpoint. Validate classifiers and OCR pipelines against representative human-labeled data before changing their production model.
4. Use the actual runtime’s model override fields and permissions. Instructions cannot change the running lead. Full-history forks may inherit the parent; fresh workers can use explicit model overrides when exposed. Headless mode and approval policy do not determine sandbox or network access by themselves.
5. Keep delegation briefs compact, run independent work concurrently when authorized, and inspect returned evidence. A fresh context or different vendor can expose additional errors; agreement does not establish validity or statistical independence.
6. Test wrappers without paid calls first, then use a small representative live evaluation when needed. Record the requested and reported model, effort, prompt, run date, outcome, latency, and usage. Report unavailable models instead of silently substituting them.

The OpenAI CLI wrappers in this library require Python 3 for portable deadlines. They preserve existing output paths; choose a new path for each run. Advisor and committee drivers publish the final answer only after successful completion. The peer driver streams a transcript, so a partial transcript after failure is diagnostic evidence, not a completed response.

Install check dependencies with `python3 -m pip install -r plugin/scripts/requirements-check.txt`. Run `bash plugin/scripts/check.sh` and `python3 plugin/scripts/test-codex-wrappers.py` and `python3 plugin/scripts/test-install-codex.py` after changes. Keep the Claude flat mirrors synchronized. Review site copy separately: the AI for Research sync script preserves existing hand-authored descriptions and does not automatically rewrite model names in them.
