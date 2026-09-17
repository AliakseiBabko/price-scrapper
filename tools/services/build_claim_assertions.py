#!/usr/bin/env python3
"""Rebuild the claim-derived assertions from an EXPLICIT, reviewed table.

⚠️ WHY THIS FILE EXISTS
-----------------------
The first version of these 34 rows was produced by a keyword classifier -
`prop_for()`, which guessed an assertion `property` from substrings and
defaulted to `arrangement`. Review found three things wrong with that at once:

  1. the guesses were WRONG (a bathroom topology claim became `vertical`; a
     "no horizontal main" claim became `position_along`);
  2. the columns CONTRADICTED THEIR OWN NOTES - rows whose notes said
     "knowledge_basis=derived, value_state=candidate" were written
     `stated`/`asserted`, and a row whose note said "becomes an assertion with
     value_state=unknown" was written `asserted`;
  3. the classifier lived in a scratchpad, so the transformation was NOT
     REPRODUCIBLE from the repository at all.

⚠️ AND IT LOST A DISPUTE. `legacy_comment:2#two_outlets_on_g7` and
`legacy_comment:4#zero_outlets_on_middle_living_wall` CONTRADICT each other -
the ledger says so explicitly - and the classifier wrote both `asserted`,
silently resolving a live disagreement in favour of both sides at once. They
are now `disputed` and name each other.

There is no classifier here. Every row is written out, and each says what it is
ABOUT (`subject_key` for a target record, `subject_element` for a model
element) and, where it counts things, WHAT it counts (`device_class`) - because
"G7 has 2" and "G7 has 0" are not a contradiction until you know one means
outlets and the other switches.

    .venv\\Scripts\\python.exe tools/services/build_claim_assertions.py
"""
from __future__ import annotations

import argparse
import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")
CLAIMS = os.path.join(REPO, "_Inbox", "migration", "services_claim_inventory.csv")

FIELDS = ["migration_key", "source_locators", "new_decision_by",
          "target_concept", "subject_key", "subject_element", "device_class",
          "property", "value", "value_type", "polarity", "knowledge_basis",
          "value_state", "scope_kind", "scope_ref", "scope_phase",
          "disputed_with", "observation_refs", "notes"]

# key, claim locator, subject_key, subject_element, device_class, property,
# value, value_type, basis, state, scope_ref, disputed_with, note
TABLE = [
    ("ASR-W6-EXIST", "legacy_comment:4#living_room_switch_at_o10", "OCC-W6",
     "", "switch", "existence", "true", "bool", "stated", "asserted", "ours",
     "", "Owner testimony about THIS apartment - currently the only route to "
     "an established existence."),
    ("ASR-ROUTE-V2-RETRACTED", "legacy_comment:5#diagonal_route_through_v2",
     "RTE-ROUTES-GVS", "", "", "route_state", "straight through V2", "string",
     "derived", "retracted", "ours", "",
     "Round 1 of the kitchen water run, withdrawn the same day: V2 is a "
     "concrete ventilation shaft. Kept so the record of what was tried, and "
     "why it was wrong, survives."),
    ("ASR-6-dn110-horizontal-main", "legacy_comment:6#dn110_horizontal_main",
     "", "flat", "sewer_stack", "route_state", "6.3 m DN110 horizontal main "
     "P2 to P1", "string", "derived", "retracted", "ours", "",
     "A main I built and the owner retracted. History."),
    ("ASR-6-two-vertical-dn110-stacks",
     "legacy_comment:6#two_vertical_dn110_stacks", "", "flat", "sewer_stack",
     "count", "2", "int", "stated", "asserted", "ours", "",
     "Two DN110 stacks, each running the full height of the building."),
    ("ASR-6-no-horizontal-dn110-main",
     "legacy_comment:6#no_horizontal_dn110_main", "", "flat",
     "horizontal_main", "count", "0", "int", "stated", "asserted", "ours", "",
     "A scoped count of ZERO. Negation is POLARITY, not a different kind of "
     "fact (design §3.0e) - and a count of zero states it more plainly "
     "than a negated sentence would."),
    ("ASR-10-second-valve-node", "legacy_comment:10#second_valve_node", "",
     "P1", "valve", "count", "2", "int", "derived", "retracted", "ours", "",
     "I heard «two switch points» as two valve groups and built a "
     "fitting out of the owner's word. Retracted the same day."),
    ("ASR-10-single-valve-node", "legacy_comment:10#single_valve_node", "",
     "P1", "valve", "count", "1", "int", "stated", "asserted", "ours", "",
     "«only ONE valve node, in the water closet»."),
    # ⚠️ THE LIVE CONTRADICTION. Both are genuine owner statements; the
    # migration may not pick one.
    ("ASR-2-two-outlets-on-g7", "legacy_comment:2#two_outlets_on_g7", "", "G7",
     "outlet", "count", "2", "int", "stated", "disputed", "ours",
     "ASR-4-zero-outlets-on-middle-living-wall",
     "⚠ DISPUTED, and the earlier generated row wrongly said `asserted`. "
     "This contradicts ASR-4-zero-outlets-on-middle-living-wall. Both are real "
     "owner statements, so both survive as sources; the VALUE stays disputed "
     "until he says which wall face each meant. Block 4's opening words read "
     "either as «this is NOT about G7» or «nothing on "
     "G7» - under the first reading there is no contradiction at all."),
    ("ASR-2-zero-switches-on-g7", "legacy_comment:2#zero_switches_on_g7", "",
     "G7", "switch", "count", "0", "int", "stated", "asserted", "ours", "",
     "CORROBORATED by ASR-4-zero-switches-on-middle-living-wall: the two "
     "blocks AGREE on switches even while they disagree on outlets. "
     "`device_class` is what makes that visible - without it, «G7 has "
     "2» and «G7 has 0» look like the same contradiction twice."),
    ("ASR-2-prior-switch-placement", "legacy_comment:2#prior_switch_placement",
     "", "G7", "switch", "count", "1", "int", "derived", "retracted", "ours",
     "", "The author's earlier placement, withdrawn by the owner."),
    ("ASR-3-zero-outlets-on-mc", "legacy_comment:3#zero_outlets_on_mc", "",
     "MC", "outlet", "count", "0", "int", "stated", "asserted", "ours", "",
     "«there are no outlets on the wall with the window, not a trace of "
     "it» - owner testimony about OUR flat, corroborated independently by "
     "OBS-MC-EMPTY-109. ⚠ NOT the substrate rule: MC is aerated block and "
     "could be chased. This is an observed absence."),
    ("ASR-3-s16-removed", "legacy_comment:3#s16_removed", "", "MC", "outlet",
     "arrangement", "S16 drawn on MC", "string", "derived", "retracted",
     "ours", "", "The placement withdrawn by the statement above."),
    ("ASR-4-zero-switches-on-middle-living-wall",
     "legacy_comment:4#zero_switches_on_middle_living_wall", "", "G7",
     "switch", "count", "0", "int", "stated", "asserted", "ours", "",
     "Agrees with ASR-2-zero-switches-on-g7."),
    ("ASR-4-zero-outlets-on-middle-living-wall",
     "legacy_comment:4#zero_outlets_on_middle_living_wall", "", "G7", "outlet",
     "count", "0", "int", "stated", "disputed", "ours",
     "ASR-2-two-outlets-on-g7",
     "⚠ DISPUTED - the other half. The block's own scope is AMBIGUOUS and "
     "that ambiguity is the whole dispute. NEEDS THE OWNER: which wall, and "
     "which face."),
    ("ASR-5-route-belongs-lower-hugging-g4b",
     "legacy_comment:5#route_belongs_lower_hugging_g4b", "", "flat", "",
     "arrangement", "lower, further from V1, hugging G4b", "string", "stated",
     "asserted", "ours", "",
     "OWNER INTENT in his own words. Deliberately SEPARATE from the numbers "
     "below - he said «lower, hugging G4b», not a coordinate."),
    ("ASR-5-derived-route-y-coordinates",
     "legacy_comment:5#derived_route_y_coordinates", "RTE-ROUTES-GVS", "", "",
     "position_along", "y=180/186", "string", "derived", "candidate", "ours",
     "", "⚠ CORRECTED: the generated row said `stated`/`asserted` while "
     "its own note said derived/candidate. These numbers are the DRAWING "
     "AUTHOR's, not part of the owner's quoted decision."),
    ("ASR-5-dogleg-turn", "legacy_comment:5#dogleg_turn", "RTE-ROUTES-GVS", "",
     "", "route_state", "an additional turn", "string", "derived", "retracted",
     "ours", "", "The author's dogleg, withdrawn on the owner's objection."),
    ("ASR-5-two-independent-one-turn-routes",
     "legacy_comment:5#two_independent_one_turn_routes", "", "flat", "",
     "arrangement", "two independent routes, one turn each", "string",
     "stated", "asserted", "ours", "",
     "A service pair is two runs, not one run drawn twice."),
    ("ASR-5-dn50-run-observed-to-chase",
     "legacy_comment:5#dn50_run_observed_to_chase", "RTE-SEWER", "", "",
     "route_state", "runs along the wall base into a chase", "string",
     "observed", "asserted", "53", "",
     "⚠ SCOPED TO 53, not ours: photo 930d is apartment 53. Observed "
     "there; its projection here is candidate."),
    ("ASR-5-dn50-continuation-unknown",
     "legacy_comment:5#dn50_continuation_unknown", "RTE-SEWER", "", "",
     "route_state", "", "string", "unknown", "unknown", "ours", "",
     "⚠ CORRECTED: the generated row said `stated`/`asserted` while its "
     "own note said this becomes an assertion with value_state=unknown. No "
     "photo shows how the DN50 reaches the stack. An explicit UNKNOWN, not an "
     "omission - drawing the branch would be inventing an element."),
    ("ASR-7-bathroom-service-topology",
     "legacy_comment:7#bathroom_service_topology", "", "P1", "", "arrangement",
     "risers in the niche, meters at mid height, services leave low", "string",
     "stated", "asserted", "ours", "",
     "⚠ PROPERTY CORRECTED from `vertical`, which the keyword classifier "
     "guessed from the word «height». This is an arrangement, not a "
     "measurement."),
    ("ASR-7-applied-from-comparable-flat",
     "legacy_comment:7#applied_from_comparable_flat", "", "P1", "",
     "arrangement", "topology taken from an annotated photo of another flat",
     "string", "observed", "asserted", "53", "",
     "⚠ SCOPED TO 53. The owner annotated a photo of ANOTHER flat; its "
     "application here is a projection."),
    ("ASR-7-topology-not-setting-out",
     "legacy_comment:7#topology_not_setting_out", "RTE-BATH-W", "", "",
     "route_state", "topology_only", "string", "stated", "asserted", "ours",
     "", "The generator may not treat this as placement."),
    ("ASR-7-positions-indicative", "legacy_comment:7#positions_indicative", "",
     "P1", "", "position_along", "indicative", "string", "stated", "candidate",
     "ours", "", "value_state=candidate for every position derived from this "
     "block, by the owner's own word."),
    ("ASR-11-p1-hot-cold-and-valve", "legacy_comment:11#p1_hot_cold_and_valve",
     "ASM-ZONE-P1", "", "riser", "count", "2", "int", "stated", "asserted",
     "ours", "", "Hot AND cold, owner-stated; his «switch» is the "
     "shut-off valve."),
    ("ASR-11-p1-internal-arrangement",
     "legacy_comment:11#p1_internal_arrangement", "ASM-ZONE-P1", "", "",
     "arrangement", "sewer mid-way between the walls, valve node nearer V1",
     "string", "stated", "asserted", "ours", "",
     "Owner-stated arrangement, 2026-09-07."),
    ("ASR-11-derived-stack-y-131", "legacy_comment:11#derived_stack_y_131",
     "OCC-service-outlets-SS-B", "", "", "position_along", "y=131", "string",
     "derived", "candidate", "ours", "",
     "⚠ CORRECTED to derived/candidate. Computed by the author from the "
     "owner's QUALITATIVE arrangement; he gave no number."),
    ("ASR-11-sh-b-south-end-assumed",
     "legacy_comment:11#sh_b_south_end_assumed", "", "SH-B", "riser",
     "position_along", "south end of P1", "string", "assumed", "candidate",
     "ours", "",
     "⚠ CORRECTED to assumed/candidate. The owner's statement does not "
     "mention SH-B at all."),
    ("ASR-12-second-sewer-stack-behind-v2",
     "legacy_comment:12#second_sewer_stack_behind_v2", "OCC-P1SVC-SS-K2", "",
     "sewer_stack", "existence", "true", "bool", "stated", "asserted", "ours",
     "", "Owner-supported in the same block: «two sewage pipes, the "
     "transit from the top of the building to the bottom»."),
    ("ASR-12-kitchen-dn50-connects-to-it",
     "legacy_comment:12#kitchen_dn50_connects_to_it", "RTE-SEWER", "", "",
     "route_state", "connects to SS-K2", "string", "derived", "candidate",
     "ours", "",
     "⚠ CORRECTED to derived/candidate. INFERRED by the author, not "
     "stated by the owner - and ASR-5-dn50-continuation-unknown records that "
     "no photo shows the connection."),
    ("ASR-12-no-horizontal-main-needed",
     "legacy_comment:12#no_horizontal_main_needed", "", "flat",
     "horizontal_main", "count", "0", "int", "derived", "asserted", "ours", "",
     "⚠ PROPERTY CORRECTED from `position_along`. Corroborates "
     "ASR-6-no-horizontal-dn110-main."),
    ("ASR-W6-HOST-G6", "legacy_comment:4#living_room_switch_at_o10", "OCC-W6",
     "", "switch", "position_along", "G6", "string", "derived", "candidate",
     "ours", "",
     "The substrate rule DISPROVED R5; it does not prove G6. O10's south edge "
     "is touched by G6 cross_hi, R4 end_to and R5 end_to, and G6 is the only "
     "aerated block among them. A constraint that eliminates two of three "
     "options has still observed nothing."),
]

# ⚠️ These two are NEW OWNER DECISIONS, not legacy sources. The generated rows
# borrowed an unrelated locator - the old W6 statement and E-KL-LIGHT - purely
# to satisfy coverage, which manufactured false provenance. They carry
# `new_decision_by` instead, which the coverage gate accepts as an explicit
# alternative to a locator.
DECISIONS = [
    ("ASR-CEILING-CAST-IN", "owner, 2026-09-17 (cast-in clarification)", "",
     "slabs", "light_point", "installation_method", "cast_in", "enum",
     "stated", "asserted", "ours", "existing",
     "«a constructor is able to include wiring in the concrete while "
     "pouring it... this is how it works for the ceiling». This is why a "
     "concrete host is legitimate for the existing ceiling outlets, and why "
     "the substrate rule needed an installation_method axis."),
    ("ASR-REWIRE-TOPOLOGY", "owner, 2026-09-17 (full rewire decision)", "",
     "flat", "", "arrangement",
     "board near the entrance; distribution through the ceiling; drops down "
     "the wall; drops exclusively in aerated block", "string", "stated",
     "asserted", "ours", "new",
     "⚠ THE PLANNED TOPOLOGY, recorded as ONE arrangement claim so it is "
     "not mistaken for four separate facts. The earlier row recorded only "
     "`installation_method=chased` and cited an unrelated W6 locator - it "
     "encoded neither the board, the ceiling distribution, the drops nor the "
     "substrate requirement, so calling it a model constraint overstated what "
     "had landed."),
    ("ASR-REWIRE-SUBSTRATE", "owner, 2026-09-17 (full rewire decision)", "",
     "flat", "", "installation_method", "chased", "enum", "stated",
     "asserted", "ours", "new",
     "Every new drop is CHASED - a retrofit cannot cast into concrete already "
     "poured - and exclusively into aerated block. Enforced by "
     "check_locator_geometry for phase=proposed as a WHITELIST, not as "
     "«not concrete»."),
    ("ASR-EXISTING-IS-REFERENCE", "owner, 2026-09-17 (full rewire decision)",
     "", "flat", "", "arrangement",
     "the existing installation is reference only; it does not constrain the "
     "new layout", "string", "stated", "asserted", "ours", "existing",
     "«this is the current placement... just for reference, for testing "
     "how to construct electric wiring». Everything migrated in this pass "
     "is the EXISTING phase and binds nothing."),
]


def build():
    rows = []
    for (key, src, subj, elem, dev, prop, value, vtype, basis, state, scope,
         disputed, note) in TABLE:
        rows.append({
            "migration_key": key, "source_locators": src, "new_decision_by": "",
            "target_concept": "assertion", "subject_key": subj,
            "subject_element": elem, "device_class": dev, "property": prop,
            "value": value, "value_type": vtype, "polarity": "affirm",
            "knowledge_basis": basis, "value_state": state,
            "scope_kind": "apartment", "scope_ref": scope,
            "scope_phase": "existing", "disputed_with": disputed,
            "observation_refs": "", "notes": note})
    for (key, author, subj, elem, dev, prop, value, vtype, basis, state,
         scope, phase, note) in DECISIONS:
        rows.append({
            "migration_key": key, "source_locators": "",
            "new_decision_by": author, "target_concept": "assertion",
            "subject_key": subj, "subject_element": elem, "device_class": dev,
            "property": prop, "value": value, "value_type": vtype,
            "polarity": "affirm", "knowledge_basis": basis,
            "value_state": state, "scope_kind": "apartment",
            "scope_ref": scope, "scope_phase": phase, "disputed_with": "",
            "observation_refs": "", "notes": note})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(DRAFTS, "assertions.csv"))
    a = ap.parse_args()

    claims = set()
    with io.open(CLAIMS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            claims.add(row["claim_locator"])

    rebuilt = build()
    keys = set(r["migration_key"] for r in rebuilt)
    for row in rebuilt:
        for cite in (row["source_locators"] or "").split(";"):
            cite = cite.strip()
            if cite and cite not in claims:
                print("FAIL %s cites %s, which the claim inventory does not "
                      "carry" % (row["migration_key"], cite))
                return 1

    kept = []
    if os.path.exists(a.out):
        with io.open(a.out, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["migration_key"] not in keys:
                    kept.append(row)

    with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in kept + rebuilt:
            writer.writerow(dict((f, row.get(f, "")) for f in FIELDS))
    print("rebuilt %d claim assertion(s) + %d owner decision(s); kept %d other"
          % (len(TABLE), len(DECISIONS), len(kept)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
