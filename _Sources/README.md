# `_Sources/` — Source Extraction Notes

One Markdown note per processed source: a YouTube video, a rendered web page, a
document, or a screenshot bundle. Each note holds the structured extraction from
that source, its frontmatter provenance (URL, video ID, upload date, channel,
language, fetch method, `fact_yield`, `promotional_ratio`), and a pointer to the
raw evidence archived under `_Archive/processed_sources/`.

**Naming**: `YT_<video_id>_<short_slug>.md` for YouTube sources. The video ID in
the filename is what `tools/youtube/preflight_playlist.py` matches against for
deduplication — don't rename a note without understanding that.

## Why this is top-level

These notes are **vault-wide evidence, not one topic's material.** They lived
under `11_Budget_and_Planning/_supporting/knowledge/sources/` until 2026-08-30
for purely historical reasons — the budgeting guide happened to be the first
thing built here. By the time it was measured, `12_Engineering_and_Systems` cited
these notes from 44 files against `11_Budget_and_Planning`'s own 23, with 3,044
references spread across sixteen folders.

Top-level and underscore-prefixed matches the vault's existing convention for
cross-cutting infrastructure (`_Archive/`, `_Inbox/`, `_assets/`), and puts these
notes at the same tier as the raw transcripts in `_Archive/processed_sources/`
that they point to.

## What reads and writes this folder

- `.agents/skills/renovation-knowledge-intake/SKILL.md` — declares this as the
  canonical source-notes path and owns the intake pipeline.
- `tools/youtube/preflight_playlist.py` — dedup check before fetching.
- `tools/youtube/archive_transcripts.py` — repoints each note's `transcript_file:`
  after moving the transcript to `_Archive/`.
- `tools/build_knowledge_base_index.py` — indexes numeric claims from these notes.
- Every room and systems wiki page — cites them by wikilink.

Accumulated facts are synthesised into `_Knowledge/store/` and from there into the
room/systems wiki pages. A note here is the evidence layer, not reader content.
