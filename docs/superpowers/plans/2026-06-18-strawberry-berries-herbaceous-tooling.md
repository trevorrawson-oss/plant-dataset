# Strawberry / berries_herbaceous Tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Claude Code structural lane for the strawberry gold-standard arc (anchor 13, the first `berries_herbaceous` crop): the calendar deriver, the two cert-gate branches, and the `build_region_shells` path, all test-first, so Step 3.5 onward can run.

**Architecture:** Mirror the certified tree tooling exactly. `berry_calendar.py` is the strawberry analog of `tree_calendar.py` (a pure deriver + a coherence gate). `berry_herbaceous_gate.py` is the analog of `photoperiod_gate.py` (a structural cert function, no-op off-scope). Both are wired into `whole_crop_gate.py` as new always-on A-sections (no-op unless `calendar_basis == "perennial_herbaceous"`), exactly as A9 wired the photoperiod gate. `build_region_shells.py` gains a berry-herbaceous path beside the tree path. No existing crop is affected: every new check is gated on the new basis, which only strawberry will carry, and only after Step 3.5 sets it.

**Tech Stack:** Python 3 (stdlib only -- `json`, `re`, `sys`, `os`). Flat `tools/` directory with co-located `test_*.py` scripts run via `python3 tools/test_X.py` (plain `assert` + a final "all tests passed" print; there is no pytest in this repo).

## Global Constraints

- **Mirror the existing tool patterns verbatim.** `photoperiod_gate.py` is the template for a gate module; `tree_calendar.py` for a deriver + coherence gate; `_build_tree_shells`/`_build_tree_region`/`_build_tree_cell` for the shell builder; `test_photoperiod_gate.py` for a test file.
- **Every new check no-ops off-scope.** The two gates return `[]` unless `crop.get("calendar_basis") == "perennial_herbaceous"`. The shell path fires only for `_is_berry_herbaceous(crop)`.
- **Admission-safe.** A check must PASS at the Step-3.5 admission state (region cells shaped but unfilled: `grown_as` null, `calendar` `[]`). Skip null/empty per-cell data exactly as `photoperiod_violations` skips a null `recommended_day_length_type` and `tree_calendar_violations` skips an empty `calendar`.
- **Canonical `crops_data_final.json` is COMPACT** (`separators=(",",":")`, no trailing newline, never `indent=2`). These tasks never rewrite the dataset file; they only add/modify tool files. (Step 3.5's apply, which does touch the dataset, is downstream of this plan and uses `apply_region_shells.py`.)
- **TDD, frequent commits.** One test-first cycle per task; commit at the end of each task. The plant-dataset repo is on `main` and dataset-repo commits are autonomous (announce-then-execute); these are tool/doc commits, so the pre-commit release-verify hook self-skips (no `crops_data_final.json` staged).
- **No em dashes in any string a grower reads.** Irrelevant to these tool files (Python comments may use `--`), but the deriver/gate only emit backend violation strings, never user-facing copy.
- **Design of record:** `docs/superpowers/specs/2026-06-18-strawberry-berries-herbaceous-model-design.md` (D1-D9). Read it before starting.

---

## File Structure

- `tools/berry_calendar.py` (CREATE) -- `derive_perennial_berry_calendar`, `derive_annual_berry_calendar`, `derive_berry_calendar`, `berry_calendar_violations`. Imports `_months` from `tree_calendar` (DRY -- the month parser is identical).
- `tools/test_berry_calendar.py` (CREATE) -- worked-example tests for both calendar shapes + the coherence gate.
- `tools/berry_herbaceous_gate.py` (CREATE) -- `berry_herbaceous_violations` (structural cert: lifecycle scalars, `grown_as` typing, no-tree-keys, token placement, photoperiod guard, no cross-pollination machinery).
- `tools/test_berry_herbaceous_gate.py` (CREATE) -- structural-invariant tests.
- `tools/whole_crop_gate.py` (MODIFY, after the A9 block ~line 287) -- add A10 (structural) + A11 (calendar coherence), importing the two new modules.
- `tools/build_region_shells.py` (MODIFY) -- add `_is_berry_herbaceous`, `_build_berry_herbaceous_shells`, `_build_berry_region`, `_build_berry_cell`, and a dispatcher branch in `build_region_shells`.
- `tools/test_build_region_shells.py` (MODIFY) -- add berry-herbaceous shell-build assertions.

Task order: 1 (deriver) -> 2 (structural gate) -> 3 (wire both into whole_crop_gate) -> 4 (shell builder). Tasks 1 and 2 are independent; 3 depends on both; 4 is independent of 1-3 but listed last because it is the largest.

---

### Task 1: `berry_calendar.py` -- the calendar deriver + coherence gate

**Files:**
- Create: `tools/berry_calendar.py`
- Test: `tools/test_berry_calendar.py`

**Interfaces:**
- Consumes: `from tree_calendar import _months` (parses the leading month range of a display string into 0-based month indices; already handles the `"(...)"` aside).
- Produces:
  - `derive_perennial_berry_calendar(bloom_field, harvest_field, last_frost_field, first_frost_field) -> list[str] | None` -- 12 tokens from `{dormant, growing, bloom, harvest, renovation}`; `None` if any input is empty/unparseable.
  - `derive_annual_berry_calendar(plant_out_field, bloom_field, harvest_field) -> list[str] | None` -- 12 tokens from `{season_over, plant, growing, bloom, harvest}`; `None` if plant_out or harvest is empty/unparseable.
  - `derive_berry_calendar(grown_as, cell) -> list[str] | None` -- dispatches on `grown_as` ("perennial"/"annual"), reading `cell["bloom"]`, `cell["harvest"]`, `cell["plant_out"]`, `cell["resolved_from"]["last_frost"|"first_frost"]`.
  - `berry_calendar_violations(crop) -> list[str]` -- `[]` unless basis is `perennial_herbaceous`; recompute-from-dates per non-empty cell, fail on mismatch.

- [ ] **Step 1: Write the failing test**

Create `tools/test_berry_calendar.py`:

```python
#!/usr/bin/env python3
"""Tests for the berries_herbaceous calendar deriver + coherence gate (strawberry,
anchor 13). Run: python3 tools/test_berry_calendar.py

The strawberry calendar is DERIVED data (the tree_calendar lesson): a pure function of
the cell's grown_as + display windows, so it cannot drift from them. Two shapes:
  - PERENNIAL (matted-row, June-bearing spine): dormant winter / growing season /
    bloom / harvest / renovation (month after harvest). Frost dates bracket dormancy.
  - ANNUAL (hot-summer CA/FL): plant in fall, growing, bloom, harvest, season_over.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_calendar import (derive_perennial_berry_calendar, derive_annual_berry_calendar,
                            derive_berry_calendar, berry_calendar_violations)

# 1. PERENNIAL z5: last_frost Apr, first_frost Oct, bloom May, harvest June -> renovation July.
perennial = derive_perennial_berry_calendar("May", "June", "April", "October")
assert perennial == ["dormant", "dormant", "dormant", "growing", "bloom", "harvest",
                     "renovation", "growing", "growing", "growing", "dormant", "dormant"], perennial

# 2. ANNUAL CA z9: plant Oct, bloom Feb, harvest Mar-Jun -> season_over the rest.
annual = derive_annual_berry_calendar("October", "February", "March-June")
assert annual == ["growing", "bloom", "harvest", "harvest", "harvest", "harvest",
                  "season_over", "season_over", "season_over", "plant", "growing", "growing"], annual

# 3. unparseable / empty inputs -> None (the caller owns emptiness)
assert derive_perennial_berry_calendar("", "June", "April", "October") is None
assert derive_annual_berry_calendar("October", "February", "") is None

# 4. dispatch reads the cell shape
cell_p = {"bloom": "May", "harvest": "June", "resolved_from": {"last_frost": "April", "first_frost": "October"}}
assert derive_berry_calendar("perennial", cell_p) == perennial, derive_berry_calendar("perennial", cell_p)
cell_a = {"plant_out": "October", "bloom": "February", "harvest": "March-June"}
assert derive_berry_calendar("annual", cell_a) == annual, derive_berry_calendar("annual", cell_a)
assert derive_berry_calendar("bogus", cell_a) is None

# 5. coherence gate: no-op off-basis
non_berry = {"calendar_basis": "frost_anchored", "regions": {}}
assert berry_calendar_violations(non_berry) == [], "non-berry crop must be a no-op"

# 6. coherence gate: a stored calendar that matches the deriver -> clean
def berry_crop(stored_cal, grown_as="perennial"):
    return {"calendar_basis": "perennial_herbaceous", "regions": {"northern_tier": {
        "resolved_by_zone": {"5": {"grown_as": grown_as, "bloom": "May", "harvest": "June",
            "resolved_from": {"last_frost": "April", "first_frost": "October"},
            "calendar": stored_cal}}}}}
assert berry_calendar_violations(berry_crop(perennial)) == [], berry_calendar_violations(berry_crop(perennial))

# 7. coherence gate: a DRIFTED stored calendar -> violation naming the cell
drift = list(perennial); drift[6] = "growing"   # renovation hand-edited away
assert any("northern_tier" in v and "5" in v and "incoherent" in v
           for v in berry_calendar_violations(berry_crop(drift))), berry_calendar_violations(berry_crop(drift))

# 8. coherence gate: an EMPTY calendar (Step-3.5 admission) -> skipped (no-op)
assert berry_calendar_violations(berry_crop([])) == [], "empty calendar is the admission state -- skip"

print("berry_calendar: all tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_berry_calendar.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'berry_calendar'`.

- [ ] **Step 3: Write minimal implementation**

Create `tools/berry_calendar.py`:

```python
#!/usr/bin/env python3
"""Strawberry (`berries_herbaceous`, anchor 13) `calendar[]` generator + coherence gate.

The strawberry calendar is DERIVED data -- a pure function of the cell's grown_as +
display windows -- not independent information, exactly like the tree calendar. Two shapes,
selected by the per-cell `grown_as` (perennial in the north, annual in hot-summer CA/FL):

  PERENNIAL (June-bearing matted-row spine): dormant winter bracketed by the frost dates;
    growing inside the frost-free season; bloom; harvest; renovation = the month after
    harvest end (mow + thin the row). Never season_over (a perennial bed does not end).
  ANNUAL (CA interior/desert + FL): plant in fall; growing; bloom; harvest; the planting
    then ENDS -> season_over fills the rest. Never renovation/dormant.

`berry_calendar_violations(crop)` recompute-from-dates per cell and fails on any mismatch
(wired into whole_crop_gate, flip-blocking, no-op unless basis is perennial_herbaceous).
See 2026-06-18-strawberry-berries-herbaceous-model-design.md (D2/D4/D9).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import _months   # DRY: identical "leading month range" parser


def derive_perennial_berry_calendar(bloom_field, harvest_field, last_frost_field, first_frost_field):
    """12-token perennial matted-row calendar, or None if any window is empty/unparseable.
    Dormancy is bracketed by the frost dates; renovation is the month after harvest end."""
    bm, hm = _months(bloom_field), _months(harvest_field)
    lf, ff = _months(last_frost_field), _months(first_frost_field)
    if not (bm and hm and lf and ff):
        return None
    cal = ["dormant"] * 12
    m = lf[0]                              # frost-free growing season (last_frost .. first_frost)
    while True:
        cal[m] = "growing"
        if m == ff[-1]:
            break
        m = (m + 1) % 12
    m = hm[0]                              # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    cal[bm[0]] = "bloom"
    cal[(hm[-1] + 1) % 12] = "renovation"  # mow + thin the month after the June flush
    return cal


def derive_annual_berry_calendar(plant_out_field, bloom_field, harvest_field):
    """12-token annual (fall-plant, winter-wrap) calendar, or None if plant_out or harvest
    is empty/unparseable. The planting ENDS after harvest -> season_over fills the rest."""
    pm, hm = _months(plant_out_field), _months(harvest_field)
    if not (pm and hm):
        return None
    cal = ["season_over"] * 12
    p, hs = pm[0], hm[0]
    cal[p] = "plant"
    m = (p + 1) % 12                       # growing: plant+1 up to harvest_start-1 (wrapping)
    while m != hs:
        cal[m] = "growing"
        m = (m + 1) % 12
    m = hs                                 # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    bm = _months(bloom_field)              # bloom overlay (a month within the pre-harvest run)
    if bm:
        cal[bm[0]] = "bloom"
    return cal


def derive_berry_calendar(grown_as, cell):
    """Dispatch on the cell's grown_as, reading its display fields. None off-enum/unparseable."""
    if grown_as == "perennial":
        rf = cell.get("resolved_from") or {}
        return derive_perennial_berry_calendar(
            cell.get("bloom"), cell.get("harvest"), rf.get("last_frost"), rf.get("first_frost"))
    if grown_as == "annual":
        return derive_annual_berry_calendar(
            cell.get("plant_out"), cell.get("bloom"), cell.get("harvest"))
    return None


def berry_calendar_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis perennial_herbaceous.
    For every cell with a NON-EMPTY calendar, stored must equal the calendar derived from that
    cell's own grown_as + dates. Empty calendars are the Step-3.5 admission state (skipped)."""
    if crop.get("calendar_basis") != "perennial_herbaceous":
        return []
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            cal = cell.get("calendar") or []
            if not cal:
                continue
            ga = cell.get("grown_as")
            expect = derive_berry_calendar(ga, cell)
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but grown_as/dates missing or "
                         f"unparseable (grown_as={ga!r})")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with grown_as+dates "
                         f"(grown_as={ga!r}); stored {cal} != derived {expect}")
    return V
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_berry_calendar.py`
Expected: PASS -- prints `berry_calendar: all tests passed`.

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/berry_calendar.py tools/test_berry_calendar.py
git commit -m "feat(strawberry): berry_calendar deriver + coherence gate (anchor 13, test-first)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `berry_herbaceous_gate.py` -- the structural cert branch

**Files:**
- Create: `tools/berry_herbaceous_gate.py`
- Test: `tools/test_berry_herbaceous_gate.py`

**Interfaces:**
- Consumes: nothing from earlier tasks (independent of Task 1).
- Produces: `berry_herbaceous_violations(crop) -> list[str]` -- `[]` unless basis `perennial_herbaceous`; asserts the structural invariants (lifecycle scalars present, `self_fertile is True`, no `photoperiod` gating, no tree cross-pollination keys on varieties, per-cell `grown_as` typing + no tree-only keys + token placement). Also exports `GROWN_AS_ENUM` and `LIFECYCLE_SCALARS`.

- [ ] **Step 1: Write the failing test**

Create `tools/test_berry_herbaceous_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for the berries_herbaceous structural cert branch (strawberry, anchor 13).
Run: python3 tools/test_berry_herbaceous_gate.py

Invariants (2026-06-18-strawberry-berries-herbaceous-model-design.md D6-D9):
  - fires ONLY for calendar_basis == perennial_herbaceous (no-op otherwise).
  - lifecycle SCALARS present (Step 2, before 3.5 sets the basis -> admission-safe);
    self_fertile is True; "photoperiod" NOT in gating_factors (deliberate inverse of onion).
  - varieties carry NO tree cross-pollination keys (bloom_group/pollinizer/...).
  - per FILLED cell: grown_as in {perennial, annual}; no tree-only keys (suitability,
    chill_hours_delivered); annual cells carry no renovation/dormant, perennial cells no
    season_over. A cell with grown_as null AND empty calendar is the admission state (skip).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_herbaceous_gate import berry_herbaceous_violations, GROWN_AS_ENUM

def well_formed():
    """Minimal valid filled strawberry: scalars set, self-fertile, one perennial + one
    annual cell whose calendars carry the right tokens for their grown_as."""
    return {
        "slug": "strawberry-mini", "calendar_basis": "perennial_herbaceous",
        "self_fertile": True, "gating_factors": [],
        "establishment_years": 1, "productive_lifespan_years": 4,
        "years_to_first_harvest": [2], "years_to_full_production": [2, 3],
        "varieties": {"recommended": [
            {"name": "Honeoye", "type": "june_bearing"},
            {"name": "Albion", "type": "day_neutral"}]},
        "regions": {
            "northern_tier": {"resolved_by_zone": {"5": {"grown_as": "perennial",
                "calendar": ["dormant","dormant","dormant","growing","bloom","harvest",
                             "renovation","growing","growing","growing","dormant","dormant"]}}},
            "ca_interior": {"resolved_by_zone": {"9": {"grown_as": "annual",
                "calendar": ["growing","bloom","harvest","harvest","harvest","harvest",
                             "season_over","season_over","season_over","plant","growing","growing"]}}}},
    }

# 0. well-formed -> clean
assert berry_herbaceous_violations(well_formed()) == [], berry_herbaceous_violations(well_formed())

# 1. off-basis -> NO-OP even with garbage
off = {"slug": "carrot", "calendar_basis": "frost_anchored", "self_fertile": None,
       "gating_factors": ["photoperiod"], "regions": {}}
assert berry_herbaceous_violations(off) == [], "non-perennial_herbaceous crop must be a no-op"

# 2. ADMISSION STATE: scalars set (Step 2) but cells unfilled (grown_as null, calendar []) -> clean
c = well_formed()
for r in c["regions"].values():
    for cell in r["resolved_by_zone"].values():
        cell["grown_as"] = None; cell["calendar"] = []
assert berry_herbaceous_violations(c) == [], berry_herbaceous_violations(c)

# 3. missing lifecycle scalar -> violation
c = well_formed(); c["productive_lifespan_years"] = None
assert any("productive_lifespan_years" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 4. self_fertile not True -> violation
c = well_formed(); c["self_fertile"] = False
assert any("self_fertile" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 5. photoperiod in gating_factors -> violation (the onion-guard)
c = well_formed(); c["gating_factors"] = ["photoperiod"]
assert any("photoperiod" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 6. a variety carrying tree cross-pollination machinery -> violation
c = well_formed(); c["varieties"]["recommended"][0]["bloom_group"] = 2
assert any("bloom_group" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 7. a tree-only key on a cell (mis-route) -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["suitability"] = "fruits_reliably"
assert any("suitability" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 8. bad grown_as enum on a filled cell -> violation
c = well_formed(); c["regions"]["ca_interior"]["resolved_by_zone"]["9"]["grown_as"] = "biennial"
assert any("grown_as" in v and "biennial" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 9. annual cell carrying a perennial token -> violation
c = well_formed(); c["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"][6] = "renovation"
assert any("ca_interior" in v and "9" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 10. perennial cell carrying season_over -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"][10] = "season_over"
assert any("northern_tier" in v and "5" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

assert GROWN_AS_ENUM == {"perennial", "annual"}, GROWN_AS_ENUM
print("berry_herbaceous_gate: all tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_berry_herbaceous_gate.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'berry_herbaceous_gate'`.

- [ ] **Step 3: Write minimal implementation**

Create `tools/berry_herbaceous_gate.py`:

```python
#!/usr/bin/env python3
"""Berries_herbaceous structural cert branch (strawberry, anchor 13; the ONLY crop with
this archetype). Fires ONLY for calendar_basis == perennial_herbaceous (a no-op otherwise).
Imported + run by whole_crop_gate.py as section A10. The calendar coherence (stored ==
derived) is the SEPARATE A11 (berry_calendar.berry_calendar_violations), mirroring how the
tree split A3 (perennial cert) from A4 (calendar coherence).

Admission-safe: the lifecycle SCALARS are Step-2 data (authored BEFORE Step 3.5 sets the
basis, so they are present whenever this gate fires, exactly as photoperiod_gate asserts
variety typing). The prose pairs (renovation_*, year_one_notes_*, type_selection_*,
grown_as_note_*) are owned by register_fill_gate at Step 11, NOT here. A per-cell grown_as
that is null AND has an empty calendar is the Step-3.5 admission state (skipped).
See 2026-06-18-strawberry-berries-herbaceous-model-design.md (D6-D9).
"""
GROWN_AS_ENUM = {"perennial", "annual"}
LIFECYCLE_SCALARS = ("establishment_years", "productive_lifespan_years",
                     "years_to_first_harvest", "years_to_full_production")
_TREE_ONLY_CELL_KEYS = ("suitability", "chill_hours_delivered")
_CROSS_POLLINATION_KEYS = ("bloom_group", "pollinizer", "pollinizer_distance_ft",
                           "bloom_window_relative")


def berry_herbaceous_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis perennial_herbaceous."""
    if crop.get("calendar_basis") != "perennial_herbaceous":
        return []
    V = []

    # 1. lifecycle SCALARS present (Step-2 data; admission-safe -- see module docstring).
    for f in LIFECYCLE_SCALARS:
        v = crop.get(f)
        if v is None or v == []:
            V.append(f"lifecycle scalar {f} empty (required once basis is perennial_herbaceous)")
    if crop.get("self_fertile") is not True:
        V.append(f"self_fertile must be true (strawberry is self-fertile, no cross-pollination "
                 f"calendar); got {crop.get('self_fertile')!r}")

    # 2. photoperiod guard -- strawberry type is a VARIETY attribute, not an onion zone gate.
    if "photoperiod" in (crop.get("gating_factors") or []):
        V.append("photoperiod must NOT be in gating_factors (strawberry type is a variety "
                 "attribute, not a latitude gate)")

    # 3. no tree cross-pollination machinery on the varieties.
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            for k in _CROSS_POLLINATION_KEYS:
                if k in v:
                    V.append(f"varieties.recommended[{i}] ({v.get('name')!r}): {k} is tree "
                             f"cross-pollination machinery; strawberry is self-fertile")

    # 4. per-cell: grown_as typing, no tree-only keys, token placement vs grown_as.
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            for tk in _TREE_ONLY_CELL_KEYS:
                if tk in cell:
                    V.append(f"{rk}.{z}: tree-only key {tk!r} present "
                             f"(mis-routed through the tree builder?)")
            ga = cell.get("grown_as")
            cal = cell.get("calendar") or []
            if ga is None and not cal:
                continue  # Step-3.5 admission state
            if ga not in GROWN_AS_ENUM:
                V.append(f"{rk}.{z}: grown_as {ga!r} not in {sorted(GROWN_AS_ENUM)}")
                continue
            if cal:
                if ga == "annual" and ("renovation" in cal or "dormant" in cal):
                    V.append(f"{rk}.{z}: annual cell carries a perennial token "
                             f"(renovation/dormant): {cal}")
                if ga == "perennial" and "season_over" in cal:
                    V.append(f"{rk}.{z}: perennial cell carries season_over "
                             f"(annual-only token): {cal}")
    return V
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_berry_herbaceous_gate.py`
Expected: PASS -- prints `berry_herbaceous_gate: all tests passed`.

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/berry_herbaceous_gate.py tools/test_berry_herbaceous_gate.py
git commit -m "feat(strawberry): berry_herbaceous structural cert gate (anchor 13, test-first)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Wire A10 + A11 into `whole_crop_gate.py`

**Files:**
- Modify: `tools/whole_crop_gate.py` (insert after the A9 block, currently ending ~line 287, before the `B. dual-voice coverage` block)

**Interfaces:**
- Consumes: `berry_herbaceous_violations` (Task 2), `berry_calendar_violations` (Task 1). The gate already does `sys.path.insert(0, ...)` at line 64, so a bare `from berry_herbaceous_gate import ...` resolves.
- Produces: two new always-on sections that `fail(...)` per returned violation. No-op unless the crop's basis is `perennial_herbaceous`.

- [ ] **Step 1: Write the failing test**

There is no unit harness for the procedural `whole_crop_gate.py`; its test is an integration run. First confirm the strawberry shell (still `frost_anchored`, so both new sections must no-op and the gate must behave exactly as today):

Run: `python3 tools/whole_crop_gate.py strawberry`
Expected BEFORE the edit: the run prints A1..A9 and B..G with NO `A10`/`A11` lines. (Capture this as the baseline -- the edit must add A10/A11 lines that report `0` for strawberry, changing nothing else.)

Then assert the imports do not yet exist:

Run: `python3 -c "import sys; sys.path.insert(0,'tools'); import whole_crop_gate" strawberry 2>&1 | grep -c "A10"`
Expected: `0` (no A10 section yet).

- [ ] **Step 2: Confirm the new modules import cleanly in isolation**

Run: `python3 -c "import sys; sys.path.insert(0,'tools'); from berry_herbaceous_gate import berry_herbaceous_violations; from berry_calendar import berry_calendar_violations; print('imports ok')"`
Expected: `imports ok` (Tasks 1 + 2 are in place).

- [ ] **Step 3: Insert the A10 + A11 sections**

In `tools/whole_crop_gate.py`, immediately AFTER the A9 photoperiod block (the loop `for m in _photo: fail(f"photoperiod: {m}")`) and BEFORE `# ---------------- B. dual-voice coverage ----------------`, insert:

```python
# ---------------- A10. berries_herbaceous structural cert (no-op off perennial_herbaceous) ----------------
# Strawberry (anchor 13, the only berries_herbaceous crop) is a herbaceous perennial whose
# LIFECYCLE is region-dependent: a per-cell grown_as in {perennial, annual} (north matted-row
# vs hot-summer CA/FL annual). This asserts the structural invariants the generic checks do not
# encode -- lifecycle scalars present, self_fertile, the photoperiod guard (strawberry type is a
# variety attribute, NOT an onion zone gate), no tree cross-pollination keys, no tree-only cell
# keys, and grown_as<->token placement. No-op unless basis perennial_herbaceous. (strawberry, 2026-06-18.)
from berry_herbaceous_gate import berry_herbaceous_violations
print("A10. berries_herbaceous structural cert (lifecycle + grown_as + guards; no-op off scope)")
_berry = berry_herbaceous_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | berries_herbaceous violations: {len(_berry)}")
for m in _berry:
    fail(f"berries_herbaceous: {m}")

# ---------------- A11. berries_herbaceous calendar coherence (DERIVED-from-dates) ----------------
# The strawberry calendar[] is a pure function of the cell's grown_as + display windows (the
# tree_calendar lesson): perennial -> dormant/growing/bloom/harvest/renovation bracketed by frost;
# annual -> plant/growing/bloom/harvest/season_over. Recompute-from-dates and fail on any mismatch.
# Empty calendars are the Step-3.5 admission state (skipped). No-op off perennial_herbaceous.
from berry_calendar import berry_calendar_violations
print("A11. berries_herbaceous calendar coherence (calendar == derive(grown_as, dates); no-op off scope)")
_berrycal = berry_calendar_violations(crop)
print(f"  berries_herbaceous calendar violations: {len(_berrycal)}")
for m in _berrycal:
    fail(f"berries_herbaceous calendar: {m}")
```

- [ ] **Step 4: Run the integration check**

Run: `python3 tools/whole_crop_gate.py strawberry`
Expected: the run now prints `A10. ...` reporting `calendar_basis='frost_anchored' | berries_herbaceous violations: 0` and `A11. ... violations: 0` (both no-op because strawberry's shell is still `frost_anchored`). Every other section is unchanged. Confirm the final line is still the pre-existing `GATE: ...` summary and the exit behavior is unchanged (no new violations introduced).

Then prove the sections actually fire on a `perennial_herbaceous` crop with a synthetic fixture:

Run:
```bash
python3 -c "
import sys; sys.path.insert(0,'tools')
from berry_herbaceous_gate import berry_herbaceous_violations
from berry_calendar import berry_calendar_violations
crop={'calendar_basis':'perennial_herbaceous','self_fertile':None,'gating_factors':[],'regions':{}}
print('structural fires:', len(berry_herbaceous_violations(crop))>0)
print('calendar no-op on empty regions:', berry_calendar_violations(crop)==[])
"
```
Expected: `structural fires: True` (missing scalars/self_fertile), `calendar no-op on empty regions: True`.

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/whole_crop_gate.py
git commit -m "feat(strawberry): wire A10 (structural) + A11 (calendar coherence) into whole_crop_gate

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `build_region_shells` berries_herbaceous path

**Files:**
- Modify: `tools/build_region_shells.py` (add the detector + builders; add a dispatcher branch in `build_region_shells`, after the `_is_tree`/`_is_indoor` branches ~line 46)
- Test: `tools/test_build_region_shells.py` (add berry-herbaceous assertions)

**Interfaces:**
- Consumes: the existing module-level `SESSION`/`DATE` constants and the `build_region_shells(crop)` entry point.
- Produces:
  - `_is_berry_herbaceous(crop) -> bool` -- True if basis is `perennial_herbaceous` (re-run marker) or archetype is `berries_herbaceous`.
  - `_build_berry_herbaceous_shells(crop) -> crop` -- sets `calendar_basis = "perennial_herbaceous"`, builds all 10 region cells.
  - `_build_berry_region(r)` / `_build_berry_cell(cell)` -- the region-constant and per-cell shells (mutate in place, idempotent + no-clobber via `setdefault`).

- [ ] **Step 1: Write the failing test**

Append to `tools/test_build_region_shells.py` (match the file's existing harness style -- it runs as a script with asserts). Add:

```python
# ---- berries_herbaceous (strawberry, anchor 13) shell build ----
from build_region_shells import (build_region_shells, _is_berry_herbaceous,
                                  _build_berry_herbaceous_shells)

def _berry_shell_crop():
    """An author-fresh strawberry-shaped crop: perennial archetype, frost_anchored wipe
    default, two region cells to reshape."""
    return {
        "slug": "strawberry", "archetype": "berries_herbaceous", "lifecycle": "perennial",
        "calendar_basis": "frost_anchored",
        "regions": {
            "northern_tier": {"region_label": "Northern tier", "resolved_by_zone": {
                "5": {"start_indoors": None, "direct_sow": None, "plantings": [], "calendar": []}}},
            "ca_interior": {"region_label": "California -- interior", "resolved_by_zone": {
                "9": {"start_indoors": None, "direct_sow": None}}}},
    }

# detector: True by archetype (first run) and by basis (re-run)
assert _is_berry_herbaceous(_berry_shell_crop()) is True
assert _is_berry_herbaceous({"calendar_basis": "perennial_herbaceous"}) is True
assert _is_berry_herbaceous({"archetype": "warm_season_fruiting", "calendar_basis": "frost_anchored"}) is False
# strawberry must NOT be picked up by the tree detector (archetype is not *_fruit_tree, lifecycle not permanent)
from build_region_shells import _is_tree
assert _is_tree(_berry_shell_crop()) is False

# build flips the basis and shapes every cell
c = build_region_shells(_berry_shell_crop())
assert c["calendar_basis"] == "perennial_herbaceous", c["calendar_basis"]
# dash resolution on the region label (shared convention)
assert c["regions"]["ca_interior"]["region_label"] == "California: interior", c["regions"]["ca_interior"]["region_label"]

cell = c["regions"]["northern_tier"]["resolved_by_zone"]["5"]
# the grown_as lifecycle slot + its dual-register note, scaffolded null
assert cell["grown_as"] is None and "grown_as_note_seasoned" in cell and "grown_as_note_beginner" in cell
# render keys reused from the annual/tree names; calendar empty at admission
assert cell["calendar"] == [] and cell["plant_out"] is None and cell["bloom"] is None
assert cell["harvest_start"] is None and cell["harvest_end"] is None
assert cell["resolved_from"] == {} and cell["resolution_method"] is None
assert cell["frost_risk_note_seasoned"] is None
# annual-only keys stripped; NO tree-only keys introduced
assert "start_indoors" not in cell and "direct_sow" not in cell and "plantings" not in cell
assert "suitability" not in cell and "chill_hours_delivered" not in cell

# region-constant rule layer: ONE crown-setting establishment entry (no succession/second_planting)
pls = c["regions"]["northern_tier"]["plantings"]
assert len(pls) == 1 and pls[0]["track"] == "perennial" and pls[0]["label"] == "establishment"
assert pls[0]["plant_out"] == [] and pls[0]["bloom"] == [] and pls[0]["harvest_start"] == []

# idempotent + no-clobber: a re-run does not wipe a filled value
cell["plant_out"] = "Apr 1-20"
build_region_shells(c)
assert c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["plant_out"] == "Apr 1-20", "re-run clobbered a filled cell"

print("build_region_shells berries_herbaceous: all tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_build_region_shells.py`
Expected: FAIL with `ImportError: cannot import name '_is_berry_herbaceous'`.

- [ ] **Step 3: Add the dispatcher branch**

In `tools/build_region_shells.py`, in `build_region_shells(...)`, after the `_is_indoor` branch (line 45-46) and before the `direct = ...` line (line 47), insert:

```python
    if _is_berry_herbaceous(crop):
        return _build_berry_herbaceous_shells(crop)
```

- [ ] **Step 4: Add the detector + builders**

In `tools/build_region_shells.py`, after the tree builders (after `_build_tree_cell`, ~line 238, before `_north_should_promote`), insert:

```python
# ---------------------------------------------------------------------------
# BERRIES_HERBACEOUS region model (strawberry Step 3.5, anchor 13; the only crop with
# this archetype). A herbaceous perennial whose LIFECYCLE is region-dependent: the north
# grows it as a perennial matted row, hot-summer CA/FL as a fall-planted annual. The crop
# is planted from bare-root dormant crowns in a frost-anchored window, so frost resolution
# stays ON (basis perennial_herbaceous, not a tree basis). The per-cell grown_as picks the
# lifecycle the renderer + the A10/A11 gates branch on. See the 2026-06-18 design spec.
# ---------------------------------------------------------------------------

# resolved-cell keys belonging to the ANNUAL sowing model only -- a crown-planted perennial
# has no indoor start, no second sowing, no per-cell rule structure. Stripped.
_BERRY_CELL_DEAD = ("start_indoors", "direct_sow", "lifted_from_zone", "plantings",
                    "notes", "zone_notes", "planting_note",
                    "first_plant_date", "last_plant_date")


def _is_berry_herbaceous(crop):
    """A herbaceous-perennial berry (strawberry) takes the berry region path. Detected by the
    perennial_herbaceous basis marker (set by THIS builder, so re-runs stay on the path) or, on
    the first run before the flip, by the berries_herbaceous archetype. NOT a tree (_is_tree keys
    on *_fruit_tree / lifecycle permanent, neither of which strawberry is)."""
    return (crop.get("calendar_basis") == "perennial_herbaceous"
            or crop.get("archetype") == "berries_herbaceous")


def _build_berry_herbaceous_shells(crop):
    """Build every region cell to the berries_herbaceous reference shape. Pure transform; no
    biology invented; idempotent + no-clobber. Sets calendar_basis -> perennial_herbaceous, the
    marker that branches Step 5.5 + the A10/A11 gates onto the perennial-herbaceous criteria."""
    crop["calendar_basis"] = "perennial_herbaceous"
    for r in (crop.get("regions") or {}).values():
        if isinstance(r, dict):
            _build_berry_region(r)
    return crop


def _build_berry_region(r):
    lbl = r.get("region_label")
    if isinstance(lbl, str) and " -- " in lbl:
        r["region_label"] = lbl.replace(" -- ", ": ")
    r.setdefault("region_notes_seasoned", None)
    r.setdefault("region_notes_beginner", None)
    if r.get("sources_pending_admission") == []:
        r.pop("sources_pending_admission", None)
    # region-constant RULE layer: a SINGLE crown-setting establishment entry (no succession,
    # no second_planting -- a strawberry bed is planted once per replant cycle). Only (re)build
    # when it is not already the perennial entry -- never clobber a filled rule.
    pl = r.get("plantings")
    if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)
            and pl[0].get("track") == "perennial"):
        r["plantings"] = [{
            "succession_id": 1, "label": "establishment", "track": "perennial",
            "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": [],
            "anchoring_urls": {},
        }]
    r.setdefault("plantings_provenance", None)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            _build_berry_cell(cell)


def _build_berry_cell(cell):
    """Reshape one resolved_by_zone cell to the berries_herbaceous key-set, idempotent +
    no-clobber. The per-zone `grown_as` makes the region-dependent lifecycle first-class. The
    render keys reuse the annual/tree names (plant_out/bloom/harvest_*) so the renderer reads
    berry, tree, and annual cells uniformly. NO tree keys (suitability/chill_hours_delivered)."""
    for dead in _BERRY_CELL_DEAD:
        cell.pop(dead, None)
    cell.setdefault("grown_as", None)               # perennial (north) | annual (hot-summer CA/FL)
    cell.setdefault("grown_as_note_seasoned", None)
    cell.setdefault("grown_as_note_beginner", None)
    cell.setdefault("plant_out", None)              # crown-setting window (frost-anchored)
    cell.setdefault("bloom", None)
    cell.setdefault("harvest_start", None)
    cell.setdefault("harvest_end", None)
    cell.setdefault("harvest", None)
    cell.setdefault("calendar", [])                 # 12-month cycle, derived at Step 4 (A11)
    cell.setdefault("frost_risk_note_seasoned", None)  # late-frost-kills-open-blossom warning
    cell.setdefault("resolved_from", {})            # frost dates used (auditable)
    cell.setdefault("resolution_method", None)      # -> "perennial_herbaceous_precompute" once filled
    cell.setdefault("sources", [])
    cell.setdefault("anchoring_urls", {})
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 tools/test_build_region_shells.py`
Expected: PASS -- prints (among the file's existing output) `build_region_shells berries_herbaceous: all tests passed`.

- [ ] **Step 6: Run the full tool test suite (no regressions)**

Run: `for t in tools/test_*.py; do echo "== $t =="; python3 "$t" || break; done`
Expected: every test file prints its `... all tests passed` line; none errors. (Confirms the new modules + the whole_crop_gate edit broke nothing.)

- [ ] **Step 7: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/build_region_shells.py tools/test_build_region_shells.py
git commit -m "feat(strawberry): build_region_shells berries_herbaceous path (anchor 13, test-first)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## After this plan

The tooling exists and is green. The arc then runs in the normal collaboration:
1. **claude.ai** authors Steps 1-3 (source set, the Step-2 scalars incl. the lifecycle scalars + `self_fertile` + `start_method.start = "bare_root_dormant"`, companions). Trevor hands the kickoff bundle.
2. **Claude Code** runs Step 3.5: `build_region_shells` (this plan's path) flips the basis + builds the 10 shells; apply via `apply_region_shells.py`; the always-on gate must report A10/A11 = 0 at admission.
3. **claude.ai** authors Steps 4-8 (the per-region `grown_as` + crown windows + the derived calendars + all the prose).
4. **Claude Code** runs Step 11 cert: `whole_crop_gate` (incl. A10/A11) + `register_fill_gate` + `register_completeness_gate` + the verbatim/source-fidelity fetch, then the flip.

The deriver's exact perennial frost-bracket boundary + the annual winter-wrap shape are validated against the FIRST real authored cell at Step 4 (the way `tree_calendar` was pinned byte-for-byte against apple); if a legitimately-authored cell needs a refinement, adjust the deriver + its test there.

## Self-Review

- **Spec coverage:** D2 (new basis) -> Task 4 sets it. D3 (`grown_as`) -> Task 4 scaffolds it, Tasks 1+2 gate it. D4 (calendar vocab, `renovation`, `season_over` split) -> Task 1 deriver + Task 2 token placement. D5 (`bare_root_dormant`, new shell path, not `_is_tree`) -> Task 4 (+ its `_is_tree` False assertion). D6 (lifecycle scalars) -> Task 2 presence check. D7 (no photoperiod gate) -> Task 2 guard. D8 (self-fertile, no cross-pollination) -> Task 2 checks. D9 (the gate) -> Tasks 1+2+3. The prose-fill (renovation_*, year_one_notes_*, type_selection_*) is intentionally left to `register_fill_gate` at Step 11 (noted in Task 2 docstring) -- not a gap.
- **Placeholder scan:** none -- every step carries runnable code/commands.
- **Type consistency:** `berry_herbaceous_violations`/`berry_calendar_violations` names match across Tasks 1/2/3; `_is_berry_herbaceous`/`_build_berry_herbaceous_shells` match across Task 4's interface + body; `grown_as`/`GROWN_AS_ENUM`/`perennial_herbaceous`/`renovation`/`season_over` used identically in every task and the deriver's output matches the gate's fixtures byte-for-byte (the Task 1 `perennial`/`annual` arrays equal the Task 2 `well_formed()` calendars).
