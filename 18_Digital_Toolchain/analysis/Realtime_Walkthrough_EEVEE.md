# Real-time interior walkthrough in EEVEE — the recipe, and the limitation that matters

**Added 2026-09-18.** The owner's requirement is to *walk through the flat from inside*. `Tool_Selection_Blender_SketchUp.md` established that EEVEE Next in Blender 5 is the named tool and that **Blender 5.2 is already installed here**. This page is how, and what it will not do.

---

## ⚠️⚠️ THE LIMITATION FIRST, BECAUSE IT SHAPES THE WHOLE PLAN

**EEVEE's ray tracing is SCREEN-SPACE, not path tracing.** Only geometry currently *in frame* contributes light. VICUBE Animation (`Ufw8RQb7Pj4`) demonstrates it directly:

> *"Only the objects that are currently in the frame can reflect light… if I go to the left, this wall doesn't reflect light anymore… if the light isn't in the frame anymore, then you won't get any indirect light from it."*

And, on the case that is ours:

> *"Especially for animations this can be a huge problem."*

**A walkthrough is an animation.** So as you turn, walls that leave the frame stop bouncing light and the room gets darker — most visibly in a corridor or a small room where most surfaces are behind the camera.

> **This is not a bug to be tuned away; it is how screen-space tracing works.** It is mitigated by light probes (below), which bake indirect light and therefore do *not* depend on what is in frame.

> ⚠️⚠️ **CORRECTED 2026-09-18 — the statement above was TOO ABSOLUTE.** Codex, reviewing
> this page, supplied the re-verification this section deferred. Blender 5.2 offers
> **probe-based tracing OR screen tracing, and screen tracing FALLS BACK TO PROBES when
> rays leave the view** — it does not simply lose the light. Baked volume probes capture
> static diffuse indirect lighting. Source: Blender's own 5.2 ray-tracing and volume-probe
> documentation, not a practitioner video.
>
> **So "only geometry in frame contributes light" is wrong as a flat statement**; what is
> true is that the *screen-traced* contribution is view-dependent and the *probe* contribution
> is not. A stable, convincing static walkthrough is therefore realistic — with the real cost
> being that **every material or layout revision may require a re-bake.** The original text
> came from a 4.2 demonstration (`Ufw8RQb7Pj4`) and was carried forward on the assumption
> that silence in the 5.2 changelog meant no change. **That assumption was the defect.**

## The recipe, from `V0Q3E_63TP4` (Blender 5, 2026-01)

**Setup**
1. **Preferences → System → Vulkan.** *"EEVEE is much more optimised for it."* Restart Blender.
2. **Light the interior with AREA LIGHTS ON THE WINDOWS** — one per window opening, simulating sky. Then add a **Sun** for direct light; raise its **angle** to soften.

**EEVEE settings**
3. Raise viewport samples. **Enable Ray Tracing.** Set resolution **1:1** (one ray per pixel).
4. Under **Fast GI**, also set resolution 1:1 and raise the steps.
5. ⚠️ **Do not raise shadow steps** — *"it doesn't enhance the image that much and it's quite expensive."*

**Light probes — the step that makes the difference**
6. Add a **light-probe volume** covering the interior. Each probe point captures indirect light and acts as a small emissive HDR. **~8 resolution was enough for one interior.**
7. ⚠️ **Every probe point must be INSIDE the interior.** Scale the volume to achieve it. A black gap in a corner traced to probes sitting *behind a curtain*.
8. **Bake.** Dark areas afterwards are tuned with the **distance** value, which controls how bounces affect surfaces.

**⚠️⚠️ The trap that would bite this project**
9. > *"You might experience light leaks. I'm not, because my walls have two faces… if I turn off solidify, you can see how the light leaks when you only have one surface. So always keep your interior inside another box."*

   **Single-surface walls leak light.** Our IFC walls are extruded solids with real thickness, so they have two faces by construction — **we are fine by accident of the architecture**, and it is worth knowing why.

**Finishing**
10. Compositor: glare, depth of field, exposure. Result reported: **a 2K render in 6 seconds**, visually close to Cycles apart from window frames.

## Material caveats from `Ufw8RQb7Pj4`

- **Glass is not transparent by default in EEVEE Next.** Per material: *Settings → Render Method → **Dithered***, and enable **Raytraced Transmission**. ⚠️ Doing so makes the object **disappear from reflections**.
- Glass also needs a value node into the **Thickness** input of Material Output. Blender normally adds it; if glass renders black, check this.
- ⚠️ **Memory**: cranking screen-trace resolution can use **up to twice the RAM Cycles would need for the same scene.**
- Slow shader compilation on opening a scene is improved by **Preferences → System → Max Shader Compilation Subprocesses**, set to the CPU thread count.
- **Volumetrics are cheap in EEVEE and expensive in Cycles** — the one place EEVEE is clearly ahead.

## What Blender 5.2 changed, from `6iHgqkmYXmc`

| | change | relevance here |
| :--- | :--- | :--- |
| **EEVEE** | **instanced geometry handled far more efficiently** | a flat full of repeated joinery, and later furniture, navigates more smoothly |
| **EEVEE** | **camera ray visibility for lights** — a light can illuminate without appearing in shot | *"makes lighting setups much easier"* for interiors; lets a window area-light sit outside the view |
| **Cycles** | **texture cache** — only the needed parts of textures are held in memory | matters only once real materials arrive |
| Cycles | extra denoising data exposed for reflections and depth | compositing only |
| both | professional camera colour spaces (Sony, ARRI, …) | **not relevant to this project** |

## ⚠️ What this means for the plan

- ⚠️⚠️ **"The walkthrough is achievable today" WAS WRONG AND IS WITHDRAWN (2026-09-18).**
  Codex reproduced why, and the error was a conflation: **the browser viewer and the EEVEE
  recipe are two different things, and this page treated them as one.**
  `tools/blender/walk_viewer.html` is a **Three.js GLB viewer — EEVEE is not involved in it
  at all.** What it shows today has flat colours, **zero textures**, no collision, vertical
  free flight on Q/E, and it loads a **stale GLB** (18 walls painted against the current
  IFC's 24, exported a day and a half before it). What is achievable today is a **shell
  viewer**. The EEVEE walkthrough described above is a real recipe that **nobody has yet
  run on this model.**
- **The path is still short**, and that is the honest version of the original claim: the
  geometry exists and is gated, so what remains is window area-lights, a sun, a probe
  volume and a bake — plus, before any of it, a **freshness check** so a derived view can
  never again depict a model that no longer exists.
- **It is a lighting exercise, not a modelling one.** The geometry already exists and is gated; what is missing is window area-lights, a sun, a probe volume and a bake.
- **Expect the walkthrough to look worse than a still.** Screen-space GI means turning changes the light. Probes reduce it; they do not remove it.
- ⚠️ **Do not promise photoreal.** `V0Q3E_63TP4` is explicit that the remaining visible difference from Cycles is *"a trade-off of EEVEE. We are working in real time."* For choosing between layouts, that is more than enough — which is what the лоджия-to-kitchen walk is actually for.

## Source Notes

- `V0Q3E_63TP4` — coral lab, 2026-01-07, Blender 5. The recipe.
- `Ufw8RQb7Pj4` — VICUBE Animation, 2024-07-15, Blender 4.2. The limitations. ⚠️ Not re-verified on 5.2.
- `6iHgqkmYXmc` — blendereverything, 2026-07-15. The 5.2 changes.
- ⚠️ Triaged out as superseded: `wGS0xp-XBqw` (2024-09, same "EEVEE like Cycles" technique on 4.x) and `Enggo_nqDHs` (2024-03, before EEVEE Next shipped in 4.2). `uDvzYI5jpDk` (2023-12) predates EEVEE Next entirely.
- No prices. Not region-specific.
