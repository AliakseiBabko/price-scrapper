# Zemskov/Zemstandart full-channel batch — triage state

**Last updated 2026-08-18.** Originally written 2026-08-17; kept updated in
place rather than superseded, since a fresh session should read this one
file and get the current picture without cross-referencing several dated
versions.

Channel: `https://www.youtube.com/@Земстандарт/videos`
Preflight manifest: `_Inbox/transcripts/preflight_20260817T115037Z.json` (local-only, gitignored — regenerate with `preflight_playlist.py` if missing)
Full fresh-title dump (UTF-8, tab-separated `#\tvideo_id | title`): `_Inbox/transcripts/channel_fresh_titles.txt` (local-only, gitignored)
Category 4 candidate list (re-derived 2026-08-18, chunked): `_Inbox/planning/zemskov_category4_candidates_20260818.md` (tracked in git)

> [!NOTE]
> This file and the Category 4 candidate list live in `_Inbox/planning/`, not `_Inbox/transcripts/` — the latter is entirely gitignored (raw transcript dumps), so planning/triage docs that need to survive across sessions and machines belong here instead. `channel_fresh_titles.txt` and the preflight manifest are raw data and stay in the ignored `transcripts/` folder — they're regeneratable from `preflight_playlist.py` if a fresh clone doesn't have them locally.

Preflight result: **372 total videos, 214 already duplicates (already in `00_Master/processed_sources.csv` / source notes), 158 fresh.** Title-skim triage sorted the 158 fresh videos into 5 categories (row numbers below refer to `channel_fresh_titles.txt`).

## Category 1 — Off-topic / channel-meta / self-promo tool (EXCLUDE, never fetch)
Rows: 1, 6, 9, 32, 33, 36, 37, 90, 99, 49 (10 videos). Not renovation content — never fetch.

## Category 2 — Cleaning products / customer testimonial (low priority, likely exclude)
Rows: 31, 124 (2 videos). Not triaged further; default to skip unless revisited.

## Category 3 — Numbered "Top N mistakes/lifehacks" round-ups — ✅ DONE (18/18)

All 18 videos triaged 2026-08-18 across 3 chunks: 12 fetched and fully integrated (source notes + intermediate store + wiki-page routing), 6 no-captions (`skipped` in the CSV). This tier substantially outperformed Category 5's baseline — 10 of 12 fetched videos were dense and low-promotion, including several genuinely important safety rules (radiator/laminate expansion-gap mechanism, countertop-joint sealant mechanism, a pressure-testing QC protocol). See the 2026-08-18 entries in `00_Master/processed_sources.csv` (`run_20260818_*`, the Category 3 rows) and the intermediate store's Change Log for full detail. Nothing further to do here.

## Category 4 — Clear technique/how-to videos — 🔄 IN PROGRESS (chunk 1 of ~6 done)

Row list re-derived 2026-08-18 (the original "~45-50 videos" estimate wasn't precise) into **~36 genuine candidates**, chunked into groups of 6-7. Full chunked list, with exclusion reasoning, is in `_Inbox/planning/zemskov_category4_candidates_20260818.md` — **read that file before continuing this category**, don't re-derive from scratch.

**Chunk 1 — done 2026-08-18** (7 targeted, 6 fetched + 1 no-captions): masonry technique (foam-glue bonding + first-course leveling, with a numeric client-facing QC threshold), a full window replacement + measurement masterclass, and — the standout — a complete mechanism-explained plumbing stub-out coordinate reference by fixture type. One video (a glass-unit "crash test") matched the title heuristic but turned out to be a low-value stunt video, correctly flagged rather than padded out. 5 of 6 fetched videos were genuinely dense.

**Chunks 2-6 — not yet started**, ~29 candidates remaining. Same pacing as before: fetch one chunk (6-7 videos) serialized with real spacing, extract, integrate into the store, then **do the wiki-routing check before starting the next chunk** — don't defer it (see the skill file's step 5a, hardened 2026-08-18 after this exact gap was found and fixed).

## Category 5 — Single-apartment "$X wasted, thanks to the designer/developer" dunk case-studies — 🔄 3-video trial done, ~75-80 remain, awaiting user decision on pace

A 2026-08-05 direct trial on this format found it "heavily self-promotional with thin technical yield." A follow-up 3-video trial on 2026-08-17/18 (`DPnZjaSPACA` no-captions, `MNVBzis94Yw`, `cidd4YHBJdA`) found the opposite — both fetched videos cleared the value bar strongly, one (`MNVBzis94Yw`) had essentially zero promotional content. Both were fully integrated into the store. **~75-80 videos in this category remain unprocessed** — the user has not yet decided whether/how to continue into the rest of this category. If resuming: re-derive a chunked candidate list the same way Category 4's was built (cross-reference `channel_fresh_titles.txt` against `00_Master/processed_sources.csv`), and consider doing a slightly larger second trial chunk (5-6 videos) before committing to the full ~75-80, given the two trials so far gave contradictory signals about this format's average value.

## What to do next (in a new session)

1. Read this file, then `.agents/skills/renovation-knowledge-intake/SKILL.md` directly (**not** via the `Skill` tool — that path isn't reliably resolved; see the file's own "How to invoke this file" note).
2. If continuing Category 4: read `_Inbox/planning/zemskov_category4_candidates_20260818.md`, confirm chunk 2's video IDs are still unprocessed (`grep` each against `00_Master/processed_sources.csv`), then fetch serialized with real spacing.
3. After each chunk: integrate into the intermediate store, **then do the wiki-page-routing check before moving to the next chunk** — per-source/per-chunk, not a deferred batch pass (this was a real gap found and fixed 2026-08-18, now documented in the skill file's step 5a).
4. If a topic's content has no existing wiki page: note it in the store's "Pending Wiki-Page Decisions" section (near the top of `renovation_budgeting_knowledge_store.md`) rather than leaving it implicit — and if 3+ sources have accumulated on one sub-topic with no page, build the page that session (see that section's own threshold rule; the Windows page was the first real application of it).
5. Standing rules still apply: serialize fetches with real spacing (rate-limit risk), verify every background-agent "completed" claim against `git status --short` and CSV row count before trusting it, chunk large batches (6-8 videos), use the collision-safe `run_id` format (`run_<date>_<video_id>`), confirm upload dates via `yt-dlp` metadata, commit+push only when the user asks (branch first if on `main`).
