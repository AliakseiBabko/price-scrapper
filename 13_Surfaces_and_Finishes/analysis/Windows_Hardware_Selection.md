# Windows — Hardware Selection

Part of [[13_Surfaces_and_Finishes/Windows|Windows]].

## Tilt-and-Turn vs. Turn-Only

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) recommends: **Tilt-and-turn is unambiguously the better default over turn-only, all else equal** — the cost premium is small (~1-2% of total window cost), negligible against the functional gains. Three advantages:

1. **Avoids needing a hard fall-limiter/restrictor**: a turn-only sash swings fully open with no other restraint, requiring a child-safety stop as an added part/failure point.
2. **Trickle/slot ventilation**: turn-only sashes are only fully open (losing heat/security) or fully closed — tilt-and-turn's tilt position gives a small continuous perimeter gap for fresh air without opening the sash.
3. **Durability/self-weight mechanism for large sashes — the main point**: a large, heavy sash operated by full swing-open turning bears its own weight on the side hinges every time it opens, gradually deforming/sagging (adjustment screws compensate only temporarily). **A large sash (worked example: ~2m×2m, near-square) can't be split into a narrower vertical pair** for facade-appearance/code reasons — a heavy near-square sash operated fully-open reportedly deforms within about a week of regular use to the point it can't close properly. **Fix: restrict a large/heavy sash to tilt-only operation** (occasional use, e.g. cleaning) — tilting transfers the sash's weight onto the bottom frame/transom instead of the side hinges, avoiding the deformation mechanism entirely.

## Panoramic-Window Safety Hardware

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) explains: **The problem**: standard safety-code parapet height (~1.1m) conflicts directly with a panoramic-window design goal — at that height, someone seated sees mostly the opaque parapet and only a strip of sky, not the view a floor-to-ceiling glazed section is meant to provide.

Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov) recommends: **Standard resolution**: split the window into a fixed panoramic (non-opening) section below the code-required parapet height, and a small opening transom (фрамуга) above it, rather than making the whole panoramic window openable.

### Device 1 — Remote Transom-Opening Mechanism

A handle-plus-linkage-plus-angled-hinge assembly lets a high transom (positioned anywhere above the low parapet) be opened from a handle mounted at normal reachable height, without climbing on furniture. Solves two failure modes of the naive alternative: a low handle lets driving rain blow straight in through the low opening gap; a high handle avoiding that problem becomes unreachable without a stool, with real fall risk. **Includes an integrated anti-break-in push-button lock** — a small transom section is otherwise easy to force open from outside by simply pushing; one motion releases it from inside.

**Framing vs. standard child-safety locks**: standard child-safety locks on openable windows are unreliable in practice because parents forget to re-engage them after use — this design removes the child-accessible opening entirely rather than relying on a lock someone must remember to use. `single-account`, not independently benchmarked against child-safety-incident data.

### Device 2 — Removable/Detachable Technical Handle

For a panoramic (non-transom) window section that must default to non-openable for child safety, but occasionally needs to open — stated example: periodic servicing access to an external AC condenser mounted behind the glazing. A decorative cap normally sits flush in the handle-spindle position (window reads as a plain fixed pane); sliding the cap aside exposes the spindle, where a separately-stored ordinary PVC-window technical handle is fitted to open/close the window, then removed and the cap snapped back afterward.

**Stated child-safety property**: claimed "practically impossible" for a child to defeat without the stored handle (specifically ruling out a pencil/found-object attack on the exposed spindle) — `single-account`, narrator's own claim, not independently tested.

Both devices are stated to be established, multi-year-use hardware, not a new invention — the source's framing is informational (most people don't know these exist).

## DIY Sash Self-Adjustment

Two specific adjustments, one tool (a 4mm hex key) — **explicit scope limit**: any other fitting/hardware adjustment should be left to a professional.

1. **Vertical position adjustment** — a screw at the bottom hinge controls the sash's vertical position; turning it clockwise several times raises a sagging sash that's begun catching on the frame.
2. **Seal-pressure adjustment** — an eccentric bolt around the sash perimeter controls how firmly the sash presses against the weatherstripping; rotating the eccentric's thicker lobe toward the seal increases pressure. **Paper-test technique**: close the sash on an ordinary sheet of paper at a test point, then pull it out — pressure is too weak if it slides out easily, correct if it comes out with resistance or tears. **Repeat at multiple points around the sash perimeter**, not just one — pressure varies point to point.

## Developer-Window Repair & Adjustment (added 2026-08-19)

> [!NOTE]
> A partner-branded technique demo (guest installer explicitly introduced as a company partner) framed as a stopgap for developer-standard windows the source's own company would otherwise discard outright — not a permanent fix or an endorsement of developer-grade windows. Extends the DIY sash self-adjustment content above with genuinely different adjustment points. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_uBNF5ZYOE0Y_developer_window_repair_195|note]]]

- **Lock strike-plate (ответная часть) alignment**: simulate the sash's closed position by turning the handle down *first* — this is what determines where the lock's moving part actually seats, not the sash's physical position against the frame. Press the sash to the frame and check whether the frame-mounted strike plate aligns with the lock mechanism; if not, loosen and slide the strike plate until it does. Repeat per lock point on all sashes.
- **Sash-to-frame overlap (притвор) consistency check**: pencil-mark the sash's overlap edge against the frame where the seal runs, close the sash, then reopen and measure the overlap distance at several points around the perimeter — inconsistent distances indicate the sash itself sits wrong relative to the frame (not a seal problem). Fix with the same 4mm hex key used for vertical/seal-pressure adjustment above.
- **Center-pressure-part (средний прижим) relocation**: for a misaligned two-part fitting causing draft, unscrew and flip/reposition the *frame-side* piece. This exposes old fastener holes — clean/degrease them and seal with tube-type sealant, applied with a finger, using a white cloth (never colored — the degreaser is also a solvent that can transfer dye) and long sweeping wipe strokes (short dabbing risks the cloth sticking).
- **Seal (уплотнитель) inspection and replacement, by profile type**: check corners specifically first — a seal welded at the corners during frame fabrication loses elasticity exactly there, creating four hard-point contacts instead of even perimeter pressure. **Decision rule**: single-lobed seal → replace immediately; double-lobed → inspect, replace only if degraded; chamber-type with a small lobe → generally fine as-is. Also check the seal's own splice/joint location — correct at the *top* of the frame (unnoticed micro-draft), a defect at the *bottom* (felt draft).
- **Final-step check, easy to overlook**: retighten the handle's own mounting screws (they loosen with normal use) using a manual Phillips screwdriver only — a powered driver risks stripping/over-torquing them, leaving the handle loose on the sash.

## Condensation Fix: Windowsill-Drilled Directional Vent

When a wide windowsill blocks radiator warm air from reaching the glass (severe cases: a rag has to be laid along the frame to catch water), drill a hole through the sill directly opposite the center of each glass unit and insert a directional grille, one per pane — restores warm-air flow to the lower glass and stops fogging. **Explicit caution: only drill the sill if condensation is actually a problem** — don't drill preemptively.
