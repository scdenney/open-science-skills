---
disable-model-invocation: true
name: tables
description: Designs publication tables for social-science manuscripts. Covers whether a result belongs in a table at all, column order, row grouping and panels, decimal precision, standard-error and confidence-interval conventions, self-contained titles and notes, and code-generated output. Use when building or revising a regression, balance, descriptive, or robustness table, or when working with modelsummary, stargazer, gt, esttab, or booktabs. Finished tables go to figure-table-audit for end-stage QA.
argument-hint: '[describe the table you are building, the model or data, the claim it supports, and the target venue]'
---

# Table Designer

Applies to descriptive, regression, balance, and summary tables under any method. For tables whose interpretation depends on method-specific standards, also consult the relevant sibling skill (`conjoint-design`, `conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr`). For end-stage QA on a finished table set, hand off to `figure-table-audit`.

Tables are for precise reading. A table is the right shape when the relevant comparison can be made without arithmetic and every number quoted in the text traces to a specific cell. If readers must subtract to recover the substantive quantity, reshape the table.

## Instructions

### 1. Decide whether the result belongs in a table at all

Tables are for reading values; figures are for seeing patterns. Use a table when:

- Readers need exact values (descriptive statistics for a sample, balance check, key effect sizes for citation).
- The comparison spans many models or specifications and a coefficient plot would be too dense.
- Regulatory or replication norms require it (CONSORT flow numbers, baseline balance).

Use a figure when the substantive claim is a *pattern* — a slope, a non-monotonicity, a difference of differences. Many regression tables in social science would be more readable as coefficient plots with a small accompanying summary table.

### 2. State the comparison and the estimand before laying out the table

Write down, in one sentence, what the table is supposed to let the reader compare. The first column or first panel should anchor that comparison. Examples:

- "Effect of treatment on turnout, baseline → with covariates → with fixed effects → preferred specification."
- "Sample means by treatment arm, with balance test."
- "AMCEs by attribute, pooled and split by partisanship."

If the comparison is not clear, the table will read as a coefficient dump.

### 3. Choose column order to match the argument

Columns should mirror how the text walks the reader through the result:

- **Regression tables**: baseline / minimal-controls → preferred specification → robustness checks. Place the preferred model in a clearly labeled column, not necessarily the rightmost; readers focus on the column that the text says is preferred.
- **Comparison tables**: control / treatment 1 / treatment 2 / contrast(s), or pre / post / difference.
- **Descriptive tables**: full sample → analytic sample → by treatment arm; or order subgroups by substantive logic, not alphabetically.
- Pass models to `stargazer`/`modelsummary` in the order the manuscript discusses them rather than accepting the package's default order.

### 4. Group rows and structure panels

- Group covariate blocks: treatment(s) at the top, then primary moderators, then controls, then fixed-effect indicators, then fit statistics.
- Separate blocks with horizontal rules or panel breaks rather than letting regression output run as a flat list.
- Suppress controls in the main table when there are many — show "Controls: yes" and put the full coefficient set in SI.
- For multi-panel tables, use a clear panel header (e.g., "Panel A. Full sample / Panel B. Eligible voters only") and keep column structure identical across panels.
- Order rows within a block by substantive interest, not alphabetically — readers expect the headline coefficient first.

### 5. Pick precision and uncertainty conventions and stick to them

- Choose decimal precision based on the meaningful digit, not on what the software prints. Two decimals for proportions, three for small effects, integer counts for N.
- Be consistent across tables in the manuscript: same precision for the same quantity.
- Show uncertainty as standard errors `(in parentheses)` OR confidence intervals `[in brackets]` — pick one convention and use it everywhere. Note the convention in the table notes.
- Significance stars (`*`, `**`, `***`) are conventional but not required; if used, define thresholds in the notes consistently across tables.
- Report N per column and a fit statistic appropriate to the model (R² for OLS, pseudo-R² or log-likelihood for non-linear, ICC for multilevel).

### 6. Write self-contained titles and notes

A reader should be able to understand the table from title + notes alone. Title should name the **estimand** or **model family**, not just "Results."

Notes should specify:

- The dependent variable (and how it is coded).
- Treatment / condition coding and the omitted category.
- Controls included (or "Controls: yes; full list in SI").
- Fixed effects and clustering structure for SEs.
- Weights (and the weighting variable).
- Sample restrictions and N source.
- Significance markers (with thresholds).
- Data source and any transformations.
- For non-linear models: link function, units of coefficients (logit vs. AME).

### 7. Generate tables from code, not by hand

- Use `modelsummary`, `stargazer`, `gt`, `huxtable`, or `kable` (R); `stargazer` or `pystout` (Python); `esttab` (Stata) — whichever fits the workflow.
- Write the table-generating code so that re-running it after a model update updates the manuscript automatically. Hand-typed tables are a rich source of post-revision errors.
- Round in the formatting layer, not in the analysis — keep raw model output at full precision and round only when rendering.
- Insert numbers into the manuscript text programmatically (`\Sexpr{}` in knitr/Sweave, inline R/Python in Quarto, or LaTeX `\input{}` of generated `.tex` fragments) rather than retyping them from tables.

### 8. Production sanity

- Check that the compiled table fits the page (column count, font size). Wide tables should rotate (landscape) or move to SI.
- Check column alignment: numbers right-aligned or decimal-aligned, text left-aligned, headers per convention.
- Use booktabs (`\toprule`, `\midrule`, `\bottomrule`) or equivalent rules, with no vertical rules between columns.
- Confirm that the same coefficient appears with the same row label across tables (no `Treat` here and `Treatment_1` there).

## Output

When asked to design or revise a table, produce:

```
# Table Plan

Comparison: <one sentence>
Estimand / model family: <what is being estimated>
Column order: <what each column shows, why this order>
Row grouping: <treatment block / covariate block / FE / fit stats>
Precision and uncertainty: <decimals, SE vs CI, star thresholds>
Title: <names the estimand or model family>
Notes draft: <DV, coding, controls, FE, clustering, weights, N source, stars>
Reproducibility: <package, script path, output format>
Open issues: <anything that needs author input>
```

When asked to produce code, default to a `modelsummary` or `gt` script (R) or `stargazer`/`pystout` (Python), with model objects passed in the order the manuscript discusses them.
