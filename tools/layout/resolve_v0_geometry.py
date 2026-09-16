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
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, os.path.join(REPO, "tools"))
from lib import rectunion as ru  # noqa: E402

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
        # wall_id -> exact PLAN footprint, mitred where it meets the glazing
        # plane. This is the 2D section: a doorway reads as the wall stopping.
        self.plan_polygons = {}
        # wall_id -> the semantic BODY for 3D: the plan polygon extended across
        # any doorway, because the block continues over a door head and a plan
        # cannot say so. The two differ, deliberately, and both are published.
        self.body_polygons = {}
        # elements, each keeping its own semantic id rather than being an
        # anonymous rectangle
        self.openings = []
        self.shafts = []
        self.window_frames = []
        self.loggia_bays = []
        # wall_id -> {face_role: face record}. A locator is
        # host_id + face_ref + along_face_mm + height, with the datum explicit.
        self.faces = {}
        # The ONE transform between drawing millimetres and model metres, on a
        # stable base-wall datum. Published so no consumer reproduces it.
        self.frame = None

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


def glazing_clip(elements):
    """The лоджия glazing plane, as a half-plane a wall is cut on.

    Owner, 2026-09-15: *"M2 and M6b are indeed not squared but inclined - the
    surface is flush with the glazing and the insulation, this is the cut under
    one angle and we have one surface."* The лоджия face is a splay, so a wall
    running into it ends on the slope and an axis-aligned rectangle overshoots
    by a triangle.
    """
    gl = elements.get("loggia_glazing")
    if not gl:
        return None
    a, b = gl["axis_from"], gl["axis_to"]
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    if length <= 0:
        return None
    return (a[0], a[1], -(b[1] - a[1]) / length, (b[0] - a[0]) / length)


def wall_plan_polygon(w, clip):
    """A wall's EXACT plan footprint - mitred where it meets the glazing plane.

    ⚠️ THIS IS WHY IT LIVES HERE. The mitre used to be applied inside the DXF
    serialiser, and `dxf_wall_entities.read_walls` - which validates the mitred
    polygon correctly - then returned only its BOUNDING BOX. `model_from_dxf.py`
    rebuilt each wall as a rectangle from that box, so the IFC silently restored
    the triangles the mitre removes: 5,710 mm² on M2 and 5,707 mm² on M6b,
    pushing both walls back through the glazing plane in 3D.

    Nothing caught it, on either side, and the reason is structural: clipping a
    rectangle on a plane through its corner does NOT change its bounding box, so
    every extent, length and thickness check is blind to it by construction. A
    seeded square-back of M6b in the DXF was rejected only by the stale-review-
    drawing hash, and every wall check passed.

    Returns (polygon, was_mitred, area_cut_mm2).
    """
    x0, y0, x1, y1 = wall_box(w)
    loop = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if not clip:
        return loop, False, 0.0
    cut = ru.clip_halfplane(loop, *clip)
    box_area = (x1 - x0) * (y1 - y0)
    if len(cut) >= 3 and abs(ru._shoelace_area(cut) - box_area) > 1.0:
        return cut, True, box_area - ru._shoelace_area(cut)
    return loop, False, 0.0


OPENINGS_PLACED = _canon("v0_openings_placed.json")
OPENING_NOTES = _canon("wall_openings.csv")
SHAFTS = _canon("ventilation_shafts.csv")
WINDOW_FRAMES = _canon("window_frames.csv")


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def load_openings(glazing=None):
    """Placed openings, with their SEMANTIC IDs, straight from the vector.

    Not anonymous rectangles: every opening keeps `opening_id`, its kind from
    `wall_openings.csv` and the wall the record hosts it in, so a consumer can
    say which opening it is rather than only where it is. ⚠️ O9 is DIAGONAL and
    carries no axis-aligned face pair - it is returned with `axis: DIAGONAL`
    and no polygon, because the лоджия glazing block is the only thing that
    knows its rotation.
    """
    if not os.path.exists(OPENINGS_PLACED):
        return [], []
    notes = {}
    if os.path.exists(OPENING_NOTES):
        with io.open(OPENING_NOTES, encoding="utf-8") as fh:
            notes = {r["opening_id"]: r for r in csv.DictReader(fh)}
    with io.open(OPENINGS_PLACED, encoding="utf-8") as fh:
        placed = json.load(fh)
    out = []
    for o in placed.get("openings", []):
        note = notes.get(o["opening_id"], {})
        rec = {
            "opening_id": o["opening_id"],
            "axis": o.get("axis"),
            "kind": note.get("type", "opening"),
            "recorded_wall": (note.get("in_wall_or_divider") or "").strip(),
            "polygon": None,
        }
        if o.get("axis") == "EW":
            rec["polygon"] = _rect(o["from_mm"], o["face_lo_mm"], o["to_mm"], o["face_hi_mm"])
        elif o.get("axis") == "NS":
            rec["polygon"] = _rect(o["face_lo_mm"], o["from_mm"], o["face_hi_mm"], o["to_mm"])
        elif o.get("axis") == "DIAGONAL" and glazing is not None:
            # O9 is an opening in its own right - owner, 2026-09-15: "draw it as
            # another opening". It was once exported only as frame, bays and
            # mullions, so the single element that actually breaks the лоджия
            # enclosure carried no opening entity at all.
            rec["polygon"] = loggia_band(glazing, 0.0, glazing["run_mm"])
        out.append(rec)
    return out, [u["opening_id"] for u in placed.get("unplaced", [])]


def load_shafts():
    """Ventilation shafts, by id. NOT walls - the DXF legend says so, and
    counting one as wall area would corrupt every finish take-off."""
    if not os.path.exists(SHAFTS):
        return []
    out = []
    with io.open(SHAFTS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append({
                "shaft_id": r["shaft_id"],
                "polygon": _rect(float(r["x0_mm"]), float(r["y0_mm"]),
                                 float(r["x1_mm"]), float(r["y1_mm"])),
                "room": r.get("room", ""),
                "channels": r.get("channels", ""),
            })
    return out


def _opening_verticals(opening_id):
    """(sill_mm, head_mm) for an opening, following leaf suffixes.

    A combined unit is recorded as leaves - O4a the window leaf on its 735
    sill, O4b the full-height door beside it - so the unit's extent is the
    lowest sill to the highest head.
    """
    if not os.path.exists(OPENING_NOTES):
        return None, None
    with io.open(OPENING_NOTES, encoding="utf-8") as fh:
        rows = {r["opening_id"]: r for r in csv.DictReader(fh)}

    def _num(raw):
        if not raw:
            return None
        text = str(raw).strip().rstrip("?")
        try:
            return float(text.split()[0])
        except (ValueError, IndexError):
            return None

    if opening_id in rows:
        return (_num(rows[opening_id].get("sill_height_mm")),
                _num(rows[opening_id].get("head_height_mm")))
    leaves = [v for k, v in rows.items()
              if k.startswith(opening_id) and len(k) == len(opening_id) + 1
              and k[-1].isalpha()]
    sills = [_num(v.get("sill_height_mm")) for v in leaves]
    heads = [_num(v.get("head_height_mm")) for v in leaves]
    sills = [s for s in sills if s is not None]
    heads = [h for h in heads if h is not None]
    return (min(sills) if sills else None), (max(heads) if heads else None)


def load_window_frames(openings):
    """Frame members, each tied to the OPENING it divides.

    The member's vertical extent is the opening's, not the storey's - drawn
    0 to ceiling they read as full-height posts standing in front of each
    window, which is what they did until 2026-09-16.
    """
    if not os.path.exists(WINDOW_FRAMES) or not os.path.exists(OPENINGS_PLACED):
        return []
    with io.open(OPENINGS_PLACED, encoding="utf-8") as fh:
        placed = {o["opening_id"]: o for o in json.load(fh).get("openings", [])}
    out = []
    with io.open(WINDOW_FRAMES, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            o = placed.get(r["opening_id"])
            if not o or o.get("axis") not in ("EW", "NS"):
                continue
            # ⚠️ OPENING-LOCAL 3D, not a plan footprint. A VERTICAL mullion has
            # a horizontal position and runs sill to head; a HORIZONTAL transom
            # has a vertical position measured from the sill and spans the
            # opening's width. Describing both as "a rectangle in plan" is why
            # the transom was silently dropped: it has no plan footprint, so the
            # IFC consumer discarded a member the compiler had resolved. A plan
            # consumer filters members with no plan representation; the IFC
            # takes every one.
            span = float(o["to_mm"]) - float(o["from_mm"])
            sill, head = _opening_verticals(r["opening_id"])
            thickness = float(r["member_mm"])
            rec = {
                "opening_id": r["opening_id"],
                "member": r["member"],
                "axis": r["axis"],
                "member_mm": thickness,
                "sill_mm": sill,
                "head_mm": head,
                "polygon": None,
                "has_plan_footprint": r["axis"] == "vertical",
            }
            if r["axis"] == "vertical":
                centre = float(o["from_mm"]) + span * float(r["position"])
                half = thickness / 2.0
                a, b = centre - half, centre + half
                rec["polygon"] = (_rect(a, o["face_lo_mm"], b, o["face_hi_mm"])
                                  if o["axis"] == "EW"
                                  else _rect(o["face_lo_mm"], a, o["face_hi_mm"], b))
                rec["z_from_mm"], rec["z_to_mm"] = sill, head
                rec["along_opening_mm"] = round(span * float(r["position"]), 1)
            else:
                # The transom spans the full opening width; its POSITION is a
                # fraction of the opening's HEIGHT, measured from the sill.
                rec["polygon"] = (_rect(o["from_mm"], o["face_lo_mm"],
                                        o["to_mm"], o["face_hi_mm"])
                                  if o["axis"] == "EW"
                                  else _rect(o["face_lo_mm"], o["from_mm"],
                                             o["face_hi_mm"], o["to_mm"]))
                if sill is not None and head is not None:
                    centre_z = sill + (head - sill) * float(r["position"])
                    rec["z_from_mm"] = round(centre_z - thickness / 2.0, 1)
                    rec["z_to_mm"] = round(centre_z + thickness / 2.0, 1)
                    rec["height_above_sill_mm"] = round((head - sill) * float(r["position"]), 1)
            out.append(rec)
    return out


def loggia_band(gl, p0, p1):
    """A band across the лоджия glazing assembly, between two positions along
    its own axis. The assembly is DIAGONAL, so this is the only place that
    knows its rotation - which is exactly why it belongs in the compiler."""
    ax, ay = gl["axis_from"]
    bx, by = gl["axis_to"]
    length = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / length, (by - ay) / length
    nx, ny = -uy, ux
    d = gl.get("assembly_depth_mm") or 150.0
    return [(ax + ux * p0, ay + uy * p0),
            (ax + ux * p1, ay + uy * p1),
            (ax + ux * p1 + nx * d, ay + uy * p1 + ny * d),
            (ax + ux * p0 + nx * d, ay + uy * p0 + ny * d)]


def load_loggia_bays(elements):
    """The лоджия glazing's bays and mullions, in their drawn order.

    ⚠️ The BAY COUNT is an assumption, not a measurement. The pattern - full
    height, no parapet, one transom at about 1000 - is confirmed from a
    handover photo of flat 109, whose лоджия is 2.5 m2 against our 6.05, and
    `wall_openings.csv` states that the pattern transfers while the bay count
    and widths do not.
    """
    gl = elements.get("loggia_glazing")
    if not gl:
        return []
    out = []
    for idx, bay in enumerate(gl.get("bays", []), 1):
        out.append({"id": "O9-bay-%d" % idx, "role": "glazing_bay",
                    "from_mm": bay["from_mm"], "to_mm": bay["to_mm"],
                    "polygon": loggia_band(gl, bay["from_mm"], bay["to_mm"])})
    for idx, m in enumerate(gl.get("mullions", []), 1):
        out.append({"id": "O9-mullion-%d" % idx, "role": "glazing_mullion",
                    "from_mm": m["from_mm"], "to_mm": m["to_mm"],
                    "polygon": loggia_band(gl, m["from_mm"], m["to_mm"])})
    return out


def body_polygon(wall_id, plan_poly, was_mitred, extension_rects):
    """The SEMANTIC wall body for 3D, distinct from the plan section for 2D.

    A plan draws a doorway as the wall stopping; the block continues over the
    door head, because this flat has no structural lintels. So the body extends
    across the opening while the plan polygon does not.

    ⚠️ IF A WALL IS BOTH MITRED AND EXTENDED, THIS RAISES rather than guessing.
    An earlier version chose `extended rectangle if extension else mitred
    polygon`, which happens to be right today only because no wall has both -
    and would SILENTLY square a clipped corner the first time one did. That is
    the same failure class as the bug this whole change exists to fix, so it
    fails loudly instead of relying on a coincidence holding.
    """
    if not extension_rects:
        return list(plan_poly), "plan polygon unchanged"
    if was_mitred:
        raise ValueError(
            "wall %s is BOTH mitred on the glazing plane AND extended across an "
            "opening. Unioning a clipped polygon with an extension rectangle is "
            "not implemented, and choosing one over the other would silently "
            "restore the mitred corner. Implement the union before this case "
            "reaches the model." % wall_id)
    x0, y0, x1, y1 = _bbox(plan_poly)
    for rect_poly in extension_rects:
        ex0, ey0, ex1, ey1 = _bbox(rect_poly)
        x0, y0, x1, y1 = min(x0, ex0), min(y0, ey0), max(x1, ex1), max(y1, ey1)
    return _rect(x0, y0, x1, y1), "extended across %d opening(s)" % len(extension_rects)


FACE_ROLES = ("cross_lo", "cross_hi", "end_from", "end_to", "glazing_cut")


def wall_faces(w, plan_poly, was_mitred=False):
    """A wall's faces as STABLE NAMED RECORDS, not polygon indexes or +1/-1.

    ⚠️ "The wall normal" is not uniquely defined once a wall is mitred - M6b has
    five corners, and a service on its glazing-plane face has a different
    outward normal from one on its parallel face. A locator must therefore name
    the face it means:

        host_id + face_ref + along_face_mm + height (with an explicit datum)

    An index into a polygon would not survive the polygon changing; `+1/-1`
    cannot express a third face at all. The names are fixed by ROLE:

      cross_lo / cross_hi  the two long faces, low and high on the cross axis
      end_from / end_to    the two ends, at `from_mm` and `to_mm`
      glazing_cut          the mitred face, present only where a wall is cut
                           on the лоджия glazing plane

    Each record carries ordered endpoints, tangent, outward normal, length and
    role. `along_face_mm` is measured from the face's first endpoint, which is
    why the endpoints are ORDERED and not just a pair.
    """
    x0, y0, x1, y1 = wall_box(w)
    ew = w["axis"] == "EW"
    named = {
        "cross_lo": ((x0, y0), (x1, y0)) if ew else ((x0, y0), (x0, y1)),
        "cross_hi": ((x0, y1), (x1, y1)) if ew else ((x1, y0), (x1, y1)),
        "end_from": ((x0, y0), (x0, y1)) if ew else ((x0, y0), (x1, y0)),
        "end_to": ((x1, y0), (x1, y1)) if ew else ((x0, y1), (x1, y1)),
    }
    centre = ((x0 + x1) / 2.0, (y0 + y1) / 2.0)
    faces = {}
    for role, (a, b) in named.items():
        faces[role] = _face_record(role, a, b, centre)

    if was_mitred and plan_poly:
        # The mitred face is the polygon edge that lies on neither the box's
        # cross faces nor its ends - i.e. the one the clip introduced.
        box_edges = {tuple(sorted([tuple(round(v, 3) for v in a),
                                   tuple(round(v, 3) for v in b)]))
                     for a, b in named.values()}
        best = None
        for i in range(len(plan_poly)):
            a, b = plan_poly[i], plan_poly[(i + 1) % len(plan_poly)]
            key = tuple(sorted([tuple(round(v, 3) for v in a),
                                tuple(round(v, 3) for v in b)]))
            if key in box_edges:
                continue
            if abs(a[0] - b[0]) < 1e-6 or abs(a[1] - b[1]) < 1e-6:
                continue        # still axis-aligned: a shortened box edge
            length = math.hypot(b[0] - a[0], b[1] - a[1])
            if best is None or length > best[0]:
                best = (length, a, b)
        if best:
            faces["glazing_cut"] = _face_record("glazing_cut", best[1], best[2], centre)
    return faces


def _face_record(role, a, b, centre):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    tx, ty = (dx / length, dy / length) if length else (0.0, 0.0)
    nx, ny = -ty, tx
    mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    # point the normal AWAY from the wall's centre
    if (mid[0] - centre[0]) * nx + (mid[1] - centre[1]) * ny < 0:
        nx, ny = -nx, -ny
    return {
        "role": role,
        "endpoints": [tuple(a), tuple(b)],
        "tangent": (round(tx, 9), round(ty, 9)),
        "outward_normal": (round(nx, 9), round(ny, 9)),
        "length_mm": round(length, 3),
    }


def locate_on_face(faces, face_ref, along_face_mm):
    """A host-local locator resolved to drawing coordinates.

    `host_id + face_ref + along_face_mm` is the service locator this project
    needs; the height and its datum are carried separately, because a height is
    not a plan quantity. Raises on an unknown face rather than defaulting to
    one, since defaulting is how a socket ends up on the wrong side of a wall.
    """
    face = faces.get(face_ref)
    if face is None:
        raise KeyError("no face %r on this host; available: %s"
                       % (face_ref, ", ".join(sorted(faces))))
    (ax, ay), _ = face["endpoints"]
    tx, ty = face["tangent"]
    return (ax + tx * along_face_mm, ay + ty * along_face_mm)


class CoordinateFrame(object):
    """The one transform between drawing space and model space.

    ⚠️ THE ORIGIN IS THE BASE-WALL DATUM, NOT "the minimum of whatever geometry
    exists". Taking the minimum would mean that adding insulation, an external
    service, a лоджия extension or any variant primitive OUTSIDE the wall
    envelope silently translates the entire IFC coordinate frame - and every
    previously issued model, annotation and review decision would refer to a
    different place while still loading cleanly. The datum is therefore derived
    from the NAMED WALLS ONLY, which is a stable, gated population, and asserted
    against its recorded contract.

    drawing space: millimetres, on the developer plan's own origin
    model space:   metres, from the base-wall datum
    """

    def __init__(self, origin_mm, units_per_metre=1000.0, datum="base_wall_envelope"):
        self.origin_mm = (float(origin_mm[0]), float(origin_mm[1]))
        self.units_per_metre = float(units_per_metre)
        self.datum = datum

    def drawing_to_model(self, point):
        """Drawing millimetres -> model metres."""
        return ((float(point[0]) - self.origin_mm[0]) / self.units_per_metre,
                (float(point[1]) - self.origin_mm[1]) / self.units_per_metre)

    def model_to_drawing(self, point):
        """Model metres -> drawing millimetres."""
        return (float(point[0]) * self.units_per_metre + self.origin_mm[0],
                float(point[1]) * self.units_per_metre + self.origin_mm[1])

    def as_dict(self):
        return {
            "origin_mm": [round(self.origin_mm[0], 3), round(self.origin_mm[1], 3)],
            "datum": self.datum,
            "drawing_units": "millimetres on the developer plan origin",
            "model_units": "metres from the datum",
            "note": ("derived from the NAMED WALLS only, so a primitive outside the "
                     "wall envelope cannot translate the model frame"),
            "stable_against": "any non-wall addition (gated)",
            "NOT_stable_against": ("adding or correcting a NAMED WALL outside the "
                                   "present envelope - accepted for v0, must be "
                                   "frozen in canonical configuration before "
                                   "variants reuse this compiler"),
        }


def base_wall_datum(walls):
    """The origin: the minimum corner of the NAMED WALL envelope.

    Deliberately not `min()` over every primitive in the model. Insulation,
    services, the лоджия glazing assembly and variant geometry can all lie
    outside the wall envelope, and any of them moving the origin would move the
    whole model.

    ⚠️⚠️ WHAT THIS IS AND IS NOT STABLE AGAINST, stated plainly rather than
    implied. It is stable against ANY non-wall addition - that is gated in
    `scripts/resolve_v0_geometry_selftest.py`, which also proves a
    min()-over-everything datum would have moved.

    It is NOT stable against adding or correcting a NAMED WALL that lies
    outside the present envelope. Such a wall would move the origin, and every
    previously issued IFC and every annotation against it would then refer to a
    different place while still loading cleanly.

    That is accepted for v0, where the 25 named walls are a closed, gated set
    and the envelope is the flat's own. ⚠️ **It must NOT be carried into
    variants**: before a second variant reuses this compiler, freeze the datum
    as an explicit value in canonical configuration and assert against it, so
    that correcting a wall corrects geometry rather than silently re-basing the
    coordinate frame.
    """
    boxes = [wall_box(w) for w in walls if w.get("from_mm") is not None]
    if not boxes:
        raise ValueError("no placed walls: the coordinate datum is undefined")
    return (min(b[0] for b in boxes), min(b[1] for b in boxes))


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
    # EXACT plan footprints, computed once here so the DXF and the IFC draw the
    # same polygon instead of each deriving its own from a bounding box.
    clip = glazing_clip(elements)
    plan = {}
    mitred = []
    for w in walls:
        if w.get("face_lo_mm") is None:
            continue
        poly, was_mitred, cut_mm2 = wall_plan_polygon(w, clip)
        plan[w["wall_id"]] = poly
        if was_mitred:
            mitred.append({"wall_id": w["wall_id"], "corners": len(poly),
                           "area_cut_mm2": round(cut_mm2, 1)})
    report["mitred_walls"] = mitred

    # --- elements, with their semantic ids -------------------------------
    openings, unplaced = load_openings(elements.get("loggia_glazing"))
    shafts = load_shafts()
    frames = load_window_frames(openings)
    bays = load_loggia_bays(elements)

    # Which openings the plan draws as a GAP between wall segments rather than
    # as a void inside one. Those are the walls whose BODY extends across the
    # opening, because the block continues over the door head.
    boxes = {w["wall_id"]: wall_box(w) for w in walls if w.get("from_mm") is not None}

    def _inside(host_box, poly, tol=1.0):
        bx0, by0, bx1, by1 = host_box
        px0, py0, px1, py1 = _bbox(poly)
        return (px0 >= bx0 - tol and px1 <= bx1 + tol
                and py0 >= by0 - tol and py1 <= by1 + tol)

    extensions = {}
    voids = {}
    for o in openings:
        if not o["polygon"]:
            continue
        host = next((wid for wid, bx in boxes.items() if _inside(bx, o["polygon"])), None)
        if host:
            o["hosting"] = "void_in_wall"
            o["host_wall"] = host
            voids.setdefault(host, []).append(o["opening_id"])
        elif o["recorded_wall"] in boxes:
            o["hosting"] = "gap_between_walls"
            o["host_wall"] = o["recorded_wall"]
            extensions.setdefault(o["recorded_wall"], []).append(o)
        else:
            o["hosting"] = "spans_between_elements"
            o["host_wall"] = None

    body = {}
    extension_record = []
    for wid, poly in plan.items():
        rects = [e["polygon"] for e in extensions.get(wid, [])]
        was_mitred = any(m["wall_id"] == wid for m in mitred)
        body[wid], why = body_polygon(wid, poly, was_mitred, rects)
        if rects:
            extension_record.append({
                "wall_id": wid,
                "openings": [e["opening_id"] for e in extensions.get(wid, [])],
                "why": why,
            })
    # Host-local faces, by wall. Named roles, not indexes - see wall_faces.
    faces = {}
    for w in walls:
        if w.get("from_mm") is None:
            continue
        wid = w["wall_id"]
        faces[wid] = wall_faces(w, plan.get(wid),
                                any(m["wall_id"] == wid for m in mitred))

    frame = CoordinateFrame(base_wall_datum(walls))
    report["coordinate_frame"] = frame.as_dict()

    report["body_extensions"] = extension_record
    report["opening_hosting"] = {
        o["opening_id"]: o.get("hosting", "unplaced") for o in openings}
    report["unplaced_openings"] = unplaced
    # ⚠️ TWO COUNTS, both stated. wall_openings.csv holds 11 AUTHORED LEAF
    # records; the model carries 10 PHYSICAL opening units, because O4a and O4b
    # are two leaves of the single hosted opening O4. That is legitimate
    # aggregation, not a missing opening - but an unexplained difference of one
    # is exactly the gap a later omission could hide behind, so both numbers are
    # reported rather than left to be inferred.
    leaf_ids = set()
    if os.path.exists(OPENING_NOTES):
        with io.open(OPENING_NOTES, encoding="utf-8") as fh:
            leaf_ids = {(r["opening_id"] or "").strip()
                        for r in csv.DictReader(fh) if (r["opening_id"] or "").strip()}
    unit_ids = {o["opening_id"] for o in openings}
    aggregated = sorted(
        lid for lid in leaf_ids
        if lid not in unit_ids and lid[:-1] in unit_ids and lid[-1].isalpha())
    report["opening_counts"] = {
        "authored_leaf_records": len(leaf_ids),
        "physical_opening_units": len(openings),
        "aggregated_leaves": aggregated,
        "note": ("%d leaf records aggregate into %d units; %s are leaves of a "
                 "combined unit" % (len(leaf_ids), len(openings),
                                    ", ".join(aggregated) or "none")),
    }

    report["drawn_vs_solid"] = drawn_vs_solid
    report["drawn_vs_solid_within_15mm"] = sum(
        1 for r in drawn_vs_solid if abs(r["delta_mm"]) <= 15.0)

    if verbose:
        print("resolved %d walls; %d movements across %d rules"
              % (len(walls), len(report["movements"]), len(report["rules_in_order"])))

    resolved = ResolvedGeometry(walls, authored, report, elements, blocks, raw)
    resolved.plan_polygons = plan
    resolved.body_polygons = body
    resolved.openings = openings
    resolved.shafts = shafts
    resolved.window_frames = frames
    resolved.loggia_bays = bays
    resolved.faces = faces
    resolved.frame = frame
    return resolved


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
