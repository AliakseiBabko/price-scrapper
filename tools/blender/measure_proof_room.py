#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Measures the proof-room renders. Turns "it looks right" into a number.

⚠️⚠️ THIS IS THE HALF THAT MAKES THE EXPERIMENT AN EXPERIMENT.
`proof_room.py` produces pictures, and a picture that looks plausible is exactly
the "persuasive visualization" Codex named as the biggest risk in this project.
So nothing here is judged by eye:

  SCALE - the calibration texture carries a red corner wedge once per 1000 mm.
  The orthographic camera has a known mm-per-pixel, so the wedge spacing in the
  PNG is a direct reading of the APPLIED texture scale. Expected spacing is
  1000 / mm_per_px pixels; anything else is a scale error with a known factor.

  GI - the question is whether turning away from the window collapses the
  indirect light. That is a comparison of two frames' luminance, and it is the
  RATIO that matters, not either absolute value. Screen-space-only GI would put
  the away frame far below the toward frame; baked probes should hold it up.
"""

import json
import os
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def red_wedge_columns(img, min_run=3):
    """x positions of the texture's red corner wedge.

    The wedge is the one saturated red thing in the scene, so it survives being
    lit, shaded and box-projected. Everything else in the calibration image is
    neutral by design, which is why the marker was made red in the first place.
    """
    w, h = img.size
    px = img.convert("RGB").load()
    score = [0] * w
    for x in range(w):
        n = 0
        for y in range(0, h, 4):
            r, g, b = px[x, y]
            # ⚠ NO ABSOLUTE BRIGHTNESS FLOOR. The first version also required
            # r > 55 and found nothing: the marker renders at r ~= 51 in an
            # interior lit only by one window, so the test was rejecting the
            # very pixels it existed to find. CHROMA is the signal, not
            # brightness - a dark red is still the only red in the scene.
            if r > g + 20 and r > b + 20:
                n += 1
        score[x] = n
    peak = max(score) if score else 0
    if peak == 0:
        return [], score
    thresh = max(2, peak * 0.35)
    cols, run = [], []
    for x in range(w):
        if score[x] >= thresh:
            run.append(x)
        elif run:
            if len(run) >= min_run:
                cols.append(sum(run) / float(len(run)))
            run = []
    if run and len(run) >= min_run:
        cols.append(sum(run) / float(len(run)))

    # ⚠⚠ MERGE THE PARTS OF ONE MARKER INTO ONE MARKER.
    # The wedge is a TRIANGLE ~200 mm across, so a column scan finds its two
    # dense edges separately. Ungrouped, that produced alternating gaps of 38
    # and 362 px, a mean of 167.6, and a confident report that the texture was
    # applied at 419 mm instead of 1000 - a 58% error that was entirely in the
    # MEASUREMENT, not in the thing measured. The period is the sum of the two,
    # exactly 400.0 px. Anything closer together than half the smallest credible
    # period is one marker seen twice.
    if len(cols) > 2:
        spans = sorted(b - a for a, b in zip(cols, cols[1:]))
        merge_below = max(spans[-1] * 0.5, 4.0)
        grouped, bucket = [], [cols[0]]
        for prev, cur in zip(cols, cols[1:]):
            if cur - prev < merge_below:
                bucket.append(cur)
            else:
                grouped.append(sum(bucket) / float(len(bucket)))
                bucket = [cur]
        grouped.append(sum(bucket) / float(len(bucket)))
        cols = grouped
    return cols, score


def mean_luma(path, box=None):
    img = Image.open(path).convert("RGB")
    if box:
        img = img.crop(box)
    px = img.load()
    w, h = img.size
    total, n = 0.0, 0
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            total += 0.2126 * r + 0.7152 * g + 0.0722 * b
            n += 1
    return round(total / max(n, 1), 2)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "data", "outputs", "proof_room")
    rep_path = os.path.join(outdir, "proof_room_report.json")
    with open(rep_path, encoding="utf-8") as fh:
        rep = json.load(fh)

    result = {"measured_from": rep_path, "ifc_sha256": rep.get("ifc_sha256")}

    # ---------------- SCALE ----------------
    ortho = rep["renders"]["ortho_south"]
    mm_px = ortho["mm_per_px"]
    img = Image.open(os.path.join(outdir, "ortho_south.png"))
    cols, _ = red_wedge_columns(img)
    gaps = [round(b - a, 2) for a, b in zip(cols, cols[1:])]
    expected_px = 1000.0 / mm_px
    scale = {
        "marker_period_mm": 1000.0,
        "mm_per_px": mm_px,
        "expected_marker_spacing_px": round(expected_px, 2),
        "wedge_columns_px": [round(c, 1) for c in cols],
        "observed_gaps_px": gaps,
    }
    if gaps:
        mean_gap = sum(gaps) / len(gaps)
        applied_mm = mean_gap * mm_px
        scale["mean_gap_px"] = round(mean_gap, 2)
        scale["APPLIED_TILE_MM"] = round(applied_mm, 1)
        scale["error_mm"] = round(applied_mm - 1000.0, 1)
        scale["error_pct"] = round((applied_mm - 1000.0) / 10.0, 2)
        scale["VERDICT"] = ("PASS - the texture is applied at its stated physical size"
                            if abs(applied_mm - 1000.0) <= 25.0 else
                            "FAIL - applied scale is wrong by %.1f mm in 1000"
                            % (applied_mm - 1000.0))
    else:
        scale["VERDICT"] = "INCONCLUSIVE - no calibration marker found in the render"
    result["scale_test"] = scale

    # ---------------- GI, AS A CONTROLLED COMPARISON ----------------
    # ⚠⚠ THE FIRST VERSION OF THIS TEST WAS INVALID. It compared the
    # toward-window frame against the away frame and reported a ratio of 1.756 -
    # the away frame BRIGHTER - and then called that a PASS. Two different views
    # differ in what they contain, not only in how they are lit, so the number
    # measured framing rather than light. The control is the SAME camera with the
    # probe bake on and off; then the only variable is the thing under test.
    away_baked = os.path.join(outdir, "away_from_window.png")
    away_ctrl = os.path.join(outdir, "away_from_window_noprobe.png")
    gi = {"what_it_tests": ("whether BAKED PROBES carry indirect light into a view "
                            "with the window behind the camera - the case "
                            "screen-space tracing cannot serve."),
          "method": "same camera, same samples; probe bake ON vs OFF"}
    if os.path.exists(away_ctrl):
        lb, lc = mean_luma(away_baked), mean_luma(away_ctrl)
        gi["away_with_probes_mean_luma"] = lb
        gi["away_without_probes_mean_luma"] = lc
        gain = round(lb / lc, 3) if lc else None
        gi["probe_gain"] = gain
        if gain is None:
            gi["VERDICT"] = "INCONCLUSIVE - control frame is black"
        elif gain >= 1.25:
            gi["VERDICT"] = ("PASS - baking the probes lifts the away-facing view to "
                             "%.2fx the unbaked one, so indirect light DOES survive "
                             "the window leaving frame. The screen-space limit is "
                             "real and the probes are the documented answer to it."
                             % gain)
        elif gain >= 1.05:
            gi["VERDICT"] = ("MARGINAL - %.2fx. The probes contribute, but little at "
                             "this resolution and bake setting." % gain)
        else:
            gi["VERDICT"] = ("UNRESOLVED - %.2fx. The probe bake contributes NO "
                             "measurable light to this view, so question 1 is NOT "
                             "answered by this run." % gain)
            gi["leading_hypothesis"] = (
                "the bake does not work under `blender -b`. The probe object is "
                "created, is a LightProbeVolume, and lightprobe_cache_bake returns "
                "FINISHED - but a light cache normally needs a GPU context that "
                "headless Blender does not have, and there is no cache_info "
                "attribute to confirm the cache holds data. The baked run IS about "
                "2x slower per frame, so something is being computed; it just does "
                "not change the light.")
            gi["what_would_settle_it"] = (
                "bake once in the Blender GUI, save the .blend with its cache, then "
                "render headless FROM that file. That separates 'EEVEE cannot' from "
                "'headless cannot bake', which this run cannot distinguish.")
            gi["what_must_NOT_be_concluded"] = (
                "that EEVEE cannot carry indirect light out of frame. Blender's own "
                "5.2 documentation says screen tracing falls back to probes, and "
                "nothing here contradicts that - the experiment failed to TEST it.")
        # Both frames also reported raw, so nobody has to trust the ratio alone.
        gi["towards_window_mean_luma_for_reference"] = mean_luma(
            os.path.join(outdir, "towards_window.png"))
        gi["why_the_reference_is_not_the_test"] = (
            "a different view; included only so the numbers can be sanity-checked")
    else:
        gi["VERDICT"] = ("INCONCLUSIVE - no control run. Re-run proof_room.py with "
                         "--bake no --suffix _noprobe")
    result["gi_test"] = gi

    # ---------------- COST ----------------
    result["cost"] = {
        "total_run_seconds": rep.get("total_seconds"),
        "probe_bake_seconds": (rep.get("probe_bake") or {}).get("seconds"),
        "per_render_seconds": {k: v.get("seconds") for k, v in rep["renders"].items()},
        "samples": rep["eevee"]["samples"],
        "note": ("headless CPU render. The recorded recipe's '2K in 6 seconds' is a "
                 "GPU VIEWPORT figure and is not comparable - that distinction is the "
                 "difference between a walkthrough being interactive and not."),
    }
    result["uv_premise"] = {
        "meshes": rep.get("mesh_objects"),
        "with_uv_maps": rep.get("mesh_objects_with_uv_maps"),
        "finding": rep.get("uv_finding"),
    }

    out = os.path.join(outdir, "proof_room_measurements.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    print("SCALE : %s" % scale.get("VERDICT"))
    if gaps:
        print("        marker every %.1f px expected %.1f -> applied tile %.1f mm"
              % (scale["mean_gap_px"], expected_px, scale["APPLIED_TILE_MM"]))
    print("GI    : %s" % gi.get("VERDICT"))
    if "probe_gain" in gi:
        print("        away with probes %.1f  without %.1f  gain %s"
              % (gi["away_with_probes_mean_luma"],
                 gi["away_without_probes_mean_luma"], gi["probe_gain"]))
    print("UV    : %s of %s meshes have UV maps"
          % (rep.get("mesh_objects_with_uv_maps"), rep.get("mesh_objects")))
    print("wrote : %s" % os.path.relpath(out, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
