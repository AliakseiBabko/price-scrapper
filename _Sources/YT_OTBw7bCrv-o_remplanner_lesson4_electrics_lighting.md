---
source_type: video transcript (software tutorial — lesson 4 of a 13-lesson vendor course; processed as a DRAWING-CONVENTION SPECIFICATION, not as a tutorial)
source_url: https://www.youtube.com/watch?v=OTBw7bCrv-o
video_id: OTBw7bCrv-o
transcript_file: _Archive/processed_sources/20260908_remplanner_lesson4_electrics_lighting_9093ffa9.txt
fetched: 2026-09-08 (anonymous, yt-dlp --write-auto-subs --sub-langs ru-orig)
upload_date: 2025-06-24 (confirmed via yt-dlp metadata)
duration: 18:09
channel: RemPlanner — vendor channel for the RemPlanner online renovation-planning tool; narrator not named in this lesson
source_metadata_location: not applicable (a tool's own conventions, not a project)
jurisdiction: n/a — no regulatory claims made
language: ru (ru-orig auto-generated)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 7
promotional_ratio: medium (a vendor's own product course — but it sells nothing beyond the tool, and the conventions it states are checkable on their own merits)
corroborates_existing: false
---

# Extraction Note — RemPlanner: "Видеоуроки Remplanner. Урок 4. Электрика и освещение" (YouTube OTBw7bCrv-o)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

**A vendor's own product tutorial, and it must be read as one.** Standing rule 3 still applies but has no named practitioner to attach to: **the claims below are attributable to RemPlanner the product, as design decisions its authors made, not to a practitioner's experience.** They carry weight only because each is stated *with the reason it exists*, usually in terms of what a builder needs — and those reasons are checkable independently of the tool.

> [!WARNING]
> **⚠️ Honest assessment of density: roughly 70% of this transcript is mouse mechanics** — «наведите курсор», «левым кликом», «зажатой левой кнопкой мыши» — **and is worthless to this project.** It is extracted anyway because the remaining ~30% is drawing convention on questions this project has open (`cap3` setting-out dimensions, and the datum change flagged in `_Inbox/planning/toolchain_gap_analysis_20260908.md` §E). **Do not expect a normal fact yield from this format; expect a few structurally heavy items.** ASR is comparatively clean here, the narration being scripted.

## Value-filter verdict

**Partial extraction — conventions only.** UI mechanics deliberately discarded. The one tool-mechanics item retained below is kept for what it implies about the data model, not for how to click it.

## Quantities / Measurements — ⚠️⚠️ dimensioning conventions, with the reasons stated

- **Dimensions run to the CENTRE of a device or fixture, never to its edge.** Stated for sockets — *«сами размеры по-прежнему указывают именно на центр розетки, а не на её край»* — and again for luminaires, with the rationale: *«размеры всех светильников показывают расстояние до их центра, а не до края предмета, что позволяет строителям правильно рассчитать выводы проводов»*.
  - **→ The reason is that the builder is setting out a cable stub-out, and the stub-out is at the centre.** Bears directly on `cap3`, and on §E's datum decision, which the gap analysis says must be made **before** `cap3` emits dimensions rather than retrofitted.
- ⚠️⚠️ **A centred fixture is dimensioned as `1/2`, not in millimetres.** Where a chandelier is to sit exactly at a room's centre, the tool prints the value `1/2` in place of numeric dimensions, *«указывая строителям на то, что светильник должен быть смонтирован ровно по центру комнаты, независимо от любого расхождения в размерах»*. **Rectangular rooms only** — the mechanic is stated not to work otherwise.
  - **→ A RELATIVE dimension that survives as-built variance where an absolute figure does not.** This is the single most valuable item in the source, and it addresses a problem this project has measured rather than assumed: `00_Master/Geometry_Variance_Study.md` found **−45 to +30 mm** deltas across three surveyed flats of this very layout against the developer's plan. **An absolute millimetre dimension to a centred fixture is wrong on site by construction; `1/2` cannot be.**
  - ⚠️ **Open question, recorded in the triage: whether our own DXF/SVG pipeline can express a proportional dimension at all, or whether it needs Bonsai's annotation subsystem.** Untested.
- **Sockets that are not on a wall — floor and ceiling sockets — carry TWO mounting dimensions, to the nearest walls, and still to the centre.** A dimensioning rule for free-standing points.
- **Height tags may be moved independently of the element** to stop them colliding with other dimensions. **A recognition that annotation placement is a separate concern from element position** — which is precisely the failure mode the research report named for hand-rolled sheet generation (*«dimension chains collide on dense MEP plans»*).

## Switches / Sockets / Cables — ⚠️ an element type our model does not have

- **«Вывод провода» is a distinct element from a socket**: a cable brought out of the wall where a load connects directly, with no socket. **The cases named: all kinds of подсветка, wall luminaires, and appliances that have no plug of their own — air conditioners, ovens.**
  - **→ A taxonomy gap.** A вывод is not a розетка: it is installed differently, priced differently, and cannot be counted in the same line. Our model's electrical elements do not distinguish it, and the BOM needs it as its own `resource_role`.
  - **Independently corroborated by practice, not just by the tool**: `YT_F0rXrbPDPf4` and `YT_DI5GAV64mnU` both use выводы specifically for towel rails, mirror lighting, concealed lighting and air conditioners — exactly the cases listed here.
- **A socket group can carry a `vertical` status which changes how it is drawn on the развёртки and in 3D, while leaving the plan unchanged** — *«на чертежах при этом ничего не изменится. Однако на развёртках стен и в режиме 3D визуализации такая группа будет расположена вертикально»*.
  - ⚠️ **→ An element property whose rendering differs per sheet type.** A data-model insight for our own sheet pipeline: representation is a function of (element, sheet), not of element alone.
- **Up to three electrical points may be stacked in one vertical plane at different heights**, and single sockets and groups can be positioned to **1 mm precision** via keyboard in millimetre mode. ⚠️ The 1 mm figure is a tool capability, **not a tolerance claim** — do not read it as a buildable precision.
- **Sockets, switches and thermostats can be combined in one group under a common frame**, and groups move only along the wall they are mounted on.
- **Grouping is creation-order dependent**: two already-placed single sockets will not merge when moved together; one must be deleted and re-placed. Retained for one reason only — ⚠️ **it shows grouping is a modelled RELATION between elements, not a derived consequence of proximity.** If our model ever needs socket groups (it will, for the frames on a sheet), the relation has to be stored, not computed.

## Lighting

- **Luminaire placement behaves like furniture placement** in the tool's own framing, with additions: rotation for asymmetric fittings, a **height-above-floor parameter for wall luminaires**, per-element hiding of mounting dimensions, and free-text comments attachable to an individual fitting.
  - **The per-element comment matches practice**: `YT_F0rXrbPDPf4` says he annotates each socket with what it is for. **So a per-element note is a required field of a services plan, not a nicety.**

## Design Concept — sheet-level visibility control

- **Each services sheet carries its own visibility settings** — furniture can be shown on the socket plan, and all height tags can be hidden if not wanted. **Corroborates `YT_DI5GAV64mnU`'s practice of reading the socket plan with the furniture layer overlaid, and `YT_F0rXrbPDPf4`'s of switching furniture off for the issued version.** Three independent statements that **a services sheet has two audiences and therefore two configurations** — the reviewer, who needs furniture, and the installer, who does not.

## Unclear / Needs Confirmation

- Whether the `1/2` notation is a RemPlanner invention or reflects an established Russian drafting convention. **Not stated, and worth finding out before adopting it** — if it is conventional, a Belarusian installer will read it; if it is a vendor's own, they may not. **This is the highest-value open question in Round 1.**
- The narrator is not named, so nothing here can be attributed to a person.
- No claim in this source is about the physical world, so none of it corroborates or contradicts any existing technical page. It is entirely about representation.
