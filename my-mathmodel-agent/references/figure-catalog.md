# Mathematical modeling competition figure catalog

For the user's eight reference figures and their reasons, prerequisites and
transfer boundaries, read [exemplar-figure-lessons.md](exemplar-figure-lessons.md).
For executing a substantial chart upgrade, use [data-figure-agent.md](data-figure-agent.md).
AI concept diagrams follow [ai-workflow-gate.md](ai-workflow-gate.md).

Use a figure because it makes a model, comparison, uncertainty, or decision
easier to inspect. The three HiMCM exemplars reviewed for this skill suggest a
useful progression: a workflow and state diagram establish the model, maps and
time series establish the inputs, spatial snapshots and distributions show the
simulation, and sensitivity or ranking plots explain the decision. Keep this
sequence when it fits the problem.

## Core figure types

| Type | Best question | Typical encoding | Required annotation |
|---|---|---|---|
| Workflow diagram | How do inputs become outputs? | boxes, arrows, one direction | input, model, output, validation |
| State-transition diagram | How does an entity move between stages? | nodes and labeled arrows | state meaning, transition probability or delay |
| Time-series small multiple | How do forcing and outcomes change over time? | aligned line panels | units, time origin, scenario labels |
| Spatial small multiple | How does a pattern evolve in space? | equal-scale maps or grids | coordinate units, time, shared color scale |
| Uncertainty band or interval plot | How variable is the result? | mean/median with interval | replicate count and interval definition |
| Distribution plot | What is the shape or tail of outcomes? | histogram, ECDF, violin, or dot plot | bin or bandwidth rule and sample size |
| Sensitivity or ablation plot | Which assumption changes the conclusion? | tornado, slope, response curve, or paired dots | varied range and fixed conditions |
| Component/ranking plot | Which indicators drive a score? | stacked bars, ordered dots, or slope chart | normalization, weights, and direction |

## Selection by argument and presentation

Evaluate three independent dimensions, without treating subjective scores as
award predictions: visual quality (hierarchy, spacing, typography, contrast),
presentation ability (how clearly the relationship and conclusion are shown),
and modeling maturity (appropriate encoding, provenance, uncertainty, and
limits). A restrained interval plot can be stronger than an ornate 3D chart.

| Type | Argument served | Design opportunity | Evidence needed |
|---|---|---|---|
| Illustrated workflow | Full-paper logic | coherent icons and Q1/Q2 branches | actual implemented route; no unsupported causal links |
| Variable–formula–algorithm diagram | How computation works | compact cards and labeled connectors | implemented variables, equations, update order |
| Lifecycle/state diagram | Delays, feedback, survival | botanical icons plus precise transitions | implemented states; establishment and mortality paths |
| Aligned time series | Forcing and seasonal differences | consistent scenario colors, separate variable panels | dated records and original units |
| Mean/median with interval band | Trend and stochastic variation | direct labels and selected milestones | replicate count; process quantiles distinguished from mean confidence intervals |
| Spatial scatter snapshots | Individual locations and stages | equal-scale panels, state colors | saved coordinates and stage records; illustrative run identified |
| Spatial heatmap/contours | Aggregate spatial concentration | shared perceptually uniform color scale | saved grids; density, occupancy, and dispersal probability distinguished |
| Annotated heatmap matrix | Compact month/indicator comparison | numbers plus restrained color | comparable normalization; separate scales for unlike units |
| Dumbbell/slope plot | Alternative methods or normalization | paired marks and direct labels | matched outputs; common scale |
| Interval dot plot | Ranking and robustness | main score plus range | range definition; sensitivity is not a statistical confidence interval |
| Observations plus fitted curve | Parameter estimation | distinguish observations and model | original observations, fit procedure, residual or validation checks |
| PDF/ECDF distribution | Outcome shape and tails | concise distribution comparison | samples or justified distribution; probabilities versus densities labeled |
| Sensitivity heatmap/response surface | Interactions and thresholds | highlight selected operating point | joint parameter experiments; do not infer interaction from one-at-a-time tests |
| Stacked area/bar plot | Composition and contributions | few meaningful groups | additive quantities; do not stack means of distances without an additive definition |
| Geographic context map | Location and applicability | restrained basemap and study markers | source and geographic accuracy; context map is not measured species distribution |

## Lessons from exemplar figures

- Pair complementary outputs such as population and occupied area; increasing
  population need not imply proportional spatial expansion.
- Show the parameter evidence chain when available: observations → fitted
  relationship → modeled response or distribution. Never invent observations
  or add a fitting method just to imitate an exemplar.
- Use shared coordinates and color scales for temporal or scenario comparison.
  Prefer requested milestones to an unreadable twelve-panel page.
- Explain zero handling before plotting logarithmic counts. If using log1p,
  label the transformation explicitly.
- Replace repetitive legends with direct labels or a continuous parameter
  colorbar when appropriate. Pale curves must remain visible after shrinking.
- Dual axes and R-squared alone do not validate a fit. Use separate panels
  when dual axes invite a misleading relationship.
- Do not add unavailable variables such as wind direction, radiation, or
  stage-specific coordinates. Collect the evidence first or choose another plot.
- Quantitative charts use reproducible plotting code. AI illustrations may
  supply conceptual icons, but must not define quantitative coordinates,
  interval lengths, fitted curves, or ranking bar geometry.

## Advanced types that are useful when earned

- A heatmap is strong for a two-dimensional grid, transition matrix, or
  parameter-by-scenario response. Use a shared scale and annotate the unit.
- A contour or response-surface plot is strong when two continuous inputs and
  one output are genuinely modeled. Add the observed or selected operating
  point; do not imply precision between sparse simulations.
- A polar plot is appropriate for real direction, angle, or seasonality. It is
  useful for wind direction or directional coverage, but not for ordinary
  category comparisons.
- A 3D surface is appropriate only when the third dimension is a real
  continuous response and the view adds information that a heatmap or contour
  plot hides. Prefer a 2D projection when labels, exact values, or uncertainty
  matter. Never use 3D bars merely to make a paper look advanced.
- A network or Sankey-style diagram is appropriate for flows between states or
  resources. Keep the number of nodes small enough that edge direction and
  magnitude remain readable.

## Visual rules for a polished competition paper

For implementation, use [python-figures.md](python-figures.md): figure design
cards, complementary panel recipes, real print dimensions, reusable Matplotlib
helpers, and export/visual verification. The catalog selects the evidence;
that reference turns it into a designed, inspected figure.

Use one visual question per figure and one main message per panel. Prefer two
or three purposeful panels over a dense dashboard. Keep axes, units, legends,
and color meanings consistent across figures. Directly label a few important
values, but do not label every mark when it harms readability. Use a neutral
background, restrained grid lines, adequate contrast, and a type size that is
readable at the final PDF scale.

For stochastic models, pair a process visual with a summary visual: for
example, four spatial snapshots plus a count/area interval plot. For scoring
models, pair the final ranking with a component plot or weight-sensitivity
plot. A single representative simulation may illustrate mechanism, but the
caption must say so; means, intervals, and rankings must come from the full
declared replicate set.

Before embedding a figure, check: source data and script are recorded; units
and sample size are visible; the caption states whether values are observed,
assumed, or simulated; the figure is interpretable in grayscale or with a
color-blind-safe palette; and the rendered PDF has no clipping, overlap, or
unreadable labels. The figure-type icons in `../assets/figure-type-icons.svg`
are a planning reference, not content to paste into a submission.
