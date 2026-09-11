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

This skill turns the contest into a stateful, evidence-backed pipeline. It
borrows the useful harness ideas from `MAGA2010/hackathon-run`: one feature at
a time, default-FAIL contracts, machine-checkable evidence, fresh-context
review, bounded fallback, and an append-only decision log.

## Use this skill when

Use it for a contest workspace that contains problem files and needs a
reproducible path to a defensible paper. Invoke it with `$my-mathmodel-agent`.

Do not use it for:

- a single formula or short homework answer;
- a coding request that is unrelated to a contest project;
- changing a paper's wording when no evidence or project state is involved.

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

## Startup ritual

Before acting on a project:

1. Read `state.json`, `project_manifest.json`, and `PROGRESS.md`.
2. Read the current stage artifact and its upstream evidence.
3. Run `python3 my-mathmodel-agent/scripts/status.py <project>`.
4. Identify the first gate whose value is `false`.
5. Work only on that gate, or record why a fallback is required.
6. At the end, update the state, progress log, decision log, and evidence map.

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
| `paper/render_log.json` | Compilation and page inspection | incomplete |
| `audit/gate_evidence.json` | Evidence behind every state gate | empty |
| `audit/final_report.md` | Final independent review | absent |
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

`READY` requires all ten gates to be `true` and `audit/final_report.md` to
contain zero hard errors. A successful solver exit is not sufficient. A
compiled PDF is not sufficient. A plausible explanation is not sufficient.

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

Keep the project's original files in place when updating them. Replace the
current version at the same path, remove obsolete content, and do not leave
older `v1`, `v2`, or backup copies unless the user explicitly requests them.
