# -*- coding: utf-8 -*-
"""Three album sheets in the style of the owner's reference album
(Вероника Романова, project 5443509): title top-left, legend beneath it,
footer, a вертикальная Лист tab, a light plan, and coloured symbols ATTACHED TO
WALLS with H= tags in centimetres.

The fix he asked for: every wall-mounted item is placed on a named wall at a
fraction along it and offset to the correct FACE, so nothing floats mid-room.
"""
import csv, io, math, os, shutil
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
os.chdir(REPO)
HERE = os.path.join(REPO, '_Drawings', 'sheets')
MMPX = 9.789
S = 3
PAD_L, PAD_T, PAD_R, PAD_B = 660, 200, 90, 150

RUNS = {}
for r in csv.DictReader(io.open('data/canonical/wall_runs.csv', encoding='utf-8')):
    RUNS[r['wall_id']] = (float(r['ax_basic_px']), float(r['ay_basic_px']),
                          float(r['bx_basic_px']), float(r['by_basic_px']),
                          float(r['thickness_mm']))


def F(sz, bold=False):
    for n in (('arialbd.ttf', 'DejaVuSans-Bold.ttf') if bold else ('arial.ttf', 'DejaVuSans.ttf')):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            continue
    return ImageFont.load_default()


f_ttl, f_leg, f_leghd, f_tag, f_ft, f_tab, f_note = (F(78), F(30), F(30), F(23, True),
                                                     F(34), F(40), F(26))


SPANS = {}
for _r in csv.DictReader(io.open('data/canonical/wall_opening_spans.csv', encoding='utf-8')):
    SPANS.setdefault(_r['wall_id'], []).append(
        (_r['opening_id'], float(_r['span_lo_basic_px']),
         float(_r['span_hi_basic_px']), float(_r['sill_height_mm'])))


def _axis(wid):
    """(varying-axis value at a, at b) for the wall's own run direction"""
    ax, ay, bx, by, th = RUNS[wid]
    return (ax, bx) if abs(bx - ax) >= abs(by - ay) else (ay, by)


def beside_opening(wid, oid, jamb, clear_mm=170):
    """t for a point `clear_mm` clear of one jamb of a named opening.

    jamb is 'lo' or 'hi'. This is how a switch gets placed: next to the door,
    not at an arbitrary fraction along the wall.
    """
    a, b = _axis(wid)
    for o, lo, hi, sill in SPANS.get(wid, []):
        if o != oid:
            continue
        d = clear_mm / MMPX
        v = (lo - d) if jamb == 'lo' else (hi + d)
        return (v - a) / (b - a)
    raise KeyError('%s has no opening %s' % (wid, oid))


def opening_conflict(wid, t, height_mm):
    """the opening this point falls inside and must not, or None.

    An item inside an opening is only wrong if it sits ABOVE that opening's
    sill - a socket at H=30 below a 266 window sill is legitimate; a switch at
    H=90 in a door opening is not.
    """
    a, b = _axis(wid)
    v = a + (b - a) * t
    for o, lo, hi, sill in SPANS.get(wid, []):
        if lo <= v <= hi and height_mm > sill:
            return o
    return None


def on_wall(wid, t, side):
    """point on a wall face + the outward normal. t is 0..1 along the run,
    side is +1 / -1 for which face."""
    ax, ay, bx, by, th = RUNS[wid]
    x, y = ax + (bx - ax) * t, ay + (by - ay) * t
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = -uy * side, ux * side
    off = th / 2.0 / MMPX
    return x + nx * off, y + ny * off, nx, ny


class Sheet(object):
    def __init__(self, title, sheet_no):
        im = Image.open('_Inbox/_Visual_Drop/floor_plan_basic.jpg').convert('RGB')
        im = im.resize((1061 * S, 1113 * S), Image.LANCZOS)
        im = Image.blend(im, Image.new('RGB', im.size, 'white'), 0.80)
        self.pw, self.ph = im.size
        self.im = Image.new('RGB', (self.pw + PAD_L + PAD_R, self.ph + PAD_T + PAD_B), 'white')
        self.im.paste(im, (PAD_L, PAD_T))
        self.d = ImageDraw.Draw(self.im, 'RGBA')
        self.title, self.no = title, sheet_no
        self.placed = []
        W, H = self.im.size
        self.d.rectangle([26, 26, W - 26, H - 26], outline=(120, 120, 120), width=3)
        self.d.text((70, 96), title, fill=(30, 30, 30), font=f_ttl, anchor='lm')
        self.d.text((70, 196), u'Условные обозначения:', fill=(130, 130, 130), font=f_leghd, anchor='lm')
        self.d.rectangle([26, H - 430, 96, H - 26], fill=(232, 150, 40))
        tb = Image.new('RGBA', (330, 60), (0, 0, 0, 0))
        ImageDraw.Draw(tb).text((0, 30), u'Лист %d' % sheet_no, fill=(255, 255, 255), font=f_tab, anchor='lm')
        self.im.paste(tb.rotate(90, expand=True), (34, H - 415), tb.rotate(90, expand=True))
        self.d.text((70, H - 80), u'ЖК Дубравинский, 3Б/2+, 4-й этаж',
                    fill=(40, 40, 40), font=f_ft, anchor='lm')
        self.d.text((W // 2, H - 80), u'модель из data/canonical \u00b7 %s' % u'2026-09-07',
                    fill=(40, 40, 40), font=f_ft, anchor='mm')
        self.d.text((W - 70, H - 80), u'Aliaksei Babko', fill=(40, 40, 40), font=f_ft, anchor='rm')
        self.ly = 262

    def P(self, p):
        return (p[0] * S + PAD_L, p[1] * S + PAD_T)

    def spot(self, cx, cy, w, h):
        for r in range(0, 46):
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
                           (1, 1), (-1, -1), (1, -1), (-1, 1)):
                x, y = cx + dx * r * 13, cy + dy * r * 13
                b = (x - w / 2 - 4, y - h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4)
                if all(b[2] < q[0] or b[0] > q[2] or b[3] < q[1] or b[1] > q[3] for q in self.placed):
                    self.placed.append(b); return x, y
        self.placed.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)); return cx, cy

    # ---------------------------------------------------------------- symbols
    def sym_socket(self, x, y, nx, ny, col, gang=1, ip=False):
        """semicircle on the wall with a stem, the standard socket symbol"""
        r = 21
        cx, cy = x + nx * r, y + ny * r
        a = math.degrees(math.atan2(ny, nx))
        self.d.arc([cx - r, cy - r, cx + r, cy + r], a - 90, a + 90, fill=col, width=6)
        px, py = -ny, nx
        self.d.line([(cx - px * r, cy - py * r), (cx + px * r, cy + py * r)], fill=col, width=6)
        self.d.line([(x, y), (cx, cy)], fill=col, width=6)
        for k in range(gang):
            o = (k - (gang - 1) / 2.0) * 11
            self.d.line([(cx + px * o, cy + py * o),
                         (cx + px * o + nx * 13, cy + py * o + ny * 13)], fill=col, width=5)
        if ip:
            self.d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)

    def sym_switch(self, x, y, nx, ny, col, gang=1):
        r = 13
        cx, cy = x + nx * (r + 6), y + ny * (r + 6)
        self.d.line([(x, y), (cx, cy)], fill=col, width=6)
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=col, width=5)
        px, py = -ny, nx
        for k in range(gang):
            o = (k - (gang - 1) / 2.0) * 12
            self.d.line([(cx + px * o + nx * r, cy + py * o + ny * r),
                         (cx + px * o + nx * (r + 20), cy + py * o + ny * (r + 20))],
                        fill=col, width=5)

    def sym_ceiling(self, x, y, col, double=False, pendant=False):
        r = 24
        self.d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=6)
        if double:
            self.d.ellipse([x - r + 9, y - r + 9, x + r - 9, y + r - 9], outline=col, width=5)
        self.d.line([(x - r, y), (x + r, y)], fill=col, width=6)
        self.d.line([(x, y - r), (x, y + r)], fill=col, width=6)
        if pendant:
            for a in (45, 135, 225, 315):
                ax = x + math.cos(math.radians(a)) * (r + 15)
                ay = y + math.sin(math.radians(a)) * (r + 15)
                self.d.line([(x, y), (ax, ay)], fill=col, width=4)
                self.d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], outline=col, width=4)

    def sym_pipe(self, x, y, nx, ny, col, kind):
        r = 17
        cx, cy = x + nx * (r + 4), y + ny * (r + 4)
        self.d.line([(x, y), (cx, cy)], fill=col, width=7)
        if kind == 'sewer':
            self.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=7)
            k = r * 0.7
            self.d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=col, width=6)
            self.d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=col, width=6)
        else:
            self.d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], fill=col)

    def htag(self, x, y, txt, col):
        w = len(txt) * 15 + 20
        tx, ty = self.spot(x, y, w, 40)
        self.d.line([(x, y), (tx, ty)], fill=col + (170,), width=2)
        self.d.rectangle([tx - w / 2, ty - 20, tx + w / 2, ty + 20],
                         fill=(255, 255, 255, 245), outline=col, width=3)
        self.d.text((tx, ty), txt, fill=col, font=f_tag, anchor='mm')

    def callout(self, x, y, lines, col=(40, 40, 40)):
        w = max(len(t) for t in lines) * 15 + 26
        h = 14 + 30 * len(lines)
        tx, ty = self.spot(x, y, w, h)
        self.d.line([(x, y), (tx, ty)], fill=(90, 90, 90, 190), width=2)
        self.d.rectangle([tx - w / 2, ty - h / 2, tx + w / 2, ty + h / 2],
                         fill=(255, 255, 255, 248), outline=(90, 90, 90), width=3)
        for i, t in enumerate(lines):
            self.d.text((tx, ty - h / 2 + 17 + 30 * i), t, fill=col, font=f_note, anchor='mm')

    def legend(self, draw_fn, label, col):
        x, y = 108, self.ly
        draw_fn(x, y, col)
        self.d.text((190, y), label, fill=(40, 40, 40), font=f_leg, anchor='lm')
        self.ly += 62

    def note(self, lines):
        self.ly += 14
        for t in lines:
            self.d.text((70, self.ly), t, fill=(110, 110, 110), font=f_note, anchor='lm')
            self.ly += 32

    def check_openings(self, items):
        """items = [(wall_id, t, height_mm, label)]. Raises on any clash."""
        bad = []
        for wid, t, h, lbl in items:
            o = opening_conflict(wid, t, h)
            if o:
                bad.append('%s at H=%d on %s falls inside opening %s' % (lbl, h, wid, o))
        if bad:
            raise AssertionError('items inside openings: ' + '; '.join(bad))
        print('  opening check: %d items, all clear' % len(items))

    def save(self, name):
        tmp = os.path.join(HERE, '_' + name)
        self.im.save(tmp)
        shutil.copyfile(tmp, '_Drawings/sheets/' + name)
        print('wrote _Drawings/sheets/%s %s' % (name, self.im.size))
        self.im.resize((self.im.width // 2, self.im.height // 2), Image.LANCZOS).save(
            os.path.join(HERE, name.replace('.png', '_preview.png')))
