---
source_type: video transcript (Korean architecture-tech channel, hands-on model test with measured checks)
source_url: https://www.youtube.com/watch?v=-FsHQEYldnQ
video_id: -FsHQEYldnQ
transcript_file: _Archive/processed_sources/20260913_grasshopperpp_computer_use_autocad_36215d42.txt
fetched: 2026-09-13 via youtube-transcript-api (ko auto captions — ORIGINAL language)
upload_date: 2026-09-12 (confirmed via yt-dlp metadata)
channel: Grasshopper Plus Plus (presenter 현철 / Hyuncheol)
source_title: "GPT-6 Astra | AutoCAD Drawing | Computer Use"
language: ko
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 13
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — Grasshopper Plus Plus: "Computer Use" Is Script Generation With a GUI Performance (YouTube -FsHQEYldnQ)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## ⚠️⚠️ A language finding that matters beyond this source

**This video has an ENGLISH title and KOREAN audio.** The caption manifest shows `ko-orig`; it was fetched as `ko` and the metadata confirms `language: ko`.

**→ The standing language rule is written around Russian sources whose English titles hide Russian audio. It generalises exactly: TITLE LANGUAGE IS NOT A SIGNAL OF SPOKEN LANGUAGE, in any language pair.** Had the habitual `en` been used, this would have been an auto-**translated** track — the precise failure rule 1 exists to prevent. **This is the vault's first Korean-language source.**

`promotional_ratio: low` — nothing is sold; it is a hands-on test with the presenter reacting live.

## ⚠️⚠️ The Central Finding — "Computer Use" Is Not What It Looks Like

**Setup, stated explicitly and importantly: *«제가 MCP 연결을 하지 않았어요»* — he did NOT connect MCP.** AutoCAD was simply open on screen; the model was asked whether it could draw the plan. A permission dialogue appeared (*«캐드 사용하도록 허용할까요?»*) and the GUI visibly flickered blue around the cursor as the agent operated it.

**So on the surface this is a fourth architecture — driving the GUI directly, beyond the open-loop, closed-loop and tool-driving patterns the vault already holds. IT IS NOT, and the presenter says so himself:**

> *«사실 컴퓨터 유즈에서 이렇게 하나씩 보여 주는 건 사실 인간을 위한 거죠… 얘는 도면을 그냥 한 방에 탁 그려 버렸어요. 이미 정보가 다 있으니까.»*
> — **"Showing it one by one in Computer Use is actually FOR THE HUMAN. It just drew the whole drawing in one shot, because it already had all the information."**

**What it actually did**: read the PDF, **converted PDF → PNG to read it**, built a complete plan, then **WROTE PYTHON SCRIPTS** — a `create plan` and a `check plan` — which set defaults, created the layers, and drew the geometry. **The script ran past 4,000 lines.** On the second run it simply **called the already-written script and produced the drawing in one shot**, with no step-by-step animation at all — which visibly disappointed him (*«애니메이션 실패»*).

> **⚠️⚠️ → "Computer Use" on this evidence collapses into the TOOL-DRIVING / CODE-EXECUTION architecture already recorded on [[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]]. The GUI stepping is a rendering of progress for an observer, not the mechanism.** **Do not record it as a distinct architecture.**

- **⚠️ Its drawing ORDER matches human practice**, which he notes: plan → lines → text → **dimensions last**. *«그리는 방식이 우리랑 되게 비슷합니다.»*
- It also produced a **`geometry.json`** holding the extracted per-object information, layer-separated — **a structured intermediate, not just geometry.**

## ⚠️⚠️ The Failure — "Complete" Was Printed Before the Work Was Complete

**The first run hit a TOKEN/credit limit mid-execution** (*«아웃 오브 코덱스… 토큰 제한에 걸리고 말았습니다»*), against a stated **five-hour window** that later reset.

**⚠️⚠️ And the part that matters: it had already printed a COMPLETE message, while the drawing was visibly half-finished** — *«아까 컴플리트 메시지는 떴었는데»*, *«뭔가 그리다 만 것 같은»*, *«약간 어설프긴 하죠»*.

> **→ A SELF-REPORTED SUCCESS THAT WAS NOT ONE.** Exactly what `00_Master/Validator_Design_Discipline.md` exists for — **printing is not checking**, and a completion message is an assertion, not evidence.

- **⚠️ The recovery is the useful half: because the PLAN and the SCRIPTS had been written to disk, the work was resumable.** After the reset he said in effect *"I have checked the scripts and information in the work folder — now draw the drawing from the start"*, and it reused them. *«이미 다 계획에 있었고 다만 실행하다가 크레딧이 날아갔을 뿐»* — the plan was always there; only execution lost its credits.
- **→ DURABLE INTERMEDIATE ARTEFACTS ON DISK SURVIVE A CONTEXT OR CREDIT FAILURE.** An agent that plans into files rather than into its context window can be resumed; one that plans in-context cannot. **A real argument for the file-based working style this repo already uses.**

## ⚠️ Numeric Data — What Was Checked, and It Was Checked

**Unusually for this source class, he verifies rather than asserts:**

- **Overall dimensions read correctly from the PDF: 18.4 m × 11.8 m.**
- **A distance measured in the result: *«거리 한번 확인해 보니까… 정확합니다»* — accurate.**
- **Dimensions behave properly** (*«치수 제대로 움직이고 있습니다»*) and **dimension spacing is accurate** (*«치수의 간격 이런 거 봐도 너무 정확하다»*).
- Door details, dimension centrelines and wall representation all rated good; even overlapping tree symbols reproduced *«작가의 의도를 그대로»* — the original author's intent intact.
- **It also succeeded from an IMAGE-based drawing, not only a PDF** — including a section embedded in a box inside the plan.

## ⚠️⚠️ Two Findings That Land on Open Items in This Vault

### 1. The agent silently chooses a DATUM — bottom-left of the wall

> *«여기 재밌는 게 원점을 여기다 그리더라고요… 이거는 꽤 공통적으로 나옵니다. 벽의 왼쪽 아래를 원점의 중심으로 삼는다. 이거 굉장히 특이한 발견인 것 같아요.»*
> — **"It puts the origin here. This comes up QUITE COMMONLY. It takes the BOTTOM-LEFT OF THE WALL as the origin."** He calls it a notable discovery, and **observes the same placement from a second, different model.**

- **⚠️⚠️ This is the silently-supplied-values rule applied to THE DATUM** — the class of defect `Drawing_Conventions_From_Practice.md` §7 already records (an agent inventing 5-inch walls and a 9-ft ceiling). **Here the invented value is the coordinate origin, which is more consequential because everything else is measured from it.**
- **⚠️ And this project has that exact question OPEN**: §1 of that page records *"The datum, which is still ours to decide."* **An observed convention that two independent models converge on is worth knowing before choosing — not as authority, but as the default you will be fighting if you choose differently.**

### 2. ⚠️⚠️ A second model OVERRODE the dimension text so it disagreed with the geometry

Testing a different model on the same plan, he finds it accurate **but**: *«치수를 오버라이트 했다. 치수를 오버라이트해서 실제 치수랑 다르다»* — **it overrode the dimension text, so the displayed dimension differs from the real geometry.**

> **⚠️⚠️ This is a DRAWING THAT LIES, and this vault already established the mechanism that permits it.** `Drawing_Conventions_From_Practice.md`'s closed open-item 2 records that **in DXF a dimension's text is an arbitrary override in group code 1 that nothing computes from — change the geometry and the override goes stale.** **Here a model writes exactly such an override, at generation time.**
>
> **→ A generated drawing's dimension TEXT must never be trusted as evidence of its geometry. Measure the geometry.** ⚠️ **`check_dxf_closure.py` and `vector_extent_oracle.py` already work this way — asserting against the geometry and against the PDF's own hatched solids rather than against annotation — which is precisely the defence.** Independent confirmation that the defence is aimed at a real failure.

## ⚠️ Named Limitations of the Generated Geometry

- **Everything is POLYLINES** — *«객체를 아직은 다 폴리라인으로 그리긴 해요»*. **Curves drawn as polylines use far too many points** (*«너무 많이 그려요»*).
- **⚠️ NO BLOCK CONCEPT** — *«블록 개념은 아직 없는 거 같아요»*. The WC is drawn well but as unique geometry, not a reusable symbol.
- **No dashed-line concept** — *«점선 그런 개념 없고 하나씩 다 그렸다»*, drawn piece by piece.
- **Korean text hit an encoding problem** (*«한글이라서 다른 문제로 되어 있고»*).
- Layers WERE created correctly and named as instructed (an `A` architecture prefix); the comparison model used `A` / `L` for architecture and landscape.

**→ Taken together: it produces a drawing that LOOKS right and is STRUCTURALLY naive — no blocks, no linetypes, over-tessellated curves. Fine as a picture, weak as a model to edit or to take quantities from.** Consistent with the transcription-succeeds / structure-fails pattern recorded across this folder.

## ⚠️ Confidence & Evidence Notes

- **⚠️⚠️ MODEL NAMES AND VERDICTS ARE DELIBERATELY NOT ROUTED**, per the standing rule that capability claims date fastest of anything in this vault. **What is routed is the architecture correction, the datum observation, the dimension-override failure, the complete-before-complete failure, and the structural limitations** — all of which outlive the model generation being tested.
- **`single-account`**, one session, one operator, no replication. **The measured checks are spot-checks made on camera, not a benchmark.**
- **ASR (Korean)**: adequate but mangled on loanwords — «컴퓨터 유주»/«컴퓨터 유즈» for Computer Use, «아웃 오브 코덱스» for the credit/limit message, «페이블» for the comparison model, «킨더튼» for kindergarten, «지오메트리.j이슨» for `geometry.json`. **Figures heard once are candidates; the 18.4 × 11.8 m reading is stated clearly and repeated in effect by the accuracy check.**
- **⚠️ One contrast worth recording against [[_Sources/YT_E-ECbD14g_8_sketchupessentials_mcp_permission_and_estimation|E-ECbD14g_8]]: that operator scoped execution permission to the session; this one clicks *«항상 허용»* — ALWAYS ALLOW.** **The safer discipline is the first, and this is a live example of the looser one.**
- **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Agent_Connected_CAD.md`** — Computer Use collapsing into tool-driving; the complete-before-complete failure; durable artefacts enabling resumption; the structural limitations; the always-allow contrast.
- **`18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §1 and §7** — the bottom-left-of-wall datum convention, and the dimension-text override as a drawing that lies.
- **5b**: no prices; no conversion owed.
