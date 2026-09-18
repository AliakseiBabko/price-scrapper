# Joint review — what Codex and Antigravity answered, reproduced and weighed

**2026-09-18.** Both engines answered `joint_review_prompt_toolset_20260918.md`. This
records what was **reproduced**, what was **overstated**, where the two **disagree**,
and how my own recorded prediction scored.

---

## 1. Defects reproduced — all four of Codex's, one WORSE than reported

| # | claim | verdict |
| :--- | :--- | :--- |
| 1 | the walkthrough loads a stale GLB | ⚠️⚠️ **CONFIRMED, worse** |
| 2 | `build_variant.py` builds the `reference_only` sketch | ⚠️⚠️ **CONFIRMED** |
| 3 | the album target has split authority | ⚠️ **CONFIRMED** |
| 4 | the furniture/finish layer is documentation, not code | **CONFIRMED** |

### 1.1 The stale GLB — and the number is 18 against **24**, not 23

```
data/outputs/variants/v0-existing/model.glb        Sep 16 11:32   IfcWall painted: 18
data/outputs/variants/v0-existing/model.ifc        Sep 17 18:54   IFCWALL(     :  24
```

`tools/blender/walk_viewer.html:64` loads `model.glb` with **no source-IFC hash and no
shell-signature check**. Codex said 23 walls; the current IFC carries **24**, so the
gap is one wall wider than reported.

> ⚠️⚠️ **This is the retired-schematic failure recurring one output downstream.** The
> same shape as the acceptance "lapse": an artefact that *describes* its own freshness
> while nothing reads it. The GLB is a day and a half behind the model it depicts and
> looks complete.

### 1.2 The variant builder — reproduced exactly, exit 0

```
$ ./.venv-ifc314/Scripts/python.exe tools/layout/build_variant.py \
      data/variants/v1-homestyler.json --no-render
  walls: 39   doors: 0   windows: 0   status: "reference_only"   EXIT=0
```

**Why the guard missed it.** `build_variant.py:181` refuses a base whose status
*starts with* `RETIRED`. v1's base is `data/canonical/current_apartment_shell.json`,
whose status reads `from_developer_layout_via_cad_not_field_verified` — schema
`0.1.0`, **15 walls**. Not the string, so not refused.

> ⚠️⚠️ **`check_variant_basis.py` correctly refuses v1 — and this path never asks it.**
> The refusal we built and tested with 23 seeds is bypassed by using the other builder.
> A gate only guards the door it is nailed to.

### 1.3 Split authority on the album

Three live numbers: **11** (`Planning_Project_Deliverable_Set.md:69`, stale),
**32** (`zk-dubravinskiy-full-album.json` — the *active* target, owner 2026-09-07),
**37** (the lab|remont album, which you supplied 2026-09-18 as what you want). The
32-sheet JSON is what tooling would read. **This is a scope question only you can
settle.**

### 1.4 The asset layer

`data/catalog/` **does not exist**. `Finishes_and_Furniture_Data_Model.md` says so
itself: *"Proposed 2026-08-26, not yet built."*

> ⚠️ **A synthesis neither engine made:** that document says the mechanism is in place
> because `furniture.place` and `finish.set` "already exist as operations in
> `tools/layout/build_variant.py`" — **the very builder defect 1.2 shows is obsolete.**
> The furniture mechanism is attached to the path that cannot express a mitre.

## 2. Where Antigravity OVERSTATED

**Claim: the rough-in layers "contain zero geometry and zero data in `data/canonical/`."**
**False as written.** The directory holds `ventilation_shafts.csv` (V1, V2 — footprints,
channel counts, chain-closure provenance), `plumbing_anchors.csv` (P1, P2, corrected
2026-09-17), `service_outlets.csv`, `services_observed.csv`, `electrical_existing.csv`.

**What survives the correction, and it is the real point:** what exists is *vertical and
fixed* — risers and anchors. What does not exist is **horizontal routing**: duct runs,
ceiling drop zones, drainage falls. Against a 2500 ceiling that is a genuine gap, and
its sequencing argument stands.

**Claim: the 2500 ceiling conflict is the risk "nobody has named."** It is named, with
the same arithmetic, in `apartment-layout-modelling/SKILL.md:115` — 150–200 mm duct
void, ducts first, **2300–2350 before any fitting**, no height recoverable from the
screed. Antigravity rediscovered a recorded constraint and reported it as unnamed.

**Claim: vertical wall-bed mechanisms need 2350–2450 mm.** ⚠️ **Unsourced, and it
contradicts the vault.** `design_envelopes.csv` ENV-WALLBED-OPEN records 2000 mattress
+ mechanism + plinth ≈ **2150–2250 against 2500**, with the clear/slab-to-slab
distinction explicit. Antigravity asserted a dimension with no evidence — the exact
failure rule 9 exists for. **Not adopted.** Its tall-wardrobe version may still hold;
that needs a source, not a round number.

## 3. Where they genuinely DISAGREE — and it is question 1

This is the substantive split, and it is sharper than I predicted.

| | Antigravity | Codex |
| :--- | :--- | :--- |
| the asset layer | **Ungated.** "If an asset fails to load, has broken normals, or has an unmapped texture, **the build still passes.**" | **Do NOT create an ungated layer** for anything affecting fit, procurement, services or quantities. Gate hashes, dimensions, units, bounding boxes, transforms, collisions. **Only artistic appearance is review-only.** |

> **Codex is right, and the reason is already in this repo.** Antigravity's boundary is
> drawn at the *file type* — meshes and textures are ungated because they are meshes and
> textures. Codex draws it at the **claim**: a dimension is gateable whatever file it
> arrives in. That is the same distinction as **presence vs requirement** in the covering
> work, and the same as **`review_only` vs `issued`** in the services gate. A sofa's mesh
> is appearance; a sofa's **600 mm depth** is a fit claim that decides whether a corridor
> works. An ungated layer would let the second ride in on the first.
>
> ⚠️ Codex's sharpest line, and it should be a standing rule: **"A manufacturer mesh must
> never become dimensional evidence. The canonical product dimensions validate the mesh,
> not vice versa."** That is rule 9 applied to a file instead of a drawing.

**They agree on everything else that matters:** keep canonical-data-first; keep Blender;
chat cannot remain the only *spatial* interface past step 5; a spatial input channel is
needed that is not "learn to model."

## 4. Codex contradicts one of OUR pages, and is probably right

`Realtime_Walkthrough_EEVEE.md:65` says the walkthrough **"is achievable today."** Codex:
false for the stated goal — flat colours, zero textures, no collision, vertical free
flight via Q/E, stale geometry, and **EEVEE is not involved in the browser viewer at
all**. The GLB/Three.js viewer and the EEVEE recipe are two different things and the page
conflates them.

It also says our screen-space statement is **too absolute**: Blender 5.2 offers probe-based
*or* screen tracing, and **screen tracing falls back to probes when rays leave the view**.
Our page already flagged itself as "demonstrated on 4.2, not re-verified on 5.2" — Codex
supplied the re-verification we deferred, from Blender's own 5.2 docs.

⚠️ **Both corrections are to a page I wrote this week.** The page must be fixed before it
is quoted again — that is the ±25 failure repeating.

## 5. My recorded prediction scored **2 of 4**

I predicted: *converge on 1 and 3, disagree on 2 and 4.*

| Q | predicted | actual | |
| :--- | :--- | :--- | :--- |
| 1 asset layer | converge | **disagree, sharply** | ❌ |
| 2 Blender for 5–7 | disagree | **both keep Blender** | ❌ |
| 3 chat interface | converge | converge | ✅ |
| 4 walkthrough | disagree | disagree | ✅ |

**What I got right anyway:** *"the asset layer is the weakest part of the architecture and
the part with the least built behind it."* Both engines went there first, and Codex's
defect 4 proved it — the catalogue does not exist.

## 6. The order the work should now take

Codex's sequence and Antigravity's sequence agree on the first move and differ after it.
Merged, with the rough-in placed where Antigravity argues it belongs:

1. **Freshness checks on every derived view.** A GLB or `.blend` carries its source IFC
   hash and shell signature; the viewer refuses a mismatch. *This is the defect that is
   live right now and it is cheap.*
2. **Retire or repair `build_variant.py`.** Either it resolves through `ResolvedGeometry`
   or it refuses anything not schema v2. Today it silently builds a sketch.
3. **Settle 32 vs 37 sheets.** Owner decision, blocks scope.
4. **Rough-in envelopes before furniture** — duct routes, ceiling drop zones, drainage
   falls, against 2500. Antigravity's strongest contribution: *proving a 2500 ceiling
   takes the ventilation before choosing a wardrobe.*
5. **The asset registry**, on Codex's boundary: identity + sha256 + units + expected
   dimensions + licence, gated; appearance review-only.
6. **One proof room**, then decide Three.js vs Unreal on measurement, not feature lists.

## 7. The biggest risk, as both stated it

Antigravity: **critical-path inversion** — decorating before the rough-in is solved.
Codex: **a persuasive visualization becoming a second, weaker model.**

> These are one risk seen from two ends, and **Codex's framing has the evidence**: the
> stale GLB is *already* a convincing picture of a model that no longer exists. A grey
> correct model loses an argument to a pretty wrong one. Everything this repo does —
> provenance, gates, seeds — was built so the data wins that argument; a rendered view
> with no freshness check hands the win back.
