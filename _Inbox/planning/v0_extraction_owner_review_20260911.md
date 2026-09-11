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
