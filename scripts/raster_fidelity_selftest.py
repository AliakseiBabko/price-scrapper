# -*- coding: utf-8 -*-
"""Prove the raster check FAILS on translation, scale, drift and a missing wall.

CODEX, `V0_DXF_RASTER_FIDELITY` round 3, finding 4, asked for exactly this:

> *seed translation, scale, endpoint drift, and wrong-wall identity against that
> frozen raster evidence.*

The point is not that the numbers look good. It is that the check is capable of
producing bad ones. The old overlay could not: registered on the DXF's own wall
faces, a translated model dragged the reference with it and scored the same.

Each case mutates a COPY of the exported DXF and asserts
`tools/layout/raster_fidelity.py --dxf <copy>` exits non-zero. The mask case
mutates the frozen evidence instead and asserts exit 2.

Usage
-----
    py -3 scripts/raster_fidelity_selftest.py
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
MASK = os.path.join(REPO, '_Drawings', 'evidence', 'v0_wall_ink_mask.png')
TOOL = os.path.join(REPO, 'tools', 'layout', 'raster_fidelity.py')

WALL_LAYERS = ('V0-WALL-CONCRETE', 'V0-WALL-AERATED', 'V0-WALL-EXTERNAL',
               'V0-WALL-LOGGIA')


def wall_entities(msp):
    return [e for e in msp
            if e.dxftype() == 'LWPOLYLINE' and e.dxf.layer in WALL_LAYERS]


def named(msp, wid):
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


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case('the WHOLE model translated 500 mm - the class the old overlay could not see')
def _(doc):
    msp = doc.modelspace()
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE':
            e.set_points([(q[0] + 500, q[1]) for q in e.get_points()],
                         format='xy')
        elif e.dxftype() == 'TEXT':
            e.dxf.insert = (e.dxf.insert.x + 500, e.dxf.insert.y, 0)


@case('the whole model scaled 3% about the origin')
def _(doc):
    msp = doc.modelspace()
    K = 1.03
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE':
            e.set_points([(q[0] * K, q[1] * K) for q in e.get_points()],
                         format='xy')
        elif e.dxftype() == 'TEXT':
            e.dxf.insert = (e.dxf.insert.x * K, e.dxf.insert.y * K, 0)


@case('endpoint drift: G5 pulled 400 mm off its end')
def _(doc):
    e = named(doc.modelspace(), 'G5')
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    if (x1 - x0) > (y1 - y0):
        x1 -= 400
    else:
        y1 -= 400
    e.set_points([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], format='xy')


@case('one wall displaced sideways onto open floor: R4 moved 600 mm in x')
def _(doc):
    e = named(doc.modelspace(), 'R4')
    e.set_points([(q[0] + 600, q[1]) for q in e.get_points()], format='xy')


@case('a wall the drawing shows is simply absent: G5 deleted')
def _(doc):
    msp = doc.modelspace()
    msp.delete_entity(named(msp, 'G5'))


def run(dxf, mask=None):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    cmd = [sys.executable, TOOL, '--dxf', dxf]
    if mask:
        cmd += ['--mask', mask]
    p = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True,
                       errors='replace')
    return p.returncode, p.stdout


def main():
    if not os.path.exists(DXF) or not os.path.exists(MASK):
        print('need both the exported DXF and the frozen mask')
        return 2

    print('baseline: the real DXF against the frozen mask must PASS')
    rc, out = run(DXF)
    ok = rc == 0
    print('  %s exit %d' % ('ok     ' if ok else 'FAILED ', rc))
    if not ok:
        for line in out.splitlines():
            if 'BREACH' in line or 'FAIL' in line:
                print('     %s' % line.strip())
        print('\nFAIL - fix the baseline before trusting any seeded case')
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
            rc, _ = run(copy)
            if rc != 0:
                print('  ok      rejected (exit %d): %s' % (rc, name))
            else:
                print('  FAILED  ACCEPTED: %s' % name)
                ok = False
        finally:
            shutil.rmtree(d, ignore_errors=True)

    # The evidence itself must be frozen: a tampered mask is not measured
    # against, it is refused. Otherwise "frozen" is a word in a docstring.
    print('\nthe frozen evidence must be refused if it changes:')
    d = tempfile.mkdtemp()
    try:
        from PIL import Image
        import numpy as np
        bad = os.path.join(d, 'tampered.png')
        a = np.asarray(Image.open(MASK).convert('L')).copy()
        a[100:140, 100:140] = 255           # erase a patch of evidence
        Image.fromarray(a).save(bad)
        rc, _ = run(DXF, mask=bad)
        if rc == 2:
            print('  ok      refused a tampered mask (exit 2)')
        else:
            print('  FAILED  measured against a tampered mask (exit %d)' % rc)
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
