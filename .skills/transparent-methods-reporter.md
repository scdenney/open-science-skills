---
name: transparent-methods-reporter
description: Implements high-transparency reporting standards for experimental social science, including conjoint and factorial vignette designs. Ensures adherence to best methods section practices drawing on the **APSA Experimental Section** checklist.
---

# Transparent Methods Reporter

Use this skill to draft or audit the methodology section. It ensures the report provides sufficient information for a reader to follow the research steps and independently assess the validity of the conclusions.

## Instructions for the Agent

### 1. Subjects, Recruitment, and Setting
- **Eligibility:** Explicitly state who was eligible to participate and the criteria for subject selection.
- **Timeline:** Report the exact dates of the recruitment period and when the experiments were conducted, including any repeated measurements or follow-ups.
- **Provider Details:** For survey experiments, identify the survey firm used and describe their recruitment methods if they are not universally known.
- **Response Rates:** Provide the response rate and specify the exact formula used for its calculation.
- **Context:** Detail the specific setting (e.g., lab, field, classroom) and relevant geographic or institutional characteristics of the population.

### 2. Allocation and Treatment
- **Randomization Procedure:** State clearly if random assignment was used and describe the specific procedure (e.g., simple randomization, blocking, or restrictions).
- **Unit of Randomization:** Explicitly define the unit of randomization—whether individuals, households, groups, or clusters.
- **Baseline Balance:** Provide a table of baseline means and standard deviations for demographic characteristics and other pretreatment measures across all experimental groups to detect potential errors in assignment.
- **Intervention Detail:** Describe every treatment condition and the control condition in detail. This must include exact stimuli, scripts, images, or question wordings.
- **Material Availability:** Ensure complete treatment materials (vignettes, mailings, software programs) are provided in an appendix for replication.

### 3. Measurement and Sample Flow
- **Variable Definitions:** Provide precise definitions for how all primary outcomes, secondary outcomes, and covariates are measured and coded.
- **Index Construction:** If an index is used, explain exactly how it was constructed.
- **CONSORT Flow:** Document the sample at every stage:
    - The number initially assessed for eligibility.
    - Any exclusions prior to random assignment and the specific reasons for them.
    - The number of subjects assigned to each experimental group.
    - The proportion of each group that actually received the intended intervention and reasons for non-receipt.
- **Attrition and Missing Data:** Report the number of subjects in each group who dropped out or lack outcome data. Examine whether this attrition is related to treatment assignment.
- **Analysis Sample:** State the number of subjects included in the final analysis for each group and provide a rationale for any cases deleted at this stage.

### 4. Statistical Analysis
- **Intent-to-Treat (ITT):** Prioritize ITT analysis by reporting sample means, standard deviations, and Ns for outcome variables for the entire collection of subjects assigned to a group, regardless of whether they received the treatment.
- **Clustering and Weights:** Note if the level of analysis differs from the level of randomization and describe any weighting procedures in detail.
- **AMCE Estimation:** For conjoint designs, specify: the estimator (LPM with respondent fixed effects is standard), clustering structure (SEs clustered at respondent level), and how marginal means are computed.
- **Interaction Specification:** If interaction models are pre-registered, report the exact interaction terms, the hypothesis each tests, and the visualization method (e.g., conditional marginal means plots).
- **Cross-Group Models:** If the design is fielded across multiple sites/countries, specify whether per-group models are estimated separately or pooled with group × attribute interactions.
- **Pre-Specified Figures:** List all planned figures with a brief description of what each shows and which hypothesis it tests.

### 5. Conjoint-Specific Reporting
This section applies when the experiment uses a conjoint or factorial vignette design.

- **Attribute Table:** Report a complete table listing all attributes, their levels, and the reference category for each. If levels are country-specific (localized), provide both the generic attribute definition and the country-specific operationalizations.
- **Randomization Constraints:** If any attributes are nested, linked, or restricted (not fully independently randomized), document: (a) which attributes are constrained, (b) the justification for the constraint, and (c) which attributes remain fully independent. This is critical because constrained randomization changes the interpretation of AMCEs.
- **Vignette Assembly:** If using factorial vignettes (paragraph-form rather than attribute tables), provide: (a) the template showing how attributes are assembled into a coherent vignette, (b) worked examples of assembled vignettes for multiple attribute combinations, and (c) all country-specific text for each attribute level.
- **Task Structure:** Report: the number of paired-choice tasks per respondent, whether tasks involve forced choice or rating or both, attribute order randomization method, and profile position randomization.
- **DV Specification:** Clearly distinguish primary and secondary dependent variables. State the exact question wording for each. If both forced choice and rating are used, specify which is primary (for AMCE estimation) and which is secondary (for robustness).
- **Post-Block Items:** Document any post-block measures (attribution items, manipulation checks) with exact wording and response options. Clearly label these as non-confirmatory if they are not primary outcomes.
- **Effective Sample Size:** Report the effective number of profile evaluations (Respondents × Tasks × Profiles per task) and the number of observations per cell in the attribute space.

## Mandatory 28-Item Checklist
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
- [ ] 20. Complete attribute table with all levels and reference categories provided?
- [ ] 21. Any randomization constraints (nesting, linking, restrictions) documented and justified?
- [ ] 22. Vignette assembly template and worked examples included (if factorial vignette)?
- [ ] 23. Number of tasks, choice format, and randomization method reported?
- [ ] 24. Primary and secondary DVs clearly distinguished with exact question wording?
- [ ] 25. Post-block items (attribution, manipulation checks) documented with exact wording?
- [ ] 26. Effective sample size (profile evaluations) and per-cell Ns reported?
- [ ] 27. AMCE estimation method, clustering, and marginal means computation specified?
- [ ] 28. All pre-registered interaction models and planned figures listed?
