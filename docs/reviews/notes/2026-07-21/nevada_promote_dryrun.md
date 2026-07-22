# Nevada region promote -- scratch dry-run record

**Date:** 2026-07-21. **Batch:** `tools/batches/nevada_region_promote.json` (118 patches).
**Base canonical:** `a071f0c1` (SHA-guarded; confirmed unchanged at dry-run time).
**Driver:** `scratchpad/nv_dryrun.py` (apply batch to a scratch copy -> full gate suite via
`region_harness.build_scratch_tools` (nevada in EXPECTED_SPANS) -> footprint audit -> RED checks).

## Batch shape (verified)
118 patches = **111 `regions.nevada` cells** (all `op:add`, net-new) + `region_chill_delivered.nevada`
(add, `{"8":[500,900],"9":[300,700],"10":[150,450]}`) + `region_chill_delivered_provenance` (replace =
append the nevada note to the global string, `value.startswith(from)` verified) + **5 `source_catalog`
adds** (`nws_vef`, `unlv_mg_svn`, `unr_fs0261`, `unr_sp2007`, `unr_sp9911`). Scratch out-SHA
`320df2ea...`.

## Full gate suite (scratch canon + scratch tools) -- GREEN
| gate | result |
|---|---|
| `gate_all.py` (whole suite on every certified crop) | **119/119 PASS** |
| `zone_span_gate.py` (A45) | 0 violations across 128 |
| `chill_gate.py` | 0 violations |
| `second_planting_gate.py` (A43) | 0 violations (rules=AB, 128 crops) |
| `photoperiod_gate.py` (A9) | validated inside `whole_crop_gate` via gate_all (onion/shallot 0); standalone CLI emits nothing by design |
| `coverage_floor_gate.py` (A31/A32) | 89 = **PRE-EXISTING** (identical 89 on the base canonical; the 9 uncertified shells' mushroom/indoor-collapse pattern, same as RGV/PNW/mid-South; gate_all's certified-only view is authoritative) |
| `calendar_coherence_gate.py` | 0 (0 growing-after-harvest + 0 harvest-hole) |
| `prose_window_sweep.py` | 0 prose date mentions with no matching resolved window (TOL=4d) |

## Footprint audit (byte-level, scratch vs real canonical) -- EXACT
- count 128 unchanged; `total_crops` 128.
- **111 crops changed, all 111 gained EXACTLY `regions.nevada`; 0 crops changed beyond the added
  nevada cell.**
- 0 top-level keys added/removed (only `region_chill_delivered` + provenance mutated in place).
- `source_catalog` +5 (the new ids), -0.
- COMPACT: no trailing newline, no `", "` spacing, **0 escaped-unicode** (`\u` count 0).

## RED checks (each injected defect must BOUNCE) -- ALL BOUNCED
- **A45** drop the `"8"` key from `cherry-tomato.nevada` (+ span -> `["9","10"]`) -> `zone_span_gate`
  rc=1 BOUNCED.
- **A43** comma-join `cucumber.nevada.9` `plant_out` ("Mar 10 - Apr 20, Aug 1 - Aug 20") alongside its
  `second_planting` -> whole_crop_gate BOUNCED (*"demux: plant_out still multi-window alongside
  second_planting"*).
- **A9** keep `onion.nevada` `intermediate_day` but move `plant_out` to April -> whole_crop_gate
  BOUNCED (3 zone violations: *"intermediate_day but plant_out window [4] includes
  late-spring/summer months (intermediate-day onions are fall-to-early-spring-planted)"*). Confirms the
  onion-daylength window-fit coupling is live. (Note: `long_day`+April is NOT a defect -- long-day
  onions are legitimately spring-planted; the forbidden combo is intermediate/short-day + a spring set,
  which the real fall-planted `intermediate_day` cells avoid by construction.)

## release_verify
`release_verify.py` is single-crop-pilot-shaped (section A expects only the promote-target slug to
change); a roster-wide 111-cell column trips its collateral check by design, same as RGV/PNW/mid-
Atlantic/mid-South. The binding regression proof is the byte-level footprint audit above + the
pre-commit backstop (`precommit_release_verify.py`, which checks ALL changed crops) at commit.

## Verdict: GO
Gate suite green, footprint exact, all three defect classes (zone-parity / fall-envelope / photoperiod
window-fit) RED-proven at roster scale. Cleared for the atomic promote (Task 11).
