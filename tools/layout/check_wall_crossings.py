# -*- coding: utf-8 -*-
"""Fail if any two wall runs in the flat's geometry model cross one another.

Why this exists
---------------
The owner raised it on 2026-09-04, looking at v17 of the wall drawing: R1a and
R1b were drawn crossing at the corner, and "the walls cannot overlap - when we
calculate the length of a wall section we should take account of the thickness
of the one it is adjacent to, because we shouldn't double count the thickness
of the walls."

He was right, and a sweep of all 25 runs found a SECOND instance he had not
spotted - G2 x G4C, where G4C was drawn running through the top wall. That is
the reason this is a script and not a habit: one crossing was visible, the other
was not, and the difference between them was luck.

The rule it enforces is the model's junction convention: every wall length is the
CLEAR INTERNAL run, face to face between its neighbours, so no wall's length
includes any part of a wall it touches. Corner and T-junction volumes belong to
no wall and are carried as a separate junction allowance.

A T-junction is legal: a wall may butt against another's face, and a run may
pass a wall that stops on it. What is illegal is two runs each extending past
the other's face, which double-counts the shared volume.

Usage
-----
    py -3 tools/layout/check_wall_crossings.py

Exits non-zero on any crossing.
"""
from __future__ import print_function

import csv
import io
import os
import sys

# the model's raster scale: mm per pixel of the BASIC plan. See
# data/canonical/wall_materials.json -> the registration notes.
MM_PER_PX = 9.789

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RUNS = os.path.join(REPO, 'data', 'canonical', 'wall_runs.csv')


def load(path):
    walls = []
    with io.open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            walls.append((
                r['wall_id'],
                float(r['thickness_mm']),
                (float(r['ax_basic_px']), float(r['ay_basic_px'])),
                (float(r['bx_basic_px']), float(r['by_basic_px'])),
            ))
    return walls


def orient(a, b):
    """('h'|'v'|None, fixed, lo, hi) for an axis-aligned run."""
    if a[1] == b[1]:
        return 'h', a[1], min(a[0], b[0]), max(a[0], b[0])
    if a[0] == b[0]:
        return 'v', a[0], min(a[1], b[1]), max(a[1], b[1])
    return None, 0.0, 0.0, 0.0


def crossings(walls):
    half = dict((w[0], w[1] / 2.0 / MM_PER_PX) for w in walls)
    out = []
    for i in range(len(walls)):
        for j in range(i + 1, len(walls)):
            w1, w2 = walls[i], walls[j]
            o1, f1, l1, h1 = orient(w1[2], w1[3])
            o2, f2, l2, h2 = orient(w2[2], w2[3])
            if o1 is None or o2 is None or o1 == o2:
                continue                      # skew or parallel: not this check
            if o1 == 'v':                     # normalise to (horizontal, vertical)
                w1, w2 = w2, w1
                o1, f1, l1, h1, o2, f2, l2, h2 = o2, f2, l2, h2, o1, f1, l1, h1
            into_h = min(f2 - l1, h1 - f2)    # how far the vertical sits inside
            into_v = min(f1 - l2, h2 - f1)    # how far the horizontal sits inside
            if into_h > half[w2[0]] and into_v > half[w1[0]]:
                out.append((w1[0], w2[0], min(into_h, into_v) * MM_PER_PX))
    return sorted(out, key=lambda r: -r[2])


def main():
    if not os.path.exists(RUNS):
        print('missing %s' % RUNS)
        return 2
    walls = load(RUNS)
    bad = crossings(walls)
    print('checked %d wall runs' % len(walls))
    if not bad:
        print('PASS - no wall crosses another; every junction is a clean butt')
        return 0
    for a, b, mm in bad:
        print('  FAIL %-5s x %-5s  overlap %4.0f mm  '
              '- one must stop on the other\'s face' % (a, b, mm))
    print('%d crossing(s). Two solids cannot occupy the same volume, and a '
          'length that runs through a junction double-counts it.' % len(bad))
    return 1


if __name__ == '__main__':
    sys.exit(main())
