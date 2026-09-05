# PLA-8 BATCH 26 (TREES AND SHRUBS) -- INDEPENDENT SOURCE-TRUTH REVIEW BRIEF

You review ONE crop's authored ladders against the documents. **You did not author them and you must
not defend them.** You write one report. You change no data file.

This pass exists because it is the one that has historically found the real defects. On batch 24 it
found 28 FIX items across 97 rungs, and none of them was a timing rule: the defects were finer than
the obvious ones, and every one was invisible to the promote's guards.

## What you are checking

For every rung on your crop, in `tools/staging/pla8_batch26_trees/out_<crop>.json`:

**Does the anchoring document actually say this?**

Fetch and READ the documents named in `record_<crop>.md` and in the entry's `anchoring_urls`. Do not
work from the record report's quotes alone -- the report is a previous agent's reading, and your job
is the independent one. Where the report quotes a sentence, confirm the sentence exists and that the
document is the one that carries it.

Grade every rung:

* **HOLDS** -- the document supports it, at the scope the note claims.
* **WRONG** -- the document says something different, or the opposite.
* **UNSUPPORTED** -- no document read says this. Distinguish from WRONG.
* **SYNTHESIS** -- true, but fuses two statements the document keeps separate, or infers a step.
* **STYLE** -- register, wording, consumer-copy rules.
* **FIT** -- true and sourced, but attached to the wrong method or the wrong rung.

## The defect classes this batch is most likely to carry

Batch 24's and 25's reviewers found the coarse rules all held and the FINE ones failed. Look there:

1. **A method aimed at the wrong life stage.** Batch 24 shipped a spinosad note timed to "adults
   laying" when the method reaches the larva. If a note gives timing, check the timing is the one
   that makes that method work.
2. **A claim narrowed or widened against its record.** "Drainage is the stress" when the record lists
   drainage AND stress separately. "The one part you can still fix" excluding a claim the record
   makes.
3. **An unsourced mechanism smuggled in as a reason.** The practice can be right while the REASON is
   invented, and the reason is what a reader learns. Thyme's aphid entry did exactly this: lean soil
   is right, "vigorous enough to shrug off aphids" inverts why.
4. **Region-scoped advice presented as universal.** `rhs` is UK. Its pesticide-availability and
   product statements are UK product law and must not appear as facts about a US reader's options.
   UC IPM AGRICULTURE pages are commercial: per-acre rates and postharvest thresholds are not home
   advice.
5. **A number with no warrant.** Every °F figure, every interval, every threshold must be in a
   document. Batch 24's leek agent correctly REFUSED a figure its brief supplied because the record
   said something else. That was the right call.
6. **A commercial-orchard practice presented as home advice.** WSU tree fruit and UC IPM
   AGRICULTURE pages are the anchors for pear psylla, codling moth, leaffooted bug and black heart.
   Per-acre rates, degree-day spray timing without a home-scale signal, and postharvest standards
   are not home advice. The BIOLOGY from those pages is usable; the PROGRAM is not.
7. **A title read as a sentence.** NC State Toolbox `Insects:`/`Diseases:` rows are factsheet
   titles. A rung anchored to one of those rows has no document behind it.

## Check the corrections too, not just the ladders

Each entry may carry `field_corrections`: prose the batch is changing, each with a `why` and an
`anchor`. **Verify the anchor carries the replacement text.** A correction that swaps one unsourced
sentence for another unsourced sentence is not a correction. Grade these the same way.

Also confirm the correction was NEEDED: if the original prose was fine and the replacement is merely
different, say so.

## Check what is missing

A ladder can be wrong by omission. If the documents support a cheap early step the ladder skips, say
so. If the ladder reaches a chemical tier the sources do not justify, say so -- **a short ladder is
correct when the evidence is short**, and padding is a defect.

Ladder caps and holds this batch inherited from documents, which you should verify are honored:
* **PLA-457 HOLD.** `control_methods.horticultural_oil` states a sulfur/oil interval that disagrees
  with its own anchor (UC IPM PN 7405 says 30 days, PN 7406 two weeks, PN 7408 three weeks); a
  roster-wide ruling is pending. A rung in this batch may recommend horticultural oil, and may
  recommend sulfur, but **no rung may state a sulfur/oil spacing interval in prose**. If one does,
  that is a FIX item regardless of which figure it gives. If the authoring agent filed a hold note
  instead, confirm the note names the document and the figure it declined to write.
* **Borers inside wood** (persimmon borer, mulberry borers, pawpaw peduncle borer): the documents
  say no spray reaches larvae already inside. A ladder that offers a spray rung against the larva
  is WRONG unless a document times a spray to the egg-laying or crawler stage and the note says so.
* **Zebra swallowtail** (pawpaw): the sources say do not control it. Any rung beyond leaving it
  alone is padding.
* **Pear decline**: no cure; the ladder is vector control and rootstock. A rung promising to treat
  the phytoplasma is WRONG.
* **Trees the record says have no effective home spray** (Alternaria black heart, popcorn disease,
  root and crown rot): the ladder should say so and stop at sanitation/siting, not reach for a
  chemical tier because it exists.
* **Split limbs** (pomegranate's mealybugs and scale, any other split the pin table records) carry
  FULL re-authored prose in `field_corrections`; grade every field, and check that each limb's
  prose describes only ITS organism.

## Output

Write `tools/staging/pla8_batch26_trees/review_<crop>.md`:

* One section per problem entry, one line per rung, with the grade and the evidence.
* For every FIX item: the exact text, what is wrong, and the document sentence that settles it.
* A `## SUMMARY` with counts by grade, and the single most important finding.
* A `## RECORD-LEVEL FINDINGS` section for anything that is a problem with the RECORD rather than the
  rung. Those are filed for a later pass, not fixed now.

Be specific and quote verbatim. "Seems fine" is not a review. If everything on a rung holds, say so
and name the sentence that carries it.
