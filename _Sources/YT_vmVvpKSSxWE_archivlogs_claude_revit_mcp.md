---
source_type: video transcript (architecture channel, setup tutorial plus a capability demo)
source_url: https://www.youtube.com/watch?v=vmVvpKSSxWE
video_id: vmVvpKSSxWE
transcript_file: _Archive/processed_sources/20260913_archivlogs_claude_revit_mcp_20c67fb0.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026-05-19 (confirmed via yt-dlp metadata, upload_date=20260519)
channel: Archi Vlogs
source_title: "I Connected Claude AI to Revit - The Results Scared Me"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 4
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Archi Vlogs: Agent-Driven Revit Models From a Plan, But Cannot Plan (YouTube vmVvpKSSxWE)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️ Partial extraction - the demo verdict is discarded, the observed failures are kept

**Half this video is install steps (pyRevit, its MCP extension, the Claude Desktop connector config) and half is a capability demo with subjective reactions** - the title promise ("the results scared me"), a career-anxiety close, and repeated subscribe requests. **Per the standing rule, the capability verdict is discarded.** What is kept is the architecture and, more usefully, **the specific ways it failed on camera.**

## Durable Facts - The Integration Path

- **The chain, named concretely**: the **pyRevit** plugin, then an MCP extension installed from its extensions list (a "Revit MCP Python" / "MCP server for Revit" pair), then the **Claude Desktop** developer config pointing at the pyRevit extension path, then the connector appears in Claude. **Claude must be fully quit from the tray and Task Manager, not just closed**, for config changes to take.
- `ASR-uncertain` on exact package names, and **install steps date fast - recorded as a route that exists, not as instructions to follow.**

## ⚠️⚠️ Rules / Heuristics - What It Could and Could Not Do

**The demo is the valuable part precisely because it fails visibly, and the failures are all of one kind.**

**It succeeded at**: creating walls from a drafted plan, adding floors per room, placing doors, **naming and numbering every room**, and adding room tags and windows on the sample project. His own comparison: "doing a better job than a fresher who has just started using Revit."

**It failed at**: producing a plan **closed on all sides** with no circulation; **forgetting a wall** ("it forgot to add a wall over here for some reason"); and **placing a door to a bedroom that is outside the building.**

- **⚠️⚠️ His own conclusion is the finding, and he states it plainly: "it cannot plan right now. What it can do is basically create a model from your existing floor plans."**
- **→ The generalisation worth keeping: an agent-connected CAD is a MODELLING ACCELERATOR from a plan that already exists, not a space planner.** Every failure is a *spatial-logic* failure - connectivity, enclosure, adjacency - while every success is a *transcription* success.
- **⚠️ This corroborates, from a completely different tool, the rule already recorded in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7 that an agent generating building geometry silently supplies what you did not specify.** Here it supplied a door location and omitted a wall, and nothing flagged either. **Directly relevant to this project v0 route, which is to model from the printed dimension strings rather than to ask an agent to design.**

## Confidence & Evidence Notes

- **`single-account`**, one session, one operator, no repetition.
- **ASR**: "Cloud"/"Clawd" for Claude throughout; package names uncertain.
- **⚠️ The failures are more durable than the successes.** A model generation may fix the missing wall; the *category* of failure - spatial logic versus transcription - is the part likely to persist, and it is what is routed.
- **No regulatory content.**

## Recommended Downstream Routing

- `18_Digital_Toolchain/analysis/Agent_Connected_CAD.md` (NEW PAGE) - the integration path, and the modelling-accelerator-not-planner finding.
- **5b**: no prices; no conversion owed.
