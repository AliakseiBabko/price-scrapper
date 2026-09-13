---
source_type: video transcript (BlenderBIM/IFC specialist channel, short how-to)
source_url: https://www.youtube.com/watch?v=jTL3a6QwckA
video_id: jTL3a6QwckA
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_custom_wall_type_7d2bffa0.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2022-11-02 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "BlenderBim - Custom Wall Type in 5ish mins"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 7
promotional_ratio: none
corroborates_existing: false
region: south_africa_presenter_names_his_type_South_African_standard_220_masonry - flagged, thickness not transferred
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: ⚠️⚠️ A CORRECTION - the Type Library Does NOT Quantise Wall Thickness, and the Worked Example Is Literally 220 (YouTube jTL3a6QwckA)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**BlenderBim-era (2022-11); read because no Bonsai-era replacement exists.** `promotional_ratio: none`. `corroborates_existing: false` — **this source corrects a previously recorded inference rather than supporting it.**

## ⚠️⚠️ 1. THE CORRECTION: authoring an exact wall thickness is a five-minute task

**The previous round recorded, from [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §8, that a practitioner accepted a 200 mm wall type *"because that's similar to a masonry brick wall of 220"* — and I inferred from it that "a type-library workflow trades dimensional fidelity for schedulability."**

**That inference was wrong, and this video is the proof — by the same presenter, using the same number.**

He builds a wall type from scratch in five minutes:

1. An **empty** object, named `MT R1 R2 220 masonry wall`;
2. assigned the IFC class **`IfcWallType`**;
3. given an **`IfcMaterialLayerSet`** — *"that creates a set of materials **including a thickness**"* — with layer set name **`double brick`**;
4. **thickness set to `220`** — *"that's a double wall"*;
5. saved as a standalone `.ifc` into his own library folder: *"this is going to be **my South African standard 220 masonry wall**."*

> **→ ⚠️⚠️ THE LIBRARY SHIPS COARSE DEFAULTS (100 / 200 / 300 / 350); IT DOES NOT CONSTRAIN YOU TO THEM.** The 20 mm error in the earlier source was **convenience, not a limitation** — the practitioner simply did not bother, in a tutorial where it did not matter.
>
> **→ The correction matters for this project specifically.** Our walls carry **exact `clear_mm`** in `data/canonical/`, and the recorded inference implied that adopting a type-based workflow would cost dimensional fidelity. **It would not.** **The type system is exactly as precise as the number you type**, and a per-wall-thickness type library is a small, one-off authoring job.
>
> ⚠️ **What survives from the earlier note is the weaker and still-true observation**: the *nearest stock type is the path of least resistance*, and a practitioner under no dimensional pressure will take it. **That is a discipline risk, not a tool limitation** — and it is the kind of thing a gate catches.

## ⚠️⚠️ 2. Thickness is a property of the TYPE, and retyping an instance changes its geometry

He demonstrates the reverse direction: an existing 300 wall is retyped to the new 220 type —

> *"Come down to **IFC object metadata → IFC construction type**… **assign type**… **and you see it has changed the thickness of the wall to 220.**"*

> **→ GEOMETRY FOLLOWS THE TYPE. Changing a wall's type changes what it is dimensionally, not merely how it is labelled.**
>
> ⚠️⚠️ **This is a clean, desirable property and it is the opposite of the placed-not-associated defect recorded across this whole batch.** Here the association holds: one edit, and the model updates. **It also means a wall's thickness is not free-form per instance** — a different thickness needs a different type, which is the discipline our `wall_blocks.csv` already imposes from the other direction.
>
> ⚠️ **And it makes the phase-by-type pattern worse** — see [[_Sources/YT__hADRIo-ma4_ifcarchitect_custom_phases|_hADRIo-ma4]] §3, where every phase needs its own type. **Multiply "one type per thickness" by "one type per phase" and the library grows as their product.**

## ⚠️ 3. He verifies the result with the measure tool

After loading the type and placing a wall: *"select the measure tool and **measure it to make sure it's right** — and you can see **it says 220**, which is quite nice."* He measures the stock 300 wall first, as a control.

> **→ A READBACK CHECK, and they are rare in this material.** ⚠️ **It is the same circular form as [[_Sources/YT_xlmbZHIaHJw_cgessentials_homebuilder_floor_plan_from_scan|xlmbZHIaHJw]] §1** — it confirms the tool applied the number he typed, not that the number is right — **but unlike that case there is nothing else it could check, since the thickness is a specification rather than a measurement of something real.** **Recorded as an appropriate use of a readback**, and as a mild contrast: *checking that a tool did what you asked is worthwhile when you authored the value, and worthless when you inferred it.*

## Mechanics worth keeping

4. **⚠️ A type library is a FOLDER OF `.ifc` FILES that the user owns**, outside the add-on install — *"I'm going to navigate to my IFC library, **which is a folder that I've created — it's not the library that comes with it**"* — loaded per project via `IFC project library → paperclip`.
   > **→ ⚠️⚠️ UNLIKE STYLESHEETS, PATTERNS AND TITLE BLOCKS, TYPE LIBRARIES ARE PROJECT-EXTERNAL BUT USER-OWNED — so they are git-trackable.** Corroborates [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|4JYFYvNg5Xk]] §3. **If any part of this were adopted here, a `types/` directory of small IFC files in the repo is the shape it would take**, and the presenter notes IFC files are *"incredibly efficient, kilobytes big."*
5. **`IfcMaterialLayerSet` is the native construct for a layered wall build-up** — a set of materials each with a thickness. ⚠️ **Directly relevant and currently unused here**: our walls are single-material solids, but a real renovation wall is block + plaster + finish, and **the layer set is where a finish schedule and a per-layer quantity would come from.** Flagged as a capability we have not modelled.
6. **A type can be created from a blank project**, not only by duplicating a shipped one — he starts from `blank project` rather than the IFC4 demo library.
7. **Thumbnails auto-generate** for a loaded type.

## What was deliberately NOT extracted

- All UI paths and panel names — BlenderBim-era, dated.
- **The 220 mm figure is NOT transferred as a dimension.** He names it *"my South African standard 220 masonry wall"* — ⚠️ **a national convention, and this flat's wall thicknesses come from `data/canonical/`, measured.** The figure appears above only because it is the arithmetic proof of §1.
- **No prices, no regulatory content.**

## Source Notes

*Ifc Architect* (YouTube), 2022-11-02, 5 min, **read in full**. **Claims are this presenter's, as opinion.** ⚠️ **Eighth source from this presenter in the vault.** ⚠️⚠️ **He is a South African architect and names his own national standard here explicitly** — see [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] §6. **Standing rule 4: no regulatory routing from this channel.** ⚠️ **Dated**: `IfcWallType` and `IfcMaterialLayerSet` are IFC-standard and stable; **the UI around them is not**, and the workflow should be confirmed against our installed Bonsai 0.8.6-alpha260801 before being relied on.
