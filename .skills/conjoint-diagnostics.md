---
name: conjoint-diagnostics
description: Systematic diagnostic checklist for evaluating choice-based conjoint experiments. Use when (1) reviewing a conjoint paper or manuscript, (2) auditing a conjoint analysis script or dataset, (3) assessing measurement error and IRR in conjoint data, (4) evaluating external validity of a conjoint design, or (5) checking interpretation of AMCEs, marginal means, and interaction effects. Covers design, estimation, measurement error correction, external validity, and reporting.
---

# Conjoint Experiment Diagnostics

## Instructions

Work through each section below for the conjoint study under review. Assess whether the study addresses each item adequately, partially, or not at all. Flag items that pose threats to inference and prioritize recommendations by severity.

If provided with R scripts or data, inspect the actual implementation, not just what the paper claims. Check for discrepancies between described and implemented methods.

---

## 1. Design Diagnostics

### 1.1 Attribute and Level Selection
- Are attributes conceptually distinct and non-overlapping?
- Are levels realistic and mutually exclusive within each attribute?
- Is the number of attributes justified? (Bansak et al. 2021 PSRM: attributes can scale with modest satisficing, but each additional attribute adds cognitive load)
- Are there "dominant" attributes that might crowd out attention to others?
- Do the attribute levels span a meaningful range of the construct of interest?

### 1.2 Profile Restrictions
- Are implausible or contradictory attribute combinations allowed?
- If restrictions are imposed, are they documented and justified?
- If no restrictions, does the paper acknowledge potential odd profiles? (Bansak & Jenke 2025: odd profiles have minimal impact on first-order inferences, but should be acknowledged)

### 1.3 Number of Tasks and Satisficing
- How many tasks per respondent? (Bansak et al. 2018: up to 30 tasks with limited satisficing)
- Are attention checks embedded?
- Is there evidence of survey fatigue or satisficing in later tasks? (e.g., declining response time, increased randomness)

### 1.4 Randomization
- Is attribute-level assignment fully randomized (uniform distribution)?
- If non-uniform, is this justified and documented?
- Are profile-pair attributes independent or dependent? (Clayton et al. 2023 distinguish independent, dependent, and pair-level attributes)

### 1.5 Sample and Power
- Is the sample size justified with a power analysis? (Schuessler & Freitag 2020 cjpowR; Stefanelli & Lukac 2020)
- What is the effective sample size (N respondents x T tasks)?
- Are Type S (sign) and Type M (magnitude/exaggeration) errors considered?
- For subgroup analyses, is there adequate power within each subgroup?

---

## 2. Estimation Diagnostics

### 2.1 Estimand Clarity
- Verify the estimand is clearly defined (AMCE, MM, AMIE, or pAMCE) and the choice is justified.
- Check whether AMCEs are interpreted with awareness that they depend on the attribute distribution used for averaging (Hainmueller et al. 2014).
- Check whether MMs are used where reference-category-free comparisons are needed (Leeper et al. 2020).

### 2.2 Reference Levels
- Are reference levels clearly specified and substantively meaningful?
- Are AMCEs interpreted relative to the correct reference category?
- For subgroup comparisons, is the reference category consistent across groups? (Leeper et al. 2020: conditional AMCEs are sensitive to reference choice)

### 2.3 Subgroup Analysis
- Are subgroups defined by pre-treatment characteristics (not post-treatment)?
- **Use marginal means and diff-in-MMs for subgroup comparisons**, not conditional AMCEs. (Leeper, Hobolt & Tilley 2020: conditional AMCEs are reference-category dependent and can yield arbitrary subgroup differences)
- Are diff-in-MMs presented alongside MMs for interpretability?
- Is heterogeneity detection systematic or ad hoc? (Robinson & Duch 2024 cjbart; Goplerud et al. 2025 FactorHet)

### 2.4 Standard Errors and Clustering
- Are standard errors clustered at the respondent level? (Required when T > 1 tasks per respondent)
- Is the clustering variable correctly specified?
- Are confidence intervals reported? At what level? (Convention: 95%, some papers use 90% or dual CI bars)

### 2.5 Multiple Testing
- How many AMCEs/MMs are estimated in total?
- Is there a correction for multiple comparisons? (Liu & Shiraito 2023: >90% chance of at least one spurious significant AMCE with no correction when no true effects exist)
- If no correction, is this limitation acknowledged?
- Consider: Bonferroni (conservative), Benjamini-Hochberg (FDR), adaptive shrinkage (recommended as default when limited prior knowledge)

---

## 3. Measurement Error Diagnostics (Clayton et al. 2023)

This is a critical and often-overlooked diagnostic. Conjoint experiments produce substantial measurement error due to the inherent complexity of multi-attribute trade-offs.

### 3.1 Understanding the Problem
- Conjoint responses have **swapping error**: respondents sometimes select the opposite of their true preference. This is NOT classical measurement error.
- For binary outcomes, swapping error biases both MMs (toward 0.5) and AMCEs (toward 0).
- Intra-Respondent Reliability (IRR) in conjoint experiments averages ~75% (range 73-81% across eight replicated studies). This means ~15% of responses are effectively random noise.
- IRR does NOT vary systematically with attribute combinations but DOES vary with respondent characteristics (younger, male, non-white respondents tend to have lower reliability).
- For subgroup comparisons, bias can attenuate, exaggerate, or flip the sign of differences.

### 3.2 Does the Study Estimate IRR?
Four methods, in order of ease:
1. **Borrow from similar studies**: Use IRR ≈ 0.75 from Clayton et al.'s replications of similar conjoint studies. Justify the chosen value.
2. **Extrapolate from existing data**: Use within-respondent task-pair agreement as a function of attribute-level differences, extrapolating to zero differences (no repeated tasks needed).
3. **Repeat-task design** (recommended for new studies): Repeat the first conjoint task at the end of the survey (with left/right profiles flipped). IRR = proportion agreement.
4. **Full attribute-specific IRR**: Estimate IRR for each attribute value separately (most intensive).

### 3.3 Does the Study Apply Bias Correction?
- Corrected MM: ρ̃(a) = (ρ̂(a) − τ) / (1 − 2τ)
- Corrected AMCE: θ̃(a, a') = θ̂(a, a') / (1 − 2τ)
- Where τ is the swapping error probability, estimated from IRR via: τ̂ = (1 − √(1 − 2(1 − IRR))) / 2
- The correction ALWAYS increases absolute value of AMCEs and distance of MMs from 0.5.
- For subgroup differences, the correction can increase (~82%), decrease (~12%), or flip sign (~5%).
- Software: `projoint` R package (Clayton et al.)

### 3.4 If No Correction, What Is the Risk?
- Sensitivity analysis: Report results for a range of plausible IRR values (e.g., 0.70, 0.75, 0.80)
- At minimum, acknowledge measurement error as a limitation
- For subgroup analyses, this concern is especially acute since bias direction is unpredictable

---

## 4. External Validity Diagnostics

### 4.1 Profile Distribution
- Does the uniform attribute distribution match real-world frequencies? (de la Cuesta et al. 2022)
- If not, does the paper discuss how this affects interpretation?
- Are pAMCEs computed for comparison?

### 4.2 Forced Choice vs. Real-World Behavior
- Does the forced-choice format accurately reflect the decision context? (Visconti & Yang 2024)
- Should an abstention/neither option be offered? (Miller & Ziegler 2024: preferential abstention can produce different-sign AMCEs)
- Is there a rating outcome alongside forced choice? (Treger 2025: forced-choice and rating elicit distinct preferences)

### 4.3 Attention and Salience
- Does the conjoint format artificially inflate attention to attributes that respondents would ignore in real decisions? (Fu & Li 2024)
- Could this lead to effect magnitude amplification, sign reversal, or importance reversal?

---

## 5. Interpretation Diagnostics

### 5.1 AMCE Interpretation
- Does the paper correctly interpret AMCEs as average effects on choice probability, not majority preferences? (Abramson et al. 2022)
- Does the paper acknowledge that AMCEs depend on the distribution of other attributes? (Bansak et al. 2023 respond that AMCEs map to vote share changes)
- Are AMCEs interpreted as causal effects or merely as preference rankings?

### 5.2 Magnitude Reporting
- Are effect sizes reported in interpretable units (percentage points)?
- Are substantive significance thresholds discussed alongside statistical significance?
- Is there comparison to benchmark effect sizes in similar studies?

### 5.3 Interaction Effects
- If interactions are examined, are AMIEs used rather than conditional AMCEs? (Egami & Imai 2019)
- Is there a test for whether a factor matters at all? (Ham et al. 2024 CRTConjoint: conditional randomization test)

---

## 6. Reporting Checklist

A well-reported conjoint study should include:

- [ ] Clear statement of the estimand (AMCE, MM, or both)
- [ ] Reference levels for all attributes
- [ ] Number of respondents, tasks per respondent, and effective sample size
- [ ] Attention check protocol and pass rates
- [ ] Randomization procedure (uniform or weighted)
- [ ] Any profile restrictions and justification
- [ ] Clustering specification for standard errors
- [ ] Confidence interval level(s) reported
- [ ] Discussion of measurement error / IRR (Clayton et al. 2023)
- [ ] Multiple testing approach or acknowledgment of concern (Liu & Shiraito 2023)
- [ ] Pre-registration status and any deviations
- [ ] Software and packages used for estimation

