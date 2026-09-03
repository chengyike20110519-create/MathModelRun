---
name: my-mathmodel-agent
description: "Evidence-driven mathematical modeling contest workflow: select a problem, route models, validate methods, run Python/AMPL experiments, freeze results, write LaTeX/Typst papers, and audit evidence and formatting."
---

# My MathModel Agent

Use this skill for Chinese or international mathematical modeling contest projects that need a reproducible path from problem files to a defensible paper. Treat the project as a stateful artifact, not a chat-only answer.

This is the **Codex** skill entry. For Claude Code, use `.claude/skills/my-mathmodel-agent/SKILL.md` in the same repository.

## Quick entry points

- **Scaffold a new contest project**: `python3 my-mathmodel-agent/scripts/init_project.py <project-name>`
- **Check environment**: `python3 my-mathmodel-agent/scripts/doctor.py`
- **Validate the repository**: `python3 scripts/validate_repo.py`

## Operating contract

1. Read `state.json` and `project_manifest.json` before acting.
2. Follow `my-mathmodel-agent/references/workflow-contract.md` for the stage machine and artifact contracts.
3. Never skip method validation (S4), result freezing (S6), or final audit (S9).
4. Paper numbers may only come from `frozen_numbers.json`.
5. Choose exactly one paper syntax: LaTeX or Typst. Do not mix them.
6. For AMPL, verify `solve_result`, objective, bounds, and constraint violations before reporting success.

## Default stages

```text
S0 PREFLIGHT  → S1 ANALYZE  → S2 ROUTE  → S3 DATA_PLAN
→ S4 METHOD_POC  → S5 EXPERIMENT  → S6 FREEZE
→ S7 WRITE  → S8 RENDER  → S9 AUDIT  → READY
```

At **S0 PREFLIGHT**, verify problem files, record hashes, and run `doctor.py`.

At **S1 ANALYZE**, decompose the problem into subproblem task cards. Distinguish facts from assumptions.

At **S2 ROUTE**, compare candidate topics and routes. For each subproblem record baseline, primary, rejected alternatives, fallback, validation plan, and required figures.

At **S3 DATA_PLAN**, build a data dictionary, cleaning rules, leakage checks, and visualization plan.

At **S4 METHOD_POC**, define symbols, assumptions, objectives, and constraints. Implement the smallest runnable proof of concept before full experiments.

At **S5 EXPERIMENT**, run baseline → primary → ablation → sensitivity → robustness. Save code, parameters, logs, metrics, tables, and figures. For optimization, verify feasibility before reporting success.

At **S6 FREEZE**, write every final number and conclusion source to `frozen_numbers.json` with `source_file`, `source_run`, `subproblem`, and `notes`.

At **S7 WRITE**, assemble the paper from frozen numbers.

At **S8 RENDER**, compile and inspect the PDF for overflow, blank pages, missing figures, broken references, formulas, units, and encoding.

At **S9 AUDIT**, run evidence and format audits. Classify failures and return to the corresponding stage:

- model → S4
- code/data → S5
- numbers → S6
- paper/figures → S7
- compilation/layout → S8

## Subagents (Claude Code)

When using Claude Code, invoke role subagents from `.claude/agents/`:

- `mathmodel-analyst`: problem decomposition.
- `mathmodel-modeler`: model design and validation plan.
- `mathmodel-coder`: reproducible experiments.
- `mathmodel-writer`: paper assembly from frozen numbers.
- `mathmodel-reviewer`: evidence and format audit.

## Deliverable behavior

Communicate the current stage, artifacts created, evidence checked, risks, and next entry point. Do not claim completion because a model or solver ran; completion requires `audit/final_report.md` with zero hard errors.

For detailed schemas and examples, read `my-mathmodel-agent/references/workflow-contract.md` only when creating or validating a project.
