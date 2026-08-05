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

- **Inbox** (new, not-yet-processed sources): `00_Inbox\` - e.g.
  `00_Inbox\transcripts\` for a `youtube-transcript-fetch` output
  directory, `00_Inbox\_Visual_Drop\` for screenshots pending
  `visual-evidence-organize`.
- **Archive** (raw source evidence after processing): `90_Archive\processed_sources\`.
- **Source log**: `00_Master\processed_sources.csv` - this wrapper does
  not own writing to it, but a processed source should be logged there
  per this repo's existing convention (a separate step from the
  knowledge-base handoff below).

### CSV schema and status vocabulary (canonical - this is now the authoritative copy)

`Schema`: `run_id,date,source_type,source_url,source_title,source_hash,source_year,region,pricing_priority,conversion_basis,topic_tags,scope,target_docs,status,notes`

`status` must be one of:
- `inbox` / `processing` - mid-workflow, transcript fetched but not yet fully extracted/integrated.
- `archived` - fully processed: extracted, integrated into the knowledge base, transcript moved to `90_Archive\processed_sources\`.
- `skipped` - could not be processed (e.g. no captions available via either `youtube-transcript-api` or `yt-dlp`, or the video is private/unavailable) - never fetched or extracted. Note the specific reason in `notes`.
- `duplicate_skipped` - the video ID was already logged under a prior `run_id` before this one started (checked by canonical video ID, not by re-deriving a transcript hash) - not re-fetched or re-extracted. Cite the earlier `run_id`/source-note slug in `notes`.
- `failed` - a fetch or extraction attempt was made and errored for a reason other than "no captions"/"duplicate"/"unavailable" (e.g. a tool crash) - distinct from `skipped` so a genuine bug isn't confused with an expected no-captions/duplicate outcome.

**Before fetching anything from a playlist or channel already represented in this CSV**, canonicalize each candidate video ID (from any URL form - `watch?v=`, `youtu.be/`, `shorts/`, `embed/`, a playlist entry) and check it against every `source_url` in this CSV *and* every `YT_<video_id>_*.md` source-note filename under `11_Budget_and_Planning/_supporting/knowledge/sources/` - a row can exist without a note (e.g. `duplicate_skipped`) and in principle a note could exist without a row, so check both. Do not rely on transcript-hash-based dedup alone (it only catches a duplicate *after* re-fetching, and does nothing for a video whose prior row has `source_hash: n/a`).

**`tools/youtube/preflight_playlist.py`** (added 2026-08-04) automates exactly this check, plus an availability/caption probe for the videos that turn out to be genuinely new - run it against a playlist/channel URL before invoking `youtube-transcript-fetch` on anything from it:

```
.venv\Scripts\python.exe tools\youtube\preflight_playlist.py "<playlist_or_channel_url>" --output-dir <dir>
```

It writes a UTF-8 JSON manifest (never round-trips metadata through the console, which has previously mangled Cyrillic titles) classifying every video as `duplicate` / `private` / `unavailable` / `no_captions` / `fresh`, and warns if a CSV row and a source note disagree about what's been processed. Read-only - it never touches the CSV, moves a file, or fetches a transcript itself.

**`tools/youtube/archive_transcripts.py`** (added 2026-08-04) does the move-to-archive-and-repoint-the-note step once extraction notes exist for a batch of fetched transcripts:

```
.venv\Scripts\python.exe tools\youtube\archive_transcripts.py <inbox_dir> [--dry-run]
```

It matches each transcript to its source note by the `.meta.json` sidecar's own `video_id` field against each note's frontmatter `video_id:` field - never by filename globbing (a prior glob-based approach broke on a video ID with a leading underscore) - and rewrites the note's `transcript_file:` line by regex on the frontmatter key, not by guessing at the old path string. Run with `--dry-run` first on an unfamiliar batch.

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
  `11_Budget_and_Planning\_supporting\knowledge\intermediate\renovation_budgeting_knowledge_store.md`
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
   the sources folder, upserts the intermediate knowledge store, and
   updates the master wiki page **only if** this source changes or
   strengthens the synthesized guide - not on every source.
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
  `00_Master/Appliance_Preferences.md`. Reconciling the wiki's synthesized
  understanding with those standalone master documents is a separate,
  explicit step the user asks for, not an automatic side effect of intake.
