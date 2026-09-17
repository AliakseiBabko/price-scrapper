---
source_type: video transcript (Technical BIM data extraction tutorial)
source_url: https://www.youtube.com/watch?v=fUlDzxSDOls
video_id: fUlDzxSDOls
transcript_file: _Archive/processed_sources/20260917_spbproduction_bonsai_spreadsheet_qto_schedule_a9e7aa94.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2023-11-06 (confirmed via yt-dlp metadata)
channel: SPB Production
source_title: "Extract Data from IFC file | Create Door Schedule with Bonsai BIM Spreadsheet Tool"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 6
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Tom (SPB Production): Bonsai Spreadsheet Tool for IFC Quantity Takeoff, Property Query Syntax, and Quotation Trap on Spaced Psets (YouTube fUlDzxSDOls)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
A 16.9-minute comprehensive tutorial by Tom (SPB Production) demonstrating how to extract data from an IFC model and generate formatted component schedules and quantity takeoffs using Bonsai's built-in **Spreadsheet Import/Export** tool. `promotional_ratio: none`.

## 1. The Spreadsheet tool architecture in Bonsai
- Located under the **Quality and Coordination** tab → **Spreadsheet** panel.
- Tom shows that the tool reads loaded IFC geometry and metadata in memory, exporting directly to tabular formats: `.ods` (OpenDocument Spreadsheet), `.xlsx`, or `.csv`.
- Export can include or exclude `GlobalId` via a dedicated toggle (`include_global_id`).

> **→ Answers Open Problem 11 (Quantity take-off from IFC).** Demonstrates the standard practitioner path for extracting schedules from an IFC model without writing custom Python code.

## 2. Query syntax for attributes vs property sets
- **Class filter**: e.g. `IfcDoor`.
- **Attribute syntax**: attributes on the entity itself are accessed directly (e.g. `ObjectType`, `Name`).
- **Property Set syntax**: properties within property sets are queried using dot-notation: `Pset_Name.PropertyName` (e.g. `Pset_DoorCommon.FireRating`).

## 3. ⚠️ Critical failure trap: property sets containing spaces MUST be quoted
- Tom encounters an unhandled export error when querying custom property sets: if a property set name or property name contains spaces (e.g. `IFC Door Information`), entering it unquoted causes the spreadsheet export to fail immediately.
- **The fix**: the entire entity path or property set name must be wrapped in quotation marks: `"IFC Door Information".Function` or `"IFC Door Information"."Type Mark"`.

> **→ A precise parser rule for our tooling.** When authoring or querying IFC property sets via IfcOpenShell or Bonsai queries, spaces break unquoted dot-notation.

## 4. Grouping, counting, and aggregation mechanics
- By default, the tool outputs one row per instance occurrence in the building.
- To produce an aggregated schedule (e.g. door count by type):
  1. Enable **Show grouping** and set the key column to `Group` (e.g. grouped by `Door Type`).
  2. Add an attribute column with `.count` suffix (e.g. `"IFC Door Information"."Type Mark".count`).
  3. Set the grouping function on the count column to `sum`.
  4. Enable **Show summary** with `sum` to calculate grand totals across all rows.

> **→ Corroborates [[_Sources/YT_94kAIpRnhcY_dudeblender_floor_plan_series|94kAIpRnhcY]] and the BOM data model**: component schedules must separate instance enumeration from type aggregation and count summation.

## What was deliberately NOT extracted
- Formatting cells inside LibreOffice Calc.
- No prices or renovation costs.

## Source Notes
Tom, SPB Production (YouTube), 2023-11-06, 16.9 min, read in full. Claims are this presenter's, as opinion.
