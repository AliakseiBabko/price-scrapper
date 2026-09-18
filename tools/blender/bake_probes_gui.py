#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bake the light probe cache in a Blender that HAS a GPU context, then quit.

⚠️⚠️ WHY THIS EXISTS, AND WHY IT IS NOT A "GUI STEP".
The proof room measured a probe gain of 1.00x - the bake changed nothing - and
the leading hypothesis was that `lightprobe_cache_bake` cannot work under
`blender -b`. That was read, wrongly, as "a human must click Bake in the GUI".

The real distinction is **headless vs having an OpenGL/GPU context**, not
**script vs human**. Blender launched WITHOUT `-b` opens a window and creates
that context, and a `-P` script still drives everything and quits at the end. So
no clicking is required by anyone; what is required is a window.

⚠️ It therefore OPENS A WINDOW on the machine running it, briefly. That is the
whole cost, and it is why this is a separate script rather than a flag: it is the
one step in the pipeline that is not headless, and that should be visible in the
file list rather than buried.

⚠️ The bake is deferred through a TIMER. At the moment a startup `-P` script
runs, the window exists but the draw context may not be ready, and baking too
early is the same failure as baking headless - it returns FINISHED and produces
nothing. The timer lets Blender reach its event loop first.
"""

import json
import os
import sys
import time

import bpy

_STATE = {"started": time.time(), "done": False}


def _argv_after_ddash():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def _report(path, payload):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _bake():
    """Runs once, from Blender's own event loop, then quits."""
    if _STATE["done"]:
        return None
    _STATE["done"] = True

    opts = dict(zip(_argv_after_ddash()[0::2], _argv_after_ddash()[1::2]))
    blend = os.path.abspath(opts.get("--blend"))
    out = opts.get("--report") or (os.path.splitext(blend)[0] + "_bake_report.json")

    payload = {
        "blend": blend,
        "blender_version": bpy.app.version_string,
        "background_mode": bpy.app.background,
        "note": ("background_mode False is the point - a light cache needs the GPU "
                 "context that `blender -b` does not create"),
    }

    probes = [o for o in bpy.data.objects if o.type == "LIGHT_PROBE"]
    payload["light_probes"] = [o.name for o in probes]
    if not probes:
        payload["status"] = "FAILED - no light probe in the file, nothing to bake"
        _report(out, payload)
        bpy.ops.wm.quit_blender()
        return None

    try:
        t0 = time.time()
        res = bpy.ops.object.lightprobe_cache_bake(subset="ALL")
        payload["bake_result"] = list(res)
        payload["bake_seconds"] = round(time.time() - t0, 2)
        payload["status"] = "ok"
    except Exception as exc:                                  # noqa: BLE001
        payload["status"] = "FAILED"
        payload["error"] = str(exc)
        _report(out, payload)
        bpy.ops.wm.quit_blender()
        return None

    # ⚠ SAVE, or the cache dies with the process. The cache lives in the file,
    # and the whole point is to render from it afterwards.
    try:
        bpy.ops.wm.save_mainfile(filepath=blend)
        payload["saved"] = True
        payload["blend_bytes_after"] = os.path.getsize(blend)
    except Exception as exc:                                  # noqa: BLE001
        payload["saved"] = False
        payload["save_error"] = str(exc)

    payload["total_seconds"] = round(time.time() - _STATE["started"], 2)
    _report(out, payload)
    print("BAKE_DONE %s" % out)
    bpy.ops.wm.quit_blender()
    return None


# 1.0 s is enough for the event loop to come up; the timer fires once because
# _bake returns None.
bpy.app.timers.register(_bake, first_interval=1.0)
