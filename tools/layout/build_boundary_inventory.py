#!/usr/bin/env python3
"""The IN-SCOPE BOUNDARY FACE INVENTORY, built from the compiler, not the patches.

⚠️⚠️ WHY THIS FILE EXISTS AT ALL
--------------------------------
`check_boundary_patches.py` asserts that every in-scope boundary surface is
covered. If the patch file also decided WHICH surfaces are in scope, that check
would be circular — the patches would define the thing they are measured
against, and a face nobody thought about would simply never be in scope.

So the inventory is a SEPARATE record with a SEPARATE origin:

    the compiler's resolved faces   →   every face that physically exists
    authored classification         →   which of them bound the apartment

⚠⚠ WHAT THIS PROVES, EXACTLY: **the inventory is complete, the
classification is not.** Every face the compiler resolves appears here, so no
face is missing because nobody typed it. That is NOT the same as knowing every
envelope face has been IDENTIFIED - 94 of 102 currently say `unknown`, and a
newly created envelope face arrives `unknown` and blocks nothing. Do not read a
passing run as "every boundary is understood".

⚠️ THE SKELETON IS GENERATED, THE CLASSIFICATION IS AUTHORED. This tool emits
one row per face the compiler actually resolves, so a face cannot be missing
because nobody typed it. It never invents a classification: a new face arrives
as `unknown`, and an existing row's `in_scope`, `reason` and `evidence` are
PRESERVED verbatim.

⚠️⚠️ AND IT REFUSES TO DROP AN AUTHORED ROW. If a face disappears from the
compiler while carrying an authored classification, that is a geometry change
somebody needs to look at, not a row to delete silently. The MC end-cap defect
was exactly this shape: a conclusion that depended on what was NOT in the model.

    .venv-ifc314\\Scripts\\python.exe tools/layout/build_boundary_inventory.py [--write]
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.tabular import read_csv  # noqa: E402

INVENTORY = os.path.join(REPO, "data", "canonical", "boundary_face_inventory.csv")

FIELDS = ["host_id", "face_ref", "length_mm", "in_scope", "reason", "evidence"]

# ⚠️ A CLOSED VOCABULARY. `unknown` is legal and is the honest default - it
# states that nobody has classified this face yet, which is a different claim
# from `internal`. What it must never do is make a face generator-eligible.
IN_SCOPE = ("envelope", "internal", "unknown")


def compiler_faces():
    """(host_id, face_ref, length_mm) for every face the compiler resolves."""
    from resolve_v0_geometry import resolve
    resolved = resolve()
    rows = []
    for wall in resolved.walls:
        host = wall["wall_id"]
        for face_ref, record in sorted(resolved.faces.get(host, {}).items()):
            rows.append((host, face_ref, round(record["length_mm"], 1)))
    rows.sort()
    return rows


def load(path=INVENTORY):
    if not os.path.exists(path):
        return {}
    return dict(((r["host_id"], r["face_ref"]), r)
                for r in read_csv(path, required=FIELDS))


def build(path=INVENTORY):
    """Returns (rows, problems). Problems are never written around."""
    existing = load(path)
    faces = compiler_faces()
    present = set((h, f) for h, f, _length in faces)
    problems = []

    for key, row in sorted(existing.items()):
        if key in present:
            continue
        if (row.get("in_scope") or "unknown") != "unknown":
            problems.append(
                "%s.%s carries an AUTHORED classification (%s) but the compiler "
                "no longer resolves that face. A conclusion that depends on "
                "what is not in the model is how MC's end cap went wrong - "
                "look at the geometry change, do not delete the row"
                % (key[0], key[1], row.get("in_scope")))

    rows = []
    for host, face_ref, length in faces:
        row = existing.get((host, face_ref))
        if row is None:
            rows.append({"host_id": host, "face_ref": face_ref,
                         "length_mm": length, "in_scope": "unknown",
                         "reason": "not yet classified", "evidence": ""})
            continue
        state = (row.get("in_scope") or "").strip()
        if state not in IN_SCOPE:
            problems.append("%s.%s has in_scope %r, which is not one of %s"
                            % (host, face_ref, state, ", ".join(IN_SCOPE)))
        if state == "envelope" and not (row.get("evidence") or "").strip():
            problems.append(
                "%s.%s is classified `envelope` with no evidence. An envelope "
                "face drives insulation and party-wall decisions; a confident "
                "label nobody looked at is worse than `unknown`"
                % (host, face_ref))
        rows.append({"host_id": host, "face_ref": face_ref,
                     "length_mm": length,
                     "in_scope": state or "unknown",
                     "reason": row.get("reason") or "",
                     "evidence": row.get("evidence") or ""})
    return rows, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--path", default=INVENTORY)
    a = ap.parse_args()

    rows, problems = build(a.path)
    for problem in problems:
        print("FAIL %s" % problem)
    counts = {}
    for row in rows:
        counts[row["in_scope"]] = counts.get(row["in_scope"], 0) + 1
    print("%d face(s): %s" % (len(rows), ", ".join(
        "%s %d" % (k, counts[k]) for k in sorted(counts))))
    if problems:
        print("FAILED: %d problem(s)" % len(problems))
        return 1
    if a.write:
        with io.open(a.path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print("wrote %s" % os.path.relpath(a.path, REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
