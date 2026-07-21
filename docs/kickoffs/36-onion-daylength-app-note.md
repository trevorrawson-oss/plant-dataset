# Kickoff (TO plant-app): onion + shallot day-length correction + the "which onion" explainer

**For:** a plant-app session. This is a small consumption note, not a new feature. It rides the
next dataset submodule bump (dataset push is Trevor-gated).
**Paired with:** the dataset change `docs/reviews/notes/2026-07-21/onion_daylength_intermediate_decision.md`.

## What changed on the dataset side (2026-07-21)
Onion and shallot day-length recommendations were corrected in the two SE temperate belts, because
the region builds had shipped `long_day` where the latitude actually calls for intermediate-day:

- **mid_south** (AR/OK/TN/MO): `long_day` -> **`intermediate_day`** in **both** zone 7 and zone 8.
- **mid_atlantic** (NC/VA/MD/DE/NJ/PA): `long_day` -> **`intermediate_day`** in **zone 8** (the
  Coastal Plain). **Zone 7 (Piedmont) stays `long_day`** -- it runs north to ~40°N.

The spring planting window was also trimmed to end in **late March** (was mid-April), because
intermediate-day onions must be set early to size up before their day-length trigger. Harvest
(day-length-anchored, May-June) is unchanged.

**No new field, no schema change, no new app logic.** The app already reads
`resolved_by_zone[zone].recommended_day_length_type` and the per-zone
`day_length_note_beginner` / `day_length_note_seasoned`; those fields simply now carry the corrected
values and prose. The corrected `plant_out` / `last_plant_date` / `calendar` also flow through
automatically.

## The "which onion" explainer (render this)
The per-zone `day_length_note_beginner` / `day_length_note_seasoned` ARE the explainer, written for
this exact purpose: they tell the grower which day-length onion to buy and why. **Please surface
them** wherever onion or shallot is shown for a mid_south or mid_atlantic ZIP (an info tooltip or a
"Which variety?" callout next to the recommendation is ideal). A grower who buys the wrong
day-length onion gets marble-sized bulbs, so this note is high-value.

A short single-register version, if you want a one-liner above the per-zone note:

> **Onions are day-length sensitive.** In the Mid-South and the Mid-Atlantic Coastal Plain, grow
> **intermediate-day** onions (like Candy or Super Star) and set them out early, February into late
> March, so they build size before summer's longest days trigger bulbing. Short-day (Southern) types
> also do well in the warm south; long-day (Northern) onions stay small here and are not
> recommended. In the cooler Mid-Atlantic Piedmont (zone 7), long-day onions are the right pick.

(That paragraph is a summary for the app to render as-is if useful; the authoritative per-zone
wording lives in the dataset's `day_length_note_*` fields and should win where both are shown.)

## Verify after the submodule bump
- A z8 Mid-South ZIP (e.g. Little Rock 72201) and a z8 Coastal-Plain ZIP (e.g. Wilmington 28401)
  show onion `recommended_day_length_type = intermediate_day` and a planting window ending in late
  March (not mid-April).
- A z7 Mid-Atlantic ZIP (e.g. Richmond area) still shows `long_day` for onion.
- The `day_length_note` renders for both onion and shallot.

## Owner split
Dataset side is done (Trevor-gated push). This surfacing + the plant-astro submodule bump are the
app/astro sessions' work, Trevor-gated.
