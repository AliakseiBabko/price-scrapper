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
  1. Find the source note under 11_Budget_and_Planning/_supporting/knowledge/
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
SOURCE_NOTES_DIR = (
    REPO_ROOT
    / "11_Budget_and_Planning"
    / "_supporting"
    / "knowledge"
    / "sources"
)

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inbox_dir", help="Folder containing fetched transcripts + .meta.json sidecars.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen without moving/editing anything.")
    args = parser.parse_args()

    inbox_dir = Path(args.inbox_dir)
    if not inbox_dir.exists():
        print(f"Inbox dir does not exist: {inbox_dir}", file=sys.stderr)
        return 1

    note_index = load_known_ids_from_notes(SOURCE_NOTES_DIR)  # {video_id: note_path}
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    moved, skipped_no_note, skipped_no_meta = [], [], []

    for txt_path in sorted(inbox_dir.glob("*.txt")):
        meta_path = txt_path.with_suffix("").with_suffix(".meta.json")
        # (transcripts use "<name>.txt" / "<name>.meta.json", not "<name>.txt.meta.json")
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

        if not video_id or video_id not in note_index:
            skipped_no_note.append((txt_path.name, video_id))
            continue

        note_path = note_index[video_id]
        slug = derive_slug_from_note(note_path, video_id)
        if not slug:
            print(f"  WARNING: note {note_path.name} doesn't start with expected prefix for "
                  f"video_id={video_id!r} - skipping, fix manually.", file=sys.stderr)
            skipped_no_note.append((txt_path.name, video_id))
            continue

        date_match = INBOX_DATE_PREFIX_RE.match(txt_path.stem)
        date_str = date_match.group(1) if date_match else date.today().strftime("%Y%m%d")

        new_txt_name = f"{date_str}_{slug}_{hash8}.txt"
        new_meta_name = f"{date_str}_{slug}_{hash8}.meta.json"
        new_txt_path = ARCHIVE_DIR / new_txt_name
        new_meta_path = ARCHIVE_DIR / new_meta_name

        new_relpath = f"_Archive/processed_sources/{new_txt_name}"

        # Rewrite the transcript_file: frontmatter line directly by regex, rather than
        # substring-replacing an assumed old path. A previous version of this script
        # tried substring replacement with a couple of guessed old-path forms (full
        # inbox-relative path, then a bare-filename fallback) - the fallback matched
        # inside an already-updated line in one test case (the full-path form didn't
        # match due to an inbox-folder-name mismatch), silently producing a corrupted
        # nested path. Rewriting the whole line by its own key is unambiguous: it
        # doesn't matter what the old value was, only that a `transcript_file:` line
        # exists at all - and if it doesn't, that's reported, not guessed around.
        note_text = note_path.read_text(encoding="utf-8")
        new_note_text, n_subs = re.subn(
            r"^transcript_file:.*$",
            f"transcript_file: {new_relpath}",
            note_text,
            count=1,
            flags=re.MULTILINE,
        )
        replaced = n_subs > 0

        if args.dry_run:
            print(f"[dry-run] {txt_path.name} -> {new_relpath}"
                  f"{'' if replaced else '  (WARNING: no transcript_file match found in note to repoint)'}")
        else:
            txt_path.rename(new_txt_path)
            meta_path.rename(new_meta_path)
            if replaced:
                note_path.write_text(new_note_text, encoding="utf-8")
            else:
                print(f"  WARNING: moved {txt_path.name} but found no matching transcript_file: "
                      f"line in {note_path.name} to repoint - fix its frontmatter manually.",
                      file=sys.stderr)

        moved.append((txt_path.name, new_relpath, note_path.name, replaced))

    print()
    print(f"{'Would move' if args.dry_run else 'Moved'}: {len(moved)}")
    for old, new, note, replaced in moved:
        mark = "OK" if replaced else "NOTE NOT REPOINTED"
        print(f"  [{mark}] {old} -> {new}  (note: {note})")

    if skipped_no_note:
        print(f"\nNo matching source note found ({len(skipped_no_note)}) - left in place:")
        for name, vid in skipped_no_note:
            print(f"  {name}  (video_id in meta.json: {vid!r})")

    if skipped_no_meta:
        print(f"\nNo .meta.json sidecar found ({len(skipped_no_meta)}) - left in place:")
        for name in skipped_no_meta:
            print(f"  {name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
