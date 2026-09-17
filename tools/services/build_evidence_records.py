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
        "observation_refs": "OBS-BATH-S-53",
        "notes": "⚠ BASIS CORRECTED: this was scoped to OUR apartment "
                 "with knowledge_basis=observed while saying in the same note "
                 "that it comes from b83a, a comparable flat. The observation "
                 "is OBS-BATH-S-53, scoped there; this is the derived "
                 "candidate projection. The comparable-flat rule applies to "
                 "every scoped evidentiary claim, not only to assertions.",
    },
    # corroboration that now names the observation backing it
    "ASR-3-zero-outlets-on-mc": {"observation_refs": "OBS-MC-EMPTY-109"},
    # ⚠️ The projection now NAMES the observations it rests on - both flats.
    "ASR-EC-LIGHT-OURS": {
        "observation_refs": "OBS-CORRIDOR-LIGHT-109;OBS-CORRIDOR-LIGHT-2",
        "notes": "The projection onto ours, resting on TWO flats: 109 "
                 "(a82a/a89c) and 2 (9e9b). It claimed that support while "
                 "naming no observation at all, and the flat-2 observation did "
                 "not exist. Still candidate/derived - two flats are a "
                 "stronger projection, not an observation of ours.",
    },
    "ASR-LIGHT-L3-EXIST": {
        "observation_refs": "OBS-CORRIDOR-LIGHT-109;OBS-CORRIDOR-LIGHT-2",
    },
}

# ⚠️ OBS-EC-LIGHT-109 and OBS-LIGHT-L3-109 described THE SAME corridor point
# from THE SAME a82a/a89c photographs - two representations of one observation,
# not two pieces of evidence. Merged into a single flat-109 record citing both
# source locators. And apartment 2 was dropped entirely: the L3 literal cites
# 9e9b, the first record said so explicitly, and no flat-2 observation existed.
DROP_OBSERVATIONS = {"OBS-EC-LIGHT-109", "OBS-LIGHT-L3-109"}

NEW_OBSERVATIONS = [
    ("OBS-CORRIDOR-LIGHT-109",
     "legacy_csv:electrical_existing:E-C-LIGHT;legacy_generator:LIGHT:L3",
     "corridor ceiling pendant point", "109", "a82a;a89c", "1", "1", "",
     "none",
     "ONE observation of ONE point, citing both the CSV row and the drawing "
     "literal. It replaces OBS-EC-LIGHT-109 and OBS-LIGHT-L3-109, which "
     "described the same point from the same photographs and would have "
     "double-counted apartment 109 as two independent sightings."),
    ("OBS-CORRIDOR-LIGHT-2",
     "legacy_csv:electrical_existing:E-C-LIGHT;legacy_generator:LIGHT:L3",
     "corridor ceiling pendant point", "2", "9e9b", "1", "1", "", "none",
     "⚠ APARTMENT 2, WHICH HAD BEEN DROPPED. Both sources cite 9e9b and "
     "the earlier record said in its own note that this must be a separate "
     "observation - and then none existed. This is the SECOND flat, and it is "
     "the whole reason the corridor point is the strongest projection."),
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
              "value_state", "scope_kind", "scope_ref", "scope_phase",
              "observation_refs", "notes"]

# Separates the builder's own note from whatever it replaced, so a second run
# can strip its previous output instead of stacking on it.
MARK = " || "

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
                    # ⚠️ IDEMPOTENT. This PREPENDED the repair note every run,
                    # so two executions gave different files and the committed
                    # state matched neither. A builder that owns a record must
                    # REPLACE it deterministically - otherwise editing the
                    # explicit table cannot repair a row that already exists,
                    # which defeats the point of having the table.
                    prior = row.get(field, "")
                    if MARK in prior:
                        prior = prior.split(MARK, 1)[1]
                    row[field] = value + MARK + prior
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
    # ⚠️ REPLACE, do not skip. Skipping meant a correction to the explicit
    # table could never reach a row that already existed.
    owned = set(o[0] for o in NEW_OBSERVATIONS)
    rows = [r for r in rows if r["migration_key"] not in owned]
    rows = [r for r in rows if r["migration_key"] not in DROP_OBSERVATIONS]
    added = 0
    for (key, src, what, scope, via, cmin, cmax, mm, mkind, note) in NEW_OBSERVATIONS:
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
                "scope_kind": "apartment", "scope_ref": scope,
                "scope_phase": "existing", "observation_refs": "",
                "notes": note})

    print("rewrote %d row(s), dropped %d, added %d observation(s) and %d "
          "value(s)" % (changed, dropped, added, len(NEW_VALUES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
