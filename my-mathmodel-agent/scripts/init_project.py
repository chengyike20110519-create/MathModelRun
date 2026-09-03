#!/usr/bin/env python3
"""Initialize a new math-model project scaffold."""
import argparse
import json
from pathlib import Path

DIRECTORIES = [
    "problem_files",
    "planning",
    "methods",
    "code",
    "data_cleaned",
    "results",
    "figures",
    "paper",
    "audit",
]

FROZEN_NUMBERS_SKELETON = {
    "frozen_at": None,
    "source_file": None,
    "source_sha256": None,
    "values": {},
}


def main():
    # The script lives at <repo_root>/my-mathmodel-agent/scripts/init_project.py
    repo_root = Path(__file__).resolve().parents[2]
    templates_dir = repo_root / "templates"

    parser = argparse.ArgumentParser(
        description="Initialize a new math-model project scaffold."
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
    for d in DIRECTORIES:
        (root / d).mkdir(parents=True, exist_ok=True)

    manifest = json.loads(
        (templates_dir / "project_manifest.json").read_text(encoding="utf-8")
    )
    manifest["project_name"] = root.name
    (root / "project_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    model_route = json.loads(
        (templates_dir / "model_route.json").read_text(encoding="utf-8")
    )
    (root / "model_route.json").write_text(
        json.dumps(model_route, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    (root / "state.json").write_text(
        json.dumps({"stage": "PREFLIGHT", "status": "not_started"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (root / "frozen_numbers.json").write_text(
        json.dumps(FROZEN_NUMBERS_SKELETON, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Initialized {root}")


if __name__ == "__main__":
    main()
