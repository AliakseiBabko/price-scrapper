# HVAC — Fresh-Air Ventilation & Ducting

Covers breathers vs. full mechanical ventilation, the shared-shaft constraint kitchen hoods also run into, supply-ventilation contracting, and duct sizing/soundproofing. Part of [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]].

Prolife Invest's dated Moscow comparison puts a full ducted supply-and-exhaust ventilation system at **1.5–10 million RUB** as of 2026-07-29. Using the trailing six-month USD/RUB average of 76.4100, `1,500,000 ÷ 76.4100 = $19,630.94` and `10,000,000 ÷ 76.4100 = $130,872.92`, or **≈$19,600–≈$131,000** in the nearest-$100 and nearest-$1,000 buckets respectively. The same source gives a breather figure rendered as “1,350” without a confirmed unit; that number is **not computable** and is not converted. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_DsdLa87Acz4_prolife_invest_moscow_flipping|extraction note]]]

## Whole-Apartment Airflow-Balance Design Methodology (added 2026-08-25)

ADS-vent.ru (ventilation-design/installation company, worked teaching example, region unresolved — general engineering methodology, not jurisdiction-specific) walks through a complete supply+exhaust design sequence, genuinely different from the rest of this page's per-device/per-fixture content — this is the *coordination* methodology across an entire unit, not a single fixture's technique:

- **Size total required airflow with single air-exchange-per-hour**: full room volume turns over once per hour as the residential comfort baseline (worked example: 3m ceilings × 87m² ≈ 260 m³/h for one floor).
- **⚠️ Never tie a kitchen hood's dedicated exhaust riser into the kitchen's general natural-exhaust stack** — a third, independent riser is required; conflating the two is described as a common installer mistake despite being against code. Kitchen and bathroom/toilet natural-exhaust stacks are, by default building convention, two separate risers, each serving only its own room type.
- **⚠️ The core balance-table technique**: "dirty zone" rooms (bath/toilet, kitchen, utility) get exhaust only; "clean zone" rooms (bedrooms, living room) get supply sized to *exceed* their own exhaust need by exactly what the dirty zones draw — producing a pressure gradient (slight negative pressure in dirty zones, slight positive in clean zones) so air flows from clean into dirty zones, containing odors rather than letting them spread. Reconciled to a whole-floor total in the worked example (260 m³/h ground floor, 410 m³/h whole building including the second floor).
- **⚠️ A fan's rated airflow is a curve against duct-network resistance (pascals), not a fixed number**: worked example shows the same unit delivering 400 m³/h at 100 Pa resistance but only ~300 m³/h at 150 Pa — route ducts with as few bends/branches as possible to preserve real delivered airflow.
- **⚠️ Duct velocity should stay ≤4-5 m/s in main trunks because resistance scales roughly with velocity squared**, not linearly — doubling velocity in a worked comparison (160mm duct, 300 vs. 600 m³/h) showed a measured 4x resistance difference for just one meter of straight duct, against a total system pressure budget of only ~100-150 Pa.
- **⚠️ Exterior wall/roof termination grilles are often the single largest resistance point in an otherwise well-sized system**: a standard round exterior grille at 300 m³/h through 160mm duct showed ~40 Pa resistance — upsizing to a 200mm duct/grille just before the wall penetration dropped that to ~15 Pa.
- **⚠️ Fan/unit selection rule: size around the single most heavily-loaded duct path** (exterior grille to the most distant/most-resistive room grille — not necessarily the physically longest run), not an average. Full worked calculation totaled ~67 Pa on the exhaust branch and ~57 Pa on the supply branch before matching both against the selected unit's own spec curve at the required flows.
- **⚠️ Post-installation manual damper balancing at every grille is a required commissioning step, not optional** — most semi-residential units can't independently regulate supply vs. exhaust to different target flows in software; skipping manual balancing risks the exhaust side pulling more than the supply side delivers, degrading natural exhaust risers and risking **backdraft** through them.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_bZTJv6aZevw_adsvent_ventilation_design_methodology|bZTJv6aZevw]]]

### Second Voice: Combined Passive-Supply + Mechanical-Exhaust System, Private-House Context (added 2026-08-25)

"Строительство, проектирование, бизнес-обучение" (private-house ventilation installer, Russia level 1, region unresolved to city, `promotional_ratio: medium`) — a private-house context, but the balance/compensation logic transfers to an apartment:

- **⚠️ Natural exhaust ventilation's seasonal/height-dependent failure, extending the "bottle-cap" mechanism above**: draft depends on the indoor/outdoor temperature differential — **effectively stops entirely in summer**; only reasonably effective on 2-3 story buildings with a long enough shaft run (5-7m); "practically ineffective" on single-story buildings. **Even a multi-story apartment building's shared shaft is unstable by floor**: lower floors get excess draft, middle floors normal, upper floors reportedly no usable draft at all. `single-account`, `unverified` on the apartment-floor claim specifically.
- **A centrifugal-turbine exhaust fan holds its rated output better under real duct+grille resistance than a typical vane/screw fan** — a concrete comparative example (stable ~100 m³/h vs. a vane fan's rated 230 m³/h dropping 30-40% once real ducting/grilles are attached). Self-interested (favors the practitioner's preferred brand) but the underlying mechanism is a checkable engineering distinction, recorded with that caveat.
- **Balancing airflow between duct runs of different lengths via fixed inline restrictors (15/30 m³/h) on the shorter run** — a distinct technique from video 1's adjustable end-grille dampers, addressing the same "air takes the path of least resistance" problem.
- **Kitchen-hood exhaust must be a fully separate system from the general background exhaust fan** — corroborates video 1's code-based rule with a mechanistic reason: grease-laden air fouls fan blades and risks imbalance over time.
- **Kitchen-hood makeup-air compensation**: a dedicated supply valve placed opposite the hood in the kitchen/living zone, since hood airflow (250-500 m³/h by speed) can otherwise draw down bedroom valves' intended supply — extends video 1's balance-table methodology with a hood-specific compensation case.
- **A dissenting, more skeptical voice on heat-recovery units**: this practitioner considers compact cyclical heat-recovery units of limited value outside a single isolated room, citing a -10°C to -15°C practical limit before internal condensate freezes — calls them "a gimmick." `single-account`, `unverified`, contrasts with this page's existing more neutral Goncharov-sourced heat-recovery taxonomy entry above — record as a genuine practitioner disagreement, not a resolved contradiction.
- **Pricing, Russia, 2023-03-07**: exhaust fan + full installation ≈65,000 RUB ≈ $700; supply valve installed ≈5,000-5,500 RUB ≈ $50-60 each; full small-house system (2-3 valves + exhaust) ≈80,000-95,000 RUB ≈ $800-$1,000 (trailing-6-month USD/RUB average). **Labor-Only-adjacent / small-installer turnkey** delivery model — not comparable to a full-service company's overhead.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_ctPLFrzuIqg_house_ventilation_explainer_valves|ctPLFrzuIqg]]]

### Third Voice: Single-Flow vs. Two-Flow Architecture, Real-Project Ceiling-Zone Planning (Forcemontage, added 2026-08-25)

Forcemontage (turnkey renovation company, in-house HVAC specialist interview, real project, region unresolved, `promotional_ratio: medium`):

- **⚠️ Single-flow vs. two-flow system taxonomy**: single-flow = passive supply (window/wall valves, driven only by exhaust-created vacuum, no per-room mechanical regulation) + mechanical exhaust — chosen specifically where low ceiling height rules out full ducting through living spaces; two-flow = both supply and exhaust mechanical (separate units or one combined unit, optionally with heat recovery).
- **Real-project ceiling-drop-by-zone worked example**: technical zone (AC air handler + exhaust fan + supply unit) 350mm drop; corridor/transit zone 150-180mm; bathroom zone also dropped; **living spaces kept duct-free entirely** by routing everything through technical/transit zones only.
- **AC outdoor-unit placement, four real cases**: a pre-designed facade basket needs no management-company approval; direct facade mounting without one does; balcony placement works but makes the balcony unusably hot; **ventilated-facade-cavity recessing** (bracket-mounted to the structural slab, with a separate serviceable access hatch) is a real solved alternative saving boxing space.
- **⚠️ Sash-integrated humidity-auto-regulating supply valve — a genuinely distinct installation technique from this page's window-reveal L-duct method**: the valve mounts inside the window sash's own pressure-seal channel (milled without cutting the internal metal reinforcement), installed during finish-stage work, with the exterior side concealed under the sash handle's cover plate — **no visible exterior penetration at all**. A wall-mounted equivalent exists too (same auto-regulating valve, duct chased into the wall behind finish). Incoming air is directed toward the ceiling to mix with heating-system warm air before reaching occupant level, avoiding a felt cold draft.
- **Cost range (region-unresolved, area-basis ambiguous, not comparable to this page's other pricing)**: "economy system, ~2,500-10,000 RUB/m²" cited as a bare data point.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_7vjW6SzHeWM_forcemontage_ventilation_types_cost|7vjW6SzHeWM]]]

### Fourth Voice: Four-Way Comparative Framework, and a Critical Single-Breather Limitation (Dmitry_HVAC, added 2026-08-25)

Dmitry_HVAC (individual HVAC specialist, Russia level 1 for general practice — real projects named in Moscow and St. Petersburg; the specific headline price below is region-unresolved-to-level-1, `promotional_ratio: medium`) ranks four ventilation approaches (window airing → passive valve → active local breather → centralized ducted system) against a consistent criteria set: filtration, preheat, volume control, noise, design integration, weather-dependency, cost, install-stage constraint, operating cost.

- **⚠️ Critical caveat against relying on local breathers alone for whole-apartment balance**: air from a single local breather installed in one room does **not** spread to other rooms — it travels the path of least resistance straight to the nearest exhaust point (worked example: a unit in one room with a nearby bathroom exhaust pulls air directly to that bathroom, never entering adjacent rooms). **A multi-room apartment needs one breather per room for guaranteed air quality in each room** — a few strategically-placed breathers are not a substitute for a properly designed, fully ducted balance system like video 1's methodology describes.
- **Window-sash valve warranty risk, explicit claim**: cutting a passive valve into a window sash voids the window manufacturer's warranty outright, per any window company, regardless of window or valve quality. Real failure cases: condensate freezing on a windward-facing valve; rainwater leaking directly into a valve during a storm.
- **Passive-system seasonal cutoff, cited to an unnamed study, `unverified`**: natural-draft/passive-valve ventilation is reported to become essentially non-functional above ~+5°C outdoor temperature.
- **Terminology, independently corroborating the existing Goncharov-sourced note**: "рекуператор" properly names only the heat-exchanger module, not the whole ventilation machine — a second independent source flagging the same common mislabeling.
- **Rough-stage-only installation rule, reinforced with a real "we tried, we stopped" data point**: the company attempted finish-stage centralized-system retrofits a couple of times, does not recommend it, and no longer takes on such jobs.
- **Acceptance-test technique**: use a CO2 meter to verify real air exchange, since a well-designed system can be genuinely inaudible — noise level alone doesn't confirm the system is working.
- **Verify a building's ventilation-modification restrictions with the management company before purchasing**, not after — real case cited of a very expensive Moscow/St. Petersburg apartment with zero ventilation-modification allowance.
- **Pricing**: active breathers observed at 29,000/37,000/40,000/58,000 RUB, top-tier ~80,000 RUB (a fourth independent breather price reference point on this page). Centralized system "from" **≈600,000 RUB ≈ $6,600** (trailing-6-month USD/RUB average to 2023-10-29) — region-unresolved-to-level-1 for this specific figure despite the channel's broader Moscow/St. Petersburg practice.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_EUM7kv77VVY_dmitry_hvac_top4_comparison|EUM7kv77VVY]]]

## Breathers vs. Full Mechanical Systems

A separate decision from AC sizing. One practitioner's framing, worth treating as a reasonable starting heuristic rather than settled fact:

- A **wall-mounted "breather" unit** (a local fresh-air intake/filter device) is reported to handle the majority of typical indoor air-quality needs at a fraction of the cost of a full system.
Prolife Invest recommends: **full ducted supply-and-exhaust mechanical ventilation** is framed as worth the added cost mainly in specific situations — e.g. an apartment on a loud arterial road where windows realistically can't be opened for fresh air.
- The practical recommendation: default to breathers unless there's a specific reason (noise, air quality, a strong personal preference) pushing toward a full system, since most people reportedly don't perceive a meaningful difference in day-to-day comfort.

### Terminology, Full Device Taxonomy, and Buying Guide (added 2026-08-24, Round 3, podcast interview with Pavel Goncharov/BRIX-ATMEX)

Pavel Goncharov (founder, BRIX; owner, ATMEX/Air Nani) explains: **"breather" (бризер) was originally a Tion product name (2013's Tion O2) that became a genericized category term** — a breather is a subset of the broader "supply complex" category (every breather is a supply complex; not every supply complex markets itself as a "breather"). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

**Full ascending taxonomy of ventilation options**, each with its own real limitation:

1. **Open window** — no filtration, no control, and — see the "bottle-cap" mechanism below — often not even reliable airflow.
2. **In-profile trickle vent** — basic foam filter (barely stops dust), no heating, mostly a paper-compliance checkbox for developers.
3. **Wall-mounted trickle vent/valve** (100-130mm insulated bore, adjustable damper) — **⚠️ doesn't work at all if the building's exhaust ventilation is weak/absent** (no pressure differential to pull air through); no heating; **a poorly-designed unit lets cold air drop straight to floor level (draft-on-the-feet), while a well-designed one routes incoming air upward first so it warms in transit** — a concrete design-quality checkpoint.
4. **Compact heat-recovery unit (рекуператор)** — cyclic "inhale-exhale" operation (roughly 1-minute cycles, a heat-storage element captures outgoing warmth and returns it to incoming air) — **halves effective average throughput** versus continuous flow; needs 1-2 wall penetrations; **redundant if the apartment already has working separate exhaust ventilation** (duplicates an exhaust function it doesn't need to provide). No compact device does simultaneous non-cyclic bidirectional recovery — that needs a large cross-flow exchanger only feasible at central-system scale.
5. **Breathers / supply complexes** — single penetration, continuous one-directional forced supply; base tier (physical buttons, coarse filtration, noisier) vs. premium tier (CO2-sensor automation, app/smart-home integration, quieter, multi-stage filtration).
6. **Central ducted supply+exhaust system** — see existing content below; unambiguous top performer except on price/disruption.

**⚠️ "Bottle-cap" mechanism — why an open window sometimes moves zero air**: without forced supply and with weak/absent exhaust ventilation, opening a window can produce no felt airflow at all, the same way a capped bottle with one small hole won't drip — there's nothing pulling air in to replace what would leave. Real client cases cited of standing directly at a fully-open window and feeling nothing. This is why supply and exhaust ventilation are a coupled problem, not independent ones. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

**⚠️ Common misconception corrected: an air conditioner provides zero fresh-air exchange** — it only recirculates and thermally conditions air already in the room. A real case: a client believed her 2-year-old AC was "ventilating" the apartment; what had actually changed was a previously-leaky window seal getting fixed — the AC just recirculated faster, which felt similar but supplied none of real ventilation's air-exchange benefit. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### CO2, Air Quality, and Sizing

- **⚠️ CO2 buildup impairs cognition mainly by blocking oxygen transfer from blood to tissue, not by depleting room oxygen** — even heavy breathing barely lowers room oxygen, but elevated CO2 suppresses respiratory drive and interferes with oxygen delivery to tissue (including the brain), producing real fatigue/brain-fog. **Cited thresholds** (attributed to an unnamed American cognition study, `unverified`): 1,000+ ppm → 15% cognitive-function decline; 1,400+ ppm → 50% decline. **A 15-minute pre-bed window-airing is not adequate** — CO2 rebuilds to an unsafe level within about an hour. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **Airflow sizing benchmark, cited to ГОСТ/СНиП code: 30 m³/h of supply air per person** — size with margin (65-70 m³/h for two people, not exactly 60). Even a mid-range breather's lowest/second speed setting already exceeds a typical 15-minute window-airing session's air exchange. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **CO2-sensor-driven automatic control is the single most valuable feature-tier upgrade** — the device infers occupancy from exhaled CO2 and self-adjusts airflow without manual management. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **Myth-check: summer doesn't reduce the need for forced ventilation — the opposite.** Natural stack-effect draft is driven by the indoor-outdoor temperature differential, strong in winter and weak in summer — a breather is often *more* necessary in summer than commonly assumed. A breather is also valuable in shoulder seasons (autumn/spring) when building heating isn't on yet but outdoor air already needs conditioning. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Filtration, Heating, and Humidification

- **Three-stage filtration**: coarse pre-filter (fine mesh/washable foam, catches insects/debris, wash ~every 3 months — commonly skipped since accessing it needs 4 screws); HEPA-class filter (**H11 or H13 recommended** for residential use — sufficient for pollen and PM2.5); odor-control stage (activated carbon, needs replacement, or a photocatalytic filter — no replacement needed, ~5-year rated life). **PM2.5** = particulates ≤2.5μm, small enough to cross lung barriers into the bloodstream — `unverified` as medical claim, record the mechanism only. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **Heating is the feature that separates a climate-appropriate device from an imported one that struggles in Russia's winters** — cited example: Xiaomi's breather-category heating elements are described as too weak for real cold snaps, and its units are separately flagged for poor insulation/thermal bridging causing winter condensation — `single-account`, self-interested competitor comparison, recorded but treated skeptically. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **⚠️ Winter outdoor air has very low *absolute* humidity regardless of a forecast's *relative*-humidity percentage** (cold air holds far less total moisture at the same relative %) — warmed winter air brought indoors via any ventilation path is genuinely dry, and a **breather dries indoor air far more than a window did, purely due to its much higher throughput volume**. **Sizing rule: pair active ventilation with a humidifier rated ≥300 ml/hour** (roughly 3L/10hrs of ventilated occupancy in winter; should run near-continuously in winter). For a private house, a centralized nozzle/misting system is recommended over per-room units but must be planned at the design stage (not retrofittable) and is expensive; for an apartment, an ordinary ultrasonic humidifier or air washer, refilled daily or every 2 days, is sufficient. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Noise, Buying, and Bedroom Priority

- **⚠️ Continuous/steady noise (a running breather) is subjectively far less sleep-disruptive than intermittent noise at a comparable dB level** (traffic, a motorcycle) — the ear habituates to a constant tone but keeps re-triggering on irregular sounds; source explicitly caveats this as personal framing, not research he's reviewed himself. **Buying tip: compare a candidate unit's noise rating against a device you already tolerate (e.g. your own AC), or request a free in-home demo** — this source's own company sends an engineer to bring a unit into the actual room and let the buyer listen from the sleeping position, lights off, before purchase. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **If only one unit is affordable, prioritize the bedroom over kitchen/living room** — a single unit cannot serve a multi-room apartment (one per room needed), but starting with the bedroom and expanding later is reasonable; pre-wire power outlets in candidate future-unit locations during renovation regardless of initial budget. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Installation Practicalities and Common Mistakes

- Can be installed at **any renovation stage** (unlike a central system, which must be planned early) — only needs nearby power (ideally a hard-wired feed run during finishing so no visible cord remains). Typical install: **~2 hours**, **132mm bore** via water-cooled diamond core drilling with contained/vacuumed debris. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **⚠️ Common installer mistakes**: skipping duct-sleeve insulation (causes condensation around the bore); boring interior/exterior openings non-coaxially (silently obstructs part of the duct cross-section); installing too close to a wall/corner; damaging exterior cladding/tile during the exterior bore; miswiring the electrical feed, forcing re-chasing of already-painted walls. **⚠️ Genuinely new technique: angle the exterior bore with a slight downward slope toward the outside (a couple of degrees)**, not level — so any snow/rain entering the sleeve drains back out rather than pooling in the wall cavity. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **⚠️ Window-reveal routing mechanism, extending this page's existing one-line note above (`f7ab173e`)**: the device still sits in the wall cavity between window and wall as usual — the bore does *not* penetrate the exterior facade skin; instead an L-shaped duct routes the airflow sideways within the wall cavity out to the window reveal space (~20cm deep behind cladding on a business-class ventilated-facade building), with the exterior grille fitted flush into the reveal and painted to match — essentially invisible from the street. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]
- **Facade-modification pushback from a management company/developer is rare** (only 1-2 cases company-wide since 2017, resolved with a discreet cap or matching paint). **Named developer PIK is flagged as stricter than average**, with this source's company keeping pre-approved technical paperwork on file specifically for PIK buildings. A custom double-glazed pane with a built-in bore is a fallback for floor-to-ceiling glazing with no wall cavity at all. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Pricing Tiers (size × budget matrix, Russia-market, round/approximate figures)

Pavel Goncharov (BRIX/ATMEX): apartment ≤80m², minimal budget → breather, **~30,000 RUB or less**; apartment >80m², minimal budget → central supply-only system, electric heating (no recovery), **~300,000 RUB** cited as a decent block; private house, minimal budget → still a central heat-recovery unit (cheapest available), since electric-only heating would be too costly to run for a whole house; ≤80m², comfort tier → a better-tier breather (price step "not large"); >80m², comfort tier → central system *with* heat recovery; house, comfort tier → central heat-recovery, optionally add humidification; unlimited budget, any size → central ducted supply+exhaust, heat recovery, centralized control, max CO2 sensors, **per-room individually-addressable dampers** ("the Maybach and Rolls-Royce" of ventilation) — **flagged by the interviewer: per-room dampers are individually expensive enough to raise a real payback-period question even on an unlimited budget.** Budget for designer exterior grilles regardless of tier — genuinely expensive. **Running cost**: ~350-600 RUB/month per unit in central Russia (scales roughly linearly, 3 units ≈ 1,000-2,000 RUB/month) for morning/evening/overnight use. **Annual filter cost**: from ~3,000 RUB (coarse pre-filter, though it's washable not replaced) — upper bound `ASR-uncertain`/not recoverable from this transcript. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Named Device Recommendations (self-interested — recorded with that flag)

Pavel Goncharov's own stated top-3, explicitly disclosing his own conflict of interest before naming his own product: **Air Nani A7 Forever** (his own company — cites a never-replace photocatalytic odor filter and built-in humidification as unmatched differentiators); **Tion 4S** (competitor — simple, quiet, long-established); **Ballu ASP100** (competitor, large HVAC conglomerate — praised for compact/attractive design fitting narrow wall segments, not the quietest). Read the self-endorsement skeptically per this project's tier-steering filter; the two competitor mentions are recorded at face value as a market-reference point. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov|uiiggEC7c9M]]]

### Breather Price Ladder with Named Brands (added 2026-08-24, Round 4)

Konstantin Kruglov/Ontario gives a fuller three-tier breather ("бризер") price ladder than this
page's existing minimal-budget figure, with named brands per tier, Russia-market:

- **Economy: 15,000–30,000 RUB ≈ $180–$370** (2025-10-10 exact-date rate) — Эра ("Era", described
  as "super-economy"), Балу (Ballu), Вакио (Vakio), Зилан.
- **Comfort: 35,000–50,000 RUB ≈ $430–$610** — Tion's "О2" and "Лайт (Light)" lines, Blauberg (not
  officially supplied to Russia — parallel-import only), Xiaomi (flagged here for lacking Russian
  service centers — a different caveat than this page's existing "heating too weak" claim about
  the same brand), Royal Clima, Бреза (Breza), Зигения (Zigenia)/Аэропак (Aeropak), iFresh.
- **Premium: 60,000–90,000 RUB ≈ $740–$1,100** — Mitsubishi, Tion 4S, Biox, Air Nani.

**⚠️ Mitsubishi's premium breather needs two wall penetrations, not the usual single bore** — it
has its own built-in exhaust function (most breathers are supply-only), so a real bidirectional
duct requires two separate bores. `single-account`, `unverified`.

**⚠️ Improper installation (poor exterior-bore sealing, non-professional drilling) can void the
manufacturer's warranty outright** — a concrete consequence attached to this page's existing
"use professional installers" guidance. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wowlXrlGrEc_kruglov_breather_purifier_humidifier|wowlXrlGrEc]]]

### Second Independent Confirmation of Bore Size and Drainage-Slope Technique (added 2026-08-24, Sidorik Round 4)

Pavel Sidorik, individual practitioner, own apartment, installing 3 reused/new Tion 3S breather units: independently confirms, from an unrelated channel and installer, two specific numbers already recorded on this page from the Kruglov/Ontario podcast source — **132mm bore diameter**, and the **angled exterior bore (sloped downward toward the outside) so rainwater drains back out rather than pooling in the wall cavity**, with the exterior grille fitted at a matching angle for the same reason. Also independently matches the existing 3-stage filtration structure (foam pre-filter → carbon → HEPA) and the existing "AC does not ventilate" mechanism note below. Genuinely new detail not yet on this page: a live demonstration that opening two windows on opposite sides of a dual-aspect apartment (not just one) produces strong enough cross-draft turbulence to make a room physically uncomfortable to stand in — a concrete illustration of why "just open a window" isn't a real substitute for forced ventilation in a high-rise. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_C-3BcpXDRnk_sidorik_ventilation_ac_ep19|C-3BcpXDRnk]]]

## Separate-Zone Exhaust Ventilation for Two Rooms Sharing One Building Channel (added 2026-08-24, Sidorik Round 4)

Pavel Sidorik, individual practitioner, own apartment, Belarus (level 1, via a spoken 75-BYN price): a common new-build configuration is **one shared exhaust-ventilation channel physically located in only one of two adjoining wet rooms** (his case: the toilet room has the channel, the bathroom doesn't). The developer's own default fix — a flat duct with holes cut mid-run so both rooms feed into the same channel — **does not work at all**: when the room fan nearer the channel is off, air reverses through the mid-run holes and pushes the other room's humid/odorous air back into the room instead of extracting it.

**⚠️ A simpler two-independent-fans-plus-T-junction design also fails, and a channel fan with fully separated ducts is required instead**: even two separate room fans feeding one shared duct via a T-junction still let air currents mix between rooms whenever only one fan is running, since the inactive branch offers a path for air to migrate backward. The fix is a single **ducted/channel fan serving both rooms through two completely separate, individually dedicated duct runs** (not a shared junction) into a distribution box, which then feeds the one available building exhaust channel — keeping both rooms' air streams genuinely isolated from each other while still using the single shared channel.

**Named product**: S&P TD-EVO-VAR duct/channel fan — low-profile, quiet via rubber vibration-isolating mounts, supports continuous minimum-speed running with a timed step-down after a manual speed-boost switch is released, and accepts an external air-quality sensor via 0-10V analog input. **Distribution box** can be a custom sheet-metal box (commissioned from a metalworker) or self-built far more cheaply from flat plastic duct sections using a heat gun. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_zkM_gea0XVE_sidorik_bathroom_toilet_ventilation|zkM_gea0XVE]]]

**Clarification from a later video in the same series**: the custom 90°-turn duct fitting shown for this build connects to the practitioner's own private "booster"/"accelerator" vent channel serving only his own toilet room, which then joins the shared building vent channel downstream — not a direct modification of the shared channel itself, addressing viewer criticism that the build blocked neighbors' ventilation. The fitting itself was fabricated by fusing flat plastic duct sections together with a hot-melt glue gun (used here as a plastic-welding technique, not just an adhesive). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_zaW8XagX72U_sidorik_hot_glue_lifehacks|zaW8XagX72U]]]

## Masonry Vent-Duct Sizing for a Wet Room (added 2026-08-25)

Architect Vitaliy Zlobin (independent country-house architect, `single-account`, region unresolved) gives a concrete masonry vent-shaft sizing rule for a bathroom/WC/shower room, distinct from this page's mostly apartment-scale mechanical-system content above:

- **A 140×140mm brick vent-duct opening is sufficient for a wet room up to 10m²** — sized to brick-coursing modularity rather than an arbitrary round number, so it's buildable within a standard masonry wall without odd partial courses.
- **Duct air-intake height convention for a 3m ceiling: ~270cm** — set below the dropped-ceiling void specifically to leave room above for recessed downlights and other services; can be raised, but only if the intake's own path through the ceiling void to the duct opening is separately worked out.
- **The duct must always terminate at the roof, never mid-building**, specifically for reliable odor removal — applies whether the shaft itself is masonry or, in a non-masonry building, a fabricated panel duct.
- **An electric booster fan mounted in the duct is explicitly odor-removal assistance only, not a substitute for real forced ventilation** — the source states it "probably can" function as forced ventilation but will be underpowered for that job; don't rely on a duct-mounted booster alone where genuine mechanical exhaust capacity is actually needed. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_DcWsQMiMcak_zlobin_wc_bath_theory_pt1|DcWsQMiMcak]]]

## Kitchen Extraction Hoods Share the Same Shaft-Capacity Ceiling

The same shared-shaft constraint that governs fresh-air ventilation applies just as strongly to a kitchen range hood set to extraction mode ("отвод") — a mechanism worth stating explicitly since it's easy to assume a hood's own motor rating determines its real performance. **This is corroborated across 5 independent sources** — full multi-source breakdown, including a direct conflict this raises with the kitchen's already-selected hood model, lives in [[15_Appliances/analysis/Kitchen_Hood_Analysis|Kitchen Hood Analysis]]. Summary:

Roman Che TV, Мебель — это просто, ЛенРемонт, and Argus report: **a hood vented into a shared apartment-building ventilation shaft cannot move air faster than the shaft/duct itself allows**, regardless of the hood's own rated m³/h — the shaft, not the hood, is the actual bottleneck.
Roman Che TV, Мебель — это просто, ЛенРемонт, and Argus report: **an oversized hood on an undersized duct doesn't yield more airflow — it causes more noise and can force draft reversal**, potentially pushing air backward into a neighboring apartment's line.
Roman Che TV, Мебель — это просто, ЛенРемонт, and Argus report: **no hood works without makeup air ("приток")** — if a kitchen has no dedicated fresh-air supply, a window needs cracking for real extraction to occur at all.
Roman Che TV, Мебель — это просто, ЛенРемонт, and Argus report: **the practical alternative in a constrained-venting apartment is recirculation mode** (carbon-filtered, air returned to the room) — functionally reliable regardless of shaft capacity, though it doesn't remove humidity and needs a periodic filter.
Zemstandart/Alexey Zemskov advises: **a tee-fitting-plus-check-valve setup can preserve natural kitchen ventilation alongside a ducted hood**, independently described by three unrelated sources — see [[15_Appliances/analysis/Kitchen_Hood_Analysis|Kitchen Hood Analysis]] for the DIY detail and the unresolved Russia-specific regulatory question this area also touches.

## Supply Ventilation Design & Ducting

`single-account`, one practitioner's stated standing rule.

Zemstandart/Alexey Zemskov recommends: **supply-air ("приточка") ventilation must be designed only by a specialized ventilation contractor**, never a general contractor, architect, or interior designer. Stated sequence: the general design project is completed first, marked only "supply," "supply+exhaust," or "ducted system" as a placeholder; the ventilation contractor then visits, measures, and produces the actual duct/routing design; the general project is updated to add the required electrical feed/breakers; boxing/drywall to conceal ducts is finalized last, after the ventilation design is locked. [source: `_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]

Zemstandart/Alexey Zemskov reports: **round-section ducts are preferred over flat/rectangular for lower noise.** Flat ducts are reserved for minimizing ceiling drop specifically; a technique for avoiding a full-room ceiling drop while still using round ducts is to route the supply duct above the kitchen cabinets and box it behind a floor-to-ceiling kitchen facade, rather than dropping the whole room's ceiling to the duct's lowest point — cited as recovering roughly 12–15 cm of ceiling height. [source: `_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]

Zemstandart/Alexey Zemskov reports: **a breather can be vented through a window reveal/embrasure instead of an exterior wall**, as a workaround where facade penetrations are banned by the building — the intake/exhaust opening is cut into the window's reveal rather than the wall itself. [source: `_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]

## Exhaust-Duct Concealment in a Hallway

Zemstandart / Alexey Zemskov reports `single-account`, `ASR-uncertain` — this source's transcript is unusually garbled even though flagged as manually-captioned; treat the specific numbers below with more caution than this page's other figures. A bulky developer-installed exhaust-duct box can be replaced with a smaller-cross-section duct — bathroom/toilet exhaust routed via a forced/booster fan through a round-to-flat adapter into the hallway and building shaft, junction pulled tight to the ceiling for noise, all concealed behind a stretch ceiling. Reported total ceiling-height loss ~10 cm, of which roughly 6 cm is attributed to the developer's own pre-existing duct routing (not this technique) and ~4 cm to the technique itself — the specific cm split is uncertain, but the qualitative point (net added loss is small, most hallways tolerate it well) is better supported. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_HX2pDdILM7U_hidden_exhaust_duct_concealment|extraction note]]]

## Kitchen Exhaust Duct Sizing, Ceiling Drop & Soundproofing

`single-account`, cleanly-transcribed (unlike the exhaust-concealment entry above).

Zemstandart / Zemproekt says **duct cross-section trades off noise against ceiling drop, and "bigger" isn't the same as "quieter"**: a duct box needs to be *thick*, not just *wide*, to cut noise — a wide-but-thin box lowers the ceiling more without the expected noise benefit. Standard cross-section for most systems is **55×110 mm**; a powerful exhaust hood run through that standard size will be very noisy and instead needs a **250×55 mm** cross-section. Duct *length* is a separate noise driver — a longer run from the forced-exhaust point to the shaft (one real project cited ~4 m) increases noise independent of cross-section.

Zemstandart / Zemproekt says **ceiling drop is typically ~40 mm more than the duct box's own thickness** — the extra allowance is for electrical cable conduit routed alongside/above the duct in the same concealed space. This must be pre-calculated in the design project so the actual finished ceiling height isn't a surprise after the renovation is done.

Zemstandart / Zemproekt recommends **always adding self-adhesive duct soundproofing regardless of the box's own thickness** — a duct is never fully soundproof on its own. Spec: self-adhesive, minimum 3 mm thick.

Zemstandart / Zemproekt (technical content presented by Sergey Saratov) says **a design project should document every ventilation exhaust point (forced and natural)** explicitly, so the client can verify contractors' work against the plan during the renovation. This is also the source of the tee-fitting-plus-check-valve technique's independent corroboration cited above (Zemstandart, 2026-08-10). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_ZqfaeREBEYQ_kitchen_ventilation_mistakes|extraction note]]]

## Real Long-Term Failure Case: Tiling Over a Ventilation-Valve Access Point (added 2026-08-24, Petrishin-Stroi Round 9)

Sergey Petrishin's company gives a genuinely rare **6-years-later revisit
case study** — returning to a client's own apartment to fix a defect
from the original renovation, rather than a same-project acceptance
checklist. **⚠️ Never permanently conceal a shared ventilation-system
valve behind tile/finish with no inspection access** — this apartment's
original renovation built a flat, visually flawless tiled wall directly
over a set of shared-ventilation valves, with no access hatch left. The
defect stayed invisible for 6 years until a *new downstairs neighbor*
raised a critical complaint about blocked ventilation traceable to this
concealed valve — the concealment was a **shared-building-system risk**,
not just a private inconvenience for the apartment's own owner.

**Notable finding: a management-company technical-project sign-off is
not a reliable catch for this kind of defect.** The client states every
apartment in this development had its water-supply/sewage/ventilation
technical projects formally reviewed and approved by the building's
management company, both before and after each renovation — this defect
still passed that review; the company's own explanation was "человеческий
фактор" (human error), framed as a real, always-present risk rather than
an excuse.

**Practical repair note**: fixing this kind of concealed-access defect
means removing the finish covering the valve, then re-finishing —
original matching material may no longer be available years later,
forcing a real (if temporary) design compromise (this case: dark
leftover tile used in place of the original light tile, with an explicit
plan to swap back once matching material is sourced). `single-account`,
heavily ASR-garbled transcript — treat with appropriate caution. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_nhJI_yGjfRU_petrishin_ventilation_6years_later|nhJI_yGjfRU_petrishin_ventilation_6years_later]]]
