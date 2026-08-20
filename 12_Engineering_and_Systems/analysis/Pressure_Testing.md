# Plumbing — Pressure Testing (Опрессовка)

Verifying rough plumbing before closing walls — arguably the single highest-stakes QA step in the whole rough-in process, since a missed leak found later means removing screed and opening walls. Part of [[12_Engineering_and_Systems/Plumbing_and_Waterproofing|Plumbing & Waterproofing]].

## Two Verification Stages, Not One

Zemstandart / Alexey Zemskov says: 1. **Basic check at normal working pressure** (~3 atm, ordinary everyday system pressure) — cap all outlets, apply the system's normal supply pressure. This only catches gross assembly errors (an uncrimped fitting collar, an unscrewed cap) — **don't expect it to catch anything subtler**.
Zemstandart / Alexey Zemskov says: 2. **Real verification = pressure testing at deliberate overpressure**, using a hydrostatic test pump. Code technically requires only 1.5× working pressure (~4.5 atm), but that's stated to often be insufficient to reveal micro-cracks or marginal joints in practice — **test to 10 atm for a real check**.

> [!NOTE]
> **Independently corroborated (added 2026-08-18)**: a second, unrelated source gives the same staged protocol — pressurize to 2 atm, then 5, then 10, hold ~10 minutes, and confirm the drop is ≤0.5 atm — matching this page's own ramp-and-hold procedure almost exactly (the only difference is the very first stage, 2 atm here vs. 3 atm below, not materially significant). Two independent sources converging on the same numbers is a real vote of confidence in this protocol specifically. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_zLJtkP6ymrg_15_diy_plumbing_mistakes_700|extraction note]]]

## Tooling

attribution: unconfirmed — the tooling paragraph has no cited extraction note with a decisive channel field: a pressure-test pump ("опрессовщик"), manual or electric, both typically rated to 40 atm. Manual is preferred for apartment/house work (more portable); electric is mainly for industrial use. A basic consumer manual pump costs from ~1,000 RUB; a professional-grade unit can often be rented for ~500 RUB/day in a major city — no need to buy one for a single job.

## Procedure

1. Fill the entire system: cap all outlets, open water at the collector, then briefly uncap and immediately recap each outlet in turn as water reaches it, to bleed trapped air.
2. Connect the test pump to any outlet, fill its own reservoir, and close off that branch from the rest of the building's supply (so pumped pressure doesn't just bleed back into the main system).
3. Ramp pressure in stages: 3 atm → 5 atm → 10 atm.

Zemstandart / Alexey Zemskov says **two efficiency lifehacks, no quality tradeoff**: (1) **test a whole branch (all cold, or all hot) in one pump-up**, not fixture-by-fixture — cap every outlet on that branch, open every collector valve for it, and pressurize once. (2) **Test hot and cold circuits together in a single pressurization** by temporarily bridging them with a small jumper fitting at any one outlet, creating one closed loop — saves at least ~30 minutes versus testing the two circuits separately.

## Holding and Reading the Result

Zemstandart / Alexey Zemskov says after reaching 10 atm, hold for 10 minutes and watch the gauge. **A drop of up to 0.5 atm is normal** — residual trapped air, and plastic/PEX pipe expanding slightly under pressure — don't expect literally zero drop. **Physically inspect the entire run after the hold regardless of what the gauge showed** — a leak too small to register as a measurable pressure drop can still weep slowly enough to saturate and delaminate screed from its substrate over time, or slowly drip at a demountable "american"-nut union fitting, eventually accumulating into a puddle that repeatedly trips the leak-protection sensor under the collector (see [[12_Engineering_and_Systems/analysis/Leak_Protection_Systems|Leak Protection]]).

Zemstandart / Alexey Zemskov says **if pressure visibly drops**: look for a wet spot on the floor or visible drips at the collector to localize the leak. **If the leak is at a non-demountable joint** (e.g. where pipe meets an in-wall stub-out), that joint must be fully cut out and rebuilt from scratch — then **the entire pressure test must be redone**, not just re-checked at that one spot, since a system can have more than one leak and stopping after finding the first risks missing others that would only surface after the renovation is finished and walls are closed.

> [!WARNING]
> **Never try to inspect or work on a leaking joint while the system is still at 10 atm.** The joint can rupture suddenly under that pressure, and the resulting water jet is forceful enough to cause eye injury. Release pressure first, always.

Zemstandart / Alexey Zemskov says **what pressure testing does and doesn't validate**: it verifies internal rough-plumbing joints only — **not** any device attached downstream afterward (mixers, water filters, storage/tank water heaters, washing machines, dishwashers, etc.). These must be physically disconnected and capped with standard plugs during the test, not left connected.

## Practical Risks

attribution: unconfirmed — the cited multi-day risk has no decisive channel field: **a multi-day-installation risk**: if plumbing work spans more than one day, any point after the last outlet is installed is effectively an open invitation for other trades on site (plasterers needing water for mixing mortar, sometimes even connecting their own plastering machine directly to a supply point) to tap into the system between your own work sessions — physically isolate/disconnect the system when you're not actively working on it, or another trade's equipment risks damage from an unexpected pressurization, and your own test results risk being contaminated by their use.

attribution: unconfirmed — the cited air-testing fallback has no decisive channel field: **air-based pressure testing** exists as a fallback specifically for conditions where water would freeze (an unheated new-build in winter) — but is discouraged except as a last resort: finding an air leak requires soaping every single joint by hand, and a typical apartment has hundreds of joints (a house, thousands). Prefer delaying a water-based test until normal conditions are available over defaulting to air testing.

Zemstandart / Alexey Zemskov says **demand this test be performed in front of you before accepting rough plumbing** — otherwise a leak surfaces later as water in your own screed or the downstairs neighbor's ceiling, not as a caught defect.
