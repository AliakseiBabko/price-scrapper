---
source_type: video transcript (SketchUp-education channel, head-to-head model capability test)
source_url: https://www.youtube.com/watch?v=BEHlmJCKvTA
video_id: BEHlmJCKvTA
transcript_file: _Archive/processed_sources/20260913_sketchupessentials_model_comparison_method_b88a3862.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: TheSketchUpEssentials (Justin Geis)
source_title: "Is AI 3D Modeling FINALLY Here? Testing Claude Fable 5"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 3
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - TheSketchUpEssentials: PARTIALLY PROCESSED - The Comparison METHOD, Not the Verdict (YouTube BEHlmJCKvTA)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️⚠️ Partial extraction, on an instruction written before it was fetched

**The 2026-09-11 triage deferred this with an explicit handling rule: "A model-capability test. Capability claims date fastest of anything in this vault - worth reading only for the EVALUATION METHOD, not the verdict."** That instruction is followed literally here.

**Discarded in full**: every model name and version, which model won, the benchmark commentary, and **the entire availability/pricing discussion** (a named plan tier, a named cut-off date, a shift to usage-credit billing, an intention to restore it later). **That last is the most perishable content this vault has ever been offered** - it was already a moving target on the day of recording. `fact_yield: 3`, and the number is honest.

**⚠️ Fourth source from this one channel across two rounds** (with `f0EU_xbavEA`, `X1lnTEpy6PQ`, `E-ECbD14g_8`). **Treat his claims as one consistent voice, not as corroboration.**

## ⚠️⚠️ Rules / Heuristics - The Comparison Discipline, Which Is the Reusable Part

**He runs two models against the same task and controls the inputs deliberately** - *"I made sure to keep it uniform across the different tests so that everything was apples to apples."*

- **The same prompt to both**, including the clarifying clause: *"Please ask me any questions that you need to do so accurately."*
- **⚠️ Both models asked substantially the same clarifying questions** - how to handle dimensions, what level of detail, how to treat the frame, cushions and legs. **That symmetry is what makes the comparison fair, and he checks for it rather than assuming it.**
- **→ The transferable rule: when comparing two agents on a generative task, hold the prompt AND the clarification round constant, and verify the clarifications matched before comparing the outputs.** A different question asked is a different task performed.
- **⚠️ This is the FOURTH independent appearance of the interview-me prompting pattern in this source class** - after Меркулов, Urban Decoders and `E-ECbD14g_8`. **Here it is used as an experimental control rather than as a prompt-quality technique**, which is a genuinely different application of it.

## ⚠️ Durable Facts - How to Judge Generated Geometry

- **Inspect the HIDDEN GEOMETRY, not the silhouette** - *"sometimes I feel like it's better to look at the hidden geometry in here cuz it can give you an idea of how this is created."* **→ Judge generated geometry by its construction, not its appearance.** A shape that looks right and is built wrong will fail at the next edit.
- **The defect he names is the same family seen across this whole batch**: arms built as cylinders *"still kind of intersecting with the model"* - **non-merged, interpenetrating solids.** Same class as the wall corners that *"don't really merge together"* in [[_Sources/YT_X1lnTEpy6PQ_sketchupessentials_claude_connector_day_one|X1lnTEpy6PQ]], and precisely what `tools/layout/check_wall_junctions.py` exists to reject.
- **Note the architecture differs from that of `X1lnTEpy6PQ`**: this test drives SketchUp through an **MCP connection** (closed loop), where the connector video used file generation (open loop). **Both paths exist for the same application** - see [[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]].

## Confidence & Evidence Notes

- **`single-account`**; a single unreplicated head-to-head on one object.
- **⚠️ No output of this test is routed as a capability finding.** The method is routed; the result is not.
- **ASR**: good. **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- `18_Digital_Toolchain/analysis/Agent_Connected_CAD.md` - the comparison discipline, hidden-geometry inspection, and the non-merged-solid defect family.
- **5b**: no prices; no conversion owed.
