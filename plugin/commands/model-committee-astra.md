# Model Committee (Astra-chaired)

Run the `model-committee` skill with the **GPT-6 Astra chair**. Two things change from the default, not one: Astra chairs instead of Fable 5.1, and the GPT member steps down one tier from Astra to `gpt-5.6-sol` so the chair is not also a member. Members are therefore GPT-5.6 "Sol" and Claude Opus 5; Astra validates schemas, aggregates the weighted scores, applies the precommitted tie rule, and runs the compatible-component synthesis from outside both members. Always delegate that step via `codex-member.sh --model gpt-6-astra --effort xhigh` — this skill loads inside Claude Code, so the session is never Astra.

This is the GPT-side mirror of the Fable default: the row to use when the deliberation should be adjudicated by the *other* vendor's premier model, or when a Fable session wants the committee chaired from outside its own family.

Follow the skill's chair table and protocol as written. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
