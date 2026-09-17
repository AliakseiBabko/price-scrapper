#!/usr/bin/env python3
"""Give every projection and drawing-only assertion an explicit SUBJECT.

⚠️ WHY: the normative design requires every property assertion to name what it
is about, and 90 of 108 generated assertions named nothing. An assertion with
no subject is not a weak fact, it is not a fact - "existence = true" about
nothing cannot be checked, contradicted or generated from.

These rows are the comparable-flat PROJECTIONS (`...-EXIST`) and the
DRAWING-ONLY historical assertions (`...-DREW`). Neither has a target
occurrence to point at - that is the whole point of them, since no occurrence
is minted from comparable-flat evidence - so they carry `subject_element`: the
wall, zone or room the claim is about.

⚠️ THE WALL IDS ARE TRANSCRIBED FROM THE LITERALS, NOT INFERRED. Each one is
the wall the legacy tuple names. Where the legacy assignment is itself
disproven - S4 on R2 and S9 on R6, both concrete - the subject stays the wall
that was DRAWN, because the assertion is about what the sheet claimed. The
disproof is its own separate record.

    .venv\\Scripts\\python.exe tools/services/build_projection_assertions.py
"""
from __future__ import annotations

import argparse
import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

# migration_key suffix -> (subject_element, device_class)
# Walls are as the legacy literal names them; rooms where a CSV row is scoped
# to a room rather than a wall; `slabs` for ceiling points.
SUBJECTS = {
    # --- generator sockets, wall from the SOCK literal -------------------
    "SOCK-S1": ("G3", "outlet"), "SOCK-S2": ("G3", "outlet"),
    "SOCK-S4": ("R2", "outlet"), "SOCK-S5": ("G5", "outlet"),
    "SOCK-S6": ("G8", "outlet"), "SOCK-S7": ("G8", "outlet"),
    "SOCK-S8": ("G4a", "outlet"), "SOCK-S9": ("R6", "outlet"),
    "SOCK-S12": ("MB", "outlet"), "SOCK-S13": ("MA", "outlet"),
    "SOCK-S17": ("G7", "outlet"), "SOCK-S18": ("G7", "outlet"),
    "POWER-S3": ("G3", "power_outlet"),
    # --- switches, from SWDEF --------------------------------------------
    "SWDEF-W1": ("G4C", "switch"), "SWDEF-W2": ("G4C", "switch"),
    "SWDEF-W3": ("G2", "switch"), "SWDEF-W4": ("G6", "switch"),
    "SWDEF-W5": ("G8", "switch"),
    # --- ceiling points: the SLAB, not a wall ----------------------------
    "LIGHT-L1": ("slabs", "light_point"), "LIGHT-L2": ("slabs", "light_point"),
    "LIGHT-L3": ("slabs", "light_point"), "LIGHT-L4": ("slabs", "light_point"),
    "LIGHT-L5": ("slabs", "light_point"), "LIGHT-L6": ("slabs", "light_point"),
    "LIGHT-L7": ("slabs", "light_point"),
    "tag-F1": ("slabs", "detector"),
    # --- canonical CSV rows, scoped to a room or an element --------------
    "electrical-existing-E-KL-LIGHT": ("kitchen_living", "light_point"),
    "electrical-existing-E-KL-SOC-W": ("kitchen_living", "outlet"),
    "electrical-existing-E-C-LIGHT": ("corridor", "light_point"),
    "electrical-existing-E-C-SWITCH": ("corridor", "switch"),
    "electrical-existing-E-C-HIGH": ("corridor", "unidentified_box"),
    "electrical-existing-E-MR-SOC": ("middle_room", "outlet"),
    "electrical-existing-E-MR-LIGHT": ("middle_room", "light_point"),
    "electrical-existing-E-SB-SOC": ("small_bedroom", "outlet"),
    "electrical-existing-E-SB-LIGHT": ("small_bedroom", "light_point"),
    "electrical-existing-E-WC-BOX": ("toilet", "unidentified_box"),
    "service-outlets-SV-K": ("V2", "grille"),
    "service-outlets-SS-K": ("G3", "sewer_connection"),
    "service-outlets-SW-K": ("G3", "water_takeoff"),
    "service-outlets-SH-B": ("P1", "riser"),
    "plumbing-anchors-T1": ("G4b", "towel_rail_tails"),
    "plumbing-anchors-P1": ("P1", ""), "plumbing-anchors-P2": ("P2", ""),
    # --- routes ----------------------------------------------------------
    "ROUTES-GVS": ("flat", "route"), "ROUTES-HVS": ("flat", "route"),
    "ROUTES-HVS-v": ("flat", "route"), "SEWER": ("flat", "route"),
    "BATH-W": ("flat", "route"), "BATH-S": ("flat", "route"),
    # --- named individually, because their keys are not locator stems -----
    "EC-LIGHT-OURS": ("corridor", "light_point"),
    "electrical-existing-E-KL-SOC-K": ("G3", "outlet"),
    "tag-V-1": ("V1", "grille"),
    "POWER-S3-APPEARANCE": ("G3", "power_outlet"),
    "POWER-S3-NOT-220": ("G3", "power_outlet"),
    "POWER-S3-380": ("G3", "power_outlet"),
    "POWER-S3-3PH": ("G3", "power_outlet"),
    # ⚠️ The two disproven hosts keep the wall that was DRAWN as their
    # subject. The assertion is about what the sheet claimed, and moving the
    # subject to some corrected wall would destroy the record of the error.
    "SOCK-S4-SUBSTRATE": ("R2", "outlet"),
    "SOCK-S9-SUBSTRATE": ("R6", "outlet"),
    "MC-EMPTY": ("MC", "outlet"),
}

# Rows that should never have been assertions at all.
DROP = {
    # a `duplicate` claim is a RELATION, not a property assertion
    "ASR-11-heights-from-csv",
    # superseded by ASR-REWIRE-TOPOLOGY + ASR-REWIRE-SUBSTRATE, which carry
    # real provenance instead of a borrowed W6 locator
    "ASR-REWIRE-DROPS-IN-BLOCK",
}

SUFFIXES = ("-EXIST", "-DREW", "-GEOM")


def subject_for(key):
    """(subject_element, device_class) or None - never a guess."""
    stem = key[4:] if key.startswith("ASR-") else key
    for suffix in SUFFIXES:
        if stem.endswith(suffix):
            stem = stem[:-len(suffix)]
            break
    return SUBJECTS.get(stem)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(DRAFTS, "assertions.csv"))
    a = ap.parse_args()

    with io.open(a.out, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys())

    dropped = [r for r in rows if r["migration_key"] in DROP]
    rows = [r for r in rows if r["migration_key"] not in DROP]
    filled, missing = 0, []
    for row in rows:
        if (row.get("subject_key") or "").strip():
            continue
        if (row.get("subject_element") or "").strip():
            continue
        found = subject_for(row["migration_key"])
        if found is None:
            missing.append(row["migration_key"])
            continue
        row["subject_element"], device = found
        if device and not (row.get("device_class") or "").strip():
            row["device_class"] = device
        filled += 1

    with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print("filled %d subject(s); dropped %d non-assertion row(s)"
          % (filled, len(dropped)))
    if missing:
        print("STILL WITHOUT A SUBJECT (%d):" % len(missing))
        for key in missing:
            print("   %s" % key)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
