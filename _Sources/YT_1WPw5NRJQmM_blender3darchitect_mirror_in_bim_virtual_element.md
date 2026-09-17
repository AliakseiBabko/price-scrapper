---
source_type: video transcript (BIM geometry and modeling tutorial)
source_url: https://www.youtube.com/watch?v=1WPw5NRJQmM
video_id: 1WPw5NRJQmM
transcript_file: _Archive/processed_sources/20260917_blender3darchitect_mirror_in_bim_virtual_element_be74f9c0.txt
fetched: 2026-09-17 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2026-06-17 (confirmed via yt-dlp metadata)
channel: Blender 3D Architect (Alan Brito)
source_title: "Blender's Mirror Doesn't Work for BIM — Use This Instead (Free)"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 5
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Alberto (Blender 3D Architect): Why buildingSMART/IFC Has No Mirrored Instances, Position Reflection vs. Geometric Inversion, and IfcVirtualElement (YouTube 1WPw5NRJQmM)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is
A 10.8-minute technical geometry tutorial by Alberto (architect, presenting on the Blender 3D Architect channel) explaining why standard 3D mirroring (`Ctrl+M` or Blender's Mirror Modifier) fails in BIM, why the IFC schema does not support mirrored instances, and how Bonsai's mirror tool uses `IfcVirtualElement`. `promotional_ratio: medium` (closing book/workshop pitches).

## 1. ⚠️ Why IFC has no "Mirrored Instance": semantic and physical asymmetry
- Alberto explains that in Blender or general 3D DCC tools, mirroring flips vertex coordinates across an axis (negative scaling / vertex reflection).
- In buildingSMART and IFC specifications, however, **there is deliberately no concept of a mirrored instance of a product**.
- **The architectural reason**: Real building products are physically asymmetric. For example, a chair with an adjustment lever on the left, a door with left-handed hinges, or a plumbing/electrical fixture layout cannot be "mirrored" in reality; a mirrored version is a completely different physical product/part with opposite handedness. If an instance carried a mirrored transformation, it would represent a manufactured object that does not exist.
- Therefore, IFC representations enforce valid right-handed coordinate systems and reject negative scale transforms on element occurrences.

> **→ Directly validates our project's geometry rules.** In this repository, `validate_services_observed.py` strictly refuses unflipped readings from mirrored flats, and `Geometry_Variance_Study.md` notes that mirrored survey flats cannot simply be inverted via coordinate negation. Alberto confirms that this is a foundational principle of openBIM semantics, not a repo-specific idiosyncrasy.

## 2. Bonsai's Mirror tool: Position reflection, NOT geometric flip
- Because IFC disallows negative coordinate scaling on instances, Bonsai's "Mirror" tool behaves completely differently from Blender's `Ctrl+M`:
  - It does **not** flip the mesh geometry.
  - It calculates the perpendicular distance from the selected object to a mirror plane and creates a duplicate instance placed at the symmetric distance on the opposite side.
  - The newly created instance retains its original orientation and handedness; any required re-orientation must be performed via explicit rotation (e.g. 180° rotation) or by assigning a distinct opposite-handed type.

## 3. The Mirror Plane requires an `IfcVirtualElement`
- Bonsai requires two objects to execute a mirror operation: the target object and a reference plane.
- The reference plane must be an IFC entity classified as `IfcVirtualElement` with specific local axis conventions (local Y pointing vertical, local Z pointing along the plane normal).
- Alberto notes that Bonsai by default always renders `IfcVirtualElement` in wireframe in the 3D viewport, preserving it as a non-physical reference object.

## What was deliberately NOT extracted
- 3D cursor placement keystrokes.
- The closing promotional block for technical drawing workshops and rendering books.

## Source Notes
Alberto, Blender 3D Architect (YouTube), 2026-06-17, 10.8 min, read in full. Claims are this presenter's, as opinion.
