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
| Ceilings: legacy Do/Don't material cited only to archive text without a decisive `channel:` field | archive source-note entries listed in the page | `attribution: unconfirmed — cited archive extraction does not isolate a channel in frontmatter` |
| `13_Surfaces_and_Finishes/Doors_and_Trim.md`: door anatomy, openings, concealed doors, entrance doors, swing direction, materials and buying | `YT_yHmEQTqduDk`, `YT_ludvy76HGSU`, `YT_c4b7iyg8v5U`, `YT_-HKwxCBa40k`, `YT_ti8J19zY0EM`, `YT_D2Qz6s8eNoU`, `YT_oVf6AyxJjd0`, `YT_7Vd95idVXak`, `YT_COhFXPyfXxM`, `YT_Mfzce0Qm4HM`, `YT_WMc_AjUqQ-4` | Ontario / Konstantin Kruglov where `YT_yHm...` is cited; Zemstandart / Alexey Zemskov for ZEMS notes; Forcemontage for concealed-door facts; Sergey Gusev / ПРО ДВЕРИ for manufacturer/material claims |
| `13_Surfaces_and_Finishes/Flooring_Guide.md`: transitions, matching, laying direction, glue-down technique, retail-tier warning and sequencing | `YT_PwJsksBs4Ek`, `YT_lOMxNoyW_NE`, `YT_XFhz1NXlln8`, `YT_cJLZebMtW7A` and the cited archive entry for glue-down technique | Zemstandart / Zemproekt or Zemstandart / Zemsproekt as recorded; archive-only claims are marked unconfirmed |
| `13_Surfaces_and_Finishes/Walls_and_Paint.md`: substrate, masonry, false walls, radiator niches, load-bearing openings, layout, partitions and finish interaction | `YT_zPR8PGWq5lA`, `YT_8kOUv9EVQTQ`, `YT_g7Cuj1p-0CA`, `YT_Qs_FxXdsq40_masonry_glue_foam_technique_260`, `YT_Y-eITaok1Gw`, `YT_p-6OI34C6bw`, `YT_u3UuZN9LHg0`, `YT_sJ8UZj36TMQ`, `YT_Eq0kg2hD-Ws`, `YT_F5v7eI3ry1M`, `YT_EnSpVCSUiqg` | Zemstandart / Zemproekt or Zemstandart / Zemsremont per note; exact mixed/guest channels are retained when the note distinguishes them |
| Walls: claims citing `note 1`, `note 2`, or `note 3` without a linked extraction-note target | the page's own Source Notes block and the referenced detail notes | `attribution: unconfirmed — the guide's local note number does not expose a unique extraction-note `channel:` value` |
| `13_Surfaces_and_Finishes/Windows.md`: profile, fastening, slopes, hardware, replacement and acceptance | `YT_6_cH35u4ouM`, `YT_AGjYrwqilNA`, `YT_gjTGr8j6-DA`, `YT_nb3L-k69yx8`, `YT_qwIRfgn1Tog`, `YT_XFrmhhM1ogg`, `YT_XmtGo4BE1bw`, `YT_irOVnHty0fc`, `YT_NhGzB1L7hM`, `YT_uBNF5ZYOE0Y`, `YT_IAZreuaqhjg` | Zemstandart / Alexey Zemskov or Zemstandart / Zemsproekt; guest/technical contributors are named only where the note's frontmatter identifies them |
| `14_Furniture/Wardrobes_and_Storage.md`: sizing, walk-ins, wardrobe tradeoff, client cases and worked layouts | `YT_RyHzFDGgqKA`, `YT_n0O47DdhATw`, `YT_o4KitYl8vpU`, `YT_Xh7uwbKVmfA`, `YT_VgsPDOcPV7c`, `YT_kj503mBQXq8`, `YT_hVFmcw1H2Rk`, `YT_pVMvsuhrwWs` | Zemstandart / Zemproekt; `YT_pVMvsuhrwWs` is used only for its source-note channel, not generalized to all furniture claims |

## Editing rule and exclusions

The guide claim itself is the unit of editing. A source name is woven into
that claim's sentence while the existing `[source: ...]` footer is retained.
Where a claim is backed only by an archive note, a local `note 1/2/3`, or a
mixed note whose channel cannot isolate the particular sentence, the sentence
receives `attribution: unconfirmed — <reason>` instead of a guessed name.

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
| Plumbing: `Leak_Protection_Systems`, `Water_Heaters`, `Shower_Podium_and_Drains`, `Hygienic_Shower_and_Towel_Warmer`, `Wall_Hung_Toilet_Installation` | mixed, single-account, and archive-backed notes; the cited note fields do not isolate a decisive channel for the edited claims | inline `attribution: unconfirmed` with archive, mixed-source, or non-isolated reason; original source footers retained |
| Plumbing: `Pipe_Material_Selection` | mixed and single-account claims; `YT_1_IcoSaNKP4` is cited for corroboration but does not isolate every sentence | named channel withheld for aggregate claims; inline unconfirmed reasons added |
| Doors: `Entrance_Doors` | linked extraction notes and manufacturer pricing note do not isolate a decisive channel for the edited claims | inline `attribution: unconfirmed`; no claim meaning or source footer changed |

## Detail-page completion inventory (turn 18)

| detail pages edited | source/channel evidence | attribution treatment |
|---|---|---|
| Plumbing: `Rough_Plumbing_Sequencing`, `Waterproofing_and_Plastering` | cross-source, regulatory, and archive-only claims; cited notes do not isolate a decisive channel for the edited sentences | inline `attribution: unconfirmed` with cross-source, jurisdiction, or archive reason |
| Plumbing: `Cost_Drivers_and_Buying_Guidance` | points-pricing claim is backed by the frontmatter-identified RemontHochu.ru note; other claims are not channel-isolated | RemontHochu.ru named only for the points-pricing claim; other edited claims unconfirmed |
| Doors: `Material_and_Finish_Tiers`, `Rough_Opening_and_Casing_Sizing`, `Style_Hardware_and_Security` | mixed, single-account, and archive-only claims; source footers do not isolate one channel for most edited sentences | inline `attribution: unconfirmed`; original wording, footers, and wikilinks retained |

## Accumulated-detail audit and guide start (turn 20)

| scope | audit/source finding | attribution treatment |
|---|---|---|
| Detail audit: Plumbing Cost Drivers and Doors Style/Hardware | residual claim sentences lacked sentence-level attribution after earlier bounded edits | archive, jurisdiction, or non-isolating claims marked `attribution: unconfirmed` |
| Guide start: `Flooring_Guide.md` | guide section labels identify Zemskov/Zemstandart, while existing source notes include archive-only single-account evidence | named Zemstandart / Alexey Zemskov only where the guide's cited section makes that channel explicit; existing single-account caveats retained |
| Guide start: `Walls_and_Paint.md` | first substrate/deviation section cites an archive note without a decisive `channel:` field | first four claims marked `attribution: unconfirmed`; no channel inferred from the section heading |

## Final guide start and untouched-analysis audit (turn 22)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: `Windows.md`, `Wardrobes_and_Storage.md` | guide source-note targets reviewed; the edited guide claims do not have decisive `channel:` frontmatter | inline `attribution: unconfirmed`; no channel inferred from guide headings |
| Windows analysis: `Windows_Measurement.md` | first measurement claims reviewed; cited analysis notes do not isolate a decisive channel | first three claims marked `attribution: unconfirmed`; remaining Windows analysis claims require a further bounded pass |
| Electrical/Heating analysis audit | multiple untouched analysis pages still contain claim prose without inline attribution, including Electrical Key Concepts and Planning and additional Electrical/Heating detail pages | identified for follow-up; Workstream B detail acceptance remains open |

## Windows/Furniture continuation and analysis audit (turn 24)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: `Windows.md`, `Wardrobes_and_Storage.md` | remaining edited claims are backed by mixed or source-note targets without decisive `channel:` metadata | inline `attribution: unconfirmed` with non-isolating-source reason |
| Windows analysis: `Windows_Quality_and_Buying`, `Windows_Slope_Finishing`, `Windows_Measurement` | cited notes are single-account, archive-only, or channel-non-isolating for the audited claims | inline `attribution: unconfirmed`; source footers retained |
| Electrical/Heating analysis: `Electrical_Buying_and_Hiring`, `Heating_Type_Selection` | audited comparison/buying claims do not expose decisive channel metadata | inline `attribution: unconfirmed`; remaining Electrical/Heating analysis claims still require a full bounded audit |

## Windows/Furniture and Electrical/Heating continuation (turn 26)

| scope | source/channel finding | attribution treatment |
|---|---|---|
| Guides: remaining `Windows.md` and `Wardrobes_and_Storage.md` claims | remaining claims use mixed, single-account, or non-isolating source-note support | inline `attribution: unconfirmed`; guide claim starts now have no unmarked `**` prose |
| Windows analysis: `Windows_Hardware_Selection`, `Windows_Installation_and_Fastening` | cited technical notes do not isolate a decisive channel for the edited claims | inline `attribution: unconfirmed`; original source footers retained |
| Electrical/Heating analysis: `Rough_Electrical_Sequencing`, `Temporary_Construction_Electrical`, `Heating_Placement_Rules` | cited technical claims are source-non-isolating or single-account | inline `attribution: unconfirmed`; further Electrical Key Concepts and Windows analysis claims remain for audit |

## Detail-page continuation inventory (turn 14)

| detail-page family | claim/source inventory | attribution treatment |
|---|---|---|
| Plumbing: `Fixture_Stubout_Coordinates` | `YT_ssS7-TdXhu0` for the coordinate grid; `YT_fSEPr5fpfPM` for kitchen-group offset | Zemstandart / Alexey Zemskov for the decisive frontmatter-backed notes |
| Plumbing: `Water_Inlet_Node_Components`, `Pressure_and_Water_Hammer` | mixed and archive-derived source paragraphs; no single channel isolates the aggregate claims | `attribution: unconfirmed` with a mixed/archive reason; no channel inferred from page family |
| Doors: `Concealed_Door_Considerations`, `Doors_Trim_Cost_and_Buying`, `Door_Swing_Direction` | archive-only, mixed, and single-account claims; linked note targets do not consistently expose a decisive `channel:` field | `attribution: unconfirmed` with the specific archive/mixed/non-isolated reason |
| Ceilings | filesystem check found no `13_Surfaces_and_Finishes/analysis/*Ceil*` file; no separate claim-bearing detail page exists | no detail edit required; Ceilings remains guide-level |
