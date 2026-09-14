---
source_type: video transcript (renovation company - 18 rules for flat electrical installation, shown on a real object)
source_url: https://www.youtube.com/watch?v=JpGKJz8WDew
video_id: JpGKJz8WDew
transcript_file: _Archive/processed_sources/20260914_remcraft_flat_electrics_rules_87a42f2f.txt
fetched: 2026-09-14 via youtube-transcript-api (ru, forced per standing rule 1); ⚠️ first attempt failed on a DNS error and was re-fetched
upload_date: 2025-02-15 (from the yt-dlp sidecar, --fetch-upload-date; actually run)
channel: REMCRAFT - дизайн и ремонт
source_title: "ИДЕАЛЬНАЯ электрика в квартире. Современные стандарты качественного электромонтажа"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Engineering / Electrical`)
fact_yield: 28
promotional_ratio: medium - their own object throughout, and the implicit argument is "hire us"; no pricing, no CTA mid-video
corroborates_existing: partly
contradicts_existing: ⚠️ true - he corrects a widely-held reading of a rule, and takes the opposite side of a trade-off from Шемчук
region: Russia (ПУЭ cited) - no price figures usable; one cable-overrun cost mentioned but cut off in the captions
---

# Source Note - REMCRAFT: ⚠️⚠️ five reasons wiring belongs on the CEILING, and the шлейф prohibition is narrower than everyone thinks (YouTube JpGKJz8WDew)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none)

⚠️ **173k views, 2025, filmed on their own live object with the cables visible. A contractor arguing for the method they sell — flagged — but the arguments are mechanical and mostly checkable.**

## ⚠️⚠️ 1. «Вода внизу, электрика наверху» — five reasons, and one the vault did not have

**His first and most emphatic rule: run the wiring along the CEILING.**

1. **⚠️⚠️ THE CLEARANCE RULE MAKES FLOOR WIRING NON-COMPLIANT.** Per ПУЭ, a water pipe and an electrical cable must keep **≥5 cm at a perpendicular crossing and ≥10 cm running parallel.** With all the plumbing in the floor and a screed usually **no more than 10 cm total**, 5 cm is simply not available. *«Можно просто забить на это правило… мы для себя решили, что всё-таки будем придерживаться правил.»*
2. **⚠️ Ceiling runs go WITHOUT corrugated conduit; floor runs cannot.** At realistic densities you end up with a multi-layer bundle of conduit down the corridor to the panel — **and screed needs a rigid base, so it would be bearing on conduit.** *«Так делать нельзя.»*
3. **⚠️ Shadow and hidden skirtings** (теневой / скрытый плинтус) are now common and already need a deep recess; wiring arriving from the floor would force chasing deeper still above them — *«пол стены выдолбить»*.
4. **⚠️⚠️ WATERPROOFING — the reason I had not seen stated before.** With floor wiring, a chase rises to every point from the floor. **On his object that is 100+ points at which the waterproofing must be breached and then patched.** High human-factor exposure and a correspondingly high leak probability.
5. **⚠️ With every chase strictly above, you know where cable is without a drawing** — look at a back-box: nothing below it, chase above it.

> **⚠️⚠️ AND HE NAMES THE REAL REASON PEOPLE DO IT IN THE FLOOR, against his own trade: it is simply easier. *«Ты сидишь на полу… значительно сложнее» работать на потолке,* and greater labour means greater cost.** **He notes companies do floor wiring and market it as excellent.**
>
> ⚠️⚠️ **JURISDICTION: ПУЭ is Russian. Flagged, and deliberately NOT routed to `16_Legal_and_Regulations/`, which is Belarus-only.** **The 5 cm / 10 cm separations are recorded as the shape of the constraint; the Belarusian equivalent has not been checked here.**

## ⚠️⚠️ 2. The ШЛЕЙФ myth — the prohibition is real but narrower than it is quoted

> **The widespread claim is that daisy-chaining sockets (шлейф) is forbidden. His correction: what ПУЭ forbids is joining PROTECTIVE conductors — the EARTH — in a daisy chain. Some people extend that to phase and neutral, which the rules do not say.**
>
> **Their implementation: the earth conductor passes THROUGH each back-box with a separate branch to each socket, and is never broken.**

> **→ ⚠️⚠️ A precise, checkable scope correction rather than a "trust me" claim, and it is exactly the sort of half-remembered rule that costs money when over-applied.** ⚠️ **Russian ПУЭ again — same jurisdiction flag. What transfers is the DISTINCTION between the protective conductor and the live conductors, which is a physical-safety argument rather than a local drafting quirk.**

## ⚠️⚠️ 3. Junction boxes on the ceiling, or distribution at the switch block — a real trade-off, and he takes the opposite side from Шемчук

**His choice: bring every cable down and make the joints at the switch block.**

| | **Ceiling junction boxes** | **Distribution at the switch block (his choice)** |
| :--- | :--- | :--- |
| Later re-assignment of which switch runs which zone | **not possible once commuted** | **⚠️ possible — swap switches and zones freely** |
| Cable used | less | **⚠️ more — on this flat, 140 m extra lighting cable** |

> **→ ⚠️⚠️ PAIR THIS WITH [[_Sources/YT_0c-QhBDQMWE_shemchuk_technical_design_album_series|Шемчук]] IN THIS SAME BATCH, WHO DOES THE OPPOSITE — ceiling junction boxes, with their positions documented so the owner can find them behind a stretch ceiling in 10–15 years.**
>
> **Both are reasoned and they optimise different things: Шемчук buys cheapness and documents his way out of the maintenance problem; REMCRAFT buys reconfigurability and pays 140 m of cable for it.** **Recorded as a genuine perspectives split rather than a right answer — and the deciding question is whether you expect to change the lighting control after the works.**

## ⚠️ 4. Safety and commissioning practices worth copying

- **⚠️⚠️ ISOLATE EVERY LIVE-CAPABLE CABLE END DURING THE WORKS, even with every line RCD-protected.** During a renovation someone switches on a breaker marked *«не включать»*, or simply switches them all — and every tail is live. **Anyone on site is exposed: a tradesman, a subcontractor, the client.** He notes many only RCD-protect the socket circuits, which is exactly when an un-isolated tail is dangerous.
- **⚠️ Cable marking must name the GROUP the cable belongs to** in the distribution scheme — not *«что вижу, то пою»*, "this one's for that lamp", which leaves you guessing later. **Corroborates Шемчук's cable schedule from the other direction.**
- **⚠️⚠️ TEMPORARY SOCKETS AND SWITCHES, wired from the panel during the works, so the electrics can actually be ACCEPTED** — you press a switch and a lamp lights — rather than being handed *«куча соплей»* of loose tails that nobody can verify.
- **⚠️⚠️ POSITIONAL ACCURACY TO THE CENTIMETRE, and it has to be caught before plastering.** A switch has to sit truly centred relative to a door opening **counted WITH its architrave** and an adjacent wardrobe. **→ The point is the coordination: the architrave width and the wardrobe position must be known at first fix, which is the same "decide the finishes before the services" pattern this batch produced three other times.**
- **⚠️ Cable without conduit in NON-COMBUSTIBLE bases is permitted**, and he addresses the folk belief that bare cable stains walls through the plaster: in ~20 years of practice they have never seen it. ⚠️ **An absence-of-evidence claim from one firm.**

## Routing

- §1 → [[12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing|Rough Electrical Sequencing]] and [[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Cable Circuits & Panel Design]]
- §2 → [[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Cable Circuits & Panel Design]]
- §3 → same page, as a perspectives block against Шемчук
- §4 → [[12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing|Rough Electrical Sequencing]]

## What was NOT taken

- The implicit "hire us" framing and the object tour.
- **⚠️ The cable-overrun cost figure, which the captions cut off mid-sentence** — the 140 m quantity is kept, the money is not.
- **Nothing routed to `16_Legal_and_Regulations/`** — ПУЭ is Russian; see §1 and §2 for the claims flagged in place.
