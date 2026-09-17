#!/usr/bin/env python3
"""Author the exchange IDS, and the expected applicability count for each spec.

⚠️⚠️ IDS IS NOT THE WHOLE MODEL GATE. It states EXCHANGE requirements that it
can express reliably. These stay in Python because IDS either cannot express
them or cannot express them precisely:

  cross-build identity stability      scripts/ifc_identity_selftest.py
  global uniqueness + derived rel ids  same
  exact geometry and canonical parity   tools/ifc/check_model_against_canonical.py
  opening / void / fill SEMANTICS       same - `PartOf` can say "is voided",
                                        not "the void matches this opening"
  coordinate frame and quantities       the compiler self-tests

⚠️⚠️ AND THE FAILURE THIS GUARDS AGAINST IS `0 of 0`.
------------------------------------------------------
An IDS specification whose applicability matches NOTHING reports success. A
suite of them reports total success while checking nothing at all - the same
class as a seeded gate that cannot fail. So every specification here carries a
separately asserted EXPECTED APPLICABILITY COUNT, written beside the IDS and
enforced by `check_ids.py`. If the model stops producing walls, the wall
specification does not quietly start passing.

    .venv-ifc314\\Scripts\\python.exe tools/ifc/author_ids.py
"""
from __future__ import annotations

import argparse
import io
import json
import os

from ifctester import ids
from ifctester.facet import Attribute, Entity, Material, PartOf, Property

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDS_PATH = os.path.join(REPO, "data", "canonical", "ifc_exchange.ids")
EXPECT_PATH = os.path.join(REPO, "data", "canonical", "ifc_exchange_expectations.json")

# spec name -> how many entities it MUST apply to. Authored, not measured:
# these are the counts the model is required to contain.
EXPECTED = {
    "Walls carry a type designation": 25,
    "Walls carry a material association": 25,
    "Doors carry a type designation": 6,
    "Windows carry a type designation": 3,
    "Every wall declares its phase": 25,
    "Every wall is in a spatial container": 25,
    "Walls expose their canonical identity": 25,
    "No unclassified proxies": 2,
}


def build():
    spec_set = ids.Ids(
        title="Apartment exchange requirements",
        description=("What the issued IFC must carry for schedules, phasing "
                     "and durable reference. NOT the whole model gate - "
                     "geometry, identity stability and void semantics are "
                     "checked in Python."),
        author="aliaksei.babko@innowise.com",
        date="2026-09-17",
        purpose="Exchange requirement contract for the generated apartment model",
    )

    def spec(name, applicability, requirements, instructions):
        s = ids.Specification(name=name, ifcVersion=["IFC4"],
                              instructions=instructions)
        for facet in applicability:
            s.applicability.append(facet)
        for facet in requirements:
            s.requirements.append(facet)
        spec_set.specifications.append(s)

    # ── types and materials — what schedules depend on ───────────────────────
    spec("Walls carry a type designation", [Entity(name="IFCWALL")],
         [Attribute(name="ObjectType")],
         "Schedules group by type. An instance does not carry its type's "
         "name, so without a type designation there is nothing to group on.")
    spec("Walls carry a material association", [Entity(name="IFCWALL")],
         [Material()],
         "Layer build-up and material quantities come from the material "
         "association on the type.")
    spec("Doors carry a type designation", [Entity(name="IFCDOOR")],
         [Attribute(name="ObjectType")], "Door schedule grouping.")
    spec("Windows carry a type designation", [Entity(name="IFCWINDOW")],
         [Attribute(name="ObjectType")], "Window schedule grouping.")

    # ── phase — load-bearing now the flat is being rewired ───────────────────
    spec("Every wall declares its phase",
         [Entity(name="IFCWALL")],
         [Property(propertySet="Pset_ApartmentPhase", baseName="Phase",
                   dataType="IfcLabel")],
         "existing / demolished / new. A rewire makes this load-bearing; an "
         "element with no phase cannot be filtered into any issued view.")

    # ── spatial containment — expressible precisely, so it belongs here ──────
    spec("Every wall is in a spatial container", [Entity(name="IFCWALL")],
         [PartOf(name="IFCBUILDINGSTOREY",
                 relation="IFCRELCONTAINEDINSPATIALSTRUCTURE")],
         "An element outside the spatial tree vanishes silently in viewers, "
         "and wrong containment is a common export defect.")

    # ── canonical identity, where it is exposed ──────────────────────────────
    spec("Walls expose their canonical identity", [Entity(name="IFCWALL")],
         [Property(propertySet="Pset_ApartmentIdentity",
                   baseName="CanonicalId", dataType="IfcLabel")],
         "The GlobalId derives from the canonical uuid; exposing the uuid "
         "makes the derivation auditable from the file alone.")

    # ── prohibited: an unclassified proxy is a modelling escape hatch ────────
    spec("No unclassified proxies",
         [Entity(name="IFCBUILDINGELEMENTPROXY")],
         [Attribute(name="ObjectType")],
         "A proxy with no ObjectType says only 'something is here'. The two "
         "vent shafts are proxies today and must declare what they are.")

    return spec_set


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ids", default=IDS_PATH)
    ap.add_argument("--expectations", default=EXPECT_PATH)
    a = ap.parse_args()

    spec_set = build()
    names = [s.name for s in spec_set.specifications]
    missing = [n for n in names if n not in EXPECTED]
    if missing:
        print("FAIL every specification needs an expected applicability "
              "count: %s" % ", ".join(missing))
        return 1

    os.makedirs(os.path.dirname(a.ids), exist_ok=True)
    spec_set.to_xml(a.ids)
    with io.open(a.expectations, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(EXPECTED, ensure_ascii=False, indent=2) + "\n")
    print("wrote %s (%d specifications)"
          % (os.path.relpath(a.ids, REPO), len(names)))
    print("wrote %s" % os.path.relpath(a.expectations, REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
