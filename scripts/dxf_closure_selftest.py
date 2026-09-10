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

import io
import os
import shutil
import subprocess
import sys
import tempfile

import ezdxf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
CANON = os.path.join(REPO, 'data', 'canonical')
SIDECAR = os.path.join(REPO, '_Drawings', 'review',
                       'v0_dxf_readback.json')
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
PAIRED = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


def paired(name):
    """A case that mutates the DXF **and** a canonical table together.

    !! CODEX round 3, finding 2, is the reason this decorator exists. Its probe
    had to copy the whole tool to get an isolated fixture, because the gate read
    `data/canonical` from a fixed path. A checker that cannot be pointed at
    seeded inputs cannot be adversarially tested against them, so the gate took
    a `--canon` argument and these cases get a writable copy of the directory.

    The mutator is called as `fn(doc, canon_dir)`.
    """
    def deco(fn):
        PAIRED.append((name, fn))
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


# --- the classes CODEX seeded in ROUND 3, both of which PASSED -------------
# !! Both are the same shape of defect and it is not topology: the gate was
# checking the drawing against a table a person edits, so an *ordinary coupled
# correction* made a wrong extent self-consistent. CODEX's phrasing of why the
# first one matters is the part to keep:
#
#   "the export and its purported extent oracle share the same editable
#    measurement"
#
# The answer was to stop treating `wall_blocks.csv` as evidence of extent and
# re-derive the hatched solids from the PDF at check time
# (`tools/layout/vector_extent_oracle.py`), and to make the exception ledger
# validate its own fields rather than allowlist a delta beside decorative ones.


# --- the class CODEX seeded in ROUND 4 --------------------------------------
# !! Not a measurement error and not a table edit: the READER invented geometry.
# Both gates reduced a wall polyline to min/max x/y, so a closed TRIANGLE on
# three of a rectangle's four corners kept the same label, layer, bounding box
# and nominal size, lost half the wall body, and passed both binding checks.
# Everything downstream - corner squares, cavities, body masks, dense edge
# samples - was reasoning about a rectangle nobody had drawn, and no later check
# could ever have noticed, because by then the real polygon was gone.
#
# The seed is kept exactly as CODEX wrote it, and the bulge case below covers the
# other way the exporter's rectangle contract can break.


@case('CODEX r4: MC replaced by a TRIANGLE on three of its own corners')
def _(doc):
    e = named(doc.modelspace(), 'MC')
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    e.set_points([(x0, y0), (x1, y0), (x1, y1)], format='xy')


@case('G6 given a bulged edge - a rectangle by vertices, an arc when drawn')
def _(doc):
    e = named(doc.modelspace(), 'G6')
    p = [(q[0], q[1]) for q in e.get_points()]
    x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
    y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
    e.set_points([(x0, y0, 0, 0, 0.6), (x1, y0), (x1, y1), (x0, y1)],
                 format='xyseb')


INPLACE = []


def inplace(name):
    """A case that mutates a COMMITTED artefact and must be restored after.

    !! The staleness check deliberately compares the committed drawing against
    the committed state, and skips a seeded `--dxf` copy - the sidecar describes
    the real export, not a fixture. So this class of seed cannot use the copy
    runner: written as a `@paired` case it would have mutated a temporary file
    the check never looks at, and passed while testing nothing. A seed that
    cannot fail is worse than no seed, because it reads as coverage.
    """
    def deco(fn):
        INPLACE.append((name, fn))
        return fn
    return deco


@inplace('the review drawing left reporting the PREVIOUS round')
def _():
    """CODEX r4 finding 2, as a permanent seed: the exact stale claims it found."""
    import json as _json
    d = _json.loads(io.open(SIDECAR, encoding='utf-8').read())
    d['open_exceptions'] = (d.get('open_exceptions') or 0) - 1
    d['loggia_loop_closed'] = not d.get('loggia_loop_closed')
    io.open(SIDECAR, 'w', encoding='utf-8', newline='').write(
        _json.dumps(d, indent=1, ensure_ascii=False) + '\n')


@paired('CODEX r3: MC +1000 mm AND wall_blocks.csv edited to match')
def _(doc, canon):
    grow(named(doc.modelspace(), 'MC'), 1000)
    wb = os.path.join(canon, 'wall_blocks.csv')
    s = io.open(wb, encoding='utf-8').read()
    # clear 3315 -> 4315 and solid 3565 -> 4565 keeps clear + 250 == solid, so
    # build_wall_corners.py's invariant cannot defend this class either
    s2 = s.replace('MC,MC,external,300,70,3315,250,3565,',
                   'MC,MC,external,300,70,4315,250,4565,')
    assert s2 != s, 'the MC row in wall_blocks.csv changed shape; fix this seed'
    io.open(wb, 'w', encoding='utf-8', newline='').write(s2)


@paired('CODEX r3: G4a exception evidence falsified, delta_mm left alone')
def _(doc, canon):
    ex = os.path.join(canon, 'wall_extent_exceptions.csv')
    lines = io.open(ex, encoding='utf-8').read().splitlines(True)
    out = ['G4a,1,99999,-25.0,,invented_status,\n' if l.startswith('G4a,')
           else l for l in lines]
    assert out != lines, 'no G4a row; fix this seed'
    io.open(ex, 'w', encoding='utf-8', newline='').write(''.join(out))


@paired('an exception row for a wall that does not exist')
def _(doc, canon):
    ex = os.path.join(canon, 'wall_extent_exceptions.csv')
    s = io.open(ex, encoding='utf-8').read()
    s += 'ZZ9,100,100,0.0,invented,open,"a wall nobody has ever named"\n'
    io.open(ex, 'w', encoding='utf-8', newline='').write(s)


@paired('a wall quietly removed from wall_blocks.csv so its absence is legal')
def _(doc, canon):
    msp = doc.modelspace()
    msp.delete_entity(named(msp, 'R4'))
    wb = os.path.join(canon, 'wall_blocks.csv')
    lines = io.open(wb, encoding='utf-8').read().splitlines(True)
    out = [l for l in lines if not l.startswith('R4,')]
    assert out != lines, 'no R4 row; fix this seed'
    io.open(wb, 'w', encoding='utf-8', newline='').write(''.join(out))


def run(path, canon=None):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    cmd = [sys.executable, GATE, '--dxf', path]
    if canon:
        cmd += ['--canon', canon]
    p = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True,
                       errors='replace')
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

    if PAIRED:
        print('\nseeded defects that mutate the DXF AND a canonical table:')
        for name, mutate in PAIRED:
            d = tempfile.mkdtemp()
            try:
                copy = os.path.join(d, 'seeded.dxf')
                canon = os.path.join(d, 'canonical')
                shutil.copy(DXF, copy)
                shutil.copytree(CANON, canon)
                doc = ezdxf.readfile(copy)
                mutate(doc, canon)
                doc.saveas(copy)
                rc = run(copy, canon)
                if rc != 0:
                    print('  ok      rejected: %s' % name)
                else:
                    print('  FAILED  ACCEPTED: %s' % name)
                    ok = False
            finally:
                shutil.rmtree(d, ignore_errors=True)

    if INPLACE:
        print('\nseeded defects in a COMMITTED artefact (restored after each):')
        for name, mutate in INPLACE:
            before = io.open(SIDECAR, encoding='utf-8').read() \
                if os.path.exists(SIDECAR) else None
            try:
                mutate()
                rc = run(DXF)
                if rc != 0:
                    print('  ok      rejected: %s' % name)
                else:
                    print('  FAILED  ACCEPTED: %s' % name)
                    ok = False
            finally:
                if before is not None:
                    io.open(SIDECAR, 'w', encoding='utf-8',
                            newline='').write(before)
        # the restore must itself be verified: a selftest that leaves the tree
        # dirty has broken the thing it was checking
        if run(DXF) != 0:
            print('  FAILED  the real export no longer passes after restore')
            ok = False
        else:
            print('  ok      the committed artefact is restored and still passes')

    print()
    if ok:
        print('PASS - the real export passes and every seeded defect is rejected')
        return 0
    print('FAIL - a seeded defect was accepted')
    return 1


if __name__ == '__main__':
    sys.exit(main())
