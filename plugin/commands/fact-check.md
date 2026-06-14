# Fact Check

Fact-check the claims in the manuscript below against their cited sources. **First run the pre-flight gate:** if there is no per-source Markdown knowledge base, or raw PDFs/docs are still unconverted, refuse to run and return a `Pre-flight: NOT READY` checklist that tells the user to convert sources with `process-source` first. If the knowledge base is ready, run `citation-check` (in-text/reference parity and source existence). Then, for each in-text citation or footnote that backs a substantive claim, locate the source's knowledge-base Markdown file (`sources/md/` or `knowledge_base/md/`) and verify the source actually supports the claim — flagging contradiction, overclaiming, scope creep, stale numbers, misattribution, and sources missing from the knowledge base. Quote the supporting or contradicting passage for every verdict.

$ARGUMENTS
