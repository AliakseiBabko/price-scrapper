# 🌬️ Kitchen Hood — How They Actually Work (and a Conflict With the Selected Model)

*Tags: #kitchen #ventilation #hood #research*

> [!IMPORTANT]
> **Read this before trusting the DHL555BL's rated 618 m³/h spec.** In a standard multi-unit apartment building, a hood set to extraction mode cannot pull air faster than the shared ventilation shaft/duct allows — regardless of the hood's own motor power. This is now corroborated across 5 independent sources below (§2), with a concrete sizing formula in §2.1. See §5 for what this means for the already-selected hood.

> [!NOTE]
> **Regulatory claim status**: several sources below discuss a Russian building-code restriction on connecting a hood to a shared ventilation shaft. **The user has explicitly confirmed they cannot verify this applies to their own location (Belarus) and it should be treated as an open question to research later, not a settled rule** — see §6 for the full, hedged writeup. Nothing in §6 should be read as "this applies here."

---

## 1. Sources

| # | Channel | Title | Published | Type |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Roman Che TV | "ВЫТЯЖКА на Кухню КАКУЮ ВЫБРАТЬ и КАК?" | 2021-03-05 | Independent consultant, explicitly non-sponsored |
| 2 | Мебель — это просто (Вячеслав Герасимов) | "Вытяжка на кухню. Часть 1. Как выбрать модель." | 2019-02-01 | Furniture assembler, independent (paid by install complexity, not hood sales — self-disclosed) |
| 3 | Мебель — это просто | "Часть 2. САМЫЕ ВАЖНЫЕ ПАРАМЕТРЫ: шум, производительность, мощность" | 2019-02-22 | Same channel, part 2 of 4 |
| 4 | Мебель — это просто | "Часть 3. МАТЕРИАЛЫ, ПОДКЛЮЧЕНИЕ, ПОЛЕЗНЫЕ СОВЕТЫ" | 2019-10-05 | Same channel, part 3 of 4 |
| 5 | Мебель — это просто | "Часть 4. Вытяжка и вентиляция. Все способы подключения" | 2020-01-22 | Same channel, part 4 of 4 |
| 6 | ЛенРемонт (Денис Сорокин) | "Какую вытяжку лучше выбрать для кухни? Отзыв директора ремонтной мастерской" | 2019-12-02 (title says "2022" — **discrepancy, YouTube metadata is more reliable, treated as 2019**) | Repair-shop owner's own channel — self-promotional (discount code, phone numbers, gift pitch) |
| 7 | Вентиляция для Вашего дома \| Argus | "Эти способы совмещения вентиляции и вытяжки УНИЧТОЖАТ вашу кухню" | 2024-09-27 | Ventilation-installation company's own channel — self-promotional (Telegram-bot consultation pitch) |

None of these sources name a region/city — all treated as general RU-market content, not scoped to Minsk/Belarus. Archive: `_Archive/processed_sources/20260731_roman_che_kitchen_hood_guide_a89bb70d.txt` (source 1), `..._hood_video_2_88d0e98b.txt` (2), `..._hood_video_3_ec2042f3.txt` (3), `..._hood_video_4_1368bd4b.txt` (4), `..._hood_video_5_54ec0a93.txt` (5), `..._hood_video_6_f9450975.txt` (6), `..._hood_video_7_a7501bb5.txt` (7).

**Reading the sources**: 2–5 are one continuous 4-part series from a furniture assembler who installs hoods but doesn't sell them (mild independence signal, self-disclosed in source 3). 6 and 7 are both installation-company channels with a lead-generation angle — their specific numeric claims are usable but weighted slightly lower where they conflict with the more careful/independent sources, and flagged explicitly where self-interest could shape the framing.

## 2. Core Mechanism: Duct/Shaft Capacity, Not Motor Rating, Caps Real Performance

**Now corroborated by 5 of the 7 sources** (1, 3, 4, 6, 7), independently and via different mechanisms — this is the single most load-bearing fact on this page:

- A hood set to **extraction mode ("отвод")** is physically capped by whatever is downstream of it. In a multi-unit building, that's the shared ventilation shaft — the same structure covered in [[12_Engineering_and_Systems/analysis/AC_Key_Concepts_and_Placement|HVAC: Key Concepts & Indoor Unit Placement]] (a "venshakhta," never to be structurally modified).
- **Standard ex-Soviet-bloc shafts are commonly cited around ~100–120 m³/h** (source 1) — but source 3 gives a materially more precise, diameter-dependent formula (§2.1 below) that puts a 100mm duct closer to ~180 m³/h. **These two figures conflict and are not reconciled here** — plausibly different shaft cross-sections, measurement methods, or just different real buildings; treat as a range (~100–180 m³/h for a typical 100mm connection) rather than a single number, and verify this apartment's actual shaft/duct size directly rather than assuming either figure.
- **An oversized hood on an undersized duct doesn't get you more airflow — it gets you more noise and can force air backward.** Source 3 explains the mechanism directly: air resonates against the too-small opening, and the motor works harder against resistance, generating more noise (analogized to a vacuum cleaner with a clogged hose). Source 6 (ЛенРемонт) independently names the failure mode **"опрокидывание тяги"** (draft reversal/backdraft) — a hood forcing more air than the shaft can carry can push air backward through the system, including potentially into a neighboring apartment's line. Source 7 (Argus) corroborates the undersized-duct-causes-noise mechanism independently, from a ventilation-installation (not furniture) background.
- **No hood works without makeup air ("приток")** — corroborated independently and near-identically by sources 4 and 5 (unrelated channels): if a kitchen has no dedicated fresh-air supply, a window needs to be cracked for the hood to actually extract air at all; poor real-world performance despite a "good" hood is very often explained by this, not a defective unit.

### 2.1 A Concrete Sizing Formula (source 3 — single-source, not yet cross-checked)

Source 3 gives a duct-diameter-to-capacity table, explicitly caveated by the source itself as approximate (varies with shaft roughness, blockage, and weather/pressure conditions):

| Duct/shaft diameter | Approx. throughput capacity |
| :--- | :--- |
| 100mm | ~180 m³/h |
| 130mm | ~300 m³/h |
| 150mm | ~400 m³/h |

**Recommended hood performance = shaft figure + ~50% margin** (source's own reasoning: the hood normally runs at speed 1–2, not max, so a 50% buffer over the duct's practical capacity gives comfortable headroom without meaningfully exceeding what the duct can carry). `single-account`, not corroborated by another source in this batch, but internally well-reasoned and comes with an explanation for *why*, not just an assertion — worth treating as the best available planning number until independently checked.

### 2.2 Manufacturer Capacity Specs Are Often Inflated (source 1 only — single-account)

Source 1 states RU-market hoods are commonly rated at **no-load ("холостой ход")** — free airflow with no duct/filter resistance — overstating real installed performance by roughly 2×, and that the EU market caps legally-sold hood ratings at 1,000 m³/h. **Not mentioned or corroborated by any of sources 2–7** — remains single-source. Source 3 (min-speed-not-max-speed heuristic, §3) and source 6 (backdraft from oversized dual-motor units) both independently support the general *spirit* of "don't trust a big headline capacity number," without directly confirming the specific 2× no-load-inflation claim.

## 3. Noise — Judge by Minimum Speed, Not Maximum

A genuinely new, independently actionable heuristic from source 3, not present in source 1:

- **Compare hoods by their noise level at minimum (speed 1) operation, not maximum.** A hood runs on speed 1 (occasionally 2) for the vast majority of its actual use; max speed is for unusual situations only. Worked example given: two hoods rated 58 dB and 64 dB at max speed look similar, but at minimum speed one measures 35 dB and the other 42 dB — "almost twice as quiet" despite the max-speed specs suggesting the reverse ranking.
- **Reference points**: quiet furnished apartment ambient ≈ 30–40 dB; normal speech ≈ 50–55 dB; an average hood at max speed ≈ 55–65 dB; a genuinely good/quiet hood at max speed ≈ 44–45 dB.
- **On budget hoods (≤5,000–6,000 RUB, 2019 pricing), don't bother comparing noise specs at all** — the source states these are commonly faked or simply omitted by manufacturers at this price tier.
- **A dirty/clogged grease filter degrades noise and is a real fire hazard, not just a performance issue.** Sources 2 and 6 corroborate independently: grease buildup near an open gas flame is a stated ignition risk (source 6), and running a hood with no filter at all is described as "categorically forbidden" since it destroys the fan motor quickly (source 2).

**Cross-check against the already-selected [[Bosch_DHL555BL_Hood]]**: its own catalog-scraped spec range is 38–56 dB (min–max). Its **38 dB minimum-speed figure is actually better than source 3's own "genuinely good hood" benchmark of 44–45 dB** — a positive data point for the existing selection on the metric this page argues actually matters, independent of the shaft-capacity question in §5.

## 4. A Widely-Repeated Sizing Formula Is Debunked (source 3)

Source 3 explicitly and mechanistically debunks a formula the source attributes to "fake YouTube experts": *kitchen floor area × ceiling height × an "air exchange norm" of 12 × a 1.6 "reserve coefficient."* Reasons given:

1. **Conflates power (watts) with performance/capacity (m³/h)** — different physical quantities.
2. **The 1.6 "reserve coefficient" is unsourced/arbitrary** and ignores duct length or diameter entirely — i.e., ignores exactly the constraint §2 above identifies as the real bottleneck.
3. **The "12x/hour" air-exchange figure is a sanitary norm for whole-room forced ventilation systems**, not applicable to a hood, whose actual job is localized extraction near the cooktop, not full-room air turnover.

Demonstrated with a smoke test: smoke near floor level clears, but smoke at ceiling height is essentially unaffected even after a simulated full "10x/hour" cycle — a hood barely captures air above its own installation height. Applying the debunked formula to a 30 m² / 3m-ceiling kitchen implies needing ~1,700 m³/h — "already an industrial-grade hood," illustrating how far off the formula runs. **Actionable conclusion: size a hood to the duct/shaft capacity (§2.1), not to room volume.**

## 5. ⚠️ Conflict / Cross-Check With the Already-Selected [[Bosch_DHL555BL_Hood]]

The DHL555BL's own model page cites its selling point as **dual-motor extraction up to 618 m³/h**, achieved via a wide smooth-walled duct into the ventilation shaft. Cross-referencing against everything above:

- If this apartment's shaft/duct connection is a standard ~100mm ex-Soviet-style connection, the two available capacity estimates (source 1: ~100–120 m³/h; source 3's formula: ~180 m³/h, or ~270 m³/h with the recommended +50% margin) both put **real achievable extraction well below the rated 618 m³/h** — anywhere from roughly a sixth to a third of the rated figure, depending on which estimate is closer to this apartment's actual shaft.
- **Positive finding**: the DHL555BL's 38 dB minimum-speed noise rating clears source 3's own bar for "genuinely good" (44–45 dB) — so the noise-comfort case for this hood holds up independently of the capacity question.
- Source 6's warning that dual-motor units marketed on "low noise + high power" can cause **опрокидывание тяги** (draft reversal/backdraft) if the duct can't carry the rated airflow is directly relevant to a dual-motor 618 m³/h unit specifically — worth confirming actual duct sizing before installation, not assuming the rated capacity is either achievable or safe to attempt to reach.

**Practical implication, unchanged from before but now better-supported**: confirm this apartment's actual shaft/duct diameter and realistic capacity before assuming the 618 m³/h figure is meaningful, and size the connecting ductwork per §2.1's formula (duct capacity + ~50% margin, not room volume) rather than trying to max out the hood's own rating.

## 6. Regulatory Claims — Russian-Sourced, Explicitly Unconfirmed for Belarus

> [!NOTE]
> **Per the user's own explicit guidance**: this section documents what these Russian-language sources claim about Russian building code, for future reference — **not as a rule known to apply in Belarus**. The user has said they cannot confirm this and it's a research item for later, not a settled fact. Nothing here should inform a purchase or installation decision until independently checked against Belarus's own code and (if applicable) the specific development's documentation.

Two of the seven sources address this, and **they disagree with each other in specificity and tone**:

- **Source 4 gives the more precise, carefully-hedged account**: natural ventilation preservation is described as **mandatory only when gas equipment is present** in the apartment, per (per the source's own citation) **SNiP clause 7.8.7, dated 2003**. The source explicitly states **no new law was passed in 2019** — only a fire-code enforcement amendment requiring compliance with the pre-existing 2003 clause to actually be checked/enforced. For an **electric** cooktop, the source frames natural-ventilation preservation as **explicitly optional**, not mandatory. What the rule is stated to actually forbid: **fully/permanently sealing the shaft opening**, framed as a gas-leak safety backstop — not a blanket ban on hood-to-shaft connections.
- **Source 6 (ЛенРемонт, self-promotional) gives a more alarmist, vaguer account**: cites a generic "СНиП и ГОСТ" (no specific clause), claims a 2019 law made having a gas cooktop + hood *together* outright illegal, cites a specific **2,500 RUB fine**, and claims annual gas-inspector visits can issue citations. This source has a direct incentive to frame improper installation as riskier (it sells correction/installation services) and is less precisely sourced than source 4 — **its account is weighted lower here**, but not discarded.
- **Neither source names Belarus, a Belarusian code, or any authority outside Russia.** Per this project's standing regulatory-evidence bar (used in `renovation_regulations_belarus_knowledge_store.md`), this content does **not** qualify for that stricter-bar store — it stays here, clearly flagged, as background context only.
- Source 4 separately cites a distinct Russian rule (**"Свод Правил... п. 7.3.2"**) about minimum distance (8m) between exterior air intakes and exhaust discharge points, plus facade-modification restrictions — relevant only if exterior venting on a multi-unit building's facade were ever considered, and equally unconfirmed for Belarus.

**If this becomes relevant later**: the concrete thing to check is whether Belarus's own construction code (СНБ) has an equivalent clause, and whether the specific apartment's gas-vs-electric cooktop status changes the answer per that code — not whether the Russian SNiP citation above is itself accurate (it appears reasonably well-sourced for Russia, per source 4).

## 7. Two Installation Modes — Extraction vs. Recirculation

| Mode | How it works | Reliability in an apartment building |
| :--- | :--- | :--- |
| **Extraction ("отвод")** | Vents collected air out through ducting into the shared shaft | Capped by shaft/duct capacity (§2) regardless of hood rating |
| **Recirculation ("рециркуляция")** | Passes air through a carbon filter, returns cleaned air to the room | Functionally reliable regardless of shaft condition, but doesn't remove humidity and needs a periodic filter |

- **Filter lifespan is shorter and more variable than a generic "periodic replacement" implies**: source 2 states carbon filter life can range from a few days to a few weeks depending on filter type and usage intensity — materially shorter than the impression a generic yearly-ish replacement cadence might give. **For a recirculation setup, prioritize filter availability and lifetime cost over brand** (source 1) — check the specific model's filter price and service life before buying; a pricier, longer-lived filter can be cheaper per year than a cheaper, shorter-lived one.
- **Don't combine a carbon filter with a working shaft connection** — source 2 states a carbon filter should only be used when extraction isn't possible at all; adding one on a ducted hood just adds resistance and degrades extraction performance for no benefit.
- **Regenerable carbon filters exist** (source 1): a 10–12 year-lifespan filter (~100–250 EUR) that gets burned clean in an oven every 2–3 months instead of replacement — roughly cost-equivalent over a decade to ~15–20 disposable filters, trading money for recurring maintenance effort.
- **If running recirculation-only, don't go below 250 m³/h rated capacity** (source 2) — carbon filters add resistance, and weak units underperform even for the more limited recirculation job.

## 8. Ducting: Material, Diameter, and Fitting Choices (source 4 — richest single source on this topic)

- **Connection sizing rule**: the hood's flange diameter should equal or be smaller than the duct/shaft diameter — never force a larger flange into a smaller duct (demoed audibly noisier in the source). Don't narrow the duct for no reason even when flange and shaft already match.
- **Material comparison**:
  - **Corrugated/flexible duct ("гофра")** — cheapest, quick to install. Aluminum variants crush/tear easily and **must never be routed behind a drywall ceiling** (snags on the metal frame, can tear or detach from the flange, essentially unfixable once installed). Polyester corrugated is more durable but audibly rustles. **Stainless steel corrugated** is recommended as the best corrugated option (durable, cleanable) but has sharp edges and needs screws/sealant rather than hose clamps; cited at ~1,000 RUB/meter for 100mm (2019 pricing, historical).
  - **Rigid plastic ducting (round or rectangular)** — generally recommended as optimal. Round diameters 100/125/150mm; rectangular equivalents roughly 120×60mm ≈ 100mm round, 220×90mm ≈ 150mm round. **Round is preferred over rectangular/flat** — stiffer, quieter, tighter joints; flat only worth using where clearance is genuinely tight (e.g. no cornice space).
  - A 110mm sewer pipe is sometimes substituted for 100mm round duct — functionally fine, just aesthetically a "sewer pipe on the wall" if left visible.
- **Noisiest fittings, named explicitly**: pyramid transitions (flange-to-duct size changes), vertical right-angle elbows, and round-to-flat transitions. If a round-to-flat transition is unavoidable, place it high up rather than right at the hood ("the higher the noise source, the quieter it seems"). **Prefer two 45° elbows over one 90° elbow** — smoother bend, less noise, and useful for correcting minor duct/hood misalignment.
- **Diameter tension, not resolved**: sources 2–4 consistently work in the 100/125/150mm range for hood ducting; **source 7 (Argus) recommends 16–20cm (160–200mm)** for proper sizing, calling smaller diameters a common installer mistake. Not necessarily contradictory (could describe a different duct segment or a more conservative sizing philosophy from a specialist installer), but a real numeric tension — worth confirming actual planned duct diameter against both ranges before finalizing.
- **Jointing tips**: dry-fit the whole run before sealing anything (so it can still be disassembled later); round-duct joints usually don't need sealant (tight fit by design), flat ducts always do (silicone); "Момент Монтаж" construction adhesive works for permanent joins. The factory flap/butterfly valve at the hood's own flange can be removed as unnecessary noise; if backdraft is a concern, install a **separate check valve at the shaft entry** instead (see §9) — and note it needs periodic cleaning/servicing or it clogs with grease and stops working.
- **Vibration**: pad ducting where it passes through cabinetry/shelving with foam/sealing tape to reduce transmitted vibration noise. Automotive sound-deadening wrap on ducts is judged not worth the cost/effort for the marginal benefit.

## 9. Preserving Natural Ventilation While Adding a Hood — Method Inventory

Source 4 gives five methods (framed around the Russia-specific gas/SNiP question in §6, but the underlying techniques are general engineering, not regulation-dependent):

1. **Recirculation-only** — simplest, shaft stays fully open, but carbon-filter extraction is inherently less effective than true extraction.
2. **Vent directly outside** — cited as largely infeasible/illegal on a standard Russian apartment building facade (exterior walls aren't private property, an 8m intake-clearance rule applies per source 4's own citation); more realistic for a private house.
3. **Special flange with a built-in grille/backdraft damper** at the shaft opening — low-maintenance beyond periodic cleaning, but limited to shaft openings that physically accept this flange type.
4. **Tee fitting + separate check valve** — the most universal method for irregular openings. **Independently corroborated by 3 sources**: source 4 gives detailed DIY install notes (shorten the valve body, angle it slightly toward the opening, avoid a full-seat position that could stick the flap open, use construction adhesive as a gasket; names Ukrainian brand "Вентс" as a notably better-quality check valve than most); source 5 (ЛенРемонт) independently describes the same spring/weighted-flap mechanism; source 6 (Argus) independently describes essentially the same two-valve strategy (a factory valve on the hood branch plus a second, separately-installed check valve on the natural-vent branch, oriented to open only toward the shaft) — a clean cross-corroboration from three unrelated professional backgrounds (furniture assembly, repair shop, ventilation installer).
5. **Physically divide the shaft/duct** during renovation into two channels (natural ventilation + hood) — described as achievable with a custom-formed tee (~160mm reducing to 125mm for the hood branch, ~20% narrowing accepted as a tradeoff) or costlier custom metalwork.

**A distinct DIY noise-reduction technique from source 7 (Argus)**, not mentioned elsewhere: remove the hood's own stock fan (voids warranty) and install a separate quiet in-line/canal fan positioned near the shaft entry (not at the hood canopy) with an inline muffler, wired to the original hood's switch. Claimed to produce near-silent operation. `single-account`, commercial context (pitched as a service this installer offers), but mechanically plausible and well-specified enough to record.

## 10. Shaft Architecture and the "Neighbor Odor" Question

- **Most multi-story buildings use a "satellite duct" ("спутник") design**: one large collector shaft runs the full building height; each floor's apartment connects via a smaller branch duct, sealed against sideways leakage into a neighboring floor's branch by a cement plug. Source 4 frames cross-apartment odor complaints as usually caused by these plugs degrading with age, being damaged during a neighbor's own renovation, or never installed correctly — a building-management responsibility, not inherently a resident-vs-resident conflict.
- **If the shaft/plugs are in good condition, a properly-sized hood does not meaningfully bother neighbors** — source 3 states this as a general claim and backs it with a personal example (his own 650 m³/h hood, one floor above a neighbor, no reported complaints). Source 6 nuances this with the specific failure mode: it's **draft reversal (опрокидывание тяги)** from an oversized/mis-ducted unit, not simply "a powerful hood," that causes cross-apartment odor transfer — consistent with, and more mechanistic than, source 3's claim.
- **Mold/mildew from a hood is described as a myth in most cases** (source 4) except: (1) a hood installed but never actually used, trapping moisture; (2) an apartment that's never ventilated (windows never opened); (3) pre-existing ambient humidity unrelated to the hood (e.g. a damp building basement).
- **Modern airtight windows/doors have removed the passive infiltration older Soviet-era wood windows provided** — both source 4 and source 5 make this point independently, meaning mechanical ventilation/window-cracking is now often necessary where it wasn't in an older building with leakier original windows.

## 11. Hood Types (corroborated across sources 1, 2, 6)

Consistent taxonomy across sources: **canopy/козырьковые** (cheap, exposed, noisy — Soviet-era default); **built-in/встраиваемые** (good for small kitchens); **wall-mounted/настенные** (classic, dome/купольные, flat T-shaped, inclined); **corner/угловые**; **island/островные** (ceiling-mounted, needs pre-planned ducting + reinforced ceiling backing); **worktop/wall-integrated** (expensive, needs non-standard cabinetry, must be planned at the renovation-design stage, not after); **cooktop-integrated (downdraft)**; and fully hidden "invisible" units (source 2 names German brand GUTMANN specifically as an example of this category, noting these high-power units **cannot be connected to shared building ventilation due to their power** — a concrete, brand-specific instance of the §2 capacity-cap principle).

**Mounting height**: source 2 gives a clean, internally-consistent figure — **650mm above an electric cooktop, 750mm above gas**. Source 5 (ЛенРемонт) gives conflicting, ASR-degraded figures (60–80cm range, inconsistently stated for inclined vs. straight hoods) — **treated as unreliable and superseded by source 2's cleaner numbers**. Inclined hoods have inherently weaker capture due to their shape and are sometimes mounted lower (350–400mm) — flagged by source 2 itself as looking impractical/oversized at that height.

## 12. Price-Tier Guidance (RUB, 2019–2021 pricing — historical, not directly usable for current budgeting)

Source 1's three-tier framing (2021): budget hoods (up to ~150,000 RUB — likely a thousands-RUB figure per that source's own convention, treat with the same unit caution as other RUB figures in this knowledge base) are largely decorative/"checkbox" purchases; mid-tier (~150,000–300,000) genuine design elements with moderate real performance; premium (300,000+) capable of meaningfully cleaning air, **but only if venting conditions actually support it** (§2). **If you can't vent outside and have no booster fan, the source's own stated ceiling on what's worth paying is ~25,000–30,000 RUB** — above that, in a shaft-constrained apartment, you're paying for design/status, not additional real airflow. Source 6 gives only a floor price (basic canopy hoods "from 1.5 thousand RUB," 2019) — not a comparable ceiling figure, and doesn't corroborate or contradict source 1's ceiling claim. **The price-ceiling claim remains single-source.**

## 13. A Single-Source, Self-Undermining Anecdote Worth Flagging

Source 6 (ЛенРемонт's own owner) discloses running **no hood at all in his own home for 5 years** as a deliberate experiment, reporting no meaningful grease buildup, and argues hoods are largely a "marketing tool" — while simultaneously disclosing his own business profits from hood repairs ("it's in my interest that everyone buys hoods"). This is an unusually candid, self-undermining claim from a source with a commercial incentive to say the opposite — worth recording as a genuine data point, but it's a single anecdote from one household, not corroborated by any other source in this batch (which otherwise consistently treat hoods as functionally useful when correctly sized/installed), and should not be read as a general recommendation against installing one.

## 14. What to Check for This Kitchen Before Finalizing the Hood Decision

- [ ] Confirm this apartment's actual shaft/duct diameter and realistic throughput — the two available formulas (§2, §2.1) disagree by nearly 2×, and neither has been checked against this specific building.
- [ ] Size the connecting ductwork using §2.1's diameter-to-capacity table (+ ~50% margin), not room volume — and note the diameter tension in §8 (100-150mm per most sources vs. 160-200mm per Argus) before finalizing duct spec.
- [ ] Re-confirm the DHL555BL's real EU-market rated capacity against its RU/local listing, given source 1's (single-source, unconfirmed) claim that RU-market figures can be inflated ~2x versus EU no-load measurement differences.
- [ ] Check whether a tee + check-valve setup (§9, method 4) is needed to preserve natural kitchen ventilation, independent of whatever the eventual regulatory answer turns out to be (§6) — it's good practice regardless of which code applies.
- [ ] Treat §6's regulatory content as background only, per the user's own instruction — resolve Belarus applicability separately before it affects any decision.

## 15. See Also

- [[Kitchen_Hoods]] — the full researched candidate comparison table (price/spec) this analysis complements.
- [[Bosch_DHL555BL_Hood]] — the currently-selected model; see its own "Ducting Requirement" concern, which §5 above directly extends.
- [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]] — general ventilation-shaft rules (the "venshakhta" — never structurally modify it) this hood-specific mechanism builds on.
