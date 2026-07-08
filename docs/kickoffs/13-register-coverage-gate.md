# Kickoff: register-coverage HARD gate (retroactive #4-#7 + #6)

**Created 2026-07-07** (register #6 session, on Trevor's decision). Register:
`docs/field_addition_register.md` entry #8. This closes a real gap Trevor flagged at the end of #6:
*"moving forward for new crops, are we creating gates to make sure all of this happens?"* Today the
answer is **no** -- and this kickoff builds the gate that makes it yes.

## 0. The problem (why this exists)

The register fields shipped so far -- #4 timing spine (`propagule`/`dtm_anchor`/`sow_depth_inches`/
`thin_to_inches`/`harvest_window_days`/`day_range_from_sow`), #5 `watering.schedule_by_stage`, #6
`germination_light`/`seedling_light`, #7 `heat_threshold_f`/`heat_effect`/`frost_tolerance_f`/
`frost_effect`/`chilling_sensitivity_f` -- are guarded only **softly**:

1. Each field's **standalone gate validates shape only WHEN the field is present** ("unauthored roster
   stays green" -- deliberate, so partial rollout is green). A new crop that simply OMITS the field
   passes clean.
2. "Fold into the per-crop GS-arc checklist" is a **process step, not a programmatic gate.**

A `grep` for required-field enforcement across `whole_crop_gate.py` / `release_verify.py` returns
NOTHING for the register fields. So a newly-certified crop (or the 10 uncertified §E shells at their
certification) could silently ship WITHOUT any of them -- the backfill-treadmill the field-register
warns about.

## 1. The fix (the proven pattern)

The machinery already exists and is proven in the suite: **`whole_crop_gate` A17** (`npk_ratio`
present-or-explicit-null, UNIVERSAL) and **A20** (display-readiness field presence). The pattern:
*every crop must carry this field or an explicit null/N-A sentinel; no-op only for the field's defined
legit-N/A archetype.* The register fields never got this treatment.

Build a **register-coverage hard gate** -- new A-number(s) in `whole_crop_gate.py` (or a dedicated
`tools/register_coverage_gate.py` wired into the Step-11 suite) that, for each SHIPPED register field,
requires every **certified** crop (`verification_status.status == "verified_gs_arc"`) to carry the
field **or its defined null/N-A**, exempting:
- the **10 uncertified §E shells** (artichoke/asparagus/avocado/olive/sweet-corn + 5 mushrooms), and
- the field's **defined legit-N/A cases** -- reuse the standalone gates' rules verbatim:
  - #6: `germination_light` null allowed iff `propagule != seed` (no-home-seed-path); `seedling_light`
    `na` is a real value; microgreens IN-scope. (`tools/seedling_light_gate.py`.)
  - #7: `INDOOR_SLUGS` = the 8 microgreens are N/A-indoor for climate. (`tools/climate_threshold_gate.py`.)
  - #5: the sparse-tree watering pattern (subset of stage ids) for the 10 perennials.
  - #4: empty-DTM perennials carry no dtm_anchor/ladder/sow_depth; `spacing_inches==[]` microgreens
    exempt from sow_depth/thin_to. (`tools/timing_spine_gate.py` already encodes these.)

## 2. Scope (Trevor 2026-07-07): RETROACTIVE #4-#7 + #6

All four register passes are complete on the stable 114 roster, so one gate covers everything shipped:
- **#4** timing spine, **#5** `watering.schedule_by_stage`, **#6** germination/seedling light, **#7**
  climate thresholds.

**Critical timing rule:** turn the hard requirement on **PER FIELD only AFTER that field's rollout is
complete** -- otherwise it fails on an in-progress roster. All four are done now, so all four can go on
at once. (Any FUTURE register field stays soft until its own rollout completes, then joins this gate.)

## 3. Method (same discipline as every gate here)

1. **TDD, RED before GREEN.** Inject the defect class into a SCRATCH COPY of the real canonical: a
   certified crop MISSING a required field (not its null/N-A) -> must bounce; a certified crop with the
   field or its legit null -> green; an uncertified §E shell missing everything -> green (exempt); a
   legit-N/A case (microgreen climate, no-home-seed-path germination_light null) -> green. Confirm the
   clean canonical is GREEN before trusting it. (Model: `tools/test_seedling_light_gate.py`.)
2. **Wire into the Step-11 suite** as new A-number(s), or a dedicated gate the suite calls. Keep the
   per-field N-A predicates DRY by importing them from each field's standalone gate rather than
   re-encoding.
3. **Regression:** `whole_crop_gate` 18/18 still PASS on the current canonical (all 114 certified carry
   all four register sets today, so the gate should be GREEN on first run -- if it is not, that IS a
   real coverage gap it just caught, which is the point).
4. **No state trio / no canonical change** -- this is tooling only (READ-ONLY on `crops_data_final.json`).
   Commit the gate + its test; Trevor confirms the push.

## 4. Payoff

Converts "fold into the checklist" from a promise into an enforced invariant: **a new crop cannot
certify without the register fields (or their explicit null/N-A).** Stops silent coverage drift as the
roster grows (the 10 §E shells at their certification, plus any future crops). This is the durable
answer to Trevor's question.

## 5. Start here
- Read `docs/field_addition_register.md` #8 + this file.
- Confirm SHA/git state (`shasum -a 256 crops_data_final.json` == `LATEST.txt`).
- Read `whole_crop_gate.py` A17 (`npk_gate.npk_ratio_violations`) + A20 as the templates.
- Read the four standalone gates for the N-A predicates to reuse: `timing_spine_gate.py`,
  `climate_threshold_gate.py`, `seedling_light_gate.py` (+ the #5 watering shape rule in
  `whole_crop_gate`/`register_fill_gate`).
