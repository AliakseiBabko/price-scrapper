#!/usr/bin/env python3
"""Assert the generated IFC back against the canonical tables it claims to come from.

`model_from_resolved.py` builds the model from the geometry compiler.
That is only worth anything if the result is checked: the defect this whole
exercise started from - a schematic silently disagreeing with the measured
geometry - was invisible precisely because NOTHING read the file the model was
built from. A generator with no gate is the same arrangement with a new file.

Checks, all of them against a table the generator does not own:

  1. Every wall in `wall_blocks.csv` is present in the IFC, exactly once.
  2. Each wall's DRAWN thickness matches its recorded `thickness_mm`.
  3. Each opening's sill and head match `wall_openings.csv`, where recorded.
  4. Each wall's DRAWN LENGTH is its recorded solid_mm, its sanctioned entry in
     wall_extent_exceptions.csv, or that plus an opening width - because a wall
     is extended across a doorway the plan draws it as stopping at.
  5. Both ventilation shafts are present, and are NOT walls.

A further check - each fill against its own opening - was written and REMOVED: it
could never fire, because `create_shape` returns no geometry for an
IfcOpeningElement, so both sides read empty and it skipped every time. Check 3
catches the same defect and is stronger, because it measures against
`wall_openings.csv` rather than against another number in the same file. A check
that cannot fail is worse than no check, since it reads as coverage.

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
EXTENTS = REPO / "data" / "canonical" / "wall_extent_exceptions.csv"

THICKNESS_TOL_MM = 2.0     # the DXF rounds to 0.1 mm; 2 mm is generous and still tight
VERTICAL_TOL_MM = 5.0
LENGTH_TOL_MM = 5.0
AREA_TOL_MM2 = 500.0   # a tenth of the 5,700 mm2 a squared-back mitre restores


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


def want_open_ids() -> set[str]:
    with OPENINGS.open(encoding="utf-8") as fh:
        return {(r["opening_id"] or "").strip() for r in csv.DictReader(fh)}


def check(ifc_path: Path) -> list[str]:
    import ifcopenshell
    import ifcopenshell.geom

    problems: list[str] = []
    model = ifcopenshell.open(str(ifc_path))
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    # 1 + 2 - walls against wall_blocks.csv
    recorded, solid = {}, {}
    with BLOCKS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            recorded[row["wall_id"]] = parse_mm(row.get("thickness_mm"))
            solid[row["wall_id"]] = parse_mm(row.get("solid_mm"))

    exceptions = {}
    if EXTENTS.exists():
        with EXTENTS.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                drawn = parse_mm(row.get("drawn_mm"))
                if row.get("wall_id") and drawn:
                    exceptions[row["wall_id"].strip()] = drawn

    # Opening widths, by the wall each is recorded in - the only extension a
    # wall's drawn length is allowed to carry.
    openings_in: dict[str, list] = {}
    with OPENINGS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            host = (row.get("in_wall_or_divider") or "").strip()
            width = parse_mm(row.get("width_mm"))
            if host and width:
                openings_in.setdefault(host, []).append(width)

    # No exemptions. There are no lintel or spandrel elements: this flat has no
    # structural lintels (owner, 2026-09-16 - an opening is just an opening, and
    # everything in it is joinery), so a wall runs continuously over its openings
    # and every IfcWall must be one that wall_blocks.csv records.
    seen = {}
    for wall in model.by_type("IfcWall"):
        name = wall.Name or ""
        seen[name] = seen.get(name, 0) + 1

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

        # LENGTH, and it has to allow for one legitimate difference. Where the
        # DXF draws a wall as stopping at a doorway, the model extends it across
        # the opening and cuts a void, because there is no structural lintel in
        # this flat - the block simply continues over the door. So a wall's
        # drawn length is either its recorded solid_mm, or solid_mm plus the
        # width of an opening recorded in it. Anything else is an extension
        # nobody asked for, which is exactly what this check exists to catch.
        # The expected length is the SANCTIONED drawn length where one exists.
        # Eight walls differ from their solid_mm for reasons already recorded and
        # validated in wall_extent_exceptions.csv - corner gain already covered,
        # deliberate recorded moves, within build tolerance - and check_dxf_closure
        # validates that ledger. Reusing it keeps this check strict: a length that
        # matches neither the record, nor its sanctioned exception, nor an opening
        # extension is a real divergence.
        want_len = exceptions.get(wall.Name) or solid.get(wall.Name)
        if want_len:
            drawn_len = max(size[0], size[1]) * 1000.0
            allowed = [want_len] + [want_len + w for w in openings_in.get(wall.Name, [])]
            if not any(abs(drawn_len - a) <= LENGTH_TOL_MM for a in allowed):
                problems.append(
                    "wall %s drawn %.0f mm long; expected %.0f%s"
                    % (wall.Name, drawn_len, want_len,
                       (" or, with the openings in it, " +
                        ", ".join("%.0f" % a for a in allowed[1:])) if len(allowed) > 1 else ""))

    # 5 - XY PLACEMENT against the resolved graph.
    #
    # ⚠️ Added because the gate demonstrably did not catch it: translating wall
    # G5 500 mm sideways, with every dimension unchanged, passed with 0
    # problems. Identity, length, thickness, opening verticals and shaft count
    # are all invariant under a rigid shift - so a wall in the wrong PLACE was
    # indistinguishable from a wall in the right one.
    #
    # The comparison is against the compiler's resolved geometry, not against
    # another number in the IFC. The cross axis must match exactly: no
    # reconciliation rule moves a wall sideways. The long axis may extend
    # OUTWARD only, and only as far as an opening recorded in that wall - which
    # is the sanctioned extension across a doorway - never inward, and never
    # without an opening to account for it.
    try:
        sys.path.insert(0, str(REPO / "tools" / "layout"))
        import resolve_v0_geometry as rv
    except Exception as exc:  # noqa: BLE001
        problems.append("cannot load the geometry compiler to check placement: %s" % exc)
        rv = None

    if rv is not None:
        resolved = rv.resolve()
        boxes = {w["wall_id"]: rv.wall_box(w) for w in resolved.walls
                 if w.get("from_mm") is not None}
        if boxes:
            off_x = min(b[0] for b in boxes.values())
            off_y = min(b[1] for b in boxes.values())
            for wall in model.by_type("IfcWall"):
                want_box = boxes.get(wall.Name)
                if want_box is None:
                    continue
                v = _verts(settings, wall)
                if not len(v):
                    continue
                got = (v[:, 0].min() * 1000.0 + off_x, v[:, 1].min() * 1000.0 + off_y,
                       v[:, 0].max() * 1000.0 + off_x, v[:, 1].max() * 1000.0 + off_y)
                grow = max(openings_in.get(wall.Name, [0.0]) or [0.0])
                long_axis = 0 if (want_box[2] - want_box[0]) >= (want_box[3] - want_box[1]) else 1
                for axis, name in ((0, "x"), (1, "y")):
                    lo_d = got[axis] - want_box[axis]
                    hi_d = got[axis + 2] - want_box[axis + 2]
                    if axis == long_axis:
                        ok = (-grow - LENGTH_TOL_MM <= lo_d <= LENGTH_TOL_MM
                              and -LENGTH_TOL_MM <= hi_d <= grow + LENGTH_TOL_MM)
                        why = "may extend outward up to %.0f mm for an opening" % grow
                    else:
                        ok = abs(lo_d) <= LENGTH_TOL_MM and abs(hi_d) <= LENGTH_TOL_MM
                        why = "cross axis: no rule moves a wall sideways"
                    if not ok:
                        problems.append(
                            "wall %s placed %.1f/%.1f mm off in %s against the resolved "
                            "geometry (%s)" % (wall.Name, lo_d, hi_d, name, why))

    # 6 - EXACT FOOTPRINT PARITY against the compiler's plan polygon.
    #
    # ⚠️ The placement check above compares bounding boxes, and a mitre is
    # INVISIBLE to a bounding box: clipping a rectangle on a plane through its
    # corner leaves min and max untouched. That is precisely how the IFC came to
    # restore 5,710 mm2 on M2 and 5,707 mm2 on M6b with every gate passing, on
    # both sides. Area is the measure that sees it.
    if rv is not None and getattr(resolved, "body_polygons", None):
        def _area(points):
            n = len(points)
            return abs(sum(points[i][0] * points[(i + 1) % n][1]
                           - points[(i + 1) % n][0] * points[i][1]
                           for i in range(n))) / 2.0

        def _canonical(points, scale=1.0, dx=0.0, dy=0.0):
            """A polygon reduced to a comparable form: identity, not resemblance.

            Rounded to 0.1 mm, closing duplicate dropped, rotated so the
            lexicographically smallest vertex leads, and normalised for winding
            direction. Two polygons with the same canonical form ARE the same
            polygon - which area alone cannot tell you, because a different
            shape can have the same area and the same bounding box.
            """
            # ⚠️ The IFC is in metres from a shifted origin; the compiler is in
            # millimetres on the drawing's own. Comparing without restoring the
            # offset reports every wall as different while area and corner count
            # match exactly - which is what it did on the first run.
            pts = [(round(p[0] * scale + dx, 1), round(p[1] * scale + dy, 1))
                   for p in points]
            if len(pts) > 1 and pts[0] == pts[-1]:
                pts = pts[:-1]
            if not pts:
                return ()
            forward = min(range(len(pts)), key=lambda i: pts[i:] + pts[:i])
            fwd = tuple(pts[forward:] + pts[:forward])
            rev_pts = list(reversed(pts))
            backward = min(range(len(rev_pts)), key=lambda i: rev_pts[i:] + rev_pts[:i])
            rev = tuple(rev_pts[backward:] + rev_pts[:backward])
            return min(fwd, rev)

        for wall in model.by_type("IfcWall"):
            # Compared against the BODY polygon, which is the compiler's own
            # 3D footprint - the plan polygon extended across any doorway. The
            # extension is therefore expected geometry rather than an allowance
            # this check has to guess at.
            want_poly = resolved.body_polygons.get(wall.Name)
            if not want_poly:
                continue
            curve = (wall.Representation.Representations[0]
                     .Items[0].SweptArea.OuterCurve)
            got = [tuple(p.Coordinates) for p in curve.Points]
            if _canonical(got, 1000.0, off_x, off_y) != _canonical(want_poly):
                got_mm2 = _area([(p[0] * 1000.0 + off_x, p[1] * 1000.0 + off_y)
                                 for p in got])
                want_mm2 = _area(want_poly)
                problems.append(
                    "wall %s footprint differs from the compiler's body polygon: "
                    "%d corners / %.0f mm2 against %d corners / %.0f mm2. Area is "
                    "reported as a diagnostic - the test is exact polygon identity, "
                    "because a different shape can share both area and bounding box"
                    % (wall.Name, len(set(got)), got_mm2,
                       len(want_poly), want_mm2))

    # 3 - opening verticals against wall_openings.csv
    want_open = {}
    with OPENINGS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            oid = (row["opening_id"] or "").strip()
            if oid:
                want_open[oid] = (parse_mm(row.get("sill_height_mm")),
                                  parse_mm(row.get("head_height_mm")))

    # Measure the ASSEMBLY, not the glass. A window is a frame plus a pane, and
    # the pane is deliberately inset by the frame width - so checking the
    # IfcWindow alone would report every window as 70 mm short at both ends.
    # The frame's jambs run the full sill-to-head, so the union of everything
    # named for the opening is the opening.
    assemblies: dict[str, list] = {}
    for cls in ("IfcWindow", "IfcDoor", "IfcMember"):
        for part in model.by_type(cls):
            oid = (part.Name or "").split()[0]
            if oid in want_open:
                assemblies.setdefault(oid, []).append(part)

    for oid, parts in assemblies.items():
        sill, head = want_open[oid]
        zs = []
        for part in parts:
            v = _verts(settings, part)
            if not len(v):
                problems.append("opening part %s has no geometry" % part.Name)
                continue
            zs.append((v[:, 2].min(), v[:, 2].max()))
        if not zs:
            continue
        lo = min(z[0] for z in zs) * 1000.0
        hi = max(z[1] for z in zs) * 1000.0
        if sill is not None and abs(lo - sill) > VERTICAL_TOL_MM:
            problems.append("%s assembly starts %.0f mm, wall_openings.csv records sill %.0f"
                            % (oid, lo, sill))
        if head is not None and abs(hi - head) > VERTICAL_TOL_MM:
            problems.append("%s assembly ends %.0f mm, wall_openings.csv records head %.0f"
                            % (oid, hi, head))

    # 4 - ventilation shafts present, and not counted as walls
    shafts = [p for p in model.by_type("IfcBuildingElementProxy")
              if (p.Name or "").startswith("Vent shaft")]
    if len(shafts) != 2:
        problems.append("expected 2 ventilation shafts, found %d" % len(shafts))
    for wall in model.by_type("IfcWall"):
        if (wall.Name or "").startswith("Vent shaft"):
            problems.append("ventilation shaft %s is modelled as a wall" % wall.Name)

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
