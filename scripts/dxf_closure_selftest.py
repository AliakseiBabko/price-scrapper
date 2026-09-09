# -*- coding: utf-8 -*-
"""Prove the DXF closure gate FAILS on a corner void, an overlap, a missing wall.

CODEX, V0_DXF_RASTER_FIDELITY round 1, on the previous check: it *"prints misfits
and returns 0 even when five walls exceed the threshold"* and had *"no explicit
corner-closure assertion"*. The replacement gate has both. This file is the part
that makes it credible: **a gate nobody has watched fail is not a gate**, which is
the same standard `scripts/structural_assembly_selftest.py` already applies.

Each case mutates a COPY of the exported DXF and asserts
`tools/layout/check_dxf_closure.py --dxf <copy>` exits non-zero.

Usage
-----
    py -3 scripts/dxf_closure_selftest.py
"""
from __future__ import print_function

import os
import shutil
import subprocess
import sys
import tempfile

import ezdxf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
GATE = os.path.join(REPO, 'tools', 'layout', 'check_dxf_closure.py')

WALL_LAYERS = ('V0-WALL-CONCRETE', 'V0-WALL-AERATED', 'V0-WALL-EXTERNAL',
               'V0-WALL-LOGGIA')


def wall_entities(msp):
    return [e for e in msp
            if e.dxftype() == 'LWPOLYLINE' and e.dxf.layer in WALL_LAYERS]


def named(msp, wid):
    """The wall polyline whose label text is `wid`."""
    lab = {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
           for e in msp if e.dxftype() == 'TEXT'
           and e.dxf.layer == 'V0-WALL-LABEL'}
    if wid not in lab:
        return None
    tx, ty = lab[wid]
    best = None
    for e in wall_entities(msp):
        p = [(q[0], q[1]) for q in e.get_points()]
        cx = sum(q[0] for q in p) / len(p)
        cy = sum(q[1] for q in p) / len(p)
        d = (cx - tx) ** 2 + (cy - ty) ** 2
        if best is None or d < best[0]:
            best = (d, e)
    return best[1] if best else None


def shrink(e, mm, end='hi'):
    """Pull a wall back along its long axis, opening a void at one end.

    !! `end` matters and one seed here was wrong because of it. Shrinking R1a's
    EAST end does not touch the R1a/R1b corner, which is at its WEST end - so the
    gate correctly accepted that mutation and the failure was in the test, not in
    the check. A negative case has to break the thing it claims to break.
    """
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    if (x1 - x0) > (y1 - y0):
        if end == 'hi':
            x1 -= mm
        else:
            x0 += mm
    else:
        if end == 'hi':
            y1 -= mm
        else:
            y0 += mm
    e.set_points([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], format='xy')


def grow(e, mm):
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    if (x1 - x0) > (y1 - y0):
        x1 += mm
    else:
        y1 += mm
    e.set_points([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], format='xy')


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case('a corner void: MC pulled 300 mm back off R7')
def _(doc):
    e = named(doc.modelspace(), 'MC')
    shrink(e, 300)


@case('a corner void: R1a pulled 300 mm back off R1b (its WEST end)')
def _(doc):
    e = named(doc.modelspace(), 'R1a')
    shrink(e, 300, end='lo')


@case('a corner void: R2 pulled 300 mm off G3 (its north end)')
def _(doc):
    e = named(doc.modelspace(), 'R2')
    shrink(e, 300, end='hi')


@case('an unsanctioned overlap: G6 grown 400 mm into R5')
def _(doc):
    e = named(doc.modelspace(), 'G6')
    grow(e, 400)


@case('a missing wall that is not quarantined: R6 deleted')
def _(doc):
    msp = doc.modelspace()
    e = named(msp, 'R6')
    msp.delete_entity(e)


@case('SIX walls shifted 500 mm, so the junctions between them and the rest open')
def _(doc):
    msp = doc.modelspace()
    for e in wall_entities(msp)[:6]:
        p = [(q[0] + 500, q[1]) for q in e.get_points()]
        e.set_points([(q[0], q[1]) for q in p], format='xy')


# --- the classes CODEX seeded, every one of which PASSED ------------------
# !! Round 2 of V0_DXF_RASTER_FIDELITY: CODEX did what the previous artefact
# asked ("do not take the six on trust - seed your own") and three of its seeds
# went straight through. Each of the three exposed a different structural gap in
# the gate, not a threshold that needed nudging:
#
#   * the whole model shifted     - every assertion in the gate was RELATIVE, and
#                                   my own shift seed above moved only the first
#                                   six walls, which BREAKS junctions. A complete
#                                   translation breaks nothing relative. Fixed by
#                                   anchoring cross-axis faces to the placement.
#   * a duplicated wall           - walls_from_dxf returned a dict keyed by label,
#                                   so the copy overwrote the original and the
#                                   count never changed. Fixed by returning a list.
#   * a wall over-extended 1000mm - it ran into open room, opening no cavity and
#                                   overlapping nothing. Length was never asserted,
#                                   only printed. Fixed by the extent check.
#
# They are kept here verbatim in intent, and the two extra classes CODEX
# recommended but did not seed are below them.


@case("CODEX: the WHOLE model shifted 500 mm, so nothing relative changes")
def _(doc):
    msp = doc.modelspace()
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE':
            e.set_points([(q[0] + 500, q[1]) for q in e.get_points()],
                         format='xy')
        elif e.dxftype() == 'TEXT':
            e.dxf.insert = (e.dxf.insert.x + 500, e.dxf.insert.y, 0)


@case('CODEX: G6 duplicated - a second polyline on the same footprint')
def _(doc):
    msp = doc.modelspace()
    e = named(msp, 'G6')
    msp.add_lwpolyline([(q[0], q[1]) for q in e.get_points()], format='xy',
                       dxfattribs={'layer': e.dxf.layer, 'closed': True})


@case('CODEX: MC over-extended 1000 mm into open room')
def _(doc):
    grow(named(doc.modelspace(), 'MC'), 1000)


@case('CODEX recommended: G6 correctly placed but 100 mm too thick')
def _(doc):
    e = named(doc.modelspace(), 'G6')
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    if (x1 - x0) > (y1 - y0):
        y1 += 100                      # thicken across its own axis
    else:
        x1 += 100
    e.set_points([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], format='xy')


@case('R7 slid 500 mm ALONG its own axis - the residual hole in a face anchor')
def _(doc):
    e = named(doc.modelspace(), 'R7')
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    if (x1 - x0) > (y1 - y0):
        x0, x1 = x0 + 500, x1 + 500    # faces unchanged; the run moves
    else:
        y0, y1 = y0 + 500, y1 + 500
    e.set_points([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], format='xy')


@case('a pinned extent exception silently widened: G4a shortened another 200 mm')
def _(doc):
    shrink(named(doc.modelspace(), 'G4a'), 200)


def run(path):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, GATE, '--dxf', path], cwd=REPO,
                       env=env, capture_output=True, text=True, errors='replace')
    return p.returncode


def main():
    if not os.path.exists(DXF):
        print('no exported DXF; run tools/layout/export_v0_dxf.py first')
        return 2
    print('baseline: the real DXF must PASS')
    rc = run(DXF)
    ok = rc == 0
    print('  %s  exit %d' % ('ok     ' if ok else 'FAILED ', rc))
    if not ok:
        print('\nFAIL - the gate rejects the real export; fix that before trusting '
              'any seeded case')
        return 1

    print('\nseeded defects, each must be REJECTED:')
    for name, mutate in CASES:
        d = tempfile.mkdtemp()
        try:
            copy = os.path.join(d, 'seeded.dxf')
            shutil.copy(DXF, copy)
            doc = ezdxf.readfile(copy)
            mutate(doc)
            doc.saveas(copy)
            rc = run(copy)
            if rc != 0:
                print('  ok      rejected: %s' % name)
            else:
                print('  FAILED  ACCEPTED: %s' % name)
                ok = False
        finally:
            shutil.rmtree(d, ignore_errors=True)

    print()
    if ok:
        print('PASS - the real export passes and every seeded defect is rejected')
        return 0
    print('FAIL - a seeded defect was accepted')
    return 1


if __name__ == '__main__':
    sys.exit(main())
