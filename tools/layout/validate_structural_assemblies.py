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

import csv
import io
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
AREA_TOL_M2 = 0.0005
REQUIRED_VERTEX_FIELDS = ('source_drawing', 'source_entity', 'status',
                          'field_verified')


def read(path):
    if not os.path.exists(path):
        return None
    with io.open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


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
    if assemblies is None:
        if declared:
            problems.append('walls %s declare an assembly but %s is missing'
                            % (sorted(declared), os.path.basename(assemblies_path)))
        return problems

    members = {}
    for a in assemblies:
        aid = (a.get('assembly_id') or '').strip()
        if not aid:
            problems.append('an assembly row has no assembly_id')
            continue
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
            try:
                pts.append((float(r['x_mm']), float(r['y_mm'])))
            except (KeyError, ValueError):
                problems.append('%s vertex %s: x_mm/y_mm not numeric'
                                % (aid, r.get('vertex_index')))
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
        got = shoelace_m2(pts)
        try:
            want = float(a['footprint_area_m2'])
        except (KeyError, ValueError):
            problems.append('%s: footprint_area_m2 missing or not numeric' % aid)
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
