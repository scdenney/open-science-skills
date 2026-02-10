---
name: design-conjoint-expert
description: Specialized logic for multidimensional choice experiments. Covers attribute architecture (orthogonality, nesting, restrictions), AMCE and marginal mean estimation, interaction effects, power analysis, design variants (paired-choice, factorial vignettes, between-subjects conversion), and regression models for conjoint data.
---

# Conjoint Design Expert

Use this skill when designing or reporting a conjoint experiment. It ensures the design is multidimensional, balanced, and statistically powered.

## Instructions for the Agent

### 1. Attribute Architecture
- **Orthogonality:** Ensure every attribute is independent of every other attribute to allow for the estimation of causal effects for each component.
- **Randomization of Order:** Order attributes randomly for each respondent to prevent "primacy" or "recency" effects, unless a specific logical flow is theoretically required.
- **Attribute Density:** Monitor for respondent fatigue. While 10 attributes are a common upper limit, evaluate if the complexity of the levels increases cognitive load.
- **Nested/Constrained Randomization:** Not all attributes need to be fully crossed. When ecological validity demands it, certain attribute levels can be linked or nested within other attributes (e.g., origin countries nested within policy domain). This is acceptable when: (a) the nesting is theoretically justified, (b) the primary attributes of interest remain fully independently randomized, and (c) the analyst acknowledges that nested attributes cannot be cleanly separated from their parent attribute. See Auspurg & Hinz (2015) on restricted randomization in factorial surveys.
- **Attribute-Level Restrictions:** Exclude implausible combinations that would confuse respondents or produce artifactual responses. Document all restrictions in the pre-analysis plan.

### 2. Statistical Power and Error Logic
- **Effective N:** Calculate sample size based on (Respondents $\times$ Tasks $\times$ Profiles).
- **Type S and Type M Errors:** When power is low, beware of "Type S" (Sign) errors (getting the direction wrong) and "Type M" (Magnitude) errors (exaggerating the effect size).
- **Minimum Detectable Effect (MDE):** Set the MDE based on the attribute with the highest number of levels, as this level will be the most difficult to estimate precisely.

### 3. Estimating Effects
- **Reference Categories:** Clearly identify the "baseline" or "reference" level for every attribute.
- **Average Marginal Component Effects (AMCE):** Frame results as the average change in the probability of being selected when an attribute changes from the reference level to the level of interest.
- **Marginal Means (MMs):** In addition to AMCEs, report marginal means — the model-predicted probability that a profile is selected when a given attribute level is shown, averaged over all other attributes. MMs provide absolute levels of support rather than relative differences, and are particularly useful for subgroup comparisons (Leeper, Hobolt, and Tilley 2020).
- **Interaction Effects:** When the design includes theoretically motivated interactions (e.g., procedure $\times$ composition), estimate interaction models and present results as conditional marginal means — separate AMCE/MM estimates for each level of the moderating attribute. Visualize with parallel/divergent line plots.

### 4. Design Variants
- **Paired-Choice vs. Rating:** Conjoint tasks can use forced binary choice (select one of two profiles) or rating scales (rate each profile independently). Forced choice produces a binary DV suitable for LPM estimation of AMCEs. Ratings provide continuous DVs that capture intensity. Best practice: use forced choice as primary DV with ratings as secondary/robustness check.
- **Factorial Vignette Design:** An alternative to tabular conjoint displays. Attributes are assembled into short paragraph-form vignettes rather than presented as attribute tables. This enhances realism and respondent engagement while preserving experimental control (Auspurg & Hinz 2015). Appropriate when: profiles describe complex scenarios (e.g., policy decisions) rather than simple object comparisons.
- **Between-Subjects to Conjoint Conversion:** When a between-subjects vignette experiment suffers from confounds (outcomes not held constant across conditions), consider converting to a conjoint. Benefits: (a) holds outcomes constant through independent randomization, (b) specifies concrete content rather than vague descriptions, (c) gains statistical power through repeated within-respondent measurements, (d) enables estimation of interaction effects.

### 5. Regression Models for Conjoint Data
- **Baseline AMCE Model:** Y_itj = $\alpha_i$ + $\beta$(Attributes_tj) + $\varepsilon_{itj}$. Respondent fixed effects ($\alpha_i$), SEs clustered by respondent. $\beta$ coefficients are AMCEs.
- **Interaction Models:** Add attribute $\times$ attribute interaction terms to test conditional effects. Present as conditional marginal means plots.
- **Cross-Group Comparison:** Estimate per-group AMCEs (e.g., per country) separately, then pool with group $\times$ attribute interactions for formal heterogeneity tests.
- **Secondary DV Replication:** Replicate all models using continuous rating outcome as robustness check.

## Quality Checks
- [ ] **Independence:** Is the randomization of attribute levels truly independent?
- [ ] **Power:** Was the sample size calculated using the level with the smallest predicted effect?
- [ ] **Baseline:** Are the reference categories for all attributes explicitly stated?
- [ ] **Ecological Validity:** Are all attribute combinations plausible? Have implausible combinations been restricted?
- [ ] **Nesting Documented:** If any attributes are nested or linked, is this documented and justified?
- [ ] **Interaction Pre-Specified:** Are theoretically motivated interactions specified in the pre-analysis plan?
- [ ] **Multiple DVs:** Is the primary DV (forced choice or rating) clearly identified, with secondary DVs labeled as robustness checks?
- [ ] **Vignette Assembly:** If using factorial vignettes, do the assembled paragraphs read coherently for all attribute combinations?
