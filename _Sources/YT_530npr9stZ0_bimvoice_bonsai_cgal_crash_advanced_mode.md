---
source_type: video transcript (Software troubleshooting and geometry kernel mechanics)
source_url: https://www.youtube.com/watch?v=530npr9stZ0
video_id: 530npr9stZ0
transcript_file: _Archive/processed_sources/20260917_bimvoice_bonsai_cgal_crash_advanced_mode_3ac2f2d2.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-10-22 (confirmed via yt-dlp metadata)
channel: BIMvoice
source_title: "BonsaiBIM Keeps Crashing When Loading IFC? Try This Fix!"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 4
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Stefan Catargiu (BIMvoice): Geometry Kernel Crash on IFC Import (CGAL vs. Open Cascade) and Advanced Mode Selective Loading (YouTube 530npr9stZ0)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
A 4.4-minute technical troubleshooting video by Stefan Catargiu (BIMvoice) documenting an acute crashing bug in Bonsai during IFC model import, diagnosed with IfcOpenShell lead developer Dion Moult. `promotional_ratio: none`.

## 1. The CGAL geometry kernel crash bug
- Stefan reports that opening complex IFC models in Bonsai was consistently causing Blender to crash to desktop immediately upon file load.
- Working directly with Dion Moult, the root cause was identified inside the geometry processing backend:
  - By default, Bonsai uses a hybrid geometry library combining **CGAL** (Computational Geometry Algorithms Library) and **Open Cascade** (OCCT).
  - The CGAL kernel implementation suffered from severe stability bugs (particularly acute on ARM64 / Apple Silicon macOS, though kernel bugs can affect other platforms).
  - Any model containing geometry processed through the faulty CGAL code path crashed Blender instantly.

## 2. The workaround: Advanced Mode and switching to Open Cascade
- To bypass the crash, Stefan details the required workflow:
  1. In `File → Open IFC Project`, check the **Enable Advanced Mode** checkbox before opening the file.
  2. In the exposed advanced settings, locate the **Geometry Library** selector.
  3. Change the kernel from the default CGAL hybrid to pure **Open Cascade**.
- With Open Cascade selected, the identical IFC models loaded cleanly without crashing.

> **→ Directly addresses §4.4 (Bonsai stability and kernel limitations).** Documents that Bonsai's default geometry engine can suffer fatal crashes on valid IFC geometry, and proves that Open Cascade is the stable fallback kernel.

## 3. Selective loading to manage model weight
- Advanced Mode also exposes selective loading options: modellers can filter by IFC classes, element types, or spatial decomposition (e.g. loading a single building storey rather than the whole project). This provides a memory management tool when inspecting large IFC deliverables.

## What was deliberately NOT extracted
- General introductory remarks.

## Source Notes
Stefan Catargiu, BIMvoice (YouTube), 2025-10-22, 4.4 min, read in full. Claims are this presenter's, as opinion. Technical diagnosis confirmed by Dion Moult.
