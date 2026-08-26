#!/usr/bin/env python3
"""Pull the room schedule out of the Homestyler DWG - it was there all along.

Homestyler writes a label per room on layer `P-Comment Text` in the form

    Kids Room S:15.28m² C:18.43m

so the drawing carries every room's name, area **and perimeter**, positioned
inside the room. That is the schedule the empty `P-Room` blocks did not have,
and the label position is a seed point for recovering the room polygon.

The plan is repeated once per export sheet, so each label appears several
times; they are bound to a plan instance by position and de-duplicated.

Output is in the same coordinate frame as `data/cad/wall_plan.json`, so the
seeds line up with the wall geometry directly.

Usage:
  python tools/cad/extract_room_labels.py
"""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import ezdxf

REPO = Path(__file__).resolve().parents[2]
DEFAULT_DXF = REPO / "data" / "cad" / "dxf" / "20260727-ZK Dubravinskiy.dxf"
WALL_PLAN = REPO / "data" / "cad" / "wall_plan.json"

LABEL = re.compile(r"^(.+?)\s+S:([0-9.]+)\s*m²\s+C:([0-9.]+)\s*m$")
# The wall-section block's own extents, measured from the geometry.
BLOCK_EXTENT = (-4953.0, -4823.0, 4866.0, 5037.0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dxf", type=Path, default=DEFAULT_DXF)
    ap.add_argument("--wall-plan", type=Path, default=WALL_PLAN)
    ap.add_argument("--out", type=Path, default=REPO / "data" / "cad" / "room_labels.json")
    a = ap.parse_args()

    doc = ezdxf.readfile(str(a.dxf))
    msp = doc.modelspace()

    labels = []
    for e in msp:
        if e.dxftype() not in ("MTEXT", "TEXT") or e.dxf.layer != "P-Comment Text":
            continue
        raw = (e.plain_text() if hasattr(e, "plain_text") else e.dxf.text)
        m = LABEL.match(raw.strip().replace("\n", " "))
        if m:
            labels.append({"x": e.dxf.insert.x, "y": e.dxf.insert.y, "name": m.group(1).strip(),
                           "area_m2": float(m.group(2)), "perimeter_m": float(m.group(3))})

    inserts = list(msp.query('INSERT[layer=="P-Wall-Section"]'))
    anchor = (52274.836, 31819.746)  # the instance the rest of the pipeline uses
    chosen = min(inserts, key=lambda e: math.dist((e.dxf.insert.x, e.dxf.insert.y), anchor))
    cx, cy = chosen.dxf.insert.x, chosen.dxf.insert.y
    bx0, by0, bx1, by1 = BLOCK_EXTENT

    # wall_plan.json places its origin at the minimum corner of the wall outline.
    ox, oy = cx + bx0, cy + by0

    inside = []
    for L in labels:
        dx, dy = L["x"] - cx, L["y"] - cy
        if bx0 - 200 <= dx <= bx1 + 200 and by0 - 200 <= dy <= by1 + 200:
            inside.append(L)

    rooms, seen = [], set()
    for L in sorted(inside, key=lambda r: -r["area_m2"]):
        if L["name"] in seen:
            continue
        seen.add(L["name"])
        rooms.append({
            "name": L["name"],
            "area_m2": L["area_m2"],
            "perimeter_m": L["perimeter_m"],
            "seed_mm": [round(L["x"] - ox, 1), round(L["y"] - oy, 1)],
        })

    plan = json.loads(a.wall_plan.read_text(encoding="utf-8")) if a.wall_plan.exists() else {}
    env = plan.get("envelope_mm", {})
    outside = [r["name"] for r in rooms
               if env and not (0 <= r["seed_mm"][0] <= env.get("width", 0)
                               and 0 <= r["seed_mm"][1] <= env.get("depth", 0))]

    result = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_dxf": str(a.dxf.relative_to(REPO)),
        "layer": "P-Comment Text",
        "frame": "same as data/cad/wall_plan.json - millimetres from the wall outline's minimum corner",
        "instance_insert_mm": [round(cx, 1), round(cy, 1)],
        "labels_found_total": len(labels),
        "labels_in_this_instance": len(inside),
        "rooms": rooms,
        "total_area_m2": round(sum(r["area_m2"] for r in rooms), 2),
        "seeds_outside_envelope": outside,
        "caveats": [
            "Areas and perimeters are Homestyler's own numbers for the OWNER'S layout, not the "
            "developer's. They are clear internal areas as Homestyler computes them.",
            "The seed is where the label sits, which is inside the room but not its centroid.",
        ],
    }
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("%d rooms, total %.2f m2" % (len(rooms), result["total_area_m2"]))
    for r in rooms:
        print("  %-24s S=%6.2f m2  C=%6.2f m  seed (%6.0f, %6.0f)"
              % (r["name"], r["area_m2"], r["perimeter_m"], *r["seed_mm"]))
    if outside:
        print("WARNING seeds outside the wall envelope: %s" % ", ".join(outside))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
