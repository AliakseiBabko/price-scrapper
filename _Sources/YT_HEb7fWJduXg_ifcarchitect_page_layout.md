---
source_type: video transcript (BlenderBIM/IFC specialist channel, step-by-step project part 5)
source_url: https://www.youtube.com/watch?v=HEb7fWJduXg
video_id: HEb7fWJduXg
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_page_layout_b1124fa4.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2022-12-13 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "BlenderBim Beginner Tutorial - Step by Step Project - Part 5 - Page Layout in 18mins"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 13
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: ⚠️⚠️ THE SHEET IS AN SVG FILE ON DISK, ASSEMBLED BY HAND IN INKSCAPE - Which Settles the Two-Engine Question (YouTube HEb7fWJduXg)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️ Dating caveat, and why it is read anyway

**BlenderBim-era (2022-12), and the add-on has since been renamed and its UI overhauled.** It is read because **the Bonsai-era series has only four parts and no page-layout instalment** — the rule set for this round is *read the old one only where no new one exists*, and that is the condition here. **UI paths and button names are discarded; the architecture is not, because the architecture is a file format and a directory on disk.**

`promotional_ratio: none` — free tools throughout, files given away on the OSArch community thread, no sponsor and no product.

## ⚠️⚠️ 1. CONFIRMED OUTRIGHT: the sheet is an SVG file on disk, edited in Inkscape

The previous source in this round inferred SVG+CSS from three indirect tells. **This states it as a file path:**

> *"Come here to your **Sheets file**, which is inside of your BlenderBim add-on — so it's here in your user, then **AppData / Roaming / Blender Foundation / Blender / [version] / scripts / addons / blenderbim / bim / data / sheets**. And you can see our sheet is there, `00`. And what you need to do is… **open with Inkscape**."*

And the final export: *"**it's saved as an SVG**… save as… **portable document format**."*

> **→ ⚠️⚠️ THE INFERENCE IN [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]] §4 IS NOW CONFIRMED, NOT INFERRED. Bonsai's drawings and sheets are SVG files in a known directory, and the delivery path is SVG → PDF.**
>
> **That is our pipeline's format and our pipeline's path.**

## ⚠️⚠️ 2. THE ANSWER ON SHEET ASSEMBLY: it is manual drag-and-drop in a vector editor

Bonsai's own contribution to the sheet is to **dump every printed drawing onto an A3 page in a heap**:

> *"We're just going to make an **A3 sheet**… with each drawing selected we're just going to click **add drawing to sheet**… and that's it, we've just got four drawings… say **create sheets**, and you can see **it's loaded everything onto this BEAUTIFUL MESS.**"*

Everything after that is done by hand in Inkscape: *"select each drawing and bring them out… I'm just going to adjust the plan so it's in the corner there, and then I'm going to put the detail down here… I think I'm going to put it there."*

> **→ ⚠️⚠️ BONSAI DOES NOT COMPOSE A SHEET. IT COLLECTS VIEWS ONTO A PAGE AND A HUMAN ARRANGES THEM BY EYE.**
>
> **This settles the gap analysis's open question, and the answer inverts the proposal.** [`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) §Kind 3 quotes Bonsai's stated limit — *"requires Blender's graphical interface for practical sheet assembly unless driving headless Python API scripts with rigid layout rules"* — and concludes **"two engines, split by whether the sheet is annotated."**
>
> **In practice there is one artefact, not two engines: an SVG file both tools can write.** And on the specific capability:
>
> | | Bonsai | Our SVG pipeline |
> | :--- | :--- | :--- |
> | **Drawing generation** (cut, hatch, tags, symbols) | **strong** — and we have nothing | weak |
> | **Sheet composition** | **manual, by eye, in Inkscape** | **already programmatic** |
>
> **→ ⚠️⚠️ ADOPTING BONSAI'S SHEET WORKFLOW WOULD BE GIVING UP A CAPABILITY WE ALREADY HAVE, NOT GAINING ONE.** The thing worth taking from Bonsai is **drawing generation**; the sheet layout is the half we are already better at, because a script places views the same way every time and a person does not.
>
> **And the shared format makes the split practical rather than theoretical**: Bonsai can emit the drawings, our generator can compose the page, because both speak SVG. ⚠️ **Untested, and it is now the concrete thing to test.**

## ⚠️⚠️ 3. The round trip is real — Bonsai preserves manual Inkscape edits across regeneration

This is the part that makes the shared artefact usable rather than a one-way dump. He arranges in Inkscape, saves, returns to Blender, regenerates — and the arrangement survives:

> *"We've saved the layout… but it gets printed still through BlenderBim. So if we go to BlenderBim and we say **create sheets again**, you can see **now everything is in its appropriate space**."*

Later, after changing the model and re-printing a drawing: *"go back to Inkscape… **you can see it's been updated, isn't that amazing.**"*

> **→ THE SHEET SVG IS A PERSISTENT SHARED DOCUMENT: BONSAI OWNS THE VIEW CONTENTS, THE EDITOR OWNS THE PLACEMENT, AND NEITHER DESTROYS THE OTHER'S WORK.**
>
> ⚠️ **This is a genuinely good architecture and it is the one to copy** — regardless of whether Bonsai is ever adopted. It is the same principle as generating our sheets from `data/canonical/`: **the content is derived, the arrangement is authored, and they live in one file without a merge step.**

## ⚠️⚠️ 4. Per-drawing element filtering is a CSS-LIKE SELECTOR stored as data on the camera

To drop the site terrain from one drawing but not others:

> *"We're going to go to **IFC object property sets**, and in here the **`EPset_annotation`** … where it says **`exclude`** … we're going to say **`.IfcGeographicElement[name="site"]`** … **so that's basically how you list something when you want to exclude it or include it.**"*

> **→ ⚠️⚠️ A CSS ATTRIBUTE SELECTOR — `.Class[attribute="value"]` — STORED IN A PROPERTY SET ON THE DRAWING'S CAMERA.** Both `exclude` and `include` exist.
>
> **Two things follow, and both matter.**
>
> **(a) It is further hard confirmation of the CSS architecture** (§1), now in the query layer as well as the styling layer.
>
> **(b) ⚠️⚠️ It is a better implementation of a convention this vault already holds.** [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §3 records *a services sheet has two audiences and therefore two configurations*, and the mechanism observed there was **layer toggles** — the reviewer's view shows furniture, the installer's does not. **A selector is strictly better than a layer**: it is declarative, it queries the model's own classes and attributes rather than a parallel layer taxonomy nobody maintains, and **it is data, so it can be committed, diffed and gated.**
>
> **→ Directly adoptable in our own generator**, which already has the model data to query. ⚠️ **And it is a third magic-string vocabulary** — after lowercase hatch materials and ALL-CAPS fill types — **but this one is a real query language rather than an enum, so the IDS argument applies differently: what needs validating is that the selector MATCHES SOMETHING.** A selector with a typo excludes nothing and reports nothing.

## ⚠️⚠️ 5. A concrete re-synchronisation order — the first hard answer to the restated headless question

The open item from the previous round was: *"which re-synchronisation steps does the GUI perform that a headless script must call explicitly?"* **Here is one, stated because it bit him:**

> *"You have to refresh it — **you need to print the drawing again**. So if I clicked the **create sheets** button now, you can see **nothing's changed** in the drawing here. So what you need to do is you need to go to my story plan, you need to click **create drawing**"* — and only then `create sheets`.

> **→ TWO-STAGE CACHE: `create drawing` (per view) MUST PRECEDE `create sheets` (per page). A sheet regenerates from the printed drawings, not from the model.**
>
> **This is exactly the shape of failure predicted from [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|fxpIg-su-00]] §2: the command succeeds, reports nothing wrong, and emits a stale sheet.** ⚠️ **A headless build must regenerate drawings before sheets, and a gate should assert that no sheet is older than the drawings on it** — which is a file-mtime or hash check, and cheap. **Add it to the restated open item as the first concrete entry.**

## ⚠️⚠️ 6. The final PDF may contain geometry that is merely HIDDEN, not absent

A view that renders past its own boundary is fixed by masking it:

> *"This guy hasn't quite been cut properly… **draw a rectangle** around the detail roughly where I want it to be **clipped**… select the shape, then select the detail in the layer, right click and say **clip**. And you can see that it's been clipped correctly."*

> **→ ⚠️⚠️ A CLIP HIDES GEOMETRY; IT DOES NOT REMOVE IT. The over-extending wall is still in the SVG, and therefore still in the PDF.**
>
> **This is a real integrity concern for a deliverable, and it is specifically dangerous for THIS project.** `tools/layout/vector_extent_oracle.py` **re-derives wall solids from the source PDF's vector content at check time** — an oracle the exporter does not consume. **Clipped-but-present geometry is exactly the kind of content a vector extractor reads and a human never sees.** A sheet produced this way would carry invisible extra geometry into anything downstream that parses it.
>
> ⚠️ **Recorded as a hazard of the workflow, not of our current pipeline** — we do not clip. **But it is a good argument for never fixing a rendering defect by masking it**, and for the oracle's design generally: *what is in the file is not what is on the page.*

## ⚠️ 7. …and it is the second instance of "the preview lies"

> *"For some reason when it creates it like this **it displays the view incorrectly and doesn't cut it sometimes** — you can see this wall's extending way past where it should — **but that gets sorted in Inkscape when you save it as a PDF.**"*

> **→ With [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|Part 4]] §6 (*"there is a preview, but it's not too accurate — when it prints, it's perfect"*), this is the second statement that the intermediate view is not authoritative.** ⚠️ **Mildly encouraging for a headless build, consistently**: the authoritative artefact is the printed file, which is the path a script uses anyway.

## Sheet conventions worth keeping

8. **⚠️ Each view arrives on the sheet as TWO objects: the drawing and its title tag** — *"there are two images per item, the top one is the tag basically… it just says **notification, name, scale**"* — and the tag must be **positioned by hand near its drawing.** **→ A per-view title block carrying number, name and scale is the convention; its placement is not automatic.**
9. **Drawing numbers and sheet numbers exist and cross-reference**: *"this is the **drawing number**… and this is the **sheet number** that it's on."*
10. **A drawing may appear on multiple sheets** — *"you can add drawings to multiple sheets, **this isn't Revit**."* ⚠️ Recorded as stated; the dig at Revit is not evaluated.
11. **⚠️ PDF export settings, and they matter**: *"make sure that you **don't have rasterized effects checked**, and that your **DPI is set at 300**."* **→ Keep the output vector; do not let an effect silently rasterise part of a sheet.** ⚠️ **Directly relevant to our own SVG→PDF step and to the presentation-pass rule already recorded** — *a presentation pass must not silently destroy the drawing's scale.* **Rasterising a layer is one way it does.**
12. **⚠️ The live sheet and the exported sheet are different artefacts**: after `save as`, *"**this is no longer a live file, this is a printed file**."* **→ Final cleanup happens on the dead copy, so it is not carried back — which also means it is not reproducible.** Anything fixed there is lost on the next regeneration.
13. **Excluding the terrain removed the ground line, so he drew one by hand** — a rotated annotation line for the natural ground level. **→ A filter that removes an element also removes what it implied**; the convention has to be restored separately.

## What was deliberately NOT extracted

- **All UI paths, panel names and the add-on directory layout** — BlenderBim-era and renamed since. The *existence* of a sheets directory of SVGs is architectural and is kept; its path is not.
- The drag-by-drag arrangement narration — mouse work, and the point of §2 is precisely that it is mouse work.
- The presenter's closing remarks about ending the series.
- **No prices, no regional claims, no regulatory content, no dimensional figures.**

## Source Notes

*Ifc Architect* (YouTube), 2022-12-13, 17 min, **read in full**. An entirely open-source workflow (Blender, BlenderBim, IfcOpenShell, Inkscape), with project files published free on the OSArch community thread — **this is the ecosystem this project already builds on.** **Claims are this presenter's, as opinion**; tool behaviours observed on one version. ⚠️ **Nothing is measured or verified.** ⚠️ **Fifth source from this presenter in the vault** — agreement with his other four is one voice repeating. ⚠️ **Dated**: see the caveat at the top. **The SVG-file-on-disk architecture is very unlikely to have changed** (the Bonsai-era Part 2 in this round still opens drawings in a browser and still promises a CSS video), **but it should be confirmed against our installed Bonsai 0.8.6-alpha260801 before the two-engine framing is formally revised.**
