# Paper formatter (LaTeX)

Typeset the draft below as a house-style LaTeX paper and build the PDF. Detect the input format and convert the body with pandoc, wrap it in the EB Garamond template under `assets/`, and build with latexmk via `scripts/format_paper.py`. Then do the house-specific finishing by hand: `\figcap` title+note captions, `[H]` floats, a single-spaced title block with the introduction on its own page, and author-date (`apsr`) citations. If a target journal is named, prepare for it — spacing, page limit, anonymization, disclosures, citation style. Leave the output folder clean: the driver removes latexmk byproducts (`.aux`, `.log`, `.fls`, `.blg`, …) after its builds, and after any hand rebuild finish with `format_paper.py --clean --out build`.

$ARGUMENTS
