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

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "services"))

from check_locator_geometry import check, geometry          # noqa: E402
from check_target_schema import load as load_targets        # noqa: E402

# O3 is a window in MC. Along MC's `cross_lo` (which runs x 9380.9 -> 12946.0)
# its void spans 855.0 - 2655.0, and its verticals are sill 266, head 2251.
O3_LO, O3_HI = 855.0, 2655.0


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
        """A wall_face occurrence on MC, the wall that hosts O3."""
        row = {"migration_key": "SEED", "target_concept": "occurrence",
               "service_kind": "socket", "phase": "existing",
               "locator_kind": "wall_face", "host_ref": "MC",
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
    if live.get("OCC-W6", ("", ""))[0] == "partial":
        print("PASS %-50s %-11s %s" % ("the real slice loads and W6 is partial",
                                       "PARTIAL", "via check_target_schema.load()"))
    else:
        print("FAIL the real slice: W6 is %r" % (live.get("OCC-W6"),))
        failures += 1

    # ── 1 ─ centre INSIDE O3 ─────────────────────────────────────────────────
    centre = (O3_LO + O3_HI) / 2.0
    rows = [socket(along_face_mm=str(centre), vertical_mm="1000"),
            avoid("SEED"), says("SEED", "vertical", "1000")]
    expect("a terminal centred inside O3", rows, "SEED", "invalid",
           "INSIDE the void of O3")

    # ── 2 ─ centre CLEAR but the asserted extent crosses O3 ──────────────────
    # 80 mm clear of the jamb, with a 300 mm device: the centre is fine and the
    # envelope is not. This is the seed the whole three-state verdict exists
    # for, and a centre-only validator passes it.
    rows = [socket(along_face_mm=str(O3_LO - 80.0), vertical_mm="1000"),
            avoid("SEED"),
            says("SEED", "vertical", "1000"),
            says("SEED", "extent_along_mm", "300"),
            says("SEED", "extent_vertical_mm", "80")]
    expect("centre clear but EXTENT crosses O3", rows, "SEED", "invalid",
           "CROSSES the void of O3")

    # ── 3 ─ the same position with the extent UNKNOWN ────────────────────────
    rows = [socket(along_face_mm=str(O3_LO - 80.0), vertical_mm="1000"),
            avoid("SEED"), says("SEED", "vertical", "1000"),
            says("SEED", "extent_along_mm", "", "unknown"),
            says("SEED", "extent_vertical_mm", "", "unknown")]
    expect("centre clear, extent unknown -> INCOMPLETE", rows, "SEED",
           "incomplete", "NOT proven valid")

    # ── 4 ─ a valid terminal immediately outside the void ────────────────────
    rows = [socket(along_face_mm=str(O3_LO - 400.0), vertical_mm="1000"),
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
    w6 = [r for r in targets if r.get("migration_key") == "OCC-W6"]
    expect("O10 host_wall=None, R5 adjacent -> W6 stays partial",
           w6 + [r for r in targets
                 if r.get("subject_key") == "OCC-W6"],
           "OCC-W6", "partial", "not a defect")

    # ...and the anchor is genuinely checked: an anchor that touches nothing
    # must still be rejected, or seed 7 would be passing vacuously.
    rows = [socket(along_face_mm="500", anchor_ref="O3", host_ref="R5"),
            avoid("SEED")]
    expect("an anchor that does not touch the host", rows, "SEED", "invalid",
           "does not touch")

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

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
