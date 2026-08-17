# 📋 Appliance Set Selection Rules

*Tags: #kitchen #rules #selection #design*

This document defines the binding rules used when composing appliance sets for this renovation project. It exists so that future replacements, additions, or reviews follow a consistent and visually coherent logic.

---

## 🔑 Rule 1 — Strict Pairs: Oven + Microwave

The oven and microwave will be installed **in a single vertical column**, one directly above the other, visible from the same angle at the same time. They must form a unified visual unit.

### 1a. Same Series (Generation)
Both appliances must belong to the **same product line / generation** from the same manufacturer. This ensures:
- Matching control panel layout (button positions, display style, knob shape)
- Matching handle design (profile, color, material)
- Matching frame/trim proportions

> **Example of a violation**: Pairing a Bosch Serie 8 oven (touch ring, TFT display) with a Bosch Serie 6 microwave (rotary dial, LCD). They are different generations with different UI philosophy.

### 1b. Same Color Scheme — No Exceptions
The entire front face of both appliances must match in color AND material finish:

| Finish | Code suffix (Bosch) | Acceptable pairing |
|---|---|---|
| Full black glass | `B0`, `B1`, `BB0`, `EB3` | Only with other full-black glass |
| Black + stainless trim | `MS0`, `S0` | Only with matching black+steel |
| Stainless steel | `S`, `SS` | Only with other stainless |
| White | `W`, `W0` | Only with other white |

> **Example of a violation**: Bosch **BFL524MS0** (black glass + stainless steel trim) paired with Bosch **HBG578EB3** (full black glass). The MS0 has a visible stainless steel border around the door and on the controls — a clear mismatch with the all-black EB3 oven panel.

> **Correct pair**: Bosch **BFL524MB0** (full black glass) + Bosch **HBG578EB3** (full black glass) — both are Serie 6, same black glass finish, matching rotary+LCD interface.

### 1c. Replacement Protocol
If one appliance in the oven+microwave pair becomes **unavailable**:
1. First, search for a **direct color/series replacement** of the unavailable unit within the same generation.
2. If no replacement exists in the same series, **both appliances must be replaced together** to maintain pair coherence.
3. Never substitute just one appliance if it breaks the series or color match.

---

## ⚖️ Rule 2 — Relaxed Pairs: Other Appliances

For appliances **not placed in the same visual column** (cooktop, dishwasher, hood), strict series matching is not required. However:

- **Color must still be consistent** across the set (e.g., all-black glass fronts across the kitchen)
- **Brand mixing** is acceptable (e.g., Bosch oven + Electrolux cooktop), as long as color matches
- A white induction hob would look out of place next to a black oven and microwave column — avoid this

---

## 🏷️ Rule 3 — Set Naming

Sets must be named to reflect their **actual positioning**, not just their price point. Do not label a set "Economy" if its total price is comparable to another set in the comparison.

| Naming principle | Example |
|---|---|
| Use the brand/series identity | "Bosch Serie 6 (Balanced)" |
| Reflect the standout feature | "Gorenje Pyrolysis (Full-featured)" |
| Never mislead on price tier | Don't call a ~3,600 BYN set "Economy" if the next set is ~3,554 BYN |

---

## 📐 Rule 4 — Column Visual Simulation

In the **Visual Column Comparison** table in `Kitchen_Appliance_Sets.md`:
- Images must reflect the real installed proportions: same width, oven taller than microwave
- `width: 100%; height: auto` on all images — lets the natural image ratio determine height, simulating real-world proportions where both appliances are 60 cm wide but the oven is taller
- Images are placed in a **single flex column cell** per column (`display: flex; flex-direction: column; gap: 0`) to eliminate any gap between them

---

## 🔍 Rule 5 — Availability Check (onliner.by)

Before finalizing any model in a set:
1. Verify the model is **currently listed and in stock** on `catalog.onliner.by`
2. If out of stock, find the closest replacement following Rule 1 (for oven/microwave pairs) or Rule 2 (for others)
3. Document any substitutions and the reason in the appliance set notes

---

*Last updated: 2026-06-12. Applied to: Kitchen sets, Laundry sets.*
