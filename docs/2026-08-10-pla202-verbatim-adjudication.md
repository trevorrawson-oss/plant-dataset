# PLA-202 -- Verbatim HARD-hit adjudication: every hit read, per-crop dispositions

**Date:** 2026-08-10. **Base canonical:** `c16071bc` (PLA-199's promote; verified against
LATEST.txt at session start -- the issue anticipated `060b91b8`, one promote behind).
**Scan:** `tools/verbatim_scan.py` at `2310bae` (post-PLA-160, coverage-floor honest).
No canonical change in this arc. No matcher change in this arc (the PLA-138 rule: the
count was made smaller only by reading, never by tuning).

## What this arc did

1. **Fixed the denominator first.** Retried every uncovered document with an
   alternate-user-agent ladder, then re-ran the roster.
2. **Checked publisher reuse terms** for the institutions carrying the hits (annex below).
3. **Built the benign class by hand-reading** a 38-hit sample (the 20 longest hits +
   the 10 largest repeated-run families + 8 random unique runs) BEFORE classifying
   anything at scale. The standard with all 38 sample rulings:
   `scratchpad adjudication_standard.md`, reproduced in §3.
4. **Read every remaining hit** -- all 333 HARD hits were individually read against
   their source context (172 run-groups + 6 post-retry hits). No hit was ruled by
   pattern alone; family members were each eyeballed in their own prose context.

## 1. The denominator (before adjudicating the numerator)

Baseline re-run against `c16071bc` reproduced PLA-160's numbers exactly
(17 clean / 84 crops / 327 HARD / 20 blocked / 3,082 of 3,355 pairs), so PLA-199's
catalog-only promote moved nothing -- confirmed, not assumed.

**Retry pass 1** (129 distinct uncovered documents x 5 header profiles: repo Chrome UA,
curl, full-browser-with-referer, iOS Safari, Googlebot; per-host politeness delay):
**25 recovered** -- 18 via `curl/8.4.0` (all of TAMU aggie-horticulture yielded to curl,
exactly the `url-liveness-is-not-a-status-code` pattern), 6 via the repo's own UA
(transient/rate-limit failures), 1 via Googlebot (UMN). **Retry pass 2** (77 still-dead
non-MSU documents, 6s per-host delays): **8 more** (all UMN -- slower cadence cleared what looks like rate limiting, not a WAF). MSU's 27 documents behind
Incapsula remain unreadable from every vantage, consistent with the 2026-07-30
measurement that MSU blocks regardless of headers.

Post-retry roster (the real denominator):

| | pre-retry | post-retry |
|---|---|---|
| pairs compared | 3,082 / 3,355 | **3,142 / 3,355 (94%)** |
| crops verbatim-clean (exit 0) | 17 | **21** (artichoke, sweet-pea, field-corn, flint-corn flipped in) |
| crops with HARD hits | 84 / 327 hits | 84 / 333 hits (6 new hits from newly readable docs) |
| crops coverage-blocked, zero hits (exit 2) | 20 | **16** |
| distinct unreadable documents | 129 | **96** (33 recovered across both passes) |

The 6 post-retry hits (strawberry x3 vs the TAMU small-acreage strawberry guide;
radish + turnip vs UMN root-maggots; pumpkin vs UMN cucumber-beetles) were read and
ruled with everything else -- all six benign (attributed geographic enumeration;
lifecycle-fact recitations with close tracking noted).

## 2. Headline result: 333 hits read, 308 benign, 25 rewrites across 15 crops

| disposition | hits | distinct prose fields |
|---|---|---|
| benign (classes B1-B6, each ruling recorded) | 308 | -- |
| **REWRITE owed** | **25** | **22 fields in 15 crops** |

Class distribution: B3 quantitative-spec 100, B2 stock-idiom 86, B4 technical-phrasing
69, B1 calendar-furniture 24, B6 functional-procedure 15, B5 citation-furniture 14;
R1 attributed near-quote 18, R2 unattributed lift 7.

The issue's calibration held: **the rewrite class concentrates exactly where the
length-sort predicted.** 7 of the 10 longest hits (>=12 words) are rewrites; the 168
hits at the 8-word floor yielded only 4.

## 3. The adjudication standard (built from reading, then applied by reading)

The question each hit answers: **does our prose reproduce the source's EXPRESSION
beyond what stating the fact requires?** Facts, quantities, procedures, and standard
terminology are nobody's expression; a source's connected explanatory sentence is --
and attribution does not un-reproduce it.

Benign classes (every ruling individually recorded in the ledger):

- **B1 calendar-furniture** -- month lists / table headers ("jan feb mar ... oct" x24:
  our Hawaii succession strings are month lists; every planting calendar prints the
  same header).
- **B2 stock-idiom** -- phrases original to no one: "as soon as the ground/soil can be
  worked" (x34, matched against FIVE different institutions' documents), "1 to 2 inches
  of water a week", "the soil to a depth of at least 6 inches", "one of the easiest
  herbs to grow" (UF says it of mint, Clemson of dill).
- **B3 quantitative-spec** -- rates, analyses, dilutions, schedules, spacings, depths,
  date windows: "5 pounds of calcium nitrate (15.5-0-0) per 1000 square feet". The
  factual content dictates the wording; attributed inline where a recommendation.
- **B4 technical-phrasing** -- standard definitional/botanical wording: monoecious =
  "separate male and female flowers on the same plant" (four independent sources use
  the identical phrase), the black-rot V-lesion description, pathogen binomials,
  symptom descriptions that track the observation.
- **B5 citation-furniture** -- `sources_summary` name strings matching the document's
  own title. Titles are supposed to match; this is attribution working. (Scan-scope
  note for a future pass -- deliberately NOT changed now.)
- **B6 functional-procedure** -- procedural steps whose wording tracks the procedure
  (hand-pollination steps, IPM control lists), verbatim spine <= ~9 words with the
  surroundings already paraphrased.

Rewrite classes (disposition = rewrite; attribution does not cure):

- **R1 attributed near-quote** (18 hits) -- "X notes / suggests / is direct about it:"
  followed by the source's connected explanatory clause verbatim, without quotation
  marks. The fact is citable; the sentence is theirs.
- **R2 unattributed lift** (7 hits) -- the source's expressive sentence or clause in
  our own voice ("Downy mildew is one of the most important leaf diseases of
  cucurbits"; "Root-knot nematodes are the leading killer of figs...").

Two under-measurement discoveries made while reading (recorded, not acted on):

- **Single-word swaps break runs.** asparagus `soil.preferred_description_seasoned`
  reads as a 10-word hit but is a ~16-word UMN sentence with "soil"->"ground" and
  "rains"->"rain" swapped; pawpaw's peduncle-borer sentence likewise ("burrows"->
  "bores"). Both ruled REWRITE. Corollary: `run_words` understates true overlap, and
  lifts paraphrased more aggressively than one word in eight are NOT measured by this
  instrument (stated in §6).
- **Cross-document coincidences exist.** A Nevada carrot note matched the sweet-corn
  row of a South Texas guide on "august to mid september for a fall crop" -- calendar
  phrasing collides across unrelated documents; matches are evidence, not verdicts.

## 4. Per-crop dispositions (the unit that matters: can this crop flip)

**Verbatim criterion SATISFIED (51 crops):** 21 scan-clean (acorn-squash, artichoke,
bee-balm, borage, broccoli, butternut-squash, cosmos, field-corn, flint-corn, kohlrabi,
lavender, marigold, nasturtium, oregano, sage, spaghetti-squash, sunflower-sprouts,
sweet-pea, viola, wheatgrass, zinnia) + 30 all-benign with full coverage
(arugula-microgreens, banana-pepper, bell-pepper, blackberry, broccoli-microgreens,
calendula, cantaloupe, chamomile, cilantro-microgreens, eggplant, garlic,
honeydew-melon, jalapeno, leek, lemongrass, microgreens-mix, parsnip, pea-shoots,
popcorn, potato, pumpkin, radish, radish-microgreens, shallot, slicing-cucumber,
sweet-alyssum, sweet-corn, sweet-potato, thyme, watermelon).

**All hits benign but coverage incomplete (39 crops):** every HARD hit adjudicated
benign; remaining exposure is only the still-unreadable documents (mostly MSU).
These crops' verbatim blocker is reduced to a coverage question.

**REWRITES OWED (15 crops, 22 fields, 25 hits):**

| crop | field | class | notes |
|---|---|---|---|
| asparagus | `description_seasoned` | R1 | UC IPM "two distinct periods" sentence |
| asparagus | `hardiness_notes_seasoned` | R1 x2 | Missouri spring-freeze sentence + the same UC IPM sentence again |
| asparagus | `soil.preferred_description_seasoned` | R1 | UMN sentence, cosmetic swaps |
| beet | `regions.utah_dixie.region_notes_beginner` | R1 | USU "left in the ground quite late into winter" |
| cabbage | `regions.hawaii_tropical` zone_notes z10/11/12/13 + region_notes_seasoned | R1 x5 | one CTAHR sentence ("excellent garden crops at low elevations...") repeated per zone -- ONE rewrite fixes five hits |
| carrot | `regions.utah_dixie.region_notes_beginner` | R1 | same USU sentence as beet |
| cherry-sour | `regions.mid_atlantic` suitability z7+z8 | R1 x2 | NC State "favorable but need careful management" clause, same text both zones |
| chives | `regions.fl_peninsula.region_notes_beginner` | R1 | UF "cool-season herb that thrives..." |
| echinacea | `regions.fl_peninsula.region_notes_beginner` | R1 | UF colloquial "fizzle out" voice |
| english-cucumber | `diseases[1].symptoms_seasoned` | R2 | Clemson downy-mildew importance sentence in our voice |
| fig | `companions.bad_seasoned[0].why_seasoned` | R2 | UGA "leading killer" editorial phrase |
| lime | `diseases[5].cause_seasoned` | R2 | UF epidemiology clause verbatim in our voice |
| pawpaw | `pests[0].cause_seasoned` | R2 | KYSU peduncle-borer sentence, cosmetic swaps |
| raspberry | `regions.utah_dixie.region_notes_seasoned` | R1 | USU ripens-after-heat reasoning clause |
| spring-onion | `regions.utah_dixie.region_notes_seasoned` | R1 | USU "green onions can be planted spring or fall..." (16w, longest attributed near-quote) |
| strawberry | `regions.ca_north_coast.region_notes_seasoned` | R2 x3 | "production is highest in the first full season..." matches THREE UC documents -- one rewrite fixes three hits |
| turnip | `regions.utah_dixie.region_notes_beginner` | R1 | same USU sentence as beet/carrot |

Pattern worth naming: **the R1 class is an authoring-pattern problem, not scattered
accidents.** 12 of 18 R1 hits are region-prose fields written as "institution + verbatim
clause", and the USU Washington-County fall-gardening PDF alone accounts for 5 rewrites
across 4 crops (beet, carrot, turnip, spring-onion -- the utah_dixie build reused the
pattern). The rewrite work is ~16 sentences of fresh paraphrase.

**Zero hits but coverage-blocked (16 crops):** apple, cherry-sweet,
cilantro-coriander, collards, elderberry, grapefruit, kale, mulberry, orange-navel,
peach, pear-asian, pear-european, persimmon, sunflower, swiss-chard, tomatillo.
All are blocked on the still-unreadable documents; none carries an unadjudicated hit.

Full machine-readable ledger (every hit: path, url, maximal shared run, class,
disposition, ruling route): `docs/pla202_verbatim_adjudication_c16071bc.json`.
Per-crop summary: embedded in the same file's compilation source.

## 5. Publisher reuse terms (annex; dispositions do NOT lean on this)

Full annex with verbatim policy quotes and URLs:
`docs/2026-08-10-pla202-extension-reuse-terms.md`. The one-line answer: **no cited
institution publishes a grant covering commercial web republication.** Six have
explicit conditional grants -- every one scoped noncommercial or educational (UF/IFAS
and UC ANR via CC BY-NC-ND 4.0, WSU, OSU per-document, UGA, MU print-only); four
require permission outright (USU, UMN, ISU, CTAHR); five are bare-copyright unstated
(Clemson -- our largest hit source at 64 -- NC State text, Arizona, Arkansas, TAMU).
So the reuse-terms check does not shrink the problem, and it sharpens the ruling
logic: benign hits are benign because facts, quantities, and stock phrasing are not
protected expression -- not because reuse is licensed.

Dispositions above were made on the reproduce-expression test alone. A true marked
quotation remains an option for any R1 (short attributed quotation is the classic
fair-use posture even commercially), but given the terms above, paraphrase is the
clean path and is what the rewrite disposition specifies.

## 6. What was NOT measured (PLA-138 stopping rule)

- **96 documents never compared** (27 MSU/Incapsula, 7 UMN, 6 NCSU content.ces, 5 UC
  Davis postharvest, 4 Arizona, and a long tail -- each recorded with its refusal
  reason in the ledger's roster file). Every pair involving them is unmeasured; the 16
  exit-2 crops and the 50 hit-carrying crops with partial coverage (the 39 all-benign
  crops of §4 plus 11 of the 15 rewrite crops, which carry coverage gaps of their own)
  cannot claim full verbatim coverage until those documents are read or their citations
  are re-anchored. [An earlier draft said "42" here -- that was the pass-1 retry count,
  stale after retry pass 2 recovered 8 more documents; reconciled 2026-08-10.]
- **Borderline hits (6-7 shared words) were NOT adjudicated** -- the repo's HARD
  threshold is >=8; the scan reports borderlines and this arc left them unruled
  (2,362 across the roster).
- **Paraphrase below the 8-word floor is invisible to this instrument.** The two
  cosmetic-swap catches in §3 prove close paraphrase exists that the n-gram measure
  understates; a lift altered every 7th word would score zero. No tool measures
  close-paraphrase here; adjudication of that class would be a different (reading-only)
  arc.
- **Only each crop's own anchoring URLs were compared.** Prose lifted from a document
  cited by a DIFFERENT crop (or by nothing) is unmeasured -- e.g. the cross-crop
  template families (pepper/cucurbit/bean shared text) were each compared only against
  their own citations.
- **`sources_summary` name strings are inside scan scope** and produced 14 B5 hits;
  whether to exclude them is a scan-scope decision deliberately left to a future issue
  (changing the collector now would be matcher-tuning mid-adjudication).
- **Register siblings of the 22 rewritten fields were not read.** Concretely: beet,
  carrot and turnip were hit on `region_notes_beginner` against the USU Washington
  County PDF, and their `_seasoned` siblings were never examined against that document.
  The scan covers them only to its own 8-word floor; nobody READ them for this arc.
- **One sentence was removed on suspicion, then corroborated after the fact.** The
  rewrite pass also folded away strawberry's "mid to late August is a good planting
  time in all coastal locations" (ca_north_coast), which the author flagged as
  UC-boilerplate-shaped. It was NOT in the ledger (sub-threshold for the scan). The
  post-promote source-truth sample then found UC IPM's strawberrytime page publishing
  "Middle to late August generally is the best time to plant strawberries in all
  locations" -- the suspicion was right. It remains a suspected-class removal outside
  the 25 adjudicated hits, not a 26th hit cleared; it is evidence for the
  close-paraphrase sampling successor below.

## 7. The three named successors (tracked gaps, not started)

The 22-field rewrite pass proposed by the first draft of this section SHIPPED
2026-08-10 as the `c16071bc` -> `76f92a20` promote (see the post-promote addendum
below). Three successors remain, named so the gap is tracked rather than implied:

1. **Coverage endgame for the 96 unreadable documents** -- re-anchor citations off
   dead MSU pages where a live equivalent exists, or record a per-document coverage
   exemption with reason (mirroring the A54 exemption pattern). Until then, 16
   zero-hit crops stay blocked and 50 hit-carrying crops keep partial coverage.
2. **Scan-scope ruling on `sources_summary`** (and whether `succession_continuous`
   month-strings belong in prose scope) -- a deliberate instrument change, TDD'd, its
   own issue.
3. **A reading-only sampling pass over the close-paraphrase class** -- the layer this
   instrument cannot see (single-word swaps, sub-threshold boilerplate). Three
   confirmed members already: the two cosmetic-swap catches in §3 and the strawberry
   sentence above. Sampling design, not a matcher.

## 8. Post-promote addendum (2026-08-10, `c16071bc` -> `76f92a20`)

The rewrite pass was applied the same day (tools/promote_pla202_rewrites.py; guard
suite tools/test_promote_pla202_rewrites.py). Roster re-scanned in full against
`76f92a20` -- recomputed, not derived:

| bucket | crops |
|---|---|
| verbatim criterion SATISFIED | **55** |
| all hits benign, coverage incomplete | **49** |
| rewrites owed | **0** |
| zero hits, coverage-blocked | **17** |

Sum 121. 308 HARD hits remain roster-wide, every one adjudicated benign in the
ledger; zero unadjudicated. Of the 15 rewrite crops: echinacea, english-cucumber,
raspberry and spring-onion moved to SATISFIED; ten moved to the coverage-incomplete
bucket on their own unreadable documents; **cherry-sour cleared both its hits and
thereby moved to the zero-hit coverage-BLOCKED bucket** (its uncovered documents now
control its exit code) -- the recompute caught what copying forward would have missed.
Post-promote roster: `docs/pla202_verbatim_roster_76f92a20.json`.

**The per-hit ledger `docs/pla202_verbatim_adjudication_c16071bc.json` is keyed to
`c16071bc` and is HISTORICAL as of this promote** -- read it as the adjudication-time
snapshot (its 25 rewrite rows describe prose that no longer exists), never as current
state. The current measurement is the `76f92a20` roster file.

**And plainly: PLA-202 closing does NOT mean the dataset is verbatim clean.** 96
cited documents were never compared and 2,362 borderline (6-7 word) hits were never
adjudicated; what closed is the adjudication of every HARD hit the instrument could
measure, and the repair of the 25 that needed it.
