# Session state, 2026-09-18 — written before compaction

**Purpose: survive a context compaction.** Everything below is already in git; this is the index to it, so the next turn does not depend on a chat summary. Head is `90c7826`.

---

## 1. What is awaiting an answer right now

**A joint review prompt went to Codex AND Antigravity**, identical text: `_Inbox/planning/joint_review_prompt_toolset_20260918.md`. **Their two answers are the next input.** It asks five things:

1. does canonical-data-first stretch to **furniture, appliances and textures** — bought assets and appearances, not authored facts — or does it need a second, explicitly ungated layer, and what is the boundary rule?
2. is **Blender right for steps 5–7 specifically** (real furniture libraries, uploaded textures, walkable interior)?
3. does **chat-as-the-only-interface** survive fifty furniture items when it handles three walls?
4. does the **walkthrough** survive EEVEE's screen-space GI, or does it need a game engine / stills?
5. what is the **biggest unnamed risk**?

⚠️ **My own prediction, for checking against:** they converge on 1 and 3, disagree on 2 and 4. **The asset layer is the weakest part of the architecture** and the part with the least built behind it.

## 2. The owner's goal, in his terms

The model is the thing; drawings represent it. **He does not draw and will not learn.** Chat is the permanent interface. Path: basic layout ✅ → basic 3D ✅ → functional zoning → layout options from sizing/volumes/daily scenarios, which fix zoning **and engineering systems** → **real** furniture, appliances and uploaded textures → colour, lighting, design variants → **a walkthrough of the finished flat**, not renderings.

## 3. Where the model actually is

**Everything green.** `v0-existing/spec.json` is schema v2, **compiled from `ResolvedGeometry`** — 25 walls, 2 shafts, real polygons, M2/M6b mitred, 11 opening leaves in 10 units.

| gate | state |
| :--- | :--- |
| `check_dxf_closure.py` + selftest (24 seeds) | PASS |
| `raster_fidelity.py` + selftest (7 seeds) | PASS |
| IFC identity / types / connections / IDS | PASS |
| `check_variant_basis.py` + selftest (23 seeds) | PASS |
| `check_baseline_acceptance.py` + selftest (20 seeds) | PASS (correctly reports PROVISIONAL) |
| `covering_patches` (34 seeds), `boundary_patches` (37 seeds) | PASS |

## 4. Open items that need the OWNER, not more work

| | what | where |
| :--- | :--- | :--- |
| **1** | **v0 baseline acceptance** — `pending_owner_review`, 7 scopes. Nothing downstream is decision-bearing until he accepts | `00_Master/V0_Baseline_Review_Sheet.md`, `data/canonical/v0_baseline_acceptance.json` |
| **2** | **Wall-bed cabinet external width** from a manufacturer. **Blocks the only proven sleeping arrangement.** 1800 is excluded; 1600 on R6/R7 *cannot be relied upon* — 1750 clear less ±50 tolerance less ~20 plaster ≈ 1680 against a cabinet typically 1690–1740 | `design_parameters.csv`, `design_envelopes.csv` |
| **3** | **`V1` shaft footprint unestablished** — blocks any V1-clearance question | its own acceptance scope |
| **4** | **`BAND-KL-3`** — desk or no desk at the living-zone window. SC-A and SC-B want different answers | `room_depth_bands.csv` |
| **5** | **Electric vs water towel rail.** `T1` is a capped **water** tail; a practitioner source recommends electric because water ones leak | `YT_uTssUK7-mlI` |
| **6** | **Blender 5.2.0 → 5.2.2** (released 2026-09-15). Would need a Bonsai re-probe | `data/outputs/blender_bonsai_environment.json` |

## 5. The design record — where the owner's rules live

- `design_intents.csv` — DI-001…DI-008. **DI-006** (constant = family + RC frame; variable = everything else incl. dividers) and **DI-008** (entrance→storage→bed→window bands) are `governing`. ⚠️ **DI-008 is AUTHORED, not derived** — I claimed the building forced it and that was false.
- `occupancy_scenarios.csv` — **SC-NOW is what gets built** (adults in the 9,36 bedroom, both children in the middle room). SC-A and SC-B swap who occupies the transformable zone; only that branching is confined to the outer bays.
- `design_parameters.csv`, `design_envelopes.csv`, `room_depth_bands.csv`.
- `v1-homestyler` is **`reference_only`, permanently** — a freehand sketch over the same constructor raster v0 came from. Its coordinates are never evidence. The basis gate refuses it by design.

## 6. The findings that changed how the work is done

- ⚠️⚠️ **Four rule-9 errors in three days, all one shape**: quoting a container's bounds as the contained thing's — `solid_mm` for `clear_mm`, envelope for bay clear span, host wall for opening extent. **Check which dimension before using any figure.**
- **Огурцов**: given a drawing, the model got geometry exact and **identity wrong** (лоджия ↔ services duct; taps modelled as glasses; a kitchen mirrored).
- **ChatGPT architecture test**: given no geometry, it got **strategy right and geometry wrong** — room widths exceeding the site width, an illegal stair. **Every failure was a chain that does not close.**
- → **The model reasons well about relationships and holds geometry badly.** Both halves argue for canonical-data-first and for closure gates.
- **Six sources triaged out across three batches for being older than what they describe.** Tooling content ages faster than practice content.

## 7. The target deliverable

`00_Master/Planning_Project_Deliverable_Set.md` now carries a **third observed album** — lab|remont, 45 pages / **37 sheets**, supplied by the owner as what he wants out of this. Sheet 11 is the developer's as-supplied electrics as its own deliverable; sockets, lighting and switches are three separate sheets; развёртки are per room per wall face. ⚠️ **37 sheets × 3 variants = 111 sheets, so the set must be generated.**

## 8. The walkthrough is a procedure, not an aspiration

`18_Digital_Toolchain/analysis/Realtime_Walkthrough_EEVEE.md`. Vulkan → area lights on the window openings + sun → ray tracing and Fast GI at 1:1 → light-probe volume, all probes inside, bake. ⚠️ **EEVEE's GI is screen-space** — only geometry in frame contributes light, a known problem for animation, mitigated but not removed by baked probes. Not re-verified on 5.2. **Single-surface walls leak light; our IFC walls are solids, so we escape that by construction.**

## 9. If asked "what next" with no further input

**The walkthrough of the existing state is buildable today** — geometry exists and is gated, so it is a lighting exercise. It would also honestly test whether the screen-space limitation matters at these room sizes, which is question 4 of the joint review.
