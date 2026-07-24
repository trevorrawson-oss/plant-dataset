# Asparagus Certification (Authoring Half) -- `herbaceous_perennial`, crop #120

**Date:** 2026-07-23
**Base canonical:** `ccf5e890` (origin/main `44b3214`, after the design-first archetype arc)
**Predecessor spec:** `docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md` (the DESIGN-FIRST half: archetype + A46 gate + 2-region staged reference, all shipped)
**Scope of THIS arc:** the AUTHORING + CERTIFICATION half. Extend the staged reference to the full
cert bar (all agronomy, all 16 regions, register fields, fuller IPM), fix two gate blockers the
design half did not account for, then one atomic promote of asparagus from honest shell to certified
crop #120 (119 -> 120 certified; 128 total unchanged), full release gauntlet, and the state trio.

---

## 1. What is already done (do NOT redo)

The design-first arc (PUSHED `44b3214`) delivered, and this arc builds on:
- `herbaceous_perennial -> frost_anchored` registered in `calendar_basis_gate.ARCHETYPE_BASIS`.
- The A46 structural gate `tools/herbaceous_perennial_gate.py`, wired into `whole_crop_gate` + picked
  up by `gate_all`, RED-proven (12 defect classes).
- `tools/staging/asparagus_reference.json` -- a T1-clean template: 2 regions (northern_tier z4
  `perennializes`, hawaii_tropical z12 `unsuitable`), 4 varieties with honest T1 resistance grades,
  3 IPM ladders (asparagus beetle / rust / Fusarium crown rot), the perennial fields, start_method,
  succession_policy, planting_layout.

The reference is the proven skeleton. This arc EXTENDS it in staging, then promotes it.

## 2. Decisions ruled by Trevor (2026-07-23 brainstorm)

1. **Gate blocker fix = archetype-scoped carve-out** (see §4). Extend the existing perennial
   exemptions in A34 (cross_consistency Rule 2) and A37 (calendar_coherence Bug 1) to
   `archetype == "herbaceous_perennial"`, TDD RED-proofed. Archetype-scoped, so all 119 certified
   crops are byte-untouched and `gate_all` stays 119/119.
2. **Suitability map = honest-marginal** (see §5). Mark mild-winter-but-growable cells `marginal`
   with a dormancy caveat; reserve `perennializes` for regions with reliable dormancy + a production
   record. Guarantees >= 1 `marginal` cell (the enum value the reference never exercised).
3. **Category = new `"Perennial Vegetables"`** (see §7). UC Master Gardener classifies asparagus as a
   perennial, cool-season STEM vegetable, never "fruiting." Create the category now; asparagus moves
   into it. Artichoke (same archetype, currently `Fruiting Veg`) is re-homed when it certifies (its
   fast-follow arc), not here.
4. **IPM depth = fuller ~5** (see §6). Extend the reference's 3 to the set T1 asparagus pages
   consistently headline: pests = asparagus beetle (common + spotted), cutworm; diseases = rust,
   purple spot (Stemphylium), Fusarium crown and root rot.

Confirmed (not re-litigated): variety depth = the light path (`varieties.recommended` +
`hero_description` + `resistance` map, already in the reference); the dedicated sex-ratio/dioecious
variety archetype stays DEFERRED to a later variety arc (gate it on T1-sourceable-at-variety-
granularity per the shallot-held lesson).

## 3. The cert bar (empirically mapped from `tools/whole_crop_gate.py` + helpers)

`gate_all` runs `whole_crop_gate` on every crop with `verification_status.status == "verified_gs_arc"`
and requires each to print `GATE: PASS`. That IS the machine cert bar. `control_ladder_gate` /
`variety_resistance_gate` are separate (run on scratch). What asparagus must satisfy, by area:

### 3a. Structural / archetype (already satisfied by the reference, keep)
- `archetype:"herbaceous_perennial"`, `calendar_basis:"frost_anchored"` (A30).
- A46: `perennial:true`; `lifecycle` in {perennial,permanent} (reconcile the shell's `"permanent"` ->
  `"perennial"` at promote); `succession_policy.suitable:false` + non-null `reason_seasoned`;
  `years_to_first_harvest`=[2,3] (min>=1), `years_to_full_production`=[3,4],
  `productive_lifespan_years`=18 (positive int); no succession/second_planting planting TRACKS;
  `rotation` present as prose (NOT the shell's null-filled dict); per-cell suitability coherence.

### 3b. days_to_maturity -- the perennial N/A path (LOAD-BEARING)
- Keep `days_to_maturity: []` (explicit EMPTY LIST -- not absent, not null, not a years value).
  `dtm_empty(crop)` returns True only for `== []`, which makes A39 skip `dtm_anchor` and A40 skip the
  `day_range_from_sow` ladder. Do **NOT** author `dtm_anchor` (A40 fails "anchor present but
  days_to_maturity empty"). The 2-3-year establishment lag lives in the A46 establishment fields.
- `days_to_maturity_mid` is un-gated; leave null.

### 3c. Region coverage + zone parity (A31, A45, A2)
- All 16 canonical regions present (shell has only the old 10; MISSING: `pnw, mid_atlantic,
  mid_south, nevada, utah_dixie, rgv`). Each region: `region_id`, `region_label`, `zone_span` ==
  `EXPECTED_SPANS[region]` (string, ascending), `plantings` (non-empty list; single
  `{"track":"perennial",...}` establishment entry, no succession/second_planting track),
  `resolved_by_zone` with a cell per zone in the span, `region_notes_beginner` + `region_notes_seasoned`
  (A2: not both null), `sources`.
- `EXPECTED_SPANS`: northern_tier[3,4,5,6,7], warm_arid[8], ca_interior[8,9], pnw[8,9],
  mid_atlantic[7,8], mid_south[7,8], nevada[8,9,10], utah_dixie[8], se_gulf[8,9,10], rgv[9,10],
  ca_north_coast[9,10], ca_south_coast[9,10,11], ca_desert[9,10,11], low_desert_az[9,10],
  fl_peninsula[10,11], hawaii_tropical[10,11,12,13]. (Total 39 zone cells across 16 regions.)

### 3d. Per-zone cell shape (frost_anchored + herbaceous_perennial)
Each `resolved_by_zone.<z>` cell:
- `calendar`: length-12 list, tokens in `{wait,indoors,plant,growing,harvest,late,cold_pause,
  heat_pause,season_over}` (A5/A32). The established-bed steady state:
  `cold_pause... -> harvest (spring spears) -> growing (summer fern) -> cold_pause (fall dieback +
  winter)`. This is the pattern the §4 carve-out makes legal.
- `suitability` in {perennializes,marginal,unsuitable} (A46). `marginal`/`unsuitable` cells carry
  `suitability_note_seasoned` + `suitability_note_beginner` (CP twin; `suitability_note` is a
  CP_BASE_NAME so both registers required by A36).
- `sources` (list) + `anchoring_urls` (dict): EACH entry `{"url":"https://...","verified":"2026-07-23"}`
  -- the `verified` field is MANDATORY for F and is MISSING on the current reference cells (systematic
  fix on all cells, new + existing).
- `resolution_method` (e.g. `"frost_anchored_resolved"`), `notes` (optional prose).
- Omit `plant_out` / `start_indoors` / `harvest`/`harvest_start`/`harvest_end` on the steady-state
  cells: an established permanent bed is planted once, so an annual planting/harvest window string
  would misrepresent it. (These are all OPTIONAL, not presence-gated. Omitting them keeps A24/A43
  vacuous and matches the "calendar = established-bed steady state" design. The crown-planting window
  lives in `start_method` + `year_one_notes_*`, not the annual month-strip.)
- `unsuitable` cells: all-`growing` 12-token calendar (as the reference's hawaii cell) -- exempt from
  A34/A37 (no `harvest` token) and honest ("if you must, it just sits and declines").

### 3e. Register floor (A39/A40/A41/A42, fire once `verified_gs_arc`)
- `propagule:"crown"` (A40 enum). No `dtm_anchor`, no `sow_depth_inches` (crown is not seed-like).
- `watering.schedule_by_stage`: non-empty list of `{stage_id, system, rate, frequency, level,
  note_seasoned, note_beginner}`, keyed to real `growth_stages` ids.
- Keys must EXIST (values may be null/"na"): `germination_light`, `seedling_light`,
  `heat_threshold_f`, `frost_tolerance_f`, `chilling_sensitivity_f`, `tray_sowing`.
  - `germination_light`: T1 value for asparagus seed (or null since propagule=crown; null is legal
    when propagule != seed). `seedling_light`: `"na"` (crown-started) or `bright_default`.
  - `heat_threshold_f`/`heat_effect`: T1. Likely `heat_effect:"heat_tolerant"` + null threshold
    (ferns tolerate summer heat) OR a real threshold if a T1 source names one -- author from source.
  - `frost_tolerance_f`/`frost_effect`: the FERN is frost-tender (fall dieback) -> `frost_effect:"killed"`
    with a T1 foliage-frost threshold; the CROWN is deeply hardy (that hardiness lives in
    `hardiness_notes_*` + region notes, not this foliage field). Author from a T1 source.
  - `chilling_sensitivity_f`: null (asparagus WANTS chill; it is not chill-sensitive).
  - `tray_sowing`: `"na"`.
- A40 amend-not-recert: a `verification_status.field_additions` entry for the timing-spine columns
  (`propagule` etc.) with all-T1 `sources`.

### 3f. Display-readiness + quality fields (A20, A12, A17, A19/A26/A27, A23, B, A29, A36, C/D, E, F, G)
Author to non-null, dual-register, T1-anchored:
- `sunlight` (raw-display token, no snake_case), `sunlight_hours` [lo,hi] in [1,18], `water`,
  `watering.*`, `ph` (`preferred_range` + `tolerated_range` nested + `note_seasoned`/`_beginner` whose
  stated pH agrees within 0.5 of preferred_range -- A34 Rule 1), `spacing_inches` [lo,hi] <=72,
  `germination_temp_f` [32,110], `soil` + `soil_prep_*`.
- `fertilizer.type/timing/frequency` (no snake_case) + NPK (`npk_ratio` "N-P-K" if `npk_hint_*`
  present, A17).
- `growth_stages` (non-empty; the establishment/dormancy stages) + `tips_by_stage` (every stage id
  has a `text_seasoned`/`text_beginner` tip -- A12 coverage).
- `notifications`, `weather_triggers`, `failure_diagnostics`, `pests`, `diseases` non-empty (A12).
- `container_notes.container_ok` (real bool; asparagus is a poor container crop -> likely false with a
  prose reason).
- `description_beginner`/`description_seasoned` (with the variety fold-in), `hardiness_notes_*`,
  `harvest_ready_beginner`/`_seasoned` (+ `harvest_ready_sources`/`_anchoring_urls`), `storage`,
  `year_one_notes_*` (the establishment-year deviation), `sources_summary`.
- Every sourced leaf: `sources` all in `source_catalog` + tier T1 (E), paired `anchoring_urls` with
  `url`+`verified` (F). All four reference source ids (`umn_ext`, `msu_ext`, `rutgers_njaes`,
  `uc_ipm`) already exist in `source_catalog` as T1; author may add more T1 ids (e.g. UC IPM asparagus
  pages, UMass, Cornell) -- new source_catalog entries must be T1 with real publisher/url.
- `verification_status`: `status:"verified_gs_arc"`, `launch_ready_core:true`,
  `launch_ready_seasoned:true`, clean `open_findings` (no `blocks_launch:true` unresolved -- G), a
  `verification_log_ref`, `source_set`, `field_additions` (timing-spine).

### 3g. planting_layout (A44) -- FIX
The reference dict `{"pattern":"rows",...}` CRASHES A44 (`pl not in LAYOUTS` where LAYOUTS is a string
set -> TypeError). Set `planting_layout:"row"` (the enum string; not `"block"`, so no
`pollination_block_min_rows`). The row/in-row spacing detail moves to prose (`spacing_inches`,
`soil_prep_*`, region notes) until the planner-arc widens A44 to accept the dict form.

### 3h. Legacy top-level `zones{}` -- leave as the null shell (un-gated; do not fill).

## 4. The gate blocker + carve-out (the discovered gap)

The design-first spec accounted for A5/A24/A28 but NOT A34/A37. Asparagus's honest steady-state
calendar `[cold_pause, harvest (spring), growing (summer fern), cold_pause]` fails:

- **A37 Bug 1** (`calendar_coherence_gate.py:120` `growing_reachability_violations`): a `growing`
  token must be backward-reachable from a `plant`/`indoors` without passing `harvest`/`season_over`.
  The summer fern `growing` sits AFTER the spring `harvest`, so it traces back to `harvest` (a
  BLOCKER) -> flagged. **No token arrangement avoids this** (the fern genuinely grows after harvest;
  verified empirically). The gate's own docstring already exempts this exact pattern for non-
  frost_anchored crops: "an evergreen perennial legitimately grows after harvest."
- **A34 Rule 2** (`cross_consistency_gate.py:71` `cross_consistency_violations`): a frost_anchored
  cell rendering a `harvest` token must also carry a plant-class token. A permanent bed planted years
  ago has no annual plant token. The gate's own docstring already exempts this for non-frost_anchored:
  "trees/berries plant once at establishment, not in the annual month-strip."

**Fix (both, TDD RED-proofed):** extend each existing exemption to the archetype.
- `calendar_coherence_gate.growing_reachability_violations`: after the
  `if crop.get("calendar_basis") != "frost_anchored": return []` line, add
  `if crop.get("archetype") == "herbaceous_perennial": return []` (the fern-after-harvest is the
  frost_anchored analog of the evergreen exemption). Update the docstring.
- `cross_consistency_gate.cross_consistency_violations` Rule 2: change the guard from
  `if crop.get("calendar_basis") == "frost_anchored":` to also skip when
  `crop.get("archetype") == "herbaceous_perennial"` (an established permanent bed is planted once, like
  trees/berries). Keep Rule 1 (pH) firing for all crops. Update the docstring.

**RED-proof (the CLAUDE.md hard rule -- a gate isn't done until a defect is sneaked at it and caught):**
- REGRESSION (the carve-out must NOT weaken enforcement for annuals): a NON-herbaceous_perennial
  frost_anchored crop with `harvest` but no plant token STILL bounces A34 Rule 2; a frost_anchored
  annual with an impossible `growing`-after-`harvest` STILL bounces A37 Bug 1.
- GREEN: asparagus's real harvest->fern cells now pass both.
- SCOPE: `gate_all` stays 119/119 (run it -- no certified crop carries the archetype, so none is
  perturbed).

Both carve-outs are single-condition, archetype-scoped, and mirror logic each gate already contains.

## 5. The 16-region suitability map (each cell T1-verified during authoring)

Per-CELL suitability (a region can mix values across its zones). Author a full established-bed cell
(calendar + suitability + notes + sources) for every zone in every region's `EXPECTED_SPANS`.

| Region (zones) | Suitability | Basis (T1-verify) |
|---|---|---|
| northern_tier (3-7) | **perennializes** | cold winters, textbook dormancy (reference did z4) |
| warm_arid (8) | **perennializes** | real winter dormancy; grown across the interior West/plains z8 |
| utah_dixie (8) | **perennializes** | z8 winter chill sufficient |
| mid_atlantic (7,8) | **perennializes** | Mid-Atlantic winters give full dormancy |
| mid_south (7,8) | **perennializes** | Upper/Mid South z7-8 dormancy sufficient |
| pnw (8,9) | **perennializes** | WA/OR are major producers; cool wet maritime winters |
| ca_interior (8,9) | **perennializes** | the Sacramento/San Joaquin DELTA is the #1 US region -> z9 perennializes here |
| nevada (8,9,10) | **perennializes** z8,z9 / **marginal** z10 | high-desert winters cold at z8-9; z10 mild-winter marginal |
| se_gulf (8,9,10) | **marginal** (z8 possibly perennializes) | humid Southeast: z8 grows w/ dormancy but heat+rust pressure; z9-10 mild-winter marginal -- T1-verify the z8 call |
| ca_north_coast (9,10) | **marginal** | cool maritime, frost-poor winters -> imperfect dormancy |
| ca_south_coast (9,10,11) | **marginal** z9,z10 / **unsuitable** z11 | mild winters -> marginal; z11 frost-free -> unsuitable |
| ca_desert (9,10,11) | **marginal** z9 / **unsuitable** z10,z11 | low-chill hot desert; z9 marginal, hotter zones unsuitable |
| low_desert_az (9,10) | **unsuitable** | extreme summer heat + low chill (Phoenix/Yuma); design pre-ruled |
| rgv (9,10) | **unsuitable** | subtropical S. Texas, no sustained dormancy |
| fl_peninsula (10,11) | **unsuitable** | subtropical/tropical, no dormancy |
| hawaii_tropical (10-13) | **unsuitable** | tropical, no dormancy (reference did z12) |

Guarantees multiple `marginal` cells (decision #2). Every cell's suitability call is T1-sourced;
where a source is thin or conflicting, prefer the more conservative (`marginal` over `perennializes`,
`unsuitable` over `marginal`) and record the modeling basis in the cell/region notes + an
`open_findings` entry if confidence is low (severity low, blocks_launch false).

## 6. IPM (fuller ~5, decision #4)

Extend the reference's ladders (asparagus beetle / rust / Fusarium) to add, from T1 sources:
- **cutworm** (pest, `type:"insect"`): ladder from existing `control_methods` (handpick,
  garden_sanitation, stem_collars/beneficial_nematodes, Bt/spinosad, pyrethroid rescue).
- **purple spot / Stemphylium** (disease, `type:"fungal"`): ladder (resistant_varieties?,
  airflow_spacing, garden_sanitation / fern removal, sulfur or copper_fungicide) -- T1 (MSU/UMass name
  it a fern + spear-blemish disease).
All ladder `method` ids must resolve in the `control_methods` catalog (add a new catalog method ONLY
if a rung has no home, authored from a fetched T1 page -- prefer reuse). Problem `type` uses
`fungal` (NOT "disease"). The `control_ladder` A39 hard-flip is still deferred, so legacy `pests`/
`diseases` shape is cert-legal, but author to the ladder standard (no retrofit for artichoke later).
Validate with `control_ladder_gate` on a scratch merge.

Variety `resistance` maps: keys must match `diseases[].id`. With purple spot added, Millennium may
carry `purple-spot:susceptible` (MSU rates it more susceptible to rust AND purple spot); Jersey Knight
`tolerant`. T1-ONLY per grade -- never encode an unsourced grade (the design half caught a fabricated
Millennium rust=resistant; MSU says susceptible). Cross-check every grade against a FETCHED T1 page
(raw HTML/PDF, not a WebFetch markdown table -- the column-shift lesson).

## 7. Category = new `"Perennial Vegetables"`

- Set `asparagus.category = "Perennial Vegetables"`. No category-vocabulary gate exists (verified), so
  a new value is dataset-safe.
- **Frontend note (NOT this repo):** a new category value affects plant-astro's category grouping /
  rendering (the dataset-shape-change-breaks-frontends lesson). Flag it for the plant-astro session
  (Trevor-gated bump); grep plant-astro for the category list and confirm it renders an unknown
  category gracefully before the submodule bump. Out of scope for the dataset cert here, but recorded.
- Artichoke stays `Fruiting Veg` until its cert arc, when it is re-homed into `Perennial Vegetables`
  (both herbaceous_perennial). Record this as an explicit follow-on.

## 8. Promote plan (the one atomic canonical write)

Until this point, `crops_data_final.json` is READ-ONLY (CLAUDE.md); all authoring lives in
`tools/staging/asparagus_reference.json`. The promote:
1. Finalize the extended reference (all §3 fields, 16 regions, register fields,
   `verification_status.status:"verified_gs_arc"`, `category:"Perennial Vegetables"`,
   `lifecycle:"perennial"`, `planting_layout:"row"`, `verified` on every anchoring_urls entry).
2. Deterministic splice script (`tools/` one-off): load canonical, replace the `asparagus` crop dict
   with the finalized reference crop, add any new `source_catalog` / `control_methods` entries, dump
   COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never indent). Verify
   ONLY asparagus (+ catalog additions) changed vs base (release_verify invariant A).
3. The crop count stays 128; certified goes 119 -> 120.

## 9. Cert gauntlet (CLAUDE.md protocol #6, before any push)

1. `python3 tools/whole_crop_gate.py asparagus crops_data_final.json` -> `GATE: PASS` (all A-gates).
2. `python3 tools/gate_all.py crops_data_final.json` -> 120/120 certified PASS (asparagus now in the
   certified roster; all others unperturbed).
3. `python3 tools/release_verify.py` -> clean (only asparagus changed; reference crop byte-identical;
   no new violations).
4. `control_ladder_gate` + `variety_resistance_gate` on the canonical (now inclusive of asparagus) ->
   0 violations.
5. The A34/A37 carve-out RED battery (regression + green + scope) re-run.
6. Per-batch source-truth sample: spot-check a sample of authored T1 claims (agronomy numerics,
   resistance grades, suitability calls) against the FETCHED source pages.

## 10. State trio + register (at content release)

- Regenerate `CURRENT_STATE.md` via `tools/gen_current_state.py`, fill prose slots. (NOTE the
  current-state-md-drift lesson: the file has no `---` separator and is hand-maintained surgically --
  confirm the generator does not corrupt it; if it would, hand-edit.)
- Append `STATE_HISTORY.md` (most-recent-first).
- Bump `LATEST.txt` (new SHA + session line).
- Field-addition register row IF a field is added. (Likely a row for the new `category` value +/or
  any new register/catalog additions; `category` itself is an existing field with a new value, so
  assess whether a register row is warranted vs a state-history note.)

## 11. Verification / sequencing (subagent-driven-development, fresh subagent per task)

Ordered so each stage's output is gate-validated before the next depends on it:
1. **Gate carve-outs (§4)** -- TDD: RED (regression bounces) -> GREEN (carve-out) -> gate_all 119/119.
   Commit. (Do first: nothing else can gate-pass a productive cell until this lands.)
2. **planting_layout + anchoring_urls `verified` fixes (§3g, §3d)** on the reference. Commit.
3. **Full agronomy fan-out (§3f)** authored into the staged reference (T1). Fresh sourcing subagent +
   a T1-FIDELITY review. Commit.
4. **16 regions (§3c/§3d/§5)** -- author all 39 zone cells with suitability + calendars. Validate
   A31/A45/A46/A32/A5/A24/A34/A37 on a scratch merge. Commit.
5. **IPM fuller set + variety resistance keys (§6)** extended; control_ladder_gate + variety_
   resistance_gate clean on scratch. Commit.
6. **Register floor (§3e)** + category (§7) + lifecycle reconcile + verification_status ->
   verified_gs_arc. Commit.
7. **PROMOTE (§8)** -- splice into canonical (the one atomic write). 
8. **CERT GAUNTLET (§9)** + T1 source-truth sample. If clean:
9. **STATE TRIO + register (§10)**. Commit.
10. **Checkpoint Trevor**; push is Trevor-gated. plant-astro bump is a separate astro-session concern
    (Trevor coordinates; he has concurrent plant-astro sessions -- different repo, no overlap, but the
    new `category` value is a heads-up for that session).

Every authored value is T1-sourced (.edu / government extension); a dedicated T1-FIDELITY review runs
on all authored content (agronomy numerics, resistance grades, region suitability calls), fetching the
real page (raw HTML/PDF, not a WebFetch markdown table) and dropping rather than fabricating any claim
that does not verify.

## 12. Explicitly deferred (out of scope here)

- **Artichoke** on the same `herbaceous_perennial` archetype (the fast-follow; also re-homes it into
  `Perennial Vegetables`).
- The dedicated **sex-ratio/dioecious variety archetype** (per-variety yield/sex schema) -- a later
  variety arc, gated on T1-sourceable-at-variety-granularity.
- The `control_ladder` **A39 hard-flip** / roster-wide rollout.
- The plant-astro **submodule bump** + the new-category frontend handling (astro session, Trevor-gated).
- The **planner-arc** widening of A44 to accept the `planting_layout` dict form (row/in-row spacing).

---

## Appendix: load-bearing facts + gotchas (carried from the design arc)

- Canonical JSON is COMPACT; READ-ONLY until the §8 promote (stage first).
- No em dashes in consumer copy; American English; temps render `°F`; "ladybug" not "lady beetle".
- frost_anchored + perennial:true certifies cleanly (A3 no-ops) -- proven by chives/mint/bee-balm.
- control_ladder problem `type` = `fungal` (the gate's TYPE_TARGETS has no "disease").
- `resistance` map GRADES = {immune,resistant,tolerant,susceptible}; keys == `diseases[].id`.
- T1-OR-DROP: verify EVERY resistance grade + agronomy numeric against a FETCHED T1 page; WebFetch
  silently shifts HTML data-table columns and WebSearch summaries invent pages -- fetch raw HTML/PDF +
  cross-check; drop rather than fabricate.
- `days_to_maturity: []` (empty list) is the perennial N/A sentinel; never add `dtm_anchor`.
- every `anchoring_urls` entry needs `{"url","verified":"YYYY-MM-DD"}`.
- Don't commit until Trevor approves each change; push + astro bump are Trevor-gated.
