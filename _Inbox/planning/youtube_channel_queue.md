# YouTube Channel Queue — Future Intake Work

Master list of channels to process, across three categories with different evaluation approaches. Created 2026-08-24 per explicit user request, as a durable plan to read before starting new channel work in any future session.

## Currently active (Group A channels already underway)

- **Zemskov/Zemstandart** — CLOSED. All 5 categories of the 372-video manifest complete as of 2026-08-19 (see [[project_zemskov_channel_triage_complete_20260819]] memory). Not a source of new work unless the user explicitly reopens it.
- **Konstantin Kruglov/Ontario** — PAUSED, rate-limited. Rounds 1–4 done, Round 5 halted 2/7 in (see `kruglov_ontario_full_channel_plan_20260824.md`). Round 4 yield 8.14 facts/video. **Do not retry yet** — see IP-wide-block correction below; paused 2026-08-24, same day as this queue entry.
- **Pavel Sidorik** — PAUSED, rate-limited. Rounds 1–5 done, Round 6 halted 2/7 in (see `pavel_sidorik_channel_plan_20260824.md`). Round 5 yield 13.0 facts/video (highest yet). Through episode #27 of 42 in its "New Building A-to-Z" series; the 36-episode "Khrushchevka" series and large standalone/tool-review pools still ahead. **Do not retry yet** — paused 2026-08-24, same day.
- **TimRemont** — PAUSED, rate-limited on its very first fetch attempt, before any content was assessed (see `timremont_channel_plan_20260824.md`). Rotated in as a third channel when both above paused simultaneously; this is the incident that revealed the block is IP-wide, not per-channel. **Do not retry yet** — no verdict possible on this channel until a real retry succeeds.
- **Petrishin-Stroi** — ACTIVE. Rounds 1-12 complete 2026-08-24 (88 videos fetched/extracted + 5 genuinely skipped for no captions, 802 new facts). Yields: 8.6, 9.5, 8.9, 11.1, 8.75, 9.5, 7.75, 7.6, 9.5, 9.6, 10.9, 7.2 facts/video — Round 12 at 66% of Round 11's baseline (a real drop, driven by two short single-technique TV-format clips and one heavily-pre-covered episodic-series episode, not a rate-limit or format failure), well above the 1.0 floor, no stop-and-ask trigger. Round 12 highlights: a genuinely distinct fourth flood/burst mechanism on this channel (a radiator freeze-burst from a management-company multi-unit heating shutoff combined with an open window, plus a positive-case corroboration of the radial-piping isolation benefit from the opposite direction of Round 10's finding); a Шумопласт cross-check confirming only partial (not full) originating-source status for Round 6's existing section, adding real manufacturer engineering-album spec data and a second product-selection criterion; and a first-touch spot-check of the older numbered "ЖК Виноградный" episodic series (~13 episodes, 2015-2017) with an explicit verdict to sample a few more episodes before committing to the full series. Two videos hit genuine no-captions failures. See `petrishin_stroi_channel_plan_20260824.md`. Round 13 next — 248 of 341 videos still remain (341 − 93 manifest entries touched across Rounds 1-12, counting the 5 skips).
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

## Group C — CAD / 2D Floor-Plan Channel (unique category, own evaluation)

https://www.youtube.com/@RemPlanner/videos

Per explicit user description: mixed content — CAD software tutorials/advice plus actual 2D floor plans and facades for real construction/renovation projects. **Value hypothesis (per user)**: the videos walking through an actual apartment's 2D plan could teach how to represent a real layout as a 2D/CAD drawing from real measurements — a third, distinct use case, not "renovation technique" (Group A) and not "design guidance" (Group B).

**This does not cleanly fit the existing `renovation-knowledge-intake` taxonomy** (checked 2026-08-24: neither `.agents/skills/homestyler-cad-to-revit/` nor `.agents/skills/residential-bim-geometry-rules/` are about extracting knowledge from external video sources — both are this project's own CAD/BIM production workflows, a different concern). Before processing this channel, do a small scoping pass: title-skim to separate pure software-tutorial videos (lower priority, generic CAD instruction) from videos that walk through an actual apartment's 2D plan/facade (higher priority, the ones with the hypothesized teaching value), and decide explicitly where extracted content should live (a new dedicated store/page, or an existing one) before running a trial batch — don't force it into the renovation intake pipeline's existing taxonomy buckets by default.

## Rate-limit channel-switching protocol (added 2026-08-24, per explicit user instruction)

When a fetch attempt returns a rate-limit/IP-block signature — HTTP 429, "Sign in to confirm you're not a bot," `youtube-transcript-fetch` exit code 2, or any error interpretable as upstream throttling — **do not simply wait idle for a cooldown.** Pause the current channel's round (per the existing circuit-breaker rule: no retry, no false `skipped` row for the blocked video) and switch to the *other* currently-active Group A channel to keep making progress. If only one Group A channel is active when this happens, pull the next unstarted channel from Group A's queue above to bring the active count back to two. Resume a paused channel later after a real cooldown has passed (as already practiced with Kruglov's Round 4 — a bounded single retry, not repeated hammering).

This is specifically a Group A protocol — Group B/C channels stay trial-only until their value is separately confirmed, so don't rotate one of them in as a rate-limit substitute without the user's go-ahead.

**Correction, confirmed 2026-08-24**: this protocol assumes a rate-limit is channel-specific, but a real incident the same day showed otherwise — Kruglov/Ontario, Pavel Sidorik, *and* a freshly-rotated-in TimRemont all hit the identical block signature (`youtube-transcript-api` IP-block message + `yt-dlp` "Sign in to confirm you're not a bot") within about 15 minutes of each other, the third one on its very first fetch attempt before any content was even seen. This points to a **session/IP-wide throttle**, not a per-channel one. **When a second channel switch in short succession also hits the same block signature, stop rotating in a third — that's the signal the block is IP-wide, and rotating further channels just burns dispatches into the same wall.** At that point, actually pause all YouTube fetching for a real cooldown (longer than the single-channel bounded-retry cooldown - this is a stronger signal) before retrying any of the blocked channels, rather than continuing to search for an unaffected channel.

## Progress Log

- 2026-08-24 — Queue created per explicit user request: 11 Group A channels, 8 Group B channels, 1 Group C channel, plus the rate-limit channel-switching protocol formalized (already practiced informally when Kruglov's Round 4 was rate-limited and the session switched to starting Pavel Sidorik). No channel in this queue has been preflighted yet.
