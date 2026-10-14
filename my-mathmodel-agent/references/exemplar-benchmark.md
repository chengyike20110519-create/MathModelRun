# Problem-type quality benchmark

Select criteria from the actual subproblem, available data and contest rules.
For mixed problems, assess each subproblem separately. Complexity and model
count are not quality measures; a simple validated model may be the best route.
These targets do not guarantee an award and do not replace evidence gates.

| Type | Baseline | Strong validation | Typical failure |
|---|---|---|---|
| Prediction | Persistence, trend or seasonal naive model | Time-respecting backtest, leakage checks, error by horizon, uncertainty; compare a justified alternative when feasible | Random time split, untested extrapolation, extra models without benefit |
| Optimization | Feasible simple heuristic or current policy | Constraint residuals, solver status, bound/gap if available, tiny exact instance, sensitivity of the decision | Infeasible optimum, omitted constraints, claiming optimality without proof |
| Evaluation / ranking | Transparent equal weights or a justified existing rule | Scaling and direction checks, weight perturbation, rank stability, external validation when available | Arbitrary weights, double-counted correlated indicators, false precision |
| Simulation | Analytic limiting case or simple mechanism | Conservation/units, boundary cases, repeated seeds, convergence and uncertainty, calibration when data exists | One random run, invented calibration, plausible-looking animation |
| Mechanistic estimation | Dimensional balance or defensible simple estimate | Identifiable parameters, measured-driver calibration when available, residuals and uncertainty | Assumed share presented as a fitted fact |

Common requirements: answer every requested deliverable, distinguish measured,
estimated and assumed values, cite retrievable data, compare fairly, and test
assumptions that could change the conclusion. Disaggregate only when variation
matters and available evidence supports it. An external projection is a useful
cross-check when comparable and independent; its absence is a stated limitation,
not an automatic failure. Do not force a letter, policy split, or full page budget
unless the actual contest asks for it. Quality comes from sufficient evidence,
not filling pages.

## Energy-paper examples (conditional)

The existing notes below describe energy/compute estimation papers and retain
their original team references. Their source papers have not been reverified in
this update; verify originals before citing team numbers or attributed methods.
They are examples to adapt, not universal scoring requirements.

## 1. Estimate the core quantity from a driver, not an assumed share

Awarded papers derive the headline number from measurable physical quantities
and then **fit the free parameters to real data**. They do not pick a
plausible percentage band and call it a model.

Observed patterns:

- Decompose the target into parts that each have a measurable driver. Team
  15022 estimated HPC energy as `E_HPC = E_crypto + k * E_DC`, pulling
  cryptocurrency energy from the Cambridge Bitcoin Electricity Consumption
  Index and data-centre energy from the IEA, then *fit* the HPC share `k` and
  the energy-vs-compute relation rather than fixing them.
- Build bottom-up from a real device/asset list when one exists. Team 15502
  walked the TOP500 supercomputer list, split machines into MPP vs Cluster,
  and summed per-machine energy from rated capability and energy-conversion
  efficiency, anchored to a real measured total (551 EFlops societal compute,
  end-2023).
- Fit a functional form to data and show the fit. 15022 fitted
  `E = a * ln(u * P) + b` (HPC energy vs global compute power `P`) and plotted
  the fitted curve against the points.

**Conditional improvement target.** For every headline quantity, ask "what physically
measurable driver is this estimated from, and which parameter was fit to which
data points?" If the answer is "we assumed a range", the route is not yet
award-calibre. When suitable data exist, fit and validate the central relationship. Otherwise
label assumptions and test how they affect the result.

## 2. Disaggregate by region and by end-use

Awarded papers avoid a single global average for anything that varies
geographically or by component.

- Weight energy mixes by where the facilities actually sit. 15022 modelled the
  US, China, and a third bloc separately; 16226 used US and China regional
  electricity data (EIA state data) rather than one global grid factor.
- Split energy into end-use components. 16226 decomposed total energy into
  electricity, water, chemical fuel, building, manufacturing, and waste, then
  carbon-accounted each.
- Fit different parameters for different regimes when the data says so. 15022
  used utilisation 60% before 2018 and 50% after, because post-2018 compute
  growth changed the regime.

**Conditional improvement target.** "Global average" is a fallback, not a primary model.
The data plan must name the disaggregation axis (region / source / end-use /
time regime) and justify any collapse to a single average.

## 3. Forecast with several models and compare; validate against an external number

Awarded papers do not bet the projection on one extrapolation.

- Use at least two structurally different forecast models and compare. 15502
  combined grey prediction GM(1,1), ARIMA, and a resistant differential
  equation, and compared their trajectories.
- Backtest honestly and report the error even when it is unflattering. A grey
  model trained on 2015-2020 under-predicts 2024 because growth accelerated;
  the awarded move is to *use that failure* to justify a scenario envelope
  around an external projection, not to hide it.
- Anchor the forecast to an independent external projection (IEA, IPCC,
  national lab, IEA "Energy and AI") and present your model as a band around
  it, not as a lone curve.

**Conditional improvement target.** A single-extrapolation projection with no external
cross-check scores at most 2 on Method validity. Provide >=2 compared models
plus one independent external anchor, and report the backtest error.

## 4. Publish a real data-source table

Awarded papers make provenance inspectable, not just claimed.

- Include an explicit data-source table with source name, what it provides,
  and a URL or full citation. 16226's Table 2 listed EIA state electricity
  data and specific dataset URLs; 15022 cited the IEA and the Cambridge
  Centre for Alternative Finance.
- The paper's source table must match the workflow's data provenance records.

**Conditional improvement target.** A number attributed to "industry data" or "literature"
with no retrievable source is a provenance failure. Every external constant in
the frozen numbers needs a citable source.

## 5. Treat the required deliverables as first-class model outputs

For HiMCM/ICM the non-modeling deliverables carry real weight and are where
average papers lose points.

- Sensitivity analysis is its own section with real parameter sweeps (15022
  dedicated a full section; 16226 section 9), not a paragraph.
- The extension to a second environmental area is a deliberate choice with a
  stated reason; water is the most common and defensible pick because it is
  thermally coupled to energy consumption.
- Recommendations are split into technical and policy, one is selected and
  actually incorporated into the model with a rerun showing the delta (15502
  section 6.2 "Model Upgrade", 15022 section 7.2).
- The letter to the named body is 1-2 pages, references the body's actual
  report by name (e.g. the UN Advisory Board on AI's "Governing AI for
  Humanity"), uses your frozen findings, and fits the page budget.
- References are real and consistently formatted; the AI Use Report is present
  if AI was used and does not count toward the page limit.

**Conditional improvement target.** Score these against the contest checklist explicitly.
A missing letter, a sensitivity section that is only prose, or a
recommendation that is described but never incorporated into the model is a
hard gap for an award-calibre submission.

## 6. Structure and length

Follow the current contest requirements and use enough space to explain the
model and evidence clearly. A maximum page limit is not a target. Required
letters and reports come from the problem statement, not from these examples.

## 7. Review applicability

Record applicable criteria, evidence and limitations in the review. Use
`not_applicable` with a reason for unrelated examples; do not count them as
failures or successes. Scores of 5 require strong task-specific evidence,
not a particular model family.
