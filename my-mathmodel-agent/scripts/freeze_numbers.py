#!/usr/bin/env python3
"""Freeze verified results with an auditable provenance record."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_PROVENANCE = ("source_file", "source_run", "subproblem", "notes")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_results(path: Path):
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    raise ValueError("results must be .json or .csv")


def validate_values(values):
    if not isinstance(values, list):
        return
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ValueError(f"values[{index}] must be an object")
        missing = [key for key in REQUIRED_PROVENANCE if not value.get(key)]
        if missing:
            raise ValueError(
                f"values[{index}] missing provenance fields: {', '.join(missing)}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze verified results with source hash and provenance."
    )
    parser.add_argument("results", help="verified .json or .csv results file")
    parser.add_argument("--output", default="frozen_numbers.json")
    args = parser.parse_args()

    source = Path(args.results).resolve()
    output = Path(args.output)
    if not source.is_file():
        parser.error(f"results file does not exist: {source}")

    try:
        data = load_results(source)
        validate_values(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    payload = {
        "schema_version": "1.0",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(source),
        "source_sha256": sha256(source),
        "values": data,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Frozen {source} -> {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
