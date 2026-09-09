# -*- coding: utf-8 -*-
"""Build and check the corner ledger for the flat's wall model.

The problem the owner posed, 2026-09-04
---------------------------------------
"One bad thing is overlapping. Another bad thing is creating a void. A correct
junction is, for example, MA and R8, R8 and MB - a perfect corner when you take
the thickness into account. If we connect R1a and R1b we get a void at the very
corner. You should extend either R1b or R1a by the thickness, 250 mm."

He is right, and it breaks the convention this repo adopted one version earlier.
"Every length is the clear internal run" cannot double-count a corner, but it
leaves every L-corner unfilled. A corner is a solid and exactly one wall owns it.

Why this is a LEDGER and not a re-snap of the drawing
-----------------------------------------------------
The first attempt snapped the drawn pixel runs until the corners closed. That was
the wrong instrument: it moved lengths that come from printed dimensions and the
owner's own chains by tens of millimetres, to satisfy a raster registration that
is only good to ~50 mm. The drawing locates walls; it does not define them.

So the corner decision lives in the LENGTHS instead. Each wall carries:

    clear_mm  what the plan prints and what a tape held inside the room reads
    solid_mm  clear_mm + the thickness of every corner this wall OWNS

Nothing is double-counted, nothing is voided, and no printed number is disturbed.

Ownership is deterministic, so the ledger does not depend on who builds it:

    1. the concrete FRAME owns the corner    (the structure beats the infill)
    2. else the THICKER wall owns it         (the envelope beats a partition)
    3. on a tie, the LONGER run owns it      (the continuous line beats a stub)
    4. on a tie, the alphabetically first    (only so the output is stable)

!! Rule 1 was missing from this description until 2026-09-09, and its absence was
not cosmetic. G3 and R2 are BOTH 250 mm, so a reader following the old
"thicker, then longer" text would predict a length tie-break and could conclude
that G3 owns C_G3_R2 - which is exactly the contradiction found in G3's own note
that day. The code always implemented frame priority; only the prose was wrong,
and the prose is what a maintainer reads.

Rule 2 independently reproduces the two junctions the owner pointed to as already
correct - MA over R8 and MB over R8 - which is the check that it is the right rule
rather than a convenient one.

Usage
-----
    py -3 tools/layout/build_wall_corners.py            # check the ledger
    py -3 tools/layout/build_wall_corners.py --write    # (re)generate it

Exits non-zero if any L-corner is unowned, owned twice, or absent from the ledger.
"""
from __future__ import print_function

import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_wall_junctions import (MM_PER_PX, RUNS, TOL_MM,  # noqa: E402
                                  NEAR_MM, load, orient,
                                  successor_groups, is_dominant_pair,
                                  butts_not_corners)

LEDGER = os.path.join(os.path.dirname(RUNS), 'wall_corners.csv')
FIELDS = ['corner_id', 'kind', 'wall_a', 'wall_b', 'owner',
          'owner_gains_mm', 'note']


def run_len_mm(w):
    return (abs(w['b'][0] - w['a'][0]) + abs(w['b'][1] - w['a'][1])) * MM_PER_PX


FRAME = 'concrete'      # the monolithic RC frame; everything else is infill


def pick_owner(w1, w2):
    """(owner, other) by the deterministic rule."""
    f1, f2 = w1['cls'] == FRAME, w2['cls'] == FRAME
    if f1 != f2:
        return (w1, w2) if f1 else (w2, w1)
    if w1['t'] != w2['t']:
        return (w1, w2) if w1['t'] > w2['t'] else (w2, w1)
    if abs(run_len_mm(w1) - run_len_mm(w2)) > 1.0:
        return (w1, w2) if run_len_mm(w1) > run_len_mm(w2) else (w2, w1)
    return (w1, w2) if w1['id'] < w2['id'] else (w2, w1)


def classify(walls):
    """-> (list of L corners, list of T junctions)"""
    tol, near = TOL_MM / MM_PER_PX, NEAR_MM / MM_PER_PX
    byid = dict((w['id'], w) for w in walls)
    groups = successor_groups(walls)
    Ls, Ts = [], []
    for i in range(len(walls)):
        for j in range(i + 1, len(walls)):
            h, v = walls[i], walls[j]
            oh, fh, lh, hh = orient(h)
            ov, fv, lv, hv = orient(v)
            if oh is None or ov is None or oh == ov:
                continue
            if oh == 'v':
                h, v = v, h
                oh, fh, lh, hh, ov, fv, lv, hv = ov, fv, lv, hv, oh, fh, lh, hh
            if not (lh - near <= fv <= hh + near and lv - near <= fh <= hv + near):
                continue
            if not is_dominant_pair(h, v, groups, byid, near):
                continue          # this junction belongs to a successor sibling
            if butts_not_corners(h, v):
                continue          # a thin partition on a frame face: a butt
            ah, av = h['t'] / 2.0 / MM_PER_PX, v['t'] / 2.0 / MM_PER_PX
            h_int = (fv - lh > av + tol) and (hh - fv > av + tol)
            v_int = (fh - lv > ah + tol) and (hv - fh > ah + tol)
            if h_int and v_int:
                continue                       # a true crossing: check_wall_crossings
            if h_int or v_int:
                thru, butt = (h, v) if h_int else (v, h)
                Ts.append((thru['id'], butt['id']))
            else:
                own, oth = pick_owner(h, v)
                Ls.append((own, oth))
    return Ls, Ts


ASSEMBLIES = os.path.join(os.path.dirname(RUNS), 'structural_assemblies.csv')
BLOCKS = os.path.join(os.path.dirname(RUNS), 'wall_blocks.csv')
DIRECTIVES = os.path.join(os.path.dirname(RUNS), 'junction_directives.csv')

CLOSURE_KINDS = {'wall_extension', 'insulation_infill', 'unresolved'}


def directives():
    """Owner-directed junctions that classify() cannot emit, plus their checks.

    Why a companion file rather than widening classify(): that function works on
    the older basic-raster wall_runs.csv with a broad proximity rule and already
    carries domain-specific suppression. Raising its capture radius to absorb
    known tens-of-millimetre gaps would fold three different things - extraction
    error, closure by external insulation, and an explicit owner instruction -
    into one inferred geometry, and would risk inventing corners elsewhere. So
    the derived ledger stays derived, and the owner's instructions are declared.

    !! insulation_infill is NOT a wall extension. The owner: the gaps at MB / R2
    / R9 "are filled with the insulation, another layer which lays on top of the
    external walls". Closing those by lengthening masonry would count insulation
    as masonry. Such a row carries no `extends` and must never be turned into
    ownership.

    Returns (rows, problems).
    """
    if not os.path.exists(DIRECTIVES):
        return [], []
    rows, problems, seen = [], [], set()
    with io.open(DIRECTIVES, encoding='utf-8') as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            did = (r.get('directive_id') or '').strip()
            a, b = (r.get('wall_a') or '').strip(), (r.get('wall_b') or '').strip()
            kind = (r.get('closure_kind') or '').strip()
            ext = (r.get('extends') or '').strip()
            if not did:
                problems.append('junction_directives line %d has no directive_id' % i)
                continue
            if did in seen:
                problems.append('%s: directive_id repeats' % did)
            seen.add(did)
            if kind not in CLOSURE_KINDS:
                problems.append('%s: closure_kind %r is not one of %s'
                                % (did, kind, sorted(CLOSURE_KINDS)))
            if a == b or not a or not b:
                problems.append('%s: wall_a and wall_b must differ and be named' % did)
            if kind == 'wall_extension' and ext not in (a, b):
                problems.append('%s: extends %r must be wall_a or wall_b' % (did, ext))
            if kind == 'insulation_infill' and ext:
                problems.append('%s: an insulation_infill row must NOT name a wall '
                                'to extend - the closure is the insulation layer, '
                                'not masonry' % did)
            if not (r.get('source') or '').strip():
                problems.append('%s: no source; a directive without provenance is '
                                'indistinguishable from a guess' % did)
            rows.append(r)
    return rows, problems


def assembly_of():
    """wall_id -> assembly_id, for walls that are legs of one physical element.

    Owner, 2026-09-09: "R1a and R1b is actually one corner element... this corner
    is one concrete slab without any joints." The vector plan agrees - it draws a
    block joint across the full wall thickness at every real joint, and there is
    none at that corner.

    !! So the ledger must not describe that corner as a joint. The corner VOLUME
    still has to be allocated to exactly one leg, because the quantity arithmetic
    works on rectangular legs and would otherwise count it twice or not at all -
    but the allocation is a bookkeeping device inside one casting, not a junction
    between two walls. This function is what lets rows_from() say so, and say it
    on every regeneration rather than in a hand-edit that the next --write wipes.
    """
    out = {}
    if not os.path.exists(ASSEMBLIES):
        return out
    with io.open(ASSEMBLIES, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            for wid in (r.get('member_walls') or '').split('|'):
                if wid.strip():
                    out[wid.strip()] = r['assembly_id']
    return out


def assembly_of_strict(walls):
    """assembly_of(), but FAILS CLOSED instead of silently losing an assembly.

    !! The permissive version returns an empty map when the canonical file is
    missing or unreadable, and the only visible consequence is that a monolithic
    pair quietly regenerates as an ordinary L-corner with a construction-joint
    note. That is a fail-open on the exact semantics this ledger exists to carry.

    A wall whose `structural_element_id` is not its own id is DECLARING that it
    belongs to a compound assembly, so the assembly must be resolvable. Returns
    (map, problems).
    """
    problems = []
    declared = {}
    if os.path.exists(BLOCKS):
        with io.open(BLOCKS, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                sid = (r.get('structural_element_id') or '').strip()
                wid = r['wall_id']
                if not sid:
                    problems.append('%s has no structural_element_id; a singleton '
                                    'must carry its own id, never blank' % wid)
                elif sid != wid:
                    declared[wid] = sid

    if declared and not os.path.exists(ASSEMBLIES):
        problems.append('%s references assemblies %s but %s is missing'
                        % (os.path.basename(BLOCKS),
                           sorted(set(declared.values())),
                           os.path.basename(ASSEMBLIES)))
        return {}, problems

    asm = assembly_of()
    for wid, sid in sorted(declared.items()):
        if asm.get(wid) != sid:
            problems.append('%s declares structural_element_id %r, but %s does '
                            'not list it as a member of that assembly'
                            % (wid, sid, os.path.basename(ASSEMBLIES)))
    for wid, sid in sorted(asm.items()):
        if declared.get(wid) != sid:
            problems.append('%s lists %s as a member of %r, but the wall does '
                            'not declare that structural_element_id'
                            % (os.path.basename(ASSEMBLIES), wid, sid))
    return asm, problems


def directive_rows(drows, walls):
    """Ledger rows for the owner-directed junctions, in the generated shape."""
    byid = dict((w['id'], w) for w in walls)
    out = []
    for r in drows:
        if (r.get('closure_kind') or '').strip() != 'wall_extension':
            continue
        a, b = sorted([r['wall_a'].strip(), r['wall_b'].strip()])
        ext = r['extends'].strip()
        other = b if ext == a else a
        w = byid.get(other)
        gain = '%g' % (w['t'] if w else 0)
        out.append({
            'corner_id': 'C_%s_%s' % (a, b),
            'kind': 'owner_directed',
            'wall_a': a,
            'wall_b': b,
            'owner': ext,
            'owner_gains_mm': gain,
            'note': ('OWNER-DIRECTED (%s): %s extends onto %s to close a junction '
                     'classify() cannot see. %s'
                     % (r.get('directive_id', '?'), ext, other,
                        (r.get('notes') or '').split('.')[0])),
        })
    return out


def rows_from(Ls, asm=None):
    asm = asm if asm is not None else {}
    out = []
    for own, oth in sorted(Ls, key=lambda r: (r[0]['id'], r[1]['id'])):
        a, b = sorted([own['id'], oth['id']])
        same = (asm.get(a) is not None and asm.get(a) == asm.get(b))
        if same:
            kind = 'continuous_casting'
            note = ('NO CONSTRUCTION JOINT: %s and %s are legs of one monolithic '
                    'casting, %s - see structural_assemblies.csv. The %g mm is a '
                    'one-time volume allocation to %s so the rectangular-leg '
                    'arithmetic counts the corner once; it is NOT a junction. '
                    'Use the assembly footprint for demolition, reinforcement, '
                    'structural review and IFC.'
                    % (a, b, asm.get(a), oth['t'], own['id']))
        else:
            kind = 'L'
            note = ('%s runs through to %s\'s far face; %s stops on %s\'s near face'
                    % (own['id'], oth['id'], oth['id'], own['id']))
        out.append({
            'corner_id': 'C_%s_%s' % (a, b),
            'kind': kind,
            'wall_a': a,
            'wall_b': b,
            'owner': own['id'],
            'owner_gains_mm': '%g' % oth['t'],
            'note': note,
        })
    return out


def main():
    walls = load(RUNS)
    Ls, Ts = classify(walls)
    asm, asm_problems = assembly_of_strict(walls)
    drows, d_problems = directives()
    want = rows_from(Ls, asm)
    have_ids = set(r['corner_id'] for r in want)
    for r in directive_rows(drows, walls):
        if r['corner_id'] in have_ids:
            d_problems.append('%s is already a derived corner; remove the directive'
                              % r['corner_id'])
        else:
            want.append(r)
    asm_problems += d_problems
    print('%d L-corners, %d T-junctions across %d wall runs'
          % (len(Ls), len(Ts), len(walls)))

    if '--write' in sys.argv:
        with io.open(LEDGER, 'w', encoding='utf-8', newline='') as f:
            wr = csv.DictWriter(f, fieldnames=FIELDS)
            wr.writeheader()
            wr.writerows(want)
        print('wrote %s' % LEDGER)

    if not os.path.exists(LEDGER):
        print('FAIL - no ledger. Run with --write')
        return 1

    with io.open(LEDGER, encoding='utf-8') as f:
        have = dict((r['corner_id'], r) for r in csv.DictReader(f))
    # !! Compare EVERY generated field, not just membership and the gain.
    # Until 2026-09-09 this loop accepted any owner that was one of the two
    # walls, and never looked at `kind` at all. So restoring G3 as owner of
    # C_G3_R2 -- the precise contradiction this ledger had just resolved --
    # would have PASSED, and so would flipping C_R1a_R1b back to a construction
    # joint. A check that cannot fail on the error it exists to catch is not a
    # check. scripts/structural_assembly_selftest.py proves each case fails.
    problems = list(asm_problems)
    SEMANTIC = ('wall_a', 'wall_b', 'owner', 'owner_gains_mm', 'kind', 'note')
    for r in want:
        got = have.get(r['corner_id'])
        if got is None:
            problems.append('%s missing from the ledger' % r['corner_id'])
            continue
        for field in SEMANTIC:
            if (got.get(field) or '') != r[field]:
                problems.append('%s: %s is %r, the generator says %r'
                                % (r['corner_id'], field, got.get(field),
                                   r[field]))
    for cid in have:
        if cid not in set(r['corner_id'] for r in want):
            problems.append('%s in the ledger is not a corner in the geometry' % cid)

    gains = {}
    for r in want:
        gains.setdefault(r['owner'], []).append((r['owner_gains_mm'], r['corner_id']))
    print('\nsolid_mm = clear_mm + the corners a wall owns:')
    for wid in sorted(gains):
        tot = sum(float(g) for g, _ in gains[wid])
        print('  %-5s + %s = +%g mm' % (wid, ' + '.join(g for g, _ in gains[wid]), tot))
    owned = set()
    for r in want:
        other = r['wall_b'] if r['owner'] == r['wall_a'] else r['wall_a']
        owned.add(other)
    print('  every other wall: solid_mm = clear_mm')

    # !! The invariant this tool has always PRINTED as a heading but never
    # checked: solid_mm must equal clear_mm plus the corners the wall owns.
    # R8's solid_mm sat at 1790 while it owned two 300 mm corners on a 1490 clear
    # run, i.e. 2090 - the 1790 looks copied from R9, which owns one. Nothing
    # caught it, because the tool reported the gains without comparing them to
    # the file. Found only when the exporter drew R8 over-long and the owner
    # noticed on the drawing.
    if os.path.exists(BLOCKS):
        with io.open(BLOCKS, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                clear, solid = r.get('clear_mm'), r.get('solid_mm')
                if not clear or not solid:
                    continue
                owns = sum(float(g) for g, _ in gains.get(r['wall_id'], []))
                want = float(clear) + owns
                if abs(want - float(solid)) > 1.0:
                    problems.append(
                        '%s: solid_mm is %s, but clear_mm %s + owned corners %g '
                        '= %g' % (r['wall_id'], solid, clear, owns, want))

    if problems:
        for p in problems:
            print('  FAIL %s' % p)
        return 1
    print('\nPASS - every L-corner is owned exactly once; no void, no double '
          'count; and solid_mm = clear_mm + owned corners for every wall')
    return 0


if __name__ == '__main__':
    sys.exit(main())
