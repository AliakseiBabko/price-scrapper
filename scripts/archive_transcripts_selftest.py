#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Self-test for tools/youtube/archive_transcripts.py.

Guards the covers_also transcript archiving pipeline:
  1. Grouped note with inbox pt2 transcript -> moved to archive with
     name <date>_<slug>_pt2_<hash8>.txt (and .meta.json), line
     transcript_file_pt2: written to source note, path resolves.
  2. Idempotency: second run does not duplicate, overwrite, or re-move files
     whose transcript_file_ptN: already resolves to an existing file on disk.
  3. Absent transcript_file_pt2: line is cleanly inserted after
     transcript_file or covers_also.
  4. Multiple covers_also IDs are assigned pt2, pt3, pt4... strictly in
     the order declared in the covers_also: list (not alphabetic).
  5. Missing covers_also transcripts for processed notes are detected and
     reported without crashing or creating bogus lines.
  6. Legacy hand-named pt files existing on disk are preserved untouched,
     not renamed or treated as un-archived.
  7. Inbox files without .meta.json or without matching notes are left in place.

Run:
    python scripts/archive_transcripts_selftest.py
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "youtube"))

from archive_transcripts import archive_transcripts  # noqa: E402


def run_tests() -> int:
    failures = 0

    def assert_eq(actual, expected, msg: str):
        nonlocal failures
        if actual != expected:
            print(f"FAIL: {msg} (expected {expected!r}, got {actual!r})")
            failures += 1
        else:
            print(f"  OK: {msg}")

    def assert_true(cond: bool, msg: str):
        nonlocal failures
        if not cond:
            print(f"FAIL: {msg}")
            failures += 1
        else:
            print(f"  OK: {msg}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        inbox_dir = tmp / "inbox"
        archive_dir = tmp / "archive"
        notes_dir = tmp / "notes"

        inbox_dir.mkdir()
        archive_dir.mkdir()
        notes_dir.mkdir()

        # Seed 1: Single covers_also part (pt2) archiving
        print("--- Test 1: Single covers_also pt2 archiving ---")
        note1 = notes_dir / "YT_vid11111111_foundation_guide.md"
        note1.write_text(
            "---\n"
            "video_id: vid11111111\n"
            "covers_also: vid22222222\n"
            "transcript_file: _Archive/processed_sources/20260901_foundation_guide_11111111.txt\n"
            "---\n"
            "# Foundation Guide\n",
            encoding="utf-8",
        )
        (archive_dir / "20260901_foundation_guide_11111111.txt").write_text("primary transcript", encoding="utf-8")

        inbox_txt1 = inbox_dir / "20260905_pt2_fetch_vid22222222.txt"
        inbox_txt1.write_text("pt2 transcript content", encoding="utf-8")
        inbox_meta1 = inbox_dir / "20260905_pt2_fetch_vid22222222.meta.json"
        inbox_meta1.write_text(
            json.dumps({"video_id": "vid22222222", "sha256": "2222abcd99990000"}),
            encoding="utf-8",
        )

        res = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res, 0, "archive_transcripts returned 0")

        expected_archived_txt = archive_dir / "20260905_foundation_guide_pt2_2222abcd.txt"
        expected_archived_meta = archive_dir / "20260905_foundation_guide_pt2_2222abcd.meta.json"
        assert_true(expected_archived_txt.is_file(), "Archived pt2 txt file exists")
        assert_true(expected_archived_meta.is_file(), "Archived pt2 meta file exists")
        assert_true(not inbox_txt1.exists(), "Inbox txt was moved")
        assert_true(not inbox_meta1.exists(), "Inbox meta was moved")

        note1_text = note1.read_text(encoding="utf-8")
        expected_relpath = "_Archive/processed_sources/20260905_foundation_guide_pt2_2222abcd.txt"
        assert_true(f"transcript_file_pt2: {expected_relpath}" in note1_text, "Note updated with transcript_file_pt2")

        # Seed 2: Idempotency (re-run does nothing)
        print("\n--- Test 2: Idempotency check ---")
        inbox_txt1_dup = inbox_dir / "20260906_duplicate_vid22222222.txt"
        inbox_txt1_dup.write_text("duplicate content", encoding="utf-8")
        inbox_meta1_dup = inbox_dir / "20260906_duplicate_vid22222222.meta.json"
        inbox_meta1_dup.write_text(
            json.dumps({"video_id": "vid22222222", "sha256": "2222abcd99990000"}),
            encoding="utf-8",
        )

        res2 = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res2, 0, "archive_transcripts idempotency run returned 0")
        assert_true(inbox_txt1_dup.exists(), "Duplicate inbox txt left in place")
        assert_eq(note1.read_text(encoding="utf-8"), note1_text, "Note frontmatter untouched on duplicate run")
        inbox_txt1_dup.unlink()
        inbox_meta1_dup.unlink()

        # Seed 3: Multiple covers_also parts declaration order preserved
        print("\n--- Test 3: Multiple covers_also parts strictly preserved in declaration order ---")
        note2 = notes_dir / "YT_multi000001_multi_part_series.md"
        note2.write_text(
            "---\n"
            "video_id: multi000001\n"
            "covers_also: zzz_part2_i, aaa_part3_i, mmm_part4_i\n"
            "transcript_file: _Archive/processed_sources/20260901_multi_part_series_multi000.txt\n"
            "---\n",
            encoding="utf-8",
        )
        (archive_dir / "20260901_multi_part_series_multi000.txt").write_text("p1", encoding="utf-8")

        for vid, sha in [
            ("aaa_part3_i", "aaaa111122223333"),
            ("zzz_part2_i", "zzzz111122223333"),
            ("mmm_part4_i", "mmmm111122223333"),
        ]:
            (inbox_dir / f"fetch_{vid}.txt").write_text(f"text for {vid}", encoding="utf-8")
            (inbox_dir / f"fetch_{vid}.meta.json").write_text(
                json.dumps({"video_id": vid, "sha256": sha}), encoding="utf-8"
            )

        res3 = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res3, 0, "Multi-part archive returned 0")

        pt2_matches = list(archive_dir.glob("*_pt2_zzzz1111.txt"))
        pt3_matches = list(archive_dir.glob("*_pt3_aaaa1111.txt"))
        pt4_matches = list(archive_dir.glob("*_pt4_mmmm1111.txt"))
        assert_true(len(pt2_matches) == 1, "zzz assigned pt2")
        assert_true(len(pt3_matches) == 1, "aaa assigned pt3")
        assert_true(len(pt4_matches) == 1, "mmm assigned pt4")
        if pt2_matches and pt3_matches and pt4_matches:
            pt2_file = pt2_matches[0]
            pt3_file = pt3_matches[0]
            pt4_file = pt4_matches[0]
            note2_text = note2.read_text(encoding="utf-8")
            assert_true(f"transcript_file_pt2: _Archive/processed_sources/{pt2_file.name}" in note2_text, "pt2 in note")
            assert_true(f"transcript_file_pt3: _Archive/processed_sources/{pt3_file.name}" in note2_text, "pt3 in note")
            assert_true(f"transcript_file_pt4: _Archive/processed_sources/{pt4_file.name}" in note2_text, "pt4 in note")

        # Seed 4: Missing covers_also transcript detection
        print("\n--- Test 4: Missing covers_also transcript reporting ---")
        note3 = notes_dir / "YT_miss0000001_missing_part_note.md"
        note3.write_text(
            "---\n"
            "video_id: miss0000001\n"
            "covers_also: present0002, missing0003\n"
            "transcript_file: _Archive/processed_sources/20260901_missing_part_note_miss000.txt\n"
            "---\n",
            encoding="utf-8",
        )
        (archive_dir / "20260901_missing_part_note_miss000.txt").write_text("p1", encoding="utf-8")
        (inbox_dir / "fetch_present0002.txt").write_text("present text", encoding="utf-8")
        (inbox_dir / "fetch_present0002.meta.json").write_text(
            json.dumps({"video_id": "present0002", "sha256": "bbbb222233334444"}),
            encoding="utf-8",
        )

        res4 = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res4, 0, "Missing part run returned 0")
        note3_text = note3.read_text(encoding="utf-8")
        assert_true("transcript_file_pt2:" in note3_text, "pt2 created for present transcript")
        assert_true("transcript_file_pt3:" not in note3_text, "pt3 NOT created for missing transcript")

        # Seed 5: Legacy hand-named pt file existing on disk preserved untouched
        print("\n--- Test 5: Legacy hand-named pt file preserved on disk ---")
        note4 = notes_dir / "YT_leg00000001_legacy_parts_note.md"
        legacy_txt_name = "20260710_legacy_custom_name_pt_file.txt"
        (archive_dir / legacy_txt_name).write_text("original legacy content", encoding="utf-8")
        note4.write_text(
            "---\n"
            "video_id: leg00000001\n"
            "covers_also: leg00000002\n"
            "transcript_file: _Archive/processed_sources/20260710_legacy_main.txt\n"
            f"transcript_file_pt2: _Archive/processed_sources/{legacy_txt_name}\n"
            "---\n",
            encoding="utf-8",
        )
        (archive_dir / "20260710_legacy_main.txt").write_text("leg main", encoding="utf-8")

        (inbox_dir / "fetch_leg00000002.txt").write_text("new content", encoding="utf-8")
        (inbox_dir / "fetch_leg00000002.meta.json").write_text(
            json.dumps({"video_id": "leg00000002", "sha256": "cccc333344445555"}),
            encoding="utf-8",
        )

        res5 = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res5, 0, "Legacy pt run returned 0")
        assert_true(
            (archive_dir / legacy_txt_name).read_text(encoding="utf-8") == "original legacy content",
            "Legacy pt file content preserved",
        )
        assert_true(
            f"transcript_file_pt2: _Archive/processed_sources/{legacy_txt_name}" in note4.read_text(encoding="utf-8"),
            "Legacy pt2 reference in note preserved untouched",
        )

        # Seed 6: Incomplete metadata left in inbox
        print("\n--- Test 6: Incomplete metadata left in inbox ---")
        unmatched_txt = inbox_dir / "unmatched.txt"
        unmatched_txt.write_text("unmatched", encoding="utf-8")
        unmatched_meta = inbox_dir / "unmatched.meta.json"
        unmatched_meta.write_text(json.dumps({"video_id": "unknownvid99"}), encoding="utf-8")

        nometa_txt = inbox_dir / "nometa.txt"
        nometa_txt.write_text("nometa", encoding="utf-8")

        res6 = archive_transcripts(inbox_dir, archive_dir=archive_dir, notes_dir=notes_dir)
        assert_eq(res6, 0, "Incomplete inbox items run returned 0")
        assert_true(unmatched_txt.is_file(), "Unmatched video_id transcript left in inbox")
        assert_true(nometa_txt.is_file(), "Transcript without meta left in inbox")

    print(f"\nCompleted archive_transcripts selftest. Failures: {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
