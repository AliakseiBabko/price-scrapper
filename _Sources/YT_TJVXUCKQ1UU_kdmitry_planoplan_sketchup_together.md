---
source_type: video transcript (designer's client-facing progress report — why two modelling tools are used together and what each is for)
source_url: https://www.youtube.com/watch?v=TJVXUCKQ1UU
video_id: TJVXUCKQ1UU
transcript_file: _Archive/processed_sources/20260908_kdmitry_planoplan_sketchup_together_33aeb300.txt
fetched: 2026-09-08 (anonymous, yt-dlp --write-auto-subs --sub-langs ru-orig)
upload_date: 2026-02-04 (confirmed via yt-dlp metadata)
duration: 5:31
channel: "Дизайнер Дмитрий К" (@k_dmitry, 372 subscribers) — practising interior designer, Moscow
jurisdiction: Russia — standing rule 4 applies
language: ru (ru-orig auto-generated)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 9
promotional_ratio: low
corroborates_existing: false
---

# Extraction Note — Дизайнер Дмитрий К: "Как использовать Планоплан и SketchUp вместе для дизайна квартиры" (YouTube TJVXUCKQ1UU)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

5½ minutes, 788 words, and **the highest facts-per-minute of anything in Round 1.** A progress report on the same «Кожуховская» flat as `YT_FRKr9X3AFfY`. Promotional ratio low; he names both tools' weaknesses as readily as their strengths.

**⚠️ ASR note, and it produced a correction**: this transcript renders the client's exercise machine as **«гребной тренажёр» (a ROWING machine)**, where `YT_YEpfNcwwGoU` rendered the same object as «грибной тренажёр» (nonsense — "mushroom"). **The correct term is гребной, and this note is the reason the other note carries the flag.** Recorded per the vault's practice of correcting a garbled technical term *with* the flag rather than silently.

## Value-filter verdict

**Full extraction.** Short, but it states a division-of-labour principle that bears directly on this project's own toolchain question.

## Design Concept — ⚠️⚠️ accuracy and content-speed separated into two tools, joined by a raster underlay

**The mechanism, which is the whole source:**

1. **SketchUp is the accuracy tool.** *«SketchUp позволяет создавать по обмерному размеру наиболее точную модель»* — the model is built from survey dimensions.
2. **From that model he exports the plan as a flat image and uses it as a подложка (underlay) in Планоплан.**
3. **Планоплан is the concept-speed tool, and its value is stated as being purely its catalogue** — ready-made furniture, textures and materials, *«всё под рукой»* — so that concept variants come out fast and *«тем самым быстрее принять принципиальное решение по дизайну»*.
4. **Precise rework, if needed, goes back to SketchUp.**

- ⚠️ **The rationale for the underlay is the load-bearing part**: *«с нуля начертить точную модель в планоплане очень сложно, ну, почти нереально. А вот по хорошей качественной подложке в размерах можно сделать хорошую, точную модель»*. **The underlay exists because the fast tool cannot be accurate on its own — accuracy is imported, not authored, in the tool where the content lives.**
- **He rebuilds the same model twice on purpose and says the time is worth it** — *«стоит немножечко потратить времени, чтобы воссоздать модель Планоплана… она у меня абсолютно идентична со скетчаповской»* — and he keeps a good model library in SketchUp too, so the duplication is not for want of assets.

## Quantities / Measurements — a third-party tolerance figure

- ⚠️ **He states his working tolerance as ±1–2 cm against his on-site measurements**: *«тут у меня с допуском плюс-минус 1–2 см всё соответствует тем размерам, которые я замерял на объекте»*.
  - **This must not be merged with this project's own tolerance.** Ours is **nominal ±50 mm** (`00_Master/project_decisions.md`) and `Geometry_Variance_Study.md` measured **−45 to +30 mm** across three surveyed comparables. His ±10–20 mm is *tighter*, and the reason is that **he is modelling a flat that exists and that he has measured, whereas this flat is not built yet** (`tools/cad/PROVISIONAL_MODEL_POLICY.md`: *"the current model is a planning baseline, not an as-built survey"*). **Different datum, different meaning — record the comparison, do not adopt the figure.**

## Design Concept — ⚠️ what a planning model must be accurate ABOUT

**The clearest statement in Round 1 of what fidelity a planning model actually needs, and it is not visual fidelity.**

- **What must be hand-modelled rather than taken from a catalogue: anything absent from the catalogue AND size-critical.** His three examples are all objects that are **real and already owned**, not chosen: the client's **rowing machine** (found as a third-party 3D model, imported to SketchUp, materials assigned and grouped, then exported into Планоплан), the client's **existing dishwasher migrating from the old flat** (modelled by hand), and an **existing door that stays** (modelled by hand, *«чётко по форме, по размеру»*).
- ⚠️⚠️ **The rule, with its reason**: *«только каталожных моделей или какого-нибудь кубика вместо тренажёра — это будет некрасиво, ненаглядно. Поэтому мне нужна настоящая модель тренажёра.»* And the tolerance he will accept: *«пускай он, может быть, чуть-чуть отличается от того, который стоит в квартире, но по размерам, по габаритам он практически идеально точный»*.
  - **→ Dimensional accuracy is required; visual identity is not. A placeholder box defeats the model's purpose, because the purpose is legibility (наглядность), not inventory.**
  - **This is the same insight the gap analysis reached from the cost direction** — *"the model's job is not to be dimensionally exact; it is to hold quantities stable enough that a substitution re-prices correctly"* — arrived at independently, from legibility rather than cost. **Two different arguments converging on "get the size right, leave the identity swappable" is worth more than either alone.**

## Family Requirements / Preferences

- **Objects migrating from the old flat are modelled at real size and placed before the layout is agreed** — the existing dishwasher and the rowing machine both shape the plan. **A `cap6` input this vault has no equivalent of: an inventory of what the household already owns and is keeping, with real dimensions.**
- **A bulky item can drive a whole room's clearance**: the rowing machine *«занимает много места… обязан его учитывать»* and (per `YT_YEpfNcwwGoU`) needs open floor mid-room to be unfolded and used.

## Mistakes / Warnings

- **Sequencing he states for the next step**: furnish every room completely *before* seeking approval of the planning decision, *«и, может быть, даже не в одном варианте»*. Corroborated more strongly in `YT_FRKr9X3AFfY`, which states the principle outright.

## Unclear / Needs Confirmation

- He does not say how the SketchUp→Планоплан object export is done, nor whether scale survives it — only that it is done.
- Whether the exported plan raster carries a scale reference, or whether scale is re-established by hand in Планоплан. **Relevant to us, because standing rule 9 requires a scale independent of the thing being measured**, and a plan exported without one would fail that.
