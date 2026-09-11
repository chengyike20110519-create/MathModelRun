#!/usr/bin/env python3
"""Mechanically audit project structure, state gates, and provenance."""
import argparse
import json
from pathlib import Path


REQUIRED_DIRECTORIES = (
    "problem_files",
    "planning",
    "methods",
    "code",
    "data_cleaned",
    "results",
    "figures",
    "paper",
    "audit",
)

REQUIRED_FILES = (
    "state.json",
    "project_manifest.json",
    "input_manifest.json",
    "planning/problem_analysis.json",
    "planning/decision_log.jsonl",
    "methods/model_route.json",
    "data_cleaned/data_plan.json",
    "figures/visualization_plan.json",
    "methods/method_validation.json",
    "results/run_manifest.json",
    "frozen_numbers.json",
    "paper/evidence_map.json",
    "paper/render_log.json",
    "audit/gate_evidence.json",
    "audit/acceptance.json",
)

GATES = (
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
)

# stage records the stage currently being advanced. A declared stage must never
# be ahead of the first gate that is still false.
STAGE_GATE = {
    "PREFLIGHT": "input_snapshot",
    "ANALYZE": "problem_decomposed",
    "ROUTE": "model_route_selected",
    "DATA_PLAN": "data_plan_ready",
    "METHOD_POC": "method_validated",
    "EXPERIMENT": "experiments_reproduced",
    "FREEZE": "results_frozen",
    "WRITE": "paper_written",
    "RENDER": "pdf_verified",
    "AUDIT": "audit_passed",
}

FIELDS = (
    "name",
    "value",
    "unit",
    "source_file",
    "source_run",
    "subproblem",
    "notes",
)


def read_json(path: Path, issues: list[str], label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"{label} 无法解析：{exc}")
        return None


def audit_gate_contract(root: Path, issues: list[str]) -> None:
    state = read_json(root / "state.json", issues, "state.json")
    gate_evidence = read_json(root / "audit" / "gate_evidence.json", issues, "audit/gate_evidence.json")

    if not isinstance(state, dict):
        return
    gates = state.get("gates")
    if not isinstance(gates, dict):
        issues.append("state.json 缺少 gates 对象")
        return

    unknown = sorted(set(gates) - set(GATES))
    missing = sorted(set(GATES) - set(gates))
    if unknown:
        issues.append(f"state.json gates 包含未知门禁：{', '.join(unknown)}")
    if missing:
        issues.append(f"state.json gates 缺少门禁：{', '.join(missing)}")

    evidence_gates = gate_evidence.get("gates") if isinstance(gate_evidence, dict) else None
    if not isinstance(evidence_gates, dict):
        issues.append("audit/gate_evidence.json 缺少 gates 对象")
        return
    for gate in GATES:
        if gates.get(gate) and not evidence_gates.get(gate):
            issues.append(f"门禁 {gate} 已为 true，但 audit/gate_evidence.json 没有证据")

    stage = state.get("stage")
    if stage not in STAGE_GATE and stage != "READY":
        issues.append(f"state.json stage 未知：{stage!r}")
        return
    first_false = next((gate for gate in GATES if not gates.get(gate)), None)
    if first_false is None:
        if stage != "READY":
            issues.append("所有门禁均已通过，但 stage 尚未推进到 READY")
        return
    expected_stage = next(
        name for name, gate in STAGE_GATE.items() if gate == first_false
    )
    declared_index = list(STAGE_GATE).index(stage) if stage in STAGE_GATE else len(STAGE_GATE)
    expected_index = list(STAGE_GATE).index(expected_stage)
    if declared_index > expected_index:
        issues.append(
            f"state.json stage 声明为 {stage}，但门禁 {first_false} 仍为 false；"
            f"声明阶段不允许领先于 {expected_stage}"
        )


def audit_frozen_numbers(root: Path, issues: list[str], state: dict | None) -> None:
    frozen = read_json(root / "frozen_numbers.json", issues, "frozen_numbers.json")
    if not isinstance(frozen, dict):
        return
    if frozen.get("schema_version") != "2.0":
        issues.append("frozen_numbers.json schema_version 必须为 2.0")
    gates = state.get("gates") if isinstance(state, dict) else None
    freeze_expected = bool(isinstance(gates, dict) and gates.get("results_frozen"))
    if freeze_expected and (not frozen.get("frozen_at") or not frozen.get("source_sha256")):
        issues.append("frozen_numbers.json 缺少冻结时间或源文件哈希")
    values = frozen.get("values")
    if not isinstance(values, list):
        issues.append("frozen_numbers.json values 必须是数组")
        return
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            issues.append(f"冻结值 values[{index}] 不是对象")
            continue
        missing = [key for key in FIELDS if key not in value]
        if missing:
            issues.append(f"冻结值 values[{index}] 缺少字段：{', '.join(missing)}")


def audit_acceptance_contracts(root: Path, issues: list[str]) -> None:
    route = read_json(root / "methods" / "model_route.json", issues, "methods/model_route.json")
    state = read_json(root / "state.json", issues, "state.json")
    gates = state.get("gates") if isinstance(state, dict) else None
    route_expected = bool(isinstance(gates, dict) and gates.get("model_route_selected"))
    if isinstance(route, dict) and route_expected:
        subproblems = route.get("subproblems")
        if isinstance(subproblems, list):
            for index, item in enumerate(subproblems):
                if not isinstance(item, dict):
                    issues.append(f"model_route.subproblems[{index}] 不是对象")
                elif not item.get("acceptance_criteria"):
                    issues.append(f"model_route.subproblems[{index}] 缺少 acceptance_criteria")

    render = read_json(root / "paper" / "render_log.json", issues, "paper/render_log.json")
    if isinstance(render, dict) and isinstance(gates, dict) and gates.get("pdf_verified"):
        pages = render.get("pages")
        if not isinstance(pages, list) or not pages:
            issues.append("pdf_verified 为 true，但 render_log.pages 为空")
        elif any(not isinstance(page, dict) or not page.get("checked") for page in pages):
            issues.append("pdf_verified 为 true，但存在未逐页检查的页面")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mechanically audit a MathModel workspace before READY."
    )
    parser.add_argument("project", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    missing = [name for name in REQUIRED_DIRECTORIES + REQUIRED_FILES if not (root / name).exists()]
    issues: list[str] = []

    audit_gate_contract(root, issues)
    state = read_json(root / "state.json", issues, "state.json")
    audit_frozen_numbers(root, issues, state)
    audit_acceptance_contracts(root, issues)

    if isinstance(state, dict) and state.get("stage") == "READY":
        gates = state.get("gates", {}) if isinstance(state.get("gates"), dict) else {}
        if not all(gates.get(gate) for gate in GATES):
            issues.append("状态为 READY，但仍有门禁未通过")
        if not (root / "audit" / "final_report.md").exists():
            issues.append("READY 缺少 audit/final_report.md 独立审查报告")
        acceptance = read_json(root / "audit" / "acceptance.json", issues, "audit/acceptance.json")
        if isinstance(acceptance, dict) and acceptance.get("verdict") != "pass":
            issues.append("READY 要求 audit/acceptance.json verdict=pass")

    gates = state.get("gates") if isinstance(state, dict) else {}
    ready = all(isinstance(gates, dict) and gates.get(gate) for gate in GATES)
    if issues:
        verdict = "FAIL"
    elif missing or not ready:
        verdict = "INCOMPLETE"
    else:
        verdict = "MECHANICAL_PASS"

    lines = [
        f"# Mechanical Audit: {verdict}",
        "",
        f"项目：{root}",
        "",
        f"缺失文件或目录：{len(missing)}",
        *(f"- {item}" for item in missing),
        "- 无" if not missing else "",
        "",
        f"硬问题：{len(issues)}",
        *(f"- {item}" for item in issues),
        "- 无" if not issues else "",
        "",
        "说明：本报告只验证结构、门禁和溯源契约；READY 仍要求独立审查者复现证据并写出 audit/final_report.md。",
    ]
    report = "\n".join(lines) + "\n"
    (root / "audit").mkdir(exist_ok=True)
    (root / "audit" / "mechanical_report.md").write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if verdict == "MECHANICAL_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
