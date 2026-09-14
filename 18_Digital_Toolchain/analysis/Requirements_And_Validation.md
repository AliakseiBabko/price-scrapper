# Requirements and Model Validation

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**How a requirement on a model gets written down, and how it gets checked.** General practice — **not this project's own ruleset**, whose status lives in [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md).

> [!IMPORTANT]
> **⚠️⚠️ This page exists because a source directly challenges a commitment this project has already made.** The gap analysis records an **`Adopt`** on authoring a project **`.ids`** ruleset (buildingSMART Information Delivery Specification). **One source argues, with an experiment, that the `.ids` FORMAT is doing no work — that every requirement in every format reduces to three columns.** The challenge is recorded here in full; **the decision is the owner's and is logged as an open item, not reversed.**

## 1. ⚠️⚠️ Every requirement reduces to ENTITY, ATTRIBUTE, CONSTRAINT

**DataDrivenConstruction** assembled the **same 20 validation rules written in eight different formats** — a Word execution plan, an Excel matrix, **Solibri Model Checker JSON**, CSV, a nested JSON, **DWS** (AutoCAD standards checking), **IDS from buildingSMART**, and XML — *«each with its own structure, its own syntax, its own way of expressing the exact same rules.»*

> *"To validate and apply the data in your case study, you only need **three columns. The group or type name, the parameter name, and the boundary conditions for its values.**"*
>
> Restated at the close: ***ENTITY** — what we check. **ATTRIBUTE** — which parameter. **CONSTRAINT** — what rule it must follow.*

- **⚠️ The Word plan actually carried FIVE columns — entity, attribute, constraint, plus SEVERITY and CATEGORY.** Severity and category are dropped as not load-bearing **for the check itself**. → **They are load-bearing for what you do with a failure**, which is a different job, and dropping them is a choice rather than a reduction.
- **⚠️ The verbosity spread is large**: Solibri costs *«dozens of lines of code»* per rule; **IDS is 250 lines of XML for 16 rules**, about 15 lines a rule; the consolidated form is **two Excel sheets of 6 KB each**.

[source: [[_Sources/YT_EHCgAi2x8-Q_ddc_requirements_three_columns|YT_EHCgAi2x8-Q]]]

## 2. ⚠️⚠️ The experiment — and the caveat that halves it

The same Revit model was validated **twice**: once against the requirements expressed as **JSON**, once against the **Solibri** expression of the identical rules.

> **Both runs returned 76.3%, 1,993 passed, 599 failed. Identical.**
>
> *"It does not matter which format the requirements are written in. If the rules are the same, the result is the same. **The format is unnecessary complexity.**"*

- **⚠️ THE RIGHT SHAPE OF EVIDENCE, and rare in this source class: hold the rules constant, vary only the notation, show the outcome does not move.**
- **⚠️⚠️ AND THE CAVEAT: the SAME AI agent wrote BOTH parsers, in the same run, from the same reading of the rules.** Two parsers by one author agreeing is **much weaker than two independent tools agreeing**. **The honest conclusion is that the formats are interchangeable TO THIS AGENT** — not that a real Solibri run would agree. **The experiment that would settle it was not performed.**
- **⚠️ An arithmetic slip worth recording, in a video about validation:** the final run reports **3,235 passed and 1,343 failed**, which sums to **4,578**; the narration says **"45,578 total"**, while its own closing line says *«nearly 5,000 checks»*. **Do not carry the 45,578.**

[source: [[_Sources/YT_EHCgAi2x8-Q_ddc_requirements_three_columns|YT_EHCgAi2x8-Q]]]

## 3. ⚠️⚠️ What this means for this project's `.ids` decision

**The case for a three-column CSV instead:**

- **Our rule count is small and will stay small** — wall thicknesses, a door clear width, socket heights, a `Pset_<Class>Common.Status` on every demolished element.
- **A CSV plus a short IfcOpenShell loop produces the same pass/fail list, is diffable in git, and needs no schema, no editor and no validator binary.** **The whole toolchain is already this shape** — `tools/lib/tabular.py`, strict CSV, one checker per concern.
- **`.ids` buys interoperability with other people's validators, and there is no counterparty.** ⚠️ **Speckle was declined on exactly this argument** — *«Git + canonical JSON … is leaner, runs entirely offline»*.

**The case for keeping `.ids`:**

- ⚠️ **It is an open buildingSMART standard**; a three-column CSV is a private schema, and this vault's standing preference is for open formats.
- ⚠️⚠️ **A hand-rolled checker is apparatus we then have to guard.** Standing rule 10: **a gate nobody has watched fail is not a gate** — every rule needs a seeded failure in a selftest. **That cost lands whichever notation wins, and it is the real cost.**
- ⚠️ **The reduction is asserted over ONE curated set of 20 rules.** A production `.ids` also carries **cardinality, applicability facets and optional-versus-required distinctions**, which three columns do not obviously hold. **Untested in the source, and the honest place where the reduction may leak.**

> **→ OPEN ITEM for the owner:** write the rules as a **three-column CSV first**, because that is the load-bearing part and it can exist in an afternoon; **emit `.ids` from it later if a counterparty ever needs it.** The columns are the source of truth either way, **which is the source's actual point and it survives the §2 caveat.**

[source: [[_Sources/YT_EHCgAi2x8-Q_ddc_requirements_three_columns|YT_EHCgAi2x8-Q]]]

## 4. ⚠️⚠️ A check's output is the list of things that failed — not a percentage

The demonstrated run produces *«detailed breakdowns for every project, every rule, **every failed element**»*, and the companion source emits **element identifiers that paste straight back into the authoring tool** to be located and fixed.

- **→ ⚠️⚠️ ADDRESSED FAILURES ARE THE PRODUCT OF A CHECK.** **This project's own gates already work this way and `00_Master/Validator_Design_Discipline.md` says why — *printing is not checking*.** **A 70.7% compliance headline is precisely the number that is useless without the list underneath it.**
- **⚠️ Treat the compliance percentage as decorative.** 36 rules of unstated importance, unweighted, across four projects. **A model can be 95% compliant and unbuildable, or 70% compliant with every failure trivial.**
- ⚠️ **The formal version of "an addressed failure" is a BCF issue**, which carries a viewpoint and a camera position as well as the element id.

[source: [[_Sources/YT_EHCgAi2x8-Q_ddc_requirements_three_columns|YT_EHCgAi2x8-Q]]]

## ⚠️ What is NOT established here

- **No error rate, on anything.** No case is shown where the agent misread a format, and no run is compared against a known-good validation.
- **The demonstration is a scripted best case** — two Revit files, two IFC files, and requirement sets the presenter prepared.
- **`promotional_ratio: high`** — it demonstrates the presenter's own converters and closes on his own book.

## Related

- [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Take-Off and the Cost Join]] — the same source family, on the quantity→price side.
- [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] — the silent-failure modes that a rule of this kind would catch.
- [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md) — where the `.ids` `Adopt` is recorded.

Part of [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]]. Sources: [[18_Digital_Toolchain/analysis/Source_Notes|Digital Toolchain — Source Notes]]. Edit history: [[18_Digital_Toolchain/analysis/Change_Log|Digital Toolchain — Change Log]].
