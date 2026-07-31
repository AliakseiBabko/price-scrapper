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
7. **Source Notes** — list the archived sources (and, where they exist, the richer extraction notes in `11_Budget_and_Planning/_supporting/knowledge/sources/`) this page's content is built from, so a claim can be traced back to evidence.

## Rules carried over from the `11_Budget_and_Planning` pipeline

These pages should follow the same discipline already established for `Budgeting_Guide.md`, even though they're a different destination:

- **Stay brand-name-free by default.** Describe functional tiers/categories (e.g. "budget inverter models" vs. "premium models with lower noise and more self-diagnostics") rather than naming specific commercial brands, unless a brand name is itself the durable fact (rare). Several sources feeding this content are self-promotional company channels — see each source's own advertising notes in the `11_Budget_and_Planning` intermediate store for context before pulling a claim in here.
- **Preserve uncertainty.** If a fact came from a source tagged `unverified`, `single-account`, or with an ASR-garbled figure in the budgeting store, don't launder it into unqualified fact here — carry the same hedge (e.g. "one installer's stated rule of thumb," not "the rule").
- **No pricing without a date/currency/region caveat.** These pages are technical/practical references first; if a price figure is included at all, treat it the same way the budgeting store does (source year, currency, region stated explicitly) rather than a bare number.
- **Cite sources by archive path**, matching the existing table convention (`` `90_Archive/processed_sources/<file>.txt` ``), and additionally link the richer extraction note where one exists, since those carry the full evidence-level breakdown this folder's pages don't need to duplicate.

## Not done yet

All three pages (`HVAC_and_Ventilation.md`, `Electrical_and_Lighting.md`, `Plumbing_and_Waterproofing.md`) are now converted to this shape (last one finished 2026-07-31). No known remaining flat-table placeholders in this folder — if a new system topic is added later (e.g. a dedicated Waterproofing-only or Smart-Home page), use any of the three as the reference example.

This template also now backs `07_Bathroom/Bathroom_Guide.md` and `08_WC/WC_Guide.md` (created 2026-07-31), even though those live outside this folder — the shape (narrative sections + Quick Reference + Source Notes) is the same; only the routing rule below determines which page a given fact lands on.

This template also now backs `13_Surfaces_and_Finishes/Doors_and_Trim.md` (created 2026-07-31), synthesized from the two Doors/Trim Durable Facts batches in the budgeting knowledge store (8 single-channel Zemstandart sources + 7 independent-channel sources). Same shape; also carries an explicit top-of-page corroboration note since most of its first-batch content traces to one channel, following the pattern established in `07_Bathroom/Bathroom_Guide.md`'s own top-of-page note.

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

Found a smaller version of the same gap that motivated this template in the first place: several genuinely useful facts (recessed-lighting/dimmer/switch-count guidance from WITALT, two-way-switch and bedroom-lighting rules from Prolife Invest) existed only in their source extraction notes under `11_Budget_and_Planning/_supporting/knowledge/sources/` — never promoted into the budgeting store's own Durable Facts/Rules sections, and therefore invisible to anyone not reading each extraction note individually. They're now in this page.

## Note from converting Plumbing_and_Waterproofing.md

Same pattern confirmed a second time: the toilet-first sequencing rule, the sink-drainage-slope rule, the full zashivka/venshakhta breakdown, and — most notably — the heated-towel-rail-as-mold-prevention fact all existed only in `YT_QHl1YEHMfgE_doma_minska_severny_bereg_ep2_layout.md` and were absent from the main budgeting store's Durable Facts/Rules sections. This is now the second folder-conversion in a row where extraction-note content outran what got promoted to the store. Worth treating this as a standing pipeline gap rather than a one-off — when a new source note is written, its facts should be checked against the store (and, going forward, against these `12_Engineering_and_Systems` pages too) before being considered "captured," not just filed in the source note itself.
