---
source_type: video transcript (openBIM / Bonsai BIM live session, practitioners discussing drawing internals, Revit migration, and MEP)
source_url: https://www.youtube.com/watch?v=RL3IAGeMi5s
video_id: RL3IAGeMi5s
transcript_file: _Archive/processed_sources/20260917_bimvoice_bonsai_drawings_internals_and_mep_void_27d4b11d.txt
fetched: 2026-09-17 via youtube-transcript-api (en auto-generated captions, ORIGINAL language verified)
upload_date: 2024-07-06 (confirmed via yt-dlp metadata)
channel: BIMvoice
presenters: Stefan Catargiu (BIMvoice), Lloyd Sark (IfcArchitect)
scope: General openBIM practitioner practice (2D drawing internals, SVG generation, annotation storage, native MEP limitations)
tags: [Digital Toolchain, Bonsai BIM, 2D Drawings, SVG, IfcAnnotation, MEP, System Flow, OpenBIM]
fact_yield: 6
promotional_ratio: low (educational live practitioner Q&A)
---

# Bonsai BIM Live: 2D Drawing Tools Under the Hood and the MEP Reality

Stefan Catargiu (BIMvoice) hosts Lloyd Sark (IfcArchitect) in an educational live practitioner session exploring Bonsai BIM's 2D drawing pipeline, Revit-to-Bonsai migration, annotation synchronization, and native MEP authoring.

## Key Practitioner Claims & Mechanisms

1. **How 2D drawings work under the hood in Bonsai**:
   Bonsai creates an IFC camera/drawing entity (`IfcCamera` / view context), slices 3D model geometry across a defined cut plane, and generates 2D vector geometry directly into `.svg` files located in a project `drawings/` folder. Linework styling (cut lines, projection lines, fills) is governed by an external CSS stylesheet (`style.css`).
   > *"It will create this folder for you called drawings. This is where it actually stores the drawings as SVGs... We don't have to open Bonsai to edit or view the SVG... My CSS file is very complicated at this point."* [Lloyd Sark]

2. **IFC data storage vs. draw-time computation**:
   2D annotations (dimensions, tags, detail lines, fill regions) are persisted directly in the IFC model as `IfcAnnotation` entities associated with specific drawing views. However, the projected linework of building elements (walls, slabs, doors) is **not** stored as static 2D vector geometry in the IFC file; it is computed dynamically at draw time from the 3D meshes.

3. **The MEP functionality void in Bonsai**:
   When asked about native MEP (mechanical, electrical, plumbing) authoring in Bonsai, Lloyd Sark explicitly reports that native MEP modeling is currently ineffective and broken in production:
   > *"The MEP functionality is not as good modeling wise as the general ones... If you want to get the actual data, the MEP elements are not that effective. Audit editing it is good if you have a file coming in from somewhere else. But doing it natively at the moment, there's a few issues with the system flow basically. When you do pipes, when you do connections, when you do HVAC for instance, it has a lot of misunderstandings when you model it out. To show you here, it would just be me showing you where it's not working basically."* [Lloyd Sark]

4. **2D drafting as the necessary stopgap for discipline sheets**:
   Because 3D MEP modeling lacks working system flows and connection logic in Bonsai, openBIM practitioners do **not** generate 2D electrical or plumbing sheets from 3D distribution elements. Instead, they cut the architectural model and draft 2D annotations (electrical and plumbing symbols, circuits, lines) as an overlay:
   > *"The nice thing about drawing work, and I know that sounds not great, is that you can make everything correct using the 2D elements... The drawing becomes a stop gap for fixing any issues. And the same thing happens in Revit: people use fill regions and lines to draw in things that just don't want to fit together."* [Lloyd Sark]

5. **Multi-discipline drawing coordination across plans**:
   Lloyd Sark breaks down an architectural drawing set into individual discipline overlays on a single geometry cut:
   > *"Typically for a plan for instance you would do: an existing plan, a demolition plan, a new plan, doing a furniture layout, doing electrical layouts, doing a plumbing layout, doing a stormwater layout — right? It is all the same plan with different 2D information on it."*
   Bonsai provides an operator (`copy annotation to drawing`) to copy 2D elements across drawing views without redrawing shared dimension chains.

6. **Library types vs. raw occurrences**:
   Catargiu and Sark emphasize that all reusable assets (furniture, structural steel, fixtures) must be defined as `IfcTypeObject` (e.g. `IfcBeamType`, `IfcFurnishingElementType`) rather than raw occurrences. Loading raw occurrences balloons file size and prevents global attribute inheritance.

## Architectural Relevance

- **Answers Open Problem 7**: Closes the question of how 2D discipline sheets are generated in openBIM practice. Practitioners **do not** generate MEP drawings from 3D conduits, pipes, or wires; they slice the architectural geometry and draft 2D symbols and linework as an `IfcAnnotation` overlay.
- **Corroborates Open Problem 2 & 3 Void**: Directly confirms from the leading Bonsai drawing practitioner that native MEP modeling in Bonsai is unstable and unusable for system flows.
