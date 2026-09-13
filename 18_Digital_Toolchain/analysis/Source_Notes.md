# Digital Toolchain — Source Notes

Traceability record for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]] and its `analysis/` pages. Not reader content.

## Design-toolchain group, Round 1 (2026-09-08)

Russian sources. Triage that authorised the round: [`design_toolchain_sources_triage_20260908.md`](../../_Inbox/planning/design_toolchain_sources_triage_20260908.md).

| Source | Practitioner | Contribution |
| :--- | :--- | :--- |
| [`YT_OTBw7bCrv-o`](../../_Sources/YT_OTBw7bCrv-o_remplanner_lesson4_electrics_lighting.md) | RemPlanner (vendor; narrator unnamed) | Dimensioning to centre, the `1/2` notation, `вывод` as an element type, per-sheet representation |
| [`YT_DI5GAV64mnU`](../../_Sources/YT_DI5GAV64mnU_kdmitry_technical_project_remplanner_festivalnaya.md) | Дизайнер Дмитрий К | Staged workflow, socket derivation, furniture-overlay reading, blank-sheet discipline |
| [`YT_F0rXrbPDPf4`](../../_Sources/YT_F0rXrbPDPf4_kdmitry_technical_project_remplanner_review.md) | Дизайнер Дмитрий К | The 18-tab sheet set, switch grouping, the finish-scheme-as-costing-input link, scope boundary |
| [`YT_TJVXUCKQ1UU`](../../_Sources/YT_TJVXUCKQ1UU_kdmitry_planoplan_sketchup_together.md) | Дизайнер Дмитрий К | The two-tool split, the underlay, what a planning model must be accurate about |
| [`YT_YEpfNcwwGoU`](../../_Sources/YT_YEpfNcwwGoU_kdmitry_concept_2room_planoplan_rationale.md) | Дизайнер Дмитрий К | Conventional colour at concept stage; sketch renders as a stage-1 output |
| [`YT_FRKr9X3AFfY`](../../_Sources/YT_FRKr9X3AFfY_kdmitry_doors_partitions_planning.md) | Дизайнер Дмитрий К | Door casings constraining partition position; doors modelled open and closed, trim as a later layer |

## AI-agent modelling and raster registration batch (2026-09-11)

English-language, US/UK market, `en-orig` auto-captions — the **original** language, not a translated track. Triage: [`ai_agent_modelling_sources_triage_20260911.md`](../../_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md).

| Source | Practitioner | Contribution |
| :--- | :--- | :--- |
| [`YT_f0EU_xbavEA`](../../_Sources/YT_f0EU_xbavEA_sketchupessentials_import_scale_reference_images.md) | Justin Geis, TheSketchUpEssentials | **Two-point scale verification**; a scaled raster is orientation, not measurement |
| [`YT_9tfvs3XW5qQ`](../../_Sources/YT_9tfvs3XW5qQ_trimble_2d_floorplans_to_3d_walls.md) | Aaron Dietzen, Trimble SketchUp | The ink's width as an error term; the oracle principle from the GUI side |
| [`YT_HOjQiiHJ714`](../../_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling.md) | Aaron Dietzen, Trimble SketchUp | An agent silently invents unspecified construction values; file-generator architecture |
| [`YT_3tAYEJTyUFY`](../../_Sources/YT_3tAYEJTyUFY_fairley_ai_read_construction_drawings.md) | Tim Fairley | Context rot, and condensing drawings into a queryable store |
| [`YT_althlPj8Tag`](../../_Sources/YT_althlPj8Tag_trimble_cad_linework_to_geometry.md) | Aaron Dietzen, Trimble SketchUp | Skimmed, corroborating only — `fact_yield: 0`, deliberately and accurately |

## AI toolchain batch (2026-09-13)

Owner-supplied list of 11 videos. **9 English, 2 Russian — every transcript fetched in its ORIGINAL spoken language** (`en` for the English-origin sources, `ru` for the Russian), never an auto-translated track. Triage and per-source verdicts: [`ai_toolchain_sources_triage_20260913.md`](../../_Inbox/planning/ai_toolchain_sources_triage_20260913.md).

**⚠️ Four of these are the same practitioner (Tim Fairley), three of them new plus one already processed on 2026-09-11. Repeated claims across his videos are ONE consistent stated position, not independent corroboration.**

| Source | Practitioner | Contribution | Yield |
| :--- | :--- | :--- | :--- |
| [`YT__k1jQBS4Nk8`](../../_Sources/YT__k1jQBS4Nk8_fairley_why_ai_fails_on_drawings.md) | Tim Fairley | The tiling mechanism; Anthropic's stated limits; the FIU benchmark pointer; the 141 overcount; scripts-versus-judgement | 9 |
| [`YT_ItW-ielFvGg`](../../_Sources/YT_ItW-ielFvGg_fairley_drawings_to_queryable_database.md) | Tim Fairley | **The 44-question measured benchmark**; the three artefacts; confidence tiers; the order-of-magnitude cross-check | 12 |
| [`YT_S77hdyyjTmA`](../../_Sources/YT_S77hdyyjTmA_fairley_three_layer_vector_takeoff.md) | Tim Fairley | The three data layers; take-off as a data layer; the element schema and its IFC origin; classify-versus-measure | 8 |
| [`YT_VcBohP2LbNM`](../../_Sources/YT_VcBohP2LbNM_aicontractor_flag_not_verify.md) | The AI Contractor | **Flag generator, not verifier**; three prompt rules; OpenAI's limits corroborating Anthropic's | 5 |
| [`YT_2eONA-6WVVI`](../../_Sources/YT_2eONA-6WVVI_merkulov_bti_to_visualisation_pipeline.md) | Алексей Меркулов / АМС | The БТИ-to-visualisation pipeline; LLM-as-prompt-engineer | 7 |
| [`YT_vmVvpKSSxWE`](../../_Sources/YT_vmVvpKSSxWE_archivlogs_claude_revit_mcp.md) | Archi Vlogs | Revit MCP path; **modelling accelerator, not space planner** | 4 (partial) |
| [`YT_6trAkQY5_kc`](../../_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp.md) | Make Form | The closed-loop architecture; the feedback/token trade-off | 3 (partial) |
| [`YT_la8Ml1fQfOg`](../../_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects.md) | Urban Decoders | The interview-me prompting pattern; change-versus-protect | 3 (partial) |
| [`YT_sujS9Mgveo4`](../../_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check.md) | Sketchup Gurus | **The batch's only measured fidelity check** — 610 drawn vs 616 modelled | 2 |
| [`YT_EibFZPrtAp0`](../../_Sources/YT_EibFZPrtAp0_civilengineering_chatgpt_dimensions_antipattern.md) | Civil engineering | **A documented ANTI-PATTERN** — vision-reading dimensions off a raster with no verification | 2 |
| [`YT_QLge-kb_L2I`](../../_Sources/YT_QLge-kb_L2I_moydom3d_five_ai_services_roundup.md) | Мой Дом и Сад 3D | Render-as-communication-artefact framing only; roundup discarded | 1 (near-skip) |

**Round 1 yield**: 11 videos processed, 56 new facts (excluding duplicate/corroborating-only outcomes), yield = **5.1** new facts per processed video.
