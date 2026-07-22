# Utah "Dixie" region promote -- scratch dry-run (Task 10)

**Date:** 2026-07-22. **Batch:** `tools/batches/utah_dixie_region_promote.json` (121 patches).
**Base canonical:** `b1045e04` (live at dry-run time). Applied to a scratch COPY; the real canonical was
never touched. Result: **GO** -- full suite green, footprint exact, three RED-checks bounce.

## base_sha guard
`live = b1045e0433c7` == `batch.base_sha = b1045e0433c7` -> match (apply_patch fails closed on drift).

## Footprint byte-audit (scratch vs base)
- Crops that gained `regions.utah_dixie`: **111** (expected 111).
- Crops touched BEYOND `regions.utah_dixie`: **0** (every one of the 128 crops is byte-identical once the
  new `utah_dixie` cell is removed).
- Top-level keys added/removed: **none** (`region_chill_delivered.utah_dixie` and the provenance append
  land inside existing top-level dicts/strings, not new top-level keys).
- `source_catalog` entries added: **8** (`usu_ext_veg_dates`, `usu_ext_tomato`, `usu_ext_wash_fruits`,
  `usu_ext_raspberry`, `usu_ext_garlic`, `usu_ext_fall_veg`, `usu_ext_wash_frost`, `usu_ext_peaches`) --
  all cited by cells (0 uncited), all T1 USU sub-ids.
- `region_chill_delivered.utah_dixie` = `{"8": [250, 450]}`.
- `total_crops` = 128; `len(crops)` = 128 (unchanged).
- COMPACT (no newlines), no trailing newline, no escaped-unicode (`\u`).

## Full gate suite (scratch tools with `utah_dixie` in EXPECTED_SPANS)
| gate | result |
|---|---|
| `gate_all.py` | **PASS -- every certified crop passes the whole suite (119/119)** |
| `zone_span_gate.py` (A45) | 0 violations (single-zone parity on "8") |
| `chill_gate.py` | 0 violations |
| `second_planting_gate.py` (A43) | 0 violations |
| `calendar_coherence_gate.py` | 0 violations (0 growing-after-harvest + 0 harvest-hole) |
| `prose_window_sweep.py` | 0 prose windows with no matching resolved window (TOL=4d) |
| `coverage_floor_gate.py` (A31/A32) | 89 violations = **PRE-EXISTING** (the 9 uncertified shells; identical **89** on the base canonical; `gate_all`'s certified-only PASS is authoritative -- the documented RGV/PNW/mid-Atlantic/mid-South/Nevada pattern) |

A9 (photoperiod) for onion/shallot is exercised inside `gate_all`'s per-crop `whole_crop_gate` run and was
independently confirmed 0 at authoring (region_harness: `intermediate_day`, fall plant_out Sep 26-Oct 5,
never April+).

## Adversarial RED-checks (proves the ceremony catches the defect classes at roster scale)
Each mutation applied to a scratch copy, gated, then discarded:
- **A45 span-parity:** injected a stray non-span `resolved_by_zone["9"]` into a `utah_dixie` cell (span
  still `["8"]`) -> `zone_span_gate` bounced (rc=1, 1 violation). BOUNCED.
- **A43 dedup:** comma-joined a second window into a cool crop's PRIMARY `plant_out` while it carries a
  `second_planting` (kale) -> `second_planting_gate` bounced (rc=1, 1 violation). BOUNCED.
- **A9 window-fit:** kept onion `intermediate_day` but moved `plant_out` to April (the forbidden spring
  set for an intermediate-day onion) -> `whole_crop_gate onion` bounced (rc=1). BOUNCED. (Confirms the
  flip is NOT a pure label change -- the memory `onion-daylength-intermediate-a9-window-fit` couples
  day_length_type to plant_out.)

## Verdict
**GO for the atomic promote (Task 11).** Footprint exact, suite green (the 89 coverage_floor is the
pre-existing uncertified-shell floor, identical on base), all three defect classes RED-proven to bounce.
