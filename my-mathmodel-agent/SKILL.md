---
name: my-mathmodel-agent
description: "Evidence-driven mathematical modeling contest workflow for CUMCM, MCM/ICM, HiMCM, Huawei Cup, and similar events. Use it to decompose a problem, choose and validate model routes, run reproducible Python/AMPL experiments, freeze results, write LaTeX or Typst papers, render them, and audit every claim. Not for casual homework, simple calculations, or one-off coding questions."
metadata:
  short-description: "Run a math-modeling contest from problem files to audited paper"
---

# MathModel Run

Math modeling is not only a modeling problem. Under contest time pressure, it
is a **decision, evidence, and delivery problem**:

- A model looks sophisticated but has no validation path.
- The code runs, but the paper quotes a number from an old run.
- Every subproblem "passes" locally, yet the final PDF has broken figures.
- A reviewer asks why the primary model beats the baseline, and there is no
  reproducible answer.

This skill turns the contest into a stateful, evidence-backed decision workflow. It
borrows the useful harness ideas from `MAGA2010/hackathon-run`: one feature at
a time, default-FAIL contracts, machine-checkable evidence, fresh-context
review, bounded fallback, and an append-only decision log. Evidence is also
classified by strength: a structural check can prove that an artifact exists,
but only a real rerun or inspection can prove that it works.

## Use this skill when

Use it for a contest workspace that contains problem files and needs a
reproducible path to a defensible paper. Invoke it with `$my-mathmodel-agent`.

Do not use it for:

- a single formula or short homework answer;
- a coding request that is unrelated to a contest project;
- changing a paper's wording when no evidence or project state is involved.

## Default user experience

The primary product is not one-click paper generation. The primary product is
help with the next modeling decision: identify the first blocker, compare
routes, run the smallest useful validation, expose weaknesses, and only then
write the affected section.

Unless the user explicitly asks for a complete paper, do not generate one.
Return a bounded work package with:

1. the current blocker;
2. why it blocks later work;
3. the smallest next action;
4. acceptance criteria;
5. the exact fallback if it fails.

Prefer these user-visible outputs over a full draft:

- problem cards;
- model decision cards;
- experiment plans;
- critique reports;
- verified result explanations;
- one section or one figure at a time.

Paper writing is a controlled downstream action. It may consume only verified
and frozen results, and it must not invent missing assumptions, numbers, or
conclusions to make the draft look complete.

## Write and draw incrementally

Do not postpone all figures until the paper is otherwise complete. Treat each
major section as a paired argument: prose states the question and mechanism,
then a figure makes the mechanism or result inspectable. The preferred loop is:

1. State the claim the subsection must establish and identify its source data
   or frozen result.
2. Decide whether a figure materially improves that claim. If yes, write a
   figure specification before drafting surrounding prose: purpose, axes or
   spatial encoding, units, colors, uncertainty, sample size, output path, and
   the sentence that will interpret it.
3. Generate that one figure, complete its standalone scientific and visual
   gate, then insert it into the current paper source with its caption and
   evidence link. Quantitative geometry comes from reproducible code; workflow
   images use AI generation and the separate logic gate below.
4. Compile and inspect the affected page(s) before moving to the next section.
   Check that the actual rendered PDF contains the image, rather than merely
   checking that the source contains a figure command.
5. Continue section by section, reusing the same scenario colors and notation.

This incremental loop is both a writing method and a token-saving rule: do not
re-read the entire paper to add a late batch of figures. Re-open only the
current section, its data/result artifact, and the figure specification. A
figure that cannot be embedded and rendered in the real delivery pipeline is
not counted as completed evidence. If the native editor and fallback renderer
handle assets differently, test both paths and report which PDF is authoritative;
do not claim visual completion from a source-only compile.

For the usual spread-and-impact problem, consider the sequence of one model
workflow/state diagram, one forcing/time-series plot, one spatial snapshot or
heatmap, one horizon summary curve, one sensitivity or ablation plot, and one
component/ranking comparison. Use only the subset that answers real decisions.
Prefer 2-D plots, small multiples, maps, and annotated process diagrams. The
visual target is **clear first, memorable second**: icons may be detailed,
layered, colorful, or mildly dimensional when they create a useful visual
anchor, but every decorative element must support a state, variable, pathway,
or decision. Use a coherent icon family rather than mixing unrelated emoji,
stock symbols, and line-art styles. Keep labels readable after the figure is
reduced to paper-column width, preserve strong contrast, and use vector output
whenever possible. Use 3-D, radar, or polar graphics only when their geometry
represents a model variable that a 2-D view would hide; never add them solely
to make the paper look advanced. A polished figure should have one dominant
visual hierarchy: input, mechanism, comparison, or decision—not all four at
the same visual weight.

Use AI-generated visuals only for conceptual workflow or mechanism schematics.
Final quantitative figures—curves, intervals, heatmaps, rankings, sensitivity,
and tables—should be generated from the saved data with Python or another
reproducible plotting tool. Their default style is restrained and publication
grade: a small consistent palette, clear axes and units, direct labels, vector
or high-resolution output, and no decorative illustration that competes with
the evidence. Avoid glossy gradients, excessive shadows, ornamental scenery,
and fake chart elements in data figures. A quantitative figure may be visually
distinctive, but its visual emphasis must come from the data and annotation.

For figure review, score each candidate on four checks: (1) semantic clarity,
whether a reader can identify the modeled object and relationship; (2) visual
salience, whether the main conclusion is visible within a few seconds; (3)
reduction safety, whether text, icons, and colors survive PDF shrinking and
black-and-white printing; and (4) evidence fidelity, whether every plotted
value and highlighted relationship is traceable to a source or frozen result.
If a beautiful icon competes with the data or makes a schematic look like an
observed measurement, simplify it or label the diagram explicitly as a model
schematic.

## Plan the paper structure and section titles

Before drafting, turn the prompt into a short outline: list each requested
deliverable, identify which model or analysis answers it, and map the answer
to a section. Then inspect a small number of relevant exemplar papers for
organizational patterns. Borrow useful sequencing and levels of detail; do not
copy their headings or methods unless the current work actually uses them.

Use an informative title for the paper and for each section. A paper title
should name the subject and the main modeling or decision contribution. A
section title should tell the reader what problem, method, evidence, or result
it contains. Prefer specific titles such as `Climate-Driven Spatial Spread`
or `Regional Invasive-Plant Impact Index` over vague labels such as `Model`
or decorative titles that conceal the section's purpose. Never name a method
that was not implemented, a result that was not established, or a validation
that was not performed.

Choose a hierarchy that follows the problem's logic, not a fixed universal
template. A useful starting pattern is:

1. Introduction: problem restatement and a brief modeling roadmap.
2. Data, scope, and assumptions: sources, units, coverage, missingness,
   assumptions, and notation, grouped to avoid repeating the same details in
   several chapters.
3. One main section per major question or decision task. For each model, use
   only the subsections needed to explain its purpose and rationale, variables
   and derivation, algorithm or simulation design, output definition, results
   answering the prompt, validation, and relevant sensitivity or limitations.
4. Cross-model comparison or robustness, when it answers a distinct question
   that would be awkward to place under one model alone.
5. Conclusion, references, and any contest-required AI-use statement.

Keep the levels parallel where possible. Separate two ideas when readers need
to find or assess them independently; combine them when splitting would leave
an empty or very short subsection. Do not create headings merely to make the
table of contents look detailed. Conversely, do not hide a substantial method,
result, or validation inside one dense catch-all section. The number and depth
of headings must follow the evidence and the contest's format and page limits.

The project workflow and its evidence links must also be represented in the
paper as required by the `paper_written` contract, using a concise `Workflow`
or `工作流` section or an equivalent clearly labeled figure. Keep this
explanation proportionate; do not let process narration displace the model,
results, or interpretation.

Before writing full prose, check that every prompt deliverable maps to a
section, every proposed heading has enough supported content, the ordering
moves from question to method to evidence to answer, and no heading promises
more than the project can substantiate. Generate the final table of contents
and page numbers from the rendered document rather than maintaining them by
hand.

## Learn from exemplar papers without copying them

When reviewing strong HiMCM or MCM papers, extract decisions rather than
surface style. Record what each borrowed idea accomplishes, what evidence it
needs, and whether the current problem supports it. Keep the following
combined pattern available when it fits the problem:

1. State the problem and scope, then show a workflow from inputs to outputs.
2. Define variables and assumptions before using them in equations.
3. Build a simple baseline that answers the main scale or trend question.
4. Add the primary mechanism model only when it answers a distinct part of the
   prompt; show its states and transitions with a diagram or compact table.
5. Describe the simulation or optimization algorithm in ordered steps so that
   update order, randomness, and stopping rules are reproducible.
6. Report both direct requested outputs and mechanism-oriented outputs when
   they explain the result: for example count, occupied area, distance, or
   risk score rather than one aggregate number alone.
7. Use sensitivity, ablation, resolution, baseline, or held-out checks to
   explain which assumptions control the conclusion.
8. End each major model with an interpretation and a boundary statement: what
   the result supports and what it cannot establish.

This is a menu, not a mandatory recipe. Do not add a Leslie matrix, cellular
automaton, AHP, ANP, TOPSIS, a radar chart, or any other named technique just
because an exemplar uses it. Prefer the simplest route that answers the
question and can be validated. A sophisticated method without an independent
check is weaker than a transparent method with reproducible evidence.

Separate three kinds of evidence in the paper: observed or sourced data,
assumed parameters, and outputs generated by the model. If simulated data are
used for a training or testing demonstration, label them and do not call that
an external validation. A representative run may illustrate a spatial
pattern, but means, intervals, and rankings must come from the declared
replicate set.

## Model-to-figure design

Use the dedicated [data-figure-agent](references/data-figure-agent.md) mode for
substantial results figures and chart revision. Delegate design/implementation
and independent review separately when available. Its job is to select an
encoding for the actual question, compare purposeful alternatives, verify the
estimators, render, and revise until the agreed visual criteria pass. User-
provided outstanding-paper examples are the quality reference, not an award
prediction or a universal layout template. Read the applicable entries in
[exemplar-figure-lessons.md](references/exemplar-figure-lessons.md): learn why
the design was chosen, its data prerequisites, and what should change on a new
problem. Do not keep producing a default chart when feedback shows it fails to
express the argument.

For conceptual workflow/model diagrams, use AI image generation by default as
the user requested. Follow [ai-workflow-gate.md](references/ai-workflow-gate.md):
freeze implemented nodes, labels, and edges first; inspect every rendered label
and arrow against the specification; independently review the final-size image.
AI-generated quantitative axes, marks, measurements, or unimplemented methods
are not accepted. Preserve the preferred AI visual style while correcting logic.

Use the per-figure [review template](templates/figure-review.json) and
`scripts/figure_gate.py`: `seal` binds declared data/model, specification,
code/helper, caption and exact outputs and resets reviews to pending; `check`
blocks absent files, pending reviews, unresolved hard defects and stale hashes.
Scientific and visual review must both pass. The machine validates the records,
not the truth of the model or aesthetic quality. A standalone pass permits
preview and insertion; final paper acceptance requires `scope=paper` and the
actual rendered page. Treat changed placement or artifacts as requiring review.

Choose figures by argument: conceptual figures explain logic, quantitative
figures establish results, and validation figures establish the strength and
limits of the evidence. Assess beauty, presentation ability, and modeling
maturity separately; beauty is not evidence of a good model. Read the figure
catalog for the selection matrix and exemplar-derived design checks. Select
the smallest complementary set supported by available data, not a fixed quota.

Plan figures together with the model route. Use a workflow or state diagram
for structure, a map or spatial small multiple for geometry, a time series for
temporal forcing or growth, a distribution or interval plot for stochastic
outcomes, and a sensitivity or ablation plot for robustness. Every figure must
answer a stated question and identify its units, sample size or replicate
count, and uncertainty meaning. Use the same colors for the same states or
scenarios throughout the paper.

For the reusable figure catalog and visual examples, read
[references/figure-catalog.md](references/figure-catalog.md) when planning a
paper or reviewing exemplar figures. It distinguishes competition-useful
advanced charts from decoration and includes the local SVG reference sheet at
`assets/figure-type-icons.svg`.

For Python data figures, also read
[references/python-figures.md](references/python-figures.md). It combines
reviewed GitHub scientific-visualization, Matplotlib, and Seaborn skills with
contest-specific layout recipes and actual rendered-image review. Before
coding, write a compact figure design card: question, data fields, panel
relationship, scales, interval meaning, final width, and one useful annotation.
For a substantial results section, consider a complementary composition such
as fit plus residuals, spatial snapshots plus aggregate statistics, or score
components plus normalization and weight sensitivity. Select complexity from
the evidence; do not substitute a larger title or more colors for more insight.

Use `scripts/figure_tools.py` for scoped styles, readable coincident markers,
annotated matrices, supplied intervals, and fixed-size PNG/PDF/SVG export with
data hashes. Adapt its functions to the figure rather than forcing every plot
into one layout. Use native Matplotlib axes for quantitative charts; manually
drawing ticks and positions in a document canvas is not a scientific-plotting
fallback. Resolve runtime/font problems before exporting. A style library
alone does not repair wrong scales, unsupported intervals, or a weak argument.

Inspect the actual exported image at its intended manuscript width. Record
visible elements first, then check scientific meaning, readability, visual
hierarchy, and comparison efficiency. Fix an identified defect and inspect
again; stop when the requested criteria are met. Successful code execution or
a mechanically clean export does not establish visual quality. During an
existing-figure update, overwrite the requested active image and companion
vector files so the user's original link shows the corrected figure.

When the user requests Nature-style figures, read
[references/nature-figures.md](references/nature-figures.md). Use a primary
evidence panel and purposeful supporting views when the argument benefits from
unequal sizes. Use `nature_style`, `nature_panel_title`, and
`check_panel_alignment` from the plotting helpers; measure final drawn axes in
physical points. A community Nature-inspired skill supplies design guidance,
not proof of journal acceptance. Keep typography suited to the contest paper.

For a stochastic spatial model, aim to show both the process and the summary:
one or more time-point snapshots plus count, area, distance, or occupancy
statistics. For a scoring model, show the indicator definition, normalization
or weighting path, component values, and final ranking. Do not use a 3D, radar,
or polar chart unless its geometry represents a real variable in the model.
Do not select one run because it looks attractive and present it as typical;
label it as illustrative and keep inferential claims tied to aggregate runs.

Before accepting a paper outline, perform a content audit: each heading must
contain enough supported material, each major claim must have a number, table,
figure, source, or validation record, and every figure must have a sentence in
the text explaining the decision it supports. Page count is a consequence of
this complete argument. Never increase it by empty headings, repeated prose,
or decorative graphics.

## Choose the operating mode

| Mode | Use when | First action |
|---|---|---|
| `SETUP` | New contest folder | Run `init_project.py`, then verify inputs |
| `RUN` | Existing project needs to advance | Read `state.json`, find the first false gate |
| `REVIEW` | A stage claims to be complete | Independently reproduce the evidence |
| `RECOVER` | A model, run, number, or PDF failed | Return to the earliest invalid gate |
| `DELIVER` | Paper is rendered | Run the final acceptance audit |

Never skip from a plan to a polished paper. The only valid path is through
validated methods, reproducible experiments, frozen numbers, and audit.

The evidence gates establish defensible work. For stronger work, select the
problem-type criteria in [references/exemplar-benchmark.md](references/exemplar-benchmark.md).
These are improvement targets, not an award guarantee. Energy-paper examples
must not become universal requirements for optimization, evaluation or simulation.

## Practice and improvement

When the user asks for training, timed practice, or a post-practice review, use
[references/practice-loop.md](references/practice-loop.md). Practice improves
saved instructions, tools and evaluation evidence; it does not update model weights.
Keep mathematical modeling guidance local to this skill and contest projects.
A bounded exercise uses only relevant stage artifacts; it does not require a
full paper or all ten gates. Never mark the full project READY from a partial drill.

## Startup ritual

Before acting on a project:

1. Read `state.json`, `project_manifest.json`, and `PROGRESS.md`.
2. Read the current stage artifact and its upstream evidence.
3. Run `python3 my-mathmodel-agent/scripts/status.py <project>`.
4. Identify the first gate whose value is `false`.
5. Work only on that gate, or record why a fallback is required.
6. At the end, update the state, progress log, decision log, and evidence map.
7. If an artifact was changed, invalidate downstream gates whose inputs changed;
   never preserve a stale `true` gate just because the file still exists.

If the project directory is new, scaffold it with:

```bash
python3 my-mathmodel-agent/scripts/init_project.py <project-name>
```

If the environment is uncertain, run:

```bash
python3 my-mathmodel-agent/scripts/doctor.py
```

## Stage machine

```text
S0 PREFLIGHT
  input_manifest
      |
      v
S1 ANALYZE
  problem_analysis.json
      |
      v
S2 ROUTE
  model_route.json
      |
      v
S3 DATA_PLAN
  data_plan.json + visualization_plan.json
      |
      v
S4 METHOD_POC
  method_validation.json + runnable PoC
      |
      v
S5 EXPERIMENT
  run_manifest.json + metrics + logs + figures
      |
      v
S6 FREEZE
  frozen_numbers.json
      |
      v
S7 WRITE
  paper + evidence_map.json
      |
      v
S8 RENDER
  PDF + render_log.json
      |
      v
S9 AUDIT
  audit/final_report.md
      |
      v
READY
```

The detailed rules for each stage are in
[references/workflow-contract.md](references/workflow-contract.md). Read the
stage section you are executing, not the entire document by default.

## Default-FAIL contract

Every subproblem and model route starts with `passes: false`.

A gate changes to `true` only when its acceptance criteria have
machine-checkable evidence. Evidence is one of:

- `command`: the exact command and exit result;
- `test`: an automated check with a pass/fail result;
- `data`: a source file, row count, hash, or schema check;
- `figure`: a generated figure plus the script that produced it;
- `log`: a run log that records parameters, seed, environment, and output;
- `manual`: visual inspection or a human decision, with the inspected path.

Evidence has three levels:

- `STRUCTURAL`: JSON/schema/path/hash checks; this proves organization only.
- `RUNTIME`: a fresh rerun from saved inputs, with exit status, metrics, output
  hashes, and environment recorded.
- `VISUAL`: an actual rendered artifact inspected page-by-page or frame-by-frame.

`STRUCTURAL` evidence alone can never open `method_validated`,
`experiments_reproduced`, `pdf_verified`, or `audit_passed`. A fallback or
degraded toolchain must be named and cannot be described as submission-ready
without the required runtime and visual checks.

The generator may propose evidence. The independent reviewer must reproduce
it. A claim such as "the model works" or "the fit is good" is not evidence.

## Role split

Use separate contexts whenever the environment supports them:

| Role | Owns | Must not do |
|---|---|---|
| Orchestrator | state, gates, handoff, blockers | mark its own work passing |
| Analyst / modeler | problem cards and model routes | edit final paper numbers |
| Coder | reproducible experiments and logs | declare a result frozen |
| Writer | paper and evidence map | use numbers outside `frozen_numbers.json` |
| Reviewer | independent reproduction and audit | "fix" the artifact being reviewed |

For Codex, stay in the current context but explicitly switch roles. For
Claude Code, the mirrored agents live under `.claude/agents/`.

## Required artifacts

| Artifact | Purpose | Default |
|---|---|---|
| `input_manifest.json` | Problem-file inventory and hashes | incomplete |
| `planning/problem_analysis.json` | One default-FAIL task card per subproblem | all gates false |
| `methods/model_route.json` | Baseline, primary, fallback, validation plan | all gates false |
| `data_cleaned/data_plan.json` | Fields, units, cleaning, leakage checks | incomplete |
| `figures/visualization_plan.json` | Figure purpose, source, script, destination | incomplete |
| `methods/method_validation.json` | Smallest runnable PoC and its evidence | pending |
| `results/run_manifest.json` | Reproducible run records | pending |
| `frozen_numbers.json` | Final numbers with provenance | no values |
| `paper/evidence_map.json` | Claim -> number/figure/run mapping | incomplete |
| `paper/workflow.json` | Paper workflow steps, inputs, outputs, and evidence links | incomplete |
| `paper/render_log.json` | Compilation and page inspection | incomplete |
| `audit/gate_evidence.json` | Evidence behind every state gate | empty |
| `audit/final_report.md` | Final independent review | absent |
| `audit/package_manifest.json` | Submission inventory, hashes, and exclusions | absent until delivery |
| `planning/decision_log.jsonl` | KEEP/CUT/DEFER/PIVOT decisions | empty |
| `PROGRESS.md` | Durable handoff log across fresh contexts | initialized |

Machine-readable contract details are in
[references/artifact-contracts.md](references/artifact-contracts.md).

## Evidence gates

The state gates are intentionally conservative:

```text
input_snapshot
problem_decomposed
model_route_selected
data_plan_ready
method_validated
experiments_reproduced
results_frozen
paper_written
pdf_verified
audit_passed
```

`READY` requires all ten gates to be `true`, `audit/final_report.md` to contain
zero hard errors, and `audit/package_manifest.json` to identify the exact
deliverable files and hashes. A successful solver exit is not sufficient. A
compiled PDF is not sufficient. A plausible explanation is not sufficient.
If the PDF was produced by a fallback renderer, `READY` remains false until
the fallback is explicitly allowed by the contest format and independently
checked as submission-compliant.

Every paper must contain a clearly labeled `Workflow` or `工作流` section (or
an equivalent workflow figure) and a matching `paper/workflow.json`. The JSON
must list the ordered path from problem snapshot through audit, with each step
identifying its input, output, evidence, and paper location. A workflow file
that is not represented in the paper does not satisfy `paper_written`.

## Recovery rules

Return to the earliest invalid gate:

| Failure | Return to |
|---|---|
| Question misunderstood or data scope wrong | S1 |
| Primary model cannot be justified | S2 |
| Data leakage, missing fields, bad units | S3 |
| PoC does not run or baseline comparison is invalid | S4 |
| Code, solver status, metrics, or seed unreliable | S5 |
| Paper number lacks provenance or run changed | S6 |
| Claim, figure, or citation does not match evidence | S7 |
| Compile error, overflow, missing figure, bad encoding | S8 |
| Hard error in audit | earliest failed gate |

When a primary route fails, use the recorded fallback. Do not silently replace
the model or rewrite acceptance criteria to make it pass. Record the decision
in `planning/decision_log.jsonl`.

## Commands

```bash
# create a contest workspace
python3 my-mathmodel-agent/scripts/init_project.py 2026-cumcm-a

# show current stage, false gates, and next action
python3 my-mathmodel-agent/scripts/status.py 2026-cumcm-a

# inspect local tooling
python3 my-mathmodel-agent/scripts/doctor.py

# freeze a verified result file with provenance
python3 my-mathmodel-agent/scripts/freeze_numbers.py \
  results/verified_results.json --output 2026-cumcm-a/frozen_numbers.json

# independent final audit
python3 my-mathmodel-agent/scripts/audit_workspace.py 2026-cumcm-a
```

The start page and human-facing map are in `../../index.html`. They explain
the workflow without replacing the machine contracts above.

## Completion behavior

Report:

- current stage and gate status;
- artifacts created or changed;
- evidence reproduced;
- unresolved risks or blockers;
- the exact next entry point.

Do not say "done", "paper finished", or "results final" unless the relevant
gates are true and the evidence exists at the paths named above.

## Reference routing

- Read [references/workflow-contract.md](references/workflow-contract.md) when
  executing or reviewing a stage.
- Read [references/artifact-contracts.md](references/artifact-contracts.md)
  when creating, editing, or validating state files.
- Read [references/evaluation-rubric.md](references/evaluation-rubric.md) when
  acting as the independent reviewer or preparing the final submission.
- Read [references/exemplar-benchmark.md](references/exemplar-benchmark.md) at
  S2–S5 and during quality review; select only criteria applicable to the task.
- Read [references/practice-loop.md](references/practice-loop.md) for training,
  timed drills, failure review, and transfer checks on unseen problems.
- Read [references/python-figures.md](references/python-figures.md) when
  creating or upgrading quantitative Python figures. Read only the applicable
  composition recipe, then inspect the rendered output.
- Read [references/data-figure-agent.md](references/data-figure-agent.md) for
  substantial data-chart work, and the applicable entries in
  [references/exemplar-figure-lessons.md](references/exemplar-figure-lessons.md)
  for transfer from user reference figures.
- Read [references/ai-workflow-gate.md](references/ai-workflow-gate.md) for AI
  workflow and mechanism images; use the figure review gate before acceptance.

Update requested files at their existing active paths, incorporating current
user changes. Keep the discoverable SKILL.md consistent with its references so
the next invocation uses the update. Create numbered alternatives only when
the user explicitly requests versions; use Final only after acceptance. Keep
historical skill snapshots outside active skill discovery and never claim that
a missing historical version has been recovered.
