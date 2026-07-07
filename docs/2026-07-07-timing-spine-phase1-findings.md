# Timing-Spine Phase 1 -- gate build + surfaced tensions

**Date:** 2026-07-07 · **Canonical:** `4abf43a5` (read-only; NOTHING edited this phase) ·
**Scope:** the one-time cross-crop layer of the timing-spine authoring (Plan 3) -- field contract +
gate, before any per-crop authoring. **Method:** column GS arc (`gs_cross_crop_field_addition_v0.md`).

## What Phase 1 shipped (tooling only, canonical untouched)
- **`docs/timing_spine_contract.md`** -- the locked field spec (8 fields, enums, archetype rules, gate tiers).
- **`tools/timing_spine_gate.py`** + **`tools/test_timing_spine_gate.py`** -- TDD (RED, then GREEN);
  every check has a sneaked-defect assertion, including the two calibration cases below
  (`shallot`-class monotonic defect caught; `chives`-class post-harvest cyclic dip exempt).
- Field-addition register row added (bundle entry).

## Gate baseline on `4abf43a5`
`timing_spine_gate.py` -> **1 hard violation, 8 warnings, propagule 0/124** (the whole roster is the
authoring TODO, as expected -- the 6 new columns are 0% populated; `day_range_from_sow` exists on 35
crops from certification). No-scope exit = 1 **solely because of the one real defect below.**

## Tension A -- `shallot` ladder out of order (REAL defect, gate hard-fail)
`shallot.growth_stages` mins are `[7, 21, 70, 95, 90]` -- `maturity_curing` (min **90**) starts
*before* `bulb_sizing` (min **95**), which is contradictory. Its sibling `onion` is correctly
ordered (`bulb_sizing [100,130]` -> `maturity_curing [110,140]`). This is a genuine authoring
inconsistency, not a false positive.
- **Recommended disposition:** fix as a 1-line correction **when shallot is authored** (it is an
  allium in the fall/winter batch anyway) -- bump `maturity_curing` to begin at/after `bulb_sizing`
  (mirror onion: `[110,140]`), with per-field provenance. Until then the gate is honestly RED-by-1
  on canonical. **No edit made now** (gate work surfaces; it does not one-off edit -- CLAUDE.md).

## Tension B -- 8 harvest-vs-DTM warnings (anchor-dependent, resolve during authoring)
Harvest-stage entry sits outside a +/-15% DTM band for: beefsteak-tomato, basil, heirloom-tomato,
grape-tomato, lettuce-leaf, cilantro-coriander, tomatillo, celery. Diagnosis:
- **`celery` is actually CORRECT** -- ladder `[150,200]` reconciles with DTM `[80,120]` once you know
  it is `from_transplant` (+10 weeks indoors = ~70 days). Proof that the check must be anchor-aware,
  which is why it is a WARNING, not a hard fail.
- **beefsteak / heirloom / grape-tomato** share a templated harvest entry `[55,80]` not individualized
  to each cultivar's DTM (75-90 / 70-90 / 65-75). A real (minor) authoring imprecision.
- **basil / lettuce-leaf / cilantro** are cut-and-come-again -- early harvest below DTM is legitimate.
- **Disposition:** no separate action. Authoring `dtm_anchor` (and individualizing the tomato
  ladders) during the per-crop pass resolves these; re-run `--warnings` per batch to confirm they clear.

## Gate-design decisions made (for ratification)
1. **Monotonic-min is HARD but only up to the harvest anchor** (`id=='harvest'`, else last stage);
   post-harvest cyclic stages are exempt. Catches `shallot`; exempts `chives`. (Runbook §5.1 said
   "non-decreasing down the ladder"; this scopes it so perennial dormancy/regrowth overlap does not
   false-positive.)
2. **Harvest-vs-DTM is a WARNING, not a hard fail** -- inherently anchor-dependent + cut-and-come-again.
3. **Microgreens** (`spacing_inches == []`) are exempt from BOTH `sow_depth_inches` and `thin_to_inches`
   (surface-broadcast; no per-plant spacing/depth).
4. **Provenance excludes `day_range_from_sow`** (pre-existing at cert); only the 6 new columns demand a
   `field_additions` entry.

## Next
Phase 2 -- author **garlic** first (per the runbook), then the fall/winter batch. Fix shallot in that
batch. Canonical writes begin at garlic (an explicit authoring task); state trio at each content release.
