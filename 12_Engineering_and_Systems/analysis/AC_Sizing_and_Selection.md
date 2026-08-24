# HVAC — AC Sizing & Selection

Part of [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]].

**USD normalization for the dated BURO AC-system comparison:** using the metadata-confirmed 2026-03-12 source date and trailing 6-month USD/RUB average of 79.39, the 200,000 RUB economy split-system example is ≈$2,500; 500,000–700,000 RUB good-quality split systems are ≈$6,300–$8,800; 1,000,000–3,000,000 RUB concealed/ducted systems are ≈$12,600–$37,800; and 1,500,000–5,000,000 RUB integrated supply/exhaust cooling is ≈$18,900–$63,000. The 5,000–50,000 RUB/m² span is ≈$60–$630/m². [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_6Z7uH2_rXsw_buro_segment_pricing_2026|extraction note]]]

FLATART VIDEOS / Yuri Kokichev gives a **rough sizing rule of thumb** (explicitly caveated by the source as an *averaged* estimate, not a substitute for a real heat-load calculation): roughly **1 kW of cooling capacity per 10 m²** of room area, with the smallest commonly available unit size being 2 kW, plus a **~20% capacity buffer** as standard practice. Push capacity upward for rooms with strong sun exposure, extra heat-generating equipment, or rooms that share airflow with an adjoining open-plan space (e.g. a living-dining combo needs sizing for the combined area, not just its own footprint).

Zemsproekt / Zemstandart (Alexey Zemskov, with Sergey Saratov identified in the note) says **the kitchen-specific multiplier, added 2026-08-19, is**: apply the standard bedroom/kids-room formula above, then **multiply by 1.5×** for a kitchen — kitchens carry meaningfully more heat sources (appliances, cooking) than a same-area bedroom, and sizing with the unmultiplied formula runs the unit permanently near its capacity ceiling, causing premature failure. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_fSEPr5fpfPM_kitchen_stubouts_ac_fridge_niche_166|note]]]

## Budget vs. Premium Tiers

Described functionally, not by brand — several sources on this topic are self-promotional retailer/installer channels, so specific brand endorsements are treated as commercial opinion, not neutral fact:
- Functional cooling performance and air filtration are reported as broadly similar between budget and premium inverter units.
- What premium tiers reportedly add: lower noise/sound pressure, more self-diagnostic and safety systems (more relevant to service technicians than day-to-day occupants), and design/finish options (color choices beyond plain white).
- Reported warranty pattern: mainstream mid/premium brands commonly carry ~5-year bundled warranties (equipment + installation) when bought and installed through the same vendor; the cheapest no-name tier may carry a shorter (e.g. 1-year) equipment warranty even when installation warranty stays the same length.
- One installer's own framing: "you're paying mostly for design and quiet operation at the top end, not a different cooling result" — recorded as that source's opinion, not verified independently.

## Why "AC Budget" Alone Doesn't Mean Much Without Specifying the Approach

For the same 100 m² apartment, holding cooling function constant, one design studio gives a concrete illustration of just how wide the range is depending on *how* it's done, not just *what brand*:

| Approach | Total Cost (RUB) | Trade-off |
| :--- | :--- | :--- |
| Standard split-system units (budget/economy) | ≈200,000 | Visible indoor units, most affordable |
| Standard split-system units (good quality) | ≈500,000–700,000 | Visible indoor units, reliable |
| Concealed/ducted AC (same cooling function) | ≈1,000,000–3,000,000 | Hidden installation, same functional result |
| Full supply-and-exhaust ventilation with integrated cooling | ≈1,500,000–5,000,000 | Adds fresh-air ventilation on top of cooling |

That's roughly **5,000–50,000 RUB/m²** from this one system category alone — a source's own explicit illustration of why a bare "price per m²" figure is close to meaningless without knowing which of these was assumed. *(Secondary reference, single-source, 2026 — see [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_6Z7uH2_rXsw_buro_segment_pricing_2026|extraction note]] for the full context.)*

FLATART says: **filtration**: basic units include a washable coarse mesh filter (rinse, dry, reinsert); some add antibacterial/ionic filter inserts. Worth an honest expectation-setting note from the same source: a user is unlikely to *consciously notice* any difference from the added filter — any benefit is framed as subtle/subjective at best, not a dramatic, perceptible change.

### Economy vs. Premium, Quantified (added 2026-08-24, Round 4)

Konstantin Kruglov/Ontario (level 1 — Moscow named directly, presenter's own bedroom AC use case)
gives sharper, more numeric economy-vs-premium content than this page's existing qualitative
"Budget vs. Premium Tiers" section above, largely extending it but with one flagged tension:

- **Compressor and service life**: economy tier typically uses cheap, often-unbranded compressors
  rated **3–5 years**; premium tier uses named Japanese-manufacturer compressors — **Mitsubishi,
  Panasonic, Hitachi** — rated **10–15+ years**.
- **Indoor-unit noise, quantified**: economy **40–45 dB** (audible, sleep-disruptive); super-premium
  down to **19 dB**; premium outdoor units are also reported near-silent, unlike some economy
  outdoor units.
- **Operating temperature range**: economy typically down to only **≈−5°C** outdoor ambient;
  premium down to **≈−25°C** — extends usable heat-pump heating into the shoulder-season gap after
  central heating is switched off.
- **Control sophistication**: economy = basic remote, sometimes no shutoff timer; premium =
  geolocation-triggered auto-activation and smart-home/voice-assistant integration.
- **Inverter prevalence**: more common (by model count) in premium, but explicitly not an absolute
  rule — check the specific model either way.
- **⚠️ Filtration tension, not resolved**: this source claims filtration quality *does* differ
  meaningfully by tier (economy = basic mesh only; premium = HEPA/plasma/antibacterial stages) —
  in tension with FLATART's claim just above that filtration is broadly similar and any difference
  is barely noticeable. Both are single-account claims from self-interested installer channels;
  recorded as an open disagreement, not adjudicated.
- **Price points** (2025-08-29 exact-date USD/RUB rate 80.2918): economy set from **~25,000 RUB ≈
  $310**; premium over **100,000–200,000 RUB ≈ $1,200–$2,500** (unit/set price, installation
  inclusion unconfirmed — not directly comparable to the RUB/m² whole-system figures above without
  confirming installation is included on both sides).

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_WK-KLd2ssYY_kruglov_ac_economy_vs_premium|WK-KLd2ssYY]]]

### Four Base Functions, Sizing-to-BTU Mapping, and Maintenance (added 2026-08-24, Round 4)

Konstantin Kruglov/Ontario (level 1 — Moscow/Moscow-region pricing named directly):

- **Every AC has four base functions**: cooling; heating (standard units typically rated to
  **−10°C** outdoor ambient; a "winter package" add-on can extend some units to **−25°C** —
  a different mechanism than this page's tier-based −5°C/−25°C figures above, recorded separately,
  not reconciled); dehumidification ("dry" mode — room temperature stays roughly constant while
  humidity drops; source cites his own hometown Vladivostok's ~100% mid-summer humidity as the
  clearest use case); filtration (100% of units have at least a basic filter; pricier models add
  ionization).
- **Sizing formula mapped to retail BTU-class sizes** (operationalizes the existing 1kW/10m² rule
  above): up to 25 m² → "9" class; up to 35 m² → "12" class; 45–55 m² → "18" class; above that →
  "24" class. Same upward-adjustment factors apply (sun exposure, panoramic windows, ceilings
  above ~3 m — this source's own added ceiling-height threshold).
- **⚠️ Quantified inverter vs. on/off temperature-holding comparison, in tension with this page's
  "inverter is generally preferred" framing above**: an inverter unit set to 22°C holds roughly
  **21–23°C** (±1°C); an on/off unit set to 22°C can swing across roughly **20–25°C** (±4–5°C).
  **⚠️ Counter-intuitive durability claim**: on/off units are described as the *more* durable of
  the two — capable of running for decades with only cosmetic plastic yellowing as a typical
  failure mode and cheap repairs, while inverter units are more mechanically complex. Practical
  recommendation: **inverter for a bedroom** (precise holding matters for sleep comfort), **on/off
  is fine for a living room**. `single-account`, `unverified` — recorded as a nuance on the
  existing "inverter preferred" claim, not an override of it.
- **Maintenance**: no line-servicing needed for the first 2–3 years; annually thereafter, a
  technician cleans the heat exchangers and checks the refrigerant line for leaks. Owner-level
  filter cleaning: monthly. Standard equipment warranty: 1–2 years (this source's own company
  states a 3-year installation warranty — self-promotional, tagged as such).
- **Moscow installation pricing, 2025 summer** (2025-06-13 exact-date USD/RUB rate 79.0028): split-
  system install **20,000–25,000 RUB ≈ $250–$320/unit** (excludes rope-access/high-rise technician
  fees); ducted or multi-split install **from 45,000 RUB ≈ $570**.
- **Named-brand equipment price tiers, per set, Moscow market, 2025 summer**: **economy 25,000–
  45,000 RUB ≈ $320–$570** (Ballu, a name transcribed as "leха гри" — `ASR-uncertain` — and base-line
  Electrolux); **comfort 40,000–75,000 RUB ≈ $510–$950** (higher-line Electrolux, Gree, Energolux,
  LG, Mitsubishi Heavy); **premium 70,000–200,000 RUB ≈ $890–$2,500** (Daikin, Mitsubishi Electric,
  Hitachi, Toshiba, Panasonic) — the first full-unit named-brand price table this store has for AC
  equipment (the round's earlier `WK-KLd2ssYY` named only compressor manufacturers, not full units).

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]
