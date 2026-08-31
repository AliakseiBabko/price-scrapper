---
source_type: video transcript (single-speaker practitioner explainer, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=0sJPlpi8I2U
video_id: 0sJPlpi8I2U
transcript_file: _Archive/processed_sources/20260824_sidorik_khrushchevka_finale_cost_7b77e438.txt
fetched: 2026-08-24
upload_date: 2020-08-07 (metadata-confirmed via yt-dlp `upload_date`; precedes videos 1/2 of this trial batch, which cover the *next* project this video announces)
channel: Pavel Sidorik (individual finisher/plasterer/tiler/electrician practitioner) — `single-account`
regional_applicability: Belarus, level 1 — the speaker states directly "это среднестатистическая стоимость ремонта для Беларуси" ("this is the average renovation cost for Belarus") and explicitly names Belarus, Russia, Ukraine, and Kazakhstan as the comparison set for material-cost similarity
currency: USD stated directly by the speaker (primary figures); a secondary Russian-ruble (RUB, not Belarusian ruble/BYN) conversion is also given by the speaker himself — see Numeric Data note below on this apparent mismatch
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 7
promotional_ratio: low
corroborates_existing: false
---

# Extraction Note — Pavel Sidorik: Khrushchevka Remake Finale — Finished Apartment Tour and Total Cost (YouTube 0sJPlpi8I2U)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Source Metadata

Final (37th) episode of a self-managed, self-executed renovation of a
31.2 m² one-room "khrushchevka" (1964-built apartment), done personally by
the speaker over roughly one year in his spare time (alongside his main
job). This is a genuine, complete, first-person documented project with a
real, itemized final smeta total — one of the strongest case-study
candidates processed for this project's topic. No sponsor segment in this
video.

## Region check (why this clears the level-1 bar)

Direct quote: *"Хочу сказать, что это среднестатистическая стоимость
ремонта для Беларуси... стоимость материалов примерно будет одинаковой
для Беларуси, России, Украины и, наверное, даже для Казахстана"* ("I want
to say this is the average renovation cost for Belarus... the cost of
materials will be roughly the same for Belarus, Russia, Ukraine, and
probably even Kazakhstan"). Belarus is named directly and specifically as
the primary reference market for this project's total — **level 1**,
clearing this project's location-attribution bar directly (distinct from,
and stronger than, this trial's video 1, which did not clear it). The
speaker also separately notes labor cost specifically varies by
region/country ("you can find masters cheaper or more expensive"), while
material cost is what he claims travels across these markets — a caveat
worth preserving alongside the headline total, not dropped.

## Numeric Data — Real Total Project Cost, Self-Managed, 31.2 m² Khrushchevka (2020)

- **Labor total**: **$6,168** (stated directly in USD).
- **Materials total**: **$9,193** (stated directly in USD).
- **Combined total, speaker's own figure**: **≈$15,500** (rounding the
  $6,168 + $9,193 = $15,361 sum, with the speaker's own explicit caveat
  that the true total likely runs "about $300 more" once minor
  uncounted items are included — treat the true total as **≈$15,500–
  15,800**, not a single exact figure).
- **Per-m² figure (this project's own derivation, not stated by the
  speaker)**: $15,361 ÷ 31.2 m² ≈ **$492/m²** (labor + materials, before
  the speaker's own "~$300 more" caveat; ≈$502–507/m² (`arithmetic-exact`) if that caveat is
  included). This is the **first self-managed case in this store with
  both (a) level-1 Belarus confirmation and (b) a directly computable
  $/m² figure** — the existing Yana Vrublevskaya self-managed case
  (`yana_vrublevskaya_minsk_mir_studio_2023_case`) has neither a
  confirmed m² denominator nor level-1 region confirmation.
- **Delivery model**: **Self-Managed / Itemized** — explicitly a DIY
  project, done personally by the speaker (a professional finisher) in
  his own spare time, not a hired/managed crew; the labor figure
  represents the speaker's own valuation of his own labor time (per-video
  smeta accumulation, referenced but not individually re-extracted here),
  not a third-party contractor's invoice.
- **Secondary RUB figure, flagged as an apparent currency mismatch, not
  silently corrected**: the speaker also states the labor/materials
  totals in **"российских рублей"** (**Russian** rubles) — 6,168
  USD → "440 4096" (ASR-garbled digit run, most plausibly **≈440,000
  RUB**) and 9,193 USD → **661,896 RUB**. A same-project sanity check
  using `tools/pricing/currency_converter.py` (`--pair USD/RUB
  --trailing-months 6 --before 2020-08-07`, resolved rate **71.16
  RUB/USD**) gives 6,168 USD ≈ 439,000 RUB and 9,193 USD ≈ 654,000 RUB —
  both close to the speaker's own stated RUB figures (within ~0.2% and
  ~1.2% respectively), confirming the garbled labor-total digit string is
  most likely **440,000-ish RUB**, not a transcription of a materially
  different number. **Flagged, not corrected in the store**: this is a
  Belarus-based project (per the region check above) with costs converted
  to *Russian* rubles rather than Belarusian rubles (BYN) — plausibly the
  speaker converting to RUB for a broader Russian-speaking-audience
  frame of reference (common on this and similar channels per this
  project's own standing observation about Russian being the channel
  lingua franca regardless of speaker's own country), not a claim that
  the renovation itself was priced/paid in RUB. **Treat the USD figures
  as the authoritative primary figures**; the RUB figures are a same-
  source illustrative conversion, not a second currency of payment.

## Mistakes / Warnings & Planning Rules — Small-Apartment-Specific Technique

- **A small wet room's footprint is constrained by the original building
  envelope, not by owner preference** — the speaker explicitly declines
  to enlarge the bathroom despite repeated viewer requests, citing the
  disproportionate cost/bureaucracy of a real replanning (hidden-works
  acts, official replanning approval, waterproofing sign-off) on a 31.2 m²
  unit where the bathroom footprint is a small fraction of an already-tiny
  total area.
- **A shower installation (инсталляция) can be pushed flush against a
  wall as a deliberate space-saving compromise in a cramped bathroom** —
  the speaker candidly notes this was a forced choice given space
  constraints, not an ideal ergonomic layout, but reports it as
  personally workable even for a broad-shouldered user.
- **Cladding a wall-hung toilet's installation frame in laminated
  chipboard (ламинированное ДСП), rather than a permanent solid box, is
  a deliberate future-serviceability choice** — done specifically so the
  frame can be disassembled and reconnected to a new riser during an
  anticipated future capital repair (капремонт) without demolishing a
  permanent enclosure.
- **A building's own scheduled capital-repair (капремонт) timeline can
  block an otherwise-desired fix now** — the speaker was refused
  permission to replace an old heated towel rail connected to the
  building's heating system specifically because it would require its own
  design/approval process; the fix was deliberately deferred to the
  building's already-scheduled capital repair instead of pursuing a
  separate approval now, avoiding duplicate paperwork/cost.
- **A loft-style glass-and-metal partition between an open kitchen and
  living space must still satisfy the gas-appliance-open-space code**
  (a partition cannot leave a fully open gap between a gas kitchen and
  the adjoining living space) — the speaker's own solution (a full glass
  panel to the ceiling, not a partial screen) is offered as a code-
  compliant way to still get an open, visually connected loft aesthetic.
  Same underlying gas-code constraint independently corroborates this
  store's existing gas-code-compliant-partition finding from a different
  channel's source (Category 5, `yt_2E7YVK6PhIM`).
- **A sloped/pitched ceiling (top-floor apartment under a roof) is
  presented as a design opportunity worth preserving rather than a defect
  to correct** — the speaker deliberately did not level the sloped
  ceiling (280–320 cm) specifically to avoid losing the height gain,
  framing the slope as giving a converted-attic ("мансардный") character.
- **A single quartz-vinyl/quartz-laminate flooring material can be run as
  one continuous "carpet" across wet and dry zones alike** (kitchen,
  hallway, living space) specifically because of its water tolerance —
  offered as a simpler alternative to zoning different flooring materials
  by room, with the same click-lock installation method as ordinary
  laminate but higher wear resistance.

## Target Page(s)

- Build a **scoped case study** at
  `11_Budget_and_Planning/case_studies/sidorik_khrushchevka_finale_31m2_2020_case.md`,
  following the `yana_vrublevskaya_minsk_mir_studio_2023_case` template —
  this source's level-1 Belarus confirmation and computable $/m² figure
  make it a stronger self-managed reference than the existing Yana
  Vrublevskaya case on those two specific dimensions (though Yana's case
  has richer line-item granularity).
- `Budgeting_Guide.md` §"self-managed benchmarks" — add this as a third
  self-managed reference point alongside the labor-only rate card and the
  Yana Vrublevskaya case, since it is real financial data that
  materially strengthens the guide's self-managed section (a headline
  benchmark update is warranted per this wrapper's own step-5 guidance).
- The small-apartment/gas-code/future-serviceability technique bullets
  route to `Rules_Heuristics.md`'s general Mistakes/Warnings and Planning
  Rules sections — no dedicated small-apartment page exists yet in this
  vault (noted, but below the 3+-source page-creation threshold).

## Relevance to This Project's Topic

Very high value: a real, complete, itemized self-managed renovation total
with the strongest regional evidence (level 1, explicit) of any
self-managed source in this store, plus a directly computable $/m²
figure — fills a genuine gap (this store's existing self-managed
references each lack one of these two properties). Several genuinely
useful small-apartment planning/code-compliance techniques as a bonus.

## Promotion self-check

Re-read in full after drafting. The labor/materials/total figures, the
per-m² derivation, the RUB-figure cross-check, the region-confirmation
quote, and all six technique bullets are reflected in the case study and
store additions. The apartment's for-sale mention at the very end is
noted but not extracted as a durable fact (a one-off, non-generalizable
detail).
