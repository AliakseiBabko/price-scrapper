---
source_type: video transcript (podcast-style interview, channel owner interviews an in-house interior designer, Russian, ASR auto-generated captions — ru language, not translated)
source_url: https://www.youtube.com/watch?v=IXZItGe0K9M
video_id: IXZItGe0K9M
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 a54b9aa84a69c7bef02ff5e223442e84c1047eb592893874d92f8326583a95ec)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated/ASR captions, is_translated=false, language_code=ru)
upload_date: 2025-10-25 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation — St. Petersburg (guest: Anastasia Berezinets, in-house/affiliated interior designer)
regional_applicability: national/unspecified for the general process content; the "35,000 RUB/m²" underquote case is a Moscow-based secondary-market apartment (level 1, spoken directly)
currency: RUB, converted at trailing-6-month USD/RUB mean before 2025-10-25 (80.3882 RUB/USD, via tools/pricing/currency_converter.py) where a concrete figure is stated
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 8
promotional_ratio: medium-high (65-minute podcast interview framed as career advice for aspiring designers, with repeated Telegram/seminar plugs; majority of runtime is designer career/business-model content excluded per this project's value filter)
corroborates_existing: partial — extends this store's existing author-supervision re-measurement fact (Round 3, `uqv1-7DCKYI`) with a concrete geometry-drift numeric range and a real worked case; a second independent design-fee-vs-real-cost mismatch case (different numbers, same mechanism as `uqv1-7DCKYI`'s Moscow 3,000 RUB/m² case); corroborates the existing "client insists on cheap execution of an expensive design" budget-mismatch theme
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ) interviews Anastasia Berezinets: "How an Interior Designer Works and Why There Are So Many Mistakes in Design Projects" (YouTube IXZItGe0K9M)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 4, video 2 of 8.** English-displayed title, Russian ASR audio. A 65-minute podcast-style interview with Anastasia Berezinets, a working interior designer, framed explicitly as career-advice content for aspiring/beginning designers (education path, studio vs. freelance, client acquisition, pricing, seasonality, contracts). **Medium-high promotional ratio**: the interview repeatedly plugs the host's Telegram channel and beginner-designer seminars, and much of the runtime is generic career/business-model advice not specific to any renovation technique or checkable fact. **Value-filter verdict: partial extraction** — the career/marketing majority is excluded; a handful of genuinely new, checkable process/mistake mechanisms and two real numeric cases are kept, consistent with this store's precedent for this format (`uqv1-7DCKYI`, Round 3).

## Contractor Acceptance / Vetting — Design-Project Measurement Drift, Extending the Existing Author-Supervision Fact

- **⚠️ Named root-cause mechanism, extends this store's existing "re-measure after demolition" author-supervision fact with a concrete numeric range**: a design project is normally measured during a "rough" (`черновые обмеры`) site visit — before plaster/drywall/wall-leveling work happens. Once walls are actually plastered/leveled, real geometry commonly shifts **3-15 cm** from the original rough measurement, and **old-fund ("старый фонд") buildings can shift up to 20 cm** — described by both speakers as a real, recurring, non-negligible pattern, not an edge case.
- **⚠️ Real worked case showing the compounding effect**: a client (a tall/basketball-playing occupant) specified a bathtub requiring **190 cm** of clear length in the bathroom. After the actual post-demolition geometry came in roughly 10 cm smaller than planned, and after subtracting a further ~3 cm for the tile-plus-adhesive buildup on the tub's edge, the space that was actually left could fit **only a 108 cm bathtub** — a **~13 cm** total shortfall traced directly to uncorrected rough-measurement drift plus an unaccounted finish-thickness allowance.
- **⚠️ Named fix, a specific drawing convention**: mark on the drawings which dimensions are **critically fixed and must not change** (e.g., a minimum clearance for built-in appliances/furniture) versus which are flexible/approximate — one practitioner's own evolved convention marks fixed-critical dimensions in **red** and flexible ones in **black** directly on the drawing set, plus a callout/annotation at the specific critical points, rather than relying on a single undifferentiated dimension chain.
- **⚠️ Named recommended workflow to avoid the drift entirely (acknowledged as rarely accepted by clients due to schedule impact)**: take rough measurements first, let demolition and wall-leveling/plastering happen, then take **final ("чистовые")** measurements before producing the dimensioned drawing set — as opposed to producing final drawings directly from the rough measurements and hoping geometry doesn't move.
- **⚠️ Real anecdote — a dimension-chain ambiguity causing a visible defect**: in an unrelated project, switches/outlets ended up positioned behind a door once open, because the drawing's dimension chain wasn't anchored to a fixed reference point (it wasn't specified whether a run of dimensions should be measured from the window/curtain line or from the wall) — when the built geometry shifted, everything anchored to that ambiguous chain (bed position, light fixture position) shifted with it.
- **⚠️ A stated three-way liability triage when a construction-phase problem surfaces without author supervision in place**: is it (1) a genuine design error, (2) a construction-crew execution error, or (3) a coordination gap (the design called for something realizable, that a different crew executed successfully elsewhere, but the current crew either couldn't or wouldn't attempt it) — the speaker's own real example: a panel cut into a decorative frieze pattern was declared "impossible" by one crew but had been executed without issue by a previous crew on an earlier project of hers; she resolved the dispute by sending reference photos from the earlier successful install, not by disputing the crew's judgment directly.

## Planning Rules / Budget — Design-Fee-vs-Real-Cost Mismatch, a Third Independent Case

- **⚠️ Real case, a different underquote mechanism from this store's existing Moscow 3,000 RUB/m² case (`uqv1-7DCKYI`)**: a Moscow designer quoted a 64 m² secondary-market ("вторичка") apartment's demolition-and-renovation "materials + labor" cost at **≈35,000 RUB/m² (≈$430/m²)** — while the host states that in the same (business) segment, a genuinely good labor-only crew (not even a company) starts at **≈45,000 RUB/m² (≈$560/m²)** for labor alone, and a company operating in the business segment starts at **≈60,000 RUB/m² (≈$750/m²)** all-in. The host's own read: the quoting designer likely simply didn't know real current market rates for labor/materials — a knowledge gap distinct from `uqv1-7DCKYI`'s case, where the estimator's assumption stayed anchored to an outdated *scope* rather than an unfamiliarity with current *rates*.
- **General mechanism, stated directly by the host**: because the designer is typically the first person to quote a renovation's likely cost to a client, an inaccurate quote (in either direction) sets a client expectation that a later, more accurate builder's quote then appears to contradict — leading the client to suspect the builder of price-gouging even when the builder's number is the accurate one.

## Mistakes / Warnings — Payment-Risk Mitigation and Client-Budget-Reality Corroboration

- **⚠️ Concrete anti-non-payment practice**: this designer withholds **10%** of the total design-project fee until final delivery, specifically because a digital design file, once handed over electronically, is trivially non-recoverable if a client simply stops responding after receiving it — she states this figure was arrived at only after "several" (unspecified, more than one or two) real non-payment incidents, not adopted preemptively.
- **Corroborates this store's existing "client insists on cheap execution of an expensive design" budget-mismatch theme (`uqv1-7DCKYI`)**: the host's own framing — a client who insists on paying an economy-segment price to execute a business/premium-segment design "drew a Mercedes and will get a Hyundai" — independently restated by a second interviewee on this same channel.

## Assumptions / Uncertainties

- The 3-15cm/20cm geometry-drift figures and the 108cm-vs-190cm bathtub case are both the speakers' own recollected figures, not independently verified against any as-built survey — recorded as their own stated experience.
- The bulk of this video (career education path, studio-vs-freelance economics, client-acquisition/marketing tactics, seasonality, portfolio-building advice) was reviewed in full but excluded from this note as designer-career/business-model content outside this project's own scope (this project is a client, not an aspiring designer).

## Target Page(s)

- **`11_Budget_and_Planning/_supporting/knowledge/intermediate/store/Durable_Facts.md`** — extends the existing Author-Supervision Scope section (Round 3) with the geometry-drift numeric range, the real bathtub case, and the red/black dimension-marking convention; adds a third independent design-fee-mismatch case; adds the payment-risk-mitigation practice.
- **`00_Master/wiki_page_format.md` / `Estimate_and_Contract_Templates.md`** — the red/black critical-vs-flexible dimension-marking convention and the 10%-final-payment-holdback practice are both concrete, adoptable drafting/contracting conventions worth a look for that page in a future pass (not added directly in this round — flagged as a candidate, not confirmed fit).

## Relevance to This Project's Topic

Beyond the excluded career-advice majority, this interview contributes a genuinely concrete, numeric illustration of why a design project's dimensions can drift between initial measurement and final execution (3-15cm typical, up to 20cm in old-fund buildings) with a real worked case (a specified 190cm bathtub clearance collapsing to 108cm), plus a specific, adoptable drawing convention (red/black critical-dimension marking) for guarding against exactly this failure mode in this project's own design process.
