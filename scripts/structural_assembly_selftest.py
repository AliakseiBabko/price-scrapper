# -*- coding: utf-8 -*-
"""Prove the assembly and corner checks FAIL on the errors they exist to catch.

Why this exists
---------------
CODEX, round 2 of VECTOR_PLAN_TO_MODEL_EXTRACTION: *"the current checker does not
enforce what the generator produces... restoring G3 as owner of C_G3_R2 could
still PASS, and changing C_R1a_R1b back to kind = L could also PASS."* That was
true, and it is the worst kind of defect in a validator - a green result that
means nothing. A check nobody has watched fail is not yet a check.

So each case below breaks one thing in a COPY of the canonical data and asserts
the validator rejects it. Same intent as scripts/verify_batch_selftest.py, which
guards tools/verify_batch.py against over-suppression.

Usage
-----
    py -3 scripts/structural_assembly_selftest.py
"""
from __future__ import print_function

import csv
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'data', 'canonical')
TOOL = os.path.join(REPO, 'tools', 'layout', 'validate_structural_assemblies.py')
CORNERS = os.path.join(REPO, 'tools', 'layout', 'build_wall_corners.py')


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


VA = _load(TOOL, 'va')


def rows(path):
    with io.open(path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        return list(r.fieldnames), list(r)


def write(path, fields, data):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case('a member wall that does not exist')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs[0]['member_walls'] = 'R1a|NOPE'
    write(p, f, rs)


@case('a member that does not declare the assembly')
def _(d):
    p = os.path.join(d, 'wall_blocks.csv')
    f, rs = rows(p)
    for r in rs:
        if r['wall_id'] == 'R1b':
            r['structural_element_id'] = 'R1b'
    write(p, f, rs)


@case('a blank structural_element_id')
def _(d):
    p = os.path.join(d, 'wall_blocks.csv')
    f, rs = rows(p)
    for r in rs:
        if r['wall_id'] == 'R6':
            r['structural_element_id'] = ''
    write(p, f, rs)


@case('a footprint area that disagrees with its vertices')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs[0]['footprint_area_m2'] = '0.9000'
    write(p, f, rs)


@case('a vertex with no provenance')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[2]['source_entity'] = ''
    write(p, f, rs)


@case('a vertex with an unknown status')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[0]['status'] = 'looked_about_right'
    write(p, f, rs)


@case('a non-orthogonal footprint edge')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[3]['y_mm'] = '15000.0'
    write(p, f, rs)


@case('a gap in the vertex indices')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[4]['vertex_index'] = '9'
    write(p, f, rs)


@case('the assemblies file deleted while a wall still declares one')
def _(d):
    os.remove(os.path.join(d, 'structural_assemblies.csv'))


@case('an unknown schema_version')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs[0]['schema_version'] = '99'
    write(p, f, rs)


def run_assembly_cases():
    ok = True
    for name, mutate in CASES:
        d = tempfile.mkdtemp()
        try:
            for fn in ('structural_assemblies.csv',
                       'structural_assembly_vertices.csv', 'wall_blocks.csv'):
                shutil.copy(os.path.join(CANON, fn), os.path.join(d, fn))
            mutate(d)
            problems = VA.validate(
                os.path.join(d, 'structural_assemblies.csv'),
                os.path.join(d, 'structural_assembly_vertices.csv'),
                os.path.join(d, 'wall_blocks.csv'))
            if problems:
                print('  ok      rejected: %s' % name)
            else:
                print('  FAILED  ACCEPTED: %s' % name)
                ok = False
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return ok


# --- added after CODEX round 3 found each of these PASSING ------------------
# The lesson generalises: "the field is present" and "float() did not raise" are
# both weaker than they look. A vocabulary field needs its vocabulary checked,
# and nan parses fine while defeating every comparison it appears in.


@case('field_verified with a value outside its vocabulary')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[0]['field_verified'] = 'maybe'
    write(p, f, rs)


@case('a non-finite vertex coordinate (nan), which made the area nan and PASSED')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[0]['x_mm'] = 'nan'
    write(p, f, rs)


@case('a non-finite recorded footprint area (nan)')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs[0]['footprint_area_m2'] = 'nan'
    write(p, f, rs)


@case('an infinite vertex coordinate')
def _(d):
    p = os.path.join(d, 'structural_assembly_vertices.csv')
    f, rs = rows(p)
    rs[1]['y_mm'] = 'inf'
    write(p, f, rs)


@case('a duplicate assembly_id')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs.append(dict(rs[0]))
    write(p, f, rs)


@case('a degenerate zero-area footprint whose recorded area agrees')
def _(d):
    p = os.path.join(d, 'structural_assemblies.csv')
    f, rs = rows(p)
    rs[0]['footprint_area_m2'] = '0'
    write(p, f, rs)
    p2 = os.path.join(d, 'structural_assembly_vertices.csv')
    f2, rs2 = rows(p2)
    for i, r in enumerate(rs2):
        r['x_mm'] = '2980.9'
        r['y_mm'] = '%.1f' % (14645.3 + i)      # distinct points, zero area
    write(p2, f2, rs2)


LEDGER = os.path.join(CANON, 'wall_corners.csv')

CORNER_CASES = [
    ('the old G3 contradiction: G3 restored as owner of C_G3_R2',
     'C_G3_R2', 'owner', 'G3'),
    ('C_R1a_R1b flipped back to a construction joint',
     'C_R1a_R1b', 'kind', 'L'),
    ('a corner note replaced with something plausible but wrong',
     'C_MA_R8', 'note', 'MA and R8 meet at a corner.'),
    ('an owner gain that does not match the geometry',
     'C_MB_R9', 'owner_gains_mm', '250'),
]


def run_corner_cases():
    """build_wall_corners.py must reject a tampered ledger. Run as a subprocess
    because the tool reads the canonical path directly, so the file is restored
    from git afterwards rather than pointed elsewhere."""
    ok = True
    original = io.open(LEDGER, encoding='utf-8').read()
    try:
        for name, cid, field, bad in CORNER_CASES:
            f, rs = rows(LEDGER)
            hit = False
            for r in rs:
                if r['corner_id'] == cid:
                    r[field] = bad
                    hit = True
            if not hit:
                print('  SKIP    %s (%s not in the ledger)' % (name, cid))
                continue
            write(LEDGER, f, rs)
            rc = subprocess.call([sys.executable, CORNERS],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            if rc != 0:
                print('  ok      rejected: %s' % name)
            else:
                print('  FAILED  ACCEPTED: %s' % name)
                ok = False
    finally:
        with io.open(LEDGER, 'w', encoding='utf-8', newline='') as fh:
            fh.write(original)
    return ok


def main():
    print('assembly validator - negative cases:')
    a = run_assembly_cases()
    print('\ncorner ledger - negative cases:')
    b = run_corner_cases()
    print('\nledger restored; canonical data unchanged')
    if a and b:
        print('\nPASS - every seeded defect was rejected')
        return 0
    print('\nFAIL - a seeded defect was accepted')
    return 1


if __name__ == '__main__':
    sys.exit(main())
