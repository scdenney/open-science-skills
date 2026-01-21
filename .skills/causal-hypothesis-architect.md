---
name: causal-hypothesis-architect
description: Guides the transformation of theoretical concepts into falsifiable, counterfactual-based hypotheses. Focuses on identifying the Data Generating Process (DGP) and avoiding naive causal claims.
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

### 3. Scope and Generalization
- **Defining the Target Population:** A hypothesis is not universal. Explicitly name the population for whom the theory should hold.
- **Mechanism vs. Effect:** Distinguish between a hypothesis about a *causal effect* (did it happen?) and a hypothesis about a *causal mechanism* (why did it happen?).

## Quality Checks
- [ ] **Falsifiability:** Can I describe a specific data result that would force the rejection of this theory?
- [ ] **Identifying Assumptions:** Have I stated what must be true for this correlation to be interpreted as a cause?
- [ ] **Counterfactual:** Is the point of comparison (the control group) clearly defined?
- [ ] **Population:** Is the scope of the claim limited to a specific, named population?