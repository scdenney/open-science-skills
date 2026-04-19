# Paper Review (Lite)

Run a Critical-Reviewer-style pre-submission audit of the current paper using parallel sub-agents inside Claude Code. Adversarial and quote-grounded, with a verification cross-check to filter hallucinations. Covers content and argument, numerical consistency, references and DOIs, writing quality, figures and formatting, replication archive completeness, and — for experimental papers — CONSORT flow and pre-registration verification. Returns a severity-ranked report with a journal-readiness checklist.

For heavier adversarial review (30+ Red Team / Blue Team / verification stages, resumable, cost-tracked, standalone CLI), use [`openpeerreview`](https://github.com/scdenney/open-peer-review) instead.

$ARGUMENTS
