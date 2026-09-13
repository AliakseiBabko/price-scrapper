# AI toolchain sources — triage and outcome, 2026-09-13

**Owner-supplied list of 11 videos**, delivered with the question of whether this source class needed its own knowledge-base folder. **Both questions were answered by the owner before processing**; this file records the triage, the per-source verdict, and what the batch actually produced.

## 1. The structural decision, made first because it gated the routing

The owner asked whether a new folder was needed for "how to work with AIs for processing construction data, how to create 2D/3D plans, how to calculate cost."

**Answer given, and the reasoning, is recorded in full in [[18_Digital_Toolchain/analysis/Change_Log|the new folder's Change Log]].** In short: **this revisits, and partly overturns, the [2026-09-08 Group C decision](design_toolchain_sources_triage_20260908.md) §5**, which routed the same class to `00_Master/`. That decision was sound when the class had zero processed sources; it had eleven by 2026-09-11.

**Decided: `18_Digital_Toolchain/` for GENERAL source-derived toolchain knowledge; `00_Master/` keeps this project's OWN toolchain decisions and status.** Same split `17_Design_and_Ergonomics/` has against `00_Master/Design_Concept.md`.

**⚠️⚠️ The decisive argument was mechanical and had not been visible in September**: `tools/check_page_sizes.py` excludes `00_Master` by design (`NUMBERED_FOLDER_RE = ^(?!00_)\d{2}_`), so `Drawing_Conventions_From_Practice.md` had been growing **ungated** at 243 lines with no fragmentation check ever run against it.

**Also decided**: two taxonomy buckets added to the intake wrapper (`Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`) — without them this content had no bucket and fell to `Other / Unclassified`.

## 2. ⚠️⚠️ The language finding, which had to be settled before any fetch

**Nine of the eleven sources are English-spoken; two are Russian.**

This vault's standing rule 1 exists to stop an **auto-translated English** track being taken for a Russian source. **Here it pointed the other way**: the pipeline's habitual `--languages ru,en` would have pulled **auto-translated Russian captions for nine English-spoken videos.**

**→ Each video was fetched with its own original language explicitly set**, and the `language` field in every `.meta.json` was verified after fetching. **The rule is "original language", not "Russian".**

Fetch discipline: **serialised, one at a time, 90 s spacing** (the 2026-08-30 batch used 75 s successfully), with an exit-code-2 circuit breaker armed for the whole phase. **11/11 succeeded, no rate-limit, no failures.**

## 3. Per-source verdict

| Video | Channel | Verdict | Yield |
| :--- | :--- | :--- | :--- |
| `ItW-ielFvGg` | Tim Fairley | **Full** — the batch's best source | 12 |
| `_k1jQBS4Nk8` | Tim Fairley | **Full** | 9 |
| `S77hdyyjTmA` | Tim Fairley | **Full** | 8 |
| `2eONA-6WVVI` | Меркулов / АМС | **Full**, high promotional ratio | 7 |
| `VcBohP2LbNM` | The AI Contractor | **Full** — lowest promotional ratio in the batch | 5 |
| `vmVvpKSSxWE` | Archi Vlogs | **Partial** — capability verdict discarded, observed failures kept | 4 |
| `6trAkQY5_kc` | Make Form | **Partial** — install walkthrough not routed | 3 |
| `la8Ml1fQfOg` | Urban Decoders | **Partial** — feature tour and model lineup discarded | 3 |
| `sujS9Mgveo4` | Sketchup Gurus | **Full** (1 minute long) | 2 |
| `EibFZPrtAp0` | Civil engineering | **Routed as an ANTI-PATTERN**, not as technique | 2 |
| `QLge-kb_L2I` | Мой Дом и Сад 3D | **Near-skip** — one framing kept, roundup discarded | 1 |

**Round 1 yield: 11 processed, 56 new facts, yield = 5.1 per video.** Above the 1.0 floor; no stop-and-ask triggered.

**⚠️ Four of the eleven are the same practitioner** (Fairley ×3 new, plus `3tAYEJTyUFY` from 2026-09-11). **Repeated claims across his videos are one consistent position, not corroboration** — flagged on every page that cites him.

## 4. Findings that generalise beyond this batch

1. **⚠️⚠️ A ONE-MINUTE VIDEO PREDICTS LOW VOLUME, NOT LOW VALUE.** `sujS9Mgveo4` was flagged a likely skip on the title-skim — 60 seconds, "perfect 3D" in the title. It was fetched anyway and **held the only measured dimensional-fidelity check in the entire batch** (610 drawn against 616 modelled), answering the exact question the 35-minute masterclass left hanging. **The masterclass measured nothing.** → **Duration and title hype are weak predictors; presence of a measurement is the signal.**
2. **⚠️⚠️ RECORDING WHAT A SOURCE FAILED TO PROVIDE IS WHAT MAKES ITS SEQUEL RECOGNISABLE.** `3tAYEJTyUFY`'s CSV row complained it had *"NO ACCURACY MEASUREMENT of any kind."* `ItW-ielFvGg` is the same workflow two months later **with the benchmark**. The gap note is what made the match obvious. → **Write the gap down, in the row, not just the finding.**
3. **⚠️ A BATCH CAN INVERT WHICH WAY A STANDING RULE POINTS.** See §2. → **Re-derive a rule's application per batch rather than applying its habitual form.**
4. **⚠️ A SOURCE CAN BE WORTH PROCESSING AS A NEGATIVE EXAMPLE.** `EibFZPrtAp0` performs, confidently and with no verification, precisely the failure the rest of the batch measures. **Recorded as a documented bad practice** — the same treatment the vault gives a self-flagged live-wiring demonstration.
5. **⚠️ THE VENDOR'S HEADLINE NUMBER HID THE USEFUL STRUCTURE.** "50× less tokens, 20% more accurate" is two separable purchases: **vector extraction buys the accuracy, the index buys the cost.** → **Decompose a compound performance claim before recording it.**

## 5. What the batch did NOT produce, stated plainly

- **No cost-calculation content of substance.** The owner's question named cost calculation; **the batch touches it only through quantity take-off as a data layer** (`S77hdyyjTmA`) and not at all as a costing method. **The cost engine remains the one genuinely absent tool identified in [`toolchain_gap_analysis_20260908.md`](toolchain_gap_analysis_20260908.md) §B, and nothing here closes it.**
- **No source ran `tools/youtube/extract_layout_frames.py`.** The owner authorised frame extraction "where it matters"; on reading the transcripts, **the value in all eleven turned out to be spoken architecture and measured numbers rather than on-screen sheet layouts** — unlike the 2026-09-08 RemPlanner/k_dmitry group, which was genuinely screencast-bound. **Recorded so the decision is visible rather than silently skipped.** ⚠️ **If any of these is revisited for its on-screen database schemas, frame extraction is the way in.**
- **No regulatory content anywhere.** Nothing routed to `16_Legal_and_Regulations/`.
- **No prices anywhere.** No USD conversion was owed for any source in the batch.

## 6. Open items this batch raises

- **⚠️ The `IfcRelConnectsPathElements` question gains a new argument.** Two sources independently state their element schema is copied from IFC. The 2026-09-11 round found the relation **unused anywhere in this repo** and decided against adopting it for wall corners. **That decision stands** ([`deep_research_review_geometry_20260911.md`](deep_research_review_geometry_20260911.md)); what is new is the weaker but real point that **an outsider reverse-engineering IFC by hand is an argument for reading the schema before inventing fields** — relevant when `data/canonical/` next grows a field.
- **⚠️ Per-measurement confidence tiers are not currently an explicit stored field** in `data/canonical/`. Provenance is required; a *reliability tier* (counted / read-from-schedule / scaled) is not. **Cheap to add, and it is the one idea from this batch this project does not already have in some form.** Not actioned — an owner decision.
