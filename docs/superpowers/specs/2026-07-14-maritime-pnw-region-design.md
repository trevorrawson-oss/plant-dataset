# Maritime Pacific Northwest region -- design spec

**Date:** 2026-07-14
**Kickoff:** `docs/kickoffs/27-maritime-pnw-region.md` (roadmap item 4)
**Base canonical:** `d0832254` (RGV shipped) / dataset `main` @ `7398a28` (== `origin/main`)
**Precedent:** the RGV arc (`docs/superpowers/specs/2026-07-13-rgv-subtropical-tx-region-design.md`),
shipped 2026-07-13. This spec is deliberately "same as RGV except..." -- the deltas are called out
inline. The two Trevor decisions of 2026-07-14 (below) are settled: **Option A full roster-wide**,
and **proceed now** (do not wait on the RGV plant-app fence pilot; the dataset build is a separate
repo and does not block on it).

---

## 1. Product goal

Author a real maritime Pacific Northwest region (`pnw`, WA/OR west of the Cascades, z8-9) so the
~750 z8-9 WA/OR ZIPs stop riding generic frost-anchored zone dates that assume a HOT summer the
maritime PNW does not have. This is the second new authored region after RGV and the highest-impact
remaining one: the generic dates are most misleading here not because of frost timing but because
they assume summer heat the region rations.

## 2. Why PNW needs its own region (not a generic-zone stretch)

West of the Cascades, WA/OR is a **cool-summer maritime** climate: a long, mild, dry growing season
with summer highs in the 70s-low 80s degF, real winter chill, and frost dates in the shoulder
seasons. The generic z8-9 dates get the frost timing roughly right but get the **season character**
wrong in three ways that PNW inverts relative to both the generic template and RGV:

- **Warm-season crops are the weak axis.** Tomato, pepper, eggplant, melon, sweet corn, okra, sweet
  potato, winter squash need heat the maritime PNW rations. They want early / short-season cultivars,
  transplants started well ahead, warmest-site framing; some (melon, okra, sweet potato, long-season
  pepper) are honestly marginal. A generic "plant in May, harvest by September" calendar overstates
  what ripens here.
- **Cool-season crops are the strong axis.** Brassicas, greens, roots, peas, and cool herbs thrive
  on a very long season; the mild winter overwinters many of them. **Summer is the PRIME growing
  window (just cool), NOT a heat_pause** -- the opposite of RGV.
- **Real chill -> temperate tree fruit is a STRENGTH.** The maritime PNW banks ample winter chill;
  it is premier apple / pear / cherry / plum country. The A3 no-fruit split flips the other way from
  RGV: the chill-gated trees mostly FRUIT here (the region's flagship, the way citrus was RGV's).

## 3. Scope decision (Trevor-approved 2026-07-14): Option A -- full roster-wide

`coverage_floor_gate` A31 derives its region roster from `zone_span_gate.EXPECTED_SPANS`. The moment
`pnw` is added to `EXPECTED_SPANS`, all **108 certified region-carrying crops** need a `pnw`
`resolved_by_zone` cell or A31 fails them. A partial / opt-in region would reintroduce borrowed data
under a real region label (the exact dishonesty a new region exists to retire), so **Option A (full
roster-wide)** is both the honest answer and the only one A31 accepts.

**Roster confirmed against canonical `d0832254` (identical to RGV's -- no certifications since):**

| Crop class (`calendar_basis`) | Count | PNW reality | Gate floor | Authoring weight |
|---|---|---|---|---|
| `frost_anchored` annuals | 79 | Summer IS the growing window (cool, not paused). Cool crops thrive + many overwinter -> **no summer heat_pause**; warm crops transplant-led / early-cultivar, the heat-hungry few honestly marginal | A31 + A32 (real calendar) | The bulk; standard deriver off WSU/OSU windows |
| `perennial_chill_gated` fruit | 14 | **The flagship.** Ample chill -> most FRUIT | A31 + **A3 fruit split** (A32 exempt) | Real fruiting cells for the fruiting set; light verdict cells for the edge cases |
| `perennial_evergreen` (citrus) | 5 | The reverse of RGV: too cold / too little heat -> `survives`/`unsuitable`, honest | A31 (A32 exempt) | Light cold-limited verdict cells |
| `perennial_woody_ornamental` (herbs) | 5 | Grow well; **lavender THRIVES** (Sequim rain-shadow) vs RGV's humidity-struggle | A31 + A32 | Real calendars + cold-edge notes |
| `berries_woody` | 4 | **A PNW signature** (WA #1 US red raspberry; premier blueberry; marionberry an OR native; elderberry native) | A31 + A32 | Real calendars + strong notes |
| `perennial_herbaceous` (strawberry) | 1 | Strong (June-bearing PNW berries) | A31 + A32 | Real calendar |

Net: **~89 real calendars** (79 annuals + 10 non-tree perennials) + **~14 tree cells** (A3-governed,
flagship-heavy). A32's calendar-presence floor applies only to
`{frost_anchored, perennial_herbaceous, berries_woody, perennial_woody_ornamental}`; the trees
(`perennial_chill_gated`, `perennial_evergreen`) are A32-exempt and governed by A3.

## 4. Data-model design

### 4.1 Zone span -- `["8", "9"]` (maritime WA/OR)

Maritime WA/OR west of the Cascades is dominantly z8 (Puget Sound lowlands, Willamette Valley) with
milder z9 pockets (the coast, protected lowlands). A45 requires `resolved_by_zone` keys to match the
span exactly, so most crops get **two zone rows** (`"8"` and `"9"`). `pnw` is added to
`EXPECTED_SPANS` with `["8", "9"]`; `region_chill_delivered.pnw` carries the same two zone keys.

**The east-side wrinkle (flagged for the plant-app kickoff, NOT gated here).** z8-9 in WA/OR is
dominantly the maritime west side, but hot, dry east-of-the-Cascades z8 pockets exist (Spokane
basin, Columbia Basin) that state+zone matching alone would wrongly pull into a maritime calendar.
The authority for the ZIP distribution is plant-app's `zip-zones.json` (not in this repo). This is
the mirror of RGV's 785xx fence: the plant-app handoff fences the region to **west-side ZIP3s**. The
dataset build does not depend on it; it is a section-9 confirm-item.

### 4.2 Frost-ANCHORED resolution -- the standard model (the biggest delta from RGV)

**This is the single most important structural difference from RGV, and it makes the arc lighter.**
RGV cells were frost-FREE ("Hawaii-shaped": `resolution_method = month_resolved_frost_free`,
`resolved_from = {last_frost: null, first_frost: null}`, no `cold_pause`) because RGV has no killing
winter -- the deriver is frost-free-blind, so RGV forced hand-authored calendars. PNW has a **real
winter**, so its cells are ordinary **frost-anchored** cells, identical in shape to each crop's
existing `ca_north_coast` / `ca_interior` / `northern_tier` cells:

- `resolution_method: "frost_anchored_resolved"`.
- `resolved_from: {last_frost: <date>, first_frost: <date>}` -- **real maritime frost dates**
  (Puget/Willamette lowlands: last frost ~ early-mid April, first frost ~ late Oct-early Nov for z8;
  milder for z9 pockets), sourced to WSU/OSU/NWS in build.
- Authored month windows (`plant_out`, `start_indoors`, `harvest`/`harvest_start`/`harvest_end`,
  `first_plant_date`/`last_plant_date`, optional `second_planting{}`, `succession_*`); `calendar[]`
  **derived by `tools/annual_calendar.py`** with `calendar_basis = "frost_anchored"`.

**Deriver validation (done 2026-07-14, empirical de-risk).** The deriver's `heat_pause` is
declaration-driven, not temperature-computed: it emits `heat_pause` tokens only for months in a
cell's `heat_pause.months` object (`annual_calendar.py:86,114`). A cool-summer cell declares **no**
heat_pause months, so the whole warm season renders `plant`/`harvest`/`growing` and winter (January
inactive) grows a contiguous `cold_pause` (`annual_calendar.py:101-108`). Verified against the
closest already-shipped maritime analog, `ca_north_coast` (z9-10 foggy coastal CA): `lettuce-leaf`
re-derives **byte-exact** (`cold_pause` winter -> long `plant`/`harvest` Feb-Oct -> `cold_pause` late
fall, zero heat_pause). The `broccoli` re-derive "DIFF" was only the authored `second_planting` fall
cycle absent from the quick re-derive -- confirming the rule: **author `second_planting` where a real
fall cycle exists** (as the roster already does), and the calendar falls out. **No deriver change, no
new resolution architecture, no new `calendar_basis`, no hand-authoring.**

### 4.3 Per-crop PNW cell -- mirrors the crop's existing frost-anchored archetype

Each crop's `pnw` cell carries the same key set its existing frost-anchored region cells carry for
that archetype:

- **Annuals / herbs / berries / strawberry (frost-anchored calendar archetypes):** region-level
  `region_id, region_label, zone_span, sources, plantings, resolved_by_zone, region_notes_beginner,
  region_notes_seasoned`; per-zone `plant_out, start_indoors, harvest(_start/_end),
  first_plant_date, last_plant_date, resolution_method, resolved_from, sources, anchoring_urls`
  (+ optional `second_planting`, `succession_spring/fall`, `successions_realized`, `zone_notes`,
  `notes`, `planting_note` where the crop's archetype uses them).
- **Chill-gated trees (`perennial_chill_gated`):** add region-level `chill_basis_seasoned,
  chill_basis_beginner, plantings_provenance`; per-zone `suitability, suitability_note_{seasoned,
  beginner}, bloom, harvest, frost_risk_note_seasoned` (the fruiting flagship set carries real
  bloom+harvest windows; A32-exempt).
- **Citrus (`perennial_evergreen`):** add region-level `min_winter_temp_f, cold_basis_{seasoned,
  beginner}` (+ conditional heat basis); per-zone `suitability, suitability_note_{seasoned, beginner},
  min_winter_temp_f, resolution_method, resolved_from`. For PNW the honesty is COLD-limited, not
  heat-limited: `suitability = survives`/`unsuitable`, the `cold_basis_*` fields carry why.

`whole_crop_gate` run per crop during build validates the exact per-field shape, so the archetype
template is enforced, not assumed. The build emits a `docs/pnw_cell_contract.md` mirroring
`docs/rgv_cell_contract.md` for the tree/citrus honesty-field shapes.

### 4.4 Top-level touch-points

- `zone_span_gate.EXPECTED_SPANS`: add `pnw: ["8", "9"]`. **No `DONORS` entry** -- PNW is authored
  fresh, not cloned from a donor zone.
- `region_chill_delivered.pnw`: a substantial maritime chill band keyed by the pnw zones (4.5).
- `region_chill_delivered_provenance`: the PNW chill band's source note (WSU/OSU).
- `coverage_floor_gate.CANONICAL_REGIONS` / `CANONICAL_ZONES`: auto-derived from `EXPECTED_SPANS`
  -- no edit needed.
- `region_source_map` / any top-level per-region source listing: add a `pnw` entry if the schema
  requires it (confirm shape in build).

### 4.5 `region_chill_delivered.pnw` -- the A3 FRUIT split (flips vs RGV)

The maritime PNW banks ample chill. Unlike RGV's near-zero `[0, 300]`, `pnw` carries a **substantial
band** consistent with the existing frost-anchored regions in the table (`northern_tier` z3
`[1000,1600]`, `ca_interior` z8 `[500,1100]`, `se_gulf` z8 `[650,1000]`). The band is
**user-displayed** (plant-astro TreeGuide "your area banks ~X chill hours"), so it is sourced to
WSU/OSU in build, **in the same chill model the existing table uses** (the build reconciles the model
so the number is comparable to its neighbors), not guessed. The operative fact is that it clears the
fruiting threshold (~600-1000 hr) of apple / pear / cherry / plum, driving the A3 flip to
`fruits_reliably` for the flagship set. Exact `[low, high]` per zone is a build sourcing task.

## 5. Viability taxonomy (the honest per-class calendar)

- **Annuals (79).** Summer is the growing window. **Cool-season crops** (brassicas, greens, roots,
  peas, cool herbs): long spring-through-fall season, many overwintering; **no summer `heat_pause`**
  (the summer lull, if any, renders `growing`, not a pause). Standard frost-anchored calendar,
  `cold_pause` winters. **Warm-season crops** (tomato, pepper, eggplant, melon, sweet corn, squash,
  okra, sweet potato, cucumber): transplant-led, early / short-season framing; author the honest
  marginality of the heat-hungry ones (melon, okra, sweet potato, long-season pepper) in prose +
  a compressed, transplant-anchored calendar rather than an optimistic hot-summer window. This is
  the PNW analog of RGV's per-crop honesty calls -- **follow the T1 evidence over the generic
  template.** Warm annuals carry no `suitability` field (annual archetype has none; A32 forces a
  calendar), so honesty lives in the calendar shape + `region_notes_*`, exactly as RGV did for humid
  berries.
- **Chill-gated fruit (14).** A3 FRUIT split against the pnw chill band:
  - Fruiting (chill delivered >= requirement): apple, pear-european, pear-asian, cherry-sweet,
    cherry-sour, plum, apricot, nectarine, peach, fig, mulberry, persimmon -> **`fruits_reliably`**
    with real bloom+harvest windows (the region's flagship). Exact per-crop call sourced to WSU/OSU
    in build (cool-summer ripening caveats noted where they apply -- e.g. late-ripening peach/fig in
    the coolest sites).
  - Edge cases (cool-summer heat-limited, not chill-limited): pomegranate, pawpaw -> honest
    `survives` / marginal verdict per the T1 evidence in build (pomegranate wants more summer heat
    than the maritime PNW gives; pawpaw wants summer heat + humidity).
- **Citrus (5, evergreen).** The reverse of RGV: cold-limited. `suitability = survives`/`unsuitable`
  with honest `cold_basis_*` notes (marginal even as protected container plants west of the
  Cascades). A3 no/limited-fruit.
- **Woody herbs (5).** Real calendars. Rosemary/oregano/sage/thyme grow well (cold-edge note for the
  coldest z8); **lavender THRIVES** (the maritime rain-shadow is prime lavender country) -- an honest
  strength note, the inverse of RGV's humidity-struggle.
- **Berries (4).** Real calendars + strong suitability: **a PNW signature.** Raspberry (WA is the #1
  US red-raspberry state), blueberry (premier region -- acidic soils + chill), blackberry
  (marionberry an OR-bred cultivar), elderberry (native). All strong.
- **Strawberry (1).** Real frost-anchored calendar (spring plant -> summer harvest; June-bearing PNW
  berries are strong).

## 6. Sourcing (T1)

WSU (Washington State University) and OSU (Oregon State University) extension have strong maritime /
west-side planting calendars for vegetables and tree fruit. Budget a **targeted T1 hunt** (mirror the
RGV TAMU hunt) across the classes:

- Annuals: WSU / OSU maritime-PNW (west-side) vegetable planting-calendar tables.
- Tree fruit: WSU / OSU home-orchard + tree-fruit-for-western-WA/OR guidance (drives both the chill
  band and the per-crop fruit/no-fruit call).
- Berries + strawberry: WSU / OSU small-fruit / caneberry / blueberry / strawberry-for-the-maritime-
  PNW guidance.
- Frost dates + chill band: WSU / OSU / NWS maritime frost-date and chill-accumulation data.

**PDF-extraction gotcha (from the RGV arc):** extract calendar tables in the CONTROLLER env with
`pypdf`; subagent sandboxes block network / PDF tooling. The **T1-or-it-doesn't-ship** rule holds.
New T1 sources may be catalogued as needed (the rule is about tier, not the existing catalog list).
Where a class lacks a clean T1 window, that crop's `pnw` cell is authored conservatively and flagged,
never fabricated.

## 7. Rollout mechanics -- author off-canonical, promote atomically

Reuse the RGV SDD shape and toolchain, parametrized for the region id:

- **`tools/rgv_cell_audit.py` -> generalize to a region-id param** (`tools/region_cell_audit.py`,
  or copy+repoint). The anomaly detector (in-ground `season_over`, missing-indoors, stray
  `lifted_from_zone`, span/key drift, citation id->URL misattribution). **RELAX the `cold_pause`
  check for `pnw`:** `cold_pause` is LEGITIMATE in a frost-anchored maritime calendar (unlike the
  frost-free RGV where the auditor forbids it). Run on every batch + at promote.
- **`tools/rgv_harness.py` -> parametrize region id.** Off-canonical per-crop gate harness (scratch
  tools + scratch canonical + `EXPECTED_SPANS` patch + chill-band injection).
- **`tools/build_rgv_promote.py` -> parametrize region id.** Atomic-promote emitter (staging files
  -> one SHA-guarded batch + chill band + provenance replace).
- **SDD execution:** class-batched authoring (annuals split into cool-season / warm-season sub-
  batches; then trees, berries+herbs, strawberry), fresh-subagent review per batch, per-crop harness
  gate, one atomic promote, **scratch dry-run before the canonical write**, Trevor-gated promote.

The promote is **one atomic SHA-guarded batch**: `EXPECTED_SPANS.pnw` + 108 `regions.pnw` cells +
`region_chill_delivered.pnw` + provenance replace, landing together (a partial land would leave
A31/A3 failing on the new region). Canonical stays COMPACT (`separators=(",",":")`,
`ensure_ascii=False`, no trailing newline).

## 8. Verification (TDD, per session protocol)

Green gate is not a clean release. Before promote:

- `whole_crop_gate` 18/18 + `tools/gate_all.py` (whole suite on **every** certified crop) -> 116/116.
- `tools/zone_span_gate.py` (A45) -> 0 (span<->key parity + `pnw` in `EXPECTED_SPANS`).
- `coverage_floor_gate` (A31) -> the 108 roster all carry `pnw`; standalone count reads the 9
  uncertified shells only (benign, as in RGV; `gate_all`'s certified-only view is authoritative).
- A3 (`perennial_gate`) -> the tree fruit/no-fruit split coheres with the `pnw` chill band.
- `chill_gate` -> 0.
- `tools/release_verify.py` -> clean (section A collateral is the known roster-wide-structural false
  positive; the pre-commit backstop `precommit_release_verify.py` is the binding multi-crop
  regression gate).
- Per-batch source-truth sample (spot-check authored windows against the cited WSU/OSU table).
- Independent byte-diff footprint audit: EXACTLY 108 `regions.pnw` + `region_chill_delivered` +
  provenance changed; 0 other keys; count 125; COMPACT.

**No new gate.** A45/A31/A32/A3 are already region-generic (from the 2026-07-12 reconciliation +
the RGV arc). The adversarial discipline still applies to the parametrized tooling: prove the
region-id generalization on a scratch copy before trusting it.

## 9. App handoff (dataset-only arc)

Dataset-only here; the paired plant-app kickoff (mirror `docs/kickoffs/26-rgv-plant-app-zip3-fence.md`)
owns the app side:

- `REGION_STATES.pnw = WA, OR`.
- **The west-side ZIP3 fence** (the confirm-item from 4.1): fence `pnw` to maritime west-side ZIP3s
  so hot-dry east-of-the-Cascades z8 pockets (Spokane / Columbia Basin) do NOT resolve to a maritime
  calendar. Derive the exact ZIP3 list from `zip-zones.json`; if the east-side z8 ZIPs are few and
  already carry a better home (warm_arid adjacency), the fence may be a simple west-side allow-list.
- `regions.json` sync + the empty-state-ZIP cleanup are existing plant-app roadmap items.

No plant-astro bump from this session (memory `plant-astro-bump-owned-by-astro-session`): certify +
push the dataset here, then stop.

## 10. Non-goals

- No new `calendar_basis`, no deriver change, no new gate.
- No plant-astro submodule bump, no plant-app code changes (separate repos / sessions).
- No re-authoring of existing regions; `pnw` is purely additive.
- No variety-level work (the leek pilot is a separate parallel track).
- The east-side ZIP3 fence is scoped, authored, and owned on the app side, not here.

## 11. Risks / open items

- **Chill band model reconciliation.** The existing `region_chill_delivered` table's numbers imply a
  specific chill model; the WSU/OSU PNW figure must be sourced in the same model to be comparable.
  Build reconciles; flagged, not guessed.
- **Warm-crop honesty calibration.** Which of tomato/pepper/melon/corn/okra/sweet-potato/squash are
  "grows well with early cultivars" vs "honestly marginal" is a per-crop T1 call; the annual
  archetype has no `suitability` field, so the honesty must land in calendar shape + notes. Follow
  the WSU/OSU evidence, not the generic template.
- **Tree edge cases.** pomegranate + pawpaw (heat-limited, not chill-limited) and any late-ripening
  stone fruit in the coolest sites need a sourced call, not an assumption.
- **`release_verify` section A** false-positives on roster-wide structural releases (known; roadmap
  tooling follow-up). The pre-commit backstop is the binding regression gate.
- **Concurrency (sweet-corn collision rule).** If the leek pilot runs in parallel, do not let two
  sessions hold the canonical open at once; rebase leek's base SHA onto whatever canonical PNW lands
  at.

## 12. Acceptance criteria / definition of done

- `pnw` region authored + certified across the 108 roster; `zone_span = ["8", "9"]`.
- A45 / A31 / A32 / A3 + `gate_all` 116/116 + `chill_gate` 0 + `release_verify` clean +
  pre-commit backstop no-regression.
- Footprint EXACT (108 `regions.pnw` + `region_chill_delivered.pnw` + provenance; 0 other keys;
  count 125; COMPACT).
- The WA/OR z8-9 ZIPs resolve to `pnw` (not generic zone dates) once the app consumes it.
- State trio updated (CURRENT_STATE.md regenerate + prose slots, STATE_HISTORY.md prepend,
  LATEST.txt bump); roadmap item 4 -> SHIPPED; field-addition register row added.
- A plant-app kickoff written (`REGION_STATES.pnw -> WA,OR` + the west-side ZIP3 fence).
- Dataset committed + PUSHED (Trevor confirms push); NO plant-astro bump from this session.

Then item 4 is closed; the program is down to item 5 (the judged-belt ruling pass) + item 6 (PR,
product call).
