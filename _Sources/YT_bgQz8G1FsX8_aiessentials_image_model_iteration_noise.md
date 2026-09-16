---
source_type: video transcript (practitioner testing a new image-generation model release against the vendor's own claims, for interior/architectural iteration)
source_url: https://www.youtube.com/watch?v=bgQz8G1FsX8
video_id: bgQz8G1FsX8
transcript_file: _Archive/processed_sources/20260916_aiessentials_image_model_iteration_noise_2a99960a.txt
fetched: 2026-09-16 via youtube-transcript-api (en - ORIGINAL language, confirmed by yt-dlp probe)
upload_date: 2026-09-15 (from the yt-dlp sidecar, --fetch-upload-date; actually run)
channel: The AI Essentials / Justin
source_title: "GPT Images 2.5 is Better - But THIS Still happens"
language: en (original)
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / Concept and Visualisation`)
fact_yield: 8
promotional_ratio: low-medium - he tests the vendor's published claims one by one and reports where they fail, including a failed final take
corroborates_existing: true
contradicts_existing: false
region: n/a - software capability
---

# Source Note - ⚠️ The edit-drift problem is largely solved; the ITERATION-NOISE problem is not (YouTube bgQz8G1FsX8)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none)

⚠️ **Same channel as the SketchUp MCP tutorial in this batch, and as `T45kiCGvCQs` already in the vault.** **Taken because [[18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation|the visualisation page]] records non-destructive editing as the technique that carries, and this tests exactly that claim on a new release.**

## ⚠️⚠️ 1. THE FINDING — which of the two failure modes got fixed, and which did not

**He separates two things the vault has treated together, and the separation is the value:**

| Failure mode | Verdict on the new release |
| :--- | :--- |
| **Edit LOCALITY** — an edit changing unrelated parts of the scene, camera position drifting between turns | **⚠️⚠️ MATERIALLY IMPROVED.** *"The way that it's maintaining the camera location when you make changes and not changing any other elements in the scene is very, very good. That is a huge step forward."* |
| **⚠️⚠️ ITERATION NOISE** — texture noise accumulating across successive edits | **NOT FIXED.** *"The noise issue is still a big problem for me."* |

**And he names precisely why the second one is the binding constraint for design work, in the exact workflow this project would use:**

> *"A lot of the time what I'm doing is I'm iterating — what if we looked at a wall panel? What if we looked at a wall tile? What if we had a different carpet? What if we had a different piece of furniture in here? And when you're getting that noise creeping in over and over again, that's a real problem, because I need it to stay consistent in a way where I'm not losing the visual fidelity of the elements in there."*

> **→ ⚠️⚠️ THIS IS THE RIGHT DISTINCTION AND THIS VAULT DID NOT HAVE IT.** **Edit locality determines whether ONE edit is usable. Iteration noise determines whether a SEQUENCE of edits is usable — and option exploration is inherently a sequence.**
>
> **→ The practical rule that follows: for a finish comparison, generate each option from the SAME base image in a fresh turn, rather than chaining edits one on top of another.** **Chaining accumulates noise; branching from a fixed base does not.** ⚠️ **That is inference from his account, not his stated advice — flagged as such — but it follows directly from the failure he describes and it costs nothing to adopt.**
>
> ⚠️ **It also strengthens what the visualisation page already records as the technique that carries: keep the AUTHORED artefact as the base and edit non-destructively from it. The noise finding says why that matters beyond tidiness — the base does not degrade, and every option is one generation away from it.**

## ⚠️ 2. Secondary observations

- **Latency claimed down by up to 50%** by the vendor; he accepts it as plausible and welcome — *"I feel like I'm doing a lot of waiting between different image iterations"* — but does not measure it. **Vendor claim, unverified, recorded as such.**
- **⚠️ Claims about "better from reference photos" and "more natural lighting and textures" he explicitly declines to verify** — *"that's very difficult for me to test."* **Worth noting a tester who says which claims he cannot check rather than rating everything.**
- **⚠️ Background removal and transparency disappointed him, and his final take FAILED** — *"I didn't really feel like I got a super good result… it failed on my final take."* **A reported failure in a review of a product he is broadly positive about.**
- **Templates plus supplied data performed well** — a preset layout with real data placed accurately onto an image. ⚠️ **Adjacent to this project only via sheet/board production; not a modelling capability.**
- **⚠️ A sketch-to-render input path exists** (draw, send, get a render back). **His own verdict: a nice idea he will not use day-to-day, and clunky on a computer as opposed to a tablet.** **Recorded as a capability that exists, with a practitioner's unenthusiastic verdict attached.**

## Routing

- §1 → [[18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation|AI for Concept and Visualisation]], into the non-destructive-editing section
- §2 → same page, as minor observations

## What was NOT taken

- Version numbers and the vendor blog post's unverified claims as facts.
- The template/flyer material, which is outside this project's use.
- **Nothing routed to `16_Legal_and_Regulations/`** — no regulatory claim is made.
