---
name: cross-national-comparative-designer
description: Guides the design of cross-national comparative survey experiments. Focuses on theoretically motivated case selection, instrument localization, ecological validity, and cross-national analytical strategies.
---

# Cross-National Comparative Designer

Use this skill when designing a survey experiment that will be fielded in multiple countries. It ensures that case selection is theoretically motivated, that experimental materials are properly localized, and that the analytical strategy handles cross-national comparison rigorously.

## Instructions for the Agent

### 1. Case Selection and Theoretical Justification
- **Variation by Design:** Cases should be selected to vary on theoretically relevant dimensions (e.g., regime type, institutional structure, immigration history, partisan polarization), not for convenience or data availability. Each case should serve a specific theoretical function.
- **Case Selection Table:** Produce a summary table listing each country, its relevant contextual features (e.g., immigration salience, institutional architecture, regime type), and the specific motivation for its inclusion. This table belongs in the PAP and should be referenced in the narrative.
- **Avoid the "Most Similar" Trap:** Cross-national designs are often most informative when cases are deliberately diverse. Including cases that vary on regime type (e.g., democracy vs. hybrid regime) or institutional structure (e.g., parliamentary vs. presidential) enables stronger tests of whether a theoretical mechanism generalizes beyond a single political context.
- **The N=4 Sweet Spot:** For survey experiments with ~2,500 respondents per country, 3--5 cases typically balance theoretical leverage with practical feasibility (budget, translation, vendor logistics). Fewer than 3 limits comparison; more than 5 strains resources without proportional analytical gain.

### 2. Instrument Localization
- **Conceptual Equivalence over Literal Translation:** The goal is not identical wording across countries but equivalent conceptual meaning. A "skilled worker visa" means H-1B in the US, E-7 in South Korea, S Pass in Singapore. Use country-specific referents that carry the same conceptual weight.
- **Institutional Referents:** Localize all political actors (president, cabinet, ministry), legislative bodies (Congress, Bundestag, National Assembly, Parliament), international organizations (UN, EU, OECD, ASEAN), and policy instruments (visa types, permit categories). Document all localizations in a country-specific table.
- **Cultural Calibration of Stimuli:** For attributes like "country of origin" that signal cultural proximity or distance, the specific countries must be calibrated per respondent country. "Culturally distant" means different things in the US (e.g., Somalia) than in South Korea (e.g., Yemen) or Singapore (e.g., Afghanistan). Document the calibration rationale.
- **Ecological Validity Check:** Every experimental stimulus should be plausible in the respondent's national context. A vignette about EU directives makes sense for German respondents but not Singaporean ones. Test each localized version against the question: "Would a newspaper in this country plausibly report this?"

### 3. Composition and Origin Country Selection
- **Origin Countries as Group Cues:** When immigrant origin countries are used as experimental stimuli (common in immigration conjoint studies), select origins that: (a) are recognizable to respondents, (b) vary on the intended dimension (e.g., cultural proximity), and (c) do not carry overwhelming confounding associations (e.g., ongoing war, recent political crisis) unless those associations are part of the theoretical design.
- **Nesting Origins within Domains:** If the experiment crosses policy domain (e.g., labor vs. asylum) with immigrant composition, it may be necessary to use different origin countries for different domains within the same respondent country. This preserves ecological validity (asylum seekers plausibly come from different countries than labor migrants) but means the composition attribute cannot be cleanly separated from domain. Document this nesting and acknowledge it in the analysis.
- **Avoiding Origin Overlap:** Within a single respondent country, avoid reusing the same origin country across different experimental roles (e.g., using Nigeria as both the "distant" labor origin and the "distant" asylum origin). This prevents respondents from noticing repeated countries and developing response patterns.

### 4. Cross-National Analytical Strategy
- **Per-Country Estimation First:** Always estimate the primary model separately for each country before pooling. This respects the possibility that the data-generating process differs across contexts and provides country-specific effect sizes that are interpretable on their own.
- **Pooled Models with Country Interactions:** For formal tests of cross-national heterogeneity, estimate a pooled model that includes attribute $\times$ country interaction terms. Wald tests on the interaction coefficients provide a statistical test of whether effect sizes differ across countries. Note that respondent fixed effects absorb country main effects when country is a respondent-level constant.
- **Scope Conditions, Not Country Hypotheses:** When the theory predicts that effect magnitudes will vary by institutional context but does not make precise predictions about which country will show the largest effect, frame country-specific expectations as "contextual expectations and scope conditions" rather than confirmatory hypotheses. This avoids the proliferation of underpowered country-level tests while preserving theoretical nuance.
- **Visualization:** Present cross-national results as side-by-side AMCE panels (one per country) or forest plots. These enable visual comparison of effect magnitudes and patterns, which is often more informative than formal statistical tests of heterogeneity.

### 5. Practical Considerations
- **Survey Vendors:** Cross-national online surveys typically require country-specific vendors or an international panel provider. Verify that quota-matching (age, gender, education, region) is available in all target countries.
- **Translation Protocol:** Use professional translation with back-translation verification. For experimental stimuli, the back-translation should be evaluated by a bilingual researcher who understands the experimental design, not just the language.
- **Ethical Approvals:** Some countries or institutions require separate ethics review. Plan for varying timelines and requirements across sites.
- **Pre-Registration:** Pre-register at the study level (not per-country). The pre-analysis plan should include both the pooled analytical strategy and the per-country estimation plan.

## Quality Checks
- [ ] **Case Justification:** Is each country's inclusion theoretically motivated and documented in a case selection table?
- [ ] **Localization Documented:** Are all country-specific referents (actors, institutions, visa types, origin countries) listed in a localization table?
- [ ] **Conceptual Equivalence:** Do localized stimuli carry equivalent conceptual meaning across countries, even if wording differs?
- [ ] **Ecological Validity:** Is every stimulus plausible in each national context?
- [ ] **Origin Calibration:** Are origin countries calibrated for cultural proximity/distance per respondent country, with rationale documented?
- [ ] **No Origin Overlap:** Within each respondent country, is each origin country used in only one experimental role?
- [ ] **Per-Country Models:** Does the analysis plan include per-country estimation before pooling?
- [ ] **Scope Conditions:** Are cross-national expectations framed as scope conditions rather than confirmatory hypotheses (unless the theory makes precise directional predictions)?
- [ ] **Translation:** Is a professional translation and back-translation protocol specified?
