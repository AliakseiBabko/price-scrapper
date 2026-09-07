# Plumbing — Pipe Material Selection

Covers PEX vs. polypropylene vs. metal-plastic, manifold-node material, the riser-to-shutoff segment, and a common PEX press-fitting mistake. Part of [[12_Engineering_and_Systems/Plumbing_and_Waterproofing|Plumbing & Waterproofing]].

## Pipe Material Selection

- Konstantin Kruglov/Ontario explains: **PEX (cross-linked polyethylene, "сшитый полиэтилен") is now used in ~95% of plumbing rough-in work**, per one source — named brands include Rehau, Stout, and Uponor, among many other EU/Chinese-market brands. Its decisive structural advantage: a PEX run from manifold to fixture is **one continuous pipe with zero hidden internal joints** — no couplings buried under plaster, screed, or tile. It's also described as low-skill-tolerant (the source claims even an untrained person can learn to press-fit it correctly).
- Konstantin Kruglov/Ontario contrasts: **Reinforced polypropylene** (soldered/welded joints) was the standard before PEX and remains viable, but has one real advantage left: it's cheaper. Its joints, unlike PEX's, do get buried under plaster/screed/tile — a hidden failure point PEX avoids entirely.
- Konstantin Kruglov/Ontario warns: **Metal-plastic pipe (металлопласт) is explicitly described as obsolete** by one source — "don't even consider it," not used by that company in ~10 years.
- Konstantin Kruglov/Ontario recommends: **Match the manifold node's own internal plumbing material to the downstream distribution material**: use polypropylene internally only if the whole downstream run is polypropylene; PEX internally only if downstream is PEX. **Stainless steel is the more robust choice specifically for the manifold node itself** (where many device-to-device joints exist, unlike an open PEX run's two joints total) — its cost premium over PEX is described as "not large," and it tolerates high temperature and pressure spikes well. The stated system-design principle: **the whole system is only as strong as its weakest joint** — running stainless steel throughout the entire apartment is considered unjustified overkill (expensive, and stainless joints buried in walls are undesirable when continuous PEX can avoid joints entirely). `single-account`, but internally well-reasoned.
- Konstantin Kruglov/Ontario advises: **After a stainless-steel manifold-node installation, do a visual leak check daily for the first 2–3 weeks** — stainless fittings can loosen slightly from vibration early on; after that settling period, rely on the leak-detection system's own sensor under the manifold instead.

## ⚠️ Independent Corroboration of the Stainless-Node / PEX-Distribution Split, With Sizes (Vasily_Sanuzel, 2023-10-07 and 2024-05-10)

Василий (Vasily_Sanuzel) builds exactly the division Kruglov argues for above, on two separate jobs, without referencing anyone: **stainless-steel press-fit tube for the node's device-to-device connections, PEX for the runs out to the fixtures.** Two independent practitioners arriving at the same split is stronger than either account alone.

- **His stated reason for stainless at the node** adds one Kruglov does not give: **a larger internal bore for a given outside diameter** than the alternatives — plus longevity and appearance. Press-fitted onto an O-ring inside the fitting and crimped with a matched die.
- **Distribution in PEX with a sliding sleeve** («сшитый полиэтилен, надвижная гильза»), **16 mm as standard and 20 mm for the shower system** — a concrete sizing rule this page did not carry.
- **⚠️ A clash detail worth knowing before assembly: the filter bowls had to be taken off to get the press tool in**, then refitted. Crimping needs swing room the drawn layout will not show.

[source: [[_Sources/YT_M8EyOCrm0tw_sanuzel_water_inlet_unit_assembly|YT_M8EyOCrm0tw]], [[_Sources/YT_z0hcMY5PYoc_sanuzel_pik_cabin_prep_works|YT_z0hcMY5PYoc]]]

## PEX Insulation vs. Conduit Rule (added 2026-08-24, Round 2)

Konstantin Kruglov / Ontario, real Moscow jobsite, says: **if routing PEX pipe without a manufacturer-approved corrugated conduit, use at least 4mm-thick thermal insulation instead.** A developer-installed heating pipe on this jobsite used corrugated conduit without insulation — noted as possibly acceptable under that specific pipe manufacturer's own approval, and more damage-resistant, but **not a general recommendation for self-installed PEX: if you install the pipe yourself, use insulation; using conduit instead is specifically a developer choice, not a rule to copy.** [source: [[_Sources/YT_QcYJwQgu67g_kruglov_perfect_plumbing_mistakes|QcYJwQgu67g_kruglov_perfect_plumbing_mistakes]]]

## ⚠️ Manufacturers' Own Answers — Low-Noise Soil Pipe, Axial PEX, and Why Pipes Burst Now (four exhibitors via Vasily_Sanuzel, 2024-06-03)

**⚠️ Every claim in this section comes from a vendor's own representative about that vendor's own product**, collected by Василий (Vasily_Sanuzel) at a plumbers' trade meet-up from subscriber questions. Read with the tier-steering filter on. Two answers are mechanism-level and are marked as such; the figures are `vendor claim`.

**Why low-noise ("white") soil pipe is quieter — the mechanism, not the marketing.** Ostendorf's technical specialist: «никаких нанотехнологий». It is **wall thickness plus density**:

- **Wall thickness comparable to SML cast iron — 5.3 mm on DN110 — and the fittings carry the same thickness as the barrel**, not just the pipe.
- **Mineralised, higher-density polypropylene**: mineral additives raise stiffness and density, so an identical nominal wall is heavier and stiffer than a lookalike. **Stiffness class SN16**, which he says exceeds even the external KG2000 system, specified for indoor use precisely to guarantee the acoustic result.

**⚠️ Cast iron to plastic without adapters**: the SN system **matches SML's outside diameter**, so a jointless («безраструбный») cast-iron stack is converted by cutting, butting the plastic against the iron, and closing it with **the wide CV clamp already sold in the cast-iron range**. He calls it «одна-единственная альтернатива» to SML — `vendor claim` on exclusivity, but the dimensional compatibility is checkable.

**⚠️ Axial PEX: the bend left by the coil does not matter, under stated conditions.** Elson's representative, on the observation that a pressed axial joint sits slightly off-axis: **provided the cut is square (90°) and clean, with no burrs or nicks, and the sleeve is drawn correctly, the residual bend «не влияет на соединение никак»** — «если вы сделали опрессовку, это навсегда». A checkable condition rather than reassurance.

**⚠️ Euroconus across manufacturers — and the real reason for the mono-brand rule.** Mixing «теоретически… в умелых руках, скорее всего, будет работать». The recommendation to stay single-brand is then justified **by the warranty: they warrant the joint for 5 years, and only on their own complete assembly.** Recording it as **a liability boundary rather than a physical incompatibility** is what makes it usable — it tells you what you are actually giving up.

**PP versus PEX, from a manufacturer's mouth** — corroborates this page's existing case: PP comes in sticks up to 4 m so **every turn is another welded fitting**, against PEX's **two connection points** manifold-to-fixture; cross-linking gives memory and better tolerance of temperature and pressure loading; **both need fixing, PP more of it.** Василий draws the conclusion aloud — more joints, more chances to get one wrong — and it is not contradicted.

**⚠️ Why pipes burst now, and it reframes the risk.** Two causes given: **operating parameters exceeded** — PEX takes **18–20 bar** short-term, essentially unreachable domestically, and «если системы собраны правильно, это должно быть исключено» by the safety fittings — or, far more commonly, **mechanical damage by another trade after the pipes are laid**: «заходят бригады, там плиточники или ещё кто-то, и кто-то нечаянно уронил молоток, просверлил или порез сделал». Василий's own framing, offered and not contradicted: a burst pipe is «мнение из прошлого», from **steel corroding at the cut thread where the wall is thinnest**. → **The modern risk is a trade sequencing and protection problem, not a material problem.**

**Flash/seam («облой») as an acceptance criterion**: it arises on **injection-moulded fittings**, and the manufacturer's own position is that **it is a defect they must control**, because a professional installer should not be spending time trimming it. Keep the criterion, discount the percentage.

[source: [[_Sources/YT_LDeNqQL7TLQ_sanuzel_plumbers_meetup_manufacturer_qa|YT_LDeNqQL7TLQ]]]

## Polypropylene's Joint-Narrowing Defect, With a Real Demonstration (added 2026-08-19)

> [!NOTE]
> A second, independent source reinforcing the polypropylene-vs-PEX preference above with a specific visual mechanism. [source: [[_Sources/YT_1_IcoSaNKP4_multitrade_qc_tour_049|note]]]

Zemstandart/Alexey Zemskov recommends: **Every polypropylene weld/fusion joint measurably narrows the pipe's internal diameter** — visible when a real joint is cut open crosswise, not just marketing caution. Online demonstrations claiming polypropylene has "no narrowing" typically only cut *along* the pipe's length, never through an actual joint, which is exactly where the defect shows. Push-fit/PEX-style fittings avoid this failure mode entirely by design.

> [!NOTE]
> **First cross-channel corroboration (added 2026-08-24)**: RemProektMD (Chișinău/Moldova, unrelated to Zemstandart) independently demonstrates the same joint-narrowing defect on camera, cutting open both a good and a deliberately poor-quality polypropylene joint side by side, and adds a stated real-world consequence — a narrowed joint can measurably reduce delivered water pressure at downstream fixtures. [source: [[_Sources/YT_2fLCiWU6U-I_remproektmd_pipe_replacement|2fLCiWU6U-I]]]

RemProektMD (Andrei/Stanislav) adds a **human-factor mechanism for why polypropylene joint failure is delayed and hard to predict**: joint quality depends heavily on installer technique (heating duration/consistency during welding), a poor joint is often not visually detectable at installation time, and can hold for years before failing suddenly — described as "a delayed-action bomb." This explains why a passing pressure test at handover doesn't guarantee long-term joint integrity, illustrated with a real case: a new-build client declined pipe replacement, passed a pressure test, and later had a joint leak under bathroom tile (found quickly by luck) — the same failure under parquet/engineered flooring would be far harder to locate and repair. [source: [[_Sources/YT_2fLCiWU6U-I_remproektmd_pipe_replacement|2fLCiWU6U-I]]]

RemProektMD describes the **Rehau PEX press-fit installation sequence**: slide the crimp ring onto the pipe, expand the pipe end with an expansion tool, insert the fitting, compress the ring — the fitting's internal diameter matches the pipe's own bore exactly (no narrowing regardless of installer skill), independently corroborating the existing Kruglov/Ontario "low-skill-tolerant" claim above from an unrelated channel. [source: [[_Sources/YT_2fLCiWU6U-I_remproektmd_pipe_replacement|2fLCiWU6U-I]]]

Zemsremont/Zemstandart demonstrates: **Push-fit fitting technique, a specific detail not covered above**: expand the pipe end with the expansion tool **twice** — the first pass to a standard 90° circular expansion (so the second, correctly-oriented pass doesn't risk inserting the tool the wrong way and causing a later leak) — then insert the fitting immediately, before the expanded end starts contracting again. **Tool-rental economics for a DIY installer**: the expansion tool rents for **~500-1,000 RUB/day** wherever pipe/fittings are sold — a full apartment's rough-plumbing job needs at most 2-3 days even for a first-timer (~1,500-3,000 RUB total, 2019 pricing, `unverified`), trivial against the cost of a flood from a bad joint.

## The Riser-to-Shutoff Segment — a Special Case

Стройплощадка × Будни сантехника explains: **The segment between the riser and the main shutoff valve is governed by the building's own infrastructure, not installer preference.** One source, working on a low floor of a 23-story high-rise with an unusually high measured riser pressure (11 atm, from ~7 atm of static column height alone plus the required minimum pressure at the top floor), built that specific segment in **welded steel pipe**, bent with a pipe bender — steel tolerates any pressure or temperature the shared riser might see. In a low-rise building with normal pressure, the same segment could reasonably use threaded fitting + an approved polymer pipe instead. The underlying rule: **this segment is legally part of the building's shared riser infrastructure** (per the building's own project documentation) and can only be serviced by the building's own plumber — so it must use whatever material that documentation specifies, not whatever the apartment's own contractor prefers. Substituting plastic into a shared steel heating riser (e.g., to hang a radiator) is called explicitly against code, though "many people in the regions do it anyway."

## A Common PEX Press-Fitting Mistake

Zemstandart/Alexey Zemskov advises: **Always slide the fitting's crimp collar/sleeve onto the pipe *before* inserting the fitting body** — a step experienced installers still forget occasionally, since it's easy to insert the fitting first and only then realize the collar can't be added afterward without redoing the joint. One source calls double-checking this "foolproof" once you've been burned by it once. **Crimp each joint twice**: once in the standard tool position, then rotate the crimping tool/collar 90° and crimp again — a single crimp can leave the seal uneven around the collar's circumference, and the second, rotated crimp is what actually guarantees a full, even seal.
