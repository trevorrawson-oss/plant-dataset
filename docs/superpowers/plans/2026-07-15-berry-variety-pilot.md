# Berry Variety Pilot (strawberry) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `berry` bearing-habit variety archetype (the 5th), pilot it on strawberry (9 varieties), and establish the per-variety `hero_description` common-core standard with the 4 prior pilots backfilled -- all amend-not-recert, gate-clean.

**Architecture:** Extend the existing archetype-dispatch `variety_detail_gate` with a `berry` block whose `bearing_habit` enum sub-dispatches on a crop-level `berry_group ∈ {strawberry, cane, bush}` (strawberry live; cane/bush designed + RED-tested + reserved). Add `hero_description` to the universal common-core. Author strawberry's varieties + backfill the 33 prior-pilot varieties into one SHA-guarded compact splice. Gate stays SOFT/standalone (not wired into A39).

**Tech Stack:** Python 3 standalone gates (no pytest; assert-style test files), `tools/apply_patch.py` (SHA-guarded JSONPath splicer), compact JSON canonical.

## Global Constraints

- Canonical `crops_data_final.json` is **COMPACT**: `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=`. Never reformat it.
- Canonical is **READ-ONLY** until the explicit promote task (Task 7). All authoring happens in scratch copies / batch JSON.
- **No em dashes** in any consumer-facing string (notes, `hero_description`). Use commas/colons/semicolons/periods. American English. Temps render `°F`.
- Per-variety `sources` are **T1-ONLY** (cert gate E source-tier). Honesty about weaker data lives in `confidence_tier` + prose.
- Gate is **SOFT/standalone** -- NOT wired into `whole_crop_gate`/A39 this arc.
- Base canonical **`8dd4ac4c`**; re-stamp `base_sha` from the live canonical at build time (the splice fails closed on drift).
- **Trevor approves every commit and every promote/push.** Tool/test commits (Tasks 1-2, 6 builder) are code; the canonical promote (Task 7) is the gated content change.
- Field-addition register **row 18**.

---

### Task 1: Extend `variety_detail_gate.py` with the `berry` archetype + `hero_description` common-core

**Files:**
- Modify: `tools/variety_detail_gate.py`
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: existing `archetype()`, `_variety_objs()`, `in_scope()`, `_int()`, `variety_violations()`.
- Produces: `berry` archetype dispatch; `berry_group(crop) -> str|None`; `_berry_checks(slug, nm, x, group) -> list[str]`; `COMMON_CORE` now includes `"hero_description"`.

- [ ] **Step 1: Write failing tests for the berry block + hero_description**

Add to `tools/test_variety_detail_gate.py` (after the existing tree/hardiness fixtures):

```python
def bvar(**over):
    v = {"id": "albion", "name": "Albion", "maturity_class": "early",
         "confidence_tier": "T1", "hero_description": "The day-neutral standard, sweet berries all season.",
         "note_beginner": "b", "note_seasoned": "s", "sources": ["ucanr_ext_8256"],
         "bearing_habit": "day_neutral", "use": "fresh", "is_reference": True}
    v.update(over)
    return v

def bcrop(varieties, group="strawberry", slug="strawberry"):
    return {"slug": slug, "days_to_maturity": [], "variety_archetype": "berry",
            "berry_group": group, "varieties": {"recommended": varieties}}

_honeoye = bvar(id="honeoye", name="Honeoye", bearing_habit="june_bearing", is_reference=False)

# clean strawberry crop -> no violations
BCLEAN = bcrop([bvar(), _honeoye])
assert variety_violations(BCLEAN) == [], variety_violations(BCLEAN)
assert variety_warnings(BCLEAN) == [], variety_warnings(BCLEAN)

# bad bearing_habit for the strawberry group (a cane value) bounces
assert any("bearing_habit" in v for v in variety_violations(
    bcrop([bvar(), _honeoye, bvar(id="x", name="X", bearing_habit="summer_bearing", is_reference=False)])))

# missing hero_description bounces (new common-core)
_no_hero = bvar(id="nh", name="NH", is_reference=False); _no_hero.pop("hero_description")
assert any("hero_description" in v for v in variety_violations(bcrop([bvar(), _no_hero])))

# chill_hours_required is NOT allowed under berry_group strawberry
assert any("chill_hours_required" in v for v in variety_violations(
    bcrop([bvar(chill_hours_required=800), _honeoye])))

# reserved cane group accepts a cane habit + chill (designed, RED-proven)
CANEOK = bcrop([bvar(id="boyne", name="Boyne", bearing_habit="summer_bearing",
                     chill_hours_required=800, is_reference=True)], group="cane", slug="raspberry")
assert variety_violations(CANEOK) == [], variety_violations(CANEOK)

# invalid berry_group bounces
assert any("berry_group" in v for v in variety_violations(bcrop([bvar()], group="vine")))
```

Also add `"hero_description"` to the module-level `REQUIRED` tuple and add `hero_description="h"` to the existing `variety()` and `tvar()` factories (dry-bean/apple fixtures) so the pre-existing CLEAN asserts stay green once hero_description is common-core.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL (AssertionError -- berry archetype not handled; `hero_description` not required).

- [ ] **Step 3: Implement the berry archetype + hero_description common-core**

In `tools/variety_detail_gate.py`, add the berry enums/traits near the other archetype blocks:

```python
# berry archetype (strawberry/cane/bush, sub-dispatched by crop-level berry_group)
STRAWBERRY_HABIT = {"june_bearing", "everbearing", "day_neutral"}
CANE_HABIT = {"summer_bearing", "fall_bearing"}                                    # RESERVED (0 live)
BUSH_HABIT = {"northern_highbush", "southern_highbush", "rabbiteye", "half_high"}  # RESERVED (0 live)
BERRY_GROUP_HABIT = {"strawberry": STRAWBERRY_HABIT, "cane": CANE_HABIT, "bush": BUSH_HABIT}
BERRY_GROUPS_WITH_CHILL = {"cane", "bush"}
BERRY_TRAITS = ("bearing_habit", "use")
```

Add `"hero_description"` to `COMMON_CORE`:

```python
COMMON_CORE = ("id", "name", "maturity_class", "confidence_tier",
               "hero_description", "note_beginner", "note_seasoned", "sources")
```

Register the archetype in the dispatch maps + `archetype()` (berry has an empty static ENUMS entry -- `bearing_habit` is validated dynamically against berry_group in `_berry_checks`):

```python
ARCHETYPE_TRAITS = {"annual_dtm": ANNUAL_TRAITS, "photoperiod_annual": PHOTOPERIOD_TRAITS,
                    "hardiness_annual": HARDINESS_TRAITS, "tree_fruit": TREE_TRAITS,
                    "berry": BERRY_TRAITS}
ARCHETYPE_ENUMS = {"annual_dtm": ANNUAL_ENUMS, "photoperiod_annual": PHOTOPERIOD_ENUMS,
                   "hardiness_annual": HARDINESS_ENUMS, "tree_fruit": TREE_ENUMS,
                   "berry": ()}
```

```python
def archetype(crop):
    a = crop.get("variety_archetype")
    return a if a in ("annual_dtm", "photoperiod_annual", "hardiness_annual", "tree_fruit", "berry") else "annual_dtm"


def berry_group(crop):
    return crop.get("berry_group")
```

Add the berry checker (beside `_tree_checks`/`_hardiness_checks`):

```python
def _berry_checks(slug, nm, x, group):
    """Berry block: bearing_habit must match the crop's berry_group vocabulary; chill_hours_required is
    a cane/bush field (positive int) and is REJECTED under berry_group strawberry (strawberry has no chill)."""
    V = []
    valid = BERRY_GROUP_HABIT.get(group, set())
    habit = x.get("bearing_habit")
    if habit not in valid:
        V.append(f"{slug}/{nm}: bearing_habit {habit!r} not in {sorted(valid)} for berry_group {group!r}")
    chill = x.get("chill_hours_required")
    if group in BERRY_GROUPS_WITH_CHILL:
        if chill is not None and (not _int(chill) or chill <= 0):
            V.append(f"{slug}/{nm}: chill_hours_required {chill!r} must be a positive int")
    elif chill is not None:
        V.append(f"{slug}/{nm}: chill_hours_required not allowed for berry_group {group!r} (no chill)")
    return V
```

In `variety_violations`, after the archetype-specific dispatch block, add the berry branch and a crop-level `berry_group` validity check. Berry is season-only, so it is NOT added to `DTM_ARCHETYPES`. Insert alongside the existing `if arch == "tree_fruit"` / `elif arch == "hardiness_annual"` chain:

```python
        elif arch == "berry":
            V += _berry_checks(slug, nm, x, berry_group(crop))
```

and once per crop (after the loop, near the `ref_count`/`dupes` checks):

```python
    if arch == "berry" and berry_group(crop) not in ("strawberry", "cane", "bush"):
        V.append(f"{slug}: berry_group {berry_group(crop)!r} not in ['bush', 'cane', 'strawberry']")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS (all asserts, incl. the pre-existing dry-bean/apple/onion/leek fixtures now carrying `hero_description`).

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "feat(variety-gate): add berry archetype (berry_group dispatch) + hero_description common-core"
```

---

### Task 2: `register_completeness` ruling for the 3 new keys

**Files:**
- Modify: `tools/register_completeness_gate.py`
- Test: `tools/test_register_completeness_gate.py`

**Interfaces:**
- Consumes: `EXCLUDED_KEYS` set, `ruled_categorical(pat, k)`.
- Produces: `bearing_habit`, `berry_group` ruled globally; `hero_description` ruled path-scoped to `varieties.recommended`.

- [ ] **Step 1: Write failing tests**

Add to `tools/test_register_completeness_gate.py` (match the file's existing assert style):

```python
from register_completeness_gate import _is_ruled
# berry enum tokens ruled globally (siblings of cold_hardiness_class / day_length_type / variety_archetype)
assert _is_ruled("$.crops[?(@.slug=='strawberry')].varieties.recommended[0].bearing_habit", "bearing_habit")
assert _is_ruled("$.crops[?(@.slug=='strawberry')].berry_group", "berry_group")
# hero_description ruled path-scoped to varieties.recommended (single-register marquee, analog of pet_safe.note)
assert _is_ruled("$.crops[?(@.slug=='strawberry')].varieties.recommended[0].hero_description", "hero_description")
# NOT ruled elsewhere (guard the path scope)
assert not _is_ruled("$.crops[?(@.slug=='strawberry')].hero_description", "hero_description")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: FAIL (AssertionError on the new asserts).

- [ ] **Step 3: Implement the rulings**

In `tools/register_completeness_gate.py`, add `"bearing_habit"` and `"berry_group"` to `EXCLUDED_KEYS` with a comment (alongside `cold_hardiness_class` at line 86):

```python
    "bearing_habit",  # berry archetype (berry variety pilot 2026-07-15): per-variety bearing-habit/group enum (june_bearing|day_neutral|... ) read by variety_detail_gate; structural token, sibling of day_length_type/cold_hardiness_class
    "berry_group",    # berry archetype (2026-07-15): crop-level berry sub-discriminator enum (strawberry|cane|bush), sibling of variety_archetype
```

Add the `hero_description` clause to `ruled_categorical` (path-scoped, beside the `self_fruitful` clause):

```python
    if k == "hero_description" and "varieties.recommended" in pat:
        return True  # berry variety pilot (Trevor 2026-07-15): the single-register per-variety MARQUEE hero
        # line -- one form read identically by both registers (the variety analog of the ruled pet_safe.note /
        # saucer_practice single-register consumer lines), additive above the dual-register note_beginner/
        # note_seasoned detail. Path-scoped to varieties.recommended; not a categorical token, an intentional
        # single-register hero. Standing common-core going forward (backfilled onto the 4 prior pilots).
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/register_completeness_gate.py tools/test_register_completeness_gate.py
git commit -m "feat(register): rule bearing_habit/berry_group + hero_description (berry variety pilot)"
```

---

### Task 3: Recorded adversarial RED proof on real strawberry shape

**Files:**
- Create: `docs/reviews/notes/2026-07-15/berry_strawberry_red_proof.md`
- (scratch only; canonical READ-ONLY)

**Interfaces:**
- Consumes: `variety_detail_gate.variety_violations`, real strawberry crop object.

- [ ] **Step 1: Build a scratch strawberry-on-berry-schema fixture + prove green**

Write a throwaway script (in the scratchpad, not committed) that loads the real canonical, takes the strawberry crop, rewrites its `varieties.recommended` to the flat berry schema (all 9 varieties with `bearing_habit`/`maturity_class`/`use`/`hero_description`/notes/T1 sources, one `is_reference`), sets `variety_archetype:"berry"` + `berry_group:"strawberry"`, and asserts `variety_violations(strawberry) == []`.

- [ ] **Step 2: Inject each defect class and confirm it bounces**

For each of these, mutate the green scratch strawberry and assert `variety_violations` is non-empty with the expected substring; record PASS/FAIL in the proof doc:
1. `bearing_habit="summer_bearing"` (a cane value under strawberry group) -> "bearing_habit"
2. drop `hero_description` on one variety -> "hero_description"
3. `maturity_class="everbearing"` (bad enum) -> "maturity_class"
4. two varieties `is_reference:true` -> "exactly one"
5. duplicate `id` -> "duplicate variety id"
6. `chill_hours_required:800` under strawberry group -> "chill_hours_required not allowed"
7. `berry_group:"vine"` -> "berry_group"
8. a reserved cane crop (`berry_group:"cane"`) with a strawberry habit -> "bearing_habit ... for berry_group 'cane'"

- [ ] **Step 3: Record the proof + commit the note**

Write `docs/reviews/notes/2026-07-15/berry_strawberry_red_proof.md` with the 8 defect classes, the expected substring, and the observed result (all bounce; canonical SHA unchanged; working tree clean).

```bash
git add docs/reviews/notes/2026-07-15/berry_strawberry_red_proof.md
git commit -m "test(berry): adversarial RED proof -- 8 defect classes bounce on real strawberry shape"
```

---

### Task 4: Author strawberry's 9 varieties (flat berry schema)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/strawberry_variety_sourcing.md` (the per-variety source table)
- (variety objects staged for the Task 6 batch; canonical READ-ONLY)

**Interfaces:**
- Produces: 9 strawberry variety objects on the berry schema, consumed by the Task 6 builder.

**Known facts (from the current legacy varieties -- do not re-derive the type):**

| name | bearing_habit | maturity_class (onset) | use (existing) |
|---|---|---|---|
| Honeoye | june_bearing | early | fresh, freezing, jam |
| Earliglow | june_bearing | early | fresh, jam |
| Jewel | june_bearing | mid | fresh, freezing |
| Allstar | june_bearing | mid | fresh |
| Albion | day_neutral | early | fresh |
| Seascape | day_neutral | early | fresh, freezing |
| Tristar | day_neutral | early | fresh |
| Ozark Beauty | everbearing | early | fresh, jam |
| Quinault | everbearing | early | fresh |

- [ ] **Step 1: Author each variety object** to this exact shape (dual-register notes preserved from the existing `recommended_note`, tightened per register; single-register `hero_description` marquee hook; `id` = slugified name):

```json
{"id":"albion","name":"Albion","bearing_habit":"day_neutral","maturity_class":"early",
 "use":"fresh","is_reference":true,"confidence_tier":"T1",
 "hero_description":"The day-neutral benchmark: firm, sweet berries from summer into fall.",
 "note_beginner":"...","note_seasoned":"...",
 "sources":["ucanr_ext_8256","umd_ext"],"anchoring_urls":{...}}
```

Rules: `maturity_class` = ripening ONSET (per the table); `hero_description` a single crisp marquee line (a hook, NOT a restatement of the note), no em dashes, `°F` if any temp; per-variety `sources` T1-ONLY, drawn from the strawberry `source_set` already present (`cornell_ext`, `umd_ext`, `umn_ext`, `ucanr_ext_8256`, `uf_ifas_hs403`, `osu_ext`, `usu_ext`, `uc_ipm`); `is_reference:true` on **Albion only** (widely adaptable day-neutral, the "good first choice"); optional `regional_fit` only where genuinely warranted (a short-day southern/annual-system type -- none of these 9 clearly require it, so default absent).

- [ ] **Step 2: Record the sourcing table** in `docs/reviews/notes/2026-07-15/strawberry_variety_sourcing.md` (variety -> bearing_habit + maturity_class -> T1 source id + URL + confidence_tier). Confirm 0 non-T1 per-variety sources.

- [ ] **Step 3: Self-check** each variety object against the Task-1 gate on a scratch crop: `variety_violations` == [] with these 9. (No commit -- staged for Task 6.)

---

### Task 5: Author the `hero_description` backfill for the 4 prior pilots (33 varieties)

**Files:**
- (variety hero lines staged for the Task 6 batch; canonical READ-ONLY)

**Interfaces:**
- Produces: one `hero_description` string per variety for dry-bean (5), apple (16), onion (6), leek (6).

- [ ] **Step 1: Author one marquee `hero_description` per variety** for all 33, distilled from each variety's EXISTING `note_beginner`/`note_seasoned` (a hook, not a restatement; no new sourcing needed -- the hero is a distillation of already-sourced content). No em dashes; American English; `°F` where a temp appears. Example (dry-bean/Black Turtle): `"The classic black bean, an Americas heirloom that holds its shape in the pot."`

- [ ] **Step 2: Self-check** on scratch: after adding these hero lines, `variety_violations` == [] for dry-bean/apple/onion/leek (they now satisfy the new common-core field). (No commit -- staged for Task 6.)

---

### Task 6: Build the SHA-guarded batch + scratch apply + footprint audit + release battery

**Files:**
- Create: `tools/build_berry_pilot_patch.py`
- Create: `tools/batches/berry_strawberry_pilot.json` (generated)
- Test: `tools/test_build_berry_pilot_patch.py`

**Interfaces:**
- Consumes: the Task 4 strawberry objects + Task 5 hero lines; `tools/apply_patch.py`.
- Produces: one atomic batch (strawberry berry-schema + 33 hero adds) + a footprint the battery verifies.

- [ ] **Step 1: Write the builder** `tools/build_berry_pilot_patch.py` that loads the live canonical, re-stamps `base_sha`, and emits ops: for strawberry -- `add variety_archetype`, `add berry_group`, `replace varieties.recommended`, and `replace verification_status.source_set` only if a source id is genuinely added; for each of the 33 prior-pilot varieties -- `add $.crops[?(@.slug=='<crop>')].varieties.recommended[?(@.id=='<id>')].hero_description`. Compute all `from`/`value` from the loaded canonical so guards cannot drift (the `build_variety_descriptions_patch.py` pattern). Assert no em dash enters any authored string.

- [ ] **Step 2: Write + run a builder test** (`tools/test_build_berry_pilot_patch.py`): the emitted batch has a `base_sha` matching the live canonical, exactly the expected op count (strawberry ops + 33 hero adds), and every `hero_description` value is dash-free. Run: `python3 tools/test_build_berry_pilot_patch.py` -> PASS.

- [ ] **Step 3: Generate the batch + apply to a SCRATCH copy**

```bash
cp crops_data_final.json /tmp/berry_scratch.json
python3 tools/build_berry_pilot_patch.py > tools/batches/berry_strawberry_pilot.json
python3 tools/apply_patch.py tools/batches/berry_strawberry_pilot.json --base /tmp/berry_scratch.json --out /tmp/berry_candidate.json
```
Expected: apply reports footprint = strawberry + dry-bean/apple/onion/leek `varieties` only; top-level unchanged (or `source_catalog` +N iff a source was added); count 125.

- [ ] **Step 4: Footprint audit + full release battery on the CANDIDATE** (`/tmp/berry_candidate.json`):

```bash
python3 tools/variety_detail_gate.py /tmp/berry_candidate.json --warnings --coverage         # strawberry in scope; 0 viol / 0 warn
python3 tools/whole_crop_gate.py strawberry /tmp/berry_candidate.json                        # PASS (positional slug, not --slug)
python3 tools/gate_all.py /tmp/berry_candidate.json                                          # 116/116
python3 tools/register_completeness_gate.py /tmp/berry_candidate.json                        # A25 = 0 unruled
python3 tools/release_verify.py /tmp/berry_candidate.json --base crops_data_final.json --slug strawberry  # section A footprint = the 5 crops; B "no new violations"; D 0 dashes
```
Plus a byte-diff footprint check: exactly strawberry + the 4 pilots changed; all 120 other crops byte-identical; compact (no trailing newline); count 125. Fix authoring/builder and re-run until green.

- [ ] **Step 5: Commit the tooling** (NOT the canonical):

```bash
git add tools/build_berry_pilot_patch.py tools/test_build_berry_pilot_patch.py tools/batches/berry_strawberry_pilot.json docs/reviews/notes/2026-07-15/strawberry_variety_sourcing.md
git commit -m "build(berry): strawberry pilot patch builder + generated batch + sourcing table"
```

---

### Task 7: Promote (Trevor-gated) + field register row + state trio

**Files:**
- Modify: `crops_data_final.json` (the ONE promote), `LATEST.txt`, `CURRENT_STATE.md`, `STATE_HISTORY.md`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: `tools/batches/berry_strawberry_pilot.json`.

- [ ] **Step 1: STOP -- get Trevor's explicit go** for the promote (canonical content change). Do not proceed without it.

- [ ] **Step 2: Apply the batch to the real canonical** (re-stamp `base_sha` from the live SHA first; the guard fails closed on drift):

```bash
python3 tools/apply_patch.py tools/batches/berry_strawberry_pilot.json --base crops_data_final.json --out crops_data_final.json
shasum -a 256 crops_data_final.json
```

- [ ] **Step 3: Re-run the full battery on the promoted canonical** (all green, same commands as Task 6 Step 4 but against `crops_data_final.json`): `variety_detail_gate` 0/0, `whole_crop_gate.py strawberry crops_data_final.json` PASS, `gate_all` 116/116, `register_completeness` A25=0, `release_verify` clean. Confirm compact + count 125 + strawberry/4-pilots still certified.

- [ ] **Step 4: Field-addition register row 18** in `docs/field_addition_register.md` (the `berry` archetype + `hero_description` common-core; HARD-FLIP INV-1 = the Spec-2 rollout trigger, mirror the row-13/14/16 wording).

- [ ] **Step 5: State trio** -- regenerate `CURRENT_STATE.md` surgically (NO `gen_current_state` regen -- it corrupts the no-separator file; hand-edit the top entry), append `STATE_HISTORY.md` (most-recent-first), bump `LATEST.txt` (new SHA + session). Record: canonical `8dd4ac4c -> <new>`, 5th archetype, strawberry pilot, hero_description common-core + 33-variety backfill, gate soft/standalone, committed-unpushed, no plant-astro bump this session.

- [ ] **Step 6: Commit the promote** (Trevor-gated; single content commit):

```bash
git add crops_data_final.json docs/field_addition_register.md CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "feat(berry): strawberry variety pilot (5th archetype) + hero_description common-core + 33-variety backfill"
```

Push + plant-astro bump + plant-app INV-2 consumption are separate, Trevor-gated follow-ons (NOT this arc).

---

## Self-Review

**Spec coverage** (each spec section -> task):
- §4 berry archetype + berry_group -> Task 1. §5 schema (common core + berry block, maturity_class onset, reserved cane/bush) -> Task 1 + Task 4. §6 shape-only gate + TDD RED -> Task 1 + Task 3. §7 hero_description common-core + bundled backfill -> Task 1 (common-core) + Task 5 (backfill) + Task 6 (splice). §8 register ruling -> Task 2. §9 sourcing + flagship -> Task 4. §10 footprint + battery -> Task 6 + Task 7. §11 register row 18 -> Task 7. §12 scope-out (no honesty engine, no cane/bush population, no A39 flip) -> honored (Task 1 leaves cane/bush reserved; no engine built). §13 success criteria -> Task 6/7 battery. §14 open items (flagship=Albion, hero voice, regional_fit) -> resolved in Task 4.
- No gaps.

**Placeholder scan:** the `note_beginner/seasoned` and `hero_description` string VALUES in Tasks 4-5 are authored content (the deliverable), not code placeholders -- their shape, rules, and sources are fully specified. No "TBD"/"add error handling"/"similar to Task N".

**Type consistency:** `berry_group` (crop-level) / `bearing_habit` (per-variety) / `hero_description` (per-variety) used identically across Tasks 1, 2, 4, 6. `_berry_checks(slug, nm, x, group)` signature matches its call site. `BERRY_GROUP_HABIT` keys `{strawberry, cane, bush}` match the `archetype()`/`berry_group` validity check and the register `berry_group` ruling. `COMMON_CORE` + `hero_description` consistent between gate (Task 1) and register ruling (Task 2).
