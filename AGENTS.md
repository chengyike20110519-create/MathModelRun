# MyMathModelAgent

This repository is a **Codex / Claude Code compatible skill** for mathematical modeling contests.

## File update policy

When the user asks to update, revise, or rewrite a file:

1. Update the original file in place, or replace it with the new version at the same path.
2. Remove obsolete content from that file; do not append a competing “new version” below the old one.
3. Remove obsolete duplicate files created by earlier revisions when they represent the same document.
4. Before finishing, verify that opening the requested path shows only the current version.
5. Do not preserve old versions unless the user explicitly asks for version history, backups, or archival copies.
6. Never overwrite unrelated user changes without first reading and incorporating them.

This policy applies to documentation, prompts, workflows, templates, scripts, reports, and configuration files.

## Skill entry points

If your agent tool does not auto-discover skills, load the appropriate entry point:

- **Codex**: `my-mathmodel-agent/SKILL.md`
- **Claude Code**: `.claude/skills/my-mathmodel-agent/SKILL.md`
- **Generic Agent**: read `README.md`, then follow the workflow in `docs/WORKFLOW.md`

## Core idea

Evidence-driven math modeling: problem → model → code → evidence → paper → audit.
Never skip method validation, result freezing, or final audit.

## Quick start

```bash
# 1. Scaffold a new contest project
python3 my-mathmodel-agent/scripts/init_project.py my-contest

# 2. Copy problem files into my-contest/problem_files/

# 3. Let the agent run through the 10-stage workflow
#    In Codex:  "$my-mathmodel-agent" or "@my-mathmodel-agent"
#    In Claude: "/my-mathmodel-agent"
```

## Repository layout

```text
MyMathModelAgent/
├── README.md                         # Project overview and install guide
├── AGENTS.md                         # This file: fallback entry and update policy
├── LICENSE                           # MIT
├── my-mathmodel-agent/               # Codex skill
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/workflow-contract.md
│   └── scripts/                      # init_project.py, doctor.py, freeze_numbers.py, audit_workspace.py
├── .claude/skills/my-mathmodel-agent/ # Claude Code skill mirror
│   ├── SKILL.md
│   └── agents/                       # Role-specific subagent prompts
├── .claude/agents/                   # Claude role agents
├── .claude/workflows/                # Reusable workflow definitions
├── competitions/                     # Competition-specific extensions
├── docs/                             # Detailed documentation
├── scripts/                          # Repository maintenance tools
├── templates/                        # Project templates and paper templates
└── tests/                            # Regression tests
```

## Important rules

1. Read `state.json` and `project_manifest.json` before acting.
2. Paper numbers must come from `frozen_numbers.json` only.
3. LaTeX and Typst cannot be mixed.
4. Every frozen number needs `source_file`, `source_run`, `subproblem`, and `notes`.
5. A `READY` state requires `audit/final_report.md` with zero hard errors.
6. Every requested file update must replace the old version at its original path.

For the full stage machine and gate contracts, see `my-mathmodel-agent/references/workflow-contract.md`.
