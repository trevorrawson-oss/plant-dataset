# PLA-8 BATCH 25 (HERBS) -- INDEPENDENT SOURCE-TRUTH REVIEW BRIEF

You review ONE crop's authored ladders against the documents. **You did not author them and you must
not defend them.** You write one report. You change no data file.

This pass exists because it is the one that has historically found the real defects. On batch 24 it
found 28 FIX items across 97 rungs, and none of them was a timing rule: the defects were finer than
the obvious ones, and every one was invisible to the promote's guards.

## What you are checking

For every rung on your crop, in `tools/staging/pla8_batch25_herbs/out_<crop>.json`:

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

Batch 24's reviewers found the coarse rules all held and the FINE ones failed. Look there:

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
6. **Powdery mildew leaf-wetness advice.** This batch corrects four crops on it. UC IPM Pub 7493:
   "all powdery mildew species can germinate and infect without water on the plant's surface";
   "Water on plant surfaces for extended periods INHIBITS spore germination". If any powdery-mildew
   rung on your crop still says to keep foliage dry or avoid overhead watering AS A MILDEW CONTROL,
   that is WRONG and the batch is supposed to have fixed it.

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

Two ladder caps this batch inherited from documents, which you should verify are honored:
* **Spittlebugs (lavender, rosemary, sage):** UMN says "Pesticides are not effective." No chemical
  rung belongs on those ladders.
* **Slugs (sage):** with `type: mollusk` only 8 methods are legal, and `airflow_spacing` is not one
  of them.

## Output

Write `tools/staging/pla8_batch25_herbs/review_<crop>.md`:

* One section per problem entry, one line per rung, with the grade and the evidence.
* For every FIX item: the exact text, what is wrong, and the document sentence that settles it.
* A `## SUMMARY` with counts by grade, and the single most important finding.
* A `## RECORD-LEVEL FINDINGS` section for anything that is a problem with the RECORD rather than the
  rung. Those are filed for a later pass, not fixed now.

Be specific and quote verbatim. "Seems fine" is not a review. If everything on a rung holds, say so
and name the sentence that carries it.
