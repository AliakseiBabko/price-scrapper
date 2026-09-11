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

## §C — ⚠️⚠️ Four verifiable errors, two of them about THIS REPO

**All four were checked against the repo or its primary sources today, not judged by feel.**

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

### 4. ⚠️⚠️ It states a Belarusian corridor-width requirement that the norm does not contain

The report lists, under Belarusian regulatory constraints: *"Clear Corridor Widths (СН 3.02.01-2019): Corridors leading to living rooms must provide an unobstructed clear width of at least [dropped]; entrance vestibules and kitchen corridors must maintain [dropped]."*

**Checked against the primary source this vault already archives** — `_Archive/processed_sources/20260908_SN_3.02.01-2019_zhilye_zdaniya_normy_by_preview.pdf`, 25 pages, read directly:

- **Every «коридор» clause in the norm concerns ВНЕКВАРТИРНЫЕ corridors** — the building's common corridors in a corridor-type block — and clause 10 does not even state a figure, referring out instead (*«Наименьшую ширину внеквартирных коридоров и дверей в них следует принимать в соответствии с…»*).
- **A search for every width figure in the document returns only stairs, landings, lift machinery rooms and doors** — 1.15 m stair flights, 1.4 m landings, 0.5 m / 1.4 m / 1.8 m door and access dimensions. **There is no in-apartment corridor or passage width anywhere in it.**

⚠️ **Stated with the caveat the vault already carries for this copy**: it is the `normy.by` preview, watermarked *для ознакомления*, and **does not include Изменения № 1 and № 2** — so the honest claim is *"not present in this copy"*, not *"does not exist"*. **But the report cites the base norm, and in the base norm it is not there.**

**→ This is the most dangerous of the four errors, because it is the one that would have been routed into `16_Legal_and_Regulations/` as a Belarusian requirement and sat next to Alexey Zemskov's 1100 mm practitioner figure — turning an opinion this vault correctly labels `practitioner_opinion` into a fabricated norm.** Standing rules 3 and 4 both exist to stop precisely this.

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

---

# ROUND 2 — the follow-up answers, reviewed 2026-09-11

**Source**: Google Doc `19av7NprlkO9EMVttS113sNHFVmWIjqJ7-sIpKXOyuh0`, read the same way. **3,510 words.** Questions asked in [`gemini_followup_questions_20260911.md`](gemini_followup_questions_20260911.md).

## ✅ The formatting instruction worked, and the effect is total

**Round 1: 1,109 `textRun` + 84 `inlineObjectElement` (images of the numbers, no alt text). Round 2: 524 `textRun` + ZERO inline objects.**

**Every threshold, formula and figure is machine-readable.** That one instruction is now a standing requirement for any Deep Research request whose output will be read programmatically — **put it in the next brief.**

## ✅ It accepted all four corrections, and withdrew one outright

**Behaviour worth recording, because it is the opposite of the 2026-09-08 report's:**

| Correction | Response |
| :--- | :--- |
| № 384 repealed by № 164 | **Accepted and redone.** Adds the dates: published on pravo.by **7 April 2026**, in force **8 July 2026** |
| СН corridor widths fabricated | ⭐ **"was factually incorrect and is withdrawn."** No defence, no hedging |
| ГОСТs cited for Belarus | **Answered per-standard with enacting instruments** — see below |
| arXiv paper unverified | **Supplied authors, date, venue and two verbatim quotations**, plus a scope caveat that undercuts its own recommendation |
| Vendor benchmark | **"published by Calibras ApS on their commercial blog evaluating their own proprietary product… not an independent, peer-reviewed study."** |

## ⭐ The corridor answer is better than a correction — it closes the question

- **СН 3.02.01-2019's corridor clauses govern only внеквартирные corridors.** Confirms what was read off the archived PDF here.
- **Intra-flat corridor width is NOT regulated in Belarus for an ordinary apartment** — not by СН 3.02.01-2019, nor ТКП 45-3.02-209-2010, nor СНБ 3.02.04-03. *"Purely a design and ergonomic decision."*
- **Where a minimum does appear**: flats designated for wheelchair users (СН 3.02.12-2020) need **1.15–1.20 m**; and fire/egress rules constrain **door clear widths** (flat entrance door ≥ 0.80 m, interior room doors ≥ 0.70 m) rather than corridor width.
- ⚠️ **Traces the origin of the phantom figure**: *"The '1.0 m clear width for corridors leading to living rooms' was a legacy requirement from Soviet СНиП 2.08.01-89 (Clause 2.1), discontinued when Belarus adopted its national codes."*

> **→ This settles how `corridor.min_clear_width` must be labelled.** Alexey Zemskov's **1100 mm** stays exactly what `rules.jsonl` already says it is — **`practitioner_opinion`, with no Belarusian norm behind it and none against it.** The vault's existing labelling was right; there is simply nothing to promote it to.

## The ГОСТ answer, and why the modular filter survives anyway

- **ГОСТ 2.307-2011 — legally applicable in Belarus**, enacted by **Постановление Госстандарта РБ № 50 of 27 July 2011**, effective 1 January 2012.
- **ГОСТ 21.501-2018** — adopted interstate (Protocol 111-П, 30 Aug 2018) with Belarus voting in favour; used by Belarusian design institutes, **but national СН and ТКП supersede it on conflict**.
- **ГОСТ 28984-2011** — interstate; Belarus codified modular coordination nationally instead (ТКП 45-1.01-159-2009 / СНБ 1.01.02-01).

⚠️⚠️ **And the genuinely smart move: it defuses its own jurisdiction problem.** *"The modular coordination filter does not rely on statutory compliance."* It rests on **manufactured block increments** — cellular concrete to **СТБ 1570-2005**, silicate partition blocks to **СТБ 1117-98**, in 100 / 120 / 200 / 300 / 600 mm steps — so it works as **a physical prior about the building stock, not a legal one.** **That makes the filter usable regardless of which standard binds, and it finally cites Belarusian СТБ rather than Russian ГОСТ.**

## ⭐ Question 5 — the loop-closure algorithm is buildable, with one trap

**The specification is concrete and internally coherent:**

1. **Represent the plan as a planar straight-line graph**; edges carry displacement vectors.
2. ⚠️ **Do NOT use a fundamental/minimum cycle basis** (it names Paton's), because it *"generates long, overlapping cycles spanning across the entire building"* — which destroys localisation. **Use the minimal bounded faces of the planar embedding**: build a DCEL, sort each vertex's outgoing half-edges counter-clockwise by `atan2`, define `next(e)` as the predecessor of `twin(e)` in that order, trace faces, and **discard the outer face by its negative signed area**.
3. **Incomplete chains are handled by counting degrees of freedom per face** — 0 unmeasured edges → validate closure; **1 unmeasured → solve it deterministically (`delta_missing = -sum(measured)`) and propagate outward**; **≥2 → under-constrained, excluded from the gate without failing the model.** That last behaviour is exactly right for a gate.
4. **Localisation via a syndrome vector** over the signed face–edge incidence matrix `B`. A single misread edge shared by faces A and B gives `c_A = +e_k`, `c_B = -e_k`, all others zero → the edge is `Edges(A) ∩ Edges(B)` minus the edges of every passing face.
5. **Three or more failing cycles → L1-norm syndrome minimisation** (basis pursuit: minimise `sum |e_j|` subject to `B·e = c`), justified because OCR errors are sparse.
6. References given: **Mehlhorn & Michail (2009)** on minimum cycle bases in planar graphs, and **Mikhail & Gracie (1981)**, *Analysis and Adjustment of Survey Measurements* — the Gauss-Markov condition-adjustment model for closed traverses. ⚠️ **The survey-adjustment lineage is the important one: this is a solved problem in geodesy, not a novel invention.**

> [!WARNING]
> **⚠️ ONE INTERNAL CONTRADICTION, AND IT IS A REAL TRAP.** Its implementation note says to use **`networkx.algorithms.cycles.minimum_cycle_basis`** — **which is precisely the kind of basis step 2 tells you not to use.** `minimum_cycle_basis` is a graph-theoretic minimum-weight basis and is **not embedding-aware**; it does not return planar faces in general.
>
> **→ Implement the DCEL face traversal it actually describes. That needs no `networkx` at all — only `atan2` sorting and a signed-area test.** Anyone who implements by reaching for the named shortcut gets long overlapping cycles and loses the localisation the whole design exists for.

**Dependency check, run here**: `shapely` 2.1.2 ✅ and `numpy` 2.5.1 ✅ are present in `.venv-ifc314`; **`scipy` and `networkx` are not.** Only the multi-error L1 step needs `scipy.optimize.linprog` — **the single-error case is pure set intersection, so a first version needs no new dependency at all.**

## Question 6 — the scale gate, now fully specified

- **Metric**: `S_k = V_k / L_k` (mm per pixel).
- **Rejection**: `abs(S_k - S_ref) > 3.0 * sigma_robust`, or in practical terms **a deviation of more than 5.0 % from the reference scale**, for drawings whose scan skew and lens distortion stay under 1.5 %.
- ⭐ **Robust estimation, which was the real question**: **median for `S_ref`, and `sigma_robust = 1.4826 * MAD`.** It gives the reason — mean and standard deviation are destroyed by exactly the gross outliers being hunted (`1200` read as `7200`) — and notes MAD's **50 % breakdown point**, so half the strings can be garbage without moving the reference.
- **Multi-scale sheets**: cluster the 1D `{S_k}` with DBSCAN (`eps = 0.05 * S_guess`) or a 1D GMM, **snap cluster centroids to standard scale ratios** (1:10/20/25/50/100/200), then **partition spatially by the convex hull of each cluster's dimensions** so a detail viewport is judged against its own scale.

## Question 7 — verified against PyPI here, and it was right

| Claim | Verified |
| :--- | :--- |
| `ifctester` is a separate PyPI distribution | ✅ **Real. Latest 0.8.5**, *"IFC model auditing tool with support for IDS"*, 27 releases |
| `ifcopenshell.bcf` does not exist; the package is **`bcf-client`**, importing as **`bcf`** | ✅ **Real. Latest 0.8.5**, *"BCF-XML file handler"*, 20 releases |
| Both align with our IfcOpenShell | ✅ **All three are at 0.8.5** |

**So its explanation of why the imports failed — packaging boundaries, not a wrong recommendation — is correct.** It also states the source lives in the IfcOpenShell monorepo at `src/bcf` but ships standalone, and that **Bonsai reads BCF 2.1 and 3.0 natively** under Scene Properties → BIM Collaboration Format. ⚠️ The Bonsai claim is unverified here.

## Question 8 — IDS will not gain spatial rules, and it explains why

**"No"** for IDS 1.0, 1.1 and 2.0 — and the reason is architectural rather than scheduling: adding spatial predicates would force **every** IDS validator to embed a 3D kernel, destroying the lightweight XML-validator design. It notes **mvdXML is deprecated and superseded by IDS**, and that the research alternative (**BOT + SHACL**, with GeoSPARQL for geometry) is too slow for mesh intersection work.

**Verdict: custom Python over Shapely/IfcOpenShell is the established route, and there is no standard coming.** Its suggested shape — **rules in a readable YAML DSL compiled to Shapely predicates** — fits `rules.jsonl` closely and keeps geometry out of the rule text.

## Question 9 — MCP over project data, with real precedents

Argues the pattern is MCP's intended design, citing Anthropic's own **`server-sqlite` / `server-postgres`** (semantic tools plus deterministic constraints as the gate) and **IaC servers** that edit declarative state and run `terraform plan` locally. Sketches a `FastMCP` server for this project exposing `get_layout_state()` and `propose_layout_patch()`, where the patch runs the compiler and **all** gates and returns structured assertion output.

⚠️ **The "OSArch FastMCP prototypes (late 2025 – early 2026)" are described without a link or repo name — the one place in an otherwise well-cited answer where a claim is unverifiable.**

## ⚠️ What remains unverified after round 2

- **The arXiv quotations.** It supplied authors, an EMNLP 2026 Findings venue and two verbatim passages including **Beam F1 0.994 vs 0.301 zero-shot vs 0.820 fixed-pipeline on 300 sheets**. ⚠️ **A model confirming its own citation is weak evidence, and 0.994 is a very high number.** **But it volunteered the caveat that matters**: tested **only on structural RC framing plans, not interior partition or non-bearing renovation layouts** — so it does not transfer to our task regardless of whether the figures hold.
- **Two № 164 claims the vault's own primary-source reading does not contain**: the **abolition of Госстройэкспертиза for residential re-planning** from 8 July 2026, and that **co-owner consent no longer needs notarisation**. Everything else it says about № 164 — the gas/central-heating-only project track, partitions and openings by эскиз via «одно окно», insulation without a проект, glazing outside the definition — **matches `run_20260908_postanovlenie164` in `processed_sources.csv`.** ⚠️ **The two new ones need the primary text before they go anywhere near `16_Legal_and_Regulations/`.**
- **Bonsai's BCF 2.1/3.0 support**, and the OSArch MCP prototypes.

## What to build, in order

1. ⭐ **The loop-closure checker** — DCEL faces (not `networkx`), DOF-counted per face, single-error localisation by set intersection. **No new dependencies.** Defer the L1 multi-error path until a real multi-error case appears.
2. **The scale gate** — median + `1.4826 * MAD`, 5 % rejection band. Small, and it pairs with (1) to catch the compensating-error case chain closure cannot.
3. **The rule gate** — `pip install ifctester bcf-client`, YAML DSL to Shapely predicates, BCF-XML out. ⚠️ **Keep practitioner heuristics and Belarusian norms in separate rule sets**; round 2 makes that split sharper, not softer, since the corridor norm turned out not to exist.
4. **Defer the MCP layer** until (1)–(3) exist, since its whole value is calling gates that must be built first.
