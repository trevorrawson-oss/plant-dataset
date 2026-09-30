# 55 - PLA-10, ground spacing, layout and vertical growing: kickoff (dataset side)

**Written:** 2026-09-29. **READ-ONLY session: canonical unchanged; nothing staged, nothing committed.**
**Canonical measured:** `edcd9bf9` (the committed canonical at HEAD `5fc5357`, `git show HEAD:crops_data_final.json`).
The working tree carried the parallel PLA-533 session's staged subtractive pass (`cd0f9f17`, `LATEST.txt`
already bumped, uncommitted) while this was written; every number below was taken on a scratch copy of
`edcd9bf9` and cross-checked on a scratch copy of `cd0f9f17`. **The two differ, on the fields this arc
touches, only in `rootstock_options` on lemon, lime, orange-navel and grapefruit** (the PLA-533 subtractive
edits); `spacing_inches`, `planting_layout`, `thin_to_inches`, `thinning`, `mature_height_ft`,
`mature_spread_ft`, `footprint_inches` and `det_indet` are byte-identical across the two on all 128 crops.
**Checkout:** branch `main`, HEAD `5fc5357`, origin/main `612059f` (HEAD one commit ahead, the parallel
session's MANIFEST commit). Consumers measured at plant-astro `main` `3f7d2d5` (submodule pin `3f58d7a`
= canonical `83384c85`) and plant-app `feat/community-foundation` `6676406d`.
**Linear, status field checked before trusting any body:** PLA-10 Backlog; PLA-534 Todo (scoping only);
PLA-426 Backlog; PLA-429 Backlog; PLA-465 In Progress; PLA-7 In Progress (closing on PLA-586); PLA-532
**Todo, not started, so none of its sources are admitted**; PLA-607 Backlog; PLA-544 Backlog.

> Every number here was MEASURED with a key walk and regex scans over the scratch canonical, a scan of
> `tools/.doc_cache` keyed by `sha1(url)`, and two read-only sweeps of `~/plant-astro/src` and
> `~/plant-app/src` + `scripts`. Regex-derived populations are UPPER BOUNDS and are labelled as such; the
> firm numbers are the ones taken from a field or from a page read. Re-measure before believing any of
> them in a later session.

---

## 0. The one-paragraph finding

`spacing_inches` already IS in-row spacing on every surface that labels it (plant-astro's hero says
"between plants", plant-app's bed sheet says "inches between plants") and in the prose of 12 of the 18
crops whose own prose states an (in-row, between-row) pair. But it is a **blend** on the cucurbits and the
brambles: butternut's `[24, 72]` is its in-row minimum and its between-row maximum in one pair, acorn and
spaghetti squash carry a `48` that is neither their in-row high (36) nor their row high, watermelon's
`[36, 72]` sits below its own prose hills (4 to 8 ft), and blackberry's `[36, 72]` averages erect and
trailing types. **Both planners use the one number on both axes**, so a potato row is planned at 12 in
between rows where the crop's own prose says 30 to 36. The ruled list-of-layouts shape from August has
never been landed: `planting_layout` is a bare enum string on 6 crops (4 corn `block`, artichoke and
asparagus `row`; the PLA-7 D3 note's "every value block" is wrong by two), gate A44 rejects a dict, and the
asparagus arc downgraded its dict to the string for exactly that reason. `height_inches` collides with
PLA-465's landed, gated, provenance-bearing `mature_height_ft`; the recommendation is to retire the inch
field from PLA-10's shape, not to add a second height. The fork-by-method population is **24 crops** by
what a cited page or the crop's own prose actually states, not 12 to 20, and it forks along **three
different axes** (support, arrangement, cultivar habit) that the August shape folds into one `method` enum.
No technique source is admitted: PLA-532 has not run, and the catalog's 220 entries contain zero
container- or vertical-scoped ids. Neither PLA-607 nor a homepage-anchor gate exists; §F cannot see
`spacing_inches` at all because the field has an `_anchoring_urls` sibling and no `_sources` sibling.

---

## 1. What exists (measured on `edcd9bf9`)

### 1.1 `spacing_inches`

| shape | crops | who |
| -- | -- | -- |
| `[lo, hi]` | **113** | every certified crop that is not a microgreen |
| `[]` | **15** | 8 certified microgreens (legitimately N/A, the timing-spine contract says so) + the 7 shells |
| absent / null / scalar | 0 | |

- Ceiling `360` (mulberry `[300, 360]`); `numeric_sanity` bounds it 1 to 72 on annual bases and 1 to 360
  on tree bases (archetype-aware).
- **Citation slots:** `spacing_inches_anchoring_urls` is non-empty on **11** crops (cherry-tomato,
  roma-tomato, carrot, lemon, grape-tomato, radish, potato, sweet-potato, tomatillo, lime, celery).
  **No crop carries a `spacing_inches_sources` key.** `whole_crop_gate` §F's root-level sibling check keys
  on `*_sources` (`whole_crop_gate.py:1306-1309`), so the 11 anchored spacings are never checked and the
  other 102 certified spacings have no citation slot at all. Section 6 returns to this.
- **Meaning, from the consumers:** plant-astro `HeroCard.astro:204` sub-labels it **"between plants"**
  ("between trees" for fruit trees); plant-app `BedCropSheet.tsx:356-364` labels it **"Plant spacing"**,
  caption "inches between plants". Both planners then use the SAME number for between-row width
  (astro `fit.ts:170-177` `rowWidthFt`; app `fit.ts:181-205` `rowWidthFt`, PLA-423's fallback) and as the
  side of a square for area (`(s/12)^2`). So it is in-row where labelled and both-axes where computed.
- **Meaning, from the prose.** 18 crops state an explicit (in-row, between-row) pair in consumer prose
  (`soil_prep_*`, `start_method.notes_seasoned`, `growth_stages[].user_action_seasoned`,
  `planting_method_notes_*`, region notes). Compared with `spacing_inches`:

| crop | `spacing_inches` | prose in-row | prose between rows | verdict |
| -- | -- | -- | -- | -- |
| bell-pepper | [18, 24] | 18-24 | 30-36 | = in-row |
| jalapeno | [12, 18] | 12-18 | 24-36 | = in-row |
| habanero | [18, 24] | 18-24 | 24-36 | = in-row |
| banana-pepper | [12, 18] | 12-18 | 36 | = in-row |
| cayenne-pepper | [18, 24] | "about 18" | 24-36 | lo = in-row; hi unstated |
| eggplant | [18, 24] | 18-24 | 30-36 | = in-row |
| potato | [10, 12] | 10-12 | 30-36 | = in-row |
| sweet-potato | [12, 18] | 12-18 | 36-48 | = in-row |
| sugar-snap-peas | [1, 2] | 1-2 | 18-24 | = in-row |
| brussels-sprouts | [18, 24] | 18-24 | 24-36 | = in-row |
| raspberry | [18, 24] | 18-24 (red); 30-48 (black) | 72-96 | = in-row for red |
| strawberry | [15, 24] | 15 (matted, generic); 18-24 (regions); 12 (two-row beds) | 36-48 | lo = matted-row in-row; hi = region value |
| **butternut-squash** | **[24, 72]** | 24-36 | 60-72 | **BLEND: in-row lo, between-row hi** |
| **acorn-squash** | **[24, 48]** | 24-36 (bush 18-24) | 36-72 | hi is neither in-row nor row |
| **spaghetti-squash** | **[24, 48]** | 24-36 (bush less) | 36-60 | hi is neither in-row nor row |
| **watermelon** | **[36, 72]** | hills 48-96 | 72-96 | below the crop's own hill spacing |
| **blackberry** | **[36, 72]** | erect 24-48; semi-erect/trailing 72-96 | 96-120 | averages two cane types |
| broad-beans-fava | [4, 8] | sow 4-6, thin to 8-10 | 18-30 | a sowing spacing, not the final stand |

  The 2026-07-01 review notes for the cucurbits say this out loud: cantaloupe "`spacing_inches` [24,36]
  carries in-row/hill spacing; wide row spacing (5-6 ft) is in prose"; spaghetti "`spacing_inches` =
  [24,48] -- in-row 24 in to ~4 ft row"; acorn "[24,48]; bush 18-24 in, vining rows 3-6 ft". The blend
  was authored knowingly and recorded as a prose-carries-the-rest convention.
- `thin_to_inches` exists on **41** crops and equals `spacing_inches` on 40 of them (fava is the one
  difference, `[4,6]` vs `[4,8]`). `thinning.to_spacing` is a free string on 23 crops; on the 6 cucurbits
  it reads "N plants per hill" (onion's is the list `[4, 6]`). Neither consumer reads `thinning`.

### 1.2 `planting_layout`

| crop | value | `pollination_block_min_rows` |
| -- | -- | -- |
| sweet-corn, field-corn, popcorn, flint-corn | `"block"` | 4 |
| artichoke, asparagus | `"row"` | absent |

- It is a **string enum**, gate A44 (`tools/planting_layout_gate.py`, `LAYOUTS = {block, row, hill, grid,
  single}`), conditional (absent on 122, never null). The gate's docstring says `row` is "DEFINED but
  unpopulated"; that is stale by two crops. The PLA-7 issue's 2026-09-21 D3 correction ("`planting_layout`
  exists on 6 crops, every value `"block"`") is wrong by the same two.
- **The ruled list-of-objects shape has never existed in canonical.** The 2026-07-23 asparagus plan wrote
  `{"pattern": "rows", "row_spacing_inches": [48, 60], "in_row_spacing_inches": [12, 18]}` and the cert
  spec §3g downgraded it to the string because "the reference dict CRASHES A44 (`pl not in LAYOUTS` where
  LAYOUTS is a string set -> TypeError)". So the August migration note ("the 6 pilot crops' existing single
  values become one-entry lists") is a shape change on 6 crops PLUS an A44 rewrite, and the row/in-row
  numbers for asparagus live only in prose today.
- plant-app reads it in two places: the "LAYOUT" at-a-glance tile (`at-a-glance.ts:168-173`, "Block",
  sub "Wind-pollinated", only when `block`) and the block-planting advisory in `plot-calc.ts:122-131`
  (`pollination_block_min_rows ?? 4`). plant-astro never reads it.

### 1.3 Row, hill, trellis, stake and vertical spacing stated in prose (regex, consumer strings only;
`verification_status`, `sources`, `anchoring_urls` and legacy `zones{}` excluded)

| signal | crops (upper bound) | where it lives (top fields) |
| -- | -- | -- |
| an explicit between-row number | **18** firm (table above); 33 loose | `soil_prep_*`, `start_method.notes_seasoned`, `growth_stages[].user_action_seasoned`, `thinning.tip_seasoned`, brambles' `planting_method_notes_*` |
| "per hill" / plants per hill | **10** | the 6 cucurbits + cucumber, slicing-cucumber, pickling-cucumber, cantaloupe: `start_method.notes_seasoned`, `thinning.to_spacing`, `growth_stages[]` |
| trellis | 32 | `companions[].why_seasoned`, `container_notes.notes_*`, `container_notes.shape_requirements_*`, `growth_stages[]` |
| stake | 47 | `growth_stages[]`, `container_notes.notes_*`, `start_method.notes_beginner`, `weather_triggers[]` |
| cage | 14 | `container_notes.notes_*`, `det_indet.detail_*` |
| the word "vertical" | 6 | zucchini, heirloom-tomato (a fruit-crack symptom), english-cucumber, yellow-summer-squash, pole-beans, lavender |
| "vertical" as a KEY or enum value | **0** | |
| `height_inches` | **0** | |

Only **6 crops' prose ties a spacing number to a method** in the same sentence (acorn, butternut,
spaghetti, pumpkin, watermelon, honeydew: "bush ... 18 to 24 ... vining ... 24 to 36", "hills 4 to 8 ft
... closer for bush"). No crop's prose gives a staked-vs-unstaked or trellised-vs-ground spacing number;
those live only in the cited pages (section 5).

### 1.4 Other habit fields already on the record

- `det_indet` object on the 6 tomato crops (5 `indeterminate`, roma `determinate`); plant-astro renders
  only `det_indet.type` as a hero line, plant-app ships it and reads nothing.
- `varieties.recommended[].plant_habit` on dry-bean (5 entries: `bush` x4, `half_runner` x1);
  `bearing_habit` on strawberry (9 entries). These are the cultivar axis, already at variety level.
- The roster already splits bush and pole beans **by crop slug** (green-beans-bush, pole-beans), so the
  bean fork PLA-10 lists is not a within-crop fork here.

---

## 2. Height and spread, and the `height_inches` vs `mature_height_ft` collision

### 2.1 What is on the record (121 certified)

| field | authored | null | notes |
| -- | -- | -- | -- |
| `mature_height_ft` `[lo, hi]` feet | **16** | 105 | all 16 woody; `field_additions` `plant_dimensions` record on each (16 records); decimals already in use (thyme `[0.5, 1]`) |
| `mature_spread_ft` `[lo, hi]` feet | **14** | 107 | apple and lemon are height-only, "spread not stated on the page" recorded |
| `footprint_inches` | **0** | 121 | PLA-429's slot, defined by the PLA-465 spec, authored by nobody; not a published datum (re-confirmed: no page read carries a trunk or crown width at the ground) |
| `rootstock_options[].mature_height_ft` | 54 of 60 rows | 6 | 19 grafted crops; all 60 rows carry both keys |
| `rootstock_options[].spread_ft` | 53 of 60 rows | 7 | the planner substitutes a picked rootstock's `spread_ft * 12` for spacing (app `rootstock.ts:44-57`) |
| any other spread field | none | | |

Armor already on these: A59 `plant_dimensions_gate` (shape, presence, and a coverage rule that lets a
woody certified crop be null only if cane fruit or a record names the field), `numeric_sanity` 120/80 ft on
tree bases and 20/20 elsewhere, register row 30. **Every one of the 18 tip-over crops named on PLA-10 is
herbaceous and null on all three keys** (re-confirmed on `edcd9bf9`; the 16 authored are all woody).

### 2.2 The collision, as a decision (D3 in section 7)

PLA-10 (Aug 6) ruled `height_inches: [min, max]` and `spread_inches: [min, max]`, "new, universal, crop
level". PLA-465 (Sep 16-18) landed `mature_height_ft` and `mature_spread_ft` on every certified crop's key
set, with a gate, provenance convention, sanity bounds and a register row, and Trevor's R1 explicitly
widened them to "define for all 121, author the woody; the herbaceous case has consumers beyond D3 (corn,
sunflower and staked tomatoes shade neighbours, a planner and PLA-534 concern)". Nothing anywhere reads
`height_inches`.

| option | what it means | cost | what it breaks |
| -- | -- | -- | -- |
| **A. Retire `height_inches`/`spread_inches` from PLA-10's shape; PLA-10 authors the HERBACEOUS heights into `mature_height_ft` / `mature_spread_ft`** | one height field, feet, decimals for herbs | authoring only (the field, gate, provenance and bounds exist; 16 precedents) | nothing; the D3 wind rule and the shading rule read feet; both consumers already format rootstock height in feet |
| B. Add `height_inches` beside `mature_height_ft` | two heights in two units | a second gate, register row, allowlist line; a rule that must pick one | every consumer has to reconcile them; a crop with both is a contradiction waiting to be authored |
| C. Rename roster-wide to inches | one field, inches | migrate 16 authored values + 16 provenance notes + A59 + `numeric_sanity` + the unmerged app allowlist branch | the PLA-465 landing records go stale on a unit; no consumer asked for inches |

**Recommend A.** The one genuine argument for inches is herb precision, and `[0.5, 1]` already carries it.
The spec should also write down the herbaceous meaning ("expected height at maturity in the ground, not
staked height of a vine", or the staked height for indeterminates, which is the D3 case) because that is
the sentence a source has to contain.

### 2.3 Three things called "footprint"

PLA-429's `footprint_inches` is the plant's body width at the ground (trunk, crown). PLA-534's "footprint"
is the ground AREA a plant consumes, which is what vertical growing reduces. `mature_spread_ft` is canopy.
The spec should name all three once so the vertical delta is defined against area (derived from
in-row x between-row, or from the layout entry), never against the PLA-429 slot, which stays null.

---

## 3. Which crops genuinely fork by method (measured, not the ~12-20 estimate)

Counted only where a **cited page in the cache or the crop's own prose states two different spacings for
two ways of growing the same crop**. Support-post spacings (bramble trellis posts 10 to 20 ft apart) are
build specs, not plant spacings, and are excluded.

| axis | crops | evidence (page read) |
| -- | -- | -- |
| **support: staked / caged / unstaked-sprawl** | cherry-tomato, beefsteak-tomato, roma-tomato, heirloom-tomato, grape-tomato, tomatillo (6) | Cornell tomato guide: "12 to 24 in determinate; 14 to 20 in staked indeterminate; 24 to 36 in unstaked indeterminate". ISU: staked 1.5-2 ft, caged 2-3 ft, sprawl 3-4 ft. UNL G1650: unstaked 3 ft in rows 4-5 ft; staked 18-24 in in rows 3 ft; caged 24-36 in in rows 4 ft. Illinois: dwarf 12, staked 15-24, trellised/ground 24-36. UMD: "18-36 in rows x 48-60 between rows ... depends on ... whether staked or caged". USU tomatillo: hills vs transplants 2 ft in rows 3 ft. |
| **support: trellised / ground** | cucumber, slicing-cucumber, pickling-cucumber, english-cucumber (4) | Clemson: "non-trellised ... 8 to 10 in apart in rows 5 ft apart. If trellised, four to five seeds per foot in rows 3 ft apart ... thin to 9 to 12 in". UMN: train to a 3-4 ft trellis "allowing you to space garden rows more closely". ACES greenhouse: single-leader cordon 12-18 in within row, rows 5 ft. UMD: 12 in x 48-72 in, or hills of 2-3. |
| **arrangement: hill / row** + **cultivar: bush / vining** | butternut, acorn, spaghetti (3), pumpkin (1), zucchini, yellow-summer-squash (2), watermelon, cantaloupe, honeydew (3) | NMSU CR457: squash "in hills 24-45 in apart in rows 36-60 in; four to five seeds per hill"; UMD summer squash: "Hills (2-3 plants) 3-4 ft in-row x 4-6 ft; single plants 2-3 ft x 3-5 ft"; UMN squash: hills 5-6 ft, bush types "only two to three feet between rows or hills"; ISU melons: hills 1.5-2 ft apart, rows 5-6 ft; UMN melons: groups 18-24 in, rows 5-6 ft, small-fruited types "to a fence or trellis" (NO trellis spacing stated); UGA watermelon: hills 8 ft on all sides. Own prose on all 6 winter cucurbits/melons: "closer for bush kinds". |
| **system: matted row / two-row bed** | strawberry (1) | own prose: matted rows 15-24 in x 36-48 in; ca_interior "12 in apart in two-row beds" |
| **arrangement: block rows / hills** | sweet-corn, field-corn, popcorn, flint-corn (4) | ISU: "8-12 in apart in rows 2.5-3 ft ... may also be planted in hills ... 4-5 seeds per hill ... hills 2.5 ft apart with 2.5-3 ft between" |

**Firm fork population: 24 crops** (20 without corn, whose hill form is an alternative sowing of the same
block). Three crops PLA-10 names do NOT fork on spacing in any cited page: **snow-peas, sugar-snap-peas,
sweet-pea** get a support requirement only (UMD "rows 18 to 24 in on center ... can be trellised";
Clemson "regardless of row type planted, space rows 2 feet apart"). Beans fork by slug, not within a
crop, except dry-bean's `half_runner` Pinto. Pole-beans carries one method (Illinois: rows 30-36 in OR
hills 30 in, both up a support).

**What this says about the August shape.** `method: row | hill | block | vertical` puts an arrangement
(row, hill, block), a support (vertical), and, via the bush-vs-vining spacing on cucurbits, a cultivar
habit into one enum. The sources fork on these independently (Illinois pole beans: rows OR hills, both
trellised; Cornell tomatoes: staked OR not, all in rows). Section 7 D2 lays out the options.

---

## 4. Consumers: every read of spacing today, and what an in-row redefinition changes

### 4.1 plant-astro (`main` `3f7d2d5`, submodule pin `3f58d7a` = canonical `83384c85`, two content revisions behind `cd0f9f17`)

| surface | file:line | reads | renders | null handling | in-row / between / both |
| -- | -- | -- | -- | -- | -- |
| Guide hero stat strip | `src/components/guides/HeroCard.astro:198-204, 317-322` | `spacing_inches` | "Spacing" `lo-hi"` (trees: `lo/12-hi/12 ft`), sub-label **"between plants"** / "between trees" | absent -> hidden; **`[]` is truthy -> would render `NaN-NaN ft` / `undefined-undefined"`** (latent; avocado/olive/mushrooms/microgreens only, none certified with a hero) | in-row |
| Care Guide "The specs" | `CareGuideCard.astro:59-74, 147-158` | `spacing_inches` | "Spacing" `lo-hi inches`, no qualifier | strict 2-finite guard, fail-closed | unstated |
| Planner catalog | `src/lib/planner/catalog.ts:126-151` | `spacing_inches` | placeable iff array, non-empty, not zone_independent; `[s0, s1 ?? s0]` | excluded silently ("N crops we have verified spacing ... for") | |
| Planner math | `src/lib/planner/fit.ts:4-7, 10-11, 53-64, 74-76, 166-177, 200-216` | same | area `(s/12)^2`; tight = lo (Seasoned), roomy = hi (Beginner); woody floored at 144 in; `rowPlantCount` in-row; **`rowWidthFt` between-row** | | **both axes** |
| Tree guide rootstock card | `src/lib/rootstock-presence.ts:97-117`, `RootstockCard.astro:47` | `rootstock_options[].mature_height_ft` | "Mature height" `lo–hi ft` | null -> line omitted (2026-09-22 ruling) | |
| Hero det/indet line | `HeroCard.astro:113-121, 245` | `det_indet.type` | "Indeterminate" | hidden | |
| App-preview mock | `src/lib/app-preview/demo.ts:566-575` | tomato only | "Spacing ... between plants" | | in-row |

Never read on plant-astro: `spacing_inches_anchoring_urls`, `planting_layout`, `thin_to_inches`,
`footprint_inches`, crop-level `mature_height_ft` / `mature_spread_ft`, `rootstock_options[].spread_ft`,
`pollination_block_min_rows`, `thinning`. The content collection declares `spacing_inches` as
`z.array(z.number()).optional()` and passes everything else through (`src/content.config.ts:34, 46, 107`).

### 4.2 plant-app (`feat/community-foundation` `6676406d`; export provenance `d7b33682`, four content revisions behind)

- **Export.** `scripts/export-projection.mjs` `SHIP_TOP_LEVEL` ships `spacing_inches` +
  `spacing_inches_anchoring_urls` (:71), `thin_to_inches` (:74), `planting_layout` (:64), `det_indet` (:46),
  `rootstock_options` whole (:68). `projectRoster` (:201-211) **throws on any unclassified top-level key**,
  so `row_spacing_inches` or a new `planting_layout` sibling needs an allowlist line before `build:guides`
  can run. **The PLA-465 line (`378c7b9f`, adds `footprint_inches`, `mature_height_ft`, `mature_spread_ft`)
  is on local branch `feat/pla-465-dimension-keys` only, not on `main` or HEAD**, so today's HEAD cannot
  build an export from any canonical since `a7f234ce`. The committed export (`assets/data/guides.dataset`,
  provenance `dataset-provenance.json`: `canonical_sha256 d7b33682`, `dataset_commit 824cd27`) carries 121
  `spacing_inches`, 41 `thin_to_inches`, 6 `planting_layout`, 0 of the three dimension keys.
- **Guide tiles and facts.** `at-a-glance.ts:145-158` "SPACING" `lo–hi in`; `guide-facts.ts:75-85`
  "Spacing"; `guide-chapters.ts:164` "Spacing ... to ... in apart"; `SeedlingDetailSheet.tsx:140` (truthy
  check only, same latent `[]` defect as astro); `crop-timing.ts:105` / `StartFromSeedCard.tsx:42-58`
  "Thin to ... apart". All unqualified or plant-to-plant.
- **Planner.** `catalog.ts:25, 105-116` (drops crops with no range); `fit.ts:11-13` tight = lo / roomy = hi,
  every caller roomy except the woody 144-in floor (:59-75); `rowPlantCount` (:177) in-row;
  **`rowWidthFt` (:181-205): the row's own `rowSpacingInches` wins, then legacy per-planting values, then
  the max `planningSpacingInches` across the row's crops, so `spacing_inches` is the between-row width
  whenever no decision exists**; `rootstock.ts:44-66` substitutes a picked rootstock's `spread_ft*12`;
  `solve-fit.ts:84-101` `PLANT_FOOTPRINT_FLOOR_INCHES = 6` with a doc comment that predates PLA-465;
  `plot-calc.ts:47-58, 73-88, 122-131` (row subject = widest crop; cached lookup inches; block advisory);
  `calculator-layout.ts:45-83, 153-157` and `types.ts:90-115` ("dataset has no row-spacing field yet").
- **Bed sheet and calculator copy.** `BedCropSheet.tsx:356-376` **"Plant spacing", "inches between plants
  (guide range lo-hi)"**, "Closer than the guide's {min} in minimum"; `CalcCropPane.tsx:546-576` **"Space to
  the next row"** stepper + **"Look it up"** action; `CalculatorPane.tsx:120-134, 177-195, 1457-1470,
  1793-1804` (no-room notice, deviation, `row_spacing_placeholder` event).
- **Herb.** `herb/slice.ts:14-15` FACT_KEYS include `spacing_inches` and `thin_to_inches` only (no
  `planting_layout`, `det_indet`, rootstock, height); `canned.ts:27-32` the "start" answer says "Space
  lo–hi in apart"; **`prompt.ts:200-209` "ROW SPACING IS NOT IN THE CERTIFIED DATASET YET ... corn is 9
  inches between plants and about 30 between rows ... look it up FIRST"**; `planner-tools.ts` `plan_rows`
  (:63-73, :812-842 given value -> shared cache -> unavailable -> plant-spacing placeholder -> REFUSE; :888-895
  "No verified row spacing for {crop}, so this uses its plant spacing as a placeholder."), `set_spacing`
  (:978-1000; **:999 compares a ROW spacing against `spacing_inches[0]`, the PLANT minimum, and warns
  "Closer than the guide's {min} in minimum"**, the PLA-423 blur in live code), `describe_plan` (:381-393).
- **Lookup scaffolding (PLA-426/427).** `src/lib/row-spacing.ts` (storage key `plant.rowSpacing.lookups`,
  extension-host allowlist, captions "No verified row spacing found. From the crops in this row." / "{X}
  from {host}."; header comment says it retires when PLA-426 lands) and `row-spacing-lookup.ts`
  (claude-haiku-4-5 + web_search, row-to-row inches only, `ROW_SPACING_LOOKUP_IS_PRO = false` unruled).

### 4.3 What redefining `spacing_inches` as in-row changes, per surface

- **Guide pages, both consumers: nothing.** They already say "between plants" or say nothing. The Care
  Guide spec row could gain the word "between plants" for free.
- **The 6 to 8 blended values (section 1.1) move**, and every stat card, tile, Herb canned answer and
  planner capacity on those crops moves with them: butternut hi 72 -> 36, acorn and spaghetti hi 48 -> 36,
  watermelon `[36,72]` -> its hill or in-row figure, blackberry and strawberry to one system's figure. That
  is a per-crop decision row in the spec, not a rule.
- **Both planners' `rowWidthFt` stop being fed an in-row number** once `row_spacing_inches` exists; until
  the consumer repoints, an in-row-only `spacing_inches` UNDERSTATES between-row width on every row crop
  (potato 12 in vs 30-36), which is the planner drawing more rows than fit. The area-per-plant `(s/12)^2`
  has the same direction. So the app repoint (PLA-426's stated retirement condition: lookup demotes to
  fallback, placeholder notice retires, Herb prompt line goes) and the astro `rowWidthFt` repoint are
  precondition-grade for the data flip, the same "frontend first" order PLA-7 used.
- **Herb** answers "in-row spacing" already; the fix is `set_spacing:999` and the prompt paragraph.
- **PLA-580's routed question** (is multi-plant pot capacity an area question?) gets its input: in-row
  spacing squared is a lower bound on per-plant area, so a pot-capacity rule built on `spacing_inches`
  alone over-fills the pot for row crops; the spec should say whether pots read in-row only.

---

## 5. Sources: which admitted catalog sources publish row, hill and vertical spacing (pages read from cache)

- **Technique-scoped sources: none admitted.** PLA-532 is Todo. A scan of all 220 `source_catalog` entries
  for container / vertical / trellis / stake / cage / HORT-189 / SPES-450 / 426-336 / "Extension Gardener
  Handbook ch. 16" finds zero technique-scoped ids (the only "container" hits are lavender's CSU sheet and
  the artichoke overwintering bulletin). NC State ch. 16 (the "much less ground ... yield per square foot"
  claim PLA-534 rests on) and VT HORT-189 are neither catalogued nor cached.
- **Cache coverage.** 1,368 distinct URLs are cited or catalogued; **1,193 are cached** (`tools/.doc_cache`,
  `sha1(url).txt`); 175 are UNCACHED and therefore UNDETERMINED here, not absent (PLA-161's rule).
- **Row spacing from pages the crops already cite** (regex over cached bodies, then the hits read):
  pages carrying a between-row statement are cited by **105 of 121** certified crops (upper bound; the
  count is inflated by general guides such as CTAHR B-91, whose regex hits include "rows 25 to 30 feet
  long"). The **16 without one** are the 8 microgreens (N/A) plus bee-balm, borage, calendula, cosmos,
  elderberry, lemongrass, mulberry, pawpaw, plum. The multi-crop tables that will do most of the work, each
  confirmed by reading the cached body:

| source id | page | what it carries |
| -- | -- | -- |
| `vce_426_331` | VCE 426-331 | Table 5 "Distance between plants in row / Distance between rows", plus the rule "Space plants closer together in the row when using wider spacing between rows"; cited by ~40 crops |
| `wsu_em051e` / `wsu_ext` | WSU EM051E | Table 4 "Distance Between Plants (inch) / Distance Between Rows (inch)" |
| `uf_ifas_vh021` (+ `ufifas_ext_vh021`, `uf_ifas`) | UF/IFAS VH021 | planting table "Spacing (Inches): Plants / Rows" |
| `nmsu_ext_cr457b` / `nmsu_ext` | NMSU CR457B | "Distance Between Plants in Rows (in.) / Distance Between Rows (in.)" |
| `uga_b577` / `uga_calendar` | UGA B577 chart | "Distance between rows / Distance between plants" |
| single-crop pages | UMD tomato ("18-36 in rows x 48-60 between rows ... whether staked or caged"), Clemson melons ("rows 6 to 8 feet apart ... in the rows 18 to 24 inches apart"), UMN cucumbers/squash/melons/peas, ISU corn/cucumbers/melons/tomatoes, Illinois snap beans, USU tomatillo, VCE 426-840 and UADA FSA-6107 for brambles | |

- **Hill spacing:** 14 cached pages state a hill spacing or plants-per-hill: NMSU CR457 (squash, melons),
  NMSU H240 (chile: "hills 12 inches apart, 4-6 seeds per hill"), UMD cucumbers and summer squash, ISU
  cucumbers / melons / sweet corn, UGA C1035 watermelon ("hills ... 8 ft on all sides"), Illinois snap
  beans (pole beans in hills 30 in), USU tomatillo, MSState P3616 (generic thinning), UMN raspberries and
  VCE 426-840 (canes per hill, a pruning count, not a spacing). Pages cited by **32 of 121** certified
  crops (upper bound).
- **Vertical-conditional spacing:** the tomato pages above (Cornell x2, ISU, UNL G1650, Illinois, MSState
  P3616, CTAHR B-91 and HGV-5), the bean pages (Illinois, CTAHR B-91 "bush ... 4 inches ... pole ... 12 to
  18", HGV-8 "pole beans 6-12 in on both sides of a trellis, 36-40 in between rows", NMSU, UF pole beans
  "3-5 in, rows at least 36 in"), Clemson cucumber and ACES greenhouse cucumber. **No cited page gives a
  trellised spacing for melons, squash or peas**; UMN melons says only "training the plant to a fence or
  trellis". The bramble pages give trellis POST spacing (UGA C766 / VCE 426-840 / az1585: posts 10-20 ft,
  wires at 3 and 5 ft), which is PLA-534's "support specification" question, not a plant spacing.
- **What this means for sizing:** the row and hill columns can be authored from the existing catalog on
  roughly 100 crops without a new admission. The vertical arc's central claim (area delta, water, shading)
  and every trellis-spacing number for cucumbers-beyond-Clemson, melons and squash need PLA-532's
  admissions, and the technique pages must be read from raw bytes first (the 2026-07-30 / 08-03 standard).

---

## 6. Armor: what must land before this arc's first promote, and what each would catch

### 6.1 PLA-607 (identity ratchet over every sourced block; Backlog, not built)

- **What it would catch on this arc:** a NEW `planting_layout[]` entry, a new `row_spacing_inches`, or a
  herbaceous `mature_height_ft` landing with `sources` `[]` / `null` / absent while carrying a value, on a
  certified crop, by (crop, path) identity, so substitution cannot hide it. That is exactly the shape of
  this arc's blocks: every layout entry carries its own numbers and its own citation.
- **What it would NOT catch as specified:** `spacing_inches` today. The field has an `_anchoring_urls`
  sibling and **no `_sources` sibling on any crop**, so §F never walks it and a PLA-607 built over "every
  block type that carries a `sources` slot" would not see it either. If PLA-10 keeps `spacing_inches` as a
  bare pair with an anchoring dict, the redefinition and the 6 to 8 repaired values ship with no coverage
  floor unless this arc adds one. Cheapest fix: give the layout entry (or a `spacing` block) a `sources`
  list so the existing §F pair check and PLA-607 both apply, and treat the crop-level `spacing_inches` as a
  denormalized read of the default entry that a coherence rule checks.
- **Recommendation:** PLA-607's own note says "must land BEFORE the next arc that authors cited blocks",
  and this arc will author more cited blocks than anything since the IPM ladder. Land it before the first
  PLA-10 promote. It does not block the spec, the source reads or the consumer repoints, and its armed
  population should be measured on the canonical current at that time (the PLA-533 subtractive pass has
  already shrunk it).

### 6.2 A homepage-anchor gate (PLA-544 comment, 2026-09-25; Backlog, not scoped)

- **What it would catch:** a layout or row-spacing anchor whose URL is a bare host and the node's only
  citation. Measured today: `spacing_inches_anchoring_urls` carries **0** bare-host URLs across the 11
  anchored crops, and every row/hill/vertical page identified in section 5 is a pathed document.
- **Recommendation:** not a precondition. Put the one predicate (an anchoring URL must have a path when it
  is the sole citation) inside this arc's own gate, mutation-tested both ways, and let PLA-544's
  roster-wide gate land on its own schedule; a roster gate armed before this arc's data would flood the
  parallel session (the `parallel-session-gates-arm-off-the-data` lesson).

### 6.3 What already exists and what this arc must change or add

- **A44** `planting_layout_gate` rejects anything but a string in `{block, row, hill, grid, single}` and
  couples `block` to `pollination_block_min_rows`; the list shape needs a rewrite (enum per entry, exactly
  one `default: true`, per-method required keys, `block` keeps the min-rows coupling) and a coverage floor
  in the A57/A59 pattern (entry count >= 1 on every certified non-microgreen crop; every entry cites).
- **`numeric_sanity`** needs bounds for `row_spacing_inches` / `hill_spacing_inches` /
  `support_spacing_inches` and an ordering rule (between-row >= in-row on a row entry; `footprint_inches`,
  if ever authored, < `spacing_inches[0]`, already stated in the PLA-465 spec).
- **`display_readiness_gate`** demands a 2-positive pair on `spacing_inches` for placeability; keep it.
- **`register_coverage_gate` / A39** will make the new fields hard cert requirements once the register row
  lands; the 7 shells stay byte-identical (A39 exempts them); microgreens need the same `[]` N/A predicate
  `spacing_inches` already has.
- **plant-app export allowlist** throws on a new top-level key: the allowlist line must be on the app's
  default branch before the data lands (E1 is a waiver keyed on identity + failure character, not a bypass,
  `tools/precommit_release_verify.py` `EXPORT_WAIVERS`). The PLA-465 line is still unmerged, which is a
  prerequisite for this arc's line too.
- **SHA-pinned tests** (`test_problem_id_collision_gate` `PINNED_SHA`, `bare_host_scan`'s population, and
  the inventory PLA-544's comment asks for) re-measure in the promote's Task 8, on the landed bytes.
- **The two latent `[]` render defects** (astro `HeroCard.astro:198`, app `SeedlingDetailSheet.tsx:140`,
  truthy checks on an array) are worth a consumer ticket before microgreens or a shell ever gets a hero.

---

## 7. Decisions needed (each with a recommendation and what it rests on)

| # | decision | recommendation | rests on |
| -- | -- | -- | -- |
| **D1** | `spacing_inches` = in-row, and what to do with the blended values | Keep the August redefinition. In the same promote, repair the 6 to 8 blended pairs (butternut, acorn, spaghetti, watermelon, blackberry, strawberry; review fava and cayenne) to the in-row figure their own prose and cited page state, moving the row half into the new row field. Each is a decision row with the page sentence quoted. | Section 1.1 table; consumers already label it between plants; the 07-01 review notes record the blend as deliberate |
| **D2** | The layout shape: the August single `method` enum, or separate axes | Keep list-with-default, but split the axes: `arrangement: row \| hill \| block`, `support: none \| stake \| cage \| trellis` (PLA-534's `vertical` is a support value, not an arrangement), with the spacing keys following the arrangement (`row`: `spacing_inches` in-row + `row_spacing_inches`; `hill`: `hill_spacing_inches` + `plants_per_hill`; `block`: `pollination_block_min_rows`), and the cultivar axis staying on `varieties[].plant_habit` (already there on dry-bean). One `default: true` per crop; beginner surfaces read the default. | Section 3: Illinois pole beans fork on arrangement AND support at once; Cornell/UNL tomatoes fork on support in rows; cucurbits fork on arrangement and cultivar; peas need support with no spacing fork |
| **D3** | `height_inches` vs `mature_height_ft` | Option A: retire the inch fields from PLA-10's shape; author herbaceous heights into `mature_height_ft` / `mature_spread_ft` in feet with decimals; write the herbaceous meaning (in-ground mature height; for indeterminates, the supported height) into the spec so the D3 wind rule and the shading rule read one field | Section 2.2; 16 precedents, A59, register row 30, `numeric_sanity` 20 ft; nothing reads `height_inches`; the app's allowlist line already names the ft keys |
| **D4** | Spread and footprint | `mature_spread_ft` is the spread field (retire `spread_inches`); `footprint_inches` stays null roster-wide (still not a published datum); PLA-534's "footprint" is defined as area derived from the default entry, never a field | Section 2.3 |
| **D5** | Multi-entry authoring scope | The measured 24 (tomatoes 6, cucumbers 4, winter cucurbits + pumpkin 4, summer squash 2, melons 3, strawberry 1, corn 4); peas 3 get `support: trellis` on their single entry; everything else one entry. Not the ~12-20 estimate. | Section 3 |
| **D6** | Hill and block in this pass | Yes, as ruled. Hill: 14 pages already cached, 10 crops' prose already says "per hill". Block: the 4 corn crops already carry `block` + min rows; no other wind-pollinated crop is in the roster, so "a few others" is zero on this roster. | Sections 1.2, 5 |
| **D7** | Sources: run PLA-532 first? | Split. Row and hill columns author from the existing catalog now (105/121 upper bound, the five multi-crop tables named). PLA-532 is a precondition only for the vertical claims and for trellis spacings on melons, squash and peas; run it in parallel, from raw bytes. | Section 5 |
| **D8** | Armor ordering | PLA-607 lands before the first PLA-10 promote (its own note, and this arc's block shape). The homepage rule folds into this arc's gate. A44 rewrite + coverage floor + `numeric_sanity` bounds ship with the promote, mutation-tested per PLA-215. Give the layout entries a `sources` slot so §F and PLA-607 see them. | Section 6 |
| **D9** | Consumer order | Frontend first, as PLA-7: (1) merge the PLA-465 allowlist line and add this arc's; (2) app `rowWidthFt` / `plan_rows` / `set_spacing:999` / prompt paragraph repoint, lookup demotes (PLA-426's retirement condition); (3) astro `rowWidthFt` and the Care Guide qualifier; (4) data flip; (5) submodule bump (astro session's call). | Section 4.3 |
| **D10** | Row spacing on tree and woody crops | Presence-or-null. Author it on the row-planted woody crops with a cited row figure (raspberry, blackberry, blueberry, strawberry, elderberry hedge); null with reason on orchard trees, where a home grower plants one to three and the planner already floors them at 144 in. | PLA-426 "honest absence"; section 5 bramble pages |
| **D11** | Herbaceous height authoring scope | Not measured this session: which herbaceous crops' cited pages state a height. Measure at spec time; the 18 tip-over crops + corn, sunflower, the 6 tomatoes and the vining cucurbits are the consumers named so far. | PLA-10 comment 2026-09-21; PLA-465 R1 |
| **D12** | Is pot capacity an area question (routed from PLA-580)? | Answer in the spec: pots read the default entry's in-row spacing as a lower bound on per-plant area and `plants_per_pot` as the sourced anchor; no new field. | Section 4.3 last bullet |

---

## 8. Suggested sequence and size

1. **Rulings on D1-D12** (this document + the PLA-10 summary).
2. **Field-shape spec** (one session): the entry schema, the three axes, the coherence rules, the per-crop
   decision rows for the blended values, the herbaceous height meaning, the register row, the A44 rewrite
   and floor, the `numeric_sanity` bounds, the consumer render contract. Reads PLA-426's four requirements
   as acceptance criteria (range not scalar; method axis explicit; distinct from plant spacing at the
   schema level; presence-or-null).
3. **Consumer sessions** (app allowlist + planner repoint; astro planner + Care Guide qualifier), before
   any data flip.
4. **PLA-607** lands (its own ticket).
5. **Promote 1, row + hill + block on the certified roster** (~105 crops from the existing catalog, fan
   out to subagents by archetype, independent source-truth review pass), suite + harness by convention.
6. **PLA-532 admissions** (parallel with 5), then **promote 2, support entries** on the 24 fork crops and
   the 3 peas, and the herbaceous heights.
7. **PLA-534** opens on its own kickoff against the landed baseline.

---

## 9. Not measured here, and other caveats

- Every prose and cache population is regex-derived and reported as an upper bound; the firm numbers are
  the 18-crop pair table, the 6-crop planting_layout census, the field counts, and the pages quoted.
- 175 cited URLs are not in the local cache; their content is UNDETERMINED, not absent.
- PLA-532's candidate pages were not fetched; nothing here asserts what they say beyond PLA-532's own text.
- Which herbaceous crops' cited pages state a mature height was not measured (D11).
- The 18 tip-over crops are taken from the PLA-10 comment of 2026-09-21 (measured then on `1721208e`);
  only their dimension nulls were re-confirmed here.
- The plant-app sweep was on `feat/community-foundation`; the PLA-465 allowlist branch was inspected by
  `git branch --contains`, not checked out.
- The staged `cd0f9f17` was used only for the cross-check in the header; every pin above is `edcd9bf9`.
