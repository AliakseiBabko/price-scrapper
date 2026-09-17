# Agent brief — round 2: a NARROW re-triage of nine wrongly-skipped videos

**For Antigravity. 2026-09-17, after reviewing round 1.** Read `AGENTS.md` and `.agents/skills/renovation-knowledge-intake/SKILL.md` first.

**Round 1 was good work.** The 292-video accounting reconciles, the gates pass, the routing carries real citations, and the negative result in §2 — that MEP and services are a **total void** across every source — is the most useful thing in it. Nothing below contradicts that.

**This is a narrow corrective pass over NINE named videos.** It is not a new sweep. Do not look at anything outside the list.

---

## 1. The defect in round 1's filter, stated precisely

⚠️ **Skip rationales were assigned by TITLE KEYWORD, not by ranking against the 12 open problems the brief asked for.** A small set of boilerplate reasons was applied across whole channels, and several landed on videos they do not describe.

**The clearest evidence.** *"Interactive manual geometry clicking; redundant with 6 existing floor plan sources in vault"* was used to skip **all** of these:

| Id | Title | Why that rationale is wrong |
| :--- | :--- | :--- |
| `kEFgXvcbHEw` | Stop Using Default Walls: **Create Custom IFC Types** for Bonsai BIM | Not a floor plan. IFC typing |
| `0ktp-S7Lev0` | Your Bonsai Doors & Windows Are Broken Without This — **How to Manage Voids** | Not a floor plan. Opening/void semantics |
| `oQBCy_zKMtI` | **modify your wall opening** with Bonsai (IFC native) | Not a floor plan |
| `iIR3zl4b6vA` | **how to add wall openings** in IFC models using Bonsai (IFC native) | Not a floor plan |
| `xImmD0Ns4NQ` | **Create Window Schedule** With Bonsai BIM from IFC | Not a floor plan. Schedules = open problem 11 |
| `Vy4RBlXFNQE` | **Door Schedule from IFC** with Bonsai BIM | Same |
| `dRSoT80oDNA` | Blender Has **Parametric Walls** Now: Create & Edit with Bonsai BIM | Not a floor plan |

And separately:

| Id | Title | Round 1 rationale | Why it is wrong |
| :--- | :--- | :--- | :--- |
| `RL3IAGeMi5s` | Bonsai BIM live: **new 2D drawing tools**, Revit questions, **how drawings work under the hood** | *"Proprietary Revit workflow"* | The subject is **Bonsai's own 2D drawing internals**. "Revit" appears in the title as audience Q&A. **Open problem 7 came back NOT COVERED** — and this is the one video in 292 whose title claims to address it. It is also the video the owner linked by hand |
| `415peYvhkcg` | **Avoid These Mistakes** When Using Bonsai with Blender 4.5 | *"Software release announcement / news"* | A mistakes-and-pitfalls video is exactly the practitioner-stated-limits material §3 of your own report is built from |

> **⚠️ THE RULE THAT PREVENTS THIS RECURRING: a skip rationale must name WHICH of the 12 open problems the video fails to serve.** *"Redundant with floor plan sources"* is not one of the twelve. If a rationale cannot be written in those terms, the video has not been triaged — it has been categorised by topic.

---

## 2. Two facts from our own code that change the ranking

I checked the generator while reviewing your report. Both of these make videos you skipped more valuable than they looked:

1. **⚠️ Our IFC generator emits NO TYPES AT ALL** — no `IfcWallType`, `IfcDoorType`, `IfcWindowType`. It creates concrete instances only (`tools/ifc/model_from_resolved.py`). **Bonsai's Spreadsheet QTO groups and sums BY TYPE**, which you documented yourself in `YT_fUlDzxSDOls`. So as things stand **we could not produce a door or window schedule from our own model.** That makes `kEFgXvcbHEw`, `xImmD0Ns4NQ` and `Vy4RBlXFNQE` directly load-bearing.
2. **Our generator writes IFC4** and, thanks to your `XYeasHbyw-U` note, will stay there. Treat anything 4.3-specific as out of scope rather than aspirational.

---

## 3. The nine videos, and the SPECIFIC question each must answer

Process only these. **Answer the question, do not summarise the video.**

| # | Id | The question we need answered |
| :--: | :--- | :--- |
| 1 | `kEFgXvcbHEw` | How is a custom `IfcWallType` (or door/window type) **defined and attached**? What does a type carry — material layer set, thickness, Psets? What breaks in a model that has instances but **no types**? |
| 2 | `xImmD0Ns4NQ` | What does a window schedule **require of the model** to work at all? Types? Psets? `Tag`? |
| 3 | `Vy4RBlXFNQE` | Same for doors. **If 2 and 3 answer the same question, say so and process only one.** |
| 4 | `0ktp-S7Lev0` | What is the failure it names, in IFC terms — `IfcOpeningElement`, `IfcRelVoidsElement`, `IfcRelFillsElement`? We generate voids and fills ourselves; **what do practitioners get wrong that a generator would also get wrong?** |
| 5 | `oQBCy_zKMtI` | Editing an existing opening IFC-natively: what is preserved, what is rebuilt? |
| 6 | `iIR3zl4b6vA` | Adding an opening IFC-natively. **If 4–6 overlap heavily, process the strongest and skip the rest with a reason** |
| 7 | `RL3IAGeMi5s` | ⚠️ **The priority of the nine.** How do Bonsai drawings work *under the hood* — what generates a 2D sheet from the model, what is stored in the IFC vs computed at draw time, and **is there any route to a per-discipline (electrical/plumbing) sheet rather than an architectural plan?** Open problem 7 rests on this |
| 8 | `415peYvhkcg` | Which mistakes? **Only the ones that would also afflict a GENERATED model** — ignore UI ergonomics |
| 9 | `dRSoT80oDNA` | What makes a Bonsai wall "parametric", and is that a TYPE, a Pset, or an add-on convention? Does it survive a round-trip through plain IFC4? |

**Optional tenth, your judgement:** `Vd6qnRO0ZP4` (*Select & Copy Multiple Global IDs Correctly*) — round 1 filed it under IDS, but `GlobalId` stability matters to us because our identity rule derives the IFC GUID from a minted UUID. Take it **only** if it says something about GlobalId persistence across edits.

---

## 4. What to produce

1. **A verdict for every one of the nine**, even where you process nothing:
   - **PROCESSED** — with the extraction note; or
   - **SKIP CONFIRMED** — *"the round 1 skip was right, for this better reason: …"*, naming **which of the 12 problems it fails to serve**.
   - ⚠️ **"Skip confirmed" is a correct and welcome answer.** Do not process a video to be seen to comply. Over-correcting a filter is the same error in the other direction.
2. **Extraction notes + same-turn routing** for anything processed, as in round 1.
3. **⚠️ CORRECT THE ROUND 1 REPORT.** In `_Inbox/planning/bonsai_blender_triage_20260917.md`, amend the skip rationales for these nine so the record is not misleading, and add a short note at the top saying the filter was applied by topic rather than by open problem. **Do not delete the original rationales — show them as superseded.** A triage report whose reasoning is wrong is worse than one with a gap, because the gap is visible.
4. **Update the §1 verdict table** for any open problem whose status changes — particularly **7 (2D discipline sheets)** and **11 (QTO)**.
5. **If `kEFgXvcbHEw` establishes what a type must carry, say plainly what our generator would have to emit.** Name the entities. Do not design it — that is ours — but do not leave it as "types are important" either.

---

## 5. Constraints

- ⚠️ **Do not change `tools/`, `data/canonical/`, or anything under `_Inbox/migration/`.** The services migration is mid-flight and under adversarial review.
- ⚠️ **Do not re-open the wider skip list.** Nine videos, plus one optional.
- **Wall-corner and edge-intersection videos stay skipped, and that call was right** — `MiY8oPp7E94` (Shear Tool corners), `quMG0HGeY74` (edge intersections), `th7fyP_fZ08` (snap tools). Our junction problem is not geometric technique, it is **corner OWNERSHIP**, settled by `data/canonical/wall_corners.csv` and gated by `tools/layout/check_wall_junctions.py`. Mesh-editing tricks do not transfer. Say so in the report so the question is closed rather than re-asked.
- Rules 1, 2, 3, 6, 7 as before: original language, dates actually confirmed via `yt-dlp`, every claim attributed to the named practitioner as opinion, routing in the same turn, serialized fetches.
- Gates before commit: `tools/verify_batch.py --base <ref>`, `tools/check_page_sizes.py`. Then rule 12: merge `--no-ff` to main, delete the branch local and remote.
