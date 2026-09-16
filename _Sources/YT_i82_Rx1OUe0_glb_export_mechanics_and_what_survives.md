---
source_type: video transcript (three technical tutorials on getting geometry and appearance out of Blender into a real-time viewer - the glTF/GLB format itself, material baking, and a Blender-to-Unreal import)
source_url: https://www.youtube.com/watch?v=i82_Rx1OUe0
video_id: i82_Rx1OUe0
covers_also: 2sgKu0bKUwU, AK4tVgdWVo4
transcript_file: _Archive/processed_sources/20260916_glb_export_mechanics_and_what_survives_0fd551cd.txt
transcript_file_pt2: _Archive/processed_sources/20260916_gx_blender_materials_to_glb_dbe4b3ee.txt
transcript_file_pt3: _Archive/processed_sources/20260916_gx_blender_to_unreal_import_b65aba4b.txt
fetched: 2026-09-16 via youtube-transcript-api (en - ORIGINAL language, confirmed by yt-dlp probe)
upload_date: 2025-11-26 (i82_Rx1OUe0); 2023-01-29 (2sgKu0bKUwU); 2026-05-15 (AK4tVgdWVo4) - all from yt-dlp sidecars, --fetch-upload-date, actually run
channel: Deayan Studios; Aneeqa Younas; jbdtube
source_title: "Master Exporting in Blender - Fix GLB/glTF Exports" (+ "Blender materials export to GLB/GLTF", "Import Blender 3D Scene in Unreal Engine")
language: en (original)
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / Model to Walkable View`)
fact_yield: 21
promotional_ratio: low-medium - three straight technical tutorials; two close with course or Patreon plugs, none makes a capability claim
corroborates_existing: true
contradicts_existing: false
region: n/a - software capability
---

# Source Note - ⚠️⚠️ WHY appearance does not transfer, and exactly what it would cost to fix (YouTube i82_Rx1OUe0 +2)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none)

⚠️ **jbdtube also supplied the Bonsai→Twinmotion guide in the previous batch.** **These three were fetched to test the one finding that could change the walkable-view decision: that appearance does not survive an IFC→viewer export.** **It survives the test, and now has a mechanism and a price attached.**

## ⚠️⚠️ 1. THE MECHANISM — Blender's materials are not a transferable thing at all

**Demonstrated rather than asserted.** A model with a working shader is exported to GLB and opened in a glTF viewer:

> ***"This is how it will look in glTF viewer — it's COMPLETELY BLANK. It doesn't have those colours… The reason is these complex shaders. Now, these don't have to be complex — even if they were just one or two nodes blended together, Blender can understand them, but OTHER SOFTWARES will not be able to read Blender's internal materials."***

> **→ ⚠️⚠️ SO IT IS NOT A LOSSY TRANSFER, IT IS A NON-TRANSFER.** A Blender shader network is a Blender-only construct. **The only universal carrier is an IMAGE TEXTURE** — *"there is a universal way of transferring your materials… and the way is you use textures."*

**And the third source hits the same wall from the Unreal side, independently:** a bump he had authored procedurally simply did not arrive, and his conclusion is a rule — ***"use PIXEL TEXTURES rather than PROCEDURAL MAPS."***

> **→ ⚠️ THIRD INDEPENDENT ARRIVAL at the same rule in two batches** (the Twinmotion guide reported no materials at all off a Bonsai model). **Procedural or node-based appearance does not leave the authoring tool. Baked images do.**

## ⚠️⚠️ 2. THE PRICE OF FIXING IT — and this is the part that decides the question

**Baking a shader into a texture is not one step. The prerequisites are the cost:**

| Required | Detail |
| :--- | :--- |
| **⚠️⚠️ A UV MAP on every object** | *"If it doesn't have a UV map, your textures are not going to work."* Quick path is Smart UV Project; controlled path is marking seams and unwrapping |
| An image to bake into | Square, power-of-two (1024×1024 used) |
| **⚠️ Render engine set to CYCLES** | EEVEE cannot bake |
| One bake **per channel** | Base colour, roughness, metallic… each its own image |

**⚠️ And a trap worth knowing: baking "combined" bakes the LIGHTING IN.** He demonstrates shadows becoming part of the texture, then moving the light and the shadow staying — *"it's like it's becoming twice as dark."*

> **→ ⚠️⚠️ FOR THIS PROJECT, THIS IS THE DECISIVE COST, AND IT IS BIGGER THAN "RE-DRESS THE SURFACES".** **An IFC model out of Bonsai carries no UV maps.** So a textured walkable view would mean **UV-unwrapping the whole apartment and baking multiple channels per material** — before any appearance decision is even made. **That is a modelling project, not an export step.**
>
> **→ AND IT SHARPENS THE RECOMMENDATION RATHER THAN CHANGING IT: for judging clearance and circulation, none of this is needed.** **Geometry and flat colour need no UV map and no bake.** ⚠️ **What these sources do NOT test is whether a plain Principled BSDF base colour — no node network — travels as a glTF PBR material. That is the glTF-native case, it is cheap to verify locally, and it should be verified rather than assumed.**

## ⚠️⚠️ 3. What glTF and GLB actually are — and why GLB, for a web viewer

**The name decodes to the design intent**: **GL** from graphics library, **TF** = **transmission format** — *"made for easy transferability over the internet, so it has to be extremely fast and lightweight."*

> **This made it the gold standard for interactive web elements… and also game assets, VR and AR, where you require these objects to be rendered in real time without any lag.**

| | **glTF** | **GLB** |
| :--- | :--- | :--- |
| Structure | Mesh, textures and dependencies in **separate files** that must stay co-located | **⚠️⚠️ Everything in ONE binary file** |
| Risk | *"Very prone to errors"* through missing dependencies | No dependency issues |
| Loading | Slower | *"A lot more robust and even faster to load, especially for web applications"* |

> **→ ⚠️⚠️ THIS IS DIRECT EXTERNAL SUPPORT FOR THE PROPOSED FIRST RUNG.** **The format this project's pipeline already names as its 3D view was designed for exactly the use being considered — real-time viewing in a browser — and GLB is the correct variant of it.** **Nothing exotic is being proposed.**

## ⚠️⚠️ 4. What silently does NOT export, beyond materials

**The failure is quiet, which is what makes it worth recording:**

- **⚠️⚠️ PROCEDURAL GEOMETRY EXPORTS AS ITS PRE-MODIFIER STATE.** glTF stores real mesh data only; a geometry-node modifier is a relationship, not mesh. **Export an arrow built by nodes on a cube base and you get… the cube.** *"The same would happen for FBX and OBJ as well."*
- **⚠️ Applying the modifier is NOT sufficient on its own**: instances need a **Realize Instances** node first, and curves a **Curve to Mesh** node, or they are not converted.
- **⚠️⚠️ APPLY SCALE, ideally all transforms** — *"I've seen that you have it scaled up or down and you think it looks absolutely perfect, but when you actually export it, the entire scaling goes completely haywire."*
- **⚠️ Pack all resources and purge unused data before exporting** (File → External Data), so nothing is left pointing outside the file.

> **→ ⚠️ MOSTLY NOT A RISK ON THIS PROJECT, because a Bonsai/IFC model is real mesh rather than node-generated — but the SCALE point is, and it is cheap insurance.** **⚠️⚠️ The general principle is the one to keep: the exporter writes what is BAKED INTO THE MESH, not what you see in the viewport.** **That is the same class of defect as this vault's rule that generated geometry is placed rather than associated.**

## ⚠️ 5. Optimisation, which matters because of §6

- **Decimate (planar)** to strip redundant faces; **Triangulate** for formats that dislike n-gons and quads.
- **⚠️⚠️ Keep texture resolution as low as the use allows** — *"the larger this is, the more memory it's going to take, the larger your files are going to be, the slower it's going to be to load on websites."*

## ⚠️⚠️ 6. Blender → Unreal: GLB beats FBX, and the file is enormous

**A worked import of a full architectural scene with interior:**

- **⚠️ He prefers GLB over FBX for this** — *"compared to FBX, I think I would choose GLB. It works a little bit better. It lets me do less things."* PBR materials arrived; glass *"doesn't look bad."*
- **⚠️⚠️ BUT THE HONEST REFRAIN, repeated three times: *"either way you need to do some work"*, *"you always need to fix things one way or the other."*** **On camera: missing textures, a lost procedural bump, and flickering against Unreal's default landscape.**
- **⚠️⚠️ THE GLB WAS "ALMOST HALF A GIGABYTE"** — notably heavier than the FBX — and he warns to allow **at least half an hour** for export plus import.

> **→ ⚠️⚠️ THE HALF-GIGABYTE FIGURE IS THE ONE TO CARRY INTO THE DECISION, because it cuts against the WEB rung specifically.** **A textured architectural scene is not a web-deliverable file.** **⚠️ But it is not this project's case either: his scene is a whole building with exterior, landscape and imported asset libraries; an untextured single apartment is a different order of magnitude.** **→ The rule that follows is simple and testable: the web rung survives only if the model stays untextured or lightly textured — which is the same conclusion §2 reaches from the cost side.**
- Unreal's own offer, stated: first-person, third-person, vehicles and VR templates, and door-opening interactions.

## Routing

- §1, §2 → [[00_Master/Model_and_Views|One model, many views]], sharpening the appearance-does-not-transfer finding with its mechanism and price
- §3, §5, §6 → same page, into the walkable-view rungs
- §4 → same page, as the export-integrity rule. **It was considered for Model to Drawing Pipeline and not sent there**: that page is about 2D sheet generation, and this is a 3D export concern

## What was NOT taken

- Blender UI paths, menu locations, version numbers, and the course/Patreon plugs.
- Any claim about which renderer looks better — outside this project's use.
- **Nothing routed to `16_Legal_and_Regulations/`** — no regulatory claim is made.
