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


def check_competition_template(competition):
    repo = Path(__file__).resolve().parents[2]
    templates = {
        "cumcm": repo / "templates" / "paper" / "cumcm.typ",
        "mcm": repo / "templates" / "paper" / "mcm.typ",
        "himcm": repo / "templates" / "paper" / "himcm.typ",
    }
    if competition not in templates:
        print(f"[template] unknown competition {competition}")
        return False
    present = templates[competition].exists()
    print(f"[template] {competition}: {'OK' if present else 'MISSING'}")
    return present


def main():
    parser = argparse.ArgumentParser(description="MathModel environment doctor")
    parser.add_argument("--skip-tools", action="store_true", help="skip external tool checks")
    parser.add_argument("--competition", choices=["cumcm", "mcm", "himcm"], help="check template for a competition")
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

    if args.competition:
        # Templates are optional; only fail if not present when explicitly requested.
        check_competition_template(args.competition)

    print()
    if ok:
        print("doctor: environment is ready for MyMathModelAgent")
        return 0
    else:
        print("doctor: some required components are missing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
