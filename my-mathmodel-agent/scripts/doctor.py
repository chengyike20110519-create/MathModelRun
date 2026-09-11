#!/usr/bin/env python3
"""Environment diagnostic for math modeling contest projects."""
import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


def check_python():
    print(f"[python] {sys.version.split()[0]}")
    if sys.version_info < (3, 9):
        print("  ERROR: Python 3.9+ required")
        return False
    print("  OK")
    return True


def check_package(name, optional=False):
    spec = importlib.util.find_spec(name)
    status = "OK" if spec else ("OPTIONAL" if optional else "MISSING")
    print(f"[pkg] {name}: {status}")
    return optional or spec is not None


def check_tool(name, optional=False):
    path = shutil.which(name)
    status = "OK" if path else ("OPTIONAL" if optional else "MISSING")
    print(f"[tool] {name}: {status}")
    return optional or path is not None


def check_templates():
    repo = Path(__file__).resolve().parents[2]
    templates_dir = repo / "templates"
    if not templates_dir.exists():
        print(f"[template] templates/ directory missing")
        return False
    count = sum(1 for _ in templates_dir.glob("*.json"))
    print(f"[template] {count} JSON templates found in templates/")
    return count > 0


def main():
    parser = argparse.ArgumentParser(description="MathModel environment doctor")
    parser.add_argument("--skip-tools", action="store_true", help="skip external tool checks")
    parser.add_argument("--competition", help="check template for a competition (no-op, templates are generic)")
    args = parser.parse_args()

    ok = True
    ok &= check_python()
    ok &= check_package("numpy")
    ok &= check_package("scipy")
    ok &= check_package("pandas")
    ok &= check_package("matplotlib")
    ok &= check_package("openpyxl", optional=True)

    if not args.skip_tools:
        ok &= check_tool("git")
        ok &= check_tool("python3")
        ok &= check_tool("typst", optional=True)
        ok &= check_tool("latexmk", optional=True)
        ok &= check_tool("pandoc", optional=True)

    check_templates()

    print()
    if ok:
        print("doctor: environment is ready for MathModel Run")
        return 0
    else:
        print("doctor: some required components are missing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
