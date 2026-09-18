---
source_id: YT_1WakaBxLkVg
title: "Я построил квартиру в 3D c помощью SketchUp и Claude"
channel: "Степан Огурцов"
url: https://www.youtube.com/watch?v=1WakaBxLkVg
video_id: 1WakaBxLkVg
upload_date: 2026-09-16
duration: "9:09"
language: ru
region: russia_level2_channel_only
processed: 2026-09-18
transcript_file: _Archive/processed_sources/1WakaBxLkVg.ru.txt
---

# Building an apartment in 3D with SketchUp + Claude — what worked, what broke

**Степан Огурцов**, a practising 3D designer, models an apartment from a supplied drawing using Claude to generate Ruby, and narrates every failure. **This is the closest source in the vault to what this project is actually doing**, and it corroborates the architecture while naming the exact hazard.

## ⚠️⚠️ GENERATE A SCRIPT, DO NOT DRIVE THE MODELLER LIVE

> *«Здесь многие ошибаются, берут прямое подключение и сжигают кучу токенов, кучу ресурсов в нейро. Платят за это очень много. А со скетчапом можно работать с помощью Ruby, и это гораздо дешевле.»*

**Огурцов names the direct live connection as the common mistake** — it burns tokens and costs a great deal — and works instead by having the model **emit a Ruby script that he pastes into SketchUp's console.** He states it as a cost argument, not an architectural one.

⚠️ **This is in direct opposition to `YT_BFImll1TqYE`**, which is a tutorial for exactly the live-MCP setup he calls the mistake. See the Perspectives block on the toolchain page.

## The dimensions came out right — and the MEANING came out wrong

He spot-checks the generated model against the drawing and finds it exact: *«Вот этот вот у нас 3261. Точно совпадает… эта длина 4673»* — *«будто бы он прямо оцифровал правильно модель»*.

**Then the semantic failure:**

> *«Он почему-то решил, что здесь лоджия, а здесь короб с коммуникациями.»*

**It swapped a services duct and a лоджия.** He forgives it as a small error — but the shape of it is the point: **millimetre-accurate geometry carrying the wrong identity.** He also notes it merged windows into the wrong wall *«потому что, видимо, понял, что это лоджия на своё усмотрение»* — it decided, on its own initiative, what the space was.

## ⚠️⚠️ THE GOVERNING WARNING — the model does not consider its mistakes mistakes

> *«Вы должны понимать, что происходит, что это за процесс, чтобы видеть косяки нейросетки, которые всплывают внезапно, а нейросеть их косяками-то и не считает.»*

And, after being stuck cleaning a geometry mess:

> *«Если бы экспертности в области скетчапа у меня не было, то я бы и не смог найти выход из этой проблемы. Просто плюнул бы, и результат был бы потерян.»*

**His own worked example of this**: `cleanup` would not merge the geometry, and he could not see why. He solved it by asking Claude *how to make a solid group* — i.e. he used the model to diagnose the model's output, but only because he knew enough to ask the right question.

## Prompt iteration converged on subtraction, not addition

His final working instruction was a list of things **not** to make:

> *«Не делай пол, не делай окна, не делай двери. Нужна только геометрия стен и проёмов внутри них. А так пусть всё будет сплошной группой.»*

Walls and openings only, as one solid group. Even then it needed a cleanup pass and a colour strip.

## The division of labour he settles on

**Windows, sills, doors, radiators and textures he then places BY HAND** — *«Дальше уже работаю вручную»* — and concludes:

> *«Здесь мы убираем с помощью нейросетей часть рутины. Остальную часть нужно не бояться делать ручками, как прежде. Нужно контролировать экспертно этот процесс.»*

**The AI removes part of the routine. The rest is done by hand, under expert control.**

## Source Notes

- Promotional content: moderate — two plugs for his own 3D design courses, and a QR for a "ремонт по фотке" visualisation service. The technical narration is unaffected by it.
- No prices for renovation work. Course pricing not stated.
- Region: Russia at channel level only; no city named. No figure here needs a location.
