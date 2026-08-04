---
name: homestyler-cad-to-revit
description: "Workflow for processing Homestyler CAD exports and preparing them for Revit integration."
---

# Homestyler CAD to Revit Integration

**Purpose**: Establish a lightweight source-tracking workflow for Homestyler CAD exports (DWG/CTB/PNG), treating them as reference underlays for future Revit modeling.

## Workflow Rules

1. **Underlay Philosophy**: 
   - Treat Homestyler DWG files as a Revit underlay/reference, **not** native BIM.
   - Never claim native Revit walls/MEP elements were generated from the DWG unless a specific Revit add-in or Dynamo process actually created them.

2. **Inbox Retention**:
   - Keep files in `00_Inbox/cad/` until Revit verification is complete. Do not archive them immediately upon receipt.

3. **Revit Verification Process**:
   - Prefer **Link CAD** over Import CAD in Revit.
   - Verify units manually in Revit using at least one known apartment dimension (e.g., verifying a standard doorway width or overall wall length against the DWG measurement).

4. **Tracking and Archiving**:
   - Once Revit link/import has been confirmed and units checked, update the `00_Master/cad_sources.csv` file. 
   - Change the `status` column from `inbox` to `linked`, `imported`, `skipped`, or `failed` as appropriate.
   - Add verification outcomes (especially unit assumptions) to the `notes` column.
   - Only after verification and status update should the source files be moved to `90_Archive/homestyler_exports/`.

## Local CAD review and cleanup

- Autodesk DWG TrueView is installed locally and is the preferred Windows
  viewer for checking the original DWG and derived DXF artifacts.
- Never delete or overwrite the original Homestyler DWG. Noise removal must
  produce a derived, clearly named DXF under `data/cad/`.
- Select a repeated apartment instance using multiple control dimensions and
  topology: entrance opening, door leaf, hall depth, continuous perimeter,
  doors/windows, and room arrangement. Do not choose by X/Y position alone.
- Furniture, cabinets, symbols, and duplicate geometry outside the selected
  apartment crop are removable from the derived reference drawing. The result
  remains an underlay and requires visual review in DWG TrueView before BIM
  promotion.
