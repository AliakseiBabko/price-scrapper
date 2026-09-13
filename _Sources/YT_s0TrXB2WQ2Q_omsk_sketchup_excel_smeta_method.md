---
source_type: video transcript (one-man finisher channel, method walkthrough)
source_url: https://www.youtube.com/watch?v=s0TrXB2WQ2Q
video_id: s0TrXB2WQ2Q
transcript_file: _Archive/processed_sources/20260913_omsk_sketchup_excel_smeta_method_6fddc2c8.txt
fetched: 2026-09-13 via youtube-transcript-api (ru auto captions - ORIGINAL language)
upload_date: 2020-11-22 (confirmed via yt-dlp metadata)
channel: Ремонт квартир Омск
source_title: "Как быстро составлять смету с помощью SketchUp и Excel"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Quantities / Measurements`, `Cost Drivers`)
fact_yield: 9
promotional_ratio: low
corroborates_existing: true
region: Omsk, Russia (level 1 - channel name and stated market)
delivery_model: Self-Managed / Itemized - a one-man finisher pricing his own work for clients
---

# Source Note - Ремонт квартир Омск: A Finisher Smeta From a 20-Minute Model, and a Closure Residual He Throws Away (YouTube s0TrXB2WQ2Q)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this was processed, and the rule that governs it

**Tier 2 single deferred from 2026-09-08, on the note: "Same idea, Russian, Omsk 2020. Rule 2: 2020 Omsk RUB is not comparable. Take the METHOD, discard every figure."** That instruction is followed exactly - **no price figure is carried from this source**, and in fact he gives almost none, since his subject is how to build the estimate rather than what anything costs.

**`promotional_ratio: low`** - no product is sold. ⚠️ **One caveat about the source register rather than its content: he offers a TORRENT link for SketchUp via his VK group.** Recorded because it places his tooling advice at the informal end of practice; it is not routed as advice, and it does not bear on the method.

## ⚠️⚠️ The Finding This Vault Should Act On: A Chain-Closure Residual, Observed and Discarded

**He draws the flat's perimeter in plan by typing each measured dimension, walking round the loop, and returning to the start. He then states, plainly, what happens:**

> «Программа делает углы в проекте автоматически 90 градусов, а в реальности такое бывает редко... когда мы пройдём по кругу и вернёмся в то место, откуда начали, размер последней линии может немножко отличаться от той, что записана у вас в тетрадке. Но думаю, такие погрешности не очень страшные.»

- **⚠️⚠️ That residual IS the chain-closure check, and he throws it away.** The perimeter is a known whole; he walks it; the discrepancy lands entirely in the final segment. **`00_Master/Evidence_Reading_Discipline.md` standing rule 9 says to prefer chain closure over judgement wherever a whole is known** - and here a practitioner has the closure signal in front of him and dismisses it as «не очень страшные».
- **⚠️ He also names the cause without connecting it to the effect: the software forces 90° corners and real flats are rarely square.** So **the closing error is absorbing the flat's out-of-square, plus every measurement error, into one segment.** A large residual means the survey or the squareness assumption is wrong; a small one is evidence both are sound. **It is a free quality metric and it is being read as a nuisance.**
- **→ Worth carrying as the clearest external illustration of why this project gates closure** (`check_wall_junctions.py`, `check_dxf_closure.py`) rather than eyeballing it. **It also validates `00_Master/Geometry_Variance_Study.md`'s finding that real deltas run -45 to +30 mm**: that is exactly the magnitude that would show up in his last line.

## Rules / Heuristics - The Modelling Method, and Its Deliberate Imprecisions

**A simple 3D model, 10-20 minutes for a flat, ~5 for a one-room.** He is explicit that no expertise is required: «я не программист и не дизайнер, а среднестатистический пользователь».

**⚠️ What he deliberately does NOT model accurately, and this is the disciplined part:**

- **Wall thickness** - «делать стены той же толщины как и в реальности смысла нет, просто делайте приблизительно похоже на реальность». **Approximate is fine because no quantity he needs depends on it.**
- **Adjacent/secondary rooms** can be drawn anywhere convenient and dragged into position afterwards.
- **⚠️ The technique for entering a dimension is the one this vault already mandates: draw the line roughly, then TYPE the number and press Enter** - the line snaps to the typed length. «Не обязательно нужной нам длины, просто ещё раз щёлкаем по мыши и... печатаем нужный нам размер». **Independent corroboration of "type the dimensions, don't click the pixels"** ([[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §6), reached by a finisher entering survey measurements rather than by anyone tracing a raster.
- **Set the unit system BEFORE starting, and his reason is specific**: dimensions are typed by hand throughout, so unfamiliar units cause repeated confusion and error. He uses centimetres.

**Quantity extraction is native, no plugin**: Окно → Лоток по умолчанию → Показать лоток opens the Entity Info tray. **Click a wall for its area, a line for its length, Ctrl-click to multi-select** - and that yields **total wall area net of window and door openings, floor area, or whole-flat perimeter** in one read. *(This is exactly the aggregation the Quantifier Pro sources automate - see the new toolchain page.)*

**A screenshot of the model is sent to the client** so they can picture the result.

## ⚠️⚠️ Rules / Heuristics - The Smeta Structure, and Stratified Precision

**Two separate estimates: one for MATERIALS, one for WORKS.** The materials estimate has **three parts**:

1. **Черновые (rough) materials** - plaster, profiles, plasterboard.
2. **Расходники (consumables)** - drill bits, grinder discs, gloves. **A named category in its own right, which most estimates fold invisibly into labour.**
3. **Чистовые (finish) materials** - **greyed out in his sheet, and deliberately approximate**, bought at later stages and costed properly later.

**⚠️⚠️ The reason for the stratification is the insight, and it is a pricing principle rather than a formatting one:**

> **Rough materials can be priced confidently because «они более-менее одинаково стоят везде» - they cost roughly the same everywhere. Finish materials «могут очень сильно отличаться» - they vary enormously, because they are a taste-and-tier choice rather than a commodity.**

- **→ Estimate precision should be stratified by how variable the category actually IS.** Pretending to three significant figures on finish materials is false precision; the client uses that section to size their own budget and to choose cheaper or dearer.
- **⚠️ This converges with the gap analysis's own "staged commitment" requirement** - price by trade stage and **do not commit Stage 4 rates during Stage 1** - reached from the opposite direction, by a practitioner explaining why his finish column is grey.

**⚠️ The works estimate ends with an explicit list of works NOT included** - «чтобы для клиента не было сюрпризом, что ему надо будет оплачивать грузчиков». **An exclusions list as a standard closing section.** *(Compare this page's existing four-line-смета red flag from Руслан: the test of a смета is what it names, and naming the exclusions is the honest form of that.)*

**⚠️ A stated contingency: add ~20% for непредвиденные расходы**, with the reason given - «как бы вы ни считали, всё равно всё учесть не сможете», plus changes made during the work. `single-account`, Omsk 2020, but a concrete figure with a stated mechanism.

## The Closing Argument, Which Is Also the Opening One

**Both times he states the model's value, it is about CHANGE, not about the first calculation:**

- Opening: «если вам в течение ремонта надо будет что-то узнать из размеров, поменять проект или работу в смете, это очень легко сделать, так как проект уже создан, и не надо сидеть с бумажками и на калькуляторе каждый раз».
- Closing: «с 3D макетом вам будет очень легко пересчитать площади, размеры, внести изменения в смету».

**⚠️⚠️ That is now THREE independent arrivals at the same conclusion in this one thread** - see the new toolchain page. **The model earns its keep on re-calculation after a change, not on first-pass precision** - which is precisely what this project's own gap analysis concluded when the owner corrected it: the model's job *"is not to be dimensionally exact - it is to hold quantities stable enough that a substitution re-prices correctly."*

## Confidence & Evidence Notes

- **ASR quality: poor.** No punctuation, heavy mangling - «испечь об» for SketchUp, «вдавить вытяните» for Push/Pull, «лоток» correct but «тело»/«контра» garbled, «по моей смерти» for «по моей смете». **Nothing numeric is taken from this transcript except the ~20% contingency, which is stated twice in effect.**
- **`single-account`**, Omsk 2020, one practitioner's own workflow.
- **No prices carried.** Rule 2 applied as instructed by the 2026-09-08 triage.
- **No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md` (NEW PAGE)** - native Entity Info aggregation, the deliberate imprecisions, the three-arrivals convergence.
- **`11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement.md`** - the three-part materials smeta, stratified precision, the exclusions list, the 20% contingency.
- **`00_Master/Evidence_Reading_Discipline.md`** - ⚠️ the discarded closure residual, as an external illustration of the rule.
- **5b**: no comparable price figures; none converted, per the 2026-09-08 instruction.
