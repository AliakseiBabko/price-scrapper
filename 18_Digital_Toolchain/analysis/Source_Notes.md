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

## Bonsai / IFC / Blender batch (2026-09-13)

**Eleven owner-supplied videos plus two channels.** All eleven `en-orig`, each verified from the caption manifest before fetching. **One re-record pair handled once** (`xXmvs0PK_Bg` → `duplicate_skipped`, folded into `mq63GWbgWdM`). Triage, channel assessment and outcome: [`bonsai_ifc_batch_20260913.md`](../../_Inbox/planning/bonsai_ifc_batch_20260913.md).

> **⚠️⚠️ This batch differs in kind from the previous four.** Those were general AI-capability sources and were correctly triaged as *mechanism kept, scores discarded*. **This one is the toolchain this project actually runs** — Blender 5.2 + Bonsai 0.8.6-alpha260801, installed and idle — and the vault already holds an **`Adopt` decision** on Bonsai's drawings subsystem with one stated open question. **The sources are evidence bearing on a decision already taken, not capability scouting.**

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_p3Q7jNyRAtI`](../../_Sources/YT_p3Q7jNyRAtI_sfeviz_precise_plan_from_bad_image.md) | **⚠️⚠️ A plan image is not uniformly scaled — 45 mm anisotropy measured**; standing rule 9 executed on all four clauses unprompted; **wall thickness read as evidence of a concealed service**; an evidence ceiling stated and honoured | 14 |
| [`YT_PNoOyCHa_V0`](../../_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan.md) | **The drawing is GENERATED, not exported**; the ~1 m plan cut convention and its reason; **a plan symbol is authored, not cut**; type-level edits with silent blast radius; drafted-only elements invisible to take-off | 12 |
| [`YT_fxpIg-su-00`](../../_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai.md) | **⚠️⚠️ Four places the parametric association leaks**, which reframes the headless question; IFC as an *authoring* format is new; type duplication as the divergence mechanism | 11 |
| [`YT_Q4rbqUbhYXY`](../../_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image.md) | **Wall SURFACES not centrelines**, with the practitioner's reason; **a differing-thickness junction is authored, not automatic**; a hand-run geometry check with a known trap; ⚠️ scaling off an assumed door width | 9 |
| [`YT_YYmFMxMV6io`](../../_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export.md) | **Three silent-failure modes in one export path**; ⚠️ **text collision is manual in a purpose-built tool too**, which qualifies the adopt decision; the named style set | 9 |
| [`YT_xlmbZHIaHJw`](../../_Sources/YT_xlmbZHIaHJw_cgessentials_homebuilder_floor_plan_from_scan.md) | **⚠️⚠️ Wall direction sets inside/outside AND every hosted object** — independent confirmation; a scale verification that checks the wrong thing; an element's anchor as a per-object datum | 7 |
| [`YT_tAq0foY2GOY`](../../_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save.md) | **⚠️⚠️ The only controlled experiment in four batches** — the IFC is master, the `.blend` a cache; **and `Ctrl+S` writes to the IFC**, a live hazard in our own viewing instructions | 6 |
| [`YT_mq63GWbgWdM`](../../_Sources/YT_mq63GWbgWdM_architecturetopics_inkscape_trace_to_blender.md) | ⚠️⚠️ **A correct scale reference discarded over an unresolved unit** — the cleanest rule-9 failure in the vault; raster auto-trace as the naive counterpart to vector extraction | 5 |
| [`YT_4JYFYvNg5Xk`](../../_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai.md) | **A schema upgrade that reports success and leaves a deprecated entity**; a concrete rule for the IDS validation already marked `Adopt` | 5 |
| [`YT_DgovrfgLxYs`](../../_Sources/YT_DgovrfgLxYs_brockmesarich_astra_blender_parts_schedule.md) | A parts schedule off individuated geometry — **the cheap half of take-off**; ⚠️ near-skipped, `promotional_ratio: very_high` | 3 |

**Round yield**: 11 videos (10 processed, 1 duplicate), **81 new facts, yield = 7.4** per video. **Two new pages**: `Model_To_Drawing_Pipeline.md`, and `Raster_To_Geometry.md` extracted from `Drawing_Conventions_From_Practice.md` at the backstop.

## @IfcArchitect Tier 1 (2026-09-13)

**Eight videos from the 42-video channel, all `en-orig`, all read in full.** Triage and the question-map that drove the selection: [`ifcarchitect_tier1_20260913.md`](../../_Inbox/planning/ifcarchitect_tier1_20260913.md).

> **⚠️⚠️ THIS ROUND ANSWERED NAMED QUESTIONS RATHER THAN EXTRACTING OPENLY**, which is a first for this folder. Four open items were closed and two earlier conclusions corrected. **⚠️⚠️ All eight are ONE PRESENTER — a South African architect who names his own national standards twice. His agreement with himself is not corroboration, and every convention from him carries an unstated national default.**

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_VgvPk78IU0U`](../../_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting.md) | **⚠️⚠️ No auto-dimension at all** — placement is manual, which corrects the `Adopt` premise; **but tags are bulk-placed and `{{ }}` data-bound**, template type-level and value instance-level; the three-tier dimension chain at 400 mm; **SVG+CSS**; Qto in one command | 17 |
| [`YT_HEb7fWJduXg`](../../_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout.md) | **⚠️⚠️ The sheet is an SVG file on disk, assembled by hand in Inkscape** — so we are already better at composition; the round trip preserves manual edits; **a CSS selector filters per drawing**; `create drawing` must precede `create sheets`; **a clip hides geometry, it does not remove it** | 13 |
| [`YT__hADRIo-ma4`](../../_Sources/YT__hADRIo-ma4_ifcarchitect_custom_phases.md) | **⚠️⚠️ A demolition plan is a QUERY** over `Pset_*Common.Status` — the same three phases we carry as DXF layers; ⚠️ **but do not copy his type-per-phase pattern**; the standard breaks for spaces and the fallback is vendor-specific | 13 |
| [`YT_dPWQbjaeoyo`](../../_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css.md) | **⚠️⚠️ The styling system is literally CSS** — which dissolves the "magic strings" into class names; **the cut/projection/text/annotation/material taxonomy**; ⚠️ **four of five styling artefacts live in the app install** | 12 |
| [`YT_QTviOpqz1rw`](../../_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail.md) | **⚠️⚠️ A detail is MODELLED, not drafted** — a scoping decision for the owner; a detail is a section at 1:10; **text overflow fixed by shrinking the font, third instance**; the anatomy of a spec note and its two deferrals | 11 |
| [`YT_r0ebxigzM6U`](../../_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation.md) | **One camera primitive, four sheet types**; **classification is the switch that puts an object in the drawing** — demonstrated, not asserted; cut line weight is automatic, cut fill is not | 8 |
| [`YT__vrVETTI5jQ`](../../_Sources/YT__vrVETTI5jQ_ifcarchitect_custom_titleblock.md) | **Title blocks use the SAME `{{ }}` binding as tags** — one portable mechanism; ⚠️ custom ones are destroyed by a reinstall; never raster-trace something already vector | 8 |
| [`YT_jTL3a6QwckA`](../../_Sources/YT_jTL3a6QwckA_ifcarchitect_custom_wall_type.md) | **⚠️⚠️ CORRECTION: the library does NOT quantise** — an exact 220 type takes five minutes; thickness is a type property and geometry follows it; `IfcMaterialLayerSet` for layered build-ups | 7 |

**Round yield**: 8 videos, **89 new facts, yield = 11.1** per video — **the second-highest of any round in this folder** (5.1 / 7.0 / 11.8 / 7.4 / 11.1). ⚠️ **And the same caveat as the 11.8 round applies: the highest yields come from the most concentrated sources.** The number measures how much one voice said that was new to us, not how well-evidenced any of it is.

## Dude Blender floor-plan series (2026-09-13)

**Three owner-supplied videos, one continuous exercise, extracted as ONE source.** All `en-orig` with **author-supplied manual English subtitles** — the best transcript quality in this folder.

> **⚠️⚠️ This is the SIXTH Blender floor-plan source in the vault and the fourth in the mesh-tracing family.** The prior expectation was a fifth restatement, **and the modelling task genuinely is one.** What is not a restatement is the **geometry-integrity discipline**: this presenter states his invariants in advance, enumerates his failure modes as a debugging checklist, names where he is guessing, and reports defects he has hit before and cannot explain. **73 minutes, 29 facts, 9.7 per video against a batch norm of 7.**

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_94kAIpRnhcY`](../../_Sources/YT_94kAIpRnhcY_dudeblender_floor_plan_series.md) (+ `0JdX11vu7Zo`, `MEUsrN0V22g`) | **⚠️⚠️ Wall direction is the FACE NORMAL, with a visual gate** — blue outside, red toward the thickness; **the drawn line is a wall FACE, not a centreline**; **chain closure finds a 300 mm gap and he attributes it to wall thickness**; **the opening is fragile in BOTH families**, with the invariants stated as a checklist; **the commit point** — parametric until you bake, and *"full control at the cost of flexibility"*; **a material SLOT is the role/product split made explicit**; floor faces subdivided **by material region, not by room**; *edit one, edit all* shown to be **a property of instancing, not of BIM**; and **False Color as a measurable stand-in for an aesthetic judgement** | 29 |

**Round yield**: 3 videos, **29 new facts, yield = 9.7** per video. ⚠️ **The modelling task is now thoroughly covered — further sources on "how to draw a floor plan in Blender" should be declined** unless they carry something these six do not.

## DataDrivenConstruction Tier 1 (2026-09-14)

**Four videos from the 2026-09-14 channel triage, processed as the round's highest-value item: the quantity→price gap.** All `en`. ⚠️ **`promotional_ratio` high to very_high throughout — every video demonstrates the channel's own tools — and NOT ONE accuracy figure appears in any of them.** The tools are claimed free, `pip install`-able and fully local, with AI on the user's own API key; **that posture is materially different from a SaaS pitch and it is the same posture as ours. It is not verified — no repository was inspected.**

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_X06cIaroAeI`](../../_Sources/YT_X06cIaroAeI_ddc_openconstructionerp_qto_cost_join.md) (+ `ryJxOanNJVQ`, `QBaH8oBsPpM`) | **⚠️⚠️ THE FIRST SOURCE IN THIS VAULT THAT PRICES.** Three quantity routes into one BOQ line — model elements (bidirectional), a **two-point-calibrated PDF take-off**, and **a pivot table turned into positions**; a line carrying **region, currency, classification and a regional factor — and NO price date**; **resource decomposition**, which is how сметное дело works here; the basis chosen per line. ⚠️⚠️ **The unmeasured step: a “three-level semantic search” matching elements to catalogue positions, no error rate** — and **photo → priced positions**, the most suspect claim on the channel. ⚠️ **The Claude Code demo produces 214 line items and no cost at all**; the converter video is titled RAG and contains none | 21 |
| [`YT_EHCgAi2x8-Q`](../../_Sources/YT_EHCgAi2x8-Q_ddc_requirements_three_columns.md) | **⚠️⚠️ EVERY REQUIREMENT REDUCES TO THREE COLUMNS** — entity, attribute, constraint — across Word, Excel, Solibri JSON, CSV, nested JSON, DWS, **IDS** and XML; **the experiment**: identical results (76.3%, 1,993 / 599) from JSON and from Solibri, *“the format is unnecessary complexity”*. ⚠️⚠️ **DIRECTLY CHALLENGES THE `.ids` `Adopt` IN THE GAP ANALYSIS.** ⚠️ **And the caveat that halves it: one agent wrote both parsers.** ⚠️ An arithmetic slip in a video about validation — 3,235 + 1,343 = 4,578, narrated as “45,578” | 14 |

**Round yield**: 4 videos (3 folded into one note), **35 new facts**. **One new page: [[18_Digital_Toolchain/analysis/Requirements_And_Validation|Requirements and Model Validation]]**, created because `Model_To_Drawing_Pipeline.md` was at 379 lines and could not absorb it.

> **⚠️⚠️ A LANGUAGE FINDING WORTH CARRYING PAST THIS ROUND**: `ryJxOanNJVQ` has **no `-orig` caption track at all** — only a `manual: en` — **and that manual track renders *Claude Code* as “Cloud Code” and “clawed code”.** → **A “manual” subtitle can be machine-generated and merely uploader-accepted. `manual` is NOT evidence of a human transcript, and the tell is errors on proper nouns.** ⚠️ **Fourth distinct form of the title/caption-language trap recorded in this vault.**

## Bonsai and Blender practitioner triage (2026-09-17)

**Eight substantive sources triaged across five target channels/playlists** (`@blender3darchitect`, `@BIMvoice`, `@SPB-production`, `@dynamiterevit`, `@Modelflick`), addressing open problems 1–12 from `_Inbox/planning/agent_brief_bonsai_blender_triage_20260917.md`.

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [`YT_XYeasHbyw-U`](../../_Sources/YT_XYeasHbyw-U_spbproduction_bonsai_ifc_schema_conversion.md) | **Stepwise migration (2x3 → 4.0 → 4.3) via `IfcPatch` Migrate recipe**; IFC4.3 infrastructure scope; downgrade risk stripping georeferencing and converting unmapped entities to `IfcBuildingElementProxy`. | 6 |
| [`YT_CbDO16CfC7M`](../../_Sources/YT_CbDO16CfC7M_spbproduction_ifctester_ids_validation.md) | **Client-side WASM IDS validation via IFC Tester (`ifctester.org`)**; zero data egress; audit reports keyed by `GlobalId`; UI schema mismatch bug. | 6 |
| [`YT_fUlDzxSDOls`](../../_Sources/YT_fUlDzxSDOls_spbproduction_bonsai_spreadsheet_qto_schedule.md) | **Bonsai Spreadsheet module for QTO and schedules**; class filtering, Pset dot notation, double-quote requirement on spaced names, grouping and count/sum export to CSV. | 6 |
| [`YT_sdNStKd-fqE`](../../_Sources/YT_sdNStKd-fqE_bimvoice_bonsai_vanishing_geometry_type_vs_element.md) | **Vanishing geometry trap** (assigning `IfcElementType` defaults out of spatial containment); live classification crash; text-to-mesh requirement; `IfcAnnotation` unviewable fallback to proxy. | 7 |
| [`YT_-UuUCMOAvx4`](../../_Sources/YT_-UuUCMOAvx4_bimvoice_ids_wall_type_validation_mystery.md) | **IDS applicability debugging**: targeting `IfcWallType` vs `IfcWall` for type naming regex; property set attachment level; failure auditing. | 6 |
| [`YT_1WPw5NRJQmM`](../../_Sources/YT_1WPw5NRJQmM_blender3darchitect_mirror_in_bim_virtual_element.md) | **BIM mirroring geometry trap**: buildingSMART lacks mirrored instances; Bonsai mirror reflects coordinate offset across `IfcVirtualElement` without flipping geometry. | 5 |
| [`YT_-XPGFbmuh8U`](../../_Sources/YT_-XPGFbmuh8U_bimvoice_why_not_ditch_bim_tools_for_bonsai.md) | **Production reality of openBIM**: Solibri retained for speed (Bonsai validation on complex models wastes days); IfcOpenShell scripting vs GUI split; native IFC in-place editing. | 6 |
| [`YT_530npr9stZ0`](../../_Sources/YT_530npr9stZ0_bimvoice_bonsai_cgal_crash_advanced_mode.md) | **CGAL geometry kernel crash on import**; workaround via Advanced Mode switching Geometry Library to Open Cascade. | 5 |

**Round yield**: 8 substantive videos processed, **47 new facts, yield = 5.9** per video. Routed to `Requirements_And_Validation.md` and `Quantity_Takeoff_and_Cost_Join.md`. Over 280 candidate videos triaged and skipped with one-line rationale in the triage report.

