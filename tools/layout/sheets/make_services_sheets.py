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
from sheet_lib import Sheet, on_wall, beside_opening, route_block_conflicts

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
# ВОДОСНАБЖЕНИЕ under the floor — the OWNER’s route, corrected twice by him.
#
# Round 1 (2026-09-07): my rendering of his line turned north at x=648 and ran
# diagonally to (690, 96) — straight through V2, a concrete ventilation shaft.
#
# Round 2 (2026-09-07, same day, the black and blue arrows on his screenshot):
#   (a) the horizontal run sat mid-туалет. It belongs LOWER — further from V1,
#       the туалет’s own vent shaft, and hugging G4b, the туалет’s south wall.
#       Now y=180/186 against G4b’s north face at 192.87: 67 mm clear, and
#       675 mm off V1 instead of 597.
#   (b) I had added a turn that isn’t there: north at x=700, then EAST again to
#       reach the take-offs. He: “they should approach the wall, the outlet
#       directly — right ahead, not making an additional turn. You made it turn
#       left and then right.” He is right, and the reason is that BOTH outlets
#       already sit east of V2’s east face (714.2 and 720.5 against 677), so
#       each pipe needs exactly ONE turn: east along the floor, then straight
#       north into its own outlet. My dogleg existed only because I routed the
#       PAIR as one offset line instead of routing each pipe to its own fitting.
#
# So these are two independent routes, each ending on its own take-off, not one
# line drawn twice.
ROUTES = [(u'ГВС', R, [(90, 180), (720.49225, 180), (720.49225, 69.9953)]),
          (u'ХВС', B, [(90, 186), (730.70995, 186), (730.70995, 69.9953)])]

# no routed segment may cross a shaft or a plumbing block. The junction check
# taught this — a check that cannot fail is not a check.
BLOCKS = {'V1': (67, 70, 139, 111), 'V2': (636, 92, 677, 162),
          'P1': (52, 110, 87, 192), 'P2': (636, 71, 677, 91)}
for lbl, col, route in ROUTES:
    # P1 is the riser each route takes off FROM, so it is excluded by name,
    # not by loosening the tolerance until the check stops complaining.
    bad = route_block_conflicts(route, BLOCKS, clear_mm=60.0, connects=('P1',))
    if bad:
        raise SystemExit(u'%s route crosses a service block: %s' % (lbl, u'; '.join(bad)))
    s3.polyline_rounded(route, col, width=9, offset=0.0, r_mm=260.0)
    m = s3.P(((route[0][0] + route[1][0]) / 2.0, route[0][1] + (-5 if col is R else 9)))
    s3.d.text(m, lbl, fill=col, font=s3.f_src, anchor='mm')
print(u'  route/block clearance: %d routes, all clear of %d blocks, 1 turn each'
      % (len(ROUTES), len(BLOCKS)))
s3.callout(*(list(s3.P((380, 183))) + [[u'ГВС + ХВС под полом — трасса ВЛАДЕЛЬЦА',
                                        u'трафареты «ВОДОСНАБЖЕНИЕ» на стяжке'], B]))

# ORDER CORRECTED 2026-09-07 by the owner: in 930d the sewer socket is CLOSER
# TO THE VENTILATION SHAFT than either water outlet. I had it as the eastmost
# of the three, i.e. furthest from the shaft — exactly inverted.
#
# Note the FORM of his statement: “closer to the venting shaft” is a relation to
# a named object, and 930d is apartment 53, which is MIRRORED. Had he said “on
# the left” I would have had to invert it and would probably have got it wrong
# again. A relation to an identified object survives mirroring; left/right does
# not. This is the third time wall-handedness has bitten this sheet.
#
# What is EVIDENCE here is the ORDER only. The spacings are the canonical
# figures, not measured off this photo: the water pair 100 mm apart per
# SW-K in service_outlets.csv (“~92-111 apart”), the sewer 130 mm west of the
# hot one. Distances from the wall’s west end (x=697): 100 / 230 / 330 mm.
PIPES = [('P-S', 'G3', 0.0326, +1, MG, 'sewer', 6, u'канализация DN50 — ближе всего к шахте', '930d'),
         ('P-H', 'G3', 0.0750, +1, R, 'water', 61, u'горячая, из пола', '930d'),
         ('P-C', 'G3', 0.1076, +1, B, 'water', 61, u'холодная, из пола', '930d')]
# The three take-offs sit 100 mm apart, which at this scale is 30 sheet px —
# and each of my per-item labels is ~200 px wide. Six boxes around three
# symbols could not do anything but cover them (the owner had already flagged
# labels overlaying their icons once). So this cluster gets ONE grouped
# callout, with the symbols left clean and a single leader to the group. Which
# is also just how a real sheet annotates a group of adjacent fittings.
CLUSTER = []
for iid, wid, t, side, col, kind, h, nt, src in PIPES:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s3.P((x, y))
    s3.sym_pipe(px, py, nx, ny, col, kind)
    CLUSTER.append((px, py, iid, col, h, nt, src))
    REVIEW.append({'item_id': iid, 'kind': 'plumbing outlet', 'wall': wid, 'gang': '-',
                   'height_cm': h, 'source_photos': src, 'photo_shows': nt,
                   'position_basis': 'ORDER from 930d (sewer nearest the shaft, owner); '
                                     'spacings from service_outlets.csv, indicative',
                   'owner_verdict': '', 'owner_correction': ''})
# leader from the middle of the row, callout below it in open kitchen floor
mx = sum(c[0] for c in CLUSTER) / float(len(CLUSTER))
my = max(c[1] for c in CLUSTER)
# anchored EAST into open kitchen floor, not south onto its own pipes
s3.callout(mx + 620, my + 150, [u'ВЫВОДЫ НА СЕВЕРНОЙ СТЕНЕ КУХНИ (930d)',
                    u'P-S  канализация DN50   H=6 см — на полу',
                    u'P-H  ГВС (горячая)      H=61 см',
                    u'P-C  ХВС (холодная)     H=61 см',
                    u'канализация — БЛИЖЕ ВСЕГО К ШАХТЕ (владелец)',
                    u'шаг 100/100 мм — справочный'], B)
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
