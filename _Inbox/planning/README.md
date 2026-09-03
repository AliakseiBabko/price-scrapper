# `_Inbox/planning/` — what is in here

**This is a map, not a status board.** It says what each file is and where that file's *live* state
is recorded. **It deliberately does not copy round counts or open/closed status into this page**, because
a second copy of that state would drift from the first — which is exactly the failure that caused the
machine-local memory store to be drained into this repo on 2026-08-31, one of its notes already citing
a path that had stopped existing the day before.

**Created 2026-09-02.** Out of scope for the wiki page-shape rules in `00_Master/wiki_page_format.md`
— these are working documents, not vault pages.

## Read this first for any channel work

**[`youtube_channel_queue.md`](youtube_channel_queue.md) is the authoritative state of every channel** —
group classification, what is active, what is closed, the rate-limit channel-switching protocol, and a
Progress Log that is appended to at the close of every round. **Read it before starting new channel
work in any session, and update it at the end of one.** Where a channel's per-round detail lives in its
own file below, the queue is still the place that says whether the channel is open.

## Per-channel plan and triage files

Each holds the durable, cross-session plan for one channel: the video list, tier/cluster
classification, per-round results and the verdict. **Read the channel's own file before resuming it —
don't re-derive the video list or clustering from scratch.**

| File | Channel |
| :--- | :--- |
| `kruglov_ontario_full_channel_plan_20260824.md` | Konstantin Kruglov / Ontario — the largest plan file here |
| `petrishin_stroi_channel_plan_20260824.md` | Petrishin-Stroi |
| `krasnov_design_channel_triage_20260901.md` | Игорь Краснов / @krasnov_design |
| `kuzina_nadezhda_channel_plan_20260831.md` | Надежда Кузина / @kuzinadesign |
| `pavel_sidorik_channel_plan_20260824.md` | Pavel Sidorik |
| `shevrina_smbureau_channel_plan_20260830.md` | Мария Шеврина / SMBUREAU |
| `remproektmd_channel_plan_20260824.md` | RemProektMD |
| `flat_interio_channel_triage_20260902.md` | Мебельная компания FLAT / @flat_interio |
| `bezverkhaia_channel_triage_20260902.md` | Татьяна Безверхая / @tatianabezverkhaia |
| `mikhailovskaya_course_triage_20260901.md` | Татьяна Михайловская — one playlist, not a whole channel |
| `dolgushev_channel_triage_20260826.md` | @SergeyDolgushev / ARCHIDOLGUSHEV |
| `sbk_remont_channel_plan_20260828.md` | @sbk.remont / «ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ» — **reconstructed 2026-09-02 after the fact**; see its own warning |
| `timremont_channel_plan_20260824.md` | TimRemont |
| `kruglov_ontario_20260820.md` | Kruglov/Ontario — the earlier 4-video batch that predates the full plan above. **Superseded by it**; kept because it is the record of the process-convention test that established the routing default, the round-yield stopping signal and the batch-status JSON convention |

## Zemskov / Zemstandart — a four-file set, read in this order

The largest single-channel effort in the vault, split across four files as it progressed. **They are
sequential, not alternatives:**

1. `zemskov_full_channel_triage.md` — the original triage and category scheme. **Start here**; kept
   updated in place rather than superseded.
2. `zemskov_category4_candidates_20260818.md` — Category 4 candidate list.
3. `zemskov_category5_candidates_20260819.md` — Category 5 candidate list.
4. `zemskov_remainder_pool_20260819.md` — what was left after Category 5 closed the original triage.

## Vault-maintenance records (not channel work)

| File | What it holds |
| :--- | :--- |
| `page_splitting_backlog_20260831.md` | **The full history of the vault's page-shape work**, appended pass by pass: the original splitting backlog, the threshold recalibrations, the 300-line hard ceiling and **its correction to a soft target**, the 29-page fragmentation merge, and the housekeeping audit. **Read this before changing page-shape rules or tooling** — several rules here were arrived at by getting them wrong first, and the reasoning is more useful than the conclusions. Its content is mirrored into `_Knowledge/store/Change_Log.md`. |

## Machine-readable batch artifacts (not documents)

Alongside the markdown above, this folder holds **~58 non-markdown working artifacts** that are
deliberate records, not clutter:

- **`batch_status_<date>_<channel>_round<N>.json`** — per-round state: video list, per-video
  integration state, and (from partway through) the round yield. The convention was established by
  the 2026-08-20 Kruglov process test. ⚠️ **The schema drifted**: `round_yield` is absent in early
  files, free text in the middle, structured in later ones. **Anything parsing these must handle all
  three shapes** — that drift is why rounds 1–4 of `@sbk.remont` have no recoverable yield figures.
- **`preflight_<timestamp>.json`** — `preflight_playlist.py` output, the dedup record for a
  playlist/channel against `processed_video_ids.txt`.
- **`*_titles_dump.txt`**, `krasnov_round2_candidates_meta.json`, `sbk_remont_preflight` — inputs to
  the title-skim value-filter pass.

**Keep them.** They are the evidence a round actually happened, and reconstructing
`sbk_remont_channel_plan_20260828.md` was only possible because they were kept.

## Sibling folders under `_Inbox/`

`frames/`, `audio/`, `pdf_pages/`, `transcripts/`, `_Visual_Drop/` are **working scratch for
in-flight sources** and are gitignored apart from a few frame index files. Nothing durable should
live in them — a fact that matters belongs in a `_Sources/` extraction note or a wiki page.

## Conventions for this folder

- **One file per channel, created when the channel is first triaged**, named
  `<channel>_channel_plan_YYYYMMDD.md` or `<channel>_channel_triage_YYYYMMDD.md`. The date is the
  creation date and **is not updated** — the file is kept current in place, as
  `zemskov_full_channel_triage.md` records deliberately.
- **Append round results; don't rewrite earlier rounds.** A superseded verdict stays visible with a
  note pointing at what replaced it. Several findings in these files are corrections of earlier
  rounds by later ones, and that trail is the point.
- **Close a round by updating `youtube_channel_queue.md`'s Progress Log**, not only the channel file.
