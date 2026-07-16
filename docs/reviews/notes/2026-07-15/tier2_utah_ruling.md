# Tier-2 belt ruling: Utah z8 (roadmap item 5, Task 4)

Design spec: `docs/superpowers/specs/2026-07-15-region-tier2-ruling-pass-design.md`.
Method: build a naive, region-blind `frost_anchored` calendar for a representative annual from
its own generic biology fields anchored to the belt's real frost dates, run it through
`tools/annual_calendar.py`, and compare against real T1 regional guidance for a 3-crop basket
(annual / chill-gated tree fruit / berry, per the brief: cherry-tomato / apple / raspberry). No
canonical write of any kind; `source_catalog` is not touched (it lives inside
`crops_data_final.json`).

**Scope note.** The brief and the design spec's own belt table (`docs/superpowers/specs/
2026-07-15-region-tier2-ruling-pass-design.md` section 3) both scope this belt as **Utah z8, 15
ZIPs** (not z8-9 -- the roadmap's summary prose below carried a stray "z8-9" from an earlier
pass; corrected in Step 7 below).

## Marquee anchor: St. George, Washington County (the "Dixie" belt)

Utah's 15 z8 ZIPs cluster in southwest Utah's low-elevation "Dixie" core: St. George, Washington,
Hurricane, Ivins, Santa Clara, La Verkin, Toquerville and neighboring towns (all in the
2,600-3,700 ft band). This is confirmed both by USU Extension's own Washington County elevation
table (below) and by independent 2023-USDA-map zone lookups placing St. George/Hurricane/Ivins/
Washington/Toquerville at 8b and Santa Clara/La Verkin/Gunlock/Dammeron Valley at 8a. Washington
County's higher-elevation towns (Central, Enterprise, New Harmony at 5,300+ ft; Pine Valley at
6,527 ft) are colder zones and fall **outside** this z8 belt -- a fact that turns out to matter
directly for the apple finding below.

**Real frost-date normals, St. George (USU Extension Washington County, "Elevations for
Washington County," 2020):**
https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf (fetched; the raw
PDF text did not machine-extract via WebFetch's own parser, so it was re-extracted locally with
`pypdf` from the binary WebFetch had already cached -- no network re-fetch needed). Verbatim table
row: `*St. George 2624 3/30 11/1` -- the asterisk is explained in the document's own footnote:
*"Date taken from actual records provided by the Utah Climate Center"* (unlike the county's other
rows, which are elevation-interpolated estimates). The document also states directly: *"The
frost-free season is approximately 210 days; however, it is often over 100 degrees in June, July,
and August!"*

- Average last spring frost (32°F): **March 30**
- Average first fall frost (32°F): **November 1**

**Cross-check (adjacent rows, precision check on the table read):** `Bloomington 2575 3/30 11/1`
(near-identical elevation, identical dates) and `Washington 2624 3/30 11/1` (same elevation as St.
George, same dates -- St. George and Washington City are adjacent valley-floor twin cities) both
confirm the reading is internally consistent, not a misread; `Santa Clara 2788 4/5 10/28` and
`Ivins 2959 4/5 10/28` (slightly higher elevation) show the expected direction (later spring /
earlier fall as elevation rises). **Independent cross-check:** USU Extension, "Suggested Vegetable
Planting Dates for Utah," https://extension.usu.edu/yardandgarden/research/suggested-vegetable-
planting-dates-for-utah, states directly: *"the average last spring frost in St. George occurring
on March 30"* -- an exact match from a second, independently-authored USU document.

**A minor, honestly-flagged discrepancy:** an older USU Washington County document, "Fall
Gardening in the St. George Area" (Rick Heflebower, Washington County Horticulture Agent, dated
2008), https://extension.usu.edu/washington/files/Fall_Vegetable.pdf (also re-extracted locally
with `pypdf`), states *"The average frost date for fall is October 23"* and *"a long growing
season of approximately 196 days"* -- both about a week/two weeks short of the 2020 document's
November 1 / 210-day figures. The 2020 document is newer and explicitly sourced to Utah Climate
Center actual records (marked with an asterisk specifically for St. George); it is used as the
primary figure here, with the 2008 figure noted as a secondary, directionally-consistent (same
season, same order of magnitude) but slightly more conservative USU-authored estimate.

## Basket crop 1: cherry-tomato (frost_anchored annual)

**Canonical generic fields** (read-only query):
`weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor: from_transplant, frost_tolerance_f: 32`
-- same crop-level values as Tasks 1-3 (not belt-specific).

**Naive calendar** (built in the session scratchpad, `last_frost = Mar 30`, run through
`derive_annual_calendar(cell, calendar_basis="frost_anchored")`):

| Field | Naive value |
|---|---|
| `start_indoors` | Feb 24 - Mar 2 |
| `plant_out` | Apr 6 - Apr 20 |
| `harvest` | Jun 7 - Jul 5 |
| derived `calendar[]` | `cold_pause`(Jan), `indoors`(Feb-Mar), `plant`(Apr), `growing`(May), `harvest`(Jun-Jul), then `cold_pause` **Aug through Dec** (5 straight months) |

**A methodological check (the brief's Nevada-edge-case warning):** Utah's real last frost (Mar
30) is late enough that January stays inactive under the naive construction (`start_indoors` does
not begin until late February), so the deriver's January-active exception that suppressed
`cold_pause` entirely for Nevada (last frost Feb 28) does **not** fire here -- Utah's naive
calendar shape mechanically matches mid-Atlantic/mid-South's flat winter `cold_pause`, not
Nevada's all-`growing` back half, even though Utah's real climate is arid high-desert like
Nevada's, not humid like mid-Atlantic/mid-South's. This was confirmed by actually running the
deriver (not assumed), per the brief's instruction.

**Real T1 guidance, three independent USU sources:**

1. **USU Extension, "Suggested Vegetable Planting Dates for Utah"** (Table 1, `extension.usu.edu/
   yardandgarden/research/suggested-vegetable-planting-dates-for-utah`) -- tomato is Group D
   ("Very Tender"); St. George's recommended planting date is **April 1**, just 2 days after the
   station's own last-frost figure (March 30) -- a much tighter margin than the naive model's
   `plant_out` window (Apr 6-20).
2. **USU Extension, "How to Grow Tomatoes in Your Garden"** (`extension.usu.edu/yardandgarden/
   research/tomatoes-in-the-garden`) -- states the heat mechanism directly: *"During unfavorable
   weather (night temperatures lower than 50°F, or day temperatures above 95°F), tomatoes do not
   set and flowers abort."* A related passage on row-cover management notes fruit abortion above
   90°F during early fruit set. **No fall or second-planting strategy is mentioned anywhere in
   this document.**
3. **USU Extension Washington County, "Fall Gardening in the St. George Area"** (Rick
   Heflebower, `extension.usu.edu/washington/files/Fall_Vegetable.pdf`) -- the county's own fall
   vegetable-gardening guidance is entirely about **cool-season** crops (broccoli, cabbage,
   cauliflower, lettuce, carrots, spinach, onions for storage, turnips, beets). Tomato is not
   mentioned once, positively or negatively.

**Naive vs. real:** directionally close at the *start* of the window -- the naive `plant_out`
(Apr 6-20) opens within a week of the real USU-recommended April 1 date, the same order of
closeness found in the first three belts. The naive back half (`cold_pause` Aug-Dec) is the real
gap, and it is wrong in two separate, real, sourced ways, similar in *kind* (though not identical
in *mechanism*) to Nevada's finding: (a) it never shows any heat-driven pause during the real
90-95°F+ blossom-abort period (June through at least August, per USU's own tomato guide), and (b)
it shows five straight months of frost/dormancy starting in August, when real frost does not
return until late October/early November and USU's own St. George-specific fall-gardening
guidance describes an *actively gardened* September cool-season window, not a dormant one --
just not for tomato. Like Nevada (and unlike mid-Atlantic/mid-South, which had a real fall tomato
reflush to add), USU's own St. George-specific guidance does **not** recommend a fall tomato
cycle at all -- so the fix implied by this gap is a heat-pause + accurate frost-return date, not a
second tomato planting window.

**Existing canonical cross-reference:** this crop already carries a `warm_arid` region (z8,
Las Cruces/Mesilla Valley NM, `nmsu_ext`) with a real last frost of ~March 19 and a
synthesis note that the spring crop "begins coming in from about mid-to-late May, well ahead of
the peak midsummer heat that suppresses fruit set" -- directionally the same story found
independently above for St. George, from a different T1 source, in an already-authored z8 desert
region.

## Basket crop 2: apple (chill-gated tree fruit)

Apple is not annual-deriver-driven (`weeks_indoors: None, days_to_maturity_mid: None,
dtm_anchor: None, frost_tolerance_f: 28` -- season-only/chill-gated, matches Tasks 1-3).

**Canonical `chill_hours_required` per recommended variety:** Dorsett Golden 100, Anna 200, Ein
Shemer 100, Zestar! 800, McIntosh 900, Liberty 800, Empire 700, Honeycrisp 800, Gala 600, Golden
Delicious 700, Jonagold 700, Mutsu 600, Fuji 600, Granny Smith 600, Pink Lady 550, Dolgo 500.

**Real guidance -- this belt's own county extension does not recommend apple for the z8 core
itself.** USU Extension Washington County, "Fruits"
(`extension.usu.edu/washington/gardening/fruits/`), verbatim:

> Lower elevations (St. George area): *"apricots, cherries, figs, grapes, peaches, persimmons,
> plums, and strawberries"* thrive, plus *"nuts such as almonds, pecans, and pistachios."*
>
> Higher elevations (Brookside, Central, Enterprise, New Harmony -- all 5,300+ ft, all **outside**
> this z8 belt): *"apples, pears, and berries such as raspberries and blackberries grow well."*

This is a real, direct, T1, county-extension-office statement that **apple is positioned as a
higher-elevation crop, explicitly not part of the low-elevation (St. George/Dixie, i.e. the
actual z8 belt) recommended list.** Several secondary (non-T1) gardening sources corroborate the
same directional story (low-chill fruit -- figs, pomegranates, apricots -- recommended for
St. George; "fruit trees that require a certain amount of chill hours such as apples and pears
won't do well in the southwest"), but none of them are T1 and none supply a hard chill-hour
number for St. George specifically; they are cited here only as corroborating direction, not as
load-bearing evidence, the same convention Task 3 used for its Almanac.com cross-check.

**A genuine research gap, honestly reported:** despite checking USU's "Apple Production and
Variety Recommendations for the Utah Home Garden," "How to Grow Peaches in Your Garden," the
Utah Climate Center's station network pages (including its Fruit Growth Network, FGNET, which
does operate a station in Washington County), and the Washington County apple variety page, **no
USU-published numeric chill-hour figure for St. George/Washington County was found.** The apple
variety-recommendation page does not mention chill hours at all; the peach page gives
variety-level chill requirements (500-1,050 hrs) but no regional figure; the climate-center tools
require interactive navigation this task could not drive. This gap is recorded, not papered over.

**The strongest available quantitative anchor is this dataset's own existing regions for the
same crop**, both already z8, both in comparable high-desert climates, bracketing the question:

| Region | Zone | Anchor city (elevation) | Source | `chill_hours` | Apple suitability |
|---|---|---|---|---|---|
| `low_desert_az` | 9 | Phoenix, AZ (~1,100 ft) | `uariz_ext` | [250, 400] | `marginal` -- only Anna/Dorsett Golden/Ein Shemer (100-200 hr) crop; "high-chill varieties never fruit here" |
| `warm_arid` | 8 | Las Cruces/Mesilla Valley, NM (~3,900 ft) | `nmsu_ext` | [400, 700] | `fruits_reliably` -- "elevation banks enough chill for mid chill varieties (Gala, Fuji, Golden Delicious) plus low chill types" |
| **Utah z8 belt (this task)** | 8 | St. George, UT (**2,624 ft**, per the frost-table station) | -- | **not sourced; no region exists** | **unresolved -- sits between the two anchors on elevation** |

St. George's elevation (2,624 ft) sits meaningfully below `warm_arid`'s Las Cruces anchor (~3,900
ft) but well above `low_desert_az`'s Phoenix anchor (~1,100 ft) -- and this dataset's own
`chill_basis_seasoned` text for `warm_arid` explicitly ties its higher chill accumulation to
elevation ("more than the low deserts because of elevation"), the same elevation-chill logic
Washington County's own Extension office is using when it recommends apple only at the county's
higher-elevation towns. Taken together, this is real, converging (though not numerically
conclusive) evidence that St. George's real chill accumulation likely sits closer to the
`marginal` (250-400 hr) end of that bracket than the `fruits_reliably` (400-700 hr) end -- i.e.
**closer to Phoenix than to Las Cruces** -- which would mean only the lowest-chill third of the
canonical variety list (Dorsett Golden 100, Anna 200, Ein Shemer 100) crops reliably, the same
narrow set that succeeds in `low_desert_az`, not the broader mid-chill list (Gala/Fuji/Golden
Delicious/Mutsu/Granny Smith, 600-700 hr) that succeeds in `warm_arid`.

## Basket crop 3: raspberry (berry, in place of a blueberry/cane-fruit slot)

Raspberry is also not annual-deriver-driven (perennial, `berries_woody` calendar basis).
Canonical: `chill_hours_required: 800` (crop-level default), `chill_hours_range: [250, 1200]`,
`hardiness_zone_min/max: 3/11`. Per-variety chill spans Bababerry (250) and Dorman Red (300) up
through the bulk of the mainstream list at 800 (Boyne, Nova, Latham, Killarney, Jewel, Bristol,
Royalty, Heritage, Anne), with Caroline and Autumn Bliss at 600 and Tulameen at 700.

**Real T1 guidance, USU Extension, "Raspberry Management for Utah"**
(`extension.usu.edu/yardandgarden/research/raspberry-management-for-utah`) -- names the marquee
zone directly: *"Along the Wasatch Front and in Utah's Dixie, fall-bearing raspberries tend to be
better adapted, as the fruit ripens after the hottest part of the summer is over, thus avoiding
fruit sunburn."* "Utah's Dixie" is the same colloquial name for the St. George/Washington County
belt used throughout USU's own Washington County publications above -- this is a direct, positive,
belt-specific identity statement for raspberry, matching the brief's framing.

**A genuine tension, reported both ways rather than resolved in favor of the more convenient
reading:** the same county's own "Fruits" page (quoted above, apple section) lists raspberries and
blackberries in the **higher-elevation** column, not the St. George/low-elevation column -- i.e.
the general county fruit-zone guide and the crop-specific raspberry management guide (same
institution, different documents) do not fully agree on whether raspberry is a St.-George-core
crop or a higher-elevation one. The crop-specific document is more detailed and directly names the
belt ("Utah's Dixie"), so it is weighted higher here, but the disagreement is real and worth
recording rather than silently picking a side.

**This dataset's own existing `warm_arid` region for raspberry (z8, sourced `usu_ext` -- the
SAME USU raspberry-management page cited above) already encodes exactly this elevation/heat
tension**, independently of this task's research:

> `region_notes_seasoned`: *"The warm arid interior is variable: higher elevations with real
> chill grow raspberries well, while hot, low, alkaline-soil sites are marginal and need
> heat-tolerant, low-chill everbearing types."*

St. George (2,624 ft, hot, and -- per the USU Washington County soil/gardening context -- alkaline
desert soil) is exactly the "hot, low, alkaline-soil" case this existing canonical text describes
as `marginal`, needing a heat-tolerant, low-chill everbearing type -- which is precisely what the
fall-bearing recommendation above is pointing at (Bababerry 250 hr and Dorman Red 300 hr, and
likely Caroline/Autumn Bliss/Heritage/Anne, which are classic fall-bearing/primocane cultivars,
though the canonical schema does not yet carry a populated `bearing_habit` field for raspberry to
confirm this directly -- raspberry has not yet been migrated onto the new `berry` archetype
schema the 2026-07-15 strawberry pilot introduced).

**Comparison:** raspberry is a real, genuine, USU-documented crop identity for this exact belt
("Utah's Dixie" by name) -- not a suitability concern -- but, like apple, it is a **marginal, not
a clean, positive match**: the crop-specific guidance and this dataset's own existing `warm_arid`
raspberry text both describe low, hot, arid sites (which is what St. George is) as needing
specifically heat-tolerant, low-chill, fall-bearing cultivars, not the canonical list's dominant
high-chill (800 hr) mainstream cultivars. This is directly analogous in shape to Nevada's apple
finding and to mid-South's chill-gradient note: real, sourced, cultivar-tier differentiation
needed, not a suitability-class flip.

## Ruling: CONDITIONAL-GO

**Cherry-tomato** is directionally fine, the same shape (though not identical mechanism) as all
three prior belts: the naive spring start is close to real USU guidance, and the one real gap
(a flat winter `cold_pause` that both hides the real summer heat-driven fruit-abort period and
mischaracterizes September/October as dormant when real frost does not return until very late
October/November and cool-season fall gardening is genuinely underway) is a real, sourced,
"conservative/mischaracterized" gap of the kind this dataset already has shapes for
(`heat_pause` + an accurate frost-return date), not a suitability flip -- USU's own St. George
fall-gardening guidance does not recommend a fall tomato cycle, matching Nevada's finding, not
mid-Atlantic/mid-South's.

**Raspberry** is a genuine, real, USU-documented crop identity for this exact belt ("Utah's
Dixie" named directly), but a marginal one: real guidance (both the USU raspberry-management page
and this dataset's own pre-existing `warm_arid` raspberry region text, independently converging)
says the belt's low, hot, alkaline sites need heat-tolerant, low-chill, fall-bearing cultivars,
not the canonical list's dominant 800-hr mainstream cultivars. No suitability-class concern, but a
real cultivar-tier caveat.

**Apple is the sharpest finding of this belt, and arguably the sharpest class-level (not just
variety-tier) caveat found across this arc's four belts so far.** The belt's own county
Extension office does not include apple in its low-elevation (St. George/Dixie, i.e. the actual
z8 core) recommended-fruit list, listing it only for the county's higher-elevation towns, which
sit in a colder zone outside this z8 belt entirely. This dataset's own existing z8/z9 desert
apple regions (`warm_arid` NM, `fruits_reliably` at 400-700 chill hr / ~3,900 ft elevation;
`low_desert_az` AZ, `marginal` at 250-400 chill hr / ~1,100 ft elevation) bracket St. George's own
elevation (2,624 ft) closer to the `marginal` end than the `fruits_reliably` end. This is real
and sourced, but it stops short of the design spec's NEW-REGION bar: no source states apple
fails to fruit in St. George outright (only that it is not the elevation's recommended choice),
and no hard local chill-hour figure was found despite a genuine, multi-source search effort
(recorded as an open gap, not glossed over). Absent that missing number, this reads as a real
`marginal`-leaning signal, not a confirmed suitability-class flip -- the same evidentiary
distinction that kept Nevada's sharper-than-average apple caveat at CONDITIONAL-GO rather than
NEW-REGION.

None of the three basket crops shows a confirmed suitability-CLASS mismatch. Two of three
(cherry-tomato, raspberry) are directionally-fine-with-a-real-caveat, the established shape from
Tasks 1-3. Apple's caveat is real, sourced, and sharper than any prior belt's, but is bounded
between two already-existing regional archetypes in this very dataset rather than confirmed as a
hard failure. **Ruling: CONDITIONAL-GO**, with three caveats recorded for any future authoring
pass on this belt: (a) cherry-tomato and likely its warm-season neighbors need a real summer
heat-pause plus an accurate (not artificially early) frost-return date, not a fall reflush window
(USU does not recommend one); (b) raspberry needs cultivar-tier differentiation toward
heat-tolerant, low-chill, fall-bearing types, mirroring the caveat this dataset's own `warm_arid`
region text already carries for the same crop in a comparable climate; (c) apple's chill
suitability is genuinely uncertain at St. George's specific elevation and should not simply
inherit either neighboring desert region's verdict -- resolving it needs a real, St.-George-
specific numeric chill-hour figure that this task could not locate; until then, a future
authoring pass should treat apple as leaning `marginal`, not `fruits_reliably`, for the belt's
low-elevation core.

## Source table

| Institution | URL | What it backs |
|---|---|---|
| USU Extension Washington County, "Elevations for Washington County" (2020) | https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf | St. George real last/first frost normals: Mar 30 / Nov 1 (marked as Utah Climate Center actual-record data); "often over 100 degrees in June, July, and August" |
| USU Extension, "Suggested Vegetable Planting Dates for Utah" | https://extension.usu.edu/yardandgarden/research/suggested-vegetable-planting-dates-for-utah | Cross-check on St. George last frost (Mar 30); tomato (Group D) planting date Apr 1 |
| USU Extension, "How to Grow Tomatoes in Your Garden" | https://extension.usu.edu/yardandgarden/research/tomatoes-in-the-garden | Heat/blossom-drop thresholds (>95°F day / <50°F night abort; >90°F fruit-set abort under row cover); no fall/second planting mentioned |
| USU Extension Washington County, "Fall Gardening in the St. George Area" (Rick Heflebower, 2008) | https://extension.usu.edu/washington/files/Fall_Vegetable.pdf | Secondary/older frost-date cross-check (Oct 23 fall frost, 196-day season); confirms fall guidance is cool-season-only, no tomato |
| USU Extension Washington County, "Fruits" | https://extension.usu.edu/washington/gardening/fruits/ | Elevation-based fruit recommendation split: low elevation (apricot/cherry/fig/grape/peach/persimmon/plum/strawberry + nuts) vs. higher elevation (apple/pear/raspberry/blackberry) |
| USU Extension, "Raspberry Management for Utah" | https://extension.usu.edu/yardandgarden/research/raspberry-management-for-utah | Names "Utah's Dixie" directly as fall-bearing-raspberry-adapted territory (sunburn avoidance); already the source for this dataset's own `warm_arid` raspberry region text |
| (context only, not load-bearing) secondary chill-hour framing on St. George's low-chill fruit suitability, multiple non-T1 gardening sites | e.g. https://fruittreehub.com/what-fruit-trees-grow-in-st-george-utah/ | Directional corroboration only (same convention as Task 3's Almanac.com cross-check); not cited as a standalone claim |

All primary sources above are `.edu` Utah State University Extension (`usu_ext`, already
catalogued in `source_catalog`, covers the whole USU Extension family). Two PDFs
(`2020_Frost_dates_and_elevation.pdf`, `Fall_Vegetable.pdf`) did not machine-extract through
WebFetch's own summarizing parser; both were re-extracted locally with `pypdf` from the binary
copies WebFetch had already cached to disk (no re-fetch, no external tooling beyond what was
already installed), and both extracted cleanly as text (no image-render/visual read was needed
for this task -- there was no chart/table requiring a visual read the way Task 3's Nevada charts
did). This task's own comparison table (apple, above) also cites two ALREADY-CANONICAL region
entries (`warm_arid` and `low_desert_az` on apple and raspberry) as internal cross-references;
these are existing dataset content, not new sources, and are not re-cited to `source_catalog`.
No new `source_catalog` registration was made for the newly-found USU pages above (per the design
spec, they are cited here by institution+URL only; formal registration happens only if/when this
belt is later built as a real region). No `crops_data_final.json` bytes were read-write touched.
