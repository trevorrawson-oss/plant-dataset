# PLA-8 BATCH 22 (stragglers) -- HANDOFF: authored, NOT merged, NOT committed

> **SUPERSEDED 2026-09-01 -- DO NOT ACT ON THIS FILE.** Batch 22 is merged, read, promoted
> and gauntleted; canonical is now `919eabc4`, not `fabdaae1`. Everything in
> section 2 ("What remains") is DONE, and sections 3-6 have been superseded by measurement:
> the pumpkin "template defect" in section 4 was NOT a defect, and section 6's "three
> singular/plural repoints" is four. Read
> `docs/2026-09-01-pla8-batch22-outcome-and-carryforward.md` instead. Kept for the record of
> what was known before the read.

**Written 2026-09-01 at the end of a long session. Read this before touching batch 22.**

Canonical is `fabdaae1` (batch 21, flowers). Working tree clean, `main` in sync with origin.
**Verify first:** `shasum -a 256 crops_data_final.json` must read
`fabdaae1d3c35d54ccc49704253b5eb4e191700897786c1ec761e340166b5cb6`.

---

## 1. State

| item | state |
|---|---|
| batches 18, 19, 20, 21 | committed **and pushed** (`f4355e3`/`e3779dc`, `9e8151e`/`3c4e8ac`, `8a31d66`/`0920c70`, `333c623`/`27a9f87`) |
| roster | **91 / 121 laddered** |
| batch 22 | **authored only.** 3 `out_*.json` in `tools/staging/pla8_batch22_stragglers/`, **not merged, not read, not committed** (the whole directory is untracked) |

Authored: english-cucumber 9 problems / 50 rungs, edamame 9 / 43, pumpkin 8 / 42.
**26 problems, 135 rungs.**

## 2. What remains

1. `python3 tools/ladder_batch.py merge --out tools/staging/pla8_batch22_stragglers`
2. **Verify all 26 ids against `PINNED_IDS.md` programmatically** (merge cannot do it: it reports
   `ids reused 0` because the pre-state problems carry no id).
3. `python3 tools/ladder_batch.py verify --out ...`, then READ (section 4 below is the read list).
4. Promote + suite + harness, using batch 21's as the template but **re-measuring the premise**
   (section 3). Then apply, gauntlet, state trio, commit, push, `COMMIT_FOR`.

## 3. THE PREMISE IS DIFFERENT FROM BATCH 21. MEASURE IT, DO NOT INHERIT IT.

**Schema: FULL** (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`, `sources`,
`anchoring_urls`) -- the batch 17-20 shape. Batch 21 was NOTE-schema. Copying batch 21's
`check_note_schema_premise` would refuse this batch outright.

**Type: SPLIT BY CROP, a fifth distinct situation in six batches.**

| crop | pre-state |
|---|---|
| english-cucumber | all `None` (9) -- set from nothing |
| pumpkin | all `None` (8) -- set from nothing |
| edamame | **all COARSE** (`pest` x5, `disease` x4) -- upgrade |

Batch 17 all-coarse, 18 mixed, 19 all-fine, 20/21 all-none, 22 split-by-crop. **The type field is
genuinely heterogeneous. Measure every batch.**

**Divergence guard: re-measure before choosing a shape.** Batch 20 needed narrow-vs-broad; batch 21
needed no shape comparison at all (9 of 20 reused-id instances matched a shipped ladder, correctly)
and used a prose-echo scan instead. All three straggler crops have laddered siblings, so this batch's
answer is probably different again.

## 4. THE THREE AUTHORING REPORTS -- captured here because they exist nowhere else

### english-cucumber (protected-culture crop; 50 rungs)

* **All five ladders overlapping a cucumber sibling DIFFER, each traceable to its own record.**
  `aphids` +`augmentative_release` (its record says "conserve **or release**" under cover);
  `cucumber-beetles` -`resistant_varieties` (the non-bitter-cultivar fact is absent from its record;
  it carries a different fact instead, that pollinator exclusion on parthenocarpic types also
  excludes the beetle and the wilt it vectors); `powdery-mildew` +`balance_nitrogen`;
  `downy-mildew` +`wet_foliage_discipline` and **-`chlorothalonil`** (its record names copper and
  stops); spider mites +`augmentative_release` (*Phytoseiulus persimilis* named).
* **Biggest gap: humidity/venting under cover has NO method.** It is the most-repeated instruction in
  the record (5 problems) and `airflow_spacing` is a different action (layout set at planting).
* **Three of four powdery-mildew materials unplaceable**: potassium bicarbonate is not in the catalog
  at all; `neem_oil` and `horticultural_oil` are insect/mite-scoped and illegal on fungal.
* `weed_host_control` is illegal on `viral`, so CMV's weed-reservoir advice has no home -- **and an
  aphid-vectored virus is the textbook case for that method.**
* Prose defects: powdery mildew's beginner register names a cultivar the seasoned one does not
  (backwards); its beginner says "water at the base" while `cause_seasoned` says the fungus does not
  need leaf wetness; downy mildew has a flat "never" in one register only. `uf_ifas` CV268 is the
  sole source for four of nine problems; `csu_ext` is a program landing page anchoring three.

### edamame (the coarse-upgrade crop; 43 rungs)

* Fine types assigned with the organism that drove each; SCN is `nematode` and sits in `diseases`,
  which matches existing roster practice.
* Differences from the laddered legumes are all record-driven: `two-spotted-spider-mite`
  +`horticultural_oil`; `bean-leaf-beetle` +`planting_time_avoidance` +`spinosad` (its record makes
  **pod feeding**, not seedling girdling, the costly injury); `white-mold` +`crop_rotation`.
* **A banned absolute is live in shipped consumer prose**: SCN `prevention_beginner` says
  "**never** grow soybeans in the same spot every year", while its seasoned register hedges the same
  instruction. Not carried into any rung. **This is a content defect to fix, and existing prose is
  not scanned for absolutes by any gate.**
* **Two source keys each name TWO different documents** (verified): `iastate_ext` -> a home-garden
  "all about beans" article on the 5 pests and a soybean-diseases page on the 4 diseases; `mu_ext` ->
  publication G7150 on bean leaf beetle and an "edamame, an easy crop to introduce" news piece on
  three others. The news piece is thin support for *Sclerotinia* persistence and *Pseudomonas*
  seedborne carryover.
* Its downy mildew is a **warm**-weather disease while every sibling downy-mildew record frames it as
  cool -- probably correct biology for soybean, worth a source-truth confirm.
* Gaps: lawn/grub management (no method); `weed_host_control` illegal on `nematode`; "do not move
  soil on tools or shoes" (no method).

### pumpkin (42 rungs)

* **`bacterial-wilt` CONFIRMED correct**: its record states the beetle-gut mechanism in both
  registers and makes no soil-persistence claim, which is exactly the tell separating it from
  nasturtium's *Ralstonia*. The id that was a trap in batch 21 is the right reuse here.
* `squash-vine-borer` differs most from the squash siblings (7 rungs vs 4): its record alone carries
  early planting/flight timing and late-winter tillage, and names no collar.
* **A TEMPLATE DEFECT, verified**: the three cucumbers' downy-mildew treatment reads "apply a labeled
  fungicide **such as copper or chlorothalonil**, covering leaf undersides"; pumpkin's is
  byte-identical **with the product list removed**. So pumpkin's ladder honestly carries no spray rung
  while its siblings do. Adjudicate whether the products were lost or UGA C1206 names none.
* **`horticultural_oil` cannot reach `fungal` -- a THIRD batch reporting it** (citrus greasy spot,
  berry records, now pumpkin powdery mildew). With "general plant vigor" this is the best-evidenced
  catalog gap on the board.
* Gaps: preventive vine-burying at the joints (no method); "keep young plants vigorous"; a board
  under ripening fruit (`straw_mulch` covers the mulch half only).
* `umn_ext` points at three different URLs across the record (each problem's own anchor is correct,
  but the key is not stable).

## 5. READ THIS BEFORE WRITING ANY BRIEF -- the method that failed, and the fix

**Six factual errors in my briefs and pin tables across batches 21 and 22.** Every one was a claim
ASSERTED from a scan shortcut or memory; every COMPUTED claim was right. Two authoring agents caught
two of them, an audit caught the rest, and **one (`cutworm` singular) would have shipped a wrong join
key**, because the guard that refuses it did not exist until the error was found.

**Three rules, now written into both pin tables:**

1. **Never collapse a problem name to one id.** Eight roster names carry more than one id; a
   `sorted(ids)[0]` display hides the rest. That is how `southern-bacterial-wilt` (which already
   existed on eggplant) was mistaken for a needed mint.
2. **Check every intended MINT against the roster BY ID**, not by problem name. A name scan cannot
   see an id whose holder names the problem differently. This turned six "new" problems into reuses
   across two batches.
3. **Compute every roster-wide claim before putting it in a brief.** Both wrong claims in batch 22's
   briefs ("stink-bugs is on the legumes"; "7 of 9 shared ids" -- it is 4) were assertions the agents
   had to correct.

## 6. Filed, NOT fixed (carried across recent batches)

1. **Three singular/plural id repoints** would retire a defect class: asparagus `cutworm`,
   swiss-chard `flea-beetle`, basil `japanese-beetle`. Each is one token; each is the lone holder of
   a singular whose plural has 8, 31 and 6 holders. **Batch 21's
   `check_singular_variants_not_taken` refuses once they are repaired, so retire that guard in the
   same change.**
2. **viola's own note recommends Bt on a butterfly host**, contradicting the catalog's caution. The
   ladder already omits it; the note is what should change.
3. **Mis-pointed source keys are a measured class** (batches 17, 18, 20, and edamame above). Shape: a
   crop's problems share ONE source id whose URL is specific to ONE of them. Mechanically detectable;
   the scan is worth building and has not been.
4. **Catalog gaps, best-evidenced first**: general plant vigor (four berry authors + citrus + edamame
   + pumpkin); `horticultural_oil` unable to reach `fungal` (three batches); burying overwintering
   inoculum (and `garden_sanitation`'s caution contradicts it); dormant lime sulfur; humidity/venting
   under cover; watering QUANTITY (three batches); soil pH.
5. **The oil temperature ruling from batch 18 was OVERTURNED** by reading (batch 19 outcome doc §8).
   The crops' 95°F is correctly sourced; the catalog's 90°F comes from the spider-mite pest note; the
   real citrus limit is regional. Specified but not actioned.

## 7. After batch 22

Roster goes to **94 / 121**. Remaining **7 batches**: roots (parsnip/potato/sweet-potato, 22),
woody herbs (25), other trees (24), alliums (19), soft herbs (19), pome fruit (15), microgreens (14,
**LAST** per standing ruling). Trevor asked for roots next.
