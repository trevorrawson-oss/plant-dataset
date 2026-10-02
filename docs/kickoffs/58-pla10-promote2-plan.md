# 58 - PLA-10 promote 2: the plan (support entries, apple overrides, finding corrections, heights)

**Written:** 2026-10-02, PLA-10 promote 2 session 1. **READ-ONLY on canonical:** `cf1d480d` (== `LATEST.txt`), no
crop record edited, nothing staged. **Checkout:** `main`, session start HEAD `bc71f34` == origin/main; this session's
tools commit `78d734b` (local). **Consumers read:** plant-app `feat/community-foundation` `f6fa8c8b` and its origin tip
`1c464e2d` (identical in every file that matters here except a row-gap flag in `planner/fit.ts` / `layout.ts`);
plant-astro `main` `54a8249` (submodule at `bc71f34`).

**Measurement records** (read-only lanes, every quote checked against cached bytes; they are measurements, not
citations, and the promote re-reads every page from hashed bytes): `58-pla10-promote2-measurements/`
- `A_support_tomatoes_cucumbers.md`: the 10 support-fork crops, per-entry quotes and cache files.
- `B_peas_cucurbits_strawberry.md`: the 3 peas, the 9 melons and squash against UMN's rule, the strawberry bed.
- `C_tipover_heights_pla465_backfill.md`: the 11 tip-over closed ranges re-read, PLA-465's 16 backfill records.
- `D_heights_remaining.md` + `.tsv`: the other 84 null-height crops, classed, one TSV row per quote.
- `E_consumer_preconditions.md`: what promote 2's keys do to plant-app and plant-astro, file:line.
- `finding_corrections.tsv`: every open finding that still states a spacing figure promote 1 moved.

**Rulings in force, not reopened:** D1-D12, R1-R5, W1-W6, the 2026-10-01 promote-1 rulings, PLA-532's admissions.

**RULED (Trevor, 2026-10-02), folded into §1-§3 below as TAKEN.** SPLIT TAKEN: promote 2 = apple overrides + 24
corrections + support entries; promote 3 = heights (46) + the 16-crop backfill; promote 3 may stage while promote 2 is
in review and lands after. T1-T2 in promote 2 session 2; T3-T5 in promote 3 session 1. Not reopened, recorded: roma's
PSU/ISU `row-none` disagreement. The tomatillo `det_indet` copy defect is PLA-652, linked to PLA-10, not this promote.

---

## 0. What landed this session

`78d734b` tooling(pla10): `tools/promote_pla10_promote2.py` (base `cf1d480d`) with owed items 1 and 2 only:
- **(R)** a `rootstock_options[]` row may gain `spacing_inches` (`[lo, hi]` or null) and, only while that is non-null,
  one appended source + its anchor. apple only (R1). Every override quoted from hashed bytes. A bare-host
  `add_source` refuses (A63 passes a co-cited bare anchor, and the row's `umd_ext` states no spacing).
- **(F)** a named open finding's `summary` may gain exactly one appended `[CORRECTION <date>: ... -- see <ref>.]`;
  nothing else under `verification_status` is writable.
- Suite 66 passed (RED first: 61 failed); harness 52/52 caught; affected set rc 0 (72 passed, 2/2 scripts).

**Support entries and heights need a further tools commit** (section 8): the promote cannot yet add a layout entry,
move a default, author a height, or append the A59 `field_additions` record.

---

## 1. First rows: apple's overrides and the finding corrections

### 1.1 apple `rootstock_options[].spacing_inches` (owed item 1)

NCSU Extension Gardener Handbook ch. 15, Table 15-4 (nonspur, feet), already cited by apple as
`ncsu_ext_handbook_tree_fruit`, hashed `0e16d13e...`. Added to each non-null row as its second source. Quotes are
the full table row, as promote 1 quoted M26.

| row | override | quote (table row) |
| -- | -- | -- |
| M9 | `[48, 96]` | `M.9** 4 – 8 3 – 5 6 – 11` |
| M26 | `null` (the crop basis `[96, 144]`) | none: the recommended row; crop-level figure already cited |
| MM106 | `[144, 192]` | `MM.106 12 – 16 8 – 11 17 – 22` |
| MM111 | `[168, 216]` | `MM.111 14 – 18 9 – 12 20 – 25` |
| seedling | `[216, 300]` | `Seedling* 18 – 25 12 – 16 25 – 35` |

All four pass the promote's evidence check against the real bytes today (suite control).

### 1.2 The finding corrections (owed item 2, widened by measurement)

The handoff named seven `*_pilot_spacing_*` findings. **Re-measured against every crop promote 1 moved (67 crops): 24
findings on 24 crops still state a spacing figure that is no longer true** (13 `open`, 11 `accepted`). List with
context: `finding_corrections.tsv`.

| group | findings |
| -- | -- |
| The seven named | acorn, spaghetti, butternut, watermelon, pumpkin, honeydew: each states its old `spacing_inches`. **cantaloupe: its figure did NOT move** (`[24,36]` still true); what is retired is the mechanism ("between-row ... carried in prose rather than the numeric field"), now false since `row_spacing_inches` `[60,90]` exists. Still a correction (Class 2, retired mechanism). |
| fava (the 8th) | `broad_beans_fava_pilot_finding_001`: "spacing_inches [4,8]", now `[8,10]` |
| 16 more | slicing-cucumber 004 `[12,24]`, pickling-cucumber 005 `[8,18]`, habanero 006 `[18,24]`, arugula babyleaf `[1,3]`, sweet-potato 004 `[12,18]`, cilantro `[2,4]`, chives `[8,12]`, mint 005 `[12,24]`, dill `[8,12]` (summary AND basis), rosemary 004 "24-36 in", mandarin-clementine 004 `[120,216]`, shallot "6 to 8 inches", cosmos 003 `[12,18]`, sweet-alyssum 008 `[4,8]`, bee-balm `[18,24]`, sweet-pea 004 "3 to 6 in" |

Also checked: `thin_to_inches` (moved on 16 crops) adds no finding beyond those above. 8 findings on crops whose
spacing did NOT move name `spacing_inches` with the still-true value; no correction.

**Decision rows**

| # | question | recommendation | why |
| -- | -- | -- | -- |
| C1 | Correct all 24, or only the seven + fava? | **TAKEN (Trevor, 2026-10-02).** **All 24.** | Your rule: a finding still stating an old number is a correction, whatever its subject. The allowance is per finding id, so the count costs nothing in tools. |
| C2 | dill's `basis` also states "8 to 12 inch spacing". Widen the allowance to `basis`? | **TAKEN: one summary correction naming the basis figure; no basis allowance.** **No. One correction on `summary` that names the basis figure too** ("the summary's [8,12] and the basis's 8 to 12 inch spacing are now [9,9]"). | Keeps the allowance at one field; the convention puts the correction in the record's string, and the finding is one record. |
| C3 | cantaloupe's correction is mechanism-only. | **TAKEN: mechanism-only.** **Correct it** (Class 2 in `docs/verification_log_ref_convention.md`). | The figure is true; the claim that rows live only in prose is not. |
| C4 | Correction text | **TAKEN.** One line per finding: `[CORRECTION 2026-10-0x: spacing_inches is <new> since PLA-10 promote 1 (<old> was <blend / modeled range>); <rows now in row_spacing_inches, where true> -- see PLA-10 promote 1, d021116.]` | The convention's format; the promote checks it. |

---

## 2. Support entries (what PLA-534 needs)

**Measured: the cached pages back 13 support entries on 10 crops, not 16.** Every promote-1 `row-none` entry stays,
with its id. PLA-532's two technique pages give **no number** for tomatoes or cucumbers: `vce_hort_189` gives only
build specs, and `umn_ext_trellises_cages` only "the same spacing ... as if they were going to grow on the ground".
The figures come from the crops' own cited pages. Every source below is **already hashed** in `tools/.evidence_cache`
(ISU tomato, PSU heat-stress, Clemson cucumber); the kickoff-55 fork pages (UNL G1650, Cornell, Illinois, UMD tomato,
OSU EC1333) are `.doc_cache` text only and would need fetching to be cited.

| crop | new entries (in-row / rows), source | recommended default | hero tile |
| -- | -- | -- | -- |
| cherry-tomato, grape-tomato | `row-stake` [18,24] / [60,72] (PSU "for staked culture"); `row-cage` [24,36] / rows see S3 (ISU "if grown in wire cages, space plants 2-3 feet apart") | **`row-cage`** (S1) | **unchanged** [24,36] under cage; **moves to [18,24]** under stake |
| heirloom-tomato | same two | `row-cage` | unchanged under cage |
| beefsteak-tomato | `row-stake` [18,24] (ISU; beefsteak does not cite PSU); `row-cage` [24,36] (ISU) | `row-cage` | **moves [36,48] -> [24,36]** (either way) |
| roma-tomato (determinate) | `row-cage` [24,36] (ISU) only | `row-none` stays | unchanged [18,24] |
| tomatillo | **none** (S4) | `row-none` | unchanged |
| slicing-cucumber, pickling-cucumber, cucumber | `row-trellis` [9,12] / [36,36] (Clemson "if cucumbers are trellised ... rows spaced 3 feet apart ... thin so they are 9 to 12 inches apart") | `row-none` stays | unchanged |
| english-cucumber | `row-trellis` [9,12] / [36,36] (Clemson, which names "burpless or european-type") | **`row-trellis`** (S5) | **moves [12,18] -> [9,12]**; row mirror [48,72] -> [36,36] |

**Decision rows**

| # | question | recommendation | why |
| -- | -- | -- | -- |
| S1 | Indeterminate tomato default: stake or cage? (The kickoff assumed **cherry-tomato's staked default moves the hero tile**: it does, [24,36] -> [18,24].) | **TAKEN, CONDITIONAL ON S3: cage default on cherry, grape, heirloom, beefsteak only if a cage row figure is citable. If not, `row-none` stays default and the support entries go in non-default; a planner regression is not an acceptable price for a default change.** **Cage.** | Every tomato's own prose says it needs staking or caging, so `row-none` default contradicts it; staked spacing assumes pruning to 1-3 stems (UMD, OSU EC1333), cages need none, and the beginner register is the default reader. Cage leaves cherry/grape/heirloom heroes where they are; stake moves all four to [18,24]. |
| S2 | cherry-tomato's current `row-none` [24,36] is PSU's "indeterminate tomatoes **without stakes**", not "the caged figure" spec §1.4 calls it. | **TAKEN: appended to spec §1.4.** **Record it (spec §1.4 correction).** No value change: it is the right figure for `row-none`. | The page says unstaked. |
| S3 | Rows on the cage entries: ISU's "rows should be spaced 4-5 feet apart" follows its sprawl sentence; applying it to cages is a reading. UNL's explicit cage row [48,48] is doc-cache only. | **TAKEN: fetch UNL G1650 into the evidence cache, cite it for cage rows [48,48]. ISU's 4-5 ft sentence is NOT applied to cages.** **Fetch UNL G1650 into the evidence cache and cite it for cage rows [48,48]**; else `not_authored`. | A figure on a page beats a reading. Note it moves cherry/grape's crop-root row mirror [60,72] -> [48,48] if cage is the default. **If no cage row figure is citable, S1 = cage would make the crop-root row mirror null (`not_authored`) on cherry, grape, heirloom and beefsteak, which all carry a row figure today: a planner regression. In that case keep `row-none` the default and add the support entries non-default.** |
| S4 | tomatillo: two entries (`row-stake`, `row-cage`, both [24,24]) from UCANR Alameda's single "space plants about two feet apart and provide support such as a cage or stake", or none? | **TAKEN: none.** **None.** | One figure duplicated across two ids is not a fork. USU's tomatillo fork is hill vs row, outside promote 2. |
| S5 | english-cucumber default `row-trellis`? | **TAKEN; the hero [12,18] -> [9,12] and row mirror [48,72] -> [36,36] moves are the decision row.** **Yes.** | Its own text: "train the plants up a string or trellis to keep the long fruit straight". |
| S6 | Staked row spacing conflict: PSU "a minimum of 5-6 feet" vs UNL "rows 3 feet apart". | **TAKEN.** **PSU** for `row-stake` (hashed, already cited by cherry/grape). | Cited and hashed; UNL is doc-cache only. |
| S7 | roma `row-stake`? Hashed staked figures are explicitly indeterminate. | **TAKEN.** **No stake entry on roma.** | Scope: roma is determinate; its own text says "a sturdy cage instead of a tall stake". |

**Flags (page disagrees with the spec or the record):**
- roma's `row-none` (ISU [18,24] / [48,48]) disagrees with PSU's explicit "24 inches ... 4-5 feet between rows for
  determinate tomatoes without stakes". Recorded; not reopened in promote 2 unless you say so.
- heirloom's `row-none` (Missouri "24 to 36 inches") names no support method.
- Illinois "trellised **or** ground bed plants 24 to 36" is one figure, not a fork; ACES's 5 ft row figure belongs
  to its double-row system, not the single cordon (kickoff 55 misquoted both).
- **Data defect, surfaced not fixed:** tomatillo's `det_indet.detail_beginner` is a verbatim copy of cherry-tomato's
  ("cherry tomato varieties", Tumbling Tom); `detail_seasoned` opens "Cherry tomatoes are almost always
  indeterminate". Needs its own ticket.

### 2.1 Peas

| crop | decision | deciding sentence |
| -- | -- | -- |
| snow-peas | **`row-none` stays (support optional)** | UMD: "plants grown together will hold each other up or can be trellised to make harvesting easier" |
| sugar-snap-peas | **`row-none` stays** | USU (its spacing source): "most pea varieties are self-supporting during growth"; "snap and snow peas climb naturally so little additional work is required other than constructing the supports" (a harvest/yield benefit, not a requirement) |
| sweet-pea | **`row-none` stays; NO trellis entry (P2, ruled)** | **Contradicts the spec's "support required" expectation:** OSU (its spacing source) "bush or dwarf types ... make colorful hedges"; NCSU, UC IPM and its own description agree. Only Cornell's high-tunnel cut-flower page says "plants must be provided with a trellis" |

So **no pea entry is replaced**; the PLA-629 ordering constraint (spec §10.2) does not bind.

| # | question | recommendation |
| -- | -- | -- |
| P1 | Optional `row-trellis` on snow / sugar-snap? Extending UMN's same-spacing rule to peas is an inference (PLA-532 says so); Clemson garden-peas (doc-cache only) gives 1-2 in and "space rows 2 feet apart" regardless of row type. | **TAKEN: none.** **None this promote.** The only figure carries a row number that conflicts with the trellis-rows-null ruling, and the same-spacing route is an inference. |
| P2 | sweet-pea `row-trellis` from Cornell "2 to 4 plants per foot on a trellis, with rows 4 to 6 ft. apart": rows [48,72] are stated; in-row [3,6] is **arithmetic** (12 / 4 to 12 / 2), not a stated figure. | **RULED: NO sweet-pea trellis entry.** A row entry requires `in_row_inches` and the only candidate is arithmetic the quote check would false-pass; rows alone do not make an entry. Cornell's rows [48,72] are recorded in the decision row for a future promote. Spec §10.2's "support required" gets an appended correction. **Rows [48,72]; in-row by ruling.** `quote_states` would wrongly pass [3,6] off the "6" in "4 to 6 ft" (a false pass the check cannot see): the in-row needs a hand check and a decision row, or the entry waits. Scope is commercial high tunnel. **Alternative: no sweet-pea trellis entry.** |

Oddity, not acted on: UMN growing-peas (doc-cache only) says seeds "six to seven inches apart"; every other page and
canonical say 1-3 in.

### 2.2 Melons and squash (UMN: "same spacing as on the ground", fruit up to ~3 lb)

UMN gives no trellised row spacing: every trellis entry is `row_spacing_inches: null`, `not_authored`, cites the
crop's ground page + `umn_ext_trellises_cages`, no height override.

| crop | entry | basis |
| -- | -- | -- |
| acorn-squash | **`row-trellis` [24,36]** | Quoted by name on its own UMN page: "you can train small-fruited squash like delicata or acorn to a trellis" |
| cantaloupe | `row-trellis` [24,36] **by ruling (M1)** | USU: "cantaloupe plants can be trained to a fence or trellis"; ISU cultivar weights mostly 4-9 lb, only 'sarah's choice' 3 lb, 'sugar cube' 2 lb. Cultivar is not an entry axis (§1.1). |
| honeydew-melon | **none (M2)** | No cached page gives a crop-level fruit weight (only 'snow leopard' 2 lb) |
| watermelon | none | USU icebox 10-15 lb, large 15-25 lb |
| pumpkin | none | UMN: "larger squash and pumpkins are too heavy to trellis" |
| butternut, spaghetti | none | UMN names only delicata and acorn; no cached weight |
| zucchini, yellow-summer-squash | none | UMD: "summer squash grows on non-vining bushes" |

| # | question | recommendation |
| -- | -- | -- |
| M1 | cantaloupe trellis entry, given most cultivars exceed 3 lb? | **TAKEN: USU's sentence is the citation; UMN's sling/weight condition is stated in the decision row.** **Yes, with the cultivar condition in the decision row.** USU names cantaloupe on a trellis directly; UMN's slings cover the weight. |
| M2 | honeydew? | **TAKEN: none.** (acorn by name: TAKEN; the rest none.) **No.** Qualifying it is an inference. |

Flag: UMD melons says "growing plants on a trellis allows **closer** spacing" (no figure), against UMN's same-spacing
rule. VCE HORT-189 points melons and squash to **cages**, with no spacing, so D7 blocks a cage entry.

### 2.3 Strawberry `row-none-bed`

UC IPM "Cultural Tips for Growing Strawberry" (`uc_ipm`; cached as text, and as the cited PDF 281247.pdf): "space
plants about 12 inches apart in each row with rows about 12 inches apart in two-row beds"; beds "18 inches wide if
you are planting two rows". Entry: `row-none-bed`, `rows_per_bed: 2`, in-row [12,12].

| # | question | recommendation |
| -- | -- | -- |
| B1 | The spec never says what `row_spacing_inches` means on a bed entry. The page's 12 in is between the two rows *in* the bed; no home page gives a between-bed figure (UC's 52-56 in beds are a commercial cost study). | **TAKEN; appended to spec §1.1.** **Rows within the bed: [12,12], and write that meaning into spec §1.1** (`rows_per_bed` present => `row_spacing_inches` is the in-bed row gap). The entry is non-default, so no planner reads it. |
| B2 | Spec frames it as `ca_interior`; UC IPM is statewide California home-garden, and the entry is crop-level. | **TAKEN. Confirm the UC IPM PDF is hashed before staging; fetch it if not.** **Crop-level entry, California scope stated in the decision row.** |

Evidence note: the UC IPM HTML is doc-cache only; confirm the cited PDF is hashed or fetch it.

### 2.4 Height overrides on support entries: **0**

No cached page gives a plant height *caused by* a support form. Trellis, stake and cage heights are not plant heights
(§4.5). OSU EC1333's "indeterminate plants ... can easily grow 7 to 8 feet high. for these, it is best to stake"
describes indeterminate habit, not the stake (doc-cache only): **not an override**. Pea and sweet-pea climbing
heights are open bounds ("up to five feet", "over 5 ft", "up to 8 feet").

Consumer note (E): no consumer reads an entry height except Herb's slice, which passes all entries to the model.

---

## 3. Heights

### 3.1 The 11 tip-over crops (closed ranges)

All 11 are certified, null today, and cite the page; the quote is in the cached text.

| crop | `mature_height_ft` | `mature_spread_ft` | page / quote |
| -- | -- | -- | -- |
| bell-pepper, jalapeno, banana-pepper, cayenne-pepper, habanero | [3,4] | null | UMD growing peppers: "can reach 3-4 ft. in height" |
| broccoli | [47/12, 47/12] | [20/12, 20/12] | NC State: "about 47 inches tall and 20 inches wide" |
| brussels-sprouts | [2,4] | [2,4] | NC State Toolbox: "2-4 feet tall and wide" |
| broad-beans-fava | [2,6] | null | NC State Toolbox: "grows 2-6 feet tall" |
| dill | [1.5,4] | null | UW-Madison: "18 inches to 4 feet tall" |
| eggplant | [2,4] | null | NC State Toolbox: "2 to 4 feet tall" |
| cosmos | [3,6] (H1) | null | UF/IFAS "3-6 feet"; NC State "up to 4 feet" (no lower bound) |

| # | question | recommendation |
| -- | -- | -- |
| H1 | cosmos: UF/IFAS [3,6] vs NC State "up to 4 feet"? | **TAKEN (promote 3).** **UF/IFAS [3,6]**: the only closed range; the crop's own description says 3 to 6 ft. |
| H2 | Scope: the UMD page names cayenne and habanero in its hot-variety list; it calls pungent types "mostly" *C. annuum*. habanero is *C. chinense*, which the page never names. | **TAKEN: cayenne and habanero in scope, reviewer confirms (promote 3).** **cayenne in scope; habanero in scope by name** (the page lists it and gives its ripening time). Reviewer confirms. |
| H3 | dill's prose says 3 to 5 ft in four places, above UW's 4 ft. | **TAKEN: corrected in the heights promote.** **The 5 ft high end is uncited: a prose correction rides the heights promote** (restatement adjudication, the promote-1 pattern). |
| H4 | broccoli's point from inches: store `47/12` exactly or rounded? | **TAKEN: store the quotient to 4 places and add `quote_states_ft` with a stated tolerance (T4); never store a rounded value the check cannot match.** (Superseded recommendation follows.) **Round to whole inches over 12 is what both consumers render; store the quotient to 4 places and fix the quote check (section 8, T4)**, or store exactly. Measured: a rounded 3.9167 FAILS `quote_states`; only the unrounded quotient passes. |

### 3.2 The rest: 84 null-height crops, classed (`D_heights_remaining.md`)

Population confirmed: 105 null - 8 microgreens = 97 (spec's figure); minus the 13 above (11 tip-over + 2 peas) = 84
(72 herbaceous, 12 woody; the woody keep their PLA-465 rulings).

| class | herbaceous | woody |
| -- | -- | -- |
| STATES-CLOSED | **35** | 1 (apricot, not reopened) |
| CONDITIONAL (authors null) | 7 | 7 |
| SCOPE-DOUBT | 7 | 2 |
| NONE | 23 | 2 |

**Closed (35):** 5 tomatoes, tomatillo, kale, spinach, green-beans-bush, edamame, potato, sweet-potato, onion, okra,
celery, artichoke, asparagus, leek; basil, cilantro, chives, mint, lemongrass; marigold, nasturtium, sunflower,
borage, calendula, zinnia, chamomile, sweet-alyssum, echinacea, bee-balm, viola, sweet-pea.
- **7 are habit-spanning** (5 tomatoes, nasturtium, sweet-pea: det/indet or climbing/bush in one range). Strict
  clean count: **28**. Tomatoes: NCSU "1 to 10 feet tall and 1 to 4 feet wide" vs Cornell "height: 2 to 6 feet".
- **Pages disagree on 21 of the 36** (onion NCSU 1-1.5 vs Cornell 1-3; echinacea NCSU 3-4 / PSU 24-36 in / UF 1-3;
  NCSU sunflower contradicts itself). Each needs a decision row, as promote 1's W2 range rule did for spacing.
- viola's pages are all pansy; mint's main page is spearmint (scope rows).

**Corrections to spec §4.4 (append, never rewrite):** okra is NOT "no": UF Gardening Solutions (cited, cached)
"most fall within the 3-6 foot range" -> [3,6]. pole-beans' hit is not only a trellis height: UMN "pole beans are
twining vines growing up to six feet and sometimes taller" (open bound, still null). Uncached counts: zucchini cites 39
distinct URLs, all cached (the spec's 3/60 counted occurrences).

**Total with a closed statement on a cached cited page: 46 herbaceous of 97** (11 + 35). Strict: 39.

### 3.3 PLA-465's 16: the `mature_dimensions_*` backfill

peach, nectarine, apple, lemon, blueberry, thyme, rosemary, oregano, sage, fig, pomegranate, elderberry, persimmon,
mulberry, pawpaw, lavender. Each carries one `plant_dimensions` field_addition (2026-09-16) naming the URL and a
sha256; every catalog id exists and every URL is document-pathed. 14 of 16 have the height sentence in cached text.

| # | flag | recommendation |
| -- | -- | -- |
| K1 | apple: the record's URL (s3.wp.wsu.edu) is not cited on the crop and not cached. The same WSU handbook is cited and cached at the wpcdn URL and contains "m 26-semi-dwarf habit, 10'-14' tall". | **TAKEN.** **Backfill to the cited wpcdn URL.** |
| K2 | blueberry: the record's PSU URL is not cited or cached; the cited PSU `highbush-blueberry-production` says "usually 4 to 8 feet tall at maturity" against the authored [5,8]. | **RULED: fetch the record's PSU page first; if it states [5,8], keep and re-hash; if it is gone or states otherwise, re-anchor to the cited PSU [4,8] and record it as a PLA-465 value correction.** **Decision row:** fetch the record's page, or re-anchor to [4,8] (a value change on a woody crop, which reopens a PLA-465 value: your call). |
| K3 | None of the 16 records' sha256 values matches any cached file (lemon and pawpaw are cached under other fetches). | **TAKEN.** The backfill re-hashes: the sibling pair cites the page, the record keeps its historical sha. |
| K4 | oregano, sage, lavender, mulberry, persimmon, pawpaw take a low end from the NCSU Toolbox attributes line. | **TAKEN.** Quote that line. |

---

## 4. The gate list

| gate | change | when |
| -- | -- | -- |
| **A44** `planting_layout_gate` | Extend to the **rootstock override key**: on a crop carrying any `rootstock_options[].spacing_inches`, every row carries it (all-or-none, so a null is explicit), each null or `[lo,hi]`; a non-null override has a source the row cites with an anchor. (Entry `rows_per_bed` and support-only `mature_height_ft` are already gated.) | promote 2 tools commit, unarmed until the data |
| **A62** `sourced_block_ratchet_gate` | `SIBLING_BLOCKS["mature_dimensions"] = ("mature_height_ft", "mature_spread_ft")`. Without it A62 **fails** the new citation keys (it fails a citation key on an unnamed block). | heights tools commit |
| **A59** `plant_dimensions_gate` | Keeps the `field_additions` record rule and gains the sibling rule: height or spread non-null => `mature_dimensions_sources` non-empty, an anchor per source. Measured: A59 already REQUIRES a `plant_dimensions` field_additions record on every authored height, so **each new height needs a record the promote cannot write today** (section 8, T3). | heights tools commit |
| `numeric_sanity` | Unchanged (20 ft herbaceous ceiling; rootstock spacing 1-360 in, which covers 300). | |
| **Live-state re-measure** | `test_problem_id_collision_gate.py` `PINNED_SHA`; `test_sourced_block_ratchet_gate.py` + `sourced_block_ratchet_known.py` MEASURED_ON; `test_bare_host_gate.py` + `bare_host_gate_known.py`; `test_bare_host_scan.py` (`bare_host_self_pathed_known.json`); `test_gate_citation_ratchets_a62_a63.py`; `test_gate_plant_dimensions_a59.py`; `test_numeric_sanity_gate.py`; the `promote_fixture.COMMIT_FOR` pin. E1: the app re-export. Re-grep `cf1d480d` across `tools/test_*.py` in each data commit (the 7 are not the full PLA-544 inventory). | each data commit |

---

## 5. Consumer preconditions (measured, `E_consumer_preconditions.md`)

**Nothing in plant-app or plant-astro throws on promote 2, and neither build needs a code change first.** The hard
preconditions are dataset-side shape rules for the stage:

| # | hard precondition | source |
| -- | -- | -- |
| X1 | Leave optional entry fields **absent, never null** (`in_row_inches`, `hill_spacing_inches`, `plants_per_hill`, `rows_per_bed`, `mature_height_ft`); `rows_per_bed` an int; every pair exactly 2 numbers; `support` in the 4-value enum. | astro `content.config.ts:19-31` (optional, not nullable): the astro build fails otherwise |
| X2 | Every new rootstock-row source carries `anchoring_urls[id].url`. | astro `pot-figure.ts:23-34` `isSourced` requires it; otherwise apple M9/M26 silently lose "pot OK, 20+ gal" (`pot-figure.test.ts:100-126` reads live M9). **Already enforced:** the promote writes the anchor with the source and refuses otherwise. |
| X3 | No `source_quote` (or another app drop name) inside new entries or rows. | app `export-projection.mjs:174-192` throws |
| X4 | A default whose numbers change needs its app suites re-measured in the app data commit (test work, no code). | beefsteak (moves under S1 either way), english-cucumber (S5); **cherry-tomato if S1 = stake (in-row [18,24]) OR if S1 = cage with S3's cage rows (row mirror [60,72] -> [48,48])**; it stays put only under cage with rows `not_authored`, which leaves the crop-root row mirror null: FullnessMeter, PlotDiagram, RowsWindow, CalculatorPane, fill-fractions, fit, plot-calc, herb/planner-tools (file:line in E) |

Already in place: `mature_dimensions_sources` / `_anchoring_urls` are in the app's ship list
(`export-projection.mjs:88-92`); astro types crop heights as a nullable pair (`content.config.ts:75-76`); every reader
in both repos keys on `default` + `arrangement`, never `support` or entry count, so a support default renders its
in-row as "between plants", consistent with the mirror; no consumer persists an entry id; nothing reads
`open_findings[].summary` (the app keeps status, source_set, date). Spec §11's `container-card.ts:168-169 sizeRange`
reference is stale; astro has no hero height tile.

Soft (data can land without them): the app planner reads `spread_ft * 12` for a picked rootstock
(`rootstock.ts:51-55`) and never the override (seedling plans at 360 in vs the sourced [216,300]); read the override
first, label the proxy modeled. Sub-3-ft heights round differently (app whole inches, astro one decimal): authoring
sub-3-ft values as whole inches over 12 avoids the mismatch. Show support / "needs support" on spacing surfaces;
read `rows_per_bed` and entry heights (PLA-629); add height to Herb's FACT_KEYS; refresh the stale "105 of 121" test
title (`at-a-glance.layout.test.ts:80`).

---

## 6. Where the cached page disagrees with the spec's expectation

1. **sweet-pea is not support-required** (spec §10.2): OSU, NCSU, UC IPM, its own description.
2. **No pea entry is replaced**; the PLA-629 constraint does not bind.
3. **Tomatillo has no support fork** (kickoff 55: USU's fork is hill vs row).
4. **Support entries total 13 measured (16 maximum), not "the measured 24"**: the 24 were three axes, and the
   arrangement axis landed in promote 1.
5. **PLA-532's pages carry no tomato or cucumber number**; the figures come from crops' own pages.
6. **Melon/squash trellis: acorn by name, cantaloupe by ruling, the rest none.**
7. **okra states a height** (spec §4.4 said no); pole-beans' reason changes; zucchini's uncached count was occurrences.
8. **cherry-tomato's [24,36] is PSU's unstaked figure** (spec §1.4 called it caged).
9. **Heights: 46 herbaceous crops (39 strict), not "11 + 63 candidates"**, with page disagreements on 21.
10. **Evidence: most height pages are not hashed.** Only 3 of the tip-over / backfill pages are in
    `tools/.evidence_cache` (UMD peppers, UF HS402, NC State pawpaw); 6 of 7 non-pepper tip-over pages and 14 of 16
    backfill pages are `.doc_cache` text only. Support entries mostly rest on already-hashed pages.

---

## 7. Worklist sizes, and the promote 3 recommendation

| unit | size |
| -- | -- |
| apple overrides | 5 rows (4 non-null, 1 null), 4 sources added |
| finding corrections | 24 findings on 24 crops |
| support entries | **RULED: 16 entries on 12 crops**: 13 (tomatoes 9 on cherry, grape, heirloom, beefsteak, roma; cucumbers 4) + acorn 1 + cantaloupe 1 (M1) + strawberry bed 1; sweet-pea 0 (P2); defaults move on 6 crops under S1 = cage (cherry, grape, heirloom, beefsteak to `row-cage`; english-cucumber to `row-trellis`); hero in-row changes on beefsteak and english-cucumber; the row mirror changes on every new default (S3) |
| heights | 11 tip-over + 35 others = **46 crops** (39 strict), ~21 disagreement decision rows, 7 habit-spanning rulings |
| backfill | 16 crops (2 flagged) |
| pages to hash before citing | support: UNL G1650 (S3), UC IPM strawberry if its PDF is not hashed; heights: ~30 (most tip-over, most backfill, the D-table pages) |

**SPLIT TAKEN (2026-10-02). Promote 2 = apple overrides + corrections + support entries; promote 3 = heights + the
backfill.**
- PLA-534 needs the support entries; heights are not on its path.
- The support stage rests almost entirely on already-hashed pages and has 9 decision rows. Heights need ~30 page
  fetches, ~30 decision rows, a third record allowance (A59's `field_additions`), a quote-check change (T4), and two
  gate changes (A62 sibling, A59 sibling rule). Bundled, heights set the landing date for support.
- The two touch disjoint keys (entries + rootstock rows + finding summaries vs crop-root heights + their sibling pair +
  field_additions), so promote 3 can stage while promote 2 is in review.

**Sessions:**
- **Promote 2, session 2:** tools commit 2 (section 8, T1-T2: the layout-entry stage key and A44's override key;
  TDD + harness + affected set), fetch UNL G1650 (+ UC IPM PDF if needed), stage all of section 1 and section 2.
- **Promote 2, session 3:** independent source-truth review (every entry + every correction text), gauntlet, data
  commit, arming, state trio; app re-export + the X4 re-measure.
- **Promote 3, sessions 1-3:** tools (T3-T5) + fetch; author the 46 + backfill 16; review + land.

---

## 8. Tools still owed (later commits, each TDD + mutation harness + affected set)

| # | change | for |
| -- | -- | -- |
| T1 | Stage key `planting_layout_add` (append entries verbatim, ids pinned, never re-derived) and `default` move; mirrors recomputed through `planting_layout_gate`'s own functions (imported, never retyped); restatement adjudication when a mirror moves (promote 1's guard 4). Existing entries byte-identical. | promote 2 |
| T2 | A44 rootstock override key (section 4). | promote 2 |
| T3 | **A third record allowance:** append one `verification_status.field_additions[]` entry with `field == "plant_dimensions"` per newly authored crop (A59 requires it). Same shape as (F): append-only, named field, nothing else writable. | promote 3 |
| T4 | **The quote check cannot read heights as authored** (measured): `quote_states` matches `mature_height_ft` exactly, so a rounded 47/12 fails, and `mature_spread_ft` has no branch (falls into the inches path and fails at any value). Add a promote-3-only `quote_states_ft` with a stated rounding tolerance in `pla10_promote_common.py`, leaving the promote-1 copy byte-identical (the suite pins it). | promote 3 |
| T5 | A62 `SIBLING_BLOCKS["mature_dimensions"]`; A59 sibling rule. | promote 3 |

---

## 9. Not in promote 2 or 3

`plant_habit` values (PLA-12); vertical claims beyond support entries (PLA-534); `footprint_inches`; the 12 woody
height nulls; per-rootstock row spacing; tomatillo's hill fork; the tomatillo `det_indet` copy defect (PLA-652); roma's PSU/ISU `row-none` disagreement unless reopened.
