# Kind: chapter

One chapter of a book, drafted against a book-wide argument map.

## Interview
- The chapter's argument in one paragraph and what it builds on (which earlier chapters, which dissertation or paper text it reuses).
- The book-wide invariants it must honour (cohort rules, definitions, the canonical tables) and where they are recorded.
- The chapter's own sources of truth: analysis outputs, `numbers.tex` if any, the chapter bib.
- State: outline, draft, revision; what "done" means for this pass.

## Manifest defaults
- `sections_from: latex` or `markdown-headings`
- `planning_dir`: the book-level wiki (`chapters/CLAUDE.md` and the chapter's `README.md` are declared, not moved)
- `knowledge_base`: the book's `knowledge_base/md`
- `checks`: `citations` (chapter bib, `verify_bib: true`), `numbers` where results are quoted, `prose_tells`, `credentials`

## Lint questions
- Section: does the section advance the chapter's stated argument or digress; is every empirical claim tied to a source or to the book's own analysis; are the book-wide definitions used with their canonical wording.
- Global: does the chapter deliver what the book map assigns it and nothing another chapter owns; are cross-references to other chapters consistent with their current state; does the chapter reuse earlier text with its numbers re-verified.

## Ship
A chapter ships to the book, not to a venue: `check_deliverable.py ship` at each pass, and the chapter's `State` line in the book map updated at closure.

## Related skills
`narrative-building`, `literature-review`, `citation-check`, `sci-edit manuscript`.
