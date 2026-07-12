# Onion Variety Pilot -- Design Spec (the PHOTOPERIOD archetype)

- **Date:** 2026-07-12
- **Status:** design, pending Trevor review
- **Canonical at design time:** `a6ead469` (count 125, 116 certified)
- **Arc:** variety-DTM load-bearing + Phase 4 variety expansion -- the **photoperiod-annual** archetype
  pilot, the third variety archetype after dry-bean (DTM-annual) and apple (tree-fruit).
- **Related specs:** `docs/superpowers/specs/2026-07-11-apple-variety-pilot-design.md`,
  `2026-07-11-dry-bean-variety-pilot-design.md`, `2026-06-16-onion-photoperiod-model-design.md`
- **Related memory:** `apple-variety-pilot-tree-archetype`, `variety-dtm-load-bearing-deferred`,
  `onion-photoperiod-model`, `trevor-north-star-accuracy-authority`

---

## 1. Context and goal

Dry-bean proved the flat per-variety schema on the **DTM-annual** archetype; apple proved it on the
**tree-fruit** archetype (season-only, chill-gated). Onion is the **photoperiod-annual** archetype:
a DTM annual whose varieties ALSO carry a day-length class that gates where they will bulb. It is the
first crop with **two** load-bearing per-variety dimensions -- `days_to_maturity` (harvest timing, the
dry-bean lane) AND `day_length_type` (regional viability, the apple-chill parallel).

Onion is **not greenfield** (like apple): it already carries a rich crop-level `photoperiod` model
(dual-register long/intermediate/short-day explainers tied to latitude, T1-sourced tamu_agrilife +
piedmont_mg), per-region/zone `recommended_day_length_type` + latitude notes, and 6 recommended
varieties each carrying `day_length_type`. Critically, **the photoperiod honesty engine already
exists and is gate-enforced** (A9 `photoperiod_gate`, spec 2026-06-16): it validates variety typing,
enforces the COVERAGE invariant (every day-length type a region resolves to must have >=1 recommended
variety carrying it) and WINDOW-FIT (long-day = spring-planted, short-day = fall/winter-planted). So
this pilot is **schema enrichment**, not honesty-engine design.

Trevor's driver: extend the honest variety layer to the photoperiod archetype so the app can show, per
latitude, the RIGHT onions with full per-variety detail ("you are in the North; grow long-day types
like Walla Walla") -- the accuracy/authority play. North star: `trevor-north-star-accuracy-authority`.

## 2. Where onion sits (not greenfield)

- **Crop-level:** `days_to_maturity` `[90,120]`, `dtm_anchor: from_planting`, `calendar_basis:
  frost_anchored`; a sourced `photoperiod` object (dual-register explainer of the 3 day-length classes
  by latitude threshold).
- **Per-region/zone:** `recommended_day_length_type` (e.g. northern_tier z3 = long_day) +
  `day_length_note_beginner`/`_seasoned` (the "at your latitude, grow X" guidance).
- **Per-variety (6 today):** `name`, `use`, `day_length_type` (long/intermediate/short), a single
  `recommended_note`. NO per-variety DTM, id, maturity_class, is_reference, confidence_tier, sources.
- **Gate:** A9 `photoperiod_gate` (fires on `photoperiod` in gating_factors) already enforces variety
  typing + coverage + window-fit; `day_length_type`/`recommended_day_length_type` are already ruled in
  `register_completeness` EXCLUDED_KEYS.

## 3. Governing principles (the contract -- inherited)

The variety contract carries over unchanged (dry-bean 3.1-3.4, apple 3.1-3.6). Restated for onion:

### 3.1 Flat, sparse override-by-ABSENCE
A variety stores a value only where it differs from the crop default, else inherits by omission. No
`delta` overlay. A load-bearing value is the actual value the app uses.

### 3.2 Source-authoritative, T1-or-it-does-not-ship
A T1 source is the authority for a load-bearing number (`days_to_maturity`, `day_length_type`). T1
ships automatically; any NON-T1 datapoint goes on a source manifest for Trevor's sign-off before the
splice (apple 6). No silent drops/downgrades. Onion day-length classes + DTM are standard extension
data, so T1 is expected; a transparency note is added only if a datapoint lands weak.

### 3.3 Common core + dispatched archetype block
The schema is a universal common core + one archetype block selected by the crop's `variety_archetype`
(absence defaults to `annual_dtm`; onion declares `photoperiod_annual`). Section 4.

### 3.4 DTM-anchor inheritance
A variety's `days_to_maturity` inherits the crop `dtm_anchor` (`from_planting` for onion), never
redefines it. `maturity_class` = DTM class (early/mid/late), the annual meaning.

### 3.5 Soft-gate lifecycle (inherited invariants)
- **INV-1 (no open-ended soft):** the field-addition register row carries the explicit hard-flip
  trigger -- the photoperiod-block checks fold into the A39 register-coverage hard floor + `gate_all`
  when the Spec-2 rollout column pass reaches full-roster coverage.
- **INV-2 (validation precedes load-bearing consumption):** plant-astro must not consume variety
  `days_to_maturity` as load-bearing until the crop is gate-clean. (Lighter than apple here: the
  `day_length_type` regional match is already A9-enforced, so day-length is already trustworthy.)

## 4. Per-variety schema (common core + `photoperiod_annual` block)

### 4.1 Universal common core (unchanged from apple 4.1)
`id` (slug), `name`, `maturity_class` (enum early|mid|late), `is_reference` (exactly one true;
onion = **Super Star**), `confidence_tier` (T1..T4), `note_beginner`, `note_seasoned`, `sources`,
`anchoring_urls`. Optional: `disease_notes`, `regional_fit`.

### 4.2 The `photoperiod_annual` archetype block (new)

| field | type | required | notes |
|---|---|---|---|
| `days_to_maturity` | int | yes | Load-bearing, absolute; inherits crop `dtm_anchor: from_planting`. **T1-sourced.** Shared DTM lane with dry-bean. |
| `day_length_type` | enum `long_day`\|`intermediate_day`\|`short_day` | yes | Load-bearing regional-viability class ("will it bulb at your latitude?"). **T1-sourced.** Already present + A9-typed. |
| `use` | string | yes | Culinary / storage (e.g. "sweet fresh-eating", "all-purpose storage"). Free-text; already present. |

`maturity_class` here = DTM class (the annual meaning, as dry-bean). **No** bean traits
(`seed_type`/`seed_color`/`seed_size`/`plant_habit`/`primary_use` are legume-specific, N/A). **No**
tree block. This is the smallest archetype block: onion shares DTM with dry-bean and adds one
distinctive field.

## 5. The gate refactor (`variety_detail_gate.py`, TDD RED before GREEN)

- **Add `photoperiod_annual` to the dispatch.** Required = common core + `day_length_type` + `use`;
  add `DAY_LENGTH = {long_day, intermediate_day, short_day}` to `TREE_ENUMS`'s sibling set for the
  photoperiod archetype (enum-validate `day_length_type`).
- **Share the DTM machinery across DTM archetypes.** The `days_to_maturity` presence/int/`[7,400]`/
  season-only check (`_annual_dtm_checks`, today gated to `annual_dtm`) and the class/DTM coherence
  warning (fastest not `late` / slowest not `early`) run for **any DTM archetype**
  `{annual_dtm, photoperiod_annual}`. Refactor the dispatch so both share these; the bean-trait
  presence/enum set stays `annual_dtm`-only, the tree block stays `tree_fruit`-only.
- **Separation of concerns (do NOT duplicate A9).** `variety_detail_gate` validates only that
  `day_length_type` is a valid enum. The day-length-vs-region honesty (coverage, window-fit, variety
  typing) stays in the A9 `photoperiod_gate`. No new day-length coherence in `variety_detail_gate`.
- **Adversarially proven on a scratch copy of real onion** before content is trusted: bad
  `day_length_type` enum, missing `days_to_maturity` on a DTM crop, absurd DTM (violates `[7,400]`),
  two `is_reference`, missing `use`, a class/DTM mismatch -- each bounces (RED) before GREEN.
- Stays **soft + standalone**, opt-in via `maturity_class` presence; NOT wired into a
  `whole_crop_gate` A-number this spec (A39 hard-flip = Spec 2, INV-1).

## 6. `register_completeness` ruling: none expected

The new per-variety STRING keys are already ruled: `day_length_type` (EXCLUDED_KEYS), `use`
(ruled), `id`/`maturity_class`/`confidence_tier` (dry-bean clause), `note_beginner`/`note_seasoned`
(auto-ruled by suffix). `is_reference` (bool)/`days_to_maturity` (int)/`sources` (list) are non-string.
`recommended_note` is REPLACED by the dual-register notes. So **no new register keys are expected** --
verify on the scratch battery (`register_completeness` 0 unruled); add a ruling only if a key surfaces.

## 7. Content: enrich the 6 varieties

Enrich all 6 to the flat schema in the sparse-override shape:

| id | name | day_length_type | maturity_class | flagship |
|---|---|---|---|---|
| `walla-walla` | Walla Walla | long_day | (verify) | no |
| `yellow-sweet-spanish` | Yellow Sweet Spanish | long_day | (verify) | no |
| `super-star` | Super Star | intermediate_day | (verify) | **yes** |
| `cimarron` | Cimarron | intermediate_day | (verify) | no |
| `texas-1015y-supersweet` | Texas 1015Y SuperSweet | short_day | (verify) | no |
| `yellow-granex` | Yellow Granex | short_day | (verify) | no |

Add `id`, `maturity_class` (from sourced DTM), `is_reference` (Super Star true), `confidence_tier`,
per-variety `days_to_maturity` (T1-sourced), dual-register `note_beginner`/`note_seasoned` (replacing
`recommended_note`, preserving its real content), per-variety `sources`/`anchoring_urls`.
`day_length_type` + `use` carry forward. Sourcing from extension onion-variety guides (Texas A&M,
UMN, Utah State; Johnny's-class T2 only if needed -> manifest). All prose original (17 USC 102(b)/
Feist), onion voice, dual-register, no em dashes, American English, temps as `°F`.

## 8. Honesty engine: already built (A9)

No new honesty engine. `day_length_type` x latitude viability is enforced by the A9 `photoperiod_gate`
(coverage + window-fit + variety typing) + the region model's `recommended_day_length_type` +
day-length notes. This pilot enriches the varieties the coverage invariant already depends on. App
consumption: the region already resolves "grow long-day here"; enriched varieties let the app render
full per-variety detail matched to latitude. `days_to_maturity` follows INV-2 (no load-bearing
harvest recompute until gate-clean); `day_length_type` is already trustworthy (A9-gated).

## 9. Authoring and release plan

1. **Gate refactor first (TDD),** RED-proven on a scratch copy of canonical (section 5).
2. **Author the 6 varieties** to the flat schema; verify each DTM + day_length_type against a T1
   extension source.
3. **Source manifest sign-off (Trevor):** surface any non-T1 datapoint with proposed source + tier;
   Trevor approves or holds. Nothing load-bearing ships on an unapproved non-T1 source.
4. **SHA-guarded COMPACT splice** (via `tools/build_onion_varieties_patch.py` + `apply_patch.py`,
   mirroring the apple builder): exactly onion's `varieties` object + the crop-level `variety_archetype`
   key + `verification_status.source_set`; all other crops byte-identical; count 125; COMPACT; footprint
   audited.
5. **Release gates (protocol #6):** `whole_crop_gate onion` (incl A9 photoperiod: coverage +
   window-fit unchanged), `variety_detail_gate` coverage, `gate_all` (116 certified unchanged),
   `release_verify` (`--slug onion`) no new concerns, per-batch source-truth sample.
6. **State trio:** patch CURRENT_STATE.md surgically (no `---` separator, `current-state-md-drift`),
   append STATE_HISTORY.md (most-recent first), bump LATEST.txt. Trevor confirms the push; **no
   plant-astro bump from this session** (`plant-astro-bump-owned-by-astro-session`).

## 10. Field-addition register entry

Add a row to `docs/field_addition_register.md` for the photoperiod-variety bundle (`day_length_type`
as the archetype's load-bearing field, sharing `days_to_maturity` with the DTM archetypes), with the
explicit **hard-flip trigger** (INV-1): *"flip the `variety_detail_gate` photoperiod-block checks from
soft/standalone into the A39 register-coverage hard floor + `gate_all` when the Spec-2 rollout column
pass reaches full-roster coverage."* Onion = the photoperiod-archetype + allium-family exemplar.

## 11. Scope boundaries (explicitly OUT)

- **Reconciling the roster's 5 variety shapes + `variety_archetype` roster-wide + folding in
  `varieties_detail[]`** -> Spec 2 (the column pass).
- **The allium family** (shallot, leek, garlic -- day-length relatives the A9 gate is built to
  inherit) -> the natural follow-on after this pilot, NOT this spec. Onion is the exemplar.
- **The A9 photoperiod honesty engine** (coverage/window-fit/variety-typing) -> already built; not
  re-touched.
- **plant-astro variety-driven consumption** -> Spec 2 (INV-2 on `days_to_maturity`).
- **Flipping the photoperiod-block checks into the A39 hard floor** -> Spec 2, post-rollout (INV-1).

## 12. Success criteria

- All 6 onion varieties carry the full section-4 schema, each `days_to_maturity` + `day_length_type`
  T1-anchored (or Trevor-signed-off), each with an honest `confidence_tier`.
- `variety_detail_gate` refactored to dispatch `photoperiod_annual` (DTM machinery shared across DTM
  archetypes; day_length enum validated); adversarial RED proof recorded; dry-bean + apple stay green.
- A9 `photoperiod_gate` stays green (coverage + window-fit unchanged; the 6 varieties still cover all
  3 resolved day-length types).
- Canonical footprint = exactly onion's `varieties` + `variety_archetype` (+ source_set); count 125;
  COMPACT; `gate_all` 116 certified unchanged; `release_verify` no new concerns.
- The contract (sections 3-4) is written so Spec 2's rollout + the allium family inherit the
  override + source-authoritative + archetype-dispatch rules without renegotiation.

## 13. Open items to confirm during authoring

- The exact T1 source id(s) for onion variety DTM + day_length_type (extension onion-variety guides;
  reuse tamu_agrilife/umn_ext/usu_ext or add one; non-T1 -> manifest).
- Per-variety DTM values (verify each against its T1 source; `maturity_class` must cohere with DTM).
- Whether any variety carries a real `disease_notes`/`regional_fit` (e.g. Walla Walla overwinter fit).
- Whether every variety reaches T1 or some land honestly at T2 (recorded in `confidence_tier`, never
  forced).
