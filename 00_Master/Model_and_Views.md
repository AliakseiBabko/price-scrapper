# One model, many views

## The question

Are the 2D plans and the 3D volume two separate models, or one model shown two
ways?

## The answer: one model

**One model — and the source of truth is the CANONICAL AUTHORED DATA, not any
file that is generated from it.** The 2D drawings are not drawn alongside the 3D
model; both are generated from the same authored facts.

> [!IMPORTANT]
> **⚠️ CORRECTED 2026-09-16.** This section previously read *"`model.ifc` — the
> single source of truth"* and named `model_from_spec.py` as the generator. Both
> were wrong by then: that generator built from a schematic that was **retired**
> the same day, and calling a generated IFC the source of truth is the claim that
> let the 3D model diverge from the measured geometry for months without any gate
> noticing. **Canonical authored data is the source of truth. IFC is the
> authoritative GENERATED model for an issued build; drawings, quantities and
> visualisations are generated views of the same resolved model.**

```
data/canonical/            THE SOURCE OF TRUTH - authored facts + provenance
  wall_blocks.csv          lengths of record, thickness, material class
  v0_named_walls_placed.json   authoritative for POSITION and FACES
  wall_openings.csv        sills and heads, with their measurement basis
  wall_corners.csv · window_frames.csv · ventilation_shafts.csv
  building_spec.json       ceiling height
                    │
                    ▼
      RECONCILIATION - chain closure, corner ownership, placement
      yielding, loggia closure.  ⚠️ Currently trapped inside
      tools/layout/export_v0_dxf.py; should become a shared
      geometry compiler that every consumer reads.
                    │
                    ▼
             the resolved model - generated, never authored
                    │
   ┌────────────────┼─────────────────┬──────────────────┐
   ▼                ▼                 ▼                  ▼
model.ifc        DXF plan         Blender / glb      quantities
(the issued      + A3 sheets      + Cycles renders   (areas, finishes)
 representation) 2D               3D                 non-graphic
```

⚠️ **`model_from_dxf.py` reads the DXF for coordinates today.** That makes 2D an
intermediate for 3D, which is the wrong shape and is recorded as transitional:
it was the right recovery step because the 3D immediately inherited four
existing gates. Both exporters should end up consuming the same resolved
geometry, keeping independent DXF and IFC gates.

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

## ⚠️⚠️ The PHOTOREAL view — engine settled, and what it costs (researched 2026-09-16)

**The walkable view answers "does this space work". A photoreal view answers "what
will it look like" — tile, wallpaper, stretch ceiling, lighting, furniture.
Different branch, same model.** 18 sources triaged in
[[_Inbox/planning/blender_render_triage_20260916|the rendering triage]].

- **⚠️⚠️ ENGINE: Cycles, and not as a compromise.** Every advantage V-Ray and Octane
  are credited with — a native frame buffer, image history, ready-made artist
  nodes — is an **interactive-GUI** advantage, and is worth nothing when renders
  are launched **headless from a script**. ⚠️ **Octane's free tier needs an ACTIVE
  INTERNET CONNECTION and a separate licence server, and ships as a Blender
  FORK** — hostile to the pinned Blender 5.2 this repo carries. ⚠️ **V-Ray is paid,
  and a paying V-Ray user argues against buying it for Blender on ecosystem
  grounds**: almost the entire community is on Cycles and EEVEE, so the answers do
  not exist. **EEVEE is the preview, not the alternative — it shares Cycles' node
  graph, so it previews the exact materials you will render.** [source: [[_Sources/YT_BifyAj9KpaI_blender_render_engine_choice|YT_BifyAj9KpaI]]]
- **⚠️ RENDER TIME IS NOT THE OBSTACLE**: interior stills in **under five minutes on
  a single GPU**, and a scene that once took 8 hours took **15 minutes** on a
  GTX 1070 laptop. **Setup time is the real axis — and setup time is exactly what a
  SCRIPT amortises.** [source: [[_Sources/YT_1IdW1-Gtoao_blender_archviz_course_method|YT_1IdW1-Gtoao]]]
- **⚠️⚠️ LIGHT GROUPS change the answer to "let me see options".** Lamps, emissive
  objects and the environment can each be assigned to a named group, rendered as
  separate passes, and then **recoloured and rebalanced after the render is
  finished**. **Render once; explore warm-vs-cool or lamps-on-vs-off in
  compositing, not by re-rendering.** [source: [[_Sources/YT_1IdW1-Gtoao_blender_archviz_course_method|YT_1IdW1-Gtoao]]]
- **⚠️ THE INTERIOR RECIPE IS SPECIFIC and worth keeping**: light **portals** fitted
  to window openings; the **glass-shadow trick** — Blender's glass shader blocks
  light by default, so mix Glass with Transparent driven by
  `Light Path → Is Shadow Ray`, and raise transparency bounces to about 24;
  **Cryptomatte-masked selective denoising** so walls denoise hard and fabric
  gently; clamp indirect to 3–5 and never clamp direct. **Lighting: AgX view
  transform, sun as key softened to about 30 degrees, sky texture as fill, and
  artificial light as accent with a BLACKBODY colour temperature rather than an
  RGB swatch.** [source: [[_Sources/YT_BifyAj9KpaI_blender_render_engine_choice|YT_BifyAj9KpaI]]]

> **→ ⚠️⚠️ AND THE UV COST IS NOW CONFIRMED A THIRD TIME, with the per-surface
> procedure: textured surfaces need UV maps, and an IFC model has none.** **But
> with a licence attached that changes the economics** — the course author, on the
> finish this flat has most of: white plaster walls and ceilings can be *"just a
> very simple white material, and to be honest with you, that could actually do
> the trick"*, with bump and micro-reflection as refinement rather than
> requirement.
>
> **→ SO SPEND THE UV WORK WHERE IT SHOWS — tile, wood, stone — and leave plaster
> flat.** [source: [[_Sources/YT_1IdW1-Gtoao_blender_archviz_course_method|YT_1IdW1-Gtoao]]]

> [!WARNING]
> **⚠️⚠️ THE ARCHITECTURE CAUTION SURVIVES ALL OF THIS, and the material tutorials
> sharpen it.** Every source authors materials **by hand, in a GUI**. **Do that here
> and the `.blend` becomes a second source of truth that drifts from
> `finish_schedule.json` — exactly what this page exists to prevent.** **The
> standing proposal is to drive materials from the finish schedule in code, so a
> finish change is a RE-RUN rather than a re-decoration.**
>
> ⚠️ **Stated plainly: NONE of the 18 sources shows a scripted archviz pipeline.
> They support the ingredients, not the shape. The shape is this project's own.**

### ✅ BUILT 2026-09-16 — the proposal is no longer a proposal

`tools/blender/render_room.py` renders one room in Cycles with its wall finish
read from the finish schedule. Same shape as `export_glb.py`: a Python file run
by `blender --background --python`, writing a PNG and a JSON report, editing
nothing. **A finish change is now a re-run.**

**The split that keeps it honest.** `data/canonical/finish_schedule_*.json` stays
a COSTING artefact — trade, material, unit rate. Appearance lives in
`data/canonical/render_appearance.json`, keyed by the schedule's own `material`
string. **Neither file grew a second job**, and an unmatched material string is
reported rather than silently painted.

**Rooms are mapped to surfaces by the model's own `IfcRelSpaceBoundary`** — 40 of
them in v0-existing — not by guessing geometry.

**Four things the first runs got wrong, kept because each is a rule:**

1. **The `IfcSpace` is a flat PLATE** (measured Z span 0.02 m). Taking room
   height from it put the camera 8 cm **below the floor**. Height comes from the
   bounding walls, which carry the real 0–2.5 m.
2. **The camera faced away from the only window** and the room rendered as a dark
   blue box. It now aims at the opening, which is both the lighting-correct and
   the compositionally standard choice. **The sun is aimed through that same
   window** rather than at a fixed compass bearing — a hard-coded azimuth is a
   coin flip, and a wrong one puts the only opening in shadow.
3. **The windowless Bathroom rendered PURE BLACK** — physically correct and
   useless. Sun and sky cannot enter a room with no opening. A ceiling luminaire
   is now always added, coloured by **blackbody kelvin, not an RGB swatch**.
4. **A flat 75 W calibrated on the 16.9 m² bedroom blew out the 3.1 m² bathroom.**
   Power is per m². **Any lighting figure calibrated in one room is wrong in
   every other one** unless it is stated per unit area.

> ⚠️⚠️ **WHAT IT IS NOT.** It is a **lighting study, not a daylight study**: it
> shows how a room reads when sun comes through that window, and says nothing
> about whether the sun is ever in that position at this site on any date.
> **Untextured by construction** — roughness, not pattern, is what separates tile
> from paint here. **A wall bounds two rooms but is one object**, so its far side
> carries this room's finish; invisible from inside, wrong for any exterior view.
> **A room under ~6 m² cannot be photographed from inside itself** — the bathroom
> needs a 12 mm lens and still shows only a corner; the walkable view is the
> better tool for those. Every run writes these limits into its own report, so a
> render cannot be mistaken for a finished visualisation.

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

---

## ⚠️⚠️ Is 3D MEP worth modelling, or is a 2D overlay the real answer? (2026-09-17)

**The question arose because one source appeared to settle it.** Lloyd Sark (IfcArchitect), in `RL3IAGeMi5s`, reports that **Bonsai's native MEP is broken** — *"there's a few issues with the system flow… when you do pipes, when you do connections, when you do HVAC"* — and that practitioners therefore cut the architectural plan and **draft 2D annotations as an overlay**: *"the drawing becomes a stop gap."*

**Two Russian practitioners contradict the conclusion while agreeing with the fact.**

| | Practice | Tool |
| :--- | :--- | :--- |
| Алексей Дубровин, `kxJ9R3gQjKw` | electrics **and now plumbing** modelled in 3D as normal commercial work; all clients order it; all work executed to the 3D project | unnamed 3D modeller |
| LOFT DIY, `0T97_CA7hgo` | wiring modelled in 3D, organised by **layer and group**, lengths read off by selecting the group | SketchUp |
| Алексей Шемчук, `0c-QhBDQMWE` +4 | *«В модели выполняется вся работа таким образом, как она потом будет выполняться на объекте»* — cable types colour-coded in the model, routes chosen against the other trades, a per-cable schedule with start, end and **length** | unnamed 3D modeller |

### ⚠️ THE RECONCILIATION — and it is the useful part

> **Sark's complaint is about the SYSTEM layer. The benefits the others report come from the GEOMETRY layer.**

*System flow*, port-to-port connectivity and `IfcDistributionPort` are the semantic network. **Everything the three practitioners actually gain is obtainable from the physical run alone** — a cable of a stated type, on a stated path, at a stated height, in a chase of measurable length:

- **coordination against other trades**, decided in the model rather than on site;
- **quantities by selection**, including ⚠️⚠️ **chase length — a priced LABOUR item**: Дубровин selects the chases and reads *«67 с лишним метров»*;
- **as-built documentation** handed to following trades so they know *«где сверлить можно, где сверлить нельзя»*, which transfers cable-strike liability;
- **installation schematics** that cut fitting time and errors.

**→ ⚠️ THE 2D-OVERLAY FALLBACK IS EVIDENCE ABOUT ONE AUTHORING APPLICATION, NOT ABOUT WHETHER THE GEOMETRY IS WORTH HAVING.** It is a labour-saving retreat in a hand-modelling workflow; a pipeline that GENERATES geometry from canonical data does not pay that labour, so the reason for the retreat does not transfer.

**What does transfer is the narrower warning**: the connectivity layer is where practitioners report Bonsai misbehaving. Modelling runs as geometry while keeping circuit membership as authored data — rather than relying on port semantics — takes the benefits and avoids the reported failure.

⚠️ **Standing rule 3 caveat:** Дубровин sells 3D design as a service, and offers no measured comparison against 2D practice. The benefits are specific and plausible; they are not independently verified.

### ⚠️⚠️ The method, in order — and the step we have never done

Алексей Дубровин's four method videos (`wbUm7i-nHHk` +3) give the sequence: **survey → primary 3D model → furniture → services**. Шемчук states the same order independently.

**The survey list is the part we lack.** He records walls, openings, **floor level changes**, ⚠️ **wall composition** (*«состав стен — там, где несущие бетонные»*), existing penetrations, riser and stack positions, the developer's original heating runs — and locates ⚠️⚠️ **in-screed heating pipes by THERMAL IMAGING**, marking turns and tees.

> **→ ⚠️⚠️ WE HAVE NEVER DONE THIS.** `photo_positions.csv` holds one photograph of our unit and it is an exterior elevation. `project_decisions.md` records horizontal heating distribution with heat meters already installed — **and we do not know where those pipes run.** Thermal imaging is a directly applicable technique, not a general recommendation.

**Two design findings that settle open questions:**

1. ⚠️ **The circuit list is authored INPUT, not derived geometry** — *«состав групповых линий — это то, что задаёт, как электрика будет проходить по дому»*. A circuit carries designation, description, breaker rating, cable cross-section, RCD/RCBO and phase. The count of lighting circuits is governed by **inrush**, not steady load: an LED driver trips a breaker that the running current would never reach. **No geometry produces that**, which is why the list precedes the tracing.
2. ⚠️ **The board gets TWO views of one thing** — a single-line schematic and a physical DIN-rail layout at real module sizes — and the layout **deliberately omits** the outgoing line cables, labelling them instead. A precedent for our own view model, including the principle that a view may legitimately drop detail.

**Routing method is chosen from wall material and the ceiling build-up plan**, which is this project's substrate rule and the owner's ceiling-distribution topology reached independently.

⚠️ Open questions arising: `_Inbox/planning/mep_3d_open_questions_20260917.md`. The highest-value unknown is **how a chase is represented so its length is selectable** — Дубровин reads *«67 с лишним метров»* off the model, and chase length is priced LABOUR.
