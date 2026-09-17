# Kind: paper

A journal article, research note, or working paper, usually LaTeX in an Overleaf submodule.

## Interview
- Venue and its limits (word count, abstract length, reference style, anonymization), and the submission or resubmission date.
- Pre-registration: the registry URL and the snapshot of record; every result number resolves through `numbers.tex`.
- Which files are the manuscript (`main.tex`, `si.tex`, `sections/`), and whether the body is one file or split (sections are logical either way; never split a file for the pipeline).
- The knowledge base: `sources/md/` and `references.bib`; whether `verify_bib` should run (yes when fabricated entries are the risk).

## Manifest defaults
- `sections_from: latex`, `sections_files: [manuscript/main.tex]` (or the `sections/` files in order)
- `sources_of_truth`: the manuscript files, `numbers.tex`, `references.bib`, the pre-analysis plan
- `knowledge_base: sources/md` (or the commons)
- `checks`: `citations` (bib, `verify_bib: true`, scan the `.tex` files), `numbers` (source, snapshot, `snapshot_in` the files that quote it), `prose_tells`, `credentials`
- `build`: `make -C manuscript all` or `latexmk`, artifacts `[manuscript/main.pdf]`

## Lint questions
- Section: does each paragraph's claim have a citation or a result behind it; are estimand, design, and estimator named with one term each; does the section quote numbers only through the snapshot macros.
- Global: does the introduction promise what the results deliver; do the hypotheses in the pre-registration appear with the same numbering and direction; does the discussion claim only what the design identifies; are limitations stated where a referee would raise them.

## Ship
`check_deliverable.py ship` after `make all`; then `paper-review-lite` at a milestone and `presubmit` before submission; the Overleaf submodule is committed and pushed before the parent pointer.

## Related skills
`paper-tex`, `methods-reporting`, `citation-check`, `fact-check`, `figure-table-audit`, `replication-package`, `referee-response` (for the revision), `sci-edit manuscript` (serial, guarded rewrite).
