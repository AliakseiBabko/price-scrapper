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
  `11_Budget_and_Planning\knowledge\sources\`
- Intermediate knowledge store:
  `11_Budget_and_Planning\knowledge\intermediate\renovation_budgeting_knowledge_store.md`
- Master wiki page:
  `11_Budget_and_Planning\knowledge\wiki\renovation_budgeting_master_guide.md`

Create these paths if they don't exist yet; don't invent alternate paths
or fall back to `tiered-knowledge-base`'s generic suggested layout - this
wrapper's paths take priority for this topic.

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
