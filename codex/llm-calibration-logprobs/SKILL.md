---
name: llm-calibration-logprobs
description: "Reads a model's own uncertainty from token log-probabilities: collecting and aggregating label logprobs, confidence tiers and margins for triage, calibration against human labels (ECE, Brier, reliability diagrams), downstream use, and reproducibility. Use for per-item classifier confidence or routing low-confidence cases to human review; codebook and validation design go to text-classification."
---

# Reading a Model's Own Uncertainty from Token Log-Probabilities

## Instructions

This skill covers **within-model** confidence: how sure one model is about each decision, read from the token log-probabilities it emits, and whether that confidence is *calibrated* against ground truth. Agreement across several independent models is a different kind of evidence — when a pipeline uses both, report both. Codebook design and human-validation statistics (κ, F1) belong to `$text-classification`; cross-reference rather than re-derive them.

### 1. What a Logprob Can and Cannot Tell You

- Use logprobs when you need a per-item, continuous confidence signal. It comes free with the forward pass that produced the label and answers "how sure was the model about *this* classification?", which a hard 0/1 label cannot.
- A logprob is the model's subjective probability under its own distribution, **not a probability of correctness**. A model can assign 0.95 to labels that are right 70% of the time. Treat it as a claim about confidence that calibration (§4) tests.
- Applied social science usually takes the final label at face value and discards the distribution it came from; computational linguists treat token probabilities as the native uncertainty signal. Neither is enough alone — the logprob is informative but must be calibrated against external truth before it carries weight. State the choice in the methods section.
- Prefer the emitted-token logprob over a prompted "rate your confidence HIGH/MEDIUM/LOW" string. Verbalized confidence is generated text subject to the same biases (Kadavath et al. 2022; Tian et al. 2023); it can be made roughly calibrated with effort (Tian et al. 2023), but treat it as a separate, weaker signal and cross-check it rather than substitute it. A long reasoning trace is not a confidence measure either.

### 2. Collecting Logprobs and Aggregating Multi-Token Labels

- **Check compatibility before choosing the model.** Logprob support depends on model, endpoint, and reasoning setting; confirm with current documentation and a small test response before a batch. Astra does not support reasoning effort `none`, so a logprob example from a non-reasoning model may not transfer to it. Keep a validated compatible model for calibration, and mark missing logprobs as unavailable rather than filling them with verbal confidence.
- **Enable logprob return.** OpenAI chat completions take `logprobs=True` and `top_logprobs=K` (K ≤ 20 at time of writing) and return per-token `.token`, `.logprob`, and `.top_logprobs`. vLLM's OpenAI-compatible server exposes the same fields (`logprobs=K`); Ollama returns per-token logprobs too. A typical script sets `api_kwargs["logprobs"] = True` and `api_kwargs["top_logprobs"] = 5`, then stores `resp.choices[0].logprobs.content` alongside the parsed label.
- **Fix decoding.** Set `temperature=0` and a fixed `seed`, and record both. Temperature 0 makes the label deterministic on most backends but does not make hosted-API logprob values bit-identical (§6).
- **Constrain the output so label tokens are findable.** A rigid schema (JSON with a `"code"` field) lets you locate the label; free prose makes the span ambiguous.
- **Aggregate label tokens by character span.** A label like `civic_commitment` spans several sub-word tokens. Reconstruct the output string, locate the label (e.g., the value after `"code":`), map each token to its character offsets, and select exactly the tokens overlapping the label span — never guessed token indices. Then choose an aggregation and state it; the three are not interchangeable:
  - **Sum** = `log P(whole label)`, the joint probability. Principled, but length-confounded: longer labels score lower. Comparable only across labels of similar token length. (`logprob_code_sum`)
  - **Mean per-token logprob** (geometric-mean probability) removes most of the length confound; the better default when label lengths differ.
  - **First-token logprob**: cheap and length-invariant, informative only when the labels diverge at the first token. Check that before relying on it; shared prefixes make it useless. (`logprob_first_token`)
- **Store the top alternatives** at the first label position (`top_alternatives_json`). The margin to the runner-up is a separate, often more discriminating signal (§3).

### 3. Confidence Tiers, Margins, and Triage

- Map the chosen-label probability `p = exp(logprob)` onto action tiers. A starting scheme:
  - `p ≥ 0.90` → auto-accept
  - `0.65 ≤ p < 0.90` → accept, flag for spot-check
  - `p < 0.65` → human review
- These cut points are house planning defaults, not values from a cited study, and mean nothing until calibration is checked (§4). If the model is overconfident, a 0.90 cut admits too many errors. Re-derive the cuts from your own reliability diagram at the bin where empirical accuracy crosses the tolerated error rate.
- Use the margin as a second trigger. A small gap to the runner-up (e.g., `p_top − p_second < 0.10`) marks a coin-toss between two specific labels even when `p` is high. Flagging on either signal catches more errors than absolute confidence alone, and the runner-up label shows which codebook boundary is ambiguous.
- Route low-confidence items to humans; the tiers allocate scarce review time to genuine coin-tosses rather than a random sample. This is the within-model counterpart of disagreement-based flagging in `$text-classification`.
- Plan for roughly 10-20% of items in the low tier (house default). A much larger share usually means overlapping labels or an under-specified prompt — return to the codebook before spending review hours.

### 4. Calibration Assessment

A model is calibrated if, among items labeled with confidence `p`, a fraction `p` are correct. Tiers are trustworthy only after this is measured against held-out ground truth.

- **Ground truth must be human-adjudicated labels** (or another external standard), not the model's modal answer or other model runs. Checking logprobs against model output measures self-consistency, not correctness; within-model confidence and cross-model agreement can both look reassuring while the labels are jointly wrong, because model errors are correlated.
- **Reliability diagram.** Bin by predicted confidence (e.g., 10 equal-width bins) and plot mean confidence against empirical accuracy. Below the diagonal is overconfidence, above is underconfidence. Modern deep networks, including large transformers, tend toward overconfidence (Guo et al. 2017).
- **Expected Calibration Error.** `ECE = Σ_b (n_b / N) · |acc(b) − conf(b)|` (Guo et al. 2017). Report it with the bin count, since it is binning-sensitive, and always with the diagram — different curves can share an ECE.
- **Brier score.** `BS = (1/N) Σ (p_i − y_i)²` (Brier 1950). A proper scoring rule that captures calibration and resolution together, so it penalizes hedging everything at 0.5. Report it alongside ECE.
- **Calibration is not accuracy.** Triage depends on calibration: if the 0.90 bin is 70% accurate, the auto-accept tier leaks errors regardless of overall F1.
- **Temperature scaling** fixes calibration without changing the argmax label: fit one scalar `T` on a calibration split and rescale before softmax; it often largely corrects ECE (Guo et al. 2017). Report ECE and Brier before and after, and never fit `T` on the evaluation data.

### 5. Using Uncertainty in the Pipeline

- **Route, don't discard.** Dropping unsure items biases the remaining sample toward what the model finds easy, which is rarely random with respect to the construct.
- **Propagate uncertainty.** When labels feed a regression or prevalence estimate, carry per-item confidence (observation weights, soft labels, or multiple-imputation draws over the label) instead of hard 0/1 labels. At minimum, rerun the downstream analysis without the low-confidence tier and report whether conclusions move. This connects to the measurement-error correction in `$text-classification`.
- **Report the share of the corpus in each tier.** It is a corpus-level quality signal and sizes the review budget.

### 6. Caveats

- **Hosted-API logprobs are unstable.** Providers may restrict or change logprob support without notice, and values drift across snapshots and even identical calls; batching, kernel non-determinism, and silent updates perturb them at temperature 0. Pin the exact model version, record the run date, and re-measure calibration after any model update. Open-weight models served locally (vLLM, Ollama — e.g., Llama 3.1 8B or Qwen 2.5 3B) give stable, inspectable logprobs.
- **Closed-set tasks only, mostly.** Logprob confidence is interpretable for a fixed label set. For open-ended generation, per-token logprobs measure local fluency, not global correctness.

### 7. Reproducibility and Reporting

- **Collection recipe:** exact model version or snapshot, decoding settings (`temperature`, `seed`, `top_logprobs` K), the output schema used to locate labels, and the aggregation function with its rationale. Archive the raw per-token logprobs and top-K alternatives, not only the derived scalar.
- **Calibration:** reliability diagram, ECE with bin count, and Brier score on a held-out human-labeled set; direction and size of miscalibration; whether temperature scaling was applied.
- **Triage:** thresholds and how they were derived from the diagram, per-tier shares, and the human-review rate.
- **Ground-truth source** for calibration, stated explicitly.
- For the broader methods checklist (model disclosure, archived prompts, DA-RT/JARS), use `$methods-reporting`; for codebook and human-validation metrics, `$text-classification`.

## Quality Checks

- [ ] Logprobs enabled (`logprobs=True`, `top_logprobs=K`); `temperature=0` and a fixed `seed` recorded
- [ ] Label tokens located by character span; aggregation (first-token / sum / mean) stated, with the sum's length confound acknowledged
- [ ] Top-K alternatives stored and margin to the runner-up computed
- [ ] Logprob confidence not reported as probability of correctness without calibration against external ground truth
- [ ] Reliability diagram against **human-adjudicated** labels; ECE (with bin count) and Brier reported (Guo et al. 2017; Brier 1950)
- [ ] Direction of miscalibration stated; temperature scaling, if used, fit on a separate split
- [ ] Triage thresholds derived from the reliability diagram, with house defaults re-justified on this corpus
- [ ] Low-confidence items routed to review, not discarded; per-tier shares and review rate reported
- [ ] Downstream analysis rerun without the low-confidence tier (or uncertainty propagated), with sensitivity reported
- [ ] Verbalized confidence and reasoning text not substituted for the token logprob
- [ ] Model snapshot pinned, run date recorded, calibration re-measured after model updates
- [ ] Collection recipe and raw per-token logprobs archived; token-probability vs. face-value convention stated in the methods section
