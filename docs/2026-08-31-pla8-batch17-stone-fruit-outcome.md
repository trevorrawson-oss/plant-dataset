# PLA-8 BATCH 17 -- STONE FRUIT: the *Prunus* category, six crops in one genus

**Date:** 2026-08-31 · **Base:** `213cb110` (batch 16's output) · **Output:** `2a9d3c85`
**Crops:** apricot, cherry-sour, cherry-sweet, nectarine, peach, plum
**Shipped:** 49 problems gain `id` + fine `type` + `control_ladder`; **137 rungs**. Roster laddered
**73 -> 79**. Catalog steady at **61** (no mint). 274 new register strings.

Per-crop: apricot 9/30, cherry-sour 7/24, cherry-sweet 9/30, nectarine 9/15, peach 8/16, plum 7/22.

---

## 1. The headline: ids were pinned BEFORE the fan-out, not minted six times

Six species in ONE genus is the exact setup that produced batch 13's defect, where all five agents
independently minted the SAME WRONG bacterial id. Convergence is not correctness. So the entire
`ID_CONVENTION` table was adjudicated against each record's own stated taxon *before any agent ran*,
and each agent was instructed to FLAG a pinned id it disagreed with rather than silently change it.

**Three refusals, each verified against the records rather than assumed:**

| refused | why |
| -- | -- |
| `bacterial-spot` | The roster id sits on five peppers whose disease is a generic *Xanthomonas* leaf spot -- and is actually NAMED "Bacterial leaf spot" there, so the id was already loose. Stone fruit bacterial spot is ***Xanthomonas arboricola* pv. *pruni***, stated outright in peach's own `cause_seasoned`. Ships as `bacterial-spot-pruni`. |
| generic `aphids` | apricot's entry names a two-species complex (green peach + mealy plum aphid); plum's says "Two aphids specific to plum" (*Brachycaudus helichrysi*, *Hyalopterus pruni*). Neither is the generic roster aphid on 50 vegetable crops. Ship as `apricot-aphids` / `plum-aphids`. |
| merging the two cherry fruit flies | cherry-sour names a THREE-species complex (*R. cingulata*, *R. fausta*, *R. indifferens*); cherry-sweet names *R. indifferens* ALONE. Same ruling shape as batch 16's sweet-pea refusal: the record's own prose governs, not the kinship. Likewise cherry-sweet's compound "Borers (peachtree and American plum borer)" ships as `cherry-borers`, never `peachtree-borer`. |

**Three reuses, each taxon-verified against the anchor record:** `plum-curculio` (apple; both records
name *Conotrachelus nenuphar*), `spotted-wing-drosophila` and `birds` (both strawberry).

**Result: the pinned map came through with zero drift.** All three reuses landed on the exact
existing strings with their anchor crop present; both refused ids remain absent from all six crops;
11 batch-internal shared ids and 9 crop-unique ids, exactly as adjudicated.

### The `brown-rot` scoping question, ruled NOT a refusal

cherry-sweet flagged that its brown rot names both *M. fructicola* and *M. laxa*. Measured: a clean
3-3 split (apricot / cherry-sour / cherry-sweet name both; nectarine / peach / plum name
*M. fructicola* alone). **Ruled a TEMPLATE artifact, not a taxon split** -- the six records fall into
two near-identical prose families and the species list tracks the template rather than the host.
Both species attack all six. The shared id stands; the *M. laxa* omission on three records is filed
as a record-completeness gap.

---

## 2. Two cross-crop adjudications, both settled against apple's SHIPPED ladders

Parallel authoring produced two inconsistencies on ids shared with already-certified crops. Both were
settled by READING apple's shipped ladders in canonical, not by preference.

1. **`plum-curculio` carries NO `handpick` rung.** apple's certified ladder folds jarring into
   `garden_sanitation` ("spread a sheet under the tree and tap the branches to jar the beetles
   down"). nectarine and plum independently folded it the same way; apricot and peach split it out
   and were collapsed. One join key cannot carry three shapes. `check_curculio_shape` guards it
   **including on apple**, so the anchor cannot drift either, and carries its own anti-vacuity check.
2. **`bacterial-spot-pruni` carries a hedged terminal `copper_fungicide` rung on all four crops.**
   apricot and peach originally refused it, reasoning that a rung reads as an endorsement. apple's
   certified fire-blight ladder ships copper exactly this way ("a limited, preventive help, not a
   cure, and it cannot save wood that is already infected"). Convention: **author it, hedged** -- a
   ladder is a menu ordered by invasiveness, and the hedge carries the "not reliable" message.

---

## 3. THE SELF-DENIAL GUARD IS NEW, AND IT CAUGHT A LIVE DEFECT THREE TIMES

Adding the terminal copper rung revealed that BOTH apricot and peach had a *cultural* rung whose note
asserted the ABSENCE of the rung being added:

* apricot: "There is no reliable rung above this one for a home tree ... which is why this ladder
  stops at cultural steps."
* peach, **surviving its first fix pass**: "once symptoms are showing there is no good home cure
  **to follow it with**."

Shipping either would have been a ladder that denies its own terminal rung.

**Why it earns a guard.** The prose is LOCALLY TRUE when written and becomes false only when a later
rung is added. It survives every structural gate and every read that looks at one rung at a time, and
there is no natural term to scan for.

**The guard is a proxy, and the proxy was measurably incomplete.** The first implementation was an
enumerated phrase list. It fired on 15 hits, which prompted a roster check: **97 shipped notes across
39 crops already use "rung"/"ladder" in consumer prose** (~2%), so a pure vocabulary ban would refuse
the roster rather than this batch. Narrowed to "a claim about which rungs exist" -> 5 real hits. Then
cherry-sour found a SIXTH by applying the *rule* instead of the regex ("is the base the rest of this
ladder sits on"), which the enumeration missed. The guard now implements the rule structurally
(ladder vocabulary + a structural claim in the same sentence) with the phrase list kept as a fast
statement of known shapes, plus a positive control asserting that honest MATERIAL hedges ("copper is
preventive at best rather than curative") are never rejected.

**Scope ruled:** batch 17 ships free of ladder-STRUCTURE claims. The ~2% roster-wide vocabulary leak
is FILED as its own sweep, same class as the spaced-`°F` item in playbook section 7.

---

## 4. Two premises that differ from batches 15/16, both nearly shipped silently

1. **The schema is NOT note-shaped.** Batches 15/16 crops carry `note_beginner`/`note_seasoned` on
   the problem. Stone fruit carries the OLDER full schema -- four dual-register pairs
   (symptoms/cause/organic_treatment/prevention) and no `note_*` field at all. Copying batch 16's
   premise check verbatim REFUSED THE ENTIRE BATCH on first run. The guard now asserts the full
   schema *and* refuses a note-shaped record, so the premise cannot silently invert later.
2. **`type` is an UPGRADE, not an addition.** All 49 problems already carried a coarse legacy value
   (`pest`/`disease`); the ladder gate resolves `applies_to` against a FINE value. Verified as the
   established pattern: **579 already-laddered problems roster-wide carry only fine types, zero
   coarse.** Without `check_type_transition` this promote would have overwritten an existing field as
   a side effect of `apply_to`, unasserted in either state.

---

## 5. The catalog is the problem, not the authors (playbook section 6)

Counted by how many of the six bots hit each wall INDEPENDENTLY:

| gap | bots |
| -- | -- |
| No trunk-care key at all (wound avoidance, white trunk paint, keep mowers off bark) | **6** |
| `airflow_spacing` MEANS says "set at planting", but every tree crop uses it for canopy pruning (all citing apple's shipped precedent) | **5** |
| `borer_stem_surgery` MEANS is written entirely for squash vines; apricot correctly predicted all six would hit it | **5** |
| `prune_out_infection` illegal on `insect`, so borer canker removal has nowhere to go | **4** |
| `even_watering` excludes fungal | **4** |
| `balance_nitrogen` lacks `bacterial` | **4** |
| No mating-disruption pheromone key (already known-owed) | **2** |
| No ground/pupation barrier for a soil-pupating insect | **2** |
| No post-harvest chilling key (SWD refrigeration) | **2** |

The `balance_nitrogen` gap has a **shipped workaround already in the data**: apple's certified
fire-blight `garden_sanitation` rung carries "Go easy on fertilizer: soft, sappy new growth from too
much nitrogen..." rather than using a key.

### What this does to `garden_sanitation`

29 of 137 rungs (21%) name it, across 29 distinct problems, and they carry **seven distinct actions**.
Squarely on-meaning: mummy/dropped-fruit/leaf cleanup (17), removing a tree that cannot be saved (4 --
the catalog explicitly assigns this here), in-season shoot-tip clipping (2). **Eight are off-meaning,
every one forced by the type map**: pruning out scale-crusted wood and cankers (3), trunk-base
clearing plus wound avoidance and trunk paint (3), nursery-stock inspection (1), late-nitrogen
restraint (1).

This is the `bottom_watering` shape -- one key meaning several things. **Ruled: ship as authored,
file the catalog remediation.** The content in these rungs is correct; the metadata key is wrong, and
it is wrong the same way in already-shipped data. Widening mid-batch would mean re-authoring and
would leave apple inconsistent with its own siblings.

---

## 6. Source-truth findings FILED, not fixed

* **cherry-sweet's borer entry has a taxonomic slip.** `cause_seasoned` says "Clearwing moth and
  beetle borers"; the American plum borer is a pyralid MOTH (*Euzophera semifuneralis*), not a beetle.
* **plum's San Jose scale is anchored to a mealy plum aphid page**
  (`ipm.ucanr.edu/agriculture/plum/mealy-plum-aphid/`) as its SOLE source. A mis-pointed key
  candidate: wrong document for scale biology, symptoms and dormant-oil control.
* **Brown rot's bloom-time fungicide names a CLASS and never a material** on all four crops that
  carry it. Under the material rule no rung could be authored, so the batch's highest-severity
  disease ships sanitation-only while apricot's own prose says sanitation alone is insufficient in
  humid regions. A sourcing gap, not a ladder gap.
* **peach's bacterial spot beginner register drops the pathovar** the seasoned register carries, so a
  beginner reader never learns this is a different organism from the pepper disease of the same
  common name -- the exact distinction the id refusal turns on.
* **peachtree borer prevention is internally tense**: clear grass and weeds from the trunk base, and
  keep mowers and trimmers off the bark. A reader following the first can create the wound the second
  warns about.

---

## 7. Verification

* Guard suite **61/61** (`tools/test_promote_pla8_batch17.py`).
* Mutation harness **38 injected, preflight 39/39 anchors exact, positive control GREEN, sentinel
  RED**. Families: schema, types, ids, splits, curculio, copper, selfdenial, materials, validate,
  blast, mechanics.
* `gate_all` PASS (every certified crop) · `control_ladder_gate` 0 · `register_completeness` PASS ·
  `whole_crop_gate` PASS x6 · copy hygiene clean on all 274 new strings.
* `release_verify`: two concern classes, both verified as known tool artifacts rather than waved off.
  (a) 17 "novel region keys vs lettuce-leaf" -- **all six crops' `regions` subtrees are BYTE-IDENTICAL
  between base and candidate** and `chill_basis_*` already exists in the base, so these are the
  documented section-E false flag where a key is called novel because the ANNUAL reference lacks it.
  (b) "crops changed != expected" -- `--expect-changed` appends to the pilot default, so it demands
  cherry-tomato change; correct behavior for this batch is that it does not.

### What the harness caught that the suite did not

Four guard branches were **green and vacuous** until the harness ran:

1. `not in ID_CONVENTION` -- masked by the `i != want` check below it; no driver.
2. the reuse-anchor branch -- the existing test tripped "resolves nowhere" first.
3. the structural self-denial rule -- every test used a phrase the *enumerated* list already caught.
4. **the positive control itself** -- the test RE-IMPLEMENTED the comparison instead of driving the
   promote's function, so disabling that function changed nothing. A test that duplicates the logic
   it checks is vacuous however green it looks.

A fifth was found while writing the suite: `kept the coarse type` sat behind the fine-type membership
check and could never fire. Found only because every driver asserts its branch's ONE message.

---

## 8. Next

Batch 18 (acid citrus: lemon, lime) is AUTHORED and BLOCKED. `sooty-mold` is a `fungal` problem whose
entire control is INSECT control (suppress the honeydew producer, manage ants, wash the film off);
`TYPE_TARGETS` forbids a fungal type from naming any insect method, so lemon honestly emitted
`control_ladder: null` -- and `ladder_batch.py merge` crashes on it, because the runner has no
representation for a problem that cannot be laddered yet.

**Ruled (Trevor, 2026-08-31): mint `ant_exclusion` first**, with `applies_to` spanning
`insect_soft_bodied`/`insect_general` AND `disease_general`. Both citrus bots independently named ant
exclusion the largest citrus gap; it fixes sooty mold, scale and mealybugs at once. Batch 18 lands
after that catalog revision. Every new method needs a real T1 document fetched and READ.

Also carried forward: the citrus records say horticultural oil is unsafe above **95°F** while the
catalog's own `horticultural_oil` CAUTION says **90°F** -- a 5-degree conflict on the same material,
needing one ruling rather than per-crop drift. And lime anthracnose's BEGINNER register carries a flat
absolute ("Persian limes are not affected") where its seasoned register hedges ("appears to be
immune").

Batches remaining after 18: ~8 (sweet citrus, berries, woody herbs, soft herbs, flowers, alliums,
roots, other trees, stragglers; microgreens LAST per the standing ruling).
