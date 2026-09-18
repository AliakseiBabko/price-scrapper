---
source_id: YT_KTvihMIPFVk
title: "Нейросеть нарисовала мне кухню в SketchUp. 3 способа"
channel: "Степан Огурцов"
url: https://www.youtube.com/watch?v=KTvihMIPFVk
video_id: KTvihMIPFVk
upload_date: 2026-09-17
duration: "15:32"
language: ru
region: not_region_specific_tooling
processed: 2026-09-18
transcript_file: _Archive/processed_sources/KTvihMIPFVk.ru.txt
---

# Three routes from a drawing to a dimensioned SketchUp model — all via generated Ruby

Огурцов tests three inputs through the same pipe: **Claude → Ruby script → paste into SketchUp's console.** He never connects live.

| route | input | outcome |
| :--- | :--- | :--- |
| 1 | a kitchen firm's **dimensioned drawing** | sizes correct (80, 60 verified) — **but the whole thing came out MIRRORED** |
| 2 | a **hand sketch** | good; ⚠️ **Claude caught an error in the sketch itself** — *«справа написано 580, а не 850»* |
| 3 | **his own rough massing** + screenshot + a style reference image | best result; the style reference was respected |

## ⚠️⚠️ The cost argument, now with a mechanism

The earlier note recorded his claim that live connection is expensive as a bare assertion. Here he gives the reason:

> *«Так как он просто пишет код, по сути он не программирует расположение мыши, да, не бегает мышью и не мучает сам себя, он пишет код… и это маленький расход лимитов. Самое главное, что можно даже на базовой подписке получать много-много таких размерных элементов.»*

**Writing code is not driving a mouse.** He reports the whole exercise fits inside a basic subscription. ⚠️ **Still no measured figures** — but a stated mechanism is more than the opposing source offers.

## Model selection is deliberate, and he states the rule

- **Sonnet for plain geometry**, to economise — *«Выберем модель Sonnet попроще, чтобы экономить ресурсы»*.
- **Opus when detail is wanted** — *«Именно Опус нужно использовать… модель помощнее, так как мы будем просить детализации»*, and *«Мне нравится Опус тем, что он детали лучше прорисовывает»*.
- The detailed run took **over 10 minutes**.

## The error-recovery loop

When a script threw, he pasted the error straight back: *«вот это то, что у нас с ошибочкой вылетело, можно вставить обратно в Клода… Он сам должен разобраться, в чём тут проблема, и починить этот код.»* It worked.

## ⚠️ The same semantic failure as the apartment video

It modelled **drinking glasses where taps belonged** — *«Он говорит: "Это стекло со стаканами", а на самом деле… наверное, краны всё-таки предполагались»* — and mirrored an entire kitchen without noticing.

> **Two videos, two subjects, one failure class: dimensions right, OBJECT IDENTITY wrong.** In `YT_1WakaBxLkVg` it was a лоджия and a services duct; here it is taps, glasses and a mirrored layout. **This is a pattern across sources now, not an anecdote.**

## Incidental but useful

**The generated Ruby runs on old SketchUp**, including SketchUp Make 2017 — *«этот код работает и на старых версиях»*. A generated script has no version floor the way a live plugin does.

## Source Notes

- Promotional: moderate — two plugs for his own workshop. The technical demonstration stands on its own.
- No prices. Not region-specific.
