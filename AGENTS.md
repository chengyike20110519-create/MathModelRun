# MyMathModelAgent

This repository is a **Codex / Claude Code compatible skill** for mathematical modeling contests.

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

```
MyMathModelAgent/
├── README.md                     # Project overview and install guide
├── AGENTS.md                     # This file: fallback entry for non-skill-aware tools
├── LICENSE                       # MIT
├── my-mathmodel-agent/           # Codex skill
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/workflow-contract.md
│   └── scripts/                  # init_project.py, doctor.py, freeze_numbers.py, audit_workspace.py
├── .claude/skills/my-mathmodel-agent/  # Claude Code skill mirror
│   ├── SKILL.md
│   └── agents/                   # Role-specific subagent prompts
├── docs/                         # Detailed documentation
├── templates/                    # Project templates and paper templates
└── tests/                        # Regression tests
```

## Important rules

1. Read `state.json` and `project_manifest.json` before acting.
2. Paper numbers must come from `frozen_numbers.json` only.
3. LaTeX and Typst cannot be mixed.
4. Every frozen number needs `source_file`, `source_run`, `subproblem`, and `notes`.
5. A `READY` state requires `audit/final_report.md` with zero hard errors.

For the full stage machine and gate contracts, see `my-mathmodel-agent/references/workflow-contract.md`.
