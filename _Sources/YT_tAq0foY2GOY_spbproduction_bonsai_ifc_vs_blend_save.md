---
source_type: video transcript (BlenderBIM quick-tip channel, controlled demonstration)
source_url: https://www.youtube.com/watch?v=tAq0foY2GOY
video_id: tAq0foY2GOY
transcript_file: _Archive/processed_sources/20260913_spbproduction_bonsai_ifc_vs_blend_save_1ebe35bd.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2023-11-20 (confirmed via yt-dlp metadata)
channel: SPB Production
source_title: "Bonsai BIM: save as an IFC or a Blend file?"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 6
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - SPB Production: ⚠️⚠️ THE ONLY CONTROLLED EXPERIMENT IN FOUR BATCHES - and It Finds a Hazard in Our Own Viewing Instructions (YouTube tAq0foY2GOY)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️⚠️ Why this five-minute video is extracted at 6 facts

**It is the only source across four batches of this material that runs an actual experiment with a control, and reports what happened.**

His method, unprompted: create **two objects that differ in exactly one property** — a cube converted to an `IfcSlab`, and a sphere left as a plain Blender mesh — then **save each way, restart Blender, reopen, and observe which survived.** Then he varies it again: delete one file, open the other, observe. **Four conditions, one variable, a restart between each to defeat in-memory state.**

> **This is what the rest of this material conspicuously lacks.** The vault's standing complaint across the last four rounds is that *essentially nothing is measured* and that **a self-generated check is not an independent one**. **Here the design is sound, the variable is isolated, and the conclusion follows from the observation.** `promotional_ratio: none` — no sponsor, no plug, no product.

## ⚠️⚠️ 1. THE RESULT: the IFC is the master; the `.blend` is a cache that holds geometry but not data

| Condition | Outcome |
| :--- | :--- |
| Save as **IFC**, restart, reopen the IFC | The `IfcSlab` cube is there. **The plain Blender sphere is gone.** *"Blender objects or Blender properties are not saved in an IFC file."* |
| Save as **`.blend`**, restart, reopen the blend | **Both** survive — IFC objects and plain Blender objects. |
| **Delete the `.blend`**, open the IFC | *"The IFC exists on its own, with the geometry AND IFC data."* |
| **Delete the IFC**, open the `.blend` | *"**The geometry is still there, but the IFC data is LOST**… I could reload it and find it again of course, but if Blender doesn't find the file, the geometry exists, I can still edit it and work with it as a Blender file, **but the IFC data is lost**."* |

> **→ ⚠️⚠️ THE `.blend` DOES NOT CONTAIN THE IFC DATA. IT CONTAINS GEOMETRY PLUS A LINK TO THE IFC FILE THAT HOLDS THE DATA.** Break the link and you are left with a mesh — the exact thing BIM exists to be more than.
>
> **This validates the architecture this project already has.** Our IFC is authored programmatically and is the master; Blender is a **viewer** (`00_Master/How_To_View_Outputs.md`, `00_Master/Model_and_Views.md`). **A `.blend` is never the source of truth here, and this source shows precisely why it must not become one.** ⚠️ **It also says that nothing of value is lost by our not keeping `.blend` files at all.**

## ⚠️⚠️ 2. THE HAZARD FOR THIS PROJECT: the two files are LINKED, and Ctrl+S writes to the IFC

> *"You can see here that **the shortcut for saving IFC project or saving Blender project is the same**. So once they are connected, once you hit **Ctrl+S** — or save IFC project, or just go simple save — **BOTH the blend file and the IFC file are saved.**"*

He demonstrates it: moves the cube, presses save, reopens each file, and **both reflect the move.**

> **→ ⚠️⚠️ AN ORDINARY `Ctrl+S` IN A BLENDER SESSION WRITES TO THE CANONICAL IFC.**
>
> **This is an actionable safety finding about our own documentation, not a general observation.** `00_Master/How_To_View_Outputs.md` instructs the owner to open the project IFC in Blender with Bonsai — *"then `File → Open IFC Project`"* — in order to **look** at it. **In that session, a reflexive Ctrl+S after nudging the view, or any accidental edit followed by a save, silently rewrites the deliverable.** Blender users press Ctrl+S constantly; it is muscle memory.
>
> **And our gates would not necessarily catch it.** `check_dxf_closure.py` and `raster_fidelity.py` assert the **DXF** against the canonical data and the source PDF. **A mutated IFC that nothing re-derives from would not be checked by either** — and the IFC is what the owner is told to open.
>
> **→ OPEN ITEM RAISED, and it is cheap to close**: either open the IFC **read-only** for viewing (a copy in a scratch directory, or a file-permission bit), or **hash the project IFC and assert it in the batch gate** so an out-of-band modification is caught at commit. ⚠️ The second is the same pattern already used for the **frozen** ink mask and registration in `raster_fidelity.py`, and for the archived transcripts — **this project already knows how to do this; it just has not applied it to the IFC.**

## 3. The rule that follows, stated as a workflow choice

> *"Basically it depends on your workflow — whether you will be saving only as an IFC project, or whether you will be using some of Blender's functionality and then you want to save both the IFC and the blend file."*

> **→ The `.blend` is only needed for Blender-native work that has no IFC representation** — lighting, cameras, render setup, modifiers. **For this project that is exactly the `build_apartment_demo.py` render path, and nothing else.** Recorded as the clean division: **IFC for the model, `.blend` only for presentation state that is legitimately not part of the building.**

## 4. Corroboration within the batch

**[[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §6 states the same trap from the authoring side**, a year earlier and from a different presenter: *"you're only saving the IFC, not the Blender file — so if you have something in the Blender file that you want to save, make sure it's classified as an IFC, or just save the Blender file separately."*

> **→ Two independent sources, same finding.** ⚠️ **The one this source adds and the other does not is the LINKED SAVE (§2)** — which is the half that actually creates risk for us, because it makes the dangerous direction the default one.

## 5. What "classified as IFC" means, concretely

The conversion step is explicit: a plain mesh becomes a BIM object only when an IFC class is **assigned** to it — he makes the cube an `IfcSlab`. **An object is not in the model because it is in the scene; it is in the model because it carries a class.**

> **→ Corroborates [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §11 from the opposite direction**: there, deliberately-unclassified drafting lines were used to draw a countertop that would never reach a schedule. **Same mechanism, once as a feature and once as a trap.**

## 6. ⚠️ The limits of this experiment, stated plainly

**It tests persistence, not fidelity.** He confirms that the `IfcSlab` and its data **survive** a round trip; he does **not** check that geometry, property sets, GUIDs or relationships come back **unchanged**. A silent lossy round trip — a dropped property set, a regenerated GUID — would pass every condition he ran.

> ⚠️ **For this project that is the question that would actually matter**, since our IFC carries the canonical data and GUID stability is what a BCF issue or an IDS report would key on. **Recorded as untested, not as safe.**

## What was deliberately NOT extracted

- Blender and add-on version details — the add-on has since been renamed to Bonsai.
- UI paths — dated.
- **No prices, no regional claims, no regulatory content, no dimensional figures** — there are none in the video.

## Source Notes

Tom, SPB Production (YouTube), 2023-11-20, 5 min, **read in full**. **Claims are this presenter's, as opinion** — though **this is the rare case where the claim rests on a demonstrated result rather than an assertion**, and the experimental design is recorded above so it can be judged. ⚠️ **Dated to the BlenderBIM era**; the save behaviour is architectural rather than cosmetic and is unlikely to have changed, **but §2 should be reproduced against our installed Bonsai 0.8.6-alpha260801 before the open item is closed** — the fix is cheap enough to apply either way.
