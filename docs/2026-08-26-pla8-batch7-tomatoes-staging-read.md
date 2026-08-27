# PLA-8 batch 7 (THE TOMATOES) -- staged, read, NOT promoted (2026-08-26, late evening)

beefsteak-tomato, cherry-tomato, grape-tomato, roma-tomato. 34 problems, **154 rungs staged** in
`tools/staging/pla8_batch7_tomatoes/` (out_*.json are the authoring record; `merge` re-derives
scratch_canonical.json from them). Authored by four parallel agents from each crop's OWN prose,
then read and adjudicated by the orchestrator. **The promote is deliberately NOT built yet**: its
suite must replay from `promote_fixture.pre_state(BASE)`, and the base it needs is the
chemical-cohort canonical `674fab25`, which is applied but uncommitted. Build the promote AFTER
Trevor's commit registers that SHA in `COMMIT_FOR`.

## What was read (the denominator, not just the fixes)

- All 34 problems' source prose, all four agents' full reports, **all 80 method-meaning pairs**
  `verify` printed, and **every rung string** (147 authored + 11 from adjudication), held against
  the prose and against each method's MEANS text.
- Claims traced to the catalog rather than assumed: water_spray's early-day timing and
  floating_row_cover's same-family-bed trap warning are both catalog cautions verbatim; the
  copper rungs restate the acute-split caution the chemical-cohort round added HOURS earlier,
  correctly; grape's horticultural_oil whitefly rung carries the new bee-precaution and the
  sulfur-interval caution, correctly.
- Two UMN documents fetched and read from LIVE bytes for the mint (below).

## Adjudications (the two cross-sibling conflicts verify flagged, plus three scope calls)

1. **neem_oil on flea-beetles: DROPPED** (was on beefsteak + grape; cherry + roma had refused
   it). All four crops' prose names a neem spray for flea beetles, but the catalog entry's
   meaning is soft-bodied smothering/antifeedant; a hard-shelled chewing beetle is
   legal-but-wrong-meaning, the `bottom_watering` shape. Finding: neem_oil's `applies_to`
   (insect_general) is wider than its prose scope; the crops' flea-beetle neem advice is now
   deliberately unplaced. If a future catalog round widens neem's MEANS on a T1 read, these
   rungs can return.
2. **garden_sanitation on blossom-end-rot: KEPT on all four** (added to grape, authored fresh
   from grape's prose). The method's MEANS explicitly covers pulling first affected fruit; every
   note states the culling-not-disease-control framing, since BER is non-contagious.
3. reflective_mulch for whiteflies: KEPT. Legal (insect_soft_bodied), mechanism identical
   (deterring incoming winged adults), crop prose commands it; the entry's "documented cases"
   (cucurbit aphid-virus) is provenance, not a scope bar. Worth naming whitefly in the entry at
   a future catalog touch; not this batch's edit.
4. yellow_sticky_traps for whiteflies: in-meaning ("other small flying pests").
5. Grape's wilt sanitation note keeps the tool-hygiene clause (prose-supported secondary clause
   riding the rogue-and-destroy action); roma's equivalent omits it. Both prose-faithful;
   divergence stands.

## THE MINT: `splash_barrier_mulch` (spec in `mint_splash_barrier_mulch.json`)

All four agents independently reported the same control blocked: every crop's early-blight AND
septoria prose commands mulching the soil against splash, and no legal key carried it
(moisture_buffering_mulch is physiological-only and MEANS moisture; straw_mulch MEANS a
strawberry fruit barrier). Eight instances with nowhere to go is the playbook's mint signal, and
the melons/mancozeb model applies: growth, not debt. Both UMN anchors were fetched and READ live
2026-08-26; the leaf-spot page carries the mechanism sentence, the acceptable-mulch list, and
the herbicide-residue caution the entry restates. **8 rungs staged** (early-blight + septoria x
4 crops), inserted after water_at_the_base.

## Structural state

- `merge`: 154 rungs, **ids minted 34 / reused 0** (correct: no tomato problem carried an id
  before). THESE IDS ARE NOW THE JOIN KEYS; the promote must ship these exact ids.
- `whole_crop_gate` on scratch_canonical_with_mint.json: **PASS x4, 0 violations**;
  `control_ladder_gate` on the same: **0**. Hygiene sweep over all new strings: clean.
- KNOWN ARTIFACT: `ladder_batch.py verify` (which reads the LIVE catalog) crashes with
  `KeyError: 'splash_barrier_mulch'` and its gate_all shows the 4 crops failing -- both are the
  unminted key, not defects. The mint-injected scratch run above is the true check. Re-run
  verify after the promote mints the key and it will come clean.

## Findings filed, NOT fixed (existing prose; for the corrections log / a later ruling)

1. Hornworm companion plants disagree between registers on ALL FOUR crops:
   prevention_beginner says "dill or fennel", prevention_seasoned says "dill and basil". Rungs
   carry register-faithful unions; the source wobble stands.
2. Blossom-end-rot register tension on ALL FOUR: organic_treatment_beginner says the fix is
   watering "not calcium supplements" (Clemson's anchor is literally the calcium-myth page)
   while organic_treatment_seasoned says "Foliar calcium spray provides some relief" (roma's
   prevention_seasoned reconciles at "only marginal relief"). No calcium rung was authored
   anywhere; the register wobble is the finding.
3. Whitefly transplant inspection (grape + roma prose, "the usual introduction route") is
   unplaceable: `certified_clean_stock` is disease-only in applies_to and MEANS
   pathogen-in-planting-material. Catalog question for a future round: an insect-vector
   quarantine key, or a widening argued on a T1 read.
4. Unplaceable prose advice, recorded as deliberate gaps: flea-beetle transplant-size advice
   (planting_time_avoidance is a calendar action, refused by three agents independently);
   diatomaceous earth (known-owed method, still unminted, playbook section 7); spider-mite dust
   suppression and humidity-raising; BER root-disturbance avoidance and nitrogen-AMOUNT
   moderation (avoid_ammoniacal_nitrogen is a FORM swap; balance_nitrogen is not
   physiological-legal); wilt tool sanitation as a method of its own.
5. Late blight is typed `fungal` while the prose correctly calls P. infestans an oomycete; the
   type enum has no oomycete value and fungal_foliar is the operative control class. Recorded,
   not a defect.

## What the promote needs (build after the chemical-cohort commit)

- Base: the committed canonical carrying `674fab25`. Register it in `COMMIT_FOR` first.
- One promote: mint `splash_barrier_mulch` + write 4 crops' pests[]/diseases[] ids, types and
  ladders from out_*.json. Blast radius: 4 crops' problem arrays + 1 catalog method, nothing
  else; `assert set(pre)==set(post)` before value compares at every level.
- Guard families per the PLA-215 convention, `VerifyPostIsDriven` written FIRST (the
  chemical-cohort harness went 49/49 first-run because of it). Reuse: id-stability (the 34
  minted ids byte-exact), tier monotonicity, the neem-flea-beetle refusal as a REFUSAL-SPEC
  (a neem rung appearing on any flea-beetles ladder must redden), the splash mint verbatim,
  sibling-divergence pins (grape has whiteflies/wilt, beefsteak/cherry do not; only grape
  carries horticultural_oil + weed_host_control rungs).
- Roster flips 29 -> 33 laddered. After this batch: peppers / leafy greens / roots / brassicas
  per the demand-first ordering; microgreens + companion/pollinator LAST.
