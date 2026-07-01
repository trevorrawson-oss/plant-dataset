# spaghetti-squash -- author-fresh pilot NOTES

Session: `spaghetti_squash_author_fresh_pilot` (2026-06-30, Claude Code lane, web access).
Output: `spaghetti_squash_crop.json` (compact canonical) + `.pretty.json` (review) + `build_spaghetti.py` (the deterministic builder).
Base canonical SHA: `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5` (READ-ONLY, untouched -- verified unchanged after the run).

## What this is
Gold-standard fill of the existing `spaghetti-squash` SHELL. The structural template is the
**certified in-canon `butternut-squash`** record (`verified_gs_arc`), which itself mirrors the
certified `zucchini-courgette` + the pumpkin pilot (all `warm_season_fruiting` / `frost_anchored`
Cucurbita). Butternut supplies the WINTER-squash model the task asked for: single mature harvest ->
cure -> store. Structure was borrowed; EVERY biological value was re-derived for spaghetti squash.

## The core model: WINTER squash (mature harvest + cure), NOT summer squash
Like butternut and unlike its same-species cousin zucchini, spaghetti squash is grown to FULL
MATURITY with a HARD rind and harvested ONCE: rind a thumbnail cannot dent, stem dried/corky, skin
dull not glossy, the ground spot turned from white to yellow. `harvest_urgency` = `low` (it stores).
After harvest it can be eaten straight away or given a short cure (~10 days, 80-85 degrees F) to
harden the rind, then stored cool/dry (50-60 degrees F).

## Key spaghetti-vs-butternut refits (Cucurbita PEPO, not moschata)
Spaghetti squash is *C. pepo* (same species as zucchini/acorn), where butternut is *C. moschata*.
That drives the biology divergences from the template:

- **SIGNATURE -- flesh strands into "spaghetti."** The whole reason to grow it: cooked flesh
  separates into long pale strands. Woven through description, harvest_ready, storage (freezer =
  cooked strands), tips, and the failure_diagnostics ("picked pale -> mushy, will not strand").
- **Ripens DEEP YELLOW, not tan.** Every "tan" ripeness cue from butternut re-authored to
  golden/deep-yellow; immature = pale/cream/green-tinged. (harvest_ready, growth_stages
  fruit_development + harvest, tips, notifications, failure_diagnostics.)
- **Squash vine borer: SUSCEPTIBLE, a managed pest** -- the marquee reversal. Butternut's moschata
  stems make it borer-RESISTANT (its headline advantage); spaghetti squash as a thin-stemmed pepo is
  a *preferred host* like zucchini/acorn. The entire SVB pest entry was re-authored to
  susceptible-and-manage (row cover to bloom, scout stem-base frass, slit-and-remove, bury vine
  joints), and every borrowed "shrugs off the borer" claim (companions note + bad-cucurbits why,
  growth_stages.vining, tips.vining, yield factors, description) was flipped. Sourced to UIUC
  (pepo squash most SVB-susceptible).
- **Moderate keeper (~1-3 months), NOT butternut's 4-6.** Storage prose re-derived: C. pepo stores
  a couple of months (longer than acorn, well short of butternut), edible at harvest, curing
  optional. Honest butternut comparisons ("not as long as a butternut") are kept deliberately.
- **DTM 90-100** (mid 95), vs butternut's 85-110. Moderately vigorous vines ~6-8 ft (vs 8-12 ft).
- **Heat/disease claims neutralized.** Butternut's "moschata handles heat/disease better than pepo"
  framing removed; spaghetti squash carries the ordinary cucurbit heat/mildew sensitivity.
- **pH 6.0-6.8** pref / 5.8-7.5 tol (carried; correct for spaghetti squash). Full sun, well-drained
  loam, high organic matter. germ 70-95 degrees F, weeks_indoors 3.
- **Spacing in FEET, cap-conscious.** `spacing_inches = [24,48]` -- in-row 24 in to ~4 ft row; real
  rows 3-5 ft and 6-8 ft sprawl live in prose (soil_prep, description, yield). Well within the A33
  non-tree bound of 72. Flagged in open_findings.
- **Varieties** re-derived for spaghetti squash: Vegetable Spaghetti (OP standard, 95d), Tivoli
  (AAS bush, container, 98d), Small Wonder (compact semi-bush, single-serving, early ~85d),
  Orangetti (orange-fleshed semi-bush, sweeter, 90d), Stripetti (striped keeper, mildew-tolerant,
  100d). Container line = Tivoli / Small Wonder / Orangetti; short-season = Small Wonder.

## Calendar handling
Full 10-region roster, zones 3-11, non-empty 12-token calendars. The frost-anchored winter-squash
windows are shared with the butternut/pumpkin template (a 90-100 day and an 85-110 day warm vining
cucurbit share a near-identical calendar), so the calendar tokens/dates carry over gate-clean and
A37-normalized; only the region PROSE (region_notes x10, plantings_provenance x10) was re-authored
for spaghetti squash (drop moschata/variety-specific claims, add the pepo SVB note). Winter
`cold_pause` off-season, late-spring/early-summer `plant`, single fall `harvest`; hot-desert cells
(ca_desert, low_desert_az) split into spring + midsummer plantings around peak heat with a
`season_over` gap (no heat_pause objects anywhere in the record -- so A28 is a clean no-op).

## Sourcing (all EXISTING source_catalog IDs; all T1; 0 uncatalogued, 0 non-T1; 17 distinct)
Same catalogued winter-squash T1 set as butternut. Core biology grounded (web-verified this session):
- **umn_ext** -- UMN Growing pumpkins and winter squash + Harvesting/storing (pH, soil temp,
  spacing, water, store 50-60 degrees F / 50-70% RH, chilling injury below 50 degrees F).
- **umass_ext** -- UMass Pumpkin & Winter Squash Harvest/Curing/Storage (C. pepo edible at harvest,
  moderate keeper, cure 5-10 d at 80-85 degrees F).
- **uiuc_ext** -- U of Illinois winter squash + squash vine borer (spaghetti = *C. pepo*, oblong
  8-9 in yellow stringy flesh; pepo squash the most SVB-susceptible).
- **clemson_hgic** -- cucurbit insect pests + pumpkins/winter squash (squash bug, cucumber beetle,
  mildews).
Regional planting-window cells anchor to the institution-level extension portals (uga_ext, ucanr,
uc_mg, nmsu, tamu, umd, iastate, ufifas/uf_ifas_vh021, uariz, uhawaii, uwi) -- same pattern as the
butternut and pumpkin pilots.

## FLAGS (open_findings, all blocks_launch=false, modeled-and-flagged)
1. `spaghetti_pilot_regional_calendars_modeled` -- per-zone windows MODELED from DTM 90-100 + the
   crop-invariant frost anchors + representative extension dates (parallel to butternut/pumpkin).
2. `spaghetti_pilot_spacing_prose` -- `spacing_inches` [24,48]; full rows (3-5 ft) + 6-8 ft sprawl
   in prose.
3. `spaghetti_pilot_variety_dtm_modeled` -- variety DTMs from breeder/seed-catalog norms + AAS
   standing (Tivoli AAS), not per-variety T1 pages.
4. `spaghetti_pilot_regional_source_anchors_general` -- several regional cells anchor to
   institution-level portals; core agronomy verified vs UMN/UMass/UIUC/Clemson.
5. `spaghetti_pilot_hawaii_window_modeled` -- hawaii z11 broad frost-free default; catalogued CTAHR
   source is a scanned/image PDF not WebFetch-readable (same as zucchini/butternut/pumpkin). No
   fabricated source.

## Verification (run on a SCRATCH splice; canonical byte-untouched)
- `python3 tools/whole_crop_gate.py spaghetti-squash scratch_spaghetti.json` -> **GATE: PASS (exit 0)**;
  all A2-A37 zero violations (incl. **A37 calendar-coherence = 0** -- no A37 lines to report),
  B null_values 0, C/D dash+temp 0, E 17 distinct IDs / 0 uncatalogued / 0 non-T1, F anchoring gaps
  0, G flip-state `author_fresh_pilot` with 0 launch blockers.
- `tools/release_verify.py scratch_spaghetti.json --base crops_data_final.json --slug spaghetti-squash`
  -> **RELEASE-VERIFY: clean (exit 0)**; only spaghetti-squash changed among crops, reference
  lettuce-leaf byte-identical, **no new violations introduced** (the long "cleared" list is the
  shell's pre-existing empty-state violations this fill resolved), calendars crop-specific (not
  byte-identical to any reference).
- `tools/derive_realized_successions.py --check scratch_spaghetti.json` -> **up to date (exit 0)**
  (succession out of scope: `suitable=false`, single planting).

## Status / next
`status="author_fresh_pilot"`, `launch_ready_core=false`, `launch_ready_seasoned=false`. NOT
launch-ready: queued for the daily biology-fidelity review + a per-region source-truth sample to
confirm the modeled regional windows and variety DTMs before any flip. Promotion to canonical is a
separate Trevor-gated step.
