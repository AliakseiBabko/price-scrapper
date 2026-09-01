# YouTube Channel Queue — Future Intake Work

Master list of channels to process, across three categories with different evaluation approaches. Created 2026-08-24 per explicit user request, as a durable plan to read before starting new channel work in any future session.

## Currently active (Group A channels already underway)

- **Zemskov/Zemstandart** — CLOSED. All 5 categories of the 372-video manifest complete as of 2026-08-19 (see [[project_zemskov_channel_triage_complete_20260819]] memory). Not a source of new work unless the user explicitly reopens it.
- **Konstantin Kruglov/Ontario** — PAUSED, rate-limited. Rounds 1–4 done, Round 5 halted 2/7 in (see `kruglov_ontario_full_channel_plan_20260824.md`). Round 4 yield 8.14 facts/video. **Do not retry yet** — see IP-wide-block correction below; paused 2026-08-24, same day as this queue entry.
- **Pavel Sidorik** — PAUSED, rate-limited. Rounds 1–5 done, Round 6 halted 2/7 in (see `pavel_sidorik_channel_plan_20260824.md`). Round 5 yield 13.0 facts/video (highest yet). Through episode #27 of 42 in its "New Building A-to-Z" series; the 36-episode "Khrushchevka" series and large standalone/tool-review pools still ahead. **Do not retry yet** — paused 2026-08-24, same day.
- **TimRemont** — Originally paused, rate-limited on its very first fetch attempt (see `timremont_channel_plan_20260824.md`); that was the incident revealing the block is IP-wide, not per-channel. **Update 2026-08-25**: a targeted Small Bedroom batch (3 TimRemont videos, part of a cross-channel 8-video dispatch, see `00_Master/processed_sources.csv` rows `run_20260825_gWAOrislxFY`, `run_20260825_U95vMOOhKH8`, `run_20260825_CVqedVQlZZU`) fetched **all 3 TimRemont videos cleanly, zero rate-limit signatures** — this channel is confirmed fetchable now, not still blocked. Low-to-medium promotional ratio, genuine real-project technique/case-study content (own-apartment full renovation, walk-in-closet/zoning case, frameless soundproofing install) — clears the value bar on this small sample; a full trial/round dispatch per the standard Group A pipeline is still owed before treating the whole channel as vetted.
- **Petrishin-Stroi** — ACTIVE, but ⚠️ stop-and-ask signal triggered at Round 13. Rounds 1-13 complete 2026-08-24 (93 videos fetched/extracted + 8 genuinely skipped for no captions, 811 new facts). Yields: 8.6, 9.5, 8.9, 11.1, 8.75, 9.5, 7.75, 7.6, 9.5, 9.6, 10.9, 7.2, **1.5** facts/video — Round 13 dropped 79% from Round 12's 7.2, a clear >50%-drop stop-and-ask trigger, and near the 1.0 absolute floor. **Explicitly flagged, not a mystery**: Round 13 was deliberately composed of higher-thinness-risk content (3 more "ЖК Виноградный" episodic-series episodes, 2 third-party НТВ short-format clips, 1 third-party Москва 24 human-interest report, 2 real kitchen case studies that turned out to have no captions), not a random sample of the channel's remaining pool — the channel's own higher-confidence formats (named-technique tutorials, cost-case studies, "Как выглядит качественная X"/"Как убить X"/"СРАВНЕНИЕ!" series) consistently yielded 7.6-11.1 facts/video across Rounds 1-11 and remain untested for exhaustion. **Explicit verdict recorded on the Vinogradny series** (4 of ~13 episodes now spot-checked across Rounds 12-13, average yield 4.0/episode, 3 of 4 individually 1-3/episode): deprioritize the remaining ~9 episodes — not worth a dedicated future round, format's own short/informal 2016-17 style caps yield regardless of trade sampled. **Third-party TV-segment cluster** (Москва 24, НТВ) also now characterized as low-to-thin yield across 5 total clips sampled (Rounds 12+13) — deprioritize remaining clips of this type if any exist on the manifest. See `petrishin_stroi_channel_plan_20260824.md` for full Round 13 detail. **Recommend checking in with the user before dispatching Round 14** — a round drawn from the channel's already-confirmed high-yield formats would likely return to the 7-11 facts/video range, but this is a recommendation, not an automatic go-ahead per the stop-and-ask rule. 240 of 341 videos still remain (341 − 101 manifest entries touched across Rounds 1-13, counting the 8 skips).
- **RemProektMD** — PAUSED, single-video rate-limit. Rounds 1-2 complete/partial 2026-08-24 (10 videos archived, 1 skipped for no-captions, yield 7.0 then 5.2 facts/video — within tolerance, no stop-and-ask trigger). See `remproektmd_channel_plan_20260824.md`. **Round 2's 7th and final fetch (`C2vRkbcEs7U`, electrical panel) hit a rate-limit** — stopped immediately, no CSV row written, left pending for a later retry. This looks like an isolated single-video incident (6 clean fetches immediately before it, in a session with dozens of other clean fetches since the earlier IP-wide block cleared), not a repeat of that IP-wide throttle — but per the channel-switching protocol, don't immediately retry; pick up Petrishin-Stroi instead and retry `C2vRkbcEs7U` after a real cooldown. **Scope flag, still worth the user's attention**: this is a Moldova (Chisinau) company channel, a new country/currency for this project — no MDL/EUR rate support in `currency_converter.py`; prices actually encountered so far were either EUR (Round 1, unconverted) or stated directly in USD by the source (Round 2, no conversion needed). Technique content is unaffected and has already produced a genuine cross-channel corroboration (polypropylene pipe joint defect). Still has a heavy repetitive "yearly trend showcase" cluster (2023/24/25/26 versions of similar content) worth a light dedup-aware pass in a future round rather than full individual processing.

**Block-lifted finding (2026-08-24): the IP-wide rate-limit has cleared.** Petrishin-Stroi's Round 1 trial fetched all 5 videos cleanly with zero rate-limit signatures (video 1 succeeded on the very first attempt). This means Kruglov/Ontario, Pavel Sidorik, and TimRemont are now all fetchable again in a future session — a real cooldown has now genuinely passed since their 2026-08-24 halt, not just wall-clock time. Still fetch serialized/spaced per the standing rule (this finding doesn't relax that), and still watch for a fresh block signature — it could recur.

**Per explicit user instruction (2026-08-24): keep exactly two Group A channels active at a time.** With the block confirmed lifted, Petrishin-Stroi is the first active channel going forward; remproektmd (next in queue) is the natural second pick once picked up — see the rate-limit protocol below for how/when to rotate channels, and its IP-wide-block correction in particular.

## Group A — Construction/Renovation Technique Channels (same pipeline as Kruglov/Sidorik)

Process each like Kruglov/Sidorik: `preflight_playlist.py` → title-skim triage → small trial batch (2–5 videos, report substance/promotion ratio) → full-scale rounds only if it clears the value bar, chunked 5–8 videos per dispatch. None of these have been preflighted yet — do that first when picking one up, don't assume value.

Queue (order as provided by the user, not yet re-prioritized):

1. https://www.youtube.com/@timremont/videos
2. https://www.youtube.com/@Petrishin-Stroi/videos
3. https://www.youtube.com/@remproektmd/videos
4. https://www.youtube.com/@VitionRu/videos
5. https://www.youtube.com/@i.ippoitov/videos
6. https://www.youtube.com/@Boyarin_pro/videos
7. https://www.youtube.com/@DOMEO-ru/videos
8. https://www.youtube.com/@krnkrptn/videos
9. https://www.youtube.com/@axenovservice/videos
10. https://www.youtube.com/@REMCRAFT/videos
11. https://www.youtube.com/@remontkvpro/videos
12. **`@sbk.remont`** ("ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ", Vladimir Amelchenko, business/premium-segment turnkey renovation, St. Petersburg, 94 videos) — added 2026-08-28 per explicit user request. `preflight_playlist.py` run (93 fresh, 1 duplicate, light mode). **3-video title-skim trial complete, 3-for-3 clean pass**: quartz-vinyl terminology/selection (`KXmidtaUNxI`), concealed-mount-door schedule/cost/swing-angle consequences (`ukZBqIlz8e0`, nuances the existing Ontario door note independently), 11 business/premium planning-process points (`33b61qeO_XY`, independently corroborates the ARCHWOOD author-supervision-vs-technical-supervision distinction). Low promotional ratio all 3. **Recommend a full preflight → round pipeline for this channel — awaiting user go-ahead before Round 1.**

When a Group A channel currently active (Kruglov or Sidorik) is fully exhausted (all rounds/clusters done) or abandoned (fails its own trial), pull the next channel from this queue, top to bottom, to keep two active.

## Group B — Pure Design / Room-Tour Channels (value UNCONFIRMED — trial-only)

Per explicit user discussion (2026-08-24): these are design-focused (color scheme, room tours, furniture/layout arrangement, "what solution works for this specific room/wall") rather than construction technique. **The user is explicitly unsure whether transcript-based extraction from this content type is useful at all** — unlike Group A, do not assume a good trial-batch result means "proceed to full-scale processing" the way it did for Kruglov/Sidorik. Treat each trial's verdict as a real open question to report back on, not a formality.

**What a trial batch (2–4 videos per channel) should specifically test for:**

- **Genuinely reusable, per the user's own framing**: a specific problem framed with multiple named solution options (e.g. "10 ways to treat a statement/accent wall," "3 layout options for a small bedroom," "what to do with an awkward corner") — extract normally, this is exactly the kind of content the user wants surfaced.
- **Genuinely reusable**: a real named technique or stated reasoning behind a choice (why a specific furniture arrangement works for a given room shape/size/light condition) — extract normally.
- **Low value, don't force extraction**: pure narrated description of one specific finished apartment's look with no generalizable "why" and no alternative comparison — matches this project's existing advertising/promotional-content filter reasoning (a single showcased result isn't a technique).
- **Apply the existing advertising filter explicitly**: a furniture retailer's own channel (`divanru`, `pride-mebel` below) is a brand-showcase context by default — check for tier-steering (pushing their own catalog) vs. genuine general design reasoning before extracting.

**Routing for anything that clears the bar**: `17_Design_and_Ergonomics/` (general technique — Functional Zoning & Furniture Arrangement, Color Palette & Material Direction, Whole-Apartment Coherence are all still placeholders and are the most likely destinations) and/or a room folder's own future "Design & Zoning" page once that room has enough room-specific sources (per that folder's per-room-integration note) — not `11_Budget_and_Planning`.

Channels (not yet preflighted):

1. https://www.youtube.com/@divanru/videos — furniture retailer, check promotional framing first
2. https://www.youtube.com/@dsgninterior/videos
3. https://www.youtube.com/@OlgaKulekinaDesign/videos
4. https://www.youtube.com/@YourInteriorDes/videos
5. https://www.youtube.com/@kakjivutdrugie/videos
6. https://www.youtube.com/@pride-mebel/videos — furniture retailer, check promotional framing first
7. https://www.youtube.com/@AnnaSheveleva/videos
8. https://www.youtube.com/@Geometrium/videos

**Recommended first step when picking this group up**: run one small trial (2-4 videos) across a couple of these channels, report the honest substance-to-promotion ratio and whether real "N options for X problem" content actually shows up, and let the user decide whether to invest further in this group at all — same decision structure as the original Kruglov trial, but with the outcome genuinely open this time.

## Group B addition — Мария Шеврина / SMBUREAU (added and trialled 2026-08-30)

https://www.youtube.com/@shevrinamaria/videos — 37 videos, requested directly by the user, not from the original Group B list.

**Round 1 trial complete: 8 videos, 8/8 pass, yield 9.0 facts/video.** Full triage and results in `shevrina_smbureau_channel_plan_20260830.md`.

**⚠️ This channel breaks the Group B assumption and should probably be reclassified.** The premise of Group B is that design/room-tour channels may not yield transcript-extractable knowledge at all. This one yields *technical* content — an AC-enclosure failure mechanism, LED voltage drop, laminate expansion behaviour, a renovation cost structure from real bills of quantities, two documented physical experiments — and routed to eleven pages across six folders including `11_Budget_and_Planning`, `12_Engineering_and_Systems` and `13_Surfaces_and_Finishes`. **Treat it as a Group A channel presented by a designer** and process it with the normal Group A round pipeline.

**Rounds 1–3 complete (24 of 37 videos): yields 9.0, 9.75 and 11.0 facts/video — no decay across three rounds.** ⚠️ **Recommended stopping point.** Every format that produces mechanism-and-number content has been mined; the 13 remaining videos are showcase, exhibition and career content plus one style explainer, and a Round 4 would likely fall below the 1.0 facts/video floor. **Better to re-run preflight in a few months for new podcast episodes** — that format was the single richest across all three rounds — than to work down this tail. Round 3 detail and a short Round-4 shortlist are in the plan file.

*(Superseded note: )* Round 2 created this vault's first loose-furniture pages and closed the Round 1 разнотон finding. **Round 3 is scoped in the plan file, awaiting go-ahead**; 16 videos remain, of which about 5 look genuinely worthwhile.

**Format matters more than topic on this channel** — two rounds of evidence: the **podcast** (live project commentary), **mistakes** and **subscriber-critique** formats consistently yield mechanism-and-number content, while **brand-survey** videos are half per-SKU aesthetic verdict and yield noticeably less. Prioritise by format, not by subject.

## Group C — CAD / 2D Floor-Plan Channel (unique category, own evaluation)

https://www.youtube.com/@RemPlanner/videos

Per explicit user description: mixed content — CAD software tutorials/advice plus actual 2D floor plans and facades for real construction/renovation projects. **Value hypothesis (per user)**: the videos walking through an actual apartment's 2D plan could teach how to represent a real layout as a 2D/CAD drawing from real measurements — a third, distinct use case, not "renovation technique" (Group A) and not "design guidance" (Group B).

**This does not cleanly fit the existing `renovation-knowledge-intake` taxonomy** (checked 2026-08-24: neither `.agents/skills/homestyler-cad-to-revit/` nor `.agents/skills/residential-bim-geometry-rules/` are about extracting knowledge from external video sources — both are this project's own CAD/BIM production workflows, a different concern). Before processing this channel, do a small scoping pass: title-skim to separate pure software-tutorial videos (lower priority, generic CAD instruction) from videos that walk through an actual apartment's 2D plan/facade (higher priority, the ones with the hypothesized teaching value), and decide explicitly where extracted content should live (a new dedicated store/page, or an existing one) before running a trial batch — don't force it into the renovation intake pipeline's existing taxonomy buckets by default.

## Group E — Channels discovered via topic-scoped search (added 2026-08-25)

Not from a pre-built list like Groups A-C — surfaced by targeted web searches for specific under-served topics (Entrance/Hallway, Kids Room, Living/Dining zoning) on 2026-08-25, per explicit user request to fill those gaps. Each channel below was hit once or a few times as part of that topic search, not deliberately trialed the way Groups A/B channels are — verdicts here are provisional, based on 1-4 videos each, not a full trial batch. **Channel identity was frequently misattributed from search-snippet context and had to be corrected via `yt-dlp` metadata** — a recurring finding this session; don't trust a search result's apparent channel without verifying.

**Substantive (worth a deliberate future trial batch on each)**:
- **Sergey Kodolov** (`youtube.com/kodolov` / channel ID `UCSRNLMsKZTe2Tm3vQ9HrxNA`) — broad renovation/design/construction channel (electrical, plumbing, ventilation, flooring, painting, bathroom, kitchen, kids room), not just design-tour content. 3 videos processed (kids-room combination, design-process methodology, Dubai apartment review), all substantive, real reasoning throughout. **Recommend proposing as a new Group A construction-channel candidate** — broad enough to warrant the full preflight → trial → round pipeline, not just opportunistic single-video mining.
- **Anuta Vlady** — individual designer/course-educator, does subscriber-apartment-makeover-critique videos (real layouts, real reasoning, "why this arrangement for this room"). **6 of 6 videos processed today were substantive** (hallway design, entryway declutter, 3x kitchen-living/bedroom-study makeovers, one partial) — the single most consistently useful channel found this session. Worth deliberately trialing more of her catalog.
- **Бюро ARCHWOOD** (Marina Izmailova's design bureau, `@archwooddesign`) — family-interior-focused design bureau, layout analysis by an architect. 3 of 3 videos processed were substantive (90m² family-with-2-kids layout with 5 rejected variants, dark-room fix mechanism, texture/pattern framework) — filled two previously-empty `17_Design_and_Ergonomics/` placeholder pages.
- **RemPlanner** (`@RemPlanner`) — same channel as Group C above (confirmed same identity); its one processed video (`OfqkRAZUfe0`, kids-room 15-year forward planning) was substantive, but most of its other catalog is CAD-software tutorials per Group C's own note — don't expect a high hit rate without the scoping pass Group C already calls for.
- Single-video positive data points, not yet re-tested: **Interior Nalitso** (real 52m² old-fund replanning case), **Olga Kachanova** (kitchen-in-hallway zoning case + a kids-room source, strong region evidence), **Omikor/Elena** (kitchen-living zoning rules), **Iolanta Fedotova** (living+bedroom zoning rules), **13DS/Olesya** (10 ranked partition methods), **Ekaterina Popova** (worked bedroom-living zoning example), **500LUX**/guest **Marina Zvereva** (living-room layout rules), **LightLab/Artem Voronov** (kitchen-living lighting technique), **Karen Karapetyan** (5-layout subscriber critique incl. RU permitting rules), **Sergey Tregubov/РАЗРУЛИ МОЙ ХАУС** (real kids-room pricing).

**Thin/low-value — deprioritize**:
- **INMYROOM TV** — entryway room-tour compilations, high ad-read density, mostly showcase; 3 videos only yielded partial extractions. Mine opportunistically at most.
- **Fenix Interior** — turnkey design-build studio, medium promotional/tier-steering ratio.
- **Studio57/Alexander Kasperovich**, **Sergey Gusev/ПРО ДВЕРИ** (door/partition retailer), **Дела домашние** (content aggregator, not a specialist), **Mirlay Glass** (partition installer, thin #shorts), **the soundproofing/flooring channel behind `pd_HXj0jT9g`** featuring installer **DELI** — all high-promotional or thin on inspection.

## Rate-limit channel-switching protocol (added 2026-08-24, per explicit user instruction)

When a fetch attempt returns a rate-limit/IP-block signature — HTTP 429, "Sign in to confirm you're not a bot," `youtube-transcript-fetch` exit code 2, or any error interpretable as upstream throttling — **do not simply wait idle for a cooldown.** Pause the current channel's round (per the existing circuit-breaker rule: no retry, no false `skipped` row for the blocked video) and switch to the *other* currently-active Group A channel to keep making progress. If only one Group A channel is active when this happens, pull the next unstarted channel from Group A's queue above to bring the active count back to two. Resume a paused channel later after a real cooldown has passed (as already practiced with Kruglov's Round 4 — a bounded single retry, not repeated hammering).

This is specifically a Group A protocol — Group B/C channels stay trial-only until their value is separately confirmed, so don't rotate one of them in as a rate-limit substitute without the user's go-ahead.

**Correction, confirmed 2026-08-24**: this protocol assumes a rate-limit is channel-specific, but a real incident the same day showed otherwise — Kruglov/Ontario, Pavel Sidorik, *and* a freshly-rotated-in TimRemont all hit the identical block signature (`youtube-transcript-api` IP-block message + `yt-dlp` "Sign in to confirm you're not a bot") within about 15 minutes of each other, the third one on its very first fetch attempt before any content was even seen. This points to a **session/IP-wide throttle**, not a per-channel one. **When a second channel switch in short succession also hits the same block signature, stop rotating in a third — that's the signal the block is IP-wide, and rotating further channels just burns dispatches into the same wall.** At that point, actually pause all YouTube fetching for a real cooldown (longer than the single-channel bounded-retry cooldown - this is a stronger signal) before retrying any of the blocked channels, rather than continuing to search for an unaffected channel.

## Progress Log

- 2026-08-24 — Queue created per explicit user request: 11 Group A channels, 8 Group B channels, 1 Group C channel, plus the rate-limit channel-switching protocol formalized (already practiced informally when Kruglov's Round 4 was rate-limited and the session switched to starting Pavel Sidorik). No channel in this queue has been preflighted yet.
- 2026-08-28 — Added `@sbk.remont` to Group A per explicit user request, ran `preflight_playlist.py` (93 fresh/1 duplicate) and a 3-video trial batch — 3-for-3 clean pass, low promotional ratio, real cross-channel corroboration/nuance found. Recommend a full round pipeline; awaiting user go-ahead.
- 2026-08-28 — Rounds 1-7 of `@sbk.remont` complete (56 videos total). Round 7 (8 videos, all fetched cleanly, no rate-limit): 52 new facts, ~6.5/video (up ~10.6% from Round 6's ~5.875) — 7 full extractions, 1 partial (`3GvLuU2x7wU`, overlapped an existing vacation-mode panel note). Two overlap-flagged videos (`dfXZ66EcGQQ`, `pyew_HmvSOE`) checked directly against `AosCvLCh6WA`/`33b61qeO_XY` and confirmed genuinely new mechanisms. Five existing dedicated pages gained new sections directly. See `_Knowledge/store/Change_Log.md` for full detail.

## Group A addition — Надежда Кузина / @kuzinadesign (added and Round 1 complete 2026-08-31)

https://www.youtube.com/@kuzinadesign/videos — 108 videos, requested directly by the user, not from the original Group A/B lists. Full triage and round detail in `kuzina_nadezhda_channel_plan_20260831.md`.

**Classified Group A on arrival, not trialled as Group B.** Two of its videos had already been processed opportunistically on 2026-08-30 (`gEhVxuxtOjc`, `n5ZBqdq0wH8`) with `fact_yield` 6 and 8 and low promotional ratio — the "is this content type useful at all" question Group B exists to answer had therefore already been answered twice. **Same pattern as Шеврина/SMBUREAU: a designer-presented channel that yields technical content.**

**Round 1 complete: 8 dispatched, 7 processed, 1 genuinely skipped for no captions. 137 new facts, yield 19.6 facts/video — the highest first-round yield of any channel in this vault** (against Шеврина 9.0, sbk.remont ~6.5, Petrishin-Stroi 8.6). All seven fetched cleanly in `ru` with **zero rate-limit signatures**.

**⚠️ The finding that should drive Round 2: format beats topic, and it is not close.** Her two recorded lectures/seminars (47 and 78 minutes) yielded 27 and 38 facts; the 6–12 minute single-topic explainers yielded 9–19. **The audience Q&A sections are the densest part of both lectures**, because questions force specific numbers out of her. This restates the Шеврина finding on a second channel — **hunt long-format lectures, seminars and podcasts first.**

**Also worth knowing before Round 2**: she states negative results freely (she searched ГОСТ/СНиП for kitchen outlet positions and found nothing; she declined to solve a 2.70 m bedroom; she abandoned her own podium-bed plan) — **do not mistake her hedges for thin content.** And **ASR quality varies sharply by upload year** — pre-2022 uploads are unpunctuated and heavily mangled, so several numeric passages were deliberately not extracted rather than guessed.

**Round 2 recommended** (awaiting go-ahead; no stop-and-ask trigger fired): the ~12 remaining Cluster 1 videos, prioritising long-format items, including `VBMzas01VRs` so the protruding-corner/irregular-geometry gap logged in `Pending_Wiki_Page_Decisions.md` gets its second source. **Cluster 2, the 19-video «Цвет в интерьере» series, is entirely untouched** but the two already-processed colour videos yielded 6 and 8, below Round 1's average — finish Cluster 1 first.

**⚠️ Region upgrade to an existing Group E entry, from this round**: **500LUX is a Sochi studio** (founder Сергей Реньжин, relocated from Moscow ~2020) — stated by him directly in `9MsEZVjLH2M`, so **level 1**, replacing the provisional/unresolved attribution in the Group E list above.

## Group A addition — Игорь Краснов / @krasnov_design (added and Round 1 complete 2026-09-01)

https://www.youtube.com/@krasnov_design/videos — St. Petersburg turnkey interior design studio ("Студия Краснов," "более 160 реализованных проектов"). Full triage and round detail in `krasnov_design_channel_triage_20260901.md`.

**Classified Group A on arrival, not trialled as Group B** — same pattern as Кузина/@kuzinadesign and Шеврина/SMBUREAU: a designer-presented channel expected to yield technical content, given the precedent those two channels already set.

**Round 1 complete: 8 of 8 dispatched and processed, zero skips. 67 new facts, yield 8.4 facts/video.** Above the 1.0/video floor, no stop-and-ask trigger, but noticeably below Кузина's first-round 19.6 and Шеврина's 9.0 — closer to sbk.remont's ~6.5-8.6 range. All 8 fetched cleanly in `ru` with **zero rate-limit signatures**.

**Densest source: the bathroom-mistakes video (`ThgEv7FWNeE`, 14 facts).** **Weakest: the bedroom-mistakes video (`gGII-GzuDUg`, 5 facts)** — comedic-listicle voice-over format with few hard numbers, honestly flagged as closer to this vault's Group B design-psychology genre than to this round's technical density.

**Round 2 complete: 8 of 8 dispatched and processed, zero skips, zero rate-limit signatures. Raw 71 / net-of-restatement 56 new facts, net yield = 7.0 facts/video** — a real drop from Round 1's 8.4 (though not past the 50%-drop stop-trigger) and Round 2's own raw-vs-net gap (71→56, ~21% discarded to restatement) is the largest measured for this channel so far. **Headline finding: prospect-refuge theory ("теория обзора и укрытия")**, a genuinely new named mechanism this vault did not previously have (`ufKHek_TU30`) — routed prominently to `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md`. Full detail in `krasnov_design_channel_triage_20260901.md`'s Round 2 section.

**Round 3 complete: 8 of 8 dispatched and processed, zero skips, zero rate-limit signatures. Raw 79 / net-of-restatement 66 new facts, net yield = 8.25 facts/video** — yield recovered from Round 2's 7.0 back toward Round 1's 8.4, confirming Round 2's own prediction that returning to the room-specific mistake-video register (this round's bathroom/bedroom/kitchen×4/general cluster) would outyield the generic design-secrets register. **Two headline findings**: (1) a black-fixture claim Krasnov made in Round 1 is reversed by 2 of his own 3 statements on the topic across this round, converging with this vault's existing Kruglov/Ontario position — see the updated Perspectives block on `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md`; (2) kitchen kickplate/toe-kick ergonomics, a genuinely new mechanism explaining why the popular "floating cabinet" trend causes real fatigue, routed to `03_Kitchen/Kitchen_Furniture.md`. 3 rounds complete, 24 of 115 manifest videos processed, ~91 remaining. Full detail in `krasnov_design_channel_triage_20260901.md`'s Round 3 section.

**Round 3 guidance**: this round's own methodological finding — a "design methodology + premium-styling" listicle cluster restates itself heavily, both within-round and against Round 1 — suggests future rounds should favor room-specific mistake videos (plumbing/bathroom/kitchen/flooring, Round 1's register) over generic "design secrets/premium tips/psychology" listicles (Round 2's register) when selecting the next batch from this channel's ~35+ remaining untouched videos.

**One genuine cross-channel Perspectives disagreement recorded**: black-vs-chrome bathroom-fixture mark visibility, directly opposing the existing Kruglov/Ontario position — see `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md`.

**No priced figures anywhere in this round** — unusual for this vault's turnkey-studio sources; worth watching whether this channel's monetisation model simply doesn't lean on public pricing the way others do, or whether Round 1 just happened to draw from a low-pricing-content slice of the catalogue.

**Round 2 not yet dispatched.** The channel's "mistakes/secrets/traps" cluster has **~50+ videos still untouched**. Per this vault's own "format beats topic" finding (established on Кузина/Шеврина), check for longer-format content (client consultations, project walkthroughs, podcast-style interviews) before committing to more short listicles — none of Round 1's 8 videos exceeded ~14.5 minutes.
