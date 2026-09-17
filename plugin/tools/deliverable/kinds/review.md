# Kind: review

A referee report or an editor's note on someone else's manuscript.

## Interview
- The venue, the deadline, the manuscript version reviewed (file and hash), and whether a replication archive was available.
- The report's frame: recommendation categories the journal uses, confidential-to-editor section or not, word limit.
- What the review must not do: rewrite the science, reveal the reviewer, cite the reviewer's own unpublished work.

## Manifest defaults
- `sections_from: markdown-headings`, `sections_files: [referee_report.md]`
- `sources_of_truth`: the manuscript as received (`manuscript.md` or PDF), the journal's reviewer guidelines
- `checks`: `citations` (anything the report cites must resolve), `prose_tells`, `credentials`, `leaks` (no reviewer-identifying strings)
- `night_shift`: never enabled; a review is one sitting

## Lint questions
- Section: is each criticism anchored to a page or section of the manuscript; is it a defect of the work or a preference of the reviewer; is the requested change proportionate.
- Global: does the recommendation follow from the numbered points; are major and minor points separated; is anything in the report identifying or inappropriate for the author-visible section.

## Ship
`check_deliverable.py ship`, then the journal's submission form; the report and the manuscript version reviewed are kept together in the repo.

## Related skills
`journal-review` (drafts the report), `sci-edit lint` before submission.
