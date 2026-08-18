# PLA-161 -- the completion contract: predicates that refuse an unjustifiable ZERO and an unjustifiable COMPLETION

`76f92a20` -> `394bb8bd`. One promote, FINDINGS-ONLY: a single adjudicating declaration appended
to lemon. No citation repointed, no prose, no calendar, no catalog, no other crop touched.

Zeros and completions fail differently, and the completion is the more dangerous of the two,
because **a zero invites suspicion and a completion does not.** Nobody re-reads a line that says
the work is done.

---

## 0. The pre-build re-verification, which changed the build three ways

The issue was written 2026-08-06. Every number in it was re-measured before a line was written,
per the standing rule that a record is not the data it describes.

| Claim | Verdict |
|---|---|
| base `72284f02` | **STALE.** It is the canonical SHA of commit `3b222f8`; six promotes had landed since, and the issue's own SHA preflight would `sys.exit(1)`. |
| `blob()` reads a five-field list, `detail` does not exist, `basis` is the big miss | CONFIRMED (numerator `466,067` matched to the character at base) |
| campaign C table 97 SOLE / 196 MASKED, #17 = 0/18, #24 zero rows | CONFIRMED byte-identical |
| SELF-PATHED 315 bare / 152 SOLE | CONFIRMED (155 SOLE at `76f92a20`) |
| hunt #28 still bare and masked | CONFIRMED |
| `assert_absence_reportable` returns True for **zero** of 128 crops | **REFUTED. 58 of 128,** and 28 of those unjustified. The predicted failure had already arrived. |
| RED case lemon/`lsu_agcenter` | **REFUTED. A phantom** -- zero bare `lsu_agcenter` citations dataset-wide, and lemon never cites it, at `76f92a20` **and at the issue's own base**. Never constructible. |
| predicate 2 is unbuilt | **SUPERSEDED.** `tools/hunt_footprint.py` (PLA-187, `aee5aa3`) already shipped most of it, four days after this issue was filed. |

**The lesson that generalises.** The blind spot was recorded as latent, "protected today only by
cache incompleteness." That protection was a side effect of an unrelated deficiency, not a design
property, and completing the doc cache removed it. A gap whose safety depends on something else
staying broken is not latent, it is scheduled.

---

## 1. Predicate 1 -- `cited_urls()` widened

`cited_urls` walked `anchoring_urls` by exact key, so a source id named only in a `sources` /
`source_set` list could never reach `report.rows`, therefore never `report.uncached`, therefore
**the guard against reporting an absence over unread documents could not refuse over them.**

### The headline: justified versus unjustified zeros

|  | BEFORE | AFTER |
|---|---|---|
| guard returns "absence reportable" | 58 of 128 CROPS | 30 of 128 CROPS |
| **justified** | 30 (52%) | **30 (100%)** |
| **unjustified** | **28 (48%)** | **0** |
| documents enumerated roster-wide | 3,359 | 3,575 (+216) |

Zero crops newly pass; the widening is monotonic by construction. 58 -> 30 is **visibility
gained**, not defects introduced.

### The design finding that shaped it

**A source id is not a document.** cherry-tomato anchors `clemson_hgic` at six different
factsheets, and 366 (crop, id) pairs carry more than one URL. So the unit stays the URL, every
anchored URL is kept, and the catalog URL is added **only for ids the crop never anchors** (48
such ids, all 48 resolving). Deduping by source id would have collapsed those six documents into
one and shrunk the very denominator the guard protects.

`anchoring_urls_only()` is kept as THE WRONG METHOD, the way `proximity_band_hits` is.

### `umn_ext`: split, not fixed

`https://extension.umn.edu/vegetables` is **404 under both a browser and a urllib user-agent**.
The doc cache is recording that correctly; the defect is in `source_catalog['umn_ext'].url`, which
is canonical data. Counterfactual: **28 -> 8** if it resolved (`broccoli`, `eggplant`,
`english-cucumber`, `fig`, `kohlrabi`, `radish`, `sage`, `shallot` remain). Split to PLA-140.

**It also falsifies PLA-140's own heuristic.** That issue reasons a dead document 404s on the leaf
while the parent serves. `umn_ext` is the inverse: **parent dead, leaves serving** (crops anchor
working deep links like `extension.umn.edu/vegetables/growing-onions`).

---

## 2. Predicate 2 -- `tools/reporting_contract.py`, extracted and adopted

Extracted from `hunt_footprint`, not reimplemented. Inherits predicate 1's two design choices:
**every reason collected** (never return on the first), and `unguarded_completion_line` kept as the
wrong method for mutation testing.

Adopted in **campaigns B, C, D and `bare_host_scan`** -- everywhere, not only where the defect was
already visible, because adopting only at visible sites leaves the next `0 of N` unguarded.

```
C  BEFORE  HONEST OPEN after re-scope :  0 of 25 decisions,   0 of 68 nodes
   AFTER   COMPLETION REFUSED -- 39 masked-only DECISIONS (195 masked node-CITATIONS)

B  BEFORE  HONEST OPEN, document work :  0 of 33 decisions,   0 of 97 nodes
   AFTER   COMPLETION REFUSED -- 16 masked-only DECISIONS (28 masked node-CITATIONS)

D  BEFORE  HUNTS WITH NO SEARCH LEFT: 10 of 12
   AFTER   COMPLETION REFUSED -- 26 masked-only DECISIONS (116 node-CITATIONS); hunts
           #25, #26, #27, #28, #29 produced no rows and no reason was given
```

Residues are **re-derived live** from `hunt_footprint` on every run, never pinned: a stale constant
would put the contract back to sleep the moment the residue moved.

**Unit discipline, enforced in the predicate itself.** D's completion line counts HUNTS while its
residue counts DECISIONS, so `masked_unit` is separate from `unit`. Labelling the residue "hunts"
there would have been exactly the unit slide this arc keeps re-pricing itself with.

**195 versus 196**: both right. 196 is every masked citation in C's hunts; 195 is masked citations
on **masked-only** decisions, and a decision with even one SOLE row did enter a denominator. The
contract wants 195.

---

## 3. The sibling re-key -- additive, with the guard it forced

`sibling_leads(crops, slug, path, sid=None)` re-keys to same-path / **any**-id.
`pathed_by_sibling` delegates with a `sid` filter and **still drives the SIBLING-PATHED verdict on
the narrow key.** Campaign D closed on that join; folding the re-key in would re-price a closed
campaign as a side effect of a refactor. Measured and filed as its own issue rather than applied:
**6 -> 19 DECISIONS at the pin, 3 -> 12 live.**

**The replacement RED case, named before the test was written:** `lime` / `low_desert_az` / bare
`uariz_ext` at `regions.low_desert_az.resolved_by_zone.9`. Same-id join returns `[]`; grapefruit
cites `az_coop_ext` pathed at *Low Desert Citrus Varieties* at that same path. `uariz_ext` and
`az_coop_ext` are one institution under two id spellings, the trap PLA-187 recorded.

**Naming it surfaced a real bug.** `pathed_by_sibling` never checked that the SUBJECT was citrus.
Campaign D's SOLE nodes carry **15 non-citrus subject NODES over 5 crops**, and the re-key would
hand `edamame` (a legume) a citrus IPM page and a citrus variety collection. `sibling_set_for()`
guards it. **The issue's own "3 -> 38" was measured without that guard**; the correct live figure
is **3 -> 36 NODES / 12 DECISIONS**, the missing 2 nodes being edamame's.

---

## 4. SELF-PATHED, and `blob()`

**SELF-PATHED** (`bare_host_scan.self_pathed()`): **315 bare CITATIONS / 155 SOLE / 78 DECISIONS /
37 CROPS.** Masked rows included deliberately -- hunt #28 is masked, and filtering to SOLE would
rebuild the blind spot this issue removes. Still a LEAD, never a repoint.

**`blob()`** now serialises the whole finding rather than five enumerated fields. Enumerating is
what caused the defect: the list named `detail` (**0** findings) and omitted `basis` (**361**
findings, **88,392** chars). Whole-finding and the enumerated wide list agree on every triple, so
the simpler rule is provably not looser.

**Reach, stated so it cannot be over-claimed:** 45 TRIPLES / 38 PAIRS / 20 FINDINGS / 13 CROPS
newly visible, and **ZERO decision verdicts move in C or D at either SHA.** Overlap with C's
decisions is 0; with D's it is 1, already closed by another route. Where it bites is campaign A and
the masked residue -- arugula's `uc_mg` is hunts #9 and #11.

---

## 5. Hunt #28 -- refuted by the document, declared instead of repointed

The only sanctioned canonical change. Its own scope said read the document first.

`hgic.clemson.edu/cold-tolerance-in-citrus/`, read in full from cache (2,223-character body):

* mentions **"lemon" exactly once**, in a taxonomy list;
* publishes **one** temperature, 15F for satsuma, and names kumquat at about the same;
* contains **zero** occurrences of Gulf, Louisiana, Florida, Southeast, zone, container, wrap or
  cover; its only protection guidance is to protect the **graft union**.

The node claims a high-20s F lemon damage threshold and `survives_no_fruit` at zone 8. Neither is
in the document. **And this crop's own certification record had already ruled it**: the resolved
finding `lemon_cold_threshold_was_miscredited_now_uc8100` states "Clemson's cold-tolerance page
publishes satsuma and kumquat at 15F and no lemon number."

Repointing would have credited the document with a figure the dataset had already adjudicated it
does not publish. **CASE 2.** The declaration mirrors hunt #31's warm_arid precedent key-for-key
(`id, severity, status, blocks_launch, filed_in_session, summary`), and the citation is **left BARE
by design** so the record of examination survives a future scan.

---

## 6. Two corrections against myself

Recorded because this issue is about counts that cannot show their warrant.

1. **"94 SELF-PATHED decisions"** was my own keying artifact -- I used the full node path as a
   region surrogate for crop-level nodes. The issue's **78** is right (72 region-scoped + 6
   crop-level buckets).
2. **"The cohort guard is not load-bearing here"** was FALSE, and a green suite would never have
   said so. Diffing the original walk against the delegation: **0 differences over campaign D's
   real nodes**, but **468 at the pin / 117 live** over a synthetic cross product, every one a
   non-citrus subject. The guard is load-bearing, merely unreachable from real campaign input.

A green suite proves "no assertion I wrote is violated," never "behaviour is unchanged."

---

## 7. Gauntlet

* TDD RED -> GREEN throughout: predicate 1 (5 RED), re-key (4 RED), SELF-PATHED (7 RED), blob
  (2 RED), promote (7 RED).
* `whole_crop_gate lemon` **PASS**; `gate_all` **121/121**.
* `release_verify` 16 concerns, **all proven PRE-EXISTING base-vs-base, zero new**. The one
  differing line is its collateral check correctly confirming exactly lemon changed.
* Source-truth sample **9/9** assertions verified against the cached document and canonical.
* Full `pytest tools/` **1082 passed, 1 skipped**. COMPACT preserved.
* Promote sabotages caught: wrong base SHA, node no longer bare, double-file.
* Blast radius asserted **both directions**, so an ADDITION cannot hide.

**Disclosure:** `reporting_contract.py` and its tests were written together, so there was no RED
phase for the module itself. The genuine RED was the live tool output, reproduced before building
and changed by adoption.
