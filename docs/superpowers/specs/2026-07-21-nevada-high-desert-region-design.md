# Nevada high-desert region -- design spec

**Date:** 2026-07-21
**Kickoff:** roadmap item 10 (`docs/region_coverage_roadmap.md`).
**Base canonical:** `a071f0c1` (the onion/shallot day-length correction) / `origin/main` `25b561e`
(already LIVE via plant-astro `1cd4aa3`).
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md` (CONDITIONAL-GO,
broader than mid-Atlantic/mid-South; built as a full region per Trevor's 2026-07-16 ruling).
**Template:** the mid-South arc (`docs/superpowers/{specs,plans}/2026-07-20-mid-south-region*`) for
process/tooling/gate ceremony, but the CONTENT donor is the **desert** neighbor `low_desert_az`
(Phoenix), not a humid belt. This is "the roster-wide region column arc, high-desert archetype, with
the three deltas in section 3." Task structure, gate ceremony, and A9/A43/A45/chill verification apply.

## 1. Product goal
Author a real Nevada high-desert region (`nevada`, Las Vegas Valley / Clark County) so the belt stops
riding generic frost-anchored zone dates whose flat back half is not merely incomplete but actively
misleading: the naive single-cycle calendar shows `growing` straight through the Jun-Sep >90degF
fruit-set abort AND through the real Nov 25 frost return. Region label: **"Nevada: Mojave High Desert
(Las Vegas Valley)"**. Marquee anchor North Las Vegas / Las Vegas (z9). This is a genuinely different
climate archetype from the four prior belts (high desert, not humid; extreme diurnal swing; a real
winter chill season), so it reuses the desert conventions (summer `heat_pause`), not the humid-belt
fall-reflush shape.

## 2. Scope + zone span (DECIDED)
Roster-wide (A31): all **111** certified region-carrying crops get a `nevada` cell (same roster as
mid-Atlantic/mid-South: ~82 frost_anchored annuals + ~14 chill_gated trees + ~5 evergreen citrus +
~5 woody-ornamental herbs + ~4 berries + 1 strawberry). Count stays 128, 119 certified unchanged --
a roster-wide column, not a new crop.

**zone_span `["8","9","10"]`** (3-zone; the same shape `se_gulf` already carries, so A45 handles it
natively -- one-line `EXPECTED_SPANS.nevada = ["8","9","10"]` add, **no `DONORS` entry** because
Nevada is authored fresh, not zone-cloned from a donor zone). Decided from the ruling's ZIP
distribution: **z9 94 ZIPs (dominant, Las Vegas Valley), z8 15 ZIPs (cooler/higher pockets), z10 1
ZIP (Laughlin/Colorado-River corner, rides the belt verdict)**. Reno and northern Nevada are z6b-7b
(2023 USDA map) and are NOT in this belt -- they stay `northern_tier`; the app-side ZIP3 fence keeps
them off the Mojave calendar (section 8).

## 3. The three deltas from the desert neighbors (`warm_arid` / `low_desert_az`)
1. **Warm-season annuals: single spring window + summer heat_pause, NO fall reflush.** The desert
   donor (`low_desert_az` cherry-tomato) encodes a TWO-window calendar --
   `[...harvest, harvest, heat_pause, heat_pause, plant, growing, harvest, harvest]` -- a spring crop,
   a summer `heat_pause`, AND a Sep-planted fall crop harvesting into December (succession_id 2,
   `planting_note: multi_season`). **Nevada deletes succession 2 for warm crops**: UNR explicitly does
   not recommend a fall tomato cycle for Southern Nevada (SP-99-11; the UNLV Master Gardener chart
   shows no fall tomato shading). Instead: a **widened single spring succession** (mid-Mar through late
   May, per UNR SP-99-11 / FS-02-61 / the UNLV chart -- a real ~2.5-month succession, wider than the
   naive 2-week window), the summer **`heat_pause`** (Jun-Sep, UNR's >90degF-day / <55degF-night
   fruit-set cutoff), then a **`cold_pause`** approaching the Nov 25 frost. **Cool-season annuals keep
   the desert two-window shape** (spring Feb-Apr + fall mid-Aug-Oct, UNR cool-season, heat_pause
   between) -- for cool crops the fall window is when they thrive, so it stays; use
   `tools/second_cycle.py` for those (combine-derive-then-split, A43-safe).
2. **Apple (Option A, Trevor-confirmed 2026-07-21).** Apple stays crop-level `fruits_reliably`
   (confirmed by the UNR North Las Vegas Research Orchard field trial SP-20-07, the strongest possible
   evidence, running counter to any "hot desert = chill-starved" assumption). But the variety list is
   NOT uniformly confirmed, so `regions.nevada.chill_basis_beginner`/`chill_basis_seasoned` do the
   steering (prose-only, NO new field -- the `low_desert_az` "high-chill varieties never fruit here"
   idiom):
   - **Named as reliable (trial-confirmed):** Dorsett Golden (Top Choice, 100hr), Pink Lady (Top
     Choice, trial 300-400hr), Mutsu (Top Choice, 500hr), Anna (Notable, 200hr), Fuji (Notable,
     <500hr), Granny Smith (Notable, 700hr -- the confirmed ceiling). Plus the safely low-chill set
     that sits under the confirmed range (Ein Shemer 100hr, Dolgo 500hr, Gala 600hr).
   - **Flagged as unproven for the Las Vegas Valley** (>=700hr, no local trial evidence): Zestar!
     (800), McIntosh (900), Empire (700), Honeycrisp (800), Golden Delicious (700), Jonagold (700),
     **plus Liberty (800, trial "under review"/inconclusive)**.
   - `region_chill_delivered.nevada = {"8":[500,900], "9":[300,700], "10":[150,450]}`. z9 is
     trial-anchored: Granny Smith (700hr) fruits (Notable Mention), so the confirmed ceiling is ~700;
     the flagged >=700hr tier sits at/above the band top. Sits between Phoenix `[100,400]` and
     `warm_arid` `[450,850]`, consistent with Las Vegas (~2,000 ft, colder winter nights) banking more
     chill than Phoenix (~1,100 ft) but less than NM high desert (~3,900 ft). z8 (higher/cooler) and
     z10 (Laughlin, warm-edge) are elevation-gradient derived off the z9 trial anchor and flagged as
     derived in `region_chill_delivered_provenance` (the honest mid-South intra-state-gradient idiom).
3. **Garlic: the real, narrower Sept-mid-Oct clove window.** The UNLV/UNR Master Gardener guide shows
   garlic shading only Sept (E/M/L) through Oct (early) -- a fall clove-set window closing 3-6 weeks
   earlier than `warm_arid` ("late September to November") or `low_desert_az` ("mid-September through
   November"). Do NOT inherit either neighbor's wider window verbatim; author Nevada's own Sep 1 - Oct
   15 window, harvest the following early summer.

## 4. Frost anchors + gradient
Frost-anchored (all three zones have a real winter frost; `resolution_method` frost-anchored, NOT
frost-free like RGV/Hawaii). **z9 anchor: last frost Feb 28 / first frost Nov 25** (NWS Las Vegas
Technical Memorandum WR-235, 1961-90 normals, T1 `.gov`). Warm-crop transplant windows are authored
to UNR's grower-facing guidance (mid-March, cited to UNR SP-99-11's "last frost date for Southern
Nevada is March 15" and the UNLV chart), not the raw meteorological mean -- the meteorological date is
the stored frost anchor, the extension's practical date drives the authored plant window (the same
"cite the extension quote, resolve to it" pattern the desert cells already use). **z8** (cooler/higher
pockets): last frost ~2-3 weeks later, first frost ~2-3 weeks earlier, gradient-derived off z9.
**z10** (Laughlin, warmest): last frost ~1-2 weeks earlier, first frost later, gradient-derived. z8/z10
are documented as gradient-derived (no direct z8/z10 Nevada station was in the ruling; a targeted T1
source hunt for a Mesquite/Pahrump z8 or Laughlin z10 normal happens in the build, else the gradient
derivation stands, honestly flagged).

## 5. Class split (all T1: UNR/UNCE Extension, UNLV Master Gardener, NWS)
- **~82 frost_anchored annuals**, split by season: **warm crops** (tomato/pepper/eggplant/squash/
  melon/cucumber/beans/corn/okra/sweet-potato...) get delta-1's single-spring + heat_pause + no-fall +
  Nov cold_pause; **cool crops** (lettuce/brassicas/roots/peas/greens/spinach...) keep the desert
  two-window Feb-Apr / mid-Aug-Oct shape.
- **~14 chill-gated trees.** Apple `fruits_reliably` + delta-2 variety steering. Other trees judged
  against the `[300,700]` z9 band: low/mid-chill pome & stone that clear it fruit; high-chill cherries
  and any tree above ~700hr flagged/marginal in prose; peach/apricot/nectarine bloom-frost + heat
  judged per-crop (Vegas is not the humid-East, so the brown-rot rationale does not carry -- these are
  re-judged from the arid-desert reality, likely `fruits_reliably` on chill but watch late frost).
  pomegranate/fig/persimmon/mulberry are desert-strong. Exact per-tree calls resolved in the build
  from each tree's `chill_hours_required` vs the band.
- **~5 citrus.** Las Vegas is COLDER than Phoenix (the trial evidence: colder winter nights), so
  citrus is MORE cold-limited here than in `low_desert_az` -- mostly `marginal` / `survives_no_fruit`
  (container/protected), the hardier mandarin/kumquat least bad, lime/grapefruit worst. Re-judged
  fresh, not cloned from Phoenix's warmer verdict.
- **~5 woody herbs.** Desert-adapted: lavender/rosemary/thyme/oregano/sage thrive in arid heat +
  alkaline soil (the `warm_arid`/`low_desert_az` strength).
- **~4 berries.** Blackberry/raspberry `marginal` (heat + alkaline soil), blueberry very-marginal
  (needs acid soil, hostile in the alkaline Mojave -- container-only honesty in prose; berries carry
  no suitability field so honesty lives in prose, A32 still forces a calendar), strawberry a
  cool-window annual.
- **Onion (the A9 WATCH):** desert onions are short-day / intermediate-day and **fall-planted**
  (clove/set Oct-Nov -> spring harvest), so no April-or-later `plant_out` -- A9's photoperiod
  window-fit rule (intermediate/short-day forbids a spring plant_out) is **naturally satisfied**.
  VERIFY explicitly in the build: `recommended_day_length_type` for `nevada` must be short_day or
  intermediate_day, and the `plant_out`/calendar must not place a spring set. (memory
  `onion-daylength-intermediate-a9-window-fit`.) Shallot follows onion by species identity. Garlic is
  delta 3.

## 6. Build / verification
Reuse `tools/region_harness.py` / `tools/build_region_promote.py` / `tools/second_cycle.py` /
`tools/prose_window_sweep.py`. **`low_desert_az` (Phoenix) is the STRUCTURAL donor** for annual/herb
cell shape (heat_pause placement, `calendar[]` shape, `plantings`/`resolved_by_zone`/provenance
structure); **windows are re-authored from UNR sources**, re-anchored to the Vegas frost dates, the z8
column added, and delta 1 applied (succession-2 removal for warm crops; cool crops keep two windows via
`second_cycle`). **Trees + citrus are authored fresh** (Phoenix's `marginal` apple and warmer citrus
verdicts cannot be transformed into Nevada's `fruits_reliably` apple / colder citrus). Subagent
family-shard authoring + prose-honesty fan-out writing DISJOINT staging files, controller-merged
behind a structural-identity guard (no per-subagent commits -- parallel-safe), then `prose_window_sweep`
(prose-vs-resolved date honesty) + an independent opus content review before promote. Atomic
SHA-guarded single splice: 111 `regions.nevada` cells + `region_chill_delivered.nevada` +
`region_chill_delivered_provenance.nevada` + provenance replace-append + the new `source_catalog` adds
(section 7). **NO new gate, NO new field:** reuses A45 (`+nevada` in `EXPECTED_SPANS`), A3
(`perennial_gate` tree no-fruit split), A31/A32 (`coverage_floor`), A43 (second-planting comma-storage
forbid), A9 (`photoperiod_gate`), `chill_gate`, `calendar_coherence`.

**Gate ceremony (protocol #6, before promote):** `whole_crop_gate` 18/18 (spot) + `tools/gate_all.py`
119/119 + A9 (onion/shallot 0/0) + A45 (0) + `chill_gate` (0) + `calendar_coherence` (0) + A43 (0) +
`prose_window_sweep` (0) + `release_verify` (B-H clean; section-A collateral is the documented
roster-wide single-crop-pilot false positive, pre-commit backstop binding) + a footprint byte-audit
(EXACTLY the 111 `regions.nevada` cells + the chill band + provenance + the source adds; 0 other crops
changed; no top-level keys added/removed beyond the region entries; count 128; COMPACT, 0
escaped-unicode).

## 7. Sourcing
Register the genuinely-new T1 `source_catalog` entries in-batch (the mid-South in-batch-adds pattern;
`region_harness` injects `staging/nevada_sources.json` into the scratch canonical so per-crop gating
sees the ids, `build_region_promote` emits the `add $.source_catalog.<id>` patches). Candidates:
- `nws_vef` -- NWS Las Vegas WR-235 "Climate of Las Vegas" (frost anchors Feb 28 / Nov 25).
- `unlv_mg_svn` -- UNLV-hosted "Vegetable Planting Guide for Southern Nevada" (Clarita Huffman, UNR
  Coop Ext Master Gardener) -- the warm/cool windows + the garlic Sept-mid-Oct window.
- `unr_sp2007` -- UNR SP-20-07 orchard fruit trial (the apple variety/chill evidence).
- UNR SP-99-11 ("Growing Tomatoes in Southern Nevada") + FS-02-61 ("Home Vegetable Production in
  Southern Nevada"): register as distinct ids OR ride the already-catalogued `unr_ext` family --
  resolved in the build by inspecting `source_catalog`'s UNR granularity. T1-or-it-does-not-ship: every
  authored window/verdict traces to one of these; the single Almanac.com cross-check is NOT registered
  (secondary aggregator, directional corroboration only).

## 8. Release + handoff
State trio at release: regenerate `CURRENT_STATE.md` (`tools/gen_current_state.py`, then fill prose
slots -- watch the no-`---`-separator drift, memory `current-state-md-drift`), append `STATE_HISTORY.md`
(most-recent first), bump `LATEST.txt` (SHA + session). Field-addition register row. **Trevor confirms
the push.** plant-astro submodule bump is a SEPARATE later step owned by the plant-astro session (memory
`plant-astro-bump-owned-by-astro-session`) -- not run from here. Paired app handoff owed: a plant-app
kickoff (next number) -- `REGION_STATES.nevada = NV` + a **ZIP3 fence** so northern-Nevada Reno/Carson
z6-7 ZIPs do NOT resolve to the Mojave `nevada` calendar (the mirror of RGV's 785xx and PNW's west-side
fences; Nevada's fence keeps `nevada` to the southern Clark County ZIP3s, 889/890/891 + Laughlin), and
a note that the small z8 tail's in-app delivery depends on the plant-app `isWarm` decoupling (kickoff
#32).

## 9. Out of scope
- No new field, no new gate, no new archetype.
- No plant-astro bump (separate session).
- The 2 pre-existing shallot per-variety `day_length_type` tensions (memory `shallot-variety-dtm-held`).
- Utah "Dixie" (roadmap item 11) -- shares Nevada's heat/frost-return gap shape and will reuse these
  conventions, but is its own arc.
