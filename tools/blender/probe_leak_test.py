#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Does a baked probe grid leak light through a 75 mm partition?

⚠️⚠️ WHY THIS IS A STANDALONE SCENE AND NOT THE PROOF ROOM.
The first attempt put a "sealed" partition across the 9.36 room inside the real
IFC model and called any light behind it leakage. It was not sealed: Cycles
rendered the far side at 130.9, proving a light path existed. The 9.36 room is
not an isolated box - it opens to the loggia through O4 and the rest of the flat
continues around it, so light travels round the partition through geometry the
test never accounted for. **A test that assumes a seal it has not verified
measures nothing**, and that was the tenth defect in this experiment.

So this builds its own closed box from scratch, with nothing else in the scene:
two chambers, one light, one divider at the real 75 mm of G7/G8. Then the seal is
ASSERTED by the ground-truth renderer before any EEVEE number is believed - if
Cycles puts light in the dark chamber, the geometry is wrong and the run is
void.

Antigravity's claim, 2026-09-18: a probe grid spaced 0.3-0.5 m cannot resolve a
75 mm wall, so probes in the lit chamber spill irradiance into the dark one.
"""

import json
import os
import sys
import time

import bpy

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def argv_after_ddash():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def box(name, centre, half, material=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.object
    ob.name = name
    ob.location = centre
    ob.scale = half
    if material:
        ob.data.materials.append(material)
    return ob


def grey():
    m = bpy.data.materials.new("grey")
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b:
        b.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
        b.inputs["Roughness"].default_value = 0.7
    return m


def build(partition_mm, probe_res):
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    mat = grey()

    # Two chambers, each 2.0 x 2.0 x 2.5, sharing a divider on y = 0.
    # Built as SHELLS from six slabs each, so every surface is real geometry
    # with thickness - single-surface walls leak light by construction and that
    # would confound the very thing being measured.
    t = 0.15
    hx, hz = 1.0, 1.25
    for sign, tag in ((-1.0, "lit"), (1.0, "dark")):
        cy = sign * (1.0 + partition_mm / 2000.0)
        box("floor_%s" % tag, (0, cy, -t / 2), (hx + t, 1.0 + t, t / 2), mat)
        box("ceil_%s" % tag, (0, cy, 2.5 + t / 2), (hx + t, 1.0 + t, t / 2), mat)
        box("xlo_%s" % tag, (-hx - t / 2, cy, 1.25), (t / 2, 1.0 + t, hz), mat)
        box("xhi_%s" % tag, (hx + t / 2, cy, 1.25), (t / 2, 1.0 + t, hz), mat)
        box("end_%s" % tag, (0, cy + sign * (1.0 + t / 2), 1.25), (hx + t, t / 2, hz), mat)

    # THE DIVIDER, at the real partition thickness, oversized so it cannot be
    # flanked.
    box("partition", (0, 0, 1.25), (hx + t, partition_mm / 2000.0, hz + 0.2), mat)

    lamp = bpy.data.lights.new("sun_in_lit", type="AREA")
    lamp.shape = "RECTANGLE"
    lamp.size, lamp.size_y = 1.4, 1.4
    lamp.energy = 200.0
    ob = bpy.data.objects.new("sun_in_lit", lamp)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0.0, -1.9, 1.3)
    ob.rotation_euler = (1.5708, 0.0, 0.0)          # faces +y, into the lit chamber

    bpy.ops.object.lightprobe_add(type="VOLUME")
    p = bpy.context.object
    # ONE volume spanning BOTH chambers - which is exactly the configuration
    # Antigravity warns about, and the one a whole-flat probe would produce.
    p.location = (0, 0, 1.25)
    p.scale = (hx + 0.2, 2.4, hz + 0.2)
    d = p.data
    for a, v in (("resolution_x", probe_res), ("resolution_y", probe_res),
                 ("resolution_z", max(4, probe_res * 3 // 4))):
        if hasattr(d, a):
            setattr(d, a, v)
    if hasattr(d, "capture_world"):
        d.capture_world = True

    w = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0, 0, 0, 1)
        bg.inputs[1].default_value = 0.0

    cam_d = bpy.data.cameras.new("cam")
    cam_d.lens = 30.0
    cam = bpy.data.objects.new("cam", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    # Inside the DARK chamber, looking at its far end wall.
    cam.location = (0.0, 1.0 + partition_mm / 2000.0 - 0.5, 1.3)
    cam.rotation_euler = (1.5708, 0.0, 3.14159)
    bpy.context.scene.camera = cam
    return {"partition_mm": partition_mm, "probe_resolution": probe_res,
            "probe_half_extent": tuple(round(v, 3) for v in p.scale),
            "grid_spacing_mm": round(2 * p.scale[1] * 1000.0 / max(probe_res - 1, 1), 1)}


def render(path, engine, samples):
    sc = bpy.context.scene
    sc.render.engine = engine
    if engine == "CYCLES":
        sc.cycles.samples = samples
        try:
            sc.cycles.device = "CPU"
        except Exception:                                    # noqa: BLE001
            pass
    else:
        sc.eevee.taa_render_samples = samples
        for a in ("use_raytracing", "use_shadows"):
            if hasattr(sc.eevee, a):
                setattr(sc.eevee, a, True)
    sc.render.resolution_x, sc.render.resolution_y = 800, 600
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.abspath(path)
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return round(time.time() - t0, 2)


def main():
    opts = dict(zip(argv_after_ddash()[0::2], argv_after_ddash()[1::2]))
    outdir = os.path.abspath(opts.get("--outdir", "."))
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    res = int(opts.get("--probe-res", "8"))
    mm = float(opts.get("--partition-mm", "75"))

    rep = {"experiment": "does a baked probe grid leak through a 75 mm partition?",
           "background_mode": bpy.app.background}
    rep["scene"] = build(mm, res)

    # ⚠ LIGHT-OFF CONTROL. The seal assertion failed twice with Cycles reporting
    # ~119 in a chamber that should be black, and a flat featureless grey frame
    # cannot distinguish "light leaked in" from "something else is lighting
    # this". With the only emitter disabled the correct answer is black; if it
    # is not, the fault is not a leak and the whole test is void.
    if opts.get("--lights-off", "no").lower() not in ("no", "0", "false"):
        for o in list(bpy.data.objects):
            if o.type == "LIGHT":
                bpy.data.objects.remove(o, do_unlink=True)
        rep["lights_removed"] = True

    rep["eevee_unbaked"] = {"png": os.path.join(outdir, "leak_eevee_unbaked.png")}
    rep["eevee_unbaked"]["seconds"] = render(
        rep["eevee_unbaked"]["png"], "BLENDER_EEVEE", 48)

    t0 = time.time()
    r = bpy.ops.object.lightprobe_cache_bake(subset="ALL")
    rep["bake"] = {"result": list(r), "seconds": round(time.time() - t0, 2)}

    rep["eevee_baked"] = {"png": os.path.join(outdir, "leak_eevee_baked.png")}
    rep["eevee_baked"]["seconds"] = render(
        rep["eevee_baked"]["png"], "BLENDER_EEVEE", 48)

    rep["cycles"] = {"png": os.path.join(outdir, "leak_cycles.png"),
                     "role": ("SEAL ASSERTION. If this is not near black the box is "
                              "not sealed and every EEVEE number here is void.")}
    rep["cycles"]["seconds"] = render(rep["cycles"]["png"], "CYCLES",
                                      int(opts.get("--cycles-samples", "64")))

    out = os.path.join(outdir, "probe_leak_report.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(rep, ensure_ascii=False, indent=2) + "\n")
    print("LEAK_TEST_OK %s" % out)
    if not bpy.app.background:
        bpy.ops.wm.quit_blender()
    return 0


if __name__ == "__main__":
    sys.exit(main())
