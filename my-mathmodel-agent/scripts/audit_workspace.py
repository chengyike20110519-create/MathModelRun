#!/usr/bin/env python3
"""Audit project artifacts, state gates, and frozen-number provenance."""
import argparse
import json
from pathlib import Path


REQUIRED = (
    "problem_files",
    "planning",
    "methods",
    "code",
    "data_cleaned",
    "results",
    "figures",
    "paper",
    "audit",
    "state.json",
    "project_manifest.json",
    "frozen_numbers.json",
)
REQUIRED_PROVENANCE = ("source_file", "source_run", "subproblem", "notes")


def read_json(path: Path, issues: list[str], label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"{label} 无法解析：{exc}")
        return None


def audit_frozen_numbers(root: Path, issues: list[str]) -> None:
    path = root / "frozen_numbers.json"
    if not path.exists():
        issues.append("缺少 frozen_numbers.json：结果尚未冻结")
        return
    frozen = read_json(path, issues, "frozen_numbers.json")
    if not isinstance(frozen, dict):
        return
    if not frozen.get("frozen_at") or not frozen.get("source_sha256"):
        issues.append("frozen_numbers.json 缺少冻结时间或源文件哈希")
    values = frozen.get("values")
    if isinstance(values, list):
        for index, value in enumerate(values):
            if not isinstance(value, dict):
                issues.append(f"冻结值 values[{index}] 不是对象")
                continue
            missing = [key for key in REQUIRED_PROVENANCE if not value.get(key)]
            if missing:
                issues.append(
                    f"冻结值 values[{index}] 缺少溯源字段：{', '.join(missing)}"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a math modeling project workspace")
    parser.add_argument("project", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    missing = [name for name in REQUIRED if not (root / name).exists()]
    issues: list[str] = []

    if not (root / "state.json").exists():
        issues.append("缺少 state.json")
    else:
        state = read_json(root / "state.json", issues, "state.json")
        if isinstance(state, dict) and state.get("stage") == "READY" and missing:
            issues.append("状态为 READY，但仍缺少必需文件")

    audit_frozen_numbers(root, issues)
    status = "PASS" if not missing and not issues else "FAIL"
    lines = [
        f"# Final Audit: {status}",
        "",
        f"项目：{root}",
        "",
        f"缺失文件：{len(missing)}",
        *(f"- {item}" for item in missing),
        "- 无" if not missing else "",
        "",
        f"问题：{len(issues)}",
        *(f"- {item}" for item in issues),
        "- 无" if not issues else "",
        "",
        "审计结论：证据、冻结结果和格式检查全部通过后，才能将 state.json 更新为 READY。",
    ]
    report = "\n".join(lines) + "\n"
    (root / "audit").mkdir(exist_ok=True)
    (root / "audit" / "final_report.md").write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
