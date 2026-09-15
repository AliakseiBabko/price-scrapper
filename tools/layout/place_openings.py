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

Where a candidate span comes from - THREE sources, not one
----------------------------------------------------------
Until 2026-09-15 only source (a) was read, and five of ten openings were
reported UNPLACED with "no drawn gap inside <wall> matches its width". That
message was true of what the code looked at and false about the drawing: the
drawing records every one of them, just not as a hatch gap INSIDE a solid.

(a) `candidate_openings` - an unhatched stretch WITHIN one solid. Empty for
    every internal door in this flat, which is why nothing was found.

(b) `bridged_openings_mm` - a doorway that splits its wall into TWO solids.
    The merge in place_named_walls.vector_solids records the gap it bridged.
    !! This is the same record raster_fidelity.py already uses to exclude
    opening spans from its metric, and the same one render_vector_extraction.py
    already draws in red as "NO OPENING PLACED". Two consumers could see the
    doorway and the placer could not. It supplies O8 (1009.9 against a recorded
    1010) and the two 710s in G4C (O1, O7) - which wall_blocks.csv's own G4C
    note had ALREADY written down by coordinate: "the two 710s in the chain are
    the ПР openings the vector records as bridged at 13360.3..14070.3 and
    14790.3..15500.3".

(c) an INTER-WALL gap - the doorway is not in a wall at all, it is the space
    BETWEEN two walls standing on the same line. O5 and O6 are both of this
    kind and both flank the column R4:
        O6  G4d's east end 5146.0 -> R4's west face 6056.0  = 910.0
        O5  R4's east face 6305.9 -> G6's west end 7216.0   = 910.1
    against a recorded 910 for each. Found by projecting every placed wall body
    onto the host wall's own centreline and taking the unoccupied intervals, so
    it needs no new measurement and no new threshold.

Choosing between candidates
---------------------------
!! Width alone CANNOT discriminate O1 from O7: both are 710 mm in the same wall
G4C, and both gaps are drawn. Width is now a FILTER and position is the ranking
key - the coarse basic-plan px span in wall_opening_spans.csv, pushed through
the identification fit. That fit is bad for geometry (3.3% anisotropy, 93 mm
residuals) but it is far better than 710 mm, which is the distance it has to
tell apart here. The geometry still comes entirely from the drawing; the fit
only says WHICH drawn gap a name belongs to - exactly the role it already has
for walls.

!! An opening that cannot be matched is still reported UNPLACED rather than
given a plausible position.
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


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.console import utf8_console  # noqa: E402


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


def inter_wall_gaps(host, walls):
    """Unoccupied stretches on the HOST wall's own centreline.

    A doorway between two walls (O5, O6) leaves no gap inside either one, so
    neither `candidate_openings` nor `bridged_openings_mm` can hold it. Project
    every wall BODY that crosses the host's centreline onto the host's axis,
    merge the occupied intervals, and the holes between them are the doorways.

    !! The host wall itself is included in the occupied set, so its own body can
    never be offered as an opening - only the space beside it.
    """
    # !! face_lo/face_hi are X on an NS wall and Y on an EW one, so a wall can
    # only be tested against the host's line as a BOX. Comparing the raw field
    # pairs silently compares an x against a y and finds nothing.
    def box(w):
        if w['axis'] == 'EW':
            return w['from_mm'], w['face_lo_mm'], w['to_mm'], w['face_hi_mm']
        return w['face_lo_mm'], w['from_mm'], w['face_hi_mm'], w['to_mm']

    hx0, hy0, hx1, hy1 = box(host)
    along, across = (0, 2), (1, 3)
    if host['axis'] == 'NS':
        along, across = (1, 3), (0, 2)
    c = (box(host)[across[0]] + box(host)[across[1]]) / 2.0
    occ = []
    for w in walls:
        if w.get('from_mm') is None or w.get('face_lo_mm') is None:
            continue
        b = box(w)
        if b[across[0]] - 0.5 <= c <= b[across[1]] + 0.5:
            occ.append([b[along[0]], b[along[1]]])
    if not occ:
        return []
    occ.sort()
    merged = [occ[0][:]]
    for a, b in occ[1:]:
        if a <= merged[-1][1] + 0.5:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [{'from_mm': merged[i][1], 'to_mm': merged[i + 1][0],
             'approx_width_mm': merged[i + 1][0] - merged[i][1]}
            for i in range(len(merged) - 1)
            if merged[i + 1][0] - merged[i][1] > 50.0]


def px_span_mm(row, axis, fit):
    """The coarse basic-plan px span as mm - for RANKING only, never geometry."""
    f = fit['x'] if axis == 'EW' else fit['y']
    try:
        lo = f['a'] * float(row['span_lo_basic_px']) + f['b']
        hi = f['a'] * float(row['span_hi_basic_px']) + f['b']
    except (TypeError, ValueError, KeyError):
        return None
    return min(lo, hi), max(lo, hi)


def glazing():
    """The лоджия glazing assembly as extracted from the vector."""
    path = os.path.join(CANON, 'v0_elements_extracted.json')
    if not os.path.exists(path):
        return None
    return json.load(io.open(path, encoding='utf-8')).get('loggia_glazing')


def load_shafts():
    """The ventilation shafts as boxes. They are not walls and never become
    walls - but they FLANK an opening, so the placer has to know them."""
    path = os.path.join(CANON, 'ventilation_shafts.csv')
    if not os.path.exists(path):
        return {}
    out = {}
    for r in csv.DictReader(io.open(path, encoding='utf-8')):
        out[r['shaft_id']] = (float(r['x0_mm']), float(r['y0_mm']),
                              float(r['x1_mm']), float(r['y1_mm']))
    return out


def place_divider_opening(oid, spec, walls, shafts, want):
    """An opening whose flanks are two named ELEMENTS, not one host wall.

    O10, the прихожая-to-кухня passway, is the only one: `wall_openings.csv`
    records its host as "DIVIDER: V2 -> R5". It has never had a span row,
    which is why it was not merely unplaced but INVISIBLE - the placer
    iterates spans, so an opening with no span row is never attempted and
    never reported. It is the gap between the venting shaft and the column,
    and both flanks are immovable, so the drawing fixes it completely.

    The rule is general: the axis in which the two flanks OVERLAP gives the
    opening its face pair; the axis in which they are SEPARATED gives its run.
    """
    names = [t.strip() for t in
             spec.split(':', 1)[-1].replace('->', '→').split('→')]
    if len(names) != 2:
        return None, 'divider spec %r does not name exactly two flanks' % spec

    def box(n):
        if n in shafts:
            return shafts[n]
        w = walls.get(n)
        if not w or w.get('from_mm') is None:
            return None
        if w['axis'] == 'EW':
            return w['from_mm'], w['face_lo_mm'], w['to_mm'], w['face_hi_mm']
        return w['face_lo_mm'], w['from_mm'], w['face_hi_mm'], w['to_mm']

    a, b = box(names[0]), box(names[1])
    for n, v in zip(names, (a, b)):
        if v is None:
            return None, 'flank %s has no geometry' % n

    ox = min(a[2], b[2]) - max(a[0], b[0])      # overlap in x
    oy = min(a[3], b[3]) - max(a[1], b[1])      # overlap in y
    if ox > 0 and oy <= 0:            # separated in y -> the opening runs in y
        lo, hi = sorted([min(a[3], b[3]), max(a[1], b[1])])
        f_lo, f_hi = max(a[0], b[0]), min(a[2], b[2])
        axis = 'NS'
    elif oy > 0 and ox <= 0:
        lo, hi = sorted([min(a[2], b[2]), max(a[0], b[0])])
        f_lo, f_hi = max(a[1], b[1]), min(a[3], b[3])
        axis = 'EW'
    else:
        return None, ('flanks %s and %s do not overlap on exactly one axis'
                      % (names[0], names[1]))

    return {'opening_id': oid, 'wall_id': 'DIVIDER %s|%s' % (names[0], names[1]),
            'solid_id': None, 'axis': axis,
            'face_lo_mm': round(f_lo, 1), 'face_hi_mm': round(f_hi, 1),
            'from_mm': round(lo, 1), 'to_mm': round(hi, 1),
            'width_mm': round(hi - lo, 1),
            'named_width_mm': want or None,
            'width_delta_mm': round(abs((hi - lo) - want), 1) if want else None,
            'span_source': 'gap BETWEEN flanking elements',
            'source': 'flanking element faces'}, None


def main():
    utf8_console()
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
    fit = placed['identification_fit_basic_px_to_mm']

    # rough opening spans from the hatch gaps, per solid
    vsolids = pn.vector_solids(ex, plan)
    pn.clip_to_envelope(vsolids)
    rough = {}
    for s in vsolids:
        key = (s['axis'], round(s['face_lo_mm'], 1), round(s['face_hi_mm'], 1))
        rough.setdefault(key, []).extend(s.get('candidate_openings') or [])
        # (b) the doorways the MERGE bridged. Without these, every internal
        # door in this flat is invisible here - candidate_openings is empty for
        # all four of their walls.
        for lo, hi in (s.get('bridged_openings_mm') or []):
            rough[key].append({'from_mm': lo, 'to_mm': hi,
                               'approx_width_mm': hi - lo})

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
        # (a) + (b) gaps carried by the host's own solid, (c) the space BESIDE
        # it. A gap from (c) lies outside the host wall by construction, so the
        # containment test below is applied only to the first two.
        inside = list(rough.get(key) or [])
        beside = inter_wall_gaps(w, walls.values())
        lines = reveal_lines(plan, s, mm)
        want = float(named.get(oid, {}).get('width_mm', '0').rstrip('?') or 0)
        approx = px_span_mm(r, s['axis'], fit)

        best = None
        for c, is_inside in ([(c, True) for c in inside]
                             + [(c, False) for c in beside]):
            lo, hi = snap(c['from_mm'], lines)[0], snap(c['to_mm'], lines)[0]
            if hi <= lo:
                continue
            # must fall inside the HOST wall, not merely the shared solid
            if is_inside and (hi < w['from_mm'] - 1 or lo > w['to_mm'] + 1):
                continue
            err = abs((hi - lo) - want) if want else 0.0
            if err > WIDTH_TOL_MM:
                continue
            # !! Width is the FILTER; POSITION is the ranking key. O1 and O7 are
            # both 710 mm in G4C and both gaps are drawn, so width ties and
            # whichever came first used to win. The px fit is crude but it only
            # has to separate two gaps 710 mm apart.
            if approx:
                rank = abs((lo + hi) / 2.0 - (approx[0] + approx[1]) / 2.0)
            else:
                rank = err
            if best is None or rank < best[0]:
                best = (rank, lo, hi, err, is_inside)
        if best is None:
            unplaced.append((oid, wid,
                             'no drawn gap inside %s matches its %s mm width'
                             % (wid, want or '?')))
            continue
        _, lo, hi, err, is_inside = best
        src = 'within/bridged solid' if is_inside else 'gap BETWEEN walls'
        out.append({'opening_id': oid, 'wall_id': wid, 'solid_id': w['solid_id'],
                    'axis': s['axis'], 'face_lo_mm': s['face_lo_mm'],
                    'face_hi_mm': s['face_hi_mm'],
                    'from_mm': round(lo, 1), 'to_mm': round(hi, 1),
                    'width_mm': round(hi - lo, 1),
                    'named_width_mm': want or None,
                    'width_delta_mm': round(err, 1) if want else None,
                    'span_source': src,
                    'source': 'vector reveal lines'})
        print('%-4s %-5s %11.1f %11.1f %8.1f %8s  %s'
              % (oid, wid, lo, hi, hi - lo, want or '-', src))

    # --- openings with NO span row at all -----------------------------
    # !! These are the dangerous ones: an opening the loop above never visits
    # cannot appear in `unplaced` either, so it is missing AND silent. O10 was
    # absent from the DXF for exactly this reason and no check said so - it was
    # not in the placed list, not in the unplaced list, and not in the review
    # drawing's own "still open" caption, which counts only `unplaced`.
    shafts = load_shafts()
    elsewhere = []
    seen = set(x['opening_id'] for x in out) | set(o for o, _, _ in unplaced)
    for oid, row in sorted(named.items()):
        if oid in seen:
            continue
        host = (row.get('in_wall_or_divider') or '').strip()
        want = float((row.get('width_mm') or '0').rstrip('?') or 0)
        # Two kinds are DELIBERATELY not openings here, and saying so is not the
        # same as failing to place them. Listing them as UNPLACED would be a
        # false alarm, and a checker that cries wolf gets ignored.
        if (row.get('type') or '').strip() == 'glazing':
            # !! O9 IS an opening, and until 2026-09-15 it was the only element
            # breaking the envelope that carried no opening entity - it was
            # exported as frame + bays + mullions only, so anything iterating
            # V0-OPENING missed the biggest hole in the flat. Owner, arrow on
            # the glazing: "draw it as another opening."
            # It is the one opening that is NOT axis-aligned (the лоджия splays,
            # which is why the plan draws this line diagonal), so it carries an
            # explicit bbox and the gate matches on that.
            gl = glazing()
            if not gl:
                elsewhere.append((oid, 'no glazing geometry extracted'))
                continue
            import math
            axp, ayp = gl['axis_from']
            bxp, byp = gl['axis_to']
            L = math.hypot(bxp - axp, byp - ayp)
            ux, uy = (bxp - axp) / L, (byp - ayp) / L
            nx, ny = -uy, ux
            dep = gl['assembly_depth_mm'] or 150.0
            cor = [(axp, ayp), (bxp, byp),
                   (bxp + nx * dep, byp + ny * dep),
                   (axp + nx * dep, ayp + ny * dep)]
            out.append({'opening_id': oid, 'wall_id': host, 'solid_id': None,
                        'axis': 'DIAGONAL',
                        'bbox': [round(min(c[0] for c in cor), 1),
                                 round(min(c[1] for c in cor), 1),
                                 round(max(c[0] for c in cor), 1),
                                 round(max(c[1] for c in cor), 1)],
                        'run_mm': round(gl['run_mm'], 1),
                        'assembly_depth_mm': dep,
                        'bays': len(gl.get('bays') or []),
                        'mullions': len(gl.get('mullions') or []),
                        'named_width_mm': want or None,
                        'span_source': 'the лоджия glazing assembly, diagonal',
                        'source': 'vector glazing extraction'})
            print('%-4s %-5s %11s %11s %8.1f %8s  %s'
                  % (oid, 'DIAG', '-', '-', gl['run_mm'], want or '-',
                     'diagonal assembly, %d bays' % len(gl.get('bays') or [])))
            continue
        if oid[:-1] in seen and oid[-1:] in ('a', 'b'):
            elsewhere.append((oid, 'a LEAF of the combined unit %s, divided by a '
                                   'frame mullion - one structural opening, '
                                   'already placed' % oid[:-1]))
            continue
        if not host.upper().startswith('DIVIDER'):
            unplaced.append((oid, host or '?',
                             'no span row and host %r is not a divider' % host))
            continue
        rec, why = place_divider_opening(oid, host, walls, shafts, want)
        if rec is None:
            unplaced.append((oid, host, why))
            continue
        out.append(rec)
        print('%-4s %-5s %11.1f %11.1f %8.1f %8s  %s'
              % (oid, 'DIV', rec['from_mm'], rec['to_mm'], rec['width_mm'],
                 want or '-', rec['span_source']))

    if elsewhere:
        print('\nNOT rectangular openings - handled elsewhere, not missing:')
        for oid, why in elsewhere:
            print('  %-4s %s' % (oid, why))

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
                            for o, w, y in unplaced],
               'handled_elsewhere': [{'opening_id': o, 'why': y}
                                     for o, y in elsewhere]},
              io.open(args.out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('\nplaced %d of %d named openings; wrote %s'
          % (len(out), len(named), os.path.relpath(args.out, REPO)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
