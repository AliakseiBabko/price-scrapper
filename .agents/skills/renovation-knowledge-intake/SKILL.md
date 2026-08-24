---
name: renovation-knowledge-intake
description: "Project wrapper for turning renovation budgeting/planning sources (YouTube videos, screenshots, transcripts, case studies, notes) into this repo's renovation budgeting knowledge base and master guide. Defines this project's extraction taxonomy and storage paths only - delegates fetching, extraction, and synthesis to the shared youtube-transcript-fetch, visual-evidence-organize, meeting-transcript-extract, and tiered-knowledge-base skills. Use when a new renovation/budgeting source (video, screenshots, transcript, document) needs to be processed into the project's knowledge base or master budgeting guide."
---

# Renovation Knowledge Intake

Project-local wrapper only. All extraction, taxonomy-grouping, and
synthesis logic lives in the shared skills below - this file exists to
supply the project-specific facts they need (taxonomy, storage paths,
this repo's own instructions) and to sequence the handoff between them.
Do not reimplement fetching, extraction, or wiki-synthesis rules here.

## Required start

1. **Read this repository's own instructions first** - `.antigravityrules`
   at the repo root - before processing a source, in case it states a
   relevant convention this skill should defer to.
2. Confirm exactly one source is being processed, unless the user
   explicitly asks for batch processing (matching
   `tiered-knowledge-base`'s own batching rule - see that skill's
   `references/tiered-pipeline.md`).

### Deferred maintenance backlog

[`references/backlog.md`](references/backlog.md) tracks housekeeping/
completeness work explicitly deferred in favor of active channel
expansion (e.g. the Workstream D/E residual from the closed
`PRICE_SCRAPPER_ATTRIBUTION_AND_CURRENCY_NORMALIZATION` dialogue). Not a
pipeline step to run on every source - check it when the user asks to
resume housekeeping, and add to it (rather than letting deferred work go
unrecorded) whenever new work is knowingly deferred this way.

### How to invoke this file (added 2026-08-17)

Read this project-local file directly and follow it as plain instructions;
do not assume the harness resolves it through a `Skill`-tool invocation. See
[`references/lessons.md`](references/lessons.md#background-agent-dispatch)
for the incident that established this rule.

### Dispatching a large batch to a background agent (added 2026-08-17)

If this skill is being run by a background/sub-agent (not the main session)
on a multi-video batch:

- **Chunk it.** The serialized, minutes-spaced fetch requirement (see
  below) means a 25-30 video batch in one agent dispatch burns a large
  token/wall-clock budget and risks hitting a hard session limit mid-batch
  with no clean resume path - a real dispatch on 2026-08-17 stalled this
  way partway through a 30-video list. Split into several smaller
  sequential dispatches (roughly 5-8 videos each) instead of one dispatch
  for the whole list.
- **Never let a dispatched agent delegate further.** It must do the work
  itself and the orchestrator must verify real changes. See
  [`references/lessons.md`](references/lessons.md#background-agent-dispatch).
- **Always verify a background agent's completion claim against
  `git status --short`, the CSV row count, and the status JSON below** before
  trusting its narrative report.
- **Maintain a status file for every dispatched chunk:**
  `_Inbox/planning/batch_status_<YYYYMMDD>_<short-label>.json`. It maps each
  assigned video ID to exactly one of `pending`, `fetched`, `extracted`,
  `integrated`, `archived`, `skipped`, or `failed`; update it at every
  transition. If spacing pauses interrupt a chunk, resume the same agent
  after checking this file, then cross-check archive citations if a collision
  is suspected. See
  [`references/lessons.md`](references/lessons.md#background-agent-dispatch).

## Shared skills this wrapper uses

- `youtube-transcript-fetch` - fetches a YouTube transcript to a file.
- `visual-evidence-organize` - organizes/describes a dump of screenshots.
- `meeting-transcript-extract` - extracts structured facts from
  transcript/text sources, in **caller-defined taxonomy mode** using this
  project's taxonomy (below) instead of its default meeting schema.
- `tiered-knowledge-base` - owns the intermediate store and master wiki:
  upserting facts, preserving traceability/uncertainty, deciding whether
  the wiki needs updating.

If any of these shared skills isn't available in the current environment,
say so explicitly and ask the user how to proceed rather than
improvising its job here.

## Source folders

Raw sources for this topic land and get archived in locations this repo
already uses (per `.antigravityrules` and the existing
`00_Master/processed_sources.csv` convention) - this wrapper reads from
and writes evidence pointers to these, but does not relocate files itself
beyond what the shared skills already do:

- **Inbox** (new, not-yet-processed sources): `_Inbox\` - e.g.
  `_Inbox\transcripts\` for a `youtube-transcript-fetch` output
  directory, `_Inbox\_Visual_Drop\` for screenshots pending
  `visual-evidence-organize`.
- **Archive** (raw source evidence after processing): `_Archive\processed_sources\`.
- **Source log**: `00_Master\processed_sources.csv` - this wrapper does
  not own writing to it, but a processed source should be logged there
  per this repo's existing convention (a separate step from the
  knowledge-base handoff below).

### CSV schema and status vocabulary (canonical - this is now the authoritative copy)

`Schema`: `run_id,date,source_type,source_url,source_title,source_hash,source_year,region,pricing_priority,conversion_basis,topic_tags,scope,target_docs,status,notes`

**`run_id` format (changed 2026-08-17, collision-safe by construction):**
`run_<YYYYMMDD>_<source_key>`, where `source_key` is a stable identifier
already unique per source - the YouTube video ID for a YouTube source (the
same ID already used everywhere else in this skill for dedup), or a short
stable slug for another source type (e.g. derived from its URL or
filename). **Do not use a sequential counter** (the older `run_YYYYMMDD_N`
form seen in earlier CSV rows) for any new row - two sessions/agents
writing on the same day can independently pick the same next `N` with no
way to detect it until the rows collide. A real collision from exactly this
cause happened on 2026-08-17 (two concurrent sessions processing the same
playlist batch both picked `run_20260817_N` values that collided) and left
a wiki citation pointing at a filename a different writer had actually used
- see [[feedback_background_agent_batch_orchestration_pitfalls]]. Keying
the id off the source itself instead of a shared counter needs no
coordination between writers and makes a same-source double-log
self-evident (same `run_id` twice) rather than silently overwriting a
different source's row. Existing rows already using the old sequential
form are historical - leave them as-is, don't rewrite CSV history to
migrate them.

`status` must be one of:
- `inbox` / `processing` - mid-workflow, transcript fetched but not yet fully extracted/integrated.
- `archived` - fully processed: extracted, integrated into the knowledge base, transcript moved to `_Archive\processed_sources\`.
- `skipped` - could not be processed (e.g. no captions available via either `youtube-transcript-api` or `yt-dlp`, or the video is private/unavailable) - never fetched or extracted. Note the specific reason in `notes`.
- `duplicate_skipped` - the video ID was already logged under a prior `run_id` before this one started (checked by canonical video ID, not by re-deriving a transcript hash) - not re-fetched or re-extracted. Cite the earlier `run_id`/source-note slug in `notes`.
- `failed` - a fetch or extraction attempt was made and errored for a reason other than "no captions"/"duplicate"/"unavailable" (e.g. a tool crash) - distinct from `skipped` so a genuine bug isn't confused with an expected no-captions/duplicate outcome.

**Before fetching anything from a playlist or channel already represented in this CSV**, canonicalize each candidate video ID (from any URL form - `watch?v=`, `youtu.be/`, `shorts/`, `embed/`, a playlist entry) and check it against every `source_url` in this CSV *and* every `YT_<video_id>_*.md` source-note filename under `11_Budget_and_Planning/_supporting/knowledge/sources/` - a row can exist without a note (e.g. `duplicate_skipped`) and in principle a note could exist without a row, so check both. Do not rely on transcript-hash-based dedup alone (it only catches a duplicate *after* re-fetching, and does nothing for a video whose prior row has `source_hash: n/a`).

**`tools/youtube/preflight_playlist.py`** (added 2026-08-04) automates exactly this check - run it against a playlist/channel URL before invoking `youtube-transcript-fetch` on anything from it:

```
.venv\Scripts\python.exe tools\youtube\preflight_playlist.py "<playlist_or_channel_url>" --output-dir <dir>
```

**Default is light mode (changed 2026-08-05): duplicate check only, no network probing.** Pass `--probe` to additionally check per-video availability/caption-track presence up front (one extra yt-dlp call per fresh video) - opt-in only, because that probing was observed contributing to a YouTube 429/IP-block on the same run that then also blocked the real transcript fetch immediately after. For normal processing, prefer light mode and let `youtube-transcript-fetch` report per-video availability/caption failures itself when it fetches each video. If `--probe` is used and hits a rate-limit/IP-block response, the script stops probing further videos in that run (circuit breaker) rather than generating more 429s.

It writes a UTF-8 JSON manifest (never round-trips metadata through the console, which has previously mangled Cyrillic titles) classifying every video as `duplicate` / `private` / `unavailable` / `no_captions` / `rate_limited` / `fresh`, and warns if a CSV row and a source note disagree about what's been processed. Read-only - it never touches the CSV, moves a file, or fetches a transcript itself.

**Fetching must be serialized, not parallel, and spaced out** - one video at a time via `youtube-transcript-fetch`, with real spacing between fetches (order of minutes, not back-to-back), never multiple videos/agents fetching concurrently. The root cause isn't "this video" or "this channel" - `youtube-transcript-api`/`yt-dlp` are unofficial access paths sensitive to request pattern and IP reputation, not a stable sanctioned API; a 429 or a "Sign in to confirm you're not a bot" wall are both YouTube's automated-traffic defenses reacting to the same underlying thing. If a fetch exits with code 2 (rate_limited_or_ip_blocked - see that skill's own docs), treat it as a circuit breaker for the whole fetch phase: stop fetching further videos in this run, don't mark them `skipped` in the CSV, and don't retry immediately - wait for a real cooldown and use at most one bounded retry.

**Channel-switching on rate-limit, added 2026-08-24, per explicit user instruction**: don't just idle-wait out a cooldown when this happens - switch to processing a different channel instead, so work continues while the blocked channel cools down. `_Inbox/planning/youtube_channel_queue.md` is the standing multi-channel queue this applies to: it names which two channels are meant to be "active" at a time (Group A, construction/technique channels processed the same way as this skill's existing worked examples) plus a separate trial-only Group B (design/room-tour channels, value explicitly unconfirmed) and Group C (a CAD/2D-plan channel needing its own scoping pass). When a rate-limit hits one active channel, pick up the other active one, or pull the next unstarted Group A channel from that queue if only one was active - resume the paused channel later after a real cooldown, same bounded-single-retry discipline as above. Read that queue file before starting any new channel's intake.

### Language: always fetch and cite the original language (Russian), never a translated caption track (added 2026-08-24)

Per explicit user direction: the large majority of sources this project processes are Russian-speaking channels/practitioners, even when a video's on-screen title, description, or YouTube's own auto-translated metadata is in English — **title/metadata language is not a signal of spoken-audio language**, and several already-processed sources from English-titled videos (e.g. multiple Kruglov/Ontario videos titled "The BEST lighting options for your APARTMENT," "10 BEST ELECTRICAL SOLUTIONS") turned out to have fully Russian spoken audio and Russian-language captions once fetched. Always fetch the original-language (Russian) transcript, never an auto-translated-to-English caption track, even if an English track is offered or looks more convenient.

**Why this matters, concretely**: this project's own searchability depends on it. If some sources are archived in Russian and others in a translated-to-English caption track, a later search for a specific Russian technical term (a part name, a technique, a measurement convention) won't reliably find every source that actually discusses it — you'd have to separately search the term and its possible translations across two languages, and translations of the same Russian term are rarely stable/consistent across different auto-translation passes. Keeping every transcript in its real original language keeps a single Russian-word search reliable across the whole archive.

**Mechanically, this is already the default** — `youtube-transcript-fetch`'s underlying tool tries `--languages ru,en` (Russian first, English only as a fallback if no Russian track exists at all) — but this default must never be overridden to `en,ru` or `en` for a Russian-speaking source, and this expectation should be treated as a hard rule, not an implementation detail that happens to currently be true. Verified 2026-08-24: 100% of this project's 292 archived transcripts with a recorded language field are Russian (`"language": "ru"`), consistent with the channels processed so far.

**This also governs how extraction notes and wiki pages are written, not just how transcripts are fetched.** When `meeting-transcript-extract` produces the extraction note (pipeline step 3) and when that content is later routed into a wiki `analysis/` page (step 5a), **preserve the original Russian term inline** (in quotes, alongside its English translation/explanation) for every named technique, material, part, or measurement convention the first time it's introduced in a bullet — not just a translated-only English paraphrase. This is already happening in most existing source notes (e.g. `"сшитый полиэтилен"`, `"хомуты"`, `"лучевая"` in `YT_QcYJwQgu67g_kruglov_perfect_plumbing_mistakes.md`) but had never been written down as a rule before this — make sure it keeps happening deliberately, at both the extraction-note layer and the wiki-page layer, not just the raw archived transcript, so a future search for a specific Russian word works regardless of which layer someone is searching.

**Authenticated fetching (`--cookies-from-browser`) is an opt-in escalation path, not the default.** If anonymous fetching keeps hitting a 429/bot-check wall on a small batch, `youtube-transcript-fetch` (and this tool's own `--probe` mode) support `--cookies-from-browser BROWSER[:PROFILE]` to authenticate as an existing logged-in browser session - see that skill's own docs for the tradeoffs (account-level risk distinct from IP-level limiting; never export/commit/log cookie contents or the cookie database path). Use it deliberately per-run when needed, not as a new default for every batch.

`youtube-transcript-fetch` itself lives outside this repo (global, machine-local, at `~/.claude/skills/youtube-transcript-fetch/`) and isn't versioned by this repo's git history. A point-in-time backup of its 2026-08-05 rate-limit-hardening patch is kept at `tools/youtube/vendored_skill_backup/youtube-transcript-fetch/` (read-only reference, not live/imported) specifically so that fix doesn't silently vanish on a machine/session with an older unpatched copy - see that folder's own `README.md`.

**`tools/youtube/archive_transcripts.py`** (added 2026-08-04) does the move-to-archive-and-repoint-the-note step once extraction notes exist for a batch of fetched transcripts:

```
.venv\Scripts\python.exe tools\youtube\archive_transcripts.py <inbox_dir> [--dry-run]
```

It matches each transcript to its source note by the `.meta.json` sidecar's own `video_id` field against each note's frontmatter `video_id:` field - never by filename globbing (a prior glob-based approach broke on a video ID with a leading underscore) - and rewrites the note's `transcript_file:` line by regex on the frontmatter key, not by guessing at the old path string. Run with `--dry-run` first on an unfamiliar batch.

### Process note for a broad (non-topic-scoped) playlist (added 2026-08-05)

For a playlist that isn't scoped to one topic (i.e. its videos will end up routed across several different wiki pages, not one), run `preflight_playlist.py` **and** a lightweight topic-clustering pass **before** splitting into parallel extraction batches - classify each fresh video's likely destination page(s) first (a quick title/first-line skim is enough, doesn't need to be exact), then batch by destination cluster rather than arbitrary chunks of N videos. The bottleneck on a broad playlist is synthesis (deciding per-fact page routing and reconciling it across sources afterward), not extraction - grouping related content into the same batch up front means each batch's own report comes back pre-organized by page, cutting down the reconciliation work substantially versus discovering the routing spread only after all batches finish.

Section-reference validation (checking that a prose `§N.M` cross-reference actually matches an existing heading) was considered as a companion tool during the 2026-08-04 hardening pass but deliberately deferred - not worth building preemptively. Revisit if a heading/anchor mismatch actually surfaces again, or when the next larger wiki reorg happens (a natural time to add a repo-wide reference check, since headings are being renumbered anyway).

### Value-filter pass before processing a list of videos (added 2026-08-17)

Per explicit user guidance (confirmed effective on a real 8-video test against the Zemskov/Zemstandart channel, 2026-08-17): whenever asked to process a **list** of sources (a playlist, a channel, or any named batch of several videos) - not a single video - run a value-filter pass before committing to full pipeline processing on all of them, rather than processing every fresh video in the list by default. This is a separate concern from the topic-clustering pass above (that one decides *how to batch*; this one decides *whether to process at all*), and both apply together on a broad, high-volume list.

1. **Title-skim triage first.** Skim titles (and any known channel-specific formats) to flag videos that look more likely to carry genuinely new, checkable content (a specific number, dimension, code/regulation reference, or named technique/mechanism) versus videos that look like a channel's low-substance recurring format (e.g. this channel's "$X wasted, thanks to the designer/developer" dunk-style videos, which a direct trial found to be heavily self-promotional with thin technical yield). Title sentiment alone is not a reliable filter on its own - a "how not to X" or dunk-format title sometimes turned out to be the densest source in a batch, and a positive "how to X" title sometimes just repeated an existing price campaign's script - so treat the title-skim as a first-pass narrowing step, not a final verdict. **Update (2026-08-17)**: for the Zemskov/Zemstandart channel specifically, "как нельзя / how not to X" titles were misleading in 14/14 checked in one batch - every one was actually a positive step-by-step technique demo, not a critique. Still spot-check (title-skim narrows, it doesn't decide), but for this channel lean toward treating "how not to" as a positive-content signal.
2. **Spot-check before full extraction.** For flagged (and any genuinely uncertain) videos, fetch the transcript and do a quick read for density/promotional-ratio before running the full `meeting-transcript-extract` + `tiered-knowledge-base` integration on it. Two videos uploaded close together should also be checked against each other (and against already-processed sources) for script/project reuse - the same time-limited price campaign or the same apartment walkthrough can produce two videos with near-zero independent marginal value.
3. **Only fully process (or partially process) what clears the bar.** A video that's mostly promotional narrative with little checkable substance can be processed partially (extract just the few genuinely new facts) or skipped outright rather than run through the full pipeline. A video abandoned after this pass still gets a `00_Master/processed_sources.csv` row if it was actually fetched (reuse `status: skipped`, and say why in `notes` - e.g. "low-value pass: spot-checked transcript, mostly promotional/duplicate script, not extracted" - to distinguish this from a no-captions skip); a video excluded by title-skim alone, never fetched, does not need a row (same as any video never selected off a manifest).
4. **When unsure whether a filter is worth the cost at all**, do a small trial batch first (2-4 videos) processed the normal way, report back the substance-to-promotion ratio honestly, and let the user decide whether to filter the rest of the list this way, process all of it anyway, or stop - do not silently apply a strict filter to a whole large list without that check-in on the first list of its kind.

**What counts as "valuable" for this filter (per explicit user guidance, 2026-08-17)** - use these as the actual triage criteria in steps 1-2 above, not just "high fact density":

- **Favor:** a real case/project with concrete numbers and detail about what was actually done, why it was done that way, and what the alternative/comparison was (a genuine "X vs Y, and here's why X" with reasoning) - not just an outcome stated in isolation.
- **Favor:** content where the author (or a team) is visibly synthesizing a pattern across multiple real projects/cases - a practitioner or group doing something research-like on a topic - over a single one-off anecdote presented as a universal rule.
- **Favor:** genuine practitioner experience and technical rationale, even from a source that also runs a business, as long as the *content itself* is explaining a real mechanism/tradeoff rather than just asserting a conclusion.
- **Filter out / deprioritize:** content that's fundamentally branded promotion for the specific author's/channel's own company or services - a pitch dressed as advice.
- **Filter out / deprioritize:** pure consumer/client sentiment about a renovation ("we love how it turned out", satisfaction-only testimonials) with no concrete technical or numeric substance behind it - sentiment alone doesn't answer "what should I actually do."
- This criteria set works together with (does not replace) the existing "Advertising / promotional content filter" and "Market data vs. tier-steering" sections below, which apply *within* a source once you've decided to process it - this value-filter criteria is for the *upstream selection* decision, before spending extraction effort on a source at all.

### Round yield and stopping signal

When a channel/list round is declared complete, append one structured line to
its planning file: `**Round N yield**: <videos processed> videos, <genuinely-new
fact count> new facts (excluding duplicate/corroborating-only outcomes), yield
= <new facts / videos processed>.` Count a fact once even if it routes to
several pages. For the next round, default to stop-and-ask-the-user if yield
falls by more than 50% from the previous round or is below **1.0 new fact per
processed video**. The absolute floor makes a weak tail explicit; document
the reason in the planning note if an exception is chosen.

### Source-note quality fields

At step 6, add these optional frontmatter fields to each new or updated source
extraction note:

```yaml
fact_yield: 0
promotional_ratio: low | medium | high
corroborates_existing: false
```

`fact_yield` is a rough integer count of genuinely new facts;
`promotional_ratio` describes substantive-to-promotional balance; and
`corroborates_existing` is true only when the source materially confirms an
existing claim. These are project-local annotations, not shared-skill schema
changes.

## This project's taxonomy

Pass this exact bucket list to `meeting-transcript-extract` as the
caller-defined taxonomy for every renovation/budgeting source processed
through this wrapper. Room buckets match this repo's own numbered room
folders (`01_Entrance` … `10_Balcony`):

```
Rooms / Zones
Entrance
Hallway
Kitchen
Living and Dining Room
Kids Room
Small Bedroom / Study
Bathroom
WC
Laundry Room
Balcony / Loggia
Demolition
Flooring
Walls / Ceilings
Kitchen Appliances
Laundry Appliances
Other Appliances
Electrical
Switches / Sockets / Cables
Lighting
Plumbing
Doors / Trim
Furniture / Built-ins
Materials
Labor Prices
Material Prices
Quantities / Measurements
Cost Drivers
Budget Ranges
Planning Rules
Regulations / Permits / Approvals
Mistakes / Warnings
Family Requirements / Preferences
Design Concept
Unclear / Needs Confirmation
Other / Unclassified
```

Use these buckets exactly as given - don't rename, merge, or reorder them
per `meeting-transcript-extract`'s own taxonomy-mode rules. This is the
single taxonomy for this wrapper's topic ("renovation budgeting and
planning") - it does not vary per source. The `Family Requirements /
Preferences` and `Design Concept` buckets exist so a source that touches
family needs or aesthetic direction feeds those specific `00_Master`
documents' subject matter (via the intermediate store, not by this
wrapper writing to those files directly - see Guardrails).

## This project's storage paths

Pass these exact paths to `tiered-knowledge-base` (its own required-start
step asks for these three; this wrapper answers that question so the
user doesn't have to restate it each time):

- Source extraction notes folder:
  `11_Budget_and_Planning\_supporting\knowledge\sources\`
- Intermediate knowledge store:
  `11_Budget_and_Planning\_supporting\knowledge\intermediate\store\_index.md`
  (the former monolith is retained as a redirect stub; use the linked
  `Numeric_Data.md`, `Durable_Facts.md`, `Rules_Heuristics.md`,
  `Planning_Rules.md`, `Pending_Wiki_Page_Decisions.md`, and `Change_Log.md`
  files, opening only the bucket(s) touched by the source)
- Master wiki page (auto-updatable):
  `11_Budget_and_Planning\Budgeting_Guide.md`

Create these paths if they don't exist yet; don't invent alternate paths
or fall back to `tiered-knowledge-base`'s generic suggested layout - this
wrapper's paths take priority for this topic.

### Regulations / Permits / Approvals - a second, stricter-bar store

Content sorted into the `Regulations / Permits / Approvals` taxonomy
bucket (above) goes to a **separate** intermediate store, not the main
budgeting one, because jurisdictional facts need a higher evidence bar
than pricing or technique - applying the wrong city's rule is actively
misleading, not just imprecise:

- Regulations knowledge store:
  `11_Budget_and_Planning\_supporting\knowledge\intermediate\renovation_regulations_belarus_knowledge_store.md`
  (intake staging only — once a new qualifying fact lands here, also mirror it
  into the dedicated wiki folder below per step 5a's routing pattern)

### Regulations / Permits / Approvals now has its own wiki folder too (added 2026-08-24)

`16_Legal_and_Regulations/` is a dedicated, strictly-Belarus-scoped wiki
section (compact `Legal_and_Regulations_Guide.md` + layered `analysis/`
pages: `Renovation_Permits_and_Approvals.md`, `Property_Registration.md`,
`Handover_Acceptance_and_Defect_Reporting.md`) — the synthesized
counterpart to the intermediate store above, same relationship as
`Durable_Facts.md` has to a room/domain `analysis/` page. When a source's
`Regulations / Permits / Approvals`-bucket content clears this store's
level-1 Belarus-attribution bar, mirror it into the matching `analysis/`
page under `16_Legal_and_Regulations/` the same session, not just into the
intermediate store — this folder is a routine step 5a destination now, not
a placeholder waiting for a future audit.

**This folder's evidence bar is stricter than the rest of the project's own
convention, not just a repeat of the store's bar above**: elsewhere in this
project, a Russian-Federation source is explicitly usable as *secondary
comparative reference* for pricing/technique (clearly labeled as such).
**That allowance does not extend to `16_Legal_and_Regulations/` at all** —
law, permitting bodies, and registration/warranty procedure are
jurisdiction-specific; a Russian-sourced legal/regulatory claim is a
different country's law, not just weaker evidence, and must never be
written into this folder even with a hedge/caveat. If a source's
regulatory content is Russian (or any non-Belarus) and doesn't independently
qualify for the general store's own level-1 bar, it stays out of this
folder entirely — route it to the general budgeting store's own
Rules/Heuristics or Durable Facts instead, same as any other RU-sourced
technique content, never into `16_Legal_and_Regulations/`.

Property Registration and Handover/Acceptance/Defect-Reporting are
currently empty placeholders — per explicit user direction, properly
filling them out is a dedicated future task (reviewing actual Belarus
legislation/official procedure), not something to backfill opportunistically
from renovation-vlog transcripts the way the rest of this project's
technique/pricing content is built. A video source can still contribute if
it genuinely clears the level-1 bar, but don't treat incidental video
mentions as sufficient coverage for this folder the way they are for other
topics.

Contractor-sourcing/vetting content (finding and evaluating renovation
contractors/workers) is a budgeting/execution decision, not a legal one —
route it to `11_Budget_and_Planning` as normal, never to
`16_Legal_and_Regulations/`, even though a source may discuss it in the
same breath as handover/registration topics.

### Design Concept-bucket content now has its own wiki folder too (added 2026-08-24)

`17_Design_and_Ergonomics/` is a dedicated wiki section for general design/
aesthetics/color-scheme/furniture-arrangement/ergonomics/functional-zoning
knowledge gathered from sources — the synthesized counterpart to the
`Design Concept` taxonomy bucket, same relationship the Regulations store
has to `16_Legal_and_Regulations/`. When a source's `Design Concept`-bucket
content is genuinely general technique (not this project's own specific
decision), mirror it into the matching `analysis/` page under
`17_Design_and_Ergonomics/` the same session — routine step 5a destination
now, not a holding pen.

**This folder is explicitly not where this project's own specific design
decisions go.** `00_Master/Design_Concept.md` and
`00_Master/Family_Requirements.md` remain the only place for this
project's own chosen palette/materials/family routines — this wrapper still
never writes to those two files directly (existing guardrail, unchanged).
`17_Design_and_Ergonomics/` is general practitioner knowledge only, the same
way `11_Budget_and_Planning` is general budgeting knowledge rather than this
project's own specific budget.

**Per-room integration**: once a room folder (`01_Entrance` … `10_Balcony`)
accumulates enough room-*specific* design/zoning/furniture-arrangement
sources, it gets its own "Design & Zoning" `analysis/` page (per the vault's
standing don't-force-structure-before-content-exists rule) that cross-links
back to `17_Design_and_Ergonomics/` for the general principle being applied.
No room has crossed that threshold as of 2026-08-24 — don't create one
preemptively.

### What counts as a case study

Per explicit user guidance: a case study is **not** limited to a full
start-to-end renovation project. It's any **logically self-contained,
non-scattered body of information** about home renovation that can stand
on its own as a reference - which can be:

- A full-cycle project (design through move-in) - the original, narrower
  reading.
- A **scoped** slice: one room, one stage/phase of work, one trade, or
  one material category - as long as the source's coverage of that scope
  is coherent and detailed enough to be useful on its own, not just a
  handful of unrelated one-off mentions.

The deciding question is **coherence, not scope size**: does the source
present a connected, internally consistent body of information about
*something* (a stage, a room, a full project), or is it scattered
mentions of unrelated things? The former can earn a case study; the
latter belongs in the intermediate store's regular sections regardless
of how much total content it has. When in doubt, a source with real
arithmetic-checkable structure (stage totals, itemized line items that
sum to a stated whole) is a stronger case-study candidate than a source
that's just a list of loosely-related tips - but don't require "single
verified real project" as a hard gate the way earlier passes in this
project implicitly did.

**Only admit a fact to this store if the source names a specific
location directly in its own content (level 1 - spoken/written in the
source itself), not merely via channel branding, tags, or title (level
2 only).** A source whose region is inferred only from metadata does not
clear this bar, even if it's otherwise a reliable source for the main
budgeting store. This store is a scaffold the user intends to build out
further from non-video sources (official codes, исполком procedures,
etc.) - don't treat sparse video-only coverage here as a gap to rush to
fill.

`11_Budget_and_Planning\Renovation_Sequence.md` is a separate, top-level,
human-curated companion page (sequencing summary). It is **not** the
master wiki page and this skill must not auto-update it - if a source
clearly affects sequencing content, note that in the intermediate store
and let the user decide whether to fold it into `Renovation_Sequence.md`
by hand, or ask the user explicitly before editing it directly.

## Pipeline

For one source at a time:

1. **YouTube source** → run `youtube-transcript-fetch` first to get the
   transcript file. Do not proceed to extraction on an un-fetched video.
1a. **Company/advertising website source** → fetch the real rendered page
   text before extracting, not a summarization tool's paraphrase - see
   "Company website sources: fetching and marketing filter" below for why
   and how. Save the fetched text as an evidence file under
   `_Archive/processed_sources/` (same convention as an archived
   transcript) before treating it as a text source for step 3.
2. **Screenshot/image source** → run `visual-evidence-organize` first (or
   use an existing screenshot-analysis artifact already produced by it),
   to get an organized, described bundle. Do not attempt raw OCR/image
   reading here.
3. **Transcript/text source** (the fetched transcript, an organized
   screenshot bundle's description output, a document, a case study, or
   notes) → run `meeting-transcript-extract` in caller-defined taxonomy
   mode, passing this project's taxonomy (above). This produces the
   structured Markdown extraction note.
4. **Hand the extraction note to `tiered-knowledge-base`**, passing this
   project's three storage paths (above) as the resolved paths so it
   skips its own path-resolution prompt.
5. `tiered-knowledge-base` writes/updates the source extraction note in
   the sources folder and upserts the intermediate knowledge store. For
   each Durable-Facts-bucket item, **prefer routing it directly to an
   existing matching room/domain wiki `analysis/` page** (following
   `00_Master/wiki_page_format.md`) instead of appending it to
   `Durable_Facts.md`. Use `Durable_Facts.md` only when no matching wiki
   page exists yet, or when the fact is genuinely cross-cutting and has no
   single-page home; record the gap in Pending Wiki-Page Decisions when
   appropriate. Update the master wiki page **only if** this source changes
   or strengthens the synthesized guide - not on every source.
   Every claim added to a wiki guide or `analysis/` page should name its
   source channel/practitioner inline, cross-checked against the note's
   `channel:` frontmatter, when that field is decisive - never inferred or
   guessed. **Corrected 2026-08-20, per direct user feedback**: when the
   channel can't be confirmed, do not write `attribution: unconfirmed` -
   that produced hundreds of content-free notices adding no usable
   information. Instead leave the claim's own existing citation as the only
   marker, and make sure it links directly to the specific source (not just
   a page-level Source Notes list) so the claim stays traceable even without
   a named channel. See `00_Master/wiki_page_format.md`'s "Inline attribution
   when it can be confirmed" section for the full corrected rule.

5b. **Normalize every new price at intake.** When a source adds a price
   figure to the intermediate store, a guide, or a comparison table, append a
   USD-equivalent and keep the original currency and amount unchanged. If
   the source's publish date/year is absent, record that the conversion is
   not computable.

   **Precision by category, per explicit user instruction (2026-08-21)** -
   the source's confirmed publish date (usually the `yt-dlp` upload date) is
   the anchor for all three; query `tools/pricing/currency_converter.py`
   directly against `data/scraper.db` rather than `exchange_rates_reference.md`'s
   calendar-year rows, which are now a fallback for when the exact publish
   date can't be pinned down, not the default:
   - **Individually volatile/short-cycle categories (appliances, and
     anything else priced like a consumer-electronics item)**: use the
     **exact publish date**, daily granularity -
     `python tools/pricing/currency_converter.py --pair USD/RUB --date <YYYY-MM-DD> --amount <N>`.
   - **General renovation materials/services (the default case)**: use the
     **trailing 6 or 12 calendar months ending on the publish date**, not a
     calendar-year average (the two rarely line up with when the price was
     actually current) -
     `python tools/pricing/currency_converter.py --pair USD/RUB --trailing-months 6 --before <YYYY-MM-DD> --amount <N>`
     (use `12` instead of `6` when the source itself spans a longer project
     timeline, or when 6 months of samples would be too thin to trust).
   - **Publish date confirmed but only to the year** (day/month unknown):
     fall back to `exchange_rates_reference.md`'s calendar-year average, or
     `currency_converter.py --period <YYYY>`, and note the reduced
     precision.
   For current-year (2026+) sources, run
   `python tools/pricing/fetch_exchange_rates.py` to refresh the database
   with the latest daily rates if needed.

   **Missing-year rule, per explicit user instruction (2026-08-21)**: if a
   source's price year has no row yet in `00_Master/exchange_rates_reference.md`
   (e.g. a 2013 or 2016 source, older than this table's current 2017 floor),
   don't stop at "not computable" - backfill the real year first, then
   convert:
   1. `python tools/pricing/fetch_exchange_rates.py --backfill --start-year <YEAR>`
      to pull the real daily series for that year from CBR/NBRB into
      `data/scraper.db` (verified working back to at least 2013 for both
      currencies as of this instruction).
   2. `python tools/pricing/generate_exchange_rates_reference.py` to
      regenerate the reference table from the database - it preserves every
      already-`confirmed` row untouched and only adds the new year.
   3. Convert using the newly-added row, citing it normally.
   **USD/BYN pre-2016 caveat**: Belarus redenominated the ruble in mid-2016
   (four zeros dropped). A pre-2016 BYN figure is on the old, much larger
   scale (e.g. ~10,000-16,000 old-BYN per USD, not ~2-3) - never divide a
   pre-2016 BYN price by a post-2016 rate or vice versa; confirm which side
   of the redenomination the source's own figure and year fall on before
   converting, and note this explicitly if there's any ambiguity.
   Never use a current spot rate or a guessed value for any year.

   **Rounding, per explicit user correction (2026-08-21)**: a USD-equivalent
   is a comparability aid for an approximate figure, not a transaction
   record — never show cents/decimal places. Round to a whole dollar at
   minimum, and round further to a fixed bucket by magnitude, not by eye:
   **nearest 10 below $1,000, nearest 100 from $1,000-$99,999, nearest
   1,000 above that** (e.g. `4,000 RUB → ~$50/m²`, not `$47.2/m²`;
   `32,000-130,000 RUB → ~$500-$2,000`, not `$494.6-$2,009.3`). The
   exception is a figure that is itself genuinely exact — a real stated
   transaction total, or one recovered by an explicit arithmetic
   cross-check against other stated figures in the same source (e.g. the
   7komnat.by case's $70,000/52m² totals) — those stay precise, since
   rounding them would discard real information rather than avoid
   manufacturing false precision.

   **Self-check before reporting, don't just eyeball the total**: an
   off-by-a-few-dollars miss on the rounding bucket (e.g. `$63` instead
   of the correct `$60`, or `$53,000` instead of `$53,200`) is easy to
   miss by reading the total and hard to catch after the fact — it has
   happened twice (`PRICE_SCRAPPER_USD_BACKFILL_RESIDUAL` rounds 2 and 7).
   `tools/verify_batch.py`'s `check_rounding_bucket` check now catches
   this automatically for any newly-added `≈$` figure — run it (or read
   its JSON `problems` for `"check": "rounding_bucket"`) before reporting
   a batch as done, not only after a reviewer flags it.
5a. **When a source's content instead (or additionally) gets folded into
   a room or systems wiki page** (`07_Bathroom/Bathroom_Guide.md`,
   `12_Engineering_and_Systems/*`, `13_Surfaces_and_Finishes/*`,
   `14_Furniture/*`, etc. - outside this wrapper's own three owned
   paths, but a routine downstream step per this project's established
   practice), follow the page-shape convention in
   `00_Master/wiki_page_format.md` -
   **this is the default shape for new and growing content now, not
   just a retrofit for pages that already got unwieldy.** Concretely:
   a brand-new topic with several distinct sub-decisions starts
   directly as a compact guide page + `analysis/` detail pages (with
   Source Notes and Change Log split into their own pages from the
   first source, not deferred); an existing *layered* page gets new
   facts routed into the right `analysis/` page as full prose, with
   only a sentence-level touch-up to the compact guide if the summary
   itself needs to change; an existing *single-file* page (currently:
   `08_WC/WC_Guide.md`, `09_Laundry_Room`, `03_Kitchen`,
   `10_Balcony`) keeps accumulating normally until its own topic
   decomposition genuinely calls for splitting, per that file's own
   "Default going forward" section - don't split preemptively on a
   guess.

   **This step is routine, not deferrable (confirmed the hard way,
   2026-08-18).** A real multi-session batch (Category 5 trial + all of
   Category 3 + a first Category 4 chunk, ~19 sources) wrote everything
   to the intermediate store only and never took this step, despite
   several sources containing content that clearly belonged on an
   existing room/systems page (plumbing stub-out coordinates, masonry
   technique, kitchen island sizing). Nothing enforced doing it in the
   moment, so it silently didn't happen across an entire multi-turn
   session until the user asked directly whether wiki pages had been
   updated. Treat 5a as owed *per source*, the same turn its content is
   integrated into the store - not something to batch into a separate
   "catch-up pass" later, even though that's what recovered it this
   time. If a session's pace makes per-source routing impractical (e.g.
   a fast multi-video chunk), say so explicitly to the user rather than
   silently deferring it.

   **The routing pass is also an error-catching mechanism, not just
   placement.** Re-read the original transcript before marking a routed fact
   as corroborating or confirming an existing page; flag ambiguous
   negation/contrast phrasing (especially Russian `не X, а Y`) as `uncertain`.
   See [`references/lessons.md`](references/lessons.md#negation-routing-incident)
   for the incident behind this rule.

   **When a source's content has no existing wiki page to route to at
   all** (not "which section," but "no page exists for this sub-topic
   yet"), don't create a separate holding file for it — the intermediate
   store already is that staging area. Note it inline (as this store's
   sources already do, e.g. "no dedicated Windows page exists yet") and
   also add/update an entry in the store's own "Pending Wiki-Page
   Decisions" section near the top of the file. **Threshold rule: once a
   sub-topic has 3+ sources accumulated with no page, create the page
   that session** — don't defer further. This was adopted and first
   applied 2026-08-18: a Windows page had been deferred since
   `yt_BbtWl3n-GNg` first flagged the gap on 2026-08-10, accumulated to
   13 sources by 2026-08-18 with the gap re-flagged almost every time,
   and was only actually built once the threshold was made explicit and
   retroactively applied. Don't wait for a user to notice a gap has grown
   this large again.
6. **Promotion self-check (do not skip):** after step 5, re-read the
   extraction note's full prose one more time and confirm every concrete,
   reusable fact/rule/mechanism/number in it - not just the ones that
   happened to make the store's Source Index summary paragraph - has a
   corresponding entry in the store's Durable Facts, Rules/Heuristics, or
   Numeric Data sections. A fact "existing" only inside the extraction
   note file, invisible unless someone opens that specific note directly,
   does not count as captured. This step exists because this exact gap
   was found and fixed for six sources on 2026-07-31 (see the store's
   Change Log) - it recurred across multiple sources before being caught,
   so treat it as a standing risk on every source, not a one-off cleanup.
   Vague/promotional/low-value mentions can be skipped; a specific
   mechanism, a checkable rule, or a concrete number cannot.

## Renovation delivery model classification

Per explicit user guidance: this project's own plan is a **self-managed /
piecemeal** renovation (hiring individual specialists per trade, sourcing
materials directly, no single company managing design-through-furnishing),
not a **turnkey / full-service** renovation (one company handles design,
project management, quality control, and construction as one bundled,
higher-priced package). These two delivery models produce genuinely
different $/m² figures for comparable work, and conflating them makes a
turnkey company's price look like "the" market rate when it actually
includes overhead (management, design, coordination) the self-managed
approach doesn't pay for.

**Classify every source/case using this dimension** and record it
explicitly (in the extraction note, the store, and the guide where the
figure is cited):

- **Turnkey / Full-Service** — a company (often the source's own
  business) quotes an all-in price covering design, project management,
  and construction/furnishing as one bundle. Company case studies and
  self-promotional "here's what our client paid us" videos are almost
  always this category by default - check for a bundled design fee,
  mentions of a company handling "under key"/"под ключ" scope, or a
  project manager/foreman role priced into the total.
- **Self-Managed / Itemized** — per-work-type or per-material average
  market rates, meant for someone assembling their own team and sourcing
  materials directly (a "смета" broken into individual line items with
  no company-management overhead bundled in is the clearest signature).
  **This is the category most relevant to this project's own plan** -
  prioritize surfacing this kind of data prominently, not burying it
  under turnkey figures.
- **Labor-Only** — a narrower version of the above: rates for hired labor
  specifically, materials priced/sourced separately.
- **Mixed / Ambiguous** — a source blends both, or doesn't give enough
  detail to tell (e.g. a company channel that also candidly discusses
  brigade/self-managed alternatives). Record what's known rather than
  forcing a single label.

**Do not blend a turnkey $/m² figure with a self-managed one** as if they
describe the same thing - keep them as clearly separate, clearly labeled
numbers everywhere they appear (store, guide). When `Budgeting_Guide.md`
cites a headline benchmark, state which delivery model it reflects.

## Price comparability requires location AND year - a price without both has minimal comparative value

Per explicit user guidance: a price/cost figure only has real comparative
value once it carries **both** of these, not just one:

- **Location/market** - which country, and (where knowable) which city or
  market tier within it. "RUB" alone is not a market - Moscow, a
  provincial Russian city, and Minsk can have very different price levels
  even in the same currency. Record the most specific location the source
  actually supports (per this project's existing level-1/level-2/level-3/
  level-4 evidence framework) rather than defaulting to a channel's
  general regional association.
- **Year** - when the price was stated (source upload/publish date,
  confirmed via metadata where possible - see "Confirm dates via metadata,
  not assumption" below). Prices in this market move meaningfully year to
  year (a real example already in this store: the same company's design
  fee rose from 3,000 RUB/m² in 2022 to 5,000 RUB/m² by 2026, ~67% over
  ~4 years - ordinary inflation, not noise to round away).

**Practical effect on every price/cost entry (source note, intermediate
store Numeric Data entries, `Budgeting_Guide.md`, comparison tables):**

- Record location and year explicitly next to every price figure, not
  just once at the top of a source note - a reader looking at one row of
  a comparison table shouldn't have to hunt elsewhere for either.
- **Never compare, average, or flag two prices as "conflicting" without
  both references resolved for each side of the comparison.** A price
  gap between two sources from different years is not evidence of a
  contradiction until inflation/time is accounted for; a price gap
  between two sources in different cities/markets is not evidence of
  overcharging or undercharging until the market difference is accounted
  for. Where one or both references are missing, say so explicitly
  ("year unconfirmed", "region unresolved") rather than implying a clean
  comparison was made.
- A price with **neither** reference resolved still has some value - as a
  bare data point attached to a specific type of work/material - but must
  not be used for cross-source comparison, ranking, or "is this a good
  price" judgments until at least one of the two is resolved.
- **Confirm dates via metadata, not assumption, whenever practical** - a
  video's stated upload date can now be checked directly via `yt-dlp`
  metadata (`extract_info(...).get('upload_date')`) rather than left as
  "not independently confirmed" by default; do this before treating two
  same-topic prices from what might be different eras as either
  consistent or contradictory.

## Advertising / promotional content filter

Renovation-content channels are very often run by the company doing the
work, a sponsored partner, or a real-estate/supplier affiliate — treat
that as the default assumption, not the exception. When processing a
source:

- **Identify the source's own monetization/promotional format** up
  front (self-case-study of the channel's own project, a joint
  interview with a named business partner/store, an explicit
  sponsor-gift call-out, embedded recruitment/affiliate links, a
  specific residential complex or property being showcased) and record
  it in the extraction note and store, even when the surrounding
  factual content is otherwise usable.
- **Brand, supplier, and specific-property endorsements from a
  promotional or self-interested source are not "universal" findings.**
  Extract them (don't delete real evidence), but tag them clearly as
  commercial mentions - a business recommending its own partner's
  product, or a company showcasing its own project, is not neutral
  technical fact even if phrased as advice.
- **Prioritize durable, brand-agnostic, region-appropriate technique and
  heuristics** (placement rules, drainage mechanisms, approval
  processes, cost-driver reasoning, sizing rules of thumb) over "buy
  brand X" or "this specific ЖК/development is worth it" claims when
  deciding what's worth carrying into the intermediate store's Durable
  Facts/Rules sections and especially into `Budgeting_Guide.md` - the
  guide in particular should stay brand- and property-name-free by
  default, since it's the compressed, most-trusted-by-default layer.
- This is a filtering *lens* applied during extraction and synthesis,
  not a retroactive editorial rule that deletes already-recorded source
  content - a source note can and should still say "the speaker
  recommended Brand X," just with the commercial context attached.

## Company website sources: fetching and marketing filter

A company's own website is the single most self-promotional source type
this project processes - more so than even its YouTube channel, since
there's no third-party platform mediating it at all. Two separate
problems need handling for this source type: getting the *real* content,
and then filtering *marketing* from *usable data* within it.

### Fetching: use a real rendered browser, not a summarization tool, for anything that will become evidence

**Do not treat a `WebFetch`-style tool's paraphrase as source text.** Use a
real rendered browser and click through tabs, accordions, expanders, and
modals before saving evidence. See
[`references/lessons.md`](references/lessons.md#webfetch-tabs-incident) for
the incident that established this rule.

- **Prefer Playwright MCP** (`browser_navigate` + `browser_snapshot`/
  `browser_evaluate`) when available in the session - it renders the
  real page and lets you click through tabs/accordions/expanders one by
  one, reading `document.body.innerText` (or a similar real-DOM read)
  after each click, not just the page's default state.
- **If Playwright MCP isn't loaded in the current session** (MCP tools
  are loaded once at session start and won't appear mid-conversation
  even after `claude mcp add` - a genuinely new session is needed), fall
  back to `tools/web/fetch_rendered_page.mjs`, a local Playwright script
  with the same underlying capability (real rendered text, no
  summarization) but without tab-clicking built in - manually inspect
  the page structure first if you suspect hidden tabbed content.
- **Save the fetched text as a real evidence file** under
  `_Archive/processed_sources/`, the same way an archived video
  transcript is preserved - a website source needs the same
  traceability a transcript gets, not a one-off summary that can't be
  re-checked later.
- A `WebFetch` pass is still fine for a *quick investigative question*
  ("does this page mention a city name?") where losing hidden-tab
  content is an acceptable risk and nothing is being committed as
  evidence - the rule above applies specifically to fetching a source
  that will be extracted into the store.

### Marketing filter: what's real data vs. what's advertising copy

A company website is overwhelmingly written to persuade, not to inform -
most of its text is not extractable as durable fact. Apply this filter
during extraction:

**Extract as real data** (the actual point of processing this source
type):
- Concrete, checkable numbers: prices, dimensions, timelines, page/item
  counts, deposit amounts - anything a reader could verify or act on.
- Named, structured processes: a numbered stage list, a checklist, a
  named quality-control sequence - even if the company's own framing is
  "look how thorough we are," the *structure itself* (e.g. "review by
  more than one role before delivery," "bound scope-change requests to
  an explicit window") is a reusable planning artifact independent of
  which company is used.
- Specific technique/mechanism claims with a stated *reason*, not just
  an assertion - "frosted glass still leaks sound because X" is
  extractable (tag confidence per the advertising filter above); "our
  glass doors are the best" is not.
- Real project examples with real numbers (a specific job's actual
  cost/timeline/materials) - rare on a company's own marketing site
  compared to a case-study video, but extract them the same way as a
  video case study when present.
- Verifiable facts about the company itself when relevant to region/
  currency confirmation (see the Price Comparability section above) -
  an address, a founding date, a stated service area.

**Do not extract as durable fact** (recognize and skip, don't launder
into the store):
- Superlative/unverifiable claims with no underlying data shown ("we
  analyzed 100-200 projects," "the best quality on the market") - if
  specific enough to be worth recording at all, tag `unverified` and
  attribute it explicitly as the company's own claim, never adopt it as
  a store-level fact.
- Generic value propositions and "why choose us" framing with no
  checkable content behind them.
- Testimonials/reviews without concrete, specific detail attached
  (a vague "great service!" quote is not evidence of anything;
  a testimonial citing an actual price or defect is).
- The company's own "we know better than the client" framing on a
  technique claim - extract the technique, drop the framing (see the
  worked example in `web_zemspro_about_development`'s Mistakes/Warnings
  section: four real design rules were extracted from a passage whose
  overall point was "we override the client's wishes," which itself is
  not a fact worth recording).

This filter is a lens for what's worth carrying forward, not a
reason to under-process a company-website source relative to a video -
these sites can and do contain genuinely useful checklists, process
structures, and technique rules once separated from the surrounding ad
copy, per the worked example above.

### Market data vs. tier-steering - a finer distinction within promotional sources

Per explicit user guidance: most sources processed for this topic are
from turnkey/full-service companies (majority of sources so far, and
expected to remain the majority going forward). Within a source like
this, **separate two different things that get blended in the same
sentence**:

- **General market-rate/technique information** (what a work item
  typically costs, how a system works, what materials exist in a
  category) - usually reasonably fair/accurate, because it's describing
  a real market the company also operates in, not something they're
  fabricating.
- **The specific tier/product/service the company steers the viewer
  toward** ("we use this grade of material," "we recommend adding
  supervision/design services") - this carries a **structural incentive
  toward the company's own higher margin**, even when phrased as neutral
  advice, since a turnkey company's revenue scales with the tier the
  client selects.

**Practical effect**: when a source states "material/service X typically
costs $Y" as general market information, that's usable market data (tag
normally). When the same source then recommends *this specific*
material/service/tier as *the* choice, flag that recommendation as
tier-steering, not neutral technical guidance - the same market usually
has a cheaper equivalent a self-managed buyer could choose instead, and
the store/guide should make room for that framing (e.g. "a cheaper
in-category alternative may exist - see market rate cards") rather than
adopting the source's specific tier choice as the default.

## Guardrails

- **No raw source overwrites.** Never overwrite an existing source
  extraction note's underlying raw evidence, or an already-fetched
  transcript/organized screenshot bundle, when reprocessing a source -
  update the note, don't destroy the evidence trail under it.
- **No raw detail leaking into the wiki.** The master wiki page stays a
  compressed, readable guide (per `tiered-knowledge-base`'s own
  wiki-synthesis rules) - this wrapper doesn't relax that for this
  project's content, however detailed a case study source is.
- **Preserve uncertainty and traceability end to end.** A confidence tag
  applied by `meeting-transcript-extract` (ASR-uncertain, speaker-
  uncertain, inferred, single-account) must carry through
  `tiered-knowledge-base`'s own confidence tagging (`confirmed`/
  `inferred`/`uncertain`/`unverified`) rather than being dropped or
  silently upgraded at the handoff.
- **Don't add project-specific extraction or synthesis rules here.** If a
  gap is found in how sources get extracted or synthesized, fix it in the
  relevant shared skill, not by duplicating logic into this wrapper.
- **This wrapper doesn't write to `00_Master` documents directly.** The
  `Family Requirements / Preferences` and `Design Concept` taxonomy
  buckets route matching content into this topic's knowledge store/wiki
  like any other bucket - they do not make this skill write to
  `00_Master/Family_Requirements.md`, `00_Master/Design_Concept.md`, or
  `15_Appliances/Appliance_Preferences.md`. Reconciling the wiki's synthesized
  understanding with those standalone master documents is a separate,
  explicit step the user asks for, not an automatic side effect of intake.
