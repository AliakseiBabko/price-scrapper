#!/usr/bin/env python3
"""Assert the generated IFC back against the canonical tables it claims to come from.

`model_from_dxf.py` builds the model from the gated DXF and the canonical CSVs.
That is only worth anything if the result is checked: the defect this whole
exercise started from - a schematic silently disagreeing with the measured
geometry - was invisible precisely because NOTHING read the file the model was
built from. A generator with no gate is the same arrangement with a new file.

Checks, all of them against a table the generator does not own:

  1. Every wall in `wall_blocks.csv` is present in the IFC, exactly once.
  2. Each wall's DRAWN thickness matches its recorded `thickness_mm`.
  3. Each opening's sill and head match `wall_openings.csv`, where recorded.
  4. Both ventilation shafts are present, and are NOT walls.
  5. Every opening fill sits within its own vertical span.

⚠️ READ THE SHAPE INTO A LOCAL FIRST. `create_shape(...).geometry` returns a
buffer owned by the shape element; chaining lets the element be collected and
the buffer reads back EMPTY with no error, so every measurement silently
becomes zero. That cost an hour on 2026-09-16 and is why `_verts` exists.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
BLOCKS = REPO / "data" / "canonical" / "wall_blocks.csv"
OPENINGS = REPO / "data" / "canonical" / "wall_openings.csv"

THICKNESS_TOL_MM = 2.0     # the DXF rounds to 0.1 mm; 2 mm is generous and still tight
VERTICAL_TOL_MM = 5.0


def _verts(settings, element) -> np.ndarray:
    """The shape must stay referenced while its buffer is read. See the module note."""
    import ifcopenshell.geom

    shape = ifcopenshell.geom.create_shape(settings, element)
    return np.array(shape.geometry.verts).reshape(-1, 3)


def parse_mm(raw):
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    m = re.match(r"^(-?\d+(?:\.\d+)?)", text.rstrip("?"))
    return float(m.group(1)) if m else None


def check(ifc_path: Path) -> list[str]:
    import ifcopenshell
    import ifcopenshell.geom

    problems: list[str] = []
    model = ifcopenshell.open(str(ifc_path))
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    # 1 + 2 - walls against wall_blocks.csv
    recorded = {}
    with BLOCKS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            recorded[row["wall_id"]] = parse_mm(row.get("thickness_mm"))

    seen: dict[str, int] = {}
    for wall in model.by_type("IfcWall"):
        seen[wall.Name] = seen.get(wall.Name, 0) + 1

    for wid in recorded:
        count = seen.get(wid, 0)
        if count == 0:
            problems.append("wall %s is in wall_blocks.csv but not in the IFC" % wid)
        elif count > 1:
            problems.append("wall %s appears %d times in the IFC" % (wid, count))
    for name in seen:
        if name not in recorded:
            problems.append("IFC carries wall %s, which wall_blocks.csv does not" % name)

    for wall in model.by_type("IfcWall"):
        want = recorded.get(wall.Name)
        if want is None:
            continue
        v = _verts(settings, wall)
        if not len(v):
            problems.append("wall %s has no geometry" % wall.Name)
            continue
        size = v.max(0) - v.min(0)
        drawn = min(size[0], size[1]) * 1000.0
        if abs(drawn - want) > THICKNESS_TOL_MM:
            problems.append("wall %s drawn %.1f mm thick, wall_blocks.csv records %.1f"
                            % (wall.Name, drawn, want))

    # 3 - opening verticals against wall_openings.csv
    want_open = {}
    with OPENINGS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            oid = (row["opening_id"] or "").strip()
            if oid:
                want_open[oid] = (parse_mm(row.get("sill_height_mm")),
                                  parse_mm(row.get("head_height_mm")))

    for cls in ("IfcWindow", "IfcDoor"):
        for fill in model.by_type(cls):
            oid = (fill.Name or "").split()[0]
            if oid not in want_open:
                continue
            sill, head = want_open[oid]
            v = _verts(settings, fill)
            if not len(v):
                problems.append("opening fill %s has no geometry" % fill.Name)
                continue
            lo, hi = v[:, 2].min() * 1000.0, v[:, 2].max() * 1000.0
            if sill is not None and abs(lo - sill) > VERTICAL_TOL_MM:
                problems.append("%s sill drawn %.0f mm, wall_openings.csv records %.0f"
                                % (oid, lo, sill))
            if head is not None and abs(hi - head) > VERTICAL_TOL_MM:
                problems.append("%s head drawn %.0f mm, wall_openings.csv records %.0f"
                                % (oid, hi, head))

    # 4 - ventilation shafts present, and not counted as walls
    shafts = [p for p in model.by_type("IfcBuildingElementProxy")
              if (p.Name or "").startswith("Vent shaft")]
    if len(shafts) != 2:
        problems.append("expected 2 ventilation shafts, found %d" % len(shafts))
    for wall in model.by_type("IfcWall"):
        if (wall.Name or "").startswith("Vent shaft"):
            problems.append("ventilation shaft %s is modelled as a wall" % wall.Name)

    # 5 - a fill must sit inside its own opening
    for rel in model.by_type("IfcRelFillsElement"):
        op, fill = rel.RelatingOpeningElement, rel.RelatedBuildingElement
        if op is None or fill is None:
            continue
        vo, vf = _verts(settings, op), _verts(settings, fill)
        if not len(vo) or not len(vf):
            continue
        if (abs(vf[:, 2].min() - vo[:, 2].min()) > VERTICAL_TOL_MM / 1000.0
                or abs(vf[:, 2].max() - vo[:, 2].max()) > VERTICAL_TOL_MM / 1000.0):
            problems.append("%s does not sit in its own opening" % fill.Name)

    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ifc", type=Path,
                    default=REPO / "data" / "outputs" / "variants" / "v0-existing" / "model.ifc")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    problems = check(a.ifc)
    if a.json:
        print(json.dumps({"ifc": str(a.ifc), "problems": problems,
                          "passed": not problems}, ensure_ascii=False, indent=2))
    else:
        for p in problems:
            print("  " + p)
        print("%s: %d problem(s)" % (a.ifc.name, len(problems)))
        print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
