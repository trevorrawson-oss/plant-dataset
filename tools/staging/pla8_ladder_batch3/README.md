# PLA-8 ladder rollout -- BATCH 3, the three cucumbers. READ COMPLETE.

3 crops: cucumber, pickling-cucumber, slicing-cucumber. 9 problems each, **137 rungs**
(44 + 47 + 46). Canonical at authoring time: `c13ddea5`. Catalog: 50 methods.

## This batch broke the batching tool, which is the most valuable thing in it

`ladder_batch.py families` reported these three as a **TWIN GROUP** and instructed: "identical prose
means the read is one problem set plus a mechanical equality check on its siblings." Batch 2 had
proved that shape on the four corns and the plan was to repeat it: author one crop, propagate,
assert identity in the promote.

**The signature it grouped on was `tuple(sorted(problem_name(p)))` -- problem NAMES ONLY.** It never
compared a character of prose. The 31% byte-identical figure printed two lines above came from a
different function (`prose_key`) and was an unrelated aggregate.

Measured field by field against `c13ddea5`, **not one of the ten reported twin groups was a true
twin**:

| reported "twin group" | prose fields identical |
|---|---|
| collards, kale | 28.7% |
| beefsteak-tomato, cherry-tomato | 34.4% |
| arugula/broccoli-microgreens, pea-shoots, radish-microgreens | 0.0% |
| **cucumber, pickling-cucumber, slicing-cucumber** | **72.2%** |
| grape-tomato, roma-tomato | 68.1% |
| dry-bean, green-beans-bush, pole-beans | 75.7% |
| acorn/butternut/spaghetti-squash | 76.8% |
| cayenne-pepper, habanero | 79.5% |
| snow-peas, sugar-snap-peas | 82.8% |
| yellow-summer-squash, zucchini-courgette | 96.7% |

**The corns are why nobody noticed.** They measure 96.2%, and all twelve differences sit on a single
problem (Raccoons: "sweet corn" where the others say "corn", same one-rung `exclusion_fencing`
ladder on all four). That propagation was sound. The group had been selected for a reason that had
nothing to do with prose and came out right anyway, so the method read as proven. **A mechanical
proxy standing in for reading is reproducible and wrong; reproducibility is not validity.**

## What the propagation would have cost here

Four ladder-relevant divergences, all on `pickling-cucumber`, all about variety resistance:

| problem / field | cucumber + slicing | pickling-cucumber |
|---|---|---|
| Cucumber beetles `prevention_seasoned` | "choose **non-bitter** varieties that attract fewer beetles" | "choose **wilt-tolerant** varieties such as **County Fair**" |
| Bacterial wilt `prevention_seasoned` | "less-bitter varieties" | "wilt-tolerant varieties such as County Fair" |
| Aphids `cause_seasoned` + `prevention_seasoned` | no resistance claim | "**CMV-resistant** pickling varieties reduce the virus risk" |
| Angular leaf spot `cause_seasoned` | no second mention | "start from clean seed and **lean on resistant varieties**" |

Copying cucumber onto pickling erases County Fair and two earned rungs; copying pickling outward
invents CMV resistance on two crops that never claim it. **Three independent authoring passes
instead of one plus a copy.**

## The tool is fixed, and the fix is mutation-tested

`prose_signature` + `family_cut` in `tools/ladder_batch.py` now group on **byte-identical problem
prose, in order** (order matters: propagation is index-wise, so a same-prose-different-order pair is
not propagate-safe). `families` now reports **two groupings with two different instructions**:

- **TRUE TWINS** -- propagate mechanically, promote asserts it. Now 2 groups / 4 crops.
- **SHARED-NAME FAMILIES** -- same problems, different prose, with the identity percentage printed.
  Cheap read, but **every member needs its own authoring pass**.

The corrected cut also finds propagate-safe SUBSETS the old one could not: **`dry-bean` +
`green-beans-bush` are true twins while `pole-beans` diverges from both.**

Guards: `tools/test_ladder_batch.py` (9 tests) + `tools/mutate_ladder_batch_suite.py` --
**8 injections, 8 caught, 0 survivors**, preflight 9/9 anchors, positive control GREEN, sentinel RED.
Two guard gaps were found and closed by that harness rather than by inspection:
1. `test_every_prose_field_is_load_bearing` built its fixture from the CLASSIC schema only, so
   dropping the microgreens half of `PROSE_FIELDS` survived. That is the identical blind spot
   `prose_key`'s own docstring already records. The test now covers both schemas and asserts
   COVERAGE of `PROSE_FIELDS`, not overlap.
2. Nothing distinguished an explicit null from an absent field.

## The read

**ZERO method-meaning mismatches**, matching batch 2 and against 22 of 165 in batch 1.

Five loose fits were flagged by the authoring agents. **All five resolved to ACCEPT on shipped
precedent** -- and four of the five had the same cause, below.

| flagged | precedent | verdict |
|---|---|---|
| `even_watering` on spider-mites | `heirloom-tomato/spider-mites`; `mite` is deliberately in `applies_to` | accept |
| `yellow_sticky_traps` on beetles | `jalapeno/pepper-weevil`, also a beetle | accept |
| `garden_sanitation` on beetles | 82 shipped uses across every problem type | accept |
| `balance_nitrogen` on aphids | 6 shipped uses, all aphids, incl. tomato and strawberry (neither leafy nor cole) | accept |
| `water_at_the_base` on powdery mildew | no precedent, but all three crops' `prevention_seasoned` says "avoid overhead watering" | accept, note carries the qualifier |

Also checked and clean: consequence clauses (no generic clause reused across problems -- batch 1's
worst defect class is absent; every "no cure" claim sits on a disease where it is true); hedges
(4/4 preserved, including slicing's "primarily a squash pest" and pickling's "reduce the virus risk"
rather than prevent); 0 absolutes in 274 new strings; copy hygiene 0/0/0/0/0.

### ONE REAL FIX APPLIED

**cucumber was missing the `resistant_varieties` rung its own prose earns on Cucumber beetles.**
cucumber and slicing-cucumber carry BYTE-IDENTICAL `prevention_seasoned` there ("choose non-bitter
varieties that attract fewer beetles"), but slicing's agent keyed it and cucumber's refused, reading
the catalog's `best_use` ("for diseases that recur in your beds") as disease-only.

Shipped precedent settles it: `resistant_varieties` is `applies_to: ["any"]` and already carries
varietal NON-PREFERENCE traits on insects -- `jalapeno/pepper-maggot` ("goes for thick-walled bell
types, and slender hot peppers are seldom bothered") is nearly the identical construction, plus
`sweet-corn/corn-earworm` x4 corns (husk cover), `fig/dried-fruit-beetle-souring` (tight eye), and
`apple/woolly-apple-aphid` (rootstock). Rung added; the two crops now agree.

### The bacterial-wilt divergence is CORRECT, and stays

pickling carries `resistant_varieties` on bacterial-wilt; cucumber and slicing do not. That is not
an inconsistency. pickling claims genuine wilt TOLERANCE (County Fair); the other two claim only
that less-bitter varieties attract fewer BEETLES, which is a vector claim. Keying that to
`resistant_varieties` on a bacterial problem would read as wilt resistance they never assert. This
is the already-recorded structural limit -- a vector-borne disease cannot carry a rung aimed at its
vector, and there is no disease->vector cross-reference -- first hit on Stewart's wilt.

## THE SYSTEMATIC FINDING: `best_use` is narrower than the method's own shipped use

Four of the five false flags, and cucumber's missing rung, have one cause. `prepare` puts
`best_use` in front of the authoring agents as **"what the method MEANS"**, and `best_use` was
written around each method's motivating crop and never widened as the method spread.

**Measured: 11 of 49 shipped methods.**

| method | `best_use` names | actually ships on |
|---|---|---|
| `garden_sanitation` | black rot | 45 problems / 16 crops / 7 types |
| `resistant_varieties` | clubroot, black rot | 29 problems / 14 crops / 5 types |
| `crop_rotation` | clubroot, black rot | 24 problems / 12 crops / 4 types |
| `floating_row_cover` | cabbageworms | 15 problems / 11 crops |
| `handpick` | cabbageworms | 15 problems / 13 crops |
| `airflow_spacing` | celery | 14 problems / 12 crops |
| `bt` | cabbageworms | 8 problems / 8 crops |
| `balance_nitrogen` | leafy and cole crops | 6 problems / 6 crops |
| `off_season_tillage` | hornworm | 6 problems / 6 crops |
| `even_watering` | celery blackheart | 4 problems / 3 crops |
| `bottom_watering` | fungus gnats, trays | 2 problems / 1 crop |

Batch 2 recorded `off_season_tillage`'s too-narrow gloss as a one-off prose defect. It is one of
eleven. The cost is real and recurring: **false gaps** (an agent refuses a legal, precedented rung)
and **wasted flagging** (four of five this batch). Deferred arc, now scoped and measured.

## Catalog gaps this batch hit, none forced

- **No plant-vigor / grow-through-the-window method.** "Keep young plants vigorous so they grow past
  the vulnerable stage" is load-bearing in BOTH the Cucumber beetles and Bacterial wilt entries on
  all three crops, and is now unrepresented. Biggest single gap.
- **No handling-discipline method.** "Do not work among wet vines" has no key. It landed on
  `garden_sanitation` for cucumber and `water_at_the_base` for the other two -- both defensible, both
  restating their own crop's prose. Left divergent deliberately: the fix is a method, not a note
  edit, and these crops are not twins.
- **No disease-side nitrogen method.** `balance_nitrogen` is `insect_soft_bodied`-only, so "avoid
  excess nitrogen" is placed on Aphids and dropped on Powdery mildew, where the same prose says it.
- **No `chlorothalonil` or any conventional FUNGICIDE key** (`carbaryl` and `pyrethroid` are the only
  conventional entries, both insecticides). Anthracnose loses its only named spray on all three and
  ends cultural-only. Downy mildew survives because copper is named alongside.
- **No potassium-bicarbonate key**, and `neem_oil` / `horticultural_oil` are scoped insect/mite only,
  so 3 of the 4 organic fungicides the powdery-mildew prose names are unexpressible. Only sulfur.
- **No trap-board key.** Folded into `handpick` on all three (the kill step is manual), consistently.

## Existing-prose defects found, NOT fixed here (READ-ONLY on canonical)

1. **`organic_treatment_seasoned` recommends chlorothalonil, a conventional synthetic, inside a
   field named `organic_`** -- on downy mildew AND anthracnose, all three crops.
2. **Angular leaf spot `organic_treatment_beginner` opens "There is no cure" and then recommends a
   copper spray.** The seasoned register handles it correctly ("no rescue spray that cures it ... to
   slow spread"); the beginner register reads as self-contradictory.
3. **Powdery mildew `cause_seasoned` says it does not need leaf wetness to infect, while both
   treatment registers say to avoid overhead watering.** Defensible (humidity vs free water) but the
   prose supplies no mechanism, and "dry weather with high humidity" reads as self-contradictory.
4. **`slicing-cucumber` Angular leaf spot cites only `['umn_ext']`** where cucumber and pickling both
   carry `['umn_ext', 'clemson_hgic']` for near-identical prose -- and slicing KEEPS the "roughly 75
   to 82°F with frequent rain" figure that pickling drops. So it asserts a numeric threshold while
   citing one fewer source than its siblings do for the same sentence. Now load-bearing: a rung
   restates it. Looks like a dropped source id, not a deliberate narrowing.
5. **Downy mildew is typed `fungal`** though its own prose calls it "a fungus-like water mold
   (Pseudoperonospora cubensis)". Correct within the gate's enum, which has no oomycete type.
   Flagged so nobody later reads the type as a taxonomic assertion.

## Status

Authored, merged, read, and verified in the scratchpad. **NOT PROMOTED.** Gates on the merged
scratch canonical: `control_ladder_gate` 0, `variety_resistance_gate` 0, `variety_ladder_delta_gate`
0, `register_completeness` PASS, `gate_all` PASS. Copy hygiene 0 across all five checks.
