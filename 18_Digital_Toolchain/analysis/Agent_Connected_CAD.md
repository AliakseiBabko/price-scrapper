# Agent-Connected CAD

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**What happens when a language model is wired directly to a CAD or BIM application rather than handed a file — the two architectures, the feedback trade-off, and the one thing it reliably cannot do.**

> [!IMPORTANT]
> **⚠️ Install steps and product versions from these sources are deliberately not recorded.** They date within months and none of this is this project's toolchain. **What is recorded is the architecture and the observed failure categories**, which outlive any particular connector.

## 1. Two architectures, and this vault previously held only one


**⚠️ A plain definition, from a setup tutorial, since this page assumed one:** *"MCP
stands for Model Context Protocol — the standard way that AI tools communicate
with systems where data live, or different tools. This is how your AI talks to
SketchUp."* **The shape is two pieces: an EXTENSION inside the CAD application that
exposes its own scripting API and built-in tools, and a CONNECTOR in the AI
desktop client that turns language into commands the extension executes.**

**⚠️⚠️ It grants two distinct powers and conflating them is a mistake**: the agent can
**execute arbitrary code** in the application's scripting console, **and** it can
**call the application's existing tools** — the second being the tool-driving
architecture §4 records as strictly better than emitting raw geometry. ⚠️ **It
requires the DESKTOP client; the web version cannot do it, and there is no extra
licence cost — it spends subscription tokens "a lot more quickly."** ⚠️ **Named as
useful for EXTENSION DEVELOPMENT as much as modelling: write a script, run it, see
the result, iterate, "without you having to go in and double-check what it did."**
[source: [[_Sources/YT_pkFnSQ9Bapg_archivlogs_gpt6_revit_mcp_planning_reversal|YT_pkFnSQ9Bapg]]]

**⚠️⚠️ A refinement of an existing vault finding, and the distinction is real.**

[[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7 records, from Trimble's own channel, that *"an AI CAD integration is a FILE GENERATOR, not a live modeller — there's not a direct live connection… it won't go in and edit it"*, with each change emitting a new file. **That is true of the adapter it describes, and false of an MCP-connected application.**

| | **Open loop** (file generator) | **Closed loop** (MCP-connected) |
| :--- | :--- | :--- |
| **How it works** | The model emits a geometry file; a human imports it | Model → connector → the application's **own scripting API** → the running document |
| **Feedback** | None. The model never sees the result | **The application sends back a view of what it did**, and the model issues the next command against it |
| **State** | The file | **The running document** |
| **Observed** | An elevation → a `.dae` file in 5–10 min, imported by hand ([[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|sujS9Mgveo4]]) | Prompt → reasoning → FreeCAD Python API → **screenshot of the viewport returned** → analyse → next command, repeating ([[_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp\|6trAkQY5_kc]]) |

- **The closed loop is what lets a model build something step by step** rather than in one shot, because it can react to what it actually produced.

> [!IMPORTANT]
> **⚠️⚠️ AND THERE IS A THIRD OPTION THE TABLE OMITS, WHICH A PRACTITIONER RUNNING
> BOTH RECOMMENDS FOR THE BULK OF THE WORK: HEADLESS SCRIPTING.**
>
> He models in **Blender by writing scripts against its API headlessly** and drives
> **Unreal by MCP**, and explains each choice. On the modelling: *"use the Blender
> API headlessly to write the script to generate the file and then take screenshots
> to confirm progress — **this is a far more token-efficient way of modelling
> without connecting to an MCP server**."* **The agent "does not see the live model"
> and instead renders screenshots back into the project folder to check itself.**
> *"**Using pure code is far more efficient** to generate simpler models and
> processes, **although using MCP has far more control for detailed models**."*
>
> On Unreal, where he does connect: *"the main difference … is that you have much
> more **natural conversation** … **However, it does come at a great cost, which is
> both time and token count.** I would still recommend using MCP mainly for the more
> technical parts — graph setup, blueprint creation, complex asset placement —
> **rather than trying to generate every single detail this way.**"*
>
> **→ ⚠️⚠️ SO MCP IS A CONTROL SURFACE, NOT A CAPABILITY GATE.** The geometry can be
> produced either way. **What MCP buys is conversational granularity and live
> control; what it costs is tokens and wall-clock time, by roughly an order of
> magnitude (§ costs below).**
>
> **→ THE ALLOCATION RULE: SCRIPT the bulk generation; reserve MCP for interactive
> setup that is awkward to express as a batch script.**
>
> **→ ⚠️⚠️ THIS PROJECT IS ALREADY ON THE SCRIPTED SIDE, and one step better.**
> `tools/ifc/model_from_spec.py` is headless generation from a spec; the difference
> is that **his verification is the agent looking at its own screenshots, and this
> project's is deterministic gates that can fail a build.** **The feedback channel he
> relies on is precisely the one this page flags as unreliable.** [source: [[_Sources/YT_SsBLhNgqTqQ_mcp_versus_headless_scripting_and_measured_accuracy|YT_SsBLhNgqTqQ]]]

- **⚠️⚠️ But note what the feedback channel IS: a screenshot. The model checks its own work by looking at a picture of it** — which places the verification step squarely inside the precise-visual-interpretation weakness measured on [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]]. **The loop is closed; its feedback is the unreliable channel.**
- A comparable path exists for Revit via the **pyRevit** plugin plus an MCP extension and a desktop-client connector entry, and Claude is reported connecting directly to **Rhino and Revit** to model from a single instruction. [sources: [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp|vmVvpKSSxWE]], [[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects|la8Ml1fQfOg]]]

## 2. ⚠️ The feedback/token trade-off, which is a real engineering decision

The FreeCAD connector ships **two configurations**, and the choice generalises far beyond it:

- **With viewport screenshots** — after each command the model receives the text result **and an image**, so it "can actually see what it built and react to it visually." **More tokens on every single operation.**
- **`only_text_feedback`** — **no image**; only object names, dimensions, and success or error messages. **Significantly fewer tokens per operation.**
- **Stated guidance: screenshots for short sessions of one or two parts; text-only for long sessions with many back-to-back operations.**

> **→ The general form: visual feedback buys the agent the ability to notice what it did wrong, and costs tokens on every operation. Text feedback is cheap and blind.**
>
> **⚠️⚠️ And the reason to record it here rather than adopt it: this project has already chosen a third option that neither source has.** `check_dxf_closure.py`, `check_wall_junctions.py` and `raster_fidelity.py` are **deterministic** feedback — not expensive-and-fallible, not cheap-and-blind, but **exact, machine-checkable, and able to fail a build.** **The trade-off above only binds when the checker is the model itself.** That is the whole argument for gates over inspection, arriving from outside.

## 3. ⚠️⚠️ What it can do, and the one category it cannot

**A Revit session demonstrated on camera, and the split in its results is clean.** [source: [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp|vmVvpKSSxWE]]]

**Succeeded** — all of it transcription: creating walls from a drafted plan, adding a floor per room, placing doors, **naming and numbering every room**, adding room tags and windows. The operator's own comparison: *"doing a better job than a fresher who has just started using Revit."*

**Failed** — all of it spatial logic:

- A plan **closed on all sides**, with no circulation.
- **A forgotten wall** — *"it forgot to add a wall over here for some reason."*
- **A door to a bedroom placed outside the building.**

**⚠️ The operator's own conclusion is the finding, and he states it plainly: *"It can't plan right now. What it can do is basically create a model from your existing floor plans."***

> [!WARNING]
> **⚠️⚠️ REVISED 2026-09-16 — THE SAME ARCHITECT, A NEWER MODEL, AND THIS NO LONGER HOLDS CLEANLY.**
>
> He re-ran his own test with a deliberately harder brief — a 40 × 50 ft site, a
> **four-bedroom** house, parking, two washrooms, a courtyard, and three stated
> setbacks — with **no plan supplied**, saying *"I wouldn't do this to any intern."*
> **In about 14 minutes it returned a two-level plan honouring all three setbacks,
> an ~8 × 8 ft courtyard, ground-floor parking, a staircase in two flights of nine
> risers that he checks and calls "perfect", plus sections, elevations and sheets
> unprompted — and furniture modelled in place, including a car correctly
> categorised as parking.** It also **self-corrected mid-run**: *"the first visual
> check caught dining chairs encroaching on the staircase approach — I am moving
> the dining seating forward."*
>
> **⚠️⚠️ BUT THE HONEST REVISION IS NARROWER THAN THE VIDEO'S TITLE, and his own
> commentary supplies the limits.** **Rooms were not named at all** — he is reduced
> to guessing: *"I believe one of them is a bedroom, this was supposed to be a
> kitchen, probably this can be a washroom."* **A window looks into a space rather
> than out.** **An area is left over that he cannot account for.**
>
> **→ SO THE MOVE IS FROM "cannot plan" TO "produces a plausible massing and
> circulation with UNRESOLVED ROOM SEMANTICS."** **Naming a room is the cheapest
> part of planning and it did not do it; deciding what a leftover area is for is
> planning, and it did not do that either.**
>
> **→ ⚠️⚠️ AND THE RULE UNDER THIS PAGE SURVIVES INTACT: an agent silently supplies
> what you did not specify. Here it supplied room boundaries it could not name and
> a window orientation nobody asked for. The failure mode did not change — only its
> granularity did.**
>
> ⚠️ **Weighting: same observer, same channel, no independent replication; heavily
> promotional, including an uncontrolled "the other model messed up big time"
> comparison which is NOT carried.** ⚠️ **One thing does raise its value: the brief
> is a generic house, so the famous-building retrieval explanation does not apply.**
> [source: [[_Sources/YT_pkFnSQ9Bapg_archivlogs_gpt6_revit_mcp_planning_reversal|YT_pkFnSQ9Bapg]]]

> [!IMPORTANT]
> **⚠️⚠️ AND THE FIRST MEASURED CHECK, from a different practitioner three days
> later, turns that revision into something precise.** He set out to test accuracy
> rather than capability — *"how usable are these AI features if they're still
> producing inconsistent and inaccurate results?"* — supplied **two floor plans,
> dimensions, areas and style references**, modelled in **Rhino**, and then measured
> the output against the input.
>
> | Checked | Result |
> | :--- | :--- |
> | **Overall dimensions** (input 46 × 42 ft) | **CORRECT** — *"the dimensions are accurate. I'm honestly surprised."* |
> | **Room locations against the plan** | **CORRECT** |
> | **Materials against the style reference** | Largely correct |
> | **⚠️⚠️ Detail, on closer inspection** | **WRONG** — *"the more I look at it, the more detail I get into it, it just kind of messed things up"* |
>
> **→ ⚠️⚠️ THE FAILURE IS DEPTH-DEPENDENT, NOT RANDOM: overall dimensions and room
> topology survive; detail degrades the closer you look.** **That is a much more
> useful statement than "it can/cannot plan", and it yields his own rule — use it
> for ELEMENTS rather than whole buildings: site context, a few window variants, a
> roof or rainscreen study.**
>
> **⚠️ Both this source and the scripting one agree the INPUT decides the outcome:
> *"if you do provide scaled plans, sections and elevations, it can use those to
> build much more accurately."* → The same conclusion this project reached when it
> chose to model from printed dimension strings over a registered raster.**
> [source: [[_Sources/YT_SsBLhNgqTqQ_mcp_versus_headless_scripting_and_measured_accuracy|YT_SsBLhNgqTqQ]]]


> **→ An agent-connected CAD is a MODELLING ACCELERATOR from a plan that already exists, not a space planner.** Every success was transcribing something specified; every failure was inferring something that was not.

- **⚠️ This corroborates, from an entirely different tool, the rule already on [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7: an agent generating building geometry silently supplies the values you did not specify.** There it invented 5-inch walls, a 9-ft ceiling and a standard door. Here it invented a door position and omitted a wall — **and nothing flagged either.** The mitigation is unchanged: **require an agent to enumerate every value it supplied that the prompt did not, and treat each as a defect to resolve from evidence.**
- **⚠️ Directly relevant to this project's `v0` route**, which is to model from the printed dimension strings over a registered raster rather than to ask an agent to design. **This is the external evidence that the route is the right one** — the failures are precisely in the part this project never delegates.

## 4. ⚠️⚠️ A third architecture — drive the tool, don't emit the geometry

**Both architectures above have the model producing geometry. An independent tester, on the connector's first day, predicts that is the wrong shape entirely — and names why:**

> *"Describing things with words is inherently clunky… it's very difficult to describe the precision movements and things that we do in 3D to an AI engine and have the AI engine actually understand it."*

**His proposed correction: the model should not emit geometry at all. It should DRIVE THE RIGHT PARAMETRIC TOOL inside the application.** He cites a real instance — an MCP server integrated with **Medeek's extensions**, so the agent instructs Medeek's *wall tool* and that creates the walls. *"Instead of saying make me this space… it'll go find the right tool in SketchUp."*

> **→ This is strictly better than both. Open-loop emits geometry and cannot check it. Closed-loop emits geometry and checks it by looking at a screenshot. TOOL-DRIVING delegates to something that enforces the invariants BY CONSTRUCTION — a wall tool cannot produce walls that fail to merge at a corner.**
>
> **⚠️⚠️ And this project is already on that architecture.** `tools/layout/export_v0_dxf.py` is a controlled emitter and the gates check its output; nothing writes raw geometry freehand. **External corroboration of a choice already made — from someone arriving at it as a prediction rather than as practice.**

- **Corroborated from a second direction**: a vendor's own release notes are cited as claiming their model is *"significantly better at drawing 3D objects using CAD code"* — i.e. the improvement is being pursued through **code execution against a tool**, not through better direct geometry generation. [sources: [[_Sources/YT_X1lnTEpy6PQ_sketchupessentials_claude_connector_day_one|X1lnTEpy6PQ]], [[_Sources/YT_E-ECbD14g_8_sketchupessentials_mcp_permission_and_estimation|E-ECbD14g_8]]]

### ⚠️ Third confirmation of the open loop, and the defect this project gates for

**An independent tester reaches the file-generator conclusion by trying to make a change**: *"I don't think there's like a live link in here… it can't go in there and it can't make changes to your model."* Asked to resize a room, it **regenerated the whole model and he had to re-download it**. **A mechanism detail the vendor video omits: it works by writing a mini-script** — so it is code generation, and that is why it is open-loop.

- **⚠️⚠️ And he names the exact defect `tools/layout/check_wall_junctions.py` exists to reject**: *"these walls are all kind of separate and they don't really like merge together on the corners."* **The same family appears again in a furniture test** — arms built as cylinders *"still kind of intersecting with the model."* **Non-merged, interpenetrating solids are the characteristic failure of generated geometry across every tool in this round.**
- **The transcription-succeeds / spatial-logic-fails split holds for a third time**: given a floor-plan image, window widths came out **4 ft** and **4 ft** and the overall space **12 × 12 ft** — *"generally right"* — while *"it definitely did not match the orientation of the bed"* and it *"did a terrible job of orientation on the furniture."*


**⚠️⚠️ A STAGE-GATE METHOD, from the most honest source in the 2026-09-16 batch — a
3ds Max practitioner who deliberately published his failures** (*"I have
intentionally kept the unsuccessful moments… short social media demonstrations
usually show only the final few seconds"*), **and who notes mistakes can begin "as
early as the scaling or wall construction stage":**

> *"**One project, one chat, one completed stage, one instruction or skill.** First
> define the task and review the result. Then check it. **Submit a consolidated
> correction list.** Approve the stage and only then continue."*

**His conclusion on what the tool is:** *"A powerful automation tool, **but not an
autonomous 3D visualizer.** It performs specific tasks well when it receives
accurate source data, a clear algorithm, and defined review criteria. **If you give
it an entire project in one enormous prompt, the result becomes unpredictable**,
while the time and token costs rise very quickly."*

> **⚠️⚠️ AND AN ANTI-OVER-ENGINEERING RULE WORTH KEEPING VERBATIM, because it cuts
> against the direction everything else in this space pushes:**
>
> > *"**Do not build a complex system of agents simply because it sounds
> > technologically impressive. If you can check something with your own eyes in
> > two minutes, there is no reason to spend resources on a separate agent.**
> > Automation should simplify your work, not make you watch artificial
> > intelligence argue with itself for hours."*
>
> **→ That is the right test for this repository's own apparatus, and it is the
> complement of [[00_Master/Validator_Design_Discipline|Validator Design
> Discipline]]'s rule that a gate nobody has watched fail is not a gate: a gate
> earns its place by catching what a person would miss or would not repeat.** **A
> two-minute eyeball check does not need one.**
>
> ⚠️ **He also reframes the operator rather than removing them:** *"you become the
> operator and art director… accuracy, taste, composition and the final artistic
> decision still remain the responsibility of the human."* **Greatest value, in his
> words: repetitive operations, batch corrections, and complex custom modelling.**
> [source: [[_Sources/YT_SsBLhNgqTqQ_mcp_versus_headless_scripting_and_measured_accuracy|YT_SsBLhNgqTqQ]]]

**⚠️ COSTS, in usage rather than currency — the only such figures this vault holds,
all self-reported and unaudited:** a villa in Blender from one sketch and a room
schedule, **under 15 minutes** and roughly **a tenth of a weekly allowance** at low
reasoning; the same model taken into **Unreal via MCP, ~2 hours over two sessions**;
a third party's game assets via Blender MCP, **~8 hours, weekly allowance falling
from 83 to 44 per cent**. **→ The RATIO is the durable part: headless generation is
cheap; MCP-driven interactive work is roughly an order of magnitude dearer in both
time and tokens.** [source: [[_Sources/YT_SsBLhNgqTqQ_mcp_versus_headless_scripting_and_measured_accuracy|YT_SsBLhNgqTqQ]]]

## 5. Operating an agent-driven CAD — three practical rules

- **⚠️⚠️ Scope execution permission to the SESSION, not permanently.** Asked to run a Ruby script, the operator grants it **for that conversation only**: *"I don't like to give like blanket permission for things like that just cuz I'm still a little bit paranoid about this kind of going outside of the guard rails."* **An MCP server for a CAD application is, by construction, arbitrary code execution against your documents.** ⚠️ **The same argument applies to agents running against this repository, which holds the canonical data and the gates.**
  - **⚠️⚠️ THIRD ARRIVAL, and the first to name a FAILING DEFAULT: the desktop
    client installs with FULL ACCESS ENABLED.** *"For some reason when this gets
    installed, it gets installed with full access turned on and I don't love
    that"* — and he turns it off by hand, keeping manual approvals. **→ Check that
    setting after installing rather than assuming it is off.** His own summary is
    worth keeping verbatim: *"the permissions and approval settings can limit that
    access, but they don't eliminate the risk."* ⚠️⚠️ **Set directly against the
    other presenter in the same batch, who clicks "approve for me" so it stops
    asking. Two practitioners, the same week, opposite choices.** [source: [[_Sources/YT_pkFnSQ9Bapg_archivlogs_gpt6_revit_mcp_planning_reversal|YT_pkFnSQ9Bapg]]]
- **⚠️ The connection drops, routinely.** *"That's pretty common that it'll drop the connection. And then you need to rerun this."* **The closed loop is not only slow and visually verified — it is also not durable.**
- **⚠️⚠️ Ask the clarifying questions FIRST, and the silently-supplied-values hazard becomes a recorded assumption.** Prompted with *"ask me any questions you have before getting started"*, the agent asked: is there an overall measurement? exterior only? include surroundings? new document? **The operator answered "no — you can estimate from the images", accepting estimation deliberately and with open eyes.**
  **→ The hazard recorded in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §7 is not that an agent estimates — it is that it estimates SILENTLY. The interview round is a mitigation for that rule, not merely a prompt-quality trick.**
- **Judge generated geometry by its CONSTRUCTION, not its silhouette** — *"it's better to look at the hidden geometry… it can give you an idea of how this is created."* A shape that looks right and is built wrong fails at the next edit.
- **⚠️ When comparing two agents on a generative task, hold the prompt AND the clarification round constant, and verify the clarifications matched** before comparing outputs. A different question asked is a different task performed.

## 6. ⚠️⚠️ "Computer Use" is not a fourth architecture — it collapses into §4

**A Korean test drove AutoCAD with NO MCP connection at all** — *«제가 MCP 연결을 하지 않았어요»* — the application simply open on screen, a permission dialogue accepted, and the GUI visibly flickering as the agent operated it. **On the surface, a fourth architecture. It is not, and the presenter says so himself:**

> *"Showing it one by one in Computer Use is actually **FOR THE HUMAN**. It just drew the whole drawing in one shot, because it already had all the information."*

**What it actually did**: read the PDF (converting it to PNG first), planned the whole drawing, **wrote Python scripts — over 4,000 lines** — and executed them. On the second run it simply called the script it had already written and produced the drawing in one shot, with no stepping at all.

> **→ The GUI performance is a progress rendering for an observer, not the mechanism. Computer Use, here, IS tool-driving with code execution.** Record it as §4, not as a new row.

- **⚠️ Its drawing ORDER matched human practice** — plan, lines, text, **dimensions last** — and it emitted a `geometry.json` alongside, a structured intermediate rather than only geometry. [source: [[_Sources/YT_-FsHQEYldnQ_grasshopperpp_computer_use_autocad|-FsHQEYldnQ]]]

### ⚠️⚠️ "Complete" was printed over a half-finished drawing

**The first run hit a token/credit limit mid-execution — after already printing a COMPLETE message**, leaving a visibly unfinished drawing. **A self-reported success that was not one; `Validator_Design_Discipline.md`'s "printing is not checking", demonstrated.**

- **⚠️ The recovery is the useful half: because the PLAN and the SCRIPTS were on disk, the work was resumable.** *"The plan was always there; only execution lost its credits."* **→ An agent that plans into FILES can be resumed; one that plans into its context window cannot.**

## 7. ⚠️⚠️ Placed, but not associated — the defect that spans tools

**A Revit/Dynamo test placed beams correctly along a grid — main on the numeric axes, secondary on the lettered, marks applied — and then: *«если я его смещу, балки останутся на месте»* — MOVE THE GRID AND THE BEAMS STAY WHERE THEY ARE.** They were placed, not constrained.

> **→ GENERATED GEOMETRY IS PLACED, NOT ASSOCIATED. The parametric RELATIONSHIP is absent unless explicitly demanded.**
>
> **⚠️ Same defect class as a second model OVERRIDING a dimension's text so it disagreed with the geometry** — *«치수를 오버라이트해서 실제 치수랑 다르다»* — **a drawing that lies.** This vault already established the mechanism that permits it: a dimension's text is an arbitrary override that nothing computes from. **In both cases the output LOOKS right and nothing holds it right.**
>
> **→ The question to ask of generated geometry is not "is it correct?" but "is it correct BECAUSE OF anything?"** ⚠️ **A contrast worth keeping: a purpose-built parametric tool reportedly DOES maintain this** — drag the boundary and interior walls adapt. **The difference is not intelligence; it is whether anything maintains the constraint.**

### ⚠️ The complexity cliff, located precisely

| Task | Result |
| :--- | :--- |
| Parametric steel plate **with four holes** | **Failed** — constraints not satisfied |
| Corrected retry, same task | **Failed again, with MORE warnings** |
| The same plate **without holes** | **Succeeded** — real parametric family, and the operator **drove each parameter and confirmed it worked** |

**→ The boundary is not "simple versus complex" in any vague sense — it is where constraints must be solved against each other. And iteration did not converge: the second attempt was worse.** ⚠️ **A third source frames the same behaviour as *"the longer and more complex the project is, the more it kind of like drifts."*** [sources: [[_Sources/YT_JCCEW6797yw_bimdlyachaynikov_revit_dynamo_families_audit|JCCEW6797yw]], [[_Sources/YT_T45kiCGvCQs_aiessentials_task_vs_profession|T45kiCGvCQs]], [[_Sources/YT_ZS_tnIN0zoA_archmaster_seven_tools_roundup|ZS_tnIN0zoA]]]

## 8. ⚠️⚠️ Revision — the open question, answered

**[[18_Digital_Toolchain/analysis/Agent_Connected_CAD|§1]] recorded that the file-generating path REGENERATES the whole model on any change. A practitioner who has now done it both ways states the difference:**

| | **Ruby console, no MCP** | **MCP** |
| :--- | :--- | :--- |
| Granularity | **Coarse** — *"just say make Villa Savoye and wait"* | **Fine** — *«하나하나 명령을 해줄 수가 있어요»* |
| Revision | Regenerate everything | **"Modify just that window" — or "change all 100 windows"** |

- **⚠️⚠️ The method that worked is simple enough to copy: an ANNOTATED SCREENSHOT plus a plain-language instruction.** He screenshots the elevation, highlights the wrong door, and writes *"the door at the entrance is modelled wrong, fix it to match the drawing."* **It fixed it, in about 7 minutes.** No prompt engineering; **the annotation carries the location.**
- **His conclusion is the practical one**: small fiddly corrections are **inevitable** — a human modeller makes them too, and an agent makes more — **and the MCP path means you simply instruct each fix.**
- **⚠️ MCP setup is genuinely hard** (GitHub download, a Python tool, PowerShell verification, registration, restart) — **and he delegated the installation to the model itself: 7 min 16 s, installed and verified.** **Setup friction is itself a delegable task.**

### ⚠️⚠️ Two triage tests this batch established

1. **A FAMOUS BUILDING IS NOT A TEST OF DRAWING COMPREHENSION.** A Villa Savoye demo worked because *«유명한 건물이기 때문에 이미 도면 같은 게 온라인상에 많이 올라와 있어요»* — the model **found the drawings online itself** and inferred dimensions from them. **Retrieval, not reading. The first question of any "AI modelled this building" demo is whether the building is famous.**
2. **⚠️ The models generate their own verification artefacts** — one created a separate "plan review" file to check its geometry; another **set up section cuts and kept checking itself mid-process.** **Two models, two applications, same emergent behaviour.** ⚠️ **But it does not follow that the check is sound: the first one printed "complete" over a half-finished drawing.** **A self-generated check is not an independent one.**

**⚠️ And a permission contrast worth recording**: §5 records an operator scoping execution rights **to the session**; this batch has one clicking **«항상 허용» — ALWAYS ALLOW**. **The safer discipline is the first.** [sources: [[_Sources/YT_Qh9xgjd38VI_feeeld_drawings_to_sketchup_with_revision|Qh9xgjd38VI]], [[_Sources/YT_26UFabH--JU_feeeld_villa_savoye_ruby_console|26UFabH--JU]]]

## Source Notes

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [[_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp\|vmVvpKSSxWE]] | The Revit integration path; the modelling-accelerator-not-planner finding and its three named failures | 4 (partial) |
| [[_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp\|6trAkQY5_kc]] | The closed-loop architecture; the screenshot-versus-text feedback trade-off | 3 (partial) |
| [[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|sujS9Mgveo4]] | The open-loop contrast, and its measured fidelity — see [[18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation\|AI for Concept and Visualisation]] §3 | 2 |
| [[_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling\|YT_HOjQiiHJ714]] (2026-09-11) | The original file-generator finding this page refines, and the silently-supplied-values rule | — |

**⚠️ Both new sources are channel-growth vehicles** (a lead-magnet PDF, subscribe requests, a "the results scared me" framing). **No capability verdict from either is routed.**

## ⚠️⚠️ Live connection vs generated script — a genuine practitioner disagreement (added 2026-09-18)

Two sources published a day apart take opposite routes, and **neither measures the cost that divides them.**

### Perspectives

**Степан Огурцов** (`YT_1WakaBxLkVg`, 2026-09-16) — a practising 3D designer modelling a real apartment from a drawing — names the live connection as the common error:

> *«Здесь многие ошибаются, берут прямое подключение и сжигают кучу токенов, кучу ресурсов в нейро. Платят за это очень много. А со скетчапом можно работать с помощью Ruby, и это гораздо дешевле.»*

He has the model **emit a Ruby script** which he pastes into SketchUp's console.

**Justin, The AI Essentials** (`YT_BFImll1TqYE`, 2026-09-17) — a tutorial — installs a Blender MCP add-on and lets Claude or ChatGPT **execute code in Blender live**, approving permissions per action.

### Common ground

Both are generating and running code either way. The difference is **who holds the loop**: a script the human pastes and can read first, or a connection the model drives with per-action approval.

### ⚠️ Where the evidence runs out

**Огурцов asserts the live route is much more expensive and shows no figures. Justin never mentions cost.** The disagreement is therefore unresolved on evidence, and anyone repeating "MCP is expensive" is repeating one practitioner's assertion.

### Your priority

**This project already takes the script side, and for a reason neither source gives: a generated artefact can be GATED.** `data/canonical` → compiler → IFC/DXF is checkable by `check_dxf_closure.py` and the IFC gates precisely because the output is a file, not a live mutation. A model driving Blender directly leaves nothing to diff. **The cost argument is a bonus, not the reason.**

⚠️ **And Justin's security section is the durable half of his video** regardless of the route: the ChatGPT desktop app ships with **full computer access ON by default**, which he recommends turning off; prefer *allow once* over *allow for this conversation*; consider a VM. That applies to any agent-connected CAD setup, including this one.

## ⚠️⚠️ The dimensions came out right and the MEANING came out wrong (added 2026-09-18)

Огурцов's model, generated from a supplied drawing, **checked out dimensionally** — he spot-measured 3261 and 4673 against the drawing and both matched — and then:

> *«Он почему-то решил, что здесь лоджия, а здесь короб с коммуникациями.»*

**It swapped a services duct and a лоджия**, and merged windows into the wrong wall because *«видимо, понял, что это лоджия на своё усмотрение»* — it decided on its own initiative what the space was.

> **This is the single most relevant observation in the vault for this project's architecture.** Geometry can be millimetre-correct while the identity attached to it is wrong, and **no dimensional check catches that.** It is the argument for canonical-data-first: identity, class and adjacency are AUTHORED and gated, and geometry is compiled from them — rather than identity being inferred from geometry by anything, human or model.

**His governing warning belongs next to it:**

> *«Вы должны понимать, что происходит… чтобы видеть косяки нейросетки, которые всплывают внезапно, а нейросеть их косяками-то и не считает.»*
>
> *«Если бы экспертности в области скетчапа у меня не было, то я бы и не смог найти выход из этой проблемы. Просто плюнул бы, и результат был бы потерян.»*

**The model does not consider its mistakes mistakes** — so the check has to be external, and the person has to know enough to write it. That is the same conclusion `00_Master/Validator_Design_Discipline.md` reached from eleven review rounds inside this project, arrived at independently by a practitioner outside it.

### What he does by hand, after

Windows, sills, doors, radiators and textures — *«Дальше уже работаю вручную»*. His prompt converged on **subtraction**: *«Не делай пол, не делай окна, не делай двери. Нужна только геометрия стен и проёмов внутри них.»* Walls and openings only, as one solid group.
