# Paper Review (Lite, Cross-Model Adversarial)

Run a cross-model adversarial pre-submission audit. Claude and Codex (GPT-5.4) independently apply the `paper-review-lite` specification (9 review dimensions, Critical-Reviewer posture, quote-grounded findings), then each model cross-checks the other's findings. The final report annotates every retained Critical or Recommended issue with confidence (Mutual, Asymmetric-confirmed, or Asymmetric-after-adjudication) and drops hallucinations on either side.

Heavier than `/oss:paper-review-lite`. Roughly 22 model calls (9 Claude Red Team, 9 Codex Red Team, 4 cross-model Blue Team). Reach for it before submission when you want maximum adversarial pressure and a second model family's blind spots. For an even heavier standalone deliverable with Red Team personas, math audits, and code-replication checks, use [`presubmit`](https://github.com/scdenney/presubmit) instead.

$ARGUMENTS
