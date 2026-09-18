---
source_id: YT_render_and_aec_cluster_20260918
title: "Render-engine and AEC-landscape cluster — triage record"
channel: "multiple"
url: https://www.youtube.com/watch?v=6iHgqkmYXmc
video_ids: [6iHgqkmYXmc, V0Q3E_63TP4, Ufw8RQb7Pj4, dturff3XgSk, dSEHWnedxIM, wGS0xp-XBqw, Enggo_nqDHs, uDvzYI5jpDk]
upload_date: 2026-07-15
language: en
region: not_region_specific
processed: 2026-09-18
transcript_file: _Archive/processed_sources/6iHgqkmYXmc.en.txt
---

# The render-engine batch — what was extracted, and what was triaged out

**The three render sources that matter are extracted into `18_Digital_Toolchain/analysis/Realtime_Walkthrough_EEVEE.md`** — the recipe, the screen-space limitation and the Blender 5.2 changes. This note records the triage and the two remaining sources.

## ⚠️ Triaged out, with reasons

| id | title | uploaded | why not processed |
| :--- | :--- | :--- | :--- |
| `wGS0xp-XBqw` | How to make EEVEE Next look like Cycles | 2024-09-21 | **superseded** by `V0Q3E_63TP4` (2026-01), same technique on Blender 5 |
| `Enggo_nqDHs` | Eevee vs Eevee NEXT vs Cycles | **2024-03-01** | ⚠️ **predates EEVEE Next shipping** — it went stable in Blender 4.2, July 2024. A March 2024 comparison is of a preview build |
| `uDvzYI5jpDk` | The Ultimate Render Engine Comparison for Architects | **2023-12-15** | ⚠️ **predates EEVEE Next entirely.** Same reasoning that triaged out the 2021–22 Blender-vs-SketchUp videos |

**Three batches running, the same filter has now removed six sources for being older than the thing they describe.** That is worth noting as a pattern: tooling content ages faster than practice content, and this vault's date discipline applies to both.

## `dturff3XgSk` — The Rise of BIM 2.0 (ArchiTech Network, 2025-08-01)

Context rather than technique, and the context is useful.

- **The trajectory**: CAD (2D lines) → BIM (model, with plans/sections/elevations *generated* from it) → "BIM 2.0".
- ⚠️ **Why a new wave exists at all**: *"Revit was cutting edge at the time, but after Autodesk acquired it, the innovation seemed to really slow… Revit is still the dominant BIM tool, but the pace of development has lagged whilst subscription costs keep rising significantly."* By 2020 major firms published open letters demanding progress.
- **Fragmentation is the other driver**: *"Even as architects we jump between Rhino, Revit, Enscape, Grasshopper, Ladybug"*, against product-design industries that work in one integrated platform.
- Nine startups presented, ranging from full-stack BIM platforms to point solutions — floor-plan layout optimisation, early feasibility.

> **⚠️ What it means here.** This project's output is **IFC**, an open format neither owned nor versioned by a vendor. The video describes an industry actively trying to escape a dominant tool whose development slowed and whose subscription rose. **That is the risk an open, file-based, gated pipeline was already hedging**, and it is the second independent reason recorded for the same decision — the first being that a generated artefact can be checked.

## `dSEHWnedxIM` — AI in Construction: The Complete Applied Guide (Tim Fairley, 2026-02-21)

**3 hours 16 minutes. Fetched, archived, NOT fully extracted — a value-filter decision under standing rule 5.**

Sampling establishes it is a **business-process course** for construction *businesses*: AI fundamentals, prompting, and automating recurring office work. Its own worked example is *"every week or month you have to send a report to your client… compiling that report would probably save you a fair bit of time."*

Its automation rule is sound and is the one durable thing sampled:

> **Automate tasks that are recurrent, predictable and repeatable, and time-consuming in aggregate** — not one-offs, because *"you have to set them up… it's not really saving you any time."*

⚠️ **It is aimed at running a construction business, not at modelling one apartment.** The transcript is archived so a later pass can mine it if this project ever acquires a contractor-management dimension; today it does not.

## Source Notes

- No prices in any source in this cluster. None region-specific.
- `dturff3XgSk` is moderately promotional for the channel's events; the nine startups are named as presenters, not endorsed.
