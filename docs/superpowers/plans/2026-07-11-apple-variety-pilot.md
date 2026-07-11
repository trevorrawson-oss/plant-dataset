# Apple Variety Pilot (Tree Archetype) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the bean-hardwired `variety_detail_gate` into an archetype-dispatched gate, add the tree-fruit block + honesty fields, and enrich apple's varieties (the 13 + 2 triploids + 1 crabapple) to the flat per-variety schema so the app can compute an honest per-region cross-pollination calendar.

**Architecture:** The per-variety schema splits into a universal common core plus one archetype block selected by a crop-level `variety_archetype` key (absent defaults to `annual_dtm`, so dry-bean is byte-untouched; apple declares `tree_fruit`). The gate dispatches required fields, enums, and coherence checks on that key. Content ships via a SHA-guarded COMPACT splice mirroring the dry-bean patch builder, gated by the full release battery, with a Trevor source-manifest sign-off for any non-T1 datapoint before the splice.

**Tech Stack:** Python 3 (stdlib only), flat assert-based test files (run directly, not pytest), the repo's existing gate + `apply_patch` tooling.

**Spec:** `docs/superpowers/specs/2026-07-11-apple-variety-pilot-design.md`

## Global Constraints

- **Canonical JSON is COMPACT:** `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 7 (the authoring/promote splice). Tasks 1-5 touch only tooling + tests + a scratch copy.
- **TDD: RED before GREEN.** Every gate change gets a failing test first; the tree-block gate is adversarially proven on a scratch copy of real canonical (Task 5) before the content is trusted.
- **No em dashes in consumer copy** (variety prose): use commas/colons/semicolons/periods. `--` is fine in code/docs/commits. American English. Temps render as `°F`. "plant" lowercase except sentence start / "Plant Pro".
- **T1-or-it-does-not-ship** for load-bearing honesty numbers (per-variety `chill_hours_required` + `bloom_group`, region bloom anchors). Non-T1 -> Trevor manifest sign-off before the splice (Task 6). No silent drops or downgrades.
- **Release verification before any promote** (protocol #6): `whole_crop_gate` apple + `gate_all` (whole suite, every certified crop) + `release_verify` + `variety_detail_gate` + per-batch `source_truth_sample`.
- **State trio at release:** CURRENT_STATE.md (patch surgically -- it has no `---` separator, a naive regen corrupts it), STATE_HISTORY.md (prepend, most-recent first), LATEST.txt (SHA + session).
- **Canonical count stays 125.** Batch 1 adds 3 *varieties inside apple*, not crops. Footprint = apple's `varieties` object + apple's new `variety_archetype` key; all 124 other crops byte-identical.
- **No plant-astro submodule bump from this session** (owned by the plant-astro session). Trevor confirms every push.

---

## File Structure

- `tools/variety_detail_gate.py` (modify) -- add `variety_archetype` dispatch; split `REQUIRED` into common core + annual/tree blocks; add tree-block validators + tree coherence.
- `tools/test_variety_detail_gate.py` (modify) -- keep all annual (dry-bean) asserts green; add tree-archetype fixture + tree defect asserts.
- `tools/register_completeness_gate.py` (modify) -- rule `bloom_group` + `self_fruitful` scoped to `varieties.recommended`.
- `tools/test_register_completeness_gate.py` (modify) -- regression assert the two new keys are ruled.
- `tools/build_apple_varieties_patch.py` (create) -- emit the SHA-guarded COMPACT patch (mirror `build_dry_bean_varieties_patch.py`).
- `tools/batches/apple_varieties_pilot.json` (create, generated) -- the patch file.
- `docs/field_addition_register.md` (modify) -- tree-variety bundle row with the INV-1 hard-flip trigger.
- `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (modify at release).

---

## Task 1: Gate -- `variety_archetype` dispatch + common-core / archetype-block split

**Files:**
- Modify: `tools/variety_detail_gate.py`
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: existing `_variety_objs(crop)`, `in_scope(crop)`, `dtm_empty(crop)` (from `timing_spine_gate`).
- Produces: `archetype(crop) -> "annual_dtm" | "tree_fruit"`; `variety_violations(crop)` now dispatches required fields + enums on archetype. Annual behavior is unchanged (all existing asserts stay green).

- [ ] **Step 1: Write the failing test — a tree crop with only the annual fields must now fail on missing tree fields, and the annual (dry-bean) fixture must stay clean.**

Add to `tools/test_variety_detail_gate.py` (after the existing `CLEAN` block):

```python
from variety_detail_gate import archetype

def tvar(**over):
    v = {"id": "golden-delicious", "name": "Golden Delicious", "maturity_class": "mid",
         "is_reference": True, "confidence_tier": "T1", "note_beginner": "b", "note_seasoned": "s",
         "sources": ["umn_ext"], "bloom_group": "mid", "bloom_window_relative": [0.42, 0.6],
         "bloom_duration_days": 10, "chill_hours_required": 700, "use": "fresh eating", "triploid": False}
    v.update(over)
    return v

def tcrop(varieties, slug="apple"):
    return {"slug": slug, "variety_archetype": "tree_fruit", "days_to_maturity": [],
            "varieties": {"recommended": varieties}}

_mcintosh = tvar(id="mcintosh", name="McIntosh", bloom_group="early",
                 bloom_window_relative=[0.2, 0.36], chill_hours_required=900,
                 use="fresh eating, sauce", is_reference=False)

# archetype dispatch
assert archetype(tcrop([tvar()])) == "tree_fruit"
assert archetype(CLEAN) == "annual_dtm"          # no variety_archetype key -> default
assert archetype({"slug": "x", "variety_archetype": "bogus", "varieties": {"recommended": []}}) == "annual_dtm"

# a clean tree crop -> no violations
TREE_CLEAN = tcrop([tvar(), _mcintosh])
assert variety_violations(TREE_CLEAN) == [], variety_violations(TREE_CLEAN)

# a tree crop is NOT required to carry the bean traits (they are annual-only now)
assert not any("seed_type" in v or "plant_habit" in v for v in variety_violations(TREE_CLEAN)), variety_violations(TREE_CLEAN)

# a tree crop MISSING a tree-required field -> violation
notree = tvar(); del notree["bloom_group"]
assert any("bloom_group" in v for v in variety_violations(tcrop([notree, _mcintosh])))

# a tree variety does NOT need days_to_maturity (grafted / season-only)
assert not any("days_to_maturity" in v for v in variety_violations(TREE_CLEAN)), variety_violations(TREE_CLEAN)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL -- `archetype` is not importable (ImportError), or the tree fixture reports spurious `seed_type`/`plant_habit` missing violations under the old bean-hardwired `REQUIRED`.

- [ ] **Step 3: Implement the dispatch + block split in `tools/variety_detail_gate.py`**

Replace the enum/`REQUIRED` constants block (currently lines ~26-38) with:

```python
MATURITY_CLASS = {"early", "mid", "late"}
CONFIDENCE = {"T1", "T2", "T3", "T4"}
# annual (dry-bean) archetype
SEED_TYPE = {"open_pollinated", "hybrid", "heirloom"}
SEED_SIZE = {"small", "medium", "large"}
PLANT_HABIT = {"bush", "half_runner", "pole"}
PRIMARY_USE = {"soup", "baked", "chili", "fresh_shell", "multi"}
# tree_fruit (apple) archetype
BLOOM_GROUP = {"very_early", "early", "mid", "late", "very_late"}
SELF_FRUITFUL = {"no", "partial", "yes"}

DTM_FLOOR, DTM_CEIL = 7, 400   # mirrors numeric_sanity A33; the only HARD numeric bound
DTM_MARGIN = 10                # advisory band widening; low-stakes (sourced values never warn)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

COMMON_CORE = ("id", "name", "maturity_class", "confidence_tier",
               "note_beginner", "note_seasoned", "sources")
ANNUAL_TRAITS = ("seed_type", "seed_color", "seed_size", "plant_habit", "primary_use")
TREE_TRAITS = ("bloom_group", "bloom_window_relative", "bloom_duration_days",
               "chill_hours_required", "use")
COMMON_ENUMS = (("maturity_class", MATURITY_CLASS), ("confidence_tier", CONFIDENCE))
ANNUAL_ENUMS = (("seed_type", SEED_TYPE), ("seed_size", SEED_SIZE),
                ("plant_habit", PLANT_HABIT), ("primary_use", PRIMARY_USE))
TREE_ENUMS = (("bloom_group", BLOOM_GROUP),)


def archetype(crop):
    """Crop declares its variety archetype; absence defaults to annual_dtm (dry-bean stays untouched)."""
    a = crop.get("variety_archetype")
    return a if a in ("annual_dtm", "tree_fruit") else "annual_dtm"
```

Then in `variety_violations(crop)`, replace the required-fields + enum loops with the dispatched versions. The function head becomes:

```python
def variety_violations(crop):
    V = []
    if not in_scope(crop):
        return V
    slug = crop.get("slug", "?")
    arch = archetype(crop)
    season_only = dtm_empty(crop)
    required = COMMON_CORE + (TREE_TRAITS if arch == "tree_fruit" else ANNUAL_TRAITS)
    enums = COMMON_ENUMS + (TREE_ENUMS if arch == "tree_fruit" else ANNUAL_ENUMS)
    vars_ = _variety_objs(crop)
    ids, ref_count = [], 0
    for x in vars_:
        nm = x.get("name") or x.get("id") or "?"
        for f in required:
            if f not in x or x[f] in (None, "", []):
                V.append(f"{slug}/{nm}: missing required variety field {f!r}")
        for f, enum in enums:
            if f in x and x[f] not in enum:
                V.append(f"{slug}/{nm}: {f} {x[f]!r} not in {sorted(enum)}")
        vid = x.get("id")
        if isinstance(vid, str):
            if not SLUG_RE.match(vid):
                V.append(f"{slug}/{nm}: id {vid!r} is not slug-shaped")
            ids.append(vid)
        ir = x.get("is_reference")
        if not isinstance(ir, bool):
            V.append(f"{slug}/{nm}: is_reference {ir!r} must be a bool")
        elif ir:
            ref_count += 1
        if arch == "annual_dtm":
            V += _annual_dtm_checks(slug, nm, x, season_only)
        else:
            V += _tree_checks(slug, nm, x)
    if ref_count != 1:
        V.append(f"{slug}: exactly one variety must have is_reference true (found {ref_count})")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        V.append(f"{slug}: duplicate variety id(s) {dupes}")
    return V


def _annual_dtm_checks(slug, nm, x, season_only):
    """days_to_maturity presence/int/[7,400] for the annual archetype (unchanged behavior)."""
    V = []
    dtm = x.get("days_to_maturity")
    if dtm is None:
        if not season_only:
            V.append(f"{slug}/{nm}: days_to_maturity missing (crop is DTM-based)")
    elif not _int(dtm):
        V.append(f"{slug}/{nm}: days_to_maturity {dtm!r} must be an int")
    elif not (DTM_FLOOR <= dtm <= DTM_CEIL):
        V.append(f"{slug}/{nm}: days_to_maturity {dtm} outside [{DTM_FLOOR},{DTM_CEIL}]")
    return V
```

Add a stub `_tree_checks` for now (Task 2 fills it):

```python
def _tree_checks(slug, nm, x):
    """Tree-fruit block validators (bloom/chill/triploid). Filled in Task 2."""
    return []
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS -- `variety_detail_gate tests: OK` (all existing annual asserts + the new archetype asserts).

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "refactor(variety-gate): variety_archetype dispatch + common-core/archetype split (dry-bean unchanged)"
```

---

## Task 2: Gate -- tree-block validators

**Files:**
- Modify: `tools/variety_detail_gate.py` (`_tree_checks`)
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: `_int(x)`, `BLOOM_GROUP`, `SELF_FRUITFUL` from Task 1.
- Produces: `_tree_checks(slug, nm, x) -> [violation strings]` enforcing `bloom_window_relative` shape, `bloom_duration_days`/`chill_hours_required` positive int, `triploid` bool, optional `self_fruitful` enum.

- [ ] **Step 1: Write the failing tests — one defect per tree-block rule**

Add to `tools/test_variety_detail_gate.py`:

```python
# tree-block: bloom_window_relative must be two floats in [0,1] with start < end
for bad in [[0.5], [0.5, 1.2], [0.6, 0.4], [0.6, 0.6], "0.4-0.6"]:
    c = tcrop([tvar(bloom_window_relative=bad), _mcintosh])
    assert any("bloom_window_relative" in v for v in variety_violations(c)), (bad, variety_violations(c))

# tree-block: chill_hours_required + bloom_duration_days must be positive ints
assert any("chill_hours_required" in v for v in variety_violations(tcrop([tvar(chill_hours_required=0), _mcintosh])))
assert any("chill_hours_required" in v for v in variety_violations(tcrop([tvar(chill_hours_required="700"), _mcintosh])))
assert any("bloom_duration_days" in v for v in variety_violations(tcrop([tvar(bloom_duration_days=0), _mcintosh])))

# tree-block: triploid must be a bool
assert any("triploid" in v for v in variety_violations(tcrop([tvar(triploid="yes"), _mcintosh])))

# tree-block: bad bloom_group enum
assert any("bloom_group" in v for v in variety_violations(tcrop([tvar(bloom_group="earlyish"), _mcintosh])))

# tree-block: self_fruitful optional, but if present must be in enum; valid value is clean
assert any("self_fruitful" in v for v in variety_violations(tcrop([tvar(self_fruitful="sometimes"), _mcintosh])))
assert variety_violations(tcrop([tvar(self_fruitful="partial"), _mcintosh])) == [], "valid self_fruitful is clean"

# a triploid variety (real edge case) is clean
assert variety_violations(tcrop([tvar(), tvar(id="mutsu", name="Mutsu", triploid=True, is_reference=False,
                                             bloom_group="mid", bloom_window_relative=[0.44, 0.62],
                                             chill_hours_required=600, use="cooking, fresh eating")])) == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL -- `_tree_checks` returns `[]`, so none of the tree-block defects are caught.

- [ ] **Step 3: Implement `_tree_checks`**

Replace the Task-1 stub:

```python
def _tree_checks(slug, nm, x):
    """Tree-fruit block: bloom-window shape, positive-int chill/duration, triploid bool, self_fruitful enum."""
    V = []
    bwr = x.get("bloom_window_relative")
    if bwr is not None:
        if (not isinstance(bwr, list) or len(bwr) != 2
                or not all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in bwr)
                or not (0.0 <= bwr[0] < bwr[1] <= 1.0)):
            V.append(f"{slug}/{nm}: bloom_window_relative {bwr!r} must be [start,end] floats "
                     f"in [0,1] with start < end")
    for f in ("bloom_duration_days", "chill_hours_required"):
        val = x.get(f)
        if val is not None and (not _int(val) or val <= 0):
            V.append(f"{slug}/{nm}: {f} {val!r} must be a positive int")
    trip = x.get("triploid")
    if not isinstance(trip, bool):
        V.append(f"{slug}/{nm}: triploid {trip!r} must be a bool")
    sf = x.get("self_fruitful")
    if sf is not None and sf not in SELF_FRUITFUL:
        V.append(f"{slug}/{nm}: self_fruitful {sf!r} not in {sorted(SELF_FRUITFUL)}")
    return V
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS -- `variety_detail_gate tests: OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "feat(variety-gate): tree-block validators (bloom window, chill, triploid, self_fruitful)"
```

---

## Task 3: Gate -- tree bloom coherence (advisory warning)

**Files:**
- Modify: `tools/variety_detail_gate.py` (`variety_warnings`)
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: `BLOOM_GROUP`, `archetype`.
- Produces: `variety_warnings(crop)` additionally emits a tree coherence WARNING when `bloom_group` order and `bloom_window_relative` start order disagree. Advisory only (never a violation). Annual warnings unchanged.

- [ ] **Step 1: Write the failing test — a bloom_group/relative-window inversion warns but does not violate**

Add to `tools/test_variety_detail_gate.py`:

```python
# tree coherence: a very_early variety whose start sits ABOVE a late variety's start -> WARNING, not violation
early_hi = tvar(id="dorsett", name="Dorsett", bloom_group="very_early",
                bloom_window_relative=[0.8, 0.95], chill_hours_required=100, is_reference=False)
late_lo = tvar(id="fuji", name="Fuji", bloom_group="late",
               bloom_window_relative=[0.1, 0.25], chill_hours_required=600)
c_incoh = tcrop([late_lo, early_hi])
assert variety_violations(c_incoh) == [], variety_violations(c_incoh)   # shape is valid
assert any("bloom" in w.lower() for w in variety_warnings(c_incoh)), variety_warnings(c_incoh)

# the real monotonic ladder (early low-start .. late high-start) -> no warning
assert variety_warnings(TREE_CLEAN) == [], variety_warnings(TREE_CLEAN)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL -- `variety_warnings` has no tree branch yet, so the inversion produces no warning.

- [ ] **Step 3: Implement the tree branch in `variety_warnings`**

At the top of `variety_warnings(crop)`, after the `in_scope` guard and `slug`/`vars_` setup, dispatch the tree branch; leave the existing annual band + class/DTM warnings under the annual branch:

```python
def variety_warnings(crop):
    W = []
    if not in_scope(crop):
        return W
    slug = crop.get("slug", "?")
    vars_ = _variety_objs(crop)
    if archetype(crop) == "tree_fruit":
        return _tree_warnings(slug, vars_)
    # --- annual archetype (unchanged) ---
    band = crop.get("days_to_maturity")
    ...  # existing band + class/DTM warning code stays exactly as-is
    return W


BLOOM_RANK = {"very_early": 0, "early": 1, "mid": 2, "late": 3, "very_late": 4}


def _tree_warnings(slug, vars_):
    """Advisory: bloom_group ordering must agree with bloom_window_relative start ordering."""
    W = []
    pairs = []
    for x in vars_:
        g = BLOOM_RANK.get(x.get("bloom_group"))
        bwr = x.get("bloom_window_relative")
        if g is not None and isinstance(bwr, list) and len(bwr) == 2:
            pairs.append((x.get("name", "?"), g, bwr[0]))
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            ni, gi, si = pairs[i]
            nj, gj, sj = pairs[j]
            if gi < gj and si > sj:
                W.append(f"{slug}/{ni}: bloom_group '{list(BLOOM_RANK)[gi]}' earlier than "
                         f"{nj} '{list(BLOOM_RANK)[gj]}' but relative start {si} > {sj} (order mismatch)")
    return W
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS -- `variety_detail_gate tests: OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "feat(variety-gate): tree bloom_group/relative-window coherence warning (advisory)"
```

---

## Task 4: register_completeness -- rule `bloom_group` + `self_fruitful`

**Files:**
- Modify: `tools/register_completeness_gate.py` (`ruled_categorical`, near lines 169-176)
- Test: `tools/test_register_completeness_gate.py`

**Interfaces:**
- Consumes: existing `ruled_categorical(pat, k)` predicate.
- Produces: `bloom_group` and `self_fruitful` under `varieties.recommended` return `True` (ruled), so the tree keys do not trip the C11/A25 unruled-string flood.

- [ ] **Step 1: Write the failing regression test**

Add to `tools/test_register_completeness_gate.py`:

```python
from register_completeness_gate import ruled_categorical

# apple tree-variety pilot: bloom_group + self_fruitful are RULED categorical under varieties.recommended
P = "$.crops[?(@.slug=='apple')].varieties.recommended[0]"
assert ruled_categorical(P, "bloom_group"), "bloom_group must be ruled"
assert ruled_categorical(P, "self_fruitful"), "self_fruitful must be ruled"
# guard against over-broad rulings: an unrelated string key stays UNRULED
assert not ruled_categorical(P, "totally_new_prose_key"), "unrelated key must stay unruled"
# path guard: bloom_group outside varieties.recommended is NOT auto-ruled here
assert not ruled_categorical("$.crops[?(@.slug=='apple')].bloom_group", "bloom_group")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: FAIL -- `AssertionError: bloom_group must be ruled` (the key is not yet in `ruled_categorical`).

- [ ] **Step 3: Add the ruling in `register_completeness_gate.py`**

Immediately after the dry-bean block (the `if (k in ("id", "seed_type", ...)` block ending near line 176), add:

```python
    if (k in ("bloom_group", "self_fruitful")
            and "varieties.recommended" in pat):
        return True  # apple tree-variety pilot (Trevor 2026-07-11): tree-archetype categorical labels --
        # bloom_group (very_early..very_late relative bloom class, T1-sourced) + self_fruitful
        # (no/partial/yes override of crop self_fertile). Terse single-form attributes, path-scoped to
        # varieties.recommended, siblings of the already-ruled .use/.note/.hardiness_note + the dry-bean
        # bundle. bloom_window_relative (list) / bloom_duration_days,chill_hours_required (int) / triploid
        # (bool) are non-string, out of A25 scope; note_beginner/note_seasoned auto-rule by suffix.
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/register_completeness_gate.py tools/test_register_completeness_gate.py
git commit -m "feat(register): rule bloom_group + self_fruitful (apple tree-variety pilot)"
```

---

## Task 5: Adversarial RED proof on a scratch copy of real canonical

Prove the tree gate catches real defects *in apple's actual shape* before any content is trusted (the CLAUDE.md "sneak a defect at it" bar). This is a verification task; no production code changes.

**Files:**
- Create (scratch, gitignored/temporary): `/private/tmp/claude-501/.../scratchpad/apple_scratch.json`

- [ ] **Step 1: Build a scratch canonical whose apple already carries a *valid* tree schema, then confirm the gate is green on it**

Write `scratchpad/prove_apple_gate.py` that: loads canonical, finds apple, sets `variety_archetype="tree_fruit"`, and rewrites apple's 13 varieties with a *minimal valid* tree schema (id/name/maturity_class/is_reference[one true]/confidence_tier/notes/sources + bloom_group/bloom_window_relative/bloom_duration_days/chill_hours_required/use/triploid, taken from the real bloom values already in canonical). Dump to `apple_scratch.json` (compact is fine for scratch). Run:

Run: `python3 tools/variety_detail_gate.py scratchpad/apple_scratch.json --warnings`
Expected: `violations=0`; apple now appears in `in_scope` count; no coherence warnings (the real 13 form a monotonic ladder).

- [ ] **Step 2: Inject each defect class into the scratch apple and confirm each bounces**

For each of the following, mutate `apple_scratch.json`'s apple in a throwaway copy and re-run the gate, asserting a non-zero exit + the expected substring:
- `bloom_group` set to `"earlyish"` -> violation mentions `bloom_group`.
- `bloom_window_relative` set to `[0.6, 0.4]` -> violation mentions `bloom_window_relative`.
- `chill_hours_required` set to `0` -> violation mentions `chill_hours_required`.
- `triploid` set to `"yes"` -> violation mentions `triploid`.
- two varieties with `is_reference: true` -> violation mentions `is_reference`.
- a bloom_group/relative-window inversion -> `--warnings` shows the coherence WARNING (advisory, exit still 0 unless other violations).

Encode these as asserts in `scratchpad/prove_apple_gate.py` (subprocess the gate like `test_variety_detail_gate.py::_run` does) so the proof is repeatable.

Run: `python3 scratchpad/prove_apple_gate.py`
Expected: prints `apple tree-gate adversarial proof: OK` (every defect bounced).

- [ ] **Step 3: Record the proof**

No commit (scratch only). Paste the proof output into the Task-7 release notes / STATE_HISTORY entry as the recorded RED evidence. Confirm canonical is still byte-untouched:

Run: `shasum -a 256 crops_data_final.json | cut -d' ' -f1`
Expected: `340c2983...` (unchanged; canonical was never written).

---

## Task 6: Author Batch 1 + source manifest + Trevor sign-off (CHECKPOINT)

**Files:**
- Create: `tools/build_apple_varieties_patch.py` (mirror `tools/build_dry_bean_varieties_patch.py`)
- Produce: a source manifest (markdown table) for Trevor

This task authors content and gathers sourcing; it ends at a human gate. Do NOT splice until Trevor signs off the manifest.

- [ ] **Step 1: Draft the 16 variety objects in the builder**

Copy `build_dry_bean_varieties_patch.py` to `build_apple_varieties_patch.py` and adapt: `CANON`, `OUT="tools/batches/apple_varieties_pilot.json"`, target slug `apple`. Author `VARIETIES` = the 13 existing (carry their current `bloom_group`/`bloom_window_relative`/`bloom_duration_days`/`chill_hours_required`/`use` forward; add `id`, `maturity_class` [ripening season], `is_reference` [Golden Delicious `true`, all others `false`], `confidence_tier`, `triploid: false`, `self_fruitful` only where it differs [`golden-delicious`: `partial`], dual-register `note_beginner`/`note_seasoned`, per-variety `sources`/`anchoring_urls`) + `jonagold` + `mutsu` (`triploid: true`) + `dolgo` (crabapple, long-bloom universal pollinizer). Prose: original, apple voice, dual-register, no em dashes, °F. The patch replaces apple's `varieties` object and adds the crop-level `variety_archetype: "tree_fruit"` key.

The two patch ops (SHA-guarded, mirroring dry-bean):

```python
patch = {"base_sha": sha, "patches": [
    {"op": "add", "json_path": "$.crops[?(@.slug=='apple')].variety_archetype", "value": "tree_fruit"},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='apple')].varieties",
     "from": current_varieties, "value": new_varieties},
]}
```

- [ ] **Step 2: Verify each load-bearing number against a source; classify T1 vs non-T1**

For every variety's `bloom_group` + `chill_hours_required`, and each region's bloom anchor targeted for upgrade, find the source and record its tier. Prefer T1 (university extension / USDA). Region bloom-anchor upgrade targets: WSU, Cornell/NY, Michigan State, Utah State bloom-sequence + chill records. `bloom_window_relative` is DERIVED from `bloom_group` (document the mapping in the builder docstring); it is never listed as "sourced."

- [ ] **Step 3: Produce the source manifest for Trevor (non-T1 only need sign-off)**

Emit a markdown table: `datapoint | variety/region | proposed source id | tier | URL | what it backs`. T1 rows are informational; **every non-T1 row is a sign-off request** with a one-line note on why T1 was unavailable and the T2 candidate. Save to `docs/kickoffs/` or paste inline for Trevor.

- [ ] **CHECKPOINT (Trevor):** Trevor reviews the manifest and approves ship-as-T2 (recorded in each variety's `confidence_tier`) or holds specific datapoints. **Do not proceed to Task 7 until sign-off.** No load-bearing number ships on an unapproved non-T1 source.

- [ ] **Step 4: Commit the builder (tooling only; canonical untouched)**

```bash
git add tools/build_apple_varieties_patch.py
git commit -m "build(apple): variety-pilot patch builder (13 + Jonagold/Mutsu + Dolgo, tree schema)"
```

---

## Task 7: SHA-guarded splice + full release battery (CHECKPOINT: promote)

**Files:**
- Generate: `tools/batches/apple_varieties_pilot.json`
- Modify (promote): `crops_data_final.json`

- [ ] **Step 1: Generate the patch + apply to a scratch copy**

```bash
python3 tools/build_apple_varieties_patch.py
python3 tools/apply_patch.py tools/batches/apple_varieties_pilot.json --out crops_data_final.scratch.json
```
Expected: `apply_patch` reports the footprint = apple's `varieties` + `variety_archetype` key only; SHA gate passes (base `340c2983`).

- [ ] **Step 2: Audit the footprint (exactly apple moved; count 125; COMPACT)**

```bash
python3 -c "import json; a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json')); ca={c['slug']:c for c in a['crops']}; cb={c['slug']:c for c in b['crops']}; print('count', len(b['crops'])); print('moved', [s for s in ca if ca[s]!=cb.get(s)])"
```
Expected: `count 125`; `moved ['apple']` (and nothing else).

- [ ] **Step 3: Run the full release battery on the scratch candidate**

```bash
python3 tools/whole_crop_gate.py apple crops_data_final.scratch.json
python3 tools/variety_detail_gate.py crops_data_final.scratch.json --warnings --coverage
python3 tools/gate_all.py crops_data_final.scratch.json
python3 tools/release_verify.py crops_data_final.scratch.json --base crops_data_final.json
python3 tools/source_truth_sample.py --dataset crops_data_final.scratch.json --crops apple
```
Expected: `whole_crop_gate` apple clean (18/18); `variety_detail_gate` apple in-scope, violations=0 (coverage shows apple's 16 objs); `gate_all` all 116 certified unchanged + apple clean; `release_verify` no new CONCERN; `source_truth_sample` apple bloom/chill trace to the approved sources.

- [ ] **CHECKPOINT (Trevor):** green battery + manifest sign-off = promote-eligible. On Trevor's go:

- [ ] **Step 4: Promote scratch to canonical (COMPACT) and confirm SHA**

```bash
python3 -c "import json; d=json.load(open('crops_data_final.scratch.json')); open('crops_data_final.json','w',encoding='utf-8').write(json.dumps(d, separators=(',',':'), ensure_ascii=False))"
shasum -a 256 crops_data_final.json | cut -d' ' -f1
```
Expected: a new SHA (record it for the state trio). Re-run `python3 tools/whole_crop_gate.py apple` and `python3 tools/gate_all.py` against the promoted canonical -- both clean.

---

## Task 8: State trio + field-addition register + release commit

**Files:**
- Modify: `CURRENT_STATE.md` (surgical patch), `STATE_HISTORY.md` (prepend), `LATEST.txt`, `docs/field_addition_register.md`

- [ ] **Step 1: Add the field-addition register row**

Add a `docs/field_addition_register.md` row for the tree-variety bundle (the tree block) with the explicit INV-1 hard-flip trigger verbatim: *"flip the `variety_detail_gate` tree-block checks from soft/standalone into the A39 register-coverage hard floor + `gate_all` when the Spec-2 rollout column pass reaches full-roster coverage."*

- [ ] **Step 2: State trio**

- CURRENT_STATE.md: patch surgically (no `---` separator; do NOT run a naive `gen_current_state` regen -- it corrupts the file per `current-state-md-drift`). Update count/certified line + add the apple tree-pilot note.
- STATE_HISTORY.md: prepend a most-recent-first entry: canonical SHA transition (`340c2983 -> <new>`), footprint (apple varieties + variety_archetype), the schema/gate/register changes, the recorded adversarial RED proof (Task 5), the manifest sign-off summary.
- LATEST.txt: bump SHA + session line.

- [ ] **Step 3: Release commit (Trevor confirms push)**

```bash
git add crops_data_final.json tools/batches/apple_varieties_pilot.json CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/field_addition_register.md
git commit -m "feat(apple): tree-archetype variety pilot -- 13 + Jonagold/Mutsu/Dolgo to flat tree schema"
```
Trevor confirms the push. **No plant-astro submodule bump from this session** (owned by the plant-astro session; the app consumption feature + INV-2 handoff is Spec 2).

---

## Self-Review notes (author)

- **Spec coverage:** schema refactor (Task 1) + tree block (Task 2) + coherence (Task 3) + honesty fields `triploid`/`self_fruitful` (Tasks 1-2) + register ruling (Task 4) + adversarial RED (Task 5) + sourcing contract & manifest sign-off (Task 6) + splice/battery/footprint (Task 7) + state trio, register row, INV-1 (Task 8). Honesty-engine *computation* (Spec §5) and plant-astro consumption are Spec 2 (INV-2), intentionally absent.
- **`bloom_window_relative` derivation** (Spec §5) is documented in the Task-6 builder docstring, not gate-enforced beyond shape -- correct, since it is derived, not sourced.
- **Non-obvious risk:** Task 1 must keep the existing annual asserts green; the dispatch defaults to `annual_dtm` on absent/unknown `variety_archetype`, so the dry-bean fixtures (no key) are unaffected. Verified by re-running the full test file at each step.
