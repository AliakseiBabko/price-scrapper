#!/usr/bin/env python3
"""Read a vector (CAD-exported) floor-plan PDF as geometry rather than as a picture.

The developer's plans arrived in this project as rasters, so every dimension had
to be traced through a registration transform. `_Inbox/_Visual_Drop/3Б_3+ МН5_287.pdf`
is a real ArchiCAD export, and this reads its line work and its dimension labels
directly.

Subcommands
-----------
  parse   <pdf> <out.json>      line segments + placed glyphs, in PDF points
  labels  <plan.json>           reassemble glyphs into strings (dimensions, marks)
  scale   <plan.json>           derive mm-per-point by pairing labels with the
                                dimension lines they annotate
  render  <plan.json> <out.png> rasterise the line work, to eyeball handedness
  chains  <plan.json> [a+b+c=x] test that a dimension chain closes on the geometry

!! The scale MUST come from `scale`, never from a fit of segment lengths onto
round millimetres. Such a fit cannot separate a scale from twice that scale --
every 5 mm multiple is also a 10 mm multiple -- and on this drawing it returned
1:150 for a drawing that is 1:75. See 00_Master/Evidence_Reading_Discipline.md.

!! Dimensions read here are the developer's PROJECT dimensions. The sheet itself
says the as-built may differ, and this repo measures that difference at +1.0% to
+1.9% (the drawing reads LARGER). Do not treat 0.1 mm agreement as build accuracy.
"""

import json
import math
import re
import sys
import zlib
from collections import defaultdict

# glyph advances as a fraction of font size, calibrated against strings whose
# content is known ("ТИП 22", "45,49"); good enough to rejoin split numbers.
W_DIGIT, W_PUNCT, W_SPACE, W_LETTER = 0.453, 0.227, 0.230, 0.590
JOIN = 0.30            # label join tolerance, in font sizes
BS = chr(92)


# --------------------------------------------------------------------------- parse

def _streams(data):
    for m in re.finditer(rb"(\d+) (\d+) obj(.*?)endobj", data, re.S):
        body = m.group(3)
        s = re.search(rb"stream\r?\n(.*?)\r?\nendstream", body, re.S)
        if not s:
            continue
        raw = s.group(1)
        if b"FlateDecode" in body:
            try:
                raw = zlib.decompress(raw)
            except Exception:
                continue
        yield raw


_ESC = {"n": 10, "r": 13, "t": 9, "b": 8, "f": 12}


def _unescape(s):
    """PDF literal-string escapes -> bytes. Octal codes carry the CIDs here."""
    out, i, n = bytearray(), 0, len(s)
    while i < n:
        c = s[i]
        if c != BS:
            out.append(ord(c) & 0xFF)
            i += 1
            continue
        i += 1
        if i >= n:
            break
        c = s[i]
        if c.isdigit():
            oct_digits = ""
            while i < n and len(oct_digits) < 3 and s[i] in "01234567":
                oct_digits += s[i]
                i += 1
            out.append(int(oct_digits, 8) & 0xFF)
        else:
            out.append(_ESC.get(c, ord(c) & 0xFF))
            i += 1
    return bytes(out)


def _mat_mul(a, b):
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (a0 * b0 + a1 * b2, a0 * b1 + a1 * b3,
            a2 * b0 + a3 * b2, a2 * b1 + a3 * b3,
            a4 * b0 + a5 * b2 + b4, a4 * b1 + a5 * b3 + b5)


def _apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def parse(pdf_path):
    """Content stream -> device-space segments and placed glyph runs."""
    data = open(pdf_path, "rb").read()
    content = None
    for s in _streams(data):
        if len(re.findall(rb"\d \d+\.?\d* l", s)) > 100:
            content = s
            break
    if content is None:
        sys.exit("no drawing content stream found in %s" % pdf_path)

    txt = content.decode("latin-1")
    num = r"-?\d+\.?\d*(?:e-?\d+)?"
    string = r"\((?:" + BS + BS + r".|[^()" + BS + BS + r"])*\)"
    token = re.compile(
        "(?P<num>" + num + ")|(?P<str>" + string + r")|(?P<name>/[^\s/\[\]<>(]+)|"
        r"(?P<op>[A-Za-z'" + chr(34) + r"*]+)|(?P<other>[\[\]<>{}])", re.S)

    ctm = (1, 0, 0, 1, 0, 0)
    tm = tlm = (1, 0, 0, 1, 0, 0)
    gstack, segs, texts, stackv = [], [], [], []
    cur = start = None
    tfs = 1.0
    # PDF draws a dashed line as ONE path with a dash pattern, so without
    # tracking the `d` operator a dashed line is indistinguishable from a solid
    # one. On this drawing the dashed lines are the developer's SUGGESTED
    # FURNITURE, which must never be mistaken for built fabric.
    dashed = False
    dash_flags = []

    for m in token.finditer(txt):
        if m.group("num") is not None:
            stackv.append(float(m.group("num")))
            continue
        if m.group("str") is not None:
            stackv.append(("str", m.group("str")[1:-1]))
            continue
        if m.group("name") is not None:
            stackv.append(("name", m.group("name")))
            continue
        if m.group("op") is None:
            continue
        op, a, stackv = m.group("op"), stackv, []
        nums = [v for v in a if isinstance(v, float)]
        try:
            if op == "q":
                gstack.append((ctm, dashed))
            elif op == "Q":
                if gstack:
                    ctm, dashed = gstack.pop()
            elif op == "d":
                # "[] 0 d" is solid and yields exactly one number (the phase);
                # any real pattern yields the array entries as well.
                dashed = len(nums) > 1
            elif op == "cm" and len(nums) >= 6:
                ctm = _mat_mul(tuple(nums[-6:]), ctm)
            elif op == "m" and len(nums) >= 2:
                cur = start = (nums[-2], nums[-1])
            elif op in ("l", "v", "y", "c") and len(nums) >= 2:
                p = (nums[-2], nums[-1])
                if cur is not None:
                    segs.append(_apply(ctm, *cur) + _apply(ctm, *p))
                    dash_flags.append(dashed)
                cur = p
            elif op == "h" and cur is not None and start is not None:
                segs.append(_apply(ctm, *cur) + _apply(ctm, *start))
                dash_flags.append(dashed)
                cur = start
            elif op == "re" and len(nums) >= 4:
                x, y, w, h = nums[-4:]
                pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
                for i in range(4):
                    segs.append(_apply(ctm, *pts[i]) + _apply(ctm, *pts[i + 1]))
                    dash_flags.append(dashed)
            elif op == "Tf" and nums:
                tfs = nums[-1]
            elif op == "BT":
                tm = tlm = (1, 0, 0, 1, 0, 0)
            elif op == "Tm" and len(nums) >= 6:
                tm = tlm = tuple(nums[-6:])
            elif op in ("Td", "TD") and len(nums) >= 2:
                tlm = _mat_mul((1, 0, 0, 1, nums[-2], nums[-1]), tlm)
                tm = tlm
            elif op in ("Tj", "'") and a and isinstance(a[-1], tuple):
                full = _mat_mul(tm, ctm)
                texts.append((full[4], full[5], a[-1][1], full[0], full[1], tfs))
        except Exception:
            pass

    out_texts = []
    for x, y, s, ax, ay, fs in texts:
        b = _unescape(s)
        try:
            u = b.decode("utf-16-be")          # ArchiCAD writes 2-byte CIDs
        except Exception:
            continue
        out_texts.append({"x": round(x, 4), "y": round(y, 4), "t": u,
                          "ang": round(math.degrees(math.atan2(ay, ax)), 2),
                          "sc": round(math.hypot(ax, ay) * fs, 4)})
    return {"segments": [[round(v, 4) for v in s] for s in segs],
            "dashed": [i for i, f in enumerate(dash_flags) if f],
            "texts": out_texts}


# -------------------------------------------------------------------------- labels

def _advance(s):
    w = 0.0
    for c in s:
        if c.isdigit():
            w += W_DIGIT
        elif c in ",.-/":
            w += W_PUNCT
        elif c.isspace() or c in "   ":
            w += W_SPACE
        else:
            w += W_LETTER
    return w


def labels(plan):
    """Glyph runs -> strings. Handles rotated dimension text and thin-space
    thousands separators, which otherwise split '1 795' into '1' and '795'."""
    texts = plan["texts"]
    for t in texts:
        a = math.radians(t["ang"])
        t["u"] = t["x"] * math.cos(a) + t["y"] * math.sin(a)
        t["v"] = -t["x"] * math.sin(a) + t["y"] * math.cos(a)
    texts.sort(key=lambda t: (round(t["ang"]), -round(t["v"], 1), t["u"]))

    groups, cur = [], None
    for t in texts:
        join = False
        if (cur is not None and abs(t["ang"] - cur["ang"]) < 0.5
                and abs(t["v"] - cur["v"]) < 0.6
                and abs(t["sc"] - cur["sc"]) < 0.2):
            join = abs(t["u"] - (cur["u"] + cur["sc"] * _advance(cur["s"]))) \
                <= JOIN * cur["sc"]
        if join:
            cur["s"] += t["t"]
        else:
            if cur:
                groups.append(cur)
            cur = dict(t, s=t["t"])
    if cur:
        groups.append(cur)

    dims, other = [], []
    for g in groups:
        g["s"] = re.sub(r"[\s   ]+", " ", g["s"]).strip()
        if re.fullmatch(r"\d[\d ]*", g["s"]):
            v = int(g["s"].replace(" ", ""))
            if 50 <= v <= 20000:
                dims.append(dict(v=v, x=g["x"], y=g["y"], ang=g["ang"], sc=g["sc"]))
                continue
        if g["s"]:
            other.append(g)
    return dims, other


# --------------------------------------------------------------------------- scale

def scale(plan, dims):
    """mm per point, from label-to-dimension-line pairs. Returns (k, pairs)."""
    segs = plan["segments"]
    hor = [(min(s[0], s[2]), max(s[0], s[2]), s[1]) for s in segs
           if abs(s[1] - s[3]) < 1e-6]
    ver = [(min(s[1], s[3]), max(s[1], s[3]), s[0]) for s in segs
           if abs(s[0] - s[2]) < 1e-6]

    pairs = []
    for d in dims:
        v, x, y, ang = d["v"], d["x"], d["y"], d["ang"]
        best = None
        horizontal = abs(ang) < 1 or abs(abs(ang) - 180) < 1
        for a, b, c in (hor if horizontal else ver):
            off = (y - c if abs(ang) < 1 else c - y) if horizontal else \
                  (x - c if abs(ang - 90) < 1 else c - x)
            if not 0.3 <= off <= 4.5:
                continue
            along = x if horizontal else y
            if a - 1.0 <= along <= b + 1.0 and (b - a) > 0.4:
                if best is None or (b - a) < best:
                    best = b - a
        if best:
            pairs.append((v, best))
    if not pairs:
        sys.exit("no label could be paired with a dimension line")
    ratios = sorted(v / L for v, L in pairs)
    return ratios[len(ratios) // 2], pairs


# -------------------------------------------------------------------- wall-face grid

def grid(plan, mm_per_pt, min_run_mm=120.0, tol_mm=3.0):
    """Axis-aligned line positions in mm, clustered. Returns (xs, ys)."""
    vert, horz = defaultdict(float), defaultdict(float)
    for x0, y0, x1, y1 in plan["segments"]:
        if abs(y1 - y0) < 1e-6 and abs(x1 - x0) * mm_per_pt >= min_run_mm:
            horz[round(y0 * mm_per_pt, 2)] += abs(x1 - x0) * mm_per_pt
        elif abs(x1 - x0) < 1e-6 and abs(y1 - y0) * mm_per_pt >= min_run_mm:
            vert[round(x0 * mm_per_pt, 2)] += abs(y1 - y0) * mm_per_pt

    def clust(dct):
        out = []
        for k in sorted(dct):
            if out and k - out[-1] <= tol_mm:
                continue
            out.append(k)
        return out
    return clust(vert), clust(horz)


def check_chain(lines, parts, tol=3.0):
    """Every placement where the chain's intermediate lines all exist."""
    hits = []
    for a in lines:
        pos, path, ok = a, [a], True
        for p in parts:
            pos += p
            m = [c for c in lines if abs(c - pos) <= tol]
            if not m:
                ok = False
                break
            path.append(m[0])
        if ok:
            hits.append(path)
    return hits


# -------------------------------------------------------------------------- render

def render(plan, out_png, px_per_pt=2.2):
    from PIL import Image, ImageDraw
    segs = plan["segments"]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * px_per_pt) + 20
    H = int((max(ys) - y0) * px_per_pt) + 20
    img = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(img)
    for s in segs:
        dr.line([((s[0] - x0) * px_per_pt + 10, H - ((s[1] - y0) * px_per_pt + 10)),
                 ((s[2] - x0) * px_per_pt + 10, H - ((s[3] - y0) * px_per_pt + 10))],
                fill="black")
    img.save(out_png)
    return img.size


# ----------------------------------------------------------------------------- cli

def _load(path):
    return json.load(open(path, encoding="utf-8"))


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd = argv[1]

    if cmd == "parse":
        plan = parse(argv[2])
        json.dump(plan, open(argv[3], "w", encoding="utf-8"), ensure_ascii=False)
        print("segments %d   glyph runs %d" % (len(plan["segments"]), len(plan["texts"])))
        return 0

    plan = _load(argv[2])

    if cmd == "render":
        print("wrote %s %s" % (argv[3], render(plan, argv[3])))
        return 0

    dims, other = labels(plan)

    if cmd == "labels":
        print("=== %d dimension labels ===" % len(dims))
        print(sorted(d["v"] for d in dims))
        print("\n=== other labels ===")
        for g in other:
            print("  ang=%5.0f (%7.2f,%7.2f)  %s" % (g["ang"], g["x"], g["y"], g["s"]))
        return 0

    k, pairs = scale(plan, dims)
    if cmd == "scale":
        print("mm per point = %.4f   ->  paper scale 1:%.3f" % (k, k * 72 / 25.4))
        agree = sum(1 for v, L in pairs if abs(L * k - v) <= max(2.0, 0.004 * v))
        print("%d of %d paired labels agree with the geometry within "
              "max(2 mm, 0.4%%)" % (agree, len(pairs)))
        for v, L in sorted(pairs):
            print("   label %6d   geometry %8.1f mm   err %+6.1f" % (v, L * k, L * k - v))
        return 0

    if cmd == "chains":
        vx, hy = grid(plan, k)
        specs = argv[3:] or []
        if not specs:
            print("give chains as 1795+120+910=x  (axis x or y)")
            return 2
        rc = 0
        for spec in specs:
            body, axis = spec.rsplit("=", 1)
            parts = [int(p) for p in body.split("+")]
            hits = check_chain(vx if axis == "x" else hy, parts)
            print("%-34s sum=%5d  %s" % (body, sum(parts),
                                         "CLOSES" if hits else "NOT FOUND"))
            for p in hits[:2]:
                print("     at %.1f : %s = %.1f"
                      % (p[0], " + ".join("%.1f" % (p[i + 1] - p[i])
                                          for i in range(len(p) - 1)), p[-1] - p[0]))
            if not hits:
                rc = 1
        return rc

    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
