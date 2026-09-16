"""Build a VIEWING .blend from a variant's IFC, with chosen elements dropped.

The plain `model.blend` that `verify_environment.py` writes is the whole model,
which is correct and unusable for looking at: the two slabs cap the flat top and
bottom, and the eight `IfcSpace` room volumes fill every room with a solid block.
Opening it, you see a closed box.

This writes a sibling `.blend` with those dropped, so the walls, openings and
internal structure are actually visible. It is a VIEW, like the GLB and the
sheets - regenerated from `model.ifc`, never edited, never a source of truth.

    blender --background --python tools/blender/build_view_blend.py -- \
        <model.ifc> <out.blend> <report.json> <bonsai-site> \
        [--drop-class IfcSpace] [--drop-name "ceiling"] [--keep-spaces]

⚠️ OPEN THIS WITHOUT THE BONSAI PROFILE. Bonsai connects the `.blend` to the
`.ifc` it loaded, and then an ordinary Ctrl+S rewrites the MODEL - the hazard
recorded in `00_Master/How_To_View_Outputs.md` and left ungated in
`18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline` section 6. Dropping the
link at save time does not work (`bim.unload_project` removes the objects too,
saving an empty file), so the protection is at OPEN time: launch without
`BLENDER_USER_CONFIG` / `BLENDER_USER_EXTENSIONS` pointing at the profile, Bonsai
never loads, and a reflex save can only damage this rebuildable view.

The cost of that is real: without Bonsai nothing is clickable-for-data - no
phase on a wall, no area on a room. This file is for LOOKING at geometry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy


def _argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def enable_bonsai(site: Path | None) -> str:
    """See export_glb.py - the module name is `bl_ext.renovation_local.bonsai`,
    and enabling must happen before the scene is cleared."""
    if site:
        sys.path.insert(0, str(site.resolve()))
    errors = []
    for module in ("bl_ext.renovation_local.bonsai", "bl_ext.user_default.bonsai", "bonsai"):
        try:
            bpy.ops.preferences.addon_enable(module=module)
            return "enabled:%s" % module
        except Exception as exc:  # noqa: BLE001
            errors.append("%s -> %s" % (module, exc))
    return "failed: " + " | ".join(errors)


def ifc_class_of(obj) -> str | None:
    for key in ("ifc_definition_id", "IfcClass", "ifc_class"):
        if key in obj:
            val = obj[key]
            if isinstance(val, str) and val.startswith("Ifc"):
                return val
    name = obj.name or ""
    if "/" in name and name.split("/", 1)[0].startswith("Ifc"):
        return name.split("/", 1)[0]
    return None


def main() -> int:
    args = _argv_after_ddash()
    if len(args) < 4:
        print("VIEW_FAILED usage: <ifc> <out.blend> <report.json> <site> [--drop-class C] [--drop-name S]")
        return 2

    ifc_path = Path(args[0])
    out_blend = Path(args[1])
    out_json = Path(args[2])
    site = Path(args[3]) if args[3] else None
    rest = args[4:]

    drop_classes = {rest[i + 1] for i, a in enumerate(rest) if a == "--drop-class"}
    drop_names = [rest[i + 1].lower() for i, a in enumerate(rest) if a == "--drop-name"]

    report: dict = {
        "ifc": str(ifc_path),
        "blend": str(out_blend),
        "drop_classes": sorted(drop_classes),
        "drop_names": drop_names,
    }

    report["bonsai"] = enable_bonsai(site)
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    try:
        bpy.ops.bim.load_project(filepath=str(ifc_path.resolve()))
        report["ifc_load"] = "ok"
    except Exception as exc:  # noqa: BLE001
        report["ifc_load"] = "failed: %s" % exc
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("VIEW_FAILED " + str(out_json))
        return 2

    dropped: list[str] = []
    kept: list[str] = []
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        cls = ifc_class_of(obj) or ""
        lowered = obj.name.lower()
        if cls in drop_classes or any(s in lowered for s in drop_names):
            dropped.append(obj.name)
            bpy.data.objects.remove(obj, do_unlink=True)
        else:
            kept.append(obj.name)

    report["dropped"] = sorted(dropped)
    report["kept"] = sorted(kept)
    report["kept_count"] = len(kept)

    # NOT unloaded here: `bim.unload_project` removes the objects along with the
    # IFC link, which saves an empty file. The protection is at OPEN time - this
    # file must be opened WITHOUT the Bonsai profile environment variables, so
    # Bonsai never loads and a Ctrl+S cannot sync anything back to the .ifc.
    report["ifc_link"] = "retained in file; open without the Bonsai profile"

    out_blend.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out_blend.resolve()))
    report["blend_bytes"] = out_blend.stat().st_size if out_blend.exists() else None

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("VIEW_WROTE " + str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
