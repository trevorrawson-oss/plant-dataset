# Batch 23 (roots) -- findings for the r10 catalog queue and the open list

## 1. NEW, and the strongest catalog signal this batch: `certified_clean_stock` cannot reach an insect

`applies_to = [viral, bacterial, fungal_foliar, fungal_soilborne, disease_general, nematode]`.
No `insect_*` member, so it is **illegal on any insect-typed problem**. Measured live: it appears on
**86 problems -- 50 fungal, 29 bacterial, 6 viral, 1 nematode, ZERO insect.**

Two of the three agents reported this independently, which is the playbook's own trigger: "If
several bots independently report the same control blocked, that is the catalog, not the authors."

It blocks the single most emphasized instruction on **three** problems in this batch:
* `sweet-potato-weevil` -- the record says "Certified slips plus sanitation carry nearly all of the
  control." Roughly half the stated program is unexpressible; the ladder opens on sanitation instead.
* `whiteflies-virus-vectors` -- "start with certified, virus-tested slips" is the entry's leading
  advice and its stated reason for existing.
* `aphids-virus-vectors` (potato) -- "the reason gardeners are advised to start from certified seed
  potatoes rather than saved tubers."

**The asymmetry is the argument.** The identical instruction ("do not save slips from a patch that
showed wilt") IS placeable on `fusarium-wilt` purely because that problem is typed fungal. Whether
you can say "buy clean planting material" currently depends on the pathogen's kingdom, but the
decision is a property of the PLANTING MATERIAL, not of the organism.

Apply the playbook's test -- *does the method's own PROSE describe the action this crop needs?* It
does: **"Problems that travel in the planting material itself"** is the head clause, and a weevil
riding in an infested slip is exactly that. The pathogen list that follows is enumeration, not scope.

**This is a widening candidate, not a mint.** It was NOT acted on: minting or widening mid-batch is
the batch-1 defect (authored against 37 methods that became 43 underneath it).

## 2. Confirms an existing r10 queue item with a second crop: in-season mounding

r8 deferred mounding after reading split it into three mechanisms, and recorded that **the barrier
reading had no document**. Parsnip supplies a second crop for the THIRD mechanism (covering a crown
against a canker fungus): itersonilia prevention says to hill soil over the shoulders, and the
entry's cause names exposed shoulders as the entry point. `moisture_buffering_mulch` is
physiological-only and the wrong action; `splash_barrier_mulch` is laid at planting, not drawn up
mid-season. Potato adds its own mounding instruction. **Still unplaced, still owed a document.**

## 3. NEW: `off_season_tillage` cannot reach a fungal problem, and `garden_sanitation`'s caution CONTRADICTS the source

Parsnip's canker prevention says to **bury** old parsnip residue by deep cultivation to lower
inoculum. The right ACTION is `off_season_tillage`, whose `applies_to` is
`[insect_chewing, insect_general]` -- illegal on a fungal problem. The only legal alternative,
`garden_sanitation`, carries a CAUTION that says the opposite: *"Destroy diseased debris rather than
leaving or burying it."* The agent authored only the "clear the tops off the bed" half and wrote
neither "bury" nor "destroy rather than bury", so the shipped rung neither invents nor contradicts.
Two possible fixes: widen `off_season_tillage` to `fungal_soilborne`/`disease_general`, or soften
the sanitation caution where an extension source specifies deep burial.

## 4. Extends an existing r10 item: `weed_host_control` reach

Already queued as "cannot reach `viral` or `nematode`". Roots adds **`bacterial`**: parsnip's
aster-yellows names dandelion and broadleaf weeds harboring the phytoplasma, and the rung had to be
placed on the leafhopper (insect) entry instead. Carrot's shipped ladder hit the same wall.
Separately, its reach INTO insects is too lax in the other direction: it admits any insect type via
`insect_soft_bodied`, which is how a hard-bodied wireworm larva takes it legally.

## 5. Confirms an existing r10 item: plant vigor / tolerance has no method

Reported by potato twice ("vigorous, evenly watered plants are far more tolerant"; "keep plants
vigorous with steady water and feeding") and sweet-potato once ("healthy, well-watered transplants
usually outgrow flea beetle feeding" -- the FIRST line of that entry's organic treatment).
`even_watering` is illegal for insect and means calcium disorders; `balance_nitrogen` is legal for
fungal but means the OPPOSITE move (restrain nitrogen), so using it would invert the advice.

## 6. `prompt_harvest`'s MEANS text is now out of date

Written entirely around fruit ("over-ripe or fallen fruit ... birds and squirrels take ripe fruit",
and `how_it_works_beginner` is fruit-only: "Pick fruit as it ripens instead of letting it hang").
**Counted, not estimated: this batch adds 5 root-lifting rungs** (parsnip/`carrot-rust-fly`,
parsnip/`itersonilia-canker`, potato/`wireworms`, sweet-potato/`sweet-potato-weevil`,
sweet-potato/`wireworms-root-feeding-larvae`) **to 3 already shipped** (carrot x2, radish x1) --
**8 total.** An earlier draft of this file said "at least four", an undercount by half, and the read
record said "x4" for a batch shipping 5. The distinguishing clause still governs correctly; the
MEANS and `how_it_works_*` text should name root lifting.

Same shape, not previously raised: **`off_season_tillage.how_it_works_*` is written entirely around
pupal cells of soil-pupating Lepidoptera** (hornworm, corn borer). It now carries wireworm rungs on
potato and sweet-potato -- click beetle larvae that persist several years and do not fit that text
at all. The ACTION is in both crops' prose, so the rungs are sourced; the method's rendered
explanation is what is wrong.

## 7. Other unplaced instructions, recorded not forced

potato: "never plant near tomatoes" (no method covers host proximity); "avoid fresh manure" on scab
(no amendment-restraint method; `lower_soil_ph` is specifically lime/wood-ash restraint); "plant into
warm soil" for blackleg; seed-piece suberization (known gap, and correctly NOT folded into
`cure_and_store`, which is post-harvest); trimming tunneled tubers to use first (this is literally
`cure_and_store`'s caution, illegal on an insect type). sweet-potato: soil organic matter / compost
on root-knot; tool-and-bin hygiene (the bin half went into `cure_and_store`, the tool half is the
known "soil on tools or shoes" gap -- note there IS roster precedent for forcing it, at
sugar-snap-peas/`fusarium-wilt`/`garden_sanitation`).

## 8. Pre-existing prose defects found while reading. NOT fixed, not this batch's scope.

1. **parsnip canker, both registers**: "the fungus *Itersonilia perplexans*, also called black
   canker". Black canker names the DISEASE, not the fungus. In both registers, so it is a copy
   defect rather than a slip.
2. ~~**sweet-potato has no curing or storage FIGURES anywhere.**~~ **[RETRACTED 2026-09-01 -- THIS
   FINDING WAS FALSE.]** The claim was true only of the two DISEASE entries; the headline said
   "anywhere", and the independent source-truth pass refuted it at six sites in the live record:
   `storage.notes_seasoned`/`notes_beginner` (cure at 80 to 85°F and 85 to 90 percent humidity for
   1 to 2 weeks, 5 to 7 days minimum, then hold at 55 to 60°F), `storage.room_temp_*`,
   `storage.fridge_*` (below about 50 to 55°F is chilling injury), `tips_by_stage.harvest`,
   `failure_diagnostics` and `notifications`. **There is no sourcing gap.** The rungs' instruction to
   take conditions from sweet potato's own guidance resolves correctly.

   This is the "a stale record commissions phantom work" pattern, authored fresh rather than
   inherited: filed as written it would have sent a later session hunting for figures the record
   already holds. Worse, it asserted the absence of the very data that proved a REAL defect --
   see item 18.
3. **sweet-potato flea beetle entry makes a root claim it never treats.** Both `symptoms_*` and
   `cause_*` say the larvae scar developing storage roots; every line of treatment and prevention
   addresses foliage. The root controls exist one entry over, under
   `wireworms-root-feeding-larvae`. Worth a cross-reference.
4. **parsnip's aster-leafhopper `organic_treatment_*` contains no treatment for the insect** -- both
   registers describe managing the disease. Defensible IPM, but it renders adjacent to the
   near-identical aster-yellows entry.
5. **Live `never` absolutes in shipped consumer prose**: potato ("never lime a potato bed", "never
   plant near tomatoes"), sweet-potato x4. These are SOURCE fields and the roots handoff section 4
   already scoped the absolutes campaign OUT after measuring; recorded only so the count is honest.
   None reached a rung.
6. potato late blight carries no rotation instruction while early blight does. Consistent with the
   biology (airborne arrival) and with the tomato precedent, so no rung was added. Noted because a
   reviewer scanning for parallelism will expect one.

---

# Found while BUILDING the promote and its suite (not by the authoring pass)

## 9. My own pre-authoring id scan had the defect it was built to prevent

The stemmed token-subset scan I ran before fan-out used a stemmer that stripped `es`, so `beetles`
became `beetl` while `beetle` stayed `beetle`. **The two did not compare equal**, and the scan
therefore reported ZERO stem-equal variants facing this batch. The real answer is TWO: swiss-chard's
singular `flea-beetle` against the `flea-beetles` this batch takes on potato and sweet-potato.

I only knew about that pair because the roots handoff lists it in section 6. **The scan built to
replace that prior knowledge would not have found it.** This is the batch 22 lesson recurring one
batch later in a subtler form: batch 22 learned that an EQUALITY check passes an id that merely
resembles a live one, and this batch learned that a STEMMED check does too if the stemmer is wrong.

Caught by a suite driver, not by reading. The fix strips a trailing plural `s` instead, keeping the
singular as the shared key, and `test_stemmer_matches_singular_and_plural` pins it. Re-running the
corrected scan over all 22 ids against all 216 live ids returns exactly the 2 known pairs and keeps
every intended distinction (`aphids` vs `aphids-virus-vectors`, `black-rot` vs
`sweet-potato-black-rot`, `damping-off` vs `root-rots-damping-off`, and so on).

The guard was also reshaped by this. Its first form asked "is a MINTED id stem-equal to a live one",
which skipped `flea-beetles` because that id is itself live. The real question is: **where the
roster holds two stem-equal variants of one name, which one does the batch take, and was that
decided or typed?** `STEM_VARIANT_PINS` now records the adjudication, and
`test_removing_the_pin_refuses_the_shipped_batch` proves the pin is load-bearing.

## 10. The prose-echo guard caught two real echoes, and one of them the similarity guard missed

`check_no_shipped_prose_echo` refused the batch twice on its first runs:

1. `potato/aphids-virus-vectors/water_spray` carried "Do it early in the day so the leaves dry
   quickly.", byte-identical to `cherry-tomato/spider-mites/water_spray`.
2. `potato/common-scab/even_watering` carried "Dry soil at that stage is what lets scab get its hold
   on the skins.", byte-identical to **`beet/common-scab/even_watering` -- the same problem id and
   the same method**, which is precisely the precedent-copy vector this batch created.

**Item 2 is the important one, because `check_no_precedent_copy` scored that exact pair 0.508 and
passed it.** A single copied sentence inside an otherwise independently written note does not move a
whole-note similarity ratio above 0.70. The two guards are complementary and neither subsumes the
other: the similarity guard sees wholesale copying, the echo guard sees sentence-level lifting.
Keeping both is the finding; treating the new guard as a replacement would have shipped item 2.

Both were reworded, meaning preserved. Max precedent similarity across the batch fell from 0.508 to
0.483 as a result. A full scan of the corrected batch against a 5,637-note / 9,382-sentence shipped
corpus now returns zero echoes.

## 11. Internal ladder vocabulary: 9 in this batch, and a MEASURED legacy population of 130

`check_no_ladder_vocabulary` refused on nine rungs whose seasoned register used "rung" or "ladder"
in consumer-facing copy ("the workhorse rung", "the highest-leverage rung on this ladder", "the
cultural rungs carry the real defense"). All nine were reworded to "step", "control", "decision",
which is already the roster's ordinary vocabulary (267 shipped rungs use "step").

Measuring before accepting the scope, as the standard requires: **130 shipped rungs across 50 crops
already carry this vocabulary**, led by honeydew-melon (10), artichoke (9), watermelon (8),
cantaloupe (8). But batch 22's three crops carry **zero**, and so do beet, fig, strawberry, viola.
So the guard IS enforced from batch 21/22 onward and the 130 are legacy from before it existed.
Complying was therefore the right call rather than dropping a guard the roster does not honor.

**The 130 are a real, bounded cleanup candidate** -- a mechanical find, a hand rewrite per rung, and
no sourcing work. Filed, not fixed; it is not this batch's job.

## 12. Two guards had to be lifted out of `main()` to be testable

`main()` held the control_methods and source_catalog immutability checks inline, where no suite
driver could reach them: mutating either would have SURVIVED the harness and been reported as a
permanent gap. They are now `check_catalog_untouched()`, driven directly, plus an end-to-end
subprocess driver for the base-SHA refusal and for `main()` itself on the real canonical. A guard
that exists only inside an entry point the suite never calls is untested code wearing a guard's
clothes, and padding a harness total with it as a "forward assertion" would have been the wrong
close.

---

# Found by the INDEPENDENT SOURCE-TRUTH PASS, after every gate and the mutation harness were green

The batch was gate-clean (`gate_all` 121/121), suite-green (82 tests) and mutation-clean (64/64,
zero survivors) when this pass ran. **It found eleven defects anyway, one of them in the guard this
batch was built around.** That is the argument for keeping the independent pass: none of these are
findable by a gate, and three were invisible to the very check written to catch them.

## 18. THE GUARD WAS MEASURING THE WRONG THING, and it hid the one copy in the batch

`check_no_precedent_copy` used `difflib.SequenceMatcher` with **default arguments** and averaged the
two registers. Both halves were wrong:

* **`autojunk`.** difflib's autojunk heuristic engages on sequences of 200 characters or more and
  treats any character appearing in over 1% of the sequence as junk. **That describes every seasoned
  register in the dataset**, so the guard was deflating precisely the strings it exists to compare.
* **Mean of registers.** Averaging dilutes one copied register against one independent one.

Measured on the real case, `potato`/`common-scab`/`even_watering` against `beet`'s rung for the same
problem and the same method:

| metric | beginner | seasoned | reported |
|---|---|---|---|
| defaults + mean (what shipped) | 0.509 | 0.353 | **0.431 -- "independent"** |
| autojunk=False, per-register max | 0.509 | **0.757** | **0.757 -- REFUSED** |

It is a copy. The two seasoned registers shared a **56-character verbatim run** ("the half still
available once the crop is in the ground") plus "is the in-season half of scab control" and "the pH
decision ... before planting; this one is made every week". beet's ladder was written earlier in the
SAME session, which is why it was the closest pair on the roster.

**The guard was reachable, non-vacuous, mutation-tested and wrong.** Every property the PLA-215 bar
checks was satisfied; none of them asks whether the metric measures what the guard claims. The
harness proved the guard FIRES; it cannot prove the guard SEES.

Corrected: `autojunk=False`, **per-register max**, threshold unchanged at 0.70. Recalibrated on the
same peer population under the corrected metric: **62 singleton-vs-singleton pairs, per-register
ceiling 0.684** (apple vs strawberry on `powdery-mildew`/`sulfur`), median 0.409, nothing legitimate
at or above 0.70. The batch after rewriting tops out at **0.660**. `test_metric_is_autojunk_free_and_
per_register` pins the regression with the real pair.

The published figures in the read record were also stale (0.508 was the pre-echo-fix maximum) and
are corrected there.

## 19. A rung contradicted its own crop's storage data

`sweet-potato`/`scurf-storage-soft-rot`/`cure_and_store` said to hold the cured crop **"warm and
dry"**. "Dry" is in neither the problem's prose (which says "store warm, never cold or wet") nor the
crop's storage block, and it **contradicts** it: sweet potato cures at **85 to 90 percent humidity**
and stores at 55 to 60°F with ventilation. Low-humidity storage produces exactly the "moisture loss
and shrinkage" this same problem lists as a symptom. Fixed to "warm rather than cold ... chilling
and wet". The beginner register's "cold or damp" was aligned to the source's "wet".

**This is the defect item 2 asserted could not exist.** The retracted finding claimed the crop held
no storage data; the crop's storage data is what proves this rung wrong.

## 20. Safety text softened, and safety text asymmetric between two crops in one batch

* **Copper hazard band weakened on BOTH potato rungs, in the beginner register.** Rungs said
  "copper is toxic to fish"; the catalog caution says "**highly to very highly** toxic to fish
  **and aquatic life**". Two terms weakened, in the register most likely to be acted on. Restored.
* **`insecticidal_soap` shipped different safety information on two crops.** potato's rung carried
  UC IPM's moderate acute rating for potassium salts of fatty acids and the PPE instruction;
  sweet-potato's carried neither, though both use the same method against the same kind of pest.
  Added for parity. **The rating itself was verified NOT fabricated and NOT upgraded** -- same
  ingredient, same band, same use context as the catalog -- which was the single highest-risk item
  going in, given a neem bee-safety rating was invented in three fields in an earlier batch.

## 21. Four hedges and ceilings lost in compression

The standard names this as the INVERSE defect with no term to scan for. Four instances, all fixed:

1. `potato`/`colorado-potato-beetle`/`handpick`: source "tolerate **up to about** 30 percent
   defoliation ... but **only about** 10 percent" became "**roughly** 30 percent ... **closer to**
   10 percent". Two upper bounds became point estimates, and 30% came to read as a target.
2. `parsnip`/`parsnip-leafminer`/`garden_sanitation`: source "sprays are **largely ineffective**"
   became the mechanical assertion "a contact spray **does not reach** a feeder ...".
3. `parsnip`/`damping-off`/`garden_sanitation`: source "stop watering **for a bit**" / "let the
   surface dry **somewhat**" became "cutting the water back **for a few days**" -- an invented
   duration and a dropped hedge in one clause.
4. `parsnip`/`damping-off`/`sound_sowing_practice`: "the bed has to be held damp **for weeks**"
   introduced a week-scale quantity the crop's prose does not give (it says only that germination
   is long).

**One reported hedge defect was REFUTED and NOT applied.** The review flagged `beneficial_predators`
on both crops for upgrading "often" to "usually". The sources are register-split: the BEGINNER prose
on both crops says "helpers **usually** keep them in check" and the SEASONED says "beneficial
insects **often** control them". Both rungs are beginner-register and say "usually", matching their
own register's source. The review compared a beginner rung against the seasoned source.

## 22. Two catalog cautions narrowed or dropped in a rung

* `sweet-potato`/`flea-beetles`/`floating_row_cover` said "ground that carried the **same crop**
  last season"; the caution says "the **same-family** crop grew last year". Potato's two row-cover
  rungs and parsnip's all say "family" correctly; only this one narrowed it. Fixed.
* `sweet-potato`/`wireworms-root-feeding-larvae`/`off_season_tillage` omitted the no-dig /
  soil-structure caution that potato's parallel rung carries twice. Added.

## 23. Filed, NOT fixed -- these need adjudication rather than an edit

1. **A pH figure disagreement between two records citing the SAME document.** potato/`common-scab`
   prose says "around **pH 5.0 to 5.3**"; the `lower_soil_ph` catalog entry says "Clemson puts the
   potato target at **pH 5.0 to 5.2**". Both cite `clemson_hgic`, same URL. The rung restated the
   crop's prose, which is what the rule requires, so the rung is compliant and one of the two
   records is wrong about a document they share.
2. **`parsnip-leafminer` may become a duplicate join key.** Parsnip's prose names no genus, so the
   crop-scoped mint was the conservative call. If the miner is later resolved to *Liriomyza*, the
   roster will hold two pinned ids for one taxon (`celery-leafminer` is *Liriomyza* spp.); if it
   resolves to *Euleia heraclei*, the separate id is right.
3. **The three `certified_clean_stock` ladders still omit their crops' leading advice** (item 1).
   A mitigating clause inside a neighbouring rung's note was considered and NOT written: it would
   make the note describe something other than its own method, which is the defect the authoring
   discipline exists to prevent. The r10 widening plus a thin-ladder backfill is the clean fix, and
   that is the agreed sequence.
