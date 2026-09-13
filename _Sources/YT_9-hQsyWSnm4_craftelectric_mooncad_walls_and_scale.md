---
source_type: video transcript (plugin/CAD developer channel, practical walkthrough of a tool in active development)
source_url: https://www.youtube.com/watch?v=9-hQsyWSnm4
video_id: 9-hQsyWSnm4
transcript_file: _Archive/processed_sources/20260913_craftelectric_mooncad_walls_and_scale_0f11f132.txt
fetched: 2026-09-13 via youtube-transcript-api (ru auto captions - ORIGINAL language)
upload_date: 2025 (confirmed via yt-dlp metadata)
channel: Craftelectric
source_title: "MoonCad - построение стен коммерческого помещения ~130 м², подложка и масштаб"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`, `Quantities / Measurements`)
fact_yield: 9
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - a software tool, not a renovation source
---

# Source Note - Craftelectric / MoonCad: Two Conventions This Project Does Not Have (YouTube 9-hQsyWSnm4)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this was processed, and a triage correction

**Deferred on 2026-09-08 as the Craftelectric channel's second Tier 2 single, characterised then as "wall-tracing over a scaled raster underlay" - i.e. expected to be thin.** ⚠️ **It is not thin. It contains two modelling conventions this project does not currently state anywhere**, both of which bear directly on `data/canonical/` and on the raster-registration procedure. **Recorded as a triage correction: "wall-tracing over a scaled underlay" understated it.**

⚠️ **Note this is a DIFFERENT tool from the same developer** - **MoonCad** (transcribed variously «Moon Cat», «Mooncad»), a Russian CAD in active development, not the SketchUp plugin of [[_Sources/YT_A1HxpHxrvv4_craftelectric_cable_enclosure_schema|A1HxpHxrvv4]]. He states the interface is changing, so **no UI specific is routed.**

## ⚠️⚠️ Rules / Heuristics - Register the Scale on the LONGEST Known Distance

**Setting the scale of a plan underlay, stated with the reason:**

> «Нужно выбрать самое большое известное расстояние на вашем плане... Даже 5-6 м уже будет достаточно, но **чем длиннее выбранное расстояние, тем точнее получится масштаб**.»

His own registration uses **18,229 mm** - the full length of the premises.

- **⚠️⚠️ This vault already holds the COMPLEMENT of this rule and not the rule itself.** `f0EU_xbavEA` gave **two-point scale verification** - register on one printed dimension, verify on a *second, independent* one ([[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §6). **This adds WHICH dimension to register on: the longest available.**
- **The two combine into one procedure: REGISTER on the longest known dimension, VERIFY on a second independent one.** The reasoning is sound and not merely stated - the relative error of a registration scales inversely with the length of the reference, so a short reference multiplies its own reading error across the whole drawing.
- **⚠️ Directly actionable here**: `tools/layout/raster_fidelity.py` registers mm→px from the PDF's hatched wall faces against a frozen registration. **Whether that registration uses the longest available reference is a checkable question, and this gives the reason to ask it.**
- **He then aligns the underlay so the main internal walls sit on the zero axes** - a datum-setting move, and the same concern as the datum question `Drawing_Conventions_From_Practice.md` §1 records as still open.

## ⚠️⚠️ Rules / Heuristics - A Wall's Side Is Relative to Its DIRECTION, Not to the Screen

**A wall is drawn on a base line, and its body sits left, centred, or right of that line. The gotcha, stated explicitly:**

> «Левая и правая сторона считаются не относительно экрана, а **относительно направления базовой линии от первой точки стены ко второй**... если я нарисую такую же стену в обратную сторону, снизу вверх, то при выборе "слева" стена окажется уже с другой стороны.»

**His rule: «Когда мы рисуем контур помещения, лучше идти последовательно в одном направлении по периметру» - traverse the perimeter consistently in one direction, and the wall-to-baseline relationship stays predictable.**

- **⚠️⚠️ This is a real convention this project needs and does not state.** `data/canonical/wall_blocks.csv` and `tools/layout/build_wall_corners.py` deal with exactly this - which side of a centreline the solid occupies, and which wall owns an L-corner. **A direction-dependent side convention is a live hazard the moment walls are entered or edited by hand.**
- **→ Worth recording as a candidate convention for `.agents/skills/residential-bim-geometry-rules/`**: if a wall carries a direction, traverse consistently; if it does not, say so explicitly so nobody assumes one.

## ⚠️ Durable Facts - Wall Material Is Not Cosmetic

**Wall types in the worked project: concrete, brick, ГКЛ. His stated reason for carrying the material, and it is an electrical-design reason rather than a drafting one:**

> «Это важно не только для цвета на плане. Материал стены дальше влияет на понимание объекта и подготовку электрики - **где будут размещаться розетки и выключатели, как смотреть развёртки, как вести трассы и какие работы могут появиться в проекте**.»

- **→ Wall material drives socket and switch placement, how the развёртки are read, how runs are routed, and WHAT WORKS APPEAR IN THE PROJECT.** That last clause is the cost link: chasing brick, chasing concrete and fixing to ГКЛ are different operations at different rates.
- **⚠️ This project already holds `data/canonical/wall_materials.json` and `room_rollouts.csv`.** **This supplies the argument for why the material must reach the electrical take-off and the BOM, not just the drawing** - and it pairs directly with the chase/containment quantities in [[_Sources/YT_A1HxpHxrvv4_craftelectric_cable_enclosure_schema|A1HxpHxrvv4]], where `штроба кирпич 20x20` is a priced line whose rate depends on the substrate.

## Durable Facts - Two Smaller Items Worth Keeping

- **⚠️ A minimum-area threshold suppresses spurious rooms: closed contours below 1.5 m² do not become rooms by default**, «чтобы случайные маленькие замкнутые области не превращались в комнаты». **A deliberate noise-rejection threshold on automatic region detection** - the same class of decision as this project's gates distinguishing a genuine L-corner void from an artefact.
- **Floor-level parameters are set once per storey**: wall height (3,300 mm here), ceiling type (монолит), floor type (со стяжкой). **Storey-level defaults rather than per-element repetition.**
- Snapping aid worth noting: hovering ~2 s over an existing angled wall raises parallel and perpendicular guides relative to *that* wall - **useful specifically for non-orthogonal geometry**, which is where this project's corner ledger is known to be weakest.

## Confidence & Evidence Notes

- **`single-account`**, developer demonstrating his own tool, in active development. **No UI detail is routed.**
- **ASR**: adequate. «Moon Cat»/«Mooncad» inconsistent, «рассвортки» for развёртки, «18.229. 229 мм» garbled for 18,229 mm.
- **`corroborates_existing: true`** for the underlay/scale procedure; **the longest-reference rule and the wall-direction convention are NEW to this vault.**
- **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §6** - the longest-reference registration rule, alongside the existing two-point verification.
- **`18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md` (NEW PAGE)** - wall material as a driver of electrical works and rates.
- **⚠️ `_Inbox/planning/` - the wall-direction convention, flagged as a candidate for `.agents/skills/residential-bim-geometry-rules/`.**
- **5b**: no prices; no conversion owed.
