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

## ❌ NOT ANSWERED — whether indirect light survives the window leaving frame

**Probe gain: 1.00×.** The away-facing view measured **113.6** mean luma with the
probes baked and **113.6** without. The bake contributes **nothing measurable**.

> ⚠️⚠️ **THIS IS NOT A VERDICT ON EEVEE, AND MUST NOT BE QUOTED AS ONE.** Blender's
> own 5.2 documentation says screen tracing falls back to probes. Nothing here
> contradicts that — **the experiment failed to test it.**

**Leading hypothesis: the bake does not work under `blender -b`.** A diagnostic run
confirms the probe object is created, is a `LightProbeVolume`, and that
`lightprobe_cache_bake` returns `FINISHED` — but a light cache normally needs a GPU
context headless Blender lacks, and there is **no `cache_info` attribute** to confirm
the cache holds data. The baked run *is* ~2× slower per frame, so something is being
computed; it just does not change the light.

**What would settle it:** bake once in the Blender GUI, save the `.blend` with its
cache, render headless *from that file*. That separates *"EEVEE cannot"* from
*"headless cannot bake"*, which this run cannot distinguish.

## ⚠️ Three defects in the experiment itself, all mine, all caught by measuring

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

> **Every one of the three was found by insisting on a number.** An experiment
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
| **1** | does the walkthrough survive EEVEE's screen-space GI? | ❌ **still open** — needs a GUI bake |
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
