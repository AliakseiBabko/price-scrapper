# Maria Shevrina / SMBUREAU — Channel Processing Plan (started 2026-08-30)

**Channel**: https://www.youtube.com/@shevrinamaria/videos
**Purpose of this file**: single source of truth for processing this channel across sessions. Read this first when resuming — don't re-derive the video list or clustering from scratch.

**Context**: requested directly by the user on 2026-08-30, immediately after the colour-combination batch. Not from the standing `youtube_channel_queue.md` list — a new channel, added to that queue's Group B when this plan was created.

## Channel facts

- **37 videos, all `fresh`** — preflight run 2026-08-30 light mode, manifest `_Inbox/planning/preflight_20260830T190503Z.json`. No prior contact with this channel anywhere in the vault (checked by name and by video ID).
- **SMBUREAU** is an interior-design studio; Maria Shevrina is the presenter. The channel's centre of gravity is **minimalism** specifically — it recurs in a large share of titles, and several videos are explicitly about distinguishing minimalism from adjacent styles (scandi, japandi, MUJI).
- **Region: unresolved so far.** No city in the channel metadata. The studio exhibits at BEST INTERIOR FESTIVAL (a Russian design event) and at Design Shanghai. To be resolved per-source at level 1 (spoken/written in the content itself), per the standing rule.
- **⚠️ Titles are auto-translated to English by YouTube for roughly half the catalogue** — the spoken audio is Russian. This is exactly the case the language rule was written for: **fetch with `--languages ru`** rather than the default `ru,en`, since this channel's videos may carry manual English subtitle tracks that the fetcher would otherwise prefer over the Russian auto-track (the failure mode hit on 2026-08-30 with SHELNAT `jOXPHR9Mpek`).

## Group classification: Group B (design channel, value not assumed)

This is a **pure design/studio channel**, not a construction-technique channel — so it falls under the queue's Group B rules, where a good trial result does **not** automatically license full-scale processing. The trial has to answer the user's own open question: does transcript-based extraction from design content actually produce something reusable?

The encouraging precedent is that the two best design channels found so far (Anuta Vlady, Бюро ARCHWOOD) both cleared the bar decisively, and this channel's title mix leans much more toward the formats that worked for them ("N mistakes," "anti-trends," "how to choose X") than toward the format that didn't (single-apartment showcase tours).

## Title-skim triage — all 37 videos

Classified by the Group B value criteria: favour a problem framed with multiple named solution options, or a named technique with stated reasoning; deprioritise single-project showcase narration and self-promotional content.

### Tier 1 — high priority (problem + named options, or mistakes with reasoning)

| # | Video ID | Title | Likely destination |
|---|---|---|---|
| 1 | `avRNMkNdOBs` | 7 Common Interior Design and Renovation Mistakes | 17_Design, cross-cutting |
| 3 | `z4G-ocStu9o` | Best Interior Design Solutions from Our Completed Projects | 17_Design (if solutions are named/generalised, not a tour) |
| 7 | `QES02ExtmAg` | False anti-trends: rails, hidden doors, shadow plinths — trend or antitrend | 13_Surfaces (рейки → Decorative_Wall_Panels; скрытые двери → Concealed_Door_Considerations); shadow plinth has **no page anywhere in the vault** |
| 9 | `XGI6FS2ZdCc` | 25 АНТИТРЕНДОВ в дизайне интерьера | 17_Design, wide spread |
| 10 | `0WXiKNXPD_0` | ЭСТЕТИЧНЫЕ vs ПРАКТИЧНЫЕ решения | 17_Design — explicit tradeoff framing, the single most promising title on the channel |
| 31 | `b5oeFxmaubI` | White interior design — giving you the perfect white | 17_Design/Neutrals — directly extends the 2026-08-30 colour batch |
| 32 | `Bnuim5NjgCU` | УЖАСНЫЕ РЕШЕНИЯ в минимализме ТОП 10 | 17_Design |
| 34 | `UDrpyZE_V38` | Как РЕАЛЬНО сэкономить на ремонте — считаем деньги, смотрим ведомость | **11_Budget_and_Planning** — the only title on the channel promising real figures and a bill of quantities |
| 37 | `NfHyCfo1J4w` | Apartment Lighting — Mistakes | 12_Engineering/Lighting_Design |
| 22 | `9h2tAnm6rqA` | How to Design a Small Apartment | 17_Design / 06_Small_Bedroom |
| 24 | `TUVsZ1Xx1aQ` | Плохие решения в ремонте — ошибки в ремонте | 17_Design / cross-cutting |
| 16 | `6y3UiXx9NQI` | Kitchen design in modern interiors: mistakes | 03_Kitchen |
| 15 | `haM4H-b-bZM` | Which tiles to choose for a bathroom — trends and timeless types | 07_Bathroom / 13_Surfaces |
| 33 | `KI2GvB0jzHs` | PODCAST 01 — kitchen design, which countertop, how to choose a colour | 03_Kitchen + 17_Design |

### Tier 2 — medium priority (furniture selection, room-specific, style differentiation)

| # | Video ID | Title | Note |
|---|---|---|---|
| 11 | `GcTaKRQ3QC0` | How to Choose a Sofa | 14_Furniture has **no sofa page** — a real gap |
| 14 | `rRQ05JAoLtk` | How to Choose Dining and Coffee Tables | 14_Furniture gap |
| 25 | `ccZBjb5qIQA` | Стулья для кухни — как выбрать стул в столовую зону | 14_Furniture gap |
| 21 | `HImsHPnSh-c` | Minimalist Bathroom Design: Unconventional Solutions | 07_Bathroom |
| 26 | `nYvqqkNeS4k` | Minimalist Bedroom Design — lighting, accent wall | 06_Small_Bedroom / 17_Design |
| 30 | `MOXm91CE-QQ` | How to think through the HALLWAY in minimalism | 02_Hallway |
| 19 | `k1YBZzIMAgw` | Дизайн в стиле MUJI — отличия от сканди, джапанди и минимализма | Style-differentiation; useful vocabulary, low actionability |
| 28 | `Vv1oLfRd7rM` | Anti-trends 2023 + what to replace them with | ⚠️ **script-reuse risk** against #7 and #9 — check before processing |
| 23 | `AFBu0Uv-47U` | Плохой дизайнер — как дизайнеры обманывают заказчиков | Contractor/designer vetting → 11_Budget_and_Planning, not 16_Legal |
| 18 | `dSm7M6oGFis` | Interior Design Mistakes — reviewing subscriber interiors | Subscriber-critique format; **this format was the most substantive on Anuta Vlady's channel**, so worth a real look despite looking like a reaction video |
| 20 | `A5G04uPvzL0` | Разбор интерьера подписчицы | same format |
| 29 | `p5lXLETWI5s` | Разбор интерьера подписчицы — минимализм | same format |

### Tier 3 — low priority / likely filter out

| # | Video ID | Title | Reason |
|---|---|---|---|
| 36 | `Dz_n3257JFQ` | TRENDS in interior 2023 | Dated trend listicle; the 2026-08-30 colour batch already showed this format yields little durable content |
| 4 | `C7j7NSwlJVk` | Review of a completed 75 m² minimalist interior | Single-project showcase — the exact Group B "low value" category |
| 6 | `yyVKaoD-ag4` | Review of a minimalist apartment interior and our best solutions | Single-project showcase |
| 17 | `FeS2eypPmX4` | Классные решения на примере нашего проекта | Single-project showcase |
| 35 | `d7xxUkVzAlA` | Обзор ремонта в стиле минимализм | Single-project showcase |
| 5 | `f3T2XC0lcjs` | BIF2025 exhibition, our studio's stand | Self-promotional event coverage |
| 8 | `Yi_ONPfxSUs` | BEST INTERIOR FESTIVAL 2024, SMBUREAU stand | Self-promotional event coverage |
| 12 | `F-rn8udbmco` | Design Shanghai exhibition | Event coverage; possible trend observations, low density |
| 2 | `WfJpgwStO1s` | Misconceptions about the interior design profession | Career content, out of scope |
| 13 | `fN8wJAEz2zM` | How to become an interior designer / choosing a college | Career content, out of scope |
| 27 | `GvjT1mNRaiQ` | How to become an interior designer — myths, skills | Career content, out of scope |

**Triage totals**: 14 Tier 1, 12 Tier 2, 11 Tier 3. Only 11 of 37 look like clear non-starters, which is a better ratio than the Group B expectation.

## Round 1 (trial) — 8 videos

The user named four (`avRNMkNdOBs`, `z4G-ocStu9o`, `QES02ExtmAg`, `XGI6FS2ZdCc`); four more were added from Tier 1 to spread the trial across **different destination pages**, so the trial tests routing breadth as well as content quality:

| Video ID | Why in the trial |
|---|---|
| `avRNMkNdOBs` | user-named |
| `z4G-ocStu9o` | user-named; also tests whether "solutions from our projects" is generalised technique or a disguised showcase |
| `QES02ExtmAg` | user-named; three specifically named elements with verdicts, routes to existing 13_Surfaces pages |
| `XGI6FS2ZdCc` | user-named; the widest-spread title on the channel |
| `0WXiKNXPD_0` | aesthetic-vs-practical tradeoff framing — the format the user most wants |
| `b5oeFxmaubI` | tests whether this channel adds to the colour work done the same day |
| `UDrpyZE_V38` | the only pricing-bearing title; tests region/currency resolution for this channel |
| `NfHyCfo1J4w` | tests routing into 12_Engineering (Lighting_Design) rather than 17_Design |

Fetched serialised at 75 s spacing with `--languages ru` forced.

### Round 1 results — completed 2026-08-30

**8 of 8 processed. None skipped. Round 1 yield: 8 videos, 72 new facts, 9.0 new facts per processed video** — well above this project's 1.0 stop-and-ask floor, and comparable to the best Group A construction channels (Petrishin-Stroi's strong rounds ran 7.6–11.1).

All 8 fetched cleanly in Russian at 75 s spacing with `--languages ru` forced; no rate-limit, no missing captions. Metadata confirmed **none of these videos has a manual English subtitle track**, so the forced-`ru` precaution was cheap insurance rather than strictly necessary here — but the auto-translated titles mean it should stay the default on this channel.

| Video | Yield | Verdict |
|---|---|---|
| `avRNMkNdOBs` | 7 | FULL — seven mistakes with mechanisms, incl. a controlled on-site paint experiment |
| `z4G-ocStu9o` | 10 | FULL — ten named reusable construction details, **not** the showcase its title suggested |
| `QES02ExtmAg` | 5 | PARTIAL — much of the runtime is reassurance; the real items kept |
| `XGI6FS2ZdCc` | 9 | PARTIAL — 25 items, restricted to those with a mechanism or spec |
| `0WXiKNXPD_0` | 12 | FULL — client-intake instrument, a second documented experiment, shadow-plinth numbers |
| `b5oeFxmaubI` | 7 | FULL — the no-perfect-white position, RAL-vs-manufacturer decks |
| `UDrpyZE_V38` | 14 | FULL — bill-of-quantities cost structure, the richest source in the round |
| `NfHyCfo1J4w` | 8 | FULL — densest lighting addition this vault has had |

**Routed to eleven pages across six folders** — `11_Budget_and_Planning` (Budgeting_Guide §5a, Numeric_Data), `12_Engineering_and_Systems` (Lighting_Design, AC_Key_Concepts_and_Placement), `13_Surfaces_and_Finishes` (Walls_and_Paint, Flooring_Guide, Ceilings_Guide, Door_Swing_Direction, Doors_Trim_Cost_and_Buying, Concealed_Door_Considerations), `07_Bathroom` (four pages), `03_Kitchen`, and `17_Design_and_Ergonomics` (five pages).

**⚠️ Group B verdict: clear pass, and for a reason worth recording.** This channel breaks the Group B pattern — its content is largely *technical* rather than taste commentary. An AC-enclosure failure mechanism, LED voltage drop over a 5 m reel, laminate expansion behaviour, a cost breakdown from real bills of quantities, and two documented physical experiments are not "design channel" content by this project's previous classification. **It is arguably a Group A channel that happens to be presented by a designer.**

**Two things the trial caught that are worth carrying forward:**

1. **The title-skim heuristic mis-sorted `z4G-ocStu9o`.** "Best Solutions from Our Completed Projects" is exactly the shape the Group B criteria flag as a probable disguised showcase; it turned out to be the second-richest source in the round. Treat the title-skim as a narrowing step, never a verdict — which is what the skill already says, now with a concrete instance behind it.
2. **Real script and topic overlap exists within the channel.** `QES02ExtmAg` and `XGI6FS2ZdCc` are an announced pair and repeat the marble-format rule; `0WXiKNXPD_0` repeats the plastic-trim and corner-bead material from both. Each counted once. **This is the main argument for not processing all remaining Tier 1+2 videos indiscriminately.**

**One disagreement recorded rather than adopted**: her blanket rejection of stretch ceilings rests partly on the claim that the flood-protection argument fails — which is contradicted by a documented real flood-containment incident already on `Ceilings_Guide.md` from RemProektMD. Written up as a Perspectives block with her flood claim explicitly marked as the weaker half, and her sequencing-damage point (a fit-out trade holing an already-installed membrane) marked as the genuinely new contribution.

## Open questions for the user

1. ~~**Group B verdict**~~ — **ANSWERED 2026-08-30: clear pass at 9.0 facts/video, and the channel is arguably mis-classified as Group B at all** (see Round 1 results). The open question is now not *whether* to continue but *how much* of the remaining 29 videos to take.
2. **Anti-trend cluster** — **the two processed do repeat each other materially** (announced as a pair; the marble-format rule appears in both). **Recommend skipping `Vv1oLfRd7rM`** ("Anti-trends 2023") entirely: it is the oldest of the three and a third pass over the same ground is unlikely to clear the bar.
3. **Furniture-selection cluster** (`GcTaKRQ3QC0` sofa, `rRQ05JAoLtk` tables, `ccZBjb5qIQA` chairs) targets a real gap — `14_Furniture` currently has only wardrobe/storage pages, nothing on loose furniture selection. If Round 1 clears the bar, this cluster is the strongest argument for a Round 2.

## Round 2 — completed 2026-08-30

**8 of 8 processed, none skipped. Round 2 yield: 8 videos, 78 new facts, 9.75 per video** — slightly above Round 1's 9.0, so no decay across two rounds. All fetched cleanly at 75 s spacing with `--languages ru`, no rate-limit.

| Video | Yield | Verdict |
|---|---|---|
| `KI2GvB0jzHs` podcast | 12 | FULL — richest of the round; procurement constraints a polished explainer never mentions |
| `6y3UiXx9NQI` kitchen mistakes | 13 | FULL — most numerically dense kitchen source in the vault; figures cross-check |
| `haM4H-b-bZM` bathroom tile | 11 | FULL — causes behind the "dirty tile" effect, plus the slab-logistics cost |
| `MOXm91CE-QQ` hallway | 10 | FULL — raised-wardrobe technique, entrance-door ladder, manifold placement |
| `rRQ05JAoLtk` tables | 9 | FULL — the dimensional core of the furniture cluster |
| `dSm7M6oGFis` subscriber critique | 9 | FULL — **format probe passed** |
| `GcTaKRQ3QC0` sofa | 8 | PARTIAL — brand survey; principles extracted, SKU verdicts not |
| `ccZBjb5qIQA` chairs | 6 | PARTIAL — same; its value is sharpening the leg rule |

**Structural outcome: this vault's first loose-furniture pages.** The three furniture videos crossed the 3-source threshold and produced `14_Furniture/Seating_and_Tables.md` plus `analysis/Loose_Furniture_Selection_Principles.md`, `Seating_Selection.md` and `Table_Types_and_Dimensions.md`, with their own Source Notes and Change Log. `Furniture_Index.md` had explicitly anticipated this gap and is now updated. **All three sources are the same channel, so the pages carry a prominent `single-account` caveat** rather than reading as settled practice.

**Routed to fifteen pages across nine folders.**

### What Round 2 confirmed and what it added

- **Round 1's разнотон finding is now closed.** Round 1 proved walls and fronts at one code don't match; the podcast supplies the remedy (real MDF-in-enamel front samples, **~3,000 RUB ≈ $50** each) and the sequencing rule — **pick the stone slab first, then eliminate the enamel shades that don't suit it**, because stone is fixed and enamel is tintable.
- **A third documented experiment**: an overhang *with a drip groove* still fails to keep water off the fronts, extending Round 1's plain-overhang test. This studio now has three physical experiments on record here.
- **The subscriber-critique format probe passed** — every item was a named problem with a specific corrective and a stated reason. **`A5G04uPvzL0` and `p5lXLETWI5s` are now worth processing.**
- **Two Russian-law claims kept out of `16_Legal_and_Regulations/`** (shaft-vented hoods; entrance-zone water supply subject to БТИ designation), per that folder's Belarus-only rule — routed to technical pages with the jurisdiction flagged and the Belarus position marked open.

### The honest caveat on the furniture cluster

**Three of the eight were brand-by-brand surveys of Russian furniture SKUs**, and roughly half of each runtime is per-model aesthetic verdicts. **None of those were extracted** — taste, market-specific, time-decaying, failing this project's value criteria. Only the reasoning underneath was kept. So ~55 minutes of furniture video produced comparatively compact pages, and the yield figures for those three (8, 9, 6) are lower than the rest of the round for that reason. **This is the weakest content type this channel produces**, and further brand surveys should be deprioritised in favour of the mistakes/podcast/critique formats.

## Recommended Round 3 (awaiting user go-ahead)

Ordered by expected yield, now informed by two rounds of evidence about which formats actually pay:

1. **`A5G04uPvzL0` and `p5lXLETWI5s`** — the two remaining subscriber-critique videos. The format probe passed, and this format consistently produces named-problem/named-corrective content.
2. **Any further "podcast" episodes** — `KI2GvB0jzHs` was episode 01 and the richest single source across both rounds. She said a second would follow within a week, so more exist beyond the 37-video listing captured on 2026-08-30. **Worth re-running preflight on the channel** to pick up anything published since.
3. **`TUVsZ1Xx1aQ`** (плохие решения в ремонте) and **`Bnuim5NjgCU`** (ужасные решения в минимализме) — the mistakes format, which has been the most reliable across both rounds.
4. **`9h2tAnm6rqA`** (small apartment) and **`HImsHPnSh-c`** (minimalist bathroom, unconventional solutions) — room-specific, both feed thin pages.
5. **`AFBu0Uv-47U`** (плохой дизайнер / how designers deceive clients) — contractor-vetting content for `11_Budget_and_Planning`.

**Deprioritised after two rounds**: `Vv1oLfRd7rM` (anti-trend overlap, unchanged), `Dz_n3257JFQ` (dated trends), `k1YBZzIMAgw` (style differentiation, low actionability), the four single-project showcases, the three exhibition videos and the three career videos. **21 of 37 processed or deliberately excluded; 16 remain, of which about 5 look genuinely worthwhile.**

---

## Superseded — the Round 2 recommendation as originally scoped

Ordered by expected yield, weighted toward gaps this vault actually has and away from the overlap the trial exposed:

1. **`GcTaKRQ3QC0` (sofa), `rRQ05JAoLtk` (dining and coffee tables), `ccZBjb5qIQA` (kitchen chairs)** — the furniture-selection cluster. `14_Furniture` holds only wardrobe and storage pages; there is nothing on loose furniture selection anywhere in the vault. The strongest argument for a Round 2.
2. **`KI2GvB0jzHs` (podcast: kitchen, countertop choice, colour choice)** and **`6y3UiXx9NQI` (kitchen mistakes)** — `03_Kitchen` is still a single-file page, and the worktop-overhang material from the trial suggests this channel has more kitchen substance.
3. **`haM4H-b-bZM` (bathroom tile: trends vs. timeless types)** — follows directly from the format rules already extracted.
4. **`9h2tAnm6rqA` (small apartment)** and **`MOXm91CE-QQ` (hallway in minimalism)** — room-specific, and `02_Hallway` is thin.
5. **`dSm7M6oGFis` / `A5G04uPvzL0` / `p5lXLETWI5s`** — the subscriber-critique format, which was the most substantive format on Anuta Vlady's channel. Worth one sample before committing to all three.

**Deprioritised**: `Vv1oLfRd7rM` (anti-trend overlap), `Dz_n3257JFQ` (dated trends), the four single-project showcases, the three exhibition videos and the three career videos — 11 of 37 remain clear non-starters, unchanged from the initial triage.
