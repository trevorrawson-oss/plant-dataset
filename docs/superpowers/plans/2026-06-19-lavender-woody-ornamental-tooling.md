# Lavender woody-ornamental tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Build the test-first tooling for the `perennial_woody_ornamental` archetype (anchor 14, lavender) so the data arc (Steps 1-3 -> 3.5 -> 4) can run, exactly mirroring the strawberry `berries_herbaceous` tooling.

**Architecture:** A pure-function calendar DERIVER (`woody_ornamental_calendar.py`) + a release-lane FILL pass (`derive_woody_ornamental_calendars.py`) + a structural cert gate (`woody_ornamental_gate.py`, whole_crop_gate A12) + the deriver coherence gate (A13) + a `build_region_shells` path. All no-op unless `calendar_basis == "perennial_woody_ornamental"`, so the 13 certified crops are untouched. Each tool is a sibling of its `berry_*` counterpart.

**Tech Stack:** Python 3 stdlib only; `pytest`-free plain-`assert` test modules run via `python3 tools/test_*.py` (the existing convention); DRY reuse of `tree_calendar._months`.

## Global Constraints
- Canonical JSON is COMPACT: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. (Tools that only read/derive do not re-serialize the dataset; the FILL pass writes compact.)
- All new tooling is NO-OP unless `calendar_basis == "perennial_woody_ornamental"` -- verified by a "returns [] / unchanged on a frost_anchored crop" test in every gate/deriver task.
- Calendar tokens for this basis: `dormant`, `growing`, `bloom`, `prune` (perennial); `plant`, `growing`, `bloom`, `season_over` (annual). NO `harvest`/`renovation` token (bloom IS the cut window; `prune` is the woody cut-back). Per spec D3.
- Mirror the berry tooling's public function names/shapes so `whole_crop_gate` wiring is symmetric.

---

## File Structure
- `tools/woody_ornamental_calendar.py` (Create) -- the deriver + `woody_ornamental_calendar_violations` (A13 body).
- `tools/test_woody_ornamental_calendar.py` (Create) -- deriver + coherence tests.
- `tools/woody_ornamental_gate.py` (Create) -- `woody_ornamental_violations` (A12 structural).
- `tools/test_woody_ornamental_gate.py` (Create) -- structural-gate tests.
- `tools/derive_woody_ornamental_calendars.py` (Create) -- release-lane FILL pass (CLI + `fill_woody_ornamental_calendars`).
- `tools/test_derive_woody_ornamental_calendars.py` (Create) -- FILL-pass tests.
- `tools/whole_crop_gate.py` (Modify: after A11, ~line 310) -- wire A12 + A13.
- `tools/build_region_shells.py` (Modify: the `_is_*` dispatch ~line 47 + a new builder) -- `_is_woody_ornamental` + `_build_woody_ornamental_shells`.
- `tools/test_build_region_shells.py` (Modify) -- shell-path test.

---

## Task 1: The calendar deriver (`woody_ornamental_calendar.py`)

**Files:**
- Create: `tools/woody_ornamental_calendar.py`
- Test: `tools/test_woody_ornamental_calendar.py`

**Interfaces:**
- Consumes: `tree_calendar._months(field) -> list[int]` (the shared leading-month-range parser).
- Produces: `derive_perennial_woody_calendar(bloom, last_frost, first_frost) -> list[str]|None`; `derive_annual_woody_calendar(plant_out, bloom) -> list[str]|None`; `derive_woody_ornamental_calendar(grown_as, cell) -> list[str]|None`; `woody_ornamental_calendar_violations(crop) -> list[str]`.

- [ ] **Step 1: Write failing tests**

```python
# tools/test_woody_ornamental_calendar.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from woody_ornamental_calendar import (
    derive_perennial_woody_calendar, derive_annual_woody_calendar,
    derive_woody_ornamental_calendar, woody_ornamental_calendar_violations)

D,G,B,P,SO,PL = "dormant","growing","bloom","prune","season_over","plant"

def test_perennial_frost_bracketed():
    # bloom Jun-Jul, frost-free Apr..Oct -> dormant winter, prune the month after bloom
    cal = derive_perennial_woody_calendar("Jun - Jul", "Apr", "Oct")
    assert cal == [D,D,D,G,G,B,B,P,G,G,D,D]

def test_perennial_frost_free():
    # no frost dates -> grows year-round, bloom Feb-Apr, prune May (the evergreen analog)
    cal = derive_perennial_woody_calendar("Feb - Apr", None, None)
    assert cal == [G,B,B,B,P,G,G,G,G,G,G,G]

def test_annual_fall_plant_overwinter():
    # plant Oct, bloom Apr-May -> season_over fills the gap, no prune
    cal = derive_annual_woody_calendar("Oct", "Apr - May")
    assert cal == [G,G,G,B,B,SO,SO,SO,SO,PL,G,G]

def test_none_on_empty():
    assert derive_perennial_woody_calendar("", "Apr", "Oct") is None
    assert derive_annual_woody_calendar("Oct", "") is None

def test_dispatch_and_coherence_noop_off_basis():
    crop = {"calendar_basis": "frost_anchored", "regions": {}}
    assert woody_ornamental_calendar_violations(crop) == []

def test_coherence_flags_mismatch():
    cell = {"grown_as": "perennial", "bloom": "Jun - Jul",
            "resolved_from": {"last_frost": "Apr", "first_frost": "Oct"},
            "calendar": [D]*12}  # wrong
    crop = {"calendar_basis": "perennial_woody_ornamental",
            "regions": {"r": {"resolved_by_zone": {"6": cell}}}}
    v = woody_ornamental_calendar_violations(crop)
    assert len(v) == 1 and "incoherent" in v[0]

if __name__ == "__main__":
    for n,f in sorted(globals().items()):
        if n.startswith("test_") and callable(f): f(); print("ok", n)
    print("ALL PASS")
```

- [ ] **Step 2: Run, verify it fails**

Run: `python3 tools/test_woody_ornamental_calendar.py`
Expected: FAIL with `ModuleNotFoundError: woody_ornamental_calendar`.

- [ ] **Step 3: Implement the deriver**

```python
# tools/woody_ornamental_calendar.py
"""Lavender (`perennial_woody_ornamental`, anchor 14) calendar generator + coherence gate.
DERIVED data -- a pure function of grown_as + display windows, like berry_calendar/tree_calendar.
  PERENNIAL: dormant winter (frost-bracketed) | growing in the frost-free season | bloom |
    `prune` = the hard cut-back, month after bloom end. Frost-FREE (no frost dates) -> grows
    year-round (the evergreen analog), bloom+prune overlay, no dormancy. No harvest token --
    bloom IS the cut-for-use window. Never season_over (a shrub does not end).
  ANNUAL: plant -> growing -> bloom -> season_over. No prune/dormant.
See 2026-06-19-lavender-woody-ornamental-model-design.md (D3/D9)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import _months

def derive_perennial_woody_calendar(bloom_field, last_frost_field, first_frost_field):
    bm = _months(bloom_field)
    lf, ff = _months(last_frost_field), _months(first_frost_field)
    if not bm:
        return None
    if not (lf and ff):
        cal = ["growing"] * 12
    else:
        cal = ["dormant"] * 12
        m = lf[0]
        while True:
            cal[m] = "growing"
            if m == ff[-1]: break
            m = (m + 1) % 12
    m = bm[0]
    while True:
        cal[m] = "bloom"
        if m == bm[-1]: break
        m = (m + 1) % 12
    cal[(bm[-1] + 1) % 12] = "prune"   # the hard cut-back, month after bloom end
    return cal

def derive_annual_woody_calendar(plant_out_field, bloom_field):
    pm, bm = _months(plant_out_field), _months(bloom_field)
    if not (pm and bm):
        return None
    cal = ["season_over"] * 12
    p, bs = pm[0], bm[0]
    cal[p] = "plant"
    m = (p + 1) % 12
    while m != bs:
        cal[m] = "growing"
        m = (m + 1) % 12
    m = bm[0]
    while True:
        cal[m] = "bloom"
        if m == bm[-1]: break
        m = (m + 1) % 12
    return cal

def derive_woody_ornamental_calendar(grown_as, cell):
    if grown_as == "perennial":
        rf = cell.get("resolved_from") or {}
        return derive_perennial_woody_calendar(
            cell.get("bloom"), rf.get("last_frost"), rf.get("first_frost"))
    if grown_as == "annual":
        return derive_annual_woody_calendar(cell.get("plant_out"), cell.get("bloom"))
    return None

def woody_ornamental_calendar_violations(crop):
    if crop.get("calendar_basis") != "perennial_woody_ornamental":
        return []
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict): continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict): continue
            cal = cell.get("calendar") or []
            if not cal: continue
            ga = cell.get("grown_as")
            expect = derive_woody_ornamental_calendar(ga, cell)
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but grown_as/dates missing or "
                         f"unparseable (grown_as={ga!r})")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with grown_as+dates "
                         f"(grown_as={ga!r}); stored {cal} != derived {expect}")
    return V
```

- [ ] **Step 4: Run, verify PASS** -- `python3 tools/test_woody_ornamental_calendar.py` -> `ALL PASS`.
- [ ] **Step 5: Commit** -- `git add tools/woody_ornamental_calendar.py tools/test_woody_ornamental_calendar.py && git commit -m "feat(lavender): woody-ornamental calendar deriver + coherence (test-first)"`

---

## Task 2: The structural gate (`woody_ornamental_gate.py`, A12)

**Files:**
- Create: `tools/woody_ornamental_gate.py`
- Test: `tools/test_woody_ornamental_gate.py`

**Interfaces:**
- Produces: `woody_ornamental_violations(crop) -> list[str]` (no-op off basis). Checks: every resolved cell's `grown_as` in {perennial, annual}; `prune` token appears ONLY in perennial cells; NO tree keys (`rootstock`, `pollinizer`, a non-null `chill_hours_required` used as a gate); NO `harvest`/`renovation` token in any cell; `gating_factors` empty (D7); lifecycle scalars present (`hardiness_zone_min/max`).

- [ ] **Step 1: Write failing tests** -- a `well_formed()` perennial_woody_ornamental crop returns `[]`; mutate each invariant (a bad `grown_as`, a `prune` in an annual cell, an injected `rootstock`, a non-empty `gating_factors`, a `harvest` token) and assert one violation each; a `frost_anchored` crop returns `[]`.

```python
# tools/test_woody_ornamental_gate.py  (skeleton -- fill the well_formed() fixture)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from woody_ornamental_gate import woody_ornamental_violations

def well_formed():
    return {"calendar_basis":"perennial_woody_ornamental","gating_factors":[],
            "hardiness_zone_min":5,"hardiness_zone_max":9,
            "regions":{"r":{"resolved_by_zone":{
                "6":{"grown_as":"perennial","calendar":["dormant","dormant","dormant","growing",
                     "growing","bloom","bloom","prune","growing","growing","dormant","dormant"]}}}}}

def test_clean(): assert woody_ornamental_violations(well_formed()) == []
def test_noop_off_basis():
    c = well_formed(); c["calendar_basis"]="frost_anchored"
    assert woody_ornamental_violations(c) == []
def test_bad_grown_as():
    c = well_formed(); c["regions"]["r"]["resolved_by_zone"]["6"]["grown_as"]="biennial"
    assert any("grown_as" in v for v in woody_ornamental_violations(c))
def test_prune_in_annual():
    cell = c2 = well_formed()["regions"]["r"]["resolved_by_zone"]["6"]
    c = well_formed(); cell = c["regions"]["r"]["resolved_by_zone"]["6"]
    cell["grown_as"]="annual"  # annual cell must not carry a prune token
    assert any("prune" in v for v in woody_ornamental_violations(c))
def test_tree_key_rejected():
    c = well_formed(); c["rootstock"]="dwarf"
    assert any("rootstock" in v or "tree" in v for v in woody_ornamental_violations(c))
def test_gating_factors_must_be_empty():
    c = well_formed(); c["gating_factors"]=["cold_hardiness"]
    assert any("gating_factors" in v for v in woody_ornamental_violations(c))

if __name__ == "__main__":
    for n,f in sorted(globals().items()):
        if n.startswith("test_") and callable(f): f(); print("ok", n)
    print("ALL PASS")
```

- [ ] **Step 2: Run, verify fail** (`ModuleNotFoundError`).
- [ ] **Step 3: Implement** `woody_ornamental_violations` per the invariants above (model on `tools/berry_herbaceous_gate.py`'s structure: early `return []` off basis; walk `regions[].resolved_by_zone`; collect strings).
- [ ] **Step 4: Run, verify PASS.**
- [ ] **Step 5: Commit** -- `feat(lavender): A12 woody-ornamental structural gate (test-first)`.

---

## Task 3: The release-lane FILL pass (`derive_woody_ornamental_calendars.py`)

**Files:**
- Create: `tools/derive_woody_ornamental_calendars.py`
- Test: `tools/test_derive_woody_ornamental_calendars.py`

**Interfaces:**
- Produces: `fill_woody_ornamental_calendars(crop) -> int` (sets each resolved cell's `calendar = derive_woody_ornamental_calendar(grown_as, cell)`, returns the count filled, skips cells the deriver returns None for); CLI `python3 tools/derive_woody_ornamental_calendars.py <slug> <in.json> <out.json>` writing COMPACT.

- [ ] **Step 1: Write failing test** -- a 2-cell crop (one perennial, one annual) -> `fill_*` returns 2 and each `calendar` equals the deriver's output; a None-yielding cell (empty bloom) is skipped and counted out. Model on `tools/test_derive_berry_calendars.py`.
- [ ] **Step 2: Run, verify fail.**
- [ ] **Step 3: Implement** (mirror `tools/derive_berry_calendars.py`; reuse `derive_woody_ornamental_calendar`; CLI uses `json.dump(..., separators=(",",":"), ensure_ascii=False)`).
- [ ] **Step 4: Run, verify PASS.**
- [ ] **Step 5: Commit** -- `feat(lavender): woody-ornamental calendar FILL pass (test-first)`.

---

## Task 4: Wire A12 + A13 into `whole_crop_gate.py`

**Files:**
- Modify: `tools/whole_crop_gate.py` (immediately after the A11 block, ~line 310).

**Interfaces:**
- Consumes: `woody_ornamental_gate.woody_ornamental_violations`, `woody_ornamental_calendar.woody_ornamental_calendar_violations`.

- [ ] **Step 1: Add the A12/A13 blocks** (symmetric to A10/A11):

```python
# ---------------- A12. woody_ornamental structural cert (no-op off perennial_woody_ornamental) ----------------
from woody_ornamental_gate import woody_ornamental_violations
print("A12. woody_ornamental structural cert (lifecycle + grown_as + prune-placement + guards; no-op off scope)")
_wo = woody_ornamental_violations(crop)
for v in _wo: violations.append(f"A12 {v}")

# ---------------- A13. woody_ornamental calendar coherence (DERIVED-from-dates) ----------------
from woody_ornamental_calendar import woody_ornamental_calendar_violations
print("A13. woody_ornamental calendar coherence (calendar == derive(grown_as, dates); no-op off scope)")
_wocal = woody_ornamental_calendar_violations(crop)
for v in _wocal: violations.append(f"A13 {v}")
```
(Match the EXACT local-variable + `violations.append` convention used by the A10/A11 blocks above lines 298/310 -- read them first and copy the form.)

- [ ] **Step 2: Verify no regression on the certified crops** -- `python3 tools/whole_crop_gate.py strawberry` and `python3 tools/whole_crop_gate.py lemon` still `PASS` (A12/A13 print + no-op). Run `python3 tools/test_woody_ornamental_calendar.py` and `python3 tools/test_woody_ornamental_gate.py` -> still `ALL PASS`.
- [ ] **Step 3: Commit** -- `feat(lavender): wire A12/A13 woody-ornamental gates into whole_crop_gate`.

---

## Task 5: The `build_region_shells` woody-ornamental path

**Files:**
- Modify: `tools/build_region_shells.py` (the `_is_*` dispatch ~line 47; add `_is_woody_ornamental` + `_build_woody_ornamental_shells`).
- Test: `tools/test_build_region_shells.py` (add a case).

**Interfaces:**
- Produces: `_is_woody_ornamental(crop) -> bool` (`calendar_basis == "perennial_woody_ornamental"`); `_build_woody_ornamental_shells(crop)` (transplant-shaped per-region skeleton -- `plant_out`/`bloom` window slots + null `region_notes` + `grown_as: null` + empty `calendar` + `anchoring_urls: {}`, the Step-3.5 admission state). Dispatch checks `_is_woody_ornamental` BEFORE `_is_tree` so the new basis is never caught by the tree path.

- [ ] **Step 1: Write failing test** -- a `perennial_woody_ornamental` crop with empty `regions` -> `build_region_shells` yields all 10 region shells, each with a null `grown_as`, empty `calendar`, null `region_notes`, `anchoring_urls: {}`; assert `_is_woody_ornamental` is checked before `_is_tree` (a woody-ornamental crop does NOT get tree dormancy slots). Model on the berry-herbaceous shell test.
- [ ] **Step 2: Run, verify fail.**
- [ ] **Step 3: Implement** the dispatch line (`if _is_woody_ornamental(crop): return _build_woody_ornamental_shells(crop)` placed beside the `_is_berry_herbaceous` line ~47) + the builder (mirror `_build_berry_herbaceous_shells`: transplant window slots, no fruit/harvest slot, the `prune`-bearing perennial shape needs only the date slots since the deriver computes the calendar at Step 4).
- [ ] **Step 4: Run, verify PASS** (`python3 tools/test_build_region_shells.py`).
- [ ] **Step 5: Commit** -- `feat(lavender): build_region_shells perennial_woody_ornamental path (test-first)`.

---

## Self-Review
- **Spec coverage:** D1 (basis) -> Task 5 builder sets it; D3 (tokens) -> Task 1 deriver; D9 (deriver) -> Task 1; D10 (A12/A13 gates) -> Tasks 2+4; D2 (grown_as) -> validated in Tasks 1/2; the FILL pass (release lane) -> Task 3. D4-D8, D11-D12 are DATA-arc decisions (claude.ai authoring at Steps 1-8), not tooling -- correctly out of this plan.
- **No central token enum** exists (confirmed: `renovation` was never registered in an allowlist; the deriver + gate are the token authority), so no token-registration task is needed -- `prune` is authored by Task 1's deriver and policed by Task 2's gate.
- **No-op safety:** every gate/deriver task includes an off-basis test; Task 4 re-runs the certified crops.
- **Naming consistency:** `woody_ornamental_*` function/file names are symmetric to `berry_*`, so the whole_crop_gate wiring mirrors A10/A11 exactly.

## Execution Handoff
Tooling is built HERE (Claude Code, test-first, this plan). After it lands, the DATA arc runs the strawberry way: claude.ai authors (Steps 1-3 -> 4 region fill -> 6-8 prose), Claude Code releases (verify -> derive via Task 3 -> gate via Task 4 -> promote). Recommended execution: **inline** (superpowers:executing-plans) -- the 5 tasks are tightly coupled siblings best built in one pass with the certified-crop regression check at the end.
