# RGV annual planting windows -- extracted T1 tables (for Task 4 / Task 7)

**Date:** 2026-07-13
**Purpose:** the per-crop RGV planting windows that Task 3 flagged as PDF-locked. Extracted via
`pypdf` (controller environment; subagent sandboxes block network + PDF tooling) from two Tier-1
Texas A&M AgriLife Extension sources. This is the authoritative window data Tasks 4/7 author the
annual `rgv` cells from. Cite `tamu_agrilife` with the specific URL below in each cell's
`anchoring_urls`.

## Sources (both T1, verified live 2026-07-13)

1. **`tamu_lrgv_veg_bilingual`** -- "Vegetable Crops of the Lower Rio Grande Valley" (Barbara Storz,
   TAMU AgriLife Extension), a clean Spring/Fall/days-to-harvest table.
   `https://agrilifeextension.tamu.edu/wp-content/uploads/2025/08/Bilingual-Vegetable-Planting-Guide.pdf`
2. **`tamu_rgv_veg_guide`** -- "RGV Homeowner Vegetable Guide" (Jennifer Herrera + Fernando Lamas;
   reviewer Dr. Juan Anciso, TAMU AgriLife Vegetable Specialist), per-crop windows + variety +
   transplant detail (Revised 3/7/2022).
   `https://cameron.agrilife.org/files/2022/05/RGV-Homeowner-Vegetable-Guide-2022.pdf`

Where the two differ, the RGV Homeowner Guide (source 2) is the more RGV-specific, more detailed
authority; the bilingual table (source 1) is the clean corroborating structure. Both are cited.

## Table A -- "Vegetable Crops of the LRGV" (source 1, English column, VERBATIM)

Format: `Crop | Spring window | Fall window | days to harvest` (`-` = not grown that season).

| Crop | Spring | Fall | DTH |
|---|---|---|---|
| Beans (Snap & Lima) | 3/1 to 3/31 | 8/10 to 9/15 | 50-80 |
| Beets | - | 9/1 to 2/14 | 50-90 |
| Bok Choi & Pak Choi | - | 10/1 to 12/31 | 90 |
| Broccoli | - | 9/1 to 12/31 | 80-100 |
| Brussels Sprouts | - | 9/1 to 11/30 | 110-140 |
| Cabbage | - | 9/1 to 12/1 | 90-120 |
| Carrots | - | 9/15 to 12/31 | 90-100 |
| Cauliflower | - | 9/1 to 11/30 | 90-120 |
| Cantaloupe & Honeydew | 2/25 to 3/20 | 8/1 to 9/1 | 85-90 |
| Celery (Seeded) | - | 8/1 to 9/1 | 150-160 |
| Celery (Transplanted) | - | 9/1 to 11/30 | 90-110 |
| Chinese Cabbage | - | 10/1 to 12/31 | 90 |
| Cilantro | - | 9/1 to 2/14 | 50-60 |
| Collards | - | 9/1 to 2/14 | 40-60 |
| Sweet Corn | 2/14 to 3/20 | 8/1 to 9/1 | 85-90 |
| Cucumber | 2/14 to 4/15 | 8/15 to 9/15 | 65-70 |
| Dandelion | - | 9/1 to 12/31 | 55-60 |
| Dill | - | 9/1 to 12/31 | 60-70 |
| Eggplant | 2/14 to 3/20 | 6/15 to 8/15 | 100-120 |
| Endive, Escarole, Frisee | - | 9/1 to 12/31 | 110 |
| Fennel | - | 9/1 to 12/31 | 55 |
| Kale | - | 9/1 to 2/14 | 50-60 |
| Kohlrabi | - | 9/1 to 2/14 | 75-100 |
| Leek | - | 9/1 to 2/14 | 75-100 |
| Lettuce (Head) | - | 9/1 to 12/31 | 80-90 |
| Lettuce (Leaf) | - | 9/1 to 2/14 | 40-60 |
| Mustard Greens | - | 9/1 to 2/14 | 40-60 |
| Okra | 2/14 to 3/20 | - | 100-120 |
| Onion | - | 10/1 to 12/1 | 100-150 |
| Parsley | - | 9/15 to 2/14 | 90-100 |
| Parsnips | - | 9/15 to 12/31 | 100-120 |
| Sweet Peas (English) | - | 9/1 to 9/30 | 70-80 |
| Southern Peas | 3/1 to 4/15 | 9/1 to 9/30 | 65-75 |
| Hot Peppers | 2/14 to 3/20 | 8/10 to 9/15 | 80-100 |
| Sweet Peppers | 2/14 to 3/20 | 7/15 to 8/15 | 90-100 |
| Pumpkin & Winter Squash | 3/1 to 4/15 | 8/1 to 9/1 | 90-120 |
| Potato | 12/15 to 1/15 | - | 90-100 |
| Sweet Potato | 3/15 to 4/15 | - | 90-120 |
| Radish | - | 9/1 to 2/14 | 25-30 |
| Swiss Chard | - | 9/1 to 2/14 | 50 |
| Bloomsdale Spinach | - | 9/1 to 2/14 | 45-60 |
| Flatleaf Spinach | - | 9/15 to 2/14 | 45-60 |
| Summer Squash | 2/14 to 4/15 | 8/15 to 9/15 | 40-60 |
| Tomato | 2/14 to 3/20 | 8/10 to 9/15 | 90-120 |
| Turnip | - | 9/15 to 1/1 | 50-70 |
| Watermelon | 2/14 to 3/20 | 8/10 to 9/1 | 90-100 |

(Note: source prints `11/31` for Brussels sprouts/cauliflower fall-end and `9/31`-style artifacts;
these are transcribed to the valid month-end above.)

## Table B -- RGV Homeowner Guide per-crop windows (source 2, curated; overrides Table A where more specific)

- **Green Bean (bush):** early March; again early-late September (fall). Varieties Derby/Blue Lake 274/Contender.
- **Green Bean (pole):** early March; again early-mid September (to late Sept diminished).
- **Sweet Corn:** late February-late March; again late August-mid September. Golden Queen/Silver Queen/G90.
- **Pepper (hot + sweet):** transplants set out late February-mid March; again mid-late September. Start seed in flats 3-4 wks before transplant.
- **Potato:** mid-December-late January (best December). Red LaSoda/Kennebec/Yukon Gold.
- **Tomato:** transplants set out mid-February-early March; again mid-September-mid-October (fall can start as early as July with afternoon shade; high heat drops blossoms). Tycoon/Better Boy/Celebrity/Charger.
- **Watermelon:** late February-late March. Legacy/Sangria/Crimson Sweet/Sugar Baby.
- **Cantaloupe:** late February-late March (same culture as watermelon).
- **Zucchini Squash:** late February-early April; again late August-mid September (fall).
- **Butternut Squash:** early March; again early-mid September (fall).
- **Broccoli:** early September-early December (start seed in flats; transplant preferably no earlier than early October, best by mid-October). Packman/Belstar/Green Magic/Marathon.
- **Cabbage / Collards / Cauliflower / Kale / Kohlrabi:** "same time as broccoli" (early Sept-early Dec, transplant by mid-Oct).
- **Spinach:** mid-October-mid-January.
- **Swiss Chard:** mid-October-January (direct); flats can start early September, transplant no earlier than mid-October.
- **Beets:** mid-October-end December.
- **Carrot:** mid-October-mid-December.
- **Turnip:** mid-October-mid-December.
- **Cowpeas (southern pea):** early March; again early September (fall). Texas Pinkeye/Dolico.
- **Cilantro:** early October-early February.
- **Dill:** early October-mid-December (best late Oct-early Nov, heat reduces germination).
- **Onion (bulbing):** mid-October-mid-December (1015Y no later than end October, ~150 days). Texas 1015Y/Texas Early White.
- **Onion (bunching):** mid-October-mid-December.
- **Leek:** mid-October-mid-November (start in flats, transplant).
- **Sweet Potato:** late March-end April (slips).

## Slug-mapping guidance for Task 4 (dataset slug -> guide row)

Author each of the 79 frost_anchored annual slugs from its best-matching guide row. Notes:
- Multiple dataset slugs map to ONE guide row (author them consistently to that row): the cucumber
  family (cucumber/english-cucumber/pickling-cucumber/slicing-cucumber) -> "Cucumber"; the tomato
  family (cherry/roma/grape/beefsteak/heirloom-tomato) -> "Tomato" (tomatillo -> warm-season
  analog); the pepper family (bell-pepper -> Sweet Peppers; jalapeno/cayenne/habanero/serrano ->
  Hot Peppers; banana-pepper -> Sweet Peppers); the summer-squash family (summer-squash/
  yellow-summer-squash/zucchini-courgette) -> "Summer Squash"/"Zucchini"; winter-squash +
  butternut-squash + pumpkin -> "Pumpkin & Winter Squash".
- Cool-season crops here are FALL/WINTER crops (fall window only, summer = `season_over`); the
  Homeowner Guide's mid-October transplant nuance is the beginner-facing "best" date.
- Warm-season crops carry a spring window + a fall window (`second_planting`) around a mid-summer
  gap; per the summer-gap rule, use `season_over` for the gap unless a T1 heat-stop is stated
  (tomato's "high heat makes plants drop blossoms" is the one explicit heat basis in these sources).
- **Crops NOT in these two guides** (e.g. basil and other warm herbs, arugula) get a conservative
  cell: warm herbs follow the warm-season spring+fall pattern (basil is frost-tender, plant after
  the last rare frost ~late Feb); leafy cool herbs/greens follow the cool-season fall/winter
  pattern. Flag any crop with no guide row + no clean corroborating T1 window as thin in the cell's
  provenance, and author conservatively -- never fabricate a precise date.
- **Confirm the exact 79-slug roster** with the Task-4 roster query before authoring; if `leek` or
  another crop is NOT among the 108 certified region-carrying crops, skip it (it is out of scope
  until its own certification).
