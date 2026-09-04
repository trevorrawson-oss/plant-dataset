# PLA-8 BATCH 25 (HERBS) -- RECORD / SOURCE PASS BRIEF

You are one of seven reviewers, one per crop. **You do not author ladders. You do not edit any file
in the repo.** You produce ONE markdown report. Another pass authors from it.

Canonical: `a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`. READ-ONLY.

## What this batch is

Seven herbs go through PLA-8 (the least-invasive-first IPM ladder). Before any ladder is authored,
the RECORD each ladder will be authored against has to be true and anchored. Batch 24 skipped
straight to authoring, then found 50 record defects and had to re-author 71% of the batch. This
pass exists so that does not happen again.

**61% of this batch's problem records (22 of 36) carry NO `sources` and NO `anchoring_urls` at all.**
Your crop's unsourced entries are named in your task. They are prose somebody wrote that no document
backs. Your job is to find out whether they are TRUE, and to anchor them.

## The rules that govern your reading

1. **Unsupported is not unsourceable. HUNT before you downgrade.** The last four times a claim in
   this dataset was flagged unsupported, all four were found at Tier 1 on a real hunt. Do not report
   "no source found" until you have tried the crop's own extension vocabulary (listed in your task),
   the obvious land-grant institutions for the crop's growing regions, and the specific
   pathogen/pest name once you have one.
2. **Locating the right document is NOT the same as supporting the claim.** Read the document and
   quote the sentence that carries the claim. A document that is about the right organism but never
   states the claim does NOT anchor it. Quote verbatim; do not paraphrase into support.
3. **Match the TAXON, not the common name.** A common name can be a different genus on a different
   host. When you name an organism, resolve it to a binomial and say which document gave you that
   binomial.
4. **Absence findings are document-scoped.** "No extension publishes X" is almost always false and
   usually means "the two documents I opened do not publish X." Say which documents you checked.
5. **A 403 is not a dead URL and a 200 is not a live one.** WAF challenge pages and text-less PDFs
   have been cached as successful reads before. If a fetch gives you no readable text, say so
   rather than treating it as an absence.
6. **Report what the document says, including when it contradicts the record.** A record claim you
   cannot support is a FINDING, not something to quietly soften.

## Source admission

Only sources in `tools/staging/pla8_batch25_herbs/source_catalog_admission.txt` are citable, by their
catalog key. The catalog is 219 entries, **all university-extension / government / .edu -- there are
NO journal entries**, so an APS or peer-reviewed-journal citation cannot currently be used as an
anchor even when it is the best evidence. If the ONLY support you find is a journal, report it as
`JOURNAL-ONLY` with full details and say so plainly -- that is a real and useful outcome, and it
becomes a catalog-addition decision rather than a silent gap. Prefer a T1 extension document that
carries the same claim.

Check the catalog before concluding a source "fails the tier bar" -- it may already be admitted.
Note the catalog key is `name`, not `title`.

## What to produce

Write ONE file: `tools/staging/pla8_batch25_herbs/record_<crop>.md`. Nothing else. For EVERY problem
entry on your crop (both `pests[]` and `diseases[]`), one section:

```
## <exact current `name`> [pests|diseases]  -- severity <x>, type <y>
STATUS: SOURCED-OK | SOURCED-WEAK | UNSOURCED-FOUND | UNSOURCED-NOT-FOUND | JOURNAL-ONLY | WRONG
ORGANISM: <binomial(s), or "umbrella -- multiple organisms", or "cannot be resolved">, per <doc>
ANCHORS: <catalog_key> <url> -- verified <date you fetched it>
  > verbatim quote carrying the claim
  > verbatim quote carrying the claim
RECORD CLAIMS THAT HOLD: <list, each with which anchor carries it>
RECORD CLAIMS WITH NO ANCHOR: <list, verbatim from the record>
RECORD CLAIMS THAT ARE WRONG: <list, with the document sentence that refutes it>
LADDER-RELEVANT FACTS the record does not carry: <things a control ladder would need>
```

Then a final `## SUMMARY` section: counts by STATUS, and the single most important finding.

**Be specific about the ladder-relevant facts.** The next pass builds a least-invasive-first ladder
(cultural -> physical -> soft chemical -> biological -> conventional). Facts that matter: what
overwinters where, what the infection/emergence timing is, whether resistant varieties exist,
whether a threshold or monitoring signal is published, what the source ACTUALLY recommends doing.

## Consumer-copy constraints (so you flag record prose that violates them)

No em dashes. American English. Temperatures render as `°F`. "plant" lowercase except sentence-start.
Everyday words over technical ones in consumer prose.
