---
source_type: video transcript (kitchen fabricator channel, dimensional-tolerance explainer)
source_url: https://www.youtube.com/watch?v=BOIJzganJ9U
video_id: BOIJzganJ9U
transcript_file: _Archive/processed_sources/20260914_cappuccino_furniture_gaps_tolerances_e7557a6f.txt
fetched: 2026-09-14 via youtube-transcript-api (ru-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2020-01-21 (confirmed via yt-dlp metadata)
channel: CAPPUCCINO - студия интерьера и мебели (Odessa / Kyiv, Ukraine)
presenter: Юрьев Юрий
source_title: "ЗАЗОРЫ В МЕБЕЛИ. КАКИЕ СТАНДАРТНЫЕ ЗАЗОРЫ?"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Furniture`, `Design and Ergonomics`)
fact_yield: 11
promotional_ratio: none
corroborates_existing: true
region: ukraine_odessa_kyiv_2020 - flagged; a fabricator's shop convention, NOT a norm
delivery_model: fabricator
---

# Source Note - CAPPUCCINO: ⚠️⚠️ FURNITURE GAPS — a Tolerance Argument That Mirrors This Project's Own, at a Tenth the Scale (YouTube BOIJzganJ9U)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**Four minutes, 51k views, no promotion at all.** ⚠️ **The highest value-per-minute source in this round, and the one most directly connected to this project's own geometry discipline.**

## ⚠️⚠️ 1. The argument: furniture cannot be made millimetre-exact, and he builds the case from tolerances upward

> *"Мебель сделать миллиметр в миллиметр… просто возьмите постичь [примите как есть] — ни один [производитель] не сведёт."*

**His stack of contributing tolerances**: every instrument, every machine, every material, and **the geometry of the room.**

### ⚠️⚠️ The material tolerance, with a figure and an accumulation argument

> *"Возьмём производителя ЛДСП Egger. Каждый лист материала имеет свою погрешность: один лист может быть **17,8 миллиметров**, другой лист может быть **18** с копейками. Кажется, это мелочь — но **на 5 метров набегает плюс-минус 1 миллиметр**. И это только по ЛДСП."*

> **→ A NOMINAL 18 mm BOARD IS 17.8–18.x mm, AND THE ERROR ACCUMULATES ALONG A RUN.** ⚠️ **This is the same reasoning structure as `00_Master/Geometry_Variance_Study.md`, which measured −45 to +30 mm between the developer plan and three surveyed flats and set this project's ±50 mm nominal.** **Same argument, two orders of magnitude apart — and the furniture is ordered against the tighter one.**

### ⚠️⚠️ …but the dominant term is the ROOM, and he says so

> *"Наибольшую проблему составляет **геометрия помещения**, потому что, к сожалению, ремонт вам делают **не роботы, а живые люди**: рука может дрогнуть, стена может где-то оказаться пузом, либо угол 90 градусов — а [он] 90,5 или 90,05. И это всё кардинально влияет на конечный размер мебели и на то, как она станет."*

> **⚠️⚠️ A FABRICATOR NAMING OUT-OF-SQUARE ROOM GEOMETRY AS THE LARGEST SOURCE OF ERROR IN FITTED FURNITURE.** **This is independent corroboration, from the furniture trade, of the entire premise behind this project's wall-geometry gating, the corner ledger and the variance study.** ⚠️ **And it is the reason the `обмерочный чертёж` matters: the furniture order is where the building's real geometry is finally paid for.**

## ⚠️⚠️ 2. The three gaps, with numbers

| Gap | Figure | Notes |
| :--- | :--- | :--- |
| **Furniture to wall** | **⚠️⚠️ 3 mm per wall, MINIMUM, even with perfect walls** | *"Даже в таком случае мебель нужно делать на 3 миллиметра [меньше] от каждой стены… это такой стандарт, для того чтобы можно было **монтировать без проблем**."* |
| **Upper modules to ceiling** | **⚠️ down to 6 mm achievable** | With **3D-adjustable hangers** (he names the Italian maker **Camar**); driven by floor, ceiling and wall level |
| **Between fronts** | **⚠️ 3 mm, their standard** | Every company sets its own, driven by front thickness, front shape and opening angle |

> **⚠️⚠️ THE 3 mm PER-WALL FIGURE IS THE ONE TO CARRY.** **It is not a quality margin — it is the clearance required to physically install the unit at all.** **→ A kitchen run modelled hard against two wall faces is, in reality, 6 mm shorter than the opening.** ⚠️ **Directly relevant to how built-in furniture is dimensioned against `data/canonical/` and to `room_rollouts.csv`.**
>
> ⚠️ **And the 6 mm ceiling gap is what makes a "kitchen to the ceiling" physically possible** — a topic this vault covers from the design side but not from the mounting side.

## ⚠️⚠️ 3. The colour trap that only appears once it is built

> *"Если вы выберете фасады тёмного цвета, а корпус сделаете светлым, то **даже через эти 3 миллиметра будет видна светлая кромка корпуса**."*

**His fix: ask the designer to specify the front edge of the carcasses in dark, or as close to the front colour as possible.**

> **→ ⚠️⚠️ A 3 mm GAP IS A 3 mm STRIPE OF CARCASS COLOUR, REPEATED AROUND EVERY FRONT.** **Invisible in a render, unavoidable in reality, and fixed only at the ordering stage.** **New to this vault, and it belongs with the design-vs-built gap this project keeps finding.**

## ⚠️ 4. Corner and 45° modules take larger gaps

> *"На кухне, где есть модуль под 45 градусов, зазоры будут гораздо больше, чем на обычной ровной кухне, для того чтобы открыть фасад."*

> ⚠️ **Read with the corner-kitchen and corner-sink critiques already on [[03_Kitchen/analysis/Layout_Sizing_and_Ergonomics|Layout, Cabinet Sizing and Ergonomics]] and [[03_Kitchen/analysis/Worktops_and_Backsplash|Worktops & Backsplash]]. This adds the mechanical reason a 45° module looks looser: the front needs more clearance to swing.**

## ⚠️ What was deliberately NOT extracted

- **Camar as a brand recommendation** — the **3D adjustability and the 6 mm result** are kept; the brand is not routed.
- **No prices, no regulatory content.**
- **⚠️ Nothing here is a norm.** **These are one Ukrainian fabricator's shop standards.** **The transferable question is not "are his 3 mm correct" but "what does OUR fabricator use, and does our model leave room for it."**

## Source Notes

CAPPUCCINO (YouTube), presenter **Юрьев Юрий**, 2020-01-21, 4 min, **read in full**, `ru-orig` verified. ⚠️ **English title in the channel listing over Russian audio.** `promotional_ratio: none` — no pitch, no product, a sign-off wishing the viewer *"пусть мебель вам приносит удовольствие, а не разочарование от щелей."*

**Claims are this fabricator's shop practice, as opinion.** ⚠️ **The Egger 17.8 mm figure is the only measurement in the source and is stated from trade experience, not shown.** ⚠️ **The ±1 mm over 5 m accumulation is his arithmetic and is not derived on camera — it is plausible for a stack of boards but is not a verified figure.**
