# -*- coding: utf-8 -*-
"""The raster half of C-01: dense, symmetric, and registered independently.

What was wrong with the old overlay
-----------------------------------
CODEX, `V0_DXF_RASTER_FIDELITY` rounds 1 and 3, and every objection stands:

  1. it fitted the registration **from wall faces belonging to the DXF under
     test**, then scored those same faces - so displacing the model dragged the
     reference with it;
  2. it sampled **four points per wall**;
  3. it measured one direction only, so a **missing** wall was invisible;
  4. it re-thresholded the raster every run, so the evidence could move;
  5. it called the result advisory.

This tool fixes 1-4. (5 stays partly true and is stated at the bottom.)

The three things that make it independent
-----------------------------------------
**Registration comes from the PDF, not the DXF.** The vector plan gives exact mm
for its hatched wall solids, and the raster is a render of the same drawing. So
mm→px is fitted between *PDF* solid faces and raster wall lines. The DXF is never
consulted while registering, which is the circularity CODEX named.

**The evidence is frozen.** The ink mask is built once by a recorded threshold,
committed as `_Drawings/evidence/v0_wall_ink_mask.png`, and its sha256 asserted
here. A run compares against that committed artefact; it does not re-derive it.
`--rebuild-mask` regenerates it and prints the new hash, deliberately as a
separate, visible act.

**Both directions are measured, densely.** Every sample along every DXF wall edge
is scored against the ink, *and* every wall ink pixel is scored against the DXF
wall BODIES. The second direction is the one that can see a wall that is not
there - and it is measured per hatched solid, because globally a single missing
wall is 0.167 against a 0.103 baseline and a 400 mm endpoint drift is 0.108,
which no global threshold can separate from noise.

Why edges and not area IoU
--------------------------
CODEX recommended area overlap, and I measured the raster before implementing it:
this drawing renders walls as **outlines with hatching**, not as filled bands -
horizontal dark runs are 1-3 px for 27+30+21% of all runs, while a 250 mm wall
would be ~21 px. So a filled DXF rectangle has no area counterpart in the raster,
and an IoU between them would be a number about the *rendering convention*, not
about fidelity. Dense symmetric **edge** distance compares line work with line
work, which is the same evidence on both sides. CODEX's reason for wanting the
dense boundary measure *alongside* area - that a thick nearby ink band can hide
edge displacement - is exactly why the second direction is included.

Usage
-----
    py -3 tools/layout/raster_fidelity.py
    py -3 tools/layout/raster_fidelity.py --rebuild-mask
    py -3 tools/layout/raster_fidelity.py --dxf <copy>      # for the selftest

Exit 0 pass, 1 a measured breach, 2 registration unusable.
"""
from __future__ import print_function

import argparse
import hashlib
import importlib.util
import io
import json
import os
import sys

import numpy as np
from PIL import Image

import ezdxf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

RASTER = os.path.join(REPO, '_Inbox', '_Visual_Drop', 'fllor_plan_detailed.jpeg')
MASK = os.path.join(REPO, '_Drawings', 'evidence', 'v0_wall_ink_mask.png')
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')

INK = 160              # grey level below which a pixel is ink; measured, not guessed
MIN_LINE_FRAC = 0.30   # a row/col carrying this much ink is a drawn wall line
WALL_LAYERS_PREFIX = 'V0-WALL'

# The frozen evidence. Empty until the first --rebuild-mask; once set, a run
# refuses to measure against a mask that is not this one.
MASK_SHA256 = '6ebc7feaf6505767daa7288e3df2ca039f11d6e3538b4bd8e88a168aefa552a3'

# Thresholds. These are the ones that decide the exit code, so they are stated
# here and not buried: they come from the round-1 measurement that 19 of 24
# walls sat within 60 mm, plus the +30/-45 mm build tolerance.
MAX_P90_MM = 60.0      # per wall, 90th percentile edge-to-ink distance
MAX_MEAN_MM = 45.0     # per wall, mean
# Global unexplained wall ink. The accepted export measures 0.103, so 0.15
# leaves headroom for noise while a whole missing wall (G5 deleted -> 0.167)
# still trips it. An ABSOLUTE statement, independent of any baseline.
MAX_UNEXPLAINED_FRAC = 0.15

# Per-solid deviation from the frozen baseline. This is what actually has the
# resolution: a single deleted wall moves its own solid by +0.49 and a 400 mm
# endpoint drift by +0.036, while every unaffected solid moves 0.000 - whereas
# globally those are 0.167 and 0.108 against a 0.103 base, so the drift is
# invisible in the global figure.
#
# !! It is a REGRESSION test and must not be read as more: the baseline is
# measured from the accepted export, so it detects any deviation from the
# reviewed state and does NOT certify that state. The non-circular claims here
# are direction 1's millimetre distances and the global fraction above.
MAX_SOLID_DEVIATION = 0.02
MIN_SOLID_INK_PX = 200        # below this a solid's fraction is noise


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(HERE, '%s.py' % name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# --------------------------------------------------------------- the mask ----
def build_mask():
    """The frozen ink mask: a recorded threshold, and nothing adaptive."""
    a = np.asarray(Image.open(RASTER).convert('L'))
    return (a < INK)


def mask_sha256(path):
    return hashlib.sha256(io.open(path, 'rb').read()).hexdigest()


def save_mask(m, path):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    Image.fromarray((~m).astype(np.uint8) * 255).save(path)


def load_mask(path):
    return np.asarray(Image.open(path).convert('L')) < 128


# ------------------------------------------------- distance transform --------
def chamfer(mask):
    """Approximate Euclidean distance, in pixels, to the nearest True cell.

    Two-pass 3x4 chamfer. scipy is not installed in either venv here, so this is
    written out rather than imported. It is an APPROXIMATION - worst-case a few
    percent above the true Euclidean distance - which is stated because the
    numbers it produces are compared against a millimetre threshold.
    """
    BIG = 1e9
    d = np.where(mask, 0.0, BIG)
    h, w = d.shape
    D1, D2 = 1.0, 1.41421356

    def shift_right(a):
        out = np.full_like(a, BIG)
        out[1:] = a[:-1]
        return out

    def shift_left(a):
        out = np.full_like(a, BIG)
        out[:-1] = a[1:]
        return out

    def sweep_row(row, prev, forward):
        """One causal pass over a row, vectorised except the in-row recursion."""
        if prev is not None:
            row = np.minimum(row, prev + D1)
            row = np.minimum(row, shift_right(prev) + D2)
            row = np.minimum(row, shift_left(prev) + D2)
        # the along-row dependency is inherently sequential; np.minimum.accumulate
        # on (value - index) turns it into a running minimum
        idx = np.arange(w, dtype=np.float64)
        if forward:
            acc = np.minimum.accumulate(row - idx)
            row = np.minimum(row, acc + idx)
        else:
            acc = np.minimum.accumulate((row + idx)[::-1])[::-1]
            row = np.minimum(row, acc - idx)
        return row

    for y in range(h):
        d[y] = sweep_row(d[y], d[y - 1] if y > 0 else None, True)
    for y in range(h - 1, -1, -1):
        d[y] = sweep_row(d[y], d[y + 1] if y + 1 < h else None, False)
    return d


# ------------------------------------------------------- registration --------
def raster_lines(mask):
    """Rows and columns carrying a long run of ink - the drawn wall lines."""
    h, w = mask.shape
    rowc = mask.sum(axis=1)
    colc = mask.sum(axis=0)
    rows = [int(y) for y in np.where(rowc >= w * MIN_LINE_FRAC)[0]]
    cols = [int(x) for x in np.where(colc >= h * MIN_LINE_FRAC)[0]]
    return rows, cols


def wall_like_ink(mask, solids, P, mm_per_px):
    """Ink the DRAWING itself says is wall: ink inside a hatched solid.

    !! Two wrong versions preceded this, and a diagnostic render settled it
    rather than argument. First I took whole qualifying ROWS, which swept in
    every glyph sharing a y with a wall - 37.6% "unexplained". Then I required a
    long contiguous run, which still admitted the **dimension extension lines
    and the dashed centre lines**: they are long, straight, axis-aligned and
    inside the flat, so no run-length rule can separate them from wall line
    work. 34% "unexplained", and the render showed nearly all of it was
    annotation, not missing walls.

    The discriminator has to come from something that knows where walls ARE, and
    the PDF's hatched solids do - independently of the DXF, which is the whole
    point of this direction. So wall ink is ink lying inside a hatched solid's
    footprint. Annotation is excluded because it is not inside one, and a wall
    the DXF omits still has its solid full of ink with no DXF edge near it,
    which is the defect this direction exists to catch.
    """
    h, w = mask.shape
    inside = np.zeros_like(mask)
    pad = max(1, int(round(30.0 / max(mm_per_px, 1e-6))))
    for s in solids:
        if s['axis'] == 'EW':
            xa, xb, ya, yb = (s['from_mm'], s['to_mm'],
                              s['face_lo_mm'], s['face_hi_mm'])
        else:
            xa, xb, ya, yb = (s['face_lo_mm'], s['face_hi_mm'],
                              s['from_mm'], s['to_mm'])
        (px0, py0), (px1, py1) = P(xa, ya), P(xb, yb)
        i0, i1 = sorted((int(round(px0)), int(round(px1))))
        j0, j1 = sorted((int(round(py0)), int(round(py1))))
        i0, i1 = max(0, i0 - pad), min(w - 1, i1 + pad)
        j0, j1 = max(0, j0 - pad), min(h - 1, j1 + pad)
        if i1 >= i0 and j1 >= j0:
            inside[j0:j1 + 1, i0:i1 + 1] = True
    return mask & inside


REGISTRATION = os.path.join(REPO, '_Drawings', 'evidence',
                            'v0_raster_registration.json')


def cached_registration(pdf_hash, mask_hash):
    """The frozen mm->px fit, keyed by BOTH pieces of evidence it came from.

    The registration depends only on the PDF and the mask, and both are frozen
    by hash - so recomputing it every run is not just slow (the RANSAC is
    O(faces^2 x lines^2), tens of seconds), it also leaves the fit invisible.
    Committing it makes the number auditable: a reviewer can read what this
    check believes the scale is, instead of inferring it from a log line.

    !! It is keyed by both hashes so it can never be stale in a way that
    matters, and it is written only by `--refit`, never as a silent side effect.
    """
    if not os.path.exists(REGISTRATION):
        return None
    try:
        with io.open(REGISTRATION, encoding='utf-8') as f:
            d = json.load(f)
    except ValueError:
        return None
    if d.get('pdf_sha256') != pdf_hash or d.get('mask_sha256') != mask_hash:
        return None
    return d


def save_registration(pdf_hash, mask_hash, sx, ox, sy, oy, solids, meta,
                      baseline=None):
    d = os.path.dirname(REGISTRATION)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    payload = {
        'what': ('The frozen mm->px registration for tools/layout/'
                 'raster_fidelity.py, fitted between the PDF\'s hatched wall '
                 'solid faces and the raster\'s wall lines. The DXF under test '
                 'is NOT consulted - that circularity is what CODEX rejected in '
                 'the previous overlay.'),
        'pdf_sha256': pdf_hash,
        'mask_sha256': mask_hash,
        'sx': sx, 'ox': ox, 'sy': sy, 'oy': oy,
        'mm_per_px': 2.0 / (abs(sx) + abs(sy)),
        'fit': meta,
        'solids': [{k: s[k] for k in ('solid_id', 'axis', 'face_lo_mm',
                                      'face_hi_mm', 'from_mm', 'to_mm')}
                   | ({'bridged_openings_mm': s['bridged_openings_mm']}
                      if s.get('bridged_openings_mm') else {})
                   for s in solids],
    }
    if baseline is not None:
        payload['solid_unexplained_baseline'] = baseline
    elif os.path.exists(REGISTRATION):
        try:
            with io.open(REGISTRATION, encoding='utf-8') as f:
                old = json.load(f)
            if old.get('solid_unexplained_baseline'):
                payload['solid_unexplained_baseline'] =                     old['solid_unexplained_baseline']
        except ValueError:
            pass
    with io.open(REGISTRATION, 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, indent=1, ensure_ascii=False))


def pdf_faces():
    """Wall-solid face coordinates in mm, from the PDF. Never from the DXF."""
    oracle = _load('vector_extent_oracle')
    ok, got = oracle.pdf_identity()
    solids = oracle.vector_solids()
    xs, ys = set(), set()
    for s in solids:
        tgt = xs if s['axis'] == 'NS' else ys
        tgt.add(round(s['face_lo_mm'], 1))
        tgt.add(round(s['face_hi_mm'], 1))
    return sorted(xs), sorted(ys), (ok, got), solids


def fit_axis(faces_mm, px_lines, sign):
    """(inliers, err, scale, offset) mapping mm -> px, by RANSAC over pairs.

    !! The tolerance and the span floor both matter. A loose fit at HALF the true
    scale scored 15 of 15 inliers once, because every other face happens to land
    on a line - which is why pairs must span at least 2 m and the residual
    tolerance is 4 px, and why the caller cross-checks that the two axes agree
    on scale.
    """
    best = None
    faces = sorted(set(faces_mm))
    lines = sorted(set(px_lines))
    for i, f1 in enumerate(faces):
        for f2 in faces[i + 1:]:
            if f2 - f1 < 2000:
                continue
            for p1 in lines:
                for p2 in lines:
                    if p1 == p2:
                        continue
                    s_ = (p2 - p1) / float(f2 - f1)
                    if sign * s_ <= 0 or not 0.05 <= abs(s_) <= 0.20:
                        continue
                    o = p1 - s_ * f1
                    inl, err = 0, 0.0
                    for f in faces:
                        q = s_ * f + o
                        dd = min((abs(q - p) for p in lines), default=1e9)
                        if dd <= 4.0:
                            inl += 1
                            err += dd
                    if best is None or (inl, -err) > (best[0], -best[1]):
                        best = (inl, err, s_, o)
    return best


# --------------------------------------------------------------- the DXF -----
def dxf_walls(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    labels = {e.dxf.text: (e.dxf.insert.x, e.dxf.insert.y)
              for e in msp if e.dxftype() == 'TEXT'
              and e.dxf.layer == 'V0-WALL-LABEL'}
    out = []
    for e in msp:
        if (e.dxftype() != 'LWPOLYLINE'
                or not e.dxf.layer.startswith(WALL_LAYERS_PREFIX)):
            continue
        p = [(q[0], q[1]) for q in e.get_points()]
        x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
        y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        name = (min(labels.items(),
                    key=lambda kv: (kv[1][0] - cx) ** 2 + (kv[1][1] - cy) ** 2)[0]
                if labels else '?')
        out.append({'id': name, 'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1})
    return out


def solid_for(w, solids, face_tol=40.0):
    """The hatched solid a wall sits on, matched on axis and face band."""
    axis = 'EW' if (w['x1'] - w['x0']) > (w['y1'] - w['y0']) else 'NS'
    lo, hi = ((w['y0'], w['y1']) if axis == 'EW' else (w['x0'], w['x1']))
    a, b = ((w['x0'], w['x1']) if axis == 'EW' else (w['y0'], w['y1']))
    best = None
    for s in solids:
        if s['axis'] != axis:
            continue
        if max(abs(s['face_lo_mm'] - lo), abs(s['face_hi_mm'] - hi)) > face_tol:
            continue
        ov = min(s['to_mm'], b) - max(s['from_mm'], a)
        if ov <= 0:
            continue
        if best is None or ov > best[1]:
            best = (s, ov)
    return best[0] if best else None


def openings_of(w, solids):
    """Along-axis intervals where the DRAWING has no face line: the doorways.

    !! This is the difference between a metric and a number. Without it G2 and
    G4C were the only two walls to "breach" - G2 p90 139.7 mm, G4C p90 187.1 mm -
    and both breaches were doorways. G2 sits on solid S14, whose own
    `bridged_openings_mm` records the 1010 mm entrance door at 5146.0..6155.9,
    and G2 spans 4645.9..6866.5: **45% of its length is an opening with no drawn
    face line to be near.** G4C sits on S21 with two 710 mm openings, also 45%
    of its run. Scoring a wall's face against ink where the drawing deliberately
    draws none measures the opening, not the wall.

    The intervals come from the PDF's own merge record, so this is the drawing
    correcting the metric, not a threshold being relaxed to fit.
    """
    s = solid_for(w, solids)
    if not s:
        return []
    return [tuple(iv) for iv in (s.get('bridged_openings_mm') or [])]


def edge_pixels(w, P, step_mm=25.0, openings=()):
    """Dense samples along a wall rectangle's four edges, as (px, py) floats.

    Samples inside a recorded opening are dropped - see `openings_of`.
    """
    axis = 'EW' if (w['x1'] - w['x0']) > (w['y1'] - w['y0']) else 'NS'

    def in_opening(x, y):
        v = x if axis == 'EW' else y
        return any(a <= v <= b for a, b in openings)

    pts = []
    for (ax, ay), (bx, by) in ((( w['x0'], w['y0']), (w['x1'], w['y0'])),
                               ((w['x1'], w['y0']), (w['x1'], w['y1'])),
                               ((w['x1'], w['y1']), (w['x0'], w['y1'])),
                               ((w['x0'], w['y1']), (w['x0'], w['y0']))):
        L = max(abs(bx - ax), abs(by - ay))
        n = max(2, int(L / step_mm) + 1)
        for k in range(n):
            t = k / float(n - 1)
            mx, my = ax + (bx - ax) * t, ay + (by - ay) * t
            if in_opening(mx, my):
                continue
            pts.append(P(mx, my))
    return pts


def per_solid_unexplained(wall_ink, dist_mm, solids, P, limit_mm):
    """Unexplained wall-ink fraction per hatched solid, for the regression test."""
    h, w = wall_ink.shape
    far = wall_ink & (dist_mm > limit_mm)
    out = {}
    for sd in solids:
        if sd['axis'] == 'EW':
            xa, xb, ya, yb = (sd['from_mm'], sd['to_mm'],
                              sd['face_lo_mm'], sd['face_hi_mm'])
        else:
            xa, xb, ya, yb = (sd['face_lo_mm'], sd['face_hi_mm'],
                              sd['from_mm'], sd['to_mm'])
        (p0, q0), (p1, q1) = P(xa, ya), P(xb, yb)
        i0, i1 = sorted((int(p0), int(p1)))
        j0, j1 = sorted((int(q0), int(q1)))
        sl = (slice(max(0, j0), min(h, j1 + 1)),
              slice(max(0, i0), min(w, i1 + 1)))
        tot = int(wall_ink[sl].sum())
        if tot < MIN_SOLID_INK_PX:
            continue
        out[sd['solid_id']] = (int(far[sl].sum()) / float(tot), tot)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--mask', default=MASK)
    ap.add_argument('--rebuild-mask', action='store_true')
    ap.add_argument('--refit', action='store_true',
                    help='re-fit the registration and commit it')
    ap.add_argument('--out', default=os.path.join(
        REPO, '_Drawings', 'review', 'v0_raster_fidelity.png'))
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--allow-unfrozen-mask', action='store_true',
                    help='measure against a mask whose hash is not the frozen '
                         'one; for building the freeze, not for a gate run')
    args = ap.parse_args()

    if args.rebuild_mask:
        m = build_mask()
        save_mask(m, args.mask)
        h = mask_sha256(args.mask)
        print('wrote %s  %d x %d, ink %.3f%%'
              % (os.path.relpath(args.mask, REPO), m.shape[1], m.shape[0],
                 100 * m.mean()))
        print('sha256 %s' % h)
        print('\nset MASK_SHA256 in this file to that hash to freeze it')
        return 0

    if not os.path.exists(args.mask):
        print('no frozen mask at %s; run --rebuild-mask first'
              % os.path.relpath(args.mask, REPO))
        return 2
    got = mask_sha256(args.mask)
    frozen_ok = (MASK_SHA256 and got == MASK_SHA256)
    if not frozen_ok and not args.allow_unfrozen_mask:
        print('the mask is not the frozen evidence:\n  expected %s\n  got      %s'
              % (MASK_SHA256 or '(unset)', got))
        return 2
    mask = load_mask(args.mask)
    print('frozen mask %s  %d x %d  ink %.3f%%  sha256 %s'
          % (os.path.relpath(args.mask, REPO), mask.shape[1], mask.shape[0],
             100 * mask.mean(), got[:16]))

    # --- register from the PDF, never from the DXF -----------------------
    oracle = _load('vector_extent_oracle')
    pdf_ok, pdf_hash = oracle.pdf_identity()
    if not pdf_ok:
        print('the source PDF is not the one the oracle trusts: %s' % pdf_hash)
        return 2
    cached = None if args.refit else cached_registration(pdf_hash, got)
    if cached:
        sx, ox, sy, oy = (cached['sx'], cached['ox'], cached['sy'],
                          cached['oy'])
        solids = cached['solids']
        aniso = abs(abs(sx) - abs(sy)) / max(abs(sx), abs(sy))
        print('registration: FROZEN, %s  (--refit to redo)'
              % os.path.relpath(REGISTRATION, REPO))
        print('  mm->px  sx %.5f  sy %.5f  anisotropy %.2f%%  %s'
              % (sx, sy, 100 * aniso, cached.get('fit', '')))
    else:
        xs_mm, ys_mm, _ident, solids = pdf_faces()
        rows, cols = raster_lines(mask)
        fx = fit_axis(xs_mm, cols, +1)
        fy = fit_axis(ys_mm, rows, -1)
        if not fx or not fy:
            print('could not register from the PDF: x=%s y=%s'
                  % (bool(fx), bool(fy)))
            return 2
        sx, ox = fx[2], fx[3]
        sy, oy = fy[2], fy[3]
        aniso = abs(abs(sx) - abs(sy)) / max(abs(sx), abs(sy))
        meta = ('%d PDF x-faces / %d y-faces against %d cols / %d rows; '
                'inliers %d / %d' % (len(xs_mm), len(ys_mm), len(cols),
                                     len(rows), fx[0], fy[0]))
        print('registration: FITTED - %s' % meta)
        print('  mm->px  sx %.5f  sy %.5f  anisotropy %.2f%%'
              % (sx, sy, 100 * aniso))
        if args.refit:
            save_registration(pdf_hash, got, sx, ox, sy, oy, solids, meta)
            print('  wrote %s' % os.path.relpath(REGISTRATION, REPO))
    if aniso > 0.05:
        print('  anisotropy above 5%% - the fit is unusable')
        return 2
    mm_per_px = 2.0 / (abs(sx) + abs(sy))

    def P(x, y):
        return (sx * x + ox, sy * y + oy)

    # --- direction 1: every DXF wall edge -> nearest ink -----------------
    print('\ndirection 1: DXF wall edges -> ink (dense, %s mm steps)' % 25)
    dist_to_ink = chamfer(mask)
    h, w = mask.shape
    walls = dxf_walls(args.dxf)
    findings, per_wall = [], []
    for wl in sorted(walls, key=lambda v: v['id']):
        ds = []
        ops = openings_of(wl, solids)
        for px, py in edge_pixels(wl, P, openings=ops):
            ix, iy = int(round(px)), int(round(py))
            if 0 <= iy < h and 0 <= ix < w:
                ds.append(dist_to_ink[iy, ix] * mm_per_px)
        if not ds:
            continue
        ds.sort()
        mean = sum(ds) / len(ds)
        p90 = ds[int(0.9 * (len(ds) - 1))]
        per_wall.append((wl['id'], len(ds), mean, p90, ds[-1], len(ops)))
    for wid, n, mean, p90, mx, nops in sorted(per_wall, key=lambda t: -t[3]):
        flag = ''
        if p90 > MAX_P90_MM or mean > MAX_MEAN_MM:
            flag = '  BREACH'
            findings.append({'kind': 'edge_far_from_ink', 'walls': [wid],
                             'detail': 'mean %.0f mm, p90 %.0f mm over %d '
                                       'samples' % (mean, p90, n)})
        print('  %-5s n=%-4d mean %6.1f  p90 %6.1f  max %6.1f mm  %s%s'
              % (wid, n, mean, p90, mx,
                 ('%d opening(s) skipped' % nops) if nops else '', flag))

    # --- direction 2: wall ink -> nearest DXF wall BODY (missing-wall mass) -------------
    # !! This is the direction the four-probe version could not have: it is the
    # one that sees a wall the DXF does NOT draw. Only ink on a long straight
    # run is considered, so text and dimension strings do not count as walls.
    print('\ndirection 2: wall ink -> nearest DXF wall BODY (missing-wall mass)')
    # !! Measured against wall EDGES first, and a diagnostic render showed the
    # error: nearly all the "unexplained" ink was the 45/50-degree HATCHING
    # inside the wall bands, which sits up to 150 mm from either face of a
    # 300 mm wall and is therefore legitimately far from any edge. Wall ink
    # belongs against the wall BODY. That also makes this direction the
    # missing-wall-mass measure CODEX asked for: it is the recall of inked wall
    # region by DXF wall bodies.
    body_mask = np.zeros_like(mask)
    for wl in walls:
        (px0, py0), (px1, py1) = (P(wl['x0'], wl['y0']), P(wl['x1'], wl['y1']))
        i0, i1 = sorted((int(round(px0)), int(round(px1))))
        j0, j1 = sorted((int(round(py0)), int(round(py1))))
        i0, i1 = max(0, i0), min(w - 1, i1)
        j0, j1 = max(0, j0), min(h - 1, j1)
        if i1 >= i0 and j1 >= j0:
            body_mask[j0:j1 + 1, i0:i1 + 1] = True
    dist_to_edge = chamfer(body_mask)
    wall_ink = wall_like_ink(mask, solids, P, mm_per_px)
    n_ink = int(wall_ink.sum())
    if n_ink:
        far = dist_to_edge[wall_ink] * mm_per_px
        unexplained = float((far > MAX_P90_MM).mean())
        print('  %d wall ink pixels inside a hatched solid; %.1f%% lie more '
              'than %.0f mm from any DXF wall body'
              % (n_ink, 100 * unexplained, MAX_P90_MM))
        print('  mean %.1f mm, p90 %.1f mm'
              % (far.mean(), float(np.percentile(far, 90))))
        # --- per-solid regression against the frozen baseline ------------
        per = per_solid_unexplained(wall_ink, dist_to_edge * mm_per_px,
                                    solids, P, MAX_P90_MM)
        base = (cached or {}).get('solid_unexplained_baseline') or {}
        if args.refit:
            save_registration(pdf_hash, got, sx, ox, sy, oy, solids,
                              locals().get('meta', 'refit'),
                              dict((k, round(v[0], 4)) for k, v in per.items()))
            print('  wrote the per-solid baseline into %s'
                  % os.path.relpath(REGISTRATION, REPO))
        elif base:
            drifted = []
            for sid, (fr, n) in sorted(per.items()):
                b = base.get(sid)
                if b is None:
                    continue
                if fr - b > MAX_SOLID_DEVIATION:
                    drifted.append((sid, b, fr, n))
            for sid, b, fr, n in sorted(drifted, key=lambda t: t[1] - t[2]):
                findings.append({
                    'kind': 'solid_ink_unexplained', 'walls': [],
                    'detail': 'solid %s: %.3f of its wall ink unexplained '
                              'against a frozen baseline of %.3f (n=%d)'
                              % (sid, fr, b, n)})
                print('  BREACH solid %-4s unexplained %.3f vs baseline %.3f '
                      '(n=%d) - wall mass the DXF stopped covering'
                      % (sid, fr, b, n))
            if not drifted:
                print('  ok   %d solids within %.2f of the frozen per-solid '
                      'baseline' % (len(per), MAX_SOLID_DEVIATION))
        else:
            print('  !!   no frozen per-solid baseline; run --refit. Without it '
                  'a single missing wall is only %.3f of the global figure'
                  % 0.064)

        if unexplained > MAX_UNEXPLAINED_FRAC:
            findings.append({
                'kind': 'ink_without_wall', 'walls': [],
                'detail': '%.1f%% of wall ink lies more than %.0f mm from any '
                          'DXF wall body (limit %.0f%%)'
                          % (100 * unexplained, MAX_P90_MM,
                             100 * MAX_UNEXPLAINED_FRAC)})
            print('  BREACH: the drawing shows wall line the DXF does not')

    # --- the picture, so a person can check the numbers -----------------
    if args.out:
        rgb = np.zeros(mask.shape + (3,), np.uint8)
        rgb[...] = 255
        rgb[mask] = (205, 205, 205)
        rgb[wall_ink] = (0, 150, 0)
        for wl in walls:
            ops = openings_of(wl, solids)
            bad = any(f['walls'] == [wl['id']] for f in findings)
            col = (220, 0, 0) if bad else (0, 90, 220)
            for px, py in edge_pixels(wl, P, step_mm=4.0, openings=ops):
                ix, iy = int(round(px)), int(round(py))
                if 0 <= iy < h and 0 <= ix < w:
                    rgb[iy, ix] = col
        d = os.path.dirname(args.out)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        Image.fromarray(rgb).resize((w * 2, h * 2), Image.NEAREST).save(args.out)
        print('\nwrote %s   grey = all ink, green = wall ink inside a hatched '
              'solid, blue = DXF wall edges actually scored (opening spans '
              'excluded), red = a breaching wall'
              % os.path.relpath(args.out, REPO))

    if args.json:
        print(json.dumps({'findings': findings,
                          'mm_per_px': mm_per_px,
                          'anisotropy': aniso}, indent=1))

    print()
    if findings:
        print('FAIL - %d finding(s): %s'
              % (len(findings),
                 ', '.join(sorted(set(f['kind'] for f in findings)))))
        return 1
    print('PASS - every wall edge is within %.0f mm of ink (p90), and the '
          'drawing shows no wall line the DXF omits'
          % MAX_P90_MM)
    return 0


if __name__ == '__main__':
    sys.exit(main())
