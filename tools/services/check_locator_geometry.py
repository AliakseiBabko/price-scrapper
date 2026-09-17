#!/usr/bin/env python3
"""Geometry gate for service locators. Step 3 of pass 2 — the `wall_face` half.

`check_target_schema.py` proves a record is well FORMED. This one asks whether
it describes a place that exists, against the geometry compiler.

⚠️ IT RUNS ON `.venv-ifc314`, because `resolve_v0_geometry` lives there.

THE THREE-STATE VERDICT, AND WHY IT IS NOT TWO
----------------------------------------------
A point cannot collide with anything, so a terminal is checked as an ENVELOPE —
and the envelope is usually unknown. Unknown dimensions are NOT an excuse to
pass:

  centre inside a void             INVALID
  centre clear, extent unknown     INCOMPLETE - not proven valid
  full asserted envelope clear     VALID

⚠️ THE VALIDATOR NEVER INVENTS DEVICE DIMENSIONS. A default socket size written
in here would be an assumption nobody can see, and it would turn every
INCOMPLETE into a confident VALID. Extent comes from `extent_along_mm` /
`extent_vertical_mm` assertions or it is unknown.

⚠️ `host_interaction` DECIDES WHETHER AN OVERLAP IS A DEFECT AT ALL
-------------------------------------------------------------------
`SV-VT` IS a hole through G4b — the owner's transfer opening between the ванная
and the туалет. A blanket *"a service may not overlap a void"* rule would
eventually reject the one element whose entire purpose is to be a penetration.
So the void test applies only to `avoid_void`, and **absence of the property is
NOT treated as `avoid_void`** — it is `incomplete`.

⚠️ AN ANCHOR IS NOT A HOST
--------------------------
`W6` is anchored to opening `O10` and mounted on `R5`. The compiler resolves O10
as `hosting=spans_between_elements` with **`host_wall=None`** — no wall hosts
it; R5 is its southern flank, and R5's `end_to` face at y=13650.3 is exactly
coincident with O10's southern edge. So requiring an anchor's `host_wall` to
equal the service's `host_ref` would reject a legitimate case, and would also be
wrong in kind: *"mounted beside an opening"* and *"mounted on the opening's host
wall"* are different relationships. The anchor check is BOUNDARY ADJACENCY.

    .venv-ifc314\\Scripts\\python.exe tools/services/check_locator_geometry.py
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "services"))

from check_target_schema import load as load_targets   # noqa: E402

TOUCH_MM = 1.0        # coincidence tolerance for boundary adjacency

# ⚠️ A CABLE CANNOT BE CHASED INTO CONCRETE (owner, 2026-09-17). Significant
# cavities may not be cut into the monolithic RC frame, so no chased accessory
# is hosted on a `concrete` wall. This is the electrical twin of
# A_PIPE_CANNOT_CROSS_CONCRETE_2026_09_07, and it has the same standing: it
# DISPROVES a placement, it never proves an element exists.
#
# It matters because wall assignment is the axis `WALL_MAPPING_WAS_WRONG_TWICE`
# records as the one that could not be read off photographs at all. A
# constraint the model carries can refute an assignment without the owner
# having to notice it again.
# ⚠️ CORRECTED SAME DAY: cast-in is NOT chasing. The owner - "a constructor is
# able to include wiring in the concrete while pouring it... this is how it
# works for the ceiling". So the prohibition is on CUTTING A CAVITY INTO CURED
# CONCRETE, and `installation_method` is the axis, not the material alone.
#
#   phase=proposed + concrete   INVALID, no exception - a retrofit cannot cast
#                               into concrete that is already poured, and the
#                               owner's rewire puts every drop in block
#   phase=existing  + cast_in   allowed; this is how the ceiling points exist
#   phase=existing  + chased    INVALID
#   phase=existing  + unstated  INCOMPLETE - not impossible, just unevidenced
# ⚠️ MATERIAL, NOT `class`. `class` mixes material with exposure -
# `external_warm_perimeter` is a thermal role, not something you can or cannot
# chase - so asking it for substrate gave the wrong kind of answer.
#
# ⚠️ AND THE PROPOSED RULE IS A WHITELIST, NOT "NOT CONCRETE". The owner's
# rewire puts every drop «exclusively in the walls from the softer materials
# like aerated concrete». An earlier version only REFUSED concrete, so a
# proposed accessory on M2 - loggia_enclosure, material unknown - sailed
# through substrate checking entirely.
CHASEABLE_MATERIALS = ("aerated_block",)
NO_CHASE_MATERIALS = ("reinforced_concrete",)
MATERIALS = os.path.join(REPO, "data", "canonical", "wall_materials.json")


class DuplicateWallId(Exception):
    """Two records claim the same wall id. See `wall_classes`."""


def wall_classes(path=MATERIALS):
    """wall id -> MATERIAL, from canonical data, never hardcoded here.

    A wall with no `material` returns None and is reported INCOMPLETE - never
    assumed chase-able.

    ⚠️ DUPLICATE IDS ARE REJECTED, NOT LAST-WINS. This built the index straight
    from the sequence, so a second record for an existing wall silently
    overwrote the first. Appending a second `R5` with material=aerated_block
    resolved CONCRETE R5 AS AERATED BLOCK - which is precisely the reading that
    would authorise chasing the monolithic RC frame.

    It is the same defect `dxf_closure_selftest.py` already seeds for
    `wall_blocks.csv` and `wall_corners.csv`: a collection that deduplicates
    destroys the thing being checked. The sequence is read first, then checked,
    then indexed.
    """
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    walls = data.get("walls", [])
    seen, duplicates = set(), []
    for wall in walls:
        wid = wall.get("id")
        if wid in seen:
            duplicates.append(wid)
        seen.add(wid)
    if duplicates:
        raise DuplicateWallId(
            "wall_materials.json declares %s more than once - a duplicate id "
            "silently overwrites the first record, and a wrong material here "
            "would authorise chasing the RC frame"
            % ", ".join(sorted(set(duplicates))))
    return dict((w.get("id"), w.get("material")) for w in walls)


def geometry():
    import resolve_v0_geometry
    return resolve_v0_geometry.resolve(), resolve_v0_geometry


def _along_span(face, polygon):
    """Where `polygon` sits along `face`, in along-face millimetres."""
    (ax, ay), _b = face["endpoints"]
    tx, ty = face["tangent"]
    values = [(px - ax) * tx + (py - ay) * ty for px, py in polygon]
    return min(values), max(values)


def _assertions(targets, subject):
    out = {}
    for row in targets:
        if (row.get("target_concept") or "") != "assertion":
            continue
        if (row.get("subject_key") or "") != subject:
            continue
        out[(row.get("property") or "").strip()] = row
    return out


def _number(assertion):
    """The asserted number, or None when the record says `unknown`."""
    if assertion is None:
        return None
    if (assertion.get("value_state") or "").strip() == "unknown":
        return None
    text = (assertion.get("value") or "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def check(targets, resolved, opening_verticals, classes=None):
    """[(migration_key, verdict, message)] - one row per occurrence."""
    if classes is None:
        classes = wall_classes()
    results = []
    faces = resolved.faces
    openings = resolved.openings

    for row in targets:
        if (row.get("target_concept") or "") != "occurrence":
            continue
        key = (row.get("migration_key") or "").strip()
        kind = (row.get("locator_kind") or "").strip()

        if kind == "unlocated":
            results.append((key, "unlocated",
                            "no placement asserted, and the record says so"))
            continue
        if kind == "surface_local":
            # ⚠️ NOT A PASS. The compiler publishes no support-surface
            # registry, no ceiling regions and no surface resolver, so there is
            # nothing to check this against. Reporting `valid` here would be
            # claiming ceiling validation that does not exist.
            results.append((key, "unsupported",
                            "support geometry unavailable - the compiler "
                            "publishes no support surfaces, so `surface_local` "
                            "cannot be validated"))
            continue
        if kind != "wall_face":
            results.append((key, "invalid",
                            "unknown locator_kind %r - an unrecognised kind is "
                            "a hard failure, never a skip" % kind))
            continue

        host = (row.get("host_ref") or "").strip()
        if host not in faces:
            results.append((key, "invalid",
                            "missing host: no wall %r in the resolved model"
                            % host))
            continue
        face_ref = (row.get("face_ref") or "").strip()
        if face_ref not in faces[host]:
            results.append((key, "invalid",
                            "invalid face_ref %r on %s; known roles are %s"
                            % (face_ref, host,
                               ", ".join(sorted(faces[host])))))
            continue
        # ⚠️ SUBSTRATE, BEFORE ANY GEOMETRY. A perfectly placed socket on a
        # concrete column is still not buildable, and saying "valid" about it
        # would be precise about the wrong thing.
        klass = classes.get(host)
        assertions = _assertions(targets, key)
        method = (assertions.get("installation_method") or {}).get("value", "")
        method = (method or "").strip()
        phase = (row.get("phase") or "").strip()
        # PROPOSED work: a WHITELIST. Every new drop must land on a chase-able
        # material, so anything not on the list fails - including a material
        # nobody has recorded.
        if phase == "proposed" and klass not in CHASEABLE_MATERIALS:
            results.append((key, "invalid",
                            "host %s is %r and this is PROPOSED work - every "
                            "new drop must be chased into %s, and a retrofit "
                            "cannot cast into concrete already poured"
                            % (host, klass, "/".join(CHASEABLE_MATERIALS))))
            continue
        if klass in NO_CHASE_MATERIALS:
            if method == "chased":
                results.append((key, "invalid",
                                "host %s is %s and the accessory is chased - a "
                                "cavity may not be cut into the monolithic RC "
                                "frame" % (host, klass)))
                continue
            if method != "cast_in":
                results.append((key, "incomplete",
                                "host %s is %s and no installation_method is "
                                "asserted - cast-in is possible but "
                                "UNEVIDENCED here, and chasing is prohibited"
                                % (host, klass)))
                continue
        if klass is None:
            results.append((key, "incomplete",
                            "host %s has no `material` in wall_materials.json, "
                            "so the substrate rule cannot be applied - NOT "
                            "assumed chase-able" % host))
            continue

        face = faces[host][face_ref]
        length = face["length_mm"]

        # ⚠️ AN ANCHOR IS NOT A HOST. Adjacency only, and a null host_wall is
        # perfectly normal for an opening that spans between elements.
        anchor = (row.get("anchor_ref") or "").strip()
        if anchor:
            opening = next((o for o in openings
                            if o.get("opening_id") == anchor), None)
            if opening is None:
                results.append((key, "invalid",
                                "anchor_ref %r is not an opening the compiler "
                                "resolves" % anchor))
                continue
            # ⚠️ ADJACENCY, NOT HOSTING. O10 has host_wall=None and that is
            # correct - it spans between elements. R5 is its southern flank.
            if not _shares_boundary(faces[host], opening["polygon"]):
                results.append((key, "invalid",
                                "anchor_ref %s does not touch %s at all"
                                % (anchor, host)))
                continue

        along = _number(assertions.get("position_along"))
        if along is None:
            along_text = (row.get("along_face_mm") or "").strip()
            along = float(along_text) if along_text else None

        if along is None:
            results.append((key, "partial",
                            "no along-face position asserted on the occurrence "
                            "- placement is deliberately incomplete, which is "
                            "not a defect"))
            continue
        if along < 0 or along > length:
            results.append((key, "invalid",
                            "along_face_mm %.1f is outside %s.%s, which is "
                            "%.1f mm long" % (along, host, face_ref, length)))
            continue

        interaction = (assertions.get("host_interaction") or {}).get("value", "")
        interaction = (interaction or "").strip()
        if interaction in ("creates_penetration", "fills_opening"):
            results.append((key, "valid",
                            "host_interaction=%s - overlapping a void is this "
                            "element's PURPOSE, not a defect" % interaction))
            continue
        if interaction != "avoid_void":
            results.append((key, "incomplete",
                            "no host_interaction asserted; absence is NOT "
                            "read as avoid_void"))
            continue

        vertical = _number(assertions.get("vertical"))
        ext_a = _number(assertions.get("extent_along_mm"))
        ext_v = _number(assertions.get("extent_vertical_mm"))

        lo = along - (ext_a / 2.0 if ext_a else 0.0)
        hi = along + (ext_a / 2.0 if ext_a else 0.0)

        hit = None
        for opening in openings:
            # A void hosted in this wall cuts THROUGH it, so it is present on
            # every face of it. Openings hosted elsewhere are simply not this
            # wall's business.
            if opening.get("host_wall") != host:
                continue
            o_lo, o_hi = _along_span(face, opening["polygon"])
            if hi < o_lo or lo > o_hi:
                continue
            sill, head = opening_verticals(opening["opening_id"])
            if vertical is not None and sill is not None and head is not None:
                v_lo = vertical - (ext_v / 2.0 if ext_v else 0.0)
                v_hi = vertical + (ext_v / 2.0 if ext_v else 0.0)
                if v_hi < sill or v_lo > head:
                    continue
            hit = (opening["opening_id"], o_lo, o_hi, along <= o_hi and along >= o_lo)
            break

        if hit and hit[3]:
            results.append((key, "invalid",
                            "centre at %.1f is INSIDE the void of %s (%.1f-%.1f "
                            "along %s.%s)" % (along, hit[0], hit[1], hit[2],
                                              host, face_ref)))
        elif hit:
            results.append((key, "invalid",
                            "centre at %.1f is clear but the asserted extent "
                            "%.1f-%.1f CROSSES the void of %s (%.1f-%.1f)"
                            % (along, lo, hi, hit[0], hit[1], hit[2])))
        elif ext_a is None or ext_v is None:
            results.append((key, "incomplete",
                            "centre at %.1f is clear, but the device extent is "
                            "unknown - NOT proven valid, and no default size is "
                            "invented here" % along))
        else:
            results.append((key, "valid",
                            "envelope %.1f-%.1f clear of every void on %s.%s"
                            % (lo, hi, host, face_ref)))
    return results


def _shares_boundary(host_faces, polygon):
    """Does any face of the host lie on the polygon's boundary?"""
    for face in host_faces.values():
        for px, py in polygon:
            (ax, ay), (bx, by) = face["endpoints"]
            nx, ny = face["outward_normal"]
            if abs((px - ax) * nx + (py - ay) * ny) <= TOUCH_MM:
                lo, hi = _along_span(face, [(px, py)])
                if -TOUCH_MM <= lo <= face["length_mm"] + TOUCH_MM:
                    return True
    return False


FAILING = ("invalid",)

# ⚠️ AN ISSUED MODEL ACCEPTS `valid` AND NOTHING ELSE.
# `--strict` only promoted `incomplete`, so `unlocated`, `partial` and
# `unsupported` still passed it - and an unlocated occurrence is precisely a
# thing that cannot be drawn. A `surface_local` locator that CANNOT BE CHECKED
# passed strict too, which is the worst of the four. Review views may keep
# every verdict; an issued model may not.
ISSUABLE = ("valid",)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="also fail on `incomplete` (a REVIEW view)")
    ap.add_argument("--issued", action="store_true",
                    help="issued-model gate: fail anything that is not `valid`")
    a = ap.parse_args()

    resolved, module = geometry()
    targets = load_targets()
    results = check(targets, resolved, module._opening_verticals)

    bad = 0
    for key, verdict, message in results:
        print("%-12s %-14s %s" % (verdict.upper(), key, message))
        if a.issued:
            if verdict not in ISSUABLE:
                bad += 1
        elif verdict in FAILING or (a.strict and verdict == "incomplete"):
            bad += 1
    print("\n%d occurrence(s); %d failing" % (len(results), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
