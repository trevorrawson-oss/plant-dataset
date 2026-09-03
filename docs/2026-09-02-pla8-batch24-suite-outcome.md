# PLA-8 batch 24 (alliums) -- the guard suite and mutation harness, and what writing them found

**Written 2026-09-02.** Base `c24d7754` (catalog r10) -> post **`3eefc4b8`**. Roster **97 -> 101**.
Reads with `docs/2026-09-02-pla8-alliums-handoff.md`, which this note amends in four places.

The handoff's START HERE was "batch 24 is staged with a passing promote and NO suite". The suite and
harness now exist. **Writing them found four defects in the promote that were passing every check it
had**, and none of them would have been caught by adding mutations to the suite as it stood, because
three were in code no branch could reach and one was in a number rather than a branch.

---

## 1. What shipped

| file | what |
|---|---|
| `tools/promote_pla8_batch24.py` | **amended** -- four guard corrections, below. Post SHA UNCHANGED at `3eefc4b8`. |
| `tools/test_promote_pla8_batch24.py` | **new** -- 113 drivers, ~97s |
| `tools/mutate_pla8_batch24_suite.py` | **new** -- 88 mutations across 16 families, preflight + positive control + sentinel |

Every promote amendment is a CHECK, never a transform, so the output is byte-identical to the
candidate the handoff describes. Verified: `3eefc4b8ace43b040ce45e8e38692017991a56a30c0f2b9739e0656c634d8d48`.

---

## 2. THE FOUR DEFECTS WRITING THE SUITE FOUND

### 2.1 An unused pin element reading as coverage (`check_id_adjudications`)

`ID_SCOPE_PINS` declares BOTH halves of the scope split that makes chives' compound Botrytis a
distinct id from the live `botrytis-neck-rot`: chives' entry is a FOLIAR blight (`"dense canopies"`),
the live id is the STORAGE rot (`"curing"`). The loop unpacked
`(resembles, own_phrase, other_phrase)` and **never read `own_phrase`**. Only the other half was
checked. Chives' record could have stopped describing a foliar blight -- the entire reason it is a
separate id -- with the guard still green.

A pin that declares a reason and checks half of it is worse than a pin that declares one reason,
because the unchecked half reads as covered.

Wired, and verified RED against the real defect before being trusted. Both halves now have drivers
and both are in the harness.

### 2.2 An anti-vacuity branch that was itself unreachable (`check_no_precedent_copy`)

```
if cmp_a == 0: raise ... pass A ... vacuous
if cmp_b == 0: raise ... pass B ... vacuous
```

`by_m` (pass B, keyed on method alone) is a strict SUPERSET of `by_idm` (pass A, keyed on problem id
AND method), so **`cmp_b == 0` implies `cmp_a == 0`** and with pass A tested first the pass-B branch
could never fire. It was an anti-vacuity branch that was itself vacuous -- the exact class batch 21
shipped two of, arrived at from the opposite direction.

Fixed by checking the SUPERSET first. Both branches now have drivers, plus a third asserting the
ORDER, so a refactor cannot quietly restore the dead branch.

### 2.3 THE METRIC HAD A THIRD DILUTION. **`difflib` is asymmetric.**

This is the one that matters, and it is the handoff's own lesson arriving again.

difflib's matcher is GREEDY, not optimal: it takes the longest match it can see and recurses either
side, so the decomposition depends on which sequence is indexed and **`ratio(a, b) != ratio(b, a)`**.

Measured on this corpus, over 1200 sampled real pairs:

| statistic | value |
|---|---|
| maximum asymmetry | **0.271** |
| p99 | 0.170 |
| median | 0.021 |
| pairs where the SHIPPED argument order scored LOWER | **607 of 1200** |

One pair, verified by an independent walk over the matching blocks rather than by trusting `ratio()`:
**52 characters matched one way, 11 the other** -- 0.343 against 0.073, same two strings.

Against a 0.70 threshold that is decisive, and the shipped order gave no systematic protection: it
under-scored more often than it over-scored. Fixed by taking the **max of both orders** -- the
strongest evidence of copying rather than an accident of which side was passed first.

**Re-measured across all 18575 comparisons under the corrected metric: the batch's worst pair is
UNCHANGED at 0.693 and nothing crosses 0.70.** The correction strengthens the guard without changing
this batch's verdict, so batch 24 ships on it.

That makes **three** dilutions found in one metric:

| # | dilution | found | a mutation harness reddens on it? |
|---|---|---|---|
| 1 | `autojunk` engages at 200 chars and junks any char in >1% of the sequence | batch 23 | **no** |
| 2 | a MEAN of two registers dilutes one copied register against one independent one | batch 23 | **no** |
| 3 | greedy matching makes `ratio()` asymmetric by up to 0.271 | **here** | **no** |

**A harness proves a guard FIRES; it cannot prove the guard MEASURES the right thing.** In all three
cases the branch fires correctly and only the number handed to it is wrong. The suite therefore
carries a `MetricDiscriminates` class that asserts NUMBERS rather than branches, including a
constructed pair sharing a 127-character verbatim run that scores **0.637 with autojunk on (passes,
ships) and 0.744 with it off (refused)** -- the defect is not that the number is lower, it is that it
lands on the other side of the line.

### 2.4 The guard was too slow to be mutation-tested at all

`check_no_precedent_copy` makes 18575 comparisons and took **62s** under the corrected symmetric
metric. At 88 mutations the harness would have run for over three hours, which is the practical
reason a guard this expensive quietly stops being verified.

Fixed WITHOUT weakening the metric, by a rigorous O(1) prune: `ratio` is `2M/T` and `M` cannot exceed
the shorter length, so a pair whose length ratio already sits at or below the running worst can never
beat it or reach the threshold. Verified against an unpruned independent walk over the same 36132
register pairs -- identical comparison counts, identical worst, identical refusals, 25% of pairs
skipped, highest true score among the skipped pairs **0.566**. The suite asserts the equivalence
against a re-derived reference implementation rather than against the code under test.

The measured ceiling is now PRINTED BY THE PROMOTE (`precedent scan : 509 + 18066 comparisons, worst
0.693 (...)`) and pinned by the suite from that output, so it is a computed artifact rather than a
claim in a docstring.

---

## 3. Two assertions WITHDRAWN, with the arithmetic asserted

`verify_post`'s touched-problem count and per-crop tally are FORWARD assertions, verified unreachable
and withdrawn from the harness rather than reported as permanent survivors:

* every added key is `(batch crop, one of exactly 3 field names)`, so a touched triple carries at
  most 3 keys and **81 added keys force exactly 27 triples**;
* each batch crop's pinned problem count IS its full problem count, and those maxima sum to 27, so
  the per-crop split is forced too.

The suite asserts that arithmetic (`test_the_touched_and_per_crop_counts_are_FORWARD_assertions`) and
will fail if a future edit makes either reachable. A forward assertion is not a gap; padding a
harness total with one is not coverage.

---

## 4. The gauntlet, re-run against the amended promote

| check | result |
|---|---|
| `gate_all` | **121/121 PASS** |
| `whole_crop_gate` chives / leek / onion / shallot | PASS, PASS, PASS, PASS |
| A54 `source_catalog_title_gate` | 0 violations |
| `register_completeness_gate` | PASS |
| `control_ladder_gate` | 0 violations |
| `release_verify` | **byte-identical base vs candidate** -- the batch introduces no new concern |
| control_methods / source_catalog | 64 -> 64, 219 -> 219 |
| crops changed | exactly `['chives', 'leek', 'onion', 'shallot']` |
| laddered roster | 97 -> **101**, 82 rungs |

`release_verify` being byte-identical is a stronger result than "clean but for the known concern":
the four Step-5 review notes it prints are present on the BASE too and are not this batch's.

---

## 5. AMENDMENTS TO THE HANDOFF'S FORWARD GUIDANCE

The handoff's last line says batch 25's schema "has not been checked at all" and that the microgreens
use a fourth shape with "zero laddered anywhere, so batch 29 has no proven precedent". Measured:

| batch | crops | problems | schema | severity | **type situation** |
|---|---|---|---|---|---|
| 25 other trees | mulberry, pawpaw, persimmon, pomegranate | 24 | FULL, uniform | all | **COARSE** (`pest`/`disease`) |
| 26 woody herbs | lavender, rosemary, sage, thyme | 20 | FULL, uniform | all | **ALREADY FINE** (incl. `mollusk`) |
| 27 soft herbs | lemongrass, mint, oregano | 16 | FULL, uniform | **SPLIT** | **THREE-WAY SPLIT** |
| 28 pome fruit | pear-asian, pear-european | 15 | FULL, uniform | all | ALREADY FINE, incl. **`other`** |
| 29 microgreens | 7 remaining of 8 | 14 of 16 | `description_*` + `name_beginner`/`name_seasoned` | none | fine on the laddered one, absent on the rest |

Totals reconcile exactly with the handoff: **20 crops / 89 problems remain.**

Four corrections:

1. **Batch 25 is COARSE-typed, so it needs batch 23's upgrade guard, not batch 24's set-from-nothing.**
   Batch 24's `check_type_set_from_nothing` refuses batch 25 on its first problem. Ninth distinct
   type situation in nine batches; the guard is never inherited.
2. **Batches 26 and 28 are ALREADY FINE-typed** -- a third situation again, with nothing to set and
   nothing to upgrade. The guard there must assert the EXISTING value is retained and coherent.
3. **Batch 27 is a THREE-WAY split, not a uniform batch**: lemongrass coarse + severity, oregano fine
   + severity, **mint no type and no severity**. More complex than batch 24's two-way split.
4. **Batch 29 DOES have a laddered precedent, and it is inside the batch.** `microgreens-mix` carries
   2 laddered problems on the `description_*` schema -- `fungus-gnats` (insect, 3 rungs) and
   `damping-off` (fungal, 4 rungs) across `bottom_watering`, `garden_sanitation`,
   `yellow_sticky_traps`, `sensible_seeding_rate`, `airflow_spacing`. The other 7 crops carry the
   SAME two problems. The shape is proven; the handoff's "no proven precedent" is not right.

### A LIVE BLOCKER FOR BATCH 28, found while measuring

**Both pears' "Pear decline" is typed `other`, which is NOT in the gate's `TYPE_TARGETS`.** They are
the only two `other`-typed problems on the roster and both are unladdered, so no precedent exists.
Only 4 of 64 methods carry `applies_to: any` (`crop_rotation`, `floating_row_cover`,
`garden_sanitation`, `resistant_varieties`), so a ladder authored against `other` would be confined
to those four and would exclude the actual controls.

**The resolution is already set by precedent and does not need research.** Pear decline is a
phytoplasma ("a tiny disease organism carried by the pear psylla insect"), and the roster types every
phytoplasma disease `bacterial`: aster yellows on carrot, parsnip, marigold, nasturtium, cosmos and
echinacea, plus X-disease on cherry-sweet -- **7 shipped, laddered precedents, all `bacterial`**.
Re-type at batch-28 authoring time, as a pinned adjudication rather than a silent fix.

---

## 6. `even_watering` REFRAMED -- it is not a widening, it is r10's two-class problem again

The handoff calls this the strongest catalog signal in the arc: seven independent reports across two
batches (roots 3, alliums 4). **Confirmed at seven**, and on leek/`pink-root` the instruction is
unrepresented in any rung. But the count is not the interesting part.

`even_watering` already carries **THREE** distinct mechanisms, and has already been widened twice:

| mechanism | `applies_to` | shipped rungs |
|---|---|---|
| calcium delivery (blackheart, blossom-end rot) | `physiological` | 12 |
| spider mites building up on plants "left dry and stressed" | `mite` | **25** |
| common scab (*Streptomyces scabies*) favored by dry soil | `bacterial` | 2 |

So the precedent for widening it is strong, and each previous widening moved its mechanism into the
prose. The batches are asking for a FOURTH: general plant vigor against insect feeding (thrips) and
fungal infection (pink root).

**This is r10's Class A / Class B split exactly, and it must be run the same way**, because
`applies_to` governs what the GATE accepts and does nothing to what a READER sees:

* **The insect half is nearly free.** The method's own text ALREADY states the vigor mechanism --
  mites "build up fastest on plants that have been left dry and stressed" -- and thrips are the same
  stress-favored sap feeder. Widening to `insect` generalizes a claim the method already makes.
  Still needs a T1 source carrying it past mites.
* **The fungal half is a DIFFERENT claim** (stress predisposing to root disease) and needs its own
  source. Do not let the insect half carry it.
* **Widening without generalizing `how_it_works_*` would ship the r10 Class-B defect verbatim**: a
  reader dealing with onion thrips would be told about celery blackheart and transpiration-driven
  calcium flow. The prose is the substance; the target set is only the mechanism.

---

## 7. What is owed

1. **The mutation harness result** -- running at the time of writing; ~2.5h for 88 mutations.
   Record the count here and in the Linear close-out before the batch is called done.
2. **The independent source-truth pass on batch 24 has NOT been run.** It found ELEVEN defects on
   batch 23 when every gate, an 82-test suite and a 64/64 harness were green. Gates and harnesses do
   not substitute for it. **This is the single largest outstanding risk on this batch.**
3. Commit `tools/promote_pla8_batch24.py`, the suite, the harness and
   `tools/staging/pla8_batch24_alliums/` together; the staging dir and promote are still UNTRACKED.
4. Register `3eefc4b8` in `COMMIT_FOR` after the data commit lands. **Never amend a pinned commit.**
5. `main` is 5 commits ahead of origin and UNPUSHED. Trevor confirms every push.
