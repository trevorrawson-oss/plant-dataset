# Kickoff: Maritime Pacific Northwest region (roadmap item 4)

**For:** a FRESH plant-dataset (Claude Code) session.
**Goal:** author a real maritime Pacific Northwest region (`pnw`, WA/OR west of the Cascades, z8-9)
so the ~750 z8-9 WA/OR ZIPs stop riding generic frost-anchored zone dates that assume a HOT summer
the maritime PNW does not have. This is roadmap item 4, the highest-impact remaining region: cool
maritime summers are where the generic dates are MOST misleading.
**Base:** canonical `d0832254` / dataset `main` (pushed, `30c5236`). Rebase onto current `origin/main`
before starting.
**First action:** `superpowers:brainstorming` (a new authored region -- creative/design work). Do
NOT splice until the scope + design calls below are made.
**Precedent:** this is the SECOND new authored region, directly after the RGV arc (#25, shipped
2026-07-13). **Reuse the RGV playbook and toolchain** -- it worked end to end. See "Reusable assets".

## Why PNW needs its own region

West of the Cascades (Puget Sound, the Willamette Valley, the coast), WA/OR is a **cool-summer
maritime** climate: a long, mild, dry growing season with summer highs in the 70s-low 80s°F, real
winter chill, and frost dates in the shoulder seasons. The generic frost-anchored zone dates are
"most misleading here" NOT because of frost timing but because they assume a **hot** summer:

- **Warm-season crops are the weak axis.** Tomatoes, peppers, eggplant, melons, sweet corn, okra,
  sweet potato, winter squash need heat the maritime PNW rations. They want early / short-season
  cultivars, transplants started well ahead, and warmest-site / wall-o-water tricks; some (melon,
  okra, sweet potato, long-season peppers) are marginal. A generic "plant in May, harvest by
  September" calendar overstates what ripens here.
- **Cool-season crops are the strong axis.** Brassicas, greens, roots, peas, and cool herbs thrive
  with a very long season; the maritime winter is mild enough for overwintering many of them. The
  summer here is the PRIME growing window (just cool), NOT a heat_pause -- the OPPOSITE of RGV.
- **Real chill -> temperate tree fruit is a STRENGTH.** The maritime PNW banks ample winter chill;
  it is a premier apple / pear / cherry / plum region. So the A3 no-fruit split flips the other way
  from RGV: the chill-gated trees mostly FRUIT here (the region's flagship, the way citrus was RGV's).
  `region_chill_delivered.pnw` is a substantial chill band, not RGV's near-zero.

## Read first (context)

- `docs/region_coverage_roadmap.md` -- item 4 is this. Items 5-6 (judged belt, PR) are separate.
- **`docs/kickoffs/25-rgv-subtropical-tx-region.md` + the RGV spec/plan
  (`docs/superpowers/{specs,plans}/2026-07-13-rgv-subtropical-tx-region*`)** -- the template arc.
  PNW follows the same shape; the sections below are mostly "same as RGV except...".
- `docs/2026-07-12-region-zonespan-gaps.md` -- the plant-app sweep; the PNW rows are WA (302 z8 / 129
  z9) + OR (199 z8 / 121 z9).
- `docs/gs_cross_crop_field_addition_v0.md` -- the column GS-arc method (a new region = a roster-wide
  column).
- memory `rgv-subtropical-tx-region` -- the RGV reusable lessons + toolchain.

## THE BIG ONE -- same roster-wide scope as RGV (Option A is the proven answer)

Adding a region is a ROSTER-WIDE authoring arc: `coverage_floor_gate` A31 derives its roster from
`EXPECTED_SPANS`, so the moment you add `pnw`, **all ~108 certified region-carrying crops need a
`pnw` `resolved_by_zone` cell or A31 fails them**. RGV proved **Option A (full roster-wide, ~108
crops)** is the honest answer and is tractable via the class-batched, per-crop-gated, atomic-promote
approach. Confirm the scope with Trevor, but the default is: repeat Option A.

## Design calls for the brainstorm (the PNW specifics; contrast with RGV noted)

1. **Zone span.** Likely `["8","9"]` (maritime WA/OR). CONFIRM from the actual `zip-zones.json`
   WA/OR z8-9 distribution. **The east-side wrinkle:** z8-9 in WA/OR is dominantly the maritime west
   side, but check for any hot, dry east-of-the-Cascades z8 pockets (Spokane basin, etc.) that
   state+zone alone would wrongly pull into a maritime calendar -- this may need a ZIP3 fence
   (west-side ZIP3s) on the app side, the mirror of RGV's 785xx fence. Flag it for the plant-app
   kickoff.
2. **FROST-ANCHORED, not frost-free (the opposite of RGV).** PNW has real last-spring / first-fall
   frost dates, so the standard `frost_anchored` calendar model APPLIES and `tools/annual_calendar.py`
   (summer-centered) may actually WORK here -- VALIDATE it against a maritime cell rather than
   reusing RGV's hand-authored Hawaii-shape. This is the single biggest structural difference from
   RGV: RGV forced hand-authoring because the deriver is frost-free-blind; PNW's summer-centered
   season is what the deriver was built for. Confirm early -- if the deriver reproduces a sensible
   maritime calendar from authored windows, the annual authoring is LIGHTER than RGV's.
3. **Cool-summer viability (the honest-calendar work).**
   - Cool-season crops: long maritime season, many overwintering; NO summer heat_pause (summer is the
     growing window). Standard spring-through-fall, some year-round.
   - Warm-season crops: transplant-led, early/short-season cultivars, warmest-site framing; author
     honest marginality for the heat-hungry ones (melon / okra / sweet potato / long-season pepper)
     rather than an optimistic hot-summer calendar. This is the PNW analog of RGV's per-crop honesty
     calls -- follow the T1 evidence over the generic template.
   - Chill-gated trees: mostly `fruits_reliably` (the region's strength); `region_chill_delivered.pnw`
     is a real, sourced chill band (WA/OR extension chill data). A3 flips vs RGV (fruit, not no-fruit).
     Citrus / subtropical evergreens: the reverse of RGV -- `survives`/`unsuitable` (too cold / too
     little heat), honest.
4. **`region_chill_delivered.pnw` band.** A substantial maritime chill figure (order-of-magnitude far
   above RGV's `[0,300]`; WA/OR banks plenty). Source from WSU / OSU extension chill data; it is the
   app-displayed chill table, so source it.
5. **Sourcing (T1).** WSU (Washington State University) + OSU (Oregon State University) extension have
   strong maritime-PNW / west-side vegetable + tree-fruit planting calendars. Budget a targeted T1
   hunt (mirror the RGV TAMU hunt); the same PDF-extraction gotcha may apply (extract tables in the
   CONTROLLER env with pypdf; subagent sandboxes block network/PDF tooling -- see the RGV arc).

## Mechanics (what a new region touches) + REUSABLE ASSETS

Same touch-points as RGV: `EXPECTED_SPANS.pnw`, `region_chill_delivered.pnw` (+ provenance replace),
a `pnw` cell on every certified region-carrying crop, the gate surface (A45 span parity, A31/A32
roster+calendar, A3 tree split, gate_all 116/116, release_verify, the pre-commit backstop), the state
trio, roadmap item 4 -> SHIPPED, a paired plant-app kickoff (REGION_STATES + any ZIP3 fence).

**REUSABLE from the RGV arc (do NOT rebuild these):**
- `tools/rgv_cell_audit.py` -- the anomaly detector (in-ground season_over, missing-indoors,
  cold_pause, stray lifted_from_zone, span/key drift, citation id->URL misattribution). GENERALIZE it
  to take a region id (it is currently rgv-hardcoded) -> `tools/region_cell_audit.py`, or copy+repoint.
  Run it on every batch + at promote. NOTE for PNW: `cold_pause` is LEGITIMATE in a frost-anchored PNW
  calendar (unlike frost-free RGV where the auditor forbids it) -- relax that specific check for pnw.
- `tools/rgv_harness.py` -- the off-canonical per-crop gate harness (scratch tools + scratch canonical
  + EXPECTED_SPANS patch + chill-band injection). Parametrize the region id.
- `tools/build_rgv_promote.py` -- the atomic-promote emitter (staging files -> one SHA-guarded batch
  + chill band + provenance replace). Parametrize.
- The SDD execution shape: class-batched authoring (annuals / trees / berries+herbs), fresh-subagent
  review per batch, per-crop harness gate, one atomic promote, scratch dry-run before the canonical
  write, Trevor-gated promote. It worked.

## Definition of done

`pnw` region authored + certified across the ~108 roster; A45/A31/A32/A3 + gate_all + release_verify
green; the sweep shows the WA/OR z8-9 ZIPs resolving to `pnw` (not generic zone dates); state trio
updated; roadmap item 4 marked SHIPPED; a plant-app kickoff written (REGION_STATES pnw -> WA,OR + the
west-side ZIP3 fence if the east-side z8 pockets need it). Then item 4 is closed; the program is down
to item 5 (the judged-belt ruling pass) + item 6 (PR, product call).

## Sequencing note

- **The RGV plant-app fence (kickoff #26) is the pipeline pilot** -- it proves the app consumes a
  brand-new authored region end to end (regions.json sync + REGION_STATES + ZIP3 fence). Land it (or
  at least verify the sync path) before or in parallel with this arc, so PNW does not stack a second
  un-consumed region on an unproven app path. The PNW *dataset* build does not technically block on it
  (different repo), but the validation de-risks the whole remaining program.
- The LEEK variety pilot is a separate track (variety, not region), unblocked; it can run in parallel
  with this arc. If both run, rebase leek's plan base SHA onto whatever canonical PNW lands at, and do
  not let two sessions hold the canonical open at once (the sweet-corn collision rule).
