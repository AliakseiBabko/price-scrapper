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

## 5. ✅ Owner decisions, 2026-09-16

1. **RETIRE the schematic outright.** *"It was long ago and I added new data."* `current_apartment_base.json` stops being an input. It is marked retired in place rather than deleted, so the history stays readable.
2. **O2's sill stays DERIVED at 812.** *"All they have are photos."* No tape exists for this window, so the figure keeps its `?` and its ±100 mm caveat, and the model carries it as the uncertainty it is rather than rounding it into a fact.
3. **Door heads stay at `2050?`** — same reasoning. No door is fitted at handover, so these are openings the owner specifies later anyway.
4. **ALL openings get modelled, with their frames.** ⚠️ **Question 4 as originally written — "how much does the loggia matter?" — was wrong to ask**, and the data already answered it: O9 is recorded as *"the single most thermally important element in the flat."* Asking the owner to rank it was a bad question and is retracted.

### What "reproduce the frames" can and cannot deliver

**Frames ARE reproducible for three openings** — `window_frames.csv` records mullion and transom positions as ratios of the opening, with member widths:

| opening | members | pattern |
| :--- | :--- | :--- |
| O2 | mullion at 0.5, 195 mm | two sashes, no transom |
| O3 | mullion at 0.5 + transom at 0.44, 195 / 120 mm | **2 × 2, four panes** |
| O4 | mullion at 0.4348, 195 mm | two leaves — window + glass door of one 1380 unit |

**⚠️ O9 is the exception, and the limit is in the source rather than in the modelling.** Its width is the best-corroborated figure in the whole model — 2939 derived, against apartment 53's printed 2.93 m, **9 mm apart, 0.3%**. Its *pattern* is confirmed from a handover photo: **floor to ceiling, NO parapet, dark anthracite frames, vertical bays split by one horizontal transom at ~1000 mm, at least one opening casement.**

**But that photo is flat 109, whose лоджия is 2.5 m² against our 6.05**, and the record states it plainly: ***"the PATTERN transfers and the bay count and widths do not."***

**So O9 is modelled as: full height, no parapet, one transom at 1000 mm — all evidenced — and a bay count that is an ASSUMPTION carried as one**, labelled in the data and visible in the model's report. It is not measured and must not be drawn as though it were.

**O9 is also the only diagonal opening.** The лоджия is not rectangular: west side M2 = 1850, east side M6b 1170 + R8 1490 = 2660, so it splays 810 mm over MA's 2825 — `hypot(2825, 810) = 2939`. Every other opening is axis-aligned; this one needs an arbitrary angle, which is the actual modelling difficulty and the only one.

**Still unknown and worth a look on site:** whether O9 is single or double glazed. A dark aluminium лоджия frame is often cold single glazing, which changes the thermal case completely.

---

## 6. What this does NOT change

**The DXF, the sheets and the take-off are unaffected** — they already run on the gated data and their gates still pass. **This is a defect in one consumer, not in the geometry.** The renderer, the walkable viewer and the `.blend` viewing file all work correctly; they are simply drawing the wrong flat, and they will draw the right one unchanged once their input does.
