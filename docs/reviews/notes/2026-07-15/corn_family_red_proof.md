# Dry-corn §E shape: adversarial RED proof (field-corn, representative for all 3 corns)

Task 2 of the corn-family arc. CLAUDE.md requires every new/reused gate surface to be
adversarially stress-tested before it is trusted: inject the defect class into a scratch copy,
confirm it bounces. field-corn, popcorn, and flint-corn share the same §E shape (dry-down
`growth_stages` ladder ending in a `harvest` stage then a `cure_thresh` curing stage, the same
register fields, the same 12-region roster), so one proof against the validated field-corn
exemplar covers all three -- the dry-bean / sweet-corn one-proof-per-arc precedent.

## Setup

Scratch canonical built by loading the real `crops_data_final.json` READ-ONLY and appending the
validated exemplar `/private/tmp/field_corn.json` at `$.crops[<len>]`, written to
`/tmp/corn_red_scratch.json`. Canonical source dict itself is never mutated; only the in-memory
copy is written out.

Green baseline, confirmed via the real invocation (positional slug, positional path):

```
python3 tools/whole_crop_gate.py field-corn /tmp/corn_red_scratch.json  -> GATE: PASS
python3 tools/gate_all.py /tmp/corn_red_scratch.json                     -> gate_all: PASS (117 certified crops)
```

Each defect below is injected on a fresh deep copy of the field-corn object, spliced into a
fresh copy of the real canonical, written to `/tmp/corn_red_scratch.json`, and run through the
identical `whole_crop_gate.py field-corn /tmp/corn_red_scratch.json` subprocess invocation. Each
assertion checks BOTH that the violation list is non-empty AND that the expected substring(s)
are present in the joined violation text (non-vacuous).

Canonical `crops_data_final.json` was read-only throughout. SHA before and after this task:
`c73d7fa001aac43ff98ac8c5fcf0106dd4cf16623cd6fd2d129e00c16759d7d3` (matches `LATEST.txt`),
unchanged. Working tree was clean before and after (aside from this note).

Harness: `/private/tmp/corn_red_proof.py` (re-runnable, `python3 /private/tmp/corn_red_proof.py`).

## Results: 6/7 defect classes bounced as expected; 1 confirmed no-op + 1 mis-attributed gate

| # | Defect class | Mutation | Expected substring | Result |
|---|---|---|---|---|
| 1 | non-monotonic `growth_stages.day_range_from_sow` | `silking.day_range_from_sow` set to `[5,8]` (min drops below the prior stage's min) | `non-decreasing` | BOUNCED (1 violation): `timing-spine: field-corn: ladder mins non-decreasing violated at 'silking' (5 < 55) up to the harvest anchor` |
| 2 | dropped `germination_light` | delete the key entirely | `germination_light` | BOUNCED (1 violation): `register-coverage: field-corn: #6 germination_light missing (present-or-null: null == no home-from-seed path)` |
| 3 | absurd `days_to_maturity` | `[7, 9]` | `days_to_maturity` | **DID NOT BOUNCE** (`GATE: PASS`, 0 violations). `[7,9]` sits INSIDE the universal `numeric_sanity` `[7,400]` floor -- the sweet-corn finding, reproduced here. Checked both A33 (numeric sanity) and A34 (cross-consistency): neither fires: `[7,9]` is internally consistent (min <= max, both positive) and the floor bound is a wide `[7,400]` band with no crop-class-aware tightening. This is a known, already-logged gap, not a defect in this proof. |
| 4 | em dash in a consumer-facing string | appended `" Note — field corn differs."` to `description_seasoned` | `dash` | BOUNCED (1 violation): `dash: description_seasoned: 'Field corn (Zea mays var. indentata), or dent corn, is a tall, frost-tender warm...'` |
| 5 | bad enum `calendar_basis` | `calendar_basis:"bogus"` | `calendar_basis` | BOUNCED (1 violation): `calendar_basis: calendar_basis 'bogus' is not a known base [...]; an unknown/typo/case-slip/novel basis silently no-ops EVERY calendar gate (A3/A4/A5/A6/A9/A10/A11/A13/A14/A15/A16/A24/A28)` |
| 6 | dropped canonical region (11/12) | delete `regions.pnw` | `region-roster` | BOUNCED (1 violation, A31): `region-roster: non-indoor crop is missing canonical region(s) ['pnw'] (has 11/12); the 12-region roster is the coverage floor` |
| 7 | `growth_stages` missing the `harvest` id | rename the `harvest` stage's `id` to `maturity` (stage object stays, day_range_from_sow untouched) | `harvest` | BOUNCED (2 violations) -- but via **A12** (`compound_population_gate` / tips rendering-conformance), not A40 as originally expected. See deviation note below. |

Every assertion checked both that the violation list was non-empty AND that the expected
substring was present in the joined violation text.

Full harness output:

```
BASELINE: field-corn appended to real canonical -> GATE: PASS (confirmed)

DEFECT (non-monotonic day_range_from_sow): BOUNCED, 1 violation(s)
    VIOLATION: timing-spine: field-corn: ladder mins non-decreasing violated at 'silking' (5 < 55) up to the harvest anchor

DEFECT (dropped germination_light): BOUNCED, 1 violation(s)
    VIOLATION: register-coverage: field-corn: #6 germination_light missing (present-or-null: null == no home-from-seed path)

DEFECT (absurd days_to_maturity [7,9]): DID NOT BOUNCE (GATE: PASS), 0 violation(s)
    NOTE: [7,9] sits INSIDE the universal numeric_sanity [7,400] floor (sweet-corn finding) -- expect this NOT to bounce A33; see if it bounces elsewhere (e.g. cross-consistency).

DEFECT (em dash in consumer string (description_seasoned)): BOUNCED, 1 violation(s)
    VIOLATION: dash: description_seasoned: 'Field corn (Zea mays var. indentata), or dent corn, is a tall, frost-tender warm'

DEFECT (bad enum calendar_basis='bogus'): BOUNCED, 1 violation(s)
    VIOLATION: calendar_basis: calendar_basis 'bogus' is not a known base ['berries_woody', 'frost_anchored', 'non_seasonal_indoor', 'perennial_chill_gated', 'perennial_evergreen', 'perennial_herbaceous', 'perennial_woody_ornamental']; an unknown/typo/case-slip/novel basis silently no-ops EVERY calendar gate (A3/A4/A5/A6/A9/A10/A11/A13/A14/A15/A16/A24/A28), so the crop's whole calendar layer would be validated by nothing

DEFECT (dropped canonical region (pnw) -- 11/12): BOUNCED, 1 violation(s)
    VIOLATION: region-roster: non-indoor crop is missing canonical region(s) ['pnw'] (has 11/12); the 12-region roster is the coverage floor -- a partial/empty roster certifies a crop that renders for almost nowhere

DEFECT (growth_stages missing the 'harvest' id (renamed to 'maturity')): BOUNCED, 2 violation(s)
    VIOLATION: tips conformance -- tips_by_stage['harvest']: ORPHANED key (not a growth_stage id) -- renderer reads tipsByStage[stage.id], so these tips never render
    VIOLATION: tips conformance -- tips_by_stage: growth_stage 'maturity' has NO renderable tip (coverage gap) -- the journey card renders a blank tip slot for that stage

6/7 defect classes bounced with the expected substring(s) present (defect 3 confirmed a known,
pre-logged gap rather than a proof failure; defect 7 bounced under a different gate than
originally attributed).
```

## Deviation note: defect 7 bounces via A12, not A40

The task brief expected "`growth_stages` missing the `harvest` id" to trip A40 (`timing_spine_gate`
ladder monotonicity). Traced empirically (both via `timing_spine_gate.timing_spine_violations`
called directly, and via the full gate subprocess): it does **not**.

Why: `timing_spine_gate._harvest_index` matches the stage with `id == "harvest"`, falling back to
`len(stages) - 1` (the last stage) when no such id exists. On the real field-corn ladder, `harvest`
is stage 8 of 9 -- `cure_thresh` (the curing stage) comes after it. Renaming `harvest`'s id shifts
the anchor to `cure_thresh` (index 8), which merely *extends* the monotonic-min check window by one
stage. Since the real ladder (`germination` 0, `seedling` 10, `vegetative` 20, `tasseling` 55,
`silking` 60, `kernel_fill` 72, `dry_down` 95, `harvest` 110, `cure_thresh` 125) is already
non-decreasing front-to-back, the extended window still passes -- A40 stays clean.

The break instead surfaces via **A12** (`compound_population_gate.tips_violations`): field-corn's
`tips_by_stage` dict is keyed by growth-stage id, including a real `harvest` entry. Once no
`growth_stages` item carries `id == "harvest"`, that key becomes an ORPHANED key (the renderer
reads `tipsByStage[stage.id]`, so those authored tips never render), and the new `maturity` id
shows up as a growth stage with no renderable tip (a coverage gap). Both violations correctly
reference `harvest`, so the substring assertion (`harvest`) still passes -- the defect class is
genuinely caught by the gate suite, just by a different, more directly-relevant gate (A12's
stage-id/tips-key consistency check) than A40's ladder-monotonicity check. This is the corn-arc's
equivalent of the sweet-corn DTM-floor finding: a documented, empirically-verified deviation
between the brief's expected gate attribution and the suite's actual behavior, not a gate gap.

## Conclusion

The gate suite correctly rejects 6 of 7 targeted defect classes on the real, validated field-corn
shape, with the 7th (`days_to_maturity` inside the universal `[7,400]` floor) confirming a
pre-existing, already-logged gap rather than a new one, and the `harvest`-id defect confirming
real (if differently-routed) coverage. Since field-corn, popcorn, and flint-corn share this exact
§E shape (dry-down ladder + register fields + 12-region roster), this proof is taken as
representative for all three corns, per the dry-bean / sweet-corn one-proof-per-arc precedent.
Canonical `crops_data_final.json` was never written; SHA unchanged throughout.
