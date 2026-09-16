#!/usr/bin/env python3
"""Guard `check_model_against_canonical.py` by seeding real defects.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate. The real model must PASS and each seeded defect must be REJECTED.

The seeds are the failures this generator can actually produce - a wall lost in
the DXF read, a thickness that drifts from `wall_blocks.csv`, an opening placed
at the wrong height (the defect that started all this: window panes on the
floor), a ventilation shaft counted as a wall (which would corrupt every finish
take-off), and a fill outside its own opening.

    .venv-ifc314\\Scripts\\python.exe scripts/model_from_dxf_selftest.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "ifc"))

import ifcopenshell  # noqa: E402

from check_model_against_canonical import check  # noqa: E402

REAL = REPO / "data" / "outputs" / "variants" / "v0-existing" / "model.ifc"


def seed_delete_wall(model):
    """A wall the DXF carries and the IFC lost."""
    wall = next(w for w in model.by_type("IfcWall") if w.Name == "R2")
    model.remove(wall)
    return "wall R2 deleted"


def seed_duplicate_wall(model):
    """The same wall emitted twice - a double count in every take-off."""
    wall = next(w for w in model.by_type("IfcWall") if w.Name == "G6")
    copy = model.create_entity("IfcWall", GlobalId=ifcopenshell.guid.new(),
                               Name=wall.Name, ObjectPlacement=wall.ObjectPlacement,
                               Representation=wall.Representation)
    return "wall %s duplicated" % copy.Name


def seed_wrong_thickness(model):
    """A wall drawn thinner than `wall_blocks.csv` records."""
    wall = next(w for w in model.by_type("IfcWall") if w.Name == "R3")
    curve = wall.Representation.Representations[0].Items[0].SweptArea.OuterCurve
    pts = [list(p.Coordinates) for p in curve.Points]
    ys = sorted({p[1] for p in pts})
    if len(ys) < 2:
        raise RuntimeError("R3 is not the rectangle this seed assumes")
    lo, hi = ys[0], ys[-1]
    for p in curve.Points:
        c = list(p.Coordinates)
        if abs(c[1] - hi) < 1e-9:
            c[1] = lo + (hi - lo) * 0.5      # halve the drawn thickness
            p.Coordinates = tuple(c)
    return "wall R3 drawn at half its recorded thickness"


def seed_window_on_the_floor(model):
    """THE original defect: a pane dropped to floor level."""
    win = next(w for w in model.by_type("IfcWindow") if w.Name.startswith("O3"))
    solid = win.Representation.Representations[0].Items[0]
    loc = solid.Position.Location
    c = list(loc.Coordinates)
    c[2] = 0.0
    loc.Coordinates = tuple(c)
    return "window O3 dropped to the floor"


def seed_shaft_as_wall(model):
    """A ventilation shaft counted as wall area."""
    shaft = next(p for p in model.by_type("IfcBuildingElementProxy")
                 if (p.Name or "").startswith("Vent shaft"))
    model.create_entity("IfcWall", GlobalId=ifcopenshell.guid.new(),
                        Name=shaft.Name, ObjectPlacement=shaft.ObjectPlacement,
                        Representation=shaft.Representation)
    return "a ventilation shaft also modelled as a wall"


def seed_shaft_missing(model):
    """One of the two shafts dropped entirely."""
    shaft = next(p for p in model.by_type("IfcBuildingElementProxy")
                 if (p.Name or "").startswith("Vent shaft"))
    name = shaft.Name
    model.remove(shaft)
    return "%s removed" % name


def seed_unsanctioned_extension(model):
    """A wall stretched along its length by an amount no opening accounts for.

    This is the failure mode the wall-extension feature could hide: walls are
    deliberately extended across a doorway, so the length check has to allow ONE
    kind of growth. Anything else must still be caught.
    """
    wall = next(w for w in model.by_type("IfcWall") if w.Name == "G5")
    curve = wall.Representation.Representations[0].Items[0].SweptArea.OuterCurve
    pts = [list(p.Coordinates) for p in curve.Points]
    ys = sorted({p[1] for p in pts})
    hi = ys[-1]
    for p in curve.Points:
        c = list(p.Coordinates)
        if abs(c[1] - hi) < 1e-9:
            c[1] = hi + 0.4          # 400 mm of length nobody sanctioned
            p.Coordinates = tuple(c)
    return "wall G5 lengthened by 400 mm with no opening to account for it"


def _translate_wall(model, wall_id, dx=0.0, dy=0.0):
    wall = next(w for w in model.by_type("IfcWall") if w.Name == wall_id)
    curve = wall.Representation.Representations[0].Items[0].SweptArea.OuterCurve
    for p in curve.Points:
        c = list(p.Coordinates)
        c[0] += dx
        c[1] += dy
        p.Coordinates = tuple(c)


def seed_wall_shifted_sideways(model):
    """A rigid sideways shift - every dimension unchanged.

    ⚠️ This seed exists because the gate demonstrably did NOT catch it. Before
    the placement check, translating G5 500 mm in x passed with 0 problems:
    identity, length, thickness, opening verticals and shaft count are all
    invariant under a rigid shift, so a wall in the wrong place looked exactly
    like a wall in the right one.
    """
    _translate_wall(model, "G5", dx=0.5)
    return "wall G5 translated 500 mm sideways, dimensions unchanged"


def seed_wall_slid_along_axis(model):
    """A slide ALONG the wall's own axis - the harder half of the same defect.

    The long axis legitimately grows outward where a wall is extended across a
    doorway, so the check has to allow that and still refuse a slide. G7 runs
    north-south and carries no opening, so any movement of its ends is wrong.
    """
    _translate_wall(model, "G7", dy=0.3)
    return "wall G7 slid 300 mm along its own axis"


SEEDS = [
    ("wall shifted sideways", seed_wall_shifted_sideways),
    ("wall slid along its axis", seed_wall_slid_along_axis),
    ("wall lengthened without sanction", seed_unsanctioned_extension),
    ("wall deleted", seed_delete_wall),
    ("wall duplicated", seed_duplicate_wall),
    ("wall thickness halved", seed_wrong_thickness),
    ("window dropped to the floor", seed_window_on_the_floor),
    ("ventilation shaft counted as a wall", seed_shaft_as_wall),
    ("ventilation shaft missing", seed_shaft_missing),
]


def main() -> int:
    if not REAL.exists():
        print("FAIL: %s does not exist - build it first" % REAL)
        return 1

    failures = 0

    real_problems = check(REAL)
    if real_problems:
        print("FAIL the real model must pass, but reports:")
        for p in real_problems:
            print("    " + p)
        failures += 1
    else:
        print("PASS the real model passes (0 problems)")

    tmp = Path(tempfile.mkdtemp(prefix="model_selftest_"))
    try:
        for label, seed in SEEDS:
            path = tmp / ("seed_%s.ifc" % label.replace(" ", "_"))
            shutil.copy(REAL, path)
            model = ifcopenshell.open(str(path))
            detail = seed(model)
            model.write(str(path))

            problems = check(path)
            if problems:
                print("PASS %-38s rejected (%d problem(s)) - %s"
                      % (label, len(problems), problems[0][:70]))
            else:
                print("FAIL %-38s NOT rejected - %s" % (label, detail))
                failures += 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print("failures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
