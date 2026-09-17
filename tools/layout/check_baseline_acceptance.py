#!/usr/bin/env python3
"""Is the v0 baseline DECISION-BEARING? Recompute the hashes and say so.

⚠️⚠️ THE DEFECT THIS CLOSES IS THAT THE LAPSE WAS PROSE
-------------------------------------------------------
`v0_baseline_acceptance.json` said an acceptance "lapses" if any artefact
changes, and nothing anywhere read the file. An artefact could be regenerated
while the record still said `accepted`, and `compare_variants.py` would go on
producing a sheet that looked decision-bearing. A rule nobody enforces is a
comment.

So the acceptance is now a COMPUTED state, not a stored one:

    status accepted            AND
    all five scopes accepted   AND
    every artefact's CURRENT sha256 equals the accepted one

…or the baseline is provisional and anything read off it must SAY SO. There is
no third answer, and `decision_bearing()` is the only thing entitled to give
it.

⚠️ A FAILING CHECK IS NOT AN ERROR. Today the baseline is correctly pending -
the owner has not reviewed it. This exits non-zero under `--require` only,
which is for a consumer that must not proceed; the plain run reports.

    .venv-ifc314\\Scripts\\python.exe tools/layout/check_baseline_acceptance.py
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECORD = os.path.join(REPO, "data", "canonical", "v0_baseline_acceptance.json")

# ⚠⚠ V1's FOOTPRINT IS ITS OWN SCOPE, and it is the reason the shaft scope
# was split. Accepting "shafts" as one thing would have let a baseline become
# decision-bearing while V1's size is explicitly unestablished - the vault says
# it NEEDS A CAREFUL RE-MEASUREMENT - and any comparison turning on V1's
# clearance would then have read as settled.
SCOPES = ("wall_and_opening_arrangement",
          "ventilation_shaft_positions",
          "ventilation_shaft_v2_footprint",
          "ventilation_shaft_v1_footprint",
          "loggia_outline_and_glazing", "m2_and_m6b_geometry",
          "open_extent_exceptions")

# ⚠⚠ THE EXACT SET, NOT MERELY A NON-EMPTY ONE. Removing
# `v0_named_walls_placed.json` from an otherwise accepted record returned
# `(True, [])`: the loop only checked the artefacts that were STILL listed, so
# dropping one silently removed it from the scope of the approval. A pin you
# can shrink is not a pin.
# ⚠ THE REVIEW SHEET IS PINNED TOO. It defines what each accepted scope
# MEANS - above all the V1 exclusion - so its wording could otherwise change
# without the acceptance lapsing.
REQUIRED_ARTEFACTS = (
    "_Drawings/review/v0_dxf_readback.png",
    "data/cad/dxf/v0_developer_layout.dxf",
    "data/canonical/v0_named_walls_placed.json",
    "00_Master/V0_Baseline_Review_Sheet.md",
)

# The variant specs a comparison would read. A RETIRED spec means owner
# acceptance of the DXF unblocks nothing, because the comparison does not
# consume the thing that was accepted.
VARIANT_SPECS = ("data/outputs/variants/v0-existing/spec.json",)

BANNER = ("PROVISIONAL - v0 baseline NOT accepted by the owner. "
          "Not decision-bearing.")


# ⚠⚠ TEXT FILES ARE HASHED WITH NEWLINES NORMALISED. git on Windows rewrites
# LF to CRLF on checkout, so a raw byte hash of a committed .md or .json
# changes without anybody editing it - the pin would lapse on a fresh clone and
# the owner's acceptance would evaporate for a reason that has nothing to do
# with the drawing. Binary artefacts are hashed raw, where the bytes ARE the
# content.
TEXT_SUFFIXES = (".md", ".json", ".csv", ".dxf", ".svg", ".txt")


def sha256(path):
    with io.open(path, "rb") as fh:
        blob = fh.read()
    if path.lower().endswith(TEXT_SUFFIXES):
        blob = blob.replace(bytes([13, 10]), bytes([10]))
    return hashlib.sha256(blob).hexdigest()


def load(path=RECORD):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def decision_bearing(record=None, variant_specs=None):
    """(bool, reasons). The ONLY entitled answer to 'may this drive a choice'."""
    record = load() if record is None else record
    reasons = []

    status = (record.get("status") or "").strip()
    if status != "accepted":
        reasons.append("status is %r, not `accepted`" % status)

    scopes = record.get("scopes") or {}
    missing = [s for s in SCOPES if s not in scopes]
    if missing:
        reasons.append("the record has no scope(s) %s - a scope that is absent "
                       "has not been accepted, it has been forgotten"
                       % ", ".join(missing))
    for name in SCOPES:
        state = ((scopes.get(name) or {}).get("state") or "").strip()
        if state != "accepted":
            reasons.append("scope %s is %r" % (name, state or "absent"))

    # ⚠️⚠️ THE HASHES ARE RECOMPUTED, NOT TRUSTED. This is the whole point: an
    # artefact regenerated after acceptance must invalidate it, and the only
    # way to know is to read the bytes again.
    artefacts = record.get("artefacts") or {}
    missing_pins = [a for a in REQUIRED_ARTEFACTS if a not in artefacts]
    extra_pins = [a for a in artefacts if a not in REQUIRED_ARTEFACTS]
    if missing_pins:
        reasons.append(
            "the record does not pin %s. The required set is EXACT - a pin "
            "that can be shrunk silently removes an artefact from the scope of "
            "the approval" % ", ".join(sorted(missing_pins)))
    if extra_pins:
        reasons.append("the record pins %s, which is not in the required set"
                       % ", ".join(sorted(extra_pins)))
    for relative, accepted_hash in sorted(artefacts.items()):
        path = os.path.join(REPO, relative)
        if not os.path.exists(path):
            reasons.append("%s is pinned but does not exist" % relative)
            continue
        current = sha256(path)
        if current != accepted_hash:
            reasons.append(
                "%s has CHANGED since acceptance (%s -> %s) - the approval was "
                "given against different bytes and does not transfer"
                % (relative, str(accepted_hash)[:12], current[:12]))

    # ⚠️ Acceptance never means as-built, and a record that claims otherwise is
    # refused rather than quietly honoured.
    if record.get("field_verified"):
        reasons.append("the record claims field_verified - owner acceptance of "
                       "a PLANNED reading cannot confer that")
    if (record.get("provenance") or "") != "planned":
        reasons.append("provenance is %r, expected `planned`"
                       % record.get("provenance"))

    # ⚠⚠ ACCEPTANCE MUST UNBLOCK THE THING IT CLAIMS TO. The comparison reads
    # the VARIANT SPEC, not the DXF, and v0-existing/spec.json is an early
    # schematic that carries its own `_retired` warning - 18 walls against 25,
    # no ventilation shafts, a rectangular loggia. Accepting the new geometry
    # would have unblocked a sheet built from the retired one. That is the
    # retired-schematic failure the vault already has a name for.
    for relative in (VARIANT_SPECS if variant_specs is None
                     else variant_specs):
        path = os.path.join(REPO, relative)
        if not os.path.exists(path):
            reasons.append("%s does not exist, so the comparison has no "
                           "baseline to read" % relative)
            continue
        with io.open(path, encoding="utf-8") as fh:
            spec = json.load(fh)
        if "_retired" in spec:
            reasons.append(
                "%s is RETIRED (%s). The comparison consumes THIS, not the "
                "accepted DXF, so acceptance would unblock a sheet built from "
                "a superseded schematic"
                % (relative, str(spec["_retired"])[:70]))
    return (not reasons), reasons


def blocked_topics(record=None):
    """Topics that stay blocked even when the baseline is accepted.

    ⚠ A scope may be accepted while a measurement inside it is still open -
    V1's footprint is exactly that. Accepting the shaft POSITIONS does not
    establish V1's SIZE, so any comparison turning on V1's clearance must
    refuse regardless of the overall acceptance state.
    """
    record = load() if record is None else record
    out = []
    for item in (record.get("open_measurements") or []):
        if (item.get("state") or "") != "resolved":
            out.append("%s - %s" % (item.get("topic"), item.get("blocks")))
    return out


def banner(record=None, variant_specs=None):
    """The line a consumer must print when the baseline is not accepted."""
    ok, _reasons = decision_bearing(record, variant_specs)
    return None if ok else BANNER


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--require", action="store_true",
                    help="exit non-zero unless the baseline is decision-bearing")
    a = ap.parse_args()

    ok, reasons = decision_bearing()
    for reason in reasons:
        print("  %s" % reason)
    if ok:
        print("DECISION-BEARING - the owner has accepted every scope and no "
              "pinned artefact has changed since")
        return 0
    print("PROVISIONAL - the v0 baseline is not decision-bearing (%d reason(s))"
          % len(reasons))
    print("  -> anything read off it must carry: %s" % BANNER)
    return 1 if a.require else 0


if __name__ == "__main__":
    raise SystemExit(main())
