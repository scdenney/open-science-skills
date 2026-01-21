---
name: design-conjoint-expert
description: Specialized logic for multidimensional choice experiments. Focuses on attribute orthogonality, AMCE estimation, and power analysis.
---

# Conjoint Design Expert

Use this skill when designing or reporting a conjoint experiment. It ensures the design is multidimensional, balanced, and statistically powered.

## Instructions for the Agent

### 1. Attribute Architecture
- **Orthogonality:** Ensure every attribute is independent of every other attribute to allow for the estimation of causal effects for each component.
- **Randomization of Order:** Order attributes randomly for each respondent to prevent "primacy" or "recency" effects, unless a specific logical flow is theoretically required.
- **Attribute Density:** Monitor for respondent fatigue. While 10 attributes are a common upper limit, evaluate if the complexity of the levels increases cognitive load.

### 2. Statistical Power and Error Logic
- **Effective N:** Calculate sample size based on (Respondents $\times$ Tasks $\times$ Profiles). 
- **Type S and Type M Errors:** When power is low, beware of "Type S" (Sign) errors (getting the direction wrong) and "Type M" (Magnitude) errors (exaggerating the effect size).
- **Minimum Detectable Effect (MDE):** Set the MDE based on the attribute with the highest number of levels, as this level will be the most difficult to estimate precisely.

### 3. Estimating Effects
- **Reference Categories:** Clearly identify the "baseline" or "reference" level for every attribute.
- **Average Marginal Component Effects (AMCE):** Frame results as the average change in the probability of being selected when an attribute changes from the reference level to the level of interest.



## Quality Checks
- [ ] **Independence:** Is the randomization of attribute levels truly independent?
- [ ] **Power:** Was the sample size calculated using the level with the smallest predicted effect?
- [ ] **Baseline:** Are the reference categories for all attributes explicitly stated?