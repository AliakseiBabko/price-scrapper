# v0 vector extraction — the owner's marked-up review, transcribed

**Created 2026-09-11.** The owner annotated [`_Drawings/review/v0_vector_extraction.png`](../../_Drawings/review/v0_vector_extraction.png) with 14 red labels and ~16 arrows. **This file transcribes them against the solid IDs on the drawing so they can be acted on and checked off.** The annotated PNG is committed in place per `_Drawings/README.md` — git holds the unannotated render.

**Nothing here has been implemented.** Several items contradict current canonical data, and two need the owner's confirmation before anything is changed — see §5.

**Status of the thing being reviewed**: `data/canonical/v0_named_walls_placed.json` carries `status: "DRAFT - not owner-reviewed."` **This review is that review.**

---

## 1. ❌ False positives — drawn as elements, are not walls

| # | Where | The comment | What the extraction currently says |
| :-- | :--- | :--- | :--- |
| 1 | **S37**, the thin strip down the far right edge | *"this thin areat is not a wall, just a line of the vector drawing"* | The legend's **"1 second leaf"** — *"a second leaf shares a run and a face with a wall already named — S37 is the party wall's other side"* |
| 2 | The small red box at the **top of S34 R5**, beside the `250` / `75` dimension strings | *"this is not a wall section, just dimentions from the vector drawing"* | One of the **4 bridged doorways** |
| 3 | The red box on the left wall **below S16 M2** | *"not a wall section, it is M2, no insulation"* | Also one of the **4 bridged doorways** |

> [!WARNING]
> **⚠️ Two of the four "bridged doorways" are not doorways at all.** That category is **50 % wrong**, and both false ones come from the same cause — a gap in the hatching that is dimension linework or a drawing artefact rather than an opening. **Whatever rule bridges a gap needs to distinguish a real reveal from a line.**

## 2. ➕ Missing — present on the drawing, absent from the extraction

| # | Where | The comment |
| :-- | :--- | :--- |
| 4 | West end of **S08 G6**, the red bridged box between `S26 R4` and `S08 G6` | *"missing door opening"* |
| 5 | Right of **S07 G4d** / at **G4G4d**, the red box toward `S26 R4` | *"missing door opening"* |
| 6 | Running **south from the `MB_R8` corner** — a hatched wall in the underlay, boxed in red by the owner, that no solid claimed | *"missing wall with external insulation 150 mm"* |
| 7 | At the **`MB_R9`** corner, bottom right — a break in the orange band | *"missing section of external insulation 120 mm"* |
| 8 | The left wall segment **below the red box under S16 M2** | *"this is a separate wall section with external insulation 150 mm"* |

> **⚠️ On items 4 and 5**: the drawing bridges **4** doorways but places only **3** openings (`O2`, `O3`, `O4`). Items 4 and 5 are two of the bridged gaps that never became opening elements — so the bridge/place split is the defect, not the detection.
>
> **⚠️ Item 6 is the largest single miss**: a whole wall, not a sliver.

## 3. ⚠️ Overlaps — two different kinds, and they should not be conflated

**Wall against wall (3):**

| # | Where | The comment |
| :-- | :--- | :--- |
| 9 | **Left end of `S10 G4b`**, running into `S18 G4a+R1b+R6` | *"wall overlap"* |
| 10 | **Left end of `S07 G4d`**, into the same vertical wall | *"wall overlap"* |
| 11 | **Top of `S32 R9`** | *"wall overlap"* |

**Wall against the insulation band (3 arrowheads, 2 labels):**

| # | Where | The comment |
| :-- | :--- | :--- |
| 12 | **`M2_MA`** corner, bottom left | *"overlapping of the wall and expernal insulation layer"* |
| 13 | **`MA_R8`** corner | *(same label, second arrowhead)* |
| 14 | **`S32 R9` / `R9` junction**, bottom right | *"overlapping of the wall and expernal insulation layer"* |

⚠️ **`check_wall_junctions.py` and `check_dxf_closure.py` both PASS on this model today.** So either these overlaps are in the *render* rather than in the gated geometry, or they are of a kind neither gate looks for — **most likely the second, since neither gate tests a wall against an insulation band.** That has to be established before anything is "fixed", or the fix will chase a drawing artefact.

## 3b. ✅ RESOLVED 2026-09-11 — the overlaps are in the SOLIDS, not in the model

The owner pressed on these, naming them precisely: *"R1a and G4a, and the walls of the bathroom, G4b, G4d, overlapping with that G4a wall… R9 overlaps with G7."* **Every one is real, and none of them is a defect in the model.**

**Measured on the DXF — the walls themselves:**

> **Exactly ONE wall pair overlaps in the whole model: `M2 × MA`, 200.0 × 299.7 mm.** That is the sanctioned `C_M2_MA` corner, where M2 owns 300 mm onto MA. **Every pair he named — R1a/G4a, G4b/G4a, G4d/G4a, R9/G7 — has zero overlap in the DXF.**

**Measured on the vector solids — what the render actually draws:**

| claimed solids | carrying | overlap |
| :--- | :--- | :--- |
| `S07` × `S18` | G4d × (R1b+R6+**G4a**) | 239.2 × 120.0 mm = 0.0287 m² |
| `S10` × `S18` | G4b × (R1b+R6+**G4a**) | 239.2 × 120.0 mm = 0.0287 m² |
| `S32` × `S33` | **R9** × **G7** | 75.0 × 820.0 mm = 0.0615 m² |
| `S14` × `S36` | (**R1a**+R3+G2+G3) × (R2+R7+G5) | 250.1 × 249.9 mm = 0.0625 m² |

**All four of his reports land on a real solid-on-solid overlap. He was reading the picture correctly.**

**What the model already did about them** — `v0_named_walls_placed.json` → `overlap_resolution`, `before: 3, after: 0`:

- `R9` kept, `G7` trimmed — *"nested same-axis solid (extraction artefact)"*
- `R1b` kept, `G4b` trimmed — *"corner owner by thicker-then-longer"*
- `G4a` kept, `G4d` trimmed — same rule

**And the fourth, `S14 × S36` at 250 × 250 mm, is not in that list because it is not an error: it is the `C_G3_R2` CORNER**, which the closure gate reports as *"ok C_G3_R2 solid, 625 cells"* and which `wall_corners.csv` owns exactly once. **Two solids sharing a corner square is what a corner looks like.**

> [!WARNING]
> **⚠️⚠️ SO THIS IS THE SAME CLASS OF PROBLEM AS M6b, FOR THE THIRD TIME: the render shows a PRE-RESOLUTION state and does not say so.** It draws the raw hatched solids. The placement step trims three of these overlaps and the ledger owns the fourth, so the model is clean — but the picture still shows the overlap, and the owner has now reported it twice.
>
> **The render's honest caption — *"this is a picture of the EXTRACTION, not evidence it is right"* — is true and is not enough.** It does not distinguish *"the extraction found a problem that is still open"* from *"the extraction found a problem the model already fixed"*, and those demand opposite responses from a reviewer.

⚠️ **One figure to check, not yet chased**: the resolution records the R9/G7 overlap as **75.0 × 570.0 mm**; measured on the raw solids it is **75.0 × 820.0 mm**. The 75 matches exactly; the length differs by 250 mm, which is one wall thickness — so probably a definitional difference over whether a corner is included. **Worth confirming, because it is the kind of 250 mm that this project has been bitten by before.**

## 1b. ✅ RESOLVED 2026-09-11 — S37 is the same wall as S36, read twice

The owner, pressing on the thin strip at the far right: *"what is it? It's a thin layer. It should be so… it should be just one wall, like G3_R2… then it goes to S37. It's strange."*

**He is right, and the geometry says so unambiguously:**

| solid | axis | thickness | faces | run |
| :--- | :--- | :--- | :--- | :--- |
| **`S36`** (claimed, carries R2+R7+G5) | NS | **250.1 mm** | 12695.9 … **12946.0** | 8530.6 … 16261.6 |
| **`S37`** (was "second leaf") | NS | **297.6 mm** | 12695.9 … **12993.5** | 8530.6 … 16261.6 |

**Identical run. Identical low face. S37 simply reaches 47.5 mm further — to 12993.5, which is the flat envelope's own x-max.** And `wall_blocks.csv` records **R2 at 250 mm**, matching S36 and not S37.

**→ S37 is the same wall read a second time, 47.5 mm fatter because it swallowed the plan's boundary line. It is not a second leaf.**

**The classifier's rule was too weak, and the fix is a rule it already had elsewhere.** It called anything sharing a wall's axis, most of its run, and one of its faces a *second leaf*. **It never asked whether the solid NESTS one already claimed.**

- **A genuine second leaf ABUTS** — shares one face, lies on the far side of it.
- **A duplicate NESTS** — one face range contains the other over the same run.

That is exactly the test `overlap_resolution` already applies as *"nested same-axis solid (extraction artefact)"*; **it had simply never been applied in the classifier.** The render now reports **"1 same wall as S36, read twice"** in place of the wrong **"1 second leaf"** — and it names the partner, because *"same wall as S36"* is checkable by a reader and *"artefact"* is not.

## 4. ⭐⭐ The rule behind most of the above

**Two arrows, to the `MA_R8` and `MB_R8` corners:**

> ### *"walls should touth other walls; insilations fill in the gaps; not a layer between walls"*

**This is a modelling rule, not a defect report, and it explains items 12–14.** The insulation is currently drawn as a **band that separates** two walls at a corner; the owner's model is that **walls meet walls, and insulation fills whatever gap is left over** — it is never the thing in between.

> [!IMPORTANT]
> **⚠️⚠️ THIS REFINES THE 2026-09-10 INSTRUCTION AND NEEDS TO BE RECORDED AS SUCH.** `project_decisions.md` quotes the owner from 2026-09-10: *"still that M2 is not touching MA. See the gap. There shouldn't be gaps. There should be an insulation layer, which is outside — 70 millimetres thick. I want you to draw this external insulation layer instead of leaving the gap."*
>
> **That was read as: draw the insulation into the gap. The correction is: the walls themselves should have been made to touch, and insulation is what fills what remains — an external skin, not a spacer.** Same complaint ("there shouldn't be gaps"), different remedy. **Whoever implements this must not read the September 10 quote alone.**

## 5. ✅ ANSWERED by the owner, 2026-09-11 — with a drawing and a third correction

### 5a. The insulation thicknesses are a standard detail, and our own record already agrees

**Evidence supplied**: a screenshot of the developer's drawing for **a different apartment in the same building, same constructor, same dimensions** — showing `120` and `150` dimension strings against a concrete column, with the insulation layer highlighted.

**His reading of it, verbatim in substance**: the **long face** of the concrete column is covered with **150 mm**; its **edge/end face** takes **120 mm**; and where the wall is a **300 mm aerated-concrete block**, the insulation is **70 mm**. *"This is kind of standard approach… 120 is also a standard thickness, but for specific places."*

⚠️ **Checked against `data/canonical/wall_blocks.csv`, and it matches exactly — the pattern was already in our data, unnamed:**

| wall | class | thickness | insulation | matches his rule |
| :--- | :--- | :--- | :--- | :--- |
| `MA`, `MB`, `MC` | `external` | **300** | **70** | ✅ 300 block → 70 |
| `R8`, `R9` | `concrete` | **250** | **150** | ✅ column long face → 150 |
| `M2` | `loggia_enclosure` | 200 | **0** | ✅ *"it is M2, no insulation"* (item 3) |
| **column END face** | — | — | **120** | ⚠️ **a case our record does not have at all** |

**→ So 120 mm is not a new thickness to justify; it is the third member of a detail we had two-thirds of.** It resolves item 7 (*"missing section of external insulation 120 mm"* at `MB_R9`) as the **return face of column R9**.

> [!WARNING]
> **⚠️ PROVENANCE, and it must travel with these figures: the 120/150/70 pattern is read off ANOTHER UNIT'S drawing, not this flat's own plan.** Same building, same developer, same dimensions — which makes it strong evidence of a standard detail, and the same standing this vault gives `_Survey/`. **It is not the same standing as a figure printed on our own sheet.** Any band placed on this basis should record `status` accordingly rather than `from_drawing`, which currently means *this* drawing.

### 5b. ✅ M6b confirmed — and the data confirms it three ways over

The owner: *"This is exactly the M6b section which is missing."*

**Independently verified, not taken on his word alone:**

1. **`M6b` is the only wall in `unmatched`** in `v0_named_walls_placed.json`, and its `solid_id` is **`None`** — the single named wall the extraction never attached to any solid. **It is literally the missing wall.**
2. Its **`clear_mm` is 1170**, and **`1 170` is the dimension printed on the plan immediately beside the owner's red box** for item 6 (*"missing wall with external insulation 150 mm"*).
3. `M2` beside it records `insulation_mm: 0`, matching his separate note that the red box there *"is M2, no insulation"*.

**→ `M6b` gains geometry, and its insulation becomes 150 mm — closing the `unresolved` entry that has carried `70.0` with empty evidence on both sides.**

> [!CAUTION]
> **⚠️ ONE TENSION TO PUT BACK TO HIM BEFORE WRITING IT.** `M6b` is recorded as **200 mm, class `loggia_enclosure`** — and his own rule maps **150 mm to a 250 mm concrete column**, not to a 200 mm loggia enclosure. Its neighbour `M2`, same class and thickness, carries **0**.
>
> **So one of three things is true**: `M6b`'s thickness or class is wrong in `wall_blocks.csv`; or `M6b` is a genuine exception; or items 6 and 8 are two different walls and only one of them is `M6b`. **Do not write 150 onto a 200 mm loggia enclosure without settling which.**

### 5d. ⚠️⚠️ CORRECTION 2026-09-11 — M6b IS NOT MISSING FROM THE MODEL, and the picture is what was wrong

**The owner, asked whether M6b is a 250 mm concrete column:** *"No. M6b is the external wall of the loggia. This is not a concrete slab. This is 200 mm thick aerated concrete wall with external insulation."*

**So the tension in §5b dissolves — and so does my inference.** I had read his pattern as *150 mm belongs to a 250 mm concrete column*. **That was an over-generalisation of his words; 150 belongs to M6b too, and M6b is 200 mm aerated block.** Its thickness is not in doubt either: `wall_blocks.csv` records **THICKNESS OWNER-CONFIRMED 2026-09-10 at 200 mm**.

**⚠️ And checking the model rather than the picture produced the bigger correction:**

| Check | Result |
| :--- | :--- |
| Is M6b in `wall_blocks.csv`? | **Yes** — 200 mm, `loggia_enclosure`, clear 1170 |
| Is M6b in the exported DXF? | **Yes** — all **25** named walls are present. M6b sits at x **5931.0–6131.0**, y **6120.7–7560.6**, NS axis |
| Is M6b in `v0_named_walls_placed.json`? | **Yes**, but with **`solid_id: None`** — the **only** wall in `unmatched` |
| Does `render_vector_extraction.py` draw it? | ❌ **No, and it structurally cannot.** The render iterates over *vector solids*; before today it had no concept of a wall placed by directive |

> [!WARNING]
> **⚠️⚠️ SO THE "MISSING WALL" IS A RENDERING DEFECT, NOT A MODEL DEFECT.** The wall exists in the record and in the DXF. **It is invisible on the one picture the owner was asked to review, and a drawing that silently omits an element it cannot show is indistinguishable from one where the element does not exist.**
>
> **Fixed in the render the same day**: it now prints, in red beside the grey omitted-solid lists — *"NOT DRAWN HERE, 1 named wall(s): M6b — placed by directive, in `wall_blocks.csv` and in the DXF, but the vector plan has no solid for it, so this picture cannot show it. **ABSENT HERE IS NOT ABSENT.**"*
>
> **This is the `Validator_Design_Discipline` family "anything a reader will trust must be derived, never hand-maintained" — one step further out. The render's own caption was honest about what it IS (a picture of the extraction); it was silent about what it OMITS. The omitted *solids* were listed; the omitted *wall* was not.**

**What is genuinely still missing for M6b is its insulation BAND**, not the wall. `place_insulation.py` puts M6b in `unresolved` because neither of its two evidence tests fires — the drawing contains no composite solid for it and nothing abuts it — and the tool refuses to guess a side. ⚠️ **The owner's answer settles that it HAS insulation and that the insulated face is the one away from the loggia. It does not by itself settle which coordinate that is, and it should not be inferred from a centroid — the module docstring records that a centroid rule gets M6b wrong precisely because the лоджия is an appendix.**

### 5e. The classification cannot carry the insulation rule

`wall_blocks.csv` `class` has four values: `concrete` (10), `aerated_block` (10), `external` (3), `loggia_enclosure` (2).

⚠️ **`loggia_enclosure` has exactly two members and they now need opposite treatment** — `M2` at **0 mm** and `M6b` **insulated**. And `external` (MA/MB/MC) is *also* aerated block, so the class mixes **material** with **exposure**.

**→ An insulation rule keyed on `class` will get one of M2/M6b wrong whichever way it is written.** What the rule actually needs is **exposure — does this face the outside?** That is a missing attribute, not a missing value.

**With exposure separated out, the whole set becomes thermally coherent rather than a list of arbitrary numbers:**

| wall | material & thickness | insulation | why it makes sense |
| :--- | :--- | :--- | :--- |
| MA, MB, MC | aerated block **300** | **70** | thick, and aerated block insulates itself |
| **M6b** | aerated block **200** | **150** | **thinner, so it needs more to reach the same performance** |
| R8, R9 long face | concrete **250** | **150** | concrete is a thermal bridge |
| R9 end face | concrete **250** | **120** | a return face, less exposed |
| M2 | **200**, not exposed | **0** | not a thermal boundary at all |

**That pattern is checkable, which a list of numbers is not.** It also predicts the 120 mm case the record did not have.

### 5c. ⭐ A THIRD correction, which he raised unprompted — and it is verified

> *"The window opening should be clear from any external insulation… they have gaps in the window openings, which is logical because insulation is for the walls only."*

**Checked against the data. He is right, and it is measurable:**

| wall | insulation band | window opening | overlap |
| :--- | :--- | :--- | :--- |
| `MA` | 2830.9 – 5881.0 | `O4` 4351.0 – 5731.0 | **1380 mm** |
| `MB` | 6131.0 – 9131.0 | `O2` 6731.0 – 8531.0 | **1800 mm** |
| `MC` | 9380.9 – 12946.0 | `O3` 10235.9 – 12035.9 | **1800 mm** |

> **⚠️⚠️ ALL THREE BANDS RUN STRAIGHT THROUGH THEIR WINDOWS. 4,980 mm of insulation is drawn where there is no wall to insulate** — and every placed opening in the model (`O2`, `O3`, `O4`) is affected, because all three sit on the three insulated external walls.
>
> **The fix is a rule, not three edits: an insulation band is interrupted by every opening in its host wall.** And per the owner, the source drawing already shows those gaps — so this is the extraction failing to reproduce evidence that exists, not a missing decision.

## 6. What the gates say right now, for contrast

Run 2026-09-11, before any of this is acted on:

- `check_wall_junctions.py` → **PASS**, 25 wall runs, no overlap, no gap, every L-corner owned.
- `check_dxf_closure.py` → **PASS**, no unsanctioned overlap, no unexplained near-miss, no cavity.

> **⚠️ So a human found ~15 real defects in a model that two adversarial gates call clean.** That is not a failure of the gates — they check wall-to-wall closure, and **most of these are a different class**: element *identity* (is this a wall at all?), element *completeness* (a missing wall, a missing opening), and wall-versus-insulation overlap, which nothing tests. **The lesson for `Validator_Design_Discipline.md` is that the gates' scope was never the same as "the model is right", and the DRAFT flag on `v0_named_walls_placed.json` was carrying that weight alone.**

## Suggested order — §5 is answered, so this is the live worklist

1. **Remove the three false positives** (1–3). Cheapest, and two of them shrink a category that is currently 50 % wrong.
2. **Place the two missing door openings** (4–5) — the bridge/place split.
3. **Add `M6b`** (item 6) — it is the only unmatched wall, 1170 clear. ⚠️ **Settle the 200 mm / `loggia_enclosure` versus 150 mm tension in §5b first.**
4. ⭐ **The insulation rules, both of them, since they are now settled and they change how bands are derived**: **(a)** walls touch walls and insulation fills what is left, never a layer between them (§4); **(b)** a band is interrupted by every opening in its host wall (§5c, 4980 mm wrong today). **Do these before re-deriving, or the bands get built twice.** Add the column END-face case at 120 mm (§5a) while the derivation is open.
5. **Then re-run both gates**, and expect the corner ledger to move.

---

# SECOND REVIEW ROUND — `v0_vector_extraction_with_comments.png`, 2026-09-11

The owner annotated the **corrected** render. Most marks repeat round one and stay open; **two are new.**

## ✅ NEW — two of the red boxes are VENTING SHAFTS, and they were filed as slivers

He drew red boxes round two areas and labelled both *"venting shaft"*. Located against the solids:

| his mark | solid | size | where |
| :--- | :--- | :--- | :--- |
| top-middle, beside the printed `400` | **`S11`** | 400.0 × 400.1 mm | x 8980.8–9380.9, y 15090.3–15490.3 |
| top-left | **`S19`** + **`S20`** | 397.2 × 400.0 and 147.1 × 400.0 | x 2980.8–3378.0 and 4370.9–4518.0, y 15590.3–15990.3 |

> [!WARNING]
> **⚠️ All three were being OMITTED as "sliver under 500 mm" — a SIZE rule standing in for a semantic one.** The code's own docstring says *"a bucket that holds both is not a classification"*, and this was that failure one level down: a **structural venting shaft** sharing a bucket with extraction noise, purely because it measures under 500 mm.
>
> **It matters beyond tidiness. A вентблок is IMMOVABLE**, and `Layout_Option_Review.md` §5 turns on exactly where the second one sits, because it is what the corridor-to-kids trade has to avoid.
>
> ⚠️ **And the owner had already said it once**: an earlier round is quoted in a code comment as *"S11 is noise, it's a venting shaft"*. **It reached a comment and stopped there** — unqueryable, and free to drift.

**Fixed by moving the identifications out of comments and into data.** New `data/canonical/v0_solid_roles.csv` records `S11`, `S19`, `S20` as `venting_shaft`, plus `S35` as `drawn_stove` and `S12`/`S13` as `window_element`, each with `identified_by: owner` and a date — because **a role is a claim and needs someone to have looked.** The render reads it, an identified role now beats the size bucket, and the legend names them: *"3 venting shaft (owner-identified): S11, S19, S20"*. The generic buckets shrank from 9 and 8 to **6 and 5**.

## ✅ NEW — *"you marked external insulation as a wall"*

Pointing at the orange band running south from `MB_R8` — **the band placed earlier the same day for `M6b`.**

**Diagnosis: the band was right, the picture was still missing its wall.** `M6b` is in the DXF at x 5931.0–6131.0; its band sits at x 6131.0–6281.0. But the render could not draw a wall with no vector solid, so **the only thing visible at that spot was the orange strip — which reads as the wall.** He had marked the same location in round one as *"missing wall"*, so this is the same gap reported a second time, in a new form.

**Fixed**: a named wall with no solid is now **drawn dashed in red and labelled — `M6b by directive`** — so wall and insulation read as a pair. ⚠️ **Three round-trips have now been caused by this one render showing less than the model holds**; the dashed outline is the structural fix rather than another caption.

## Still open from round one, unchanged

- The three wall-on-wall **overlaps** (S07/S18, S10/S18, S32/S33) — **resolved in the model, shown unresolved in the picture.** §3b.
- **Two bridged doorways that never became openings** (4 bridged, 3 placed).
- **`S34 R5`'s red box** — dimension linework, still counted as a doorway.
- **The `M2` red box** — *"not a wall segment. Part of the M2"*, still counted as a doorway.
- The **120 mm return face** on R9.

⚠️ **So the "4 doorway(s) bridged" category is now known to be wrong in at least two of four**, and the owner has flagged both twice.

## ✅ ROUND 2 RESOLVED — the render now explains every mark, 2026-09-11

**The structural fix, rather than a fourth caption.** Every item the owner flagged twice was already correct in the model and unexplained in the picture. The render now states what the model did:

| what he marked | what the picture now says |
| :--- | :--- |
| *"wall overlap"* ×3 | **`RESOLVED: R1b kept, G4b trimmed`**, **`G4a kept, G4d trimmed`**, **`R9 kept, G7 trimmed`** — drawn in teal on the overlap itself |
| the fourth overlap (S14×S36) | **`RESOLVED: corner - the ledger owns it`** |
| *"not a wall, just dimentions"* at S34 | **`solid runs 279 mm past R5 - not wall`**. ⚠️ Measured: S34 runs **1328.8 mm**, R5 is recorded and drawn at **1050.0 mm** — the printed figure. **The model was right; the solid swallowed a dimension line** |
| *"missing door opening"* ×2 | Every bridge now labelled with its solid, width and fate: **`S14 1010 mm - NO OPENING PLACED`**, **`S21 710 mm`** ×2, **`S16 150 mm`** |
| *"not a wall segment. Part of the M2"* | **`S16 150 mm - NO OPENING PLACED`** — named, so it can be argued with |
| *"you marked external insulation as a wall"* | **`M6b by directive`**, dashed red, beside its band |
| *"venting shaft"* ×2 | **`3 venting shaft (owner-identified): S11, S19, S20`** in the legend |

**New legend rows: `6 place(s) a solid runs PAST its wall` and `4 solid overlap(s) ALREADY RESOLVED in the model`.**

> [!IMPORTANT]
> ⚠️ **ALL FOUR BRIDGED DOORWAYS ARE UNPLACED.** The picture now shows what the counts implied: **4 bridged, 0 of them became openings.** The three placed openings (`O2`, `O3`, `O4`) come from **reveals**, a different mechanism entirely. So "4 bridged / 3 placed" was never 3-of-4 succeeding — the two routes are unrelated, and the bridge route has placed nothing.

**✅ And it closed the 250 mm discrepancy flagged in §3b.** The resolution recorded the R9/G7 overlap as **75 × 570 mm** where the raw solids gave **75 × 820**. The render now shows **`solid runs 570 mm past G7`** — so **820 = 570 over-reach + 250 corner**, and the two figures were measuring different things. Not a defect.

⚠️ **One thing the gates structurally could not have caught**: `check_dxf_closure.py` asserts no WALL is drawn past its SOLID. Every case here is the opposite direction — a SOLID past its WALL — which no gate tests, and which only a reader looking at the picture would ever raise.

