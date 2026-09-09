# -*- coding: utf-8 -*-
"""Overlay the exported DXF on the developer's raster plan, and MEASURE the fit.

Why
---
Owner, 2026-09-09: *"I want your DXF feedback correspond directly to what we have
in a converted pixel-based image… I want you to create overlay and check the
positioning of walls… I want you to check yourself and not come back to me
showing the same result."*

Fair. This registers the DXF onto the raster and then reports, per wall, how far
its drawn edges sit from ink in the image - so the check is a number, not an
impression, and it can be re-run after every change.

!! On the registration, and rule 9
   `dimension_tolerance.json` records `mm_per_px: 20.6302` for the detailed plan.
   That cannot be right for this file: it is 879 px wide and the flat is about
   10.2 m, which is ~11.6 mm/px. So the scale is DERIVED here from the ink
   bounding box and PRINTED, and an independent residual is reported, rather than
   trusting a recorded constant that does not survive a sanity check. Two
   unknowns per axis, fitted from the flat's own extent.
"""
from __future__ import print_function

import argparse
import os
import sys

import ezdxf
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')
RASTER = os.path.join(REPO, '_Inbox', '_Visual_Drop', 'fllor_plan_detailed.jpeg')
OUT = os.path.join(REPO, '_Drawings', 'review', 'v0_dxf_over_raster.png')

INK = 150            # a pixel darker than this counts as ink
PROBE_MM = 90.0      # how far from a drawn edge we look for ink


def line_positions(im, thresh=INK, min_frac=0.30):
    """Rows and columns that carry a long run of ink - the drawn WALL LINES.

    !! Registering on the ink BOUNDING BOX gave 6.6% anisotropy, because the box
    includes the dimension strings and the room labels printed outside the walls.
    The wall lines themselves are what both representations have in common, so
    the fit uses those: a row or column whose ink covers at least `min_frac` of
    the drawing is a wall line, and their positions are matched against the DXF's
    own face coordinates.
    """
    g = im.convert('L')
    w, h = g.size
    px = g.load()
    rows, cols = [], []
    rowc = [0] * h
    colc = [0] * w
    for y in range(h):
        for x in range(w):
            if px[x, y] < thresh:
                rowc[y] += 1
                colc[x] += 1
    for y in range(h):
        if rowc[y] >= w * min_frac:
            rows.append(y)
    for x in range(w):
        if colc[x] >= h * min_frac:
            cols.append(x)
    return rows, cols


def fit_axis(dxf_faces, px_lines, sign):
    """Best (scale, offset) mapping mm -> px, by RANSAC over pairs.

    `sign` is +1 where pixel and mm axes run the same way and -1 where they are
    opposed (image y grows downward; the drawing's y grows upward).
    """
    best = None
    faces = sorted(set(round(f, 1) for f in dxf_faces))
    lines = sorted(set(px_lines))
    for i, f1 in enumerate(faces):
        for f2 in faces[i + 1:]:
            if f2 - f1 < 2000:
                continue
            for p1 in lines:
                for p2 in lines:
                    if p1 == p2:
                        continue
                    s_ = (p2 - p1) / (f2 - f1)
                    if sign * s_ <= 0 or not 0.05 <= abs(s_) <= 0.20:
                        continue
                    o = p1 - s_ * f1
                    inl, err = 0, 0.0
                    for f in faces:
                        q = s_ * f + o
                        d = min((abs(q - p) for p in lines), default=1e9)
                        if d <= 4.0:
                            inl += 1
                            err += d
                    if best is None or (inl, -err) > (best[0], -best[1]):
                        best = (inl, err, s_, o)
    return best


def ink_bbox(im, thresh=INK, margin_frac=0.02):
    g = im.convert('L')
    w, h = g.size
    px = g.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if px[x, y] < thresh:
                xs.append(x)
                ys.append(y)
    if not xs:
        sys.exit('no ink found in the raster')
    # trim the outer few per cent, which is frame/scan noise
    xs.sort()
    ys.sort()
    n = len(xs)
    k = int(n * margin_frac)
    return xs[k], xs[n - 1 - k], ys[k], ys[n - 1 - k]


def load_walls(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    labels = {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
              for e in msp if e.dxftype() == 'TEXT'
              and e.dxf.layer == 'V0-WALL-LABEL'}
    walls = []
    for e in msp:
        if e.dxftype() != 'LWPOLYLINE' or not e.dxf.layer.startswith('V0-WALL'):
            continue
        p = [(q[0], q[1]) for q in e.get_points()]
        x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
        y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        name = min(labels.items(),
                   key=lambda kv: (kv[1][0] - cx) ** 2 + (kv[1][1] - cy) ** 2)[0] \
            if labels else '?'
        walls.append({'id': name, 'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1,
                      'layer': e.dxf.layer,
                      'axis': 'EW' if (x1 - x0) > (y1 - y0) else 'NS'})
    return walls, msp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--raster', default=RASTER)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--zoom', type=float, default=2.0)
    args = ap.parse_args()

    im = Image.open(args.raster).convert('RGB')
    walls, msp = load_walls(args.dxf)
    if not walls:
        sys.exit('no walls in the DXF')

    rows, cols = line_positions(im)
    xfaces = [v for w in walls for v in (w['x0'], w['x1'])]
    yfaces = [v for w in walls for v in (w['y0'], w['y1'])]
    fx = fit_axis(xfaces, cols, +1)
    fy = fit_axis(yfaces, rows, -1)
    if not fx or not fy:
        sys.exit('could not register: %s / %s' % (bool(fx), bool(fy)))
    print('raster %s  %dx%d px' % (os.path.basename(args.raster), *im.size))
    print('wall lines found: %d rows, %d cols' % (len(rows), len(cols)))
    print('x: %d/%d faces land on a drawn line   %.5f px/mm (%.2f mm/px)'
          % (fx[0], len(set(round(v, 1) for v in xfaces)), fx[2], 1 / abs(fx[2])))
    print('y: %d/%d faces land on a drawn line   %.5f px/mm (%.2f mm/px)'
          % (fy[0], len(set(round(v, 1) for v in yfaces)), fy[2], 1 / abs(fy[2])))
    aniso = abs(abs(fx[2]) - abs(fy[2])) / max(abs(fx[2]), abs(fy[2])) * 100
    print('anisotropy %.2f%%' % aniso)
    if aniso > 4.0:
        print('  !! over 4%% - the registration is not trustworthy, so the '
              'per-wall verdicts below are not either')

    Z = args.zoom
    sx = abs(fx[2]) * Z

    # !! P() must return coordinates in the ZOOMED canvas, because that is what
    # both the drawing and the ink probe use. Returning unzoomed pixels while
    # probing a 2x canvas silently compared two different spaces.
    def P(x, y):
        return ((fx[2] * x + fx[3]) * Z, (fy[2] * y + fy[3]) * Z)

    canvas = im.resize((int(im.width * Z), int(im.height * Z)), Image.LANCZOS)
    dr = ImageDraw.Draw(canvas, 'RGBA')
    grey = canvas.convert('L').load()

    COLOUR = {'V0-WALL-CONCRETE': (215, 30, 30), 'V0-WALL-AERATED': (20, 150, 50),
              'V0-WALL-EXTERNAL': (200, 40, 180), 'V0-WALL-LOGGIA': (200, 40, 180)}

    def ink_distance_mm(xmm, ymm, limit_mm=400.0):
        """Distance in MILLIMETRES from this point to the nearest ink.

        !! A hit/miss probe was useless. At ~13 mm/px a 90 mm radius is 7 px, and
        on a drawing this dense almost every point has ink within 7 px - 23 of 24
        walls "passed" while the overlay plainly showed them off the walls. A
        distance is actionable; a boolean at a generous radius is flattery.
        """
        cx, cy = P(xmm, ymm)
        lim = max(2, int(limit_mm * sx))
        best = None
        for r in range(0, lim + 1):
            for dy in range(-r, r + 1):
                for dx in (-r, r) if abs(dy) != r else range(-r, r + 1):
                    x, y = int(cx + dx), int(cy + dy)
                    if 0 <= x < canvas.width and 0 <= y < canvas.height                             and grey[x, y] < INK:
                        best = r
                        break
                if best is not None:
                    break
            if best is not None:
                break
        return (best / sx) if best is not None else limit_mm

    print()
    print('%-5s %-4s %-9s %-9s %s'
          % ('wall', 'axis', 'worst mm', 'mean mm', 'distance from each sampled edge to ink'))
    misfit = []
    for w in sorted(walls, key=lambda w: w['id']):
        a, b = P(w['x0'], w['y1']), P(w['x1'], w['y0'])
        dr.rectangle([min(a[0], b[0]), min(a[1], b[1]),
                      max(a[0], b[0]), max(a[1], b[1])],
                     outline=COLOUR.get(w['layer'], (120, 120, 120)) + (255,),
                     width=max(1, int(Z)))
        if w['axis'] == 'EW':
            mid = (w['x0'] + w['x1']) / 2
            probes = [(mid, w['y0']), (mid, w['y1']),
                      (w['x0'], (w['y0'] + w['y1']) / 2),
                      (w['x1'], (w['y0'] + w['y1']) / 2)]
        else:
            mid = (w['y0'] + w['y1']) / 2
            probes = [(w['x0'], mid), (w['x1'], mid),
                      ((w['x0'] + w['x1']) / 2, w['y0']),
                      ((w['x0'] + w['x1']) / 2, w['y1'])]
        ds = [ink_distance_mm(xm, ym) for xm, ym in probes]
        worst, mean = max(ds), sum(ds) / len(ds)
        print('%-5s %-4s %9.0f %9.0f   %s'
              % (w['id'], w['axis'], worst, mean,
                 ' '.join('%.0f' % d for d in ds)))
        if worst > 60.0:
            misfit.append((w['id'], worst, mean))

    print()
    if misfit:
        print('walls whose worst sampled edge is more than 60 mm from ink '
              '(60 mm is about 5 px here):')
        for wid, worst, mean in sorted(misfit, key=lambda t: -t[1]):
            print('  %-5s worst %5.0f mm   mean %5.0f mm' % (wid, worst, mean))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    canvas.save(args.out)
    print('\nwrote %s %s' % (os.path.relpath(args.out, REPO), canvas.size))
    return 0


if __name__ == '__main__':
    sys.exit(main())
