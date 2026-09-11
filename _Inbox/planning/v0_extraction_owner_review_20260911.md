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

## 4. ⭐⭐ The rule behind most of the above

**Two arrows, to the `MA_R8` and `MB_R8` corners:**

> ### *"walls should touth other walls; insilations fill in the gaps; not a layer between walls"*

**This is a modelling rule, not a defect report, and it explains items 12–14.** The insulation is currently drawn as a **band that separates** two walls at a corner; the owner's model is that **walls meet walls, and insulation fills whatever gap is left over** — it is never the thing in between.

> [!IMPORTANT]
> **⚠️⚠️ THIS REFINES THE 2026-09-10 INSTRUCTION AND NEEDS TO BE RECORDED AS SUCH.** `project_decisions.md` quotes the owner from 2026-09-10: *"still that M2 is not touching MA. See the gap. There shouldn't be gaps. There should be an insulation layer, which is outside — 70 millimetres thick. I want you to draw this external insulation layer instead of leaving the gap."*
>
> **That was read as: draw the insulation into the gap. The correction is: the walls themselves should have been made to touch, and insulation is what fills what remains — an external skin, not a spacer.** Same complaint ("there shouldn't be gaps"), different remedy. **Whoever implements this must not read the September 10 quote alone.**

## 5. ⚠️ Two things that need the owner before any change

1. **A third insulation thickness appears.** Canonical `v0_insulation_placed.json` holds exactly two: **70 mm** on `MA`/`MB`/`MC` and **150 mm** on `R8`/`R9`, every band `status: from_drawing` with evidence. **Item 7 introduces 120 mm at `MB_R9`**, and items 6 and 8 add two more walls at 150 mm. **Where do 120 and the new 150s come from — the drawing, or the specification?** The existing five are all evidenced from the drawing, and adding unevidenced ones would break that.
2. **`M6b` is still open and may be item 8.** `v0_insulation_placed.json` records `M6b` under `unresolved` with `insulation_mm: 70.0` and **empty evidence on both sides** — deliberately not guessed. Item 8 ("a separate wall section with external insulation 150 mm", on the left wall below `S16 M2`) is in roughly that area. **If it is M6b, the answer is 150 and not 70, and the unresolved entry closes.** Worth confirming rather than assuming.

## 6. What the gates say right now, for contrast

Run 2026-09-11, before any of this is acted on:

- `check_wall_junctions.py` → **PASS**, 25 wall runs, no overlap, no gap, every L-corner owned.
- `check_dxf_closure.py` → **PASS**, no unsanctioned overlap, no unexplained near-miss, no cavity.

> **⚠️ So a human found ~15 real defects in a model that two adversarial gates call clean.** That is not a failure of the gates — they check wall-to-wall closure, and **most of these are a different class**: element *identity* (is this a wall at all?), element *completeness* (a missing wall, a missing opening), and wall-versus-insulation overlap, which nothing tests. **The lesson for `Validator_Design_Discipline.md` is that the gates' scope was never the same as "the model is right", and the DRAFT flag on `v0_named_walls_placed.json` was carrying that weight alone.**

## Suggested order, once §5 is answered

1. **Remove the three false positives** (1–3). Cheapest, and two of them shrink a category that is currently 50 % wrong.
2. **Place the two missing door openings** (4–5) — the bridge/place split.
3. **Add the missing wall** (6) and settle its insulation with item 8 / `M6b`.
4. **Decide the insulation rule** (§4) — this changes how corners are built, so it comes before re-deriving the bands.
5. **Then re-run both gates**, and expect the corner ledger to move.
