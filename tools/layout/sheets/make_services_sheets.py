# -*- coding: utf-8 -*-
"""Three services sheets, each symbol carrying the photo it was placed from.

The owner, 2026-09-07: "for manually reviewing your results, for each outlet or
switch provide the index of the image you based your positioning on. If you
investigated two images, mention both IDs."

That request forced an honest count. Of 13 socket positions, 8 have some
photographic basis and 5 have NONE - I chose a plausible fraction along a wall
and drew it. Those now say `НЕТ ФОТО` on the sheet instead of looking like the
others. The review table is written to
data/canonical/electrical_placement_review.csv for him to mark up.
"""
import csv, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_lib import Sheet, on_wall, beside_opening

G, B, R, MG, GY, OR = ((0, 150, 60), (0, 110, 220), (210, 30, 40),
                       (190, 60, 190), (110, 110, 110), (225, 130, 0))
NOPH = u'НЕТ ФОТО'

# id, wall, t, face, gang, H cm, source photo ids, what the photo shows
SOCK = [
 # ============ КУХНЯ-ГОСТИНАЯ ============
 # The north-wall row is the only placement in this room with two independent
 # photos agreeing: 930d (close to frontal, H=100 above the worktop) and a89d
 # (the same three boxes at mid height on the far wall).
 ('S1', 'G3', 0.16, +1, 2, 100, '930d + a89d', u'ряд из 3 розеток над столешницей, H=100'),
 ('S2', 'G3', 0.42, +1, 2, 100, '930d + a89d', u'то же, средняя в ряду'),
 # G7 - the wall to the middle room. TWO outlets, no switches, per the owner
 # 2026-09-07. I had left it empty; before that I had put a switch on it.
 ('S17', 'G7', 0.30, +1, 1, 30, u'владелец', u'ВЛАДЕЛЕЦ: на G7 две розетки, выключателей нет'),
 ('S18', 'G7', 0.68, +1, 1, 30, u'владелец', u'то же, вторая'),
 # the east party run - REDUCED from 4 to 2. The owner: "too many outlets on the
 # bigger wall neighbouring the other apartment."
 ('S4', 'R2', 0.55, +1, 1, 30, 'a89d + add8', u'низкая розетка на длинной стене (СЧЁТ уточняется)'),
 ('S5', 'G5', 0.45, +1, 1, 30, 'a89d + add8', u'то же, вторая (СЧЁТ уточняется)'),
 # MC, the window wall - NONE. Owner: "there are no outlets on the wall with the
 # window, not a trace of it." S16 removed.
 # ============ СРЕДНЯЯ КОМНАТА ============
 ('S6', 'G8', 0.30, -1, 1, 30, 'b6f0', u'2 низкие розетки; СТЕНА не подтверждена'),
 ('S7', 'G8', 0.72, -1, 1, 30, 'b6f0', u'то же'),
 ('S12', 'MB', 0.08, -1, 1, 30, NOPH, u'—'),
 # ============ КОМНАТА 9.36 ============
 ('S8', 'G4a', 0.34, -1, 1, 30, '9db4 + bc18', u'розетки на боковых стенах; СТЕНА не подтверждена'),
 ('S9', 'R6', 0.50, -1, 1, 30, '9db4', u'то же, вторая стена'),
 ('S13', 'MA', 0.42, -1, 1, 30, NOPH, u'—'),
]

# СИЛОВАЯ розетка - its own list and its own symbol
POWER = [('S3', 'G3', 0.70, +1, 100, u'930d + a89d + владелец',
          u'третья в ряду, у электроплиты — владелец: НЕ 220 В, вероятно 380 В')]

# id, wall, opening, jamb, face, gang, H, sources, what the photo shows
SWDEF = [
 ('W1', 'G4C', 'O1', 'hi', -1, 1, 90, 'a82a', u'коробки у дверей мокрых зон, со стороны прихожей'),
 ('W2', 'G4C', 'O7', 'lo', -1, 1, 90, 'a82a', u'то же'),
 ('W3', 'G2', 'O8', 'hi', +1, 2, 90, 'a89c + a82a', u'ПАРА коробок на простенке, H≈880'),
 ('W4', 'G6', 'O5', 'hi', +1, 1, 90, NOPH, u'—'),
 # !! NOT on G4d: G4C lands exactly on O6's near jamb, so there is no wall
 # there, and beyond the far jamb G4d ends 20 mm later. The switch goes on
 # G8 instead - immediately inside the room, past R4's column.
 ('W5', 'G8', None, 0.14, +1, 1, 90, NOPH, u'— (на G8: у G4d нет места у проёма)'),
 # НЕ на G7: владелец - на стене между средней комнатой и гостиной
 # нет ни выключателей, ни розеток. Выключатель гостиной - у проёма
 # O10, единственного входа в помещение.
 ('W6', 'R5', None, 0.30, +1, 2, 90, u'вывод — у проёма O10',
  u'— (выведено логикой: O10 — единственный вход)'),
]

LIGHT = [
 ('L1', 860, 150, u'вывод 1 — зона кухни', True, 'add8 + 930d', u'ДВА вывода в комнате 25 м²'),
 ('L2', 860, 620, u'вывод 2 — зона гостиной', True, 'add8', u'то же, второй кабель'),
 ('L3', 430, 200, u'прихожая', True, 'a82a + a89c + 9e9b', u'подвес в коридоре, все 3 квартиры'),
 ('L4', 495, 520, u'средняя комната', True, 'b6f0', u'кабель у окна'),
 ('L5', 150, 500, u'комната 9.36', True, 'bc18', u'кабель на потолке'),
 ('L6', 150, 150, u'туалет', False, NOPH, u'—'),
 ('L7', 150, 300, u'ванная', False, NOPH, u'—'),
]

REVIEW = []


def tagsrc(sh, px, py, iid, src, col):
    """the item id and the photo it came from, under the symbol"""
    txt = u'%s · %s' % (iid, src)
    w = len(txt) * 12 + 18
    x, y = sh.spot(px, py + 62, w, 34)
    sh.d.line([(px, py), (x, y)], fill=(150, 150, 150, 150), width=2)
    fill = (255, 246, 232, 250) if src == NOPH else (255, 255, 255, 246)
    edge = (215, 120, 0) if src == NOPH else (170, 170, 170)
    sh.d.rectangle([x - w / 2, y - 17, x + w / 2, y + 17], fill=fill, outline=edge, width=3)
    sh.d.text((x, y), txt, fill=(215, 120, 0) if src == NOPH else (90, 90, 90),
              font=sh.f_src, anchor='mm')


# ============================================================ Лист 1 РОЗЕТКИ
s = Sheet(u'Розетки и выключатели', 1)
s.f_src = s.d and __import__('sheet_lib').F(21)
s.legend(lambda x, y, c: s.sym_socket(x - 20, y, 1, 0, c, 1), u'Розетка стандартная', G)
s.legend(lambda x, y, c: s.sym_socket(x - 20, y, 1, 0, c, 2), u'Розетка двойная', G)
s.legend(lambda x, y, c: s.sym_power(x - 20, y, 1, 0, c), u'СИЛОВАЯ розетка (плита, 380 В?)', R)
s.legend(lambda x, y, c: s.sym_switch(x - 20, y, 1, 0, c, 1), u'Выключатель 1-клавишный', GY)
s.legend(lambda x, y, c: s.sym_switch(x - 20, y, 1, 0, c, 2), u'Выключатель 2-клавишный', GY)
s.note([u'H = высота от чистого пола, см.', u'',
        u'Под каждым символом: ЕГО НОМЕР и ID ФОТО,',
        u'по которому он поставлен. Оранжевая рамка',
        u'и «НЕТ ФОТО» — положение НЕ подтверждено',
        u'ничем, выбрано мной.',
        u'', u'⚠⚠ ПРИВЯЗКА К СТЕНАМ ПЕРЕСМАТРИВАЕТСЯ.',
        u'   Направление взгляда на фото инвертирует',
        u'   лево/право, и я применил это непоследовательно.',
        u'   Таблица для правки:',
        u'   data/canonical/photo_wall_mapping.csv', u'',
        u'⚠ Ни одно горизонтальное положение НЕ',
        u'   измерено в НАШЕЙ квартире. Все фото —',
        u'   соседние квартиры, две из трёх зеркальные.',
        u'', u'Таблица для правки:',
        u'data/canonical/electrical_placement_review.csv'])

SW = []
for iid, wid, oid, jamb, side, gang, h, src, shows in SWDEF:
    t = beside_opening(wid, oid, jamb) if oid else (
        jamb if isinstance(jamb, float) else 0.16)
    SW.append((iid, wid, t, side, gang, h, src, shows))

for iid, wid, t, side, gang, h, src, shows in SOCK:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_socket(px, py, nx, ny, G, gang)
    s.htag(px, py, u'H=%d' % h, G, nx, ny)
    tagsrc(s, px, py, iid, src, G)
    REVIEW.append({'item_id': iid, 'kind': 'socket', 'wall': wid, 'gang': gang,
                   'height_cm': h, 'source_photos': src, 'photo_shows': shows,
                   'position_basis': 'NONE - chosen by me' if src == NOPH
                   else 'photo of another flat, horizontal position indicative',
                   'owner_verdict': '', 'owner_correction': ''})

for iid, wid, t, side, h, src, shows in POWER:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_power(px, py, nx, ny, R)
    s.htag(px, py, u'H=%d' % h, R, nx, ny)
    tagsrc(s, px, py, iid, src, R)
    s.callout(px, py, [u'СИЛОВАЯ — под электроплиту', u'НЕ 220 В, уточнить 380 В'], R)
    REVIEW.append({'item_id': iid, 'kind': 'POWER socket (380 V?)', 'wall': wid,
                   'gang': '-', 'height_cm': h, 'source_photos': src,
                   'photo_shows': shows,
                   'position_basis': 'photo of another flat; VOLTAGE from the owner, to confirm',
                   'owner_verdict': '', 'owner_correction': ''})

for iid, wid, t, side, gang, h, src, shows in SW:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_switch(px, py, nx, ny, GY, gang)
    s.htag(px, py, u'H=%d' % h, GY, nx, ny)
    tagsrc(s, px, py, iid, src, GY)
    REVIEW.append({'item_id': iid, 'kind': 'switch', 'wall': wid, 'gang': gang,
                   'height_cm': h, 'source_photos': src, 'photo_shows': shows,
                   'position_basis': 'NONE - chosen by me' if src == NOPH
                   else 'photo of another flat, horizontal position indicative',
                   'owner_verdict': '', 'owner_correction': ''})

SIDES = dict(((w, t), sd) for _i, w, t, sd, _g, _h, _sr, _sh in SOCK)
SIDES.update(dict(((w, t), sd) for _i, w, t, sd, _h, _sr, _sh in POWER))
SIDES.update(dict(((w, t), sd) for _i, w, t, sd, _g, _h, _sr, _sh in SW))
s.check_openings([(w, t, h, u'розетка ' + i) for i, w, t, _s, _g, h, _sr, _sh in SOCK]
                 + [(w, t, h, u'силовая ' + i) for i, w, t, _s, h, _sr, _sh in POWER]
                 + [(w, t, h, u'выкл. ' + i) for i, w, t, _s, _g, h, _sr, _sh in SW],
                 SIDES)
s.save('sheet_01_sockets.png')

# ========================================================== Лист 2 ОСВЕЩЕНИЕ
s2 = Sheet(u'Освещение', 2)
s2.f_src = __import__('sheet_lib').F(21)
s2.legend(lambda x, y, c: s2.sym_ceiling(x, y, c, False, True), u'Вывод под светильник', G)
s2.legend(lambda x, y, c: s2.sym_ceiling(x, y, c), u'Светильник встраиваемый (проект)', G)
s2.legend(lambda x, y, c: s2.sym_switch(x - 20, y, 1, 0, c, 1), u'Выключатель', GY)
s2.note([u'Показаны только СУЩЕСТВУЮЩИЕ выводы',
         u'застройщика — по одному на комнату,', u'кроме кухни-гостиной.', u'',
         u'✅ В кухне-гостиной выводов ДВА — застройщик',
         u'   разводит помещение как ДВЕ ЗОНЫ.', u'',
         u'⚠ Выводы в туалете и ванной НЕ видны ни на',
         u'   одном фото — показаны предположительно.'])
for iid, bx, by, nt, pend, src, shows in LIGHT:
    px, py = s2.P((bx, by))
    s2.sym_ceiling(px, py, G, False, pend)
    s2.callout(px, py, [nt], (40, 40, 40) if pend else (180, 100, 0))
    tagsrc(s2, px, py, iid, src, G)
    REVIEW.append({'item_id': iid, 'kind': 'ceiling light point', 'wall': '-',
                   'gang': '-', 'height_cm': 'ceiling', 'source_photos': src,
                   'photo_shows': shows,
                   'position_basis': 'NONE - chosen by me' if src == NOPH
                   else 'photo of another flat, position within the room indicative',
                   'owner_verdict': '', 'owner_correction': ''})
px, py = s2.P((860, 330))
s2.sym_detector(px, py, R)
s2.callout(px, py, [u'ПОЖАРНЫЙ ИЗВЕЩАТЕЛЬ на потолке',
                    u'переносится на лист «Безопасность»'], R)
tagsrc(s2, px, py, 'F1', 'a89d + add8', R)
REVIEW.append({'item_id': 'F1', 'kind': 'fire detector, ceiling', 'wall': '-',
               'gang': '-', 'height_cm': 'ceiling', 'source_photos': 'a89d + add8',
               'photo_shows': u'белый цилиндр на потолке, отличается от патрона',
               'position_basis': 'photo of another flat; position within the room indicative',
               'owner_verdict': '', 'owner_correction': ''})
s2.legend(lambda x, y, c: s2.sym_detector(x, y, c), u'Пожарный извещатель', R)

for iid, wid, t, side, gang, h, src, shows in SW:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s2.P((x, y))
    s2.sym_switch(px, py, nx, ny, GY, gang)
s2.save('sheet_02_lighting.png')

# ============================================ Лист 3 ВОДОСНАБЖЕНИЕ И КАНАЛИЗАЦИЯ
s3 = Sheet(u'Водоснабжение, канализация, вентиляция', 3)
s3.f_src = __import__('sheet_lib').F(21)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод холодной воды', B)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод горячей воды', R)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'sewer'), u'Вывод канализации DN50', MG)
s3.legend(lambda x, y, c: s3.d.rectangle([x - 22, y - 16, x + 22, y + 16], outline=c, width=6),
          u'Стояк / сантехблок', B)
s3.legend(lambda x, y, c: s3.d.rectangle([x - 22, y - 16, x + 22, y + 16], outline=c, width=6),
          u'Вентиляционный короб', OR)
s3.legend(lambda x, y, c: [s3.d.line([(x - 26, y - 5), (x + 26, y - 5)], fill=R, width=8),
                           s3.d.line([(x - 26, y + 6), (x + 26, y + 6)], fill=B, width=8)],
          u'ГВС / ХВС под полом (трасса владельца)', B)
s3.note([u'✅ Сплошной контур — положение определено',
         u'   по НАШЕМУ плану.',
         u'✅ Трасса ГВС/ХВС — НАНЕСЕНА ВЛАДЕЛЬЦЕМ,',
         u'   больше не предположение. Две линии —',
         u'   две трубы, видны на 930d.', u'',
         u'✕ ОТОПЛЕНИЕ не показано — трасса нигде не',
         u'   зафиксирована.'])
for bid, (x0, y0, x1, y1), col in (('V1', (67, 70, 139, 111), OR), ('V2', (636, 92, 677, 162), OR),
                                   ('P1', (52, 110, 87, 192), B), ('P2', (636, 71, 677, 91), B)):
    p0, p1 = s3.P((x0, y0)), s3.P((x1, y1))
    s3.d.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=col + (48,), outline=col, width=6)
# ВОДОСНАБЖЕНИЕ under the floor, drawn by the OWNER on sheet 3 and
# replacing my dashed guess. His line: out of P1, straight EAST across the
# прихожая at a constant level, then ONE turn north up to the kitchen
# take-offs. My guess dog-legged south first and then back up - longer, and
# wrong. Two parallel lines because 930d shows TWO pipes rising from the floor,
# red hot and blue cold.
ROUTE = [(90, 172), (648, 172), (690, 96)]
for off, col, lbl in ((-3.0, R, u'ГВС'), (3.0, B, u'ХВС')):
    for i in range(len(ROUTE) - 1):
        (x0, y0), (x1, y1) = ROUTE[i], ROUTE[i + 1]
        dx, dy = x1 - x0, y1 - y0
        L = (dx * dx + dy * dy) ** 0.5
        px_, py_ = -dy / L * off, dx / L * off
        a = s3.P((x0 + px_, y0 + py_))
        b = s3.P((x1 + px_, y1 + py_))
        s3.d.line([a, b], fill=col + (240,), width=9)
    m = s3.P(((ROUTE[0][0] + ROUTE[1][0]) / 2.0, ROUTE[0][1] + off * 4))
    s3.d.text(m, lbl, fill=col, font=s3.f_src, anchor='mm')
s3.callout(*(list(s3.P((380, 172))) + [[u'ГВС + ХВС под полом — трасса ВЛАДЕЛЬЦА',
                                        u'трафареты «ВОДОСНАБЖЕНИЕ» на стяжке'], B]))

PIPES = [('P-H', 'G3', 0.055, +1, R, 'water', 61, u'горячая, из пола', '930d'),
         ('P-C', 'G3', 0.075, +1, B, 'water', 61, u'холодная, из пола', '930d'),
         ('P-S', 'G3', 0.115, +1, MG, 'sewer', 6, u'канализация DN50', '930d')]
for iid, wid, t, side, col, kind, h, nt, src in PIPES:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s3.P((x, y))
    s3.sym_pipe(px, py, nx, ny, col, kind)
    s3.htag(px, py, u'H=%d' % h, col, nx, ny)
    tagsrc(s3, px, py, iid, src, col)
    REVIEW.append({'item_id': iid, 'kind': 'plumbing outlet', 'wall': wid, 'gang': '-',
                   'height_cm': h, 'source_photos': src, 'photo_shows': nt,
                   'position_basis': 'photo of another flat, horizontal position indicative',
                   'owner_verdict': '', 'owner_correction': ''})
for iid, bx, by, nt, src in (('V-1', 103, 92, u'решётка вытяжки H=218', '930d + 9e9b'),
                             ('V-2', 656, 128, u'решётка вытяжки H=218', '9e9b')):
    px, py = s3.P((bx, by))
    s3.d.ellipse([px - 16, py - 16, px + 16, py + 16], outline=OR, width=6)
    s3.callout(px, py, [nt], OR)
    tagsrc(s3, px, py, iid, src, OR)
s3.save('sheet_03_plumbing.png')

FN = ['item_id', 'kind', 'wall', 'gang', 'height_cm', 'source_photos', 'photo_shows',
      'position_basis', 'owner_verdict', 'owner_correction']
with io.open('data/canonical/electrical_placement_review.csv', 'w',
             encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FN)
    w.writeheader(); w.writerows(REVIEW)
noph = sum(1 for r in REVIEW if r['source_photos'] == NOPH)
print('review table: %d items, %d with NO photo basis' % (len(REVIEW), noph))
