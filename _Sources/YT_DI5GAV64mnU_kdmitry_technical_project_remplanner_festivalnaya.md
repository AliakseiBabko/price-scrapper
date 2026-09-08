---
source_type: video transcript (designer's client-facing progress report, published publicly — walkthrough of the delivered technical part of a design project)
source_url: https://www.youtube.com/watch?v=DI5GAV64mnU
video_id: DI5GAV64mnU
transcript_file: _Archive/processed_sources/20260908_kdmitry_technical_project_remplanner_festivalnaya_965d6902.txt
fetched: 2026-09-08 (anonymous, yt-dlp --write-auto-subs --sub-langs ru-orig)
upload_date: 2025-07-22 (confirmed via yt-dlp metadata)
duration: 33:33
channel: "Дизайнер Дмитрий К" (@k_dmitry, 372 subscribers) — a practising interior designer, Moscow; the channel is a public log of client progress reports
source_metadata_location: Moscow, Фестивальная улица (stated in title and transcript)
jurisdiction: Russia — standing rule 4 applies, nothing routed to 16_Legal_and_Regulations/
language: ru (ru-orig auto-generated; see ASR warning below)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 24
promotional_ratio: low
corroborates_existing: false (new subject matter — no prior vault source covers the production of a technical design package)
---

# Extraction Note — Дизайнер Дмитрий К: "Технический дизайн-проект квартиры на Фестивальной в Remplanner: подробный обзор" (YouTube DI5GAV64mnU)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

**A source type new to this vault: a designer's client-facing progress report, published publicly.** The narration is addressed to his own clients («даю пояснение… моим заказчикам»), not to a YouTube audience, and the channel has 372 subscribers. **Promotional ratio: low, and for a structural reason rather than a charitable one — he is not selling to the viewer; the viewer is incidental to a client review.** He names no supplier, quotes no price, and pitches no service.

The corresponding limit, stated plainly: **this is one project, not a pattern synthesised across many.** Per the value-filter criteria, that puts it below a practitioner who compares cases — so the transferable content is his *method and conventions*, which repeat across his catalogue, rather than any particular decision about this flat.

> [!WARNING]
> **⚠️ ASR quality is materially worse than this vault's usual sources, because the subject is software.** Observed in this transcript: «Rimliner»/«ремплайнере» for Remplanner, «потудомочной машины» for посудомоечной, «канузла» for санузла, «полотенсушитель», «покисушителя». **Every number below was heard once in auto-captions and is recorded as a candidate, not a confirmed figure** — see the flag on each. Independent corroboration is noted where `YT_F0rXrbPDPf4` (the same designer, a different flat) states the same thing.

## Value-filter verdict

**Full extraction.** The value is not the flat — it is that he narrates *why the documentation is shaped the way it is*, which is the one subject this vault has ~250 pages and no source for.

## Design Concept / Planning Rules — the staged workflow

- **A stated three-stage регламент работы**, in his words: **stage 1** — concept layout and furniture arrangement agreed with the clients in Планоплан; **stage 2** — «базу технической части» built in Ремпланнер; **stage 3** — detailed visualisation per room. He is explicit that stage 2 comes **before** detailed visualisation, and gives the reason: the technical base *«позволяет составить целостную картину расположения всех инженерных элементов, привязки к мебели и оборудованию… ещё раз сформировать целостную картину работ по ремонту»* before effort goes into renders.
  - **Why this matters beyond his practice**: the ordering claim is that **engineering coordination is a cheaper place to discover a layout problem than a render is.** Corroborated by the same designer on a second flat (`YT_F0rXrbPDPf4`), where he opens with the identical stage-2 framing.
- **Client review is done on a live guest link to the model, not on the PDF** — he sends the clients the same view link he is narrating from, and walks the tabs. The printable album is generated separately. (Same practice in `YT_F0rXrbPDPf4`, where he adds that on-screen review is *«удобно для согласования»* and that he corrects the model live and reissues the link.)

## Doors / Trim — a rule with a rationale

- **Door swing direction is set by switch reachability**, not by room convention: *«я его привязываю к тому, чтобы было удобно пользоваться выключателями при входе-выходе из комнат»*. On this flat he reversed the living-room door to open outward and changed the swing on the санузел and kitchen doors on that basis, on the **исходный план** sheet — i.e. before anything electrical was drawn.
  - ⚠️ **This is a "connect the dots" derivation running backwards from the usual direction — electrics constraining door geometry.** Worth recording as a planning rule; see `data/layout_rules/rules.jsonl`.
- **He does this even where there is no перепланировка at all** — the flat has no capital changes, and door swing is still treated as a live design variable.

## Walls / Ceilings

- **A suspended-ceiling drop of 80–100 mm is affordable where ceiling height allows, and is what buys freedom to route cable and lighting where wanted** — *«даже если опустить потолок на 8–10 см, мы можем себе это позволить… расположить элементы освещения и коммуникации… там, где нам нужно, не сильно занижая доступную высоту»*. He uses this to reject a client-side reservation about suspended ceilings, while adding *«если я не ошибаюсь, конечно, мы это ещё раз проверим»*.
  - ⚠️ **Figure heard once in ASR; and it is his affordability threshold on this flat, not a general minimum.** The vault holds a contested 27 mm drop figure measured from a different datum (see the `@YourInteriorDes` Round 1 finding) — **these are not comparable and must not be reconciled**: 27 mm is a plasterboard/track minimum, 80–100 mm is a service-routing allowance.
- **The демонтажный план is deliberately near-empty and he says why** — demolition work will happen on site (old radiators, old finishes) but with no capital changes he carries no special notation, and the same for the план перегородок. **Deliverable-set discipline: a sheet can legitimately be blank, and the album says so rather than dropping it.**

## Switches / Sockets / Cables — socket-by-socket derivation from named appliances

**This is `cap6`→`cap8` performed aloud: every point is cited to an appliance, a routine or a client request.** Per the gap analysis this pays twice — the same count is the `ELE-01` BOM quantity, currently `unmeasured`.

⚠️ **All heights below are single-mention ASR figures. Treat as candidates.** Where `YT_F0rXrbPDPf4` independently repeats one, that is noted.

**Kitchen**
- A **row of sockets for the dishwasher, hob and oven, placed off to the side behind the dishwasher, low down at plinth/цоколь level**.
- A separate low socket for the **fridge**.
- A socket for the **waste disposer (измельчитель)**.
- Sockets **on the фартук at 105 cm** — ⚠️ candidate figure.
- A socket for the **TV**.
- Sockets **at 170 cm** for microwave, kettle and other equipment standing on the additional worktop created when the kitchen was reconsidered in Планоплан — ⚠️ candidate figure. He notes a second group also at the 105 cm level.
- Additional sockets **at 30 cm ("стандартная высота") at the room entrance**, and by the dining table.

**Wet rooms (both)**
- A **вывод for the lighting** (not a socket).
- **Two moisture-protected sockets set deliberately to one side** — *«чуть-чуть в стороне, чтобы вода на них не попадала»* — while still being *«под рукой»*. **A rule with its failure mode stated: the offset exists to keep splash off, and the constraint is that it must not cost reachability.** He calls this his standard: *«по стандарту, как я это делаю»*.
- A point for the **electric towel rail**, and sockets for **washer and dryer**.

**Corridor / прихожая**
- A socket for a **voice assistant**, explicitly *«по просьбе заказчиков»* — a client-requested point, not a derived one.
- **Two sockets in the corner mid-corridor at a height convenient for use while seated on the shoe bench (тумба для обуви)**.
- A **robot-vacuum parking socket**.
- One more socket at the exit «для обслуживания» — cleaning-appliance service point.
- ⚠️ **The щиток is placed inside the wardrobe adjoining the entrance**: he judges it easiest to bring the cable into that cupboard and house the квартирный щиток with автоматы and реле there, together with the слаботочный panel. **A `cap8` decision with a location rationale — proximity to the incoming cable and concealment inside joinery.**

**Bedroom**
- A **вывод for the air conditioner**, with the unit **moved to above the door**, which he calls *«одно из рекомендованных местоположений»*.
- A socket for an **air purifier**.
- A **TV socket block behind the TV, because the TV is on a bracket** — the bracket is the reason the block sits where it does.
- **A pair of sockets at the dressing table**, and **a pair each side of the bed**.
- A **вывод for lighting inside the wardrobe**.

## Quantities / Measurements — sheet set as an information model

- **He ships a план кондиционеров as its own sheet**, and uses it to record the A/C position before the socket plan is read. ⚠️ **See the repo finding in `_Inbox/planning/design_toolchain_sources_triage_20260908.md` §6: our own 16-sheet deliverable set has no A/C sheet at all.**
- **Socket and furniture layers are overlaid deliberately** — the socket plan is read *«с наложением на план расположения мебели»*, because a socket position is only meaningful against the object it serves.
- Tab structure observed on this project: исходный план · замерные планы · демонтажный · перегородки · мебель · развёртки стен · розетки · освещение · кондиционеры. **A fuller enumeration from the same designer is in `YT_F0rXrbPDPf4`, which lists ~18 tabs and is the better source for the sheet set.**

## Furniture / Built-ins

- **A wet-room worktop formed over the concealed-cistern WC**, giving a shelf; boiler above; hooks for towels; **a niche for a washer/dryer column**; a mirror niche with concealed lighting; a laundry-basket space under the worktop. He checks all of it **on the wall развёртка** rather than on the plan — *«давайте посмотрим на развёртке стен… как это может выглядеть»*.
- **A bench doubling as a shoe store (скамья/обувница)** in the прихожая.
- **A room excluded from the project is excluded from the drawings, and he says so rather than leaving it ambiguous** — one room is not touched by the renovation, so he does not develop it on the furniture plan, while noting it stays in the plan of works.

## Family Requirements / Preferences

- Client-driven changes carried into the technical stage: bed moved closer to the corner in the kids' room, desk shifted to the side, a beanbag repositioned, **a beanbag added "for a guest, the daughter's friend"** — a named social scenario driving a furniture item.
- **Storage furniture deliberately left generic at this stage** — «комод или стеллаж», resolved later at detailed visualisation — *«главное, что мы находим её место»*. **A staging principle: reserve the volume now, choose the object later.** This is the same role/identity split the BOM design uses (`resource_role` vs `product_id`).

## Mistakes / Warnings

- He corrects himself live on an omission (a switch he had not yet placed) and states the model and guest link will be updated — **the review mechanism is expected to catch things, and the artefact is expected to change.** Recorded because our `_Drawings/review/` convention (overwrite, git holds the previous state) rests on the same assumption.

## Unclear / Needs Confirmation

- Whether «одно из рекомендованных местоположений» for an A/C above a door refers to a manufacturer recommendation, a trade norm, or his own practice. Not stated.
- The 105 cm / 170 cm / 30 cm socket heights and the 80–100 mm ceiling drop are all single-mention ASR. **Cross-check against the vault's existing socket-height pages before any of them is treated as a figure.**
- His claim that the flat needs no перепланировка is asserted, not evidenced, and is a fact about his project rather than a transferable one.
