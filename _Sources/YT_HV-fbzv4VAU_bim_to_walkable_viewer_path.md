---
source_type: video transcript (a worked Bonsai/Blender-BIM to Twinmotion export tutorial, plus two sources on the Unreal route and one on render post-production)
source_url: https://www.youtube.com/watch?v=HV-fbzv4VAU
video_id: HV-fbzv4VAU
covers_also: dnqlClsPD4g, U4AHDngSb7k, iQPKN271msY
transcript_file: _Archive/processed_sources/20260916_bim_to_walkable_viewer_path_0c5eb9db.txt
transcript_file_pt2: _Archive/processed_sources/20260916_wt_gpt6_blender_unreal_house_110327f5.txt
transcript_file_pt3: _Archive/processed_sources/20260916_wt_twinmotion_rendering_ai_tools_ce2cf598.txt
transcript_file_pt4: _Archive/processed_sources/20260916_wt_airbnb_photos_to_3d_blender_bb505f14.txt
fetched: 2026-09-16 via youtube-transcript-api (en - ORIGINAL language, confirmed by yt-dlp probe)
upload_date: 2026-08-21 (HV-fbzv4VAU); 2026-09-09 (dnqlClsPD4g); 2026-08-01 (U4AHDngSb7k); 2026-09-08 (iQPKN271msY) - all from yt-dlp sidecars, --fetch-upload-date, actually run
channel: jbdtube; Bad Decisions Studio; ViaRender; Luke Byrne (AI Luke)
source_title: "Videoguide - Export Blender BIM Model, Import in Twinmotion 2026" (+ three on the Unreal route, render post-production, and photos-to-3D)
language: en (original)
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / Model to Walkable View`)
fact_yield: 19
promotional_ratio: ⚠️ VARIES SHARPLY - pt1 is a straight workflow tutorial with course plugs; ⚠️⚠️ pt2 is a course-selling show whose relevant segment is explicitly UNFINISHED; pt3 and pt4 are product-led. Weighted per item.
corroborates_existing: partly
contradicts_existing: false
region: n/a - software capability
---

# Source Note - ⚠️⚠️ IFC to a walkable view: the path works, and it carries geometry but NOT appearance (YouTube HV-fbzv4VAU +3)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none)

## ⚠️⚠️ Why this group was fetched

**The owner is deciding whether to add a WALKABLE view to a pipeline whose 3D output is already Blender/glb off an IFC** ([[00_Master/Model_and_Views|One model, many views]]). **The recommendation on the table was: glb viewer first, Twinmotion second, Unreal only if VR is wanted.** **These four test that recommendation against people who have actually done it.**

## ⚠️⚠️ 1. THE PATH WORKS, AND THE EXPORT DETAIL IS SPECIFIC

**A worked Bonsai (Blender-BIM) → Twinmotion transfer, with the choices named:**

- **Formats that work: GLB, glTF and FBX** — he imports all three side by side and they arrive equivalently. **GLB is his default "because everything is included, like materials and textures"**; glTF splits into separate files.
- **⚠️⚠️ Do NOT "export all"** — it exports every individual object. **Isolate what you want, then "export visible" or "export selected".**
- **⚠️⚠️ KEEP THE HIERARCHY ON IMPORT** — *"if you collapse all, everything is going to be one single object, and then it's longer to detach and edit."* **He imports three collections (roof, ground floor, first floor) and they arrive as three folders of meshes.**
- **Axes: up = Z, forward = X.** Scale is auto-detected. **⚠️ If the Blender model used modifiers, check "apply modifiers" — in a Bonsai workflow they were already converted to IFC geometry.**

> **→ ⚠️⚠️ THIS CONFIRMS THE PROPOSED ROUTE IS REAL AND SHORT.** **The project's bundled Blender already ships the glTF exporter, and `Model_and_Views.md` already names glb as a view. Nothing new has to be invented.**

## ⚠️⚠️ 2. THE COST NOBODY MENTIONS UP FRONT: appearance does not transfer

> ***"You can see it doesn't have materials… it didn't work again with materials in Bonsai 3D, knowing that I need to do these either with the rendering software."***

**Everything visual is re-authored in Twinmotion: materials dragged from a library onto surfaces, and mapping fixed by hand.**

- **⚠️ BIM geometry arrives with NO UV MAPPING**, so library materials appear invisible until mapping is set. **His fix is CUBIC projection — *"since this is architecture, you will not have any problems, because everything is kind of straight."*** **Anything more complex has to be unwrapped back in the modelling tool.**
- **⚠️⚠️ Use "apply to object" or "apply to selection", NOT "replace material"** — replace changes every surface sharing that material, which after a BIM import is most of the model.
- **⚠️ Low-poly BIM placeholder assets should be DELETED, not carried over** — trees, furniture and terrain from the BIM authoring tool are deliberately low-poly, and are replaced with library assets on arrival.

> **→ ⚠️⚠️ THE FINDING FOR THIS PROJECT: an IFC-to-walkable pipeline transfers GEOMETRY, and appearance is a second, manual body of work in the destination tool.** **That is a real cost and it lands on the wrong side of this project's own architecture, because materials re-authored in Twinmotion are NOT derived from the model — they are a second source of truth that will drift.**
>
> **→ WHICH ARGUES FOR SCOPE DISCIPLINE RATHER THAN AGAINST THE IDEA: if the walkable view is for JUDGING SPACE — does the passage work, is the clearance tolerable — untextured grey geometry answers it, and the material work is unnecessary.** **If it is for showing someone a finished-looking room, the appearance work is the majority of the effort and it duplicates decisions the vault already records in text.**

## ⚠️ 3. Unreal — the one source that tried it end-to-end did not finish, and says so

**A show recreated a real estate listing: an agent read the listing's photos and floor plan by computer use, modelled it in Blender, and ported it to Unreal.** **Their stated reason for Unreal is exactly the owner's**:

> *"Inside Blender you can model it, but **only inside Unreal Engine can you create an interactive walkthrough that you can turn to a website and send to people**."*

**⚠️⚠️ AND THE ACCURACY QUESTION WAS RAISED BY THEIR OWN AUDIENCE, ACKNOWLEDGED ON CAMERA, AND LEFT UNANSWERED:**

> *"You guys were saying, okay, it made it, but **is it accurate? Do the dimensions read correctly?** Because it's nice as a fancy mockup, but **can I actually use it to build a virtual walkthrough for my clients?**"*

**They then show the result and concede: *"Is it perfect? Absolutely not."* *"There are differences probably in measurement, probably in the design."* The segment ends mid-experiment — *"the experiment was halfway through… in the next episode you're going to see the complete."***

> **→ ⚠️⚠️ SO THE ONE END-TO-END UNREAL DEMONSTRATION IN THIS BATCH DEMONSTRATES THE WORKFLOW AND NOT THE FIDELITY — and the fidelity is the only thing that would make it useful here.** **Recorded as: the route exists; its dimensional accuracy is unevidenced by this source.**
>
> ⚠️⚠️ **Heavy course-selling throughout, with the segment used as a lead-in to a paid programme, plus "there's a small window before everyone finds out" urgency. No capability verdict is carried from it.**

**⚠️ The other Unreal account, from the practitioner in the companion note, is more useful and less excited**: **~2 hours over two sessions** to get first- and third-person walkthrough blueprints, camera sequences, procedural placement and material swaps — **using MCP for the blueprint/graph work specifically, because that is the part not worth scripting.**

## ⚠️ 4. What the batch says about the RUNG BELOW Unreal

- **⚠️⚠️ An interactive WEB APP is named as an intermediate output, before Unreal** — *"create interactive web apps with controls, labels, filters"* — and a third party shipped game assets from Blender into a **three.js** site. **→ Corroborates the proposal that a browser-based walkable view is a real rung and not a compromise.**
- **⚠️ Twinmotion's pitch in this batch is rendering, not walking**: the dedicated Twinmotion source is entirely foliage, lighting, camera, AI upscalers and Photoshop post-production. **Nothing in it is about dimensional judgement or circulation.** **→ Twinmotion is an IMAGE tool in practice, whatever its walkthrough features. It belongs on the "show someone" branch, not the "decide something" branch.**
- **⚠️ Low yield, recorded honestly**: the photos-to-3D source is a marketing-video workflow (listing photos → rough Blender model → AI video), and its one transferable point is negative — **AI video generated straight from photos blends rooms together *"because AI doesn't know where one room stops and the next one begins"*, and building the model first is what fixes the inconsistency.** **An argument for having a model, not for any tool.**

## ⚠️⚠️ 5. What this means for the decision on the table

**Recorded as analysis, flagged as such, because the owner asked for it:**

1. **The route is confirmed and short** (§1), and the project already emits the input format.
2. **Appearance does not transfer** (§2) — so a textured, realistic walkthrough is a second project, and one that would create a second source of truth for materials.
3. **The only end-to-end Unreal demonstration available does not evidence dimensional accuracy** (§3), which is the property this project would be relying on.
4. **A browser/web walkable view is independently named as a real intermediate** (§4).

> **→ NOTHING HERE CHANGES THE PROPOSED ORDER — glb walkable view first — and §2 strengthens the case for stopping there**: **for judging clearance and circulation, untextured geometry is not a limitation, it is the point.**

## Routing

- §1, §2 → Model to Drawing Pipeline as an export-path record, and flagged to [[00_Master/Model_and_Views|One model, many views]]
- §3, §4, §5 → Agent-Connected CAD and [[00_Master/Model_and_Views|One model, many views]]

## What was NOT taken

- Version numbers, library names, plug-in links and pricing.
- The course pitches, the "small window" urgency framing, and the AI-video product promotion.
- **Any capability verdict from the unfinished Unreal experiment** (§3).
- **Nothing routed to `16_Legal_and_Regulations/`** — no regulatory claim is made.
