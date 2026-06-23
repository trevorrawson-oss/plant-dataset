## 2026-06-23 -- zucchini_steps6-8_author (claude.ai author lane)

**Crop:** zucchini-courgette (anchor; `warm_season_fruiting`)
**Arc position:** Steps 6-8 (consumer prose + the 7 compounds) -- the FINAL authoring leg before cert.
**Base (in):** crop SHA `fd8174dec57ceb0d9e7ce66755902144e70e4f31d3f071e24fb2bc3ec8b1ba25` @ full-file `642f4890`
**Out:** crop SHA `4950084db4ab91fb1bd5b5624ba9415a52867e3af1e5892d6410c85fb19b45eb` (author lane; NOT yet applied/promoted)

**Preflight caught a base/kickoff denominator mismatch** (file walk = 285 nulls + 120 empties vs kickoff "78 + 7"). Three structural forks surfaced to Trevor; release-lane adjudicated all three: (1) `zones{}` confirmed DEAD/gate-excluded -> ignored; (2) region window arms + per-cell `zone_notes/planting_note/notes` left null (optional/4-5.5 rule-layer, reconciled at release) -> guidance went into region-summary `region_notes_*`; (3) 4 traditional companion `verified_date` nulls left as correct honest state. Gap fully explained (dead zones + structural arms + optional/no-evidence fields).

**Authored:** `description_*`, `harvest_ready_*`; all 10 `region_notes_*` pairs (derived per-region from 4-5.5 windows + provenance, A5-clean); depth-lifted `fertilizer` (MODERATE-feeder, stage_id->flowering), `watering` (base-water/mildew nexus), `container_notes` deep prose (`overwintering.applicable:false` N/A prose; `shape_requirements` re-authored; `self_watering_ok:true`), `rotation` (3yr, avoid cucurbits), `storage` (tender/not-a-keeper), `yield_expectations` (+5-item `factors_seasoned`), `moon_phase_preference.source_note_seasoned` (N/A); all 7 compounds with stage-id-keyed A12-conformant `tips_by_stage`, `growth_stages` (6), `pests` (svb-lead, squash bug, cucumber beetle), `diseases` (powdery-mildew-lead, bacterial wilt), `failure_diagnostics` (4-slot), `notifications` (3), `weather_triggers` (2). `first_planting_notify_days:3`; `last_reviewed` stamped. `verification_status` NOT set (Step 11).

**Gauntlet:** all 6 gates PASS -- register-fill 0 unexpected; dual-voice 0 missing/0 null; A12 conformant; copy rules clean (7 °F, 0 em-dash/`--`/"degrees F" in consumer; provenance-only "degrees F" exempt); collateral 0 unexpected + 0 key-delta; region-window integrity 0 drift. 8-gram self-scan: 6 overlaps all vs own provenance (intended), 0 vs source_quote (none in slice).

**Release-review flags:** anchoring reuses existing parents + specific-page URLs (no new sub-id mints) -- Step 11 fetch to confirm URLs; numeric thresholds to confirm (41°F chilling, 6-10 lb/plant); N/A-prose rulings logged. Carry-forwards unchanged: hawaii year_round vs CTAHR B-91, warm_arid z8 vs NMSU CR457, desert heat_pause (A5-confirmed).

**Next:** Claude Code preflight `642f4890` -> apply -> `whole_crop_gate` (residual -> 0) + register gates + A12 gate + `release_verify` -> promote -> Step 9 (dash/temp sweep) -> Step 11 cert (+ the 3 carry-forwards + flip). Parallel: broccoli 4-5.5 region-fill leg.
