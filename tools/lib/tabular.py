# -*- coding: utf-8 -*-
"""Strict CSV reading and numeric parsing, shared so the same holes stop recurring.

Where this came from
--------------------
Five adversarial review rounds against ONE validator (the
`VECTOR_PLAN_TO_MODEL_EXTRACTION` dialogue, closed 2026-09-09) found the same two
failure families over and over. They are not bugs in one tool; they are two
idioms that look like validation and are not:

  1. **`float(x)` not raising does not mean the number is usable.**
     `float('nan')` parses. And every comparison against nan is False, so a test
     written as `if abs(got - want) > tol: complain` reports AGREEMENT on nan
     input - it is structurally incapable of failing. Polarity decides whether a
     nan is caught or swallowed, which is far too subtle to leave to each call
     site: `check_room_rollout.py` happens to reject nan because its test is
     `ok = abs(d) <= tol`, while `cost_rollup.py` happily printed a bottom line
     of "nan-nan BYN".

  2. **`csv.DictReader` hides both a stray cell and a missing one.**
     Extra cells are dropped unless `restkey` is set; missing cells silently
     become `None`. At the time of writing exactly ONE of the ~20 DictReader call
     sites in this repository passed `restkey`.

Also caught here, because it defeats every cross-reference check: an identifier
carrying an invisible character. A BOM inside an id, used CONSISTENTLY in every
file, satisfies every join because both sides are equally wrong. **Consistency is
not validity**, and `tools/verify_batch.py` does not cover it - that scans only
files changed between two refs, so it is not the gate for data already committed.

Usage
-----
    from tools.lib.tabular import read_csv, finite, ValidationError

    rows = read_csv(path)                       # raises on a malformed file
    rows, problems = read_csv(path, strict=False)   # or collect and decide

    v = finite(row['qty'])
    if v is None:
        ...  # not a usable number: nan, inf, empty or text
"""
from __future__ import print_function

import codecs
import csv
import io
import math
import os

RESTKEY = '__extra_cells__'

INVISIBLE = tuple(chr(c) for c in (
    0xFEFF,   # BOM / zero-width no-break space
    0x200B,   # zero-width space
    0x200C,   # zero-width non-joiner
    0x200D,   # zero-width joiner
    0x00A0,   # no-break space -- looks exactly like a space and is not
    0x2060,   # word joiner
))


class ValidationError(Exception):
    """A tabular file is malformed in a way that must not be worked around."""


def finite(value):
    """float(value) if it is a real, finite number - else None.

    Use this instead of `float()` wherever the result reaches a comparison. A
    nan does not merely give a wrong answer; it makes the comparison itself
    meaningless, and which way it falls depends on whether the test is written
    positively or negatively.
    """
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def check_file(path, rows):
    """Problems with a file's SHAPE and characters, independent of its meaning."""
    problems = []
    name = os.path.basename(path)
    with io.open(path, 'rb') as f:
        if f.read(3).startswith(codecs.BOM_UTF8):
            problems.append('%s starts with a UTF-8 BOM' % name)
    for i, r in enumerate(rows or [], start=2):
        if RESTKEY in r:
            problems.append('%s line %d has %d undeclared extra cell(s): %r'
                            % (name, i, len(r[RESTKEY]), r[RESTKEY]))
        for k, v in r.items():
            if k == RESTKEY:
                continue
            if v is None:
                problems.append('%s line %d is missing a value for %r' % (name, i, k))
                continue
            for ch in INVISIBLE:
                if ch in v:
                    problems.append('%s line %d field %r contains U+%04X, an '
                                    'invisible character - it makes values compare '
                                    'unequal while looking equal'
                                    % (name, i, k, ord(ch)))
            if any(ord(c) < 32 and c != chr(9) for c in v):
                problems.append('%s line %d field %r contains a control character'
                                % (name, i, k))
    return problems


def read_csv(path, strict=True, required=None):
    """Rows from a CSV, with extra and missing cells VISIBLE.

    `required` names columns that must exist in the header. With `strict`, any
    problem raises ValidationError; otherwise returns `(rows, problems)`.
    """
    with io.open(path, encoding='utf-8', newline='') as f:
        rdr = csv.DictReader(f, restkey=RESTKEY)
        rows = list(rdr)
        fields = list(rdr.fieldnames or [])
    problems = check_file(path, rows)
    for col in (required or ()):
        if col not in fields:
            problems.append('%s has no %r column (found %r)'
                            % (os.path.basename(path), col, fields))
    if strict and problems:
        raise ValidationError('%s:\n  %s' % (path, '\n  '.join(problems)))
    return rows if strict else (rows, problems)


def check_vocabulary(path, rows, column, allowed):
    """A column whose values must come from a closed set.

    A misspelling here is the quietest defect of all: `kind = 'openning'` on a
    room-rollout face turned an opening into finishable wall area, with no error
    and a plausible total. A presence check would not have caught it.
    """
    problems = []
    name = os.path.basename(path)
    for i, r in enumerate(rows or [], start=2):
        v = (r.get(column) or '').strip()
        if v not in allowed:
            problems.append('%s line %d: %s = %r is not one of %s'
                            % (name, i, column, v, sorted(allowed)))
    return problems


def check_unique(path, rows, columns):
    """A key that must not repeat. `columns` is a tuple naming the composite."""
    problems = []
    name = os.path.basename(path)
    seen = {}
    for i, r in enumerate(rows or [], start=2):
        key = tuple((r.get(c) or '').strip() for c in columns)
        if key in seen:
            problems.append('%s line %d repeats %s = %r, first seen on line %d'
                            % (name, i, '+'.join(columns), key, seen[key]))
        else:
            seen[key] = i
    return problems
