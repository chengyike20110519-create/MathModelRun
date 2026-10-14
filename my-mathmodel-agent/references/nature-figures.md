# Nature-inspired evidence figures for mathematical modeling

Read this after `python-figures.md` when a user requests Nature-style scientific figures.
This is original, contest-adapted guidance learned from public skills, not journal endorsement.
Retain the established Python workflow; do not ask for the plotting language again.
Use saved observations and model outputs. Style changes do not create scientific evidence.

## 1. Build a visual argument

State one question, the conclusion supported by the available data, and its strongest limitation.
Give each panel a distinct inferential role: establish, compare, decompose, validate, or bound.
Use the smallest set that supplies those roles; different chart types alone do not justify panels.
If removing a panel changes no inference, merge it or move it to a separate supporting figure.
Give decisive evidence the largest area or first reading position when appropriate.
Supporting panels should be quieter but still readable; equal sizes are not a universal rule.
Keep negative outcomes and conclusion-changing boundaries visible.
Preserve scenario colors, definitions, denominator choices, and units across related panels.

## 2. Choose an archetype from the evidence

| Archetype | Suitable evidence | Modeling adaptation |
|---|---|---|
| Quantitative grid | Comparable measurements, runs, conditions | Shared-scale temporal/spatial results and a boundary diagnostic |
| Schematic-led composite | A necessary mechanism plus quantitative evidence | Explain a model chain, then test the consequences using saved outputs |
| Image plate plus quantification | Genuine calibrated images with corresponding measurements | Pair field imagery or simulation snapshots with the quantities they support |
| Asymmetric mixed-modality figure | Different but complementary evidence types | Give the main comparison a hero panel beside decomposition or validation |

These are choices, not required figure parts. A schematic does not belong in every panel a.
Use white quantitative backgrounds; dark image regions need a modality-specific reason.
Do not invent photographs, microscopic channels, mechanisms, or validation data to match a sample.
An AI concept illustration remains illustrative and separate from numerical evidence.
Prefer direct labels and dedicated legend/colorbar space when a legend would obscure the result.

## 3. Compose and measure at the final physical size

Start with the local manuscript preset near 7.1 inches wide and 9–10 pt body text.
Nature-inspired composition does not authorize shrinking a contest figure to journal microtype.
Use `nature_style` from `scripts/figure_tools.py` for a restrained Python starting style.
Plan gutters, legends, colorbars, and long labels before allocating the plotting rectangles.
Use one layout engine, then call `fig.canvas.draw()` after final layout-affecting changes.
Use `check_panel_alignment` to record actual axes rectangles in physical points.
Check shared edges, intended equal widths/heights, and repeated gutters only for comparable groups.
Record intentional hero-panel widths, equal-aspect maps, insets, and colorbars as exceptions.
Do not weaken every tolerance to hide an intentional local difference.
Grid cells that look equal in source are not proof that rendered plot areas are aligned.
Rerun geometry checks after changing fonts, labels, legends, scale, aspect, or figure size.
An alignment report measures geometry; it does not validate the model or its conclusions.

## 4. Worked data contract: dandelion climate comparison

The current trial uses saved outputs through `src/nature_climate_figure.py`.
It updates the active `population_area.png`, `.pdf`, and `.svg` paths in place.
Panel a is the wider main comparison: plant means at five actually saved day checkpoints.
Show process 5th–95th percentile intervals as independent vertical lines at those checkpoints.
Connecting mean points are reading guides; they do not add simulated intermediate observations.
Mean and process percentile bounds describe different distribution features.
A skewed process distribution can place the mean outside its 5th–95th percentile interval.
Do not construct invalid negative `yerr`, move the mean, or widen bounds to disguise that fact.
Draw the percentile endpoints and mean independently and label their statistical meanings.
Panel b shows mean occupied area using the model's 10 m occupancy cells and square-metre units.
Panels c, d, and e show day-365 mean plant counts per 5 m spatial cell for the three cities.
All maps use extent `(0, 100, 0, 100)`, `origin="lower"`, and the same positive LogNorm limits.
Show exactly zero mean-count cells as white with an explicit zero explanation.
Log color is a display transformation, not a change to the stored count or cell geometry.
The external source is at x = -1 m, y = 50 m; place and label its marker outside the map domain.
Counts per 5 m cell and occupied area based on 10 m cells are separate estimators.
Do not infer one from the other or label count-per-cell as density without area conversion.
Label the zero-living-plant fraction at a checkpoint without claiming permanent extinction.
A zero living count can coexist with viable seeds or later recovery unless the model proves otherwise.
These panels describe this simulation under its recorded assumptions, not field observations.

## 5. Review the rendered scientific meaning

Inspect the exported full figure and every panel at manuscript size before delivery.
Check whether the dominant visual object is the decisive evidence, rather than an annotation.
Verify displayed points, interval definitions, map orientation, bin size, normalization, and source marker.
Check that comparable maps retain a common color norm and distinguish zero from missing values.
Review small text, cropped legends, panel-letter positions, collisions, and grayscale readability.
Technical audits and visual review complement numerical recomputation; none replaces the others.
Deliver the actual preview, reusable vectors, caption, provenance, and any unresolved limitation.

## 6. Sources inspected on 2026-10-12

- Primary: [Yuan1z0825/nature-skills nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure), current [Apache 2.0 license](https://github.com/Yuan1z0825/nature-skills/blob/main/LICENSE).
- Evidence-role guidance: [multi-panel architecture](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/references/multipanel-evidence-architecture.md); [rendered QA](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/references/qa-contract.md).
- Secondary: [jing1312/nature-figure-skill](https://github.com/jing1312/nature-figure-skill), [MIT license](https://github.com/jing1312/nature-figure-skill/blob/main/LICENSE), independently maintained upstream snapshot described in its [derivative notice](https://github.com/jing1312/nature-figure-skill/blob/main/DERIVATIVE_NOTICE.md).
- Sample-based [Nature observations](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/references/nature-2026-observations.md) are design examples, not official publication requirements.

No external repository was wholesale installed and no external code was copied into this reference.
If later copying substantial source code, preserve the applicable license, authorship, and change notices.
Use gallery examples only for design exploration; demo values and Node/JS atlas output are not Python evidence.
