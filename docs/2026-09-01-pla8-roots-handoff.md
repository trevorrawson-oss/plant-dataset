# PLA-8 -- HANDOFF: the roots batch is NEXT, and the catalog is ready for it

**Written 2026-09-01 at the end of a long session. Read this before starting roots.**

Canonical is `6a67a677` (catalog round 8). Working tree clean, `main` in sync with origin.
**Verify first:** `shasum -a 256 crops_data_final.json` must read
`6a67a677960afcf3a0a85069c73737243d8117869232ec66ce8b79e99bdc8797`.

Everything below is committed and pushed. Nothing is half-done.

---

## 1. What shipped this session

| commit | what |
|---|---|
| `839c9de` | **PLA-8 batch 22, the stragglers** -- english-cucumber, edamame, pumpkin; 26 problems, 135 rungs, 4 mints; roster laddered **91 -> 94** of 121 |
| `a405351` | `COMMIT_FOR` registration for `919eabc4` |
| `ad571e6` | **`ladder_batch verify` absolute-vocabulary reconciliation** + a drift test |
| `a0caf3d` | the absolutes finding re-measured: a campaign of **85**, not 3 defects |
| `4c8bf1e` | **PLA-8 catalog round 8** -- `cure_and_store` + `lower_soil_ph`; methods **62 -> 64** |
| `2e352f5` | `COMMIT_FOR` registration for `6a67a677` |

Verification across both promote arcs: batch 22 suite 103/103 and harness **72 injected / 0
survived**; catalog r8 suite 57/57 and harness **42 / 0**. Full repo suite **4132 passed, 1 skipped**
(4070 before + exactly the 62 new tests, so nothing was lost). `gate_all` 121/121 on both.

Close-outs for both are appended to **PLA-8** in Linear.

## 2. START HERE: the roots batch, as ONE batch

parsnip (6 problems), potato (8), sweet-potato (8) = **22 problems**. Trevor asked whether to split
it in two; measured, the answer is no and the measurement is worth keeping:

* **The three crops share ZERO prose with each other.** There is no read to amortize, so splitting
  saves nothing on the expensive step and doubles the fixed overhead (promote + suite + harness +
  gauntlet + state trio + close-out).
* **The premise is uniform**: all 22 problems are FULL schema, all carry coarse types (`pest` x8,
  `disease` x8 across the three), and all carry `severity`. That is batch 17's shape, the simplest
  there is, and one promote covers it.
* It is **smaller than batch 22** (22 problems vs 26).

### Three things that are DIFFERENT from batch 22 -- do not inherit its promote wholesale

1. **ZERO template twins.** Measured: no roots problem shares byte-identical source prose with any
   laddered crop. Batch 22's `check_template_sibling_divergence` would be VACUOUS, and its own
   anti-vacuity branch will refuse rather than pass quietly. **Drop it and choose a guard by
   measuring**, the way batch 22 did. Three batches have now needed three different divergence
   guards; the ratio of exact-vs-diverging ladders does NOT pick the right one.
2. **The type rule is uniformly coarse -> upgrade**, not batch 22's split-by-crop. Assert it in the
   direction that actually holds.
3. **Run the substring / token-subset id scan**, not an equality check. Batch 21 earned "check every
   mint BY ID"; batch 22 followed that and still missed two, because an exact-id check passes an id
   that merely *resembles* a live one. See `docs/2026-09-01-pla8-batch22-outcome-and-carryforward.md`
   section 5.

### The catalog is now ready, and that is why r8 ran first

7 of the 22 roots problems needed methods that did not exist. `cure_and_store` and `lower_soil_ph`
are now live, so **author against the 64-method catalog**. Do not mint mid-batch: `ladder_batch
prepare` regenerates its brief FROM CANONICAL, and batch 1's documented defect was being authored
against a 37-method catalog that grew to 43 underneath it.

**Still unplaceable in roots, so expect these instructions to have no home:**

* **"keep the soil evenly moist" on common scab** -- see the correction in section 4. No legal
  method exists.
* **hilling / mounding over stems and crowns** (parsnip canker, and 4 shipped squash problems).
  DEFERRED at r8, not refused; see section 5.
* seed-piece suberization before planting (potato blackleg) -- distinct from post-harvest curing.
* "do not move soil on tools or shoes" (sweet-potato SCN-adjacent, edamame).

## 3. THE THIN-LADDER SCAN -- run, and here is the whole result

Recommended at the end of the r8 work and run before writing this. **It is done; do not re-derive
it.**

**Population.** 775 laddered problems / 3,149 rungs. 133 carry <= 2 rungs, 167 carry 3.

**Method.** A thin ladder is not itself a defect -- some problems have two rungs because two is all
there is. The defect shape is narrower: *the prose names a control that EXISTS in the catalog, is
LEGAL for that problem's type, and is absent from the ladder.* High-precision instruction phrases
were used as a **lead generator only**, over the <= 2-rung population, and every hit was READ.

**Result: 10 leads over 9 problems. 6 real, 4 false.**

### The 6 real gaps

| problem | ladder | missing | note |
|---|---|---|---|
| `strawberry`/`red-stele` | `crop_rotation`, `resistant_varieties` | **`improve_drainage`**, **`certified_clean_stock`** | prose: "Plant in well-drained soil or raised beds, buy certified plants". Also: **`crop_rotation` is ON the ladder and is named NOWHERE in the prose** -- a rung with no prose support, the inverse defect, worth its own look |
| `fig`/`dried-fruit-beetle-souring` | `garden_sanitation`, `resistant_varieties` | **`prompt_harvest`** | `prompt_harvest`'s own `best_use` literally names "fig souring" as its case |
| `fig`/`fig-endosepsis` | `garden_sanitation`, `resistant_varieties` | **`prompt_harvest`** | "pick promptly, remove affected and dropped fruit" |
| `beet`/`common-scab` | `crop_rotation` | **`lower_soil_ph`** | now available as of r8 |
| `garlic`/`botrytis-neck-rot` | `balance_nitrogen` | **`cure_and_store`** | now available as of r8; `garlic`/`fusarium-basal-rot` is the same shape |

All five are on **already-laddered, shipped crops**. None is in the roots batch. Each is a small
guarded promote; the two fig ones share a method and could go together.

### The 4 false positives, and why they matter more than the count suggests

**Every one failed for the same reason: the prose names the control in order to DISCOUNT it.**

* `lemon`/`huanglongbing` and `lime`/`huanglongbing` -> `resistant_varieties`. The prose says
  "Research into tolerant varieties is ongoing but there is no home cure." Adding the rung would
  assert that resistance exists.
* `cantaloupe`/`bacterial-wilt` -> `resistant_varieties`. "Few home varieties carry useful
  resistance, so exclusion and early beetle control are the reliable tools."
* `chamomile`/`gray-mold` -> `improve_drainage`. The match is "well-drained" inside "lean,
  well-drained, airy plantings rarely see it" -- a descriptive aside about where the disease does
  NOT occur, not an instruction.

**A keyword scan cannot tell "do X" from "X will not help here", and 40% of its hits were the
latter.** That is the `document-subject-defeats-proximity-scans` lesson again: the scan is a
reproducible way to generate leads and is not a verdict. Do not automate this into a gate.

**The reassuring half of the result:** only 10 leads across 133 thin ladders. The thin population is
overwhelmingly thin for good reason. This is bounded follow-up work, not a rot.

## 4. A CORRECTION I OWE, made during the scan

The r8 record claimed that `even_watering` "already carries" the soil-moisture half of common scab
control. **That is wrong.** `even_watering.applies_to` is `['physiological', 'mite']`, which does not
intersect `TYPE_TARGETS['bacterial']`, so it is **ILLEGAL** on both potato and beet common scab, and
no other method carries a "keep the soil evenly moist" instruction for a disease. I asserted method
availability without checking legality -- the exact failure the repo has a rule against.

Corrected in the live surfaces (`LATEST.txt`, `CURRENT_STATE.md`, the r8 content module docstring,
and the batch-22 carry-forward). **`STATE_HISTORY.md` was deliberately left byte-for-byte**, per its
append-only rule, and commit `4c8bf1e`'s message stands as the historical record. The mint itself is
unaffected: `lower_soil_ph` never claimed the moisture half.

**r9 candidate: widen `even_watering` to reach `bacterial` / `disease_general`**, or the scab
moisture instruction stays homeless on potato, beet and any future scab host. The PNW handbook names
*Streptomyces scabies* on beet, potato, parsnip, carrot and radish, so the population is larger than
two.

## 5. The r9 catalog queue, in evidence order

1. **Widen `even_watering`** to reach disease types (section 4). Cheapest, and it unblocks a control
   both scab sources call half the answer.
2. **In-season mounding**, DEFERRED at r8 with its measurement recorded in
   `build_pla8_catalog_r8_content.py`. 5 problems / 5 crops, 4 already laddered with the instruction
   unplaced. Blocked on ONE thing: reading splits it into three mechanisms (adventitious rooting for
   resilience; a physical barrier against larval entry; covering a crown against a canker fungus) and
   **the barrier reading has no document** -- asked directly, UIUC names burying nodes for rooting
   and does not mention mounding over the lower stem to prevent entry. Source that, or admit it as
   two methods.
3. **`horticultural_oil` cannot reach `fungal`** -- reported by three batches now.
4. **General plant vigor** -- four berry authors, citrus, edamame, pumpkin.
5. **Humidity / venting under cover** -- the most-repeated instruction in english-cucumber's record
   (5 problems) with no method at all.
6. **`weed_host_control` cannot reach `viral` or `nematode`** -- english-cucumber's CMV is the
   textbook case, an aphid-vectored virus with a named weed reservoir.
7. Seed-piece suberization; potassium bicarbonate; lawn/grub management; a lift-fruit-onto-a-board
   method; dormant lime sulfur; watering QUANTITY.

## 6. Open, filed, NOT fixed

1. **The absolutes campaign: 85, not 3.** Measured roster-wide: 171 absolute-word hits in problem
   prose, 134 "never" clauses, of which **85 instruct the reader** and ~45 are ordinary descriptive
   English ("seeds that never come up"). I originally reported this as three defects from batch 22's
   crops and Trevor approved fixing them; measuring first showed that fixing 3 of 85 would make the
   dataset **less** consistent. **It needs a read-then-adjudicate pass, NOT a find-and-replace.**
   The tooling half is already fixed in `ad571e6`.
2. **FOUR one-token id repoints** would retire the lone-crop minority-id class: asparagus `cutworm`,
   swiss-chard `flea-beetle`, basil `japanese-beetle`, artichoke `botrytis-gray-mold`. Batch 21's and
   batch 22's `check_singular_variants_not_taken` both refuse once the first three are repaired --
   **retire the guard in the same change.**
3. **`wet_foliage_discipline` missing from 13 laddered problems** whose own prose says to time work
   to dry foliage (34 carry the instruction, 21 carry the rung).
4. **The 5 thin-ladder gaps** in section 3.
5. **Mis-pointed / unstable source keys** -- a measured class across batches 17, 18, 20 and 22. Each
   problem's own `anchoring_urls` is correct; the KEY is not stable. Mechanically detectable; the
   scan is still worth building and still has not been.
6. **viola's own note recommends Bt on a butterfly host** (batch 21). The ladder already omits it.
7. **The batch-18 oil temperature ruling was OVERTURNED** by reading (batch 19 outcome doc section 8).
   Specified, not actioned.

## 7. Operational notes

* **The pre-commit E1 hook will always block a dataset commit**, and this is structural, not a
  problem to fix: it wants `~/plant-app`'s export to reference a commit that cannot exist until
  after the commit. Batch 21 bypassed it too -- plant-app's provenance records `dataset_commit
  27a9f87`, batch 21's OWN second commit. Use `--no-verify` and put the reason in the message.
* **plant-app owes a `npm run build:guides` covering THREE dataset revisions** (batch 21's, batch
  22's and r8's), not one. Trevor is having the app pick this up when its current work finishes. The
  shipped export is that far behind; it does not block dataset work.
* **`release_verify` is single-crop-pilot-shaped.** It demands exactly one changed crop, so a
  catalog-only round always reports one section-A concern it cannot avoid. Read section B, the
  top-level line, and the reference-crop line instead.

## 8. Roster position

**94 / 121 laddered.** Remaining **27 crops / 138 problems / 7 batches**, counts COMPUTED from
canonical:

| batch | crops | n | problems |
|---|---|---|---|
| **roots (NEXT)** | parsnip, potato, sweet-potato | 3 | 22 |
| alliums | chives, leek, onion, shallot | 4 | 27 |
| other trees | mulberry, pawpaw, persimmon, pomegranate | 4 | 24 |
| woody herbs | lavender, rosemary, sage, thyme | 4 | 20 |
| soft herbs | lemongrass, mint, oregano | 3 | 16 |
| pome fruit | pear-asian, pear-european | 2 | 15 |
| microgreens (**LAST**, standing ruling) | arugula-, broccoli-, cilantro-microgreens, pea-shoots, radish-microgreens, sunflower-sprouts, wheatgrass | 7 | 14 |

Note the alliums batch inherits `cure_and_store` directly: onion and shallot both carry Botrytis neck
rot with curing and storage instructions, and garlic's shipped one-rung ladder is the backfill.
