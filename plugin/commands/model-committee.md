# Model Committee

Run the `model-committee` skill with the **Fable 5.1 chair** (the default). Members are GPT-6 Astra and Claude Opus 5; the chair sits outside both, so it cannot vote its own prior a third time. Fable validates schemas, aggregates the weighted scores, applies the precommitted tie rule, and writes the decision. Delegate that step via `claude-member.sh --model claude-fable-5-1 --effort high` unless the session is verifiably running Fable. Other chairs: `/model-committee-opus` (cheap, in-session; the chair is also a member), `/model-committee-astra` (Astra chairs; the GPT member steps down to Sol), `/model-committee-sol` (legacy).

First determine whether the task genuinely benefits from committee treatment, then freeze a shared brief and rubric, collect blind proposals, exchange critiques, let both models revise, cross-rank the revised candidates, and apply the precommitted decision rule. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
