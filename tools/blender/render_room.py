"""Render ONE room in Cycles, with materials driven from the finish schedule.

`00_Master/Model_and_Views.md` names the render as a VIEW derived from
`model.ifc`. This is the generator for it, and the point of generating rather
than decorating is stated there: a hand-dressed `.blend` becomes a second source
of truth and drifts from the schedule silently. Here a finish change is a re-run.

Runs inside Blender, exactly like its sibling `export_glb.py`:

    blender --background --python tools/blender/render_room.py -- \
        <model.ifc> <room name> <out.png> <out_report.json> <bonsai-site> \
        <finish_schedule.json> <render_appearance.json> [--samples N] [--gpu]

HOW A ROOM IS MAPPED TO SURFACES
--------------------------------
The IFC carries `IfcRelSpaceBoundary` - 40 of them in v0-existing - which is the
model's own statement of which elements bound which space. That is read with
ifcopenshell (bundled with Bonsai) and matched to Blender objects by name, since
Bonsai names objects `<IfcClass>/<Name>`. No geometry guessing.

THREE LIMITS, STATED RATHER THAN DISCOVERED LATER
-------------------------------------------------
1. A wall bounds TWO rooms and is one object with one material. The far side
   therefore takes this room's finish too. That is invisible from a camera
   inside the room, which is the only place this script puts one, but it makes
   the output wrong for any exterior or whole-flat view.
2. The floor and ceiling are two slabs spanning the whole flat, not per room, so
   they take one finish. Same reasoning, same limit.
3. Windows are a flat stand-in. Real daylight needs the glass-shadow trick
   (Mix Shader between Glass and Transparent, driven by Light Path > Is Shadow
   Ray) or the glass blocks the light it should admit. Not implemented; the
   report says so on every run.

None of the three is hidden: `open_limits` in the report lists them, so a render
cannot be mistaken for a finished visualisation.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

EXCLUDED_CLASSES = {"IfcSpace", "IfcOpeningElement"}

# Which appearance key an IFC class takes when it is not a bounding wall of the
# room being rendered. Slabs are split into floor and ceiling by height below.
CLASS_TO_ELEMENT = {
    "IfcDoor": "door",
    "IfcWindow": "window_glass",
}


def _argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def enable_bonsai(site: Path | None) -> str:
    """Enable Bonsai however this Blender exposes it. See export_glb.py - the
    module is `bl_ext.renovation_local.bonsai`, and the order matters."""
    if site:
        sys.path.insert(0, str(site.resolve()))
    errors = []
    for module in ("bl_ext.renovation_local.bonsai", "bl_ext.user_default.bonsai", "bonsai"):
        try:
            bpy.ops.preferences.addon_enable(module=module)
            return "enabled:%s" % module
        except Exception as exc:  # noqa: BLE001 - reported, not swallowed
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


def element_name_of(obj) -> str:
    """Bonsai names objects `<IfcClass>/<Name>`; the part after the slash is the
    IFC element Name, which is what the space boundaries refer to."""
    return obj.name.split("/", 1)[1] if "/" in obj.name else obj.name


def read_space_boundaries(ifc_path: Path, room: str) -> tuple[set[str], list[str]]:
    """Element NAMES bounding `room`, from the IFC's own IfcRelSpaceBoundary.

    Returns (bounding element names, all space names) so a misspelled room can
    be reported with the list of what was actually available.
    """
    import ifcopenshell  # bundled with Bonsai; only importable after enable

    model = ifcopenshell.open(str(ifc_path.resolve()))
    spaces = [s.Name for s in model.by_type("IfcSpace") if s.Name]
    bounding: set[str] = set()
    for rel in model.by_type("IfcRelSpaceBoundary"):
        space, element = rel.RelatingSpace, rel.RelatedBuildingElement
        if space is None or element is None or space.Name != room:
            continue
        if element.Name:
            bounding.add(element.Name)
    return bounding, spaces


def appearance_material(name: str, spec: dict) -> bpy.types.Material:
    """One Principled BSDF, base colour and roughness from the appearance file.

    Deliberately not a node network: `glb_material_probe.py` measured that a
    procedural network does not survive a glTF export, and keeping the render
    and the walkable view on the same material model means what you judge in one
    is what you judge in the other.
    """
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = tuple(spec["base_color"])
    bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.8))
    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.0))
    return mat


def _world_bounds(obj) -> tuple[Vector, Vector]:
    """`matrix_world` applied explicitly. Reading local bounds is what put the
    camera in a corner the first time this pattern was used, in the viewer."""
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    lo = Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
    hi = Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
    return lo, hi


def glass_shadow_material(name: str, spec: dict) -> bpy.types.Material:
    """The glass-shadow trick, and it is the difference between a lit room and
    the dark blue box the first run produced.

    Blender's Glass BSDF blocks light and casts a shadow by default, because
    full refraction is expensive. For a WINDOW that is simply wrong: the one
    opening a daylit interior has stops admitting daylight. The fix, recorded on
    `00_Master/Model_and_Views.md` as the highest-value single technique in the
    2026-09-16 batch, is a Mix Shader between Glass and Transparent driven by
    `Light Path > Is Shadow Ray` - so the pane still looks like glass to camera
    and reflection rays, and is invisible to shadow rays.

    This is a node network, and unlike the flat materials it will NOT survive a
    glTF export. That is correct: it exists for Cycles, and the walkable view
    has no lighting to admit.
    """
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    glass = nt.nodes.new("ShaderNodeBsdfGlass")
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    path = nt.nodes.new("ShaderNodeLightPath")

    glass.inputs["Color"].default_value = tuple(spec["base_color"])
    glass.inputs["Roughness"].default_value = float(spec.get("roughness", 0.05))

    # Fac 0 -> Glass (camera/reflection rays), Fac 1 -> Transparent (shadow rays).
    nt.links.new(path.outputs["Is Shadow Ray"], mix.inputs["Fac"])
    nt.links.new(glass.outputs["BSDF"], mix.inputs[1])
    nt.links.new(transp.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return mat


def add_light_portals(bounding: set[str]) -> int:
    """An area light fitted to each window opening, with `is_portal` set.

    A portal emits nothing. It tells the sampler WHERE light enters, which is
    the other half of the interior fix: the glass trick lets daylight through,
    the portal stops the sampler wasting its rays looking for it.
    """
    made = 0
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or ifc_class_of(obj) != "IfcWindow":
            continue
        lo, hi = _world_bounds(obj)
        span = hi - lo
        # The window's thin axis is its normal; the other two are its opening.
        thin = min(range(3), key=lambda i: span[i])
        sx, sy = [span[i] for i in range(3) if i != thin]
        data = bpy.data.lights.new("Portal_%s" % obj.name, type="AREA")
        data.shape = "RECTANGLE"
        data.size, data.size_y = max(sx, 0.05), max(sy, 0.05)
        try:
            data.cycles.is_portal = True
        except Exception:  # noqa: BLE001 - reported by the caller's count
            continue
        light = bpy.data.objects.new(data.name, data)
        bpy.context.collection.objects.link(light)
        light.location = (lo + hi) / 2.0
        # Face the portal along the window's thin axis.
        light.rotation_euler = (
            (math.radians(90.0), 0.0, 0.0) if thin == 1
            else (0.0, math.radians(90.0), 0.0) if thin == 0
            else (0.0, 0.0, 0.0)
        )
        made += 1
    return made


def room_bounds(room: str, bounding: set[str]) -> tuple[Vector, Vector] | None:
    """Horizontal extent from the room's IfcSpace, VERTICAL extent from its walls.

    The space states where a room is in plan and nothing else states that. But
    in this model the IfcSpace is a flat PLATE - measured Z span 0.02 m - so
    taking height from it puts the camera 8 cm BELOW the floor, which is what
    the first run did. The bounding walls carry the real 0..2.5 m storey height,
    so the two are read from different sources on purpose.
    """
    space = None
    for obj in bpy.data.objects:
        if obj.type == "MESH" and ifc_class_of(obj) == "IfcSpace" and element_name_of(obj) == room:
            space = obj
            break
    if space is None:
        return None
    lo, hi = _world_bounds(space)

    wall_z = [
        _world_bounds(o)
        for o in bpy.data.objects
        if o.type == "MESH" and element_name_of(o) in bounding
    ]
    if wall_z:
        lo.z = min(b[0].z for b in wall_z)
        hi.z = max(b[1].z for b in wall_z)
    return lo, hi


def paint(bounding: set[str], schedule: dict, appearance: dict, room: str) -> dict:
    """Assign one material per object. Bounding walls get the room's scheduled
    finish; slabs split into floor and ceiling; everything else is context."""
    mats = appearance["materials"]
    elements = appearance["elements"]
    default = appearance["_default"]

    entry = schedule.get(room) or {}
    material_string = entry.get("material")
    unmatched = None
    if material_string and material_string in mats:
        wall_spec = mats[material_string]
    else:
        wall_spec = default
        unmatched = material_string or "(room absent from finish schedule)"

    # Split the two slabs by height: the lower is the floor, the upper the
    # ceiling. Two slabs is what the model carries; if that ever changes this
    # assumption is what breaks, so it is asserted in the report.
    slabs = [o for o in bpy.data.objects
             if o.type == "MESH" and ifc_class_of(o) in ("IfcSlab",)]
    slab_z = {o.name: (o.matrix_world @ Vector(o.bound_box[0])).z for o in slabs}
    ceiling_names = set()
    if len(slabs) >= 2:
        ceiling_names = {max(slab_z, key=slab_z.get)}

    counts: dict[str, int] = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        cls = ifc_class_of(obj) or "unclassified"
        ename = element_name_of(obj)

        if cls == "IfcSlab":
            key = "ceiling" if obj.name in ceiling_names else "floor"
            spec, label = elements[key], key
        elif cls == "IfcWindow":
            # Not a flat material: see glass_shadow_material for why a window
            # painted flat is what made the first render a dark blue box.
            obj.data.materials.clear()
            obj.data.materials.append(
                glass_shadow_material("FIN_window_glass", elements["window_glass"])
            )
            obj["render_role"] = "window_glass"
            counts["window_glass"] = counts.get("window_glass", 0) + 1
            continue
        elif cls in CLASS_TO_ELEMENT:
            key = CLASS_TO_ELEMENT[cls]
            spec, label = elements[key], key
        elif ename in bounding:
            spec, label = wall_spec, "room_finish"
        else:
            spec, label = elements["context"], "context"

        obj.data.materials.clear()
        obj.data.materials.append(appearance_material("FIN_%s" % label, spec))
        obj["render_role"] = label
        counts[label] = counts.get(label, 0) + 1

    return {
        "assigned": counts,
        "room_material": material_string,
        "unmatched_material": unmatched,
        "slabs_found": len(slabs),
    }


def set_up_world(appearance: dict) -> None:
    """Sky texture as fill - step 3 of the four-step formula."""
    light = appearance["lighting"]
    world = bpy.data.worlds.new("RenderWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    sky = nt.nodes.new("ShaderNodeTexSky")
    bg = nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg.inputs["Strength"].default_value = float(light["sky_strength"])
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def add_sun(appearance: dict, room_centre: Vector, windows: list[Vector]) -> dict:
    """Sun as key - step 2. Angle widened so the shadow is not razor-sharp.

    AIMED THROUGH THE ROOM'S OWN WINDOW rather than at a fixed compass bearing.
    A hard-coded azimuth is a coin flip: get it wrong and the only opening is in
    shadow, which no amount of sun strength fixes. Deriving it from the opening
    means the key light enters where light can actually enter.

    ⚠️ So this is a LIGHTING STUDY, not a daylight study. It tells you how the
    room reads when sun comes through that window; it does NOT tell you whether
    the sun is ever in that position at this site, on this orientation, on any
    given date. Treating it as the latter would be exactly the mistake
    `00_Master/Evidence_Reading_Discipline.md` is about.
    """
    light = appearance["lighting"]
    data = bpy.data.lights.new("Key", type="SUN")
    data.energy = float(light["sun_strength"])
    data.angle = math.radians(float(light["sun_angle_deg"]))
    obj = bpy.data.objects.new("Key", data)
    bpy.context.collection.objects.link(obj)

    elev = math.radians(float(light["sun_elevation_deg"]))
    if windows:
        window = windows[0] if len(windows) == 1 else sum(
            windows, Vector((0.0, 0.0, 0.0))) / len(windows)
        horizontal = Vector((room_centre.x - window.x, room_centre.y - window.y, 0.0))
        if horizontal.length < 1e-6:
            horizontal = Vector((1.0, 0.0, 0.0))
        horizontal.normalize()
        # Point the sun DOWN and INTO the room through the opening.
        direction = Vector((
            horizontal.x * math.cos(elev),
            horizontal.y * math.cos(elev),
            -math.sin(elev),
        ))
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        aimed = "through window"
    else:
        rot = math.radians(float(light["sun_rotation_deg"]))
        obj.rotation_euler = (math.radians(90.0) - elev, 0.0, rot)
        aimed = "fixed azimuth (no window in this room)"
    return {"aimed": aimed, "elevation_deg": float(light["sun_elevation_deg"])}


def room_windows(lo: Vector, hi: Vector, margin: float = 0.5) -> list[Vector]:
    """Centres of the windows serving this room.

    A window sits IN the wall, so its centre falls just outside the space's own
    footprint - the Bedroom window measures y 0.36..0.44 against a space
    starting at y 0.60. Hence the margin: test against a slightly grown room
    box, not the box itself.
    """
    found = []
    for obj in bpy.data.objects:
        if obj.type != "MESH" or ifc_class_of(obj) != "IfcWindow":
            continue
        wlo, whi = _world_bounds(obj)
        centre = (wlo + whi) / 2.0
        if (lo.x - margin <= centre.x <= hi.x + margin
                and lo.y - margin <= centre.y <= hi.y + margin):
            found.append(centre)
    return found


def _look_at(obj, target: Vector) -> None:
    """Aim -Z at `target` with +Y up. Building the rotation from a direction
    vector rather than writing Euler angles by hand: the hand-written yaw in the
    first version pointed the camera away from the room's only window."""
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def kelvin_to_rgb(kelvin: float) -> tuple[float, float, float]:
    """Approximate blackbody colour, normalised to 1.0 on the strongest channel.

    Deliberately a colour TEMPERATURE rather than a picked RGB swatch: the
    sources on `00_Master/Model_and_Views.md` are specific that the mix of cool
    skylight and warm lamps is what reads as real, and that choosing a warm
    colour by eye does not reproduce it. Tanner Helland's piecewise fit, which
    is accurate enough at the 2000-6500 K domestic range this is used in.
    """
    t = max(1000.0, min(40000.0, kelvin)) / 100.0
    if t <= 66.0:
        r = 255.0
        g = 99.4708025861 * math.log(t) - 161.1195681661
    else:
        r = 329.698727446 * ((t - 60.0) ** -0.1332047592)
        g = 288.1221695283 * ((t - 60.0) ** -0.0755148492)
    if t >= 66.0:
        b = 255.0
    elif t <= 19.0:
        b = 0.0
    else:
        b = 138.5177312231 * math.log(t - 10.0) - 305.0447927307
    rgb = [max(0.0, min(255.0, c)) / 255.0 for c in (r, g, b)]
    peak = max(rgb) or 1.0
    return tuple(c / peak for c in rgb)


def add_room_light(appearance: dict, lo: Vector, hi: Vector, windows: list[Vector]) -> dict:
    """A ceiling luminaire at the room centre.

    In a daylit room this is the ACCENT the four-step formula calls for. In a
    windowless one it is the only light in the scene: the Bathroom - an internal
    room with no opening - rendered PURE BLACK without it, which is physically
    correct and completely useless. Sun and sky cannot enter a room with no
    window, and no amount of sun strength changes that.
    """
    light = appearance["lighting"]
    data = bpy.data.lights.new("Luminaire", type="AREA")
    data.shape = "SQUARE"
    data.size = float(light.get("artificial_size_m", 0.6))
    # Power BY AREA. A flat wattage calibrated on one room is wrong in every
    # other one: 75 W read correctly in the 16.9 m2 bedroom and blew the 3.1 m2
    # bathroom to white.
    area_m2 = max((hi.x - lo.x) * (hi.y - lo.y), 0.5)
    data.energy = float(light.get("artificial_power_w_per_m2", 4.5)) * area_m2
    kelvin = float(light.get("artificial_kelvin", 3200))
    data.color = kelvin_to_rgb(kelvin)
    obj = bpy.data.objects.new("Luminaire", data)
    bpy.context.collection.objects.link(obj)
    centre = (lo + hi) / 2.0
    obj.location = Vector((centre.x, centre.y, hi.z - 0.12))
    return {
        "kelvin": kelvin,
        "power_w": round(data.energy, 1),
        "room_area_m2": round(area_m2, 2),
        "role": "accent" if windows else "only light source (windowless room)",
    }


def place_camera(lo: Vector, hi: Vector, eye: float, windows: list[Vector]) -> dict:
    """Stand at the far end of the room and look TOWARDS the window.

    Two reasons, and they agree. Compositionally it is the standard interior
    shot: the opening is the brightest thing in a daylit room and the eye needs
    it. Practically, the first version stood AT the window looking away from it,
    so the one light source in the scene was behind the camera and the room read
    as a dark blue box - which is what the first two renders were.

    With no window, fall back to looking along the longer horizontal axis, which
    is what shows a room's proportion rather than a corner.
    """
    centre = (lo + hi) / 2.0
    span_x, span_y = hi.x - lo.x, hi.y - lo.y
    z = min(lo.z + eye, hi.z - 0.1)

    if windows:
        target = windows[0]
        if len(windows) > 1:  # aim at the mean of several openings
            target = sum(windows, Vector((0.0, 0.0, 0.0))) / len(windows)
        # Stand at the point inside the room furthest from the window, pulled in
        # off the wall so the camera is not inside it.
        away = (centre - target)
        if away.length < 1e-6:
            away = Vector((1.0, 0.0, 0.0))
        away.z = 0.0
        away.normalize()
        half = Vector((span_x, span_y, 0.0)) / 2.0
        reach = min(
            abs(half.x / away.x) if abs(away.x) > 1e-6 else 1e9,
            abs(half.y / away.y) if abs(away.y) > 1e-6 else 1e9,
        )
        loc = centre + away * max(reach - 0.45, 0.0)
        loc.z = z
        aim = Vector((target.x, target.y, z - 0.10))
        facing = "window"
    else:
        # No opening to aim at, so stand in a corner and look down the DIAGONAL.
        # That is the longest sightline a box has, and in a small room it is the
        # difference between reading the space and filling the frame with one
        # wall - the 1.8 x 1.7 m bathroom showed nothing from the long axis.
        loc = Vector((lo.x + 0.30, lo.y + 0.30, z))
        aim = Vector((centre.x, centre.y, lo.z + (hi.z - lo.z) * 0.45))
        facing = "corner diagonal (no window in this room)"

    data = bpy.data.cameras.new("Cam")
    # Focal length by room size. 20 mm is already wide, and it still filled the
    # frame with one corner of the 1.8 x 1.7 m bathroom: a small wet room cannot
    # be photographed from inside itself at a normal lens. Below ~6 m2 go wider
    # and accept the distortion, which is what the trade does.
    diagonal = math.hypot(span_x, span_y)
    data.lens = 20.0 if diagonal >= 3.5 else 12.0
    cam = bpy.data.objects.new("Cam", data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    _look_at(cam, aim)
    bpy.context.scene.camera = cam
    return {
        "location": [round(v, 3) for v in loc],
        "aimed_at": [round(v, 3) for v in aim],
        "eye_height_m": round(z - lo.z, 3),
        "facing": facing,
        "lens_mm": data.lens,
        "windows_serving_room": len(windows),
        "room_span_m": [round(span_x, 3), round(span_y, 3), round(hi.z - lo.z, 3)],
    }


def main() -> int:
    args = _argv_after_ddash()
    if len(args) < 7:
        print("RENDER_FAILED usage: <ifc> <room> <out.png> <report.json> <site> <schedule> <appearance>")
        return 2

    ifc_path = Path(args[0])
    room = args[1]
    out_png = Path(args[2])
    out_json = Path(args[3])
    site = Path(args[4]) if args[4] else None
    schedule_path = Path(args[5])
    appearance_path = Path(args[6])
    rest = args[7:]
    samples = 64
    if "--samples" in rest:
        samples = int(rest[rest.index("--samples") + 1])
    use_gpu = "--gpu" in rest

    report: dict = {
        "ifc": str(ifc_path),
        "room": room,
        "png": str(out_png),
        "schedule": str(schedule_path),
        "appearance": str(appearance_path),
        "open_limits": [
            "A wall bounds two rooms but is one object, so its far side carries this room's finish. Invisible from inside; wrong for any exterior view.",
            "Floor and ceiling are whole-flat slabs, so they take one finish rather than a per-room one.",
            "Glass is the shadow-ray trick, not measured glazing: no pane count, no coating, no frame. It admits daylight correctly and tells you nothing about a spec.",
            "Untextured by construction: an IFC out of Bonsai carries no UV maps. Roughness, not pattern, is what separates tile from paint here.",
        ],
    }

    report["bonsai"] = enable_bonsai(site)
    report["blender_version"] = bpy.app.version_string

    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    appearance = json.loads(appearance_path.read_text(encoding="utf-8"))

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    try:
        bpy.ops.bim.load_project(filepath=str(ifc_path.resolve()))
        report["ifc_load"] = "ok"
    except Exception as exc:  # noqa: BLE001
        report["ifc_load"] = "failed: %s" % exc
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("RENDER_FAILED " + str(out_json))
        return 2

    bounding, spaces = read_space_boundaries(ifc_path, room)
    report["spaces_in_model"] = spaces
    report["bounding_elements"] = sorted(bounding)
    if not bounding:
        report["error"] = "room %r has no space boundaries; available spaces: %s" % (room, spaces)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("RENDER_FAILED " + str(out_json))
        return 2

    bounds = room_bounds(room, bounding)
    if bounds is None:
        report["error"] = "no IfcSpace mesh named %r" % room
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("RENDER_FAILED " + str(out_json))
        return 2
    lo, hi = bounds

    report["paint"] = paint(bounding, schedule, appearance, room)

    # Drop the non-physical classes only AFTER the space has been measured.
    for obj in list(bpy.data.objects):
        if obj.type == "MESH" and ifc_class_of(obj) in EXCLUDED_CLASSES:
            bpy.data.objects.remove(obj, do_unlink=True)

    windows = room_windows(lo, hi)
    centre = (lo + hi) / 2.0
    set_up_world(appearance)
    report["sun"] = add_sun(appearance, centre, windows)
    report["luminaire"] = add_room_light(appearance, lo, hi, windows)
    report["light_portals"] = add_light_portals(bounding)
    report["camera"] = place_camera(lo, hi, 1.60, windows)

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    # Clamp INDIRECT only. Clamping direct light kills the key light itself -
    # recorded on 00_Master/Model_and_Views.md as the interior specialist's rule.
    scene.cycles.sample_clamp_indirect = 4.0
    scene.cycles.transparent_max_bounces = 24
    if use_gpu:
        scene.cycles.device = "GPU"
    lighting = appearance["lighting"]
    scene.view_settings.view_transform = lighting["view_transform"]
    try:
        scene.view_settings.look = lighting["look"]
    except Exception:  # noqa: BLE001 - look names differ between versions
        report["look"] = "unavailable: %r" % lighting["look"]
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 800
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(out_png.resolve())

    out_png.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.render.render(write_still=True)

    report["samples"] = samples
    report["device"] = "GPU" if use_gpu else "CPU"
    report["png_bytes"] = out_png.stat().st_size if out_png.exists() else None

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("RENDER_WROTE " + str(out_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
