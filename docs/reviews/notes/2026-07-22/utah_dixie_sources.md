# Utah "Dixie" region -- T1 sourcing note + shard bible (Task 3)

All sources are **USU Extension (`usu_ext`)**, T1, `extension.usu.edu`, verified **2026-07-22**. Every
authored window/verdict traces to a page below. Non-USU aggregators are NOT used.

## Region identity + frost anchor
- `region_id = "utah_dixie"`, `region_label = "Utah: St. George Dixie (Mojave-edge high desert)"`, `zone_span = ["8"]` (SINGLE zone).
- **Frost anchor z8: last frost Mar 30 / first frost Nov 1** -- USU Washington County, "Elevations for Washington County" (2020), St. George row marked Utah Climate Center actual-record. Cross-confirmed by "Suggested Vegetable Planting Dates for Utah" ("last spring frost in St. George occurring on March 30"). Secondary (older, more conservative): Heflebower "Fall Gardening in the St. George Area" (2008) gives avg fall frost Oct 23 / ~196-day season. **Use Mar 30 / Nov 1 as the stored `resolved_from`.**
- `resolution_method = "frost_anchored_resolved"`, non-empty `plantings[]` (the anchored-model requirement).

## SOURCE REGISTRATION -- USU per-pub sub-ids (CORRECTED after gating the reference cell)
`region_cell_audit` FORBIDS one source id mapping to two URLs within a single cell. Utah cells cite
MULTIPLE distinct USU pages (a warm cell needs the veg-dates window page AND the tomato heat-abort
page), so a single generic `usu_ext` id does NOT work. Follow the Nevada precedent (per-pub sub-ids
under the family): `tools/staging/utah_dixie_sources.json` registers **8 USU sub-ids** (all T1,
`_admission_provenance` set). **Each cell cites ONLY the specific sub-ids it uses, each with its own
page URL in `anchoring_urls`.** The id -> page -> use map:

| source_id | page | cite it for |
|---|---|---|
| `usu_ext_veg_dates` | Suggested Vegetable Planting Dates | spring windows (Group A-D dates) + fall Group E dates |
| `usu_ext_tomato` | How to Grow Tomatoes | the >95 degF/<50 degF heat-abort -> `heat_pause` basis |
| `usu_ext_wash_fruits` | Washington County Fruits | tree suitability (the elevation split; apple/pear marginal) |
| `usu_ext_raspberry` | Raspberry Management for Utah | raspberry Utah's-Dixie fall-bearing steer |
| `usu_ext_garlic` | Garlic in the Garden | garlic fall clove window |
| `usu_ext_fall_veg` | Fall Gardening in the St. George Area | cool-crop fall windows + fall-planted storage onion |
| `usu_ext_wash_frost` | Elevations for Washington County | frost anchor Mar 30/Nov 1 + "100 degF Jun-Aug" heat basis |
| `usu_ext_peaches` | How to Grow Peaches | low-chill stone-fruit variety selection (chill 500-1050 per-variety) |

A cell's `sources` list = the sub-ids it cites; `anchoring_urls` maps each to its page. (The parent
`usu_ext` entry stays in the catalog; these are additional sub-ids, like Nevada's `unr_sp9911` under
`unr_ext`.) Prune any sub-id that ends up uncited before the promote (Task 9 footprint audit).

## USU planting-date GROUP structure ("Suggested Vegetable Planting Dates for Utah," Table 1)
Vegetables grouped A-D by cold tolerance; St. George gets **explicit warm-adjusted dates** (NOT the
generic frost-relative rule -- St. George's row is ~2 weeks earlier than a naive derivation):

| Group | Tolerance | **St. George date** | Crops |
|---|---|---|---|
| A | Hardy | **Feb 15** | radish, turnip, spinach, peas, onions, broccoli, cabbage, Brussels sprouts (+ kale/collards/bok-choy/arugula/kohlrabi) |
| B | Semi-Hardy | **Mar 1** | carrot, beet, lettuce, Swiss chard, cauliflower, potato, parsley, parsnip |
| C | Tender | **Mar 15** | sweet corn, cucumber, summer squash, snap bean, dry bean (direct sow) |
| D | Very Tender | **Apr 1** | tomato, pepper, eggplant, watermelon, cantaloupe, pumpkin, winter squash |

Warm-crop transplants (Group D): `start_indoors` **~late Feb** (~6 weeks before the Apr 1 set) -> the
`plant_out` is the USU date, the mean frost date (Mar 30) is the stored anchor ("cite the extension
date, resolve to it"). **NO early-Feb workaround needed** (Apr 1 plant + late-Feb indoors leaves Jan
inactive -> honest winter `cold_pause` renders).

## LOAD-BEARING HONESTY RULE: no warm-crop fall planting
USU documents a fall planting **only for cool crops** (Group E + Heflebower). There is NO USU St. George
fall/summer replant for ANY warm crop. So **ALL 42 warm crops = SINGLE spring window, NO `second_planting`**
(delta 4a, applied uniformly). This is a real simplification from Nevada (which had a UNLV-sourced
quick-crop Jul-Aug replant; USU has none -> do NOT author one, no fabricated windows).

## Fall windows (cool crops only)
**Group E "Special Plants for Fall Harvest" (dated):** beets Jul 1-Aug 1; cabbage May 1-Jul 15; kale
Jul 1-Aug 15; lettuce Jun 1-Aug 1; onion Aug 1-Aug 10; spinach Jul 1-Aug 15; turnip Jul 1-Aug 1.
**Heflebower fall guidance (undated, author fall window by analogy + cite Heflebower):** cole crops
broccoli/cauliflower as transplants (~Jul-early Aug, like cabbage); carrots direct-seed (~Jul, like
beet/turnip); collards/bok-choy/kohlrabi/arugula (cole/greens, ~Jul-Aug); "turnips, carrots and beets
can be left in the ground quite late into winter." **Cool crops with NO USU fall window -> spring-only:**
peas (snow/sugar-snap/fava), Brussels sprouts, parsnip, potato, radish-as-fall only if the shard finds
support (Heflebower calls radish large-seeded/easy but gives no fall date -> spring-only unless justified).

## heat_pause (SOURCE IT)
St. George "will reach 100°F in June, July, and August" (Fruits page + frost/elevation doc). Tomato:
"night temperatures lower than 50°F, or day temperatures above 95°F -> tomatoes do not set and flowers
abort" (USU "Tomatoes in the Garden"). **`heat_pause.months = [6,7,8]`** (Jun-Aug) for the heat-ABORT
crops; `basis_seasoned`/`basis_beginner` cite these pages. **NO fall tomato mentioned anywhere.**

## Per-class shape + window map

### WARM (Task 4, 42) -- all SINGLE spring, no fall
- **Shape A (spring window + `heat_pause` Jun-Aug + `cold_pause`):** the heat-abort crops -- tomato
  (beefsteak/cherry/grape/heirloom/roma), pepper (bell/banana/cayenne/habanero/jalapeno), eggplant,
  tomatillo (Group D, plant Apr 1); cucumber (slicing/pickling/english/cucumber), summer squash
  (yellow-summer-squash, zucchini-courgette), green-beans-bush, edamame (Group C, plant Mar 15 -- these
  finish or stall in the Jun-Aug heat). `start_indoors` late Feb for the transplanted Group D set.
- **Shape C (single long heat-lover season, NO `heat_pause`):** melons (cantaloupe/honeydew/watermelon),
  winter squash (acorn/butternut/spaghetti), pumpkin (Group D, plant Apr 1); okra, sweet-potato (NOT in
  Table 1 -- author from heat-lover biology: they thrive through the St. George summer, plant late spring,
  harvest into fall; flag "not in USU Table 1"); dry-bean, pole-beans, sweet-corn/field-corn/flint-corn/
  popcorn (Group C, plant Mar 15, single long season, dry-down/full-season harvest -- no USU fall corn).
- **Shape D (warm herbs/flowers):** basil, lemongrass (warm herbs, love heat -> grow through summer,
  no heat_pause or light one); cosmos, marigold, nasturtium, sunflower, zinnia (warm annual flowers;
  nasturtium fades in peak heat -> may carry a light heat_pause; author per crop). Plant ~Apr 1 or Mar 15.

### COOL (Task 5, 40) -- spring + fall where USU documents it
- Spring dates: Group A (Feb 15) or Group B (Mar 1) per the table above. Two-window (`second_planting`)
  ONLY for the fall-window set above (built via `second_cycle.build_two_cycle_cell`, A43-safe).
- **Alliums (Shape F, delta 4d):**
  - **onion (bulb):** FALL-planted for storage (Heflebower: "Onions that are to be kept for storage
    actually do better if planted now and then harvested next summer. Variety selection here is
    critical."). `recommended_day_length_type = "intermediate_day"` (St. George ~37°N). Fall `plant_out`
    (set/transplant ~Aug-Oct) -> harvest next early summer; NO spring bulb set -> A9 window-fit satisfied
    (VERIFY A9 = 0). Group E onion Aug 1-10 is the fall set date.
  - **shallot:** "follows onion" (species identity).
  - **garlic:** fall clove `plant_out` **late September to November** (USU "Garlic in the Garden": "Plant
    garlic from late September to November"; fall preferred), harvest early-mid summer when tops yellow.
    Author a St. George window in that range (do NOT inherit warm_arid/low_desert_az verbatim).
  - **spring-onion (green onion):** "Green onions can be planted spring or fall as they do not take long
    to mature" (Heflebower) -> two-window, harvested green (no day-length gating).
  - **chives:** perennial allium (spring-fall growth), not fall-set.
- Cool herbs (cilantro-coriander, dill, parsley) + cool flowers (calendula, viola, sweet-alyssum,
  sweet-pea, borage) + perennials (mint, chamomile, bee-balm, echinacea): cool two-window / their biology.

### TREES (Task 6, 14) -- the Washington County "Fruits" elevation split is the direct authority
Verbatim: LOW elevation (St. George): "those fruits that do well include: apricots, cherries, figs,
grapes, peaches, persimmons, plums, and strawberries" (+ nuts). HIGHER elevation (Brookside/Central/
Enterprise/New Harmony, 5,300+ ft, OUTSIDE the z8 belt): "apples, pears, and berries such as raspberries
and blackberries grow well."
- **apple + pear-asian + pear-european = `marginal`** (delta 4b). Region-level `chill_basis_seasoned`/
  `chill_basis_beginner`: only the lowest-chill third crops at St. George's ~2,624 ft (Dorsett Golden 100,
  Anna 200, Ein Shemer 100); Washington County Extension recommends apple and pear only for the county's
  higher-elevation towns (5,300+ ft), not the St. George core; the mid/high-chill varieties do not
  accumulate enough chill here. Cite the Fruits page. (`low_desert_az` "high-chill varieties never fruit
  here" idiom; the INVERSE of Nevada's `fruits_reliably` apple.)
- **`fruits_reliably` (low-elevation list):** apricot, cherry-sour, cherry-sweet, fig, nectarine, peach,
  persimmon, plum. Re-judged arid (late frost + sunburn, not humid brown-rot). Peach nominal chill is
  high (USU per-variety 500-1050) but the county lists peaches as thriving low-elevation -> `chill_basis`
  names low-chill variety selection. **FLAG for content review:** cherry-sour is a high-chill crop yet
  the county lists "cherries" in the low-elevation column -- follow the county (`fruits_reliably`) but the
  reviewer should sanity-check the sour-cherry-vs-low-band tension (Nevada called cherry-sour marginal).
- **mulberry + pomegranate:** NOT named on the Fruits page (page omits them) but classic low-desert fruit
  and `fruits_reliably` in the Nevada/warm_arid donors -> author `fruits_reliably` from desert biology +
  the donor; note "not on the USU Fruits list, judged from low-desert biology + neighbor regions."
- **pawpaw = `unsuitable`** (humid-forest understory tree, dry alkaline Mojave mismatch; on neither list).

### CITRUS (Task 7, 5) -- cold-limited
St. George is a cold-limited desert winter (z8b ~15-20°F lows), colder than Phoenix; the Fruits page does
not list citrus (not a St. George crop). `suitability = "survives"`/`"unsuitable"` (protected/container
where real), `min_winter_temp_f`, `cold_basis_*`. mandarin-clementine hardiest, lime + grapefruit worst.
Author from the Nevada citrus donor (all cold-limited). NO `fruits_reliably`.

### PERENNIALS (Task 8, 10)
- **Woody herbs** (lavender/oregano/rosemary/sage/thyme): desert-STRONG (arid heat + alkaline soil).
- **raspberry = `marginal`** (delta 4c): fall-bearing/low-chill steer. MIRROR the `warm_arid`
  `region_notes_seasoned`. USU "Raspberry Management for Utah" (verbatim): "Along the Wasatch Front and
  in Utah's Dixie, fall-bearing raspberries tend to be better adapted, as the fruit ripens after the
  hottest part of the summer is over, thus avoiding fruit sunburn." Name the fall-bearing/primocane
  cultivars USU lists (**Caroline, Josephine, Polana, Joan J, Polka**) plus the low-chill desert types
  (Bababerry, Dorman Red); note alkaline soil -> iron chlorosis (chelated iron), afternoon shade minimizes
  sunburn, raised beds in heavy soil. Prose steer (no `bearing_habit` field yet).
- **blackberry = `marginal`** (Fruits page higher-elevation column). **blueberry very-marginal** (alkaline
  soil hostile -> container-only honesty in prose). **elderberry marginal.** Berries carry no suitability
  field -> honesty in prose; A32 still requires a calendar.
- **strawberry = low-elevation THRIVER** (delta 4c; Fruits page low-elevation list names strawberries).
  Real calendar; author the positive verdict (better than Nevada's fall-set-only).

## Chill band + hunt outcome (hunt-once-then-flag, DONE)
`region_chill_delivered.utah_dixie = {"8": [250, 450]}`. **The chill-hunt is complete and came up empty:**
no USU-published numeric chill-hour ACCUMULATION figure for St. George / Washington County exists (checked
"How to Grow Peaches" [per-variety requirements 500-1050 only], the Fruits page, the Utah Climate Center /
peach chill materials; all give per-variety REQUIREMENTS, never a regional accumulation total; the only
regional note is general -- "peaches with higher chill requirements are typically better suited to Utah"
re winter warm-spell early-bud-break, not an accumulation number). So `[250,450]` is elevation-bracketed
INFERENCE (Phoenix `[100,400]` below, Las Cruces `[450,850]` above; St. George ~2,624 ft leans Phoenix/
marginal), flagged honestly in `region_chill_delivered_provenance` (see `utah_dixie_chill_band.json`).

## Source URL table (all `usu_ext`, cite via `anchoring_urls`)
| What it backs | URL |
|---|---|
| Frost Mar 30/Nov 1; "100°F in June, July, August" | https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf |
| Group A-D + St. George dates; last frost Mar 30; Group E fall dates | https://extension.usu.edu/yardandgarden/research/suggested-vegetable-planting-dates-for-utah |
| Tomato heat abort >95°F/<50°F; no fall tomato | https://extension.usu.edu/yardandgarden/research/tomatoes-in-the-garden |
| Fall cool-season guidance; storage onion fall-plant; ~196-day season/Oct 23 | https://extension.usu.edu/washington/files/Fall_Vegetable.pdf |
| Tree elevation split (apple/pear higher-elev only; low-elev fruit list) | https://extension.usu.edu/washington/gardening/fruits/ |
| Raspberry "Utah's Dixie" fall-bearing; cultivars; alkaline/chlorosis | https://extension.usu.edu/yardandgarden/research/raspberry-management-for-utah |
| Garlic plant late Sep-Nov, fall preferred | https://extension.usu.edu/yardandgarden/research/garlic-in-the-garden |
| Peach per-variety chill 500-1050; no regional accumulation number | https://extension.usu.edu/yardandgarden/research/peaches-in-the-garden |
