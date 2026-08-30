---
video_id: pxVSMo5e7yc
channel: Pavel Sidorik
source_type: youtube
source_title: "Электрика в новостройке 4 серия. Ремонт Новостройки от А до Я #9"
source_url: https://www.youtube.com/watch?v=pxVSMo5e7yc
transcript_file: _Archive/processed_sources/20260824_sidorik_electrical_ep9_5fd23430.txt
upload_date: 2020-12-05
fetched: 2026-08-24
fact_yield: 13
promotional_ratio: low
corroborates_existing: true
region: belarus_level1
---

# Source Note — Pavel Sidorik, "Electrical in the new building, episode 4" (#9)

4th and final episode of this project's electrical mini-series (continues
directly from `9-NjgDLleOw`, `IWVPepWlzSs`, `7QuzCGvDG_w` covered in Round
2). Low promotional content — a giveaway drawing (laser level) at the end,
clearly excluded from extraction. Region: **Belarus level 1** — speaker
states the fiber-splicing service costs "35 белорусских рублей" (35
Belarusian rubles) directly, and separately states labor pricing is "средняя
цена по Минску" (average price for Minsk) — both spoken directly about this
project's own scope, not channel branding.

## Electrical / Switches-Sockets-Cables

- **ПУЭ point 2.1.57 — cable-to-pipe parallel-routing clearance** (a
  different rule from this page's existing perpendicular-crossing 5cm
  rule): minimum 100mm between cable/wire and a parallel pipe run in
  general; minimum 400mm where the pipe carries hot water or flammable
  liquid/gas, unless the cable is heat-protected or rated for it. Sidorik's
  own routing sits at 200-300mm from hot/cold-water risers, plus the pipes
  are already insulated (not radiating heat), which he cites as compliant
  margin.
- **Damper-tape mechanism, explained directly** (partially new): the
  soundproofing damper strip that isolates screed from wall is made from
  *the same soundproofing material* used elsewhere in the project, applied
  around the perimeter after plastering, specifically so the screed never
  physically touches the wall — this is the mechanism behind an existing
  "perimeter damper strip" note on the waterproofing/plastering page,
  confirmed here from the electrical rough-in stage's perspective.
- **Fiber-optic splicing is a specialized paid service, not DIY without the
  right tool**: requires a dedicated fusion-splicer machine; a technician
  found via a classified ad charged **35 BYN (≈$10, trailing-6-month
  average to 2020-12-05, rounded)** including the cable, took 20 minutes,
  same-day turnaround (called in morning, technician arrived that evening).
  Fiber cable must be handled carefully — never kinked/bent sharply.
- **Panel assembly convention — one dedicated dif-avtomat (RCBO) per
  high-power appliance**: named list — induction/electric cooktop, electric
  oven, washing machine, dryer, water heater (boiler); room sockets also
  get their own dedicated breaker per group. Real induction-cooktop figures
  given: 4.5-5kW draw, wired with 3×4mm² cable (would need 3×6mm² for a
  conventional 8kW resistive cooktop instead) — a concrete real-world data
  point corroborating and extending this page's existing cable-gauge table.
- **Breaker brand/warranty specifics**: EKF Averes (10-year warranty) and
  EKF Proximo (7-year warranty) breakers; speaker wanted all-Averes but the
  store only had partial stock, so panel is mixed.
- **Voltage-monitoring relay, real reading and adjustable window**: relay
  window set 200-250V (adjustable at any time); real observed line voltage
  236V; relay auto-disconnects the whole panel if voltage exceeds the
  window. A separate live ammeter display on the same relay shows real-time
  whole-apartment current draw — demoed live: 1.8A idle, rising to 9.4A
  with an electric kettle switched on, framed as a practical way to
  understand combined appliance draw.
- **"Non-switchable" always-on circuit, concrete membership list**: a
  16A dif-avtomat feeding only the refrigerator and the internet modem/router
  stays live even when the master "away" switch cuts everything else —
  reasoning given: the modem must stay up so smart-home devices (including a
  water-leak-detection system) can keep reporting to the cloud while the
  owner is away.
- **Panel wet-room vs. dry-room RCD trip-current rule, a specific new
  number**: dry rooms use 30 mA trip-current dif-avtomats; wet rooms use
  10 mA (faster-tripping) — makes a general safety-margin gap for wet rooms
  concrete and numeric where this page's existing equipotential-bonding
  note only established that wet rooms need *some* extra protection.
- **Junction-box placement convention**: two external (surface, later
  plastered-over) junction boxes near the panel — one serving backsplash/
  countertop-zone kitchen sockets, one serving general kitchen sockets —
  plus three more external junction boxes for room lighting circuits (also
  later plastered over). All other switching happens inside deep back-boxes
  (подрозетники) as mini junction boxes instead, explicitly stated as
  ПУЭ-permitted and materially the same technique as a ceiling junction box,
  just relocated.
- **Wire-joining technique used throughout**: twist ("скрутка") + solder +
  adhesive-lined heat-shrink tubing, heat-shrunk with a plain gas torch
  (an industrial heat gun also works). Speaker's position, stated as his own
  opinion: any ПУЭ-permitted joining method (crimp, weld, twist+solder) is
  equally reliable *if executed correctly* — cites having opened 40-year-old
  twisted joints, including aluminum wire, that were still functioning
  fine. `single-account`, opinion.
- **Back-box (подрозетник) installation sequencing rule — install empty,
  thread cable after, not before**: mortaring in a back-box with its cables
  already fed through makes it impossible to seat level, since the cable
  slack constantly pushes the box off-center; the fix is to set the empty
  box in gypsum plaster/drywall adhesive, let it cure (ideally overnight),
  then thread cables through afterward. Grey plaster is cosmetically
  preferable on a grey wall but not functionally required. Level tolerance
  of ±1-2mm is acceptable, correctable at the socket/switch faceplate
  itself.
- **Cable-fixation-in-chase shortcut**: use cut pieces of corrugated conduit
  as an ad-hoc cable retainer inside a chase instead of drilling a hole for
  a dowel + cable clip — avoids an extra drilling step per fixation point.
- **Incoming-cable re-pull technique, real example**: developer-installed
  10mm² multi-strand incomer cable, found taped with plain electrical tape
  inside corrugated conduit (called below-average even by this developer's
  own typical standard, though "tolerable"). To re-pull a matching new cable
  through the same conduit run, the old and new cable ends are soldered
  together (tensile-tested by hand-pulling — described as unbreakable by
  hand) rather than mechanically spliced, specifically so the joint survives
  being dragged through the conduit without snapping and getting stuck.

## Regulations / Permits / Approvals

- ПУЭ point 2.1.57 is a cited *code reference* (cable-to-pipe clearance),
  not a permits/handover/registration topic — stays in the Electrical
  bucket above per this project's routing rule (code-compliance technique,
  not jurisdictional permitting/registration process). Does not route to
  `16_Legal_and_Regulations/`.

## Cost Drivers / Labor Prices

- Fiber-splicing service price above (35 BYN / ≈$10) is Belarus level-1,
  Minsk-adjacent (technician found via local classified ad). Speaker
  explicitly states labor pricing throughout this episode reflects "average
  price for Minsk" ("средняя цена по Минску") — general anchor for reading
  any other implied labor cost in this episode, though no further concrete
  labor total is given (materials/labor cost summary shown on-screen only,
  not read aloud with figures; switch/socket cost explicitly deferred to a
  later episode since they weren't installed yet).

## Unclear / Needs Confirmation

- The panel's lighting-circuit breakdown is stated as "3 groups" but 4
  room-pairings are named (living room-corridor; living room-balcony;
  kitchen-corridor; bathroom-small room) — possible verbal slip or a pairing
  sharing one breaker not fully disambiguated in speech. Flagged, not
  resolved.

[transcript: `_Inbox/transcripts/20260824_sidorik_electrical_ep9_pxVSMo5e7yc_5fd23430.txt`]
