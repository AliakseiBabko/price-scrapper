#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""THE PROOF ROOM - an experiment, not a picture.

WHY IT EXISTS
-------------
After the 2026-09-18 joint review, three questions were left that argument
cannot settle and both engines said to settle by measurement:

  1. does an interior walk look acceptable on EEVEE, given screen-space GI?
  2. can an uploaded texture be applied AT THE RIGHT PHYSICAL SCALE, when an
     IFC out of Bonsai carries NO UV MAPS at all?
  3. how long does one rebuild actually take?

⚠️⚠️ SO THIS SCRIPT MUST MEASURE, NOT ILLUSTRATE. `Validator_Design_Discipline.md`
says printing is not checking, and a render that merely looks plausible is the
visual form of the same mistake - it is exactly the "persuasive visualization
becoming a second, weaker model" that Codex named as the biggest risk. Every
claim this produces has to come back as a number in the report.

THE SCALE TEST, STATED SO IT CAN FAIL
-------------------------------------
The texture is a 1000 x 1000 mm calibration grid with 500 mm major lines. It is
mapped by BOX PROJECTION FROM OBJECT COORDINATES, which needs no UV map - that
is the point, because the IFC has none. An ORTHOGRAPHIC camera then photographs
a wall at a known mm-per-pixel. If the mapping is right, the major grid lines
land exactly 500 mm apart in world terms, and `measure_proof_room.py` reads that
off the PNG. If it is wrong, it is wrong by a factor that can be reported rather
than argued about.

⚠️ ROOM BOUNDS COME FROM THE COMPILER, NOT FROM `IfcSpace`. The current model
contains ZERO IfcSpace - eight existed on 2026-09-16 and none survive - so
`render_room.py`, which selects a room by its space boundaries, cannot run on
it at all. That is recorded as a finding; this script does not depend on it.
"""

import hashlib
import json
import os
import sys
import time

import bpy                                    # noqa: E402
from mathutils import Vector                  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def argv_after_ddash():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def enable_bonsai(site):
    """Bonsai lives in a pinned profile; the environment record names it."""
    if site and os.path.isdir(site):
        if site not in sys.path:
            sys.path.insert(0, site)
    for name in ("bl_ext.renovation_local.bonsai", "bonsai"):
        try:
            bpy.ops.preferences.addon_enable(module=name)
            return "enabled:%s" % name
        except Exception:                                    # noqa: BLE001
            continue
    return "already_enabled_or_builtin"


# ---------------------------------------------------------------------------
# The material. NO UV MAP IS CREATED OR NEEDED.
# ---------------------------------------------------------------------------

def calibration_material(image_path, metres_per_tile):
    """Box projection driven by OBJECT coordinates.

    ⚠️⚠️ THIS IS THE WHOLE ANSWER TO QUESTION 2, SO IT IS WORTH STATING PLAINLY.
    A mesh imported from IFC has no UV layer, and generating one per object is
    the work both review engines warned would drown the pipeline. It is not
    needed: `Texture Coordinate -> Object` gives coordinates in METRES in the
    object's own space, and the image node's BOX projection maps all three axes
    from them. Scale is then a single number - 1 / tile size in metres - and it
    is physically correct by construction rather than by eye.

    ⚠️ THE HONEST LIMIT: object coordinates are per-object, so the pattern does
    not run continuously ACROSS two walls - each starts its own grid at its own
    origin. Scale is right; alignment across objects is not. For tile a designer
    would care; for judging whether a room reads correctly it does not.
    """
    mat = bpy.data.materials.new("calibration")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.65
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(image_path)
    tex.projection = "BOX"
    tex.projection_blend = 0.25
    tex.extension = "REPEAT"
    mapping = nt.nodes.new("ShaderNodeMapping")
    s = 1.0 / float(metres_per_tile)
    mapping.inputs["Scale"].default_value = (s, s, s)
    coord = nt.nodes.new("ShaderNodeTexCoord")

    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


# ---------------------------------------------------------------------------
# Lighting - the recipe from `Realtime_Walkthrough_EEVEE.md`
# ---------------------------------------------------------------------------

def set_up_eevee(scene, samples, use_probes):
    # In Blender 5.2 the identifier is BLENDER_EEVEE. "EEVEE Next" REPLACED the
    # old engine in 4.2 rather than sitting beside it, so the _NEXT suffix that
    # the tutorials use is not a valid enum here - it raised outright.
    valid = [i.identifier for i in
             scene.render.bl_rna.properties["engine"].enum_items]
    engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in valid else "BLENDER_EEVEE"
    scene.render.engine = engine
    ee = scene.eevee
    ee.taa_render_samples = samples
    report = {"engine": engine, "engine_enum_options": valid, "samples": samples}
    for attr, value in (("use_raytracing", True),
                        ("use_shadows", True),
                        ("use_volumetric_shadows", True)):
        if hasattr(ee, attr):
            setattr(ee, attr, value)
            report[attr] = value
    # Ray-tracing resolution 1:1, per the recorded recipe.
    rt = getattr(ee, "ray_tracing_options", None)
    if rt is not None and hasattr(rt, "resolution_scale"):
        rt.resolution_scale = "1"
        report["ray_resolution"] = "1:1"
    report["use_probes"] = use_probes
    return report


def add_window_lights(openings_m, power):
    """An area light on each opening, standing in for sky - the recorded recipe.

    ⚠ The 9.36 room's opening gives onto the ЛОДЖИЯ, not the street, so the
    light reaching it is already once-bounced in reality. This is a lighting
    stand-in, not a daylight calculation, and the report says so.
    """
    n = 0
    for (cx, cy, cz, w, h) in openings_m:
        lamp = bpy.data.lights.new("win%d" % n, type="AREA")
        lamp.shape = "RECTANGLE"
        lamp.size, lamp.size_y = max(w, 0.1), max(h, 0.1)
        lamp.energy = power
        obj = bpy.data.objects.new("win%d" % n, lamp)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = (cx, cy, cz)
        obj.rotation_euler = (1.5708, 0.0, 0.0)     # face +y, into the room
        n += 1
    return n


def add_probe_volume(lo, hi):
    """A light-probe volume covering the room interior.

    ⚠️ Every probe point must sit INSIDE the room - the recorded recipe traces a
    black corner to probes that ended up behind a curtain. The volume is therefore
    inset from the walls rather than matched to them.
    """
    inset = 0.25
    bpy.ops.object.lightprobe_add(type="VOLUME")
    p = bpy.context.object
    p.location = ((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2)
    p.scale = (max(hi.x - lo.x - inset, 0.5) / 2.0,
               max(hi.y - lo.y - inset, 0.5) / 2.0,
               max(hi.z - lo.z - inset, 0.5) / 2.0)
    d = p.data
    for attr, value in (("resolution_x", 8), ("resolution_y", 8), ("resolution_z", 6)):
        if hasattr(d, attr):
            setattr(d, attr, value)
    return {"location": tuple(round(v, 3) for v in p.location),
            "half_extent": tuple(round(v, 3) for v in p.scale),
            "inset_m": inset}


# ---------------------------------------------------------------------------
# Cameras
# ---------------------------------------------------------------------------

def add_ortho_camera(name, location, look, width_m):
    cam = bpy.data.cameras.new(name)
    cam.type = "ORTHO"
    cam.ortho_scale = width_m
    obj = bpy.data.objects.new(name, cam)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    _aim(obj, look)
    return obj


def add_persp_camera(name, location, look, lens=24.0):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    obj = bpy.data.objects.new(name, cam)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    _aim(obj, look)
    return obj


def _aim(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render_to(scene, cam, path, res_x, res_y):
    scene.camera = cam
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    # ⚠ Blender resolves a RELATIVE render path against the blend file, and with
    # no blend file that becomes the drive root: the first run wrote every PNG
    # to C:\data\outputs\... instead of into the repo. Absolute, always.
    scene.render.filepath = os.path.abspath(path)
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return round(time.time() - t0, 2)


# ---------------------------------------------------------------------------

def main():
    args = argv_after_ddash()
    opts = dict(zip(args[0::2], args[1::2]))
    ifc_path = opts.get("--ifc")
    outdir = opts.get("--outdir")
    texture = opts.get("--texture")
    site = opts.get("--site") or None
    samples = int(opts.get("--samples", "48"))
    tile_m = float(opts.get("--tile-m", "1.0"))
    # ⚠ THE CONTROL. The first GI test compared the toward-window frame against
    # the away frame and got a ratio of 1.756 - the away frame BRIGHTER. That
    # measured what happened to be in each shot, not the lighting: two different
    # views are not a controlled comparison. The control is the SAME camera with
    # the probe bake on and off, so the only variable is the thing being tested.
    do_bake = opts.get("--bake", "yes").lower() not in ("no", "0", "false")
    suffix = opts.get("--suffix", "")
    _SUFFIX[0] = suffix
    if not (ifc_path and outdir and texture):
        print("PROOF_FAILED usage: --ifc X --outdir Y --texture Z")
        return 2
    outdir = os.path.abspath(outdir)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    t_start = time.time()
    report = {
        "experiment": "proof room - EEVEE walkthrough + physically scaled texture",
        "question_1": "does an interior walk look acceptable on EEVEE screen-space GI?",
        "question_2": "can a texture be applied at the RIGHT PHYSICAL SCALE with no UV map?",
        "ifc": ifc_path,
        "ifc_sha256": sha256(ifc_path),
        "texture": texture,
        "tile_metres": tile_m,
        "probe_bake_requested": do_bake,
        "suffix": suffix,
    }

    report["bonsai"] = enable_bonsai(site)
    report["blender_version"] = bpy.app.version_string

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    try:
        bpy.ops.bim.load_project(filepath=os.path.abspath(ifc_path))
        report["ifc_load"] = "ok"
    except Exception as exc:                                 # noqa: BLE001
        report["ifc_load"] = "failed: %s" % exc
        _write(report, outdir)
        print("PROOF_FAILED ifc_load")
        return 2

    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    report["mesh_objects"] = len(meshes)

    # THE UV FACT, MEASURED RATHER THAN ASSUMED. This is the premise of the
    # whole texture question, so it is checked here instead of being quoted
    # from a note.
    with_uv = [o for o in meshes if o.data.uv_layers]
    report["mesh_objects_with_uv_maps"] = len(with_uv)
    report["uv_finding"] = (
        "%d of %d imported meshes carry a UV map. Box projection from object "
        "coordinates is therefore not a convenience - it is the only route that "
        "does not require generating UVs per object."
        % (len(with_uv), len(meshes)))

    mat = calibration_material(os.path.abspath(texture), tile_m)
    painted = 0
    for o in meshes:
        o.data.materials.clear()
        o.data.materials.append(mat)
        painted += 1
    report["meshes_painted"] = painted

    # --- the room, from the COMPILER ---------------------------------------
    sys.path.insert(0, os.path.join(REPO, "tools"))
    sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
    import resolve_v0_geometry as R                          # noqa: E402
    g = R.resolve()
    W = {w["wall_id"]: w for w in g.walls}
    ox, oy = g.frame.origin_mm
    upm = g.frame.units_per_metre

    def mx(mm):
        return (mm - ox) / upm

    def my(mm):
        return (mm - oy) / upm

    x0, x1 = mx(W["R6"]["face_hi_mm"]), mx(W["G8"]["face_lo_mm"])
    y0, y1 = my(W["MA"]["face_hi_mm"]), my(W["G4d"]["face_lo_mm"])
    z1 = 2.5
    lo, hi = Vector((x0, y0, 0.0)), Vector((x1, y1, z1))
    report["room"] = {
        "id": "9.36",
        "bounds_m": [round(v, 4) for v in (x0, y0, 0.0, x1, y1, z1)],
        "width_m": round(x1 - x0, 4),
        "depth_m": round(y1 - y0, 4),
        "source": "ResolvedGeometry faces: R6.hi, G8.lo, MA.hi, G4d.lo",
        "caveat": ("the NORTH bound is G4d low face and G4d spans only part of the "
                   "room width, so depth is approximate at the north-east corner. "
                   "It does not affect the two questions being tested."),
        "walls_resolved": len(g.walls),
    }

    # The opening, in metres, for the window light.
    o4 = [o for o in g.openings if o["opening_id"] == "O4"][0]
    oxs = [p[0] for p in o4["polygon"]]
    ocx = mx((min(oxs) + max(oxs)) / 2.0)
    ow = (max(oxs) - min(oxs)) / upm
    # ⚠ 260 W BLEW THE ROOM TO WHITE. The first run returned a mean luma of 205
    # of 255 in both the probe and the control frame, and the GI comparison then
    # reported a gain of 1.00 - not because the probes did nothing, but because
    # both frames were CLIPPED and could not differ. A saturated measurement is
    # no measurement. Power is now a parameter and the report carries the frame
    # statistics, so clipping is visible instead of silent.
    light_w = float(opts.get("--light-w", "28"))
    report["window_light_watts"] = light_w
    report["window_lights"] = add_window_lights(
        [(ocx, y0 + 0.02, 1.2, ow, 1.5)], power=light_w)

    report["eevee"] = set_up_eevee(bpy.context.scene, samples, use_probes=True)
    report["probe_volume"] = add_probe_volume(lo, hi)

    world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("w")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.16, 0.18, 0.21, 1.0)
        bg.inputs[1].default_value = 0.6

    if do_bake:
        try:
            t0 = time.time()
            bpy.ops.object.lightprobe_cache_bake(subset="ALL")
            report["probe_bake"] = {"status": "ok", "seconds": round(time.time() - t0, 2)}
        except Exception as exc:                             # noqa: BLE001
            report["probe_bake"] = {"status": "FAILED", "error": str(exc)}
    else:
        report["probe_bake"] = {"status": "SKIPPED - this is the control run",
                                "seconds": 0.0}

    # --- the three renders --------------------------------------------------
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    renders = {}

    # 1. ORTHOGRAPHIC elevation of the south wall - THE MEASUREMENT.
    ortho_w = 4.0
    res_x, res_y = 1600, 1200
    cam = add_ortho_camera("ortho_south", (cx, cy, 1.25), (cx, y0 - 1.0, 1.25), ortho_w)
    renders["ortho_south"] = {
        "png": os.path.join(outdir, "ortho_south%s.png" % suffix),
        "ortho_width_m": ortho_w, "res": [res_x, res_y],
        "mm_per_px": round(ortho_w * 1000.0 / res_x, 4),
        "expected_major_line_spacing_px": round(500.0 / (ortho_w * 1000.0 / res_x), 1),
        "purpose": "measure the applied texture scale against a known mm/px",
        "seconds": render_to(bpy.context.scene, cam,
                             os.path.join(outdir, "ortho_south%s.png" % suffix), res_x, res_y),
    }

    # 2. PERSPECTIVE facing the window - the favourable case.
    cam = add_persp_camera("towards_window", (cx, cy + 0.6, 1.6), (cx, y0, 1.3))
    renders["towards_window"] = {
        "png": os.path.join(outdir, "towards_window%s.png" % suffix),
        "purpose": "the case screen-space GI handles well: the light source is in frame",
        "seconds": render_to(bpy.context.scene, cam,
                             os.path.join(outdir, "towards_window%s.png" % suffix), 1280, 960),
    }

    # 3. PERSPECTIVE facing AWAY - THE ACTUAL TEST.
    cam = add_persp_camera("away_from_window", (cx, cy - 0.4, 1.6), (cx, y1, 1.3))
    renders["away_from_window"] = {
        "png": os.path.join(outdir, "away_from_window%s.png" % suffix),
        "purpose": ("THE TEST THAT MATTERS. The window is now BEHIND the camera. "
                    "If screen-space GI is the whole story this goes dark; if the "
                    "baked probes carry the indirect light it does not. This is "
                    "question 1, and it is the frame to compare against #2."),
        "seconds": render_to(bpy.context.scene, cam,
                             os.path.join(outdir, "away_from_window%s.png" % suffix), 1280, 960),
    }
    report["renders"] = renders
    report["total_seconds"] = round(time.time() - t_start, 2)
    _write(report, outdir)
    print("PROOF_OK %s" % os.path.join(outdir, "proof_room_report%s.json" % _SUFFIX[0]))
    return 0


_SUFFIX = [""]


def _write(report, outdir):
    p = os.path.join(outdir, "proof_room_report%s.json" % _SUFFIX[0])
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    sys.exit(main())
