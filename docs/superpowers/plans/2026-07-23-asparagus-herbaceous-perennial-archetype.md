# Asparagus `herbaceous_perennial` Archetype (Design-First) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mint the `herbaceous_perennial` crop archetype + a TDD structural cert gate (A46) and land a staged, newest-standard reference asparagus that proves the shape end to end -- without promoting asparagus into the canonical or certifying it.

**Architecture:** `herbaceous_perennial` is a new archetype label mapping to the existing `frost_anchored` calendar basis (the sweet-corn `warm_season_grass` pattern -- new label, existing calendar machinery, no new deriver). A new archetype-scoped gate `herbaceous_perennial_gate.py` (whole_crop_gate A46) armors the no-replant / establishment / suitability invariants, mirroring the per-archetype gates `berry_herbaceous_gate` / `berries_woody_gate` / `woody_ornamental_gate`. A staged reference asparagus (2 contrasting region cells + a control_ladder + a variety-resistance map) exercises the archetype against the standalone gates.

**Tech Stack:** Python 3 (stdlib only), plain-assert test scripts (`python3 tools/test_*.py`), compact JSON dataset.

## Global Constraints

- Canonical `crops_data_final.json` is **COMPACT** (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline) and **stays byte-untouched this arc** -- asparagus remains a shell; the reference lives in `tools/staging/`. (CLAUDE.md READ-ONLY-on-canonical + design-first scope.)
- **TDD: RED before GREEN.** Every gate defect class is injected into a scratch/fixture and confirmed to bounce before the gate is trusted (CLAUDE.md hard rule).
- No em dashes in consumer copy (commas/colons/semicolons/periods; `--` is fine in docs/code/commits). American English. Temps render `°F`.
- All authored content (variety facts, agronomy numerics, IPM notes, region prose) is **T1-sourced** (.edu / government extension); cite via the `source_catalog` id + `anchoring_urls`.
- Base canonical: `ccf5e890` (origin/main `7923579`). Spec: `docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md`.
- Per-task commits land on `main` **local + unpushed**; the push is Trevor-gated (CLAUDE.md). Checkpoint with Trevor at plan completion.
- Gate number **A46** is free (A45 is the current max; SE-Alaska's reserved A46/A47 were never built).
- The per-variety resistance field is named **`resistance`** (a `{kebab-problem-id: grade}` map; `GRADES = {immune, resistant, tolerant, susceptible}`), validated by `variety_resistance_gate`. (The spec's prose called it `resists:`; the real field is `resistance`.)

## File Structure

- Create: `tools/herbaceous_perennial_gate.py` -- the A46 structural gate (`herbaceous_perennial_violations(crop)`), archetype-scoped no-op.
- Create: `tools/test_herbaceous_perennial_gate.py` -- plain-assert unit tests + RED defect battery.
- Modify: `tools/calendar_basis_gate.py` -- one line in `ARCHETYPE_BASIS`.
- Modify: `tools/test_calendar_basis_gate.py` -- assert the new archetype/basis pairing.
- Modify: `tools/whole_crop_gate.py` -- wire A46 after the A45 block (~line 680). **No `gate_all.py` edit** (it subprocesses whole_crop_gate per certified crop).
- Create: `tools/staging/asparagus_reference.json` -- the staged reference crop (NOT promoted).
- Create: `docs/reviews/notes/2026-07-23/asparagus_a46_red_proof.md` -- the adversarial RED-battery record.

---

### Task 1: Register the `herbaceous_perennial` archetype

**Files:**
- Modify: `tools/calendar_basis_gate.py` (the `ARCHETYPE_BASIS` dict, ends ~line 61)
- Test: `tools/test_calendar_basis_gate.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `ARCHETYPE_BASIS["herbaceous_perennial"] == "frost_anchored"`. `calendar_basis_violations(crop)` now treats a crop with `archetype="herbaceous_perennial"` + `calendar_basis="frost_anchored"` as clean, and flags any other basis under that archetype (D8 dispatch check).

- [ ] **Step 1: Write the failing test**

Append to `tools/test_calendar_basis_gate.py` (before any final `print(...)` summary line; if the file runs bare asserts top-to-bottom, append at end):

```python
# herbaceous_perennial archetype (asparagus GS arc, 2026-07-23)
from calendar_basis_gate import calendar_basis_violations, ARCHETYPE_BASIS
assert ARCHETYPE_BASIS.get("herbaceous_perennial") == "frost_anchored", ARCHETYPE_BASIS.get("herbaceous_perennial")
# clean: herbaceous_perennial on frost_anchored
_hp_ok = {"slug": "asparagus", "archetype": "herbaceous_perennial",
          "calendar_basis": "frost_anchored", "zone_independent": False}
assert calendar_basis_violations(_hp_ok) == [], calendar_basis_violations(_hp_ok)
# dispatch lie: herbaceous_perennial on a tree basis -> violation
_hp_bad = dict(_hp_ok, calendar_basis="perennial_chill_gated")
assert any("herbaceous_perennial" in v for v in calendar_basis_violations(_hp_bad)), calendar_basis_violations(_hp_bad)
print("calendar_basis_gate: herbaceous_perennial pairing OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_calendar_basis_gate.py`
Expected: FAIL on the first new assert -- `AssertionError: None` (archetype not yet registered).

- [ ] **Step 3: Add the archetype registration**

In `tools/calendar_basis_gate.py`, in the `ARCHETYPE_BASIS` dict, add this line after the `"microgreen": "non_seasonal_indoor",` entry (keep the closing `}` on its own line):

```python
    "herbaceous_perennial": "frost_anchored",  # asparagus (+ later artichoke), 2026-07-23: an
    # herbaceous perennial VEGETABLE -- a new archetype label riding the SAME frost_anchored basis +
    # annual calendar machinery (the warm_season_grass pattern), with NO new calendar-layer dispatch.
    # The no-replant / establishment / suitability invariants are carried by the A46
    # herbaceous_perennial_gate, not by the calendar layer. calendar_basis stays frost_anchored so
    # A3 (perennial tree cert) correctly no-ops (proven by chives/mint/bee-balm certifying this way).
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_calendar_basis_gate.py`
Expected: PASS, ending `calendar_basis_gate: herbaceous_perennial pairing OK`.

- [ ] **Step 5: Confirm no roster regression**

Run: `python3 tools/calendar_basis_gate.py crops_data_final.json`
Expected: `calendar_basis gate: 0 violation(s) across 128 crops` (no certified crop uses the new label; asparagus shell has `archetype=None`, exempt from the D8 check).

- [ ] **Step 6: Commit**

```bash
git add tools/calendar_basis_gate.py tools/test_calendar_basis_gate.py
git commit -m "feat(archetype): register herbaceous_perennial -> frost_anchored (asparagus GS arc)"
```

---

### Task 2: Build the A46 `herbaceous_perennial_gate`

**Files:**
- Create: `tools/herbaceous_perennial_gate.py`
- Test: `tools/test_herbaceous_perennial_gate.py`

**Interfaces:**
- Consumes: nothing (reads a `crop` dict).
- Produces: `herbaceous_perennial_violations(crop) -> list[str]` (`[]` = clean); no-op unless `crop["archetype"] == "herbaceous_perennial"`. Exports `SUITABILITY_ENUM = {"perennializes", "marginal", "unsuitable"}`.

- [ ] **Step 1: Write the failing test**

Create `tools/test_herbaceous_perennial_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for the herbaceous_perennial structural cert branch (asparagus GS arc, 2026-07-23).
Run: python3 tools/test_herbaceous_perennial_gate.py

Invariants (docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md):
  - fires ONLY for archetype == 'herbaceous_perennial' (no-op otherwise -- keeps the 119 certified,
    incl. the herbaceous herbs chives/mint on culinary_herb, untouched).
  - perennial true; lifecycle in {perennial, permanent}; succession_policy.suitable False + reason;
    establishment fields sane (years_to_first_harvest non-empty min>=1, years_to_full_production
    non-empty, productive_lifespan_years positive int); no succession/second_planting planting
    tracks; per filled cell: suitability in enum + a marginal/unsuitable cell carries a reason note
    + a non-empty calendar (A32 honesty floor); rotation present.
  - a cell with suitability null AND empty calendar is the admission state (skip).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from herbaceous_perennial_gate import herbaceous_perennial_violations, SUITABILITY_ENUM

def well_formed():
    """Minimal valid herbaceous_perennial crop: one thriving + one unsuitable region cell."""
    return {
        "slug": "asparagus-mini", "archetype": "herbaceous_perennial",
        "calendar_basis": "frost_anchored", "perennial": True, "lifecycle": "perennial",
        "succession_policy": {"suitable": False, "reason_seasoned": "A permanent 15-to-20-year bed is established once, never succession-planted."},
        "years_to_first_harvest": [2, 3], "years_to_full_production": [3, 4],
        "productive_lifespan_years": 18, "rotation": "Permanent bed; do not rotate. Choose the site for the long haul.",
        "regions": {
            "northern_tier": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"4": {"suitability": "perennializes",
                    "calendar": ["cold_pause","cold_pause","cold_pause","harvest","harvest","harvest",
                                 "growing","growing","growing","growing","cold_pause","cold_pause"]}}},
            "hawaii_tropical": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"12": {"suitability": "unsuitable",
                    "suitability_note_seasoned": "Asparagus needs a real winter dormancy it will not get here; it declines instead of perennializing.",
                    "calendar": ["growing","growing","growing","growing","growing","growing",
                                 "growing","growing","growing","growing","growing","growing"]}}}},
    }

# 0. well-formed -> clean
assert herbaceous_perennial_violations(well_formed()) == [], herbaceous_perennial_violations(well_formed())

# 1. off-archetype -> NO-OP even with garbage (chives-style herb stays untouched)
off = {"slug": "chives", "archetype": "culinary_herb", "calendar_basis": "frost_anchored",
       "perennial": True, "lifecycle": "perennial", "regions": {}}
assert herbaceous_perennial_violations(off) == [], "non-herbaceous_perennial crop must be a no-op"

# 2. ADMISSION STATE: unfilled shell cell (suitability null, calendar []) -> skipped
c = well_formed()
c["regions"]["northern_tier"]["resolved_by_zone"]["4"] = {"suitability": None, "calendar": []}
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 3. perennial not true -> violation
c = well_formed(); c["perennial"] = False
assert any("perennial" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 4. lifecycle annual -> violation
c = well_formed(); c["lifecycle"] = "annual"
assert any("lifecycle" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5. succession suitable true -> violation
c = well_formed(); c["succession_policy"]["suitable"] = True
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5b. succession suppressed but no reason -> violation
c = well_formed(); c["succession_policy"]["reason_seasoned"] = None
assert any("reason_seasoned" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6. empty years_to_first_harvest -> violation
c = well_formed(); c["years_to_first_harvest"] = []
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6b. years_to_first_harvest min 0 (no real establishment lag) -> violation
c = well_formed(); c["years_to_first_harvest"] = [0]
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6c. productive_lifespan_years null -> violation
c = well_formed(); c["productive_lifespan_years"] = None
assert any("productive_lifespan_years" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 7. a succession planting track -> violation
c = well_formed(); c["regions"]["northern_tier"]["plantings"].append({"track": "succession", "label": "fill"})
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 8. bad suitability enum on a filled cell -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "fruits_reliably"
assert any("suitability" in v and "fruits_reliably" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 9. unsuitable cell missing the reason note -> violation
c = well_formed(); c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"].pop("suitability_note_seasoned")
assert any("hawaii_tropical" in v and "12" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 10. a suitability-marked cell with an EMPTY calendar (A32 honesty floor) -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["calendar"] = []
assert any("northern_tier" in v and "calendar" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 11. rotation missing -> violation
c = well_formed(); c["rotation"] = None
assert any("rotation" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

assert SUITABILITY_ENUM == {"perennializes", "marginal", "unsuitable"}, SUITABILITY_ENUM
print("herbaceous_perennial_gate: all tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_herbaceous_perennial_gate.py`
Expected: FAIL -- `ModuleNotFoundError: No module named 'herbaceous_perennial_gate'`.

- [ ] **Step 3: Write the gate implementation**

Create `tools/herbaceous_perennial_gate.py`:

```python
#!/usr/bin/env python3
"""Herbaceous-perennial structural cert branch (asparagus GS arc, anchor pilot; later artichoke).
Fires ONLY for archetype == 'herbaceous_perennial' (a no-op otherwise). Imported + run by
whole_crop_gate.py as section A46. The calendar itself is validated by the frost_anchored annual
layer (A5/A24/A28) -- this gate owns the invariants unique to a no-replant perennial VEGETABLE:
the establishment lag, succession suppression, and per-region SUITABILITY honesty (a chill-
dependent crop that will not perennialize in the tropics is marked, not given a fake calendar).

See docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md.
Scoped to archetype (not calendar_basis) so the herbaceous HERBS (chives/mint/bee-balm on
culinary_herb / companion_and_ornamental_flower, ruled 2026-07-05) stay untouched.
"""
SUITABILITY_ENUM = {"perennializes", "marginal", "unsuitable"}


def herbaceous_perennial_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless archetype herbaceous_perennial."""
    if crop.get("archetype") != "herbaceous_perennial":
        return []
    V = []

    # 1. perennial flag (a herbaceous perennial is, definitionally, perennial).
    if crop.get("perennial") is not True:
        V.append(f"perennial must be true for a herbaceous_perennial crop; got {crop.get('perennial')!r}")

    # 2. permanent-bed lifecycle.
    if crop.get("lifecycle") not in ("perennial", "permanent"):
        V.append(f"lifecycle must be perennial|permanent for a herbaceous_perennial crop; "
                 f"got {crop.get('lifecycle')!r}")

    # 3. succession SUPPRESSED with a stated reason (a permanent bed is never succession-planted).
    sp = crop.get("succession_policy") or {}
    if sp.get("suitable") is not False:
        V.append(f"succession_policy.suitable must be false (a permanent bed is not succession-"
                 f"planted); got {sp.get('suitable')!r}")
    elif not sp.get("reason_seasoned"):
        V.append("succession_policy.reason_seasoned must explain why succession is unsuitable")

    # 4. establishment fields sane (the multi-year lag that distinguishes this archetype).
    yfh = crop.get("years_to_first_harvest")
    if not (isinstance(yfh, list) and yfh
            and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in yfh)
            and min(yfh) >= 1):
        V.append(f"years_to_first_harvest must be a non-empty numeric list with min >= 1 (a real "
                 f"establishment lag); got {yfh!r}")
    if not crop.get("years_to_full_production"):
        V.append(f"years_to_full_production must be non-empty; got {crop.get('years_to_full_production')!r}")
    pls = crop.get("productive_lifespan_years")
    if not (isinstance(pls, int) and not isinstance(pls, bool) and pls > 0):
        V.append(f"productive_lifespan_years must be a positive int; got {pls!r}")

    # 5/6. per region: no succession/second_planting tracks; per filled cell: suitability coherence.
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for p in (r.get("plantings") or []):
            if isinstance(p, dict) and p.get("track") in ("succession", "second_planting"):
                V.append(f"{rk}: a permanent bed must not carry a {p.get('track')!r} planting track")
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            suit = cell.get("suitability")
            cal = cell.get("calendar") or []
            if suit is None and not cal:
                continue  # admission state: an unfilled shell cell
            if suit not in SUITABILITY_ENUM:
                V.append(f"{rk}.{z}: suitability {suit!r} not in {sorted(SUITABILITY_ENUM)}")
                continue
            if suit in ("marginal", "unsuitable") and not cell.get("suitability_note_seasoned"):
                V.append(f"{rk}.{z}: a {suit} cell must carry suitability_note_seasoned "
                         f"(the dormancy/chill reason, not a fake calendar)")
            if not cal:
                V.append(f"{rk}.{z}: a suitability-marked cell must carry a non-empty calendar "
                         f"(the A32 honesty floor -- mark unsuitable, still show the honest cycle)")

    # 7. permanent-bed rotation guidance present.
    if crop.get("rotation") in (None, "", []):
        V.append("rotation must be present (a permanent bed's no-rotate guidance)")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in herbaceous_perennial_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
    print(f"herbaceous_perennial gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_herbaceous_perennial_gate.py`
Expected: PASS, ending `herbaceous_perennial_gate: all tests passed`.

- [ ] **Step 5: Confirm no roster regression**

Run: `python3 tools/herbaceous_perennial_gate.py crops_data_final.json`
Expected: `herbaceous_perennial gate: 0 violation(s) across 128 crops` (no crop carries the archetype yet; asparagus shell has `archetype=None`).

- [ ] **Step 6: Commit**

```bash
git add tools/herbaceous_perennial_gate.py tools/test_herbaceous_perennial_gate.py
git commit -m "feat(gate): add herbaceous_perennial structural cert gate (A46, TDD)"
```

---

### Task 3: Wire A46 into `whole_crop_gate`

**Files:**
- Modify: `tools/whole_crop_gate.py` (insert after the A45 block, ~line 680)

**Interfaces:**
- Consumes: `herbaceous_perennial_violations` (Task 2).
- Produces: an `A46.` section in the always-on suite; `gate_all` picks it up automatically (it subprocesses whole_crop_gate per certified crop).

- [ ] **Step 1: Insert the A46 wiring block**

In `tools/whole_crop_gate.py`, find the end of the A45 block:

```python
print("A45. region zone_span parity (expected span + resolved_by_zone key parity + donor integrity)")
_zsp = _zonespan_violations(crop)
print(f"  zone_span violations: {len(_zsp)}")
for m in _zsp:
    fail(f"zone-span: {m}")
```

Immediately AFTER that block (before the `# ---------------- A24.` comment), insert:

```python

# ---------------- A46. herbaceous_perennial structural cert (asparagus GS arc, 2026-07-23) ----------------
# The no-replant perennial VEGETABLE archetype (asparagus, later artichoke): a new label on the
# frost_anchored basis (so A3 tree-cert correctly no-ops), with its own structural armor for the
# invariants the calendar layer does not cover -- establishment lag, succession suppression, and
# per-region SUITABILITY honesty (a chill-dependent crop marked unsuitable in the tropics, not given
# a fake calendar). Scoped to archetype == 'herbaceous_perennial' -> no-op on all 119 certified
# (incl. the herbaceous herbs chives/mint, which stay culinary_herb per the 2026-07-05 ruling).
from herbaceous_perennial_gate import herbaceous_perennial_violations
print("A46. herbaceous_perennial structural cert (establishment + succession + suitability; no-op off scope)")
_hpv = herbaceous_perennial_violations(crop)
print(f"  archetype={crop.get('archetype')!r} | herbaceous_perennial violations: {len(_hpv)}")
for m in _hpv:
    fail(f"herbaceous-perennial: {m}")
```

- [ ] **Step 2: Verify the wiring runs + no-ops on a certified crop**

Run: `python3 tools/whole_crop_gate.py chives crops_data_final.json | grep -E "A46|GATE:"`
Expected: a line `A46. herbaceous_perennial structural cert ...` followed later by `GATE: PASS` -- chives is `culinary_herb`, so A46 reports `0` violations and chives still passes.

- [ ] **Step 3: Confirm the full certified roster is unperturbed**

Run: `python3 tools/gate_all.py crops_data_final.json`
Expected: `gate_all: PASS -- every certified crop passes the whole suite` (119 certified; A46 no-ops on every one).

- [ ] **Step 4: Commit**

```bash
git add tools/whole_crop_gate.py
git commit -m "feat(gate): wire A46 herbaceous_perennial into whole_crop_gate"
```

---

### Task 4: Author the staged reference asparagus (newest-standard bar)

**Files:**
- Create: `tools/staging/asparagus_reference.json`

**Interfaces:**
- Consumes: the `control_methods` catalog ids (existing), the A46 gate (Task 2), `control_ladder_gate`, `variety_resistance_gate`.
- Produces: a single crop dict `{ "crop": { ...asparagus... } }` that passes all three standalone gates. Referenced by Task 5.

> **This is a content-authoring task** -- a sourcing-capable subagent authors the T1 values into the skeleton below. The **structure, ids, method references, and grades are fixed by this plan** (so the ladder/resistance gates pass referentially); the **prose (`note_*`, `hero_description`, `suitability_note_*`, `region_notes_*`), agronomy numerics, and `sources`/`anchoring_urls`** are authored from T1 extension sources (UC ANR, U.Minn/Michigan/Illinois Extension, Cornell). No em dashes in consumer copy; American English; `°F`.

- [ ] **Step 1: Write the reference skeleton**

Create `tools/staging/asparagus_reference.json` with this exact structure. Author every `"<T1 ...>"` marker from a cited source; keep all ids/methods/grades verbatim.

```json
{"crop": {
  "slug": "asparagus",
  "name": "Asparagus",
  "category": "Fruiting Veg",
  "type": "crop",
  "archetype": "herbaceous_perennial",
  "calendar_basis": "frost_anchored",
  "perennial": true,
  "lifecycle": "perennial",
  "difficulty": "medium",
  "start_method": {"start": "transplant", "notes_seasoned": "<T1: crowns are the standard start; seed adds a year>", "notes_beginner": "<T1: plant one-year-old crowns>"},
  "succession_policy": {"suitable": false, "reason_seasoned": "<T1: a permanent 15-to-20-year bed is established once, never succession-planted>"},
  "years_to_first_harvest": [2, 3],
  "years_to_full_production": [3, 4],
  "productive_lifespan_years": 18,
  "rotation": "<T1: permanent bed; do not rotate; choose a long-term site>",
  "planting_layout": {"pattern": "rows", "row_spacing_inches": [48, 60], "in_row_spacing_inches": [12, 18]},
  "varieties": {"recommended": [
    {"id": "millennium", "name": "Millennium", "is_reference": true, "confidence_tier": "T1",
     "hero_description": "<T1: cold-hardy all-male hybrid, the modern high-yield standard>",
     "note_beginner": "<T1 dual-register>", "note_seasoned": "<T1 dual-register>",
     "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}},
     "resistance": {"asparagus-rust": "resistant", "fusarium-crown-rot": "resistant"}},
    {"id": "jersey-knight", "name": "Jersey Knight", "is_reference": false, "confidence_tier": "T1",
     "hero_description": "<T1: all-male Jersey-series hybrid>",
     "note_beginner": "<T1>", "note_seasoned": "<T1>",
     "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}},
     "resistance": {"asparagus-rust": "tolerant", "fusarium-crown-rot": "tolerant"}},
    {"id": "mary-washington", "name": "Mary Washington", "is_reference": false, "confidence_tier": "T1",
     "hero_description": "<T1: the open-pollinated heirloom standard>",
     "note_beginner": "<T1>", "note_seasoned": "<T1>",
     "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}}},
    {"id": "purple-passion", "name": "Purple Passion", "is_reference": false, "confidence_tier": "T1",
     "hero_description": "<T1: sweeter, tender purple spears>",
     "note_beginner": "<T1>", "note_seasoned": "<T1>",
     "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}}}
  ], "note_beginner": "<T1>", "note_seasoned": "<T1>", "sources": ["<catalog_id>"], "anchoring_urls": {}},
  "pests": [
    {"id": "asparagus-beetle", "type": "insect", "name": "Asparagus beetles (common and spotted)",
     "control_ladder": [
       {"method": "garden_sanitation", "note_beginner": "<T1: cut and remove old ferns in fall; the beetles overwinter in the debris>", "note_seasoned": "<T1>"},
       {"method": "handpick", "note_beginner": "<T1: pick off beetles and knock eggs from spears>"},
       {"method": "floating_row_cover", "note_beginner": "<T1>", "note_seasoned": "<T1>"},
       {"method": "beneficial_predators", "note_beginner": "<T1: a tiny native wasp parasitizes the eggs; ladybugs and lacewings help>"},
       {"method": "spinosad", "note_beginner": "<T1: an organic option once softer rungs have not held; spray at dusk to spare bees>", "note_seasoned": "<T1>"},
       {"method": "pyrethroid", "note_beginner": "<T1: a conventional rescue only; a pyrethroid such as permethrin, harmful to bees and fish, read the label>", "note_seasoned": "<T1>"}
     ]}
  ],
  "diseases": [
    {"id": "asparagus-rust", "type": "disease", "name": "Asparagus rust (Puccinia asparagi)",
     "control_ladder": [
       {"method": "resistant_varieties", "note_beginner": "<T1: start with a rust-resistant all-male hybrid>"},
       {"method": "airflow_spacing", "note_beginner": "<T1: wider rows and full sun dry the ferns faster>"},
       {"method": "garden_sanitation", "note_beginner": "<T1: remove and destroy infected ferns in fall>"},
       {"method": "sulfur", "note_beginner": "<T1: a protectant fungicide on the ferns if rust is chronic; do not use above 90°F>", "note_seasoned": "<T1>"}
     ]},
    {"id": "fusarium-crown-rot", "type": "disease", "name": "Fusarium crown and root rot",
     "control_ladder": [
       {"method": "resistant_varieties", "note_beginner": "<T1: all-male hybrids carry the best Fusarium tolerance>"},
       {"method": "garden_sanitation", "note_beginner": "<T1: do not replant asparagus into an old asparagus bed; choose a fresh, well-drained site>", "note_seasoned": "<T1: avoid replant sites; Fusarium persists in soil>"}
     ]}
  ],
  "regions": {
    "northern_tier": {
      "region_id": "northern_tier", "region_label": "<from canonical>",
      "plantings": [{"succession_id": 1, "label": "crowns", "track": "perennial"}],
      "resolved_by_zone": {"4": {
        "suitability": "perennializes",
        "calendar": ["cold_pause","cold_pause","cold_pause","harvest","harvest","harvest","growing","growing","growing","growing","cold_pause","cold_pause"],
        "resolution_method": "frost_anchored_resolved",
        "notes": "<T1: spear harvest window opens as soil warms; stop cutting after 6-to-8 weeks and let ferns grow>",
        "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}}}},
      "region_notes_beginner": "<T1>", "region_notes_seasoned": "<T1>"
    },
    "hawaii_tropical": {
      "region_id": "hawaii_tropical", "region_label": "<from canonical>",
      "plantings": [{"succession_id": 1, "label": "crowns", "track": "perennial"}],
      "resolved_by_zone": {"12": {
        "suitability": "unsuitable",
        "suitability_note_seasoned": "<T1: asparagus needs a real winter dormancy it will not reliably get here; it declines rather than perennializing>",
        "suitability_note_beginner": "<T1: not recommended; asparagus needs a cold winter rest>",
        "calendar": ["growing","growing","growing","growing","growing","growing","growing","growing","growing","growing","growing","growing"],
        "resolution_method": "frost_anchored_resolved",
        "sources": ["<catalog_id>"], "anchoring_urls": {"<catalog_id>": {"url": "<T1 url>"}}}},
      "region_notes_beginner": "<T1>", "region_notes_seasoned": "<T1>"
    }
  }
}}
```

> **Authoring notes:**
> - Confirm the `calendar` tokens (`cold_pause`, `harvest`, `growing`) are in the frost_anchored annual enum (check `tools/annual_calendar.py`); adjust dormancy/harvest month placement to the zone's real frost dates.
> - Pull `region_label` / `zone_span` verbatim from the canonical's existing shell cells so they match A45's `EXPECTED_SPANS`.
> - If a Fusarium ladder rung needs a "well-drained site / no-replant" cultural method with no existing catalog home, add ONE new `control_methods` entry authored from a fetched T1 page (never broaden a method on an unsupported claim) -- and note it for the authoring arc's catalog add. Prefer reusing `garden_sanitation` as skeletoned if the T1 source supports it.
> - All four grades used (`resistant`/`tolerant`) are in `variety_resistance_gate.GRADES`; both resistance keys (`asparagus-rust`, `fusarium-crown-rot`) match `diseases[].id`, so the referential check passes.

- [ ] **Step 2: Validate against the three standalone gates**

```bash
python3 - <<'PY'
import json, sys, os
sys.path.insert(0, "tools")
from herbaceous_perennial_gate import herbaceous_perennial_violations
from control_ladder_gate import check_crop as ladder_check   # confirm the fn name via: grep -n "^def " tools/control_ladder_gate.py
from variety_resistance_gate import resistance_violations
crop = json.load(open("tools/staging/asparagus_reference.json"))["crop"]
cat = json.load(open("crops_data_final.json")).get("control_methods", {})
print("A46:", herbaceous_perennial_violations(crop))
print("resistance:", resistance_violations(crop))
# control_ladder_gate signature: pass the crop (+ catalog if required) -- see its check_crop def.
PY
```
Expected: `A46: []` and `resistance: []`. For the ladder gate, run `python3 tools/control_ladder_gate.py` per its `__main__` usage against a scratch canonical carrying the reference (built in Task 5), or call its `check_crop` with the catalog per its signature; expect 0 violations. (Verify the exact `control_ladder_gate` entry-point with `grep -n "def check\|def .*violations\|__main__" tools/control_ladder_gate.py` before wiring the call.)

- [ ] **Step 3: Commit**

```bash
git add tools/staging/asparagus_reference.json
git commit -m "content(asparagus): staged herbaceous_perennial reference (2 cells + ladder + resistance)"
```

---

### Task 5: Adversarial verification + footprint proof

**Files:**
- Create: `docs/reviews/notes/2026-07-23/asparagus_a46_red_proof.md`

**Interfaces:**
- Consumes: the reference (Task 4), the gates (Tasks 1-3).
- Produces: the RED-proof record + the green-verification summary.

- [ ] **Step 1: Run the A46 RED battery on the REAL reference shape**

Per CLAUDE.md ("a gate isn't done until a defect has been sneaked at it and caught"), inject each defect class into the staged reference and confirm A46 bounces it:

```bash
python3 - <<'PY'
import json, copy, sys
sys.path.insert(0, "tools")
from herbaceous_perennial_gate import herbaceous_perennial_violations as V
base = json.load(open("tools/staging/asparagus_reference.json"))["crop"]
assert V(base) == [], ("clean reference must pass", V(base))
defects = {
  "perennial_false": lambda c: c.update(perennial=False),
  "lifecycle_annual": lambda c: c.update(lifecycle="annual"),
  "succession_suitable": lambda c: c["succession_policy"].update(suitable=True),
  "no_reason": lambda c: c["succession_policy"].update(reason_seasoned=None),
  "yfh_empty": lambda c: c.update(years_to_first_harvest=[]),
  "yfh_zero": lambda c: c.update(years_to_first_harvest=[0]),
  "pls_null": lambda c: c.update(productive_lifespan_years=None),
  "succession_track": lambda c: c["regions"]["northern_tier"]["plantings"].append({"track":"succession"}),
  "bad_suitability": lambda c: c["regions"]["northern_tier"]["resolved_by_zone"]["4"].update(suitability="fruits_reliably"),
  "unsuitable_no_note": lambda c: c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"].pop("suitability_note_seasoned"),
  "empty_calendar": lambda c: c["regions"]["northern_tier"]["resolved_by_zone"]["4"].update(calendar=[]),
  "rotation_null": lambda c: c.update(rotation=None),
}
for name, mutate in defects.items():
    c = copy.deepcopy(base); mutate(c)
    assert V(c), f"defect {name} was NOT caught"
    print(f"  bounced: {name}")
print("A46 RED battery: all defect classes caught")
PY
```
Expected: 12 `bounced:` lines + `A46 RED battery: all defect classes caught`.

- [ ] **Step 2: Confirm gate_all still 119/119 and the canonical is byte-untouched**

```bash
python3 tools/gate_all.py crops_data_final.json
git status --porcelain crops_data_final.json
shasum -a 256 crops_data_final.json | grep -q ccf5e890 && echo "canonical UNTOUCHED (ccf5e890)" || echo "CANONICAL CHANGED -- STOP"
```
Expected: `gate_all: PASS`; empty `git status` line for the canonical; `canonical UNTOUCHED (ccf5e890)`.

- [ ] **Step 3: Write the RED-proof note**

Create `docs/reviews/notes/2026-07-23/asparagus_a46_red_proof.md` recording: the 12 defect classes + that each bounced; the clean-reference pass; the 3 standalone-gate greens (A46 / control_ladder / variety_resistance); `gate_all` 119/119; canonical untouched. Note the design-first boundary (2 of 16 regions authored; full roster + cert deferred to the follow-on arc).

- [ ] **Step 4: Commit**

```bash
git add docs/reviews/notes/2026-07-23/asparagus_a46_red_proof.md
git commit -m "docs(asparagus): A46 RED-proof + design-first verification record"
```

- [ ] **Step 5: Checkpoint with Trevor**

Summarize: archetype registered, A46 built + RED-proven + wired, staged reference passes the standalone gates, roster still 119/119, canonical untouched. Confirm before any push. State the next arc: full authoring + 16-region fan-out + certification to 120, then artichoke on the same archetype.

---

## Self-Review

**1. Spec coverage:**
- Archetype registration (spec §2) -> Task 1. ✓
- New TDD structural gate A46 with the 7-invariant contract + RED battery (spec §3) -> Task 2 (unit) + Task 5 (adversarial on real shape). ✓
- Suitability marker + honest calendar, no A32 carve-out (spec §4) -> A46 invariant #6 (Task 2) + reference cells (Task 4). ✓
- Reference asparagus to newest-standard bar: 2 cells + control_ladder + varieties + resistance (spec §5) -> Task 4. ✓
- Variety light path (recommended + hero + resistance; defer sex-ratio archetype) (spec §6) -> Task 4 skeleton (no per-variety DTM/gate). ✓
- Deferred items (spec §7) -> not built; Task 5 Step 5 states the next arc. ✓
- Verification: A46 RED, standalone gates, gate_all 119/119, canonical untouched (spec §8) -> Task 5 + Task 4 Step 2. ✓
- Wiring: whole_crop_gate only, gate_all auto (spec §8) -> Task 3 (+ noted no gate_all edit). ✓

**2. Placeholder scan:** Tasks 1-3 + Task 5 contain complete code/commands. Task 4's `"<T1 ...>"` markers are **content-authoring targets** (a data-authoring task cannot pre-embed T1 values without doing the sourcing), not code placeholders -- the structure, ids, methods, and grades are fully specified so the gates pass referentially. Two entry-point lookups are flagged inline (`control_ladder_gate` signature) with the exact `grep` to resolve them at execution.

**3. Type consistency:** `herbaceous_perennial_violations(crop)` and `SUITABILITY_ENUM` names match across Tasks 2/3/5. The variety field is `resistance` (not `resists`) everywhere. `GRADES` values (`resistant`/`tolerant`) match `variety_resistance_gate`. Calendar tokens (`cold_pause`/`harvest`/`growing`) flagged for enum confirmation in Task 4.
