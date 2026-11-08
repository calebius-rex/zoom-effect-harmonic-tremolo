#!/usr/bin/env python3
"""Minimal build entry for the Harmonic effect scaffold."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EFFECT_DIR = ROOT / "src" / "custom" / "harmonic"

def main() -> None:
    print("[harmonic] building scaffold...")
    build_script = EFFECT_DIR / "build.py"
    if not build_script.exists():
        raise FileNotFoundError(f"Missing build script: {build_script}")

    subprocess.run([sys.executable, str(build_script)], check=True, cwd=ROOT)

if __name__ == "__main__":
    main()
