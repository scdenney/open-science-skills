---
name: model-council-voting
description: Runs several language models as independent coders on the same labeling or discovery task and reads their disagreement as data — panel assembly for model diversity, keeping votes independent, consensus rules, agreement statistics (Cohen's and Fleiss kappa, Krippendorff's alpha), the correlated-errors caveat that stops agreement being mistaken for validity, human validation beyond the panel, and reporting. Use when the user asks about a council, panel, ensemble, or jury of models, asks how to combine several models' labels, or asks what kappa or alpha to report for model coders. Single-model codebook and validation work goes to text-classification, per-item confidence to llm-calibration-logprobs.
argument-hint: "[describe your coding/discovery task, candidate models, and what agreement you want to measure]"
---

# Model Council Voting: Panels of Language Models as Independent Coders

## Instructions

A "council" runs the same labeling, scoring, or term-discovery task through several language models independently and reads their (dis)agreement as data. It sits **on top of** the single-model codebook-and-validation workflow in `text-classification` — build and validate the codebook there first, then escalate to a council only when one model is not enough. Companion skills: `topic-modeling` (an independent, non-LLM method for cross-checking what a council finds), `llm-calibration-logprobs` (per-item confidence from one model's token probabilities, a different signal than cross-model agreement), and `methods-reporting` (the standards the write-up must meet).

Two running examples supply the concrete figures below, both from the author's own work: a **four-model Korean term-discovery study** (an ensemble spanning four training origins, with a documented appendix reporting its voting and sensitivity tables) and a **two-model classification study** (a documented agreement analysis over a survey codebook). They are cited as worked illustrations, not as general findings.

### 1. When a Council Beats a Single Model

- Use a council when the labeling decision is **contested or ambiguous** — fuzzy category boundaries, stance or frame coding, constructs where reasonable coders disagree. The disagreement rate is itself a measurable property of the task, not noise to be averaged away.
- Use a council for **corpus-driven discovery** where the output set is not fixed in advance — e.g., which identity terms a corpus foregrounds. The term-discovery study runs a zero-shot extraction prompt over sampled text windows, one pass per model; requiring several model *families* to independently surface the same term (§4) is what separates a real corpus signal from one model's idiosyncrasy.
- Use a council for **robustness reporting** when results must survive a skeptical reader. Showing a finding holds across models from different training traditions answers the "would this replicate with a different model?" objection directly.
- A council is **overkill** when the task is unambiguous and a single validated model already agrees with humans at the level your downstream analysis needs (validate first via `text-classification`). For high-volume, well-defined coding, N model passes plus the agreement bookkeeping rarely buy anything.
- Decide up front which role the council plays — reliability evidence, robustness check, or discovery filter. It is not a substitute for the out-of-council validation in §7.

### 2. Assembling a Diverse Panel

- **Diversify training families and origins to decorrelate errors.** The threat a council guards against is a shared blind spot: models trained on overlapping data or by the same lab tend to make the *same* mistakes, so they vote together for the wrong reason. The term-discovery ensemble deliberately spans four origins — EXAONE-Deep (LG AI Research, Korea), Aya Expanse (Cohere, Canada), Qwen2.5 (Alibaba, China), and Gemma 3 (Google, US) — precisely because none shares training data or architecture with the others in any direct way, which makes cross-family agreement a conservative test. Four checkpoints from one family is a near-useless council.
- **Aim for 3–6 jurors.** Below 3 there is no many-rater agreement statistic (§5) and no meaningful k-of-N rule (§4); above ~6 the marginal decorrelation falls off and the bookkeeping grows. Two models is not a council but a pairwise reliability check reported with Cohen's κ, which is how the two-model classification study treats its pair. These bounds are house defaults, not a cited optimum; the binding constraint is *family diversity*, not raw count (§6).
- **Prefer open-weight models, pinned to an exact revision and re-runnable locally.** Proprietary APIs change underneath you and show high, unpredictable run-to-run variance even at temperature 0 (Barrie, Palmer & Spirling 2025). If a proprietary model is in the council, record its exact dated identifier and treat its votes as the least reproducible (`vlm-ocr` makes the same point for OCR).
- **Pin decoding.** Temperature 0 (greedy) is the default so a juror's vote does not wobble between runs. Where you want sampling diversity within a window, the term-discovery pipeline runs at temperature 0.3 with a fixed window-sampling seed and moves the reproducibility guarantee one level up: because decoding at non-zero temperature is not bit-for-bit deterministic, reproducibility is enforced at the level of the term set rather than the raw generations.
- **Consider an optional reference coder.** One stronger or domain-specialized model (or the human-coded gold sample of §7) can serve as the yardstick for per-juror precision and recall — in that study's per-model precision table the Korean-primary model reaches 56% precision and 100% recall against the nine-term reference, while the English-primary model misses two terms. Keep the reference out of the vote count itself, or you reintroduce a single point of failure.
- **Record the exact model tag for every juror** — version, quantization, revision, in the form `exaone-deep:32b-q4_K_M` / `aya-expanse:32b` / `qwen2.5:32b` / `gemma3:27b`, one row per juror. Family-name-only reporting ("we used Qwen and Gemma") is not reproducible.

### 3. Keeping Votes Independent

- **Run each juror in isolation** — no model sees another model's output, and there is no multi-round "discussion." Debate or chained prompting collapses the disagreement you are trying to measure and manufactures a consensus that reflects persuasion order, not the corpus.
- **Do not pool jurors into one prompt.** Asking a single model to "play the role of four experts" yields one model's guess at what four models would say, fully correlated by construction. Independence requires N separate inference runs.
- **Hold every shared input constant across jurors.** Same prompt, same sampled windows, same seed, same post-processing. The term-discovery pipeline gives all four models the same Korean zero-shot prompt, the same adaptive window sampling, and the same wf ≥ 50 absolute floor; only the model varies, so any disagreement is attributable to the model and not to a moving input.
- **For a deliberation design, use `model-committee` instead**, where GPT-5.6 Sol and Claude Opus 5 inspect each other's arguments, revise, and cross-rank toward one decision. Debate can improve a single *answer*, but a debating pair is not a panel of independent raters — do not report debate-derived consensus as if it were independent-coder agreement.

### 4. Consensus Rules

- **State a k-of-N rule before looking at outputs.** The term-discovery study keeps a term only if at least three of the four models selected it (3-of-4). Common defaults — 3-of-4, 4-of-6, simple majority — are house conventions, not cited thresholds; higher k buys precision at the cost of recall.
- **Prefer absolute floors over distribution-relative thresholds.** A per-juror threshold expressed as mean + 2 SD is distorted whenever a few high-frequency items inflate the distribution. The term-discovery study hit exactly this and switched to an absolute weighted-frequency floor (`wf ≥ 50`): the mean+2SD rule is sensitive to high-frequency demonym terms that inflate the distribution in some model runs, whereas an absolute floor yields more comparable cut-offs across models that differ in extraction volume.
- **Add category filters that encode theory, not vote count.** A term can win 4-of-4 and still be excluded on principled grounds: the term-discovery study excludes proper nouns (kingdoms, dynasties, the country itself) regardless of vote count, because they function as referential labels rather than contested conceptual constructs — five terms reach 4/4 consensus and are filtered out this way. Fix which categories are eligible *before* counting votes, so the filter is a stated rule rather than a post-hoc rescue.
- **Run a sensitivity analysis on both dials — the per-juror floor and k.** That study's weighted-frequency sensitivity table shows the published `wf ≥ 50` is the highest value at which all nine final terms remain while also being the lowest value at which the only additional entrant is a general-register term, and that moving from 3-of-4 to unanimous 4-of-4 drops three substantive terms. Report the band over which the conclusion holds; a set that swings with a small threshold change is not a stable instrument.
- **Treat principled abstention as informative, not as a tie.** If jurors may return "none / insufficient evidence," count and report the abstention rate per juror rather than silently recoding it as a vote (`text-classification` makes the same point about NAs as informative missingness).

### 5. Reading Agreement as Reliability, Not Validity

- **Agreement measures reliability — reproducibility of the coding — not validity.** A council that agrees perfectly with itself can be perfectly, consistently wrong, and a panel typically agrees with *itself* more than it agrees with humans. High inter-model agreement is never evidence that the labels are correct; that is what §7 is for.
- **Report chance-corrected agreement, not raw percent agreement**, which is inflated by the base rate — two coders assigning everything to the majority class agree often by luck. Match the coefficient to the design:

| Design | Coefficient | Notes |
|---|---|---|
| Exactly 2 jurors, nominal labels | Cohen's κ (Cohen 1960) | the two-model classification study reports 80.9% overall agreement, κ = 0.730, between Llama 3.1 8B and Qwen 2.5 3B |
| 3 or more jurors, nominal labels | Fleiss' κ (Fleiss 1971) | the natural statistic for a council of 3+ |
| Ordinal labels, more than 2 coders, or missing votes/abstentions | Krippendorff's α (Krippendorff 2004/2019) | generalizes across measurement levels and rater counts; prefer it when jurors abstain or labels are ranked |

- **Interpret κ/α with the Landis & Koch (1977) bands** as rough guides, not bright lines: < 0.00 poor, 0.00–0.20 slight, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect (the user's κ = 0.730 is "substantial"). The bands are a convention from one paper — report the raw α/κ value alongside the label.
- **Diagnose low agreement before trusting the consensus.** Inspect *which* categories or items drive it: in the two-model classification study the lowest per-code agreement was `civic_commitment` at 66.5%, and collapsing two overlapping codes raised overall agreement from 73.0% to 80.9% and κ from 0.634 to 0.730. Low council agreement usually signals a codebook problem (fix it in the `text-classification` workflow), not a model problem.

### 6. The Correlated-Errors Caveat

- **N jurors carry fewer than N independent votes when their errors are correlated.** A majority vote beats the best single classifier only when members err *independently*; when members are dependent the ensemble can be no better — or worse — than its best member (Kuncheva & Whitaker 2003). Four checkpoints of one model, or four models distilled from a common teacher, tend to be wrong together, so their unanimous vote is closer to one vote than to four. Family diversity (§2) is the lever that raises the *effective* number of votes toward the nominal N.
- **Watch for shared-error signatures.** If two jurors miss or hallucinate the *same* items, treat them as partially redundant — down-weight their joint vote, or report the council with and without one of the pair. A per-model unique-selection analysis, examining which terms each model alone chose, is the diagnostic that surfaces shared vs. idiosyncratic behavior.
- **Report the families represented, not just an agreement number.** High agreement *with low family diversity* is weak evidence; high agreement *across diverse families* is strong. Report the diversity check rather than a single effective-N figure: the general dependence result is well established, but treating it as a precise "effective sample size" calculation for LLM juries goes beyond what can be cleanly cited.

### 7. Validating Beyond the Panel

- **The council must never grade its own work** — validate against at least one source *outside* the council.
- **Human-coded gold sample.** Hand-code a stratified sample (the `text-classification` skill specifies 50–100 items, two independent human coders, Cohen's κ or Krippendorff's α for inter-coder reliability) and report each juror's and the consensus's precision/recall/F1 against it. This is the only step that speaks to validity.
- **An independent, non-LLM method.** Cross-check council output against a method that imposes no LLM prior. The term-discovery study runs BERTopic and LDA over the same corpus and asks whether they independently recover the council's nine terms: BERTopic recovers 9/9, LDA 5/9, with the LDA misses explained by known properties of document-level bag-of-words modeling. The two-model classification study makes the parallel move against an STM ("two independent analytical approaches … converge on the same substantive story"); see `topic-modeling` for that side of the triangulation.
- Where the council, the human sample, and the independent method diverge, report the divergence — it is usually substantively informative (e.g., LDA misses corpus-wide terms precisely because they are corpus-wide).

### 8. Reporting and Reproducibility

- **Report every juror's exact tag, quantization, revision, decoding parameters, and seed** — all of them, in one table.
- **Publish the per-item / per-term vote table.** The unit-level record of which juror voted which way is the core evidence; the term-discovery study's cross-model voting table gives one row per term with a check/dash per model, the vote tally, and the final status. A reader must be able to see the votes, not just the aggregate.
- **Report the consensus rule, the absolute floors, the category filters, and the sensitivity bands** (§4), and the agreement statistic with its coefficient, value, Landis–Koch label, and per-category breakdown where relevant (§5).
- **State the council's role explicitly** — reliability evidence, robustness check, or discovery filter — and report the out-of-council validation (§7). Distinguish discovery from confirmation: if the codebook or term set was revised after seeing council output, report the revision trajectory, since undocumented post-hoc revision is a researcher degree of freedom that can inflate findings (Simmons, Nelson & Simonsohn 2011; Nosek et al. 2018).
- **Archive prompts, sampling seeds, the merge/voting code, and the raw per-juror generations** so the council can be re-run. For the broader methods-section checklist (APSA/JARS/DA-RT), compose with the `methods-reporting` skill.

## Quality Checks

- [ ] Council justified over a single validated model — contested/ambiguous, discovery-driven, or robustness (escalated from `text-classification`) — and its role stated: reliability evidence, robustness check, or discovery filter
- [ ] Panel spans **diverse training families/origins** rather than multiple checkpoints of one family (EXAONE/Aya/Qwen/Gemma-style spread), with 3–6 jurors
- [ ] Open-weight jurors preferred and pinned to exact revisions; exact model tags recorded (version, quantization, revision); any proprietary juror's dated identifier noted and its votes flagged as least reproducible
- [ ] Decoding pinned — temperature 0, or a fixed seed with reproducibility enforced at the level of the final set
- [ ] Votes cast **independently** — no cross-talk, no deliberation, no single-prompt role-play; one inference run per juror on identical inputs
- [ ] k-of-N rule stated **before** inspecting outputs; absolute floors used in place of mean+2SD thresholds where jurors differ in output volume; theory-driven category filters applied independent of vote count
- [ ] Sensitivity analysis reported on both the per-juror floor and k, with the stability band stated
- [ ] Abstentions counted and reported per juror, not recoded as votes
- [ ] Chance-corrected agreement reported with the coefficient matched to the design (Cohen for 2; Fleiss for ≥3 nominal; Krippendorff α for ordinal/>2/abstentions) and the Landis–Koch band; read as **reliability, not validity**
- [ ] Disagreement diagnosed per category before the consensus is trusted
- [ ] Correlated-error caveat addressed: family diversity documented, shared-error signatures inspected, effective vs. nominal votes acknowledged (Kuncheva & Whitaker 2003)
- [ ] Validated **beyond the panel** — human-coded gold sample (precision/recall/F1) and/or an independent non-LLM method (`topic-modeling`)
- [ ] Per-item/per-term vote table published; model tags, seeds, prompts, voting code, and raw generations archived; discovery vs. confirmation framing and any revision trajectory stated (Simmons et al. 2011; Nosek et al. 2018; compose with `methods-reporting`)
