# Model Committee (Fable-chaired)

Run the `model-committee` skill with the **Fable 5.1 chair**. Members are unchanged — GPT-5.6 "Sol" and Claude Opus 5 — and only the post-round-3 step moves: Fable validates schemas, aggregates the weighted scores, applies the precommitted tie rule, and writes the decision without voting its own prior a third time. Delegate that step via `claude-member.sh --model claude-fable-5-1 --effort high` unless the session is verifiably running Fable.

Follow the skill's chair table and protocol as written. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
