---
source_type: video transcript (single-speaker practitioner explainer, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=9-NjgDLleOw
video_id: 9-NjgDLleOw
transcript_file: _Archive/processed_sources/20260824_sidorik_electrical_ep6_ca2723ac.txt
fetched: 2026-08-24
upload_date: 2020-10-31 (metadata-confirmed via yt-dlp `upload_date`)
channel: Pavel Sidorik (individual finisher/plasterer/tiler/electrician practitioner) — `single-account`
regional_applicability: unresolved for this specific episode (no location/currency named directly this time) — series-level Belarus attribution already well-established by episodes 2-5, but per this round's per-episode-check rule this episode does not independently clear the bar
currency: not applicable — no pricing stated in this episode; speaker explicitly defers the full materials/labor "смета" to the end of this electrical mini-series (episode 8 or later)
language: ru (clean, manually-created captions)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 10
promotional_ratio: low
corroborates_existing: true (independently corroborates an existing Zemstandart/Zemskov "plan furniture before sockets" rule)
---

# Extraction Note — Pavel Sidorik: New-Building Renovation A-to-Z, Episode #6 "DIY electrician in a new building" (YouTube 9-NjgDLleOw)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Source Metadata

Episode 6, first of an explicitly announced 2-3-part electrical mini-series
within the same continuous ~61 m² apartment renovation (episodes 7-8 in
this round continue it). Covers: developer-supplied electrical inventory,
planning method, materials list, marking/layout, and the start of
chasing/drilling. No sponsor segment in this episode — a reusable
dust-barrier product ("Blue Dolphin" brand, same brand as the earlier
window-masking-tape and floor-layout-tape mentions) is shown and used but
not pitched as a paid placement (no link/CTA, described purely as a
practical technique). Not flagged as advertising.

### Region note (checked explicitly per this round's brief)

**No direct location or currency statement appears in this episode** —
unlike episodes 2 (Minsk labor rate), 3 (Belarus developer-remediation
practice), 4 (Minsk + explicit "белорусский рубль"), and 5 (explicit
"белорусский рубль" without a city). The only regulatory reference is
"ГОСТ" (a state-standard family shared across Russia, Belarus, and other
CIS countries, not itself Belarus-specific). **Conclusion: region
unresolved for this specific episode's own content**, per this round's
per-episode-check rule — this does **not** reset or weaken the series'
already well-established Belarus attribution from episodes 2-5 (still the
same continuous apartment/project), it simply means this episode's own
technique/material content is recorded without a fresh region tag of its
own; treat it as generally applicable RU/CIS-market technique unless a
later episode in this same mini-series states a location directly (worth
checking again for episodes 7-8).

## Cable Circuits & Panel Design — Materials and Cable Specifications

- **Developer-supplied electrical inventory in this apartment**: an
  exterior metal panel with breakers, of which only **one** breaker is
  actually wired to anything (the rest are decorative/for future circuits
  per the developer's own labeling) — that one active breaker feeds a
  single outlet (the speaker adds a second outlet since one is
  insufficient) and, temporarily, one string of work lighting. Incoming
  service cable: 3-conductor, 10mm² stranded, plus a separate fiber-optic
  line — expected to need extending (crimped/reconnected, not soldered)
  since it won't reach the new panel's planned location; a coupling
  sleeve (муфта) is the fallback if extension isn't possible. Grounding
  is already present in the bathroom. A video door-intercom is present
  and will be relocated.
- **Cable-type specification for this project (GOST-only requirement)**:
  socket/power circuits use ВВГнг-LS 3×2.5; lighting circuits use two
  different cable types depending on switch type — ВВГнг-LS 3×1.5 (for
  runs needing a 3rd conductor, e.g. two-way/pass-through switching) and
  ВВГнг-LS 2×1.5 (simple single-point switching). **Buying-guidance rule:
  cable must be certified to ГОСТ (the state standard), never to ТУ
  (a manufacturer's own internal specification)** — framed as a real
  quality-shortcut red flag distinct from brand name, a generalizable
  buying heuristic for cable purchasing in this market.
- **Panel components, named brand**: EKF-brand "Aeres" and "Proximo"
  series RCBOs (дифавтоматы), a voltage-monitoring relay, the main
  incomer breaker, and standard breakers; a built-in "Proximo" 36-module
  panel enclosure; a separate built-in metal enclosure specifically for
  low-voltage/data cabling.
- **Back-box drilling technique**: use a **72mm hole saw for a 68mm
  back-box**, not a 68mm hole saw matched exactly to the box — the extra
  4mm of clearance is specifically so the back-box can still be leveled/
  adjusted within the hole once set. **Tool choice depends on wall
  material**: a rotary hammer alone is sufficient for a soft block wall
  (this project's aerated-concrete/silicate partitions); drilling into
  solid concrete needs a heavier-duty drill, since a lighter drill's
  torque-limiting clutch will slip/trip repeatedly on concrete. Groove
  (штроба) depth is sized to fit two 2.5mm² cables side by side.
- **Conduit/back-box parts list**: НД (ПНД) corrugated conduit, 16mm and
  20mm diameters, for floor-routed cable, secured with dedicated conduit
  clips; both standard and deep 68mm back-boxes used depending on
  location; connections made via terminal blocks inside back-boxes (not
  twisted/soldered joints); dowel-clamps for securing cable runs; ferrule
  end sleeves (НШВИ) for panel-side wire termination; heat-shrink tubing;
  dedicated light-fixture terminal blocks.

## Planning Rules — Furniture-First Electrical Planning Method (corroborates existing rule)

- **Draw the furniture layout before finalizing socket/switch placement** —
  independently corroborates this store's existing Zemstandart/Zemskov
  rule of the same substance (`Electrical_Key_Concepts_and_Planning.md`'s
  "Plan furniture layout before finalizing socket placement"), now with a
  second, independent practitioner and a concrete method: model the
  apartment in SketchUp with exact room dimensions, ceiling heights, and
  furniture drawn to real size and position, then read off electrical-
  point placement directly against that model — outline furniture
  footprints on the floor/walls for a quick sanity check before
  finalizing. Especially important for built-in kitchen and bathroom
  furniture, where a mismeasured point is expensive to fix later. **A
  self-taught, non-expert can do this**: the speaker reports spending 2
  days on the SketchUp model despite limited software familiarity, and
  explicitly credits YouTube tutorials as sufficient to learn the tool.
  A prior, less-precise iteration of this same practice (from this
  channel's earlier khrushchevka project) used hand-drawn pencil sketches
  instead — the digital model is presented as a genuine upgrade in
  planning precision, not just a stylistic choice.
- **Uniform switch-height marking technique**: mount a laser level on a
  spring-loaded extension pole (распорная штанга) positioned mid-room,
  and mark every switch location in the room from that single 360°-laser
  position at once — guarantees a consistent height (this project's
  standard: 90cm from finished floor) across every switch in the room
  without repositioning the laser per point.
- **Floor-base prep specific to electrical rough-in**: after screed
  demolition (episode 3) and cement-laitance grinding, leftover surface
  pits/divots were patched with cement plaster (applied, then scraped
  flush with a trowel) purely to create a smooth enough base for routing
  corrugated conduit — cosmetic evenness only, since the patched floor
  will be fully covered by the new screed regardless. **Real before/after
  screed-thickness figures for this project**: original developer screed
  10cm, new total floor buildup (screed + underlayment) reduced to
  **7-8cm** — a concrete confirmation of episode 3's stated rationale for
  demolishing an oversized developer screed to reclaim ceiling height.
- **Reusable dust-containment room barrier, same "Blue Dolphin" product
  line as this channel's earlier window-masking tape**: a pre-made
  plastic zip-door barrier that hangs over a doorway and seals with
  included double-sided tape — lets the crew chase/drill one room at a
  time fully sealed off, vacuum it clean, then move tools/belongings
  there before opening the next room; reusable across multiple future
  projects. **Material-specific adhesion caveat**: on this project's
  aerated-silicate-block walls, the included double-sided tape alone was
  judged unreliable (dusty, porous surface), so the speaker backs it up
  with ordinary plastering tape as a secondary adhesive. Same PPE list as
  prior episodes (goggles, mask, hearing protection) plus a vacuum,
  needed even with a dust-collecting grinder/drill attachment.

## Switches / Sockets / Cables — Named Product and a Cosmetic Lifehack

- **Named brand with a direct price/quality assessment**: EKF-brand
  outlets/switches, "Valencia" series — described by the practitioner as
  "хороший вариант по соотношению цена и качество" (good price-to-quality
  ratio). Planned devices: two-gang switch, two-gang pass-through
  (3-way/traveler) switch, one-gang switch, grounded outlets, outlets
  with integrated USB charging ports, network/ethernet outlets. A TV
  antenna outlet was considered and explicitly **not** included in this
  project.
- **Cosmetic lifehack: swap only the switch/outlet's outer frame (рамка)
  to a different color while keeping the same white mechanism/base** — a
  cheaper way to get a color accent on a switch plate than buying an
  entirely different product line, since frames are sold separately from
  the mechanism.

## Numeric Data / Measurements — Real Worked Room-by-Room Electrical Point List

A real, itemized point-by-point plan for this project's bathroom/WC and
kitchen, comparable in kind to this store's existing 46 m²/~100 m²
electrical-walkthrough entries (a different, independent practitioner and
apartment):

- **Bathroom/WC**: 2 outlets above the vanity + 1 switch for mirror
  backlighting; 2 outlets in the closet (washer + dryer); underfloor-
  heating thermostat at 90cm height, left of the entry; additional cable
  runs for a ventilation fan and mirror backlight; lighting: 4 recessed
  fixtures in the bath zone, 2 in the toilet zone; a dedicated 220V cable
  in the toilet zone for a water heater (boiler).
- **Kitchen**: 6 outlets along the backsplash + 1 switch for under-
  cabinet lighting (exact backsplash outlet height deferred until tile
  layout is finalized); oven/microwave/fridge outlets routed sideways
  into an adjacent cabinet (alternative: behind the kickplate/plinth);
  cooktop + dishwasher outlets likewise routed into an adjacent cabinet
  or behind the plinth; 2× 220V outlets + 1 network outlet behind the TV;
  a dedicated 220V cable for a range hood; 2 outlets under the window; 1
  outlet near the sofa. Kitchen-living lighting: one central fixture,
  spotlights, and a track light.
- **Apartment-wide switch height standard for this project: 90cm from
  finished floor**, applied uniformly (see the extension-pole marking
  technique above).

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md`
  — cable specifications, GOST-vs-TU buying rule, named panel components,
  back-box drilling technique.
- `12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing.md` —
  the furniture-first planning method (corroborating an existing rule),
  the extension-pole marking technique, and the floor-prep/dust-
  containment technique notes.
- `12_Engineering_and_Systems/analysis/Switches_and_Controls.md` — the
  named EKF/Valencia product line and the frame-color-swap lifehack.
- General budgeting store `Numeric_Data.md` — the room-by-room worked
  electrical point list, alongside the two existing independent
  walkthrough entries.

## Relevance to This Project's Topic

High value: a genuinely independent second confirmation of an existing
planning rule (furniture-before-sockets), several concrete, transferable
techniques (extension-pole marking, oversized hole-saw sizing, GOST-vs-TU
buying guidance), and a real, itemized bathroom/kitchen electrical point
list usable as a direct planning comparison against this store's other two
such walkthroughs. No pricing yet (deferred to a later episode in this
same mini-series) and no fresh region confirmation this specific episode.

## Promotion self-check

Re-read in full after drafting. The developer-inventory description, all
cable/panel material specifications and the GOST-vs-TU rule, the back-box
drilling technique, the furniture-first planning method and SketchUp
detail, the extension-pole marking technique, the floor-prep and
screed-thickness figures, the dust-barrier technique and its
material-specific adhesion caveat, the named EKF/Valencia product line and
frame-swap lifehack, and the full room-by-room point list are all
reflected in the store/page additions below. No promotional content was
identified in this episode to exclude.
