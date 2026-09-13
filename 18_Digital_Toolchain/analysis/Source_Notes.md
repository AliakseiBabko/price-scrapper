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

## Toolchain Round 2 — deferred Tier 2 items (2026-09-13)

**The Round 2 named in the [2026-09-11 triage](../../_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md) plus the Tier 2 singles deferred on [2026-09-08](../../_Inbox/planning/design_toolchain_sources_triage_20260908.md).** Triage and outcome: [`ai_toolchain_round2_20260913.md`](../../_Inbox/planning/ai_toolchain_round2_20260913.md).

**⚠️ FIVE of the eleven are one channel (TheSketchUpEssentials / Justin Geis), with a sixth already in the vault. Treat his claims as ONE consistent voice, never as corroboration.**

| Source | Practitioner | Contribution | Yield |
| :--- | :--- | :--- | :--- |
| [`YT_A1HxpHxrvv4`](../../_Sources/YT_A1HxpHxrvv4_craftelectric_cable_enclosure_schema.md) | Craftelectric | **The cable/containment cardinality split**; the cable-log take-off | 10 |
| [`YT_PVXE79HM0-c`](../../_Sources/YT_PVXE79HM0-c_stroyploshchadka_panel_design_toolchain.md) | Стройплощадка | The electrical deliverable set; **layer along the responsibility seam**; the data-carrying label | 10 |
| [`YT_s0TrXB2WQ2Q`](../../_Sources/YT_s0TrXB2WQ2Q_omsk_sketchup_excel_smeta_method.md) | Ремонт квартир Омск | **A chain-closure residual observed and discarded**; the three-part смета; stratified precision | 9 |
| [`YT_9-hQsyWSnm4`](../../_Sources/YT_9-hQsyWSnm4_craftelectric_mooncad_walls_and_scale.md) | Craftelectric / MoonCad | **Register on the longest known distance**; **a wall's side is relative to its direction** | 9 |
| [`YT_sSnjQJX4-iY`](../../_Sources/YT_sSnjQJX4-iY_mastersketchup_quantifier_three_methods.md) | MasterSketchUp | Three cost-attachment methods; **a build cancelled by a partial estimate** | 9 |
| [`YT_MZv33G7UE_A`](../../_Sources/YT_MZv33G7UE_A_mindsight_quantifier_pro_material_reports.md) | mind.sight.studios | Where a cost attaches; **waste and tax as first-class fields** | 8 |
| [`YT_X1lnTEpy6PQ`](../../_Sources/YT_X1lnTEpy6PQ_sketchupessentials_claude_connector_day_one.md) | TheSketchUpEssentials | **The tool-driving architecture**; third confirmation of the open loop; the corner-merge defect | 8 |
| [`YT_E-ECbD14g_8`](../../_Sources/YT_E-ECbD14g_8_sketchupessentials_mcp_permission_and_estimation.md) | TheSketchUpEssentials | **Session-scoped execution permission**; the interview round as a mitigation | 5 (partial) |
| [`YT_YkHGQPfZEgM`](../../_Sources/YT_YkHGQPfZEgM_upstairs_plan_presentation_technique.md) | Upstairs | Three presentation-pass rules; **styling recipe deliberately not routed** | 4 (partial) |
| [`YT_BEHlmJCKvTA`](../../_Sources/YT_BEHlmJCKvTA_sketchupessentials_model_comparison_method.md) | TheSketchUpEssentials | The comparison discipline; hidden-geometry inspection | 3 (partial) |
| [`YT_tJSS-IWrJoE`](../../_Sources/YT_tJSS-IWrJoE_sketchupessentials_ai_render_tool_selection.md) | TheSketchUpEssentials | **Edit-consistency as the render selection criterion** | 2 (near-skip) |

**Round 2 yield**: 11 videos processed, 77 new facts, yield = **7.0** per processed video — **above Round 1's 5.1.**

## @ConstructIQ Tier 1 round (2026-09-13)

**The five-video Tier 1 round recommended by [`constructiq_channel_triage_20260913.md`](../../_Inbox/planning/constructiq_channel_triage_20260913.md).**

> [!WARNING]
> **⚠️⚠️ ALL FIVE ARE ONE PRACTITIONER — Tim Fairley / @ConstructIQ — bringing this vault to NINE of his videos.** Nothing here corroborates anything else of his. The product funnel is constant. **Where a claim from him matters, it needs a second, unrelated voice.**

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_VrSs8mGI8ss`](../../_Sources/YT_VrSs8mGI8ss_fairley_takeoff_to_priced_bid.md) | **Take-off → priced bid end to end**; the rate-flagging gate; first-cut-then-check; the scope-gap reconciliation | 16 |
| [`YT_wgcOBhejKvo`](../../_Sources/YT_wgcOBhejKvo_fairley_agent_collision_and_git_for_knowledge_work.md) | **File-versus-line: why agentic harnesses break on documents**; his own architecture publicly retracted | 12 |
| [`YT_8aSYNMXk33A`](../../_Sources/YT_8aSYNMXk33A_fairley_eight_levels_of_context.md) | The context ladder; **the two problems skills solve**; the router-file pattern | 12 |
| [`YT_sjcDHXReSNI`](../../_Sources/YT_sjcDHXReSNI_fairley_workflow_systems_failure_modes.md) | **Four failure modes of a standalone workflow**; the slop problem; the **skeptic step** | 11 |
| [`YT_LBN9xF_rs1w`](../../_Sources/YT_LBN9xF_rs1w_fairley_subagents_and_lost_in_the_middle.md) | **"Lost in the middle"**; the sub-agent fresh-context mechanism | 8 |

**Round yield**: 5 videos, 59 new facts, yield = **11.8** per processed video — the highest of any round in this folder (Round 1 5.1, Round 2 7.0).

## Astra-era modelling batch (2026-09-13)

**Ten owner-supplied videos. ⚠️⚠️ THREE KOREAN, ONE RUSSIAN, SIX ENGLISH — each fetched in its verified ORIGINAL language.** One (`-FsHQEYldnQ`) has an **English title and Korean audio**; had the habitual `en` been used it would have been an auto-**translated** track. **This vault's first Korean-language sources.** Triage and outcome: [`astra_modelling_batch_20260913.md`](../../_Inbox/planning/astra_modelling_batch_20260913.md).

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_Qh9xgjd38VI`](../../_Sources/YT_Qh9xgjd38VI_feeeld_drawings_to_sketchup_with_revision.md) | **The REVISION question answered** — MCP edits in place; annotated-screenshot method; a third spatial-logic failure | 14 |
| [`YT_-FsHQEYldnQ`](../../_Sources/YT_-FsHQEYldnQ_grasshopperpp_computer_use_autocad.md) | **Computer Use is NOT a fourth architecture**; the silently-chosen datum; a dimension text that lies; "complete" over half-finished | 13 |
| [`YT_JCCEW6797yw`](../../_Sources/YT_JCCEW6797yw_bimdlyachaynikov_revit_dynamo_families_audit.md) | **Placed but not associated**; the complexity cliff located; the ID-traceable model audit | 9 |
| [`YT_gq1LIFNxjeI`](../../_Sources/YT_gq1LIFNxjeI_upstairs_archviz_ai_workflow.md) | Non-destructive layered editing; protective prompt phrases; the occlusion rule | 8 (partial) |
| [`YT_9pDOD_xx2kA`](../../_Sources/YT_9pDOD_xx2kA_melosazemi_sketch_to_cad_tracing.md) | **Tracing gives topology, not thickness**; "automatically to scale" as a claim to distrust | 6 |
| [`YT_T45kiCGvCQs`](../../_Sources/YT_T45kiCGvCQs_aiessentials_task_vs_profession.md) | Drift with length; the buildability constraint | 5 (partial) |
| [`YT_vHWOV5lJudg`](../../_Sources/YT_vHWOV5lJudg_melosazemi_floor_plan_generation_as_option_exploration.md) | Generation as option exploration; **the entrance-transition test** | 5 (partial) |
| [`YT_26UFabH--JU`](../../_Sources/YT_26UFabH--JU_feeeld_villa_savoye_ruby_console.md) | **A famous building is not a test**; the cheap-tier methodology | 4 (partial) |
| [`YT_hLslbz8n-1w`](../../_Sources/YT_hLslbz8n-1w_sudheendra_cad_to_unreal_walkthrough.md) | A 4-hour manual baseline; cross-model prompt writing; **no verification at all** | 4 (partial) |
| [`YT_ZS_tnIN0zoA`](../../_Sources/YT_ZS_tnIN0zoA_archmaster_seven_tools_roundup.md) | **Undisclosed self-promotion**; two capability categories | 2 (near-skip) |

**Round yield**: 10 videos, 70 new facts, yield = **7.0** per processed video.
