# Kickoff: PNW plant-app west-side ZIP3 fence (roadmap item 4 paired follow-up)

**For:** a plant-app session.
**Goal:** route the maritime WA/OR (west-of-the-Cascades) z8-9 ZIPs to the new `pnw` region,
WITHOUT pulling the hot-dry east-of-the-Cascades z8-9 ZIPs into a maritime calendar.
**Precedent:** this is the direct analog of the RGV 785xx fence (`docs/kickoffs/26-rgv-plant-app-zip3-fence.md`),
but harder -- see "The catch" below.

## Sync/rebuild off this canonical

- Dataset side is DONE: canonical `sha256 8dd4ac4c3b543bfbb3779fcf4fcafe0d4f34f3942476c6b21272e5c687d21503`
  (2026-07-14). Sync the plant-dataset submodule / regions.json to this SHA and rebuild.
- `pnw` is in `zone_span_gate.EXPECTED_SPANS` as `["8","9"]`; every certified region-carrying
  crop now carries a `regions.pnw` cell; `region_chill_delivered.pnw = {"8":[968,1950],"9":[700,1500]}`.

## The headline: a real `pnw` region now exists, dataset side is done

The maritime Pacific Northwest (Puget Sound, the Willamette Valley, the WA/OR coast) now has its
own authored, T1-sourced (WSU/OSU) region with honest cool-summer calendars: cool-season crops as
the strength (long season, overwintering), warm crops transplant-led and honestly marginal
(tomatoes/peppers/corn early-cultivar only; okra/sweet-potato/melons flagged not-really), and
temperate tree fruit as the flagship (apples/pears/cherries/plums fruit reliably; peaches/apricots
marginal on cool-wet springs). It replaces the generic frost-anchored zone dates that assumed a hot
summer the maritime PNW does not have.

## The catch: WA and OR each straddle the Cascades (why a plain state map is WRONG)

RGV was a clean allow-list: fence one ZIP3 group (785xx) TO `rgv`. PNW is NOT. **WA and OR each
contain BOTH a maritime west side (cool summers -> `pnw`) AND a hot, dry, continental east side
(Spokane, the Columbia Basin, Bend, Klamath Falls, Pendleton -> NOT `pnw`).** A naive
`REGION_STATES.pnw = WA, OR` would wrongly send the east-side z8-9 ZIPs to the maritime calendar,
which is the exact mistake the RGV spec's "east-side wrinkle" flagged. The east side is a
hot-summer climate; a maritime calendar there is as wrong as the generic dates were for the west.

## What you need to do

### 1. `REGION_STATES`: map `pnw` to WA, OR -- but gate it behind the ZIP3 fence (step 2)
Add `pnw -> {WA, OR}`. On its own this is necessary but NOT sufficient: it must be combined with the
west-side ZIP3 fence so only the maritime ZIPs actually resolve to `pnw`.

### 2. `ZIP3_REGION_HINT`: fence `pnw` to the WEST-of-the-Cascades ZIP3s only
Author a ZIP3 allow-list (west side -> `pnw`) OR an east-side deny-list, derived from the actual
`zip-zones.json` distribution + the Cascade divide. **The exact ZIP3 list must come from
zip-zones.json (not from this doc -- I do not have that file here).** Starting hypothesis to VERIFY:
- **West-side WA (maritime -> `pnw`):** the Puget Sound + SW-WA ZIP3s, roughly `980`-`986`
  (Seattle/Bellevue/Everett/Tacoma/Bellingham/Olympia) + the Vancouver-WA / SW-WA `986`. Coastal WA.
- **East-side WA (NOT `pnw`):** `988` (Wenatchee), `989` (Yakima), `990`-`992` (Spokane), `993`
  (Pasco/Tri-Cities), `994` (Clarkston) -- hot-summer continental; leave on their current
  (generic zone or `warm_arid`-adjacent) resolution.
- **West-side OR (maritime -> `pnw`):** the Willamette Valley + coast, roughly `970`-`975`
  (Portland/Salem/Eugene + the Rogue Valley `975` is a judgment call -- interior SW OR, warmer/drier,
  verify against zip-zones.json).
- **East/central OR (NOT `pnw`):** `976` (Klamath Falls), `977` (Bend/central-OR high desert),
  `978` (Pendleton/NE OR) -- continental; leave as-is.
Verify each boundary ZIP3 against zip-zones.json; the Cascade crest is the climate divide, and a few
ZIP3s straddle it (split those by the dominant side, or flag for Trevor).

### 3. Verify the regions.json sync path picks up `pnw`
`resolveFromZip` reads `zone_span` at runtime, so once `pnw` (`["8","9"]`) is in the synced data and
the ZIP3 fence routes a west-side ZIP to `pnw`, both zones resolve. Confirm a sample Seattle ZIP
(e.g. a `981xx`) resolves to `pnw` and a sample Spokane ZIP (`992xx`) does NOT.

## Honesty flags, do not "correct"
- The west-side-only fence is deliberate, not a simplification. The east side of WA/OR is genuinely
  a different (hot-summer continental) climate; sending it to `pnw` would be a real error.
- Warm-crop marginality in the `pnw` calendars (tomatoes/peppers early-cultivar-only; okra/
  sweet-potato/melons flagged not-really-suitable) is T1-sourced honesty (OSU EM9027), not a data
  gap -- render it, do not "fix" it to look more optimistic.
- Peaches/apricots/nectarines are `marginal` (cool-wet-spring disease), apples/pears/cherries/plums
  `fruits_reliably` -- this is the honest maritime tree-fruit story; surface it as authored.

## Definition of done
Maritime WA/OR z8-9 ZIPs (west of the Cascades) resolve to `pnw` in the app, not generic zone dates;
east-of-the-Cascades z8-9 ZIPs do NOT resolve to `pnw`. `REGION_STATES` (pnw -> WA,OR) +
`ZIP3_REGION_HINT` (west-side fence) both updated; the regions.json sync path verified end to end for
a west-side sample (Seattle `pnw`) AND an east-side sample (Spokane NOT `pnw`). Dataset side is
`8dd4ac4c`; plant-astro consumes the new region + the chill band + the tree-fruit calendars
automatically once the submodule bumps.
