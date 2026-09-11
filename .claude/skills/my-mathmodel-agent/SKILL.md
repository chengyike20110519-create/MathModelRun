---
name: my-mathmodel-agent
description: "Evidence-driven mathematical modeling contest workflow for Claude Code: decompose a problem, select baseline/primary/fallback model routes, validate PoCs, run reproducible Python/AMPL experiments, freeze results, write LaTeX or Typst papers, render, and audit every claim. Use for CUMCM, MCM/ICM, HiMCM, and similar contests; not for casual homework or one-off coding questions."
---

# MathModel Run

Use this skill when working on Chinese or international mathematical modeling contest projects that need a reproducible path from problem files to a defensible paper.

This is the Claude Code skill entry point. For Codex, use `my-mathmodel-agent/SKILL.md` in the repository root.

## Startup ritual

1. Read `state.json`, `project_manifest.json`, and `PROGRESS.md`.
2. Find the first gate whose value is `false`.
3. Read only the stage contract needed for that gate.
4. Work on one gate at a time and update the durable handoff log.

## Stage machine

```text
S0 PREFLIGHT  → S1 ANALYZE  → S2 ROUTE  → S3 DATA_PLAN
→ S4 METHOD_POC  → S5 EXPERIMENT  → S6 FREEZE
→ S7 WRITE  → S8 RENDER  → S9 AUDIT  → READY
```

The required state gates are:

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

Every gate starts `false`. A gate becomes `true` only after independent, reproducible evidence exists in `audit/gate_evidence.json`.

## Core contracts

- Each subproblem gets `planning/problem_analysis.json` with observable acceptance criteria.
- Each model route records `baseline`, `primary_model`, `fallback_model`, rejected alternatives, and a validation plan.
- Each experiment run records command, input hash, parameters, seed, environment, metrics, logs, and outputs.
- Paper numbers may only come from `frozen_numbers.json`.
- Each paper claim maps through `paper/evidence_map.json` to a frozen value, figure, or run.
- Every PDF page is checked in `paper/render_log.json`.
- Final readiness requires zero hard errors in `audit/final_report.md`.

## Role subagents

Invoke the role agents under `.claude/agents/`:

- `mathmodel-analyst`: decompose problem facts, assumptions, ambiguities, and acceptance criteria.
- `mathmodel-modeler`: define symbols, assumptions, objectives, constraints, and model routes.
- `mathmodel-coder`: implement reproducible experiments and logs.
- `mathmodel-writer`: assemble the paper only from frozen evidence.
- `mathmodel-reviewer`: independently reproduce evidence and audit the project.

## Recovery

Return to the earliest invalid gate:

- question or data scope → S1
- model route → S2
- data leakage or units → S3
- PoC → S4
- experiment or solver status → S5
- numbers → S6
- claim or evidence mismatch → S7
- compile or layout → S8

Use the recorded fallback instead of silently changing the model. Append KEEP/CUT/DEFER/PIVOT/ACCEPT_RISK decisions to `planning/decision_log.jsonl`.

## Completion behavior

Do not claim completion because code ran, a solver returned success, or a PDF compiled. Report stage, artifacts, reproduced evidence, risks, and next entry point. Completion requires all gates true and a final independent audit with zero hard errors.

For detailed stage instructions, read `my-mathmodel-agent/references/workflow-contract.md`. For machine-readable JSON shapes, read `my-mathmodel-agent/references/artifact-contracts.md`. For final review scoring, read `my-mathmodel-agent/references/evaluation-rubric.md`.

When updating a user-requested file, replace the current version at its original path and remove obsolete content or duplicate old versions.
