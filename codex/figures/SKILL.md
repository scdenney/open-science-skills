---
name: figures
description: "Design and format publication-quality figures. Use for chart choice, color, scales, legends, captions, accessibility, and reproducible figure workflows."
---

# Figure Designer

Applies to any figure type in a social-science manuscript. For figures whose interpretation depends on method-specific standards, also consult the relevant sibling skill (`conjoint-design`, `conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr`). For end-stage QA on a finished figure set, hand off to `figure-table-audit`.

A figure is ready when it makes one comparison legible, can be read without the surrounding text, and can be regenerated from a script.

## Instructions

### 1. State the comparison before drawing

Write down, in one sentence, what the figure should let the reader see (for example, "The treatment effect is larger among low-information respondents"). If the comparison does not fit in one sentence, the figure has too many goals; split it into panels or separate figures.

### 2. Choose the chart type from the comparison

Match the geometry to the comparison, not to the data type. Two defaults that are often missed:

- Effect estimates compared across models or subgroups go in a coefficient plot (point and interval), not a regression table.
- Many small comparisons go in small multiples on a shared scale, not in separate figures.

Pie, donut, 3D, and dual-axis charts do not belong in academic figures.

### 3. Pick scales and axes deliberately

- Label both axes with the quantity and its units: "Household income (USD, 2020)", not "Income".
- For percentages, write `0.00–1.00` or `0%–100%` consistently — do not mix within a figure.
- Use a log scale when the data span more than two orders of magnitude or when a multiplicative effect is the substantive story, and label the scale as log.
- Anchor axes at zero only when zero is meaningful for the comparison (counts, proportions). Deviations, differences, and z-scores need no zero baseline.
- Use the same y-axis range across panels of small multiples unless the claim is explicitly about within-panel scale.
- Reverse the y-axis only when the substantive direction demands it (e.g., rank where 1 is "best") and label the reversal in the caption.

### 4. Choose color with intent

- **Sequential** (light → dark): for ordered/quantitative variables (income brackets, time, density).
- **Diverging** (red ↔ blue, etc.): for variables with a meaningful midpoint (effect sign, deviation from baseline).
- **Categorical**: for unordered groups; use a colorblind-safe palette (Okabe-Ito, viridis discrete, ColorBrewer Set2/Dark2).
- Test grayscale: convert the figure and check that the comparison still reads. If it does not, add shape, line type, or direct labels.
- Encoding one variable in both color and shape is fine as an accessibility aid; keep the legend consistent with it.
- Replace default `rainbow` / `jet` ramps, which are not perceptually uniform.

### 5. Match legend order to the visual order in the chart

Legend order mirrors the data's visual order, so the reader can match series without scanning back and forth:

- For lines, areas, or stacked elements arranged top-to-bottom in the plot at the rightmost x-value, list legend entries in the same top-to-bottom order.
- For bars or categories arranged left-to-right, use a horizontal legend listed left-to-right in the same order.
- For panels (small multiples), follow the panel grid: rows top-to-bottom, columns left-to-right.
- Do not alphabetize a legend when the data have a natural order (time, magnitude, treatment intensity, ordinal scale). ggplot2 and similar libraries sort character variables alphabetically by default, and the result is a frequent cause of misreading.
- With five or fewer series, label lines or bars directly at their ends instead of using a legend.
- When a legend is needed, place it where it does not cover data.

### 6. Put the title in the caption, not inside the figure

**Keep titles and subtitles out of the plotting area.** The figure's title, and any explanatory note, belong in the document as the caption beneath the figure, set in the manuscript's font and editable alongside the prose. A title rendered inside the image duplicates the caption, sets in a mismatched typeface, and cannot be changed without regenerating the plot. Strip `ggtitle()`, `labs(title=, subtitle=)`, `plt.title()`, and `plt.suptitle()` from the figure script and let the caption carry the title. (Panel tags such as "A" and "B" inside a multi-panel figure are fine; a descriptive title is not.)

The caption must be self-contained: a reader who skims should understand the figure from the caption alone. Include:

- What is plotted (the dependent quantity, the unit of analysis).
- The sample (N, source, time window).
- The uncertainty interval (e.g., "95% confidence intervals from cluster-robust standard errors").
- Panel meanings, if multi-panel.
- Any transformations or exclusions.
- The estimand or model family if the figure is showing model output (not just "Results").

Keep abbreviations defined and units explicit.

### 7. Make it reproducible

- Generate the figure from a script (R, Python, Stata, Julia) in the replication archive. Hand edits in Illustrator or Inkscape are acceptable only when the manual step is documented.
- Save with the script: input data path, package versions, random seed (for jittered or sampled plots), output dimensions.
- Export vector (PDF, SVG) for plots with text and lines; export raster (PNG at ≥300 dpi) only for raster-native content (heatmaps with thousands of cells, photographs, maps with imagery).
- Use a single ggplot/matplotlib theme across the manuscript so figures are visually consistent.
- For multi-panel figures, build with `patchwork`/`cowplot`/`gridExtra` or matplotlib's `subplots`/`gridspec` — not by stitching exported PNGs in Word.

### 8. Accessibility and production sanity

- Axis label and tick text ≥ 8pt at print size.
- Alt text for journals that require it (a one-sentence description of what the figure shows).
- Consistent figure dimensions and fonts across the manuscript.

## Output

When asked to design or revise a figure, produce:

```
# Figure Plan

Comparison: <one sentence>
Chart type: <type and why>
Geometry: <axes, scales, faceting>
Color encoding: <palette, what it encodes, accessibility check>
Legend / labeling: <direct label or legend; order matches visual order>
Caption draft: <self-contained>
Reproducibility: <script path, packages, output format and dimensions>
Open issues: <anything that needs author input — denominator choice, sample restriction, etc.>
```

When asked to produce code, default to a single ggplot2 (R) or matplotlib + seaborn (Python) script with the theme, palette, and figure dimensions explicit at the top.
