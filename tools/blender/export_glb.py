"""Export a variant's IFC to GLB - the walkable/3D view of the one model.

`00_Master/Model_and_Views.md` names `Blender / glb` as one of the views derived
from `model.ifc`. This is the generator for it, so the walkable view is a VIEW
and not a second model: it is regenerated from the IFC and never edited.

Runs inside Blender (`blender --background --python`), loads the IFC with
Bonsai, optionally paints each IFC class a flat colour, and exports one GLB.

WHY FLAT COLOUR AND NO TEXTURES
-------------------------------
`tools/blender/glb_material_probe.py` establishes, by parsing the exported GLB
rather than by looking at it, that a bare Principled BSDF base colour survives a
glTF export exactly (colour, roughness and metallic all arrive), while a
procedural node network is dropped - its material exports with a null
baseColorFactor. Sources processed 2026-09-16 say the same from three
directions, and add the price of the alternative: baking needs a UV map on every
object, Cycles, and one bake per channel. An IFC model out of Bonsai has no UV
maps.

So flat colour is free and textures are a modelling project. For the questions
this view exists to answer - does the passage past a lowered wall bed work, is
the clearance tolerable - flat colour is not a limitation, it is the point.
Keeping it untextured also keeps the file small enough to open in a browser,
which is the constraint the same sources put on the web route.

This writes only into the variant's own output directory, and never touches the
`.ifc` it reads. See the Ctrl+S warning in `00_Master/How_To_View_Outputs.md`:
this process is headless and saves no mainfile, so that hazard does not apply.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy

# Flat colours per IFC class. Chosen for legibility while walking, not realism:
# floors and ceilings recede, walls read as neutral, and the things you are
# judging clearance against (doors, furniture) stand out.
CLASS_COLOURS = {
    "IfcWall": (0.78, 0.76, 0.72, 1.0),
    "IfcWallStandardCase": (0.78, 0.76, 0.72, 1.0),
    "IfcSlab": (0.55, 0.52, 0.50, 1.0),
    "IfcDoor": (0.72, 0.45, 0.20, 1.0),
    "IfcWindow": (0.45, 0.65, 0.85, 1.0),
    "IfcFurnishingElement": (0.30, 0.55, 0.40, 1.0),
    "IfcColumn": (0.60, 0.58, 0.56, 1.0),
    "IfcBeam": (0.60, 0.58, 0.56, 1.0),
    "IfcStair": (0.65, 0.60, 0.45, 1.0),
    "IfcFlowTerminal": (0.85, 0.85, 0.88, 1.0),
    "IfcLightFixture": (0.95, 0.92, 0.75, 1.0),
    "IfcSanitaryTerminal": (0.90, 0.90, 0.92, 1.0),
}
DEFAULT_COLOUR = (0.70, 0.70, 0.70, 1.0)

# Excluded from the walkable view. IfcSpace is a room VOLUME, not a physical
# object: exported it fills every room with a solid block you cannot see past,
# which defeats the only purpose this view has. Translucency is not the fix -
# glTF needs alphaMode BLEND, and Blender 4.2+ renamed the material property
# that drives it, so the alpha silently arrived as 1.0 on the first run.
EXCLUDED_CLASSES = {"IfcSpace", "IfcOpeningElement"}


def _argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def enable_bonsai(site: Path | None) -> str:
    """Enable Bonsai however this Blender happens to expose it.

    It is installed here as an EXTENSION (``extensions/renovation_local/bonsai``),
    so the module name is ``bl_ext.renovation_local.bonsai`` - not ``bonsai``,
    which is the legacy add-on name and the first thing that fails.
    """
    if site:
        sys.path.insert(0, str(site.resolve()))
    attempts = [
        "bl_ext.renovation_local.bonsai",
        "bl_ext.user_default.bonsai",
        "bonsai",
    ]
    errors = []
    for module in attempts:
        try:
            bpy.ops.preferences.addon_enable(module=module)
            return "enabled:%s" % module
        except Exception as exc:  # noqa: BLE001 - reported, not swallowed
            errors.append("%s -> %s" % (module, exc))
    return "failed: " + " | ".join(errors)


def ifc_class_of(obj) -> str | None:
    """Bonsai names objects '<IfcClass>/<Name>'; fall back to a custom property."""
    for key in ("ifc_definition_id", "IfcClass", "ifc_class"):
        if key in obj:
            val = obj[key]
            if isinstance(val, str) and val.startswith("Ifc"):
                return val
    name = obj.name or ""
    if "/" in name and name.split("/", 1)[0].startswith("Ifc"):
        return name.split("/", 1)[0]
    return None


def flat_material(name: str, rgba) -> bpy.types.Material:
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if rgba[3] < 1.0:
        mat.blend_method = "BLEND"
    return mat


def drop_excluded() -> dict:
    """Remove non-physical classes before export. See EXCLUDED_CLASSES."""
    dropped: dict[str, int] = {}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        cls = ifc_class_of(obj)
        if cls in EXCLUDED_CLASSES:
            dropped[cls] = dropped.get(cls, 0) + 1
            bpy.data.objects.remove(obj, do_unlink=True)
    return dropped


def paint_by_class() -> dict:
    counts: dict[str, int] = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        cls = ifc_class_of(obj) or "unclassified"
        rgba = CLASS_COLOURS.get(cls, DEFAULT_COLOUR)
        mat = flat_material("FLAT_%s" % cls, rgba)
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        counts[cls] = counts.get(cls, 0) + 1
    return counts


def main() -> int:
    args = _argv_after_ddash()
    ifc_path = Path(args[0])
    out_glb = Path(args[1])
    out_json = Path(args[2])
    site = Path(args[3]) if len(args) > 3 and args[3] else None
    paint = not (len(args) > 4 and args[4] == "--no-paint")

    report: dict = {"ifc": str(ifc_path), "glb": str(out_glb)}

    # ORDER MATTERS. `read_factory_settings` resets preferences, which drops the
    # registered extension repository Bonsai lives in - the enable then fails with
    # "extension repository does not exist". So enable the add-on against the
    # profile's real preferences first, and clear the default scene by hand.
    report["bonsai"] = enable_bonsai(site)
    report["blender_version"] = bpy.app.version_string

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    try:
        bpy.ops.bim.load_project(filepath=str(ifc_path.resolve()))
        report["ifc_load"] = "ok"
    except Exception as exc:  # noqa: BLE001
        report["ifc_load"] = "failed: %s" % exc
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("EXPORT_FAILED " + str(out_json))
        return 2

    report["mesh_objects_loaded"] = len([o for o in bpy.data.objects if o.type == "MESH"])
    report["dropped_non_physical"] = drop_excluded()
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    report["mesh_objects_exported"] = len(meshes)

    # Apply scale on everything. The 2026-09-16 batch records this as the single
    # cheapest export-integrity step: an unapplied scale looks correct in the
    # viewport and "goes completely haywire" on export.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    if meshes:
        bpy.context.view_layer.objects.active = meshes[0]
        try:
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            report["scale_applied"] = True
        except Exception as exc:  # noqa: BLE001
            report["scale_applied"] = "failed: %s" % exc

    report["painted_by_class"] = paint_by_class() if paint else "skipped"

    out_glb.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(out_glb),
        export_format="GLB",
        use_selection=False,
        export_apply=True,
        export_yup=True,
    )
    report["glb_bytes"] = out_glb.stat().st_size if out_glb.exists() else None

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("EXPORT_WROTE " + str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
