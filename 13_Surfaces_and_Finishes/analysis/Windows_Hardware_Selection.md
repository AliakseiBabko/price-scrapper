# Windows — Hardware Selection

Part of [[13_Surfaces_and_Finishes/Windows|Windows]].

## Tilt-and-Turn vs. Turn-Only

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) recommends: **Tilt-and-turn is unambiguously the better default over turn-only, all else equal** — the cost premium is small (~1-2% of total window cost), negligible against the functional gains. Three advantages:

1. **Avoids needing a hard fall-limiter/restrictor**: a turn-only sash swings fully open with no other restraint, requiring a child-safety stop as an added part/failure point.
2. **Trickle/slot ventilation**: turn-only sashes are only fully open (losing heat/security) or fully closed — tilt-and-turn's tilt position gives a small continuous perimeter gap for fresh air without opening the sash.
3. **Durability/self-weight mechanism for large sashes — the main point**: a large, heavy sash operated by full swing-open turning bears its own weight on the side hinges every time it opens, gradually deforming/sagging (adjustment screws compensate only temporarily). **A large sash (worked example: ~2m×2m, near-square) can't be split into a narrower vertical pair** for facade-appearance/code reasons — a heavy near-square sash operated fully-open reportedly deforms within about a week of regular use to the point it can't close properly. **Fix: restrict a large/heavy sash to tilt-only operation** (occasional use, e.g. cleaning) — tilting transfers the sash's weight onto the bottom frame/transom instead of the side hinges, avoiding the deformation mechanism entirely.

## Panoramic-Window Safety Hardware

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) explains: **The problem**: standard safety-code parapet height (~1.1m) conflicts directly with a panoramic-window design goal — at that height, someone seated sees mostly the opaque parapet and only a strip of sky, not the view a floor-to-ceiling glazed section is meant to provide.

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) recommends: **Standard resolution**: split the window into a fixed panoramic (non-opening) section below the code-required parapet height, and a small opening transom (фрамуга) above it, rather than making the whole panoramic window openable.

### Device 1 — Remote Transom-Opening Mechanism

A handle-plus-linkage-plus-angled-hinge assembly lets a high transom (positioned anywhere above the low parapet) be opened from a handle mounted at normal reachable height, without climbing on furniture. Solves two failure modes of the naive alternative: a low handle lets driving rain blow straight in through the low opening gap; a high handle avoiding that problem becomes unreachable without a stool, with real fall risk. **Includes an integrated anti-break-in push-button lock** — a small transom section is otherwise easy to force open from outside by simply pushing; one motion releases it from inside.

**Framing vs. standard child-safety locks**: standard child-safety locks on openable windows are unreliable in practice because parents forget to re-engage them after use — this design removes the child-accessible opening entirely rather than relying on a lock someone must remember to use. `single-account`, not independently benchmarked against child-safety-incident data.

### Device 2 — Removable/Detachable Technical Handle

For a panoramic (non-transom) window section that must default to non-openable for child safety, but occasionally needs to open — stated example: periodic servicing access to an external AC condenser mounted behind the glazing. A decorative cap normally sits flush in the handle-spindle position (window reads as a plain fixed pane); sliding the cap aside exposes the spindle, where a separately-stored ordinary PVC-window technical handle is fitted to open/close the window, then removed and the cap snapped back afterward.

**Stated child-safety property**: claimed "practically impossible" for a child to defeat without the stored handle (specifically ruling out a pencil/found-object attack on the exposed spindle) — `single-account`, narrator's own claim, not independently tested.

Both devices are stated to be established, multi-year-use hardware, not a new invention — the source's framing is informational (most people don't know these exist).

## DIY Sash Self-Adjustment

Two specific adjustments, one tool (a 4mm hex key) — **explicit scope limit**: any other fitting/hardware adjustment should be left to a professional.

1. **Vertical position adjustment** — a screw at the bottom hinge controls the sash's vertical position; turning it clockwise several times raises a sagging sash that's begun catching on the frame.
2. **Seal-pressure adjustment** — an eccentric bolt around the sash perimeter controls how firmly the sash presses against the weatherstripping; rotating the eccentric's thicker lobe toward the seal increases pressure. **Paper-test technique**: close the sash on an ordinary sheet of paper at a test point, then pull it out — pressure is too weak if it slides out easily, correct if it comes out with resistance or tears. **Repeat at multiple points around the sash perimeter**, not just one — pressure varies point to point.

## Developer-Window Repair & Adjustment (added 2026-08-19)

> [!NOTE]
> A partner-branded technique demo (guest installer explicitly introduced as a company partner) framed as a stopgap for developer-standard windows the source's own company would otherwise discard outright — not a permanent fix or an endorsement of developer-grade windows. Extends the DIY sash self-adjustment content above with genuinely different adjustment points. [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|note]]]

- **Lock strike-plate (ответная часть) alignment**: simulate the sash's closed position by turning the handle down *first* — this is what determines where the lock's moving part actually seats, not the sash's physical position against the frame. Press the sash to the frame and check whether the frame-mounted strike plate aligns with the lock mechanism; if not, loosen and slide the strike plate until it does. Repeat per lock point on all sashes. [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|uBNF5ZYOE0Y_developer_wi]]]
- **Sash-to-frame overlap (притвор) consistency check**: pencil-mark the sash's overlap edge against the frame where the seal runs, close the sash, then reopen and measure the overlap distance at several points around the perimeter — inconsistent distances indicate the sash itself sits wrong relative to the frame (not a seal problem). Fix with the same 4mm hex key used for vertical/seal-pressure adjustment above. [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|uBNF5ZYOE0Y_developer_wi]]]
- **Center-pressure-part (средний прижим) relocation**: for a misaligned two-part fitting causing draft, unscrew and flip/reposition the *frame-side* piece. This exposes old fastener holes — clean/degrease them and seal with tube-type sealant, applied with a finger, using a white cloth (never colored — the degreaser is also a solvent that can transfer dye) and long sweeping wipe strokes (short dabbing risks the cloth sticking). [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|uBNF5ZYOE0Y_developer_wi]]]
- **Seal (уплотнитель) inspection and replacement, by profile type**: check corners specifically first — a seal welded at the corners during frame fabrication loses elasticity exactly there, creating four hard-point contacts instead of even perimeter pressure. **Decision rule**: single-lobed seal → replace immediately; double-lobed → inspect, replace only if degraded; chamber-type with a small lobe → generally fine as-is. Also check the seal's own splice/joint location — correct at the *top* of the frame (unnoticed micro-draft), a defect at the *bottom* (felt draft). [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|uBNF5ZYOE0Y_developer_wi]]]
- **Final-step check, easy to overlook**: retighten the handle's own mounting screws (they loosen with normal use) using a manual Phillips screwdriver only — a powered driver risks stripping/over-torquing them, leaving the handle loose on the sash. [source: [[_Sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|uBNF5ZYOE0Y_developer_wi]]]

## Condensation Fix: Windowsill-Drilled Directional Vent

When a wide windowsill blocks radiator warm air from reaching the glass (severe cases: a rag has to be laid along the frame to catch water), drill a hole through the sill directly opposite the center of each glass unit and insert a directional grille, one per pane — restores warm-air flow to the lower glass and stops fogging. **Explicit caution: only drill the sill if condensation is actually a problem** — don't drill preemptively.

## ⚠️⚠️ Ice and Condensation on Windows — the Cause, Where This Page Held Only the Cure (ЭлитБалкон / Владимир Кожушко, added 2026-09-14)

**This page already carries a "Condensation Fix: Windowsill-Drilled Directional Vent". That is a retrofit. This is the diagnosis it exists to treat.**

> ***«Окно — это же не греющий элемент помещения, это не радиатор, это не толстая стена. Окно — это светопрозрачная ограждающая конструкция.»***

**Thermal imaging as he describes it:** wall at +22, window surface +17 or +15, some places +5, and somewhere around **0 °C**. **At −20 to −25 outside, that zero-degree zone is where ice forms.**

**⚠️⚠️ AND THE QUESTION THAT REFRAMES THE PROBLEM:**

> ***«Окно — это же не источник воды. Там нету ни родника, там нету подведённого трубопровода.»***

> **→ ⚠️⚠️ THE MOISTURE COMES FROM INSIDE THE ROOM. Ice on a window is a HUMIDITY problem, not a window problem — the window is simply where the coldest surface happens to be.** **Replacing the window does not address the cause.**

**His remedies, in order, and note every one is about the AIR rather than the glass:**

1. **Open the sash slightly.** Winter air is cold and dry; it dilutes the moisture-laden indoor air, which then leaves via the extract.
2. **If you will not open it — a wall valve or supply unit**, so air enters through the wall instead. He notes this also spares houseplants a cold draught.
3. **A dehumidifier**, mains-powered, collecting into a reservoir.
4. **⚠️⚠️ REMOVE THE MOISTURE SOURCES, named concretely: an aquarium, watering plants, and raising the room temperature.** Move the aquarium elsewhere; water plants less or move them out. **→ This vault had nothing naming indoor humidity sources at all.**
5. **⚠️⚠️ THE RADIATOR IS A SCREEN (ширма).** It cuts off the cold air falling off the glazing **and keeps humid room air from reaching the glass and profile in the first place.**
6. **⚠️⚠️ THE WINDOWSILL TRAP: a sill that overhangs and covers the radiator stops it doing that — the heat goes forward into the room instead of up across the glass.** ***«Чем шире подоконник, чем он больше перекрывает радиатор, тем хуже.»***

> **→ ⚠️⚠️ ITEMS 5 AND 6 ARE THE ACTIONABLE PAIR, because they turn a cosmetic decision into a performance one.** **Windowsill depth is normally chosen on looks and on whether you want to stand things on it. This says an over-deep sill above a radiator CAUSES the condensation that the drilled-vent fix above exists to retrofit.** **Decide sill depth and radiator position together.**
>
> ⚠️ **Single-account, no measurements offered, and a contractor rather than a building physicist — but the causal chain is checkable and it is consistent with this vault's ventilation material.** **It also matches his own insulation finding that the thinnest, coldest spots are where mould appears.**

## ⚠️⚠️ Hardware Is a SPARE-PARTS Decision, and the Handle Order Is a Specification (same source)

**People write to him naming two brands and asking which is better. He declines the question and substitutes three criteria.**

**⚠️⚠️ 1. Is the brand still SUPPORTED where you live.** Better-known is better, and present in your city or country is better still — **because then it can be repaired.** A lesser-known brand may leave the market: no updates, no stock, and then the hardware cannot be serviced. What happens instead is that parts get **"married" (женить)** to each other — a broken corner switch or hinge replaced from another system. **The trade's own answer, he says, is to scrap the old hardware and fit something current that is actually available.**

> **→ ⚠️⚠️ Window hardware is a SPARE-PARTS-AVAILABILITY decision on a 15-year horizon, not a performance decision.** **A different and more useful frame than "buy reputable hardware": the hardware WILL need service, and the question is whether parts will still exist.**

**⚠️⚠️ 2. Go and operate it — and treat inability to show it as information.** If a window company has no office and does not have the hardware to show, *«это уже звоночек»*; they may never have handled it. **Feel for it: poor hardware is *«твёрдая, чёрствая»* and works stiffly, good hardware is *«помягче»* and closes and adjusts easily.** Ask what can break and whether there is a representative in the country. ⚠️ **Same test as the cutaway-stand check on [[13_Surfaces_and_Finishes/analysis/Entrance_Door_Construction_Spec|Entrance Door Construction & Spec]] — two unrelated trades, one idea.**

**⚠️⚠️ 3. The opening ORDER — tilt first, not swing first.** On a tilt-and-turn sash, when the handle reaches 90°, specify that the sash TILTS first. His reasons: ventilation is the frequent action; **it prevents condensate** (which is the section above); **the sash does not sag, because tilting does not hang its weight on the side hinges**; and a child who has tilted a sash will not work out that it must be pushed back before the handle can be raised.

> **→ ⚠️⚠️ THE ANTI-SAG POINT INDEPENDENTLY CORROBORATES this page's existing Zemskov finding** — that a heavy sash operated by full swing bears its weight on the side hinges and deforms, his worked example being a ~2×2 m sash failing within about a week. **Zemskov's remedy is to RESTRICT a large sash to tilt-only; this generalises it to the default handle order on any sash, and it costs nothing to specify at order time.** **Second independent source, same mechanism.**

**His summary: *«бренд, плавность хода, возможность обслуживания и удобство открывания»*.**

> **⚠️ A second, independent installer puts the same weight on hardware and states it more strongly** — Окна 2.0 (Анна): *«Фурнитуру бы я назвала вообще сердцем окна, потому что это самое важное в надёжности окна.»* **Hardware here means hinges, the whole perimeter locking mechanism, covers and handles.** Her recommendation is reputable makers over cheaper Turkish analogues, **argued on cost: avoided service call-outs for repeated adjustment.**
>
> **→ ⚠️⚠️ Two sources agree hardware is the reliability-critical component; they differ on the TEST, and the one above is better.** **"Buy a reputable brand" is not checkable at the point of sale — "is this brand still represented in my country, and can I operate it in your office" is.** **Recorded as corroboration of the importance, not of the criterion.** [source: [[_Sources/YT_M8ho5TC86eQ_okna20_choosing_pvc_windows|YT_M8ho5TC86eQ]]]

[source: [[_Sources/YT_2OCpQtu3fp8_elitbalkon_window_hardware_and_double_frames|YT_2OCpQtu3fp8]] (+-L00JLZJQ-c); ice section from [[_Sources/YT_Nr5_Pma2Tvg_elitbalkon_ventilation_and_condensation|YT_Nr5_Pma2Tvg]] (+SM4AnGeEvDI)]
