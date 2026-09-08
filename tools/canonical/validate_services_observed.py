"""Gate on data/canonical/services_observed.csv - observed existing services, wall by wall.

The point of this file is to let the owner dictate what he sees in a photo ("two sockets at
the bottom of G3, a smoke detector on the ceiling") and have it become model data without
the mis-assignment that has repeatedly poisoned this model. Per Photo_Evidence_Request.md,
FOUR figures were retracted in two days and every one was "a real number attached to the
wrong element".

So the rules below are not schema hygiene. Each one blocks a failure that has already
happened in this repo:

  1. A wall you cannot name does not exist. room+wall_code must already appear together in
     device_counts_per_wall.csv - you cannot invent a wall by typing it.
  2. A NUMBER NEEDS A SCALE. height_mm or along_wall_mm without a scale_ref is refused. A
     photo carries no scale unless something of known length is in the same plane, and
     electrical_existing.csv already records heights it could not measure for exactly this
     reason.
  3. AN OFFSET NEEDS A DATUM. along_wall_mm without along_wall_ref is meaningless - "600 mm
     along the wall" from which end?
  4. A MIRRORED FLAT MUST BE FLIPPED. Three of the four surveyed flats are mirrored relative
     to ours, and reading a mirrored photo as this layout is the single documented dominant
     error. handedness=mirrored demands mirror_applied=yes.
  5. ANOTHER FLAT BOUNDS, IT DOES NOT REFINE. Per Geometry_Variance_Study.md the deltas run
     -45 to +30 mm, so a dimension taken from another flat's photo may not be recorded as
     high confidence. Existence and building standards may.

Usage:
    python tools/canonical/validate_services_observed.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANON = ROOT / "data" / "canonical"
OBS = CANON / "services_observed.csv"
COUNTS = CANON / "device_counts_per_wall.csv"
PHOTOS = CANON / "photo_positions.csv"

FIELDS = [
    "obs_id", "room", "wall_code", "kind", "count", "grouping", "height_band",
    "height_mm", "along_wall_mm", "along_wall_ref", "scale_ref", "evidence_photo",
    "source_flat", "handedness", "mirror_applied", "determined_by", "confidence", "notes",
]

KINDS = {
    # electrical
    "socket_220", "socket_380", "switch", "dimmer", "ceiling_light_point", "wall_light_point",
    "smoke_detector", "tv_antenna", "ethernet", "fibre_termination", "intercom",
    "consumer_unit", "thermostat", "doorbell", "floor_socket",
    # plumbing and heating
    "water_stub_cold", "water_stub_hot", "sewer_stub", "radiator", "heating_pipe_pair",
    "heat_meter", "towel_rail_tail", "water_meter", "shutoff_valve", "filter_unit",
    # ventilation
    "extract_grille", "extract_duct_spigot", "vent_opening",
}
GROUPINGS = {"single", "double", "triple", "row", "block", "n/a"}
HEIGHT_BANDS = {
    "floor", "low", "mid", "worktop", "switch", "high", "ceiling", "unknown",
}
FLATS = {"ours", "109", "2", "53", "n/a"}
HANDEDNESS = {"mirrored", "same", "n/a"}
YESNO_NA = {"yes", "no", "n/a"}
DETERMINED = {"owner", "photo_reading", "both"}
CONFIDENCE = {"high", "medium", "low"}

OBS_RE = re.compile(r"^OBS-\d{3,}$")
POSITIONAL = ("height_mm", "along_wall_mm")


def ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def read(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"FAIL missing {path.relative_to(ROOT).as_posix()}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def main() -> int:
    ensure_utf8_stdout()
    problems: list[str] = []

    with OBS.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle), [])
    if header != FIELDS:
        sys.exit(f"FAIL header is\n  {header}\nexpected\n  {FIELDS}")

    rows = read(OBS)
    known_walls = {(r["room"], r["wall_segment"]) for r in read(COUNTS)}
    known_rooms = {r for r, _ in known_walls}
    known_photos = {r["photo_id"] for r in read(PHOTOS)}

    seen_ids: set[str] = set()
    for n, row in enumerate(rows, start=2):
        where = f"row {n} ({row.get('obs_id') or 'no id'})"

        oid = row["obs_id"]
        if not OBS_RE.match(oid or ""):
            problems.append(f"{where}: obs_id must look like OBS-001")
        if oid in seen_ids:
            problems.append(f"{where}: duplicate obs_id {oid!r}")
        seen_ids.add(oid)

        # 1. a wall you cannot name does not exist
        pair = (row["room"], row["wall_code"])
        if pair not in known_walls:
            if row["room"] not in known_rooms:
                problems.append(
                    f"{where}: room {row['room']!r} is not in device_counts_per_wall.csv - "
                    "copy the room string from there exactly"
                )
            else:
                walls = sorted(w for r, w in known_walls if r == row["room"])
                problems.append(
                    f"{where}: {row['room']!r} has no wall {row['wall_code']!r}. "
                    f"Known walls for that room: {', '.join(walls)}"
                )

        for field, vocab in (
            ("kind", KINDS), ("grouping", GROUPINGS), ("height_band", HEIGHT_BANDS),
            ("source_flat", FLATS), ("handedness", HANDEDNESS),
            ("mirror_applied", YESNO_NA), ("determined_by", DETERMINED),
            ("confidence", CONFIDENCE),
        ):
            if row[field] not in vocab:
                problems.append(
                    f"{where}: {field}={row[field]!r} not in {sorted(vocab)}"
                )

        if not is_int(row["count"]) or int(row["count"]) < 1:
            problems.append(f"{where}: count must be a positive integer")

        # 2. a number needs a scale
        for field in POSITIONAL:
            if row[field].strip():
                if not is_int(row[field]):
                    problems.append(f"{where}: {field} must be an integer in mm or empty")
                if not row["scale_ref"].strip():
                    problems.append(
                        f"{where}: {field} is given but scale_ref is empty. A photo carries NO "
                        "scale unless something of known length is in the same plane - name it "
                        "(e.g. 'O2 opening 1800 wide') or leave the number out and use "
                        "height_band instead."
                    )

        # 3. an offset needs a datum
        if row["along_wall_mm"].strip() and not row["along_wall_ref"].strip():
            problems.append(
                f"{where}: along_wall_mm without along_wall_ref - measured from WHICH end?"
            )

        # 4. a mirrored flat must be flipped
        if row["handedness"] == "mirrored" and row["mirror_applied"] != "yes":
            problems.append(
                f"{where}: handedness=mirrored but mirror_applied={row['mirror_applied']!r}. "
                "Reading a mirrored flat's photo as this layout is the documented dominant "
                "error in this model - flip the wall assignment, then say so."
            )
        if row["source_flat"] == "ours" and row["handedness"] != "same":
            problems.append(f"{where}: source_flat=ours must have handedness=same")

        # 5. another flat bounds, it does not refine
        if row["source_flat"] not in {"ours", "n/a"}:
            if any(row[f].strip() for f in POSITIONAL) and row["confidence"] == "high":
                problems.append(
                    f"{where}: a dimension from flat {row['source_flat']} may not be high "
                    "confidence. Geometry_Variance_Study.md measures -45 to +30 mm between "
                    "flats of this layout, so another flat BOUNDS this one's number rather "
                    "than refining it. Use medium at most."
                )

        # evidence must be traceable
        ev = row["evidence_photo"].strip()
        if not ev:
            problems.append(f"{where}: evidence_photo is empty - name a photo_id or 'owner_statement'")
        elif ev != "owner_statement" and ev not in known_photos:
            problems.append(
                f"{where}: evidence_photo {ev!r} is not a photo_id in photo_positions.csv "
                "(or the literal 'owner_statement')"
            )
        if ev == "owner_statement" and row["determined_by"] == "photo_reading":
            problems.append(f"{where}: determined_by=photo_reading but evidence is owner_statement")

        if row["height_band"] == "unknown" and row["height_mm"].strip():
            problems.append(f"{where}: height_band=unknown but height_mm is given")

    print(f"{len(rows)} observation(s) in {OBS.relative_to(ROOT).as_posix()}")
    if problems:
        print()
        for p in problems:
            print(f"  FAIL {p}")
        print()
        print(f"FAIL {len(problems)} problem(s).")
        return 1
    print()
    if not rows:
        print("PASS - empty, which is the correct starting state. See")
        print("       00_Master/Existing_Services_Capture_Protocol.md for what to dictate.")
    else:
        print("PASS - every wall is one that exists, every number has a scale behind it,")
        print("       every offset has a datum, mirrored flats are flipped, and no")
        print("       other-flat dimension claims high confidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
