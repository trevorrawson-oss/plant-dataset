# plant — Register-Bearing-Field Inventory v1.0

**Status:** AUTHORITATIVE (Phase 0, Part 1). All 13 sibling-ambiguous fields resolved 2026-05-30 (§9). Signed off; supersedes gold-standard arc checklist Appendix A as the canonical register-field roster.
**Reconciled 2026-06-08:** `source_quote`/`source_quote_seasoned` reclassified **SP → EXCLUDED** to match the shipped dataset (canonical SHA `ab389f72`; 794 `source_quote_seasoned` un-renamed to bare `source_quote` across 32 crops, `register_completeness_gate.py` synced, roster gate PASSes). Folded into §3.2 / §4 / §8, with the reversal recorded in §10. `synthesis_note`/`design_note`/`zone_coverage_note` are unaffected (remain SP). **Filename kept at `v1_0`** (no bump) so the roster gate's filename reference holds — this follows the doc's existing convention of folding dated addenda into v1.0 (cf. the 2026-06-03 addenda in §2.1).
**Authored:** 2026-05-30, Phase 0 session.
**Dataset at authoring:** SHA `74fa36f0…2026952f` (Phase B correction, 2.7.5), 123 crops. Read-only; no write performed by Part 1.
**Authoritative ruling source:** gold-standard arc checklist v1.1 **Appendix A** (the auto-derived denominator from a live 123-crop walk, 2026-05-30).
**Secondary cross-reference:** `schema_2_7_visibility_map_v1_0.md` (cherry-derived, 2026-05-16). **On any conflict, Appendix A governs** — see §6. The map contributes the CN/SN primitive distinction the rename needs (CN/SN never take a register suffix) and validates cherry-shaped CP/SP fields.

---

## 0. What this inventory is for

Phase 0 converts every register-bearing prose field to the symmetric `_seasoned`/`_beginner` shape, where **presence is the visibility declaration**: `_seasoned`+`_beginner` → both modes; `_seasoned` only → seasoned-only; `_beginner` only → beginner-only; neither → field absent. The suffix *is* the data (no separate `registers:` marker that could drift — the `anchoring_urls` lesson).

This document is the prerequisite the conversion consumes. Its value is the **curated, defensible ruling per prose field**, with everything non-prose explicitly excluded so the exclusion is auditable rather than implicit. A naive recursive walk returned 1,436 false candidates on cherry alone (sweeping in `slug`, `category`, every `anchoring_urls.*` leaf); this inventory is the hardened denominator that walk cannot produce.

**Scope decisions locked with Trevor at session open (2026-05-30):**
1. **Suffix everything register-bearing** — top-level/dict prose AND compound sub-field prose. One uniform rule: presence decides visibility everywhere, matching the dataset's existing per-sub-field `_beginner` siblings (220 already authored) and avoiding a second visibility mechanism layered only on compounds.
2. **`audience` entry-tag survives** alongside field suffixes — it governs *whole-entry* visibility (hide an entire advanced pest/tip block, `name` included); suffixes govern *per-prose-field* register within a visible entry. Different granularities; each fact lives in exactly one place.
3. **CN/SN primitives never take a register suffix.** Suffixing is the prose axis only. Every `zones.N.{plant_out, harvest, …}` planting-window primitive is CN → untouched.
4. **Schema version → 2.8** for this shape change; the region-primary flip and perennial extension re-number (neither has shipped a schema artifact).
5. **`companions` `_core`/`_seasoned` array split → OUT OF SCOPE**, flagged for separate reconciliation (§5). It is an array-level register split (a *reshape*), not a key rename; folding it in would violate the byte-preserving-rename boundary that makes the apply safe.

---

## 1. The ruling vocabulary

Each string-valued field gets exactly one ruling:

- **CP** (core-prose-needs-sibling) — user-facing prose a beginner needs. Gets `X_seasoned` + `X_beginner`. The default (currently implicit-seasoned) value is preserved byte-for-byte into `_seasoned`; the `_beginner` sibling is kept if present, else scaffolded **null**.
- **SP** (seasoned-prose) — user-facing prose that is depth/justification content. Gets `X_seasoned` only. **No `_beginner` sibling** — its absence is the explicit "hide in beginner mode" signal.
- **USER-FACING-CATEGORICAL** — short controlled-vocabulary phrase shown to growers. **No register suffix** (behaves like CN for this session). Carried as its own bucket because the dash-resolution step (checklist Step 9) must see these — `water` carries `--` on 2 mushroom crops a key-name heuristic would miss.
- **EXCLUDED** — machinery / identifier / enum / structural / audit-leaf / CN / SN. Never renders or never carries a register choice. No suffix. Listed by class in §4 so the exclusion is auditable.

**Mechanical note on "preserve the seasoned default":** today the unsuffixed field IS the seasoned register. The conversion renames `X` → `X_seasoned` carrying the value unchanged. **No seasoned content is created, nulled, or altered** — only relabeled. Null scaffolding only ever creates the *beginner* sibling. (Apply enforces this with a value-preservation audit: every renamed `X` byte-identical to pre-rename `X`, else `sys.exit(1)`.)

---

## 2. CP rulings — gets `_seasoned` + `_beginner`

### 2.1 Top-level / dict-sub-field (Appendix A, map-validated for cherry-shaped fields)

`description`; `harvest_ready`; `soil.preferred_description`; `ph.note`; `companions.note`; `rotation.note`; `storage.notes`; `varieties.note`; `yield_expectations.first_year_note`; `succession_policy.tip`; `start_method.hardening_off`; `start_method.notes`; `fertilizer.notes`; `fertilizer.notify_message`; `fertilizer.npk_hint`; `watering.signs_overwater`; `watering.signs_underwater`; `container_notes.notes`; `container_notes.soil_mix.type`; `container_notes.soil_mix.amendments`; `container_notes.watering_adjustment`; `container_notes.fertilizer_adjustment`; `det_indet.detail`; `bolting.note`; `bolting.prevention`.

Plus, from the map's Surface 13 (container) and Surface 28 (companions) expansions, present where applicable: `container_notes.overwintering.approach`.

**Bolting addendum (2026-06-03, closes `m15_step6_finding_001`).** `bolting.note` and `bolting.prevention` are CP (rename base → `_seasoned`, scaffold `_beginner: null`) on the 9 crops carrying a `bolting` dict (spinach, basil, broccoli, lettuce-leaf, arugula, bok-choy, radish, cauliflower, cilantro-coriander). The sibling `bolting` keys are ruled in §4: `bolting.risk` → EXCLUDED (enum `high`/`medium`; already noted §9.2); `bolting.triggers` → USER-FACING-CATEGORICAL (≤8-word phrase, dash-gated by Step 9, no sibling). **Root cause of the omission:** the original Appendix A walk was anchored on tomato shape, which has no `bolting` field, so the whole dict was missed; tomatoes do not bolt, so the gap was invisible until the lettuce Step 6 register read. Applied as the `bolting_register_conversion_addendum` (2.8 addendum, byte-preserving: 18 prose → `_seasoned`, 18 null `_beginner` scaffolded).

**Register-conversion completion addendum (2026-06-03, applied SHA `8a1d8a50` → `815efe62`).** The roster-completeness gate found the 2.8 conversion's tomato-anchored walk had also missed nested + array-variant prose. claude.ai ruled; Claude Code applied (10,801 prose fields, byte-preserving rename + null scaffold, no copy authored). New rulings registered:
- **CP (§2.1 / §2.3 — `_seasoned` + null `_beginner`):** `storage.fridge`, `storage.room_temp`, **`storage.freezer`**, `watering.amount`, **`watering.frequency`**, **`watering.method`**, `yield_expectations.per_plant`, `yield_expectations.peak_production`, `rotation.avoid_after`, `zones.N.safe_sowing_note` (lettuce-only today; already carried an AUTHORED `_beginner` — kept, not null-scaffolded), `container_notes.shape_requirements`, `container_notes.drainage.saucer_practice`, `tasks[].description`; and the `growth_stages_annual[]` / `growth_stages_year_one[]` inner prose (`user_action`, `what_to_look_for`, `log_prompt`) — CP identical to plain `growth_stages` §2.3. `tip` (bare top-level) — CP, **§7-FLAGGED** (flower/herb archetype; confirm at anchor; cf. `indoor_cycle.tip`/`thinning.tip`).
- **SP (§3 — `_seasoned` only):** `synthesis_note`, `design_note`, `uscrn_validation.zone_coverage_note` (nested planting-rule evidence prose, §3.2 class — always ruled SP); `succession_policy.count_note` (beside `succession_policy.reason` SP); `regions.*.resolved_by_zone.N.heat_pause.basis`; `regions.*.microclimate_note`. *(`source_quote` was originally listed here under SP; reclassified **EXCLUDED** 2026-06-08 — see §3.2, §4, §10.)*
- **USER-FACING-CATEGORICAL (§4 — no suffix, left bare):** `rotation.good_after` (bare list), `thinning.when` (short timing), `varieties_detail[].fruit_size`, `varieties_detail[].fruit_color`.
- **Root cause:** the Appendix-A walk was tomato/cherry-anchored and (a) never descended into nested planting-rule objects and (b) did not recognize array-name variants (`growth_stages_annual`/`_year_one`) as the same field as `growth_stages`. **The standing completeness gate, not human roster-assembly, is the real protection** -- it caught `storage.freezer` post-conversion, and a closed-set enumeration of the partially-ruled dicts (storage/watering/yield/rotation/container_notes) then caught `watering.frequency`/`watering.method` (the 2nd+3rd misses) before they spawned separate addenda. `freezer`+`frequency`+`method` ruled CP, batched (`815efe62` -> `e27eec14`).

**Variety-delta addendum (2026-06-12, ruled by Trevor at the lemon anchor; closes the register_completeness HALT on lemon Steps 1-3).** The crop-base + variety-DELTA model (schema 2.9; "Fuji is a view of apple") gives each `varieties.recommended[]` entry a `delta.<attr>.{value, parent, changed}` overlay (attr = hardiness/size/habit/flavor/heat_tolerance/foliage/flesh/fruit_size/...). The completeness gate flagged `delta.*.value` + `delta.*.parent` as unruled prose patterns (the gate refuses to auto-rule new prose). **Ruled USER-FACING-CATEGORICAL (§4 -- no suffix, left bare, dash-gated):** these are terse single-form attribute/diff descriptors (e.g. "compact; container-friendly", "high-20s F damage; fruits z9b-11"), not dual-register prose -- consistent with the existing `varieties.recommended[].use` categorical ruling. `delta.*.changed` is a bool (EXCLUDED by non-prose). **This sets the register treatment for the entire variety-delta model** (recurring across all varietals as the dataset expands). Gate rule: `register_completeness_gate.ruled_categorical` matches `k in {value,parent}` under `varieties.recommended[].delta.*`.

**Variety recommended-note addendum (2026-06-15, ruled by Trevor at the microgreens-mix anchor; closes the register_completeness HALT on microgreens-mix Steps 1-3).** microgreens-mix is the FIRST crop to populate `varieties.recommended[]` with individual entries carrying a per-entry `note` (the mix components: radish/broccoli/kale/arugula/mustard/pea-shoots/sunflower/cilantro/basil -- different SPECIES in a blend, NOT cultivars of one base, so the crop-base + variety-DELTA model does not apply). The completeness gate flagged `varieties.recommended[].note` as an unruled prose pattern. **Ruled USER-FACING-CATEGORICAL (§4 -- no suffix, left bare, dash-gated):** these are terse single-form per-variety descriptors (days-to-harvest + flavor + handling, e.g. "Fast brassica, 8 to 12 days; spicy. No presoak."), read identically by beginner and seasoned growers -- not register-divergent teaching prose -- consistent with the `varieties.recommended[].use` + `delta.*` categorical rulings on the same array. **This sets the register treatment for per-variety recommended notes across the whole varietal expansion.** It is DISTINCT from the top-level `varieties.note` (ruled CP, gets `_seasoned`/`_beginner`): the gate's `varieties.recommended` path guard separates the per-entry note from the crop-level note. Gate rule: `register_completeness_gate.ruled_categorical` matches `k == "note"` under `varieties.recommended[]` (excluding the `delta.*` sub-path).

**RULING -- null-valued SP/CP fields (2026-06-03):** SP/CP fields with NULL values are left **BARE** (un-suffixed), NOT renamed to `X_seasoned: null`. A bare null = empty-by-nature (no content exists), distinct from a present-null `_seasoned` key (which would falsely imply authoring-pending). **Consequence:** a logical SP/CP field may carry two key-names across crops -- `X_seasoned` where populated, bare `X` where null. **Any walk over an SP/CP field MUST key on the bare stem and treat both `<stem>` and `<stem>_seasoned` as the same field -- never key on the suffix alone, or the null slots are silently missed** (the inverse of the bolting bug). The completeness gate honors this: a bare null whose stem is a ruled SP/CP field is ruled-and-empty = PASS (non-string values are never prose-shaped, so never flagged).

`fertilizer.npk_hint` and `det_indet.detail` are CP under the **cultivar-specialty vocabulary precedent** (visibility map line 28): specialty vocabulary (NPK, determinate/indeterminate) defaults to CP-with-teaching-beginner-sibling, not seasoned-only — beginners learn the term through a gloss-then-use sibling.

### 2.2 Region notes (Appendix A; region-primary shape, post-dates the map)

`regions.*.region_notes` → CP, sibling `regions.*.region_notes_beginner`.
**Live state:** 1,230 `region_notes` keys, all present-null; 1,230 `region_notes_beginner`, all present-null (1C scaffolding). The pair is **already symmetric** — conversion is just the base rename `region_notes` → `region_notes_seasoned` keeping the existing `region_notes_beginner`; no scaffolding needed.

### 2.3 Compound prose (the seven CP-per-entry compounds, Appendix A §"Compound fields")

Per-entry prose; the default value → `_seasoned`, `_beginner` kept-or-scaffolded-null per entry:

| Compound | CP prose sub-fields | live occ. | existing `_beginner` |
|---|---|---|---|
| `pests` | `symptoms`, **`cause`**, `organic_treatment`, `prevention` | 335 ea. | 11 (0 for `cause`) |
| `diseases` | `symptoms`, **`cause`**, `organic_treatment`, `prevention` | 251 ea. | 10 (0 for `cause`) |
| `growth_stages` | `what_to_look_for`, `user_action`, `log_prompt` | 760 ea. | 12 / 12 / 6 |
| `notifications` | `title`, `body` | 516 ea. | 14 ea. |
| `weather_triggers` | `title`, `body` | 285 ea. | 10 ea. |
| `failure_diagnostics` | `label`, `what_happened`, `next_season_tip` | 615 ea. | 15 ea. |
| `tips_by_stage` | `text` | 1,503 | 34 |

**`pests[].cause` and `diseases[].cause` are CP — the single most important correction in this inventory.** The visibility map ruled `cause` as CN (line 130). Appendix A and Appendix C finding 004 rule it CORE-PROSE-NEEDS-SIBLING: per the 2026-05-30 ruling, "`pests.cause`/`diseases.cause` need a `_beginner` sibling (register transform, same content)." Live data confirms: 586 `cause` fields, all sentence-like prose, **0 existing `cause_beginner`**. The checklist exists *specifically because* the cherry-derived roster (which the map embodies) silently dropped these fields. Following the map here would (a) reintroduce the bug v1.1 was built to fix, and (b) declare `cause_beginner` correctly-absent on the anchors, making the M16 regression test unable to rediscover its own finding 004. **Appendix A governs.**

**Compound suffix totals (the scope decision #1 in numbers):** 9,574 CP compound prose occurrences → `_seasoned` rename; 220 already have `_beginner`; **9,354 null `_beginner` siblings scaffolded.**

### 2.4 `suitability_reason` — CP, **beta-test flagged** (decided 2026-05-30)

`zones.N.suitability_reason` (90 occ., 36 crops) and `regions.*.resolved_by_zone.N.suitability_reason` → **CP**: rename base → `_seasoned`, scaffold `_beginner: null`.

Explains *why* a zone is marginal (e.g. "Habanero needs 90-120 days; Zone 4's ~140-day season is marginal for reliable ripening"). Its sibling `suitability` (the verdict enum) is excluded and shows to both modes. Ruled **core** because a first-season grower who gets only the verdict "marginal" with no reason is left without the *what-to-do* (start indoors early / pick a faster variety) — the exact failure beginner mode prevents.

**The `_beginner` sibling is authored in a different register, not a copy of the seasoned sentence** — plain-language, action-forward (e.g. "This pepper needs a long warm season; your summer may be too short for a reliable harvest, so start it indoors early or choose a faster variety"). Per the no-content-authoring scope guard, Phase 0 scaffolds the null slot only; the beginner prose is written in each crop's gold-standard arc.

**Beta-test flag:** ruled CP now to preserve the option of beginner-facing reasons. If beta data later shows beginners prefer just the verdict, **CP→SP-only is a clean one-line flip** (drop the `_beginner` sibling). Authoring the beginner register now costs little; not authoring it would force a re-open. Trevor's call to revisit post-beta.

### 2.5 `disease_resistance_notes_default` — CP, **register suffix outermost** (convention ratified 2026-05-30)

`disease_resistance_notes_default` (1 occ., tomatillo) is plain prose → **CP**. Its `_default` suffix is a **fallback-scope marker** (the crop-level note that applies when a variety has no specific resistance documentation), **not** a register marker. Under the ratified convention **"the register suffix is always outermost,"** it becomes `disease_resistance_notes_default_seasoned` + `disease_resistance_notes_default_beginner`. A reader strips the trailing `_seasoned`/`_beginner` to recover the meaningful stem `disease_resistance_notes_default`. This convention governs any future scope-suffixed prose (schema 2.8 perennial fields, variety expansion), so it needs no re-deciding. Only one such field exists today; the `growth_stages_annual`/`growth_stages_year_one` variants are array *names* (their inner prose has clean stems), not collisions.

---

## 3. SP rulings — gets `_seasoned` only (no beginner sibling)

### 3.1 Top-level (Appendix A + map agree)

`succession_policy.reason` (biology explainer is depth content); `yield_expectations.factors` (yield-modifying factor analysis); `moon_phase_preference.source_note` (contested-evidence depth).

### 3.1b `varieties_detail[]` depth prose — **decided SP-only 2026-05-30** (Group A)

`varieties_detail[].history`; `varieties_detail[].origin_note`; `varieties_detail[].flavor_notes`; `varieties_detail[].growth_habit_notes`; `varieties_detail[].seed_saving_notes`; `varieties_detail[].short_season_notes`; `varieties_detail[].pollination_notes`.

All 6 occurrences each, all on tomatillo today; none on anchors. Connoisseur/variety-comparison depth (e.g. "Rendidora's upright habit vs. Toma Verde's sprawling"; "wet-process seed saving per Seed Savers Exchange"). A seasoned grower comparing cultivars wants this; a first-season grower picking "a tomatillo" does not. **Ruled SP-only by Trevor 2026-05-30**, consistent with the `history`/`origin_note` call on the same structure. Gets `_seasoned`, no `_beginner`. (Note: `varieties_detail[].description` and `varieties_detail[].notes` remain CP — basic identity, not depth — see §7.)

### 3.2 Zones/regions evidence prose (visibility map line 88: "backend evidence prose; no beginner siblings" — applies to `synthesis_note`/`design_note`; the map's `source_quote` = SP token is **superseded 2026-06-08**, see §4 / §10)

Within `zones.N.plantings[]…` and `regions.*…plantings[]…` planting-rule objects, the **own-voice reasoning** fields are SP:
`synthesis_note`; `design_note`; `uscrn_validation.zone_coverage_note`. (`source_quote` was formerly ruled SP here; reclassified **EXCLUDED** 2026-06-08 — it holds *verbatim* source text, not authored prose; see §4 and the §10 reversal note.)

These are the **"show your work" layer** behind each planting date — the crop-specific reasoning written in the project's own voice (`synthesis_note`, `design_note`). Real readable *authored* prose (so it lives on the register axis), but justification content a beginner never needs (so seasoned-only). **Confirmed SP with Trevor 2026-05-30** (for `synthesis_note`/`design_note`). Gets `_seasoned`, no `_beginner`. The *verbatim* extension quote behind a date — e.g. *"Plants started earlier are difficult to manage… (UMN)"* — lives in `source_quote`, which is **EXCLUDED** backend evidence (not authored prose), reclassified 2026-06-08 (§10); it is not part of this SP layer.

**Sibling evidence fields in the same objects are EXCLUDED, not SP** (see §4): the verbatim quote `source_quote` (reclassified 2026-06-08), plus the structured citation record `source` (catalog ID like "UMN"), `source_id`, `source_disagreements[].claim`, `source_disagreements[].source`. None of these are register-bearing authored prose. Clean line within one rule object: **authored own-voice reasoning** (`synthesis_note`, `design_note`) → SP `_seasoned`; **verbatim quote + structured evidence** (`source_quote`, `source`, `source_id`, …) → EXCLUDED.

---

## 4. EXCLUDED — no suffix (listed by class for audit)

Counts are distinct field *paths* at the authoring SHA (list indices collapsed).

- **AUDIT_LEAF (~941 paths):** all `*.anchoring_urls.<id>.url` / `.verified`; `accessed`, `publisher`, `source_class`, `source_note`, **`source_quote`** (verbatim source-evidence text — reclassified SP→EXCLUDED 2026-06-08, §10; never rendered; its interim `source_quote_seasoned` form was un-renamed back to bare `source_quote` in the shipped dataset), `verification_log_ref`, `filing_record`, `filed_in*`, `resolved_*`, `resolution*`, `last_audited`, `assigned_to`, `deferred_to`, `disposition`, `scope`, `session`, `field`. Plus the entire `verification_status` subtree (`open_findings[].note`/`summary`/`resolution_note`, `retro_resolution_log[]`, `launch_ready_*`, etc.) — backend audit trail, never rendered.
- **MACHINERY (~655 paths):** `id`, `slug`, `stage_id`, `tip_id`, `region_id`, `evidence_tier`, `added_in`, `last_reviewed`/`_operation`/`_session`, `offset_from`/`_days`/`_hours`, `schema_version`, `last_updated`, dates (`date`, `stored_date`, `uscrn_*_date`, `first/last_plant_date` as computed anchors), `resolution_tier`/`_method`, `anchor_threshold`, `fallback_beyond_horizon`, `calendar_state`, `window_type`, `timing_relative`, `to_spacing`, `phase`, `status`, `image`, `example_product`, `plantings_provenance`, `provenance`, `lifted_from_zone`. Plus the entire `sources_summary` subtree (`primary`, `frost_data`, `_note`, ...) — backend source-provenance scaffolding, named backend machinery in the arc checklist §2, never rendered (citation authority is the top-level `source_catalog`); ruled EXCLUDED at the basil herb anchor 2026-06-12, synced to `register_completeness_gate.EXCLUDED_PATH_SUBSTR`.
- **ENUM / CN-PRIMITIVE (~195 paths):** `severity`, `action`, `condition`, `type`, `confidence`, `category`, `timing`, `archetype`, `flower_type`, `light_required`, `lifecycle`, `self_fertile`, `heat_tolerance`, `growth_habit`, `tier`, `frequency`, `unit`, `method`, `label` (as evidence label), `evidence_label`, `trigger_type`, `sunlight`/`water`/etc. (also in §USER-FACING-CATEGORICAL), zone-boolean/range primitives (`zone_8_presence`, `hardiness_zone_min/max`, `reliable_fruit_zone_min/max`, `zone_10_desert_fold`, `bolting.risk` (enum `high`/`medium`; see Bolting addendum §2.1)). Plus USER-FACING-CATEGORICAL (no suffix, dash-gated): `bolting.triggers` (see Bolting addendum §2.1).
- **CN — zones/regions planting-window primitives (the bulk of the scary count, but untouched):** every `zones.N.{plant_out, start_indoors, direct_sow, harvest, harvest_start, harvest_end, first_plant_date, last_plant_date, bloom, notes, planting_note, zone_notes}` and the `regions.*.resolved_by_zone.*` equivalents. CN = primitive shown to both modes with no register choice → **no suffix**. (Note: some of these, e.g. `zone_notes`, `planting_note`, are dash-gated by Step 9 via Appendix A's leaf registry even though they take no register suffix.) **`suitability_reason` is NOT in this bucket — it is CP, see §2.4.**
- **CN-METADATA (evidence structure):** `sources` arrays/objects, `source`, `source_id`, `source_disagreements[].claim`/`.source`, `source_quote` (verbatim quote — listed under AUDIT_LEAF above; EXCLUDED 2026-06-08), `uscrn_validation.*` (except `zone_coverage_note` which is SP).
- **IDENTIFIER / LABEL (~11+ paths):** `name` (pests/diseases/growth_stages/varieties), `botanical_name`, `family`, `variety`, `region_label`.

---

## 5. OUT OF SCOPE — flagged for separate reconciliation

**`companions` `_core`/`_seasoned` array split** (`good_core[]`, `good_seasoned[]`, `bad_core[]`, `bad_seasoned[]`) — present in all 123 crops; carries `why` (511×), `category` (330×), `timing` (330×) prose/primitives inside. This is a *fourth* register mechanism (array-level split), not the field-suffix or `audience` mechanisms. **Excluded from the Phase 0 conversion** because converting an array-level split into field suffixing is a reshape (with `core`→`beginner` vocabulary implications), not the byte-preserving key rename this session is scoped to. **Recommend a dedicated companions-reconciliation session.** The *flat* `companions.note` + `companions.note_beginner` pair (separate from the array split, present in all 123) **is** in scope and ruled CP (§2.1).

---

## 6. Map ↔ Appendix A conflicts and their resolution

| Field | Visibility map | Appendix A | Resolution | Verified |
|---|---|---|---|---|
| `pests[].cause`, `diseases[].cause` | CN (no sibling) | CP (needs sibling) | **CP** — Appendix A; matches Appendix C finding 004 | 586 prose fields, 0 existing `cause_beginner` ✓ |
| `regions.*.region_notes` | (field absent from map) | CP, sibling `region_notes_beginner` | **CP** — Appendix A (post-region-shape) | 1,230 `region_notes` (null) + 1,230 `region_notes_beginner` (null) ✓ |
| `sunlight`/`water`/`difficulty`/… | CN | USER-FACING-CATEGORICAL (dash-gated, no sibling) | **USER-FACING-CATEGORICAL** — Appendix A | `water` dash on exactly 2 mushroom crops ✓ |

**Principle:** Appendix A is the auto-derived denominator from a live 123-crop walk at the current SHA; the map is cherry-derived (2026-05-16) and pre-dates the region-primary work. Where they agree, fine. Where they conflict, Appendix A governs — this is the design of checklist v1.1, and the kickoff names Appendix A (not the map) as this inventory's starting point.

---

## 7. Anchor-unvalidated rulings (FLAGGED — confirm when the archetype's anchor runs)

The authoritative sources are both tomato-shaped (cherry/beefsteak) or cherry-derived. The eight non-tomato archetypes (fruit trees, herbs, berries, mushrooms) carry prose whose register is **not yet anchor-validated**. Most of their heavy field surface (chill_hours, rootstock_options, cane_management, bloom_window, dormancy/pruning windows) **does not exist in the dataset yet** — deferred to schema 2.8 per the visibility map (line 308). The prose that *does* exist today gets a **best-judgment CP ruling**, flagged, to be confirmed when that archetype's gold-standard anchor exercises it:

| Field | Crops w/ field today | Best-judgment ruling | Basis |
|---|---|---|---|
| `bloom_time` (top-level + `varieties_detail[]`) | 157 occ. | CP | bloom timing is grower-facing; cultivar-specialty precedent |
| `hardiness_notes` | 39 | CP | grower-facing hardiness guidance |
| `chill_hours_note` | 26 | CP | cultivar-specialty vocabulary precedent (map line 308 names chill_hours) |
| `pollinator_notes` | 26 | CP | grower-facing |
| `year_one_notes` | 19 | CP | perennial first-year guidance, grower-facing |
| `soil_prep` | 15 | CP | grower-facing |
| `deadheading` | 12 | CP | grower-facing maintenance action |
| `substrate_notes` | 5 | CP | mushroom-specific, grower-facing |
| `planting_method_notes` | 4 | CP | grower-facing |
| `indoor_cycle.tip`, `thinning.tip` | few | CP | grower-facing tip prose |
| `varieties_detail[]` **basic prose** (`description`, `notes`) | varies | **CP** (decided) | basic variety identity, grower-facing |
| `varieties_detail[]` **depth prose** (`history`, `origin_note`, `flavor_notes`, `growth_habit_notes`, `seed_saving_notes`, `short_season_notes`, `pollination_notes`) | 6 ea. (tomatillo) | **SP-only** (decided 2026-05-30, §3.1b) | connoisseur/comparison depth; not anchor-blocking |

**These rulings are NOT presented as settled.** Each must be confirmed (and possibly recut CP↔SP) when the owning archetype's anchor runs. Per Appendix A line 304 and the kickoff: a field with no anchor behind its ruling is flagged, not asserted.

---

## 8. Conversion summary (what Part 2 will do, per these rulings)

- **CP top-level/dict (§2.1):** rename base → `_seasoned` (value preserved); keep-or-scaffold-null `_beginner`.
- **CP region notes (§2.2):** rename `region_notes` → `region_notes_seasoned`; keep existing null `region_notes_beginner` (already symmetric).
- **CP compound prose (§2.3):** rename base → `_seasoned` on 9,574 occurrences; scaffold 9,354 null `_beginner` siblings; keep 220 existing.
- **SP (§3):** rename base → `_seasoned`; **no** `_beginner` sibling. Includes `succession_policy.reason`, `yield_expectations.factors`, `moon_phase_preference.source_note`; `varieties_detail[]` depth prose (`history`, `origin_note`, `flavor_notes`, `growth_habit_notes`, `seed_saving_notes`, `short_season_notes`, `pollination_notes` — §3.1b); and zones/regions `synthesis_note`/`design_note`/`zone_coverage_note`. (`source_quote` was originally in this SP set; reclassified **EXCLUDED** 2026-06-08 and reverted from its interim `_seasoned` form — see §10.)
- **USER-FACING-CATEGORICAL, EXCLUDED, OUT-OF-SCOPE:** untouched (no rename, no scaffold).
- **Anchor-unvalidated (§7):** ruled CP for the conversion (rename + scaffold) but the ruling itself carries a flag in this inventory; the apply treats them as CP unless Trevor recuts any before the write.

**Apply integrity:** SHA-gated start; dry-run on throwaway copy; collateral hash audit (every non-prose key byte-identical pre/post); value-preservation audit (every renamed `X` byte-identical to pre-rename `X`); anchor-content audit (cherry/beefsteak/lettuce prose byte-identical); minified output; independent post-write re-verification; schema bump to 2.8; `LATEST.txt` updated. `sys.exit(1)` on any mismatch.

---

## 9. Decisions resolved this session (2026-05-30) + remaining confirmations

**Resolved (no longer open):**
1. **All 13 sibling-ambiguous fields ruled** (Groups A–D): varieties depth → SP-only (§3.1b); perennial/establishment (`year_one_notes`, `deadheading`, `hardiness_notes`, `disease_resistance_notes_default`) → CP; pollination (`pollinator_notes`) → CP; `suitability_reason` → CP/beta-flagged (§2.4); `chill_hours_note`/`substrate_notes` → CP (§7-flagged).
2. **`risk` → EXCLUDED** (enum: only `high`/`medium`); **`why` → DEFERRED** (companions-only, §5).
3. **Register-suffix-outermost convention ratified** (§2.5) — handles `disease_resistance_notes_default` and all future scope-suffixed prose.
4. **Appendix A governs over the cherry-derived map** on conflict (ratified) — keeps `cause` CP, preserves M16 finding 004.
5. **Companions array split → out of scope**, dedicated reconciliation session **scheduled immediately after Phase 0, before M15 lettuce** (§5).

**Remaining confirmations before the Part 2 write:**
1. **Schema version 2.8** — confirmed this change takes 2.8; region flip / perennial extension renumber. (Pin the bookkeeping at apply.)
2. **Anchor-unvalidated set (§7)** — accepted as best-judgment-CP-for-conversion; each still flagged for confirmation at its archetype anchor. (No action needed unless recutting any now.)
3. **Sign-off on this inventory as a whole**, which gates the Part 2 apply.

---

## 10. Post-sign-off reconciliations (reversal log)

This section records rulings changed **after** the original sign-off/apply, folded back into the body above so no field is classed two ways. Each entry is a reconciliation to shipped reality, not a re-litigation.

**2026-06-08 — `source_quote` (and the interim `source_quote_seasoned`): SP → EXCLUDED.**
- **Ruling:** `source_quote` is **EXCLUDED** — §4 AUDIT_LEAF / evidence-machinery, same class as `source` / `source_id` / `source_note` / `source_class`. No register suffix. Applies wherever it occurs, including `zones.N.plantings[].*[].source_quote` and `regions.*.plantings[].*[].source_quote`.
- **Why (the new lens):** `source_quote` holds *verbatim* third-party extension text (e.g. *"tomatoes will take 6 weeks"*, *"Desert Valleys: Dec-March"*). As a rendered `_seasoned` field it would put unparaphrased source quotes into the shipping app as product content — against the project's paraphrase discipline and verbatim-detection rubric (some stored quotes exceed the <15-word line). As backend evidence it is standard citation practice. This **reverses** the 2026-05-30 "Confirmed SP" call (§3.2), which weighed the quotes as *content* and did not weigh the verbatim-display IP posture. The seasoned "show your work" layer is **not lost**: `synthesis_note` / `design_note` (the reasoning in the project's own voice) stay SP and keep rendering.
- **Shipped (Claude Code):** all **794** `source_quote_seasoned` un-renamed to bare `source_quote` across **32 crops** (byte-preserving; values unchanged); `register_completeness_gate.py` `EXCLUDED_KEYS` synced to match the inventory + `whole_crop_gate`; **canonical SHA now `ab389f72`**; roster gate **PASSes**. `synthesis_note_seasoned` / `design_note_seasoned` / `zone_coverage_note` unchanged.
- **Filename:** kept at `register_bearing_field_inventory_v1_0.md` (no bump) per the doc's convention of folding dated addenda into v1.0 (cf. the 2026-06-03 addenda, §2.1); the roster gate's filename reference therefore needs no change.

---

*Inventory v1.0, reconciled 2026-06-08. §9 records the original 2026-05-30 Part-1 state and its remaining confirmations; sign-off, the Part 2 apply, and the 2026-06-08 `source_quote` reconciliation have since shipped (see §10). No prose was authored in this reconciliation — a key was reclassified and its interim suffix reverted.*
