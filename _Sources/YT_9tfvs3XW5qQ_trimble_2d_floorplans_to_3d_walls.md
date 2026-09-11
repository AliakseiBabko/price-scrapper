---
source_type: video transcript (software vendor's own channel, GUI workflow — processed for MEASUREMENT DISCIPLINE only; GUI mechanics discarded)
source_url: https://www.youtube.com/watch?v=9tfvs3XW5qQ
video_id: 9tfvs3XW5qQ
transcript_file: _Archive/processed_sources/20260911_trimble_sketchup_2d_floorplans_to_3d_walls_57c6b5c3.txt
fetched: 2026-09-11 (anonymous, yt-dlp --write-auto-subs --sub-langs en-orig)
upload_date: 2025-06-17 (confirmed via yt-dlp metadata)
duration: 17:25
channel: Trimble SketchUp (official) — presenter Aaron Dietzen
source_metadata_location: not stated; imperial units, US-market
jurisdiction: n/a — no regulatory claim
language: en (en-orig auto-generated)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 4
promotional_ratio: medium (vendor channel teaching its own product)
corroborates_existing: true (independently states the oracle principle behind vector_extent_oracle.py)
---

# Extraction Note — Aaron Dietzen / Trimble SketchUp: "3 Ways to Convert 2D Floorplans to 3D Walls" (YouTube 9tfvs3XW5qQ)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

**Selected because its title is the closest in the batch to the owner's stated struggle** — 2D plan to 3D walls. **Honest assessment: the majority of it is SketchUp GUI mechanics** (push/pull to height, reversing inside-out faces, `orient faces`, careful group selection) **and is worthless to a programmatic pipeline.** It was extracted for three discipline statements that are tool-independent.

**Companion source**: `YT_althlPj8Tag` (same presenter, "CAD Linework to SketchUp Geometry") covers the import step and corroborates without adding an independent finding.

## Value-filter verdict

**Partial extraction — measurement discipline only.**

## Quantities / Measurements — ⚠️ the ink has width, and the width is an error term

Tracing a wall off a raster plan, he says exactly what he is doing and why it is uncertain:

> *"I can inference or, you know, I could draw an edge from about the middle of this black line here to about the middle of this black line here and see, okay, that's probably around 5½ inches… just like working off of a printed set of plans, the line itself is maybe an eighth or a quarter inch thick. So you need to take all this with a grain of salt when I'm looking at what this actually represents."*

**→ Two distinct points, and both are additions rather than restatements:**

1. **Reading a thickness off a raster requires first choosing which part of the drawn line you measure to** — centre, inner face, or outer face. He chooses centre-to-centre and says so; an unstated choice is an unstated error.
2. ⚠️ **The drawn line's own thickness is a genuine error bar.** `00_Master/Evidence_Reading_Discipline.md` requires identifying *"the two elements its extension lines terminate on"* — **this adds that the terminating element itself has thickness**, which at plan scale can be of the same order as the tolerance being claimed.

**Directly applicable to the `v0` reconstruction and to the frozen ink mask, where the mask's stroke width is exactly this quantity.**

## Mistakes / Warnings — ⚠️⚠️ the oracle principle, reached by hand

> *"In all these situations, I would recommend working alongside a dimension plan of some sort. It doesn't matter how good the information you get, there's always a possibility that there's a difference between what's in the model and the actual dimension it's supposed to represent. So I always recommend double-checking against printed dimensions of some sort, whether that's a PDF or a hard copy or whatever."*

**This is `tools/layout/vector_extent_oracle.py`'s reason for existing, stated from the GUI side by someone who arrived at it through experience.** The repo built that oracle after learning that *"asserting the DXF against `wall_blocks.csv` only proves that two things a person edits together agree"* — a coupled edit of both had passed the gate.

**→ Recorded as corroboration of the hardest-won lesson in this project's geometry work.** The claim he makes is stronger than a habit: *it does not matter how good your source is* — the check is required regardless of source quality.

## Design Concept — how you want the walls delivered changes the method

He opens by refusing to treat the question as having one answer: *"how you actually want your walls presented to you once you're done is going to change a little bit of how this works"* — all walls in one mass, or each wall in its own container; openings cut now, or added later. He notes the three methods therefore *"may look more like nine if you consider all the possibilities."*

**→ Mild corroboration of this project's own wall-versus-assembly split** — a wall is a calculation leg, an assembly is the physical element — reached here from the opposite direction, as a question about how the output will be consumed rather than how it is measured.

**He also confirms the raster's limits in passing**: *"I already scaled this so that it is about the right size. Again, about the right size, since I can't pull an accurate dimension."* Consistent with `YT_f0EU_xbavEA`'s conclusion that the underlay is orientation rather than measurement.

## Unclear / Needs Confirmation

- **No tolerance figures anywhere.** *"About the right size"*, *"probably around 5½ inches"*, *"a grain of salt"* — the discipline is qualitative by his own framing. **No numeric tolerance may be derived from this source.**
- He does not say how a door or window opening should be dimensioned once the wall is solid, only that he would *"come in and add in window geometry, door geometry as I had it"* later.
- ⚠️ **Everything about face orientation, `orient faces`, and group selection was discarded as tool-specific** and is not recorded above. If a future session wants the GUI method, the transcript is archived.
