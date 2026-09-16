# Scope — rebuilding the 3D model from the gated geometry

**2026-09-16.** Written after the owner opened the 3D model in Blender, compared it against `_Drawings/review/v0_dxf_readback.png`, and said it was significantly different. **It is, and he is right to distrust it.** This scopes the fix.

**Not a proposal to accept as written** — §5 lists what only the owner can decide.

---

## 1. The finding: two datasets describe this flat, and the 3D model uses the weaker one

| | 3D model / renders / walkable view | DXF readback, sheets, take-off |
| :--- | :--- | :--- |
| Source | `data/canonical/current_apartment_base.json` | `wall_blocks.csv`, `wall_corners.csv`, `wall_openings.csv`, `ventilation_shafts.csv`, … |
| Walls | **18** | **25** |
| Wall thickness | 2 values, 0.15 / 0.25 m, assigned by default | **5** — 75 / 120 / 200 / 250 / 300 mm, per wall |
| Wall class | none | concrete / aerated block / external / loggia enclosure |
| Ventilation shafts | **0** | 2, with full footprints and chain-closure provenance |
| Loggia | rectangular | **2939 mm diagonal glazing** (O9) |
| Openings | 11, invented verticals | 11, **tape-measured** where it matters |
| Guarded by | **nothing reads this file** | `check_dxf_closure` (24 seeded defects), `raster_fidelity` (7), `check_wall_junctions`, `vector_extent_oracle`, `structural_assembly_selftest` (14) |

**It is the same flat.** Room areas agree: living 19.48 vs 19.49, small bedroom 9.35 vs 9.36, kitchen 5.25 vs 5.24, bathroom 3.10 vs 3.09, WC 1.24 vs 1.24. Bedroom is 1.4% out, entrance hall 3.3%.

**But the schematic is an early reconstruction that nothing checks, and it is what every 3D view is built from.** This is the second-source-of-truth failure `00_Master/Model_and_Views.md` exists to prevent — except it is between two files in `data/canonical/`, not a stray `.blend`, which is why no gate caught it.

---

## 2. ⚠️⚠️ The windows are the worst of it, and the numbers are not close

**Every window in the schematic is 1800 wide, sill 1000, head 2100 — the same three numbers four times, with no provenance anywhere in the file.** Every other significant figure there carries a source; `openings` carries none.

**What the gated data actually records:**

| id | type | wall | width | sill | head | basis |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- |
| **O3** | window | MC | **1763** | **266** | **2251** | **TAPE, owner, 2026-09-07, on a very similar flat** |
| **O2** | window | MB | **1760** | 812? | 2251? | width TAPE; sill DERIVED and flagged *"Confirm the sill"* |
| **O4a** | window | MA | 600? | **735** | 2235 | sill TAPE, confirmed to 1 mm by a second photo |
| O9 | glazing | M2→M6b | 2939 | — | — | the loggia's diagonal run |

**The living-room window is 1985 mm tall on a 266 mm sill — very nearly floor to ceiling, leaving 249 mm to the slab.** The model draws it **1100 mm tall starting 1000 mm up**: the sill is out by **734 mm** and the height by **885 mm**. That is not a tolerance question. It changes the light, the elevation, the radiator position and every render.

**And O9 does not exist in the model at all**, so the loggia reads as a closed rectangular box instead of a glazed diagonal.

> ⚠️ **A fill-vs-opening defect was found and fixed the same day** — every window PANE was generated at z 0.00–1.10, lying on the floor slab, while its void was cut correctly. Fixed in `model_from_spec.py`, gated in `audit_model_quality.py`, watched failing on a seeded model. **That was a separate bug. Fixing it does not make these numbers right** — it only makes the wrong numbers self-consistent.

---

## 3. What the gated data gives, and what it does not

**Gives, directly:** per-wall thickness, material class, `clear_mm` / `solid_mm` and corner ownership; opening widths, sills and heads with provenance; both ventilation shafts as placed footprints; room areas and rollouts; the loggia loop.

**Does NOT give, and this is the real work:**

1. **Wall COORDINATES are not in any canonical table.** `export_v0_dxf.py` derives them at run time by chain closure, corner ownership, `wall_placement_directives.csv` and loggia-loop closing. The only coordinate table, `structural_assembly_vertices.csv`, holds **6 rows for one assembly**. So the geometry lives in the exporter, not in the data.
2. **Door head heights are uncertain** — `2050?` on every internal door, derived from one photo of another flat at ±60 mm. Tolerable: the developer fits no doors, so these are openings the owner will specify anyway.
3. **O2's sill is flagged for confirmation** in its own note. It is the one window whose vertical geometry is still a derivation from a photo of a different flat at ±100 mm.
4. **Coordinate systems differ.** The gated data is millimetres on the drawing's origin (x ≈ 2980–9380, y ≈ 14645–15990); the IFC is metres from 0. A rebuild needs one stated transform, and getting it wrong is silent.

---

## 4. Approach — and the recommendation is the cheap one

**Option A — generate the IFC from `v0_developer_layout.dxf`.** The DXF is already the gated artefact, and `tools/layout/dxf_wall_entities.py` already exists as *the one reader of wall entities*, refusing anything that is not the rectangle the exporter promises. A new `tools/ifc/model_from_dxf.py` would read walls from the DXF, heights from `storey_height_m`, and openings from `wall_openings.csv`.
**Cost:** moderate. **Benefit: the 3D model inherits everything the four existing gates already guarantee**, because it is built from the artefact they assert.

**Option B — refactor `export_v0_dxf.py` to emit a coordinate table** that both the DXF and the IFC consume.
**Cost:** higher, and it touches a file guarded by 24 seeded defects. **Benefit:** one derivation, two consumers, no DXF round-trip.

**Recommended: A**, then B later if the round-trip proves awkward. A is reversible and does not disturb a gated exporter.

**Either way the IFC must carry a gate of its own**, per standing rule 10 — at minimum: wall count and per-wall thickness match `wall_blocks.csv`; every opening's sill and head match `wall_openings.csv`; both shafts present. **Seeded and watched failing**, or it is not a gate.

---

## 5. ⚠️ What only the owner can decide

1. **Is the schematic retired, or kept?** If the 3D model moves to the gated geometry, `current_apartment_base.json` has no consumer left except the renders and the walkable view, which move with it. **Keeping both is what caused this.** Recommendation: retire it, and say so in the file itself rather than deleting it, so the history stays readable.
2. **O2's sill — 812 derived, or measure it?** It is the one window whose vertical geometry is still a photo derivation of a *different flat*. A tape on the real window settles it. Everything else that matters is already measured.
3. **Door heads at `2050?`** — accept ±60 mm from a photo, or measure one door opening and apply the standard.
4. **How much does the loggia matter?** O9's diagonal glazing is real geometry the model omits entirely. It affects the loggia renders and the balcony-insulation work, and nothing else.

---

## 6. What this does NOT change

**The DXF, the sheets and the take-off are unaffected** — they already run on the gated data and their gates still pass. **This is a defect in one consumer, not in the geometry.** The renderer, the walkable viewer and the `.blend` viewing file all work correctly; they are simply drawing the wrong flat, and they will draw the right one unchanged once their input does.
