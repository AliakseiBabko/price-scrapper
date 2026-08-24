# HVAC — AC Condensate Drainage: Why a Simple Trap Isn't Enough

Part of [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]].

An AC indoor unit produces condensate that has to go somewhere, and the "obvious" options are both wrong:

Zemstandart/Alexey Zemskov warns: **draining straight into a sewer stack** lets sewer odor and bacteria migrate back up into the room through the drain line.
Zemstandart/Alexey Zemskov explains: **a simple water trap** (P-trap style) seems like the fix, but during periods the AC isn't running, the trap's water **evaporates**, loses its seal, and the same backflow problem returns.

Zemstandart/Alexey Zemskov recommends: **the correct mechanism is a "dry trap" valve**: condensate flows into a small reservoir; rising water lifts a floating ball; once the water rises high enough, it overflows through a top port into the sewer connection (a standard ~32 mm pipe). When the AC sits idle and the reservoir water evaporates, the floating ball settles and blocks the opening — so there's no path for sewer gas/bacteria to travel back up the drain, even after months of disuse.

Zemstandart/Alexey Zemskov recommends: **route AC condensate drainage into the bathroom/WC specifically, not out through the building's exterior facade** — a second source, corroborating the underlying mechanism above, states that venting condensate outdoors on a modern building tends to create real problems (icing, staining, facade-appearance issues) and recommends routing it into the bathroom's own drainage instead. **A dry-trap siphon is specifically required here, not an ordinary water-trap type** — an ordinary trap's water reservoir evaporates over a season the AC isn't used (e.g. winter), and once dry, sewer odor migrates back up through the AC's own drain tubing and spreads through the apartment via the indoor unit — the same seasonal-disuse failure mode, restated with the specific fix (route to bathroom + use a dry trap) rather than just the mechanism.

**Practical installation notes:**
- In-wall condensate and refrigerant lines should run at roughly a **2° slope** toward the sewer riser.
Zemstandart/Alexey Zemskov recommends: **photograph the routing during installation** — this meaningfully reduces the risk that later wall work (shelving, drilling) accidentally damages a hidden line.
- Where gravity drainage to a riser isn't feasible (e.g. the nearest riser is too far or wrong elevation), a **condensate pump** is the standard workaround, mounted inside/adjacent to the indoor unit housing.
- **⚠️ Reliability caveat (added 2026-08-24, Round 4)**: Konstantin Kruglov/Ontario flags condensate pumps as failure-prone and noisy in practice — "no reliable long-lasting device exists" in this category per the source, and the pump's own noise creates a separate comfort problem. The source's practical recommendation is to plan indoor-unit placement so a pump is never needed at all, rather than treating it as an equivalent alternative to gravity drainage. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]
