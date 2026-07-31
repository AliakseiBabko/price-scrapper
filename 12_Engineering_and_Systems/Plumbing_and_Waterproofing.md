# Plumbing & Waterproofing

Covers water supply/drainage rough-in, fixture placement and sequencing, leak protection, and wet-zone waterproofing. Format follows [[12_Engineering_and_Systems/_supporting/wiki_page_format|the shared engineering-systems page template]] — narrative sections first, a Quick Reference table at the end.

## 1. Key Concepts

- **Rough plumbing vs. finish plumbing** — rough-in (supply/drain line routing, collector/manifold assembly, riser connections) happens early and gets concealed under screed/tile; finish plumbing (fixtures, faucets, visible trim) happens near the end. Most of the durable technical content on this page concerns rough-in, since mistakes there are the expensive ones to fix later.
- **Every apartment has two distinct "wet zones"**: the kitchen (a "clean" wet zone) and the bathroom/WC (a "dirty" wet zone). The default structural principle is that a wet zone should stay stacked above the same wet zone in the apartment below — see §2.
- **A "zashivka" is not the same thing as a "venshakhta"** — this distinction matters enough to repeat here even though the ventilation-shaft half of it is documented in [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]] §1: a **zashivka** (plumbing cladding box, built around water/sewer risers, sometimes oversized "for the developer's convenience") **can be demolished and rebuilt more compactly** to reclaim space. A **venshakhta** (ventilation shaft, a completely different structure) must never be touched. See §4 for the full detail on what can and can't be modified within a zashivka specifically.

## 2. Wet-Zone Placement & Approval

- **Default principle**: a wet zone (kitchen or bathroom) should remain stacked above the same wet zone in the downstairs neighbor's apartment — this is a structural/plumbing-stack alignment convention, not an arbitrary preference.
- **Even a flexible/free-planning unit doesn't bypass the approval requirement**: a top-floor or free-planning apartment may have more physical flexibility to deviate from the stacking default, but **relocating a wet point still requires going through the same architecture-registration/approval process** as a standard layout would — flexibility of the physical layout doesn't remove the paperwork. *(This overlaps with regulatory content already tracked with a stricter evidence bar in `11_Budget_and_Planning/_supporting/knowledge/intermediate/renovation_regulations_belarus_knowledge_store.md` — see that store for the Minsk-specific исполком approval process this connects to.)*
- **Bathroom layout preferences**: avoid a bathroom entrance directly off a kitchen/dining area (awkward for guests and host alike) — prefer entrance from a hallway/corridor. Keep the bathroom door at least ~1–1.5 m from the entryway/mudroom zone, since dirt/grit concentrates near the entry and a bathroom door too close to it means frequently crossing the "dirty" entry zone.

## 3. Rough Plumbing: Sequencing & Layout

- **Toilet placement should drive bathroom layout, not the reverse** — place the toilet first, as close to the riser as practical, because it requires a 100 mm-diameter drain pipe, the hardest pipe size to conceal/route of any bathroom fixture. Plan sink and shower positions around the toilet's fixed position, not the other way around.
- **When relocating a sink, place it along a wall, not mid-room** — pressurized supply lines can be hidden in screed with little constraint, but the gravity-fed drain line needs a consistent slope toward the riser; the farther a sink sits from the riser, the more screed depth is needed to conceal the sloped pipe. A wall placement lets the drain run inside the wall to the riser without losing the required slope.
- **Scan floor screeds with a detector before chasing or drilling** — prevents accidentally cutting or puncturing concealed PEX radiator/heating lines that may not match what the developer's own drawings show (a floor plan's marked line positions and the actual as-built routing can differ).

## 4. The Zashivka: What Can and Can't Be Modified

Within a plumbing cladding box (zashivka):
- The box itself **can be demolished and rebuilt more compactly** to reclaim space — a worked example from one source gained ~10 cm this way.
- A **water-supply pipe** inside a zashivka can sometimes be re-routed (a plumber can re-weld/reposition it).
- A **sewage stack** inside a zashivka generally **cannot** be relocated — it runs as a single vertical column, following the same structural logic that makes a ventilation shaft untouchable (see [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]] §1).

Don't assume "it's inside a cladding box, so it's all fair game" — supply and drain lines within the same box follow different modification rules.

## 5. Fixtures & Leak Protection

- **Install coarse and fine main-line water filters** inside the plumbing collector cabinet — protects faucets, shower valves, and appliances downstream from pipe debris and sediment.
- **A skipped flush pre-filter has a specific, documented failure mode, not just a theoretical risk**: one source cites a real incident where sediment (from a period the water was shut off during a vacation) jammed a wall-hung toilet's cistern float mechanism, requiring an emergency repair callout. That company now installs flush filters as a non-negotiable standard item as a direct result.
- **Install individual pressure regulators and manifolds/collectors per plumbing line** — equalizes water pressure across fixtures and allows isolated shut-off per fixture without cutting water to the whole apartment.
- **Install reverse check valves on hot/cold supply manifolds** — prevents backflow and cross-contamination between the hot and cold supply lines.
- **Install dry siphon traps on washing machine and dishwasher drain lines** — prevents sewer gas odors from migrating back up through appliance drain connections when the appliance isn't running.
- **Install motorized leak-protection servo shutoff valves**, particularly on towel-warmer/heated-rail supply loops — towel warmer pipe leaks are cited as a disproportionately common source of major water damage; an automatic servo shutoff limits exposure if a leak occurs while nobody's home.
- **A heated towel rail (hydronic/water type) is a functional necessity in a bathroom, not just a comfort item** — it's the heat source that lets post-shower humidity properly evacuate via ventilation; skipping a bathroom heat source is described as inviting mold risk over time. Choose a reputable manufacturer specifically to reduce long-term leak risk — the same logic and caution already noted for towel-warmer leak protection above.

## 6. Cost Drivers & Common Mistakes

- **The visible price gap between a surface-mounted and a built-in (behind-the-wall) plumbing fixture is commonly much smaller than the real installed-cost gap** once pipework, fittings, sleeves, and labor are counted — comparing device sticker price alone significantly understates what a built-in install actually costs. Price the full installation, not just the fixture, before deciding between the two.
- **Do not over-engineer plumbing cabinets** with multi-tiered manifolds, extra bypasses, and cosmetic LED backlighting — this inflates plumbing hardware budgets substantially without functional benefit; a simpler, adequately-protected setup (filters, regulator, leak protection — see §5) covers the actual risk without the extra spend.
- **Do not bypass main water shutoff valves during plumbing modifications** — carries a severe leak/flooding risk that isn't worth the time saved.

## 7. Buying / Practical Guidance

- **Price rough plumbing work by fixture "points," not by linear meters of pipe** — a sink needs 2 points (hot + cold), for example; pricing by pipe length is a known vector for "turns out we needed more pipe, please pay more" upselling. A points-based quote, cross-checked against the design project's fixture count, is much harder to inflate after work starts. *(See the general version of this smeta-literacy principle in [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] §4, which applies the same logic to electrical rough-in.)*

## 8. Quick Reference — Do's and Don'ts

### Do's

| Rule | Applies To | Reason | Source |
| :--- | :--- | :--- | :--- |
| Apply continuous hydro-isolation in shower zones and wet floors | Bathroom, WC | Prevent moisture seepage and damage to subfloor/neighbors | `90_Archive/processed_sources/20260727_vid1_transcript_d04723c5.txt` |
| Install coarse and fine main line water filters inside plumbing collector cabinet | Bathroom, WC, Kitchen | Protects faucets, shower valves, and appliances from pipe debris | `90_Archive/processed_sources/20260727_renovation_tips_video_f23c504a.txt` |
| Install individual pressure regulators and manifolds for plumbing lines | Bathroom, WC, Kitchen | Equalizes water pressure and enables isolated shut-off per fixture | `90_Archive/processed_sources/20260727_renovation_tips_video_f23c504a.txt` |
| Install reverse check valves on cold and hot water supply manifolds | Bathroom, WC, Kitchen | Prevents backflow and cross-over between hot and cold water supplies | `90_Archive/processed_sources/20260727_renovation_mistakes_video_21ade3f6.txt` |
| Install dry siphon traps for washing machine and dishwasher drain lines | Laundry Room, Kitchen | Prevents sewer gas odors from backing up through appliance drain lines | `90_Archive/processed_sources/20260727_renovation_guide_mistakes_3_a0e895b1.txt` |
| Perform detector scanning on raw floor screeds before chasing or drilling | Floor Screeds, Heating Zones | Prevents accidental cutting or puncturing of concealed PEX radiator/heating lines | `90_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e.txt` |
| Install motorized leak-protection servo shutoff valves on towel warmer supply loops | Bathroom | Prevents major water damage caused by towel warmer pipe leaks | `90_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e.txt` |
| Place the toilet first when laying out a bathroom, as close to the riser as practical | Bathroom, WC | Its 100mm drain pipe is the hardest to conceal; other fixtures should plan around it | `90_Archive/processed_sources/20260731_doma_minska_severny_bereg_ep2_layout_3e31aa05.txt` |
| Place a relocated sink along a wall, not mid-room | Kitchen, Bathroom | Preserves the drain's required gravity slope without excess screed depth | `90_Archive/processed_sources/20260731_doma_minska_severny_bereg_ep2_layout_3e31aa05.txt` |
| Install a heated towel rail (hydronic) from a reputable manufacturer | Bathroom | Manages post-shower humidity via ventilation, reducing mold risk; reduces long-term leak risk | `90_Archive/processed_sources/20260731_doma_minska_severny_bereg_ep2_layout_3e31aa05.txt` |
| Install a flush pre-filter even if it seems skippable | Bathroom, WC | Prevents sediment jamming a wall-hung toilet's cistern float mechanism, especially after extended water shutoffs | `90_Archive/processed_sources/20260731_borodaty_prorab_moscow_business_class_70000a9f.txt` |
| Price rough plumbing by fixture "points," not pipe length | Bathroom, WC, Kitchen | Closes off a common "we needed more pipe, pay extra" upsell pattern | `90_Archive/processed_sources/20260731_remonthochu_smeta_methodology_7d91eb29.txt` |

### Don'ts

| Rule | Applies To | Risk | Source |
| :--- | :--- | :--- | :--- |
| Do not bypass main water shutoff valves during plumbing modifications | Bathroom, WC, Kitchen | Severe leak and flooding risk | `90_Archive/processed_sources/20260727_vid1_transcript_d04723c5.txt` |
| Do not over-engineer plumbing cabinets with multi-tiered manifolds, extra bypasses, and LED backlighting | Bathroom, WC | Inflates plumbing hardware budgets massively without functional benefit | `90_Archive/processed_sources/20260727_renovation_guide_mistakes_a8e90887.txt` |
| Do not assume a plumbing cladding box's sewage stack can be relocated just because the box itself can be rebuilt | Bathroom, WC, Kitchen | The stack runs as one vertical column and generally cannot be moved, even though the cladding box around it can be rebuilt more compactly | `90_Archive/processed_sources/20260731_doma_minska_severny_bereg_ep2_layout_3e31aa05.txt` |
| Do not compare a built-in vs. surface-mounted fixture by device price alone | Bathroom, Kitchen | The real installed-cost gap (pipework, fittings, sleeves, labor) is commonly much larger than the visible device-price gap | `90_Archive/processed_sources/20260730_witalt_budget_tiers_moscow_68264373.txt` |

## 9. Source Notes

- **Toilet-first sequencing, sink-drainage-slope rule, heated towel rail, the zashivka/venshakhta distinction** (Дома Минска Episode 2, designer interview, Minsk-region) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_QHl1YEHMfgE_doma_minska_severny_bereg_ep2_layout|full extraction note]].
- **Flush pre-filter failure anecdote** (Бородатый Прораб, Moscow) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_OrKB6uSKRyk_borodaty_prorab_moscow_business_class|full extraction note]].
- **Price-by-fixture-points rule** (РемонтХочу, Moscow) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cdNwbqsLUK4_remonthochu_smeta_methodology|full extraction note]].
- **Built-in vs. surface-mounted cost-gap** (WITALT, region-unresolved secondary reference) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_BMmPLHVmnqw_renovation_budgeting_interview|full extraction note]].
- Pre-existing Do's/Don'ts rows sourced from earlier archived transcripts — see individual table cells above for paths.
