# -*- coding: utf-8 -*-
"""Лист 5 — ОТОПЛЕНИЕ.

Its own script, and its own sheet, because the reference album keeps one
service per sheet. See `convention` in zk-dubravinskiy-full-album.json.

Deliberately SPARSE. The owner asked for this sheet "even empty" so he can draw
the preliminary pipe trace on it by hand, the way he drew the водоснабжение
route on sheet 3 — and that worked precisely because there was clear floor to
draw on. So: radiators, the riser, the openings for reference, notes pushed to
the margins, and nothing in the middle of any room.

What is drawn is only what is derivable or recorded:
  * three radiators, one under each external window, from wall_opening_spans
  * SH-B, flagged as a HYPOTHESIS, not a fact
  * the heat meter as a QUESTION mark, because building_spec says one exists
    and nothing in the survey has located it
The pipe route is left blank on purpose. It is the one service with no trace.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_lib import Sheet, RUNS, SPANS, MMPX, S, F  # noqa: E402

R, B, GY, OR, GN = ((210, 30, 40), (0, 110, 220), (110, 110, 110),
                    (225, 130, 0), (0, 150, 60))

s5 = Sheet(u'Отопление', 5)
s5.f_src = F(21)

# ---------------------------------------------------------------- радиаторы
# A radiator sits on the INSIDE face of its external wall, under the window.
# All three of ours face north into their room: комната 9.36 is north of MA,
# средняя комната north of MB, кухня-гостиная north of MC.
DEPTH_MM = 110.0          # a typical panel radiator, for the plan footprint
COVER = 0.80              # of the opening width — indicative, not a selection

RADS = [('RAD-1', 'MA', 'O4', u'комната 9.36',
         u'⚠ ПОД ОКОННОЙ ЧАСТЬЮ O4 — но какая из створок дверь, НЕ РЕШЕНО'),
        ('RAD-2', 'MB', 'O2', u'средняя комната 16.63', u''),
        ('RAD-3', 'MC', 'O3', u'кухня-гостиная 24.73', u'')]

for rid, wid, oid, room, warn in RADS:
    ax, ay, bx, by, th = RUNS[wid]
    face = ay - th / 2.0 / MMPX                  # north face, into the room
    lo, hi = [(o[1], o[2]) for o in SPANS[wid] if o[0] == oid][0]
    mid, half = (lo + hi) / 2.0, (hi - lo) * COVER / 2.0
    d = DEPTH_MM / MMPX
    p0 = s5.P((mid - half, face - d))
    p1 = s5.P((mid + half, face))
    s5.sym_radiator(p0[0], p0[1], p1[0], p1[1], R)
    cx, cy = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
    s5.htag(cx, cy, u'%s · %s' % (rid, oid), R, 0, -1)

# --------------------------------------------------------------- стояк SH-B
px, py = s5.P((70, 165))
s5.sym_meter(px, py, GY, u'?')
s5.htag(px, py, u'SH-B ?', GY, -1, 0)

# ------------------------------------------------------------------ легенда
s5.legend(lambda x, y, c: s5.sym_radiator(x - 34, y - 11, x + 34, y + 11, c, 5),
          u'Радиатор отопления (установлен застройщиком)', R)
s5.legend(lambda x, y, c: s5.sym_meter(x - 20, y, c, u'?'),
          u'Счётчик тепла — НЕ НАЙДЕН, положение под вопросом', GY)
s5.legend(lambda x, y, c: [s5.d.line([(x - 26, y), (x + 26, y)], fill=c, width=9)],
          u'Трубы отопления — НЕ НАНЕСЕНЫ (см. ниже)', GN)

# Everything that would otherwise be a callout lives HERE, in the margin. The
# owner draws on this sheet, so the plan itself must stay clear - that is why
# his ГВС/ХВС line on sheet 3 worked.
s5.note([u'ЛИСТ НАМЕРЕННО ПУСТОЙ В ЧАСТИ ТРАСС.', u'',
         u'✅ Что известно: застройщик сдаёт квартиру с уже',
         u'   установленными радиаторами и ГОРИЗОНТАЛЬНОЙ',
         u'   разводкой труб отопления со счётчиком тепла',
         u'   (building_spec.json). Значит трубы — в стяжке.', u'',
         u'✅ Радиаторы: по одному под каждым окном; положение',
         u'   выведено из проёмов O4 / O2 / O3. Лоджия не',
         u'   отапливается. Длина показана условно — 80% проёма.', u'',
         u'⚠ RAD-1 (комната 9.36): показан по центру O4, но',
         u'   O4 — это окно + балконная дверь, а какая из',
         u'   створок дверь — НЕ РЕШЕНО. Радиатор стоит',
         u'   под ОКОННОЙ половиной — уточнить сторону.', u'',
         u'? SH-B — стояк в изоляции в туалете (P1).',
         u'   ГИПОТЕЗА: это стояк отопления. Горизонтальная',
         u'   разводка со счётчиком требует стояка в блоке;',
         u'   SH-B — единственный в изоляции. НЕ ПОДТВЕРЖДЕНО.',
         u'   ПРОВЕРКА: рядом должен быть счётчик ТЕПЛА —',
         u'   не воды. На b83a два водяных, значит нужен 3-й.', u'',
         u'✕ ТРАССА ТРУБ НЕ ЗАФИКСИРОВАНА НИГДЕ. Это',
         u'   единственная служба без единого следа, и причина',
         u'   моя: трафарет на стяжке я трижды прочитал как',
         u'   «ОТОПЛЕНИЕ», а там «ВОДОСНАБЖЕНИЕ», поэтому',
         u'   отопительный никто и не искал.', u'',
         u'➜ ПРОШУ НАНЕСТИ ТРАССУ ОТ РУКИ — как Вы сделали',
         u'   с ГВС/ХВС на листе 3. Пол оставлен чистым.',
         u'   Достаточно предварительной линии от стояка',
         u'   к каждому радиатору.'])

s5.save('sheet_05_heating.png')
