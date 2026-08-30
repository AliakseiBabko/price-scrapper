---
source_type: video transcript (self-promotional renovation-company channel, real jobsite walkthrough of rough electrical wiring, Russian, auto-generated captions)
source_url: https://www.youtube.com/watch?v=gKBzDEllg4M
video_id: gKBzDEllg4M
transcript_file: _Archive/processed_sources/20260824_kruglov_best_wiring_a_to_z_fa6fe90b.txt
fetched: 2026-08-24
upload_date: 2023-12-17 (metadata-confirmed via yt-dlp `upload_date`)
channel: Konstantin Kruglov | Ontario (presenter identified on-camera as Никита Кузнецов, руководитель компании Онтарио / Nikita Kuznetsov, head of the Ontario company)
regional_applicability: level 2 only (channel's established Moscow association; no city named directly in this video's spoken content — a real 83 m² jobsite is shown but no location stated)
currency: n/a (no pricing content — a 20-30% cost-premium figure is given only as a relative comparison, not an absolute price)
language: ru (auto-generated captions, method=youtube-transcript-api, generated=True)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 12
promotional_ratio: low
corroborates_existing: true
---

# Extraction Note — Konstantin Kruglov/Ontario: Best Electrical Wiring for Modern Renovations, A to Z (YouTube gKBzDEllg4M)

## Source classification

Video/topical transcript — a real jobsite walkthrough (83 m², 3 rooms + kitchen-living + entry + 2 wet rooms, mid-renovation) of rough electrical wiring decisions, narrated by the company's head (on-camera, named). Dominant purpose: technical education anchored in a real, visible install, not a studio-recorded generic list.

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Genuinely case-anchored content (specific measurements, a real panel shown and explained, a real client conversation reconstructed) — higher evidence quality than a purely studio-recorded list video from the same channel.

## Electrical

Konstantin Kruglov / Ontario says (level 1, spoken directly, anchored to a real 83 m² jobsite unless noted):

- **⚠️ Floor-vs-ceiling routing decision rule, with an explicit cost tradeoff**: route through the floor (cheaper) only if the screed can still cover the highest point of the routed cable/conduit by at least 4cm; if it can't (e.g. because plumbing crossing forces the cable higher), route through the ceiling instead — but ceiling routing costs roughly **20-30% more** than floor routing for the same job. Ceiling routing is also the default when the ceiling is a suspended/false ceiling (not a plastered one) or when the designer/owner simply prefers it, independent of the screed-height constraint.
- **⚠️ Minimum clearance between electrical cabling and water-supply pipes when they cross: 5cm, or a code-compliant sleeve** — a real violation was shown on this jobsite (cable and pipe crossing with less than that), and the source states explicitly that hitting both the 5cm clearance and the 4cm screed-cover minimum simultaneously is often not achievable within a normal floor buildup; when it isn't, the company flags this to the client, gets explicit informed sign-off to proceed with the shortfall, and frames it as a minor-severity violation, not something requiring the floor buildup to grow.
- **⚠️ Conduit-color/type code rule**: use only grey PVC ("ПВХ") conduit when routing is exposed/embedded above a ceiling — striking-colored options (black/orange/red) are a different material ("ПНД") that supports combustion and is only safe to use when it will be fully embedded in poured floor screed; the source is explicit that colored ПНД conduit should never be used for ceiling routing.
- **⚠️ Real panel example, with a specific device-combination rationale**: main incoming breaker → voltage-monitoring relay (trips if a voltage spike exceeds a set threshold) → RCBOs ("дифы") dedicated to wet-zone circuits → a bank of shared RCDs, each protecting a labeled group (A/B/C/D) of ordinary breakers hanging off it, rather than a separate RCBO per circuit. **Concrete practical benefit of the shared-RCD-per-group design, stated as a real client capability**: a client can switch off just the socket group in a kids' room while the lighting circuit (a different group) stays on, without losing leakage protection on either — every breaker is still leakage-protected via its shared RCD, even though the breaker itself only protects against short-circuit/overload. Corroborates and gives a concrete real-world use case for this store's existing shared-RCD-vs-RCBO tradeoff note.
- **⚠️ Floor-routed corrugated conduit over acoustic underlayment must be tied with cable ties to the underlayment's own mesh, never nailed/stapled through it** — the soundproofing mat beneath the conduit is a "zero-impact-noise" product and puncturing it with a fastener defeats its function.
- **⚠️ Sequencing rule: plaster the walls before marking/chasing electrical point locations, not the reverse** — real apartment walls are out-of-plane/crooked; if a point is marked and chased against the raw wall/slab surface, the finished result comes out visually crooked once plaster (which adds real thickness) is later applied over it. Plastering first also means less of the actual load-bearing wall gets chased, since more of the channel depth is absorbed by the plaster layer itself. **This is a wall-specific companion to this store's existing floor-screed-as-datum rule** — the same "reference the finished surface, not the substrate" logic applies to both floor and wall finishes.
- **⚠️ Chase depth rule**: chase deep enough that the finished plaster layer over the buried cable is at least 0.5cm thick — plaster only functions/bonds properly from about 0.5cm of thickness upward; a cable sitting almost flush with the wall surface risks inadequate plaster cover.
- **⚠️ Corrugated conduit is only needed for the floor/ceiling run up to the point it enters a wall — inside the wall itself, code-rated cable (e.g. "ВГ") can be chased and buried without conduit**, because routing multiple such cables in conduit inside a wall would require an impractically large/long chase; this is standard, coded, and safe practice.
- **⚠️ Equipotential-bonding box (коробка уравнивания потенциалов) is a mandatory-by-code wet-room grounding component**, distinct from ordinary circuit grounding — it bonds the room's metal fixtures/parts together to the same ground reference (the source's named examples: the plumbing manifold/installation-frame, and a metal bathtub). Stated rationale: stray/leakage currents can travel through water or metal fixtures and deliver a shock to someone touching a fixture or standing in a metal tub; equipotential bonding is described as low-cost to implement and mandatory to include.
- **⚠️ Electric underfloor-heating cable used vertically on a wall as a towel-warmer substitute** — a real jobsite decision shown: two wall sections in this bathroom will have electric floor-heating cable mounted on the wall itself (not the floor), finished with porcelain tile over it, functioning as a heated wall/towel-hanging surface instead of a standard electric towel rail; the actual floor in the same room will separately get its own electric underfloor heating.
- **⚠️ Electric underfloor heating under tile is characterized as close to mandatory-by-default, not a luxury upsell** — cited reasoning: very low running cost ("kopecks") for a large comfort payoff, specifically recommended "in an obligatory way" wherever tile flooring is used.
- **⚠️ Floor-embedded socket installation technique**: a floor socket's back-box is much larger/deeper than a standard wall box, so before pouring screed, build a temporary foam/rigid-insulation (e.g. Penoplex) block shaped as a placeholder in the exact location/size the floor socket will occupy; once the screed cures, remove the foam block and install the actual floor socket into the resulting cavity — using the foam block as disposable formwork rather than trying to install the real box before the pour.
- Designer/finish-planning note: a TV-wall socket cluster should include a spare cable-conduit run between two of the sockets specifically to let an HDMI cable be routed invisibly later (e.g. from the TV point down to a shelf-mounted smart speaker), avoiding visible cabling once furniture/decor is in place.

## Mistakes / Warnings

- **⚠️ Marking/chasing electrical points from the raw slab instead of the design project's own "finished floor" reference produces visibly crooked socket/switch placement** — the same finished-floor-reference issue this store already has for the floor screed extends explicitly to how design-project point coordinates should be interpreted on site; an electrician who marks from the bare slab, ignoring the not-yet-poured finished screed, will produce misaligned results even with an otherwise-correct design drawing.

## Design Concept

- A developer-provided example (not this company's own work, cited critically): an oversized sliding door/window unit that the developer's own hardware specs can't structurally support at that size, prompting the developer to compensate by offering a plastic "breather"-type fresh-air ventilation unit (filtering, winter pre-heating) rather than actually usable window ventilation — cited as evidence of a real developer cutting a corner on load-bearing hardware sizing, kept as a specific critical anecdote about developer defaults rather than a generalized "breather" recommendation (this store already covers breathers independently).

## Advertising / Promotional Content Notes

Low promotional ratio. On-camera presenter is named and identified as the company's head (Никита Кузнецов, Онтарио), which is itself a form of credibility-building self-promotion; one closing Instagram/website/measurement-booking call-out. The technical content itself (routing rules, code clearances, conduit color code, panel design) is neutral/brand-agnostic and not steered toward a specific product or upsell — the client-consent framing around the 5cm/4cm shortfall is presented candidly, including the company's own tradeoff reasoning, rather than glossed over.

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` — floor-vs-ceiling routing decision + cost premium, pipe/cable clearance rule, conduit color/material code, real panel-group RCD example, floor conduit anchoring-to-mesh technique, wall-plastering-before-chasing sequencing (companion to existing screed-as-datum rule), chase-depth-for-plaster-cover rule, conduit-only-to-wall-entry rule, floor-socket foam-formwork technique, marking-from-raw-slab mistake.
- `12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer.md` — electric underfloor-heating-cable-on-wall as a towel-warmer alternative (new option distinct from the page's existing hydronic-vs-electric-towel-warmer comparison).
- Equipotential-bonding box: routed to `Cable_Circuits_and_Panel_Design.md` (wet-room electrical grounding requirement) since no dedicated bonding/grounding subsection exists elsewhere and this is fundamentally an electrical-code component, even though it touches plumbing fixtures.
- Underfloor heating under tile as a near-default recommendation: this is a corroborating restatement of guidance already established elsewhere in this store (electric underfloor heating cost-effectiveness) — not logged as a separately new fact, noted here for completeness only.
- Developer breather anecdote: kept in this note only (Design Concept section) — too anecdotal/single-instance to promote to a wiki page beyond this store's existing breather coverage.

## Relevance to This Project's Topic

Medium-high — several concrete, checkable install-sequencing and code-clearance rules (5cm pipe/cable clearance, 4cm screed cover, conduit color code, chase-depth-for-plaster) directly useful for QC-checking a hired crew's rough electrical work under this project's self-managed plan.

## Gaps

- Region: level 2 only; no city named despite the real jobsite footage.
- No absolute pricing — only a relative 20-30% ceiling-vs-floor cost premium, not usable for $/m² comparison.
- Presenter identity (Nikita Kuznetsov, head of Ontario) is new to this store's source roster for this channel — noted for completeness, not independently verified beyond the on-camera self-identification.

## Recommended Downstream Routing

Wiki-routed to `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` (primary) and `12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer.md` (heated-wall towel-warmer alternative) — existing matching pages found for every genuinely new fact, no `Durable_Facts.md` entry needed.

## Promotion self-check

Re-read in full after drafting. All concrete rules, measurements, and techniques identified during extraction are reflected in the sections above; the developer-breather anecdote and the underfloor-heating corroboration are explicitly flagged as not promoted beyond this note / already covered.
