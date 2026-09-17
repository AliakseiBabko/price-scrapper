#!/usr/bin/env python3
"""WHAT WAS BUILT — the existing-state covering record, and its parity bridge.

⚠️⚠️ PRESENCE IS NOT REQUIREMENT, AND THE TWO MUST NOT SHARE A TABLE
--------------------------------------------------------------------
    wall_covering_patches.csv   `insulation_present`  — what the developer
                                actually built, directly evidenced.
    insulation_decision_table   `insulation_required` — what the boundary rule
    over the boundary patches   says SHOULD be there.

These are different facts about the same face, and conflating them was a real
category error on my part: M2's abutting run came out `unresolved` because the
neighbour's parapet contact is unknown, and I reported that as blocking. It
never was. Whether insulation is PRESENT on M2 is drawn on the plan and stated
by the owner; it does not depend on the parapet at all.

⚠️ AN EVIDENCE-BACKED AUTHORED FACT IS NOT AN "EXCEPTION". The defect was never
that M2's insulation extent was authored — it was that it lived in wall-wide
columns (`insulation_mm`, `insulation_from_mm`, `insulation_side`) that each
consumer interpreted its own way, which is how the IFC came to assert a uniform
200+150 while the drawing showed 570 mm. Canonical input stays canonical; it
just stops being a column that means different things to different readers.

⚠️ THICKNESS CARRIES ITS OWN STATE, SEPARATELY FROM PRESENCE. M2's band is
present on evidence while its 120 mm is an owner's assumption by symmetry with
M6b. One row-level status would have laundered that, exactly as it would in the
boundary assertions.

EXISTING-PHASE GEOMETRY COMES FROM HERE. `place_insulation.py` and
`typing_pass.py` consume the resolved result rather than re-reading the legacy
columns, and `check_parity()` asserts the two agree for as long as both exist.
"""
from __future__ import annotations

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.tabular import ValidationError, finite, read_csv  # noqa: E402

PATCHES = os.path.join(REPO, "data", "canonical", "wall_covering_patches.csv")
BLOCKS = os.path.join(REPO, "data", "canonical", "wall_blocks.csv")

PRESENCE = ("present", "absent", "unknown")
KINDS = ("external_insulation",)
PHASES = ("existing", "demolished", "new")

# ⚠️ THE FACE DECIDES THE SIDE. `insulation_side` was a separate column saying
# `low`/`high`, which is the same fact as `cross_lo`/`cross_hi` written twice -
# and two columns for one fact is how they drift.
FACE_SIDE = {"cross_lo": "low", "cross_hi": "high"}

REQUIRED = ["patch_uuid", "host_id", "face_ref", "phase", "covering_kind",
            "along_from_mm", "along_to_mm", "vertical", "presence_state",
            "presence_basis", "thickness_mm", "thickness_value_state", "state"]


def load(path=PATCHES):
    rows = read_csv(path, required=REQUIRED)
    seen = set()
    for row in rows:
        key = (row["patch_uuid"],)
        if key in seen:
            raise ValidationError("covering patch %s appears twice"
                                  % row["patch_uuid"])
        seen.add(key)
    return rows


def active(rows=None):
    rows = load() if rows is None else rows
    return [r for r in rows if (r.get("state") or "").strip() == "active"]


def resolved(rows=None, phase="existing"):
    """host -> the covering bands actually built, in host-local terms.

    Returns {host_id: [{face_ref, side, from, to, thickness, presence, ...}]}
    for patches whose presence is `present`. An `absent` patch is REAL DATA and
    is kept in the record - it is what says MC's end has no cap - but it
    contributes no band.
    """
    out = {}
    for row in active(rows):
        if (row.get("phase") or "").strip() != phase:
            continue
        if (row.get("covering_kind") or "").strip() != "external_insulation":
            continue
        lo, hi = finite(row.get("along_from_mm")), finite(row.get("along_to_mm"))
        if lo is None or hi is None or hi <= lo:
            raise ValidationError(
                "covering patch %s has bounds %r..%r, which do not describe a "
                "band" % (row["patch_uuid"], row.get("along_from_mm"),
                          row.get("along_to_mm")))
        presence = (row.get("presence_state") or "").strip()
        if presence not in PRESENCE:
            raise ValidationError("covering patch %s has presence_state %r, "
                                  "not one of %s"
                                  % (row["patch_uuid"], presence,
                                     ", ".join(PRESENCE)))
        if presence != "present":
            continue
        thickness = finite(row.get("thickness_mm"))
        if thickness is None or thickness <= 0:
            raise ValidationError(
                "covering patch %s is PRESENT with thickness %r. Something "
                "that is there has a depth; record it or mark the patch "
                "unknown" % (row["patch_uuid"], row.get("thickness_mm")))
        out.setdefault(row["host_id"], []).append({
            "patch_uuid": row["patch_uuid"],
            "face_ref": row["face_ref"],
            "side": FACE_SIDE.get(row["face_ref"]),
            "from_mm": lo, "to_mm": hi, "thickness_mm": thickness,
            "thickness_value_state": row.get("thickness_value_state"),
        })
    return out


def legacy_equivalent(rows=None):
    """What the legacy wall_blocks columns WOULD say, derived from the patches.

    ⚠️ This exists for the PARITY BUILD and for nothing else. The legacy shape
    cannot express more than one band per wall, or a band that is not flush
    with the wall's own end - so if a second band is ever authored on one wall,
    this raises rather than silently reporting the first.
    """
    bands = resolved(rows)
    out = {}
    for host, entries in sorted(bands.items()):
        if len(entries) > 1:
            raise ValidationError(
                "%s has %d covering bands, which the legacy single-column "
                "shape cannot express. The parity bridge must be retired "
                "before this is authored, not worked around" % (host, len(entries)))
        band = entries[0]
        # ⚠ ABSOLUTE extent, resolved from the face-local bounds - and ONLY
        # where the band stops short of the face. A band that runs the whole
        # face has no extent to state, which is what the legacy blank meant.
        face = _face_span(host, band["face_ref"])
        (ax, ay), _b = face["endpoints"]
        tx, ty = face["tangent"]
        full = band["from_mm"] <= 0.5 and band["to_mm"] >= face["length_mm"] - 0.5
        extent_from = extent_to = None
        if not full:
            points = [(ax + tx * band[k], ay + ty * band[k])
                      for k in ("from_mm", "to_mm")]
            axis = 1 if abs(ty) > abs(tx) else 0
            extent_from = min(p[axis] for p in points)
            extent_to = max(p[axis] for p in points)
        out[host] = {"insulation_mm": band["thickness_mm"],
                     "side": band["side"],
                     "from_mm": band["from_mm"], "to_mm": band["to_mm"],
                     "extent_from_mm": extent_from, "extent_to_mm": extent_to}
    return out


def _face_span(host, face_ref):
    """(start_point, tangent, length) for a face, from the compiler."""
    from resolve_v0_geometry import resolve
    faces = resolve().faces.get(host) or {}
    face = faces.get(face_ref)
    if face is None:
        raise ValidationError("%s has no face %r" % (host, face_ref))
    return face


def check_parity(rows=None):
    """Compare the derived result against the legacy columns. Returns problems.

    ⚠️⚠️ THE PARITY BUILD. Both records are kept while this passes; the legacy
    columns are removed only once the patches reproduce them exactly AND no
    consumer still reads them. A cutover that changes an answer at the same
    time as it changes the source makes it impossible to say which did it.
    """
    problems = []
    derived = legacy_equivalent(rows)
    legacy = {}
    for row in read_csv(BLOCKS, required=["wall_id", "insulation_mm"]):
        raw = (row.get("insulation_mm") or "").strip()
        if not raw:
            continue
        legacy[row["wall_id"]] = {
            "insulation_mm": finite(raw),
            "side": (row.get("insulation_side") or "").strip() or None,
            "from_mm": finite(row.get("insulation_from_mm")),
            "to_mm": finite(row.get("insulation_to_mm")),
        }

    for host in sorted(set(derived) | set(legacy)):
        want, got = legacy.get(host), derived.get(host)
        if want is None:
            problems.append(
                "%s has a covering patch but wall_blocks.csv records no "
                "insulation - the patches would ADD a band the legacy build "
                "does not have" % host)
            continue
        if got is None:
            problems.append(
                "%s carries insulation in wall_blocks.csv but has no covering "
                "patch - the patches would LOSE a band" % host)
            continue
        if abs(got["insulation_mm"] - want["insulation_mm"]) > 0.5:
            problems.append("%s thickness: patches say %.1f, wall_blocks.csv "
                            "says %.1f" % (host, got["insulation_mm"],
                                           want["insulation_mm"]))
        if want["side"] and got["side"] != want["side"]:
            problems.append("%s side: patches say %r (from face %s), "
                            "wall_blocks.csv says %r"
                            % (host, got["side"], "cross_*", want["side"]))
        # ⚠️ The legacy extent is ABSOLUTE drawing mm; the patch is face-local.
        # Converting proves the two describe the same stretch of wall, which is
        # the whole point of the parity build.
        for label, key in (("from", "extent_from_mm"), ("to", "extent_to_mm")):
            legacy_value = want["from_mm"] if label == "from" else want["to_mm"]
            derived_value = got.get(key)
            if legacy_value is None and derived_value is None:
                continue
            if legacy_value is None or derived_value is None:
                problems.append(
                    "%s extent %s: patches resolve to %r, wall_blocks.csv says "
                    "%r - one records a partial band and the other does not"
                    % (host, label, derived_value, legacy_value))
                continue
            if abs(derived_value - legacy_value) > 0.5:
                problems.append(
                    "%s extent %s: patches resolve to %.1f, wall_blocks.csv "
                    "says %.1f" % (host, label, derived_value, legacy_value))
    return problems


def main() -> int:
    problems = check_parity()
    for problem in problems:
        print("FAIL %s" % problem)
    bands = resolved()
    print("%d covering patch(es), %d wall(s) carrying a band"
          % (len(active()), len(bands)))
    for host, entries in sorted(bands.items()):
        for band in entries:
            print("  %-5s %-9s %8.1f..%-8.1f %5.0f mm  %s"
                  % (host, band["face_ref"], band["from_mm"], band["to_mm"],
                     band["thickness_mm"], band["thickness_value_state"]))
    if problems:
        print("FAILED: %d parity problem(s)" % len(problems))
        return 1
    print("PASS - the covering patches reproduce the legacy columns exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
