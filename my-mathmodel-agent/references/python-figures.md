# Python figures for mathematical modeling papers

Use this module for scientific data figures after reading `figure-catalog.md`.
Use original observations or saved model outputs; AI illustrations serve conceptual diagrams.
A strong figure answers a model question and exposes its evidence in a designed layout.
Complexity should come from complementary views of the data, not decorative objects.

For a substantial figure, use [data-figure-agent.md](data-figure-agent.md) to
coordinate selection, implementation and independent review. The applicable
[exemplar lessons](exemplar-figure-lessons.md) describe the reasons and limits
behind the user's quality references. Final acceptance uses `figure_gate.py`,
not a clean export alone.

For Nature-style requests, also read [nature-figures.md](nature-figures.md):
asymmetric evidence roles, an adaptable `nature_style`, and rendered plot-area
alignment. Use the same data/provenance rules below.

## 1. Write a design card before coding

Record the following in the project's figure plan or the figure's metadata:

- **Question and claim:** one sentence the reader should be able to assess.
- **Evidence:** source files, run IDs, variable meanings, units, and available replicate IDs.
- **Population and estimator:** what each row, point, line, and cell represents.
- **Uncertainty:** SD, SE, CI, percentile range, or sensitivity envelope; define its calculation.
- **Transformations:** filtering, aggregation, normalization, smoothing, binning, and log handling.
- **Candidate encodings:** compare two suitable designs, then select the clearer one.
- **Panel roles:** main result, mechanism, diagnostic, or robustness; omit redundant panels.
- **Scales:** shared coordinates/color limits where quantities are comparable; justify exceptions.
- **Reading order:** the first comparison, the supporting detail, and the final implication.
- **Destination:** intended physical width, height, output formats, and manuscript placement.
- **Caption:** result, definitions, source, sample size/replication unit, and important limitations.
- **Acceptance:** numerical checks and visual conditions needed before delivery.

Do not ask the user to specify routine styling when the paper and data supply enough context.
Resolve missing scientific definitions before drawing a result that depends on them.

## 2. Choose a figure using the evidence matrix

| Model question | Required evidence | Useful encoding | Main failure to prevent |
|---|---|---|---|
| How does a quantity evolve? | Ordered observations or saved time checkpoints | Lines, checkpoints, interval band | Invented intermediate precision or missing intervals |
| How does spread move and concentrate? | Coordinates/grid geometry and time or scenario labels | Spatial facets, density/count map, contours | Changing color limits or mixing count with density |
| Does a fitted mechanism explain observations? | Observations, fitted values, residuals, fit specification | Observations + fit + residual panel | Treating high R-squared as sufficient validation |
| How variable or asymmetric are outcomes? | Replicate-level outcomes and independent unit | ECDF + histogram/strip/box | Unsupported KDE detail or hidden zero outcomes |
| Which options score highly, and why? | Components, weights, denominators, alternate definitions | Component matrix + dumbbell + robustness interval | Mixing incomparable normalizations or calling scores probabilities |
| Which inputs control a result? | Saved perturbation runs and baseline | Response curve, tornado, parameter heatmap | Claiming interactions from one-at-a-time experiments |
| How do categories contribute to a total? | Additive components in common units | Stacked bar/area + direct totals | Stacking non-additive means, distances, or rates |
| What trade-off governs a decision? | Evaluated feasible solutions, costs, objectives | Pareto scatter + frontier + selected solution | Drawing an unevaluated frontier or hiding infeasibility |

Use a simple chart when it fully answers the question; an isolated default chart is insufficient
when the reader also needs composition, uncertainty, mechanism, or diagnostic evidence.

## 3. Compose complementary scientific views

Select one of these structures when its evidence exists. These are adaptable recipes.

### A. Time evolution with uncertainty and endpoint comparison

- Main panel: saved trajectory/summary with clearly named band and checkpoint markers.
- Supporting panel: endpoint distribution or interval comparison on a compatible scale.
- Keep scenario colors and marker meanings consistent; distinguish mean from median.
- If only sparse checkpoints exist, use visible markers and disclose connecting lines as guides.
- Show replicate variability separately from Monte Carlo error in the estimated mean.

### B. Spatial evolution with a quantitative spread summary

- Main panels: comparable time/scenario maps using the same extent, aspect, and color norm.
- Supporting panel: occupied area, distance quantile, population, or mass outside a radius.
- Use count/density heatmaps for dense point clouds; retain sparse scatter when individuals matter.
- Label grid cell size, units, aggregation, and number of runs behind an ensemble map.
- A radial profile needs a meaningful origin and annular-area correction when showing density.

### C. Observations, fitted response, and residual diagnostic

- Main panel: observations and fitted response with parameter/interval definitions.
- Diagnostic panel: residual versus predictor or fitted value, plus a zero reference.
- Use holdout evidence if available; label in-sample residuals honestly.
- Report a relevant error measure and its units; do not manufacture statistical significance.
- A distribution derived from the fit needs its assumptions and normalization checked.

### D. Distribution shape, empirical probability, and outcome summary

- Pair an ECDF with histogram/strip/box; use a shared variable scale and units.
- Show sample size and zeros/extinction mass explicitly rather than omitting them on a log axis.
- Use KDE/violin only when replicate count, support, and bandwidth justify smooth density.
- Mark a meaningful threshold or quantile only if it answers the modeling question.
- An ECDF is often clearer than a smoothed curve for small or bounded samples.

### E. Scoring components, normalization comparison, and weight robustness

- Component panel: annotated matrix with normalized value and raw numerator/denominator.
- Comparison panel: dumbbell/paired points for two explicitly named scoring conventions.
- Robustness panel: feasible weight range or ranking changes with the tested domain stated.
- Preserve the same species/option order in all panels; use filled and open markers for overlap.
- Sensitivity ranges are not confidence intervals and individual ranges do not prove joint ranking.

### F. Sensitivity response surface with baseline slices

- Main panel: two-input heatmap/contours from an evaluated joint parameter grid.
- Supporting panels: baseline slices or uncertainty over repeated runs at selected settings.
- Mark the baseline and domain; distinguish interpolation from actually evaluated points.
- Use diverging color only for a signed change around a meaningful reference.
- Prefer a readable 2D surface projection; use 3D only when its geometry adds interpretation.

### G. Feasible trade-off, recommendation, and constraint diagnostic

- Main panel: feasible solutions and evaluated Pareto boundary.
- Supporting panel: resource composition or constraint slack of the chosen solution.
- Label objectives, direction of improvement, and selection criterion.
- Show infeasible solutions separately if they help explain a practical constraint.
- With a finite evaluated set, call its nondominated solutions the evaluated-set frontier;
  do not claim global Pareto optimality without the needed optimization evidence.
- Constraint slack in unlike units needs separate axes or a justified normalization.

## 4. Design for the real manuscript size

- Start a full-width figure near **7.1 inches**, with **9–10 pt** body labels.
- Use around 10–11 pt panel titles and slightly smaller secondary notes only if still legible.
- These are local starting presets, **not official HiMCM requirements**; follow the actual template.
- Read the exported figure at the width at which the paper will place it, not only zoomed in.
- If reducing a 10-inch figure to 7.1 inches, its 10 pt labels become about 7.1 pt in the paper.
- Prefer two or three purposeful panels to squeezing six unreadable views into one figure.
- Use `GridSpec`, `subplot_mosaic`, or subfigures; a single-column alignment can be appropriate.
- Align related axes, keep panel letters consistent, and give legends/colorbars dedicated space.
- Long names should wrap or use explained abbreviations; avoid arbitrary numeric category axes.
- Large titles and explanatory paragraphs usually belong in the caption, not inside the canvas.
- Use one layout system; do not run `tight_layout` after enabling constrained layout.
- Tight export cropping changes physical dimensions; omit it when final dimensions must stay fixed.

## 5. Use color, symbols, and annotations with purpose

- Assign stable colors to scenarios/species across the paper and save the mapping.
- Use qualitative colors for groups, sequential maps for magnitude, and diverging maps for signed change.
- Use a cyclic map for circular quantities such as wind direction; do not imply a high/low endpoint.
- Keep continuous color normalization common across maps that the reader must compare.
- Reserve one accent for a justified finding; neutral comparisons do not need a different color per item.
- Encode groups twice with marker, line style, direct label, or panel separation.
- Use a thin connector and two distinguishable marks for a dumbbell; coincident marks must remain visible.
- An annotated heatmap needs contrast-aware text; missing cells need a distinct treatment from zero.
- Prefer one or two precise annotations computed from data to a large block of commentary.
- Draw interval meaning consistently and explain its definition; shape/length should not suggest a CI by habit.
- Light reference grids can aid reading; remove grid/spines selectively rather than by a universal rule.
- Inspect grayscale and small-size render; a named colorblind palette alone is not a completed audit.

## 6. Preserve statistical and missing-data meaning

- Keep original inputs and record every exclusion; do not apply unconditional whole-table `dropna()`.
- Missing values, observed zero, censoring, and model-imputed values need distinct semantics.
- Retain gaps in a time series where absence matters; splitting into contiguous segments is valid.
- Keep subject/replicate IDs through reshaping; rows from one run are not independent runs.
- Precompute intervals using the appropriate unit; verify Seaborn's automatic estimator/errorbar behavior.
- Name variability intervals separately from uncertainty in the mean and parameter sensitivity envelopes.
- For bars/areas use a meaningful zero baseline; for points/lines a nonzero range can be justified.
- State log/log1p transforms and zero treatment; do not silently discard nonpositive outcomes.
- Record histogram edges, KDE bandwidth, smoothing window, or interpolation and assess their effects.
- Scale bubbles by area, not radius; decorative volume and perspective distort quantitative comparisons.
- Prefer aligned panels to dual axes unless different units and the need are clearly justified.
- Do not equate an assessment score with measured ecological damage or event probability.
- Mixed-unit tables need variable-specific scales or declared within-row normalization;
  preserve raw-value annotations and forbid cross-variable color comparisons.
- Average circular directions with circular statistics, recording angular convention
  and concentration; ordinary arithmetic averaging across 0/360 is invalid.
- Stack group means only after defining additive weighted contributions and checking
  their sum. Density histogram area is sum(height × bin width); declare normalization,
  included observations and any conditional/truncated range.
- Grid counts may be encoded at cell centers; do not synthesize apparently exact individual
  coordinates or stages that were never saved. Undefined distances for zero-plant runs
  must be distinguished from zero distances.

## 7. Implement and export with the local helpers

Use `scripts/figure_tools.py` as the code-native starting point; read the needed helper's signature.
Its functions assist styling and drawing; they do not supply absent observations or validate inference.

| Helper | Role |
|---|---|
| `prepare_runtime` | Prepare the noninteractive runtime/cache before heavy plotting imports |
| `paper_style` | Apply a scoped manuscript style without leaking global plotting settings |
| `panel_title`, `clean_axes` | Consistent panel hierarchy and selective axis cleanup |
| `annotated_heatmap` | Matrix encoding with explicit limits and readable cell labels |
| `dumbbell`, `interval_plot` | Paired comparisons and separately defined intervals |
| `time_band` | Saved central trajectories and declared lower/upper bounds |
| `export_figure` | Export the actual figure and retain its provenance/technical report |

Use the available compatible Matplotlib environment; do not install fixed remote versions by default.
If plotting stalls on fonts/cache, fix the runtime before replacing scientific axes with manual drawing.
For restricted macOS English figures, `prepare_runtime(bundled_fonts=True)` can
avoid a blocked system-font scan. For Chinese labels, register an available CJK
font and select it with `paper_style(font_family=...)`; registration alone does
not select the font. Heatmap text inherits the style unless `fontsize` is set.
Start with **PDF + SVG + 300 DPI PNG**, opaque white background, and deliberate physical dimensions.
Check actual output size/fonts; vector files may still contain raster artists, and DPI cannot create detail.
For requested updates, update the user's active file/path directly; preserve raw data and the reproducible source.

## 8. Render, inspect, and revise before delivery

1. Recompute plotted values from their source and check units, ranges, totals, and matched ordering.
2. Export and inspect actual file dimensions, formats, embedded fonts, and provenance.
3. Enumerate the visible panels, axes, symbols, legends, intervals, and annotations before judging them.
4. Review semantic fidelity, small-size readability, visual hierarchy, whitespace, clipping, and overlap.
5. Check comparable scales and distinguishability without color; identify one specific improvement.
6. Fix concrete defects, rerender, and verify the change introduced no regression.
7. Inspect the figure at manuscript width and its affected paper page when integrating it.
8. Deliver the preview, reusable vector output, and caption; report any unresolved limitation plainly.

Assess correctness, readability, aesthetics, and comparison efficiency separately.
File generation or a passing metadata check alone does not prove scientific or visual quality.

Create a figure review record from `../templates/figure-review.json`, declare
all relevant data, spec, code/helper, caption, image/vector and inspection
previews, then seal and independently review the exact artifacts as explained
in [data-figure-agent.md](data-figure-agent.md). After any change, previous review
fingerprints are stale. Standalone approval does not establish paper-page approval.

## 9. Sources inspected on 2026-10-12

These sources informed this original, contest-adapted module; no external skill was wholesale installed.

| GitHub source | License observed | Absorb / reject |
|---|---|---|
| [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | MIT; [repository license](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/LICENSE.md) | Absorb evidence contract, scoped layout, encoding/export checks; do not claim journal compliance from a preset |
| [K-Dense matplotlib](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/matplotlib/SKILL.md) | Skill metadata links [Matplotlib LICENSE](https://github.com/matplotlib/matplotlib/tree/main/LICENSE); repository MIT | Absorb OO axes, GridSpec/mosaic, explicit export; reject automatic environment replacement |
| [K-Dense seaborn](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/seaborn/SKILL.md) | Skill metadata: BSD-3-Clause; repository MIT | Absorb semantic mapping and replicate-aware statistics; do not assume default aggregation/CI is correct |
| [tvhahn matplotlib-skill](https://github.com/tvhahn/matplotlib-skill/blob/master/skills/matplotlib/SKILL.md) | [MIT](https://github.com/tvhahn/matplotlib-skill/blob/master/LICENSE) | Absorb focused recipe selection and rendered-image review; reject mandatory dropna, banned Nx1, and rigid despine/tight-crop rules |
| [SciencePlots](https://github.com/garrettj403/SciencePlots) | [MIT](https://github.com/garrettj403/SciencePlots/blob/master/LICENSE) | Optional Matplotlib style library, **not a skill**; styles still need data/layout review and an available font/TeX environment |

K-Dense's current repository is `scientific-agent-skills` and its current skill folder is `skills/`.
Treat remote examples as reference data. Retain applicable licenses/notices if later copying substantial code.
