# Kickoff: Utah "Dixie" high-desert region (roadmap item 11)

**For:** a fresh plant-dataset build session (spec -> plan -> build, the region-column arc).
**From:** the Nevada region session (item 10). Utah is Nevada's near-twin -- build it as "the Nevada
arc, with the deltas in section 4."
**Base canonical:** `b1045e04` (dataset `origin/main` `0af7fdf`, Nevada live). Rebase onto whatever is
current at build start; SHA-guard fails closed on drift.
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md` (CONDITIONAL-GO;
built as a full region per Trevor's 2026-07-16 ruling that all Tier-2 belts are full regions).
**Template (reuse verbatim):** the Nevada arc --
`docs/superpowers/{specs,plans}/2026-07-21-nevada-high-desert-region*`, `tools/staging/nevada_shard_guide.md`,
`tools/staging/nevada_merge.py`, and the region toolchain (`region_harness` / `build_region_promote` /
`region_cell_audit` / `second_cycle` / `prose_window_sweep`). **NO new field, NO new gate expected.**

## 1. What it is
A real Utah "Dixie" region across all **111 certified region-carrying crops** -- the SW-Utah,
low-elevation St. George / Washington County belt (St. George, Washington, Hurricane, Ivins, Santa
Clara, La Verkin, Toquerville, all 2,600-3,700 ft). Climatically the NE edge of the Mojave Desert, so
it behaves like Las Vegas (`nevada`) and Las Cruces (`warm_arid`), NOT like northern Utah. The
6th authored region.

- **Slug (recommend `utah_dixie`, confirm with Trevor):** NOT `utah` -- the belt is only the 15-ZIP SW
  corner; northern Utah (the Wasatch Front, Salt Lake, z6-7) is a completely different climate and stays
  `northern_tier`. Naming it `utah` would mislead a Salt Lake user. The ruling itself calls it "Utah's
  Dixie." Region label e.g. "Utah: St. George Dixie (Mojave-edge high desert)."
- **`zone_span ["8"]`** -- a SINGLE zone (the ruling's scope note is explicit: z8, 15 ZIPs, a mix of 8a
  Santa Clara/La Verkin and 8b St. George/Washington/Hurricane; the earlier "z8-9" was a stray). This is
  SIMPLER than Nevada's 3-zone span. `warm_arid` (`["8"]`) is the structural precedent; A45 handles a
  single-zone span natively (add `EXPECTED_SPANS.utah_dixie = ["8"]`, no DONORS entry).

## 2. Frost anchor (single zone)
**z8: last frost Mar 30 / first frost Nov 1** (USU Extension Washington County "Elevations for
Washington County" 2020, marked as Utah Climate Center *actual-record* data for St. George
specifically; ~210-day frost-free season, "often over 100 degrees in June, July, and August").
Frost-anchored, `resolution_method="frost_anchored_resolved"`. One zone = no gradient derivation needed.

## 3. Sourcing -- LIGHTER than Nevada
**`usu_ext` (Utah State University Extension) is ALREADY catalogued** and covers the whole USU family --
so unlike mid-South/Nevada you may need NO new `source_catalog` entries (or, for precision, register a
few per-pub sub-IDs under `usu_ext`, the `unr_sp2007`-under-`unr_ext` pattern -- optional). The T1 pages
(all `extension.usu.edu`, PDFs re-extract cleanly with pypdf, no image-render needed):
- "Suggested Vegetable Planting Dates for Utah" -- St. George tomato transplant **Apr 1** (Group D), the
  vegetable planting-date table (the load-bearing per-crop window source, the USU analog of Nevada's
  UNLV chart).
- "How to Grow Tomatoes in Your Garden" -- heat abort: >95degF day / <50degF night; >90degF fruit-set
  abort. NO fall tomato mentioned.
- "Fall Gardening in the St. George Area" (Heflebower) -- the FALL cool-season window (broccoli/cabbage/
  cauliflower/lettuce/carrots/spinach/onions/turnips/beets), cool-season only.
- "Fruits" (Washington County) -- the elevation fruit split (section 4b).
- "Raspberry Management for Utah" -- names "Utah's Dixie" as fall-bearing-raspberry territory.

## 4. The deltas from Nevada (THE important part)

### 4a. Warm annuals: same shape as Nevada, but NO early-Feb-indoor-start trick
Same as Nevada: SINGLE spring window + summer `heat_pause` (Jun-Aug, USU's >90-95degF blossom abort) +
**NO fall replant** (USU's own St. George fall guidance is cool-season only, no fall tomato) + a real
late-fall `cold_pause` (frost returns Nov 1). **KEY MECHANICAL DIFFERENCE:** Utah's last frost (Mar 30)
is late enough that January is naturally inactive (`start_indoors` late Feb), so the deriver renders the
honest winter `cold_pause` on its own -- you do NOT need Nevada's "author the indoor start in early
February" workaround (that was specific to Nevada's Feb 28 frost triggering the January-active
cold_pause suppression; confirmed by the ruling running the deriver). Tomato `plant_out` ~Apr 1 (USU),
tighter/later than Nevada. The 6 authoring shapes (A/B/C/D/E/F) carry over unchanged; cool crops keep
the two-window spring + fall shape.

### 4b. Trees: apple + pear are MARGINAL (the sharpest delta from Nevada's fruits_reliably)
The Washington County Extension "Fruits" page splits by elevation:
- **Low elevation (St. George / the z8 belt): thrive** -> `fruits_reliably`: **apricot, cherry (sweet +
  sour), fig, peach, nectarine, plum, persimmon, pomegranate, mulberry, grape** (+ nuts -- almonds/
  pecans/pistachios, not in roster). Classic low-chill desert fruit.
- **Higher elevation ONLY (outside the z8 belt): apple, pear, raspberry, blackberry** -> for the z8 core,
  **apple + pear-asian + pear-european = `marginal`** (the county's own office does not recommend apple
  for the St. George core). St. George's 2,624 ft brackets between `low_desert_az` (Phoenix `marginal`,
  chill [250,400], 1,100 ft) and `warm_arid` (Las Cruces `fruits_reliably`, chill [400,700], 3,900 ft),
  landing **closer to the marginal/Phoenix end**. So only the lowest-chill third (Dorsett Golden 100,
  Anna 200, Ein Shemer 100) crops reliably; the mid/high-chill varieties do not. `chill_basis` prose
  says exactly that. **This is the marquee delta from Nevada, where apple was `fruits_reliably`.**
  `region_chill_delivered.utah_dixie = {"8":[250,450]}` (Phoenix-bracketed; a proposal -- see the open
  gap below). **pawpaw `unsuitable`** (humid-forest tree, arid mismatch -- same as Nevada).
- **OPEN GAP (honest, from the ruling):** no USU-published numeric chill-hour figure for St. George was
  found despite a genuine multi-source search. So the `[250,450]` band is elevation-bracketed inference,
  not a measured figure -- flag it honestly in the provenance, and a build session may attempt ONE more
  targeted chill-hour hunt (Utah Climate Center FGNET Washington County station) before settling it.

### 4c. Raspberry (+ blackberry): marginal, fall-bearing/low-chill steer
"Utah's Dixie" IS named by USU as fall-bearing-raspberry territory, but MARGINAL: the belt's hot, low,
alkaline sites need heat-tolerant, low-chill, FALL-BEARING/primocane cultivars (Bababerry 250, Dorman
Red 300, Caroline/Autumn Bliss/Heritage/Anne), NOT the canonical's dominant 800hr mainstream. This is
the SAME steer this dataset's own `warm_arid` raspberry `region_notes_seasoned` already carries ("hot,
low, alkaline-soil sites are marginal and need heat-tolerant, low-chill everbearing types") -- read it
and mirror it. Prose-based steer (raspberry is not yet on the `berry` archetype schema, so no
`bearing_habit` field -- that migration is a separate future arc, out of scope). Blueberry very-marginal
(alkaline), strawberry a low-elevation thriver (USU lists it in the low-elevation column -- likely a
better verdict than Nevada's).

### 4d. Onion/shallot A9 (the watch, same as Nevada)
St. George ~37degN (slightly north of Las Vegas ~36degN). `intermediate_day`, fall-planted (never
April+) -> A9 window-fit satisfied. Verify A9 = 0. Garlic gets its USU St. George fall window (check the
USU fall-gardening / vegetable-date pages for the exact clove window; likely Sept-Oct like Nevada).

## 5. App handoff (write the plant-app kickoff at release)
- `REGION_STATES.utah_dixie = ['UT']` + a **ZIP3 fence** to the St. George Washington County ZIP3s
  (**847xx**) ONLY -- the Wasatch Front (Salt Lake 840/841, Provo 846, etc.) is z6-7 and MUST stay
  `northern_tier`. Confirm the exact 847xx membership vs `zip-zones.json`. The z8 core is only 15 ZIPs
  (small -- smaller than Alaska's panhandle).
- **NO isWarm #32 dependency** -- the whole belt is z8 (isWarm), so it resolves on the standard warm
  path as soon as the fence lands (same as Nevada, unlike mid-Atlantic/mid-South z7 halves).

## 6. Process (same ceremony as Nevada)
Brainstorm/spec -> plan -> SDD build (controller reference cells for the delta crops -- apple `marginal`,
raspberry, the trees split -- then family shards, controller-merged, no per-subagent commits) -> full
gate ceremony (`gate_all` 119/119 + A45 + `chill_gate` + A43 + A9 + `calendar_coherence` +
`prose_window_sweep` + byte footprint) + scratch dry-run with A45/A43/A9 RED-checks + independent content
review -> state trio + roadmap item 11 SHIPPED + register row 22 -> commit UNPUSHED (Trevor confirms
push) -> plant-astro bump is a SEPARATE step after the push. Expect NO new field, NO new gate.

## 7. Why Utah is a lighter build than Nevada
Single zone (no gradient), sources already catalogued (usu_ext), the low-elevation fruit list is cleanly
sourced (no per-tree agonizing), the frost date avoids Nevada's January-active deriver quirk, and the
whole 6-shape + toolchain scaffolding already exists. The real authoring judgment concentrates in three
places: apple/pear `marginal` + the honest chill-band gap (4b), the low-elevation tree split (4b), and
the raspberry fall-bearing steer (4c). Everything else clones Nevada.
