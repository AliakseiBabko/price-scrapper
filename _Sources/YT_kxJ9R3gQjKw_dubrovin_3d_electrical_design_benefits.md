---
source_type: video transcript (practising electrical installer and designer, arguing the case for 3D electrical design from commercial experience)
source_url: https://www.youtube.com/watch?v=kxJ9R3gQjKw
video_id: kxJ9R3gQjKw
transcript_file: _Archive/processed_sources/20260917_dubrovin_3d_electrical_design_benefits_2ada0ee0.txt
fetched: 2026-09-17 via youtube-transcript-api (ru, forced per standing rule 1)
upload_date: 2019-11-12 (confirmed via yt-dlp metadata)
channel: Алексей Дубровин
source_title: "3D проектирование электрики"
language: ru
extraction_taxonomy: custom (this project taxonomy - bucket `Digital Toolchain / Engineering systems`)
fact_yield: 9
promotional_ratio: low (channel/social links in the description; the argument itself is substantive)
corroborates_existing: true
region: RU (no jurisdictional claim)
delivery_model: contractor-designer, works only to his own 3D projects
---

# Source Note — Алексей Дубровин: ⚠️⚠️ A PRACTITIONER WHO DOES 3D MEP COMMERCIALLY, AND THE REASONS ARE NOT AESTHETIC (YouTube kxJ9R3gQjKw)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Why this source matters here

⚠️⚠️ **It is the direct counter-case to `RL3IAGeMi5s`.** Lloyd Sark (IfcArchitect) reports that **Bonsai's** native MEP is broken and that openBIM practitioners fall back to drafting 2D overlays on an architectural cut. This source shows a practitioner **modelling electrics in 3D as normal commercial practice** — and the benefits he names are **coordination, quantities and liability**, none of which is a drawing-production convenience.

**The two are not actually in conflict, and the distinction is the finding**: Sark is describing a *tool limitation in one authoring application*; Dubrovin is describing *why the geometry is worth having*. See §4.

## 1. It is his normal practice, not an experiment

Дубровин states he has been doing 3D electrical design for years, that **all his clients now order projects this way and all work is executed only to the 3D project**, and that this has been so for a second year — which he offers as evidence the approach is viable rather than novel. He reports colleagues adopting it too.

> ***«все мои заказчики заказывают проекты, все работы выполняют только по 3d проектам, и уже это происходит второй год… это показывает, что данные проекты востребованы и вполне жизнеспособны»***

⚠️ He adds that he now designs **plumbing the same way**, and that *«сантехника ещё больше даёт преимущества при 3D проектировании»* — **plumbing benefits MORE than electrics**, because electrics is comparatively simple to design.

## 2. The benefits he names, in his order

| # | Benefit | His words |
| :-- | :--- | :--- |
| 1 | **Coordination, and a settled question of blame** | every socket, switch and point is specified and tied down; if the installer forgot one *«это будет явно его вина»*, if the client did, that is equally visible — *«снимает очень много проблем, которые очень портят отношения»* |
| 2 | **The client can actually read it** | a top-down 2D plan is *«не очень удобно»*; **3D развёртки** are *«более наглядно… также, как человек смотрит в реальности»*, and the client sees points **against the furniture** |
| 3 | ⚠️⚠️ **Exact material counts** | *«очень просто посчитать материалы — абсолютно все виды кабеля, выключатели, подрозетники, распредкоробки»*, so the client does not overpay for surplus |
| 4 | ⚠️⚠️ **As-built documentation handed to following trades** | model plus развёртки given to the kitchen fitters, ceiling installers and so on: *«знают, где сверлить можно, где сверлить нельзя»*, and signing for it **transfers the risk of a cable strike** — *«это очень сильно дисциплинирует подрядчиков»* |
| 5 | **Route optimisation on the drawing, not on site** | crossings removed, conduit vs trunking decided, bundle splitting decided, trace width optimised — *«сделать это не вживую на объекте, когда уже кабель прокладывается, а на чертежах»* |
| 6 | **Installation schematics** | the fitter knows which conduit carries which cable without recalling anything: *«просто прокладывать кабель… повышает скорость монтажа значительно и уменьшает количество ошибок»* |
| 7 | **Signals quality of workmanship** | *«вряд ли мастер, который делает тяп-ляп, будет заморачиваться с проектированием»* |

## 2a. ⚠️⚠️ THE QUANTITIES CLAIM IS THE ONE TO TAKE SERIOUSLY

He demonstrates take-off **by selection in the model**, and — critically — **not only of materials but of LABOUR**:

> ***«выделяем кабель — пожалуйста, 300 метров 3×1.5… посчитать кабель 3×2.5 — несколько секунд — 347 метров… надо посчитать, сколько штроб планируется делать — выделяем штробы — пожалуйста, штроб на объекте 67 с лишним метров»***

**→ ⚠️⚠️ CHASE LENGTH IS A PRICED LABOUR ITEM, and it falls out of the model by selecting the chases.** That is the single most transferable claim in the source: штробление is normally estimated, and here it is measured.

## 3. What he does NOT claim

- ⚠️ **No claim about IFC, openBIM, system flows, distribution ports or schema.** The tool is not named in the transcript; the workflow is geometric modelling plus selection-based counting.
- No claim about clash detection as an automated process — coordination is by eye, in the model, against the other trades.
- No claim that the drawing set is generated automatically; развёртки are produced from the model, but the transcript does not describe automation.

## 4. ⚠️⚠️ Reconciling this with `RL3IAGeMi5s` — the finding that matters

> **Sark's complaint is about the SYSTEM layer; Dubrovin's benefits come from the GEOMETRY layer.**

Lloyd Sark reports *«a few issues with the system flow… when you do pipes, when you do connections»* — that is `IfcDistributionPort`, port-to-port connectivity and flow direction, i.e. the semantic network. **Every benefit Dubrovin lists is obtainable from the physical run alone**: a cable of a stated type, following a stated path, at a stated height, in a chase of measurable length.

**→ The 2D-overlay fallback is evidence about Bonsai's MEP authoring, NOT evidence that 3D MEP geometry is unnecessary.** A pipeline that generates geometry from canonical data does not need the authoring UI that Sark finds broken, and can decline the connectivity layer he finds unreliable while still modelling the runs.

## 5. Transfer to this project

- ⚠️ The benefits at §2.4 and §2.5 apply **directly** to the planned full rewire: the owner's stated topology is board → ceiling → drop, and the trades who follow will drill into these walls.
- §2a is the strongest argument for modelling chases as geometry rather than recording them as a property: **chase length is a quantity we would otherwise estimate.**
- ⚠️ **Caution, standing rule 3:** this is one contractor's commercial case for a service he sells. The benefits are plausible and specific, but the source is not disinterested and offers no measured comparison against 2D practice.

## Source Notes
Алексей Дубровин, practising electrical installer/designer (RU), video of 2019-11-12, transcript in Russian (rule 1: `ru` forced, never auto-translated).
