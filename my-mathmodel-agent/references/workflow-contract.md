# Workflow contract

## Required project files

```text
problem_files/ planning/ methods/ code/ data_cleaned/ results/
figures/ paper/ audit/ state.json project_manifest.json frozen_numbers.json
```

## Gate contracts

| Gate | Evidence required |
|---|---|
| S0 | readable input files, input manifest, hash snapshot |
| S1 | each subproblem has input/output/task type/constraints |
| S2 | score table, baseline/primary/fallback and rejection reason |
| S3 | field definitions, units, cleaning rules, figure plan |
| S4 | runnable PoC, assumptions, equations, validation result |
| S5 | run manifest, logs, metrics, constraint checks, generated figures |
| S6 | frozen numbers with source paths and run identifiers |
| S7 | paper outline, section-to-evidence map, figure/table index |
| S8 | successful LaTeX or Typst render and visual inspection |
| S9 | evidence audit and format audit, no hard errors |

## Number provenance

Each frozen value should include `name`, `value`, `unit`, `source_file`, `source_run`, `subproblem`, and `notes`. Never copy a number from an earlier chat message without a file source.

## Model route record

Each subproblem record should include: `task_type`, `role`, `baseline`, `primary_model`, `fallback_model`, `rejection_reason`, `validation`, `required_figures`, and `paper_section`.

## AMPL invariant

Keep model structure in `.mod`, data in `.dat`, orchestration in Python, and close independent AMPL sessions. Report solver status only after checking `solve_result`, objective value, variable bounds, and constraint violations.

## Automation

Run `scripts/freeze_numbers.py results/model_results.json --output frozen_numbers.json` only after the final experiment is verified. Run `scripts/audit_workspace.py <project>` before delivery; a nonzero exit means the project is not ready.
