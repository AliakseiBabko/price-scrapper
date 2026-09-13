---
source_type: video transcript (Korean architecture channel, first of a two-part pair)
source_url: https://www.youtube.com/watch?v=26UFabH--JU
video_id: 26UFabH--JU
transcript_file: _Archive/processed_sources/20260913_feeeld_villa_savoye_ruby_console_58307018.txt
fetched: 2026-09-13 via youtube-transcript-api (ko auto captions — ORIGINAL language)
upload_date: 2026-09-09 (confirmed via yt-dlp metadata)
channel: feeel.d (presenter 김석현 / Kim Seokhyun)
source_title: "GPT-6 Astra가 SketchUp을 직접 조작해서 모델링을 완성했습니다!" (Astra directly operated SketchUp and completed the modelling)
language: ko
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 4
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — feeel.d: PARTIALLY PROCESSED — the Predecessor, and Why Villa Savoye Is Not a Test (YouTube 26UFabH--JU)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## ⚠️ Partial extraction — this is the "before" of a pair

**Same channel and presenter as [[_Sources/YT_Qh9xgjd38VI_feeeld_drawings_to_sketchup_with_revision|Qh9xgjd38VI]], four days earlier, and that later video explicitly refers back to this one** as the Ruby-console attempt made *«MCP를 전혀 사용하지 않은 방식»* — with no MCP at all.

**The later video supersedes it on every axis that matters**: it uses a real unknown drawing set, tests revision, and has the author's own manual subtitles. **The overlapping material is not re-extracted.** `fact_yield: 4`, and three of the four are methodological rather than about capability.

## ⚠️⚠️ The Finding That Matters: a famous building is not a test of drawing comprehension

**The subject is Villa Savoye**, and he says plainly why that made it easy: *«유명한 건물이기 때문에 이미 도면 같은 게 온라인상에 많이 올라와 있어요. 그래서 그 올라와 있는 것들을 GPT가 알아서 찾아서 그걸 기반으로 해서 수치도 어느 정도 추측을 해 내고»* — **it is a famous building, its drawings are already all over the internet, so the model found them itself and inferred the dimensions from them.**

> **⚠️⚠️ → THIS DEMONSTRATES RETRIEVAL AND RECALL, NOT DRAWING COMPREHENSION.** A model reproducing Villa Savoye may be reconstructing something it already knows, from sources it fetched, rather than reading what it was given.
>
> **→ And that makes the SUCCESSOR video the real test**, because it supplies an **anonymous, free-to-download US house** whose drawings the model cannot have memorised. **When assessing any "AI modelled this building" demonstration, the first question is whether the building is famous.**

**⚠️ This generalises beyond this source, and it is the reason the note is kept at all:** it is the same class of confound as a benchmark leaked into training data. **Recorded as a triage test for this whole content class.**

## ⚠️ Durable Facts — the cheap-tier test, which is good methodology

**He deliberately ran this on the WEAKEST configuration available to him**, and explains why:

- He has two accounts: a **company pro tier at roughly 280,000 KRW/month**, and a **personal general subscription at about $20/month**. He used the personal one, **on the "Light" model rather than a stronger one.**
- **His reasoning: the pro account would obviously succeed, so it proves nothing** — *«프로 버전은 돈을 많이 내니까 당연히 한도가 좀 더 훨씬 크기 때문에 당연히 진행이 될 거라고»*. He wanted to know whether a normal subscriber would hit the token limit partway.
- **It completed on the cheap tier.** He notes a higher tier would probably have done better.

> **→ Testing the ACCESSIBLE configuration rather than the best one is the more useful experiment, and it is rarer than it should be in this source class.** ⚠️ **Both subscription figures are Korean/US consumer tiers that will date within months — recorded as context, not routed as prices, and not converted.**

## Durable Facts — Two Smaller Items

- **With permissions granted in advance, the agent opens the SketchUp file itself and starts from a zero base** — *«스케첩 파일부터 GPT가 열어 줍니다… 진짜 제로 베이스 상태에서»*.
- **⚠️ His prompt ENUMERATES the elements to be modelled** rather than describing the building: ramp, stairs, floor slabs, windows, glazing, terrace, roof, parapet, structure — **plus the exact SketchUp version (21), which he stresses.** A worked instance of the "specify the process and the expected output" rule already recorded in this folder; the version pin matters because the generated code targets a specific API.
- Result judged **against photographs** — *«사진이랑 비교를 해 봐도 거의 비슷한»*, nearly similar. **A visual comparison, not a measurement.**

## Confidence & Evidence Notes

- **`single-account`**, one run. **Model names, tiers and capability verdicts deliberately NOT routed** per the standing dating rule.
- **⚠️ No dimensional verification of any kind**, and given the Villa Savoye confound, **no conclusion about drawing comprehension can be drawn from it at all.**
- **ASR (Korean)**: adequate; loanwords mangled — «캐치업»/«스케첩» for SketchUp, «아스트로» for the model name, «프로포트» for prompt, «파라펜» for parapet.
- **No prices carried; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Agent_Connected_CAD.md`** — the famous-building confound as a triage test, and the cheap-tier methodology note.
- **5b**: subscription figures are consumer tiers, deliberately not converted.
