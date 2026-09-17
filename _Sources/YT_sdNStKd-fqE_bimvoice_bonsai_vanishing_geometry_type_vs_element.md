---
source_type: video transcript (Practitioner troubleshooting and data modeling Q&A)
source_url: https://www.youtube.com/watch?v=sdNStKd-fqE
video_id: sdNStKd-fqE
transcript_file: _Archive/processed_sources/20260917_bimvoice_bonsai_vanishing_geometry_type_vs_element_f20ff131.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-11-12 (confirmed via yt-dlp metadata)
channel: BIMvoice
source_title: "BonsaiBIM Secrets: How to Stop Text and Geometry from VANISHING After Classification."
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 5
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Stefan Catargiu (BIMvoice): The Vanishing Geometry Trap (Type vs. Occurrence), GUI Crashes, Text-to-Mesh Prerequisite, and IfcAnnotation Viewer Omission (YouTube sdNStKd-fqE)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
An 11.2-minute practitioner troubleshooting video by Stefan Catargiu (BIMvoice) answering community inquiries about why Blender geometry and text disappear when assigned IFC classes in Bonsai. `promotional_ratio: low` (brief pitch for community kickstart challenge at the end).

## 1. The "Vanishing Geometry" trap: Type vs. Occurrence
- When assigning an IFC class to a Blender mesh object, the Bonsai UI presents a selector defaulting to **IFC Element Type** (`IfcElementType`) rather than **IFC Element** (`IfcElement`).
- When a user assigns a class with `Type` selected, the object disappears from the 3D viewport. Stefan explains the architectural reason: an IFC Type is an abstract definition in the project library, not a physical occurrence placed in a storey container (`IfcBuildingStorey`). The geometry is moved into the type definition and unlinked from the active scene.
- **The rule**: To keep an object visible and spatially placed in the 3D building model, it MUST be assigned as an `IfcElement` (occurrence instance).

> **→ Directly bears on IFC authoring.** In programmatic generation (via `ifcopenshell`), this corresponds to the critical distinction between creating an `IfcWallType` / `IfcDoorType` (which has no `IfcLocalPlacement` and no spatial containment) and instantiating an `IfcWall` / `IfcDoor` mapped to that type with an `IfcRelDefinesByType` relationship.

## 2. Active software crash on class assignment
- During the live demonstration, when Stefan selects a standard IFC element (`IfcFooting` pad footing) and clicks `Assign IFC Class`, **Bonsai crashes Blender immediately to desktop**. Stefan has to restart Blender and recreate the scene.

> **→ Explicit practitioner limitation recorded**: Bonsai exhibits live unhandled crashes during basic GUI entity classification tasks, even on simple primitive geometry.

## 3. Text objects MUST be converted to meshes before IFC classification
- In Blender, 2D/3D text objects are curve/font data blocks, not polygon meshes.
- Stefan demonstrates that attempting to assign an IFC class to a Blender text object fails or causes it to vanish. The text object must first be explicitly converted into a polygonal mesh (`Object → Convert to → Mesh`) before Bonsai can wrap it into an IFC entity representation.

## 4. Interoperability breakdown: `IfcAnnotation` unsupported in external viewers
- Stefan discusses assigning IFC classes to instructional text or 3D callouts: `IfcAnnotation` is the semantically correct IFC entity, but in practice, **almost no commercial or external IFC viewers render `IfcAnnotation` entities**.
- As a workaround to ensure 3D text labels remain visible across external BIM tools, practitioners convert text to meshes and classify them as `IfcBuildingElementProxy` with `PredefinedType = USERDEFINED` and name `Annotation`.

> **→ Stated industry limitation**: Downstream viewer toolchains fail to support native IFC annotation standards, forcing practitioners to corrupt the physical model with proxy solids just to display readable labels in 3D.

## What was deliberately NOT extracted
- Basic Blender shortcut explanations (`Shift+A`).
- Closing academy promotional pitch.

## Source Notes
Stefan Catargiu, BIMvoice (YouTube), 2025-11-12, 11.2 min, read in full. Claims are this presenter's, as opinion.
