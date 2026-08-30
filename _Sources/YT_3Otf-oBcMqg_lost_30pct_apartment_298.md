---
source_type: video transcript (single-speaker case-study + heavy self-promotion, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=3Otf-oBcMqg
video_id: 3Otf-oBcMqg
transcript_file: _Archive/processed_sources/20260819_lost_30pct_apartment_298_8b83742a.txt
fetched: 2026-08-19
upload_date: 2025-03-16 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: project location stated in-video — Nizhny Novgorod (level 1), explicitly contrasted with Moscow pricing in the same breath; the fee-payback claims are Moscow-vs-Nizhny-Novgorod specific
currency: RUB (no absolute price figures stated, only relative payback-multiple claims)
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "Lost 30% of the Apartment!" (#298, YouTube 3Otf-oBcMqg)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: PARTIAL EXTRACTION

Category 5 further-pool batch (chunk 1 of 4), video 3 of 7. Roughly 60-70% of this video is a direct sales pitch for the source's own "Zems Pro knowledge base" design-project product (extensive screen-recording of internal design documentation, a promised "300-400 masterclasses" bundled with future project purchases, a price-increase countdown urging viewers to book now). The remaining content is a genuine full-apartment replan case study (Nizhny Novgorod), reclaiming ~30% of layout-conflicted floor area for a large technical-requirements list (multiple bathrooms, kids' rooms with pet/hobby storage, home-office nooks, a loggia lounge). **A named-individual legal-dispute segment was deliberately excluded from extraction** (see Excluded Content below), per this project's standing convention.

## Planning Rules / Quantities/Measurements — Extractable Technique Points

- **Removing an unnecessary exterior insulation layer from an enclosed loggia, where it duplicates insulation already present elsewhere in the build, recovered 17cm of usable loggia width in this project** — flagged as project-specific (depends on the building's actual insulation redundancy), but the underlying check ("is there a removable insulation layer inflating this loggia's wall thickness beyond what's structurally needed") is a general technique worth verifying on any enclosed-loggia replan.
- **A loggia intended to hold a real lounge/seating zone (not just storage) needs a minimum usable width of about 1.1m, with 1.2m recommended** — the source states below ~1m width, a seating area doesn't function; this project reached ~1.2m only after removing the redundant insulation layer above.
- **A 100mm-thick partition wall between two rooms is called explicitly insufficient for adequate soundproofing** — flagged the same way as the wall itself, painted out as a problem area on the design overlay. This corroborates and extends this store's newly-recorded 80mm-partition soundproofing-inadequacy finding (`p-6OI34C6bw`, same chunk) — two independent thickness figures (80mm, 100mm) from the same source now both flagged as inadequate, without yet stating a minimum thickness that *is* adequate.
- **Radiators can be recessed into a false (furring) wall so they don't protrude into the room's usable floor area** — presented as a standard technique applied throughout this project's design, paired with the observation that false walls are also routinely needed to box in plumbing stacks/risers the developer left exposed with no dedicated enclosure — the developer's as-delivered wet-room walls are described as leaving stacks "bare, cover them however you can."
- **A toilet needs roughly 90cm of clear wall width behind/beside it (excluding the fixture footprint itself) for the installation to be considered comfortable** — stated as a specific figure achieved in the replanned bathroom design, though not derived with the same explicit formula as the doorway-width rule in the companion video (`p-6OI34C6bw`) — treat as a single-project data point corroborating a workable clearance figure rather than a fully derived standard.
- **A door/rough-opening's position within its wall run should be set relative to a structural column or load-bearing element it needs to clear, not centered on the wall segment by default** — the defect found: a developer-positioned opening was shifted toward the center of its wall run in a way that put it in direct conflict with a protruding structural column corner, when positioning it nearer the column instead would have avoided the conflict entirely.

## Excluded Content — Named-Individual Legal Dispute

A ~2-minute segment names a specific individual ("info-дизайнер" [info-product designer] Karen Karapetyan) as the subject of two won lawsuits (first and second instance), describes ongoing non-payment of court-ordered compensation, and solicits viewers who have "suffered from his actions" to contact the channel for legal/informational support toward a potential class action. **Deliberately excluded from extraction** per this project's standing convention against laundering named-individual legal-dispute content as neutral technical fact — this is dispute/reputational content, not a renovation technique or planning fact, regardless of its accuracy.

## Advertising / Promotional Content Notes

The majority of this video's runtime is a direct sales pitch for the source's own paid design-project service ("Zems Pro"), including an extended screen-recording tour of internal knowledge-base documentation (categories, rule pages, a promised customer-facing "300-400 masterclasses" bundle) and an explicit price-increase countdown urging early booking. The payback-multiple claims ("pays for itself several times over in Nizhny Novgorod, several dozen times over in Moscow") are the source's own unverified marketing framing — tag `unverified`, not extracted as a store-level fact. The replan case study itself is presented as unambiguous proof of the paid service's value (no comparison to a self-managed or cheaper alternative achieving the same layout gain), consistent with this project's turnkey/full-service tier-steering caution.

## Target Page(s)

The 100mm-partition-soundproofing-inadequate finding should be routed alongside the 80mm finding from `p-6OI34C6bw` (same chunk) — both flag a Walls/Partitions technique gap with no existing dedicated page yet (see that source's own Pending Wiki-Page Decision note). The recessed-radiator and stack-boxing false-wall techniques are general planning notes with no single obvious existing page.

## Relevance to This Project's Topic

Moderate — most of the video is a sales pitch with limited durable value; the few extractable technique points (loggia width threshold, partition-thickness corroboration, recessed-radiator/stack-boxing technique, door-opening-vs-column positioning rule) are genuine but thin relative to the video's length.

## Gaps

- The exact "adequate" partition thickness is still not stated by any source processed so far — only two inadequate figures (80mm, 100mm) are now recorded.
- The 90cm toilet-clearance figure is a single-project data point, not derived with an explicit formula (unlike the companion video's doorway-width derivation).
- Region is confirmed level 1 for this specific project (Nizhny Novgorod) — but the general technique points (radiator recessing, partition thickness, door positioning) are not claimed to be Nizhny-Novgorod-specific and likely generalize; treat the specific payback-multiple figures as regionally split (Nizhny Novgorod vs. Moscow) per the source's own framing.

## Recommended Downstream Routing

`tiered-knowledge-base` — Planning Rules / Quantities/Measurements Durable Facts sections of the renovation budgeting intermediate store. Cross-reference the partition-thickness finding against `p-6OI34C6bw`'s own entry in the same chunk when integrating, since they corroborate the same underlying gap (no page yet).

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above; the legal-dispute segment was deliberately excluded, not omitted by oversight.
