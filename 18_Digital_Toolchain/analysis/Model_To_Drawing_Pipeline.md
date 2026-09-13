# Model to drawing — how a BIM model becomes a sheet, and where the association leaks

**How practitioners get an annotated drawing out of a 3D model**, what the model has to carry for that to work, and the ways the result is silently wrong.

> [!IMPORTANT]
> **This page exists because the decision it informs is already taken.** [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md) §Kind 3 marks **Bonsai's drawings subsystem `Adopt`** for annotated sheets — *"we need to start using the parts we have"* — against our hand-rolled SVG→PDF, on the grounds that hand-rolling *"fails exactly here: dimension chains collide on dense MEP plans."*
>
> **Everything below is evidence bearing on that adoption and on its one stated open question**: whether the drawing subsystem is usable headless, or whether annotated sheets must be a GUI step.
>
> ⚠️ **Read for mechanism, not as a tool recommendation.** Every UI path in the underlying sources is discarded as dated — the add-on was renamed from BlenderBIM to Bonsai and its UI overhauled between the sources cited here.

## 1. ⚠️⚠️ The dividing line: a drawing that is GENERATED versus a drawing that is EXPORTED

**Two complete routes to the same annotated floor plan appear in the same batch, and they differ on the only axis that matters.**

**The mesh route** (Ruben Messerschmidt, 2024): a section box cuts the model, the cross-sections and elevations are **exported as meshes** into their own collection, dimensioned with an annotation add-on, and rendered to SVG through a camera with a paper size.

**The BIM route** (Ifc Architect, 2022; Prof Rino, 2025): a camera is placed on a storey and **`create drawing`** produces the plan **from the model**. Correcting a window means moving it in the model and regenerating.

> *"It's **similar to AutoCAD in that you have to print the end result**."* — Ifc Architect. He moves two windows from the inner to the outer wall face, regenerates, *"and you can see the windows have moved — it's as straightforward as that."*

> **→ ⚠️⚠️ IN THE MESH ROUTE THE DRAWING IS PERMANENTLY DETACHED FROM THE MODEL. A dimension on an exported mesh cannot know its model changed.**
>
> **This is the same defect the 2026-09-11 round found spanning three unrelated AI tools — *generated geometry is PLACED, NOT ASSOCIATED* — arriving now in the drawing layer instead of the geometry layer.** And the conclusion recorded then applies unchanged: **the difference is not capability, it is whether anything maintains the constraint.**
>
> **This is the gap analysis's `Adopt` verdict vindicated**, and on a better ground than the one it was argued from. The original case was about *annotation quality*. **The stronger case is association**: a generated drawing is a view of the model, an exported one is a copy of it, and this project's whole discipline is built on not keeping two copies of the same fact. [source: [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|YT_PNoOyCHa_V0]], [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YT_YYmFMxMV6io]]]

### ⚠️ But the association is not free, and it is not automatic

Both BIM-route practitioners re-synchronise by hand, three years apart:

- *"I like to just **update representation** every now and then to make sure that it's all updating."* — Ifc Architect, 2022
- On raising a wall from 2 m to 3 m: *"press two. **Nothing's going to happen because you need to REFRESH**."* — Prof Rino, 2025

## 2. ⚠️⚠️ Four places the parametric association leaks — and what they mean for a headless build

**Prof Rino hits all four inside one 24-minute beginner tutorial, and treats each as a normal quirk. Collected, they reframe the open question.**

| # | What breaks | His fix |
| :--- | :--- | :--- |
| a | **Moving a door does not move its opening** — *"the movement has been working, but the opening is not there inside the wall"* | `shift G` |
| b | **A parameter change does not take effect** until explicitly refreshed | refresh |
| c | **Flipping a door's swing DISPLACES the door** — *"the door is not really well defined parametrically. He has been changing the position"* | grab, choose a base, re-place by hand |
| d | **Converting to parametric geometry loses the element's materials** | re-assign |

> **→ ⚠️⚠️ EACH OF THESE IS A MANUAL GESTURE THAT RE-ESTABLISHES CONSISTENCY. A HEADLESS SCRIPT MUST KNOW TO MAKE EVERY ONE OF THEM.**
>
> **And a missed one does not produce an error.** It produces a valid-looking IFC with a door whose opening is somewhere else. **That is the worst failure shape there is** — the class `00_Master/Validator_Design_Discipline.md` exists to catch.
>
> **→ The gap analysis's open item should be restated.** Not *"is the drawing subsystem stable headless"* but: **"which re-synchronisation steps does the GUI perform that a headless script must call explicitly, and what gates the result?"**
>
> **→ And it argues for a gate BEFORE the adoption**: an IFC-level check that every opening coincides with its hosted element, before any Bonsai-touched file enters the deliverable. **That check does not exist today.** [source: [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|YT_fxpIg-su-00]]]

## 3. ⚠️⚠️ Silent-failure modes of a generated drawing

**Collected across both routes. In every case the export succeeds and the sheet is wrong.**

**(a) Edges below an angle threshold are dropped.** *"It didn't take all the edges into account… because these edges have a very low angle. Simply increase the crease angle — 175° should be fine."* The omission is a function of a parameter, so it is **systematic**: every near-coplanar edge disappears from every sheet. ⚠️ Raising the threshold costs time — *"this takes even longer because more edges means more calculations"* — which is the pressure that keeps people on a lossy default.

**(b) The drawing's own geometry is not exported unless a line group exists.** *"If we would export everything now, **we would only see the dimensions**… **Actually it looks like nothing happened**"* when the enabling step is performed. **A sheet of dimension strings floating over nothing**, and the fix gives no visible feedback.

**(c) DXF export has acknowledged, unquantified scaling issues.** *"Be aware of some **scaling issues** that might happen… check out the documentation where they go in detail about how to fix these issues."*
> **⚠️⚠️ DISQUALIFYING FOR THIS PROJECT, not merely a caution.** Every gate here is dimensional — `check_dxf_closure.py` asserts drawn length and thickness against the record *and* against the PDF's hatched solids. **A route whose own documentation has a section on fixing its scaling cannot carry a deliverable.**

**(d) A schema upgrade that reports success may not convert the content.** A downloaded IFC2x3 door is auto-upgraded to IFC4 — *"Bonsai will be nice enough to upgrade the file for us"* — and then **does not appear under the door tool**, because it is still an `IfcDoorStyle` (the IFC2x3 entity) rather than an `IfcDoorType` (its IFC4 replacement). **The header says IFC4; the contents are semantically a door that no door tool can see.**
> **→ ⚠️ This is a concrete, checkable rule for the IDS validation the gap analysis already marked `Adopt`**: assert every element resolves to an IFC4 type entity, refuse a deprecated `*Style` survivor. ⚠️ The entity-class reading is this vault's interpretation of the observed symptom, not the presenter's claim — **reproduce before relying on it.**

[sources: [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YT_YYmFMxMV6io]], [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|YT_4JYFYvNg5Xk]]]

## 4. ⚠️ Text collision is manual in a purpose-built tool too — which qualifies the adopt decision

**The gap analysis's stated reason for adopting Bonsai is that hand-rolling fails on dimension-chain collisions and text overlaps. A dedicated annotation add-on has the same problem, fixed one dimension at a time:**

- A dimension whose arrows point inwards — located by hiding list entries one by one, then `tweak distance = −1` to flip it out.
- A dimension too narrow for its text — *"it gets blind outside"* — fixed by setting that one dimension's alignment to left.
- **Defaults unusable at building scale**: font size raised to 30, line weight to 2, arrow size to 30, *"it's way too thin and the font is way too small."*

> **→ ADOPTING A TOOL DOES NOT SOLVE TEXT COLLISION; IT RELOCATES IT.**

### ⚠️⚠️ ANSWERED: Bonsai does not place dimensions either — there is no auto-dimension at all

**The question left open above was *"does Bonsai place dimension text without per-instance intervention?"* Three sources from the specialist channel answer it: no.**

**A dimension in Bonsai is a polyline the user snaps vertex by vertex.** There is no "dimension this wall" command:

> *"We're going to select **dimension**… **you can see it adds in as a POLYLINE CURVE**… change it to **edit mode**, and this allows me to **edit the vertices directly**… `GY` to snap it to the bottom… `E` to extend this dimension line."*

He then composes the whole dimension set by hand over some four minutes. **And the collisions are fixed the same way as everywhere else** — a long specification leader overruns and the fix is to shrink the font to 1.5.

> **→ ⚠️⚠️ THREE INDEPENDENT INSTANCES ACROSS TWO TOOLS AND TWO PRESENTERS. NOTHING IN THIS MATERIAL SOLVES TEXT PLACEMENT.**
>
> **The gap analysis's stated rationale for `Adopt` does not survive.** It marks the drawings subsystem `Adopt` **specifically because** hand-rolling fails on *"dimension chains colliding on dense MEP plans; excessive custom code required to handle text overlaps."* **Bonsai does not solve that. It gives it to the human.**
>
> **⚠️⚠️ And the inversion is the point.** Our SVG pipeline generates from `data/canonical/`, where **every wall's length, thickness and position is already a number**. A script emitting a three-tier dimension chain at computed offsets is **not "excessive custom code" — it is a loop over data we already hold**, for one apartment with fixed geometry. **Hand-snapping in a GUI is the thing that does not survive a re-run.**
>
> **→ For DIMENSIONS specifically, the generative route is the better one, and the premise behind the `Adopt` verdict should be corrected.** ⚠️ This does **not** overturn `Adopt` for the rest of the subsystem — see §4b, §5, §10. [sources: [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|YT_VgvPk78IU0U]], [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|YT_QTviOpqz1rw]]]

### ⚠️⚠️ 4b. …but TAGS are bulk-placed and data-bound, and that is where the real value sits

**The opposite of dimensions, in the same tool:**

- **`bulk tag`** places one tag per selected object in a single command, each already related to its object — *"we've added in a tag for each space that **already has a relationship aligned with that space**… it's grabbing the names."*
- **A tag's text is a TEMPLATE resolved against the bound object**: a `product assignments` relationship plus **`{{ }}` placeholders**. Binding a leader to a column and writing `{{name}}` makes it read *"column"*, live.
- **⚠️⚠️ The TEMPLATE is type-level; the DATA is instance-level.** Appending a unit to one space tag changed every tag using that type, **and each still rendered its own object's values** — *"office / timber / 9.41 m²"* beside the bathroom's own.

> **→ ⚠️⚠️ THE ONLY UNAMBIGUOUSLY GOOD INSTANCE OF TYPE-LEVEL SEMANTICS IN THIS MATERIAL.** §5 records type edits as a hazard with a silent wide blast radius; **here the blast radius is the feature, and what makes it safe is that the TEMPLATE is shared while the VALUE is not.**
>
> **⚠️⚠️ It also answers a question this vault recorded as untested.** [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §1 asks *"whether our own DXF/SVG pipeline can express a proportional dimension (`1/2`) at all, or whether it needs Bonsai's annotation subsystem."* **An annotation whose content is a template over model attributes can trivially carry a literal `1/2`** — and the general mechanism matters more: **the annotation is DERIVED from the model, not transcribed beside it.**
>
> **→ And it needs no Bonsai. A template-substitution pass over an SVG is a string operation.** The same `{{ }}` binding drives the **title blocks** (§10). **We can do this; we have not.**

**⚠️ The one thing worth copying regardless: a NAMED STYLE SET.** Dimension style and line style are separate scene-level objects, and every annotation references one — so a single edit restyles everything using it. **If our SVG pipeline keeps the annotated sheets, this is the abstraction it should have**: one style object, not per-element attributes. And **annotation defaults are authored for object scale, not building scale** — there is no usable default; every generated sheet needs an explicit style pass. [source: [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YT_YYmFMxMV6io]]]

## 5. What the model must carry for a drawing to come out of it

### ⚠️⚠️ A plan symbol is AUTHORED, not derived by cutting the geometry

> *"If I want to see **how the shower actually looks when it's cut**, I can go into object properties → geometry → representations and turn on the **plan representation**, so we can see **where the drain is**."*

**A drain does not appear in a section through a shower tray. It appears because the SYMBOL has one.** Each IFC object carries a 2D plan representation distinct from its 3D geometry, and the practitioner works almost entirely in that view, rotating each fixture's symbol into place.

> **→ THIS IS A CAPABILITY OUR HAND-ROLLED SVG PIPELINE DOES NOT HAVE**, because it can only draw what it can compute from geometry. **A large part of what "adopting the drawings subsystem" would buy is this symbol library**, not the annotation engine. [source: [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|YT_PNoOyCHa_V0]]]

### ⚠️⚠️ The unit of change is the TYPE, and a type edit has a silent wide blast radius

Two presenters, three years apart, independently:

> *"I'm going to mirror along the Y global… **and you see that's changed ALL the doors, because they're the same type.**"* — Ifc Architect
> *"Whatever we apply for this door, **because they belong to the same IFC door class, is going to be modified for both of them.**"* — Prof Rino

**The remedy is to DUPLICATE THE TYPE** — *"call this IFC new class of door type two"* — then place an instance of the new one. **Materials behave identically.** An instance-level override exists but is reached only by a different selection mode: *tabbing into* the object rather than selecting it.

> **→ ⚠️⚠️ AN EDIT WHOSE SCOPE IS IMPLICIT IN A MODAL SELECTION STATE.** He noticed because the change was visible; on a dense plan it would not be.
>
> **→ Supports the gap analysis's "Keep programmatic" verdict directly.** A type is a named object in code, and the blast radius of an edit is visible in the diff. **It also means every genuinely different door in this flat needs its own type** — a modelling decision with a schedule consequence, since schedules group by type. [sources: [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|YT_PNoOyCHa_V0]], [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|YT_fxpIg-su-00]]]

### An object is in the model because it carries a CLASS, not because it is in the scene

A plain mesh becomes a BIM object only when an IFC class is assigned to it. **The same mechanism appears once as a feature and once as a trap**: deliberately-unclassified drafting lines are used to draw a kitchen countertop and built-in cupboards — *"we're not going to model it per se"* — and **anything drafted-only is invisible to quantity take-off.** ⚠️ **Joinery is exactly the class of item this hides, and it is not cheap.**

## 6. ⚠️⚠️ The IFC is the master; the `.blend` is a cache that holds geometry but not data

**Established by the only controlled experiment in four batches of this material** — two objects differing in exactly one property, saved four ways with a restart between each:

| Condition | Outcome |
| :--- | :--- |
| Save IFC → reopen IFC | the classified object survives; **the plain Blender object is gone** |
| Save `.blend` → reopen | **both** survive |
| Delete the `.blend` → open the IFC | *"the IFC exists on its own, with the geometry AND IFC data"* |
| **Delete the IFC → open the `.blend`** | *"the geometry is still there, but **the IFC data is LOST**"* |

> **→ THE `.blend` CONTAINS GEOMETRY PLUS A LINK TO THE IFC THAT HOLDS THE DATA.** Break the link and you have a mesh.
>
> **This validates the architecture this project already has** — IFC authored programmatically as master, Blender as viewer — and says **nothing is lost by our not keeping `.blend` files at all.** The `.blend` is only needed for state that is legitimately not part of the building: lighting, cameras, render setup. **For us that is the `build_apartment_demo.py` render path and nothing else.**

### ⚠️⚠️ And the hazard that follows: the two files are LINKED, so `Ctrl+S` writes to the IFC

> *"**The shortcut for saving IFC project or saving Blender project is the same.** So once they are connected, once you hit **Ctrl+S** — or just go simple save — **BOTH the blend file and the IFC file are saved.**"*

> **→ ⚠️⚠️ THIS IS A LIVE HAZARD IN OUR OWN INSTRUCTIONS, not a general observation.** `00_Master/How_To_View_Outputs.md` tells the owner to open the project IFC in Blender with Bonsai in order to **look** at it. **A reflexive `Ctrl+S` in that session rewrites the deliverable**, and Blender users press it constantly.
>
> **And our gates would not catch it**: `check_dxf_closure.py` and `raster_fidelity.py` assert the **DXF** against the canonical data and the source PDF. **A mutated IFC that nothing re-derives from is checked by neither.** → **Open item, and cheap to close** — open the IFC read-only for viewing, or **hash the project IFC and assert it in the batch gate**. The second is the same frozen-artefact pattern already used for the ink mask, the registration and the archived transcripts.
>
> ⚠️ **The experiment tests PERSISTENCE, not FIDELITY.** It shows the data survives a round trip; it does not show geometry, property sets or **GUIDs** come back unchanged. **A silent lossy round trip would pass every condition run.** Recorded as untested, not as safe. [source: [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|YT_tAq0foY2GOY]]]

## 7. Sheet mechanics worth keeping

- **⚠️ A sheet is a camera with an EXTENT and a LOCATION**, and there is no fit-to-content default — a new plan camera arrives at **50 m × 50 m**, *"definitely too big for us"*, rescaled by hand to ~20 × 10 and dragged to centre the building. **For a headless build this is a virtue: extent and origin should come from the canonical data, not from where someone dragged a box.**
- **⚠️ The drawing subsystem refuses to run on an unsaved project** — it *"complains because the project has not been saved."* **The generator reads the IFC FILE, not the in-memory session** — mildly encouraging for the headless question, since a subsystem that reads from disk is one a script can feed.
- **The drawing lives in its own collection**, with the model and section boxes hidden. **The drawing is a separate artefact from the model, not a view of it** — which is the mesh route's weakness restated (§1).
- **A type library is itself an IFC file**, attached at project level. ⚠️ A shape that suits us: diffable, hashable, gated like anything else.

## 8. ⚠️ The default type library is thin — but it does NOT constrain you

**Three sources, same complaint**: the demo template ships **one door**, one window, and slabs in **200 and 300 only**. Everything else comes from duplicating and editing a type.

> ⚠️ **And a practitioner accepts a dimensional consequence without comment**: *"we're going to select the **200 wall, because that's similar to a masonry brick wall of 220**."* **A 20 mm type error, taken because the library has no 220.**

### ⚠️⚠️ CORRECTED: authoring an exact thickness is a five-minute task, and the worked example is literally 220

**This page previously inferred from the above that *"a type-library workflow trades dimensional fidelity for schedulability."* That inference was wrong, and the correction comes from the same presenter using the same number.**

He builds a wall type from scratch: an empty → **`IfcWallType`** → an **`IfcMaterialLayerSet`** (*"a set of materials **including a thickness**"*) → layer set name `double brick` → **thickness `220`** → saved as a standalone `.ifc` in his own library folder.

> **→ THE LIBRARY SHIPS COARSE DEFAULTS; IT DOES NOT LIMIT YOU TO THEM. The type system is exactly as precise as the number you type.**
>
> **The correction matters here specifically**: our walls carry exact `clear_mm`, and the retired inference implied a type-based workflow would cost that. **It would not.**
>
> ⚠️ **What survives is weaker and still true**: *the nearest stock type is the path of least resistance*, and a practitioner under no dimensional pressure takes it. **That is a discipline risk, not a tool limitation** — which is what gates are for.
>
> **⚠️ And thickness is a TYPE property**: retyping a 300 wall to the 220 type *"has changed the thickness of the wall to 220."* Geometry follows the type — **a clean association, and the opposite of the placed-not-associated defect in §2.** It also means a distinct thickness needs a distinct type, which **multiplies against the type-per-phase pattern in §11.** [source: [[_Sources/YT_jTL3a6QwckA_ifcarchitect_custom_wall_type|YT_jTL3a6QwckA]]]
>
> **⚠️ `IfcMaterialLayerSet` is the native construct for a LAYERED build-up** — several materials each with a thickness. **Currently unused here**: our walls are single-material solids, but a real renovation wall is block + plaster + finish, and **the layer set is where a finish schedule and per-layer quantities would come from.**

## ⚠️⚠️ 10. THE ARCHITECTURE: the drawings and sheets are SVG, styled by CSS

**Established by four independent tells across three sources, two of them naming the files outright.**

| Evidence | Source |
| :--- | :--- |
| A generated drawing **opens in a browser** — *"it's going to ask you what should we open it with. You can use any browser."* | Pt 2 |
| The sheets are **`.svg` files in a known directory**, opened in **Inkscape**; final export is **SVG → PDF** | Page layout |
| Per-drawing element filtering uses a **CSS attribute selector** (§11) | Page layout |
| **The stylesheet is a literal `.css` file** the user edits in Notepad — *"custom line weights, line styles and hatch patterns — **using CSS**"* | Lineweights |

> **→ ⚠️⚠️ BONSAI'S OUTPUT FORMAT IS OUR OUTPUT FORMAT. Our pipeline is SVG→PDF; so is this.**
>
> **This corrects the architecture the gap analysis proposed.** It concluded *"keep our SVG pipeline for the diagrammatic sheets… put Bonsai behind the sheets that need dimension chains, tags and schedules. **Two engines, split by whether the sheet is annotated.**"* **There are not two incompatible engines — there is one artefact two tools can write.** Which makes a shared stylesheet, shared PDF post-processing, or lifting the conventions into our own generator all live options.

### The styling taxonomy, and it is the right one to copy

The stylesheet is organised by **the element's ROLE IN THE VIEW**, not by element class: **`cut`**, **`projection`**, **`text`**, **`annotation`**, user-extensible **predefined types**, and **`material`** (*"a 3D element that references a 2D pattern"*). Demonstrated: setting `text` blue and `cut` red turns wall cut lines red and text blue **while symbols and annotations are untouched.**

> **→ ⚠️⚠️ CUT vs PROJECTION IS FIRST-CLASS, AND IT IS THE FUNDAMENTAL DISTINCTION IN ARCHITECTURAL DRAWING** — what is cut is heavy and poché'd, what is beyond is light. **Our generator should be organised the same way: style by role in the view, plus material for fill.** **The most directly copyable design in the round, and it needs no Bonsai.**

### ⚠️ The "magic strings" are CSS class names

`brick`, `concrete`, `earth`, `SEALANT`, and any name you invent are **classes defined in that stylesheet** — user-extensible, and documented in the file itself. **The casing inconsistency is an artefact of the shipped default, not a convention.**

> ⚠️ **What remains true and matters: nothing validates that a name typed into an attribute matches a class that exists.** A typo yields **no hatch and no error**. **And a hatch needs TWO registrations in TWO files** — an SVG `<pattern>` and a matching CSS `material` rule — **define one without the other and you get nothing.** **Together with the `IfcDoorStyle` survivor, these are the concrete rules for the IDS validation the gap analysis already marked `Adopt`.**

### ⚠️⚠️ The scoping is inconsistent, and it is close to disqualifying on our own terms

| Artefact | Lives | |
| :--- | :--- | :--- |
| **Stylesheet** | **beside the IFC**, referenced per drawing | ✅ project-local |
| **Hatch patterns, markers, symbols, view titles, title blocks** | **inside the application install** | ⚠️ version-global, *"you will LOSE your custom title block"* on reinstall |
| **Type libraries** | a user-owned folder of `.ifc` files | ✅ git-trackable |

> **→ ⚠️⚠️ FOUR OF THE FIVE STYLING ARTEFACTS LIVE IN `AppData/Roaming`, NOT WITH THE PROJECT.** Every gate in this repo rests on artefacts being committed, hashed and diffable. **A deliverable whose appearance depends on an application install directory is not reproducible**, and a rebuild elsewhere would silently produce differently-styled sheets. **→ If any of this is adopted, the styling artefacts must be copied into the repo and installed by the build, never edited in situ.** [sources: [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|YT_dPWQbjaeoyo]], [[_Sources/YT__vrVETTI5jQ_ifcarchitect_custom_titleblock|YT__vrVETTI5jQ]]]

## ⚠️⚠️ 11. Sheet content is a QUERY, and a phase drawing is a filter

**Two instances of the same mechanism — a selector stored as a property set on the drawing's camera:**

- **Exclude one object**: `.IfcGeographicElement[name="site"]` drops the terrain from one drawing and not others.
- **⚠️⚠️ Exclude a whole phase**: a filter over `Pset_*Common.Status = "new"` hides everything new, **and *"we've got essentially a DEMOLITION PLAN which shows the existing and what will be demolished"*** — from the same model that produced the general-arrangement plan.

> **→ ⚠️⚠️ ONE MODEL, MANY SHEETS, GENERATED BY A DECLARATIVE QUERY. And this is a better implementation of a convention this vault already holds.** [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §3 records *a services sheet has two audiences and therefore two configurations*, observed as **layer toggles**. **A query beats a layer on every axis**: it reads the model's own data instead of a parallel taxonomy nobody maintains, and **a sheet's content becomes a stated rule that can be committed and diffed rather than a remembered click.**
>
> **⚠️ Directly actionable for our own phase sheets.** `data/cad/` exports **existing / demolished / new as DXF layers**; the IFC-native equivalent is **`Pset_<Class>Common.Status`** with values `existing` / `demolish` / `new` — **the same three phases, as a standard property on the element.** That is strictly better than a layer, and `IfcOpenShell` can write it. ⚠️ **The failure mode is silence: a selector with a typo excludes nothing and reports nothing** — so the gate is *assert the filter matched something.*
>
> **⚠️⚠️ But do NOT copy his pattern of putting the status on the TYPE.** He creates `wall 100 existing`, `wall 100 demo`, `wall 100 new`, and changes an element's phase by reassigning its type. **Phase is a property of this particular wall, not of what kind of wall it is** — and since thickness is *also* a type property (§8), **the library grows as the product of thicknesses and phases.** He half-admits it: *"in the future it's most likely going to work a bit better."* **Set `Status` per instance; we author programmatically, so "inherited automatically" costs us nothing — it is a column in a CSV.**
>
> ⚠️ **The pattern breaks for spaces**: `Pset_SpaceCommon` **has no Status field**, and the fallback is a **BlenderBim-specific `EPset_status`** that *"doesn't show up in 2D"* and is not caught by the filter. **Second instance in this round of reaching for a vendor extension where the standard falls short** — the first being a Blender-specific quantity set preferred over `IFC4 base quantities` *"because it works a little bit better right now."* **→ Standing rule for any adoption: prefer the standard property set; if a vendor extension is used, record why and what breaks without it.** [source: [[_Sources/YT__hADRIo-ma4_ifcarchitect_custom_phases|YT__hADRIo-ma4]]]

## ⚠️⚠️ 12. Sheet ASSEMBLY is manual — and we are already better at it

Bonsai's contribution to a sheet is to dump every printed drawing onto an A3 page: *"say create sheets, and you can see **it's loaded everything onto this BEAUTIFUL MESS**."* Everything after that is drag-and-drop in Inkscape, by eye.

| | Bonsai | Our SVG pipeline |
| :--- | :--- | :--- |
| **Drawing generation** (cut, hatch, tags, symbols) | **strong** — we have nothing | weak |
| **Sheet composition** | **manual, by eye, in Inkscape** | **already programmatic** |

> **→ ⚠️⚠️ ADOPTING BONSAI'S SHEET WORKFLOW WOULD MEAN GIVING UP A CAPABILITY WE HAVE, NOT GAINING ONE.** The half worth taking is **drawing generation**. **This settles the gap analysis's open question about headless sheet assembly: the GUI route is manual, but the artefact is plain SVG, so a script can write it — which is what we already do.**
>
> **⚠️ The round trip is real and is the good part**: he arranges in Inkscape, saves, regenerates in Blender, and **the arrangement survives** — *"you can see it's been updated, isn't that amazing."* **The content is derived, the arrangement is authored, and they coexist in one file with no merge step.** That principle is worth copying regardless.
>
> ⚠️ **Three hand-finishing steps are load-bearing, not optional**: the arrangement itself; **deleting section tags he cannot suppress** (*"I just delete them afterwards in Inkscape anyway"*); and **clipping a view that renders past its boundary.** **⚠️⚠️ A clip HIDES geometry, it does not remove it** — the over-extending wall is still in the SVG and therefore in the PDF. **Specifically dangerous here, because `vector_extent_oracle.py` re-derives wall solids from a PDF's vector content**: clipped-but-present geometry is exactly what an extractor reads and a human never sees. **Never fix a rendering defect by masking it.**
>
> ⚠️ **Two export settings that matter**: *"make sure you **don't have rasterized effects checked**, and your **DPI is set at 300**"* — keep the output vector. **And the live sheet and the exported sheet are different artefacts**; anything fixed on the dead copy is lost on the next regeneration. [source: [[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|YT_HEb7fWJduXg]]]

## ⚠️⚠️ 13. One camera primitive, four sheet types — and a detail must be MODELLED

**Plan, section, elevation and detail are the same generator.** *"Essentially, it's all the same process."* They differ only in **(direction, extent, scale)**:

| | Plan | Section | Elevation | Detail |
| :--- | :--- | :--- | :--- | :--- |
| **Extent** | 10 × 8 m | 7500 | 7500 | **1000** |
| **Scale** | 1:50 | 1:100 | 1:100 | **1:10** |

> **→ `Sheet_Production_Roadmap.md` treats sheet types as separate products. They are not — one parameterised generator covers all four, and a "detail" needs no new machinery.**

**⚠️⚠️ But the detail's CONTENT does.** To produce one roof-eaves detail he drafts nothing — he **models** battens on a 50×50 profile arrayed at 300 mm, a fascia on a 20×300 profile, a 50 mm roof overhang and an `IfcCovering` ceiling.

> **→ A DETAIL SHEET IS A MODELLING TASK AT A FINER RESOLUTION, AND THE DRAWING FALLS OUT OF IT.** Our model is **nominal ±50 mm**, walls as single solids, no build-up layers and no fixings — **nothing in it can produce a construction detail.**
>
> **→ Three honest options for `Sheet_Production_Roadmap.md`, none free**: **(1)** model at detail resolution where a detail is genuinely needed, extending the gated chain to cover it; **(2)** draft details in 2D — cheap, but a drafted-only element is invisible to take-off **and an unclassified modelled object is not even drawn** (§5); **(3)** issue no details at all, which is legitimate for a fit-out where trades own their build-ups — **and the vault already has the principle: a sheet may legitimately be blank, and the album should say so.**
>
> ⚠️ **And option 2 is not really an alternative**: even his fully modelled detail needs **insulation batting, a sealant fill area, and hand-drawn lines over the battens** *"just so I know it's been cut."* **Every detail is some of both; the question is where the line sits.** ⚠️ **Flagged for the owner as a decision.** [sources: [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|YT_r0ebxigzM6U]], [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|YT_QTviOpqz1rw]]]

### ⚠️ Classification is the switch that puts an object in the drawing

A plain Blender cube is invisible to the section until it is given a class; **the moment `IfcGeographicElement`/`terrain` is assigned, *"it's now being cut by the camera view."***

> **→ An unclassified object is not saved to IFC, not scheduled, AND NOT DRAWN. Same mechanism, third consequence** — demonstrated rather than asserted. ⚠️ **A cut element's LINE WEIGHT is automatic but its FILL is not**: with no material it cuts as an empty white outline, *"technically correct and conventionally wrong."*

## 14. The dividing line between the two families of tool, stated dimensionally

**Across this batch, six sources model a floor plan. They split cleanly on one question: is a dimension an INPUT or a CONSEQUENCE?**

| | The dimension is… | Sources |
| :--- | :--- | :--- |
| **BIM / parametric route** | **an INPUT** — type `10000`, press enter; `shift E` to extend to a snap; `shift C` to close; offsets typed from a named edge | Ifc Architect, Prof Rino, CG Essentials |
| **Mesh-tracing route** | **a CONSEQUENCE** of where the mouse went, read back off an edge-length overlay | Architecture Topics ×2, SFE-Viz |

> **→ This is a sharper distinction than any feature comparison, and it decides everything downstream.** A traced wall has no length property to schedule, no type to group by, and nothing to check against. **This project is firmly on the first side and should stay there** — our walls come from `data/canonical/`, which is the same relationship one step further back.

### ⚠️⚠️ 14b. Both families lose their parameters — and our generative route escapes the trade-off entirely

**The mesh route is parametric too, until you BAKE.** Before applying the `Solidify` modifier, the practitioner stops and warns:

> *"Just make sure that you don't have any changes to the floor plan, because after this point… **we're now committing to this geometry**. The geometry created by the Solidify Modifier **doesn't have vertices, it is being dynamically calculated.** But after we commit, **all of this will become real geometry and there is no way back.**"*

**And he must commit, because until he does, inside and outside are the same surface** — *"we would apply the same material on the outside than on the inside."* His summary: **"full control over our walls AT THE COST OF FLEXIBILITY."**

> **→ ⚠️⚠️ THE SAME THEME, THIRD FORM. The BIM route stays parametric and LEAKS its associations (§2). The mesh route is parametric until you bake, and then THE PARAMETERS ARE SIMPLY GONE** — *"if we ever wanted to make the walls thicker now… we would have to move specific vertices and do each wall one by one."*
>
> **⚠️⚠️ OUR ROUTE HAS NEITHER PROBLEM, AND IT IS WORTH NAMING WHY.** Walls are rebuilt from `data/canonical/` on every run, **so the parameters live UPSTREAM of the geometry rather than inside a modifier stack or an element's type.** We get per-face control in the output *and* keep the parameters, because they were never in the model to begin with. **Neither hand route can have both.**
>
> ⚠️ **A related mesh-route limit**: one `Solidify` gives **one thickness per object** — *"there's no way to give different thicknesses to different walls"* — so a second thickness needs a second Walls object. **Against the BIM route, where thickness is a type property (§8).** This flat has several wall thicknesses.

### ⚠️⚠️ 14c. The OPENING is the fragile relationship in BOTH families

**In the mesh route the void is a box (`CTRL_Hole`) parented to the door, and the wall carries a Boolean pointed at a whole COLLECTION — so membership *is* the relationship.** That looks more robust than §2's `shift G`. **It is not.** The same practitioner reports three failures:

1. **The cutter silently vanishes on duplicate** — *"it's happened to me a couple of times… **I'm really not sure where it went or why it disappeared**."*
2. **Rotating a door ejects its cutter from the collection** — *"any time we change something, **we need to place our cutter back on the cutters collection**."*
3. **Anything else dropped into that collection is subtracted from the walls**, including objects created while it happened to be active.

> **→ ⚠️⚠️ BIM: the void does not follow the element. MESH: the cutter is lost, ejected, or joined by something that should not be there. In every case the wall silently has no hole — or an extra one — and the model still looks plausible.**
>
> **⚠️⚠️ And he states the invariants as a debugging checklist, which is a validator specification**: *"make sure that **every door and every window has a cutter**… [and] **make sure that everything inside this collection is a `CTRL_Hole`. If there's anything else in this collection, move it out.**"*
>
> **→ That is precisely the opening-coincidence check recorded as missing in §2 — written out by a practitioner as a troubleshooting procedure, and now a CROSS-FAMILY requirement rather than a Bonsai quirk.** [source: [[_Sources/YT_94kAIpRnhcY_dudeblender_floor_plan_series|YT_94kAIpRnhcY]]]

### ⚠️ 14d. "Edit one, edit all" is a property of instanced geometry, not a BIM concept

Blender's import modes carry the same distinction the BIM sources make, **with the trade-off measured**: `Append` gives each copy its own mesh data; **`Append (Reuse Data)` shares one datablock** — 386,203 faces, add a second coffee table, **count unchanged, the new object reports 0 faces** — *"but if I do this with the table, you'll see that **all the tables are modified**."* To diverge, use plain `Append`. **The same pattern appears again for materials**, which must be duplicated before one room's tile scale can differ from another's.

> **→ FIFTH AND SIXTH INSTANCES OF THE THEME** (door types, materials, tags, wall types, mesh datablocks, material slots). **It is not a BIM feature — it is what instancing is — and the trade-off is finally quantified: memory and face count against editability.**

## Sources

All read in full, 2026-09-13. Batch triage and channel assessment: [`bonsai_ifc_batch_20260913.md`](../../_Inbox/planning/bonsai_ifc_batch_20260913.md).

- [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|Ifc Architect — BlenderBim floor plan]] (2022-10-18) ⚠️ dated; UI content discarded, document semantics retained
- [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|Prof Rino — first BIM drawing in Bonsai]] (2025-11-07) — the most current Bonsai source here
- [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|SPB Production — IFC or blend save?]] (2023-11-20) — the controlled experiment
- [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|Ruben Messerschmidt — dimensioned floor plan export]] (2024-04-23) — the mesh route
- [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|Alan Rito — external IFC libraries]] (2026-05-27) ⚠️ `promotional_ratio: medium`

**Added 2026-09-13 from the `@IfcArchitect` Tier 1 round** — triage: [`ifcarchitect_tier1_20260913.md`](../../_Inbox/planning/ifcarchitect_tier1_20260913.md). **⚠️⚠️ All eight are ONE PRESENTER, a South African architect** (he names his own *"South African standard 220 masonry wall"* and calls his line weights *"very South African standardy"*). **His agreement with himself is not corroboration, and every drawing convention from him carries an unstated national default.**

- [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|2D drafting]] (2025-03-27) — **the round's core**: dimensions manual, tags data-bound, output SVG+CSS
- [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|Section & elevation]] (2025-05-12) — one camera primitive; classification puts an object in the drawing
- [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|2D detail]] (2025-05-20) — **a detail is modelled, not drafted**
- [[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|Page layout]] (2022-12-13) ⚠️ dated — **the sheet is an SVG file, assembled by hand**
- [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|Lineweights & CSS]] (2023-01-25) ⚠️ dated — **the styling system is literally CSS**
- [[_Sources/YT__vrVETTI5jQ_ifcarchitect_custom_titleblock|Custom titleblock]] (2023-03-27) ⚠️ dated — `{{ }}` binding, and the install-directory problem
- [[_Sources/YT_jTL3a6QwckA_ifcarchitect_custom_wall_type|Custom wall type]] (2022-11-02) ⚠️ dated — **the correction in §8**
- [[_Sources/YT__hADRIo-ma4_ifcarchitect_custom_phases|Custom phases]] (2024-02-12) ⚠️⚠️ **hardest dating caveat** — he says phasing *"was not possible a year ago"* and his method *"will most likely work a bit better"* in future

> [!WARNING]
> **Every claim here is a named practitioner's opinion or observed tool behaviour on one version on one machine.** ⚠️ **Nothing on this page has been reproduced against our installed Bonsai 0.8.6-alpha260801.** Worth reproducing before any is treated as a fact about our toolchain: the leaky associations (§2), the `Ctrl+S` linkage (§6), the schema-upgrade defect (§3d), **the SVG/CSS directory layout (§10)** and **the phase workflow (§11)**. **§6 is worth mitigating regardless, since the fix is cheap and the failure is silent.**
>
> ⚠️ **`Pset_<Class>Common.Status` is IFC-standard and safe to rely on. The workflow around it in 2024 is not.**

## Open items

**Answered by the 2026-09-13 `@IfcArchitect` round, and struck:**

- ~~*Does Bonsai place dimension text without per-instance intervention?*~~ **No.** There is no auto-dimension at all, and text collision is fixed by shrinking fonts — three instances, two tools, two presenters (§4). **The premise behind the `Adopt` verdict is corrected; for dimensions our generative route is the better one.**
- ~~*Is sheet assembly scriptable, or must it be a GUI step?*~~ **In the GUI it is manual drag-and-drop. But the artefact is plain SVG, so a script can write it — which is what we already do (§12).**
- ~~*Can the annotation subsystem express a proportional `1/2` dimension?*~~ **Yes, and more generally: annotation text is a `{{ }}` template over model data (§4b). It needs no Bonsai.**
- ~~*Does the type library force quantised wall thicknesses?*~~ **No — corrected in §8.**

**Open:**

- **⚠️⚠️ Restate the gap analysis's headless question** as *"which re-synchronisation steps must a headless script call explicitly, and what gates the result?"* (§2). **Four concrete entries so far**: `shift G` after moving a hosted element; refresh after a parameter change; **`create drawing` must precede `create sheets`** (a two-stage cache — otherwise the sheet is silently stale, §12); and *"always tick to confirm, otherwise it's not going to work."* **→ A cheap first gate: assert no sheet is older than the drawings on it.**
- **⚠️⚠️ Close the `Ctrl+S` hazard** — read-only viewing copy, or hash the project IFC in the batch gate (§6)
- **⚠️⚠️ Revise the two-engine framing** (§10). It assumed two incompatible engines; there is one SVG artefact. **Confirm the directory layout and stylesheet mechanism against our installed version first.**
- **⚠️⚠️ Decide the DETAIL question** (§13): model at detail resolution, draft in 2D, or issue no details and say so. **Owner's call.**
- **⚠️ No opening-coincidence check exists** — needed before any Bonsai-touched file enters the deliverable (§2)
- **⚠️ Adopt `Pset_<Class>Common.Status`** for existing/demolish/new in place of DXF layers, **per instance, not per type** (§11)
- **⚠️ Nothing validates a styling vocabulary** — a mistyped material or object type yields no hatch and no error; a mistyped selector excludes nothing and reports nothing (§10, §11). **Three concrete IDS rules now recorded.**
- **⚠️ Styling artefacts live in the application install** and would have to be repo-managed and installed by the build (§10)
- **Whether an IFC round trip preserves GUIDs and property sets** — untested by anything read so far (§6)
