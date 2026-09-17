---
source_type: video transcript (Dynamite Revit, two long-form Bonsai tutorials - custom door/window types, and project setup)
source_url: https://www.youtube.com/watch?v=lR-zcXpnvco
video_id: lR-zcXpnvco
covers_also: Y0NUwQNqkKI
transcript_file: _Archive/processed_sources/20260917_dynamiterevit_door_window_custom_types_c61152a0.txt
transcript_file_pt2: _Archive/processed_sources/20260917_dynamiterevit_project_setup_levels_grids_953d59e6.txt
fetched: 2026-09-17 via youtube-transcript-api (en, ORIGINAL language)
upload_date: 2024-06-01 (lR-zcXpnvco); 2024-01-19 (Y0NUwQNqkKI) - from yt-dlp, actually run
channel: Dynamite Revit (Christina)
source_title: "Windows & Doors In BlenderBIM (Bonsai) | Working With Door & Window Modifiers To Custom Types" (+ Project Setup: IFC Project, Levels, Grids, Views)
language: en
extraction_taxonomy: custom (this project taxonomy - bucket `Digital Toolchain / IFC authoring`)
fact_yield: 5
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note — Christina (Dynamite Revit): custom types and project setup, from the playlist that was dismissed (YouTube lR-zcXpnvco +1)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

⚠️ **Provenance note:** this whole playlist was skipped in an earlier triage round as *"basic architectural wall/door drafting & Inkscape SVG post-processing"*. It contains a **45-minute** tutorial on door and window typing and a **26-minute** project-setup tutorial. The dismissal was wrong, and is recorded as superseded in `_Inbox/planning/bonsai_blender_triage_20260917.md`.

## 1. Door and window types are parametric, then customisable

- Bonsai ships **parametric geometry modifiers** on door and window types: *«select your door type and select geometry and materials, and under parametric geometry you can see that you have a door modifier… you can choose between different types of doors, double swing, left, sliding»*.
- The stated motivation is that ⚠️ *«the standard window and door types tend to offer a rather basic final look»*, so the tutorial goes further and builds **custom detailed types using Blender's modelling tools**.

⚠️ **The trade-off she names is one we will meet**: as a Revit professional, *«one huge aspect of my work so far has been to strike a balance between the level of detail of the geometry of my model and its performance»*. **Detail is not free.**

**→ For us**: our openings are generated as voids with frame members from the compiler. The parametric door/window *modifier* is an authoring convenience we do not need — but it confirms that **type-level parametric geometry is the normal home for door and window variation**, consistent with `fN9cP6w0DsM`: geometry is inherited from the type.

## 2. Project setup: levels, grids, plans and elevations (`Y0NUwQNqkKI`)

The setup sequence is **levels → grids → floor plans and elevations**, all from Project Overview; levels are added and their elevation edited and applied; Bonsai adds a standard grid that is then extended.

⚠️ **We have one storey** (`IfcBuildingStorey`, "Apartment level") and no grids. Nothing here says a flat needs grids; it says the tool expects them for a building.

## 3. ⚠️⚠️ The most useful thing in both videos is a warning about the sources themselves

> ***"one of the most exciting aspects of learning a software that's pretty much still in development is that sometimes very simple features get completely changed, so you do have to pay a lot of attention to where everything went"*** — and she pins her recording to Blender 4.0 and a specific Bonsai build, adding *«in a few months from now, maybe not all the things I'm going to [show still apply]»*.

**→ ⚠️ BONSAI TUTORIALS DATE FAST, AND UI STEPS DATE FASTEST.** This is a reason to take **schema statements** (what `IfcMaterialLayer.Priority` means) and **failure modes** (elements vanishing from the spatial tree) from this corpus, and to distrust **click-paths**. It is the same conclusion this project reached from the other direction in `_Inbox/planning/bonsai_toolchain_open_questions_20260917.md` §5: *take the mechanism, not the conclusion.*

## Source Notes
Christina, Dynamite Revit — two tutorials, 2024-01-19 and 2024-06-01, English original captions. Both predate the Bonsai 0.8.x releases discussed elsewhere in this vault, which is itself relevant per §3.
