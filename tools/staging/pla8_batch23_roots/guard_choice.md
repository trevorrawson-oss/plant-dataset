# Batch 23 (roots): the divergence guard, CHOSEN BY MEASUREMENT

The roots handoff (section 2.1) said: batch 22's `check_template_sibling_divergence` would be
VACUOUS here because roots has zero template twins, its anti-vacuity branch would refuse, and
**"Drop it and choose a guard by measuring. Four batches have now needed four different divergence
guards; the exact-vs-diverging ratio does NOT pick the right one."**

## The risk this batch actually carries is NOT sibling-to-sibling

The three roots crops share zero prose with each other, so there is nothing to copy sideways.
The copy vector is **cross-crop, into a precedent crop**, and this session CREATED it: 13 of the 22
pinned ids are REUSED from laddered crops, and each authoring agent was pointed at the precedent
crop as a shape exemplar (carrot, beet, the tomatoes, eggplant, radish, garlic, fig, okra).
The guard has to protect the thing the method deliberately exposed.

## GUARD: `check_no_precedent_copy`

For each authored roots rung, compare `(note_beginner, note_seasoned)` against every existing
roster rung sharing the same `(problem id, method)`. REFUSE if max similarity >= **0.70**.

## Why 0.70, measured not chosen

Roster-wide similarity was measured first and would FLOOD: 16,510 cross-crop shared-(id,method)
pairs, 434 byte-identical. But every dense identical cluster is a PROPAGATION group (peppers,
beans, melons, corns, brassicas) where copying was deliberate and the promote asserted it.
Byte-identical SOURCE prose turned out to be too strict a test for "propagated" -- the melon trio
(watermelon / cantaloupe / honeydew) has slightly different source prose and 169 identical rungs
anyway, so a source-identity split still leaves the flood in the "independent" bucket. This is
exactly the handoff's warning, and the reason the ratio does not pick the guard.

So the population was narrowed to roots' ACTUAL peers: crops whose max prose-kinship to any other
laddered crop is < 0.55, i.e. crops in no propagation group at all. There are 13 of them (apple,
asparagus, basil, beet, broad-beans-fava, carrot, celery, edamame, fig, lettuce-leaf, strawberry,
swiss-chard, tomatillo). potato and sweet-potato measure 0.370 and 0.360 -- squarely singletons.
parsnip measures 0.582 against beet, but on a denominator of ONE shared problem (damping-off);
against carrot, its real relative, it shares 3 ids. Treat parsnip's hits as read-then-adjudicate
rather than assuming propagation.

Among those 13 singletons there are **207 shared-(id,method) rung pairs**, and their similarity
distribution is the empirical ceiling for genuinely independent authoring:

    max 0.644   p99 0.626   p95 0.520   median 0.291

Nothing independent reaches 0.70. The top of the distribution is `powdery-mildew`/`sulfur` between
apple and strawberry at 0.644 and `aphids`/`balance_nitrogen` between lettuce-leaf and swiss-chard
at 0.644: two crops saying the same true thing about the same method in their own words.

| threshold | legitimate singleton pairs tripped |
|---|---|
| 0.95 | 0 of 207 |
| 0.85 | 0 of 207 |
| 0.75 | 0 of 207 |
| **0.70** | **0 of 207** |

0.70 sits just above a measured ceiling of 0.644 and catches a propagated rung, which scores 1.000.

## Reachability -- MEASURED, because a guard that cannot fire is not coverage

The 13 reused ids have **388 existing rungs** on the roster available to compare against:
flea-beetles 109 (x2 crops), damping-off 39, early-blight 39, fusarium-wilt 30, late-blight 24,
carrot-rust-fly 13, root-knot-nematode 8, aster-yellows 6, colorado-potato-beetle 4, wireworms 3,
common-scab 3, aster-leafhoppers 1. The guard cannot be vacuous by construction.

The 9 MINTED ids have no precedent by definition and are out of this guard's reach. That is a
FORWARD condition, not a gap: document it, do not pad the harness total with it.


---

# CORRECTION 2026-09-01 -- the threshold was right, the METRIC was wrong

Everything above about WHICH population to calibrate against still holds. What was wrong is the
similarity function itself, and the independent source-truth pass caught it after every gate and the
mutation harness were green.

The guard used `difflib.SequenceMatcher` with **default arguments**, averaged over the two registers.
`autojunk` engages at 200 characters and junks any character present in more than 1% of the
sequence, which describes every seasoned register in this dataset; the mean then dilutes one copied
register against one independent one. The batch's single real copy --
`potato`/`common-scab`/`even_watering` against `beet`, same problem id, same method, beet's rung
authored earlier in the SAME session -- scored **0.431** and passed. Under `autojunk=False` with a
**per-register max** it scores **0.757**, above the 0.70 line, and it shares a 56-character verbatim
run with beet's rung.

**Recalibrated on the same peer population under the corrected metric:**

    62 singleton-vs-singleton shared-(id,method) pairs
    per-register max: ceiling 0.684   median 0.409
    nothing legitimate at or above 0.70 (0 of 62 at every threshold from 0.70 to 0.95)

The ceiling pair is apple vs strawberry on `powdery-mildew`/`sulfur` at 0.684: two crops saying the
same true thing about the same method in their own words. The threshold stays **0.70**. The corrected
batch tops out at **0.660**.

**The lesson is not about difflib.** The guard was reachable (243 comparisons), non-vacuous (its
anti-vacuity branch is driven), and mutation-tested (3 injections, 3 caught). Every property the
PLA-215 bar checks was satisfied, and the guard still did not see the thing it was built to see. A
mutation harness proves a guard FIRES; it cannot prove the guard MEASURES THE RIGHT THING. That
needs a positive control made of the real defect -- which is now
`test_metric_is_autojunk_free_and_per_register`, pinned with the actual pair.
