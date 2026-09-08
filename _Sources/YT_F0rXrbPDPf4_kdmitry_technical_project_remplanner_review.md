---
source_type: video transcript (designer's client-facing progress report — full tab-by-tab walkthrough of a technical design package, incl. lighting and switch grouping)
source_url: https://www.youtube.com/watch?v=F0rXrbPDPf4
video_id: F0rXrbPDPf4
transcript_file: _Archive/processed_sources/20260908_kdmitry_technical_project_remplanner_review_ad202a1d.txt
fetched: 2026-09-08 (anonymous, yt-dlp --write-auto-subs --sub-langs ru-orig)
upload_date: 2025-03-19 (confirmed via yt-dlp metadata)
duration: 18:13
channel: "Дизайнер Дмитрий К" (@k_dmitry, 372 subscribers) — practising interior designer, Moscow
source_metadata_location: Moscow (flat not further identified in this video)
jurisdiction: Russia — standing rule 4 applies
language: ru (ru-orig auto-generated; see ASR warning below)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 31
promotional_ratio: low
corroborates_existing: true (independently repeats the staged workflow, the guest-link review and the wet-room socket offset from YT_DI5GAV64mnU, on a different flat)
---

# Extraction Note — Дизайнер Дмитрий К: "Технический дизайн проект квартиры в Remplanner — обзор с комментариями" (YouTube F0rXrbPDPf4)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

Same designer, same format, **a different flat and four months earlier** than `YT_DI5GAV64mnU`. This pairing was selected deliberately in Round 1 to test whether the format repeats or whether the first walkthrough happened to be the good one.

> [!IMPORTANT]
> **⚠️ The format repeats and holds — and this one is DENSER on the sheet set than the longer video was.** 18 minutes against 33, and it enumerates ~18 tabs where the other named 9. **The Round 1 scoping hypothesis (yield tracks format, not topic) is confirmed for this channel.**

> [!WARNING]
> **⚠️ This transcript's ASR is markedly worse than `YT_DI5GAV64mnU`'s — it carries no punctuation at all** and mangles heavily: «Редактор… который называется р» / «редакторе rer» for Remplanner, «плане ЕС», «за карнизам», «тартер» (likely торшер), «пена кухни» (стена кухни), «отвёртки стен» (развёртки стен), «пальш-панель» (фальш-панель). **Segmentation of a claim to a specific room is therefore less reliable here than in the other note. Where a room attribution below could not be read with confidence it is flagged.** This is exactly the software-subject ASR degradation recorded in the triage.

## Value-filter verdict

**Full extraction.** The single most useful source found so far for `00_Master/Planning_Project_Deliverable_Set.md`.

## Quantities / Measurements — ⚠️⚠️ the sheet set, as a second independent instance

Our 16-sheet target set was derived from **one** architect's album (Sergey Dolgushev), and that document's own line invites a second opinion: *"treat the sheet list as a checklist to argue with."* **This is that second instance, from a different practitioner in a different tool.** Tabs he walks, in order:

| # | Sheet / tab | Notes he attaches to it |
| :-- | :--- | :--- |
| 1 | **исходная планировка** | |
| 2 | **демонтаж** | Near-empty: no перепланировка, so only old radiators would be shown. **Same reasoning as `YT_DI5GAV64mnU` — a sheet may legitimately be blank** |
| 3 | **план перегородок** | **Dimensions of every partition** |
| 4 | **экспликация помещений** | |
| 5 | **расположение радиаторов** | A dedicated sheet for radiators |
| 6 | **план мебели** | |
| 7 | **привязки сантехники** | ⚠️ **Plumbing drawn in GREEN**, with per-element comments |
| 8 | **водоснабжение** | What he says matters most here: **осевые привязки** of the communications |
| 9 | **план розеток** | **Heights shown, plus a comment on each stating what the socket is for** |
| 10 | **план освещения** | Read in conjunction with the furniture positions |
| 11 | **план выключателей** | ⚠️ **Which switch drives which group, groups colour-coded, with lines drawn from the switch to each group it controls** |
| 12 | **план тёплых полов** | Plus the thermostat position |
| 13 | **кондиционеры** | ⚠️ Again a dedicated A/C sheet — **we have none** |
| 14 | **напольные покрытия** | Material per room **and the laying pattern** |
| 15 | **схема отделки (walls)** | ⚠️ **Tile shown in brick-red, everything else is wallpaper.** And see the cost note below |
| 16 | **схема потолков** | Ceiling material plus the positions of за-карнизные niches |
| 17 | **схема гидроизоляции** | Where waterproofing is applied |
| 18 | **развёртки стен** | ⚠️ **Electrics AND finishes are shown on the elevations**, so heights can be read off them |

- **Album generation to printable PDF is a separate step from review.** Review happens on the guest link on screen, because *«для согласования удобно всё это просматривать на экране»*, and because narrating is faster than annotating: *«я даю краткие пояснения, потому что это быстрее, чем комментировать в печатном виде»*.
- ⚠️⚠️ **The finish scheme is explicitly a costing input, not only a drawing**: *«эта схема отделки — она также поможет в расчёте стоимости ремонта»*. **This is the practitioner stating the `cap5` finish-schedule → BOM link that the gap analysis identified as designed-but-unpopulated.**
- ⚠️ **A scope boundary worth recording**: *«эти строительные планы меня не интересуют, дизайнер их не отрабатывают»* — the construction/строительные plans are **not** the designer's deliverable. Useful for arguing about which of our 16 sheets are actually in scope.
- **The furniture layer is left switched on during development and turned off for the final drawings** — *«при создании заключительной версии этих чертежей, для того чтобы мебель не мешала, её можно будет отключить»*. **A layer-visibility convention that differs between the working view and the issued sheet.**
- **The stated purpose of the commentary is pedagogical**: *«я специально это подробно прокомментировал, чтобы научить своего заказчика разбираться в предложенной мной документации»*. **The album is designed to be taught, not merely handed over.**

## Lighting — a stated design principle plus a distinct fixture class

- **The principle, in his words: keep lighting to «минимальное количество необходимого освещения» while still preserving цветовое зонирование**, which he calls characteristic of contemporary design. **An explicit argument against over-lighting, from someone selling lighting plans.**
- ⚠️⚠️ **Floor-level recessed navigation lights («навигационный свет») in the corridor** — dim, switched on for the night by their own switch, lighting the direction of travel from bedroom and living room toward kitchen and wet rooms. **A distinct fixture class with a purpose and its own switch, not a decorative accent.** This is `cap6` scenario data: the scenario is "walking to the bathroom at night".
- **Bedroom: doubled or single-but-more-powerful fixtures in the room's corners**, which together give sufficient light — and ⚠️ **no light source at all placed above the bed**. Bra at the headboard plus concealed light in the cornice niche instead.
- **Dining zone**: pendant over the table + general light + a few recessed spots.
- **Task lighting as LED strip under wall cabinets**, plus concealed light in the curtain niche.
- **Wet rooms**: one main fixture each, plus extra light in the shower zone.
- **Living room**: decorative central pendant, **plus track lighting — the only room where he uses track**, carrying both pendants and directed spots; recessed spots and concealed cornice light as well.
- **Balcony**: a single fixture.

## Switches / Sockets / Cables — ⚠️⚠️ switch grouping, which is `cap8`

The roadmap's own line is that *"the value of the lighting sheet is entirely in this grouping; the fixture dots are already printable."* **This is a worked example of the grouping.**

- **At the flat entrance: a master switch plus a two-way (проходной) switch covering two lighting groups**, the groups distinguished by colour on the sheet with lines running from the switch to each.
- **The floor navigation lights get their own switch**, thrown at night.
- **Flanking the two-way switch: right for the WC, left for the shower room.** Inside the shower room, one switch controls **the shower light and the extract fan together** — a deliberate pairing.
- **Kitchen approach: two-gang and one-gang two-way switches** covering pendant, spots and concealed light — plus, noticed live during the walkthrough, **one more switch needed for the under-cabinet LED task light**, which he says he will add and reissue.
- **Bedroom: a two-way pair — one left of the entrance, one over the headboard — controlling two lighting groups.** ⚠️ **The reason for splitting the room's fixtures into two groups is stated: so overall brightness in the room can be regulated.** The headboard bra have their own switches; the cornice-light switch sits at the headboard and is **currently not two-way, with «если будет нужно, могу также сделать проходным»** recorded as an option.
- **Living room: two-way control from two points**, with the wardrobe light and the central light on the two-way pair, and **two further separate switches — one for the fixtures on the track, one for the work-zone track.**
- **Balcony: one switch.**

**Socket list, cited to what each serves** (corroborating and extending `YT_DI5GAV64mnU`):
- Kitchen: over-worktop; fridge; oven + hob; ⚠️ **extract hood at 220 cm** (candidate figure, single ASR mention); beside the dishwasher; waste disposer; фартук; TV zone; general sockets in the dining zone.
- Wet room: **вывод for the towel rail**; **вывод for the mirror light**; **a water-protected socket to the side of the basin** — ⚠️ **the same offset-for-splash rule as `YT_DI5GAV64mnU`, from a different flat, so this is his standing practice and not a one-off**; washing-machine socket.
- Corridor: **two sockets in the niche where the washing machine stands**; two over the тумбочка/комод in the прихожая; a вывод for the mirror light; **a robot-vacuum socket** — again, repeated across both flats.
- Bedroom: socket groups **at the dressing area and at the head of the bed**; a TV socket group; a socket over the bedside table.
- Living room: **sockets flanking the sofa**, which he calls *«аналог спальной зоны»* — ⚠️ **an explicit transfer of the bedside-pair rule to the sofa**; a floor lamp can go on them.
- Work zone: sockets **on two levels**.
- **Sockets are verified in 3D against the furniture** before issue.

## Surfaces and Finishes

- **Floor: SPC / кварцевый ламинат in the dry rooms, керамогранит in the wet rooms, and linoleum on the balcony** — the balcony choice has a reason: *«не хочу очень сильно перегружать конструктивными элементами, тяжёлым керамогранитом»*, i.e. **a dead-load argument for a light sheet material on a balcony slab.** He flags it as still under consideration.
- ⚠️ **Laying pattern is specified on the floor-finishes sheet, not left to the fitter** — he changes from **палубная (deck) laying to «английская ёлка» (herringbone)**, while noting the stylistic decision is revisited later.
- **Ceilings: натяжной потолок ПВХ**, with за-карнизные niches located on the ceiling scheme.
- **Walls: tile zones in brick-red on the scheme, wallpaper elsewhere.**

## Plumbing — ⚠️ a consequential claim worth checking

- **On the waterproofing scheme he states: if the wet rooms are to be threshold-free («беспороговое хождение»), then waterproofing must be done over the whole flat's area** — *«тогда гидроизоляцию нужно делать по всей площади квартиры»*.
  - ⚠️⚠️ **Flagged as needing corroboration, and it is the single claim in this note most worth checking.** As literally transcribed it is a strong claim (whole-flat waterproofing), and it carries a real cost consequence. It may be a compressed statement of a narrower rule (wet room plus a margin into the adjoining room), and the ASR here is poor. **Do not act on it or route it as a rule until a second independent source is found.** Standing rule 3: this is his opinion as stated, not a norm.
- Plumbing gets both an **attachment/привязки** sheet and a separate **водоснабжение** sheet, with axial (осевые) attachments called out as the thing that matters.
- **Underfloor heating: a plan exists with the thermostat located**, though he says it is only partly worked out at this stage.

## Design Concept — model review affordances

- ⚠️ **The 3D review view can toggle ceiling lighting on and off, toggle the display of sockets, and hide all furniture in order to see socket positions alone.** He also switches the развёртки between 2D and 3D. **Recorded because our `_Drawings/review/` artefact is a static overwritten drawing — this is a capability comparison, and the "hide furniture to check the sockets alone" view is the one worth reproducing.**
- **A/C: one unit planned for the whole flat**, moved from where Планоплан had it at the client's request, with more to be added only if needed.

## Unclear / Needs Confirmation

- **The whole-flat waterproofing claim above.** Highest-priority open question from this source.
- The 220 cm hood-socket height is a single ASR mention.
- Because this transcript has no punctuation, **a few room attributions in the socket and switch lists are read from context and could be off by one room.** They are recorded as read; anything load-bearing should be re-checked against the video with `tools/youtube/extract_layout_frames.py`, which would also capture the sheets themselves.
