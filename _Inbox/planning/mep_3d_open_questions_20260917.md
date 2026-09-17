# Open questions — modelling engineering systems in 3D

**2026-09-17.** The decision that 3D MEP is worth doing is now evidenced (`00_Master/Model_and_Views.md`). These are the questions that decision *opens*, with what is already answered marked, so the next research round has a target rather than a channel.

**Legend:** ✅ answered — ⚠️ partially — ⛔ open — 👤 needs the owner, not research.

---

## A. What is actually modelled

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| A1 | Is a cable modelled as a **line** or as a **solid** in a chase? | ⛔ | Everyone says "cable lines"; nobody says the geometry. Decides whether chase volume is derivable |
| A2 | Is **conduit (гофра)** modelled separately from the cable? | ⚠️ | Дубровин decides *conduit vs trunking* per route (`kxJ9R3gQjKw`), so the choice is recorded — not that the conduit is drawn |
| A3 | Are **back-boxes (подрозетники)** modelled, or only counted? | ⚠️ | Counted — they appear in his material take-off. Geometry unstated |
| A4 | Are **junction boxes** modelled and described? | ✅ | Yes — inserted during tracing, with *«описание самих распределительных коробок»* to ease wiring (`097wiJBFs0U`) |
| A5 | How is a **chase** represented such that its length is selectable? | ⛔ | ⚠️⚠️ The highest-value open question. Дубровин selects chases and reads *«67 с лишним метров»*; the representation is not shown. **Chase length is priced labour** |
| A6 | Do runs carry **height/level**, or only plan position? | ⛔ | Implied by 3D развёртки, never stated |

## B. Survey — the step we have never done

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| B1 | What must a survey capture before MEP design starts? | ✅ | Full list in `wbUm7i-nHHk` §1: walls, openings, **floor level changes**, **wall composition**, penetrations, riser/stack positions, original heating runs |
| B2 | How are **concealed in-screed heating pipes** located? | ✅ | **Thermal imaging** — *«тепловизионное обследование»* — marking turns and tees |
| B3 | ⚠️⚠️ Will we survey this flat, and when? | 👤 | **Nothing in our unit is field-verified.** Everything rests on flats 53, 109 and 2. The building is unfinished |
| B4 | What precision does MEP design need, versus the ±50 mm build tolerance? | ⛔ | Unstated anywhere |

## C. Circuits and the board

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| C1 | Is circuit membership **derived** from the model or **authored**? | ✅ | **Authored, and it comes FIRST**: *«состав групповых линий — это то, что задаёт, как электрика будет проходить»* (`3cw4oSGr4Cw`) |
| C2 | What fields does a circuit record need? | ✅ | designation, description, breaker rating, cable cross-section, RCD/RCBO + its number, phase; phase-selection relay where used |
| C3 | What governs the **number of lighting circuits**? | ✅ | **Inrush, not steady load** — LED drivers trip a breaker the running current would never reach |
| C4 | How is the board represented? | ✅ | **Two views**: single-line schematic, and a physical DIN-rail layout at real module sizes. Outgoing line cables deliberately omitted from the layout |
| C5 | How many circuits, and what comfort/safety level, for **this** flat? | 👤 | Drives cable counts and board size |
| C6 | Where does the board go? | 👤 | Owner said *near the entrance*; the wall is not chosen |
| C7 | Is the supply **single- or three-phase**, and what is the calculated load? | 👤 | Open since the S3 work. `project_decisions.md` notes an all-electric flat with no gas, so the hob sits on this figure |

## D. Sheets and deliverables

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| D1 | What does the client actually receive? | ✅ | 3D model with all layers + schematics as PDF, **and развёртки of every wall** as a PDF album (`097wiJBFs0U`) |
| D2 | Which derived schematics are needed? | ✅ | board connections, **switching / two-way**, junction-box locations + per-box description, material specification |
| D3 | Are the schematics **generated** or drawn? | ⛔ | Never stated by any source. ⚠️ The crux for us: we intend to generate |
| D4 | How does a 2D discipline sheet come out of an IFC model? | ⚠️ | Mechanism known — camera cut plane → SVG → CSS (`RL3IAGeMi5s`) — but **nobody demonstrates a services sheet**, only architectural |
| D5 | Do we produce развёртки per wall, and does that reuse `room_rollouts.csv`? | ⛔ | Our rollout data covers **1 of 8 rooms** |

## E. The IFC question

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| E1 | Do we model runs as IFC geometry, or keep them outside IFC? | ⛔ | The three MEP practitioners use general 3D tools, **not IFC**. Nobody has demonstrated what we intend |
| E2 | Do we use `IfcDistributionPort` connectivity at all? | ⚠️ | **Leaning no.** Lloyd Sark reports system flow and connections misbehaving in Bonsai; C1 says circuits are authored anyway |
| E3 | Which leaf types for a chased cable — `IfcCableSegment`, `IfcCableCarrierSegment`? | ⛔ | Unevidenced anywhere in 292 videos |
| E4 | What does an `IfcWallType` + `IfcMaterialLayerSet` cost us to emit? | ✅ | Entities known (round 2). **Blocks schedules until done** |
| E5 | Does a services-bearing IFC survive Bonsai without the MEP bugs? | ⛔ | Untested. We would be the test |

## F. Quantities

| # | Question | State | Evidence / gap |
| :-: | :--- | :--- | :--- |
| F1 | Can cable length be taken off per circuit? | ✅ | Yes — by selection; LOFT DIY groups by circuit and reads the group length; Шемчук carries per-cable start/end/**length** |
| F2 | Can **chase length** be taken off? | ✅ | Yes in principle (`67 м`), ⛔ mechanism unknown — see A5 |
| F3 | Does take-off need types, or does selection suffice? | ⚠️ | Bonsai QTO needs **grouping by type**; the general-3D practitioners need only layers/groups |
| F4 | Is there a cable **slack allowance** convention? | ✅ | Шемчук: *«с учётом запаса 15 см на подключение розетки и опуск кабеля»* |

---

## What I would research next, in order

1. **A5 — how a chase is represented.** It is the one item that is priced labour, demonstrably takeable-off, and mechanically unexplained. Nothing else on the list is worth more.
2. **D3 — generated or drawn schematics.** Decides whether the board and switching diagrams are in scope for our pipeline or are hand work forever.
3. **E3 — leaf types for a chased cable run.** Unevidenced in 292 videos, so this is likely a documentation/`ifcopenshell` question rather than a YouTube one.

⚠️ **B3, C5, C6 and C7 are the owner's**, and C7 in particular has been open since the S3 adjudication. No amount of research closes them.

## Where to look, given the channels are nearly exhausted

- **Дубровин**: 18 videos, 5 processed. `3eX61NlC3gE` and `MmR67_wyDL0` (3D plumbing, part 1) **have no captions at all** — they would need audio transcription, which is the only remaining route into that channel.
- **Шемчук**: the five-part album series is processed; the channel may hold more.
- ⚠️ **openBIM channels are exhausted for this topic.** 292 videos, zero MEP. Further Bonsai research should target **E4/E5**, not services practice.
