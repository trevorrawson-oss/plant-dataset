# Timing-Spine Field Contract (locked spec)

**Status:** locked v1 -- the "field contract first" step of the column GS arc
(`gs_cross_crop_field_addition_v0.md` §2.1) for the seed->harvest timing spine (Plan 3).
**Drafted:** 2026-07-07 · **Gate:** `tools/timing_spine_gate.py` (+ `test_timing_spine_gate.py`).
**Consumer contract (authority):** `plant-app/src/lib/guides.ts` (`Guide` type) +
`plant-app/src/lib/crop-timing.ts`. If this doc and those files disagree, those files win.
**Anchor-truth:** `docs/2026-07-06-batch2-audit-findings.md`.

The spine is a **coupled bundle** authored per-crop (not a field-by-field sweep): the stage ladder
only means anything relative to `dtm_anchor` + `days_to_maturity`, and `propagule` /
`sow_depth_inches` / `thin_to_inches` are archetype-determined. So: this contract + the gate are a
one-time cross-crop layer; the VALUES are authored one crop at a time, in archetype batches.

---

## The fields

| Field | Location | Type | Required when | Absent when |
|---|---|---|---|---|
| `propagule` | crop | enum¹ | **every crop** | never (universal) |
| `dtm_anchor` | crop | enum² | `days_to_maturity` non-empty AND you want a non-`from_sow` anchor | empty-DTM perennials (MUST be absent); annuals where `from_sow` is correct (app defaults to it) |
| `day_range_from_sow` | each `growth_stages[]` | `[min,max]` int days | present on a crop -> present on **all** its stages | perennials/trees where a from-planting timeline is not meaningful |
| `sow_depth_inches` | crop | `[min,max]` | propagule ∈ {seed, clove, set, tuber}, **except microgreens** | transplant / grafted / division / crown / bare_root / slip³; microgreens (surface-sown) |
| `thin_to_inches` | crop | `[min,max]` | direct-sown / thinnable crops | microgreens (`spacing_inches == []`); one-per-station transplants |
| `harvest_window_days` | crop | `[min,max]` | crops with a real productive window | one-shot harvests |
| `divide_every_years` | crop | positive int | divide-to-renew perennials (mint, chives, rhubarb, asparagus) | everything else |

¹ `propagule` ∈ {seed, transplant, clove, set, tuber, slip, crown, bare_root, division, rhizome, runner}
² `dtm_anchor` ∈ {from_sow, from_transplant, from_planting}
³ `slip` (sweet potato) has a real planting depth but is not in the sow_depth-required set; author it if a T1 source gives one, but the gate does not demand it.

`weeks_indoors` already exists; the app reads `start_method.weeks_before`. **Reconcile at authoring:**
make `weeks_before` canonical and `weeks_indoors` mirror-or-drop (note which in provenance). Open flag.

## `dtm_anchor` by archetype (from the audit's DTM split)
- **Empty-DTM perennials** -- citrus, woody herbs (rosemary/sage/thyme/oregano/lavender), all
  fruit trees & woody berries: `days_to_maturity == []` -> **`dtm_anchor` MUST be absent** (gate-enforced).
- **Herbaceous perennials** (mint, chives, lemongrass, bee-balm, echinacea): DTM present ->
  `from_planting`.
- **Propagule crops** (garlic=clove, potato=tuber, sweet-potato=slip, onion/shallot=set): `from_planting`.
- **Annuals:** indoor-started -> `from_transplant`; direct-sown -> `from_sow` (or leave absent; the
  app defaults to `from_sow`).

## The ladder (`day_range_from_sow`)
Days from the planting event to ENTERING each stage. The germination stage's `[min,max]` is the
sprout window; the harvest stage's entry should track `days_to_maturity` (see the WARNING tier).
Ladder counts are archetype-consistent (audit §3): 6 annuals/flowers, 5 herbaceous
perennials/microgreens, 4 tender perennials (lemongrass). Stages carry `id` (Microgreens Mix uses
`stage_id`; the app normalizes -- author new ladders with `id`).

---

## Gate tiers (`timing_spine_gate.py`)

**VIOLATIONS (exit 1) -- hard shape/coherence, checked only when the field is PRESENT (absence is a
coverage TODO, so the un-authored roster stays green except real defects):**
1. `propagule` / `dtm_anchor` in their enums.
2. Empty-DTM crop must NOT carry `dtm_anchor`.
3. `[min,max]` arrays (`sow_depth_inches`, `thin_to_inches`, `harvest_window_days`, every stage
   `day_range_from_sow`): numeric pair, `min <= max`, `min >= 0`; `divide_every_years` a positive int.
4. Ladder **all-or-nothing**: present on any stage -> present on all.
5. Ladder **mins non-decreasing up to and including the harvest anchor** (the `id=='harvest'` stage,
   else the last stage). Post-harvest cyclic stages (dormancy / flowering / spring_regrowth / curing)
   are exempt -- they legitimately overlap. (This is why `chives` passes and `shallot` does not.)
6. `sow_depth_inches` present for seed/clove/set/tuber propagules (microgreens exempt: `spacing_inches == []`).
7. `propagule` <-> `start_method` consistency: `seed` not on a `grafted_nursery_tree`; a
   clove/slip/tuber/rhizome propagule's word appears in the start_method prose.
8. **Amend-not-recert provenance:** a certified crop carrying any of the six NEW columns must log a
   `verification_status.field_additions` entry (`field` ∈ the new columns or `"timing_spine"`), and
   that entry's `sources` must be catalogued + T1. (`day_range_from_sow` predates this pass -- authored
   at certification -- so it is EXCLUDED from the provenance requirement.)

**WARNINGS (`--warnings`, exit unaffected) -- surfaced, not blocking:**
- Harvest-stage entry outside a +/-15% widened DTM band. This is anchor-dependent (a `from_sow`
  ladder vs a `from_transplant` DTM differ by the indoor period) and cut-and-come-again crops
  legitimately harvest before DTM, so it is a review signal, not a wall. Authoring `dtm_anchor`
  per crop resolves most of these (e.g. celery's [150,200] ladder reconciles with DTM [80,120] once
  it is `from_transplant`).

**Coverage:** `--slugs a,b,c` / `--all-certified` marks a required scope; a required crop missing
`propagule` is a TODO (exit 1). No scope -> coverage is informational.

## Authoring order (per the runbook §6)
1. **garlic** (propagule pilot: clove / from_planting / sow_depth / planting->curing ladder).
2. Fall/winter set: brassicas, alliums (shallot/onion), cool greens, fava, overwinter roots.
3. The remaining certified crops toward all 114.
4. New archetype crops (§E) adopt this checklist + gate at certification (fold-in).

## Handoff
When a batch passes: `npm run build:guides` in plant-app (branch `feat/crop-guide-foundation`)
regenerates `guides.json`; `crop-timing.ts` lights up automatically (graceful -- present-or-omitted).
