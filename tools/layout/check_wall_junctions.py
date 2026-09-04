# -*- coding: utf-8 -*-
"""Check every junction in the flat's wall geometry for BOTH failure modes.

Why this exists
---------------
Owner, 2026-09-04, on v18: "One bad thing is overlapping. Another bad thing is
creating a void. A correct junction is, for example, R1a and MA, MA and R8, R8
and MB - a perfect corner when you take the thickness into account. If we connect
R1a and R1b we get a void at the very corner. That's not correct. You should
extend either R1b or R1a by the thickness, 250 mm."

He is right, and it exposes a flaw in the convention this repo adopted one
version earlier. "Every length is the clear internal run" avoids double-counting
but guarantees an unfilled square at every L-corner, because neither wall
reaches the other's far face. A corner is a solid, and exactly one of the two
walls has to own it.

  OVERLAP   both walls reach through the other  -> the corner volume is counted twice
  VOID      neither wall reaches through        -> the corner volume is counted zero times
  OK        exactly one reaches through         -> counted once. This is a corner.

A T-junction is different and needs no ownership decision: the through wall
already spans the joint, and the butting wall stops on its face. It fails only
if the butting wall stops short of that face (GAP) or crosses it (OVERLAP).

Where the corner ownership actually LIVES
-----------------------------------------
Not in these pixel runs. The first attempt at this snapped the drawn coordinates
until the corners closed, and that was the wrong instrument: it moved lengths
that come from printed dimensions and the owner's own chains by tens of
millimetres, to satisfy a raster registration only good to ~50 mm. The drawing
LOCATES walls; it does not define them.

So the drawing keeps showing CLEAR internal runs - which is what a plan of
internal dimensions should show - and each wall carries clear_mm plus solid_mm,
where solid_mm adds the thickness of every corner that wall owns. The ownership
is recorded in data/canonical/wall_corners.csv and enforced by
tools/layout/build_wall_corners.py.

An L-corner that reads as a VOID in the drawn runs is therefore expected and
fine, PROVIDED the ledger owns it. This check fails only on a void that nothing
owns - a corner whose material would be lost from the quantities.

Usage
-----
    py -3 tools/layout/check_wall_junctions.py

Exits non-zero on any overlap, void or gap.
"""
from __future__ import print_function

import csv
import io
import os
import sys

MM_PER_PX = 9.789          # mm per pixel of the BASIC plan; see wall_materials.json
TOL_MM = 25.0              # AGENTS.md: dimensions are nominal +/-25 mm
NEAR_MM = 150.0            # beyond this the two runs are simply not meeting

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RUNS = os.path.join(REPO, 'data', 'canonical', 'wall_runs.csv')
LEDGER = os.path.join(REPO, 'data', 'canonical', 'wall_corners.csv')


def owned_corners():
    """corner ids the ledger assigns an owner to, so the solid is accounted."""
    if not os.path.exists(LEDGER):
        return set()
    with io.open(LEDGER, encoding='utf-8') as f:
        return set(r['corner_id'] for r in csv.DictReader(f) if r.get('owner'))


def load(path):
    out = []
    with io.open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out.append({
                'id': r['wall_id'],
                't': float(r['thickness_mm']),
                'a': (float(r['ax_basic_px']), float(r['ay_basic_px'])),
                'b': (float(r['bx_basic_px']), float(r['by_basic_px'])),
            })
    return out


def orient(w):
    a, b = w['a'], w['b']
    if a[1] == b[1]:
        return 'h', a[1], min(a[0], b[0]), max(a[0], b[0])
    if a[0] == b[0]:
        return 'v', a[0], min(a[1], b[1]), max(a[1], b[1])
    return None, 0.0, 0.0, 0.0


def junctions(walls):
    ledger = owned_corners()
    tol = TOL_MM / MM_PER_PX
    near = NEAR_MM / MM_PER_PX
    rows = []
    for i in range(len(walls)):
        for j in range(i + 1, len(walls)):
            h, v = walls[i], walls[j]
            oh, fh, lh, hh = orient(h)
            ov, fv, lv, hv = orient(v)
            if oh is None or ov is None or oh == ov:
                continue
            if oh == 'v':
                h, v = v, h
                oh, fh, lh, hh, ov, fv, lv, hv = ov, fv, lv, hv, oh, fh, lh, hh
            # do these two runs come anywhere near meeting?
            if not (lh - near <= fv <= hh + near and lv - near <= fh <= hv + near):
                continue
            half_h = h['t'] / 2.0 / MM_PER_PX      # half thickness of the horizontal
            half_v = v['t'] / 2.0 / MM_PER_PX      # half thickness of the vertical
            # does the horizontal run span the vertical's full thickness?
            h_through = (lh <= fv - half_v + tol) and (hh >= fv + half_v - tol)
            v_through = (lv <= fh - half_h + tol) and (hv >= fh + half_h - tol)
            # is the joint at an END of each run, or interior to one of them?
            h_interior = (fv - lh > half_v + tol) and (hh - fv > half_v + tol)
            v_interior = (fh - lv > half_h + tol) and (hv - fh > half_h + tol)

            if h_interior and v_interior:
                kind = 'CROSS'
            elif h_interior or v_interior:
                kind = 'T'
            else:
                kind = 'L'

            if kind == 'L':
                if h_through and v_through:
                    rows.append(('OVERLAP', h['id'], v['id'], 'L',
                                 'both reach through; corner counted twice'))
                elif not h_through and not v_through:
                    a, b = sorted([h['id'], v['id']])
                    if 'C_%s_%s' % (a, b) in ledger:
                        continue          # accounted in solid_mm by the ledger
                    need = min(h['t'], v['t'])
                    rows.append(('VOID', h['id'], v['id'], 'L',
                                 'unowned corner - %d mm of material lost' % need))
            elif kind == 'T':
                butt, thru = (v, h) if h_interior else (h, v)
                b_through = v_through if h_interior else h_through
                if b_through:
                    rows.append(('OVERLAP', thru['id'], butt['id'], 'T',
                                 '%s crosses %s instead of stopping on its face'
                                 % (butt['id'], thru['id'])))
                else:
                    # butting wall must actually touch the through wall's near face
                    if h_interior:
                        short = min(abs(lv - (fh + half_h)), abs(hv - (fh - half_h)))
                    else:
                        short = min(abs(lh - (fv + half_v)), abs(hh - (fv - half_v)))
                    if short * MM_PER_PX > TOL_MM:
                        rows.append(('GAP', thru['id'], butt['id'], 'T',
                                     '%s stops %.0f mm off %s\'s face'
                                     % (butt['id'], short * MM_PER_PX, thru['id'])))
            else:
                rows.append(('OVERLAP', h['id'], v['id'], 'CROSS',
                             'runs cross away from either end'))
    return rows


def main():
    if not os.path.exists(RUNS):
        print('missing %s' % RUNS)
        return 2
    walls = load(RUNS)
    bad = junctions(walls)
    print('checked %d wall runs' % len(walls))
    if not bad:
        print('PASS - no overlap, no gap, and every L-corner void is owned '
              'in wall_corners.csv')
        return 0
    order = {'OVERLAP': 0, 'VOID': 1, 'GAP': 2}
    for f, a, b, kind, msg in sorted(bad, key=lambda r: (order[r[0]], r[1])):
        print('  %-7s %-4s %-5s x %-5s  %s' % (f, kind, a, b, msg))
    print('%d junction problem(s). A corner is a solid: exactly one of the two '
          'walls must own it, in the ledger or in the geometry.' % len(bad))
    return 1


if __name__ == '__main__':
    sys.exit(main())
