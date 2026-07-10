# Corn GS Arc (sweet-corn anchor) — design spec

**Status:** approved design (brainstormed with Trevor 2026-07-10). Ready for an implementation plan.
**Date:** 2026-07-10
**Kickoff:** `docs/kickoffs/21-corn-grass-archetype.md` (reframed 2026-07-10 — corn is NOT a
gate-worthy archetype).
**Origin:** `sweet-corn` is one of the 10 uncertified §E shells. Certifying it also unlocks the corn
family (`corn`/field-dent, `popcorn`, `flint-corn` are all *Zea mays* frost-anchored annuals — queued
as fast follow-ons, not authored here).
**Primary precedent:** `dry-bean` (`docs/superpowers/specs/2026-07-09-dry-bean-gs-anchor-design.md`) —
a fresh frost-anchored annual GS arc certified with ZERO new archetype gate.
**Reference:** Phase 4 Master Crop List (`~/Documents/plant-project/08-reference/master_crop_list.pdf`,
Grasses/Corn pp. 12-13) — see memory `master-crop-list-phase4-inventory`.

---

## 1. Goal

Certify the `sweet-corn` shell as a `verified_gs_arc`, carrying the full register stack from birth
(the dry-bean greenfield playbook). Add exactly one net-new schema element — a `planting_layout`
conditional field — to structure corn's defining agronomic fact (block planting for wind pollination)
so the app can render and (lightly) enforce it. Everything else is authoring on existing fields.

## 2. Non-goals (explicit)

- **No new archetype.** Corn is a frost-anchored, direct-sown annual. It rides the existing annual
  gate set. NO new `calendar_basis`, NO berries_woody-style structural-cert + calendar-coherence +
  `derive_*_calendar` trio. (Verified: the gate dispatch key is `calendar_basis`, not `archetype`;
  every archetype gate opens `if crop.get("calendar_basis") != "<basis>": return []`. Corn's
  `calendar_basis` stays `frost_anchored`, so it inherits the 83-annual gate set unchanged.)
- **No dry corns in this arc.** `corn`/`popcorn`/`flint-corn` are queued follow-ons. They reuse this
  arc's `planting_layout` model + the dry-bean `dry_down → harvest → cure_thresh` ladder.
- **No garden-planner build.** The planner is a separate future arc (memory `planner-data-model-arc`,
  Trevor targeting ~2026-07-11/12). This arc only ships `planting_layout` as a corn-only conditional
  field that is forward-compatible with that arc.
- **No roster-wide `planting_layout` register rollout.** Deliberately kept off the A39 present-or-null
  treadmill (see §4). That decision belongs to the planner arc.
- **`broom-corn`** (*Sorghum*) and **`sugar-cane`** (*Saccharum*, perennial tropical) are out of scope
  despite the "corn" name — different genus, own basis/archetype.

## 3. Crop model & identity

- **slug:** `sweet-corn` (existing shell) · **species:** *Zea mays* (var. *saccharata*/*rugosa*).
- **`archetype`:** set `"warm_season_grass"` (currently the wrong `warm_season_fruiting`). COSMETIC —
  a descriptive label only; it gates nothing. Chosen for honesty/tidiness.
- **`calendar_basis`:** stays `frost_anchored` (UNCHANGED). This is the load-bearing field; it keeps
  sweet-corn on the standard annual gate set.
- **`perennial`:** `false`. · **`succession_policy`:** `suitable: true` (see §5).
- **regions:** 10 regional sow→harvest calendars, T1-anchored (see §6).

## 4. The `planting_layout` field + its gate (the one net-new schema element)

**Why a field at all (not just prose):** block planting is corn's make-or-break instruction — plant a
BLOCK of ≥4 short rows, never one long row, or wind can't move pollen from tassels to silks and ears
fill only partially. Trevor wants the app (backyard/hobby gardeners) to be able to render this as a
structured callout, and it is the first brick of the future planner's layout column.

**Shape** (flat sibling fields — matches the `heat_threshold_f`+`heat_effect` / `tray_sowing`+`pot_up`
convention; NOT a nested object):

```jsonc
"planting_layout": "block",           // enum: block | row | hill | grid | single | null
"pollination_block_min_rows": 4       // int >= 2 (corn: 4); present IFF planting_layout == "block"
```

**Population scope in THIS arc:**
- `sweet-corn`: `planting_layout: "block"`, `pollination_block_min_rows: 4`.
- All other ~121 crops: field **absent** (NOT null-everywhere). No 125-crop splice; matches the
  conditional-field precedent (`divide_every_years` lives only on perennials). The gate no-ops on
  absent (§ below), so nothing floods.
- The other enum values (`row`/`hill`/`grid`/`single`) are **defined but unpopulated** here — chosen
  so the planner arc can take the field roster-wide without redefining it. (`hill` already latent in
  the data: cucurbits carry no `thin_to` precisely because they're hill-planted.)

**Prose carries the why/how** (spacing + soil-prep + tips copy, consumer voice, T1-sourced): wind
pollination, tassel → silk (each silk = one kernel), a 4×4 grid beats a single long row, and the
cross-pollination isolation caveat (keep sweet corn away from popcorn/field corn or kernels go
starchy). The field is only the machine-readable flag + parameter.

**The gate** — `tools/planting_layout_gate.py` (new), `check_crop(crop)` (aliased `_layout_violations` in the A44 wiring) +
`test_planting_layout_gate.py`, TDD RED-before-GREEN, adversarially proven on a scratch copy of the
real canonical; wired into `whole_crop_gate` as a new A-number and run roster-wide by `gate_all`:

1. **No-op guard:** `if not crop.get("planting_layout"): return []` — silent on the 121 crops without
   the field, so it never becomes a backfill treadmill.
2. **Enum guard:** `planting_layout` ∈ {`block`,`row`,`hill`,`grid`,`single`}.
3. **Coherence:** `planting_layout == "block"` ⟺ `pollination_block_min_rows` present AND an int ≥ 2
   (corn authored at 4). Any non-`block` value ⟹ `pollination_block_min_rows` absent.
4. **NOT added to A39 register-coverage** — this is the deliberate line that keeps it conditional, not
   a hard present-or-null cert requirement for every crop.

**Adversarial RED set (must each bounce before GREEN):** bad enum value (`"blocks"`); `block` with no
`pollination_block_min_rows`; `pollination_block_min_rows` present on a `row`/non-block value; absurd
row count (0, negative, or a non-int); and a regression check that a crop with the field ABSENT passes
clean.

## 5. Harvest model & `growth_stages` (the authoring core)

Sweet corn is the **milk-stage, succession-suitable** case (the dry corns are the dry-down case, and
reuse the dry-bean ladder as follow-ons — see §8).

**Stage ladder** (annual/seed spine; the `harvest` id is the A40 anchor, same rule as dry-bean):

```
germination → seedling → vegetative → tasseling → silking → kernel_fill → harvest
```

- `harvest` = the **milk stage** — the tight ripeness window (squeeze a kernel, it runs milky; silks
  brown and dry). A40 anchors ladder-monotonicity + the DTM band on this id.
- **No `dry_down` / `cure_thresh`** in this arc — that ladder is exclusively the dry corns'.
- **DESIGN CHOICE (Section-4 approval, item c):** surface `tasseling` and `silking` as their OWN
  stages rather than folding them into a generic `flowering`. Corn's male (tassel) and female (silk)
  flowers are separate structures on separate parts of the plant and are the pollination story the
  block-planting field exists to serve — distinct stages make the biology legible and give the app
  real milestones. (Confirm no annual gate keys off a required literal `flowering` id — the timing
  spine anchors on the `harvest` id, not on `flowering`, so this is safe; verify in the plan.)
- **Biology in stage prose:** the "knee-high by the Fourth of July" vegetative milestone; tassel drops
  pollen onto silks; a too-small block fills ears poorly (ties back to `planting_layout`).

**Succession:** `succession_policy.suitable: true` (green-beans model) — stagger sowings, or use
varieties of differing maturity, for continuous harvest. Prose notes you stagger BLOCKS (not single
rows) and the isolation caveat vs. popcorn/field corn.

**Varieties:** carry the **su / se / sh2 sugar genetics** at variety level (per the Master Crop List) —
the real driver of sweet-corn variety selection; it sets the eating-window and DTM differences. Author
a representative set (e.g. a `su` standard, an `se` sugary-enhanced, an `sh2` supersweet) with
T1-aligned DTM.

**DTM:** a T1-sourced band on `days_to_maturity` (+ `days_to_maturity_mid`), varying by sugar type.
If no single clean figure exists, synthesize + ratify with Trevor (the dry-bean non-regional-DTM
precedent).

## 6. Region suitability

Corn needs a long warm season, so short-season cold zones and the extreme desert are the honesty
pressure points — the same tension dry-bean hit. **Follow the dry-bean Option-C precedent:** the
annual region model cannot yet express a hard per-region `suitable: false` (A32 requires a non-empty
calendar; the suitability enum is tree-only), so marginal regions stay plantable with an honest
advisory in the calendar/region prose rather than a false hard block. No schema change here.
T1-anchored regional sow→harvest calendars, `succession` staggering where the season allows. Region
sourcing (extension services per region) is gathered at authoring time.

## 7. Register stack — the greenfield checklist

`sweet-corn` must carry the full register stack natively (the §E new-crop checklist; dry-bean proved
these fall out of clean authoring, no backfill): timing spine (A39/A40), `germination_light` +
`seedling_light` + `tray_sowing`/`pot_up` (note corn is direct-sown → `seedling_light: na`,
`tray_sowing: na` unless authored otherwise from prose), climate thresholds
(`heat_threshold_f`/`heat_effect`/`frost_tolerance_f`/`frost_effect`/`chilling_sensitivity_f` —
corn is frost-tender, warm-loving), watering `schedule_by_stage` (per-stage, from corn's own prose;
silking/tasseling is the critical-moisture window), `pet_safe`, `second_planting`/A43 (succession is
same-plant staggering — confirm the A43 shape), and the new `planting_layout` field. The plan
enumerates the exact checklist; the gate suite is the backstop.

## 8. Corn-family decision table (settled here; built later)

| crop | sugar/type | harvest | ladder | succession | planting_layout |
|------|-----------|---------|--------|-----------|-----------------|
| `sweet-corn` (this arc) | su/se/sh2 | milk stage | `…→ kernel_fill → harvest` | `suitable: true` | `block` / 4 |
| `corn` (field/dent) | dent | dry-down | reuse dry-bean `dry_down → harvest → cure_thresh` | `suitable: false` | `block` / 4 |
| `popcorn` | flint/pop | dry-down | same dry-bean ladder | `suitable: false` | `block` / 4 |
| `flint-corn` | flint | dry-down | same dry-bean ladder | `suitable: false` | `block` / 4 |

All four share the `planting_layout: block` model and the wind-pollination biology; they split only
on the harvest ladder (milk vs. dry-down) and succession.

## 9. Certification & gate strategy

- **No new archetype gate.** The only new gate is `planting_layout_gate.py` (§4), which is a light
  conditional field gate, not an archetype structural cert.
- **TDD hard rule:** RED before GREEN; sneak each defect class at the new gate on a SCRATCH COPY of
  the real canonical and confirm it bounces before trusting it (§4 RED set).
- **Release verification before promote** (protocol #6): `whole_crop_gate` 18/18 on sweet-corn +
  `tools/gate_all.py` (whole suite on every certified crop — must stay green after the new A-number is
  wired) + `release_verify` + the source-truth sample. A green single gate is NOT a clean release.
- **SHA-guarded COMPACT splice** (`tools/apply_patch.py`): EXACTLY `sweet-corn` mutated, all other
  crops byte-identical, count unchanged, `separators=(",",":")`, `ensure_ascii=False`, no trailing
  newline. Re-baseline the guard SHA against the **post-tomato-cleanup** canonical (Trevor is doing a
  tomato cleanup in a separate session first — see §12).
- **State trio** at release: regen/patch `CURRENT_STATE.md` (note the drift caveat — memory
  `current-state-md-drift`, hand-maintain surgically), append `STATE_HISTORY.md` (most-recent first),
  bump `LATEST.txt` (SHA + session).

## 10. Verification (beyond the gate suite)

- Source-truth sample: pull 2-3 authored claims (block-planting rows, milk-stage harvest cue, a
  variety DTM) back to their T1 sources (university extension / .edu / gov).
- Consumer-copy scan: 0 em dashes, American English, `°F` rendering, "plant" lowercased per CLAUDE.md.
- Frontend-safety: grep for any field-name assumptions before a future plant-astro bump; the new
  `planting_layout` field is additive (no rename/collapse), so no consumer breaks (memory
  `dataset-shape-change-breaks-frontends`).

## 11. Success criteria

1. `sweet-corn` certifies: `whole_crop_gate` 18/18, `gate_all` green roster-wide (with the new
   A-number live), `release_verify` clean, timing_spine 0/0, calendar_coherence 0.
2. `planting_layout_gate` is TDD-complete: every RED defect bounces on a scratch canonical; the gate
   no-ops cleanly on all crops that lack the field.
3. `planting_layout: "block"` + `pollination_block_min_rows: 4` present on sweet-corn; field absent on
   all others; enum forward-compatible with the planner arc.
4. Block-planting, milk-stage harvest, su/se/sh2 varieties, and region calendars are T1-sourced.
5. Canonical splice touches EXACTLY sweet-corn; COMPACT; count unchanged +0 (shell → certified, no
   new crop added — sweet-corn already exists in the roster).
6. State trio updated; committed on `main`, held for Trevor's push confirmation.

## 12. Open items / pinned-at-authoring

- **Sequencing:** HOLD implementation until Trevor's separate-session **tomato cleanup** lands, then
  re-baseline the splice SHA against the updated canonical. Spec-writing does not touch the dataset,
  so it proceeds now.
- **DTM band:** pin the su/se/sh2 DTM figures at authoring; ratify a synthesized band with Trevor if
  no single clean T1 figure exists (dry-bean precedent).
- **`tasseling`/`silking` as distinct stages:** confirm in the plan that no annual gate requires a
  literal `flowering` stage id (expected safe — the spine anchors on `harvest`).
- **`planting_layout` roster-wide + `row_spacing` + height/spread:** deferred to the planner arc
  (memory `planner-data-model-arc`). If a hobby-gardener use case later demands enforcement across
  more crops, that arc promotes `planting_layout` to an A39 register field.
- **Region suitability model gap:** the open annual per-region `suitable: false` limitation (Option C)
  is inherited, not solved here.
