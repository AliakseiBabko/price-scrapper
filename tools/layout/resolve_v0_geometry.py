# -*- coding: utf-8 -*-
"""THE geometry compiler: canonical authored data -> one resolved model.

WHY THIS EXISTS
---------------
The reconciliation that turns authored facts into geometry - corner closure,
лоджия loop closure, placement yielding and near-miss snapping - lived inside
`export_v0_dxf.py`. That made the DXF the only artefact that knew what the
geometry actually was, so a second consumer had to either re-implement the
reconciliation or read the DXF back. `model_from_dxf.py` does the second, which
is why 2D currently sits between the authored data and the 3D model.

That is the wrong shape. `on_element`, `along_wall_mm`, a wall face, a service
normal and a local->world transform have to mean EXACTLY the same thing in the
IFC and in every discipline sheet, and today only one script knows.

So the reconciliation moves here, and both exporters become serialisers over the
resolved model. This module holds no drawing code and no IFC code on purpose.

WHAT IT RETURNS, AND WHY ALL THREE PARTS
----------------------------------------
`resolve()` returns a `ResolvedGeometry` carrying:

  * `walls`    - the resolved geometry, after every reconciliation rule;
  * `sources`  - the PRE-RECONCILIATION value of every field a rule can move;
  * `report`   - machine-readable: which rule moved what, by how much, and why.

The second and third are not diagnostics. An authored figure carries a
measurement basis, and once closure or snapping has moved it, a consumer that
sees only the final number cannot tell a tape measurement from a value the
compiler nudged 12 mm to close a corner. Keeping the source value and the
rule that moved it is what stops the compiler becoming the same kind of
silent authority the retired schematic was.

WHAT THIS MODULE DOES NOT DO
----------------------------
It does not draw, it does not write IFC, and it does not invent geometry. Every
rule here already existed and is exercised by `check_dxf_closure` (24 seeded
defects), `raster_fidelity` (7), `check_wall_junctions` and
`vector_extent_oracle`. Those gates remain the permanent acceptance - NOT a
diff against the old implementation, because keeping the old reconciliation
around to compare against would make it a second authority, which is the defect
being removed.
"""
from __future__ import annotations

import copy
import csv
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLACED = os.path.join(REPO, "data", "canonical", "v0_named_walls_placed.json")
ELEMENTS = os.path.join(REPO, "data", "canonical", "v0_elements_extracted.json")
BLOCKS = os.path.join(REPO, "data", "canonical", "wall_blocks.csv")

# Fields a reconciliation rule is allowed to move. Snapshotted before any rule
# runs, so the report can state a before and an after for each one.
MUTABLE_FIELDS = ("from_mm", "to_mm", "face_lo_mm", "face_hi_mm", "laid_length_mm")


class ResolvedGeometry(object):
    """The resolved model. Generated data - never authored, never hand-edited."""

    def __init__(self, walls, sources, report, elements, blocks, raw=None):
        self.walls = walls
        self.sources = sources
        self.report = report
        self.elements = elements
        self.blocks = blocks
        # Each rule's own return value, verbatim, for consumers that print it.
        self.raw = raw or {}

    def wall(self, wall_id):
        for w in self.walls:
            if w["wall_id"] == wall_id:
                return w
        return None

    def moved(self, wall_id):
        """Every rule that moved this wall, with before and after.

        The question a consumer actually needs to ask: is this number the one
        that was authored, or one the compiler adjusted?
        """
        return [m for m in self.report["movements"] if m["wall_id"] == wall_id]

    def as_dict(self):
        return {
            "walls": self.walls,
            "sources": self.sources,
            "report": self.report,
        }



def _canon(name):
    return os.path.join(REPO, "data", "canonical", name)


CORNERS = _canon("wall_corners.csv")

# ---------------------------------------------------------------------------
# THE RECONCILIATION RULES. Moved here verbatim from export_v0_dxf.py on
# 2026-09-16; not one line of their logic changed, which is why the 34 seeded
# defects still reject and the DXF is identical to 0.000000 mm. They live here
# because the geometry they decide has to be the same geometry the IFC and
# every discipline sheet see - previously only the DXF exporter knew it.
# ---------------------------------------------------------------------------

def close_corners(walls):
    """Extend each corner OWNER so the corner is solid, not a void.

    Owner, 2026-09-09: *"if I have this corner, R1b and R1a, one of this wall
    should go up to the end of the another one... we need to factor in the
    thickness of the wall to have a closed corner, which is actually the case in
    reality."*

    He is right, and this is the gap between the two lengths the model already
    carries. The walls are laid at their CLEAR run, which is what a tape inside
    the room reads - so every L-corner comes out as an open square. `solid_mm`
    is `clear_mm` plus the corners that wall OWNS, and `wall_corners.csv` says
    who owns which. Applying it here closes every corner with no double count,
    because exactly one of the two walls is extended.
    """
    by_id = {w["wall_id"]: w for w in walls}
    fixes = []
    # !! An explicit owner directive PINS the end it names, and corner closure
    # must not undo it. R9 is the case: the owner set its south face to 7600.6
    # ("not flush with MB, as you can see on the photo"), and close_corners
    # would have pushed it straight back to MB's far face 7560.6 because that
    # is what owning a corner normally means. A derived closure may not
    # overwrite a stated fact - it can only fill what the statement leaves open.
    pinned = set()
    _pd = _canon("wall_placement_directives.csv")
    if os.path.exists(_pd):
        for r in csv.DictReader(io.open(_pd, encoding="utf-8")):
            rel = (r.get("relation") or "").strip()
            if rel.startswith("align_") and (r.get("status") or "").strip() == "accepted":
                pinned.add((r["wall_id"], rel.split("_", 1)[1]))
    if not os.path.exists(CORNERS):
        return fixes
    for r in csv.DictReader(io.open(CORNERS, encoding="utf-8")):
        own, other = by_id.get(r["owner"]), None
        pair = (r["wall_a"], r["wall_b"])
        other_id = pair[1] if r["owner"] == pair[0] else pair[0]
        other = by_id.get(other_id)
        if not own or not other or own.get("from_mm") is None                 or other.get("from_mm") is None:
            continue
        gain = float(r["owner_gains_mm"])
        ob = wall_box(other)
        # the corner sits at whichever end of the owner is nearer the other wall
        lo, hi = (ob[1], ob[3]) if own["axis"] == "NS" else (ob[0], ob[2])
        centre = (lo + hi) / 2.0
        # !! Extend only AS FAR AS the other wall's far face, never by a flat
        # thickness. R8 already spanned MA's band, so adding its full 300 mm gain
        # pushed it 350 mm past the corner and straight into G8 - an overlap the
        # closure gate caught. Clamping makes the corner exactly solid and no
        # more, which is what "owns the corner" means.
        if abs(own["from_mm"] - centre) <= abs(own["to_mm"] - centre):
            target = lo
            if (own["wall_id"], "start") in pinned:
                fixes.append((r["corner_id"], own["wall_id"], other_id, 0.0,
                              "start (PINNED by directive)"))
                continue
            if own["from_mm"] > target:
                own["from_mm"] = round(target, 1)
                end = "start"
            else:
                end = "start (already covered)"
                gain = 0.0
        else:
            target = hi
            if own["to_mm"] < target:
                own["to_mm"] = round(target, 1)
                end = "end"
            else:
                end = "end (already covered)"
                gain = 0.0
        own["closed_corner"] = True
        fixes.append((r["corner_id"], r["owner"], other_id, gain, end))
    return fixes


def yield_to_reference(walls):
    """A wall placed by directive gives way to the accepted geometry it abuts.

    !! M6b is placed from R8's *pre-extension* start, but `close_corners` then
    grows R8 onto MB's face - so R8's DRAWN body ran 50 mm into M6b and the gate
    reported an unsanctioned overlap. Reordering will not help in general: the
    directive is written against a declared face, and corner closure legitimately
    moves drawn extents afterwards.

    The rule is an ordering of authority, not a nudge: a wall positioned BY
    RELATION abuts its reference's drawn extent, keeping its declared face
    alignment and losing length. The trim is reported.

    !! This was keyed on QUARANTINE and should never have been. When M6b's 200 mm
    was confirmed on 2026-09-10 and the quarantine lifted, the yield stopped
    applying and M6b overlapped R8 by 200 x 50 mm - a geometry defect caused by
    TRUSTING a figure, which is nonsense. It is the SECOND appearance of the same
    conflation: `vector_extent_oracle.check()` had it too, found the same day.
    Quarantine asks whether a figure is believed; the directive relation is a fact
    about how the wall is positioned. Key on the relation.
    """
    out = []
    q = [w for w in walls if w.get("placement_directive")]
    if not q:
        return out
    for w in q:
        ref = None
        for o in walls:
            if o is w or o.get("from_mm") is None or o.get("placement_directive"):
                continue
            if o["axis"] != w["axis"]:
                continue
            # collinear: the cross-axis bands must overlap
            if min(o["face_hi_mm"], w["face_hi_mm"]) <= max(o["face_lo_mm"],
                                                            w["face_lo_mm"]):
                continue
            ov = min(o["to_mm"], w["to_mm"]) - max(o["from_mm"], w["from_mm"])
            if ov <= 0:
                continue
            if ref is None or ov > ref[1]:
                ref = (o, ov)
        if ref is None:
            continue
        o, ov = ref
        was = w["to_mm"] - w["from_mm"]
        # trim at the end that meets the accepted wall
        if abs(w["to_mm"] - o["from_mm"]) < abs(w["from_mm"] - o["to_mm"]):
            w["to_mm"] = round(o["from_mm"], 1)
        else:
            w["from_mm"] = round(o["to_mm"], 1)
        w["laid_length_mm"] = round(w["to_mm"] - w["from_mm"], 1)
        w["yielded_mm"] = round(was - w["laid_length_mm"], 1)
        out.append((w["wall_id"], o["wall_id"], w["yielded_mm"],
                    w["laid_length_mm"]))
    return out


SNAP_MM = 25.0     # below this a perpendicular gap is extraction noise


LOGGIA_ENCLOSURE = ('M2', 'M6b')


def close_loggia_loop(walls, gl):
    """Bring the лоджия's enclosure walls down onto the glazing axis.

    !! CODEX round 3, finding 5, and it is right that this is *"locally
    modellable work, not an owner blocker"*: M6b existing did not make the
    лоджия a closed loop. The glazing runs at the drawing's true splay while M2
    and M6b are axis-aligned boxes, and both stopped short of the glazing line -
    M2 by 58 mm, M6b by 291 mm. So the enclosure had a hole at each end and the
    review PNG showed the glazing floating.

    The axis is the DRAWING's, from `loggia_glazing.axis_from/axis_to`, not a
    line fitted to anything here. For each enclosure wall the target is the
    axis's y at the LOWER of its two faces, so the wall's whole thickness meets
    the line rather than just its centreline.
    """
    out = []
    if not gl:
        return out
    ax, ay = gl["axis_from"]
    bx, by = gl["axis_to"]
    if abs(bx - ax) < 1e-6:
        return out

    def y_on_axis(x):
        return ay + (by - ay) * (x - ax) / (bx - ax)

    by_id = {w["wall_id"]: w for w in walls}
    for wid in LOGGIA_ENCLOSURE:
        w = by_id.get(wid)
        if not w or w.get("from_mm") is None or w["axis"] != "NS":
            continue
        target = min(y_on_axis(w["face_lo_mm"]), y_on_axis(w["face_hi_mm"]))
        if w["from_mm"] <= target + 1.0:
            continue                      # already reaches the glazing
        gain = w["from_mm"] - target
        w["from_mm"] = round(target, 1)
        w["laid_length_mm"] = round(w["to_mm"] - w["from_mm"], 1)
        out.append((wid, gain, w["laid_length_mm"]))
    return out


def snap_near_misses(walls):
    """Close a SUB-TOLERANCE perpendicular gap by extending the lesser wall.

    !! MA's top face lands at 9350.3 and R6 starts at 9360.6 - a 10.3 mm butt
    joint the owner would read as one of the cavities he has asked three times to
    be rid of. Nothing caught it, because the near-miss check was documented in
    the closure gate and never implemented.

    10 mm is not a model question. `Geometry_Variance_Study.md` puts the BUILD
    tolerance at +30/-45 mm against three surveyed flats, so a gap an order of
    magnitude below that is noise in the vector extraction, not a design
    decision, and snapping it is a statement about the drawing rather than about
    the flat. A gap ABOVE `SNAP_MM` is left alone deliberately: the closure gate
    fails on it and the owner decides, which is what happened with J_G4a_G4b.

    The wall that yields is the lesser one under the ledger's own ownership rule
    - thinner first, then shorter - so the thicker/longer wall's recorded extent
    is never disturbed.
    """
    out = []
    for i, a in enumerate(walls):
        for b in walls[i + 1:]:
            if a.get("from_mm") is None or b.get("from_mm") is None:
                continue
            if a["axis"] == b["axis"]:
                continue
            ax0, ay0, ax1, ay1 = wall_box(a)
            bx0, by0, bx1, by1 = wall_box(b)
            ix = min(ax1, bx1) - max(ax0, bx0)
            iy = min(ay1, by1) - max(ay0, by0)
            if ix > 1.0 and -SNAP_MM <= iy < 0.0:
                gap, axis_gap = -iy, "y"
            elif iy > 1.0 and -SNAP_MM <= ix < 0.0:
                gap, axis_gap = -ix, "x"
            else:
                continue
            # the lesser wall yields: thinner, then shorter
            ka = (a["face_hi_mm"] - a["face_lo_mm"], a["to_mm"] - a["from_mm"])
            kb = (b["face_hi_mm"] - b["face_lo_mm"], b["to_mm"] - b["from_mm"])
            mover, fixed = (a, b) if ka < kb else (b, a)
            fb = wall_box(fixed)
            lo, hi = ((fb[1], fb[3]) if mover["axis"] == "NS"
                      else (fb[0], fb[2]))
            if abs(mover["from_mm"] - hi) < abs(mover["to_mm"] - lo):
                mover["from_mm"] = round(hi, 1)
            else:
                mover["to_mm"] = round(lo, 1)
            mover["laid_length_mm"] = round(mover["to_mm"] - mover["from_mm"], 1)
            out.append((mover["wall_id"], fixed["wall_id"], gap, axis_gap))
    return out


def wall_box(w):
    """(x0, y0, x1, y1) of a placed wall."""
    if w["axis"] == "EW":
        return w["from_mm"], w["face_lo_mm"], w["to_mm"], w["face_hi_mm"]
    return w["face_lo_mm"], w["from_mm"], w["face_hi_mm"], w["to_mm"]


def _load_blocks():
    with io.open(BLOCKS, encoding="utf-8") as fh:
        return {r["wall_id"]: r for r in csv.DictReader(fh)}


def _snapshot(walls):
    """Pre-reconciliation values of every movable field, by wall id."""
    out = {}
    for w in walls:
        out[w["wall_id"]] = {f: w.get(f) for f in MUTABLE_FIELDS}
    return out


def _movements(before, walls, rule):
    """Which walls this rule actually moved, and by how much.

    Compares field by field rather than trusting the rule's own return value:
    a rule that reports nothing while moving geometry is exactly the failure
    this report exists to make visible.
    """
    moves = []
    for w in walls:
        prev = before.get(w["wall_id"], {})
        for field in MUTABLE_FIELDS:
            old, new = prev.get(field), w.get(field)
            if old is None or new is None:
                continue
            if abs(float(new) - float(old)) > 1e-9:
                moves.append({
                    "wall_id": w["wall_id"],
                    "rule": rule,
                    "field": field,
                    "from": round(float(old), 3),
                    "to": round(float(new), 3),
                    "delta_mm": round(float(new) - float(old), 3),
                })
    return moves


def resolve(verbose=False):
    """Authored data -> resolved geometry, with provenance for every movement.

    The rule ORDER is the existing one and is load-bearing: corners are closed
    before the лоджия loop, the loop before yielding, yielding before snapping.
    Laying at clear and then closing corners is the only order under which a
    wall's drawn extent equals its recorded solid_mm - laying at solid and then
    closing counts the corner twice, which is how R8 once came out 2390 against
    a recorded 2090.
    """
    # The working-directory hazard is fixed AT SOURCE: every canonical path in
    # the rules is now repo-absolute. An earlier version pinned the cwd with
    # os.chdir() instead - that worked, but it mutates process-global state and
    # is unsafe the moment two consumers call the compiler, so it is gone.
    return _resolve_in_repo(verbose)


def _resolve_in_repo(verbose):
    with io.open(PLACED, encoding="utf-8") as fh:
        placed = json.load(fh)
    with io.open(ELEMENTS, encoding="utf-8") as fh:
        elements = json.load(fh)

    walls = placed["walls"]
    sources = _snapshot(walls)
    authored = copy.deepcopy(sources)

    report = {
        "inputs": {
            "placed": os.path.relpath(PLACED, REPO).replace("\\", "/"),
            "elements": os.path.relpath(ELEMENTS, REPO).replace("\\", "/"),
            "blocks": os.path.relpath(BLOCKS, REPO).replace("\\", "/"),
            "placed_authoritative_for": placed.get("authoritative_for"),
        },
        "rules_in_order": [],
        "movements": [],
    }

    # The rules' own return values are kept verbatim. The DXF exporter prints
    # them, and reproducing that output exactly is part of showing the
    # extraction changed nothing: a serialiser that reports differently is a
    # serialiser whose inputs may differ.
    raw = {}
    for name, run in (
        ("close_corners", lambda: close_corners(walls)),
        ("close_loggia_loop", lambda: close_loggia_loop(walls, elements.get("loggia_glazing"))),
        ("yield_to_reference", lambda: yield_to_reference(walls)),
        ("snap_near_misses", lambda: snap_near_misses(walls)),
    ):
        before = _snapshot(walls)
        returned = run()
        raw[name] = returned
        moves = _movements(before, walls, name)
        report["rules_in_order"].append({
            "rule": name,
            "reported": len(returned) if returned is not None else 0,
            "measured_field_changes": len(moves),
        })
        report["movements"].extend(moves)

    blocks = _load_blocks()

    # The standing invariant, computed here so every consumer sees the same
    # verdict rather than reading it off the exporter's console output.
    drawn_vs_solid = []
    for w in walls:
        recorded = blocks.get(w["wall_id"], {}).get("solid_mm")
        if not recorded or w.get("from_mm") is None:
            continue
        drawn = float(w["to_mm"]) - float(w["from_mm"])
        drawn_vs_solid.append({
            "wall_id": w["wall_id"],
            "drawn_mm": round(drawn, 1),
            "solid_mm": float(recorded),
            "delta_mm": round(drawn - float(recorded), 1),
        })
    report["drawn_vs_solid"] = drawn_vs_solid
    report["drawn_vs_solid_within_15mm"] = sum(
        1 for r in drawn_vs_solid if abs(r["delta_mm"]) <= 15.0)

    if verbose:
        print("resolved %d walls; %d movements across %d rules"
              % (len(walls), len(report["movements"]), len(report["rules_in_order"])))

    return ResolvedGeometry(walls, authored, report, elements, blocks, raw)


def main():
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", help="write the reconciliation report as JSON")
    a = ap.parse_args()

    resolved = resolve(verbose=True)
    for rule in resolved.report["rules_in_order"]:
        print("   %-20s reported %2d, measured %2d field change(s)"
              % (rule["rule"], rule["reported"], rule["measured_field_changes"]))
    print("drawn == solid_mm within 15 mm: %d of %d"
          % (resolved.report["drawn_vs_solid_within_15mm"],
             len(resolved.report["drawn_vs_solid"])))

    if a.report:
        os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
        with io.open(a.report, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(resolved.as_dict(), ensure_ascii=False, indent=2))
        print("wrote %s" % a.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
