# -*- coding: utf-8 -*-
"""The review-facing state of v0, DERIVED - so a drawing cannot state a stale one.

Why this exists
---------------
`render_dxf.py` carried its "Still open" list as hard-coded prose. It went stale
**twice**:

  - round 2: the caption read *"M6b absent … so the лоджия does not close"* while
    the committed DXF drew M6b. I edited the words.
  - round 4: CODEX found the same class again - the caption read *"the лоджия is
    still NOT a closed loop"* and *"9 walls carry an OPEN extent exception"*
    while the geometry closed the loop and the ledger held **10**.

Editing the words was the wrong fix the first time. A caption a person maintains
by hand will drift from the geometry every time the geometry moves, and the owner
reads the caption. His standing instruction is precisely about this: *"I want you
to check yourself and not come back to me showing the same result."* A drawing
that reports last round's verdict is that failure in its purest form.

So nothing here is written by hand. Every figure is computed from the same
canonical data and the same exported DXF the gates read, and
`render_dxf.py` writes what it drew to a sidecar that
`check_dxf_closure.py` then asserts is current. **A stale review drawing now
fails the closure gate.**
"""
from __future__ import print_function

import csv
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(REPO, 'data', 'canonical')
READBACK_PNG = os.path.join(REPO, '_Drawings', 'review',
                            'v0_dxf_readback.png')
SIDECAR = os.path.splitext(READBACK_PNG)[0] + '.json'

# The SECOND delivered image. !! It had no byte check, and it went stale the
# very next day - not by anyone editing it, but because a regenerated copy was
# reverted with `git checkout --` to tidy a working tree. The readback PNG
# survived the same tidy-up because its gate would have caught it. One image
# authenticated and one not is not a policy, it is an oversight.
FIDELITY_PNG = os.path.join(REPO, '_Drawings', 'review',
                            'v0_raster_fidelity.png')

# The лоджия's enclosure walls must reach the glazing axis for the loop to close.
LOGGIA_ENCLOSURE = ('M2', 'M6b')
LOOP_TOL_MM = 5.0


def _rows(name, canon=None):
    p = os.path.join(canon or CANON, name)
    if not os.path.exists(p):
        return []
    with io.open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def loggia_loop(walls, glazing):
    """(closed, worst_gap_mm, per_wall). Geometric, from the drawing's own axis.

    The axis is `loggia_glazing.axis_from/axis_to` as extracted from the vector.
    A wall closes the loop when its near end reaches the axis y at BOTH of its
    faces, so the whole thickness meets the line rather than just a centreline.
    """
    if not glazing:
        return None, None, {}
    ax, ay = glazing['axis_from']
    bx, by = glazing['axis_to']
    if abs(bx - ax) < 1e-6:
        return None, None, {}

    def y_on_axis(x):
        return ay + (by - ay) * (x - ax) / (bx - ax)

    per, worst = {}, 0.0
    by_id = dict((w['id'], w) for w in walls)
    for wid in LOGGIA_ENCLOSURE:
        w = by_id.get(wid)
        if not w:
            per[wid] = None
            worst = max(worst, float('inf'))
            continue
        target = min(y_on_axis(w['x0']), y_on_axis(w['x1']))
        gap = max(0.0, w['y0'] - target)
        per[wid] = float(round(gap, 1))
        worst = max(worst, float(gap))
    if worst == float('inf'):
        return False, None, per
    return bool(worst <= LOOP_TOL_MM), float(round(worst, 1)), per


def summary(walls, glazing, canon=None):
    """Everything the review drawing is allowed to say about outstanding state."""
    ex = _rows('wall_extent_exceptions.csv', canon)
    open_ids = sorted(r['wall_id'] for r in ex
                      if (r.get('status') or '').strip() == 'open')
    placement = _rows('wall_placement_directives.csv', canon)
    quarantined = sorted(r['wall_id'] for r in placement
                         if 'quarantin' in (r.get('status') or ''))
    closed, worst, per = loggia_loop(walls, glazing)
    return {
        'wall_count': int(len(walls)),
        'open_exceptions': len(open_ids),
        'open_exception_ids': open_ids,
        'total_exceptions': len(ex),
        'quarantined': quarantined,
        'loggia_loop_closed': closed,
        'loggia_worst_gap_mm': worst,
        'loggia_per_wall_gap_mm': per,
    }


def caption_lines(s, omitted_openings=()):
    """The "Still open" block, generated. No sentence here is hand-maintained."""
    out = []
    if s['quarantined']:
        out += ['%s PLACED but QUARANTINED —' % ', '.join(s['quarantined']),
                '   thickness unresolved, excluded',
                '   from quantities and IFC']
    if s['loggia_loop_closed'] is False:
        gap = s['loggia_worst_gap_mm']
        out += ['the лоджия is NOT a closed loop:',
                ('   worst gap %.0f mm to the glazing' % gap) if gap is not None
                else '   an enclosure wall is missing',
                '   axis']
    elif s['loggia_loop_closed'] is True:
        out += ['the лоджия loop IS closed —',
                '   M2 and M6b reach the glazing',
                '   axis (worst gap %.0f mm)' % (s['loggia_worst_gap_mm'] or 0)]
    if s['open_exceptions']:
        out += ['%d of %d walls carry an OPEN extent'
                % (s['open_exceptions'], s['total_exceptions']),
                '   exception: drawn length vs',
                '   recorded solid_mm']
    if omitted_openings:
        out += ['%d internal doors OMITTED, not' % len(omitted_openings),
                '   guessed: %s —' % ' '.join(omitted_openings),
                '   their reveals are drawn',
                '   differently in thin walls']
    return out


def write_sidecar(s, path=SIDECAR):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    payload = dict(s)
    payload['what'] = (
        'What _Drawings/review/v0_dxf_readback.png actually says. '
        'check_dxf_closure.py asserts this matches the current geometry and '
        'ledger, so a review drawing that reports a previous round cannot pass '
        'the gate.')
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(payload, indent=1, ensure_ascii=False) + '\n')


def read_sidecar(path=SIDECAR):
    if not os.path.exists(path):
        return None
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.load(f)
    except ValueError:
        return None


COMPARED = ('open_exceptions', 'total_exceptions', 'loggia_loop_closed',
            'wall_count', 'quarantined')


def stale(current, drawn):
    """Which claims the drawing makes that the current state does not support."""
    if drawn is None:
        return ['the review drawing has no sidecar; regenerate it with '
                'tools/layout/render_dxf.py']
    out = []
    for k in COMPARED:
        if drawn.get(k) != current.get(k):
            out.append('%s: the drawing says %r, the current state is %r'
                       % (k, drawn.get(k), current.get(k)))
    return out


def render_matches(repo, dxf, tool='render_dxf.py', image=None,
                   extra_args=()):
    """(expected_sha256, delivered_sha256, why) for a delivered review image.

    !! CODEX round 5, finding 2. The stale-drawing check authenticated the
    SIDECAR and never read the image, so replacing only
    `v0_dxf_readback.png` with the pre-fix artefact from `23ac367` - a real
    byte-for-byte substitution - passed while the gate called the PNG current.
    That is the owner's original failure mode restored: the delivered picture
    from the previous round, with a check saying it is fresh.

    A digest recorded in the sidecar would not fix it either, because the
    sidecar is as editable as the image and a coupled edit updates both. So
    **nothing stored is trusted**: the expected bytes are recomputed by running
    the renderer into a temporary path and comparing. `render_dxf.py` is
    byte-deterministic on a given machine, and its sidecar follows `--out`, so
    the probe cannot disturb the committed pair.

    ⚠️ The one honest caveat: determinism holds for a given font set. On a
    machine that resolves a different font the bytes differ, and this reports a
    mismatch. The remedy is the same as for a genuinely stale image -
    regenerate - and the regenerated PNG then shows up in the diff, which is
    visible rather than silent.
    """
    import hashlib
    import subprocess
    import sys
    import tempfile

    image = image or READBACK_PNG
    if not os.path.exists(image):
        return None, None, ('the review drawing %s does not exist; render it '
                            'with tools/layout/%s'
                            % (os.path.relpath(image, repo), tool))

    def sha(path):
        with io.open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    delivered = sha(image)
    tmp = tempfile.mkdtemp()
    try:
        probe = os.path.join(tmp, 'expected.png')
        r = subprocess.run(
            [sys.executable, os.path.join(repo, 'tools', 'layout', tool),
             '--dxf', dxf, '--out', probe] + list(extra_args),
            cwd=repo, env=dict(os.environ, PYTHONIOENCODING='utf-8'),
            capture_output=True, text=True, errors='replace')
        if r.returncode != 0 or not os.path.exists(probe):
            return None, delivered, ('could not re-render the expected review '
                                     'drawing: %s'
                                     % (r.stderr.strip().splitlines()[-1]
                                        if r.stderr.strip() else 'no output'))
        expected = sha(probe)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    if expected != delivered:
        return expected, delivered, (
            '%s is NOT what the renderer produces now: delivered %s, expected '
            '%s. The delivered image is from another state - regenerate it '
            'with tools/layout/%s'
            % (os.path.relpath(image, repo), delivered[:12],
               expected[:12], tool))
    return expected, delivered, None
