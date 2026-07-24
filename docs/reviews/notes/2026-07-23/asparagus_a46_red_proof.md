# herbaceous_perennial archetype (asparagus GS arc) -- A46 RED-proof + footprint verification (2026-07-23)

Design-first arc: register the `herbaceous_perennial` archetype, build + wire the A46 structural cert
gate (TDD), and author a staged reference (`tools/staging/asparagus_reference.json`, finalized at commit
`c25f9f0`) to the newest-standard bar. This note is the adversarial proof that A46 actually catches every
defect class it claims to, plus confirmation that none of this touched the certified canonical.

## A46 RED battery (12 defect classes injected into the REAL staged reference; must bounce)

Per CLAUDE.md ("a gate isn't done until a defect has been sneaked at it and caught"), each defect was
injected via `copy.deepcopy` of the clean, gate-passing reference, one mutation at a time, and checked
against `herbaceous_perennial_violations`:

1. `perennial_false` -- `perennial: True -> False` -- bounced.
2. `lifecycle_annual` -- `lifecycle -> "annual"` (outside the `{perennial, permanent}` enum) -- bounced.
3. `succession_suitable` -- `succession_policy.suitable: False -> True` -- bounced.
4. `no_reason` -- `succession_policy.reason_seasoned -> None` -- bounced.
5. `yfh_empty` -- `years_to_first_harvest -> []` (empty) -- bounced.
6. `yfh_zero` -- `years_to_first_harvest -> [0]` (min must be >= 1) -- bounced.
7. `pls_null` -- `productive_lifespan_years -> None` -- bounced.
8. `succession_track` -- appended a `{"track": "succession"}` planting to `northern_tier` -- bounced.
9. `bad_suitability` -- `northern_tier` zone 4 `suitability -> "fruits_reliably"` (outside
   `SUITABILITY_ENUM = {perennializes, marginal, unsuitable}`) -- bounced.
10. `unsuitable_no_note` -- popped `suitability_note_seasoned` off the `unsuitable` `hawaii_tropical`
    zone 12 cell -- bounced.
11. `empty_calendar` -- `northern_tier` zone 4 `calendar -> []` (violates the A32 honesty floor: a
    filled cell must carry a non-empty calendar) -- bounced.
12. `rotation_null` -- `rotation -> None` -- bounced.

Baseline: the clean reference (`tools/staging/asparagus_reference.json`, commit `c25f9f0`) passes with
`herbaceous_perennial_violations(base) == []` before any mutation is applied.

**Result: 12/12 defect classes bounced.** Console output:

```
  bounced: perennial_false
  bounced: lifecycle_annual
  bounced: succession_suitable
  bounced: no_reason
  bounced: yfh_empty
  bounced: yfh_zero
  bounced: pls_null
  bounced: succession_track
  bounced: bad_suitability
  bounced: unsuitable_no_note
  bounced: empty_calendar
  bounced: rotation_null
A46 RED battery: all defect classes caught
```

## Standalone-gate greens on the staged reference (re-run, all clean)

- `herbaceous_perennial_gate` unit suite (`tools/test_herbaceous_perennial_gate.py`) -- **all tests
  passed** (17 cases incl. the accepted-value branch and non-list-type guard).
- `control_ladder_gate` unit suite (`tools/test_control_ladder_gate.py`) -- **OK** (catalog, ladder,
  identity + coverage tests).
- `variety_resistance_gate` unit suite (`tools/test_variety_resistance_gate.py`) -- **all tests passed**.
- Crop-specific checks against the staged reference itself:
  - `A46 (herbaceous_perennial_violations)`: **[]**
  - `resistance (resistance_violations)`: **[]**
  - `control_ladder (ladder_violations)`: **[]**
  - `control_ladder (identity_violations)`: **[]**
- `control_ladder_gate` whole-catalog baseline (`python3 tools/control_ladder_gate.py
  crops_data_final.json`): **`control_ladder_gate: 0 violation(s)`** -- the real `control_methods` /
  `source_catalog` catalog stays clean (the staged reference is not merged into the canonical, so this
  is a baseline confirmation, not a reference-inclusive run).

These reconfirm Task 4's own gate run (post the class-attribution + spacing fixes) rather than
introducing a new result.

## Footprint proof (canonical untouched)

```
$ python3 tools/gate_all.py crops_data_final.json
gate_all: ran whole_crop_gate on 119 certified crop(s)
gate_all: PASS -- every certified crop passes the whole suite

$ git status --porcelain crops_data_final.json
(empty)

$ shasum -a 256 crops_data_final.json
ccf5e8902e07a2f967ec277b33ee8f6171d0b159c4ceed1072447a23a1f4635a  crops_data_final.json
canonical UNTOUCHED (ccf5e890)
```

- `gate_all`: **119/119 certified crops PASS** the whole 18-gate suite. Roster count unchanged.
- `git status --porcelain crops_data_final.json`: **empty** -- no working-tree change to the canonical.
- Canonical SHA-256: **`ccf5e8902e07a2f967ec277b33ee8f6171d0b159c4ceed1072447a23a1f4635a`**, matches
  `LATEST.txt` (`ccf5e890...`, the ladybug consumer-copy sweep release). **Byte-untouched** across the
  entire archetype-registration + gate + staged-reference arc (commits `0ad48f5`..`c25f9f0`).

This whole arc -- archetype registration, the new A46 gate + its unit tests, wiring into
`whole_crop_gate`, and the fully-authored `asparagus_reference.json` staged content -- lives entirely in
`tools/`, `tools/staging/`, and `docs/`. `crops_data_final.json` was never opened for write, consistent
with CLAUDE.md's READ-ONLY-during-gate-work rule (no explicit promote task was issued this arc).

## Design-first boundary (explicit, not implicit)

This arc is **design-first, not a certification**. What shipped:
- The `herbaceous_perennial` archetype registered (frost_anchored calendar basis).
- The A46 structural gate, TDD-built and now adversarially RED-proven against the real reference shape
  (this note).
- A46 wired into `whole_crop_gate` (fires only for `archetype == "herbaceous_perennial"`; no-op for the
  119 certified crops, confirmed by the unchanged `gate_all` PASS above).
- One staged, fully-authored reference crop (asparagus) covering **2 of 16 regions**
  (`northern_tier` zone 4 perennializes / `hawaii_tropical` zone 12 unsuitable), plus its
  `control_ladder` (asparagus beetles, rust, Fusarium crown rot) and per-variety `resistance` map
  (4 varieties: Millennium graded `susceptible` on rust and honest-N/A on Fusarium per T1 evidence,
  Jersey Knight `tolerant`/`tolerant`, Mary Washington and Purple Passion carrying no resistance map).

What did NOT ship, and is explicitly deferred to the follow-on arc:
- The remaining **14 of 16 regions** for asparagus (only northern_tier and hawaii_tropical are
  authored; the other 14 region cells are untouched/empty).
- Promoting asparagus from staged reference to a certified 120th roster entry (would require the full
  16-region fan-out, a promote task, and full release verification per CLAUDE.md protocol #6).
- Applying the `herbaceous_perennial` archetype to artichoke (the other honest-shell crop this archetype
  targets), on the same reference-shape pattern once asparagus's fan-out lands.
- Any A46 hard-flip / roster-wide enforcement decision -- moot until more crops actually use the
  archetype.

`tools/staging/asparagus_reference.json` remains staging content: valid against all three standalone
gates, but not merged into `crops_data_final.json`, and the crop is not part of the 119-certified/128
count.
