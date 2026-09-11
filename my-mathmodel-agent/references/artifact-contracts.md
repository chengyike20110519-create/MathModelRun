# Artifact contracts

The project state is stored in JSON so another fresh agent can resume without
reading the previous conversation. Keep these files valid even while work is
incomplete; use `false`, `pending`, or empty arrays rather than prose that
cannot be checked.

## Shared evidence object

Every `evidence` item uses:

```json
{
  "kind": "command",
  "value": "python3 code/poc_q1.py -> exit 0; MAE=0.42",
  "path": "results/poc_q1.log",
  "at": "2026-09-10T12:00:00Z"
}
```

Allowed `kind` values:

| Kind | Required meaning |
|---|---|
| `command` | Exact command and observed exit/result |
| `test` | Automated test and pass/fail result |
| `data` | Source, schema, row count, or hash check |
| `figure` | Figure path plus generating script |
| `log` | Reproducible run log with parameters and environment |
| `manual` | Human inspection with the inspected path |

`value` must be concrete. Do not write "looks correct", "passed", or "good
fit" without the command, path, metric, or decision rule that supports it.

## `state.json`

Required top-level fields:

- `schema_version`
- `project_name`
- `contest`
- `paper_format`
- `stage`
- `status`
- `next_action`
- `gates`
- `budget`
- `updated_at`

Required gate keys:

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

All gates start `false`. `READY` requires all of them to be `true`.

`stage` records the stage currently being advanced, using the imperative
S-stage names `PREFLIGHT`, `ANALYZE`, `ROUTE`, `DATA_PLAN`, `METHOD_POC`,
`EXPERIMENT`, `FREEZE`, `WRITE`, `RENDER`, `AUDIT`, then `READY`. It is the
stage in progress, not the last completed stage. The declared stage must never
be ahead of the first gate that is still `false`: `PREFLIGHT` binds to
`input_snapshot`, `ANALYZE` to `problem_decomposed`, and so on in gate order.
`audit_workspace.py` treats a stage that is ahead of the gates as a hard
issue.

`next_action` is a hand-maintained hint. `status.py` derives the authoritative
next action from the first `false` gate and reports when the declared
`next_action` has drifted from it.

## `input_manifest.json`

```json
{
  "generated_at": null,
  "files": [
    {
      "path": "problem_files/problem.pdf",
      "kind": "problem",
      "sha256": null,
      "readable": false,
      "notes": ""
    }
  ],
  "environment": {
    "python": null,
    "latex": null,
    "typst": null,
    "solvers": []
  }
}
```

Every file gets a path, kind, hash, readability state, and note. Add external
data sources to the same manifest or to a `sources` array with URL, access
date, license, and retrieval method.

## `planning/problem_analysis.json`

```json
{
  "schema_version": "2.0",
  "generated_at": null,
  "subproblems": [
    {
      "id": "Q1",
      "question": "",
      "deliverable": "",
      "role": "main",
      "task_type": "prediction",
      "inputs": [],
      "outputs": [],
      "hard_constraints": [],
      "soft_objectives": [],
      "metrics": [],
      "attachment_dependencies": [],
      "facts": [],
      "assumptions": [],
      "ambiguities": [],
      "out_of_scope": [],
      "acceptance_criteria": [],
      "passes": false,
      "evidence": []
    }
  ]
}
```

`acceptance_criteria` must be observable. Good examples:

- "The fitted curve is compared with at least one transparent baseline."
- "The optimization result reports feasibility, objective, and maximum
  constraint violation."
- "The forecast uses only data available before the prediction date."

Bad examples:

- "The model is accurate."
- "The answer is reasonable."
- "The paper looks complete."

## `methods/model_route.json`

```json
{
  "schema_version": "2.0",
  "generated_at": null,
  "subproblems": [
    {
      "id": "Q1",
      "baseline": "",
      "primary_model": "",
      "fallback_model": "",
      "rejected": [
        {
          "model": "",
          "reason": ""
        }
      ],
      "selection_evidence": [],
      "validation_plan": [],
      "required_figures": [],
      "paper_section": "",
      "acceptance_criteria": [],
      "passes": false,
      "evidence": []
    }
  ]
}
```

Complexity is not evidence. A primary model stays only if its comparison with
the baseline can be reproduced.

## `data_cleaned/data_plan.json`

```json
{
  "schema_version": "2.0",
  "generated_at": null,
  "fields": [
    {
      "name": "",
      "type": "float",
      "unit": "",
      "source": "",
      "range": null,
      "missing_code": null,
      "notes": ""
    }
  ],
  "cleaning_rules": [],
  "leakage_checks": [],
  "split_plan": {
    "train": "",
    "validation": "",
    "test": ""
  },
  "external_sources": []
}
```

For non-prediction tasks, `split_plan` may be `null`, but the reason must be
recorded in `leakage_checks`.

## `figures/visualization_plan.json`

```json
{
  "schema_version": "2.0",
  "figures": [
    {
      "id": "fig-q1-fit",
      "purpose": "Compare baseline and primary models.",
      "source": "results/metrics.json",
      "script": "code/make_figures.py",
      "output": "figures/q1_fit.png",
      "paper_section": "results",
      "acceptance_criteria": [
        "Axes have units.",
        "Baseline and primary are visually distinguishable."
      ],
      "passes": false,
      "evidence": []
    }
  ]
}
```

## `methods/method_validation.json`

```json
{
  "schema_version": "2.0",
  "generated_at": null,
  "subproblem": "Q1",
  "symbols": [],
  "assumptions": [],
  "objective": "",
  "constraints": [],
  "algorithm": "",
  "poc": {
    "command": "",
    "input": "",
    "output": "",
    "duration_seconds": null
  },
  "baseline_comparison": {
    "baseline": "",
    "primary": "",
    "metric": "",
    "baseline_value": null,
    "primary_value": null
  },
  "status": "pending",
  "passes": false,
  "evidence": []
}
```

`status` is one of `pending`, `pass`, `fail`, `blocked`.

## `results/run_manifest.json`

```json
{
  "schema_version": "2.0",
  "runs": [
    {
      "run_id": "run-001",
      "subproblem": "Q1",
      "stage": "baseline",
      "command": "",
      "input_files": [],
      "input_sha256": [],
      "parameters": {},
      "seed": null,
      "environment": {},
      "started_at": null,
      "finished_at": null,
      "status": "pending",
      "metrics": {},
      "outputs": [],
      "warnings": [],
      "evidence": []
    }
  ]
}
```

`stage` is one of `baseline`, `primary`, `ablation`, `sensitivity`,
`robustness`, or `derived`.

## `frozen_numbers.json`

```json
{
  "schema_version": "2.0",
  "frozen_at": null,
  "source_file": null,
  "source_sha256": null,
  "values": [
    {
      "name": "",
      "value": null,
      "unit": "",
      "source_file": "",
      "source_run": "",
      "subproblem": "",
      "notes": ""
    }
  ]
}
```

Do not freeze an empty list at delivery. A valid `READY` project has at least
one frozen value for every quantitative claim in the paper.

When the `results_frozen` gate is `true`, `audit_workspace.py` also checks
that every `source_run` is registered in `results/run_manifest.json` and that
every `source_file` exists in the workspace.

## `paper/evidence_map.json`

```json
{
  "schema_version": "2.0",
  "claims": [
    {
      "claim_id": "claim-q1-main",
      "claim": "",
      "paper_location": "results-q1",
      "evidence": [
        {
          "kind": "data",
          "value": "frozen_numbers.json#CO2_2021",
          "path": "frozen_numbers.json",
          "at": null
        }
      ],
      "passes": false
    }
  ],
  "figures": [],
  "tables": []
}
```

`paper_location` can be a section, label, or line reference. It must let a
fresh reviewer find the claim quickly.

When the `paper_written` gate is `true`, `audit_workspace.py` checks that
`claims` is non-empty, that every claim has at least one evidence entry, and
that any `frozen_numbers.json#<name>` reference resolves to a frozen value
that actually exists.

## `paper/render_log.json`

```json
{
  "schema_version": "2.0",
  "format": "latex",
  "compile_command": "",
  "status": "pending",
  "pdf": "paper/main.pdf",
  "page_count": 0,
  "pages": [
    {
      "page": 1,
      "checked": false,
      "issues": [],
      "evidence": []
    }
  ],
  "hard_errors": [],
  "warnings": []
}
```

Every page needs a `checked` value. Overflow, blank pages, missing figures,
broken references, encoding failures, and submission-template violations are
hard errors.

## `audit/gate_evidence.json`

```json
{
  "schema_version": "2.0",
  "gates": {
    "input_snapshot": [],
    "problem_decomposed": [],
    "model_route_selected": [],
    "data_plan_ready": [],
    "method_validated": [],
    "experiments_reproduced": [],
    "results_frozen": [],
    "paper_written": [],
    "pdf_verified": [],
    "audit_passed": []
  }
}
```

Every gate value is an evidence array. `state.json` should only set a gate to
`true` when the matching array is non-empty and the reviewer can reproduce it.

Each entry must be a valid evidence object (see Shared evidence object above):
`kind` must be one of the six allowed values, `value` must be a non-empty
string, and if `path` is present the file must exist in the workspace.
`audit_workspace.py` rejects entries with an invalid `kind`, a blank
`value`, or a `path` that does not exist.

## `planning/decision_log.jsonl`

One JSON object per line:

```json
{"at":"2026-09-10T12:00:00Z","subject":"Q2-primary-model","classification":"PIVOT","rationale":"The primary route cannot meet the hard time constraint.","author":"analyst","relates_to":"methods/model_route.json"}
```

The file is append-only. Correct a prior decision by adding a new record, not
by editing history. `audit_workspace.py` validates every line: it must be a
JSON object with a non-empty `at` timestamp, a non-empty `subject`, and a
`classification` of `KEEP`, `CUT`, `DEFER`, `PIVOT`, or `ACCEPT_RISK`.

## `audit/final_report.md`

The final report must contain:

1. Overall verdict: `PASS` or `FAIL`.
2. Hard errors and their return stage.
3. Soft risks and whether they are accepted.
4. Evidence reproduced.
5. Unverified claims.
6. Gate-by-gate result.
7. Final submission readiness.

A report with unverified claims cannot be `PASS`.
