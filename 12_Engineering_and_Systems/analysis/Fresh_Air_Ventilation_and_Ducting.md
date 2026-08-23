# HVAC — Fresh-Air Ventilation & Ducting

Covers breathers vs. full mechanical ventilation, the shared-shaft constraint kitchen hoods also run into, supply-ventilation contracting, and duct sizing/soundproofing. Part of [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]].

Prolife Invest's dated Moscow comparison puts a full ducted supply-and-exhaust ventilation system at **1.5–10 million RUB** as of 2026-07-29. Using the trailing six-month USD/RUB average of 76.4100, `1,500,000 ÷ 76.4100 = $19,630.94` and `10,000,000 ÷ 76.4100 = $130,872.92`, presented at a price-range precision close to the original figures as **$20,000–$130,000**. The same source gives a breather figure rendered as “1,350” without a confirmed unit; that number is **not computable** and is not converted. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_DsdLa87Acz4_prolife_invest_moscow_flipping|extraction note]]]

## Breathers vs. Full Mechanical Systems

A separate decision from AC sizing. One practitioner's framing, worth treating as a reasonable starting heuristic rather than settled fact:

- A **wall-mounted "breather" unit** (a local fresh-air intake/filter device) is reported to handle the majority of typical indoor air-quality needs at a fraction of the cost of a full system.
Prolife Invest recommends: **full ducted supply-and-exhaust mechanical ventilation** is framed as worth the added cost mainly in specific situations — e.g. an apartment on a loud arterial road where windows realistically can't be opened for fresh air.
- The practical recommendation: default to breathers unless there's a specific reason (noise, air quality, a strong personal preference) pushing toward a full system, since most people reportedly don't perceive a meaningful difference in day-to-day comfort.

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
