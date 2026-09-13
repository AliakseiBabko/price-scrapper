---
source_type: video transcript (Korean architecture channel, hands-on test with a real construction drawing set)
source_url: https://www.youtube.com/watch?v=Qh9xgjd38VI
video_id: Qh9xgjd38VI
transcript_file: _Archive/processed_sources/20260913_feeeld_drawings_to_sketchup_with_revision_79ed65ff.txt
fetched: 2026-09-13 via youtube-transcript-api (ko MANUAL subtitles - ORIGINAL language, author-authored)
upload_date: 2026-09-13 (confirmed via yt-dlp metadata)
channel: feeel.d (presenter 김석현 / Kim Seokhyun)
source_title: "GPT-6 Astra, 도면만으로 스케치업 모델링 완성 후 수정까지!" (From drawings alone to a finished SketchUp model - and revision too)
language: ko
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 14
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - feeel.d: A Real Drawing Set to a Model, and the REVISION Question Answered (YouTube Qh9xgjd38VI)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source, and a transcript-quality note

**Selected because its title promises the one thing this vault recorded as impossible on the file-generating path: REVISION.** [[_Sources/YT_X1lnTEpy6PQ_sketchupessentials_claude_connector_day_one|X1lnTEpy6PQ]] found that asking for a change **regenerated the whole model and required re-downloading it**. This tests the other architecture.

**⚠️ The transcript is the AUTHOR'S OWN MANUAL Korean subtitles (`generated: false`) - the highest transcript quality available anywhere in this vault**, and a welcome change from the ASR this source class usually gives. Korean original; fetched as `ko`.

`promotional_ratio: low` - nothing sold; a test driven by a viewer request and his own curiosity.

## ⚠️⚠️ The Architecture Comparison - his own two methods, and why MCP wins

**He has now done it both ways and states the difference plainly:**

| | **Ruby console, NO MCP** (his earlier video) | **MCP** (this one) |
| :--- | :--- | :--- |
| How | Code pasted straight into SketchUp's Ruby console | Registered MCP server; commands issued one at a time |
| Granularity | **Coarse** - *«조금 더 세밀한 조정이 어려운 방식»*, "just say make Villa Savoye and wait" | **Fine** - *«하나하나 명령을 해줄 수가 있어요»* |
| Worked examples | - | *"make a wooden table of these dimensions"*; **"if you need a window changed, ask it to modify just that window"**; **"if 100 windows need changing, change all 100"** |

> **⚠️⚠️ THAT IS THE ANSWER TO THE OPEN QUESTION. The distinction between the architectures is not cosmetic - it is whether you can REVISE. The file-generating path regenerates everything; the MCP path edits in place, at the granularity of a single element or of a hundred at once.**

**⚠️ MCP installation is genuinely hard, and he documents it**: download files from GitHub, install, install a Python execution tool, verify through PowerShell, register the MCP in the harness, restart, confirm the connection. *«생각보다 되게 어렵죠. 그냥 설치하고 이렇게 하면 되는 게 아니에요.»*

- **⚠️⚠️ And his workaround is the neat part: he asked the model to install its own MCP connection.** It took **7 min 16 sec**, performed the installation, and verified the connection itself. **→ Setup friction is itself a delegable task.**

## ⚠️ The Test - a deliberately hard source, deliberately trimmed

**Input: a real, free-to-download US two-storey timber house set** - *«실제로 시공이 가능한 수준의 도면»*, construction-grade, dense with information, **all dimensions present, in feet-inches with millimetres also shown.** He says he chose a hard one on purpose when simpler sources were available.

**⚠️⚠️ He CURATES THE CONTEXT BEFORE STARTING, and this is a transferable move: he DELETES the detail plans** - *«이건 너무 많은 정보가 들어가 버려서 오히려 시간만 많이 잡아먹을 것 같아서»*, too much information, it would only eat time - **reducing the set to 13 pages of elevations, sections and plans.**

- **→ Hand-curating which sheets enter the context is the manual form of the indexing step recorded from Fairley.** Same purpose: keep out what the task does not need.
- **⚠️ And a prompt instruction worth stealing, given as the last line of his request: *«모델링을 바로 시작하지 말고 시간을 좀 소요를 해서 이 드로잉 세트를 좀 이해를 하고 나서 시작을 해라»* - "Do not start modelling immediately. Take some time to UNDERSTAND the drawing set first, then begin."** **An explicit comprehend-before-acting instruction**, and the delegated form of Fairley's *"read the documents yourself first."*

## Numeric Data - Time, and What It Is Worth

- **38 min 57 sec** to a completed model; **the basic form was done in about 20 minutes**, the rest spent on checking because **he had instructed it to double-check repeatedly**.
- **A further 7 minutes** for the revision. **~45 minutes total.**
- **⚠️ His honest benchmark against himself: *«제가 직접 이 건물을 모델링한다고 해도... 45분 안에 해낼 자신이 없습니다»* - even modelling it himself he is not confident he could do it in 45 minutes**, given columns, railings, a single detailed door, and roof detailing.
- **⚠️ A good observation on PERCEIVED cost: watching it work feels slow; *«만약에 내가 다른 일을 하고 있다... 굉장히 빨리 한 것처럼 느껴지겠죠»* - if you are doing other work meanwhile it feels very fast. Attended versus unattended changes the felt cost, not the real one.**
- **⚠️ Account context, recorded and NOT routed as a price**: a pro tier at roughly **300,000 KRW/month** with about **20x the tokens** of a standard subscription. **Korean market, a subscription tier that will date within months - no conversion performed and none owed.**

## ⚠️ What Worked, and What Failed - both specific

**Worked, checked against the PDF's own rendering:** railings, projecting elements, **roof, chimney, window POSITIONS and window SHAPES** - *«거의 완벽하게»*, near-perfect. Floor-plan division into stairs and rooms came out well. **It saved the file to a folder under its own chosen name, and captured plan and section views into the same folder.**

**Failed, and the failures are the familiar family:**

- **The entrance door modelled wrong** - appears raised rather than as one leaf.
- **A sink modelled ROUND where the drawing shows it SQUARE.**
- **The entrance wall arrangement** (apparently for a shoe cabinet) not implemented.
- **⚠️⚠️ Furniture placed ACROSS the stair, blocking the route up.** *«1층에 올라가는 길에 이렇게 계단을 막아버리는»*
  - **→ A SPATIAL-LOGIC failure, the same family as the Revit session's door into an outside bedroom** ([[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp|vmVvpKSSxWE]]). **Transcription succeeds, circulation and adjacency fail. Now observed in a third unrelated tool.**
- **⚠️ His own diagnosis is interesting and plausible: the drawing was construction-grade and SO information-dense that it may have confused it more** than a simpler set would.

## ⚠️⚠️ Two Emergent Self-Verification Behaviours

- **The model set up SECTION CUTS ITSELF and kept checking its own work mid-process** - *«AI가 단면도 어느정도 설정을 해서 이렇게 직접 확인을 중간중간에 계속 하더라구요»*.
- **⚠️⚠️ This is the SECOND independent observation of a model generating its own verification artefact in this batch** - [[_Sources/YT_-FsHQEYldnQ_grasshopperpp_computer_use_autocad|-FsHQEYldnQ]] records it creating a separate "plan review" file to check its own geometry. **Two different models, two different applications, same emergent behaviour.**
- **→ Worth recording as an observed pattern rather than a feature: a capable agent asked to be careful appears to BUILD ITSELF A CHECK VIEW.** ⚠️ **It does not follow that the check is sound** - in `-FsHQEYldnQ` the same model printed "complete" over a half-finished drawing. **A self-generated check is not an independent one.**

## ⚠️⚠️ The Revision Test - it passes, and the method is simple

**He screenshots the elevation, marks the wrong area with a highlighter, and writes in plain Korean: "the door at the building entrance is modelled wrong, fix this part to match the drawing."**

**Result: *«수정을 잘 해줬습니다»* - it fixed it properly**, in about 7 minutes.

- **⚠️ The method is the transferable part: an ANNOTATED SCREENSHOT plus a plain-language instruction.** He notes he uses screenshot-and-markup constantly at work for issuing corrections. **No special prompt engineering; the annotation carries the location.**
- He notes **English prompts work better** but used Korean deliberately.
- **⚠️ His conclusion is the practical one: small fiddly corrections are INEVITABLE - a human modeller produces them too, and an agent produces more (edges not meeting and so on) - and the MCP path means you can simply instruct each fix.** *«이런 것들도 지시를 해 놓으면은 알아서 수정을 해 버리니까»*

## ⚠️ His Honest Overall Verdict

> **Not yet at the level where every detail can be delegated to produce a finished model in one shot. BUT: interpret the drawing, inspect the result, point out what is wrong, and it revises. So beyond "make a box" or "make a railing" - basic modelling AND REPEATED REVISION in real design work are clearly possible, and even complex modelling.**

- **⚠️ His proposed next test is the one this project actually cares about: whether the process can run in REVERSE - extracting DRAWINGS from the model.** Recorded as an open question, not an answer.

## Confidence & Evidence Notes

- **`single-account`**, one test, unreplicated. **Model names and version verdicts deliberately NOT routed** per the standing dating rule; **the architecture comparison, the revision method, the failure classes and the self-verification observation are.**
- **⚠️ No dimensional fidelity was measured.** He compares the model visually against the PDF's own rendering and judges *«거의 완벽»*. **This vault's only measured elevation-to-3D check remains `sujS9Mgveo4`'s 610-versus-616 mm.** **A visual "near-perfect" is not a measurement, and is recorded as the former.**
- **Transcript quality excellent** (author's manual subtitles).
- **No prices carried; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Agent_Connected_CAD.md`** - the Ruby-console versus MCP granularity comparison as the answer to the revision question; the annotated-screenshot revision method; the spatial-logic failure as a third instance; the self-verification observation; delegating MCP setup.
- **5b**: no prices carried; the subscription figure is Korean-market and deliberately not converted.
