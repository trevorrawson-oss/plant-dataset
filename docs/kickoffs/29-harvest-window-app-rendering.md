# Kickoff #29 -- plant-app / plant-astro: render harvest as a WINDOW (roster-wide), not a single day

**Owner:** plant-app / plant-astro. **Blocks cert?** No (the dataset has shipped window-ready for the
whole roster since the timing-spine pass). **Supersedes #20** (`20-dry-bean-app-harvest-window.md`), which
asked for this on dry-bean only and was never generalized. **Origin:** Trevor, 2026-07-15/16 -- the app is
still showing a single harvest day, which is false precision; a window is more accurate and more honest.

## The problem
Real harvest timing swings with variety, weather, soil, and microclimate. A single date ("Harvest: Sep 18")
implies a precision we do not have. The app is almost certainly deriving that single date from
`days_to_maturity_mid` (a single midpoint) or `plant_date + midpoint`, and NOT consuming the window that is
already stored. Show a window.

## The principle (Trevor)
- No variety selected -> show the crop-level window (it spans the varieties + conditions).
- A variety IS selected -> center a ~2-week window on that variety's DTM datapoint (`variety DTM +/- 7 days`).
  Trevor: "a 2 week range on harvesting from the datapoint, that's accurate enough." This is a RENDERING RULE,
  no data change -- even a fixed variety still swings ~2 weeks with weather/soil.

## Data facts the app can rely on (all populated, roster-wide)

CROP (parent) level -- three equivalent sources of a window, pick per view:
- `days_to_maturity: [min, max]` -- the maturity band (e.g. field-corn `[95,120]`, popcorn `[90,110]`,
  dry-bean `[90,100]`, onion `[90,120]`). This band IS a window because it spans the crop's varieties.
- growth stage `id:"harvest"` -> `day_range_from_sow: [min, max]` -- the from-sow harvest window
  (field-corn `[110,132]`, dry-bean `[90,100]`). Add to the sow/plant date for a date range.
- per-region `resolved_by_zone[zone].harvest_start` / `harvest_end` -- an already-computed calendar-date
  window (field-corn northern-tier = `Sep 9` -> `Sep 27`). This is the simplest to render as-is.
- `dtm_anchor` (`from_sow` | `from_planting`) -- tells you what the DTM counts from.

VARIETY level:
- each variety carries a SINGLE `days_to_maturity` (a point, not a range) -- e.g. Tom Thumb 85, Robust 103,
  Black Turtle 105, Walla Walla 90. For a variety-specific window, apply `variety DTM +/- 7 days` (the
  2-week rule above). We deliberately do NOT store a per-variety range (a tolerance rule is honest + free;
  a per-variety range would be real seed-catalog authoring for ~90% overlap).

SEASON-ONLY crops (no DTM): strawberry, apple, and the tree/berry crops carry `days_to_maturity: []` and
no per-variety DTM. They render by `maturity_class` (early/mid/late) and, for trees, bloom season -- a
class-based window, not a day-count. Do not try to compute a day window for these; keep the season model.

## The ask
1. **Stop rendering a single harvest date.** Replace the `days_to_maturity_mid` / plant+midpoint single-day
   render with a window from `harvest_start`->`harvest_end` (or the DTM band applied to the plant date).
   Roster-wide, every DTM crop -- not just dry-bean.
2. **Variety selected -> `variety DTM +/- 7 days`** as the (tighter) harvest window, centered on the datapoint.
   Fall back to the crop band when no variety is chosen.
3. **Respect the tight-window crops.** A crop with `harvest_window_days` present (e.g. sweet-corn `[4,7]`)
   has a genuinely TIGHT pick window at maturity (milk stage) -- render that as a short window, not the
   wide 2-week rule. Crops where `harvest_window_days` is ABSENT (dry-bean, field-corn, popcorn, flint-corn --
   one-shot dry harvest, leave it on the stalk) use the day_range / DTM band spread. Two distinct behaviors:
   `harvest_window_days` = "how long it stays good once ready"; the `+/-7-day` rule = "uncertainty in when it
   is ready." Combine sensibly; do not synthesize a window from `harvest_window_days` when it is absent.
4. **Newly available crops:** the corn family (`field-corn`, `popcorn`, `flint-corn`) lands on the next
   submodule bump -- confirm they render (guide pages, calendar, varieties) and pick up the window treatment.

## Verify
`npm run build:guides`; render a DTM crop (dry-bean/field-corn) and confirm the harvest shows a date RANGE,
both crop-level (band) and variety-selected (DTM +/-7d); confirm a season-only crop (strawberry) still
renders its class-based season. See memory `dataset-shape-change-breaks-frontends` (grep the new corn slugs +
`npm run build` after the bump).

## Not in scope (dataset side is done)
No dataset change is needed -- the band, the harvest stage `day_range_from_sow`, and the per-region
`harvest_start`/`harvest_end` are all populated roster-wide. Only if we later want a *data-backed* per-variety
range (instead of the `+/-7-day` rule) is that a dataset field-addition (deferred; the rule is the pragmatic call).
