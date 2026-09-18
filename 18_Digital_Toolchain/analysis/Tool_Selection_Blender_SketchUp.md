# Blender against SketchUp — what the evidence actually supports in 2026

**Added 2026-09-18** from a five-video comparison cluster plus two working demonstrations. Written because the owner asked for hindsight on the tool choice.

> [!CAUTION]
> **⚠️⚠️ THREE OF THE FIVE COMPARISON VIDEOS CANNOT SPEAK TO A 2026 DECISION, AND THAT IS THE FIRST FINDING.**
>
> | source | uploaded |
> | :--- | :--- |
> | *Is SketchUp actually BETTER Than Blender?* | **2022-05-11** |
> | *Should You Switch From SketchUp to Blender?* | **2022-05-11** |
> | *Blender vs Sketchup — Which One is Better?* | **2021-11-11** |
>
> **All three predate Blender 4.x, let alone the 5.2 LTS installed here.** EEVEE Next did not exist; the add-on ecosystem was different; Bonsai was still BlenderBIM. **Quoting their verdicts as current would be this vault's own date discipline (standing rule 2) failing on software instead of prices.** They are logged as triaged-out so nobody re-reads them, not discarded quietly.

## What the current evidence says

### Blender is the challenger, not the standard

`6dfSakWnqcY` (2026-01) cites a **2024 survey: ~59% of ArchViz artists on 3ds Max, 9–10% on Blender.** That is worth knowing when handing a file to somebody else — **an IFC hand-off is portable, a `.blend` is not**, which is one more reason this project issues IFC rather than a Blender file.

### ⚠️ The walkthrough requirement is already satisfied by what is installed

The owner wants to **walk through the flat from inside**. The same source names **EEVEE Next, in Blender 5**, as the realtime engine for exactly that — Cycles for polished stills, EEVEE for interactive movement.

> **`tools/blender/bin/blender-5.2.0-windows-x64` is already Blender 5.** The walkthrough needs no new software, no new licence and no change of plan. ⚠️ blender.org now serves **5.2.2 LTS** (2026-09-15); we are two patch releases behind on the same line.

### Precision in Blender is numeric, not guide-based

`CVa-dNIkel8` (2025-09) answers the commonest SketchUp-refugee question: **you do not need guides.** Select an edge, `Shift+D`, then axis and distance — `X 20`, `Enter`. He warns that SketchUp users *"create guides for everything"* until nobody can attribute them.

⚠️ **Largely moot here** — this project does not model by hand in either tool, because geometry is compiled from `data/canonical`. What transfers is that **Blender's precise input is numeric and axis-locked**, the same discipline the compiler enforces.

---

## ⚠️⚠️ The comparison that actually matters is not Blender vs SketchUp

Two working demonstrations by **Степан Огурцов** (`YT_1WakaBxLkVg`, `YT_KTvihMIPFVk`) build real dimensioned models in SketchUp from drawings, via Claude-generated Ruby. **They are better evidence about the workflow than any of the comparison videos**, because something is actually produced and checked.

### Perspectives — the tool is not the decision, the ARCHITECTURE is

| | position |
| :--- | :--- |
| **Comparison videos** | which modeller has better rendering, add-ons, learning curve |
| **Огурцов, in practice** | the modeller is a target; what matters is that **a script is generated and pasted**, never a live connection |
| **This project** | the modeller is a *consumer*; geometry is compiled from canonical data and issued as IFC |

**All three of Огурцов's routes and all of this project's outputs share one property: the model is produced by generated, inspectable code.** SketchUp takes Ruby; Blender takes Python and Bonsai; IFC takes neither and is read by both. **On that axis the Blender choice is not in tension with his method at all** — he would be doing the same thing here, in a different language.

### Your priority

**The tool comparison does not reopen the decision, and the strongest reason is not in any of these videos**: a generated artefact can be *gated*. `check_dxf_closure.py`, `raster_fidelity.py` and the IFC checks exist because the output is a file that can be diffed against canonical data. **A hand-modelled SketchUp scene has nothing to check against, whoever made it.**

⚠️ **Where SketchUp genuinely wins, and it is worth saying plainly:** Огурцов's loop from drawing to walkable massing is *fast*, and his generated Ruby even runs on SketchUp Make 2017. **If the goal were a quick client-facing massing rather than a gated construction model, SketchUp would be the better tool.** This project needs both, and the model-first architecture is what lets one produce the other.

---

## ⚠️⚠️ The failure mode both demonstrations hit — and it is not about tools at all

**In two different videos, on two different subjects, the geometry came out dimensionally correct and the OBJECT IDENTITY came out wrong:**

- an apartment: a services duct and a **лоджия swapped**, windows merged into the wrong wall, *«понял, что это лоджия на своё усмотрение»*
- a kitchen: **drinking glasses modelled where taps belonged**, and an entire kitchen **mirrored** without notice

> **Neither error is detectable by any dimensional check.** Both would survive a tape measure, a closure gate and a raster overlay. **This is the single strongest external argument for canonical-data-first**: identity, class and adjacency are *authored and gated*, and geometry is *compiled from them* — rather than identity being inferred from geometry by anything, human or model.

And his governing warning, which belongs next to `00_Master/Validator_Design_Discipline.md`:

> *«Вы должны понимать, что происходит… чтобы видеть косяки нейросетки, которые всплывают внезапно, а нейросеть их косяками-то и не считает.»*

**The model does not consider its mistakes mistakes.** Arrived at independently, outside this project, from the opposite direction.

## Source Notes

- `YT_1WakaBxLkVg`, `YT_KTvihMIPFVk` — Степан Огурцов, 2026-09-16 and 2026-09-17, Russian, working demonstrations.
- `6dfSakWnqcY` — inspirationTuts CAD, 2026-01-03. `CVa-dNIkel8` — Expose Academy, 2025-09-28.
- Triaged out as stale: `-vWO3dC2ap0`, `KRq8Dc8yRxk` (both 2022-05-11), `79MonZ5CMVw` (2021-11-11).
- No prices in any source. None region-specific except the Russian channel attribution.
