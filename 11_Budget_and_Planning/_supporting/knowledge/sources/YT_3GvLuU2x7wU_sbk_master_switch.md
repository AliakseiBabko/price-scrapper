---
source_type: video transcript (turnkey renovation company owner, short single-concept explainer, Russian, ASR auto-generated captions — no punctuation)
source_url: https://www.youtube.com/watch?v=3GvLuU2x7wU
video_id: 3GvLuU2x7wU
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 5bcca7891b8b1aa03ccb7feaa8f0f669da40abeddee59c345c8d442858b4431e)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated captions)
upload_date: 2021-12-06 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation company — St. Petersburg
regional_applicability: general technique, not region-specific
currency: RUB, converted at trailing-6-month USD/RUB mean before 2021-12-06 (72.8923 RUB/USD, via tools/pricing/currency_converter.py)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 3
promotional_ratio: medium (short single-CTA format, thin on independent content)
corroborates_existing: true (same underlying feature as this store's existing "vacation/away mode" panel note on Cable_Circuits_and_Panel_Design.md, from Konstantin Kruglov/Ontario — that note already covers the exception list of always-on loads; this video adds the physical implementation parts list and a cost figure)
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ): "Master Switch — Turn Off All Lighting From One Place" (YouTube 3GvLuU2x7wU)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 7, video 3 of 8.** A very short (2-minute) single-concept explainer video — thin by construction, not a satire/comedy case (matches the channel's own genuinely-short technique-tip format). Applied the value filter: genuinely new content is limited to the physical parts list and cost; the underlying "switch off everything except always-on loads" concept is already recorded in this store from a different channel (Kruglov/Ontario's vacation-mode note). Extracted as **partial** — only the non-duplicate facts below.

## Electrical — Master Switch: Physical Implementation and Cost

- **A "master switch" (мастер-выключатель) is a single wall switch wired through a contactor to cut all lighting circuits (and optionally selected outlet circuits) with one press on the way out the door** — functionally the same single-press "everything off" concept as this store's existing vacation/away-mode panel note (Konstantin Kruglov/Ontario, `Cable_Circuits_and_Panel_Design.md`), but implemented here as a dedicated physical switch rather than a panel-level mode setting.
- **⚠️ Named exclusion list, matching the existing vacation-mode note**: fridge, router, and air conditioner (implicitly, any circuit deliberately wired outside the master-switch's contactor) stay powered regardless of the master switch being pressed — the same always-on exception logic already recorded from Kruglov/Ontario, now independently corroborated from a second company.
- **Stated parts list and cost**: the switch itself, a contactor, and a breaker — total cited cost **≈3,000 RUB (≈$40)** — framed as a low-cost addition not worth skipping for the convenience/peace-of-mind it buys (e.g. certainty that a forgotten iron plugged into a master-switched outlet is not still powered after leaving).

## Assumptions / Uncertainties

- No region-specific claim in this video; general technique.
- Cost figure (≈3,000 RUB) is the speaker's own stated illustrative price, `single-account`/`unverified`, not itemized by component.
- This video does not name "vacation mode" or reference any panel-level smart/scene-based implementation — it describes a simpler always-available hardware switch, which may or may not be how Kruglov/Ontario's vacation mode is physically implemented in that source; treated as a compatible but not confirmed-identical implementation.

## Target Page(s)

- **`12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md`** — added as a short corroborating note under/near the existing vacation/away-mode panel-modes section, with the parts list and cost as the genuinely new addition.

## Relevance to This Project's Topic

Low-yield due to video length and conceptual overlap with existing content, but the parts list (switch + contactor + breaker) and concrete ≈3,000 RUB cost are new, checkable additions to an already-recorded concept — worth a short corroborating addition rather than a full skip.
