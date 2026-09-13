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

> **→ ADOPTING A TOOL DOES NOT SOLVE TEXT COLLISION; IT RELOCATES IT.** This does not overturn the `Adopt` verdict — Bonsai is a different tool and may place better — **but it removes the assumption underneath it.**
>
> **The honest form of the question**: *does Bonsai place dimension text without per-instance intervention, and is that placement reachable headless?* **Placement, not annotation capability, decides whether an annotated sheet can be generated by `make`.**

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

## 8. ⚠️ The default type library is thin, and it quantises

**Three sources, same complaint**: the demo template ships **one door**, one window, and slabs in **200 and 300 only**. Everything else comes from duplicating and editing a type.

> ⚠️ **And it has a dimensional consequence a practitioner accepts without comment**: *"we're going to select the **200 wall, because that's similar to a masonry brick wall of 220**."* **A 20 mm type error accepted because the library has no 220.**
>
> **→ A type-library workflow trades dimensional fidelity for schedulability. Ours currently has the fidelity and not the schedule** — `data/canonical/` carries exact `clear_mm` per wall. **That is the right way round, and it is worth not losing if Bonsai is introduced.**

## 9. The dividing line between the two families of tool, stated dimensionally

**Across this batch, six sources model a floor plan. They split cleanly on one question: is a dimension an INPUT or a CONSEQUENCE?**

| | The dimension is… | Sources |
| :--- | :--- | :--- |
| **BIM / parametric route** | **an INPUT** — type `10000`, press enter; `shift E` to extend to a snap; `shift C` to close; offsets typed from a named edge | Ifc Architect, Prof Rino, CG Essentials |
| **Mesh-tracing route** | **a CONSEQUENCE** of where the mouse went, read back off an edge-length overlay | Architecture Topics ×2, SFE-Viz |

> **→ This is a sharper distinction than any feature comparison, and it decides everything downstream.** A traced wall has no length property to schedule, no type to group by, and nothing to check against. **This project is firmly on the first side and should stay there** — our walls come from `data/canonical/`, which is the same relationship one step further back.

## Sources

All read in full, 2026-09-13. Batch triage and channel assessment: [`bonsai_ifc_batch_20260913.md`](../../_Inbox/planning/bonsai_ifc_batch_20260913.md).

- [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|Ifc Architect — BlenderBim floor plan]] (2022-10-18) ⚠️ dated; UI content discarded, document semantics retained
- [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|Prof Rino — first BIM drawing in Bonsai]] (2025-11-07) — the most current Bonsai source here
- [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|SPB Production — IFC or blend save?]] (2023-11-20) — the controlled experiment
- [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|Ruben Messerschmidt — dimensioned floor plan export]] (2024-04-23) — the mesh route
- [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|Alan Rito — external IFC libraries]] (2026-05-27) ⚠️ `promotional_ratio: medium`

> [!WARNING]
> **Every claim here is a named practitioner's opinion or observed tool behaviour on one version on one machine.** ⚠️ **Nothing on this page has been reproduced against our installed Bonsai 0.8.6-alpha260801.** The leaky associations (§2), the `Ctrl+S` linkage (§6) and the schema-upgrade defect (§3d) are the three worth reproducing before any of them is treated as a fact about our toolchain — **and §6 is worth mitigating regardless, since the fix is cheap and the failure is silent.**

## Open items

- **⚠️⚠️ Restate the gap analysis's headless question** as *"which re-synchronisation steps must a headless script call explicitly, and what gates the result?"* (§2)
- **⚠️⚠️ Close the `Ctrl+S` hazard** — read-only viewing copy, or hash the project IFC in the batch gate (§6)
- **⚠️ Does Bonsai place dimension text without per-instance intervention?** This is what actually decides the annotated-sheet split (§4)
- **⚠️ No opening-coincidence check exists** — needed before any Bonsai-touched file enters the deliverable (§2)
- **Whether an IFC round trip preserves GUIDs and property sets** — untested by anything read so far (§6)
