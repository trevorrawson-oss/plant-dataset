# Tier-2 belt ruling: mid-Atlantic z8 (roadmap item 5, Task 1)

Design spec: `docs/superpowers/specs/2026-07-15-region-tier2-ruling-pass-design.md`.
Method: build a naive, region-blind `frost_anchored` calendar for a representative annual from
its own generic biology fields anchored to the belt's real frost dates, run it through
`tools/annual_calendar.py`, and compare against real T1 regional guidance for a 3-crop basket
(annual / chill-gated tree fruit / berry). No canonical write of any kind; `source_catalog` is
not touched (it lives inside `crops_data_final.json`).

## Marquee anchor: Raleigh, NC (Wake County)

NC carries the most belt ZIPs (793 z8 + 20 z9), so NC is the marquee state; Raleigh is the
marquee city (state capital, best-documented NC State Extension station).

**Real frost-date normals (Raleigh Ap / Wake County COOP station, 1944-2019, State Climate
Office of NC data):**
- Average last spring frost: **April 8**
- Average first fall frost: **October 30**

Source: NC State Extension, "Average First and Last Frost Dates,"
https://gardening.ces.ncsu.edu/weather-2-2/average-first-and-last-frost-dates/ (T1, `.edu`,
gardening.ces.ncsu.edu is the NC State Extension gardening portal; same institution as the
already-catalogued `ncsu_ext`).

These real dates replace the brief's placeholder (Apr 5) for the deriver run below.

## Basket crop 1: cherry-tomato (frost_anchored annual)

**Canonical generic fields** (read-only query):
`weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor: from_transplant, frost_tolerance_f: 32`
-- matches the brief's expected values exactly.

**Naive calendar** (built in the session scratchpad, `last_frost = Apr 8`, run through
`derive_annual_calendar(cell, calendar_basis="frost_anchored")`):

| Field | Naive value |
|---|---|
| `start_indoors` | Mar 4 - Mar 11 |
| `plant_out` | Apr 15 - Apr 29 |
| `harvest` | Jun 16 - Jul 14 |
| derived `calendar[]` | `cold_pause` x2, `indoors`, `plant`, `growing`, `harvest` x2, then `cold_pause` **Aug through Dec** (5 straight months) |

**Real T1 guidance, two independent already-catalogued sources:**

1. **Virginia Cooperative Extension Pub. 426-331** (`vce_426_331`) -- Table 4 (Zones 8a/8b),
   verbatim tomato row: `"Tomatoes3 | Zone 8a Spring: April 10-July 1 | Zone 8a Fall: July
   1-Aug 10 | Zone 8b Spring: April 1-July 1 | Zone 8b Fall: July 1-Aug 10"` (superscript 3 =
   "planting dates for transplants"). This table carries an explicit, separate **fall planting
   window** for tomatoes in z8, distinct from spring.
2. **NC State Extension**, "Central North Carolina Planting Calendar for Annual Vegetables,
   Fruits, and Herbs" (`ncsu_ext` family) -- the tomato row's transplant ("T") markers run
   continuously **April 1, 15; May 1, 15; June 1, 15; July 1** -- a single continuous
   succession-transplant window through early July, three months past the naive model's Apr
   15-29 window.

**Naive vs. real:** directionally correct at the *start* of the window (both real sources open
transplanting in the first half of April, matching the naive Apr 15 start within roughly a
week), but the naive single-cycle deriver closes the growing season at the end of the first
harvest (mid-July) and shows flat `cold_pause` for Aug-Dec. Both independent T1 sources instead
show active tomato transplanting/growing continuing into early-to-mid August (VCE's explicit
fall window; NC State's continuous succession window), which would put real fruit into
September/October, well before the real Oct 30 first frost. **The naive calendar is not wrong
about suitability or the spring start, but it materially under-represents the season** -- it
omits a real, documented second cycle that this dataset already models elsewhere for hot z8/z9
belts via `heat_pause` + fall reflush (se_gulf/low_desert_az donor rows per the roadoc's
"Heat-pause spot check").

## Basket crop 2: apple (chill-gated tree fruit)

Apple is not annual-deriver-driven (`weeks_indoors: None, days_to_maturity_mid: None,
dtm_anchor: None, frost_tolerance_f: 28` -- confirms season-only/chill-gated, per the brief).

**Canonical `chill_hours_required` per recommended variety:** Dorsett Golden 100, Anna 200, Ein
Shemer 100, Zestar! 800, McIntosh 900, Liberty 800, Empire 700, Honeycrisp 800, Gala 600, Golden
Delicious 700, Jonagold 700, Mutsu 600, Fuji 600, Granny Smith 600, Pink Lady 550, Dolgo 500.
Range: 100-900, with the bulk of mainstream varieties in the 550-900 band.

**Real chill-hour guidance:** NC State Extension Gardener Handbook, ch. 15 "Tree Fruit and
Nuts": *"Typically, throughout North Carolina, gardens receive in excess of 1,000 chilling hours
annually, so insufficient chilling rarely occurs"*; the extension recommends planting varieties
with a chilling requirement of "750 hours or greater" specifically to avoid *premature* bloom
during warm winter spells (too little chill, not too much, is NC's actual risk).
Source: https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts (T1,
`.edu`, NC State Extension).

**Comparison:** a real >1,000 chill-hour annual accumulation clears every variety in the
canonical recommended list (max 900, McIntosh) with room to spare -- none of them would be
misclassified as under-chilled. A bare z8 zone label does not carry chill data at all today (no
region = no `region_chill_delivered` entry), but z8 in this humid-continental-lite belt does not
carry the "warm zone label implies low chill" risk that flagged RGV/low-desert -- there is no
plausible naive read of "z8" that would predict a chill deficit here. **Missing chill data is
moot for apple in this belt**: the real figure is unambiguously `fruits_reliably` territory for
the whole recommended roster, and a bespoke region would not flip that story.

## Basket crop 3: blueberry (berry, genuine native range)

Blueberry is also not annual-deriver-driven (perennial). Canonical: `chill_hours_required: 1000`
(crop-level), `chill_hours_range: [150, 1000]`, `hardiness_zone_min/max: 3/11`. Per-variety
range spans Sharpblue (150 hr, southern highbush) to Patriot (1000 hr, northern highbush), with
Duke/Bluecrop/Jersey/Northblue/Northland at 800 and Premier at 550.

**Real T1 guidance, two NC State Extension sources:**
1. "Growing Blueberries in the Home Garden,"
   https://content.ces.ncsu.edu/growing-blueberries-in-the-home-garden -- gives region-specific
   variety recommendations: Coastal Plain highbush **Duke, Jersey**; Coastal Plain/Piedmont/
   Foothills rabbiteye **Premier** (among others), explicitly "the best choice for most soils
   below 2,500 ft elevation in NC" (i.e., essentially the whole belt).
2. Brunswick County Center (NC Cooperative Extension), "Vaccinium for the Coastal Plain:
   'Rabbiteye' and 'Southern Highbush'," https://brunswick.ces.ncsu.edu/news/vaccunium-for-the-
   coastal-plain-rabbiteye-and-southern-highbush/ -- rabbiteye needs 400-600 chill hours;
   Coastal Plain cultivars with 350-1,000 chill-hour requirements "do best."

**Comparison:** three of the canonical recommended varieties (Duke, Jersey, Premier) are
literally the same cultivars NC State names for this exact belt. Combined with the >1,000
chill-hour annual accumulation established above, the belt clears the entire canonical
`chill_hours_range` [150, 1000] for blueberry -- no variety is at risk of under-chilling, and
real guidance confirms mid-Atlantic z8 as genuine, well-documented native/adapted highbush and
rabbiteye range. No divergence signal.

## Ruling: CONDITIONAL-GO

**Tree fruit (apple) and berry (blueberry) are honestly served by the generic, region-less
fallback**: real chill data clears both crops' full canonical variety range with margin, and
real NC State variety guidance for the belt literally overlaps the canonical recommended list.
No suitability misclassification exists or would be fixed by building a bespoke region.

**The annual/warm-season class (cherry-tomato) has one specific, real, T1-documented gap**: the
naive frost-anchored single-cycle calendar is directionally right about spring start but omits
an entire second (fall) planting cycle that both VCE 426-331 and NC State's own planting
calendar document for this exact zone. This is conservative, not misleading -- it never tells a
user the wrong thing, it just offers less of the season than is real. It is the same class of
gap this dataset already has a shape for (`heat_pause` + fall reflush, already live on other hot
z8/z9 belts), not a wholesale climate-regime mismatch like RGV's frost-free flip or PNW's chill/
heat inversion across many classes. That bar -- a full NEW-REGION spec/plan/build -- is not met
here: nothing found flips a suitability class, and 2 of 3 basket crops show no divergence at
all. **Ruling: CONDITIONAL-GO**, with the caveat recorded for any future authoring pass on this
belt: warm-season annuals (tomato and likely its neighbors -- pepper, squash, bean) would
benefit from a `heat_pause` + fall-reflush addition; tree fruit and berries need no such
correction.

## Source table

| Institution | URL | What it backs |
|---|---|---|
| NC State Extension | https://gardening.ces.ncsu.edu/weather-2-2/average-first-and-last-frost-dates/ | Raleigh (Wake Co.) real last/first frost normals: Apr 8 / Oct 30 (1944-2019) |
| NC State Extension, "Central North Carolina Planting Calendar for Annual Vegetables, Fruits, and Herbs" | https://content.ces.ncsu.edu/central-north-carolina-planting-calendar-for-annual-vegetables-fruits-and-herbs | Tomato transplant window (continuous Apr 1 - Jul 1 succession), 75-85 DTM |
| Virginia Cooperative Extension Pub. 426-331 (`vce_426_331`, already catalogued) | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | Zone 8a/8b tomato spring (Apr 10/1 - Jul 1) + explicit fall (Jul 1 - Aug 10) planting windows |
| NC State Extension Gardener Handbook, ch. 15 "Tree Fruit and Nuts" | https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts | Statewide NC chill accumulation ">1,000 hrs/yr"; 750-hr minimum recommendation |
| NC State Extension, "Growing Blueberries in the Home Garden" | https://content.ces.ncsu.edu/growing-blueberries-in-the-home-garden | Regional blueberry variety recommendations (Duke, Jersey, Premier, etc.) by NC region |
| NC Cooperative Extension, Brunswick County Center, "Vaccinium for the Coastal Plain" | https://brunswick.ces.ncsu.edu/news/vaccunium-for-the-coastal-plain-rabbiteye-and-southern-highbush/ | Rabbiteye 400-600 chill-hr requirement; Coastal Plain 350-1,000 chill-hr cultivar range |

All sources above are `.edu` university/cooperative extension (NC State or Virginia Tech), T1 by
this dataset's standard; `ncsu_ext` and `vce_426_331` are already catalogued in
`source_catalog`. No `crops_data_final.json` bytes were read-write touched; `source_catalog`
itself was not written (per the design spec, new sources found here are cited by
institution+URL directly in this note, not registered until/unless this belt is later built as
a real region).
