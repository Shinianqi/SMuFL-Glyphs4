#!/usr/bin/env python3
"""Regenerate every checked-in data file and verify the result.

    python3 tools/build_all.py

Steps:
  1. tools/build_glyphdata.py          -> data/generated/GlyphData-SMuFL.xml
  2. tools/build_groups.py             -> data/generated/Groups-SMuFL.plist
  3. tools/build_glyphnames_snapshot.py-> data/generated/smufl_glyphnames.json
  4. tools/verify.py                   -> consistency checks

The output is deterministic: same inputs, same bytes.  Commit the results so
users never have to run Python to install the data.
"""
from __future__ import annotations

import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    "build_glyphdata.py",
    "build_groups.py",
    "build_glyphnames_snapshot.py",
    "verify.py",
]


def main() -> int:
    for step in STEPS:
        print("\n== " + step)
        result = subprocess.run([sys.executable, os.path.join(TOOLS, step)])
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
