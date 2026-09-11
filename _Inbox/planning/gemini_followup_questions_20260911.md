# Follow-up questions for Gemini — round 2 on the geometry report

**Created 2026-09-11.** Seven questions that survived a filter: **anything answerable from this repo or from a primary source we already hold was answered here instead of being asked.** Three candidate questions were dropped that way — see §B.

Companion to [`deep_research_review_geometry_20260911.md`](deep_research_review_geometry_20260911.md), which grades round 1.

---

## §A — ⭐ THE FOLLOW-UP PROMPT — paste this

> Thank you — the audit was useful and I have adopted several of its verdicts. Before I act on the rest, I need corrections and detail. **I have checked four of your claims against primary sources and my own repository, and all four are wrong. Please correct the record rather than defending it, and tell me plainly where you were uncertain.**
>
> **First, a formatting request that matters more than it sounds: give every number, formula and threshold as PLAIN TEXT, not as an equation object.** Your last report rendered 84 values as inline images. I read it programmatically and every one of those values was invisible to me — a sentence like "corridors must be at least ___" arrived with nothing in it. **Write `1/32 inch`, `<= 0.25`, `k = 3` inline as text.**
>
> **Corrections needed:**
>
> 1. **Постановление № 384 of 16.05.2013 was REPEALED IN FULL** by Постановление Совета Министров Республики Беларусь **№ 164 of 3 April 2026**, in force three months after publication. Your Belarusian layer, and your summary matrix, are built on a repealed act. **Redo that analysis against № 164 and current Belarusian norms.** What changed that affects apartment re-planning specifically — approval tracks, what counts as перепланировка, and what now requires a проект?
> 2. **You stated that СН 3.02.01-2019 sets clear widths for corridors leading to living rooms and for entrance/kitchen corridors. I have read the norm. It does not.** Its only corridor clauses concern **внеквартирные** (extra-apartment, common) corridors, and clause 10 states no figure at all — it refers out. **Either give me the exact clause number and a verbatim Russian quotation, or withdraw the claim.** And then answer the real question: **in Belarus, is the width of a corridor INSIDE a flat regulated at all — by СН, СТБ, ТКП, or an ЖК/СНБ document — or is it purely a design decision?**
> 3. **Is ГОСТ 28984-2011 «Модульная координация размеров в строительстве» legally applicable in Belarus**, as an adopted interstate standard or otherwise? Same question for ГОСТ 21.501-2018 and ГОСТ 2.307-2011, which you cited for dimensioning practice. **Name the Belarusian instrument that adopts each one, or say it is Russian-only.** This decides whether I can use your modular-coordination filter at all.
> 4. **`arXiv:2609.07362` ("BlueprintAgent") is the sole support for your constraint-triggered-revisit recommendation, and it is days old.** Give me a verbatim quotation of its central claim and its reported accuracy figures, and confirm the venue. **If you cannot quote it, say so.**
>
> **New questions:**
>
> 5. **Planar cycle loop closure — I want to build this, so give me the algorithm, not the concept.** How are the cycles chosen (a cycle basis of the planar graph? minimal faces? something else)? How does it behave when a floor plan's dimension chains are incomplete, so some loops cannot close at all? How is the failing edge identified when three or more adjacent cycles fail together rather than two? Give the error-localisation rule precisely, any published reference, and any existing open-source implementation.
> 6. **Your scale-factor invariance gate: state the rejection threshold in plain text**, and tell me how the reference distribution is estimated robustly — mean and standard deviation are wrecked by the very outliers we are hunting, so is it median and MAD, or something else? What happens when one sheet legitimately carries **two different scales** (a plan at 1:100 with a detail at 1:20)?
> 7. **Package reality check.** You recommended `ifctester` and `ifcopenshell.bcf`. **Neither is present in my environment (IfcOpenShell 0.8.5).** Give the exact PyPI package names to install for (a) IDS validation and (b) writing BCF-XML topics, say whether BCF writing lives inside IfcOpenShell or in a separate project, and confirm Bonsai can open the resulting BCF.
> 8. **IDS cannot express spatial rules — is anything changing that?** Is there work in IDS 1.1/2.0, an extension, or a community convention for expressing a clearance or adjacency requirement in a standard machine-readable form? Or is hand-written Python over Shapely genuinely the only route today?
> 9. **MCP as a semantic layer over a project's own canonical data**, rather than over a CAD tool, was your most interesting suggestion. **Are there real precedents?** Point me at any MCP server that exposes a project's own domain data for an agent to manipulate, with the deterministic build and validation left to local code.
>
> **Same standards as before: cite everything, date-stamp any capability claim, prefer primary sources, and where you are uncertain say so rather than smoothing it over.** And note that one of your benchmark citations was a vendor's own blog post about its own system, presented as an independent benchmark — **please label vendor-authored evidence as such.**

---

## §B — Questions deliberately NOT asked, because we answered them here

**The filter that matters: do not spend an external research round on something a primary source in this repo already settles.**

| Candidate question | Why it was dropped |
| :--- | :--- |
| *"What are the СН 3.02.01-2019 corridor widths?"* | **Read the archived norm directly** (`_Archive/processed_sources/20260908_SN_3.02.01-2019_…pdf`, 25 pp). There are none for in-flat corridors. That turned a question into **error #4** in the review — a much better outcome than asking |
| *"Are `ifctester` / `ifcopenshell.bcf` available?"* | **Checked the venv**: neither imports under `.venv-ifc314` (IfcOpenShell 0.8.5). The remaining unknown is only the correct **package names**, which is what question 7 now asks — a far narrower ask |
| *"What are the СН bathroom minimum dimensions?"* | **Already verified from the primary source on 2026-09-08** and recorded in `16_Legal_and_Regulations/analysis/Wet_Zones_and_Minimum_Room_Dimensions.md`. The vault's figures are better sourced than the report's, which were inside dropped images anyway |

## §C — Why the formatting request leads the prompt

It is not a stylistic preference. **The Docs API returns 1,109 `textRun` elements and 84 `inlineObjectElement`s for round 1's report; the inline objects carry no alt text, and two sampled downloads confirmed they are rendered images of the values** (the first reads `1/32 inch`).

**So roughly every threshold, tolerance and formula in a 6,761-word report was unreadable to an automated reader.** Asking for plain text is the single highest-leverage instruction in the follow-up — without it, round 2 will be just as unquotable as round 1.

## Open items

- **Whether to verify `arXiv:2609.07362` ourselves rather than asking its citer.** A model asked to confirm its own citation is weak evidence; a direct fetch would be stronger and is cheap. **Question 4 is the fallback, not the preferred route.**
- **Nothing in this round asks about cost, procurement or scheduling** — those stay with the 2026-09-08 brief and the BOM work.
- **Question 5's answer is the one that becomes code.** If round 2 returns a usable localisation rule, the next build item is the loop-closure checker for the `v0` reconstruction.
