# -*- coding: utf-8 -*-
"""The canonical structural assemblies - the PHYSICAL elements.

⚠⚠ structural_assemblies.csv says of A_NW_CORNER: *"THIS row is the
physical element for geometry, demolition, reinforcement and IFC"*, and that
R1a/R1b "remain rows in wall_blocks.csv as CALCULATION LEGS for clear-length,
face and quantity work". The IFC had been emitting the legs, which asserts a
joint inside one monolithic pour.
"""
from __future__ import annotations

import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSEMBLIES = os.path.join(REPO, "data", "canonical", "structural_assemblies.csv")
VERTICES = os.path.join(REPO, "data", "canonical", "structural_assembly_vertices.csv")


def load_assemblies(assemblies=ASSEMBLIES, vertices=VERTICES):
    """[{id, kind, members, footprint, thickness_mm}] from canonical data."""
    points = {}
    with io.open(vertices, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            points.setdefault(row["assembly_id"], []).append(
                (int(row["vertex_index"]), float(row["x_mm"]), float(row["y_mm"])))
    out = []
    with io.open(assemblies, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            aid = row["assembly_id"]
            ordered = sorted(points.get(aid, []))
            if not ordered:
                raise ValueError("assembly %s has no footprint vertices" % aid)
            out.append({
                "id": aid, "kind": row.get("kind", ""),
                "members": [m for m in row["member_walls"].split("|") if m],
                "footprint": [(x, y) for _i, x, y in ordered],
                "thickness_mm": None,
            })
    return out
