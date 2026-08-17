---
source_type: video transcript (company technique/opinion video, two-narrator)
source_url: https://www.youtube.com/watch?v=n_1gnhHM184
video_id: n_1gnhHM184
transcript_file: _Archive/processed_sources/20260814_stupidest_smart_house_186_159f04b4.txt
fetched: 2026-08-14 via youtube-transcript-api (manual ru captions)
upload_date: 2022-12-04 (confirmed via yt-dlp metadata, upload_date=20221204)
channel: Zemstandart (Alexey Zemskov + Sergey Saratov, "technical expert for comfort-class renovation") — Moscow-based (channel-level association only, not stated in-video)
source_metadata_location: Moscow (channel convention, level 2 — not spoken/written in the source itself)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
---

# Extraction Note — Zemstandart: "The Stupidest Smart House" — Smart-Gadget Critique & Switch-Logic Rule (#186, YouTube n_1gnhHM184)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

**Company opinion/technique video, two narrators**: Alexey Zemskov (channel owner) opens with the segment framing (comfort-class positioning) and hands off to Sergey Saratov, described as "the technical expert responsible for comfort-class renovation" on the company's team. **Turnkey/Full-Service** channel convention — content is framed throughout as "in our projects," "in our company," i.e. the company's own design/technique standard, not neutral third-party product review.

**Advertising/promotional filter applied**: this is not a client case study (no specific paid job referenced) but a company-standard-setting opinion piece — several of its claims are framed as blanket recommendations ("never buy a smart door," "always use milled handles") that also happen to describe this company's own design defaults. The rate-card figures given at the top (comfort/business/elite labor bands) are the company's own self-quoted pricing tiers, repeated near-verbatim from other sources in this store (see Numeric Data below) — **not a new data point**, a restatement. Extracted as company-stated practice/opinion, tagged accordingly, not adopted as neutral universal fact where it reflects only this company's stylistic preference (e.g. milled handles vs. push-pull).

## Rooms / Zones

- None found — content is cross-cutting technique/product-category advice, not scoped to one room.

## Electrical

- **Server/low-voltage cabinet or panel ("серверная"/"слаботочный щит") for aggregating all low-voltage cabling must include ventilation**, or heat from powered equipment inside it (routers, hubs, PoE switches, etc.) accumulates with no path out and risks equipment failure over time. `confirmed` as the speaker's own stated design rule. [source: yt_n_1gnhHM184]
- **Never buy furniture with a built-in ventilation grille for this purpose** — described as a 3x markup vs. buying a plain cabinet/furniture piece and separately sourcing a generic grille at a building-materials market, then paying an installer to cut the opening for it. Same "component markup vs. assemble separately" pattern already seen elsewhere in this store for smart-door hardware (see Switches / Sockets / Cables below). `confirmed` as stated practice, `single-account`, tier-steering-adjacent (a specific purchasing-channel recommendation, not just a technical requirement). [source: yt_n_1gnhHM184]

## Switches / Sockets / Cables

- **Core "logical switch placement" rule, demonstrated with an unrehearsed test**: switches should be positioned so their function is inferable by physical proximity/logic to the fixture they control, without needing a printed legend — e.g. a switch physically closest to a given light fixture controls that fixture. Zemskov ran an on-camera test asking the company's own staff designer (not otherwise identified) to guess which of four switches controlled which of four lighting elements purely from their layout, with no prior briefing; the designer correctly inferred all four purely from proximity/logic and stated the reasoning was "because it's logical." `confirmed`, directly demonstrated. [source: yt_n_1gnhHM184]
- **Explicit position against multi-button "piano" style switch panels (up to ~64-68 preset lighting-scene buttons) for comfort-class work**: framed as a business-class/elite-tier feature that is disproportionately complex, expensive, and "illogical" relative to its benefit at the comfort price point — reserved for business-class-and-above budgets where the extra cost is proportionate. For comfort-class, the company's stated default is individual logically-placed switches instead. `confirmed` as the company's own segment-scoped design position — a genuinely new **tier-scoping nuance on switch/control hardware choice** not previously recorded this specifically in this store's existing Switches & Controls entries (which cover physical placement/orientation/wiring, not this scene-panel-vs-individual-switch tier distinction). [source: yt_n_1gnhHM184]
- **"Smart door" is not a real distinct product — always buy a plain door and a separate smart lock**: the speaker states plainly that a pre-integrated "smart door" product is functionally a normal door with a smart lock bundled in at a markup, and that buying the two separately (a standard door, then ordering a smart lock installed onto it) saves "at least 3x." Stated as a direct purchasing-behavior warning, explicitly urging viewers not to search "smart door" online at all. `confirmed` as stated company advice, `single-account`. A companion caveat: regardless of price tier, fingerprint/app-based smart locks are described as still failing to open reliably at times ("always glitch a bit") — the phone-app fallback is reported to work in practice, so the speaker's practical mitigation is "don't forget your phone at home." `confirmed` as the speaker's own qualified endorsement (not unreservedly positive). [source: yt_n_1gnhHM184]
- **Smart-lighting/curtain voice control has a real, demonstrated command-batching limitation** (Alice/Yandex smart-speaker ecosystem specifically): a single combined voice command covering two actions ("open the curtains and turn off the light") reliably fails to execute either action in this speaker's on-camera repeated test; issuing the same two actions as two separate, sequential commands works. Also demonstrated: a partial-position curtain command (e.g. "close the curtains 50%") succeeds where a full open/close command given as part of a combined phrase does not. `confirmed`, directly demonstrated (not a claim taken on faith) — a concrete voice-assistant reliability caveat, genuinely new to this store. [source: yt_n_1gnhHM184]
- **Rule: any smart/voice-controlled lighting circuit must retain a normal physical switch in parallel, regardless of how good the smart control is** — reasoning given: without this, a malfunction forces the occupant to use the branch breaker in the electrical panel to turn lights on/off, which the speaker frames as an unacceptable fallback for daily use. `confirmed`, stated as a hard rule ("always duplicate control"). This generalizes/reinforces (from a new source) the existing store principle that smart controls should never fully replace physical switches. [source: yt_n_1gnhHM184]

## Lighting

- **"Duty/night light" (дежурное освещение) placement rule and terminology note**: the speaker's favorite/most-used design element — a continuous, low-level, non-blinding light source kept on at all times along hallway paths and inside bathrooms/WCs specifically, intended for night-time use (e.g. walking to get water or use the toilet) without needing full lighting. Explicit **search-term mismatch flagged by the speaker himself**: "дежурный свет"/"duty light" is described as internal company jargon that won't return useful results if searched online — the equivalent retail/product search term is "подсветка лестницы" ("stair lighting" fixtures), which the speaker states will surface the correct fixture type. `confirmed` as the company's own terminology/sourcing tip — directly useful, checkable guidance for anyone shopping for this fixture type. [source: yt_n_1gnhHM184]

## Furniture / Built-ins

- **Milled/routed ("фрезерованные") handles preferred over push-pull mechanisms and over protruding standard handles, for both cabinetry and doors**: push-pull mechanisms are described as not always triggering reliably (demonstrated on camera — a cabinet door shown not fully closing/releasing after a push). Protruding standard handles are criticized on two grounds: they snag/damage adjacent surfaces when the door/drawer swings open, and they are a real injury/collision risk (framed as something "everyone has hit at least once"). Milled handles are presented as solving both — no protruding part, comparable ease of grip, sometimes doubling as a design element — and are stated as this company's now-default choice across its own projects. `confirmed` as company stated preference/technique reasoning (mechanism given, not just assertion), `single-account`. [source: yt_n_1gnhHM184]
- **Do not buy furniture with integrated ventilation for a low-voltage/server cabinet use case** — cross-referenced above under Electrical; recorded here too since it's specifically a furniture-purchasing decision. [source: yt_n_1gnhHM184]

## Materials

- **Ultra-thin/flush-mount TVs use a single combined power+signal connection (a UTP cable) rather than a standard power cord + separate signal cable(s)**, and this has a hard downstream planning consequence: the TV type must be decided and locked in at the design-project stage, before rough-in electrical/low-voltage wiring is finalized — because if the buyer later decides against the expensive flush TV and wants to switch to a standard TV, the wall will only have the single UTP outlet already roughed in, which a standard TV's normal power+signal inputs cannot use. Reported as "in no case" reversible once the wall is closed up. `confirmed` mechanism and planning consequence, `single-account`, genuinely new and checkable technical fact for this store (previous store content on behind-TV planning covers only cable-channel sizing and outlet-plate layout, not this power-delivery-architecture lock-in issue). [source: yt_n_1gnhHM184]
- **Ultra-thin/flush-mount TVs are quoted as roughly 3x the price of a comparable standard TV, all else equal**, per the speaker's stated framing. `single-account`, `unverified` (no comparative model/price data given). [source: yt_n_1gnhHM184]

## Labor Prices

- **Comfort/business/elite labor-only price bands restated, consistent with existing store entries**: comfort-class labor (materials excluded) 25,000–45,000 RUB/m²; business-class labor 50,000–85,000 RUB/m²; elite-class labor 90,000–150,000 RUB/m². The speaker explicitly frames the entire video's advice as scoped to comfort-class only — techniques discussed do not apply/are not relevant to business or elite tiers. **This is a restatement, not a new corroborating data point** — the same exact figures were already recorded in this store from `yt_7VfZIYGUrTo` and `yt_Gp5Lr20SrtU` (both processed 2026-08-14, days-to-same-week apart), all same channel/company — `single-account` at the company level regardless of how many of its own videos repeat the number. [source: yt_n_1gnhHM184]

## Budget Ranges

- See Labor Prices above — the same three-tier band applies here as a segmentation framework, not a distinct budget-range fact.

## Mistakes / Warnings

- **The video's central framing ("smart" home gadgets are all somewhat unreliable/limited despite marketing) is itself the main warning**: every smart-home feature discussed (voice-controlled curtains/lights, smart locks, push-pull furniture mechanisms) is paired with a specific, demonstrated failure mode rather than a blanket endorsement or blanket dismissal — treat as balanced/attributed opinion from a company that also sells smart-home integration as part of its own renovation packages, not a neutral third-party test. [source: yt_n_1gnhHM184]
- **Piano-style multi-scene switch panels are flagged as a common client-driven mistake at the comfort-class budget tier**: the speaker attributes rising demand for these panels to clients having seen "designer videos" and wanting the aesthetic without weighing the cost/complexity tradeoff at their actual budget tier. `confirmed` as the speaker's own stated observation. [source: yt_n_1gnhHM184]

## Other / Unclassified

- None found beyond the above buckets.

## Confidence & Evidence Notes

- **ASR quality**: manual (non-auto-generated) Russian captions were used (`is_generated_captions: false` per metadata sidecar); transcript reads as clean, coherent conversational prose — one on-camera command-repetition demonstration reads a little choppy in text form (rapid successive "Alisa, open the curtains" / "Alisa, turn off the light" commands) but the intended meaning and outcome of the demonstration are unambiguous from context. No passages flagged `ASR-uncertain`.
- **Two-narrator source, both clearly distinguishable by role/introduction** — Zemskov's opening framing segment and Saratov's technical-advice segment are both clearly delineated in the transcript by content/register even without explicit speaker labels; no attribution ambiguity found.
- **Currency/region**: no location named directly in the transcript (checked). Region recorded as level-2 (channel convention) only, consistent with how this project's other Zemstandart sources are tagged pending the standing open audit question already recorded in this store.
- **Labor-price restatement flagged explicitly** (see Labor Prices above) so a downstream reader doesn't treat this as a third independent corroboration — it's the same company repeating its own number across a short span of videos.

## Assumptions / Uncertainties

- Assumed "Sergey Saratov" 's stated role ("technical expert responsible for comfort-class renovation") is accurate as self-described on camera — not independently verified against any company staff page.
- The company staff designer's name/identity in the switch-logic demonstration is not given in the transcript — recorded as "the company's own staff designer," not a named individual.

## Recommended Downstream Routing

- **`tiered-knowledge-base`** — this project's renovation budgeting knowledge store (Switches/Sockets/Cables, Lighting, Furniture/Built-ins, Materials, Electrical, Mistakes/Warnings sections), per this task's assignment. Adds a genuinely new tier-scoping nuance to this store's existing switch/control rules (piano-panel-vs-individual-switch by budget tier), a new demonstrated voice-assistant command-batching limitation, the "smart door is not a real product" purchasing rule, the duty-light terminology/search-term tip, and the ultra-thin-TV design-lock-in planning consequence.
- **No `Budgeting_Guide.md` update recommended** — the labor-price figures are a restatement of an existing entry, and the rest of the content is technique/product-category guidance, not a new pricing benchmark.
- **`12_Engineering_and_Systems/Electrical_and_Lighting.md` candidate addition** — the switch-tier-scoping rule, the voice-assistant command-batching caveat, and the always-duplicate-with-a-physical-switch rule fit that page's existing Switches & Controls section; flagged for the next page-promotion pass rather than edited directly in this task (per this task's scope: log to this store, not necessarily edit every downstream wiki page unprompted).
