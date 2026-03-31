---
name: topic-modeling
description: Guides structural topic model (STM) specification for survey and experimental text data. Covers model selection, preprocessing, topic count diagnostics, covariate effects on prevalence, and reporting. Use when (1) selecting a topic model for open-ended survey responses or text corpora, (2) specifying an STM with metadata covariates, (3) choosing the number of topics and evaluating diagnostics, (4) interpreting topic content and estimating covariate effects, (5) preprocessing text data for topic modeling, (6) validating output against treatment groups, or (7) reporting topic modeling results.
argument-hint: "[describe your corpus and research question]"
---

# Topic Modeling for Survey and Experimental Text Data

## Instructions

### 1. Model Selection

- Default to Structural Topic Models (STM) when analyzing text from surveys or experiments. STM incorporates document-level metadata — treatment conditions, respondent demographics, country — directly into estimation, allowing prevalence and content to vary with covariates (Roberts et al. 2014).
- Use standard LDA only when no document-level covariates are needed and the corpus is large enough for unsupervised discovery (Blei, Ng & Jordan 2003).
- Consider BERTopic when working with short texts where word co-occurrence is sparse, or when multilingual embedding-based similarity is required (Grootendorst 2022). BERTopic clusters document embeddings rather than relying on bag-of-words, which can capture semantic similarity missed by word-count models.
- Recognize the distinction between topic categorization and attitude inference: topic models reveal what respondents *discussed*, not what they *believe*. If the goal is inferring latent attitudes rather than categorizing surface content, complement topic modeling with targeted classification (Hobbs & Green 2025).

### 2. Preprocessing

- Make preprocessing decisions explicit and justify each choice. Preprocessing is not neutral — stemming, stopword removal, and term-frequency thresholds all affect which topics emerge (Denny & Spirling 2018).
- Lowercase all text. Remove punctuation and numbers unless they carry substantive meaning in the domain.
- Remove stopwords using a standard list, but inspect the list for domain-relevant terms that should be retained (e.g., "foreign" in immigration research).
- Apply stemming only after checking that it does not collapse substantively distinct terms. Compare results with and without stemming as a robustness check (Denny & Spirling 2018).
- Set a lower-frequency threshold to remove very rare terms (e.g., appearing in fewer than 10 documents). This reduces noise without losing substantive content. Report the threshold chosen.
- For translated text, preprocess after translation. Note that translation artifacts (e.g., inconsistent phrasing across translators) may affect topic coherence — document any translation pipeline.

### 3. Model Specification

- Specify the prevalence formula to include theoretically relevant covariates. For survey experiments, include treatment conditions; for cross-national data, include country. Example: `prevalence = ~ treatment + country` (Roberts et al. 2014).
- Optionally specify a content formula when you expect the *words* associated with a topic (not just its prevalence) to vary by covariate. This is useful when the same topic manifests with different vocabulary across groups.
- Use spectral initialization (`init.type = "Spectral"`) for reproducibility. Spectral initialization is deterministic given the same data, unlike random initialization which requires multiple runs (Roberts, Stewart & Tingley 2019).
- Set a random seed and record it regardless of initialization method.

### 4. Selecting the Number of Topics

- Do not rely on a single metric. Evaluate candidate models across a range of K values (e.g., K = 5 to 30) using multiple diagnostics: semantic coherence, exclusivity, held-out likelihood, and residuals (Roberts, Stewart & Tingley 2019).
- Semantic coherence measures whether high-probability words within a topic co-occur in the corpus. Higher is better, but coherence alone favors very common topics (Mimno et al. 2011).
- Exclusivity measures whether high-probability words are distinctive to one topic. The coherence-exclusivity frontier identifies models that balance both (Roberts, Stewart & Tingley 2019).
- After narrowing candidates statistically, read the top words and representative documents for each topic. The final K should be interpretable — topics should be substantively meaningful and distinguishable from one another (Chang et al. 2009).
- Report the range of K values considered, the diagnostics used, and the rationale for the final choice.

### 5. Interpretation and Validation

- For each topic, report the top 10-15 words by probability and by FREX (frequency-exclusivity weighted). FREX words are often more interpretable because they are both common within the topic and rare outside it (Roberts, Stewart & Tingley 2019).
- Extract and read 3-5 representative documents per topic using `findThoughts()` or equivalent. Do not interpret topics from word lists alone — the documents provide essential context.
- Assign short substantive labels to each topic based on both word lists and representative documents. Labels should be descriptive (e.g., "economic contribution concerns") not technical (e.g., "Topic 7").
- Estimate covariate effects on topic prevalence using `estimateEffect()`. For experimental data, test whether treatment conditions significantly shift which topics respondents discuss. For cross-national data, test whether topic prevalence differs by country. Plot these effects with confidence intervals (Roberts et al. 2014).
- For construct validation in survey experiments: check whether topics related to the intended construct (e.g., civic engagement) show higher prevalence among respondents exposed to relevant treatment conditions. If the experimental manipulation did not affect topic prevalence, this is evidence of a construct validity problem.

### 6. Robustness and Sensitivity

- Run the model at neighboring values of K (e.g., K-2, K+2) to check whether substantive conclusions are sensitive to topic count.
- Compare results with and without stemming as a preprocessing robustness check (Denny & Spirling 2018).
- If using STM, compare results with and without covariates to assess how much the covariate structure shapes the topic solution.
- For experimental data, verify that topic assignments are not driven by a small number of high-frequency terms. Inspect whether removing the single most common term in a topic changes its interpretation.

### 7. Reporting

- Report: preprocessing pipeline (stopwords, stemming, frequency thresholds), number of topics and selection rationale, initialization method, convergence diagnostics, random seed.
- Present a topic summary table with: topic number, label, top FREX words, prevalence (overall and by covariate group), and 1-2 example documents.
- When reporting covariate effects on prevalence, present coefficient estimates with confidence intervals. Visualize cross-group differences (e.g., side-by-side prevalence plots by country or treatment).
- Distinguish discovery from confirmation: topic modeling is exploratory. State explicitly which findings were anticipated and which emerged from the data. If using topics to validate constructs, frame findings in terms of whether the intended constructs appeared, not whether the model "confirmed" a hypothesis (Grimmer & Stewart 2013).
- Make replication materials available: analysis code, preprocessing decisions, and random seed. If the corpus cannot be shared, provide the topic-term matrix and document-topic proportions (Grimmer & Stewart 2013).

## Quality Checks

- [ ] Model type justified (STM vs. LDA vs. BERTopic) given data structure and research question
- [ ] Preprocessing decisions documented and justified (stemming, stopwords, thresholds)
- [ ] Number of topics selected using multiple diagnostics (coherence, exclusivity, held-out likelihood) plus substantive interpretability
- [ ] Covariates included in prevalence formula match the experimental or observational design
- [ ] Each topic interpreted using both word lists (probability + FREX) and representative documents
- [ ] Covariate effects on topic prevalence estimated and reported with confidence intervals
- [ ] Robustness checks performed (alternative K, preprocessing variants)
- [ ] Topics labeled descriptively based on content, not just numbered
- [ ] Discovery vs. confirmation framing made explicit
- [ ] Random seed, initialization method, and convergence reported
- [ ] Replication materials (code, preprocessing pipeline, seed) available or planned
