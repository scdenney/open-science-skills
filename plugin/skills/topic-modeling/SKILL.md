---
disable-model-invocation: true
name: topic-modeling
description: Advises on setting up and validating topic models for survey and experimental text. Covers the discovery-versus-measurement question, choosing STM, LDA, or BERTopic, preprocessing consequences, prevalence and content formulas, topic-count selection across coherence, exclusivity and FREX, held-out likelihood, and residuals, validation of topics against human judgment, robustness, and DA-RT-compliant reporting. Use when the user has open-ended responses or another corpus and asks what topics are present, how many topics to use, about STM, searchK, coherence, or FREX, or wants topic prevalence compared across treatment arms or countries. Fixed-codebook coding goes to text-classification.
argument-hint: '[describe your corpus and research question]'
---

# Topic Modeling for Survey and Experimental Text Data

## Instructions

Help the user design the analysis before fitting anything. Work through the decisions below in order, explain what each choice changes and which standard governs it, and record the choice with its rationale. Every one of them — model, preprocessing, covariates, K, labels — shapes which topics appear, so each belongs in the methods section.

### 1. Discovery or Measurement?

Settle this first; it decides the rest.

- Topic models are discovery tools: they show what respondents *discussed*. If the user already has categories and wants each document coded against them, that is classification — use `text-classification`.
- If the goal is to infer latent attitudes rather than categorize surface content, topics alone will not do it; complement them with an embeddings-based scaling of contextually common words or a supervised classifier (Hobbs & Green 2025).
- A common sound design is two-stage: discover categories with a topic model, then write those categories into a codebook and measure them with validated supervised classification for confirmatory tests (Grimmer & Stewart 2013).
- If topic-prevalence effects will be tested as hypotheses, pre-register them (`pre-registration-writing`) so `estimateEffect()` output is confirmatory rather than exploratory by default (Nosek et al. 2018).

### 2. Model Choice

- **STM** is the default for survey and experimental text. It brings document metadata — treatment arm, demographics, country — into estimation so prevalence and content can vary with covariates (Roberts et al. 2014).
- **LDA** fits when no document-level covariates are needed and the corpus is large enough for unsupervised discovery (Blei, Ng & Jordan 2003).
- **BERTopic** fits short texts where word co-occurrence is sparse, or multilingual corpora where embedding similarity is needed (Grootendorst 2022). It clusters embeddings with HDBSCAN, so each document gets one hard topic (no mixed membership), c-TF-IDF topic words can be unstable on small corpora, and there is no native covariate framework.

### 3. Preprocessing

Preprocessing is not neutral: stemming, stopword removal, and frequency thresholds all change which topics emerge (Denny & Spirling 2018). Justify each choice.

- Lowercase; drop punctuation and numbers unless they carry meaning in the domain.
- Use a standard stopword list, but inspect it for domain terms that should stay (e.g., "foreign" in immigration research).
- Stem only after checking that it does not merge substantively distinct terms, and compare results with and without stemming (Denny & Spirling 2018).
- Prune rare terms with a threshold that scales with the corpus: a fixed 2-5 documents for small open-ended corpora; roughly 0.5-1% of documents for larger ones (Grimmer & Stewart 2013). In `stm`, `plotRemoved()` shows terms and documents dropped across candidate thresholds before you pass one to `prepDocuments()`. Report the threshold and the retained counts.
- For translated text, preprocess after translation and document the translation pipeline; inconsistent translation can degrade coherence.

### 4. Model Specification

- Put theoretically relevant covariates in the prevalence formula — treatment arm for experiments, country for cross-national data: `prevalence = ~ treatment + country` (Roberts et al. 2014).
- Add a content formula only when you expect the *words* of a topic, not just its prevalence, to differ by covariate (different framings across countries or arms). Content covariates parameterize SAGE-style deviations from a baseline, which complicates comparing β across groups; inspect group vocabulary with `sageLabels()` (Roberts, Stewart & Tingley 2014; 2019).
- Use spectral initialization (`init.type = "Spectral"`). It is deterministic on a given machine and BLAS configuration; cross-machine precision can still differ slightly, so record hardware and OS (Roberts, Stewart & Tingley 2019).
- Set and record a seed regardless of initialization, plus the `stm` version and R session info.

### 5. Selecting the Number of Topics

- Use several diagnostics across a range of K (e.g., 5-30): semantic coherence, exclusivity, held-out likelihood, and residuals (Roberts, Stewart & Tingley 2019). `searchK()` returns all four; `selectModel()` fits several initializations at a fixed K and returns the coherence-exclusivity frontier (useful only with non-spectral initialization).
- Coherence rewards topics whose top words co-occur but favors very common topics (Mimno et al. 2011). For a poor topic, diagnose the failure — *chained* (two concepts joined by a shared word), *intruded* (unrelated words mixed in), *random*, or *unbalanced* (general and specific terms mixed) — because the diagnosis says whether to change K, preprocessing, or covariates.
- Exclusivity: `stm` reports FREX, a weighted harmonic mean of frequency and exclusivity ranks (default ω = 0.7). The coherence-FREX frontier marks models that balance both (Roberts, Stewart & Tingley 2019).
- Held-out likelihood is one input, not the decider: it can correlate *negatively* with human interpretability (Chang et al. 2009). When the metrics disagree, prefer interpretability.
- After narrowing statistically, read top words and representative documents for each candidate. The final K must give substantively meaningful, distinguishable topics.
- Report the K range, the diagnostics, and the rationale for the final choice.

### 6. Interpretation and Validation Against Human Judgment

Statistical fit does not show that a topic measures what its label claims. Validate the topics as measures (Grimmer & Stewart 2013).

- For each topic, report the top 10-15 words by probability and by FREX (Roberts, Stewart & Tingley 2019).
- Read 3-5 representative documents per topic (`findThoughts()`). Word lists alone are not enough to interpret a topic.
- Label topics descriptively ("economic contribution concerns"), from both word lists and documents. Write each label with a one-sentence definition so the labels work as a codebook others can apply.
- Test the labels against human coders. Have coders blind to the model assign a random sample of documents to the labeled topics (or to none) and report agreement with the model's dominant topic, using Krippendorff's α or κ (Krippendorff 2019; Landis & Koch 1977). Human word-intrusion and topic-intrusion tasks test whether topics are interpretable at all (Chang et al. 2009). Low agreement means the labels or K need revision before any substantive claim.
- Estimate covariate effects on prevalence with `estimateEffect()` and plot them with confidence intervals (Roberts et al. 2014). When testing many topics against a treatment, report FDR or similar corrections alongside uncorrected estimates.
- Guard against spurious treatment effects with `permutationTest()`, which permutes the treatment label and refits to give a randomization-inference null for each topic's effect (Roberts, Stewart & Tingley 2014; 2019).
- For construct validation in survey experiments, check whether topics tied to the intended construct rise among respondents exposed to the relevant treatment. A null is *suggestive* of a construct-validity problem, not proof: first rule out low power, a K that splits or merges the construct topic, a content-covariate effect (the treatment changed *how* the topic was framed, not *whether* it was discussed), and preprocessing that dropped construct vocabulary.

### 7. Robustness

- Refit at neighboring K (K−2, K+2) and check whether substantive conclusions hold.
- Compare with and without stemming (Denny & Spirling 2018).
- For STM, compare with and without covariates to see how much they shape the solution.
- Check that topics are not driven by one high-frequency term: remove a topic's most common term and see whether its interpretation changes.
- Inspect topic correlations with `topicCorr()`.

### 8. Reporting

- Preprocessing pipeline (stopwords, stemming, thresholds, documents and terms retained after `prepDocuments`), K and its rationale, initialization, convergence (max EM iterations, final variational bound), seed, `stm` version, R session info. For the broader checklist see `methods-reporting`.
- A topic summary table: number, label and definition, top FREX words, prevalence overall and by covariate group, and 1-2 example documents.
- Human validation results: coder procedure, sample size, and agreement with the model's topic assignments.
- Covariate effects as estimates with confidence intervals, with side-by-side prevalence plots by group.
- Discovery versus confirmation: say which findings were anticipated and which emerged. Treating every topic comparison as a hypothesis test recreates the researcher-degrees-of-freedom problem (Simmons, Nelson & Simonsohn 2011; Nosek et al. 2018). When topics validate constructs, report whether the intended constructs appeared, not that the model "confirmed" a hypothesis (Grimmer & Stewart 2013).
- Replication materials: code, preprocessing decisions, seed. If the corpus cannot be shared, provide the topic-term matrix and document-topic proportions (Grimmer & Stewart 2013).

## Quality Checks

- [ ] Discovery vs. measurement settled; categories already known routed to `text-classification`
- [ ] Model type (STM, LDA, BERTopic) justified by data structure and question
- [ ] Preprocessing choices documented and justified; retained counts reported
- [ ] K chosen from multiple diagnostics (`searchK`/`selectModel`) plus interpretability; held-out vs. coherence conflicts resolved toward interpretability (Chang et al. 2009)
- [ ] Prevalence (and, if justified, content) covariates match the design; `sageLabels()` inspected for content covariates
- [ ] Topics interpreted from probability and FREX words plus `findThoughts()` documents, and labeled with definitions
- [ ] Topic labels validated against blind human coding with agreement reported (Grimmer & Stewart 2013)
- [ ] Prevalence effects from `estimateEffect()` with confidence intervals and multiple-comparison adjustment
- [ ] `permutationTest()` run for experimental treatment effects
- [ ] Robustness: neighboring K, preprocessing variants, covariate structure, `topicCorr()`
- [ ] Discovery vs. confirmation stated; confirmatory prevalence hypotheses pre-registered where feasible
- [ ] Seed, initialization, convergence, `stm` version, session info, and replication materials archived

## Example

A minimal STM pattern for a survey experiment where `df` has one row per respondent with `open_ended_responses` (text) and `treatment_arm` (factor). Adapt it; stages (a)-(d) map onto Sections 3-6.

```r
library(stm)
set.seed(20260418)

# (a) Preprocess and choose the rare-term threshold (Section 3).
processed <- textProcessor(df$open_ended_responses, metadata = df)
plotRemoved(processed$documents, lower.thresh = seq(1, 20, by = 2))
prepped <- prepDocuments(processed$documents, processed$vocab,
                         processed$meta, lower.thresh = 5)

# (b) Sweep K: coherence, exclusivity, held-out likelihood, residuals (Section 5).
k_search <- searchK(prepped$documents, prepped$vocab, K = c(5, 10, 15, 20),
                    prevalence = ~ treatment_arm, data = prepped$meta,
                    init.type = "Spectral")
plot(k_search)

# (c) At the chosen K, compare random initializations on the frontier.
# Spectral init is deterministic, so selectModel needs a random init here.
k_chosen   <- 10
candidates <- selectModel(prepped$documents, prepped$vocab, K = k_chosen,
                          prevalence = ~ treatment_arm, data = prepped$meta,
                          runs = 20, init.type = "LDA")
plotModels(candidates)
fit <- candidates$runout[[1]]

# (d) Treatment effects on prevalence (Section 6); follow with permutationTest and topicCorr.
effects <- estimateEffect(1:k_chosen ~ treatment_arm, fit,
                          metadata = prepped$meta, uncertainty = "Global")
summary(effects)
```
