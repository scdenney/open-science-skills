---
name: text-classification
description: Guides LLM-based text classification for survey and experimental text data. Covers codebook design, learning regime selection, model choice, human-LLM hybrid workflows, and validation. Use when (1) designing an LLM classification scheme for open-ended survey responses, (2) writing a codebook for LLM text annotation, (3) choosing between zero-shot, few-shot, fine-tuning, or instruction-tuning, (4) selecting a model for classification, (5) validating LLM classifications against human-coded ground truth, (6) implementing hybrid human-LLM workflows, (7) addressing reproducibility concerns, or (8) reporting LLM classification methods and results.
argument-hint: "[describe your text data and classification task]"
---

# LLM-Based Text Classification for Social Science Research

## Instructions

### 1. Codebook Design

- Treat codebook design as the most consequential decision in the classification pipeline. LLMs struggle with loose instructions and revert to general-purpose definitions rather than following researcher-specific operationalizations (Halterman & Keith 2025).
- Structure each code with the following components (adapted from Halterman & Keith 2025):
  - **Label**: The exact output string the model should return
  - **Definition**: A single-sentence operationalization of the construct
  - **Clarification**: What IS included — boundary cases that belong in this category
  - **Negative clarification**: What is NOT included — common confusions and adjacent categories
  - **Examples**: 2-3 positive examples (correctly classified) and 2-3 negative examples (common misclassifications)
- Keep the number of codes small (3-6) for initial classification. Larger coding schemes increase ambiguity and reduce inter-annotator agreement for both humans and LLMs (Chae & Davidson 2025).
- Allow multi-label assignment when responses may reflect more than one construct. Specify this explicitly in the prompt — models default to single-label output unless instructed otherwise.
- Include a residual category (e.g., `none_of_above` or `uncodeable`) for responses that are too vague, too short, or off-topic. Define this category as precisely as the substantive codes (Halterman & Keith 2025).
- Iterate the codebook through pilot testing. Examine disagreements between LLM output and hand-coding to identify ambiguous definitions, then revise. Most codebook problems are definition problems, not model problems (Halterman & Keith 2025).

### 2. Choosing a Learning Regime

- Follow the decision framework from Chae & Davidson (2025), which maps document characteristics and available resources to the appropriate approach:

  **Zero-shot prompting**: Use when classifying short documents with a large decoder model (GPT-4o, Llama3-70B+) and no labeled training data. Best for rapid prototyping and tasks where constructs are well-defined. GPT-4o achieves the best zero-shot performance across tasks (Chae & Davidson 2025).

  **Few-shot prompting**: Add labeled examples to the prompt. Results are inconsistent — adding examples helps some models but degrades others (Chae & Davidson 2025). Always compare few-shot against zero-shot on a held-out sample before committing. Select diverse examples covering edge cases, not just prototypical instances.

  **Fine-tuning**: Train a model on labeled data. Effective with as few as 100 hand-coded examples for smaller models (Chae & Davidson 2025). Fine-tuned smaller models (Llama3-8B, GPT-3 Davinci) can match GPT-4o zero-shot performance. Prefer this when you have labeled data and need cost-effective classification at scale.

  **Instruction-tuning**: Combine detailed prompting with fine-tuning on paired instruction-output examples. Most powerful regime for complex tasks — instruction-tuned Llama3-70B surpasses GPT-4o zero-shot on stance detection (Chae & Davidson 2025). Requires more technical infrastructure but yields the highest accuracy.

- When resources permit, test multiple regimes on the same pilot sample and select based on empirical performance, not assumptions.

### 3. Model Selection and Reproducibility

- Prefer open-weight models (Llama 3, Gemma, Mistral) for publishable research. Open-weight models run locally produce substantially lower and more predictable variance across runs, while proprietary models (GPT-4, Gemini) show high and unpredictable variance even with temperature=0 (Barrie, Palmer & Spirling 2025).
- If using proprietary models, document the exact model identifier (e.g., `gpt-4o-2024-08-06`), not the model family name. Commercial models are modified or deprecated without notice — GPT-3 was withdrawn from OpenAI's API entirely (Barrie, Palmer & Spirling 2025; Chae & Davidson 2025).
- Set temperature to 0 for classification tasks. This reduces but does not eliminate stochastic variation in proprietary models (Barrie, Palmer & Spirling 2025).
- Run the same 50 responses through the classifier twice, separated by at least two weeks. Report the agreement rate between runs as a variance metric. If agreement is below 95%, flag the results as potentially unstable.
- Be aware that commercial models may refuse to classify politically sensitive content. Chae & Davidson (2025) found GPT-4o refused to process some Facebook comments about political candidates due to content moderation filters. For sensitive topics (immigration attitudes, extremism, hate speech), test for refusal rates before full deployment.
- Consider data privacy: survey responses sent to commercial APIs may be absorbed into training data (Chae & Davidson 2025). For data containing personally identifying information, use locally hosted open-weight models or confirm the API provider's data retention policy.

### 4. Prompt Construction

- Place the codebook in the system prompt. Include all components for each code (label, definition, clarification, negative clarification, examples).
- Specify the exact output format: code labels only, comma-separated if multi-label. Instruct the model to return no additional text. Smaller models in particular generate conversational preamble unless explicitly constrained (Chae & Davidson 2025).
- For structured or complex inputs, use JSON formatting for both input and expected output. LLMs trained on code corpora parse JSON reliably and produce more consistent structured output (Chae & Davidson 2025).
- Include the response text in the user message, separated clearly from instructions. Use a consistent delimiter (e.g., `"Code this response:\n\n{text}"`).
- Do not include information in the prompt that the classifier should not use. If country of origin should not influence coding, do not include it in the input — models will use any available signal.

### 5. Pilot Testing and Validation

- Hand-code 50-100 responses as ground truth before any LLM classification. This sample serves dual purposes: validating the codebook and benchmarking LLM performance.
- Use two independent human coders for the pilot sample. Calculate inter-coder reliability (Cohen's Kappa). If human κ < 0.7, the codebook needs revision before LLM testing — the problem is the coding scheme, not the model (Halterman & Keith 2025).
- Compare LLM output against the human-coded ground truth. Report per-category precision, recall, and F1. Aim for F1 > 0.7 per category; if any category falls below 0.5, consider whether the definition is ambiguous or the task requires fine-tuning rather than prompting (Halterman & Keith 2025).
- Examine the confusion matrix for systematic error patterns. If the model consistently confuses two categories, either merge them or sharpen the negative clarification in the codebook.
- If zero-shot F1 is inadequate, iterate in this order: (1) revise codebook definitions, (2) add few-shot examples, (3) fine-tune on labeled data. Do not skip to fine-tuning before testing whether the codebook is the problem (Halterman & Keith 2025).

### 6. Hybrid Human-LLM Workflows

- Implement a hybrid workflow: LLM classifies all responses, then human reviewers adjudicate uncertain cases. This achieves 93%+ accuracy at a fraction of full manual coding cost (Heseltine & Clemm von Hohenberg 2024).
- Flag responses for human review using one or more of: (a) LLM self-reported confidence (prompt the model to rate HIGH/MEDIUM/LOW), (b) disagreement across multiple model runs, (c) responses assigned to the residual category, (d) responses near decision boundaries (e.g., coded with two competing labels).
- Expect 10-15% of responses to require human review. If the flagging rate exceeds 25%, the codebook or model is performing poorly — return to pilot testing.
- Use human review not only for quality assurance but also for codebook refinement. Patterns in flagged cases often reveal systematic ambiguities that can be resolved with better definitions.
- For ensemble approaches, run two or more models (e.g., GPT-4o and Llama3-70B) and flag cases where they disagree. Ensemble means of LLM estimates correlate highly with expert survey benchmarks on party positioning tasks (Benoit et al. 2025).

### 7. Analysis and Interpretation

- Report code prevalence overall and by relevant subgroups (e.g., country, treatment condition). Present as proportions with confidence intervals.
- Cross-tabulate codes to assess co-occurrence. For construct validation, the joint prevalence of related codes (e.g., recognition of a cue + positive interpretation) is more informative than marginal prevalence alone.
- When using LLM classifications as variables in downstream analysis (regression, causal inference), acknowledge measurement error. Classification errors can attenuate or bias effect estimates. Consider bias-correction procedures when using classifier output as dependent or independent variables (Chae & Davidson 2025).
- LLMs can outperform human coders on tasks requiring contextual reasoning — interpreting implicit references, handling sarcasm, drawing on background knowledge (Tornberg 2025). But LLMs are not oracles. Treat LLM classifications as one measurement instrument, not ground truth.

### 8. Reporting

- Document the full classification pipeline: model name and exact version, temperature and other generation parameters, complete prompt text, codebook, date of classification runs.
- Report validation metrics: per-category precision, recall, F1 against human-coded ground truth. Report overall accuracy and Cohen's Kappa.
- Report the variance test: agreement rate between repeated runs on the same subset.
- Report the human review rate: what proportion of responses were flagged and adjudicated.
- Archive the complete prompt, codebook, and classification code. If using a proprietary model, note the risk of future deprecation and specify whether results can be reproduced (Barrie, Palmer & Spirling 2025).
- State explicitly whether the LLM was used for discovery (exploring what codes might apply) or confirmation (applying pre-specified codes). If the codebook was revised after seeing LLM output, report the revision history.
- When citing LLM-classified data in results, present representative examples for each code category. Readers need to assess whether the classification matches their substantive understanding (Glazier, Boydstun & Feezell 2021).

## Quality Checks

- [ ] Codebook includes all components per code: label, definition, clarification, negative clarification, examples (adapted from Halterman & Keith 2025)
- [ ] Learning regime (zero-shot, few-shot, fine-tuning, instruction-tuning) chosen based on data characteristics and available resources, not convenience
- [ ] Exact model version documented (not just model family name)
- [ ] Pilot sample of 50-100 responses hand-coded by two independent coders before LLM classification
- [ ] Inter-coder reliability (κ) reported for human coders; codebook revised if κ < 0.7
- [ ] Per-category precision, recall, and F1 reported against human ground truth
- [ ] Variance test conducted: same responses classified twice, agreement rate reported
- [ ] Hybrid workflow implemented: uncertain cases flagged and human-reviewed
- [ ] Human review rate reported (target: 10-15% of responses)
- [ ] Complete prompt, codebook, and classification code archived for replication
- [ ] Reproducibility risk acknowledged if using proprietary models (Barrie, Palmer & Spirling 2025)
- [ ] Data privacy addressed: PII not sent to commercial APIs without policy review (Chae & Davidson 2025)
- [ ] Downstream analysis acknowledges measurement error from classification
- [ ] Discovery vs. confirmation framing made explicit; codebook revision history documented if applicable
