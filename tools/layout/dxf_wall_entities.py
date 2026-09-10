# -*- coding: utf-8 -*-
"""The ONE reader for wall entities, and it refuses anything but a rectangle.

Why this exists
---------------
CODEX, `V0_DXF_RASTER_FIDELITY` round 4. It replaced MC's four-point rectangular
`LWPOLYLINE` with a **closed triangle on three of the same four corners**. Label,
layer, bounding box, nominal length and nominal thickness were all unchanged;
half the wall body was gone. **Both binding gates returned exit 0.**

The cause was the same line written twice:

    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)

`check_dxf_closure.walls_from_dxf()` and `raster_fidelity.dxf_walls()` each
reduced the polyline to its bounding box, and every corner square, cavity scan,
body mask and dense edge sample downstream then operated on **a rectangle nobody
had drawn**. The closure gate could report a corner square fully covered by an
entity that does not cover it.

Two properties of this bug are worth keeping in mind, because they are what make
it a class rather than an incident:

  1. **The substitution is invisible to every later check.** Nothing downstream
     can detect it, however careful, because by then the real polygon is gone.
  2. **It was duplicated.** Two readers meant two chances to reintroduce it, and
     a fix to one would have left the other. Hence one module, used by both.

The contract, and why it is a whitelist
---------------------------------------
`export_v0_dxf.py` draws walls as axis-aligned rectangles and nothing else. So
the safe rule is not "cope with any polygon" but **"refuse anything that is not
the shape the exporter promises"** - a closed, zero-bulge, axis-aligned
quadrilateral with four distinct corners whose polygon area equals its
bounding-box area. Coping with arbitrary polygons would be a larger change with
more places to be subtly wrong; refusing is small, total, and fails closed.

⚠️ **`AREA_TOL` is not cosmetic.** The seeded triangle has exactly half the
bounding box's area, so any sane tolerance catches it - but a *slightly* skewed
quadrilateral is caught only because the tolerance is tight. It is a fraction of
the bbox area, not an absolute, so it does not loosen on large walls.
"""
from __future__ import print_function

import ezdxf

WALL_LAYER_PREFIX = 'V0-WALL'
LABEL_LAYER = 'V0-WALL-LABEL'

AXIS_TOL_MM = 0.5      # an edge this far off axis is not axis-aligned
AREA_TOL = 0.001       # |polygon area - bbox area| / bbox area
MIN_SIDE_MM = 1.0      # a degenerate sliver is not a wall


class MalformedWall(Exception):
    """A wall entity is not the rectangle the exporter contract promises."""


def _shoelace(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


def validate_rectangle(entity, points):
    """Return (x0, x1, y0, y1) or raise MalformedWall with the reason."""
    if not entity.closed:
        raise MalformedWall('the polyline is not closed')
    for q in entity.get_points():
        # a bulge turns a "straight" edge into an arc, so the vertices can be a
        # perfect rectangle while the drawn body is not
        if len(q) > 4 and abs(q[4]) > 1e-9:
            raise MalformedWall('a vertex carries a bulge (%.4f): the edge is '
                                'an arc, not a straight side' % q[4])
    pts = list(points)
    # a closed polyline may or may not repeat its first point
    if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-9 \
            and abs(pts[0][1] - pts[-1][1]) < 1e-9:
        pts = pts[:-1]
    if len(pts) != 4:
        raise MalformedWall('%d distinct corners, expected 4' % len(pts))
    for i in range(4):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 4]
        if abs(ax - bx) > AXIS_TOL_MM and abs(ay - by) > AXIS_TOL_MM:
            raise MalformedWall('edge %d is neither horizontal nor vertical '
                                '(%.1f,%.1f)-(%.1f,%.1f)' % (i, ax, ay, bx, by))
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    w, h = x1 - x0, y1 - y0
    if w < MIN_SIDE_MM or h < MIN_SIDE_MM:
        raise MalformedWall('degenerate: %.2f x %.2f mm' % (w, h))
    bbox_area = w * h
    poly_area = _shoelace(pts)
    if abs(poly_area - bbox_area) > AREA_TOL * bbox_area:
        raise MalformedWall(
            'polygon area %.1f mm2 is not its bounding-box area %.1f mm2 '
            '(%.1f%% off) - the entity does not fill the box the checks would '
            'have used' % (poly_area, bbox_area,
                           100.0 * abs(poly_area - bbox_area) / bbox_area))
    return x0, x1, y0, y1


def labels(msp):
    return {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
            for e in msp if e.dxftype() == 'TEXT'
            and e.dxf.layer == LABEL_LAYER}


def read_walls(path):
    """(walls, problems). A malformed entity lands in `problems`, never in `walls`.

    The caller decides how loudly to fail, but it may not silently proceed: both
    gates treat a non-empty `problems` as a finding.
    """
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    lab = labels(msp)
    walls, problems = [], []
    for e in msp:
        if (e.dxftype() != 'LWPOLYLINE'
                or not e.dxf.layer.startswith(WALL_LAYER_PREFIX)):
            continue
        pts = [(q[0], q[1]) for q in e.get_points()]
        cx = sum(p[0] for p in pts) / len(pts) if pts else 0.0
        cy = sum(p[1] for p in pts) / len(pts) if pts else 0.0
        name = (min(lab.items(),
                    key=lambda kv: (kv[1][0] - cx) ** 2 + (kv[1][1] - cy) ** 2)[0]
                if lab else '?')
        try:
            x0, x1, y0, y1 = validate_rectangle(e, pts)
        except MalformedWall as exc:
            problems.append({'wall': name, 'detail': str(exc)})
            continue
        walls.append({'id': name, 'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1,
                      'axis': 'EW' if (x1 - x0) > (y1 - y0) else 'NS',
                      'layer': e.dxf.layer})
    return walls, problems


def label_names(path):
    doc = ezdxf.readfile(path)
    return [e.dxf.text for e in doc.modelspace()
            if e.dxftype() == 'TEXT' and e.dxf.layer == LABEL_LAYER]
