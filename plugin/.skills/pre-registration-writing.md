---
name: pre-registration-writing
description: Guides writing a complete pre-analysis plan (PAP) for experimental social science. Use when (1) choosing a registry platform (OSF, EGAP, AsPredicted), (2) structuring a PAP document end-to-end, (3) specifying analytical strategies with locked, conditional, and exploratory tiers, (4) pre-registering analysis code on simulated data, (5) writing contingency plans for design failures, (6) documenting deviations from a registered plan, or (7) planning a registered report submission. Covers PAP structure, decision rules, code registration, contingency trees, deviation reporting, and timeline logistics.
---

# Pre-Analysis Plan Writer

## Instructions

### 1. Registry Selection
- **OSF (Open Science Framework):** Use for maximum flexibility. Supports free-form documents, file attachments (analysis code, stimuli), version control, and optional embargo periods. Registration is timestamped and immutable once confirmed. Best for complex designs that require supplementary materials.
- **EGAP (Evidence in Governance and Politics):** Use for political science, development economics, and governance research. EGAP registrations undergo administrative review before acceptance, which provides a quality signal. The structured form prompts for specific design elements. Best when the research community values EGAP-specific credibility.
- **AsPredicted:** Use for simple designs requiring fast registration. The structured 9-question format enforces brevity and is completable in under an hour. Registrations are private until the authors choose to make them public. Best for straightforward experiments with few analytical degrees of freedom.
- **Registered Reports:** A distinct format where the journal peer-reviews the introduction and methods before data collection. Acceptance is contingent on design quality, not results. Pursue registered reports when the research question is important but the expected results are uncertain or likely null -- this eliminates publication bias by design. Note that registered reports require substantially more lead time than standard pre-registration.

### 2. PAP Document Structure
- **Recommended Section Order:** Organize the PAP into: (1) study information (title, authors, timeline, registry), (2) theoretical motivation and hypotheses, (3) research design (experimental conditions, randomization, sample), (4) sampling and recruitment, (5) variable definitions and measurement, (6) analysis plan (models, tests, decision rules), and (7) contingency plans. This order mirrors the research process and makes the document navigable for reviewers.
- **Cross-Reference, Don't Repeat:** For hypothesis specification, reference the three-level specification framework (conceptual, operationalized, statistical) from the hypothesis-building skill. For reporting elements, reference the JARS six elements from the methods-reporting skill. The PAP should implement these frameworks, not redefine them.
- **Write for a Reader:** The PAP is a communication document, not a private notebook. Write as if an independent researcher will use it to replicate the study without contacting the authors. Avoid shorthand, undefined acronyms, and references to "the usual approach." Every analytical decision should be explicit.
- **Version Control:** Use the registry's built-in versioning. If amendments are needed after initial registration, create a new version rather than editing the original. Each version is timestamped, preserving the audit trail.

### 3. Specifying the Analytical Strategy
- **Three-Tier Classification:** Classify every planned analysis as locked (primary hypothesis tests -- cannot be changed), conditional (executed only if a pre-specified condition is met, e.g., "if the manipulation check passes, estimate the interaction model"), or exploratory (clearly labeled hypothesis-generating analyses with uncontrolled error rates). This framework generalizes the conjoint-specific version from conjoint-design to all experimental designs.
- **Decision Rules:** For each confirmatory hypothesis, state in advance what constitutes support, falsification, or an inconclusive result. Specify: the test statistic, the alpha level, the SESOI, and the decision mapping (e.g., "If p < 0.05 and the coefficient exceeds 3 percentage points in the predicted direction, the hypothesis is supported; if the equivalence test rejects effects larger than 3 percentage points, the hypothesis is falsified; otherwise, the result is inconclusive").
- **Exact Model Specifications:** Write out every primary model in formal notation or code. For regression models, specify: the dependent variable, all independent variables, interaction terms, fixed effects, clustering structure, and the estimator. Ambiguous prose descriptions ("we will control for demographics") are insufficient -- name every variable.
- **Multiple Testing Corrections:** Pre-specify the correction procedure and define which tests belong to the same family. For families of related tests (e.g., AMCEs across attributes within a single hypothesis), specify Benjamini-Hochberg (FDR control) or Bonferroni. Document the family groupings and the rationale for each.

### 4. Analysis Code Pre-Registration
- **Simulated Data Approach:** Generate a mock dataset that matches the expected data structure (variable names, types, distributions, sample size, missingness patterns). Write all analysis code -- data cleaning, primary models, robustness checks, planned figures -- to run on this simulated dataset. Register the code alongside the PAP (Lakens 2025).
- **Benefits:** Code pre-registration eliminates ambiguity about analytical decisions that prose alone cannot resolve (e.g., how exactly are covariates centered? What happens to observations with missing values on one covariate but not others?). It also catches specification errors before data collection -- if the code does not run on simulated data, it will not run on real data.
- **What to Include:** The registered code should cover: (1) data import and cleaning pipeline, (2) variable construction (indices, recodes, exclusion criteria), (3) primary confirmatory models, (4) conditional models with the triggering conditions, (5) planned figures with axis labels and titles, and (6) robustness checks. Exploratory code need not be pre-registered but should be documented post hoc.

### 5. Contingency Planning
- **Manipulation Check Failure:** If the manipulation check indicates that the treatment did not shift the intended construct, pre-specify the response: (a) report the ITT estimate regardless (it answers the policy-relevant question of what happens when the treatment is delivered), (b) investigate moderators of treatment uptake, and (c) do not selectively exclude non-compliers without a pre-specified rule.
- **Excessive Attrition:** Define an attrition threshold (e.g., >15% differential attrition across conditions) and the response if exceeded: (a) conduct attrition analysis (are attriters different from completers on observables?), (b) report Lee bounds on the treatment effect, (c) consider sensitivity analysis under alternative missing-data assumptions (MNAR models).
- **Covariate Imbalance:** Despite randomization, baseline imbalance may occur. Pre-specify: (a) which baseline variables will be checked, (b) the threshold for concern (e.g., a standardized difference > 0.10), and (c) the response (include the imbalanced covariate in the primary model as a robustness check, report both adjusted and unadjusted estimates).
- **Sample Size Shortfall:** If recruitment falls short of the target N, pre-specify: (a) the minimum N below which the study will not be analyzed (the threshold at which power drops below a defensible level), (b) a sensitivity analysis showing the MDE for the achieved N, and (c) whether the study will be reframed as exploratory if underpowered.
- **Decision Trees:** For complex contingencies, use explicit if-then decision trees: "If condition X holds, analyze using Model A; if condition X does not hold, analyze using Model B and report the deviation." This prevents post hoc rationalization of analytical choices.

### 6. Deviation Documentation
- **Four-Part Deviation Record:** Document every deviation from the registered plan with: (a) what changed (the specific analysis, variable, or procedure that differs from the PAP), (b) why it changed (the substantive or methodological reason), (c) the impact on severity (does the deviation make the test more or less capable of falsifying the hypothesis?), and (d) the impact on validity (does the deviation improve or degrade construct, internal, or external validity?) (Lakens 2025).
- **Principled vs. Convenience Deviations:** Distinguish between principled deviations (fixing a validity problem discovered after registration, e.g., a measure that does not function as intended) and convenience deviations (changing the analysis because the pre-registered approach yields unfavorable results). Principled deviations can strengthen a study; convenience deviations undermine credibility.
- **Side-by-Side Reporting:** When a deviation occurs, report both the pre-registered analysis and the deviated analysis. Readers can then assess whether the deviation affects the conclusions. Never replace the pre-registered analysis with the deviated one -- always present both.

### 7. Timeline and Logistics
- **When to Register:** Register after the design is finalized and the analysis code runs on simulated data, but before any data collection begins. For registered reports, submit for journal review before data collection. For standard pre-registration, the timestamp must precede the first survey response.
- **Embargo Options:** OSF allows registrations to be embargoed for up to 4 years (visible only to contributors until the embargo lifts). Use embargoes for competitive research where premature disclosure could enable scooping. EGAP registrations are public upon acceptance. AsPredicted registrations are private until authors choose to share.
- **Updating Registrations:** If the design changes after registration (e.g., after pilot results), create a new version or a new registration that references the original. Document what changed and why. Do not delete or overwrite the original registration.
- **IRB Coordination:** In many institutions, IRB approval is required before data collection but not before pre-registration. Register early, then amend the PAP if IRB review requires design changes. Include the IRB protocol number in the PAP once approved. Budget for the possibility that IRB review will take 4--8 weeks.
- **PAP-to-Paper Mapping:** After data collection and analysis, include a PAP concordance table in the paper's appendix: a two-column table mapping each PAP element to the corresponding section of the paper, with deviations flagged. This makes compliance auditable and signals transparency.

## Quality Checks
- [ ] **Registry Selected:** Is the registry platform chosen and justified (OSF, EGAP, AsPredicted, or registered report)?
- [ ] **Readable Structure:** Does the PAP follow a logical section order that an independent researcher could navigate?
- [ ] **Three-Tier Classification:** Is every planned analysis classified as locked, conditional, or exploratory?
- [ ] **Decision Rules:** Are support, falsification, and inconclusive criteria specified for each confirmatory hypothesis?
- [ ] **Exact Models:** Are all primary models written in formal notation or code, with every variable named?
- [ ] **Multiple Testing:** Is the correction procedure and family grouping pre-specified?
- [ ] **Code Registered:** Does analysis code run on a simulated dataset that matches the expected data structure?
- [ ] **Contingencies Specified:** Are contingency plans written for manipulation check failure, attrition, imbalance, and sample size shortfall?
- [ ] **Decision Trees:** Are complex contingencies expressed as explicit if-then decision trees?
- [ ] **Deviation Protocol:** Is the four-part deviation documentation framework (what, why, severity, validity) committed to?
- [ ] **Side-by-Side Commitment:** Does the PAP commit to reporting both pre-registered and deviated analyses when deviations occur?
- [ ] **Timeline:** Is the registration timestamped before data collection, with IRB coordination planned?
- [ ] **PAP Concordance:** Does the plan include a commitment to a PAP-to-paper concordance table?
