# PLA-10 field-shape spec: planting layout, row spacing, heights, rootstock spacing, plant habit

**Written:** 2026-09-30. **READ-ONLY session:** canonical unchanged, nothing staged, no `tools/` edit, no promote.
**Checkout:** branch `main`, HEAD `26e455a` == origin/main `26e455a`; canonical `00dda31c` == `LATEST.txt`.
**Consumers measured:** plant-astro `main` `277529c`; plant-app `feat/community-foundation` `71e327ba` (dirty working
tree: `guides.dataset`, `dataset-provenance.json`, one test, `control-methods.json`; read, not touched).
**Linear status fields checked before trusting bodies:** PLA-10 In Progress; PLA-607 Done; PLA-465 Done; PLA-13 Todo;
PLA-426 / PLA-429 / PLA-629 Backlog; PLA-534 Todo.
**Rulings in force:** D1-D12 on PLA-10 (2026-09-29), the apple addendum (2026-09-30), and R1-R5 below (Trevor,
2026-09-30). They are not reopened here.

> Method. Field counts are a key walk over a scratch copy of `00dda31c`. Page claims come from `tools/.doc_cache`
> (`sha1(url).txt`, 1,216 files; 3,961 of the 4,321 distinct URLs the certified crops cite are cached, 360 are
> UNCACHED and therefore UNDETERMINED, never absent). Page populations are regex-derived, so they are **upper bounds**
> and are labelled that way. The firm numbers are the field counts and the sentences quoted verbatim. Promote
> authoring re-reads every page from raw bytes (the 2026-07-30 / 08-03 standard); nothing here is a citation.

---

## Rulings (resolved by Trevor, 2026-09-30)

| # | question | ruling | rests on |
| -- | -- | -- | -- |
| **R1** | **Rootstock basis for tree spacing: which crops move?** | **TAKEN.** Move a tree crop's `spacing_inches` only where a cited page states a spacing for the recommended rootstock or its size class, carrying the other classes as `rootstock_options[].spacing_inches` overrides from the same page. **Promote 1 moves apple only**; pear-european, grapefruit, cherry-sweet, pear-asian and cherry-sour get findings recording the basis gap. The D10 rationale's WSU EB0937 example is **struck**: it was unconfirmed (§3). | §5. apple is the only crop with a cited page giving spacing by class (UMN: standard 20-25 / semi-dwarf 12-15 / dwarf 6-8 ft). |
| **R2** | **What `spacing_inches` means on a crop whose default entry is a hill.** | **NOT TAKEN as recommended. `spacing_inches` keeps ONE meaning on every crop: the distance between individual plants.** A hill entry carries the between-hills distance (`hill_spacing_inches`) and `plants_per_hill`. Consumers reading the default entry render "between hills" when the default is a hill. **Amended (Trevor, 2026-09-30): the mirror is the between-plants figure from the default entry, falling back to any other entry that carries one (declared order); `null` only when no entry does.** The 8 zone-independent crops move from `[]` to `null` with `row_spacing_reason: "not_applicable"`. **Further rulings (2026-09-30):** `row_spacing_inches` follows the default entry only, no fallback; a third reason value `see_layout` marks a hill default whose row figure lives on a non-default entry (§3); no dedicated spacing-reason field. | Trevor's ruling. Re-measured: under the fallback rule **no hill candidate goes `null`** (every one has a per-plant figure on a cited page); the only `null`s after promote 1 are the 8 microgreens (§2.4). `null` still reaches consumers, so the consumer repoint is a **hard blocker** on promote 1 (§10.1). |
| **R3** | **Citation-gate scoping (PLA-607's deferred question): are `growth_stages[]` and `notifications[]` sourced block types?** | **TAKEN. Both stay NAMED (sourced) on A62; the 1,073 waivers stay.** This arc adds one scoped coherence check: a spacing restated in either family (or in the other prose fields listed in §9) on a repaired crop must agree with the new values after the promote. | §9. 334 of 728 stage items and 167 of 538 notifications carry a number with a unit; 47 + 26 restate a spacing; 17 crops already cite per item. |
| **R4** | **`varieties[].plant_habit` controlled vocabulary (PLA-13, 2026-09-30).** | **TAKEN.** `standard, compact, dwarf, bush, half_runner, vining, erect, semi_erect, trailing`, a closed enum with a per-family allowlist; present-or-null on dict entries; `dwarf` only where `container_path == "cultivar"`. | §7. dry-bean already carries `half_runner`; the bramble pages split spacing on erect vs semi-erect/trailing. |
| **R5** | **A crop whose in-row spacing has no page in its cited set.** | **TAKEN.** Hunt first, inside promote 1. A crop still without a page after a recorded hunt ships its default entry under a **MIGRATION waiver**: keyed by identity, valid only while the entry's `in_row_inches` byte-equals the pre-promote `spacing_inches`, listed by name, able only to shrink. | §2.3. About 8 crops: bok-choy, rosemary, mulberry, borage, cosmos, sweet-alyssum, bee-balm, viola. The value exists today uncited; moving it into an entry changes where it lives, not what is claimed. |

**Decided in this spec (technical calls, each reversible before the promote that uses it):** D8 goes option (b), the
layout entry is the sourced record and `spacing_inches` is a gated mirror (§2); height and spread cite through a
crop-root sibling pair `mature_dimensions_sources` / `mature_dimensions_anchoring_urls` (§4.3); `grid` and `single`
leave the arrangement enum (0 population); `pollination_block_min_rows` stays crop-root (§1.3); vine run is not
`mature_spread_ft` (§4.5); a cultivar-conditional open bound ("over 5 ft") authors null (§4.4).

---

## 1. `planting_layout`: a list of (arrangement, support) entries

### 1.1 Canonical shape

`planting_layout` is a crop-level **list**. On every certified crop it is present and either non-empty or `[]`. `[]`
appears only on `zone_independent` crops (the 8 microgreens, measured), where it is the claim "assessed, no ground
layout". The 7 shells are byte-identical, because A39 exempts them.

Each entry:

| key | type | rule |
| -- | -- | -- |
| `id` | string | **Join key, pinned at first authoring and never re-derived** (the problem-id rule, applied here). Pattern `^(row\|hill\|block)-(none\|stake\|cage\|trellis)(-[a-z0-9]+)?$`. The qualifier appears only when two entries share a pair (strawberry's `row-none-bed`). |
| `arrangement` | enum | `row`, `hill`, `block` |
| `support` | enum | `none`, `stake`, `cage`, `trellis` |
| `default` | bool | exactly one `true` per crop |
| `in_row_inches` | `[lo, hi]` | **the distance between individual plants along the row (R2: one meaning everywhere).** Required on `row` and `block`. On `hill`, present only where the page also states a between-plants distance for that layout; otherwise absent. |
| `hill_spacing_inches` | `[lo, hi]` | required on `hill`, absent otherwise: the distance between hills along the row |
| `row_spacing_inches` | `[lo, hi]` or `null` | between rows (between hill rows on `hill`; equal to `hill_spacing_inches` when a page says "on all sides") |
| `row_spacing_reason` | `null` or `"not_authored"` | non-null iff `row_spacing_inches` is null. An entry is never `not_applicable`: an entry exists only where there is a ground layout. |
| `plants_per_hill` | `[lo, hi]` | required on `hill`, absent otherwise (not null: absent) |
| `rows_per_bed` | int >= 2 | optional, `row` only, absent by default; strawberry's two-row bed (promote 2) |
| `mature_height_ft` | `[lo, hi]` | **optional override**, absent unless the entry's support changes the height (pole beans, indeterminate tomatoes); `support != "none"` only |
| `sources` | list of catalog ids | non-empty; the one citation slot for every number in the entry |
| `anchoring_urls` | `{source_id: {url, verified}}` | one per source, the existing convention |

**Support requirement is derived, not stored.** A crop needs support iff none of its entries has `support: "none"`.
Pole beans (only `row-trellis` / `hill-trellis`) require it; tomatoes (with a `row-none` sprawl entry) do not. No
boolean can then disagree with the entries.

**Why an (arrangement, support) pair and not one `method` enum** (ruled D2, restated because the shape rests on it):
the sources fork on the two independently. Illinois gives pole beans in rows OR hills, both trellised; Cornell
tomatoes fork staked vs unstaked, all in rows. Cultivar habit (bush vs vining cucurbits) is **not** an entry axis. It
lives on `varieties[].plant_habit` (§7), and bush cucurbit spacings are not authored this arc (D2).

`vertical` is not a value. PLA-534's vertical growing is `support` in `{stake, cage, trellis}`. Adding a support
value (netting, fence) is an enum change by ruling, not a free string.

### 1.2 Crop-level mirrors (the §2 decision)

| crop-root key | meaning | rule |
| -- | -- | -- |
| `spacing_inches` | between individual plants (existing field, D1; one meaning on every crop, R2) | `==` the `in_row_inches` of **the first entry that carries one, default first, then declared order**; **`null` only when no entry carries one** (a new state for this field), which after promote 1 means the 8 `zone_independent` crops (today `[]`, §3) |
| `row_spacing_inches` | between rows (new) | `== default.row_spacing_inches`; `null` on microgreens |
| `row_spacing_reason` | why null (new) | `null` when `row_spacing_inches` is non-null. Otherwise one of three values (ruled 2026-09-30): **`"see_layout"`** iff the default is a `hill` with no row figure and a non-default entry carries one; **`"not_applicable"`** on `zone_independent` crops and nowhere else; **`"not_authored"`** in every other case. `row_spacing_inches` follows the **default entry only, no fallback**. |
| `spacing_inches_anchoring_urls` | **retired** | the 11 existing dicts move into the default entry's `anchoring_urls` |

The mirrors carry **no** citation keys. Consumers read them exactly as they read `spacing_inches` today.

### 1.3 Block

`block` keeps its coupling to the crop-root `pollination_block_min_rows` (int >= 2): a crop has a `block` entry iff
it carries `pollination_block_min_rows`. The field stays at the root because the app reads it there
(`plot-calc.ts:122-123`, `at-a-glance.ts:168-172`), and because it is a pollination property of the crop, not of one
layout. Moving it into the entry would repoint two consumer reads for no data gain. Block population: the 4 corn crops,
measured. No other wind-pollinated crop is on the roster (D6).

### 1.4 Worked examples

**Single entry, the common case (potato).** The migrated anchors come from the retired `spacing_inches_anchoring_urls`.

```json
"planting_layout": [
  {
    "id": "row-none", "arrangement": "row", "support": "none", "default": true,
    "in_row_inches": [10, 12], "row_spacing_inches": [30, 36], "row_spacing_reason": null,
    "sources": ["umn_ext", "umaine_ext", "clemson_hgic"],
    "anchoring_urls": {
      "umn_ext": {"url": "https://extension.umn.edu/vegetables/growing-potatoes", "verified": "2026-06-30"},
      "umaine_ext": {"url": "https://extension.umaine.edu/publications/2077e/", "verified": "2026-06-30"},
      "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/potato/", "verified": "2026-06-30"}
    }
  }
],
"spacing_inches": [10, 12], "row_spacing_inches": [30, 36], "row_spacing_reason": null
```

(`[30, 36]` is potato's own prose pair; promote 1 re-reads it from the page before writing.)

**Block, migrated from the string (sweet-corn).** Today: `"planting_layout": "block"`, `pollination_block_min_rows: 4`.

```json
"planting_layout": [
  {
    "id": "block-none", "arrangement": "block", "support": "none", "default": true,
    "in_row_inches": [8, 12], "row_spacing_inches": [30, 36], "row_spacing_reason": null,
    "sources": ["iastate_ext"], "anchoring_urls": {"iastate_ext": {"url": "<ISU sweet corn page>", "verified": "<read date>"}}
  },
  {
    "id": "hill-none", "arrangement": "hill", "support": "none", "default": false,
    "hill_spacing_inches": [30, 30], "row_spacing_inches": [30, 36], "row_spacing_reason": null,
    "plants_per_hill": [4, 5],
    "sources": ["iastate_ext"], "anchoring_urls": {"iastate_ext": {"url": "<ISU sweet corn page>", "verified": "<read date>"}}
  }
],
"pollination_block_min_rows": 4
```

(ISU: "8-12 in apart in rows 2.5-3 ft ... may also be planted in hills ... 4-5 seeds per hill ... hills 2.5 ft apart
with 2.5-3 ft between.")

**Support fork (cherry-tomato, promote 2 adds the support entries).**

```json
"planting_layout": [
  {"id": "row-stake", "arrangement": "row", "support": "stake", "default": true,
   "in_row_inches": [18, 24], "row_spacing_inches": [36, 36], "row_spacing_reason": null,
   "mature_height_ft": [6, 8], "sources": ["unl_ext"], "anchoring_urls": {"unl_ext": {"url": "<UNL G1650>", "verified": "<date>"}}},
  {"id": "row-cage", "arrangement": "row", "support": "cage", "default": false,
   "in_row_inches": [24, 36], "row_spacing_inches": [48, 48], "row_spacing_reason": null,
   "sources": ["unl_ext"], "anchoring_urls": {"unl_ext": {"url": "<UNL G1650>", "verified": "<date>"}}},
  {"id": "row-none", "arrangement": "row", "support": "none", "default": false,
   "in_row_inches": [36, 36], "row_spacing_inches": [48, 60], "row_spacing_reason": null,
   "sources": ["unl_ext"], "anchoring_urls": {"unl_ext": {"url": "<UNL G1650>", "verified": "<date>"}}}
]
```

(UNL G1650: "unstaked 3 ft in rows 4-5 ft; staked 18-24 in in rows 3 ft; caged 24-36 in in rows 4 ft". The `[6, 8]`
height override is illustrative until promote 2 reads a page for it. Which entry is the default is a promote-2
decision row. **cherry-tomato's `spacing_inches` is `[24, 36]` today**, the caged figure, so a staked default moves
the hero tile; that move is the decision row, not an accident.)

**Hill default with a row entry behind it (watermelon, per R2 as amended).**

```json
"planting_layout": [
  {"id": "hill-none", "arrangement": "hill", "support": "none", "default": true,
   "hill_spacing_inches": [96, 96], "row_spacing_inches": [96, 96], "row_spacing_reason": null,
   "plants_per_hill": [2, 2], "sources": ["uga_ext"], "anchoring_urls": {"uga_ext": {"url": "<UGA C1035>", "verified": "<date>"}}},
  {"id": "row-none", "arrangement": "row", "support": "none", "default": false,
   "in_row_inches": [60, 72], "row_spacing_inches": [72, 96], "row_spacing_reason": null,
   "sources": ["clemson_hgic"], "anchoring_urls": {"clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/watermelon/", "verified": "<date>"}}}
],
"spacing_inches": [60, 72], "row_spacing_inches": [96, 96], "row_spacing_reason": null
```

(UGA C1035: "hills ... 8 ft on all sides". Clemson: "Plants should be spaced 5 to 6 feet apart within the row" in
"rows spaced 6 to 8 feet apart". The hill default carries no between-plants figure, so `spacing_inches` falls back to
the row entry's `[60, 72]`. **`row_spacing_inches` follows the default only, no fallback** (ruled 2026-09-30), and
here the hill entry carries its own `[96, 96]`. Had UGA given hill spacing with no row figure, the crop-root
`row_spacing_inches` would be `null` with `row_spacing_reason: "see_layout"`, pointing the reader at the Clemson row
entry's `[72, 96]`. The hero renders the default's hill tile ("8 ft
between hills, 2 plants per hill"). Today's `[36, 72]` sits below the crop's own hill prose, a D1 blend. Whether
watermelon's default is the hill or the row is a promote-1 decision row.)

**Microgreens (arugula-microgreens).**

```json
"planting_layout": [], "spacing_inches": null, "row_spacing_inches": null, "row_spacing_reason": "not_applicable"
```

(Today `spacing_inches: []`; promote 1 writes `null`, §3.)

### 1.5 Migration of the 6 string values

| crop | today | promote 1 writes |
| -- | -- | -- |
| sweet-corn, field-corn, popcorn, flint-corn | `"block"` + min rows 4 | `block-none` default (+ `hill-none` where the page gives hills), min rows kept |
| artichoke, asparagus | `"row"` | `row-none` default. asparagus's row/in-row numbers (the 2026-07-23 plan's `[48, 60]` / `[12, 18]`) live only in prose today and are re-read from its page |

The string form ceases to exist. Also owed alongside: append a correction to the PLA-7 D3 note (artichoke and
asparagus are `row`, not `block`); fix `planting_layout_gate`'s stale docstring (it says `row` is unpopulated).

### 1.6 A44 rewrite (`tools/planting_layout_gate.py`)

The rewrite checks the list shape, fires on every certified crop (presence armed in the data commit, never before), and
refuses a population below its floor:

1. `planting_layout` is a list. `[]` iff `zone_independent` is true. It is non-empty on every other certified crop.
2. Each entry has exactly the keys in §1.1 for its arrangement, with enums closed and `id` matching its pair and pattern.
   Ids and pairs are unique per crop.
3. Exactly one `default: true`.
4. `hill` iff `plants_per_hill` and `hill_spacing_inches` are present; `row` and `block` require `in_row_inches`;
   `hill` carries `in_row_inches` only when its page states one. `block` entry iff `pollination_block_min_rows` is
   present and an int >= 2.
5. Every `[lo, hi]` holds numbers with `0 < lo <= hi`. On an **entry**, `row_spacing_inches` is null iff
   `row_spacing_reason == "not_authored"` (`see_layout` and `not_applicable` are crop-root values only).
6. `mature_height_ft` appears only on entries with `support != "none"`, in A59's shape.
7. **Mirror equality**: `spacing_inches ==` the `in_row_inches` of the **first entry carrying one, default first,
   then declared order**; `null` iff no entry carries one. `row_spacing_inches` equals the **default's, no fallback**.
   Crop-root `row_spacing_reason` is `null` iff `row_spacing_inches` is non-null; otherwise `"see_layout"` iff the
   default is a `hill` and some non-default entry carries a non-null `row_spacing_inches`, `"not_applicable"` iff
   `zone_independent`, else `"not_authored"`. On `zone_independent`: `planting_layout == []`, `spacing_inches` `null`,
   `row_spacing_inches` `null`, `row_spacing_reason == "not_applicable"`. Mutations the gate must catch: mirror taken
   from the second carrier while the default carries one; mirror non-null when no entry carries one; a `[]` mirror
   surviving on a zone-independent crop; crop-root `row_spacing_inches` borrowed from a non-default entry;
   `see_layout` on a `row` / `block` default, or with no entry carrying a row figure; `not_authored` where
   `see_layout` holds.
8. No crop-root `spacing_inches_sources` or `spacing_inches_anchoring_urls`. A62's discovery guard fails the first, and
   this check fails the second by name, so a second authored copy cannot reappear (§2).
9. Report the inspected population (crops and entries) and REFUSE below a literal floor (CLAUDE.md,
   "inspected and clean" vs "inspected nothing").

Mutation bar (PLA-215): one mutation per check family, a MUTATION-APPLIED marker plus a sentinel, the WHOLE suite as the
positive control, and `set(pre) == set(post)` before value comparison in the promote's guards.

---

## 2. `spacing_inches`: the D8 question, decided **(b)**

### 2.1 The two options

| | (a) authored, gains `spacing_inches_sources` | **(b) the default entry is the record; `spacing_inches` is a gated mirror** |
| -- | -- | -- |
| authored copies of in-row | two: crop root + default entry | one: the entry |
| citation slots for in-row | two, can cite different pages | one |
| §F sees | root sibling pair (`whole_crop_gate.py` sibling loop keys on `*_sources`), +1 claim leaf per crop, **plus** each entry (`anchor_walk` recurses into list items) | each entry only; root has no `sources`, correctly, since it asserts nothing of its own |
| A62 sees | `SIBLING_BLOCKS["spacing_inches"]` **and** `ITEM_FAMILIES["planting_layout"]` | `ITEM_FAMILIES["planting_layout"]` keyed by `id` only |
| A62 waivers at naming | **+102 or more**: every existing uncited spacing becomes a waived identity when the sibling family is named | 0 new, if every entry is cited (R5 governs any exception) |
| drift guard needed | yes, an equality gate anyway, or the two copies may disagree (which is the blend defect again) | yes, the mirror gate (§1.6 check 7), including the R2 `null` state (§2.4) |
| consumer change for in-row | none | none |
| `ANCHOR_ONLY` | `spacing_inches_anchoring_urls` leaves it (gains a sources home) | same, by retirement |

### 2.2 Why (b)

1. **The blend was one field doing two jobs.** Two authored copies of one number, each with its own citation, rebuild
   the conditions for a new divergence. (a) needs the equality gate anyway, so it pays for (b)'s gate and keeps a
   second citation that can disagree.
2. **Zero change to §F and a naming-only change to A62.** Measured in `whole_crop_gate.py`: `anchor_walk` checks any
   dict with a non-empty `sources`, recursing through lists, so every entry is a claim leaf the day it lands. A62's
   discovery guard already fails an unnamed `planting_layout[].sources` (PLA-607's proof set). Naming the family is the
   whole change.
3. **A reintroduced second copy fails by name.** Under (b), a later session that adds `spacing_inches_sources` trips
   A62's discovery guard (unnamed sourced field) and A44 check 8. Under (a) nothing stops the entry and the root
   drifting except the equality gate.
4. **A mirror gate is a coherence gate, and coherence is not fidelity.** That is acceptable here because fidelity sits
   on the entry, where §F, A62 and A63 all see it. The mirror gate only proves the consumer copy did not drift.

### 2.3 What (b) costs promote 1

Every crop that carries a spacing pair (113) needs a cited default entry. Today 11 carry an anchoring dict and 102 carry
nothing. A regex over cached cited pages finds an in-row candidate on 101 of 113 (an upper bound on citability). The
12 without one are bok-choy, rosemary, lime, orange-navel, mandarin-clementine, mulberry, grapefruit, borage, cosmos,
sweet-alyssum, bee-balm and viola. The four citrus are covered by UF/IFAS HS132, already cited by all five citrus
crops: "For home plantings, the spacing recommended should be a minimum of 15 feet between trees". The regex missed it
because it names no species. That leaves about 8 for a hunt, and R5 decides what ships if a hunt fails.

### 2.4 R2 as amended: one meaning, a fallback, and the `null` state

`spacing_inches` means the distance between individual plants on every crop. A hill's between-hills distance never
enters it (`hill_spacing_inches` carries that). The mirror takes the between-plants figure from **the default entry,
falling back to any other entry that carries one, in declared order**; it is `null` only when no entry does.

| state | when |
| -- | -- |
| `[lo, hi]` | some entry carries `in_row_inches`: every `row` / `block` default, and any `hill` default with a `row` or `block` entry (or its own `in_row_inches`) behind it |
| `null` | **new:** no entry carries a between-plants figure, including every `zone_independent` crop (`[]` today, §3) |

**Population, re-measured under the fallback rule.** The hill candidates are the crops whose cited pages lead with
hills: 3 winter squash, pumpkin, 2 summer squash, 3 melons. **Every one has a per-plant row figure on a cached cited
page**, so a row entry can sit behind any hill default and **none goes `null`**:

| crop(s) | per-plant figure on a cited page |
| -- | -- |
| butternut, acorn, spaghetti, pumpkin | UMN pumpkins and winter squash: "Plant ... seeds three-fourths of an inch deep, 24 to 36 inches apart. Use the closer spacing if the variety is a bush type. Spacing between rows should be 5 to 6 feet." (pumpkin also UGA C1206: "Spacing rows per plants 72 by 48 in") |
| zucchini, yellow-summer-squash | OSU: "36 to 40-inch spacing between rows with plants 18-36 inches apart within the row"; UMN / SDSU "thin to stand 8 to 12 inches apart" |
| watermelon | Clemson: "Plants should be spaced 5 to 6 feet apart within the row" |
| cantaloupe | UGA B1179: "4 to 6 feet between rows and 2 to 3 feet in the row"; ISU "Transplants should be planted 2 feet apart in row" |
| honeydew-melon | ISU: "Transplants should be planted 2 feet apart in row, with rows 4-6 feet apart" |

Regex over cached pages, then the lines read, so this is **0 of 9 as measured**. Promote 1 must author the row entry
for any of these whose default it sets to a hill, or the crop goes `null`. **After promote 1, `null` = the 8
microgreens exactly**, unless a decision row drops a row entry.

**What `null` breaks until repointed, measured:**
- astro `content.config.ts:46` declares `spacing_inches: z.array(z.number()).optional()`, and `.optional()` **rejects
  `null`**. The build fails on the first microgreen page until the schema is `.nullable().optional()`.
- Both planner catalogs (astro `catalog.ts:126`, app `catalog.ts:105`) admit a crop only with a non-empty array. That
  keeps the microgreens out (correct, as today), but any crop that does go `null` **silently drops out of both
  planners**. Placement is rows only (hill layouts are display-only, ruled 2026-09-30). Hill placement, when built, is
  `hill_spacing_inches` on both axes with `plants_per_hill` per cell, not hill x row: PLA-636.
- `display_readiness_gate` demands a 2-positive pair for placeability on the non-indoor path. The microgreens take its
  indoor early return (`display_readiness_gate.py:66`), but the gate must still accept `null` wherever A44 check 7
  allows it, rather than reading it as "absent".
- **`timing_spine_gate.is_microgreen()` (`timing_spine_gate.py:36-41`) identifies a microgreen by `spacing_inches == []`**,
  and exempts it from `sow_depth_inches` / `thin_to_inches`. On `null` it returns False, and the 8 microgreens go red for
  missing sow depth and thinning. It must key on `zone_independent` (or the archetype) in promote 1's tools commit.
  Test fixtures that build microgreens with `spacing_inches: []` (`test_timing_spine_gate.py:98`,
  `test_register_coverage_gate.py:89`, `test_display_readiness_gate.py:46`) change with it. Shells keep `[]` (A39 exempts
  them; `test_reset_to_shell.py:68`).
- The hero guards already drop the tile on a non-pair (astro `hero-spacing.ts`, app `at-a-glance.ts` `isPair`). App
  `SeedlingDetailSheet.tsx:140`'s guard was fixed under PLA-633 (plant-app `7e02f379`).
- `numeric_sanity` skips a null. Its annual ceiling of 72 on `spacing_inches` no longer needs raising for hills,
  because the 96-inch watermelon hill lands in `hill_spacing_inches` (§10.1).

That makes the consumer repoint (§11) a **hard blocker** on promote 1 (§10.1), not an ordering preference: data that
lands first fails the astro build on the first `null`.

**Migrated anchor to check:** lemon's `spacing_inches_anchoring_urls` keys `uf_ifas_hs1153` to the URL of **HS402**. The
key and the document disagree; promote 1 resolves the key against the catalog before moving the anchor.

---

## 3. `row_spacing_inches`: present-or-null with a reason

- Present-or-null on **every certified crop** at the root (mirror) and on every entry.
- **`row_spacing_inches` follows the default entry only, no fallback** (ruled 2026-09-30); the between-plants fallback
  in §2.4 does not extend to rows.
- `row_spacing_reason` values at the crop root (ruled 2026-09-30, three values):
  - **`not_authored`**: a row spacing exists in the world and this dataset has not sourced it.
  - **`not_applicable`**: no ground rows. Only on `zone_independent` crops: measured, exactly the 8 microgreens.
  - **`see_layout`**: the default is a `hill` whose entry carries no row figure, and a **non-default** entry does. The
    reader goes to `planting_layout[]` for the row figure of the layout it is showing. Legal only on a hill default. A
    `row` / `block` default with no row figure is `not_authored` even when another entry has one, because a row default
    that lacks its own row spacing is a data gap, not a pointer.

  On an entry the reason is only ever `not_authored`. Population of `see_layout` is 0 until promote 1's decision rows
  set hill defaults; it depends on whether each hill page states a between-hill-rows figure. UGA's "8 ft on all sides"
  does; NMSU CR457 gives both hill and row spacing ("hills 24-45 in apart in rows 36-60 in"), so the measured candidates
  are expected to be few.
- **The 8 zone-independent crops change shape in promote 1.** They carry `spacing_inches: []` today (the timing-spine
  "legitimately N/A" contract). Promote 1 writes `spacing_inches: null`, `row_spacing_inches: null`,
  `row_spacing_reason: "not_applicable"` and `planting_layout: []` on each: arugula-microgreens,
  broccoli-microgreens, cilantro-microgreens, microgreens-mix, pea-shoots, radish-microgreens, sunflower-sprouts,
  wheatgrass. **No dedicated spacing-reason field** (ruled 2026-09-30): the empty layout plus `row_spacing_reason:
  "not_applicable"` carries the reason. A consumer tells this `null` apart from a data gap by `planting_layout == []`. The 7
  shells keep `[]` (A39 exempts them). Consequences: `timing_spine_gate.is_microgreen()` must stop keying on `[]`, and
  the consumers must accept `null` first (§2.4, §10.1 hard blocker).
- **Orchard trees are authored where their cited pages carry a row spacing** (D10 as amended). Cached cited pages with
  a between-row statement, as read this session:

| crop | page | sentence | authorable? |
| -- | -- | -- | -- |
| fig | UF/IFAS MG214; UGA C945 | "10-16 ft ... between plants and 13-20 ft ... between rows ... similar spacing should be maintained for dooryard trees"; "tree form ... 15 to 20 feet apart in the row and 20 feet apart between rows" | yes |
| pear-asian | UC ANR Asian pears | "12 feet apart in rows and 17 to 18 feet between rows" | commercial framing ("200 trees per acre"); reviewer call |
| persimmon | UF/IFAS HS1389 | "... between trees and 20 ft (6 m) between rows, allowing for 145 trees per acre" | commercial; reviewer call |
| mandarin-clementine | UF/IFAS CH116 | "Citrus trees were spaced 15 feet in a row and 20 feet between rows" | **no: a research trial's layout, not a recommendation** |
| blueberry | UGA C946; NC State; UMD | "highbush ... 4 ft between plants in a row and 10 ft between rows"; rabbiteye 5-6 x 11-12 | yes |
| blackberry | Clemson; UC MG SLO | "Erect varieties ... 2 to 4 feet apart in the row and 10 feet between rows" | yes |
| raspberry | UGA C766; PSU | rows 12 ft (C766); "8 to 12 feet apart in field production" (PSU) | yes |
| apple | WSU western-WA fruit handbook (cached copy) | states spacing "is determined by size of mature trees", **no number in the cached bytes** | **not confirmed; the WSU EB0937 example is struck from the D10 rationale (R1).** apple's between-tree figures come from UMN (§5); its row spacing is `not_authored` unless promote 1 finds a recommending sentence on a cited page. |

- **Authoring rule for the source-truth pass:** only a sentence that **recommends** a spacing counts. A trial's
  layout, a trap grid ("SWD traps ... 25 feet apart"), a trellis-post spacing, or a pollinizer distance ("within
  about 50 ft") is not a row spacing. All four appeared in this session's scan.

```json
"row_spacing_inches": null, "row_spacing_reason": "not_authored"
```

---

## 4. Heights

### 4.1 Meaning

- `height_inches` / `spread_inches` are **retired** (D3); `mature_height_ft` / `mature_spread_ft` carry herbaceous
  heights, feet with decimals (thyme `[0.5, 1]`, `[0.5, 1.3333]` precedent).
- **Crop-level figure = height as grown on the default layout entry.** A support entry may carry
  `mature_height_ft` as an override (§1.1). A crop with no support entry has no override.
- A point value from a page ("about 47 inches tall") authors as `lo == hi` (A59 allows `0 < lo <= hi`).
- Display below about 3 ft in inches is a consumer formatting rule (D3), not a dataset shape.

### 4.2 Worked example (eggplant, herbaceous)

```json
"mature_height_ft": [2, 4], "mature_spread_ft": null,
"mature_dimensions_sources": ["ncsu_ext"],
"mature_dimensions_anchoring_urls": {"ncsu_ext": {"url": "https://plants.ces.ncsu.edu/plants/solanum-melongena/", "verified": "<read date>"}}
```

(NC State Toolbox: "The plant may grow 2 to 4 feet tall and is multi-branched.")

### 4.3 Where their sources live (PLA-607's question): a crop-root sibling pair

**Decided:** `mature_dimensions_sources` + `mature_dimensions_anchoring_urls`, one pair covering both fields.
- §F checks it with no code change (its root sibling loop pairs any `X_sources` with `X_anchoring_urls`).
- A62 names it `SIBLING_BLOCKS["mature_dimensions"] = ("mature_height_ft", "mature_spread_ft")`.
- A63 walks crop-root `*_anchoring_urls` already.
- A59's `field_additions` record rule **stays**: the record is the amend-not-recert provenance, the sibling is the
  per-claim citation. Different jobs.
- **Backfill the 16 authored crops in promote 2** from their existing `plant_dimensions` records (each already names
  the institution, URL, bytes and sha256), so the roster has one citation convention, not two.
- The entry-level override is cited by the entry's own `sources`.
- Rejected: citing through `field_additions` only. §F skips `verification_status` by design, and PLA-465's own report
  measured the note's verbatim sentence as checked by nothing.

### 4.4 Measured: how many uncovered crops' cited pages state a height

Population: certified crops with `mature_height_ft` null, minus the 8 microgreens = **97**. The 16 authored are all
woody. A cached cited page carries a mature-height candidate statement near the crop's name on **63 of 97** (regex upper
bound; seedling heights, pest body lengths and trellis heights filtered, then the 18 below read by hand).

**The 18 tip-over crops first (PLA-10 2026-09-21 comment), read:**

| crop | states? | page | sentence / note |
| -- | -- | -- | -- |
| bell-pepper, jalapeno, banana-pepper, cayenne-pepper, habanero | yes, genus-level | UMD growing peppers | "Peppers are produced on bushy plants that can reach 3-4 ft. in height." **Scope check owed:** a genus-level page on habanero (*C. chinense*) and cayenne (crop-scope-is-not-its-slug) |
| broccoli | yes, point | NC State basics of broccoli | "Full-grown plants reach about 47 inches tall and 20 inches wide" |
| brussels-sprouts | yes | NC State Toolbox | "The plants can grow 2-4 feet tall and wide on a thick stalk." |
| broad-beans-fava | yes | NC State Toolbox *Vicia faba* | "a stiffly erect plant that grows 2-6 feet tall" |
| cosmos | yes | NC State Toolbox; UF/IFAS | "stalks that will get up to 4 feet tall"; "Garden cosmos can reach 3-6 feet" (the two disagree on the high end: a reviewer call) |
| dill | yes | UW-Madison | "Dill plants grow 18 inches to 4 feet tall" |
| eggplant | yes | NC State Toolbox | "may grow 2 to 4 feet tall" |
| snow-peas, sugar-snap-peas | cultivar-conditional, open bound | UMD peas | "Determinate cultivars ... less than 3 ft. in height; indeterminate cultivars ... over 5 ft." **Authors null**: an open bound cannot fill `[lo, hi]`, and which habit is grown is a `plant_habit` fact (PLA-12). |
| collards, okra, pole-beans, yellow-summer-squash, zucchini-courgette | **no** | none among cached cited pages | pole-beans' only hit is Clemson's trellis height ("at least 6 to 8 feet tall"), a support spec, never a plant height. Uncached cited URLs: okra 0/22, collards 0/35, pole-beans 0/22, zucchini 3/60 (undetermined). |

**13 of 18 state a height on a cached cited page, 11 of them as a closed range or point.** The two peas stay null.
**5 of 18 have no page in the cited set**, and D11 rules out a height hunt, so they stay null. The PLA-7 D3
wind/support app rule will therefore have 11 inputs among its 18 crops after promote 2. Record that on PLA-7 when promote 2
lands. The crops' own `container_notes` prose remains the cross-check on each authored number.

Candidate counts for the rest (upper bound, unread; promote 2 reads each from raw bytes). The zeros are the crops with
no candidate:
- **Warm fruiting:** tomatoes 16-24 hits each, tomatillo 6, sweet-potato 3, cucumbers 1-3. **Zero:** all vining
  cucurbits (their pages give vine run, see §4.5), dry-bean, green-beans-bush.
- **Cool-season:** kale 11, arugula 9, swiss-chard 8, lettuce 3. **Zero:** 14 crops (the root and bulb crops, cabbage,
  cauliflower, spinach, bok-choy, kohlrabi, collards).
- **Flowers:** echinacea 22, zinnia 19, marigold 18, sunflower 10, calendula / nasturtium 9. **Zero:** bee-balm, viola.
- **Herbs:** mint 10, chives 6, cilantro / dill 4, lemongrass 3, basil / parsley 2.
- **Corn:** flint 16, field / sweet 5. **Zero:** popcorn.
- **The 12 woody nulls** keep their PLA-465 rulings. This arc does not reopen them.

### 4.5 Two meaning calls

- **Vine run is not spread.** The cucurbit pages and prose give "vines sprawl 8 to 12 feet", a length along the ground,
  not a canopy diameter. `mature_spread_ft` stays null on vining crops. The ground area is the §6 derived quantity.
- **A trellis or stake height is not a plant height** (pole beans, above).

---

## 5. Rootstock-conditional spacing on grafted trees (apple addendum)

### 5.1 Shape

- Crop-level `spacing_inches` (and the default entry's `in_row_inches`) = **the recommended-rootstock basis**, the same
  basis PLA-465 used for `mature_height_ft`, and own-root / species where the rootstock is not size-controlling.
- `rootstock_options[].spacing_inches` = `[lo, hi]` **override** or `null`, cited by the row's own `sources` (A62
  names `rootstock_options` by `name`). It is authored only where a page states that rootstock's or its class's spacing.
- Row spacing per rootstock is not modeled. No cited page carries one for a home planting.

```json
"spacing_inches": [144, 180],
"rootstock_options": [
  {"name": "M9", "size_class": "dwarf", "spacing_inches": [72, 96], "sources": ["umn_ext"], "...": "..."},
  {"name": "M26", "size_class": "semi_dwarf", "spacing_inches": null, "...": "..."},
  {"name": "seedling", "size_class": "standard", "spacing_inches": [240, 300], "sources": ["umn_ext"], "...": "..."}
]
```

(UMN apples: "Tree spacing Standard trees: 20-25 feet Semi-dwarf trees: 12-15 feet Dwarf trees: 6-8 feet". M26 is
the recommended row, so its spacing is the crop-level figure and its override is null. Whether MM106 / MM111 take the
semi-dwarf figure is a promote-1 decision row: their size_class is `semi_dwarf` but their spreads are 15 and 18 ft.)

- **Consumer read:** `picked_rootstock.spacing_inches ?? crop.spacing_inches`. The app's current proxy
  (`planner/rootstock.ts:52-54`: a spread above 0 overrides spacing as `spread_ft * 12`) becomes the fallback when the
  override is null, labelled modeled.

### 5.2 Measured: which tree crops' `spacing_inches` spans rootstocks

`spacing_inches` in feet against each rootstock row's `spread_ft`. "Inside" means the size classes whose spread falls
inside the crop-level range.

| crop | spacing ft | classes on record | classes inside | recommended (its spread) | verdict |
| -- | -- | -- | -- | -- | -- |
| **apple** | 5-25 | dwarf, semi_dwarf, standard | dwarf, semi_dwarf (+ standard via UMN's 20-25) | M26 (10) | **SPANS, confirmed by a cited page** (UMN by class); the live hero's "5 to 25 ft" |
| pear-asian | 12-25 | semi_dwarf, standard | both | OHxF 87 (12) | spans by arithmetic; no cited page gives spacing by rootstock |
| cherry-sweet | 15-25 | dwarf...standard (4 classes) | semi_dwarf, semi_standard, standard | Gisela 6 (12-18) | spans by arithmetic; ISU's rule is "spaced [as far as] expected to reach ... tall", with no figure by rootstock |
| cherry-sour | 15-25 | dwarf...standard | semi_standard, standard | Mahaleb (10-15) | spans by arithmetic; range sits above the recommended row |
| pear-european | 15-25 | dwarf, semi_dwarf, standard | semi_dwarf (OHxF 97 only) | OHxF 87 (12) | **off-basis**: range excludes the recommended row's spread |
| grapefruit | 18-30 | dwarf, standard | standard | Swingle (12-18) | **off-basis**; open finding already cites HS1260 "in-row spacing 8-12 ft" for Swingle |
| orange-navel, lemon, lime, mandarin-clementine | 15-25 / 15-25 / 12-20 / 10-18 | standard (+ dwarf Flying Dragon on two) | standard | varies | standard basis; HS132's "minimum of 15 feet" governs; mandarin's is recorded modeled (open finding) |
| peach, nectarine, plum, apricot, persimmon, mulberry, pawpaw | narrow | standard only, or non-size-controlling | standard | | **not spanning**: UGA "about 18-20 ft" (peach), Clemson "18 to 22 feet" (plum), USU "18 to 22" (apricot) |

**So apple is the only crop confirmed by a page, and five more carry a basis problem the pages cannot yet fix.** R1
decides what moves. Note USU's peach line, "Depending on rootstock and training system, trees should be placed 12 to 16
feet apart": that is a rootstock-conditional statement on a crop whose rootstock rows are all non-size-controlling.
Recorded for the reviewer, not acted on.

---

## 6. Footprint: two meanings, never conflated

| name | meaning | state |
| -- | -- | -- |
| **`footprint_inches`** (PLA-429) | width of the plant's own body at the ground: trunk, crown, rootball. The physical floor, strictly below `spacing_inches[0]` (A59 already enforces). | **null on all 121, stays null** (not a published datum; LOW). The app's `PLANT_FOOTPRINT_FLOOR_INCHES = 6` (`solve-fit.ts:101`, capped by the guide minimum at `:169-170`) stands. |
| **ground area** (PLA-534) | area a plant consumes on the ground, what vertical growing reduces | **derived, not a field**: `in_row_inches x row_spacing_inches` of the chosen entry; on `hill`, `hill_spacing_inches` squared per hill (a hill occupies a square cell, the same cell PLA-636's placement uses), divided by `plants_per_hill` for per-plant. A hill layout whose page gives a distinct between-row figure is authored as a `row` entry, not a `hill`, so a hill's area never multiplies by a row spacing. PLA-534's "much less ground" delta is expressed between two entries of one crop. |
| `mature_spread_ft` | canopy spread | a field (§4), not a footprint |

The app's `areaPerPlantSqft = (s/12)^2` (`fit.ts:5-8`, both consumers) uses in-row on both axes today. Once
`row_spacing_inches` exists it becomes `(in_row/12) * (row/12)`. That repoint belongs to the consumer session.

---

## 7. `varieties[].plant_habit` controlled vocabulary (RULED, R4, 2026-09-30)

**Shape:** a scalar string from the enum, or `null` (not authored), on **dict** variety entries. Measured: 756
`recommended` entries on 121 crops, **133 of them bare strings** (stubs with no place for a key). Stubs carry nothing
until PLA-12 turns them into dicts. Existing values: dry-bean `bush` x4, `half_runner` x1. `bearing_habit`
(strawberry, 9) and `type` (brambles, blueberry, elderberry) are different axes and stay as they are.

| value | families it may appear on | notes |
| -- | -- | -- |
| `bush`, `vining` | cucurbits (cucumber x4, summer squash x2, winter squash x3, pumpkin, melons x3); legumes (dry-bean, green-beans-bush, pole-beans, edamame, broad-beans-fava, peas x3, sweet-pea) | UMN's bush-variety bypass; UMD peas' determinate/indeterminate is this axis |
| `half_runner` | legumes | already live on dry-bean |
| `standard`, `compact` | solanums (tomatoes x5, tomatillo, peppers x5, eggplant); tree fruit on `container_path` `cultivar` | on a `direct` crop `compact` is the smallest legal value (patio tomato) |
| `dwarf` | **only where `container_notes.container_path == "cultivar"`** | smallness is genetic; on `rootstock` crops size comes from `rootstock_options[]` and no variety carries `dwarf` (PLA-464 cleaned this out of the rootstock rows) |
| `erect`, `semi_erect`, `trailing` | brambles (raspberry, blackberry) | Clemson / UGA / VCE split spacing on these |
| any value | not on a family's allowlist | **refused** by the gate |

**Measured consequences:**
- **`dwarf` is legal on 8 crops today, and in practice on 1.** `container_path == "cultivar"` holds on butternut,
  acorn, spaghetti, watermelon, cantaloupe, pumpkin, honeydew (all cucurbits, which use bush/vining) and mulberry
  ("Dwarf Everbearing").
- **PLA-629's "genetic dwarf peach" cannot carry `dwarf` under this rule**, because peach, nectarine, plum, apricot,
  persimmon and pawpaw have `container_ok: false`, so `container_path` is null. Letting genetic-dwarf stone fruit
  carry `dwarf` needs their container answer changed first. That is a container-arc (PLA-7) question, and this spec
  does not pre-empt it.
- **Tomato determinacy is not `plant_habit`.** It is orthogonal to size (a dwarf indeterminate exists). It stays on
  crop-level `det_indet`; a variety-level determinacy is a PLA-12 question.
- Gate: family allowlist + the dwarf rule. It ships with PLA-12's first variety promote. This arc authors no habit
  values (D2: bush cucurbit spacings are not authored).

---

## 8. Pot capacity (D12)

- **`container_notes.plants_per_pot` governs where sourced.** Measured: readings on 7 crops (cherry-tomato,
  green-beans-bush, lettuce-leaf, swiss-chard, cabbage, parsley, eggplant x2).
- **The area rule is a modeled fallback, labelled at the call site** exactly as PLA-580 labels its volume scaling:
  per-plant area = `in_row_inches^2` or, where row spacing exists, the §6 derived area; capacity = pot surface area /
  per-plant area. It never overrides a sourced reading.
- **The strawberry contradiction, recorded:** strawberry's certified prose says "a 12-inch pot holds up to four plants"
  (`container_notes.notes_seasoned`; beginner: "up to four plants fit in a 12-inch pot"). A 12-inch pot's surface is
  about 113 sq in, or about 28 sq in per plant. Strawberry's in-row `[15, 24]` squared is 225-576 sq in, so the area
  rule would put **one** plant where the prose puts four, off by about 8x. strawberry's `plants_per_pot` is **null**;
  the four lives only in prose. **This is evidence that in-row and container spacing diverge**, which is why container
  spacing stays in PLA-7 and why the area rule may only be a labelled fallback.

---

## 9. Citation-gate scoping: `growth_stages[]` and `notifications[]` (RULED, R3, 2026-09-30)

**Ruled: sourced block types. Both stay on A62's named list; the 1,073 waivers (615 + 458, 104 crops each)
stay.**

What the ruling rests on, measured on `00dda31c`:

| | `growth_stages[]` | `notifications[]` |
| -- | -- | -- |
| items (certified) | 728 | 538 |
| carrying a number with a unit | **334** (46%) | **167** (31%) |
| restating a spacing | **47** items on 47 crops | **26** on 25 crops |
| crops citing per item | 17 (blueberry, raspberry, blackberry, elderberry + 13 flowers) | the same 17 |

1. **They are a restatement layer with its own claims.** cabbage's seedling stage: "Harden off over 7 to 10 days
   before setting out at 12-to-24-inch spacing; protect seedlings from flea beetles with row cover and from cabbage root
   maggot with stem collars." That is three claims, two of which appear in no other field.
2. **This arc moves the numbers they restate.** fava's `notifications[0]` says "4 to 6 inches apart"; cayenne's
   `growth_stages[2]` says "about 18 inches apart in rows 24 to 36 inches apart". Unsourced by design would mean no
   gate ever asks whether that restatement still agrees with its source.
3. **Per-item citation is authorable**: 17 crops did it (113 cited stage items, 80 cited notifications).
4. **Cost of keeping them named:** a new certified crop must cite them per item (the 7 shells when they certify). It is
   not a treadmill: the waivers are identities and only shrink.

**The alternative, not taken:** rule them unsourced by design, move them to `EXCLUDED` with a reason, drop the
1,073 waivers, and add a coherence gate that every number they state matches a sourced field. That is cleaner on paper,
but the coherence gate can only check numbers that have a sourced twin. The flea-beetle and stem-collar class above
would be unchecked either way.

**This arc adds one scoped check:** after promote 1, every spacing restated in `growth_stages[]`,
`notifications[]`, `soil_prep_*`, `start_method.notes_*` or `planting_method_notes_*` on a repaired crop equals the new
mirrors or is re-authored in the same promote. The six blend crops' restatements are listed in §10.1.

---

## 10. Promote plan

Sequence (from the rulings, updated with measured state):
1. **D9 pulled-forward items**, measured today:
   - **DONE:** the app `set_spacing` warning that compared a row spacing to `spacing_inches[0]`
     (`planner-tools.ts:998-1000`), and the `SeedlingDetailSheet.tsx:140` empty-array guard. Both landed under PLA-633
     (plant-app `7e02f379`, OTA `106562e7`).
   - **OWED to the running consumer repoint:** both planners' `rowWidthFt` (app `planner/fit.ts:182-207`, astro
     `planner/fit.ts:171-178`) reading `row_spacing_inches`; the `herb/prompt.ts:200-209` "row spacing is not in the
     dataset" paragraph;
   - the PLA-465 allowlist line is on `feat/community-foundation` as cherry-pick `1cbf0c61`, not on the app's `main`.
2. This spec, then the rulings.
3. PLA-532.
4. Consumer repoints (§11).
5. Promote 1.
6. Promote 2.
7. PLA-534 opens.

### 10.1 Promote 1: row + hill + block, the mirror flip, the blend repairs

**Authors:**
- `planting_layout` on **all 113** certified crops with a spacing pair: one cited default entry each, and
  `row_spacing_inches` where a cited page carries it (~105 upper bound; the 16 without a row page are the 8 microgreens +
  bee-balm, borage, calendula, cosmos, elderberry, lemongrass, mulberry, pawpaw, plum).
- `planting_layout: []` on the 8 microgreens, and their `spacing_inches` `[]` -> `null` with `row_spacing_reason:
  "not_applicable"` (§3).
- `hill` entries where a page gives hills: the winter cucurbits, pumpkin, summer squash, melons, corn. Each crop's
  default is a decision row. **A hill default ships with the row entry its page supports**, so `spacing_inches` falls
  back to it (§2.4 measured all 9 as having one). Expected `null` population after promote 1: **8 (the microgreens)**,
  asserted as an enumerated constant in the promote suite, never derived from the walk.
- `block` on the 4 corn.
- The 6-string migration (§1.5).
- The mirrors `row_spacing_inches` / `row_spacing_reason` on all 121.
- Retiring `spacing_inches_anchoring_urls`.
- apple's rootstock basis move and overrides (R1).

**Blend repairs (D1), each a decision row quoting the page**, with the restatements that must move with them:

| crop | today | the page/prose points to | restatements to reconcile |
| -- | -- | -- | -- |
| butternut-squash | [24, 72] | in-row 24-36; rows 5-6 ft (own prose) | `soil_prep_*` (states both, already right), `yield_expectations.factors_seasoned[2]` |
| acorn-squash | [24, 48] | vining 24-36 in-row, rows 3-6 ft; bush 18-24 (not authored, D2) | `soil_prep_*` |
| spaghetti-squash | [24, 48] | 24-36 in-row, rows 3-5 ft | `soil_prep_*` |
| watermelon | [36, 72] | hills 4-8 ft, rows 6-8 ft (prose); UGA 8 ft all sides. On a hill default the mirror falls back to the Clemson row entry, "5 to 6 feet apart within the row" (R2 as amended) | `soil_prep_seasoned`, `growth_stages[0]` ("per hill") |
| blackberry | [36, 72] | recommend **erect** as default: Clemson "2 to 4 feet apart in the row and 10 feet between rows"; trailing waits on `plant_habit` | `planting_method_notes_*` (states both types, already right) |
| strawberry | [15, 24] | matted row 15 x 36-48 (generic); region 18-24 | 18 spacing-bearing fields incl. region `synthesis_note`s; the in-row default is a decision row |
| broad-beans-fava | [4, 8] | sow 4-6, **thin to 8-10**; rows 18-30 | `start_method.notes_*`, `growth_stages[0]`, `notifications[0]` (all say sow 4-6, correct as sowing); `thin_to_inches [4, 6]` must also be reconciled |
| cayenne-pepper | [18, 24] | "about 18" in-row, rows 24-36; hi unstated | `growth_stages[2]` |

- The 2026-07-01 review notes that record the blend as deliberate get `[CORRECTION 2026-09-29: ...]` appended (D1a), never
  rewritten.

**Gates promote 1 must add or change**, each mutation-tested per PLA-215:
- **A44 rewrite** (§1.6), mirror equality included, presence armed in the data commit.
- **Coverage floor**: every certified non-zone-independent crop has >= 1 entry and a default; the inspected count is
  reported, and the gate refuses below a literal floor.
- **A62 naming**: `ITEM_FAMILIES["planting_layout"] = (("planting_layout",), "id", None)`; drop
  `spacing_inches_anchoring_urls` from `ANCHOR_ONLY`. Any R5 migration waivers go in with their byte-equality guard.
- **A63**: no code change. A scratch injection of a bare, sole anchor on a `planting_layout` entry must redden it
  (proof, not trust).
- **`display_readiness_gate`**: accept `spacing_inches: null` wherever A44 check 7 allows it (§2.4); keep the
  2-positive pair rule everywhere else.
- **`timing_spine_gate.is_microgreen()`**: key on `zone_independent`, not `spacing_inches == []`, with the three
  fixtures that build a microgreen from `[]` (§2.4).
- **`numeric_sanity`**: bounds for `in_row_inches` (same as `spacing_inches`: non-tree 72, tree 360);
  `hill_spacing_inches` (non-tree about 120, because watermelon's hill is 96); `row_spacing_inches` (non-tree about 144, tree about 480; blackberry rows reach 120 in); a
  `plants_per_hill` count; ordering `row_spacing_inches[1] >= in_row_inches[0]` on `row` entries;
  `rootstock_options[].spacing_inches` on the tree bound.
- **Register row 33**: `planting_layout` (list) + `row_spacing_inches` + `row_spacing_reason`; A39 presence-or-null.
- **The restatement check** (§9), scoped to the repaired crops.
- **Full test tree** before the tools commit (~1 hour; tell Trevor first).

**Tests that pin or read live state on this path and must re-measure in the data commit (Task 8), found by grep this
session:**
- **Pin the SHA outright** (4 tests + 3 measured waiver modules):
  - `test_sourced_block_ratchet_gate.py` (SHA + per-family literals; `sourced_block_ratchet_known.py` MEASURED_ON);
  - `test_bare_host_gate.py` (SHA; `bare_host_gate_known.py`);
  - `test_bare_host_scan.py` (`bare_host_self_pathed_known.json` measured_on);
  - `test_problem_id_collision_gate.py` (`PINNED_SHA`).
- **Read the live canonical and assert against it** (3 tests):
  - `test_gate_citation_ratchets_a62_a63.py`;
  - `test_gate_plant_dimensions_a59.py` (promote 2);
  - `test_numeric_sanity_gate.py`.

That is **seven**. It is not the full pin inventory PLA-544 asked for, which is still owed.

**HARD BLOCKER: promote 1 does not land until the consumer repoint has landed** (ruled 2026-09-30). The data commit
introduces `spacing_inches: null` (the 8 microgreens, §2.4), and measured today:
- astro `content.config.ts:46` declares `spacing_inches: z.array(z.number()).optional()`, which **rejects `null`**: the
  astro build fails on the first microgreen page until it is `.nullable().optional()`;
- both planner catalogs (astro `catalog.ts:126`, app `catalog.ts:105`) **drop any crop without a non-empty array**. That is
  correct for the microgreens. **Placement is rows only in both planners for now; hill layouts are display-only**
  (ruled 2026-09-30). A hill-default crop is placed in rows from the `spacing_inches` fallback (its row entry, §2.4),
  so the catalogs need no hill-placement change for promote 1. They must still accept `null` without crashing. **Hill
  placement, when built, is `hill_spacing_inches` on BOTH axes with `plants_per_hill` per cell, not hill x row: PLA-636**,
  future planner work outside this arc;
- `display_readiness_gate` **must accept `null`** where A44 allows it (a dataset gate, in promote 1's tools commit);
- both hero surfaces render the hill tile from a hill default.

**Other consumer preconditions:**
- The app export allowlist must classify `row_spacing_inches` and `row_spacing_reason` on the branch that builds,
  **before** the data lands. `projectRoster` (`export-projection.mjs:211-221`) throws on an
unclassified key, and `row_spacing_inches` is absent from `SHIP_TOP_LEVEL` today.

### 10.2 Promote 2: support entries and heights (after PLA-532)

**Authors:**
- Support entries on the measured 24: tomatoes x6 stake/cage/none; cucumbers x4 trellis/none.
- Pea support: promote 2 decides per crop whether the promote-1 `row-none` entry stays (support optional: UMD "can be
  trellised") or is replaced by `row-trellis` (support required: sweet-pea). The replacement is safe only while no
  consumer persists an entry id, so it must precede PLA-629.
- strawberry's `row-none-bed` (`rows_per_bed: 2`, ca_interior two-row beds).
- Melon, squash and pea trellis spacings **only if** PLA-532 admits a page that states them (D7).
- Height overrides on support entries.
- Herbaceous `mature_height_ft` / `mature_spread_ft` per §4.4 (the 11 tip-over closed ranges first, then crops whose
  cited pages state one).
- The `mature_dimensions_*` sibling pair on every authored crop, the 16 backfilled.

**Gates:**
- A44 extends to the override key.
- A62 `SIBLING_BLOCKS["mature_dimensions"]`.
- A59 keeps its record rule and gains the sibling (height non-null => sibling cited).
- `numeric_sanity` unchanged (20 ft herbaceous ceiling holds).
- The same live-state re-measure.

### 10.3 Not in either promote

`plant_habit` values (PLA-12); vertical claims beyond support entries (PLA-534); `footprint_inches` (stays null); the 12
woody height nulls (their PLA-465 rulings); per-rootstock row spacing.

---

## 11. Consumer contract

Line numbers are as measured today on astro `277529c` and app `71e327ba`.

| surface | reads | fallback while null |
| -- | -- | -- |
| **Planner row width, app** `planner/fit.ts:182-207` `rowWidthFt` | row's own `rowSpacingInches` (user decision, wins, `:193`) -> legacy per-planting (`:198`) -> **crop `row_spacing_inches`** (hi for roomy/Beginner, lo for tight/Seasoned, mirroring spacing) -> today's `planningSpacingInches` max | `row_spacing_reason == "see_layout"` (the default is a hill with no row figure; another entry carries one): **do not read the default entry's row figure, it has none.** Read the row figure from the entry that carries it, and surface that layout as an option the grower can pick. Never use its row figure silently inside the hill layout, and never substitute `hill_spacing_inches` for it. `"not_authored"` (a `row` or `block` default with a null row spacing): fall back as before, via the lookup cache (`row-spacing.ts:119`) then plant spacing, with the "No verified row spacing" caption (PLA-426's read-through; the lookup demotes to fallback, it does not retire). `"not_applicable"`: not placeable in rows (microgreens are already excluded by `catalog.ts:105`). |
| **Planner row width, astro** `planner/fit.ts:171-178` | **crop `row_spacing_inches`** -> today's max of `planningSpacingInches` | same as app, minus the user decision and the lookup cache: `see_layout` surfaces the entry that carries the row figure; `not_authored` falls back to plant spacing as before |
| **Area per plant**, both `fit.ts:5-8` | `(in_row/12) * (row/12)` when `row_spacing_inches` is present | `(s/12)^2`, as today |
| **Herb `set_spacing`** `planner-tools.ts:998-1000` (the row-vs-plant-minimum warning fixed under PLA-633, plant-app `7e02f379`) | compare a row value against `row_spacing_inches[0]`, a plant value against `spacing_inches[0]` | no row minimum known: no below-minimum warning on rows |
| **Herb `plan_rows`** `planner-tools.ts:824-844` | given -> **dataset `row_spacing_inches`** -> cache -> placeholder -> refuse | as today |
| **Herb prompt** `herb/prompt.ts:200-209` | the "ROW SPACING IS NOT IN THE CERTIFIED DATASET YET" paragraph retires for crops where `row_spacing_inches` is present, and for `see_layout` crops (the row figure is in the dataset, on another layout) | kept, scoped to `not_authored` crops |
| **Herb spacing intent** `herb/slice.ts:12-20` FACT_KEYS; `canned.ts:27,31` | add `row_spacing_inches`, `row_spacing_reason`, and the `planting_layout` entries; "Space X apart in rows Y apart" | `see_layout`: answer from the layout being discussed, naming it ("in hills, 8 ft apart; planted in rows, rows are 6 to 8 ft apart"); `not_authored`: "Space X apart" (in-row only, as today) |
| **Herb pot-size intent** | **does not exist today** (no canned intent; `container_notes` is not in FACT_KEYS). When built: `plants_per_pot.readings` (sourced) -> `min_pot_gallons` / `recommended_pot_gallons` -> the §8 area fallback, labelled modeled | never `spacing_inches` alone |
| **Hero spacing tile, astro** `HeroCard.astro:200` via `hero-spacing.ts` (2-finite guard, 77b51d2) | **R2:** when the default entry is a `hill`, read the **default entry**: `hill_spacing_inches` "between hills" + `plants_per_hill` "plants per hill". Otherwise `spacing_inches`, "between plants" / "between trees". `spacing_inches` is never relabelled: it always means between individual plants. | `spacing_inches: null` occurs only when no entry carries a between-plants figure (the 8 microgreens after promote 1): tile dropped; a malformed value drops the tile (already) |
| **Hero spacing tile, app** `at-a-glance.ts:145-158` (`isPair`), `SeedlingDetailSheet.tsx:140` (empty-array guard **fixed**, PLA-633, plant-app `7e02f379`) | same as astro | same |
| **Planner catalogs** astro `catalog.ts:126`, app `catalog.ts:105` | admit a crop with a `spacing_inches` pair and **place it in rows only** (ruled 2026-09-30); a hill-default crop places in rows from its `spacing_inches` fallback. Hill layouts are **display-only** (the hero tile), not placed. `null` with `planting_layout: []` stays excluded (microgreens). **Hill placement, when built, is `hill_spacing_inches` on both axes with `plants_per_hill` per cell, not hill x row: PLA-636** (future planner work, not this arc) | today both drop a crop without a non-empty array: correct for the microgreens; a hill-default crop is never dropped because its row entry feeds `spacing_inches` (§2.4) |
| **Hero height**, astro `container-card.ts:168-169` (`sizeRange`, needs 0 < lo <= hi); app: no top-level height reader yet | `mature_height_ft` / `mature_spread_ft`; below about 3 ft render inches (D3 consumer rule) | tile hidden on null |
| **Picker (PLA-629)** | spacing: `picked_rootstock.spacing_inches ?? spacing_inches`; height: `picked_rootstock.mature_height_ft ?? mature_height_ft`; layout: `picked_entry.in_row_inches` / `.row_spacing_inches` / `.mature_height_ft ?? mature_height_ft`; habit: `varieties[].plant_habit` (after PLA-12) | default entry / crop-level silently (D2) |
| **Layout tile + block advisory**, app `at-a-glance.ts:168-172`, `plot-calc.ts:122-123` | `pollination_block_min_rows` at the root (unchanged); "LAYOUT" tile may read the default entry's `arrangement` | as today |
| **Export allowlist**, app `export-projection.mjs:43-85` `SHIP_TOP_LEVEL` | add `row_spacing_inches`, `row_spacing_reason` (promote 1); `mature_dimensions_sources` / `_anchoring_urls` (promote 2); drop `spacing_inches_anchoring_urls` (`:82`) when it is retired | the build throws until classified |
| **Astro content schema** `content.config.ts:46` | `spacing_inches: z.array(z.number()).optional()` **must become `.nullable().optional()`** (R2's null state, §2.4); new keys pass through (`.passthrough()` at `:107`) | **hard blocker**: the build fails on the first microgreen page after promote 1 until changed |

---

## Surfaced, not fixed here

- lemon's spacing anchor is keyed `uf_ifas_hs1153` but points at HS402 (§2.3).
- plant-app's PLA-465 allowlist change exists on `feat/community-foundation` (cherry-pick `1cbf0c61`), not on `main`.
- Herb has no pot-size intent, so PLA-629's "Herb's ... pot-size intents read the picked value" has nothing to read
  into yet.
- USU's peach page makes a rootstock-conditional spacing statement on a crop whose rootstock rows are all
  non-size-controlling (§5.2).
