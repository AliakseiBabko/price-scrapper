---
source_type: video transcript (single-speaker technical explainer, Russian, ASR auto-generated captions, no punctuation, numeric/terminal details heavily garbled)
source_url: https://www.youtube.com/watch?v=VXfpDJruyVs
video_id: VXfpDJruyVs
transcript_file: 90_Archive/processed_sources/20260804_two_way_switch_wiring_d19dbb7b.txt
fetched: 2026-08-04
upload_date: 2019-06-02
channel: Alexey Zemskov / ZEMS group (Zemstandart/Zemsproekt/Zemsremont)
regional_applicability: Belarus/Russia region (channel's usual market); no specific city named — secondary reference
currency: N/A (no pricing stated)
language: ru (ASR auto-generated, no punctuation, wiring/terminal-numbering passages especially garbled)
extraction_taxonomy: custom (renovation planning)
---

# Extraction Note — How Two-Way and Intermediate Switches Work and How to Wire Them

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata

- Single-speaker technical explainer on two-way (проходной) and intermediate (перекрестный) switch wiring, illustrated with a physical demo. Sign-off confirms channel ("как алексей земсков до свидания" — garbled but recognizable).
- **Transcription quality warning**: the specific step-by-step wiring/terminal-numbering portions of the transcript are badly garbled (ASR mangling of technical vocabulary and numbers); only the general conceptual claims below are extracted with reasonable confidence. Do not treat any terminal-numbering detail as reliable — none is included here.

## Durable Facts

- **Standard switch**: a simple break in the circuit — 2 terminals (1 wire in, 1 out) — either fully open or fully closed, no other state.
- **Two-way/проходной switch**: has 3 terminals (1 common input, 2 outputs) and must be used in **pairs**; it routes the incoming wire to one of two output wires depending on toggle position. A single проходной switch's own physical position does **not** by itself indicate whether the controlled light is on or off — the lamp's state depends on the combination of both paired switches' positions. This matches the caveat stated in `YT_8eECI5sWEy4_switch_placement_general_rules.md` from this same batch.
- General wiring principle (numeric terminal labeling excluded due to transcription quality): phase enters one проходной switch, travels via two "traveler" wires to the second проходной switch, which then feeds the lamp; flipping either switch changes which traveler wire is live, changing the lamp's state.
- **Intermediate/перекрестный switch**: used when a light must be controlled from **more than 2** locations. Additional перекрестный switches (4-terminal: 2 in / 2 out) are inserted between the two end проходной switches — described as chainable to an unlimited number of intermediate points. The two end switches always remain проходной (2 total, never more); every switch between them must be the 4-terminal перекрестный type — a plain 3-terminal проходной switch cannot be substituted mid-chain and will not function correctly if used there. This is consistent with the switch-type explanation in `YT_PIYzs2b4UDU_buying_finish_electrics.md` from this batch.
- **Anti-pattern flagged**: electricians who twist bare wires together and wrap them with tape instead of using proper junction connectors (e.g. terminal blocks/wire nuts), or who stuff such loose twisted connections into a ceiling void instead of housing them inside a proper junction box, are called out as a quality red flag — the speaker's explicit advice is to fire such an electrician and hire a competent one. `unverified`, opinion, but a concrete/checkable installation anti-pattern.
- States his own normal practice is to mount junction/distribution boxes at ceiling level, while switches themselves go wherever is convenient for the client on the wall. `single-account`

## Numeric Data

None reliably extractable — the transcript's numeric/terminal-count passages are too garbled to trust (see transcription quality warning above).

## Assumptions / Uncertainties

- All wiring "how-to" specifics beyond the conceptual switch-type behavior are omitted here due to transcription garbling; a reader needing actual wiring instructions should consult a clean/verified source, not this note.

## Relevance to This Project's Topic

Confirms and slightly extends the two-way/intermediate switch terminology used elsewhere in this batch, and adds one checkable installation-quality anti-pattern (twisted/taped wire joints outside a proper junction box). Same channel as the rest of the batch — `single-account`.
