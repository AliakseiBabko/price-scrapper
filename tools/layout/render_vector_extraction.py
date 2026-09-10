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

CLAIMED = (28, 130, 60)
UNCLAIMED = (190, 110, 20)
OPENING = (200, 40, 40)
INK = (208, 208, 208)


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

    placed = json.load(io.open(os.path.join(REPO, 'data', 'canonical',
                                            'v0_named_walls_placed.json'),
                               encoding='utf-8'))
    claimed = {}
    for wl in placed['walls']:
        if wl.get('solid_id'):
            claimed.setdefault(wl['solid_id'], []).append(wl['wall_id'])

    LEG = 470
    img = Image.new('RGB', (int(w * Z) + LEG, int(h * Z)), (255, 255, 255))
    bg = Image.fromarray((~mask).astype(np.uint8) * 255).convert('RGB')
    bg = Image.eval(bg, lambda v: 208 if v < 128 else 255)
    img.paste(bg.resize((int(w * Z), int(h * Z)), Image.NEAREST), (0, 0))
    dr = ImageDraw.Draw(img)
    f_s, f_m, f_b = font(13), font(17), font(26)

    def P(x, y):
        return ((sx * x + ox) * Z, (sy * y + oy) * Z)

    n_claimed = 0
    for s in sorted(solids, key=lambda s: s['solid_id']):
        x0, y0, x1, y1 = box_of(s)
        a, b = P(x0, y0), P(x1, y1)
        who = claimed.get(s['solid_id'])
        col = CLAIMED if who else UNCLAIMED
        if who:
            n_claimed += 1
        dr.rectangle([min(a[0], b[0]), min(a[1], b[1]),
                      max(a[0], b[0]), max(a[1], b[1])],
                     outline=col, width=2)
        # the bridged openings, hatched back in
        for lo, hi in (s.get('bridged_openings_mm') or []):
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
        tw = dr.textlength(lab, font=f_s)
        dr.rectangle([cx - tw / 2 - 2, cy - 8, cx + tw / 2 + 2, cy + 8],
                     fill=(255, 255, 255))
        dr.text((cx - tw / 2, cy - 7), lab, fill=col, font=f_s)

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
    for col, lab in ((CLAIMED, '%d claimed by a named wall' % n_claimed),
                     (UNCLAIMED, '%d recognised, not used'
                      % (len(solids) - n_claimed)),
                     (OPENING, 'a doorway bridged when two')):
        dr.rectangle([lx, y, lx + 26, y + 14], outline=col, width=2)
        dr.text((lx + 36, y), lab, fill=(20, 20, 20), font=f_s)
        y += 22
    dr.text((lx + 36, y), 'collinear solids were merged', fill=(20, 20, 20),
            font=f_s)
    y += 30
    dr.text((lx, y), 'How to read it', fill=(0, 0, 0), font=f_m)
    y += 24
    for line in ('A WALL CONTINUES THROUGH ITS DOOR,',
                 'so one solid often carries several',
                 'named walls — the top of the flat is',
                 'one 9715 mm solid holding R1a, G2,',
                 'R3 and G3.',
                 '',
                 'The unused ones are expected, not a',
                 'gap: the drawing continues the',
                 "neighbour's structure past the party",
                 'wall, and a wall can yield a second',
                 'solid at a different face band. The',
                 'model names 25 walls; the drawing',
                 'holds more structure than this flat.',
                 '',
                 'This is a picture of the EXTRACTION,',
                 'not evidence that it is right. The',
                 'checks that can fail are',
                 'check_dxf_closure.py and',
                 'raster_fidelity.py — looking is not',
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
