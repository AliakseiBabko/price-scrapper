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
from make_segment_key_sheet import label_segments, outline_segments

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
# Segment bands FIRST, so the legend text and every symbol sit ON them
# rather than under a translucent wash. Lighter than sheet 00: here they
# must not compete with the devices they underlie.
outline_segments(s, fill_alpha=20)
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
# Wall codes last, so spot() routes them around the symbols above.
print('  s segment labels: %d' % label_segments(s, tiny=True))
s.save('sheet_01_sockets.png')

# ========================================================== Лист 2 ОСВЕЩЕНИЕ
s2 = Sheet(u'Освещение', 2)
# Segment bands FIRST, so the legend text and every symbol sit ON them
# rather than under a translucent wash. Lighter than sheet 00: here they
# must not compete with the devices they underlie.
outline_segments(s2, fill_alpha=20)
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
# Wall codes last, so spot() routes them around the symbols above.
print('  s2 segment labels: %d' % label_segments(s2, tiny=True))
s2.save('sheet_02_lighting.png')

# ============================================ Лист 3 ВОДОСНАБЖЕНИЕ И КАНАЛИЗАЦИЯ
s3 = Sheet(u'Водоснабжение, канализация, вентиляция', 3)
# Segment bands FIRST, so the legend text and every symbol sit ON them
# rather than under a translucent wash. Lighter than sheet 00: here they
# must not compete with the devices they underlie.
outline_segments(s3, fill_alpha=20)
s3.f_src = __import__('sheet_lib').F(21)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод холодной воды', B)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод горячей воды', R)
s3.legend(lambda x, y, c: s3.sym_pipe(x - 20, y, 1, 0, c, 'sewer'), u'Вывод канализации DN50', MG)
s3.legend(lambda x, y, c: s3.d.line([(x - 26, y), (x + 26, y)], fill=MG, width=9),
          u'Лежак канализации DN50 по низу стены', MG)
s3.legend(lambda x, y, c: s3.d.line([(x - 26, y), (x + 26, y)], fill=GY, width=5),
          u'— в ванной: ТОПОЛОГИЯ по b83a, не разметка', GY)
s3.legend(lambda x, y, c: s3.sym_riser(x - 20, y, c, dn=True),
          u'Стояк канализации DN110 — транзит (их ДВА)', MG)
s3.legend(lambda x, y, c: s3.sym_valve(x - 20, y, c), u'Запорный вентиль', R)
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
# The SEWER RUN, added 2026-09-07 on the owner: I had drawn the DN50 socket
# and never drawn the pipe it connects to. 930d shows it plainly — a grey PVC
# pipe running HORIZONTALLY along the wall base from the socket and continuing
# into a chase behind the shaft. So it is drawn as observed: west along G3’s
# base from the socket, disappearing behind the V2/P2 block.
#
# It stops there ON PURPOSE. The only sewer stack in the record is SS-B, DN110,
# in P1 in the туалет — about 6 m away — and no photo shows how this DN50
# reaches it, or whether P2 holds a second riser instead. The photo shows the
# pipe entering the chase and nothing beyond, so that is where the line ends
# and the callout says so. Drawing a 6 m branch across the flat would be
# inventing an element, which is the rule the З1/З2 voids broke.
SEWER = [(707.22765, 69.9953), (672, 69.9953)]

# RETRACTED 2026-09-07, same day it was drawn. I built a 6.3 m DN110 лежак from
# P2 to P1 out of the owner’s words “behind the V2 venting shaft, AND THEN behind
# the water closet”. He was naming TWO PLACES, not describing a route. His
# correction: “two sewage pipes — one behind the water closet and another one
# behind the second vent shaft, next to the kitchen … the transit from the top of
# the building to the bottom.” They are two STACKS, both DN110, each running the
# full height of the building. There is no horizontal main across this flat.
#
# What I did wrong is not the reading — it is that the reading FIT TOO WELL. Two
# midpoints from one sentence both landed on my route, and y=152 landed inside
# P1’s span, and I called that corroboration. It was not: a 250 mm-wide corridor
# between two fixed obstacles has a midline whatever runs along it, and P1 spans
# 80 px so almost any y hits it. I checked BEFORE drawing and still fooled
# myself, because I tested whether the geometry ALLOWED my route instead of
# whether the evidence REQUIRED it. Consequence: the 125 mm screed-fall warning
# and the G4C penetration were both consequences of an element that is not there.

# ============ ВЫВОДЫ В ВАННУЮ — топология из b83a ============
# b83a (the owner’s annotated photo of a туалет in a comparable flat) shows the
# arrangement he wants applied: the ГВС / ХВС / канализация risers stand in the
# niche at the far end, the two water meters sit at mid height on the risers,
# and all three services then drop and leave the туалет AT LOW LEVEL — his
# label on the photo reads “to the bathroom”.
#
# My sheet had NOTHING in the ванная. A bath and a basin were on the plan the
# whole time and I had drawn no water and no drain to either. Third omission of
# the same kind in one day, and the biggest.
#
# On our plan this is a very short route, which is itself a check on the
# reading: P1 (x 52..87, y 110..192) sits directly NORTH of the bath’s head
# (bath x 52..123, y 202..378) with only G4b between them, and the basin is on
# G4b just east of it (x 125..185). So “to the bathroom” is a metre of pipe.
#
# ⚠ TOPOLOGY, NOT A SETTING-OUT. His words: “the specific layout could be
# different … but the general approach is the same”, and more examples are
# coming. Positions within the ванная are indicative and the sheet says so.
BATH_W = [(70, 190), (70, 212), (152, 212)]          # ГВС+ХВС: P1 -> ванна -> раковина
BATH_S = [(150, 220), (78, 220), (78, 191)]          # DN50: раковина/ванна -> стояк SS-B

ROUTES = [(u'ГВС', R, [(90, 180), (720.49225, 180), (720.49225, 69.9953)]),
          (u'ХВС', B, [(90, 186), (730.70995, 186), (730.70995, 69.9953)]),
          (u'DN50', MG, SEWER),
          (u'ГВС-в', R, BATH_W), (u'ХВС-в', B, [(p[0], p[1] + 5) for p in BATH_W]),
          (u'DN50-в', MG, BATH_S)]

# no routed segment may cross a shaft or a plumbing block. The junction check
# taught this — a check that cannot fail is not a check.
BLOCKS = {'V1': (67, 70, 139, 111), 'V2': (636, 92, 677, 162),
          'P1': (52, 110, 87, 192), 'P2': (636, 71, 677, 91)}
for lbl, col, route in ROUTES:
    # P1 is the riser each route takes off FROM, so it is excluded by name,
    # not by loosening the tolerance until the check stops complaining.
    # each route is exempted only from the block it TAKES OFF FROM or RUNS
    # INTO - by name, not by loosening the tolerance until the check goes quiet.
    # every route here either takes off from a block or runs into one;
    # exempt only that block, by name.
    conn = ('P2',) if route is SEWER else ('P1',)
    bad = route_block_conflicts(route, BLOCKS, clear_mm=60.0, connects=conn)
    if bad:
        raise SystemExit(u'%s route crosses a service block: %s' % (lbl, u'; '.join(bad)))
    s3.polyline_rounded(route, col, width=9, offset=0.0, r_mm=260.0)
    if col is not MG and route is not BATH_W:   # short runs: label would sit on a block
        m = s3.P(((route[0][0] + route[1][0]) / 2.0, route[0][1] + (-5 if col is R else 9)))
        s3.d.text(m, lbl, fill=col, font=s3.f_src, anchor='mm')
print(u'  route/block clearance: %d routes, all clear of %d blocks, 1 turn each'
      % (len(ROUTES), len(BLOCKS)))
s3.callout(*(list(s3.P((380, 183))) + [[u'ГВС + ХВС под полом — трасса ВЛАДЕЛЬЦА',
                                        u'трафареты «ВОДОСНАБЖЕНИЕ» на стяжке'], B]))
# was “продолжение НЕ ЗАФИКСИРОВАНО” — the owner has now answered it, so the
# open question is closed and the note says what it connects to instead.
s3.callout(*(list(s3.P((684, 70))) + [[u'Лежак DN50 уходит за шахту — 930d',
                                       u'врезка в стояк SS-K2 за шахтой V2 —',
                                       u'второй транзитный стояк (владелец)',
                                       u'горизонтальной магистрали по квартире НЕТ'], MG, (-380, 640)]))

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
# The SECOND VALVE NODE is RETRACTED too, drawn and withdrawn the same day.
# I heard “two switch points” as two valve groups. Owner: “only ONE valve node,
# [in] the water closet” — the two things behind V2 and behind the туалет are the
# two SEWER STACKS, which is what he had been telling me all along. “Switch
# point” was my word, and I built a fitting out of it.

# ============ P1, САНТЕХБЛОК В ТУАЛЕТЕ ============
# The owner: “you can directly draw another outlet for both hot and cold water
# and the switch as well.” — the “switch” being the shut-off VALVE, and the
# outlets being SW-B, the risers with meters. All three of P1’s services have
# been sitting in service_outlets.csv since it was written and NONE of them had
# ever been drawn. Exactly the same omission as the sewer run: I had drawn only
# the kitchen items and left the flat’s entire service block off its own
# services sheet. Recording a finding is not delivering it.
#
# Heights are the CSV’s: SW-B meters ~1380, valves ~1630, the two sewers and
# the insulated riser floor to ceiling.
# ARRANGEMENT per the owner 2026-09-07: “the sewage pipe is in the middle
# approximately between the walls, and the valve node is kind of closer to the
# venting shaft.” V1 sits directly north of P1, so the valves go north (nearest
# V1) and the stack sits near the mid-line between R1a’s south face (69.8) and
# G4b’s north face (192.87), i.e. y ≈ 131. SH-B keeps the south end.
P1SVC = [('SW-B-H', 70, 114, R, 'valve', u'ГВС: стояк, счётчик H=138, вентиль H=163', 'ade6'),
         ('SW-B-C', 70, 122, B, 'valve', u'ХВС: стояк, счётчик H=138, вентиль H=163', 'ade6'),
         ('SS-B', 70, 133, MG, 'riser', u'стояк канализации DN110 — транзит по всей высоте дома', 'ade6'),
         ('SH-B', 70, 165, GY, 'riser', u'стояк в изоляции — НАЗНАЧЕНИЕ НЕ ПОДТВЕРЖДЕНО', 'ade6'),
         # the SECOND sewer stack — behind V2, on the kitchen side. Owner: “two
         # sewage pipes … the transit from the top of the building to the bottom.”
         # This is what the kitchen DN50 лежак runs into, and it is why no
         # horizontal main across the flat was ever needed.
         ('SS-K2', 656, 81, MG, 'riser', u'стояк канализации DN110 за шахтой V2 — второй транзитный стояк', u'владелец')]
for iid, bx, by, col, kind, nt, src in P1SVC:
    px, py = s3.P((bx, by))
    if kind == 'riser':
        s3.sym_riser(px, py, col, dn=iid.startswith('SS-'))
    else:
        s3.sym_valve(px, py, col)
    REVIEW.append({'item_id': iid, 'kind': 'service riser / valve, P1', 'wall': 'P1',
                   'gang': '-', 'height_cm': 'floor-ceiling', 'source_photos': src,
                   'photo_shows': nt,
                   'position_basis': 'inside P1 per service_outlets.csv; '
                                     'arrangement WITHIN the block indicative',
                   'owner_verdict': '', 'owner_correction': ''})
s3.callout(*(list(s3.P((120, 214))) + [[u'ВАННАЯ — ОБЩИЙ ПОДХОД по b83a',
                                        u'ГВС + ХВС из узла P1 по низу — на ванну,',
                                        u'далее на раковину на G4b',
                                        u'DN50 от раковины и ванны — в стояк SS-B',
                                        u'проход через G4b (блок 120 мм)',
                                        u'⚠ ТОПОЛОГИЯ, НЕ РАЗМЕТКА — владелец:',
                                        u'   «раскладка может отличаться, подход тот же»'], B, (280, 520)]))
s3.callout(*(list(s3.P((87, 150))) + [[u'P1 — САНТЕХБЛОК (ade6)',
                                       u'SS-B  стояк канализации DN110 — транзит',
                                       u'      сверху донизу дома; примерно по середине',
                                       u'      между стенами; вентили — ближе к шахте V1',
                                       u'SW-B  ГВС + ХВС: счётчики H=138,',
                                       u'      вентили H=163',
                                       u'SH-B  стояк в изоляции — не подтверждён',
                                       u'      как отопление',
                                       u'УЗЕЛ ЗАПОРНЫХ ВЕНТИЛЕЙ — ТОЛЬКО ОДИН,',
                                       u'здесь, в туалете (владелец)',
                                       u'счётчики — по середине высоты стояков (b83a)'], B, (170, 560)]))



# ============ ВЕНТИЛЯЦИЯ: ВАННАЯ ДЫШИТ ЧЕРЕЗ ТУАЛЕТ ============
# Owner on the two circles in b83a: “they are two venting openings — first, we
# connect the venting shaft with the water closet, and another connects water
# closet with the bathroom.”
#
# So the extract path is ВАННАЯ → ТУАЛЕТ → V1. The ванная has NO duct of its
# own: it has a high-level transfer opening through G4b, and the туалет alone
# is grilled into the shaft.
#
# My service_outlets.csv had SV-V as “ventilation extract grille, ванная, on
# V1”, which is geometrically IMPOSSIBLE and our own wall model said so before
# any of this: V1 ends at y=111 and the ванная begins at G4b’s south face,
# y=205.1 — 921 mm of туалет floor in between. The block never touches the
# ванная. That is independent corroboration in the way the retracted лежак’s
# midpoints were NOT: the model was built from linear dimensions with no
# knowledge of ventilation, so it had no way to agree by construction.
#
# ⚠ The POSITION along G4b is indicative — b83a is a different flat with a
# deeper туалет, and left/right in it says nothing about ours. What transfers
# is the topology. Placed east of the basin (which ends at x=185) so it is
# clear of both the basin and P1.
px, py = s3.P((200, 199))
s3.sym_transfer(px, py, OR, 0, -1)
s3.callout(px, py, [u'ПЕРЕТОЧНОЕ ОТВЕРСТИЕ у потолка (b83a)',
                    u'ванная → туалет → шахта V1',
                    u'у ванной НЕТ своего канала — вытяжка',
                    u'только через туалет. Не закрывать при отделке',
                    u'⚠ положение по G4b — справочное, уточнить'], OR, (330, 300))
s3.legend(lambda x, y, c: s3.sym_transfer(x - 20, y, c, 1, 0),
          u'Переточное отверстие у потолка', OR)
REVIEW.append({'item_id': 'SV-VT', 'kind': 'transfer opening, high level',
               'wall': 'G4b', 'gang': '-', 'height_cm': u'у потолка',
               'source_photos': 'b83a', 'photo_shows': u'ванная → туалет, второе — туалет → V1',
               'position_basis': u'TOPOLOGY from the owner; position along G4b indicative',
               'owner_verdict': '', 'owner_correction': ''})

for iid, bx, by, nt, src in (('V-1', 103, 92, u'решётка вытяжки H=218', '930d + 9e9b'),
                             ('V-2', 656, 128, u'решётка вытяжки H=218', '9e9b')):
    px, py = s3.P((bx, by))
    s3.d.ellipse([px - 16, py - 16, px + 16, py + 16], outline=OR, width=6)
    s3.callout(px, py, [nt], OR)
    tagsrc(s3, px, py, iid, src, OR)
# Wall codes last, so spot() routes them around the symbols above.
print('  s3 segment labels: %d' % label_segments(s3, tiny=True))
s3.save('sheet_03_plumbing.png')

FN = ['item_id', 'kind', 'wall', 'gang', 'height_cm', 'source_photos', 'photo_shows',
      'position_basis', 'owner_verdict', 'owner_correction']
with io.open('data/canonical/electrical_placement_review.csv', 'w',
             encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FN)
    w.writeheader(); w.writerows(REVIEW)
noph = sum(1 for r in REVIEW if r['source_photos'] == NOPH)
print('review table: %d items, %d with NO photo basis' % (len(REVIEW), noph))
