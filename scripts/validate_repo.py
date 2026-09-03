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
    "LICENSE",
    ".gitignore",
    "my-mathmodel-agent/SKILL.md",
    "my-mathmodel-agent/agents/openai.yaml",
    "my-mathmodel-agent/references/workflow-contract.md",
    "my-mathmodel-agent/scripts/init_project.py",
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
    "docs/INSTALL.md",
    "docs/WORKFLOW.md",
    "docs/CONTRIBUTE.md",
    "templates/shared/requirements.txt",
    "tests/test_smoke.py",
]

REQUIRED_EXECUTABLES = [
    "my-mathmodel-agent/scripts/doctor.py",
    "my-mathmodel-agent/scripts/init_project.py",
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
    for rel in ["my-mathmodel-agent/agents/openai.yaml", ".codex-plugin/plugin.json"]:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        try:
            text = path.read_text()
            # YAML is a superset of JSON; try JSON first, fall back to yaml if installed.
            try:
                json.loads(text)
            except json.JSONDecodeError:
                try:
                    import yaml
                    yaml.safe_load(text)
                except ImportError:
                    pass  # skip YAML validation if PyYAML is missing
            print(f"OK parse: {rel}")
        except Exception as exc:
            ok = error(f"cannot parse {rel}: {exc}")
    return ok


def validate_smoke_tests():
    print("Running smoke tests...")
    # Prefer pytest if available, otherwise run the script directly.
    if subprocess.run([sys.executable, "-m", "pytest", "--version"], capture_output=True).returncode == 0:
        cmd = [sys.executable, "-m", "pytest", "tests/test_smoke.py", "-v"]
    else:
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
    else:
        print("validate_repo: repository has issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
