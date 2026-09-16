# One model, many views

## The question

Are the 2D plans and the 3D volume two separate models, or one model shown two
ways?

## The answer: one model

**One model. The 2D drawings are generated *from* the 3D model, not drawn
alongside it.** That is the whole reason for the spec → IFC pipeline, and it is
already how everything currently produced works:

```
data/canonical/current_apartment_base.json      the geometry, once
        + data/variants/<id>.json               a variant as a patch
                    │
                    ▼
      tools/ifc/model_from_spec.py              ONE model per variant
                    │
                    ▼
             model.ifc  ── the single source of truth
                    │
   ┌────────────────┼─────────────────┬──────────────────┐
   ▼                ▼                 ▼                  ▼
A3 sheets        DXF plan         Blender / glb      quantities
(SVG + PDF)      (TrueView)       (3D volume)        (areas, finishes)
2D              2D               3D                 non-graphic
```

Every one of those is a **view**. A floor plan is a horizontal section through
the model at about 1.2 m; an elevation is a vertical one; the 3D scene is the
same solids with no section at all; a schedule of floor areas is a view with no
picture in it. In BIM terms they are all derived representations of one dataset,
and that is the standard practice this repo follows.

## Why it has to be one

If the plan and the 3D were separate models, they would drift the first time
anything changed — and you would not find out which one is wrong until a
contractor did. With one model:

- moving a wall in the spec changes the plan, the DXF, the 3D and the floor
  areas in the same run;
- **if two outputs disagree, that is a bug in a generator, not something to fix
  by editing a drawing.** Never correct a plan by hand — correct the model and
  regenerate;
- quantities are computed from the same solids you are looking at, so a
  take-off cannot quietly describe a different flat.

## ⚠️⚠️ Adding a WALKABLE view — what the route costs (researched 2026-09-16)

**A walkthrough is a VIEW, so it fits this architecture as another arrow off the
IFC. The question is only which tool and what it costs.** Evidence from four
practitioners who have done it: [source: [[_Sources/YT_HV-fbzv4VAU_bim_to_walkable_viewer_path|YT_HV-fbzv4VAU]]]

- **⚠️ THE EXPORT PATH IS SHORT AND CONFIRMED.** Bonsai/Blender → **GLB, glTF or
  FBX** → Twinmotion or a web viewer, all three arriving equivalently. **GLB is the
  usual choice because textures travel inside one file.** ⚠️ **Export VISIBLE or
  SELECTED, never "all"**, and **keep the hierarchy on import** — collapse it and
  the whole model becomes one object. Up axis Z, forward X.
- **⚠️⚠️ THE COST NOBODY STATES UP FRONT: APPEARANCE DOES NOT TRANSFER.** A BIM model
  arrives with no usable materials and **no UV mapping**, so every surface is
  re-dressed by hand in the destination tool (cubic projection works for
  architecture, since the geometry is orthogonal). **Low-poly BIM placeholder
  furniture and planting are deleted and replaced from the target's library.**
  > **→ ⚠️⚠️ THAT LANDS ON THE WRONG SIDE OF THIS PAGE'S OWN RULE. Materials
  > re-authored in a visualiser are NOT derived from the model — they are a second
  > source of truth, and they will drift exactly as this page warns.**
  >
  > **→ SO SCOPE THE WALKABLE VIEW TO WHAT IT IS FOR. To JUDGE SPACE — does the
  > passage past a lowered wall bed work, is the clearance tolerable — untextured
  > grey geometry answers the question completely, and the material work is
  > unnecessary.** **To SHOW someone a finished-looking room, the appearance work is
  > the majority of the effort and duplicates decisions already recorded in text.**
- **⚠️ A BROWSER/WEB walkable view is independently named as a real intermediate**,
  not a compromise — one practitioner lists interactive web apps with controls and
  filters as an output alongside Unreal, and a third party shipped Blender assets
  into a three.js site.
- **⚠️⚠️ UNREAL: the only end-to-end demonstration available DEMONSTRATES THE
  WORKFLOW AND NOT THE FIDELITY.** Its makers raised the accuracy question
  themselves — *"is it accurate? do the dimensions read correctly? … can I actually
  use it to build a virtual walkthrough?"* — conceded *"is it perfect? absolutely
  not"*, and ended the segment mid-experiment. **Dimensional accuracy is the one
  property this project would depend on, and it is unevidenced there.** ⚠️ A
  separate practitioner reports **~2 hours over two sessions** for first- and
  third-person walkthrough blueprints, using MCP for the blueprint work specifically.
- **⚠️ Twinmotion, in practice, is an IMAGE tool.** The dedicated Twinmotion source in
  this batch is entirely foliage, lighting, cameras, AI upscalers and Photoshop
  post-production — **nothing about circulation or dimensional judgement.** **It
  belongs on the "show someone" branch, not the "decide something" branch.**

### ⚠️⚠️ The mechanism behind "appearance does not transfer", and its price (added 2026-09-16)

**Three technical sources put a mechanism and a cost under the finding above.**
[source: [[_Sources/YT_i82_Rx1OUe0_glb_export_mechanics_and_what_survives|YT_i82_Rx1OUe0]]]

- **⚠️⚠️ IT IS A NON-TRANSFER, NOT A LOSSY ONE.** Demonstrated on camera: a working
  Blender shader exported to GLB opens in a glTF viewer *"completely blank."*
  *"Even if they were just one or two nodes blended together, Blender can
  understand them, but other softwares will not be able to read Blender's internal
  materials."* **The only universal carrier is an IMAGE TEXTURE.** ⚠️ A third
  source hits the same wall importing to Unreal — a procedural bump simply did not
  arrive — and states the rule as *"use pixel textures rather than procedural maps."*
- **⚠️⚠️ AND THE PRICE OF FIXING IT IS BIGGER THAN "RE-DRESS THE SURFACES": baking
  requires a UV MAP on every object** (*"if it doesn't have a UV map, your textures
  are not going to work"*), the renderer set to **Cycles**, and **one bake per
  channel** — base colour, roughness, metallic. ⚠️ Baking "combined" bakes the
  LIGHTING in, shadows included, permanently.
  > **→ An IFC model out of Bonsai carries NO UV maps. So a textured walkable view
  > means UV-unwrapping the whole apartment and baking several channels per
  > material, before any appearance decision is even made. That is a modelling
  > project, not an export step.**
- **⚠️⚠️ WHICH IS AN ARGUMENT FOR THE UNTEXTURED VIEW RATHER THAN AGAINST THE IDEA:
  geometry and flat colour need no UV map and no bake.** ⚠️ **One thing to VERIFY
  rather than assume, and it is cheap because we control it: whether a plain
  Principled BSDF base colour — no node network — travels as a glTF PBR material.
  None of these sources tests that case, and it is the one this project would use.**

**⚠️⚠️ AND A SIZE CONSTRAINT THAT BINDS THE WEB RUNG SPECIFICALLY**: a full
architectural scene with interior exported to GLB came out at **almost half a
gigabyte**, heavier than the same scene as FBX, with *"at least half an hour"* for
export plus import. ⚠️ **Not this project's case — that scene has exterior,
landscape and imported asset libraries, where this is one untextured apartment —
but it gives the rule: the web rung survives only while the model stays untextured
or lightly textured.** **The same conclusion the cost side reaches.**

**⚠️ Two export-integrity points worth keeping regardless of the decision**: **apply
SCALE (ideally all transforms)**, because *"the entire scaling goes completely
haywire"* otherwise; and **the exporter writes what is baked into the MESH, not what
the viewport shows** — node-generated geometry exports as its pre-modifier state.
⚠️ Mostly moot for a Bonsai/IFC model, which is real mesh, **but the scale point is
cheap insurance.**

**⚠️ On format choice, the sources agree with the pipeline's existing wording**: glTF
splits mesh, textures and dependencies into separate co-located files and is *"very
prone to errors"*; **GLB packs everything into one binary file, *"a lot more robust
and even faster to load, especially for web applications."*** **The format was
designed as a *transmission format* for exactly this use — real-time viewing over
the web — so nothing exotic is being proposed.**

> **→ ⚠️⚠️ CONCLUSION AS RESEARCHED, not as a decision: a glb walkable view is the
> cheap rung and it is sufficient for the spatial questions currently open on this
> project.** **Twinmotion buys appearance, at the price of a second source of truth
> for materials. Unreal buys interactivity and VR, and nobody in this batch has
> shown it dimensionally faithful.** **The decision is the owner's; this records what
> each rung costs.**

## What legitimately lives outside the model

Not everything belongs in the model, and forcing it there is the opposite
mistake:

| Belongs in the model | Belongs in the drawing layer |
|---|---|
| Walls, openings, rooms, levels | Dimension chains, which ones to show |
| Element phase (existing/demolished/new) | Red demolition hatch, dashed originals |
| Furniture as placed objects | Whether furniture is shown or greyed on this sheet |
| Finish assigned to each surface | The hatch pattern that represents that finish |
| Areas computed from geometry | The экспликация block layout |

That is the same rule as for layers in
[Finishes_and_Furniture_Data_Model.md](Finishes_and_Furniture_Data_Model.md):
the model holds what a thing *is*; the sheet decides what to *show*.

The one deliberate exception is the **3D массинг**: Dolgushev's album uses a
simplified grey volume rather than a render, because it sells understanding of
space rather than a picture of a finished interior. That is still generated from
the same model — a simplified *representation*, never a second model.

## Where this is not true yet — and it should be

The principle is right; the repo has not finished converging on it. Five
geometry definitions exist today:

| File | What it is | Fate |
|---|---|---|
| `data/canonical/current_apartment_base.json` | the spec the variant pipeline uses | **keep — this is the one** |
| `tools/ifc/current_apartment_layout.py` | the original hardcoded seed | retire once the spec is CAD-based; keep as the provenance record |
| `data/canonical/apartment_provisional.json` | earlier provisional model | legacy |
| `data/canonical/apartment_design.json`, `apartment_poc.json` | proof-of-concept models | legacy, demo only |
| `data/cad/wall_plan.json` | the **real** footprint from the Homestyler DXF | should become the source of `current_apartment_base.json` |

So the honest current state is: *one model per variant, but more than one
definition of the flat.* Converging them is the next piece of work — rebuild
`current_apartment_base.json` from the CAD footprint, then the hardcoded seed
and the provisional models have no reason to exist.

## The viewing setup this project uses

Fixed, so it does not have to be rediscovered:

- **2D → DWG TrueView.** Variants export to millimetre DXF with phase layers;
  TrueView's measure tool reads real dimensions.
- **3D → Blender.** Either the `.blend` produced by the repo's portable
  Blender 5.2 + Bonsai (opens in a plain Blender, no add-on), or Bonsai in your
  own Blender to get the data as well as the geometry.
- Everything else — sheets, renders, comparison — through
  `tools/drawings/build_gallery.py`.

Commands in [How_To_View_Outputs.md](How_To_View_Outputs.md).
