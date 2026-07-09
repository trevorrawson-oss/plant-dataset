# Dry-Bean GS Anchor — design spec

**Status:** approved design (brainstormed with Trevor 2026-07-09). Ready for an implementation plan.
**Date:** 2026-07-09
**Origin:** Phase 4 crop expansion. `dry-bean` is the first *net-new* crop authored since the
register stack (timing spine, seedling/seed-tray, climate thresholds) rolled out across the 114. All
prior register work was **column passes onto existing crops**; this is the first **greenfield** crop
that must carry the full register stack *from birth*. It is therefore also the first real test of the
"§E new-crop checklist" fold-in (`docs/gs_cross_crop_field_addition_v0.md` §2.5, and the per-field
"fold into the per-crop checklist for new (§E) crops" notes in `docs/field_addition_register.md`).
**Reference:** Phase 4 Master Crop List, `~/Documents/plant-project/08-reference/master_crop_list.pdf`
(Beans & Peas family, pp. 8-11) — see memory `master-crop-list-phase4-inventory`.

---

## 1. Goal

Author, certify, and gate-clear a new `dry-bean` crop to gold-standard (`verified_gs_arc`), modeled
on certified `green-beans-bush`, harvested for mature/cured dry seed rather than green snap pods. In
doing so, prove that a greenfield crop naturally produces every shipped register field and passes the
full always-on gate suite (A39 register-coverage included) with **no new gate required** — or, if a
defect class surfaces, catch it and close it TDD-first.

**Two deliverables in this spec:**
1. The `dry-bean` GS anchor (built now).
2. A **beans-family decision table** settling the family→crop→variety splits for the rest of the
   master-list bean additions (documented once; only `dry-bean` is built now).

Corn is explicitly **out of scope** here — it needs a new warm-season block-planted-grass archetype
and gets its own brainstorm + spec next.

## 2. Non-goals

- No corn, sugar-cane, or broom-corn work (separate specs; sugar-cane and broom-corn are each their
  own new archetype and are out of Phase 4 food-crop scope).
- No authoring of the *other* beans-family crops (cowpea, lima, shelling-bean, runner-bean) — they are
  only **decided** here, not built.
- No new archetype. `dry-bean` rides `warm_season_fruiting`.
- No reformatting or unrelated edits to `crops_data_final.json`. The canonical stays **READ-ONLY**
  until the authoring/promote step of the implementation plan, and is written COMPACT
  (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline) per CLAUDE.md.

## 3. Crop model & identity

- **One crop**, slug `dry-bean`, name `"Dry Beans"` (display name TBD at authoring; consider
  `"Dry Beans (Shelling / Storage)"` if disambiguation from snap/shell helps the picker).
- Species *Phaseolus vulgaris*, **bush** habit at the crop level (Black Turtle / Pinto / Navy / Kidney
  are bush or half-runner; bush types mature uniformly, which is what makes a single dry-down harvest
  work). Pole / half-runner cultivars are flagged at the variety level, not the crop level.
- **Variety picker** (`varieties.recommended[]`): Black Turtle, Pinto, Navy, Kidney, Jacob's Cattle
  (final list + per-variety DTM/notes pinned at authoring; master-list tier-1 names are Black Turtle,
  Pinto, Jacob's Cattle).
- Crop-level numbers are an **honest bush-dry-bean composite**, the same way `green-beans-bush` carries
  a representative baseline plus a variety list.

## 4. Approach — clone-and-refit from `green-beans-bush`

Take the certified `green-beans-bush` record (`verified_gs_arc`, 65 top-level keys, carries the full
register stack) as the **structural skeleton** and re-author every value from T1 dry-bean sources —
exactly the "modeled on a certified reference crop" method used for radish←carrot. Same species means
the register fields, pest/disease arrays, soil/pH/sun, and spacing come across largely intact; the
authoring effort concentrates on the harvest-model delta (§5).

Rejected alternatives: (a) blank shell like the 34 staged drafts — does not carry the register fields,
so it fails to test the greenfield goal; (b) multi-crop composite (green-beans-bush + pole-beans +
fava) — over-engineers a single-species crop.

## 5. The snap → dry delta

Everything not listed here is inherited from `green-beans-bush` with values re-verified against dry-bean
T1 sources: sun, spacing, pH, soil, pests/diseases, `germination_temp_f`, `propagule: seed`,
`dtm_anchor: from_sow`, `sow_depth_inches ~[1,1.5]`, `germination_light: neutral`, `seedling_light: na`,
`tray_sowing: na` (+ no `pot_up`), `weeks_indoors: 0`, `heat_threshold_f: 90`, `frost_tolerance_f: 32`,
`chilling_sensitivity_f: null`, `perennial: false`, `archetype: warm_season_fruiting`.

| Field | green-beans-bush (snap) | dry-bean | Rationale |
|---|---|---|---|
| Harvest model | pick immature pods over a ~2-wk flush, repeatedly | let all pods mature and dry on the plant → one harvest when ~90% rattle-dry → cure → thresh | defining difference |
| `days_to_maturity` | `[50,60]` | **~`[85,100]`** (source-pinned) | dry seed, not green pod |
| `days_to_maturity_mid` | (mid of above) | recompute from the new range | derived field |
| `growth_stages` ladder | germination → harvest (pods) | adds **dry-down/maturity** + **cure/thresh** stages; `day_range_from_sow` extends to ~85–100 (cure stage sits past nominal DTM) | §6 |
| `harvest_window_days` | `[14,28]` (flush) | **omitted (one-shot)** | dry beans harvest as a single event, like potato / winter squash (both carry no `harvest_window_days`). A window would imply a repeated-harvest span that does not exist. `harvest_window_days` is archetype-**optional** in A39, so omission is gate-clean. |
| `succession_policy` | suitable=true, every 2 wks | **suitable=false** | one full-season crop; you do not succession-plant a dry-down bean |
| `storage` | fridge, ~7 days | **dry, airtight, cool/dry, months–years** (thresh to ~13–15% moisture first) | wholly different storage block |
| `water` / watering taper | steady all season | steady through pod-fill, then a deliberate **dry-down taper** (stop watering to cure pods on the plant) | signature of the dry harvest |
| `yield_expectations` | ~5–10 lb/10 ft (green) | dry **shelled** weight (much lower per row); source-pin | different harvested product |
| `varieties.recommended[]` | Provider, Blue Lake, … | Black Turtle, Pinto, Navy, Kidney, Jacob's Cattle | §3 |
| `harvest_ready_*` / `description_*` | snap-pod prose | dry-down prose ("pods brown and rattle; beans rock-hard"), dual-register | consumer copy re-authored |

**Three ruled modeling calls (Trevor, 2026-07-09):**
1. **`harvest_window_days` → one-shot / omitted.** Single harvest event; matches potato + winter-squash
   precedent. The dry-down timing pressure ("harvest before pods shatter or fall rain molds them")
   lives in the dry-down growth stage, not this field.
2. **Cure/thresh → explicit growth stage(s).** Curing to storage-dry (~13–15% moisture, beans shatter
   not dent) is a distinct user action with its own timing and its own failure mode (store too moist →
   the jar molds). It earns its own stage and a real "your beans are curing, don't store yet" app card.
3. **Habit → bush** at the crop level; pole/half-runner noted per variety.

## 6. `growth_stages` ladder (the greenfield spine)

Authored from scratch on the standard per-stage shape (`id`, `name`, `day_range_from_sow`, `audience`,
`user_action_*`, `what_to_look_for_*`, `log_prompt_*` — cherry-tomato/green-beans-bush reference), with
`day_range_from_sow` pinned to T1. Intended ladder (day ranges illustrative, source-pinned at authoring):

1. `germination` — `[7,14]`
2. `seedling` / vegetative
3. `flowering`
4. `pod_development` (pod-fill)
5. `dry_down` — pods yellow → brown on the plant but **not yet ready to pick**; the "be patient, watch
   for the pods to dry and rattle" period. `day_range_from_sow` ~`[75,90]`. Drives the app's *"your
   beans are drying down"* card (the lead-in Trevor wants before the harvest window opens).
6. **`harvest`** (id must be literally `harvest`) — the **harvest window**: ~90% of pods brown, dry, and
   rattling; harvest anytime across this window, before pods shatter or fall rain molds them.
   `day_range_from_sow` ~`[85,100]` — this range **is** the window the app surfaces (§6a). Sits at ~DTM.
7. `cure_thresh` — post-harvest cure 1–2+ wks to rock-hard, then shell/store. `day_range_from_sow`
   sits **past** nominal DTM (~`[95,115]`).

**6a. App harvest-window (Trevor's requirement — the app must show a *window* to harvest, not a point):**
The window is the `harvest` stage's `day_range_from_sow` `[min,max]`. `crop-timing.ts` reads the ladder,
so from a user's sow date it can render "harvest window: ~[sow+85] to [sow+100]" plus the `dry_down`
lead-in card. The **data** side is fully covered by the two stages above (window = `harvest` range; the
"drying down now" signal = the `dry_down` stage + each stage's `what_to_look_for_*` observational prose:
"pods brown and rattle; a bean should shatter, not dent, under a hammer"). Whether the app renders the
harvest stage as a min→max *window* vs a single point is a **plant-app** concern — a verification +
handoff item (§10), not a dataset blocker. `harvest_window_days` (the repeated-flush field) stays
**omitted**; re-adding it would double-count against this stage window and misrepresent a one-shot crop.

**Gate interaction (A40 timing-spine, wired into `whole_crop_gate` → `gate_all`) — load-bearing:**
`timing_spine_gate._harvest_index` anchors the ladder on the stage whose `id` is exactly `"harvest"`,
**else the last stage**. Consequences the ladder MUST respect:
- Stage 6 is named `harvest` so the anchor lands at DTM (the harvest window), not on `dry_down` or
  `cure_thresh`. If `harvest` were absent, the anchor would fall on the last stage (`cure_thresh`) —
  pointing `crop-timing.ts` at the end-of-cure date and enforcing monotonicity through curing.
- A40 enforces `day_range_from_sow` **non-decreasing up to and including the `harvest` anchor** (HARD
  violation) — so `dry_down` `[75,90]` before `harvest` `[85,100]` is fine — and **exempts post-harvest
  stages** (its comment names *curing*) from monotonicity + the ±15% DTM alignment, so `cure_thresh`
  past DTM is legal precisely because it follows the `harvest` anchor.

## 7. Register stack — the greenfield checklist test

The crop must carry every shipped register field or its defined null/N-A (A39 present-or-explicit-null).
Expected native values, all inherited/verified from the same-species template:

| Register | Field(s) | dry-bean value |
|---|---|---|
| #4 timing spine | `propagule` / `dtm_anchor` / `sow_depth_inches` / `thin_to_inches` | `seed` / `from_sow` / `~[1,1.5]` / `~[2,4]` |
| #4 (optional) | `harvest_window_days` / `divide_every_years` | omitted (one-shot) / N/A |
| #5 watering | `watering.schedule_by_stage[]` | authored per-stage, non-empty (with dry-down taper) |
| #6 light | `germination_light` / `seedling_light` (+cap) | `neutral` / `na` |
| #9 seed-tray | `tray_sowing` / `pot_up` | `na` / absent |
| #7 climate | `heat_threshold_f`+`heat_effect` / `frost_tolerance_f`+`frost_effect` / `chilling_sensitivity_f` | `90`+(match template) / `32`+`killed` / `null` |

**This is the test:** if the §E checklist is right, authoring the crop naturally yields all of the
above and `register_coverage_gate` (A39) + the standalone register gates pass without special-casing.
Any gap found is a checklist bug to fix, and the fix is folded back into the per-crop GS-arc checklist.

## 8. Certification & gate strategy

- Full GS arc → `verification_status.status = "verified_gs_arc"` with a real T1 `source_set` (Clemson
  HGIC, UMN, USU, UMD, etc. — the dry-bean-relevant subset of green-beans-bush's set, plus any dry-bean
  specific T1 pages), a `verification_log` documenting the independent source-fidelity fetch, and
  `field_additions`/provenance as needed.
- **Must pass, all green:** `tools/whole_crop_gate.py` on dry-bean (incl. A39); `tools/gate_all.py`
  (whole suite on every certified crop — the 18 gold anchors stay **18/18**, byte-untouched);
  `tools/release_verify.py`; the per-batch **source-truth sample** (`tools/source_truth_sample.py`).
  Register gates specifically: `timing_spine_gate`, `seedling_light_gate`, `seed_tray_gate`,
  `climate_threshold_gate`, `register_coverage_gate`, `register_completeness_gate`,
  `numeric_sanity_gate` (DTM within `[7,400]`), plus dash/degrees scans (`temp_scan`, no em dashes in
  consumer copy, `°F`).
- **Expectation: no new gate.** dry-bean rides the existing suite. If the dry-down/one-shot harvest or
  the cure stage surfaces a real defect class (e.g., a gate that wrongly assumes `harvest_window_days`
  present, or a stage-ladder monotonicity check tripped by the post-DTM cure stage), close it TDD-first
  — RED (inject the defect into a scratch copy, watch it bounce) before GREEN — per CLAUDE.md.
- **READ-ONLY discipline:** all authoring lands via a SHA-guarded splice (`tools/apply_patch.py` batch
  or equivalent), footprint = EXACTLY the new `dry-bean` object added, every other crop + top-level key
  byte-identical, count 124 → **125**, COMPACT, no trailing newline. Nothing else in the file changes.

## 9. Beans-family decision table (settled here; not built here)

Per the master crop list crop-vs-variety rule ("different species OR different garden cycle OR different
use pattern that changes harvest rules = new crop, else variety"):

| Item | Botanical | Decision | Level | When |
|---|---|---|---|---|
| **dry-bean** | *P. vulgaris*, cured | **BUILD NOW** — this spec | crop (Black Turtle/Pinto/Navy/Kidney/Jacob's Cattle = varieties) | now |
| shelling-bean | *P. vulgaris*, fresh-shelled | new crop | crop (Borlotti/Cranberry, Tongue of Fire) | later |
| cowpea / black-eyed pea | *Vigna unguiculata* | new crop (different genus, warm-season, own cycle) | crop | later |
| lima bean | *P. lunatus* | new crop (distinct species) | crop | later |
| runner bean | *P. coccineus* | new crop (distinct species) | crop | later |
| **greasy beans** | *P. vulgaris*, Appalachian heirloom pole snap/shell | **varieties**, not a crop | variety-set under `pole-beans` | later |

Snap/wax/filet types remain varieties under existing `green-beans-bush` / `pole-beans` (unchanged).

## 10. Verification (beyond the gate suite)

- **plant-app timing end-to-end:** confirm `crop-timing.ts` reads dry-bean's new ladder + `dtm_anchor`
  correctly — a July direct-sow should land the `dry_down` stage and the `harvest` window in fall
  (mirrors the brussels-sprouts spine end-to-end check). Graceful-omit confirmed for the absent
  `harvest_window_days`.
- **App harvest-window (Trevor's requirement) — verify + hand off:** confirm the data lets the app show
  a *window* to harvest, not a single date: the `harvest` stage's `day_range_from_sow` `[min,max]`
  resolves to a sow-relative date range, and the `dry_down` stage + `what_to_look_for_*` prose supply
  the "drying down now / ready when pods rattle" cues. If the app currently renders only a single
  harvest point, file a plant-app handoff to surface the min→max window (a website/app concern, not a
  dataset blocker) so the dataset ships window-ready.
- **State trio at promote:** regenerate `CURRENT_STATE.md` (`tools/gen_current_state.py`, then fill
  prose slots — note the current-state-md drift caveat, hand-maintain if needed), append
  `STATE_HISTORY.md` (most-recent first), bump `LATEST.txt` (SHA + session).
- **Roster count:** 124 → 125 crops; certified count +1.

## 11. Success criteria

1. `dry-bean` exists as a certified (`verified_gs_arc`) crop, COMPACT-spliced, every other crop
   byte-identical.
2. It carries the full register stack natively; A39 + all standalone register gates PASS.
3. `gate_all` green across the whole certified roster; `whole_crop_gate` 18/18 anchors intact;
   `release_verify` clean; source-truth sample clean; zero em dashes / spelled degrees in its copy.
4. The dry-down + cure model reads as authoritative (one-shot harvest, explicit `dry_down` and
   `cure_thresh` stages, dry storage), sourced to T1.
5. **The app can surface a harvest *window*** (Trevor's requirement): the `harvest` stage's
   `day_range_from_sow` resolves to a sow-relative date range, with the `dry_down` lead-in and the
   "pods rattle" readiness cue — verified end-to-end (§10), with a plant-app handoff filed if the app
   renders only a point today.
6. The §E new-crop checklist is confirmed (or corrected + re-folded) by the exercise.
7. Beans-family splits are documented (§9) for the next crops.

## 12. Open items / pinned-at-authoring

- Exact `days_to_maturity` range, per-variety DTMs, `sow_depth_inches`/`thin_to_inches`, and every
  `day_range_from_sow` value — pinned to specific T1 pages during authoring; surface any source
  contradiction rather than paper over it (green-beans-bush yield-correction precedent).
- Final display name and variety list.
- `heat_effect` enum value for dry-bean (match green-beans-bush; verify blossom-drop framing).
- Stage split RESOLVED (§6): three distinct late stages — `dry_down` (drying, not ready) → `harvest`
  (the window) → `cure_thresh` (post-harvest cure). Exact `day_range_from_sow` values pinned at authoring.
