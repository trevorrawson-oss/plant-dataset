# Pest / IPM Control-Ladder Foundation -- Design Spec

**Date:** 2026-07-22
**Arc type:** cross-crop field addition (register row 22) -- restructure + normalization, not greenfield
**Scope decision:** Approach **B** (ladder + shared method catalog + stable pest/disease identities). Approach **C** (per-crop pest-management "hub": philosophy essay + scouting calendar) is captured as a FUTURE register row, to be built additively when a consumer pulls on it.
**Pilot:** Broccoli (primary) + Microgreens (legit short-ladder case) + Celery (second crop, cross-family). Trevor is actively growing all three -- dogfoodable.

---

## 1. Context and goal

Every crop already carries `pests[]` and `diseases[]` as per-crop free-form lists. Two problems:

1. **Treatment is a single blob.** Each entry has one `organic_treatment_*` (or, on microgreens, `management_*`) string. There is no softest-first escalation, no honest "start here, turn to that if the soft method fails," and no fair pros/cons of each control type.
2. **No canonical vocabulary.** "Aphids" on tomato and "Aphids" on broccoli are independent objects. Pests/diseases have no stable identity, so a future variety-resistance arc has nothing to reference.

**Goal:** give every pest/disease a structured, honest **IPM escalation ladder** built on a **shared, authored-once catalog of control methods**, and a **stable `id`** per problem. This delivers the pesticide-honesty feature Trevor asked for ("don't hate on any type, be honest about best use + pros/cons") AND lays the identity foundation the variety-resistance arc depends on -- which is exactly why this arc is sequenced BEFORE the variety expansion.

**North-star fit:** accuracy + trust + authority. The distinctive trust signal is honesty in both directions -- naming conventional synthetics fairly (not demonizing them) AND being candid that "organic" is not automatically harmless.

## 2. The honest framing (the accuracy crux)

- **Softest-first escalation.** A control ladder is ordered cultural -> physical -> biological -> soft chemical -> conventional. Order encodes "try this, escalate only if needed."
- **Ladders may legitimately bottom out early.** Clubroot (no chemical cure -- rotation, liming, resistant varieties only) and blackheart (calcium physiology, no spray) and microgreens (raw, ~10-day, indoor -- prevention is the whole game) all have ladders that stop at `cultural`. The design and the gate must treat a short ladder as VALID, never as incomplete.
- **Conventional is last-resort, never default.** Where a synthetic option exists, it is labeled rescue-only with its real costs (kills beneficials + pollinators, resistance, pre-harvest interval).
- **"Organic" != "harmless."** Copper accumulates in soil and harms aquatic life; sulfur burns foliage and hits beneficial mites; neem and spinosad harm bees while wet; Bt kills all caterpillars including butterfly larvae. These cons are authored honestly in the catalog.

## 3. Governing principles (the contract)

- **Shared catalog, referenced by id.** Mirror the existing `source_catalog` pattern: honest pros/cons of a method are authored ONCE in `control_methods` and referenced from every crop. No per-crop duplication, no drift.
- **Order is the escalation.** `control_ladder` is a flat ordered array; the softest-first semantics live in the order, and tier bands are derived from each method's catalog `tier` (not duplicated per rung).
- **New keys only are enforced.** The gate requires the NEW keys (`id`, `type`, `control_ladder`); it tolerates the heterogeneous legacy prose shapes so this arc stays a treatment-dimension change, not a full record re-key.
- **T1 sourcing.** Control methods and ladders cite extension IPM sources (UC IPM is the gold standard) at the same T1 bar the rest of the dataset holds.
- **Soft is a stage, not a resting state (INV-1).** The pilot ships a soft/standalone gate; it hard-flips into the A39 register floor + `gate_all` when the roster-wide rollout reaches full coverage.

## 4. Data model

### 4.1 Shared catalog -- new top-level `control_methods`

Keyed dict, id -> method, mirroring `source_catalog`:

```json
"control_methods": {
  "insecticidal_soap": {
    "name": "Insecticidal soap",
    "tier": "soft_chemical",
    "applies_to": ["insect_soft_bodied"],
    "how_it_works_beginner": "...",
    "how_it_works_seasoned": "...",
    "best_use": "Early, light soft-bodied infestations you can coat directly.",
    "pros": ["Low toxicity to people and pets", "OMRI-listed for organic use"],
    "cons": ["Contact-only, no residual -- must hit the insect", "Can burn foliage in heat"],
    "cautions": ["Harms soft-bodied beneficials on direct contact"],
    "sources": ["umn_ext"],
    "anchoring_urls": { "umn_ext": { "url": "...", "verified": "2026-07-22" } }
  }
}
```

Required keys: `name`, `tier` (enum), `applies_to` (non-empty), `how_it_works_beginner`, `how_it_works_seasoned`, `best_use`, `pros` (non-empty), `cons` (non-empty), `sources` (non-empty, T1, catalogued), `anchoring_urls` (keys match `sources`). Optional: `cautions`.

### 4.2 Per-crop -- `id` + `type` + `control_ladder`

```json
"pests": [{
  "id": "aphids",
  "name": "Aphids",
  "type": "insect",
  "symptoms_beginner": "...", "cause_seasoned": "...", "prevention_beginner": "...",
  "control_ladder": [
    { "method": "balance_nitrogen" },
    { "method": "water_spray" },
    { "method": "beneficial_predators" },
    { "method": "insecticidal_soap" },
    { "method": "neem_oil" },
    { "method": "pyrethrin", "note_seasoned": "Rescue only; spray at dusk to spare bees, observe the pre-harvest interval." }
  ]
}]
```

- `id`: kebab-case slug, unique within the crop. The vocabulary the variety-resistance arc references.
- `type`: the problem class (e.g. `insect`, `fungal`, `bacterial`, `physiological`), used by the `applies_to` coherence check. Added where missing (broccoli pests lack it).
- `control_ladder`: flat ordered array of `{ method, note_beginner?, note_seasoned? }`. `method` references `control_methods`. Optional per-rung notes carry crop-specific nuance.
- The old `organic_treatment_*` / `management_*` blob is RETIRED; its content folds into the ladder rung notes.

### 4.3 The tier taxonomy (`control_methods[].tier` enum)

Ordered softest -> strongest. The monotonic-order gate check ranks by this order:

| rank | `tier` | examples |
|---|---|---|
| 1 | `cultural` | rotation, sanitation, resistant varieties, timing, spacing, soil pH, balanced fertility, trap crops |
| 2 | `physical` | floating row cover, netting, handpicking, sticky/pheromone traps, collars, water spray, pruning out infected tissue |
| 3 | `biological` | lady beetles, lacewings, parasitic wasps, beneficial nematodes, Bt |
| 4 | `soft_chemical` | insecticidal soap, neem/hort oil, kaolin, iron-phosphate bait, sulfur, copper, spinosad |
| 5 | `conventional` | pyrethroids, carbaryl, malathion, neonicotinoids, chlorothalonil |

Note (documented judgment call): **spinosad sits in `soft_chemical`, not biological** -- it is a sprayed OMRI product with a real bee caution, so grouping it with the soaps/oils is the honest, useful placement. Rung 1 `cultural` is where **resistant varieties** live -- the direct handoff to the variety-resistance arc.

### 4.4 The synthetics ceiling -- Option 2 (approved)

The conventional rung names a **representative active-ingredient class + a common example** ("a pyrethroid such as permethrin"; "carbaryl for beetles"), ALWAYS paired with the honest caution set (kills beneficials + bees, resistance, pre-harvest interval). Active ingredients are generic facts, not brand promotion. This is the extension-authoritative middle: honest, useful, non-preachy. (Rejected: Option 1 class-only = too vague; Option 3 brands/formulations = endorsement + goes stale.)

### 4.5 Safety spine -- new top-level `pesticide_safety_education`

Authored once, surfaced once (not repeated per crop), mirroring the existing `soil_education` / `ph_education` top-level objects. Carries the universal spine:

- **"Always read and follow the label -- the label is the law"** (legal/safety anchor)
- **Pre-harvest interval (PHI)** -- how long after spraying before you can eat it
- **Pollinator protection** -- never spray open blooms; spray at dusk
- **PPE / keep kids + pets off until dry**
- **Resistance management** -- rotate modes of action

Product-specific specifics live in each catalog method's `cautions`; the universal spine lives here.

## 5. The gate -- `control_ladder_gate.py`

Standalone, TDD (RED before GREEN), `--coverage` flag. Soft/standalone through the pilot; hard-flips into `whole_crop_gate` A39 + `gate_all` when rollout coverage is complete (INV-1). Each defect class below is injected into a SCRATCH copy and confirmed to bounce before the gate is trusted.

**Catalog integrity**
- Every `control_methods` entry carries the required keys; `tier` in the enum; `applies_to`/`pros`/`cons` non-empty; sources T1 + catalogued in `source_catalog`; `anchoring_urls` keys match `sources`.

**Ladder integrity (the three real defenses)**
1. **Referential** -- every `method` in a `control_ladder` exists in `control_methods`. *Defect: dangling id -> bounce.*
2. **Monotonic tier** -- referenced method tiers are non-decreasing by rank (genuinely softest-first). *Defect: conventional-before-cultural -> bounce.*
3. **`applies_to` coherence** -- a method's targets must be compatible with the problem's `type`. *Defect: insecticidal soap under a fungal disease -> bounce.*

**Identity**
- Every pest/disease has a unique kebab `id` within its crop. *Defect: missing or duplicate id -> bounce.*

**Short-ladder legitimacy (the "N/A" analog)**
- A `control_ladder` of length >= 1 is valid; the gate NEVER requires a ladder to reach conventional. Cultural-only ladders (clubroot, blackheart, microgreens) MUST pass. *Defect: gate flags a cultural-only ladder as incomplete -> that is a gate bug, RED-tested to confirm it does not.*

**Coverage (report now; A39 floor after rollout)**
- Every certified crop's pest AND disease records carry `id` + `type` + `control_ladder`. All certified crops have >= 1 pest/disease record (the 9 zero-record crops are the uncertified shells, out of scope), so there is no whole-crop `control_ladder`-absent exemption -- coverage is universal across the certified roster.

**`register_completeness` ruling:** `control_methods`, `control_ladder`, `tier`, `applies_to`, `pesticide_safety_education`, and the per-problem `id` are ruled into EXCLUDED_KEYS so A25 does not flood.

## 6. Reconciliation -- tight scope

The three existing pest/disease record shapes:
- **Broccoli shape:** `name`, `symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`, `audience`, `sources`. Lacks `type`.
- **Celery / tomato shape:** the broccoli shape + `type` + `severity`.
- **Microgreens shape:** `name_*`, `description_*`, `management_*`.

The arc touches ONLY the treatment dimension:
- **Add** `id` + `type` (where missing) + `control_ladder`.
- **Retire** the treatment blob (`organic_treatment_*` / `management_*`); content folds into ladder rung notes.
- **Leave alone** the symptom/cause/prevention/description prose, including the microgreens `name_*` / `description_*` shape. The gate enforces only the new keys, so legacy prose shapes are tolerated.

Explicitly OUT of scope: unifying the symptom/description field NAMES across shapes (a possible future cleanup, not needed for the ladder or variety-resistance).

## 7. The pilot

- **Broccoli (primary).** Cabbageworms/loopers -> Bt (the iconic biological rung); flea beetles + cabbage root maggot -> row cover (physical exclusion); clubroot -> cultural-only dead end (no chemical cure -- rotation, lime to ~pH 7.2, resistant varieties); aphids -> soap; downy mildew -> copper. Exercises the full ladder + the honest no-spray case. Its lean record shape (no `type`) also tests the normalization.
- **Microgreens (legit short-ladder case).** Fungus gnats (insect) + damping-off (fungal). Existing prose already says the right thing ("no rescue spray for a raw cut crop... prevention is the whole game"). Ladders are cultural-only. Proves the short-ladder-is-valid branch.
- **Celery (second crop, cross-family).** Apiaceae, not brassica -- proves the model is not brassica-specific. Carries the fuller record shape (`type`/`severity`), so the pilot reconciles both shape extremes. Blackheart (calcium) = a second physiological no-spray case.

Brussels sprouts is deliberately NOT a pilot crop -- its complex is a near-duplicate of broccoli's, so it adds no pilot diversity. It inherits the model at rollout.

## 8. Sourcing

T1 extension IPM. UC IPM (`ucanr`) is the gold standard for method-level pros/cons/actives; land-grant extension IPM pages for the rest. May add a few `source_catalog` entries (UC IPM specifically), as the region arcs did. Per-method `sources` are T1-only so cert source-tier holds.

## 9. Rollout (pilot -> column pass -> hard-flip)

1. **Pilot** (broccoli + microgreens + celery), soft standalone gate, ~16 ladders + the seed catalog (~15-25 methods) + `pesticide_safety_education`.
2. **Trevor's go** after reading the pilot.
3. **Roster-wide column pass in family batches** (brassicas -> nightshades -> cucurbits -> alliums -> legumes -> roots -> greens -> herbs -> trees -> berries -> citrus -> sprouts). ~1,000+ ladders across 119 certified crops, but the shared catalog makes this "reference the right methods in the right order," not 1,000 prose blobs; the catalog stabilizes after the first few families. Amend-not-recert with per-field provenance.
4. **Hard-flip** `control_ladder_gate` -> A39 + `gate_all` when coverage is complete.
5. **Variety-resistance arc** (a future register row, the next arc after this one) then references the pest/disease `id`s.

## 10. Field-addition register entry

Add row 22: **Pest/disease `control_ladder` + shared `control_methods` catalog + stable pest/disease `id`** (+ `pesticide_safety_education`). Status: PILOT (broccoli/microgreens/celery). Trigger: stable roster (MET, 128 crops / 119 certified). Approach: column GS arc, restructure + normalization. Consumer: app pest guidance + the variety-resistance handoff.

## 11. Scope boundaries (explicitly OUT)

- **Approach C** -- crop-level pest-management philosophy essay + scouting calendar (a "pest hub" destination). Future additive row; scouting overlaps the existing notifications/`weather_triggers`/`tasks` machinery.
- **Symptom/description field-name unification** across the three record shapes.
- **Variety-level resistance fields** (`resists:` / `susceptible_to:`) -- the NEXT arc; this one only builds the vocabulary it will reference.
- **The 9 uncertified shells** (mushrooms + avocado/olive/artichoke/asparagus) -- out of the certified roster.

## 12. Success criteria

- `control_methods` catalog seeded with the pilot's methods, each with honest pros/cons/cautions + T1 sources.
- Broccoli, celery, microgreens: every pest/disease carries `id` + `type` + `control_ladder`; treatment blobs retired.
- `pesticide_safety_education` top-level object present.
- `control_ladder_gate` GREEN on the pilot; all defect classes RED-tested on a scratch copy (dangling ref, non-monotonic tier, applies_to/type mismatch, missing/dup id, cultural-only-must-pass).
- `whole_crop_gate` + `gate_all` + `register_completeness` + dash/temp sweep + `release_verify` clean; canonical footprint exact outside the touched crops + new top-level objects.
- Content honest on both sides: conventional named fairly (Option 2), organic cons stated candidly.

## 13. Open items to confirm during authoring

- The exact `type` enum values (insect / fungal / bacterial / viral / physiological / mite / mollusk / ...) -- settle from the pilot's real problems, reserve unseen values.
- The exact `applies_to` target vocabulary (insect_soft_bodied, insect_chewing, fungal_foliar, soil_borne, ...) -- coarse, settled from the pilot, extended at rollout.
- Whether `severity` (on celery/tomato, absent on broccoli) is normalized in or left legacy -- lean: leave legacy this arc (not load-bearing for the ladder).
