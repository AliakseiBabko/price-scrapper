# AGENTS.md — entry point for any AI agent working in this repository

Read this first. It is a **router**, not a manual: it tells you what this repo is and where the real instructions live. Detailed procedure lives in skills, which load on demand.

**Read-status per agent — verified by cold-session test 2026-08-31, not self-reported:**

All three were asked, in a fresh session with this repo as the working directory and no tools allowed, for two facts that exist **only** in this file (that `16_Legal_and_Regulations/` is Belarus-only, and the merge-to-main rule).

| Agent | Receives this file automatically? | Evidence |
| :--- | :--- | :--- |
| **Antigravity** | **Yes** | Answered both, plus listed all four skills and knew the deprecated one. Discovery walks up from cwd; no `GEMINI.md` needed. |
| **Codex** | **Yes** | Answered both exactly. ⚠️ Note it had earlier *reported* it does not receive this file — **its self-report was wrong**; trust the test. |
| **Claude Code** | **Yes, via the `@AGENTS.md` import in `CLAUDE.md`** | ⚠️ **Failed this test on first run** and was the only agent that did. `CLAUDE.md` held a markdown *link*, which is inert prose — Claude loaded the stub, read "see AGENTS.md", and never opened it. Replaced with an `@`-import and **retested in a fresh session the same day: passes.** This is why the stub must stay an import. |

> [!WARNING]
> **None of these agents can be trusted about its own context loading.** Codex gave three mutually inconsistent accounts of whether it reads this file; Claude Code asserted it was readable via the stub when it was not. **Ask an agent what it knows, never how it knows it** — the answers are evidence, the introspection isn't.

---

## What this repository actually is

**A personal renovation knowledge base and planning vault** for one specific apartment renovation, built from ~813 extraction notes taken mostly from Russian-language YouTube practitioner sources, routed into ~243 wiki pages.

> [!IMPORTANT]
> **`README.md` describes the original project, not the current one.** This repo began as a Node/TypeScript/Playwright/SQLite marketplace price scraper (`src/`, `package.json`, `data/`). That code still exists and still runs, but it is now a *minor component*. If you read only the README you will work on the wrong thing.

The renovation vault is the primary work. The scraper feeds appliance pricing into it.

## Layout

| Path | What it holds |
| :--- | :--- |
| `_Sources/` | ~813 extraction notes, one per source. **Raw evidence — never edit to fit a conclusion.** |
| `_Knowledge/store/` | Intermediate store: `Durable_Facts`, `Rules_Heuristics`, `Numeric_Data`, `Source_Index`, `Change_Log`, `Cross_Source_Comparison_Tables` |
| `00_Master/` | Project-level docs. **Start with `project_decisions.md`** — decisions taken about this apartment, and the open items. Also the deliverable roadmap, `processed_sources.csv`, `exchange_rates_reference.md`, `wiki_page_format.md` |
| `01_`–`17_` | Room and topic wiki folders. Each has a compact guide page plus `analysis/` detail pages |
| `_Archive/processed_sources/` | Archived transcripts. **Frozen — hashed for provenance; never edit, not even to fix a BOM** |
| `_Drawings/` | **Everything I draw**, and the only place drawings go. `sheets/` = album sheets, the deliverable, regenerated in place and never versioned by filename. `review/` = the current working drawing for the owner to check, **overwritten** — git holds the previous state. `evidence/` = crops that a finding cites. See `_Drawings/README.md` |
| `_assets/` | **Referenced assets only** — appliance and fixture images. It held 38 superseded drawing iterations until 2026-09-07; those are gone from the tree, not from history |
| `_Survey/` | **The photo survey of three comparable flats** — positioning plans plus 30 photos, indexed by `data/canonical/photo_positions.csv`. Third-party watermarked listing photos, so the **bytes are gitignored and identity is kept via sha256 in `_Survey/manifest.csv`** — same treatment as the album PDFs. See `_Survey/README.md` |
| `_Precedents/` | **Other people's designs for this apartment** — organised **per author and per project** (`design_projects/<author>__<project>/`), plus `market_listings/` for listing imagery. `roster.csv` is the index. Bytes gitignored, identity via sha256 in each `manifest.csv`. ⚠️ **The model is NEVER built from these, and undimensioned means undimensioned.** See `_Precedents/README.md` |
| `_Inbox/planning/` | Channel triage plans, backlogs, work-in-progress notes |
| `src/`, `data/`, `dist/` | The legacy price scraper (Node/TS/Playwright/SQLite) |
| `tools/` | Python tooling — see below |
| `.agents/skills/` | Project-specific skills. **See the discovery note below — this differs per agent** |

## Skills

> [!WARNING]
> **Skill discovery is asymmetric across agents. Verified 2026-08-31.**
> - **Antigravity** auto-discovers `.agents/skills/**/SKILL.md` and mounts them.
> - **Codex** does **not** discover them. If you are Codex, read the relevant `SKILL.md` file explicitly before starting work.
> - **Claude Code** does not treat them as Skill-tool-invocable either; read the file.
>
> Do not assume a skill is loaded because it exists.

| Skill | Use it for |
| :--- | :--- |
| `.agents/skills/renovation-knowledge-intake/SKILL.md` | **The main pipeline.** Ingesting any new source into the vault: extraction notes, the store, wiki routing, USD normalisation, dedup, archiving. Read this before processing any source |
| `.agents/skills/apartment-layout-modelling/SKILL.md` | Layout case datasets, frames → case JSON → rules JSONL → prose |
| `.agents/skills/residential-bim-geometry-rules/SKILL.md` | Geometry conventions for the model |
| `.agents/skills/homestyler-cad-to-revit/SKILL.md` | CAD/Revit interchange |

Shared cross-project skills live in `../ai-skills/skills/` and are linked into `~/.claude/skills/` and `~/.codex/skills/`. `youtube-transcript-fetch` is the one you will most often need.

## Tools — run these, don't reimplement them

| Tool | Purpose |
| :--- | :--- |
| `tools/verify_batch.py --base <ref>` | **Run before every commit that touches vault content.** Mojibake, BOM, retired patterns, citation-ID drift, USD rounding and rate checks |
| `scripts/verify_batch_selftest.py` | Guards the above against over-suppression. Run after changing it |
| `tools/check_page_sizes.py` | **Enforces the 300-line hard page ceiling — exits non-zero on a breach.** Also warns below it, and flags FRAGMENTED pages, which means merge instead |
| `tools/split_page.py analyse\|apply\|merge` | Does the split or the merge. Moves sections by line range byte-for-byte, then asserts content-line and citation-ID parity |
| `tools/canonical/validate_services_observed.py` | **Run after adding observed existing services.** Refuses a wall that does not exist, a millimetre figure with no named scale reference, an offset with no datum, and an unflipped mirrored-flat reading. Protocol: `00_Master/Existing_Services_Capture_Protocol.md` |
| `tools/precedents/ingest_precedent.py` | Add a design precedent in one command — copies, hashes, skips byte-identical duplicates, marks every file `examined: no` |
| `tools/precedents/validate_precedents.py` | **Run after any change under `_Precedents/`.** Rehashes every file against its manifest, enforces the role vocabulary, and **fails if a layout case cites a file nobody has examined** |
| `tools/layout/check_wall_junctions.py` | **Run after any change to the flat's wall geometry.** Fails on an overlap, a gap, or an L-corner void that nothing owns. A corner is a solid: counted twice or zero times are both wrong |
| `tools/layout/build_wall_corners.py [--write]` | Builds and checks `wall_corners.csv`, the corner ledger that decides which wall owns each L-corner (thicker, then longer). `solid_mm = clear_mm + the corners a wall owns` |
| `tools/layout/validate_structural_assemblies.py` | **Run after any change to `structural_assemblies.csv`, `structural_assembly_vertices.csv` or a `structural_element_id`.** A wall is a calculation leg; an ASSEMBLY is the physical element. Checks members resolve in both directions, recomputes the footprint area by shoelace, and refuses a coordinate with no provenance |
| `tools/layout/raster_fidelity.py` | **The raster half of the v0 check. Run after every change to the v0 DXF.** Registers mm→px from the **PDF's** hatched wall faces, never from the DXF under test, against a **frozen** ink mask and a committed registration (both hashed). Measures both directions densely: every DXF wall edge → nearest ink, and every wall ink pixel → nearest DXF wall **body**, per hatched solid. Opening spans are excluded using the drawing's own bridged-opening record. Exit 1 on a measured breach, 2 if the evidence or the fit is not the frozen one. Replaced `overlay_dxf_on_raster.py`, which fitted its registration on the DXF it was scoring |
| `scripts/raster_fidelity_selftest.py` | Guards the above: the real export must pass and **7** seeded defects must be rejected — whole-model translation, 3% scale, a 400 mm endpoint drift, a sideways displacement, a malformed triangular entity, a deleted wall, and a tampered frozen mask |
| `tools/layout/check_dxf_closure.py` | **THE closure gate. Run after every v0 export.** Asserts wall identity (present, exactly once, labels and polylines in parity), absolute faces against the placement, drawn length and thickness against the record **and against the PDF's hatched solids** (`vector_extent_oracle.py` — an oracle the exporter does not consume), every ledger corner square solid, no unsanctioned overlap, no unexplained near-miss, no cavity, and a fully validated extent-exception ledger. `--canon <dir>` points it at a seeded copy of `data/canonical`. Exits non-zero on breach |
| `tools/layout/vector_extent_oracle.py` | Re-derives the hatched wall solids from the source PDF at check time, with the PDF's sha256 asserted. Exists because asserting the DXF against `wall_blocks.csv` only proves that two things a person edits together agree — a coupled edit of both passed the gate |
| `scripts/dxf_closure_selftest.py` | Guards the closure gate: the real export must pass and **24** seeded defects must each be rejected — corner voids, an overlap, a deleted wall, partial and whole-model shifts, an along-axis slide, a duplicate wall, a duplicate label entity, an over-extension, a wrong thickness, a widened pinned exception, a malformed non-rectangular entity, a bulged edge, seven that mutate the DXF **and** a canonical table together (including **duplicate keys** in `wall_blocks.csv` and `wall_corners.csv`), and two that leave a committed review artefact reporting a previous round |
| `tools/layout/dxf_wall_entities.py` | **The one reader of wall entities**, shared by both gates. Refuses anything that is not the rectangle the exporter promises — closed, zero-bulge, axis-aligned, four distinct corners, polygon area equal to bounding-box area. Exists because both gates independently reduced a polyline to its bounding box, so a triangle on three of a rectangle's corners passed both |
| `tools/layout/v0_state.py` | Derives the review drawing's "Still open" block from the canonical data and the DXF, and `render_dxf.py` writes it to a sidecar. **`check_dxf_closure.py` fails when the drawing disagrees with the current state**, because a hand-maintained caption went stale twice and the owner reads the caption |
| `scripts/structural_assembly_selftest.py` | Guards the two above by seeding 14 real defects and asserting each is rejected — including the two that used to PASS: G3 restored as owner of `C_G3_R2`, and `C_R1a_R1b` flipped back to a construction joint |
| `tools/layout/check_room_rollout.py` | Checks each room's INTERNAL rollout (развёртка) in `room_rollouts.csv`: the loop must close on both axes, and it reports finishable face area. A face is not a wall — see the header |
| `scripts/tabular_gate_selftest.py` | **Run after touching `room_rollouts.csv`, `bom.csv`, `quotes.csv` or their tools.** Seeds 13 defects and asserts each is rejected — including the one that printed a **`nan–nan BYN` bottom line** and exited 0 |
| `tools/lib/tabular.py` | **The shared strict-CSV and numeric helpers. Use `read_csv()` and `finite()`, not `csv.DictReader` and `float()`.** `DictReader` drops a stray cell and turns a missing one into `None`; `float('nan')` parses and then defeats every comparison it reaches |
| `tools/build_knowledge_base_index.py` | Rebuilds the numeric-claims index |
| `tools/youtube/preflight_playlist.py` | Dedup a playlist/channel against `processed_video_ids.txt` before fetching |
| `tools/youtube/archive_transcripts.py <inbox>` | Archive transcripts and repoint `transcript_file:` frontmatter |
| `tools/pricing/currency_converter.py` | Historical FX. **Never use a spot rate for a historical figure** |

## Standing rules

These are the ones that cause real damage when broken. Everything else is in the skills.

1. **Original language only.** Never fetch or cite auto-translated English captions for a Russian source. Force `--languages ru`. Preserve Russian terms inline in notes and wiki pages — searchability depends on it.
2. **A price is meaningless without location and year.** Never compare two figures until both are resolved. Confirm dates from `yt-dlp` metadata, not from the title.
3. **Attribute every claim to a named practitioner, as opinion.** Nothing in this vault is a flat fact. Name the person or company inline, per claim — not just in a Source Notes block at the bottom.
4. **`16_Legal_and_Regulations/` is Belarus-only.** A Russian-sourced regulatory claim never goes there, not even hedged. Route it to the relevant technical page with the jurisdiction flagged.
5. **Value-filter before batch processing.** For any playlist or channel, title-skim and spot-check transcripts first. Do not process everything by default.
6. **Route to wiki pages in the same turn as extraction** (intake step 5a). Batching it up for later has caught real errors precisely because it was done late — don't rely on that.
7. **Serialize YouTube fetches**, one at a time with spacing and bounded backoff. A rate-limit can be IP-wide across all channels — pause, don't rotate channels into the same wall.
8. **Pages are sized by judgment and organised by topic, not by intake date.** **~300 lines is a soft target, not a limit** — a coherent page at 310 lines is fine, and `tools/check_page_sizes.py` only fails at a **400-line backstop**, which a reviewed exception can waive. **The defect that matters is fragmentation, and you diagnose it by reading the headings**: topic headings mean the page is fine at any reasonable length; headings like "… (added 2026-09-01, Round 4)" mean the page is organised by when facts arrived. Fragmented → `tools/split_page.py merge` (demotes dated headings to `###`, keeping every attribution). Genuinely several topics → `apply`. **Both → merge first, then extract.** **Before adding a heading, look for an existing section the fact belongs under** — that is what prevents all of this. See `00_Master/wiki_page_format.md`.
9. **Reading a dimension is a procedure, not a glance.** Before using any figure off a drawing or a photo: identify the **two elements its extension lines terminate on**; ask what the object could **plausibly** be, because a dimension that contradicts function is wrong even when the pixels agree; check that your **scale is independent** of the thing you are measuring; and prefer **chain closure** over judgement wherever a whole is known. Full checklist and the seven real failures behind it: `00_Master/Evidence_Reading_Discipline.md`. **Areas are never evidence.**
10. **Writing a check is a procedure, and "done" differs by the kind of work.** Before writing any validator, read `00_Master/Validator_Design_Discipline.md`. It carries the failure classes that actually recurred across eleven adversarial review rounds — **a collection that deduplicates destroys the defect being checked (4x)**, **printing is not checking (3x)**, an accidental rejection is not a check, a seed that cannot fail is worse than no seed, an input a fixture cannot mutate reads as covered, and a checker must not share an editable measurement with the thing it checks. It also states what **done** means per work type: deliverable work changes a file under `data/canonical/` or `data/cad/`; apparatus work adds a permanent seed you have watched fail; a review either reproduces a finding or records that it found none. **A gate nobody has watched fail is not a gate**, and apparatus work is legitimate without being progress on the deliverable — track the two separately.
11. **A role is a claim, so it needs someone to have looked.** In `_Precedents/`, a file lands `examined: no` / `role: unexamined`, and **a layout case may not cite an unexamined file** — `tools/precedents/validate_precedents.py` enforces both. This exists because an unfurnished plan was filed as the developer handover state when it is the **after** state of a demolition. A confident label on an unlooked-at file is worse than no label.
12. **Merge to main every time.** After commit and push on a branch: merge `--no-ff` into main, push main, delete the branch locally and remotely. No lingering branches, no PRs.

## Conventions

- Page shape: see `00_Master/wiki_page_format.md`. Compact guide page + `analysis/` detail pages, with Perspectives / Common Ground / Your Priority blocks for genuine source disagreements.
- Pages fail in **two** directions: too long, and **fragmented** (many stub sections from each batch appending its own dated heading). The fix for the second is merging. Look for an existing section before adding a heading.
- USD equivalents are rounded comparability aids: nearest 10 below $1,000, nearest 100 to $99,999, nearest 1,000 above. Never show cents. A figure that is exact by construction is tagged `arithmetic-exact` and keeps its precision.
- Areas: developer plans are clear/net, БТИ are gross. **Areas are not evidence** — see the standing rule in `data/canonical/wall_materials.json`. **Dimensions nominal ±50 mm**, measured not assumed: see `00_Master/Geometry_Variance_Study.md`, which compares the developer plan against three surveyed flats of the same layout and finds deltas from −45 to +30 mm. The old ±25 had no evidence behind it. This is the BUILD tolerance, not the raster tolerance in `tools/layout/check_wall_junctions.py`.

## Cross-repo

`.agents/ai-management-link.md` explains how this repo connects to the sibling `ai-*` repos — shared skills, telemetry, and the cross-agent plan dialogue in `ai-management`.
