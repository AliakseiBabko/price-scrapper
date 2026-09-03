# Doors & Trim — Door Swing-Direction Rule

A coherent, safety-grounded rule set from a single source, internally consistent across 5 distinct reasons. `single-account` — not yet independently corroborated by another source in this knowledge base. Part of [[13_Surfaces_and_Finishes/Doors_and_Trim|Doors & Trim]]. [source: `_Archive/processed_sources/20260731_zems_b207_design_b8b72802.txt`]

- Zemstandart/Alexey Zemskov recommends: **Living-space doors (bedroom, living room, study, kids' room, kitchen, library) should open INWARD**, for: safety (fewer people pass through the room itself versus the shared corridor), light-switch ergonomics (handle and switch on the same inside wall — push-to-enter keeps orientation consistent in the dark), open-position convenience (an inward door parks against an interior wall rather than blocking an often-only-~1m-wide corridor), floor-stopper placement (inside the room rather than a corridor trip hazard), and closing convenience (reachable from the corridor).
- Zemstandart/Alexey Zemskov recommends: **WC/bathroom doors (and small utility rooms/closets) should open OUTWARD**, for space (bathrooms typically have less interior floor area than the corridor) and — the **safety-critical reason** — so that an incapacitated occupant collapsed against the door from inside can still be reached, rather than the door being blocked shut by their own body.
- Zemstandart/Alexey Zemskov says: **Quick heuristic**: a room whose light switch is inside the room gets an inward-opening door; a room whose switch is outside the room gets an outward-opening door.
- The source states fewer than 1% of his own projects use an inward-opening WC door, for unexplained edge-case reasons — treated as a rare exception, not evidence against the rule.
- **⚠️ A documented, reasoned instance of exactly this exception, with the mechanism explained**: when a WC/bathroom door opens directly onto a high-traffic junction corridor (multiple rooms' traffic converging at that exact point), the safety math can flip. Striking someone walking through that main corridor unexpectedly (a stranger to the swing, unable to anticipate it) was judged a bigger risk than striking someone already inside/entering the bathroom itself (aware of the door, moving deliberately) — so the door was deliberately built to open inward. **Weigh this against the standard outward-swing safety rationale (reaching an incapacitated occupant) on a case-by-case basis when a WC sits at a genuine traffic junction** — this doesn't overturn the default, but it's the first documented case in this store of the <1% exception actually being explained. `single-account`, `unverified`. [source: [[_Sources/YT_jrqEbkU4Wj8_developer_worse_than_designer_257|YT_jrqEbkU4Wj8]]]

Zemstandart/Alexey Zemskov says: **A related switch-hand nuance (same channel)**: an entry door should swing toward the side where the switch is reachable, so a person entering can close the door with one hand while the other hand naturally reaches the switch — a door swinging away from the switch side was called out as a specific, avoidable design mistake on a real site. `unverified`, `single-account`.

See [[13_Surfaces_and_Finishes/analysis/Rough_Opening_and_Casing_Sizing|Rough-Opening & Casing Sizing]] for the frame-level installation-plane-offset detail that implements this same safety logic at the physical-construction level.

## Diagnostic: No Valid Swing Direction Means Relocate the Opening (added 2026-08-19, remainder-pool batch)

Zemstandart/Alexey Zemskov and the cited corroborating source say: **If a door opening's position (e.g. on a diagonal corner, or hemmed in by fixtures on multiple sides) leaves the door leaf conflicting with something in every possible swing direction, the fix is almost always relocating the opening itself, not compromising on a "least-bad" swing.** Documented case: a bathroom door as originally positioned by the developer would have conflicted with the kitchen entrance, the bedroom exit, the sink, or the towel warmer depending on which way it swung — every option failed until the opening itself was moved to a wall section clear of all four conflicts. `single-account`, `unverified`. [source: [[_Sources/YT_v7UXJ5fJ0H0_worst_apartment_2019_replan_520|YT_v7UXJ5fJ0H0]]]

## Approach Direction, Not Just Room Geometry (Мария Шеврина / SMBUREAU, added 2026-08-30)

She names door swing alongside a short basin spout as her "top two favourite mistakes," and the specific insight is about *which side you actually arrive from*:

**⚠️ Work out the direction the door is most often approached from — which for a guest WC, a utility/laundry block or a wardrobe is usually *not* the entrance hall.** It is the kitchen or the living room. The handle should fall on the line of travel, rather than forcing you to take two extra steps, grab the handle, step aside to clear the swinging leaf, and only then walk in. "Очень часто есть какие-то помещения… вы будете заходить в эти помещения не со входной двери."

**Her method: rehearse the usage scenarios on the plan** — and decide the light-switch position in the same pass, since it is the same walking line.

`single-account`, `unverified`. [source: [[_Sources/YT_avRNMkNdOBs_shevrina_top7_renovation_mistakes|YT_avRNMkNdOBs]]]

## Swing Direction Decides Where the Switches Can Go (added 2026-08-31)

**⚠️ A door opening inward covers the wall where switches would otherwise sit.** She gives a worked case where inward opening would have made their chosen switch position impossible, forcing it onto the wall opposite — survivable there, but **the worst case is a door that blocks the only wall available for switches**, which happens where one side is a real wall and the other is the end panel of a non-built-in wardrobe. Mounting switches on a wardrobe end panel is possible but the electrician will not thank you for the cable run.

**Practical consequence: decide swing direction and switch position together, on the plan** — the same pairing she recommends when working out approach direction (section above).

[source: [[_Sources/YT_TUVsZ1Xx1aQ_shevrina_bad_renovation_decisions|YT_TUVsZ1Xx1aQ]]]

## Floor-to-Ceiling Doors, and the Transom Workaround (added 2026-08-31)

**⚠️ In architectural minimalism, floor-to-ceiling doors are the preferred option regardless of finish** — concealed, painted to the wall, or with architraves.

**⚠️ Where the openings cannot be full height *and* the doors take a finish different from the walls, add a matching transom panel ("антресолька") above the door** — orderable in the same finish as the leaf. It raises the opening visually and harmonises the doors with any adjacent full-height element. Her worked case: a hallway where slats, mirror and one sliding door all run to the ceiling while the hinged doors stop short, leaving the doors looking truncated.

This is the door-specific version of the rule already on [[01_Entrance/analysis/Storage|Entrance Storage]] for the entrance door — **a contrasting finish must reach the ceiling, or it reads as a patch on the wall.**

[source: [[_Sources/YT_p5lXLETWI5s_shevrina_subscriber_critique_minimalism|YT_p5lXLETWI5s]]]


## Swing Direction Also Decides Where the Flooring Joint Can Go (added 2026-08-31)

**Where a flooring transition falls in a doorway, the joint must sit under the door leaf** so it is hidden when the door is closed — which makes the swing direction an input to the *floor* programme, not only to the wall and switch layout. Interior designer Надежда Кузина flags it as an obvious rule that people nonetheless get wrong, because the joint is usually made by a different trade at a different time from the door.

**Practical consequence**: the swing decision has to be locked before the screed is set, not before the door is hung — the transition's position, the screed heights either side of it, and the leaf position are one coupled decision. Full four-method transition comparison on [[13_Surfaces_and_Finishes/analysis/Flooring_Installation_and_Baseboards|Flooring Installation, Transitions & Baseboards]]. [source: [[_Sources/YT_g252JnMcc3Q_kuzina_flooring_transition_methods|YT_g252JnMcc3Q]]]

## ⚠️⚠️ The Full Swing-Clash Cluster, from Clients at 3-10 Years' Occupancy (NSDSGN, 2022-09-20)

**Five distinct clashes, reported by clients living in his interiors rather than predicted — and his framing is the reason they belong together: «за открыванием дверей нужно очень внимательно следить, иначе могут появиться очень глупые, очень грубые ошибки, которые постоянно будут вас раздражать. Такие ошибки очень часто НЕЗАМЕТНЫ СРАЗУ и могут всплыть только уже во время жизни в квартире.»** It applies to interior doors **and furniture doors equally**, which is what makes it a coordination problem rather than a joinery one. [source: [[_Sources/YT_CSpXvPWpsgQ_nsdsgn_fifteen_post_occupancy_regrets|YT_CSpXvPWpsgQ]]]

1. **A socket or switch behind a habitually open door is unusable**, and the same-axis case where a sharply opened leaf strikes the switch and turns the light on. Full detail, including the changed-swing change-control rule, on [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Electrical: Key Concepts and Planning]].
2. **⚠️ A cabinet against a wall whose door opens, but whose internal DRAWER then cannot come out — and he attributes the fault correctly rather than to the designer: «это скорее косяк не дизайнера, а МЕБЕЛЬЩИКА, который делает проект уже по РЕАЛЬНЫМ РАЗМЕРАМ и рассчитывает все открывания». «Я очень много раз видел такой косяк.»** **⚠️ And the three named obstructions are the useful part, because two of them are not furniture at all: the drawer can foul the cabinet's own door leaf, a RADIATOR, or a WINDOWSILL.** So the check has to be run against the heating and window drawings, not only the furniture plan.
3. **⚠️ A kitchen or wardrobe run that meets a CONTINUING wall rather than sitting in a niche — the end door cannot open. «Очень часто этот момент происходит с ХОЛОДИЛЬНИКОМ», which usually stands against a wall.** **The timing is what makes it expensive: «проблемы, когда холодильник уже привезут и кухня будет собрана».** Both the appliance and the joinery are finished and paid for before anyone finds out.
4. **⚠️ Handle and light switch on OPPOSITE sides of the opening** — «самая глупая ситуация», and he lived in such a flat: «это каждый раз меня бесило». Unfixable in practice — «заново штробить стены переделывать скорее всего вы не будете, но вы будете каждый раз мучиться».
5. Any electrics or furniture immediately adjacent to a leaf's arc.

**⚠️ THE PROCESS RULE, which is the transferable output: «все эти вопросы нужно решать на стадии ДИЗАЙН-ПРОЕКТА либо на стадии ПРОЕКТИРОВАНИЯ МЕБЕЛИ. Если вся мебель уже собрана, дверь установлена — тогда уже что-то решать будет очень НЕРВНО, ДОЛГО И ДОРОГО, и конечно же нужно будет понять, КТО НАКОСЯЧИЛ.»** **→ Note the last clause: a swing clash is also a liability dispute, which is one of this practitioner's stated reasons for producing a design project at all — see [[11_Budget_and_Planning/analysis/Design_Services_and_Fees|Design Services and Fees]].** «Постарайтесь все эти ошибки исправлять ещё НА БУМАГЕ.»
