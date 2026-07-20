# Kickoff (TO plant-app): temperate-region resolution -- decouple region assignment from `isWarm`

**For:** a plant-app session (this is a plant-app CODE change; the dataset side does not touch it).
**From:** plant-dataset, 2026-07-20. Paired with the temperate-region builds (roadmap items 8/9/7).
**Priority:** this is the **highest-leverage app-side item** in the region program, ahead of the
ZIP3 fences and the empty-state cleanup. Do it in parallel with the mid-Atlantic dataset build, not
after it. Reason: it is the only thing that lets the new temperate regions deliver their z7 half, and
it is a prerequisite worth validating end to end before three temperate regions stack up behind it.

**Scope:** `src/lib/zones.ts` (the assignment layer). The calendar layer
(`src/lib/guide-calendar.ts`) needs **no change** -- see "What already works" below.

---

## The precise problem (corrected -- read this, an earlier framing was wrong)

The app resolves planting data in **two independent layers**, and they disagree about zone 7. I first
described this as "`isWarm` strands all of `northern_tier`." **That was wrong.** After reading both
layers:

**Layer 1 -- calendar resolution (`guide-calendar.ts:resolveZoneCell`) already handles cold zones.**
When no region is passed and `zone <= 7`, it explicitly resolves `northern_tier` first:

```
const order = [];
if (zone <= 7) order.push('northern_tier');
for (const k of Object.keys(regions)) if (!order.includes(k)) order.push(k);
```

So a cold-zone grower (Minnesota z5, `location.region` undefined) **does** get `northern_tier`'s real
authored calendar today. `northern_tier` is NOT stranded. This layer is correct and stays as-is.

**Layer 2 -- region assignment at onboarding (`zones.ts:resolveFromZip`) is gated on `isWarmZone`:**

```
const warmRegions = isWarmZone(hit.zone)          // isWarmZone := zone >= 8
  ? regionsForZone(hit.zone, taxonomy)
      .filter((r) => r.isWarm)                     // and the region itself must be isWarm:true
      .filter((r) => REGION_STATES[r.id]?.includes(hit.state))
  : [];
```

For any zone < 8, `warmRegions` is empty and **no region is stored** (`location.region` stays
undefined). That is fine for a genuine cold-zone grower -- Layer 1 gives them `northern_tier`. **It is
NOT fine for the new temperate regions.**

**The actual break.** `mid_atlantic` (and `mid_south`, and `se_alaska`'s z7 core) span **z7-8**. A z7
grower in Virginia / Maryland / NJ:

1. Onboarding runs `resolveFromZip` -> `isWarmZone(7)` is false -> `warmRegions = []` ->
   `location.region` is never set to `mid_atlantic`.
2. Calendar render calls `resolveZoneCell(guide, 7, undefined)` -> no region passed -> the `zone <= 7`
   rule returns **`northern_tier`'s z7 cell**, a generic cold-continental calendar.

So the grower gets a Minnesota-style z7 calendar instead of the Mid-Atlantic one that was authored for
them (the one with the real fall planting window). The `mid_atlantic` z7 data exists in the dataset
but is **shadowed by `northern_tier` and never assigned.** The z8 half is unaffected -- it flows
through the normal warm path once the standard new-region wiring is added.

## What already works (do not touch)

- `resolveZoneCell`'s region-first branch: **once `location.region` is set, it wins.** If onboarding
  assigns `mid_atlantic`, `resolveZoneCell(guide, 7, 'mid_atlantic')` returns
  `regions.mid_atlantic.resolved_by_zone['7']` before the `northern_tier` fallback is ever reached. So
  **fixing assignment (Layer 1... er, Layer 2) fixes the calendar automatically.** No `guide-calendar.ts`
  change is needed.
- `northern_tier` delivery for true cold-zone growers. Unchanged.

## Impact (corrected framing)

These are z7 ZIPs in the belt states that would **upgrade** from `northern_tier`'s generic
cold-continental calendar to their authored region-specific calendar once the region ships AND this
fix lands. Not "blank/broken" today -- they get a real but climate-mismatched answer:

| Belt (region) | z8 ZIPs (work with standard wiring) | z7 ZIPs (need this fix) |
|---|---|---|
| Mid-Atlantic (`mid_atlantic`) | 1,444 | **3,131** |
| Mid-South (`mid_south`) | 697 | ~1,900 |
| SE Alaska (`se_alaska`) | 6 (panhandle) | 22 (panhandle) |

Nevada and Utah are z8-dominant and mostly resolve through the standard warm path; their small z7
tails are the same mechanism but low-volume.

## The fix (recommended design -- plant-app owner makes the final call)

`isWarm` currently does double duty: it gates **assignment** (above) AND drives **presentation**
(`buildLabel` shows "Zone X . Region" only when `region.isWarm`; `shortRegionLabel` / the Today eyebrow
show a region only when warm). Decouple those two jobs:

1. **Assignment becomes zone-span + state based, independent of `isWarm`.** In `resolveFromZip`,
   compute assignable regions as `regionsForZone(zone, taxonomy).filter(r => REGION_STATES[r.id]?.includes(state))`
   for **all** zones, dropping the `isWarmZone(zone)` gate and the `.filter(r => r.isWarm)`. Add
   `REGION_STATES` + `STATE_REGION_HINT` entries for the temperate regions:
   - `mid_atlantic: ['NC','VA','MD','DC','DE','NJ','PA']`
   - `mid_south: ['AR','OK','TN','MO']`
   - `se_alaska: ['AK']`
   These state sets are **disjoint** from each other and from every existing warm region's states, so
   assignment stays unambiguous (no CA-style ZIP3 disambiguation needed).
2. **Keep `northern_tier` OUT of the assignable set.** It is the silent cold default, correctly handled
   by `resolveZoneCell`'s `zone <= 7` fallback. Do NOT start assigning it as a named
   `location.region` -- that would put "Zone 5 . Northern Tier (Cold Zones)" in labels where today it
   is just "Zone 5". Simplest: `northern_tier` has no `REGION_STATES` entry, so the state filter
   naturally excludes it.
3. **`isWarm` stays, as a presentation flag only.** The temperate regions want their NAME shown
   ("Zone 7 . Mid-Atlantic" is meaningful and correct), so `buildLabel` should show a region label for
   any assigned named region, not only warm ones. Whether the temperate regions also get the warm-only
   chip UI / Today-eyebrow treatment is a UX call for the owner; the minimum is that they assign and
   label. Consider renaming `isWarm` to something honest (`showsRegionChips`? `isNamedRegion` +
   `isWarm` split?) so a subarctic maritime region is never flagged "warm" to satisfy the label logic.

The regions.json taxonomy rows for the temperate regions come from the dataset side with each region
build; this kickoff is about the resolution logic, not the data rows.

## Test guidance

- A z7 VA ZIP resolves `mid_atlantic` (not `northern_tier`) once `mid_atlantic` is in the taxonomy +
  `REGION_STATES`; its rendered calendar carries the region's fall window.
- A z8 NC ZIP still resolves `mid_atlantic` (regression: the z8 path must not break).
- A z5 MN ZIP still gets `northern_tier`'s calendar and a bare "Zone 5" label (no region assigned, no
  regression).
- A z7 KY ZIP (a state with NO temperate region) still falls to `northern_tier` -- the state filter is
  what scopes the new behavior.
- Existing warm regions (RGV z9 TX, PNW z8 WA, etc.) unchanged.

## Why now, not later

Building `mid_atlantic` at z7-8 (Trevor's decision, 2026-07-20) means the majority of its ZIPs are z7.
Shipping that region without this fix would leave 3,131 of its ~4,575 ZIPs silently on the wrong
(`northern_tier`) calendar. Landing this fix in parallel -- and confirming a z7 VA ZIP flips correctly
once `mid_atlantic` lands -- validates the temperate-region delivery path before `mid_south` and
`se_alaska` stack the same z7 dependency on top of it.
