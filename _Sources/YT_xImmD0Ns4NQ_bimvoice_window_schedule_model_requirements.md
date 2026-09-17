---
source_type: video transcript (openBIM / Bonsai BIM tutorial on IFC schedule extraction and QTO)
source_url: https://www.youtube.com/watch?v=xImmD0Ns4NQ
video_id: xImmD0Ns4NQ
transcript_file: _Archive/processed_sources/20260917_bimvoice_window_schedule_model_requirements_1afe77df.txt
fetched: 2026-09-17 via youtube-transcript-api (en manual captions, ORIGINAL language verified)
upload_date: 2025-12-08 (confirmed via yt-dlp metadata)
channel: BIMvoice
presenters: Stefan Catargiu (BIMvoice)
scope: General openBIM practitioner practice (tabular window schedules, QTO aggregation, IFC attribute vs Pset syntax)
tags: [Digital Toolchain, Bonsai BIM, QTO, Window Schedule, Spreadsheet, IfcWindow, ObjectType, Pset]
fact_yield: 6
promotional_ratio: low (educational tutorial)
---

# Window Schedule Extraction and Model Schema Requirements in Bonsai BIM

Stefan Catargiu (BIMvoice) demonstrates how to extract a consolidated window schedule and quantity take-off directly from an IFC model using Bonsai BIM's Spreadsheet Import/Export tool.

## Key Practitioner Claims & Mechanisms

1. **Entity class filtering**:
   The schedule query requires specifying an IFC entity filter (`IfcWindow`) under the search group to isolate window occurrences from the spatial model.

2. **The Type / `ObjectType` requirement for count aggregation**:
   To produce a consolidated schedule showing item counts (`count()`) per window variant rather than a flat list of every individual window instance, the schedule **must group by `ObjectType`** (or `Type.Name`). If a model contains instances with no assigned types or empty `ObjectType` strings, grouping cannot aggregate identical windows, producing individual rows of count 1.

3. **Direct IFC geometric attributes**:
   Direct entity attributes are queried by their exact schema names without prefixes: `OverallHeight` and `OverallWidth`. These pull directly from the `IfcWindow` entity definition (or the type's defining parameters).

4. **Direct attribute vs. Property Set dot syntax**:
   Direct IFC attributes (`Name`, `Tag`, `OverallHeight`, `OverallWidth`) are accessed by plain attribute name. In contrast, property set values require strict dot notation: `PropertySetName.PropertyName` (e.g. `Pset_WindowCommon.ThermalTransmittance`, `Pset_WindowCommon.IsExternal`). Syntax is strictly case-sensitive.

5. **Aggregation functions (`count`)**:
   Adding a column with the `count` function automatically counts occurrences within each grouped `ObjectType`, allowing users to generate quantity summaries (e.g. Type A: 8 units, Type B: 35 units).

6. **Web UI preview before export**:
   Bonsai provides a browser-based preview mode ("load from memory") that allows modellers to test and refine column mappings, grouping rules, and sort orders in real time before writing the final schedule to `.csv` or `.ods`.

## Architectural Relevance

- **Answers Open Problem 11**: Proves that automated tabular schedule extraction requires models to carry explicit `ObjectType` or `IfcTypeObject` links.
- **Direct Guidance for Generator**: Because our `tools/ifc/model_from_resolved.py` currently emits instances with no `IfcWindowType` or `IfcDoorType`, any downstream QTO tool cannot group by type. Emitting `IfcWindowType` / `IfcDoorType` (or populating `ObjectType`) is mandatory for automated scheduling.
