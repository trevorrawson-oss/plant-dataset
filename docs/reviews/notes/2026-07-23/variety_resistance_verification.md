# Variety disease-resistance pilot -- release verification (2026-07-23)

Canonical `7b1aa59d` -> `89d37c1a` (branch `worktree-variety-resistance`). Real apply byte-identical to
the fully-gated scratch (out SHA `89d37c1a` from both the dry-run and the in-place apply).

## Gate battery (on the patched scratch AND re-run on the real canonical)
- `variety_resistance_gate` -- **0** violations.
- `control_ladder_gate` -- **0** violations (incl. the 20 new ladders + the vertebrate coherence).
- `whole_crop_gate apple` / `whole_crop_gate strawberry` -- **PASS** (both via `gate_all`'s full suite).
- `gate_all` -- **119/119 PASS** (every certified crop passes the whole 18-gate suite).
- `register_completeness_gate` -- **PASS**, 0 unruled prose fields.

## Adversarial RED battery (each defect injected into the REAL patched data; must bounce)
Baseline (both gates) clean, then:
1. Dangling `resistance` id (`appel-scab`) -> `variety_resistance_gate` bounces (referential). PASS
2. Invalid grade (`super_resistant`) -> `variety_resistance_gate` bounces (enum). PASS
3. Insecticide (`pyrethroid`) rung on a `fungal` disease -> `control_ladder_gate` bounces (applies_to). PASS
4. Conventional-before-cultural ladder -> `control_ladder_gate` bounces (monotonic-tier). PASS
5. Bird (`vertebrate`) problem with an insecticide rung -> `control_ladder_gate` bounces (coherence). PASS

All 5 defect classes caught. (RED proof reproducible via the injection script in the session log.)

## Footprint (scratch vs canonical, byte-level)
- Crops differing from canonical: **['Apple', 'Strawberry']** only.
- Top-level keys added/removed: **none**.
- Top-level keys with changed value: **['control_methods', 'source_catalog']** only (+13 methods, +10 T1
  source sub-ids; -0).
- Count 128 / 119 certified unchanged. Canonical COMPACT: 0 newlines, 0 escaped-unicode, no trailing newline.

## Consumer copy sweep (new/changed apple+strawberry records + new methods; 1202 strings)
- Em-dash (U+2014): **0**. Double-hyphen " -- ": **0**. Spelled-out degrees: **0**. "lady beetle": **0**.
- "ladybug" mentions: 4 (confirms the common-tongue rule, [[consumer-copy-common-tongue]]).

## release_verify -- 17 CONCERNS, all documented false positives
`release_verify <cand> --base <canonical> --slug apple` reports 17 concerns. Proven pre-existing by a
no-op **base-vs-base** run (`release_verify <canonical> --base <canonical> --slug apple`) that reproduces
the identical 17:
- **Section A** (1): "crops changed = ['apple','strawberry'] (expected only apple)" -- the tool's
  single-`--slug` pilot framing; we intentionally changed two crops. On base-vs-base it reads "crops
  changed = []" (still a concern), confirming the framing, not our change.
- **Section E** (16): apple's tree-region `chill_basis_beginner`/`_seasoned` keys flagged "novel" vs the
  annual reference crop `lettuce-leaf` -- pre-existing apple structure, unchanged by this arc (identical
  on base-vs-base).
- **Section B is the substantive check and is CLEAN: "no new violations introduced."** Apple gate PASS,
  reference crop byte-identical, calendars coherent, no dashes, `region_chill_delivered` well-formed.

## Independent fidelity reviews (the accuracy spine)
- **Catalog (13 methods):** FIXES-NEEDED -> fixed. 3 claims re-anchored to fetched T1
  (fruit_bagging apple-maggot -> UMN; swd_exclusion over-claim trimmed to MSU; horticultural_oil aphid ->
  UC IPM woolly-aphid).
- **Resistance (65 grades):** FIXES-NEEDED -> fixed. Full sweep of all 37 apple `susceptible` grades; 7
  defects from one root cause (WebFetch markdown parse column-shifted the Cornell DB). 3 fabrication-class
  (absence-inferred fire-blight on Anna/Dorsett Golden/Ein Shemer, blank Cornell cells) removed; 2 real
  resistant grades recovered; verified against raw HTML + Purdue PDF. Apple 54 -> 51 grades.
- **Ladders (20):** horticulture review SHIP-WITH-FIXES (0 Critical); sulfur/oil interval + fire-blight
  prune distance reconciled to single cited-T1 figures.

## Status
COMMITTED on branch `worktree-variety-resistance`, UNMERGED/UNPUSHED. Merge-to-main + push = Trevor.
NO plant-astro bump (astro lane). Roster-wide rollout + A39 hard-flip = later session.
