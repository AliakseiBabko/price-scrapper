---
source_type: video transcript (practising electrical designer/installer, four short videos giving his complete 3D MEP design method)
source_url: https://www.youtube.com/watch?v=wbUm7i-nHHk
video_id: wbUm7i-nHHk
covers_also: 097wiJBFs0U, 3cw4oSGr4Cw, r4dJsQhzbpM
transcript_file: _Archive/processed_sources/20260917_dubrovin_survey_first_primary_model_1595fe43.txt
transcript_file_pt2: _Archive/processed_sources/20260917_dubrovin_electrical_design_stages_4c9023ca.txt
transcript_file_pt3: _Archive/processed_sources/20260917_dubrovin_circuit_group_composition_3dc34c9f.txt
transcript_file_pt4: _Archive/processed_sources/20260917_dubrovin_board_schematic_two_views_aa3caf44.txt
fetched: 2026-09-17 via youtube-transcript-api (ru, forced per standing rule 1)
upload_date: 2024-12-27 (wbUm7i-nHHk); 2018-03-14 (097wiJBFs0U); 2024-12-11 (3cw4oSGr4Cw); 2024-12-05 (r4dJsQhzbpM) - all from yt-dlp, actually run
channel: Алексей Дубровин
source_title: "С чего начинается 3D проектирование? Обмер помещения." (+ этапы визуального проектирования / состав групповых линий / отображение схемы щита)
language: ru
extraction_taxonomy: custom (this project taxonomy - bucket `Digital Toolchain / Engineering systems`)
fact_yield: 14
promotional_ratio: none
corroborates_existing: true
region: RU (no jurisdictional claim)
delivery_model: contractor-designer
---

# Source Note — Алексей Дубровин: ⚠️⚠️ THE COMPLETE 3D MEP METHOD, IN ORDER — and the survey step we have never done (YouTube wbUm7i-nHHk +3)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

**Follows `kxJ9R3gQjKw`**, which argued *why* 3D MEP is worth doing. These four say **how**, in sequence. Two further channel videos (`3eX61NlC3gE`, `MmR67_wyDL0` — 3D plumbing part 1) **have no caption track at all** and could not be fetched; recorded so the gap is visible rather than assumed empty.

## ⚠️⚠️ 1. IT STARTS WITH A SURVEY, AND THE SURVEY LIST IS THE VALUABLE PART

> ***«с чего мы начинаем 3D проектирование инженерных систем — сначала строим первичную модель, а для этого мы делаем обмер помещения»***

Measured from the entrance door. What he records, in his order:

| What | Detail |
| :--- | :--- |
| Walls, windows, openings | with all dimensions |
| ⚠️ **Floor level changes** | *«перепады пола в санузлах»*, shown in blue where the floor is dropped, plus the open loggia |
| ⚠️⚠️ **Wall composition** | *«состав стен — там, где у нас несущие бетонные стены»* |
| ⚠️⚠️ **Underfloor heating in the screed, by THERMAL IMAGING** | *«делаем тепловизионное обследование и размечаем трубы… как они поворачивают, как они идут, где у нас есть тройники»* |
| Existing penetrations | e.g. holes already drilled for air conditioning |
| Riser and stack positions | water, ventilation, sewer; extract openings; how the services run |
| Original heating pipework | where the developer's pipes actually run, before any alteration |

> ***«всё это должно быть обязательно замерено с объекта в реальности»*** — and only then: *«Когда у нас есть полная 3D модель, мы уже можем начать процесс проектирования — расстановки мебели… расстановку электроточек»*.

**→ ⚠️⚠️ THE ORDER IS SURVEY → MODEL → FURNITURE → SERVICES.** Шемчук (`0c-QhBDQMWE`) states the same sequence independently: furniture first, services to suit.

## 2. The design stages, in his order (`097wiJBFs0U`, 2018)

1. 3D model of the flat from the client's dimensions and photographs. ⚠️ **Walls colour-coded by construction** — load-bearing, plasterboard, brick.
2. Place sockets, switches and luminaires **against the client's actual or intended furniture**, tied to appliances and the kitchen units. Agreed with the client.
3. ⚠️ **Decide the number of GROUP LINES** from the wanted level of comfort and safety; then cable cross-section, breaker ratings, RCD grouping. **Several board layout variants offered**; one agreed — *and only then is the tracing done.*
4. ⚠️⚠️ On the 3D model: **the number and position of CHASES**; cable lines drawn for every consumer **split into groups by cross-section**; junction boxes inserted; routing method chosen *«исходя из материала стен и плана зашивки потолка»*.
5. Then the derived schematics: **board connections**, **switching (two-way switches)**, **junction-box locations**, and *«описание самих распределительных коробок, чтобы облегчить их коммутацию»*.
6. **A general specification of all electrical materials.**
7. **Deliverables — two:** the 3D model with all layers and schematics as PDF, **and развёртки of every wall** as a PDF album.

> **→ ⚠️ ROUTING METHOD IS CHOSEN FROM WALL MATERIAL AND THE CEILING BUILD-UP.** That is this project's substrate rule and the owner's ceiling-distribution plan, arrived at independently.

## ⚠️⚠️ 3. The circuit group list is the DESIGN INPUT, not an output (`3cw4oSGr4Cw`)

> ***«состав групповых линий — это то, что задаёт нам, как у нас электрика будет проходить по дому»***

The list is composed **before** tracing, and each row carries: designation, description of what is in the group, final **breaker rating**, **cable cross-section**, the **RCD or RCBO** used and its number, plus phase-selection relays where needed. **Phase distribution** is decided here.

⚠️ **He always starts with lighting**, and the governing constraint is not steady load but **INRUSH**:

> ***«мы не можем весь свет дома посадить на один автомат, так как… в любом светодиодном светильнике есть блок питания, который при запуске даёт достаточно большой всплеск по току… нагрузку вы будете мерить токовыми клещами — нагрузка будет копеечная, а автомат будет выбивать»***

**→ An engineering constraint that no amount of geometry would ever produce.** It is a reason the circuit list cannot be derived from the model; it is authored, and the model is traced to suit it.

## 4. ⚠️ The board gets TWO representations (`r4dJsQhzbpM`)

- **Formerly a single-line diagram** (однолинейная схема): main switchgear, time relays, cross modules, group RCDs, neutral bars labelled with the groups on them, breaker ratings, line numbers.
- **Now additionally a physical layout view**: the actual DIN rails of the board — a 96-module board in his example — with **every element at its real size and position**, how many neutral and PE bars fit *«сколько их помещается в реальности»*, and internal wiring labelled with a key to where each cable goes.
- ⚠️ **Outgoing line cables are deliberately NOT drawn** on it: *«линейные кабели, которые подключены к конечным автоматам, я считаю, смысла нет [изображать] — достаточно их подписать»*.

**→ ⚠️⚠️ TWO VIEWS OF ONE BOARD — a topological schematic and a physical layout — with an explicit decision about what each omits.** That is the same one-source-many-views problem this project has, solved by a practitioner, including the judgement that a view may legitimately drop detail.

## 5. Transfer to this project

- ⚠️⚠️ **§1 is the step we have never done.** There is no interior survey of this flat — `photo_positions.csv` holds one exterior elevation — and §1 is a ready-made capture list. **Thermal imaging for the in-screed heating is directly applicable**: `project_decisions.md` records horizontal heating distribution with heat meters already installed, and we do not know where those pipes run.
- **§3 settles a design question**: circuit membership is **authored input**, not derived geometry. It also gives the fields a circuit record needs.
- **§4 is a precedent for our view model**, including the principle that a view may deliberately omit.
- ⚠️ **Rule 3 caveat:** Дубровин sells this as a service. No measured comparison against 2D practice is offered in any of the four.

## Source Notes
Алексей Дубровин, practising electrical designer/installer (RU). Four videos, 2018-03-14 to 2024-12-27, transcripts in Russian (rule 1: `ru` forced, never auto-translated). Two further relevant channel videos carry no captions.
