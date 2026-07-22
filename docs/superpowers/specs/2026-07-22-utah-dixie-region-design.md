# Utah "Dixie" high-desert region -- design spec

**Date:** 2026-07-22
**Kickoff:** roadmap item 11 (`docs/kickoffs/38-utah-dixie-region.md`).
**Base canonical:** `b1045e04` (Nevada high-desert region, LIVE via plant-astro `f948371`) /
`origin/main` `0af7fdf`. Rebase onto whatever is current at build start; the SHA-guard fails closed
on drift.
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md` (CONDITIONAL-GO;
built as a full region per Trevor's 2026-07-16 ruling that all Tier-2 belts are full regions).
**Template (reuse near-verbatim):** the **Nevada** arc
(`docs/superpowers/{specs,plans}/2026-07-21-nevada-high-desert-region*`,
`tools/staging/nevada_shard_guide.md`, `tools/staging/nevada_merge.py`) plus the region toolchain
(`region_harness` / `build_region_promote` / `region_cell_audit` / `second_cycle` /
`prose_window_sweep`). Utah is Nevada's near-twin -- "the Nevada arc, with the three deltas in
section 4." Structural content donor: the desert neighbors `low_desert_az` (Phoenix) / `warm_arid`
(Las Cruces). **NO new field, NO new gate.**

**Decisions confirmed with Trevor 2026-07-22 (brainstorming):**
1. Slug = **`utah_dixie`** (not `utah` -- the belt is only the 15-ZIP SW corner; northern Utah's
   Wasatch Front is z6-7 and stays `northern_tier`; naming it `utah` would mislead a Salt Lake user).
2. Apple + pear = **`marginal`, prose-only** (the marquee flip from Nevada's `fruits_reliably`).
3. Chill band = **hunt-once-then-flag** (one targeted St.-George chill-hour swing in the build; if
   none, ship the elevation-bracketed `[250,450]` with an explicit honest provenance flag).

## 1. Product goal
Author a real Utah "Dixie" region (`utah_dixie`, the SW-Utah St. George / Washington County belt) so
the belt stops riding generic zone dates that assume neither its real summer heat abort nor its real
late-fall frost return. Region label: **"Utah: St. George Dixie (Mojave-edge high desert)"**. Marquee
anchor St. George (z8b, 2,624 ft). Climatically the NE edge of the Mojave Desert -- it behaves like
Las Vegas (`nevada`) and Las Cruces (`warm_arid`), NOT like northern Utah. This is the **6th authored
region**, reusing the high-desert conventions (summer `heat_pause`, no fall reflush for warm crops),
not the humid-belt fall-reflush shape.

## 2. Scope + zone span (DECIDED)
Roster-wide (A31): all **111** certified region-carrying crops get a `utah_dixie` cell (same roster as
Nevada/mid-Atlantic/mid-South: ~82 frost_anchored annuals + ~14 chill_gated trees + ~5 evergreen
citrus + ~5 woody-ornamental herbs + ~4 berries + 1 strawberry). Count stays 128, 119 certified
unchanged -- a roster-wide column, not a new crop.

**zone_span `["8"]`** -- a **SINGLE zone** (the ruling's scope note is explicit: z8, 15 ZIPs, a mix of
8a Santa Clara / La Verkin and 8b St. George / Washington / Hurricane; the earlier "z8-9" was a stray
from an older pass). Simpler than Nevada's 3-zone span. **`warm_arid` (`["8"]`) is the structural
precedent**; A45 handles a single-zone span natively (add `EXPECTED_SPANS.utah_dixie = ["8"]`, **no
`DONORS` entry** -- Utah is authored fresh, not zone-cloned). Washington County's higher-elevation
towns (Central, Enterprise, New Harmony at 5,300+ ft; Pine Valley at 6,527 ft) are colder zones
OUTSIDE this z8 belt -- a fact that drives the apple finding in delta 4b.

## 3. Frost anchor (single zone)
Frost-anchored (`resolution_method="frost_anchored_resolved"`; a real winter frost, NOT frost-free
like RGV/Hawaii). **z8 anchor: last frost Mar 30 / first frost Nov 1** (USU Extension Washington
County, "Elevations for Washington County," 2020; the St. George row is marked as Utah Climate Center
*actual-record* data, not elevation-interpolated -- verbatim `*St. George 2624 3/30 11/1`, ~210-day
frost-free season, "often over 100 degrees in June, July, and August"). Cross-confirmed by a second
independent USU document ("Suggested Vegetable Planting Dates for Utah": "the average last spring frost
in St. George occurring on March 30"). One zone = **no gradient derivation needed** (the single biggest
mechanical simplification over Nevada's 3-zone gradient). An older 2008 USU doc gives a slightly more
conservative Oct 23 / 196-day figure; the 2020 actual-record figure is primary, the 2008 one noted as
directionally-consistent secondary.

## 4. The three deltas from Nevada (the important part)

### 4a. Warm annuals: same shape as Nevada, but NO early-Feb-indoor-start trick
Same high-desert shape as Nevada: **SINGLE spring window + summer `heat_pause`** (Jun-Aug, USU's
>90-95degF blossom/fruit-set abort: ">95degF day / <50degF night" tomato set failure, ">90degF" early
fruit-set abort) **+ NO fall replant** (USU's own St. George fall guidance is cool-season only -- no
fall tomato mentioned in any USU St. George document) **+ a real late-fall `cold_pause`** (frost
returns Nov 1).

**KEY MECHANICAL DIFFERENCE from Nevada:** Utah's last frost (Mar 30) is late enough that January is
**naturally inactive** (`start_indoors` late Feb), so the deriver renders the honest winter
`cold_pause` on its own. Utah does **NOT** need Nevada's "author the indoor start in early February"
workaround (that was specific to Nevada's Feb 28 frost triggering the deriver's January-active
cold_pause suppression). The ruling confirmed this by actually running `derive_annual_calendar` for
St. George: the naive winter is a flat `cold_pause`, mid-Atlantic/mid-South-shaped, not Nevada's
all-`growing` back half. Tomato `plant_out` ~Apr 1 (USU "Suggested Vegetable Planting Dates," Group D
"Very Tender") -- tighter/later than Nevada's mid-March. The 6 authoring shapes (A fruiting / B
quick-two-window / C heat-lovers-no-pause / D warm herbs / E cool two-window / F fall alliums) carry
over unchanged. Cool-season annuals keep the desert **two-window** shape (spring + fall, USU's St.
George fall cool-season window: broccoli/cabbage/cauliflower/lettuce/carrots/spinach/onions/turnips/
beets), built with `tools/second_cycle.py` (combine-derive-then-split, A43-safe).

### 4b. Trees: apple + pear MARGINAL (the marquee flip from Nevada -- confirmed)
The Washington County Extension "Fruits" page splits recommendations by elevation:
- **Low elevation (St. George / the z8 belt) -- thrive -> `fruits_reliably`:** **apricot, cherry
  (sweet + sour), fig, peach, nectarine, plum, persimmon, pomegranate, mulberry, grape** (plus nuts --
  almonds/pecans/pistachios, not in roster). Classic low-chill desert fruit; a clean sourced list (no
  Nevada-style per-tree agonizing).
- **Higher elevation ONLY (5,300+ ft, OUTSIDE the z8 belt): apple, pear, raspberry, blackberry** -> so
  for the z8 core, **apple + pear-asian + pear-european = `marginal`** (the county's own office does
  not recommend apple for the St. George core, listing it only for its colder higher-elevation towns).
  St. George's 2,624 ft brackets between `low_desert_az` (Phoenix `marginal`, ~1,100 ft) and
  `warm_arid` (Las Cruces `fruits_reliably`, ~3,900 ft), landing **closer to the marginal/Phoenix
  end**. Only the lowest-chill third crops (Dorsett Golden 100, Anna 200, Ein Shemer 100); the mid/
  high-chill varieties do not. `chill_basis_beginner`/`chill_basis_seasoned` prose says exactly that
  (the `low_desert_az` "high-chill varieties never fruit here" idiom) -- **prose-only steer, NO new
  field**. This inverts Nevada, where the UNR SP-20-07 North Las Vegas field trial confirmed apple
  `fruits_reliably`; St. George has no equivalent trial and its county office positions apple as a
  higher-elevation crop.
- **pawpaw `unsuitable`** (humid-forest tree, arid mismatch -- same as Nevada).

### 4c. Raspberry (+ blackberry): marginal, fall-bearing/low-chill steer
"Utah's Dixie" IS named by USU ("Raspberry Management for Utah") as fall-bearing-raspberry territory
("in Utah's Dixie, fall-bearing raspberries tend to be better adapted, as the fruit ripens after the
hottest part of the summer is over"), but **MARGINAL**: the belt's hot, low, alkaline sites need
heat-tolerant, low-chill, FALL-BEARING/primocane cultivars (Bababerry 250, Dorman Red 300, Caroline/
Autumn Bliss/Heritage/Anne), NOT the canonical's dominant ~800hr floricane mainstream. This is the
**SAME steer this dataset's own `warm_arid` raspberry `region_notes_seasoned` already carries** ("hot,
low, alkaline-soil sites are marginal and need heat-tolerant, low-chill everbearing types") -- read it
and mirror it. **Prose-based steer** (raspberry is not yet on the `berry` variety archetype, so no
`bearing_habit` field; that crop-wide migration is a separate future arc, OUT OF SCOPE -- see section
10). Blackberry likewise marginal (higher-elevation column). Blueberry very-marginal (alkaline soil,
container-only honesty in prose). **Strawberry a low-elevation THRIVER** (USU lists it in the
low-elevation "Fruits" column -- a cleaner positive verdict than Nevada's fall-set-only annual).

### 4d. Onion/shallot A9 (the watch, same as Nevada) + garlic
St. George ~37degN (slightly north of Las Vegas ~36degN). `recommended_day_length_type` =
**`intermediate_day`**, **fall-planted** (sets in fall -> spring harvest, never April+) -> A9
photoperiod window-fit satisfied by construction (intermediate/short-day forbids a spring `plant_out`;
memory `onion-daylength-intermediate-a9-window-fit`). **VERIFY A9 = 0 explicitly in the build.**
Shallot follows onion by species identity. **Garlic** gets its own USU St. George fall clove window
(source the exact window from the USU fall-gardening / vegetable-date pages; likely Sep-Oct like
Nevada), harvest the following early summer.

## 5. Chill band + the honest gap (hunt-once-then-flag)
`region_chill_delivered.utah_dixie = {"8":[250,450]}` -- Phoenix-bracketed inference (verify the
CURRENT canonical `low_desert_az` / `warm_arid` bands at build time to anchor the bracket precisely;
St. George's 2,624 ft sits above Phoenix ~1,100 ft, below Las Cruces ~3,900 ft, so the band leans to
the Phoenix/marginal end).

**OPEN GAP (honest, from the ruling):** no USU-published numeric chill-hour figure for St. George /
Washington County was found despite a genuine multi-source search (the ruling checked USU's apple/peach
variety pages, the Utah Climate Center station network including its FGNET fruit-growth network, and
the Washington County apple variety page). **Hunt-once-then-flag (Trevor-confirmed):** the build takes
**ONE** more targeted swing at a real St.-George-specific chill-hour number (Utah Climate Center FGNET
Washington County station) before settling the band. If a T1 number surfaces, use it. If none does,
ship `[250,450]` with an explicit `region_chill_delivered_provenance.utah_dixie` flag stating it is
**elevation-bracketed inference between the two existing z8/z9 desert regions, not a measured figure**
-- the honesty-over-false-precision convention. The `marginal` apple verdict (4b) does not depend on
the exact number; it is anchored by the county Extension's own elevation-based recommendation.

## 6. Class split (all T1: USU Extension `usu_ext`)
- **~82 frost_anchored annuals**, split by season: **warm crops** (tomato/pepper/eggplant/squash/
  melon/cucumber/beans/corn/okra/sweet-potato...) get delta-4a's single-spring + heat_pause + no-fall +
  Nov 1 cold_pause; **cool crops** (lettuce/brassicas/roots/peas/greens/spinach...) keep the desert
  two-window spring + USU-St.-George-fall shape (via `second_cycle`).
- **~14 chill-gated trees.** apple + pear-asian + pear-european `marginal` (delta 4b, prose steer);
  apricot/cherry-sweet/cherry-sour/fig/peach/nectarine/plum/persimmon/pomegranate/mulberry
  `fruits_reliably` (low-elevation column, re-judged arid: late frost + sunburn not humid brown-rot);
  pawpaw `unsuitable`. Exact per-tree calls resolved in the build from each tree's
  `chill_hours_required` vs the band + the county's low/high-elevation list.
- **~5 citrus.** St. George is a cold-limited desert winter (colder than Phoenix on winter nights),
  so citrus is `marginal` / `survives_no_fruit` (container/protected); re-judged fresh, not cloned
  from Phoenix's warmer verdict (the Nevada convention).
- **~5 woody herbs.** Desert-adapted: lavender/rosemary/thyme/oregano/sage thrive in arid heat +
  alkaline soil (the `warm_arid`/`low_desert_az`/`nevada` strength).
- **~4 berries.** raspberry/blackberry `marginal` (delta 4c, fall-bearing/low-chill prose steer),
  blueberry very-marginal (alkaline, container-only honesty in prose -- berries carry no suitability
  field so honesty lives in prose, A32 still forces a calendar), **strawberry a low-elevation thriver**
  (delta 4c).
- **Onion/shallot (the A9 WATCH):** delta 4d -- `intermediate_day`, fall-planted, A9 = 0 verified.

## 7. Build / verification
Reuse `tools/region_harness.py` / `tools/build_region_promote.py` / `tools/second_cycle.py` /
`tools/prose_window_sweep.py`, cloning `tools/staging/nevada_merge.py` -> `utah_dixie_merge.py` and the
`nevada_shard_guide.md` -> `utah_dixie_shard_guide.md`. **`low_desert_az` / `warm_arid` are the
STRUCTURAL donors** for annual/herb cell shape (heat_pause placement, `calendar[]` shape, `plantings`/
`resolved_by_zone`/provenance structure); **windows are re-authored from USU sources**, re-anchored to
the St. George frost dates (Mar 30 / Nov 1), and delta 4a applied (single spring window for warm crops;
cool crops keep two windows via `second_cycle`). **Trees + citrus + the marginal apple are authored
fresh** (Nevada's `fruits_reliably` apple / its warmer-anchored calls cannot be transformed into Utah's
`marginal` apple). SDD build: controller authors the delta reference cells (apple `marginal`, the tree
low/high-elevation split, raspberry fall-bearing steer, garlic/onion Shape F + A9), validating the
toolchain + a `staging/utah_dixie_sources.json` injection, then family-shard authoring + prose-honesty
fan-out writing DISJOINT staging files, controller-merged behind a structural-identity guard (no
per-subagent commits -- parallel-safe), then `prose_window_sweep` (prose-vs-resolved date honesty) + an
independent opus content review before promote. Atomic SHA-guarded single splice: 111
`regions.utah_dixie` cells + `region_chill_delivered.utah_dixie` +
`region_chill_delivered_provenance.utah_dixie` + provenance replace-append + any new `source_catalog`
adds (section 8). **NO new gate, NO new field:** reuses A45 (`+utah_dixie` in `EXPECTED_SPANS`), A3
(`perennial_gate` tree no-fruit split), A31/A32 (`coverage_floor`), A43 (second-planting comma-storage
forbid), A9 (`photoperiod_gate`), `chill_gate`, `calendar_coherence`.

**Gate ceremony (protocol #6, before promote):** `whole_crop_gate` 18/18 (spot) + `tools/gate_all.py`
119/119 + A9 (onion/shallot 0/0) + A45 (0) + `chill_gate` (0) + `calendar_coherence` (0) + A43 (0) +
`prose_window_sweep` (0) + `release_verify` (B-H clean; section-A collateral is the documented
roster-wide single-crop-pilot false positive, the pre-commit backstop binding) + a footprint byte-audit
(EXACTLY the 111 `regions.utah_dixie` cells + the chill band + provenance + any source adds; 0 other
crops changed; no top-level keys added/removed beyond the region entries; count 128; COMPACT, 0
escaped-unicode). Scratch dry-run first, with A45/A43/A9 RED-checks proven on a scratch copy.

## 8. Sourcing -- lighter than Nevada
**`usu_ext` (Utah State University Extension) is ALREADY catalogued** and covers the whole USU family,
so unlike mid-South/Nevada this may need NO new `source_catalog` entries. For provenance precision the
build registers a **small set of per-pub sub-IDs under `usu_ext`** for the load-bearing pubs (the
`unr_sp2007`-under-`unr_ext` pattern Nevada used), resolving exact granularity at build by inspecting
`source_catalog`'s USU structure -- or, if that structure prefers a single family id, cites `usu_ext`
generically. The T1 pages (all `extension.usu.edu`; PDFs re-extract cleanly with `pypdf`, no image
render needed):
- "Suggested Vegetable Planting Dates for Utah" -- St. George tomato transplant Apr 1 (Group D); the
  per-crop planting-date table (the load-bearing window source, the USU analog of Nevada's UNLV chart).
- "How to Grow Tomatoes in Your Garden" -- heat abort thresholds; no fall tomato.
- "Fall Gardening in the St. George Area" (Heflebower) -- the fall cool-season window.
- "Fruits" (Washington County) -- the elevation fruit split (delta 4b).
- "Raspberry Management for Utah" -- names "Utah's Dixie" (delta 4c).
- "Elevations for Washington County" (2020) -- the frost anchors (section 3).

T1-or-it-does-not-ship: every authored window/verdict traces to a USU page; non-T1 aggregators
(fruittreehub etc.) are directional corroboration only, NOT registered.

## 9. Release + handoff
State trio at release: regenerate `CURRENT_STATE.md` (`tools/gen_current_state.py`, then fill prose
slots -- watch the no-`---`-separator drift, memory `current-state-md-drift`), append `STATE_HISTORY.md`
(most-recent first), bump `LATEST.txt` (SHA + session). Field-addition register **row 22**; roadmap
item 11 -> SHIPPED. **Trevor confirms the push.** The plant-astro submodule bump is a SEPARATE later
step owned by the plant-astro session (memory `plant-astro-bump-owned-by-astro-session`) -- not run
from here. Paired app handoff owed: a plant-app kickoff (next number) --
`REGION_STATES.utah_dixie = ['UT']` + a **ZIP3 fence to the St. George Washington County ZIP3s (847xx)
ONLY**, so the Wasatch Front (Salt Lake 840/841, Provo 846, etc., z6-7) does NOT resolve to the Mojave
calendar and stays `northern_tier` (confirm exact 847xx membership vs `zip-zones.json`). **NO isWarm
#32 dependency** -- the whole belt is z8 (isWarm), so it resolves on the standard warm path as soon as
the fence lands (same as Nevada, unlike the mid-Atlantic/mid-South z7 halves).

## 10. Out of scope
- No new field, no new gate, no new archetype.
- No plant-astro bump (separate session).
- The **raspberry -> `berry` variety-archetype migration** (populating the reserved `cane`/`bush`
  branches with per-variety `bearing_habit`/chill so the fall-bearing steer becomes structured data) --
  a crop-wide arc touching raspberry/blackberry/blueberry across ALL regions, not just `utah_dixie`.
  Utah gets the accurate PROSE steer now (delta 4c). **Sequenced directly after the region program --
  immediately after Alaska (item 7) -- per Trevor 2026-07-22:** it is the ONE variety arc that is
  region-entangled (its fall-bearing/low-chill steer is authored as region prose in `warm_arid`/
  `utah_dixie`/etc.), so it runs after all region prose is settled rather than concurrently with the
  region builds.
- The 2 pre-existing shallot per-variety `day_length_type` tensions (memory `shallot-variety-dtm-held`).
