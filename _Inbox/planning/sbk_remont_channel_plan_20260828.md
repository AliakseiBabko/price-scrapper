# @sbk.remont / «ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ» — Channel Plan

**Channel**: https://www.youtube.com/@sbk.remont — Vladimir Amelchenko, business/premium-segment
turnkey renovation, St. Petersburg. 94 videos at preflight.

> [!WARNING]
> **This file was reconstructed on 2026-09-02, after the channel had already been fully processed.**
> It is the only worked channel in this vault that never got a plan file, and the omission had a real
> consequence: **`youtube_channel_queue.md` still described it as "3-video trial complete, awaiting
> user go-ahead before Round 1" while 7 rounds and 58 sources had actually been processed.** A future
> session reading the queue would have concluded the channel was untouched — and `preflight_playlist.py`
> dedups against `processed_video_ids.txt`, so it would have caught the duplicates, but only after the
> planning work had been redone.
>
> **What is below is reconstructed from evidence** — the seven `batch_status_20260828_sbk_round*.json`
> files, the 58 `_Sources/*_sbk_*.md` notes, and `00_Master/processed_sources.csv`. **Where the
> evidence does not record something, this file says so rather than reconstructing it.**

## Status: processed, 7 rounds. Treat as complete unless the channel publishes new content.

## What the evidence records

| Round | Videos | Facts | Yield | Recorded outcome |
| :--- | ---: | ---: | ---: | :--- |
| Trial (3-video title-skim) | 3 | — | — | **3-for-3 clean pass**, low promotional ratio all three |
| 1 | 7 | not recorded | not recorded | all 7 `integrated` |
| 2 | 8 | not recorded | not recorded | all 8 `integrated` |
| 3 | 8 | not recorded | not recorded | 7 `integrated`, **1 archived — satire, zero extraction, fully logged** |
| 4 | 8 | not recorded | not recorded | all 8 `integrated` |
| 5 | 8 | 55 | **6.875** | 7 full, 1 partial. No rate-limit; all 8 fetched serially with real spacing |
| 6 | 8 | 47 | **5.875** | ~15% decrease on Round 5 — within the 50%-drop threshold, above the 1.0/video floor |
| 7 | 8 | 52 | **6.5** | **+10.6% on Round 6** — no decay at close. No video skipped or archived |
| **Total** | **55 + 3 trial** | — | — | **58 source notes** |

⚠️ **Rounds 1–4 recorded only per-video state, not fact yield** — the `round_yield` field was added to
the batch-status convention partway through this channel (absent in rounds 1–4, free text in 5–6,
structured in 7). **Those four rounds' yields are not recoverable from the artifacts and are not
reconstructed here.** The three that are recorded show no decay: 6.875 → 5.875 → 6.5.

## Why the channel earned full processing

From the trial, per the queue's own entry: quartz-vinyl terminology and selection (`KXmidtaUNxI`);
concealed-mount door schedule, cost and swing-angle consequences (`ukZBqIlz8e0`), which **nuanced the
existing Ontario door note independently**; and 11 business/premium planning-process points
(`33b61qeO_XY`), which **independently corroborated the ARCHWOOD author-supervision-versus-technical-
supervision distinction.**

## What this channel is cited for in the vault

Amelchenko appears across the vault as a named practitioner — the **ten "cheapening" mistakes** cluster
in `17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md`, the **wallpaper
selection and retail-layer buying guide** in
`13_Surfaces_and_Finishes/analysis/Wallpaper_Selection_and_Hanging.md`, the **stretch-ceiling
acceptance checklist and pre-work liability act** in `13_Surfaces_and_Finishes/Ceilings_Guide.md`, the
**bathroom exhaust-fan control modes and late-stage wiring trap** in
`12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md`, and **replanning approval
and late-stage sequencing rules** in `11_Budget_and_Planning/Renovation_Sequence.md`.

## ⚠️ Note on transcript provenance for this channel

**Most of this channel's notes carry `transcript_file: not separately archived — fetched inline via
youtube_transcript_api (sha256 …)`** rather than a path into `_Archive/processed_sources/`. That is a
deliberate, hash-bearing provenance record, not a missing file — the content hash is the integrity
guarantee. Do not "repair" those lines into paths.

## Reopening condition

**Re-run `tools/youtube/preflight_playlist.py` only if the channel publishes new content.** 94 videos
existed at preflight and 58 became sources; the remainder was filtered by title-skim and the value
filter, not left unprocessed by accident.
