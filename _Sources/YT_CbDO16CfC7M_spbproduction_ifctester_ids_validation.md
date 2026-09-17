---
source_type: video transcript (Technical openBIM validation tutorial)
source_url: https://www.youtube.com/watch?v=CbDO16CfC7M
video_id: CbDO16CfC7M
transcript_file: _Archive/processed_sources/20260917_spbproduction_ifctester_ids_validation_1b78a06c.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2026-02-05 (confirmed via yt-dlp metadata)
channel: SPB Production
source_title: "Use IFC Tester to Validate IFC against IDS (Information Delivery Specification)"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 6
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Tom (SPB Production): Client-Side IDS Validation with IFC Tester, GlobalId Failure Auditing, and Batch Multi-Model Checks (YouTube CbDO16CfC7M)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
A 6.8-minute demonstration by Tom (SPB Production) on validating IFC models against buildingSMART Information Delivery Specification (IDS) XML definitions using the open-source web application IFC Tester (`ifctester.org`, developed by Sayan J. Das). `promotional_ratio: none`.

## 1. Zero-installation, fully local in-browser execution
- Tom highlights that although `ifctester.org` is accessed via a web browser, after initial loading the application runs **100% locally on the client machine** (compiled client-side code). No model bytes or IDS schemas are transmitted to external servers, satisfying data privacy and confidentiality requirements.

> **→ Relevant to Open Problem 12 (Validation).** Demonstrates that standard buildingSMART IDS audits can be run in client environments without server infrastructure.

## 2. Detailed audit reporting keyed by `GlobalId`
- Tom shows the audit results for two test models (a spa building and a residential model). When a requirement fails—for example, wall types failing an attribute naming convention or prohibited `IfcBuildingElementProxy` entities existing—the tool exports an interactive HTML audit report.
- The exported HTML report specifies the exact failure reason per element, lists the element's `GlobalId`, and summarizes passed vs. failed requirements.
- Tom notes that this standalone HTML report is the practitioner standard for sending defect notices to model authors or contractors.

> **→ Directly matches this repo's gating philosophy.** In our repository, automated validators report actionable identifiers. An IDS report provides machine-readable and human-readable failure ledgers tied directly to `GlobalId`.

## 3. Tool limitation: in-browser display bug
- Tom points out an active bug in the IFC Tester web interface: the in-browser table for fine-grained per-type pass/fail results fails to populate, forcing the user to download the external HTML report to see which specific entities failed.

> **→ Stated tool limitation**: Browser-based UI reporting has active rendering glitches, making the exported HTML/data artefact the only dependable output.

## 4. Batch validation capabilities and constraints
- Multiple IFC files can be loaded concurrently into one session, and running the audit evaluates all loaded IFC files against the active IDS specification, producing separate reports per model.
- However, Tom notes an asymmetric constraint: while multiple IFCs can be audited against one IDS, **multiple IDS files cannot be run simultaneously against a model** in one click. The user must manually switch IDS tabs and re-trigger audits.

## What was deliberately NOT extracted
- General introductions to buildingSMART standards.
- No prices or regulatory material.

## Source Notes
Tom, SPB Production (YouTube), 2026-02-05, 6.8 min, read in full. Claims are this presenter's, as opinion. Real tool evaluation of `ifctester.org`.
