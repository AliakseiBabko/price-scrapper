# Joint review prompt — the toolset and the approach

**2026-09-18.** Identical text given to Codex and to Antigravity. Recorded here so their two answers can be compared against the same question.

---

I want your opinion on whether the toolset and the approach are right. Be blunt; I would rather change direction now than after another month of building.

## What I am doing, in my own words

**The model is the thing. Drawings are just a way to represent it.** The apartment exists as digital data first; 2D plans and 3D views are outputs of it, not artefacts I draw. I am trying to automate as much of that as possible.

**I do not draw.** I cannot model by hand in any 3D tool and I do not intend to learn. I communicate with the model **through an AI agent in chat** — Claude Code, Codex or Antigravity — and give it instructions; the agent changes the data and the model rebuilds. **Chat is the main interface, permanently, not a phase.** I need the 3D tool to *see the result*, not to produce it.

## Where I am going, in order

1. ✅ a basic layout — `v0`, the existing state
2. ✅ a basic 3D model from it
3. **check the functional zoning and the general layout**
4. **generate layout options** from sizing, volumes and everyday scenarios — this is what fixes functional zoning **and the engineering systems**
5. **then real 3D**: actual furniture, actual appliances, actual materials — I want to **upload a photo of a tile or a wallpaper and see it applied** to my model
6. **then design**: colour, lighting, placement variants, textures
7. **finally — not renderings — a WALKTHROUGH.** I want to be inside the finished apartment, as close to the final variant as possible, with real textures and real 3D models of furniture and appliances.

## Where to look

Read `AGENTS.md` first; it is the router. Then:

| | |
| :--- | :--- |
| `00_Master/Spatial_Structure_Analysis.md` | what the flat permits, in four layers |
| `00_Master/Planning_Project_Deliverable_Set.md` | the target drawing set — a real 37-sheet album the owner chose |
| `18_Digital_Toolchain/analysis/Tool_Selection_Blender_SketchUp.md` | why Blender, and what the evidence does and does not support |
| `18_Digital_Toolchain/analysis/Realtime_Walkthrough_EEVEE.md` | the walkthrough recipe and its hard limit |
| `18_Digital_Toolchain/analysis/Agent_Connected_CAD.md` | generated script vs live connection |
| `data/canonical/` | the authored data everything compiles from |
| `tools/layout/`, `tools/ifc/` | the compiler and its gates |

⚠️ Antigravity auto-discovers `.agents/skills/`; **Codex does not** — read `.agents/skills/apartment-layout-modelling/SKILL.md` explicitly if you are Codex.

## The toolset as it stands

- **Authored data** in `data/canonical/` (CSV + JSON) → a **deterministic compiler** → **IFC** and **DXF**
- **Blender 5.2 LTS + Bonsai** for viewing and, eventually, the walkthrough via EEVEE
- **Gates**: `check_dxf_closure.py`, `raster_fidelity.py`, IFC identity/type/connection checks, an IDS exchange contract, and self-tests that seed real defects and watch each one fail
- **No live MCP connection to the modeller.** Artefacts are generated files, so they can be diffed and gated

## What I actually want judged

1. **Is the architecture right for the goal?** Canonical-data-first works well for walls, openings and services — things with identity and provenance. **Steps 5–7 are different**: furniture, appliances and textures are bought assets and appearances, not authored facts. **Where do they live?** A manufacturer's sofa arrives as `.fbx` or `.skp`, not as rows I can gate. Does the architecture bend to accommodate that, or does it need a second, explicitly ungated layer — and if so, what is the boundary rule?

2. **Is Blender the right tool for steps 5–7 specifically?** Not for the compiled model — that decision is made and IFC is the hand-off. For **real furniture libraries, uploaded textures and a walkable interior**, is Blender + Bonsai the right place, or is something else better at it? Say so if it is.

3. **Is chat-as-the-only-interface sustainable?** Placing three walls by instruction is fine. **Placing fifty pieces of furniture, each with a texture, may not be.** If it breaks down, where, and what should replace it — noting that "learn to model" is not available.

4. **Does the walkthrough goal survive contact with the tooling?** EEVEE's ray tracing is screen-space: only geometry in frame contributes light, which the source calls a serious problem for animation. Baked light probes mitigate it. **Is a convincing interior walk realistic on this stack, or is the honest answer that it needs a game engine, or photoreal stills instead?**

5. **What is the biggest risk you see that nobody here has named?** The last six review rounds each found real defects, including four dimensional errors of one family. Assume there is something similar in the approach itself.

## What I am not asking

Do not design the apartment or choose a layout. Do not re-litigate decisions already recorded with reasons unless you think the reason is wrong — in which case say which record and why.

**Reproduce rather than assert.** If you think something will not work, show the file, the command or the number that demonstrates it.
