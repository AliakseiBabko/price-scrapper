# Agent-Connected CAD

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**What happens when a language model is wired directly to a CAD or BIM application rather than handed a file — the two architectures, the feedback trade-off, and the one thing it reliably cannot do.**

> [!IMPORTANT]
> **⚠️ Install steps and product versions from these sources are deliberately not recorded.** They date within months and none of this is this project's toolchain. **What is recorded is the architecture and the observed failure categories**, which outlive any particular connector.

## 1. Two architectures, and this vault previously held only one

**⚠️⚠️ A refinement of an existing vault finding, and the distinction is real.**

[[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7 records, from Trimble's own channel, that *"an AI CAD integration is a FILE GENERATOR, not a live modeller — there's not a direct live connection… it won't go in and edit it"*, with each change emitting a new file. **That is true of the adapter it describes, and false of an MCP-connected application.**

| | **Open loop** (file generator) | **Closed loop** (MCP-connected) |
| :--- | :--- | :--- |
| **How it works** | The model emits a geometry file; a human imports it | Model → connector → the application's **own scripting API** → the running document |
| **Feedback** | None. The model never sees the result | **The application sends back a view of what it did**, and the model issues the next command against it |
| **State** | The file | **The running document** |
| **Observed** | An elevation → a `.dae` file in 5–10 min, imported by hand ([[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|sujS9Mgveo4]]) | Prompt → reasoning → FreeCAD Python API → **screenshot of the viewport returned** → analyse → next command, repeating ([[_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp\|6trAkQY5_kc]]) |

- **The closed loop is what lets a model build something step by step** rather than in one shot, because it can react to what it actually produced.
- **⚠️⚠️ But note what the feedback channel IS: a screenshot. The model checks its own work by looking at a picture of it** — which places the verification step squarely inside the precise-visual-interpretation weakness measured on [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]]. **The loop is closed; its feedback is the unreliable channel.**
- A comparable path exists for Revit via the **pyRevit** plugin plus an MCP extension and a desktop-client connector entry, and Claude is reported connecting directly to **Rhino and Revit** to model from a single instruction. [sources: [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp|vmVvpKSSxWE]], [[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects|la8Ml1fQfOg]]]

## 2. ⚠️ The feedback/token trade-off, which is a real engineering decision

The FreeCAD connector ships **two configurations**, and the choice generalises far beyond it:

- **With viewport screenshots** — after each command the model receives the text result **and an image**, so it "can actually see what it built and react to it visually." **More tokens on every single operation.**
- **`only_text_feedback`** — **no image**; only object names, dimensions, and success or error messages. **Significantly fewer tokens per operation.**
- **Stated guidance: screenshots for short sessions of one or two parts; text-only for long sessions with many back-to-back operations.**

> **→ The general form: visual feedback buys the agent the ability to notice what it did wrong, and costs tokens on every operation. Text feedback is cheap and blind.**
>
> **⚠️⚠️ And the reason to record it here rather than adopt it: this project has already chosen a third option that neither source has.** `check_dxf_closure.py`, `check_wall_junctions.py` and `raster_fidelity.py` are **deterministic** feedback — not expensive-and-fallible, not cheap-and-blind, but **exact, machine-checkable, and able to fail a build.** **The trade-off above only binds when the checker is the model itself.** That is the whole argument for gates over inspection, arriving from outside.

## 3. ⚠️⚠️ What it can do, and the one category it cannot

**A Revit session demonstrated on camera, and the split in its results is clean.** [source: [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp|vmVvpKSSxWE]]]

**Succeeded** — all of it transcription: creating walls from a drafted plan, adding a floor per room, placing doors, **naming and numbering every room**, adding room tags and windows. The operator's own comparison: *"doing a better job than a fresher who has just started using Revit."*

**Failed** — all of it spatial logic:

- A plan **closed on all sides**, with no circulation.
- **A forgotten wall** — *"it forgot to add a wall over here for some reason."*
- **A door to a bedroom placed outside the building.**

**⚠️ The operator's own conclusion is the finding, and he states it plainly: *"It can't plan right now. What it can do is basically create a model from your existing floor plans."***

> **→ An agent-connected CAD is a MODELLING ACCELERATOR from a plan that already exists, not a space planner.** Every success was transcribing something specified; every failure was inferring something that was not.

- **⚠️ This corroborates, from an entirely different tool, the rule already on [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7: an agent generating building geometry silently supplies the values you did not specify.** There it invented 5-inch walls, a 9-ft ceiling and a standard door. Here it invented a door position and omitted a wall — **and nothing flagged either.** The mitigation is unchanged: **require an agent to enumerate every value it supplied that the prompt did not, and treat each as a defect to resolve from evidence.**
- **⚠️ Directly relevant to this project's `v0` route**, which is to model from the printed dimension strings over a registered raster rather than to ask an agent to design. **This is the external evidence that the route is the right one** — the failures are precisely in the part this project never delegates.

## Source Notes

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp\|vmVvpKSSxWE]] | The Revit integration path; the modelling-accelerator-not-planner finding and its three named failures | 4 (partial) |
| [[_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp\|6trAkQY5_kc]] | The closed-loop architecture; the screenshot-versus-text feedback trade-off | 3 (partial) |
| [[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|sujS9Mgveo4]] | The open-loop contrast, and its measured fidelity — see [[18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation\|AI for Concept and Visualisation]] §3 | 2 |
| [[_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling\|YT_HOjQiiHJ714]] (2026-09-11) | The original file-generator finding this page refines, and the silently-supplied-values rule | — |

**⚠️ Both new sources are channel-growth vehicles** (a lead-magnet PDF, subscribe requests, a "the results scared me" framing). **No capability verdict from either is routed.**
