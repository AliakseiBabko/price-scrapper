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
# !! NO FILLS, by owner instruction 2026-09-15: *"do not fill in the polygons
# of the wall segments, because in this case I won't see the wall overlapping -
# assign a colour just for the contour, not for the filling."* He is right, and
# it matters more here than it looks: a filled polygon drawn later PAINTS OVER
# an earlier one, so an overlap is exactly the thing a fill hides, and the
# corner overlaps this model DOES sanction (a wall extending over its neighbour
# to own a corner) were invisible. Outlines make both the sanctioned and any
# unsanctioned overlap readable at a glance. The edge colour still carries the
# material identity, and the legend swatches are hollow to match.
STYLE = {
    'V0-WALL-CONCRETE': (None, (176, 24, 24), 'concrete frame'),
    'V0-WALL-AERATED': (None, (24, 132, 48), 'aerated block'),
    'V0-WALL-EXTERNAL': (None, (196, 46, 172), 'external 300'),
    'V0-WALL-LOGGIA': (None, (196, 46, 172), 'лоджия enclosure'),
    'V0-LOGGIA-GLAZING': (None, (30, 80, 120), 'лоджия glazing'),
    'V0-SLAB-EXTENSION': (None, (196, 168, 20), 'decorative slab'),
    'V0-INSULATION': (None, (214, 122, 40), 'external insulation 70/150'),
    'V0-OPENING': (None, (30, 120, 200), 'opening (from the vector)'),
    # Deliberately NOT a wall colour. The shafts are common property, immovable,
    # and they add surface while removing floor - reading as a wall is exactly
    # the mistake this grey guards against.
    'V0-VENT-SHAFT': (None, (90, 90, 104), 'ventilation shaft (not a wall)'),

    'V0-WALL-LABEL': (None, (20, 20, 20), None),
}
DRAW_ORDER = ['V0-SLAB-EXTENSION', 'V0-INSULATION', 'V0-WALL-CONCRETE',
              'V0-WALL-AERATED',
              'V0-WALL-EXTERNAL', 'V0-WALL-LOGGIA', 'V0-LOGGIA-GLAZING',
              'V0-VENT-SHAFT',
              'V0-OPENING', 'V0-SUGGESTED-FURN', 'V0-WALL-LABEL']


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.console import utf8_console  # noqa: E402


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



REGISTRATION = os.path.join(REPO, '_Drawings', 'evidence',
                            'v0_raster_registration.json')
PLAN_RASTER = os.path.join(REPO, '_Inbox', '_Visual_Drop',
                           'fllor_plan_detailed.jpeg')


def plan_underlay(size, x0, y0, PAD, S, H):
    """The developer's own drawing, warped under the model at the SAME scale.

    Owner, 2026-09-15: *"I want the base image like a raster image as a basis
    to show the difference."* A model drawn on a blank sheet can only be
    checked against itself; drawn over the plan it came from, a wall in the
    wrong place is visible at a glance.

    !! The mm->px mapping is the FROZEN, HASHED registration that
    raster_fidelity.py measures against - `_Drawings/evidence/
    v0_raster_registration.json`, fitted between the PDF's hatched wall faces
    and the raster's own wall lines, with the DXF deliberately not consulted.
    Fitting a fresh transform here would reintroduce exactly the circularity
    CODEX rejected in the old overlay_dxf_on_raster.py: a picture that makes
    the model look right because it was aligned TO the model. If the frozen
    evidence is missing or its raster has changed, this returns None and the
    drawing falls back to a white ground rather than showing an unregistered
    overlay, which would be worse than none.
    """
    if not (os.path.exists(REGISTRATION) and os.path.exists(PLAN_RASTER)):
        return None, 'frozen registration or plan raster not found'
    reg = json.load(io.open(REGISTRATION, encoding='utf-8'))
    sx, ox = reg['sx'], reg['ox']
    sy, oy = reg['sy'], reg['oy']
    src = Image.open(PLAN_RASTER).convert('L')
    # output (X, Y) -> source (u, v), both affine and axis-aligned
    a = sx / S
    c = (x0 - PAD) * sx + ox
    e = -sy / S
    f = (H / S + y0 - PAD) * sy + oy
    warped = src.transform(size, Image.AFFINE, (a, 0.0, c, 0.0, e, f),
                           resample=Image.BICUBIC, fillcolor=255)
    # Pale, so the model reads ON TOP of it rather than competing with it.
    faded = Image.eval(warped, lambda v: int(255 - (255 - v) * 0.30))
    return faded.convert('RGB'), 'mm_per_px %.4f, fit %s' % (
        reg['mm_per_px'], reg.get('fit', '?'))


def main():
    utf8_console()
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
    under, why = plan_underlay((W, H), x0, y0, PAD, S, H)
    if under is not None:
        img.paste(under, (0, 0))
        # the legend column stays white - the plan does not extend under it
        ImageDraw.Draw(img).rectangle([W - LEG, 0, W, H], fill=(255, 255, 255))
        print('  underlay: the developer plan, frozen registration (%s)' % why)
    else:
        print('  underlay: NONE - %s' % why)
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
    # The sidecar belongs to the image it describes, so it follows --out.
    # Rendering to a temporary path must not touch the committed sidecar -
    # which is exactly what the closure gate does to compute the EXPECTED
    # bytes of the delivered PNG.
    v0.write_sidecar(summary, os.path.splitext(args.out)[0] + '.json')
    y += 12
    for line in ('Grey underlay: the developer plan',
                 'itself, placed by the FROZEN',
                 'registration raster_fidelity.py',
                 'measures against — not fitted to',
                 'this DXF. Model on top.',
                 '',
                 'Project dimensions. As-built runs',
                 '1.0–1.9% smaller. DRAFT.'):
        dr.text((lx, y), line, fill=(90, 90, 90), font=f_s)
        y += 18

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    img.save(args.out)
    print('wrote %s %s' % (os.path.relpath(args.out, REPO), img.size))
    return 0


if __name__ == '__main__':
    sys.exit(main())
