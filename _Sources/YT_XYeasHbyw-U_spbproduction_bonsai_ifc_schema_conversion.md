---
source_type: video transcript (Bonsai BIM technical workflow demonstration)
source_url: https://www.youtube.com/watch?v=XYeasHbyw-U
video_id: XYeasHbyw-U
transcript_file: _Archive/processed_sources/20260917_spbproduction_bonsai_ifc_schema_conversion_cd618e56.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2024-09-20 (confirmed via yt-dlp metadata)
channel: SPB Production
source_title: "How to Convert IFC File with Bonsai BIM | Upgrade IFC 2x3 to IFC 4.0 | IFC 4.0 to IFC 4.3"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 5
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Tom (SPB Production): IFC Schema Upgrades (2x3 → 4.0 → 4.3), IfcPatch Migration Recipes, and Downgrade Loss to Proxy (YouTube XYeasHbyw-U)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
A concise 6.7-minute demonstration by Tom (SPB Production) showing the exact mechanism Bonsai uses to upgrade IFC schemas (IFC 2x3 to IFC 4.0, and IFC 4.0 to IFC 4.3) and downgrade schemas (IFC 4.0 to IFC 2x3) using the `IfcPatch` Migrate recipe. `promotional_ratio: none`.

## 1. Upgrade mechanism in Bonsai: GUI trigger and file generation
- Tom demonstrates that upgrading an IFC schema in Bonsai does not require opening the project file into the 3D viewport. In the `File → Open IFC Project` dialog, selecting an IFC 2x3 file surfaces an automated `Upgrade to IFC4` button; selecting an IFC 4.0 file surfaces an `Upgrade to IFC4x3` button.
- The upgrade runs in the background (taking 1–2 minutes on a small building model) and produces a brand-new file on disk suffixed with the schema name (e.g. `<Project>_IFC4.ifc`), leaving the original file intact.

> **→ This addresses Open Problem 8 (IFC4 vs IFC4.3).** The export/upgrade path from IFC4 to IFC4.3 is built directly into Bonsai's file handler, creating a distinct upgraded file rather than modifying in place.

## 2. Arbitrary migration and downgrades use the `IfcPatch` "Migrate" recipe
- To downgrade an IFC file (e.g. from IFC 4.0 back to IFC 2x3), Tom shows that the Open dialog button is insufficient; the practitioner must go to the **Quality and Coordination** tab → **Patch** panel → select the **Migrate** recipe.
- In Tom's workflow, `IfcPatch` takes an input IFC, an output destination path, and the target output schema (`IFC2X3`), then executes the schema migration script headlessly.

> **→ Under the hood, Bonsai's schema upgrade and downgrade tools are wrappers around `IfcPatch` migration scripts.** For our code-driven build chain, this confirms that schema conversion does not require Blender GUI interaction at all; it can be invoked directly via `ifcopenshell.util.schema` or `ifcpatch` recipes in Python.

## 3. Information loss and proxy conversion on downgrade
- Tom explicitly cautions that downgrading schemas is significantly less reliable than upgrading and incurs permanent semantic loss:
  1. Georeferencing metadata (`IfcMapConversion`, CRS data introduced in IFC4) does not exist in IFC 2x3 and is completely stripped.
  2. Any IFC entity or class introduced in IFC4 that has no direct equivalent in IFC 2x3 is translated into generic `IfcBuildingElementProxy`.
- Elements survive geometrically, but their rich BIM categorization and property sets are flattened or degraded.

> **→ Corroborates and sharpens the prior vault finding in [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|4JYFYvNg5Xk]]**: while an upgrade retains geometry, format conversion does not guarantee semantic integrity. When upgrading 2x3 to 4.0, entity types (`IfcDoorStyle`) can linger as deprecated survivors without becoming `IfcDoorType`; when downgrading 4.0 to 2x3, newer entities degrade into unclassified proxies.

## What was deliberately NOT extracted
- Blender UI theme setup and basic navigation.
- No prices or regional renovation figures.

## Source Notes
Tom, SPB Production (YouTube), 2024-09-20, 6.7 min, read in full. Claims are this presenter's, as opinion. Demonstrates real software mechanics in Bonsai 0.8.
