---
source_type: video transcript (practising architect, full-time at a firm, testing a newer model against Revit over MCP - a direct re-run of his own earlier test)
source_url: https://www.youtube.com/watch?v=pkFnSQ9Bapg
video_id: pkFnSQ9Bapg
covers_also: 9DnrSvAYKsI
transcript_file: _Archive/processed_sources/20260916_archivlogs_gpt6_revit_mcp_planning_reversal_f91f3e58.txt
transcript_file_pt2: _Archive/processed_sources/20260916_toolchain_sketchup_mcp_setup_af4dbf4b.txt
fetched: 2026-09-16 via youtube-transcript-api (en-US MANUAL track for pt1, en for pt2)
upload_date: 2026-09-15 (pkFnSQ9Bapg); 2026-09-11 (9DnrSvAYKsI) - both from yt-dlp sidecars, --fetch-upload-date, actually run
channel: Archi Vlogs (pkFnSQ9Bapg); The AI Essentials / Justin (9DnrSvAYKsI)
source_title: "GPT-6 Astra + Revit MCP: AI Just Changed Modelling Forever" (+ "How to Connect AI to SketchUp (Complete MCP Setup Tutorial)")
language: ⚠️ en - ORIGINAL language. Standing rule 1 is about not fetching TRANSLATED captions; these sources are natively English and were fetched as such after a yt-dlp language probe.
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / Agent-Connected CAD`)
fact_yield: 19
promotional_ratio: ⚠️⚠️ HIGH on pt1 - repeated like-and-subscribe appeals, a "this scared me" framing, and an explicit "Claude messed up big time" comparison. The OBSERVATIONS are usable; the verdict is not.
corroborates_existing: partly
contradicts_existing: ⚠️⚠️ YES - it reverses this vault's headline finding on agent-connected CAD, from the SAME observer
region: n/a - software capability, not priced or located
---

# Source Note - ⚠️⚠️ "It can't plan" no longer holds — the same architect, a newer model (YouTube pkFnSQ9Bapg +1)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none)

⚠️ **Both channels are already in this vault** — Archi Vlogs supplied `vmVvpKSSxWE`, the source of the finding this note revises, and The AI Essentials supplied `T45kiCGvCQs`. **Neither is independent of its own earlier video.**

## ⚠️⚠️ 1. THE REVERSAL — and it matters because it is the same person re-running his own test

**[[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]] §3 carries this vault's clearest statement on the subject, quoted from this presenter's earlier video:**

> ***"It can't plan right now. What it can do is basically create a model from your existing floor plans."***

**Everything that succeeded there was transcription; everything that failed was spatial logic — a plan closed on all sides, a forgotten wall, a bedroom door placed outside the building.**

**Here is the same architect, a newer model, and a deliberately harder brief:** a 40 × 50 ft site, **a four-bedroom house**, one parking space, two washrooms, a small courtyard, front setback 10 ft, sides 4 ft, rear 6 ft. His own framing: *"I wouldn't do this to any intern."*

**What came back, in about 14 minutes:**

- **A two-level plan honouring all three setbacks**, with an ~8 × 8 ft courtyard, parking at ground level, and **a staircase in two flights of nine risers** that he checks and calls *"perfect… the riser is touching where it should."*
- **Sections, elevations and sheets, generated unprompted.**
- **Furniture modelled in place** because the project had no furniture families loaded — including **a car, correctly categorised as parking.**
- **⚠️⚠️ Self-correction mid-run, reported by the model itself**: *"the first visual check caught dining chairs encroaching on the staircase approach — I am moving the dining seating forward."*

> **→ ⚠️⚠️ THE TRANSCRIPTION-SUCCEEDS / PLANNING-FAILS SPLIT, WHICH THIS VAULT RECORDS AS HOLDING ACROSS FOUR INDEPENDENT SOURCES, NO LONGER HOLDS CLEANLY.** **This is a spatial-logic task performed from a text brief with no plan supplied, and the result is coherent enough that a practising architect checks the stair and accepts it.**

## ⚠️⚠️ 2. BUT READ WHAT HE ALSO SAYS — the failures are still spatial, just smaller

**In his own commentary, while praising it:**

- **⚠️ Rooms were not named at all** — *"it hasn't named any of the rooms… I believe one of them is a bedroom, this was supposed to be a kitchen, probably this can be a washroom."* **He is GUESSING at the function of spaces in a plan he commissioned.**
- **⚠️ A window looks into a space rather than out** — *"it has messed up a little bit with the window inside this space, because it is again looking inside a space."*
- **⚠️ Unexplained leftover area** — *"it has left a lot of space over here which I don't know what it will be used for."*
- **Two railing warnings**, which he excuses as a problem human architects also hit.
- **The project title was inherited from an unrelated earlier prompt.**

> **→ ⚠️⚠️ SO THE HONEST FORM OF THE REVISION IS NARROWER THAN THE VIDEO'S TITLE: the model has moved from "cannot plan" to "produces a plausible massing and circulation with unresolved room semantics."** **Naming a room is the cheapest part of planning and it did not do it; deciding what a leftover area is for is planning, and it did not do that either.**
>
> **→ The vault's underlying rule survives intact and is arguably reinforced: [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|an agent silently supplies the values you did not specify]].** **Here it supplied room boundaries it could not name and a window orientation nobody asked for. The failure mode did not change; only its granularity did.**

## ⚠️ 3. Weighting — why this is recorded as a revision and not as a capability verdict

- **⚠️⚠️ Same observer, same channel, no independent replication.** The vault's existing finding and this revision come from one person.
- **⚠️⚠️ Explicitly promotional**: repeated like-and-subscribe appeals mid-test, a *"I'll be really scared for our industry"* framing, and a head-to-head claim — *"Claude couldn't do this kind of job… it messed up big time"* — **with no controlled comparison shown.** ⚠️ **This vault already holds the rule that a cross-agent comparison requires the prompt AND the clarification round held constant; none of that is demonstrated here. The comparative claim is NOT carried.**
- **⚠️ A famous-building check does not apply** (the brief is a generic house, not a known work), **so retrieval is not the explanation here** — which is the one thing that makes the result more interesting than the Villa Savoye demos this vault already discounts.
- **⚠️⚠️ He accepted blanket permission**: *"in the settings just click on approve for me… so it won't keep asking you questions."* **That is the opposite of the session-scoped discipline this vault records, and the THIRD instance of the permission contrast.**

## ⚠️⚠️ 4. What an MCP actually is, stated plainly — and the two-piece shape

**From the SketchUp tutorial, the clearest definition either channel gives:**

> *"MCP stands for Model Context Protocol. This is basically just the standard way that AI tools communicate with systems where data live, or different tools… this is how your AI talks to SketchUp."*

**And the architecture, which is the part worth keeping:**

| Piece | Where it runs | What it does |
| :--- | :--- | :--- |
| **The extension** | Inside the CAD application | Exposes the application's **own scripting API and built-in tools** to the outside |
| **The connector** | In the AI desktop client | Translates natural language into commands the extension can execute |

- **⚠️⚠️ It grants two distinct powers, and conflating them is a mistake**: the agent can **execute arbitrary code** (Ruby, in SketchUp's console) **and** it can **call the application's existing tools.** **The second is [[18_Digital_Toolchain/analysis/Agent_Connected_CAD|the tool-driving architecture]] this vault already records as strictly better than emitting raw geometry.**
- **It can take screenshots and see what it did** — the closed loop, confirmed again.
- **⚠️ Requires the DESKTOP client** (Claude Desktop or ChatGPT with Codex); the web version cannot do it. **No additional licence cost — it consumes subscription tokens, "a lot more quickly."**
- **⚠️ Named as valuable for EXTENSION DEVELOPMENT as much as modelling** — write a script, run it, see the result, iterate, *"without you having to go in and double-check and tell it what it did every time."*

## ⚠️⚠️ 5. Security, stated carefully by one presenter — and it is a third arrival

**He stops the tutorial to say it:**

> *"They can access files and execute code locally on your computer depending on the permissions you give them… this particular MCP also allows the AI to execute Ruby code directly inside of SketchUp. That's what makes it capable of creating and modifying models. But it also means you should only install code from sources you trust and review commands or permission requests before approving them. The permissions and approval settings can limit that access, but they don't eliminate the risk."*

- **⚠️⚠️ AND A CONCRETE DEFAULT WORTH KNOWING: the client installs with FULL ACCESS ENABLED.** *"For some reason when this gets installed, it gets installed with full access turned on and I don't love that."* **He turns it off manually.** **→ A default that fails open. Check it after install rather than assuming.**
- He keeps **manual approvals** on, while noting he may relent as requests become routine.

> **→ THIRD INDEPENDENT ARRIVAL at the permission-scoping discipline this vault records** — and the first to name the failing default. ⚠️ **Set directly against §3's "approve for me" in the other video: two practitioners, same week, opposite choices.**

## ⚠️ 6. Two operational details that corroborate existing entries

- **The connection drops** — *"occasionally this does have issues with disconnecting… you can just stop the server and restart it."* **Third arrival; the closed loop is not durable.**
- **⚠️ Setup is delegable to the agent itself, and both presenters do it.** One pastes a repo link and says *"install BIM-right Revit MCP"*; the other repeatedly says *"the easier way is to just say, can you run step seven for me"*, letting Codex create the Python environment, locate `uv`, find the client's install path and register the server. **→ Corroborates the existing finding that setup friction is itself a delegable task — now from two tools.**

## Routing

- §1, §2, §3 → [[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]] §3, as a dated revision of the "it can't plan" finding
- §4 → same page, into the architecture section
- §5, §6 → same page, into the operating rules

## What was NOT taken

- **Install steps, product versions, port numbers and repository links** — per that page's standing policy, they date within months and none of this is this project's toolchain.
- **The head-to-head model comparison** (§3) — no controlled prompt, so not carried.
- The like-and-subscribe appeals and the "changed modelling forever" framing.
- **Nothing routed to `16_Legal_and_Regulations/`** — no regulatory claim is made.
