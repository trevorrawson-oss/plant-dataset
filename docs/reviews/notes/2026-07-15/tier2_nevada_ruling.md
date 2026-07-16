# Tier-2 belt ruling: Nevada z8/z9/z10 (roadmap item 5, Task 3)

Design spec: `docs/superpowers/specs/2026-07-15-region-tier2-ruling-pass-design.md`.
Method: build a naive, region-blind `frost_anchored` calendar for a representative annual from
its own generic biology fields anchored to the belt's real frost dates, run it through
`tools/annual_calendar.py`, and compare against real T1 regional guidance for a 3-crop basket
(annual / chill-gated tree fruit / arid-friendly crop, here `garlic` per the brief in place of a
berry -- Nevada has no berry regionally distinct from the generic case). No canonical write of
any kind; `source_catalog` is not touched (it lives inside `crops_data_final.json`).

**A note on climate archetype.** Mid-Atlantic (Task 1) and mid-South (Task 2) are both humid,
warm-summer belts and both ruled CONDITIONAL-GO on the same narrow gap (a missing fall tomato
reflush). Nevada is a genuinely different archetype: high desert, not humid, with an extreme
diurnal swing and a real winter chill season. The evidence below does NOT reproduce the same
narrow gap-shape -- it surfaces three separate, real caveats, one per basket crop, some sharper
than anything found in the first two belts.

## Marquee anchor: Las Vegas / North Las Vegas, Clark County (z9)

NV's z9 ZIP count (94) dominates z8 (15) and z10 (1) -- unlike the other four belts in this arc,
which are each single-zone-dominant, Nevada's population and ZIP mass sit almost entirely in the
warm Las Vegas Valley z9 band (z9a suburbs: North Las Vegas, Centennial Hills, Spring Valley; z9b
urban core: the Strip/downtown). Reno and the rest of northern Nevada are z6b-7b (confirmed via
web search against the 2023 USDA map) and not represented at all in this belt's z8/z9/z10 ZIPs.
The state's single z10 ZIP is consistent with an extreme-low-elevation outlier (e.g. the Laughlin/
Colorado River corner); at 1 ZIP it rides this belt's general verdict, not its own pass (per the
design spec's open item 10).

**Real frost-date normals, Las Vegas (NWS Las Vegas forecast office, VEF):**
NOAA Technical Memorandum NWS WR-235, "Climate of Las Vegas, Nevada" (Paul H. Skrbac and Scott
Cordero, National Weather Service Office, Las Vegas, December 1995), fetched directly (PDF,
extracted with `pypdf`) -- verbatim quote: *"Based on the 1961-90 period of record, the average
first occurrence of 32 degrees in the fall is November 25; the average last occurence is
February 28."* Source:
https://www.weather.gov/media/wrh/online_publications/TMs/TM-235.pdf (T1, `.gov`, NWS technical
memorandum).

- Average last spring frost (32°F): **February 28**
- Average first fall frost (32°F): **November 25**

**Cross-check against more recent normals:** NOAA NCEI's 1991-2020 U.S. Climate Normals for Las
Vegas (as reported through the NWS/NCEI-sourced public frost-date aggregator at Almanac.com,
since the underlying NCEI table itself wasn't fetchable as raw text) put the 50/50-probability
last spring freeze at February 20 and the 50%-probability first fall 32°F frost around December
8 -- both directionally consistent with WR-235's older normals (if anything, an even shorter real
cold season in the more recent period). Either figure set makes the same point: Las Vegas's real
frost season is dramatically shorter than mid-Atlantic's (Apr 8 / Oct 30) or mid-South's (Apr 3 /
Oct 31) -- last frost arrives over a month earlier and first frost over three weeks later. This
is the first hard confirmation that Nevada is a different climate archetype, not a rerun.

## Basket crop 1: cherry-tomato (frost_anchored annual)

**Canonical generic fields** (read-only query):
`weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor: from_transplant, frost_tolerance_f: 32`
-- same crop-level values as Tasks 1-2 (not belt-specific).

**Naive calendar** (built in the session scratchpad, `last_frost = Feb 28`, run through
`derive_annual_calendar(cell, calendar_basis="frost_anchored")`):

| Field | Naive value |
|---|---|
| `start_indoors` | Jan 24 - Jan 31 |
| `plant_out` | Mar 7 - Mar 21 |
| `harvest` | May 8 - Jun 5 |
| derived `calendar[]` | `indoors, growing, plant, growing, harvest, harvest, growing, growing, growing, growing, growing, growing` (Jan indoors -> Jun harvest, then **6 straight months of `growing`, Jul-Dec, no `cold_pause` at all**) |

The all-`growing` back half is a real mechanism finding, not a copy-paste of Tasks 1-2's flat
`cold_pause`: because Nevada's real last frost is so early, January is itself an active
(`indoors`) month, and `derive_annual_calendar`'s own coherence rule only inserts `cold_pause`
when January is inactive (see `tools/annual_calendar.py` lines 96-108, "a January-active cell is
near-year-round -> NO cold_pause"). The naive construction's own logic, not a per-crop authored
bug, produces this.

**Real T1 guidance, three independent UNR/UNCE sources:**

1. **UNR Extension, "Growing Tomatoes in Southern Nevada"** (A. Roberts, 1999, SP-99-11),
   https://extension.unr.edu/publication.aspx?PubID=3267 -- states the region's own practical
   last-frost date directly: *"The last frost date for Southern Nevada is March 15"* (note: 2+
   weeks later than the raw NWS meteorological average of Feb 28 above -- the extension's own
   safety margin against a late cold snap). States the heat ceiling explicitly: *"Once
   temperatures climb above 90°F during the day and fall under 55°F at night, most varieties will
   not set fruit."* Seeds should be started "approximately six to eight weeks before" the last
   frost (mid-to-late January). Explicitly does **not** mention a fall or second planting season
   for Southern Nevada tomatoes; instead recommends mixing early (50-60 day) and main-season
   (80+ day) varieties in the same spring planting to spread the harvest before the heat cutoff.
2. **UNR/UNCE Fact Sheet-02-61, "Home Vegetable Production in Southern Nevada"** (Dr. Angela M.
   O'Callaghan, Area Extension Specialist), https://naes.agnt.unr.edu/PMS/Pubs/2002-3280.pdf
   (fetched and read in full, PDF) -- confirms: *"In Southern Nevada, [warm season vegetables]
   can be planted from March until May,"* and that these plants "do not grow well at temperatures
   above 90°F."
3. **UNLV-hosted "Vegetable Planting Guide for Southern Nevada"** (Clarita Huffman, Master
   Gardener; UNR Cooperative Extension Master Gardener program, Clark County),
   https://www.unlv.edu/sites/default/files/page_files/27/CampusLife_Planting-Calendar-LasVegas.pdf
   -- a checkbox planting chart (fetched as PDF, rendered to image and read visually since the
   embedded font would not extract as text). Tomato transplant window: **Mar (mid/late) through
   Jun (early/mid/late)** -- i.e. mid-March through the end of June, a long single-season
   succession window, with NO shaded cells in Jul/Aug (no transplanting recommended once summer
   heat sets in, and no fall reflush shown).

**Naive vs. real:** the naive spring start (indoors Jan 24-31, plant_out Mar 7-21) lines up
closely with UNR's own recommended dates (seed-start "6-8 weeks before Mar 15" = mid/late Jan;
transplant Mar 15) -- directionally correct, same as Tasks 1-2. But two real gaps, different in
shape from the humid belts':
- The naive's single 2-week `plant_out` window and May-Jun harvest close-out under-represents the
  real ~3.5-month spring succession window (mid-March through late June) all three UNR sources
  describe -- but unlike mid-Atlantic/mid-South, **there is no missing fall cycle to add**: UNR
  explicitly does not recommend one for tomato in Southern Nevada. The gap here is "spread the
  single spring window wider," not "add a second season."
- More seriously: the naive deriver's own `growing`-for-6-straight-months back half (Jul-Dec)
  actively contradicts BOTH real constraints UNR documents for this exact period -- the >90°F
  day / <55°F night fruit-set cutoff (Las Vegas routinely exceeds 100°F June-September) AND the
  real return of frost (Nov 25 average). A user reading `growing` through December would not
  learn that fruit set stops for roughly three summer months, nor that real frost returns before
  the year is out. This is a materially different, and arguably more actively misleading,
  failure mode than the flat `cold_pause` Aug-Dec seen in mid-Atlantic/mid-South (which was
  conservative -- wrong by omission -- rather than actively contradicted by a stated real-world
  threshold).

## Basket crop 2: apple (chill-gated tree fruit)

Apple is not annual-deriver-driven (`weeks_indoors: None, days_to_maturity_mid: None,
dtm_anchor: None, frost_tolerance_f: 28` -- season-only/chill-gated, matches Tasks 1-2).

**Canonical `chill_hours_required` per recommended variety:** Dorsett Golden 100, Anna 200, Ein
Shemer 100, Zestar! 800, McIntosh 900, Liberty 800, Empire 700, Honeycrisp 800, Gala 600, Golden
Delicious 700, Jonagold 700, Mutsu 600, Fuji 600, Granny Smith 600, Pink Lady 550, Dolgo 500.

**Real chill/performance guidance -- a direct field trial at the marquee city itself:** UNR
Extension, "University of Nevada, Reno Extension Research Orchard Fruit Evaluations &
Recommendations for Southern Nevada - 2020" (SP-20-07; M.L. Robinson, Angela O'Callaghan, and
Louise Ruskamp; peer-reviewed), https://naes.agnt.unr.edu/PMS/Pubs/2020-3713.pdf (fetched as PDF;
text layer was not machine-extractable so the relevant pages were rendered to images and read
directly). Trials ran 2005-2018 at the Extension Research Orchard, 4600 Horse Drive, **North Las
Vegas** -- literally inside the marquee z9 belt. The publication's own framing: *"Not all apples
do well in southern Nevada, and range from 'best apple ever tasted' to 'tasteless,' depending on
variety."* Its apple table, with per-variety chill hours:

| Variety | Rating | Chill hours (UNR trial) | Canonical `chill_hours_required` |
|---|---|---|---|
| Dorsett Golden | Top Choice | 100 | 100 (exact match) |
| Pink Lady (Cripps Pink) | Top Choice | 300-400 | 550 (canonical is HIGHER than the real trial figure) |
| Mutsu (Crispin) | Top Choice | 500 | 600 (canonical higher) |
| Anna | Notable Mention | 200 | 200 (exact match) |
| Fuji | Notable Mention | <500 | 600 (canonical higher) |
| Granny Smith | Notable Mention | 700 | 600 (canonical LOWER than the real trial figure) |
| Liberty | Under Review (inconclusive/insufficient data) | -- | 800 |

Zestar!, McIntosh, Empire, Honeycrisp, Golden Delicious, Jonagold, Gala (only mentioned as a
Mutsu pollinizer, not itself evaluated), Ein Shemer, and Dolgo do not appear in the trial at all
-- neither confirmed nor refuted by this source.

**Comparison:** apple's crop-level suitability is clearly `fruits_reliably` in real southern
Nevada -- this is the strongest possible confirmation (a direct, peer-reviewed, multi-year field
trial at the marquee city, not an inference from a same-climate-family cross-reference), and it
runs in the OPPOSITE direction a naive "hot low desert" assumption might suggest (i.e. it is not
a chill-starved climate the way Phoenix/`low_desert_az` is -- see below). The real ceiling of
CONFIRMED good performance is Granny Smith at 700 hours; Liberty (800) is explicitly unresolved,
and 6 of the canonical's 16 recommended varieties (Zestar! 800, McIntosh 900, Empire 700, Golden
Delicious 700, Jonagold 700, plus Gala at 600 unevaluated on its own) sit at or above that
confirmed ceiling with no real Nevada-specific evidence either way. This is a real, sourced gap
-- the sharpest variety-level caveat found in this arc so far (wider than mid-Atlantic's zero-gap
and mid-South's single-station margin note): roughly a third of the canonical "recommended" apple
list for this crop is unconfirmed against the belt's real chill ceiling. It does not, however,
rise to a suitability-CLASS mismatch -- apple unambiguously fruits in southern Nevada, and 9 of
16 varieties (including literally the "Top Choice" tier) are directly validated or fall
comfortably under the confirmed range.

**A useful negative cross-reference:** this dataset's `low_desert_az` region (Phoenix, real chill
`[100,400]` hours per `region_chill_delivered`, per UA Extension az1269) rules apple crop-level
`marginal`, with only its 3 lowest-chill varieties (Anna, Dorsett Golden, Ein Shemer) actually
cropping and an authored note that "high-chill varieties never fruit here." Nevada's real UNR
field-trial evidence shows meaningfully MORE chill than that -- Granny Smith (700h) and Mutsu
(500-600h) succeed here where they would not in Phoenix -- confirming Las Vegas (~2,000 ft
elevation, colder winter nights than the Phoenix valley floor at ~1,100 ft) is genuinely a
different, cooler desert climate than `low_desert_az`, not a rerun of it. The brief flagged this
region as a "useful cross-reference even though it doesn't cover NV's states" -- it is useful
precisely as a contrast, not a match.

## Basket crop 3: garlic (arid-friendly, fall-planted, in place of a berry)

Canonical: `weeks_indoors: None, days_to_maturity_mid: 240, dtm_anchor: from_planting,
frost_tolerance_f: 10, lifecycle: perennial: false` (annual, grown from clove, direct-sown). The
crop's own `start_method` notes state garlic "is planted directly in the ground from cloves in
fall, not raised as transplants" -- garlic is fall-planted and vernalization-driven, categorically
different in shape from cherry-tomato's spring/last-frost anchoring.

**Real T1 guidance, marquee city:** the same UNLV-hosted "Vegetable Planting Guide for Southern
Nevada" (Clarita Huffman, Master Gardener; UNR Cooperative Extension) used above. The garlic row
(read from the rendered chart image, cross-checked against the header column labels) shows
shading **only** at Sept (early/mid/late) through Oct (early) -- i.e. a real fall clove-planting
window of roughly **September through mid-October**, with no planting shown Feb-Apr or Aug or
Nov. This is a genuine, real, direct confirmation that Nevada's arid high-desert climate is
garlic-friendly, per the brief's framing.

**Cross-reference already in the canonical** (per the brief's suggestion): garlic's existing
`regions.warm_arid` (interior high desert, NM/west TX, z8) plants "late September to November"
(`from: first_frost, offset_days: -14, window_days: 45`, sourced `usu_ext`/`tamu_agrilife`), and
`regions.low_desert_az` (Phoenix, z9-10) plants "mid-September through November" (sourced
`uariz_ext_az1005`). Nevada's own real window (Sept - mid-Oct) is consistent in SHAPE with both
(fall clove-set, harvest the following early summer) but real and noticeably NARROWER --
closing 3-6 weeks earlier than either cross-reference region's window. This is a minor, real
content nuance (not a suitability concern): all three arid/high-desert regions agree garlic is
fall-planted and thrives, but Nevada's own real guidance would not be well served by simply
inheriting either neighbor's exact window verbatim if this belt is ever authored.

**An illustrative aside on the naive-construction method itself:** the design spec's naive
baseline (Step 3's helper script) is built to anchor a crop's own generic fields to the belt's
`last_frost` -- a construction that is honest for a genuinely spring-anchored annual like
cherry-tomato, but was never exercised against a fall/vernalization crop in Tasks 1-2. Applying
the identical mechanical construction to garlic's own generic fields (`dtm_mid=240`,
`last_frost=Feb 28`, no indoor start) produces `plant_out "Mar 7 - Mar 21"`,
`harvest "Nov 2 - Nov 30"` -- a **spring-planted, fall-harvested** shape, which is the exact
inverse of garlic's real biology (fall-planted, harvested the following summer). This is not a
live dataset defect (no such cell exists for a no-region crop; it is nowhere rendered to a real
user), but it is a genuinely different, more severe class of naive-model failure than anything
found in Tasks 1-2, whose basket crops were all legitimately spring-anchored annuals with only an
incomplete (not inverted) naive picture. It is recorded here as a finding about the METHOD's own
limits on a fall-planted crop, not as a belt-suitability concern -- garlic's real T1 sourcing
above is unambiguously positive.

## Ruling: CONDITIONAL-GO (broader than Tasks 1-2, no suitability-class flip)

Nevada does not reproduce mid-Atlantic/mid-South's narrow "add a fall tomato window" shape. It
surfaces three separate, real, sourced findings, one per basket crop:

1. **cherry-tomato:** the real spring start lines up well with UNR's own recommended dates, but
   the naive single-cycle deriver both under-represents the real ~3.5-month spring succession
   window AND -- more importantly -- produces a `growing`-for-6-months back half that actively
   contradicts UNR's own stated summer heat/fruit-set cutoff (>90°F day / <55°F night) and the
   real Nov 25 frost return, rather than merely omitting a fall cycle that doesn't exist here
   anyway (UNR explicitly does not recommend one).
2. **apple:** crop-level suitability is confirmed `fruits_reliably` by a direct, peer-reviewed,
   multi-year field trial at the marquee city -- the strongest possible evidence, and it runs
   counter to any "hot desert = chill-starved" assumption (a real contrast with `low_desert_az`).
   But a real third of the canonical recommended-variety list sits above the confirmed chill
   ceiling with no Nevada-specific evidence either way -- the sharpest variety-level caveat found
   across this arc's three belts so far.
3. **garlic:** real T1 sourcing directly confirms Nevada's arid climate is genuinely
   garlic-friendly (a real Sept-to-mid-Oct fall clove-planting window at the marquee city,
   consistent in shape with, though narrower than, the two existing cross-reference regions). No
   suitability concern -- but the same naive-construction method that worked adequately for
   cherry-tomato, if mechanically applied to garlic without crop-specific fall/vernalization
   knowledge, would invert the growing season entirely, a materially worse failure mode than
   anything the humid belts exposed in this arc.

None of the three basket crops shows a suitability-CLASS mismatch (`fruits_reliably` ->
`marginal`/`survives_no_fruit`, or an outright non-viable verdict) -- the bar the design spec sets
for NEW-REGION. Apple fruits reliably; garlic is confirmed well-suited; tomato is confirmed
growable across a real multi-month spring window. That keeps this belt on the CONDITIONAL-GO side
of the framework. But the caveats are real, sourced, and broader than Tasks 1-2's: this is not a
one-line footnote belt. **Ruling: CONDITIONAL-GO**, with three caveats recorded for any future
authoring pass on this belt: (a) cherry-tomato and its neighbors need a real summer heat-pause +
a widened spring succession window, not just a fall reflush the way the humid belts got; (b)
apple needs real chill-tier variety differentiation (the recommended list should not present its
high-chill quarter/third as equally confirmed as its Top Choice tier); (c) garlic's real window is
narrower than either arid cross-reference region and should not simply inherit one verbatim.

## Source table

| Institution | URL | What it backs |
|---|---|---|
| NWS Las Vegas (NOAA Technical Memorandum WR-235, "Climate of Las Vegas, Nevada," 1995) | https://www.weather.gov/media/wrh/online_publications/TMs/TM-235.pdf | Real last/first frost normals: Feb 28 / Nov 25 (32°F, 1961-90 period of record) |
| NOAA NCEI 1991-2020 U.S. Climate Normals (Las Vegas, via public frost-date aggregation) | https://www.almanac.com/gardening/frostdates/NV/Las%20Vegas | Cross-check: 50/50 last freeze ~Feb 20, 50% first fall 32°F ~Dec 8 (more recent normals, same directional story) |
| UNR Extension, "Growing Tomatoes in Southern Nevada" (A. Roberts, 1999, SP-99-11) | https://extension.unr.edu/publication.aspx?PubID=3267 | Southern NV's own recommended last-frost date (Mar 15); >90°F/<55°F fruit-set cutoff; no fall/second planting recommended; early+main variety mix strategy |
| UNR/UNCE Fact Sheet-02-61, "Home Vegetable Production in Southern Nevada" (Dr. Angela M. O'Callaghan) | https://naes.agnt.unr.edu/PMS/Pubs/2002-3280.pdf | Warm-season (tomato) planting window March-May; 90°F growth ceiling; cool-season Feb-Apr / mid-Aug-Oct |
| UNLV-hosted "Vegetable Planting Guide for Southern Nevada" (Clarita Huffman, Master Gardener; UNR Cooperative Extension) | https://www.unlv.edu/sites/default/files/page_files/27/CampusLife_Planting-Calendar-LasVegas.pdf | Tomato transplant window (mid-Mar - late Jun, no fall shading); garlic fall clove-planting window (Sept - mid-Oct) |
| UNR Extension, "Research Orchard Fruit Evaluations & Recommendations for Southern Nevada - 2020" (SP-20-07; Robinson, O'Callaghan, Ruskamp; peer-reviewed) | https://naes.agnt.unr.edu/PMS/Pubs/2020-3713.pdf | Direct field-trial apple variety performance + chill-hours at the marquee city (North Las Vegas Research Orchard) |

All primary sources above are `.edu`/`.gov` university extension or National Weather Service, T1
by this dataset's standard (`unr_ext`, already catalogued, covers the UNR Extension family; the
NWS/NOAA and UNLV-hosted Master Gardener sources are newly found for this task). The single
Almanac.com cross-check is a secondary aggregator of NOAA NCEI data, used only as directional
corroboration alongside the primary NWS WR-235 citation, not as a standalone T1 source. None were
previously catalogued in `source_catalog` for this belt (beyond `unr_ext` itself); per the design
spec, they are cited here by institution+URL only and are NOT registered to `source_catalog`
(that field lives inside `crops_data_final.json`, untouched by this arc; formal registration
happens only if/when this belt is later built as a real region). No `crops_data_final.json` bytes
were read-write touched.
