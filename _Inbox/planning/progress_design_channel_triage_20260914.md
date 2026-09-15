# Channel triage — @progress-design (Progress Design, transformer-furniture maker, Moscow)

**Date:** 2026-09-14 · **Owner-supplied** · **169 videos** · **Status: triaged; 3 spot-checked and read, 2 blocked by a 429; Tier 1 proposed, NOT yet processed**

**Owner's steer:** *furniture — Murphy beds, Murphy tables, other kinds of furniture. Could see a lot of useful content for the wiki project.*

---

## ⚠️⚠️ 1. Read this before deciding how much of it to process

**This is ONE vendor, and the vault already holds four of its videos** (`4xZ-9vlXV7Y`, `tRv7QSUoqpg` from 2026-08-25; `u_gIgDqRdYw`, `hT4Whu6F2gs` from today's Req V). **Dedup: 4 of 169 already processed, 165 fresh.**

> **⚠️⚠️ THE RISK HERE IS NOT LOW YIELD — IT IS MANUFACTURED CORROBORATION, AND THIS VAULT HAS ALREADY BEEN BITTEN BY IT ONCE TODAY.** In the batch just merged I wrote up FREE_DOM's `qMGSfO-glvc` as a *third independent voice* against retention straps, and it was not: the vault's existing "against straps" entry cites `wfmIOYsE2Hs`, **the same channel**. Corrected before commit, but only because I happened to open the existing entry.
>
> **Processing 40 videos from one maker would produce dozens of claims that LOOK mutually corroborating and are one company's house style.** The wall-bed pages currently derive their weight from having several unrelated makers disagreeing. **A large Progress Design slice would quietly invert that.**

**→ The recommendation below is therefore deliberately narrow, and it is organised around what only THIS vendor can add, not around what sounds useful.**

---

## ⚠️⚠️ 2. Coverage check — where this channel meets an EMPTY shelf

A grep across `_Sources/`, `00_Master/` and every numbered folder:

| Topic | Files in the vault | Verdict |
| :--- | ---: | :--- |
| wall beds / шкаф-кровать / Murphy | **28** | **Saturated.** And note: almost entirely maker-sourced |
| gas struts / газлифты | 4 | Covered, and today's batch gave it a pass/fail test |
| voice control, smart home + bed | 8 | Partly covered on the smart-home page |
| **⚠️⚠️ transformer TABLES — `стол-трансформер`, `откидной стол`** | **0** | **⚠️⚠️ ZERO. Nothing in the vault, in any folder, under any spelling** |
| mattress rated for **vertical storage** | 0 (the 2 hits are storage-organising, not mattresses) | **Empty** |

> **⚠️⚠️ THE OWNER NAMED "MURPHY TABLES" AND THE VAULT HAS NOTHING ON THEM.** That is the single clearest gap this channel can fill, and it is the part of his steer that is NOT already saturated. **The wall-bed half of the channel is the part to be stingy with; the table half is the part to actually take.**

---

## ⚠️ 3. Spot-check — 3 fetched and read, and they changed the shortlist

**Serialized, `--languages ru`, `--fetch-upload-date`. ⚠️ Two of the five hit `HTTP 429` and were NOT retried — no further fetching this run.**

⚠️ **A process note against myself:** my fetch loop tested `rc=$?` after a pipe, so it read `tail`'s exit code and the rule-7 circuit breaker never fired — it kept going after the first 429. No harm done (the two failures wrote `.FAILED` sidecars and nothing was corrupted), but the breaker only works if the exit code is captured before the pipe.

| Video | Verdict |
| :--- | :--- |
| **`jZAAwUZVb0I` "How to Choose a Transformer \| Types, Mechanisms"** | **⚠️⚠️ TAKE — the best single video on the channel.** Carries **three things the vault does not have** (below) |
| **`KgBcJ4zAHi8` "What happened to the furniture after 7 years?"** | **⚠️⚠️ TAKE — a genuine 7-YEAR post-occupancy account**, room built 2018 for two boys aged 7 and 3, with the owner explaining why a bunk bed was rejected for a room that is also the flat's *«лицо квартиры»*. **Longest-horizon wall-bed evidence this vault would hold** |
| **`68vqONqJ_9s` "Цены на кровать-трансформер. Считаем просто"** | **TAKE, with rule 2 handled.** A cost-driver walkthrough — size, shelves/no shelves, manual vs automatic mechanism, then options — with **one figure, 115,000 RUB**. Moscow (two showrooms named), no year stated → `upper_bound_from_publication` |

**What `jZAAwUZVb0I` alone adds, and why it moved to the top:**

1. **⚠️⚠️ A 10-YEAR WARRANTY ON THE FRAME** (welded one-piece steel, rated **600 kg**, no bolts so nothing develops a squeak). **This bears directly on the warranty gap I recorded this morning from `u_gIgDqRdYw` — 20,000 cycles but 3 years.** If frame and mechanism carry *different* warranty terms, the Phase-1-install / Phase-2-activate concern is narrower than the mechanisms page now states, and the question to put to a supplier is sharper: **which component is warranted for how long.** ⚠️ Different vendor's terms, so it refines the QUESTION, not the answer.
2. **⚠️⚠️ ON THE AUTOMATIC MECHANISM, THE CUSHIONS SELF-STOW** — *«сверху подушки и сиденья дивана прячутся под кровать сами»*. **That lands squarely on the four-way retention question the vault just recorded as open** (straps / no straps / elastics on the mattress / elastics on the bedding) — it is a **fifth** option that removes the manual step entirely.
3. **⚠️⚠️ A MATTRESS SPEC THE VAULT DOES NOT HOLD:** *«для наших кроватей нужен СПЕЦИАЛЬНЫЙ матрас, предназначенный для ВЕРТИКАЛЬНОГО ХРАНЕНИЯ»*. **Nothing in `14_Furniture/analysis/Mattress_Construction_And_Selection.md` mentions vertical storage as a mattress requirement** — and this project intends to buy a wall bed, so it is a live purchasing constraint.

---

## ⚠️ 4. The title-skim, by bucket

| Bucket | Count | Verdict |
| :--- | ---: | :--- |
| **⚠️⚠️ Untitled/one-word testimonials and catalogue clips** — `#отзыв покупателя` (×8 identical), `#обзор кровать-трансформер` (×6 identical), `мебель трансформер` (×9 identical), model-name clips (Атлант / Дельфин / Импульс / Веритас / Максимус / Атом / Прайд) | **~75** | **DECLINE, the whole bucket.** These are SEO clips and short testimonials. A title carrying no proposition rarely carries a finding |
| **Project showcases and client reviews** — "наш проект", "рум-тур", "отзыв клиента", kids reacting to their new beds, showroom tour, *how to get to our showroom*, cracking nuts with a bed | **~45** | **DECLINE** — with the two longevity exceptions promoted to Tier 1 below. Post-occupancy accounts are valuable; *delivery-day* testimonials are not |
| **Mechanism / spec / safety explainers** — how to choose, gas lifts, Атлант vs Дельфин, "will it fall by itself?" (×5 near-duplicates), opening without electricity, self-assembly, closing the gaps, ЛДСП vs МДФ, adjustable headboard | **~20** | **SELECTIVE.** The five "will it fall?" videos are one question answered five times — take at most one. **Two genuinely new angles: opening without power, and closing the gaps** |
| **⚠️⚠️ Transformer TABLES and non-bed transformers** — hiding a large table in a 300 mm cabinet, the cantilevered ("безопорный") table, "Тауер" fold-down table, the sliding library | **~6** | **⚠️⚠️ TAKE — this is the empty shelf, and it is the owner's stated interest** |
| **Room planning / ergonomics / storage** — bedroom planning A–Z stage 2 (colour, electrics, furniture), 3 don'ts for narrow rooms, computer chair and desk, closet organisation, where to put documents and wires, decluttering psychology, colour masterclass | **~10** | **DEFER, worth a second look.** Adjacent to existing pages but **off the owner's furniture steer**, and a furniture seller on decluttering is selling |
| **Cost-framing** — price walkthrough, "cheaper to buy another ROOM or this furniture?", affordable transformers, the cheapest Murphy bed, Era-Nova competitor review | **~5** | **SELECTIVE.** ⚠️ **`DTVaEz_t5nk` (another room vs this furniture) is a real framing this vault lacks** — the alternative to a transformer is priced as floor area |
| **Smart home / voice** — opening by Alice (×3) | 3 | **ONE at most**, and pair it with *opening without electricity* — the failure case matters more than the feature |
| **Health / sleep claims** — "a dream that breaks your back", "goodbye orthopedic sofa" | 2 | ⚠️ **DECLINE as health claims**; the sofa one only if it is a construction argument, which the vault already holds better from Краснов and Шеврина |

---

## ⚠️⚠️ 5. Proposed Tier 1 — nine videos, not forty

**Ordered by what they add, and deliberately weighted AWAY from the wall-bed material the vault has 28 files of.**

| # | Video | Why |
| :--- | :--- | :--- |
| 1 | **`jZAAwUZVb0I`** How to choose \| types, mechanisms | **Read. Three new things** (§3). The channel's spine |
| 2 | **`KgBcJ4zAHi8`** After 7 years | **Read. 7-year post-occupancy**, the longest horizon available |
| 3 | **`oT4828iDsSk`** A large table hidden in a 300 mm cabinet | **⚠️⚠️ Murphy TABLE — the empty shelf, and the owner's stated interest** |
| 4 | **`VYmnD-tHevM`** The cantilevered ("безопорный") table | **⚠️⚠️ Murphy table, structural** |
| 5 | **`KgVCayGMspo`** Fold-down table "Тауер" | **⚠️⚠️ Murphy table, a specific product** |
| 6 | **`o6_HwxwZau4`** Opening an automatic bed **without electricity** | **⚠️⚠️ The failure case for every automatic model.** ⚠️ 429'd on spot-check; retry |
| 7 | **`68vqONqJ_9s`** Price walkthrough | **Read. Cost DRIVERS in order**, plus one Moscow figure under rule 2 |
| 8 | **`DTVaEz_t5nk`** Cheaper to buy another room, or this furniture? | **Prices the alternative as floor area** — a framing the vault lacks |
| 9 | **`-TXuqiSuwDU`** What closes the gaps in transformer furniture | **The filler-panel detail behind today's 5 cm ceiling-gap finding** |

**Reserve (take only if Tier 1 yields well):** `3H4xShnLmxc` gas lifts (429'd), `WkVDUlIDCRk` Атлант vs Дельфин, `L4HMNks2Eac` ЛДСП vs МДФ, `3MyjEkab-MU` mattress & bedding against gravity, `eb1UhMz0N9Y` top-5 myths, `SfCu7uxYeZ8` survived time and a house move, `J7Q6Z3fvytQ` five people in a two-room flat.

**Grouping:** the three table videos should go under **one** source note with `covers_also`, as should any two longevity accounts — same convention as today's Качанова group.

---

## ⚠️ 6. What I recommend, plainly

**Take Tier 1's nine. Decline the other 156 unless something changes.**

The channel is **~75% SEO clips and ~27% delivery-day testimonials by count**, and its wall-bed explainers largely restate what 28 existing files already say — from a vendor the vault already cites four times. **The genuine additions are narrow and specific: the transformer TABLES (zero coverage, and the owner asked for them), one 7-year post-occupancy account, the vertical-storage mattress spec, the component-by-component warranty split, and the no-power failure case.**

⚠️ **Every claim from this batch must be attributed to Progress Design BY NAME and must not be counted as independent corroboration of `u_gIgDqRdYw`, `hT4Whu6F2gs`, `4xZ-9vlXV7Y` or `tRv7QSUoqpg`** — all four are this same company, already in the vault. **Where a Tier 1 video agrees with one of those, the note should say "the same maker, restated" in as many words**, exactly as the FREE_DOM correction now does on the mechanisms page.

**Not processed yet — this is a triage, and the fetch quota is currently 429'd.** Say the word and I'll run Tier 1 as a batch.

---

## ⚠️⚠️ 7. STOPPED ON RATE-LIMIT — state as of 2026-09-15, and what the 429s actually mean

**Tier 1 ran to 6 of 9 resolved. The run was stopped deliberately on the owner's instruction, not abandoned.**

| Video | Outcome |
| :--- | :--- |
| `jZAAwUZVb0I` + `68vqONqJ_9s` | **Processed** — grouped source note, spec and cost structure |
| `KgBcJ4zAHi8` | **Processed** — the seven-year owner account |
| `oT4828iDsSk` + `VYmnD-tHevM` | **Processed** — grouped source note, transformer tables |
| `KgVCayGMspo` | **Resolved as `skipped`** — fetched fine, but the video has NO SPEECH (19 bytes, *«[Музыка] ты»*). A silent product clip; no title-skim could have caught it |
| **`o6_HwxwZau4`** | ⏸️ **NOT FETCHED** — opening an automatic bed without power |
| **`DTVaEz_t5nk`** | ⏸️ **NOT FETCHED** — cheaper to buy another room, or this furniture? |
| **`-TXuqiSuwDU`** | ⏸️ **NOT FETCHED** — what closes the gaps in transformer furniture |

### ⚠️⚠️ The 429 is OUR request budget, not a property of any video — and here is the proof

**`KgVCayGMspo` returned HTTP 429 twice and then succeeded on the third attempt**, same video and same URL, with nothing changed but elapsed time. **A per-video defect cannot do that.** The whole day's pattern is the same shape: **roughly two fetches succeed, then everything after returns 429**, and backoffs of 300 / 420 / 600 / 900 s were not enough to clear it. A final single probe on `o6_HwxwZau4` at the end of the session returned 429 again.

> **→ ⚠️⚠️ SO ROTATING TO OTHER VIDEOS OR OTHER CHANNELS WOULD NOT HELP — it is the same IP and the same budget, which is exactly what standing rule 7 warns about ("a rate-limit can be IP-wide across all channels — pause, don't rotate channels into the same wall").** **Probing further only feeds the limiter and delays its reset.**
>
> **→ The correct resumption is a LONG pause — hours, not minutes — and then three fetches, spaced, with the exit code checked directly.** ⚠️ **Not a tighter retry loop.**

### ⚠️ A process defect found and fixed mid-run, recorded because it recurred

**The first fetch loop tested `rc=$?` after piping the fetcher through `tail`, so it read `tail`'s exit status and the rule-7 circuit breaker never fired** — it kept fetching through two 429s. Fixed by capturing the exit code directly from the fetcher with no pipe between, and the breaker then tripped correctly on the very next run. **A second, smaller one: a retry script decided what was outstanding by looking only in `_Inbox/transcripts/`, so once a transcript was archived it read as missing again and the queue was about to re-fetch an already-resolved video into an active block.** Both are the same underlying error — **checking a proxy for the state instead of the state.**

### What this means for the rest of the channel

**Nothing here changes the Tier 2 assessment in §8** — the limiter is about fetch scheduling, not about source value. **But it does mean any further slice of this channel should be run as a small number of fetches spread over a long window, rather than as a batch.**

---

## ⚠️⚠️ 8. TIER 2 — proposed 2026-09-15 after processing Tier 1, including a MISS in this triage

**Processing the first five changed where the value looks like it is. Two revisions, one of them a real error in §5 above.**

### ⚠️⚠️ The miss: children sharing one room is a PHASE 1 question, being built now

**§5 weighted the shortlist around the adults' Phase 2 wall bed and treated children's videos as generic filler. That was wrong on this project's own facts.**
[[05_Kids_Room/Kids_Room_Index|Kids_Room_Index]] records **two children aged 3 and 6 sharing the 15.28 m² room through Phase 1**, with *"shared sleep configuration"* named as a key need, and
[[00_Master/Family_Requirements|Family_Requirements]] §7 says **"install the Murphy bed(s)"** — plural.

> **→ Children sharing one room is not a Phase 2 topic on this project. It is the room being designed NOW.**
>
> **→ And it explains the batch's best result rather than crediting it to judgement: `KgBcJ4zAHi8` yielded so well because it IS this household's Phase 1 seven years on** — a room built in 2018 for two boys aged 7 and 3, two wall beds, a desk with a drawer each. **That video was picked for its longevity angle; its closest match to this project was luck.**

**Tier 2A — children sharing one room (one grouped note):**

| Video | Why |
| :--- | :--- |
| `SKJuZZ8eWcg` | **Two 140×200 beds in one nursery** — the extreme case, two near-doubles in one room |
| `tdpYeoDlCuI` | *«Две детские — два подхода к комфорту»* — two approaches **compared**, rarer than one shown |
| `CRmpl_G2oOQ` | Three children's transformers in one room |
| `onhOzoEZ-gw` | Two boys in one room |

⚠️ **One concrete check already done: the kids' room ceiling is 2.55 m, so the new "ceiling height limits bed LENGTH" finding is NOT binding there** — a 200 cm bed plus the 5 cm erection gap clears it comfortably.

### ⚠️ Tier 2B — longevity, which was the highest-yielding category by a distance

- **`SfCu7uxYeZ8`** — *«ПРОВЕРКА ВРЕМЕНЕМ И ПЕРЕЕЗДОМ ПРОЙДЕНА?»*, time **and a house move**. ⚠⚠ **Probably the ten-year modular-block project that `oT4828iDsSk` signed off trailing** and which was logged there as a follow-up lead. If so it is the longest-horizon evidence available on this furniture type, and it tests the removability finding across a MOVE rather than a renovation.
- **`XL2Dsw7FonM`** — two beds, wardrobes and a play area, family review after several months. Doubles as Tier 2A.

⚠️ **`TUhO7vtFWqA` (one year) and `DKM1U9ZoNcE` (repeat customers) are now DECLINED** — one year adds nothing behind seven.

### Tier 2C — two singles

`J7Q6Z3fvytQ` (five people in a two-room flat; this household is four) and `v-YDS9ZVpcw` (a worked 12 m² room).

### ⚠⚠ And the hard limit, which matters more than the shortlist

**This vault now cites Progress Design EIGHT times. Tier 2 would make it twelve — more entries than any other furniture source in the vault, all from one company selling the product.**

> **→ TIER 2 SHOULD BE THE LAST SLICE.** After it, the channel is exhausted of things only it can say, and the honest next step is a DIFFERENT maker, or owners with no vendor attached. **The `same_vendor_as:` frontmatter field and the "not independent corroboration" line in every note exist to stop this accumulating into false consensus — but past a point the right answer is to stop adding, not to keep labelling.**

⚠️ **And per §7, any Tier 2 run must be a few fetches spread over a long window, not a batch.**
