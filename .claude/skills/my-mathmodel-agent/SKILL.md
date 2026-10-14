---
name: my-mathmodel-agent
description: "Evidence-driven mathematical modeling contest workflow for Claude Code: decompose a problem, select baseline/primary/fallback model routes, validate PoCs, run reproducible Python/AMPL experiments, freeze results, write LaTeX or Typst papers, render, and audit every claim. Use for CUMCM, MCM/ICM, HiMCM, and similar contests; not for casual homework or one-off coding questions."
---

# MathModel Run

Use this skill when working on Chinese or international mathematical modeling contest projects that need a reproducible path from problem files to defensible decisions and, later, a defensible paper.

## Default user experience

The primary product is not one-click paper generation. First identify the
current blocker, compare model routes, run the smallest useful validation, and
write a critique report when the evidence is weak. Unless the user explicitly
asks for a complete paper, return a bounded work package instead:

1. current blocker;
2. why it blocks later work;
3. smallest next action;
4. acceptance criteria;
5. exact fallback if it fails.

Paper writing is a controlled downstream action. Use only verified and frozen
results, and prefer a problem card, model decision card, experiment plan,
critique report, result explanation, or single section when that is enough.

## Structure papers from evidence

Use exemplar papers to extract useful decisions, not to copy headings or named
methods. Map every prompt deliverable to a section, then organize the paper as
problem and scope, data and assumptions, one section per major model or task,
validation and robustness, and conclusion. A strong model route often has a
simple baseline, a primary mechanism model, an ordered simulation algorithm,
direct requested outputs, and an interpretation with explicit limits. Add only
the parts supported by the current problem and evidence.

Make model states and transitions visible with a workflow or state diagram.
Choose figures by the question they answer: maps or spatial small multiples for
geometry, time series for forcing and growth, distributions or intervals for
randomness, and sensitivity or ablation plots for robustness. Keep colors and
state names consistent. A representative run may illustrate a pattern, but
statistical claims must use the declared replicate set. Label sourced data,
assumed parameters, and model-generated outputs separately. Do not add a
Leslie matrix, cellular automaton, AHP, TOPSIS, radar chart, or other named
technique unless it is necessary and independently checkable. Page count must
come from a complete argument rather than empty headings or decorative plots.

This is the Claude Code skill entry point. For Codex, use `my-mathmodel-agent/SKILL.md` in the repository root.

For quantitative Python figures, read the shared
`my-mathmodel-agent/references/python-figures.md` from the repository root and
use `my-mathmodel-agent/scripts/figure_tools.py` as an adaptable plotting helper.
Plan evidence-driven combinations, use native axes and intended manuscript
dimensions, and inspect actual exports before claiming visual quality. Update
requested active figures in place so their original links show the revision.

For substantial result charts, use the shared
`my-mathmodel-agent/references/data-figure-agent.md` and its reference-figure
lessons. Delegate to `mathmodel-data-figure` when appropriate and keep review
independent. AI workflow images follow the shared `ai-workflow-gate.md`:
freeze implemented labels and topology, then verify every actual label/arrow.
Use `my-mathmodel-agent/scripts/figure_gate.py` and its review template to block
pending, unresolved or stale reviews. Standalone approval precedes insertion;
final paper approval also inspects the actual rendered page. Update original
active files rather than creating unsolicited numbered alternatives.

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
Evidence is labeled `STRUCTURAL`, `RUNTIME`, or `VISUAL`; structural checks alone cannot open runtime or visual gates. A fallback renderer must be identified and cannot be called submission-compliant without an explicit format check.

## Core contracts

- Each subproblem gets `planning/problem_analysis.json` with observable acceptance criteria.
- Each model route records `baseline`, `primary_model`, `fallback_model`, rejected alternatives, and a validation plan.
- Each experiment run records command, input hash, parameters, seed, environment, metrics, logs, and outputs.
- Paper numbers may only come from `frozen_numbers.json`.
- Each paper claim maps through `paper/evidence_map.json` to a frozen value, figure, or run.
- Each paper contains a labeled `Workflow`/`工作流` section or equivalent figure, mapped step-by-step in `paper/workflow.json`.
- Every PDF page is checked in `paper/render_log.json`.
- Final readiness requires zero hard errors in `audit/final_report.md` and a hashed `audit/package_manifest.json` with caches, secrets, personal paths, and obsolete duplicates excluded.

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

When updating a user-requested file, replace the current version at its original path and remove obsolete content or duplicate old versions. If upstream inputs, code, parameters, environment, or templates change, invalidate downstream gates and rerun the affected evidence.
