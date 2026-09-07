# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_lib import Sheet, on_wall, beside_opening

G, B, R, MG, GY, OR = ((0, 150, 60), (0, 110, 220), (210, 30, 40),
                       (190, 60, 190), (110, 110, 110), (225, 130, 0))

# ============================================================ Лист 1 РОЗЕТКИ
s = Sheet(u'Розетки и выключатели', 1)
s.legend(lambda x, y, c: s.sym_socket(x - 20, y, 1, 0, c, 1), u'Розетка стандартная', G)
s.legend(lambda x, y, c: s.sym_socket(x - 20, y, 1, 0, c, 2), u'Розетка двойная', G)
s.legend(lambda x, y, c: s.sym_socket(x - 20, y, 1, 0, c, 1, True), u'Розетка с влагозащитой IP44', B)
s.legend(lambda x, y, c: s.sym_switch(x - 20, y, 1, 0, c, 1), u'Выключатель 1-клавишный', GY)
s.legend(lambda x, y, c: s.sym_switch(x - 20, y, 1, 0, c, 2), u'Выключатель 2-клавишный', GY)
s.note([u'H = высота от чистого пола, см.', u'',
        u'⚠ Существующее положение застройщика,', u'   снято с фотографий соседних квартир.',
        u'   Точность по горизонтали ±150 мм.', u'   Проводка будет переделана полностью.'])

SOCK = [  # wall, t, side, gang, H cm, note
    ('G3', 0.18, +1, 2, 100, u'над столешницей'),
    ('G3', 0.46, +1, 2, 100, u'над столешницей'),
    ('G3', 0.74, +1, 1, 100, None),
    ('R2', 0.55, +1, 1, 30, None),
    ('G5', 0.30, +1, 1, 30, None),
    ('G5', 0.72, +1, 1, 30, None),
    ('MC', 0.30, -1, 1, 30, None),
    ('G7', 0.35, +1, 1, 30, None),
    ('G8', 0.30, -1, 1, 30, None),
    ('G8', 0.72, -1, 1, 30, None),
    ('MB', 0.20, -1, 1, 30, None),
    ('G4a', 0.55, -1, 1, 30, None),
    ('R6', 0.50, -1, 1, 30, None),
    ('MA', 0.30, -1, 1, 30, None),
]
for wid, t, side, gang, h, nt in SOCK:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_socket(px, py, nx, ny, G, gang)
    s.htag(px + nx * 66, py + ny * 66, u'H=%d' % h, G)
    if nt:
        s.callout(px, py, [nt])

# switches by the DOOR they serve, not by a fraction along the wall.
# wet rooms switch from OUTSIDE, in the corridor - local practice.
# wall, opening, jamb, face, gang, H
SWDEF = [('G4C', 'O1', 'hi', +1, 1, 90, u'ванная, из прихожей'),
         ('G4C', 'O7', 'lo', +1, 1, 90, u'туалет, из прихожей'),
         ('G2',  'O8', 'hi', +1, 2, 90, u'прихожая'),
         ('G6',  'O5', 'hi', -1, 1, 90, u'средняя комната'),
         ('G4d', 'O6', 'hi', -1, 1, 90, u'комната 9.36'),
         ('G7',  None, None, -1, 2, 90, u'кухня-гостиная')]
SW = []
for wid, oid, jamb, side, gang, h, nt in SWDEF:
    t = beside_opening(wid, oid, jamb) if oid else 0.06
    SW.append((wid, t, side, gang, h, nt))
for wid, t, side, gang, h, nt in SW:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_switch(px, py, nx, ny, GY, gang)
    s.htag(px + nx * 62, py + ny * 62, u'H=%d' % h, GY)
    s.callout(px, py, [nt], (90, 90, 90))
s.check_openings([(w, t, h, u'выкл. ' + nt) for w, t, _sd, _g, h, nt in SW]
                 + [(w, t, h, u'розетка') for w, t, _sd, _g, h, _n in SOCK])
x, y, nx, ny = on_wall('G4C', 0.30, +1)
px, py = s.P((x, y))
s.callout(px, py, [u'2 круглые коробки H=210', u'⚠ назначение не определено'], (180, 100, 0))
s.save('sheet_01_sockets.png')

# ========================================================== Лист 2 ОСВЕЩЕНИЕ
s = Sheet(u'Освещение', 2)
s.legend(lambda x, y, c: s.sym_ceiling(x, y, c, False, True), u'Подвесной светильник (вывод)', G)
s.legend(lambda x, y, c: s.sym_ceiling(x, y, c), u'Светильник встраиваемый', G)
s.legend(lambda x, y, c: s.sym_ceiling(x, y, c, True), u'Светильник встр. двойной', G)
s.legend(lambda x, y, c: s.sym_switch(x - 20, y, 1, 0, c, 1), u'Выключатель', GY)
s.note([u'⚠ Показаны ТОЛЬКО существующие выводы', u'   застройщика — по одному кабелю с патроном',
        u'   на комнату, кроме кухни-гостиной.', u'',
        u'✅ В кухне-гостиной выводов ДВА — застройщик',
        u'   разводит это помещение как ДВЕ ЗОНЫ,', u'   что подтверждает «жилая с кухонным',
        u'   оборудованием» на обмерных планах.'])

LIGHT = [(860, 150, u'вывод 1 — зона кухни', True),
         (860, 620, u'вывод 2 — зона гостиной', True),
         (430, 200, u'прихожая', True),
         (495, 520, u'средняя комната', True),
         (150, 500, u'комната 9.36', True),
         (150, 150, u'туалет', False),
         (150, 300, u'ванная', False)]
for bx, by, nt, pend in LIGHT:
    px, py = s.P((bx, by))
    s.sym_ceiling(px, py, G, False, pend)
    s.callout(px, py, [nt] if pend else [nt, u'⚠ не подтверждён'],
              (40, 40, 40) if pend else (180, 100, 0))
for wid, t, side, gang, h, nt in SW:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_switch(px, py, nx, ny, GY, gang)
s.save('sheet_02_lighting.png')

# ============================================ Лист 3 ВОДОСНАБЖЕНИЕ И КАНАЛИЗАЦИЯ
s = Sheet(u'Водоснабжение, канализация, вентиляция', 3)
s.legend(lambda x, y, c: s.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод холодной воды', B)
s.legend(lambda x, y, c: s.sym_pipe(x - 20, y, 1, 0, c, 'water'), u'Вывод горячей воды', R)
s.legend(lambda x, y, c: s.sym_pipe(x - 20, y, 1, 0, c, 'sewer'), u'Вывод канализации DN50', MG)
s.legend(lambda x, y, c: s.d.rectangle([x - 22, y - 16, x + 22, y + 16], outline=c, width=6),
         u'Стояк / сантехблок', B)
s.legend(lambda x, y, c: s.d.rectangle([x - 22, y - 16, x + 22, y + 16], outline=c, width=6),
         u'Вентиляционный короб', OR)
s.legend(lambda x, y, c: [s.d.line([(x - 26 + k * 16, y), (x - 26 + k * 16 + 9, y)], fill=c, width=7)
                          for k in range(4)], u'Магистраль под полом (трасса)', B)
s.note([u'✅ Сплошной контур — положение определено', u'   по НАШЕМУ плану.',
        u'⚠ Пунктирная трасса — известны только КОНЦЫ;',
        u'   путь под полом нанести по факту.', u'',
        u'✕ ОТОПЛЕНИЕ на листе НЕ показано — трасса',
        u'   нигде не зафиксирована. Трафареты на стяжке',
        u'   читаются «ВОДОСНАБЖЕНИЕ», не «ОТОПЛЕНИЕ».'])

for bid, (x0, y0, x1, y1), col in (('V1', (67, 70, 139, 111), OR), ('V2', (636, 92, 677, 162), OR),
                                   ('P1', (52, 110, 87, 192), B), ('P2', (636, 71, 677, 91), B)):
    p0, p1 = s.P((x0, y0)), s.P((x1, y1))
    s.d.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=col + (48,), outline=col, width=6)
    s.d.text(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), bid, fill=col, font=None, anchor='mm')

ROUTE = [(70, 178), (200, 252), (455, 252), (622, 120), (688, 86)]
for i in range(len(ROUTE) - 1):
    a, b = s.P(ROUTE[i]), s.P(ROUTE[i + 1])
    n = max(2, int((abs(b[0] - a[0]) + abs(b[1] - a[1])) / 30))
    for k in range(0, n, 2):
        t0, t1 = k / float(n), min(1.0, (k + 1) / float(n))
        s.d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                  (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                 fill=B + (235,), width=12)

PIPES = [('G3', 0.055, +1, R, 'water', 61, u'горячая, из пола'),
         ('G3', 0.075, +1, B, 'water', 61, u'холодная, из пола'),
         ('G3', 0.115, +1, MG, 'sewer', 6, u'канализация DN50, на стяжке')]
for wid, t, side, col, kind, h, nt in PIPES:
    x, y, nx, ny = on_wall(wid, t, side)
    px, py = s.P((x, y))
    s.sym_pipe(px, py, nx, ny, col, kind)
    s.htag(px + nx * 62, py + ny * 62, u'H=%d' % h, col)
    s.callout(px, py, [nt], col)
for bx, by, nt in ((103, 92, u'решётка вытяжки H=218'), (656, 128, u'решётка вытяжки H=218')):
    px, py = s.P((bx, by))
    s.d.ellipse([px - 16, py - 16, px + 16, py + 16], outline=OR, width=6)
    s.callout(px, py, [nt], OR)
px, py = s.P((69, 152))
s.callout(px, py, [u'P1: стояк канализации DN110,', u'стояки ГВС/ХВС со счётчиками,',
                   u'изолированный стояк (отопление?)'], B)
s.save('sheet_03_plumbing.png')
