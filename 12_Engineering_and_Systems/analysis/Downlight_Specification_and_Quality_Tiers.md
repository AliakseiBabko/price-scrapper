# Downlights — Specification by Measurable Parameter, and a Quality Ladder

Detail page for [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

## Scope

**How to specify a recessed point fixture (точечный светильник) by parameters that can be measured, and what each step up the price ladder actually buys.**

This page exists because the recessed downlight is the fixture type this project will buy in the largest quantity, and because its price spans roughly **100×** for products that look similar in a listing photograph. [[12_Engineering_and_Systems/analysis/Lighting_Fixtures_and_Fittings|Lighting Fixtures and Fittings]] holds the fixture **taxonomy**, the dimensional traps, the replica/procurement material and the chandelier and LED-strip content; **this page holds the measurable-parameter layer and the tier ladder underneath it.** Glare in the room is on [[12_Engineering_and_Systems/analysis/Lighting_Glare_and_Room_by_Room|Glare and Room by Room]]; colour temperature is on [[12_Engineering_and_Systems/analysis/Lighting_Colour_Temperature|Lighting Colour Temperature]].

> [!WARNING]
> **Whether the 100× spread is worth paying for is genuinely disputed in this vault, by two lighting-adjacent professionals who disagree.** See the Perspectives block at the foot of this page before treating the ladder as a buying instruction.

## The Six Measurable Parameters

The parameters below are the ones a buyer can check or demand a figure for. They come from a source built on five expert interviews and a light-laboratory visit, with several measurements shown on camera. [source: [[_Sources/YT_03QuTzPgPa8_kruglov_downlight_spec_eight_tiers|YT_03QuTzPgPa8]]]

### ⚠️⚠️ 1. CRI is an average, and R9 is what it hides

**CRI (identical to RA) measures how accurately a source renders colour against daylight, 100 being sunlight.** Budget fixtures measure **65–80**; professional fixtures are **not below 90**; improved models reach **97+**. A high CRI adds nothing to an object — it shows it as it actually is. The stated failure at low CRI: a strawberry that is bright red in daylight reads a sickly grey.

**The mechanism that makes a published CRI misleading, and it is the single most useful item on this page: CRI is an ARITHMETIC MEAN over ten samples — eight primary plus two additional. A high mean can conceal a near-zero component.**

- **R9 is the red-spectrum sample.** A fixture can measure **CRI ≈ 90 with R9 = 10, or even R9 = 0.** That is why two fixtures both honestly labelled "CRI 90" can look completely different, one of them rendering skin and wood pale and lifeless.
- **Shown on camera**: a marketplace lamp with a high overall CRI and **R9 of zero**, against an unbranded module with a barely higher overall CRI and a very high R9 — the second visibly better light.
- **⚠️ Manufacturers of cheap lamps never publish R9**, because a buyer who knows only CRI reads 90 and stops. **→ Demand R9 as a separate figure, not CRI alone. A supplier who will not give one has answered the question.**
- **⚠️ Cheap components cannot reach a high R9 at all** — a materials limit, not a tuning failure. **The practical ceiling this puts on a whole format: even a good GX53 lamp from a reputable maker does not exceed R9 ≈ 10%.** The format caps colour quality regardless of brand.

**This sharpens, and partly corrects, the existing CRI guidance on [[12_Engineering_and_Systems/analysis/Lighting_Fixtures_and_Fittings|Lighting Fixtures and Fittings]]** — "CRI above 95" is a sound instruction, but a CRI figure alone is not a sufficient specification, and this is the reason why.

### ⚠️ 2. Flicker (коэффициент пульсации, IRF) — and a free test anyone can run

**Cheap LED lamps pulse at 50–90%**; above ~90% it is visible to the naked eye. A good GX53 lamp from a reputable maker measures **near zero**; the professional fixtures measured in the lab read **0%**.

- **Stated cause, which ties flicker to a component rather than to luck: the simplest capacitive driver («ёмкостный драйвер») and cheap parts.** Same root cause as the heat problem in §5 — both follow from driver and diode being sealed together in one cheap body.
- **⚠️⚠️ The test, and it is free: film the lit fixture on a phone with shutter speed set to minimum.** The pulsation becomes visible on screen. **→ Runnable in a shop, on a sample, or on fixtures already installed, before committing to a whole ceiling's worth.**
- **Stated consequences: eye fatigue, headaches, general tiredness**, and — claimed — degraded eyesight over time from sustained visual-system overload. `single-account`, `unverified` as a health claim.
- **Stated priority zones: wherever long periods are spent under artificial light** — reading, working, cooking. **→ Worth checking for this flat's work zone and kitchen worktop specifically, rather than treating it as a whole-apartment specification.**

### ⚠️ 3. Beam angle and UGR

**Beam angle**: a GX53 lamp throws **150–180°**, effectively in every direction. A professional fixture can be specified **from 5°** upward.

**UGR is the named glare/discomfort parameter** — how much a source strikes the eye; a measure of visual comfort. **The stated failure of the GX53 puck is behavioural and worth recognising: it is bright and unshielded enough that you avoid raising your eyes**, and end up looking straight ahead or down. **This gives the glare mechanism on [[12_Engineering_and_Systems/analysis/Lighting_Glare_and_Room_by_Room|Glare and Room by Room]] a parameter name to specify against.**

- **Remedies, available only from the better tiers**: anti-glare **grids** («решётки»), **tubes** («тубусы»), **rings**, and recessing the emitter deeper into the body.
- **⚠️ Optical accessories as a zoning tool, not only glare control**: an **oval-forming filter («овалорисующий фильтр»)** lights the oval of a work surface instead of filling the room from that point.
- **The principle behind all of it, and it is the argument for the whole page: under a properly designed scheme every fixture performs a named function, rather than merely being on or off.**

### ⚠️ 4. Colour stability — LED binning («биновка»)

**A nominal colour temperature is a band, not a point.** Several spectra qualify as "3000 K", and within that band **one lamp drifts green while another drifts pink** — both correctly measuring 3000 K. **This is the mechanism behind visible fixture-to-fixture colour mismatch in a room of cheap lamps.**

- **The named industrial fix is binning («биновка»): diodes are measured and sorted before assembly**, and only those inside the required window go into that fixture line; the rest are resold or used in a looser-tolerance line.
- **⚠️ Binning is not a feature that can be retrofitted or checked on delivery — it is a property of the production line, and it is a substantial part of what a premium price buys on this parameter.**

### ⚠️⚠️ 5. Lifespan, degradation, and the remote driver — the structural break

**The mechanism is structural, not a quality lottery: in a GX53 or GU10 lamp the driver and the diode are sealed in one body, usually plastic, with no heat path.** The driver heats, nothing carries the heat away, and **the diode degrades fast — noticeable brightness loss and colour divergence within 1–2 years**, leaving a ceiling where one fixture is a different shade from its neighbour and a third has visibly dimmed.

- **⚠️ "It's only a lamp, just replace it" does not work, and the reason is §4**: the replacement is also nominally 3000 K and still does not match its neighbours — so in practice the whole set gets replaced.
- **Professional construction answers it in three separate ways**: the **driver sits physically remote from the diode**, joined only by a wire, so driver heat never reaches it; the body carries a **proper metal heatsink**; and rated life is **45,000–55,000 hours**, after which brightness declines slowly and gradually rather than failing.
- **→ Remote-versus-integrated driver is the single most consequential yes/no question on this page**, and it is what separates tiers 5–8 from tiers 1–4 below. **It also corroborates, for downlights, the conclusion [[12_Engineering_and_Systems/analysis/Lighting_Fixtures_and_Fittings|Lighting Fixtures and Fittings]] reaches independently for LED strips and for integrated-LED chandeliers — the driver is the component that decides serviceable life, and it should be separate and reachable.**

### 6. Build quality, control protocols, and effects

- Cheap: poor plastic and components, poor assembly, poor paint, **unreliable spring mechanisms**.
- **⚠️ In 99% of cases a cheap fixture cannot be dimmed over a professional control protocol — DALI is named** (TRIAC also appears at the professional tiers). **→ If a protocol-controlled or smart scheme is wanted, the fixture tier decides whether it is possible at all, so that decision precedes the fixture purchase.** See [[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Smart Home Systems]].
- **Tunable colour temperature within one fixture** (4000–5000 K morning, 3000 K evening) is a better-tier capability.
- **Professional-only effects**: **framing light («кадрирующий свет»)**, lighting a defined rectangle such as a picture or a door, stated to exist only in top lines; **gobo filters** for coloured or light-and-shadow patterns; and **wall washers**, ceiling-mounted to wash a wall or a defined corner.

## The Eight-Tier Ladder

> [!IMPORTANT]
> **This is one practitioner's own subjective scale and he says so twice** — «максимально субъективную шкалу… Я их сам придумал» — assembled from five expert meetings and a lab visit, not from any standard. **Record it as a structured framework, not an industry classification.** Its value is that it makes a 100× price span navigable in steps instead of as a binary.

| Tier | What it is | What changes at this step |
| :--- | :--- | :--- |
| **1** | Cheapest GX53 fixture + lamp, **≈110 RUB (≈$1)** the pair | **Avoid entirely.** The defect is *dishonest* specification: "CRI 90" on the box bears no relation to measurement, and the buyer cannot tell except by price |
| **2** | Same GX53, reputable maker — Philips, Osram, Gauss, Навигатор | Honest figures: little or no flicker, an honest CRI near 90, better life. **Every format defect remains** — ~180° puck, high UGR, no heat path, wide colour spread, R9 capped ≈10%, no adjustment |
| **3** | MR16 fixture taking a GU10 / GU5.3 lamp (example named: ArtLamp "Inter") | **The fixture separates from the lamp, so the emitter can be recessed** — UGR improves at once, and a grid or tube becomes fittable. **The GU10 lamp still has driver and diode in one plastic body**, so §5 degradation is unchanged |
| **4** | Same fixture, **LED module** instead of a GU10 lamp | Better diode, better driver, **choice of beam angles**, proper binning, longer life — **but the driver is still inside the module body**. The source is openly unsure how much a denser (possibly ceramic) body helps |
| **5** | Same module class, **driver brought OUT** (example: an SVG module with a remote driver) | **The structural break in the ladder.** No overheating, so the assembly reaches its full rated life. Every tier above has a remote driver; every tier below does not |
| **6** | **Premium.** Complete fixtures, no replaceable source. Entry lines named: SVG "mini Combo", ALED "Pola" | One-piece body, always a remote driver, aluminium body **and** aluminium heatsink, **CRI ≥ 90**, binning, wide angle choice, DALI/TRIAC dimming, moisture-protected and aimable variants |
| **7** | **Premium constructor.** Body → module (angle, temperature) → frame → optional grid / tube / diffuser. Named: SVG Combo 43 + Combase; ALED "Trix/Trace" (`ASR-uncertain`) | **Variability within one fixture family.** CRI 90–97; Philips drivers named at one maker |
| **8** | **Maximum customisation.** Named: SVG "KOB 2.0"; ALED "Aspect SPTW68" (CRI to 97), **11,000–15,000 RUB ≈ $140–$190** each | Mounting frame (black/white, stretch **and** plasterboard ceilings), module with a **needle/pin-type heatsink** maximising dissipation area, **six lens options**, **variable recess depth of the diode**, anti-glare ring hiding the source until you stand beneath it |

*Prices: Russia, marketplace, 2026. USD at **78.1048 RUB/USD**, trailing-6-month mean before the confirmed publish date 2026-09-11. At the 110-RUB magnitude the USD equivalent falls below the rounding convention's smallest bucket — it is given as a whole dollar and carries no precision beyond "about one dollar". **The load-bearing figure is the ratio, ~100×, which is scale-free.***

- **⚠️ Stated world trend, and it explains tier 8's feature set: minimise the visibility of the light source.** Already visible in design-project renders and on Pinterest.
- **⚠️⚠️ Two buyer-side actions the source offers against his own tier argument, both free.** **(a) Take your own intended fixture to a professional lighting company and ask them to run the same measurement on it**, as he did in the lab. **(b) Run the phone-camera flicker test yourself** (§2). **→ Neither requires buying anything, and both convert this page from a hierarchy into something checkable.**
- **You need not buy the top line**: reputable makers have entry ranges where the parameters are at least honestly stated. The stated purpose of the exercise is to make the axes legible, not to sell tier 8.

## ⚠️⚠️ Perspectives — Is the Spread Worth Paying For? Two Professionals, 100× Apart

**This vault holds two directly opposed positions on the same question, and neither speaker is disinterested. It is not resolved here.**

- **Сергей Реньжин (lighting designer, already recorded on [[12_Engineering_and_Systems/analysis/Lighting_Fixtures_and_Fittings|Lighting Fixtures and Fittings]]) puts the visible difference between a good and a mediocre fixture at only 15–20%**, says recessed fixtures can be bought cheap, and says Chinese fixtures are fine — **and he states this against his own commercial interest**, which is the strongest thing in its favour.
- **Константин Круглов / Ontario argues a ~100× spread**, with measured parameters behind it and a laboratory visit to support them — **but he runs a turnkey renovation company whose revenue scales with the specification level its clients choose**, and the video's structure argues upward across eight tiers.
- **What can be said without picking a side.** The two are not quite answering the same question: Реньжин is talking about **how different the lit room looks**, Круглов about **how the fixtures differ as products** — R9, flicker, UGR, binning, degradation. **A parameter can be real, measurable and still make only a modest difference to the appearance of a finished room.** Flicker and R9 are the two where the gap is least likely to be cosmetic, because one is a comfort-and-fatigue claim and the other governs how skin and wood read.
- **→ The usable synthesis, given this project is self-managed: the parameters are worth demanding as figures because they are free to ask for, and the phone-camera flicker test is worth running because it costs nothing. Whether to buy up the ladder is a separate decision, and Реньжин's 15–20% is the honest counterweight to keep next to it.**

## Related

- [[12_Engineering_and_Systems/analysis/Lighting_Fixtures_and_Fittings|Lighting Fixtures and Fittings]] — fixture taxonomy, ceiling-depth traps, replicas and procurement, chandeliers, LED strip.
- [[12_Engineering_and_Systems/analysis/Lighting_Design|Lighting Design]] — scheme planning, layers, illuminance targets.
- [[12_Engineering_and_Systems/analysis/Lighting_Glare_and_Room_by_Room|Glare and Room by Room]] — where light must not go.
- [[12_Engineering_and_Systems/analysis/Lighting_Colour_Temperature|Lighting Colour Temperature]] — Kelvin, the same-scene rule, the melatonin threshold.
- [[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Smart Home Systems]] — control protocols and biodynamic scenes.
