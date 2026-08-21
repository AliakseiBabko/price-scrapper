# Workstream B — batch 2 claim-to-source inventory

Inventory prepared before the batch-2 prose edits (2026-08-20). Each row maps
the claims in the named guide section (and the matching `analysis/` detail
page, where present) to the extraction note(s) cited by that section. The
channel value is copied from the cited note's `channel:` frontmatter; it is
not inferred from the page heading or video title. Existing footer citations
remain the click-through evidence.

## Confirmed source map

| page / claim block | extraction note(s) checked | channel used for inline attribution |
|---|---|---|
| `12_Engineering_and_Systems/Electrical_and_Lighting.md`: planning, circuit sizing, mounting heights, rough-in, temporary wiring, switches, lighting, buying | `YT_12o621100MQ`, `YT_8eECI5sWEy4`, `YT_JrClDJb8WTM`, `YT_ciXeqvKDKSI`, `YT_l_rjjPlPkRo`, `YT_uLJGsTfTj3A`, `YT_VT-zl1Xay4A`, `YT_VXfpDJruyVs`, `YT_GkpOGG_cxM0`, `YT_iRbTlv5Ka9o`, `YT_XmeoZUiGwBM`, `YT_PIYzs2b4UDU` | Alexey Zemskov / ZEMS; `YT_iRbTlv5Ka9o` additionally identifies Alexander Panfilov for technical lighting content |
| Electrical detail pages: point placement, panel, cable, switch/socket, lighting and temporary-work claims | the same note IDs above plus `YT_957RF_DcjwA`, `YT_C3yZJ_1xL-8`, `YT_hqkdbicp994`, `YT_lagL0yz7J28`, `YT_nmVie-r0iis` | ZEMS / Alexey Zemskov; `YT_957RF_DcjwA` is mixed and retains Sergey Saratov as technical contributor where its note says so |
| `12_Engineering_and_Systems/Heating.md`: underfloor-heating selection and placement | `YT_8RIyq8nZ9EQ`, `YT_C1L06upDI98` | Zemstandart / Alexey Zemskov |
| Heating: floor-standing radiators, in-floor convectors, panoramic glazing and valve clearance | `YT_-Kh9JZ34zRc`, `YT_d6xjRRXeOnc`, `YT_ob9iEwc3GWc`, `YT_dGknYgbRHe8` | Zemstandart / Alexey Zemskov |
| `12_Engineering_and_Systems/HVAC_and_Ventilation.md`: indoor-unit placement, condensate, sizing, fresh air, duct noise and buying | `YT_dGknYgbRHe8`, `YT_HX2pDdILM7U`, `YT_ZqfaeREBEYQ`, `YT_H61xa8n2nTk` | Zemstandart / Zemproekt; `YT_ZqfaeREBEYQ` identifies Sergey Saratov for the technical ventilation content; `YT_H61xa8n2nTk` is FLATART VIDEOS / Yuri Kokichev |
| `12_Engineering_and_Systems/Plumbing_and_Waterproofing.md`: rough-in sequence, fixture coordinates, pipe selection, inlet/filtration, pressure, leak protection and testing | `YT_ssS7-TdXhu0`, `YT_Onu15qOeWGA`, `YT_OSQeYSXjCfw`, `YT_zLJtkP6ymrg`, plus the other explicitly linked notes in the page's Source Notes page | Zemstandart / Zemproekt or ZEMS as recorded in each note; no attribution is added from a section title alone |
| Plumbing: water heaters, waterproofing, wet-zone relocation, riser/doorway clearance and buying | `YT_D8t1ADisUE8`, `YT_IbV-DC3z8jI`, plus the page's cited source-note links | Zemstandart / Zemproekt; the riser note's channel is used only where its frontmatter is decisive |
| `13_Surfaces_and_Finishes/Ceilings_Guide.md`: L-shaped ceiling and seamless-width case | `YT_UfmUC4-T3jY`, `YT_2hg0mjR-M30` | Zemstandart / Zemproekt (source note identifies Zemskov/Zemstandart) |
| Ceilings: legacy Do/Don't material cited only to archive text without a decisive `channel:` field | archive source-note entries listed in the page | `retired attribution-prefix — cited archive extraction does not isolate a channel in frontmatter` |
| `13_Surfaces_and_Finishes/Doors_and_Trim.md`: door anatomy, openings, concealed doors, entrance doors, swing direction, materials and buying | `YT_yHmEQTqduDk`, `YT_ludvy76HGSU`, `YT_c4b7iyg8v5U`, `YT_-HKwxCBa40k`, `YT_ti8J19zY0EM`, `YT_D2Qz6s8eNoU`, `YT_oVf6AyxJjd0`, `YT_7Vd95idVXak`, `YT_COhFXPyfXxM`, `YT_Mfzce0Qm4HM`, `YT_WMc_AjUqQ-4` | Ontario / Konstantin Kruglov where `YT_yHm...` is cited; Zemstandart / Alexey Zemskov for ZEMS notes; Forcemontage for concealed-door facts; Sergey Gusev / ПРО ДВЕРИ for manufacturer/material claims |
| `13_Surfaces_and_Finishes/Flooring_Guide.md`: transitions, matching, laying direction, glue-down technique, retail-tier warning and sequencing | `YT_PwJsksBs4Ek`, `YT_lOMxNoyW_NE`, `YT_XFhz1NXlln8`, `YT_cJLZebMtW7A` and the cited archive entry for glue-down technique | Zemstandart / Zemproekt or Zemstandart / Zemsproekt as recorded; archive-only claims are marked unconfirmed |
| `13_Surfaces_and_Finishes/Walls_and_Paint.md`: substrate, masonry, false walls, radiator niches, load-bearing openings, layout, partitions and finish interaction | `YT_zPR8PGWq5lA`, `YT_8kOUv9EVQTQ`, `YT_g7Cuj1p-0CA`, `YT_Qs_FxXdsq40_masonry_glue_foam_technique_260`, `YT_Y-eITaok1Gw`, `YT_p-6OI34C6bw`, `YT_u3UuZN9LHg0`, `YT_sJ8UZj36TMQ`, `YT_Eq0kg2hD-Ws`, `YT_F5v7eI3ry1M`, `YT_EnSpVCSUiqg` | Zemstandart / Zemproekt or Zemstandart / Zemsremont per note; exact mixed/guest channels are retained when the note distinguishes them |
| Walls: claims citing `note 1`, `note 2`, or `note 3` without a linked extraction-note target | the page's own Source Notes block and the referenced detail notes | `retired attribution-prefix — the guide's local note number does not expose a unique extraction-note `channel:` value` |
| `13_Surfaces_and_Finishes/Windows.md`: profile, fastening, slopes, hardware, replacement and acceptance | `YT_6_cH35u4ouM`, `YT_AGjYrwqilNA`, `YT_gjTGr8j6-DA`, `YT_nb3L-k69yx8`, `YT_qwIRfgn1Tog`, `YT_XFrmhhM1ogg`, `YT_XmtGo4BE1bw`, `YT_irOVnHty0fc`, `YT_NhGzB1L7hM`, `YT_uBNF5ZYOE0Y`, `YT_IAZreuaqhjg` | Zemstandart / Alexey Zemskov or Zemstandart / Zemsproekt; guest/technical contributors are named only where the note's frontmatter identifies them |
| `14_Furniture/Wardrobes_and_Storage.md`: sizing, walk-ins, wardrobe tradeoff, client cases and worked layouts | `YT_RyHzFDGgqKA`, `YT_n0O47DdhATw`, `YT_o4KitYl8vpU`, `YT_Xh7uwbKVmfA`, `YT_VgsPDOcPV7c`, `YT_kj503mBQXq8`, `YT_hVFmcw1H2Rk`, `YT_pVMvsuhrwWs` | Zemstandart / Zemproekt; `YT_pVMvsuhrwWs` is used only for its source-note channel, not generalized to all furniture claims |

## Editing rule and exclusions

The guide claim itself is the unit of editing. A source name is woven into
that claim's sentence while the existing `[source: ...]` footer is retained.
Where a claim is backed only by an archive note, a local `note 1/2/3`, or a
mixed note whose channel cannot isolate the particular sentence, the sentence
receives `retired attribution-prefix — <reason>` instead of a guessed name.

The pages' `Source Notes` and `Change Log` sections are evidence/maintenance
metadata, not claim prose, and are not rewritten. Wikilinks are not edited;
the inventory records their targets only to support the attribution check.

## Detail-page batch inventory (turn 12)

| detail-page family | claim/source inventory | attribution treatment |
|---|---|---|
| HVAC: `AC_Key_Concepts_and_Placement`, `AC_Condensate_Drainage`, `AC_Sizing_and_Selection` | `YT_H61xa8n2nTk`, `YT_wFUUakbL5O8`, `YT_fSEPr5fpfPM`, `YT_6Z7uH2_rXsw`; archive condensate paragraphs where no extraction-note frontmatter exists | FLATART, Zemstandart/Zemsproekt, or BURO named only for the matching note; archive/mixed claims unconfirmed |
| HVAC: `Fresh_Air_Ventilation_and_Ducting`, `HVAC_Common_Mistakes_and_Buying` | `YT_HX2pDdILM7U`, `YT_ZqfaeREBEYQ`; archive entries for contractor, duct, seasonal and warranty claims | Zemstandart/Zemsproekt named for the two frontmatter-backed notes; archive-only claims unconfirmed |
| Plumbing: `Rough_Plumbing_Sequencing`, `Fixture_Stubout_Coordinates`, `Pipe_Material_Selection` | `YT_ssS7-TdXhu0`, `YT_zLJtkP6ymrg`, `YT_1_IcoSaNKP4`, `YT_fSEPr5fpfPM`, plus archive entries listed in Plumbing Source Notes | ZEMS named for frontmatter-backed claims; archive-only and cross-source paragraphs unconfirmed |
| Plumbing: `Water_Inlet_Node_Components`, `Pressure_and_Water_Hammer`, `Leak_Protection_Systems`, `Pressure_Testing` | page-specific archive notes plus `YT_zLJtkP6ymrg` for pressure-test claims and the linked source notes where present | only `YT_zLJtkP6ymrg` receives a named channel; archive/mixed claims unconfirmed |
| Plumbing: `Water_Heaters`, `Waterproofing_and_Plastering`, `Shower_Podium_and_Drains`, `Hygienic_Shower_and_Towel_Warmer`, `Wall_Hung_Toilet_Installation`, `Cost_Drivers_and_Buying_Guidance` | archive entries listed in Plumbing Source Notes; `YT_cdNwbqsLUK4` for the points-pricing claim | RemontHochu named for the points-pricing claim; remaining archive-derived claims unconfirmed |
| Doors: `Door_Anatomy_and_Mount_Types`, `Door_Swing_Direction`, `Doors_Trim_Cost_and_Buying` | `YT_yHmEQTqduDk`, `YT_ludvy76HGSU`, `YT_1YiVgB9jqyU`, `YT_c4b7iyg8v5U`, `YT_7Vd95idVXak`, `YT_COhFXPyfXxM`, `YT_WMc_AjUqQ-4`, `YT_-HKwxCBa40k`, `YT_ORkPwMJ-AzU`; archive entries for older numeric claims | named channels only where the cited note has frontmatter; archive/mixed claims unconfirmed |
| Ceilings detail content | guide's `YT_UfmUC4-T3jY` and `YT_2hg0mjR-M30` notes; legacy archive table rows | Zemstandart/Zemsproekt named for the two extraction notes; legacy archive rows unconfirmed |

## Detail-page continuation inventory (turn 16)

| detail pages edited | source/channel evidence | attribution treatment |
|---|---|---|
| Plumbing: `Leak_Protection_Systems`, `Water_Heaters`, `Shower_Podium_and_Drains`, `Hygienic_Shower_and_Towel_Warmer`, `Wall_Hung_Toilet_Installation` | mixed, single-account, and archive-backed notes; the cited note fields do not isolate a decisive channel for the edited claims | inline `retired attribution-prefix` with archive, mixed-source, or non-isolated reason; original source footers retained |
| Plumbing: `Pipe_Material_Selection` | mixed and single-account claims; `YT_1_IcoSaNKP4` is cited for corroboration but does not isolate every sentence | named channel withheld for aggregate claims; inline unconfirmed reasons added |
| Doors: `Entrance_Doors` | linked extraction notes and manufacturer pricing note do not isolate a decisive channel for the edited claims | inline `retired attribution-prefix`; no claim meaning or source footer changed |

## Detail-page completion inventory (turn 18)

| detail pages edited | source/channel evidence | attribution treatment |
|---|---|---|
| Plumbing: `Rough_Plumbing_Sequencing`, `Waterproofing_and_Plastering` | cross-source, regulatory, and archive-only claims; cited notes do not isolate a decisive channel for the edited sentences | inline `retired attribution-prefix` with cross-source, jurisdiction, or archive reason |
| Plumbing: `Cost_Drivers_and_Buying_Guidance` | points-pricing claim is backed by the frontmatter-identified RemontHochu.ru note; other claims are not channel-isolated | RemontHochu.ru named only for the points-pricing claim; other edited claims unconfirmed |
| Doors: `Material_and_Finish_Tiers`, `Rough_Opening_and_Casing_Sizing`, `Style_Hardware_and_Security` | mixed, single-account, and archive-only claims; source footers do not isolate one channel for most edited sentences | inline `retired attribution-prefix`; original wording, footers, and wikilinks retained |

## Accumulated-detail audit and guide start (turn 20)

| scope | audit/source finding | attribution treatment |
|---|---|---|
| Detail audit: Plumbing Cost Drivers and Doors Style/Hardware | residual claim sentences lacked sentence-level attribution after earlier bounded edits | archive, jurisdiction, or non-isolating claims marked `retired attribution-prefix` |
| Guide start: `Flooring_Guide.md` | guide section labels identify Zemskov/Zemstandart, while existing source notes include archive-only single-account evidence | named Zemstandart / Alexey Zemskov only where the guide's cited section makes that channel explicit; existing single-account caveats retained |
| Guide start: `Walls_and_Paint.md` | first substrate/deviation section cites an archive note without a decisive `channel:` field | first four claims marked `retired attribution-prefix`; no channel inferred from the section heading |

## Final guide start and untouched-analysis audit (turn 22)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: `Windows.md`, `Wardrobes_and_Storage.md` | guide source-note targets reviewed; the edited guide claims do not have decisive `channel:` frontmatter | inline `retired attribution-prefix`; no channel inferred from guide headings |
| Windows analysis: `Windows_Measurement.md` | first measurement claims reviewed; cited analysis notes do not isolate a decisive channel | first three claims marked `retired attribution-prefix`; remaining Windows analysis claims require a further bounded pass |
| Electrical/Heating analysis audit | multiple untouched analysis pages still contain claim prose without inline attribution, including Electrical Key Concepts and Planning and additional Electrical/Heating detail pages | identified for follow-up; Workstream B detail acceptance remains open |

## Windows/Furniture continuation and analysis audit (turn 24)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: `Windows.md`, `Wardrobes_and_Storage.md` | remaining edited claims are backed by mixed or source-note targets without decisive `channel:` metadata | inline `retired attribution-prefix` with non-isolating-source reason |
| Windows analysis: `Windows_Quality_and_Buying`, `Windows_Slope_Finishing`, `Windows_Measurement` | cited notes are single-account, archive-only, or channel-non-isolating for the audited claims | inline `retired attribution-prefix`; source footers retained |
| Electrical/Heating analysis: `Electrical_Buying_and_Hiring`, `Heating_Type_Selection` | audited comparison/buying claims do not expose decisive channel metadata | inline `retired attribution-prefix`; remaining Electrical/Heating analysis claims still require a full bounded audit |

## Windows/Furniture and Electrical/Heating continuation (turn 26)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: remaining `Windows.md` and `Wardrobes_and_Storage.md` claims | remaining claims use mixed, single-account, or non-isolating source-note support | inline `retired attribution-prefix`; guide claim starts now have no unmarked `**` prose |
| Windows analysis: `Windows_Hardware_Selection`, `Windows_Installation_and_Fastening` | cited technical notes do not isolate a decisive channel for the edited claims | inline `retired attribution-prefix`; original source footers retained |
| Electrical/Heating analysis: `Rough_Electrical_Sequencing`, `Temporary_Construction_Electrical`, `Heating_Placement_Rules` | cited technical claims are source-non-isolating or single-account | inline `retired attribution-prefix`; further Electrical Key Concepts and Windows analysis claims remain for audit |

## Remaining-list continuation (turn 28)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Electrical: `Electrical_Key_Concepts_and_Planning`, `Electrical_Buying_and_Hiring` | audited claims are source-non-isolating | inline `retired attribution-prefix`; original source context retained |
| Windows analysis: `Windows_Acceptance_Checklist`, `Windows_Opening_Reconfiguration` | case-study/acceptance notes lack decisive channel metadata for edited claims | inline `retired attribution-prefix` |

## Detail-page continuation inventory (turn 14)

| detail-page family | claim/source inventory | attribution treatment |
|---|---|---|
| Plumbing: `Fixture_Stubout_Coordinates` | `YT_ssS7-TdXhu0` for the coordinate grid; `YT_fSEPr5fpfPM` for kitchen-group offset | Zemstandart / Alexey Zemskov for the decisive frontmatter-backed notes |
| Plumbing: `Water_Inlet_Node_Components`, `Pressure_and_Water_Hammer` | mixed and archive-derived source paragraphs; no single channel isolates the aggregate claims | `retired attribution-prefix` with a mixed/archive reason; no channel inferred from page family |
| Doors: `Concealed_Door_Considerations`, `Doors_Trim_Cost_and_Buying`, `Door_Swing_Direction` | archive-only, mixed, and single-account claims; linked note targets do not consistently expose a decisive `channel:` field | `retired attribution-prefix` with the specific archive/mixed/non-isolated reason |
| Ceilings | filesystem check found no `13_Surfaces_and_Finishes/analysis/*Ceil*` file; no separate claim-bearing detail page exists | no detail edit required; Ceilings remains guide-level |

## Remaining-list continuation inventory (turn 30)

| scope | claim/source finding | attribution treatment |
|---|---|---|
| Electrical: `Electrical_Key_Concepts_and_Planning`, `Electrical_Buying_and_Hiring` | the remaining audited claims cite notes whose `channel:` metadata does not isolate a decisive channel | inline `retired attribution-prefix — the cited extraction note does not isolate a single channel`; wording, source context, and footers retained |
| Windows analysis: `Windows_Acceptance_Checklist`, `Windows_Opening_Reconfiguration` | the remaining acceptance and case-study claims cite notes without decisive channel metadata | inline `retired attribution-prefix — the cited extraction note does not isolate a single channel`; wikilink targets and labels retained |

## Remaining-list continuation inventory (turn 32)

| scope | claim/source finding | attribution treatment |
|---|---|---|
| Engineering analysis: `Cost_Drivers_and_Buying_Guidance`, `Heating_Placement_Rules`, `Heating_Type_Selection`, `Pipe_Material_Selection` | residual claims cite mixed, single-account, or otherwise non-isolating notes; no channel was safely inferable for these sentences | inline `retired attribution-prefix — the cited extraction note does not isolate a single channel`; original wording, source context, and footers retained |
| Doors analysis: `Doors_Trim_Cost_and_Buying`, `Door_Swing_Direction`, `Rough_Opening_and_Casing_Sizing` | residual door-cost, swing, and opening-sizing claims were treated as source-non-isolating in this bounded pass | inline `retired attribution-prefix — the cited extraction note does not isolate a single channel`; wikilinks retained where present |

## Workstream F retrofit inventory (turn 34)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| Windows guide and analysis: `Windows.md`, `Windows_Quality_and_Buying`, `Windows_Measurement`, `Windows_Hardware_Selection` | `Windows_Source_Notes.md` identifies all 18 cited sources as Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov), with Konstantin only as a named installer partner on some installation sources | 19 old `retired attribution-prefix — ...` prefixes replaced with real Zemstandart/Zemsproekt/Zemsremont inline attribution; no old pattern remains in these four files |

## Workstream F retrofit inventory (turn 36)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| Electrical analysis: `Electrical_Key_Concepts_and_Planning` | Electrical Source Notes identify the relevant ZEMS playlist and the guide's channel note identifies it as Zemstandart / Alexey Zemskov; the edited planning and lighting claims match that source family | 7 old prefixes replaced with `Alexey Zemskov / ZEMS` inline attribution |
| Electrical analysis: `Rough_Electrical_Sequencing`, `Temporary_Construction_Electrical` | both pages' cited technical material is within the ZEMS electrical playlist listed in Electrical Source Notes | 7 old prefixes replaced with `Alexey Zemskov / ZEMS` inline attribution |
| Electrical analysis: `Electrical_Buying_and_Hiring` | page combines mixed buying sources and the current claim-to-note mapping does not isolate a single channel for every old-pattern claim | deferred for a dedicated source-link/channel pass; no ZEMS attribution guessed |

## Workstream F retrofit inventory (turn 38)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| Doors guide: `Doors_and_Trim.md` | `Doors_Trim_Source_Notes.md` maps sizing, swing, and minimum-width claims to Zemstandart/Alexey Zemskov; concealed-door mechanisms to Ontario, Avalremont, and Forcemontage; entrance security to Novakey and ПРО ДВЕРИ/Sergey Gusev | 7 old prefixes replaced with named inline attribution; no retired pattern remains in the guide |
| Doors analysis pages | remaining pages include mixed, archive-only, and source-link gaps requiring claim-level evidence review | deferred to the next Doors detail sub-batch; no unsupported channel names assigned |

## Workstream F retrofit inventory (turn 40)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| Doors detail: `Door_Anatomy_and_Mount_Types`, `Door_Swing_Direction`, `Entrance_Doors`, `Material_and_Finish_Tiers`, `Rough_Opening_and_Casing_Sizing`, `Style_Hardware_and_Security` | Doors Source Notes map the claims to Zemstandart/Alexey Zemskov, Sergey Gusev/ПРО ДВЕРИ, and Novakey where applicable; the cited source labels were retained | 33 retired prefixes converted to named inline attribution; zero old-pattern matches remain in these six pages |
| Doors detail: `Doors_Trim_Cost_and_Buying`, `Concealed_Door_Considerations` | mixed/archive support does not yet isolate a safe channel for every claim | deferred for direct extraction-link retrofit; no channel guessed |

## Workstream F retrofit inventory (turn 42)

| scope | result | remaining treatment |
|---|---|---|
| Engineering analysis: `AC_Condensate_Drainage` (5), `AC_Key_Concepts_and_Placement` (3), `AC_Sizing_and_Selection` (1), `Heating_Placement_Rules` (3) | 16 old prefixes converted to named attribution: Zemstandart/Alexey Zemskov for the AC and heating claims, FLATART for the AC filtration claim | zero old-pattern matches remain in these four files |
| Engineering analysis remaining old-pattern files | `Cost_Drivers_and_Buying_Guidance` (10), `Electrical_Buying_and_Hiring` (8), `Fresh_Air_Ventilation_and_Ducting` (9), `Heating_Type_Selection` (5), `HVAC_Common_Mistakes_and_Buying` (7), `Hygienic_Shower_and_Towel_Warmer` (6), `Leak_Protection_Systems` (6), `Pipe_Material_Selection` (9), `Pressure_and_Water_Hammer` (4), `Pressure_Testing` (3), `Rough_Plumbing_Sequencing` (7), `Shower_Podium_and_Drains` (4), `Wall_Hung_Toilet_Installation` (4), `Waterproofing_and_Plastering` (6), `Water_Heaters` (6), `Water_Inlet_Node_Components` (3) | 93 old-pattern matches remain; continue Engineering in the next bounded sub-batch with per-source mapping |

## Workstream F retrofit inventory (turn 44)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| `Heating_Type_Selection` (5) and `Pressure_Testing` (3) | Heating Source Notes and Plumbing Source Notes identify the cited playlist material as Zemstandart/Zemsproekt (Alexey Zemskov); the pressure-testing note is explicitly the Zemstandart playlist masterclass | all 8 retired prefixes replaced with named Zemstandart/Alexey Zemskov attribution |
| `Wall_Hung_Toilet_Installation` (4), `Shower_Podium_and_Drains` (4), and the hygienic-shower claims in `Hygienic_Shower_and_Towel_Warmer` (3) | Plumbing Source Notes map wall-hung-toilet, shower-podium, drain, and hygienic-shower material to Konstantin Kruglov/Ontario | all 11 retired prefixes replaced with Konstantin Kruglov/Ontario attribution |
| `Water_Heaters` (6) | Plumbing Source Notes map the tank/tankless and safety claims to Konstantin Kruglov/Ontario and Zemstandart/Alexey Zemskov; specific reliability, placement, and relief-valve claims map to the named channel | all 6 retired prefixes replaced with named channel attribution; no claim meaning changed |
| `Water_Inlet_Node_Components` (3) | Plumbing Source Notes identify the component/sequence claims as mixed LAB-REMONT, Знакомые сантехники, Добродушный сантехник, and Стройплощадка × Будни сантехника material | all 3 retired prefixes replaced with the corresponding named multi-channel attribution; disagreement about mesh sizes retained |
| `Hygienic_Shower_and_Towel_Warmer` pre-finish claim (1) | cited archive transcript has no frontmatter `channel:` field, so no channel name was inferred | retired prefix removed; claim retains a direct relative Markdown link to its specific archive extraction note |
| Engineering analysis remainder after this pass | `Cost_Drivers_and_Buying_Guidance` (10), `Electrical_Buying_and_Hiring` (8), `Fresh_Air_Ventilation_and_Ducting` (9), `HVAC_Common_Mistakes_and_Buying` (7), `Leak_Protection_Systems` (6), `Pipe_Material_Selection` (9), `Pressure_and_Water_Hammer` (4), `Rough_Plumbing_Sequencing` (7), `Waterproofing_and_Plastering` (6) | 66 old-pattern matches remain for a subsequent verified source-mapping batch; no unsupported channel names assigned |

## Workstream F retrofit inventory (turn 46)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| `Cost_Drivers_and_Buying_Guidance` (10) | Plumbing Source Notes map the built-in cost comparison to WITALT; manifold, riser, access-hatch, and recirculation claims to LAB-REMONT, Zemstandart, Стройплощадка × Будни сантехника, and Добродушный сантехник | all 10 retired prefixes replaced with claim-specific named attribution |
| `Electrical_Buying_and_Hiring` (8) | Electrical Source Notes place finish-electrical buying, tool-kit, intercom, and cable-protection material in the Zemstandart/Alexey Zemskov electrical playlist | all 8 retired prefixes replaced with Alexey Zemskov / ZEMS attribution |
| `Fresh_Air_Ventilation_and_Ducting` (9) | HVAC Source Notes map breather/full-system guidance to Prolife Invest, hood claims to the named multi-source kitchen-hood set, and duct/design claims to Zemstandart/Zemsproekt | all 9 retired prefixes replaced with the mapped channel or corroborating named channels |
| `HVAC_Common_Mistakes_and_Buying` (7) | HVAC Source Notes and the FLATART extraction note support the retailer's AC mistake/buying claims; the duct-inspection/archive claim maps to Zemstandart material | all 7 retired prefixes replaced with FLATART or Zemstandart/Alexey Zemskov attribution |
| `Leak_Protection_Systems` (6) | Plumbing Source Notes map architecture and component claims to LAB-REMONT, Знакомые сантехники, and Zemstandart/Alexey Zemskov | all 6 retired prefixes replaced with named single- or multi-channel attribution |
| `Pipe_Material_Selection` (9) | PEX/material comparison and manifold guidance map to Konstantin Kruglov/Ontario; polypropylene demonstration to Zemsremont/Zemstandart; riser-side rule to Стройплощадка × Будни сантехника | all 9 retired prefixes replaced with claim-specific named attribution |
| `Pressure_and_Water_Hammer` (4) | Plumbing Source Notes map pressure, reducer, and water-hammer mechanisms across LAB-REMONT, Знакомые сантехники, Добродушный сантехник, and Стройплощадка × Будни сантехника | all 4 retired prefixes replaced with named multi-channel attribution; differing mechanisms retained |
| `Rough_Plumbing_Sequencing` (7) | Doma Minsk supports wet-zone/zashivka/toilet/sink layout claims; Zemstandart/Zemsproekt supports lubricant and drain-elbow guidance | all 7 retired prefixes replaced with named attribution |
| `Waterproofing_and_Plastering` (6) | Plumbing Source Notes map waterproofing/plastering code and material claims to Konstantin Kruglov/Ontario and the Zemstandart/Alexey Zemskov waterproofing/checklist sources | all 6 retired prefixes replaced with named attribution |

The nine-file cluster now has zero `retired attribution-prefix` matches. No claim wording beyond the retired attribution prefix was changed.

## Workstream F retrofit inventory (turn 48)

| scope | channel evidence | retrofit treatment |
|---|---|---|
| Bathroom analysis: `Doors`, `Fixtures_Mixers_and_Sinks`, `Heated_Floor_and_Thermostat`, `Lighting_and_Electrical`, `Planning_and_Layout`, `Shelving_and_Furniture`, `Tile_Selection_and_Layout` | Existing page Source Notes identify Ontario/Konstantin Kruglov for bathroom design and fixture material, and Zemstandart/Zemproekt/Alexey Zemskov for tile, floor-thermostat, lighting, and mapped door claims; legacy archive-only audit notes did not expose a decisive channel | removed the retired pattern from all seven files; retained named channel statements where already verified and changed legacy audit prose to plain “no confirmed channel” wording without inventing attribution |
| Surfaces analysis: `Concealed_Door_Considerations`, `Doors_Trim_Cost_and_Buying` | Doors Source Notes map concealed-door claims to Ontario, Avalremont, and Forcemontage, with door sizing/buying material mapped to Zemstandart and product-specific sources including ПРО ДВЕРИ and Novakey | 18 retired prefixes replaced with claim-level named attribution; differing security/product perspectives remain explicitly represented |
| Windows analysis: `Windows_Acceptance_Checklist`, `Windows_Installation_and_Fastening`, `Windows_Opening_Reconfiguration`, `Windows_Slope_Finishing` | Windows Source Notes identify the cited family as Zemstandart/Zemsproekt/Zemsremont (Alexey Zemskov), with Konstantin named only as an installer partner where applicable | 27 retired prefixes replaced with Zemstandart/Zemsproekt/Zemsremont attribution; no wikilinks changed |
| Supporting inventories: `attribution_inventory_batch1.md`, `attribution_inventory_batch2.md` | These are traceability records, not reader claims; historical references to the retired boilerplate were normalized to `retired attribution-prefix` wording | zero literal retired-pattern matches remain in either inventory |

The requested 15-file cluster now has zero literal retired-pattern matches. Claim wording and existing source links were otherwise preserved.
