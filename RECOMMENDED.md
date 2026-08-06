# Recommended companion skills

Skills I did not write, recommend without reservation, and in two cases build on directly. They are not part of the Open Science Skills plugin and are not counted in its badges; install them from their own home. This page exists to say plainly which outside work this library leans on, and where the lineage runs.

## mattpocock/skills — Matt Pocock (MIT)

[mattpocock/skills](https://github.com/mattpocock/skills) — "Skills for Real Engineers." Install the whole set as a plugin (`claude plugins install mattpocock-skills`) or copy editable single skills (`npx skills@latest add mattpocock/skills --skill=<name>`). Faithful copies of the five skills below are kept, unmodified, at [`third-party/mattpocock/`](third-party/mattpocock/), pinned to the exact version retrieved, under his MIT license.

### grill-me / grilling — pairs with `diverge` (Ideation)

A relentless interview that maps a plan as a design tree, asking the whole **frontier** each round (every question whose prerequisites are settled, numbered, each with a recommended answer). Facts get looked up by sub-agents. Decisions go to the user. The session ends only when the frontier is empty and nothing is silently assumed. Use it the moment an idea is worth taking seriously (a design, a research question, a paper's framing), before you know what it involves. In this library's terms it is the interview that belongs **before** `diverge` — grill the plan until the decision tree is resolved, then diverge on genuinely distinct approaches to the settled problem. `research-wayfinder`'s live tickets run the same frontier-interview move.

### wayfinder — the source concept for `research-wayfinder` (Research Design)

Plans a chunk of work too big for one agent session as a shared map of decision tickets on an issue tracker, resolved one at a time — the session stops being the unit of work, and the context window stops being the source of truth. Recommended as-is for software projects; `research-wayfinder` is this library's adaptation of the same mechanics to experimental design, with tickets for estimands, identification, power, measurement, and analysis plans instead of specs, and `pre-registration-writing` as the exit.

### handoff / claude-handoff — the seed of `spawn` (Workflow & Orchestration)

`handoff` compacts the current conversation into a document a fresh agent can pick up: artifacts referenced by path instead of duplicated, a suggested-skills section, secrets redacted. `claude-handoff` (upstream in-progress) goes one further and launches the successor itself with `claude --bg`. This library's `spawn` generalizes exactly that move — environment detection (herdr, tmux, `claude --bg`), a git worktree per task, contract briefs, and lifecycle management for N peers. For the lightweight original, install his; for the full multi-session tier, `/oss:spawn`.

---

All five — grill-me, grilling, wayfinder, handoff, claude-handoff — are Matt Pocock's work, MIT-licensed. The kept copies are unmodified; the adaptations (`spawn`, `research-wayfinder`) credit the lineage in their own Heritage notes.
