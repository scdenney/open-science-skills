---
name: causal-hypothesis-architect
description: Guides the transformation of theoretical concepts into falsifiable, counterfactual-based hypotheses with formal estimands, explicit model mappings, and clear separation of confirmatory and exploratory tests. Focuses on identifying the Data Generating Process (DGP), avoiding naive causal claims, and structuring hypothesis architectures for multi-experiment pre-analysis plans.
---

# Causal Hypothesis Architect

Use this skill to ensure that every research claim is a rigorous "Popperian" test rather than a vague prediction. It forces the agent to define the causal path and the specific observations that would prove the theory wrong.

## Instructions for the Agent

### 1. The Identification Challenge
- **Define the Data Generating Process (DGP):** Before drafting the hypothesis, describe the set of rules that governs how the data is created. What are the underlying mechanics of the world being studied?
- **Map the Causal Diagram:** Visualize the relationship using a Directed Acyclic Graph (DAG), if possible and appropriate. This is especially important for causal designs using observational data. Identify "Backdoor Paths", such as variables that correlate with both the cause and the effect.
- **Closing the Backdoors:** State clearly which variables must be controlled for to isolate the treatment effect. If using an experiment, explain how random assignment "closes" these paths. This is especially important for causal designs using observational data.

### 2. Hypothesis Formulation
- **Popperian Falsifiability:** Frame the hypothesis as a "basic statement", or a specific observation that, if found to be false, would invalidate the theory.
- **The Counterfactual Logic:** Every hypothesis must specify a comparison. Define the "untreated" world. If the hypothesis is that $X$ causes $Y$, what is the specific state of the world where $X$ is absent?
- **Directional Clarity:** Avoid "existence" claims (e.g., "there is an effect"). Use "ordinal" claims that specify the direction (higher/lower) and, where possible, the expected functional form.
- **Null-by-Design Thinking:** Consider if the research is better served by a "Null-by-Design" experiment, where the expectation is no effect unless a specific threshold of intensity is met.
- **Estimand Specification:** Every hypothesis must map to a specific estimand — the statistical quantity that, if estimated, would test the hypothesis. For experimental designs, this typically means specifying: (a) the treatment contrast (what is compared to what), (b) the outcome metric (probability, scale score, etc.), and (c) the model that produces the estimate (e.g., AMCE from a conjoint, ATE from a vignette experiment). A hypothesis without a named estimand is not pre-registrable.
- **Disconfirming Evidence:** Beyond falsifiability in the abstract, specify concretely what pattern of results would constitute evidence *against* the hypothesis. For example: "If the interaction coefficients are jointly significant and indicate that procedural effects vanish when group threat is activated, this would favor group-centric accounts over the NBM."

### 3. Scope and Generalization
- **Defining the Target Population:** A hypothesis is not universal. Explicitly name the population for whom the theory should hold.
- **Mechanism vs. Effect:** Distinguish between a hypothesis about a *causal effect* (did it happen?) and a hypothesis about a *causal mechanism* (why did it happen?).
- **Scope Conditions vs. Hypotheses:** Not all theoretical expectations should be confirmatory hypotheses. When the theory predicts that effect magnitudes will vary across contexts (e.g., countries, institutional configurations) but does not make precise directional predictions about *which* context produces the largest effect, treat these expectations as "scope conditions" — interpretive frameworks examined descriptively, not through confirmatory tests. This avoids the proliferation of underpowered confirmatory hypotheses while preserving theoretical richness.

### 4. Hypothesis Architecture in Multi-Experiment Designs
- **Sequential Numbering:** When a study includes multiple experiments, number hypotheses sequentially across experiments (e.g., H1–H2 for Experiment 1, H3–H5 for Experiment 2) to maintain clarity and enable cross-referencing.
- **Micro-Macro Bridging:** When experiments target different levels of analysis (e.g., individual-level preferences vs. institutional-level legitimacy), hypotheses should explicitly bridge across levels. State how the macro-level prediction extends or parallels the micro-level one.
- **Confirmatory vs. Exploratory:** Clearly separate confirmatory hypotheses (pre-registered, subject to strict inference) from exploratory tests (theory-guided but not confirmatory). Common candidates for exploratory status: individual-level moderators (e.g., partisanship), three-way interactions, and cross-national comparisons where the theory underdetermines the expected pattern.
- **Hypothesis-to-Model Mapping:** Each confirmatory hypothesis should be explicitly linked to a specific regression model in the empirical strategy. This mapping prevents "analytical degrees of freedom" — the researcher must commit in advance to which model tests which claim.

## Quality Checks
- [ ] **Falsifiability:** Can I describe a specific data result that would force the rejection of this theory?
- [ ] **Identifying Assumptions:** Have I stated what must be true for this correlation to be interpreted as a cause?
- [ ] **Counterfactual:** Is the point of comparison (the control group) clearly defined?
- [ ] **Population:** Is the scope of the claim limited to a specific, named population?
- [ ] **Estimand:** Does each hypothesis name the specific statistical quantity (AMCE, ATE, interaction coefficient) that would test it?
- [ ] **Disconfirming Pattern:** Is the specific data pattern that would undermine the theory described?
- [ ] **Confirmatory vs. Exploratory:** Are hypotheses clearly sorted into confirmatory (pre-registered) and exploratory (theory-guided) categories?
- [ ] **Scope Conditions:** Are context-dependent expectations framed as scope conditions rather than confirmatory hypotheses?
- [ ] **Model Mapping:** Is each hypothesis linked to a specific regression specification?
