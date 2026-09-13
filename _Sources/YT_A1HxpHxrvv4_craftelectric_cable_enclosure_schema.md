---
source_type: video transcript (plugin developer channel, feature walkthrough of his own tool)
source_url: https://www.youtube.com/watch?v=A1HxpHxrvv4
video_id: A1HxpHxrvv4
transcript_file: _Archive/processed_sources/20260913_craftelectric_cable_enclosure_schema_9cb464f0.txt
fetched: 2026-09-13 via youtube-transcript-api (ru auto captions - ORIGINAL language)
upload_date: 2025 (confirmed via yt-dlp metadata)
channel: Craftelectric
source_title: "Craft Electric Tools - назначение марки кабеля, оболочек и электрических групп"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Switches / Sockets / Cables`, `Quantities / Measurements`)
fact_yield: 10
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - a software tool, not a renovation source
---

# Source Note - Craftelectric: A Cable/Enclosure Data Model, and the Cardinality That Makes It Work (YouTube A1HxpHxrvv4)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this was processed

**Named on 2026-09-08 as the Craftelectric channel's substantive item** - "electrical quantity take-off from a 3D model (cable/гофра/штробы)" - and deferred as a Tier 2 single. It is read here for its **data model**, because this project's [gap analysis](../_Inbox/planning/toolchain_gap_analysis_20260908.md) records that **`ELE-01`'s BOM line is currently unmeasured**, and because `Drawing_Conventions_From_Practice.md` already holds the вывод/розетка element split from RemPlanner. **It is the developer demonstrating his own plugin, so `promotional_ratio: medium` - but the schema is the content.**

## ⚠️⚠️ Durable Facts - The Central Design: Two Orthogonal Classifications With Different Cardinality

**This is the most transferable thing in the source, and it is a modelling decision this project has to make for its own electrical BOM.** A drawn line carries two independent classifications:

| | **Кабель (conductor)** | **Оболочка (containment)** |
| :--- | :--- | :--- |
| **What it is** | The cable or wire itself, by marka - `3x2.5`, `3x1.5`, `1x6` | **The METHOD OF LAYING** - гофра, штроба, лоток, траншея, гильза, труба |
| **Cardinality** | **Exactly ONE per line.** Assigning a second replaces the first | **MANY per line, simultaneously** |
| **Display** | Colour-coded per cable group | **Only ONE enclosure renders at a time**, deliberately |

- **⚠️⚠️ The worked case that proves the cardinality is necessary: a cable runs in гофра for most of its route, and passes through a wall inside a гильза (sleeve). Both are true of the same line at once.** One cable, two containments.
- **⚠️ The display rule is a deliberate design decision, not a limitation**: assigning a second enclosure **suppresses the first one's colour** (it goes black) «чтобы исключить путаницу при визуализации, так как оболочки могут перекрывать друг друга». **A category filter then highlights only the lines carrying the selected enclosure.**
- **→ Why this matters for `ELE-01`: the cable length and the containment length ARE NOT THE SAME NUMBER, and a BOM that carries one quantity per line cannot express the difference.** A 12 m circuit might be 12 m of cable, 7 m of гофра, 4 m of штроба and 0.4 m of гильза. **Any take-off that prices "cable run length" once has already lost the containment quantities, which are separately purchased materials and separately paid labour.**

**Containment entries carry material and size as parameters**, from autocomplete or free text: `гофра ПВХ 20`, `штроба кирпич 20x20`, `труба металл 25`. **Custom categories can be added.**

**A third, independent classification: электрическая группа (circuit)** - named per real circuit: «Розетки зал», «Спальня 1», «Освещение зал», «Коридор», «ЗУ» (earthing). **Assigned to lines the same way.**

## ⚠️⚠️ Rules / Heuristics - The Output Is a Complete Take-Off

**The кабельный журнал (cable log) report, per circuit group:**

- The **electrical group name** and the **total length of that group**.
- The **cable marka** used for it.
- **The laying method(s) AND their lengths, specifically for that group** - «штроба кирпич, гильзы, а также их длина».
- **A final consolidated materials list with quantities.**
- **A copy button → paste into Excel for further processing.**

**→ That is quantity take-off producing exactly the two things a cost join needs: a resource identity and a quantity, per circuit, with containment separated from conductor.** ⚠️ **It stops at the same boundary as every other tool in this batch - it produces quantities and prices nothing.**

## ⚠️ Durable Facts - Attributes Live on the Line, Not on the Grouping

**A grouping button auto-creates five groups as VIEWS**: a combined view (circuit name + cable marka together), cables by marka, electrical groups each separate, enclosures (all штробы/гофры/гильзы), and **an archive containing every line in the project**.

- **⚠️⚠️ Ungrouping is lossless - «все линии сохранят свои атрибуты: марку кабеля, группу, способ прокладки».** The attributes are properties of the line; the groups are a presentation of them.
- **→ This independently corroborates two conventions this vault already holds from RemPlanner** ([[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §2): that **"an element property can render differently per sheet"** and that **"grouping is a stored relation, not proximity."** **Two unrelated Russian tools, same architectural choice** - which is about as strong as convention evidence gets in this vault.

## Confidence & Evidence Notes

- **ASR quality: good for this subject class** - a prepared narration. Minor: «3 на полтора» for 3x1.5, «ждуб»/«ЗУ» for заземление, «шторма» for штроба, «трубаметалл» run together.
- **`single-account`** - one developer describing his own tool. **Nothing is verified; the schema is simply observable.**
- **`corroborates_existing: true`** for the property-versus-grouping convention. **The cable/enclosure cardinality split is NEW to this vault.**
- **No prices anywhere; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md` (NEW PAGE)** - the two-classification schema, the cardinality rule, the cable-log output.
- `18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §2 - a cross-reference for the property-versus-grouping corroboration.
- **⚠️ `_Inbox/planning/` - flagged as an input to the `ELE-01` BOM design**, which the gap analysis records as unmeasured.
- **5b**: no prices; no conversion owed.
