# RGV / subtropical-TX region -- design spec

**Date:** 2026-07-13
**Status:** DRAFT (pending Trevor review)
**Kickoff:** `docs/kickoffs/25-rgv-subtropical-tx-region.md` (roadmap item 3)
**Base canonical:** `7e29f4f4` / dataset `main` `a32e5ed` (pushed, clean)
**Method:** the column GS-arc (`docs/gs_cross_crop_field_addition_v0.md`) -- a new region is a
roster-wide column added across every certified region-carrying crop.
**Sequencing:** the LEEK variety pilot (`leek-variety-hardiness-archetype-ready`) rebases onto
whatever canonical RGV lands at; two sessions must not both hold the canonical open (sweet-corn
collision rule). Concurrency confirmed clear at kickoff (2026-07-13).

## 1. Product goal

A gardener in McAllen, Brownsville, Harlingen, Weslaco, or Edinburg types their ZIP and gets
planting dates authored for **their** climate -- a frost-free subtropical winter-vegetable valley --
instead of the Georgia/Louisiana Gulf-coast calendar they ride today. This retires the last Tier-1
gap still on borrowed data (the 2026-07-12 zone-span reconciliation shipped RGV as an explicit
interim: the 95 TX z10 ZIPs match se_gulf because TX is in se_gulf's state mapping and se_gulf was
widened to z10). Shipping a real RGV region closes roadmap item 3 and unblocks the plant-app TX
z10 ZIP3-fencing decision.

## 2. Why RGV needs its own region (not a se_gulf stretch)

The Lower Rio Grande Valley (Hidalgo / Cameron / Willacy / Starr counties) is climatically distinct
from the se_gulf belt:

- **Frost-free.** se_gulf's z10 row -- the row RGV rides today -- literally asserts
  `resolved_from: {last_frost: "Jan 31", first_frost: "Dec 15"}`. Those are Gulf-coast frost dates.
  The RGV rarely frosts; anchoring a Valley calendar to a Dec 15 first frost is simply wrong.
- **Inverted calendar.** Cool-season crops (lettuce, spinach, brassicas, peas, roots, cool herbs)
  are **winter** crops; the brutal summer is a planting gap. Warm-season crops run a very long
  season split spring + fall around a mid-summer pause.
- **Near-zero chill.** Temperate tree fruit that needs real winter chill does not fruit here; this
  is where the A3 no-fruit split and the `region_chill_delivered.rgv` band do their work.
- **Citrus country.** The RGV is one of the premier citrus regions in the United States (the Texas
  Ruby Red grapefruit is a Valley crop). Our evergreen citrus should carry authoritative RGV
  fruiting calendars, not a generic warm cell.

se_gulf's z8-9 dates were authored for Georgia/Carolina/Louisiana. They are directionally survivable
but not honest for the Valley -- exactly why the reconciliation shipped RGV as an interim rather
than a real answer.

## 3. Scope decision (Trevor-approved 2026-07-13): Option A -- full roster-wide

`coverage_floor_gate` A31 requires every non-indoor certified crop to carry the full region roster,
and that roster is derived from `zone_span_gate.EXPECTED_SPANS` (2026-07-12). The moment `rgv` is
added to `EXPECTED_SPANS`, all 108 certified region-carrying crops need an `rgv`
`resolved_by_zone` cell or A31 fails them. Trevor ruled **Option A (full roster-wide)** over a
partial/opt-in region (which would reintroduce borrowed-data-under-a-real-region-label -- the exact
dishonesty this arc exists to retire) or a phased launch.

**Why A is tractable (not 108 greenfield anchors).** The roster splits cleanly by `calendar_basis`,
and the model already does the hard parts (the calendar deriver, the frost-free resolution
convention, the A3 no-fruit split all exist):

| Crop class | Count | RGV reality | Gate floor | Authoring weight |
|---|---|---|---|---|
| `frost_anchored` annuals | 79 | Season inversion: cool crops -> Oct-Mar winter garden + summer gap; warm crops -> long spring+fall around a mid-summer pause | A31 + A32 (real calendar) | The bulk; uniform pattern off one dominant TAMU calendar |
| `perennial_evergreen` (citrus: grapefruit, lemon, lime, mandarin-clementine, orange-navel) | 5 | Thrive -- RGV's signature crop | A31 (A32 exempt) | **Full flagship fruiting calendars** (Trevor call 2026-07-13; honesty over the gate floor) |
| `perennial_chill_gated` fruit | 14 | Near-zero chill: apple/apricot/cherry-sour/cherry-sweet/nectarine/peach/pear-asian/pear-european/plum/pawpaw -> no fruit; fig/mulberry/persimmon/pomegranate -> low-chill, likely fruit | A31 + **A3 no-fruit split** (A32 exempt) | Light `suitability`-verdict cells for the no-fruit set; real cells for the low-chill set |
| `perennial_woody_ornamental` (rosemary, oregano, sage, thyme, lavender) | 5 | Grow year-round; lavender struggles in humidity | A31 + A32 | Real calendars + honesty note |
| `berries_woody` (blackberry, blueberry, raspberry, elderberry) | 4 | Blackberry strong (Texas cultivars); blueberry/raspberry marginal (chill/heat); elderberry adaptable | A31 + A32 | Real calendars + suitability notes |
| `perennial_herbaceous` (strawberry) | 1 | Winter annual (Oct plant -> spring harvest) | A31 + A32 | Real calendar |

Net: **~89 real calendars** (79 annuals + 10 non-tree perennials) + **5 flagship citrus calendars** +
**~14 light tree cells** (A3-governed). A32's calendar-presence floor applies only to
`{frost_anchored, perennial_herbaceous, berries_woody, perennial_woody_ornamental}`; trees
(`perennial_chill_gated`, `perennial_evergreen`) are A32-exempt and governed by A3.

## 4. Data-model design

### 4.1 Zone span -- `["9", "10"]` (confirm against `zip-zones.json`)

z10 is the RGV core (McAllen/Brownsville/Harlingen -- the 95 ZIPs the sweep flagged); z9 is the
inland/northern fringe (Starr County). A45 requires `resolved_by_zone` keys to match the span
exactly, so most crops get **two zone rows** (`"9"` and `"10"`).

**This is the one value that cannot be verified from this repo.** The authority is plant-app's
`zip-zones.json` 785xx distribution. It is a confirm-item paired with the plant-app handoff (section
9): if the RGV ZIP3s carry only z10, the span is `["10"]` and each crop gets one row; if z9b pockets
exist, `["9", "10"]`. The spec assumes `["9", "10"]` and the build re-derives it from the actual
distribution before authoring keys. `rgv` is added to `EXPECTED_SPANS` with whatever the ZIP table
confirms; `region_chill_delivered.rgv` carries the same zone keys.

### 4.2 Frost-free resolution -- reuse the existing Hawaii / FL-z11 pattern (no new architecture)

`resolution_method` is a free-text provenance label (not gate-enforced as an enum;
`register_completeness_gate` and `field_classification` treat it as a known field). Frost-free
resolution variants already exist and are live in Hawaii and FL-z11 cells: `month_resolved_frost_free`,
`frost_free_no_anchor`, `..._frost_free`. A frost-free cell (verified against `broccoli.hawaii_tropical`)
is shaped:

- `plantings[]` anchored to `transplant_window` / `plant_out` offsets, **not** `frost_free_spring` /
  `soil_workable`.
- `resolved_by_zone[z].resolution_method = "month_resolved_frost_free"` (or the sourced RGV variant).
- `resolved_by_zone[z].resolved_from = {last_frost: null, first_frost: null}`.
- Authored month windows (`plant_out`, `harvest`, etc.); `calendar[]` derived by
  `tools/annual_calendar.py` from the authored windows (the deriver reads the cell, not a global
  frost table).

RGV cells are **Hawaii-shaped**. No deriver change, no new resolution architecture, no new
`calendar_basis`. This is the single biggest de-risk of the arc.

### 4.3 Per-crop RGV cell -- mirrors the crop's existing region-cell archetype

Each crop's `rgv` cell carries the same key set its se_gulf / hawaii_tropical cell carries for that
archetype (`region_id`, `region_label`, `zone_span`, `sources`, `plantings[]`, `resolved_by_zone`,
`region_notes_beginner`, `region_notes_seasoned`; trees add `suitability` +
`suitability_note_{beginner,seasoned}` + `chill_basis_{beginner,seasoned}` inside the cell / zone
rows). RGV-authored values replace the donor values; the frost-free convention (4.2) governs
`resolved_from` / `resolution_method`. `whole_crop_gate` run per crop during build validates the
exact per-field shape, so the archetype template is enforced, not assumed.

- `region_id`: `rgv`
- `region_label`: `"Rio Grande Valley: Subtropical South Texas"` (final wording in build)

### 4.4 Top-level touch-points

- `zone_span_gate.EXPECTED_SPANS`: add `rgv` (span from 4.1). No `DONORS` entry -- RGV is authored
  fresh, not cloned.
- `region_chill_delivered.rgv`: a low-chill band keyed by the rgv zones (4.5).
- `region_chill_delivered_provenance`: the RGV chill band's source note.
- `region_source_map` (top-level): add an `rgv` entry if the schema requires per-region source
  listing (confirm shape in build).
- `coverage_floor_gate.CANONICAL_REGIONS` / `CANONICAL_ZONES`: auto-derived from `EXPECTED_SPANS`
  -- no edit needed.

### 4.5 `region_chill_delivered.rgv` -- the A3 no-fruit split

RGV is very low chill. Order-of-magnitude `[0, 300]` (fl_peninsula z11 and Hawaii sit at `[0, 150]`;
RGV runs slightly higher). This band is **user-displayed** (plant-astro TreeGuide "your area banks
~X chill hours"), so it is sourced to TAMU AgriLife in build, not guessed. It drives A3 for the 14
chill-gated trees: a variety/crop whose stated chill requirement exceeds the delivered band gets a
`survives_no_fruit` / `unsuitable` verdict.

## 5. Viability taxonomy (the honest per-class calendar)

- **Annuals (79).** Winter-garden inversion. Cool-season crops sow/transplant in the Oct-Mar
  window; the summer is a gap. Summer-gap token: prefer `season_over` unless a backed `heat_pause`
  is authored (consistent with the Hawaii convention and the heat_pause-at-variety-pass discipline).
  Warm-season crops run spring + fall around a mid-summer pause. Windows from the TAMU LRGV /
  South-Texas vegetable calendar.
- **Citrus (5, evergreen).** Full flagship fruiting calendars (bloom + harvest windows),
  `suitability: fruits_reliably`, TAMU-sourced. The authoritative answer for RGV's signature crop.
- **Chill-gated fruit (14).** A3 no-fruit split against the rgv chill band:
  - No-fruit (near-zero chill vs high requirement): apple, apricot, cherry-sour, cherry-sweet,
    nectarine, peach, pear-asian, pear-european, plum, pawpaw -> `survives_no_fruit` or `unsuitable`
    verdict cells with sourced notes (light; A32-exempt).
  - Low-chill, likely fruit: fig, mulberry, persimmon, pomegranate -> real cells; the exact
    fruit/no-fruit call per crop is sourced to TAMU in build (not asserted here).
- **Woody herbs (5).** Real calendars; rosemary/oregano/sage/thyme grow year-round; lavender carries
  an honest humidity-struggle note.
- **Berries (4).** Real calendars + honest suitability: blackberry strong (Texas cultivars),
  blueberry/raspberry marginal (chill/heat), elderberry adaptable.
- **Strawberry (1).** Winter-annual calendar (Oct plant -> spring harvest).

## 6. Sourcing (T1)

Texas A&M AgriLife Extension is strong on Lower-Rio-Grande-Valley / South-Texas planting calendars,
and `tamu_agrilife` is already a catalogued T1 source (se_gulf cites it). Budget a targeted T1 hunt
for RGV-specific month-by-month windows across the classes:

- Annuals: the LRGV / South-Texas vegetable planting-date table.
- Citrus: TAMU AgriLife citrus (South Texas) guidance.
- Chill-gated + low-chill fruit: TAMU low-chill fruit-for-South-Texas guidance (drives both the
  chill band and the per-crop fruit/no-fruit call).
- Berries + strawberry: TAMU small-fruit / strawberry-for-South-Texas guidance.

The T1-or-it-doesn't-ship rule holds. New T1 sources may be catalogued as needed (the rule is about
tier, not the existing catalog list). Where a class lacks a clean T1 window, that crop's RGV cell is
authored conservatively and flagged, never fabricated.

## 7. Rollout mechanics -- author off-canonical, promote atomically

**The ordering pincer.** A45 rejects any `rgv` cell while `rgv` is absent from `EXPECTED_SPANS`
("unknown region id"); adding `rgv` to `EXPECTED_SPANS` makes A31 fail all 108 crops that lack an
`rgv` cell. The span table and the 108 cells must flip together -- exactly the "widen the span and
clone the rows together" discipline the zone-span reconciliation used.

**The build.**

1. Author all 108 `rgv` cells into an **off-canonical staging structure** (canonical stays
   READ-ONLY), batched by crop-class:
   - Batch 1: annuals (79) from the TAMU LRGV vegetable calendar (may sub-batch by family for
     source-truth sampling).
   - Batch 2: citrus (5) flagship calendars.
   - Batch 3: chill-gated trees (14) -- A3 verdicts + the low-chill fruit calendars.
   - Batch 4: woody herbs (5) + berries (4) + strawberry (1).
   - Subagent-driven authoring is appropriate (independent per-crop work); each subagent returns
     structured cell content for its crop, assembled deterministically.
2. Assemble the staged cells + the `EXPECTED_SPANS` `rgv` entry + `region_chill_delivered.rgv` +
   provenance into one SHA-guarded batch (`tools/apply_patch.py` pattern). Gate on scratch copies
   first.
3. **One atomic promote.** `gate_all` is green before (no `rgv` anywhere) and after (`rgv`
   everywhere + `EXPECTED_SPANS` + chill band), never broken in between. Footprint audit: exactly
   the 108 crops' `regions.rgv` + the three top-level additions changed; all else byte-identical;
   count unchanged (125); COMPACT (no reformatting, no trailing newline).

## 8. Verification (TDD, per session protocol)

- **A45** (`zone_span_gate`): green once `rgv` is in `EXPECTED_SPANS` and every `rgv` cell's
  `resolved_by_zone` keys match the span. RED-proven by staging a cell whose keys mismatch the span
  before the promote.
- **A31 / A32** (`coverage_floor_gate`): A31 green (all 108 carry `rgv` with a non-empty
  `resolved_by_zone`); A32 green (the 89 non-tree cells carry non-empty calendars). RED-proven by
  staging a crop with a missing / empty `rgv` cell.
- **A3** (perennial no-fruit split): the 14 chill-gated trees' RGV verdicts are consistent with the
  `region_chill_delivered.rgv` band.
- **Whole-suite:** `whole_crop_gate` per crop during build, `gate_all` 116/116 roster-wide,
  `release_verify`, and the **pre-commit backstop** (it checks ALL changed crops -- the empty-shell
  regression class the reconciliation hit; watch it here since 108 crops change).
- **New gate?** No new A-number is anticipated -- RGV rides A45/A31/A32/A3 as-is (a region is data,
  and the existing floors already guard region shape). If the build surfaces a defect class the
  existing gates miss (e.g. a frost-free cell asserting a non-null `resolved_from`), add the check
  TDD-first, RED before GREEN, adversarially proven on a scratch copy.
- **Known tooling caveat:** `release_verify` is single-crop-pilot-shaped; a roster-wide change
  produces benign section-A collateral (documented in the reconciliation entry). Use the
  footprint audit + `gate_all` + the pre-commit backstop as the roster-wide truth; the roster-wide
  `release_verify` mode remains a tracked follow-up.

## 9. App handoff (dataset-only arc; Trevor call 2026-07-13)

This arc authors + certifies the RGV region in **this repo only**. The app side ships as a separate
plant-app kickoff (pattern of kickoff #24), NOT as edits from this session (two-session collision
rule), and it is a downstream handoff, not a blocker on this arc's definition of done:

- `REGION_STATES`: map `rgv` -> TX.
- `ZIP3_REGION_HINT`: fence the RGV ZIP3s (785xx: McAllen, Edinburg, Mission, Pharr, Weslaco,
  Harlingen, Brownsville, San Benito) to `rgv`. Without the fence, TX z10 keeps matching se_gulf and
  RGV never wins.
- Confirm the `rgv` `zone_span` against `zip-zones.json` (section 4.1) and verify the regions.json
  sync path.

plant-astro consumes the new region automatically (regions.ts reads spans + unions across crops at
runtime), plus the flagship citrus bloom/harvest and the RGV chill band in TreeGuide.

## 10. Non-goals

- No partial/opt-in region and no A31 gate relaxation (Option A was chosen).
- No app-side edits from this session (roadmap item 2 / a new plant-app kickoff owns them).
- No plant-astro submodule bump from this session (owned by the astro session).
- No new region beyond RGV (PNW / mid-Atlantic / PR are roadmap items 4-6, separate arcs).
- No `zone_frost_data` change (RGV is frost-free; `resolved_from` nulls, no z-entry needed).

## 11. Risks / open items

- **Zone span depends on an app-side file.** `["9","10"]` is the assumption; the build re-derives
  from `zip-zones.json` 785xx before authoring keys. If it is z10-only, the span and every cell's
  keys collapse to `["10"]`.
- **The low-chill fruit call.** fig/mulberry/persimmon/pomegranate fruit-vs-no-fruit in RGV is a
  sourced call; if TAMU evidence is thin for one, it gets a conservative `survives_no_fruit` verdict,
  not an optimistic calendar.
- **108-crop footprint + the empty-shell class.** The reconciliation's regression was empty shells
  slipping through gate_all/release_verify (certified-only); the pre-commit backstop caught it. The
  same discipline applies -- footprint-audit every batch.
- **Summer-gap token convention.** `season_over` vs `heat_pause` for the cool-crop summer gap;
  default `season_over`, author a backed `heat_pause` only where sourced (heat_pause-at-variety-pass
  discipline).

## 12. Acceptance criteria / definition of done

1. `rgv` region authored + certified across all 108 certified region-carrying crops (89 real
   calendars + 5 flagship citrus + 14 A3-governed tree cells).
2. `EXPECTED_SPANS.rgv` + `region_chill_delivered.rgv` (+ provenance) added; A45 / A31 / A32 / A3
   green; `gate_all` 116/116; `release_verify` clean (modulo the documented roster-wide collateral);
   pre-commit backstop clean.
3. Footprint audit: exactly the 108 crops' `regions.rgv` + the three top-level additions changed;
   all else byte-identical; count 125; COMPACT.
4. The plant-app sweep repro shows the RGV ZIPs resolving to `rgv` (once the paired app fence lands),
   not the se_gulf interim.
5. State trio updated (CURRENT_STATE.md surgical per the drift memory, STATE_HISTORY.md most-recent
   first, LATEST.txt SHA + session); roadmap item 3 marked SHIPPED and the RGV interim /
   TX-fencing lines retired; a plant-app kickoff written for the ZIP3 fence.
6. Commit awaits Trevor's push confirm. No plant-astro bump from this session.
