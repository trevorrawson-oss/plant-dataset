# Asparagus — app-side closeout

**Date:** 2026-07-26
**Closes:** `2026-07-25-asparagus-timing-gaps.md`
**From:** the plant-app establishment-years arc
**Status:** all four asks resolved. Nothing is blocked on the dataset. This session can wrap.

## 1. Both rulings accepted

**RULING 1 (calendar_basis stays `frost_anchored`) — you were right, and the brief was
wrong to call it "misauthored".** The argument that settled it was yours: flipping the
field would have silently no-opped six gates on asparagus's calendar (A5 coherence, A24
placement, A25 thermal backing, nursery-run, start_indoors, coherence Bug 1), trading a
rendering bug for loss of armor. That is a strictly better reason than the one the brief
gave for flipping it.

The real defect was on the app side: plant-app had overloaded `calendar_basis` as its
perennial-vs-annual discriminator, which was never that field's contract. Fixed in
plant-app `ef7f180` — perennial-ness now derives from `archetype`, which is what actually
answers "what kind of crop is this" and is already what the app's calendar-family router
keys on. Verified across all 120 records: the old and new discriminators disagree on
exactly one crop (asparagus), so it was a one-crop correction and byte-identical for the
other 119.

**RULING 2 (`years_to_first_harvest` stays GLOBAL, not per-region) — accepted, and it
closes plant-astro spec section 9 permanently.** The app's three-state model consumes a
global range with no redesign, so nothing on our side was waiting on this. Thank you for
checking it against the two widest ranges rather than ruling from the armchair.

## 2. What we consumed

| Ask | Result |
|---|---|
| `plant_out` | **29 of 39 cells.** The 10 without are all `unsuitable` (se_gulf z10, ca_desert z11, rgv z9/z10, fl_peninsula z10/z11, hawaii_tropical z10-z13). Correct. |
| `harvest` window | **29 of 39 cells**, matching |
| `establishment_years` | **5** — and genuinely its own figure, not a copy of `years_to_first_harvest` `[2,3]`. Exactly the distinction the brief asked you to preserve. |
| `days_to_maturity` | still `[]`, consistent with every other establishment crop. Treating that as confirmed-by-convention unless you know otherwise. |

Zone 6 now reads `"Apr 1 - May 10 (dormant crowns, one-time planting)"`. The app renders
that as a real two-month plant bar.

## 3. What changed on the app side as a result

**The derived plant-month inference is REMOVED** (plant-app `ef7f180`). While asparagus
had no `plant_out`, the app inferred a single planting month from the first non-`cold_pause`
month in `calendar[]`. It was explicitly a rendering inference, not sourced data. It was
gated on `!cell.plant_out`, so your authoring switched it off with no code change, and we
deleted it rather than leave a path no crop reaches.

**This makes your new A47 perennial planting-data floor load-bearing for the app, not
just dataset hygiene.** A perennial that certifies without `plant_out` now renders an
empty plant row. That is deliberate and honest — we would rather show nothing than invent
a month — but it means A47 is the thing standing between a future perennial and a blank
row on its guide page. Worth knowing it now has a consumer.

## 4. What plant-app now depends on from the dataset

Stated plainly so a future crop does not trip it:

1. **`archetype` is the app's perennial discriminator.** A crop that should behave as a
   perennial must carry one of: `berries_woody`, `berries_herbaceous`,
   `deciduous_fruit_tree`, `evergreen_fruit_tree`, `woody_ornamental`,
   `herbaceous_perennial`. `calendar_basis` is no longer consulted for this, per RULING 1.
2. **`years_to_first_harvest` `[low, high]` drives every harvest claim** on 25 crops. The
   app suppresses harvest language entirely below `low` and hedges between `low` and
   `high`. A wrong `low` reads to the user as "you get spears next year" when they do not.
3. **`establishment_years` and `years_to_first_harvest` stay distinct.** Development vs
   food. They already disagree on fig, persimmon, cherry-sweet and elderberry, and the app
   reads them for different features. Herb's coaching gate uses the first; every calendar
   and garden-tile claim uses the second.
4. **A perennial without `plant_out` renders an empty plant row.** See section 3.

## 5. How to verify from your side

```bash
cd ~/plant-dataset && python3 -c "
import json
d=json.load(open('crops_data_final.json'))
crops=d['crops'] if isinstance(d,dict) and 'crops' in d else d
if isinstance(crops,dict): crops=list(crops.values())
c=[x for x in crops if x['slug']=='asparagus'][0]
po=sum(1 for r in c['regions'].values() for z in r['resolved_by_zone'].values() if z.get('plant_out'))
print('plant_out cells:', po, '| establishment_years:', c.get('establishment_years'),
      '| ytfh:', c.get('years_to_first_harvest'), '| basis:', c.get('calendar_basis'))
"
```

Expected: `plant_out cells: 29 | establishment_years: 5 | ytfh: [2, 3] | basis: frost_anchored`.

## 6. Open

Nothing blocking. Two optional follow-ups, neither urgent:

- Confirm `days_to_maturity: []` is intentional for the establishment class rather than an
  omission (section 2). One line closes it.
- The brief's original section 7 question is now answered by RULING 2 and can be struck.

plant-app state: pushed at `ef7f180`, full suite green (3103 tests). The OTA is being
blocked by chronic Expo-side `.hbc` processing degradation, unrelated to any of this — a
fresh bundle hash timed out identically, which reproduces a previously documented episode.
It will otherwise ride the next TestFlight build. Nothing here is waiting on the dataset.
