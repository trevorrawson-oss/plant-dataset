# PLA-8 BATCH 6 -- the two peas

**Canonical `17d0eac7` -> `3a87737a`.** 2 crops, 16 problems, **84 rungs** (42 + 42), 172 register
strings. Roster laddered **27 -> 29** of 121. No control_method, no source, no crop outside the two.

`snow-peas` and `sugar-snap-peas` share all eight problem NAMES and **82.8%** of their prose. **Two
authoring passes for two crops.** There is no twin here and none left anywhere: batch 5 consumed the
last one, so from here every batch costs one pass per crop.

---

## The premise, inverted from batch 5, and asserted just as hard

Batch 5's promote proved in canonical that two crops WERE byte-identical, which is what licensed
propagating one crop's ladders onto the other. This batch's claim is the opposite: these two are
**not** the same crop. `check_not_twins` refuses in both directions.

- **Identical in canonical** would mean propagation was available and this batch did double work.
- **Identical as staged** would mean one file was copied and the second pass never happened.

---

## The read's one real finding, and it is a SCOPING, not a removal

Both passes put a `wet_foliage_discipline` rung on powdery mildew, and **both independently flagged
the record as self-contradictory without being asked**. `cause_seasoned` says the fungus is *"favored
by warm days, cool nights, and dry foliage"* and that *"Spores spread on the wind"*, while
`prevention_seasoned` says to *"avoid working among wet vines."* Both authored the rung with **no
mechanism stated**, because neither could restate a mechanism the entry undercuts. That refusal to
invent is what surfaced it.

The method's own mechanism is free-water transport, and USU says powdery mildews *"do not spread in
rain or free water."* So the rung is dropped from both powdery-mildew ladders.

**THE DROP IS SCOPED, AND ALL THREE HALVES ARE PINNED:**

| | |
| -- | -- |
| NOT on powdery mildew | on either crop |
| **STILL on ascochyta blight** | on both crops, where the entry's own cause says *"Cool, wet weather and splashing water spread them"* |
| `airflow_spacing` STAYS on powdery mildew | its own `best_use` names powdery mildew, and humidity rather than free water is what it acts on |

Right use and wrong use of one method, in one crop, held apart by guards. A guard that checked only
the removal would be satisfied by deleting the method everywhere, which is the over-correction; the
harness attacks from both sides.

**Two orderings normalized on `snow-peas`** (root rots, ascochyta), where the cross-sibling check
flagged same-method-set-different-order on prose that is 8-of-8 and 7-of-8 identical across the two
crops. Cross-sibling conflicts went **2 -> 0**.

Note the root-rot order is the OPPOSITE of batch 5's beans: the peas read drainage-then-sowing
(*"well-drained soil or raised beds ... and never sow peas into soggy ground"*), the beans read
soil-warmth-then-drainage. Order follows each crop's own prose, not a house convention.

---

## Three catalog rounds, tested against real data

- **r6** corrected `planting_time_avoidance.best_use` from "one main generation" to a predictable
  damage window. **Pea weevil has one generation a year and a bloom-timed flight**, so it is the
  clean case the corrected wording has to admit. Pinned on both crops.
- **r7 REFUSED** to widen that method to a disease target after six T1 documents came back empty.
  **Both passes then hit exactly that wall on powdery mildew and reported it as the batch's most
  valuable gap.** The refusal is now observable as data: the method reaches an insect problem and no
  fungal one. Pinned.
- **r7's mints are both consumed**: `biofungicide` on powdery mildew (the crop's prose names
  *"Sulfur or a labeled biofungicide"*), `weed_host_control` on pea aphid and thrips.
- **r8's caution is a PRECONDITION**: the promote refuses to run unless the powdery-mildew exception
  is already on the method sheet. Shipping these ladders without it would leave the trap in place
  for the 21 other crops whose powdery mildew carries wet-handling advice.

The `biofungicide` rung sits BELOW `sulfur` on both ladders, which is why r7 chose the `biological`
tier over `soft_chemical`, and a test pins that ordering.

---

## Catalog gaps, hit independently by BOTH passes, none forced

- **`certified_clean_stock` is disease-only**, so pea weevil's *"freeze saved seed for several
  days"* and *"inspect dried peas for exit holes before storing"* have **no home at all**. Both
  passes named this the biggest gap in the crop. Two distinct missing concepts: saved-seed
  inspection, and post-harvest cold treatment.
- **`even_watering` is scoped `['mite','physiological']`**, so it cannot reach drought-stressed
  thrips even though host vigor is the one preventive lever that entry names. The catalog already
  gives this method to `mite` for exactly the same stress-susceptibility logic.
- **No tool, boot or soil hygiene method** for fusarium's *"avoid moving infested soil between
  beds."* One pass deliberately left it unplaced rather than smuggling it into a note; the other
  carried it in `garden_sanitation`'s notes and flagged the stretch.
- **No general scouting key** for pea weevil's *"monitor for adults during bloom"*, and `prompt_
  harvest` MEANS removing over-ripe fruit, not terminating a nearly finished planting -- both passes
  refused it for powdery mildew's *"pull the planting"* advice.

---

## Existing-prose findings, RECORDED NOT FIXED

1. **Powdery mildew contradicts itself on moisture** (above). Either the cause text or the prevention
   text is describing the wrong disease physics. This is the record that produced the read finding.
2. **The peas assert timing as a powdery-mildew control that their sources do not make.** *"Sow early
   so the crop finishes pod fill before the late-season mildew weather"* is cited to four sources;
   six T1 documents were fetched in r7 and none states the causal link. The components are each
   sourced, the conclusion is ours.
3. **Fusarium resistance is stated more strongly than the race caveat allows.** `cause_seasoned` says
   *"Several races exist"*, then prevention recommends three varieties as carrying wilt resistance
   with no qualifier, and the beginner register goes further with *"most modern snow peas"*.
4. **"Many modern snow peas carry powdery mildew resistance"** is a population-level claim with one
   named example behind it, against a Cornell page that is a checkable variety list.
5. **Oregon Sugar Pod II carries three different resistance claims across three entries**, sourced to
   different documents. Per the a-claim-lives-in-FIELDS lesson, correcting one obliges reading all
   three.
6. **`thrips` and `ascochyta-blight` are single-sourced** (`uc_ipm`) while carrying specific
   quantitative recommendations, thin relative to the other six entries.

---

## Verification

`gate_all` **121/121** · `control_ladder_gate` **0** · both variety gates **0** ·
`register_completeness` PASS · `register_coverage` PASS · `whole_crop_gate` PASS on both ·
`release_verify` **clean** (blast radius declared exactly) · COMPACT preserved · copy hygiene **0 of
172 strings**.

**Guard suite** `tools/test_promote_pla8_batch6.py` -- 51 tests.
**Mutation harness** `tools/mutate_pla8_batch6_suite.py` -- **34 injections, 34 caught, 0
survivors**, preflight 35/35, positive control GREEN, sentinel RED. Seven families: readfinding 10,
shape 6, blast 5, nottwins 5, rounds 5, ids 2, mechanics 1.

**TWO RUNS: 5 survivors, then 0**, and the five were five different lessons:

1. **A POST-state assertion with no refusal driver** (the tolerance rung sitting last) -- stays green
   with its guard disabled, because the staged data is already correct. Same defect batch 5 shipped.
2. **A test deriving its expectations from the table it validates** -- `R6_USE` emptied made the
   loop check nothing and pass. Fixed with a COVERAGE assertion naming the contents.
3. **A test hedged across two guards** -- it accepted either the refusal message or the `applies_to`
   message, so `applies_to` coherence answered for the refusal guard. Fixed by naming the guard.
4. **A mutation too weak to test its own guard** -- the field-set injection renamed only five of
   eleven fields, so the survivors still separated the crops. Strengthened to collapse the whole
   comparison.
5. **No driver for the crop-set comparison** in `verify_post`.
