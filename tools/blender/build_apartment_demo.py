"""Build a room-by-room apartment design demonstrator from the provisional IFC."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def cli():
    values = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-blend", type=Path, required=True)
    parser.add_argument("--render-dir", type=Path, required=True)
    return parser.parse_args(values)


def material(name, color, metallic=0.0, roughness=0.55, emission=None):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 2.0
    return mat


def box(name, location, dimensions, mat, collection):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def cylinder(name, location, radius, depth, mat, collection):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def label(text, location, mat, collection):
    data = bpy.data.curves.new(f"label-data-{text}", type="FONT")
    data.body = text
    data.align_x = "CENTER"
    data.size = 0.22
    data.extrude = 0.004
    obj = bpy.data.objects.new(f"Room label {text}", data)
    collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(mat)
    return obj


def area_light(name, location, energy, color, collection):
    data = bpy.data.lights.new(name, type="AREA")
    data.energy = energy
    data.color = color
    data.shape = "DISK"
    data.size = 1.1
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    obj.location = location
    obj["design_role"] = "artificial_lighting_fixture"
    return obj


def wall_mount(name, room, side, fraction, z, mat, collection, dimensions=(0.12, 0.04, 0.18)):
    """Place a symbol flush with the room-side wall face."""
    x, y = room["x_m"], room["y_m"]
    w, d = room["width_m"], room["depth_m"]
    if side == "bottom":
        location = (x + w * fraction, y + 0.02, z)
        dims = dimensions
    elif side == "top":
        location = (x + w * fraction, y + d - 0.02, z)
        dims = dimensions
    elif side == "left":
        location = (x + 0.02, y + d * fraction, z)
        dims = (dimensions[1], dimensions[0], dimensions[2])
    elif side == "right":
        location = (x + w - 0.02, y + d * fraction, z)
        dims = (dimensions[1], dimensions[0], dimensions[2])
    else:
        raise ValueError(f"Unknown wall side: {side}")
    obj = box(name, location, dims, mat, collection)
    obj["wall_mounted"] = True
    obj["mounting_side"] = side
    obj["mounting_fraction"] = fraction
    return obj


def concealed_route(name, room, side, fraction, z, mat, collection, wall_objects):
    """Create a non-rendered ceiling-to-device route for viewport inspection."""
    x, y = room["x_m"], room["y_m"]
    w, d = room["width_m"], room["depth_m"]
    if side in {"bottom", "top"}:
        candidate = (x + w * fraction, y if side == "bottom" else y + d)
    else:
        candidate = (x if side == "left" else x + w, y + d * fraction)
    snapped, _ = snap_to_nearest_wall(candidate, (0.01, 0.01, 0.01), wall_objects, z)
    point = (snapped[0], snapped[1])
    curve = bpy.data.curves.new(f"{name}-data", type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.012
    spline = curve.splines.new("POLY")
    spline.points.add(2)
    spline.points[0].co = (point[0], point[1], 2.72, 1.0)
    spline.points[1].co = (point[0], point[1], z + 0.16, 1.0)
    spline.points[2].co = (point[0], point[1], z, 1.0)
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.hide_render = True
    obj["concealed_service"] = True
    obj["service_route"] = "ceiling-to-wall-device"
    return obj


def add_window_panes(mats, collection, wall_objects):
    """Replace opaque IFC window fills with uniform panes inside wall voids."""
    for source in [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and "ifcwindow/" in obj.name.lower()]:
        corners = [source.matrix_world @ Vector(corner) for corner in source.bound_box]
        low = Vector((min(p.x for p in corners), min(p.y for p in corners), min(p.z for p in corners)))
        high = Vector((max(p.x for p in corners), max(p.y for p in corners), max(p.z for p in corners)))
        center = (low + high) / 2
        span_x, span_y, span_z = high.x - low.x, high.y - low.y, high.z - low.z
        def wall_distance(wall):
            wall_points = [wall.matrix_world @ Vector(corner) for corner in wall.bound_box]
            wall_low = Vector((min(p.x for p in wall_points), min(p.y for p in wall_points)))
            wall_high = Vector((max(p.x for p in wall_points), max(p.y for p in wall_points)))
            closest = Vector((min(max(center.x, wall_low.x), wall_high.x), min(max(center.y, wall_low.y), wall_high.y)))
            return (center.xy - closest).length
        nearest = min(wall_objects, key=wall_distance)
        wall_corners = [nearest.matrix_world @ Vector(corner) for corner in nearest.bound_box]
        wall_low = Vector((min(p.x for p in wall_corners), min(p.y for p in wall_corners), min(p.z for p in wall_corners)))
        wall_high = Vector((max(p.x for p in wall_corners), max(p.y for p in wall_corners), max(p.z for p in wall_corners)))
        if span_x >= span_y:
            center.y = (wall_low.y + wall_high.y) / 2
            pane_dimensions = (span_x * 0.94, 0.025, span_z * 0.94)
        else:
            center.x = (wall_low.x + wall_high.x) / 2
            pane_dimensions = (0.025, span_y * 0.94, span_z * 0.94)
        pane = box(f"{source.name} transparent pane", center, pane_dimensions, mats["glass"], collection)
        pane["design_role"] = "transparent_window_pane_inside_native_opening"
        source.hide_render = True
        source.hide_viewport = True
        source.hide_set(True)


def add_wall_junctions(wall_objects, mat, collection):
    """Fill visible wall-end seams with small construction junction solids."""
    endpoints = []
    for wall in wall_objects:
        corners = [wall.matrix_world @ Vector(corner) for corner in wall.bound_box]
        low = Vector((min(p.x for p in corners), min(p.y for p in corners), min(p.z for p in corners)))
        high = Vector((max(p.x for p in corners), max(p.y for p in corners), max(p.z for p in corners)))
        if (high.x - low.x) >= (high.y - low.y):
            center_y = (low.y + high.y) / 2
            endpoints.extend([(low.x, center_y), (high.x, center_y)])
        else:
            center_x = (low.x + high.x) / 2
            endpoints.extend([(center_x, low.y), (center_x, high.y)])
    placed = set()
    for first in endpoints:
        for second in endpoints:
            if first == second or (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2 > 0.18 ** 2:
                continue
            location = ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2, 1.4)
            key = (round(location[0], 3), round(location[1], 3))
            if key in placed:
                continue
            placed.add(key)
            junction = box(f"Wall junction {key[0]} {key[1]}", location, (0.18, 0.18, 2.8), mat, collection)
            junction["construction_role"] = "overlapping_wall_corner_junction"


def extend_wall_mesh_endpoints(wall_objects, extension=0.075):
    """Extend actual wall host meshes at both local-X endpoints."""
    for wall in wall_objects:
        vertices = wall.data.vertices
        if not vertices:
            continue
        low = min(vertex.co.x for vertex in vertices)
        high = max(vertex.co.x for vertex in vertices)
        for vertex in vertices:
            if abs(vertex.co.x - low) < 1e-5:
                vertex.co.x -= extension
            elif abs(vertex.co.x - high) < 1e-5:
                vertex.co.x += extension
        wall.data.update()


def snap_to_nearest_wall(candidate, dimensions, wall_objects, z):
    """Snap a device to the nearest imported wall bounding face."""
    if not wall_objects:
        raise RuntimeError("No imported wall objects available for device mounting")
    cx, cy = candidate
    best = None
    for wall in wall_objects:
        corners = [wall.matrix_world @ Vector(corner) for corner in wall.bound_box]
        xmin, xmax = min(p.x for p in corners), max(p.x for p in corners)
        ymin, ymax = min(p.y for p in corners), max(p.y for p in corners)
        px = min(max(cx, xmin), xmax)
        py = min(max(cy, ymin), ymax)
        distance = (px - cx) ** 2 + (py - cy) ** 2
        if best is None or distance < best[0]:
            best = (distance, wall, (xmin, xmax, ymin, ymax))
    _, wall, (xmin, xmax, ymin, ymax) = best
    horizontal = (xmax - xmin) >= (ymax - ymin)
    if horizontal:
        face = ymax if cy >= (ymin + ymax) / 2 else ymin
        toward = 1.0 if cy >= (ymin + ymax) / 2 else -1.0
        location = (min(max(cx, xmin + dimensions[0] / 2), xmax - dimensions[0] / 2), face + toward * dimensions[1] / 2, z)
    else:
        face = xmax if cx >= (xmin + xmax) / 2 else xmin
        toward = 1.0 if cx >= (xmin + xmax) / 2 else -1.0
        location = (face + toward * dimensions[1] / 2, min(max(cy, ymin + dimensions[0] / 2), ymax - dimensions[0] / 2), z)
    return location, wall.name


def scene_bounds():
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    points = [obj.matrix_world @ Vector(corner) for obj in meshes for corner in obj.bound_box]
    low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return low, high


def add_room_content(rooms, design, collections, mats, wall_objects, door_objects, generate_electrical=True):
    furniture = collections["Furniture"]
    electrical = collections["Electrical Symbols"]
    lights = collections["Lighting Fixtures"]
    labels = collections["Room Labels"]
    plumbing = collections["Plumbing Fixtures"]
    concealed = collections["Concealed Services"]
    for room in rooms:
        name = room["name"]
        key = name.split(" ")[0].lower()
        x, y = room["x_m"], room["y_m"]
        w, d = room["width_m"], room["depth_m"]
        cx, cy = x + w / 2, y + d / 2
        label(name.replace(" (area proxy)", ""), (cx, cy, 0.04), mats["label"], labels)
        if key == "entrance":
            box("Hall bench", (x + w * 0.55, y + d * 0.28, 0.25), (1.1, 0.38, 0.5), mats["wood"], furniture)
            box("Hall wardrobe", (x + w * 0.18, y + d * 0.55, 0.95), (0.55, 1.3, 1.9), mats["wardrobe"], furniture)
            electrical_positions = [("bottom", 0.25), ("bottom", 0.78)]
        elif key == "living":
            box("Sofa", (x + w * 0.42, y + d * 0.48, 0.42), (2.1, 0.85, 0.8), mats["fabric"], furniture)
            box("Coffee table", (x + w * 0.42, y + d * 0.22, 0.22), (1.0, 0.55, 0.42), mats["wood"], furniture)
            box("Built-in wardrobe proxy", (x + w * 0.84, y + d * 0.6, 1.25), (0.45, 2.0, 2.5), mats["wardrobe"], furniture)
            electrical_positions = [("bottom", 0.18), ("bottom", 0.78), ("right", 0.62)]
        elif key == "bedroom":
            box("Bedroom bed", (cx, y + d * 0.55, 0.35), (2.0, 2.0, 0.55), mats["fabric"], furniture)
            electrical_positions = [("bottom", 0.25), ("bottom", 0.75)]
        elif key == "kitchen":
            box("Kitchen run", (x + w * 0.5, y + d * 0.85, 0.45), (w * 0.8, 0.48, 0.9), mats["cabinet"], furniture)
            box("Kitchen island", (cx, y + d * 0.43, 0.45), (w * 0.55, 0.5, 0.9), mats["cabinet"], furniture)
            electrical_positions = [("top", 0.2), ("top", 0.7), ("left", 0.25)]
        else:
            box(f"{name} vanity", (cx, y + d * 0.78, 0.4), (w * 0.55, 0.35, 0.8), mats["ceramic"], furniture)
            cylinder(f"{name} fixture", (cx, y + d * 0.35, 0.18), min(w, d) * 0.18, 0.12, mats["ceramic"], furniture)
            electrical_positions = [("top", 0.18)]
            plumbing_dims = (0.24, 0.04, 0.14)
            plumbing_candidate = (x + w * 0.5, y + d - 0.02)
            plumbing_location, plumbing_wall = snap_to_nearest_wall(plumbing_candidate, plumbing_dims, wall_objects, 1.15)
            plumbing_obj = box(f"{name} wall plumbing connection", plumbing_location, plumbing_dims, mats["plumbing"], plumbing)
            plumbing_obj["wall_mounted"] = True
            plumbing_obj["host_wall"] = plumbing_wall
            concealed_route(f"{name} concealed water drop", room, "top", 0.5, 1.15, mats["concealed"], concealed, wall_objects)
        if generate_electrical:
            for index, (side, fraction) in enumerate(electrical_positions, 1):
                x, y = room["x_m"], room["y_m"]
                w, d = room["width_m"], room["depth_m"]
                candidate = {
                    "bottom": (x + w * fraction, y),
                    "top": (x + w * fraction, y + d),
                    "left": (x, y + d * fraction),
                    "right": (x + w, y + d * fraction),
                }[side]
                def near_door(point):
                    for door in door_objects:
                        corners = [door.matrix_world @ Vector(corner) for corner in door.bound_box]
                        low = Vector((min(p.x for p in corners), min(p.y for p in corners)))
                        high = Vector((max(p.x for p in corners), max(p.y for p in corners)))
                        if low.x - 0.25 <= point[0] <= high.x + 0.25 and low.y - 0.25 <= point[1] <= high.y + 0.25:
                            return True
                    return False
                if near_door(candidate):
                    for alternate_side, alternate_fraction in [
                        ("bottom", 0.12), ("bottom", 0.88), ("top", 0.18),
                        ("top", 0.82), ("left", 0.25), ("right", 0.75)
                    ]:
                        alternate = {
                            "bottom": (x + w * alternate_fraction, y),
                            "top": (x + w * alternate_fraction, y + d),
                            "left": (x, y + d * alternate_fraction),
                            "right": (x + w, y + d * alternate_fraction),
                        }[alternate_side]
                        if not near_door(alternate):
                            side, fraction, candidate = alternate_side, alternate_fraction, alternate
                            break
                symbol_location, host_wall = snap_to_nearest_wall(candidate, (0.12, 0.04, 0.18), wall_objects, 1.05)
                symbol = box(f"{name} outlet {index}", symbol_location, (0.12, 0.04, 0.18) if side in {"bottom", "top"} else (0.04, 0.12, 0.18), mats["electrical"], electrical)
                symbol["design_role"] = "conceptual_electrical_symbol"
                symbol["wall_mounted"] = True
                symbol["host_wall"] = host_wall
                concealed_route(f"{name} concealed cable drop {index}", room, side, fraction, 1.05, mats["concealed"], concealed, wall_objects)
        fixture = area_light(f"{name} ceiling light", (cx, cy, 2.65), 550.0, (1.0, 0.72, 0.45), lights)
        fixture["room"] = name
        fixture["temperature_kelvin"] = 3000
        fixture["intensity_lumens_approx"] = 550


def configure_render(scene, low, high, render_path):
    center = (low + high) / 2
    span = max(high.x - low.x, high.y - low.y, 1.0)
    camera_data = bpy.data.cameras.new("Apartment demo camera")
    camera = bpy.data.objects.new("Apartment demo camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (center.x, center.y, high.z + span * 1.4)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = span * 1.18
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = camera
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = 1400, 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(render_path.resolve())


def set_scenario(scene, scenario):
    for obj in bpy.data.collections["Lighting Fixtures"].objects:
        obj.hide_render = False
        obj.data.energy = {"daylight": 300.0, "mixed": 650.0, "evening": 1100.0}[scenario]
        obj.data.color = {"daylight": (1.0, 0.92, 0.78), "mixed": (1.0, 0.72, 0.45), "evening": (1.0, 0.45, 0.18)}[scenario]
    sun = bpy.data.objects.get("Daylight sun")
    if sun:
        sun.hide_render = scenario == "evening"
        sun.data.energy = 2.0 if scenario == "daylight" else 0.8
    scene["active_lighting_scenario"] = scenario


def main():
    args = cli()
    sys.path.insert(0, str(Path("tools/blender/profile3/extensions/.local/lib/python3.13/site-packages").resolve()))
    bpy.ops.preferences.addon_enable(module="bonsai")
    if "FINISHED" not in bpy.ops.bim.load_project(filepath=str(args.ifc.resolve())):
        raise RuntimeError("Bonsai IFC import failed")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    rooms = manifest.get("rooms") or manifest["variants"][1]["rooms"]
    collections = {}
    for name in ["Furniture", "Electrical Symbols", "Lighting Fixtures", "Room Labels", "Plumbing Fixtures", "Concealed Services", "Wall Junctions"]:
        collections[name] = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collections[name])
    mats = {
        "wall": material("Demo wall junction", (0.32, 0.34, 0.37), roughness=0.8),
        "wood": material("Demo wood", (0.42, 0.16, 0.05)),
        "wardrobe": material("Demo wardrobe", (0.16, 0.24, 0.32), roughness=0.35),
        "fabric": material("Demo sofa fabric", (0.08, 0.22, 0.32)),
        "cabinet": material("Demo kitchen cabinet", (0.25, 0.42, 0.28), roughness=0.3),
        "ceramic": material("Demo ceramic", (0.75, 0.78, 0.8), roughness=0.2),
        "electrical": material("Demo electrical symbol", (0.9, 0.05, 0.03), emission=(0.5, 0.01, 0.0)),
        "plumbing": material("Demo plumbing connection", (0.05, 0.35, 0.9), metallic=0.15),
        "concealed": material("Demo concealed service route", (0.15, 0.45, 0.85), emission=(0.05, 0.15, 0.4)),
        "label": material("Demo labels", (0.95, 0.75, 0.1), emission=(0.5, 0.25, 0.0)),
        "glass": material("Demo window glass", (0.08, 0.35, 0.55), roughness=0.12),
        "door": material("Demo door leaf", (0.30, 0.10, 0.035), roughness=0.4),
    }
    glass_bsdf = mats["glass"].node_tree.nodes.get("Principled BSDF")
    if glass_bsdf:
        if glass_bsdf.inputs.get("Transmission Weight"):
            glass_bsdf.inputs["Transmission Weight"].default_value = 0.75
        glass_bsdf.inputs["Roughness"].default_value = 0.08
    window_panes = bpy.data.collections.new("Window Panes")
    bpy.context.scene.collection.children.link(window_panes)
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        if "Window" in obj.name:
            obj.data.materials.clear()
            obj.data.materials.append(mats["glass"])
            obj.hide_render = True
        elif "Door" in obj.name:
            obj.data.materials.clear()
            obj.data.materials.append(mats["door"])
        elif "ifcflowterminal/" in obj.name.lower():
            obj.data.materials.clear()
            obj.data.materials.append(mats["electrical"])
            obj["design_role"] = "native_ifc_electrical_terminal"
            if obj.name not in collections["Electrical Symbols"].objects:
                collections["Electrical Symbols"].objects.link(obj)
    wall_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and "wall" in obj.name.lower()]
    door_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and "ifcdoor/" in obj.name.lower()]
    native_electrical = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and "ifcflowterminal/" in obj.name.lower()]
    add_window_panes(mats, window_panes, wall_objects)
    add_room_content(rooms, manifest, collections, mats, wall_objects, door_objects, generate_electrical=not native_electrical)
    sun_data = bpy.data.lights.new("Daylight sun", type="SUN")
    sun_data.energy = 2.0
    sun = bpy.data.objects.new("Daylight sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_euler = (0.45, -0.5, -0.4)
    low, high = scene_bounds()
    configure_render(bpy.context.scene, low, high, args.render_dir / "apartment_demo_mixed.png")
    args.render_dir.mkdir(parents=True, exist_ok=True)
    for scenario in ("daylight", "mixed", "evening"):
        set_scenario(bpy.context.scene, scenario)
        bpy.context.scene.render.filepath = str((args.render_dir / f"apartment_demo_{scenario}.png").resolve())
        bpy.ops.render.render(write_still=True)
    set_scenario(bpy.context.scene, "mixed")
    bpy.context.scene.render.filepath = str((args.render_dir / "apartment_demo_mixed.png").resolve())
    args.output_blend.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output_blend.resolve()))
    print(f"APARTMENT_DEMO_READY {args.output_blend}")


if __name__ == "__main__":
    main()
