"""Ingest one design precedent - an author's project, or a market listing - into _Precedents/.

Why this exists: the owner has two or three more design projects for this same apartment
type, by different authors, and wants them organised per author and per project so they can
be compared and cited. Doing that by hand invites drift in the one thing that matters most
here - the sha256 identity, since the image bytes themselves stay out of git.

Layout it creates:

    _Precedents/design_projects/<author>__<project>/
        README.md        written by hand afterwards, from the template printed at the end
        manifest.csv     path, role, examined, what, bytes, sha256
        plans/           layout plans, structural schemes
        renderings/      photoreal or 3D images
        documents/       PDFs, specifications, anything not an image

    _Precedents/market_listings/<slug>/            same shape, images/ instead

Every file lands with role `unexamined`. That is deliberate: a role is a CLAIM about what a
drawing is, and this vault has already been burnt by one - an unfurnished plan filed as the
handover state turned out to be the after state of a demolition. Roles get set once someone
has actually looked at the file, by editing manifest.csv.

Usage:
    python tools/precedents/ingest_precedent.py --author nsdsgn --project euro3-2026 \
        --src "C:/Users/User/Downloads/some folder"
    python tools/precedents/ingest_precedent.py --listing minina-3-realt --src "..."
    python tools/precedents/ingest_precedent.py ... --dry-run
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRECEDENTS = ROOT / "_Precedents"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
DOC_SUFFIXES = {".pdf", ".docx", ".doc", ".xlsx", ".txt", ".md", ".dwg", ".dxf"}

FIELDNAMES = ["path", "role", "examined", "what", "bytes", "sha256"]


def ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def check_slug(value: str, label: str) -> str:
    if not SLUG_RE.match(value):
        sys.exit(
            f"FAIL {label} must be a lowercase-hyphen slug, got {value!r}.\n"
            "     Author slugs name the person or studio: 'nsdsgn', 'zemskov', "
            "'unattributed-instagram'.\n"
            "     Project slugs name the job, not the file source: 'euro3-four-variants'."
        )
    return value


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def subfolder_for(path: Path, is_listing: bool) -> str:
    """Where a file lands. Deliberately coarse - plans vs renderings is a judgement a
    human makes when they set the role, so everything image-shaped starts in one place."""
    suffix = path.suffix.lower()
    if suffix in DOC_SUFFIXES:
        return "documents"
    if suffix in IMAGE_SUFFIXES:
        return "images" if is_listing else "plans"
    return "documents"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", help="author/studio slug, for a design project")
    parser.add_argument("--project", help="project slug, for a design project")
    parser.add_argument("--listing", help="slug, for a market listing instead of a design project")
    parser.add_argument("--src", required=True, type=Path, help="folder of files to ingest")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_utf8_stdout()

    is_listing = bool(args.listing)
    if is_listing:
        if args.author or args.project:
            parser.error("--listing is an alternative to --author/--project, not an addition")
        slug = check_slug(args.listing, "--listing")
        dest = PRECEDENTS / "market_listings" / slug
    else:
        if not (args.author and args.project):
            parser.error("give --author and --project, or --listing")
        author = check_slug(args.author, "--author")
        project = check_slug(args.project, "--project")
        slug = f"{author}__{project}"
        dest = PRECEDENTS / "design_projects" / slug

    if not args.src.is_dir():
        sys.exit(f"FAIL --src is not a directory: {args.src}")

    files = sorted(p for p in args.src.rglob("*") if p.is_file())
    if not files:
        sys.exit(f"FAIL no files found under {args.src}")

    manifest_path = dest / "manifest.csv"
    existing: dict[str, dict] = {}
    if manifest_path.exists():
        with manifest_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                existing[row["sha256"]] = row

    rows: list[dict] = list(existing.values())
    added = skipped_dupe = 0

    for src in files:
        digest = sha256_of(src)
        if digest in existing:
            skipped_dupe += 1
            continue
        folder = subfolder_for(src, is_listing)
        target = dest / folder / src.name
        rel = target.relative_to(ROOT).as_posix()
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
        rows.append(
            {
                "path": rel,
                "role": "unexamined",
                "examined": "no",
                "what": "NOT YET EXAMINED - set role and what after looking at the file",
                "bytes": src.stat().st_size,
                "sha256": digest,
            }
        )
        existing[digest] = rows[-1]
        added += 1

    rows.sort(key=lambda r: r["path"])

    if args.dry_run:
        print(f"DRY RUN - would ingest {added} file(s) into {dest.relative_to(ROOT).as_posix()}")
        if skipped_dupe:
            print(f"          {skipped_dupe} skipped as byte-identical to something already there")
        for row in rows[:10]:
            print(f"  {row['sha256'][:8]}  {row['path']}")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"ingested {added} file(s) into {dest.relative_to(ROOT).as_posix()}")
    if skipped_dupe:
        print(f"  {skipped_dupe} skipped as byte-identical to a file already in the manifest")
    print(f"  manifest: {manifest_path.relative_to(ROOT).as_posix()} ({len(rows)} rows)")
    print()
    print("NEXT, and none of it is optional:")
    print(f"  1. Look at every file and set `role`, `examined` and `what` in manifest.csv.")
    print(f"     Roles: see tools/precedents/validate_precedents.py for the vocabulary.")
    print(f"  2. Write {(dest / 'README.md').relative_to(ROOT).as_posix()} - what this is,")
    print(f"     who made it, what it settles, and what may NOT be read off it.")
    print(f"  3. Add a row to _Precedents/roster.csv.")
    print(f"  4. If it is a design project worth analysing, create")
    print(f"     data/layout_cases/<case_id>.json and name it in the roster.")
    print(f"  5. Run: python tools/precedents/validate_precedents.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
