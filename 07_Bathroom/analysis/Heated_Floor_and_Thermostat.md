# Bathroom — Heated Floor & Thermostat Placement

Covers underfloor heating cost/scheduling, area-cap/sensor-redundancy rules, and a real practitioner disagreement on thermostat mounting height. Part of [[07_Bathroom/Bathroom_Guide|Bathroom Guide]].

## Cost, Scheduling, and Sensor Redundancy

Older archive-only cost claims lack a decisive extraction-note `channel:` field. The page's [Bathroom Source Notes](Source_Notes.md) is the most specific remaining trace; no more-specific extraction-note link was recovered for the legacy cost figures.

**Electric underfloor heating, cost and control**: a full setup (heating mat, thermostat, installation) is cited around **~30,000 RUB** — described as easily worth it if the budget allows, with no real downsides beyond cost. Because tile heats and cools slowly, it can't be toggled on-demand like a light switch — the source runs theirs on a schedule (starting ~6am to be comfortably warm by ~9am). [source: [[_Archive/processed_sources/20260731_video_6lacLnqpJbM_4b68d812.txt|video_6lacLnqpJbM_4b68d812]]]

- **Heating-mat area cap and sensor redundancy**: one practitioner caps underfloor heating mats at **~12 m²** per mat/zone. Each mat should have **3 temperature sensors, not 1** — the sensor itself is described as more likely to fail than the mat, and a failed single sensor leaves no way to control (or safely confirm the state of) an otherwise-working mat. `single-account`, `unverified`. [sources: `_Archive/processed_sources/20260804_business_class_five_attributes_19385e7a.txt`, `_Archive/processed_sources/20260804_pro_secrets_lifehacks_f0be401f.txt`]
- **Multi-mat rooms need a multi-loop plan, plus one aggregating controller so occupants don't have to walk between thermostats**: a room larger than the ~12 m² cap needs either a center-only or perimeter-only mat, or two separate mat loops each with its own thermostat. Worked example: living room = two 12.6 m² mats, kitchen = two 12–14 m² mats, each room with two thermostats. To avoid forcing occupants to operate multiple room thermostats separately, install one aggregating app/controller that lets every room's thermostats be operated as a group from one interface. `single-account`. [source: `_Archive/processed_sources/20260804_business_class_five_attributes_19385e7a.txt`]
- **A distinct, smaller-scale running-cost figure, recorded separately per this project's non-blending convention (added 2026-08-28, Round 5)**: Konstantin Kruglov / Ontario cites roughly **100-150 RUB/month** for an average bathroom's electric heated floor running continuously (24/7) — meaningfully lower than this page's existing formula-derived worked example (≈2,500 RUB/month for a 30m² zone), consistent with a bathroom's much smaller floor area rather than a contradiction, but not merged into the existing formula. `single-account`, `unverified`. [source: [[_Sources/YT__XCBMJmosDk_kruglov_ideal_bathroom_10_rules|YT__XCBMJmosDk]]]
- **A worked heated-floor scheduling example, corroborating and adding a specific schedule to the "runs on a schedule, not toggled on-demand" guidance above (added 2026-08-24, Round 5)**: Kruglov's own bathroom thermostat runs two daily heating windows, 6:00-9:00 and 16:00-20:00, timed so the floor is already warm for the morning and evening routine, while the tile's own heat retention keeps it comfortable between active heating periods. Framed as a meaningful electricity saving versus continuous operation; the source suggests narrowing the total daily active window further (to 4-6 hours/day) saves even more. `single-account`, `unverified`. [source: [[_Sources/YT_1x7srLdq12I_kruglov_perfect_sanuzel_secrets|YT_1x7srLdq12I]]]

## Failure Modes and Sensor Lifespan (added 2026-08-24, Round 5)

Per Kruglov/Ontario: **the heating mat itself rarely fails when installed and used correctly** — he names Термотех/Thermo as a reputable brand that warranties the mat, and states this matches his own practical experience. **The actual common failure point is the temperature sensor or a cheap thermostat unit**: he singles out a roughly 800 RUB marketplace thermostat as a concrete example of a unit that fails almost immediately ("they burn out immediately") — corroborating, with a specific cheap price point, this page's existing "cheap thermostats fail" framing elsewhere in this store.

**A separate installation-error failure mode**: tile-setters can physically damage a heating mat's own insulation while spreading tile adhesive, causing the heating element itself to burn out — a workmanship risk distinct from a component-quality risk.

**A second, distinct installation-error window, new for this store (added 2026-08-28, Round 5)**: Konstantin Kruglov / Ontario identifies a failure point *between* tiling and grouting, not just during adhesive spreading — a tile-setter cleaning excess adhesive out of the joints to prepare them for grout can physically nick/cut the heating cable sitting just beneath the tile, even after the mat already tested fine post-tiling. **Recommended mitigation**: protect the mat with a cement-based self-leveling screed poured over it (between the mat and the tile) rather than embedding it directly under tile adhesive alone, and re-test continuity a second time after tiling, before grouting. `single-account`, `unverified`. [source: [[_Sources/YT_BDudniuyJ4s_kruglov_bathroom_mistakes_every|YT_BDudniuyJ4s]]]

**Sensor lifespan and repairability**: a correctly installed sensor from a quality thermostat can last **20-30 years**; if it does fail, replacement is normally a simple swap with no need to open the tile — **except** when the original installer embedded the sensor's conduit incorrectly (e.g. concreted over with no accessible sleeve to pull a new sensor through), in which case a **sensorless thermostat** (available from Thermo and other manufacturers) is a real fallback: these units make heating decisions from internal logic/ambient air temperature instead of a floor-embedded sensor, avoiding any future need to access the embedded sensor at all. `single-account`, `unverified`. [source: [[_Sources/YT_1x7srLdq12I_kruglov_perfect_sanuzel_secrets|YT_1x7srLdq12I]]]

## Operating-Cost Formula and a Second, Distinct Area-Cap Mechanism (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 4)

Low promotional ratio, general explainer (no active project). [source: [[_Sources/YT_9ndMjQLTF9E_sbk_heated_floor_downsides|YT_9ndMjQLTF9E]]]

- **⚠️ Named operating-cost formula, distinct from this page's existing ~30,000 RUB installation-cost figure**: (room area m²) × (mat power density W/m², real examples 130-180 W/m²) × **0.4** (derating coefficient for mandatory wall/heat-source/furniture clearance) = power draw. Worked example: 30 m² × 180 W/m² × 0.4 ≈ 2 kW draw; at ~9 hours/day average active cycling, ≈20 kWh/day; at a 4.5 RUB/kWh tariff, ≈90 RUB/day (≈$1), ≈2,500 RUB/month (≈$30) for one 30 m² zone. Scaled claim: a 100 m² apartment on underfloor heating costs at minimum ≈7,000 RUB/month (≈$80) in electricity.
- **⚠️ A second, distinct thermostat area-cap mechanism, separate from this page's existing ~12 m²-per-mat cap**: a standard thermostat has its own average power limit of ≈3.5 kW — at 180 W/m² mat density, this caps a single thermostat's coverage to ≈20 m², independent of the mat-sizing convention already documented above. A lower-power mat allows a larger area on the same thermostat, but the cap always exists.
- **⚠️ Named design-coordination failure**: a large open kitchen-living room (>40 m², the speaker's recurring example) sometimes gets drawn as one single heating loop without checking whether a thermostat can actually support that area — surfacing only at installation, forcing a late correction (splitting loops/thermostats) and a scramble for wall space not originally planned.
- **⚠️ Mat wattage determines achievable floor temperature**: an underpowered mat for the specific floor buildup (screed, tile, or self-leveling compound thickness) simply can't reach the expected temperature — a real physical ceiling exists above which the floor can't get hotter regardless of mat power, a physics limit, not a defect.
- **⚠️ Repair-compounding mechanism**: repairing underfloor heating under tile installed several years earlier (example: 3+ years) commonly runs into discontinued/unmatched tile, forcing a full floor demolition and re-tile even for a small, localized heating-element repair.
- **Specialist-scarcity claim**: locating the point to open a floor for an underfloor-heating repair requires a genuine specialist skill, and very few such specialists exist — expect a long search and high labor cost.

## Thermostat Mounting Height — Practitioners Disagree

Zemstandart's placement claim is verified against `YT_uwXBHuWPUIo_underfloor_heating_thermostat_placement.md`; the opposing height-by-use claim remains without a confirmed channel unless its cited extraction note is recovered.

**The question**: how high should a thermostat be mounted, and does that answer depend on the specific unit's usage pattern?

**Perspectives:**

| Source | Position | Reasoning |
|---|---|---|
| Unnamed source (heated-floor cost/scheduling video, above) | Mount height should scale with how often you'll adjust it | A simple on/off thermostat can go anywhere. A programmable (set-and-forget) one can be low/out of sight. One you expect to adjust frequently should be mounted higher, at a convenient reachable height. |
| Zemskov / Zemstandart (Moscow, apartment-wide, not bathroom-specific) | Flat eye-level (160-170cm) for every thermostat, regardless of type | An LCD display, unlike a smartphone screen, is only legible head-on, not at an angle — a low unit forces crouching to read/operate. He explicitly rejects the common "mount high so kids can't reach it" child-safety framing as his actual reason, and separately notes he finds it ineffective in practice (children lose interest in switches quickly). |

**Common ground**: both are `single-account`, and neither directly rebuts the other's specific reasoning (usage-frequency vs. display-legibility) — they're answering slightly different questions, which is part of why this doesn't resolve cleanly into "one is right."

**Your priority**: *— not yet decided.* Zemskov's rule is a flat default requiring no case-by-case judgment; the other source's rule requires deciding, per thermostat, how often you expect to actually touch it. If most of this project's thermostats will be set-and-forget (programmable schedules, rarely touched), the first source's logic argues for low/hidden mounting; if you expect to check/adjust them often, both sources converge on mounting them higher.

### Zemskov's Full Placement Rules (apartment-wide)

> [!NOTE]
> This subsection is Zemskov/Zemstandart's own stated practice and reasoning, `single-account`, no cost figures given. [source: `_Archive/processed_sources/20260810_underfloor_heating_thermostat_placement_e9333bb7.txt`]

- **Core rule: a thermostat must always be visibly mounted, never hidden** — unlike a light switch (the light itself signals state), a hidden thermostat gives no way to check on/off/temperature without walking to it.
- **WC/bathroom-specific rule: mount the thermostat outside the room it controls, never inside** — lets you check at a glance (before entering, or on the way out of the apartment) whether it was left on. **General heuristic he gives**: place the thermostat on the same side (inside or outside the room) as that room's own light switch.
- **Thermostat-type recommendation**: an "electro-mechanical" type (LCD display for information only, physical tactile buttons for control) over a fully mechanical dial (no way to confirm the current setting from a distance) or a fully touchscreen unit (sluggish feel versus a smartphone; his estimate ~98% of clients with a fully-loaded unit use only one function despite paying for the extra complexity).
- **Single most emphasized rule: always extend the thermostat's temperature-sensor wire by soldering, never with twist-splices or standard connectors** — a stock sensor wire is too short for eye-level mounting; soldering is, per Zemskov, the one place in a modern renovation he still recommends it, since the joint must repeatedly pass through a dedicated conduit as sensors (unlike heating elements, which he says rarely fail now) do eventually need replacing. **Install that conduit from the thermostat down to the sensor pocket at rough-in stage** — without it, a failed sensor can't be practically replaced later without disturbing the finished floor.

> [!NOTE]
> **Zemskov's own reasoning on child-safety changed over a 4-year gap, worth flagging rather than silently reconciling.** An earlier (2018-12-23) same-channel video (`yt_zaZGEW8sdV4`, #011) states child-safety genuinely *is* a reason for eye-level mounting — its stated mechanism: kids lose interest in tampering with a simple light switch quickly, but stay engaged with an "electronic gadget"-like thermostat display much longer (his own estimate: roughly ages 2-7). The 2022 source above (`yt_uwXBHuWPUIo`) explicitly argues the *opposite* — that child-safety is not the real justification, only LCD legibility is. Recorded as a genuine, unresolved change/inconsistency in the same practitioner's stated reasoning over time — not evidence either individual account is unreliable, but a caution against treating any single-channel "stated reason" as fixed. **Two additional, genuinely new details from the earlier source**: (1) an alternative fix for the short-sensor-wire problem — buy a thermostat/sensor kit with a long sensor wire from the start if planning eye-level mounting, instead of (or in addition to) soldering an extension; (2) a multi-gang layout rule — when a switch plate and adjacent thermostats both control multiple rooms, position each thermostat directly above its corresponding room's switch, not stacked arbitrarily, so the switch-to-thermostat mapping is immediately intuitive. [source: `_Sources/YT_zaZGEW8sdV4_underfloor_heating_thermostat_placement_earlier_011.md`]

## ⚠️ Underfloor-Heating Cable Is Not Cut On Site — and What a "Lifehack" Running It Up the Wall Actually Reveals (Надежда Кузина, added 2026-09-01)

A debunk of a short-form clip proposing that the heating cable be run up the wall where a towel warmer would go, plastered over, so the wall becomes warm. **Three objections in ascending order of force, and the third is the one that matters for specification.** [source: [[_Sources/YT_UnCjxyDtWG0_kuzina_tiktok_lifehacks_debunked|UnCjxyDtWG0]]]

1. **The space argument is weak.** A towel still needs a holder and still occupies the space. **What difference whether it hangs on a rail along the wall or over a towel warmer?**
2. **⚠️ The physical one: a towel dries faster over a towel warmer because it is thrown over it and dries from BOTH sides. On a holder against a wall it dries from one side only — and through the tile.** *(Belongs with the towel-warmer material on [[12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer|Hygienic Shower & Towel Warmer]].)*
3. **⚠️ THE INSTALLATION FACT: underfloor-heating cable is never cut on site, because it fails either immediately or after a very short time.** Her evidence is indirect but good: **"если бы тёплый пол можно было так легко соединять и разъединять, то не существовало бы специально обученных людей, которые занимаются ремонтом тёплых полов — это прям отдельная индустрия."**

**⚠️ Her diagnosis of what the "lifehack" actually is, and it is the kind of inference that only comes from site experience:**

> **If you find yourself able to do this, you probably over-ordered the underfloor heating relative to your bathroom's area, and now have to contrive somewhere to put the surplus — because cutting it is not an option.** **"Строители подают это как супер крутой лайфхак, но на самом деле это просто результат их собственного просчёта."**

**⚠️ And a running-cost consequence nobody mentions: once you have finished in the bathroom you no longer need the floor heating, but you do want the towel to keep drying — and the rail and the floor are now ONE device on one circuit. You spend extra electricity to dry a towel.**

## ⚠️ What the Underfloor-Heating Drawing Must Carry (Татьяна Михайловская, added 2026-09-01)

**The plan-side counterpart to this page's existing finding that the cable cannot be cut on site: if the zones are not dimensioned at design stage, the over-order that follows has nowhere to go.** [source: [[_Sources/YT_MkssMwpyVsI_mikhailovskaya_design_project_composition|MkssMwpyVsI]]]

Her project carries **two systems — electric and from a gas boiler — distinguished by colour on the plan.** What the sheet must show:

- **⚠️ The AREA of each specific heating zone, stated explicitly so that purchasing is easier.**
- **⚠️ Offsets from the walls, drawn.**
- **⚠️ No heating under furniture. None under appliances.**
- **⚠️ And agreed with the client** — she names this as a step, not an assumption.

## ⚠️ Underfloor Heating Mandatory in a Bathroom, and a Recessed Towel Warmer for Small Rooms (Татьяна Безверхая, added 2026-09-02)

Moscow-practice designer, 2024, bathroom guide (`promotional_ratio: medium`, sponsored tile mid-roll excluded). [source: [[_Sources/YT_T3b-IS4Rb0E_bezverkhaia_ideal_wc_ten_rules|T3b-IS4Rb0E]]]

- **⚠️ Underfloor heating is always required in a bathroom — "всегда нужен тёплый пол в санузле."** **In an apartment it can only be electric; in a house, electric or hydronic.** **This is the third and fourth account in this vault of the apartment-electric-only rule** — after Kruglov/Ontario on [[13_Surfaces_and_Finishes/analysis/Flooring_Material_Selection|Flooring Material Selection]] and her own replanning source this round, consolidated on [[17_Design_and_Ergonomics/analysis/Whole_Home_Planning_Method|Whole-Home Planning Method]]. **Russian jurisdiction on the legality half; still no code cited by any source.**
- **Good fall in the shower so water does not pool** — a separate requirement from the underfloor heating, though she treats them together as what makes a bathroom comfortable.
- **⚠️ A towel warmer is required, and in an apartment she prefers electric on a functional argument: a hydronic one is "мало функционален"** — it only works while the building's system is running. In a house, either.
- **⚠️ The additive item for this page: an electric towel warmer can be recessed into the wall under tile, or under paint, with hooks above the mats so towels dry against the wall.** She offers this specifically as **the answer for small bathrooms with no room for a conventional towel warmer** — a genuinely space-free option this page did not hold.

**⚠️ No prices, no wattages and no coverage figures anywhere in the source** — the recommendation is categorical without any sizing guidance, so pair it with this page's existing sizing content before specifying anything.

## ⚠️⚠️ Perspectives — A Designer Who Deliberately Omitted It, Twice, and Leaves the Question Open

> [!IMPORTANT]
> **This is a direct dissent from the "always required" position above, from a designer reporting on his own two flats rather than on client work — and he declines to settle it, which is why it is recorded as a Perspectives split.** [source: [[_Sources/YT_lhikl-7c43c_nsdsgn_own_flat_year_one_fixes|YT_lhikl-7c43c]]]

**Александр Сенчугов, a year into his own Petersburg flat: «в ванной есть СПОРНЫЙ момент, который я ДО СИХ ПОР НЕ РЕШИЛ, правильно я сделал или неправильно: я в ванной НЕ СДЕЛАЛ ТЁПЛЫЙ ПОЛ.»**

- **His evidence for the omission: «я жил в предыдущей квартире 5 ЛЕТ без тёплого пола и НИ РАЗУ об этом не жалел.»** So two flats, one of them for five years.
- **His evidence against: «пару раз было, когда у меня было очень мокро на полу, и я думал — если бы я сделал, было бы прикольно, было бы теплее.»** Note the complaint is a **wet** floor, not a cold one.
- **⚠️⚠️ AND THE MITIGATION THAT RESOLVED IT IN PRACTICE, which is the transferable finding: «я это решал просто ВКЛЮЧИВ ТЁПЛУЮ СТЕНУ, и всё МОМЕНТАЛЬНО ВЫСЫХАЛО.»**
- He puts the question to viewers rather than answering it, so **it stays open in this vault too.**

**Common ground.** Both practitioners are solving the same two duties — **comfort underfoot** and **drying the room** — and both treat a heated surface as necessary for the second. Neither disputes that a cold, damp bathroom floor is a defect. **The same practitioner elsewhere states the general principle explicitly: mould needs standing water and humid air, and the cure is ventilation plus HEATING the air, «и в этом случае поможет ТЁПЛАЯ СТЕНА ИЛИ ТЁПЛЫЙ ПОЛ»** — either satisfies it. See [[07_Bathroom/analysis/Bathroom_Design_and_Palette|Bathroom Design and Palette]].

**Where they actually differ: which surface carries the heat.** Безверхая treats the floor as mandatory and the towel warmer as an additional requirement; **he finds a heated wall alone sufficient for the drying duty and lives without the floor.**

> [!NOTE]
> **⚠️ These two positions may be closer than they read, because Безверхая's own recessed-towel-warmer recommendation immediately above IS a heated wall** — «электрический полотенцесушитель можно ЗАМУРОВАТЬ В СТЕНУ под плитку, или под покраску, с крючками выше мата». **She offers it as the answer for a bathroom with no room for a conventional rail; he is using the same device as a substitute for the floor.**
>
> **→ Your priority: if the complaint you are designing against is a WET floor, a heated wall is evidenced to solve it and is the cheaper item. If the complaint is a COLD floor underfoot — a tiled floor over an unheated slab, or an insulated balcony where «плита примерзает с торца» — nothing on the wall reaches it, and this vault's other sources are unanimous.** The two duties are separable, and only the first has a wall-mounted answer. Cost and scheduling for both are in the sections above.
