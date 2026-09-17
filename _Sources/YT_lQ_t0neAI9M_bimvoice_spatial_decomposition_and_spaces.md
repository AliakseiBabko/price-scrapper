---
source_type: video transcript (BIMvoice, two tutorials on IFC spatial decomposition and IfcSpace management in Bonsai)
source_url: https://www.youtube.com/watch?v=lQ_t0neAI9M
video_id: lQ_t0neAI9M
covers_also: 9oXWh1spWys
transcript_file: _Archive/processed_sources/20260917_bimvoice_wrong_spatial_container_27ecc15b.txt
transcript_file_pt2: _Archive/processed_sources/20260917_bimvoice_ifc_spaces_what_works_e99822cd.txt
fetched: 2026-09-17 via youtube-transcript-api (en, ORIGINAL language)
upload_date: 2025-08-18 (lQ_t0neAI9M); 2025-03-29 (9oXWh1spWys) - from yt-dlp, actually run
channel: BIMvoice
source_title: "are your ifc elements in the wrong spatial container? (BonsaiBIM fix)" (+ Working with IFC Spaces in Bonsai)
language: en
extraction_taxonomy: custom (this project taxonomy - bucket `Digital Toolchain / IFC authoring`)
fact_yield: 5
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note — Stefan Catargiu (BIMvoice): ⚠️ WRONG SPATIAL CONTAINMENT IS COMMON, WHICH JUSTIFIES A GATE (YouTube lQ_t0neAI9M +1)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## ⚠️⚠️ 1. Spatial decomposition is wrong often enough to be a recurring support problem

> ***"lately I had to help a lot of people to fix their spatial decomposition… they had many IFC models where they didn't have the correct spaces or the objects, the elements in their models were not belonging to the right space… this has to be a very bad sign of quality."*** [Stefan Catargiu]

He attributes it to **export**, and splits the responsibility: *«I hope the vendors are going to make some improvements»* **and** *«users have to invest a little bit more time to understand how to manage the spaces when they export something from a tool to IFC»*. Bonsai, being IFC-native, can **reassign** an element's container after the fact.

**→ ⚠️⚠️ THIS IS THE JUSTIFICATION FOR A CONTAINMENT GATE.** `YT_sdNStKd-fqE` already records that an element outside `IfcRelContainedInSpatialStructure` **silently vanishes** from viewers. This source adds that the error is *common in practice*, not exotic — a silent failure that occurs often is exactly what this project gates.

⚠️ **Our generator calls `spatial.assign_container`**, so it is probably correct today. *Probably* is the problem: nothing asserts it.

## 2. `IfcSpace` will bite eventually

> ***"if you did not encounter yet problems with spaces, I promise you are going to encounter at some point."*** [Stefan Catargiu]

He rates Bonsai among the best tools for the job *«because Bonsai has IFC native capabilities, meaning that it allows you to also modify, add, fix spaces»*, and says the spatial tool is deep enough for *«a full workshop only on this tool»*.

⚠️ **What he does NOT do is state what spaces BUY you.** The videos are about repairing spaces, not about why a model should carry them. **Open question 16 is therefore only partly answered**: we know spaces are troublesome and fixable, not whether we need them.

## 3. Transfer to this project

- ⚠️ **Add a containment assertion to the IFC check.** Cheap, and it guards a failure that is both silent and, per this source, common.
- **We have no `IfcSpace` today.** Our rooms live in canonical data. Before adding them we need the missing half — what they are *for* — which neither video supplies. Candidates from elsewhere: space boundaries for finish quantities, and room-scoped service containment.
- ⚠️ **Rule 3 caveat:** both videos are demonstrations of a repair workflow. The claim that the error is widespread rests on his support experience, which is plausible but unquantified.

## Source Notes
Stefan Catargiu, BIMvoice — two tutorials, 2025-03-29 and 2025-08-18, English original captions.
