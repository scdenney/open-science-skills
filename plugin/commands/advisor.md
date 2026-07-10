# Advisor

Consult Fable 5 as an independent, stronger second reviewer, at the same reasoning-effort level this session is currently running at ($CLAUDE_EFFORT, read automatically). Use before committing to an interpretation or a substantial piece of writing/analysis, when stuck, when considering a change of approach, or when you believe a task is complete and want a check before finalizing. Fallback for when the native advisor tool reports itself unavailable.

Compose a self-contained briefing first — this is an isolated consult, not the native tool's automatic transcript forwarding — then run `scripts/fable-advisor.sh` per the skill's Steps. Read-only advisory: the spawned session cannot edit files. See the `advisor` skill for the full mechanism, the effort-calibration note, and when to weigh disagreement rather than silently pick a side.

$ARGUMENTS
