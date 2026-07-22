# Kickoff #39: plant-app -- wire the `utah_dixie` region (REGION_STATES + 847xx ZIP3 fence)

**For:** a plant-app session (the app owns ZIP -> region resolution; this repo owns the dataset).
**From:** the plant-dataset Utah "Dixie" region build (roadmap item 11), 2026-07-22.
**Dataset side:** SHIPPED. Canonical `b1045e04` -> **`2c98dd2b`** (promote `d215415` + two post-promote prose/provenance cleanups, COMMITTED UNPUSHED --
Trevor confirms the dataset push; plant-astro submodule bump is a separate later step). `regions.utah_dixie`
now exists on all 111 certified region-carrying crops, `zone_span ["8"]`.

## What the app needs to do
1. **`REGION_STATES.utah_dixie = ['UT']`** -- add the region-to-state mapping.
2. **`regions.json` row + `SHORT_REGION_LABEL.utah_dixie`** -- the region metadata the app reads. Full
   label is "Utah: St. George Dixie (Mojave-edge high desert)"; a short label like "Utah Dixie
   (St. George)" is fine for the UI.
3. **A ZIP3 FENCE IS REQUIRED -- fence `utah_dixie` to `847xx` ONLY.** Utah spans two completely different
   climates:
   - The SW-Utah "Dixie" belt (St. George / Washington / Hurricane / Ivins / Santa Clara / La Verkin,
     ZIP3 **847**, z8) -> `utah_dixie`. This is only ~15 ZIPs (smaller than Alaska's panhandle).
   - The Wasatch Front and the rest of northern Utah (Salt Lake `841`, Ogden `844`, Provo `846`, Logan
     `843`, Price/eastern `845`, and the `840`/`842` ranges) is z6-7, a totally different climate that
     MUST stay `northern_tier`. Naming the region `utah_dixie` (not `utah`) is deliberate for exactly this
     reason -- do NOT resolve any non-847 Utah ZIP to this region.
   - This mirrors RGV's `785xx` fence, PNW's west-side fence, and Nevada's `889/890/891` fence.
   - **Confirm the exact `847xx` membership against `zip-zones.json`** at wiring time (St. George core is
     84770; the belt runs roughly 84720-84791). If any 847xx ZIP is actually a higher-elevation z6-7
     Washington County town (Central/Enterprise/New Harmony/Pine Valley, all 5,300+ ft), keep it out of
     `utah_dixie` -- the dataset region is the LOW-elevation z8 core only (this is exactly the elevation
     line that drives the apple/pear "marginal" verdict in the data).
4. **NO isWarm #32 dependency.** The whole belt is z8 (a warm zone), so it resolves on the standard warm
   assignment path as soon as the fence lands -- unlike the mid-Atlantic / mid-South z7 halves, this
   region does NOT wait on the `isWarm` decoupling (kickoff #32). Same as Nevada.

## Notes for the app
- plant-astro consumes the `zone_span`, `region_chill_delivered.utah_dixie` chill table, and the tree
  suitability / calendars automatically once the dataset is bumped -- no per-field app work beyond the
  region wiring above.
- Content flavor the UI can lean on: apple + pear are honestly **marginal** here (recommended only for the
  county's higher-elevation towns); the low-elevation fruit stars are apricot / cherry / fig / peach /
  nectarine / plum / persimmon / pomegranate / fig and **strawberry**; raspberry is a marginal
  fall-bearing (primocane) crop; summer (Jun-Aug) is a heat pause for tomatoes and most warm crops, with
  no fall replant (unlike a two-season desert). The chill band `[250,450]` is an honest
  elevation-bracketed inference (no USU St.-George-specific chill figure exists), flagged in
  `region_chill_delivered_provenance`.
