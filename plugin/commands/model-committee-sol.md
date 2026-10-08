# Model Committee (Sol-chaired)

Run the `model-committee` skill with the **GPT-6.1 Sol chair**. Two things change from the default, not one: Sol (`gpt-6.1-sol`) chairs instead of Fable, and the GPT member steps down from Astra to `gpt-6-sol` so the chair is not also a member. Members are therefore GPT-6 Sol and Claude Opus; Sol aggregates the scores, applies the precommitted tie rule, and runs the compatible-component synthesis. Delegate that step via `codex-member.sh --model gpt-6.1-sol --effort xhigh`. This is the cheaper GPT-side chair; prefer the Astra chair (`/model-committee-astra`) for a close or high-stakes call.

Follow the skill's chair table and protocol as written. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
