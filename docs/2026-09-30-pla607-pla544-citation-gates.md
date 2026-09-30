# PLA-607 + PLA-544: the armor before PLA-10 (2026-09-30)

Gate work only. `crops_data_final.json` untouched: canonical stays `00dda31c`, certified 121,
launch-ready 114. Two gates, both wired into `whole_crop_gate` (A62, A63) and `gate_all`.

## PLA-607: `tools/sourced_block_ratchet_gate.py` (A62)

**The rule.** On a certified crop, a NAMED block carrying authored content whose citation slot is
missing, null or `[]` is uncited. Today's uncited blocks are waived by identity
(`crop|path|field`) in `tools/sourced_block_ratchet_known.py`; any other uncited block fails and
names itself. A block that is absent or null is not uncited. Shrinking passes (reported as CLOSED);
growth and substitution fail.

**Measured on 00dda31c:** 7063 named blocks inspected on 121 certified crops; **2634 uncited, on
all 121**. The ticket's "98 slots on 57 crops" is the slot-present subset (`[]`/null) and is
reconciled inside the 2634 by an independent walk; the key-absent state is the other 2536.

| block type | uncited | crops |
| -- | --: | --: |
| growth_stages[] | 615 | 104 |
| notifications[] | 458 | 104 |
| tips_by_stage.*[] | 313 | 35 |
| weather_triggers[] | 289 | 96 |
| failure_diagnostics[] | 251 | 63 |
| description (description_sources) | 108 | 108 |
| harvest_urgency (harvest_urgency_sources) | 108 | 108 |
| start_method | 103 | 103 |
| succession_policy | 86 | 86 |
| varieties.recommended[] | 77 | 12 |
| pests[] | 54 | 13 |
| diseases[] | 50 | 13 |
| harvest_ready (harvest_ready_sources) | 26 | 26 |
| watering | 17 | 17 |
| bolting | 13 | 13 |
| container_notes | 12 | 12 |
| varieties | 12 | 12 |
| fertilizer | 11 | 11 |
| pollination | 9 | 9 |
| rotation | 8 | 8 |
| verification_status.field_additions[] | 3 | 2 |
| thinning | 3 | 3 |
| ph, soil, storage, yield_expectations | 2 each | 2 each |

No crop mixes cited and uncited items inside one list family: item-level citation is a per-crop
authoring style (17 crops cite growth_stages / notifications / weather_triggers per item, 104 do not).

**Named list.** 20 dict blocks, 3 crop-root `<name>_sources` siblings (description, harvest_ready,
harvest_urgency), 10 item families (pests/diseases/growth_stages keyed by `id`, rootstock_options
and varieties.recommended by `name`, the rest by index), and `tips_by_stage.<stage>[]`.
`varieties.recommended[]` and `container_notes.plants_per_pot.readings[]` are covered by their
parent block's `sources` when they carry none of their own.

**Ruled out (Trevor, 2026-09-30):** companions (provenance deferred), zones (legacy tree, read by
plant-astro), regions (modeled by design). **launch_ready untouched:** §G is not changed; whether
launch-readiness should depend on sources is Trevor's separate ruling.

**Naming is part of adding.** A DISCOVERY guard fails any `sources` / `*_sources` /
`anchoring_urls` / `*_anchoring_urls` key on a certified crop that sits on no named, excluded or
ANCHOR_ONLY block. ANCHOR_ONLY records the eight anchored claims with no sources slot: crop-root
`anchoring_urls`, `det_indet.anchoring_urls`, and `<f>_anchoring_urls` for days_to_maturity,
days_to_maturity_mid, germination_temp_f, spacing_inches, sunlight_hours, weeks_indoors.

**Folded in: the PLA-533 pot-size ratchet** (`container_citation_floor_gate`, now deleted with its
suite and harness). Same KNOWN four, CEILING 4, same predicate, same proofs. It is not redundant:
a NEW pot-uncited crop is already caught by §F or the general ratchet, but a crop whose
container_notes is already WAIVED uncited (plum, 8 such) gaining a min_pot_gallons is invisible to
an identity waiver, and only this sub-rule sees it.

**Recorded limitations.** (1) Index-keyed families: delete a waived item + append a new uncited
one can land on a waived index. (2) An identity waiver pins which block is uncited, not what it
says: new content added to an already-waived uncited block stays silent (closed only for
min_pot_gallons, by the sub-rule).

## PLA-544: `tools/bare_host_gate.py` (A63)

**The rule.** A citation anchored at a bare domain or site root that is the SOLE citation on its
node fails, whether or not the crop paths that source id elsewhere. Co-cited bare anchors are
reported, never blocking. Waived by identity (`crop|path|anchor_key|source_id`) in
`tools/bare_host_gate_known.py`.

**Measured on 00dda31c:** 30102 anchors inspected on 121 certified crops; 1242 bare = **381 SOLE
(41 crops)** + 861 co-cited. Row-for-row agreement with `bare_host_scan.scan()` on every
`anchoring_urls` node. The gate also walks crop-root `<field>_anchoring_urls` (0 bare today; the
scan never looked there) and region/zone cells.

**Named examples, confirmed:** grapefruit and orange-navel `rootstock_options[2]` (Flying Dragon),
`ucr_citrus` at `https://citrusvariety.ucr.edu`, SOLE, both waived (orange-navel's is the one
`self_pathed` could not see). lemon `rootstock_options[0]` / `[1]`, `tamu_agrilife` at
`https://agrilifeextension.tamu.edu`, CO-CITED beside HS402: reported, non-blocking.

**BARE** = `bare_host_scan.BARE` (imported) plus a site ROOT PAGE (`/index.html` etc., or a
fragment on the root); a query string names a page and is not bare.

## PLA-544: the pinned self-pathed test, resolved by option 3

`test_self_pathed_population_at_this_canonical` now pins the population BY IDENTITY
(`tools/bare_host_self_pathed_known.json`, 321 rows = 161 SOLE / 80 decisions / 37 crops on
00dda31c). A new row fails and prints `crop|path|source_id`; a row that leaves is reported. The six
uada_ext rows (mulberry x4, persimmon x2, `regions.mid_south...`) are IN the pin as unadjudicated
leads for PLA-625; they were not adjudicated or repointed here. Its `run_test_tree` waiver is
removed. The cache-dependent `test_cited_claim_scan` test now fails with `CACHE COVERAGE, NOT A
DATA DEFECT` and every uncached URL; its waiver is re-keyed to that text, and
`mutate_run_test_tree.py`'s M6/M7 waiver cases are re-homed onto it (8/8 caught).

## Tests pinned on purpose, and the pins deliberately NOT taken

Pinned: live uncited == the waiver set; live SOLE == the waiver set (citing or repointing a waived
row forces the waiver-file edit in the same commit). Not pinned: inspected totals and the co-cited
count, which a cited promote legitimately moves; they are checked against a declared floor
(6500 blocks, 28000 anchors) and the measurement is recorded here instead.

## Proof

- Suites: `test_sourced_block_ratchet_gate.py`, `test_bare_host_gate.py`, `test_bare_host_scan.py`
  (pytest); `test_gate_citation_ratchets_a62_a63.py` (script-style, the real entry points,
  including gate_all's roster-only ceiling branch via a scratch tools/ copy, and the empty-roster
  REFUSED path).
- Harness: `tools/mutate_citation_ratchet_gates.py` (ratchet + bare + wiring): **45 injected, 45 caught, 0 survived, 0 broken** (26 + 15 + 4), anchor preflight, positive control, sentinel on every target. The first run had 2 survivors (`citation_only_block_counted`, `sources_ignored_in_cited_set`); both drivers were added before this result.
- Full tree (`run_test_tree.py`): **PASS**, 183 collectable files, 6318 passed; 73 of 74 script-style RAN; 1 SKIPPED (`test_build_berry_pilot_patch.py`, pre-existing, ran nothing); 1 waived failure (cited_claim_scan cache coverage, PLA-161 / PLA-544). The first full run caught 2 failures this work caused: `region_harness` / `rgv_harness` copy only `tools/*.py`, so JSON waiver files crashed `whole_crop_gate` at import there. The waiver sets are therefore `.py` modules.
- `gate_all` PASS 121/121, launch-ready 114/121, both ratchet populations reported; `release_verify` clean.

## Canonical-SHA-pinned tests (inventory, not re-measured)

- **Live-equality (red at the next promote):** `test_problem_id_collision_gate.py` `Preflight::test_canonical_is_the_pinned_sha` (`PINNED_SHA` 00dda31c). The only one.
- **Live population pinned at a named SHA:** `test_sourced_block_ratchet_gate.py` (00dda31c, waiver-set equality), `test_bare_host_gate.py` (00dda31c, SOLE-set equality + the Flying Dragon rows, which the PLA-533/612 re-author will move), `test_bare_host_scan.py` (hunt #28 + lemon 14-node count at 76f92a20; self-pathed identity pin at 00dda31c), `test_annual_calendar.py` `_PINNED_ANNUALS` (1721208e), `test_perennial_year_gate.py` (perennial roster 38 / 26 pill crops, fe26f783), `test_gate_plants_per_pot_a60.py` precondition (plum not container_ok, 079e3923).
- **Borderline, no SHA named:** `test_doc_roster_claim_gate.py` (128/121/7 on live); `test_promote_pla161_hunt28_declaration.py`, `test_campaign_c_reprice.py`, `test_campaign_d_reprice.py` (a record still present on live).
- **Replay-pinned (immune to promotes):** 138 files (136 via promote_fixture, 2 via git show).
- **Side finding:** `test_build_rgv_promote.py` and `test_build_corn_family_patch.py` early-`return` once their one-shot batch has landed, so they pass having inspected nothing (the vacuity class), and `run_test_tree` does not see it because they are pytest-collectable.
