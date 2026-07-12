# Region zoneSpan gaps vs the ZIP table (2026-07-12, from the plant-app session)

## Why this matters now

Onboarding in the app now **auto-picks the region from the ZIP** (no chips; the
settings region editor is the correction path). The picker flows through
`resolveFromZip`, which only offers a region when `zoneSpan.includes(zone)` for
the ZIP's zone AND the region is mapped to the ZIP's state. So any real ZIP
whose zone falls outside its region's `zoneSpan` silently gets **no region at
all**: bare "Zone N" label, generic zone dates instead of the region calendar,
and the settings picker can't offer the region either.

I swept every ZIP in `zip-zones.json` (zones 8+) against `regions.json` spans.
FL is fully covered (fl_peninsula 10-11 + se_gulf 8-9), which confirms the
mechanism works when the spans are right. These are the gaps.

## Tier 1 -- a region clearly exists for these people, the span just misses them

| State + zone | ZIPs affected | Region that should cover it | Current zoneSpan |
|---|---|---|---|
| AZ zone 10 | 71 (Phoenix metro incl. 85001) | `low_desert_az` | [9] |
| HI zone 12 | 119 (most of Honolulu) | `hawaii_tropical` | [11] |
| HI zone 13 | 2 | `hawaii_tropical` | [11] |
| HI zone 10 | 1 | `hawaii_tropical` | [11] |
| TX zone 10 | 95 (Rio Grande Valley: McAllen, Brownsville) | `se_gulf` (or a new region?) | [8, 9] |
| CA zone 11 | 28 (warmest coastal LA/SD pockets) | `ca_south_coast` / `ca_desert` | [9, 10] / [9, 10] |
| LA zone 10 | 6 (around New Orleans) | `se_gulf` | [8, 9] |

Phoenix is the headline: the low desert region was BUILT for Phoenix, and
Phoenix is zone 10 in the ZIP table (2023 USDA map shift, presumably), so
zone-10 AZ users get nothing.

**Suggested fix:** widen each region's `zoneSpan` to match the zones its ZIPs
actually carry -- BUT only after checking that region's crop calendars still
make sense at the added zone (that's the dataset's call, not the app's). If a
region's dates are keyed per-zone internally, the widened zone needs entries;
if they're region-flat, confirm the hotter zone doesn't need different heat
pauses (zone-10 Phoenix vs zone-9 Tucson, zone-12 Honolulu vs zone-11). For
Rio Grande Valley TX at zone 10, decide whether se_gulf dates stretch that far
south or whether it wants its own region.

## Tier 2 -- warm-zone states with NO region at all (policy check, maybe fine)

These states have zone 8-10 ZIPs but no warm region is mapped to them, so they
get generic zone dates. Plausibly by design (the taxonomy only special-cases
the marquee warm states), but worth a deliberate yes/no since zone 8-9 PNW
(maritime) and zone 8 mid-Atlantic behave very differently from zone-8 Gulf:

- WA (302 zips z8, 129 z9), OR (199 z8, 121 z9) -- maritime PNW
- NC (793 z8, 20 z9), VA (258 z8), MD (117 z8), DC (215 z8), DE/NJ/PA (small z8)
- AR (460 z8), OK (106 z8), TN (122 z8, 1 z9), MO (6 z8)
- NV (15 z8, 94 z9, 1 z10), UT (15 z8), AK (13 z8)
- PR (2 z11, 47 z12, 126 z13) -- product-scope question

## Data quality note

~285 ZIPs in `zip-zones.json` carry an **empty state string** (109 z8, 128 z9,
40 z10, 7 z11, 1 z12). Empty state means the state-based region filter can
never match them, so they also get no region regardless of spans. Worth a look
at how those rows were generated.

## App-side contract (for whoever makes the change)

- `regions.json` is bundled into the app as-is (`assets/data/regions.json` via
  plant-app's sync). Widening a `zoneSpan` is data-only; no app code change
  needed -- `resolveFromZip`, the onboarding auto-pick, and the settings
  region picker all read the span at runtime.
- The app's onboarding auto-pick for CA/TX uses ZIP3 prefix hints
  (plant-app `src/lib/zones.ts`, ZIP3_REGION_HINT) with per-prefix fallbacks,
  validated against `zoneSpan` -- so span widenings improve those picks
  automatically (e.g. Inland Empire zone-10 ZIPs currently fall back from
  ca_interior to ca_south_coast).
- Repro for the sweep: iterate `zip-zones.json` zones >= 8, check
  `regions.json` for a warm region whose `zoneSpan` includes the zone and
  whose state mapping (REGION_STATES in plant-app `src/lib/zones.ts`) includes
  the ZIP's state.
