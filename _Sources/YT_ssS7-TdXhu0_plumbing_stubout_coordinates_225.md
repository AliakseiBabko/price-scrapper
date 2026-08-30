---
source_type: video transcript (single-speaker technical reference explainer, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=ssS7-TdXhu0
video_id: ssS7-TdXhu0
transcript_file: _Archive/processed_sources/20260818_plumbing_stubout_coordinates_225_9d568cd7.txt
fetched: 2026-08-18
upload_date: 2023-08-01 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart/Zemsproekt (Alexey Zemskov)
regional_applicability: not stated in-video — level 2/channel-branding only (Moscow, per this channel's established convention)
currency: not applicable — no pricing stated in this source
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart: "How NOT to Do Plumbing in an Apartment?" (#225, YouTube ssS7-TdXhu0)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Category 4 "clear technique/how-to" batch, chunk 1. **One of the single most valuable sources processed from this channel to date** — a complete, precise rough-plumbing stub-out coordinate reference by fixture type (sink, shower, tub, toilet+hygienic-shower, urinal, washing machine, kitchen sink with/without an adjacent washer). All heights measured from finished-floor level unless stated otherwise. Minimal promotional content (one brief marketing-aside joke, matching the sibling `yt_qkUo7NNqbGM` filmed the same day).

## Plumbing — Stub-Out Coordinate Reference by Fixture

**Color convention**: hot water = red, cold water = blue, drain = grey.

### Sink/basin (раковина)
- Drain: 50mm diameter, centered on the sink's centerline, at **500mm** from finished floor. (Note: transcript audio says "500 сантиметров," almost certainly an ASR/speech slip for 500mm given every other figure in this source is in mm and 500cm would be absurd for a sink drain — treated as `uncertain`/corrected to 500mm.)
- Hot/cold supply: at **600mm** from finished floor, offset **50mm left (hot) / 50mm right (cold)** from the same centerline.

### Shower (душевая, built-in pan with integrated trap)
- No separate floor-drain stub-out needed — standard modern practice uses a built-in shower pan with its own integrated trap.
- **Reference height is measured from the shower podium/platform height, not the general bathroom floor level.**
- Hot/cold supply: **1100mm above the podium**, offset **75mm left (hot) / 75mm right (cold)** from the shower pan's centerline.
- **Critical distinction flagged explicitly**: standard shower-mixer center-to-center spacing is **150mm** (75+75mm) — do not confuse with the sink's 50+50mm=100mm spacing, which is not a fixed mixer-fitting spacing at all (just two closely-grouped flexible-hose stub-outs, minimized to save space under the sink).

### Bathtub (ванна)
- Determine tub placement first, mark its centerline.
- Drain: 50mm diameter, on the centerline, at **30-100mm** from finished floor (not less than 30mm, not more than 100mm).
- Hot/cold supply: offset **75mm left / 75mm right** from centerline, at **800mm** from finished floor.
- **Reasoning for 800mm height**: high enough that the mixer isn't crowding the tub rim, low enough that water doesn't fall a long distance and splash onto the floor.

### Toilet with hygienic shower (унитаз с гигиеническим душем)
- Center the toilet on its installation zone, mark centerline.
- Thermostatic-mixed-water outlet for the hygienic shower: offset **300mm strictly to the RIGHT** of centerline, at **800mm** from finished floor.
- **Handedness mechanism, extends this store's existing handedness-based placement content**: most people wipe with the same hand they wash with (typically the right hand for right-handed people), so the sprayer/wand should sit in the LEFT hand — placing the outlet to the right of centerline means the wand naturally hangs to the seated user's left. **Explicit mirror-image exception for a Muslim household**: religious practice specifically requires the left hand for this task, so the outlet should be mirrored to the opposite side for such a client.

### Urinal (писсуар) — flagged as rare in residential units, still covered
- Find centerline first.
- Drain: 50mm diameter, at **100-400mm from floor, model-dependent** (not a fixed height).
- Cold-water supply: **100mm above the drain outlet**, same centerline.
- **Critical rule**: the cold-water supply height must be set relative to the drain outlet's position, **never** independently measured from finished floor — and the drain's own position must come from that specific urinal model's own installation instructions, never a universal figure.

### Washing machine (стиральная машинка)
- No fixed centerline convention — unlike other fixtures, horizontal position is flexible (can be offset left or right of the machine's own centerline) depending on which side is more convenient for connection, influenced by adjacent fixtures. A separate video (not covered here) is referenced for fine-tuning this offset.
- Drain: 32mm diameter, at **500mm** from finished floor.
- Cold-water supply: **150mm from the drain's centerline**, same vertical axis.

### Kitchen sink, WITHOUT an adjacent washing machine (кухня без стиралки) — includes dishwasher connection by default
- Sink drain: 50mm diameter, at **200mm** from finished floor.
- Sink cold-water supply: **150mm above the drain**, same vertical axis.
- Sink hot-water supply: **75mm horizontally left** of the cold-water outlet, same horizontal axis.
- Dishwasher cold-water supply: another **75mm further left** (150mm total left of the sink's cold supply), same horizontal axis.
- Dishwasher drain: 32mm diameter, at the intersection of the dishwasher's own vertical axis and the sink drain's horizontal axis.
- **Explicit warning: never compress this coordinate grid to save space.** The hot/cold supply spacing (75mm gaps) could technically be tightened to 50mm without immediate issues, but the sewage/drain lines cannot: at 32-50mm diameter, the required chase width plus mandatory drain slope means compressed spacing forces extra elbow/joint bends and incorrect slope angles — "guaranteed" to cause intermittent drainage problems. This grid is the minimum spacing that avoids drain-line conflicts while leaving room under the sink for water filters and other under-sink appliances.

### Kitchen sink, WITH an adjacent washing machine (кухня со стиралкой) — different build-outward logic
- Washer drain: 32mm diameter, at **200mm** from finished floor.
- Washer cold-water supply: **150mm above the washer drain**, same vertical axis.
- Dishwasher cold-water supply: **75mm horizontally** from the washer's cold supply.
- Sink hot-water supply: another **75mm further** along the same horizontal axis.
- Sink cold-water supply: another **75mm further** along the same horizontal axis.
- Sink drain: 50mm diameter, **150mm below** the sink's own cold-water outlet, same vertical axis.
- Dishwasher drain: 32mm diameter, positioned exactly between the sink's drain and the washer's drain (centered horizontally between the two).
- Net layout: three drain outlets (washer 32mm, dishwasher 32mm, sink 50mm) and four supply outlets (washer cold, dishwasher cold, sink hot, sink cold) arranged along one horizontal band.
- Same explicit **never-compress-this-spacing** warning restated for this configuration.

## Advertising / Promotional Content Notes

Minimal — one brief opening joke about the presenter's marketing team wanting a business plug inserted, self-aware framing (matches the tone of the sibling `yt_qkUo7NNqbGM`, apparently filmed the same session), no structured CTA or pricing pitch delivered.

## Target Page(s)

No dedicated Plumbing wiki page exists in this vault yet — routed to the intermediate store's Plumbing Durable Facts section as a new, dense, highly-checkable reference subsection. Complements this store's existing DIY rough-plumbing checklist (`yt_zLJtkP6ymrg`, Category 3) — that source covers installation *technique and sequencing*, this one covers exact stub-out *coordinates* by fixture.

## Relevance to This Project's Topic

Very high — a complete, precise, directly usable coordinate reference for planning rough plumbing across every common fixture type, with explained mechanisms (not just bare numbers) for nearly every rule.

## Gaps

- No region confirmed at level 1 (spoken) — channel-convention-only (Moscow).
- No pricing content — Budgeting_Guide.md not affected.
- One figure ("500 сантиметров" for the sink drain height) is almost certainly an ASR/speech slip for 500mm, corrected in this note based on context — flagged as `uncertain`, not independently verified against a second source.
- Figures represent this practitioner's own standard convention; not verified against an official plumbing code or a second independent source.

## Recommended Downstream Routing

`tiered-knowledge-base` — Plumbing Durable Facts section of the renovation budgeting intermediate store.

## Promotion self-check

Re-read in full after drafting. The full coordinate reference for every fixture type covered in the transcript is reflected in the sections above.
