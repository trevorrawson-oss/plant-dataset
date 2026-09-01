# BATCH 19 -- read notes, opened during authoring

## 1. THE OIL TEMPERATURE FINDING IS BIGGER THAN BATCH 18 RECORDED, AND MAY BE RULED WRONG

Batch 18 filed this as an open sourcing question and ruled, for the rungs only, that "no rung states
a figure, so the method's caution carries it and the stricter number governs by construction."

Measured across all five citrus at `514903db`:

* **25 field instances carry `95°F`. Every single one. There is no `90` anywhere in citrus prose.**
  * lemon 2, lime 2, grapefruit 7, mandarin-clementine 7, orange-navel 7
  * across 7 distinct problems: scale, aphids, leafminer, ACP, rust mite, red mite
  * all in `organic_treatment_beginner` / `organic_treatment_seasoned`
* The catalog's `horticultural_oil.cautions[0]` says: *"Do not use oils on water-stressed plants or
  when temperatures exceed 90°F"*, anchored to UC IPM **Pest Notes 7405**, a GENERAL oil document.

**Why "stricter governs" may be the wrong ruling.** 25 of 25 is not drift or sloppiness; it is a
consistent claim, which is what a citrus-specific source looks like. UC IPM's general oil guidance
and its citrus guidance can BOTH be right at different scopes: 90°F for oils generally, 95°F for
citrus specifically. If that is what the documents say, then "the stricter number governs" is not
conservative, it is **under-advising** -- it tells a citrus grower not to spray at 92°F when their
own crop's source says they may.

The batch 18 ruling is safe for the RUNGS either way (they state no figure). What it does not settle
is the 25 rendered instances. **This needs the citrus documents read, not a default to the smaller
number.** Do not "fix" the 95s to 90 without that read.

## 1b. RESOLVED BY READING THE DOCUMENTS (2026-08-31). THE 95°F IS CORRECT AND THE RULING IS NOT.

Both documents were fetched and read. The hypothesis in section 1 is CONFIRMED, and the real answer
is better than "both are right at different scopes": **the citrus limit is REGIONAL.**

**UC IPM, "Precautions for Using Petroleum Oil Sprays", Citrus (UC ANR Pub 3441)**
`https://ipm.ucanr.edu/agriculture/citrus/precautions-for-using-petroleum-oil-sprays/`

> "Do not spray oils when temperatures exceed **95°F** or relative humidity falls to 20% or below"
>
> "in coastal regions, do not spray if the temperature will exceed **85° to 90°F** or the relative
> humidity goes below 30%"

**UC IPM Pest Notes 7405** (the catalog's current anchor for the 90°F caution) was also read. It is
**the SPIDER MITE document**. Its sentence is *"Don't use soaps or oils on water-stressed plants or
when temperatures exceed 90°F"*, it never mentions citrus, and it says nothing about any fungal
disease.

### What this settles

1. **The crops' 95°F is CORRECTLY SOURCED, not drift.** All 25 instances match the citrus-specific
   document. Nothing should be "fixed" to 90.
2. **"The stricter number governs" is WRONG IN BOTH DIRECTIONS.** Inland and desert citrus, which is
   most of our citrus regions, may safely spray to 95°F, so 90°F costs a legitimate window. On the
   COAST the real limit is **85°F**, which is stricter than the catalog's 90°F, so the rule
   under-warns exactly where it claimed to be conservative.
3. **The honest model is regional**, and the rungs are region-agnostic. The catalog caution should
   name the general figure and the citrus prose should carry the regional split, or the caution
   itself needs a citrus scope.
4. **The source is ALREADY ADMITTED.** `uc_ipm_citrus_ants` (Pub 3441) was minted by batch 18 for
   `ant_exclusion`, and `uc_ipm_citrus_timings` sits in the same `/agriculture/citrus/` tree. The
   oil precautions page is a sibling under the same publication, so a `uc_ipm_citrus_oil_precautions`
   mint is a sibling repoint, not a new tier argument.

**NOT actioned in batch 19**, which touches no `organic_treatment_*` prose and states no figure in
any rung. This is now a specified edit rather than an open question.

## 1c. THE `horticultural_oil` WIDENING: DEFENSIBLE, BUT NOT A CLEAN WIN. DO NOT DO IT HERE.

**UF/IFAS HS-1016/HS263, "Field Identification and Management of Greasy Spot Disease"**
`https://ask.ifas.ufl.edu/publication/HS263`

> "Petroleum oil reduces the penetration of the spores into the leaf, but does not reduce spore
> germination."
>
> "a single application of **oil** or oil and copper in mid-May to June or two spray applications
> which are timed to be applied in mid-May to June with the second application in late July."

So oil acts on the fungus DIRECTLY and appears alone in the timing recommendation: widening
`horticultural_oil` to `fungal_foliar` would not be a category error, and the four crop records that
recommend it are not inventing anything.

**But the same document limits it**: oil prevents or delays rather than controls, and *"on more
susceptible varieties, like grapefruit or tangelos, copper is usually required"*. **Grapefruit is
one of this batch's three crops**, named by the source as needing copper.

Note also that a general web summary of this document said oil could be used "in place of copper",
and the document itself does not support that reading. The summary was wrong; the read is the
evidence.

**Recommendation:** the widening deserves its own catalog round with a caution ("partial, and
susceptible varieties still need copper"), NOT a quiet applies_to edit inside a crop batch. Also
worth checking: mandarin's own prose says oil "gives good backyard control", which is stronger than
what UF/IFAS supports for susceptible varieties.

## 2. CROSS-BATCH SHARED IDS -- NEW THIS BATCH

Batch 18's divergence guard compared lemon against lime, both in-batch. Batch 19 shares **9 ids with
crops already shipped at `514903db`**, so the comparison is now against CANONICAL, not just within
the batch. The promote must check both.

Baseline (already shipped, acid citrus):

| id | lemon | lime |
|---|---|---|
| `scale-insects` | ant_exclusion > beneficial_predators > horticultural_oil | same |
| `citrus-aphids` | balance_nitrogen > water_spray > **ant_exclusion** > beneficial_predators > insecticidal_soap > horticultural_oil | same minus ant_exclusion |
| `citrus-leafminer` | balance_nitrogen > beneficial_predators > horticultural_oil | same |
| `phytophthora-foot-rot` | improve_drainage > resistant_rootstock > prune_out_infection | same |
| `greasy-spot` | garden_sanitation > airflow_spacing > **water_at_the_base** > copper_fungicide | same |
| `citrus-canker` | resistant_varieties > wet_foliage_discipline > garden_sanitation > copper_fungicide | same |
| `sooty-mold` | ant_exclusion | (not present) |
| `asian-citrus-psyllid` | garden_sanitation | same |
| `huanglongbing` | certified_clean_stock > garden_sanitation | same |

### Divergences to adjudicate at the read

1. **`greasy-spot` drops `water_at_the_base` on BOTH new crops**, independently, both authors giving
   the same reason: the prose does not assert irrigation placement. Two independent agents reaching
   the same refusal is evidence the records genuinely differ from lemon/lime. ALLOWED under the
   batch 18 rule, but confirm by reading all four greasy-spot records.
2. **`asian-citrus-psyllid`: 1 rung on lemon/lime, 4 on grapefruit.** grapefruit's
   `organic_treatment` explicitly recommends oil and soap on new flush; the acid citrus records do
   not. Records differ, so allowed -- but this is the widest divergence in the set and deserves a
   direct read of all the ACP records side by side.
3. **`citrus-canker`: 4 rungs on lemon/lime, 5 on grapefruit, and they are not nested.** grapefruit
   DROPS `resistant_varieties` (its prose recommends no cultivar choice, though it calls grapefruit
   "highly susceptible") and ADDS `certified_clean_stock`, `airflow_spacing`, `prune_out_infection`.
   This is a shape difference, not a length difference. Read carefully.

## 3. TWO CATALOG WALLS HIT INDEPENDENTLY BY BOTH AGENTS

The playbook rule is: several bots blocked on the same control means the CATALOG, not the crop.

1. **`horticultural_oil` cannot reach a fungal problem.** `applies_to` is
   `[insect_soft_bodied, insect_general, mite]`, so the citrus recommendation "horticultural oil,
   alone or with copper, in early summer" for **greasy spot** has no legal rung. Both new agents
   flagged it, and batch 18's lime hit it too. **Three crops, three independent authors.** Same
   SHAPE as the `ant_exclusion` blocker, which was fixed by giving the method a `disease_general`
   target. Candidate for a catalog decision.
2. **`certified_clean_stock` is pathogen-scoped**, so "inspect incoming nursery stock for scale" is
   illegal on an insect-type problem. On grapefruit the advice is **dropped from the crop entirely**
   (genuine content loss); on mandarin it survives only because HLB carries the same sentence.
   Already flagged in batch 18's handoff; now confirmed as recurring.

## 4. PROSE DEFECTS CONFIRMED ACROSS CROPS (template inheritance)

* **The phytophthora mulch setback contradiction is on grapefruit TOO**, byte-for-byte the same
  shape as lemon's: `prevention_seasoned` "a foot" vs `prevention_beginner` "a hand's width".
  Batch 18 filed this as a lemon defect. It is a TEMPLATE defect spanning at least two crops, so the
  fix must sweep all five citrus, not just lemon. (A claim lives in FIELDS, not in a record.)
* **Alternaria brown spot (mandarin) is absolute in one register and hedged in another**:
  `cause_beginner` "It cannot infect older leaves or older fruit" and `cause_seasoned` "are not
  infected", against `symptoms_seasoned` "fruit becomes more resistant as it matures, so mostly
  young fruit is affected". The authored rungs keep the hedge; the `cause_*` fields should be
  softened.
* **The Alternaria variety claim is an ABSENCE FROM A LIST, not a resistance rating** ("not among
  the varieties UF lists as susceptible"). Load-bearing: a future `varieties[].resistance` grade
  hung off `alternaria-brown-spot` must NOT record clementine as resistant on this evidence.

---

# RULINGS MADE AT THE READ (applied to the staged output)

Rungs went 111 -> 108. Every change removed or re-keyed a rung; none was added.

## R1. `greasy-spot` -- orange-navel DROPS `water_at_the_base` (111 -> 110)

Read all five records. The method means directing water to the soil rather than overhead.

* lemon and lime say **"avoid overhead wetting of foliage"** -- that is the action. Their rung stands.
* grapefruit and mandarin say nothing about wetting or irrigation. Both authors refused it. Correct.
* orange-navel says **"avoid prolonged leaf wetness where you can"** -- a GOAL, not an irrigation
  practice (leaf wetness also comes from dew and rain). Its author flagged its own reasoning:
  *"the method supplies the concrete action. Sibling-consistent with lemon/lime."*

That is importing a practice the record does not state, in order to match siblings. **Sibling
consistency is not evidence.** Dropped. Result: 4 rungs where the prose names overhead wetting, 3
where it does not.

## R2. `asian-citrus-psyllid` -- grapefruit and mandarin DROP `garden_sanitation` (110 -> 108)

The big divergence here is REAL and is preserved: the records give opposite advice.

* lemon and lime: *"Spraying your own tree does little against the psyllid... backyard chemical
  control is of limited value."* The prescribed action is detection, reporting, and **removing
  confirmed greening-infected trees**. `garden_sanitation` covers "pulling a plant that cannot be
  saved", so their 1-rung ladder is exactly right.
* all three sweet citrus: *"Spray horticultural oil or insecticidal soap on the new growth to knock
  back the young psyllids, repeating each time fresh leaves appear"*, plus conserve Tamarixia. A
  multi-rung ladder is right.

The SUB-question was `garden_sanitation`, kept by grapefruit and mandarin, refused by orange-navel.
**The refuser was right.** No sweet-citrus record mentions removing trees or seasonal cleanup; they
carry quarantine compliance and reporting, which is regulatory conduct, not sanitation. Both authors
who used it flagged it as the loosest fit in their crop. Dropped from both; all three sweet citrus
now read `beneficial_predators > insecticidal_soap > horticultural_oil`.

The regulatory content is not lost: it still renders from each entry's own `prevention_*` fields,
and "buy certified" is carried legally on the HLB ladder by `certified_clean_stock`.

## R3. `citrus-canker` -- grapefruit re-keys `prune_out_infection` -> `garden_sanitation`

**This one contradicted a STANDING RULING.** Batch 18 already adjudicated this exact id: lemon used
`prune_out_infection`, lime used `garden_sanitation`, and `garden_sanitation` won because
`prune_out_infection` means taking the cut back into clean tissue and implies a curative excision the
entry denies.

All three sweet-citrus canker records repeat that denial (*"no cure"*, *"without curing existing
ones"*), and grapefruit's rung used the curative key anyway.

The tell: **the author's own prose was already correct for the other key** -- *"This lowers how much
is on hand to spread; it does not clear the tree"* and *"a reduction in spread pressure rather than
a treatment, since the tree carries the infection whatever comes off it."* Honest prose, wrong key.
Re-keyed; the note needed no rewrite. Tier ordering still holds (cultural before soft_chemical).

## R4. The remaining canker divergences are CORRECT and stay

* grapefruit omits `resistant_varieties`: its prose calls grapefruit "highly susceptible" but
  recommends no cultivar choice. lemon says "plant resistant or tolerant types"; orange-navel says
  "choose less-susceptible varieties". The omission tracks the records.
* grapefruit and orange-navel add `certified_clean_stock` and `airflow_spacing`: both say "plant
  certified disease-free stock" and "provide good air movement". lemon and lime say neither.

## R5. `citrus-aphids` -- lime is now the lone crop WITHOUT `ant_exclusion`

All three sweet citrus carry it, matching lemon. Batch 18's `PERMITTED_DIVERGENCE` pinned
`citrus-aphids` as differing by exactly this rung, and that still holds; the pin's shape just
inverts (4 of 5 carry it, lime is the exception). Its reason stands: lime has no sooty mold entry,
so the sentence tying its aphids to ant-tended honeydew exists nowhere in its record. NOT changed.

---

# FILED, NOT FIXED -- prose defects for a sourcing pass

1. **`katydids` `prevention_beginner` is about the WRONG ORGANISM.** It reads *"Caterpillar chewing
   rarely warrants intervention... If you spot a caterpillar on a small young tree, you can simply
   pick it off by hand"*, in an entry whose name and every other field are about katydids. It also
   reads in the seasoned register. Looks like a template leak. **It matters for control**: a
   caterpillar would legitimize a `bt` rung, a katydid would not. Do not add `bt` until this is
   adjudicated.
2. **`citrus-brown-rot` contradicts itself on the organism.** `symptoms_seasoned` says *"the fungus
   splashes up from the soil"* while `cause_seasoned` says *"Soil-borne Phytophthora species...
   water molds"*. This is the exact distinction used to justify minting `citrus-brown-rot` away from
   stone fruit's `brown-rot`, so the stray "fungus" should be corrected.
3. **The phytophthora mulch setback contradiction is on grapefruit too**, byte-identical in shape to
   lemon's: `prevention_seasoned` "a foot" vs `prevention_beginner` "a hand's width". Batch 18 filed
   this as a LEMON defect; it is a TEMPLATE defect and the fix must sweep all five citrus.
4. **`scale-insects` `prevention_beginner` on orange-navel drops half of what its seasoned register
   carries** (vigor and dust-rinsing), leaving the beginner reader ants and nursery inspection only.

# CATALOG GAPS -- the strongest mint/widen candidates this batch produced

1. **`horticultural_oil` cannot reach a fungal problem.** Four citrus records now recommend oil
   against **greasy spot** and none can carry it: `applies_to` is
   `[insect_soft_bodied, insect_general, mite]`. Three independent authors flagged it this batch;
   lime hit it in batch 18. Same SHAPE as the `ant_exclusion` blocker, which was fixed by adding a
   `disease_general` target. **Candidate: widen to `fungal_foliar`.** Needs a T1 read first.
2. **Skirt pruning has no method.** orange-navel's `citrus-brown-rot` calls it the leading control
   (*"Skirting and mulching remain the most reliable cultural controls"*) and only the mulching half
   is placeable. `ant_exclusion` includes skirt pruning but for ant bypass, a different purpose.
3. **`certified_clean_stock` is pathogen-scoped**, so "inspect incoming nursery stock for scale" is
   illegal on an insect problem. On grapefruit the advice is dropped from the crop entirely.
4. **Nutrient supplementation** still has no method (carried from batch 18). Not triggered on these
   three crops: only lemon carries a micronutrient entry.
