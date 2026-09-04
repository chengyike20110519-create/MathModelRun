"""Smoke tests for MyMathModelAgent repository."""
import subprocess
import sys
import json
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def test_repo_structure():
    """Essential files and directories must exist."""
    required = [
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
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing files: {missing}"


def test_codex_agent_yaml():
    """agents/openai.yaml must be valid YAML with display metadata."""
    yaml_path = REPO_ROOT / "my-mathmodel-agent/agents/openai.yaml"
    text = yaml_path.read_text()
    assert "display_name" in text
    assert "My Mathmodel Agent" in text


def test_init_project():
    """init_project.py can scaffold a project."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "my-mathmodel-agent/scripts/init_project.py"), "test-project"],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        project = Path(tmp) / "test-project"
        assert project.exists()
        assert (project / "project_manifest.json").exists()
        assert (project / "state.json").exists()


def test_doctor_help():
    """doctor.py supports --help."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "my-mathmodel-agent/scripts/doctor.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout


def test_freeze_requires_provenance():
    """Freeze must reject result rows without provenance."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "results.json"
        output = root / "frozen_numbers.json"
        source.write_text(json.dumps([{"name": "score", "value": 1}]))
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "my-mathmodel-agent/scripts/freeze_numbers.py"),
                str(source),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert not output.exists()


def test_freeze_writes_auditable_payload():
    """Freeze must include hash, timestamp, and provenance fields."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "results.json"
        output = root / "frozen_numbers.json"
        source.write_text(
            json.dumps(
                [
                    {
                        "name": "score",
                        "value": 1,
                        "unit": "points",
                        "source_file": "results/run.json",
                        "source_run": "run-001",
                        "subproblem": "Q1",
                        "notes": "verified smoke result",
                    }
                ]
            )
        )
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "my-mathmodel-agent/scripts/freeze_numbers.py"),
                str(source),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(output.read_text())
        assert payload["source_sha256"]
        assert payload["frozen_at"]
        assert payload["values"][0]["source_run"] == "run-001"


if __name__ == "__main__":
    test_repo_structure()
    test_codex_agent_yaml()
    test_init_project()
    test_doctor_help()
    print("All smoke tests passed.")
