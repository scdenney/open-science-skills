---
name: conjoint-cleaning
description: Specialized logic for cleaning and reshaping choice-based conjoint data from Qualtrics exports into analysis-ready long format. Use when (1) preparing conjoint survey data for analysis, (2) reshaping wide Qualtrics exports to long format, (3) mapping conjoint choice and rating variables to profile-level outcomes, (4) translating attribute labels across languages, (5) diagnosing pilot contamination or data quality issues in conjoint data, or (6) setting AMCE reference categories. Covers Qualtrics column conventions, existing R packages, wide-to-long reshaping, choice variable encoding, attribute-level translation, data validation, and analysis-ready output.
---

# Conjoint Data Cleaning Expert

## Instructions

### 1. Qualtrics Export Settings and Metadata

**Export format:** When exporting from Qualtrics, select **"Use choice text"** (not "Use numeric values") so that attribute levels appear as human-readable labels. If working with non-Latin scripts (Chinese, Korean, Arabic), export as XLSX rather than CSV to avoid UTF-8/ANSI encoding issues.

**Metadata rows:** Current Qualtrics CSV exports include **3 header rows** before respondent data: (1) variable identifiers, (2) question text/descriptions, (3) ImportId JSON. Legacy exports have 2 rows. The `cjoint::read.qualtrics()` parameter `new.format = TRUE` (default) handles the 3-row format. For manual import via `readxl::read_excel()` or `readr::read_csv()`, skip the appropriate number of metadata rows after reading headers.

**Randomization order columns:** If "Export viewing order data" is enabled, Qualtrics adds `_DO_` columns (e.g., `Block1_DO`) containing pipe-separated integers showing element display order. These are useful for task-order robustness checks but are not needed for the core reshape.

### 2. Qualtrics Conjoint Implementation Methods

Qualtrics conjoint experiments use one of three implementation methods, each producing different column naming conventions:

**Method A — Conjoint Survey Design Tool (Strezhnev):** Generates JavaScript that Qualtrics executes to randomize profiles. Column naming follows `F-{task}-{profile}-{attribute}` for attribute levels and `F-{task}-{attribute}` for attribute names. The `cjoint` R package's `read.qualtrics()` function is purpose-built for this format.

**Method B — Custom JavaScript + Embedded Data:** Researchers write JavaScript to randomize attributes and store values in Qualtrics embedded data fields. Column naming is researcher-defined, commonly `C{x}-F-{task}-{idx}` for attribute names and `C{x}-F-{task}-{profile}-{idx}` for profile values. Requires manual reshaping (Section 4).

**Method C — Loop & Merge:** Each loop iteration represents one conjoint task. Embedded data fields are referenced via `${e://Field/variable_name}` and displayed with `${lm://Field/N}`. Column names reflect the embedded data field structure. Requires manual reshaping.

**Before writing any cleaning code:** Inspect the actual column headers, the QSF survey definition file, or any JavaScript in the survey to determine which method was used. Do not assume a column naming convention.

### 3. Existing R Packages for Conjoint Data Import

Before writing custom reshaping code, check whether an existing package handles the data format:

**`cjoint::read.qualtrics()`** — Purpose-built for Conjoint SDT exports (Method A). Reads Qualtrics CSV directly, handles metadata rows, outputs one row per profile with a `selected` column. Parameters: `responses` (choice column names), `covariates` (respondent-level variables), `respondentID`, `new.format` (TRUE for 3-row headers). Limited to binary forced-choice outcomes.

**`cjdata::reshape_conjoint()`** — Lightweight alternative. Functions: `read_Qualtrics()` + `reshape_conjoint()`. Handles basic wide-to-long conversion. Requires binary outcome variables (1/2 or "A"/"B"). Respondent covariates merged separately.

**`projoint::reshape_projoint()`** — For measurement-error-corrected analysis. Built-in support for repeated tasks (IRR estimation), missing data imputation (`.fill = TRUE`), and bias-corrected AMCEs. Outcome column names must contain task ID digits.

**`cregg::cj_tidy()`** — Reshapes wide-format data with automatic constraint detection via formula notation.

**When to use manual reshaping:** When the Qualtrics implementation uses custom embedded data fields (Method B) with non-standard column naming, or when the data requires language translation, attribute name merges, or pilot data exclusion that existing packages cannot handle.

### 4. Manual Wide-to-Long Reshaping

When existing packages cannot handle the data format, reshape manually. The goal: one row per respondent x task x profile, one column per attribute.

**Step 1: Build a long table of (ResponseId, task, profile, attribute_name, attribute_value)**

Iterate over tasks, profiles, and attribute positions. For each combination, read the attribute name from the name column and the corresponding value from the value column. This naturally handles randomized attribute order.

```r
for task in 1:T:
  name_cols <- paste0(prefix, "-F-", task, "-", 1:K)
  for profile in 1:P:
    val_cols <- paste0(prefix, "-F-", task, "-", profile, "-", 1:K)
    for idx in 1:K:
      append(ResponseId, task, profile, data[[name_cols[idx]]], data[[val_cols[idx]]])
```

Use `data.table::rbindlist()` for performance with large datasets.

**Step 2: Filter missing data.** Remove rows where `attribute_name` or `attribute_value` is NA — these indicate respondents who skipped the conjoint section.

**Step 3: Apply attribute name and level merges** before pivoting. Fix typos, encoding variants, or synonymous levels.

**Step 4: Pivot to wide-by-attribute** using `data.table::dcast()` or `tidyr::pivot_wider()`:

```r
dcast(long, ResponseId + task + profile ~ attribute_name, value.var = "attribute_value")
```

If `dcast` warns about duplicate row/column combinations, two positions in the same task share an attribute name for some respondents — investigate the name merge.

### 5. Choice Variable Mapping

Choice variables are separate Qualtrics questions (MC type), one per task, placed after each conjoint display.

**Identify choice columns:** These are NOT part of the embedded data fields. Map each choice question to its task number (Q17 -> task 1, Q19 -> task 2, etc.). Inspect the QSF or survey flow to confirm the mapping.

**Text vs. numeric encoding:** Text exports produce labels like "Person A"/"Person B" or "Profile 1"/"Profile 2". Numeric exports produce 1/2. Always verify from the actual data — do not assume.

**Create the binary outcome:**
```r
chosen_profile <- ifelse(raw_choice == "Person A", 1L,
                  ifelse(raw_choice == "Person B", 2L, NA_integer_))
# Merge by (ResponseId, task), then:
chosen <- as.integer(profile == chosen_profile)
```

**Handle missing choices:** Drop rows where `chosen` is NA. Some tasks may have higher dropout rates than others (especially the last task).

### 6. Ratings and Secondary DVs

Ratings may be **per-profile** (one per profile per task — usable as a continuous conjoint DV) or **per-task** (one rating of the chosen profile — descriptive only, not a standard conjoint DV).

**Endpoint label recoding:** Qualtrics text exports encode scale endpoints as text labels (e.g., "Strongly disagree" = 1, "Strongly agree" = 7). Recode these before converting to numeric. Intermediate scale points are already numeric.

### 7. Attribute-Level Translation and Factor Ordering

**Use `recode_factor()` with deliberate level ordering.** The order of arguments sets the factor level order, which determines:
- The **AMCE reference category** (first level = baseline, shown at zero)
- The **display order** in figures

**Reference category principles:**
- Ordinal attributes (time, income): **lowest** level as reference — AMCEs show benefit of higher levels
- In-group/out-group attributes (ethnicity): **majority/in-group** as reference — AMCEs show out-group penalty
- Status/legal attributes: **lowest status** as reference — AMCEs show benefit of higher status
- Nominal with neutral option: **neutral/no-opinion** as reference

**Catching unexpected values:** Set `.default = NA_character_` in `recode_factor()`. Without this, unrecognized values silently become new factor levels, masking pilot data contamination. This is not default behavior — it must be set explicitly.

**Drop unused levels:** After filtering, call `droplevels()` to remove factor levels with zero observations. `cregg::cj()` requires 2+ realized levels per factor.

### 8. Pilot and Data Quality Diagnostics

**Pilot detection:** Compare unique attribute levels in the data against the final design document. Extra levels (e.g., a country not in the final design) indicate pilot/pre-test respondents. Exclude these **as respondents** (all their rows), not just the anomalous rows — their entire randomization was generated by a different design.

**Missing conjoint data:** Respondents who skipped the conjoint section produce all-NA attribute columns. The NA filter in Step 2 removes them. Respondents who dropped out mid-conjoint will have fewer than T x P rows — this is acceptable for `cregg::cj()`.

**Duplicate attribute names:** Each task should have exactly K unique attribute names. If a merge creates duplicates within a task, the merge is incorrect.

**Choice completeness:** `chosen` should sum to T per respondent (one chosen profile per task). Fewer indicates missing choices for some tasks.

### 9. Subgroup Variables

Include respondent-level covariates in the analysis-ready dataset even for main-effects-only analysis. Future subgroup and interaction analyses should not require re-running data prep.

Merge demographics (age, gender, education, urban/rural, ethnicity, party membership), treatment assignments, randomization indicators, and open-text responses by ResponseId after reshaping.

### 10. Output Format and Package Compatibility

Save as `.rds` files (one per conjoint). The output should have:

- One row per respondent x task x profile
- One column per attribute (**factor type**, not character — `cregg::cj()` will error on character columns)
- `ResponseId`: respondent identifier (character or numeric)
- `task`: task number (integer)
- `profile`: profile number (integer)
- `chosen`: binary outcome (**numeric 0/1**, not logical or factor)
- Optional: `rating` (numeric)
- Subgroup variables at the respondent level

**cregg compatibility:** `cj(data, chosen ~ Attr1 + Attr2 + ..., id = ~ResponseId)`. The `id` parameter requires a **tilde formula** (`~ResponseId`), not a bare name. The `estimate` parameter accepts `"amce"`, `"mm"`, `"mm_differences"`, `"amce_differences"`, and `"frequencies"`.

**cjoint compatibility:** Expects a `selected` column (logical) and attributes named with the F-based convention. Use `cjoint::amce()` for estimation.

**projoint compatibility:** Requires a `projoint_data` object created via `reshape_projoint()`. Supports repeated-task IRR estimation and bias-corrected AMCEs.

## Quality Checks

- [ ] **Implementation method identified:** Determined which of the three Qualtrics methods was used (SDT, custom JS, Loop & Merge) by inspecting column headers or QSF file
- [ ] **Existing packages evaluated:** Checked whether `cjoint`, `cjdata`, or `projoint` can handle the data format before writing custom reshaping code
- [ ] **Metadata rows handled:** Skipped the correct number of header rows (3 for current Qualtrics, 2 for legacy)
- [ ] **Column convention verified:** Conjoint column naming pattern confirmed from actual data, not assumed
- [ ] **Attribute randomization handled:** Reshape pairs each name column with its value column at the same position
- [ ] **Choice encoding verified:** Choice values confirmed from actual data, including text-encoded choices
- [ ] **Pilot data excluded:** Attribute levels compared against design document; pilot respondents excluded entirely
- [ ] **Missing data filtered:** Skipped-section respondents and missing-choice tasks properly removed
- [ ] **Attributes are factors:** All attribute columns are factor type (not character) with 2+ realized levels
- [ ] **Outcome is numeric 0/1:** `chosen` column is numeric, not logical or factor
- [ ] **Reference categories set:** Factor levels ordered with intended AMCE baseline first
- [ ] **Unmapped values caught:** `recode_factor(.default = NA_character_)` used to surface unexpected values
- [ ] **Validation passed:** Row counts, choice sums, and factor levels match expectations
- [ ] **Subgroup variables included:** Respondent-level covariates present for future interaction analyses
