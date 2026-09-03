# Plumbing — Leak-Protection Systems

Covers the three-part leak-protection architecture, sensor placement, wired-vs-wireless choice, and sizing the kit count. Part of [[12_Engineering_and_Systems/Plumbing_and_Waterproofing|Plumbing & Waterproofing]].

## Architecture, Sensor Placement, and Sizing the Kit Count

- LAB-REMONT, Знакомые сантехники, and Zemstandart/Alexey Zemskov describe: **Three-part architecture, corroborated across 3 sources**: (1) an electrically/motor-actuated shutoff valve (mechanically similar to a manual ball valve, but servo-driven), installed right after the main shutoff valve; (2) a control/logic module that the sensors report to and that signals the valve; (3) a battery backup in the module so it can still trigger a shutoff during a power outage — for a limited time, hence the separate recommendation to add a proper UPS for longer coverage. Named brands (commercial mentions, not vetted comparisons): Гидролок (Gidrolock), Аквасторож (Aquastorozh), Нептун (Neptun); one source's own installed system is branded "NPT."
- Zemstandart/Alexey Zemskov specifies: **Sharper sequencing rule, independently added (2026-08-18)**: the shutoff valve must be the *very first* component after the main/riser shutoff — before any other fitting, including a coarse pre-filter. Anything placed upstream of the leak-protection valve (a filter housing, a fitting, a hose) stays an unprotected leak point regardless of the sensor system's presence downstream. [source: [[_Sources/YT_scOLgA4HPqM_7_key_lifehacks_099|extraction note]]]
- Zemstandart/Alexey Zemskov reports: **Stated response time on at least one product line**: valve closes within 5 seconds of a sensor detecting water.
- **Sensor placement doctrine**: a floor-mounted sensor at the lowest point of each wet zone (installed like a recessed electrical outlet box, core-drilled so water pools onto it), plus dedicated sensors under bathtubs, under the washing machine/dryer, and under sinks. **Pair this with building the bathroom floor a few centimeters lower than the rest of the apartment** where practical — this makes leaked water reliably pool at the sensor rather than spreading, and the sensor itself typically triggers at only 1-2mm of standing water depth. [source: [[_Archive/processed_sources/20260731_zems_b069_protection_24920eb6.txt|20260731_zems_b069_prote]]]
- **A real practical annoyance and its fix**: stepping on the floor sensor with wet feet (e.g., during a rushed morning routine) triggers the same full shutoff as an actual leak, cutting water to the entire apartment until manually reset. The fix doesn't require removing or replacing the sensor — simply dry the sensor's contacts (a hair dryer works) and it resets normally. Worth knowing before the first false trigger causes alarm. [source: [[_Archive/processed_sources/20260731_zems_b069_protection_24920eb6.txt|20260731_zems_b069_prote]]]
- Zemstandart/Alexey Zemskov and LAB-REMONT recommend: **Wired sensors are better than wireless on every relevant metric — use wireless only when running wire genuinely isn't possible**, and treat it as a real compromise even then (a wireless sensor's battery can fail at the worst possible moment, with no way to know in advance). Default to wired.
- Zemstandart/Alexey Zemskov explains: **The leak-protection control unit ("brain") must be mounted behind a plastic panel/door, not inside a metal manifold cabinet** — radio signal can't penetrate a metal door, silently disabling the whole system even though every sensor and the shutoff valve are still physically fine. A checkable installation detail worth verifying regardless of which sensor architecture is used, since the control unit's own uplink to a monitoring app is commonly wireless even on an otherwise wired-sensor system. `single-account`. [source: `_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]
- **Buy one full leak-sensor kit per riser pair (hot+cold), not per apartment** — if an apartment has two physically separate riser locations (e.g., two bathrooms on different risers), each needs its own kit, roughly doubling the cost. A workaround from one source's own apartment: consolidate both stub-outs to a single collector point and run pipe overhead (through the ceiling) to the second bathroom/kitchen from there, avoiding the need for a second kit — a real cost/complexity tradeoff, not a free win. [source: [[_Archive/processed_sources/20260731_zems_b069_protection_24920eb6.txt|20260731_zems_b069_prote]]]
- **A water-based (hydronic) towel warmer, if installed, typically sits downstream of the leak-protection system's shutoff valve and isn't covered by it** — see [[12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer|Hygienic Shower & Towel Warmer]] for why this specifically pushes toward choosing an electric towel warmer instead, or budgeting for a second dedicated leak-protection branch. [source: [[_Archive/processed_sources/20260731_zems_b174_wildbath_4e5e4ea1.txt|20260731_zems_b174_wildb]]]
- **⚠️ Heating-fixture-type placement nuance, added 2026-08-24**: a wireless leak-sensor tag works well specifically with an **in-floor convector** (the tag sits inside the convector housing, physically undisturbed), but is impractical with **exposed surface-mounted radiators** (horizontal or vertical) — a loose sensor puck near a surface radiator gets knocked around by pets or a robot vacuum, becoming a persistent annoyance rather than a benefit. **Recommendation: skip a leak-protection system entirely if the apartment uses only surface-mounted radiators and the installation was properly pressure-tested with quality fittings** — the source frames the sensor as more nuisance than benefit in that specific configuration. Konstantin Kruglov / Ontario. [source: [[_Sources/YT_Q1KSHFhLzJo_kruglov_heating_secrets|Q1KSHFhLzJo]]]
- LAB-REMONT and Знакомые сантехники report: **Cost**: 16,000–60,000 RUB for a full kit depending on functionality (one 2025 source); 20,000–45,000 RUB cited by a different 2024 source for a comparable system — broadly consistent given the one-year gap and different regions/vendors.
- Konstantin Kruglov/Ontario, real Moscow jobsite, cites a **starting price of "от 25,000 RUB"** for a leak-protection system (2023-12-08). **USD normalization**: trailing 6-month USD/RUB average (92.66 RUB/USD) before the confirmed publish date → 25,000 RUB ≈ **$270** (rounded to the nearest $10). Broadly consistent with the two cost ranges above, sitting near their lower end. [source: [[_Sources/YT_QcYJwQgu67g_kruglov_perfect_plumbing_mistakes|QcYJwQgu67g_kruglov_perfect_plumbing_mistakes]]]
- Common failure scenarios cited as the reason to install one at all: a temporary/cheap mixer connection cracking after finish work and being forgotten; a sink siphon's corrugated hose slowly sliding off its fitting; a flexible supply hose reaching the end of its finite service life and bursting; a pet nudging a lever-style mixer or drain-stopper open while the flat is unoccupied, flooding a stoppered sink or tub.
- Konstantin Kruglov / Ontario describes the automatic shutoff valve's **reset workflow precisely**: sensor detects water → signal to the control module → module signals the valve closed. To reopen, the user presses a reset button; the module first re-checks whether its sensors are still wet, and only sends the "open" signal if they now read dry — it does not reopen on a blind timer or button press alone. [source: [[_Sources/YT_4jAQ526Zy2w_kruglov_perfect_manifold_unit|4jAQ526Zy2w_kruglov_perfect_manifold_unit]]]
- Petrishin-Stroy, real damage case study on a previously-renovated
apartment: **a hidden-leak-travel mechanism specific to developer-
installed corrugated conduit ("гофра")** — developer pipe is typically
routed inside a corrugated sleeve, so a failed joint or fitting inside
that conduit lets water travel *inside the conduit itself* before
finding an exit point at a joint between two conduit sections. The
visible stain (e.g., in a kitchen or kids' room) can therefore be
physically far from the actual failed fitting (e.g., in a corridor),
making the leak hard to localize without opening not just the screed but
the finish flooring too — a genuinely new diagnostic caution, distinct
from the tee-joint/radial-vs-tee mechanism already on this page.
Separately, the same source gives a **concrete first diagnostic-
elimination step**: an unexplained water stain's timing can rule out an
air-conditioner condensate-drain leak specifically — condensate only
forms while the AC unit is actively running, so a leak appearing outside
cooling season (e.g., December) points to a plumbing/heating source
instead. (added 2026-08-24, Round 7) [source: [[_Sources/YT_YxXfsKoyx6M_petrishin_flood_prevention_heating|YxXfsKoyx6M]]]

Konstantin Kruglov / Ontario gives an explicit **sensor-placement priority order** (with the typical 3-sensor kit): **#1, mandatory** — inside the plumbing distribution/collector cabinet itself, since that location is concealed (a leak there wouldn't be noticed quickly) and concentrates the largest number of fitting connections that could fail. **#2, recommended** — under the kitchen sink and under the bathtub (the source recommends both, calling the choice "up to you" if only one sensor is left). **#3, a flexible/portable use, framed as a budget-friendly "vacation mode"**: keep a spare sensor (wired or wireless) to place in the center of the bathroom floor specifically when leaving for a short trip (1-2 days or a vacation), instead of shutting off the whole system — pick it back up on return. **UPS mechanism, stated more precisely than before**: a battery-backed UPS is recommended specifically because the system's electrically-actuated shutoff valves stop working on a power outage; the UPS's role is converting AC to DC so the system keeps running off battery during the outage — refines this page's existing "battery backup in the module, limited time, add a UPS for longer coverage" note rather than contradicting it. `single-account`, `unverified`. [source: [[_Sources/YT_sd2XYBZY-K8_kruglov_bathroom_2026_top10|YT_sd2XYBZY-K8]]]

- Vladimir Amelchenko / ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (added 2026-08-28, Round 2) independently corroborates the ≈25,000 RUB starting cost above (≈$270 at a comparable trailing-6-month rate) with a **floors-below flood-cost framing**: aggregate damage to 5-12 apartments below in a multi-story building can reach "several million RUB" — a single stated exception for ground-floor units (no apartment below, though the owner's own unit still floods regardless). [source: [[_Sources/YT_Zl_fegEg7yY_sbk_water_supply_manifold_install|YT_Zl_fegEg7yY]]]

## ⚠️ Detection Is Not Shutoff — the Timing Window, and Why a Threshold Still Matters (Надежда Кузина, added 2026-09-01)

**The most consequential single item routed in Round 5, and it corrects a reasoning error that leak sensors invite.** [source: [[_Sources/YT_UnCjxyDtWG0_kuzina_tiktok_lifehacks_debunked|UnCjxyDtWG0]]]

She endorses the devices — *"мы практически в каждый проект ставим датчики от протечек"* — **and then reads the manufacturer's own published figures on camera:**

| Stage | Time (Gidrolock's published figures) |
| :--- | :--- |
| **Sensor detects the leak** | **2 seconds** |
| **Signal reaches the system and the valve actually closes** | **a further 15–20 seconds** |
| **The same closing stage, other suppliers** | **up to 40 seconds** |

**⚠️ The argument: "за 2 секунды мою квартиру не успеет затопить" is true and beside the point, because the 2 seconds is DETECTION only.**

> **⚠️ With a bathroom threshold, all the water released during the 15–40 second closing window is contained in the bathroom. Without one, it spreads freely through the flat.**
>
> **This is an engineering argument for a threshold rather than a regulatory one, so it survives being moved to another jurisdiction** — which the Russian norm on the same subject does not. See [[07_Bathroom/analysis/Planning_and_Layout|Bathroom Planning & Layout]] for the regulatory side, flagged there as Russian.

**⚠️ Verify before relying on it**: the figures are from a 2022 reading of one supplier's site. **Re-check the current specification of whatever unit is actually specified** — the *structure* of the argument (detect, then transmit, then close) holds regardless, but the numbers will have moved.

**A related point from a second source in the same round**: **smart sensors that notify your phone while you are out are "гораздо безопаснее, чем не иметь датчик от протечек или чем иметь обычный датчик."** The notification matters precisely because the shutoff is not instantaneous and the aftermath is not self-managing. [source: [[_Sources/YT_JOBm37_9iDg_kuzina_practical_vs_good_interior|JOBm37]]]

## ⚠️ Two First-Hand Accounts — One Save, and False Triggering as the Real Failure Mode (NSDSGN, 2023 and 2022)

**This page has held the case FOR these systems. These two accounts supply a save that actually happened, and the failure mode that makes people disable them.**

### The save — and the mistake that caused the leak

**A designer's own flat, two days before filming.** A washing-machine hose on the kitchen had been badly hand-tightened without a spanner. **He had RAISED the system pressure on a friend's advice because he felt he lacked it.** The hose loosened, began to seep, then let go. **Within a few minutes the sensors shut the water off. He wiped it, the valves reopened, everything resumed.** «Если бы меня не было дома — мою квартиру от затопления. Это прямо крутая штука, я её ощутил прямо в действии.»

**⚠️ The causal chain is the lesson, and he supplies both halves without joining them: raising system pressure to fix a flow complaint transfers stress onto the weakest connection in the flat.** See [[12_Engineering_and_Systems/analysis/Pressure_and_Water_Hammer|Pressure and Water Hammer]] for the 3.5 bar ceiling from the same source. [source: [[_Sources/YT_Z0brwxSe7gQ_nsdsgn_engineering_systems_site_review|YT_Z0brwxSe7gQ]]]

From the same practitioner: he has had clients **flood ten floors down**, so the loss being insured against is not the flat's own floor. **Automation can be added so a notification reaches the phone.**

### ⚠️ False triggering — two independent accounts, and the wireless variety is implicated

**This is what the page was missing, and it is the reason a system gets disabled rather than repaired.**

1. **A subscriber's system triggers constantly, somewhere under the WC.** His diagnosis: **«что-то у них неправильно сделано, надо настроить чувствительность»**, or water is reaching it from above. [source: [[_Sources/YT_Z0brwxSe7gQ_nsdsgn_engineering_systems_site_review|YT_Z0brwxSe7gQ]]]
2. **⚠️ And a specific product warning from a second video: several clients bought AliExpress Bluetooth WIRELESS sensors — no wires, just dropped under the bath. They worked, until one began glitching badly and shutting the water off constantly: «чуть-чуть поднялась влажность воздуха, ты принял душ, и датчик это обнаруживает и перекрывает воду. И с ним ничего не сделать — единственный способ отключить было запихнуть его в коробку с рисом, чтобы рис впитал всю влагу.»** «Будьте очень аккуратны со всякими вот этими ноу-хау с AliExpress.» [source: [[_Sources/YT_2vyIWKmrSXM_nsdsgn_twenty_post_occupancy_regrets|YT_2vyIWKmrSXM]]]

**→ Two consequences worth specifying against.** **(a) Sensitivity and placement are commissioning decisions, not install-and-forget** — a sensor sited where bathroom humidity, or water from the flat above, can reach it will cry wolf until somebody disables it, which removes the protection entirely. **(b) The humidity-sensitive wireless sensor is the documented failure case**, while both accounts of a system that actually worked describe wired sensors at defined wet points.

## ⚠️⚠️ A Four-Incident Personal Count, and the Failure Mode Nobody Plans For

**The same designer, 2026, now reporting a running total rather than a single save** — which is the closest thing this page has to a frequency figure. [source: [[_Sources/YT_WCoqOCofPx4_nsdsgn_durable_interior_ten_rules|YT_WCoqOCofPx4]]]

- **«То, на чём точно нельзя экономить — это система от протечек. Мне она РАЗА ЧЕТЫРЕ спасла ремонт. И ладно мой ремонт — она ещё спасла моих СОСЕДЕЙ.»** ⚠️ **Note that at least one and possibly two of those four are already recorded on this vault from his earlier videos** (the pressure-raising leak on [[12_Engineering_and_Systems/analysis/Pressure_and_Water_Hammer|Pressure and Water Hammer]]), so the four are a personal tally over years, not four independent incidents this vault can verify. `single-account`.
- **⚠️ THE INCIDENT THAT IS GENUINELY NEW, and it is a component nobody treats as a leak risk: «один раз у нас СКАКНУЛО ДАВЛЕНИЕ в доме, и у меня просто ПОТЁК ФИЛЬТР ГРУБОЙ ОЧИСТКИ. Просто потёк, и соседей стало заливать. Но так как у меня был датчик протечек, он моментально перекрыл воду и ничего страшного не произошло.»**
  **→ Two things follow. (1) A coarse-strainer body is a candidate leak point under a mains-side pressure spike — so it needs a sensor within reach of it, which the usual "under the bath, under the sink, behind the WC" checklist may not cover if the filter sits in a riser cupboard. (2) The triggering event was OUTSIDE the flat's control, which defeats the "my installation is careful, so I don't need this" argument entirely.**
- **⚠️ Where he rates it most necessary: «особенно если вы СДАЁТЕ квартиру, если дом НОВЫЙ и есть какие-то моменты эксплуатации, которые только появляются».** A let flat (nobody present to notice) and a new building (teething failures still surfacing) — both are exposure arguments rather than installation-quality ones.
- **His verdict: «Ставьте и не думайте. Эти датчики ОКУПЯТСЯ ПРИ ПЕРВОЙ ЖЕ АВАРИИ.»**

> [!IMPORTANT]
> **⚠️ And the ranking he attaches to it elsewhere in the same source, which is the strongest argument on this page: «надо помнить, что самые РАЗРУШИТЕЛЬНЫЕ последствия для интерьера происходят НЕ из-за животных, о которых постоянно говорят, НЕ из-за детей, которые рисуют на стенах, — а из-за АВАРИЙ. Особенно если эта авария происходит, когда вы находитесь далеко где-нибудь в отпуске или в командировке.»**
>
> **He says this at the end of a ten-rule durability framework in which most of the rules are about wear from pets, children and cleaning — and then ranks a plumbing incident above all of them.** That is a budget-priority statement, not just a recommendation: **the leak system is the first durability purchase, ahead of any material upgrade.** Full framework on [[17_Design_and_Ergonomics/analysis/Material_and_Finish_Technique|Material and Finish Technique]] and [[17_Design_and_Ergonomics/analysis/Practitioner_Material_Selection_Accounts|Practitioner Material Selection Accounts]].
>
> It also converges with this page's own master-switch dissent, recorded on [[12_Engineering_and_Systems/analysis/Switches_and_Controls|Switches and Controls]]: asked which master function is worth buying, the same practitioner said **water, not electricity** — «тут хватит и пары часов отсутствия, чтобы произошло что-то очень страшное».

## ⚠️⚠️ The Installation That Produced Those Saves — Itemised, With a Sensor Count

**Round 5 found the source that specifies the system behind the four-save tally above and the fifth save below. This page had principles, false-triggering accounts and a personal count; this is the actual hardware layout.** [source: [[_Sources/YT__nDCLhRUojE_nsdsgn_own_bathroom_4m2|YT__nDCLhRUojE]]]

In a service cupboard above the WC, alongside the manifold block:

- **⚠️ «Здесь ДВА НЕПТУНА на ХОЛОДНУЮ [и] ГОРЯЧУЮ воду, от которых расходятся ДАТЧИКИ по квартире: ДВА НА КУХНЕ и ОДИН ПОД ВАННОЙ. Как только что-то происходит, они СРАЗУ ПЕРЕКРЫВАЮТ ВОДУ, и протечка тут же заканчивается.»** Plus a controller — **«мозг, который втыкается в розетку»**.
- **→ Named brand (Neptun), TWO valve units (one per supply, hot and cold, rather than one unit on a common feed), THREE sensors, and one mains-powered controller — so the socket is a rough-stage requirement, which this vault's socket checklists do already carry.**
- **⚠️ The sensor placement is worth noting against the four incidents this system caught: two of the three sensors are in the KITCHEN, and the one that caught the epoxy-grout leak below is the single sensor UNDER THE BATH. A 3 m² bathroom with a boxed-in bath got one sensor and it was enough — but only because the box it was in was the place the water went.**
- **⚠️ It also demonstrates the two-unit configuration is what makes the "коэффициент" arguments moot: with a valve on each supply, either line can be isolated independently — relevant to the false-triggering problem above, where a spurious trip on one line need not cut all water.** `single-account`.

### ⚠️ The fifth save — and it is the only one caused by a defect in the specification rather than a component failure

- **The tile-to-bath joint in that bathroom was grouted with EPOXY GROUT instead of sealant. An acrylic bath flexes when filled, the rigid grout tore away, and water began seeping into the under-bath box during showers.** He deferred it. **«В итоге однажды у меня СРАБОТАЛ ДАТЧИК ПРОТЕЧЕК. Я залез под ванну и увидел там ЛУЖУ ВОДЫ, которая перелила через ванну.»**
- **→ Note what class of failure this is. The other four saves are a component letting go — a strainer under a pressure spike, a hose loosening. This one is a BUILD ERROR that produced a slow, sub-threshold leak into a concealed void, exactly the profile that goes undetected for months. It is the strongest case on this page for a sensor inside every enclosed wet void, and not only at the obvious fixtures.** Full mechanism on [[07_Bathroom/analysis/Bathtub_Materials_and_Installation|Bathtub Materials and Installation]].

### ⚠️ And the passive equivalent of a sensor, for a free-standing bath

**A cheap detail this vault did not hold, from the same practitioner in 2022** (`CN-Ab_g4CAI`): a free-standing bath will usually sit on a podium to shed water, and —

- **⚠️ «СДЕЛАЙТЕ В ЭТОМ ПОДИУМЕ ОБЯЗАТЕЛЬНО ТРАП, на случай если у вас прольётся вода, чтобы она УШЛА В ТРАП и вы ИЗБЕЖАЛИ ЗАТОПЛЕНИЯ. Это может быть очень важно и СПАСЁТ ВАС ОТ СЕРЬЁЗНЫХ ПРОБЛЕМ.»**
- **→ A floor drain inside the podium is a passive, unpowered, unfailing version of what the sensors above do actively — it cannot false-trigger and it needs no socket. It only helps where water can reach it, so it complements rather than replaces a sensor, but for a plinth-mounted bath it is close to free at rough stage and impossible afterwards.** See [[07_Bathroom/analysis/Shower_Enclosures_and_Drainage|Shower Enclosures and Drainage]]. [source: [[_Sources/YT_CN-Ab_g4CAI_nsdsgn_thirtyfive_beautiful_but_impractical|YT_CN-Ab_g4CAI]]]

### ⚠️⚠️ A Further Save, a THIRD Distinct Failure Mode — and All Three Were Invisible (Александр Синчуков, his own kitchen, 2023-11-02)

**«Одна СУПЕР ВАЖНАЯ вещь — это ДАТЧИК ОТ ПРОТЕЧЕК. Он мне ОДИН РАЗ ПОМОГ: сантехники ПЛОХО ПРИКРУТИЛИ СЛИВ-ПЕРЕЛИВ МОЙКИ, и когда я решил побольше воды набрать [в] мойку и она стала ПЕРЕЛИВАТЬСЯ, она ПОЛИЛАСЬ НА КУХНЮ. Я ЭТОГО НЕ ЗАМЕТИЛ — у меня был ЗАКРЫТ ЯЩИК — но тут же СРАБОТАЛ ДАТЧИК.»**

- ⚠️⚠️ **→ THE COMMONALITY IS THE ARGUMENT, NOT THE INDIVIDUAL CASES. Across this channel's saves the vault now has THREE DISTINCT MECHANISMS — a strainer under a pressure spike, epoxy grout at a flexing bath rim, and a loose waste/overflow fitting — AND ALL THREE WERE INVISIBLE UNTIL THE SENSOR SOUNDED.** Two of the three were behind a closed cabinet door.
- → **That is a better case for the sensors than any single dramatic flood, and it also identifies where they belong: not "near water", but UNDER EVERY CLOSED ENCLOSURE CONTAINING A JOINT.** The enclosure is what defeats detection by eye.
- **⚠️ A SENSOR-COUNT DISCREPANCY, RECORDED RATHER THAN AVERAGED.** Here he names **FOUR locations** — under the bath, under the mixer, under the sink, and one **under the washing machine.** The itemised account in the section above (March 2024) gives **2 valve units and 3 sensors.** **Either the system grew between November 2023 and March 2024, or one of the two accounts is loose. Both are recorded with their dates; neither is corrected against the other.**
- Also in this kitchen: **a two-lever mixer with a separate tap for filtered water, filter under the sink.** *(By July 2024 the whole mixer had been replaced with a pull-out — see [[07_Bathroom/analysis/Fixtures_Mixers_and_Sinks|Fixtures, Mixers and Sinks]] for why.)*

[source: [[_Sources/YT_AEJlxbTmQJU_nsdsgn_own_kitchen_review|YT_AEJlxbTmQJU]]]

