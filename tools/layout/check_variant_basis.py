#!/usr/bin/env python3
"""Two variants may only be differenced on ONE basis. This decides whether they are.

⚠️⚠️ THE FAILURE THIS PREVENTS IS A DELTA BETWEEN TWO DIFFERENT BUILDINGS
-------------------------------------------------------------------------
`v0` was an early schematic and `v1` is built on `current_apartment_shell.json`
plus absolute Homestyler walls. Each carries its OWN reconstruction of the same
structural shell, and their extents differ by ~200–260 mm — more than the
±50 mm build tolerance. So every number in the old comparison mixed a LAYOUT
decision with two independent reconstructions, and no amount of care reading
the sheet could separate them.

Rebuilding `v0` alone would have repaired the visible defect and left
"single-basis" false, which is why this gate exists before any delta is
computed rather than after.

⚠️ WHAT MUST MATCH, AND WHAT MUST NOT
  frame                MUST — the compiler-published coordinate datum
  shell_signature      MUST — RC frame, façade, loggia enclosure, shafts
  partitions           MUST NOT — they are what a variant is allowed to change

⚠️⚠️ AND A REBASE IS NOT A TRANSFORM. v1's shell is not v0's shell translated;
it is a different reconstruction. Registering it by least-squares would invent
agreement that the evidence does not support. v1's PARTITIONS have to be
re-expressed against the resolved shell, and that is authoring work, not
arithmetic. This gate refuses until that is done; it does not do it.

    .venv-ifc314\\Scripts\\python.exe tools/layout/check_variant_basis.py
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VARIANTS = os.path.join(REPO, "data", "outputs", "variants")

RETAINED, DEMOLISHED, NEW = "retained", "demolished", "new"

# How far two polygons may differ and still be the same wall. Well inside the
# +30/-45 mm build tolerance, because this compares two COMPILED descriptions
# of one element, not two measurements of one wall.
SAME_WALL_MM = 5.0


def load(variant_id):
    path = os.path.join(VARIANTS, variant_id, "spec.json")
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def basis_problems(a, b):
    """Why these two specs may NOT be differenced. Empty means they may."""
    problems = []
    # ⚠⚠ A REFERENCE-ONLY SPEC IS NEVER A COMPARISON OPERAND, and this is
    # a PERMANENT state rather than a blocker to clear. v1 is a freehand sketch
    # made in Homestyler over the same constructor raster v0 came from, before
    # any model existed - the owner's own description. Rebasing it would have
    # manufactured precision that was never in the source.
    for spec in (a, b):
        if (spec.get("status") or "") == "reference_only":
            problems.append(
                "%s is REFERENCE ONLY - a design-intent source, not a measured "
                "variant. Its ideas are carried in "
                "data/canonical/design_intents.csv; its coordinates are not "
                "evidence and may not be differenced against anything"
                % spec.get("spec_id", "?"))
    for spec in (a, b):
        vid = spec.get("spec_id", "?")
        if "_retired" in spec:
            problems.append(
                "%s is RETIRED (%s) - a comparison may not depend on a "
                "superseded file anywhere in its chain"
                % (vid, str(spec["_retired"])[:60]))
        # ⚠ The legacy specs carry a dotted string ("0.1.0"), so this must
        # not assume an int - and a version it cannot parse is treated as too
        # old rather than skipped.
        raw = str(spec.get("schema_version") or "0").split(".")[0]
        version = int(raw) if raw.isdigit() else 0
        if version < 2:
            problems.append(
                "%s is schema v%s. v2 carries real POLYGONS; the v1 "
                "`horizontal + length + thickness` rectangle cannot represent "
                "the mitred M2/M6b geometry and squares it silently"
                % (vid, spec.get("schema_version")))
        if not spec.get("frame"):
            problems.append("%s publishes no coordinate frame, so its "
                            "coordinates mean nothing outside itself" % vid)
        if not spec.get("shell_signature"):
            problems.append("%s has no shell signature" % vid)

    if a.get("frame") and b.get("frame") and a["frame"] != b["frame"]:
        problems.append(
            "the two variants do not share a coordinate frame, so a difference "
            "between their coordinates is not a difference between layouts")
    if (a.get("shell_signature") and b.get("shell_signature")
            and a["shell_signature"] != b["shell_signature"]):
        problems.append(
            "the STRUCTURAL SHELLS differ (%s vs %s). The RC frame, façade, "
            "loggia enclosure and shafts are common property and identical in "
            "both variants by definition - if the signatures disagree, the two "
            "files describe different reconstructions of the same building and "
            "any delta mixes that in"
            % (str(a["shell_signature"])[:12], str(b["shell_signature"])[:12]))
    return problems


def _key(wall):
    """A wall's geometric identity, rounded so float noise is not a difference."""
    return tuple(sorted((round(x / SAME_WALL_MM), round(y / SAME_WALL_MM))
                        for x, y in wall.get("polygon_mm") or []))


def classify(base, proposed):
    """Every wall as retained / demolished / new. Raises unless the basis holds.

    ⚠️⚠️ THIS IS THE QUESTION THE OLD COMPARISON COULD NOT ANSWER. v1's
    operations add partitions with `phase: existing`, so the tool could not say
    which DEVELOPER partitions are being demolished - and demolition is the
    cost. A wall's phase in a variant file is an authoring artefact; its
    classification is a RELATION to the baseline and is computed here.
    """
    problems = basis_problems(base, proposed)
    if problems:
        raise ValueError(
            "the two variants are not on one basis, so retained/demolished/new "
            "cannot be computed: %s" % "; ".join(problems))

    base_walls = dict((_key(w), w) for w in base.get("walls", []))
    out = []
    seen = set()
    for wall in proposed.get("walls", []):
        key = _key(wall)
        if key in base_walls:
            seen.add(key)
            out.append((RETAINED, wall["id"], base_walls[key]["id"]))
        else:
            out.append((NEW, wall["id"], None))
    for key, wall in base_walls.items():
        if key in seen:
            continue
        if wall.get("structural"):
            # ⚠️ A structural wall cannot be demolished by a layout variant.
            # If one is missing from the proposal that is a DEFECT in the
            # proposal, not a demolition, and it is reported as such.
            out.append(("MISSING_STRUCTURAL", None, wall["id"]))
        else:
            out.append((DEMOLISHED, None, wall["id"]))
    return out


def area_comparable(a, b):
    """Room areas may be differenced only if BOTH derive them the same way."""
    methods = (a.get("area_method"), b.get("area_method"))
    if None in methods:
        return False, ("at least one variant does not state HOW its room areas "
                       "were obtained, so a delta between them is not a "
                       "measurement of anything")
    if methods[0] != methods[1]:
        return False, ("areas come from different methods (%s vs %s) - v0's "
                       "were the developer's published figures and v1's are "
                       "Homestyler's own computation, and every delta mixing "
                       "them is withdrawn" % methods)
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default="v0-existing")
    ap.add_argument("--proposed", default="v1-homestyler")
    a = ap.parse_args()

    base, proposed = load(a.base), load(a.proposed)
    problems = basis_problems(base, proposed)
    for problem in problems:
        print("FAIL %s" % problem)

    ok, why = area_comparable(base, proposed)
    print("room-area deltas: %s%s"
          % ("comparable" if ok else "WITHHELD", "" if ok else " - " + why))

    if problems:
        print("\nNOT ONE BASIS: %d problem(s). No delta may be computed, and "
              "retained/demolished/new cannot be answered." % len(problems))
        print("  -> %s must be rebased onto the resolved shell. That is "
              "AUTHORING work: its partitions have to be re-expressed against "
              "the compiler's geometry, not transformed onto it." % a.proposed)
        return 1

    for state, proposed_id, base_id in sorted(classify(base, proposed)):
        print("  %-18s %-8s %s" % (state, proposed_id or "-", base_id or "-"))
    print("PASS - one basis, and every wall is classified against the baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
