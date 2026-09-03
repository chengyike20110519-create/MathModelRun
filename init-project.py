#!/usr/bin/env python3
"""Convenience wrapper to scaffold a new math modeling project."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "my-mathmodel-agent" / "scripts" / "init_project.py"

if __name__ == "__main__":
    subprocess.run([sys.executable, str(SCRIPT), *sys.argv[1:]])
