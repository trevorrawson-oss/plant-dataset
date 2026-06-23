# Zucchini-Courgette — Steps 1-3 Author-Lane Findings

**Crop slug:** `zucchini-courgette`
**Archetype:** `warm_season_fruiting` (rail-rider — no new archetype, tooling, or design spec)
**Session:** `zucchini-courgette_steps1-3_author` (claude.ai author lane)
**Date:** 2026-06-23
**Scope:** Step 1 (source set) + Step 2 (scalars + structured biology) + Step 3 (varieties + companions). Consumer prose + compounds deferred to Steps 6-8. Region work (zones/regions) untouched — Step 3.5 / Step 4 are the release lane.

---

## SHA chain

| Stage | Crop SHA (sha256, sort_keys, compact, ensure_ascii=False) |
|---|---|
| Preflight (untouched slice, re-asserted before mutation) | `8e3faa1f2968515f7ec0d490c7613af79a1f46633de01cd81e4f7a3e68a5512f` |
| **Post-author (this handback)** | **`11c3b048c507bf898b718ac11e800004e2de8d4e673a260113bb404f6b14fa02`** |

Live full-file base at session start: `0b767fc27b33d229fb5e41fc0ef0576ea592dd1e76647e53d781134563b7fb81` (session `blueberry_step11_cert`). Release lane preflights against that base.

---

## 1. NEW KEYS ADDED — flag for CC key-delta audit

The author-fresh shell did **not** contain these. Authoring them per the kickoff added exactly three top-level keys. The release-lane collateral/key-delta assertion should expect precisely this set and nothing more:

- `self_fertile` (bool `true`) — known ENUM/CN primitive (strawberry precedent); monoecious, single plant fruits, no second cultivar needed.
- `pollinator_notes_seasoned` (CP) — the pollination note (seasoned register).
- `pollinator_notes_beginner` (CP) — the pollination note (beginner register).

`pollinator_notes` is a known CP pair in the field inventory (26 occ). No `pollination{}` block, no `bloom_group`/`pollinizer` machinery was added (correct for an insect-pollinated annual — this is a pollination *note*, not apple-style cross-pollination structure).

Verified: top-level `added == {self_fertile, pollinator_notes_seasoned, pollinator_notes_beginner}`, `removed == {}`, and every touched block's nested key SET is unchanged (values only).

---

## 2. FERTILIZER — deferred to Steps 6-8; feeder profile sourced here

Per the green-beans rail-rider precedent, the fertilizer block's fields (frequency/type/timing/prose/npk/amount + notify machinery) are entangled consumer-prose + notification surfaces authored block-coherently at Steps 6-8. The `fertilizer` block is **byte-identical to the shell** in this handback. The Step-2 fertilizer obligation ("source the feeder profile") is satisfied by recording the determination here:

- **Determination: MODERATE feeder** (NOT heavy — corrects the kickoff's guess).
- T1 basis: UMD "Medium requirement for nutrients" (`umd_ext`, growing-summer-squash-zucchini page); UMN side-dress guidance + note that rich soil may need little supplemental feed (`umn_ext`); OSU N-rate guidance (`osu_ext`).
- This is the legume→fruiting contrast called out in the kickoff (green-beans is a light/N-fixing feeder; zucchini is a moderate feeder).
- Steps 6-8 authors the fertilizer JSON fields against this profile (timing = incorporate at planting + side-dress as vines run / at flowering; keep the "consistent moisture + calcium for fruit set" nexus in prose).

---

## 3. SHAPE-CONFORMANCE FLAGS — best-guess values for CC to conform to the carrot/onion template

I authored these with reasonable values but could not verify the live enum/type against a certified slice (cherry/beefsteak `.md` files are verification records, not JSON). Per the rail-rider model, the release lane conforms any drift:

1. **Companion three-array VISIBILITY MODEL (the important one).** I authored under the *complete-roster* interpretation:
   - `good_seasoned[]` = the COMPLETE rich roster (all 7), each with `why_seasoned` + provenance + sources. This is the seasoned view.
   - `good_beginner_seasoned[]` = a LIGHT `{name, why_beginner}` projection of the tight subset (corn, pole beans, nasturtium) — the beginner view.
   - `good_beginner[]` = `[]` (born empty).
   - The both-modes items (corn/beans/nasturtium) therefore appear in BOTH `good_seasoned` (rich, `why_seasoned`) and `good_beginner_seasoned` (light, `why_beginner`) — one entry per register.
   - **Rationale for this model over the disjoint alternative:** the research-backed items (corn/beans/nasturtium) are exactly the ones with T1 provenance + sources. If `good_seasoned` held only seasoned-EXCLUSIVE extras (disjoint model), those well-sourced both-modes items would live only in `good_beginner_seasoned` as `{name, why_beginner}` and would LOSE their provenance/sources. Information-preservation forces the complete-roster reading.
   - **CC: confirm against carrot/onion.** If the certified template is disjoint (good_seasoned = seasoned-only), conform — but preserve the corn/beans/nasturtium provenance + sources when you do.
   - Same model applied to `bad_*`: `bad_seasoned[]` rich (potatoes, fennel), `bad_beginner_seasoned[]` light (potatoes, fennel), `bad_beginner[]` empty. Bad companions ARE surfaced to beginners per Trevor's adjudication.

2. **Companion `timing` enum** — used `"plant_with"` (flowers/herbs/beans), `"plant_before"` (corn, Three Sisters sequencing), `"avoid"` (bad). Conform to carrot/onion timing vocabulary.

3. **Companion `notify_weeks_before`** — corn `3`, pole beans `1`, all interplanted flowers/herbs `0`, bad `0`. Confirm the semantics (intended: weeks before the squash planting date to prompt sowing the companion, for Three Sisters sequencing).

4. **Companion `category` enum** — corn `vegetable`, pole beans `legume`, nasturtium/marigold/sweet alyssum `flower`, borage/sage `herb`, potatoes `vegetable`, fennel `herb`. Conform if the vocabulary differs.

5. **`start_method.weeks_before`** — authored as int `3` (UMD "3 weeks prior"). Confirm int-vs-range. (`start_method` has no `sources`/`anchoring_urls` slot in the shell, so none added.)

6. **`container_notes.recommended_pot_gallons = 10`** — SOFT. Hard T1 floor is `min_pot_gallons: 5` + `depth_inches_min: 12` (uwi_hort: "squash... minimum volume of five gallons and a depth of 12 to 18 inches"; umd_ext container tiers). The `10` reflects the near-universal "bigger is better, 5-10 gal" guidance but is not a clean single-figure T1 claim. CC may downgrade to `null` if the cert bar wants a strictly-T1 figure.

7. **Variety object shape `{name, recommended_note}`** — per schema 2.9 (non-tree crops carry `{name, recommended_note}`; `recommended_note` is bare USER-FACING-CATEGORICAL, both modes, no register suffix). Note schema 2.9 §224 says the variety-object upgrade was scoped to WOODY archetypes, leaving non-woody certified anchors' `recommended` as STRING lists. This author-fresh crop uses the 2.9 object shape per the kickoff's explicit "{name, ..., note}" instruction. If the live convention for non-woody crops is still string lists, conform — but the object shape is the schema-2.9 forward target.

8. **`succession_policy.successions = 3` / `max_successions_per_season = 3`** — starting estimate. Per A8, the release lane derives per-zone `successions_realized` and reconciles `successions` to max-over-zones. `window_type: continuous`, `pause_in_heat: false` (heat-loving — fall succession is borer/mildew-driven, not a heat pause; the green-beans contrast to carrot).

---

## 4. Numeric provenance (every quantitative claim → its OWN T1 source, A1 rule)

| Field | Value | T1 source(s) |
|---|---|---|
| `days_to_maturity` | `[50,65]` (mid 55) | umd_ext 50-65; osu_ext 50-65 |
| `spacing_inches` | `[24,36]` | umd_ext single-plant 2-3 ft |
| `germination_temp_f` | `[70,95]` | osu_ext optimum 70-95 (min 60) |
| `sunlight_hours` | `[6,10]` | umd_ext "at least 6, prefers 8-10" |
| `ph.preferred_range` | `[6.0,6.5]` | umn_ext "best 6.0-6.5" |
| `ph.tolerated_range` | `[5.8,7.5]` | osu_ext (5.8-7.0, grows higher) |
| `container_notes.min_pot_gallons` | `5` | uwi_hort "minimum volume of five gallons" |
| `container_notes.depth_inches_min` | `12` | uwi_hort 12-18; umd_ext 12-16 |
| `succession_policy.interval_weeks` | `3` | umn_ext "finish the planting three weeks later" |
| `weeks_indoors` / `start_method.weeks_before` | `3` | umd_ext "3 weeks prior" (transplant lead) |
| `water` | `moderate` | umn_ext ~1 inch/week (heavy-feeder nuance → 6-8 prose) |
| `watering.watering_method` | `base` | umn_ext leaves-stay-dry; sdsu_ext drip preferred (powdery-mildew nexus) |
| `watering.drought_tolerance` | `low` | umn_ext heavy water feeders; misshapen fruit from inadequate water |
| `soil` texture/drainage/OM | loam / well_draining / high | umn_ext, umd_ext, osu_ext |
| `self_fertile` | `true` | monoecious, single plant fruits (general extension consensus; pollination note carries the insect-pollination caveat) |

T1 institutions in use: `umn_ext`, `umd_ext`, `sdsu_ext`, `osu_ext`, `uwi_hort` (all catalog parents). **No T2** (almanac / seed-catalog / garden-blog) in any `sources` array — container pot-size figures were sourced specifically to uwi_hort + umd_ext to avoid the T2 trap, since the consensus figure is otherwise blog/catalog-heavy.

---

## 5. Companion evidence calibration (provenance honesty)

| Companion | Label | Conf | Basis |
|---|---|---|---|
| Corn | research_backed | high | Three Sisters structure (support + groundcover) |
| Pole beans | research_backed | high | N-fixation + Three Sisters |
| Nasturtium | research_backed | high | umn_ext: "supported by research"; Iowa study (squash bug + cucumber beetle) |
| Marigold | likely | medium | umn_ext Iowa study positive for squash, but marigold results mixed generally → calibrated down |
| Sweet alyssum | likely | medium | umn_ext Florida study (increased natural enemies of aphids on squash) |
| Borage | traditional | medium | well-documented pollinator companion; no squash-specific trial |
| Sage | traditional | low | aromatic-herb pest-deterrence folk practice; no squash trial |
| Potatoes (bad) | traditional | medium | competition-based caution; not a controlled trial |
| Fennel (bad) | traditional | low | allelopathy largely observational |

research_backed / likely → `sources: ["umn_ext"]` + companion-page anchoring + `verified_against_sources: true` + `verified_date: "2026-06-23"`. traditional → `sources: []` + `anchoring_urls: {}` + `verified_against_sources: false` + `verified_date: null`. (Onion all-traditional calibration template followed.)

---

## 6. Validation gauntlet — ALL PASS

1. **Key-delta** — exactly +3 expected top-level keys; no removals; all nested key sets unchanged. ✓
2. **Collateral** — every untouched top-level field byte-identical (zones, regions, pests, diseases, growth_stages, tips_by_stage, storage, yield_expectations, fertilizer, description_*, harvest_ready_*, moon_phase, etc.). ✓
3. **Register-pair** — 21 prose `_seasoned`/`_beginner` pairs balanced; no half-pairs. ✓
4. **Numeric fidelity** — every quantitative claim matches its cited source; pH tolerated brackets preferred; soil coherence (well_draining + clay-problematic); pause_in_heat false. ✓
5. **Copy-rules sweep** (user-facing strings) — 0 em-dashes, 0 double-hyphens, 0 "degrees F" spellouts, 0 smart quotes, 0 Title-Case crop names; °F symbol present. ✓
6. **8-gram source-verbatim scan** — 0 overlaps against the source corpus (all prose paraphrased in own voice). ✓
7. **Companion shape sanity** — good_beginner/bad_beginner born empty; good_seasoned rich shape (7); good_beginner_seasoned light (3); tight subset ⊆ rich roster; provenance/source rules per label. ✓
8. **T1-only (gate E preview)** — every in-use source ID ∈ T1 set. ✓

**Validator note (transparency):** an initial run false-positived `good_seasoned`/`good_beginner` and `bad_seasoned`/`bad_beginner` as prose register pairs. They are list-valued visibility arrays (the `_beginner` arrays are born empty BY DESIGN), not prose pairs — the matcher was corrected to skip list-valued `_seasoned` keys. The genuine companion prose pair (`note_seasoned`/`note_beginner`) is balanced.

---

## 7. Deferred to Steps 6-8 (intentionally null/empty)

`description_*`, `harvest_ready_*`, all `watering.*` prose (frequency/amount/method/signs/method_note/critical_periods/schedule_by_stage — only `watering_method` + `drought_tolerance` authored), the entire `fertilizer` block (profile recorded §2), `storage`, `yield_expectations`, `growth_stages`, `notifications`, `weather_triggers`, `tips_by_stage`, `pests`, `diseases`, `failure_diagnostics`, `moon_phase_preference`, `container_notes` deep prose (`notes_*`, `soil_mix`, `watering/fertilizer_adjustment_*`, `overwintering`, `self_watering*`, `shape_requirements` — green-beans precedent), `rotation.rotation_years` + rotation prose (only `rotation.family` set), `recipes`, `first_planting_notify_days`.

Steps 6-8 pest targets: squash vine borer, squash bug, cucumber beetle. Disease targets: powdery mildew, bacterial wilt. (For the release lane's planning only — not authored here.)

---

## 8. Release-lane handoff (for CC)

1. Preflight full-file against `0b767fc2…`; confirm slice crop SHA `== 11c3b048…` on receipt.
2. Apply slice; run collateral hash audit (only `zucchini-courgette` changes; all other crops byte-identical).
3. Key-delta audit: expect exactly +`self_fertile`, +`pollinator_notes_seasoned`, +`pollinator_notes_beginner`.
4. Conform shape flags §3 to carrot/onion template (esp. the companion visibility model — preserve provenance/sources on corn/beans/nasturtium).
5. `whole_crop_gate` (STRUCTURAL-only at Steps 1-3 for author-fresh per v1.7 C2) + `register_completeness` + `register_fill` (deferred 6-8 prose reads as not-yet-authored, not violation).
6. Promote; re-pin LATEST.txt; mint source sub-IDs if desired (specific-page anchors recorded in §4 — parents are all in the catalog).
7. Then Step 3.5 (region shells) → Step 4 (region fill) → Steps 6-8 (compounds: fertilizer block, pests, diseases, growth stages, tips, yield, storage, watering prose) → Step 9 (dash-resolution pass) → cert.
