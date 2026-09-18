# The proof room — what the experiment measured, and what it did not

**2026-09-18.** After the joint review left three questions that argument could not
settle, both engines said the same thing: **build one room and measure, do not decide
from feature lists.** This is that run. `tools/blender/proof_room.py` produces it,
`tools/blender/measure_proof_room.py` measures it, and the numbers are in
`data/outputs/proof_room/proof_room_measurements.json`.

**Blender 5.2.0 LTS + Bonsai, headless, CPU. Two runs: probe bake ON and OFF.**

---

## ✅ ANSWERED — a texture applies at its true physical size, with no UV map

**This was the step-5 blocker, and it is solved.**

| | |
| :--- | :--- |
| calibration marker period | **1000 mm** by construction |
| orthographic camera | 4.0 m across 1600 px = **2.5 mm/px** |
| expected marker spacing | **400.0 px** |
| **measured** | **400.0 px → applied tile 1000.0 mm, error 0.0** |

**How, and why it matters.** The IFC carries **no UV maps at all** — measured, not
quoted: **0 of 57 imported meshes** have one. Generating UVs per object is the work
both engines warned would drown the pipeline. It is not needed:

> **`Texture Coordinate → Object` → `Mapping` (scale = 1 / tile size in metres) →
> `Image Texture` with `projection = BOX`.**

Object coordinates are already in metres, so the scale is **one number** and is
physically correct by construction. A 600×1200 tile becomes `scale = 1/0.6, 1/1.2`.
**Your "upload a photo of a tile and see it applied" has a working mechanism.**

⚠️ **The honest limit:** object coordinates are per-object, so the pattern starts
afresh at each wall's own origin — **scale is right, alignment across two walls is
not.** For judging a room that does not matter; for a tile-setting drawing it would.

## ✅ MEASURED — what a frame actually costs

| | probe bake ON | OFF |
| :--- | ---: | ---: |
| probe bake | 104 s | — |
| ortho 1600×1200 | 112 s | 4.3 s |
| interior 1280×960 | 30 s | 16 s |

⚠️ **The recipe's "2K in 6 seconds" is a GPU VIEWPORT figure and is not comparable**
to headless CPU stills. That distinction is exactly the difference between a
walkthrough being interactive and not, and this page will not blur it.

## ✅ ANSWERED — EEVEE's probes DO carry out-of-frame light. My volume was wrong.

**⚠️⚠️ WITHDRAWN: everything this page previously said about the probe bake "writing no
cache" was wrong.** Codex found the defect on 2026-09-18 and it reproduces exactly. The
bake was working the whole time.

### The defect: the probe volume was SMALLER than the room

`add_probe_volume()` inset the volume by 0.25 m — **125 mm on every side** — under a
docstring reading *"every probe point must sit INSIDE the room"*. That misreads the
recipe. Its warning is about probe points landing **behind geometry**, such as behind a
curtain. It is not a reason to shrink the volume below the room.

| | room half-extent | probe half-extent | excluded |
| :--- | ---: | ---: | ---: |
| X | 1.413 | 1.288 | 125 mm/side |
| Y | 1.700 | 1.575 | 125 mm/side |
| Z | 1.250 | 1.125 | 125 mm/side |

**A probe volume's bounds are its INFLUENCE bounds.** A surface outside every volume
falls back to world diffuse lighting — and the world was at strength 0. So the floor,
the ceiling and all six enclosing faces were excluded: **precisely the surfaces whose
indirect lighting was being measured.** Nothing the bake produced could reach the thing
under test.

### Reproduced, behind the baffle

| render | whole frame | darkest 20% | fixed ROI |
| :--- | ---: | ---: | ---: |
| EEVEE, no bake | 4.570 | 0.000 | 4.130 |
| EEVEE, **inset volume — the bug** | 4.570 | 0.000 | 4.130 |
| EEVEE, **enclosing volume** | **56.400** | **34.506** | **48.800** |
| Cycles, path-traced ground truth | 134.820 | 119.453 | 133.210 |

> ✅ **EEVEE's baked probes DO deliver indirect light to a surface whose illuminating
> geometry is out of frame.** The documented behaviour holds. The walkthrough is not
> blocked by a renderer limitation.
>
> ⚠️ **But EEVEE recovers only ~42% of the path-traced whole-frame answer and ~37% on
> the fixed ROI**, in a deliberately severe case. Much better than black; **not
> trustworthy for final lighting judgement.** That supports Antigravity's "Cycles for
> finished aesthetics, EEVEE for spatial review" over a single-engine plan.

### Three inference errors of my own, beyond the volume itself

1. **`.blend` byte growth is not a functional test.** I concluded the cache was empty
   because the file grew ~5.7 KB regardless of probe count. A rendered positive control
   supersedes that entirely — and I had no positive control to supersede it with.
2. **The bright-world control was VACUOUS.** The probe had `capture_world = False`, so
   changing world brightness could never test whether world radiance was stored. I built
   that control specifically to be rigorous and it tested nothing. Now set to `True`.
3. **"Darkest 20%" moves its own support.** It selects the darkest pixels of *each image
   independently*, so it compares different pixels in the two frames it is meant to
   control. Replaced by a fixed geometric ROI; the old figure is kept only for continuity.

### ⚠️ The gate that would have prevented all of it

`proof_room.py` now **refuses to build** when the probe volume does not enclose the room
surfaces, and the refusal has been watched to fire on the original numbers:

```
probe volume does not enclose the room surfaces: half-extent (1.288, 1.575, 1.125)
against a room half-extent of (1.413, 1.7, 1.25). Every surface outside the volume
falls back to world lighting, so nothing measured here would be indirect light.
```

Reproduce the original defect with `PROOF_PROBE_MARGIN=-0.25`.

### ⚠️⚠️ Fixing Blender's probes does NOT fix the browser walkthrough

Codex's point, verified here: `tools/blender/export_glb.py` contains **no light, probe or
irradiance export at all**. The probe cache belongs to the `.blend`. The Three.js viewer
still needs a proven lightmap pipeline (with non-overlapping lightmap UVs — which the
box-projection texture route deliberately does **not** provide), a runtime GI solution,
or lighting simple enough to be honest only for spatial review.

## ⚠️⚠️ TEN defects in the experiment itself, all mine

**This is the part worth keeping.** Each would have produced a confident wrong answer.

1. **The first GI test compared two different views** — toward-window against
   away-from-window — got a ratio of **1.756** (the away frame *brighter*) and
   reported **PASS**. Two views differ in what they contain, not only in how they are
   lit. **It measured framing, not light.** The fix is a control: same camera, bake
   on and off.
2. **Both frames were blown to white** at 260 W — mean luma **205 of 255**. Clipped
   frames cannot differ, so the comparison was dead before it ran. **A saturated
   measurement is no measurement.**
3. **The scale detector reported a 58% error that was entirely its own.** The marker
   is a triangle, so a column scan found its two edges separately, giving alternating
   gaps of 38 and 362 px and a "mean" of 167.6. The true period is their **sum,
   400.0 px exactly.** Merging the parts of one marker turned a FAIL into an exact
   PASS.

4. **The world background was a uniform fill light** at strength 0.6 — lighting every
   surface from every direction whether or not a probe existed, and swamping the
   quantity under test. Black world now.
5. **The test surface was DIRECTLY LIT.** An empty rectangular room with a light at
   one end has no shadow anywhere, so there was no indirect component in the frame at
   all. Probes could not have changed it. An occluder now creates a region direct
   light cannot reach.
6. **The whole-frame mean was the wrong statistic** — dominated by directly lit
   surfaces that no probe can move. The measurement is now the darkest 20% of the
   frame, where indirect light is the only light.

7. **The probe volume did not enclose the room** — the one that invalidated every EEVEE
   number for four days. Found by Codex, not by me.
8. **`.blend` byte growth was used as a functional oracle** in place of a positive control.
9. **The bright-world control was vacuous** (`capture_world = False`) and the
   darkest-20% statistic moved its own support.

10. **A partition asserted to be "sealed" that was not** — twice. Cycles certified a
    light path both times. The leak test therefore produced a suggestive number and no
    verdict.

> **Six of the ten were found by insisting on a number. The last three were not found
> by me at all** — and 7 is the one that mattered most. ⚠️ **Measurement discipline is
> not the same as measuring the right thing:** four EEVEE runs agreed with each other
> perfectly while none of them touched a surface inside a valid influence volume. An experiment
> judged by eye would have passed #1, not noticed #2, and never reached #3 — and
> would have produced exactly the persuasive-but-wrong artefact this project is
> built to prevent.

## Antigravity's three added risks — one measured down, one unresolved, one adopted

Antigravity independently confirmed the probe-volume diagnosis and added three risks.
**Reproduced rather than accepted:**

### ⚠️ B — box projection on the mitred walls: REAL IN KIND, OVERSTATED ~10x

Antigravity: `M2`/`M6b` are *"mitred quadrilaterals angled at roughly 45°"*, giving a
**√2 ≈ 1.414 stretch — 41% distortion on loggia finishes.** Measured from the compiler:

| | claimed | **measured** |
| :--- | :--- | ---: |
| angle off-axis | "roughly 45°" | **15.93°** |
| stretch | 1.414 | **1.040** |
| distortion | 41% | **4.0%** |
| extent | "loggia finishes" | a **208 mm** chamfer on a ~2073 mm wall |

**The mechanism is real and the magnitude is not.** A dimension was asserted rather than
read — the same shape as the four rule-9 errors already recorded here. 4% on a 208 mm
chamfer does not affect judging a room; it would matter only for a tile-setting drawing
on that one chamfer. **The ✅ texture result above stands**, with this qualification.

### ⚠️ A — probe leak through a 75 mm partition: UNRESOLVED, with a signature

Antigravity: a probe grid spaced 0.3–0.5 m cannot resolve a 75 mm wall, so probes in a
lit bay spill irradiance into a dark one. **The arithmetic is right** — at 8×8×6 the grid
here is **685.7 mm**, over 9× the 75 mm of `G7`/`G8`.

**Two attempts to test it, both with unverified seals:**

1. A partition across the 9.36 room *inside the IFC model* — **not sealed.** Cycles
   rendered the far side at 130.9, so a light path existed: the room opens to the loggia
   through `O4` and the flat continues around it. **A test that assumes a seal it has not
   verified measures nothing.**
2. A standalone two-chamber box (`tools/blender/probe_leak_test.py`) — Cycles still reads
   119.2 where it should read black, so that seal is unverified too.

**What the numbers show anyway**, with a light-off control confirming no stray light:

| | Cycles | EEVEE unbaked | EEVEE baked |
| :--- | ---: | ---: | ---: |
| light on | 119.190 | **0.080** | **174.740** |
| light removed | 0.080 | 0.080 | 0.080 |

> ⚠️ **EEVEE-baked reads 174.7 — 47% BRIGHTER than path-traced ground truth — in a
> chamber EEVEE itself renders pitch black when unbaked.** Elsewhere in this experiment
> EEVEE *under*-reports by ~60%. An over-bright reading in exactly the configuration
> Antigravity predicted would leak is a signature, **but it is not a confirmation**, and
> it must not be quoted as one while the seal is unverified.

**Status: Antigravity's concern is plausible, unrefuted and unconfirmed.** Settling it
needs a scene whose seal the ground-truth renderer certifies first. ⚠️ It matters for the
real flat, which is three bays divided by 75 mm partitions — so a per-room
`visibility_collection` on each probe volume, as Antigravity proposes, should be treated
as **required until proven unnecessary** rather than the other way round.

### ✅ C — fixed ROI instead of adaptive statistics: ADOPTED

Already fixed. Both engines reached it independently. **A metric whose sample support
shifts with the output is not a measurement.**


## Two findings about the model, found along the way

- ⚠️⚠️ **The model has ZERO `IfcSpace`.** Eight existed on 2026-09-16; none survive.
  **`render_room.py` selects a room by its space boundaries and therefore cannot run
  on the current model at all.** The proof room takes its bounds from the compiler
  instead, which is why it works.
- ⚠️ **`model.json` claims 23 walls; the IFC beside it holds 24.** The compiler
  resolves 25, and R1a+R1b merge into one monolithic assembly `A_NW_CORNER` — which
  is correct, and 25 → 24 is the right arithmetic. **The manifest counts the walls it
  wrote individually and omits the assembly, so it under-reports by exactly one.**

## Where this leaves the three questions

| | question | state |
| :--- | :--- | :--- |
| **1** | does the walkthrough survive EEVEE's screen-space GI? | ✅ **Yes for spatial review** — baked probes deliver out-of-frame indirect light once the volume encloses the room. ⚠️ **No for final aesthetics**: EEVEE recovers ~42% of the path-traced answer. ⚠️ The BROWSER runtime is a separate, unsolved problem |
| **2** | can an uploaded texture be applied at the right scale? | ✅ **yes, exactly** |
| **3** | what does a rebuild cost? | ✅ **measured above** |

## The GUI-bake route — how question 1 gets closed

The one step that cannot run headless now has a path, and **it is the same code**, so
the comparison stays valid.

```
# 1. build the scene and stop
blender -b -P tools/blender/proof_room.py -- --save-blend data/outputs/proof_room/bake_me.blend ...
# 2. OWNER: open it in the GUI, Render Properties -> Bake Light Caches, Ctrl+S
# 3. render from the baked file
blender -b -P tools/blender/proof_room.py -- --open-blend data/outputs/proof_room/bake_me.blend --suffix _guibaked ...
```

⚠️⚠️ **The cameras are rebuilt from the compiler on BOTH routes, never taken from the
`.blend`.** A separate scene for the baked run would have made the comparison
worthless — the test and the control would differ in more than the bake. Step-by-step
instructions sit beside the file at `data/outputs/proof_room/HOW_TO_BAKE.md`
(untracked: `data/` is gitignored).

`measure_proof_room.py` then prefers `away_from_window_guibaked.png` automatically and
scores it against the unchanged `_noprobe` control. **≥1.25× means baked indirect light
reaches a view with the window behind the camera**, which is the specific failure the
source called a serious problem for animation.

⚠️ **One number will not settle "is the walkthrough good".** It settles that one
mechanism. Motion, materials and framing remain separate questions.

⚠️ **A fourth defect, caught here:** `--save-blend` first wrote
`proof_room_report.json` and **clobbered the real measurement run's report** with a
record containing no renders at all; the measurement then died on a missing key. A
build step must not overwrite a measurement step's output, and it now writes under
`_saveblend`.

## Source Notes

- No prices. Not region-specific.
- Run on Blender 5.2.0 LTS, Bonsai `bl_ext.renovation_local.bonsai`, headless CPU.
- ⚠️ In Blender 5.2 the engine identifier is **`BLENDER_EEVEE`** — "EEVEE Next"
  *replaced* the old engine in 4.2 rather than sitting beside it, so the
  `BLENDER_EEVEE_NEXT` that tutorials use is not a valid enum and raises.
- ⚠️ `Material.use_nodes` and `World.use_nodes` are deprecated and expected to be
  removed in **Blender 6.0**. Both are used here and will need replacing.
