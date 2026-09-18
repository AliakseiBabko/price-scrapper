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

def set_up_eevee(scene, samples, use_probes, raytracing=True):
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
    for attr, value in (("use_raytracing", raytracing),
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


def add_occluder(lo, hi):
    """A blocking slab between the window and the far wall.

    ⚠⚠ THE SIXTH DEFECT, AND THE DEEPEST ONE. The away-facing view was measuring
    a wall the window's area light reaches DIRECTLY - an empty rectangular room
    with a light at one end has no shadow anywhere, so there was no indirect
    component in the frame at all. Probes on or off could not change a directly
    lit surface, and the test returned 1.00x five times while looking correct.

    An occluder creates a region that direct light CANNOT reach. Whatever lands
    there has bounced, which is the only thing this experiment is trying to
    measure. Without it there is nothing to measure and the number is an
    artefact.
    """
    w = min(1.1, (hi.x - lo.x) * 0.45)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.object
    ob.name = "occluder"
    ob.scale = (w / 2.0, 0.06, 1.05)
    ob.location = (lo.x + (hi.x - lo.x) * 0.30,
                   lo.y + (hi.y - lo.y) * 0.30,
                   1.05)
    return {"name": ob.name,
            "location": tuple(round(v, 3) for v in ob.location),
            "half_extent": tuple(round(v, 3) for v in ob.scale),
            "why": ("creates a genuinely shadowed region; without one the test "
                    "surface is directly lit and no indirect light is measurable")}


def add_baffle(lo, hi, height=1.8):
    """A full-width wall across the room, stopping short of the ceiling.

    ⚠⚠ THIS IS THE ONLY GEOMETRY THAT CAN TEST THE HARD CASE, and six earlier
    scene designs could not. The question is whether light reaches a surface when
    the geometry that BOUNCED it is outside the camera frame - the exact thing
    screen-space tracing cannot do and baked probes can. Every previous layout
    failed because the bright surfaces were still in shot, so screen tracing
    handled it and the probes had nothing left to contribute.

    The baffle spans the full width and runs floor to `height`, leaving a gap
    only at the TOP. Direct light cannot reach the far half at all. Light gets
    there by passing over the baffle, striking the CEILING, and bouncing down.
    Put the camera in the far half aimed DOWNWARD and that ceiling is out of
    frame - so the measured surface is lit only by light bounced off geometry the
    camera cannot see. That is the condition, constructed rather than hoped for.
    """
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.object
    ob.name = "baffle"
    ob.scale = ((hi.x - lo.x) / 2.0 + 0.05, 0.05, height / 2.0)
    ob.location = ((lo.x + hi.x) / 2.0,
                   lo.y + (hi.y - lo.y) * 0.5,
                   height / 2.0)
    return {"name": ob.name,
            "height_m": height,
            "gap_to_ceiling_m": round(float(hi.z - height), 3),
            "location": tuple(round(v, 3) for v in ob.location),
            "why": ("blocks ALL direct light to the far half; light arrives only "
                    "over the top and off the ceiling, which the test camera "
                    "deliberately excludes from frame")}


def add_probe_volume(lo, hi):
    """A light-probe volume that ENCLOSES the room's surfaces.

    ⚠️⚠️ THIS WAS WRONG FOR THE ENTIRE EXPERIMENT, AND IT IS WHY EVERY EEVEE
    NUMBER CAME BACK BLACK. Codex found it, 2026-09-18.

    The old code INSET the volume by 0.25 m - 125 mm on every side - with the
    docstring "every probe point must sit INSIDE the room". That misread the
    recorded recipe. The recipe's warning is about probe points landing BEHIND
    GEOMETRY, such as behind a curtain; it is not a reason to make the volume
    smaller than the room. A probe volume's bounds are its INFLUENCE bounds, and
    a surface outside every volume falls back to world diffuse lighting - which,
    with the world at strength 0, is black.

    So the inset excluded the floor, the ceiling and all six enclosing faces:
    exactly the surfaces whose indirect lighting was being measured. The bake was
    working the whole time. Nothing it produced could ever reach the thing under
    test.

    The volume is therefore made slightly LARGER than the room, so every surface
    lies inside it.
    """
    margin = float(os.environ.get("PROOF_PROBE_MARGIN", "0.25"))
    bpy.ops.object.lightprobe_add(type="VOLUME")
    p = bpy.context.object
    p.location = ((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2)
    # margin > 0 ENLARGES. PROOF_PROBE_MARGIN=-0.25 reproduces the original
    # defect, which is what the regression seed uses.
    p.scale = ((hi.x - lo.x + margin) / 2.0,
               (hi.y - lo.y + margin) / 2.0,
               (hi.z - lo.z + margin) / 2.0)
    d = p.data
    res = int(os.environ.get("PROOF_PROBE_RES", "8"))
    for attr, value in (("resolution_x", res), ("resolution_y", res),
                        ("resolution_z", max(4, res * 3 // 4))):
        if hasattr(d, attr):
            setattr(d, attr, value)
    # ⚠ Codex also noted the bright-world control was VACUOUS while this is
    # False: changing world brightness cannot test whether world radiance is
    # stored if the probe never captures it.
    if hasattr(d, "capture_world"):
        d.capture_world = True
    room_half = ((hi.x - lo.x) / 2.0, (hi.y - lo.y) / 2.0, (hi.z - lo.z) / 2.0)
    encloses = all(ph >= rh - 1e-6 for ph, rh in zip(p.scale, room_half))
    return {"location": tuple(round(v, 3) for v in p.location),
            "half_extent": tuple(round(v, 3) for v in p.scale),
            "margin_m": margin,
            "room_half_extent": tuple(round(v, 3) for v in room_half),
            "ENCLOSES_ROOM_SURFACES": encloses,
            "capture_world": getattr(d, "capture_world", None),
            "resolution": [getattr(d, a, None) for a in
                           ("resolution_x", "resolution_y", "resolution_z")]}


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
    # ⚠⚠ THE GUI-BAKE ROUTE, AND WHY IT IS THE SAME CODE PATH.
    # A light cache appears not to bake under `blender -b`, so the only way to
    # test question 1 is to bake ONCE in the GUI. The temptation is to build a
    # separate scene for that - and a separate scene would make the comparison
    # worthless, because the control and the test would differ in more than the
    # bake. So the SAME builder does both: --save-blend writes the scene and
    # stops, and --open-blend renders the baked file with the SAME cameras,
    # derived the same way from the compiler.
    save_blend = opts.get("--save-blend")
    open_blend = opts.get("--open-blend")
    if not (ifc_path and outdir and texture):
        print("PROOF_FAILED usage: --ifc X --outdir Y --texture Z")
        return 2
    outdir = os.path.abspath(outdir)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    _T0[0] = time.time()
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

    if open_blend:
        bpy.ops.wm.open_mainfile(filepath=os.path.abspath(open_blend))
        report["opened_blend"] = os.path.abspath(open_blend)
        report["ifc_load"] = "skipped - scene came from the baked .blend"
        report["probe_bake"] = {"status": "BAKED IN THE GUI, loaded from file",
                                "seconds": None}
        probes = [o for o in bpy.data.objects if o.type == "LIGHT_PROBE"]
        report["light_probes_in_file"] = [o.name for o in probes]
        if not probes:
            report["WARNING"] = ("the opened file contains NO light probe, so a "
                                 "bake cannot have been saved in it")
        return _render_all(report, outdir, suffix, opts)

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

    mats = [m for m in bpy.data.materials if m.name == "calibration"]
    if opts.get("--occluder", "yes").lower() not in ("no", "0", "false"):
        report["occluder"] = add_occluder(lo, hi)
        occ = bpy.data.objects.get("occluder")
        if occ is not None and mats:
            occ.data.materials.append(mats[0])
    if opts.get("--baffle", "no").lower() not in ("no", "0", "false"):
        report["baffle"] = add_baffle(lo, hi)
        baf = bpy.data.objects.get("baffle")
        if baf is not None and mats:
            baf.data.materials.append(mats[0])
    report["eevee"] = set_up_eevee(bpy.context.scene, samples, use_probes=True)
    report["probe_volume"] = add_probe_volume(lo, hi)
    # ⚠⚠ THE GATE THAT WOULD HAVE SAVED THE WHOLE EXPERIMENT.
    # A surface outside every probe influence volume falls back to world diffuse
    # lighting. For four days that fallback was a black world, so every measured
    # surface read 0 and four EEVEE runs agreed with each other about nothing.
    # A probe volume that does not enclose the surfaces being measured is not a
    # configuration choice, it is a broken measurement - so it fails the build
    # rather than quietly rendering black.
    if not report["probe_volume"]["ENCLOSES_ROOM_SURFACES"]:
        report["PROBE_CONTAINMENT"] = "FAILED"
        _write(report, outdir)
        raise SystemExit(
            "probe volume does not enclose the room surfaces: half-extent %s "
            "against a room half-extent of %s. Every surface outside the volume "
            "falls back to world lighting, so nothing measured here would be "
            "indirect light. Set PROOF_PROBE_MARGIN >= 0."
            % (report["probe_volume"]["half_extent"],
               report["probe_volume"]["room_half_extent"]))
    report["PROBE_CONTAINMENT"] = "ok"

    world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("w")
    bpy.context.scene.world = world
    world.use_nodes = True
    # ⚠⚠ THE WORLD MUST BE BLACK, AND THIS WAS THE FIFTH DEFECT.
    # A world background at strength 0.6 is a UNIFORM FILL LIGHT: it lights every
    # surface from every direction whether or not any probe exists. With it on,
    # the away-facing view measured 113.58 mean luma both with a real GPU bake
    # and without one - identical to two decimals - because the ambient swamped
    # whatever the probes contributed. The test could not have detected the
    # effect it was built to detect.
    # With the world at zero, the ONLY light is the window; anything reaching a
    # surface facing away from it has to have BOUNCED, which is precisely the
    # quantity under test.
    world_strength = float(opts.get("--world-strength", "0.0"))
    report["world_strength"] = world_strength
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        bg.inputs[1].default_value = world_strength

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

    if save_blend:
        path = os.path.abspath(save_blend)
        d = os.path.dirname(path)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # ⚠ Write this run's report under its OWN name. The first version wrote
        # proof_room_report.json, which CLOBBERED the real headless run's report
        # with a record that has no renders in it at all - and the measurement
        # then died on a missing key. A build step must not overwrite a
        # measurement step's output.
        _SUFFIX[0] = "_saveblend"
        bpy.ops.wm.save_as_mainfile(filepath=path)
        report["saved_blend"] = path
        report["next_step"] = (
            "open this file in the Blender GUI, bake the light probe volume, save, "
            "then re-run with --open-blend to render from it")
        _write(report, outdir)
        print("PROOF_SAVED %s" % path)
        return 0

    return _render_all(report, outdir, suffix, opts)


def _render_all(report, outdir, suffix, opts):
    """The renders, shared by the headless and the GUI-baked routes.

    ⚠ Cameras are rebuilt from the COMPILER here rather than taken from the
    .blend, so the baked run and the control frame the room identically. If the
    cameras came from the file, a nudge in the GUI would silently invalidate the
    comparison.
    """
    # The GUI-baked route never ran the setup block, so the import path has to
    # be established here too.
    for extra in (os.path.join(REPO, "tools"), os.path.join(REPO, "tools", "layout")):
        if extra not in sys.path:
            sys.path.insert(0, extra)
    import resolve_v0_geometry as R                          # noqa: E402
    g = R.resolve()
    W = {w["wall_id"]: w for w in g.walls}
    ox, oy = g.frame.origin_mm
    upm = g.frame.units_per_metre
    x0 = (W["R6"]["face_hi_mm"] - ox) / upm
    x1 = (W["G8"]["face_lo_mm"] - ox) / upm
    y0 = (W["MA"]["face_hi_mm"] - oy) / upm
    y1 = (W["G4d"]["face_lo_mm"] - oy) / upm
    z1 = 2.5
    samples = int(opts.get("--samples", "48"))
    rt = opts.get("--raytracing", "yes").lower() not in ("no", "0", "false")
    report["eevee"] = set_up_eevee(bpy.context.scene, samples, use_probes=True,
                                   raytracing=rt)
    # ⚠⚠ THE GROUND TRUTH CONTROL, AND IT SHOULD HAVE COME FIRST.
    # Every EEVEE result so far says "dark behind the baffle". None of them can
    # say whether DARK IS THE CORRECT ANSWER. Cycles is a path tracer: it
    # computes the bounce properly, without probes and without screen-space
    # limits. If Cycles also renders it black, the scene simply has no bounce
    # light to deliver and the whole probe comparison was measuring nothing that
    # exists. If Cycles renders it lit, EEVEE is losing light that is really
    # there. There is no way to tell those apart from EEVEE numbers alone.
    if opts.get("--engine", "eevee").lower() == "cycles":
        sc = bpy.context.scene
        sc.render.engine = "CYCLES"
        sc.cycles.samples = int(opts.get("--cycles-samples", "96"))
        try:
            sc.cycles.device = "CPU"
        except Exception:                                    # noqa: BLE001
            pass
        report["engine_override"] = {"engine": "CYCLES",
                                     "samples": sc.cycles.samples,
                                     "why": "path-traced ground truth for the bounce"}

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
    # 4. ⚠⚠ THE OUT-OF-FRAME BOUNCE TEST.
    # Behind the baffle, aimed DOWNWARD at the base of the far wall. The ceiling
    # that does the bouncing is deliberately NOT in frame, so screen-space
    # tracing has nothing on screen to trace against and only a baked probe can
    # supply the light. If probes matter anywhere, they matter here.
    if opts.get("--baffle", "no").lower() not in ("no", "0", "false"):
        far_y = y0 + (y1 - y0) * 0.78
        cam = add_persp_camera("behind_baffle", (cx, far_y, 1.35),
                               (cx, y1, 0.15), lens=40.0)
        renders["behind_baffle"] = {
            "png": os.path.join(outdir, "behind_baffle%s.png" % suffix),
            "purpose": ("THE HARD CASE. Direct light is blocked by the baffle; the "
                        "only light arrives off the CEILING, which this camera "
                        "excludes. Screen tracing cannot serve it."),
            "seconds": render_to(bpy.context.scene, cam,
                                 os.path.join(outdir, "behind_baffle%s.png" % suffix),
                                 1280, 960),
        }

    report["renders"] = renders
    report["background_mode"] = bpy.app.background
    report["total_seconds"] = round(time.time() - _T0[0], 2)
    _write(report, outdir)
    print("PROOF_OK %s" % os.path.join(outdir, "proof_room_report%s.json" % _SUFFIX[0]))
    # ⚠ When launched WITHOUT -b, Blender enters its event loop after the script
    # and would sit there forever. Quitting here lets the same script be used
    # windowed, which is the only way to test whether a baked light cache is
    # honoured by the renderer at all.
    if not bpy.app.background:
        bpy.ops.wm.quit_blender()
    return 0


_SUFFIX = [""]
_T0 = [time.time()]


def _write(report, outdir):
    p = os.path.join(outdir, "proof_room_report%s.json" % _SUFFIX[0])
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    sys.exit(main())
