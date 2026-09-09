#!/usr/bin/env python3
"""Draw the v0 model for review, with the problem walls called out.

Owner, 2026-09-09: *"Show me the image of what we have now... not in words, but
in picture... and show me the problematic places, walls, which need my
attention."*

So this renders what the model actually contains -- the placed named walls, the
openings, the лоджия glazing, the decorative slab, the suggested furniture --
over the source drawing in pale grey, and then marks every chain whose laid
length disagrees with the drawing's own span for it.

Colours are the owner's own key from
`_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg`.
"""
import argparse
import io
import json
import math
import os
import sys
import importlib.util

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PLACED = os.path.join("data", "canonical", "v0_named_walls_placed.json")
ELEMENTS = os.path.join("data", "canonical", "v0_elements_extracted.json")
PDF = os.path.join("_Inbox", "_Visual_Drop", "3Б_3+ МН5_287.pdf")

FILL = {
    "concrete": (232, 138, 138),
    "aerated_block": (150, 214, 160),
    "external": (240, 168, 226),
    "loggia_enclosure": (240, 168, 226),
}
EDGE = {
    "concrete": (176, 24, 24),
    "aerated_block": (24, 132, 48),
    "external": (196, 46, 172),
    "loggia_enclosure": (196, 46, 172),
}
BAD = (222, 40, 40)
WARN = (230, 140, 20)
OK_RESIDUAL_MM = 60.0
BAD_RESIDUAL_MM = 250.0


def font(size):
    for name in ("DejaVuSans.ttf", "arial.ttf", "seguisb.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join("_Drawings", "review", "v0_model_review.png"))
    ap.add_argument("--scale", type=float, default=0.155, help="px per mm")
    args = ap.parse_args()

    placed = json.load(io.open(PLACED, encoding="utf-8"))
    walls = [w for w in placed["walls"] if w.get("face_lo_mm") is not None]
    chains = {c["chain"]: c for c in placed["chains"]}
    elements = json.load(io.open(ELEMENTS, encoding="utf-8"))

    spec = importlib.util.spec_from_file_location(
        "ex", os.path.join(HERE, "extract_v0_walls.py"))
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    plan = ex._load_parser().parse(PDF)
    mm = ex.MM_PER_PT

    xs, ys = [], []
    for w in walls:
        if w["axis"] == "EW":
            xs += [w["from_mm"], w["to_mm"]]
            ys += [w["face_lo_mm"], w["face_hi_mm"]]
        else:
            xs += [w["face_lo_mm"], w["face_hi_mm"]]
            ys += [w["from_mm"], w["to_mm"]]
    gl = elements.get("loggia_glazing")
    if gl:
        xs += [gl["axis_from"][0], gl["axis_to"][0]]
        ys += [gl["axis_from"][1], gl["axis_to"][1]]
    PAD, LEGEND = 340, 520
    x0, x1, y0, y1 = min(xs) - PAD, max(xs) + PAD, min(ys) - PAD, max(ys) + PAD
    S = args.scale
    W = int((x1 - x0) * S) + LEGEND
    H = int((y1 - y0) * S)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    f_small, f_mid, f_big = font(15), font(19), font(26)

    def P(x, y):
        return ((x - x0) * S, H - (y - y0) * S)

    def box(x_0, y_0, x_1, y_1):
        a, b = P(x_0, y_0), P(x_1, y_1)
        return [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]

    # --- source drawing, pale, so the fit is visible -----------------
    for sx0, sy0, sx1, sy1 in plan["segments"]:
        dr.line([P(sx0 * mm, sy0 * mm), P(sx1 * mm, sy1 * mm)], fill=(226, 226, 226))

    # --- suggested furniture -----------------------------------------
    for d in elements.get("dashed_suggested_furniture") or []:
        if d["axis"] == "EW":
            a, b = P(d["from_mm"], d["line_mm"]), P(d["to_mm"], d["line_mm"])
        else:
            a, b = P(d["line_mm"], d["from_mm"]), P(d["line_mm"], d["to_mm"])
        n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 9))
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1.0, (i + 1) / n)
            dr.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                     (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                    fill=(235, 145, 20), width=3)

    # --- slab extension ----------------------------------------------
    for s in (elements.get("slab_extension_candidates") or [])[:1] or []:
        pass
    cands = elements.get("slab_extension_candidates") or []
    if cands:
        s = max(cands, key=lambda r: r["depth_mm"])
        dr.rectangle(box(s["x_from_mm"], s["y_from_mm"], s["x_to_mm"], s["y_to_mm"]),
                     fill=(252, 240, 176), outline=(196, 168, 20), width=2)

    # --- walls --------------------------------------------------------
    for w in walls:
        if w["axis"] == "EW":
            bx = box(w["from_mm"], w["face_lo_mm"], w["to_mm"], w["face_hi_mm"])
        else:
            bx = box(w["face_lo_mm"], w["from_mm"], w["face_hi_mm"], w["to_mm"])
        dr.rectangle(bx, fill=FILL.get(w["class"], (200, 200, 200)),
                     outline=EDGE.get(w["class"], (90, 90, 90)), width=2)

    # --- лоджия glazing ---------------------------------------------
    if gl:
        ax, ay = gl["axis_from"]
        bx_, by_ = gl["axis_to"]
        L = math.hypot(bx_ - ax, by_ - ay)
        ux, uy = (bx_ - ax) / L, (by_ - ay) / L
        nx, ny = -uy, ux
        d = gl["assembly_depth_mm"] or 150.0
        for kind, items, col in (("bay", gl["bays"], (120, 200, 235)),
                                 ("mul", gl["mullions"], (60, 90, 130))):
            for it in items:
                p0, p1 = it["from_mm"], it["to_mm"]
                pts = [P(ax + ux * p0, ay + uy * p0), P(ax + ux * p1, ay + uy * p1),
                       P(ax + ux * p1 + nx * d, ay + uy * p1 + ny * d),
                       P(ax + ux * p0 + nx * d, ay + uy * p0 + ny * d)]
                dr.polygon(pts, fill=col, outline=(30, 80, 120))

    # --- openings, so the walls are not read as solid ----------------
    import csv
    tx = placed["transform_basic_px_to_mm"]
    by_id = {w["wall_id"]: w for w in walls}
    for r in csv.DictReader(io.open(os.path.join("data", "canonical",
                                                 "wall_opening_spans.csv"),
                                    encoding="utf-8")):
        w = by_id.get(r["wall_id"])
        if not w:
            continue
        along = tx["x"] if w["axis"] == "EW" else tx["y"]
        a = along["a"] * float(r["span_lo_basic_px"]) + along["b"]
        b = along["a"] * float(r["span_hi_basic_px"]) + along["b"]
        lo, hi = min(a, b), max(a, b)
        if w["axis"] == "EW":
            bx = box(lo, w["face_lo_mm"], hi, w["face_hi_mm"])
        else:
            bx = box(w["face_lo_mm"], lo, w["face_hi_mm"], hi)
        dr.rectangle(bx, fill=(255, 255, 255), outline=(30, 120, 200), width=2)
        dr.text((bx[0] + 3, bx[1] + 2), r["opening_id"], fill=(30, 120, 200), font=f_small)

    # --- junctions BETWEEN chains: do the walls actually touch? ------
    # The owner's rule is that walls touch with no gap. make_contiguous()
    # only guarantees that INSIDE a chain; a corner is where two chains meet,
    # and nothing has been enforcing those.
    junction_gaps = []
    for cid, c in chains.items():
        members = [w for w in walls if w["chain"] == cid]
        if not members:
            continue
        axis = members[0]["axis"]
        f_lo, f_hi = members[0]["face_lo_mm"], members[0]["face_hi_mm"]
        for end_name, end in (("start", min(w["from_mm"] for w in members)),
                              ("end", max(w["to_mm"] for w in members))):
            best = None
            for oid, o in chains.items():
                if oid == cid:
                    continue
                om = [w for w in walls if w["chain"] == oid]
                if not om or om[0]["axis"] == axis:
                    continue
                o_lo, o_hi = om[0]["face_lo_mm"], om[0]["face_hi_mm"]
                o_from = min(w["from_mm"] for w in om)
                o_to = max(w["to_mm"] for w in om)
                # the other chain must straddle this chain's line
                if not (o_from - 200 <= (f_lo + f_hi) / 2 <= o_to + 200):
                    continue
                d = min(abs(end - o_lo), abs(end - o_hi))
                if best is None or d < best[0]:
                    best = (d, oid, o_lo, o_hi)
            if best and 6.0 < best[0] < 400.0:
                junction_gaps.append({"chain": cid, "walls": c["walls"],
                                      "end": end_name, "gap_mm": round(best[0], 1),
                                      "against": best[1],
                                      "at": (end, (f_lo + f_hi) / 2)})
    for j in junction_gaps:
        x, y = (j["at"][0], j["at"][1]) if [w for w in walls
                                            if w["chain"] == j["chain"]][0]["axis"] == "EW" \
            else (j["at"][1], j["at"][0])
        p = P(x, y)
        dr.ellipse([p[0] - 13, p[1] - 13, p[0] + 13, p[1] + 13],
                   outline=(40, 60, 220), width=4)

    # --- wall ids -----------------------------------------------------
    for w in walls:
        if w["axis"] == "EW":
            bx = box(w["from_mm"], w["face_lo_mm"], w["to_mm"], w["face_hi_mm"])
        else:
            bx = box(w["face_lo_mm"], w["from_mm"], w["face_hi_mm"], w["to_mm"])
        cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
        t = w["wall_id"]
        tw = dr.textlength(t, font=f_small)
        dr.rectangle([cx - tw / 2 - 2, cy - 9, cx + tw / 2 + 2, cy + 9],
                     fill=(255, 255, 255))
        dr.text((cx - tw / 2, cy - 8), t, fill=(20, 20, 20), font=f_small)

    # --- problem callouts --------------------------------------------
    problems = []
    for cid, c in chains.items():
        r = c["lay"]["residual_mm"]
        if abs(r) <= OK_RESIDUAL_MM:
            continue
        members = [w for w in walls if w["chain"] == cid]
        if not members:
            continue
        if members[0]["axis"] == "EW":
            bx = box(min(w["from_mm"] for w in members), members[0]["face_lo_mm"],
                     max(w["to_mm"] for w in members), members[0]["face_hi_mm"])
        else:
            bx = box(members[0]["face_lo_mm"], min(w["from_mm"] for w in members),
                     members[0]["face_hi_mm"], max(w["to_mm"] for w in members))
        col = BAD if abs(r) >= BAD_RESIDUAL_MM else WARN
        dr.rectangle([bx[0] - 5, bx[1] - 5, bx[2] + 5, bx[3] + 5], outline=col, width=4)
        problems.append((abs(r), r, ", ".join(c["walls"]), col, bx))

    problems.sort(reverse=True, key=lambda t: t[0])
    for _, r, names, col, bx in problems:
        lab = "%+d" % round(r)
        tw = dr.textlength(lab, font=f_mid)
        lx = min(W - LEGEND - tw - 8, max(4, bx[2] + 8))
        ly = max(4, bx[1] - 24)
        dr.rectangle([lx - 3, ly - 2, lx + tw + 3, ly + 22], fill=col)
        dr.text((lx, ly), lab, fill=(255, 255, 255), font=f_mid)

    # --- legend -------------------------------------------------------
    lx = W - LEGEND + 22
    y = 26
    dr.text((lx, y), "v0 — the developer's layout", fill=(0, 0, 0), font=f_big)
    y += 34
    dr.text((lx, y), "placed from the vector plan; DRAFT",
            fill=(110, 110, 110), font=f_small)
    y += 32
    for label, cls in (("concrete frame (R…)", "concrete"),
                       ("aerated block (G…)", "aerated_block"),
                       ("external 300 (MA/MB/MC)", "external"),
                       ("лоджия enclosure (M2/M6b)", "loggia_enclosure")):
        dr.rectangle([lx, y, lx + 30, y + 16], fill=FILL[cls], outline=EDGE[cls], width=2)
        dr.text((lx + 40, y), label, fill=(20, 20, 20), font=f_small)
        y += 24
    dr.rectangle([lx, y, lx + 30, y + 16], fill=(120, 200, 235), outline=(30, 80, 120))
    dr.text((lx + 40, y), "лоджия glazing, 4 bays", fill=(20, 20, 20), font=f_small)
    y += 24
    dr.rectangle([lx, y, lx + 30, y + 16], fill=(252, 240, 176), outline=(196, 168, 20))
    dr.text((lx + 40, y), "decorative slab 1800×370", fill=(20, 20, 20), font=f_small)
    y += 24
    for i in range(0, 30, 8):
        dr.line([(lx + i, y + 8), (lx + i + 4, y + 8)], fill=(235, 145, 20), width=3)
    dr.text((lx + 40, y), "SUGGESTED furniture — not built", fill=(20, 20, 20), font=f_small)
    y += 34

    dr.text((lx, y), "NEEDS YOUR ATTENTION", fill=BAD, font=f_mid)
    y += 26
    dr.text((lx, y), "chain span vs sum of recorded lengths",
            fill=(110, 110, 110), font=f_small)
    y += 22
    dr.rectangle([lx, y, lx + 30, y + 14], outline=BAD, width=4)
    dr.text((lx + 40, y), "≥ 250 mm out", fill=(20, 20, 20), font=f_small)
    y += 22
    dr.rectangle([lx, y, lx + 30, y + 14], outline=WARN, width=4)
    dr.text((lx + 40, y), "60–250 mm out", fill=(20, 20, 20), font=f_small)
    y += 30
    for _, r, names, col, _bx in problems:
        dr.text((lx, y), "%+6d  %s" % (round(r), names), fill=col, font=f_small)
        y += 20
    y += 14
    dr.ellipse([lx, y, lx + 22, y + 22], outline=(40, 60, 220), width=4)
    dr.text((lx + 34, y + 2), "chain END not touching the wall",
            fill=(40, 60, 220), font=f_small)
    y += 22
    dr.text((lx + 34, y), "it should meet — %d of them" % len(junction_gaps),
            fill=(40, 60, 220), font=f_small)
    y += 26
    for j in sorted(junction_gaps, key=lambda t: -t["gap_mm"])[:8]:
        dr.text((lx, y), "%6.0f mm  %s (%s)"
                % (j["gap_mm"], ", ".join(j["walls"]), j["end"]),
                fill=(40, 60, 220), font=f_small)
        y += 19

    y += 12
    dr.text((lx, y), "Also unresolved:", fill=(0, 0, 0), font=f_mid)
    y += 26
    for line in ("M2 / M6b drawn axis-aligned —",
                 "   the real лоджия walls splay",
                 "window frames in MA/MB/MC not read",
                 "no corner ownership yet",
                 "O10 passway has no span row",
                 "fixtures (blue in your markup) absent"):
        dr.text((lx, y), line, fill=(60, 60, 60), font=f_small)
        y += 19

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    img.save(args.out)
    print("wrote %s  %s" % (args.out, img.size))
    print("problem chains: %d" % len(problems))
    print("junction gaps  : %d" % len(junction_gaps))
    for j in sorted(junction_gaps, key=lambda t: -t["gap_mm"]):
        print("   %6.0f mm  %-22s %-5s vs %s"
              % (j["gap_mm"], ", ".join(j["walls"]), j["end"], j["against"]))
    for _, r, names, _c, _b in problems:
        print("   %+6d  %s" % (round(r), names))
    return 0


if __name__ == "__main__":
    sys.exit(main())
