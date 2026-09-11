"""Regression smoke tests for MathModel Run."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


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
]

GATES = [
    "input_snapshot",
    "problem_decomposed",
    "model_route_selected",
    "data_plan_ready",
    "method_validated",
    "experiments_reproduced",
    "results_frozen",
    "paper_written",
    "pdf_verified",
    "audit_passed",
]

SCAFFOLD_FILES = [
    "project_manifest.json",
    "state.json",
    "input_manifest.json",
    "PROGRESS.md",
    "frozen_numbers.json",
    "planning/problem_analysis.json",
    "planning/decision_log.jsonl",
    "methods/model_route.json",
    "methods/method_validation.json",
    "data_cleaned/data_plan.json",
    "figures/visualization_plan.json",
    "results/run_manifest.json",
    "paper/evidence_map.json",
    "paper/render_log.json",
    "audit/gate_evidence.json",
    "audit/acceptance.json",
]


def run_script(script, *args, cwd=None):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *map(str, args)],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
    )


def scaffold_project(tmp):
    result = run_script(
        "my-mathmodel-agent/scripts/init_project.py",
        "test-project",
        cwd=tmp,
    )
    assert result.returncode == 0, result.stderr
    return Path(tmp) / "test-project"


def test_repo_structure():
    missing = [path for path in REQUIRED_FILES if not (REPO_ROOT / path).exists()]
    assert not missing, f"Missing files: {missing}"


def test_codex_agent_yaml():
    text = (REPO_ROOT / "my-mathmodel-agent/agents/openai.yaml").read_text()
    assert "display_name" in text
    assert "MathModel Run" in text


def test_all_template_json_files_parse():
    for path in sorted((REPO_ROOT / "templates").glob("*.json")):
        data = json.loads(path.read_text())
        assert isinstance(data, (dict, list)), path


def test_init_project_scaffolds_default_fail_contract():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        for rel in SCAFFOLD_FILES:
            assert (project / rel).exists(), rel
        for directory in [
            "problem_files",
            "planning",
            "methods",
            "code",
            "data_cleaned",
            "results/runs",
            "figures",
            "paper",
            "audit",
        ]:
            assert (project / directory).is_dir(), directory

        state = json.loads((project / "state.json").read_text())
        assert state["schema_version"] == "2.0"
        assert state["stage"] == "PREFLIGHT"
        assert list(state["gates"]) == GATES
        assert all(value is False for value in state["gates"].values())

        route = json.loads((project / "methods/model_route.json").read_text())
        assert route["subproblems"][0]["passes"] is False
        assert route["subproblems"][0]["evidence"] == []
        assert not (project / "audit/final_report.md").exists()


def test_status_reports_first_false_gate():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        result = run_script(
            "my-mathmodel-agent/scripts/status.py",
            project,
            "--json",
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["stage"] == "PREFLIGHT"
        assert payload["first_false_gate"] == "input_snapshot"
        assert payload["expected_stage"] == "PREFLIGHT"
        assert len(payload["gates"]) == 10
        assert payload["gates"][0] == {"gate": "input_snapshot", "passed": False}


def test_stage_names_match_gate_progress():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["gates"]["input_snapshot"] = True
        state["stage"] = "ANALYZE"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        result = run_script(
            "my-mathmodel-agent/scripts/status.py",
            project,
            "--json",
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["expected_stage"] == "ANALYZE"
        assert payload["next_action"] == (
            "decompose_every_subproblem_with_acceptance_criteria"
        )


def test_audit_classifies_new_project_as_incomplete():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        result = run_script(
            "my-mathmodel-agent/scripts/audit_workspace.py",
            project,
        )
        assert result.returncode == 1
        assert "Mechanical Audit: INCOMPLETE" in result.stdout
        assert (project / "audit/mechanical_report.md").exists()
        assert not (project / "audit/final_report.md").exists()


def test_audit_rejects_gate_without_evidence():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["gates"]["input_snapshot"] = True
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        result = run_script(
            "my-mathmodel-agent/scripts/audit_workspace.py",
            project,
        )
        assert result.returncode == 1
        assert "Mechanical Audit: FAIL" in result.stdout
        assert "input_snapshot" in result.stdout


def test_audit_rejects_stage_ahead_of_gates():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["gates"]["input_snapshot"] = True
        state["stage"] = "WRITE"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        result = run_script(
            "my-mathmodel-agent/scripts/audit_workspace.py",
            project,
        )
        assert result.returncode == 1
        assert "Mechanical Audit: FAIL" in result.stdout
        assert "声明阶段不允许领先于" in result.stdout


def test_audit_rejects_all_gates_true_before_ready():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        for gate in state["gates"]:
            state["gates"][gate] = True
        state["stage"] = "WRITE"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        result = run_script(
            "my-mathmodel-agent/scripts/audit_workspace.py",
            project,
        )
        assert result.returncode == 1
        assert "所有门禁均已通过" in result.stdout



def test_audit_rejects_invalid_gate_evidence_kind():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        ge_path = project / "audit" / "gate_evidence.json"
        ge = json.loads(ge_path.read_text())
        ge["gates"]["input_snapshot"].append({"kind": "vibe", "value": "ok"})
        ge_path.write_text(json.dumps(ge, ensure_ascii=False, indent=2))
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "kind 无效" in result.stdout


def test_audit_rejects_gate_evidence_with_missing_path():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        ge_path = project / "audit" / "gate_evidence.json"
        ge = json.loads(ge_path.read_text())
        ge["gates"]["input_snapshot"].append({
            "kind": "command", "value": "ls", "path": "nonexistent/file.txt"
        })
        ge_path.write_text(json.dumps(ge, ensure_ascii=False, indent=2))
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "引用的 path 不存在" in result.stdout


def test_audit_rejects_frozen_run_not_in_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["stage"] = "FREEZE"
        for g in ["input_snapshot","problem_decomposed","model_route_selected",
                  "data_plan_ready","method_validated","experiments_reproduced","results_frozen"]:
            state["gates"][g] = True
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        ge_path = project / "audit" / "gate_evidence.json"
        ge = json.loads(ge_path.read_text())
        for g in ["input_snapshot","problem_decomposed","model_route_selected",
                  "data_plan_ready","method_validated","experiments_reproduced","results_frozen"]:
            ge["gates"][g] = [{"kind": "manual", "value": "verified"}]
        ge_path.write_text(json.dumps(ge, ensure_ascii=False, indent=2))
        frozen = json.loads((project / "frozen_numbers.json").read_text())
        frozen["frozen_at"] = "2026-09-11T00:00:00Z"
        frozen["source_sha256"] = "abc123"
        frozen["values"] = [{"name": "x", "value": 1, "unit": "u",
                              "source_file": "results/runs/run-999/metrics.json",
                              "source_run": "run-999", "subproblem": "Q1", "notes": "n"}]
        (project / "frozen_numbers.json").write_text(json.dumps(frozen, ensure_ascii=False, indent=2))
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "未在 results/run_manifest.json 登记" in result.stdout


def test_audit_rejects_evidence_map_empty_claims():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["stage"] = "WRITE"
        for g in ["input_snapshot","problem_decomposed","model_route_selected",
                  "data_plan_ready","method_validated","experiments_reproduced","results_frozen","paper_written"]:
            state["gates"][g] = True
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        ge_path = project / "audit" / "gate_evidence.json"
        ge = json.loads(ge_path.read_text())
        for g in state["gates"]:
            ge["gates"][g] = [{"kind": "manual", "value": "verified"}]
        ge_path.write_text(json.dumps(ge, ensure_ascii=False, indent=2))
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "claims 为空" in result.stdout


def test_audit_rejects_evidence_map_dangling_frozen_ref():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        state_path = project / "state.json"
        state = json.loads(state_path.read_text())
        state["stage"] = "WRITE"
        for g in ["input_snapshot","problem_decomposed","model_route_selected",
                  "data_plan_ready","method_validated","experiments_reproduced","results_frozen","paper_written"]:
            state["gates"][g] = True
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        ge_path = project / "audit" / "gate_evidence.json"
        ge = json.loads(ge_path.read_text())
        for g in state["gates"]:
            ge["gates"][g] = [{"kind": "manual", "value": "verified"}]
        ge_path.write_text(json.dumps(ge, ensure_ascii=False, indent=2))
        em = {"schema_version": "2.0", "claims": [{
            "claim_id": "c1", "claim": "test", "paper_location": "s1",
            "evidence": [{"kind": "data", "value": "frozen_numbers.json#nonexistent", "path": "frozen_numbers.json"}]
        }]}
        (project / "paper" / "evidence_map.json").write_text(json.dumps(em, ensure_ascii=False, indent=2))
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "不存在于 frozen_numbers.json" in result.stdout


def test_audit_rejects_bad_decision_log_classification():
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold_project(tmp)
        log_path = project / "planning" / "decision_log.jsonl"
        log_path.write_text(
            json.dumps({"at": "2026-09-11T00:00:00Z", "subject": "x", "classification": "INVALID"}) + chr(10),
            encoding="utf-8"
        )
        result = run_script("my-mathmodel-agent/scripts/audit_workspace.py", project)
        assert result.returncode == 1
        assert "classification" in result.stdout and "无效" in result.stdout

def test_doctor_help():
    result = run_script("my-mathmodel-agent/scripts/doctor.py", "--help")
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout


def test_freeze_requires_complete_provenance():
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
                        "source_file": "results/run.json",
                        "source_run": "run-001",
                        "subproblem": "Q1",
                        "notes": "missing unit",
                    }
                ]
            )
        )
        result = run_script(
            "my-mathmodel-agent/scripts/freeze_numbers.py",
            source,
            "--output",
            output,
        )
        assert result.returncode != 0
        assert "unit" in result.stderr
        assert not output.exists()


def test_freeze_writes_auditable_payload():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "results.json"
        output = root / "frozen_numbers.json"
        source.write_text(
            json.dumps(
                {
                    "values": [
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
                }
            )
        )
        result = run_script(
            "my-mathmodel-agent/scripts/freeze_numbers.py",
            source,
            "--output",
            output,
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(output.read_text())
        assert payload["schema_version"] == "2.0"
        assert payload["source_sha256"]
        assert payload["frozen_at"]
        assert payload["values"][0]["source_run"] == "run-001"


if __name__ == "__main__":
    test_repo_structure()
    test_codex_agent_yaml()
    test_all_template_json_files_parse()
    test_init_project_scaffolds_default_fail_contract()
    test_status_reports_first_false_gate()
    test_stage_names_match_gate_progress()
    test_audit_classifies_new_project_as_incomplete()
    test_audit_rejects_gate_without_evidence()
    test_audit_rejects_stage_ahead_of_gates()
    test_audit_rejects_all_gates_true_before_ready()
    test_audit_rejects_invalid_gate_evidence_kind()
    test_audit_rejects_gate_evidence_with_missing_path()
    test_audit_rejects_frozen_run_not_in_manifest()
    test_audit_rejects_evidence_map_empty_claims()
    test_audit_rejects_evidence_map_dangling_frozen_ref()
    test_audit_rejects_bad_decision_log_classification()
    test_doctor_help()
    test_freeze_requires_complete_provenance()
    test_freeze_writes_auditable_payload()
    print("All smoke tests passed.")
