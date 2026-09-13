# Bonsai / IFC / Blender batch — triage, 2026-09-13

**Owner supplied 11 videos and 2 channels.** All 11 video IDs fresh; both channels entirely fresh (42 and 151 videos).

## 1. ⚠️⚠️ Why this batch is different in kind from the last four

The previous four rounds were general AI-capability sources: mostly a mirror, and correctly triaged as *mechanism kept, scores discarded*. **This batch is not that.** It is Blender + Bonsai + IFC — **the toolchain this project actually runs** (`00_Master/How_To_View_Outputs.md`: portable Blender 5.2 + Bonsai 0.8.6-alpha260801).

And the vault already holds a **decision** about it. `_Inbox/planning/toolchain_gap_analysis_20260908.md` §Kind 3:

> **"Capability we already own and do not use: Bonsai."** … *"no, we need to start using the parts we have."* Bonsai's **drawings subsystem** (sheet generation, camera cut planes, annotation, **dimensions**, **dynamic schedules**, CSS hatches, title blocks) is marked **Adopt for the annotated sheets**, against our hand-rolled SVG→PDF — because hand-rolling *"fails exactly here: dimension chains collide on dense MEP plans."*

**So this batch is not new-capability scouting. It is evidence bearing on an adopt decision already taken and not yet executed**, plus its one explicitly open question:

> **"Whether Bonsai 0.8.6-alpha's drawing subsystem is stable enough headless for our build chain, or whether annotated sheets have to be a GUI step. Testable in an afternoon and worth testing before committing to it."**

**That question is the value filter for everything below.** A video is worth reading here if it changes a field, a datum, a sheet, or that headless/GUI split — not if it shows a nicer program.

## 2. The two channels — opposite verdicts

### `@IfcArchitect` — 42 videos. ⚠️ The highest-relevance channel found so far.

**It is a Bonsai/BlenderBIM channel and nothing else.** Its spine is exactly the annotated-sheet chain the gap analysis says to adopt, and which we currently hand-roll:

| Capability the gap analysis marked "Adopt" | Sources on this channel |
| :--- | :--- |
| **2D drafting / annotation** | `VgvPk78IU0U` (Bonsai Pt 2 — 2D drafting), `xWPLZK_WoS8` (BlenderBim Pt 2) |
| **Section & elevation** | `r0ebxigzM6U` (Bonsai Pt 3), `ClS-6taDO1M`, `khGbssjtpeM` |
| **2D detail** | `QTviOpqz1rw` (Bonsai Pt 4), `MH9MSI7FgVA` |
| **Sheet / page layout + title block** | `HEb7fWJduXg` (Page Layout), **`_vrVETTI5jQ` (Custom Titleblock via Inkscape)** |
| **Lineweights** | `dPWQbjaeoyo` |
| **IFC typing / libraries** | `jTL3a6QwckA` (custom wall type), `0wR5uAUwn8Y` (custom window), `2Q_wtBKa8Dc` (parametric doors & windows), **`dmWjQqyKL3U` (merge two IFC project libraries)** |
| **Phases** | `_hADRIo-ma4` (custom phases) — ⚠️ we carry existing / demolished / new as DXF layers |

**⚠️⚠️ The re-record chain, and it disqualifies the owner's own pick.** `PNoOyCHa_V0` — the one video from this channel in the owner's list — is the **oldest of three recordings of the same floor-plan tutorial**:

| ID | Era | Status |
| :--- | :--- | :--- |
| `PNoOyCHa_V0` | 2022-10, "BlenderBim" | **oldest** — owner's pick |
| `agwK8hbkToM` | 2023-04, "BlenderBim 23.04.17" | superseded |
| `IXRpDka6gLI` | Bonsai era | **current** |

Same for the step-by-step project: a 5-part 2023 BlenderBim series (`kF2k_VW-yrQ` → `HEb7fWJduXg`) **re-recorded** as a 4-part Bonsai series (`Jc896Sob2bU` → `QTviOpqz1rw`). **Under the standing rule that capability verdicts date, the Bonsai-era recordings supersede the BlenderBim-era ones wherever both exist** — the add-on was renamed and its UI overhauled (`tpQjRjB1wnU` is a major-UI-update video). Read the old one only where no new one exists.

**Skip outright: all 8 version-update videos** (`FcbN-N9RKTE`, `zoQO1DHQOcQ`, `oF-0qq_yi34`, `9v9YU2KSMTE`, `FtV9VvnoXlc`, `zoecibNDokE`, `Q2p5PUjd-EM`, `oljVAjW9QVw`, `TZjmswvkGbs`), the 3 install videos, the course trailer, the features reel and the channel-recommendation video. **Release-note content is the purest form of the dating problem** — it is a diff against a version we do not run.

### `@blender3darchitect` — 151 videos. ⚠️ Mostly NOT for us, and the reason is a decision already taken.

The channel is overwhelmingly **"Blender as a CAD tool" GUI technique**: snapping, offset, trim, fillet, polar tracking, align, 3D cursor, SketchUp-migration guides. Dozens of them.

> **⚠️ The gap analysis already ruled on this class: "Native IFC authoring GUI — Keep programmatic. Use the GUI only where visual drafting genuinely beats code."** This project authors its model in **Python + IfcOpenShell + ezdxf**, gated by `check_dxf_closure.py`. **A tutorial on driving Blender's mouse is not evidence about a code path**, and ~100 of the 151 are exactly that. That is a verdict on relevance, not on quality.

**What survives the filter** — the minority that touches a field, a sheet or the headless question:

| Why it survives | Sources |
| :--- | :--- |
| **⚠️ The SVG question, head-on** | **`tDOr7p35QUQ` — "Export drawings as SVG files"**. We generate SVG→PDF ourselves; this is the same output from the other engine |
| **⚠️ Annotated sheet end-to-end** | `SwUFuCTlMOo` (floor plan → scaled CAD-style PDF), `FL28f31J9d4` (2D drawings with Bonsai + **door swing direction**), `GXe13vg39oQ` (dimension line **styles**), `ZoCUEssXt_0` (parametric dimension controls, Bonsai 0.8.5 — **one minor version below ours**) |
| **⚠️⚠️ Quantity takeoff from the model** | **`5te37tEEfvs` (how much paint a room needs)**, `dsod69UcXTE` (areas by material). This is `Qto_SpaceBaseQuantities` — the exact line the gap analysis says the screed/waterproofing/skirting lines need |
| **IFC semantics we hand-roll** | `co0lOhmkfH0` (**layered walls & IFC materials**), `kEFgXvcbHEw` (custom IFC types), `0ktp-S7Lev0` (**void management** for doors/windows), `2Uqj2sORVcg` (walls from polylines), `60UZZkRbmTQ` (extend walls to slab), `MiY8oPp7E94` (**wall corners** with shear) |
| **⚠️⚠️ Mirroring** | **`1WPw5NRJQmM` — "Blender's Mirror Doesn't Work for BIM"**. This vault has a live mirrored-flat problem: `validate_services_observed.py` **refuses an unflipped mirrored-flat reading**, and `_Survey/` holds mirrored comparables |
| Interchange | `btKlamZF8oI` / `Zoh_YR5SeXc` (Revit + DWG import), `d5BKgffzGEY` (SketchUp → IFC) |

**⚠️ Concentration note**: this is a single voice with a heavy "Blender Just Got X — And It's Free" headline formula. **151 videos from one presenter cannot corroborate anything** — the same finding that governed `@ConstructIQ`. Treat the whole channel as one source.

## 3. The 11 supplied videos

**All `en-orig`** — caption manifest checked per video before fetching, per the rule established by the previous batch. No language trap this round.

⚠️ **`xXmvs0PK_Bg` and `mq63GWbgWdM` are the same channel, same title** ("How To Turn JPG image to 3D Floor Plan - Blender") three years apart — a re-record pair. Both fetched because they are 3 and 5 minutes; **only one to be processed**, the other marked `duplicate_skipped` once confirmed.

Outcome recorded below after processing.

---

## 4. Outcome

**All 11 fetched (zero failures), all 11 read in full, none skipped unread.** 10 processed, 1 `duplicate_skipped`. **81 new facts, yield 7.4 per video.**

**Two new pages**: `Model_To_Drawing_Pipeline.md` (the batch's core), and `Raster_To_Geometry.md` — **extracted** from `Drawing_Conventions_From_Practice.md` when that page hit **390 of the 400 backstop**, via `tools/split_page.py apply` (parity verified: 227 content lines, 0 missing, 41/41 citation IDs). ⚠️ **Extraction, not a merge**: the headings were topical, not dated, so the page was long-and-coherent rather than fragmented.

### ⚠️⚠️ The five findings that changed something

1. **The `Adopt` verdict is vindicated on a better ground than it was argued from.** It was argued from *annotation quality*; **the real difference is ASSOCIATION** — the BIM route **generates** the drawing from the model, the mesh route **exports** it and permanently detaches it. **This project's whole discipline is built on not keeping two copies of one fact.**
2. **⚠️⚠️ But the headless question must be restated, because the association leaks in four places** — moving a door does not move its opening; a parameter change needs an explicit refresh; flipping a swing displaces the door; parametric conversion loses materials. **Each is a manual gesture a script must know to call, and a missed one yields a plausible-looking IFC, not an error.** → Ask *"which re-synchronisation steps must a script call explicitly, and what gates the result?"* **And build the opening-coincidence check before adopting anything.**
3. **⚠️⚠️ A plan image is not uniformly scaled — 45 mm of anisotropic format-fitting distortion measured in one sheet.** Bears on `raster_fidelity.py`'s single global registration, **and on the variance study**, whose −45/+30 mm deltas are the same magnitude.
4. **⚠️⚠️ A live hazard in our own documentation**, from the only controlled experiment in four batches: the `.blend` and IFC become linked, so **`Ctrl+S` writes to the canonical IFC** — and `How_To_View_Outputs.md` tells the owner to open it *to look at it*. **Neither gate would catch it; both assert the DXF.** A warning block was added to that page in this round.
5. **⚠️⚠️ A standing open item settled by evidence: wall direction.** Two languages, two tools, same rule — **and this source adds that the error propagates into every hosted object, silently.**

### Handling and exclusions

- **All UI paths, panel names, keystrokes, version numbers and install steps discarded** across every source — the add-on was renamed once already and two sources are pre-rename.
- **⚠️ Concentration**: `xlmbZHIaHJw` is the **seventh Justin Geis source** across two channels; `4JYFYvNg5Xk` is from `@blender3darchitect`, itself triaged here. **Flagged on the pages, not just the notes.**
- **⚠️ One advertising finding**: `DgovrfgLxYs` carries **two affiliate promotions**, one a standalone product segment unrelated to the subject — **`promotional_ratio: very_high`, the highest recorded in this vault**, near-skipped at 3 facts.
- **A genuine disagreement recorded unresolved**: whether window heads align to door heads. Neither practitioner gives a reason.
- **No prices carried** — none comparable under rule 2. **North American framing figures (2x4 = 89, 2x6 = 140, 4-inch studs) flagged and NOT transferred**; this flat is block-and-masonry. **No regulatory content.**

## 5. What is left, and what should come next

**Neither channel was processed — both were triaged only.** Recommended order, on the reasoning above:

1. **⚠️⚠️ `@IfcArchitect`, the annotated-sheet spine, Bonsai-era recordings only** — `VgvPk78IU0U` (2D drafting), `r0ebxigzM6U` (section & elevation), `QTviOpqz1rw` (2D detail), `HEb7fWJduXg` (page layout), **`_vrVETTI5jQ` (custom titleblock)**, `dPWQbjaeoyo` (lineweights). **This is the closest thing to a direct answer on what adopting the drawings subsystem actually involves.**
2. **⚠️ The `@blender3darchitect` minority only** — **`tDOr7p35QUQ` (export drawings as SVG)** first, since it is our own output format from the other engine; then `5te37tEEfvs` / `dsod69UcXTE` (quantities from the model), `1WPw5NRJQmM` (mirroring, which this flat has as a live problem), `FL28f31J9d4`, `GXe13vg39oQ`. **Not the ~100 GUI-technique videos.**
3. **⚠️ Reproduce before relying**: the four leaky associations, the `Ctrl+S` linkage, and the `IfcDoorStyle` reading — all against our installed Bonsai 0.8.6-alpha260801. **The `Ctrl+S` mitigation is worth applying regardless, since the fix is cheap and the failure is silent.**

**Still outstanding from earlier rounds** (unchanged by this one): `@RemPlanner` 5 of 6 lessons; `@k_dmitry` rounds 2–5; `@ConstructIQ` Tier 2's four conditional items.
