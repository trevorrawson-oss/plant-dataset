# To plant-app: region zone-span reconciliation -- landed & pushed (2026-07-12)

**From:** the plant-dataset session, closing the loop on your sweep report
(`docs/2026-07-12-region-zonespan-gaps.md`).
**Status:** committed AND pushed to dataset `origin/main` (tip `3f18db8`); plant-astro submodule
already bumped to it (`d333a0c`, build green 1323 pages).

## Sync/rebuild off this canonical

```
crops_data_final.json  sha256 = 7e29f4f49f5d416315f81b72d7164e3228dea3e5834edaf09673bc5c58f56204
dataset commit = 3f18db8   (bump/sync assets off this)
```

## The headline: most of your Tier-1 gaps close on a re-sync alone

The fix widened five region `zone_span`s to the 2023 USDA map. Nothing was renamed or reshaped --
`zone_span` just gained the zones its ZIPs actually carry, and every populated `resolved_by_zone`
gained the matching per-zone calendar rows. **`resolveFromZip` reads the span at runtime, so no app
code change is needed.** The single required action to light this up:

> **Re-run plant-app's sync so `assets/data/regions.json` picks up the new spans.**

The moment that lands, the ~320 ZIPs from your sweep (Phoenix, Honolulu, warm coastal CA, New
Orleans fringe) start resolving to their region instead of a bare "Zone N."

### The five widened spans (what your re-synced regions.json should show)

| Region | was -> now | your sweep gap it closes |
|---|---|---|
| low_desert_az | [9] -> **[9,10]** | AZ z10 (Phoenix metro, 71 ZIPs) |
| hawaii_tropical | [11] -> **[10,11,12,13]** | HI z10/12/13 (Honolulu, 122 ZIPs) |
| ca_south_coast | [9,10] -> **[9,10,11]** | CA z11 (warm coastal LA/SD) |
| ca_desert | [9,10] -> **[9,10,11]** | CA z11 (Inland Empire pockets) |
| se_gulf | [8,9] -> **[8,9,10]** | LA z10 (New Orleans fringe) + TX z10 (RGV, see below) |

**Scope note:** the widen touched the **108 certified crops only**. The 9 uncertified shells
(avocado, olive, artichoke, asparagus, 5 mushrooms) keep narrower spans until they are authored --
harmless, since the taxonomy build unions spans across crops, so the region still offers the widened
zones.

## Stage 2 (roadmap item 2) -- what's actually left for you

Detail lives in `docs/region_coverage_roadmap.md` (item 2 section). Three tasks:

### (a) ~285 empty-state ZIPs -- the real work, and it is a GENERATOR fix
Root cause (traced in `plant-astro/scripts/build-zip-zones.mjs`, but the same join pattern applies
wherever plant-app builds its ZIP table): each row joins PRISM zones with a **separate** frostline
ZIP->state CSV --

```js
out[zip] = [zone, zipState.get(zip) ?? ''];   // '' when the ZIP is in PRISM but not the state CSV
```

The ~285 empty states are ZIPs present in PRISM but **missing from the state file**, so the
state-based region filter can never match them regardless of spans. **Fix at the generator** (a
fuller / supplemental ZIP->state source), NOT by hand-patching rows -- a hand-patch gets wiped the
next time the table regenerates. This is **region-agnostic and one-time**: finishing RGV / PNW / any
future region never re-breaks it, because `state` is assigned upstream of all region logic.

### (b) Verify the regions.json sync path end to end
After the re-sync, confirm the 5 widened spans actually appear in the bundled `regions.json` and that
`resolveFromZip` + the settings region picker now offer those regions for a sample ZIP in each
(e.g. 85001 Phoenix -> low_desert_az; a z12 Honolulu ZIP -> hawaii_tropical). This is the "confirm the
pipe carried the change" step.

### (c) TX z10 ZIP3 fencing decision
Widening se_gulf to z10 means the **95 Rio Grande Valley z10 ZIPs (McAllen/Brownsville) now auto-match
se_gulf** (TX is in se_gulf's `REGION_STATES`). This is an **intentional interim** -- Gulf-coast
winter-garden dates are directionally right for RGV and beat a bare zone label. Your call: keep them on
se_gulf, or fence those ZIP3s (via `ZIP3_REGION_HINT`) to generic until a real RGV region ships. This
is temporary either way -- roadmap **item 3 (an authored RGV / subtropical-TX region) retires it**.

## Honesty flags -- intentional, do not "correct"

- **RGV on se_gulf is a deliberate interim** (the fencing lever above is how you tune it).
- If the app surfaces **chill hours** or the tropical-crop calendars: the 3 warm-edge chill bands
  (se_gulf z10, ca_south_coast/ca_desert z11) read slightly generous, and Honolulu carries a
  pre-existing ~25-crop generic-sourcing gap. Both are logged on the roadmap as data-quality
  follow-ups, not blockers.

## Acceptance test (re-run your own sweep)

Iterate `zip-zones.json` zones >= 8; for each, check for a warm region whose `zoneSpan` includes the
zone AND whose `REGION_STATES` includes the ZIP's state. After the re-sync:

- **Tier-1 gap table -> zero** (RGV counts as covered-via-interim through se_gulf).
- **Tier-2 no-region states -> unchanged by design** (maritime PNW, mid-Atlantic, etc. are queued
  region builds, roadmap items 4-6, not part of this drop).
- The ~285 empty-state ZIPs stay unresolved until task (a) lands -- that is the gap this stage closes.
