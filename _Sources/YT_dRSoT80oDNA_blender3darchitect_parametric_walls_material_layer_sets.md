---
source_type: video transcript (openBIM / Bonsai BIM tutorial on parametric wall modeling and thickness management)
source_url: https://www.youtube.com/watch?v=dRSoT80oDNA
video_id: dRSoT80oDNA
transcript_file: _Archive/processed_sources/20260917_blender3darchitect_parametric_walls_material_layer_sets_8d216447.txt
fetched: 2026-09-17 via youtube-transcript-api (en auto-generated captions, ORIGINAL language verified)
upload_date: 2026-05-14 (confirmed via yt-dlp metadata)
channel: Blender 3D Architect
presenters: Alan Brito (Blender 3D Architect)
scope: General openBIM practitioner practice (parametric wall modeling, IfcMaterialLayerSet, thickness propagation)
tags: [Digital Toolchain, Bonsai BIM, Walls, Parametric, IfcWallType, IfcMaterialLayerSet, Thickness]
fact_yield: 6
promotional_ratio: medium (tutorial with workshop links)
---

# Parametric Walls and Material Layer Sets in Bonsai BIM

Alan Brito (Blender 3D Architect) demonstrates the wall modeling toolchain in Bonsai BIM, showing how wall types, thickness, height, and boundary extensions behave parametrically within native IFC4.

## Key Practitioner Claims & Mechanisms

1. **Wall Tool and Type Instantiation**:
   Bonsai provides a modal Wall Tool (`Shift+A`) that instantiates standard wall types (e.g. `Wall 200`, `Wall 100`) loaded from an IFC4 template. Modellers draw polylines by clicking endpoints or typing millimeter distances.

2. **Thickness governed by `IfcMaterialLayerSet`**:
   Wall thickness is not stored as an ad-hoc local mesh dimension. It is defined on the `IfcMaterialLayerSet` associated with the `IfcWallType`.

3. **Global thickness propagation across instances**:
   When a modeller edits the layer thickness of a material layer set (e.g. changing from 0.10 m to 0.25 m) and saves changes, all wall instances referencing that `IfcWallType` update their physical geometry across the entire project simultaneously.

4. **Extrusion height parametrization**:
   Wall height is driven by an `IfcExtrudedAreaSolid` extrusion parameter. Modifying the height value in the 3D viewport sidebar (e.g. from 3.0 m to 2.5 m) adjusts the solid extrusion without destructively modifying the underlying 2D footprint polyline.

5. **Wall-to-slab boundary extension**:
   The `extend height` operator automatically adjusts wall extrusion heights to match the bottom face of an intersecting slab or target 3D cursor datum.

6. **Plain IFC4 persistence**:
   Unlike Blender modifiers which collapse or fail on export, wall parameters (layer set thickness, extrusion height, material associations) are stored in standard IFC4 schema entities (`IfcWallType`, `IfcMaterialLayerSet`, `IfcExtrudedAreaSolid`), ensuring full round-trip preservation in external BIM tools.

## Architectural Relevance

- **Answers Open Problem 9 & Generator Design**: Clarifies that parametric wall thickness in openBIM belongs on `IfcMaterialLayerSet` attached to `IfcWallType`, linked via `IfcRelDefinesByType` and `IfcRelAssociatesMaterial`.
- Emitting concrete instances with uniform extrusion dimensions without types prevents global parameter propagation.
