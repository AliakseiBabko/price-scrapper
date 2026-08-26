#!/usr/bin/env python3
"""Rebuild everything from the CAD export, in order, in one command.

The chain has five links and each one feeds the next. Running them by hand in
the wrong order silently produces a spec with no rooms, or a variant built on a
stale shell, so the order lives here rather than in someone's memory:

    wall plan   ->  room labels  ->  base spec  ->  shell + variant  ->  rooms
    (geometry)      (schedule)       (walls)        (split)             (injected)

Then build the owner variant so the drawings match the model that produced them.

Usage:
  python tools/cad/rebuild_from_cad.py            # everything
  python tools/cad/rebuild_from_cad.py --no-build # data only, skip the drawings
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IFC_PY = REPO / ".venv-ifc314" / "Scripts" / "python.exe"
DOC_PY = REPO / ".venv" / "Scripts" / "python.exe"

STEPS = [
    ("extract wall plan", IFC_PY, "tools/cad/extract_wall_plan.py"),
    ("extract room labels", IFC_PY, "tools/cad/extract_room_labels.py"),
    ("base spec from CAD", IFC_PY, "tools/cad/build_base_spec_from_cad.py"),
    ("split shell/partitions", IFC_PY, "tools/cad/split_shell_and_partitions.py"),
    ("grow room polygons", DOC_PY, "tools/cad/build_rooms_from_seeds.py"),
    ("inject rooms", DOC_PY, "tools/cad/inject_rooms.py"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-build", action="store_true", help="stop before drawing anything")
    ap.add_argument("--variant", default="v1-homestyler")
    a = ap.parse_args()

    for label, interpreter, script in STEPS:
        proc = subprocess.run([str(interpreter), str(REPO / script)], cwd=str(REPO),
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
        status = "ok" if proc.returncode == 0 else "FAILED"
        print("  %-24s %s" % (label, status))
        if proc.returncode != 0:
            print(proc.stderr[-1200:])
            return 1
        for line in (proc.stdout or "").splitlines():
            if line.strip().startswith(("slivers", "WARNING", "openings with")):
                print("      " + line.strip())

    if a.no_build:
        return 0
    proc = subprocess.run([str(DOC_PY), str(REPO / "tools/layout/make_variant.py"),
                           a.variant, "--no-blend"], cwd=str(REPO))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
