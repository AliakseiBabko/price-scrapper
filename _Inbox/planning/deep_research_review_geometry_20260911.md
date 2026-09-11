# Review — Gemini's geometry and agent-modelling report

**Created 2026-09-11.** Grades the report Gemini produced against [`deep_research_brief_geometry_and_agent_modelling_20260911.md`](deep_research_brief_geometry_and_agent_modelling_20260911.md), following the precedent of [`deep_research_review_20260908.md`](deep_research_review_20260908.md) — **grade what a model returns; never adopt it unread.**

- **Source**: Google Doc `1TMssvUXaG7CSaI4c9-0JKJM3R6FXrJhsWKZAtT_ms9c`, "Technical Audit: Programmatic Architectural Modeling and Agentic BIM Pipelines".
- **How it was read**: `qa-management/.agents/scripts/read_google_doc.py --id …` (read-only), run from that repo's root with `.agents/scripts` on `PYTHONPATH` so the OAuth credentials at `.local/google/` resolve. **56,946 characters, 6,761 words.**

## ⚠️⚠️ First — 84 numeric values are MISSING from the text, and this is measured, not suspected

The Docs API reports **1,109 `textRun` elements and 84 `inlineObjectElement`s**. The reader walks paragraphs and tables only, so **all 84 inline objects were dropped.** They carry **no alt text — 0 of 84 have a `title` or `description`** — so nothing is recoverable from the API.

**Two were downloaded and opened to identify them. They are rendered images of the values themselves** — the first reads `1/32 inch` (Revit's join-proximity threshold).

> [!WARNING]
> **→ Every formula and a large share of every figure in that report is an image, and the text around them reads as gaps**: *"a built-in spatial proximity threshold (nominally or )"*, *"corridors must provide an unobstructed clear width of at least "*, *"errors ranging from "*, *"exact match)"*.
>
> **So this review covers the report's ARGUMENTS in full and its NUMBERS only where they happen to sit in running text.** Any figure below without a stated value is one I have not seen. **If a specific number matters, it must be read off the document visually** — or the 84 images pulled and OCR'd, which is a job worth doing only for the handful that decide something.

## The verdict on the report as a whole

**Substantially better than the 2026-09-08 report, and its core arguments are sound and mechanistic.** It answers all six questions, gives a clear verdict per question, and — unusually — **tells us to change almost nothing**, which is the honest answer and not the flattering one. Its citation list is largely real and checkable (buildingSMART IFC4x3 docs, IfcTester docs, Solibri rule pages, OSWorld, CavalierContours, `slvs_py`, the same `mapid.by` СН 3.02.01-2019 PDF this vault already holds).

**But it contains three claims that are verifiably false, two of which are about THIS REPO'S OWN STATE, and it repeats a failure mode the brief explicitly predicted.** Those are in §C.

---

## §A — What it answers well, question by question

### Q1 — Wall junction topology: **do NOT adopt `IfcRelConnectsPathElements`**

**This reverses the hunch that prompted the brief, and the reason it gives is mechanistic rather than hand-waving: the relationship is *semantically passive*.**

> Downstream platforms — it names Solibri, BIMcollab, Navisworks and **Blender/Bonsai** — *"do not construct or trim 3D geometry from relationship entities during import. These engines expect explicit, pre-resolved boundary geometry in the form of `IfcExtrudedAreaSolid` or `IfcFacetedBrep`."* A file that annotates a junction with the relationship but ships overlapping volumes **displays a clash**. Writing it costs graph overhead — relationship objects, connection geometries, priority arrays — *"without providing practical geometric utility to a headless rendering or drafting pipeline."*

**Verdict: retain the ledger. It calls it *"entirely adequate and… pragmatically optimal practice"* for monolithic partition legs.** Commercial engines resolve solids internally *before* export; the IFC relationship exists for semantic archiving.

**And it names the ledger's real failure modes, which is more useful than the verdict:**

- **Non-orthogonal angles break the formula.** `solid = clear + owned corners` presumes rectangular prisms; at an oblique junction, assigning a rectangular corner volume leaves either an unmodelled triangular void or a protruding *miter ear*.
- **High-valence nodes are indeterminate on ties.** At a T- or X-junction, *thicker-then-longer* decides nothing if the legs share thickness and length.
- **It cannot arbitrate multi-layer assemblies** — e.g. gypsum wrapping a corner while insulation terminates at the stud face.

**The stated fix if we ever go non-orthogonal is NOT the IFC relationship** but 2D planar clipping: buffer centrelines to nominal widths, partition the intersection polygon along angular bisectors, allocate cells to legs, then extrude. **Shapely/GEOS — which we already have.**

It also gives the commercial formalisms concretely: **Revit** uses ASM, a 1-to-5 layer priority (Structure→Finish 2), with Butt/Miter/Square-Off arbitration on ties; **ArchiCAD** uses pairwise CSG with an Intersection Priority Number 0–999, breaking ties on creation order. Underneath: straight skeletons, half-edge/DCEL arrangements, non-manifold corefinement.

### Q2 — Raster→geometry: **the most actionable section, and it earns its place**

**Verdict: manual transcription validated by chain closure is *"adequate, mathematically safe, and established practice"*; replacing it with autonomous VLM extraction *"will introduce regressions into the verified geometry layer."***

⚠️⚠️ **It names three blind spots in chain closure, and they are real:**

1. **Compensating errors** — an over-read on one segment cancels an under-read on another, and the chain still sums.
2. **It cannot validate unchained interior clearances** at all.
3. **It cannot localise which segment is wrong.**

**And it gives three orthogonal validators that fix those:**

| Validator | What it does | Why it matters here |
| :--- | :--- | :--- |
| **Scale-factor invariance (cross-ratio consensus)** | `pixel_length / printed_value` forms a tight unimodal distribution across an affine-rectified drawing; reject outliers | **Catches a digit substitution even when the chain sums correctly** — the blind spot above |
| ⭐ **Planar cycle vector loop closure** | Model the layout as a directed planar graph; evaluate closure around each room circuit. **If two adjacent cycles fail and their neighbours pass, the shared edge is the bad reading** | **Fault LOCALISATION, which we do not have.** This is the single most valuable idea in the report |
| **Modular coordination filter** | Penalise values off standard module multiples and known unit thicknesses, re-evaluate against the nearest candidate | Cheap statistical prior; ⚠️ but see the norm caveat in §C |

**The error profile is also concrete and it converges with the video batch:**

- **Digit substitutions cluster in visually confusable pairs**; zero insertion/deletion gives discrete decade errors.
- ⚠️ **Extension-line snapping is BIMODAL, not Gaussian** — the reader snaps either to the intended witness tick *or to the opposite face of the wall*, producing a discrete error equal to the wall thickness or half-thickness.
  - **This is the same finding as `YT_9tfvs3XW5qQ`'s "the ink has width"** (`00_Master/Drawing_Conventions_From_Practice.md` §6), reached from measurement statistics rather than from a practitioner's habit. **Two independent routes to the same conclusion.**

**Its recommended pipeline**: numeric-whitelisted OCR (PaddleOCR/Tesseract 5) over pre-segmented regions → pair with witness lines via a Line Segment Detector → gate on scale invariance + modular likelihood → **use a multimodal model only as an isolated fallback judge on high-resolution crops that fail consensus, never as an end-to-end digitiser.**

⚠️ **On the VLM benchmark table: treat it with care.** Its headline comparison comes from a **vendor's own blog** (`calibras.dk`, February 2026) in which that vendor's own system beats the general model — **presented in the report as an "independent benchmark", which it is not.** The exact-match percentages are visible in running text (≈51% vs ≈57%) but the IoU figures and several model names are inside the dropped images. **The directional claim — frontier VLMs are unreliable on dense dimensioned drawings — is well supported; the specific numbers are not safe to quote.**

### Q3 — Constraints vs coordinates: **keep absolute coordinates**, and one open item closes

**Verdict: absolute coordinates are *"adequate, mathematically sound, and established practice"*; adopting SolveSpace or FreeCAD Sketcher is *"unnecessary over-engineering that will degrade pipeline reliability when handling as-built site variances."***

Named pathologies: **over-constraint** (as-built walls are never truly perpendicular, so rigid orthogonality plus true measured dimensions fails to converge), **bifurcation/branch jumps** (a partition flips across a centreline because both topologies satisfy the scalar constraints), **singular Jacobian** on near-parallel walls propagating instability to unrelated partitions, and **topological naming fragility** — the same failure that plagues FreeCAD.

> [!IMPORTANT]
> **⚠️ This CLOSES open item 2 on `Drawing_Conventions_From_Practice.md`** — *"can our DXF/SVG pipeline express a proportional dimension?"*
>
> **No, and neither can anyone else's.** In DXF a dimension is a static entity (`AcDbAlignedDimension`/`AcDbRotatedDimension`) with definition points fixed via group codes 10/11/13/14; **a `1/2` or `EQ` string is an arbitrary text override in group code 1 that nothing computes from** — edit adjacent geometry and the override stays stale. Autodesk's parametric constraint networks (`AcDbAssocNetwork`) are proprietary and unsupported by `ezdxf`. In IFC, dimensions are `IfcAnnotation`/`IfcTextLiteral` presentation, and **the schema contains no constraint solver.**
>
> **→ The RemPlanner `1/2` notation found in Round 1 is a PRESENTATION convention, full stop.** It is still worth adopting for exactly the reason recorded then — it survives as-built variance where an absolute figure cannot — but **it is a string we draw, not a relation anything solves.** That also answers the linked question of whether Bonsai's annotation subsystem is needed: not for this.

It also reports how the intent is properly drawn under **ГОСТ 21.501-2018 / ГОСТ 2.307-2011**: an explicit dash-dot symmetry axis through the element, and «Равно» or equal fractional increments where spacing is equal without fixed values. ⚠️ **Those are Russian standards — see §C.**

### Q4 — Agents driving a modeller: **programmatic generation wins, and MCP has a different job**

**Verdict: *"PROGRAMMATIC CODE GENERATION driving a headless Python pipeline… is adequate, superior to alternative paradigms, and represents modern engineering best practice. There is no empirical evidence in 2025–2026 indicating that GUI-driving or direct visual computer-use agents can match the reliability of a code-generating pipeline for building geometry."***

Reasons given: sub-pixel snapping is impossible for a screen-space agent (a 2-pixel targeting error misses an intersection snap and leaves disconnected wall profiles); **multi-step compounding** across the 20–40 GUI operations a single room needs; and **modal dialog deadlocks** — the example being *"Wall joins cannot be resolved"*, which is precisely our domain.

⚠️ **The one genuinely new architectural suggestion, and it is good**: *"Where MCP provides genuine value is as a semantic abstraction layer. Rather than exposing low-level CAD tools to an agent, the developer can expose an MCP server that operates directly on the project's canonical layout data"* — letting an agent adjust layout parameters, swap variants or query rule compliance while local Python compiles and validates deterministically. **That fits this repo exactly and costs little.**

It also catalogues the MCP servers that exist for Blender, FreeCAD, Revit and Rhino with their failure modes (UI-thread blocking, topological re-indexing, transaction locks, token overhead on geometry payloads). ⚠️ Its OSWorld figures sit partly in dropped images and its model names could not all be verified — **take the direction, not the scores.**

### Q5 — Rule checking: **the finding that changes our plan**

> [!WARNING]
> **⚠️⚠️ IDS 1.0 EXPLICITLY EXCLUDES GEOMETRIC AND SPATIAL ANALYSIS.**
>
> IDS can check that a property exists and falls in numeric bounds. **It cannot compute spatial clearances between disjoint objects, check corridor widths, test turning envelopes, or calculate boundary overlaps.**
>
> **Most of our 50 rules are spatial** — minimum clear widths, adjacency, avoid-rules. **So "adopt IDS", which the 2026-09-08 gap analysis proposed, would not have consumed them.** This is the most consequential correction in the report.

**Its replacement route is concrete and buildable from what we already have**: keep the rules in structured JSON/YAML; generate an `.ids` XML and run **`ifctester`** for the alphanumeric/property subset; extract 2D room footprints via **IfcOpenShell** and evaluate spatial predicates in **Shapely** for the geometric subset; **serialise failures to BCF-XML via `ifcopenshell.bcf`** so violations open in Blender/Bonsai with camera coordinates and element GUIDs. It supplies a worked Python sketch. It names Solibri's spatial rules (209/247 circulation, 246 accessible space, 248 clearance around objects) as the commercial equivalent, at a seat cost it rejects.

### Q6 and the source directory — both useful

**Costs** (⚠️ all inside or adjacent to dropped images where stated as ranges; the ones in running text): LiDAR survey of a flat in Minsk **$80–150**, outsourced millwork shop drawings **$100–250**, outsourced interior renders **$150–350**, against Revit $2,835/yr, ArchiCAD $2,250/yr, Solibri $2,500/yr. Its render figure is consistent with the 2026-09-08 advice to outsource rather than build an asset pipeline.

**The source directory is the best part of the deliverable after §Q2**, and it is exactly what was asked for — named people and repos rather than a summary:

- **People**: Dion Moult (Bonsai/IfcOpenShell, OSArch founder), Thomas Krijnen (IfcOpenShell/IfcGeom), Jeremy Tammik (The Building Coder, Revit API and ASM internals), realthunder / Lei Zheng (FreeCAD topological naming, `slvs_py`), Jonathan Westhues (SolveSpace).
- **Repos**: `IfcOpenShell/IfcOpenShell`, `BonsaiBIM/Bonsai`, `realthunder/slvs_py`, and ⭐ **`jbuckmccready/CavalierContours`** — 2D polyline offsetting/clipping built to avoid self-intersections and miter-join artefacts, which is directly the non-orthogonal fallback named in Q1.
- **Forums**: OSArch (`community.osarch.org`), FreeCAD BIM subforum, buildingSMART, and ⭐ **`Proekt.by` — the Belarusian engineering forum**, described as where licensed ГИПs discuss enforcement of СН 3.02.01-2019 in practice. **A genuinely new intake route for `16_Legal_and_Regulations/`, and the only Belarus-specific source in the whole report.**
- **YouTube**: OSArch, BIM Voice, MangoJelly Solutions, The Building Coder presentations. ⚠️ None yet preflighted against `processed_video_ids.txt`.

---

## §C — ⚠️⚠️ Three verifiable errors, two of them about THIS REPO

**All three were checked against the repo or its primary sources today, not judged by feel.**

### 1. It cites a regulation that was repealed in full five months ago

The report bases its Belarusian layer on *"Постановление Совета Министров Республики Беларусь № 384 от 16.05.2013"*, cites `pravo.by`'s page for it, links a `proekt.by` thread about it, and carries **"Resolution 384" into its final summary matrix.**

**This vault holds the primary source that repeals it.** `00_Master/processed_sources.csv`, run `run_20260908_postanovlenie164`: Постановление **№ 164 of 3 April 2026** *"REPEALS postanovlenie No. 384 of 2013 IN FULL (plus eleven partial repeals), so every guide, article and video citing 384 is superseded."*

**→ The report is superseded on exactly the axis the brief warned about, and our own note predicted this failure in advance.** Its wet-zone 25 % allowance happens to be independently correct — the vault verified it from СН 3.02.01-2019 §4.9 — but **it is right by coincidence of the norm, not by the regulation it cites.**

### 2. It invents a regulatory provenance for our 50 rules

It states the rules are *"drawn from Belarusian regulatory frameworks — principally СН 3.02.01-2019 and Постановление № 384."*

**Checked `data/layout_rules/rules.jsonl` directly:**

- **50 of 50 rules are `epistemic_status: practitioner_opinion`.**
- Authors: **Maxim Novikov 18, Sergey Dolgushev 12, Alexey Zemskov 8, Дизайнер Дмитрий К 7, NSDSGN 5.**
- **`regulation_ref` appears 0 times.**

**→ Our rules are named practitioners' heuristics, not norms. The report's §Q5 is therefore built on a false premise about what it is being asked to consume.** The *mechanism* it proposes (ifctester + Shapely + BCF) survives — but **"check the layout against СН 3.02.01-2019" and "consume `rules.jsonl`" are two different jobs, and the report merged them.** Keeping them separate matters: standing rule 3 says nothing in this vault is a flat fact, and a practitioner's 1100 mm corridor minimum must not be presented to anyone as a Belarusian requirement.

### 3. It claims we already implement a pattern we do not

Recommending its "Two-Stage Evaluated Layout Pipeline" — intent as functions upstream (`"offset": "wall.length / 2"`), compiled to immutable absolute coordinates — it asserts this is *"the correct structural pattern, which the pipeline currently implements."*

**Checked `data/variants/*.json` and `data/canonical/current_apartment_base.json`: no patch carries any expression.** The only matches to an expression-like pattern were two file paths and one key name (`ceiling_centre_per_room`).

**→ The recommendation is sound and worth considering. The claim that we already do it is false**, and it is the flattering kind of error — it converts an open recommendation into a reassurance.

### And two failures the brief predicted, both materialised

- ⚠️ **The Russian-norms substitution.** It cites **ГОСТ 28984-2011** as governing residential modular coordination *in Belarus*, and **ГОСТ 21.501-2018 / 2.307-2011 / 2.303-68** for dimensioning practice, **without once naming СТБ or ТКП.** (ГОСТ 28984 is an interstate СНГ standard so it may well apply — but the report does not say so, and standing rule 4 means nothing here goes to `16_Legal_and_Regulations/` unflagged.) **Its modular filter in Q2 rests on those figures, so the filter's thresholds are Russian-sourced until checked.**
- ⚠️⚠️ **The laser-scan recommendation repeats the error retracted on 2026-09-08.** It proposes a LiDAR survey to *"eliminate manual baseline transcription errors entirely"*, describing the pipeline as reconciling raster discrepancies against site reality. **The flat is not built** (`tools/cad/PROVISIONAL_MODEL_POLICY.md`: *"a planning baseline, not an as-built survey"*). **There is nothing to scan.** The $80–150 Minsk figure is worth keeping for handover, when it becomes an acceptance-inspection tool — exactly where the retraction placed the laser meter.

---

## §D — What to act on

**Nothing in this report requires changing the geometry layer, and that is its main finding.** Four items are worth doing, in this order:

1. ⭐ **Build the planar-cycle loop-closure check for the `v0` reconstruction.** It is the one capability chain closure cannot give us — **fault localisation** — and it needs only a planar graph over data we will already have. Pair it with the scale-ratio consensus gate, which catches the compensating-error case that defeats chain closure.
2. **Re-plan the rule gate around IDS's actual limits.** `ifctester` for properties, **Shapely for every spatial rule**, BCF-XML out via `ifcopenshell.bcf`. ⚠️ And keep two tracks separate that the report merged: **practitioner heuristics (`rules.jsonl`, opinion) and Belarusian norms (СН 3.02.01-2019, requirement).**
3. **Consider the MCP-over-canonical-data layer.** Small, fits the existing architecture, and avoids the failure modes of every CAD-driving MCP server the report catalogues.
4. **Add `Proekt.by` as an intake source** for Belarusian regulatory practice, and preflight the four named YouTube channels. ⚠️ **Nothing from the report's own regulatory claims should be routed to `16_Legal_and_Regulations/`** — it cites a repealed act.

**Deliberately not acted on**: the LiDAR survey (nothing built to scan), the modular-coordination thresholds (Russian-sourced, unchecked), every benchmark percentage (vendor blog or dropped image), and the "two-stage pipeline" framing as a description of current state.

## Open items this review leaves

- **The 84 dropped images.** Worth pulling only for specific decisions: the СН corridor clear widths (we currently hold only Zemskov's 1100 mm practitioner figure), and the scale-ratio rejection threshold if item 1 gets built. ⚠️ **Everything else can stay unread.**
- **Whether `arXiv:2609.07362` ("BlueprintAgent") is real and says what the report claims.** Cited with a URL and dated days before this review; it is the sole support for the constraint-triggered-revisit pattern. **Unverified.**
- **Whether ГОСТ 28984-2011 applies in Belarus as an interstate standard**, which decides if the modular filter's thresholds are usable. A question for `Proekt.by` or the primary text.
