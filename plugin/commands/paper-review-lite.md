# Paper Review (Lite)

Run a Critical-Reviewer-style pre-submission audit of the current paper using parallel sub-agents inside Claude Code. Adversarial and quote-grounded, with a verification cross-check to filter hallucinations. Covers content and argument, numerical consistency, references and DOIs, writing quality, figures and formatting, replication archive completeness, and — for experimental papers — CONSORT flow and pre-registration verification. Returns a severity-ranked report with a journal-readiness checklist.

Pass `--codex` to run the same specification across two model families: Claude and Codex (GPT-5.6 "Sol" at xhigh effort) review independently, then each cross-checks the other, and every surviving Critical or Recommended issue is annotated by confidence. Roughly 2× the calls.

For heavier adversarial review (30+ Red Team / Blue Team / verification stages, resumable, cost-tracked, standalone CLI), use [`presubmit`](https://github.com/scdenney/presubmit) instead.

$ARGUMENTS
