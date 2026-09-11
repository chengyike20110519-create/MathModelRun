#!/usr/bin/env python3
"""Show the current MathModel project stage and first false gate."""
import argparse
import json
from pathlib import Path


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

# stage records the stage currently being advanced (imperative S-stage names),
# not the last completed stage. Each stage binds to exactly one completion gate.
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

STAGE_NEXT_ACTION = {
    "PREFLIGHT": "inspect_problem_files_and_record_hashes",
    "ANALYZE": "decompose_every_subproblem_with_acceptance_criteria",
    "ROUTE": "select_baseline_primary_fallback_for_every_subproblem",
    "DATA_PLAN": "define_fields_cleaning_rules_and_figure_plan",
    "METHOD_POC": "run_a_minimal_proof_of_concept",
    "EXPERIMENT": "run_baseline_primary_ablation_sensitivity_robustness",
    "FREEZE": "freeze_every_paper_number_with_provenance",
    "WRITE": "write_the_paper_from_frozen_numbers_only",
    "RENDER": "compile_and_inspect_every_page",
    "AUDIT": "reproduce_evidence_and_write_final_report",
    "READY": "package_and_submit",
}

ARTIFACTS = [
    "input_manifest.json",
    "planning/problem_analysis.json",
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
]


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show the current MathModel project stage and next gate."
    )
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", help="print machine-readable status")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"project does not exist: {root}")

    state = read_json(root / "state.json")
    manifest = read_json(root / "project_manifest.json")
    if not isinstance(state, dict):
        parser.error("state.json is missing or invalid")

    gates = state.get("gates")
    if not isinstance(gates, dict):
        gates = {}

    gate_items = [
        {"gate": gate, "passed": bool(gates.get(gate))}
        for gate in GATES
    ]
    first_false = next((item["gate"] for item in gate_items if not item["passed"]), None)
    expected_stage = "READY"
    if first_false:
        expected_stage = next(
            name for name, gate in STAGE_GATE.items() if gate == first_false
        )
    missing = [path for path in ARTIFACTS if not (root / path).exists()]
    stage = state.get("stage", "UNKNOWN")
    # The authoritative next action is derived from the first false gate, not
    # from the hand-maintained state.next_action field, which can drift.
    declared_action = state.get("next_action")
    derived_action = STAGE_NEXT_ACTION.get(expected_stage)
    next_action = derived_action or declared_action

    payload = {
        "project": str(root),
        "project_name": manifest.get("project_name") if isinstance(manifest, dict) else None,
        "stage": stage,
        "expected_stage": expected_stage,
        "status": state.get("status"),
        "next_action": next_action,
        "declared_next_action": declared_action,
        "next_action_drift": bool(
            declared_action and derived_action and declared_action != derived_action
        ),
        "first_false_gate": first_false,
        "gates": gate_items,
        "missing_artifacts": missing,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    passed = sum(item["passed"] for item in gate_items)
    print(f"Project: {payload['project_name'] or root.name}")
    print(f"Stage:   {stage}")
    if stage != expected_stage:
        print(f"Expected stage from gates: {expected_stage}")
    print(f"Status:  {state.get('status')}")
    print(f"Gates:   {passed}/{len(gate_items)} passed")
    for item in gate_items:
        mark = "PASS" if item["passed"] else "OPEN"
        print(f"  {mark:<4} {item['gate']}")
    print()
    print(f"Next:    {next_action or 'resolve_state_contract'}")
    if payload["next_action_drift"]:
        print(f"Declared next_action is stale: {declared_action}")
    if first_false:
        print(f"Gate:    {first_false}")
    if missing:
        print("Missing artifacts:")
        for path in missing:
            print(f"  - {path}")
    else:
        print("Missing artifacts: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
