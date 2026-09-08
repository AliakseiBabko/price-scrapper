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
from sheet_lib import RUNS, Sheet  # noqa: E402

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
    'concrete': u'R* - монолитный каркас (не трогать)',
    'aerated_block': u'G* - блочная перегородка',
    'external': u'M* - наружная стена, 300 + 70 утеплителя',
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
    from sheet_lib import f_tag

    cx0, cy0 = _centroid()
    W, H = sh.im.size
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
        w, h = (58, 34) if tiny else (74, 42)
        # Clamp the SEED, then let spot() search from there. Clamping the result
        # instead would silently undo spot()'s collision avoidance - it did, and
        # put G5 on top of a socket's photo-id label on sheet 01.
        sx = min(max(mx + nx * 52, w / 2 + 34), W - w / 2 - 34)
        sy = min(max(my + ny * 52, h / 2 + 34), H - h / 2 - 34)
        tx, ty = sh.spot(sx, sy, w, h)
        sh.d.line([(mx, my), (tx, ty)], fill=col, width=3)
        sh.d.rectangle([tx - w / 2, ty - h / 2, tx + w / 2, ty + h / 2],
                       fill=(255, 255, 255), outline=col, width=3)
        sh.d.text((tx, ty), wid, fill=col, font=f_tag, anchor='mm')
        n += 1
    return n


def main():
    by_wall, rows = rooms_by_wall()

    sh = Sheet(u'ЛИСТ 00 · КЛЮЧ СЕГМЕНТОВ СТЕН', 0)

    # The legend and notes are drawn FIRST and their footprint reserved, because
    # in the first render the R1b tag landed squarely on top of the note text.
    # spot() was working; it had simply never been told the text was there.
    for cls in ('concrete', 'aerated_block', 'external', 'loggia_enclosure'):
        col = CLASS_COL[cls]

        def swatch(x, y, c, _col=col):
            sh.d.rectangle([x - 26, y - 13, x + 26, y + 13], fill=(255, 255, 255),
                           outline=_col, width=4)
        sh.legend(swatch, CLASS_RU[cls], col)

    sh.note([
        u"%d сегментов с геометрией. Код = имя стены в data/canonical/wall_runs.csv." % len(RUNS),
        u'',
        u'БЕЗ ГЕОМЕТРИИ, но диктовать в них можно:',
    ] + [u'   %s - %s' % (c, d) for c, d in NON_GEOMETRIC] + [
        u'',
        u'Как диктовать: «<помещение>, <код>: N розеток, low».',
        u'Протокол: 00_Master/Existing_Services_Capture_Protocol.md',
        u'Проверка: tools/canonical/validate_services_observed.py',
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
