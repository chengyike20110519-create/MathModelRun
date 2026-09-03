---
name: my-mathmodel-agent
description: "Evidence-driven mathematical modeling contest workflow for Claude Code: select a problem, route models, validate methods, run Python/AMPL experiments, freeze results, write LaTeX/Typst papers, and audit evidence and formatting."
---

# My MathModel Agent

Use this skill when working on Chinese or international mathematical modeling contest projects (CUMCM, MCM/ICM, HiMCM, Huawei Cup, etc.) that need a reproducible path from problem files to a defensible paper.

This is the Claude Code skill entry point. For Codex, use `my-mathmodel-agent/SKILL.md` in the same repository.

## Operating contract

Read `state.json` and `project_manifest.json` before acting. Follow `my-mathmodel-agent/references/workflow-contract.md` for the stage machine and artifact contracts. Never skip method validation, result freezing, or final audit.

## Default stages

```text
S0 PREFLIGHT  → S1 ANALYZE  → S2 ROUTE  → S3 DATA_PLAN
→ S4 METHOD_POC  → S5 EXPERIMENT  → S6 FREEZE
→ S7 WRITE  → S8 RENDER  → S9 AUDIT  → READY
```

At S2, compare candidate topics and routes using feasibility, validation, team fit, paper narrative, innovation, and fallback completeness. For each subproblem record a baseline, primary model, rejected alternatives, fallback, validation plan, and required figures.

At S4-S5, make the smallest runnable proof of concept before full experiments. Save code, parameters, logs, metrics, tables, and figures under the project directory. For optimization, use AMPL (`.mod` + `.dat` + `amplpy`) or an appropriate Python solver; verify `solve_result` and constraint feasibility before reporting success.

At S6, write every final number and conclusion source to `frozen_numbers.json`. The paper may only consume frozen values. If a result changes, invalidate and regenerate the freeze file.

At S7-S8, choose exactly one paper syntax: LaTeX (`.tex`, `\documentclass`, `\usepackage`, `\input`) or Typst (`.typ`, `#import`, `#set`, `#figure`). Do not mix syntaxes. Render and inspect the PDF for overflow, blank pages, missing figures, broken references, formulas, units, and encoding.

At S9, run both evidence and format audits. Classify failures and return to the corresponding stage: model→S4, code/data→S5, numbers→S6, paper/figures→S7, compilation/layout→S8.

## Subagents

Invoke the following role subagents when appropriate:

- `mathmodel-analyst`: problem decomposition and structured task cards.
- `mathmodel-modeler`: assumptions, variables, objectives, constraints, validation plan.
- `mathmodel-coder`: Python/AMPL implementation, logging, reproducibility.
- `mathmodel-writer`: evidence-driven paper assembly from frozen numbers.
- `mathmodel-reviewer`: critique, sensitivity checks, anti-hallucination audit.

## Deliverable behavior

Communicate the current stage, artifacts created, evidence checked, risks, and next entry point. Do not claim completion because a model or solver ran; completion requires `audit/final_report.md` with zero hard errors.

For detailed schemas and examples, read `my-mathmodel-agent/references/workflow-contract.md` only when creating or validating a project.
