# PLA-155 promote -- the vce_426_331 credit corrections (`ce9eb12f` -> `4f610318`)

ONE promote, 7 crops, citations + anchors + findings + four synthesis-note pub-number strings.
ZERO consumer-facing values move (guard G8 enumerates every changed leaf path and requires a
citation-layer suffix). Classification evidence:
`docs/2026-08-10-pla155-vce-426-331-classification.md`. Script `tools/promote_pla155_vce.py`,
guards `tools/test_promote_pla155_vce.py`.

## The edits

| crop | what moved | why |
| -- | -- | -- |
| sweet-pea | ncsu_ext (Lathyrus toolbox page) ADDED beside vce_426_331 on region + z7/z8; analog registered as accepted_modeled finding | the SOLE credit was the defect; the declared analog, the frost table, and the "no fall sowing" claim are document-true, and harvest = start_indoors + 85d is the crop's own certified days-to-bloom |
| strawberry | vce_426_331 -> vce_426_840 on region, z7 cell, plantings container, 4 rule-layer arms + their synthesis-note pub numbers; divergence finding OPEN | wrong pub number: the attributed matted-row/renovation content is in 426-840, absent from 426-331; plant-offset (2wk vs 3-4wk) and harvest offsets stay unmoved, filed |
| blueberry | vce_426_331 -> vce_426_840 (region, container, z7/z8) + finding | 426-840 publishes the blueberry planting-season statement; 426-331 has zero blueberry content |
| raspberry, blackberry | same swap + finding each | 426-840 publishes the caneberry planting-season statement; December opening noted as the dormant-season reading, not a stated date |
| elderberry | vce_426_331 REMOVED (region, container, z7/z8) + finding | 0 elderberry in 426-331 AND 426-840; mirrors the accepted mid_south state (institution root + declared finding); the frost-table role vce played is acknowledged in the finding, not silently erased |
| edamame | vce_426_331 -> vce_spes_455 on 6 nodes + anchors + source_set + finding | id/document divergence: the claims are verbatim in SPES-455 (inoculant, 7-10 day window, low N), absent from 426-331; two anchors already carried the SPES-455 URL under the wrong id |

Catalog: +2 ids (`vce_426_840`, `vce_spes_455`), both read 2026-08-10 (live fetch, now cached in
`tools/.doc_cache`), both carrying titles in their `name` field (see the title-field decision
spec, same date).

## Raw-count reconciliation (pinned in guard G10)

`vce_426_331`: 1281 -> 1247. Removals 49: strawberry 12 (region 1, z7 src+anchor 2, container
anchor 1, arms 4x2), blueberry 6, raspberry 6, blackberry 6 (region 1, container 1, cells 2x2),
elderberry 6, edamame 13 (6 src + 6 anchors + source_set). Additions 15: 7 `filed_in_session`
substrings + 8 finding-summary mentions (elderberry's finding names it three times).
`vce_426_840`: 36 (catalog 2, strawberry 12, berry trio 15, finding mentions 4, straw finding 0
[human form], catalog citable 0 + region lists 3). `vce_spes_455`: 16. `VCE 426-331` (human
form): 228 -> 225 (4 note replacements, +1 finding mention). `VCE 426-840`: 5.

## Guards

11 groups. RED before GREEN with NINE mutations, all caught -- and the mutation sweep itself
caught two invalid guards and a promote gap before anything shipped: G5/G6's first drafts used
substring-in-json checks that fired on legitimate finding prose (masking every later guard --
[[guard-tests-pass-because-an-earlier-check-fires]] inverted), and the first GREEN run exposed
five plantings-container anchors the promote had missed
([[correct-every-field-carrying-an-attribution]], again). Retention guards pin the id's
SURVIVAL on broccoli/cucumber/thyme/shallot/popcorn/bok-choy cells and northern_tier
(PLA-195 (d) territory) so a later sweep cannot blanket-strip it.

## Gauntlet

- `whole_crop_gate` PASS x7 (sweet-pea, strawberry, blueberry, raspberry, blackberry,
  elderberry, edamame) -- run under the STRICTER staged gate (see below).
- `gate_all` 119/121: the two failures are zinnia + bee-balm on A52/A53, the **concurrent
  PLA-157 session's uncommitted trigger-prose gates**, RED by their own staged design
  (docs/2026-08-10-pla157-zinnia-trigger-fix.md: "Staged to the promote boundary and STOPPED
  there: PLA-155 runs in parallel and Trevor serializes promotes"). Every other crop, including
  all seven touched here, passes their new checks too.
- `release_verify` per touched crop vs base `ce9eb12f`: the only CONCERNs are (a) the
  known single-crop-shape collateral listing (the changed set == exactly this promote's 7
  crops, independently pinned by G8) and (b) strawberry's rgv `plantings_provenance` novel-key
  concern, reproduced byte-identical against the BASE (pre-existing, not introduced here).
  One non-blocking 5.5 note (sweet-pea heat_pause months, cert-declared lettuce-peer model).
- Pinned suites: `test_hunt_footprint` OK (footprint unaffected: ncsu_ext stays bare on the
  same elderberry nodes; the strawberry/edamame swaps are pathed-to-pathed),
  `test_promote_pla156_corn` OK (12 groups), `test_gen_current_state` PASS.
- COMPACT preserved, no trailing newline.

## Session ops notes

- A `git stash` used mid-session to rebuild the pre-state briefly swept up the concurrent
  session's in-flight `whole_crop_gate.py` edit; popped immediately, verified restored. Do not
  stash in this shared checkout -- extract historical states via `git show` or
  `promote_fixture` instead.
- northern_tier tomato/lettuce divergences (vce present in legacy 5-source piles on values the
  doc contradicts, e.g. z6 tomato Apr 8-22 vs the doc's May 10-Jun 10) recorded for PLA-195
  block (d), deliberately untouched here.
