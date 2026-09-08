"""Gate on _Precedents/ - the design-precedent corpus.

What it actually protects, in order of how much damage the failure does:

  1. IDENTITY. The image bytes are gitignored, so `sha256` in a manifest is the only thing
     git holds about a file. If a manifest and a file disagree, the citation in a layout case
     points at something we can no longer prove. Checked by rehashing every file.
  2. UNEXAMINED FILES DO NOT SILENTLY BECOME EVIDENCE. A file with `examined: no` may not be
     cited by a layout case. This vault has already filed an unfurnished plan as the handover
     state when it was the after state of a demolition - the fix is to make "nobody has looked
     at this yet" a machine-visible fact.
  3. THE ROSTER MATCHES THE DISK. Every precedent folder has a roster row and vice versa,
     because the roster is what a reader consults and what a future precedent-view tool reads.
  4. Roles come from a controlled vocabulary, so the corpus stays queryable.

Usage:
    python tools/precedents/validate_precedents.py
    python tools/precedents/validate_precedents.py --skip-hashes   # faster, weaker
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRECEDENTS = ROOT / "_Precedents"
ROSTER = PRECEDENTS / "roster.csv"
CASES = ROOT / "data" / "layout_cases"

MANIFEST_FIELDS = ["path", "role", "examined", "what", "bytes", "sha256"]
ROSTER_FIELDS = [
    "precedent_id",
    "class",
    "author",
    "project",
    "same_type_as_ours",
    "files",
    "examined",
    "case_file",
    "status",
    "what_it_settles",
]

# A role is a claim about what a drawing IS. Keep it closed so the corpus stays queryable
# and so a new contributor cannot invent a synonym.
ROLES = {
    "unexamined",
    "layout_plan_furnished",
    "layout_plan_unfurnished",
    "structural_scheme",
    "services_plan",
    "rendering_photoreal",
    "rendering_3d_axonometric",
    "elevation_or_section",
    "cover",
    "moodboard",
    "specification",
    "photo_asbuilt",
    "duplicate",
    "irrelevant",
}

CLASSES = {"design_project", "market_listing"}
SAME_TYPE = {"yes", "no", "unknown"}
STATUSES = {"analysed", "partly_analysed", "ingested_only", "rejected"}

SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-hashes", action="store_true")
    args = parser.parse_args()
    ensure_utf8_stdout()

    problems: list[str] = []
    notes: list[str] = []

    if not PRECEDENTS.is_dir():
        sys.exit("FAIL _Precedents/ does not exist")
    if not ROSTER.exists():
        sys.exit(f"FAIL missing {ROSTER.relative_to(ROOT).as_posix()}")

    # ---- the roster -------------------------------------------------------
    roster = read_csv(ROSTER)
    with ROSTER.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    if header != ROSTER_FIELDS:
        problems.append(f"roster.csv header is {header}, expected {ROSTER_FIELDS}")

    roster_by_id = {}
    for row in roster:
        pid = row["precedent_id"]
        if pid in roster_by_id:
            problems.append(f"roster.csv: duplicate precedent_id {pid!r}")
        roster_by_id[pid] = row
        if row["class"] not in CLASSES:
            problems.append(f"roster {pid}: class {row['class']!r} not in {sorted(CLASSES)}")
        if row["same_type_as_ours"] not in SAME_TYPE:
            problems.append(
                f"roster {pid}: same_type_as_ours {row['same_type_as_ours']!r} not in {sorted(SAME_TYPE)}"
            )
        if row["status"] not in STATUSES:
            problems.append(f"roster {pid}: status {row['status']!r} not in {sorted(STATUSES)}")
        if row["class"] == "design_project" and "__" not in pid:
            problems.append(
                f"roster {pid}: a design_project id must be '<author>__<project>' so different "
                "authors' takes on the same flat sort together"
            )
        cf = row["case_file"].strip()
        if cf:
            if not (ROOT / cf).exists():
                problems.append(f"roster {pid}: case_file {cf} does not exist")
        elif row["status"] in {"analysed", "partly_analysed"}:
            problems.append(
                f"roster {pid}: status is {row['status']} but no case_file - an analysed "
                "precedent must point at the layout case that holds the analysis"
            )

    # ---- folders on disk --------------------------------------------------
    on_disk: dict[str, Path] = {}
    for group, cls in (("design_projects", "design_project"), ("market_listings", "market_listing")):
        base = PRECEDENTS / group
        if not base.is_dir():
            continue
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            on_disk[folder.name] = folder
            row = roster_by_id.get(folder.name)
            if row is None:
                problems.append(
                    f"{group}/{folder.name}: on disk but has NO roster row - it is invisible "
                    "to anyone reading _Precedents/README.md"
                )
            elif row["class"] != cls:
                problems.append(
                    f"roster {folder.name}: class is {row['class']!r} but it sits under {group}/"
                )
            if not (folder / "README.md").exists():
                problems.append(f"{group}/{folder.name}: missing README.md")
            if not (folder / "manifest.csv").exists():
                problems.append(f"{group}/{folder.name}: missing manifest.csv")

    for pid in roster_by_id:
        if pid not in on_disk:
            problems.append(f"roster {pid}: no folder on disk")

    # ---- manifests --------------------------------------------------------
    total_files = 0
    total_examined = 0
    examined_sha: set[str] = set()
    unexamined_sha: dict[str, str] = {}

    for pid, folder in sorted(on_disk.items()):
        manifest = folder / "manifest.csv"
        if not manifest.exists():
            continue
        with manifest.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle), [])
        if header != MANIFEST_FIELDS:
            problems.append(f"{pid}/manifest.csv header is {header}, expected {MANIFEST_FIELDS}")
            continue

        rows = read_csv(manifest)
        seen_sha: set[str] = set()
        n_examined = 0
        for row in rows:
            total_files += 1
            path = ROOT / row["path"]
            if not SHA_RE.match(row["sha256"] or ""):
                problems.append(f"{pid}: {row['path']} has a malformed sha256")
                continue
            if row["sha256"] in seen_sha:
                problems.append(
                    f"{pid}: sha256 {row['sha256'][:8]} appears twice - byte-identical files, "
                    "mark one `duplicate` or remove it"
                )
            seen_sha.add(row["sha256"])

            if row["role"] not in ROLES:
                problems.append(f"{pid}: {row['path']} role {row['role']!r} not in the vocabulary")
            if row["examined"] not in {"yes", "no"}:
                problems.append(f"{pid}: {row['path']} examined must be yes/no")
            if row["examined"] == "yes":
                n_examined += 1
                total_examined += 1
                examined_sha.add(row["sha256"])
                if row["role"] == "unexamined":
                    problems.append(
                        f"{pid}: {row['path']} is examined: yes but still has role `unexamined`"
                    )
            else:
                unexamined_sha[row["sha256"]] = f"{pid}: {row['path']}"
                if row["role"] != "unexamined":
                    problems.append(
                        f"{pid}: {row['path']} has role {row['role']!r} but examined: no - "
                        "a role is a claim, so it needs someone to have looked"
                    )

            if not path.exists():
                notes.append(f"{pid}: {row['path']} is in the manifest but not on this machine")
                continue
            actual_bytes = path.stat().st_size
            if str(actual_bytes) != row["bytes"]:
                problems.append(
                    f"{pid}: {row['path']} is {actual_bytes} bytes, manifest says {row['bytes']}"
                )
            if not args.skip_hashes:
                actual = sha256_of(path)
                if actual != row["sha256"]:
                    problems.append(
                        f"{pid}: {row['path']} SHA MISMATCH - manifest {row['sha256'][:8]}, "
                        f"file {actual[:8]}. Every citation of this file is now unprovable."
                    )

        # files on disk that no manifest row mentions
        listed = {(ROOT / r["path"]).resolve() for r in rows}
        for f in sorted(p for p in folder.rglob("*") if p.is_file()):
            if f.name in {"manifest.csv", "README.md"}:
                continue
            if f.resolve() not in listed:
                problems.append(
                    f"{pid}: {f.relative_to(ROOT).as_posix()} is on disk but not in manifest.csv "
                    "- it is gitignored, so it exists nowhere else"
                )

        row = roster_by_id.get(pid)
        if row is not None:
            if row["files"].strip() and row["files"] != str(len(rows)):
                problems.append(
                    f"roster {pid}: files={row['files']} but manifest has {len(rows)} rows"
                )
            if row["examined"].strip() and row["examined"] != str(n_examined):
                problems.append(
                    f"roster {pid}: examined={row['examined']} but manifest has {n_examined} yes"
                )

    # ---- layout cases may only cite EXAMINED files ------------------------
    for case_path in sorted(CASES.glob("*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        for doc in case.get("provenance", {}).get("companion_documents", []) or []:
            sha = (doc.get("source_sha256") or "").strip()
            src = doc.get("source_file", "")
            if not sha or not src.startswith("_Precedents/"):
                continue
            if sha in unexamined_sha:
                problems.append(
                    f"{case_path.name}: cites {doc.get('id')} ({src}) whose manifest row says "
                    f"examined: no - {unexamined_sha[sha]}"
                )
            elif sha not in examined_sha:
                problems.append(
                    f"{case_path.name}: cites {doc.get('id')} with sha256 {sha[:8]} which no "
                    "_Precedents manifest lists - the citation is unverifiable"
                )

    # ---- report -----------------------------------------------------------
    print(
        f"{len(roster_by_id)} precedent(s), {total_files} file(s), "
        f"{total_examined} examined, {total_files - total_examined} not yet."
    )
    for note in notes:
        print(f"  note: {note}")
    if problems:
        print()
        for p in problems:
            print(f"  FAIL {p}")
        print()
        print(f"FAIL {len(problems)} problem(s).")
        return 1
    print()
    print("PASS - manifests match the files, roles are in the vocabulary, the roster matches")
    print("       the disk, and no layout case cites a file nobody has examined.")
    if total_files - total_examined:
        print()
        print(
            f"       {total_files - total_examined} file(s) still `examined: no`. That is not a "
            "failure -\n       it is the honest state, and it blocks only citation."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
