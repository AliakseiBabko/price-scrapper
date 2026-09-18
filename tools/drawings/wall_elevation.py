#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Internal wall elevation (развёртка) of ONE room face, drawn from the compiler.

WHY THIS EXISTS, AND WHY IT READS THE COMPILER
----------------------------------------------
The owner's question of 2026-09-18 is whether the 9.36 room's window can grow
into the solid wall beside it. That is an ELEVATION question - width against
height, opening against what is left of the wall - and this project had no tool
that draws an elevation. It had `check_room_rollout.py`, which CHECKS a rollout,
and nothing that renders one.

⚠️⚠️ IT READS `ResolvedGeometry` DIRECTLY AND NEVER A STORED ARTEFACT. On
2026-09-18 both review engines found the same defect one output downstream: the
committed GLB painted 18 walls while the IFC beside it carried 24, and the
viewer loaded it with no freshness check. A drawing built from a stored spec
would inherit exactly that. Here the geometry is recompiled on every run, so the
picture cannot be older than the model.

⚠️ VERTICALS ARE NOT IN THE PLAN COMPILER. `ResolvedGeometry` resolves the plan;
sill and head heights live in `wall_openings.csv` and the mullion split in
`window_frames.csv`. Those are joined here, and an opening with no recorded
vertical is drawn as a FULL-HEIGHT HATCHED UNKNOWN rather than given a guessed
sill - inventing one is the failure standing rule 9 exists for.

⚠️⚠️ THE CHAIN MUST CLOSE OR NOTHING IS DRAWN. The face segments plus the
openings must sum to the room's clear span to CLOSURE_MM. A развёртка that does
not close is the defect `check_room_rollout.py` was written to catch, and a
renderer that silently draws one would hand back a picture that looks right.
"""

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from lib.tabular import read_csv, finite          # noqa: E402
import resolve_v0_geometry as R                   # noqa: E402

CANON = os.path.join(REPO, "data", "canonical")

# The chain must close to better than this. It is far tighter than the +/-50 mm
# BUILD tolerance on purpose: these are two readings of ONE compiled model, not
# two measurements of a building, so any disagreement is an arithmetic error.
CLOSURE_MM = 0.5

# Drawing
PX_PER_MM = 0.30
MARGIN = 118.0
# ⚠ The canvas was first sized from the WALL alone, so at 2825 mm it came out
# 579 px wide and the title, the notes and half the labels ran off the edge.
# A drawing whose text does not fit is not a drawing. The page is therefore at
# least this wide whatever the wall measures.
MIN_PAGE_PX = 1500.0

MATERIAL_FILL = {
    "concrete": "#b9bec6",
    "external": "#e6dfd2",
    "aerated_block": "#efe7d7",
    "loggia_enclosure": "#dfe6e6",
}
MATERIAL_LABEL = {
    "concrete": "монолит — RC frame",
    "external": "газоблок 300 — не несущая",
    "aerated_block": "газоблок",
    "loggia_enclosure": "ограждение лоджии",
}


class ClosureError(Exception):
    pass


# ---------------------------------------------------------------------------
# Geometry assembly
# ---------------------------------------------------------------------------

def _face_coord(wall, axis):
    """The coordinate of the face this wall presents, on the room's side."""
    return wall["face_hi_mm"], wall["face_lo_mm"]


def segments_along(geom, face_axis, face_coord, x0, x1):
    """Every wall presenting a face at `face_coord` between x0 and x1.

    A room face is rarely one wall. The 9.36 room's south face is MA for
    2650.1 mm and then the END of R8 for 175.0 mm - and R8 is concrete where MA
    is block, which is the whole answer to whether the opening can grow that
    way. A renderer that assumed one wall per face would have drawn that
    boundary as a single material and lost the finding.
    """
    out = []
    for w in geom.walls:
        if w["axis"] == face_axis:
            # A wall running ALONG the face: it presents a long face here.
            lo, hi = w["face_lo_mm"], w["face_hi_mm"]
            if abs(lo - face_coord) > CLOSURE_MM and abs(hi - face_coord) > CLOSURE_MM:
                continue
            a, b = w["from_mm"], w["to_mm"]
        else:
            # A wall running INTO the face: it presents its END here.
            a, b = w["face_lo_mm"], w["face_hi_mm"]
            ends = (w["from_mm"], w["to_mm"])
            if min(abs(ends[0] - face_coord), abs(ends[1] - face_coord)) > CLOSURE_MM:
                continue
        a, b = max(a, x0), min(b, x1)
        if b - a > CLOSURE_MM:
            out.append({"wall_id": w["wall_id"], "class": w["class"],
                        "x0": a, "x1": b, "length_mm": b - a})
    out.sort(key=lambda s: s["x0"])
    return out


def openings_along(geom, face_axis, face_coord, x0, x1):
    """Openings whose host wall presents this face, clipped to the span."""
    hosts = {s["wall_id"] for s in segments_along(geom, face_axis, face_coord, x0, x1)}
    out = []
    for o in geom.openings:
        if o.get("host_wall") not in hosts:
            continue
        xs = [p[0] for p in o["polygon"]] if face_axis == "EW" else [p[1] for p in o["polygon"]]
        a, b = min(xs), max(xs)
        # ⚠ DO NOT CLIP TO THE SPAN. An earlier version returned
        # max(a, x0)..min(b, x1), which quietly trimmed any opening that ran
        # past the room boundary - and that made the bounds check in build()
        # UNREACHABLE, a check that could never fire. An opening crossing the
        # boundary is not a drawing nuisance to be tidied away; it means the
        # opening and the span disagree about where the room ends, and the
        # caller has to hear about it. Overlap is enough to include it.
        if min(b, x1) - max(a, x0) > CLOSURE_MM:
            out.append({"opening_id": o["opening_id"], "x0": a, "x1": b,
                        "host_wall": o["host_wall"], "width_mm": b - a})
    out.sort(key=lambda o: o["x0"])
    return out


def _verticals():
    """sill and head per opening leaf, from the authored record.

    Returns {opening_id: {"sill_mm", "head_mm", "type", "uncertain"}}. A figure
    the record marks with '?' is carried through as UNCERTAIN rather than
    silently cleaned - the drawing says so, because O2's sill and head are
    DERIVED and the record is explicit about it.
    """
    out = {}
    for r in read_csv(os.path.join(CANON, "wall_openings.csv")):
        oid = (r.get("opening_id") or "").strip()
        if not oid:
            continue
        sill_raw = (r.get("sill_height_mm") or "").strip()
        head_raw = (r.get("head_height_mm") or "").strip()
        uncertain = "?" in sill_raw or "?" in head_raw
        sill = finite(sill_raw.replace("?", "") or "nan")
        head = finite(head_raw.replace("?", "") or "nan")
        out[oid] = {"sill_mm": sill, "head_mm": head, "uncertain": uncertain,
                    "type": (r.get("type") or "").strip(),
                    "host": (r.get("in_wall_or_divider") or "").strip()}
    return out


def leaves_for(opening_id, verticals):
    """The leaves of a compound opening, e.g. O4 -> O4a (window) + O4b (door).

    The plan compiler resolves O4 as ONE void, which is correct: it is one hole
    in one wall. The RECORD splits it into leaves because they have different
    sills - and the sill is the whole question when something sits under it.
    """
    kids = sorted(k for k in verticals
                  if k != opening_id and k.startswith(opening_id)
                  and k[len(opening_id):].isalpha())
    return kids or [opening_id]


def build(geom, face_axis, face_coord, x0, x1):
    segs = segments_along(geom, face_axis, face_coord, x0, x1)
    ops = openings_along(geom, face_axis, face_coord, x0, x1)
    span = x1 - x0

    # ⚠️⚠️ CLOSURE, AND IT HAD TO BE WRITTEN TWICE.
    # The first version summed the gaps between successive marks and compared
    # that to the span. That sum TELESCOPES - it equals the span for any marks
    # whatever - so it could not fail on any input and would have reported a
    # closed chain on a broken face. `Validator_Design_Discipline.md` names this
    # class outright: a seed that cannot fail is worse than no seed. What
    # follows checks the two things that can actually be wrong.

    # 1. The openings must be disjoint and inside the span. Two overlapping
    #    voids would double-count a hole and still "sum" correctly above.
    for o in ops:
        if o["x0"] < x0 - CLOSURE_MM or o["x1"] > x1 + CLOSURE_MM:
            raise ClosureError(
                "opening %s runs outside the clear span (%.1f..%.1f against "
                "%.1f..%.1f)" % (o["opening_id"], o["x0"], o["x1"], x0, x1))
    for a, b in zip(ops, ops[1:]):
        if b["x0"] < a["x1"] - CLOSURE_MM:
            raise ClosureError(
                "openings %s and %s overlap by %.1f mm"
                % (a["opening_id"], b["opening_id"], a["x1"] - b["x0"]))

    # 2. The wall faces must TILE the span - no gap, no overlap. This is the
    #    real closure, and it is the check that proves the face is made of
    #    walls the compiler actually resolves rather than of an assumption.
    cursor = x0
    for s in segs:
        if s["x0"] > cursor + CLOSURE_MM:
            raise ClosureError(
                "a %.1f mm gap in the face at x %.1f: no resolved wall presents "
                "a face there. Either a wall does not reach this face, or the "
                "span is wrong." % (s["x0"] - cursor, cursor))
        cursor = max(cursor, s["x1"])
    if abs(cursor - x1) > CLOSURE_MM:
        raise ClosureError(
            "the face is not fully made of walls: wall faces reach x %.1f of a "
            "span ending at %.1f (%.1f mm unaccounted)." % (cursor, x1, x1 - cursor))

    covered = sum(s["length_mm"] for s in segs)
    if covered > span + CLOSURE_MM:
        raise ClosureError(
            "wall faces OVERLAP on this face: %.1f mm of wall over a %.1f mm "
            "span. Two walls claiming the same face means the corner ledger and "
            "this span disagree." % (covered, span))

    return {"segments": segs, "openings": ops, "x0": x0, "x1": x1, "span_mm": span,
            "face_axis": face_axis, "face_coord": face_coord}


def ceiling_mm():
    """Clear height from the canonical record - screed top to ceiling underside.

    ⚠ NOT slab-to-slab (~2550), which would silently add the slab. The record
    settles this explicitly and the distinction has already cost this project
    one correction.
    """
    import json
    with open(os.path.join(CANON, "building_spec.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    return float(spec["ceiling_height_mm"]["this_flat"])


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------

def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Canvas(object):
    def __init__(self, span_mm, height_mm):
        self.sx = span_mm * PX_PER_MM
        self.sy = height_mm * PX_PER_MM
        self.h_mm = height_mm
        self.parts = []
        self.w = max(self.sx + 2 * MARGIN, MIN_PAGE_PX)
        # Centre the wall on the page when the text, not the wall, sets the width.
        self.pad = (self.w - self.sx) / 2.0
        self.h = self.sy + 2 * MARGIN + 150

    def X(self, mm):
        return self.pad + mm * PX_PER_MM

    def Y(self, mm):
        """Millimetres ABOVE THE SCREED -> pixels down. The datum is the screed,
        which is what every sill and head in the record is measured from."""
        return MARGIN + (self.h_mm - mm) * PX_PER_MM

    def rect(self, x0, x1, y0, y1, fill, stroke="#333", sw=1.0, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.parts.append(
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
            'stroke="%s" stroke-width="%.2f"%s/>'
            % (self.X(x0), self.Y(y1), (x1 - x0) * PX_PER_MM,
               (y1 - y0) * PX_PER_MM, fill, stroke, sw, d))

    def line(self, x0, y0, x1, y1, stroke="#333", sw=1.0, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.parts.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="%.2f"%s/>'
            % (self.X(x0), self.Y(y0), self.X(x1), self.Y(y1), stroke, sw, d))

    def text(self, x_mm, y_mm, s, size=11, anchor="middle", fill="#111",
             weight="normal", dy=0.0):
        self.parts.append(
            '<text x="%.2f" y="%.2f" font-family="Segoe UI,Arial,sans-serif" '
            'font-size="%d" text-anchor="%s" fill="%s" font-weight="%s">%s</text>'
            % (self.X(x_mm), self.Y(y_mm) + dy, size, anchor, fill, weight, _esc(s)))

    def text_px(self, px, py, s, size=11, anchor="start", fill="#111", weight="normal"):
        self.parts.append(
            '<text x="%.2f" y="%.2f" font-family="Segoe UI,Arial,sans-serif" '
            'font-size="%d" text-anchor="%s" fill="%s" font-weight="%s">%s</text>'
            % (px, py, size, anchor, fill, weight, _esc(s)))

    def dim(self, x0, x1, y_mm, label, colour="#b03030", tick=26.0):
        """A dimension WITH ITS EXTENSION LINES DRAWN. Standing rule 9 says a
        dimension is read by the two elements its extension lines terminate on,
        so a drawing that omits them cannot be read correctly."""
        y = self.Y(y_mm)
        for x in (x0, x1):
            self.parts.append(
                '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                'stroke-width="0.8"/>' % (self.X(x), y - tick / 2, self.X(x), y + tick / 2, colour))
        self.parts.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="0.9" marker-start="url(#a)" marker-end="url(#a)"/>'
            % (self.X(x0), y, self.X(x1), y, colour))
        self.text_px((self.X(x0) + self.X(x1)) / 2.0, y - 5, label,
                     size=11, anchor="middle", fill=colour, weight="bold")

    def vdim(self, x_mm, y0, y1, label, colour="#b03030"):
        x = self.X(x_mm)
        for y in (y0, y1):
            self.parts.append(
                '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                'stroke-width="0.8"/>' % (x - 13, self.Y(y), x + 13, self.Y(y), colour))
        self.parts.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="0.9" marker-start="url(#a)" marker-end="url(#a)"/>'
            % (x, self.Y(y0), x, self.Y(y1), colour))
        self.parts.append(
            '<text x="%.2f" y="%.2f" font-family="Segoe UI,Arial,sans-serif" '
            'font-size="11" text-anchor="middle" fill="%s" font-weight="bold" '
            'transform="rotate(-90 %.2f %.2f)">%s</text>'
            % (x - 4, (self.Y(y0) + self.Y(y1)) / 2.0, colour, x - 4,
               (self.Y(y0) + self.Y(y1)) / 2.0, _esc(label)))

    def svg(self, title, subtitle, notes):
        head = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
            'viewBox="0 0 %.0f %.0f">'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#b03030"/></marker>'
            '<pattern id="unk" width="7" height="7" patternUnits="userSpaceOnUse" '
            'patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="7" stroke="#999" stroke-width="2.2"/>'
            '</pattern></defs>'
            '<rect width="100%%" height="100%%" fill="#ffffff"/>'
            % (self.w, self.h, self.w, self.h))
        t = ('<text x="%.1f" y="34" font-family="Segoe UI,Arial,sans-serif" '
             'font-size="19" font-weight="bold" fill="#111">%s</text>'
             '<text x="%.1f" y="56" font-family="Segoe UI,Arial,sans-serif" '
             'font-size="12" fill="#555">%s</text>' % (28, _esc(title), 28, _esc(subtitle)))
        y = self.h - 150 + 26
        n = []
        for line in notes:
            n.append('<text x="%.1f" y="%.1f" font-family="Segoe UI,Arial,sans-serif" '
                     'font-size="11" fill="#333">%s</text>' % (28, y, _esc(line)))
            y += 15
        return head + t + "".join(self.parts) + "".join(n) + "</svg>"


def draw(elev, title, subtitle, notes, annotations=()):
    """Render the assembled elevation.

    ⚠ Everything drawn here is either compiled geometry or an authored record.
    Anything that is NEITHER - the radiator, for instance, which exists in this
    project only as a sentence in a notes column - is drawn hatched and labelled
    as not modelled. It must not read as a measured object.
    """
    H = ceiling_mm()
    c = Canvas(elev["span_mm"], H)
    x0, x1 = elev["x0"], elev["x1"]
    verts = _verticals()

    def rel(x):
        return x - x0

    # --- the wall faces, one rectangle per resolved wall, material-coloured
    for s in elev["segments"]:
        c.rect(rel(s["x0"]), rel(s["x1"]), 0, H,
               MATERIAL_FILL.get(s["class"], "#eeeeee"), stroke="#8a8a8a", sw=1.0)
        mid = rel((s["x0"] + s["x1"]) / 2.0)
        if s["length_mm"] * PX_PER_MM > 34:
            c.text(mid, H - 105, s["wall_id"], size=15, weight="bold", fill="#444")
            c.text(mid, H - 255, MATERIAL_LABEL.get(s["class"], s["class"]),
                   size=10, fill="#666")

    # --- the openings, leaf by leaf
    for o in elev["openings"]:
        leaves = leaves_for(o["opening_id"], verts)
        # Leaf widths come from the RECORD's own split, normalised onto the
        # compiled opening width - the compiler resolves the void, the record
        # resolves how it is divided.
        rec = [verts.get(k, {}) for k in leaves]
        cursor = o["x0"]
        widths = _leaf_widths(o, leaves)
        for k, w in zip(leaves, widths):
            v = verts.get(k, {})
            sill, head = v.get("sill_mm"), v.get("head_mm")
            a, b = cursor, cursor + w
            cursor = b
            known = sill == sill and head == head          # nan-safe
            if not known:
                c.rect(rel(a), rel(b), 0, H, "url(#unk)", stroke="#777", dash="5,4")
                c.text(rel((a + b) / 2.0), H / 2.0, "%s: vertical NOT recorded" % k,
                       size=10, fill="#444")
                continue
            # glass
            c.rect(rel(a), rel(b), sill, head, "#cfe4ef", stroke="#2b6b86", sw=1.6)
            # wall below the sill, if any
            if sill > 0:
                c.rect(rel(a), rel(b), 0, sill,
                       MATERIAL_FILL.get("external", "#e6dfd2"), stroke="#8a8a8a")
            c.text(rel((a + b) / 2.0), head + 40, k, size=12, weight="bold", fill="#1d5a73")
            label = v.get("type") or ""
            if label:
                c.text(rel((a + b) / 2.0), (sill + head) / 2.0, label, size=10, fill="#2b6b86")
            if v.get("uncertain"):
                c.text(rel((a + b) / 2.0), sill + 120,
                       "⚠ sill/head DERIVED, not measured", size=9, fill="#b03030")

    # --- ceiling and floor
    c.line(0, H, elev["span_mm"], H, stroke="#111", sw=2.0)
    c.line(0, 0, elev["span_mm"], 0, stroke="#111", sw=2.6)
    c.text_px(MARGIN - 8, c.Y(H) + 4, "потолок %d" % H, size=10, anchor="end", fill="#111")
    c.text_px(MARGIN - 8, c.Y(0) + 4, "стяжка 0", size=10, anchor="end", fill="#111")

    # --- caller annotations (candidate zones, unmodelled objects)
    for an in annotations:
        c.rect(rel(an["x0"]), rel(an["x1"]), an["y0"], an["y1"],
               an.get("fill", "none"), stroke=an.get("stroke", "#b03030"),
               sw=1.4, dash=an.get("dash", "7,5"))
        if not an.get("label"):
            continue
        lx = rel((an["x0"] + an["x1"]) / 2.0)
        ly = an.get("label_y", an["y1"] + 50)
        if an.get("rotate"):
            # A band narrower than its caption gets the caption turned. R8 is
            # 175 mm wide and the thing that must be said about it is the whole
            # answer, so it cannot simply be dropped.
            c.parts.append(
                '<text x="%.2f" y="%.2f" font-family="Segoe UI,Arial,sans-serif" '
                'font-size="11" text-anchor="middle" fill="%s" font-weight="bold" '
                'transform="rotate(-90 %.2f %.2f)">%s</text>'
                % (c.X(lx), c.Y(ly), an.get("stroke", "#b03030"),
                   c.X(lx), c.Y(ly), _esc(an["label"])))
        else:
            c.text(lx, ly, an["label"], size=11, weight="bold",
                   fill=an.get("stroke", "#b03030"))

    # --- the dimension chain along the bottom, solid | opening | solid
    marks = [x0]
    for o in elev["openings"]:
        marks += [o["x0"], o["x1"]]
    marks.append(x1)
    for a, b in zip(marks, marks[1:]):
        if b - a > 1.0:
            c.dim(rel(a), rel(b), -170, "%.1f" % (b - a))
    c.dim(0, elev["span_mm"], -330, "%.1f  в чистоте" % elev["span_mm"], colour="#333")

    # --- verticals
    c.vdim(-150, 0, H, "%d" % H)
    # ⚠ THE BAND ABOVE THE HEAD. It is derivable and nobody had looked at it:
    # a wider opening needs a longer lintel, and what is available above the
    # head is whatever is left to the ceiling. Drawn as a measured band, with
    # NO claim about what lintel it can carry - that is an engineer's figure,
    # not one this model holds.
    heads = [verts.get(k, {}).get("head_mm")
             for o in elev["openings"] for k in leaves_for(o["opening_id"], verts)]
    heads = [h for h in heads if h == h]
    if heads:
        hd = max(heads)
        c.line(0, hd, elev["span_mm"], hd, stroke="#a11", sw=0.9, dash="6,4")
        c.vdim(elev["span_mm"] + 150, hd, H, "%.0f" % (H - hd))
        c.text_px(c.X(elev["span_mm"] + 150) + 22, c.Y((hd + H) / 2.0),
                  "над проёмом — зона перемычки", size=10, anchor="start", fill="#a11")
    for o in elev["openings"]:
        for k in leaves_for(o["opening_id"], verts):
            v = verts.get(k, {})
            if v.get("sill_mm") == v.get("sill_mm") and v.get("sill_mm", 0) > 0:
                c.vdim(rel(o["x0"]) - 70, 0, v["sill_mm"], "%.0f" % v["sill_mm"])
                break

    return c.svg(title, subtitle, notes)


def _leaf_widths(opening, leaves):
    """Split the COMPILED opening width across its recorded leaves.

    ⚠ The leaf widths in `wall_openings.csv` carry '?' - they are derived from a
    photo, not taped. So they set the RATIO and the compiler sets the TOTAL:
    that way the drawing is exactly as wide as the resolved void, and the split
    inside it carries the record's uncertainty rather than overriding the
    geometry. Equal split if the record gives nothing usable.
    """
    if len(leaves) == 1:
        return [opening["width_mm"]]
    raw = []
    for k in leaves:
        for r in read_csv(os.path.join(CANON, "wall_openings.csv")):
            if (r.get("opening_id") or "").strip() == k:
                raw.append(finite((r.get("width_mm") or "").replace("?", "") or "nan"))
                break
        else:
            raw.append(float("nan"))
    if any(v != v for v in raw) or sum(raw) <= 0:
        return [opening["width_mm"] / float(len(leaves))] * len(leaves)
    total = sum(raw)
    return [opening["width_mm"] * v / total for v in raw]


# ---------------------------------------------------------------------------
# The 9.36 room's south face - the face the owner's question is about
# ---------------------------------------------------------------------------

def room_936_south(geom):
    """Derive the face WHOLLY from the compiler. No coordinate is typed here.

    ⚠ The three bounds are taken as the faces of named walls, not as numbers:
    the room's west boundary is R6's high face, its east boundary is G8's low
    face, and the wall plane is MA's high face. If any of those move, this
    drawing moves with them - which is the whole reason the project compiles
    geometry instead of storing it.
    """
    W = {w["wall_id"]: w for w in geom.walls}
    return build(geom, "EW",
                 W["MA"]["face_hi_mm"],     # the wall plane the room looks at
                 W["R6"]["face_hi_mm"],     # room west boundary
                 W["G8"]["face_lo_mm"])     # room east boundary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--face", default="room936-south")
    ap.add_argument("--output", default=os.path.join(REPO, "_Drawings", "review",
                                                     "room_936_south_elevation.svg"))
    ap.add_argument("--no-candidates", action="store_true",
                    help="draw the existing state only, with no candidate zones")
    args = ap.parse_args()

    geom = R.resolve()
    if args.face != "room936-south":
        raise SystemExit("unknown face %r" % args.face)
    elev = room_936_south(geom)

    segs = elev["segments"]
    ops = elev["openings"]
    o4 = ops[0]
    west = o4["x0"] - elev["x0"]
    east = elev["x1"] - o4["x1"]
    block_east = [s for s in segs if s["class"] != "concrete"][-1]
    conc_east = [s for s in segs if s["class"] == "concrete"]
    conc_mm = conc_east[-1]["length_mm"] if conc_east else 0.0

    # The head, and therefore the band above it, comes from the RECORD - never
    # from a literal typed into a caption, which is how a figure goes stale.
    _v = _verticals()
    _heads = [_v.get(k, {}).get("head_mm")
              for o in ops for k in leaves_for(o["opening_id"], _v)]
    _heads = [h for h in _heads if h == h]
    lintel_band = ceiling_mm() - max(_heads) if _heads else float("nan")

    ann = []
    if not args.no_candidates:
        H = ceiling_mm()
        verts = _verticals()
        head = verts.get("O4a", {}).get("head_mm") or 2235.0
        # WEST: growable, all of it aerated block.
        ann.append({"x0": elev["x0"], "x1": o4["x0"], "y0": 0, "y1": head,
                    "label": "ЗАПАД %.1f — газоблок, не несущая" % west,
                    "stroke": "#1a7f37", "dash": "9,6", "label_y": 1560})
        # EAST: 150 of block, then the frame.
        ann.append({"x0": o4["x1"], "x1": o4["x1"] + (east - conc_mm), "y0": 0, "y1": head,
                    "label": "", "stroke": "#b8860b", "dash": "5,4",
                    "label_y": head + 90})
        ann.append({"x0": elev["x1"] - conc_mm, "x1": elev["x1"], "y0": 0, "y1": H,
                    "label": "R8 монолит %.0f — рама, СТОП" % conc_mm,
                    "stroke": "#a11", "dash": None, "label_y": 1250,
                    "rotate": True})
        # The radiator: a sentence in a notes column, NOT geometry.
        sill = verts.get("O4a", {}).get("sill_mm") or 735.0
        ann.append({"x0": o4["x0"], "x1": o4["x0"] + 600, "y0": 120, "y1": sill - 60,
                    "label": "радиатор — В МОДЕЛИ НЕТ", "stroke": "#777",
                    "dash": "4,4", "label_y": 300})

    notes = [
        "Скомпилировано из ResolvedGeometry %s. Ни одна координата здесь не набрана руками."
        % ("(25 walls)" if len(geom.walls) == 25 else "(%d walls)" % len(geom.walls)),
        "ЦЕПЬ ЗАКРЫВАЕТСЯ: %.1f + %.1f + %.1f = %.1f мм в чистоте."
        % (west, o4["width_mm"], east, elev["span_mm"]),
        "ВОСТОК: %.0f мм газоблока, затем %.0f мм монолита R8 — рама, расширение на восток"
        " упирается в неё." % (east - conc_mm, conc_mm),
        "ЗАПАД: %.1f мм, целиком MA — газоблок 300, «не несущие» по описанию застройщика."
        % west,
        "!! Радиатор в модели ОТСУТСТВУЕТ. Показан как неизмеренная зона, не как объект.",
        "!! Окно выходит НА ЛОДЖИЮ, не на улицу. MA — тепловая граница квартиры.",
        "!! Над проёмом до потолка остаётся %.0f мм. Это зона перемычки — какую перемычку"
        " она несёт, модель НЕ знает, это расчёт конструктора." % lintel_band,
    ]
    svg = draw(elev,
               "Развёртка — комната 9.36, южная стена (MA + торец R8)",
               "Существующее состояние v0 · высота в свету %d мм от стяжки · %s"
               % (ceiling_mm(), "кандидатные зоны показаны" if not args.no_candidates
                  else "без кандидатных зон"),
               notes, ann)

    out = args.output
    d = os.path.dirname(out)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(svg)

    print("walls resolved      : %d" % len(geom.walls))
    print("face segments       : %s" % ", ".join(
        "%s %.1f (%s)" % (s["wall_id"], s["length_mm"], s["class"]) for s in segs))
    print("openings            : %s" % ", ".join(
        "%s %.1f" % (o["opening_id"], o["width_mm"]) for o in ops))
    print("chain               : %.1f | %.1f | %.1f  = %.1f clear"
          % (west, o4["width_mm"], east, elev["span_mm"]))
    print("east is             : %.0f mm block + %.0f mm CONCRETE (R8)"
          % (east - conc_mm, conc_mm))
    print("wrote               : %s" % os.path.relpath(out, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
