# The deliverable pipeline

How this library supports creative, knowledge-based work – a talk, a paper, a course module, a book chapter, or a referee report – across sessions and two agent vendors. It preserves context, prevents unchecked drafts from shipping, and avoids loading everything into every session. It serves as a guide for others and as the author's reference for the architecture.

<p align="center"><img src="../plugin/skills/deliverable-open/assets/pipeline.svg" alt="The eight-step deliverable pipeline over three layers: one wiki per piece of research, one manifest per deliverable, one shared commons" width="960"></p>

## Five principles

1. **One wiki per piece of research, one manifest per deliverable, one profile per kind.** The paper, its talks, and its referee responses share one `planning/` wiki. Each deliverable has its own `deliverable.yml` and `HANDOFF.md`. The deliverable's kind selects the advice, including what to ask at open, which checks apply, what lint looks for, and how it ships. An agent holds one profile at a time.
2. **Deterministic before generative.** A script resolves citations, checks numbers against the snapshot of record, and catches leaks at every commit. It runs in seconds and costs nothing. Language-model review runs afterward and stops if the script fails. Every defect that previously shipped from this estate was a fabricated source or stale number. Each was catchable through a lookup.
3. **Detection is parallel. Revision is serial.** Many inexpensive readers can assess sections at once. Revision affects only one section at a time and never rewrites a whole document in one prompt. A finding is a claim about a line, with a verbatim quote and verifiable evidence for anything blocking. Agreement between two models is not evidence.
4. **Repository files are the authority. Nothing lives only in an agent's memory.** State is an append-only `HANDOFF.md` with the current entry at the top. Raw captures are never edited. A script that both vendors run provides session context. A vendor hook does not.
5. **On demand, by name.** Pipeline skills do not activate from phrases. The repository's `AGENTS.md` states when to invoke each skill. The author or agent types its name. This requires one habitual line and provides predictability.

## The eight steps

| Step | Who | What happens | Files |
|---|---|---|---|
| 1 Open | author + agent, once | `/oss:deliverable-open`: an interview driven by the kind profile | `deliverable.yml`, `HANDOFF.md`, `planning/`, `inbox/`, `checks/` |
| 2 Braindump | author | dictate or type into a new `inbox/` file; never edited | `inbox/YYYY-MM-DD-slug.md` |
| 3 Intake | agent, author assents | `/oss:deliverable-intake`: one diff against the wiki, every statement classified and traced; unknown sources stay UNRESOLVED and go to `process-source` | `planning/*.md`, capture → `.done.md` |
| 4 Draft | author + agent | the source, section by section (`sci-edit` for prose, guarded) | `content.md`, `.tex`, `.md` |
| 5 Gate | automatic | `check_deliverable.py --fast` at every commit; CI reruns it | `.githooks/pre-commit`, `checks/citations.json` |
| 6 Lint | agent, on demand or night shift | `/oss:deliverable-lint`: `lint_prepare.py` freezes inputs and writes one brief per section; finders in parallel; one global pass; `lint_adjudicate.py` verifies anchors and derives the verdict | `checks/<date>/findings.json`, `report.md` |
| 7 React | author | dictate reactions; accepted findings become tasks, rejected ones are recorded so they are not raised again | `inbox/`, `08-open-questions.md` |
| 8 Ship, close | author + agent | `check_deliverable.py ship` (gate passed, lint fresh and complete, zero P0; modules may waive with a prompt); `/finished` prepends the stamped handoff entry and asks once about the commons | `checks/release.json`, `HANDOFF.md` |

## The files

```
paper/                        the piece of research
  planning/                   ONE wiki: 00-README.md (index, sources of truth, decisions), numbered files, 08-open-questions.md
  manuscript/                 the paper (an Overleaf submodule, say); its own deliverable.yml + HANDOFF.md
  talks/apsa-2026/            a talk: deliverable.yml (planning_dir: ../../planning), HANDOFF.md, inbox/, checks/, content.md, src/
  sources/{og,md}/, references.bib   the knowledge base (research-repo layout)
AGENTS.md  (CLAUDE.md -> symlink)    rules only, with a "Deliverable pipeline" paragraph saying when to invoke what
```

`deliverable.yml` names the audience, deadline, claim, done-test, sources of truth, logical sections, applicable checks, the knowledge base, commons tags, and an `agent:` routing block that both vendors read. Sections are logical and never require a physical split. `HANDOFF.md` has a two-line header and dated `## YYYY-MM-DD (topic)` entries, newest first. Each entry records the agent, time, Decision, Completed, Finding, and Next actions. Another session's entry is never revised.

## Kind profiles

One file per kind in the `project_hygiene` checkout's `kinds/` (resolved as `$HYG/kinds/`, see the skills) contains the interview questions beyond the common five, manifest defaults, lint questions that `lint_prepare.py` appends, the ship step, and related skills. A talk asks about the slot and what stays off the slides. It ships to a URL. A paper asks about the venue and the pre-registration. It ships through `paper-review-lite` and `presubmit`. A module asks about the calendar and students. It ships per session without a required lint. A chapter answers to the book map. A review answers to the manuscript version it read.

## Integration with the rest of the library

| Kind | Before drafting | While drafting | Before shipping |
|---|---|---|---|
| paper | `research-grill`, `research-wayfinder`, `pre-registration-writing` | `paper-tex`, `figures`, `tables`, `sci-edit manuscript` | `deliverable-lint`, then `citation-check`, `fact-check`, `methods-reporting`, `paper-review-lite`, `presubmit`, `replication-package` |
| talk | the deck template (`resources/deck-template/`) | `figures` | `deliverable-lint` |
| module | `research-repo` for a corpus companion | `sci-edit` for guides | `deliverable-lint` (optional), the site's own CI |
| review | `journal-review` | `sci-edit lint` | `deliverable-lint` |
| any | `process-source` feeds the knowledge base that the gate and lint read | `deliverable-intake` after every braindump | `orchestrate` when a disputed finding needs a decorrelated check |

## Two vendors, one infrastructure

Claude and Codex read and write the same files through the same scripts in the `project_hygiene` checkout's `scripts/` (`$HYG/scripts/`): `deliverable_context.py` (session start; Claude via a hook, Codex via the `AGENTS.md` paragraph), `check_deliverable.py` (the gate), `lint_prepare.py` and `lint_adjudicate.py` (the review), `commons.py` (the shared layer). The Codex library carries the same three skills (`$deliverable-open`, `$deliverable-intake`, `$deliverable-lint`). A Codex session reviewed the design blind, and the results were reconciled. The exchange is the first thread in the commons.

## The commons

`research/commons/` contains shared sources and bibliography, one-fact cards with evidence and `supersedes`, threads where agents leave notes for each other, and a JSON-lines index. A session sees only index lines that match its manifest's tags. At closure, writes are proposals that the author approves. A rejected proposal leaves a trace in the deliverable rather than in the commons.

## What to watch

Determine whether manifests continue to be updated after creation. If they do not, the manifest is ceremony and `HANDOFF.md` alone suffices. Determine whether section fan-out finds more than a single whole-document pass. If it does not, collapse it. Determine whether the pre-commit gate is bypassed. If it is, CI is the only gate. Determine whether fabricated *claims about real sources* dominate fabricated *sources*. If they do, move weight from the citation gate to `fact-check` against the knowledge base.
