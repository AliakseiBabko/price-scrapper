#!/usr/bin/env python3
"""Step 4: compile canonical corner ownership into IFC wall connections.

⚠️⚠️ ONE-WAY, ALWAYS
--------------------
    wall_corners.csv  (authoritative)
            ↓
    compiler-resolved junctions
            ↓
    IfcRelConnectsPathElements  (a compiled consequence)

`wall_corners.csv` decides which wall owns each L-corner — thicker, then
longer — and that decision is not revisited here. IFC gets told what was
decided. **There must never be two corner solvers**, and
`check_connections.py` asserts the mapping in both directions so IFC cannot
gain a junction the ledger does not have, nor lose one it does.

⚠️ `C_R1a_R1b` IS NOT A JUNCTION. The ledger records it as
`continuous_casting`: R1a and R1b are legs of ONE monolithic pour
(`structural_assemblies.csv` → `A_NW_CORNER`), and its 250 mm is a one-time
volume allocation so the rectangular-leg arithmetic counts the corner once.
Emitting a connection there would assert a joint in a piece of concrete that
has none.

⚠️⚠️ PRIORITIES ARE DELIBERATELY ABSENT. `RelatingPriorities` and
`RelatedPriorities` are per-material-layer, and this model has single-material
walls with no `IfcMaterialLayerSet` — by design, until the build-ups are
actually known. Writing priorities now would mean inventing layers to attach
them to. They arrive with step 5, derived from the same ledger.

CONNECTION TYPES
  the wall that STOPS on the other   ATSTART or ATEND, whichever end touches
  the wall that RUNS THROUGH (owner) ATPATH
"""
from __future__ import annotations

import csv
import io
import math
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORNERS = os.path.join(REPO, "data", "canonical", "wall_corners.csv")

# ⚠️⚠️ BOTH LISTS ARE EXPLICIT, AND AN UNKNOWN KIND RAISES.
# The first version allow-listed only `L` and silently dropped the three
# `owner_directed` corners - which ARE junctions, recorded as "MC extends onto
# R7 to CLOSE A JUNCTION". A filter that skips what it does not recognise is
# how three real joints went missing without a word.
JUNCTION_KINDS = {"L", "owner_directed"}
NON_JUNCTION_KINDS = {"continuous_casting"}


# ⚠️ Two bands, far apart, so the OWNER always protrudes whatever the walls
# are made of. Within a band the relative order of a wall's own layers is kept,
# so structure still protrudes its own insulation.
RUNNER_BAND = 60
STOPPER_BAND = 20


def _priorities(model, wall, band):
    """One priority per material layer of `wall`, in the ledger's band.

    ⚠️ Returns [] when the wall has no layer set - a priority indexes a layer,
    so there is nothing to index. That is the honest answer for the L-shaped
    casting, which has no uniform build-up.
    """
    import ifcopenshell.util.element as ue
    material = ue.get_material(wall)
    layers = getattr(material, "MaterialLayers", None) if material else None
    if not layers:
        return []
    # keep each wall's own layer order; the band decides who wins the junction
    return [band + (5 if (layer.Name or "") == "substrate" else 0)
            for layer in layers]


def load_corners(path=CORNERS):
    with io.open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _touching_end(faces, wall_id, other_id):
    """Which end of `wall_id` meets `other_id` - 'ATSTART' or 'ATEND'.

    Decided from the RESOLVED faces, so it follows the compiler's geometry
    rather than a second reading of the same inputs.
    """
    mine = faces.get(wall_id) or {}
    theirs = faces.get(other_id) or {}
    if not mine or not theirs:
        return "NOTDEFINED"
    centres = []
    for role, kind in (("end_from", "ATSTART"), ("end_to", "ATEND")):
        face = mine.get(role)
        if face is None:
            continue
        (ax, ay), (bx, by) = face["endpoints"]
        centres.append((kind, ((ax + bx) / 2.0, (ay + by) / 2.0)))
    if not centres:
        return "NOTDEFINED"
    points = []
    for face in theirs.values():
        points.extend(face["endpoints"])
    best, best_distance = "NOTDEFINED", None
    for kind, centre in centres:
        distance = min(math.dist(centre, p) for p in points)
        if best_distance is None or distance < best_distance:
            best, best_distance = kind, distance
    return best


def apply_connections(model, resolved):
    """Emit one connection per junction corner. Returns a summary."""
    walls = dict((w.Name, w) for w in model.by_type("IfcWall")
                 if not w.is_a("IfcWallType"))
    faces = resolved.faces
    made, skipped, missing = [], [], []

    for row in load_corners():
        kind = (row.get("kind") or "").strip()
        a, b = row["wall_a"].strip(), row["wall_b"].strip()
        owner = (row.get("owner") or "").strip()
        if kind in NON_JUNCTION_KINDS:
            # ⚠️ NOT a junction, and deliberately so - recorded rather than
            # quietly filtered.
            skipped.append((row["corner_id"], kind))
            continue
        if kind not in JUNCTION_KINDS:
            raise ValueError(
                "corner %s has kind %r, which is neither a declared junction "
                "nor a declared non-junction. An unrecognised kind must FAIL, "
                "never be skipped - three owner_directed junctions went "
                "missing that way" % (row["corner_id"], kind))
        if a not in walls or b not in walls:
            missing.append(row["corner_id"])
            continue
        stopper = b if owner == a else a
        runner = owner
        connection = model.create_entity(
            "IfcRelConnectsPathElements",
            GlobalId="0" * 22,          # ⚠️ replaced by the identity pass
            Name=row["corner_id"],
            Description=("compiled from wall_corners.csv: %s runs through, "
                         "%s stops on it" % (runner, stopper)),
            RelatingElement=walls[stopper],
            RelatedElement=walls[runner],
            RelatingConnectionType=_touching_end(faces, stopper, runner),
            RelatedConnectionType="ATPATH",
            # ⚠️⚠️ PRIORITIES COMPILED FROM THE LEDGER, NOT DECIDED HERE.
            # IFC resolves a junction by letting the HIGHER priority protrude.
            # wall_corners.csv already decided who runs through, so the owner's
            # layers are given the higher band and the stopper's the lower.
            # The ledger's decision therefore SURVIVES into IFC rather than
            # being re-derived from thickness or material - which would be the
            # second corner solver this whole step exists to prevent.
            # IfcRelConnectsPathElements priorities OVERRIDE the general layer
            # priorities for this connection, which is exactly what is wanted.
            RelatingPriorities=_priorities(model, walls[stopper], STOPPER_BAND),
            RelatedPriorities=_priorities(model, walls[runner], RUNNER_BAND),
        )
        made.append((row["corner_id"], stopper, runner,
                     connection.RelatingConnectionType))

    return {"connections": len(made),
            "not_junctions": [c for c, _k in skipped],
            "walls_absent": missing,
            "detail": made}
