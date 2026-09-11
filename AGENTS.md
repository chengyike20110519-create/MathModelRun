# MathModel Run / MyMathModelAgent

This repository is a **Codex / Claude Code compatible skill** for mathematical modeling contests. It provides a stateful, evidence-backed path from problem files to an audited paper.

## File update policy

When the user asks to update, revise, or rewrite a file:

1. Update the original file in place, or replace it with the new version at the same path.
2. Remove obsolete content from that file; do not append a competing “new version” below the old one.
3. Remove obsolete duplicate files created by earlier revisions when they represent the same document.
4. Before finishing, verify that opening the requested path shows only the current version.
5. Do not preserve old versions unless the user explicitly asks for version history, backups, or archival copies.
6. Never overwrite unrelated user changes without first reading and incorporating them.

This policy applies to documentation, prompts, workflows, templates, scripts, reports, pages, and configuration files.

## Entry points

- **Start page**: `index.html`
- **Codex skill**: `my-mathmodel-agent/SKILL.md`
- **Claude Code skill**: `.claude/skills/my-mathmodel-agent/SKILL.md`
- **Generic Agent**: read `README.md`, then follow `docs/WORKFLOW.md`
- **Mind map**: `docs/assets/mathmodel-mindmap.svg`

## Core idea

Evidence-driven math modeling: problem → model → code → experiment → frozen result → paper → audit.

Never skip method validation, result freezing, or final audit. Every project starts default-FAIL: all ten state gates are `false`, and a gate changes only after reproducible evidence exists.

## Quick start

```bash
python3 my-mathmodel-agent/scripts/init_project.py 2026-cumcm-a
python3 my-mathmodel-agent/scripts/status.py 2026-cumcm-a
python3 my-mathmodel-agent/scripts/doctor.py
```

## Repository layout

```text
MathModel Run/
├── index.html                         # interactive start page and mind map
├── README.md                          # overview, quick start, artifact map
├── AGENTS.md                          # fallback entry and in-place update policy
├── AGENT_PROMPT.md                    # reusable agent system prompt
├── docs/
│   ├── WORKFLOW.md                    # ten-stage workflow
│   └── assets/mathmodel-mindmap.svg   # shareable mind map
├── my-mathmodel-agent/                # Codex skill
│   ├── SKILL.md                       # router and operating contract
│   ├── references/
│   │   ├── workflow-contract.md       # stage inputs, outputs, exit gates
│   │   ├── artifact-contracts.md      # JSON field contracts
│   │   └── evaluation-rubric.md       # independent 0-5 review rubric
│   └── scripts/
│       ├── init_project.py            # default-FAIL scaffold
│       ├── status.py                  # current stage and first false gate
│       ├── doctor.py                  # environment diagnostic
│       ├── freeze_numbers.py          # provenance-backed result freeze
│       └── audit_workspace.py         # mechanical contract audit
├── templates/                         # generated project artifact templates
├── .claude/                           # Claude Code skill, agents, workflow
├── scripts/validate_repo.py           # release validator
└── tests/test_smoke.py                # regression smoke tests
```

## Important rules

1. Read `state.json`, `project_manifest.json`, and `PROGRESS.md` before acting.
2. Find the first false gate before choosing work.
3. Every subproblem needs baseline, primary, fallback, validation, and acceptance criteria.
4. Paper numbers must come from `frozen_numbers.json` only.
5. LaTeX and Typst cannot be mixed.
6. Every frozen number needs `name`, `value`, `unit`, `source_file`, `source_run`, `subproblem`, and `notes`.
7. Every true state gate needs matching evidence in `audit/gate_evidence.json`.
8. `READY` requires ten true gates, `audit/acceptance.json` verdict `pass`, and `audit/final_report.md` with zero hard errors.
9. Every requested file update must replace the old version at its original path.

For the full stage machine and gate contracts, see `my-mathmodel-agent/references/workflow-contract.md`.
