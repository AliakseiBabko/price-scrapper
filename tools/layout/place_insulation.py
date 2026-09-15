# -*- coding: utf-8 -*-
"""Place the EXTERNAL INSULATION band, with the side taken from the drawing.

Why this exists, and why it reverses an earlier instruction
-----------------------------------------------------------
Owner, **2026-09-08**: insulation must not be carried as a separate layer,
because it may be removed or left in place. That was recorded and followed, and
`project_decisions.md` still carried it as a standing decision.

Owner, **2026-09-10**, looking at the extraction render: *"still that M2 is not
touching MA. See the gap. There shouldn't be gaps. There should be an insulation
layer, which is outside — 70 millimetres thick. I want you to draw this external
insulation layer instead of leaving the gap."*

**That is a reversal and it is his to make.** It also turned out to explain the
gap exactly, which is why it is implemented rather than queried:

  * MA's masonry faces are y 9050.6..9350.3 and it records `insulation_mm` 70.
  * M2 records **0** and its solid ends at **8980.6**.
  * 9050.6 − 8980.6 = **70.0 mm.**

So M2 never butted MA's masonry — it butts **MA's insulation**, and the 70 mm
"gap" between the two hatched solids *is* the insulation band. It was never a
defect; it was a missing element.

Which side the insulation goes on is EVIDENCE, not a heuristic
--------------------------------------------------------------
A flat-centroid rule gets M6b wrong, because the лоджия is an appendix and M6b
sits on the wrong side of the centre. So each wall's outer face is decided by the
drawing, two ways, and a wall the drawing does not settle is reported rather
than guessed:

  * **composite** — a hatched solid whose thickness equals masonry + insulation
    and whose band contains the masonry. `S22` is 400 mm = R8's 250 + 150, and
    `S31` is 400 mm = R9's 250 + 150. **These two were sitting in the
    "unclaimed, not used" pile looking like noise; they are the evidence.**
  * **perpendicular abutment** — a solid whose run stops exactly
    `insulation_mm` short of the masonry face, i.e. it abuts the insulation.
    That is the MA case, and both `S16` (M2) and `S22` stop on 8980.6.

⚠️ **M6b is not settled by either test**, and it is not guessed. That is
consistent: the drawing does not contain M6b's 200 mm masonry either, which is
why it is placed by directive.

**Owner directive, 2026-09-11** — the third source, and it is now used: he
identified M6b as the loggia's external wall and set the side himself. *"M6b is
the external wall of the loggia… 200 mm thick aerated concrete wall with
external insulation"*, and *"when we're looking at the image it's to the
right… 6131 — it is to the plus x side"*. The reasoning is the loggia's own
geometry: three walls plus a glazed face, where M2 is shared between two
loggias and MA and R8 both face back into the apartment, leaving M6b as the only
outward wall. Read from `insulation_side` in `wall_blocks.csv` and emitted as
`status: from_owner_directive`, **kept distinct from `from_drawing` so the two
can never be confused** — a directive is the owner's authority, not the
drawing's evidence. ⚠️ Note the side is the OPPOSITE of R8's, which is correct
and is exactly why a centroid rule fails here.

A band is interrupted by every opening in its host wall
--------------------------------------------------------
Owner, **2026-09-11**: *"The window opening should be clear from any external
insulation… they have gaps in the window openings, which is logical because
insulation is for the walls only."* **He is right and it was measurable: before
this, all three bands ran straight through their windows — MA across O4 by
1380 mm, MB across O2 by 1800 mm, MC across O3 by 1800 mm, so 4980 mm of
insulation was drawn where there is no wall to insulate.** Every placed opening
in the model was affected, because all three sit on the three insulated external
walls. He also notes the source drawing already shows those gaps, so this was
the extraction failing to reproduce evidence rather than a missing decision.

So a band is now emitted as one or more SEGMENTS along its wall's run, split
around the openings in that wall. A wall with no openings still yields exactly
one segment, unchanged.

Usage
-----
    py -3 tools/layout/place_insulation.py [--out PATH]
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
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
OUT = os.path.join(CANON, 'v0_insulation_placed.json')

TOL_MM = 2.5


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.console import utf8_console  # noqa: E402


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(HERE, '%s.py' % name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def evidence_for(wall, ins, th, solids, side):
    """Why the insulation belongs on `side` ('low'/'high'), or an empty list."""
    lo, hi = ((wall['y0'], wall['y1']) if wall['axis'] == 'EW'
              else (wall['x0'], wall['x1']))
    run0, run1 = ((wall['x0'], wall['x1']) if wall['axis'] == 'EW'
                  else (wall['y0'], wall['y1']))
    outer = lo - ins if side == 'low' else hi + ins
    band_lo, band_hi = min(lo, outer), max(hi, outer)
    out = []
    for s in solids:
        f0, f1 = s['face_lo_mm'], s['face_hi_mm']
        if s['axis'] == wall['axis']:
            if (abs(s['thickness_mm'] - (th + ins)) < TOL_MM
                    and abs(f0 - band_lo) < TOL_MM
                    and abs(f1 - band_hi) < TOL_MM):
                out.append('composite solid %s is %.0f mm = %.0f masonry + %.0f '
                           'insulation, spanning %.1f..%.1f'
                           % (s['solid_id'], s['thickness_mm'], th, ins, f0, f1))
        else:
            # must actually cross this wall's run to be abutting it
            if min(f1, run1) - max(f0, run0) <= 1:
                continue
            if abs(s['to_mm'] - outer) < TOL_MM or abs(s['from_mm'] - outer) < TOL_MM:
                out.append('perpendicular solid %s stops exactly on %.1f, the '
                           'insulation face' % (s['solid_id'], outer))
    return sorted(set(out))


def openings_for(wall_id, openings):
    """The (from_mm, to_mm) spans of every placed opening hosted by this wall."""
    return sorted((o['from_mm'], o['to_mm']) for o in openings
                  if o.get('wall_id') == wall_id)


def split_run(run0, run1, gaps):
    """`run0..run1` minus every span in `gaps`, as a list of segments.

    Returns the whole run when there are no gaps, so a wall without openings is
    unaffected. Segments shorter than TOL_MM are dropped rather than emitted as
    slivers - an opening flush with the wall end would otherwise leave one.
    """
    segs = [(run0, run1)]
    for g0, g1 in gaps:
        nxt = []
        for a, b in segs:
            if g1 <= a or g0 >= b:      # no overlap
                nxt.append((a, b))
                continue
            if a < g0:
                nxt.append((a, min(g0, b)))
            if b > g1:
                nxt.append((max(g1, a), b))
        segs = nxt
    return [(a, b) for a, b in segs if (b - a) > TOL_MM]


def occluding_spans(band_box, axis, wall_id, walls):
    """Along-axis spans of `band_box` that ANOTHER WALL's body already fills.

    Owner, 2026-09-15, on the contour overlay: *"external insulation should not
    cover all the wall, just the exposed segment."* Right, and it was wrong in
    two measurable places - R8's band ran 0.045 m2 through MA's body and R9's
    ran 0.045 m2 through MC's. A face another wall abuts is not an external
    face, so it carries no external insulation; the band was following the
    wall's whole length instead of the part actually exposed.
    """
    out = []
    bx0, by0, bx1, by1 = band_box
    for o in walls:
        if o['id'] == wall_id:
            continue
        ox0, oy0, ox1, oy1 = o['x0'], o['y0'], o['x1'], o['y1']
        if min(bx1, ox1) - max(bx0, ox0) <= TOL_MM:
            continue
        if min(by1, oy1) - max(by0, oy0) <= TOL_MM:
            continue
        out.append((max(bx0, ox0), min(bx1, ox1)) if axis == 'EW'
                   else (max(by0, oy0), min(by1, oy1)))
    return sorted(out)


def exposed_end_bands(w, ins, side, walls, run_axis):
    """The layer carried around a wall END that nothing abuts.

    Owner, same review, three arrows marked *"missing pieces of insulation"* -
    all of them at a wall's END face, where the band stopped dead instead of
    turning the corner. R9's south end is the clearest: MB's band stops at
    R9's west face 9131.0 and R9's own band starts on its east face, so the
    250 mm of R9's own south face between them had nothing on it at all.

    An end is EXPOSED when no other wall body meets it. The layer is carried at
    THIS wall's own insulation thickness, and it reaches across the wall plus
    its own band so the corner closes as a solid rather than an L with a
    notch missing.
    """
    out = []
    for end in ('lo', 'hi'):
        # !! A neighbour TOUCHES this end, it does not overlap it, so an
        # intersection test with a tolerance-sized probe finds nothing and
        # every end reads as exposed. Reach REACH_MM past the face instead, and
        # require the neighbour to cover a real fraction of it rather than
        # clip a corner - otherwise a wall running past the side registers.
        REACH_MM, MIN_COVER = 30.0, 0.25
        if run_axis == 'EW':
            e = w['x0'] if end == 'lo' else w['x1']
            lo, hi = w['y0'], w['y1']
            near = (e - REACH_MM, e) if end == 'lo' else (e, e + REACH_MM)
        else:
            e = w['y0'] if end == 'lo' else w['y1']
            lo, hi = w['x0'], w['x1']
            near = (e - REACH_MM, e) if end == 'lo' else (e, e + REACH_MM)
        need = (hi - lo) * MIN_COVER
        abutted = False
        for o in walls:
            if o['id'] == w['id']:
                continue
            oa = (o['x0'], o['x1']) if run_axis == 'EW' else (o['y0'], o['y1'])
            oc = (o['y0'], o['y1']) if run_axis == 'EW' else (o['x0'], o['x1'])
            if min(near[1], oa[1]) - max(near[0], oa[0]) <= 0:
                continue
            if min(hi, oc[1]) - max(lo, oc[0]) >= need:
                abutted = True
                break
        if abutted:
            continue
        # the band across the end, reaching over the wall AND its own side band
        if run_axis == 'EW':
            x0, x1 = (e - ins, e) if end == 'lo' else (e, e + ins)
            y0, y1 = ((w['y0'] - ins, w['y1']) if side == 'low'
                      else (w['y0'], w['y1'] + ins))
        else:
            y0, y1 = (e - ins, e) if end == 'lo' else (e, e + ins)
            x0, x1 = ((w['x0'] - ins, w['x1']) if side == 'low'
                      else (w['x0'], w['x1'] + ins))
        out.append((end, [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]))
    return out


def main():
    utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    args = ap.parse_args()

    ent = _load('dxf_wall_entities')
    oracle = _load('vector_extent_oracle')
    ok, got = oracle.pdf_identity()
    if not ok:
        sys.exit('the source PDF is not the one the oracle trusts: %s' % got)
    solids = oracle.vector_solids()
    walls, malformed = ent.read_walls(DXF)
    if malformed:
        sys.exit('the DXF has malformed wall entities; fix those first')
    blocks = {}
    with io.open(os.path.join(CANON, 'wall_blocks.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            blocks[r['wall_id']] = r

    op_path = os.path.join(CANON, 'v0_openings_placed.json')
    openings = []
    if os.path.exists(op_path):
        openings = json.load(io.open(op_path, encoding='utf-8')).get('openings', [])

    bands, unresolved = [], []
    print('%-5s %-5s %-5s %s' % ('wall', 'ins', 'side', 'evidence from the drawing'))
    for w in sorted(walls, key=lambda v: v['id']):
        rec = blocks.get(w['id'])
        if not rec:
            continue
        raw = (rec.get('insulation_mm') or '').strip()
        if not raw:
            continue
        try:
            ins = float(raw)
        except ValueError:
            continue
        if ins <= 0:
            continue
        th = float(rec['thickness_mm'])
        ev_lo = evidence_for(w, ins, th, solids, 'low')
        ev_hi = evidence_for(w, ins, th, solids, 'high')
        directed = (rec.get('insulation_side') or '').strip().lower()
        if bool(ev_lo) == bool(ev_hi):
            # The drawing does not settle it. An OWNER DIRECTIVE may - and only
            # an owner directive: this is never inferred, and a centroid rule is
            # known to get M6b wrong because the loggia is an appendix.
            if directed in ('low', 'high'):
                # !! The reason belongs to the WALL, not to the mechanism.
                # This message hard-coded M6b's reasoning and printed it for
                # whatever wall took the directive branch - so when M2 gained
                # insulation on 2026-09-15 it was labelled with an argument
                # concluding M6b is the ONLY outward wall here, which is now
                # false and reads as evidence against what was just recorded.
                side, ev, status = directed, [
                    'owner directive: insulation_side=%s for %s in '
                    'wall_blocks.csv, because the drawing evidences neither '
                    'face. The REASONING differs per wall and lives in that '
                    'row notes column.' % (directed, w['id'])],                     'from_owner_directive'
            else:
                unresolved.append({'wall_id': w['id'], 'insulation_mm': ins,
                                   'evidence_low': ev_lo, 'evidence_high': ev_hi})
                print('%-5s %-5.0f %-5s NOT SETTLED by the drawing, and no '
                      'insulation_side directive - low:%d high:%d'
                      % (w['id'], ins, '?', len(ev_lo), len(ev_hi)))
                continue
        else:
            side = 'low' if ev_lo else 'high'
            ev = ev_lo or ev_hi
            status = 'from_drawing'
            if directed and directed != side:
                # A directive that contradicts the drawing is a real conflict and
                # must not be silently resolved either way.
                sys.exit('%s: insulation_side directive says %r but the drawing '
                         'evidences %r - resolve this before re-running'
                         % (w['id'], directed, side))
        lo, hi = ((w['y0'], w['y1']) if w['axis'] == 'EW'
                  else (w['x0'], w['x1']))
        outer = lo - ins if side == 'low' else hi + ins
        b0, b1 = min(lo, outer) if side == 'low' else hi, \
            lo if side == 'low' else max(hi, outer)
        if w['axis'] == 'EW':
            box = [w['x0'], b0, w['x1'], b1]
        else:
            box = [b0, w['y0'], b1, w['y1']]
        # The band follows the wall's RUN, interrupted by every opening in it:
        # insulation is for walls, and a window is not a wall.
        run0, run1 = ((w['x0'], w['x1']) if w['axis'] == 'EW'
                      else (w['y0'], w['y1']))
        # An explicitly RECORDED extent clips the band before anything else.
        # M2 is the case: its west face is shared with the neighbour's лоджия
        # except at the southern end, and the drawing cannot show that - there
        # is no ink west of M2 at all, so the owner is the only source. A wall
        # with no recorded extent is unaffected.
        clip = None
        try:
            cf = (rec.get('insulation_from_mm') or '').strip()
            ct = (rec.get('insulation_to_mm') or '').strip()
            if cf and ct:
                clip = (float(cf), float(ct))
        except ValueError:
            clip = None
        gaps = openings_for(w['id'], openings)
        # ...and interrupted AGAIN wherever another wall's body fills the band's
        # own footprint, because that face is not exposed. See occluding_spans.
        occl = occluding_spans(box, w['axis'], w['id'], walls)
        lo_r, hi_r = min(run0, run1), max(run0, run1)
        if clip:
            lo_r, hi_r = max(lo_r, clip[0]), min(hi_r, clip[1])
            print('%-17s recorded extent %.1f..%.1f - the rest of this face is '
                  'not exposed' % ('', clip[0], clip[1]))
        segs = (split_run(lo_r, hi_r, sorted(list(gaps) + list(occl)))
                if hi_r > lo_r else [])
        for i, (s0, s1) in enumerate(segs):
            if w['axis'] == 'EW':
                bx = [s0, box[1], s1, box[3]]
            else:
                bx = [box[0], s0, box[2], s1]
            bands.append({'wall_id': w['id'], 'insulation_mm': ins,
                          'side': side, 'axis': w['axis'],
                          'segment': i, 'of_segments': len(segs),
                          'x0': round(bx[0], 1), 'y0': round(bx[1], 1),
                          'x1': round(bx[2], 1), 'y1': round(bx[3], 1),
                          'status': status, 'evidence': ev,
                          'interrupted_by': [o['opening_id'] for o in openings
                                             if o.get('wall_id') == w['id']]})
        # the layer carried around each EXPOSED end, closing the corner
        caps = (rec.get('insulation_end_caps') or '').strip().lower()
        if caps == 'none':
            print('%-17s end caps SUPPRESSED by the record - these ends '
                  'are not exposed' % '')
        for end, bx in ([] if caps == 'none'
                        else exposed_end_bands(w, ins, side, walls, w['axis'])):
            bands.append({'wall_id': w['id'], 'insulation_mm': ins,
                          'side': side, 'axis': w['axis'],
                          'segment': 'end_%s' % end, 'of_segments': None,
                          'x0': bx[0], 'y0': bx[1], 'x1': bx[2], 'y1': bx[3],
                          'status': status,
                          "evidence": ev + ["carried around this wall's %s END, "
                                            "which no other wall abuts - the "
                                            "envelope layer is continuous around "
                                            "an exposed corner" % end],
                          'interrupted_by': []})
            print('%-5s %-5.0f %-5s  + end cap at its %s end (%.0f x %.0f)'
                  % (w['id'], ins, side, end, bx[2] - bx[0], bx[3] - bx[1]))
        if occl:
            print('%-17s occluded by an abutting wall over %s'
                  % ('', ', '.join('%.0f..%.0f' % t for t in occl)))
        note = ('' if not gaps else
                '  [%d segment(s), broken at %s]'
                % (len(segs), ', '.join(o['opening_id'] for o in openings
                                        if o.get('wall_id') == w['id'])))
        print('%-5s %-5.0f %-5s %s%s' % (w['id'], ins, side, ev[0], note))
        for extra in ev[1:]:
            print('%-17s %s' % ('', extra))

    payload = {
        'id': 'zk-dubravinskiy-v0-insulation',
        'what': ('The external insulation band per wall, with the SIDE taken '
                 'from the drawing rather than from a centroid heuristic - see '
                 'the module docstring for why a heuristic gets M6b wrong.'),
        'instruction': ('Owner 2026-09-10 reversed his 2026-09-08 decision that '
                        'insulation must not be a modelled layer: "There should '
                        'be an insulation layer, which is outside - 70 '
                        'millimetres thick. I want you to draw this external '
                        'insulation layer instead of leaving the gap." The gap '
                        'he pointed at, between M2 and MA, is exactly 70.0 mm.'),
        'pdf_sha256': oracle.PDF_SHA256,
        'bands': bands,
        'unresolved': unresolved,
    }
    with io.open(args.out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, indent=1, ensure_ascii=False) + '\n')
    print('\n%d band(s) placed from the drawing, %d not settled'
          % (len(bands), len(unresolved)))
    for u in unresolved:
        print('   !! %s - the drawing settles neither face; it is NOT guessed, '
              'and the exporter skips it until a directive says which'
              % u['wall_id'])
    print('wrote %s' % os.path.relpath(args.out, REPO))
    return 0


if __name__ == '__main__':
    sys.exit(main())
