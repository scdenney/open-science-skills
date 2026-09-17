# Kind: talk

A conference paper, seminar, keynote, or lecture given once, with slides.

## Interview
- Slot length and format (ten-minute panel slot, 45-minute seminar, keynote); whether there is a discussant and whether the paper was circulated.
- What stays off the slides on purpose (diagnostics, registration accounting, robustness) and where it lives (SI, appendix slides, notes).
- Where the numbers come from: the manuscript's `numbers*.tex` snapshot of record, and which data tables in `src/charts.py` copy it.
- Publication: the URL the QR code will point at, and whether the deck is public before or after the talk.

## Manifest defaults
- `sections_from: content-keys`, `sections_files: [content.md]`
- `sources_of_truth`: `content.md`, `notes.md`, the manuscript's `numbers.tex` and `references.bib`
- `checks`: `citations` (bib, `cite_fields: true`, `scan: [content.md]`), `numbers` (source, snapshot, `snapshot_in: [src/charts.py, notes.md]`, tables), `prose_tells` (`scan: [notes.md, content.md]`), `credentials`; `deck_budget` once budgets are measured for the deck system
- `build`: `python3 src/build.py --html`, artifacts `[index.html]`

## Lint questions
- Section: one idea per slide, and is the headline the finding rather than a topic label; does every number on the slide appear in the snapshot; is the citation string an `Author Year` the gate can resolve.
- Global: do the cumulative timings in `notes.md` fit the slot with a margin for the chair; do the appendix slides answer the objections the brief anticipates; is the spoken claim in the notes the same claim the slides show.

## Ship
`python3 src/build.py` (HTML and PDF), `check_deliverable.py ship`, copy `index.html` to the site's `assets/slides/<slug>/`, regenerate `src/qr.svg` for that URL, commit and push the site.

## Related skills
`figures` for chart design; the deck template at `resources/deck-template/`; `sci-edit` for the notes, never for slide fragments as prose.
