---
source_type: video transcript (HVAC engineer / design-services channel, renovation-sequencing checklist)
source_url: https://www.youtube.com/watch?v=l4HipwaUxpc
video_id: l4HipwaUxpc
transcript_file: _Archive/processed_sources/20260914_dmitry_hvac_renovation_start_checklist_1da65568.txt
fetched: 2026-09-14 via youtube-transcript-api (ru-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-02-23 (confirmed via yt-dlp metadata)
channel: Dmitry_HVAC — Вентиляция Отопление Кондиционеры
source_title: "С чего НАЧАТЬ РЕМОНТ квартиры в 2025? На чем СЭКОНОМИТЬ деньги и НЕРВЫ"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Budget and Planning`, `Engineering and Systems`)
fact_yield: 17
promotional_ratio: high
corroborates_existing: true
region: russia_no_city_named_2025 - flagged; electrical figures are near-universal practice but jurisdiction is unstated
delivery_model: HVAC design services and paid masterclasses
---

# Source Note - Dmitry_HVAC: A Post-Purchase Sequencing Checklist — ⚠️⚠️ and a Direct Challenge to This Project's Own Premise (YouTube l4HipwaUxpc)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

⚠️ **Second source from this presenter** — the vault already holds [[_Sources/YT_EUM7kv77VVY_dmitry_hvac_top4_comparison|YT_EUM7kv77VVY]]. **Concentration is mild at two.**

⚠️ **`promotional_ratio: high`, and it shapes the content.** Three funnel links appear before any material (a free ventilation masterclass bot, a masterclass for interior designers, a project-order taplink), and **the entire ventilation section is deferred to a paid masterclass rather than explained**: *"это огромный пласт… ёмкая тема, давайте так, вот здесь сейчас не рассказываю"*, followed by a QR code. **The ventilation content is therefore absent, not extracted.**

## ⚠️⚠️ 1. Step one: request the КЛАДОЧНЫЙ ПЛАН from the developer, immediately

> *"Первый шаг… сразу же после приобретения квартиры, даже если самой квартиры ещё не существует… вам нужно её запросить у вашего застройщика — в офисе продаж."*

**Why, in his account**: you must know **what your internal walls are made of**, because the developer's layout *"не для вас они её делали, а просто ради продажи"* and you will almost certainly change it. **The кладочный план is what tells you which walls can move — and whether a change is an official or an unofficial replanning.**

> **⚠️ The failure mode he describes is concrete**: skip it, plan a fitting room / laundry / bathroom with a designer, and discover on handover that a **monolithic load-bearing wall** is there. *"Даже если её можно снести… разрезать монолит и вывести его из квартиры с пятого или десятого этажа — это огромная проблема."*
>
> **→ ⚠️ This project already holds the equivalent** — `data/canonical/wall_materials.json` carries wall build-ups, and the developer plan and БТИ material are in hand. **Recorded as independent confirmation that this is the correct FIRST artefact, not as a new action.** ⚠️ **The demolition-logistics point (cutting and removing monolith from an upper floor) is the part this vault does not state anywhere, and it is a real cost driver for any load-bearing change.**

## 2. Step two: a concept, then a planning solution — with services decided AT concept stage

**Concept** = knowing what each room is (kitchen or kitchen-living, one children's and one adult bedroom, whether the bedroom carries a wardrobe / ensuite / study). It then grows into a **planning solution**, within which furniture positions are fixed, *"что неизбежно повлияет на все дальнейшие манипуляции."*

> **⚠️⚠️ AND THE POINT HE EMPHASISES: the ENGINEERING must be decided at the CONCEPT stage, not later.** His worked example is air conditioning: indoor units can hang almost anywhere, **but the OUTDOOR units need a place** — *"если у вас нет корзин, нет лоджии, нет балкона, и есть какой-то техэтаж, где сказали можно повесить оборудование — вот это обязательно нужно знать уже на этом этапе."*
>
> **→ The outdoor-unit location is a concept-stage constraint, not an installation detail.** ⚠️ **Directly relevant to this flat** — `10_Balcony/` and `12_Engineering_and_Systems/` both exist, and the loggia's status decides whether there is anywhere to put a condenser at all.

**Routes to a concept**: a designer (technical project / conceptual solution / full album with material selection — *"как всегда, это упирается в деньги"*), or DIY via online planners. ⚠️ **He names Room Planner** as a capable free option covering furniture, electrics, plumbing, lighting and ventilation. ⚠️ **Recorded as a tool mention only; this project already has a modelling chain and the 2026-09-08 gap analysis settled the no-new-software question.**

## ⚠️⚠️ 3. Electrics — cable sizing, with a fire-safety argument

> *"Есть провод **2,5 квадрата**, есть провод **полтора квадрата**. Например, под электродуховку **нельзя тянуть провод полтора квадрата — надо 2,5 минимум**, так же как под электроплиту. И вы **не можете притянуть один и тот же провод** как на чайник, так и на духовку, потому что провод будет просто **перегружен** — и это уже не просто некрасиво и неудобно, а **тупо опасно** для пожаробезопасности."*

> **⚠️ Recorded with the jurisdiction flagged. He names no norm and no country.** **2.5 mm² for an oven or hob, and no shared circuit between a kettle and an oven, is near-universal domestic practice rather than a peculiarity — but it is stated here as trade practice, not as a cited requirement.** **Standing rule 4: this does NOT go to `16_Legal_and_Regulations/`; it routes to the technical page with the jurisdiction flagged, and a Belarusian requirement must be confirmed separately.**
>
> ⚠️ **He also notes the cost consequence**: the cross-section you choose drives the cost of the cable runs. **And the kitchen is where it bites** — *"кухня — это прямо самое больное место"* — how many sockets and where on the worktop, so you are not endlessly plugging and unplugging a multicooker or a mincer. **Consistent with the socket-count and worktop-outlet content already in [[03_Kitchen/Kitchen_Utilities|Kitchen Utilities]].**

## ⚠️⚠️ 4. THE FINDING WORTH MOST: measure the flat AFTER handover, and the finishing tolerance is 10 mm, not 50

> *"Когда вы наконец-таки приняли квартиру, вам теперь нужно произвести **фактический замер** всей вашей квартиры… потому что то, что вам запланировали, и факт — **может не соответствовать на 1, 2, 3 см**. Дверной проём смещён на 3 см правее или левее — как будто ничего страшного. **Но для такого этапа, как заказ мебели, это может быть целой трагедией.**"*

> *"**В чистовой отделке нету допусков 5 см. Дам допуск 1 см в лучшем случае.** Это можно вот так чуть-чуть подвинуть справа налево или сверху вниз 2–3 см — и всё, у вас либо плитка по формату уже не влезет, либо будет фартук, и будет кухня, и будет соответственно вот такой вот зазор. Ну, будет некрасиво. **Почему некрасиво — потому что вы заплатили за то, чтобы было красиво.**"*

> **⚠️⚠️ THREE TOLERANCES, THREE SCALES, AND THE FURNITURE IS ORDERED AGAINST THE TIGHTEST — this is the cross-source finding of the round:**
>
> | Stage | Tolerance | Source |
> | :--- | :--- | :--- |
> | **Building, as built vs plan** | **±50 mm nominal** | `00_Master/Geometry_Variance_Study.md` (−45 to +30 mm measured) |
> | **⚠️ Finishing** | **~10 mm at best** | **this source** |
> | **⚠️⚠️ Fitted furniture** | **3 mm per wall, just to install** | [[_Sources/YT_BOIJzganJ9U_cappuccino_furniture_gaps_tolerances|the gaps note]] in this same batch |
>
> **→ The kitchen is specified against the building's ±50 mm and installed into the finish's ±10 mm with a 3 mm working clearance. The three do not reconcile — which is exactly why he insists on a post-handover measurement before anything is ordered.** ⚠️⚠️ **Two unrelated sources in one batch, from opposite ends of the trade, arriving at the same conclusion by different routes.**

**And the measured plan is a communication artefact**: with an accurate plan carrying a dimension grid, *"вы просто присылаете планировку… вам онлайн дистанционно посчитает — не нужно будет ездить что-то замерять."* Electricians, ventilation and A/C contractors can quote remotely.

> **⚠️⚠️ That is a direct description of what this project's deliverable is FOR**, and it is worth recording as external validation of the album's purpose rather than only its content.

## ⚠️⚠️ 5. His closing thesis — which contradicts this project's premise, and should be recorded as such

> *"Не засоряйте свою голову изучением того, **какую конкретно гидроизоляцию, как нужно наносить, сколько часов ждать, пока она засохнет, какой клей выбрать для плитки… какой конкретно провод нужно взять, какое напольное покрытие дольше будет служить**. Нет, не в этом ваша задача. **Вашей жизни не хватит, для того чтобы в этом разобраться.** Ваша основная задача — **найти для себя идеальных исполнителей**, которым вы доверите свои деньги."*
>
> *"Я не знаю ни одной квартиры, ни одного загородного дома — хотя через нас их прошло сотни — **чтобы человек с первого раза вписался в ремонт**, всё сделал сам, и у него всё получилось. **Не бывает такого. Это невозможно.**"*

> **⚠️⚠️ THIS IS A DIRECT CHALLENGE TO WHAT THIS VAULT IS.** The owner is self-managing and has built ~813 extraction notes precisely in order to understand waterproofing, cable cross-sections, tile adhesive and floor coverings. **This source says that is the wrong allocation of effort and that contractor selection is the real lever.**
>
> **→ Recorded as a genuine Perspectives item, not buried and not rebutted.** ⚠️ **Note the commercial interest**: he sells design services and masterclasses, so *"find ideal executors"* is congruent with *"hire professionals like me."* ⚠️ **And note the internal tension in his own video: he tells the viewer not to learn cable cross-sections roughly ninety seconds after teaching them 2.5 vs 1.5 mm².**
>
> ⚠️ **The defensible half is worth keeping regardless of the framing: a self-manager's scarcest resource is attention, and depth bought in one trade is depth not bought in another.** **This vault's own value filter already acts on that principle; this is the same argument stated from outside.**

**His summary, which is uncontroversial and matches the vault:** any renovation without a technical project is doomed to a long build, hassle and overpaying; furniture ordered without the flat's real dimensions is money burnt; engineering done by eye is renovation by guesswork; and planning beats a target move-in date.

## ⚠️ What was deliberately NOT extracted

- **The entire ventilation section** — deferred by the presenter to a paid masterclass and never delivered. **Four approaches are named (opening windows, valves, active ventilators, centralised systems) and none is explained.** ⚠️ **The vault's existing ventilation coverage is unaffected.**
- **All three funnel links, the QR codes and the designer-masterclass pitch.**
- **Room Planner** — a tool mention, not a recommendation; the no-new-software conclusion stands.
- **No prices. No regulatory routing** — see §3.

## Source Notes

Dmitry_HVAC (YouTube), 2025-02-23, 23 min, **read in full**, `ru-orig` verified. **Claims are this presenter's, as opinion.** ⚠️ **Nothing is measured; the 1 cm finishing tolerance and the 1–3 cm as-built deviations are his working figures from practice, stated without data.** ⚠️⚠️ **`promotional_ratio: high` — the most substantive section (ventilation) is withheld behind a funnel, which is itself the clearest signal about this source's purpose.** ⚠️ **The closing thesis in §5 is offered by someone who sells the alternative to self-management, and is recorded with that noted.**
