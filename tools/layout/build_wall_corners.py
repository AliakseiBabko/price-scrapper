# -*- coding: utf-8 -*-
"""Build and check the corner ledger for the flat's wall model.

The problem the owner posed, 2026-09-04
---------------------------------------
"One bad thing is overlapping. Another bad thing is creating a void. A correct
junction is, for example, MA and R8, R8 and MB - a perfect corner when you take
the thickness into account. If we connect R1a and R1b we get a void at the very
corner. You should extend either R1b or R1a by the thickness, 250 mm."

He is right, and it breaks the convention this repo adopted one version earlier.
"Every length is the clear internal run" cannot double-count a corner, but it
leaves every L-corner unfilled. A corner is a solid and exactly one wall owns it.

Why this is a LEDGER and not a re-snap of the drawing
-----------------------------------------------------
The first attempt snapped the drawn pixel runs until the corners closed. That was
the wrong instrument: it moved lengths that come from printed dimensions and the
owner's own chains by tens of millimetres, to satisfy a raster registration that
is only good to ~50 mm. The drawing locates walls; it does not define them.

So the corner decision lives in the LENGTHS instead. Each wall carries:

    clear_mm  what the plan prints and what a tape held inside the room reads
    solid_mm  clear_mm + the thickness of every corner this wall OWNS

Nothing is double-counted, nothing is voided, and no printed number is disturbed.

Ownership is deterministic, so the ledger does not depend on who builds it:

    1. the THICKER wall owns the corner     (the envelope beats a partition)
    2. on a tie, the LONGER run owns it     (the continuous line beats a stub)
    3. on a tie, the alphabetically first   (only so the output is stable)

Rule 1 independently reproduces the two junctions the owner pointed to as already
correct - MA over R8 and MB over R8 - which is the check that it is the right rule
rather than a convenient one.

Usage
-----
    py -3 tools/layout/build_wall_corners.py            # check the ledger
    py -3 tools/layout/build_wall_corners.py --write    # (re)generate it

Exits non-zero if any L-corner is unowned, owned twice, or absent from the ledger.
"""
from __future__ import print_function

import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_wall_junctions import (MM_PER_PX, RUNS, TOL_MM,  # noqa: E402
                                  NEAR_MM, load, orient,
                                  successor_groups, is_dominant_pair,
                                  butts_not_corners)

LEDGER = os.path.join(os.path.dirname(RUNS), 'wall_corners.csv')
FIELDS = ['corner_id', 'kind', 'wall_a', 'wall_b', 'owner',
          'owner_gains_mm', 'note']


def run_len_mm(w):
    return (abs(w['b'][0] - w['a'][0]) + abs(w['b'][1] - w['a'][1])) * MM_PER_PX


FRAME = 'concrete'      # the monolithic RC frame; everything else is infill


def pick_owner(w1, w2):
    """(owner, other) by the deterministic rule."""
    f1, f2 = w1['cls'] == FRAME, w2['cls'] == FRAME
    if f1 != f2:
        return (w1, w2) if f1 else (w2, w1)
    if w1['t'] != w2['t']:
        return (w1, w2) if w1['t'] > w2['t'] else (w2, w1)
    if abs(run_len_mm(w1) - run_len_mm(w2)) > 1.0:
        return (w1, w2) if run_len_mm(w1) > run_len_mm(w2) else (w2, w1)
    return (w1, w2) if w1['id'] < w2['id'] else (w2, w1)


def classify(walls):
    """-> (list of L corners, list of T junctions)"""
    tol, near = TOL_MM / MM_PER_PX, NEAR_MM / MM_PER_PX
    byid = dict((w['id'], w) for w in walls)
    groups = successor_groups(walls)
    Ls, Ts = [], []
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
            if not (lh - near <= fv <= hh + near and lv - near <= fh <= hv + near):
                continue
            if not is_dominant_pair(h, v, groups, byid, near):
                continue          # this junction belongs to a successor sibling
            if butts_not_corners(h, v):
                continue          # a thin partition on a frame face: a butt
            ah, av = h['t'] / 2.0 / MM_PER_PX, v['t'] / 2.0 / MM_PER_PX
            h_int = (fv - lh > av + tol) and (hh - fv > av + tol)
            v_int = (fh - lv > ah + tol) and (hv - fh > ah + tol)
            if h_int and v_int:
                continue                       # a true crossing: check_wall_crossings
            if h_int or v_int:
                thru, butt = (h, v) if h_int else (v, h)
                Ts.append((thru['id'], butt['id']))
            else:
                own, oth = pick_owner(h, v)
                Ls.append((own, oth))
    return Ls, Ts


def rows_from(Ls):
    out = []
    for own, oth in sorted(Ls, key=lambda r: (r[0]['id'], r[1]['id'])):
        a, b = sorted([own['id'], oth['id']])
        out.append({
            'corner_id': 'C_%s_%s' % (a, b),
            'kind': 'L',
            'wall_a': a,
            'wall_b': b,
            'owner': own['id'],
            'owner_gains_mm': '%g' % oth['t'],
            'note': '%s runs through to %s\'s far face; %s stops on %s\'s near face'
                    % (own['id'], oth['id'], oth['id'], own['id']),
        })
    return out


def main():
    walls = load(RUNS)
    Ls, Ts = classify(walls)
    want = rows_from(Ls)
    print('%d L-corners, %d T-junctions across %d wall runs'
          % (len(Ls), len(Ts), len(walls)))

    if '--write' in sys.argv:
        with io.open(LEDGER, 'w', encoding='utf-8', newline='') as f:
            wr = csv.DictWriter(f, fieldnames=FIELDS)
            wr.writeheader()
            wr.writerows(want)
        print('wrote %s' % LEDGER)

    if not os.path.exists(LEDGER):
        print('FAIL - no ledger. Run with --write')
        return 1

    with io.open(LEDGER, encoding='utf-8') as f:
        have = dict((r['corner_id'], r) for r in csv.DictReader(f))
    problems = []
    for r in want:
        got = have.get(r['corner_id'])
        if got is None:
            problems.append('%s missing from the ledger' % r['corner_id'])
        elif got['owner'] not in (r['wall_a'], r['wall_b']):
            problems.append('%s owner %r is not one of its two walls'
                            % (r['corner_id'], got['owner']))
        elif got['owner_gains_mm'] != r['owner_gains_mm']:
            problems.append('%s: owner gains %s, geometry says %s'
                            % (r['corner_id'], got['owner_gains_mm'],
                               r['owner_gains_mm']))
    for cid in have:
        if cid not in set(r['corner_id'] for r in want):
            problems.append('%s in the ledger is not a corner in the geometry' % cid)

    gains = {}
    for r in want:
        gains.setdefault(r['owner'], []).append((r['owner_gains_mm'], r['corner_id']))
    print('\nsolid_mm = clear_mm + the corners a wall owns:')
    for wid in sorted(gains):
        tot = sum(float(g) for g, _ in gains[wid])
        print('  %-5s + %s = +%g mm' % (wid, ' + '.join(g for g, _ in gains[wid]), tot))
    owned = set()
    for r in want:
        other = r['wall_b'] if r['owner'] == r['wall_a'] else r['wall_a']
        owned.add(other)
    print('  every other wall: solid_mm = clear_mm')

    if problems:
        for p in problems:
            print('  FAIL %s' % p)
        return 1
    print('\nPASS - every L-corner is owned exactly once; no void, no double count')
    return 0


if __name__ == '__main__':
    sys.exit(main())
