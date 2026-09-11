# -*- coding: utf-8 -*-
"""Show what the VECTOR EXTRACTION actually recognised in the PDF, and what it isn't.

Every other review picture in `_Drawings/review/` shows a RESULT - the model, or
the model measured against the drawing. None of them shows the step in between:
the hatch-validated wall solids the extractor finds in
`3Б_3+ МН5_287.pdf`, which named wall claimed each one, and which ones nothing
claimed. That is the thing to eyeball when the question is *"how does the
recognition work and what did it recognise"* rather than *"is the answer right"*.

What is drawn
-------------
Each recognised solid is a box, labelled with its `solid_id`, thickness and
length, coloured by what became of it:

  * **claimed** - a named wall from `wall_blocks.csv` sits on it. Several walls
    often share one solid, because **a wall continues through its door**: the top
    of the flat is one 9715 mm solid carrying R1a, G2, R3 and G3.
  * **unclaimed** - recognised, and deliberately not used. 20 of 37, and that is
    expected rather than a gap: the drawing continues the neighbour's structure
    past the party wall, and each wall's two face-pairs can yield a second solid
    at a different face band. **The model has 25 named walls; the drawing has
    more structure than this flat.**
  * **bridged opening** - where two collinear solids were merged across a doorway
    (`MERGE_OVER_OPENING_MM`), the opening is hatched back in, because it is the
    span where the drawing prints no face line and where a fidelity check must
    not score.

The background is the frozen ink mask, placed by the committed registration, so
the boxes sit on the drawing they came from.

⚠️ **This is a picture of the EXTRACTION, not evidence that it is correct.** The
checks that can fail are `check_dxf_closure.py` and `raster_fidelity.py`; a
render is for looking, and looking is not a gate. It exists because three of the
last five defects were found by rendering an intermediate result and looking at
it, when reasoning about the numbers had not found them.

Usage
-----
    py -3 tools/layout/render_vector_extraction.py [--out PATH] [--zoom N]
"""
from __future__ import print_function

import argparse
import importlib.util
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, '_Drawings', 'review', 'v0_vector_extraction.png')

CLAIMED = (28, 130, 60)          # a named wall sits on it
INSULATION = (214, 122, 40)      # masonry + insulation as one hatched band
SECOND_LEAF = (120, 120, 200)    # the other face-pair of a wall already claimed
NOT_A_WALL = (150, 150, 150)     # not on any wall line: a fixture, or a sliver
OPENING = (200, 40, 40)
INS_BAND = (255, 190, 130)       # the insulation itself, from place_insulation
CORNER = (150, 220, 170)         # a corner square the ledger assigns an owner


def classify(s, walls, blocks, claimed, bands):
    """What each unclaimed solid IS - by test, not by hand-labelling.

    !! The owner read the first version of this picture and said S9, S12, S13
    and S35 "don't exist" - S35 being "a stove drawn inside the apartment". He
    was right: they are hatched objects the reader finds, and calling them all
    "recognised, not used" put a drawn stove in the same bucket as the party
    wall's second leaf. A bucket that holds both is not a classification.
    """
    if s['solid_id'] in claimed:
        return 'claimed', CLAIMED
    # masonry + insulation drawn as one band
    for b in bands:
        w = next((x for x in walls if x['id'] == b['wall_id']), None)
        if not w:
            continue
        th = float(blocks[b['wall_id']]['thickness_mm'])
        if (s['axis'] == w['axis']
                and abs(s['thickness_mm'] - (th + b['insulation_mm'])) < 3.0):
            lo, hi = ((w['y0'], w['y1']) if w['axis'] == 'EW'
                      else (w['x0'], w['x1']))
            if s['face_lo_mm'] - 3 <= lo and s['face_hi_mm'] + 3 >= hi:
                return 'insulated assembly of %s' % b['wall_id'], INSULATION
    # the other face-pair of a wall already claimed: same axis, same run, and
    # one face shared
    for w in walls:
        if w['axis'] != s['axis']:
            continue
        lo, hi = ((w['y0'], w['y1']) if w['axis'] == 'EW'
                  else (w['x0'], w['x1']))
        r0, r1 = ((w['x0'], w['x1']) if w['axis'] == 'EW'
                  else (w['y0'], w['y1']))
        if (min(s['to_mm'], r1) - max(s['from_mm'], r0) > 0.5 * (r1 - r0)
                and (abs(s['face_lo_mm'] - lo) < 3 or abs(s['face_hi_mm'] - hi) < 3)):
            return 'second leaf at %s' % w['id'], SECOND_LEAF
    return 'not on any wall line', NOT_A_WALL


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(HERE, '%s.py' % name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def font(size):
    for n in ('DejaVuSans.ttf', 'arial.ttf', 'segoeui.ttf'):
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            continue
    return ImageFont.load_default()


def box_of(s):
    """(x0, y0, x1, y1) in mm for a solid, whatever its axis."""
    if s['axis'] == 'EW':
        return s['from_mm'], s['face_lo_mm'], s['to_mm'], s['face_hi_mm']
    return s['face_lo_mm'], s['from_mm'], s['face_hi_mm'], s['to_mm']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--zoom', type=float, default=2.6)
    args = ap.parse_args()

    oracle = _load('vector_extent_oracle')
    ok, got = oracle.pdf_identity()
    if not ok:
        sys.exit('the source PDF is not the one the oracle trusts: %s' % got)
    solids = oracle.vector_solids()

    rf = _load('raster_fidelity')
    reg = json.load(io.open(rf.REGISTRATION, encoding='utf-8'))
    sx, ox, sy, oy = reg['sx'], reg['ox'], reg['sy'], reg['oy']
    mask = rf.load_mask(rf.MASK)
    Z = args.zoom
    h, w = mask.shape

    import csv
    ent = _load('dxf_wall_entities')
    dxf = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
    walls_dxf, _bad = ent.read_walls(dxf)
    blocks = {}
    with io.open(os.path.join(REPO, 'data', 'canonical', 'wall_blocks.csv'),
                 encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            blocks[r['wall_id']] = r
    bands = []
    ip = os.path.join(REPO, 'data', 'canonical', 'v0_insulation_placed.json')
    if os.path.exists(ip):
        bands = json.load(io.open(ip, encoding='utf-8')).get('bands', [])
    placed = json.load(io.open(os.path.join(REPO, 'data', 'canonical',
                                            'v0_named_walls_placed.json'),
                               encoding='utf-8'))
    claimed = {}
    no_solid = []
    for wl in placed['walls']:
        if wl.get('solid_id'):
            claimed.setdefault(wl['solid_id'], []).append(wl['wall_id'])
        else:
            # A named wall the vector plan does not contain, so it is placed by
            # directive and this picture CANNOT draw it. It must still be
            # declared: on 2026-09-11 the owner reviewed this render and marked
            # M6b as a "missing wall", because a drawing that silently omits an
            # element it cannot show is indistinguishable from one where the
            # element does not exist. M6b is in wall_blocks.csv and in the DXF.
            no_solid.append(wl['wall_id'])

    LEG = 470
    img = Image.new('RGB', (int(w * Z) + LEG, int(h * Z)), (255, 255, 255))
    bg = Image.fromarray((~mask).astype(np.uint8) * 255).convert('RGB')
    bg = Image.eval(bg, lambda v: 208 if v < 128 else 255)
    img.paste(bg.resize((int(w * Z), int(h * Z)), Image.NEAREST), (0, 0))
    dr = ImageDraw.Draw(img)
    f_s, f_m, f_b = font(13), font(17), font(26)

    def P(x, y):
        return ((sx * x + ox) * Z, (sy * y + oy) * Z)

    # !! The owner's finding on the first version: "M2 is not touching MA. See
    # the gap." The gap between M2's solid (ends 8980.6) and MA's (starts
    # 9050.6) is exactly 70.0 mm, which is MA's recorded insulation. It was
    # never a void - the layer was simply not drawn. Drawn first, under the
    # solids, so the gap reads as the thing that fills it.
    for b in bands:
        a, q = P(b['x0'], b['y0']), P(b['x1'], b['y1'])
        dr.rectangle([min(a[0], q[0]), min(a[1], q[1]),
                      max(a[0], q[0]), max(a[1], q[1])],
                     fill=INS_BAND, outline=INSULATION, width=2)

    kinds = {}
    suppressed = {}
    n_open = 0
    n_claimed = 0
    for s in sorted(solids, key=lambda s: s['solid_id']):
        x0, y0, x1, y1 = box_of(s)
        a, b = P(x0, y0), P(x1, y1)
        who = claimed.get(s['solid_id'])
        kind, col = classify(s, walls_dxf, blocks, claimed, bands)
        if s['length_mm'] < 500 and not who:
            kind, col = 'sliver under 500 mm', NOT_A_WALL
        # !! Owner, twice: "let's remove some noise... S20 nonexistent, S19
        # nonexistent, S09 nonexistent... S11 is noise, it's a venting shaft...
        # S13 and S12 not on any wall line, exactly, this is just noise. S35 is
        # noise." He is right that they are not walls, and drawing them at the
        # same weight as the structure is what made the picture unreadable. They
        # are OMITTED from the drawing and LISTED in the legend - the record
        # keeps them, the picture does not carry them.
        if kind in ('not on any wall line', 'sliver under 500 mm'):
            suppressed.setdefault(kind, []).append(s['solid_id'])
            kinds[kind] = kinds.get(kind, 0) + 1
            continue
        kinds[kind.split(' of ')[0].split(' at ')[0]] =             kinds.get(kind.split(' of ')[0].split(' at ')[0], 0) + 1
        if who:
            n_claimed += 1
        dr.rectangle([min(a[0], b[0]), min(a[1], b[1]),
                      max(a[0], b[0]), max(a[1], b[1])],
                     outline=col, width=2)
        # the bridged openings, hatched back in
        for lo, hi in (s.get('bridged_openings_mm') or []):
            n_open += 1
            if s['axis'] == 'EW':
                p, q = P(lo, s['face_lo_mm']), P(hi, s['face_hi_mm'])
            else:
                p, q = P(s['face_lo_mm'], lo), P(s['face_hi_mm'], hi)
            dr.rectangle([min(p[0], q[0]), min(p[1], q[1]),
                          max(p[0], q[0]), max(p[1], q[1])],
                         outline=OPENING, width=3)
        cx = (min(a[0], b[0]) + max(a[0], b[0])) / 2
        cy = (min(a[1], b[1]) + max(a[1], b[1])) / 2
        lab = s['solid_id']
        if who:
            lab += ' ' + '+'.join(sorted(who))
        else:
            # !! The first version suppressed this label, so a drawn stove read
            # as a bare id and looked like an unexplained wall. Naming it is the
            # whole point of the classification.
            lab += ' ' + kind
        tw = dr.textlength(lab, font=f_s)
        dr.rectangle([cx - tw / 2 - 2, cy - 8, cx + tw / 2 + 2, cy + 8],
                     fill=(255, 255, 255))
        dr.text((cx - tw / 2, cy - 7), lab, fill=col, font=f_s)

    # --- the openings, which the first version omitted entirely -----------
    # Owner: "The opening is missing. Again, all the openings are missing."
    # Correct - only the BRIDGED merges were marked. These are the openings
    # place_openings.py positioned from the drawn reveal lines.
    n_placed_op = 0
    op_path = os.path.join(REPO, 'data', 'canonical', 'v0_openings_placed.json')
    if os.path.exists(op_path):
        op = json.load(io.open(op_path, encoding='utf-8'))
        for o in op.get('openings', []):
            if o.get('axis') == 'EW':
                x0, y0, x1, y1 = (o['from_mm'], o['face_lo_mm'],
                                  o['to_mm'], o['face_hi_mm'])
            else:
                x0, y0, x1, y1 = (o['face_lo_mm'], o['from_mm'],
                                  o['face_hi_mm'], o['to_mm'])
            a, q = P(x0, y0), P(x1, y1)
            dr.rectangle([min(a[0], q[0]), min(a[1], q[1]),
                          max(a[0], q[0]), max(a[1], q[1])],
                         outline=(30, 120, 200), width=3)
            t = o.get('opening_id', '?')
            dr.text((min(a[0], q[0]) + 4, min(a[1], q[1]) - 16), t,
                    fill=(30, 120, 200), font=f_s)
            n_placed_op += 1
        omitted = sorted(u['opening_id'] for u in op.get('unplaced', []))
    else:
        omitted = []

    # --- the corner squares the ledger owns -------------------------------
    # !! Owner, and he has said it more than once: "R1b and R1a should create the
    # angle, not a cavity... we should take into account the thickness of the
    # adjacent wall and either extend one of the walls to fill in the gap in the
    # corner. If it's a T-shape connection we need to adjust to touch the wall.
    # If it's an angle, we need to take into account the thickness."
    #
    # The EXTRACTION cannot show that, and this render was hiding the fact. A
    # face-pair extraction splits an L-shaped hatched region into two rectangles
    # that meet at a POINT: S14's run starts at 3230.9, S18's ends at 15990.3,
    # so the corner square 2980.8..3230.9 x 15990.2..16240.1 belongs to neither
    # and reads as a cavity. It is not one - R1a and R1b are one monolithic
    # casting - and `wall_corners.csv` says which wall owns each corner. Drawing
    # the owned squares is what makes the angle read as solid.
    n_corner = 0
    try:
        with io.open(os.path.join(REPO, 'data', 'canonical',
                                  'wall_corners.csv'), encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                A = next((x for x in walls_dxf if x['id'] == r['wall_a']), None)
                B = next((x for x in walls_dxf if x['id'] == r['wall_b']), None)
                if not A or not B:
                    continue
                H, V = (A, B) if A['axis'] == 'EW' else (B, A)
                if H['axis'] == V['axis']:
                    continue
                a, q = P(V['x0'], H['y0']), P(V['x1'], H['y1'])
                dr.rectangle([min(a[0], q[0]), min(a[1], q[1]),
                              max(a[0], q[0]), max(a[1], q[1])],
                             fill=CORNER, outline=CLAIMED, width=2)
                t = r['corner_id'].replace('C_', '')
                dr.text((min(a[0], q[0]), max(a[1], q[1]) + 3), t,
                        fill=CLAIMED, font=f_s)
                n_corner += 1
    except Exception:
        pass

    lx, y = int(w * Z) + 20, 24
    dr.text((lx, y), 'v0 — what the vector', fill=(0, 0, 0), font=f_b)
    y += 32
    dr.text((lx, y), 'extraction recognised', fill=(0, 0, 0), font=f_b)
    y += 42
    for line in ('hatch-validated wall solids read from',
                 '3Б_3+ МН5_287.pdf, on the frozen ink mask',
                 'via the committed registration'):
        dr.text((lx, y), line, fill=(110, 110, 110), font=f_s)
        y += 17
    y += 16
    rows = [(CLAIMED, '%d claimed by a named wall' % n_claimed),
            (INS_BAND, '%d insulation band(s), drawn' % len(bands))]
    for k in ('insulated assembly', 'second leaf', 'not on any wall line',
              'sliver under 500 mm'):
        if kinds.get(k):
            col = {'insulated assembly': INSULATION,
                   'second leaf': SECOND_LEAF}.get(k, NOT_A_WALL)
            rows.append((col, '%d %s' % (kinds[k], k)))
    rows.append((CORNER, '%d corner square(s) the ledger owns' % n_corner))
    rows.append((OPENING, '%d doorway(s) bridged' % n_open))
    rows.append(((30, 120, 200), '%d opening(s) placed from reveals'
                 % n_placed_op))
    for col, lab in rows:
        dr.rectangle([lx, y, lx + 26, y + 14],
                     fill=col if col == INS_BAND else None,
                     outline=col if col != INS_BAND else INSULATION, width=2)
        dr.text((lx + 36, y), lab, fill=(20, 20, 20), font=f_s)
        y += 22
    y += 8
    for kind in ('not on any wall line', 'sliver under 500 mm'):
        ids = suppressed.get(kind) or []
        if not ids:
            continue
        dr.text((lx, y), 'OMITTED, %d %s:' % (len(ids), kind),
                fill=(120, 120, 120), font=f_s)
        y += 17
        dr.text((lx + 10, y), ', '.join(sorted(ids)), fill=(120, 120, 120),
                font=f_s)
        y += 20
    if no_solid:
        # Drawn in the same warning red the annotations use, not the grey of the
        # omitted solids: those are things correctly left out, this is a wall
        # that EXISTS and is not on this picture.
        dr.text((lx, y), 'NOT DRAWN HERE, %d named wall(s):' % len(no_solid),
                fill=(176, 48, 48), font=f_s)
        y += 17
        dr.text((lx + 10, y), ', '.join(sorted(no_solid)), fill=(176, 48, 48),
                font=f_s)
        y += 19
        for line in ('placed by directive - in wall_blocks.csv',
                     'and in the DXF, but the vector plan has',
                     'no solid for it, so this picture cannot',
                     'show it. ABSENT HERE IS NOT ABSENT.'):
            dr.text((lx + 10, y), line, fill=(176, 48, 48), font=f_s)
            y += 15
        y += 6
    y += 6
    dr.text((lx, y), 'How to read it', fill=(0, 0, 0), font=f_m)
    y += 24
    for line in ('A WALL CONTINUES THROUGH ITS DOOR,',
                 'so one solid often carries several',
                 'named walls: S14 is one 9715 mm',
                 'solid holding R1a, G2, R3 and G3.',
                 '',
                 'THE 70 mm GAPS ARE THE INSULATION,',
                 'not voids. M2 ends at 8980.6 and',
                 "MA's masonry starts at 9050.6 -",
                 "exactly MA's recorded 70 mm. The",
                 'layer was missing, not the contact.',
                 '',
                 'AN INSULATED ASSEMBLY is hatched as',
                 'ONE band: S22 is 400 = R8 250 + 150,',
                 'S31 is 400 = R9 250 + 150. Those two',
                 'looked like noise and are the',
                 'evidence for which face the',
                 'insulation sits on.',
                 '',
                 'A SECOND LEAF shares a run and a',
                 "face with a wall already named -",
                 "S37 is the party wall's other side.",
                 '',
                 'THE OMITTED ONES ARE NOT WALLS: a',
                 'drawn stove (S35), the venting shaft',
                 '(S11, S19, S20), a window element',
                 '(S12, S13), and slivers. Listed above',
                 'rather than drawn - the record keeps',
                 'them, the picture does not.',
                 '',
                 'A CORNER SQUARE is drawn because the',
                 'extraction cannot show one: a face-',
                 'pair split makes two rectangles meet',
                 'at a POINT, so an L reads as a cavity.',
                 'R1a and R1b are one casting; the',
                 'ledger says who owns each corner.',
                 '',
                 'This is a picture of the EXTRACTION,',
                 'not evidence it is right. The checks',
                 'that can fail are check_dxf_closure',
                 'and raster_fidelity - looking is not',
                 'a gate.'):
        dr.text((lx, y), line, fill=(60, 60, 60), font=f_s)
        y += 17

    d = os.path.dirname(args.out)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    img.save(args.out)
    print('%d solids recognised, %d claimed by a named wall, %d not used'
          % (len(solids), n_claimed, len(solids) - n_claimed))
    print('wrote %s %s' % (os.path.relpath(args.out, REPO), img.size))
    return 0


if __name__ == '__main__':
    sys.exit(main())
