# Tier-2 belt ruling: mid-South z8 (roadmap item 5, Task 2)

Design spec: `docs/superpowers/specs/2026-07-15-region-tier2-ruling-pass-design.md`.
Method: build a naive, region-blind `frost_anchored` calendar for a representative annual from
its own generic biology fields anchored to the belt's real frost dates, run it through
`tools/annual_calendar.py`, and compare against real T1 regional guidance for a 3-crop basket
(annual / chill-gated tree fruit / berry). No canonical write of any kind; `source_catalog` is
not touched (it lives inside `crops_data_final.json`).

## Marquee anchor: Little Rock, AR (Pulaski County)

AR carries the most belt ZIPs (460 z8) of the mid-South belt (AR/OK/TN/MO), so AR is the
marquee state; Little Rock is the marquee city (state capital, the NWS forecast-office anchor
station for the state). The belt's TN z9 sliver (1 ZIP) is negligible at this scale; it rides
this belt's general verdict, not its own pass (the same closure Task 3 gave Nevada's z10
sliver, per the design spec's own open item).

**Real frost-date normals (NWS Little Rock forecast office, 1991-2020 climate normals, 36°F
threshold, 50% probability):**
- Average last spring frost: **April 3**
- Average first fall frost: **October 31**

Source: NWS Little Rock, "Frost and Freeze Information for Arkansas,"
https://www.weather.gov/lzk/frostfreeze.htm (T1, `.gov`, National Weather Service).

**No T1 source for AR/OK/TN/MO was previously catalogued in this dataset** (confirmed during
the design spec's `source_catalog` inspection). All sources below were newly found for this
task; none are registered to `source_catalog` (per the design spec, that only happens if/when
this belt is later built as a real region).

## Basket crop 1: cherry-tomato (frost_anchored annual)

**Canonical generic fields** (read-only query):
`weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor: from_transplant, frost_tolerance_f: 32`
-- same values as the mid-Atlantic pass (crop-level fields, not belt-specific).

**Naive calendar** (built in the session scratchpad, `last_frost = Apr 3`, run through
`derive_annual_calendar(cell, calendar_basis="frost_anchored")`):

| Field | Naive value |
|---|---|
| `start_indoors` | Feb 27 - Mar 6 |
| `plant_out` | Apr 10 - Apr 24 |
| `harvest` | Jun 11 - Jul 9 |
| derived `calendar[]` | `cold_pause`, `indoors` x2, `plant`, `growing`, `harvest` x2, then `cold_pause` **Aug through Dec** (5 straight months) |

**Real T1 guidance, two independent University of Arkansas Cooperative Extension (UAEX) pages:**

1. **UAEX, "Planting Dates for Fall Vegetable Production"** (`FSA6001`-adjacent page) --
   verbatim tomato row: `"Tomatoes (plants)* 75 - 80 [days] July 1 - July 15"`, with the note
   "To produce tomato ... plants for fall crops, sow seed about four weeks earlier than the
   dates suggest for plant setting." This is an explicit, separate **fall transplant window**
   (July 1-15) distinct from spring, with a stated 75-80 day maturity -- i.e. real fall harvest
   landing mid-September through early October, well ahead of the real Oct 31 first frost.
2. **UAEX, "How to Grow Tomatoes in Arkansas"** -- independently confirms the same practice:
   *"Late plantings may be made in early July for fall harvest and storage. These plants have
   the advantage of increased vigor and freedom from early diseases."*
3. (Spring cross-check) **UAEX, "Arkansas spring and summer vegetable planting dates"** gives a
   broad `"March - May"` transplant window for tomatoes (Zone C, "adjust planting date for
   climate zone within Arkansas"), consistent with the naive deriver's Apr 10-24 spring start.

**Naive vs. real:** the naive spring start (Apr 10-24) sits comfortably inside the real
March-May spring window -- directionally correct. But the naive single-cycle deriver closes the
season at the end of the first harvest (Jun 11-Jul 9) and shows flat `cold_pause` for Aug-Dec.
Two independent UAEX sources instead document an explicit second (fall) transplant cycle
starting July 1-15, with real fruit landing in September/October -- the same gap class already
found for the mid-Atlantic belt (Task 1) and the same shape this dataset already models
elsewhere via `heat_pause` + fall reflush for other hot z8/z9 belts. **The naive calendar is not
wrong about suitability or the spring start, but it materially under-represents the season.**

## Basket crop 2: apple (chill-gated tree fruit)

Apple is not annual-deriver-driven (`weeks_indoors: None, days_to_maturity_mid: None,
dtm_anchor: None, frost_tolerance_f: 28` -- season-only/chill-gated, matches the mid-Atlantic
pass).

**Canonical `chill_hours_required` per recommended variety:** Dorsett Golden 100, Anna 200, Ein
Shemer 100, Zestar! 800, McIntosh 900, Liberty 800, Empire 700, Honeycrisp 800, Gala 600, Golden
Delicious 700, Jonagold 700, Mutsu 600, Fuji 600, Granny Smith 600, Pink Lady 550, Dolgo 500.
Range: 100-900, ceiling variety McIntosh at 900.

**Real chill-hour guidance:** UAEX, "Chilling Hour Reports" (AR Fruit, Vegetable & Nut Update
blog), average accumulated chilling hours **by March 1** (1990-2000 historical baseline) at four
AR research/reporting stations:
- U of A Campus, Fayetteville: **1,024**
- Fruit Research Station, Clarksville: **1,081**
- Southwest Research Station, Hope: **901**
- Wynne, AR: **1,069**

Source: https://www.uaex.uada.edu/farm-ranch/crops-commercial-horticulture/horticulture/ar-fruit-veg-nut-update-blog/posts/chillhours.aspx
(T1, `.edu`, UAEX Division of Agriculture).

**Comparison:** three of the four stations (Fayetteville, Clarksville, Wynne) clear the
canonical ceiling variety (McIntosh, 900) with wide margin (1,024-1,081). The fourth, Hope --
the state's southwestern low-desert-adjacent station and the closest analog to the belt's
warmest z8 edge -- comes in at 901, which technically clears McIntosh's 900-hour floor but by
essentially no margin (1 hour). No station's figure would actually flip any recommended
variety's classification (all clear `fruits_reliably` territory even at the tightest station),
so **missing chill data is moot for apple's classification outcome here**, same conclusion as
mid-Atlantic -- but the margin is genuinely tighter at the belt's warm edge than mid-Atlantic's
blanket ">1,000 hrs statewide" figure. Flagged as a caveat, not a divergence: worth a
station-specific (not single-figure) chill treatment if this belt is ever authored as a real
region, since AR's own reporting already shows real intra-state spread (901-1,081) that a single
belt-wide number would flatten.

## Basket crop 3: blackberry (berry, UA's own breeding program)

Blackberry is also not annual-deriver-driven (perennial). Canonical crop-level:
`chill_hours_required: 400, chill_hours_range: [200, 900], frost_tolerance_f: 15,
hardiness_zone_min/max: 5/9`. Canonical recommended varieties include several literal
University of Arkansas releases: Ouachita (300 hr), Navaho (800 hr), Apache (800 hr), Kiowa
(200 hr), Arapaho (400 hr) -- plus Osage, Triple Crown, Chester, Illini Hardy, Marionberry,
Boysenberry, and the UA primocane trio Prime-Ark Freedom/Traveler/45 (300 hr each).

**Real T1 guidance:** UAEX FSA6105, "Blackberry Production in the Home Garden" (M. Elena Garcia,
Extension Fruit and Nut Specialist, University of Arkansas Division of Agriculture, Fayetteville),
https://www.uaex.uada.edu/publications/PDF/FSA-6105.pdf -- fetched and read in full (PDF).
Load-bearing quotes:
- *"Blackberries are adapted to all regions of Arkansas. They are a good addition to the home
  fruit garden... Varieties developed by the University of Arkansas fruit breeding program are
  recommended for use in the state."*
- *"They are grown in a hedgerow-type system with the first crop being harvested the year after
  the planting is established."* Planting timing: *"Plant blackberry roots or rooted plants
  anytime in the spring before the soil warms."*
- Table 1 chill-hour figures for UA-released cultivars: Chickasaw ~500 hr, **Apache 800-900 hr**,
  **Kiowa 200-300 hr**, **Navaho 800-900 hr**, **Ouachita 400-500 hr**, Prime-Jim/Prime-Jan
  300-400 hr.

**Comparison:** the canonical dataset's blackberry variety roster and chill figures line up
directly with UA's own published numbers for its own cultivars -- Navaho (800 canonical / 800-900
real) and Apache (800 canonical / 800-900 real) match exactly at the low end of the real range;
Kiowa (200 canonical / 200-300 real) and Ouachita (300 canonical / 400-500 real) are directionally
consistent, canonical sitting at or just under the real range's floor (conservative, not
misleading). All of these clear the real belt-wide chill accumulation (901-1,081 hrs) many times
over -- chill is a complete non-factor for blackberry across the whole belt. This is the strongest
match in the basket: Arkansas literally bred these named cultivars for Arkansas conditions, and
the dataset already carries most of them by name. **No divergence signal.**

## Ruling: CONDITIONAL-GO

**Tree fruit (apple) and berry (blackberry) are honestly served by the generic, region-less
fallback.** Blackberry is an especially strong match -- the crop's own home-state breeding
program's published chill-hour figures for its named cultivars line up with the canonical
values, and the belt's real chill accumulation (901-1,081 hrs) clears the entire canonical
range with room to spare everywhere in the state. Apple's classification outcome is also
unaffected (no variety flips class), though the belt's real chill margin is noticeably tighter
at its southwestern warm edge (Hope, 901 hrs) than mid-Atlantic's statewide ">1,000 hrs" -- a
caveat worth carrying forward, not a divergence.

**The annual/warm-season class (cherry-tomato) has the same specific, real, T1-documented gap
found in mid-Atlantic (Task 1):** the naive frost-anchored single-cycle calendar is directionally
right about the spring start (naive Apr 10-24 sits inside UAEX's real March-May window) but omits
an entire second (fall) planting cycle that two independent UAEX pages document for this exact
belt (July 1-15 transplant, 75-80 day maturity, landing well before the real Oct 31 frost). This
is conservative, not misleading -- it never tells a user the wrong thing, it just offers less of
the season than is real. It is the same class of gap this dataset already has a shape for
(`heat_pause` + fall reflush, already live on other hot z8/z9 belts), not a wholesale
climate-regime mismatch. That bar -- a full NEW-REGION spec/plan/build -- is not met here:
nothing found flips a suitability class, and 2 of 3 basket crops (including the belt's signature
crop, blackberry) show no divergence at all. **Ruling: CONDITIONAL-GO**, with the caveat recorded
for any future authoring pass on this belt: warm-season annuals (tomato and likely its
neighbors) would benefit from a `heat_pause` + fall-reflush addition, and any future chill
treatment should account for the belt's real intra-state chill gradient (Hope's tighter margin
vs. the rest of the state) rather than a single flat figure; tree fruit and berries otherwise
need no correction.

## Source table

| Institution | URL | What it backs |
|---|---|---|
| NWS Little Rock forecast office | https://www.weather.gov/lzk/frostfreeze.htm | Little Rock real last/first frost normals: Apr 3 / Oct 31 (1991-2020, 36°F, 50% probability) |
| University of Arkansas Cooperative Extension (UAEX), "Planting Dates for Fall Vegetable Production" | https://www.uaex.uada.edu/yard-garden/vegetables/fall-planting-dates.aspx | Explicit fall tomato transplant window (Jul 1-15, 75-80 DTM), distinct from spring |
| UAEX, "How to Grow Tomatoes in Arkansas" | https://www.uaex.uada.edu/yard-garden/vegetables/tomato-gardening.aspx | Independent confirmation of an early-July fall planting practice |
| UAEX, "Arkansas spring and summer vegetable planting dates" | https://www.uaex.uada.edu/yard-garden/vegetables/spring-summer-planting-dates.aspx | Spring tomato transplant window ("March - May", Zone C) |
| UAEX, "Chilling Hour Reports" (AR Fruit, Vegetable & Nut Update blog) | https://www.uaex.uada.edu/farm-ranch/crops-commercial-horticulture/horticulture/ar-fruit-veg-nut-update-blog/posts/chillhours.aspx | Real AR chill accumulation by station: Fayetteville 1,024 / Clarksville 1,081 / Hope 901 / Wynne 1,069 (avg by Mar 1) |
| UAEX FSA6105, "Blackberry Production in the Home Garden" (M. Elena Garcia) | https://www.uaex.uada.edu/publications/PDF/FSA-6105.pdf | UA-released cultivar chill-hour figures, statewide adaptation claim, spring planting / year-after harvest timing |

All sources above are `.edu`/`.gov` university extension or National Weather Service, T1 by this
dataset's standard. None were previously catalogued in `source_catalog` for this belt; per the
design spec, they are cited here by institution+URL only and are NOT registered to
`source_catalog` (that field lives inside `crops_data_final.json`, untouched by this arc; formal
registration happens only if/when this belt is later built as a real region). No
`crops_data_final.json` bytes were read-write touched.
