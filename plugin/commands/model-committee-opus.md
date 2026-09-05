# Model Committee (Opus-chaired)

Run the `model-committee` skill with the **Claude Opus 5 chair**. Members are unchanged — GPT-6 Astra and Claude Opus 5. This is the cheap committee: Opus is normally the model already running in-session, so the post-round-3 chair step usually costs no extra external call. Its cost is dependence — the chair is the same model as the Claude member — so it must not vote a third time, and its arithmetic needs the mechanical audit the skill specifies. Chair in-session only when the session is verifiably running Opus 5; otherwise delegate via `claude-member.sh --model claude-opus-5 --effort high`.

Prefer the default Fable chair (`/model-committee`) or the Astra chair (`/model-committee-astra`) for a close or consequential call; use this one when the decision is consequential but not close and the saving matters.

Follow the skill's chair table and protocol as written. Use this for consequential, ambiguous choices that require one answer; route factual verification, independent-coder reliability, open-ended ideation, and routine implementation to the simpler matching workflow.

$ARGUMENTS
