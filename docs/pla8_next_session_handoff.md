# PLA-8 -- handoff after batch 5 (2026-08-25)

Canonical **`7c3e5d71`**. Six commits on `main`, **unpushed**. Catalog **53 methods**.
Roster laddered **27 of 121** -- 94 crops / 706 problems left, **19 batches**.

Run `python3 tools/ladder_batch.py status` for live figures rather than trusting this paragraph.
The procedure is `docs/ladder_batch_playbook.md`. Read it; this file only covers what changed.

---

## What landed this session

| commit | |
| -- | -- |
| `c1e708f` / `39b6ca8` | catalog **r5**: mint `planting_time_avoidance` + `wet_foliage_discipline`, widen `balance_nitrogen` + `augmentative_release`, mint `ucanr_ext_dry_bean_white_mold`. 51 -> 53 methods. |
| `22d176c` / `ec33e83` | catalog **r6**: close the `planting_time_avoidance.best_use` self-contradiction. |
| `d6e8071` / `0a2ffa8` | **BATCH 5**: the three beans, 131 rungs, roster 24 -> 27. |

**Never amend any of them** -- `promote_fixture.COMMIT_FOR` pins `c1e708f`, `22d176c`, `d6e8071`.

---

## The one thing this session would tell the next one

**Read the crop prose BEFORE preparing a batch, not after the authoring agents refuse.**

Every earlier catalog round was reactive: batch 4 minted `borer_stem_surgery` only after three
agents independently refused to fake the control. That works, but batches 3 AND 4 both ended up
HOLDING content rather than shipping ladders known to drop a primary control. Reading all nine
`green-beans-bush` problems first found **five** controls with no catalog home before a single
ladder was authored, which turned a re-run into a catalog round that shipped ahead of the batch.

The corollary is that the batch then **audits the round**. r5 shipped a method sheet that
contradicted itself, and the first two authoring passes to use it found that out within hours by
disagreeing with each other. Batch 5's promote now requires every method the round produced to be
reachable in the batch: **minting a method the batch does not use means the round was not justified
by the need it claimed.**

---

## Next batch

`ladder_batch.py families` will say this, but the shape is already clear:

- **There are no true twins left.** `dry-bean` + `green-beans-bush` was the last one. From here
  every batch costs **one authoring pass per crop**. Anyone planning from the pre-2026-08-24 numbers
  is wrong by about 3x.
- **The obvious next family is the two peas** -- `snow-peas` + `sugar-snap-peas`, 8 problems each,
  **82.8% identical**, the highest-scoring shared-name family left. Same Beans & Peas sourcing this
  session just read, so the source overlap is real.
- Then `cayenne-pepper` + `habanero` (11 problems each, 79.5%), `grape-tomato` + `roma-tomato`
  (9 each, 68.1%), `collards` + `kale` (9 each, 25.0% -- barely a family).
- **80 singletons** remain; batch those by CATEGORY so sourcing overlaps.

---

## Highest-value catalog work, now measured across three batches

**No conventional FUNGICIDE key exists at all.** Both `conventional` entries are insecticides, so
chlorothalonil is unexpressible. Named on the cucumbers (batch 3) and again by both bean passes.
This is the biggest remaining hole and it will recur on every crop with a foliar disease.

Also owed, each hit independently by more than one pass:

- **`tool_and_hand_hygiene`** -- third instance. Both bean passes folded stake and trellis cleaning
  into `garden_sanitation` and both flagged the fit.
- **A botanical pyrethrin key.** `pyrethroid` is a synthetic conventional; pyrethrin is a botanical
  soft chemical. Both bean passes refused to file one under the other, correctly.
- **`weed_host_control`** -- "control nearby weeds that harbor them" has no home. Both passes.
- **Dust suppression** (spider mites) and **a general scouting key** -- both passes folded the
  scouting cue into another method's note and flagged that they had.
- Still open from earlier batches: a plant-vigor method, a disease-side nitrogen key beyond the r5
  widening, a biofungicide / potassium-bicarbonate key, `container_culture`, `certified_clean_stock`
  variants, trap cropping, diatomaceous earth.

---

## Owed, and NOT done here

- **Linear PLA-8 has no record of batches 1-5.** Its description still ends at the 2026-08-22/23
  close-out. The MCP token expired mid-write this session. A ready-to-paste close-out covering r5,
  r6 and the batches-1-4 gap is in the session scratchpad as `PLA-8_closeout_r5.md`; batch 5 and r6
  need appending to it from `STATE_HISTORY.md`.
- **plant-app owes its own `data(guides)` commit.** `build:guides` was re-run after each of the
  three promotes, so `assets/data/guides.dataset`, `src/data/control-methods.json` and
  `assets/data/dataset-provenance.json` are modified and uncommitted in that repo.
- **Nothing is pushed.** Six commits sit on `main`.
- ~~Batch 1 is still STAGED, not promoted.~~ **WRONG, corrected 2026-08-26.** Batch 1 was promoted
  in `9fbf655` ("5 crops laddered, 18 of 22 read-fixes applied", roster 7 -> 12) and all five crops
  carry rungs. The claim was carried out of `pla8-batch1-read-outcome`, which recorded it truly at
  the time of writing and was superseded the same day. **A stale record reads as current truth** --
  the exact failure `stale-records-commission-phantom-work` exists to prevent, repeated while that
  memory sat in the index. The roster arithmetic is the check: 7 pilot + 5 + 4 + 3 + 5 + 3 + 2 = 29.

---

## Guard lessons from this session, worth carrying into the next promote

1. **A `verify_post` guard needs a test that doctors the POST directly.** `check()` sees only the
   staged batch, so every input that could reach a post-state guard is refused upstream first. Five
   of batch 5's six first-run survivors were exactly this.
2. **Assert a premise where the claim lives.** Comparing staged files proves what the promote did;
   comparing canonical proves it was allowed.
3. **Never include the field the promote WRITES in a premise check** -- the premise becomes true by
   construction.
4. **A refusal test must assert the message of the guard it names.** Asserting only "something was
   refused" passes green while an earlier check answers for it; that masked three mutations in r5
   and two more in batch 5.
5. **Guards that exist in both `check` and `verify_post` differ only by indentation**, so a bare
   mutation anchor substring-matches twice. Preflight catches it as `HARNESS DEAD`; it fired twice
   this session.
6. **An unreachable guard is deleted, not tested.** r6 had an "already corrected" branch that could
   never fire because an earlier check returns first.
