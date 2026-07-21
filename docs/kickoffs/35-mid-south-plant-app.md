# Kickoff (TO plant-app): Mid-South region consumption (roadmap item 9)

**For:** a plant-app session. This is the app-side handoff for the `mid_south` region, built on the
dataset side 2026-07-20 (the dataset repo push + canonical SHA are Trevor-gated).
**Paired with:** the dataset region build (`docs/superpowers/specs/2026-07-20-mid-south-region-design.md`,
kickoff #34). Mirrors the Mid-Atlantic (#33) / PNW (#28) / RGV (#26) app handoffs.

## What shipped on the dataset side
A real Mid-South region `mid_south` (`zone_span ["7","8"]`, AR/OK/TN/MO, "Mid-South: Ozark Uplands and
Delta Lowlands") across all 111 certified region-carrying crops: `regions.mid_south` cell per crop +
`region_chill_delivered.mid_south` + 6 new University-of-Arkansas / NWS `source_catalog` entries.
Frost-anchored; the user-visible value is the FALL planting cycle for warm-season annuals (tomatoes
Jul 1-15, cucumbers, summer squash, plus a UAEX fall crop for sweet-corn / bush beans / potato) that the
generic zone dates omit, and the belt's strong Aug-Sep cool-crop fall shoulder.

## App-side work

### 1. `REGION_STATES` + taxonomy (the standard wiring)
- `REGION_STATES.mid_south = ['AR','OK','TN','MO']` in `src/lib/zones.ts`.
- Add the `mid_south` row to `assets/data/regions.json` (id, label "Mid-South: Ozark Uplands and Delta
  Lowlands", zoneSpan [7,8]) once the dataset submodule bump carries the new region -- same regions.json
  sync path RGV/PNW/Mid-Atlantic used.
- `SHORT_REGION_LABEL.mid_south` for the tight Today-eyebrow slot (e.g. "Mid-South").

### 2. NO ZIP3 fence expected (confirm)
Unlike RGV (785xx) and PNW (west-side), this belt has **no adjacent-but-different climate pocket sharing
its state+zone signature** within z7-8. AR/OK/TN/MO in z7-8 are wholly Mid-South in character, and none
overlaps another warm region's `REGION_STATES` (se_gulf is GA/AL/MS/LA/SC/FL/TX; no overlap). A plain
state+zone match should be correct with no ZIP3 exclusion. The lone z9 TN ZIP (1) rides the belt verdict
(negligible). Confirm against `zip-zones.json` during wiring; the dataset-side expectation is no fence.

### 3. THE Z7 DEPENDENCY -- same as Mid-Atlantic (kickoff #32)
`mid_south` spans z7-8, and **z7 holds the majority of the belt (~1,883 ZIPs vs z8's 697)**. Until the
**temperate-region resolution fix (kickoff #32, the `isWarm` decoupling)** lands, `resolveFromZip` only
assigns a region for zones >= 8, so a z7 grower in the Ozarks / eastern OK / most of TN / southern MO
falls back to `northern_tier`'s generic z7 cell instead of the authored `mid_south` one (with the fall
window). The z8 half (central + southern AR, western TN, SE OK, MO bootheel) resolves with the standard
wiring above.

- **If #32 has landed:** verify a z7 AR/TN ZIP (e.g. Fayetteville 72701, Nashville 37201) resolves
  `mid_south` (not `northern_tier`) and renders the fall-cycle calendar (e.g. cherry-tomato showing an
  early-July fall plant / Sep-Oct fall harvest).
- **If #32 has NOT landed:** wire the z8 half now; the z7 half delivers when #32 lands. Do not set
  `mid_south` `isWarm: true` to force z7 -- it is a temperate, not warm, region (exactly what #32 handles).

## Reference
- Dataset canonical `<new SHA at promote>`; `docs/reviews/notes/2026-07-20/mid_south_promote_dryrun.md`.
- The z7/z8 ZIP counts + the `isWarm` mechanism: `docs/kickoffs/32-plant-app-temperate-region-resolution.md`
  and `docs/region_coverage_roadmap.md`.
- plant-astro consumes the new region's spans + chill band + calendars automatically on the submodule bump.

## Owner split
Dataset side build is done (Trevor-gated push). This kickoff + the plant-astro submodule bump are the
app/astro sessions' work, Trevor-gated. This is the second real consumer of the #32 temperate-region fix.
