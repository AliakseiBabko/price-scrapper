# -*- coding: utf-8 -*-
"""Check each room's INTERNAL rollout (развёртка) and report its elevation area.

Why this exists, and why it is separate from the wall model
-----------------------------------------------------------
Owner, 2026-09-04: "The length of a wall section lets us construct the framework
of the apartment. But a slightly different question is the inner walls... for
each room we need the rollout of all of the walls, to calculate the total area,
to design the wall in different parts. Walls with the thickness is good for
building the framework, but we need also internal dimensions. How are we gonna
store the data per room?"

Two different models, and conflating them is what made the earlier room-face
schedule unusable:

  wall_blocks.csv     the FRAMEWORK. One row per wall: material, thickness,
                      clear length, solid length, the corners it owns. Answers
                      "what is built and how much of it".

  room_rollouts.csv   the ROLLOUT. One row per internal FACE, in walk order
                      around a room. Answers "what does a person standing in
                      this room see, and what has to be finished".

A face is not a wall. One wall contributes a face to two different rooms, at two
different lengths; a shaft and a plumbing block contribute faces but are not
walls at all; and a STEP - the 175 mm where a 250 concrete column projects past
the 75 partition continuing its line - is a face with no wall of its own. The
owner walked exactly this in the living room and named every step.

What this checks
----------------
1. The loop CLOSES: going round a room, the eastward lengths must equal the
   westward, and the northward the southward. A rollout that does not close has
   a missing or mismeasured face - usually a step.
2. Reports the gross elevation area, the opening area, and the net finish area.

Areas here are DERIVED from linear dimensions and a height. They are never typed
in and never read off a plan - see the standing rule that areas are not evidence.

    py -3 tools/layout/check_room_rollout.py
"""
from __future__ import print_function

import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.tabular import (check_unique, check_vocabulary,  # noqa: E402
                         finite, read_csv)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ROLL = os.path.join(REPO, 'data', 'canonical', 'room_rollouts.csv')
CLOSE_TOL_MM = 50.0        # the BUILD tolerance; see Geometry_Variance_Study.md

OPP = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}

# Closed vocabularies. !! Seeded 2026-09-09: `kind` misspelled as 'openning'
# was ACCEPTED, and it silently turned an opening into finishable wall area -
# inflating the finishable figure this tool exists to report, with no error and
# a perfectly plausible total. A presence check cannot see that; only a
# vocabulary can.
KINDS = {'wall_face', 'step', 'opening', 'shaft_face', 'plumbing_face'}
DIRECTIONS = set(OPP)


def load():
    """Rooms, or exit non-zero if the file is not fit to add up.

    Three checks that were absent until 2026-09-09, each demonstrated by a seed
    the old version accepted: the file's SHAPE (a stray cell was dropped, a
    missing one became None), the two VOCABULARIES, and the UNIQUENESS of
    room_id+seq - seq is the walk order round the room, so a duplicate makes the
    order ambiguous and the sort arbitrary.
    """
    rows, problems = read_csv(ROLL, strict=False)
    problems += check_vocabulary(ROLL, rows, 'kind', KINDS)
    problems += check_vocabulary(ROLL, rows, 'direction', DIRECTIONS)
    problems += check_unique(ROLL, rows, ('room_id', 'seq'))
    for i, r in enumerate(rows, start=2):
        for col in ('length_mm', 'height_mm'):
            if finite(r.get(col)) is None:
                problems.append('%s line %d: %s = %r is not a finite number'
                                % (os.path.basename(ROLL), i, col, r.get(col)))
    if problems:
        print('FAIL - room_rollouts.csv is not fit to add up:')
        for p in problems:
            print('  %s' % p)
        sys.exit(1)

    rooms = collections.OrderedDict()
    for r in rows:
        rooms.setdefault(r['room_id'], []).append(r)
    for k in rooms:
        rooms[k].sort(key=lambda r: int(r['seq']))
    return rooms


def main():
    if not os.path.exists(ROLL):
        print('missing %s' % ROLL)
        return 2
    rooms = load()
    bad = 0
    for rid, faces in rooms.items():
        axis = collections.Counter()
        gross = opening = 0.0
        for r in faces:
            L = float(r['length_mm'])
            H = float(r['height_mm'])
            axis[r['direction']] += L
            if r['kind'] == 'opening':
                opening += L * H
            else:
                gross += L * H
        print('room %s - %d faces' % (rid, len(faces)))
        for a, b in (('E', 'W'), ('N', 'S')):
            d = axis[a] - axis[b]
            ok = abs(d) <= CLOSE_TOL_MM
            print('   %s %6.0f  vs  %s %6.0f   -> %s%s'
                  % (a, axis[a], b, axis[b],
                     'CLOSES' if ok else 'residual %+.0f mm' % d,
                     ' (EXACT)' if d == 0 else ''))
            if not ok:
                bad += 1
        print('   perimeter of finishable faces  %6.0f mm' % sum(
            float(r['length_mm']) for r in faces if r['kind'] != 'opening'))
        print('   FINISHABLE face area  %6.2f m2   at %s mm clear height'
              % (gross / 1e6, faces[0]['height_mm']))
        print('   full-height openings  %6.2f m2   (nothing to finish)'
              % (opening / 1e6))
        print('   -> whole envelope     %6.2f m2' % ((gross + opening) / 1e6))
        steps = [r for r in faces if r['kind'] == 'step']
        if steps:
            print('   includes %d step face(s): %s'
                  % (len(steps), ', '.join('%s %s' % (r['face_id'],
                                                      r['length_mm']) for r in steps)))
        print()
    if bad:
        print('%d axis(es) do not close within %.0f mm. A rollout that does not '
              'close has a missing or mismeasured face - look for a STEP first.'
              % (bad, CLOSE_TOL_MM))
        return 1
    print('PASS - every room rollout closes on both axes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
