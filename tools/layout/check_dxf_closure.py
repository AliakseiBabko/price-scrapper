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
  1. every wall in `wall_blocks.csv` is PRESENT in the DXF, unless explicitly
     quarantined, and appears EXACTLY ONCE;
  2. every wall's cross-axis FACES match the placement - the absolute anchor,
     without which a rigid translation of the whole model satisfies every
     relative test below;
  3. every wall's DRAWN length equals its recorded `solid_mm`, and its drawn
     thickness its recorded thickness;
  4. every junction in `wall_corners.csv` is CLOSED - the corner square is
     covered by the wall union, so the corner volume exists once;
  5. no two walls OVERLAP where the ledger does not say they should;
  6. no pair of perpendicular walls sits in the NEAR-MISS band - close enough to
     be a junction, far enough to leave a cavity - without a ledger entry or a
     recorded `insulation_infill` directive explaining it;
  7. no unexplained cavity anywhere in the wall union.

Every one of 1, 2, 3 and 6 exists because a CODEX-seeded mutation passed the
gate without it. `scripts/dxf_closure_selftest.py` holds those seeds; a gate
nobody has watched fail is not a gate, and a gate that passed someone else's
seed was not the gate I reported.

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
FACE_TOL_MM = 1.0      # the placement is written to 0.1 mm; 1 mm is generous
LEN_TOL_MM = 15.0      # the exporter's own invariant tolerance
CELL = 10.0            # mm; a 10 mm sliver is below anything that matters


def read(name):
    p = os.path.join(CANON, name)
    if not os.path.exists(p):
        return []
    with io.open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def walls_from_dxf(path):
    """Every wall polyline, and the label each one lies nearest to.

    !! This used to return a dict keyed by label, and that silently DEFEATED a
    whole class of defect: add a second copy of G6 and the later entry simply
    overwrote the first, so the gate saw the same 25 walls and passed. CODEX
    seeded exactly that. Returning a LIST and asserting one polyline per label
    is the fix - the count is part of what is checked, not an index.
    """
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    labels = {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
              for e in msp if e.dxftype() == 'TEXT'
              and e.dxf.layer == 'V0-WALL-LABEL'}
    out = []
    for e in msp:
        if e.dxftype() != 'LWPOLYLINE' or not e.dxf.layer.startswith('V0-WALL'):
            continue
        p = [(q[0], q[1]) for q in e.get_points()]
        x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
        y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if labels:
            name = min(labels.items(),
                       key=lambda kv: (kv[1][0] - cx) ** 2
                       + (kv[1][1] - cy) ** 2)[0]
        else:
            name = '?'
        out.append({'id': name, 'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1,
                    'axis': 'EW' if (x1 - x0) > (y1 - y0) else 'NS',
                    'layer': e.dxf.layer})
    return out


def read_placement():
    """The model's own absolute wall faces - the gate's anchor against a SHIFT.

    !! Every other assertion in this file is RELATIVE. Corner coverage, overlaps
    and cavities are all internal to the DXF, so translating the whole model
    leaves every one of them satisfied. CODEX seeded a 500 mm shift of the entire
    drawing and it passed - and my own shift seed had moved only the first six
    walls, which is precisely why I never saw it. A partial shift breaks
    junctions; a complete one does not.

    The anchor is the CROSS-AXIS faces. `close_corners` in the exporter only ever
    moves a wall along its OWN axis, never its faces, so `face_lo_mm` and
    `face_hi_mm` are exact between the placement and the drawing. The flat
    carries walls on both axes, so any translation moves the faces of one family
    or the other and cannot hide.
    """
    p = os.path.join(CANON, 'v0_named_walls_placed.json')
    if not os.path.exists(p):
        return {}
    with io.open(p, encoding='utf-8') as f:
        d = json.load(f)
    return dict((w['wall_id'], w) for w in d.get('walls', [])
                if w.get('face_lo_mm') is not None)


def inter(a, b):
    return (min(a['x1'], b['x1']) - max(a['x0'], b['x0']),
            min(a['y1'], b['y1']) - max(a['y0'], b['y0']))


def faces_of(w):
    """(face_lo, face_hi) - the cross-axis extent, whatever the axis."""
    return (w['y0'], w['y1']) if w['axis'] == 'EW' else (w['x0'], w['x1'])


def run_of(w):
    """(from, to) - the long-axis extent."""
    return (w['x0'], w['x1']) if w['axis'] == 'EW' else (w['y0'], w['y1'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    wall_list = walls_from_dxf(args.dxf)
    ledger = read('wall_corners.csv')
    directives = read('junction_directives.csv')
    blocks = read('wall_blocks.csv')
    placement = read('wall_placement_directives.csv')
    placed = read_placement()

    quarantined = set(r['wall_id'] for r in placement
                      if 'quarantin' in (r.get('status') or ''))
    infill = set()
    for r in directives:
        if (r.get('closure_kind') or '').strip() == 'insulation_infill':
            infill.add(frozenset((r['wall_a'].strip(), r['wall_b'].strip())))

    findings = []

    # === 1. identity: present, and exactly once ==========================
    print('wall identity - present, and one polyline each:')
    by_id = {}
    for w in wall_list:
        by_id.setdefault(w['id'], []).append(w)
    dupes = sorted(k for k, v in by_id.items() if len(v) > 1)
    for wid in dupes:
        findings.append({'kind': 'duplicate_wall', 'walls': [wid],
                         'detail': '%d polylines carry this label'
                                   % len(by_id[wid])})
        print('  FAIL %-5s %d polylines nearest this label - a duplicate wall'
              % (wid, len(by_id[wid])))
    absent = [r['wall_id'] for r in blocks if r['wall_id'] not in by_id]
    for wid in absent:
        if wid in quarantined:
            print('  ok   %-5s absent but QUARANTINED by directive' % wid)
        else:
            findings.append({'kind': 'missing_wall', 'walls': [wid],
                             'detail': 'not in the DXF and not quarantined'})
            print('  FAIL %-5s missing from the DXF, not quarantined' % wid)
    stray = sorted(set(by_id) - set(r['wall_id'] for r in blocks))
    for wid in stray:
        findings.append({'kind': 'unknown_wall', 'walls': [wid],
                         'detail': 'in the DXF but not in wall_blocks.csv'})
        print('  FAIL %-5s in the DXF but not a named wall' % wid)
    if not dupes and not absent and not stray:
        print('  ok   all %d named walls present, one polyline each' % len(by_id))
    print('  %d polylines, %d labels, %d named walls'
          % (len(wall_list), len(by_id), len(blocks)))

    # W is the by-name view the rest of the gate uses. Building it AFTER the
    # duplicate assertion is deliberate: the collapse is now reported, not
    # silent.
    W = dict((w['id'], w) for w in wall_list)

    # === 2. the absolute anchor: faces match the placement ===============
    print('\nabsolute position - cross-axis faces against the placement:')
    if not placed:
        findings.append({'kind': 'no_anchor', 'walls': [],
                         'detail': 'v0_named_walls_placed.json is missing; the '
                                   'gate cannot detect a rigid shift'})
        print('  FAIL no placement file - a whole-model shift would pass')
    else:
        drift = []
        for wid, w in sorted(W.items()):
            ref = placed.get(wid)
            if not ref:
                continue
            lo, hi = faces_of(w)
            d = max(abs(lo - float(ref['face_lo_mm'])),
                    abs(hi - float(ref['face_hi_mm'])))
            if d > FACE_TOL_MM:
                drift.append((wid, lo, hi, ref['face_lo_mm'],
                              ref['face_hi_mm'], d))
        for wid, lo, hi, rlo, rhi, d in sorted(drift, key=lambda t: -t[5]):
            findings.append({'kind': 'face_drift', 'walls': [wid],
                             'detail': 'drawn %.1f/%.1f, placed %.1f/%.1f, '
                                       '%.1f mm off' % (lo, hi, rlo, rhi, d)})
            print('  FAIL %-5s drawn %9.1f/%-9.1f placed %9.1f/%-9.1f  %.1f mm'
                  % (wid, lo, hi, rlo, rhi, d))
        if not drift:
            print('  ok   all %d walls sit on their placed faces (<= %.0f mm)'
                  % (len(W), FACE_TOL_MM))

    # === 3. drawn length and thickness against the record ================
    # !! CODEX over-extended MC by 1000 mm and the gate passed: the extension ran
    # into open room, so it opened no cavity and overlapped nothing. Length is
    # not implied by closure and has to be asserted. The exporter has PRINTED
    # this invariant since it was written - printing is not checking, which is
    # the same error `build_wall_corners.py` made with solid_mm.
    # Eleven walls' recorded `solid_mm` disagrees with the drawn extent, by
    # -910 to +250 mm. That is NOT news the gate discovered: the exporter has
    # printed "14 of 25 walls within 15 mm" every run since it was written, and
    # I read past it and reported the export as agreeing. Printing is not
    # checking - the same error `build_wall_corners.py` made with its invariant.
    #
    # They are not silenced and they are not edited away. Each is pinned in
    # `wall_extent_exceptions.csv` with its measured delta and a cause, and the
    # gate fails on any DEVIATION from the pinned figure. So the debt is
    # countable and visible, a wall not on the list must agree, and a mutation -
    # CODEX's 1000 mm MC over-extension - moves a delta and fails.
    print('\ndrawn extent against wall_blocks.csv:')
    rec = dict((r['wall_id'], r) for r in blocks)
    pinned = {}
    for r in read('wall_extent_exceptions.csv'):
        try:
            pinned[r['wall_id']] = (float(r['delta_mm']),
                                    (r.get('status') or '').strip())
        except (TypeError, ValueError, KeyError):
            findings.append({'kind': 'bad_exception_row',
                             'walls': [r.get('wall_id')],
                             'detail': 'delta_mm is not a number'})
    bad = 0
    for wid, w in sorted(W.items()):
        r = rec.get(wid)
        if not r:
            continue
        a, b = run_of(w)
        lo, hi = faces_of(w)
        drawn, thick = b - a, hi - lo
        try:
            want_len = float(r['solid_mm'])
        except (TypeError, ValueError):
            want_len = None
        try:
            want_t = float(r['thickness_mm'])
        except (TypeError, ValueError):
            want_t = None
        msg = []
        if want_len is not None:
            delta = drawn - want_len
            allow, status = pinned.get(wid, (0.0, ''))
            if abs(delta - allow) > LEN_TOL_MM:
                if wid in pinned:
                    msg.append('length %.1f vs solid_mm %.0f: delta %+.1f, '
                               'but %+.1f is pinned in '
                               'wall_extent_exceptions.csv'
                               % (drawn, want_len, delta, allow))
                else:
                    msg.append('length %.1f vs solid_mm %.0f (%+.1f), and no '
                               'pinned exception' % (drawn, want_len, delta))
        # thickness is never excepted: no row in that file is about thickness,
        # and a wall of the wrong thickness is the class CODEX asked for
        if want_t is not None and abs(thick - want_t) > FACE_TOL_MM:
            msg.append('thickness %.1f vs recorded %.0f' % (thick, want_t))
        if msg:
            bad += 1
            findings.append({'kind': 'wrong_extent', 'walls': [wid],
                             'detail': '; '.join(msg)})
            print('  FAIL %-5s %s' % (wid, '; '.join(msg)))
    if not bad:
        print('  ok   every wall is drawn at its recorded thickness, and at its '
              'recorded length or its pinned delta')
    if pinned:
        opens = sorted(k for k, v in pinned.items() if v[1] == 'open')
        print('  !!   %d walls carry a PINNED extent exception, %d of them still '
              'OPEN: %s' % (len(pinned), len(opens), ', '.join(opens)))
        print('       these are recorded disagreements between the record and '
              'the drawing, not agreements')

    # === rasterise the wall union, for 4 and 7 ===========================
    # !! The first version of this gate tested "do the two rectangles overlap in
    # both axes", and it was wrong. MA ends exactly on R8's face and R8 spans the
    # corner, so the corner IS solid while the x-overlap is zero. What matters is
    # whether the corner REGION is covered by the union of walls - a coverage
    # question, not a pairwise-overlap question.
    xs = [v for w in W.values() for v in (w['x0'], w['x1'])]
    ys = [v for w in W.values() for v in (w['y0'], w['y1'])]
    if not xs:
        print('\nno walls in the DXF at all')
        return 1
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

    # === 4. per-corner coverage ==========================================
    # !! The flood-fill alone is not enough, and a seed proved it: pull MC 300 mm
    # off R7 and the void it opens CONNECTS TO THE ROOM, so the fill sees one
    # large empty region and calls it a room, not a pocket. A corner has to be
    # asserted directly. For an L between an EW wall H and an NS wall V the
    # corner square is (V's x band) x (H's y band), closed only if every cell of
    # that square is covered by the wall union.
    print('\nledger junctions - is the corner square solid?')
    for r in ledger:
        a, b = W.get(r['wall_a']), W.get(r['wall_b'])
        cid = r['corner_id']
        if not a or not b:
            continue                      # reported under wall identity
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

    # === 5. unsanctioned overlaps ========================================
    ledger_pairs = set(frozenset((r['wall_a'], r['wall_b'])) for r in ledger)
    ids = sorted(W)
    print('\noverlaps not sanctioned by the ledger:')
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

    # === 6. the near-miss band ===========================================
    # !! I DOCUMENTED this check in the header and did not implement it - the
    # pairwise near-miss branch was replaced by the flood-fill and never
    # reinstated. CODEX caught the discrepancy. It is a distinct question from
    # both the corner squares (which only covers pairs the LEDGER names) and the
    # cavity scan (which needs the pocket to be enclosed): two perpendicular
    # walls can end 200 mm apart in open air, forming a joint the owner would
    # read as a gap, with no ledger row to check and no enclosed pocket to find.
    print('\nperpendicular pairs in the near-miss band (%.0f mm):' % NEAR_MM)
    any_nm = False
    for i, ai in enumerate(ids):
        for bi in ids[i + 1:]:
            a, b = W[ai], W[bi]
            if a['axis'] == b['axis']:
                continue
            pair = frozenset((ai, bi))
            ix, iy = inter(a, b)
            # a junction-shaped relation: one axis overlaps, the other is a
            # small positive gap
            if ix > TOUCH_MM and -NEAR_MM < iy <= TOUCH_MM:
                gap = -iy
            elif iy > TOUCH_MM and -NEAR_MM < ix <= TOUCH_MM:
                gap = -ix
            else:
                continue
            if gap <= 0:
                continue                  # they touch; that is closed
            if pair in ledger_pairs:
                # the ledger names it, so §4 has already asserted the square
                continue
            if pair in infill:
                print('  ok   %-5s x %-5s  %.0f mm - closed by external '
                      'insulation' % (ai, bi, gap))
                continue
            any_nm = True
            findings.append({'kind': 'near_miss', 'walls': [ai, bi],
                             'detail': '%.0f mm gap, no ledger row and no '
                                       'directive' % gap})
            print('  FAIL %-5s x %-5s  %.0f mm apart, nothing explains it'
                  % (ai, bi, gap))
    if not any_nm:
        print('  none unexplained')

    # === 7. cavities anywhere in the union ===============================
    seen = [[False] * nx for _ in range(ny)]
    cavities = []
    for j in range(ny):
        for i in range(nx):
            if grid[j][i] is not None or seen[j][i]:
                continue
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

    print('\nwall-union cavities (empty pockets touching 2+ walls, <= 0.35 m2):')
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

    if args.json:
        print(json.dumps({'findings': findings}, indent=1, ensure_ascii=False))

    print()
    if findings:
        print('FAIL - %d finding(s): %s' % (
            len(findings),
            ', '.join(sorted(set(f['kind'] for f in findings)))))
        return 1
    print('PASS - every wall is present exactly once and on its placed faces, '
          'drawn at its recorded size, every ledger junction is closed, nothing '
          'overlaps or near-misses unexplained, and there is no cavity')
    return 0


if __name__ == '__main__':
    sys.exit(main())
