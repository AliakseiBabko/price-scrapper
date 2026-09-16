"""Answer one question deterministically: does a flat Principled BSDF base colour
survive a Blender -> GLB export?

Sources processed 2026-09-16 establish that a Blender SHADER NETWORK does not
survive a glTF export at all - it arrives blank, and the only universal carrier
is a baked image texture. None of them tests the case this project would
actually use: a plain Principled BSDF with a base colour and no node network,
which is the glTF-native PBR material. The wall-bed/clearance walkthrough only
needs flat colour, so whether that travels decides whether an untextured
walkable view is free or needs UV unwrapping and baking.

This runs inside Blender (`blender --background --python`), builds three cubes -
flat base colour, flat colour plus roughness/metallic, and a deliberately
PROCEDURAL node network as the negative control - exports one GLB, and writes
the result as JSON for the caller to assert against.

It asserts nothing itself. The verdict is computed by `glb_inspect.py` from the
exported file, so the check does not trust the exporter's own report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy


def _argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_cube(name: str, location: tuple[float, float, float]) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def flat_material(name: str, rgba, roughness=None, metallic=None) -> bpy.types.Material:
    """A bare Principled BSDF - the glTF-native case. No node network."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba
    if roughness is not None:
        bsdf.inputs["Roughness"].default_value = roughness
    if metallic is not None:
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def procedural_material(name: str) -> bpy.types.Material:
    """The NEGATIVE CONTROL: a noise texture driving base colour.

    This is the case the sources demonstrate arriving blank. If it survives,
    the probe itself is wrong and the flat result cannot be trusted either.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    noise = nt.nodes.new("ShaderNodeTexNoise")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def main() -> int:
    args = _argv_after_ddash()
    out_glb = Path(args[0])
    out_json = Path(args[1])

    reset_scene()

    cases = []

    a = make_cube("flat_colour", (0.0, 0.0, 0.0))
    a.data.materials.append(flat_material("MAT_flat_colour", (0.8, 0.1, 0.1, 1.0)))
    cases.append({"object": "flat_colour", "material": "MAT_flat_colour",
                  "kind": "flat_base_colour",
                  "expect_base_color_factor": [0.8, 0.1, 0.1, 1.0]})

    b = make_cube("flat_pbr", (2.0, 0.0, 0.0))
    b.data.materials.append(flat_material("MAT_flat_pbr", (0.2, 0.4, 0.9, 1.0),
                                          roughness=0.35, metallic=0.75))
    cases.append({"object": "flat_pbr", "material": "MAT_flat_pbr",
                  "kind": "flat_base_colour_plus_pbr",
                  "expect_base_color_factor": [0.2, 0.4, 0.9, 1.0],
                  "expect_roughness": 0.35, "expect_metallic": 0.75})

    c = make_cube("procedural", (4.0, 0.0, 0.0))
    c.data.materials.append(procedural_material("MAT_procedural"))
    cases.append({"object": "procedural", "material": "MAT_procedural",
                  "kind": "procedural_negative_control",
                  "expect_base_color_factor": None})

    out_glb.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(out_glb),
        export_format="GLB",
        use_selection=False,
        export_apply=True,
    )

    payload = {
        "blender_version": bpy.app.version_string,
        "glb": str(out_glb),
        "glb_bytes": out_glb.stat().st_size if out_glb.exists() else None,
        "cases": cases,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("PROBE_WROTE " + str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
