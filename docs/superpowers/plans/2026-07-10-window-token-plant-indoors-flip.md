# Plan: window-vs-token plant-flip (A) + indoors-flip overlap (B)

Spec: `docs/superpowers/specs/2026-07-10-window-token-plant-indoors-flip-design.md`

## Task 1 -- Gate changes (TDD, RED before GREEN) [tools/annual_calendar.py]

1. Add RED tests to `test_annual_calendar.py`:
   - A5 allows a BACKED plant-flip on a hot month (currently FAILS -- A5 flags plant-on-hot).
   - A5 still flags a hot month shown as `growing` (replaces the old plant-on-hot negative).
   - A5b: a `plant` on a hot month backed by `sp.plant_out` overlap passes; unbacked plant caught.
   - A5b: an `indoors` on a hot month backed by an OVERLAP-only window (no core month) passes
     (the item-B partial-window case; currently FAILS under core).
   Run -> confirm RED.
2. Implement:
   - A5: `flipped = hp & {m : cal[m-1] in ('indoors','plant')}`.
   - A5b: helper `_indoor_overlap(cell)`/`_plant_overlap(cell)` via `parse_months`; check `indoors`
     on hot months vs indoor overlap, `plant` on hot months vs plant overlap.
   - Update the old `_a5_bad` (plant->growing) with a comment on the moved coverage.
3. GREEN: `python3 tools/test_annual_calendar.py` all PASS; `gate_all` still PASS on the UNCHANGED
   canonical (no data touched yet -> proves the gate changes are inert on current data).

## Task 2 -- Item A batch (7 cells) [SHA-guarded]

- Builder script emits `tools/batches/window_token_A_plant_flip.json` (base_sha + full-array
  `from`/`value` guards) for the 7 se_gulf tomato calendars.
- Apply via `tools/apply_patch.py`; footprint-audit (only those 7 calendars change, count 125,
  COMPACT). `whole_crop_gate` per crop (5 slugs). `gate_all` PASS.

## Task 3 -- Item B batch (44 cells) [SHA-guarded]

- Builder script (declarative flip-group list from the spec) emits
  `tools/batches/window_token_B_indoors_flip.json`; each cell's `from` full array asserted, only the
  enumerated month indices change pause->indoors.
- Apply; footprint-audit (only the 44 calendars, count 125, COMPACT). `whole_crop_gate` per crop.
  `gate_all` PASS.

## Task 4 -- Release + state trio + handback

- Full suite on the final canonical: `gate_all`, `whole_crop_gate` (A43 incl), `calendar_coherence`,
  `release_verify <candidate>`, source-truth sample.
- State trio: CURRENT_STATE.md (surgical -- no `---` separator, per `current-state-md-drift`),
  STATE_HISTORY.md (prepend), LATEST.txt (SHA + session).
- Handback note for the app session: new canonical sha256, which of A/B landed, and the flagged
  same-rule extras for Trevor's ruling. COMMITTED, UNPUSHED (Trevor confirms).
