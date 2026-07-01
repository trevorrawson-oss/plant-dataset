# acorn-squash -- author-fresh pilot NOTES

Session: `acorn_squash_author_fresh_pilot` (2026-06-30, Claude Code lane, web access).
Output: `acorn_squash_crop.json` (compact canonical) + `.pretty.json` (review) + `build_acorn.py` (the deterministic builder).
Base canonical SHA: `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5` (READ-ONLY, untouched -- verified unchanged after the run).

## What this is
Gold-standard fill of the existing `acorn-squash` SHELL. The structural template is the
**certified in-canon `butternut-squash`** record (`verified_gs_arc`), itself modeled on the
certified `zucchini-courgette` + the pumpkin pilot (all `warm_season_fruiting` / `frost_anchored`
Cucurbita). Butternut supplies the WINTER-squash model: single mature harvest -> store. Structure
was borrowed; EVERY biological value was re-derived for acorn squash. The SVB-susceptible pepo
framing follows the sibling `spaghetti-squash` pilot (same species, same borer problem); the
storage/curing biology diverges sharply from BOTH (see below).

## The core model: WINTER squash (mature harvest), NOT summer squash
Like butternut/spaghetti and unlike its same-species cousin zucchini, acorn squash is grown to
FULL MATURITY with a hard rind and harvested ONCE. But acorn's ripeness cue is its own: the
**GROUND SPOT** (where the fruit rests on the soil) turns from cream/yellow to **deep ORANGE**,
alongside a hard rind a thumbnail cannot dent, dull (not glossy) skin, and a dry corky stem. The
deeply ribbed, heart-shaped, usually **dark-green** rind colors up weeks BEFORE ripeness, so
color alone is NOT the tell (butternut ripens tan; spaghetti ripens deep yellow; acorn is dark
green + orange ground spot). Small fruit (~1-2 lb) with sweet, fine-grained flesh, halved and
roasted by the single serving; NO stranding (that is spaghetti squash). `harvest_urgency` =
`moderate` (a shorter keeper than butternut's `low`).

## The three marquee acorn refits
1. **SHORTER keeper than butternut AND spaghetti (~1-2 months).** Acorn is the SHORTEST keeper of
   the common winter squashes: ~1-2 months (Iowa State ~5-8 weeks; UMass a couple of months), well
   short of a spaghetti squash and far short of a butternut's 4-6. Storage prose, room_temp,
   growth_stages harvest, notifications, tips, description, yield, and the verification log all
   carry this honestly (butternut comparisons kept deliberately). Store directly, cool 50-55 F.
2. **DO NOT CURE -- the divergence from every other winter squash.** Unlike butternut/spaghetti,
   acorn squash should NOT be cured: the high heat and humidity of a cure REDUCE its quality,
   shorten its already brief storage, and can leave the flesh dry and stringy. It is edible right
   off the vine. Every borrowed "cure ~10 days at 80-85 F" step from the butternut template was
   removed and reframed to "do not cure; store cool" -- in storage notes/room_temp, harvest_ready,
   watering (method + critical_periods), growth_stages harvest (stage renamed "Harvest and store"),
   notifications, weather_triggers frost_warning, tips harvest, and two failure_diagnostics.
   Sourced to UMass + Iowa State winter-squash harvest/storage pages.
3. **Squash vine borer: SUSCEPTIBLE, a managed pest** -- the pepo reversal (same as spaghetti,
   opposite of butternut). Butternut's moschata stems make it borer-RESISTANT (its headline
   advantage); acorn as a thin-stemmed pepo is a *preferred host*. The entire SVB pest entry was
   re-authored to susceptible-and-manage (row cover to bloom, scout stem-base frass, slit-and-
   remove, bury vine joints), and every borrowed "shrugs off the borer / moschata toughness" claim
   (companions note + bad-cucurbits why, growth_stages vining, tips vining, yield factors,
   description, se_gulf/ca_interior/fl_peninsula/hawaii region notes) was flipped. Sourced to UIUC.

## Other acorn refits
- **BUSH and vining cultivars both** (task-required). Vining types run ~4-8 ft; true bush /
  semi-bush types stay compact. Woven through description, soil_prep, container, yield, tips,
  growth_stages. Container line is genuinely strong for acorn (bush types widely available).
- **DTM 80-100** (mid 85), vs butternut 85-110 / spaghetti 90-100 -- acorn skews earliest.
- **pH 6.0-6.8** pref / 5.8-7.5 tol (carried; correct for acorn). Full sun, well-drained loam,
  high organic matter. germ 70-95 F, weeks_indoors 3, water moderate.
- **Spacing in FEET, cap-conscious.** `spacing_inches = [24,48]` -- bush ~18-24 in, vining 24-36 in
  in-row / 3-6 ft rows / 4-8 ft sprawl live in prose. Within the A33 non-tree bound of 72. Flagged.
- **Varieties** re-derived for acorn: Table Queen (OP dark-green ribbed vining standard, 80d),
  Table Ace (hybrid semi-bush, near-black, low-fiber, early 78d), Table King (compact bush, AAS,
  80d), Honey Bear (AAS bush, single-serving, powdery-mildew-tolerant, 95d), Celebration (F1
  multicolor semi-vining, ornamental + eating, 95d). Container line = Table King / Honey Bear /
  Table Ace; short-season = Table Ace / Table Queen; mildew-tolerant = Honey Bear.
- **Signature quality failure re-authored:** the immature/"bland" butternut diagnostic became an
  acorn-specific one -- dry/stringy/fibrous flesh from EITHER picking too early OR over-maturity,
  curing, or over-storage (an acorn gone all-orange is past prime). This captures acorn's real
  pitfalls: it does not improve with curing and slips within a month or two.

## Calendar handling
Full 10-region roster, zones 3-11, non-empty 12-token calendars. Acorn's slightly shorter season
does not shift the monthly-granularity frost-anchored calendar, so the calendar tokens/dates carry
over from the butternut template gate-clean and A37-normalized (winter `cold_pause` off-season,
late-spring/early-summer `plant`, single fall `harvest`; hot-desert cells split into spring +
midsummer plantings around peak heat with a `season_over` gap -- NO heat_pause objects, so A28 is
a clean no-op). Only the region PROSE (region_notes x10, plantings_provenance x10) was re-authored
for acorn squash. **A37 calendar-coherence = 0 -- no A37 lines to report.**

## Sourcing (all EXISTING source_catalog IDs; all T1; 0 uncatalogued, 0 non-T1; 17 distinct)
Same catalogued winter-squash T1 set as butternut/spaghetti. Core biology grounded (web-verified
this session against catalogued sources):
- **umass_ext** -- UMass Pumpkin & Winter Squash Harvest/Curing/Storage: "Harvest C. pepo squashes
  when the ground spot is dark orange"; acorn "should not be cured, because it can reduce their
  lifespan in storage"; acorn a notably shorter keeper than butternut.
- **iastate_ext** -- Iowa State winter squash: acorn stores ~5-8 weeks (1-2 months), edible right
  after harvest, do NOT cure (high temp/RH reduce quality and storage life).
- **uiuc_ext** -- U of Illinois winter squash + squash vine borer: acorn = *C. pepo*, DTM 80-100;
  pepo squash (incl. acorn) the most SVB-susceptible.
- **clemson_hgic** -- cucurbit insect pests + pumpkins/winter squash (squash bug, cucumber beetle,
  mildews).
Regional planting-window cells anchor to the institution-level extension portals (uga_ext, ucanr,
uc_mg, nmsu, tamu, umd, iastate, ufifas/uf_ifas_vh021, uariz, uhawaii, uwi) -- same pattern as the
butternut/spaghetti pilots.

## FLAGS (open_findings, all blocks_launch=false, modeled-and-flagged)
1. `acorn_pilot_regional_calendars_modeled` -- per-zone windows MODELED from DTM 80-100 + the
   crop-invariant frost anchors + representative extension dates (parallel to butternut/spaghetti).
2. `acorn_pilot_spacing_prose` -- `spacing_inches` [24,48]; bush 18-24 in, vining rows 3-6 ft and
   4-8 ft sprawl in prose.
3. `acorn_pilot_variety_dtm_modeled` -- variety DTMs from breeder/seed-catalog norms + AAS standing,
   not per-variety T1 pages.
4. `acorn_pilot_regional_source_anchors_general` -- several regional cells anchor to institution-
   level portals; core agronomy verified vs UMass/Iowa State/UIUC/Clemson.
5. `acorn_pilot_hawaii_window_modeled` -- hawaii z11 broad frost-free default; catalogued CTAHR
   source is a scanned/image PDF not WebFetch-readable (same as zucchini/butternut/spaghetti). No
   fabricated source.

## Verification (run on a SCRATCH splice; canonical byte-untouched)
- `python3 tools/whole_crop_gate.py acorn-squash scratch_acorn.json` -> **GATE: PASS (exit 0)**;
  all A2-A37 zero violations (incl. **A37 calendar-coherence = 0** -- no A37 lines to report),
  B null_values 0, C/D dash+temp 0, E 17 distinct IDs / 0 uncatalogued / 0 non-T1, F anchoring
  gaps 0, G flip-state `author_fresh_pilot` with 0 launch blockers.
- `tools/release_verify.py scratch_acorn.json --base crops_data_final.json --slug acorn-squash`
  -> **RELEASE-VERIFY: clean (exit 0)**; only acorn-squash changed among crops, reference
  lettuce-leaf byte-identical, no new violations introduced (the long "cleared" list is the shell's
  pre-existing empty-state violations this fill resolved), calendars crop-specific (Step G: not
  byte-identical to the reference).
- `tools/derive_realized_successions.py --check scratch_acorn.json` -> **up to date (exit 0)**
  (succession out of scope: `suitable=false`, single planting; acorn not in the derived set).

## Status / next
`status="author_fresh_pilot"`, `launch_ready_core=false`, `launch_ready_seasoned=false`. NOT
launch-ready: queued for the daily biology-fidelity review + a per-region source-truth sample to
confirm the modeled regional windows and variety DTMs before any flip. Promotion to canonical is a
separate Trevor-gated step.
