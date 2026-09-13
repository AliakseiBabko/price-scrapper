---
source_type: video transcript (Russian BIM channel, practitioner testing four Revit tasks from simple to complex)
source_url: https://www.youtube.com/watch?v=JCCEW6797yw
video_id: JCCEW6797yw
transcript_file: _Archive/processed_sources/20260913_bimdlyachaynikov_revit_dynamo_families_audit_0a072a04.txt
fetched: 2026-09-13 via youtube-transcript-api (ru auto captions — ORIGINAL language)
upload_date: 2026-09-12 (confirmed via yt-dlp metadata)
channel: BIM для чайников
source_title: "Chat GPT 6 Astra + Revit | #2"
language: ru
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 9
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — BIM для чайников: Where the Complexity Cliff Actually Sits in Revit (YouTube JCCEW6797yw)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Why this source is better than its class

**A working BIM practitioner testing four real Revit tasks deliberately ordered от простого к сложному — simple to complex — and reporting the failures as plainly as the successes.** `promotional_ratio: low`; nothing is sold, and she asks viewers to report their own results.

**⚠️ It is a capability test, so model names and verdicts are not routed** per the standing dating rule. **What is routed is WHERE THE FAILURES FALL**, which is a property of the task shape rather than of the model generation.

## ⚠️ Task 1 — a Dynamo script, and geometry that is PLACED but not ASSOCIATED

**Asked for a Dynamo script with nodes and an explanation of why each node**, to place beams on a grid: take a family from a named project, **main beams along the numeric axes, secondary along the lettered axes**, and fill mark `B1`.

- **It delivered — *«не с первой итерации»*, not on the first iteration** — producing a **Python Script node wired into Dynamo**, with the inputs exposed: family name, main beam type, secondary type, level name, mark to fill, offset, **and a `true` at the end to make it run.**
- **It worked**: main beams on the numeric grid, secondary on the lettered, marks `30Б1` and `20Б1` applied.
- **⚠️⚠️ And the limitation she names is the important one: *«если я его смещу, например, балки останутся на месте»* — MOVE THE GRID AND THE BEAMS STAY WHERE THEY ARE.** They are placed, not constrained to it. She notes the script could be extended to lock them.

> **⚠️⚠️ → GENERATED GEOMETRY IS PLACED, NOT ASSOCIATED. The parametric RELATIONSHIP is absent unless it is explicitly demanded.**
>
> **This is the same failure family as the dimension-text override in [[_Sources/YT_-FsHQEYldnQ_grasshopperpp_computer_use_autocad|-FsHQEYldnQ]]** — a drawing whose dimension text disagrees with its geometry. **In both cases the output LOOKS correct and the underlying relationship that would keep it correct is missing.** Two different tools, two different relationship types, same defect class. **→ When accepting generated geometry, the question is not "is it right?" but "is it right BECAUSE OF anything?"**

## ⚠️ Task 2 — re-saving a finished family: failed outright

Asked to re-save a completed family: **no such capability.** It exports a **JSON** and analyses parameters and geometry from it, but **cannot write the family back.** *«Пока я пробовал, ничего не получилось.»*

- **→ The JSON bridge is effectively read-only. It can inspect a model and it cannot author back into the native format** — consistent with the file-generator boundary already recorded across this folder.

## ⚠️⚠️ Task 3 — a model audit from exported JSON, WITH ELEMENT IDs

**The most promising result in the source.** She opens a real project and asks it to *«проанализируй открытую модель Ревит как BIM-координатор»* — find problems with **worksets, clashes, DWG files and parameters; list them and rate criticality.**

- **It exports JSON, analyses it, and produces a report** — asked for PDF, it returned **39 pages on the first iteration**: priorities, rationale, a **clash register**, worksets, duplicates.
- **⚠️⚠️ And critically, findings carry ELEMENT IDs** — *«прямо с айдишками… пересечение, перекрытие, перекрытие и два ID»* — each clash named with the two IDs involved.
- Named finding categories include ***«арматура вне основы»*** (rebar outside its host) and ***«у элементов марка повторяется»*** (duplicate element marks).
- **Her verdict: *«если это прямо допилить… то это можно в какой-то такой неплохой отчёт и собрать»*** — with real work it could be assembled into a decent report.

> **⚠️⚠️ → This is the CHECKING direction rather than the authoring direction, and it is where the technology looks strongest in this whole batch.** Two reasons it is more trustworthy than the modelling demos: **it reads the EXPORTED STRUCTURED DATA rather than the viewport** — consistent with everything this folder records about text beating pixels — **and every finding is TRACEABLE TO AN ELEMENT ID**, so a human can go and check it. **A finding you can jump to is a flag; a finding you cannot is an opinion.**

## ⚠️⚠️ Task 4 — the complexity cliff, located precisely

**Asked for a steel plate family** (Revit 25, generic model category) with parameters, **four holes**, a material, its own reference planes, and dimensions driven by parameters.

| Attempt | Result |
| :--- | :--- |
| Plate **with 4 parametric holes** | **Failed** — *«зависимости не выполняются»*, constraints not satisfied |
| Corrected version, same task | **Failed again, with MORE warnings than before** |
| **Plate WITHOUT holes** | **⚠️ Succeeded** — a real family with length, width, thickness and material, **and it set the material to steel by itself** |

- **⚠️ And she VERIFIES, which is rare in this source class: *«давайте проверим, насколько параметр рабочие. Рабочие. Этот работает. Этот и этот работает.»*** — she drives each parameter and confirms the geometry responds. *«Я в шоке.»*
- **Her reading: simple geometry yes; more complex probably yes but not in one iteration**, and feeding it the office's parameter-naming standard (ФОП) would let it pull the right parameters in.

> **⚠️⚠️ → THE FAILURE BOUNDARY IS LOCATED, AND IT IS NARROW: a parametric primitive succeeds; a parametric primitive WITH FEATURES fails, twice, and the second attempt was worse than the first.** **The cliff is not between "simple" and "complex" in any vague sense — it is at the point where constraints must be solved against each other.** ⚠️ **And "the corrected version produced more warnings" is worth keeping on its own: iteration did not converge.**

## Confidence & Evidence Notes

- **`single-account`**, one practitioner, one session, and she says openly it is *«краткий обзор буквально на коленке»* — a quick review done on her knee. **Usage limits ran out repeatedly and shaped what could be attempted.**
- **⚠️ Model names and capability verdicts deliberately NOT routed.** **What is routed is the placed-not-associated defect, the read-only JSON boundary, the ID-traceable audit pattern, and the located complexity cliff** — all properties of task shape rather than of a model version.
- **ASR**: adequate. Observed: «GPT6 ASR» for the model name, «Jon» for JSON, «скрип»/«скрипт», «Dour» for a project name, «осмещение» for смещение, «ФОП» heard once.
- **No prices; no conversion owed. No regulatory content** — nothing here is a jurisdictional claim.

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Agent_Connected_CAD.md`** — geometry placed but not associated; the located complexity cliff; the read-only JSON boundary.
- **`18_Digital_Toolchain/analysis/AI_Workflow_Systems.md`** — the ID-traceable model audit as the checking direction, and why exported structured data beats the viewport.
- **5b**: no prices; no conversion owed.
