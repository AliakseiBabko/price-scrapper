# -*- coding: utf-8 -*-
"""Place the named openings from the VECTOR, not from the raster fit.

Why
---
Owner, 2026-09-09, reading the DXF back: *"O5, O6 they're displaced, not in their
proper place. And also these O3 and new slab extension should be aligned. They
should be aligned. You can check the vector drawing."*

He is right on both, and the second is checkable to a tenth of a millimetre. In
the vector:

    window reveal in MC   10286.0 .. 11986.0   centre 11136.0
    decorative slab       10235.9 .. 12035.9   centre 11135.9

**Concentric to 0.1 mm** - the developer drew the slab centred on the window.
The exported O3 came out at 10152.1..11907.1, centre 11029.6: **106.3 mm off**,
because opening spans were transformed from basic-plan pixels through the
identification fit, which has 3.3% anisotropy. The drawing's own alignment was
destroyed by the transform.

How an opening is found here
----------------------------
1. Take the wall solid the named opening's host wall sits on.
2. Inside it, find the REVEAL LINES: perpendicular lines that cross a good part
   of the wall's thickness. A joint crosses the whole thickness; a reveal crosses
   most of it. Both are drawn, and both are exact.
3. The extractor's hatch gaps say roughly where the opening is (to the 150 mm
   bin). Snap that rough span to the nearest reveal lines, which makes it exact.
4. Match the named openings to those spans by width, then position.

!! An opening that cannot be matched is reported UNPLACED rather than being
given a plausible position. Two of them currently are, and the reason is not the
transform - see the note in the output.
"""
from __future__ import print_function

import argparse
import csv
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CANON = os.path.join(REPO, 'data', 'canonical')
PDF = os.path.join(REPO, '_Inbox', '_Visual_Drop', '3Б_3+ МН5_287.pdf')

REVEAL_MIN_FRACTION = 0.45     # a reveal line crosses at least this of the thickness
SNAP_MM = 220.0                # how far a coarse hatch-gap edge may be pulled
WIDTH_TOL_MM = 260.0           # a named width may differ from the drawn span by this


def _mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def reveal_lines(plan, solid, mm, min_fraction=REVEAL_MIN_FRACTION):
    """Perpendicular lines crossing most of the wall's thickness, in mm."""
    f_lo, f_hi = solid['face_lo_mm'], solid['face_hi_mm']
    need = (f_hi - f_lo) * min_fraction
    out = set()
    for x0, y0, x1, y1 in plan['segments']:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        if solid['axis'] == 'EW':
            if abs(X1 - X0) > 0.05:
                continue
            lo, hi, pos = min(Y0, Y1), max(Y0, Y1), X0
        else:
            if abs(Y1 - Y0) > 0.05:
                continue
            lo, hi, pos = min(X0, X1), max(X0, X1), Y0
        overlap = min(hi, f_hi) - max(lo, f_lo)
        if overlap >= need and solid['from_mm'] - 2 <= pos <= solid['to_mm'] + 2:
            out.add(round(pos, 1))
    return sorted(out)


def snap(value, lines, limit=SNAP_MM):
    if not lines:
        return value, None
    near = min(lines, key=lambda t: abs(t - value))
    if abs(near - value) <= limit:
        return near, round(near - value, 1)
    return value, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', default=PDF)
    ap.add_argument('--out', default=os.path.join(CANON, 'v0_openings_placed.json'))
    args = ap.parse_args()

    ex = _mod('ex', os.path.join(HERE, 'extract_v0_walls.py'))
    pn = _mod('pn', os.path.join(HERE, 'place_named_walls.py'))
    plan = ex._load_parser().parse(args.pdf)
    mm = ex.MM_PER_PT

    placed = json.load(io.open(os.path.join(CANON, 'v0_named_walls_placed.json'),
                              encoding='utf-8'))
    walls = {w['wall_id']: w for w in placed['walls']
             if w.get('from_mm') is not None}
    solids = {s['solid_id']: s for s in placed['solids']}

    # rough opening spans from the hatch gaps, per solid
    vsolids = pn.vector_solids(ex, plan)
    pn.clip_to_envelope(vsolids)
    rough = {}
    for s in vsolids:
        key = (s['axis'], round(s['face_lo_mm'], 1), round(s['face_hi_mm'], 1))
        rough.setdefault(key, []).extend(s.get('candidate_openings') or [])

    named = {r['opening_id']: r for r in
             csv.DictReader(io.open(os.path.join(CANON, 'wall_openings.csv'),
                                    encoding='utf-8'))}
    spans = list(csv.DictReader(io.open(os.path.join(CANON,
                                                     'wall_opening_spans.csv'),
                                        encoding='utf-8')))

    out, unplaced = [], []
    print('%-4s %-5s %-11s %-11s %-8s %-8s %s'
          % ('op', 'wall', 'from', 'to', 'width', 'named', 'source'))
    for r in spans:
        oid, wid = r['opening_id'], r['wall_id']
        w = walls.get(wid)
        if not w:
            unplaced.append((oid, wid, 'host wall %s has no geometry' % wid))
            continue
        s = solids.get(w['solid_id'])
        key = (s['axis'], round(s['face_lo_mm'], 1), round(s['face_hi_mm'], 1))
        cands = rough.get(key) or []
        lines = reveal_lines(plan, s, mm)
        want = float(named.get(oid, {}).get('width_mm', '0').rstrip('?') or 0)

        best = None
        for c in cands:
            lo, hi = snap(c['from_mm'], lines)[0], snap(c['to_mm'], lines)[0]
            if hi <= lo:
                continue
            # must fall inside the HOST wall, not merely the shared solid
            if hi < w['from_mm'] - 1 or lo > w['to_mm'] + 1:
                continue
            err = abs((hi - lo) - want) if want else 0.0
            if err > WIDTH_TOL_MM:
                continue
            if best is None or err < best[0]:
                best = (err, lo, hi)
        if best is None:
            unplaced.append((oid, wid,
                             'no drawn gap inside %s matches its %s mm width'
                             % (wid, want or '?')))
            continue
        _, lo, hi = best
        out.append({'opening_id': oid, 'wall_id': wid, 'solid_id': w['solid_id'],
                    'axis': s['axis'], 'face_lo_mm': s['face_lo_mm'],
                    'face_hi_mm': s['face_hi_mm'],
                    'from_mm': round(lo, 1), 'to_mm': round(hi, 1),
                    'width_mm': round(hi - lo, 1),
                    'named_width_mm': want or None,
                    'source': 'vector reveal lines'})
        print('%-4s %-5s %11.1f %11.1f %8.1f %8s  vector'
              % (oid, wid, lo, hi, hi - lo, want or '-'))

    if unplaced:
        print('\nUNPLACED - reported rather than given a plausible position:')
        for oid, wid, why in unplaced:
            print('  %-4s %s' % (oid, why))

    json.dump({'id': 'zk-dubravinskiy-v0-openings-placed',
               'status': 'DRAFT',
               'what': ('Named openings positioned from the vector drawing\'s own '
                        'reveal lines, replacing the raster-fit transform.'),
               'method': ('hatch-gap span snapped to perpendicular lines crossing '
                          '>=%.0f%% of the wall thickness' % (REVEAL_MIN_FRACTION * 100)),
               'openings': out,
               'unplaced': [{'opening_id': o, 'wall_id': w, 'why': y}
                            for o, w, y in unplaced]},
              io.open(args.out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('\nplaced %d of %d from the vector; wrote %s'
          % (len(out), len(spans), os.path.relpath(args.out, REPO)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
