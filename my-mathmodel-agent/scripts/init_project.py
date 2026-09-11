#!/usr/bin/env python3
"""Initialize a default-FAIL math modeling contest workspace."""
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


DIRECTORIES = [
    "problem_files",
    "planning",
    "methods",
    "code",
    "data_cleaned",
    "results/runs",
    "figures",
    "paper",
    "audit",
]

TEMPLATE_FILES = {
    "project_manifest.json": "project_manifest.json",
    "state.json": "state.json",
    "input_manifest.json": "input_manifest.json",
    "problem_analysis.json": "planning/problem_analysis.json",
    "model_route.json": "methods/model_route.json",
    "data_plan.json": "data_cleaned/data_plan.json",
    "visualization_plan.json": "figures/visualization_plan.json",
    "method_validation.json": "methods/method_validation.json",
    "run_manifest.json": "results/run_manifest.json",
    "evidence_map.json": "paper/evidence_map.json",
    "render_log.json": "paper/render_log.json",
    "gate_evidence.json": "audit/gate_evidence.json",
    "acceptance.json": "audit/acceptance.json",
    "frozen_numbers.json": "frozen_numbers.json",
}

TEMPLATE_TEXT = {
    "PROGRESS.md": "PROGRESS.md",
    "decision_log.jsonl": "planning/decision_log.jsonl",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    templates_dir = repo_root / "templates"

    parser = argparse.ArgumentParser(
        description="Initialize a default-FAIL math modeling contest workspace."
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="contest-project",
        help="project directory name (default: contest-project)",
    )
    args = parser.parse_args()

    root = Path(args.name)
    root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)

    for template_name, destination in TEMPLATE_FILES.items():
        shutil.copy2(
            templates_dir / template_name,
            root / destination,
        )

    for template_name, destination in TEMPLATE_TEXT.items():
        shutil.copy2(
            templates_dir / template_name,
            root / destination,
        )

    manifest_path = root / "project_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["project_name"] = root.name
    write_json(manifest_path, manifest)

    state_path = root / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["project_name"] = root.name
    state["updated_at"] = utc_now()
    write_json(state_path, state)

    print(f"Initialized MathModel workspace: {root.resolve()}")
    print()
    print("Next:")
    print("  1. Copy official problem files into problem_files/.")
    print("  2. Fill input_manifest.json with paths, hashes, and access dates.")
    print("  3. Run:")
    print(f"     python3 {repo_root / 'my-mathmodel-agent/scripts/status.py'} {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
