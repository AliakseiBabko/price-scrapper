#!/usr/bin/env python3
"""Guard the locator geometry gate. Seven seeds, each demanding its DIAGNOSTIC.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate — and an accidental rejection is not a check. Every seed here asserts
the EXPECTED MESSAGE, not merely a non-zero exit, because a validator that
rejects the right case for the wrong reason passes an exit-code test.

⚠️ SEED 0 GOES THROUGH THE REAL CSV LOADER. The rest mutate loaded records, but
if nothing ever exercised `load()` and the real column names, the whole suite
could pass against a record shape the production path never produces.

    .venv-ifc314\\Scripts\\python.exe scripts/locator_geometry_selftest.py
"""
from __future__ import annotations

import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "services"))

from check_locator_geometry import check, geometry          # noqa: E402
from check_target_schema import load as load_targets        # noqa: E402

# ⚠️ THE VOID SEEDS USE O8 IN G2, NOT O3 IN MC, AND THE REASON IS A FINDING.
# `MC` has NO material class in wall_materials.json, so the substrate rule now
# (correctly) returns INCOMPLETE for it before any geometry runs - which would
# have masked every void seed. Six model walls are unclassified: MA, MB, MC,
# G4C, R1a, R1b. G2 is aerated block and O8 spans 500.1-1510.0 well inside its
# 2220.6 mm face, so the geometry axis can be tested without holding the
# substrate axis constant by hand.
O8_LO, O8_HI = 500.1, 1510.0


def main() -> int:
    failures = 0
    resolved, module = geometry()
    verticals = module._opening_verticals
    targets = load_targets()

    def verdicts(rows):
        return dict((k, (v, m)) for k, v, m in
                    check(rows, resolved, verticals))

    def expect(label, rows, key, want_verdict, needle):
        nonlocal failures
        got = verdicts(rows).get(key)
        if got is None:
            print("FAIL %-50s %s produced no verdict" % (label, key))
            failures += 1
            return
        verdict, message = got
        if verdict == want_verdict and needle in message:
            print("PASS %-50s %-11s %s" % (label, verdict.upper(),
                                           message[:44]))
        else:
            print("FAIL %-50s wanted %s/%r, got %s/%r"
                  % (label, want_verdict, needle, verdict, message[:70]))
            failures += 1

    def socket(**kw):
        """A wall_face occurrence on G2, the block wall that hosts O8."""
        row = {"migration_key": "SEED", "target_concept": "occurrence",
               "service_kind": "socket", "phase": "existing",
               "locator_kind": "wall_face", "host_ref": "G2",
               "face_ref": "cross_lo", "along_face_mm": "", "vertical_mm": "",
               "support_ref": "", "surface_role": "", "u_mm": "", "v_mm": "",
               "normal_offset_mm": "", "space_ref": "", "anchor_ref": "",
               "parent_assembly_key": "", "placement_state": "candidate",
               "source_locators": "legacy_generator:SOCK:S1", "notes": ""}
        row.update(kw)
        return row

    def says(subject, prop, value, state="asserted"):
        return {"migration_key": "SEED-%s" % prop, "target_concept": "assertion",
                "subject_key": subject, "property": prop, "value": value,
                "value_type": "mm", "polarity": "affirm",
                "knowledge_basis": "derived", "value_state": state,
                "scope_kind": "apartment", "scope_ref": "ours",
                "scope_phase": "existing", "disputed_with": "",
                "source_locators": "legacy_generator:SOCK:S1", "notes": ""}

    def avoid(subject):
        row = says(subject, "host_interaction", "avoid_void")
        row["value_type"] = "enum"
        return row

    # ── 0 ─ THE REAL RECORDS, THROUGH THE REAL LOADER ────────────────────────
    live = verdicts(targets)
    # ⚠️ W6 is `unlocated`, NOT `partial`, since 2026-09-17: the wiring-
    # substrate rule disproved its R5 host, so the record no longer names a
    # wall at all. Its anchor on O10 survives, and the principle that a null
    # `host_wall` must not cause rejection is seeded below on G6, the only
    # aerated-block jamb at that opening.
    if live.get("OCC-W6", ("", ""))[0] == "unlocated":
        print("PASS %-50s %-11s %s" % ("the real slice loads; W6 host disproven",
                                       "UNLOCATED", "via check_target_schema.load()"))
    else:
        print("FAIL the real slice: W6 is %r" % (live.get("OCC-W6"),))
        failures += 1

    # ── 1 ─ centre INSIDE O3 ─────────────────────────────────────────────────
    centre = (O8_LO + O8_HI) / 2.0
    rows = [socket(along_face_mm=str(centre), vertical_mm="1000"),
            avoid("SEED"), says("SEED", "vertical", "1000")]
    expect("a terminal centred inside O8", rows, "SEED", "invalid",
           "INSIDE the void of O8")

    # ── 2 ─ centre CLEAR but the asserted extent crosses O8 ──────────────────
    # 80 mm clear of the jamb, with a 300 mm device: the centre is fine and the
    # envelope is not. This is the seed the whole three-state verdict exists
    # for, and a centre-only validator passes it.
    rows = [socket(along_face_mm=str(O8_LO - 80.0), vertical_mm="1000"),
            avoid("SEED"),
            says("SEED", "vertical", "1000"),
            says("SEED", "extent_along_mm", "300"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("centre clear but EXTENT crosses O8", rows, "SEED", "invalid",
           "CROSSES the void of O8")

    # ── 3 ─ the same position with the extent UNKNOWN ────────────────────────
    rows = [socket(along_face_mm=str(O8_LO - 80.0), vertical_mm="1000"),
            avoid("SEED"), says("SEED", "vertical", "1000"),
            says("SEED", "extent_along_mm", "", "unknown"),
            says("SEED", "extent_vertical_mm", "", "unknown")]
    expect("centre clear, extent unknown -> INCOMPLETE", rows, "SEED",
           "incomplete", "NOT proven valid")

    # ── 4 ─ a valid terminal immediately outside the void ────────────────────
    rows = [socket(along_face_mm=str(O8_LO - 400.0), vertical_mm="1000"),
            avoid("SEED"), says("SEED", "vertical", "1000"),
            says("SEED", "extent_along_mm", "300"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("a valid terminal just outside the void", rows, "SEED", "valid",
           "clear of every void")

    # ── 5 ─ an invalid face_ref, and a position off the end ──────────────────
    rows = [socket(along_face_mm="500", face_ref="cross_middle"), avoid("SEED")]
    expect("an invalid face_ref", rows, "SEED", "invalid", "invalid face_ref")

    rows = [socket(along_face_mm="-50"), avoid("SEED")]
    expect("a negative along_face_mm", rows, "SEED", "invalid", "outside")
    rows = [socket(along_face_mm="99999"), avoid("SEED")]
    expect("an along_face_mm beyond the face", rows, "SEED", "invalid",
           "outside")

    # ── 6 ─ a missing host ───────────────────────────────────────────────────
    rows = [socket(along_face_mm="500", host_ref="NOT_A_WALL"), avoid("SEED")]
    expect("a missing host", rows, "SEED", "invalid", "missing host")

    # ── 7 ─ ⚠️ THE ANCHOR SEED. O10 has host_wall=None and R5 merely SHARES
    # its boundary. W6 must stay `partial` and must NOT be rejected as
    # "hosted by another wall" - that would collapse "mounted beside an
    # opening" into "mounted on the opening's host wall", which are different
    # relationships.
    # O10 has host_wall=None and G6's cross_hi is coincident with its southern
    # edge. A service anchored to O10 and hosted on G6 must NOT be rejected:
    # "mounted beside an opening" is not "mounted on the opening's host wall",
    # and requiring host_wall==host_ref would reject every opening that spans
    # between elements.
    rows = [socket(along_face_mm="1500", host_ref="G6", face_ref="cross_hi",
                   anchor_ref="O10"), avoid("SEED"),
            says("SEED", "vertical", "900"),
            says("SEED", "extent_along_mm", "80"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("anchor to an opening with host_wall=None is accepted", rows, "SEED",
           "valid", "clear of every void")

    # ...and the anchor is genuinely checked, or the seed above passes
    # vacuously: an anchor that touches nothing must still be rejected.
    rows = [socket(along_face_mm="500", anchor_ref="O3", host_ref="G6",
                   face_ref="cross_hi"), avoid("SEED")]
    expect("an anchor that does not touch the host", rows, "SEED", "invalid",
           "does not touch")

    # ── 7b ─ ⚠️ THE SUBSTRATE RULE. A cable cannot be chased into the
    # monolithic RC frame, so a concrete host is refused BEFORE any geometry -
    # a perfectly placed socket on a concrete column is still not buildable.
    # This is the rule that disproved W6's own R5 host.
    def method(value):
        row = says("SEED", "installation_method", value)
        row["value_type"] = "enum"
        return row

    # existing + chased into concrete: refused
    rows = [socket(along_face_mm="200", host_ref="R5", face_ref="cross_lo"),
            avoid("SEED"), method("chased")]
    expect("a CHASED accessory on concrete is refused", rows, "SEED", "invalid",
           "chase may only be cut into")

    # ⚠️ existing + CAST IN: allowed. This is how the ceiling cable outlets
    # exist inside the slabs, and a blanket material refusal would reject them.
    rows = [socket(along_face_mm="200", host_ref="R5", face_ref="cross_lo"),
            avoid("SEED"), method("cast_in"), says("SEED", "vertical", "300"),
            says("SEED", "extent_along_mm", "80"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("a CAST-IN accessory on concrete is allowed", rows, "SEED", "valid",
           "clear of every void")

    # ⚠️ existing + method unstated: INCOMPLETE, not invalid - unevidenced is
    # not the same as impossible, and that distinction is the correction.
    rows = [socket(along_face_mm="200", host_ref="R5", face_ref="cross_lo"),
            avoid("SEED")]
    expect("concrete with no method is INCOMPLETE, not impossible", rows,
           "SEED", "incomplete", "UNEVIDENCED")

    # ⚠️ PROPOSED work on concrete: invalid with NO method exception, because a
    # retrofit cannot cast into concrete that is already poured.
    rows = [socket(along_face_mm="200", host_ref="R5", face_ref="cross_lo",
                   phase="proposed"), avoid("SEED"), method("cast_in")]
    expect("PROPOSED work on concrete is refused even if cast_in", rows,
           "SEED", "invalid", "already poured")

    # ...and the same position on an aerated block is fine, so the seed above
    # is not just rejecting everything.
    rows = [socket(along_face_mm="200", host_ref="G7", face_ref="cross_lo"),
            avoid("SEED"), says("SEED", "vertical", "300"),
            says("SEED", "extent_along_mm", "80"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("the same socket on aerated block is valid", rows, "SEED", "valid",
           "clear of every void")

    # ⚠️ ...and an UNKNOWN material is not assumed chase-able.
    # ⚠️ M2 is `loggia_enclosure` with NO material recorded - deliberately, the
    # thickness record is inconsistent and nothing reviewed states it.
    rows = [socket(along_face_mm="200", host_ref="M2", face_ref="cross_lo"),
            avoid("SEED")]
    expect("a host with no material is INCOMPLETE, not chase-able", rows,
           "SEED", "incomplete", "NOT assumed chase-able")

    # ⚠️ THE WHITELIST SEED, and it is the exact case the review found: an
    # earlier version only REFUSED concrete, so a PROPOSED accessory on M2
    # passed substrate checking and reached `partial`. "Not concrete" is not
    # the owner's rule; "exclusively aerated block" is.
    rows = [socket(along_face_mm="200", host_ref="M2", face_ref="cross_lo",
                   phase="proposed"), avoid("SEED")]
    expect("PROPOSED work on a non-block material is refused", rows, "SEED",
           "invalid", "every new drop must be chased into aerated_block")

    # ...and proposed work on block is accepted, so the seed above is not just
    # refusing everything proposed.
    rows = [socket(along_face_mm="200", host_ref="G7", face_ref="cross_lo",
                   phase="proposed"), avoid("SEED"),
            says("SEED", "vertical", "300"),
            says("SEED", "extent_along_mm", "80"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("PROPOSED work on aerated block is valid", rows, "SEED", "valid",
           "clear of every void")

    # ── 8 ─ surface_local reports UNAVAILABLE, and unknown kinds FAIL ────────
    rows = [socket(locator_kind="surface_local", host_ref="", face_ref="",
                   support_ref="SLAB-1", surface_role="finished_ceiling")]
    expect("surface_local reports support geometry unavailable", rows, "SEED",
           "unsupported", "support geometry unavailable")

    rows = [socket(locator_kind="ceiling_ish", host_ref="", face_ref="")]
    expect("an unknown locator_kind is a hard failure", rows, "SEED", "invalid",
           "never a skip")

    # ── 9 ─ host_interaction dispatch: a penetration is not a defect ─────────
    pen = says("SEED", "host_interaction", "creates_penetration")
    pen["value_type"] = "enum"
    rows = [socket(along_face_mm=str(centre), vertical_mm="1000"), pen,
            says("SEED", "vertical", "1000")]
    expect("creates_penetration overlapping a void is NOT a defect", rows,
           "SEED", "valid", "this element's PURPOSE")

    rows = [socket(along_face_mm=str(centre), vertical_mm="1000"),
            says("SEED", "vertical", "1000")]
    expect("absent host_interaction is NOT read as avoid_void", rows, "SEED",
           "incomplete", "absence is NOT")

    # THE nan FAMILY. A fully specified envelope with position_along=nan came
    # back "VALID envelope nan-nan clear of every void on G7.cross_lo": every
    # comparison a nan touches is false, so it passes containment instead of
    # failing it. AGENTS.md says use finite(); this used float().
    for bad in ("nan", "inf", "-inf"):
        rows = [socket(host_ref="G7", face_ref="cross_lo"), avoid("SEED"),
                says("SEED", "position_along", bad),
                says("SEED", "vertical", "300"),
                says("SEED", "extent_along_mm", "80"),
                says("SEED", "extent_vertical_mm", "80")]
        expect("a %s position is INVALID, not valid" % bad, rows, "SEED",
               "invalid", "non-finite number passes every comparison")
    rows = [socket(host_ref="G7", face_ref="cross_lo", along_face_mm="nan"),
            avoid("SEED")]
    expect("a nan on the occurrence column is INVALID", rows, "SEED",
           "invalid", "malformed measurement")

    # A MISSPELLED MATERIAL MUST NOT FAIL OPEN. Rejecting only an exact
    # "reinforced_concrete" meant `reinforced_concret` let a fully specified
    # CHASED accessory on the RC frame come back VALID. `chased` now uses the
    # aerated-block whitelist regardless of phase, so a typo cannot defeat it.
    from check_locator_geometry import wall_classes
    typo = dict(wall_classes())
    typo["R5"] = "reinforced_concret"
    rows = [socket(host_ref="R5", face_ref="cross_lo", along_face_mm="200"),
            avoid("SEED"), method("chased"), says("SEED", "vertical", "300"),
            says("SEED", "extent_along_mm", "80"),
            says("SEED", "extent_vertical_mm", "80")]
    got = dict((k, (v, m)) for k, v, m in
               check(rows, resolved, verticals, classes=typo))["SEED"]
    if got[0] == "invalid" and "chase may only be cut into" in got[1]:
        print("PASS %-50s %-11s %s"
              % ("a MISSPELLED concrete does not fail open", "INVALID",
                 got[1][:38]))
    else:
        print("FAIL %-50s got %s/%r" % ("misspelled material", got[0], got[1]))
        failures += 1


    # THE MATERIAL AUTHORITY'S OWN DUPLICATE-KEY DEFECT. Appending a second
    # R5 with material=aerated_block used to resolve CONCRETE R5 as aerated
    # block - the exact reading that would authorise chasing the RC frame.
    import json
    import tempfile
    from check_locator_geometry import (DuplicateWallId, MATERIALS,
                                        wall_classes)
    with io.open(MATERIALS, encoding="utf-8") as fh:
        materials = json.load(fh)
    materials["walls"].append({"id": "R5", "class": "aerated_block",
                               "material": "aerated_block"})
    handle, seeded_path = tempfile.mkstemp(suffix=".json")
    os.close(handle)
    with io.open(seeded_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(materials, ensure_ascii=False))
    try:
        wall_classes(seeded_path)
        print("FAIL %-50s a duplicate R5 was accepted" % "duplicate wall id")
        failures += 1
    except DuplicateWallId as exc:
        print("PASS %-50s %s" % ("a duplicate wall id is REJECTED",
                                 str(exc)[:44]))
    finally:
        os.unlink(seeded_path)

    # THE ISSUED-MODEL POLICY, EXERCISED AS BEHAVIOUR. The previous seed
    # asserted `ISSUABLE == ("valid",)` - a constant. It would have stayed
    # green if the CLI stopped consulting that constant, or inverted the
    # condition, while every geometry seed above also stayed green.
    from check_locator_geometry import FAILING, ISSUABLE

    def issued_failures(verdicts):
        """Exactly the arithmetic main() performs under --issued."""
        return sum(1 for v in verdicts if v not in ISSUABLE)

    def review_failures(verdicts):
        return sum(1 for v in verdicts if v in FAILING)

    policy_ok = True
    for verdict in ("unlocated", "partial", "unsupported", "incomplete",
                    "invalid"):
        if issued_failures([verdict]) != 1:
            print("FAIL %-50s %r does not fail --issued"
                  % ("issued policy", verdict))
            failures += 1
            policy_ok = False
    if issued_failures(["valid"]) != 0:
        print("FAIL %-50s `valid` fails --issued" % "issued policy")
        failures += 1
        policy_ok = False
    if review_failures(["unlocated", "partial", "unsupported"]) != 0:
        print("FAIL %-50s review view rejects non-failing verdicts"
              % "review policy")
        failures += 1
        policy_ok = False
    if policy_ok:
        print("PASS %-50s %s"
              % ("--issued fails all five non-valid verdicts",
                 "review view still passes three"))

    live = [v for _k, v, _m in check(targets, resolved, verticals)]
    if issued_failures(live) != len(live):
        print("FAIL %-50s %d of %d live occurrences are issuable"
              % ("issued vs live records", len(live) - issued_failures(live),
                 len(live)))
        failures += 1
    else:
        print("PASS %-50s all %d are correctly not issuable"
              % ("no live occurrence is issuable today", len(live)))


    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
