## Deliverable pipeline

This repository uses the deliverable pipeline. A deliverable, such as a talk, paper, course module, chapter, or referee report, is a folder with a `deliverable.yml` manifest and an append-only `HANDOFF.md`. Its research project has one shared `planning/` wiki. Pipeline skills run only when invoked by name.

At session start, find the nearest `deliverable.yml` from the task's path, or else the working directory, stopping at the repository root. Run `python3 ~/Documents/GitHub/resources/project_hygiene/scripts/deliverable_context.py --root <that directory>`. Read its output: the manifest, current `HANDOFF.md` entry, planning index, unprocessed captures in `inbox/`, and commons index lines matching the manifest's tags.

When the user dictates or types a braindump, write it verbatim to `inbox/YYYY-MM-DD-<slug>.md`, then invoke the intake skill: Claude: `/oss:deliverable-intake`; Codex: `$deliverable-intake`. When the user requests a review of the whole deliverable, or before a release, invoke the lint skill: `/oss:deliverable-lint` or `$deliverable-lint`. When the user opens a new deliverable, invoke `/oss:deliverable-open` or `$deliverable-open`. Before a release, run `python3 ~/Documents/GitHub/resources/project_hygiene/scripts/check_deliverable.py ship --root <dir>`. For a course module, ask first whether to lint, because lint is not required.

At session end, invoke `/finished` or `$finished`. It prepends a dated, stamped entry to `HANDOFF.md` and asks once whether anything should be promoted to the research commons. Never revise another session's `HANDOFF.md` entry. Never edit a file in `inbox/`. Never store session state in `~/.claude/projects/*/memory/`.
