---
source_type: video transcript (SPB Production, four tutorials on IFC typing, material layer sets, wall joints and IDS authoring)
source_url: https://www.youtube.com/watch?v=fN9cP6w0DsM
video_id: fN9cP6w0DsM
covers_also: 9-mkwEI3m8M, rSHAf7GBsUE, s94gzyhP3eU
transcript_file: _Archive/processed_sources/20260917_spbproduction_ifc_types_and_instances_dedeacaf.txt
transcript_file_pt2: _Archive/processed_sources/20260917_spbproduction_ifc_material_layer_sets_90d41c4c.txt
transcript_file_pt3: _Archive/processed_sources/20260917_spbproduction_wall_joints_layer_priority_d8a8530d.txt
transcript_file_pt4: _Archive/processed_sources/20260917_spbproduction_authoring_ids_in_ifctester_61c14c48.txt
fetched: 2026-09-17 via youtube-transcript-api (en, ORIGINAL language)
upload_date: 2025-06-19 (fN9cP6w0DsM); 2026-04-22 (9-mkwEI3m8M); 2026-04-29 (rSHAf7GBsUE); 2026-02-12 (s94gzyhP3eU) - all from yt-dlp, actually run
channel: SPB Production
source_title: "Types and Instances in IFC | IfcElementType and IfcElement Explained" (+ wall layers / wall joints / creating IDS)
language: en
extraction_taxonomy: custom (this project taxonomy - bucket `Digital Toolchain / IFC authoring`)
fact_yield: 12
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note — Tom (SPB Production): ⚠️⚠️ WHAT A TYPE CARRIES, AND THE SCHEMA'S OWN ANSWER TO WALL JOINTS (YouTube fN9cP6w0DsM +3)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

**Why these four.** Our generator emits **no types at all**, Bonsai's QTO groups **by type**, and our wall junctions are resolved by a corner-ownership ledger of our own invention. These four say what the schema itself does about each.

## ⚠️⚠️ 1. What is inherited from type to instance — and what is NOT

Demonstrated in BricsCAD BIM, so it is a statement about **the IFC schema**, not about one application.

| | Inherited from `IfcElementType`? |
| :--- | :--- |
| `Name`, `Description`, `GlobalId`, `Tag` | ⚠️ **NO** — each instance carries its own |
| `PredefinedType` | ✅ **YES** |
| **Properties (Psets)** | ✅ **YES** — edit the type's property and *«all of these instances have these properties inherited»* |
| **Geometry** | ✅ **YES** |

> ***"most attributes, such as name, description, global ID, or tag, are not inherited from type to element. The exception here in my case would be predefined type… whereas properties are inherited from type to an element."*** [Tom]

⚠️ **To learn an instance's type name you must query the type** — *«I would have to query the IfcColumnType for the name of the type»*. The instance does not carry it.

**→ ⚠️⚠️ THIS EXPLAINS THE QTO GROUPING REQUIREMENT.** Bonsai's Spreadsheet groups by `ObjectType`/`Type.Name` because **that is the only place the designation lives**. An instance-only model has nothing to group on — which is exactly our model today.

⚠️ Naming convention shown: type `C01` "fence column wooden"; doors as `D01`. **Types carry the schedule-facing designation; instances carry the individual mark.**

## ⚠️⚠️ 2. `IfcMaterialLayer.Priority` — the schema's answer to wall joints

The most directly transferable finding in the batch, and the nearest thing found in 292 videos to this project's corner-ownership problem.

- Bonsai's wall **trim** tool creates a *wall connection* and defaults to a **mitred** joint; a **butt** joint is made by extending manually; **unjoin walls** breaks the connection. So a joint is a **relationship**, not merely coincident geometry.
- Layer intersection at that joint is governed by an attribute on the layer itself:

> ***"the definition of IFC material layer, it has got this attribute which is name is priority and it's integer, so it's a range from 0 to 100. And this attribute controls how layers are intersected at connections."*** [Tom]

**The rule, in his worked example** (stucco 10, insulation 30, brick structure 50):

| Meeting | Result |
| :--- | :--- |
| equal priority meets equal | **joined** |
| higher meets lower | **higher protrudes through it** |
| protruding layer meets its equal | **stops and joins there** |

So brick (50) protrudes through stucco (10) **and** insulation (30), and stops where it meets brick (50).

> **→ ⚠️⚠️ COMPARE OUR RULE.** `data/canonical/wall_corners.csv` decides which wall owns an L-corner by **thicker, then longer**, at WALL granularity. IFC decides at **LAYER granularity, by an authored integer**. The two are not in conflict today — our walls are single-material, so there are no layers to prioritise — **but they will be the moment we emit `IfcMaterialLayerSet`**, and our external perimeter is genuinely layered (300 block + 70 mineral wool + render).

## 3. Material layer sets in practice (`9-mkwEI3m8M`)

Layer sets are attached to the **type**, edited through the type's material tab, and the appearance of each layer is carried by **surface styles** (surface style / fill / fill-area style) rather than by the layer itself. ⚠️ A plain brick wall type and a layered type can be given the **same priority on the structural layer** so they join correctly across types.

## 4. Authoring an IDS, not just running one (`s94gzyhP3eU`)

- **IDS** = Information Delivery Specification, buildingSMART's way to *«define and validate exchange information requirements»*.
- **IFC Tester** (`ifctester.org`) is a free open-source **web app**, and ⚠️ *«once the app is loaded, none of the data that you are using, so your IFC data or the IDS data, leaves your machine — everything runs locally»*.
- It has an **editor** for creating a specification, not only a runner for checking against one.

**→ We have no IFC validation of any kind.** This is the route to authoring one that does not send the model anywhere.

## 5. Transfer to this project

| Finding | What it changes |
| :--- | :--- |
| Types carry Psets, geometry, `PredefinedType`; instances carry `Name`/`Tag`/`GlobalId` | ⚠️ **The generator's type emission is now specified**, not guessed |
| Type name is the only home of the designation | Explains, and confirms, why schedules need types |
| `IfcMaterialLayer.Priority` governs joint intersection | ⚠️ A **second, independent** ownership rule we must reconcile with `wall_corners.csv` once layers exist |
| A wall joint is a connection that can be broken | Junctions are relationships to emit, not only geometry to compute |
| IDS can be authored locally with no data egress | A validation route for a model we cannot upload |

⚠️ **Rule 3 caveat:** Tom demonstrates in BricsCAD BIM and Bonsai. The schema statements are checkable against the IFC documentation and should be, before we emit anything — the `Priority` range 0–100 in particular.

## Source Notes
Tom, SPB Production — four tutorials, 2025-06-19 to 2026-04-29, English original captions.
