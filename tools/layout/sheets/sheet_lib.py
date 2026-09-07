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
JAMB_CLEAR_MM = 100.0  # a symbol this close to a jamb is not buildable -
                       # the MB socket read 'clear' at 59 mm from O2
STANDOFF_MM = 12.0   # the symbol's flat side sits this far off the modelled
                     # face. It must be SMALL: at 95 mm the symbols read as
                     # floating off the wall, which the owner flagged. The
                     # symbol's own body extends outward from here, so the
                     # base touching the face is what "attached" looks like.
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


def _seg_box_hit(p0, p1, box, clear_px):
    """True if segment p0-p1 comes within clear_px of the rectangle `box`.

    Sampled rather than solved: the segments here are tens of pixels long and a
    2 px step over an inflated box is both exact enough and impossible to get
    subtly wrong, which matters more. Inflating the box means a pipe that grazes
    the corner of a shaft fails too - touching concrete is not clearance.
    """
    x0b, y0b, x1b, y1b = min(box[0], box[2]), min(box[1], box[3]),                          max(box[0], box[2]), max(box[1], box[3])
    x0b -= clear_px; y0b -= clear_px; x1b += clear_px; y1b += clear_px
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = max(1e-9, (dx * dx + dy * dy) ** 0.5)
    n = int(L / 2.0) + 2
    for i in range(n + 1):
        t = float(i) / n
        x, y = p0[0] + dx * t, p0[1] + dy * t
        if x0b <= x <= x1b and y0b <= y <= y1b:
            return True
    return False


def route_block_conflicts(route, blocks, clear_mm=60.0, connects=()):
    """Every routed segment that crosses (or grazes) a shaft / plumbing block.

    Added 2026-09-07 after the owner circled the ГВС/ХВС pair running
    diagonally through V2, a concrete ventilation shaft. Same lesson as the wall
    junction check: the drawing had no way to object, so it didn't.
    """
    out = []
    c = clear_mm / MMPX
    for i in range(len(route) - 1):
        for bid, box in sorted(blocks.items()):
            if bid in connects:
                continue  # the route TAKES OFF from this block; touching it is the point
            if _seg_box_hit(route[i], route[i + 1], box, c):
                out.append(u'segment %d %s→%s hits %s %s'
                           % (i, route[i], route[i + 1], bid, box))
    return out


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
        t = (v - a) / (b - a)
        if not (0.0 <= t <= 1.0):
            raise AssertionError(
                'beside_opening(%s, %s, %s) gives t=%.3f - OFF THE END OF THE '
                'WALL. There is not %.0f mm of wall beyond that jamb; use the '
                'other one.' % (wid, oid, jamb, t, clear_mm))
        return t
    raise KeyError('%s has no opening %s' % (wid, oid))


JUNCTION_CLEAR_MM = 120.0   # an item this close to where another wall lands
                            # reads as being inside the corner. The socket on
                            # G4a at t=0.55 sat 40 mm from G4d - the owner saw
                            # it as "inside the wall between the bathroom and
                            # the small bedroom". 120 rather than 200 because a
                            # switch beside a door is INHERENTLY near a corner:
                            # 200 flagged three legitimate placements. 120 is
                            # about the minimum for an 80 mm faceplate to sit
                            # flat with a margin.


def junction_conflict(wid, t, side=None):
    """the wall whose landing this point sits on top of, or None.

    Uses proper point-to-SEGMENT distance, and tests the point where the symbol
    is actually drawn (the face, not the centreline). The first version tested
    the centreline and required the point to lie within the other wall's span -
    which skipped exactly the case that matters: G4d BUTTS on G4a, so it starts
    at x=51 while G4a's centreline is x=38, and the test never looked at it.
    That is why it passed the socket the owner could plainly see was in the wall.
    """
    if side is None:
        ax, ay, bx, by, th = RUNS[wid]
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
    else:
        px, py, _nx, _ny = on_wall(wid, t, side)
    for o, (ox, oy, obx, oby, oth) in RUNS.items():
        if o == wid:
            continue
        vx, vy = obx - ox, oby - oy
        L2 = vx * vx + vy * vy
        u = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ox) * vx + (py - oy) * vy) / L2))
        qx, qy = ox + vx * u, oy + vy * u
        d = (((px - qx) ** 2 + (py - qy) ** 2) ** 0.5) * MMPX - oth / 2.0
        if d < JUNCTION_CLEAR_MM:
            return '%s (%.0f mm from where %s lands)' % (o, max(d, 0.0), o)
    return None


def opening_conflict(wid, t, height_mm):
    """the opening this point clashes with, or None.

    Two ways to clash, and the second one cost a round of corrections:

    - ABOVE the sill, the opening itself is in the way. A switch at H=90 in a
      door opening (sill 0) is impossible.
    - BELOW a WINDOW sill the space is not free either, because every window
      in this flat has a RADIATOR under it - confirmed in every photograph.
      So a socket at H=30 under a 266 sill is blocked too, even though the
      generic rule would allow it. The owner caught exactly this on MC.
    """
    a, b = _axis(wid)
    v = a + (b - a) * t
    for o, lo, hi, sill in SPANS.get(wid, []):
        if lo <= v <= hi:
            if height_mm > sill:
                return o                      # in the opening itself
            if sill > 0:
                return o + ' (radiator below the sill)'
        else:
            d = min(abs(v - lo), abs(v - hi)) * MMPX
            if d < JAMB_CLEAR_MM:
                return '%s (only %.0f mm from its jamb)' % (o, d)
    return None


def on_wall(wid, t, side):
    """point on a wall face + the outward normal. t is 0..1 along the run,
    side is +1 / -1 for which face."""
    ax, ay, bx, by, th = RUNS[wid]
    x, y = ax + (bx - ax) * t, ay + (by - ay) * t
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = -uy * side, ux * side
    off = (th / 2.0 + STANDOFF_MM) / MMPX
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

    def reserve(self, cx, cy, r=30):
        """Claim a symbol’s own footprint so spot() routes labels AROUND it.

        Until 2026-09-07 only labels registered themselves in self.placed, so a
        label could be placed straight over a symbol and repeatedly was — the
        owner flagged it once as “you overlay the icon itself”, and again when a
        six-line callout landed on the three kitchen take-offs. spot() was
        working correctly; it simply had not been told the symbols existed.
        Every sym_* now calls this.
        """
        self.placed.append((cx - r, cy - r, cx + r, cy + r))

    # ---------------------------------------------------------------- symbols
    def sym_socket(self, x, y, nx, ny, col, gang=1, ip=False):
        self.reserve(x + nx * 21, y + ny * 21, 34)
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

    def sym_power(self, x, y, nx, ny, col):
        self.reserve(x + nx * 21, y + ny * 21, 34)
        """силовая розетка - a socket symbol with THREE bars, for a 380 V /
        high-current line. The reference album distinguishes it, and it must be
        distinguished here: a hob line is not a 220 V socket and cannot be
        substituted for one."""
        r = 23
        cx, cy = x + nx * r, y + ny * r
        a = __import__('math').degrees(__import__('math').atan2(ny, nx))
        self.d.arc([cx - r, cy - r, cx + r, cy + r], a - 90, a + 90, fill=col, width=7)
        px, py = -ny, nx
        self.d.line([(cx - px * r, cy - py * r), (cx + px * r, cy + py * r)],
                    fill=col, width=7)
        self.d.line([(x, y), (cx, cy)], fill=col, width=7)
        for k in (-1, 0, 1):
            o = k * 12
            self.d.line([(cx + px * o, cy + py * o),
                         (cx + px * o + nx * 17, cy + py * o + ny * 17)], fill=col, width=6)

    def sym_detector(self, x, y, col):
        self.reserve(x, y, 30)
        """пожарный извещатель - a circle with a dot, distinct from a luminaire"""
        r = 21
        self.d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=7)
        self.d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col)

    def sym_switch(self, x, y, nx, ny, col, gang=1):
        self.reserve(x + nx * 21, y + ny * 21, 32)
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
        self.reserve(x, y, 34)
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
        self.reserve(x + nx * 21, y + ny * 21, 30)
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

    def sym_valve(self, x, y, col):
        """a shut-off valve - the standard bow-tie, on a riser or a tail."""
        self.reserve(x, y, 24)
        k = 15
        self.d.polygon([(x - k, y - k), (x, y), (x - k, y + k)], outline=col, width=5)
        self.d.polygon([(x + k, y - k), (x, y), (x + k, y + k)], outline=col, width=5)
        self.d.line([(x, y - k - 6), (x, y + k + 6)], fill=col, width=4)

    def sym_riser(self, x, y, col, dn=False):
        """a riser passing floor to ceiling - a circle with a vertical bar."""
        r = 19 if dn else 15
        self.reserve(x, y, r + 10)
        self.d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=7)
        self.d.line([(x, y - r - 9), (x, y + r + 9)], fill=col, width=5)

    def polyline_rounded(self, pts, col, width=9, offset=0.0, r_mm=260.0):
        """a polyline with FILLETED corners, offset sideways by `offset` basic px.

        Pipework bends with a radius; a sharp right angle is a drawing
        convention, not a pipe. And the offset lets a pair of pipes run
        parallel without the two polylines diverging at the corners.
        """
        r = r_mm / MMPX
        out = []
        for i, p in enumerate(pts):
            if i == 0 or i == len(pts) - 1:
                out.append([p]); continue
            a, b, c = pts[i - 1], p, pts[i + 1]
            v1 = (a[0] - b[0], a[1] - b[1])
            v2 = (c[0] - b[0], c[1] - b[1])
            l1 = max(1e-9, (v1[0] ** 2 + v1[1] ** 2) ** 0.5)
            l2 = max(1e-9, (v2[0] ** 2 + v2[1] ** 2) ** 0.5)
            k = min(r, l1 * 0.45, l2 * 0.45)
            p1 = (b[0] + v1[0] / l1 * k, b[1] + v1[1] / l1 * k)
            p2 = (b[0] + v2[0] / l2 * k, b[1] + v2[1] / l2 * k)
            arc = []
            for t in [j / 8.0 for j in range(9)]:
                u = 1 - t
                arc.append((u * u * p1[0] + 2 * u * t * b[0] + t * t * p2[0],
                            u * u * p1[1] + 2 * u * t * b[1] + t * t * p2[1]))
            out.append(arc)
        flat = [q for grp in out for q in grp]
        # offset each vertex along the average of its adjacent segment normals,
        # so the two parallel runs stay parallel round the bends instead of
        # diverging - and collect the whole thing into ONE polyline. Drawing the
        # segments one at a time left a visible notch at every joint; PIL's
        # joint='curve' fills them.
        pts = []
        for i, p in enumerate(flat):
            nx_ = ny_ = 0.0
            for j, k in ((i - 1, i), (i, i + 1)):
                if j < 0 or k >= len(flat):
                    continue
                dx, dy = flat[k][0] - flat[j][0], flat[k][1] - flat[j][1]
                L = max(1e-9, (dx * dx + dy * dy) ** 0.5)
                nx_ += -dy / L; ny_ += dx / L
            L = max(1e-9, (nx_ ** 2 + ny_ ** 2) ** 0.5)
            pts.append(self.P((p[0] + nx_ / L * offset, p[1] + ny_ / L * offset)))
        self.d.line(pts, fill=col + (240,), width=width, joint='curve')
        # and claim the run, so a label cannot be dropped on top of a pipe -
        # same reason the sym_* methods reserve. Sampled coarsely: a corridor
        # roughly a label’s height wide is what we actually want to keep clear.
        for i in range(0, len(pts), 3):
            self.reserve(pts[i][0], pts[i][1], 22)

    def htag(self, x, y, txt, col, nx=0, ny=0, push=1.0):
        w = len(txt) * 15 + 20
        # start the search PAST the symbol body, not on top of it. `push` moves
        # the START of the search further out, for a row of symbols close
        # together whose tags would otherwise all compete for the same slot.
        tx, ty = self.spot(x + nx * 70 * push, y + ny * 70 * push - 46, w, 40)
        self.d.line([(x, y), (tx, ty)], fill=col + (170,), width=2)
        self.d.rectangle([tx - w / 2, ty - 20, tx + w / 2, ty + 20],
                         fill=(255, 255, 255, 245), outline=col, width=3)
        self.d.text((tx, ty), txt, fill=col, font=f_tag, anchor='mm')

    def callout(self, x, y, lines, col=(40, 40, 40), seek=(0, 0)):
        w = max(len(t) for t in lines) * 15 + 26
        h = 14 + 30 * len(lines)
        # the LEADER stays on (x, y) - the thing being annotated - while `seek`
        # moves where the box hunts for space. Without it spot() spirals out
        # from the anchor and can only land on the neighbours of the very thing
        # the note is about, which is how the sewer note ended up covering the
        # two shafts it describes.
        tx, ty = self.spot(x + seek[0], y + seek[1], w, h)
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

    def check_openings(self, items, sides=None):
        """items = [(wall_id, t, height_mm, label)]. Raises on any clash."""
        sides = sides or {}
        bad = []
        for wid, t, h, lbl in items:
            o = opening_conflict(wid, t, h)
            if o:
                bad.append('%s at H=%d on %s falls inside opening %s' % (lbl, h, wid, o))
            j = junction_conflict(wid, t, sides.get((wid, t)))
            if j:
                bad.append('%s on %s sits at a junction: %s' % (lbl, wid, j))
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
