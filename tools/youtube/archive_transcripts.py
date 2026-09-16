#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move fetched transcripts from an inbox folder to _Archive/processed_sources
and repoint each matching source note's `transcript_file:` frontmatter field -
by parsing metadata, never by filename globbing.

Why this exists (see conversation history 2026-08-04): this two-step move-then-
repoint was previously done with hand-rolled bash loops per playlist batch,
matching source notes to transcripts by globbing `YT_<video_id>_*.md`. That
broke once on a video ID starting with `_` (`_wWteDpfIso`), because the glob
`YT__wWteDpfIso_*` didn't match the note an extraction agent had actually
written as `YT_wWteDpfIso_*.md` (leading underscore dropped). This script
instead reads each transcript's own `.meta.json` sidecar for its authoritative
`video_id`, and reads each source note's own frontmatter `video_id:` field to
find the matching note - filenames are never parsed for identity, only used
for the human-readable slug portion of the archived filename.

Usage:
    python tools/youtube/archive_transcripts.py <inbox_dir> [--dry-run]

Expects each transcript in <inbox_dir> to have a same-stem `.meta.json`
sidecar (as written by youtube-transcript-fetch's fetch_youtube_transcript.py)
containing at least `video_id` and `sha256`. For each one:
  1. Find the source note under _Knowledge/
     sources/ whose frontmatter `video_id:` matches.
  2. Derive the archive slug from that note's own filename (the part after
     `YT_<video_id>_` and before `.md`) - keeps the archived transcript's
     name consistent with its note, which prior manual runs did by hand.
  3. Move the .txt and .meta.json to _Archive/processed_sources/ as
     `<date>_<slug>_<hash8>.txt` / `.meta.json` (date taken from the inbox
     filename's own date prefix if present, else today).
  4. Rewrite the note's `transcript_file:` line to the new archive path.

A transcript with no matching source note is left in place and reported,
not silently skipped or guessed at.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preflight_playlist import load_known_ids_from_notes  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_DIR = REPO_ROOT / "_Archive" / "processed_sources"
SOURCE_NOTES_DIR = REPO_ROOT / "_Sources"

INBOX_DATE_PREFIX_RE = re.compile(r"^(\d{8})_")
NOTE_FILENAME_RE = re.compile(r"^YT_(.+?)_([^_]+(?:_[^_]+)*)\.md$")


def derive_slug_from_note(note_path: Path, video_id: str) -> str | None:
    """Extract the slug portion of a source note's filename, i.e. everything
    after `YT_<video_id>_` and before `.md`. Returns None if the note's
    filename doesn't actually start with that video_id prefix (a real
    inconsistency worth surfacing, not papering over)."""
    stem = note_path.stem  # YT_<id>_<slug>
    prefix = f"YT_{video_id}_"
    if stem.startswith(prefix):
        return stem[len(prefix):]
    # Fall back: some notes were written with the video ID's leading
    # underscore stripped by the extraction agent (the exact bug this
    # script exists to route around) - retry without a leading underscore.
    if video_id.startswith("_") and stem.startswith(f"YT_{video_id[1:]}_"):
        return stem[len(f"YT_{video_id[1:]}_"):]
    return None


def extract_covers_also_ids(line: str) -> list[str]:
    """Extract 11-char YouTube video IDs from a covers_also: line, splitting
    on commas only. Preserves the exact declared order."""
    chunks = line.split(",")
    ids: list[str] = []
    for chunk in chunks:
        m = re.search(r"(?:^|[^A-Za-z0-9_-])([A-Za-z0-9_-]{11})(?:$|[^A-Za-z0-9_-])", chunk.strip())
        if m:
            ids.append(m.group(1))
    return ids


def note_pt_points_to_existing_file(note_text: str, part_key: str, archive_dir: Path) -> bool:
    """Check if note_text's part_key line (e.g. transcript_file_pt2:) already
    points at an existing file on disk. Idempotency test valid for both legacy
    hand-named files and new _ptN_ files."""
    m = re.search(rf"^{part_key}:\s*(\S+)", note_text, re.MULTILINE)
    if not m:
        return False
    val = m.group(1).strip()
    target_disk = archive_dir / Path(val).name
    if target_disk.is_file():
        return True
    if archive_dir == ARCHIVE_DIR:
        return (REPO_ROOT / val).is_file()
    return False


def update_note_transcript_line(
    note_text: str, key: str, new_val: str, after_key: str | None = None
) -> tuple[str, bool]:
    """Rewrite or insert a transcript_file[_ptN]: line in note frontmatter.
    Uses whole-line regex rewrite if key exists; inserts after after_key,
    covers_also:, or transcript_file: if key is absent."""
    new_text, n_subs = re.subn(
        rf"^{key}:.*$",
        f"{key}: {new_val}",
        note_text,
        count=1,
        flags=re.MULTILINE,
    )
    if n_subs > 0:
        return new_text, True

    # Line absent: insert after after_key if present
    candidates = []
    if after_key:
        candidates.append(after_key)
    candidates.extend(["covers_also", "transcript_file"])

    for candidate in candidates:
        if re.search(rf"^{candidate}:.*$", note_text, re.MULTILINE):
            inserted = re.sub(
                rf"(^{candidate}:.*$)",
                rf"\1\n{key}: {new_val}",
                note_text,
                count=1,
                flags=re.MULTILINE,
            )
            return inserted, True

    return note_text, False


def archive_transcripts(
    inbox_dir: Path,
    archive_dir: Path = ARCHIVE_DIR,
    notes_dir: Path = SOURCE_NOTES_DIR,
    dry_run: bool = False,
) -> int:
    if not inbox_dir.exists():
        print(f"Inbox dir does not exist: {inbox_dir}", file=sys.stderr)
        return 1

    note_index = load_known_ids_from_notes(notes_dir)  # {primary_video_id: note_path}
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Build covers_also map: {covers_also_video_id: (note_path, part_num, primary_vid, all_part_ids)}
    covers_also_map: dict[str, tuple[Path, int, str, list[str]]] = {}
    note_to_parts: dict[Path, tuple[str, list[str]]] = {}  # note_path -> (primary_vid, [part2_id, part3_id, ...])

    for note_path in sorted(notes_dir.glob("YT_*.md")):
        try:
            text = note_path.read_text(encoding="utf-8")
        except OSError:
            continue
        m_vid = re.search(r"^video_id:\s*(\S+)\s*$", text, re.MULTILINE)
        primary_vid = m_vid.group(1).strip() if m_vid else ""
        m_cov = re.search(r"^covers_also:\s*(.+)$", text, re.MULTILINE)
        if m_cov and primary_vid:
            part_ids = extract_covers_also_ids(m_cov.group(1))
            note_to_parts[note_path] = (primary_vid, part_ids)
            for idx, cid in enumerate(part_ids):
                part_num = idx + 2
                covers_also_map[cid] = (note_path, part_num, primary_vid, part_ids)

    moved = []
    skipped_no_note = []
    skipped_no_meta = []
    skipped_already_archived = []
    touched_notes: set[Path] = set()

    for txt_path in sorted(inbox_dir.glob("*.txt")):
        meta_path = txt_path.parent / f"{txt_path.stem}.meta.json"
        if not meta_path.exists():
            skipped_no_meta.append(txt_path.name)
            continue

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  WARNING: could not read {meta_path.name}: {e}", file=sys.stderr)
            skipped_no_meta.append(txt_path.name)
            continue

        video_id = meta.get("video_id")
        sha256 = meta.get("sha256", "")
        hash8 = sha256[:8] if sha256 else "unknown"

        if not video_id:
            skipped_no_note.append((txt_path.name, video_id))
            continue

        is_primary = video_id in note_index
        is_covers_also = video_id in covers_also_map

        if not is_primary and not is_covers_also:
            skipped_no_note.append((txt_path.name, video_id))
            continue

        if is_primary:
            note_path = note_index[video_id]
            primary_vid = video_id
            part_key = "transcript_file"
            part_suffix = ""
            prev_key = None
        else:
            note_path, part_num, primary_vid, _ = covers_also_map[video_id]
            part_key = f"transcript_file_pt{part_num}"
            part_suffix = f"_pt{part_num}"
            prev_key = f"transcript_file_pt{part_num - 1}" if part_num > 2 else "transcript_file"

        note_text = note_path.read_text(encoding="utf-8")

        # Idempotency check: if note already points to a file that exists on disk, do nothing
        if note_pt_points_to_existing_file(note_text, part_key, archive_dir):
            skipped_already_archived.append((txt_path.name, note_path.name, part_key))
            touched_notes.add(note_path)
            continue

        slug = derive_slug_from_note(note_path, primary_vid)
        if not slug:
            print(
                f"  WARNING: note {note_path.name} doesn't start with expected prefix for "
                f"video_id={primary_vid!r} - skipping, fix manually.",
                file=sys.stderr,
            )
            skipped_no_note.append((txt_path.name, video_id))
            continue

        date_match = INBOX_DATE_PREFIX_RE.match(txt_path.stem)
        date_str = date_match.group(1) if date_match else date.today().strftime("%Y%m%d")

        new_txt_name = f"{date_str}_{slug}{part_suffix}_{hash8}.txt"
        new_meta_name = f"{date_str}_{slug}{part_suffix}_{hash8}.meta.json"
        new_txt_path = archive_dir / new_txt_name
        new_meta_path = archive_dir / new_meta_name
        new_relpath = f"_Archive/processed_sources/{new_txt_name}"

        new_note_text, replaced = update_note_transcript_line(
            note_text, part_key, new_relpath, after_key=prev_key
        )

        if dry_run:
            print(
                f"[dry-run] {txt_path.name} -> {new_relpath}"
                f"{'' if replaced else f'  (WARNING: no {part_key} match found in note to repoint)'}"
            )
        else:
            txt_path.rename(new_txt_path)
            meta_path.rename(new_meta_path)
            if replaced:
                note_path.write_text(new_note_text, encoding="utf-8")
            else:
                print(
                    f"  WARNING: moved {txt_path.name} but found no matching {part_key}: "
                    f"line in {note_path.name} to repoint - fix its frontmatter manually.",
                    file=sys.stderr,
                )

        moved.append((txt_path.name, new_relpath, note_path.name, replaced))
        touched_notes.add(note_path)

    # Check touched notes for any covers_also parts with no transcript present
    missing_parts = []
    for note_path in sorted(touched_notes):
        if note_path not in note_to_parts:
            continue
        primary_vid, part_ids = note_to_parts[note_path]
        curr_text = note_path.read_text(encoding="utf-8")
        for idx, cid in enumerate(part_ids):
            part_num = idx + 2
            part_key = f"transcript_file_pt{part_num}"
            if not note_pt_points_to_existing_file(curr_text, part_key, archive_dir):
                missing_parts.append((note_path.name, cid, part_num))
                print(
                    f"  WARNING: note {note_path.name} covers_also ID {cid!r} (pt{part_num}) "
                    f"has no transcript present in inbox or note.",
                    file=sys.stderr,
                )

    print()
    print(f"{'Would move' if dry_run else 'Moved'}: {len(moved)}")
    for old, new, note, replaced in moved:
        mark = "OK" if replaced else "NOTE NOT REPOINTED"
        print(f"  [{mark}] {old} -> {new}  (note: {note})")

    if skipped_already_archived:
        print(f"\nAlready archived on disk ({len(skipped_already_archived)}) - left in place:")
        for name, note_name, pkey in skipped_already_archived:
            print(f"  {name}  (note: {note_name}, field: {pkey})")

    if skipped_no_note:
        print(f"\nNo matching source note found ({len(skipped_no_note)}) - left in place:")
        for name, vid in skipped_no_note:
            print(f"  {name}  (video_id in meta.json: {vid!r})")

    if skipped_no_meta:
        print(f"\nNo .meta.json sidecar found ({len(skipped_no_meta)}) - left in place:")
        for name in skipped_no_meta:
            print(f"  {name}")

    if missing_parts:
        print(f"\nMissing covers_also transcripts for processed notes ({len(missing_parts)}):")
        for nname, cid, pnum in missing_parts:
            print(f"  {nname}: pt{pnum} (video_id: {cid!r})")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inbox_dir", help="Folder containing fetched transcripts + .meta.json sidecars.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen without moving/editing anything.")
    parser.add_argument(
        "--archive-dir",
        default=str(ARCHIVE_DIR),
        help=f"Target directory for archived transcripts (default: {ARCHIVE_DIR})",
    )
    parser.add_argument(
        "--notes-dir",
        default=str(SOURCE_NOTES_DIR),
        help=f"Directory containing source notes (default: {SOURCE_NOTES_DIR})",
    )
    args = parser.parse_args()

    return archive_transcripts(
        inbox_dir=Path(args.inbox_dir),
        archive_dir=Path(args.archive_dir),
        notes_dir=Path(args.notes_dir),
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
