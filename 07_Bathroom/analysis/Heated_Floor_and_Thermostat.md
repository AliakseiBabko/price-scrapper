# Bathroom — Heated Floor & Thermostat Placement

Covers underfloor heating cost/scheduling, area-cap/sensor-redundancy rules, and a real practitioner disagreement on thermostat mounting height. Part of [[07_Bathroom/Bathroom_Guide|Bathroom Guide]].

## Cost, Scheduling, and Sensor Redundancy

**Electric underfloor heating, cost and control**: a full setup (heating mat, thermostat, installation) is cited around **~30,000 RUB** — described as easily worth it if the budget allows, with no real downsides beyond cost. Because tile heats and cools slowly, it can't be toggled on-demand like a light switch — the source runs theirs on a schedule (starting ~6am to be comfortably warm by ~9am).

- **Heating-mat area cap and sensor redundancy**: one practitioner caps underfloor heating mats at **~12 m²** per mat/zone. Each mat should have **3 temperature sensors, not 1** — the sensor itself is described as more likely to fail than the mat, and a failed single sensor leaves no way to control (or safely confirm the state of) an otherwise-working mat. `single-account`, `unverified`. [sources: `_Archive/processed_sources/20260804_business_class_five_attributes_19385e7a.txt`, `_Archive/processed_sources/20260804_pro_secrets_lifehacks_f0be401f.txt`]
- **Multi-mat rooms need a multi-loop plan, plus one aggregating controller so occupants don't have to walk between thermostats**: a room larger than the ~12 m² cap needs either a center-only or perimeter-only mat, or two separate mat loops each with its own thermostat. Worked example: living room = two 12.6 m² mats, kitchen = two 12–14 m² mats, each room with two thermostats. To avoid forcing occupants to operate multiple room thermostats separately, install one aggregating app/controller that lets every room's thermostats be operated as a group from one interface. `single-account`. [source: `_Archive/processed_sources/20260804_business_class_five_attributes_19385e7a.txt`]

## Thermostat Mounting Height — Practitioners Disagree

**The question**: how high should a thermostat be mounted, and does that answer depend on the specific unit's usage pattern?

**Perspectives:**

| Source | Position | Reasoning |
|---|---|---|
| Unnamed source (heated-floor cost/scheduling video, above) | Mount height should scale with how often you'll adjust it | A simple on/off thermostat can go anywhere. A programmable (set-and-forget) one can be low/out of sight. One you expect to adjust frequently should be mounted higher, at a convenient reachable height. |
| Zemskov / Zemstandart (Moscow, apartment-wide, not bathroom-specific) | Flat eye-level (160-170cm) for every thermostat, regardless of type | An LCD display, unlike a smartphone screen, is only legible head-on, not at an angle — a low unit forces crouching to read/operate. He explicitly rejects the common "mount high so kids can't reach it" child-safety framing as his actual reason, and separately notes he finds it ineffective in practice (children lose interest in switches quickly). |

**Common ground**: both are `single-account`, and neither directly rebuts the other's specific reasoning (usage-frequency vs. display-legibility) — they're answering slightly different questions, which is part of why this doesn't resolve cleanly into "one is right."

**Your priority**: *— not yet decided.* Zemskov's rule is a flat default requiring no case-by-case judgment; the other source's rule requires deciding, per thermostat, how often you expect to actually touch it. If most of this project's thermostats will be set-and-forget (programmable schedules, rarely touched), the first source's logic argues for low/hidden mounting; if you expect to check/adjust them often, both sources converge on mounting them higher.

### Zemskov's Full Placement Rules (apartment-wide)

> [!NOTE]
> This subsection is Zemskov/Zemstandart's own stated practice and reasoning, `single-account`, no cost figures given. [source: `_Archive/processed_sources/20260810_underfloor_heating_thermostat_placement_e9333bb7.txt`]

- **Core rule: a thermostat must always be visibly mounted, never hidden** — unlike a light switch (the light itself signals state), a hidden thermostat gives no way to check on/off/temperature without walking to it.
- **WC/bathroom-specific rule: mount the thermostat outside the room it controls, never inside** — lets you check at a glance (before entering, or on the way out of the apartment) whether it was left on. **General heuristic he gives**: place the thermostat on the same side (inside or outside the room) as that room's own light switch.
- **Thermostat-type recommendation**: an "electro-mechanical" type (LCD display for information only, physical tactile buttons for control) over a fully mechanical dial (no way to confirm the current setting from a distance) or a fully touchscreen unit (sluggish feel versus a smartphone; his estimate ~98% of clients with a fully-loaded unit use only one function despite paying for the extra complexity).
- **Single most emphasized rule: always extend the thermostat's temperature-sensor wire by soldering, never with twist-splices or standard connectors** — a stock sensor wire is too short for eye-level mounting; soldering is, per Zemskov, the one place in a modern renovation he still recommends it, since the joint must repeatedly pass through a dedicated conduit as sensors (unlike heating elements, which he says rarely fail now) do eventually need replacing. **Install that conduit from the thermostat down to the sensor pocket at rough-in stage** — without it, a failed sensor can't be practically replaced later without disturbing the finished floor.
