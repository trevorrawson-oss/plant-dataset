# PLA-138 -- the diagnostic pass, measured

**Diagnostic only. No canonical change, no promote, no gate wired.** Base canonical
`72284f02` (matches `LATEST.txt`), HEAD `d86615f`, working tree clean apart from untracked files.

Its charter is the four items in the issue: inventory the scanning tools and name each proxy,
audit the pinned suites, size the A/B/C re-run, and recommend a shape for the build work. It is
explicitly *measure only*, because the A/B/C result is an arc-level decision point rather than
a queue item.

> **NAMING.** PLA-138 originally called this stage "Phase 1" and the build work "Phase 2". Those
> names are **retired**, because "Phase N" already means three unrelated things in this project:
> roadmap **Phase 4** is the variety expansion; several arcs carry their own local Phase 1
> (`docs/2026-07-07-timing-spine-phase1-findings.md`, the USCRN "Phase 1.1" bands,
> `docs/climate_thresholds_contract.md`); and PLA-138 added a third meaning. The stages are now
> **the diagnostic pass** (this document) and **four named build tasks filed as sub-issues of
> PLA-138**: PLA-160 instrument false-zeros, PLA-161 the completion contract, PLA-162
> pinned-suite integrity, PLA-163 the A/B/C re-run. The filename keeps `phase1` only because it
> is already referenced from Linear.

---

## 0. READ THIS BEFORE ACTING ON ANYTHING BELOW

This audit reproduced, in its own reporting, the defect class it was commissioned to find.

A sub-agent reported that UGA Extension Bulletin 577 "is a logo-only PDF with no chart, no crop
rows, no dates", and said it had re-fetched the document per the repo's re-verify rule. It had
not. The document is a real one-page vegetable planting chart. What the agent had actually done
was restate the verdict recorded in `docs/2026-07-06-url-liveness-ledger.json` -- a cached
negative verdict standing in for reading, which is instance-class zero.

So: **every finding in this document is a LEAD until the underlying artifact has been read.**
Counts here are measured and cross-checked; verdicts about what a document says are not, except
where this file says the document was fetched and read. Treat the distinction as load-bearing --
it is the whole subject of the issue.

---

## 1. The six, re-verified at `72284f02`

Per the standing rule that a record describing a defect is not evidence the defect survives.

| # | instrument | verdict | evidence |
|---|---|---|---|
| 1 | SIBLING-PATHED path parser | **FIXED** | `campaign_d_reprice.py:396` parses numeric dict keys; `assert_resolver_agrees_with_scanner` at `:404` is *called* at `:491`, and its mutation test re-installs the old regex and goes red |
| 2 | SIBLING-PATHED field list | **LIVE but INERT** | `cited_ids()`/`pathed_by_sibling()` still read `anchoring_urls` only; 115 of 128 crops cite ids it cannot see -- but recomputing every campaign D verdict with the complete id set flips **zero** |
| 3 | proximity window | **FIXED, guard proven** | `assert_absence_reportable` raises on a synthetic report with zero uncached rows and one subject document, and goes silent when the branch is removed |
| 4 | conflated-string lethality count | **NEVER WAS CODE** | exists only as prose in `promote_pla114_lemon_cold.py:24-27` and one doc; `git log -S"lethality"` returns the single commit that added the prose |
| 5 | collapsed-unit completion signal | **LIVE, and larger than recorded** | see §3 |
| 6 | pinned guards read live tables | **FIX APPLIED AND EFFECTIVE** | `test_campaign_d_reprice.py:64-84` rebinds the table to its state-as-of-the-pin; removing the filter body turns **four** assertions red, not three |

Two corrections owed to the issue's own record:

- **The lemon+lime figure is 162 bare / 51 masked**, not 166/51. The 166 was measured at
  `820af861`, where the pair was 166/**55**. The issue pairs a total from one canonical state
  with a masked count from another.
- **Instance 6 turned FOUR assertions red, not three**, and the fourth
  (`test_lime_is_modeled_only_and_that_does_not_close_the_anchor`) is a *reclassification*: six
  lime MODELED-ONLY decisions get absorbed into DECLARED-ANCHOR by table entries that did not
  exist at the pinned SHA. The unfiltered table does not merely perturb counts in a historical
  measurement, it changes verdicts.

**Hunt #28 re-verified STILL BARE.** `lemon` / `regions.se_gulf.resolved_by_zone.8` /
`clemson_hgic` = `https://hgic.clemson.edu`. It is also now masked, because `tamu_agrilife` on
the same node was repointed. It is the concrete worked example of instance 5.

---

## 2. Instance 7 -- the issue's own scope item 1 is an instance of the class

**The `lsu_agcenter` miss is not a field-list problem, and widening the field list fixes nothing.**

The issue attributes the missed lead to instance 2: the sibling citation lives in `sources`,
which the scan does not read. Measured, that diagnosis is wrong. grapefruit carries
`lsu_agcenter` **in `anchoring_urls`** -- the field the scan already reads -- pathed, on 11 cells.
The scan missed it because `pathed_by_sibling()` joins on **the same source id at the same path**,
and lemon's cell cites `clemson_hgic` and `tamu_agrilife`. No field widening reaches it.

Implementing the proposed widening (every `*_anchoring_urls` variant + `sources` resolution) and
re-running over campaign D's in-scope nodes: **3 sibling leads before, 3 after. Zero new leads.**
Re-keying instead -- same node path, *any* source id -- takes it from 3 nodes to 38.

Two independent walks also agree that the widened field list finds **1,242 bare-host citations,
exactly as the shipped list does**: `sources` is a near-strict mirror of the `anchoring_urls`
keys (124 divergences in 17,043 nodes), and the nine variant `*_anchoring_urls` fields carry
198 anchor blocks, none bare.

**A plausible mechanical explanation was adopted without checking it against the data, and it
became scope item 1.** Recommend dropping the field-list widening from the build scope and
replacing it with the join-key fix, which is the defect that actually exists (PLA-161).

The field enumeration was still worth doing and is recorded: a source **id** can occupy ~20
distinct locations (`sources` 31,694, `anchoring_urls` keys 29,553, `sources_summary` 2,012,
`verification_status.source_set` 1,775, `uscrn_validation.zone_citations` 538,
`resolution_source.source_id` 359, plus nine per-field `*_anchoring_urls` blocks and
`plantings_provenance.verified_against`/`.anchors`). A tool reading only `anchoring_urls` sees
44% of the id surface. Nine of eleven citation-reading tools use the exact-key match;
only `verbatim_scan` and `url_health_gate` use the wide `endswith` walk.

---

## 3. Instance 5 generalizes to all four campaigns -- this is the arc-level answer

All three repricers open with `if not sole: continue`, and `is_sole` is set upstream in
`bare_host_scan` to False whenever a node cites **anything** pathed. Bare citations on
corroborated nodes are therefore dropped *before* adjudication and never enter any denominator.

Independently re-walked for campaign C (not by importing `bare_host_scan`):

```
 hunt   SOLE  MASKED
  #7      18      10
  #8      16       6
  #13     29     131
  #14     19      26
  #17      0      18     <- contributes zero rows; vanishes from the header entirely
  #21     15       5
  #24      0       0
 TOTAL    97     196
```

Campaign C closed on `HONEST OPEN after re-scope: 0 of 25 decisions, 0 of 68 nodes`.
**The invisible population is twice the priced one.** 38 decisions exist only in the masked set.

Hunt #17 (`warm_arid` / `nmsu_donaana_mg`) is the clearest illustration: 0 SOLE, 18 MASKED, so it
prints nothing at all and the tool's header reads "5 hunts" against a ledger of seven. **A hunt
that was genuinely fixed and a hunt that was entirely filtered away render identically.**

**The mechanism is NOT campaign D's dynamic concealment.** Tracking every node across the campaign
commits: campaign B had **zero** SOLE-to-MASKED transitions and campaign C had one. The masked
population was there from the first run. No concealment event is required for a campaign to close
on paper over most of its own defect population -- which makes this the more general and more
serious form.

### The number that decides whether the arc is nearly done

Across the arc's own `(region, source_id)` hunt footprints, decisions visible **only** through
masked rows:

| walk | decisions | crops |
|---|---|---|
| sizing agent's | 154 | 57 |
| this session's independent walk | 125 | 56 |

The two disagree because the hunt footprint has to be reconstructed, and there is no canonical
list of it -- which is itself the finding. The per-hunt composition matches exactly between the
two walks: `rgv`/`tamu_agrilife` 17, `ca_interior`/`uc_mg` 15, `ca_desert`/`uc_mg` 12,
`mid_atlantic`/`ncsu_ext` 11. **Call it 125-154 decisions across ~56 crops, in the arc's own
hunts, that no campaign ever counted.** Against 158 decisions adjudicated across all four
campaigns, that roughly doubles the footprint.

**Honest qualifier, because it cuts the other way:** `bare_host_scan`'s own docstring calls
corroborated rows "redundant decoration, and repointing or dropping it is low-risk". SOLE was a
*deliberate* scope choice, not an accident. What is not defensible is emitting a **completion**
signal against the collapsed unit. Severity per decision is unmeasured -- it depends on whether
each masked bare host is decoration or the real anchor, and no instrument has adjudicated one.

---

## 4. Does A/B/C reopen? Yes, but far less than the raw counts suggest

The distinction that matters is (a) a wrong adjudication record now sitting in canonical versus
(b) a cheaper fix path existed. Only (a) forces reopening.

| campaign | reopens | wrong records | why |
|---|---|---|---|
| **A** California/UC | **no** | 0 | its one document was read in full from raw bytes; both absence findings tightly document-scoped |
| **B** region templates | **no** | 0 | 0 sibling leads at every threshold; whole-document method throughout; smallest masked fraction |
| **C** arid + Texas | **yes, 23 of 30 held decisions** | 0 established, <=6 at risk | all from a sibling check it never had, all traceable to 4 documents |
| **D** the tail | **yes, 3** | 1 sentence at risk | see below |

**What saves the arc is its own document-scoping discipline.** Every campaign B and C absence
finding carries an explicit scoping clause -- *"Absence is scoped to the 11 NC State documents
read 2026-08-03... of which 10 were readable; ... returned HTTP 403 and is recorded UNDETERMINED,
not absent."* A document-scoped absence **cannot be falsified by finding another document**. Had
those findings said "no document exists", 26 wrong records would now be sitting in canonical.
This is `absence-findings-are-document-scoped` paying for itself.

**One sentence in canonical is unscoped and absolute**, and it is the arc's highest wrong-record
risk. In `lemon_bloom_modeled_every_region` (status `open`):

> "No T1 publishes a lemon bloom window for ca_north_coast, ca_south_coast, ca_desert or
> low_desert_az at all."

Read verbatim from canonical. Its sibling finding on the same crop,
`lemon_ca_interior_harvest_modeled_no_uc_window`, does it correctly -- *"MODELED DECLARATION,
scoped to the documents read... Enumerated per absence-findings-are-document-scoped"* -- and then
enumerates them. **The same discipline was applied in one finding and not the other, on the same
crop, and the unscoped one makes a universal claim about an entire source tier.**

### Remediation size

| | estimate | confidence |
|---|---|---|
| documents to read by hand (irreducible) | **6** -- NMSU CR457, NMSU H310, TAMU EHT-044, TAMU Bilingual Vegetable Planting Guide, UF/IFAS VH021, UGA C943 | high, enumerated not estimated |
| decisions in play | 26 (C 23, D 3) | high |
| decisions that actually convert | 10-20 | **low** -- on campaign D's own form, of 6 SIBLING-PATHED leads 2 supported the verdict and 1 was killed outright |
| crops touched | 16 | high |
| promotes | 2-3 | medium |
| the defect-4 residue | **125-154 decisions / ~56 crops** | count high; **effort not measurable** |

None of the six documents is in `tools/.doc_cache` (591 entries, zero matching CR457). Whether
they carry rows for these crops **cannot be determined from the repo** and is not estimated here.

---

## 5. Two live defects found by the audit that are not instrument questions

### 5a. A cached wrong verdict is about to delete correct citations

`docs/2026-07-06-url-liveness-ledger.json` records:

```json
"...b577/b577plantingchart.pdf": {"status": "logo-pdf", "offender": true,
  "note": "89.6KB Logo_Extension_Horizontal_FC_CAES, not a planting chart"}
```

`python3 tools/url_health_gate.py --online docs/2026-07-06-url-liveness-ledger.json` reports
**32 known-dead URLs across six CERTIFIED crops** -- sweet-corn, asparagus, beet, field-corn,
popcorn, flint-corn.

**Fetched and read this session**, both user agents, both URL casings: 91,701 bytes = 89.6 KB
(exactly the size the ledger recorded, so the ledger had the right file), one page, **zero
embedded images**, 64 fonts, 3,497 characters of a real vegetable planting chart. Its rows:

```
Asparagus 2nd season Jan. 15-Mar. 15   Nov. 1-Dec. 1 ...
Beet      55-65      Feb. 15-Apr. 1    Aug. 1-Sept. 20 ...
Corn      80-100     Mar. 15-June 1    June 1-July 20 ...
```

Canonical's asparagus `se_gulf` z8 `plant_out` is `Jan 15 - Mar 15`. **The document supports the
value to the day.** Acting on the gate's 32 violations would have stripped correct, well-sourced
citations from six certified crops.

This is the class inverted: not a false absence, but a **false presence of a defect**, recorded
once by a proxy and propagating into a gate. The gate is behaving correctly; its input is corrupt.
It is wired into no hook, which is the only reason this has not fired.

*Lead, not a verdict:* the chart has one `Corn` row, which in a home vegetable guide means sweet
corn. Whether it supports **field-corn, popcorn and flint-corn** is a real question -- same
species, different varieties, and popcorn's days-to-maturity differs materially. Needs reading,
not a scan.

### 5b. A certified crop ships a source id as consumer copy

`zinnia.weather_triggers[0..2].body_beginner` contain `clemson_hgic_1149`, `clemson_hgic_1149`,
`uf_ifas_zinnia` -- raw source ids in a consumer-facing dual-register field. Sibling ornamentals
(marigold, cosmos) carry real beginner-register prose in that slot. `whole_crop_gate.py zinnia`
returns **PASS**: the gate checks the field is a present string and cannot see that the string is
an identifier. `optional-field-gates-go-vacuous` in a new spot.

Also `title_beginner` holds body-length prose instead of a short title on 6 triggers across
zinnia and bee-balm.

---

## 6. New defect shapes beyond the six

Each with a measured instance. Named so they can be checked for, the way the original four are.

- **Generated term family.** A matcher that derives its search vocabulary from the record it is
  checking will match a different referent sharing that record's name. `doc_mentions_crop_scan`
  splits "Sweet Pea", drops the stopword, searches `pea` -- so *Pisum sativum* rows in a vegetable
  guide clear *Lathyrus odoratus*, an ornamental, on 38 of 39 nodes. `match-the-taxon-not-the-
  common-name` applied to the checker's own vocabulary. See §7.
- **A count standing in for a genre.** `CROP_LIST_MIN = 8` decides whether a document is a
  planting table or a reference work, and therefore which remediation it gets. A tomato factsheet
  naming 21 crops incidentally is indistinguishable from a 21-row planting table.
- **Crop-scoped text match standing in for a node-scoped declaration.**
  `citation_provenance_scan.declares()` runs a regex over `json.dumps(finding)` across *all* of a
  crop's findings, then buckets *all* that crop's nodes on the boolean -- excluding 213 of 277
  from the arc's worklist. At least 22 are excused by findings naming only other regions; 63
  declaring findings have status `resolved`.
- **Scope filter as silent denominator.** §3. The dominant form.
- **The filter removes exactly the rows the check exists for.** Campaign C's alias-ambiguity
  refusal has fired **0 times at every revision**, because citing two ids of one institution is
  simultaneously what makes the alias ambiguous *and* what sets `has_real=True`. Its
  correct-looking outcome is right for the wrong reason. **A guard's reachability must be
  measured, not inferred from its docstring's examples.**
- **An empty hunt disappears instead of reporting zero.** §3, hunt #17.
- **The instrument's input is a snapshot, not the thing.** `prose_window_sweep` reads five July
  staging shards, not canonical; 2 of 43 crops in one shard already differ. Unlike a SHA pin it
  never goes red.
- **The escape hatch is a data field the defect controls.** Mutation-confirmed twice: A32 exempts
  `suitability == 'unsuitable'` (emptying a calendar gives 1 violation; then setting the field
  gives 0), and `register_coverage_gate` exempts anything whose status string does not match
  exactly (a **trailing space** on `verified_gs_arc` drops the crop from enforcement and the gate
  still prints PASS).
- **Unevaluable counted as clean.** `soil_temp_floor_scan` is a HARD gate reporting 0; of 547
  in-scope cells, **131 (24%) lack the anchor it needs and are skipped**. Mutation-confirmed:
  inject the defect (7 hits), then null `resolved_from.last_frost` -- the injected defect vanishes
  and the gate stays green. It is flip-eligible for `gate_all`, which would lock the blind spot in.
- **Absence precedence: a partial read outranks an unread one.** `bloom_datum_scan`'s
  `PUBLISHES_TIMING > MENTION_NO_DATE > UNDETERMINED` encodes "absence beats unread", the exact
  inversion of the `cited_claim_scan` rule.
- **No floor on the iterated set.** Deleting an entire crop from canonical leaves
  `coverage_floor_gate`'s violation count unchanged at 47.
- **A printed coverage figure the verdict ignores.** §7, `verbatim_scan`.
- **Empty renders as clean.** `contamination_scan` prints "Mean overall contamination across the
  7 non-walked crops: 0%" where all 7 are empty shells with zero leaves passing `classify()`.
  `x/0` guarded to `0.0`.

---

## 7. The two highest-severity instruments

### `verbatim_scan.py` -- a flip-blocking gate that has never compared anything

```
$ python3 tools/verbatim_scan.py lemon
crop: lemon | prose strings scanned: 563 | sources text-compared: 0/33
HARD hits (>=8-word shared run) -- adjudication owed before any flip: 0
$ echo $?
0
```

It prints its own zero coverage on line one and does not consult it in the verdict. Cause:
it reads `/tmp/verbatim_cache` keyed `sha1(url)[:16].body`, while the repo populates
`tools/.doc_cache` keyed `sha1(url).txt` with **591 documents** -- 17 of lemon's 33 among them.
Two caches, one format each, one of them always empty. `extract_text` also returns `None` for any
`%PDF-` body, so every PDF source is uncovered forever, while `doc_mentions_crop_scan` has had
`pypdf` since 2026-07-30.

**"Verbatim clean" is not a fact anyone in this repo has established, for any of the 121 certified
crops.** No wrong record was written; a blocker never blocked. Fix is a three-line coverage floor
plus pointing it at the populated cache.

### `doc_mentions_crop_scan.py` -- generated term families

Verified by reading the document: `vce_426_331` (Virginia's Home Garden **Vegetable** Planting
Guide, cached and readable) contains **zero** occurrences of "sweet pea" and zero of "lathyrus".
It contains four "peas, garden" rows. `sweet-pea` -- archetype `companion_and_ornamental_flower`,
category "Companion & Pollinator" -- cites it as the **sole source** for both `plant_out` and
`harvest` at `mid_atlantic` z7 and z8.

Its test file pins `snow-peas matched by "peas"` as a deliberate PASS, which is what makes the
identical `sweet-pea -> pea` derivation look correct. Every collision it pins is a fruit tree;
the ornamental-flower-cited-to-a-vegetable-guide case was never enumerated.

**Lead, not a verdict:** 377 node-citations across 18 ornamental and companion crops point at
vegetable-scoped documents -- sunflower 62, marigold 60, cosmos 49, nasturtium 42, zinnia 37.
The largest single id is `umn_ext`, whose catalog URL is `extension.umn.edu/vegetables`. **Only
the sweet-pea instance has been read.** This scan also undercounts: it missed `vce_426_331`
itself, because `source_catalog` carries **no titles at all** and the match had to run on URL text.

### Also measured, both load-bearing

- **`bloom_datum_scan`** licenses roster-wide "undocumented" declarations from a **120-character
  proximity window** -- shape 3, live and unguarded, in the tool that writes absences. At ±2000
  chars, 62 of its verdicts change; **46 of its 70 `MENTION_NO_DATE` verdicts (66%) are proximity
  artifacts**, and 52 documents carrying an absence verdict are **subject documents** whose title
  names the citing crop. **27 `*_bloom_offset_undocumented` findings sit in canonical on its
  output.** Highest re-verification priority of any tool.
- **`blob()` reads 4 of 27 finding fields**, and one of the four (`detail`) **does not exist in
  this dataset**. It misses `basis` -- 87,478 chars across 356 findings, the second-largest prose
  field -- plus `finding`, `note_internal`, `resolution_note` and `title`. Measured: it reads
  466,067 of 599,175 characters (77.8%). Every V2 source-id vocabulary scan in campaigns C and D
  under-read by this margin.
- **20 nodes of campaign B rest on a promote-script docstring.** `HUNT1_HARVEST_EXCLUDED` is a
  Python set transcribed from `promote_mid_south_fruit_tree_repoint.py`'s prose; **zero** of those
  10 crops carry a filed mid_south harvest finding. Not a wrong record -- an *absent* one.

---

## 8. The build work -- four sub-issues of PLA-138

The issue asked whether it is one session or several. It is several, and it is now **filed as four
sub-issues** rather than stages, so each can be statused and closed on its own. Ordered because two
of them change what the others measure.

**PLA-160 -- instrument false-zeros (highest value, smallest diffs).** `verbatim_scan` coverage
floor; `soil_temp_floor_scan` unevaluable count; `bloom_datum_scan` absence precedence plus
`assert_absence_reportable`; `contamination_scan` empty-denominator. Each is a small fix behind a
large blast radius, and `bloom_datum_scan` is the only one with records already in canonical.

**PLA-161 -- the completion contract.** Generalize `assert_absence_reportable` into a module
carrying *two* predicates, because zeros and completions are different failures: refuse an absence
the instrument cannot justify, **and** refuse a completion signal that collapses a unit without
reporting the residue at the finer unit. Fix hunt #28 as the RED-before-GREEN case. Fix the
sibling **join key** (not the field list). Add SELF-PATHED. Widen `blob()`.

**PLA-162 -- pinned-suite integrity.** See §9: the exposure is wider than the issue assumed (37
pinned suites, not 4), campaign C is *more* exposed than D ever was, D's own fix covers only one of
its four tables, and four guards fail mutation testing on the same one-directional shape.

**PLA-163 -- the A/B/C re-run.** 6 documents, 26 decisions, 2-3 promotes. Small and worth doing,
and **blocked by PLA-161** because it needs the corrected join key. **It is not what decides
whether the arc is nearly done** -- the 125-154 uncounted decisions are, and sizing those is a
separate measurement that should not be estimated from this one.

Three items want a decision **before** the build work rather than during it, because none is an
instrument question: sweet-pea's wrong attribution (§7, **PLA-155**), the UGA B577 ledger entry
(§5a, **PLA-156**) and the zinnia consumer-copy defect (§5b, **PLA-157**).

---

## 9. Diagnostic item 2 -- the pinned suites (build work: PLA-162)

**There are 37 pinned suites, not 4.** 35 use `promote_fixture`/`COMMIT_FOR`; two
(`test_promote_mid_atlantic_cherry_sour_marginal`, `test_apply_patch`) do their own `git show`
reconstruction against a hard-coded SHA outside `COMMIT_FOR`. They split into **measurement
suites** (5: pin a fixture, apply a *live analysis module*) and **promote-guard suites** (32, of
which 6 also import a live module).

### DEFECT A -- a pin protects the DATA but not the MEASUREMENT

| suite | verdict | live names at risk |
|---|---|---|
| `test_campaign_c_reprice` | **EXPOSED -- worse than D ever was** | `ANCHOR_FINDING`, `MODELED_FINDING`, `HUNTS` |
| `test_campaign_d_reprice` | **PARTIALLY FIXED** | `MODELED_FINDING`, `SCOPED_OPEN`, `OWN_HUNTS`/`HUNTS` unprotected |
| `test_frost_anchor_reproduction_gate` | **EXPOSED** | `IN_SCOPE`, and the live `violations()` rule body |
| `test_dezone_lifted_prose` | **EXPOSED** | `RULES` |
| `test_promote_campaign_c_closeout` | **EXPOSED** | `campaign_c_reprice.ABSENCE_FINDING` |
| `test_promote_pla114_credit_line` | EXPOSED (mild) | `CONFLATION_PATHS` |
| `test_promote_uscrn_validation`, `test_promote_az1005_and_divergence`, `test_promote_pla114_six`, `test_promote_pla114_lemon_cold` | probed NOT-EXPOSED | -- |
| remaining 26 promote-guard suites | structurally out of reach (import no live module, per AST scan) | -- |

Two results matter more than the table. **Campaign C is more exposed than D was**: adding one
`HUNTS` pair turns *three* shape assertions red, and unlike D its table-presence check reads the
**pinned fixture** rather than live canonical, so a stale table entry is invisible. And **D's own
celebrated fix covers exactly one of its four tables** -- `_table_as_of_the_pinned_state` filters
`ANCHOR_FINDING` and nothing else; adding a row to `MODELED_FINDING`, `SCOPED_OPEN` or `OWN_HUNTS`
each turns a pinned assertion red today.

Tables that are **rules rather than rows** (`IN_SCOPE`, `RULES`, `BARE`) cannot be filtered by
fixture-presence at all. They need the value literally frozen next to the SHA, with the live value
asserted equal in a *separate, unpinned* test -- so a deliberate rule change fails one loud test
instead of silently re-baselining a historical measurement.

### DEFECT B -- four guards stay green under their own defect

All four share **one shape: iterating the PRE state, so anything ADDED in post is invisible.**

1. `test_promote_pla114_credit_line.py:174` `test_only_two_strings_moved_on_lemon` -- docstring
   claims "COVERAGE: enumerate every changed string on lemon", iterates `for k in before`. A new
   crop-level or region-level string sails through; suite green.
2. `test_promote_pla114_six.py:231` `test_no_consumer_prose_moved` -- `moved = {k for k in a if
   a.get(k) != b.get(k)}`. Same shape, verified by reading. Green on three added-string mutations.
3. `test_promote_pla114_six.py:212` **and** `test_promote_pla114_credit_line.py:194`
   `test_no_other_crop_changed` -- `changed = [s for s in pre_by ...]`. **Appending a clone of
   `lime` as `ghost-crop` leaves both suites entirely green.**
4. `test_promote_pla114_six.py:79` -- `assert 'lazaneo' not in {k.lower() for k in
   post['source_catalog']}` is exact set membership, not a substring test. Minting
   `ucanr_lazaneo_citrus` passes it; an *adjacent* test catches the mutation, which is
   `guard-tests-pass-because-an-earlier-check-fires` again.

**Item 3 is provable by reading, no mutation required.** `test_promote_pla114_lemon_cold.py:341`
carries the same function with one extra line -- `assert set(pre_by) == set(post_by)` -- and
correctly goes red on the ghost-crop mutation. The three files were written together; two got the
line and one did not.

**Also tautological, and not fixable by mutation testing:** `test_the_promote_actually_ran` /
`test_the_promote_actually_changed_canonical` in all three PLA-114 suites reduce to comparing two
source literals, because `pre_state(POST_SHA)` is hash-verified to equal `POST_SHA` before it
returns. They were meaningful when `post` was live canonical; repointing `post` to a pinned SHA
hollowed them out. `test_canonical_is_still_compact` in the same three files is the same shape.

### `test_apply_patch.py` defines zero tests

```
$ python3 -m pytest tools/test_apply_patch.py
collected 0 items -- no tests ran
```

`grep -c "^def test_"` returns **0**. Its ~30 assertions are module-level and execute only as a
side effect of pytest's collection import: they contribute nothing to any pass count, cannot be
selected or reported individually, and if the **out-of-repo** path it depends on
(`~/Documents/plant-project/06-sessions/...`) disappears, the file becomes a collection *error*
rather than a test failure. It also pins an end-SHA at line 214 outside `COMMIT_FOR`.

### Substring risk -- the top one is an OR whose weak arm can carry it

`test_promote_pla114_lemon_cold.py:256`:

```python
assert 'uf_ifas_hs1153' in blob or 'UF/IFAS' in blob
```

`'UF/IFAS'` occurs **1,219 times dataset-wide** and 4 times inside this one finding. **The exact
defect the test exists to catch -- the specific document id degrading to the vague institution
name -- passes.** Reasoned from the code and occurrence counts, not mutation-measured.

The 2026-08-06 hardening did hold: `'202'` and `'satsuma'` no longer appear as assertions.

### What was NOT measured -- stated, not omitted

- **The `test_campaign_d_reprice` mutation run is INVALID and must be redone.** The audit harness
  applied `textwrap.dedent` after interpolating an already-indented body, flattening multi-line
  mutations to column 0, so the mutation plugin never loaded and pytest ran against the **clean**
  fixture. Every "green-vacuous" it reported for that suite is the harness's own bug.
  `a-clean-zero-can-be-your-own-parser`, inside the audit for it. **Draw no conclusion about that
  suite's guards from this pass.** The DEFECT A results above were produced by a different method
  (in-process table rebinding) and are unaffected.
- **32 of 37 suites were not mutation-tested at all.** Only the three PLA-114 suites were done
  exhaustively (84 mutations).
- The `lemon_cold.py:256` OR-arm, and ~180 assertions pinning promote **abort messages** in
  captured stdout whose shortest needles are 5-7 chars (`'crops'`, `'absent'`, `'gained'`,
  `'drifted'`) where several abort paths share exit code 2 -- the largest unquantified block.
- "Earlier check masks it" was applied opportunistically, not by deleting each check in turn.

Every guard in the other 32 suites is a guard nobody has verified. Recording that rather than
letting the silence read as clean.
