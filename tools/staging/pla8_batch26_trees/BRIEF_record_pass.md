# PLA-8 BATCH 26 (TREES AND SHRUBS) -- RECORD / SOURCE PASS BRIEF

You are one of six reviewers, one per crop. **You do not author ladders. You do not edit any file
in the repo except the ONE report you write.** Another pass authors from your report.

Canonical: `ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144`. READ-ONLY.
Your crop's current problem entries are in `tools/staging/pla8_batch26_trees/records_problems.json`
(and the whole crop record, for context, in `<crop>_source.json` beside it).

## What this batch is

Six perennial trees and shrubs go through PLA-8 (the least-invasive-first IPM ladder): mulberry,
pawpaw, pear-asian, pear-european, persimmon, pomegranate. Before any ladder is authored, the RECORD
each ladder will be authored against has to be true and anchored. Batch 24 skipped straight to
authoring, then found 50 record defects and had to re-author 71% of the batch; batch 25 ran this pass
first and its reviewers found the defects BEFORE they were laddered. This pass exists so that
happens again.

Every entry on these crops already carries `sources` and `anchoring_urls`, unlike the herbs. That is
not the same as being anchored: the cert logs for these crops record that several anchors were
inherited from a sibling, that one cited page 403s, and that named pests are "real but not on the
sampled cited pages". Your job is to find out whether each claim is TRUE, whether the document the
record points at actually CARRIES it, and to name the document that does.

## The rules that govern your reading

1. **Unsupported is not unsourceable. HUNT before you downgrade.** The last four times a claim in
   this dataset was flagged unsupported, all four were found at Tier 1 on a real hunt. Do not report
   "no source found" until you have tried the crop's own extension vocabulary (listed in your task),
   the land-grant institutions for the crop's growing regions, and the specific pathogen or pest
   name once you have one.
2. **Locating the right document is NOT the same as supporting the claim.** Read the document and
   quote the sentence that carries the claim. A document about the right organism that never states
   the claim does NOT anchor it. Quote verbatim; do not paraphrase into support.
3. **Match the TAXON, not the common name.** Resolve each organism to a binomial and say which
   document gave you that binomial. "Borers" on a mulberry and "borers" on a peach are not the same
   insect. A psyllid on persimmon is not the citrus psyllid.
4. **Absence findings are document-scoped.** "No extension publishes X" is almost always false and
   usually means "the two documents I opened do not publish X." Say which documents you checked.
5. **A 403 is not a dead URL and a 200 is not a live one.** WAF challenge pages and text-less PDFs
   have been cached as successful reads before. If a fetch gives you no readable text, say so
   rather than treating it as an absence. Try a second path (WebFetch, then curl with a browser
   user agent, then the `r.jina.ai/` text proxy prefix) before calling anything unreadable, and say
   which path finally worked, because a proxy retrieval is weaker evidence than a first-party read.
6. **Report what the document says, including when it contradicts the record.** A record claim you
   cannot support is a FINDING, not something to quietly soften.
7. **A TITLE IS NOT A SENTENCE.** NC State Plant Toolbox pages (`plants.ces.ncsu.edu/plants/...`)
   list `Insects:` and `Diseases:` as rows of linked factsheet TITLES, not as statements about the
   crop. "Leaf spot" in that row means a factsheet exists, not that the toolbox asserts the crop gets
   it. Batch 25 shipped one claim anchored to a title that only parsed as a claim under the wrong
   reading. If your anchor is a toolbox row, say so and find the factsheet or another document that
   makes the actual statement.
8. **UC IPM has two audiences.** `ipm.ucanr.edu/home-and-landscape/...` and the `PMG/GARDEN` pages
   are home advice. `ipm.ucanr.edu/agriculture/...` pages are COMMERCIAL: per-acre rates, monitoring
   thresholds and postharvest standards there are not home-garden advice, though their biology
   (life cycle, overwintering site, damage description) is usable. Say which kind each anchor is.
9. **A quoted fragment carrying an ellipsis must be re-read at source** before any number inside it
   is treated as published. The scoping tends to live exactly where the ellipsis is.

## Source admission

Only sources in `tools/staging/pla8_batch26_trees/source_catalog_admission.txt` are citable, by
their catalog key (the `key` column; the catalog field is `id`/`name`, never `title`). The catalog is
220 entries, **all university-extension / government / .edu -- there are NO journal entries**, so a
peer-reviewed-journal citation cannot be used as an anchor even when it is the best evidence. If the
ONLY support you find is a journal, report it as `JOURNAL-ONLY` with full details -- that is a real
outcome and becomes a catalog-addition decision rather than a silent gap. Prefer a T1 extension
document that carries the same claim.

Read the `citable_for` column before citing a key: several keys are scoped to a specific publication
or crop (for example `uf_ifas_hs764` is one apple bulletin, `ncsu_ext_toolbox_punica_granatum` is
one toolbox page), and citing one for a claim outside its scope is a defect the promote guards catch.
Use the parent portal key (`uf_ifas_edis`, `ncsu_ext`, `uc_ipm`, `uga_ext`) for a document not
already carved out. If a document you need has no admissible key at all (an institution not in the
catalog), report it as `NEEDS-CATALOG-ADMISSION` with the institution, the URL and what it carries.

## Batch-wide things to watch for

* **Bundled entries.** One organism or disease complex per id is the rule for this batch. Where an
  entry names two problems ("Mealybugs and scale", "Leaf spot and twig dieback", "Fruit-raiding
  wildlife (raccoons, opossums, squirrels)"), report each half SEPARATELY: its own organism(s), its
  own anchors, its own ladder-relevant facts. The orchestrator decides whether to split, retire a
  half, or keep an umbrella, and needs the halves graded independently to decide.
* **Bare generics.** An entry named "Borers" or "Leaf spots and minor foliar diseases" is one of two
  things: ONE organism nobody pinned, or a genuine umbrella the literature itself leaves unresolved.
  Batch 25 found one of each and a mechanical rule would have been wrong half the time. Determine
  which, and show the evidence: if a US extension names a single organism for this crop, quote it;
  if the sources themselves list several or none, say that.
* **PLA-457, do not resolve it.** The catalog's `horticultural_oil` entry states a sulfur/oil
  spacing interval that disagrees with its own anchor (UC IPM PN 7405 says 30 days, PN 7406 says
  2 weeks, PN 7408 says 3 weeks). A roster-wide ruling is pending. If any document you read for
  this crop states a sulfur/oil interval, REPORT the figure and the document sentence under a
  `PLA-457` heading and do not adjudicate which is right.
* **Template siblings.** pear-asian and pear-european carry byte-identical entries for Pear scab,
  Pear psylla and Pear decline, and near-identical Codling moth and Fire blight. Each pear reviewer
  reads the documents independently; do not assume the sibling's reviewer is covering it.
* **Bee and pollinator safety, product claims, °F figures.** Any bee-toxicity rating, product name,
  threshold or temperature you carry forward must be quoted from a document. A rating nobody
  published is a fabrication even when it is probably right (batch 8 found one invented in three
  fields).

## What to produce

Write ONE file: `tools/staging/pla8_batch26_trees/record_<crop>.md`. Nothing else. For EVERY problem
entry on your crop (both `pests[]` and `diseases[]`, including any duplicate), one section:

```
## <exact current `name`> [pests|diseases]  -- severity <x>, type <y>
STATUS: SOURCED-OK | SOURCED-WEAK | ANCHOR-MISPOINTED | UNSOURCED-FOUND | UNSOURCED-NOT-FOUND | JOURNAL-ONLY | WRONG
ORGANISM: <binomial(s), or "umbrella -- multiple organisms", or "cannot be resolved">, per <doc>
ANCHORS: <catalog_key> <url> -- verified <date you fetched it> -- <home | commercial | toolbox-row | pdf>
  > verbatim quote carrying the claim
  > verbatim quote carrying the claim
RECORD CLAIMS THAT HOLD: <list, each with which anchor carries it>
RECORD CLAIMS WITH NO ANCHOR: <list, verbatim from the record>
RECORD CLAIMS THAT ARE WRONG: <list, with the document sentence that refutes it>
BUNDLE / GENERIC VERDICT: <only for bundled or bare-generic entries: one problem or two; pinned
  organism or genuine umbrella; the evidence>
LADDER-RELEVANT FACTS the record does not carry: <things a control ladder would need>
PLA-457: <any sulfur/oil interval a document states, verbatim, or "none seen">
```

Then a final `## SUMMARY` section: counts by STATUS, the single most important finding, and a
`## PROPOSED TYPE` line per entry giving the fine problem type from this set --
`insect | mite | mollusk | fungal | bacterial | viral | physiological | nematode | vertebrate` --
with the organism that justifies it (four of the six crops carry only the coarse `pest`/`disease`
type today, and the pears' "Pear decline" carries `other`, which no gate recognizes).

**Be specific about the ladder-relevant facts.** The next pass builds a least-invasive-first ladder
(cultural -> physical -> biological -> soft chemical -> conventional). Facts that matter on a
perennial: what overwinters where, when the vulnerable stage occurs (bloom, petal fall, fruit
sizing, leaf drop), whether the source names a monitoring signal or threshold, whether resistant
cultivars or rootstocks exist BY NAME, what sanitation the source actually prescribes (and whether
it is for a home tree or a commercial block), what the source says a home grower should NOT bother
doing, and the exact wording of any "no effective control" statement.

## Consumer-copy constraints (so you flag record prose that violates them)

No em dashes. American English. Temperatures render as `°F`. "plant" lowercase except sentence-start.
Everyday words over technical ones in consumer prose.
