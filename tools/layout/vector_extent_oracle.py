# -*- coding: utf-8 -*-
"""An extent oracle the exporter does not consume: the hatched solids themselves.

Why this exists
---------------
CODEX, `V0_DXF_RASTER_FIDELITY` round 3, finding 2. It copied the gate, its
canonical inputs and the DXF to an isolated fixture, extended MC by 1000 mm
along its run, **and** changed MC in the copied `wall_blocks.csv` from
`clear_mm=3315, solid_mm=3565` to `4315/4565`. **The gate exited 0.** Faces did
not move, the junction stayed filled, nothing overlapped, and the drawn length
agreed with the altered table. The coupled edit even preserves
`build_wall_corners.py`'s arithmetic: `4315 + 250 = 4565`.

The verdict was precise about why that matters, and it is not a demand that a
checker survive arbitrary tampering:

> *the export and its purported extent oracle share the same editable
> measurement, so an ordinary coupled correction can make a wrong extent
> self-consistent.*

That is the defect. `wall_blocks.csv` is a **table someone maintains**; asserting
the drawing against it proves only that two things a person can edit together
agree. So the oracle here is the **drawing**: the hatch-validated wall solids
re-derived from `3Б_3+ МН5_287.pdf` at check time, by the same extraction the
placement uses but from the *immutable input* rather than from any table.

What it can and cannot establish
--------------------------------
It CAN establish that a wall's drawn body lies where a hatched solid actually is,
and is not longer than one. Editing `clear_mm` cannot move a hatched solid in a
PDF, and the PDF's sha256 is asserted, so substituting the drawing is caught.

It CANNOT establish that the *right* wall was named, and it does not try - the
vector supplies position, the raster fit supplies identity, and that split is the
whole design. Nor does it replace the raster comparison C-01 names.

⚠️ **It shares extraction CODE with `place_named_walls.py`** - `collect`,
`merge_faces`, `build_runs`. A bug there fools both. That is a real residual
coupling and it is not the one CODEX found: shared code is reviewable and
versioned, a shared editable measurement is not. Stated here rather than
discovered later.
"""
from __future__ import print_function

import hashlib
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

PDF = os.path.join(REPO, '_Inbox', '_Visual_Drop', '3Б_3+ МН5_287.pdf')

# The drawing this oracle trusts. Asserted, so swapping the PDF for one that
# agrees with a wrong table is caught rather than silently believed.
PDF_SHA256 = 'b95dae5afb1feed73db80ad6afbcf1c786b9d86a686309fc6689567224481949'

# A wall may legitimately be drawn PAST its own hatched solid, because closing an
# L-corner extends the owner onto the other wall's far face. The allowance is
# bounded by the thickest wall in the flat, taken from the drawing's own solids -
# NOT from `wall_corners.csv`, which is another editable table. 1000 mm, the
# mutation CODEX seeded, is far outside it.
CORNER_ALLOWANCE_FLOOR_MM = 60.0     # extraction noise, per the snap floor
FACE_MATCH_MM = 40.0                 # a solid's face band vs the drawn faces


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(HERE, '%s.py' % name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pdf_identity():
    """(ok, actual_sha256). A missing PDF is not an ok."""
    if not os.path.exists(PDF):
        return False, None
    h = hashlib.sha256(io.open(PDF, 'rb').read()).hexdigest()
    return h == PDF_SHA256, h


def vector_solids():
    """Hatch-validated wall solids, straight from the PDF. mm, absolute."""
    ex = _load('extract_v0_walls')
    pnw = _load('place_named_walls')
    parser = ex._load_parser()
    plan = parser.parse(PDF)
    solids = pnw.vector_solids(ex, plan)
    # clip_to_envelope mutates in place and RETURNS THE ENVELOPE, not the solids
    pnw.clip_to_envelope(solids, pnw.loggia_extent(ex, plan))
    return solids


def max_solid_thickness(solids):
    """The thickest hatched solid in the drawing - the corner allowance."""
    t = [s['face_hi_mm'] - s['face_lo_mm'] for s in solids]
    return max(t) if t else 0.0


def check(walls, solids, quarantined=()):
    """Each wall's drawn run against the hatched solid it sits on.

    `walls` are the gate's DXF wall dicts (id/x0/x1/y0/y1/axis). Returns
    (findings, rows) where a row is the per-wall report line.
    """
    allow = max(max_solid_thickness(solids), CORNER_ALLOWANCE_FLOOR_MM)
    findings, rows = [], []
    for w in sorted(walls, key=lambda w: w['id']):
        lo, hi = ((w['y0'], w['y1']) if w['axis'] == 'EW'
                  else (w['x0'], w['x1']))
        a, b = ((w['x0'], w['x1']) if w['axis'] == 'EW'
                else (w['y0'], w['y1']))
        # the solid whose face band this wall sits in, on the same axis,
        # overlapping its run
        best = None
        for s in solids:
            if s['axis'] != w['axis']:
                continue
            d = max(abs(s['face_lo_mm'] - lo), abs(s['face_hi_mm'] - hi))
            if d > FACE_MATCH_MM:
                continue
            ov = min(s['to_mm'], b) - max(s['from_mm'], a)
            if ov <= 0:
                continue
            if best is None or ov > best[1]:
                best = (s, ov, d)
        if best is None:
            if w['id'] in quarantined:
                rows.append((w['id'], None, 0.0, 0.0,
                             'no hatched solid - QUARANTINED, expected'))
                continue
            findings.append({'kind': 'no_vector_solid', 'walls': [w['id']],
                             'detail': 'no hatched solid in the PDF carries '
                                       'this wall at these faces'})
            rows.append((w['id'], None, 0.0, 0.0,
                         'NO hatched solid at these faces'))
            continue
        s, _ov, faced = best
        over_lo = max(0.0, s['from_mm'] - a)      # drawn past the solid's start
        over_hi = max(0.0, b - s['to_mm'])        # drawn past the solid's end
        worst = max(over_lo, over_hi)
        note = 'solid %s %.1f..%.1f' % (s['solid_id'], s['from_mm'], s['to_mm'])
        if worst > allow:
            findings.append({
                'kind': 'extent_beyond_vector', 'walls': [w['id']],
                'detail': 'drawn %.1f..%.1f runs %.1f mm past hatched solid %s '
                          '(%.1f..%.1f); the corner allowance is %.0f mm'
                          % (a, b, worst, s['solid_id'], s['from_mm'],
                             s['to_mm'], allow)})
            note += '  OVER by %.1f mm' % worst
        rows.append((w['id'], s['solid_id'], worst, faced, note))
    return findings, rows
