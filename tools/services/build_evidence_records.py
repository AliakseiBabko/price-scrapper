#!/usr/bin/env python3
"""Repair the assertions whose SEMANTICS were wrong, and add the missing
observations and values their adjudications declare.

⚠️ FIXING SUBJECTS REPAIRED STRUCTURE, NOT SEMANTICS.
-----------------------------------------------------
After every row gained a subject, four rows were still wrong in kind:

  E-KL-SOC-K   a TRUNCATED ADJUDICATION NOTE stored as an `arrangement`
               value, scoped to ours as stated/asserted - when the source is
               an observation of THREE outlets in apartment 53 with a
               915-1105 height range
  V-1          likewise: truncated migration commentary asserted as an
               arrangement, when the claim is that the legacy sheet drew
               H=218 on support that does not cover it
  S3 appearance  classified as `function`. A larger, differently shaped
               socket is an APPEARANCE; what it does is the inference drawn
               FROM it, and conflating them is what let "looks different"
               become "is 380 V"
  S3 three-phase  classified as `voltage`, with its own note saying phase and
               voltage must not collapse into one claim

An adjudication note is PROSE ABOUT a fact. Storing it as the fact's VALUE
means nothing downstream can read the number, the count or the range.

    .venv\\Scripts\\python.exe tools/services/build_evidence_records.py
"""
from __future__ import annotations

import argparse
import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

# migration_key -> field overrides. Explicit, reviewed, no inference.
REWRITE = {
    "ASR-electrical-existing-E-KL-SOC-K": {
        "property": "count", "value": "3", "value_type": "int",
        "knowledge_basis": "derived", "value_state": "candidate",
        "scope_ref": "ours", "observation_refs": "OBS-E-KL-SOC-K-53",
        "notes": "⚠ REWRITTEN: this stored a truncated adjudication NOTE "
                 "as an `arrangement` value, scoped to ours and asserted. The "
                 "count of three is certain ABOUT APARTMENT 53 "
                 "(OBS-E-KL-SOC-K-53); its projection here is a candidate. The "
                 "915-1105 range is VAL-E-KL-SOC-K-HEIGHT, a value record, "
                 "because a range is not a point and must not be flattened "
                 "into one.",
    },
    "ASR-tag-V-1": {
        "property": "vertical", "value": "2180", "value_type": "mm",
        "knowledge_basis": "assumed", "value_state": "retracted",
        "scope_ref": "ours", "device_class": "grille",
        "notes": "⚠ REWRITTEN: this stored truncated migration commentary "
                 "as an asserted `arrangement`. The actual claim is that the "
                 "legacy sheet DREW H=218 at V1. RETRACTED: SV-T's own row "
                 "says 'not yet measured, if SV-K is the standard expect ~2.2 "
                 "m', so 2180 is that EXPECTATION drawn as a measurement - on "
                 "two photographs that both show the KITCHEN grille on V2.",
    },
    "ASR-POWER-S3-APPEARANCE": {
        "property": "appearance",
        "notes": "⚠ PROPERTY CORRECTED from `function`. A larger, "
                 "differently shaped socket is an APPEARANCE; what it DOES is "
                 "the inference drawn from it. Conflating the two is exactly "
                 "how «it looks different» becomes «it is 380 "
                 "V». Observed in 930d/a89d, apartment 53.",
    },
    "ASR-POWER-S3-3PH": {
        "property": "supply_phases", "value": "3", "value_type": "int",
        "notes": "⚠ PROPERTY CORRECTED from `voltage`, which contradicted "
                 "this row's own note. Phase count and voltage are different "
                 "facts: 380 V and three-phase are separately uncertain, and "
                 "the owner is explicit that the phases are the weaker guess - "
                 "«probably 3 phases, but I'm not sure». "
                 "value_state=unknown, weaker than the 380 V candidate.",
    },
    # ⚠️ ROUTE LAUNDERING. Scoped to ours with knowledge_basis=observed while
    # its own note says the topology comes from a comparable flat.
    "RTE-BATH-S": {
        "knowledge_basis": "derived", "value_state": "candidate",
        "notes": "⚠ BASIS CORRECTED: this was scoped to OUR apartment "
                 "with knowledge_basis=observed while saying in the same note "
                 "that it comes from b83a, a comparable flat. The observation "
                 "is OBS-BATH-S-53, scoped there; this is the derived "
                 "candidate projection. The comparable-flat rule applies to "
                 "every scoped evidentiary claim, not only to assertions.",
    },
    # corroboration that now names the observation backing it
    "ASR-3-zero-outlets-on-mc": {"observation_refs": "OBS-MC-EMPTY-109"},
}

NEW_OBSERVATIONS = [
    ("OBS-E-KL-SOC-K-53", "legacy_csv:electrical_existing:E-KL-SOC-K",
     "three socket outlets in a row on the kitchen corridor wall - two read as "
     "vertical doubles, one as a right-hand single", "53", "930d", "3", "3",
     "", "range",
     "The source of the count of three AND of the 915-1105 height range. "
     "Scoped to apartment 53, which is what 930d shows."),
    ("OBS-LIGHT-L3-109", "legacy_generator:LIGHT:L3",
     "corridor ceiling cable outlet", "109", "a82a;a89c", "1", "1", "",
     "none",
     "The observation the L3 literal rests on. Its projection onto ours is "
     "ASR-LIGHT-L3-EXIST, candidate."),
    ("OBS-BATH-S-53", "legacy_generator:BATH_S",
     "bathroom DN50 run to the main stack through G4b", "53", "b83a", "", "",
     "", "none",
     "The owner's annotated photo of a COMPARABLE flat. Topology observed "
     "there; RTE-BATH-S is the candidate projection here."),
]

NEW_VALUES = [
    ("VAL-E-KL-SOC-K-HEIGHT", "legacy_csv:electrical_existing:E-KL-SOC-K",
     "centre_height_mm", "915-1105", "range", "observed", "asserted", "53",
     "⚠ A RANGE, KEPT AS A RANGE. The generator's 1000 is a derived, "
     "rounded nominal and does NOT replace this - an observed range flattened "
     "to a point is precision nobody measured."),
]

VAL_FIELDS = ["migration_key", "source_locators", "target_concept",
              "quantity", "value", "value_type", "knowledge_basis",
              "value_state", "scope_kind", "scope_ref", "notes"]

DROP = {
    # ⚠️ Its own duplicate_of relation says it is carried by
    # legacy_comment:6#two_vertical_dn110_stacks "not by a second one" - and
    # the substantive assertion was still sitting beside it.
    "ASR-10-sewer-stacks-restated",
}


def _rewrite(path):
    with io.open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys())
    kept, changed, dropped = [], 0, 0
    for row in rows:
        if row["migration_key"] in DROP:
            dropped += 1
            continue
        patch = REWRITE.get(row["migration_key"])
        if patch:
            for field, value in patch.items():
                if field == "notes":
                    row[field] = value + " || " + row.get(field, "")
                else:
                    row[field] = value
            changed += 1
        kept.append(row)
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept)
    return changed, dropped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--drafts", default=DRAFTS)
    a = ap.parse_args()

    changed = 0
    dropped = 0
    for name in ("assertions.csv", "routes.csv"):
        c, d = _rewrite(os.path.join(a.drafts, name))
        changed += c
        dropped += d

    obs_path = os.path.join(a.drafts, "observations.csv")
    with io.open(obs_path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys())
    have = set(r["migration_key"] for r in rows)
    added = 0
    for (key, src, what, scope, via, cmin, cmax, mm, mkind, note) in NEW_OBSERVATIONS:
        if key in have:
            continue
        rows.append({"migration_key": key, "source_locators": src,
                     "target_concept": "observation", "observed_what": what,
                     "scope_kind": "apartment", "scope_ref": scope,
                     "observed_via": via, "count_min": cmin,
                     "count_max": cmax, "measurement_mm": mm,
                     "measurement_kind": mkind, "notes": note})
        added += 1
    with io.open(obs_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    val_path = os.path.join(a.drafts, "values.csv")
    with io.open(val_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=VAL_FIELDS)
        writer.writeheader()
        for (key, src, quantity, value, vtype, basis, state, scope,
             note) in NEW_VALUES:
            writer.writerow({
                "migration_key": key, "source_locators": src,
                "target_concept": "value", "quantity": quantity,
                "value": value, "value_type": vtype,
                "knowledge_basis": basis, "value_state": state,
                "scope_kind": "apartment", "scope_ref": scope, "notes": note})

    print("rewrote %d row(s), dropped %d, added %d observation(s) and %d "
          "value(s)" % (changed, dropped, added, len(NEW_VALUES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
