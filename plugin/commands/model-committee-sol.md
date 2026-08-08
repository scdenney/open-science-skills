# Model Committee (Sol-chaired)

Run the `model-committee` skill with the **GPT-5.6 "Sol" chair**. Two things change from the default, not one: Sol chairs instead of Opus 5, and the GPT member drops from Sol to `gpt-5.6-terra` so the chair is not also a member. Members are therefore GPT-5.6 "Terra" and Claude Opus 5; Sol aggregates the scores, applies the precommitted tie rule, and runs the compatible-component synthesis from outside both members. Delegate that step via `codex-member.sh --model gpt-5.6-sol --effort xhigh`.

Follow the skill's chair table and protocol as written. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
