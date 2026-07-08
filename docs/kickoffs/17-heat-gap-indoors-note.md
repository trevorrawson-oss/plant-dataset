# Kickoff #17 -- plant-astro: heat-gap `indoors` note

**For:** a plant-astro session (rendering; the dataset side is done).
**Trigger:** lands via the plant-astro submodule bump (gated on Trevor).
**Dataset change:** plant-dataset `9d1193eb` -> `1372c299` (2026-07-08), the heat-gap indoors flip.

## What changed in the data

In 22 region-zone cells, the 12-month `calendar[]` now shows `indoors` on a month that
used to show `heat_pause`, wherever a real indoor-start window covers that hot month as a
core month. This surfaces the actionable "start your fall seedlings indoors now" during
the summer heat pause, instead of only the passive "too hot."

Cells: broccoli + kohlrabi `ca_interior` (Jul) and `ca_south_coast` (Aug); beefsteak +
heirloom-tomato `fl_peninsula` (Aug + Sep); celery across `se_gulf` / `ca_interior` /
`ca_desert` / `warm_arid` / `low_desert_az` / `fl_peninsula`.

Nothing else changed -- stage ids, `day_range_from_sow`, and every other field are
byte-identical. `indoors` is already a valid calendar token, so the existing renderer
shows it with no change. **This part is already correct on screen** (an `indoors` month in
July is truthful on its own).

## The new work: the derived note

A heat-gap `indoors` cell should carry a short explanatory note. **Derive it at build time
from existing canonical fields** -- do NOT expect a note field in the data.

**Which cells get the note (the render trigger, fully data-derivable):**
an `indoors` calendar month whose index (1-12) is in that cell's `heat_pause.months`.
(A normal spring `indoors` month is NOT in `heat_pause.months`, so it gets no note.)

**Compose the note from three structured fields:**

| input | field | example (broccoli) |
|---|---|---|
| what the heat does | `heat_effect` | `crown_failure` |
| the safe-transplant temp | `heat_threshold_f` | `86` |
| the fall framing | `second_planting` (or the fall harvest window) | fall crop |

Map `heat_effect` -> a verb phrase: `crown_failure` -> "form heads",
`poor_fruit_set` -> "set fruit", `quality_loss` -> "grow well",
`bolting` -> "grow without bolting" (fall back to "grow well" for any unmapped value).

**Template (dual-register; beginner warmer, seasoned terser):**
> beginner: *"Too hot for {crop} to {effect_phrase} outside now -- start seeds indoors for a
> fall crop, and set them out once daytime highs cool to about {heat_threshold_f}°F."*

Coverage of the current 5 crops: broccoli (86, "form heads"), kohlrabi (75, "grow well"),
celery (75, "grow well"), beefsteak + heirloom-tomato (92, "set fruit"). All carry both
fields. If `heat_threshold_f` is ever absent, omit the temp clause gracefully.

**Optional per-cell override (reserved, not populated yet):** if a cell later carries
`heat_gap_note_beginner` / `heat_gap_note_seasoned`, use that verbatim instead of the
derived text. (Added only if the derived note reads too generic.)

## Steps

1. Bump the plant-astro submodule to `1372c299` (per Trevor).
2. Implement the derived-note logic above (render trigger + template).
3. `npm run build:guides` + `npx jest`.

## Verification already done on the dataset side

`gate_all` PASS (114/114), `whole_crop_gate` A5b PASS, `release_verify` clean, footprint =
ONLY `calendar[]` tokens (heat_pause -> indoors) on the 22 cells. Spec + plan:
`docs/superpowers/specs/2026-07-08-heat-gap-indoors-flip-design.md`,
`docs/superpowers/plans/2026-07-08-heat-gap-indoors-flip.md`.
