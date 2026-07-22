# Kickoff: Nevada plant-app REGION_STATES + southern-NV ZIP3 fence (roadmap item 10)

**For:** a fresh plant-app session.
**From:** the plant-dataset session that shipped the real Nevada high-desert region.
**Status:** committed, NOT YET pushed (Trevor confirms push before you sync); no plant-astro bump
this session.

## Sync/rebuild off this canonical

```
crops_data_final.json  sha256 = 9b4c478ab90348b4f47c9527f9340217c8d3a3d50f947463bb59175f3c961dad
dataset commit = fe61424   (bump/sync assets off this, once pushed)
```

## The headline: a real `nevada` region now exists, dataset side is done

The dataset shipped a real, authored Nevada high-desert region, `nevada`
("Nevada: Mojave High Desert (Las Vegas Valley)", `zone_span` `["8","9","10"]`), across all 111
certified region-carrying crops. It is the fifth authored region after RGV, PNW, mid-Atlantic, and
mid-South. Before this, southern-Nevada ZIPs rode generic frost-anchored zone dates whose flat back
half was actively misleading: it showed continuous growing through both the Jun-Sep >90degF fruit-set
abort AND the real late-November frost return. The remaining gap is entirely app-side: nothing in the
app yet points Las Vegas Valley ZIPs at `nevada`.

## What you need to do

### 1. `REGION_STATES`: map `nevada` to NV

Add `nevada` to the region-to-state map, mapped to Nevada (`NV`), the same shape as the existing
region entries (`low_desert_az`, `warm_arid`, etc).

### 2. `ZIP3_REGION_HINT`: fence the southern Clark County ZIP3s to `nevada`

This is REQUIRED (unlike mid-Atlantic / mid-South, which needed no fence). Nevada's state signature
spans two very different climates: the southern Mojave (Las Vegas Valley, this region) and northern
Nevada (Reno / Carson City / Elko / Ely), which is high, cold, continental z5-7 and belongs on
`northern_tier`, not the Mojave calendar.

Fence **only** the southern Clark County / Colorado River ZIP3s to `nevada`:

| ZIP3 | area | in `nevada`? |
|---|---|---|
| **889** | North Las Vegas, Nellis | YES (z9) |
| **890** | Las Vegas, Henderson, Laughlin (z10), Mesquite/Pahrump (z8) | YES |
| **891** | Las Vegas / Spring Valley | YES (z9) |
| 893 | Ely (eastern NV, high desert) | NO -> northern_tier (z5-6) |
| 894 / 895 | Reno / Sparks | NO -> northern_tier (z6-7) |
| 897 | Carson City | NO -> northern_tier (z6-7) |
| 898 | Elko (NE NV) | NO -> northern_tier (z5-6) |

So: `ZIP3_REGION_HINT` sends `889`, `890`, `891` to `nevada`; the rest of NV falls through to the
cold default. This is the mirror of RGV's 785xx fence and PNW's west-side fence. Confirm the exact
889/890/891 membership against `zip-zones.json` at implementation time (the z8/z9/z10 split within
the fence resolves per-ZIP from the zone table; the fence only decides state+region).

### 3. No `isWarm` (#32) dependency for this region

Unlike mid-Atlantic and mid-South (whose z7 halves are blocked by the `isWarmZone` gate until kickoff
#32 lands), **every Nevada belt zone is z8/z9/z10, all `>= 8`, so all are `isWarm`** and resolve on
the standard warm assignment path. Nevada delivers fully as soon as the fence above is in place, with
no dependency on the #32 temperate-region resolution fix. (The "small z7 tail" noted for NV in the
kickoff-#32 table is northern-NV z7, which is `northern_tier`, not part of this region.)

## What the app now surfaces for `nevada`

- **Region calendars** for all 111 crops (spans + per-zone `resolved_by_zone` read at runtime, same
  as every other region -- no app data change beyond the sync).
- **The chill table** `region_chill_delivered.nevada = {"8":[500,900], "9":[300,700], "10":[150,450]}`
  (displayed as "your area banks ~X chill hours"), trial-anchored at z9 (UNR SP-20-07 North Las Vegas
  orchard).
- **Apple variety steering** in the region's `chill_basis_*` prose: the field-confirmed reliable picks
  (Dorsett Golden, Anna, Pink Lady, Mutsu, Fuji, Granny Smith) named, the high-chill tier (McIntosh,
  Honeycrisp, Zestar!, Empire, Golden Delicious, Jonagold, Liberty) flagged as unproven for Las Vegas.
- **The onion `day_length_note`** (intermediate-day at ~36degN) -- the same per-zone day-length
  explainer surfaced for the other regions (see kickoff #36 for the render pattern).

## Notes

- No plant-astro bump was done from the dataset session (that is the plant-astro session's job,
  after the push). plant-astro consumes the spans + chill band + calendars automatically at build.
- The desert delta worth knowing for any UI copy: warm-season crops here run a SINGLE spring window
  with a summer heat break and NO fall replant (the opposite of Phoenix's two-season desert
  calendar); cool-season crops keep the two-window spring + fall shape.
