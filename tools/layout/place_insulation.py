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
why it is placed by directive. Its band is emitted with
`status: unresolved_side` and the exporter skips it until a directive says which
face.

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


def main():
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
        if bool(ev_lo) == bool(ev_hi):
            # neither settles it, or both do - either way it is not decided here
            unresolved.append({'wall_id': w['id'], 'insulation_mm': ins,
                               'evidence_low': ev_lo, 'evidence_high': ev_hi})
            print('%-5s %-5.0f %-5s NOT SETTLED by the drawing - low:%d high:%d'
                  % (w['id'], ins, '?', len(ev_lo), len(ev_hi)))
            continue
        side = 'low' if ev_lo else 'high'
        ev = ev_lo or ev_hi
        lo, hi = ((w['y0'], w['y1']) if w['axis'] == 'EW'
                  else (w['x0'], w['x1']))
        outer = lo - ins if side == 'low' else hi + ins
        b0, b1 = min(lo, outer) if side == 'low' else hi, \
            lo if side == 'low' else max(hi, outer)
        if w['axis'] == 'EW':
            box = [w['x0'], b0, w['x1'], b1]
        else:
            box = [b0, w['y0'], b1, w['y1']]
        bands.append({'wall_id': w['id'], 'insulation_mm': ins,
                      'side': side, 'axis': w['axis'],
                      'x0': round(box[0], 1), 'y0': round(box[1], 1),
                      'x1': round(box[2], 1), 'y1': round(box[3], 1),
                      'status': 'from_drawing', 'evidence': ev})
        print('%-5s %-5.0f %-5s %s' % (w['id'], ins, side, ev[0]))
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
