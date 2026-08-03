"""Build a visual technology-demonstrator scene from an IFC model.

This is deliberately project-neutral: it tests IFC import, viewport/render
presentation, measurement annotations, and switchable lighting scenarios.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def args_after_separator():
    values = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, required=True)
    parser.add_argument("--output-blend", type=Path, required=True)
    parser.add_argument("--render", type=Path, required=True)
    parser.add_argument("--scenario", choices=["daylight", "evening", "mixed"], default="mixed")
    return parser.parse_args(values)


def add_text(body: str, location: tuple[float, float, float], size: float = 0.25):
    curve = bpy.data.curves.new(f"label-{body}", type="FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.size = size
    curve.extrude = 0.005
    obj = bpy.data.objects.new(f"Label {body}", curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (0.0, 0.0, 0.0)
    return obj


def add_dimension(x1: float, x2: float, y: float, z: float, label: str):
    curve = bpy.data.curves.new(f"dimension-{label}", type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.008
    spline = curve.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (x1, y, z, 1.0)
    spline.points[1].co = (x2, y, z, 1.0)
    obj = bpy.data.objects.new(f"Dimension {label}", curve)
    bpy.context.collection.objects.link(obj)
    add_text(label, ((x1 + x2) / 2, y, z + 0.04), 0.18)


def add_area_light(name: str, location: tuple[float, float, float], energy: float, color: tuple[float, float, float]):
    data = bpy.data.lights.new(name, type="AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = 2.0
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (0.0, 0.0, 0.0)
    return obj


def point_camera(camera, target: Vector):
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()


def main() -> int:
    args = args_after_separator()
    sys.path.insert(0, str(Path("tools/blender/profile3/extensions/.local/lib/python3.13/site-packages").resolve()))
    bpy.ops.preferences.addon_enable(module="bonsai")
    loaded = bpy.ops.bim.load_project(filepath=str(args.ifc.resolve()))
    if "FINISHED" not in loaded:
        raise RuntimeError(f"Bonsai IFC load failed: {loaded}")

    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not mesh_objects:
        raise RuntimeError("IFC import produced no mesh objects")
    points = [obj.matrix_world @ Vector(corner) for obj in mesh_objects for corner in obj.bound_box]
    minimum = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    maximum = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    center = (minimum + maximum) / 2
    span = max(maximum.x - minimum.x, maximum.y - minimum.y, 1.0)

    # A top-oriented orthographic camera gives a useful apartment-plan view;
    # all imported geometry remains available for orbiting in the UI.
    camera_data = bpy.data.cameras.new("Demo camera")
    camera = bpy.data.objects.new("Demo camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (center.x, center.y, maximum.z + span * 1.35)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = span * 1.15
    point_camera(camera, center)
    bpy.context.scene.camera = camera

    if args.scenario == "daylight":
        world_strength, artificial = 0.8, 250.0
        light_color = (1.0, 0.95, 0.85)
    elif args.scenario == "evening":
        world_strength, artificial = 0.06, 900.0
        light_color = (1.0, 0.55, 0.25)
    else:
        world_strength, artificial = 0.35, 600.0
        light_color = (1.0, 0.72, 0.45)
    world = bpy.context.scene.world or bpy.data.worlds.new("Demo world")
    bpy.context.scene.world = world
    world.color = (world_strength, world_strength, world_strength)
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (world_strength, world_strength, world_strength, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = world_strength
    add_area_light("Artificial ceiling light", (center.x, center.y, maximum.z + 2.5), artificial, light_color)

    # Visual-only annotations for the current test; values are not QTO data.
    add_text(f"DEMO APARTMENT — {args.scenario.upper()}", (center.x, minimum.y - span * 0.08, maximum.z + 0.1), 0.32)
    add_dimension(minimum.x, maximum.x, minimum.y - span * 0.16, maximum.z + 0.1, f"overall proxy {span:.2f} m")
    add_text("Measurements: visual test annotations only", (center.x, maximum.y + span * 0.08, maximum.z + 0.1), 0.18)

    scene = bpy.context.scene
    available_engines = {item.identifier for item in scene.bl_rna.properties["render"].fixed_type.properties["engine"].enum_items}
    scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in available_engines else "BLENDER_EEVEE"
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(args.render.resolve())
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"
    args.output_blend.parent.mkdir(parents=True, exist_ok=True)
    args.render.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output_blend.resolve()))
    bpy.ops.render.render(write_still=True)
    print(f"DEMO_SCENE_READY {args.output_blend}")
    print(f"DEMO_RENDER_READY {args.render}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
