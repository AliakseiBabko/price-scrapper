#!/usr/bin/env python3
"""Rebuild alias relations and route records so both actually resolve.

⚠️ THE ALIASES DID NOT SATISFY THEIR OWN ADJUDICATIONS
------------------------------------------------------
The ledger says `SW-B-H`, `SW-B-C` and `V-1` produce alias relations. None
existed. Coverage passed anyway, because it counts ANY target citing a
locator - it never checks that the target is the CONCEPT the adjudication
called for. So "duplicate -> relation" was satisfied by an unrelated assertion.

And the ten relations that did exist pointed `from_ref`/`to_ref` at free-form
legacy ids and source locators, never at a target `migration_key`. An alias
that does not resolve to a target identity neither preserves identity nor
prevents duplication - it is a note.

Now: `legacy_id` is the drawing id (which IS a legacy string, correctly), and
`target_key` must resolve to a real target record. Where no target identity
exists yet - a comparable-flat concept mints no occurrence, by design -
`target_pending` says so explicitly rather than pointing at something
convenient.

⚠️ ROUTES HAD NO CONTRACT AT ALL
--------------------------------
`route` had no required fields, so a blank route row would have passed, and
routes carried no phase, knowledge basis or value state. Worse, `RTE-SEWER`
asserted topology from `SS-K` to `SS-K2` while the migration's own assertion
says that connection is author-INFERRED and candidate. `topology_only` still
asserts connectivity - it is a statement about PATH, not about certainty - so
the uncertainty has to live in `value_state`.

    .venv\\Scripts\\python.exe tools/services/build_relations_and_routes.py
"""
from __future__ import annotations

import argparse
import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

REL_FIELDS = ["migration_key", "source_locators", "target_concept",
              "relation_kind", "legacy_id", "target_key", "target_pending",
              "notes"]

PENDING = ("no target identity exists yet: the concept is evidenced only by a "
           "comparable flat, so no occurrence is minted (design §3.0f). "
           "The alias resolves when one is.")

# legacy_id, source locator, relation_kind, target_key, note
RELATIONS = [
    ("V-2", "legacy_generator:tag:V-2", "alias_of", "",
     "Displays SV-K, the kitchen grille: H=218 on the tag against SV-K's "
     "MEASURED 2177, both citing 9e9b. " + PENDING),
    ("V-1", "legacy_generator:tag:V-1", "alias_of", "OCC-SV-T",
     "⚠ MISSING UNTIL NOW - the ledger adjudicated this as an alias and "
     "no relation existed. V-1 was INTENDED to display SV-T. Its H=218 and its "
     "photo citations do NOT migrate: both photographs show the KITCHEN grille "
     "on V2, and SV-T's own row says 'not yet measured'."),
    ("SV-VT", "legacy_generator:tag:SV-VT", "alias_of", "OCC-SV-VT",
     "The drawing tag for the canonical transfer opening."),
    ("SW-B-H", "legacy_generator:P1SVC:SW-B-H", "alias_of", "OCC-SW-B-H",
     "⚠ MISSING UNTIL NOW. The hot member of the SW-B assembly."),
    ("SW-B-C", "legacy_generator:P1SVC:SW-B-C", "alias_of", "OCC-SW-B-C",
     "⚠ MISSING UNTIL NOW. The cold member of the same assembly."),
    ("SS-B", "legacy_generator:P1SVC:SS-B", "alias_of",
     "OCC-service-outlets-SS-B", "The DN110 main stack in P1."),
    ("SH-B", "legacy_generator:P1SVC:SH-B", "alias_of", "",
     "The insulated riser. " + PENDING + " SH-B's existence here is candidate "
     "and its function unconfirmed, so it has no occurrence to alias."),
    ("P-S", "legacy_generator:PIPES:P-S", "alias_of", "",
     "Displays SS-K, the kitchen DN50 connection. " + PENDING),
    ("P-H", "legacy_generator:PIPES:P-H", "alias_of", "",
     "The hot member of the SW-K take-off pair. " + PENDING),
    ("P-C", "legacy_generator:PIPES:P-C", "alias_of", "",
     "The cold member of the same pair. " + PENDING),
    ("DN50", "legacy_generator:ROUTES:DN50", "alias_of", "RTE-SEWER",
     "`DN50` IS the `SEWER` object - the literal passes the same list, not a "
     "copy of it."),
    (u"ГВС-в", u"legacy_generator:ROUTES:ГВС-в",
     "alias_of", "RTE-BATH-W", "Passes the `BATH_W` object directly."),
    (u"DN50-в", u"legacy_generator:ROUTES:DN50-в", "alias_of",
     "RTE-BATH-S", "Passes the `BATH_S` object directly."),
    ("two sewer stacks", "legacy_comment:10#sewer_stacks_restated",
     "duplicate_of", "ASR-6-two-vertical-dn110-stacks",
     "⚠ WAS WRONGLY AN ASSERTION, and my own new duplicate->relation "
     "check caught it. The claim RESTATES "
     "legacy_comment:6#two_vertical_dn110_stacks; it is carried by that "
     "record, not by a second one saying the same thing."),
    ("SW-B heights", "legacy_comment:11#heights_from_csv", "duplicate_of",
     "OCC-SW-B-H",
     "⚠ WAS WRONGLY AN ASSERTION. A `duplicate` adjudication produces a "
     "RELATION, not a property claim - the heights are carried by "
     "legacy_csv:service_outlets:SW-B, not by a second record stating them "
     "again."),
]

ROUTE_FIELDS = ["migration_key", "source_locators", "target_concept",
                "route_kind", "route_state", "from_ref", "to_ref",
                "knowledge_basis", "value_state", "scope_kind", "scope_ref",
                "scope_phase", "observation_refs", "notes"]

# key, locator, kind, from, to, basis, state, note
ROUTES = [
    ("RTE-ROUTES-GVS", u"legacy_generator:ROUTES:ГВС",
     "hot_water", "P1", "SW-K", "stated", "asserted",
     "The owner's own route, corrected by him to «lower, further from V1, "
     "hugging G4b». The RUN is his; the coordinates are the author's and "
     "are ASR-5-derived-route-y-coordinates, derived/candidate."),
    ("RTE-ROUTES-HVS", u"legacy_generator:ROUTES:ХВС",
     "cold_water", "P1", "SW-K", "stated", "asserted",
     "The parallel run. Two INDEPENDENT routes, one turn each - not one line "
     "drawn twice."),
    ("RTE-ROUTES-HVS-v", u"legacy_generator:ROUTES:ХВС-в",
     "cold_water", "P1", "bath", "derived", "candidate",
     "⚠ NOT AN INDEPENDENTLY ROUTED PIPE: the literal is BATH_W shifted 5 "
     "units so two lines do not overlap ON THE SHEET. Geometry not carried; "
     "only the topology is supported, by legacy_comment:7."),
    ("RTE-SEWER", "legacy_generator:SEWER", "sewer", "SS-K", "SS-K2",
     "derived", "candidate",
     "⚠ STATE CORRECTED: this was `topology_only`/unqualified while the "
     "migration's own ASR-12-kitchen-dn50-connects-to-it says the connection "
     "is author-INFERRED and candidate, and ASR-5-dn50-continuation-unknown "
     "records that NO photo shows it. `topology_only` asserts a PATH; it is "
     "not an uncertainty state, so the uncertainty belongs here."),
    ("RTE-BATH-W", "legacy_generator:BATH_W", "water", "P1", "bath", "stated",
     "candidate",
     "TOPOLOGY, NOT A SETTING-OUT - the owner: «рас"
     "кладка может "
     "отличаться, "
     "подход тот же"
     "»."),
    ("RTE-BATH-S", "legacy_generator:BATH_S", "sewer", "bath", "SS-B",
     "observed", "candidate",
     "From b83a - a COMPARABLE flat's annotated photo, so the topology "
     "projects here as a candidate."),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--drafts", default=DRAFTS)
    a = ap.parse_args()

    with io.open(os.path.join(a.drafts, "relations.csv"), "w",
                 encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REL_FIELDS)
        writer.writeheader()
        for legacy, src, kind, target, note in RELATIONS:
            writer.writerow({
                "migration_key": "REL-%s" % legacy.replace(" ", "-"),
                "source_locators": src, "target_concept": "relation",
                "relation_kind": kind, "legacy_id": legacy,
                "target_key": target,
                "target_pending": "" if target else "yes", "notes": note})

    with io.open(os.path.join(a.drafts, "routes.csv"), "w", encoding="utf-8",
                 newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=ROUTE_FIELDS)
        writer.writeheader()
        for key, src, kind, frm, to, basis, state, note in ROUTES:
            writer.writerow({
                "migration_key": key, "source_locators": src,
                "target_concept": "route", "route_kind": kind,
                "route_state": "topology_only", "from_ref": frm, "to_ref": to,
                "knowledge_basis": basis, "value_state": state,
                "scope_kind": "apartment", "scope_ref": "ours",
                "scope_phase": "existing", "notes": note})

    print("wrote %d relation(s) and %d route(s)" % (len(RELATIONS), len(ROUTES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
