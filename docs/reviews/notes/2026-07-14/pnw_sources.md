# Maritime PNW region -- T1 sourcing table (Task 3)

Verified 2026-07-14. All sources below are `.edu` (university extension) or `.gov` (NOAA/NWS).
No seed-catalog or blog sources are used for load-bearing windows. PDFs were fetched and their
full text extracted directly (see "PDF-extraction notes" at the end); every quoted figure below
was read from the actual document, not inferred.

## Frost-date normals (every annual cell's `resolved_from` uses these)

| Zone | Archetype | last_frost | first_frost | freeze-free days | Station / source |
|---|---|---|---|---|---|
| **z8** | Puget Sound / Willamette Valley lowland (inland/valley) | **March 21** | **November 12** | 235 | Seattle-Tacoma Airport, 1945-1997 period of record. NOAA Technical Memorandum NWS WR-257, "Climate of Seattle, Washington" (Felton, 1998). |
| **z9** | milder coastal / protected pockets | **March 29** | **November 9** | 213 | Astoria, OR station. NOAA Technical Memorandum NWS-WR-250, "Climate of Astoria, Oregon" (4th revision, Rockey, Feb 2024), 1991-2020 normals. |

- z8 source: https://www.weather.gov/media/wrh/online_publications/TMs/TM-257.pdf (T1, .gov)
- z9 source: https://www.weather.gov/media/pqr/climate/ClimateBookAstoria/ASTclimatebook.pdf (T1, .gov)
- Corroboration: WSU EM057E ("Home Vegetable Gardening in Washington," Miles et al., 2013)
  Figure 1B/1C, a statewide map (adapted from Antonelli et al. 2004) with categorical last/first
  frost bands. Both the Puget lowlands (z8 archetype) and the immediate coast (z9 archetype) fall
  in the map's mildest bracket -- last frost "Before Apr 15," first frost "After Nov 1" -- which is
  consistent with, but coarser than, the precise NOAA station normals above.

**IMPORTANT caveat for Task 4 authors:** the brief's starting hypothesis was that z9 (milder
zone) would show a slightly earlier last frost / later first frost than z8 -- i.e., a more
generous window. **The verified station data does not support that.** Astoria's (z9)
freeze-free window (213 days) is actually *shorter* than Sea-Tac's (z8, 235 days), because USDA
hardiness zones are defined by **extreme minimum winter temperature**, not by frost frequency or
freeze-free day count. Marine moderation keeps z9's coldest nights from getting as cold as z8's,
but it does not stop z9 from seeing more, or later-persisting, light frosts in a typically cooler,
cloudier coastal spring. **Do not assume z9 cells get a more permissive frost-anchored calendar
than z8 by default** -- resolve each zone independently from the dates above.

## Section A -- Annual vegetables

**Primary source:** OSU Extension EM9027, "Growing Your Own" -- table "Dates for planting
vegetables in Oregon" (osu_em9027). T1 (.edu, OSU ScholarsArchive).
URL: https://ir.library.oregonstate.edu/downloads/v979v342w

This table gives real, dated, region-specific planting windows for 45 vegetables across OSU's
four Oregon regions. **Region 1 (Coast, Astoria to Brookings)** is the z9/coastal archetype
station-region; **Region 2 (Western valleys, Portland to Roseburg)** is the z8/lowland-valley
archetype. Full table (all rows, verbatim from the extracted PDF):

| Vegetable | Start indoors before planting | Region 1 (Coast) | Region 2 (W. valleys) |
|---|---|---|---|
| Artichokes (globe) | crown pieces | Aug.-Oct., May-June | Aug.-Nov., April-June |
| Asparagus | 1 year | March-April | Feb.-March |
| Beans (lima) | not suitable | not suitable | May-June |
| Beans (snap) | not suitable | May-June | May-July |
| Beets | not suitable | March-June | March-June |
| Broccoli | 6 weeks | May-June | March-Aug. |
| Brussels sprouts | 6 weeks | May-June | May-July |
| Cabbage | 6 weeks | Jan.-April, July-Sept. | April-June |
| Cantaloupes | 4 weeks | not suitable | May |
| Carrots | not suitable | Jan.-June | March-July 15 |
| Cauliflower | 6 weeks | Jan. & June | April-July 15 |
| Celery | 9 weeks | March-June | March-July |
| Chard | not suitable | Feb.-May | April-July |
| Chinese cabbage | 4 weeks | July-Aug. | August |
| Chives | 6 weeks | April-May | March-May |
| Corn (sweet) | not suitable | April-May | April-June |
| Cucumbers (slicing) | 4 weeks | April-June | May-June |
| Cucumbers (pickling) | 4 weeks | May | May-June |
| Dill | not suitable | May | May |
| Eggplants | 9 weeks | not suitable | May |
| Endive | 6 weeks | March-July | April-Aug. 15 |
| Garlic | not suitable | Sept.-Oct. | Sept.-Feb. |
| Kale | not suitable | May-July | May-July |
| Kohlrabi | not suitable | July-Aug. | April-Aug. 15 |
| Leeks | not suitable | Feb.-April | March-May |
| Lettuce (head) | 5 weeks | Feb.-July | April-July |
| Lettuce (leaf) | 5 weeks | Feb.-Aug. | April-Aug. |
| Okra | 8 weeks | not suitable | not suitable |
| Onions | 10 weeks | Jan.-May | Mar.-May |
| Parsley | 10 weeks | Dec.-May | Mar.-June |
| Parsnips | not suitable | May-June | April-May |
| Peas | not suitable | Jan.-Aug. | Feb.-May |
| Peppers | 10 weeks | May | May-June |
| Potatoes (sweet) | 6 weeks | not suitable | not suitable |
| Potatoes (white) | not suitable | Feb.-May | April-June |
| Pumpkins | 4 weeks | May | May |
| Radish | not suitable | All year | March-Sept. |
| Rhubarb | crown pieces | Dec.-Jan. | March-April |
| Rutabagas | not suitable | June-July | June-July |
| Spinach | not suitable | Aug.-Feb. | April & Sept. |
| Squash (summer) | 4 weeks | May | May-June |
| Squash (winter) | 4 weeks | May | May |
| Tomatoes | 8 weeks | May-June | May |
| Turnips | not suitable | Jan. & Aug. | Apr.-Sept. |
| Watermelons | 4 weeks | not suitable | May |

(Region 1 = "not suitable" appears for artichoke(Region3/4 only, R1 is fine), lima beans,
cantaloupe, eggplant, okra, sweet potato, watermelon -- all warm-season/heat-loving crops.)

**Critical flag for Task 4/6/7:** Region 1 (z9/coastal) is genuinely **less suitable, not more
suitable**, for warm-season crops than Region 2 (z8/valley) -- OSU's own table marks tomato,
pepper, eggplant, cantaloupe, watermelon, okra, and sweet potato as "not suitable" or far more
restricted for the coast. Cool marine summers (fog, onshore flow, moderate daytime highs) push
these crops to marginal or unviable in z9. **Do not default z9 cells for these crops to an
easier/earlier window than z8** -- if anything the reverse; give z9 conservative/marginal
treatment (shortened window, `season_over`, or thin-source honesty note) for the heat-loving
class.

**Corroborating / supplementary source:** WSU Extension EM057E (formerly EB0422/EB0648), "Home
Vegetable Gardening in Washington" (Miles et al., WSU Dept. of Horticulture, published Feb. 2013)
(wsu_em057e). T1 (.edu). URL:
https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf

- **Table 4** (seeding recommendations, adapted from Kumar et al. 2009, WSU PNW0170) gives real,
  numeric seeding depth / row & plant spacing / germination days / optimum soil temperature /
  base air temperature / weeks-to-transplant / days-to-maturity for ~60 vegetable crops grown in
  Washington -- including several crops **not present** in the OSU EM9027 table: **tomatillo**
  (depth 1/4-1/2", soil temp 70-85F, base temp 51F, 5-6 wk to transplant, DTM 55-90, same
  parameters as tomato), **fennel/finocchio**, **corn salad**, **New Zealand spinach**, **Belgian
  endive**, **celeriac**, **salsify**, **Jerusalem artichoke**, and others.
- **Table 5** (a graphic, color-coded planting calendar for the "Pacific Northwest," adapted from
  Miles 2010, WSU Master Gardener Manual EC0001) includes calendar rows (seedling/transplant/
  harvest color bands by month) for **basil**, **cilantro**, **corn salad**, **dill**,
  **tomatillo**, and **mustard greens** among ~55 crops -- confirming these crops DO have a
  WSU-sanctioned PNW growing calendar. However, **Table 5's actual month boundaries are
  color-coded/graphic, not printed as text**, so precise numeric windows for these specific crops
  were not reliably extractable from this pass (see PDF-extraction notes). Treat this as
  **categorical confirmation of viability + general season**, not a precise window; a targeted
  pull of the underlying color values (or a follow-up numeric source) is needed before Task 4
  should assign these crops a full frost-anchored `resolved_from`-backed window with the same
  confidence as the OSU EM9027 crops.
- **Table 1** classifies warm- vs. cool-temperature crops (matches OSU's suitability pattern:
  eggplant/okra/sweet potato flagged as needing the most warmth, tunnel/greenhouse in cooler
  areas).
- **Figure 1** gives the statewide frost-date/frost-free-days maps cited above (top block).

## Section B -- Tree fruit (bloom + harvest windows, western WA/OR)

**Source:** WSU Extension EB0937, "Fruit Handbook for Western Washington: Varieties and Culture"
(Moulton & King, WSU Mount Vernon NWREC, revised Jan. 2008) (wsu_eb0937). T1 (.edu). URL:
https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf

This is a 40-year variety-trial handbook from WSU's Skagit Valley research station (maritime,
zone-8-equivalent site) and is the authoritative regional source for apple, pear, Asian pear,
plum/prune, cherry, peach/nectarine, and apricot in the maritime PNW. It explicitly covers only
tree fruit + vine/bush fruit (grape, kiwi, currant, gooseberry, aronia, seaberry) plus a short
"Other Fruit" section (quince, fig, pawpaw, persimmon, cornelian cherry, mountain ash, Shipova);
it explicitly does NOT cover blueberry/strawberry/raspberry/blackberry (covered in a separate,
no-longer-freely-available bulletin -- see Section C).

**Ripening (harvest) windows, verbatim from the variety lists** (representative varieties per
kind, earliest to latest within each):

- **Apple**: early Aug. (Sunrise, Pristine) through late Oct.-early Nov. (Mutsu). Most
  commercial-quality varieties cluster **early Sept. to late Oct.**
- **Pear (European)**: "fall pears" pick **Aug.-Sept.**, store 4-6 weeks (Red Clapp's Favorite,
  Bartlett); "winter pears" pick **Sept.-Oct.**, store 3-4 months (Seckel, Comice, Bosc).
- **Asian pear**: ripe **early Aug. (Hamese) to mid-Oct. (Atago)**.
- **Plum/prune**: Japanese types ripe **mid-July to late-Aug.**; European types ripe **mid-July
  to late-Sept.**
- **Sweet cherry**: ripe **mid-June (Early Burlat) to early Aug. (Hudson, Sweetheart)**; most
  cluster **early-mid July**.
- **Tart (pie) cherry**: ripe **early-mid July** (Surefire, Montmorency).
- **Peach/nectarine**: ripe **mid-July to mid-Aug.**
- **Apricot**: ripe **late July to late Aug.** (difficult/marginal crop in this climate -- see
  thin-source note below).
- **Fig**: breba (overwintered) crop ripens **August**; fall crop typically fails to ripen in this
  climate and should be removed unripe.
- **Quince**: harvest implied Oct. (per Fruit Calendar, grouped with pears/apples).

**Fruit Calendar (pp. 36-37 of the bulletin)** gives an explicit month-by-month harvest table
(the single cleanest T1 source for absolute calendar months): **July** -- cherries, early
peaches/plums/apricots; **Aug.** -- apricots, plums, peaches, nectarines; **Sept.** -- figs, sea
buckthorn, cornelian cherry, aronia; late peaches/plums; early pears, early apples, Asian pears;
**Oct.** -- pawpaw, hardy kiwi, table grapes; Asian pears, pears, apples, quinces, Shipova; **Nov.**
-- fuzzy kiwi, persimmons.

**Bloom timing:** the handbook gives only *relative* bloom order per fruit kind (Early/Mid/Late
within that kind's own bloom season -- Tables 2-5), not absolute calendar dates. The same Fruit
Calendar implies **absolute bloom months** via cultural-activity timing: "(Popcorn stage to petal
fall) control for brown rot/coryneum in stone fruits" is listed under **April**, and "check bee
pollination" is listed under **April-May**; "(Stage 2-3) delayed dormant control" (i.e.,
pre-bud-break) for apple/pear is listed under **March**. This implies apple/pear/most stone fruit
bloom clusters in **April** in the maritime lowlands, with apricot blooming earliest (the
handbook separately notes apricot is "very sensitive to frost at bloom time," implying a
March-ish bloom) and sweet cherry/plum spanning **March-April** depending on variety earliness.
Task 5 should treat "April" as the default bloom-window anchor for apple/pear/cherry/plum unless
a variety-specific reason (e.g., apricot, very-early Japanese plum) argues for March.

**Chill note (from EB0937's introduction):** "the coastal maritime climate of western
Washington... is characterized by mild wet winters... [a] hard frost in February or March can
damage early flowering fruit kinds like apricots [but] is rarely cold enough to do permanent harm
to temperate-climate varieties." This corroborates (does not itself quantify) the ample-chill
framing used in the chill-band derivation below.

## Section C -- Berries & strawberry

**Harvest-window source:** WSU Extension, Whatcom County -- "Seasonal Harvest Guide" (courtesy
Whatcom County Farm Friends / Ag Preservation Committee) (wsu_whatcom_harvest). T1 (.edu). URL:
https://extension.wsu.edu/whatcom/seasonal-harvest-guide/

| Crop | Harvest window |
|---|---|
| Strawberries | May-June |
| Cherries | May-June (+ pie cherries) |
| Raspberries | June-Aug., second crop Sept. |
| Blackberries | July-Aug. |
| Blueberries | July-Sept. |
| Boysenberry / Marionberry / Loganberry / Tayberry | July-Aug. |
| Gooseberry | June |
| Apricots | June-July |
| Peaches / Nectarines | July-Sept. |
| Plums | Aug.-Sept. |
| Pears | Aug.-Nov. |
| Apples | Sept.-Dec. (stored varieties year-round) |
| Asian pears | Sept.-Nov. |
| Kiwi | Oct.-Dec. |

**Blueberry cultural-timing source:** WSU Skagit County Extension, "Ask a Master Gardener" --
"Growing blueberries: Start with the right soil..." (Kari Ranten, 07/03/2025, citing Lisa Wasko
DeVetter, WSU NWREC associate professor of small-fruit horticulture) (wsu_skagit_blueberry). T1
(.edu). URL:
https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2073/2025/07/Growing-Blueberries-Start-Right.pdf

Key extracted facts: plant **January-March**; northern highbush (*Vaccinium corymbosum*) is the
common WA type, self-fertile but benefits from a second overlapping-bloom cultivar; water
**May-Aug.**; net against birds **mid-June through harvest completion in August**; prune in
**winter or early spring**.

**Strawberry cultural-timing source:** WSU Clallam County Extension Master Gardener presentation,
"Growing Strawberries" (Jeanette Stehr-Green, 2021) (wsu_clallam_strawberry). T1 (.edu). URL:
https://s3.wp.wsu.edu/uploads/sites/2069/2021/06/Growing-Strawberries-in-the-Home-Garden-J-Stehr-Green-2021.pdf

Key extracted facts: three bearing types -- **June-bearers** (crop June-July; recommended
maritime cultivars Benton, Hood, Rainier, Puget Reliance, Puget Summer, Sweet Sunrise, Shuksan,
Tillamook), **everbearers** (early summer + smaller fall crop; Fort Laramie, Quinault), and
**day-neutrals** (crop all summer; Albion, Seascape, Tribute, Tristar), citing OSU EC1618
"Strawberry Cultivars for Western Oregon and Washington" as the cultivar reference. Winter
hardiness to 10-20 degF but blossoms/buds damaged at 30 degF (frost-sensitive at bloom); renovate
June-bearers a week after harvest (mow foliage, thin rows).

**Thin/gap note (caneberry cultural timing):** WSU's dedicated small-fruits bulletin covering
raspberry/blackberry culture in detail, EM103E "Growing Small Fruits in the Home Garden" (Brun,
Benedict, DeVetter, 2015; supersedes EB1640), is **not freely available online** as a downloadable
PDF (WSU's own catalog page states it is "flash drive only," no free hosted copy found on a
`wsu.edu`/`.edu` domain during this pass -- a `skagitmg.org` reproduction exists but that host is
not `.edu`/`.gov` and was excluded per the T1 rule). Caneberry **harvest windows are T1-sourced**
(Whatcom Harvest Guide, above); caneberry **planting/pruning cultural timing is thin** for this
pass -- flag for Task 7 to treat conservatively or seek a targeted follow-up source.

## Section D -- Chill data

**Source:** WSU Skagit County Extension / WSU Mount Vernon NWREC -- "The Importance of Chilling"
(Sheri Hunter, April 8, 2016) (wsu_chilling_skagit). T1 (.edu). URL:
https://s3.wp.wsu.edu/uploads/sites/2073/2014/03/The-Importance-of-Chilling-Temperatures.pdf

Verbatim: **"Skagit Valley averages 1468 hours of chilling annually, varying from 968-1950 hours
(AWN [WSU Agricultural Weather Network], 2007-15)."** This is the load-bearing figure for the
chill-band derivation below.

**Model-nuance caveat (important, and explicitly flagged in the source itself):** "Some sources
define a chill hour, or chill unit, as exposure to temperature ranging from 32-45 degF, others,
including WSU Mount Vernon weather station, simply say an hour below 45 degF." WSU's own
practical station figure (968-1950 hrs) uses the simpler "hour below 45 degF" proxy, not the
canonical Utah/modified-Weinberger 32-45 degF window already baked into this dataset's
`region_chill_delivered` model. In a maritime winter that rarely sustains long stretches below
32 degF, the divergence between the two definitions is expected to be small, but it is not zero
-- treat the Skagit figure as a very close, not exact, proxy for the modified-Weinberger number.
This nuance is carried into the JSON provenance string.

## Section E -- Sourcing table (crop_or_class | source_id | url | windows | frost_dates | tier | notes)

| crop_or_class | source_id | url | windows | frost_dates | tier | notes |
|---|---|---|---|---|---|---|
| Annual vegetables (45 crops, both zones) | osu_em9027 | https://ir.library.oregonstate.edu/downloads/v979v342w | full month-by-month table, Section A | n/a (planting-date table, not frost-normal table) | T1 (.edu) | Region 1=z9 archetype, Region 2=z8 archetype; z9 "not suitable" flags on warm crops |
| Annual vegetables corroboration + tomatillo/fennel/corn-salad/etc. seed spec | wsu_em057e | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | Table 4 numeric seed spec; Table 5 graphic calendar (categorical only) | Fig. 1 map (categorical, corroborates NOAA) | T1 (.edu) | Table 5 month boundaries are graphic, not text -- categorical confirmation only |
| Tree fruit: apple, pear, Asian pear, plum, cherry, peach/nectarine, apricot | wsu_eb0937 | https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf | full ripening windows by variety, Section B; Fruit Calendar pp.36-37 | n/a (bloom inferred from cultural-activity calendar, not stated as absolute date) | T1 (.edu) | Bloom given only as relative order (Early/Mid/Late); April is the reasoned absolute-bloom anchor |
| Berries/tree-fruit harvest calendar (whole-county overview) | wsu_whatcom_harvest | https://extension.wsu.edu/whatcom/seasonal-harvest-guide/ | month ranges, Section C table | n/a | T1 (.edu) | HTML page, general county harvest calendar |
| Blueberry cultural timing | wsu_skagit_blueberry | https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2073/2025/07/Growing-Blueberries-Start-Right.pdf | plant Jan-Mar, water May-Aug, net mid-Jun-Aug, prune winter/early spring | n/a | T1 (.edu) | 2025, cites WSU NWREC faculty |
| Strawberry cultural timing + bearing-type calendar | wsu_clallam_strawberry | https://s3.wp.wsu.edu/uploads/sites/2069/2021/06/Growing-Strawberries-in-the-Home-Garden-J-Stehr-Green-2021.pdf | June-bearer/everbearer/day-neutral windows, Section C | winter hardy to 10-20F, bloom damaged at 30F | T1 (.edu) | cites OSU EC1618 cultivar list |
| Frost-date normals, z8 | noaa_wr257_seattle | https://www.weather.gov/media/wrh/online_publications/TMs/TM-257.pdf | n/a | last_frost Mar 21, first_frost Nov 12, 1945-1997 | T1 (.gov) | Sea-Tac Airport station |
| Frost-date normals, z9 | noaa_wr250_astoria | https://www.weather.gov/media/pqr/climate/ClimateBookAstoria/ASTclimatebook.pdf | n/a | last_frost Mar 29, first_frost Nov 9, 1991-2020 | T1 (.gov) | Astoria station; freeze-free window SHORTER than z8 despite milder zone (see caveat, top block) |
| Chill-hour figure | wsu_chilling_skagit | https://s3.wp.wsu.edu/uploads/sites/2073/2014/03/The-Importance-of-Chilling-Temperatures.pdf | n/a | n/a | T1 (.edu) | Skagit Valley AWN 2007-15: 968-1950 hrs, avg 1468; "hour below 45F" proxy model, see Section D nuance |

## Section F -- Thin-source flags (explicit, for Task 4/5/6/7 to treat conservatively)

- **Ornamental flowers** (marigold, zinnia, cosmos, sweet pea, viola, sweet alyssum, nasturtium,
  calendula, echinacea, bee balm): no T1 PNW planting-window source found. EM057E and EM9027 are
  both vegetable-only bulletins. **Fully thin.**
- **Perennial herbs except chive** (rosemary, thyme, sage, oregano, mint, lavender, lemongrass):
  no T1 PNW planting-window source found (chive alone is covered numerically in EM057E Table 4 and
  in the OSU EM9027 table). **Fully thin.**
- **Basil, cilantro/coriander, corn salad, dill, mustard greens**: WSU EM057E Table 5 gives
  categorical confirmation of a PNW growing calendar for these (color-coded chart), but exact
  month windows were not extractable as text this pass. **Downgraded from "no source" to
  "qualitative source only, no precise numeric window."**
- **Tomatillo**: previously flagged thin; now **resolved** -- EM057E Table 4 gives a full numeric
  seed spec matching tomato's parameters (70-85F soil temp, 51F base temp, 5-6 wk to transplant,
  DTM 55-90), and Table 5 confirms a transplant-based calendar shape like tomato's. No longer thin.
- **Dry bean** (as a distinct end-use/DTM class from fresh snap/lima/pole beans): OSU EM9027 and
  WSU EM057E both cover *Phaseolus vulgaris* bush/pole types for fresh use; dry bean uses the same
  planting window (frost-anchored, warm soil) with a longer DTM to full maturity/dry-down. This is
  a reasoned analogy, not a distinct T1 citation for "dry bean" by name. **Partially thin** --
  window is sound, DTM-to-dry-maturity is not independently sourced.
- **Sunflower**: absent from both EM9027 and EM057E (Table 4/5/7). **Fully thin.**
- **Caneberry (raspberry/blackberry) planting + pruning cultural timing**: harvest window is
  T1-sourced (Section C); planting/pruning timing is not (WSU's dedicated bulletin, EM103E, has no
  free `.edu`-hosted copy located this pass). **Partially thin.**
- **Apricot, peach/nectarine**: sourced (Section B) but the source itself flags these as
  marginal/difficult in this climate (frost-sensitive bloom, disease pressure, "good crop only
  about one year in three" for apricot) -- Task 5 should carry this honesty into the cell's
  suitability framing rather than treating the ripening-window figure as a guarantee of reliable
  fruiting.
- **Edge/marginal trees beyond EB0937's "Other Fruit" section** (olive, pomegranate, mulberry,
  elderberry): EB0937 covers fig, quince, pawpaw, persimmon, cornelian cherry, mountain ash,
  Shipova, but NOT olive, pomegranate, mulberry, or elderberry. **Fully thin** for these four.
- **OSU-specific berry bulletins** (OSU EM9177-9180 berry series, WSU C008-Blueberries,
  WSU C116-Raspberries): returned HTTP 403 on `extension.oregonstate.edu` and some
  `s3.wp.wsu.edu` catalog paths during this pass, or (WSU C116) turned out to be a Spokane
  County/eastern-WA continental-climate publication, not applicable to the maritime region.
  Excluded; substitute sources used instead (Section C).

## PDF-extraction notes

- WebFetch's own text extraction failed (reported "binary/garbled/compressed stream") on nearly
  every real PDF encountered; the tool nonetheless saves the fetched file locally, and a direct
  `Read()` on that cached path succeeds via native multimodal PDF parsing (full text, tables, and
  images). This was the working pattern for every WSU/OSU/NOAA PDF cited above.
- The `Read` tool's `pages` parameter requires `pdftoppm`/poppler-utils, which is not installed in
  this environment -- omit `pages` and read the whole document (worked without issue even for a
  107-page NOAA climate memo and an 8.2MB, 26-page WSU bulletin).
- Raw `curl` via Bash is denied outright by the sandbox's permission system; all fetching went
  through WebFetch + the cached-path Read() pattern above.
- WSU EM057E's Table 5 (PNW planting calendar) is a genuine gap: it is a color-coded graphic
  chart, and while the multimodal read renders it as an image I can see, reliably reading 30+ rows
  x 36 sub-columns of color bands back into precise month boundaries was judged too error-prone to
  responsibly report as numeric fact -- I reported it as categorical/qualitative confirmation only
  (see thin-source flags) rather than fabricate implied precision the source does not offer as
  text.
- Several OSU Extension catalog/publication pages (`extension.oregonstate.edu/catalog/...`) and a
  couple of `s3.wp.wsu.edu` PDFs returned HTTP 403 and were excluded rather than substituted with
  a lower-tier source.
