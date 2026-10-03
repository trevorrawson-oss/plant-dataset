# PLA-10 promote 3 -- hand-off (owed in the DATA commit)

Written 2026-10-02, promote 3 session 1, in the tools commit. Base canonical 31b766e8. Each item below is
required in the same commit that writes the promote-3 canonical; none is optional, and none may land earlier
(gates arm off the data).

1. **Flip both arming flags.**
   - `tools/sourced_block_ratchet_gate.py`: `MATURE_DIMENSIONS_ARMED = False` -> `True`.
   - `tools/whole_crop_gate.py`: `A59_SIBLING_ARMED = False` -> `True`.
   Both are pinned flag == data (`test_sourced_block_ratchet_gate::test_the_flag_matches_the_data`,
   `test_gate_plant_dimensions_a59.py`): each must be True iff a certified crop carries
   `mature_dimensions_sources`. A59's sibling call at the whole_crop_gate entry point is proved ONLY from this
   commit on: the armed branch of `test_gate_plant_dimensions_a59.py` is written and has never run.

2. **Keep the older promotes' replay suites unarmed for A62's new block** (the rootstock precedent: promote 2's
   data commit passed `rootstock_armed=False` into promote 1's check_post). Once A62's mature_dimensions block
   is armed, every earlier promote whose post-state carries a height with no sibling reddens. Pass
   `mature_dimensions_armed=False` to `SBR.roster(post)` in:
   - `tools/promote_pla10_planting_layout.py` (promote 1)
   - `tools/promote_pla10_promote2.py` (promote 2)
   - the PLA-465 promotes' post-state checks (`grep -l "SBR.roster\|sourced_block_ratchet_gate" tools/promote_pla465_*.py`;
     re-grep every `tools/promote_*.py` calling `SBR.roster` / `crop_violations`, the list above is not proven complete).
   Re-run each one's suite and mutation harness.

3. **Re-home the A59 integration fixture off basil.** `tools/test_gate_plant_dimensions_a59.py` uses
   `NULL_CROP = "basil"` (a certified crop with no height and no plant_dimensions record); promote 3 gives basil
   a height, so its guard assertion fails. Pick a certified crop that stays null after promote 3 (a NONE or
   CONDITIONAL crop in docs/kickoffs/59-pla10-promote3-worklist.md, e.g. carrot).

Also in the data commit (plan 58 §4, live-state re-measure): the pins listed there, `promote_fixture.COMMIT_FOR`
for the new canonical, and a re-grep of `31b766e8` across `tools/test_*.py`.
