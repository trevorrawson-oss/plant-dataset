# Asparagus Timing Gaps — dataset session brief

**Date:** 2026-07-25
**Raised by:** the plant-app establishment-years arc (Trevor device pass)
**Repo:** plant-dataset. Nothing here requires a plant-app change.
**Companion app spec:** `~/plant-app/docs/superpowers/specs/2026-07-24-establishment-years-app-design.md`

## 1. The finding, in one line

Asparagus (crop #120, first `herbaceous_perennial`) was certified **without any timing
fields at all**, and it is the ONLY one of the 25 establishment crops in that state.

Trevor, looking at the promoted guide: *"I see there's no planting data, so we don't
actually let anyone know when to plant or transplant?"* Correct. We do not.

## 1b. HIGHEST PRIORITY, found 2026-07-25 during the app build: `calendar_basis` is wrong

**Asparagus is authored `calendar_basis: "frost_anchored"`, which is the ANNUAL basis.**
It is the only perennial in the dataset with an annual basis:

| archetype | calendar_basis | count |
|---|---|---|
| berries_herbaceous | `perennial_herbaceous` | 1 |
| berries_woody | `berries_woody` | 4 |
| deciduous_fruit_tree | `perennial_chill_gated` | 14 |
| evergreen_fruit_tree | `perennial_evergreen` | 5 |
| woody_ornamental | `perennial_woody_ornamental` | 5 |
| **herbaceous_perennial (asparagus)** | **`frost_anchored`** | **1** |

**Why this is severe.** plant-app derives its entire perennial/annual split from this one
field: `src/lib/crops.ts:28` is
`isPerennial = basis !== 'frost_anchored' && basis !== 'non_seasonal_indoor'`.
So today `STARTER_CROPS['Asparagus'].perennial === false`, and asparagus is treated as an
ANNUAL across the whole app:

- `perennialStatusForCrop` early-returns `{ supported: false }`, so My Garden never shows
  a perennial phase for an asparagus planting
- `garden-record.ts` resolves its record `kind` as annual
- the guide screen's annual-calendar branch wins over the perennial ribbon, which made
  the new establishment-year pills unreachable on the live screen

The app has landed a narrow guard for the guide-screen symptom, but the record-kind and
My-Garden consequences can only be fixed here. Until `calendar_basis` is corrected, the
establishment-year feature is inert for the one crop it was built for.

**Requested:** set asparagus's `calendar_basis` to the perennial value appropriate for a
herbaceous perennial. `perennial_herbaceous` is the closest existing analogue (used by
`berries_herbaceous`), but the choice is yours — the app only needs it to be a value that
is not `frost_anchored` or `non_seasonal_indoor`. If a new basis is coined for the
`herbaceous_perennial` archetype, say so, because plant-app has a `calendar_basis` switch
that may need a matching arm.

## 2. What is missing, verified 2026-07-25

Across all 8 regions and every resolved zone cell:

| Field | Asparagus | Every other establishment crop |
|---|---|---|
| `plant_out` | **0 cells** | 15-39 cells |
| `harvest` (window string) | **0 cells** | 15-39 cells |
| `establishment_years` | **null** | authored (number or `[min,max]`) |
| `days_to_maturity` | `[]` | `[]` (normal for this class) |

Asparagus zone cells carry only: `calendar`, `notes`, `suitability`,
`suitability_note_*`, `resolution_method`, `sources`, `anchoring_urls`.

The full 25-crop comparison table is reproducible with the script in section 7.

## 3. Why each gap matters to the app

**`plant_out` — the important one.** The app has no way to tell a grower when to set
crowns. Every other perennial's guide renders a "Plant" bar and a "Plant" key-window
chip from this field; asparagus renders neither.

The app is shipping a stopgap: it derives a single plant-crowns month as the first
month where `calendar[i] !== 'cold_pause'` (zone 6 gives April), on the reasoning that
crowns go in as the ground becomes workable. **This is a rendering inference, not
sourced data**, and it is commented as such in the component. It generalizes without
per-crop tuning, but it is not T1-backed and it cannot express a window, only a month.
Authoring `plant_out` retires the inference for asparagus.

**`establishment_years` — a silent default.** `~/plant-app/src/lib/herb/perennial-context.ts`
gates Herb's extra establishment coaching block on this field, defaulting to **2** when
unauthored. Asparagus is the only crop of the 25 hitting that default. It lands close to
correct by luck, not by data, and it is the crop where establishment coaching matters
most (the entire failure mode is "plants it, expects spears").

**`harvest` window string — cosmetic but visible.** The app derives harvest MONTHS from
`calendar[]`, so the ribbon is correct. But the "Harvest" key-window chip reads from the
window string, so an established asparagus bed shows no harvest chip while every other
perennial does.

## 4. The one rule that must not be broken

There are two adjacent fields and they are **not synonyms**:

- `establishment_years` (29 crops) — about plant DEVELOPMENT. Drives Herb's coaching.
- `years_to_first_harvest` (25 crops) — about FOOD. Drives every harvest claim in the app.

They legitimately disagree on several crops today: elderberry `est=[1,2]` vs
`ytfh=[2,3]`; fig `est=2` vs `ytfh=[1,2]`; persimmon `est=4` vs `ytfh=[3,5]`;
cherry-sweet `est=4` vs `ytfh=[3,5]`.

**Do not merge, rename, or "reconcile" them.** The app reads them for different purposes
and a reviewer already had to catch this once. Authoring asparagus's
`establishment_years` means adding the development number, not copying `[2,3]` across
from `years_to_first_harvest`.

## 5. What the app now consumes (context for authoring)

Shipped 2026-07-25, so authoring choices have immediate downstream effect:

`years_to_first_harvest` as `[low, high]` drives a three-state model on 25 crops:

| State | Rule | asparagus `[2,3]` | pawpaw `[4,7]` |
|---|---|---|---|
| establishing | `year < low` | year 1 | years 1-3 |
| first harvests | `low <= year < high` | year 2 | years 4-6 |
| full harvest | `year >= high` | year 3+ | year 7+ |

Bed year comes from the user's own `plantedAt`. In the establishing state the app
suppresses every harvest claim and substitutes "First harvest next year" / "in about N
years", derived from `low`.

## 6. Requested work

0. **Fix `calendar_basis`** (section 1b) — highest priority, blocks the app feature entirely.
1. **Author `plant_out` on asparagus zone cells**, all 8 regions, frost-anchored like the
   other perennials. Crowns, dormant, early spring as soil becomes workable. Extension
   sources already cited on this crop (`umn_ext`, `msu_ext`, `clemson_hgic`,
   `mu_ext`) cover crown planting timing.
2. **Author `establishment_years` for asparagus** as a development figure in its own
   right. Do not copy `years_to_first_harvest`.
3. **Author the `harvest` window string** on asparagus cells, consistent with the
   existing `calendar[]` harvest months (zone 6 = Apr-May).
4. **Confirm `days_to_maturity: []` is intentional** for this class rather than an
   omission. Every establishment crop shows `[]`, so this is likely correct by
   convention; a one-line confirmation closes it.

## 7. Open question worth a ruling

The plant-astro spec's section 9 parked this and the app inherited it:
`years_to_first_harvest` is a range, but the range currently means "somewhere in here",
not "year 2 in mild zones, year 3 in cold ones". If first harvest genuinely varies by
region, that is a **per-region field** and a larger arc. The app's three-state model
would consume it without redesign. A ruling either way (range is global / range is
per-region) unblocks the question permanently.

## 8. Reproduce the audit

```bash
cd ~/plant-dataset && python3 -c "
import json
d=json.load(open('crops_data_final.json'))
crops=d['crops'] if isinstance(d,dict) and 'crops' in d else d
if isinstance(crops,dict): crops=list(crops.values())
targets=[c for c in crops if c.get('years_to_first_harvest')]
print('%-22s %-10s %-8s %-9s %s' % ('slug','ytfh','est_yrs','plant_out','harvest'))
for c in sorted(targets,key=lambda x:x['slug']):
    po=hv=0
    for r in (c.get('regions') or {}).values():
        for z in (r.get('resolved_by_zone') or {}).values():
            if isinstance(z,dict):
                if z.get('plant_out'): po+=1
                if z.get('harvest'): hv+=1
    print('%-22s %-10s %-8s %-9s %s' % (c['slug'], json.dumps(c['years_to_first_harvest']),
                                        json.dumps(c.get('establishment_years')), po, hv))
"
```

Expected after this work: asparagus's `plant_out`, `harvest`, and `establishment_years`
columns all non-empty, matching the shape of the other 24.

## 9. Acceptance

- Asparagus zone cells carry `plant_out` and `harvest` in every region where the crop is
  `perennializes`, with anchoring URLs, matching the certification bar used for the rest
  of the crop.
- `establishment_years` authored, and demonstrably NOT a copy of
  `years_to_first_harvest`.
- The audit in section 8 shows asparagus in line with the other 24.
- plant-app then drops its derived plant-month inference for asparagus. That is a
  follow-up on the app side, not a blocker here; the app degrades correctly either way.
