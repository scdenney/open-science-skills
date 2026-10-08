---
name: text-classification
description: "Advises on setting up and validating LLM text classification: codebook, learning regime and model choice, prompts, validation against human coding (kappa, F1), hybrid review, measurement error, and reporting, plus a short resumable batch pattern with a rule-based baseline. Use to classify, code, or label text at scale; category discovery goes to topic-modeling."
---

# LLM-Based Text Classification for Social Science Research

## Instructions

Treat the classifier as a measurement instrument the user is designing, not a script to write. Work through the decisions below with the user in this order, explain the trade-off and the governing standard at each, and record the choice and its rationale. Code comes after the codebook, regime, model, and validation plan are settled. If the categories are not yet known and finding them is the goal, this is discovery — route to `$topic-modeling`.

### 1. Codebook Design

- Start from the population, sampling frame, and (for experimental data) the treatment condition each response comes from. These constrain which categories can plausibly exist and which subgroups any bias assessment must cover. LLM classification extends the open-ended coding tradition in survey methodology rather than replacing it (Geer 1988; Lupia 2018).
- The codebook is the most consequential decision in the pipeline. LLMs given loose instructions fall back on general-purpose definitions instead of the researcher's operationalization (Halterman & Keith 2025).
- Give each code five components (adapted from Halterman & Keith 2025):
  - **Label**: the exact output string
  - **Definition**: a one-sentence operationalization of the construct
  - **Clarification**: boundary cases that belong in the category
  - **Negative clarification**: common confusions and adjacent categories that do not
  - **Examples**: 2-3 positive and 2-3 negative (common misclassifications)
- Start with a small code set (3-6). Larger schemes increase ambiguity and lower agreement for humans and LLMs alike (Chae & Davidson 2025).
- Decide single- versus multi-label explicitly and say so in the prompt; models default to single-label.
- Include a residual category (`none_of_above`, `uncodeable`) for vague, short, or off-topic responses, defined as precisely as the substantive codes (Halterman & Keith 2025).
- Iterate the codebook through pilot disagreements. Most codebook problems are definition problems, not model problems (Halterman & Keith 2025).
- A fully worked three-category codebook with all five components, plus a matching system prompt, is in `references/example-codebook-and-prompt.md`.

### 2. Choosing a Learning Regime

Chae & Davidson (2025) map document characteristics and available resources to a regime. The model names below are the ones they tested; carry the comparative finding forward, not the specific models.

- **Zero-shot prompting**: short documents, a large decoder model, no labeled data. Good for prototyping and well-defined constructs; the strongest proprietary model performed best zero-shot in their tests.
- **Few-shot prompting**: results are inconsistent — examples help some models and hurt others. Compare few-shot against zero-shot on a held-out sample before committing, and choose diverse examples that cover edge cases.
- **Fine-tuning**: effective with as few as ~100 hand-coded examples; fine-tuned smaller models matched GPT-4o zero-shot. Prefer it when labeled data exists and cost at scale matters.
- **Instruction-tuning**: detailed prompting combined with fine-tuning on instruction-output pairs. The most accurate regime for complex tasks (instruction-tuned Llama3-70B beat GPT-4o zero-shot on stance detection), at the cost of more infrastructure.
- **Encoder-only fine-tuning** (BERT, DeBERTa, SBERT; ~86-110M parameters, laptop hardware): often matches or beats zero-shot generative LLMs at a fraction of the cost, with deterministic output (Chae & Davidson 2025, Table 1; Ziems et al. 2024 find fine-tuned RoBERTa rarely underperforms larger generative models across 20 tasks). Prefer it when the label set is fixed, labeled data exists, and reproducibility outweighs generative flexibility.

When resources permit, test several regimes on the same pilot sample and choose on measured performance.

### 3. Model Selection and Reproducibility

- Prefer open-weight models run locally for publishable research. They show lower, more predictable run-to-run variance; proprietary models show high and unpredictable variance even at temperature 0 (Barrie, Palmer & Spirling 2025).
- Choose the least expensive model that meets the human-validated quality target. For new OpenAI pipelines, prefer the Responses API and check the chosen model's current structured-output, reasoning, and logprob support. Astra suits difficult adjudication; move an established high-volume classifier or a frozen study to it only after a representative validation pass.
- Record the exact model identifier (e.g., `gpt-4o-2024-08-06`), not the family name. Commercial models are changed or withdrawn without notice — GPT-3 was removed from OpenAI's API entirely (Barrie, Palmer & Spirling 2025; Chae & Davidson 2025).
- Use temperature 0. It reduces but does not eliminate variation in proprietary models (Barrie, Palmer & Spirling 2025).
- Variance test: classify the same ~50 responses twice with meaningful separation (two weeks apart, or across a model-version change) and report the agreement rate. N = 50 and a ≥ 95% "stable" threshold are house defaults; Barrie, Palmer & Spirling (2025) motivate the test but do not fix the numbers.
- For multiple languages or cultural contexts, validate per language against native-language hand coding. Accuracy is high outside English but not uniform: GPT-4 matched English accuracy (~90%) on Italian, German, and Chilean political tweets (Heseltine & Clemm von Hohenberg 2024) and beat supervised comparators across 11 countries, though absolute accuracy fell outside the United States (Tornberg 2025). English validation does not carry over.
- Commercial models may refuse politically sensitive content (Chae & Davidson 2025 saw GPT-4o refuse some comments about candidates). For sensitive topics, measure the refusal rate before full deployment.
- Responses sent to commercial APIs may be retained or used for training (Chae & Davidson 2025). Data containing personal identifiers goes to a locally hosted model unless the provider's retention policy has been checked; sending it off-machine is the user's decision.

### 4. Prompt Construction

- Put the full codebook (all five components per code) in the system prompt.
- Specify the exact output: labels only, comma-separated if multi-label, nothing else. Smaller models add conversational preamble unless constrained (Chae & Davidson 2025).
- For structured or complex inputs, use JSON for input and output; it parses more reliably (Chae & Davidson 2025).
- Put the response text in the user message behind a consistent delimiter (e.g., `"Code this response:\n\n{text}"`).
- Include only information the classifier is meant to use. If country should not influence coding, leave it out of the input — models use any available signal.

### 5. Pilot Testing and Validation Against Human Coding

This is the evidence that the classifier measures the construct. It is not optional.

- Before hand-labeling, run Halterman & Keith's (2025) Stage 1 label-free behavioral tests: (I) **legal labels** — does the model return only codebook labels? (II) **definition recovery** — given a verbatim definition, does it return the right label? (III) **in-context examples** — does it label the codebook's own examples correctly? (IV) **order invariance** — are predictions stable when category order is shuffled? Failing I-III means the model cannot follow the codebook; failing IV means ordering artifacts. Use these to screen models out before investing in hand coding.
- Hand-code 50-100 responses as ground truth before any LLM classification. The sample validates the codebook and benchmarks the model.
- Use two independent human coders. Report Cohen's κ (Krippendorff's α for ordinal labels or more than two coders, as Tornberg 2025 and Benoit et al. 2025 report). κ ≥ 0.7 is a house default aligned with Landis & Koch's (1977) "substantial agreement" band; Halterman & Keith (2025) call for revision when human agreement is low without fixing a cutoff. Below that band, revise the codebook before testing models — the scheme is the problem.
- Consider a **self-coding** diagnostic: ask respondents to assign their own answer to the categories. Agreement with researcher codes tests the codebook's semantic validity, and disagreement correlated with demographics reveals bias in the scheme (Glazier, Boydstun & Feezell 2021). Especially useful in cross-national or cross-demographic work.
- Compare LLM output to the human ground truth with per-category precision, recall, and F1. Halterman & Keith (2025) treat F1 ≥ 0.7 as adequate and recommend iteration when it is low; "below 0.5, consider fine-tuning" is a house operationalization.
- For error analysis, ask the model to justify its label on misclassified and boundary cases. The justification shows whether it is applying the codebook definition or a background concept (Tornberg 2025). This is a diagnostic; the justification is not the classification.
- Read the confusion matrix. If two categories are consistently confused, merge them or sharpen the negative clarification.
- If F1 is inadequate, iterate in this order: (1) revise definitions, (2) add few-shot examples, (3) fine-tune. Test whether the codebook is the problem before fine-tuning (Halterman & Keith 2025).

### 6. Hybrid Human-LLM Review

- Have the LLM classify everything and humans adjudicate uncertain cases. This reached 93%+ accuracy at a fraction of full manual cost (Heseltine & Clemm von Hohenberg 2024).
- Flag for review on one or more of: (a) token-level confidence from the model's log-probabilities — `$llm-calibration-logprobs` covers per-decision confidence, calibration (ECE, Brier), and triage thresholds, and is better calibrated than a verbalized HIGH/MEDIUM/LOW rating; (b) disagreement across repeated runs or models (Heseltine & Clemm von Hohenberg 2024); (c) residual-category assignments; (d) boundary cases coded with two competing labels. (a), (c), and (d) are defaults consistent with the hybrid-workflow literature, not individually cited.
- Plan for roughly 10-15% of responses needing review; above ~25% points to codebook or model problems and a return to piloting. These bands are house planning defaults.
- Feed patterns in flagged cases back into the codebook.
- **Multi-model ensembles.** Benoit, De Marchi & Laver (2025) run a matrix rather than a pair — three summarizer models × three scorer models × zero/few-shot — and take the ensemble mean of per-item scores, which correlates with expert-survey party positions near the inter-expert ceiling (~0.90 Pearson). Instruct models to return NA when the input lacks information rather than forcing a label, and report per-model NA rates: systematic NA differences between models are findings about the text, not noise (Benoit et al. 2025). When several models act as independent coders, treat them like human coders — report chance-corrected agreement (κ or α) across them, and remember that models trained on similar data make correlated errors, so model-model agreement is not a substitute for agreement with human coding. If labels come from a consensus rule (k of N models agreeing, with a per-model confidence floor), state the rule before looking at outputs and report a sensitivity analysis over both k and the floor.

### 7. Downstream Use and Interpretation

- Report code prevalence overall and by relevant subgroups (country, treatment arm) as proportions with confidence intervals.
- Cross-tabulate codes. For construct validation, joint prevalence of related codes (recognizing a cue and interpreting it positively) says more than marginals.
- When LLM labels become variables in regression or causal analysis, plan for measurement error up front. Even highly accurate labels can produce severe bias and poor coverage when used as proxies; the remedy is a design-based correction, not ignoring the noise (Egami et al. 2023; Knox, Lucas & Cho 2022, via Halterman & Keith 2025; Chae & Davidson 2025). Distinguish classifier-as-outcome from classifier-as-treatment-check. In a pre-registered design, register which codes map to which hypotheses (`$pre-registration-writing`).
- LLMs can beat human coders on tasks needing context — implicit references, sarcasm, background knowledge (Tornberg 2025) — but they remain one measurement instrument, not ground truth.

### 8. Reporting

- The full pipeline: exact model version, temperature and other generation parameters, complete prompt, codebook, and run dates.
- Validation: human inter-coder reliability; per-category precision, recall, and F1 against human ground truth; overall accuracy and κ; the variance-test agreement rate; the human review rate.
- Archive prompt, codebook, and classification code. For proprietary models, state the deprecation risk and whether results can be reproduced (Barrie, Palmer & Spirling 2025).
- State whether the LLM was used for discovery or confirmation. If the codebook was revised after seeing LLM output, report the revision history: undocumented post-hoc refinement is a researcher degree of freedom that can inflate findings (Simmons, Nelson & Simonsohn 2011), and transparent revision plus pre-specified confirmatory categories is the remedy (Nosek et al. 2018).
- Present representative examples for each code so readers can judge whether the labels match their understanding (Glazier, Boydstun & Feezell 2021).
- For CONSORT/JARS flow reporting and DA-RT archiving, see `$methods-reporting`.

### 9. Running at Scale: Batch Pattern With a Rule-Based Baseline

Once the design above is validated, a large set of repeated free-text values against a closed codebook (occupation or institution strings from registries, open-text survey answers, affiliation taxonomies) runs best as a resumable batch job. Adapt this pattern to the project:

- Freeze the input: deduplicate strings, keep a frequency count and stable ID per unique string, and record codebook, model, prompt version, seed, and date.
- Classify unique strings in batches with JSON output and a closed code set; write output incrementally so an interrupted run resumes; keep a short rationale and a logprob confidence where available.
- Map out-of-vocabulary outputs to explicit residual buckets and log every normalization.
- Hand-validate a stratified sample that over-represents rare classes and known failure modes; score overall and per-class accuracy and calibration by confidence bin (Section 5 statistics).
- If a regex or dictionary classifier already exists, run it on the same strings and compare agreement, collisions, and known false positives to decide which rules to keep as fallback.
- Publish the lookup table — one row per unique string with final code, validation signals, run metadata, and a stable join key to the analytic frame.

This pattern does not fit one-off qualitative coding without a stable codebook, tasks where a human reads every item anyway, or cases where a supervised model with an evaluation harness already exists.

## Quality Checks

- [ ] Codebook has all five components per code, including a defined residual category (Halterman & Keith 2025)
- [ ] Learning regime chosen from data characteristics and resources, ideally compared on a pilot (Chae & Davidson 2025)
- [ ] Exact model version recorded, not the family name
- [ ] Stage 1 label-free tests run before hand coding (Halterman & Keith 2025)
- [ ] 50-100 pilot responses hand-coded by two independent coders; κ (or α) reported and codebook revised if below the Landis & Koch "substantial" band
- [ ] Per-category precision, recall, and F1 against human ground truth reported
- [ ] Variance test run and agreement rate reported
- [ ] Per-language validation against native-language ground truth for multilingual data (Heseltine & Clemm von Hohenberg 2024; Tornberg 2025)
- [ ] Uncertain cases flagged and human-reviewed; review rate reported
- [ ] Prompt, codebook, and code archived; proprietary-model reproducibility risk stated (Barrie, Palmer & Spirling 2025)
- [ ] PII kept off commercial APIs unless the retention policy was reviewed (Chae & Davidson 2025)
- [ ] Measurement-error correction planned up front if labels feed downstream estimation (Egami et al. 2023; Knox, Lucas & Cho 2022)
- [ ] Discovery vs. confirmation stated; codebook revision history documented
- [ ] Batch runs: input set frozen, versions recorded, run resumable, out-of-vocabulary outputs mapped, stratified sample scored, baseline compared, lookup table joinable
