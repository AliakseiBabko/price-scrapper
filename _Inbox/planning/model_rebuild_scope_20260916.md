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

1. ⚠️ **CORRECTED 2026-09-16 — this item was WRONG as first written.** It said "wall coordinates are not in any canonical table" and that "the geometry lives in the exporter, not in the data". **Both are false, and Codex caught it on review.**
   **`data/canonical/v0_named_walls_placed.json` exists, is 25 KB, and declares `authoritative_for: POSITION and FACES`** — the 25 named walls attached to the vector plan's own hatch-validated solids. `export_v0_dxf.py` loads it at its `PLACED` constant. It was written on 2026-09-09 for a stated reason: routing positions through the basic-plan pixel fit scattered walls the drawing had drawn aligned, because that fit has 3.3% anisotropy and residuals to 93 mm, and the vector does not.
   **So the model is HYBRID, and that is the accurate description:** vector-extracted coordinates give position and faces; recorded lengths give `clear_mm` / `solid_mm`; chain closure, corner ownership, placement yielding and loggia closure reconcile the two. The exporter holds the *reconciliation*, not the geometry.
   **The real deficiency is narrower than stated**: that reconciliation is only reachable by running `export_v0_dxf.py`, so a second consumer must either re-implement it or read the DXF — which is why `model_from_dxf.py` reads the DXF today.
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

---

## 7. ⚠️⚠️ Codex review, 2026-09-16 — two of my claims were wrong

Requested by the owner. **Both corrections were verified against the repo before being accepted here**, not taken on the reviewer's word.

### Correction 1 — the coordinate dataset exists (see §3.1, now rewritten)

I claimed there was none. `v0_named_walls_placed.json` is authoritative for position and faces, and the DXF exporter loads it. **My "geometry lives in the exporter" framing was wrong**, and it went into this document and into the review prompt, so the reviewer was working from a false premise on that point and caught it anyway.

### Correction 2 — ⚠️⚠️ the services pipeline already has the failure this document warns about

`tools/layout/sheets/make_services_sheets.py` **hard-codes every socket, switch, light and route as a Python list** — `SOCK` carries wall code, position along wall, face, gang, height, photo evidence and owner decisions as literals, including *«ВЛАДЕЛЕЦ: на G7 две розетки, выключателей нет»*. Meanwhile `electrical_existing.csv` (11 rows) and `service_outlets.csv` (8 rows) exist separately, **and the IFC consumes neither.**

**Worse, and this is the part that matters: the script WRITES `data/canonical/electrical_placement_review.csv`.** Generated code state flows back into a directory whose whole purpose is to be the authored source. **That is the retired-schematic failure again — the same shape, one level down, and already live.** It was not caused by the model rebuild and it is not fixed by it.

### What the review changes about the plan

| Question | Verdict |
| :--- | :--- |
| Master: tables or IFC? | **Tables** — but for an OPERATIONAL reason, not the one I gave. IFC *can* carry psets and provenance; what it cannot do is round-trip evidence, rejected readings and correction history through a BIM editor. The failure mode is **split-brain authority**: geometry moves, the sidecar still describes the old placement, and nothing says which wins. **IFC is the authoritative ISSUED representation, not the authoring store.** |
| Services in 3D? | **Yes — real IFC elements.** Ceiling height, shaft access, clearances and furniture are three-dimensional conflicts. But with **concrete types**: `IfcCableSegment`, `IfcPipeSegment`, `IfcDuctSegment`, `IfcOutlet`, `IfcLightFixture`, `IfcAirTerminal`. `IfcFlowSegment` is deprecated for direct instantiation in IFC 4.3. |
| Routed geometry? | **Terminals and topology first.** Use `IfcDistributionPort` and system membership to express connectivity with no physical path asserted. Three explicit route states — `topology_only`, `design_intent`, `construction_approved`/`as_built` — and **the model must never silently promote topology into a route.** The electrician keeps route freedom within agreed zones; drainage and ventilation need pre-coordination because slope, invert and a 150–200 mm duct zone under a 2500 ceiling are consequential. |
| Chain closure? | **Sound, keep it** — a hand-maintained coordinate table duplicating every printed length would create exactly the coupled-edit problem the gates exist to catch. |
| What breaks first? | **Service identity, and it is already breaking.** See Correction 2. |

### The architecture, as corrected

```
Canonical authored facts + provenance
        ↓
Deterministic geometry/services compiler      ← does not exist yet; the
        ↓                                       reconciliation is trapped
Resolved model graph                            inside export_v0_dxf.py
   ├── IFC          ├── DXF / discipline sheets
   ├── quantities   └── GLB / Blender / renders
```

**The DXF→IFC path is transitional.** It was the right recovery step because the 3D immediately inherited four existing gates, but the DXF must not remain the interchange between this project's own generators. Both exporters should consume the same resolved geometry, keeping independent DXF and IFC gates.

### ⚠️ Ordering consequence, and it inverts the earlier plan

**Extract the geometry compiler BEFORE adding services, not after.** `on_element`, `along_wall_mm`, wall faces, service normals and world transforms have to mean the same thing in the IFC and in every discipline sheet, and today only the DXF exporter knows what they mean.

**And before generating any further services sheet:** give every service a stable canonical ID, move placements out of drawing code into the canonical tables, generate both IFC elements and sheet symbols from those records, and make sheets *select and style* elements rather than invent them. **Derive IFC GUIDs deterministically from the canonical IDs**, or a regenerated model cannot be joined to annotations, review decisions or prior issues.

### One documentation defect this exposes

**`00_Master/Model_and_Views.md` calls `model.ifc` "the single source of truth". That is now wrong** and should read: one logical model in the canonical data, of which the IFC is a compiled representation.

---

## 8. Sequencing, after the second Codex round — and my order was wrong

I proposed "fix the services-authority defect first, then extract the compiler". **That is unsafe if "fix" means the full migration**: migrating placements needs `on_element` and `along_wall_mm` to resolve, and those live in the reconciliation that is still inside `export_v0_dxf.py`. Doing it first would mean writing a second, temporary implementation of exactly the thing being extracted.

**The split is containment (can go first) versus migration (cannot).**

### 1. Contain — ✅ done 2026-09-16

- ✅ **Stop writing into `data/canonical/`.** `electrical_placement_review.csv` is generated review output and now goes to `data/outputs/review/`. It was git-tracked in the authored directory; removed from the index and moved. Nothing reads it, so the move is safe.
- ✅ **Freeze the legacy generator.** `make_services_sheets.py` carries a banner: fix a rendering bug if you must, but a NEW placement, height or owner decision goes in the canonical data, never in its Python lists.
- ⬜ **Assign stable canonical IDs and define the service schema and status vocabulary.** Not started. This is authored-data work and does not depend on the compiler.

### 2. Extract the geometry compiler — ▶️ STEP 1 OF 6 DONE 2026-09-16

✅ `tools/layout/resolve_v0_geometry.py` exists and returns the resolved model, the pre-reconciliation sources and a machine-readable reconciliation report. ✅ `export_v0_dxf.py` is now a thin serialiser over it. **Semantic equivalence proven**: identical wall ids, **max coordinate delta 0.000000 mm**, identical layers and all 93 entities, `dxf_wall_entities` 0 problems both sides, console output identical, `check_dxf_closure` / `check_wall_junctions` / `raster_fidelity` / `structural_assembly` all pass with **34 seeded defects still rejected**.

⬜ **Still to do:** move the four rule functions out of the exporter into the compiler (they are still imported FROM it), and point `model_from_dxf.py` at the resolved model so the DXF stops being an intermediate.

⚠️ **The extraction found a live hazard**: the rules read canonical files by RELATIVE path, so running from `tools/layout` silently produced different geometry — `close_corners` returned 0 fixes instead of 8, and 16 of 25 walls closed against `solid_mm` instead of 19. No error, just a different model. The compiler now pins the working directory.


Move the reconciliation out of `export_v0_dxf.py`. **Preserve byte-equivalent DXF output** and re-run the adversarial gates — `check_dxf_closure` (24 seeds), `raster_fidelity` (7), `structural_assembly_selftest` (14). Expose the shared host-local operations every consumer needs to agree on: **wall face, normal, along-wall position, and local↔world transform.**

### 3. Migrate service authority

Classify every literal in the frozen generator as **observed existing / owner decision / design assumption / route topology**, move it into canonical records, and validate placements through the shared compiler.

### 4. Generate both representations

IFC elements, ports and systems; and discipline-sheet symbols and annotations. **No service geometry invented inside either consumer** — sheets select, filter and style; they do not author.

### 5. Retire the hard-coded path

**Seeded divergence tests first**, then remove the lists and the old write-back. Per standing rule 10, the test that proves the two representations cannot drift has to exist before the thing preventing drift is deleted.

---

### ⚠️ Schema: decide it, do not drift into it

**`model_from_dxf.py` writes `IFC4`.** The deprecation of `IfcFlowSegment` for direct instantiation that justified choosing concrete leaf types is an **IFC 4.3** statement. The conclusion still holds — `IfcCableSegment`, `IfcPipeSegment`, `IfcDuctSegment`, `IfcOutlet`, `IfcLightFixture`, `IfcAirTerminal` are the right entities — **but the schema version must not change silently as a side effect of adding services.** If a move to 4.3 is wanted, make it a deliberate step and test it against Bonsai, the Blender glTF export and every existing gate before relying on it.

### Terminology

Say **"canonical authored data"**, not "the tables". The position authority is JSON (`v0_named_walls_placed.json`), not a CSV, and calling the whole store "tables" is what made it easy for me to miss it.

---

## 9. Third Codex round — identity, and a correction to my acceptance criterion

### ⚠️ "Byte-equivalent DXF" was the wrong bar, and I had already seen why

I set it in §8. It is wrong: DXF serialisation carries handles, timestamps and ordering that change without the model changing. **I had the evidence and wrote the wrong criterion anyway** — regenerating the DXF earlier the same day changed 10 lines with every gate passing, and I called it byte-noise at the time.

**The acceptance bar for the compiler extraction is SEMANTIC equivalence:**

- identical resolved wall / opening / shaft IDs;
- identical layers and entity classifications;
- coordinates and dimensions equal within the exporter's existing precision;
- **identical output from `dxf_wall_entities.py`** — the one reader, which already refuses anything that is not the rectangle promised;
- `check_dxf_closure`, `raster_fidelity`, `check_wall_junctions` and `vector_extent_oracle` all pass;
- **all 24 seeded defects still rejected**;
- the review rendering unchanged where its gate requires it.

### The extraction shape

1. A pure `resolve_v0_geometry()` returning a typed resolved graph plus a reconciliation report.
2. `export_v0_dxf.py` becomes a **thin serialiser** over that graph.
3. Differentially compare old and new output **during** the extraction.
4. **Keep the existing independent gates as the permanent acceptance — not the old implementation.** Retaining the old reconciliation to diff against would make it a second authority, which is the defect being removed.
5. Point IFC generation at the resolved graph.
6. Only then migrate service locators and generate 3D services.

### Identity — preserve CONTINUITY, not the existing strings

**The legacy IDs are not the same kind of thing, and the real data shows it:**

| Legacy id | What it actually is |
| :--- | :--- |
| `E-KL-SOC-K` | an **observation about a group** — *"socket outlets, кухня zone, count 3, height 915-1105"*, from one photo |
| `SW-K` | a **service assembly / take-off** — *"hot and cold water take-off, clamped, rising from the floor, valve tops 500-610"* |
| `SS-B` | close to a **physical element mark** — one sewer connection on P1 |
| `S1` | an individual **drawing symbol** in the frozen generator |

**So a one-to-one migration is not possible and must not be forced.** Where one legacy group becomes several physical elements, the group is retained as an observation or an assembly and its members get new identities.

Design recorded in `_Inbox/planning/services_data_model_design_20260916.md`.
