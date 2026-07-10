# Kickoff #20 -- plant-app: dry-bean harvest WINDOW + new crop

**Owner:** plant-app / plant-astro. **Blocks cert?** No (dataset ships window-ready). **Origin:**
dry-bean GS anchor (canonical `bead0bc3`, 2026-07-10). Spec/plan in `docs/superpowers/{specs,plans}/
2026-07-09-dry-bean-gs-anchor*.md`.

## What landed
A new certified crop `dry-bean` (Dry Beans) -- the 125th crop / 115th certified, and the first crop
authored to surface a harvest **window** rather than a single harvest date.

## The ask
1. **Pick up the new crop.** `dry-bean` arrives on the next submodule bump; confirm it renders (journey
   cards, calendar, varieties: Black Turtle / Pinto / Navy / Kidney / Jacob's Cattle).
2. **Render the harvest as a WINDOW, not a point.** The `harvest` growth stage carries
   `day_range_from_sow: [90, 100]`. `crop-timing.ts` (`daysToHarvestFromStage`) already reads the ladder;
   surface the min->max as a date range ("Harvest window: <date> to <date>"), not a single day. A July 1
   sow -> harvest window **Sep 29 - Oct 9**.
3. **Show the dry-down lead-in + cure follow-on.** `dry_down` (`[70,92]`) is the "your beans are drying
   down, be patient" card before the window; `cure_thresh` (`[95,112]`) is the post-harvest "cure until a
   bean shatters, not dents, before storing" card.
4. **Humid-region notes (Option C).** `fl_peninsula` / `se_gulf` / `hawaii_tropical` carry `region_notes`
   advising indoor drying (warm oven / dehydrator) because the humidity molds field-dried pods; render
   them. A future how-to ARTICLE on indoor bean-drying for humid climates should link from these guides.

## Data facts the app can rely on
- `harvest_window_days` is intentionally **ABSENT** (one-shot dry harvest). The window is the `harvest`
  stage's `day_range_from_sow`, NOT that field -- do not synthesize a window from `harvest_window_days`.
- `succession_policy.suitable = false` (single full-season crop; no succession UI for this crop).

## Verify
`npm run build:guides`; promotion-checklist count assertions (125 crops / 115 certified); `npx jest`.
See memory `dataset-shape-change-breaks-frontends` -- grep for the new slug + `npm run build` after the bump.
