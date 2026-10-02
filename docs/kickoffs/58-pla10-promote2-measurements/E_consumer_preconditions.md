# Agent E: consumer measurement for PLA-10 promote 2 (READ-ONLY)

Measured 2026-10-02. Nothing edited, checked out, stashed or committed in any repo.

## Commits read
- plant-dataset: `main` @ 78d734b, canonical sha256 prefix `cf1d480d`.
- plant-app: read via `git show`, never checked out.
  - `f6fa8c8b` is local `feat/community-foundation`. That branch is **behind origin by 21**.
  - `origin/feat/community-foundation` == `feat/pla-614-feeding-the-soil` == **`1c464e2d`**, which contains f6fa8c8b. Its shipped bundle provenance is canonical cf1d480d / dataset 73b01aa.
  - Between f6fa8c8b and 1c464e2d, the only relevant-file changes are `planner/fit.ts` (+`rowGapEstimated`) and `planner/layout.ts` (+`anyGapEstimated`). Neither reads any promote-2 key. Every app file:line below therefore holds on both commits.
  - `main` (9c888c32) is an unrelated old line: merge-base == main tip, 3,015 commits behind. It has no `scripts/export-projection.mjs`, no `planting-layout.ts` and no planner. It reads none of these fields, so it is irrelevant here.
- plant-astro: `main` @ 54a8249. Its submodule is pinned at bc71f34, so astro sees promote 2 only at the astro-session bump.

## (a) apple `rootstock_options[].spacing_inches` + second source / anchoring key on 4 rows

Today's rows carry `sources: ['umd_ext']` + `anchoring_urls.umd_ext{url,verified}`, `spread_ft` 8/10/15/18/30, and no `spacing_inches`.

**(i) THROW: none.**
- App export: `rootstock_options` ships whole (`scripts/export-projection.mjs:79`). `prune` (`:174-192`) throws only on the 4 DROP_NAMES (`plantings_provenance`, `sources_pending_admission`, `uscrn_validation`, `source_quote`) outside their measured contexts. Row keys `spacing_inches` / `sources` / `anchoring_urls` are not among them. Do NOT add `source_quote` (or any DROP_NAME) inside a rootstock row or layout entry: that throws.
- Astro: `rootstock_options` is undeclared in `content.config.ts`, so it passes through `.passthrough()` (`:137`). `spacing_inches: null` on M26 is fine.

**(ii) RENDER WRONG: one hard coupling, plus a pre-existing proxy.**
- **Astro `pot-figure.ts:23-34` `isSourced`** requires EVERY id in a row's `sources` to have `anchoring_urls[id].url` as a non-empty string.
  - M9 and M26 show "pot OK, 20+ gal" (`rootstock-presence.ts:64-71`) and the container card's "20 gal pot" pick (`container-card.ts:106-116`, `sourcedRowGallons`) only while that holds.
  - If the second source lands without a `{url}` anchor keyed by the same id, both figures vanish silently. Today `isSourced` is unaffected because the promote adds both together.
  - Note also that row `sources` is a pool: astro treats any listed source as citing `container_size_gallons`.
- App planner `planner/rootstock.ts:43-57` `effectiveCrop`: a picked rootstock replaces spacing with `spread_ft * 12`. `planner/catalog.ts:86-99` `toRootstock` never copies the row's `spacing_inches`, so the new override is ignored. Planned vs new sourced figures:
  - seedling plans at 360 in vs [240,300]
  - M9: 96 vs [72,96]
  - MM106: 180 vs [144,192]
  - MM111: 216 vs [168,216]
  - M26: override null, so the app uses spread 10 ft = 120, not the crop [96,144]. That is the spec §5.1 fallback, but it is not labelled "modeled".
  - This behaviour already exists and the data does not regress it. Only seedling plans outside the new sourced range.

**(iii) SILENTLY IGNORED:**
- App `TreeRootstockCard.tsx:9-16,51` (height and bearing only).
- Astro `rootstock-presence.ts:41-48,117-130` (height, bears, container); astro `planner/catalog.ts:7,95-121` (no rootstock picker).

## (b) planting_layout support entries, `rows_per_bed`, entry `mature_height_ft`, support defaults, pea id

**(i) THROW: astro zod only, if the shape slips. App: none.**
- Astro `content.config.ts:19-31` `plantingLayoutEntry` accepts `support: enum(none|stake|cage|trellis)`, so the new values build. It is `.passthrough()`. Fields that are **NOT nullable**:
  - `in_row_inches`, `hill_spacing_inches`, `plants_per_hill` (numberPair, optional)
  - `rows_per_bed: z.number().int().optional()`
  - `mature_height_ft: numberPair.optional()`
- So writing `null` (rather than ABSENT) for `rows_per_bed`, an entry's `mature_height_ft`, or a non-carried pair **FAILS THE ASTRO BUILD**. The same applies to a non-integer `rows_per_bed`, a pair of length != 2, or an entry-level `row_spacing_reason` other than `not_authored`/null (`:28`).
- Spec §1.1 says absent, so this is a dataset-side guard to hold, not a consumer change.
- App: `planting_layout` ships whole (`export-projection.mjs:75`); no entry-key allowlist exists; the bundle is untyped (`guides-dataset.ts` `Record<string, unknown>`).

**(ii) RENDER WRONG: nothing wrong; one loss of meaning.**
- Every reader keys on `default === true` and `arrangement`, never on `support` or on the entry count:
  - App `planting-layout.ts:61-111,145-185`
  - Astro `planting-layout.ts:39-125`, `hero-spacing.ts:31-42`
- A support default (cherry-tomato `row-stake`) shows its `in_row_inches` as "between plants". That matches the gated mirror, so `spacing_inches`, `spacingLine` and `displaySpacing` agree. Sites:
  - App hero tile `at-a-glance.ts:126-138`
  - App facts `guide-facts.ts:79-84`
  - App `guide-chapters.ts:164`, which reads raw `spacing_inches` and so equals the mirror
  - App Herb canned answer `herb/canned.ts:32-45`
  - Astro `HeroCard.astro:198`, `CareGuideCard.astro:74`
- No consumer names the support. A staked default reads as a bare spacing, and "support required" (derived, §1.1) is shown nowhere.
- No consumer persists an entry `id` in either repo (grep: only test fixtures use `row-none`). A peas `row-none` -> `row-trellis` swap is consumer-safe today, ahead of PLA-629.

**(iii) SILENTLY IGNORED:**
- `rows_per_bed`, entry `mature_height_ft` and `support` are not on app `LayoutEntry` (`planting-layout.ts:31-43`) and are not read by astro.
- Herb is the one partial reader: `herb/slice.ts:12-35` passes the whole entry list (minus `anchoring_urls`) into LLM facts. Herb therefore sees `support`, `rows_per_bed` and the entry height override, but not crop-level `mature_height_ft`, which is absent from FACT_KEYS.

**Cost if a DEFAULT flips (cherry-tomato row-stake) and its figures differ from [24,36] / [60,72].** App tests pin cherry-tomato's live 36 in / [60,72] and would need re-measuring in the data commit:
- `FullnessMeter.test.tsx:9,20`
- `PlotDiagram.test.tsx:31,81,119,255`
- `RowsWindow.test.tsx:33,1096,1117,1159,2279`
- `CalculatorPane.test.tsx:1188,1469`
- `planner/fill-fractions.test.ts:119`
- `planner/fit.test.ts:197`
- `plot-calc.test.ts:336-337,413,1052,1124,1352`
- `herb/planner-tools.test.ts` (60 in row-minimum warning)
- `planting-layout.canonical.test.ts:41` (73 crops with a row figure) and `:58` (tally) whenever any default's row figure presence changes

If the stake default keeps identical numbers, only the canonical test's structural pins may move. Astro tests are fixture-only for layout (`planner/catalog.test.ts`, `planting-layout.test.ts`, `hero-spacing.test.ts`).

## (c) crop-root `mature_dimensions_sources` / `_anchoring_urls`; herbaceous `mature_height_ft` / `mature_spread_ft`

**(i) THROW: none.**
- App: both keys are already in `SHIP_TOP_LEVEL` (`export-projection.mjs:88-92`, classified ahead of time). `mature_height_ft` / `mature_spread_ft` are at `:62`.
- Astro: the sibling pair passes through. `mature_height_ft` / `mature_spread_ft` are `numberPair.nullable().optional()` (`content.config.ts:75-76`), and an `lo == hi` point is fine.

**(ii) RENDER: correct, with one cross-consumer divergence.**
- App `planting-layout.ts:200-210` `dimensionWords`: hi < 3 ft renders inches **rounded to whole inches**. It feeds:
  - the HEIGHT tile `at-a-glance.ts:145-150`, now on herbaceous crops
  - Facts Height/Spread `guide-facts.ts:85-86,99-100`
- Astro `mature-size.ts:16-26` `matureRangeText`: hi < 3 ft renders inches to **one decimal** ([1.5,2.9] -> "18 to 34.8 inches", where the app says "18-35 in"). It feeds the container card's "Mature size" row `container-card.ts:156-160,287-299`, which renders on every crop with `container_notes` (not a hero tile; spec §11's "container-card.ts:168-169 sizeRange" is stale).
- Broccoli's 47 in point reads "3.9 ft" in both.
- The divergence matters only for non-whole-inch sub-3-ft values. Author sub-3-ft ranges as whole inches / 12 to avoid it.
- No tile cap exists in the app (`at-a-glance.ts:190-242`), so an added HEIGHT tile pushes nothing off.

**(iii) SILENTLY IGNORED:**
- The `mature_dimensions_*` pair is read by no consumer: no generic `*_sources` walker in either repo, and astro's sourced-figure gate (`pot-figure.ts`) does not cover heights.
- Herb FACT_KEYS (`herb/slice.ts:12-24`) has no `mature_height_ft` / `mature_spread_ft`, so Herb cannot answer "how tall" from data.
- Dataset-side note: consumers read only crop-level height, so an entry override on the DEFAULT entry would never be seen. Keep crop-level = default-entry height (spec §4.1).

## (d) `verification_status.open_findings[].summary` appends
No consumer reads it.
- App: `export-projection.mjs:113-118,207-214` prunes `verification_status` to `status` / `source_set` / `date`, so the guides.dataset bytes do not move from (d) alone.
- Astro reads only `.status` (`built-crops.ts:7` and the pages).

## App tests that read the live bundle and pin promote-2-sensitive values
All read `assets/data/guides.dataset`, so they move only on the app re-export.
- `src/lib/planting-layout.canonical.test.ts:22-78`
  - 121 lists; 113 placeable at equal spacing; `:41` 73 with row figure; `:58` tally `row/null 73, not_authored 40, not_applicable 8`; `:63` hills = pumpkin, watermelon; `:76` 107 row defaults
  - Moves if any default changes its row-figure presence or arrangement. Support entries stay `row`, so `:76` holds.
- `src/lib/at-a-glance.layout.test.ts:68-83`
  - thyme / apple height pins (woody: backfill adds only the sibling pair, so the values hold)
  - `:80` carrot "no height (105 of 121 today)": carrot has 0 candidates per spec §4.4, so it holds, but the title count goes stale
- Cherry-tomato pins (list in (b)): only if its default's figures change.
- `src/lib/planner/rootstock.test.ts`, `BedCropSheet.test.tsx:181,275` pin apple crop [96,144]; unaffected unless crop-level apple spacing changes.
- `src/lib/herb/spacing-intent.test.ts:94` sweet-corn slice equals the full entry list. It moves only if sweet-corn entries change.
- `src/components/guides/TreeRootstockCard.test.tsx:19-22` uses live apple rows; tolerant of new keys.
- No test pins rootstock row key sets. No snapshot files exist (0 `__snapshots__`).
- Astro: `pot-figure.test.ts:100-126` reads live apple M9 and requires it cited ("pot OK, 20+ gal"). It holds iff the isSourced coupling in (a) holds. That is checked at the astro bump.

## Preconditions

**HARD (must land / hold before the data):**
1. Dataset-side shape guards for the astro zod schema (no consumer change needed, but a slip fails the astro build):
   - never emit `null` for an entry's `rows_per_bed`, `mature_height_ft`, `in_row_inches`, `hill_spacing_inches` or `plants_per_hill`: absent only
   - `rows_per_bed` must be an integer
   - every pair must have length exactly 2
   - `support` must stay in the 4-value enum
2. Every new rootstock-row source id carries `anchoring_urls[id].url`, or astro silently drops M9/M26's 20-gal figure (`pot-figure.ts:23-34`).
3. Do not introduce any app DROP_NAME (`source_quote`, etc.) inside new entries or rows (`export-projection.mjs:180-185` throws).
4. If any DEFAULT flips to a support entry with different figures (cherry-tomato), the app data commit must re-measure the cherry-tomato suites listed in (b) plus `planting-layout.canonical.test.ts`. That is a test re-measure, not a code precondition.
5. No consumer code change is required to BUILD:
   - app: SHIP already has `mature_dimensions_*`; no entry allowlist
   - astro: schema already admits support values, `rows_per_bed`, entry height and nullable crop heights

**SOFT (render improvements; data can land without them):**
- (a) App: read `picked_rootstock.spacing_inches ?? spread proxy` (`planner/catalog.ts:86-99` + `rootstock.ts:51-55`) and label the proxy as modeled. Today seedling over-plans at 360 vs [240,300].
- (a) Astro: no rootstock spacing surface (none exists).
- (b) Name the support on spacing surfaces ("staked", "on a trellis") and surface "needs support" (derived) in both repos. Today it is invisible except to Herb's LLM facts.
- (b) Consumers ignore `rows_per_bed` and entry height overrides. Optional PLA-629 picker work.
- (c) Unify the sub-3-ft inch rounding: app integers vs astro one decimal.
- (c) Add `mature_height_ft` / `mature_spread_ft` to Herb FACT_KEYS (`herb/slice.ts:12-24`).
- (c) Astro has no hero height tile. The height shows only in the container card row.
- (c) Refresh the at-a-glance.layout.test.ts:80 title count "105 of 121".
- (d) Nothing.
