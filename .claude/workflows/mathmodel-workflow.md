---
name: mathmodel-workflow
description: "10-stage evidence-driven workflow for mathematical modeling contests."
---

# MathModel Workflow

Use this workflow when starting or resuming a math modeling contest project.

## Stage machine

```text
S0 PREFLIGHT  → S1 ANALYZE  → S2 ROUTE  → S3 DATA_PLAN
→ S4 METHOD_POC  → S5 EXPERIMENT  → S6 FREEZE
→ S7 WRITE  → S8 RENDER  → S9 AUDIT  → READY
```

## Entry actions

1. Check if a project directory is already open. If not, create one with `my-mathmodel-agent/scripts/init_project.py`.
2. Read `state.json` and `project_manifest.json`.
3. Resume from the current stage.

## Per-stage checklist

### S0 PREFLIGHT
- Confirm problem files exist and are readable.
- Record file hashes and access dates.
- Verify Python / AMPL / Typst / LaTeX availability (run `scripts/doctor.py`).
- Output: `input_manifest.json`.

### S1 ANALYZE
- Invoke `mathmodel-analyst` to decompose subproblems.
- Output: `planning/problem_analysis.json`.

### S2 ROUTE
- Score candidate topics; select baseline/primary/fallback models per subproblem.
- Output: `planning/topic_scores.json`, `methods/model_route.json`.

### S3 DATA_PLAN
- Build data dictionary, cleaning rules, leakage checks, and visualization plan.
- Output: `data_cleaned/data_plan.json`, `figures/visualization_plan.json`.

### S4 METHOD_POC
- Invoke `mathmodel-modeler` for symbols, assumptions, objectives, constraints.
- Implement the smallest runnable PoC.
- Output: `methods/model_design.md`, `code/poc_*.py`.

### S5 EXPERIMENT
- Invoke `mathmodel-coder` to run baseline → primary → ablation → sensitivity → robustness.
- Save run manifests, metrics, logs, tables, figures.
- Output: `results/run_manifest.json`.

### S6 FREEZE
- Verify final experiments; write `frozen_numbers.json` with provenance.
- Every number must have source_file, source_run, subproblem, notes.

### S7 WRITE
- Invoke `mathmodel-writer` to assemble paper from frozen numbers.
- Output: `paper/main.tex` or `paper/main.typ`.

### S8 RENDER
- Compile paper, inspect PDF page by page.
- Output: PDF + `paper/render_log.json`.

### S9 AUDIT
- Invoke `mathmodel-reviewer` for evidence and format audit.
- Output: `audit/final_report.md`.
- Zero hard errors required for READY state.

## Exit actions

1. Update `state.json`.
2. Report current stage, artifacts, evidence, risks, and next entry point.
