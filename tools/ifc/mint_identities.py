#!/usr/bin/env python3
"""Mint canonical identities ONCE, and commit them as authored data.

⚠️⚠️ THIS IS NOT A DERIVATION. It mints a fresh random UUID per persistent
element and writes it to `data/canonical/ifc_identity.csv`, which is then
AUTHORED DATA and never regenerated. Deriving identity from `G3`, `O3`,
coordinates or geometry would mean a rename or a nudge silently created a new
thing - the services data model already fixed that rule and this follows it.

Run it once to seed the registry, and again only to ADD rows for genuinely new
elements. ⚠️ It never rewrites an existing uuid, and it never reuses a retired
one: an element that goes away is marked `retired` and its uuid stays put so
nothing else can be handed it.

    .venv-ifc314\\Scripts\\python.exe tools/ifc/mint_identities.py --model out.ifc
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import sys
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from identity import REGISTRY, load_registry  # noqa: E402

FIELDS = ["canonical_uuid", "key", "ifc_class", "state", "aliases", "notes"]

# ⚠️ Property sets and relationships are NOT minted. Their identity is DERIVED
# - a pset from its owner plus its name, a relationship from its kind plus its
# endpoints - so a registry row for them would be a second source of truth.
DERIVED = ("IfcPropertySet", "IfcRelationship")


def product_key(entity):
    """`IfcClass:Name`. Unique in this model, and verified so before use."""
    return "%s:%s" % (entity.is_a(), entity.Name or "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--registry", default=REGISTRY)
    a = ap.parse_args()

    import ifcopenshell
    model = ifcopenshell.open(a.model)

    wanted = []
    for entity in model.by_type("IfcRoot"):
        if any(entity.is_a(kind) for kind in DERIVED):
            continue
        wanted.append(entity)

    keys = [product_key(e) for e in wanted]
    duplicates = set(k for k in keys if keys.count(k) > 1)
    if duplicates:
        print("REFUSING: %d key(s) are not unique, so identity cannot be "
              "attached to them: %s" % (len(duplicates),
                                        ", ".join(sorted(duplicates)[:5])))
        return 1

    existing = {}
    order = []
    if os.path.exists(a.registry):
        with io.open(a.registry, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                existing[row["key"]] = row
                order.append(row["key"])
        load_registry(a.registry)          # refuses duplicates before we add

    minted = 0
    for entity in wanted:
        key = product_key(entity)
        if key in existing:
            continue
        existing[key] = {
            "canonical_uuid": str(uuid.uuid4()), "key": key,
            "ifc_class": entity.is_a(), "state": "active", "aliases": "",
            "notes": "minted 2026-09-17 from the first stable-identity build",
        }
        order.append(key)
        minted += 1

    # ⚠️ Anything in the registry that the model no longer produces is RETIRED,
    # not deleted. The uuid must never be handed to a different element.
    present = set(keys)
    retired = 0
    for key, row in existing.items():
        if key not in present and row.get("state") == "active":
            row["state"] = "retired"
            row["notes"] = ("retired 2026-09-17: no longer produced. The uuid "
                            "stays so it is never reused. " + row.get("notes", ""))
            retired += 1

    with io.open(a.registry, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for key in order:
            writer.writerow(dict((f, existing[key].get(f, "")) for f in FIELDS))

    print("registry %s" % os.path.relpath(a.registry, REPO))
    print("   %-22s %d" % ("rows total", len(existing)))
    print("   %-22s %d" % ("minted now", minted))
    print("   %-22s %d" % ("retired now", retired))
    print("   %-22s %d" % ("derived, not minted",
                           len(model.by_type("IfcRoot")) - len(wanted)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
