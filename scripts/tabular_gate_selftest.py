# -*- coding: utf-8 -*-
"""Prove the rollout and cost-rollup gates fail on the defects they now catch.

Where these seeds came from
---------------------------
The `VECTOR_PLAN_TO_MODEL_EXTRACTION` dialogue closed with a non-blocking
follow-up (plan 4.10): the two failure families it kept finding in one validator
were likely to exist elsewhere, and three surfaces had never been seeded. This is
the first slice of that audit, run 2026-09-09 on the two with the most
consequence - the money one and a standing geometry check.

What the seeds actually found, before any fix
---------------------------------------------
  cost_rollup.py    qty = "nan" in bom.csv  ->  EXIT 0, and the bottom line
                    printed "Extended total of what is currently priceable:
                    nan-nan BYN". float("nan") parses, so the try/except
                    ValueError around it never fired.
                    An undeclared extra CSV cell -> EXIT 0.

  check_room_rollout.py   kind misspelled "openning" -> EXIT 0, silently moving
                    an opening into the finishable wall area this tool exists to
                    report. An extra cell -> EXIT 0. A duplicate seq -> EXIT 0.

And one prediction that was WRONG, recorded because it matters:
                    a nan LENGTH was already rejected. The closure test is
                    written `ok = abs(d) <= tol`, and nan makes that False, so it
                    failed. The area check in the assembly validator used the
                    opposite polarity - `if abs(got - want) > tol: complain` -
                    and nan made THAT False too, which passed. **Whether a nan is
                    caught or swallowed depends on how the comparison is
                    written**, which is exactly why the guard belongs in a shared
                    helper and not at each call site.

Usage
-----
    py -3 scripts/tabular_gate_selftest.py
"""
from __future__ import print_function

import csv
import io
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROLL = os.path.join(REPO, 'data', 'canonical', 'room_rollouts.csv')
BOM = os.path.join(REPO, 'data', 'procurement', 'bom.csv')
QUOTES = os.path.join(REPO, 'data', 'procurement', 'quotes.csv')
ROLLOUT_TOOL = os.path.join(REPO, 'tools', 'layout', 'check_room_rollout.py')
COST_TOOL = os.path.join(REPO, 'tools', 'procurement', 'cost_rollup.py')

NL = chr(10)


def rows(path):
    with io.open(path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        return list(r.fieldnames), list(r)


def write(path, fields, data):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)


def add_extra_cell(path):
    lines = io.open(path, encoding='utf-8').read().rstrip(NL).split(NL)
    lines[1] += ',SURPRISE'
    io.open(path, 'w', encoding='utf-8', newline='').write(NL.join(lines) + NL)


def run(tool):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, tool], cwd=REPO, env=env,
                       capture_output=True, text=True, errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def probe(label, path, tool, mutate):
    """Seed one defect, run the tool, restore the file. True if it was rejected."""
    backup = io.open(path, encoding='utf-8', newline='').read()
    try:
        mutate(path)
        rc, out = run(tool)
        nan = 'nan' in out.lower()
        if rc != 0:
            print('  ok      rejected: %s' % label)
            return True
        print('  FAILED  ACCEPTED: %s%s' % (label, '  [and printed nan]' if nan else ''))
        return False
    finally:
        io.open(path, 'w', encoding='utf-8', newline='').write(backup)


def rollout_cases():
    def kind_typo(p):
        f, d = rows(p)
        for r in d:
            if r['kind'] == 'opening':
                r['kind'] = 'openning'
                break
        write(p, f, d)

    def bad_direction(p):
        f, d = rows(p)
        d[0]['direction'] = 'X'
        write(p, f, d)

    def dup_seq(p):
        f, d = rows(p)
        d[1]['seq'] = d[0]['seq']
        write(p, f, d)

    def nan_length(p):
        f, d = rows(p)
        d[0]['length_mm'] = 'nan'
        write(p, f, d)

    def blank_height(p):
        f, d = rows(p)
        d[0]['height_mm'] = ''
        write(p, f, d)

    def nbsp_room(p):
        f, d = rows(p)
        d[0]['room_id'] = d[0]['room_id'] + chr(0x00A0)
        write(p, f, d)

    return [
        ('kind misspelled "openning" - an opening became finishable area', kind_typo),
        ('a direction in neither axis pair', bad_direction),
        ('a duplicate room_id+seq, making the walk order ambiguous', dup_seq),
        ('a nan length', nan_length),
        ('a blank height', blank_height),
        ('a no-break space appended to room_id', nbsp_room),
        ('an undeclared extra CSV cell', add_extra_cell),
    ]


def cost_cases():
    def nan_qty(p):
        f, d = rows(p)
        d[0]['qty'] = 'nan'
        write(p, f, d)

    def inf_qty(p):
        f, d = rows(p)
        d[0]['qty'] = 'inf'
        write(p, f, d)

    def nan_rate(p):
        f, d = rows(p)
        d[0]['rate_expected'] = 'nan'
        write(p, f, d)

    def dup_key(p):
        f, d = rows(p)
        d[1]['key'] = d[0]['key']
        write(p, f, d)

    return [
        ('a nan qty, which used to print a "nan-nan BYN" total', nan_qty),
        ('an inf qty', inf_qty),
        ('a nan rate_expected', nan_rate),
        ('a duplicate bom key', dup_key),
        ('an undeclared extra CSV cell', add_extra_cell),
    ]


def main():
    ok = True
    print('room_rollouts.csv / check_room_rollout.py')
    for label, fn in rollout_cases():
        ok = probe(label, ROLL, ROLLOUT_TOOL, fn) and ok

    if os.path.exists(BOM):
        print()
        print('bom.csv / cost_rollup.py')
        for label, fn in cost_cases():
            ok = probe(label, BOM, COST_TOOL, fn) and ok
        if os.path.exists(QUOTES):
            def nan_quote_rate(p):
                # !! quotes.csv is header-only in the repository today, so a
                # mutate-the-first-row seed silently changed nothing and the
                # case reported a false ACCEPT. That was the TEST being wrong,
                # not the tool - a reminder that a negative case which does not
                # actually alter the input proves nothing. So synthesise a row.
                f, d = rows(p)
                bf, bd = rows(BOM)
                d.append({
                    'bom_key': bd[0]['key'] if bd else 'TEST-01',
                    'source': 'selftest',
                    'quote_date': '2026-09-09',
                    'valid_until': '2099-01-01',
                    'rate_material': '10',
                    'rate_labour': 'nan',
                    'rate_unit': 'm2',
                    'currency': 'BYN',
                    'scope_note': 'seeded by scripts/tabular_gate_selftest.py',
                    'status': 'received',
                })
                write(p, f, d)
            print()
            print('quotes.csv / cost_rollup.py')
            ok = probe('a nan rate_labour in a quote', QUOTES, COST_TOOL,
                       nan_quote_rate) and ok

    print()
    for path in (ROLL, BOM, QUOTES):
        if os.path.exists(path):
            print('restored %s' % os.path.relpath(path, REPO))
    if ok:
        print()
        print('PASS - every seeded defect was rejected')
        return 0
    print()
    print('FAIL - a seeded defect was accepted')
    return 1


if __name__ == '__main__':
    sys.exit(main())
