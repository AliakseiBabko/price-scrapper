#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Preflight triage for a YouTube playlist/channel before fetching anything.

Cross-checks every video ID in a playlist against this repo's own
processed-source records (00_Master/processed_sources.csv and the
YT_<video_id>_*.md source notes under
11_Budget_and_Planning/_supporting/knowledge/sources/) *before* any
transcript is fetched, and probes availability/caption presence for the
IDs that aren't already known.

Why this exists (see conversation history 2026-08-04): duplicate/
availability/caption discovery was previously done with ad hoc one-off
python snippets and manual yt-dlp --print calls per playlist run. That
approach (a) matched duplicates by source_hash after fetching rather than
by video ID before fetching, missing rows whose source_hash is "n/a"
(e.g. prior duplicate_skipped/skipped rows); and (b) printed metadata
through the console, which mangled Cyrillic titles under some terminal
codepages. This script fixes both: canonical-ID matching happens first
(no network needed), and all metadata is pulled via yt_dlp's Python API
and written straight to UTF-8 JSON/text, never round-tripped through a
console.

Usage:
    python tools/youtube/preflight_playlist.py <playlist_or_channel_url> \\
        --output-dir <dir>

Output:
    - A triage table printed to stdout (ASCII-safe, no raw Cyrillic
      relied upon for correctness - full titles go to the JSON manifest).
    - `<output-dir>/preflight_<timestamp>.json`: full manifest, UTF-8,
      one entry per video: {video_id, title, upload_date, channel,
      status, reason, existing_run_id (if duplicate)}.

This script only reads state - it never writes to processed_sources.csv,
moves any file, or fetches a transcript. It is a decision aid for the
fetch step that follows (youtube-transcript-fetch / get_youtube_transcript.py),
not a replacement for either.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = REPO_ROOT / "00_Master" / "processed_sources.csv"
SOURCE_NOTES_DIR = (
    REPO_ROOT
    / "11_Budget_and_Planning"
    / "_supporting"
    / "knowledge"
    / "sources"
)

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")

# Matches watch?v=, youtu.be/, shorts/, embed/, or a playlist item's own
# v= param buried in a longer URL - deliberately permissive, canonicalize()
# below is what actually validates the extracted candidate.
URL_ID_PATTERNS = [
    re.compile(r"[?&]v=([A-Za-z0-9_-]{11})"),
    re.compile(r"youtu\.be/([A-Za-z0-9_-]{11})"),
    re.compile(r"/shorts/([A-Za-z0-9_-]{11})"),
    re.compile(r"/embed/([A-Za-z0-9_-]{11})"),
]


def canonicalize_video_id(candidate: str) -> str | None:
    """Extract an 11-char YouTube video ID from a URL or bare ID string.

    Returns None if nothing matching a video ID shape can be found -
    never guesses/truncates, since a wrong canonicalization would corrupt
    the whole duplicate check silently.
    """
    candidate = candidate.strip()
    if VIDEO_ID_RE.match(candidate):
        return candidate
    for pattern in URL_ID_PATTERNS:
        m = pattern.search(candidate)
        if m:
            return m.group(1)
    return None


def load_known_ids_from_csv(csv_path: Path) -> dict[str, dict]:
    """Return {video_id: {"run_id": ..., "status": ..., "source_title": ...}}.

    Every source_url in the CSV is canonicalized, not string-matched - a
    row logged as `https://www.youtube.com/watch?v=XYZ` and one logged as
    a bare ID would otherwise be treated as different sources.
    """
    known: dict[str, dict] = {}
    if not csv_path.exists():
        return known
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = canonicalize_video_id(row.get("source_url", ""))
            if vid:
                known[vid] = {
                    "run_id": row.get("run_id"),
                    "status": row.get("status"),
                    "source_title": row.get("source_title"),
                }
    return known


def load_known_ids_from_notes(notes_dir: Path) -> dict[str, Path]:
    """Return {video_id: note_path}, reading each note's own frontmatter
    `video_id:` field rather than trusting the filename - the filename is
    a human-chosen slug and has already been observed to diverge from the
    true ID (e.g. a leading underscore dropped by an extraction agent)."""
    known: dict[str, Path] = {}
    if not notes_dir.exists():
        return known
    for note_path in notes_dir.glob("YT_*.md"):
        try:
            text = note_path.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^video_id:\s*(\S+)\s*$", text, re.MULTILINE)
        if m:
            vid = m.group(1).strip()
            known[vid] = note_path
    return known


def list_playlist_video_ids(playlist_url: str) -> list[dict]:
    """Flat-list a playlist's videos via yt_dlp's Python API (not the CLI -
    keeps everything in-process and UTF-8, no console round-trip)."""
    import yt_dlp

    ydl_opts = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    entries = info.get("entries") or []
    out = []
    for e in entries:
        if not e:
            continue
        vid = e.get("id")
        if not vid or not VIDEO_ID_RE.match(vid):
            continue
        out.append({"video_id": vid, "title": e.get("title")})
    return out


def probe_video(video_id: str, languages: list[str]) -> dict:
    """Fetch just enough per-video metadata to know availability + whether
    a caption track exists in a preferred language, without downloading
    anything. One extract_info call per video - same network cost as the
    manual --print probing done previously, just via the Python API so
    the result never passes through a terminal codepage."""
    import yt_dlp

    class _SilentLogger:
        """yt_dlp logs DownloadError details to stderr even with quiet=True -
        expected here (private/unavailable videos are a normal outcome, not
        a bug), so suppress it; the exception message is still captured and
        surfaced in the result/manifest, just not duplicated to the console."""

        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True, "logger": _SilentLogger()}
    result = {
        "video_id": video_id,
        "title": None,
        "upload_date": None,
        "channel": None,
        "status": "fresh",
        "reason": None,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        msg = str(e)
        if "Private video" in msg:
            result["status"] = "private"
        elif "unavailable" in msg.lower():
            result["status"] = "unavailable"
        else:
            result["status"] = "unavailable"
        result["reason"] = msg.splitlines()[-1][:300]
        return result

    result["title"] = info.get("title")
    result["upload_date"] = info.get("upload_date")
    result["channel"] = info.get("channel") or info.get("uploader")

    subs = info.get("subtitles") or {}
    auto_subs = info.get("automatic_captions") or {}
    has_captions = any(lang in subs for lang in languages) or any(
        lang in auto_subs for lang in languages
    )
    if not has_captions:
        result["status"] = "no_captions"
        result["reason"] = (
            f"no manual or auto-generated subtitle track for any of {languages} "
            f"(available manual: {sorted(subs.keys())[:10]}, "
            f"available auto: {sorted(auto_subs.keys())[:10]})"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("playlist_url", help="Playlist or channel URL to triage.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Where to write the JSON manifest. Required - this script never assumes "
             "a temp directory (see project history: /tmp is not reliably shared "
             "between the calling shell and this interpreter on this machine).",
    )
    parser.add_argument(
        "--languages",
        default="ru,en",
        help="Comma-separated caption-language preference order for the caption-"
             "presence probe (default: ru,en). Does not affect duplicate detection.",
    )
    parser.add_argument(
        "--skip-probe",
        action="store_true",
        help="Only do the (fast, no-network) duplicate check; skip the per-video "
             "availability/caption probe for fresh IDs.",
    )
    args = parser.parse_args()

    languages = [l.strip() for l in args.languages.split(",") if l.strip()]
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    known_csv = load_known_ids_from_csv(CSV_PATH)
    known_notes = load_known_ids_from_notes(SOURCE_NOTES_DIR)

    # Cross-check the two sources of truth against each other - a mismatch is a
    # data-quality signal worth surfacing, not silently ignored.
    csv_only = sorted(set(known_csv) - set(known_notes))
    notes_only = sorted(set(known_notes) - set(known_csv))

    print(f"Fetching playlist listing for: {args.playlist_url}", file=sys.stderr)
    entries = list_playlist_video_ids(args.playlist_url)
    print(f"Playlist lists {len(entries)} video(s).", file=sys.stderr)

    manifest = []
    counts = {"duplicate": 0, "private": 0, "unavailable": 0, "no_captions": 0, "fresh": 0}

    for entry in entries:
        vid = entry["video_id"]
        if vid in known_csv:
            row = known_csv[vid]
            manifest.append({
                "video_id": vid,
                "title": entry.get("title"),
                "status": "duplicate",
                "reason": f"already logged as {row['run_id']} (status={row['status']})",
                "existing_run_id": row["run_id"],
            })
            counts["duplicate"] += 1
            continue

        if args.skip_probe:
            manifest.append({"video_id": vid, "title": entry.get("title"), "status": "fresh", "reason": None})
            counts["fresh"] += 1
            continue

        print(f"  probing {vid}...", file=sys.stderr)
        probed = probe_video(vid, languages)
        manifest.append(probed)
        counts[probed["status"]] = counts.get(probed["status"], 0) + 1

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = out_dir / f"preflight_{timestamp}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "playlist_url": args.playlist_url,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "counts": counts,
                "csv_notes_mismatch": {
                    "in_csv_no_note": csv_only,
                    "in_notes_no_csv_row": notes_only,
                },
                "entries": manifest,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print(f"Manifest written to: {manifest_path}")
    print()
    print("Triage summary:")
    for status, n in counts.items():
        if n:
            print(f"  {status:12s} {n}")
    if csv_only:
        print(f"\n  NOTE: {len(csv_only)} CSV row(s) have a source_url but no matching source note "
              f"(expected for skipped/duplicate/failed rows - verify if unexpected).")
    if notes_only:
        print(f"\n  WARNING: {len(notes_only)} source note(s) have no matching CSV row - "
              f"these look unlogged, not just unfetched: {notes_only[:10]}")

    fresh_ids = [e["video_id"] for e in manifest if e["status"] == "fresh"]
    print(f"\n{len(fresh_ids)} video(s) ready to fetch: {', '.join(fresh_ids) if fresh_ids else '(none)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
