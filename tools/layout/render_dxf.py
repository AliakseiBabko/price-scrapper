# -*- coding: utf-8 -*-
"""Render a DXF back to a PNG, by reading the DXF - not the JSON it came from.

Why read the DXF rather than the source data
--------------------------------------------
A picture drawn from the same JSON the exporter used proves only that the
exporter and the renderer agree. **This reads the exported file back**, so the
image is evidence about the DXF itself: whether the layers, colours, block
geometry and text actually landed in it. That is also the first half of the
round-trip the accepted design calls for.

Colours come from each entity's LAYER, mapped through the owner's own key, so a
layer that is missing or misnamed shows up as grey rather than silently
inheriting something plausible.

Usage
-----
    py -3 tools/layout/render_dxf.py [--dxf PATH] [--out PATH] [--scale PX_PER_MM]
"""
from __future__ import print_function

import argparse
import collections
import importlib.util
import io
import json
import math
import os
import sys

import ezdxf
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
OUT = os.path.join(REPO, '_Drawings', 'review', 'v0_dxf_readback.png')

# The owner's key, from _Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg
STYLE = {
    'V0-WALL-CONCRETE': ((232, 138, 138), (176, 24, 24), 'concrete frame'),
    'V0-WALL-AERATED': ((150, 214, 160), (24, 132, 48), 'aerated block'),
    'V0-WALL-EXTERNAL': ((240, 168, 226), (196, 46, 172), 'external 300'),
    'V0-WALL-LOGGIA': ((240, 168, 226), (196, 46, 172), 'лоджия enclosure'),
    'V0-LOGGIA-GLAZING': ((120, 200, 235), (30, 80, 120), 'лоджия glazing'),
    'V0-SLAB-EXTENSION': ((252, 240, 176), (196, 168, 20), 'decorative slab'),
    'V0-OPENING': (None, (30, 120, 200), 'opening (from the vector)'),

    'V0-WALL-LABEL': (None, (20, 20, 20), None),
}
DRAW_ORDER = ['V0-SLAB-EXTENSION', 'V0-WALL-CONCRETE', 'V0-WALL-AERATED',
              'V0-WALL-EXTERNAL', 'V0-WALL-LOGGIA', 'V0-LOGGIA-GLAZING',
              'V0-OPENING', 'V0-SUGGESTED-FURN', 'V0-WALL-LABEL']


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '%s.py' % name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def font(size):
    for name in ('DejaVuSans.ttf', 'arial.ttf', 'segoeui.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--scale', type=float, default=0.145)
    args = ap.parse_args()

    doc = ezdxf.readfile(args.dxf)
    msp = doc.modelspace()

    ents = collections.defaultdict(list)
    counts = collections.Counter()
    for e in msp:
        layer = e.dxf.layer
        counts[(layer, e.dxftype())] += 1
        ents[layer].append(e)

    print('read %s' % os.path.relpath(args.dxf, REPO))
    for (layer, kind), n in sorted(counts.items()):
        flag = '' if layer in STYLE else '   <-- layer not in the colour key'
        print('  %-22s %-12s %d%s' % (layer, kind, n, flag))

    pts = []
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE':
            pts += [(p[0], p[1]) for p in e.get_points()]
        elif e.dxftype() == 'LINE':
            pts += [(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]
    if not pts:
        sys.exit('no geometry in the DXF')
    x0 = min(p[0] for p in pts)
    x1 = max(p[0] for p in pts)
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    print('  extent %.0f x %.0f mm' % (x1 - x0, y1 - y0))

    S = args.scale
    PAD, LEG = 120, 430
    W = int((x1 - x0 + 2 * PAD) * S) + LEG
    H = int((y1 - y0 + 2 * PAD) * S)
    img = Image.new('RGB', (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    f_s, f_m, f_b = font(14), font(18), font(25)

    def P(x, y):
        return ((x - x0 + PAD) * S, H - (y - y0 + PAD) * S)

    for layer in DRAW_ORDER + [k for k in ents if k not in DRAW_ORDER]:
        fill, edge, _ = STYLE.get(layer, (None, (140, 140, 140), None))
        for e in ents.get(layer, []):
            t = e.dxftype()
            if t == 'LWPOLYLINE':
                poly = [P(p[0], p[1]) for p in e.get_points()]
                if fill:
                    dr.polygon(poly, fill=fill, outline=edge)
                else:
                    dr.line(poly + [poly[0]], fill=edge, width=2)
            elif t == 'LINE':
                a = P(e.dxf.start.x, e.dxf.start.y)
                b = P(e.dxf.end.x, e.dxf.end.y)
                if layer == 'V0-SUGGESTED-FURN':
                    n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 9))
                    for i in range(0, n, 2):
                        t0, t1 = i / n, min(1.0, (i + 1) / n)
                        dr.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                                 (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                                fill=edge, width=3)
                else:
                    dr.line([a, b], fill=edge, width=2)
            elif t == 'TEXT':
                p = e.dxf.insert
                s = e.dxf.text
                x, y = P(p.x, p.y)
                tw = dr.textlength(s, font=f_s)
                dr.rectangle([x - tw / 2 - 2, y - 9, x + tw / 2 + 2, y + 9],
                             fill=(255, 255, 255))
                dr.text((x - tw / 2, y - 8), s, fill=edge, font=f_s)

    lx, y = W - LEG + 20, 24
    dr.text((lx, y), 'v0 — read back from the DXF', fill=(0, 0, 0), font=f_b)
    y += 32
    dr.text((lx, y), os.path.basename(args.dxf), fill=(110, 110, 110), font=f_s)
    y += 20
    dr.text((lx, y), '%.0f x %.0f mm · %d entities'
            % (x1 - x0, y1 - y0, sum(counts.values())), fill=(110, 110, 110), font=f_s)
    y += 30
    seen = set()
    for layer in DRAW_ORDER:
        st = STYLE.get(layer)
        if not st or not st[2] or layer in seen or layer not in ents:
            continue
        seen.add(layer)
        fill, edge, label = st
        if fill:
            dr.rectangle([lx, y, lx + 28, y + 15], fill=fill, outline=edge, width=2)
        else:
            dr.rectangle([lx, y, lx + 28, y + 15], outline=edge, width=2)
        dr.text((lx + 38, y), label, fill=(20, 20, 20), font=f_s)
        y += 23
    y += 14
    dr.text((lx, y), 'Still open', fill=(200, 40, 40), font=f_m)
    y += 24
    # !! NOTHING BELOW IS WRITTEN BY HAND, and that is the point. This block was
    # hard-coded prose and it went stale TWICE: in round 2 it said M6b was absent
    # while the DXF drew it, and in round 4 CODEX found it saying the лоджия was
    # open and "9 walls carry an OPEN extent exception" while the loop was closed
    # and the ledger held 10. Editing the words was the wrong fix the first time
    # - a caption a person maintains drifts every time the geometry moves, and
    # the owner reads the caption.
    #
    # Now every figure is derived from the same canonical data and the same DXF
    # the gates read, and what was drawn is written to a sidecar that
    # check_dxf_closure.py asserts is current. A stale review drawing fails the
    # closure gate.
    v0 = _load('v0_state')
    walls, _malformed = _load('dxf_wall_entities').read_walls(args.dxf)
    glazing = None
    ep = os.path.join(REPO, 'data', 'canonical', 'v0_elements_extracted.json')
    if os.path.exists(ep):
        with io.open(ep, encoding='utf-8') as f:
            glazing = json.load(f).get('loggia_glazing')
    summary = v0.summary(walls, glazing)
    omitted = []
    opp = os.path.join(REPO, 'data', 'canonical', 'v0_openings_placed.json')
    if os.path.exists(opp):
        with io.open(opp, encoding='utf-8') as f:
            omitted = sorted(u['opening_id']
                             for u in json.load(f).get('unplaced', []))
    for line in v0.caption_lines(summary, omitted):
        dr.text((lx, y), line, fill=(200, 40, 40), font=f_s)
        y += 17
    v0.write_sidecar(summary)
    y += 12
    for line in ('Project dimensions. As-built runs',
                 '1.0–1.9% smaller. DRAFT.'):
        dr.text((lx, y), line, fill=(90, 90, 90), font=f_s)
        y += 18

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    img.save(args.out)
    print('wrote %s %s' % (os.path.relpath(args.out, REPO), img.size))
    return 0


if __name__ == '__main__':
    sys.exit(main())
