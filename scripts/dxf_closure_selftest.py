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
PNG = os.path.join(REPO, '_Drawings', 'review',
                   'v0_dxf_readback.png')
SIDECAR = os.path.splitext(PNG)[0] + '.json'
FIDELITY_PNG = os.path.join(REPO, '_Drawings', 'review',
                            'v0_raster_fidelity.png')
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


# --- the classes CODEX seeded in ROUND 5 ------------------------------------
# !! The first is the THIRD instance of one class in this dialogue, and that is
# the part worth remembering: **a collection that deduplicates destroys the
# defect being checked.** Round 2 it was a dict keyed by label, so a duplicate
# WALL overwrote the original and the count never moved. Round 5 it was
# `set(label_names(...))`, so a duplicate LABEL collapsed 26 entities to 25
# distinct names - and the gate printed "25 labels" for a file holding 26.
#
# I wrote the second one while FIXING round 4, which is the other half of the
# lesson: the parity check I added to catch a missing wall was itself built on a
# set.


@case('CODEX r5: an exact duplicate of a V0-WALL-LABEL entity')
def _(doc):
    msp = doc.modelspace()
    src = [e for e in msp if e.dxftype() == 'TEXT'
           and e.dxf.layer == 'V0-WALL-LABEL'][0]
    msp.add_text(src.dxf.text,
                 dxfattribs={'layer': 'V0-WALL-LABEL',
                             'insert': (src.dxf.insert.x, src.dxf.insert.y),
                             'height': src.dxf.height})


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


@inplace('CODEX r5: the PRE-FIX PNG restored, with the current sidecar kept')
def _():
    """The delivered image from a previous round, and a fresh sidecar beside it.

    !! This is the seed the round-4 stale check could not have failed, because
    it authenticated the sidecar and never read the image. CODEX substituted the
    tracked PNG from `23ac367` byte-for-byte and the gate called it current.

    The fixture is that same historical blob, taken from git so the test uses a
    genuinely stale artefact rather than a synthetic one. If the blob is not
    reachable the seed re-renders at a different scale instead, which exercises
    the same binding - the delivered bytes are not what the renderer produces
    now - and says so, rather than skipping silently.
    """
    import subprocess
    got = subprocess.run(
        ['git', 'show', '23ac367:_Drawings/review/v0_dxf_readback.png'],
        cwd=REPO, capture_output=True)
    if got.returncode == 0 and got.stdout:
        with io.open(PNG, 'wb') as f:
            f.write(got.stdout)
        return
    print('       (the 23ac367 blob is unreachable; re-rendering at another '
          'scale instead)')
    subprocess.run([sys.executable,
                    os.path.join(REPO, 'tools', 'layout', 'render_dxf.py'),
                    '--out', PNG, '--scale', '0.13'],
                   cwd=REPO, capture_output=True,
                   env=dict(os.environ, PYTHONIOENCODING='utf-8'))


@inplace('the OTHER delivered image left stale - the one that had no gate')
def _():
    """This is not hypothetical: it actually happened, the day after the
    readback PNG's byte check was written.

    !! Nobody edited the fidelity image. A regenerated copy was reverted with
    `git checkout --` to tidy a working tree, and it stayed stale for a day
    because only ONE of the two delivered images was authenticated. The readback
    PNG survived the identical tidy-up because its gate would have caught it.

    One image checked and one not is not a policy, it is an oversight - and the
    owner found it by asking whether the two pictures were the same age.
    """
    import subprocess
    got = subprocess.run(
        ['git', 'show', 'd605f4a:_Drawings/review/v0_raster_fidelity.png'],
        cwd=REPO, capture_output=True)
    if got.returncode == 0 and got.stdout:
        with io.open(FIDELITY_PNG, 'wb') as f:
            f.write(got.stdout)
        return
    print('       (the d605f4a blob is unreachable; truncating the image '
          'instead)')
    with io.open(FIDELITY_PNG, 'rb') as f:
        blob = f.read()
    with io.open(FIDELITY_PNG, 'wb') as f:
        f.write(blob[:len(blob) // 2])


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


@paired('CODEX r6: a byte-identical duplicate G6 row in wall_blocks.csv')
def _(doc, canon):
    """The fourth appearance of the collapsing-collection class.

    !! Every reader keys these tables into a dict, so last-wins, and the gate
    printed "26 named walls" beside "25 label ENTITIES" before declaring every
    wall present exactly once. The number was on screen and unchecked - the
    second time in this dialogue that printing stood in for checking.

    Closed for the whole family rather than for G6: check_unique now covers
    wall_blocks, wall_corners, wall_placement_directives and
    junction_directives. This seed is the one CODEX demonstrated; the corner
    ledger below is its sibling, and the other two are verified in the artefact.
    """
    wb = os.path.join(canon, 'wall_blocks.csv')
    lines = io.open(wb, encoding='utf-8').read().splitlines(True)
    row = [l for l in lines if l.startswith('G6,')][0]
    lines.append(row)
    io.open(wb, 'w', encoding='utf-8', newline='').write(''.join(lines))


@paired('a duplicate corner_id in the ledger, the same class one table over')
def _(doc, canon):
    wc = os.path.join(canon, 'wall_corners.csv')
    lines = io.open(wc, encoding='utf-8').read().splitlines(True)
    row = [l for l in lines if l.startswith('C_MA_R8,')][0]
    lines.append(row)
    io.open(wc, 'w', encoding='utf-8', newline='').write(''.join(lines))


@paired('SELF-AUDIT: a duplicate entry in the placement, the gate\'s own anchor')
def _(doc, canon):
    """Found by the turn-10 self-audit, not by a review.

    !! Two defects in one line. `read_placement()` read `CANON` directly and
    ignored `--canon`, so the placement - the gate's ONLY absolute anchor
    against a rigid shift - was the one input no seeded fixture could mutate. A
    probe against it could never have failed, which is worse than an unchecked
    input because it reads as covered. And the result was a dict keyed by
    wall_id, so a duplicate entry silently won: the same collapsing-collection
    class as the duplicate wall in round 2 and the duplicate label in round 5.

    That this seed fails on BOTH counts now - duplicate_placement and
    face_drift - is the evidence the isolation reaches the anchor at all.
    """
    import json as _json
    pj = os.path.join(canon, 'v0_named_walls_placed.json')
    j = _json.loads(io.open(pj, encoding='utf-8').read())
    w = [x for x in j['walls'] if x['wall_id'] == 'MC'][0]
    dup = dict(w)
    dup['face_lo_mm'] = w['face_lo_mm'] + 500
    dup['face_hi_mm'] = w['face_hi_mm'] + 500
    j['walls'].append(dup)
    io.open(pj, 'w', encoding='utf-8', newline='').write(
        _json.dumps(j, ensure_ascii=False))


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
        # Both committed artefacts are saved as BYTES and restored whatever
        # happens. A seed that mutates the PNG but restores only the sidecar
        # would leave the tree dirty and the next run measuring a fixture.
        GUARDED = (PNG, SIDECAR, FIDELITY_PNG)
        for name, mutate in INPLACE:
            before = {}
            for path in GUARDED:
                if os.path.exists(path):
                    with io.open(path, 'rb') as handle:
                        before[path] = handle.read()
            try:
                mutate()
                rc = run(DXF)
                if rc != 0:
                    print('  ok      rejected: %s' % name)
                else:
                    print('  FAILED  ACCEPTED: %s' % name)
                    ok = False
            finally:
                for path, blob in before.items():
                    with io.open(path, 'wb') as handle:
                        handle.write(blob)
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
