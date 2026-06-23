# Zucchini / Courgette -- Steps 6-8 Authoring Findings

**Session:** `zucchini_steps6-8_author` (claude.ai author lane)
**Date:** 2026-06-23
**Base (in):** crop SHA `fd8174dec57ceb0d9e7ce66755902144e70e4f31d3f071e24fb2bc3ec8b1ba25` at full-file `642f4890`
**Post-author (out):** crop SHA `4950084db4ab91fb1bd5b5624ba9415a52867e3af1e5892d6410c85fb19b45eb`
**Scope:** Steps 6-8 -- consumer prose (depth-lifted seasoned + every beginner sibling) + the 7 compounds. Region windows/calendars (4-5.5) untouched. Cert flip (Step 11) NOT set.

---

## 0. Preflight outcome -- a base/kickoff mismatch was surfaced and adjudicated BEFORE authoring

The slice crop SHA matched `fd8174de` exactly (no drift, correct base). But a full null/empty walk of the slice returned **285 nulls + 120 empty containers**, not the kickoff's "78 register-prose nulls + 7 empty compounds." Three structural forks were surfaced to Trevor rather than resolved unilaterally; all three were adjudicated by the release lane and authoring proceeded on those rulings:

1. **`zones{}` (legacy 3-11) is fully empty/vestigial.** Confirmed DEAD: deprecated pre-region-primary layer, both gates exclude `/zones/` paths, region-primary is fully live, cert reads `regions{}`. -> Authored only `regions{}` + top-level prose; left `zones{}` alone.
2. **Empty `regions.*.plantings[].harvest_start/harvest_end` + per-cell `zone_notes/planting_note/notes`.** Adjudicated: window arms are a minor 4-5.5 rule-layer item (resolved cells already carry the full harvest band; nothing renders wrong), reconciled at release lane. Per-cell annotations are OPTIONAL single-register (green-beans certified with all null); required region prose is the region-summary `region_notes_*` pairs. -> Left both null; put all regional guidance in `region_notes_*`.
3. **Four null `companions.*.provenance.verified_date`** (Borage, Sage, Potatoes, Fennel). Adjudicated: all 4 are traditional/folklore companions with `verified_against_sources:false`; null `verified_date` is the correct honest state, and `register_completeness` treats them as accepted deferred Sec.5 companions. -> Left null; no fabricated attestation.

The "78" vs "285" gap is fully explained by: the dead `zones{}` block (~90 nulls), the 4-5.5 region structural arms, optional per-cell annotations, and the no-evidence/deferred fields above. The genuine Steps 6-8 prose surface is the subset authored below.

---

## 1. What was authored (the worklist, walked from the file, not hand-listed)

### Top-level descriptive prose
- `description_seasoned` / `description_beginner` -- the warm-season summer-squash overview; the two season-shaping beats (pests + pace).
- `harvest_ready_seasoned` / `harvest_ready_beginner` -- harvest cue: 6 to 8 in, glossy, thumbnail-dents, cut don't twist, before it turns to a marrow.

### Region notes -- all 10 regions (`region_notes_seasoned` / `region_notes_beginner`)
Each pair DERIVED from that region's own authored 4-5.5 windows + `plantings_provenance` (A5: rests on the region's own T1 findings, never analogized). Region's existing `sources` array reused; no new region sources minted.
- **northern_tier** -- single continuous summer window, direct-sow after frost at soil >=70F, indoor-start option z3-z5, 3-week cadence, fall replacement counted back from first frost.
- **se_gulf** -- true spring+fall split with a hot midsummer no-plant gap; south-GA-earlier/north-GA-later shift.
- **ca_interior** -- one long continuous warm window, heat is the productive core (not a pause), fall taper on virus/whitefly.
- **ca_north_coast** -- continuous but heat-LIMITED by marine layer; later start, slower bloom, nights >55F.
- **ca_south_coast** -- one long continuous window, marine-limited, explicitly NOT year-round (frost-tender annual).
- **ca_desert** -- spring+fall split around a too-hot summer; southern desert valleys can sow Dec-Jan.
- **warm_arid** -- continuous single window at higher-elevation z8 (mirrors green-beans warm_arid finding); no documented summer gap.
- **low_desert_az** -- spring+fall split, long May-Aug no-plant gap; spring extendable to mid-April if established before heat.
- **fl_peninsula** -- inverted season: cool half continuous, Jun-Aug is the off-season.
- **hawaii_tropical** -- bounded-continuous (NOT year_round); wet-season disease/insect pressure the limiter, not cold.

### Structured-block prose (seasoned depth-lift + beginner sibling + block anchoring)
- **fertilizer** -- authored on the **MODERATE-feeder** profile (UMD "Medium requirement"). `amount`/`notes`/`notify_message`/`npk_hint` pairs; the over-N pitfall + moisture nexus. `stage_id` wired to `flowering`. Structured fields set (`frequency`, `type`, `timing`, `example_product`, `notify_days_after`=35). Anchored `umd_ext`, `umn_ext`.
- **watering** -- base-water / dry-foliage / powdery-mildew nexus; ~1 in/week; misshapen-fruit-from-uneven-water beat; critical at flowering/fruit-set. `frequency`/`amount`/`method`/`signs_over`/`signs_under`/`method_note`/`critical_periods` pairs. (existing `watering_method:base`, `drought_tolerance:low`, sources preserved.)
- **container_notes** deep prose -- `notes`/`soil_mix.type`/`soil_mix.amendments`/`watering_adjustment`/`fertilizer_adjustment`/`self_watering_notes` pairs + `drainage.saucer_practice`. **`overwintering.applicable:false` -> N/A PROSE** (annual, frost-killed). `self_watering_ok:true`. **`shape_requirements` re-authored** (dropped at Steps 1-3) as a real dual-voice pair: big sprawling plant needs wide/deep >=10 gal, >=12 in.
- **rotation** -- `rotation_years:3`; avoid following cucurbits (cucumber/melon/pumpkin/squash); `good_after` legumes/greens/alliums; clear-don't-till beat. Anchored `umn_ext`, `iastate_ext`.
- **storage** -- tender, NOT a keeper: ~couple days room temp, ~1 week fridge perforated bag, chilling-sensitive below ~41F, freezes shredded/blanched. Anchored `umn_ext`, `ucd_postharvest`.
- **yield_expectations** -- prolific (6-10 lb/plant), pick young/every 1-2 days at peak, 1-2 plants feed a household; `factors_seasoned` single-register list (5 factors). Anchored `umn_ext`, `iastate_ext`.
- **moon_phase_preference.source_note_seasoned** -- N/A prose (no-evidence field, carrot precedent). `phase`/`evidence_tier` left null by design (no evidence to assert).

### The 7 compounds (Step 8 + A12)
Stage ids defined FIRST and equal to the existing `tips_by_stage` buckets: `germination, seedling, established, flowering, harvest, end_of_season`. `fertilizer.stage_id` + growth-stage notifications keyed to these ids.
- **growth_stages** (6) -- germination -> seedling -> established/vining -> flowering (monoecious male-then-female beat) -> harvest (pick-young/often) -> end_of_season. Each: `what_to_look_for`/`user_action`/`log_prompt` + `_beginner`.
- **tips_by_stage** -- A12-conformant: dict keyed by the 6 stage ids, each a non-empty LIST, every tip uses `text_seasoned`/`text_beginner` (no `tip_*`). Core tips carry beginner siblings; the one `audience:seasoned` tip (svb frass scouting) carries prose only.
- **pests** (3) -- LEAD **squash vine borer** (the wilt+frass signature; the reason the fall succession exists), then **squash bug**, **cucumber beetle** (the wilt vector -> ties to diseases). All 4 fields + `cause_beginner`.
- **diseases** (2) -- LEAD **powdery mildew** (base-water nexus, resistant varieties, airflow), then **bacterial wilt** (cucumber-beetle-vectored, ooze-test). All 4 fields + `cause_beginner`.
- **failure_diagnostics** (4) -- poor-pollination blossom-end rot (ties to `self_fertile:true`/`pollinator_notes`), hidden-marrow, borer/wilt collapse, mildew defoliation. `label`/`what_happened`/`next_season_tip` + cause, all dual-voice.
- **notifications** (3) -- `svb_watch` (offset `established`), `succession_sow` (offset `flowering`), `harvest_check` (offset `harvest`); `title`/`body` + `_beginner`; machinery carries no sibling.
- **weather_triggers** (2) -- `frost_warning` (offset `first_frost`, warning), `heat_pollination` (info); `title`/`body` + `_beginner`; machinery no sibling.

### Bookkeeping
- `first_planting_notify_days:3` (top-level, pairs with notify system; matches `succession_policy.notify_days_before`).
- `last_reviewed:2026-06-23`, `last_reviewed_session:zucchini_steps6-8_author`. **`verification_status` NOT touched** (Step 11, Claude Code).

---

## 2. Validation gauntlet -- all 6 gates PASS

1. **Register-fill:** 0 unexpected nulls. (Allowed-to-remain: dead `zones{}`, per-cell annotations, region window arms, 4 companion verified_dates, moon phase/tier, nullable machinery `offset_from`, pre-existing base structural nulls.)
2. **Dual-voice coverage:** 0 missing + 0 null `_beginner` siblings across the whole crop. (Companion `*_seasoned[]` arrays correctly single-register by visibility-array design; `source_note_seasoned` single-register by design.)
3. **A12 tips conformance:** `tips_by_stage` keyed to all 6 real stage ids, every list non-empty, `text_*` shape (no `tip_*`); `fertilizer.stage_id` + growth-stage notification offsets are real ids.
4. **Copy rules (consumer strings only):** 0 em-dash, 0 `--`, 0 "degrees F", 0 smart-quote/en-dash; 7 `°F` symbols. ("degrees F" appears only in two PRE-EXISTING `plantings_provenance` backend fields, which are exempt.)
5. **Collateral-change audit:** every changed top-level key within the intended set; 0 unexpected; 0 key-delta (none added/removed).
6. **Region-window integrity:** 0 drift in any `regions.*` field other than the two `region_notes_*` keys (windows/calendars/plantings/resolved_by_zone byte-identical to base).

**Numeric fidelity self-audit:** authored numbers are consistent with base structured fields (`germination_temp_f:[70,95]`, container gal/depth, soil/start_method temps already authored) and standard extension ranges. See Sec.3 flags for the specific thresholds the Step 11 live-page fetch should confirm.

**8-gram verbatim self-scan:** 6 overlaps, ALL against this crop's own backend `plantings_provenance` (intended derivation of region_notes from provenance), NONE against any `source_quote` (the slice contains zero source_quote fields). No copyright concern in-lane. The authoritative source-fidelity scan vs live T1 pages is release-lane Step 11 work (source URLs are not in author-lane scope).

---

## 3. LABELED items for release review

### 3a. Source anchoring -- reused existing parents with specific-page URLs (NO new sub-id mints)
Every compound/block I anchored reuses an **existing trusted parent id** from the 122-parent catalog with a specific-page URL in `anchoring_urls`, matching the pattern the base blocks already use (e.g., base `watering` uses parent `umn_ext` with a specific squash-page URL). I did **not** mint new specific-page sub-ids, to avoid asserting exact publication numbers I cannot verify in this lane.
- Parents used for new anchoring: `umd_ext`, `umn_ext`, `iastate_ext`, `clemson_hgic`, `ucd_postharvest`, `uc_ipm`.
- **Release-lane action:** the Step 11 source-fidelity WebFetch should confirm each `anchoring_urls` URL resolves and supports the claim. If the project prefers minted specific-page sub-ids over parent+URL for these, that is a release-lane normalization. The specific new URLs introduced (not previously in the slice):
  - `umn_ext`: `/yard-and-garden-insects/squash-vine-borers`, `/squash-bugs`, `/striped-cucumber-beetles`, `/plant-diseases/powdery-mildew-vegetables`, `/diseases/bacterial-wilt-cucurbits`
  - `iastate_ext`: `/hortnews.../squash-vine-borer`, `/encyclopedia/squash`
  - `clemson_hgic`: `/factsheet/cucumber-squash-melon-other-cucurbit-insect-pests/`
  - `umd_ext`: `/resource/cucumber-beetles-vegetables`, `/resource/growing-summer-squash-zucchini-home-garden`
  - `ucd_postharvest`: `/produce-facts-sheets/squash-summer`
  - `uc_ipm`: `/PMG/GARDEN/VEGES/DISEASES/powderymildew.html`, `/.../bacterialwilt.html`

### 3b. Numeric thresholds to confirm at Step 11 (beyond what base structured fields already lock)
- **41°F chilling-sensitivity** (`storage.fridge_seasoned`) -- cited `ucd_postharvest`; standard UC Davis summer-squash figure, confirm against the produce-facts page.
- **6 to 10 lb per plant** (`yield_expectations.per_plant_seasoned`) -- cited `umn_ext`/`iastate_ext`; confirm the range.
- **5 to 10 days germination** (`growth_stages` germination) -- standard; low risk.

### 3c. N/A-prose rulings applied (never null)
- `container_notes.overwintering.applicable:false` + `approach_seasoned`/`approach_beginner` = explicit "Not applicable" prose (annual, frost-killed).
- `moon_phase_preference.source_note_seasoned` = explicit no-recommendation prose; `phase`/`evidence_tier` null by no-evidence design (carrot precedent).

### 3d. Carry-forwards into Step 11 (unchanged from kickoff, NOT resolved here -- author lane)
- hawaii `year_round` upgrade vs CTAHR B-91 (authored bounded-continuous; the slice's hawaii provenance already flags the upgrade path for the release fetch).
- warm_arid z8 NMSU CR457 confirm (authored continuous; provenance carries the split-if-contradicted flag).
- desert `heat_pause` (already A5-confirmed).

---

## 4. Handback

- **Authored slice:** `zucchini-courgette_authored_slice.json` (pretty) + `.min.json` (minified, dataset convention).
- **Post-author crop SHA:** `4950084db4ab91fb1bd5b5624ba9415a52867e3af1e5892d6410c85fb19b45eb`.
- **Apply base (Claude Code):** preflight `sha256(crops_data_final.json) == 642f4890...` (`LATEST.txt`) before applying; paths are zucchini-crop-relative.
- **Then:** `whole_crop_gate` (residual should fall to 0) + `register_completeness` + `register_fill` + the A12 compound gate + `release_verify` -> promote -> **Step 9** (whole-crop dash/temp sweep) -> **Step 11** cert (source-fidelity fetch + the 3 carry-forwards + the flip).
