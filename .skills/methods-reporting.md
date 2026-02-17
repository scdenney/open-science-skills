---
name: methods-reporting
description: Implements high-transparency reporting standards for experimental social science, including conjoint and factorial vignette designs. Ensures adherence to best methods section practices drawing on the **APSA Experimental Section** checklist, the **JARS** preregistration standards, and the **DA-RT** transparency principles.
---

# Transparent Methods Reporter

Use this skill to draft or audit the methodology section. It ensures the report provides sufficient information for a reader to follow the research steps and independently assess the validity of the conclusions. Reporting standards should be consulted *at the design stage*, not as an afterthought when writing up -- they structure both the presentation of data and the design of studies (Christensen, Freese, and Miguel 2019).

## Instructions for the Agent

### 1. Design Documentation and Pre-Registration
This section covers upstream documentation that makes transparent reporting possible. A well-documented bad design is still a bad design; transparency tools are necessary but not sufficient (Druckman 2022).

- **Design Document:** Before data collection, create a comprehensive document recording all decisions and their rationale -- motivation, stimuli, outcome measures, predictions, analysis plans, and logistics. This "design document" is the upstream practice that enables downstream transparent reporting (Druckman 2022, Ch. 5).
- **Pre-Registration vs. Pre-Analysis Plan:** Distinguish between *study registration* (basic: recording the study's existence, hypotheses, and population in a public repository) and a *pre-analysis plan* (detailed: specifying exact statistical tests, evidence thresholds, and contingency plans). Require the latter for confirmatory experiments. Name the repository used (OSF, EGAP, or AsPredicted) and provide the registration ID.
- **JARS Six Elements:** For preregistered experiments, ensure the following six elements are specified (Lakens 2025, citing Journal Article Reporting Standards): (1) randomization procedure, (2) inclusion/exclusion criteria, (3) sampling procedures and expected participation rate, (4) sample size justification with power analysis or precision rationale, (5) data diagnostics (exclusion criteria, missing data handling, outlier definitions, assumption checks), and (6) analytic strategy organized into primary, secondary, and exploratory tiers.
- **Analysis Code:** The gold standard is to preregister analysis code that runs on a simulated dataset, eliminating ambiguity about all analytical decisions (Lakens 2025). For conjoint analyses, provide the regression specification in code form (e.g., R `lm()` or `feols()` call).
- **Pilot Documentation:** Document all pilot studies, including not just manipulation check results but also response rate data, recruitment language testing, and any modifications made as a result (Druckman 2022, Ch. 5). For conjoints, pilot whether respondents attend to all attributes, find combinations plausible, and process the display as intended.

### 2. Subjects, Recruitment, and Setting
- **Eligibility:** Explicitly state who was eligible to participate and the criteria for subject selection.
- **Target Population:** State the target population to which inference is intended. This includes the units, contexts, measures, and outcomes (Druckman 2022, Ch. 6). Distinguish between the sampling frame (who could be reached) and the target population (who the theory applies to).
- **Timeline:** Report the exact dates of the recruitment period and when the experiments were conducted, including any repeated measurements or follow-ups. For "firehouse studies" conducted in response to real-world events, document the lag between the event and data collection (Mutz 2011).
- **Provider Details:** For survey experiments, identify the survey firm used and describe their recruitment methods if they are not universally known. Note whether the sample is probability-based or nonprobability (quota-matched online panel) and the implications for generalizability.
- **Response Rates:** Provide the response rate and specify the exact formula used for its calculation.
- **Survey Error Pipeline:** Report how each of three sequential error sources was addressed: (1) *coverage error* (does the sampling frame reach the target population?), (2) *sampling error* (does the sample represent the frame?), and (3) *nonresponse error* (do respondents differ from non-respondents?) (Stantcheva 2023).
- **Benchmark Validation:** Compare sample demographics and key attitude measures to those from existing high-quality, representative surveys that serve as benchmarks for the target population (Stantcheva 2023).
- **Context:** Detail the specific setting (e.g., lab, field, online panel) and relevant geographic or institutional characteristics of the population.
- **Incentives:** Describe the form and amount of any incentives provided to participants (Gerber et al. 2014).

### 3. Allocation and Treatment
- **Randomization Procedure:** State clearly if random assignment was used and describe the specific procedure (e.g., simple randomization, blocking, stratification, or restrictions). Identify the software or tool used for randomization (Gerber et al. 2014).
- **Unit of Randomization:** Explicitly define the unit of randomization -- whether individuals, households, groups, or clusters.
- **Assignment Sequence:** Provide details on the exact randomization sequence: who generated it, when it was generated, and whether it was concealed from researchers during enrollment (Gerber et al. 2014).
- **Blinding:** Report whether single-blinding (subjects unaware of condition), double-blinding (subjects and analysts unaware), or no blinding was used (Gerber et al. 2014).
- **Baseline Balance:** Provide a table of baseline means and standard deviations for demographic characteristics and other pretreatment measures across all experimental groups to detect potential errors in assignment.
- **Intervention Detail:** Describe every treatment condition and the control condition in detail. This must include exact stimuli, scripts, images, or question wordings. Specify the mode of delivery (e.g., text, audio, video, in-person) (Gerber et al. 2014).
- **Material Availability:** Ensure complete treatment materials (vignettes, mailings, software programs) are provided in an appendix for replication. Material availability is not just a reporting requirement; it is infrastructure for cumulative science (Druckman 2022).
- **Manipulation Checks:** If manipulation checks are used, report their exact wording, placement in the survey flow, and results. Do not selectively exclude respondents who "fail" manipulation checks without pre-specifying this exclusion rule and reporting results both with and without exclusions (Druckman 2022). Place comprehension checks at the end of the survey or after outcome elicitation to avoid signaling the study's purpose (Stantcheva 2023).
- **Question Wording Standards:** Use item-specific scales rather than agree-disagree, true-false, or yes-no formats to reduce acquiescence bias. Randomize response option order for nominal items; invert order for ordinal items. Separate question stems from response alternatives with a semantic pause for forced-choice items (Stantcheva 2023).
- **Soft Launch:** Before full deployment, run a small-scale "soft launch" of the complete survey to check for technical issues in the survey flow (loading, display, branching logic), separate from content pretesting. Document any issues discovered and modifications made (Stantcheva 2023).

### 4. Measurement and Sample Flow
- **Variable Definitions:** Provide precise definitions for how all primary outcomes, secondary outcomes, and covariates are measured and coded.
- **Index Construction:** If an index is used, explain exactly how it was constructed.
- **CONSORT Flow:** Document the sample at every stage:
    - The number initially assessed for eligibility.
    - Any exclusions prior to random assignment and the specific reasons for them.
    - The number of subjects assigned to each experimental group.
    - The proportion of each group that actually received the intended intervention and reasons for non-receipt.
- **Attrition and Missing Data:** Report the number of subjects in each group who dropped out or lack outcome data. Examine whether this attrition is related to treatment assignment. Report missing data handling procedures (listwise deletion, imputation, or other methods) and justify the choice (Lakens 2025, citing Wicherts et al. 2016).
- **Outlier Procedures:** If outliers are excluded or winsorized, state the definition used and report results both with and without outlier treatment.
- **Analysis Sample:** State the number of subjects included in the final analysis for each group and provide a rationale for any cases deleted at this stage.

### 5. Statistical Analysis
- **Sample Size Justification:** Report the type of sample size justification used. Lakens (2025) identifies six types: (1) measure the entire population, (2) resource constraints, (3) accuracy (confidence interval width), (4) a priori power analysis, (5) heuristics, or (6) no justification. For a priori power analyses, report: the test used, the assumed effect size and its source, alpha, power, and the resulting N. For resource-constrained designs, conduct a sensitivity analysis reporting the minimum detectable effect given the available N.
- **Raw Results First:** Always report unadjusted (raw) results alongside any corrected or reweighted results, either as the primary presentation or in an appendix. This allows readers to assess the impact of any statistical adjustments (Stantcheva 2023).
- **Intent-to-Treat (ITT):** Prioritize ITT analysis by reporting sample means, standard deviations, and Ns for outcome variables for the entire collection of subjects assigned to a group, regardless of whether they received the treatment.
- **Clustering and Weights:** Note if the level of analysis differs from the level of randomization and describe any weighting procedures in detail.
- **Three-Tier Results Labeling:** Label every reported result as *primary* (Type I and Type II error rates controlled), *secondary* (Type I controlled, Type II not), or *exploratory* (error rates uncontrolled). Exploratory results must be "clearly labeled, justified, methodologically sound, and informative" (Lakens 2025; Druckman 2022, citing JEPS review criteria).
- **Equivalence Test Reporting:** When reporting equivalence tests (TOST procedure), report: the equivalence bounds in raw effect size units (not Cohen's d), the higher p-value of the two one-sided tests, and the 90% confidence interval (not 95%, because TOST uses two one-sided tests at alpha = 0.05). Never claim "no effect" -- instead state that effects more extreme than the equivalence bounds were rejected (Lakens 2025).
- **AMCE Estimation:** For conjoint designs, specify: the estimator (LPM with respondent fixed effects is standard), clustering structure (SEs clustered at respondent level), and how marginal means are computed.
- **Interaction Specification:** If interaction models are pre-registered, report the exact interaction terms, the hypothesis each tests, and the visualization method (e.g., conditional marginal means plots).
- **Cross-Group Models:** If the design is fielded across multiple sites/countries, specify whether per-group models are estimated separately or pooled with group × attribute interactions.
- **Pre-Specified Figures:** List all planned figures with a brief description of what each shows and which hypothesis it tests.
- **Sensitivity and Robustness:** Beyond secondary DV replication, specify planned robustness checks: specification curves, alternative exclusion criteria, alternative model specifications. This addresses the "garden of forking paths" concern -- the risk that researchers unconsciously make particular analytic decisions that lead to outcomes that may not occur under other reasonable decisions (Gelman and Loken 2014, cited in Druckman 2022).

### 6. Conjoint-Specific Reporting
This section applies when the experiment uses a conjoint or factorial vignette design.

- **Attribute Table:** Report a complete table listing all attributes, their levels, and the reference category for each. If levels are country-specific (localized), provide both the generic attribute definition and the country-specific operationalizations.
- **Randomization Constraints:** If any attributes are nested, linked, or restricted (not fully independently randomized), document: (a) which attributes are constrained, (b) the justification for the constraint, and (c) which attributes remain fully independent. This is critical because constrained randomization changes the interpretation of AMCEs.
- **Vignette Assembly:** If using factorial vignettes (paragraph-form rather than attribute tables), provide: (a) the template showing how attributes are assembled into a coherent vignette, (b) worked examples of assembled vignettes for multiple attribute combinations, and (c) all country-specific text for each attribute level.
- **Task Structure:** Report: the number of paired-choice tasks per respondent, whether tasks involve forced choice or rating or both, attribute order randomization method, and profile position randomization.
- **DV Specification:** Clearly distinguish primary and secondary dependent variables. State the exact question wording for each. If both forced choice and rating are used, specify which is primary (for AMCE estimation) and which is secondary (for robustness).
- **Post-Block Items:** Document any post-block measures (attribution items, manipulation checks) with exact wording and response options. Clearly label these as non-confirmatory if they are not primary outcomes.
- **Effective Sample Size:** Report the effective number of profile evaluations (Respondents × Tasks × Profiles per task) and the number of observations per cell in the attribute space.

### 7. Validity Framework
- **Four Validity Types:** Evaluate the design against Druckman's (2022) four validity types: (1) *construct validity* (do measures capture the intended concepts?), (2) *statistical conclusion validity* (are the statistical inferences correct?), (3) *internal validity* (is the causal claim warranted?), and (4) *external validity* (does the finding generalize?). Random assignment provides internal validity; representative sampling provides generalizability -- these are independent contributions (Mutz 2011).
- **Deviation Reporting:** When deviating from a preregistered plan, document: (a) what changed, (b) why, (c) the impact on *severity* (does the deviation make the test more or less capable of falsifying the hypothesis?), and (d) the impact on *validity* (does the deviation improve or degrade the design's ability to measure what it claims?). Not all deviations reduce quality -- fixing a validity problem can *increase* test severity (Lakens 2025).
- **Design Improvement Framing:** If the design was revised in response to peer or workshop feedback, frame the improvement as a theoretical advance rather than a correction. For example: "The redesigned experiment enables a direct test of whether [mechanism] withstands [alternative explanation]" (see narrative-building skill).

### 8. Open Science Infrastructure
- **DA-RT Three Pillars:** Adhere to the Data Access and Research Transparency principles: (1) *data access* -- share replication data, (2) *production transparency* -- document how data were generated, and (3) *analytic transparency* -- provide complete analysis code (APSA Guide to Professional Ethics, cited in Druckman 2022).
- **Data Sharing Plan:** Specify what data will be shared, in what format, with what documentation, and on what platform. For cross-national studies, address varying privacy regimes across national contexts (Christensen et al. 2019).
- **Reproducible Workflow:** Provide version-controlled analysis code that reproduces all results from raw data to published figures. The path from raw data to published results should be fully documented and executable, not just described in prose (Christensen et al. 2019).
- **During-Collection Documentation:** Maintain session logs, variable creation decisions, case selection decisions, and analytic code version control throughout data collection -- not only after (Druckman 2022, Ch. 5).
- **IRB and Ethics:** Report IRB approval details. For audit studies or studies involving deception, note the specific ethical provisions. Begin the IRB process early -- it can take weeks or months (Druckman 2022).

## Mandatory Checklist

### Core Reporting (Items 1--19)
- [ ] 1. Eligibility criteria for participants reported?
- [ ] 2. Specific recruitment and conduct dates (including follow-ups) provided?
- [ ] 3. Survey firm identified and recruitment methods described?
- [ ] 4. Response rate and calculation method reported?
- [ ] 5. Use of random assignment explicitly stated?
- [ ] 6. Unit of randomization (individual, group, cluster) identified?
- [ ] 7. Table of baseline means and SDs by experimental group provided?
- [ ] 8. Detailed description of all treatment and control conditions included?
- [ ] 9. Complete treatment materials (scripts, images, etc.) made available?
- [ ] 10. Outcome variable measurement and coding defined?
- [ ] 11. Exact construction of any indices explained?
- [ ] 12. Measurement and coding of all covariates/model variables reported?
- [ ] 13. Number of subjects initially assessed for eligibility reported?
- [ ] 14. Exclusions prior to randomization and reasons provided?
- [ ] 15. Number of subjects assigned to each experimental group stated?
- [ ] 16. Proportion receiving the intervention and reasons for non-receipt reported?
- [ ] 17. Number of subjects per group lacking outcome data reported?
- [ ] 18. Number included in analysis and rationale for exclusions provided?
- [ ] 19. Outcome means/SDs/Ns reported using Intent-to-Treat (ITT) analysis?

### Conjoint-Specific Reporting (Items 20--28)
- [ ] 20. Complete attribute table with all levels and reference categories provided?
- [ ] 21. Any randomization constraints (nesting, linking, restrictions) documented and justified?
- [ ] 22. Vignette assembly template and worked examples included (if factorial vignette)?
- [ ] 23. Number of tasks, choice format, and randomization method reported?
- [ ] 24. Primary and secondary DVs clearly distinguished with exact question wording?
- [ ] 25. Post-block items (attribution, manipulation checks) documented with exact wording?
- [ ] 26. Effective sample size (profile evaluations) and per-cell Ns reported?
- [ ] 27. AMCE estimation method, clustering, and marginal means computation specified?
- [ ] 28. All pre-registered interaction models and planned figures listed?

### Design Transparency (Items 29--40)
- [ ] 29. Hypotheses stated prior to research design, not post hoc (Gerber et al. 2014)?
- [ ] 30. Subject incentives described (Gerber et al. 2014)?
- [ ] 31. Blinding status (single, double, or none) reported (Gerber et al. 2014)?
- [ ] 32. Mode of treatment delivery (text, audio, video, in-person) described (Gerber et al. 2014)?
- [ ] 33. Randomization software/tool and assignment sequence details provided (Gerber et al. 2014)?
- [ ] 34. Manipulation checks documented with placement, wording, and results (Druckman 2022)?
- [ ] 35. Sample size justification type identified and reported (Lakens 2025)?
- [ ] 36. SESOI specified and justified for all hypothesis tests, or rationale given for its absence (Lakens 2025)?
- [ ] 37. Pre-registration ID and repository stated (Druckman 2022)?
- [ ] 38. Deviations from pre-analysis plan documented with severity and validity impact (Lakens 2025)?
- [ ] 39. Results labeled as primary, secondary, or exploratory (Lakens 2025; JARS)?
- [ ] 40. Data sharing plan, reproducible analysis code, and open materials platform specified (Christensen et al. 2019)?

### Survey Design Quality (Items 41--45, Stantcheva 2023)
- [ ] 41. Was a soft-launch conducted before full deployment, with technical issues documented?
- [ ] 42. Are raw (unadjusted) results reported alongside any corrected/reweighted results?
- [ ] 43. Are benchmark comparisons to existing representative surveys reported to validate sample quality?
- [ ] 44. Have question wording best practices been followed (item-specific scales, no agree-disagree, randomized option order)?
- [ ] 45. Is the three-stage survey error pipeline (coverage, sampling, nonresponse) addressed?
