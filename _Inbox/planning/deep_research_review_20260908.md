# Review of the Gemini Deep Research report (2026-09-08)

**Report**: `_Archive/processed_sources/20260908_gemini_research_3d_budgeting_toolchain.md` — raw text as returned, 71,402 bytes, sha256 `90cd26a7…`, fetched read-only from Google Docs (`1qBwtmhZzQKZuF5J4IdybLWzafpVdQR0eTN3iFGfMuQQ`, title "Gemini research") via the qa-management repo's stored OAuth token. **Filed in the frozen archive rather than in planning, per this vault's convention that raw source evidence is archived and never edited** — which also means `verify_batch.py`'s USD-rounding check does not fire on the LaTeX degree notations (`$89.2^\circ$`) the report contains.
**Brief and acceptance criteria**: [`deep_research_brief_3d_budgeting_toolchain_20260908.md`](deep_research_brief_3d_budgeting_toolchain_20260908.md).

---

## Verdict: it passes all six acceptance criteria

| Test | Result |
| :--- | :--- |
| Distinguishes Belarus from Russia on cost basis and regulation | ✅ **Strongly.** Its standards matrix marks Russian СПДС/СП **«Non-Applicable in Belarus»**, names СТБ 2255-2011 and ТКП 45-1.03-85-2007 as Belarusian, and treats ГОСТ as interstate-adopted-but-customary |
| Answers the variant-cost-delta question concretely | ✅ **Better than asked.** Pipeline, a full JSON Schema for a `CostDeltaReport`, and the cascading-task insight (below) |
| Names where the thesis FAILS | ✅ Four "not yet replaceable" items, a per-domain failure-mode table, and a five-item **"don't build this"** list with costs |
| Date-stamps AI-capability claims | ✅ **Mostly** — explicit stamps on diffusion (SDXL / SD 3.5 / Flux.1, mid-2024→early-2026), MCP, raster-to-vector, plus tool versions. ⚠️ **But the Minsk market rates carry no date** |
| Avoids re-proposing what the digest says is built | ✅ It engages the real gaps and even cites **our own validators** ("corner ownership", "room-rollout closure script") inside its IDS/BCF gating design |
| Separates model-measured from datasheet-derived quantities | ✅ Explicitly, with formulas and deduction thresholds |

**So the report is usable.** What follows is what must be fixed before any of it is trusted.

---

## ⚠️⚠️ Errors found by checking it against the primary act we already hold

**The legal section is the weakest part of the report, and it is the part that sounds most authoritative.** Checked against `Постановление № 164` itself ([source note](../../_Sources/DOC_postanovlenie_164_2026_pereustroystvo_pereplanirovka.md)):

### 1. It misstates the content of §3's list while reasoning about it

Resolving the абзац ambiguity, it describes:

- **абзац второй** as «works altering gas, central heating, **and ventilation** systems» — **wrong.** §3's first item is «замена или перенос систем **газоснабжения, центрального отопления**». **Ventilation appears in §4 as a prohibition, not in §3 at all.**
- **абзац третий** as «insulation and **thermal envelope** works» — **wrong.** §3's second item is «устройство **гидро-, паро-, звукоизоляции**» — waterproofing, vapour and *sound* insulation. **There is no thermal insulation in that item.**

**⚠️ Its conclusion may still be right** — that абзац первый is the introductory phrase, so the exemption covers items 1–2 and **partition changes are therefore NOT exempt from the ведомость технических характеристик.** That matches the reading I independently identified as the more likely one. **But two of its three supporting descriptions are false against the text**, which means the citation to **Art. 26 of Закон № 130-З** cannot be taken on trust either.

**→ Treat as: probable answer, unreliable reasoning. Verify Art. 26 of № 130-З directly, or settle it with the исполком. The practical consequence is unchanged — budget for a ВТХ.**

### 2. ⚠️ Its Указ № 200 subparagraph mapping contradicts № 164

This is the most consequential error, because the whole "what do I actually submit" question rests on it.

| Subparagraph | Gemini says | № 164 actually says |
| :--- | :--- | :--- |
| **1.15.1** | «Extract from the ЕГРНИ», fee 0.1–0.2 БВ | **Положение 2 §4: the citizen's document list for ANTENNA / AC-unit approval** |
| **1.15.3** | «State registration of changes… new Certificate of Title» | **Положение 1 §13: the citizen's document list for PROJECT approval** |
| **1.1.21²** | «Approval of facade-mounted equipment (air conditioners, satellite dishes)», 15 calendar days | № 164 cites **1.1.21²** for **approving the acceptance act** (§20), and routes facade equipment to **1.15.1** instead |

**→ At least three of its five subparagraph descriptions conflict with the act that cites them.** Everything in that section — fees, the 15-day reduction, the acceleration surcharge, the day counts — **is unverified and now suspect.** **Fetching the actual Указ № 200 remains the top open item, exactly as the brief said.**

### 3. It garbles the attribution for general domestic noise

It labels the 23:00–07:00 rule as «Положение об условиях и порядке переустройства и перепланировки, **Resolution № 399**» — that is **№ 164's own Положение title pasted onto № 399.** So the general-noise source is still not properly identified.

**What it does add, and it is useful if true**: that the 09:00–19:00 restriction applies **per task (by the acoustic profile of the tool), not per project** — so quiet finishing work is lawful at weekends within 07:00–23:00. **That was my open question and this is a plausible answer, but it rests on the garbled citation.**

### 4. КоАП Article 22.12 — precise, plausible, unverified

It presents the 09:00–19:00 rule as *sourced from* КоАП 22.12 Part 3, where we know it is in **§15 of № 164**; both can hold (conduct rule in one act, penalty in the other), but the framing is wrong. The five penalty bands (2–10 / 10–30 / 4–10 / up to 20 / 10–30 БВ) are **exactly the kind of article-numbered detail that gets renumbered.** ⚠️ **Do not write into the vault without the code.**

**One point in it is worth keeping regardless, and it is a good one**: *paying the fine does not regularise the change* — you still legalise or restore. That is consistent with § 28 of № 164.

### 5. The СН 3.02.01-2020 quote must be verified before it is believed

It supplies a **verbatim Russian quote of Clause 4.11** — the wet-zone rule. If accurate it settles a question the vault has had open. **But a verbatim quote is precisely what an LLM hallucinates most convincingly, and this report has already misquoted § 3 of an act it had in hand.**

**⚠️ Note what the quoted text would mean for this flat if genuine**: the exception permitting a sanitary unit over a kitchen applies **only on the top floor or in a two-level flat.** This flat is **floor 4 of 21**, so the exception would not apply, and the prohibition would bind in full.

### 6. Undated prices

Minsk market rates — turnkey $180–320/m² labour, $350–650+/m² with materials; itemised direct labour $120–200/m²; plastering 18–25 BYN/m²; tiling 45–65 BYN/m²; ВТХ 150–350 BYN — **carry no date.** Under this project's own standing rule a price without a year has minimal comparative value. **Tag as "as reported 2026-09, unverified" if used at all.**

### 7. Two standards descriptions to check

**ТКП 45-1.03-85-2007** is described as governing internal finishing and flooring works and the drafting of concealed-works acts; I believe that number is «Организация строительного производства» (organisation of construction production). **Unconfirmed either way.** **СТБ 2255-2011** as the documentation standard is plausible and unverified.

---

## ⚠️ What is genuinely valuable — and this is most of the report

### The single best technical contribution: cost deltas cascade

> **A wall move is not `(L_B − L_A) × wallRate`.** Shifting a 100 mm partition cascades into: the wall structure (+m²); **wall finishes on BOTH sides** — plaster → primer → putty → paint (+2 × m²); baseboards and cornices (+linear m); flooring infill or deduction (+m²); and the ceiling junction perimeter (+linear m).

**And it names the matching failure mode**: «cascading indirect dependencies… missed in the delta script». **That is the design requirement for our delta engine, stated better than the brief asked for it.** It also supplies a `CostDeltaReport` JSON Schema with per-line `base_qty` / `candidate_qty` / `delta_qty` split across labour and material — directly implementable against `data/canonical/` plus `data/scraper.db`.

### The "worker-ready" answer is concrete and it is a datum problem

- **⚠️ MEP dimensions must reference bare structural corners, not the finished plaster face** — otherwise «a 15 mm plaster layer will shift a plumbing rough-in off-centre from an intended vanity cabinet». **That is a model-convention requirement, not a drawing style choice**, and it bears directly on `Fixture_Stubout_Coordinates.md`.
- **FFL ±0.000 must be anchored against the bare slab top** (e.g. −0.080), because back-box heights, door rough openings and drain slopes all derive from it.
- Tile setting plans need a **layout start axis, cut-piece locations (no strip < ½ tile), and specified joint width** — which matches, independently, what Vasily_Sanuzel does on site (module-driven setting-out, 120 cm + 4 mm).
- Junction details that coordination drawings omit: recessed skirting, ceiling shadow reveals, waterproofing turn-ups, acoustic decoupling pads.

### It confirms the §20 flexibility strategy I proposed in Amendment 2

> **Deliberately under-specify the submitted план-схема**: partition centrelines, door openings, room names only. **Do not draw plumbing fixtures, floor finishes, sockets, dropped ceilings or furniture on it** — § 3 excludes them from перепланировка, so keeping them off the submittal isolates finish changes from the legal acceptance perimeter.

**That is exactly the resolution to the flexibility-versus-§20 tension, now independently stated.** ✅ **The one claim in the legal section I would treat as reliable, because it follows from § 3 and § 20 as we already read them, rather than from a citation.**

### It answers the self-performance concealed-works question

**No general-contractor certificate is needed** to draft акты на скрытые работы when the owner performs the work (§ 14). **The owner signs as executor, and the act should be backed by a photo log showing a tape measure** confirming overlap depths, material batch labels, and continuity across thresholds. Named critical operations: **wet-zone waterproofing** and **floating-floor acoustic insulation.**

### Clean verdicts that remove work from the roadmap

- **НРР: a private owner cannot use it.** Mandatory only for state-funded work; НРР labour rates of **4–8 BYN/h** against a real market of **20–50+ BYN/h**, plus commercial-construction mechanisation assumptions and licensed estimating software. **→ Price from market quotes; our own price DB + FX converter becomes the primary instrument, exactly as the amendment anticipated.**
- **Classification: Uniclass/OmniClass is over-engineering here** — Belarusian suppliers and trades do not consume the codes. **Use a flat 2-tier trade-keyed taxonomy** (`TIL-01:R04:Paving_600x600`), which maps to SQLite/CSV and to `IfcPropertySet` without ontology work.
- **Nesting: percentages for drywall and standard tile; real 2D nesting only for large-format slabs >$60/m² and sheet goods** — `rectpack` named. **Directly corroborates Vasily's sub-1% framing-waste result as the exception rather than the norm.**
- **3DGS and photogrammetry give appearance, not measurable geometry** — featureless white walls defeat feature matching, and unscaled reconstruction drifts **20–80 mm over 10 m**. **→ Buy a Bluetooth laser meter ($60–120). This kills a roadmap item cheaply, as predicted.**
- **AI diffusion over clay renders is mood-only** — hallucinates tile joints, invents mouldings, alters faucets, blurs sockets. **Never a trade document.** Outsource a one-off room render at **$40–90** instead of building an asset pipeline.
- **Never let an agent vectorise a raster BTI plan for construction** — 1–3 % scale drift, non-orthogonal walls at 89.2°, misread dimensions (3.120 → 3.720). **Trace it once manually over an orthogonal grid, 1.5–2 h.** **→ That is the answer for `v0`, and it is "do it by hand", not a pipeline.**

### The build order is calendar-driven, and it is the right shape

Six phases, ~125 days, with the two insights that matter: **the 5D cost work and trade sourcing run concurrently inside the one-month permit review window**, and **all non-noisy finishing runs concurrently inside the 30-day acceptance-commission notice period.** Statutory milestones are on the critical path; compute is not.

---

## What to do next, in order

1. **⚠️ Do NOT route any of the legal content into `16_Legal_and_Regulations/`.** That folder is level-1 primary-source only, and this report is a secondary source that has already been caught misquoting an act it held. Its legal value is as **a list of things to verify**, which is what the brief said secondary summaries are for.
2. **Fetch Указ № 200 and re-derive the subparagraph map.** Highest-value single action: the report's version conflicts with № 164 in three places, and everything about the actual application depends on it.
3. **Verify the СН 3.02.01-2020 Clause 4.11 quote** against the norm. If genuine, it goes into `16_` and it constrains layout variants — the top-floor exception does not apply to this flat.
4. **Route the non-legal content**, which is admissible on ordinary evidence rules: the cascading-delta design and JSON Schema, the datum/FFL conventions, the classification verdict, the nesting thresholds, and the negative verdicts on 3DGS, diffusion and raster vectorisation. Targets: `00_Master/Sheet_Production_Roadmap.md` (amend the ten capabilities), `00_Master/Finishes_and_Furniture_Data_Model.md`, `11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement.md`, and `.agents/skills/residential-bim-geometry-rules/` for the bare-corner datum rule.
5. **Amend the roadmap's capability order** to match the report's build order, since it is constrained by statute rather than by dependency.

## Standing note for the next research round

**The report's failure pattern is worth remembering: it was strongest exactly where it had no legal citation to make, and weakest where it cited.** Every one of its errors is a misattributed or misquoted legal reference; none is in the engineering reasoning. **→ For the remaining primary sources, use Deep Research to find and summarise, and verify every citation against the act itself before it enters the vault.**

---

## ✅ Verification round, same day — outcomes

**Two of the three follow-ups the review named have been done.** Both found errors in the report.

### Указ № 200 — partially verified, and the report's map is wrong in three places

Checked against `pravo.by` and two official исполком «одно окно» pages (Ленинский район Могилёва, Могилёвский горисполком):

| Subparagraph | Report said | **Verified** |
| :--- | :--- | :--- |
| **1.1.21** | approval, free, 1 month, 15 days if applicant supplies documents | ✅ **исполком, free of charge, 1 month, validity indefinite.** ⚠️ The 15-day reduction was **not** visible in what was read |
| **1.1.21″** | facade-mounted equipment, 15 days | ❌ **Approving the acceptance act.** Free, 1 month, **valid until the technical passport is drawn up and the change registered.** Documents: application, passport, **ведомость технических характеристик** |
| **1.15.1** | ЕГРНИ extract, 0.1–0.2 БВ | ❌ **Согласование for installing antennas and other constructions on roofs and facades, including самовольную** — i.e. the AC-unit procedure, exactly as № 164 Положение 2 §4 says |
| **1.15.3** | title registration, 0.5 БВ + 0.1 + 0.3 acceleration, 7 days | ⚠️ **Unverified.** № 164 §13 cites it for **project approval** |
| **1.1.21′** | — | ⚠️ **Unverified** (retro-approval of самовольная per № 164 §24) |

**⚠️⚠️ And the 1.1.21″ page settled the абзац ambiguity that three pages had flagged for a phone call.** It describes the ВТХ exception as applying to **«certain gas, heating and insulation work only»** — the reading in which абзац первый is the introductory phrase. **→ Partition changes are NOT exempt; this project needs a ведомость технических характеристик.** The report's *conclusion* was right; its reasoning and its list descriptions were not.

### СН 3.02.01 — the quote was wrong in four ways, and it omitted the useful half

Fetched the norm and read §4.9 directly ([source note](../../_Sources/DOC_SN_3_02_01_2019_zhilye_zdaniya.md)):

1. **Designation is -2019**, not -2020 (published 2020 — the likely origin of the error).
2. **Clause is 4.9**, not 4.11.
3. **There is no top-floor exception for sanitary units.** The report invented one by conflating §4.9 with **§4.8**, which is about a living room over a **gas-stove kitchen** — a different rule about a different pairing.
4. **It omitted the 25 % partial-placement allowance and the minimum plan dimensions entirely** — the two most useful provisions in the clause.

**⚠️ And the omitted half produced the round's most consequential project finding**: the minimum for a **туалет with a washbasin is 1.4 × 1.5 m**, so **a washbasin in this flat's 1.24 m² туалет cannot comply.** Plus an unresolved discrepancy: on the ventblock dimension the vault holds, **no dimension of that room reaches the norm's 1.5 m minimum at all.**

### What this changes about how to use the report

**The pattern named in the standing note held exactly.** Every error found in two rounds of checking is a **misattributed or misquoted citation**; not one is in the engineering reasoning.

> **→ Treat the report's engineering content as usable on ordinary evidence rules, and every legal citation in it as a lead requiring the act.** Two of its legal claims have now been checked; **both were wrong in detail, and one was wrong in a way that would have put a fabricated exception into the vault.**

**Still open**: 1.1.21′ and 1.15.3; **Изменения №1 и №2 to СН 3.02.01-2019** (which bear directly on the туалет discrepancy); КоАП Article 22.12's numbering and amounts; постановление № 399 and the non-перепланировка noise window; and ТКП 45-1.03-85-2007's actual subject.

**Not yet started**: routing the report's non-legal content into the roadmap — the cascading cost-delta design, the bare-structural-corner datum rule, the classification verdict, the nesting thresholds, and the negative verdicts on 3DGS, diffusion and raster vectorisation.
