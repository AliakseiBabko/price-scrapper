# -*- coding: utf-8 -*-
"""GATE: every junction in the exported DXF is closed, and nothing overlaps.

Why this and not the raster overlay
-----------------------------------
Owner, 2026-09-09: *"I want clear joints. I don't want cavities in the angles
when two walls meet, or gaps between walls, or missing walls… I want you to check
yourself and not come back to me showing the same result."*

CODEX, reviewing the first attempt, rejected the raster metric as flattering and
partly circular - it registered on the DXF's own wall faces and then scored those
same faces against wall-adjacent ink, sampled four points per wall, treated any
dark pixel as "ink", and **returned exit 0 while five walls breached its own
threshold.** All fair.

So the primary gate is this one, and it needs no raster at all: **the question
"is this corner a void?" is answered by the exported geometry itself.** It is
exact, it cannot be circular, and it fails loudly.

What it asserts
---------------
  1. every wall in `wall_blocks.csv` is PRESENT in the DXF, unless explicitly
     quarantined, and appears EXACTLY ONCE;
  2. every wall's cross-axis FACES match the placement - the absolute anchor,
     without which a rigid translation of the whole model satisfies every
     relative test below;
  3. every wall's DRAWN length equals its recorded `solid_mm`, and its drawn
     thickness its recorded thickness;
  4. every junction in `wall_corners.csv` is CLOSED - the corner square is
     covered by the wall union, so the corner volume exists once;
  5. no two walls OVERLAP where the ledger does not say they should;
  6. no pair of perpendicular walls sits in the NEAR-MISS band - close enough to
     be a junction, far enough to leave a cavity - without a ledger entry or a
     recorded `insulation_infill` directive explaining it;
  7. no unexplained cavity anywhere in the wall union.

Every one of 1, 2, 3 and 6 exists because a CODEX-seeded mutation passed the
gate without it. `scripts/dxf_closure_selftest.py` holds those seeds; a gate
nobody has watched fail is not a gate, and a gate that passed someone else's
seed was not the gate I reported.

Exit non-zero on any breach. `--json` prints the findings for a build.
"""
from __future__ import print_function

import argparse
import csv
import io
import json
import os
import sys

import ezdxf

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(REPO, 'data', 'canonical')
DXF = os.path.join(REPO, 'data', 'cad', 'dxf', 'v0_developer_layout.dxf')

NEAR_MM = 400.0        # closer than this and a perpendicular pair is a junction
TOUCH_MM = 1.0         # overlap of at least this counts as closed
FACE_TOL_MM = 1.0      # the placement is written to 0.1 mm; 1 mm is generous
LEN_TOL_MM = 15.0      # the exporter's own invariant tolerance
CELL = 10.0            # mm; a 10 mm sliver is below anything that matters


EXCEPTION_STATUS = ('open', 'accounted')      # the only declared vocabulary

# `--canon` points the gate at a COPY of data/canonical. CODEX round 3 needed an
# isolated fixture to mutate a canonical table alongside the DXF, and had to
# copy the whole tool to get one. A checker that cannot be pointed at seeded
# inputs cannot be adversarially tested against them.
_CANON = [CANON]


def read(name):
    p = os.path.join(_CANON[0], name)
    if not os.path.exists(p):
        return []
    with io.open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _entities():
    import importlib.util
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'dxf_wall_entities.py')
    spec = importlib.util.spec_from_file_location('dxf_wall_entities', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _state():
    import importlib.util
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v0_state.py')
    spec = importlib.util.spec_from_file_location('v0_state', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _load_oracle():
    import importlib.util
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'vector_extent_oracle.py')
    spec = importlib.util.spec_from_file_location('vector_extent_oracle', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _tabular():
    """The shared strict-CSV helpers. AGENTS.md: use these, not DictReader."""
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import lib.tabular as t
    return t


def walls_from_dxf(path):
    """Validated wall rectangles, via the ONE shared reader.

    !! This used to reduce each polyline to min/max x/y itself, and CODEX round 4
    showed what that costs: a closed TRIANGLE on three of a rectangle's corners
    kept the same label, layer, bounding box and nominal size, lost half the wall
    body, and passed. Everything downstream - corner squares, cavities, overlaps -
    was then reasoning about a rectangle nobody had drawn.

    The reader now REFUSES anything that is not the shape `export_v0_dxf.py`
    promises, and it is shared with `raster_fidelity.py` so the substitution
    cannot be reintroduced in one reader and not the other.
    """
    walls, problems = _entities().read_walls(path)
    return walls, problems


def read_placement():
    """The model's own absolute wall faces - the gate's anchor against a SHIFT.

    !! Every other assertion in this file is RELATIVE. Corner coverage, overlaps
    and cavities are all internal to the DXF, so translating the whole model
    leaves every one of them satisfied. CODEX seeded a 500 mm shift of the entire
    drawing and it passed - and my own shift seed had moved only the first six
    walls, which is precisely why I never saw it. A partial shift breaks
    junctions; a complete one does not.

    The anchor is the CROSS-AXIS faces. `close_corners` in the exporter only ever
    moves a wall along its OWN axis, never its faces, so `face_lo_mm` and
    `face_hi_mm` are exact between the placement and the drawing. The flat
    carries walls on both axes, so any translation moves the faces of one family
    or the other and cannot hide.

    !! Two defects found by the turn-10 SELF-AUDIT, not by a review:

      1. this read `CANON` directly and ignored `--canon`, so the placement -
         the gate's only absolute anchor - was the ONE input a seeded fixture
         could not mutate. A probe against it could never have failed, which is
         worse than an unchecked input: it looks covered.
      2. the result was a dict keyed by `wall_id`, so a duplicate entry silently
         won and the anchor then compared against the wrong placement - the same
         collapsing-collection class as the duplicate wall (round 2) and the
         duplicate label (round 5), found by sweeping for it.
    """
    p = os.path.join(_CANON[0], 'v0_named_walls_placed.json')
    if not os.path.exists(p):
        return {}, []
    with io.open(p, encoding='utf-8') as f:
        d = json.load(f)
    rows = [w for w in d.get('walls', []) if w.get('face_lo_mm') is not None]
    seen, dupes = {}, []
    for w in rows:
        if w['wall_id'] in seen:
            dupes.append(w['wall_id'])
        seen[w['wall_id']] = w
    return seen, sorted(set(dupes))


def inter(a, b):
    return (min(a['x1'], b['x1']) - max(a['x0'], b['x0']),
            min(a['y1'], b['y1']) - max(a['y0'], b['y0']))


def faces_of(w):
    """(face_lo, face_hi) - the cross-axis extent, whatever the axis."""
    return (w['y0'], w['y1']) if w['axis'] == 'EW' else (w['x0'], w['x1'])


def run_of(w):
    """(from, to) - the long-axis extent."""
    return (w['x0'], w['x1']) if w['axis'] == 'EW' else (w['y0'], w['y1'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dxf', default=DXF)
    ap.add_argument('--canon', default=None,
                    help='a COPY of data/canonical, so a seeded fixture can '
                         'mutate a canonical table alongside the DXF')
    ap.add_argument('--no-oracle', action='store_true',
                    help='skip the vector oracle (it re-parses the PDF, ~2 s)')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    if args.canon:
        _CANON[0] = args.canon

    wall_list, malformed = walls_from_dxf(args.dxf)
    ledger = read('wall_corners.csv')
    directives = read('junction_directives.csv')
    blocks = read('wall_blocks.csv')
    placement = read('wall_placement_directives.csv')
    placed, placed_dupes = read_placement()

    quarantined = set(r['wall_id'] for r in placement
                      if 'quarantin' in (r.get('status') or ''))
    infill = set()
    for r in directives:
        if (r.get('closure_kind') or '').strip() == 'insulation_infill':
            infill.add(frozenset((r['wall_a'].strip(), r['wall_b'].strip())))

    findings = []

    # === 0a. every canonical table's key is UNIQUE =======================
    # !! CODEX round 6 duplicated a byte-identical G6 row in wall_blocks.csv.
    # The gate printed "26 named walls" on the same line as "25 label ENTITIES"
    # and then declared every wall present exactly once, because every reader
    # keys these tables into a dict and last-wins. That is the fourth appearance
    # of the collapsing-collection class, and the second time the number was
    # PRINTED and not CHECKED.
    #
    # So it is closed for the whole family rather than for G6: `check_unique`
    # was already imported and used one screen below for the exception ledger,
    # and the same call now covers every canonical table the gate keys on.
    KEYS = (('wall_blocks.csv', ['wall_id']),
            ('wall_corners.csv', ['corner_id']),
            ('wall_placement_directives.csv', ['directive_id']),
            ('junction_directives.csv', ['directive_id']))
    print('canonical table keys - does any repeat?')
    t = _tabular()
    key_problems = []
    for name, cols in KEYS:
        path = os.path.join(_CANON[0], name)
        if not os.path.exists(path):
            continue
        rows, csv_problems = t.read_csv(path, strict=False)
        for pb in csv_problems + t.check_unique(path, rows, cols):
            key_problems.append(str(pb))
    for pb in key_problems:
        findings.append({'kind': 'duplicate_table_key', 'walls': [],
                         'detail': pb})
        print('  FAIL %s' % pb)
    if not key_problems:
        print('  ok   %d tables, every key unique and no malformed row'
              % len(KEYS))
    print()

    # === 0. shape: the entity is the rectangle it is taken for ===========
    # Before any measurement, because a malformed entity silently becomes its
    # bounding box in every measurement that follows.
    print('wall entity shape - is each one the rectangle it is read as?')
    for bad in malformed:
        findings.append({'kind': 'malformed_wall', 'walls': [bad['wall']],
                         'detail': bad['detail']})
        print('  FAIL %-5s %s' % (bad['wall'], bad['detail']))
    if not malformed:
        print('  ok   every wall entity is a closed, axis-aligned, zero-bulge '
              'rectangle filling its own bounding box')
    print()

    # === 1. identity: present, and exactly once ==========================
    print('wall identity - present, and one polyline each:')
    by_id = {}
    for w in wall_list:
        by_id.setdefault(w['id'], []).append(w)
    dupes = sorted(k for k, v in by_id.items() if len(v) > 1)
    for wid in dupes:
        findings.append({'kind': 'duplicate_wall', 'walls': [wid],
                         'detail': '%d polylines carry this label'
                                   % len(by_id[wid])})
        print('  FAIL %-5s %d polylines nearest this label - a duplicate wall'
              % (wid, len(by_id[wid])))
    absent = [r['wall_id'] for r in blocks if r['wall_id'] not in by_id]
    for wid in absent:
        if wid in quarantined:
            print('  ok   %-5s absent but QUARANTINED by directive' % wid)
        else:
            findings.append({'kind': 'missing_wall', 'walls': [wid],
                             'detail': 'not in the DXF and not quarantined'})
            print('  FAIL %-5s missing from the DXF, not quarantined' % wid)
    # !! A label with no polyline is a missing wall, and this is the ONE
    # presence test that needs no table at all. My own round-3 seed found the
    # hole: delete R4's polyline AND its row in `wall_blocks.csv`, and every
    # table-based presence check agrees there are 24 walls. But the DXF still
    # carries 25 V0-WALL-LABEL texts, because the drawing labels what it claims
    # to draw. Parity between labels and polylines is internal to the artefact
    # and cannot be falsified by editing canonical data.
    # !! `set(...)` here was the THIRD instance of one class in this dialogue:
    # a collection that deduplicates destroys the very defect being checked.
    # Round 2 it was a dict keyed by label, so a duplicate WALL overwrote the
    # original. Round 5 CODEX added a duplicate LABEL entity, and the set
    # collapsed 26 entities to 25 distinct names - so the count matched, the
    # parity check passed, and the gate printed "25 labels" for a file holding
    # 26. Labels are ENTITIES in a bijection with polylines, not a set of names.
    label_entities = _entities().label_names(args.dxf)
    labelled = set(label_entities)
    repeated = sorted(set(t for t in label_entities
                          if label_entities.count(t) > 1))
    for wid in repeated:
        findings.append({'kind': 'duplicate_label', 'walls': [wid],
                         'detail': '%d label entities carry this text'
                                   % label_entities.count(wid)})
        print('  FAIL %-5s %d label entities carry this text'
              % (wid, label_entities.count(wid)))
    orphan_labels = sorted(labelled - set(by_id))
    for wid in orphan_labels:
        findings.append({'kind': 'label_without_wall', 'walls': [wid],
                         'detail': 'the DXF labels this wall but draws no '
                                   'polyline for it'})
        print('  FAIL %-5s labelled in the DXF but no polyline is drawn' % wid)
    # the RAW entity count, never the de-duplicated one
    if len(label_entities) != len(wall_list):
        findings.append({'kind': 'label_count_mismatch', 'walls': [],
                         'detail': '%d label entities, %d wall polylines'
                                   % (len(label_entities), len(wall_list))})
        print('  FAIL %d label entities but %d wall polylines'
              % (len(label_entities), len(wall_list)))

    stray = sorted(set(by_id) - set(r['wall_id'] for r in blocks))
    for wid in stray:
        findings.append({'kind': 'unknown_wall', 'walls': [wid],
                         'detail': 'in the DXF but not in wall_blocks.csv'})
        print('  FAIL %-5s in the DXF but not a named wall' % wid)
    if not dupes and not absent and not stray and not repeated:
        print('  ok   all %d named walls present, one polyline and one label '
              'each' % len(by_id))
    # `len(blocks)` is a ROW count, and printing it beside two entity counts as
    # though all three were commensurate is how "26 named walls" sat next to a
    # claim of 25 without anything objecting. It is now labelled as rows, and
    # §0a has already asserted the rows are unique.
    print('  %d polylines, %d label ENTITIES (%d distinct), %d wall_blocks rows'
          % (len(wall_list), len(label_entities), len(labelled), len(blocks)))

    # W is the by-name view the rest of the gate uses. Building it AFTER the
    # duplicate assertion is deliberate: the collapse is now reported, not
    # silent.
    W = dict((w['id'], w) for w in wall_list)

    # === 2. the absolute anchor: faces match the placement ===============
    for wid in placed_dupes:
        findings.append({'kind': 'duplicate_placement', 'walls': [wid],
                         'detail': 'the placement file carries this wall '
                                   'more than once; the anchor would '
                                   'silently use one of them'})
    print('\nabsolute position - cross-axis faces against the placement:')
    for wid in placed_dupes:
        print('  FAIL %-5s appears more than once in the placement' % wid)
    if not placed:
        findings.append({'kind': 'no_anchor', 'walls': [],
                         'detail': 'v0_named_walls_placed.json is missing; the '
                                   'gate cannot detect a rigid shift'})
        print('  FAIL no placement file - a whole-model shift would pass')
    else:
        drift = []
        for wid, w in sorted(W.items()):
            ref = placed.get(wid)
            if not ref:
                continue
            lo, hi = faces_of(w)
            d = max(abs(lo - float(ref['face_lo_mm'])),
                    abs(hi - float(ref['face_hi_mm'])))
            if d > FACE_TOL_MM:
                drift.append((wid, lo, hi, ref['face_lo_mm'],
                              ref['face_hi_mm'], d))
        for wid, lo, hi, rlo, rhi, d in sorted(drift, key=lambda t: -t[5]):
            findings.append({'kind': 'face_drift', 'walls': [wid],
                             'detail': 'drawn %.1f/%.1f, placed %.1f/%.1f, '
                                       '%.1f mm off' % (lo, hi, rlo, rhi, d)})
            print('  FAIL %-5s drawn %9.1f/%-9.1f placed %9.1f/%-9.1f  %.1f mm'
                  % (wid, lo, hi, rlo, rhi, d))
        if not drift:
            print('  ok   all %d walls sit on their placed faces (<= %.0f mm)'
                  % (len(W), FACE_TOL_MM))

    # === 3. drawn length and thickness against the record ================
    # !! CODEX over-extended MC by 1000 mm and the gate passed: the extension ran
    # into open room, so it opened no cavity and overlapped nothing. Length is
    # not implied by closure and has to be asserted. The exporter has PRINTED
    # this invariant since it was written - printing is not checking, which is
    # the same error `build_wall_corners.py` made with solid_mm.
    # Eleven walls' recorded `solid_mm` disagrees with the drawn extent, by
    # -910 to +250 mm. That is NOT news the gate discovered: the exporter has
    # printed "14 of 25 walls within 15 mm" every run since it was written, and
    # I read past it and reported the export as agreeing. Printing is not
    # checking - the same error `build_wall_corners.py` made with its invariant.
    #
    # They are not silenced and they are not edited away. Each is pinned in
    # `wall_extent_exceptions.csv` with its measured delta and a cause, and the
    # gate fails on any DEVIATION from the pinned figure. So the debt is
    # countable and visible, a wall not on the list must agree, and a mutation -
    # CODEX's 1000 mm MC over-extension - moves a delta and fails.
    # === 3a. the exception ledger validates its OWN evidence ==============
    # !! CODEX round 3, finding 3: the gate read only `wall_id`, `delta_mm` and
    # `status`. In an isolated copy it set G4a's `drawn_mm` to 1 and `solid_mm`
    # to 99999, blanked `cause` and `notes`, invented a status, left `delta_mm`
    # alone - and the gate exited 0. Its words, and they are the right words:
    # **"the claimed measurements and explanation are not checks - they are
    # decorative fields beside an allowlisted delta."**
    #
    # So every field is now checked: strict CSV (a stray or missing cell is
    # visible), a declared status vocabulary, unique and known wall ids, a
    # non-empty cause AND note, and the row's own arithmetic recomputed against
    # the actual DXF and `wall_blocks.csv`.
    print('\nextent exception ledger - is its own evidence true?')
    rec = dict((r['wall_id'], r) for r in blocks)
    pinned = {}
    ex_path = os.path.join(_CANON[0], 'wall_extent_exceptions.csv')
    if os.path.exists(ex_path):
        t = _tabular()
        ex_rows, ex_problems = t.read_csv(ex_path, strict=False)
        for p in ex_problems:
            findings.append({'kind': 'bad_exception_row', 'walls': [],
                             'detail': str(p)})
            print('  FAIL malformed CSV: %s' % p)
        for p in (t.check_vocabulary(ex_path, ex_rows, 'status',
                                     EXCEPTION_STATUS)
                  + t.check_unique(ex_path, ex_rows, ['wall_id'])):
            findings.append({'kind': 'bad_exception_row', 'walls': [],
                             'detail': str(p)})
            print('  FAIL %s' % p)
        for r in ex_rows:
            wid = (r.get('wall_id') or '').strip()
            if wid not in rec:
                findings.append({'kind': 'bad_exception_row', 'walls': [wid],
                                 'detail': 'not a wall in wall_blocks.csv'})
                print('  FAIL %-5s not a known wall' % wid)
                continue
            for field in ('cause', 'notes'):
                if not (r.get(field) or '').strip():
                    findings.append({'kind': 'bad_exception_row',
                                     'walls': [wid],
                                     'detail': '%s is empty; an exception '
                                               'without a stated cause is not '
                                               'an exception' % field})
                    print('  FAIL %-5s %s is empty' % (wid, field))
            d_claim = t.finite(r.get('drawn_mm'))
            s_claim = t.finite(r.get('solid_mm'))
            delta = t.finite(r.get('delta_mm'))
            if delta is None:
                findings.append({'kind': 'bad_exception_row', 'walls': [wid],
                                 'detail': 'delta_mm is not a finite number'})
                print('  FAIL %-5s delta_mm is not a finite number' % wid)
                continue
            pinned[wid] = (delta, (r.get('status') or '').strip())
            # recompute the row's claims against the real DXF and the record
            w = W.get(wid)
            s_true = t.finite(rec[wid].get('solid_mm'))
            probs = []
            if s_claim is None or s_true is None or abs(s_claim - s_true) > 0.6:
                probs.append('solid_mm claims %s, wall_blocks.csv says %s'
                             % (s_claim, s_true))
            if w is not None:
                a, b = run_of(w)
                d_true = b - a
                if d_claim is None or abs(d_claim - d_true) > 0.6:
                    probs.append('drawn_mm claims %s, the DXF is %.1f'
                                 % (d_claim, d_true))
                if (d_claim is not None and s_claim is not None
                        and abs((d_claim - s_claim) - delta) > 0.6):
                    probs.append('delta_mm %.1f is not drawn_mm - solid_mm '
                                 '(%.1f)' % (delta, d_claim - s_claim))
            if probs:
                findings.append({'kind': 'false_exception_evidence',
                                 'walls': [wid], 'detail': '; '.join(probs)})
                print('  FAIL %-5s %s' % (wid, '; '.join(probs)))
        if not any(f['kind'] in ('bad_exception_row',
                                 'false_exception_evidence')
                   for f in findings):
            print('  ok   %d rows: statuses declared, ids known and unique, '
                  'causes stated, arithmetic recomputed against the DXF and '
                  'the record' % len(ex_rows))

    print('\ndrawn extent against wall_blocks.csv:')
    bad = 0
    for wid, w in sorted(W.items()):
        r = rec.get(wid)
        if not r:
            continue
        a, b = run_of(w)
        lo, hi = faces_of(w)
        drawn, thick = b - a, hi - lo
        try:
            want_len = float(r['solid_mm'])
        except (TypeError, ValueError):
            want_len = None
        try:
            want_t = float(r['thickness_mm'])
        except (TypeError, ValueError):
            want_t = None
        msg = []
        if want_len is not None:
            delta = drawn - want_len
            allow, status = pinned.get(wid, (0.0, ''))
            if abs(delta - allow) > LEN_TOL_MM:
                if wid in pinned:
                    msg.append('length %.1f vs solid_mm %.0f: delta %+.1f, '
                               'but %+.1f is pinned in '
                               'wall_extent_exceptions.csv'
                               % (drawn, want_len, delta, allow))
                else:
                    msg.append('length %.1f vs solid_mm %.0f (%+.1f), and no '
                               'pinned exception' % (drawn, want_len, delta))
        # thickness is never excepted: no row in that file is about thickness,
        # and a wall of the wrong thickness is the class CODEX asked for
        if want_t is not None and abs(thick - want_t) > FACE_TOL_MM:
            msg.append('thickness %.1f vs recorded %.0f' % (thick, want_t))
        if msg:
            bad += 1
            findings.append({'kind': 'wrong_extent', 'walls': [wid],
                             'detail': '; '.join(msg)})
            print('  FAIL %-5s %s' % (wid, '; '.join(msg)))
    if not bad:
        print('  ok   every wall is drawn at its recorded thickness, and at its '
              'recorded length or its pinned delta')
    if pinned:
        opens = sorted(k for k, v in pinned.items() if v[1] == 'open')
        print('  !!   %d walls carry a PINNED extent exception, %d of them still '
              'OPEN: %s' % (len(pinned), len(opens), ', '.join(opens)))
        print('       these are recorded disagreements between the record and '
              'the drawing, not agreements')

    # === 3b. the INDEPENDENT extent oracle: the hatched solids ============
    # !! CODEX round 3, finding 2. Asserting the DXF against `wall_blocks.csv`
    # proves only that two things a person edits together agree: it extended MC
    # 1000 mm, edited MC's clear_mm/solid_mm to match, and the gate passed - the
    # coupled edit even preserves `clear + owned corner = solid`. The oracle
    # below re-derives the hatched wall solids from the PDF at check time, so no
    # table edit can move it, and the PDF's sha256 is asserted so the drawing
    # cannot be swapped either.
    if not args.no_oracle:
        print('\nindependent oracle - drawn runs against the PDF\'s hatched '
              'solids:')
        try:
            oracle = _load_oracle()
            ok, got = oracle.pdf_identity()
            if not ok:
                findings.append({'kind': 'wrong_source_drawing', 'walls': [],
                                 'detail': 'PDF sha256 is %s, expected %s'
                                           % (got, oracle.PDF_SHA256)})
                print('  FAIL the source drawing is not the one this oracle '
                      'trusts: sha256 %s' % got)
            else:
                solids = oracle.vector_solids()
                o_find, o_rows = oracle.check(wall_list, solids, quarantined)
                findings.extend(o_find)
                allow = max(oracle.max_solid_thickness(solids),
                            oracle.CORNER_ALLOWANCE_FLOOR_MM)
                worst = sorted((r for r in o_rows if r[1]),
                               key=lambda r: -r[2])[:4]
                for wid, sid, over, _faced, note in worst:
                    print('  %-5s %s' % (wid, note))
                print('  %d of %d walls sit on a hatched solid; corner '
                      'allowance %.0f mm (the drawing\'s thickest solid)'
                      % (sum(1 for r in o_rows if r[1]), len(o_rows), allow))
                for f in o_find:
                    print('  FAIL %-5s %s' % (f['walls'][0], f['detail']))
                if not o_find:
                    print('  ok   no wall is drawn past its hatched solid by '
                          'more than the corner allowance')
        except Exception as exc:                     # noqa: BLE001
            findings.append({'kind': 'oracle_unavailable', 'walls': [],
                             'detail': '%s: %s' % (type(exc).__name__, exc)})
            print('  FAIL the oracle could not run: %s: %s'
                  % (type(exc).__name__, exc))

    # === rasterise the wall union, for 4 and 7 ===========================
    # !! The first version of this gate tested "do the two rectangles overlap in
    # both axes", and it was wrong. MA ends exactly on R8's face and R8 spans the
    # corner, so the corner IS solid while the x-overlap is zero. What matters is
    # whether the corner REGION is covered by the union of walls - a coverage
    # question, not a pairwise-overlap question.
    xs = [v for w in W.values() for v in (w['x0'], w['x1'])]
    ys = [v for w in W.values() for v in (w['y0'], w['y1'])]
    if not xs:
        print('\nno walls in the DXF at all')
        return 1
    ox, oy = min(xs) - CELL, min(ys) - CELL
    nx = int((max(xs) - ox) / CELL) + 2
    ny = int((max(ys) - oy) / CELL) + 2
    grid = [[None] * nx for _ in range(ny)]
    for w in W.values():
        i0 = int((w['x0'] - ox) / CELL + 0.5)
        i1 = int((w['x1'] - ox) / CELL + 0.5)
        j0 = int((w['y0'] - oy) / CELL + 0.5)
        j1 = int((w['y1'] - oy) / CELL + 0.5)
        for j in range(j0, j1):
            for i in range(i0, i1):
                if 0 <= j < ny and 0 <= i < nx:
                    grid[j][i] = w['id']

    def covered(x0, x1, y0, y1):
        i0 = int((x0 - ox) / CELL + 0.5)
        i1 = max(i0 + 1, int((x1 - ox) / CELL + 0.5))
        j0 = int((y0 - oy) / CELL + 0.5)
        j1 = max(j0 + 1, int((y1 - oy) / CELL + 0.5))
        total = miss = 0
        for j in range(j0, j1):
            for i in range(i0, i1):
                if not (0 <= j < ny and 0 <= i < nx):
                    continue
                total += 1
                if grid[j][i] is None:
                    miss += 1
        return total, miss

    # === 4. per-corner coverage ==========================================
    # !! The flood-fill alone is not enough, and a seed proved it: pull MC 300 mm
    # off R7 and the void it opens CONNECTS TO THE ROOM, so the fill sees one
    # large empty region and calls it a room, not a pocket. A corner has to be
    # asserted directly. For an L between an EW wall H and an NS wall V the
    # corner square is (V's x band) x (H's y band), closed only if every cell of
    # that square is covered by the wall union.
    print('\nledger junctions - is the corner square solid?')
    for r in ledger:
        a, b = W.get(r['wall_a']), W.get(r['wall_b'])
        cid = r['corner_id']
        if not a or not b:
            continue                      # reported under wall identity
        h, v = (a, b) if a['axis'] == 'EW' else (b, a)
        if h['axis'] == v['axis']:
            continue                      # collinear pair; not an L
        total, miss = covered(v['x0'], v['x1'], h['y0'], h['y1'])
        if miss:
            findings.append({'kind': 'open_corner', 'corner': cid,
                             'detail': '%d of %d cells of the corner square are '
                                       'empty' % (miss, total)})
            print('  FAIL %-12s %d of %d cells EMPTY - the corner is a void'
                  % (cid, miss, total))
        else:
            print('  ok   %-12s solid, %d cells' % (cid, total))

    # === 5. unsanctioned overlaps ========================================
    ledger_pairs = set(frozenset((r['wall_a'], r['wall_b'])) for r in ledger)
    ids = sorted(W)
    print('\noverlaps not sanctioned by the ledger:')
    any_ov = False
    for i, ai in enumerate(ids):
        for bi in ids[i + 1:]:
            if frozenset((ai, bi)) in ledger_pairs:
                continue
            ix, iy = inter(W[ai], W[bi])
            if ix > TOUCH_MM and iy > TOUCH_MM:
                any_ov = True
                findings.append({'kind': 'unexpected_overlap',
                                 'walls': [ai, bi],
                                 'detail': '%.0f x %.0f mm' % (ix, iy)})
                print('  FAIL %-5s x %-5s  %.0f x %.0f mm' % (ai, bi, ix, iy))
    if not any_ov:
        print('  none')

    # === 6. the near-miss band ===========================================
    # !! I DOCUMENTED this check in the header and did not implement it - the
    # pairwise near-miss branch was replaced by the flood-fill and never
    # reinstated. CODEX caught the discrepancy. It is a distinct question from
    # both the corner squares (which only covers pairs the LEDGER names) and the
    # cavity scan (which needs the pocket to be enclosed): two perpendicular
    # walls can end 200 mm apart in open air, forming a joint the owner would
    # read as a gap, with no ledger row to check and no enclosed pocket to find.
    print('\nperpendicular pairs in the near-miss band (%.0f mm):' % NEAR_MM)
    any_nm = False
    for i, ai in enumerate(ids):
        for bi in ids[i + 1:]:
            a, b = W[ai], W[bi]
            if a['axis'] == b['axis']:
                continue
            pair = frozenset((ai, bi))
            ix, iy = inter(a, b)
            # a junction-shaped relation: one axis overlaps, the other is a
            # small positive gap
            if ix > TOUCH_MM and -NEAR_MM < iy <= TOUCH_MM:
                gap = -iy
            elif iy > TOUCH_MM and -NEAR_MM < ix <= TOUCH_MM:
                gap = -ix
            else:
                continue
            if gap <= 0:
                continue                  # they touch; that is closed
            if pair in ledger_pairs:
                # the ledger names it, so §4 has already asserted the square
                continue
            if pair in infill:
                print('  ok   %-5s x %-5s  %.0f mm - closed by external '
                      'insulation' % (ai, bi, gap))
                continue
            any_nm = True
            findings.append({'kind': 'near_miss', 'walls': [ai, bi],
                             'detail': '%.0f mm gap, no ledger row and no '
                                       'directive' % gap})
            print('  FAIL %-5s x %-5s  %.0f mm apart, nothing explains it'
                  % (ai, bi, gap))
    if not any_nm:
        print('  none unexplained')

    # === 7. cavities anywhere in the union ===============================
    seen = [[False] * nx for _ in range(ny)]
    cavities = []
    for j in range(ny):
        for i in range(nx):
            if grid[j][i] is not None or seen[j][i]:
                continue
            stack, cells, touch = [(i, j)], 0, set()
            seen[j][i] = True
            while stack:
                ci, cj = stack.pop()
                cells += 1
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = ci + di, cj + dj
                    if not (0 <= ni < nx and 0 <= nj < ny):
                        continue
                    if grid[nj][ni] is not None:
                        touch.add(grid[nj][ni])
                    elif not seen[nj][ni]:
                        seen[nj][ni] = True
                        stack.append((ni, nj))
                if cells > 40000:
                    break
            # a room is a big empty region touching many walls; a CAVITY is a
            # small one wedged between two or three
            area = cells * CELL * CELL
            if len(touch) >= 2 and area <= 0.35e6:
                cavities.append((sorted(touch), area, cells))

    print('\nwall-union cavities (empty pockets touching 2+ walls, <= 0.35 m2):')
    if not cavities:
        print('  none')
    for touch, area, cells in sorted(cavities, key=lambda t: -t[1]):
        pair = frozenset(touch) if len(touch) == 2 else None
        if pair and pair in infill:
            print('  ok   %-16s %8.0f mm2 - closed by external insulation'
                  % ('+'.join(touch), area))
            continue
        findings.append({'kind': 'cavity', 'walls': touch,
                         'detail': '%.0f mm2' % area})
        print('  FAIL %-16s %8.0f mm2 between %s'
              % ('+'.join(touch), area, ', '.join(touch)))

    # === 8. the review drawing must not report a previous round ==========
    # !! CODEX round 4: `render_dxf.py` hard-coded "the лоджия is still NOT a
    # closed loop" and "9 walls carry an OPEN extent exception" while the loop
    # was closed and the ledger held 10. The owner reads that caption, and his
    # standing instruction is exactly this: "I want you to check yourself and not
    # come back to me showing the same result." A drawing that states last
    # round's verdict IS that failure.
    #
    # The caption is now derived, and this asserts the drawing on disk was made
    # from the state that exists now. Skipped when --dxf points at a seeded copy,
    # because the sidecar describes the real export, not the fixture.
    if args.dxf == DXF and not args.canon:
        print('\nthe review drawing - is the DELIVERED IMAGE the current one?')
        try:
            v0 = _state()
            ep = os.path.join(CANON, 'v0_elements_extracted.json')
            glazing = None
            if os.path.exists(ep):
                with io.open(ep, encoding='utf-8') as f:
                    glazing = json.load(f).get('loggia_glazing')
            current = v0.summary(wall_list, glazing, canon=_CANON[0])

            # (a) the sidecar's CLAIMS against the current state. This names
            #     which claim drifted, which raw bytes cannot.
            for d in v0.stale(current, v0.read_sidecar()):
                findings.append({'kind': 'stale_review_drawing', 'walls': [],
                                 'detail': d})
                print('  FAIL %s' % d)

            # (b) the PNG BYTES against a fresh render. !! CODEX round 5:
            #     replacing only the PNG with the pre-fix artefact from 23ac367
            #     and leaving the current sidecar in place passed, because
            #     nothing here ever read the image. The sidecar's own `what`
            #     field asserted it described the PNG, without evidence.
            #     A digest stored in that same editable sidecar would not help
            #     either - a coupled edit updates both. So the expected bytes
            #     are COMPUTED: the renderer is byte-deterministic here, so the
            #     delivered image must equal what it produces now. Nothing
            #     stored is trusted.
            exp, got, why = v0.render_matches(REPO, args.dxf)
            # BOTH delivered images, not just the one that happened to have a
            # gate. The fidelity image went stale the day after this check was
            # written, because a regenerated copy was reverted to tidy the
            # working tree - and only the unauthenticated one drifted.
            f_exp, f_got, f_why = v0.render_matches(
                REPO, args.dxf, tool='raster_fidelity.py',
                image=v0.FIDELITY_PNG)
            for w in (why, f_why):
                if w:
                    findings.append({'kind': 'stale_review_drawing',
                                     'walls': [], 'detail': w})
                    print('  FAIL %s' % w)
            if not why and not f_why:
                print('  ok   both delivered images are byte-identical to a '
                      'fresh render (readback %s, fidelity %s)'
                      % (got[:12], f_got[:12]))
                print('       the readback sidecar reports %d open exception(s) '
                      'of %d, лоджия loop closed=%s'
                      % (current['open_exceptions'],
                         current['total_exceptions'],
                         current['loggia_loop_closed']))
        except Exception as exc:                       # noqa: BLE001
            findings.append({'kind': 'stale_review_drawing', 'walls': [],
                             'detail': '%s: %s' % (type(exc).__name__, exc)})
            print('  FAIL could not check the review drawing: %s' % exc)

    if args.json:
        print(json.dumps({'findings': findings}, indent=1, ensure_ascii=False))

    print()
    if findings:
        print('FAIL - %d finding(s): %s' % (
            len(findings),
            ', '.join(sorted(set(f['kind'] for f in findings)))))
        return 1
    print('PASS - every wall is present exactly once and on its placed faces, '
          'drawn at its recorded size, every ledger junction is closed, nothing '
          'overlaps or near-misses unexplained, and there is no cavity')
    return 0


if __name__ == '__main__':
    sys.exit(main())
