# sweet-corn -- adversarial RED gate proof (Task 5)

**Date:** 2026-07-10. Each defect class injected into the CERTIFIED sweet-corn draft
(`verification_status.status="verified_gs_arc"`) on a scratch copy of the full canonical; the
always-on suite (`tools/whole_crop_gate.py sweet-corn <copy>`) must bounce it (CLAUDE.md
adversarial rule: "a gate isn't done until a defect has been sneaked at it and caught"). `main`
(`crops_data_final.json`) was never touched -- all injection ran against a scratch copy of the
as-if-certified canonical, one fresh copy per defect.

## GREEN baseline

```
python3 tools/whole_crop_gate.py sweet-corn <baseline canonical, sweet-corn as-if certified>
```
Result: `GATE: PASS` -- `exit=0`. All checks report 0 violations, including the new A44
(`planting_layout violations: 0`), A40 (`timing-spine value-shape violations: 0`), A39
(`register-coverage violations: 0`), A33 (`numeric sanity violations: 0`), and C/D
(`user-facing dash hits: 0`). Confirms the clean draft is the correct starting point for
adversarial injection.

## Defect matrix

| # | Defect injected | Expected check | exit | Actual VIOLATION line |
|---|---|---|---|---|
| 0 | (none -- clean baseline) | -- | 0 | `GATE: PASS` |
| 1 | `planting_layout` -> `"blocks"` (bad enum) | A44 | 1 | `planting_layout: sweet-corn: planting_layout 'blocks' not in ['block', 'grid', 'hill', 'row', 'single']` |
| 2 | delete `pollination_block_min_rows` while `planting_layout=="block"` | A44 | 1 | `planting_layout: sweet-corn: planting_layout 'block' but pollination_block_min_rows missing` |
| 3 | `pollination_block_min_rows=4` fabricated onto `planting_layout:"row"` | A44 | 1 | `planting_layout: sweet-corn: planting_layout 'row' (not 'block') but pollination_block_min_rows present` |
| 4 | `pollination_block_min_rows` -> `1` (below floor of 2) | A44 | 1 | `planting_layout: sweet-corn: pollination_block_min_rows 1 not an int >= 2` |
| 5 | swap `kernel_fill`/`harvest` `day_range_from_sow` so `harvest[0]` (55) < `kernel_fill[0]` (68) | A40 | 1 | `timing-spine: sweet-corn: ladder mins non-decreasing violated at 'harvest' (55 < 68) up to the harvest anchor` |
| 6 | delete `heat_threshold_f` (register field #7) | A39 | 1 | `register-coverage: sweet-corn: #7 heat_threshold_f missing (present-or-null required; INDOOR_SLUGS are the only N/A)` (also trips A41 as a bonus: `climate-shape: sweet-corn: heat_effect present but no heat_threshold_f key (orphan)`) |
| 7 | `days_to_maturity` -> `[7, 9]` (absurd for corn) | A33 (numeric-sanity) | **0** | **NONE -- gate reports `numeric sanity violations: 0`, `GATE: PASS`.** |
| 8 | em dash (U+2014) appended to `soil.preferred_texture_beginner` | C/D dash gate | 1 | `dash: soil.preferred_texture_beginner: 'Corn grows best in deep, rich, well-drained soil like loam. Because it grows tal...'` |

**7/8 defect classes bounce as specified.** Defect 7 does NOT bounce -- see gap below.

## Real gap: defect 7 (days_to_maturity absurdity) does not bounce

`tools/numeric_sanity_gate.py` bounds `days_to_maturity` to the single universal band
`[7, 400]` (see its docstring: "nothing edible matures < 7 days"). This band is deliberately
crop-agnostic -- unlike `spacing_inches`, which the same gate splits by archetype
(non-tree `[1,72]` vs tree/woody `[1,360]`), `days_to_maturity` has no per-archetype or
per-crop tightening. `[7, 9]` sits inside `[7, 400]`, so it reads as "physically plausible"
to the gate even though 7-9 days is absurd for corn (sweet-corn's own baseline value is
`[60, 90]`). This is a pre-existing, documented gate limitation, not a defect introduced by
this task -- it matches the memory note `variety-dtm-load-bearing-deferred` (numeric_sanity's
`[7,400]` floor was added 2026-07-07 as a deliberately coarse bridge; a tighter, load-bearing
DTM gate was explicitly deferred pending a ~10-variety GS-arc pilot).

For context (not part of the required 8, run to confirm the gate mechanism itself is not
broken): injecting `days_to_maturity -> [3, 5]` (below the universal `[7,400]` floor) DOES
bounce -- `exit=1`, `VIOLATION: numeric-sanity: days_to_maturity [3, 5]: value(s) [3, 5]
outside the physical bound [7, 400]`. So A33 fires correctly on values outside its universal
band; it simply has no way to know that `[7,9]` (inside the band) is wrong specifically
*for corn*. Catching a within-band-but-wrong-for-this-crop DTM would require either a
per-archetype DTM band (like spacing's tree/non-tree split) or the cross-consistency layer
(A34) extended to cross-check DTM against the growth-stage ladder span (the ladder's own
`harvest` window already implies ~68-85 days here, which contradicts a `[7,9]` DTM -- a
future A34 rule, not yet built). Flagging this as a worklist item, not fixing it under this
task (task scope is proof-of-defense, not new-gate authoring).

## Confirms

- The existing gate suite protects the new greenfield sweet-corn crop for planting-layout
  coherence (A44, all 4 sub-cases), timing-spine ladder monotonicity (A40), register
  coverage (A39), and the dash/temperature notation scan (C/D). No new gate was needed for
  these four classes.
- `crops_data_final.json` (the canonical) was never modified; all mutation happened on scratch
  copies of the as-if-certified baseline.
- One real, pre-existing gap confirmed and recorded above: `numeric_sanity`'s universal
  `[7,400]` DTM floor does not catch a within-band-but-crop-implausible DTM (e.g. corn at
  `[7,9]`). Not remediated here per task scope; worklist candidate for a future A34
  DTM-vs-ladder cross-consistency rule or an archetype-aware DTM band.
