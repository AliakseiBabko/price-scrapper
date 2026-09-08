# -*- coding: utf-8 -*-
"""Sheet 00 - the wall segment key, plus segment labels for the services sheets.

The owner, 2026-09-08: "for this sheet, I need sockets with wall segments,
because I don't remember them ... actually for all of the sockets, lighting,
plumbing. I want to see all segments names. It will help me to provide a better
description."

That is the missing half of Existing_Services_Capture_Protocol.md. The protocol
asks him to dictate "кухня-гостиная 24.73, G3: 2 sockets, low" - and nothing in
the album told him which wall is G3. A capture format nobody can address is not
a capture format.

Two outputs, because they answer two different needs:

  * `label_segments(sheet)` - an overlay every services sheet calls, so each
    sheet carries its own wall names. Labels go through spot(), so they route
    around the device symbols rather than over them.
  * sheet 00 - a CLEAN key with no device symbols at all. On a busy sockets
    sheet the codes are readable but crowded; when the job is simply "what is
    that wall called", an uncluttered plan wins.

It also prints the room -> walls table, which is what the dictation actually
needs, and writes it beside the sheet as text.

Run:
    .venv/Scripts/python.exe tools/layout/sheets/make_segment_key_sheet.py
"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_lib import MMPX, RUNS, Sheet  # noqa: E402

# One colour per construction class, because the class is half of what the code
# means: R* is the monolithic frame and cannot be touched, G* is block infill and
# can, M* is the external envelope.
CLASS_COL = {
    'concrete': (210, 30, 40),
    'aerated_block': (0, 150, 60),
    'external': (120, 90, 190),
    'loggia_enclosure': (225, 130, 0),
}
CLASS_RU = {
    'concrete': u'R* - каркас (не трогать)',
    'aerated_block': u'G* - блочная перегородка',
    'external': u'M* - наружная стена 300+70',
    'loggia_enclosure': u'M* - ограждение лоджии',
}

# Codes that appear in device_counts_per_wall.csv but have NO geometry in
# wall_runs.csv. They are real places to put a device and must be nameable, so
# they are listed rather than quietly dropped.
NON_GEOMETRIC = [
    (u'ПОТОЛОК (выводы света)', u'потолок - выводы света; есть в каждом помещении'),
    (u'V2', u'вентблок, лицевая сторона - кухня-гостиная и прихожая'),
    (u'P2', u'зона стояков P - кухня-гостиная и прихожая'),
]

CLASSES = {}
for _r in csv.DictReader(io.open('data/canonical/wall_runs.csv', encoding='utf-8')):
    CLASSES[_r['wall_id']] = _r['class']


def rooms_by_wall():
    """wall code -> the rooms it faces, from the file the owner will dictate into."""
    out = {}
    rows = list(csv.DictReader(
        io.open('data/canonical/device_counts_per_wall.csv', encoding='utf-8')))
    for r in rows:
        out.setdefault(r['wall_segment'], set()).add(r['room'])
    return out, rows


def _centroid():
    """Mid-point of all wall runs, in basic px. Used to decide which SIDE of a
    wall its tag goes on: away from the centroid, so tags radiate outward
    instead of piling into the middle of the plan or off the sheet edge."""
    pts = [((ax + bx) / 2.0, (ay + by) / 2.0) for ax, ay, bx, by, _ in RUNS.values()]
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def _footprint(wid):
    """The wall's actual four corners, in basic px.

    wall_runs.csv stores the CENTRELINE plus a thickness - on_wall() offsets by
    th/2 from it, which is what fixes the convention. So the footprint is the
    centreline swept perpendicular by half the thickness.
    """
    ax, ay, bx, by, th = RUNS[wid]
    dx, dy = bx - ax, by - ay
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    half = (th / MMPX) / 2.0
    corners = [
        (ax + px * half, ay + py * half),
        (bx + px * half, by + py * half),
        (bx - px * half, by - py * half),
        (ax - px * half, ay - py * half),
    ]
    return corners, (ux, uy), (px, py), half


def outline_segments(sh, only=None, fill_alpha=34):
    """Draw each wall segment's real boundary, not just a label in its middle.

    The owner, 2026-09-08: "you're putting label in the middle, and I need to
    rely on the underlying image to see the boundaries. If you'd add clear
    boundaries, like a border in specific color, it would help me a lot."

    Three marks per segment, and the third is the one that does the work:
      * a translucent band over the wall's footprint - shows WHICH wall;
      * an outline around it - shows its extent;
      * PERPENDICULAR END TICKS overshooting the thickness at both ends - shows
        where one segment STOPS and the next begins. Without these, collinear
        neighbours of the same class (R1a | G2 | R3 | G3 all run along the top
        wall) merge into one continuous band, which is exactly the ambiguity
        being complained about.
    """
    n = 0
    for wid in sorted(RUNS):
        if only is not None and wid not in only:
            continue
        corners, (ux, uy), (px, py), half = _footprint(wid)
        col = CLASS_COL.get(CLASSES.get(wid, ''), (90, 90, 90))
        poly = [sh.P(c) for c in corners]
        sh.d.polygon(poly, fill=col + (fill_alpha,))
        sh.d.line(poly + [poly[0]], fill=col + (215,), width=4)

        ax, ay, bx, by, _ = RUNS[wid]
        over = half + 11.0
        for (ex, ey) in ((ax, ay), (bx, by)):
            p0 = sh.P((ex + px * over, ey + py * over))
            p1 = sh.P((ex - px * over, ey - py * over))
            sh.d.line([p0, p1], fill=col, width=7)
        n += 1
    return n


def label_segments(sh, only=None, tiny=False):
    """Tag every wall run with its code. Call this from any sheet.

    `only` limits it to a set of wall ids - used by the services sheets so a
    room's own walls are labelled and the rest stay quiet.

    Two placement rules, both from defects in the first render: the tag goes on
    the side AWAY from the plan's centroid, because always pushing vertical walls
    right sent the three east-wall tags (R2, G5, R7) off the drawing into the
    margin; and the tag is clamped inside the image, because spot() will happily
    walk one out of frame.
    """
    from sheet_lib import F

    f_seg = F(50, True) if not tiny else F(40, True)
    cx0, cy0 = _centroid()
    W, H = sh.im.size

    # Reserve the whole title/legend/notes column and the footer strip. Sheet 00
    # did this in its own main() and the services sheets did not, so R1b landed
    # on a legend row of the plumbing sheet. Doing it here fixes it for every
    # caller, present and future - sh.ly is the running bottom of that column.
    sh.placed.append((0, 0, 1000, max(sh.ly + 30, 320)))
    sh.placed.append((0, H - 190, W, H))

    n = 0
    for wid, (ax, ay, bx, by, th) in sorted(RUNS.items()):
        if only is not None and wid not in only:
            continue
        midx, midy = (ax + bx) / 2.0, (ay + by) / 2.0
        mx, my = sh.P((midx, midy))
        horizontal = abs(bx - ax) >= abs(by - ay)
        if horizontal:
            nx, ny = 0, (-1 if midy <= cy0 else 1)
        else:
            nx, ny = (-1 if midx <= cx0 else 1), 0
        col = CLASS_COL.get(CLASSES.get(wid, ''), (90, 90, 90))
        # sized for the bigger type the owner asked for on 2026-09-08
        pad = 30 if not tiny else 24
        w = len(wid) * (26 if not tiny else 21) + pad
        h = 66 if not tiny else 54
        # Clamp the SEED, then let spot() search from there. Clamping the result
        # instead would silently undo spot()'s collision avoidance - it did, and
        # put G5 on top of a socket's photo-id label on sheet 01.
        sx = min(max(mx + nx * 64, w / 2 + 34), W - w / 2 - 34)
        sy = min(max(my + ny * 64, h / 2 + 34), H - h / 2 - 34)
        tx, ty = sh.spot(sx, sy, w, h)
        sh.d.line([(mx, my), (tx, ty)], fill=col, width=4)
        sh.d.rectangle([tx - w / 2, ty - h / 2, tx + w / 2, ty + h / 2],
                       fill=(255, 255, 255, 250), outline=col, width=4)
        sh.d.text((tx, ty), wid, fill=col, font=f_seg, anchor='mm')
        n += 1
    return n


def main():
    by_wall, rows = rooms_by_wall()

    sh = Sheet(u'ЛИСТ 00 · КЛЮЧ СЕГМЕНТОВ СТЕН', 0)

    # ORDER MATTERS, and both orderings here were wrong once:
    #   1. the segment bands go down first, so the text sits ON them rather than
    #      under a translucent wash;
    #   2. then the legend and notes;
    #   3. then their footprint is reserved, so no tag lands on the text - which
    #      is what happened to R1b before the reserve existed;
    #   4. then the tags, last, so spot() routes them around everything above.
    print('  outlined %d segments' % outline_segments(sh))

    for cls in ('concrete', 'aerated_block', 'external', 'loggia_enclosure'):
        col = CLASS_COL[cls]

        def swatch(x, y, c, _col=col):
            sh.d.rectangle([x - 26, y - 13, x + 26, y + 13], fill=(255, 255, 255),
                           outline=_col, width=4)
        sh.legend(swatch, CLASS_RU[cls], col)

    sh.note([
        u'%d сегментов с геометрией.' % len(RUNS),
        u'Границы показаны полосой и засечками',
        u'на КОНЦАХ сегмента.',
        u'',
        u'БЕЗ ГЕОМЕТРИИ, но диктовать можно:',
        u'   ПОТОЛОК — выводы света,',
        u'      в каждом помещении',
        u'   V2 — вентблок, лицевая сторона',
        u'   P2 — зона стояков',
        u'',
        u'Диктовать так:',
        u'   «<помещение>, <код>: 2 розетки, low»',
        u'',
        u'Протокол:',
        u'   00_Master/',
        u'   Existing_Services_Capture_Protocol.md',
    ])
    # Block the whole title/legend/notes column so no tag can land on the text.
    sh.placed.append((0, 0, 1000, sh.ly + 30))
    # And the footer strip.
    sh.placed.append((0, sh.im.size[1] - 190, sh.im.size[0], sh.im.size[1]))

    n = label_segments(sh)
    print('  labelled %d segments' % n)
    sh.save('sheet_00_segment_key.png')

    # ---- the room -> walls table, which is what the dictation needs ----------
    lines = [
        u'# Сегменты стен по помещениям',
        u'',
        u'Сгенерировано tools/layout/sheets/make_segment_key_sheet.py из',
        u'data/canonical/device_counts_per_wall.csv. План: _Drawings/sheets/sheet_00_segment_key.png',
        u'',
        u'Диктовать так: `<помещение>, <код>: N розеток, low`',
        u'Строку помещения копировать ОТСЮДА дословно - валидатор сверяет её посимвольно.',
        u'',
    ]
    for room in sorted({r['room'] for r in rows}):
        walls = sorted({r['wall_segment'] for r in rows if r['room'] == room})
        geo = [w for w in walls if w in RUNS]
        other = [w for w in walls if w not in RUNS]
        lines.append(u'## %s' % room)
        lines.append(u'')
        lines.append(u'%s' % u', '.join(u'`%s`' % w for w in geo))
        if other:
            lines.append(u'')
            lines.append(u'без геометрии: %s' % u', '.join(u'`%s`' % w for w in other))
        lines.append(u'')

    out = '_Drawings/sheets/sheet_00_segment_key.md'
    io.open(out, 'w', encoding='utf-8').write(u'\n'.join(lines))
    print('wrote %s' % out)

    print()
    for room in sorted({r['room'] for r in rows}):
        walls = sorted({r['wall_segment'] for r in rows if r['room'] == room})
        print(u'  %-24s %s' % (room, u', '.join(walls)))


if __name__ == '__main__':
    main()
