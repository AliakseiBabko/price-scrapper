# Zemskov/Zemstandart remainder pool — post-Category-5 continuation

**Created 2026-08-19**, after the full Category 5 batch (37 videos, 2 trials + 4 chunks)
closed out the original full-channel triage (`_Inbox/planning/zemskov_full_channel_triage.md`).
This file tracks the **~56-video remainder** that the original triage's Category 5
candidate-derivation pass (`_Inbox/planning/zemskov_category5_candidates_20260819.md`,
its "Explicitly excluded from Category 5" section) set aside as *not* matching the strict
"$X wasted, thanks to the designer/developer" dunk pattern — but which is still real,
untouched renovation content from this channel.

## Scope decision (explicit user direction, 2026-08-19)

The user's own renovation is a **new-build apartment**, not secondary/old-building
("вторичка"/старый фонд) housing. When a candidate video turns out to be specifically
about secondary/old-building renovation:
- **Do not skip it outright** — old-building videos can still contain general technique
  tips that cross over to new-build (electrical, plumbing-component choices, balcony
  enclosure technique, etc.).
- **Do extract only the crossover-relevant points** (PARTIAL extraction), explicitly
  skipping content that's inherently old-building-specific (weak-wall entrance-door
  reinforcement, cast-iron-stack replace/keep judgment, old-wall soundproofing retrofit
  thickness, "temper your expectations" framing for cramped old layouts, etc.).
- See `YT_ajtv-urp18I_old_building_crossover_tips_101.md` for a worked example of this
  exact scoping decision already applied once.

Everything else about this project's standing conventions (serialize fetches, wiki-route
per-chunk not deferred, branch→commit→push→merge→delete-branch, CSV `run_id` format,
confidence tagging, etc.) is unchanged — see `.agents/skills/renovation-knowledge-intake/SKILL.md`
(read directly, **not** via the `Skill` tool — see that file's own "How to invoke this
file" note) for the full canonical process.

## Two permanently-excluded buckets — never fetch these

These were excluded by design during the original Category 5 candidate derivation and
that decision still stands; they are **not** part of this remainder pool's further work:

- **Channel-meta/self-promo (11 videos)**: `WGlKAKn6hQY`, `peyUIi32BpM`, `Y7YU4tKDxfg`,
  `2Ha1CBay93Y`, `SlnTNHiYzUo`, `YDXw0qHMaBI`, `dZ4_TkZmO2M`, `e0jbZYAFT_g`,
  `SUUGeKWlcj4`, `widAQZWdMcU`, `304zZRMZUoQ`.
- **Legal/dispute/named-individual callout (4 videos)**: `oycgnkyYii4` ("Wall of Shame"),
  `sxUZ_TwgMdQ`, `Duyq7P53pH4`, `ayQj0W9rd8o` (middleman lawsuit content).

## Already processed from this remainder pool (24 videos, 2026-08-19 session) — closes out the original 17-video candidate list

A probe (3 videos, user-requested) followed by one small batch (4 videos):

| Video ID | Title | Outcome |
|---|---|---|
| `zPR8PGWq5lA` | "О чём жалеют после ремонта? #229" | ✅ FULL — new-build, title/content mismatch (real 3-year deviations-and-costs case study), dense |
| `ajtv-urp18I` | "Ремонт квартиры в старой пятиэтажке #101" | ⚠️ PARTIAL — old-building, only crossover tips extracted per scoping rule |
| `MIA1tpRglGg` | "Затопили квартиру с готовым ремонтом! #068" | ❌ SKIPPED — no captions (genuine failure, confirmed via both fetch methods) |
| `_ahC-OK0dp4` | "Самый удобный ремонт квартиры в новостройке #508" | ✅ FULL — new-build, 1-year client testimonial |
| `jrqEbkU4Wj8` | "Когда застройщик хуже дизайнера #257" | ✅ FULL — new-build, standout door-swing-direction exception finding |
| `hvPddB5Lc1s` | "Самые дикие ошибки в ремонте квартиры. Румтур #103" | ✅ FULL — hotel-room QC tour format, several new ergonomic rules |
| `HHIUvRywQ6k` | "Самая сложная двушка что я видел! #226" | ✅ FULL — new-build, rare level-1 St. Petersburg region confirmation |
| `o4KitYl8vpU` | "THE STUPIDEST LAYOUT I'VE EVER SEEN. APARTMENT RENOVATION #116" | ✅ FULL — new-build, closet-niche-beside-door load-bearing-wall sizing formula |
| `Af8nNyn9a_c` | "САМАЯ ГЛУПАЯ ОШИБКА В ПЛАНИРОВКЕ КВАРТИРЫ #113" | ✅ FULL — new-build, wall-plane flush-alignment technique + quantified 10% exception |
| `WmkOC9uKnCQ` | "BEST KITCHEN-LIVING ROOM LIFE HACK #154" | ✅ FULL — new-build, dense numeric kitchen-living-loggia sequence; radiator-niche formula flagged as same-project overlap with `CHCB4KPupyc` |
| `7qxFoOsLAe8` | "ДИЗАЙН КУХНИ-ГОСТИНОЙ СВОИМИ РУКАМИ! #134" | ❌ SKIPPED — no captions (genuine failure, confirmed via both fetch methods) |
| `v7UXJ5fJ0H0` | "THE STUPIDEST LAYOUT I'VE EVER SEEN 2019. #520" | ✅ FULL — new-build, confirmed title/content mismatch, dense real 111.5m² full-replan case; disconfirms the #5xx-off-topic hypothesis |
| `f1KpZOQSZgQ` | "ПРОЕКТ И РЕМОНТ ДВУХКОМНАТНОЙ КВАРТИРЫ 60М2 #513" | ✅ FULL — client workflow interview, process heuristics + 2 design cautions |
| `ZvyXuUJ__Ag` | "APARTMENT RENOVATION. BEWARE OF MIDDLEMEN! #511" | ⚠️ PARTIAL — named-individual dispute content excluded, only generalizable scam-mechanism/red-flags extracted |
| `JHP3Fuf2KyA` | "САМАЯ БЕСПОЛЕЗНАЯ ДВУШКА ЧТО Я ВИДЕЛ #066" | ❌ SKIPPED — no captions (genuine failure, matches the early-number-risk caution) |
| `3PJJTDkppUg` | "НЕ ДАЙ СЕБЯ ОБМАНУТЬ НА РЕМОНТЕ! #504" | ✅ FULL — confirmed title/content mismatch, pure expense-tracking-methodology video, high relevance to self-managed plan |
| `XahTpDGjf9w` | "КАК ВЗЛОМАТЬ ЛЮБУЮ КВАРТИРУ! #204" | ❌ SKIPPED — no captions (genuine failure) |
| `n7X10oIqugU` | "THE MOST SHITTY APARTMENT I'VE EVER SEEN! #252" | ✅ FULL — dense full-replan case; corrected WC-width figure to a corroboration of existing WC_Guide.md formula |
| `8Xy-h8cS_-s` | "THE WORST TWO-ROOM APARTMENT I'VE EVER SEEN! #234" | ✅ FULL — dense numeric planning-logic masterclass; title-similarity duplicate-risk flag against `1pU60p0Jh3A` **resolved below (not a duplicate)** |
| `W9cCxVQVVes` | "THE HARDEST ONE-ROOM APARTMENT! #232" | ⚠️ PARTIAL — same production cluster, 5 new points despite heavy overlap |
| `HVSZh0lH9hk` | "САМАЯ Е..НУТАЯ ДВУШКА ЧТО Я ВСТРЕЧАЛ!!! #230" | ⚠️ PARTIAL — same production cluster, 9 new points |
| `1pU60p0Jh3A` | "The worst two-room apartment I've ever seen!!! #228" | ⚠️ PARTIAL — **title-similarity duplicate-risk check against `8Xy-h8cS_-s` resolved: confirmed independent project**, not a reused script |
| `ZVoExA0t6nI` | "THE MOST USELESS 3-BEDROOM APARTMENT I'VE EVER SEEN! #223" | ⚠️ PARTIAL — same production cluster, standout curved-wall-to-faceted-corner technique |
| `D8t1ADisUE8` | "ODNUSHKA FOR 200 LEMONS!!! #246" | ✅ FULL — confirmed title/content mismatch; standout finding: bedroom-under-neighbor's-kitchen water-risk caution |

All 24 are logged in `00_Master/processed_sources.csv` (`run_20260819_<video_id>`), have
source extraction notes under `11_Budget_and_Planning/_supporting/knowledge/sources/`,
are integrated into the intermediate store's Change Log, and were wiki-routed the same
session (see each source note's own "Target Page(s)" section for exactly which wiki
pages were touched). Merged to `main` — no lingering branch.

## Remaining candidates: NONE — this 17-video list is fully processed

All 17 original candidates from this file are now processed (13 FULL, 4 PARTIAL with named-individual/redundancy exclusions noted, 4 genuine no-captions skips across the full 2026-08-19 session — see the "Already processed" table above for the complete breakdown). **The 2026-08-19 batch-2/3/4/5 videos (`W9cCxVQVVes` through `D8t1ADisUE8`) belong to a distinct July-November 2023 narrated-planning-logic production cluster** (at least 6 videos: `ZVoExA0t6nI` #223, `1pU60p0Jh3A` #228, `HVSZh0lH9hk` #230, `W9cCxVQVVes` #232, `8Xy-h8cS_-s` #234, `n7X10oIqugU` #252) with heavy content overlap across the cluster — worth remembering if any further video from this same production period surfaces in a future candidate-derivation pass, since it will likely need the same PARTIAL/corroboration-heavy treatment.

**This remainder pool's broader ~50-video source** (`_Inbox/planning/zemskov_category5_candidates_20260819.md`'s "Explicitly excluded from Category 5" section) may still contain further unprocessed candidates beyond this specific 17-video list — a future session should re-derive a fresh candidate list from that source if the user wants to continue further, rather than assuming this file's exhaustion means the whole remainder pool is done.
| `XahTpDGjf9w` | "КАК ВЗЛОМАТЬ ЛЮБУЮ КВАРТИРУ! #204" | security/lock-focused, niche angle |
| `n7X10oIqugU` | "THE MOST SHITTY APARTMENT I'VE EVER SEEN! #252" | — |
| `8Xy-h8cS_-s` | "THE WORST TWO-ROOM APARTMENT I'VE EVER SEEN! #234" | — |
| `W9cCxVQVVes` | "THE HARDEST ONE-ROOM APARTMENT! #232" | layout-challenge format, this format scored well in this session |
| `HVSZh0lH9hk` | "САМАЯ Е..НУТАЯ ДВУШКА ЧТО Я ВСТРЕЧАЛ!!! #230" | — |
| `1pU60p0Jh3A` | "The worst two-room apartment I've ever seen!!! #228" | title very close to `8Xy-h8cS_-s` — check for duplicate/reused-script risk before assuming independent value (this channel has done this before, see Category 5 chunk 1's `N0AvLnbDShs`) |
| `ZVoExA0t6nI` | "THE MOST USELESS 3-BEDROOM APARTMENT I'VE EVER SEEN! #223" | — |
| `D8t1ADisUE8` | "ODNUSHKA FOR 200 LEMONS!!! #246" | dunk-style title despite being in this bucket — worth a title/content-mismatch check |

**Caution on `#5xx`-numbered videos**: `LVerbq1hkxg` (#549, processed in the Category 5
batch) turned out to be an almost entirely off-topic sponsored car-fleet promotional
video wearing a renovation-critique title. Four videos in this remaining list
(`v7UXJ5fJ0H0` #520, `f1KpZOQSZgQ` #513, `ZvyXuUJ__Ag` #511, `3PJJTDkppUg` #504) share
that same non-sequential high-number pattern relative to this channel's other
~#200-280-era videos. Not a reason to skip them outright, but fetch-and-read-first
before assuming the title reflects the content, same as any other spot-check.

## Suggested next step

Continue in small batches (3-4 videos), same pipeline as the 2026-08-19 session:
verify unprocessed against the CSV → fetch serialized with real spacing → extract
(applying the new-build-focus scoping rule above) → integrate into the intermediate
store → wiki-route the same session → CSV log → archive transcripts → branch → commit →
push → merge to `main` → delete branch. Update the table above (move rows from
"remaining" to "already processed") as each batch completes, so this file stays the
single source of truth for a fresh session picking this up.
