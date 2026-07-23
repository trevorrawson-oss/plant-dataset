# Variety disease-resistance pilot -- design (apple + strawberry)

**Date:** 2026-07-23
**Arc type:** cross-crop field addition (field-addition register **row 24**) -- a NEW per-variety field,
layered on the pest/IPM control-ladder foundation (row 23).
**Scope decision:** graded per-variety `resistance` map keyed by the crop's own pest/disease `id`s,
piloted on **apple + strawberry**, each crop **fully pest-migrated first** (Option B -- the
broccoli/celery precedent). Roster-wide rollout across the other variety crops is a LATER session.
**North-star fit:** accuracy + trust + authority. Resistance is the single highest-value
variety-choice attribute for a gardener, it is T1-sourceable from extension variety trials, and it is
IPM ladder rung-1 (prevention) made concrete and machine-readable. [[trevor-north-star-accuracy-authority]]

---

## 1. The problem

The pest/IPM arc (row 23) gave every migrated pest/disease a stable `id` and an honest, softest-first
`control_ladder`. Its rung-1 (cultural) explicitly points at "choose a resistant variety" as the
prevention layer -- but there is no structured, referenceable record of *which* variety resists
*which* disease. That resistance story exists today only as free prose:

- **Apple** varieties carry a `disease_notes` string (Liberty: *"Immune to apple scab; a strong
  low-spray choice."*) and resistance woven into `note_beginner`/`note_seasoned`.
- **Strawberry** varieties carry it only in `note_seasoned` (Earliglow: *"good resistance to red stele
  and verticillium"*).

Prose is not queryable: the app cannot shrink a variety's pest watch-list, mark IPM rung-1 as already
satisfied, or filter varieties by resistance. Authoring resistance as more prose would be a backfill
treadmill. This arc adds the structured, id-referencing layer the pest arc was sequenced to enable.

---

## 2. Design overview

Two steps per crop, in order:

1. **Pest-migration (full crop).** Run the row-23 transform over **every** pest and disease on the crop:
   add `id` + `type` + `control_ladder`, retire the legacy `organic_treatment_*` blob into the ladder
   rung notes. This gives resistance its referential targets AND fully advances the pest rollout for the
   two crops (no half-migrated state -- matching broccoli/celery).
2. **Author `resistance`.** Add an optional per-variety `resistance` map, keyed by the crop's own
   disease/pest `id`s, valued by a resistance grade, T1-sourced from extension variety-resistance tables.

A new **standalone soft gate** (`variety_resistance_gate.py`) enforces the resistance layer; the
migration reuses the existing `control_ladder_gate` (extended once for the `vertebrate` type).

---

## 3. Step 1 -- the full-crop pest-migration

Identical transform to the pest pilot (spec 2026-07-22), applied to **all** problems on both crops:

| Crop | Pests | Diseases | Total ladders |
|---|---|---|---|
| Apple | Codling moth, Apple maggot, Plum curculio, Woolly apple aphid (4, all `insect`) | Apple scab, Fire blight (`bacterial`), Cedar-apple rust, Powdery mildew (4) | **8** |
| Strawberry | Slugs (`mollusk`), Spotted wing drosophila, Tarnished plant bug, Aphids, Two-spotted spider mite (`mite`), Root/crown weevils, Birds (`vertebrate`) (7) | Gray mold, Anthracnose, Powdery mildew, Red stele, Verticillium wilt (5, all `fungal`) | **12** |

**Per problem:** add stable kebab `id` (unique within crop) + keep `type` (already present) + author a
flat, ordered, softest-first `control_ladder` referencing the shared `control_methods` catalog. **Retire**
`organic_treatment_*`; its content folds into rung notes. Leave the legacy symptom/cause/prevention prose.

**Disease ids (the resistance vocabulary):**
- Apple: `apple-scab`, `fire-blight`, `cedar-apple-rust`, `powdery-mildew`
- Strawberry: `gray-mold`, `anthracnose`, `powdery-mildew`, `red-stele`, `verticillium-wilt`

(Pest ids are also assigned -- e.g. `codling-moth`, `spotted-wing-drosophila` -- so resistance *may*
reference a pest, though documented pest resistance on these two crops is thin.)

**Catalog growth (expected, all T1).** Apple/berry problems need methods the veg pilot's 24-method
catalog lacks. New `control_methods` entries authored once and referenced by id, e.g.: fruit bagging,
kaolin clay (Surround), codling-moth pheromone traps + mating disruption, dormant/horticultural oil,
dominant-variety sanitation, exclusion/bird netting, SWD monitoring + fine-mesh exclusion, iron-phosphate
slug bait. Each with honest pros/cons + a T1 catalogued source. The catalog stabilizes as families are
added -- this is the second family after brassica/umbellifer.

**Gate extension -- the `vertebrate` type.** `control_ladder_gate.TYPE_TARGETS` stops at
insect/mite/mollusk/fungal/bacterial/viral/physiological/nematode. Strawberry's "Birds" (`vertebrate`)
requires one new entry (`vertebrate` -> `{"vertebrate", "bird"}` or similar) + a matching `applies_to`
on the bird-netting method. TDD: RED an insecticide-under-birds violation before trusting it.

**Honesty rules (inherited from row 23, non-negotiable):**
- **Option-2 synthetics:** name the representative active-ingredient class + example, always with the
  full caution set (bees/fish/PHI/read-the-label/resistance); never brands, never class-only-vague.
- **Organic is not automatically harmless:** state candidly (copper accumulates, sulfur burns hot foliage
  + harms predatory mites, oils/insecticidal soap can burn, Bt kills all caterpillars, spinosad harms bees
  while wet).
- **Short/cultural-only ladders are VALID.** Fire blight (no home cure once systemic -- prune out, avoid
  succulent growth, resistant cultivars), red stele + verticillium (soilborne, no home chemical cure --
  resistant varieties + drainage + rotation are the whole game), and birds (exclusion only) bottom out
  early and honestly. The gate never requires reaching `conventional`.
- **Common tongue in consumer copy:** "ladybug," not "lady beetle." [[consumer-copy-common-tongue]]

**Tree-guide render (apple only).** `organic_treatment_*` renders in plant-astro's TreeGuide
(`PestsDiseasesCard`) -- unlike the veg pilot, apple retirement has site consequences. Full-crop migration
keeps apple's card single-shape (every pest AND disease laddered), so the astro session can switch the
card to render `control_ladder` cleanly. Our dataset push does not touch the live site (that happens only
at the astro submodule bump), so there is no regression window -- just a handoff note that TreeGuide must
render `control_ladder`. [[dataset-shape-change-breaks-frontends]]

---

## 4. Step 2 -- the `resistance` field

### 4.1 Shape

An **optional per-variety `resistance` map**: keys are the crop's own disease/pest `id`s, values are a
bare grade string.

```json
"resistance": {"apple-scab": "immune", "cedar-apple-rust": "resistant", "fire-blight": "resistant", "powdery-mildew": "resistant"}
```

A **map** (not `resists:`/`susceptible_to:` lists) because resistance is graded, not binary -- a map
attaches exactly one grade per disease. **Bare-string values** (not per-grade objects): confidence and
sourcing stay at the variety level (below), mirroring the lightweight `{method, note}` control-ladder
rung. If heterogeneous per-disease sourcing ever forces it, the value can widen to an object -- YAGNI for
the pilot.

### 4.2 Grade enum

`immune | resistant | tolerant | susceptible` -- an ordinal, practical "how much disease does this
variety get" scale, defined precisely so authoring and source-mapping are consistent:

| Grade | Meaning | Authoring rule |
|---|---|---|
| `immune` | Pathogen cannot establish; the variety does not get the disease. | The strongest claim -- record only when a T1 source explicitly states immunity ("immune", "not susceptible", "no infection observed"), e.g. Cornell's scab-immune Liberty. If the source says merely "resistant," use `resistant`. |
| `resistant` | Rarely or lightly affected; little to no control needed. | The source rates it resistant / highly resistant. |
| `tolerant` | Gets infected but performs/yields acceptably; moderate impact. | Absorbs source tables' "moderately resistant" / "intermediate"; note the source's wording. |
| `susceptible` | Readily affected; needs active management. | Record only when a source documents susceptibility (e.g. Honeycrisp/Gala scab-susceptible). |

### 4.3 Referential integrity (the load-bearing check)

Every `resistance` key MUST be a real `id` on that crop's `diseases[]` or `pests[]` (created in step 1).
A dangling key (typo, wrong-crop id, un-migrated problem) is a gate violation. This is why step 1
precedes step 2.

### 4.4 The unknown-vs-susceptible honesty model (the N/A case)

The map is a **positive record of documented grades only.**

- **Absence of a disease key = "not studied / not documented"** -- honest silence, NOT susceptible.
- **`susceptible` is recorded only when a source documents it.** We never infer susceptibility from
  absence.
- **A variety with no documented resistance data omits `resistance` entirely** (or `{}`) -- the legit
  N/A branch the method requires.

The pilot deliberately exercises **both** branches: at least one documented-susceptible apple
(Honeycrisp or Gala -> `apple-scab: susceptible`) for the `susceptible` grade, and at least one
no-documented-data variety with `resistance` absent for the empty/N/A branch.

### 4.5 Sourcing + confidence

- **T1-only**, per the variety-pilot rule. Grades come from extension variety-resistance tables/trials
  (Cornell, UMN, land-grant fruit/berry pages).
- Carried on the variety's existing `sources` / `anchoring_urls` (already T1-enforced by
  `whole_crop_gate` E.source-tier). If a resistance table is a new T1 source, it is added to the variety's
  `sources` and the `source_catalog`.
- Datapoint honesty via the existing per-variety `confidence_tier`.
- **Independent T1-fidelity review** on every resistance claim -- the pest arc's fidelity review caught a
  fabricated bee-toxicity claim; the same adversarial read applies here (does the cited T1 source actually
  state this grade for this variety?).

### 4.6 Coexistence with existing prose

The structured map is **additive**; the existing prose stays for display:
- Apple `disease_notes` and strawberry `note_seasoned` are kept (they carry the narrative "so what" the
  map cannot).
- The content review verifies **map and prose agree** (no variety graded `resistant` in the map but
  "susceptible" in prose). Drift is the review's job, not the gate's (agreement is not machine-checkable).

---

## 5. The gate -- `tools/variety_resistance_gate.py`

New **standalone, soft, scoped** gate in the `variety_detail_gate` family (mirrors
`control_ladder_gate` / `overwinter_hardiness_gate`).

- **Scope:** only varieties carrying a non-empty `resistance` map are checked; every other variety and
  crop is silently valid (the un-migrated roster stays green). A variety without `resistance` is the N/A
  branch -- never a violation.
- **Three defenses (TDD, adversarial RED on a scratch copy before trust):**
  1. **Referential** -- every `resistance` key is a real `id` on the crop's `diseases[]`/`pests[]`.
  2. **Enum** -- every value is in `{immune, resistant, tolerant, susceptible}`.
  3. **Shape** -- `resistance` is a dict; keys are kebab strings; values are strings (not nested).
- **RED battery (each defect injected into a scratch copy, must bounce):** dangling id key; wrong-crop id;
  invalid grade (`highly_resistant`); non-string value; `resistance` as a list not a map. Plus a clean N/A
  variety (no `resistance`) must PASS.
- **CLI:** `variety_resistance_gate.py [PATH]`; exit 1 on violations. `--coverage` reserved for the
  rollout hard-flip.
- **Hard-flip deferred (INV-1):** wiring into `whole_crop_gate` A39 + `gate_all` happens at roster-wide
  rollout, not the pilot.

**`register_completeness` ruling:** the new variety-level `resistance` key is ruled into the completeness
gate (EXCLUDED_KEYS or path-scoped to `varieties.recommended`, matching how `bearing_habit` /
`hero_description` were ruled). The disease/pest keys (`id`, `type`, `control_ladder`) reuse the existing
row-23 rulings -- no new register work for those.

**`variety_detail_gate` is untouched:** it validates COMMON_CORE + archetype traits and tolerates extra
keys, so `resistance` rides as a new optional key with no change to that gate.

---

## 6. Pilot scope

- **Apple** (tree_fruit, 16 varieties): 8-problem migration + a 4-disease x 16-variety resistance matrix.
  Marquee: Liberty (`apple-scab: immune` + multi-disease resistant, Cornell) vs scab-susceptible standards
  (Honeycrisp/Gala/McIntosh). Low-chill trio + triploids already present.
- **Strawberry** (berry, 9 varieties): 12-problem migration + resistance on the classic axis (red stele +
  verticillium already stated in notes: Earliglow/Allstar resistant; Honeoye "little disease resistance").
- **Register row 24.** No plant-astro bump (astro lane). plant-app resistance consumption = a handoff note
  (kickoff, separate lane), coordinated with the pest-UI kickoff #40; INV-2 (not load-bearing until
  gate-clean).

**Explicitly NOT in scope:** broccoli/celery/microgreens (thin `{name,dtm,note}` varieties, not enriched);
onion/leek/dry-bean and the rest of the enriched-variety roster (later rollout session); the A39 hard-flip.

---

## 7. Verification plan

Release-gated (protocol #6), same rigor as the pest pilot:
- `whole_crop_gate` apple + strawberry 18/18; `gate_all` 119/119 (the whole suite, every certified crop).
- `variety_resistance_gate` 0; `control_ladder_gate` 0 (incl. the new `vertebrate` coherence).
- Adversarial RED battery for both new/extended gates (defects bounce on REAL shapes; N/A + short ladders
  pass clean).
- `register_completeness` PASS (0 unruled).
- `release_verify` clean (bar documented single-crop-pilot artifacts).
- Footprint EXACT: only apple/strawberry `pests`/`diseases`/`varieties` + any `source_catalog`/
  `control_methods` adds; all other crops byte-identical; canonical COMPACT (0 escaped-unicode); count 128.
- Consumer sweep: 0 em-dash / double-hyphen / spelled-out-degrees in new consumer copy; "ladybug" not
  "lady beetle".
- **Independent T1-fidelity review** on resistance claims + a horticulture/content review on the ladders
  (the two-review pattern the pest pilot used).

---

## 8. Open items / risks

- **Catalog + gate growth is real work.** 20 ladders + ~8-10 new T1 catalog methods + the `vertebrate`
  gate extension. Handled by the pest pilot's subagent fan-out (per-family authoring, controller-merged,
  independent reviews).
- **Resistance-table availability.** Apple 4-disease tables are well-published (Cornell/UMN/PennState);
  strawberry red-stele/verticillium is well-documented, but gray-mold/anthracnose/mildew per-variety data
  may be thinner -> those grades may be sparse (honest absence, not fabricated).
- **Grade mapping judgment.** "Moderately resistant" -> `tolerant` is a defined convention; the content
  review confirms each mapping is faithful to the source's wording.

## 9. Out of scope (later sessions)

Roster-wide `resistance` rollout (onion/leek/dry-bean + the rest as the pest rollout gives them disease
ids); the A39/gate_all hard-flip; plant-astro TreeGuide `control_ladder` render + per-variety resistance
consumption; plant-app resistance UI.
