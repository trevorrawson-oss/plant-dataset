# PLA-199 -- source_catalog titles: the field, the backfill, the mint-time gate (2026-08-10)

Base canonical `060b91b8`. Post-state built and verified on a SCRATCH copy (sha `c16071bc`);
the live canonical is untouched pending Trevor's GO -- PLA-160 runs in parallel and Trevor
serializes the two promotes. Whichever lands second rebases onto the new SHA (this promote's
`BASE_SHA` preflight aborts on mismatch, which is the rebase tripwire).

## Rulings applied (the issue OVERRIDES the spec's D1 recommendation)

- **D1 (a)**: new optional `title` field, inserted directly after `name`. NOT the spec's
  "Pub ID (Title)" name convention -- that requires a tool to parse a parenthetical out of a
  string, the PLA-138 INSTANCE 1 shape rebuilt at the exact spot the fix targets, and any
  title containing parentheses breaks naive extraction. Two backfilled titles contain
  parentheses TODAY (`usu_washco_dates` "Planting Dates (Spring)", `ufifas_ae588`
  "Carrot (Daucus carota) Production..."), so the failure mode is not hypothetical.
  The two PLA-155 precedent entries (`vce_426_840`, `vce_spes_455`) migrated off the
  parenthetical: name keeps the id restatement, the title moves to the field.
- **D2 (b)**: document-scoped ids only. Institution roots stay bare -- no title to state.
- **D3 (a-after-backfill)**: hard gate A54, armed off the DATA (dormant while the catalog
  carries zero titles) so the shared checkout cannot red PLA-160's parallel gauntlet on
  unpromoted work. Once any title exists the gate is armed; the promote suite pins all 101.
- **D4 deferred**, stated plainly: this arc buys costs #1 and #2 (authoring-time visibility of
  what a document IS). It does NOT deliver cost #3 -- titles alone do not make ornamental/genre
  detection mechanical. Detection stays with D4.

## The denominator, stated before filling

208 catalog entries (the issue's 206 + the two PLA-155 mints). **153 document-scoped**
(pathed URL, the repo's own `BARE` test), 55 institution roots. Of the 153:

- **101 filled** -- title read off the cached document in `tools/.doc_cache` (sha1(url).txt),
  hand-transcribed entry by entry. No first-line heuristic, no extraction tooling: a mechanical
  title extractor is the proxy-for-reading defect this arc exists to kill.
- **52 unfilled, recorded with reasons**:
  - 50 have **no cached document** (enumerated in `promote_pla199_titles.UNFILLED`);
  - `unr_sp2007` -- cached body has no usable text layer (155-char extraction);
  - `lsu_agcenter_3363` -- cached text layer holds body prose but **no title line** (image
    cover). Its only candidate title would come from the URL filename, which is exactly the
    banned inference, so it stays honest-empty.

101 + 52 = 153, asserted both directions in the promote (hand-written lists vs the computed
document-scoped set) and re-asserted by promote guard G7 against the gate's exemption list.

## What the titles made visible (cost #2 firing during the backfill itself)

Four cached bodies diverge from what their catalog `name`/id claims. The title records what
the document actually IS; the `name`s were NOT changed (scope: no renaming of existing ids).
None of these was adjudicated here -- they are observations for a later pass:

1. `wsu_em051e` (id/name say EM051E): the cached body's masthead reads **EM057E** -- the same
   document `wsu_em057e` carries. Both now titled "Home Vegetable Gardening in Washington".
2. `ufifas_ae588` (name: "vegetable air-temperature growth ranges"): the cached body is
   **"Carrot (Daucus carota) Production in the Sandy Soils of North Florida: Nitrogen
   Fertilization Guidelines"**.
3. `uariz_ext_az1005` (name: "'Onions (Bulb)' low-desert planting calendar"): the cached body
   is the **Maricopa County vegetable planting calendar** (az1005), same document as `ua_az1005`.
4. `uc_costs_strawberry_sjv` (name says 2004): the cached body's cover reads **2005** Sample
   Costs to Produce Strawberries, San Joaquin Valley.

## A54 (tools/source_catalog_title_gate.py, wired into whole_crop_gate)

Three checks, every violation string naming A54 (the PLA-157 traceability rule): (1) a
document-scoped id outside the frozen 52-id `LEGACY_UNFILLED` exemption must carry a non-empty
string title; (2) an institution-root id must NOT carry one (D2 fabrication tripwire); (3) a
stale exemption (id retired or no longer document-scoped) flags until pruned. The list is
shrink-only.

TDD RED->GREEN both phases (module absent -> unit RED; unwired -> reachability RED through the
real `whole_crop_gate` runner on a sabotaged scratch). **Mutation sweep 7/7 caught**: each of
the three checks neutered, exemption-swallows-everything, blank-title check dropped,
permanently-dormant wiring, violation text losing the A54 name -- every mutation turned the
suite red; restored suite green (12/12, pytest + direct runner).

## Promote (tools/promote_pla199_titles.py) + guards

Titles-only: guard G1 proves every top-level subtree outside `source_catalog` BYTE-IDENTICAL,
G3 proves per-entry that nothing besides `title` (+ the two written-down name migrations)
moved. 9 guards, hand-written expectations (counts 208/153/55/101/52, both old and new
migration names, six spot titles re-transcribed in the test rather than imported). **Artifact
sabotage sweep 8/8 caught**: title-on-root, dropped entry key, moved crop byte, dropped title,
wrong migrated name, invented title on an uncached id, trailing newline, pretty-print.

## Gauntlet (scratch post-state)

- `whole_crop_gate` PASS x3 (cherry-tomato, strawberry, edamame) with A54 armed.
- Live canonical: A54 DORMANT, gate still PASS -- the parallel arc's gauntlet is unaffected.
- `gate_all` **121/121** on the post-state.
- `release_verify` post vs base: the only concern is its known single-crop shape
  (`crops changed = []` where it expects exactly one) -- this promote's footprint is
  legitimately ZERO crops, guard-proven byte-exact; `catalog +none -none`; dash scan clean.
- COMPACT preserved (guard G9: byte-equality with canonical-compact serialization, no
  trailing newline).
- Full tools suite: **966 passed** with A54 wired (the only 6 fails were this promote's own
  suite reading the pre-GO live file as post-state; it now SYNTHESIZES the post via the
  transform under test when the canonical is still at base -- guards' expectations stay
  hand-written -- and its on-disk byte check defers, loudly, to the landed promote). The
  shared tree is fully green for the parallel PLA-160 session.

## Not done, deliberately

- No refetch of the 50 uncached documents (a fetch pass is its own bounded task; titling them
  from ids in the meantime would be the defect).
- No adjudication of the four divergences above.
- No subject/genre tagging (D4).
- No promote to the live canonical, no commit -- stopped at the promote boundary per the
  kickoff; Trevor serializes with PLA-160.
