---
source_type: video transcript (designer's client-facing progress report — doors and partition positions as a single coupled planning problem, two variants presented)
source_url: https://www.youtube.com/watch?v=FRKr9X3AFfY
video_id: FRKr9X3AFfY
transcript_file: _Archive/processed_sources/20260908_kdmitry_doors_partitions_planning_a3f0a921.txt
fetched: 2026-09-08 (anonymous, yt-dlp --write-auto-subs --sub-langs ru-orig)
upload_date: 2026-02-18 (confirmed via yt-dlp metadata)
duration: 7:24
channel: "Дизайнер Дмитрий К" (@k_dmitry, 372 subscribers) — practising interior designer, Moscow
source_metadata_location: Moscow, Кожуховская (stated in transcript)
jurisdiction: Russia — standing rule 4 applies
language: ru (ru-orig auto-generated)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 16
promotional_ratio: low
corroborates_existing: false
---

# Extraction Note — Дизайнер Дмитрий К: "Как начать планировать небольшую квартиру: выбор дверей и перегородок" (YouTube FRKr9X3AFfY)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

7½ minutes on one coupled question — *«двери и перегородки, их положение в квартире»* — treated as a single problem rather than two. Same flat as `YT_TJVXUCKQ1UU`. Promotional ratio low. The family is described as *«многодетная»*, which drives one of the two variants.

## Value-filter verdict

**Full extraction.** Contains the round's most directly usable machine-readable rule, with a parameter.

## Doors / Trim — ⚠️⚠️ door casing width constrains partition position

**The finding, and it is a genuine dependency our model does not encode:**

- **Because the doors are classical, their наличники (casings) will be wide — he estimates «сантиметров 8–10 минимум».** ⚠️ Candidate figure, single ASR mention, and stated as his own estimate for this style.
- **Therefore a partition must be moved away from a corner or set deeper, so that casings have room on BOTH sides of a door and are not cut** — *«чтобы не было подрезания наличников, чтобы всё смотрелось эстетично, перегородку нужно сдвинуть немножко глубже и расположить дверь симметрично»*.
- **He applies this in three separate places** on one flat: at the kitchen, at the corridor door cluster, and at a junction where two doors adjoin — *«додвигаем перегородку от угла примыкания двух дверей, для того чтобы была возможность сделать наличники с одной и с другой стороны у всех дверей, которые участвуют в этой проходной зоне»*.
- ⚠️ **→ The rule generalises as: in any проходная зона, the position of a partition is constrained by the trim width of every door opening onto it, on both sides of each opening.** Routed to `data/layout_rules/rules.jsonl`. **This is a "connect the dots" derivation of the same shape as the door-swing/switch rule in `YT_DI5GAV64mnU` — a finish decision propagating back into structural geometry.**

## Doors / Trim — modelling sequence and door types

- **He models doors as условные (conventional) models in BOTH open and closed states**, so the swing envelope is visible on the plan and in 3D. Three mechanisms modelled: **распашные** (conventional swing), **рото / реверсивные** (rotating within the opening on a rail), and **книжка** (bi-fold, folding to either side).
- ⚠️ **The doors are modelled WITHOUT наличники, because casings are placed separately at the stylisation stage** — *«двери без наличников… наличники я буду выставлять отдельно»*, and the actual appearance is chosen later *«на этапе комплектации»*. **A modelling-sequence convention: swing envelope first, trim as a separate later layer** — which is notable given that the trim is what constrains the partition (above). The dependency is known and reserved for, without the object being chosen.

**Рото/reversible doors — the tradeoff, both sides stated:**

- **Benefit**: they take less room on each side, *«что экономит места в проходах»* — three doors in one narrow spot occupy little passage space.
- ⚠️ **Cost, which he states himself rather than omitting**: *«этими дверями нужно пользоваться аккуратнее, потому что у них более требовательный к аккуратности использования механизм открывания и закрывания»*. **A durability/handling caveat from someone specifying them.**
- **Where he reaches for them**: the existing wet-room configuration forces **two such doors into one corridor**; and where a wardrobe leaves no room to swing a door inside the corridor, the options he names are **opening into the room instead, or a рото door**, flagged as a client discussion rather than decided.
- **A кладовая door needs only 80 cm**, bi-folding toward the простенок. ⚠️ Candidate figure.
- **Existing built-in wardrobes are to be upgraded with new fronts only, so he deliberately has not drawn their doors yet** — deferred to the furniture-design stage. **Same "reserve the volume, choose the object later" staging as `YT_DI5GAV64mnU`.**

## Walls / Ceilings — what can be moved, and why he knows

- **Only two walls in the flat are load-bearing; every other partition was installed as non-load-bearing, so they can be shifted** — *«у нас в этой квартире только вот несущая стена здесь и здесь… все эти перегородки установлены были как ненесущие, соответственно, их можно немножечко сдвигать»*. **Establishing which walls are structural is the precondition for the whole exercise.**
- **He levels out a jog (уступ) in the old partition line to widen a corridor** — *«практически уверен, что её можно выровнять, тем самым немножечко расширить ширину вот этого коридора»*. ⚠️ Hedged by him («практически уверен»), so recorded as an intention, not a verified move.

## Planning Rules — two-variant presentation with the tradeoff stated

- **He presents a second layout variant differing in exactly one decision — combining the two wet rooms — and states the case on both sides:**
  - **Against**: the family is large, *«людей много, поэтому два санузла — это хорошо»*.
  - **For**: the two are so small, and there is so much to fit into the flat, that the alternative *«нужно обязательно рассмотреть»*. The gains he enumerates are concrete — **the thickness of the dividing wall is recovered; one of the two doors disappears, which frees wall runs on both sides; and the combined room additionally absorbs the corridor jog, so it ends up larger in area.**
- ⚠️ **The methodological rule he closes on, and it is an argument about sequencing that bears on our roadmap**: *«принять окончательные решения по планировке можно только сделав расположение всей мебели, обстановки, сантехники»* — **a layout cannot be frozen until all furniture, fittings and plumbing are placed.**
  - **→ This says `cap4` (furniture and appliances as real objects) is a PREREQUISITE for freezing a layout, not a later decoration step.** Corroborated by `YT_TJVXUCKQ1UU`, where the stated next task is to furnish every room completely before seeking approval. **Worth arguing with, since our own layout is described as largely decided.**
- **Variants are presented over the original layout as a visible underlay** — *«показываю изначальную планировку, чтобы была видна разница, в виде подложки»*. **Matches our own convention that dashed lines show the original partitions on every variant sheet** (`Planning_Project_Deliverable_Set.md`) — independent corroboration of a convention we already hold.

## Unclear / Needs Confirmation

- The 8–10 cm casing width is his estimate for a classical style, single ASR mention, and will vary by product. **The rule is the dependency; the number is a placeholder until a product is chosen.**
- Whether the уступ he intends to level is genuinely non-structural — he says «практически уверен», which is not a verification.
- He does not say what рото door mechanisms cost, nor name a manufacturer.
