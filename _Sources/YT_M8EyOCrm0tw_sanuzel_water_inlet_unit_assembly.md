---
video_id: M8EyOCrm0tw
channel: Vasily_Sanuzel Ремонт Санузлов (Василий, one-man bathroom/plumbing contractor)
source_type: youtube
source_title: "Ванная в панельке П-44. Сантехнические работы. Сборка узла ввода водоснабжения. Серия 3"
source_url: https://www.youtube.com/watch?v=M8EyOCrm0tw
transcript_file: _Archive/processed_sources/20260908_sanuzel_water_inlet_unit_assembly_4a522b9f.txt
upload_date: 2023-10-07
fetched: 2026-09-08
fact_yield: 21
promotional_ratio: low
corroborates_existing: true
region: unresolved_level2_channel_only
---

# Source Note — Vasily_Sanuzel, «Сборка узла ввода водоснабжения» (П-44Т, серия 3 of 6)

Episode 3 of a six-part serialized bathroom rebuild in a П-44Т panel flat. Russian
spoken audio confirmed (`language: ru`, ASR track) — **the channel serves
auto-translated English titles by default and this one had to be pulled with
`lang=ru` forced**. The presenter does the work himself on camera; no company,
no crew, no product pitch beyond a Telegram channel mention at the end. **Low
promotional ratio, and he shows a joint that leaked on him** (see below), which
is the behavioural evidence for trusting the rest.

**Region stays level 2**: he names the housing series (П-44Т) but no city. No
prices anywhere in this video — nothing to convert.

**⚠️ Correcting the gap claim this video was selected on.** The triage argued
`узел ввода` was a zero-coverage subject; **that was true only of the Russian term
in `_Sources/`.** `12_Engineering_and_Systems/analysis/Water_Inlet_Node_Components.md`
already held ~250 lines from five channels, including a mandatory-vs-optional split.
**So this source deepens a covered subject rather than opening an empty one** — which
makes the divergences below (the reducer's status, the 3D model, the assembly craft)
the part that carries its weight, not the component list.

---

## The water inlet unit («узел ввода»)

**He models the whole assembly in 3D at full scale before ordering a single
part.** Stated purposes, in his order: know exactly which components are needed
(«мне не приходится бегать всё время в магазин»), and set out the dimensions so
the finished assembly fits the envelope it has to live in. He publishes the
model link in the description so viewers can rotate it in a browser.

> **⚠️ The strongest planning claim in the video, and it is his closing one:**
> «без предварительных расчётов я бы наверное не стал рисковать собирать
> подобные системы, так как велик риск просто не попасть в определённые
> габариты». The model also fed **dimensions given to the welder** for the riser
> stub-outs, which is what let the finished unit land inside the boxed-in
> envelope («короб») planned around it. — Василий, Vasily_Sanuzel

**Assembly order, cold side (hot is built as a mirror image, «зеркальный»):**

1. **Ball valve with electric actuator** («кран с электроприводом») from a leak-protection system («система защиты от протечек»). Needs an **extension piece** so its control head does not foul the main riser valve behind it.
2. **Coarse mesh filter** («косой фильтр», ~300 micron, «может быть 600, 500»).
3. **Pressure reducer / regulator** («редуктор давления»).
4. **Water meter** («счётчик») — *the existing meters were kept*; only the union halves were replaced.
5. **Check valve** («обратный клапан») immediately after the meter.
6. **Fine filter, 100 micron**, with a removable **neodymium magnet**.
7. **Union + tee carrying a pressure gauge** (1/4" thread, so an adapter).
8. **Magistral filter** (5 micron ordered here — «можно поставить обезжелезивающий, умягчающий»), then a tee: one branch to the **water heater**, second gauge after the filter.
9. **Collector / manifold** («коллектор») through a demountable joint, feeding the individual fixture runs.

### His mandatory-versus-optional split

**He names four items as non-negotiable** — «это обязательно, вот прямо без них
вообще никак нельзя, это просто ну запрещено» — pointing at components rather
than naming them, and the pointing sequence lands on **the valve, the coarse
filter, the pressure reducer, the meter and the check valve**.

> ⚠️ **`uncertain`: he says "four things" while gesturing at what reads as five
> components in the assembly order.** The count and the list cannot be
> reconciled from an ASR transcript with no visual. Recorded as *the mandatory
> group is {shut-off valve, coarse filter, pressure reducer, meter, check
> valve}, exact membership four-of-five unresolved* rather than guessing which
> one he excluded.

**Everything else is «по желанию» — with one exception he argues for**: the
100-micron fine filter «я бы вот это тоже добавил в обязательный минимум… для
современной сантехники». His mechanism, and it is a real one rather than an
assertion: modern mixers have aerators with very fine mesh that clog and kill
the flow, and single-lever mixers use ceramic cartridges — **any grit that
reaches a cartridge scores a small pit in it, and in time the mixer stops
shutting off and starts dripping**. The filter's built-in neodymium magnet
catches metallic particles specifically.

## Numbers stated

| Figure | Context |
| :--- | :--- |
| **~5 atm** | pressure in the risers as found |
| **3 atm, «максимум 3 с половиной»** | the working pressure he considers normal inside a flat — the reason a reducer is fitted at all |
| **3 cm per 1 m** | sewer pipe fall (see below) |
| **~300 micron** (possibly 500–600) | coarse filter mesh |
| **100 micron** | fine filter with magnet |
| **5 micron** | the magistral filter cartridge ordered on this job |

**Membrane-type reducers preferred** («мембранного типа») on two stated grounds:
they last longer, and they **distribute pressure more correctly when several
consumers open at once**.

**Buy the part that stays, not the part that gets replaced.** He kept the
existing meters but bought **bronze union halves** («полусгоны американки из
бронзы») — «американки остаются, а счётчики могут меняться, пусть они будут
хорошими». A clean spend-where-it-is-permanent heuristic.

## Drainage — the constraint that has to be set before the screed

**Fall is 3 cm per running metre, and he states the tolerance in both
directions**: «больше не надо, меньше тоже не надо».

> **The planning consequence, and it is the one worth carrying:** the pipe must
> climb continuously away from the lowest tee at the stack, so **the lower the
> connection into the stack, the lower the shower tray (and every other fixture)
> can sit.** Lowering that bottom tee was done back in episode 1 specifically to
> buy this; here he had to chase it lower still to keep the fall. — Василий

He also ran the kitchen sink drain from the same works, and set a **concealed
siphon box** («закладная для скрытого сифона», the red in-wall box) sized for a
washing machine and a dishwasher standing side by side — trimmed flush and
fitted with its internal mechanism only after the finishes are done.

## Ventilation decisions

- The flat duct («плоский воздуховод») is recessed into a ceiling cut-out and clamped, and **the outlet is brought out of the WALL, not the ceiling**. Stated reason: a fan mounted that way **does not clatter its backdraught flaps** («он не будет хлопать своими крылышками»).
- For the kitchen he ran **two separate ducts into a second shaft — general room extract and cooker hood — and deliberately fitted no backdraught valve** («не ставить там обратный клапан, а просто будет две отдельные трубы»). The hood duct is left as a stub above the ceiling because the hood position was not yet decided; whoever fits the kitchen connects to it.

## Craft detail — thread sealing

- **Smooth threads get notches cut into them** («насечки») with a hand tool before flax is wound on. Mechanism: the flax **grips the notches and travels into the thread** as the fitting turns, instead of rolling off a smooth thread. His own check that it worked: you can see the flax rotating with the fitting.
- Flax is then **preserved with a sealing paste** («чтобы он не гнил, не портился»).
- **Anything protruding after tightening is rubbish, not sealing** — «всё, что нужно для уплотнения, осталось внутри резьбы; всё, что снаружи — просто мусор» — and he trims it off with a knife.
- He trialled a **silicone sealing tape** (Italian, fabric-like, not FUM) on the conical collector threads and reports it cleaner and more convenient there; conical collector threads go very tight.
- **Coarse filter orientation is directional and gets it wrong easily**: the sump must hang **downward relative to gravity**, and the unit must not be installed with flow running upward. Failure mode if inverted — the collected debris drops back into the main bore and blocks it, or blocks the joint before it.

## Assembly and serviceability

- **Demountable unions at both ends of each filter** so filters can be pulled, cleaned or swapped without cutting anything.
- **Stainless steel tube** for the interconnections, press-fitted onto an O-ring inside the fitting and crimped with a matched die. Stated grounds: **larger internal bore for a given outside diameter**, longevity, and a neater look.
- Each element bracketed to the wall **independently of its neighbours**, on bendable mounting strip formed to shape with its own tool.
- A **laser level sets one plane** for the whole assembly, so the built unit matches the modelled one.
- Two gauges, **before and after the filter**, so the filter's condition is readable as a pressure drop.
- Reducers are deliberately **demountable so the membrane can be replaced** rather than the whole unit.

## Sequencing and trade coordination

- **Dirty work first**: chases and pipe-laying are done before any assembly («первым делом я обычно начинаю с грязных работ»). He filmed none of it — dusty, and «смотреть там особо не на что».
- **The client's own electrician worked the flat first**, and he asked for one thing: cable ends left **long, with slack**, so he could route them himself where they would not conflict with the other services. A small but real inter-trade coordination point.
- Wall thickened with aerated block in episode 1 to carry services — **and the thickening produced a niche with a shelf in the shower zone as a by-product**, i.e. a service constraint turned into storage rather than being boxed out blind.
- The risers were wrapped in thermal insulation, the sewer stack clamped in three places, and a **decorative mounting platform** built from ribbed aluminium sheet on plywood, screwed to the wall — both a finish and a convenient mounting substrate for the unit.

## ⚠️ Failure he published against himself

**One joint weeped on first pressurisation** — «одно соединение у меня всё-таки
запотело» — and he shows himself stripping and re-sealing it. This is why the
`promotional_ratio: low` classification is behavioural rather than a judgement
about tone: he had every option to cut it.

## Uncertainties

| Item | State |
| :--- | :--- |
| Which four of the five components are the "mandatory four" | ⚠️ `uncertain` — see above. Do not write a four-item list into a wiki page as if it were resolved |
| Coarse filter mesh | he says ~300 micron then immediately «может быть 600, 500, не помню» — carry as a **range**, not a figure |
| City | never named. Level 2, channel association only |
| Jurisdiction | Russia. **Nothing here goes to `16_Legal_and_Regulations/`** — the pressure and fall figures are practitioner practice, not cited code |
