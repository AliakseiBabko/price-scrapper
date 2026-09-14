---
source_type: video transcript (renovation bureau's branded channel - a two-person long-form walk through electrics, plumbing, climate and heating at the design stage)
source_url: https://www.youtube.com/watch?v=blhGIAE-mE4
video_id: blhGIAE-mE4
transcript_file: _Archive/processed_sources/20260914_planka_engineering_systems_design_stage_da10a976.txt
fetched: 2026-09-14 via youtube-transcript-api (ru, forced per standing rule 1)
upload_date: 2026 (captured into the sidecar via --fetch-upload-date)
channel: бюро Планка (Moscow)
presenter: two speakers - the bureau principal and, by reference, their engineering designer
source_title: "Инженерные системы в квартире — ВСЁ, что важно понимать на этапе РЕМОНТА"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Engineering / Electrical`, `Engineering / Plumbing`, `Engineering / HVAC`, `Engineering / Heating`)
fact_yield: 29
promotional_ratio: medium_to_high - the closing five rules include "have the people who will build it do the design", which is the firm's business model
corroborates_existing: partly
region: russia_moscow_2026 - flagged. REGULATORY CLAIMS ARE RUSSIAN; rule 4 applies. All prices RUB Moscow 2026, none transferred
---

# Source Note - бюро Планка: ⚠️⚠️ THE ENGINEERING DECISIONS THAT MUST HAPPEN BEFORE FINISHING STARTS (YouTube blhGIAE-mE4)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed; **no regulation was checked against its text**).

## ⚠️⚠️ Why this source is here at all, against my own triage call

**The 2026-09-14 triage DECLINED this channel** after two spot-checks that were branding and restatement, and named this video as the only possible exception — *"a weak reason and it did not justify a fetch today."*

> **⚠️⚠️ THAT CALL WAS WRONG, and the measurement says so.** **Ten of this video's topics have ZERO coverage in `12_Engineering_and_Systems/`**, checked against the folder's own dedicated pages and not merely by keyword. **It is by a wide margin the strongest video on the channel**, and the reason is structural: **it is the only long-form technical one, and length is the thing the six-minute listicles cannot fake.**
>
> **→ The lesson for the value filter: "the channel is weak" is not evidence about a particular video, and a LONG-FORM outlier on a short-form channel is worth the single fetch.**

## ⚠️⚠️ 1. The responsibility boundary, and the document that defines it

> ***«Зона ответственности начинается ОТ ПРИБОРА УЧЁТА И ПЕРВОГО ОТКЛЮЧАЮЩЕГО УСТРОЙСТВА на вашей ветке. Всё, что идёт дальше — ваше. И если лопнет труба у вас, вы заливаете соседей и будете платить за ремонт.»***

**The counter to the common assumption** *«труба заходит в квартиру, значит за неё отвечает УК»* — **no.**

**→ ⚠️⚠️ THE FIRST STEP HE PRESCRIBES: REQUEST THE ТЕХНИЧЕСКИЕ УСЛОВИЯ from the developer or the management company.** They state:

- **where your responsibility begins**
- **what electrical power is allocated to the flat**
- **what pipe diameters**
- **what ventilation volume, and what extract type**

> *«Это как карта. Без неё вы не знаете, куда идти.»*

> **→ ⚠️⚠️ ZERO COVERAGE IN THE VAULT, AND IT IS A FREE PRE-WORK ARTEFACT REQUEST — the same shape as the ДЕТАЛИРОВКА and ЭСКИЗ from the kitchen round: a document that exists, that you are entitled to, and whose absence you will otherwise discover late.** **⚠️ Worth requesting for this flat regardless of what the Belarusian equivalent is called.**

## ⚠️⚠️ 2. Allocated power and the demand coefficient — the constraint nothing in the vault states

- **Typical allocation: from 3.5 kW in old stock; 10–20 kW in new builds.**
- **Everything must fit inside it *«с учётом КОЭФФИЦИЕНТА СПРОСА»*** — the diversity factor, since not all loads run at once.
- **Named large loads: hob 5–7 kW; instantaneous water heaters 6–10 kW**; plus supply ventilation.

> **→ ⚠️⚠️ THE VAULT HAS EXTENSIVE CABLE AND PANEL MATERIAL AND NOT ONE WORD ON THE ALLOCATION THAT BOUNDS ALL OF IT.** **Verified: zero files in `12_Engineering_and_Systems/` mention выделенная мощность or коэффициент спроса.** **This is the ceiling every electrical decision sits under, and it is knowable from the ТУ before anything is designed.**

### ⚠️⚠️ And a genuine engineering technique for when the load does not fit

**The Arbat case**: a 40 m² terrace with a winter garden and a snow-melting system. **The melting load alone came to about 1.5× the whole flat's allocation**, and the development had no spare capacity left to grant — *«они все были израсходованы уже другими квартирами»*.

> **The solution: split the heating into SEVEN circuits of ~3 kW and switch them SEQUENTIALLY rather than energising 20 kW at once.**

> **→ ⚠️⚠️ SECTIONAL SEQUENTIAL SWITCHING TO FIT A LARGE LOAD INTO A FIXED ALLOCATION. A transferable technique, and the only piece of real engineering problem-solving on the whole channel.** ⚠️ **Relevant here to any high-load ambition — an instantaneous heater, underfloor heating, or an induction hob plus oven on a constrained supply.**

## ⚠️ 3. The panel, and two items the vault is thin on

**Their panel specification**: incoming breaker, **УЗМ** (voltage-surge relay), **УЗИП** (surge-protective device), **УЗО** (RCD), and breakers — **with separate lines for sockets, lighting, the kitchen, bathrooms, air conditioners and low-current.**

- **⚠️ Separate lighting breaker PER ROOM**, so a fault in one room leaves the others lit.
- **⚠️⚠️ NON-SWITCHABLE LINES — zero coverage in the vault.** Fridge, alarm and internet on circuits that a **«отпуск» master switch** in the panel does not kill, *«чтобы, когда вы уезжаете и выключаете рубильник, холодильник продолжал работать»*. **→ A holiday master-switch with deliberate exceptions is a concrete, cheap design decision made at panel-design time.**
- ⚠️ On УЗМ he offers the only quasi-quantified claim in the source: **one client's УЗМ tripped 12 times in two months**, and *«его сосед без УЗМ в тот же день лишился ноутбука и телевизора»*. **⚠️ An anecdote, not a failure rate.**

**⚠️ Low-current:** *«Интернет-кабель надо тянуть ДО ТОГО, как зашьют стены. И не просто витую пару, а иногда ОПТОВОЛОКНО, потому что провайдеры переходят на него.»* **Always lay закладные трубы (conduit) so a change of provider does not mean chasing walls.**

## ⚠️ 4. Plumbing — what is new against a well-covered area

**⚠️ Already covered in the vault and not re-recorded**: cross-linked polyethylene over polypropylene (29 files), collector versus tee distribution (8), leak-protection systems (10). **His versions add nothing** beyond the phrasing *«полипропилен — это прошлый век… очень высокий риск ошибки в связи с человеческим фактором»*.

**What IS new:**

- **⚠️⚠️ A WATER ANALYSIS BEFORE CHOOSING CARTRIDGES — zero coverage.** *«Сделайте анализ воды в лаборатории»* — hardness and impurities, so the filter cartridges are chosen for the actual supply. **They do it for every project.** ⚠️ *«В Москве часто жёсткая вода. Если не смягчать — кожа сухая, техника зарастает накипью.»* **→ The principle transfers; the Moscow water characterisation does not.**
- **The water-treatment train as a sequence**: coarse filter → pressure reducer → fine filter → **non-return valves** → **water-hammer arrestors**, plus a mains cartridge filter **changed every 3–6 months depending on consumption.**
- **⚠️ Access, stated as a defect**: collectors, meters and filters bricked into a wall behind a **20×20 cm** hatch. *«Всё, что требует обслуживания — фильтры, краны, счётчики — должно быть в доступе.»* **Make the hatches big.**
- **⚠️⚠️ REQUEST THE TECHNICAL SHEET FOR EVERY FIXTURE.** Example: **a bidet-function WC needs an electrical supply and may need extra hot AND cold connections.** **→ The fixture schedule drives the first-fix, and a fixture chosen late invalidates it.**
- **⚠️ A "reserve provision" pattern worth naming**, from a 56th-floor project where supply pressure falls with height: the management company suggested a **circulation pump** might eventually be needed — *«вообще они не ставятся в квартирах»* — so they **left a dedicated electrical outlet and physical space for one** without installing it.

## ⚠️⚠️ 5. Climate — the area with NOTHING in the vault

**Verified: zero files in `12_Engineering_and_Systems/` mention увлажнение at all.**

- **⚠️⚠️ HUMIDIFICATION. *«Зимой в квартирах влажность падает до 15% при норме 45–65.»*** Bad for skin and mucosa, **and wooden furniture cracks — *«гарантия снимается»*.** Two routes: **domestic units** (cheap, need maintenance, take floor space) or **built-in systems — isothermal or adiabatic**, of which they use **nozzle-type (форсуночные)**: dearer, but hold humidity automatically. **They always reserve space and dedicated sockets in the design.** ⚠️ *«8 из 10 наших клиентов просят увлажнения»* — a Moscow-market observation, not a recommendation.
- **⚠️⚠️ THE SHARED EXTRACT RISER IS A COMMONS.** Bathroom and kitchen have **separate extract risers and must not be confused**, and **you must not fit additional fans into them unless the design allows** — *«если все соседи поставят мощные вытяжки, вся система разбалансируется, и у вас в квартире будет запах из чужих кухонь»*. **→ Their approach is again a reserve: leave an electrical outlet so a fan CAN be added later if foreign smells prove unsolvable.**
- **⚠️⚠️ AC CONDENSATE MUST GO TO THE SEWER, NOT THE FAÇADE** — and the vault's `AC_Condensate_Drainage.md` is an 18-line stub. If gravity is impossible because of a door or window, **a pump — but the pump is noisy and must be soundproofed or concealed.** ⚠️ **For existing façade-draining units there is a partial remedy: an atomiser on the outdoor unit disperses the condensate as a cloud instead of a stream — but it must be removed for winter or trapped water can burst it.**
- **⚠️ Airflow direction is a design decision**: not onto a bed, not onto the hob. *«Проектируем так, чтобы поток воздуха проходил ВДОЛЬ СТЕН, не попадая на постоянное местонахождение людей.»*

## ⚠️⚠️ 6. Heating — one prohibition and one failure mode

> **⚠️⚠️ *«Водяные тёплые полы ЗАПРЕЩЕНЫ в многоквартирных домах. Если вы хотите тёплый пол — только электрический.» То же самое касается водяных полотенцесушителей.***

> **⚠️⚠️ RUSSIAN JURISDICTION, ASSERTED BY A CONTRACTOR WITH NO NORM CITED. Standing rule 4 keeps it out of `16_Legal_and_Regulations/`, and the Belarusian position MUST be confirmed separately — this is exactly the class of claim that is often true in substance and wrong in detail.** **Recorded as a question to resolve, not as a constraint adopted.**

**⚠️⚠️ AND THE BEST THING IN THE VIDEO — a named failure mode with a witness.** Their own engineering designer, Igor: *«ему просто позвонили, сказали: "Игорь, вы затопили пять этажей, которые находятся под вами"… отвод на водяной полотенцесушитель просто отвалился из-за КОРРОЗИИ»*.

- *«Это КИПЯТОК. И когда отваливается вот этот отвод, ты не сделаешь ничего. Затопление происходит максимально быстро… там считанные часы.»*
- **The interviewer then reports the same corrosion on his own rail** — wiped off, and it came back.
- **Their recommendation: cut the water towel rail out top and bottom, weld in a new section of pipe, and fit an ELECTRIC rail** — *«это просто бомба замедленного действия»*.

> **→ ⚠️⚠️ [[03_Kitchen/analysis/Cabinet_Assembly_Technique|the vault already covers water-vs-electric towel rails as a PREFERENCE]]** (`Hygienic_Shower_and_Towel_Warmer.md` §"Water (Hydronic) vs. Electric"). **What is new is the FAILURE MODE: corrosion at the branch connection, boiling water, and a flood measured in hours rather than a seep.** **That converts a preference into a risk argument, and it is checkable today on any existing rail — look for corrosion at the connection.**

**Also**: developer radiators are often underpowered; replace **the whole run from riser to meters**, including the shut-off valves, *«потому что там идёт давление, и старая арматура может поплыть через год»*. **Radiator sizing needs a heat-loss and heat-gain calculation** — *«если у вас панорамное остекление, потери тепла огромные»*. **Collector distribution for heating too**, with per-room circuits and shut-off.

## ⚠️ 7. His closing five rules, and the one that is a sales pitch

1. **Don't economise on the engineering project** — *«хороший инженерный проект стоит 50–100 000 руб. ЗА РАЗДЕЛ»*, each section (electrics, water, ventilation, heating, low-current) specifying **cable cross-sections, cable grades and pipe diameters.** ⚠️ **RUB Moscow 2026 — rule 2, not transferred. The STRUCTURE transfers: priced per discipline, not as one document.**
2. ⚠️⚠️ **"Have the people who will build it do the design."** **This is the firm's business model stated as advice** — *«нет размывания ответственности»*. **Recorded as their position, not as guidance.** ⚠️ **It also runs against the vault's technical-supervision material, where independent oversight of the builder is the point.**
3. **⚠️⚠️ Settle everything before finishing starts.** *«Как только стены заштукатурены или зашиты гипсокартоном, переносить розетки, трубы или вентиляцию можно, но уже СЛОЖНО И ОЧЕНЬ ДОРОГО.»*
4. **Leak and surge protection are mandatory** — *«это не расходы, это инвестиция»*. He names **Нептун** and **Аквасторож**. ⚠️ A motorised valve plus control unit at **30–40k ₽** (rule 2).
5. **⚠️⚠️ PROVIDE FOR THE FUTURE EVEN WHERE YOU ARE NOT BUYING NOW** — conduit and spare wiring for a humidifier or air conditioner you may want in two years. **The same reserve pattern as the circulation pump and the extract fan, stated as a rule. → This is the most portable idea in the source.**

## ⚠️ What was deliberately NOT extracted

- **Every price.** RUB, Moscow, 2026 — rule 2. The 25M ₽ renovation, the 5.7M ₽ crane lift for the winter garden, 50–100k ₽ per project section, 30–40k ₽ leak valve, ~10k ₽ water analysis. **All recorded as magnitudes in context, none converted.**
- **The Arbat terrace narrative** beyond the sequential-switching technique — a long digression about a winter garden, glazing 3 m × 2.2 m, cranes and winches. **Interesting, irrelevant at one-flat scale.**
- **Brand recommendations** — Нептун and Аквасторож recorded as named products, not endorsed.
- **The Moscow-specific water hardness and the "8 of 10 clients" humidification figure**, as market observations.
- **⚠️⚠️ The water-UFH and water-towel-rail PROHIBITION is NOT routed to `16_Legal_and_Regulations/`** — Russian, uncited, and rule 4 makes that folder Belarus-only.

## Source Notes

**бюро Планка** (Moscow), 2026, **18:29, ru, read in full**. Triage: [`planka_buro_channel_triage_20260914.md`](../_Inbox/planning/planka_buro_channel_triage_20260914.md), **which declined the rest of the channel and was right to — this is the outlier.**

⚠️ **A two-person conversation**, so some content is unscripted digression and some is the interviewer prompting. **The engineering detail is consistent and specific; the business philosophy around it is the same pitch as the other two videos.**

⚠️⚠️ **`promotional_ratio: medium_to_high`. Nothing here is tested or measured — it is an experienced practitioner's account, and the two vivid stories (Igor's flood, the UZM neighbour) are told rather than shown.** **This is exactly the evidence class the triage criticised on the other two videos. What makes it worth keeping is not better evidence but a much higher density of SPECIFIC, CHECKABLE items**: named documents to request, a named load ceiling, a named failure location on a component this flat already has.

⚠️ **ASR is reasonable by this vault's recent standards** — «шитый полиэтиленс» is **сшитый полиэтилен**, «демофония» is **домофония**, «адиоботические» is **адиабатические**. **Figures were re-derived from context; nothing reconstructed by guessing.**
