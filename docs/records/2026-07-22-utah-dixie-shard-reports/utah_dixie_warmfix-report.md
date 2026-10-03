# Utah "Dixie" WARM + TREE content-review fix report

Applied fixes from `docs/reviews/notes/2026-07-22/utah_dixie_content_review_A.md` to
`tools/staging/utah_dixie_annuals_warm.json` and `tools/staging/utah_dixie_trees.json`.
`crops_data_final.json` untouched; no commit.

## STATUS: DONE -- all cells GATE: PASS, both files audit 0 issues.

## Fixes applied

### CRITICAL C1 -- habanero (warm): re-authored as a desert heat-LOVER
Mirrored the `warm_arid` z8 desert-twin analog (Shape C, no heat_pause, harvest runs
through summer into fall). Single spring planting (Apr 1 Group D set-out, Feb indoor
start kept), harvest **Jul 5 - Oct 25**, heat_pause object REMOVED, calendar re-derived
via `annual_calendar.derive_annual_calendar`. Result: **4 harvest tokens (Jul-Oct)** where
the old cell showed zero. region_notes rewritten from "marginal/optimistic pick squeezed
against the heat wall" to "most heat-tolerant chile grown here." Dropped the now-irrelevant
`usu_ext_tomato` (tomato heat-abort page) citation from the cell; cites veg-dates + frost.

### IMPORTANT I2 -- cayenne-pepper (warm): heat-lover (Shape C)
Same treatment as habanero, mirroring `warm_arid` z8 cayenne (no heat_pause, continuous run).
Harvest **Jun 15 - Oct 25**, heat_pause removed, calendar re-derived: **5 harvest tokens
(Jun-Oct)**. Prose reframed to heat-tolerant single long-season crop.

### IMPORTANT I3 -- jalapeno (warm): heat-lover with a fall flush (split)
Mirrored `warm_arid`'s jalapeno SPLIT (jalapeno is more heat-sensitive than habanero/cayenne):
single spring planting, harvest **Jun 15 - Jun 30, Sep 15 - Oct 25**, heat_pause reduced to
**[7,8]** (peak-heat bearing gap, not a fall replant), basis reworded. Calendar re-derived:
harvest / heat_pause,heat_pause / harvest,harvest = **3 harvest tokens** across a June flush +
a Sep-Oct fall flush. No `second_planting` added (respects the delta-4a no-warm-crop-fall-replant
rule; matches the shipped `warm_arid`/`low_desert_az` single-planting comma-harvest precedent).

bell-pepper + banana-pepper (SWEET peppers) left as Shape A per ruling R2 -- not touched.

### IMPORTANT I4 -- edamame (warm): disclosed the by-analogy Group C date
Window UNCHANGED (per ruling R3: ~3-week June harvest + heat_pause [7,8,9] are correct).
Added honest disclosure in direct_sow synthesis_note + both region_notes: USU's table does
not list soybean separately, so edamame is grouped by analogy with the tender legumes /
snap bean (mirrors how okra/sweet-potato disclose their non-table basis).

### IMPORTANT I1 / R1 -- cherry-sour (trees): fruits_reliably -> marginal
`suitability` flipped to **"marginal"**. Re-authored suitability_note_* + chill_basis_* +
region_notes_*: sour cherry is high-chill (~700-1,000 hr vs the valley's [250,450] band, ~2x),
with no low-chill cultivar to bridge the gap (unlike sweet cherry's Royal Lee / Minnie Royal),
so it is marginal in the warm core and suited to the county's coolest/highest sites; low-chill
selection helps but does not close the gap. A3 stays coherent (marginal + calendar/harvest kept,
same shape as apple/pear). **cherry-sweet left fruits_reliably (unchanged).**

### MINOR polish
- M1: dropped "Shape A" build-term leak in beefsteak-tomato harvest_start note ("slowest of the
  Shape A tomatoes" -> "slowest tomato here"). habanero's leak removed by the C1 rewrite.
- M2: reworded schema token `heat_pause` out of consumer prose -- okra + sweet-potato
  region_notes_seasoned, pole-beans region_notes_seasoned + harvest_end note ("no summer pause
  in bearing" / "without a pause in growth" / "no summer pause is marked").
- M4: mulberry + pomegranate (trees) -- "warm-arid" (echoes internal region id) -> "warm desert"
  in both suitability_note_seasoned and region_notes_seasoned.
- M3 (optional per reviewer -- basis names Jun-Aug while pause codes [7,8,9]): left as-is; the
  reviewer explicitly rules the [7,8,9] choice correct and the tidy optional.

## Re-gate results
```
region_harness utah_dixie 8 ...warm.json habanero        -> GATE: PASS
region_harness utah_dixie 8 ...warm.json cayenne-pepper  -> GATE: PASS
region_harness utah_dixie 8 ...warm.json jalapeno        -> GATE: PASS
region_harness utah_dixie 8 ...warm.json edamame         -> GATE: PASS
region_harness utah_dixie 8 ...trees.json cherry-sour    -> GATE: PASS
region_cell_audit utah_dixie ...warm.json    -> 0 issue(s) across 42 cell(s)
region_cell_audit utah_dixie ...trees.json   -> 0 issue(s) across 14 cell(s)
```
Both files still exact compact JSON (`separators=(",",":")`, `ensure_ascii=False`, no trailing
newline). Residual build/schema-token leak sweep across both files: 0.

## Confirmation
**Hot chiles show harvest; cherry-sour = marginal.**
habanero 4 / cayenne 5 / jalapeno 3 harvest tokens (no all-heat_pause strip); cherry-sour
suitability == "marginal", cherry-sweet == "fruits_reliably" (untouched).
