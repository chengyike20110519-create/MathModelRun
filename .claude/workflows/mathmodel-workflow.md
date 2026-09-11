---
name: mathmodel-workflow
description: "10-stage, 10-gate evidence-driven workflow for mathematical modeling contests. Every gate starts false; a gate becomes true only when machine-checkable evidence exists."
---

# MathModel Workflow

Use this workflow when starting or resuming a math modeling contest project.

## Default-FAIL contract

Every subproblem and model route starts with `passes: false`. A gate
changes to `true` only after its acceptance criteria have machine-checkable
evidence (command, test, data, figure, log, or manual-inspection). A
claim such as "the model works" is not evidence.

## Stage machine

```text
S0 PREFLIGHT  -> S1 ANALYZE  -> S2 ROUTE  -> S3 DATA_PLAN
-> S4 METHOD_POC  -> S5 EXPERIMENT  -> S6 FREEZE
-> S7 WRITE  -> S8 RENDER  -> S9 AUDIT  -> READY
```

## Entry actions

1. Check if a project directory is already open. If not, create one with `my-mathmodel-agent/scripts/init_project.py`.
2. Read `state.json` and `project_manifest.json`.
3. Run `python3 my-mathmodel-agent/scripts/status.py <project>` to find the first false gate.
4. Resume from that gate.

## Per-stage checklist

### S0 PREFLIGHT
- Read and hash every problem file and attachment.
- Record access dates and sizes.
- Run `python3 my-mathmodel-agent/scripts/doctor.py` to check Python, numpy, scipy, pandas, matplotlib, typst, latexmk, pandoc.
- Output: `input_manifest.json`.
- Gate: `input_snapshot` - all problem files hashed and accessible.

### S1 ANALYZE
- Invoke `mathmodel-analyst` to decompose subproblems into task cards with research object, decision variables, input fields, output form, hard constraints, soft objectives, evaluation metrics, and attachment deps.
- Output: `planning/problem_analysis.json`.
- Gate: `problem_decomposed` - every subproblem has a task card with acceptance criteria.

### S2 ROUTE
- For each subproblem, define: baseline (simple), primary (best trade-off), fallback (when primary fails), rejected alternatives with reasons.
- Record validation plan (minimal PoC, sensitivity, robustness).
- Output: `methods/model_route.json` with all gates initially false.
- Gate: `model_route_selected` - baseline, primary, fallback defined with rejection reasons and validation plan.

### S3 DATA_PLAN
- Build data dictionary, cleaning rules, unit conversions, imputation strategy, and time-series leakage checks.
- Plan every figure: purpose, source data, script, destination file.
- Output: `data_cleaned/data_plan.json`, `figures/visualization_plan.json`.
- Gate: `data_plan_ready` - fields traced, units consistent, no leakage, every figure has source and script.

### S4 METHOD_POC
- Invoke `mathmodel-modeler` for symbol tables, assumptions, objectives, constraints, and algorithm outline.
- Implement the smallest runnable PoC that proves the math maps to code. Record command, log, and pass/fail.
- Output: `methods/method_validation.json` + `code/poc_*.py`.
- Gate: `method_validated` - PoC runs, produces expected output, math and code agree.

### S5 EXPERIMENT
- Invoke `mathmodel-coder` to run in order: baseline, primary, ablation, sensitivity, robustness.
- Each run records: run_id, parameters, seed, input hash, environment, log, metrics, output files.
- Save run manifests, metrics, logs, tables, and figures.
- Output: `results/run_manifest.json` + `runs/*` + `figures/*`.
- Gate: `experiments_reproduced` - all planned runs complete with reproducible command, seed, and input hash.

### S6 FREEZE
- Write `frozen_numbers.json` with seven fields per entry: `name`, `value`, `unit`, `source_file`, `source_run`, `subproblem`, `notes`.
- Paper numbers may ONLY come from this file. If code, parameters, seed, or data change, old frozen values are immediately invalid.
- Gate: `results_frozen` - every frozen entry has all seven fields and matches a run in `run_manifest.json`.

### S7 WRITE
- Invoke `mathmodel-writer` to assemble paper ONLY from frozen numbers and evidence-map entries.
- Every claim maps through `paper/evidence_map.json` to a frozen value, figure, or run.
- Output: `paper/main.tex` or `paper/main.typ` + `paper/evidence_map.json`.
- Gate: `paper_written` - every number traces to `frozen_numbers.json`, every figure has script and data source.

### S8 RENDER
- Compile PDF with typst or latexmk. Inspect page by page for overflow, blank pages, missing figures, broken cross-references, encoding errors.
- Output: PDF + `paper/render_log.json`.
- Gate: `pdf_verified` - zero compile errors, all pages checked, figures numbered and captioned.

### S9 AUDIT
- Invoke `mathmodel-reviewer` for independent audit: reproduce at least three key commands, trace frozen numbers back to code, verify every gate in `audit/gate_evidence.json`, score with the rubric in `references/evaluation-rubric.md`.
- Output: `audit/acceptance.json` + `audit/final_report.md`.
- Zero hard errors required for READY state.
- Gate: `audit_passed` - acceptance.json passes rubric, final_report.md has zero hard errors.

## Exit actions

1. Update `state.json` with current gate values.
2. Append decision to `planning/decision_log.jsonl` (KEEP/CUT/DEFER/PIVOT/ACCEPT_RISK).
3. Report current stage, artifacts, evidence, risks, and next entry point.

## Recovery

Return to the earliest invalid gate:

| Failure | Return to |
|---|---|
| Question misunderstood or data scope wrong | S1 |
| Primary model cannot be justified | S2 |
| Data leakage, missing fields, bad units | S3 |
| PoC does not run or baseline comparison invalid | S4 |
| Code, solver status, metrics, or seed unreliable | S5 |
| Paper number lacks provenance or run changed | S6 |
| Claim, figure, or citation does not match evidence | S7 |
| Compile error, overflow, missing figure, bad encoding | S8 |
| Hard error in audit | earliest failed gate |

When a primary route fails, use the recorded fallback. Do not silently replace the model or rewrite acceptance criteria.

When updating a user-requested file, replace the current version at its original path and remove obsolete content or duplicate old versions.
