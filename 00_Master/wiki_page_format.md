# 12_Engineering_and_Systems — Wiki Page Format

> [!NOTE]
> Not a final agreed format — a working template, revisit as pages get built out. Written 2026-07-31 when converting `HVAC_and_Ventilation.md` from a flat Do's/Don'ts table into a full wiki page, at the user's explicit direction that the system pages in this folder ("placeholders" per the user) should read like `11_Budget_and_Planning/Budgeting_Guide.md` or `Renovation_Sequence.md`, not stay as bare rule tables.

## Why this exists

`Electrical_and_Lighting.md`, `HVAC_and_Ventilation.md`, and `Plumbing_and_Waterproofing.md` currently exist as flat "Rule | Applies To | Reason/Risk | Source" tables. That's useful as a quick-reference layer, but it isn't a page a reader can use to actually *understand* the system — no explanation of how things work, why a rule exists, or how to size/select equipment. The goal is to bring these up to the same standard as the two pages that already work well: a real narrative/structured wiki page, with the rule table demoted to one section within it (a "Quick Reference"), not the whole page.

## Suggested section shape

Not rigid — adapt per system, since electrical, HVAC, and plumbing don't have identical concerns. But default to something like:

1. **Purpose** — one short paragraph: what this page covers and who it's for.
2. **Key Concepts / System Types** — the vocabulary and system categories a reader needs before the rest of the page makes sense (e.g. for HVAC: split-system vs. other AC types, inverter vs. non-inverter, fresh-air breathers vs. full mechanical ventilation).
3. **Core Technical Sections** — the real content, organized by sub-topic (placement rules, drainage/mechanism explanations, sizing/selection guidance, a critical safety distinction, etc.) — however many sections make sense for that system, not forced into a fixed count.
4. **Common Mistakes** — durable, checkable failure modes (not vague warnings).
5. **Buying/Practical Guidance** — timing, warranty structure, vendor selection — where the source material supports it.
6. **Quick Reference — Do's and Don'ts** — the existing table format, kept as-is where rows are still accurate, extended with new rows as more sources are processed. This is a summary/lookup aid, not the primary content anymore.
7. **Source Notes** — list the archived sources (and, where they exist, the richer extraction notes in `_Sources/`) this page's content is built from, so a claim can be traced back to evidence.

### Inline attribution when it can be confirmed — never a content-free "unconfirmed" note (corrected 2026-08-20)

Every claim or bullet in a Core Technical Section should name the actual
channel or practitioner inline in the sentence itself, whether the claim is
an agreement, a disagreement, or a single-source recommendation, whenever
the cited extraction note's `channel:` field establishes the source
confidently.

- **Acceptable:** `Kruglov/Ontario recommends a minimum 80×90 cm shower cabin because ... [source: [[...]]]`.
- **Not acceptable:** `A shower cabin should be at least 80×90 cm. [source: [[...]]]` (no attribution at all, confirmable or not).

**Correction, per direct user feedback (2026-08-20):** the original version
of this rule required writing `attribution: unconfirmed — <reason>` whenever
a channel couldn't be confirmed. That produced hundreds of claims prefixed
with bare boilerplate ("the cited source is not channel-isolated") that adds
**zero usable information** — it doesn't help the reader trace the claim,
weigh the source, or do anything they couldn't already do. **This pattern is
retired — do not write it going forward, and it is being removed from
already-edited pages.**

The only two acceptable states for a claim now are:

1. **A real named channel/practitioner**, inline in the sentence, exactly as
   the "Acceptable" example above — when the cited note's `channel:` field
   supports it.
2. **The claim's own existing citation stays as the only marker**, with
   nothing added — when a channel can't be confirmed. Do **not** insert
   `attribution: unconfirmed` prose. If the claim doesn't already carry a
   direct, click-through link to its specific source (the extraction note or
   archived transcript it came from — not just a page-level Source Notes
   list somewhere else), **add that link directly at the claim** so the
   reader can always go verify/investigate for themselves, even without a
   named channel. A link has real value; a prose explanation of why there
   isn't a name does not.

Never guess a channel to avoid state 2. The separate **Perspectives on
Record** block remains the place to surface genuine source disagreements; it
is unaffected by this correction.

## Rules carried over from the `11_Budget_and_Planning` pipeline

These pages should follow the same discipline already established for `Budgeting_Guide.md`, even though they're a different destination:

- **Stay brand-name-free by default.** Describe functional tiers/categories (e.g. "budget inverter models" vs. "premium models with lower noise and more self-diagnostics") rather than naming specific commercial brands, unless a brand name is itself the durable fact (rare). Several sources feeding this content are self-promotional company channels — see each source's own advertising notes in the `11_Budget_and_Planning` intermediate store for context before pulling a claim in here.
- **Preserve uncertainty.** If a fact came from a source tagged `unverified`, `single-account`, or with an ASR-garbled figure in the budgeting store, don't launder it into unqualified fact here — carry the same hedge (e.g. "one installer's stated rule of thumb," not "the rule").
- **No pricing without a date/currency/region caveat.** These pages are technical/practical references first; if a price figure is included at all, treat it the same way the budgeting store does (source year, currency, region stated explicitly) rather than a bare number.
- **Cite sources by archive path**, matching the existing table convention (`` `_Archive/processed_sources/<file>.txt` ``), and additionally link the richer extraction note where one exists, since those carry the full evidence-level breakdown this folder's pages don't need to duplicate.

## Layered convention: split a page's narrative into dedicated detail pages once it gets big (added 2026-08-17)

Per explicit user direction, evolving the "Suggested section shape" above once a page's **Core Technical Sections** step grows large enough to be hard to scan (`07_Bathroom/Bathroom_Guide.md` had reached 397 lines before this change — the trigger case). The single-page shape above still works fine for a page that's still small; this is what to do once it isn't:

- **Keep the single guide page, but shrink each Core Technical Section to a real middle layer, not a stub.** The first pass on `07_Bathroom` over-corrected to 2-5 generic bullets + a link per section — direct user feedback the same day: too thin, "just a link" gives nothing to actually form an opinion from. **The right target**: state the leading recommendation(s) *and the reasoning behind them* (why this material/approach over the alternatives), including a brief comparison where sources differ — enough that a reader can understand the tradeoff and make a call without clicking through, while the linked `analysis/` page still carries the exhaustive, fully-sourced, every-number version. In practice this lands around 5-10 lines of real prose per section, not 2-3 bullet fragments. A section genuinely short enough already (one paragraph, no real depth — e.g. Bathroom's Ceilings section) can stay inline as-is; splitting it out would just be an extra click for no benefit.
- **Retire a flat "quick-reference Do's/Don'ts" table entirely rather than keeping it (even consolidated) as a separate section** — also direct user feedback on the same pilot: a bare "do X / don't Y" row with no explanation of *why* was called out as uninformative regardless of whether it lives in its own file or a page section. Fold that reasoning into the guide's own per-section prose (above) instead. If a fact doesn't yet have a "why" behind it worth writing a sentence for, that's a signal the fact itself may not be worth including yet, not that it belongs in a bare table row.
- **When two named sources genuinely disagree** (not just "different levels of detail," an actual contradiction on what to do), don't bury it as a footnote inside a bigger section. Give it a **Perspectives / Common Ground / Your Priority** block on its dedicated detail page: a small table listing each source's position and stated reasoning, a "Common Ground" note on what isn't actually in dispute, and a "Your Priority" line capturing the user's own decision (or explicitly "not yet decided," plus the deciding factor both sources point to). Surface every such disagreement up front in the guide page too, in a short "Perspectives on Record" section near the top — a reader shouldn't have to reach the relevant section mid-page to discover a decision is still open. See `07_Bathroom/Bathroom_Guide.md` and its `analysis/Bathtub_and_Shower.md` (toe-kick niche) / `analysis/Heated_Floor_and_Thermostat.md` (thermostat height) for the worked pattern.
- **Cross-references by numbered section (`§N`) are fragile once content is split across files** — a detail page doesn't have the guide's own section numbers, and the guide's own numbering shifts as sections are added/removed. Prefer linking by page name (and a short in-line description of what's there) over `§N`, both from other pages and within a page's own Source Notes. This is also why the "Process note: plan the section TOC before writing" note below already warns against strict integer numbering for an open-ended page — the same numbering-fragility problem, one level up.
- **This is a restructuring convention, not a rewrite-from-scratch instruction** — move/reorganize existing prose into the new files rather than re-deriving content, so no fact gets lost or silently altered in the split. Update every inbound link that named the old single page with a `§N` anchor (check via a repo-wide search on the old page's filename) to point at the new, correct detail page instead of leaving a stale section number.
- **Move both the Source Notes section (step 7 above) and the page's own Change Log to their own dedicated pages, not inline on the guide page** — direct user feedback on the Bathroom pilot, given for Source Notes first and then, on the same reasoning, extended by the user to Change Log too: both are purely technical, indefinitely-growing sections (archive-path citations; a running edit history) that a reader doesn't want on the page they're actually reading. Leave a one-line pointer in the guide's own Source Notes / Change Log heading (e.g. "moved to its own page — [[.../Source_Notes|Source Notes]]") rather than deleting the heading outright, so the page's section list stays predictable. This supersedes step 7's "list the archived sources..." instruction for any page that's gone through this layered conversion; a page still on the original single-page shape keeps both sections inline as before, until it's converted. **Apply both moves together when converting a new page** — don't wait for the same feedback to arrive twice.
- **Rollout status**: piloted on `07_Bathroom` (2026-08-17), approved by the user, who then explicitly directed using it as the blueprint for all other folders in the vault. Converted, same day, in size order: `Plumbing_and_Waterproofing.md` (355→108 lines, 12 pages), `Doors_and_Trim.md` (239→78 lines, 8 pages), `Electrical_and_Lighting.md` (197→74 lines, 8 pages), `HVAC_and_Ventilation.md` (159→51 lines, 5 pages), `Wardrobes_and_Storage.md` (141→56 lines, 6 pages — this folder also had no `_Index.md` at all, now created as `14_Furniture/Furniture_Index.md`). This completes every page that was over ~130 lines. Confirmed the pattern generalizes cleanly across content types: room-decision content (Bathroom), dense engineering-reference content (Plumbing/Electrical/HVAC), and a self-contained furniture-technique page (Wardrobes) all converted without needing to adapt the shape itself.
- **Remaining, lower priority**: `08_WC/WC_Guide.md` (96 lines) + its separate `analysis/Dos_and_Donts.md` (22 lines) has the same two-file-overlap problem Bathroom had, but at much smaller scale — worth the same treatment eventually, just not urgent. `09_Laundry_Room`, `03_Kitchen` (mostly empty placeholders plus a thin Dos_and_Donts table), and `10_Balcony` (78 lines of narrative crammed directly into `Balcony_Index.md`, no separate Guide) are thinner still — revisit once they have more source material, rather than forcing the multi-page structure on content that doesn't yet need splitting. Pure-placeholder room folders (Entrance, Hallway, Living/Dining, Kids Room, Small Bedroom) need no conversion at all until they have real content. `11_Budget_and_Planning` and `15_Appliances` already have their own comparable tiered structures and are out of scope for this conversion.

### This is now the default shape for new/growing content, not just a retrofit (added 2026-08-17)

Per explicit user direction: once a full rollout confirmed the pattern works, the layered shape stops being something applied only when an existing page has already grown unwieldy — it's now the standard to write toward from the first source onward. Concretely:

- **Creating a wiki page for a topic with no existing page yet** (e.g. a future Windows page, or filling in `09_Laundry_Room`/`03_Kitchen`/`10_Balcony` once they have enough sources): decide the shape by whether the topic naturally decomposes into several distinct sub-decisions, not by line count alone. A topic that's genuinely one coherent narrative (comparable to Bathroom's short Ceilings section) is fine as a single small page using the plain "Suggested section shape" above — don't pre-split a page that has nothing to split yet. A topic that already spans multiple distinct sub-decisions (sizing rules, material selection, a construction technique, a buying guide — the way every converted page above did) should start directly as compact-Guide-plus-`analysis/`-pages, even while each individual page is still short. **Source Notes and Change Log go into their own pages from the very first source**, not just once a page crosses some size trigger — there's no reason to defer a move that costs nothing to do early and saves a later retrofit.
- **Adding new source content to an existing *layered* page** (any page in the "Rollout status" list above): route the new fact to the correct `analysis/` page as full prose, and only touch the compact Guide if the new fact changes what the guide's own summary/reasoning should say — a guide-page edit should stay a sentence or two, never grow back into a multi-paragraph addition. If a genuinely new sub-decision doesn't fit any existing `analysis/` page, add a new one and a matching Guide section, rather than wedging it into an unrelated page.
- **Adding new source content to an existing *single-file* page** (WC, Laundry, Kitchen, Balcony, or a future new topic that started small): keep appending normally under the plain shape until the page's Core Technical Sections step is genuinely hard to scan or has accumulated several distinct sub-decisions — then convert it then, the same way Bathroom and Wardrobes organically crossed that line. Don't convert preemptively on a guess that a page might grow.
- **This still isn't a numeric line-count threshold** — `Wardrobes_and_Storage.md` converted at 141 lines because it already had 6 clearly separable sub-decisions, not because it crossed a specific number. Judge by topic decomposition, use line count only as a rough proxy when the decomposition itself is ambiguous.

## ⚠️ Two failure modes, not one — and the second was invisible until 2026-08-31

The convention above is about pages that get **too big**. A batch of real splits on 2026-08-31 surfaced the opposite failure, which this document had never named and `tools/check_page_sizes.py` was structurally unable to see:

**A page can be fragmented rather than oversized** — many headings with very little under each. `12_Engineering_and_Systems/analysis/Lighting_Design.md` had **26 top-level sections in 242 lines, 9 lines apiece**, because every processing batch appended its own dated heading instead of adding to an existing section. It had been flagged as "too long, split it" for weeks. **Splitting it would have made it strictly worse.** The fix is merging.

**The practical rule when routing a new fact: look for an existing section it belongs under before adding a heading.** A dated heading per batch is convenient while writing and corrosive to read, and the cost only becomes visible once a page has twenty of them.

**A second lesson from the same pass, about the checker rather than the pages.** The original thresholds (detail pages at 220 lines with 3+ sections) were never tested by actually performing a split. When three were finally done — 921, 865 and 815 lines, into eleven pages — **the flagged count went up, 31 to 35**, because the correctly-sized single-topic results (234–336 lines) tripped the same threshold their oversized parents had. **A rule that punishes a correct split gives an author no achievable target short of atomising every page into stubs**, which is exactly how the fragmentation above happens. Thresholds were recalibrated accordingly; the reasoning is in the tool's own constants block.

**So the two failure modes generate each other**, and the guidance has to hold both at once: split when a page carries several genuinely independent decisions, merge when it carries one decision cut into twenty dated slices, and treat any line-count number as the weakest of the available signals.

### Page size: a soft target, and what actually matters (added 2026-09-02, revised the same day)

**The rule is approximate size plus structural integrity. It is not a line count.**

- **~300 lines is a soft target.** Crossing it is a prompt to look at the page, not a defect. **A page at 310 lines whose structure is logical is fine — leave it alone.**
- **400 lines is a backstop**, and the only thing that fails a check. Every page this vault has found at that length turned out to be several topics sharing a file. **A reviewed exception can waive it** if the structure genuinely justifies the length.
- **The integrity test is the one that matters**, and it is in the next section: is the page organised by *topic*, or by *when facts arrived*?

> [!WARNING]
> **A brief hard 300-line ceiling was tried on 2026-09-02 and was wrong.** It made "310 lines and perfectly coherent" fail in exactly the way "878 lines of twenty appended batches" failed, which tells an author nothing and pushes toward splitting pages that should stay whole. **The owner corrected it the same day: "the question is not the exact number of lines. The question is the approximate size and the integrity."** Two of the splits made under it — four pages taken apart purely for headroom — were defensible on topic grounds but were not needed for size. **Do not split a coherent page because a number says so.**

**What the ceiling episode did get right, and why the soft target survives:** the pages that reached 878, 740 and 696 lines got there by twenty batches each appending a little, and **nobody noticed until someone looked**. A soft target is what makes someone look. That is its whole job — the looking, not the enforcing.

**So the order of questions for any page is:**

1. **Are the headings topics or dates?** Dates → merge. This is the real defect.
2. **Does the page still hold one coherent subject?** No → split on the seam between subjects.
3. **How long is it?** Only now, and only as a prompt for questions 1 and 2. **Length on its own is not a finding.**

### Both directions, and how to tell which one you need (added 2026-09-02, second pass)

**Integrity is the half that matters.** A page is balanced when its sections are organised by *topic*. It fails in two directions, and the fixes are opposites — applying the wrong one makes the page worse, not better.

**Read the headings. That is the whole diagnosis.**

| What the headings say | The page is | Do |
| :--- | :--- | :--- |
| Topics — "Mixers and Taps", "Toilets and the Hygienic Shower" | Well-formed | Nothing. Size alone is not a defect |
| Ingestion log — "… (Игорь Краснов, added 2026-09-01, Round 4)" | **FRAGMENTED** | **MERGE** under thematic parents |
| Topics, but one is enormous and independent | **OVERSIZED** | **SPLIT** on the section seam |

**The detector was rewritten on this evidence.** It had been "20+ sections averaging under 12 lines", and it fired on two pages in 273 — both only *after* a split removed the large sections masking their average. Two faults:

1. **Average section length is the wrong primary signal, because it also describes the target shape.** A compact guide — `03_Kitchen/Kitchen_Furniture.md`, 11 thematic sections in 80 lines — is indistinguishable from a fragmented page by that measure. **The old rule would have condemned exactly the structure this document asks for.**
2. It measured arithmetic when **the defect is visible in the text**. A heading that reads "(added 2026-08-24, Round 3)" records *when a fact arrived* instead of *what it is about*. That is the fragmentation itself, stated outright.

So the test is now the **proportion of headings that name a processing batch** (12+ sections, at least half dated, under 17 lines each). It found **29 fragmented pages** on the same vault where the old rule found two.

**Merging is not deleting.** `tools/split_page.py merge` groups sections under a thematic parent and **demotes the original dated heading from `##` to `###`**. Every attribution, practitioner name and date survives, one level down, and the parity check treats that single demotion as the only permitted change.

**Order matters when a page is both.** Merge first, then extract a coherent group. Splitting a fragmented page distributes the fragments across two pages and leaves you with two fragmented pages. Four pages in the 2026-09-02 second pass were both at once, and merging pushed three of them well past the soft target before the follow-up split brought them back — that sequence is correct and expected, not a mistake.

**A merge does not shrink a page.** It adds the group headings, typically 10–30 lines. Budget for that.


## Not done yet

All three pages (`HVAC_and_Ventilation.md`, `Electrical_and_Lighting.md`, `Plumbing_and_Waterproofing.md`) are now converted to this shape (last one finished 2026-07-31). No known remaining flat-table placeholders in this folder — if a new system topic is added later (e.g. a dedicated Waterproofing-only or Smart-Home page), use any of the three as the reference example.

This template also now backs `07_Bathroom/Bathroom_Guide.md` and `08_WC/WC_Guide.md` (created 2026-07-31), even though those live outside this folder — the shape (narrative sections + Quick Reference + Source Notes) is the same; only the routing rule below determines which page a given fact lands on.

This template also now backs `13_Surfaces_and_Finishes/Doors_and_Trim.md` (created 2026-07-31), synthesized from the two Doors/Trim Durable Facts batches in the budgeting knowledge store (8 single-channel Zemstandart sources + 7 independent-channel sources). Same shape; also carries an explicit top-of-page corroboration note since most of its first-batch content traces to one channel, following the pattern established in `07_Bathroom/Bathroom_Guide.md`'s own top-of-page note.

This template also now backs `14_Furniture/Wardrobes_and_Storage.md` (created 2026-08-10, per explicit user request, originally under `13_Surfaces_and_Finishes/`; moved to its own top-level `14_Furniture/` folder 2026-08-10 per explicit user request — see the knowledge store's Change Log), synthesized from the "Furniture / Built-ins: Wardrobe & Closet Design" batch in the budgeting knowledge store (9 sources, all one channel — Zemstandart/Zemsproekt). Same shape, same top-of-page corroboration note pattern. Also folds in one off-topic source's legal-recourse content (§7) that doesn't fit any other page's scope.

## Content-routing rule: which page does a fact belong on?

Established while processing a mixed batch of plumbing/bathroom/WC sources — write this down instead of re-deriving it from scratch each session:

- **`12_Engineering_and_Systems/*` (Electrical, HVAC, Plumbing)** — infrastructure that exists regardless of which room it's in: rough-in sequencing, the water-inlet/collector node, pipe/wire material selection, pressure testing, code/regulatory requirements, safety mechanisms (leak protection, water hammer, check valves). The test: would this fact still apply if the fixture layout around it changed completely? If yes, it's infrastructure.
- **`07_Bathroom/Bathroom_Guide.md`** — room-level decisions specific to a combined bathroom: layout/dimension planning, fixture *selection* (bathtub material, mixer type, shower cabin construction), tile/apron/furniture construction technique, room-specific electrical/lighting choices. The test: does this fact depend on *this room's* specific fixtures and layout, not just generic plumbing?
- **`08_WC/WC_Guide.md`** — the same kind of room-level content, but specific to a standalone WC (toilet-only room): minimum dimensions, toilet-adjacent storage cabinetry, WC-specific fixtures (urinal, bidet toilet).
- **When a fact could plausibly go on more than one page** (e.g. "install a dry-trap siphon" is infrastructure, but "route AC condensate into the bathroom specifically" is a room-level choice about *where*), split it: put the mechanism/infrastructure content on the Engineering page and cross-link a short, room-specific application note from the Bathroom/WC page, rather than duplicating the full explanation twice or arbitrarily picking one page to own it entirely.

## Corroboration rule: same channel ≠ independent source

A recurring miscalibration risk worth flagging explicitly: when several processed videos come from the **same channel/practitioner**, treating each video as a separate corroborating data point overstates confidence. A claim repeated three times by one renovation company across three different videos is still a `single-account` claim, not a 3x-corroborated one — corroboration requires a genuinely different channel/practitioner reaching the same conclusion independently, not just a different video. When a page's `single-account` tags apply to multiple sources that turn out to share a channel, say so explicitly in the page's own framing note (see `07_Bathroom/Bathroom_Guide.md`'s top-of-page note for the pattern), rather than letting the tag density silently imply more independent confirmation than actually exists.

## Process note: plan the section TOC before writing, especially for a page fed by many small sources

When a page is going to be built up incrementally from many individual sources (as happened processing a 33-video playlist into `Bathroom_Guide.md`), inserting new sections mid-stream tends to force awkward non-sequential numbering (e.g. "§7a") that then has to be cleaned up with a full-file renumbering rewrite anyway. Cheaper to sketch the expected section list upfront — even a rough one — than to patch numbering repeatedly. If a page's scope is genuinely open-ended (more sources expected indefinitely), consider non-sequential/thematic headers instead of strict integers, so future inserts never require a renumbering pass at all.

## Note from converting Electrical_and_Lighting.md

Found a smaller version of the same gap that motivated this template in the first place: several genuinely useful facts (recessed-lighting/dimmer/switch-count guidance from WITALT, two-way-switch and bedroom-lighting rules from Prolife Invest) existed only in their source extraction notes under `_Sources/` — never promoted into the budgeting store's own Durable Facts/Rules sections, and therefore invisible to anyone not reading each extraction note individually. They're now in this page.

## Note from converting Plumbing_and_Waterproofing.md

Same pattern confirmed a second time: the toilet-first sequencing rule, the sink-drainage-slope rule, the full zashivka/venshakhta breakdown, and — most notably — the heated-towel-rail-as-mold-prevention fact all existed only in `YT_QHl1YEHMfgE_doma_minska_severny_bereg_ep2_layout.md` and were absent from the main budgeting store's Durable Facts/Rules sections. This is now the second folder-conversion in a row where extraction-note content outran what got promoted to the store. Worth treating this as a standing pipeline gap rather than a one-off — when a new source note is written, its facts should be checked against the store (and, going forward, against these `12_Engineering_and_Systems` pages too) before being considered "captured," not just filed in the source note itself.
