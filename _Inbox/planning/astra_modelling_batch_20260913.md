# Astra-era modelling batch — triage and outcome, 2026-09-13

**Ten owner-supplied videos, all fresh. All ten fetched and read; none skipped unread.** Round yield: **70 new facts, 7.0 per video.**

## 1. ⚠️⚠️ The language finding, settled before any fetch

**Checked the caption manifest per video rather than trusting the titles — and it was necessary:**

| Original language | Videos |
| :--- | :--- |
| **Korean (`ko-orig`)** | `26UFabH--JU`, `Qh9xgjd38VI`, **`-FsHQEYldnQ` — which has an ENGLISH title** |
| **Russian (`ru-orig`)** | `JCCEW6797yw` |
| English | the remaining six |

> **⚠️⚠️ `-FsHQEYldnQ` is titled "GPT-6 Astra | AutoCAD Drawing | Computer Use" and is spoken entirely in Korean.** Had the habitual `en` been used, the fetch would have returned an auto-**translated** track — **the precise failure standing rule 1 exists to prevent, in a language pair the rule was not written for.**
>
> **→ The rule is "original language", not "Russian". Title language is not a signal of spoken language in ANY pair. Check the `-orig` track, per video, before fetching.**

**These are this vault's first Korean-language sources.** One (`Qh9xgjd38VI`) carries the **author's own manual Korean subtitles** — the highest transcript quality anywhere in the vault, and a welcome change from the ASR this class usually yields.

## 2. What the batch was, and what the expectation was

**Six of ten are capability demos of one model release, uploaded inside one week** — exactly the class this vault has repeatedly decided to discard, and the expectation going in was that the honest outcome would be *"mechanism kept, scores discarded"*.

**That expectation held for the scores and was wrong about the value.** Per the Round 2 lesson — *a triage's confidence about an unfetched source is worth much less than it feels* — **all ten were fetched and triaged on content.** Two predictions inverted:

- **`-FsHQEYldnQ` was expected to add a FOURTH architecture ("Computer Use"). It removed one instead** — see §3.
- **The Korean sources, which the title-skim ranked mid-table, are the two strongest in the batch.**

## 3. The findings that changed something

1. **⚠️⚠️ "Computer Use" is not a distinct architecture.** With **no MCP connected at all**, the visible GUI stepping is *"actually FOR THE HUMAN"* — it wrote **4,000+ lines of Python** and executed them, and on a second run produced the drawing in one shot with no animation at all. **It collapses into tool-driving. The architecture table gains no row.**
2. **⚠️⚠️ The revision question is answered, and it is what the architecture distinction is FOR.** File generation regenerates everything; **MCP edits in place** — *"modify just that window"* or *"change all 100 windows"*. **The working method is an annotated screenshot plus a plain-language instruction.** The same practitioner **delegated the fiddly MCP installation to the model** (7 min 16 s).
3. **⚠️⚠️ One defect class spans three tools: generated geometry is PLACED, NOT ASSOCIATED.** Beams that stay put when their grid moves; a **dimension text overridden so it disagrees with the geometry** — a drawing that lies. **The output looks right and nothing holds it right.** A purpose-built parametric tool reportedly does maintain it: **the difference is not intelligence, it is whether anything maintains the constraint.**
4. **⚠️⚠️ An agent silently chooses a DATUM — and two unrelated models chose the same one**, the **bottom-left of the wall**, *"quite commonly"*. **The silently-supplied-values rule applied to the origin, from which everything else is measured.** ⚠️ **This project has that question open**; this does not answer it, it names the convention we would be silently fighting.
5. **⚠️ Tracing recovers TOPOLOGY, not THICKNESS** — a tracer's own author assigns 30 cm exterior / 20 cm interior by hand afterwards. **And "automatically up to scale" from a skewed photo is a claim to distrust**: rectification recovers shape, not absolute scale, and no reference dimension appears anywhere in that demonstration.

### Two triage tests this batch established

- **⚠️⚠️ A FAMOUS BUILDING IS NOT A TEST OF DRAWING COMPREHENSION.** A Villa Savoye demo worked because *"its drawings are already all over the internet"* and **the model found them itself**. **Retrieval, not reading — the same confound as a benchmark leaked into training data. First question of any "AI modelled this building" demo: is the building famous?**
- **⚠️⚠️ A SELF-GENERATED CHECK IS NOT AN INDEPENDENT ONE.** Two models built their own verification artefacts — a separate "plan review" file, and section cuts taken mid-process. **Encouraging, until you note that one of them printed *"complete"* over a visibly half-finished drawing.**

## 4. ⚠️⚠️ The batch-wide pattern, stated plainly

**Of ten sources, essentially one measures anything.** Timings are everywhere; dimensional verification is almost absent. One source **names accuracy as the reason for a test and then never reports an accuracy figure.**

> **This vault's only measured elevation-to-3D fidelity check remains `sujS9Mgveo4`'s 610 drawn against 616 modelled. A visual "near-perfect" is recorded as exactly that throughout this batch — never as a measurement.**

**And every failure actually observed is a BUILDABILITY or SPATIAL-LOGIC failure, not a drafting one**: furniture placed across a stair, a door into a bedroom that is outside the building, an entrance wall arrangement omitted, a round sink where the drawing shows square, beams that ignore their grid. **Transcription succeeds; "can this be built and used" fails.** One source argues independently that this is the part which does not automate — and the batch supplies the evidence for its own claim.

## 5. Handling and exclusions

- **Four sources partially processed and one near-skipped, each saying so** in its own note.
- **Two overlap pairs handled once, not twice**: the two `feeel.d` videos (the later supersedes the earlier), and the two Melos Azemi videos (same product, three days apart).
- **⚠️ Concentration flags carried**: `T45kiCGvCQs` is the **sixth source from Justin Geis across two channels**; `gq1LIFNxjeI` is the second from Upstairs.
- **⚠️ One advertising finding routed**: `ZS_tnIN0zoA`'s channel reviews **its own product as item #1** of a neutral-looking seven-tool list **with no disclosure** — recorded against `gq1LIFNxjeI` in the same batch, which is sponsored and discloses it in the first minute.
- **Every model name, version and capability verdict discarded** per the standing dating rule. **No prices carried** — Indian, Korean and subscription figures, all uncomparable under rule 2. **No regulatory content.**

## 6. Open items

- **⚠️ The reverse direction remains untested and is the one this project actually needs**: one presenter proposes it as his next test — **can drawings be extracted FROM the model?** Nothing in this batch does it.
- **⚠️ The datum convention** (bottom-left of wall) is worth stating explicitly in `.agents/skills/residential-bim-geometry-rules/` **as the default to override**, alongside the datum decision itself — because the alternative is not "no origin" but an unstated one that two unrelated models default to.
- **Still no measured accuracy figure for drawing-set-to-model** beyond the single 610/616 spot-check.
