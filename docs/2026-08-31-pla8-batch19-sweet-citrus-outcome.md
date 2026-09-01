# PLA-8 BATCH 19 -- SWEET CITRUS: the category closes

`514903db` -> `50bc203f`. ONE promote. grapefruit / mandarin-clementine / orange-navel:
**32 problems, 108 rungs** (35 / 32 / 41). Roster laddered **81 -> 84**. Catalog unchanged at 62,
`source_catalog` unchanged at 218, zero bystander crops.

**All five citrus are now fully laddered.** The read detail lives in
`tools/staging/pla8_batch19_sweet_citrus/READ_NOTES.md`; the id decisions in `PINNED_IDS.md`
alongside it.

---

## 1. What makes this batch structurally different

**Nine of the fifteen ids already existed on lemon or lime at the base commit.** Every earlier batch
compared crops that were all inside the batch. Here the comparison is against CANONICAL, and a
within-batch guard of batch 18's shape would have passed three crops that silently contradict two
shipped ones.

`check_cross_batch_divergence` reads every crop on the roster that carries a shared id. It refuses an
unpinned divergence, a pinned one that has CONVERGED (a dead exception is false documentation), a
change to the set of multi-crop ids, and a batch with no shared ids at all.

## 2. Ids were pinned BEFORE fan-out, and drift was zero

32/32 ids match the table; zero silent retypes. This repeats batch 17's result and is the second
consecutive batch where pre-pinning eliminated drift entirely.

**`ladder_batch merge` cannot enforce this.** It reports `ids reused 0` because the pre-state
problems carry no `id` at all, so the id-stability rule has nothing to compare against. The table is
enforced by briefing and then VERIFIED programmatically. Assuming it would have been the batch 13
failure, where all five agents minted the same wrong bacterial id and convergence was mistaken for
correctness.

Three pins were load-bearing:

* **`Huanglongbing (citrus greening, HLB)`** against acid citrus's `Huanglongbing (HLB, citrus
  greening)`. The parentheses are REORDERED; a name-derived slug diverges from a live join key.
* **`brown-rot`, refused.** See below.
* **The mite split.** See below.

## 3. The taxon trap

orange-navel's "Brown rot of fruit" must not take `brown-rot`.

| | organism, per the record's own prose |
|---|---|
| stone fruit `brown-rot` (batch 17, 6 crops) | *"The fungus **Monilinia fructicola**. It overwinters in mummified fruit..."* |
| orange-navel "Brown rot of fruit" | *"Soil-borne **Phytophthora** species... the same water molds that cause foot rot"* |

A true fungus versus an oomycete. Same common name, unrelated organisms: the `pea-weevil` shape.
Ships `citrus-brown-rot`. It also does not reuse `phytophthora-foot-rot`, though its own prose says
that is the same organism, because it is a different organ with different controls.

### A dead branch, caught before the harness ran

`check_brown_rot_taxon_split` first asked `holders & set(CROPS)` where `holders` is computed with
`exclude=CROPS` -- so the branch could never fire. It read as coverage. Worse, the harness would
have reported its mutation as *caught*, because a different branch catches the same injection.
Replaced with the reachable question (has the id leaked onto the acid citrus?) and given its own
driver.

## 4. The mites split, in both directions

Acid citrus carries ONE composite `citrus-mites`, and both records say why: *"Several mite species
feed by puncturing leaf cells."* Sweet citrus does not:

* grapefruit **Citrus rust mite**: *"builds up on the rind... warm, humid conditions favor it, which
  is why the Southeast sees far more russeting than the arid West."*
* mandarin and orange-navel **Citrus red mite**: *"thrives in heat and dust... trees sprayed with
  broad-spectrum insecticides, which remove predatory mites."*

Different family, organ, and regional driver. Mints `citrus-rust-mite` and `citrus-red-mite`.

**`citrus-mites` is NOT retro-split.** It was pinned one commit ago and those records are genuinely
composite. The guard refuses collapsing the new ids AND re-deriving the old one, so citrus carries
three mite ids -- which reflects what the records say rather than a tidier model.

## 5. Zero type upgrades, a first

All 32 problems already carry a fine type, so the rule takes its strong form: **no type may change
at all.** Batch 17 could assert a clean coarse -> fine upgrade; batch 18 was mixed and needed a
two-sided rule. The guard also refuses if that measured premise ever breaks, so the strong form
cannot outlive the state it was measured against.

## 6. The read: three rulings, every one against a sibling

Rungs went 111 -> 108. Nothing was added.

1. **`greasy-spot`, orange-navel drops `water_at_the_base`.** Its record says *"avoid prolonged leaf
   wetness where you can"* -- a goal, not an irrigation practice. Its author's own note said *"the
   method supplies the concrete action. Sibling-consistent with lemon/lime."* That is importing a
   practice for consistency: the sibling-precedent trap. lemon and lime keep theirs because they say
   *"avoid overhead wetting of foliage"*, which IS the action.
2. **`asian-citrus-psyllid`, grapefruit and mandarin drop `garden_sanitation`.** No sweet-citrus
   record mentions removing trees, only quarantine compliance and reporting, which is regulatory
   conduct. Two authors used the key and both flagged it as their loosest fit; the third refused.
   **The refuser was right.** The LARGE divergence is real and preserved: acid citrus says *"spraying
   your own tree does little"*, sweet citrus says *"spray oil or soap on the new growth"*.
3. **`citrus-canker`, grapefruit re-keys `prune_out_infection` -> `garden_sanitation`.** It
   contradicted a STANDING batch 18 ruling on that exact id. The tell was internal: the author's own
   prose already read *"it does not clear the tree"*, honest prose on a key that means curative
   excision. The ruling is now enforced roster-wide, including on shipped acid citrus.

**The transferable lesson: two authors stretching a key and one refusing it is a signal to read the
records, not to take the majority.** The self-flags are the highest-value part of an authoring
report.

## 7. Verification

* Guard suite **72/72**, green under both runners.
* Mutation harness **51 injected, 52/52 anchors exact, positive control GREEN, sentinel RED, ZERO
  SURVIVORS**, 14 families (schema, types, ids, brownrot, mites, canker, crossbatch, temps, vocab,
  materials, validate, blast, catalog, mechanics).
* `gate_all` **121/121** · `control_ladder_gate` 0 · `register_completeness` PASS ·
  `whole_crop_gate` PASS x3 · 216 new strings hygiene-clean.
* `release_verify` section A clean: only the three declared crops changed, top-level non-crops
  none, `catalog +none -none`, no new violations. Section E's concerns are the documented
  reference-gap artifact, verified by showing all three `regions` subtrees byte-identical base to
  candidate and the flagged keys already present in 16 base cells.

**A `release_verify` usage note worth keeping:** `--ref` must name a crop the promote does NOT
change. Passing an in-batch crop produces a "reference crop CHANGED" concern that is an artifact of
the invocation, not the data.

## 8. Two open questions CLOSED by reading the documents

### The oil temperature ruling from batch 18 was wrong

* **UC IPM, "Precautions for Using Petroleum Oil Sprays", Citrus (UC ANR Pub 3441)**: *"Do not spray
  oils when temperatures exceed **95°F**..."* and *"in coastal regions, do not spray if the
  temperature will exceed **85° to 90°F**..."*
* **UC IPM Pest Notes 7405**, the catalog's anchor for its 90°F caution, is **the SPIDER MITE
  document**. It never mentions citrus and says nothing about fungal disease.

So the crops' 25 instances of 95°F are correctly sourced, not drift, and **"the stricter number
governs" is wrong in both directions**: inland citrus may spray to 95°F, while the true coastal limit
is 85°F, stricter than the catalog's. The honest model is regional. The source class is already
admitted (`uc_ipm_citrus_ants` is the same Pub 3441), so this is a sibling mint.

### The `horticultural_oil` widening is defensible but not clean

UF/IFAS HS263 says oil *"reduces the penetration of the spores into the leaf"* and lists oil alone in
its timing recommendation, so `fungal_foliar` would not be a category error. But the same document
says oil prevents or delays rather than controls, and that *"on more susceptible varieties, like
grapefruit or tangelos, copper is usually required"* -- grapefruit being one of this batch's crops.

A web summary of that document claimed oil could be used *"in place of copper"*. The document does
not support that. **The read caught what the summary would have shipped.**

Recommendation: its own catalog round with a caution, not a quiet `applies_to` edit inside a crop
batch.

## 9. Filed, not fixed

1. **`katydids` `prevention_beginner` is about CATERPILLARS** in an entry otherwise entirely about
   katydids, and in the wrong register. A template leak, and it matters for control: a caterpillar
   would legitimize a `bt` rung, a katydid would not.
2. **`citrus-brown-rot` calls its organism "the fungus"** in `symptoms_seasoned` while `cause_*`
   correctly says water mold -- the very distinction used to justify minting the id.
3. **The phytophthora mulch-setback contradiction is on grapefruit too**, not just lemon. A TEMPLATE
   defect; the fix must sweep all five citrus.
4. **Catalog gaps**: `horticultural_oil` cannot reach a fungal problem; skirt pruning has no method
   and is orange-navel's leading brown-rot control; `certified_clean_stock` is pathogen-scoped so
   "inspect incoming nursery stock for scale" is dropped from grapefruit entirely; nutrient
   supplementation still has no method.

## 10. Roster position

Laddered **84 / 121**; 44 crops carry no ladder. Remaining: berries, woody herbs, soft herbs,
flowers, alliums, roots, other trees, and three stragglers (english-cucumber, edamame, pumpkin).
Microgreens stay LAST per the standing ruling.
