# Field-Addition Register — the live queue for cross-crop field additions

**What this is:** the standing, tracked queue of new fields to add across the crop roster, plus the
status and **trigger condition** for each. Consult this **before** adding any field that spans crops.
It is the "track" that makes the cross-crop field-addition process visible instead of buried.

**Method:** follow `docs/gs_cross_crop_field_addition_v0.md` (the "column GS arc" template — contract
first → diverse pilot incl. a legitimately-N/A case → bot rollout with a schema-validation gate +
coverage report → fold into the per-crop checklist OR run as a post-roster column pass; amend
already-certified crops with per-field provenance, never a full re-cert).

**Standing principle (load-bearing):** **run a column pass against a STABLE / complete roster, not
mid-certification.** Adding a datapoint while crops are still being certified re-opens already-done
crops *and* bolts the field onto in-flight ones — a moving target. Prefer: finish the roster, then
one clean column pass.

---

## Register

| # | Field | Status | Trigger | Approach | Consumer / notes |
|---|---|---|---|---|---|
| 1 | `growth_stages[].day_range_from_sow` (germination "expect sprouts in ~N days" window) | **folded into #4** (2026-07-07: the timing-spine bundle; the ladder is authored WITH `dtm_anchor`+DTM, not alone) | full crop roster (~123) certified | single **post-roster column pass** (NOT folded into the per-crop checklist this round) | plant-app **seed trays** reads it for the sprout-window line; it **graceful-omits** where absent, so the feature is **not blocked** — the line lights up when this lands. The number is already authored in each germination stage's prose ("in about 5 to 10 days…"), so this is a *structuring* job, not new research. Present today on ~12 of 31 app-certified crops; missing on tray-started annuals (brussels, cabbage, cauliflower, kale, broccoli, pumpkin, butternut, zucchini, zinnia). Legitimately-N/A: crops not grown from seed (perennials/trees — bare-root/nursery). |
| 2 | Establishment-only `calendar[]` for chill-limited `survives_no_fruit` cells (perennials) | **queued** | full crop roster certified | post-roster column pass + **A3 gate amendment**: today the no-fruit split (perennial_gate A3, incognito-audit B2) requires chill-limited `survives_no_fruit` cells to carry an EMPTY calendar (no over-promised bloom/harvest dates). Amend to require an establishment-only calendar instead — plant/growing/dormant/prune/care tokens derived from the region's `plantings[]` + dormancy window via a new `derive_establishment_calendar` beside `derive_tree_calendar`; still ZERO bloom/harvest tokens, so the honesty invariant holds. Cold-edge no-fruit cells (chill met) are unaffected. ~40 cells across 13 tree crops today. | plant-astro guide zone pages render the care timeline under the suitability note ("survives but rarely crops"); currently the calendar section graceful-omits. Product call Trevor 2026-07-02 (origin: sour cherry `ca_interior` z9 — "even if it survives people might still plant it"). |
| 3 | `pet_safe` (pet-friendly vs. not — cats/dogs/horses toxicity) | **queued** | full crop roster certified (post-114) | post-roster column pass. A structured, consumer-facing flag (bool or small enum, e.g. `safe` / `toxic` / `caution`) with per-crop provenance, so plant-astro can render a **quick pet-friendly / not-pet-friendly icon** on each crop. Today the safety fact lives only as PROSE in `failure_diagnostics` (rosemary = safe; chives = toxic, added Wave 4) — inconsistent and un-iconizable. Contract-first pilot must include a legitimately-safe crop, a clearly-toxic one (allium/chives, nightshade foliage, sweet-pea seed, elderberry raw), and a caution case. **Source-tier decision to settle here:** ASPCA's Toxic/Non-Toxic Plants list is the canonical pet-toxicity authority but is non-`.edu` (same class as `rhs`) — decide whether to admit it as the anchor source for this field, alongside the extension `.edu` pages (NCSU plant toolbox tags "problem for cats/dogs/horses"). | Trevor 2026-07-06: wants pet-friendly / not-pet-friendly as a reliable roster dimension, rendered as a **quick icon**; "a big issue... something I want to have and not get wrong." Chives (allium, toxic) + rosemary (safe) already give both poles for the pilot. |

| 4 | **Timing-spine bundle** -- `propagule`, `dtm_anchor`, `sow_depth_inches`, `thin_to_inches`, `harvest_window_days`, `divide_every_years` (+ the pre-existing `growth_stages[].day_range_from_sow` ladder, subsumes register #1) | **in progress** (Phase 1 done 2026-07-07) | full 114 roster certified (MET) | **coupled-bundle** column GS arc: one-time contract + gate layer (`docs/timing_spine_contract.md`, `tools/timing_spine_gate.py`), then author per-crop in archetype batches (garlic pilot -> fall/winter -> rest). NOT a field-by-field sweep -- the ladder only means anything relative to `dtm_anchor`+DTM, and depth/spacing/propagule are archetype-determined. Amend-not-recert with per-field provenance. Fold into the per-crop checklist for new (§E) crops. | plant-app `crop-timing.ts` (already built, graceful): `daysToHarvestFromStage` reads the ladder, `effectiveDtm`/`dtmAnchor` read DTM+anchor, accessors expose depth/window/propagule/thin. Consumer contract: `plant-app/src/lib/guides.ts`. Phase 1 baseline (`4abf43a5`): 1 hard defect surfaced (`shallot` ladder order) + 8 anchor-dependent warnings -- see `docs/2026-07-07-timing-spine-phase1-findings.md`. Absorbs register #1 (`day_range_from_sow`). |

| 5 | `watering.schedule_by_stage[]` -- PER-STAGE watering (rate/amount, frequency, method, level + dual-register notes per growth stage; the "how much to water after sprouts grow" data) | **COMPLETE 2026-07-07 (114/114 certified)** -- authored across 12 batches (W1 tomatoes -> W7 herbs, B8-B9 flowers, B10 microgreens, B11 citrus, B12 woody herbs; canonical `6f584c3b` -> `b15a5a0f`). Each crop authored INDIVIDUALLY from its own certified watering prose (blanket-authoring guarded, per-crop distinctions surfaced every batch); annuals/microgreens got FULL-stage coverage, the 10 perennials (citrus + woody herbs, Trevor's approved judgment call) got the SPARSE tree pattern (3 key-stage entries, subset of real growth-stage ids, blueberry precedent). Gate-clean throughout (whole_crop_gate + register_completeness + dash/temp + release_verify + pre-commit backstop). The 10 crops without it = the uncertified §E shells, correctly excluded. | done | backfilled for annuals using the EXISTING `schedule_by_stage` shape (already on 23 winter + 21 trees/perennials, e.g. the blueberry anchor); per-stage, from certified crop-level watering prose; its OWN focused pass. Paired with the day_range_from_sow ladder (same stage ids). | plant-app per-stage watering guidance (seedling -> established -> mature). Captures germination "keep the surface damp" + post-sprout "water deeply, less often". |
| 6 | PER-STAGE / seedling **LIGHT** (seedling vs mature light need) -- **NEW field, shape TBD** | **candidate** (raised 2026-07-07) | design-first, if a consumer needs per-stage light | today only crop-level `sunlight` / `sunlight_hours` exist -- there is NO per-stage/seedling light field. Adding one is a full column GS arc (contract-first + ruling + gate), like any new cross-crop field. | plant-app seedling light guidance (e.g. avoiding leggy seedlings), IF wanted. Trevor 2026-07-07 flagged it; parked as a candidate pending a decision to add. |

| 7 | STRUCTURED climate **thresholds** -- `heat_threshold_f` + `heat_effect`, `frost_tolerance_f` + `frost_effect`, `chilling_sensitivity_f` (`germination_temp_f` already structured) | **COMPLETE 2026-07-07 (`b15a5a0f` -> Phase 1 `d3a6912f` -> ROLLOUT `6659042d`); all 106 outdoor certified crops carry the 3 fields** | before the notifications + WeatherKit build (~week of 2026-07-14) | Column GS arc. Contract `docs/climate_thresholds_contract.md` (single-value thresholds not bands; heat=daytime-HIGH; coherence frost<chilling<heat; heat null=N/A heat-lover). Gate `tools/climate_threshold_gate.py` (TDD, `--coverage`, `INDOOR_SLUGS`). Trevor confirmed: keep the *_effect enums (make the deterministic alert message accurate) + add `chilling_sensitivity_f` (numeric-only, N/A for cold-adapted crops). Semantic calls: fruit-tree frost = spring BLOSSOM frost ~28F (not winter wood hardiness; fig/pomegranate exception); "chill hours" = dormancy requirement NOT chilling injury; microgreens 8 = N/A-indoor; very-hardy crops use USDA-zone hardiness. C11: heat_effect/frost_effect ruled into register EXCLUDED_KEYS. Coverage: heat SET 46/N-A 60, frost SET 106, chilling SET 29/N-A 77; only TODO = the 10 uncertified §E shells (pick up at certification). **Follow-ons:** fold into the per-crop GS-arc checklist; optional `*_night_f` for the deferred night-temp effects. | plant-app notifications engine + AI context-assembly. Dataset already had partial scaffolding (`hard_freeze`/`FROST_PROTECT` tip tokens) -- these fields give them firing numbers. See memory `notifications-ai-architecture`. |

*(Add a row when a consumer needs a new cross-crop field. Keep status/trigger current.)*

---

## To adopt (cert session)

1. **Surface it where it'll be seen** — add a one-line pointer to plant-dataset `CLAUDE.md` (the file
   every cert session auto-loads), e.g.:

   ```markdown
   ## Adding a cross-crop field
   Before adding any field across crops, follow `docs/gs_cross_crop_field_addition_v0.md` and check
   `docs/field_addition_register.md` (live queue + trigger conditions). Run column passes against a
   stable roster, never mid-certification.
   ```

2. **Graduate the method** from `gs_cross_crop_field_addition_v0.md` (proposal) to `_v1_0` once adopted.
3. **Commit** this register + the note on your terms (left untracked by the plant-app session that
   drafted them — origin: the seed-trays feature design, 2026-06-30).
