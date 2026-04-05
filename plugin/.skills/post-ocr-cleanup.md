---
name: post-ocr-cleanup
description: Guide post-OCR text cleanup for research corpora. Covers LLM-based correction, rule-based fixes, quality diagnostics, multilingual considerations, and corpus-level quality assurance. Use when (1) choosing between LLM and rule-based OCR error correction, (2) designing prompts for LLM-based OCR cleanup, (3) applying constrained decoding to prevent correction hallucination, (4) building rule-based fixes for Unicode normalization or repetition artifacts, (5) evaluating cleanup quality beyond CER/WER, (6) handling diacritics restoration or script-specific spacing, (7) sampling and flagging documents for human review at corpus scale, or (8) tracking correction provenance for reproducibility.
argument-hint: "[describe your OCR output, languages, and error patterns]"
---

# Post-OCR Text Cleanup for Research Corpora

## Instructions

### 1. Cleanup Strategy Selection

- **Choose between LLM correction, rule-based fixes, or a hybrid pipeline based on error type.** LLM correction excels at context-dependent errors (wrong but plausible characters, broken words, missing diacritics). Rule-based fixes handle deterministic patterns (control characters, Unicode normalization, repetition artifacts, whitespace) with zero risk of content alteration. Use rule-based fixes unconditionally for these categories.
- **Default to the hybrid approach for research corpora.** Run LLM correction first on all pages, then apply deterministic rule fixes on top. This order matters: LLM correction may introduce formatting artifacts that rule fixes clean up, while the reverse order wastes rule-fix effort on text the LLM will rewrite (Machidon & Machidon 2025).
- **Pilot-test LLM correction per language before corpus-wide deployment.** LLM post-correction effectiveness is highly language-dependent: English achieves 7-58% CER reduction, while some languages see no improvement or degradation (Kanerva et al. 2025). Never assume cross-language transferability.
- **Consider whether correction is needed at all.** If the downstream analysis tolerates OCR noise (e.g., topic modeling is robust to moderate error rates), the risk of correction-introduced errors may outweigh the benefit. Define the quality threshold before choosing a strategy.

### 2. LLM-Based Correction

- **Use a small text-only model, not the full VLM.** The correction input is already text; image understanding is not needed. A 7-8B parameter model with 4-bit quantization requires only ~4GB VRAM and processes pages in 2-3 seconds (Thomas et al. 2024).
- **Write tight correction prompts.** Instruct the model to "fix clear OCR mistakes only: wrong characters, broken words, garbled punctuation, repetition artifacts. Do not translate, modernize, or add anything. Output the corrected text only." Loose prompts invite hallucination.
- **Add language-specific instructions.** For Polish, explicitly mention diacritics restoration (ą, ć, ę, ł, ń, ó, ś, ź, ż). For Korean, mention hangul integrity and hanja preservation. The correction model needs to know which character set to favor.
- **Mitigate hallucination with constrained decoding.** Constrained decoding techniques (logit biasing, grammar-constrained generation) that enforce character-level similarity between input and output prevent the model from inserting plausible but fabricated content (Sastre et al. 2025). At minimum, track and flag pages where correction diverges substantially from the original.
- **Disable chain-of-thought for correction tasks.** Reasoning modes add latency without improving transcription fidelity. Use greedy decoding (`do_sample=False`) for deterministic output.
- **Consider multimodal correction for severely degraded pages.** Feeding both the original page image and the OCR text to the correction model can achieve below 1% CER on degraded documents, but doubles GPU cost (Greif et al. 2025). Reserve this for flagged pages, not routine processing.
- **Track all changes with edit-distance metrics.** Compute Levenshtein distance and change ratio (edit distance / original length) per page. Flag pages where the correction model altered more than 10% of characters for manual review — high change ratios may indicate hallucination rather than correction (Bourne 2024).

### 3. Rule-Based Fixes

- **Apply deterministic fixes in a fixed order.** (1) Control character removal, (2) zero-width and invisible Unicode character removal, (3) NFKC Unicode normalization, (4) consecutive character repetition collapse, (5) standalone symbol line removal, (6) whitespace normalization. This ordering prevents interactions between fixes.
- **Tune repetition collapse thresholds to the corpus.** The default of collapsing runs of 4+ identical characters to 3 works for most scripts but may need adjustment for languages with legitimate long character sequences or for documents with intentional formatting patterns.
- **Rule-based diacritics restoration is viable for some languages.** For Polish, rule-based approaches (removing word breaks, rejecting case-changing corrections, restoring diacritical characters replaced with visually similar ASCII) are competitive with LLM-based correction and more predictable (Ogrodniczuk 2022).
- **Generate synthetic OCR errors for training when ground truth is scarce.** Character-level Markov corruption can produce realistic synthetic training data for correction models without requiring hand-annotated ground truth (Guan & Greene 2024). Under-corrupted training data outperforms over-corrupted.
- **Preserve the raw text alongside every cleaned version.** Rule-based fixes are deterministic and reversible, but downstream researchers may prefer different normalization choices. Store both raw and cleaned text at every stage.

### 4. Quality Diagnostics and Metrics

- **Move beyond CER/WER as the sole quality measure.** Character-level edit distance is sensitive to normalization choices, does not capture semantic correctness, and can disagree across evaluation tools (Beyene & Dancy 2026). A model can scramble column order while achieving perfect CER.
- **Build a multi-signal diagnostic profile per page.** Character composition ratios (diacritics-to-Latin for European scripts, CJK character ratios for East Asian), repetition artifact density, symbol density, and page length anomalies (empty, suspiciously short, suspiciously long) each capture different failure modes.
- **Use dictionary hit rates as an automated quality proxy.** Tokenize OCR output and check against morphological dictionaries or analyzers. Compute per-page and per-document valid-token rates. This scales to every page in the corpus without human effort.
- **Calibrate thresholds against downstream task requirements.** OCR quality directly impacts NER, classification, topic modeling, and other downstream NLP tasks (van Strien et al. 2020). Define acceptable error rates based on what your analysis pipeline can tolerate, not abstract accuracy targets. Researchers in computational humanities should evaluate OCR quality relative to their analytical needs (Backer & Hyman 2025).
- **Classify pages by recommended action.** Map diagnostic signals to action categories: OK (no intervention), rule-fixable (deterministic cleanup sufficient), LLM-fixable (context-dependent errors), manual review (critical failures). This prioritizes human attention on the pages that need it most.

### 5. Multilingual Considerations

- **Check diacritic ratios for Latin-script languages.** For Polish, a page of body text with zero diacritical characters almost certainly has OCR errors. Flag pages where the diacritic-to-alphabetic ratio drops below a language-calibrated threshold (Ogrodniczuk 2022).
- **Treat Korean spacing as a distinct post-OCR task.** Korean uses space-delimited eojeol units, and OCR frequently merges or splits them incorrectly. Dedicated spacing models (Choi & Kim 2021) outperform general-purpose LLM correction for this specific error type.
- **Use morphological analyzers as correction validators.** Morfeusz for Polish, Mecab-ko for Korean — tokens that parse successfully are likely correct; tokens that fail to parse are OCR error candidates. This provides both a diagnostic signal and a correction filter.
- **Protect dialectal and archaic text from normalization.** Correction models trained on standard modern language may damage historical orthography, dialectal spellings, or archaic vocabulary. Test on a sample of the oldest and most linguistically distinctive documents before corpus-wide deployment (Kanerva et al. 2025; Machidon & Machidon 2025).

### 6. Corpus-Level Quality Assurance

- **Implement a three-tier review workflow.** (1) Automated pass/fail based on diagnostic thresholds applied to all documents, (2) spot-check review of flagged documents (10-15% of corpus), (3) deep review of a random sample of passing documents (2-5% of corpus) to catch false negatives.
- **Define specific flagging thresholds.** Mean quality score below 0.80, LLM correction change ratio above 10%, dictionary hit rate below 80%, or more than 5% empty pages. Calibrate these thresholds against your pilot evaluation results.
- **Route flagged documents to specific remediation actions.** Re-run LLM cleanup with a different prompt, re-OCR at higher DPI or without quantization, or escalate to manual transcription. Each action has different cost and quality implications.
- **Produce a corpus-level quality dashboard.** Aggregate per-document metrics into a summary CSV or report: document ID, language, page count, mean quality score, dictionary hit rate, correction change ratio, flag status, review outcome. This supports both operational monitoring and methods reporting.

### 7. Provenance and Documentation

- **Maintain a complete audit trail of all corrections.** Each correction should be attributed to its source (LLM model version, rule name) with before/after text preserved at the page level (Guo & Wei 2026). Correction pathways can substantially alter extracted entities and downstream interpretations.
- **Log model details for the LLM correction stage.** Model name, quantization method, prompt text, generation parameters (temperature, max tokens, sampling), and per-page edit-distance metrics. This is the minimum required to reproduce or audit the correction.
- **Log rule-fix details.** Which rules fired and how many characters each rule changed per page. This enables downstream researchers to assess whether rule fixes were aggressive or conservative for a given document.
- **Produce a cleanup comparison artifact.** A CSV or JSON with page-level before/after text pairs and metrics (edit distance, change ratio, flagged status) enables downstream researchers to assess correction quality and choose their preferred text version.
- **Record all thresholds and human review outcomes.** Sampling decisions, flagging thresholds, remediation actions, and human review results should be documented in a methods section alongside the corpus, not just in internal notes.

## Quality Checks

- [ ] **Strategy justified:** Cleanup approach (LLM, rule-based, or hybrid) chosen based on error types, corpus size, and resource constraints
- [ ] **LLM correction pilot-tested per language:** Cleanup validated on a sample from each language before corpus-wide application (Kanerva et al. 2025)
- [ ] **Hallucination risk mitigated:** Constrained decoding or tight prompt constraints applied to prevent fabricated content (Sastre et al. 2025)
- [ ] **Change ratio tracked:** Per-page edit distance and change ratio computed and stored; pages exceeding 10% change flagged for review
- [ ] **Rule-based fixes ordered correctly:** Deterministic fixes applied in the prescribed sequence (control chars, zero-width, NFKC, repetitions, symbols, whitespace)
- [ ] **Metrics go beyond CER/WER:** Quality assessed using multiple signals (character composition, dictionary hit rates, diagnostic flags), not CER/WER alone (Beyene & Dancy 2026)
- [ ] **Downstream impact considered:** Quality thresholds set relative to the intended analysis, not abstract accuracy targets (van Strien et al. 2020)
- [ ] **Language-specific patterns addressed:** Diacritics ratios, morphological parsing, and spacing rules checked for each language in the corpus
- [ ] **Dialectal and archaic text protected:** Correction models tested for damage to non-standard language varieties (Machidon & Machidon 2025)
- [ ] **Flagging thresholds defined:** Specific numeric thresholds set for automated quality flags (quality score, change ratio, dictionary hit rate, empty page rate)
- [ ] **Stratified human review conducted:** Review sample stratified by language, document age, print quality, and flag category
- [ ] **Both raw and cleaned text preserved:** Original OCR output retained alongside every cleanup stage for auditability
- [ ] **Correction provenance logged:** Each correction attributed to its source (LLM model, rule name) with before/after text and edit metrics (Guo & Wei 2026)
- [ ] **Cleanup comparison artifact produced:** Page-level CSV or JSON with raw text, cleaned text, and per-page metrics archived
- [ ] **Methods documented:** All thresholds, sampling decisions, model versions, prompts, and human review outcomes recorded
