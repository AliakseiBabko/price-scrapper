# -*- coding: utf-8 -*-
"""Validate the structural-assembly layer: referential integrity and footprints.

Why this exists
---------------
`structural_assemblies.csv` records the PHYSICAL elements of the flat, where
`wall_blocks.csv` records the CALCULATION LEGS. The owner approved that split on
2026-09-09 for the one case that needs it: R1a and R1b are two named legs of a
single monolithic L-shaped concrete casting with no joint between them.

CODEX, reviewing the first implementation, was right that the row alone was not
enough: the footprint was an opaque delimited string, nothing recomputed its
area, nothing checked that members exist or that a wall belongs to at most one
assembly, and there were no provenance or status fields for the coordinates -
which plan section 4.6 requires, precisely so project precision is never
mistaken for as-built accuracy.

What is checked
---------------
  * schema_version is present and known
  * every member wall exists in wall_blocks.csv
  * no wall is a member of two assemblies, and no member is repeated
  * every wall whose structural_element_id is not its own id resolves to an
    assembly that lists it; and every member declares that id  (both directions)
  * a singleton wall carries its OWN id, never blank -- blank would conflate
    "singleton" with "not migrated"
  * vertices: contiguous 0..n-1 indices, at least 4 of them, no repeated point,
    axis-aligned edges only for an orthogonal footprint, and a closing edge
  * footprint_area_m2 recomputed by the shoelace formula and compared
  * per-coordinate provenance: source_drawing, source_entity, status and
    field_verified all present, with status from a known vocabulary

Usage
-----
    py -3 tools/layout/validate_structural_assemblies.py

Exits non-zero on any problem. Negative cases are proved to fail by
scripts/structural_assembly_selftest.py.
"""
from __future__ import print_function

import codecs
import csv
import io
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(REPO, 'data', 'canonical')
ASSEMBLIES = os.path.join(CANON, 'structural_assemblies.csv')
VERTICES = os.path.join(CANON, 'structural_assembly_vertices.csv')
BLOCKS = os.path.join(CANON, 'wall_blocks.csv')

KNOWN_SCHEMA = {'1'}
KNOWN_KIND = {'monolithic_cast'}
KNOWN_STATUS = {'derived_from_vector_plan', 'measured_on_site',
                'owner_stated', 'provisional'}
# !! A required-and-non-empty check is not a vocabulary check. CODEX round 3
# passed `field_verified=maybe` straight through, because the field was only
# tested for presence. A tri-state that is meant to be a boolean is worse than
# a missing value: it reads as an answer.
KNOWN_FIELD_VERIFIED = {'yes', 'no'}
MIN_AREA_M2 = 1e-6

# !! Characters that make two strings LOOK equal and compare unequal, or that
# survive into a consumer and break it. CODEX round 4 passed a BOM-prefixed
# assembly id straight through by using it CONSISTENTLY in all three files:
# referential integrity held, every join matched, and the id was still wrong.
# Consistency is not validity. verify_batch.py has a BOM check, but it only
# scans files changed between two refs, so it is not the gate for this data.
INVISIBLE = tuple(chr(c) for c in (
    0xFEFF,   # BOM / zero-width no-break space
    0x200B,   # zero-width space
    0x200C,   # zero-width non-joiner
    0x200D,   # zero-width joiner
    0x00A0,   # no-break space -- looks exactly like a space and is not
    0x2060,   # word joiner
))
RESTKEY = '__extra_cells__'
AREA_TOL_M2 = 0.0005
REQUIRED_VERTEX_FIELDS = ('source_drawing', 'source_entity', 'status',
                          'field_verified')


def read(path):
    """Rows, or None if absent. Extra cells are CAPTURED, not swallowed.

    !! csv.DictReader silently drops cells with no header unless restkey is set,
    so a stray or mistyped column vanished without comment - CODEX round 4 got a
    PASS out of exactly that. Missing cells become None for the same reason and
    are equally invisible. Both are now visible to check_arity().
    """
    if not os.path.exists(path):
        return None
    with io.open(path, encoding='utf-8', newline='') as f:
        rdr = csv.DictReader(f, restkey=RESTKEY)
        return list(rdr)


def check_arity(path, rows):
    """Every row must have exactly the header's cells, and no invisibles."""
    problems = []
    name = os.path.basename(path)
    with io.open(path, 'rb') as f:
        head = f.read(3)
    if head.startswith(codecs.BOM_UTF8):
        problems.append('%s starts with a UTF-8 BOM' % name)
    for i, r in enumerate(rows or [], start=2):
        if RESTKEY in r:
            problems.append('%s line %d has %d undeclared extra cell(s): %r'
                            % (name, i, len(r[RESTKEY]), r[RESTKEY]))
        for k, v in r.items():
            if k == RESTKEY:
                continue
            if v is None:
                problems.append('%s line %d is missing a value for %r'
                                % (name, i, k))
                continue
            for ch in INVISIBLE:
                if ch in v:
                    problems.append('%s line %d field %r contains %r, an '
                                    'invisible character that makes values '
                                    'compare unequal while looking equal'
                                    % (name, i, k, ch))
            if any(ord(c) < 32 and c != chr(9) for c in v):
                problems.append('%s line %d field %r contains a control '
                                'character' % (name, i, k))
    return problems


def finite(value):
    """float(value) if it is a real, finite number - else None.

    !! float('nan') PARSES, so a try/except around float() is not a numeric
    check. Worse, every comparison against nan is False, so
    `abs(nan - recorded) > tol` silently reports agreement. CODEX round 3 got a
    PASS out of `x_mm=nan` that printed "area nan" while succeeding, and the
    same hole existed on footprint_area_m2. Non-finite input must be rejected at
    the parse, never compared.
    """
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def _seg_cross(a, b, c, d):
    """Do axis-aligned segments a-b and c-d touch anywhere?"""
    def rng(p, q, i):
        return (min(p[i], q[i]), max(p[i], q[i]))
    ax, ay = rng(a, b, 0), rng(a, b, 1)
    cx, cy = rng(c, d, 0), rng(c, d, 1)
    return (ax[0] <= cx[1] and cx[0] <= ax[1]
            and ay[0] <= cy[1] and cy[0] <= ay[1])


def is_simple(pts):
    """True if the closed rectilinear polygon does not touch or cross itself.

    !! The shoelace formula is happy to integrate a self-intersecting polygon,
    and the signed areas of the crossed lobes CANCEL - so a figure-eight can
    report a perfectly plausible total. CODEX round 4 built one whose area came
    out as a clean 18.0000 m2; reproducing it here gave 45.0000. Comparing a
    recomputed area against a recorded one therefore proves nothing about the
    shape unless the shape is known to be simple first.

    Only NON-ADJACENT edge pairs are tested: consecutive edges legitimately
    share exactly one endpoint.
    """
    n = len(pts)
    edges = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j == i or (j - i) % n == 1 or (i - j) % n == 1:
                continue
            if _seg_cross(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                return False, (i, j)
    return True, None


def shoelace_m2(pts):
    s = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0 / 1e6


def validate(assemblies_path=ASSEMBLIES, vertices_path=VERTICES,
             blocks_path=BLOCKS):
    problems = []

    blocks = read(blocks_path)
    if blocks is None:
        return ['wall_blocks.csv is missing']
    problems.extend(check_arity(blocks_path, blocks))
    wall_ids = set(r['wall_id'] for r in blocks)

    declared = {}
    for r in blocks:
        sid = (r.get('structural_element_id') or '').strip()
        if not sid:
            problems.append('%s: structural_element_id is blank; a singleton '
                            'must carry its own id' % r['wall_id'])
        elif sid != r['wall_id']:
            declared[r['wall_id']] = sid

    assemblies = read(assemblies_path)
    if assemblies is not None:
        problems.extend(check_arity(assemblies_path, assemblies))
    if assemblies is None:
        if declared:
            problems.append('walls %s declare an assembly but %s is missing'
                            % (sorted(declared), os.path.basename(assemblies_path)))
        return problems

    members = {}
    seen_ids = set()
    for a in assemblies:
        aid = (a.get('assembly_id') or '').strip()
        if not aid:
            problems.append('an assembly row has no assembly_id')
            continue
        # An explicit uniqueness check. A duplicate id was rejected before only
        # by ACCIDENT, via the wall-in-two-assemblies rule, and an accidental
        # rejection is not a check - the same standard this repo applies to
        # every other validator.
        if aid in seen_ids:
            problems.append('assembly_id %r appears more than once; ids must be '
                            'unique' % aid)
        seen_ids.add(aid)
        if (a.get('schema_version') or '').strip() not in KNOWN_SCHEMA:
            problems.append('%s: schema_version %r is not one of %s'
                            % (aid, a.get('schema_version'), sorted(KNOWN_SCHEMA)))
        if (a.get('kind') or '').strip() not in KNOWN_KIND:
            problems.append('%s: kind %r is not one of %s'
                            % (aid, a.get('kind'), sorted(KNOWN_KIND)))
        mem = [m.strip() for m in (a.get('member_walls') or '').split('|') if m.strip()]
        if len(mem) < 2:
            problems.append('%s: an assembly needs at least two member walls, got %r'
                            % (aid, mem))
        if len(set(mem)) != len(mem):
            problems.append('%s: member_walls repeats a wall: %r' % (aid, mem))
        for m in mem:
            if m not in wall_ids:
                problems.append('%s: member %r is not a wall in wall_blocks.csv'
                                % (aid, m))
            if m in members:
                problems.append('%s is a member of both %r and %r; a wall belongs '
                                'to at most one assembly' % (m, members[m], aid))
            else:
                members[m] = aid

    # both directions must agree
    for wid, sid in sorted(declared.items()):
        if members.get(wid) != sid:
            problems.append('%s declares structural_element_id %r but that '
                            'assembly does not list it' % (wid, sid))
    for wid, aid in sorted(members.items()):
        if declared.get(wid) != aid:
            problems.append('%s lists member %s, but the wall does not declare '
                            'that structural_element_id' % (aid, wid))

    verts = read(vertices_path)
    if verts is not None:
        problems.extend(check_arity(vertices_path, verts))
    if verts is None:
        problems.append('%s is missing; assembly footprints have no coordinates'
                        % os.path.basename(vertices_path))
        return problems

    by_asm = {}
    for v in verts:
        by_asm.setdefault((v.get('assembly_id') or '').strip(), []).append(v)

    for a in assemblies:
        aid = (a.get('assembly_id') or '').strip()
        rows = by_asm.get(aid)
        if not rows:
            problems.append('%s has no vertices' % aid)
            continue
        try:
            rows.sort(key=lambda r: int(r['vertex_index']))
        except (KeyError, ValueError):
            problems.append('%s: a vertex_index is missing or not an integer' % aid)
            continue
        idx = [int(r['vertex_index']) for r in rows]
        if idx != list(range(len(idx))):
            problems.append('%s: vertex_index must be contiguous from 0, got %r'
                            % (aid, idx))
        if len(rows) < 4:
            problems.append('%s: a footprint needs at least 4 vertices, got %d'
                            % (aid, len(rows)))
        pts = []
        for r in rows:
            x, y = finite(r.get('x_mm')), finite(r.get('y_mm'))
            if x is None or y is None:
                problems.append('%s vertex %s: x_mm/y_mm must be finite numbers, '
                                'got %r/%r' % (aid, r.get('vertex_index'),
                                               r.get('x_mm'), r.get('y_mm')))
            else:
                pts.append((x, y))
            for field in REQUIRED_VERTEX_FIELDS:
                if not (r.get(field) or '').strip():
                    problems.append('%s vertex %s: %s is empty; plan 4.6 requires '
                                    'provenance on every coordinate'
                                    % (aid, r.get('vertex_index'), field))
            st = (r.get('status') or '').strip()
            if st and st not in KNOWN_STATUS:
                problems.append('%s vertex %s: status %r is not one of %s'
                                % (aid, r.get('vertex_index'), st,
                                   sorted(KNOWN_STATUS)))
            fv = (r.get('field_verified') or '').strip()
            if fv and fv not in KNOWN_FIELD_VERIFIED:
                problems.append('%s vertex %s: field_verified %r is not one of '
                                '%s - a tri-state here would read as an answer'
                                % (aid, r.get('vertex_index'), fv,
                                   sorted(KNOWN_FIELD_VERIFIED)))
        if len(pts) != len(rows):
            continue
        if len(set(pts)) != len(pts):
            problems.append('%s: a footprint vertex is repeated' % aid)
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            if abs(x0 - x1) > 1e-6 and abs(y0 - y1) > 1e-6:
                problems.append('%s: edge %d->%d is neither horizontal nor '
                                'vertical (%.1f,%.1f)-(%.1f,%.1f); this model is '
                                'orthogonal' % (aid, i, (i + 1) % len(pts),
                                                x0, y0, x1, y1))
        simple, where = is_simple(pts)
        if not simple:
            problems.append('%s: the footprint touches or crosses itself at '
                            'edges %d and %d; a self-intersecting polygon can '
                            'still produce a plausible shoelace area, so the '
                            'area check cannot vouch for it' % (aid, where[0],
                                                                where[1]))
            continue
        got = shoelace_m2(pts)
        want = finite(a.get('footprint_area_m2'))
        if want is None:
            problems.append('%s: footprint_area_m2 must be a finite number, got %r'
                            % (aid, a.get('footprint_area_m2')))
            continue
        if got < MIN_AREA_M2 or want < MIN_AREA_M2:
            problems.append('%s: footprint area is degenerate (recomputed %.6f, '
                            'recorded %.6f); a solid must enclose area'
                            % (aid, got, want))
            continue
        if abs(got - want) > AREA_TOL_M2:
            problems.append('%s: footprint_area_m2 says %.4f, the vertices give '
                            '%.4f (tolerance %.4f)'
                            % (aid, want, got, AREA_TOL_M2))
        else:
            print('  %-12s %d vertices, area %.4f m2 recomputed (recorded %.4f)'
                  % (aid, len(pts), got, want))

    for aid in by_asm:
        if aid not in set((a.get('assembly_id') or '').strip() for a in assemblies):
            problems.append('vertices reference unknown assembly %r' % aid)

    return problems


def main():
    print('structural assemblies:')
    problems = validate()
    if problems:
        for p in problems:
            print('  FAIL %s' % p)
        print('\nFAIL - %d problem(s)' % len(problems))
        return 1
    print('\nPASS - members resolve both ways, footprints close, every '
          'coordinate carries provenance')
    return 0


if __name__ == '__main__':
    sys.exit(main())
