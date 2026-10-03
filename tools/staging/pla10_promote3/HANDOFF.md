# MORNING REPORT -- PLA-10 promote 3, session 1 (unattended run, 2026-10-02/03)

**RULED 2026-10-03:** Trevor's rulings on every row below are folded into docs/kickoffs/59-pla10-promote3-worklist.md
as TAKEN (commit `docs(pla10): promote 3 rulings`). Session 2 authors from the ruled worklist; the "Needs Trevor's
ruling" list below is historical. The three data-commit items further down still stand.

Nothing broke; no stop condition hit. Nothing pushed. Canonical 31b766e8 untouched (== LATEST.txt); no crop record
edited; no stage file under this directory except this file.

**Commits (local, unpushed; main is 2 ahead of origin):**
- `ac06c11` tooling(pla10): promote 3 session-1 tools (T3, T4, T5 unarmed, promote_pla10_promote3, suite, harness 79/79)
- the worklist commit `docs(pla10): promote 3 worklist (kickoff 59)` (SHA: `git log -1` on main; it carries
  docs/kickoffs/59-pla10-promote3-worklist.md, 52 MANIFEST.tsv rows, and this report)

**Fetch tally (53 targets):** fetched **52** (42 both UAs byte-identical, 8 browser UA only, 2 only with the Safari
header set); **429: 0**; **403: 1** (UC Santa Clara chamomile, 403 browser/plain on three passes incl. Safari headers);
**changed: 1** (cilantro's UW page, already hashed: `12-18"` now `1 to 1⁄2 feet`, same value, T4 cannot read U+2044);
**gone: 0**. 5 redirects (fig, UMN beans + leeks, ISU beans, EDIS FP623), sentences intact. 73 of 76 measured quotes
byte-present in fresh bytes. **blueberry K2: branch 1** (the record's PSU page states "5 to 8 feet tall and wide":
kept and re-hashed, no value correction).

**Worklist (docs/kickoffs/59-pla10-promote3-worklist.md), 62 rows:** CLOSED 37 (21 new + 16 backfill), DISAGREEMENT 21,
SCOPE-DOUBT 2 (habanero ruled in by H2; mint), CONDITIONAL 2 (nasturtium, sweet-pea: stage null). Recommended:
43 new heights authored, 3 staged null (nasturtium, sweet-pea, chamomile unless hashed), 23 new spreads.

**The 21 disagreement rows, recommendation each (W2 range rule, worklist §1):**
1. cosmos: keep H1 UF [3,6] -- BUT H1's premise was wrong: NCSU's attributes line states a closed [2,4].
2-6. cherry / beefsteak / roma / grape / heirloom tomato: Cornell [2,6] / [2,6] (not NCSU [1,10]); roma alt OSU det 3-4.
7. onion: NCSU [1,1.5] / [0.5,1].
8. artichoke: Cornell [3,6] / [2,4] (range beats TAMU's point).
9. basil: UC Santa Clara [0.6667,2] / [0.6667,1].
10. cilantro: USU [1,3] (UW foliage [1,1.5] needs a T4 fraction extension).
11. chives: NCSU [1,1.5] / [1,1.4167].
12. lemongrass: NCSU [2,4] / [2,3], prose "3 to 6 feet" edited (x2).
13. marigold: NCSU [1,4] / [0.5,1].
14. sunflower: NCSU attrs [1.5,10] / [1.5,3].
15. borage: UC Marin [2,3] height, NCSU [1,1.3333] spread.
16. calendula: FP087 [1,2] / [1,2].
17. zinnia: FP623 [1,3] / [1,2].
18. chamomile: stage null unless session 2 hashes a page (Santa Clara 403).
19. sweet-alyssum: UW [0.25,0.75] height, NCSU [0.5,1] spread.
20. echinacea: NCSU [3,4], prose "2 to 4 feet" edited.
21. viola: NCSU pansy prose [0.5,0.75] / [0.75,1], scope recorded.

**Needs Trevor's ruling before session 2 authors:**
- The 21 rows above (none is ruled), especially: the tomato choice (Cornell [2,6] vs NCSU [1,10] vs null as
  habit-spanning), and cosmos (H1 confirmed despite NCSU's closed [2,4]?).
- Rule 4 (worklist §1): nasturtium and sweet-pea staged null as habit-tied (spec §4.4 peas precedent) vs authored.
- Rule 3 (worklist §1), the tie-break between two closed ranges (scope, then prose agreement, then the Toolbox
  record): it is this session's proposal, not a prior ruling.
- cilantro: USU [1,3] now, or extend T4 for U+2044 fractions and take UW's foliage figure.
- chamomile: confirm "hunt, then null" (session 2 retries Santa Clara, fetches NCSU matricaria).
- Restatement edits proposed beyond H3's dill: lemongrass "3 to 6" and echinacea "2 to 4" (both below/above the cited
  figure); fava's "2 to 4" recommended `agrees`.

---

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
