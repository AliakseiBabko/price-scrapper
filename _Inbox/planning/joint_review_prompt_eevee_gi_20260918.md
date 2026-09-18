# Joint review prompt — EEVEE loses indirect light, and the probe bake produces nothing

**2026-09-18.** Identical text for Codex and Antigravity. Recorded so the two answers
can be compared against the same question. Follows
`joint_review_prompt_toolset_20260918.md`, whose answers led directly to this test.

---

You both told me to settle the visual questions by measurement rather than by feature
lists. I did. One question came back answered, one came back with a hard negative I did
not expect, and I want your judgement on the negative.

**Be blunt, and reproduce rather than assert.** If you think I have made an error, name
the file, the setting or the number. Assume I have — I found seven defects in my own
experiment while running it, and the last one inverted the conclusion.

## What is set up

- **Blender 5.2.0 LTS + Bonsai**, Windows 11, headless CPU unless stated.
- Geometry compiled from `data/canonical/` → IFC → loaded via Bonsai. **57 meshes, and
  0 of them carry a UV map.**
- Test room: **2.825 × 3.4 × 2.5 m**, the flat's 9.36 m² bedroom, bounds taken from the
  compiler.
- Tools: `tools/blender/proof_room.py` builds and renders, `tools/blender/measure_proof_room.py`
  measures, `tools/blender/bake_probes_gui.py` bakes with a GPU context.
- Findings written up in `18_Digital_Toolchain/analysis/Proof_Room_Experiment_Results.md`.

## ✅ What worked — textures at true physical scale, with no UV maps

`Texture Coordinate → Object` → `Mapping` (scale = 1 / tile size in metres) →
`Image Texture`, `projection = BOX`. Measured against an orthographic camera at a known
**2.5 mm/px**: calibration marker period **400.0 px expected, 400.0 px observed →
applied tile 1000.0 mm, error 0.0**.

**I am not asking about this.** It is recorded so you know the rig measures correctly
when the thing under test works.

## ❌ The problem — EEVEE returns black where the truth is bright

**The scene.** A baffle spans the full room width, floor to **1.8 m**, leaving a
**0.7 m gap at the ceiling**. World strength **0** (black). One **28 W** area light at
the window plane facing into the room. The camera sits behind the baffle, aimed
**downward**, so the ceiling that does the bouncing is **out of frame**. Direct light
cannot reach the camera's subject; only light that passed over the baffle and bounced.

**The numbers.** Same file, same lights, same cameras, only the engine changed:

| render | whole frame mean luma | darkest 20% |
| :--- | ---: | ---: |
| EEVEE, no probe bake | 4.570 | 0.000 |
| EEVEE, probe bake scripted headless | 4.570 | 0.000 |
| EEVEE, probe bake scripted **with a GPU context** | 4.570 | 0.000 |
| EEVEE, probe bake **clicked by hand in the UI** | 4.570 | 0.000 |
| **Cycles, 96 samples** | **134.820** | **119.453** |

**Cycles resolves the space cleanly and evenly lit. EEVEE renders it black.**

## The probe bake appears to write nothing

`bpy.ops.object.lightprobe_cache_bake` returns `FINISHED` and spends **~14 s**, but what
it adds to the `.blend` does not depend on how much there is to store:

| probe resolution | probes | world | bytes added to the `.blend` |
| ---: | ---: | :--- | ---: |
| 4×4×4 | 64 | black | 5,664 |
| 20×20×15 | 6,000 | black | 5,764 |
| 4×4×4 | 64 | **bright** | 5,627 |
| 20×20×15 | 6,000 | **bright** | 5,734 |

**125× more probes adds about 100 bytes.** The bright-world rows exist because a
near-black scene would compress to nothing at any resolution, so the dark rows alone
prove nothing.

**Everything tried, all with the same result:**

- `subset` = `ALL`, `SELECTED`, `ACTIVE`
- volume explicitly selected and set active
- headless `blender -b`; windowed with a real GPU context; **a human clicking
  "Bake All Light Probe Volumes" in the UI** — both UI buttons call this same operator
  (`properties_scene.py:448`, `properties_data_lightprobe.py:206`)
- bake deferred behind a timer so the draw context exists first
- probe volume inset 0.25 m from the walls so every probe point is inside the room
- engine is `BLENDER_EEVEE` — 5.2 has **no** `BLENDER_EEVEE_NEXT` enum
- `use_raytracing = True`, ray-tracing `resolution_scale = "1"`

**Ray tracing itself does work**, where the bouncing surfaces are on screen: turning it
off drops a partly shadowed measurement from **47.882 to 42.572**, about 11%.

## What I want judged

1. **Is the probe bake genuinely broken here, or am I missing a required step?** A
   setting, a precondition on the volume, something about overlapping geometry, a known
   5.2 issue, a driver requirement. **This is the main question.**

2. **Is my test scene valid?** Is a 0.7 m gap over a 1.8 m baffle a fair test? Is a
   single 28 W area light with a black world a reasonable way to force all light to be
   indirect, or have I built something pathological that no renderer should be expected
   to handle well?

3. **Is "put a light in every room" the right response, or is it papering over a broken
   pipeline?** A real flat has lamps, and lighting is three sheets of the target album,
   so specifying it is work I must do anyway. But I do not want to adopt a workaround
   that hides a defect I will meet again.

4. **Does this change your runtime recommendation?** Codex proposed deciding
   Three.js/Blender vs Unreal on a measured proof room rather than a feature list. This
   is that proof room. Antigravity said not to use EEVEE for finished aesthetic
   judgement and to use Cycles stills. **Does this result settle that between you?**

5. **What have I still not thought of?** The last control I added — rendering the same
   scene in Cycles — is the one that inverted the conclusion, and I only added it after
   six revisions of comparing EEVEE against EEVEE. **A measurement with no ground truth
   measures agreement, not correctness.** Assume there is another missing control of
   that kind.

## What I am not asking

Do not design the apartment. Do not re-litigate the canonical-data-first architecture —
you both endorsed it and it is working. The question is the render layer only.
