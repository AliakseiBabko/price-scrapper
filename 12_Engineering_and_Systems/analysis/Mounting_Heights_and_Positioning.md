# Electrical — Mounting Heights & Positioning Standards

A repeated on-camera demonstration (four people, heights 150–185 cm) found that the resting hand-drop height from standing is essentially constant across adults — the basis for treating switch height as a fixed constant rather than something to scale per-occupant. Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

- **Switches: 90 cm from finished floor** (95 cm as a variant for unusually tall households), **switch center 15 cm from the rough door-opening edge** — moving it to 10 cm was shown causing the switch to conflict with door casing once installed. **Independently restated in two further sources (added 2026-08-18)**, one of which names it explicitly as "the Zems standard" — same 90cm/15cm figures, now corroborated across at least four separate videos from this channel. [source: [[_Sources/YT_uLJGsTfTj3A_switch_outlet_mounting_heights|uLJGsTfTj3A_switch_outle]]]
- **Bedside points scale off furniture, not a fixed number**: bedside lamp switch ~120 cm if headboard-mounted, or ~70 cm if nightstand-mounted; bedside outlets ~70 cm; an over-bed pendant/lamp cable drop at ~100 cm. Horizontal position is set by a formula combining false-wall offset + curtain-zone clearance + nightstand width + half the bed's width. [source: [[_Sources/YT_VK8rCdChdbY_bedside_outlet_placement|VK8rCdChdbY_bedside_outl]]]
- **Countertop outlets: 110 cm from finished floor by default**, shifting by the same delta as the countertop height when a non-standard countertop is planned (e.g. +10 cm countertop → +10 cm outlets). Window-slope and ceiling-referenced points are the explicit exceptions — see [[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Cable, Circuits & Panel Design]] for the documentation convention. [source: [[_Sources/YT_l_rjjPlPkRo_switch_height_offset_rules|l_rjjPlPkRo_switch_heigh]]]
- **A small set of point types should track occupant eye level instead of a fixed height**: video-intercom monitors and underfloor-heating thermostats, both read visually while standing/using them — unlike switches, which are operated by feel, not sight. [source: [[_Sources/YT_uLJGsTfTj3A_switch_outlet_mounting_heights|uLJGsTfTj3A_switch_outle]]]

## Kitchen Heights Referenced to the Cabinetry, Not the Floor Plane (added 2026-08-31)

Everything above is measured from finished floor. This set is different: the constraint comes from the carcass, so the figures cannot be transferred between kitchens without checking the drawing. All from interior designer Надежда Кузина. [source: [[_Sources/YT_iHViNm3dESU_kuzina_kitchen_electrics_and_lighting|YT_iHViNm3dESU]]]

- **⚠️ Minimum 250 mm from floor for an outlet inside a sink base — stated as a correction to her own error.** She specified **200 mm** for a waste-disposer outlet, having fitted disposer, filter and bin into a single base under 90 cm wide, and had not accounted for the **internal stiffener rail** that holds a sink base's shape. The outlet collided with it and a cut-out had to be improvised on site. Worth more than a generic warning because the mechanism is named and the failure is her own.
- **⚠️ The 10 cm plinth trap, with the arithmetic.** Plinth («цоколь») height runs **10–15 cm**. An outlet in a 10 cm plinth leaves roughly **1 cm of clearance** once the mounting box's own half-height is taken — and outlets go in **before the finish floor is poured**, so builder tolerance plus actual floor level can consume that centimetre entirely and the faceplate then will not fit. **If the plinth is known to be 15 cm, raise the outlets rather than defaulting to the 10 cm assumption.**
- **Freestanding freezer: 25 cm** behind it, or in the plinth. Unlike a fridge it stands on the floor rather than on a shelf, so an outlet directly behind may not sit flush once the plug is in — and several manuals forbid an outlet inside the appliance's own footprint outright.
- **Built-in fridge is the easy case**: standard mounting puts it on a shelf, clear of the floor, so an outlet in the same base or in the plinth is unproblematic and there is no need to displace it to a neighbouring base.
- **The dimensional chain these hang off**: plinth 10–15 cm → base height → backsplash. **Worktop height is a function of the user's height, not a constant** — serial production defaults to **815–820 mm**; for a person of ~1.80 m she puts it **above 90 cm, with ~94 cm comfortable**; **95 cm** for the very tall. A joinery shop will build to any height, which is precisely why the outlet heights cannot be assumed.

## Perspectives — Countertop Outlet Height: 110 cm vs 100 cm (added 2026-08-31)

Two named practitioners give different default heights for a kitchen worktop outlet, and they are arguing from **different disciplines**, which is what makes this worth recording rather than averaging.

| Source | Position | Stated reasoning |
| :--- | :--- | :--- |
| Zemskov/Zemstandart-lineage electrical source (`l_rjjPlPkRo`) | **110 cm** from finished floor by default, shifting by the same delta as a non-standard countertop height | An installation standard, expressed as a rule that tracks countertop height so the relationship to the work surface stays constant |
| Надежда Кузина, interior designer (`iHViNm3dESU`) | **100 cm** from finished floor, on an 82 cm base height | Compositional. At **130 cm** the outlet lands in the **middle of the backsplash** and looks bad; sitting it near the **lower edge** of the backsplash reads far better. She explicitly rejects the usual argument for 110 cm+ — that it clears the «уголок» trim strip over the worktop/backsplash joint — because not every kitchen has that strip and where it exists it may be 1 cm rather than 5 cm. She calls that argument "нерациональный" |

**Common Ground.** Neither treats the number as a code requirement, and Кузина's own search of ГОСТ/СНиП found nothing governing outlet *position* at all (see the RU-jurisdiction note under Kitchen Utilities). Both also agree the figure is **derived, not absolute**: it moves with the countertop height. The real disagreement is over which reference the outlet should hold constant — its distance above the worktop, or its position within the visible backsplash field.

**Deciding factor both point to**: the backsplash height and whether a joint trim strip is being used. Where the backsplash is tall and untrimmed, Кузина's lower-edge logic dominates; where a substantial trim strip exists, the 110 cm figure has something concrete to clear.

> [!IMPORTANT]
> **This is decided by the кухня drawing, not by this page.** With a glass backsplash («скинали») the cut-outs are fabricated into the glass and **nothing can be moved afterwards** — so the number must be fixed against the actual elevation before the glass is ordered.

**Your Priority: not yet decided.** No kitchen elevation exists for this apartment yet, so the deciding factor above cannot be applied.

## The Zero-Reference / Working-Reference System All These Heights Are Measured From (added 2026-08-19)

> [!NOTE]
> Every "from finished floor" figure on this page (and every stub-out coordinate on [[12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates|Fixture Stub-Out Coordinates]]) is ultimately taken from this reference system on a real jobsite — previously implicit in this vault's sources, explained end-to-end for the first time here. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|note]]]

- **"Zero reference" = the finished common-corridor floor level outside the apartment's front door** — not an arbitrary site-chosen point (the construction/geodesy meaning of the same term). Every apartment measurement is ultimately taken from the screed plane beneath it, so anchoring zero to that plane avoids compounding conversion errors across every single measurement on a project. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|VHfUDBr0p4Q_door_height_]]]
- **"Working reference" = a virtual plane exactly 1000mm above zero**, marked with a laser level at chest/eye height on every wall *and* every non-plasterable surface (window/door reveals, pipe risers, ventilation shafts — a mark left only on a soon-to-be-plastered wall is later lost). In practice this working reference, not zero itself, is what nearly all on-site layout is actually measured from — zero is often never physically marked at all. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|VHfUDBr0p4Q_door_height_]]]
- **Why exactly 1000mm**: makes reference-system arithmetic trivial for any tradesperson (e.g. "25cm above zero" = "75cm below working reference," no calculator needed) — an explicit error-reduction design choice, not an arbitrary convenient height. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|VHfUDBr0p4Q_door_height_]]]
- **Practical marking procedure**: set a laser's horizontal beam to 99cm above the corridor's *finished* floor (99cm, not 100cm, because the corridor's own ~1cm finish layer is already down — the beam ends up exactly 1m above the rough screed beneath it); transfer that plane around the apartment by marker; every height figure elsewhere in this vault (switch heights, stub-out coordinates, door-opening heights) is derived by measuring down from that mark, not up from an as-yet-unpoured screed. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|VHfUDBr0p4Q_door_height_]]]
- **When the corridor floor isn't finished yet**: do not use the developer-installed entrance door's bottom edge as a zero proxy (installers set that position with no regard for future corridor floor level). **Correct substitute: the building elevator's own threshold height** — deliberately set by developers so a stroller/wheeled cart crosses without a bump. [source: [[_Sources/YT_VHfUDBr0p4Q_door_height_zero_reference_109|VHfUDBr0p4Q_door_height_]]]

## ⚠️⚠️ Never a Socket Where the Appliance Itself Blocks Access to It — One Principle, Three Instances (Александр Синчуков, 2021-01-27)

**Three hard first-fix consequences, all invisible until it is too late:**

1. **⚠️⚠️ A DISHWASHER REACHES THE BACK WALL: «это такой ГЛУБОКИЙ предмет, который прям ВПРИТИРКУ с задней стеной проходит, и за ней ПРАКТИЧЕСКИ НЕВОЗМОЖНО НИЧЕГО ПРОТЯНУТЬ. Если у вас например МОНОЛИТНАЯ СТЕНА, то вы НЕ СМОЖЕТЕ за ней протянуть ВОДУ — это нужно учитывать ПРИ ПРОЕКТИРОВАНИИ.»**
2. **⚠️ NEVER A SOCKET BEHIND THE DISHWASHER: «ни в коем случае нельзя проектировать розетку, потому что вы просто НЕ СМОЖЕТЕ ВОТКНУТЬ ТУДА ПРОВОД.»**
3. **⚠️ NOR BEHIND THE FRIDGE, for the de-energising reason: «если вам нужно будет его ОБЕСТОЧИТЬ, вам придётся его ВЫНИМАТЬ — если отдельностоящий, его нужно ВЫДЁРГИВАТЬ ИЗ НИШИ; если встроенный, это вообще ЦЕЛАЯ ИСТОРИЯ.»**
   - **⚠️ AND THE PRACTICAL FIX IS NAMED: «просто в СОСЕДНЕЙ СЕКЦИИ сделайте розетку… нужно — просто СКИНЕТЕ ЦОКОЛЬ и вынете розеточку.»**

- → **⚠️⚠️ ONE PRINCIPLE BEHIND ALL THREE: NEVER PLACE A SOCKET OR A SERVICE RUN WHERE THE APPLIANCE ITSELF BLOCKS ACCESS TO IT. Put it in the NEIGHBOURING cabinet, reachable by removing the PLINTH.** *(The single-principle reading is mine; he gives the three cases.)*
- → **It interacts directly with Round 6's factory finding that in-cabinet socket cut-outs are pre-cut at the works — so this decision has to be right before furniture production, not before first fix.**

## ⚠️⚠️ Perspectives — A Designer Attacks the 30/90 Socket-Height Orthodoxy, With Its Provenance

**«Существуют СТАНДАРТНЫЕ ВЫСОТЫ розеток — это идёт ещё с 90-х годов, когда существовал этот "ЕВРОРЕМОНТ", который я просто НЕНАВИЖУ: все розетки на высоте 30 САНТИМЕТРОВ, все выключатели на 90. Но эти размеры идут из СОВЕТСКИХ СНИПОВ и обусловлены теми законами, которые были ещё в 40-е, 50-е и 60-е годы. Сейчас совсем другое время, совсем другая эстетика… Поэтому ставьте розетки на РАЗУМНОЙ высоте — это НЕ БУДЕТ влиять на БЕЗОПАСНОСТЬ, потому что всё равно расстояние будет.»** He particularly objects to sockets high on the splashback: **«смотрится совершенно отвратительно… смотрят на вас прямо из центра фартука».**

- **⚠️ AND HIS SOLUTION: sockets recessed into the UNDERSIDE of the wall cabinets — «розетка вставляется в НИЗ ВЕРХНЕГО ЯЩИКА, и вы их ВООБЩЕ НЕ БУДЕТЕ ВИДЕТЬ, но будете просто втыкать [что нужно] ВВЕРХ.»**
- → **⚠️⚠️ ROUTED AS PERSPECTIVES, WITH THE SAFETY ASSERTION FLAGGED. This is a DESIGNER arguing against a convention this page holds as standard, on AESTHETIC grounds, while asserting that safety is unaffected — and that assertion is an opinion, not a safety analysis. The PROVENANCE argument (the heights are inherited from mid-century norms rather than derived from current practice) is legitimate and worth having; the safety conclusion is not evidence.**
- → **⚠️⚠️ JURISDICTION: this is a RUSSIAN practitioner discussing SOVIET СНиПы. Per the standing rule it is recorded here, on a technical page, with the jurisdiction flagged — NOT in `16_Legal_and_Regulations/`, which is Belarus-only. It is a design-practice argument, not a regulatory statement, and nothing here establishes what any Belarusian norm requires.**

## ⚠️⚠️ Socket Positions Must Be Reconciled With the Kitchen Maker's ТЗ — the Designer's Side of a Round 6 Finding

**«Это очень частый вопрос, который всплывает ИМЕННО НА СТРОЙКЕ, во время АВТОРСКОГО НАДЗОРА: дизайнерские ПРИВЯЗКИ РОЗЕТОК обязательно нужно УТОЧНЯТЬ В СООТВЕТСТВИИ С ТЕХНИЧЕСКИМ ЗАДАНИЕМ ОТ ПОСТАВЩИКА КУХОНЬ — потому что когда дизайн-проект попадает [на] производство, у них там СВОИ МОДУЛИ, своё оборудование, СВОИ ТИПОВЫЕ РАЗМЕРЫ, и привязки могут… ДАЖЕ СИЛЬНО ПОЕХАТЬ.»**

- → **⚠️⚠️ Round 6's factory source established that the first-fix electrical plan and the furniture order are effectively ONE DEADLINE, because socket cut-outs and lighting grooves are CNC operations. THIS IS THE SAME FINDING FROM THE DESIGNER'S SIDE, two years earlier — and it names WHERE the problem surfaces (авторский надзор, on site) and WHY (the factory's MODULE GRID overrides the designer's dimensions). Two sources, two sides, one deadline.**

[source: [[_Sources/YT_wvlr2aGDMCc_nsdsgn_five_kitchen_mistakes|YT_wvlr2aGDMCc]]]

