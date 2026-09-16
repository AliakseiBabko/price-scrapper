# Triage — Blender rendering: 7 standalone videos + a 51-part archviz playlist

**Date:** 2026-09-16 · **Owner-supplied** · **58 videos** · **Status: triaged; 18 processed, 40 declined with reasons**

**Why it was sent:** the owner had just chosen **Blender + Cycles** over Twinmotion for renders that must stay tied to the model, and asked me to check this material. **So the triage question is not "is this good content" but "does it support that decision, and what does it cost to execute".**

---

## ⚠️⚠️ 1. The filter that did most of the work

**The playlist is a 50-part course and it splits cleanly at part 20.**

| Parts | Subject | Verdict |
| :--- | :--- | :--- |
| **1–20** | CAD import, DWG TrueView, floor plan and walls, stairs, camera matching, kitchen island, windows, drawers, cabinets, appliances, booleans, outside view | **⚠️⚠️ DECLINE, the whole block.** This is **hand-modelling from drawings**. This project generates geometry from `model.ifc` — taking this half would be learning to do by hand what the pipeline already does deterministically, and would invite exactly the second-source-of-truth drift `Model_and_Views.md` exists to prevent |
| **21–28** | Illumination, HDRI setup + hacks, sun lamp, sky texture, area lights + hacks, multiple importance sampling | **TAKE selectively** — this is the real gap |
| **29–36** | Materials: intro, concrete, wood, plaster, glass, glossy, metal, shadow terminator | **TAKE selectively** — the finishes this flat actually has |
| **37–41** | Scene adjustments, Cycles rendering hacks, quick Cycles setup, bit depth, tone mapping | **TAKE selectively** |
| **42–50** | Colour correction, colour balance, vignetting, cryptomatte, transparent background, **Photoshop** post-production, render passes, **Photoshop** compositing | **DEFER.** Post-production, and two of them are Photoshop-specific. Revisit only if renders are being published rather than used to decide |
| **51** | Light Groups | **⚠️⚠️ TAKE — the highest-value single part** |

**⚠️ Also weighed: the course is 2021–2022, i.e. Blender 3.x.** A 2025 source in the same batch documents the EEVEE rewrite and Cycles improvements since. **The method holds; the numbers should be re-derived.**

---

## ⚠️ 2. Processed — 18 videos, two grouped notes

**[[_Sources/YT_BifyAj9KpaI_blender_render_engine_choice|The engine decision]]** — all 7 standalone: Cycles vs Octane, two on V-Ray, EEVEE vs Cycles, "how good is Blender for rendering", interior optimisation, photoreal interior lighting.

**[[_Sources/YT_1IdW1-Gtoao_blender_archviz_course_method|The course method]]** — 11 parts: Units and Scale (05), Illumination (21), HDRI Setup (22), HDRI Hacks (23), Area Lights (26), Area Light Hacks (27), Materials Intro (29), Plaster (32), Glass (33), Cycles Rendering Hacks (38), Light Groups (51).

### What they settled

1. **⚠️⚠️ Cycles is right, and not as a compromise.** Every advantage V-Ray and Octane are credited with — frame buffer, image history, ready-made artist nodes — is an **interactive-GUI** advantage, worth nothing when renders are launched headless from a script. **Octane's free tier requires an active internet connection and a separate licence server, and ships as a Blender fork** — actively hostile to a pinned, reproducible pipeline.
2. **⚠️⚠️ A paying V-Ray user argues against buying it for Blender**, on ecosystem grounds: ~99% of the community is on Cycles/EEVEE so the learning material does not exist, Maxon dropped Redshift for Blender, and *"Cycles is getting better and better — why do I bother at this point?"*
3. **EEVEE is the preview, not the alternative** — same node graph as Cycles, so it previews the exact materials you will render.
4. **The interior recipe exists and is specific**: light portals, the **glass-shadow trick** (Mix Shader between Glass and Transparent driven by `Light Path → Is Shadow Ray`), Cryptomatte-masked selective denoising, and named parameter changes. **Interiors in under five minutes on a single GPU.**
5. **A four-step lighting formula** — AgX + medium-high contrast, sun as key softened to ~30°, sky texture as fill, artificial light as accent with **blackbody colour temperature** — **corroborated independently by the course's own lighting order.**
6. **⚠️⚠️ Light Groups relight a finished render without re-rendering.** Directly answers "see how it may look" without a render per option.
7. **Third confirmation of the UV cost** — textured surfaces need UV maps and an IFC model has none — **plus a licence that matters: flat white plaster "could actually do the trick"**, with bump and micro-reflection as refinement rather than requirement.

---

## ⚠️ 3. Declined, with reasons

| Bucket | Count | Why |
| :--- | ---: | :--- |
| Course parts 1–20, hand-modelling from CAD | 20 | §1 — the pipeline generates geometry; this is the half that would compete with it |
| Course parts 42–50, post-production and Photoshop | 9 | Deferred, not rejected. Relevant only once renders are published rather than used to decide |
| Materials not present in this flat (concrete 30, wood 31, glossy 34, metal 35) | 4 | **Reserve.** Take the one that matches a finish when that finish is actually chosen — wood is the likeliest |
| Sun lamp (24), sky texture hacks (25), MIS (28), shadow terminator (36), scene adjustments (37), quick Cycles setup (39), bit depth (40), tone mapping (41), intro (00), part 01–04 overlap | ~11 | Covered in substance by the seven standalone, or too tool-specific to carry |

---

## ⚠️⚠️ 4. What this changes, and what it does not

**Confirms the decision**: Blender + Cycles can produce the photoreal interiors the owner wants, the method is documented, and render time is not the obstacle.

**Does not change the architecture caution.** The material half of the course is a reminder of what "realistic" costs: per-surface UV unwrapping, authored by hand in a GUI. **If those materials are dragged onto surfaces by hand, the .blend becomes a second source of truth and drifts from `finish_schedule.json` exactly as `Model_and_Views.md` warns.** **The open proposal stands: drive materials from the finish schedule in code, so a finish change is a re-run rather than a re-decoration.**

**⚠️ And one genuine limit, stated rather than glossed**: nothing in these 18 videos shows a SCRIPTED archviz pipeline. Every source authors interactively. **The scripted approach is this project's own, and the sources support its ingredients rather than its shape.**
