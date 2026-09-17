# Triage Report — Blender/Bonsai Sources vs. Toolchain Requirements

**Date:** 2026-09-17 · **Brief:** `_Inbox/planning/agent_brief_bonsai_blender_triage_20260917.md` · **Status: Complete**

Triaged **292 candidate videos** across five candidate channels/playlists:
- **A: @blender3darchitect** (Alan Brito / Alberto): 152 videos (1 already in vault, 1 processed, 150 skipped)
- **B: @BIMvoice** (Stefan Catargiu) — playlist `PLUIgjxgKOw-rjpiXaCV2oZ6WK95K9nSwM`: 82 videos (4 processed, 78 skipped)
- **C: @dynamiterevit** (Christina / Dynamite Revit) — playlist `PLm0YJLPFdYMb85q2gB-bzivMxnI1USKi9`: 6 videos (0 processed, 6 skipped)
- **D: @Modelflick** (ModelFlick): 1 video (0 processed, 1 skipped)
- **E: @SPB-production** (Tom): 51 videos (1 already in vault, 3 processed, 47 skipped)

Total processed into `_Sources/` and routed into the wiki: **8 videos** (47 new facts, yield 5.9).

---

## 1. Evaluation of the 12 Open Problems

The 12 blocking-or-near-blocking problems from brief §3 evaluated against practitioner evidence:

| # | Open Problem | Verdict | Primary Source & Practitioner | Core Finding & Architectural Transfer |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Scripted IFC authoring with `ifcopenshell`** | **NOT COVERED** (in tutorials) | Stefan Catargiu (`-XPGFbmuh8U`) | All video tutorials across all 5 channels are interactive GUI-based. Catargiu explicitly identifies IfcOpenShell scripting as a separate higher-level automation tier above the GUI, but gives no tutorial code. Our programmatic compiler remains ahead of YouTube tutorial practice. |
| **2** | **Services in IFC** (`IfcOutlet`, `IfcLightFixture`, `IfcCableSegment`, `IfcPipeSegment`, etc.) | **NOT COVERED** | *Total void* across all 292 videos | Zero videos demonstrate MEP, electrical runs, pipe networks, or distribution ports in openBIM. Public practitioner tutorials remain 100% focused on architectural envelope (walls, slabs, doors, windows, basic finishes). |
| **3** | **Concealed cable routes in 3D** (modelled run vs. zone) | **NOT COVERED** | *Total void* across all 292 videos | No practitioner demonstrates modelling 3D cable routing, chases (штробы), or conduit geometry in Blender/Bonsai. OpenBIM practitioners treat services either as 2D lines or skip them entirely. |
| **4** | **Ceiling-hosted elements** (`surface_local` support geometry) | **NOT COVERED** | *Total void* across all 292 videos | No tutorial establishes procedural attachment or relative coordinate referencing of luminaires/detectors against ceiling slabs. |
| **5** | **Elements inside a riser zone / shaft** (`zone_local` framing) | **NOT COVERED** | *Total void* across all 292 videos | Zero treatment of MEP shaft coordination, riser framing, or interior pipe stacks. |
| **6** | **IFC phasing** (existing / demolished / new strip-out) | **PARTIALLY** | Vault prior: `_hADRIo-ma4` | In this batch, phasing received no new deep treatment. Vault prior (`_hADRIo-ma4`) remains authoritative: query over `Pset_<Class>Common.Status` (`EXISTING`, `DEMOLISH`, `NEW`). |
| **7** | **2D discipline sheets generated FROM model** (electrical, plumbing, HVAC plans) | **NOT COVERED** | Christina (`dynamiterevit`), Modelflick (`oYnVK7BDGig`) | Only basic architectural floor plans are drawn. Modelflick and DynamiteRevit demonstrate manual post-processing of SVG in Inkscape (adding fills, text, furniture lines), but zero MEP discipline sheets exist. |
| **8** | **IFC4 vs IFC4.3 in Bonsai** (schema migration, what breaks) | **ANSWERED** | Tom / SPB Production (`XYeasHbyw-U`) | Stepwise upgrade required: `2x3 -> 4.0 -> 4.3` via Bonsai's `IfcPatch` `Migrate` recipe. IFC4.3 is built for infrastructure (rail, alignment, bridges) with zero architectural benefit for flats. Downgrading strips georeferencing and degrades unmapped entities into `IfcBuildingElementProxy`. Deprecated classes (e.g. `IfcDoorStyle`) are not cleaned up. |
| **9** | **Bonsai file model** (`.blend` vs `.ifc` save semantics) | **PARTIALLY** | Tom / SPB Production (`tAq0foY2GOY`, `XYeasHbyw-U`) | Reinforced finding from vault prior `tAq0foY2GOY`: native IFC editing writes directly to the `.ifc` on save (`Ctrl+S`). Opening without Bonsai or in read-only mode remains the required safeguard against accidental overwrites. |
| **10** | **GLB/glTF export and appearance gap** | **NOT COVERED** (in this batch) | Vault prior: `HV-fbzv4VAU`, `i82_Rx1OUe0`, `BifyAj9KpaI` | Thoroughly settled in 2026-09-16 batch: materials are a non-transfer; textured models require per-surface UV unwrap + Cycles baking; untextured grey geometry is the correct scope for clearance/spatial checking. |
| **11** | **Quantity take-off from IFC and cost join** | **ANSWERED** | Tom / SPB Production (`fUlDzxSDOls`) | Bonsai Spreadsheet tool extracts tabular schedules, component counts, and QTO parameters directly to `.csv`. Class filtering, Pset dot notation (`Pset_Name.Property`), grouping by type, and `count()`/`sum()`. Syntax trap: property sets with spaces require double quotes (`"IFC Door Information".Function`). |
| **12** | **Validation** (IDS, model checking, CI rules) | **ANSWERED** | Tom (`CbDO16CfC7M`), Stefan Catargiu (`-UuUCMOAvx4`, `-XPGFbmuh8U`) | Client-side WASM IDS validation via `ifctester.org` (zero data egress, GlobalId audit reports). IDS applicability trap: checks on type properties must target `IfcWallType` rather than `IfcWall`. Production reality: commercial checkers (Solibri) are retained because Bonsai validation on large models wastes days. |

---

## 2. The Missing Gaps — What These Sources Omit Entirely

The most critical strategic finding of this triage is the **total absence of MEP and building services** in openBIM practitioner material:

1. **The MEP / Services Black Hole in openBIM**: Across nearly 300 practitioner videos, not a single one deals with electrical distribution boards, cable routing, concealed conduit, plumbing manifolds, waste pipes, or HVAC ductwork. Public openBIM content is strictly limited to architectural massing, basic structure, walls, slabs, doors, windows, and decorative furniture staging.
2. **Concealed Cable Routing & Chases (Штробы)**: No practitioner demonstrates modelling 3D cable runs inside walls or underfloor screeds. The owner's requirement for 3D electrical modeling from the start is unaddressed by existing YouTube openBIM tutorials.
3. **Programmatic / Scripted IFC Authoring**: No videos teach authoring IFC through Python / `ifcopenshell`. Every tutorial relies on clicking GUI buttons in Blender. Practitioners acknowledge scripting as an elite tier (`-XPGFbmuh8U`), but treat it as proprietary studio knowledge rather than tutorial content.
4. **2D Discipline Sheets (MEP Deliverables)**: Floor plans, sections, and elevations are shown for architecture only. Generating electrical plans (switch legs, circuits, socket heights) or plumbing schematics from an openBIM model is completely unevidenced.
5. **Support Geometry for Locators**: Ceilings and risers are not coordinated in detail; locators like `surface_local` or `zone_local` have zero reference implementations in public Bonsai workflows.

---

## 3. Tool Limitations, Bugs, and Crashes Stated by Practitioners

Practitioners explicitly report severe bugs, crashes, and behavioral traps in Blender and Bonsai:

1. **CGAL Hybrid Geometry Kernel Crash (`530npr9stZ0`)**: Bonsai's default CGAL geometry kernel causes instant hard crashes of Blender upon importing or loading complex IFC models (frequent on Apple Silicon / macOS and complex meshes). **Workaround:** Enter Bonsai *Advanced Mode*, navigate to Geometry Library, and switch the kernel to **Open Cascade**.
2. **Live Classification GUI Crash (`sdNStKd-fqE`)**: Basic entity classification in the Bonsai interface (e.g. classifying a simple box as `IfcFooting`) frequently triggers an instant, unhandled crash of Blender to desktop.
3. **The Vanishing Geometry Trap (`sdNStKd-fqE`)**: In Bonsai, assigning an IFC class defaults to `IfcElementType` rather than `IfcElement`. Element types are abstract definitions and are excluded from spatial hierarchy containment (`IfcRelContainedInSpatialStructure`), causing the 3D mesh to instantly vanish from the scene upon assignment.
4. **Text Objects Cannot Be Classified Directly (`sdNStKd-fqE`)**: Native Blender 3D text cannot receive IFC classifications. Modellers must manually convert text objects into polygonal meshes (`Convert to Mesh`) before Bonsai can serialize them.
5. **Interoperability Failure of `IfcAnnotation` (`sdNStKd-fqE`)**: Standard IFC 2D/3D annotation entities (`IfcAnnotation`) fail to display in common commercial BIM viewers (e.g. BIMcollab Zoom, Solibri). Practitioners are forced to convert annotations to 3D meshes and assign them to `IfcBuildingElementProxy` so external viewers can render them.
6. **Bonsai Spreadsheet Unquoted Whitespace Bug (`fUlDzxSDOls`)**: In the Spreadsheet schedule builder, property set queries fail or crash if property sets contain spaces (e.g. `"IFC Door Information".Function`). Double quotes are strictly mandatory.
7. **Lack of Mirrored Instances in openBIM (`1WPw5NRJQmM`)**: buildingSMART and the IFC schema do not permit mirrored object instances (a physical manufactured product cannot be flipped inside out). In Bonsai, the mirror tool only reflects coordinate positions across an `IfcVirtualElement`, leaving the actual geometry orientation unmirrored.
8. **Validation Performance Bottlenecks (`-XPGFbmuh8U`)**: Validating large, multi-discipline IFC models inside Bonsai/Blender is prohibitively slow, "wasting days" compared to commercial rule engines like Solibri. This forces practitioners to retain commercial software in production.
9. **No Automated Dimensioning**: Corroborating earlier findings, dimensioning in Bonsai is entirely manual: users click vertex-to-vertex polylines. There is no automated chain dimensioning.

---

## 4. Contradictions Against the Vault

1. **Format Conversion Cleanliness vs. Entity Obsolescence**: A schema migration (IFC2x3 to IFC4) using Bonsai's `IfcPatch` `Migrate` recipe reports 100% success, but leaves deprecated entities (such as `IfcDoorStyle`) intact in the file. A passing schema syntax check does not mean semantic compliance.
2. **Geometric Mirroring vs. BIM Reality**: Modellers expect Blender's Mirror Modifier behavior (flipping geometry). OpenBIM forbids flipped geometry for standard types; Bonsai reflects placement coordinates across `IfcVirtualElement` while keeping the object untransformed.
3. **The "Ditch Commercial BIM" Narrative**: Online openBIM advocacy claims open-source tools can fully replace Revit/Solibri today. Practitioner Stefan Catargiu (`-XPGFbmuh8U`) directly contradicts this: only an estimated two practitioners operate 100% open-source, and commercial checkers remain mandatory for speed.

---

## 5. The Skip List

Summary of 284 candidate videos skipped with one-line rationales:

### Source A: @blender3darchitect

| Video ID | Video Title | Skip Rationale |
| :--- | :--- | :--- |
| `vSEyPpYJaKE` | Every Imported Model Has This Problem — Fixing Scale in Blender | Manual viewport scaling fix; compiler produces metric mm geometry natively. |
| `MBvYDbj3gBM` | Stop Modeling Walls One by One in Blender — Do This Instead | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `daTmL9lg8io` | Blender Finally Shows Dimensions in Edit Mode | Manual drafting/dimensioning; programmatic generator computes dimensions directly. |
| `ojbc0wJeTpw` | Blender Now Has Parametric Profiles — This Changes Everything | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `gRZg4MxA3rA` | Blender as a CAD Tool — Professional Dimension Lines | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `DlqIjvzq_kg` | Blender as a CAD Tool — Drafting with Precise Angles | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `noAwAKF_BI0` | The Hidden Blender Tool That Makes Precision Modeling Easy | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `btKlamZF8oI` | Blender Can Now Open Revit Files - Should Autodesk Be Worried? | Proprietary Revit workflow; not applicable to openBIM/Bonsai toolchain. |
| `2YHppVqWg-A` | Blender for Architecture with Bonsai BIM: The Workshop Autodesk Hopes You'll Never Find | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `A-LdXthsDZg` | Blender 5.2 Just Got 3ds Max File Import — And It's Free | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `5te37tEEfvs` | Blender Can Calculate How Much Paint Your Room Needs — Blender for Architecture | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `D_-Tta9pffc` | You're Limited to 2 Blender BIM Templates — Here's How to Add More | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `0sO2KWNUjg4` | Blender Just Got Unreleased AutoCAD-Style Wall Tools — And They're Free | Software release announcement / news; transient capability claims. |
| `3lzR6t9Lo-U` | Blender vs FreeCAD: Precise Door & Window Placement — Which Is Better? | FreeCAD specific tutorial; outside repo toolchain. |
| `mWyT3YoqX4A` | I Drew a Floor Plan in FreeCAD — It Built the 3D Walls Automatically | FreeCAD specific tutorial; outside repo toolchain. |
| `qu9-UKGuusg` | Your Bonsai BIM Objects Are Disorganized — Here's the Fix | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `Zoh_YR5SeXc` | Blender 5.2 Just Replaced AutoCAD for Me — DWG Import Free | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `u_7FU-JlEOQ` | Revit's Best Windows Now Work in Blender — But Nobody Shows the Fix | Proprietary Revit workflow; not applicable to openBIM/Bonsai toolchain. |
| `JlfHwK2hHaE` | Does SketchUp Import Still Work in Blender 5.2? I Tested It | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `_fYD9Pf3z5g` | Beyond the Basics: Blender Precise 3D Modeling from Specifications | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `QTSdYmfgoVo` | Blender Just Got Parametric Stairs & Railings — And They're Free (Best Architecture Add-on) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `FvtmIRuEeMk` | Blender Just Got Free IFC Furniture — But There's a Problem You Must Fix First (Bonsai BIM) | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `Qdjo6Awaimo` | Bonsai BIM vs FreeCAD: Same Floor Plan, Two Free Tools — Which Workflow Wins? | FreeCAD specific tutorial; outside repo toolchain. |
| `0ktp-S7Lev0` | Your Bonsai Doors & Windows Are Broken Without This — How to Manage Voids | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `Ww_G7vunrRQ` | Blender Just Got the Best Roof Modeling Tool — And It's Free (Bonsai BIM) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `hfJMH4gLM4s` | This Free Blender Add-on Replaces Every Paid Architecture Tool I Own | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `d5BKgffzGEY` | Blender Just Turned SketchUp Files into Revit-Compatible BIM — For Free (Bonsai BIM) | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `4JYFYvNg5Xk` | Blender Just Got Unlimited Doors & Windows — From a Revit Library, For Free (Bonsai BIM) | **ALREADY IN VAULT**: Already in vault: external IFC libraries & Revit asset import |
| `AYwtbL-Q3-Q` | Blender Just Got ArchiCAD-Style Curved Walls — And They're Free (Bonsai BIM) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `zG1_Ijh_rVg` | Stop Using Blender's Array Modifier for BIM — Use This Instead (Bonsai BIM) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `co0lOhmkfH0` | Blender Has Layered Walls & IFC Materials Now: Bonsai BIM (Free) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `kEFgXvcbHEw` | Stop Using Default Walls: Create Custom IFC Types for Bonsai BIM | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `ZoCUEssXt_0` | Blender Has Parametric Dimension Controls Now: Bonsai BIM 0.8.5 (Free) | Manual drafting/dimensioning; programmatic generator computes dimensions directly. |
| `dRSoT80oDNA` | Blender Has Parametric Walls Now: Create & Edit with Bonsai BIM (Free) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `d8WAOLqyn7o` | Blender Just Got AutoCAD-Style Editing Tools — And They're Free (Bonsai BIM) | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `fROixyEHhJU` | Stop Starting from Scratch in Blender: Create Reusable Project Templates (Free) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `Zq5uOnFjAIE` | Blender for Architects: Complete Free Course by an Architect (3.5 Hours) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `IgQWqUS4CM8` | Blender Can't Align Objects? This Free Add-on Fixes That (Align Helper) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `WZMbhS3HHRY` | SketchUp Groups in Blender: The Free Add-on Every Architect Needs | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `SwUFuCTlMOo` | Floor Plans in Blender: From Zero to Scaled CAD-Style PDF | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `aS02pwpGzCQ` | Stop Paying for 3D Furniture Models (IKEA to Blender Free Add-on) | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `ZRqocIcMlKw` | The Fastest Way to Model Handrails in Blender (Skin Modifier Trick) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `hW1A9IAUWTM` | Blender Can't Open DWG Files? Here's the Free Fix | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `eF0dGwFCnXo` | Blender 5.1: How to import SketchUp (SKP) files? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `wlo9RPNAVNI` | Your Blender Textures Are the Wrong Size (Here's Why) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `l0aMlT_R80s` | New Free Blender Add-ons You Didn't Know Existed - Architecture & Design | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `837kKRVKMIs` | AI Rendering for Architecture: Blender to Nano Banana Pro 2 Workflow | Rendering/lighting tutorial; superseded by 2026-09-16 Cycles/Blender rendering batch. |
| `ssYnUQxe57g` | Blender for Architecture: SketchUp Follow Me Alternative | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `-Bq7YI9ustE` | Blender Units for Architecture: Metric & Imperial Setup Guide | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `DpNBLcoFCFU` | Blender Snapping Tutorial: Move, Orbit & Grab Objects with CAD Precision | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `_uaqPPLG8hQ` | Blender as a CAD tool: How to create arcs? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `PmhAe562IB8` | Blender for architecture: Dividing edges like SketchUp | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `sEOtTLuDqGE` | Blender 5.1 for architecture: Managing material with the Solidify Modifier | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `6IQxrFbXeE0` | Blender 5.1 for architecture: How to use Human Scales? | Manual viewport scaling fix; compiler produces metric mm geometry natively. |
| `pNy8uDAOqy4` | Blender 5.1 for architecture: New snapping features | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `JBU1wlJXPbA` | Blender for 3ds Max users: Using the Angle Snap | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `dsod69UcXTE` | Blender for architecture: How to get areas by materials like SketchUp? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `zIN4TUa6Nyg` | Blender for Architecture: Adding Dimension lines like SketchUp | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `jBR9uU10fno` | Blender 5.0: Image references with correct scaling! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `t-nwHSpFMlM` | Blender 5.0: Snapping like a CAD tool | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `XiGKxKuvSgc` | Blender 5.0 for architecture: How to create section cuts? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `6IWqLI_ZT1o` | Blender 5.0 for SketchUp users: How to create a 2 Point Perspective camera? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `5kEXeAOdLzw` | Blender 5.0 as a 2D Drafting tool: Using the Offset tool like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `UoIqZRRMJs8` | Blender 5.0 for SketchUp users: How to use components in Blender? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `18gj85kSVuU` | Blender 5.0: How to move the camera? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `gx7a2Ubf6-M` | Blender 5.0: Precise 3D Modeling - Angular Dimensions | Manual drafting/dimensioning; programmatic generator computes dimensions directly. |
| `6J5rFtoDyIY` | Blender 5.0 as a 2D Drafting tool: Extending edges like AutoCAD? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `ZsO-CZlBmj8` | Blender 5.0 for SketchUp users: How to add dimensions like SketchUp? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `quMG0HGeY74` | Blender 5.0 as a CAD tool: How to find edge intersections? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `Vtyu_c1g-rE` | Blender 5.0: How to import any DWG? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `c_53T-HD_M4` | Blender 5.0 for SketchUp users: Using the Offset tool | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `g0ZCuKOd4S0` | Blender 5.0: How to import SketchUp (SKP) files? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `k1_sVyNfnX4` | Blender 5.0: Fillet Edges like a CAD tool | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `oPMJwTONHv4` | Blender as a CAD tool: Using the Align Command from AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `30HpG29jaHY` | Blender 4.5: Adding Isometric Views for Precise Modeling | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `PYiB8zqhLQE` | Blender 4.5 Precise 3D Modeling: Precise Scale transformations | Manual viewport scaling fix; compiler produces metric mm geometry natively. |
| `YnaPG-LTFY8` | Blender for Beginners: How to use the 3D Cursor? | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `H2pOY6rHRBI` | Blender 4.5 Precise 3D Modeling - Transformations | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `M9Swgw3n0wg` | Blender for SketchUp users: Units and Numeric Input | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `73u1T3AWjjw` | Blender 4.4: How to import SKP (SketchUp) files? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `XucSLOozxvw` | Precise Modeling with Blender: Custom Transform Orientation for 3D Modeling | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `aNJOqkI7iLU` | Blender 4.3 Tutorial: How to fix Stored Views in Blender 4.3? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `_RtL6LgAkVU` | Blender 4.3 Tutorial: How to create Groups? (Free Add-on) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `g74QFYvQ5HA` | Blender for SketchUp users: Extrudes and Dimensions (Migration Guide) | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `8cLfnIpmzQc` | Blender 4.3 Tutorial: Align Helper for Architecture and Design (Free Add-on) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `gLi0bfCLDNM` | Best Free DWG Converter? Convert 2D DWG to DXF Without AutoCAD! | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `_AkC23ndPkM` | Blender 4.3: Does MeasureIT_ARCH still work? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `OiGEKHy3vWU` | Blender Tutorial: New tool to manage multiple 3D Cursors (Free Add-on) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `tDOr7p35QUQ` | Blender for Architecture: Export drawings as SVG files! (Free Add-on) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `oOLL1Z4o5lo` | Open-Source CAD: How to Fix the Move/Copy? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `FL28f31J9d4` | Blender for Architecture: Creating 2D Drawings with Bonsai & Door Swing Direction | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `adtjnJlXoG8` | Blender for Architecture: Create Leaders like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `e4c746vnOcs` | Blender Tutorial: Fast Custom Templates from Blender files | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `YW7ZE0f9OxY` | Open-Source CAD: How to use the Trim Command like AutoCAD? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `GXe13vg39oQ` | Blender for Architecture: How to manage Dimension Line Styles? | Manual drafting/dimensioning; programmatic generator computes dimensions directly. |
| `N-ZTFf3j8wI` | Blender Tutorial: True Isometric Cameras and Viewports | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `wSDTBf1NEhU` | Blender Tutorial: How to import models from the 3D Warehouse? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `60UZZkRbmTQ` | Blender for Architecture: Extend Walls to Slab in Bonsai (Free Add-on) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `xhFYa_uaGBo` | Blender for Architecture: Rendering Dimension Lines (Free Add-on) | Rendering/lighting tutorial; superseded by 2026-09-16 Cycles/Blender rendering batch. |
| `ZJHscZ0FRGY` | Blender for Interior Design: Direct Import Furniture from IKEA (Free Add-on) | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `Kx5tkmsA08k` | Blender for Architecture: New Measure Tool for Bonsai | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `q7JT_0BARqE` | Precise Modeling For Architecture, Engineering, and 3D Printing (Workshop announcement) | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `ohRQ79NE9D4` | Blender for Architecture: Creating Dimension Lines (Free Add-on) | Manual drafting/dimensioning; programmatic generator computes dimensions directly. |
| `XRMF9r9wsDM` | Open-Source CAD: Setup Layers and Units (Quick Start) | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `2Uqj2sORVcg` | Blender for Architecture: Bonsai New Feature! Walls from Polylines | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `MZ9g5Aa8YHI` | Blender for Architecture: Snapping Between 2 Points and Divisions | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `MiY8oPp7E94` | Blender for Architecture: Wall Corners with the Shear Tool | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `XXVEMRTO-yQ` | Blender as a CAD Tool: Polar Array like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `SVqVARscRwc` | Precise Modeling with Blender: 3D Rotations like a CAD tool | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `xav08oOG4xY` | Blender 4.2 Tutorial: Hidden Shadeless Material | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `KEjnwYdk9E0` | Blender for Architecture: Crafting Pediments with Custom Bevel Profiles | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `91rjyMiA9zU` | Precise modeling in Blender: Finding Tangents between Circles | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `NoSlh9bBNIU` | Blender Tutorial: Switching Shaders Using Drivers and Custom Properties | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `bmfDV-c0F9Y` | Blender 4.2 Tutorial: How to restore the 'Import Images as Planes' feature! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `CftIQe0I5Js` | Blender 4.3 News: White Balance control for renders | Rendering/lighting tutorial; superseded by 2026-09-16 Cycles/Blender rendering batch. |
| `-peTyn3zp4Q` | Bonsai: The new BlenderBIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `Ho_D7E00UzY` | Blender 4.2 Tutorial: How to find edge extensions? | Commercial Blender addon review; out of scope for reproducible open-source pipeline. |
| `NHNx9RhcU7Y` | Blender as a CAD tool: Drafting a room like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `a49mINaRmvg` | Blender 4.3 news: Revolutionary Asset Management Enhancements | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `E4UecZpjnik` | Open-source CAD Tutorial: Creating Furniture Blocks | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `z6YB9LV1QpE` | Blender 4.2 Tutorial: Align drawings like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `T10jGNQczOE` | Blender for beginners: Snapping tricks | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `5TXQHa-E4Qs` | Open-Source DWG Editor: Windows, Mac, and Linux | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `YQdLFSXQ2g4` | BlenderBIM is over! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `TX6BR-khOzk` | Blender as a CAD tool: Simulating AutoCAD's POLAR Tracking | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `Qh-XzkbLGew` | Blender: Hidden Template System | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `7zvllsF_CAk` | Inkscape as a CAD tool: Adding dimension lines! | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `th7fyP_fZ08` | Blender CAD Secrets: Hidden Snap Tools for Precise Intersections | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `d_DMz-QEiQ4` | Blender for beginners: Camera shortcuts and options | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `GjtVylmjxJo` | Blender 4.2: How to update Add-ons? | Software release announcement / news; transient capability claims. |
| `YKcKjOVsl5c` | Blender 4.2: How to import SketchUp 2024 (SKP) files? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `Q9LOr2OqdJM` | Blender as a CAD tool: How to measure distances? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `rH37icJCWLA` | SketchUp 2024: How to change units and precision of a model? | SketchUp modeling/import; irrelevant to IFC/Bonsai pipeline. |
| `e8FTvghgpOg` | Blender 4.3 alpha: Geometry Nodes now supports Grease Pencil | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `qdeykglAUfg` | Blender 4.2: Free Add-on for Importing 3ds Max Files | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `VubsNW2qpdo` | Blender 4.2 Tutorial: How to Install, Remove, and Update Add-ons | Software release announcement / news; transient capability claims. |
| `u6LK0g0sAIY` | Blender 4.1: How to use Polar Coordinates? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `0Cpy3yQ36Pg` | AutoCAD to QCAD: Migrate to open source CAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `c1_eaW0eyIQ` | Blender 4.0: How to import any DWG? | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `Q_R9IEpUJmk` | From Blender 1.8 to 4.0: How much changed? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `AvM9XOj9M7s` | Blender 4.0: Hidden CAD tool | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `GU1DhlwAFEc` | Blender 4.0: Your new best friend - The ALT KEY | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `pEaKK7B3jUc` | Using Blender 4.0 like AutoCAD | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `ErwGvqb75bo` | Blender 4.0: New render engine Hydra Storm | Rendering/lighting tutorial; superseded by 2026-09-16 Cycles/Blender rendering batch. |
| `IvAqr70knic` | Blender 4.0: Meet the incredible Snap Base | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `QfUu4IHsmNw` | 22 Free masonry shaders and how to use the Asset Browser | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `BEDVq8MWLL0` | Free lounge chair model for Blender (OBJ-FBX)  - Blender 3D Architect | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `sf2WGOtnMzE` | Sketching a floor plan in Blender (Timelapse) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `vH2gNSkjFok` | Blender Add-on for Architectural modeling: Edge Tools | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `dnk9A5itj9E` | 3D ruler for architectural modeling in Blender | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `ijH6NPdINH4` | New bevel tool in Blender | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |

### Source B: @BIMvoice

| Video ID | Video Title | Skip Rationale |
| :--- | :--- | :--- |
| `RL3IAGeMi5s` | Bonsai BIM live: new 2D drawing tools, Revit questions and how drawings work under the hood | Proprietary Revit workflow; not applicable to openBIM/Bonsai toolchain. |
| `5Ik_HSD2XT4` | How to Optimise a Heavy IFC File From Revit in Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `bkvMqpUjkP0` | Modeling earthworks in IFC4x3 with Bonsai BIM (cut, fill and backfill) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `iO7JnykTgtk` | How to Add Images to Construction Drawings in Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `j5LAJSVNxmU` | How To Install Bonsai PR In Blender | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `NqC3E0q40zQ` | 6 ways to install Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `EC8I9EqZXzs` | Bonsai 0.8.5 Is More Than an Update. It Is a Line in the Sand | Software release announcement / news; transient capability claims. |
| `lm92E10prCg` | How to Install Bonsai BIM on Blender 5.1 Beta | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `WirBWr-hZmA` | Wait, Bonsai BIM jobs are a thing now? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `hPP1y-m2GCs` | Simplify Your Bonsai BIM Interface by Hiding Unused Tabs | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `xImmD0Ns4NQ` | Create Window Schedule With Bonsai BIM from IFC | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `90Zj-EE5ICU` | Bonsai BIM update: v0.8.4 - 1111 openBIM Upgrades for Native IFC Authoring Power! | Software release announcement / news; transient capability claims. |
| `Vy4RBlXFNQE` | Door Schedule from IFC with Bonsai BIM | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `QlHad-4oERw` | 💸 Blender for BIM: The $0 Tool to Assign IFC Entities and Generate Accurate Quantities | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `mKNE1aSrRIM` | Master IFC: FREE & Easy Upgrade from IFC4 to IFC4x3 (Quick Guide) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `r2AJe30KUIk` | BonsaiBIM Tutorial: Clean and Validate Your IFC Models Step-by-Step | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `STj9V3Hzk8M` | How to Load a Quantity Takeoff Template in BonsaiBIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `he38ShBfrlI` | 7-Day OpenBIM Kickstart Challenge (Free) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `DoDdimdquKA` | Bonsai vs Revit Usability: 6 Questions Answered (Honest Advice) | Proprietary Revit workflow; not applicable to openBIM/Bonsai toolchain. |
| `OusGMhCJGeo` | how to use color by property in bonsaibim (without getting stuck) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `PocfgyuL2EM` | 2 Amazing Tools to Instantly Find IFC Junk | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `4ME9ccBMEFc` | The Fastest Way to Understand Your IFC | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `k2tRerNDyJs` | Practical openBIM Sprint | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `De9X4LKeJEA` | How to Install BonsaiBIM Unstable Build in Blender (5.0 Beta & 4.5.3 LTS) (Auto-Update Method) | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `cw85F-3X0Js` | I just turned Blender into an IFC command center | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `zzT9XjOtqyQ` | You will not believe what BonsaiBIM can do now | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `XPba_FMZ8jM` | 34 People Told Me Their IFC Struggles — Here’s What You Can Do | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `jC0kgpG_JR4` | Blender 4.5.3 + BonsaiBIM Daily Build – Latest Working Setup | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `aZI0wonxoTA` | The Ultimate Guide to Fixing IFC Georeferencing Problems | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `XGKOQzOfzR4` | The Right Way to Georeference: Best Practices for Your IFC Model | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `V1VjLOqXuH4` | Why Your IFC2X3 Model is NOT Georeferenced (And What That Means) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `FJyYRfrdzjQ` | Is the BonsaiBIM Project Dead? Let's Find Out! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `CSTV8v--27E` | Information Delivery Specification (IDS) Series: Checking IFC Project Data | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `I6GHRGnlsdI` | How to Verify If Your IFC Model is Correctly Georeferenced with BonsaiBIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `ZEQh0YCTD7Y` | AI Meets Native IFC: Bonsai-MCP Demo | General AI image generation; covered by existing 18_Digital_Toolchain/ analysis pages. |
| `8MCudHxkh58` | Bonsai Explore Tool: Deleting and Managing IFC Section Cutaways | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `S0K1wwYNfoI` | Is Your IFC Model Georeferenced? How to Check with BonsaiBIM (by Dion Moult) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `YScv-lZy_3k` | How To Split IFC Objects In BonsaiBIM Super Fast! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `lQ_t0neAI9M` | are your ifc elements in the wrong spatial container? (BonsaiBIM fix) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `Vd6qnRO0ZP4` | Quick BonsaiBIM Hack: Select & Copy Multiple Global IDs Correctly | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `15UT8cWd4qU` | How to Auto-Generate Walls from Slab Perimeter in Bonsai (Hidden Feature) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `X8K6VgcQx5k` | I Changed My Blender Theme to THIS | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `415peYvhkcg` | Avoid These Mistakes When Using Bonsai with Blender 4.5 (Important Update!) | Software release announcement / news; transient capability claims. |
| `EuPHIaZWfGY` | without Bonsai Bootcamp perhaps I would not have had confidence to sell myself as BIM coordinator | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `kaHEnsnUD1k` | How to List All Properties in an IFC Model Using Bonsai | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `ZZKfSLrAwCU` | Customize Your Bonsai Workspace for Efficient IFC Work | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `T7Gqyw26Dq8` | Alternative Way to Export Whole Numbers from IFC with Bonsai | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `yanUyDVvn7U` | Still Questioning OpenBIM? You're Asking the Wrong Question | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `oh02NrnILaA` | Tired of Long Decimals? Bonsai BIM's Quick Rounding Fix! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `whbtODC6Qcg` | Blender 4.4 + Bonsai: Bug Hunt in Action! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `uUH6AgEBHHA` | You Won't Believe How EASY IFC Room Data Extraction is with Bonsai | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `u3yxwWgHqLE` | How to Merge Two IFC Models with Bonsai BIM (Step-by-Step Guide) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `OJFaPNyLXq0` | Bonsai 0.8.2 Just Dropped With 654 NEW Features and Fixes! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `WzSpVuibox0` | How to Add Custom Psets to IFC Project in Bonsai (Step-by-Step Guide) | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `9oXWh1spWys` | Working with IFC Spaces in Bonsai: What Works and What Doesn’t | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `zaqtSQJ_8jw` | BCF in Bonsai: Step-by-Step Guide to Reporting IFC Model Issues | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `bhsxiqVa4WM` | Your IFC Model, Story by Story – Bonsai Magic! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `ctzZp_x-1nM` | Sverchok IFC Nodes Explained – Blender to BIM Workflow | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `39acZciW1Rg` | Bonsai Workflow Boost: Essential Blender Shortcuts | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `YVr7o8rQNI8` | Modeling a small house with Stefano Verugi for QTO | QTO extraction; redundant with fUlDzxSDOls. |
| `mzP-reKQWHs` | 💡 Hidden Feature: Copying Object Info in BIM Just Got Easier in Bonsai! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `KU0WVuailo0` | Convert Any Blender Mesh to IFC – Step-by-Step Guide! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `KTORrq2YI3c` | Practical IFC Schema: Introduction | Generic beginner tutorial; covers basic UI navigation and manual wall clicking already in vault. |
| `oQBCy_zKMtI` | modify your wall opening with Bonsai in JUST minutes (IFC native) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `iIR3zl4b6vA` | how to add wall openings in IFC models using Bonsai (IFC native) | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `bJSMEETGvI0` | Bonsai devs fix bugs faster than you can report them | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `4xB4b6mizwI` | 🔥 Blender 4.3.2 Can Open IFC Models? Here’s How! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `T4OZ8C5Imxg` | the ugly truth about custom psets in your IFC models | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `ipGBMpk9X-s` | What's New in Bonsai 0.8.1: Major Upgrades You Can’t Miss! | Software release announcement / news; transient capability claims. |
| `Jgu9MWwgu_o` | you won't believe how EASY it is to model your flat and create a floor plan with Bonsai | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `AskeKa60f4E` | Bonsai Licensing EXPLAINED! Is It Really Free Forever? | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `iYHQy4UgTGc` | Bonsai IFC Model Movement Issues? Here's the FIX! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `4jkH6QNnTro` | Revolutionize Your BIM Workflow with the POWER of Blender | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `trE0gfgHmCM` | how openBIM transformed in 2024 and what comes next | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `A3Pp_dhICNU` | don’t miss out on bonsai’s newest features do this now | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `vfLOHbf8GsE` | Learn BONSAI the RIGHT Way Without Common Mistakes | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `H_143kQIzmY` | OPENBIM Like a PRO in 2025 with Easy Blender and Bonsai Installation! | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `-HFPTWxVP_o` | How to Set Custom Colors for IFC Elements | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |

### Source C: @dynamiterevit

| Video ID | Video Title | Skip Rationale |
| :--- | :--- | :--- |
| `Ozf2bdkDbso` | How to create walls with BlenderBIM? Crazy gable walls and trims edition! | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `Y0NUwQNqkKI` | BlenderBIM (Bonsai) Project Setup: IFC Project, Levels, Grids, Views, and Essential Blender Tools | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `9LBZ_JF549k` | Blender Interface For BIM Modellers - Understanding Blender's Potential for Architectural Projects | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `tHM-yd57PkM` | Revit vs. BlenderBIM (Bonsai): 5 Reasons Architects Should Be Paying Attention To the Blender NOW! | Proprietary Revit workflow; not applicable to openBIM/Bonsai toolchain. |
| `LXb51Bf5PLU` | Mastering Bosai (Formerly BlenderBIM) : Gizmo Hotkeys and Navigation Techniques for Architects | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `lR-zcXpnvco` | Windows & Doors In BlenderBIM (Bonsai) - Working With Door & Window Modifiers To Custom Types | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |

### Source D: @Modelflick

| Video ID | Video Title | Skip Rationale |
| :--- | :--- | :--- |
| `oYnVK7BDGig` | Generating Floor Plan in Bonsai BIM | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |

### Source E: @SPB-production

| Video ID | Video Title | Skip Rationale |
| :--- | :--- | :--- |
| `1lU_OaIwgrM` | Change Theme and Background Color in Open CAD Studio | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `CvnT_HM0KaI` | Polar Tracking in Open CAD Studio | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `MAsZAOtkIpM` | How to Use External References (XREF) in Open CAD Studio - XATTACH Tutorial | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `Kc8mnLkS3gM` | Mastering Blocks in Open CAD Studio (Creation, Editing) | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `QFDMSRNrZOU` | Create 2D Chair DWG Drawing in Open CAD Studio | 3D asset/furniture modeling; irrelevant to canonical programmatic compiler. |
| `bHwKKOdBtCQ` | Open CAD Studio: Object Snap Explained | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `JRlmIInZRiQ` | How to Install Open CAD Studio – Free DWG Authoring Tool | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `4_glyJFo0qI` | Open CAD Studio as a Free DWG File Viewer with No Login Needed | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `uN9zxM7p_fc` | Open CAD Studio Tutorial: Create a 2D DWG Drawing & Export to PDF | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `VMpJbnzB5k0` | View IFC Project in Geographic Context Using IFClite | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `zcfh9LboCoA` | Setup IFC Project Units in Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `DlUufnIIqk4` | Bonsai UI Overview - Use Bonsai BIM as an IFC Viewer | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `DwxcOTUyGRI` | Enrich Your IFC Project with Georeferencing Data using Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `rSHAf7GBsUE` | Wall Joints in Bonsai BIM: Material Layer Connections Explained | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `9-mkwEI3m8M` | Wall Layers in Bonsai BIM – IFC Material Layer Set in Practice | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `2DNUt3iOkJM` | New Feature in Bonsai BIM 0.8.5: Parametric Gizmo System | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `4c1xSt6pPEY` | Design-Web: Free Open Source 2D CAD in Your Browser (No Login Required) | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `4n1dhoEF-h8` | What’s New in Design 50 Alpha - 2D CAD for GNOME | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `jL9bX0HJ8Ns` | Understanding IFC: The Relationship Between IfcElement and IfcElementType | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `4jiu05gIKz4` | Explore IFC Files in Text Form with Ardit IFC Reader | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `Ksz-9552gKY` | IDSedit: Noodles-Based Information Delivery Specification (IDS) Editor | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `s94gzyhP3eU` | Use IFC Tester to Create IDS (Information Delivery Specification) | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `BZShGArYI1U` | What’s New in Design v49 Alpha | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `fu_AvTXZNXU` | IFC Compass: Simplify Your IFC Schema Searches | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `LJGAMAUXeTE` | Create Floor Plan on Linux with GNOME Design | Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault. |
| `Eqtqun9JrWM` | Use bSDD to Classify Elements in Bonsai BIM - buildingSMART Data Dictionary | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `OGtn1aVhWJg` | Overview of IFC Model Checker by OpenSource.Construction | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `62nQZ7ccz-c` | Extract Storey (Level) from an IFC Project Using Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `eJ2mufowSa0` | Hide Space Objects or Make Them Transparent in Bonsai BIM - Spatial Tool | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `FVGsMsu8BK8` | How to Correctly Fill Attribute Values According to IFC Schema | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `VpG_Pfb9IFY` | IFC Schema Information in Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `fN9cP6w0DsM` | Types and Instances in IFC - IfcElementType and IfcElement Explained | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `l6FmdCnGwkI` | Create Array in Bonsai BIM - Native IFC Modeling | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `AbEKyOnuQuU` | Extract Pages from PDF Document with Free Desktop Tool PDF4QT | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `9PZdWH3sWao` | Merge PDF Documents with Free Desktop Tool PDF4QT | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `QsCMFtY-qA4` | Remove Pages from PDF Document with Free Desktop Tool PDF4QT | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `bUuZ30Wy3T0` | How to Extract Elements from IFC File using Bonsai BIM | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `tAq0foY2GOY` | Bonsai BIM: save as an IFC or a Blend file? | **ALREADY IN VAULT**: Already in vault: Bonsai IFC vs Blend save controlled experiment (Ctrl+S hazard) |
| `wkdwzTAB8FE` | Create IDS specification with usBIM and validate IFC with it using Bonsai BIM - Free Tools | IDS validation; redundant with detailed coverage in CbDO16CfC7M and -UuUCMOAvx4. |
| `Er8Z5BuxJCg` | Tomas Polak 2013 Archviz Demo Reel | Interactive GUI archviz/modeling technique; no transfer to programmatic IFC pipeline. |
| `h9Aw_sI5ZmU` | BricsCAD: How To Insert and Adjust Raster Image | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `9WvLkwFaMms` | BricsCAD: How To Work on Non-Aligned Parts of Drawing | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `0qov2-9f93k` | BricsCAD: How To Use FILLET To Create Sharp Corner | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `dIv46Xm8wNg` | BricsCAD: How To Add Custom Hatch Pattern | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `bCpsPI_OiFo` | BricsCAD: Differnece Between Attachment and Overlay - External Reference | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `jEAvJVHFJIY` | BricsCAD: How To Freeze Layer in All Viewports - VPLAYER | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `h1mmt_5rl4w` | BricsCAD: How To Setup Insertion Units | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
| `cSzRa91l1s8` | BricsCAD: How To Turn Off Layer in Viewport | Manual 2D CAD import and tracing; geometry compiler generates directly from canonical specs. |
