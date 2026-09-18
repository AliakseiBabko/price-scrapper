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

## ⚠️ PARTLY ANSWERED — EEVEE's GI works; the probe volume adds nothing here

**Corrected 2026-09-18, and the correction includes withdrawing a claim made on this
page hours earlier: that a HUMAN had to bake in the GUI. That was wrong.**

### The bake needs a GPU context, not a person

`blender -b` creates no OpenGL context, and a light cache needs one. But Blender
launched **without** `-b` opens a window *and* still runs a `-P` script that drives
everything and quits. **No clicking by anyone.** `tools/blender/bake_probes_gui.py`
does it: `background_mode: false`, bake **13.7 s**, `FINISHED`, file saved and grown
from **172,535 → 178,414 bytes**. The cache is demonstrably in the file.

⚠️ The bake is deferred through a **timer**, because at the moment a startup script
runs the window exists but the draw context may not — baking too early fails exactly
like baking headless, returning `FINISHED` and producing nothing.

### And the probes still change nothing

| away-facing frame | shadow luma | whole frame |
| :--- | ---: | ---: |
| no probe bake | **47.882** | 79.34 |
| GPU-baked, rendered headless | **47.882** | 79.34 |
| GPU-baked, rendered **windowed** | **47.882** | 79.34 |
| baked, **ray tracing OFF** | **42.572** | 78.02 |

**Identical to three decimals** across all three probe conditions — so this is not a
headless artefact and not a bake failure.

> ⚠️⚠️ **But the last row is the finding.** Turning ray tracing **off** drops the
> shadowed region by **11%**. So **EEVEE's screen-space tracing IS supplying indirect
> light, and the baked probe volume adds nothing on top of it in this geometry.**
> That is the opposite of the failure the source warned about — and it is consistent
> with Blender's 5.2 documentation.

### ⚠️⚠️ THE CAUSE, FOUND: the bake writes no cache at all

Every 1.00× has one explanation, and it is not EEVEE. **`bpy.ops.object.lightprobe_cache_bake`
is not producing an irradiance cache in this setup.** It returns `FINISHED` and spends
~14 s, but what it writes does not depend on how much there is to write:

| probe resolution | probes | scene | bytes added to the `.blend` |
| ---: | ---: | :--- | ---: |
| 4×4×4 | 64 | black world | **5,664** |
| 20×20×15 | 6,000 | black world | **5,764** |
| 4×4×4 | 64 | **bright** world | **5,627** |
| 20×20×15 | 6,000 | **bright** world | **5,734** |

**A real cache must scale with probe count.** 125× more probes adds ~100 bytes. Tested
with `subset` = `ALL`, `SELECTED` and `ACTIVE`, with the volume selected and active,
headless and windowed. ⚠️ The dark-scene rows alone would not have proved it — a
near-black scene has near-zero irradiance everywhere and compresses to nothing either
way, which is why the bright-world control exists.

**So the probes have contributed nothing to any render in this experiment, and the
question "do baked probes rescue out-of-frame indirect light" is STILL UNTESTED.**

### ⚠️ But one result IS established, and it matters for the walkthrough

With the baffle blocking all direct light, the far half of the room renders at a mean
luma of **4.570** — essentially black — and **identically with and without the bake**.

> **As the pipeline stands today, a space with no line of sight to a light source goes
> dark.** Screen-space tracing supplies indirect light only where the bouncing surfaces
> are on screen: it is worth **11%** in a partly shadowed view (47.882 → 42.572 with ray
> tracing off) and **nothing** behind a full occluder.
>
> ⚠️ This is a real constraint on a walkthrough — a room around a corner, or one with
> its door shut, will not light itself. **It is NOT yet known whether a working probe
> bake would fix it**, because no working probe bake has been obtained here.

**What would settle it:** a bake driven from the Blender UI by hand rather than through
the operator API, or a different Blender build or GPU driver. That is now a narrow,
specific question rather than an open one.

## ⚠️⚠️ SIX defects in the experiment itself, all mine, all caught by measuring

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

> **Every one of the six was found by insisting on a number.** An experiment
> judged by eye would have passed #1, not noticed #2, and never reached #3 — and
> would have produced exactly the persuasive-but-wrong artefact this project is
> built to prevent.

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
| **1** | does the walkthrough survive EEVEE's screen-space GI? | ⚠️ **partly.** Ray tracing works and is worth 11% in a partly shadowed view. A FULLY occluded space renders black. Probes are untested because the bake writes no cache — a narrow, named blocker |
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
