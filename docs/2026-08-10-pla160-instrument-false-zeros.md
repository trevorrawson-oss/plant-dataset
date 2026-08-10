# PLA-160 -- instrument false-zeros: the four scans, fixed and measured

**Session 2026-08-10. Base canonical `060b91b8` (matches LATEST.txt; the issue's stated base
`72284f02` predates PLA-155/157 landing -- the kickoff pinned `060b91b8` and preflight passed).
NO CANONICAL CHANGE in this session: the 27 bloom findings all survived re-verification (§5),
so the corrections promote the issue anticipated turned out to be empty.**

Parallel-lane note: PLA-199 ran concurrently in this checkout (its footprint:
`whole_crop_gate.py`, `promote_pla199_titles.py`, `source_catalog_title_gate.py` + tests).
Verified disjoint from this session's footprint (the four scanners + their tests) by
inspection of `git status` -- zero file overlap.

**PLA-199's promote LANDED FIRST** (`060b91b8` -> `c16071bc`, working tree, mid-session).
Verified harmless to every measurement here: the promote is CATALOG-ONLY (101 top-level
`source_catalog.*.title` additions + 2 name migrations; its own guards prove every subtree
outside `source_catalog` byte-identical, zero crops move), and `verbatim_scan` /
`bloom_datum_scan` / `soil_temp_floor_scan` all read CROP subtrees, which are identical in
both states. This session has no promote of its own, so nothing rebases; the four suites
were re-run green against `c16071bc` after the landing. Numbers in this document were
measured at `060b91b8` and hold at `c16071bc`.

Every fix below went RED before GREEN: the defect was exercised against the unfixed tool and
the failing test was watched fail, then the fix landed (CLAUDE.md TDD rule; suites runnable
under both pytest and `python3 <file>`).

## THE COUNTS ROSE. That is the contract working, not defects introduced.

| instrument | before (false zero) | after (honest) |
|---|---|---|
| `verbatim_scan` | `HARD hits: 0`, exit 0, **0 of N sources compared**, every crop, forever | see §1 + §4: coverage floor, exit 2 on insufficient coverage; roster run recorded |
| `soil_temp_floor_scan` | `TOTAL: 0 cells`, exit 0; 131 in-scope cells silently skipped; flip-eligible | 42 unruled LEADS (corn/bean class), 191 UNDETERMINED cells, exit 1; **not** flip-eligible |
| `bloom_datum_scan` | absence outranked unread; 46/70 MENTION_NO_DATE were window artifacts | UNDETERMINED outranks absence; 64 declaration-shaped arm verdicts now refused |
| `contamination_scan` | "Mean overall contamination across the 7 non-walked crops: 0%" (0/0) | "n/a -- refuses a mean over ... denominators all 0"; per-crop `n/a (0 leaves measured)` |

Do not "fix" any of these rises by loosening a predicate. If a count looks alarming, that is
the finding.

## 1. verbatim_scan -- the flip-blocker that had never compared anything

Cause confirmed as diagnosed: it read `/tmp/verbatim_cache` (`sha1[:16].body/.meta`, a retired
format, always empty) while the repo populates `tools/.doc_cache` (`sha1.txt`, extracted text,
PDFs through pypdf at fetch time). It printed its own zero coverage and ignored it.

Fix: repointed at the SHARED cache layer (`doc_mentions_crop_scan.cache_path` semantics +
`unreadable_reason`, so WAF pages / `\x00FETCHFAIL` stubs / text-less PDFs count as NOT
COVERED); `--fetch` delegates to the shared pypdf-capable fetcher. **Coverage floor:** a
zero-hit verdict is reportable only when >=1 source was compared and none is uncovered;
otherwise `verbatim_scan COVERAGE INSUFFICIENT: compared K of N` and exit 2. Exit 1 on HARD
hits unchanged.

RED watched: the empty-cache invocation exited 0 with `0/1` compared before the fix.
Tests: `tools/test_verbatim_scan.py` (6, including the 8-word-lift detection surviving the
repoint, and the default-cache repoint proven against real lemon: 17/33 compared, was 0/33).

## 2. soil_temp_floor_scan -- the 76%-scoped zero

Three defects, three fixes (`tools/test_soil_temp_floor_scan.py`, 13 tests):

1. **The nulled-anchor escape hatch.** In-scope cells lacking a parseable
   `resolved_from.last_frost` or start date were silently skipped -- the audit's mutation
   (inject defect, null the anchor, defect vanishes green) reproduced. Now: `undetermined()`
   surfaces them; exit contract is 1 = unruled hits, **3 = zero hits but unevaluable cells
   exist** (named in output: `soil_temp_floor_scan UNDETERMINED`), 0 only when both are zero.
   Measured: 131 of 547 old-scope cells were skipped; under the corrected predicate it is
   **191 cells, all in the frost-free regions** (hawaii_tropical 132, rgv 32,
   fl_peninsula 27), which is structural (no frost date exists there) but stays reported,
   never folded into a green.
2. **RULED key narrowed to its evidence.** Was `(region, zone)` -- earned by reading 6 cells,
   suppressing every future hit in the zone (proven: injected okra/utah_dixie/z8 was
   absorbed). Now `(slug, region, zone)`, enumerating exactly the six cucurbit cells the
   2026-07-29 ruling read.
3. **The predicate.** Was bare `germination_temp_f[0] >= 70` -- an OPTIMAL band's floor read
   as a minimum, excluding all four corns and four beans (germ floor 60, `frost_effect`
   'killed'): the protected class. Now `frost_effect == 'killed' AND g[0] >= 60`. The hardy
   annuals with 60-65 floors (dill, calendula, borage, sweet-alyssum -- 'foliage_damaged')
   stay excluded: measured, they would have contributed ~40 legitimate-looking false hits.

**The corrected predicate surfaces 42 unruled LEAD cells across 8 crops** (leads, unread;
data work outside this issue's scope):

- utah_dixie z8, 8 cells, all delta -15 (Mar 15 vs Mar 30 frost): dry-bean, edamame,
  field-corn, flint-corn, popcorn, sweet-corn, green-beans-bush, pole-beans -- the exact USU
  Group C explicit-date pattern already ruled for the six cucurbits. Likely RULED candidates,
  but the ruling covers what was READ, so each needs its cell read against the USU table
  before being added.
- ca_desert z9/z10/z11, 6 cells: green-beans-bush + pole-beans opening Jan 1/Jan 15 at or
  before the Jan 15/31 frost -- the SAME shape as the ca_desert cucurbit defect corrected
  2026-07-29 (`desert-cucurbits-planted-on-last-frost`), invisible then because beans sat
  below the 70F floor. Highest-priority leads of the 42.
- northern_tier z3-z7, 10 cells: both bean crops opening exactly ON the mean last frost
  (delta 0).
- mid_atlantic + mid_south z7/z8, 18 cells: the four corns + green-beans-bush opening 5-7
  days before mean last frost.

## 3. bloom_datum_scan -- absence no longer outranks unread

- **Precedence inverted** (`best_verdict`): `PUBLISHES_TIMING > UNDETERMINED >
  MENTION_NO_DATE > NO_MENTION`. An arm with any unread document is UNDETERMINED.
- **`assert_absence_reportable` adopted** (raises `cited_claim_scan.UnreportableAbsence`,
  all reasons collected): refuses a declaration-shaped arm verdict when any document is
  UNDETERMINED, when there are no documents at all, or when an absence-verdict document is a
  SUBJECT document (head names the citing crop -- `document_subject_is`). The refusal
  demands a human whole-document read; it does not forbid one from establishing absence.
- **The wrong method is kept deliberately**: `classify` still uses the 120-char window, with
  a pinned witness test (`test_the_wrong_method_still_classifies_the_pawpaw_shape`) so the
  mutation that removes the refusal layer is detectable.
- Live report now refuses 64 declaration-shaped arm verdicts and prints the
  declared-findings-whose-support-changed section.
- Tests: `tools/test_bloom_datum_scan.py` grew 24 -> 33.

Instrument observations from §5's re-reads, both in the FALSE-PRESENCE direction (the safe
one -- they demand a read instead of licensing a declaration): the handbook ch. 15
PUBLISHES_TIMING verdict rides on a "Prune in February ... full bloom" figure caption, and
pomegranate.aspx's rides on the page DATELINE ("May 1, 2016") sitting near "blooms".

## 4. contamination_scan -- 0/0 no longer renders as 0%

`overall` is `None` (not `0.0`) on an empty denominator; per-crop rows render
`n/a (0 leaves measured)`; the mean is over MEASURABLE non-walked crops only with the
exclusion stated; an all-empty set gets an explicit refusal in the scan's own name. The
walked-crops clean-check line's unguarded `100*s/t` (same defect class, latent
ZeroDivisionError) was guarded in passing. Real run: the 7 shells now produce
"Mean overall contamination: n/a -- contamination_scan refuses a mean over 7 non-walked
crop(s) whose denominators are all 0". Tests: `tools/test_contamination_scan.py` (4).

## 5. The 27 bloom findings: ALL SURVIVE re-verification. Zero corrections owed.

**The issue expected proximity-artifact casualties here. Verification contradicts the
issue, and the issue yields.** The 27 `*_bloom_offset_undocumented` findings were NOT
written from `bloom_datum_scan`'s window verdicts -- every one rests on a whole-document
hand read, and the two that once had wrong reasons (apple, pawpaw) were already corrected
2026-07-30. This is consistent with the audit's own §4 ("campaign B: 0 wrong records,
whole-document method throughout").

Method: enumerated all 27 from canonical (13 mid_south template, 8 mid_atlantic template,
apple, pawpaw, strawberry, + 3 crop-scoped mid_atlantic: apricot, cherry-sweet,
cherry-sour). Read all 8 distinct bodies. Checked all 15 crops' `verification_log` /
`verification_log_ref` for bloom adjudications FIRST (PLA-5 rule): **zero bloom mentions,
no cert-log trap.** Then re-fetched the findings' NAMED documents into the shared cache and
re-read every bloom-family context:

| finding group | named evidence | re-verification 2026-08-10 |
|---|---|---|
| 13x mid_south (template) | UAEX set read in full 2026-07-30 | FSA-6129: all bloom language relative ("Late blooming", "9 days before Elberta") -- no date. FSA-6130: relative only. fruit-trees.aspx: descriptive only. mulberry.aspx: nav-menu hits only. pomegranate.aspx: season-granular only ("flowers twice a year ... spring ... late summer") -- no date. **CONFIRMED** |
| 8x mid_atlantic (template) | NCSU handbook ch. 15 read in full | 48 bloom-family mentions in live capture; the ONLY month-near-bloom context is the February pruning caption, exactly as the finding records. **CONFIRMED** |
| apple/mid_atlantic | corrected 2026-07-30, Trevor-ruled: rests on GEOGRAPHY | apples.extension.org verified PUBLISHES_TIMING (mid-April = WESTERN NC; belt is Piedmont/Coastal Plain). The finding already says so. **SOUND** |
| pawpaw/mid_atlantic | corrected 2026-07-30: raw-bytes read, zero bloom words | psu_ext page re-classified NO_MENTION (zero bloom/blossom/flowering). Subject document, but the finding rests on the full read, which the new refusal layer explicitly permits. **CONFIRMED** |
| strawberry (crop-scoped) | FSA-6103 + berries.aspx, sha256s recorded, Trevor-ruled 2026-08-03 | FSA-6103: "bloom very early in the spring" qualitative only. berries.aspx: zero bloom words. **CONFIRMED** |
| apricot / cherry-sweet / cherry-sour (crop-scoped) | scoped to the 11 NC State documents, 403 recorded UNDETERMINED | hunt doc re-read; scoping discipline exemplary; handbook re-verification above covers the load-bearing document. **CONFIRMED** |

A note on the scan-vs-findings relationship: the mid_south and mid_atlantic arms cite BARE
HOSTS (`uaex.uada.edu`, `content.ces.ncsu.edu`), so the scan's per-arm verdicts classify
institution HOMEPAGES -- worthless as evidence either way. The findings' evidence lives in
the hunt docs and in the named publications, which is where re-verification went.

One lead (not a defect, not acted on): pomegranate.aspx's "flowers twice a year" is a
biology nuance a future pomegranate variety/region pass may want; the modeled single spring
bloom arm is the fruiting-relevant one for mid_south.

## 6. The roster verbatim run (the actual deliverable of fix 1)

Run 2026-08-10 against `060b91b8`, after fetching the roster's uncovered documents into the
shared cache (619 attempted, 520 succeeded, 99 fetch failures -- WAF/403 hosts -- which stay
NOT COVERED, honestly). **First time in this repo's history the flip-blocking criterion has
compared anything.**

| | before (broken cache) | after |
|---|---|---|
| crop-source pairs compared | **0 of 3,355** (every crop, every run, forever) | **3,082 of 3,355 (92%)** |
| crops with an established "verbatim clean" (exit 0) | 0 -- the status had never been established for ANY crop | **17** (acorn-squash, bee-balm, borage, broccoli, butternut-squash, cosmos, kohlrabi, lavender, marigold, nasturtium, oregano, sage, ...) |
| crops with HARD hits (exit 1, adjudication owed before flip) | reported 0 | **84 crops, 327 HARD hits** |
| crops coverage-insufficient, zero hits (exit 2) | reported as clean | **20** |

Full per-crop table: `verbatim_roster_results.json` (session scratchpad; regenerate any time
-- the scan is deterministic over the cache).

**The 327 hits are UNADJUDICATED. Recording, not ruling** -- adjudication is Step-11
per-crop flip work, and the scan's own doctrine routes benign-class rulings to the voice
lane rather than self-dismissing. Composition, to size that work honestly:

- The most repeated shared runs are stock horticultural idiom and table furniture, the
  benign classes the M15 lettuce run anticipated: "as soon as the ground/soil can be
  worked" (37 hits), the calendar header row "feb mar apr may jun jul aug sep" (24), "1 to
  2 inches of water a/per week" (12), fertilizer conventions ("10 10 at 3 pounds per 100
  square"). These still need the benign-class RULING, not silence.
- By field: regions 92, watering 41, fertilizer 40, diseases 23, start_method 14,
  sources_summary 14, tips_by_stage 13. The sources_summary hits are a scan-scope question
  (backend-adjacent prose the collector currently includes) for the adjudication pass.
- Worst crops: strawberry 25, raspberry 11, asparagus 10, onion 10, cabbage 9,
  pickling-cucumber 8, shallot 8.

The 20 coverage-insufficient crops are blocked on the 99 unfetchable documents (WAF /
403 hosts). Per `url-liveness-is-not-a-status-code`, several will yield to the alternate
user agent; that retry belongs to the adjudication pass, not this session.

### Per-crop record (2026-08-10, canonical `060b91b8`)

| crop | compared | HARD | borderline | exit |
|---|---|---|---|---|
| strawberry | 31/34 | 25 | 50 | 1 |
| raspberry | 14/15 | 11 | 14 | 1 |
| asparagus | 37/41 | 10 | 18 | 1 |
| onion | 29/31 | 10 | 22 | 1 |
| cabbage | 37/38 | 9 | 8 | 1 |
| pickling-cucumber | 26/27 | 8 | 31 | 1 |
| shallot | 17/18 | 8 | 6 | 1 |
| echinacea | 9/9 | 7 | 12 | 1 |
| lime | 18/19 | 7 | 27 | 1 |
| mint | 25/26 | 7 | 10 | 1 |
| turnip | 39/43 | 7 | 17 | 1 |
| celery | 17/18 | 6 | 38 | 1 |
| cucumber | 24/26 | 6 | 29 | 1 |
| slicing-cucumber | 25/26 | 6 | 23 | 1 |
| sugar-snap-peas | 35/36 | 6 | 11 | 1 |
| yellow-summer-squash | 29/39 | 6 | 19 | 1 |
| zucchini-courgette | 28/39 | 6 | 19 | 1 |
| blackberry | 17/18 | 5 | 16 | 1 |
| bok-choy | 27/29 | 5 | 19 | 1 |
| cayenne-pepper | 38/39 | 5 | 33 | 1 |
| cherry-tomato | 76/94 | 5 | 85 | 1 |
| dry-bean | 25/27 | 5 | 37 | 1 |
| english-cucumber | 28/28 | 5 | 22 | 1 |
| fig | 15/16 | 5 | 8 | 1 |
| grape-tomato | 77/95 | 5 | 87 | 1 |
| habanero | 35/36 | 5 | 27 | 1 |
| jalapeno | 33/33 | 5 | 32 | 1 |
| roma-tomato | 74/92 | 5 | 90 | 1 |
| spring-onion | 13/13 | 5 | 9 | 1 |
| apricot | 20/24 | 4 | 9 | 1 |
| banana-pepper | 29/29 | 4 | 35 | 1 |
| bell-pepper | 30/30 | 4 | 28 | 1 |
| parsnip | 17/17 | 4 | 17 | 1 |
| pole-beans | 21/22 | 4 | 30 | 1 |
| potato | 24/25 | 4 | 39 | 1 |
| spinach | 36/40 | 4 | 8 | 1 |
| chives | 32/34 | 3 | 27 | 1 |
| edamame | 35/39 | 3 | 10 | 1 |
| eggplant | 29/29 | 3 | 28 | 1 |
| garlic | 20/21 | 3 | 14 | 1 |
| green-beans-bush | 24/25 | 3 | 35 | 1 |
| lemon | 32/33 | 3 | 28 | 1 |
| okra | 21/22 | 3 | 21 | 1 |
| pawpaw | 17/18 | 3 | 17 | 1 |
| pea-shoots | 5/5 | 3 | 4 | 1 |
| plum | 18/21 | 3 | 23 | 1 |
| pumpkin | 27/28 | 3 | 12 | 1 |
| watermelon | 23/24 | 3 | 12 | 1 |
| beefsteak-tomato | 67/82 | 2 | 79 | 1 |
| beet | 44/47 | 2 | 40 | 1 |
| blueberry | 41/45 | 2 | 40 | 1 |
| broad-beans-fava | 33/34 | 2 | 20 | 1 |
| brussels-sprouts | 33/34 | 2 | 42 | 1 |
| carrot | 39/43 | 2 | 20 | 1 |
| cauliflower | 35/36 | 2 | 10 | 1 |
| chamomile | 11/12 | 2 | 2 | 1 |
| cherry-sour | 20/24 | 2 | 7 | 1 |
| dill | 21/24 | 2 | 6 | 1 |
| heirloom-tomato | 70/84 | 2 | 80 | 1 |
| leek | 23/23 | 2 | 10 | 1 |
| lemongrass | 12/12 | 2 | 14 | 1 |
| lettuce-leaf | 87/92 | 2 | 66 | 1 |
| mandarin-clementine | 21/22 | 2 | 17 | 1 |
| parsley | 25/29 | 2 | 14 | 1 |
| popcorn | 23/24 | 2 | 10 | 1 |
| radish | 27/30 | 2 | 24 | 1 |
| rosemary | 15/16 | 2 | 5 | 1 |
| snow-peas | 35/36 | 2 | 14 | 1 |
| sweet-potato | 14/14 | 2 | 16 | 1 |
| thyme | 13/13 | 2 | 6 | 1 |
| arugula | 26/30 | 1 | 11 | 1 |
| arugula-microgreens | 4/4 | 1 | 4 | 1 |
| basil | 24/27 | 1 | 16 | 1 |
| broccoli-microgreens | 8/8 | 1 | 10 | 1 |
| calendula | 11/11 | 1 | 6 | 1 |
| cantaloupe | 22/23 | 1 | 14 | 1 |
| cilantro-microgreens | 9/9 | 1 | 5 | 1 |
| honeydew-melon | 27/28 | 1 | 20 | 1 |
| microgreens-mix | 3/4 | 1 | 4 | 1 |
| nectarine | 31/36 | 1 | 30 | 1 |
| pomegranate | 17/20 | 1 | 18 | 1 |
| radish-microgreens | 5/5 | 1 | 4 | 1 |
| sweet-alyssum | 11/11 | 1 | 3 | 1 |
| sweet-corn | 27/27 | 1 | 12 | 1 |
| acorn-squash | 26/26 | 0 | 14 | 0 |
| apple | 40/45 | 0 | 19 | 2 |
| artichoke | 25/26 | 0 | 34 | 2 |
| bee-balm | 8/8 | 0 | 5 | 0 |
| borage | 13/13 | 0 | 7 | 0 |
| broccoli | 29/29 | 0 | 12 | 0 |
| butternut-squash | 26/26 | 0 | 14 | 0 |
| cherry-sweet | 22/25 | 0 | 10 | 2 |
| cilantro-coriander | 23/26 | 0 | 9 | 2 |
| collards | 34/35 | 0 | 18 | 2 |
| cosmos | 15/15 | 0 | 1 | 0 |
| elderberry | 8/9 | 0 | 4 | 2 |
| field-corn | 27/28 | 0 | 12 | 2 |
| flint-corn | 28/29 | 0 | 13 | 2 |
| grapefruit | 20/22 | 0 | 6 | 2 |
| kale | 39/40 | 0 | 18 | 2 |
| kohlrabi | 26/26 | 0 | 15 | 0 |
| lavender | 27/27 | 0 | 14 | 0 |
| marigold | 13/13 | 0 | 10 | 0 |
| mulberry | 13/16 | 0 | 3 | 2 |
| nasturtium | 13/13 | 0 | 1 | 0 |
| orange-navel | 28/31 | 0 | 18 | 2 |
| oregano | 13/13 | 0 | 22 | 0 |
| peach | 31/36 | 0 | 30 | 2 |
| pear-asian | 28/32 | 0 | 17 | 2 |
| pear-european | 27/31 | 0 | 14 | 2 |
| persimmon | 17/20 | 0 | 9 | 2 |
| sage | 12/12 | 0 | 7 | 0 |
| spaghetti-squash | 26/26 | 0 | 14 | 0 |
| sunflower | 14/15 | 0 | 11 | 2 |
| sunflower-sprouts | 5/5 | 0 | 1 | 0 |
| sweet-pea | 9/10 | 0 | 2 | 2 |
| swiss-chard | 34/41 | 0 | 8 | 2 |
| tomatillo | 39/44 | 0 | 27 | 2 |
| viola | 10/10 | 0 | 6 | 0 |
| wheatgrass | 5/5 | 0 | 2 | 0 |
| zinnia | 17/17 | 0 | 3 | 0 |
