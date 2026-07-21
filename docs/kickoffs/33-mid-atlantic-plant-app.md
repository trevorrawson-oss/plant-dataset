# Kickoff (TO plant-app): Mid-Atlantic region consumption (roadmap item 8)

**For:** a plant-app session. This is the app-side handoff for the `mid_atlantic` region, shipped on
the dataset side 2026-07-20 (canonical `af5dcee9`, committed; the dataset repo push is Trevor-gated).
**Paired with:** the dataset region build (`docs/superpowers/{specs,plans}/2026-07-20-mid-atlantic-region*`,
kickoff #31). Mirrors the RGV (#26) / PNW (#28) app handoffs.

## What shipped on the dataset side
A real Mid-Atlantic region `mid_atlantic` (`zone_span ["7","8"]`, NC/VA/MD/DC/DE/NJ/PA Piedmont +
Coastal Plain) across all 111 certified region-carrying crops: `regions.mid_atlantic` cell per crop +
`region_chill_delivered.mid_atlantic`. Frost-anchored; the user-visible value is the FALL planting
cycle for warm-season annuals (tomatoes, cucumbers, squash, beans) that the generic zone dates omit.

## App-side work

### 1. `REGION_STATES` + taxonomy (the standard wiring)
- `REGION_STATES.mid_atlantic = ['NC','VA','MD','DC','DE','NJ','PA']` in `src/lib/zones.ts`.
- Add the `mid_atlantic` row to `assets/data/regions.json` (id, label "Mid-Atlantic: Piedmont and
  Coastal Plain", zoneSpan [7,8]) once the dataset submodule bump carries the new region -- confirm the
  regions.json sync path picks it up (same path RGV/PNW used).
- `SHORT_REGION_LABEL.mid_atlantic` for the tight Today-eyebrow slot (e.g. "Mid-Atlantic").

### 2. NO ZIP3 fence expected (confirm)
Unlike RGV (785xx) and PNW (west-side), this belt has **no adjacent-but-different climate pocket
sharing its state+zone signature** -- the seven belt states are wholly Mid-Atlantic in character within
z7-8, and none overlaps another warm region's `REGION_STATES`. So a plain state+zone match should be
correct with no ZIP3 exclusion. Confirm against `zip-zones.json` during wiring; if a stray pocket
appears, fence it, but the dataset-side expectation is none.

### 3. THE Z7 DEPENDENCY -- this region is the first real consumer of kickoff #32
`mid_atlantic` spans z7-8, and **z7 holds the majority of the belt (3,131 ZIPs vs z8's 1,444)**. But
`src/lib/zones.ts:resolveFromZip` currently only ASSIGNS a region for zones >= 8 (`isWarmZone`). So
until the **temperate-region resolution fix (kickoff #32, the `isWarm` decoupling)** lands, a z7
Virginia/Maryland/NJ grower will NOT be assigned `mid_atlantic` -- they fall back to `northern_tier`'s
generic z7 cell instead of the authored Mid-Atlantic one (with the fall window). The z8 half (NC
Coastal Plain, DC, VA Tidewater) resolves fine with the standard wiring above.

- **If #32 has already landed** (the plant-app session was working it as of 2026-07-20): a z7 VA ZIP
  should flip to `mid_atlantic` immediately once this region's `REGION_STATES` + regions.json row are
  in. Verify a z7 VA ZIP resolves `mid_atlantic` (not `northern_tier`) and renders the fall-cycle
  calendar (e.g. cherry-tomato showing a Jul-Aug fall plant / Sep-Oct fall harvest).
- **If #32 has NOT landed:** wire the z8 half now; the z7 half delivers when #32 lands. Do not flag
  `mid_atlantic` `isWarm: true` to force z7 -- it is a temperate, not warm, region (that is exactly
  what #32 exists to handle).

## Reference
- Dataset canonical `af5dcee9` (the promote); `docs/reviews/notes/2026-07-20/mid_atlantic_promote_dryrun.md`.
- The z7/z8 ZIP counts + the `isWarm` mechanism: `docs/kickoffs/32-plant-app-temperate-region-resolution.md`
  and `docs/region_coverage_roadmap.md` (the temperate-region resolution section).
- plant-astro consumes the new region's spans + chill band + calendars automatically on the submodule bump.

## Owner split
Dataset side is done (committed, Trevor-gated push). This kickoff + the plant-astro submodule bump are
the app/astro sessions' work, Trevor-gated.
