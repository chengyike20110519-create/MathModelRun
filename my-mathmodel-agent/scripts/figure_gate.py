#!/usr/bin/env python3
"""Seal artifacts and check recorded figure reviews using the standard library.

Usage: python figure_gate.py seal CASE.json
       python figure_gate.py check CASE.json

This checks the evidence/review contract, not scientific truth or aesthetics.
Sealing never approves a figure: it resets every review to pending. Paths in
files are relative to CASE.json unless absolute. A changed file invalidates its
hash, the figure fingerprint, and reviews bound to the previous fingerprint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import tempfile


BASE_ROLES = {"spec", "caption", "image", "final_size_preview", "grayscale_preview"}
KIND_ROLES = {"data": {"data", "code", "vector"}, "workflow": {"model"}}
PAPER_ROLES = {"paper_source", "paper_pdf", "rendered_page"}
SCIENTIFIC_CHECKS = {
    "data": {"sources_values", "units_estimators", "encoding_fit",
             "uncertainty_sampling", "transforms_missingness"},
    "workflow": {"labels_exact", "nodes_edges_exact", "sequence_feedback",
                 "claims_match_model"},
}
VISUAL_CHECKS = {"final_size_grayscale", "hierarchy_alignment", "labels_overlap"}
VISUAL_SCORES = ("hierarchy", "readability", "comparison", "finish")


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def reject_constant(value):
    raise ValueError(f"Non-finite JSON number is not allowed: {value}")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_case(path):
    case = json.loads(path.read_text(encoding="utf-8-sig"),
                      object_pairs_hook=unique_keys, parse_constant=reject_constant)
    if not isinstance(case, dict):
        raise ValueError("CASE.json must contain a JSON object")
    return case


def header_errors(case):
    errors = []
    if case.get("kind") not in KIND_ROLES:
        errors.append("kind must be data or workflow")
    if case.get("scope") not in {"standalone", "paper"}:
        errors.append("scope must be standalone or paper")
    if not nonempty_text(case.get("builder")):
        errors.append("builder must be a nonempty reviewer/agent identity")
    if not isinstance(case.get("files"), list) or not case["files"]:
        errors.append("files must be a nonempty list")
    return errors


def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_files(case, case_path, *, verify_recorded):
    """Return canonical descriptors with hashes of current, nonempty files."""
    records, errors, seen_files = [], [], {}
    files = case.get("files")
    if not isinstance(files, list):
        return records, ["Cannot inspect files: files is not a list"]
    for index, entry in enumerate(files):
        label = f"files[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        if not nonempty_text(entry.get("role")) or not nonempty_text(entry.get("path")):
            errors.append(f"{label} requires nonempty role and path strings")
            continue
        file_path = Path(entry["path"])
        if not file_path.is_absolute():
            file_path = case_path.parent / file_path
        try:
            if not file_path.is_file():
                errors.append(f"{label}: missing file or not a regular file: {entry['path']}")
                continue
            resolved_path = file_path.resolve()
            if resolved_path in seen_files:
                prior_index, prior_role = seen_files[resolved_path]
                errors.append(
                    f"{label}: duplicate physical file: {entry['path']} resolves to "
                    f"{resolved_path}, already registered as files[{prior_index}] "
                    f"with role {prior_role}; evidence records require distinct files")
                continue
            seen_files[resolved_path] = (index, entry["role"])
            if file_path.stat().st_size == 0:
                errors.append(f"{label}: file is empty: {entry['path']}")
                continue
            actual = hash_file(file_path)
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"{label}: cannot read {entry['path']}: {exc}")
            continue
        records.append({"role": entry["role"], "path": entry["path"], "sha256": actual})
        if verify_recorded and entry.get("sha256") != actual:
            errors.append(f"{label}: stale or missing sha256 for {entry['path']}")
    return records, errors


def fingerprint(case, records):
    payload = {"kind": case["kind"], "scope": case["scope"], "files": records}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_case_atomic(path, case):
    """Do not leave a partially rewritten manifest if writing fails."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".figure-gate-", suffix=".tmp",
                                         delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(case, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
        os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def seal(case, case_path):
    errors = header_errors(case)
    records, file_errors = inspect_files(case, case_path, verify_recorded=False)
    errors.extend(file_errors)
    reviews = case.get("reviews", {})
    if not isinstance(reviews, dict):
        errors.append("reviews must be an object")
    else:
        for name, review in reviews.items():
            if not isinstance(review, dict):
                errors.append(f"reviews.{name} must be an object")
    if errors:
        return {"verdict": "fail", "errors": errors}
    # Preserve entry annotations, existing scores, and check evidence, but no
    # review/check retains pass status after sealing changed or unchanged files.
    for entry, record in zip(case["files"], records):
        entry["sha256"] = record["sha256"]
    case["fingerprint"] = fingerprint(case, records)
    for name in ("scientific", "visual"):
        reviews.setdefault(name, {})
    for review in reviews.values():
        review["status"] = "pending"
        review["fingerprint"] = ""
        checks = review.get("checks", {})
        if isinstance(checks, dict):
            for value in checks.values():
                if isinstance(value, dict):
                    value["status"] = "pending"
    case["reviews"] = reviews
    write_case_atomic(case_path, case)
    return {"verdict": "sealed", "fingerprint": case["fingerprint"],
            "errors": [], "review_status": "pending",
            "note": "Artifacts sealed; independent scientific and visual reviews are still required."}


def review_errors(case, name, required_checks, current_fingerprint):
    errors = []
    reviews = case.get("reviews")
    review = reviews.get(name) if isinstance(reviews, dict) else None
    prefix = f"reviews.{name}"
    if not isinstance(review, dict):
        return [f"{prefix} must be an object"]
    if review.get("status") != "pass":
        errors.append(f"{prefix}.status is not pass (pending/fail reviews block delivery)")
    reviewer = review.get("reviewer")
    if not nonempty_text(reviewer):
        errors.append(f"{prefix}.reviewer must be nonempty")
    elif nonempty_text(case.get("builder")) and reviewer.strip().casefold() == case["builder"].strip().casefold():
        errors.append(f"{prefix}.reviewer must differ from builder")
    if current_fingerprint is not None and review.get("fingerprint") != current_fingerprint:
        errors.append(f"{prefix}.fingerprint is missing or stale")
    checks = review.get("checks")
    if not isinstance(checks, dict):
        errors.append(f"{prefix}.checks must be an object")
    else:
        for key in sorted(required_checks - set(checks)):
            errors.append(f"{prefix}.checks is missing {key}")
        for key, value in checks.items():
            check_prefix = f"{prefix}.checks.{key}"
            if not isinstance(value, dict):
                errors.append(f"{check_prefix} must be an object")
                continue
            if value.get("status") != "pass":
                errors.append(f"{check_prefix}.status is not pass")
            if not nonempty_text(value.get("evidence")):
                errors.append(f"{check_prefix}.evidence must be nonempty")
    if name == "visual":
        scores = review.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"{prefix}.scores must be an object")
        else:
            for key in VISUAL_SCORES:
                value = scores.get(key)
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    errors.append(f"{prefix}.scores.{key} must be a finite number")
                elif not 4 <= value <= 5:
                    errors.append(f"{prefix}.scores.{key} must be 4–5 (local quality threshold, not an award prediction)")
    return errors


def check(case, case_path):
    errors = header_errors(case)
    records, file_errors = inspect_files(case, case_path, verify_recorded=True)
    errors.extend(file_errors)
    kind, scope = case.get("kind"), case.get("scope")
    required_roles = BASE_ROLES | KIND_ROLES.get(kind, set())
    if scope == "paper":
        required_roles |= PAPER_ROLES
    roles = {record["role"] for record in records}
    for role in sorted(required_roles - roles):
        errors.append(f"Missing required file role: {role}")
    files = case.get("files")
    current = None
    if (kind in KIND_ROLES and scope in {"standalone", "paper"}
            and isinstance(files, list) and files and len(records) == len(files)):
        current = fingerprint(case, records)
        if case.get("fingerprint") != current:
            errors.append("fingerprint is missing or stale; seal and repeat independent reviews")
    errors.extend(review_errors(case, "scientific", SCIENTIFIC_CHECKS.get(kind, set()), current))
    errors.extend(review_errors(case, "visual", VISUAL_CHECKS, current))
    warnings = case.get("mechanical_warnings")
    resolutions = case.get("warning_resolutions")
    if not isinstance(warnings, list):
        errors.append("mechanical_warnings must be an explicit list")
    if not isinstance(resolutions, dict):
        errors.append("warning_resolutions must be an object")
    if isinstance(warnings, list):
        for index, warning in enumerate(warnings):
            if not nonempty_text(warning):
                errors.append(f"mechanical_warnings[{index}] must be a nonempty string")
            elif not isinstance(resolutions, dict) or not nonempty_text(resolutions.get(warning)):
                errors.append(f"Unresolved mechanical warning: {warning}")
    issues = case.get("issues", [])
    if not isinstance(issues, list):
        errors.append("issues must be a list when provided")
    else:
        for index, issue in enumerate(issues):
            prefix = f"issues[{index}]"
            if not isinstance(issue, dict):
                errors.append(f"{prefix} must be an object")
                continue
            severity, status = issue.get("severity"), issue.get("status")
            if severity == "hard":
                if status != "resolved":
                    errors.append(f"{prefix}: hard issue must be resolved; accepted is insufficient")
            elif severity == "soft":
                if status not in {"resolved", "accepted"}:
                    errors.append(f"{prefix}: soft issue must be resolved or accepted")
                if not nonempty_text(issue.get("rationale")):
                    errors.append(f"{prefix}: soft issue requires a nonempty rationale")
            else:
                errors.append(f"{prefix}.severity must be hard or soft")
    return {"verdict": "fail" if errors else "pass", "errors": errors,
            "current_fingerprint": current,
            "scope": "Contract, file freshness, and recorded reviews only; not automatic scientific or aesthetic validation."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "check"))
    parser.add_argument("case", type=Path, help="JSON figure review case")
    args = parser.parse_args(argv)
    try:
        path = args.case.resolve()
        case = read_case(path)
        result = seal(case, path) if args.action == "seal" else check(case, path)
    except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
        result = {"verdict": "fail", "errors": [f"Cannot {args.action} case: {exc}"]}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 1 if result["verdict"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
