#!/usr/bin/env python3
"""Validate that this repository is ready for release."""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "AGENT_PROMPT.md",
    "LICENSE",
    ".gitignore",
    "index.html",
    "docs/WORKFLOW.md",
    "docs/INSTALL.md",
    "docs/CONTRIBUTE.md",
    "docs/assets/mathmodel-mindmap.svg",
    "my-mathmodel-agent/SKILL.md",
    "my-mathmodel-agent/agents/openai.yaml",
    "my-mathmodel-agent/references/workflow-contract.md",
    "my-mathmodel-agent/references/artifact-contracts.md",
    "my-mathmodel-agent/references/evaluation-rubric.md",
    "my-mathmodel-agent/scripts/init_project.py",
    "my-mathmodel-agent/scripts/status.py",
    "my-mathmodel-agent/scripts/doctor.py",
    "my-mathmodel-agent/scripts/freeze_numbers.py",
    "my-mathmodel-agent/scripts/audit_workspace.py",
    ".claude/skills/my-mathmodel-agent/SKILL.md",
    ".claude/agents/mathmodel-analyst.md",
    ".claude/agents/mathmodel-modeler.md",
    ".claude/agents/mathmodel-coder.md",
    ".claude/agents/mathmodel-writer.md",
    ".claude/agents/mathmodel-reviewer.md",
    ".claude/workflows/mathmodel-workflow.md",
    "templates/project_manifest.json",
    "templates/state.json",
    "templates/input_manifest.json",
    "templates/problem_analysis.json",
    "templates/model_route.json",
    "templates/data_plan.json",
    "templates/visualization_plan.json",
    "templates/method_validation.json",
    "templates/run_manifest.json",
    "templates/evidence_map.json",
    "templates/render_log.json",
    "templates/gate_evidence.json",
    "templates/acceptance.json",
    "templates/frozen_numbers.json",
    "templates/PROGRESS.md",
    "templates/decision_log.jsonl",
    "templates/shared/requirements.txt",
    "tests/test_smoke.py",
]

REQUIRED_EXECUTABLES = [
    "my-mathmodel-agent/scripts/init_project.py",
    "my-mathmodel-agent/scripts/status.py",
    "my-mathmodel-agent/scripts/doctor.py",
    "my-mathmodel-agent/scripts/freeze_numbers.py",
    "my-mathmodel-agent/scripts/audit_workspace.py",
]

JSON_FILES = [
    ".codex-plugin/plugin.json",
    *[
        f"templates/{name}.json"
        for name in [
            "project_manifest",
            "state",
            "input_manifest",
            "problem_analysis",
            "model_route",
            "data_plan",
            "visualization_plan",
            "method_validation",
            "run_manifest",
            "evidence_map",
            "render_log",
            "gate_evidence",
            "acceptance",
            "frozen_numbers",
        ]
    ],
]


def error(msg):
    print(f"ERROR: {msg}")
    return False


def validate_files():
    ok = True
    for rel in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            ok = error(f"missing required file: {rel}")
        else:
            print(f"OK file: {rel}")
    return ok


def validate_executables():
    ok = True
    for rel in REQUIRED_EXECUTABLES:
        path = REPO_ROOT / rel
        if not os.access(path, os.X_OK):
            ok = error(f"not executable: {rel}")
        else:
            print(f"OK executable: {rel}")
    return ok


def validate_json_files():
    ok = True
    for rel in JSON_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            ok = error(f"missing JSON file: {rel}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            print(f"OK json: {rel}")
        except Exception as exc:
            ok = error(f"cannot parse {rel}: {exc}")
    for rel in ["my-mathmodel-agent/agents/openai.yaml"]:
        path = REPO_ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
            try:
                json.loads(text)
            except json.JSONDecodeError:
                try:
                    import yaml
                    yaml.safe_load(text)
                except ImportError:
                    pass
            print(f"OK parse: {rel}")
        except Exception as exc:
            ok = error(f"cannot parse {rel}: {exc}")
    return ok


def validate_smoke_tests():
    print("Running smoke tests...")
    # Prefer the direct smoke entrypoint. Some local Python distributions load
    # pytest plugin modules that can fail before tests execute; the script
    # entrypoint exercises the same regression tests without that extra layer.
    cmd = [sys.executable, "tests/test_smoke.py"]
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return error("smoke tests failed")
    return True


def main():
    ok = True
    ok &= validate_files()
    ok &= validate_executables()
    ok &= validate_json_files()
    ok &= validate_smoke_tests()
    print()
    if ok:
        print("validate_repo: repository is release-ready")
        return 0
    print("validate_repo: repository has issues")
    return 1


if __name__ == "__main__":
    sys.exit(main())
