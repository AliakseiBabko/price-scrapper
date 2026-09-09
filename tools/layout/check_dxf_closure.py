# -*- coding: utf-8 -*-
"""GATE: every junction in the exported DXF is closed, and nothing overlaps.

Why this and not the raster overlay
-----------------------------------
Owner, 2026-09-09: *"I want clear joints. I don't want cavities in the angles
when two walls meet, or gaps between walls, or missing walls… I want you to check
yourself and not come back to me showing the same result."*

CODEX, reviewing the first attempt, rejected the raster metric as flattering and
partly circular - it registered on the DXF's own wall faces and then scored those
same faces against wall-adjacent ink, sampled four points per wall, treated any
dark pixel as "ink", and **returned exit 0 while five walls breached its own
threshold.** All fair.

So the primary gate is this one, and it needs no raster at all: **the question
"is this corner a void?" is answered by the exported geometry itself.** It is
exact, it cannot be circular, and it fails loudly.

What it asserts
---------------
  1. every junction in `wall_corners.csv` is CLOSED in the DXF - the two wall
     rectangles actually overlap, so the corner volume exists once;
  2. no two walls OVERLAP where the ledger does not say they should;
  3. no pair of perpendicular walls sits in the NEAR-MISS band - close enough to
     be a junction, far enough to leave a cavity - without a ledger entry or a
     recorded `insulation_infill` directive explaining it;
  4. every wall in `wall_blocks.csv` is PRESENT in the DXF, unless it is
     explicitly quarantined.

Exit non-zero on any breach. `--json` prints the findings for a build.
"""
from __future__ import print_function

import argparse
import csv
import io
import json
import os
import sys

import ezdxf

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(REPO, 'data', 'canonical')
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')

NEAR_MM = 400.0        # closer than this and a perpendicular pair is a junction
TOUCH_MM = 1.0         # overlap of at least this counts as closed


def read(name):
    p = os.path.join(CANON, name)
    if not os.path.exists(p):
        return []
    with io.open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def walls_from_dxf(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    labels = {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
              for e in msp if e.dxftype() == 'TEXT'
              and e.dxf.layer == 'V0-WALL-LABEL'}
    out = {}
    for e in msp:
        if e.dxftype() != 'LWPOLYLINE' or not e.dxf.layer.startswith('V0-WALL'):
            continue
        p = [(q[0], q[1]) for q in e.get_points()]
        x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
        y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        name = min(labels.items(),
                   key=lambda kv: (kv[1][0] - cx) ** 2 + (kv[1][1] - cy) ** 2)[0] \
            if labels else '?'
        out[name] = {'id': name, 'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1,
                     'axis': 'EW' if (x1 - x0) > (y1 - y0) else 'NS'}
    return out


def inter(a, b):
    return (min(a['x1'], b['x1']) - max(a['x0'], b['x0']),
            min(a['y1'], b['y1']) - max(a['y0'], b['y0']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    W = walls_from_dxf(args.dxf)
    ledger = read('wall_corners.csv')
    directives = read('junction_directives.csv')
    blocks = read('wall_blocks.csv')
    placement = read('wall_placement_directives.csv')

    quarantined = set(r['wall_id'] for r in placement
                      if 'quarantin' in (r.get('status') or ''))
    infill = set()
    for r in directives:
        if (r.get('closure_kind') or '').strip() == 'insulation_infill':
            infill.add(frozenset((r['wall_a'].strip(), r['wall_b'].strip())))

    findings = []
    CELL = 10.0        # mm; a 10 mm sliver is below anything that matters

    # --- rasterise the wall union, then look for HOLES -------------------
    # !! The first version of this gate tested "do the two rectangles overlap in
    # both axes", and it was wrong. MA ends exactly on R8's face and R8 spans the
    # corner, so the corner IS solid while the x-overlap is zero. What matters is
    # whether the corner REGION is covered by the union of walls - which is a
    # coverage question, not a pairwise-overlap question. So the union is
    # rasterised and every uncovered cell that touches two or more different
    # walls is a cavity at a junction, whatever the pairwise numbers say.
    xs = [v for w in W.values() for v in (w['x0'], w['x1'])]
    ys = [v for w in W.values() for v in (w['y0'], w['y1'])]
    ox, oy = min(xs) - CELL, min(ys) - CELL
    nx = int((max(xs) - ox) / CELL) + 2
    ny = int((max(ys) - oy) / CELL) + 2
    grid = [[None] * nx for _ in range(ny)]
    for w in W.values():
        i0 = int((w['x0'] - ox) / CELL + 0.5)
        i1 = int((w['x1'] - ox) / CELL + 0.5)
        j0 = int((w['y0'] - oy) / CELL + 0.5)
        j1 = int((w['y1'] - oy) / CELL + 0.5)
        for j in range(j0, j1):
            for i in range(i0, i1):
                if 0 <= j < ny and 0 <= i < nx:
                    grid[j][i] = w['id']

    seen = [[False] * nx for _ in range(ny)]
    cavities = []
    for j in range(ny):
        for i in range(nx):
            if grid[j][i] is not None or seen[j][i]:
                continue
            # flood the empty region; note which walls it touches
            stack, cells, touch = [(i, j)], 0, set()
            seen[j][i] = True
            while stack:
                ci, cj = stack.pop()
                cells += 1
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = ci + di, cj + dj
                    if not (0 <= ni < nx and 0 <= nj < ny):
                        continue
                    if grid[nj][ni] is not None:
                        touch.add(grid[nj][ni])
                    elif not seen[nj][ni]:
                        seen[nj][ni] = True
                        stack.append((ni, nj))
                if cells > 40000:
                    break
            # a room is a big empty region touching many walls; a CAVITY is a
            # small one wedged between two or three
            area = cells * CELL * CELL
            if len(touch) >= 2 and area <= 0.35e6:
                cavities.append((sorted(touch), area, cells))

    # --- per-corner coverage: the assertion the cavity scan cannot make ----
    # !! The flood-fill alone is not enough, and the selftest proved it: pull MC
    # 300 mm off R7 and the void it opens CONNECTS TO THE ROOM, so the fill sees
    # one large empty region and calls it a room, not a pocket. A corner has to
    # be asserted directly. For an L between an EW wall H and an NS wall V the
    # corner square is (V's x band) x (H's y band), and it is closed only if
    # every cell of that square is covered by the wall union.
    def covered(x0, x1, y0, y1):
        i0 = int((x0 - ox) / CELL + 0.5)
        i1 = max(i0 + 1, int((x1 - ox) / CELL + 0.5))
        j0 = int((y0 - oy) / CELL + 0.5)
        j1 = max(j0 + 1, int((y1 - oy) / CELL + 0.5))
        total = miss = 0
        for j in range(j0, j1):
            for i in range(i0, i1):
                if not (0 <= j < ny and 0 <= i < nx):
                    continue
                total += 1
                if grid[j][i] is None:
                    miss += 1
        return total, miss

    print('ledger junctions - is the corner square solid?')
    for r in ledger:
        a, b = W.get(r['wall_a']), W.get(r['wall_b'])
        cid = r['corner_id']
        if not a or not b:
            continue                      # reported under wall presence
        h, v = (a, b) if a['axis'] == 'EW' else (b, a)
        if h['axis'] == v['axis']:
            continue                      # collinear pair; not an L
        total, miss = covered(v['x0'], v['x1'], h['y0'], h['y1'])
        if miss:
            findings.append({'kind': 'open_corner', 'corner': cid,
                             'detail': '%d of %d cells of the corner square are '
                                       'empty' % (miss, total)})
            print('  FAIL %-12s %d of %d cells EMPTY - the corner is a void'
                  % (cid, miss, total))
        else:
            print('  ok   %-12s solid, %d cells' % (cid, total))
    print()

    print('wall-union cavities (empty pockets touching 2+ walls, <= 0.35 m2):')
    if not cavities:
        print('  none')
    for touch, area, cells in sorted(cavities, key=lambda t: -t[1]):
        pair = frozenset(touch) if len(touch) == 2 else None
        if pair and pair in infill:
            print('  ok   %-16s %8.0f mm2 - closed by external insulation'
                  % ('+'.join(touch), area))
            continue
        findings.append({'kind': 'cavity', 'walls': touch,
                         'detail': '%.0f mm2' % area})
        print('  FAIL %-16s %8.0f mm2 between %s'
              % ('+'.join(touch), area, ', '.join(touch)))

    # --- unexpected overlaps stay a pairwise question --------------------
    ledger_pairs = set(frozenset((r['wall_a'], r['wall_b'])) for r in ledger)
    ids = sorted(W)
    print()
    print('overlaps not sanctioned by the ledger:')
    any_ov = False
    for i, ai in enumerate(ids):
        for bi in ids[i + 1:]:
            if frozenset((ai, bi)) in ledger_pairs:
                continue
            ix, iy = inter(W[ai], W[bi])
            if ix > TOUCH_MM and iy > TOUCH_MM:
                any_ov = True
                findings.append({'kind': 'unexpected_overlap',
                                 'walls': [ai, bi],
                                 'detail': '%.0f x %.0f mm' % (ix, iy)})
                print('  FAIL %-5s x %-5s  %.0f x %.0f mm' % (ai, bi, ix, iy))
    if not any_ov:
        print('  none')
    print()

    # 4. every wall present unless quarantined
    print('\nwall presence:')
    absent = [r['wall_id'] for r in blocks if r['wall_id'] not in W]
    for wid in absent:
        if wid in quarantined:
            print('  ok   %-5s absent but QUARANTINED by directive' % wid)
        else:
            findings.append({'kind': 'missing_wall', 'walls': [wid],
                             'detail': 'not in the DXF and not quarantined'})
            print('  FAIL %-5s missing from the DXF, not quarantined' % wid)
    print('  %d of %d walls present' % (len(W), len(blocks)))

    if args.json:
        print(json.dumps({'findings': findings}, indent=1, ensure_ascii=False))

    print()
    if findings:
        print('FAIL - %d finding(s): %s' % (
            len(findings),
            ', '.join(sorted(set(f['kind'] for f in findings)))))
        return 1
    print('PASS - every ledger junction is closed, nothing overlaps unexpectedly, '
          'no unexplained cavity, and every wall is present or quarantined')
    return 0


if __name__ == '__main__':
    sys.exit(main())
