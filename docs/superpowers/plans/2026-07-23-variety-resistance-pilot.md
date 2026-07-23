# Variety disease-resistance pilot -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a graded per-variety `resistance` field (referencing each crop's own pest/disease `id`s) to apple + strawberry, after fully pest-migrating both crops, gated by a new soft `variety_resistance_gate`.

**Architecture:** Two deterministic TDD gate tasks + one register ruling first (no canonical writes); then T1-sourced content authored to `tools/staging/` (catalog methods, 20 control-ladders, the resistance matrices) with independent fidelity/content reviews; then a deterministic builder assembles one SHA-guarded atomic splice, dry-run on a scratch copy and gated to byte-parity before the real apply. Release ceremony (state trio + commit) is Trevor-gated.

**Tech Stack:** Python 3 (stdlib only; plain-`assert` test scripts, no pytest), compact JSON, the existing gate suite (`gate_all.py`, `whole_crop_gate.py`, `control_ladder_gate.py`, `register_completeness_gate.py`, `release_verify.py`), `apply_patch.py` (SHA-guarded splicer).

## Global Constraints

- **Canonical is COMPACT:** `json.dump(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 11 (the real apply). All content is authored to `tools/staging/`; all gating runs on scratch copies.
- **TDD, RED before GREEN.** Every gate defense is adversarially injected into a scratch copy and must bounce before the gate is trusted.
- **T1-only** for every load-bearing source: each cited id must be catalogued + `tier: T1`. Non-T1 does not ship. An **independent T1-fidelity review** vets every resistance claim + every new catalog method (the pest arc's fidelity review caught a fabrication).
- **Consumer copy:** no em dashes (use commas/colons/semicolons/periods); American English; temps `°F`; "plant" lowercase except sentence-start / "Plant Pro"; **"ladybug," never "lady beetle."**
- **Resistance grade enum:** `immune | resistant | tolerant | susceptible` (see spec §4.2 for the definitions + the "moderately resistant → tolerant" mapping).
- **Honest N/A model:** the `resistance` map records documented grades only; a missing disease key = "not studied," never susceptible; `susceptible` only when a source states it; a variety with no data omits `resistance`.
- **Footprint EXACT:** only apple/strawberry `pests`/`diseases`/`varieties` + `control_methods`/`source_catalog` additions change; every other crop byte-identical; count stays 128; 119 certified unchanged.
- **No commit/push without Trevor's OK. No plant-astro bump** (astro lane). Roster-wide rollout + A39 hard-flip = later session.
- **Concurrency:** work on `main` with hardened-commit discipline (re-`shasum` base immediately before apply; `git add` explicit paths only, never `-A`/`.`; read `git status --porcelain` before commit; pathspec-scoped `git commit <paths>`; `git show --stat HEAD` after). A path-disjoint taxonomy commit (artichoke) may be unpushed on main -- safe. [[subagent-resumability-and-concurrent-git-safety]]

---

## Reference data (the pilot's fixed inputs)

**Apple** (`variety_archetype: tree_fruit`, 16 varieties): Dorsett Golden, Anna, Ein Shemer, Zestar!, McIntosh, Liberty, Empire, Honeycrisp, Gala, Golden Delicious, Jonagold, Mutsu, Fuji, Granny Smith, Pink Lady, Dolgo.
- Pests (4, all `insect`): Codling moth, Apple maggot, Plum curculio, Woolly apple aphid.
- Diseases (4): Apple scab (`fungal`), Fire blight (`bacterial`), Cedar-apple rust (`fungal`), Powdery mildew (`fungal`).
- Disease ids: `apple-scab`, `fire-blight`, `cedar-apple-rust`, `powdery-mildew`.
- Pest ids: `codling-moth`, `apple-maggot`, `plum-curculio`, `woolly-apple-aphid`.

**Strawberry** (`variety_archetype: berry`, `berry_group: strawberry`, 9 varieties): Honeoye, Earliglow, Jewel, Allstar, Albion, Seascape, Tristar, Ozark Beauty, Quinault.
- Pests (7): Slugs (`mollusk`), Spotted wing drosophila (`insect`), Tarnished plant bug (`insect`), Aphids (`insect`), Two-spotted spider mite (`mite`), Root and crown weevils (`insect`), Birds (`vertebrate`).
- Diseases (5, all `fungal`): Gray mold, Anthracnose fruit rot, Powdery mildew, Red stele, Verticillium wilt.
- Disease ids: `gray-mold`, `anthracnose`, `powdery-mildew`, `red-stele`, `verticillium-wilt`.
- Pest ids: `slugs`, `spotted-wing-drosophila`, `tarnished-plant-bug`, `aphids`, `two-spotted-spider-mite`, `root-crown-weevils`, `birds`.

Migration transform per problem (identical to spec 2026-07-22): add kebab `id` + keep `type` + author `control_ladder` (flat ordered softest-first `{method, note_beginner, note_seasoned?}`); **retire** `organic_treatment_*`; keep symptom/cause/prevention/severity/audience/sources prose.

---

## Task 1: Extend `control_ladder_gate` for the `vertebrate` type

Strawberry's "Birds" (`type: vertebrate`) is not in `TYPE_TARGETS`, so today it fails-closed as an unrecognized type. Add the type + let bird-exclusion methods be coherent under it.

**Files:**
- Modify: `tools/control_ladder_gate.py` (`TYPE_TARGETS`, ~line 22)
- Test: `tools/test_control_ladder_gate.py` (append cases, mirroring the existing `data`/`method`/`crop`/`prob` helpers)

**Interfaces:**
- Consumes: `ladder_violations(data, crop)`, and the test helpers `data(methods, crops, srcs)`, `method(**over)`, `crop(problems, key="pests")`, `prob(**over)` already in the test file.
- Produces: `TYPE_TARGETS["vertebrate"] = {"vertebrate"}` — the applies_to target a bird-exclusion method declares.

- [ ] **Step 1: Write the failing test** — append to `tools/test_control_ladder_gate.py`:

```python
# --- vertebrate type (strawberry Birds): bird exclusion is coherent, insecticide is not ---
_vcat = {
    "bird_netting": method(name="Bird netting", tier="physical", applies_to=["vertebrate"]),
    "pyrethrin":    method(name="Pyrethrin", tier="conventional", applies_to=["insect_general"]),
}
_birds_ok = prob(id="birds", name="Birds", type="vertebrate",
                 control_ladder=[{"method": "bird_netting"}])
_birds_bad = prob(id="birds", name="Birds", type="vertebrate",
                  control_ladder=[{"method": "pyrethrin"}])
# coherent: netting applies to vertebrates
assert ladder_violations(data(_vcat, [crop([_birds_ok])]), crop([_birds_ok])) == []
# incoherent: an insecticide does not apply to a vertebrate
assert any("applies_to" in v for v in
           ladder_violations(data(_vcat, [crop([_birds_bad])]), crop([_birds_bad])))
```

- [ ] **Step 2: Run the test, verify the FIRST assertion fails**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: AssertionError — before the fix, `vertebrate` is not in `TYPE_TARGETS`, so `_birds_ok` is flagged "applies_to coherence cannot be checked" (non-empty), so `== []` fails.

- [ ] **Step 3: Add the type** — in `tools/control_ladder_gate.py`, add to the `TYPE_TARGETS` dict:

```python
    "vertebrate":    {"vertebrate"},
```

- [ ] **Step 4: Run the test, verify PASS**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: prints the existing success line, exits 0 (all assertions pass, including the two new ones).

- [ ] **Step 5: Commit** (staged; do NOT push)

```bash
git add tools/control_ladder_gate.py tools/test_control_ladder_gate.py
git status --porcelain   # confirm only these two paths
git commit tools/control_ladder_gate.py tools/test_control_ladder_gate.py -m "feat(gate): control_ladder_gate handles the vertebrate problem type (strawberry Birds)"
```

---

## Task 2: Build `variety_resistance_gate.py` (soft, scoped, TDD)

The new standalone gate: referential (key is a real crop pest/disease id) + grade enum + shape, with the N/A branch silent.

**Files:**
- Create: `tools/variety_resistance_gate.py`
- Test: `tools/test_variety_resistance_gate.py`

**Interfaces:**
- Produces: `resistance_violations(crop) -> list[str]`, `all_violations(data) -> list[str]`, `main(argv) -> int`. Consumed by Task 10 (scratch gating) and the future A39 hard-flip.

- [ ] **Step 1: Write the failing test** — create `tools/test_variety_resistance_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for variety_resistance_gate. Run: python3 tools/test_variety_resistance_gate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_resistance_gate import resistance_violations

def crop(varieties, pests=None, diseases=None):
    return {"slug": "apple",
            "pests": pests or [],
            "diseases": diseases or [{"id": "apple-scab"}, {"id": "fire-blight"}],
            "varieties": {"recommended": varieties}}

# clean: graded resistance referencing real disease ids -> no violations
assert resistance_violations(crop([{"name": "Liberty",
    "resistance": {"apple-scab": "immune", "fire-blight": "resistant"}}])) == []
# N/A branch: no resistance key -> valid
assert resistance_violations(crop([{"name": "Nodata"}])) == []
# N/A branch: empty resistance dict -> valid
assert resistance_violations(crop([{"name": "Empty", "resistance": {}}])) == []
# documented susceptible -> valid grade
assert resistance_violations(crop([{"name": "Honeycrisp",
    "resistance": {"apple-scab": "susceptible"}}])) == []
# referential covers pest ids too
assert resistance_violations(crop([{"name": "P",
    "resistance": {"woolly-apple-aphid": "resistant"}}],
    pests=[{"id": "woolly-apple-aphid"}])) == []
# RED: dangling id (typo)
assert any("is not a pest/disease id" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"appel-scab": "immune"}}])))
# RED: invalid grade
assert any("not in" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"apple-scab": "highly_resistant"}}])))
# RED: value not a string
assert any("must be a string" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"apple-scab": ["immune"]}}])))
# RED: resistance not a dict
assert any("must be a dict" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": ["apple-scab"]}])))
# RED: key not kebab
assert any("is not a kebab id" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"Apple_Scab": "immune"}}])))

print("All variety_resistance_gate tests passed.")
```

- [ ] **Step 2: Run the test, verify it fails**

Run: `python3 tools/test_variety_resistance_gate.py`
Expected: `ModuleNotFoundError: No module named 'variety_resistance_gate'`.

- [ ] **Step 3: Write the gate** — create `tools/variety_resistance_gate.py`:

```python
#!/usr/bin/env python3
"""variety_resistance_gate -- validates the per-variety `resistance` map (spec 2026-07-23).

SOFT + standalone (control_ladder / variety_detail pattern): a variety OPTS IN by carrying a
non-empty `resistance` dict; every other variety and crop is silently valid -- the un-migrated
roster stays green, and a variety with no documented resistance is the legit N/A branch, never a
violation.

VIOLATIONS (exit 1): a `resistance` key that is not a real pest/disease `id` on that crop
(referential); a grade outside the enum; a malformed shape (resistance not a dict, key not kebab,
value not a string).

Hard-flip into whole_crop_gate A39 + gate_all is deferred to the roster-wide rollout (INV-1).

Usage: variety_resistance_gate.py [PATH]
"""
import json, os, re, sys

GRADES = {"immune", "resistant", "tolerant", "susceptible"}
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _problem_ids(crop):
    ids = set()
    for key in ("pests", "diseases"):
        for p in crop.get(key, []) or []:
            pid = p.get("id")
            if isinstance(pid, str):
                ids.add(pid)
    return ids


def _variety_objs(crop):
    v = crop.get("varieties")
    if not isinstance(v, dict):
        return []
    rec = v.get("recommended")
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def resistance_violations(crop):
    V = []
    slug = crop.get("slug", "?")
    valid_ids = _problem_ids(crop)
    for x in _variety_objs(crop):
        r = x.get("resistance")
        if r is None:
            continue  # N/A branch: absence is always valid
        nm = x.get("name") or x.get("id") or "?"
        if not isinstance(r, dict):
            V.append(f"{slug}/{nm}: resistance must be a dict, got {type(r).__name__}")
            continue
        for did, grade in r.items():
            if not (isinstance(did, str) and KEBAB_RE.match(did)):
                V.append(f"{slug}/{nm}: resistance key {did!r} is not a kebab id")
            elif did not in valid_ids:
                V.append(f"{slug}/{nm}: resistance key {did!r} is not a pest/disease id on {slug} "
                         f"(known: {sorted(valid_ids)})")
            if not isinstance(grade, str):
                V.append(f"{slug}/{nm}: resistance[{did!r}] value must be a string, "
                         f"got {type(grade).__name__}")
            elif grade not in GRADES:
                V.append(f"{slug}/{nm}: resistance[{did!r}] grade {grade!r} not in {sorted(GRADES)}")
    return V


def all_violations(data):
    V = []
    for crop in data.get("crops", []):
        V += resistance_violations(crop)
    return V


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path) as fh:
        data = json.load(fh)
    V = all_violations(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"variety_resistance_gate: {len(V)} violation(s)")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run the test, verify PASS**

Run: `python3 tools/test_variety_resistance_gate.py`
Expected: `All variety_resistance_gate tests passed.`

- [ ] **Step 5: Verify the gate is clean on the current canonical** (no crop carries `resistance` yet, so 0 violations — proves it is silent on the un-migrated roster)

Run: `python3 tools/variety_resistance_gate.py`
Expected: `variety_resistance_gate: 0 violation(s)`, exit 0.

- [ ] **Step 6: Commit** (staged; do NOT push)

```bash
git add tools/variety_resistance_gate.py tools/test_variety_resistance_gate.py
git status --porcelain
git commit tools/variety_resistance_gate.py tools/test_variety_resistance_gate.py -m "feat(gate): add soft standalone variety_resistance_gate (referential + grade enum + shape)"
```

---

## Task 3: Rule `resistance` into `register_completeness_gate`

The new variety-level key must be ruled so `register_completeness_gate` does not flag it as an unregistered field (matching how `bearing_habit` / `hero_description` were ruled at berry-pilot time). The disease keys (`id`, `type`, `control_ladder`) reuse the existing row-23 rulings — do NOT re-add them.

**Files:**
- Modify: `tools/register_completeness_gate.py` (the EXCLUDED_KEYS / path-scoped ruling structure — locate how `bearing_habit`/`hero_description` are ruled and follow that exact pattern; `resistance` is a `varieties.recommended`-scoped key like `hero_description`).
- Test: `tools/test_register_completeness_gate.py` (add a case if the file's style supports it; otherwise the Step-3 canonical run is the check).

- [ ] **Step 1: Locate the ruling pattern**

Run: `grep -nE "hero_description|bearing_habit|EXCLUDED|recommended|PATH" tools/register_completeness_gate.py`
Expected: shows the list/dict where variety-scoped keys are registered.

- [ ] **Step 2: Add `resistance`** following the identical pattern used for `hero_description` (same `varieties.recommended` path scope).

- [ ] **Step 3: Verify the gate is clean on the current canonical**

Run: `python3 tools/register_completeness_gate.py`
Expected: 0 unruled keys (canonical has no `resistance` yet, but the ruling is inert-and-correct; it must not newly flag anything).

- [ ] **Step 4: Commit** (staged; do NOT push)

```bash
git add tools/register_completeness_gate.py
git status --porcelain
git commit tools/register_completeness_gate.py -m "chore(register): rule the per-variety resistance key into register_completeness"
```

---

## Task 4: Author the new T1 `control_methods` catalog additions

The apple/berry problems need methods the 24-method veg catalog lacks. Author them once, referenced by id, honest pros/cons, T1-sourced. **This is a subagent authoring task followed by an independent T1-fidelity review.**

**Files:**
- Create: `tools/staging/variety_resist_catalog_content.json` (the new method objects, keyed by id)
- Create: `tools/staging/variety_resist_catalog_sources.md` (per-method T1 provenance: source id, URL, verified date, the exact sourced claim)

**Contract (each method mirrors the existing `control_methods` shape — inspect an existing entry first):**
- Required keys: `name`, `tier` (one of cultural/physical/biological/soft_chemical/conventional), `applies_to` (list of coherence targets — see `TYPE_TARGETS`; bird methods use `["vertebrate"]`), `how_it_works_beginner`, `how_it_works_seasoned`, `best_use`, `pros` (non-empty), `cons` (non-empty), `sources` (catalogued + T1), `anchoring_urls`.
- Candidate new methods (author only those actually referenced by the Task 5/6 ladders; drop any unused): `fruit_bagging` (physical), `kaolin_clay` (physical/soft; Surround), `codling_moth_pheromone_trap` (physical/monitoring), `mating_disruption` (biological/behavioral), `dormant_oil` (soft_chemical), `horticultural_oil` (soft_chemical), `bird_netting` (physical, applies_to vertebrate), `swd_exclusion_netting` (physical), `swd_monitoring_traps` (physical/monitoring), `iron_phosphate_slug_bait` (soft_chemical), `straw_mulch` (cultural, strawberry gray-mold), `renovation_bed_sanitation` (cultural, strawberry). Reuse existing catalog ids wherever a method already exists (crop_rotation, garden_sanitation, resistant_varieties, insecticidal_soap, neem_oil, sulfur, copper, handpicking, sticky_traps, row_cover, etc.) — do NOT duplicate.
- **Honesty rules (spec §3):** Option-2 synthetics (active-ingredient class + example + full caution set, never brands); "organic is not automatically harmless" stated candidly; "ladybug" not "lady beetle".
- New T1 sources (extension apple/berry IPM: UC IPM `ucanr_ext`, Cornell, `umn_ext`, `psu_ext`, `msu_ext`, land-grant) are added to `source_catalog` in the Task 9 build if not already present — list any needed additions in the sources note.

- [ ] **Step 1:** Inspect an existing catalog entry for the exact shape: `python3 -c "import json;d=json.load(open('crops_data_final.json'));import sys;json.dump(list(d['control_methods'].items())[0],sys.stdout,indent=2,ensure_ascii=False)"`
- [ ] **Step 2:** Author the new method objects to `tools/staging/variety_resist_catalog_content.json`, each fully sourced, following the honesty rules.
- [ ] **Step 3:** Write `tools/staging/variety_resist_catalog_sources.md` with per-method T1 provenance.
- [ ] **Step 4: Independent T1-fidelity review** (fresh subagent): for each new method, does the cited T1 source actually support the pros/cons/best_use claims? Flag any unsupported claim (the neem-bee-toxicity class of error). Fix flagged items; re-review until clean.
- [ ] **Step 5: Commit** the staging content (staged; do NOT push): `git add tools/staging/variety_resist_catalog_content.json tools/staging/variety_resist_catalog_sources.md && git commit <those paths> -m "content(catalog): T1 control_methods additions for apple/berry problems"`

---

## Task 5: Author apple's 8 control-ladders (migration content)

**Files:**
- Create: `tools/staging/apple_ladders_content.json` — the full new `pests` (4) + `diseases` (4) arrays for apple, each problem carrying `id` + `type` + `control_ladder`, with `organic_treatment_*` REMOVED and its content folded into rung notes, and all other legacy prose (`symptoms_*`, `cause_*`, `prevention_*`, `severity`, `audience`, `sources`, `anchoring_urls`) preserved verbatim from the canonical.
- Create: `tools/staging/apple_ladders_notes.md` — per-ladder rationale + any source additions.

**Contract:**
- Each `control_ladder` is a flat ordered array, softest-first, of `{method, note_beginner, note_seasoned?}` where `method` is a catalog id (existing or from Task 4). Rung order must be monotonic by the method's catalog `tier` (cultural → physical → biological → soft_chemical → conventional).
- `applies_to` coherence: methods on a `fungal`/`bacterial` disease must target disease/fungal/bacterial; on `insect` pests, insect targets. (The Task 1/2 gates enforce this on the scratch in Task 10.)
- **Honest short ladders where correct:** Fire blight (bacterial: prune out, avoid excess nitrogen/succulent growth, resistant cultivars; copper/antibiotic is a limited, cautioned rung, not a cure) may bottom out before conventional. Follow spec §3 honesty rules; "ladybug" not "lady beetle".
- Worked-example rung shape (do NOT copy verbatim — author from the crop's real prose + T1):

```json
{"method": "resistant_varieties",
 "note_beginner": "The surest fix for scab is to plant a resistant apple like Liberty, so you rarely have to spray at all.",
 "note_seasoned": "Cultivar resistance (e.g. Liberty, scab-immune) is the highest-leverage control; it removes most of the spray schedule."}
```

- [ ] **Step 1:** Read apple's current `pests` + `diseases` from the canonical (READ-ONLY) and copy the preserved prose fields exactly.
- [ ] **Step 2:** Author the 8 problems with `id` + `control_ladder` into `apple_ladders_content.json`, retiring `organic_treatment_*` into rung notes.
- [ ] **Step 3: Horticulture/content review** (fresh subagent): are the ladders correct, honest, softest-first, and is each retired-blob's substance preserved in the notes? Fix flagged items.
- [ ] **Step 4: Commit** the staging file (staged; do NOT push).

---

## Task 6: Author strawberry's 12 control-ladders (migration content)

Same contract as Task 5, for strawberry's 7 pests + 5 diseases.

**Files:**
- Create: `tools/staging/strawberry_ladders_content.json`
- Create: `tools/staging/strawberry_ladders_notes.md`

**Notes specific to strawberry:**
- Birds (`vertebrate`): exclusion-only ladder (bird netting) — a valid short ladder; no insecticide rung.
- Red stele + verticillium (soilborne `fungal`): no home chemical cure — resistant varieties + drainage/rotation + clean stock; short cultural ladders, honest.
- Gray mold: cultural-forward (airflow, straw mulch, sanitation, timely harvest) before any soft_chemical rung.
- SWD: monitoring + fine-mesh exclusion + prompt harvest; cautioned conventional rung only if justified.

- [ ] **Step 1:** Read strawberry's current `pests` + `diseases` (READ-ONLY), copy preserved prose.
- [ ] **Step 2:** Author the 12 problems into `strawberry_ladders_content.json`, retiring the blobs.
- [ ] **Step 3: Horticulture/content review** (fresh subagent). Fix flagged items.
- [ ] **Step 4: Commit** the staging file (staged; do NOT push).

---

## Task 7: Author apple's per-variety resistance matrix

**Files:**
- Create: `tools/staging/apple_resistance_content.json` — a map `{variety_id -> {disease_id -> grade}}` for the 16 apple varieties, documented grades only.
- Create: `tools/staging/apple_resistance_sources.md` — per-variety-per-grade T1 provenance (source id, URL, verified date, the exact sourced wording, and the enum mapping decision, e.g. "moderately resistant → tolerant").

**Contract:**
- Keys are `apple-scab | fire-blight | cedar-apple-rust | powdery-mildew` (or a pest id, if a documented pest-resistant variety exists — rare). Values are the grade enum.
- **Documented grades only.** Omit a disease for a variety when no T1 source grades it (honest silence). Record `susceptible` only when a source states it.
- **Deliberately exercise both N/A branches:** at least one variety with `apple-scab: susceptible` (e.g. Honeycrisp or Gala, both scab-susceptible standards) AND at least one variety with `resistance` entirely absent (no documented data).
- Sources: extension apple disease-resistance tables (Cornell, UMN, PennState — T1). Extend the variety's existing `sources`/`anchoring_urls` where the resistance source differs from its bloom/chill source.
- **Map-vs-prose agreement:** each graded value must not contradict the variety's `disease_notes`/`note_*` prose.

- [ ] **Step 1:** For each variety, gather T1-documented grades from extension resistance tables; record provenance in the sources note.
- [ ] **Step 2:** Write `apple_resistance_content.json` (documented grades only).
- [ ] **Step 3: Independent T1-fidelity review** (fresh subagent): for every grade, does the cited T1 source actually assign that resistance level to that named cultivar? Reject any grade not traceable to a T1 source (fabrication guard). Confirm the deliberate susceptible + absent cases are present. Fix; re-review until clean.
- [ ] **Step 4: Commit** the staging file (staged; do NOT push).

---

## Task 8: Author strawberry's per-variety resistance matrix

Same contract as Task 7, for the 9 strawberry varieties.

**Files:**
- Create: `tools/staging/strawberry_resistance_content.json`
- Create: `tools/staging/strawberry_resistance_sources.md`

**Notes:**
- The classic axis is `red-stele` + `verticillium-wilt` (already in-notes: Earliglow/Allstar resistant; Honeoye "little disease resistance" → a documented-low case). `gray-mold`/`anthracnose`/`powdery-mildew` per-variety data is thinner → grades will be sparse (honest absence, not fabricated).
- Include Honeoye as a documented-weak/susceptible case; keep at least one variety with `resistance` absent if no data exists.

- [ ] **Step 1:** Gather T1-documented grades (Cornell, UMN, `umd_ext`, `osu_ext` berry pages); record provenance.
- [ ] **Step 2:** Write `strawberry_resistance_content.json`.
- [ ] **Step 3: Independent T1-fidelity review** (fresh subagent). Fix; re-review until clean.
- [ ] **Step 4: Commit** the staging file (staged; do NOT push).

---

## Task 9: Build the promote patch + dry-run on a scratch copy

Deterministic builder assembles one SHA-guarded atomic splice from the canonical + the staging content, then applies it to a SCRATCH copy (never the canonical).

**Files:**
- Create: `tools/build_variety_resistance_promote.py` (model on `tools/build_apple_varieties_patch.py` + `tools/build_berry_pilot_patch.py`)
- Create: `tools/batches/variety_resistance_promote.json` (the emitted `{base_sha, patches}`)

**Builder behavior:**
1. Load the canonical; compute `base_sha = sha256(file bytes)`.
2. For apple + strawberry: build `replace` patches for `crops[?(@.name=='Apple')].pests`, `.diseases` (from = current arrays, to = the Task 5/6 laddered arrays), and `.varieties.recommended` (to = current variety objects with each variety's `resistance` map merged in from Task 7/8; varieties with no data get no `resistance` key).
3. Add `control_methods` additions (Task 4) as a `replace` on `control_methods` (from = current, to = current + new keys) and any new `source_catalog` entries similarly.
4. Emit the batch JSON. Assert every `resistance` key equals a `id` present in the same crop's rebuilt `pests`/`diseases` (build-time referential self-check) before writing.

- [ ] **Step 1:** Write the builder; run it to emit `tools/batches/variety_resistance_promote.json`.
- [ ] **Step 2: Dry-run on a scratch copy:**

```bash
cp crops_data_final.json /tmp/scratch_vr.json   # use the scratchpad dir
python3 tools/apply_patch.py tools/batches/variety_resistance_promote.json /tmp/scratch_vr.json
```
Expected: applies cleanly (base_sha matches, all `from`-guards match), writes compact.

- [ ] **Step 3: Commit** the builder + batch (staged; do NOT push).

---

## Task 10: Gate the scratch copy (full battery + adversarial RED)

All gating runs on the scratch from Task 9 — the canonical is still untouched.

- [ ] **Step 1: New + extended gates:**
  - `python3 tools/variety_resistance_gate.py /tmp/scratch_vr.json` → 0 violations.
  - `python3 tools/control_ladder_gate.py /tmp/scratch_vr.json` → 0 (incl. the 20 new ladders + vertebrate coherence).
- [ ] **Step 2: Whole-suite:**
  - `python3 tools/whole_crop_gate.py apple /tmp/scratch_vr.json` → 18/18.
  - `python3 tools/whole_crop_gate.py strawberry /tmp/scratch_vr.json` → 18/18.
  - `python3 tools/gate_all.py /tmp/scratch_vr.json` → 119/119.
  - `python3 tools/register_completeness_gate.py /tmp/scratch_vr.json` → 0 unruled.
- [ ] **Step 3: Adversarial RED on the scratch** (inject each defect into a copy of the scratch, confirm the matching gate bounces, discard the copy): dangling `resistance` id; invalid grade; an insecticide rung on a `fungal` disease; a conventional-before-cultural ladder; a bird problem with an insecticide rung. Document in `docs/reviews/notes/2026-07-23/variety_resistance_red_proof.md`.
- [ ] **Step 4: Footprint audit** (scratch vs canonical): a Python byte-diff proving ONLY apple/strawberry `pests`/`diseases`/`varieties` + `control_methods`/`source_catalog` changed; all other crops byte-identical; `total_crops` still 128; canonical COMPACT (0 escaped-unicode: assert `\\u` count is 0). Record the diff summary in the notes.
- [ ] **Step 5: Consumer sweep** on the new copy: 0 em-dash, 0 ` -- `, 0 spelled-out degrees in the new consumer strings; 0 "lady beetle".
- [ ] **Step 6: `release_verify`** against the scratch; expect clean bar the documented multi-crop single-crop-pilot false positive.

---

## Task 11: Real apply + full release verification

Only now does the canonical change. **This is the first canonical write; it needs Trevor's OK to commit (per Global Constraints).**

- [ ] **Step 1: Re-stamp base_sha** immediately before applying (drift guard): recompute `sha256(crops_data_final.json)`; if it differs from the batch's `base_sha`, re-run Task 9's builder against the current canonical first.
- [ ] **Step 2: Apply to the canonical:** `python3 tools/apply_patch.py tools/batches/variety_resistance_promote.json crops_data_final.json`
- [ ] **Step 3: Prove byte-parity with the scratch:** `shasum -a 256 crops_data_final.json /tmp/scratch_vr.json` → the real apply must produce the SAME hash as the Task 9 scratch (no hidden nondeterminism).
- [ ] **Step 4: Re-run the release battery on the canonical:** `gate_all` 119/119, `variety_resistance_gate` 0, `control_ladder_gate` 0, `whole_crop_gate apple`/`strawberry` 18/18, `register_completeness_gate` 0, `release_verify` clean (bar the documented artifact).
- [ ] **Step 5: Update `LATEST.txt`** (new SHA + session line) — but do NOT commit until Trevor's go.

---

## Task 12: Register row 24 + state trio + commit (Trevor-gated)

- [ ] **Step 1:** Add **row 24** to `docs/field_addition_register.md` (per-variety `resistance` field; trigger conditions; provenance; pilot = apple+strawberry; rollout later), following the row-23 format.
- [ ] **Step 2: State trio:** regenerate/hand-maintain `CURRENT_STATE.md` (per [[current-state-md-drift]], surgical — do NOT run a naive `gen_current_state` regen), append `STATE_HISTORY.md` (most-recent-first), bump `LATEST.txt`.
- [ ] **Step 3:** Summarize the diff for Trevor (what changed, gate results, footprint). **Await Trevor's OK.**
- [ ] **Step 4 (on Trevor's go):** hardened commit — `git status --porcelain` first; `git add` explicit paths only; pathspec-scoped `git commit <paths>`; `git show --stat HEAD` after. NO push, NO plant-astro bump unless Trevor directs.

---

## Out of scope (later sessions)
Roster-wide `resistance` rollout; the A39/gate_all hard-flip; plant-astro TreeGuide `control_ladder` render + resistance consumption; plant-app resistance UI (handoff note owed, separate lane). The deferred strawberry taxonomy tidy ([[strawberry-berry-taxonomy-note]]) picks up AFTER this pilot ships strawberry.

---

## Self-review (against the spec)
- Spec §3 full-crop migration (20 ladders, blob retirement, catalog growth, vertebrate gate, tree-guide handoff) → Tasks 1, 4, 5, 6, 9. ✔
- Spec §4 resistance field (map shape, grade enum, referential, N/A honesty, T1 sourcing, prose coexistence) → Tasks 2, 7, 8. ✔
- Spec §5 gate (soft/scoped/TDD/3 defenses + RED + register ruling) → Tasks 2, 3, 10. ✔
- Spec §6 pilot scope (apple+strawberry, susceptible + N/A cases, row 24) → Tasks 7, 8, 12. ✔
- Spec §7 verification (gate_all, new gate, RED, footprint, consumer sweep, release_verify, two reviews) → Tasks 10, 11 + review steps in 4–8. ✔
- Spec §8 risks (thin strawberry data → sparse honest grades; grade-mapping judgment) → Task 8 notes + Task 7/8 fidelity reviews. ✔
