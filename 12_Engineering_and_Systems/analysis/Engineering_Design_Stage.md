# Engineering — The Design Stage: What Must Be Settled Before Finishing Starts

Cross-discipline detail page for [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]], [[12_Engineering_and_Systems/Plumbing_and_Waterproofing|Plumbing & Waterproofing]], [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]] and [[12_Engineering_and_Systems/Heating|Heating]].

**The decisions that are cheap now and expensive or impossible later, and the documents that make them possible.** One Moscow bureau's account.

> [!IMPORTANT]
> ***«Как только стены заштукатурены или зашиты гипсокартоном, переносить розетки, трубы или вентиляцию можно, но уже СЛОЖНО И ОЧЕНЬ ДОРОГО.»***
>
> **This page exists because the vault held a great deal about HOW to build each system and almost nothing about the inputs that have to exist before any of them can be designed.**

## ⚠️⚠️ 1. The responsibility boundary — and the assumption that gets it wrong

> ***«Зона ответственности начинается ОТ ПРИБОРА УЧЁТА И ПЕРВОГО ОТКЛЮЧАЮЩЕГО УСТРОЙСТВА на вашей ветке. Всё, что идёт дальше — ваше. И если лопнет труба у вас, вы заливаете соседей и будете платить за ремонт.»***

**The common assumption he names and rejects:** *«труба заходит в квартиру, значит, за неё отвечает УК»* — **no.**

- **→ The boundary is a physical object you can point at**, not a line on a plan: the meter, and the first isolating valve or breaker on your branch.
- **→ And it sets the scope of what is worth replacing.** Everything downstream is your liability, which is the argument for replacing the developer's fittings rather than inheriting them.

## ⚠️⚠️ 2. ТЕХНИЧЕСКИЕ УСЛОВИЯ — the free document that bounds every other decision

**The first step he prescribes: request the технические условия from the developer or the management company.** They state:

| The ТУ tell you | Why it decides something |
| :--- | :--- |
| **Where your responsibility begins** | §1 — what you must replace and what you must not touch |
| **⚠️⚠️ What electrical POWER is allocated to the flat** | The ceiling every appliance decision sits under — see [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Electrical Key Concepts and Planning]] |
| **What pipe diameters** | What flow is actually available |
| **What ventilation volume and what extract type** | Whether a cooker hood can be ducted at all |

> *«Это как карта. Без неё вы не знаете, куда идти.»*

> **→ ⚠️⚠️ SAME SHAPE AS THE ДЕТАЛИРОВКА AND ЭСКИЗ recorded in [[03_Kitchen/analysis/Ordering_A_Kitchen_Commercially|the kitchen ordering page]]: a document that already exists, that you are entitled to, that costs nothing, and whose absence is discovered late and expensively.** ⚠️ **Request the Belarusian equivalent for this flat whatever it is called locally.**
>
> **⚠️ Also mentioned in the same breath and worth separating: one project's ТУ stated the water PRESSURE supplied to the flat, and pressure falls with height** — on a 56th-floor job the management company suggested a circulation pump might eventually be needed. **So the ТУ can carry a performance figure, not only a boundary.**

## ⚠️⚠️ 3. The reserve provision — the most portable idea in the source

**Three times in one video the same pattern appears: do not install it, but make installing it later trivial.**

| Not installed | What was left for it |
| :--- | :--- |
| A **circulation pump** for water pressure that may or may not prove inadequate | A dedicated electrical outlet and physical space |
| An **extract fan**, which must not be fitted into a shared riser by default (see [[12_Engineering_and_Systems/analysis/Breathers_vs_Mechanical_Ventilation\|Breathers vs Mechanical Ventilation]]) | An electrical outlet, in case foreign cooking smells prove unsolvable |
| **Humidification or air conditioning** not wanted yet | Conduit and spare wiring — *«если через 2 года вы захотите поставить, то будете благодарны себе, что не придётся ничего ломать»* |

> **→ ⚠️⚠️ THE RULE GENERALISES: where a system MIGHT be wanted later and its enabling work is buried by finishing, the enabling work is cheap now and unavailable later.** **A socket, a conduit and 300 mm of clear space are a rounding error against chasing a finished wall.**
>
> ⚠️ **And it is a better answer than deciding prematurely**, because it does not require knowing today whether the problem will occur.

## ⚠️ 4. The engineering project, and how it is priced

**Priced PER DISCIPLINE, not as one document** — *«хороший инженерный проект стоит 50–100 000 руб. ЗА РАЗДЕЛ»*, with sections for **electrics, water supply, ventilation, heating and low-current.** Each specifies **cable cross-sections, cable grades and pipe diameters.**

- **⚠️ RUB, Moscow, 2026 — standing rule 2 blocks the figure and it is not converted. What transfers is the STRUCTURE: a quote for "an engineering project" without a section list is not comparable to one with it.**
- **His second argument for it is budget control**: *«вы видите, сколько нужно кабеля, труб, материалов. Без проекта мастера часто перерасходуют или, наоборот, экономят там, где нельзя.»*
- **⚠️ And his argument against relying on the fitters**: *«Мастер знает, как сделать, чтобы работало, но он не знает, что вы захотите через год поставить дополнительный кондиционер или систему умного дома.»* **→ The project is a road map to check the executors against.**

> ⚠️⚠️ **ONE OF HIS FIVE CLOSING RULES IS HIS BUSINESS MODEL AND IS RECORDED AS HIS POSITION, NOT AS GUIDANCE**: *«доверяйте проектирование тем, кто будет строить… нет размывания ответственности»*. **It runs directly against [[11_Budget_and_Planning/analysis/Technical_Supervision|the technical-supervision material]] in this vault, where the point of independent oversight is precisely that the designer and the builder are not the same party.** **Both positions are defensible and they are genuinely opposed; the vault holds both.**

## ⚠️ 5. The fixture schedule is an engineering input

**Request the technical sheet for every consumer before first fix.** His example: **a bidet-function WC needs an electrical supply and may need extra hot AND cold connections.** Others he names as commonly forgotten: **the electrical panel itself having nowhere to go**, an **instantaneous water heater** with no outlet provided, and a **humidifier** with no socket.

> **→ A fixture chosen after first fix invalidates a first fix that is already buried.** **This is the same coupling the kitchen round found between the module grid and the socket layout, arriving from the services side.**

## Related

- [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Electrical Key Concepts and Planning]] — the allocated power and demand coefficient this page points at.
- [[12_Engineering_and_Systems/analysis/Humidification|Humidification]] — one of the systems the reserve provision is for.
- [[03_Kitchen/analysis/Ordering_A_Kitchen_Commercially|Ordering a Kitchen Commercially]] — the same "demand the document before paying" pattern, on the furniture side.
- [[11_Budget_and_Planning/analysis/Technical_Supervision|Technical Supervision]] — the opposing view on who should design.

[source: [[_Sources/YT_blhGIAE-mE4_planka_engineering_systems_design_stage|YT_blhGIAE-mE4]]]

Part of `12_Engineering_and_Systems/` — this page deliberately sits across all four discipline guides, because the inputs it describes are settled once for the whole flat.
