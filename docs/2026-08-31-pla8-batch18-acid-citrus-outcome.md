# PLA-8 BATCH 18 -- ACID CITRUS: the batch that could not ship, shipping

`2cde361b` -> `514903db`. ONE promote. lemon + lime: **24 problems, 78 rungs** (lemon 36, lime 42).
Roster laddered **79 -> 81**. Catalog UNCHANGED at 62 methods, `source_catalog` UNCHANGED at 218,
**zero bystander crops touched**.

Supersedes `docs/2026-08-31-pla8-batch18-handoff.md`, which described this batch staged and unapplied.

---

## 1. Why this batch is different from the seventeen before it

It is the first batch that **could not ship at all** on the base it was authored against.

`sooty-mold` is typed `fungal`. Everything its record prescribes is INSECT control: suppress the
honeydew producer, manage the ants that protect it, wash the film off. `TYPE_TARGETS` forbids a
fungal type from naming any insect method, so lemon's author honestly emitted `control_ladder: null`
rather than stretch a key, and `ladder_batch.py merge` crashes on that because the runner has no
representation for a problem that cannot be laddered yet.

The fix was the previous commit, not this one: `ant_exclusion`, the catalog's 62nd method, anchored
on UC IPM Pest Notes 74108 ("Control of sooty mold begins with managing the insect creating the
honeydew"). That anchor is the sole reason `disease_general` is in the method's `applies_to`, and
without it the disease half of the mint would have been an INFERENCE across two steps.

So `check_sooty_mold_is_laddered` is not a shape check. It asserts that the specific defect which
motivated the mint is gone, and it is **the one guard whose failure would mean the mint accomplished
nothing**.

## 2. The shared-id divergence rule, settled here

**A shared id MAY carry different ladders where the RECORDS differ. It may NOT carry different
SHAPES for the same asserted content.**

Batch 17 settled the second half (`plum-curculio` had to collapse: same content, three
organizations). This batch settles the first.

Ten ids are shared between lemon and lime. Nine match method-for-method. One diverges:

* **`citrus-aphids` DIFFERS and that is allowed.** lemon carries `ant_exclusion`, lime does not.
  Both aphid entries only OBSERVE ants, but lemon's own sooty mold entry says "Managing ants, which
  protect those insects, is part of the same fix" and names those insects as "aphids, scale,
  mealybugs, or whitefly". lime has no sooty mold entry, so that sentence exists nowhere in its
  record. This is prose-grounded, not two agents guessing.
* **`citrus-canker` was COLLAPSED.** lemon used `prune_out_infection`, lime `garden_sanitation`, on
  sentences differing by one comma. `garden_sanitation` won because `prune_out_infection` means
  taking the cut well beyond the visible margin, back into clean tissue, and implies a curative
  excision the entry explicitly denies ("There is no cure for an infected tree"). The rung would
  have contradicted the sentence it restates.

`PERMITTED_DIVERGENCE` pins that state by id AND by the exact rung, and the guard refuses in **four**
directions: an unpermitted divergence, a divergence wider than the permitted rung, a pin left
standing after the two ladders CONVERGE (a dead exception is false documentation), and a batch with
no shared ids at all (which would make the guard vacuous).

## 3. Four id refusals, each verified against the records

| refused | why |
|---|---|
| `aphids` | generic across 50 vegetable crops; both citrus entries describe a complex that vectors citrus tristeza virus |
| `spider-mites` | twospotted-focused generic on 15 crops; lemon names citrus red mite AND twospotted with DIFFERENT monitoring seasons, so the generic loses the red mite half outright |
| `anthracnose` | generic on 14 crops; lime carries *C. gloeosporioides* (`lime-anthracnose`) and *C. acutatum* (`postbloom-fruit-drop`) as SEPARATE problems. Two Colletotrichum species on one crop; the generic would merge them |
| `bacterial-spot` | the peppers' Xanthomonas leaf spot; citrus canker is *X. citri* |

**ONE reuse, recorded honestly**: `mealybugs`, from chamomile. chamomile's `cause_seasoned` is
EMPTY, so the join rests on both entries being generically named rather than on a taxon match. Both
citrus records name no species either. Flagged in the promote, not hidden -- the
`problem-id-reuse-needs-a-taxon-check` shape, admitted rather than asserted away.

## 4. Citrus `type` is MIXED, and that changes the guard

Batch 17's six crops all carried the coarse legacy value, so that promote could assert a clean
coarse -> fine upgrade. Citrus cannot: **21 of these 24 problems ALREADY carry a fine type** and only
3 are coarse. (Roster-wide the field is messier still: of the unladdered problems, 129 carry NO type
at all.)

So the rule here is two-sided, and **the second half is the one that matters**: an already-fine type
must be PRESERVED EXACTLY, never quietly rewritten, because changing it moves which methods are
legal on the problem and no other guard would notice. The three legitimate upgrades are pinned by
name AND by destination, so a fourth cannot ride along and a pinned one cannot land somewhere else.

Batch 17's docstring generalized from its own six crops; its GUARD was correctly scoped, but the
claim around it was wider than what was measured. That is corrected here.

## 5. No rung states a temperature

The crops' scale entries say oil is unsafe above 95°F; the catalog's `horticultural_oil` caution
says 90°F. Both render. The mite entries carry NO figure at all, yet their rungs had imported 95°F
from the scale entry -- the introduced-figure class batches 15/16 already ruled on.

**RULED for the rungs only**: trim the figure from every oil rung and let the method's caution carry
the number. No rung can then contradict its own method, and the stricter figure governs by
construction.

This does **not** resolve the conflict. See §7.

## 6. Verification

* Guard suite **79/79**, green under **both runners** (`unittest` and `pytest`) -- the dual-runner
  check exists because a guard placed under `__main__` is invisible to pytest.
* Mutation harness: **50 injected, preflight 51/51 anchors exact, positive control GREEN, sentinel
  RED, ZERO SURVIVORS.** Families: schema, types, ids, sooty, ants, divergence, temps, vocab,
  materials, validate, blast, catalog, mechanics.
* `gate_all` **121/121** · `control_ladder_gate` **0** · `register_completeness` PASS ·
  `whole_crop_gate` PASS on lemon and lime.
* `release_verify` **clean** against a same-class reference (`--slug lemon --ref orange-navel
  --expect-changed lime`): section A confirms only the two declared crops changed, top-level
  non-crops changed nothing, `catalog +none -none`.

### The 16 section-E concerns were VERIFIED, not waved off

Against the DEFAULT reference (`lettuce-leaf`, an annual) section E reports 16 "novel region keys"
concerns. All are the documented reference-gap artifact, and the check is three-part:

1. Both crops' `regions` subtrees are **byte-identical between base and candidate** -- this promote
   did not touch a single region cell.
2. All four flagged keys (`cold_basis_beginner`, `cold_basis_seasoned`, `min_winter_temp_f`,
   `plantings_provenance`) already sat in **16 base lemon region cells**; they predate the promote.
3. `lettuce-leaf` lacks three of them entirely, which is the gap itself.

The only top-level keys this promote changed on either crop are `pests` and `diseases`. Re-run with
`--ref orange-navel`, section E goes fully quiet.

### A new guard family the earlier suites could not reach

The two refusals protecting `control_methods` and `source_catalog` live in `main()`, not in
`check()`. Batch 17 tested them by comparing serializations **from the suite** -- which asserts the
OUTCOME without ever driving the promote's own refusal, so those branches were unreachable by that
shape of test. `CatalogUntouchedInMain` reaches them by wrapping `apply_to` to sabotage the catalog
AFTER a clean apply and running `main()` against a temp fixture. Both branches caught, plus a
positive control proving the clean run passes and writes nothing.

### On the harness finding nothing

Zero survivors on the first sweep is not this project's usual result -- the three promote suites
built immediately before this one each had vacuous branches (three on batch 17, one on the mint).
The difference was method, not luck: every driver was enumerated from the promote's own branch list
rather than written to a description of what the guard was for, and each asserts the ONE message its
branch emits, so a branch with no driver is visible **while writing the suite** instead of after
running the harness.

Two branches were reached only because of that enumeration:

1. the closing SET assertion in `check_type_transition` -- every per-problem mutation
   short-circuits past it, so it needed a driver that makes a pinned problem's pre-state type
   already fine; and
2. the pair of `main()` catalog refusals above.

## 7. OPEN, carried forward -- these are NOT closed by this batch

1. **Oil temperature, 95°F vs 90°F.** Ruled for the RUNGS only. The crops' 95°F still renders from
   their own `organic_treatment_*` fields, beside the 90°F caution, on the same page. Needs a real
   sourcing pass against the citrus documents.
2. **lemon's phytophthora entry contradicts itself on the mulch setback**: `prevention_seasoned`
   says "a foot", `prevention_beginner` says "a hand's width". Roughly 3x apart in one record.
3. **lime anthracnose's BEGINNER register carries a flat absolute** ("Persian limes are not
   affected") where its SEASONED register hedges ("appears to be immune"). The authored rungs keep
   the hedge in both registers, so the ladder and the existing beginner prose now disagree. The
   existing prose is the thing that should change.
4. **Phytophthora is typed `fungal` while its own prose says "water molds, not true fungi".** No
   oomycete type exists, and `fungal` is the only bucket reaching `improve_drainage` and
   `resistant_rootstock`, so it is correct-by-necessity -- but the record contradicts its own field.
5. **A mis-pointed-key defect.** lemon's mealybug and sooty-mold entries make ant claims citing only
   `ipm.ucanr.edu/PMG/GARDEN/FRUIT/citrus.html`, which was READ and is an INDEX PAGE with no ant
   content at all. Needs a repoint to `ucanr_ext_ants` / `ucanr_ext_sooty_mold`, both already in the
   catalog. Same class as plum's San Jose scale citing a mealy plum aphid page (batch 17).

## 8. One observation for the sweet-citrus batch (PRE-EXISTING, not introduced here)

`release_verify` section G reports lemon's `calendar` as value-identical to `orange-navel` in 14
region cells. This promote authored no calendar cell and both crops' `regions` subtrees are
byte-identical to base, so this is pre-existing state surfaced by choosing a same-class reference,
not collateral. It may well be legitimate -- citrus in the cold zones is one container-and-overwinter
story -- but it should be looked at when sweet citrus is authored, since `orange-navel` is one of
those three crops.

## 9. The largest remaining CATALOG gap on citrus

**Nutrient supplementation has no method at all.** lemon's `iron-zinc-deficiency` ladder is a single
`even_watering` rung, and the entire actual treatment -- citrus micronutrient fertilizer, chelated
iron and zinc, EDDHA on high-pH soil, foliar micronutrient spray -- is unplaceable. Compounded by
`improve_drainage` being illegal on `physiological`.

**This is bigger than ant exclusion was**: it affects every physiological disorder on the roster, not
just citrus.

Other gaps both citrus authors hit: quarantine/reporting requirements (no key), nursery-stock
inspection on insect types (`certified_clean_stock` is pathogen-scoped), "keep trees unstressed and
not dusty" on insect types (`even_watering` is mite/physiological only -- note the same advice IS
placeable on `citrus-mites`, which is an `applies_to` artifact rather than biology), and a generic
pheromone monitoring trap (only `codling_moth_pheromone_trap` exists).

## 10. Roster position

Laddered **81 / 121**. Remaining: ~7 batches -- sweet citrus (grapefruit, mandarin-clementine,
orange-navel; 32 problems, **not yet prepared**), berries, woody herbs, soft herbs, flowers,
alliums, roots, other trees, and three stragglers (english-cucumber, edamame, pumpkin). Microgreens
stay LAST per the standing ruling.

Citrus was SPLIT on size: all five citrus measured 56 problems / 414 register strings, past the ~400
threshold `prepare` warns at. Sweet citrus is the other half.

## 11. Artifacts

| file | what |
|---|---|
| `tools/promote_pla8_batch18.py` | the promote (written in the prior session; unchanged here) |
| `tools/test_promote_pla8_batch18.py` | guard suite, 79 tests, replay-pinned |
| `tools/mutate_pla8_batch18_suite.py` | mutation harness, 50 injections, 13 families |
| `tools/staging/pla8_batch18_acid_citrus/` | authored + merged batch, `out_lemon.json` / `out_lime.json` |
