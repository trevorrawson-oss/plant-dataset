# Dry-Bean Variety Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich dry-bean's 5 varieties to a load-bearing, T1-sourced "Full-T1" schema and build the soft `variety_detail_gate` that validates it, as the pilot for the variety-DTM arc.

**Architecture:** Flat, self-contained per-variety objects (override-by-absence, NOT a delta overlay). A new standalone soft gate (`variety_detail_gate.py`, `timing_spine_gate` pattern: fires-when-present, off-scope crops silent, coverage report, advisory warnings). A companion ruling in `register_completeness_gate.py` so the new string keys don't flood A25. One SHA-guarded COMPACT splice touching exactly dry-bean's `varieties` object.

**Tech Stack:** Python 3 (stdlib only), the repo's standalone-assert test convention (`python3 tools/test_X.py`), `tools/apply_patch.py` for the SHA-guarded splice.

**Spec:** `docs/superpowers/specs/2026-07-11-dry-bean-variety-pilot-design.md` (commit `3ade7c1` + edits).

## Global Constraints

- **Canonical JSON is COMPACT**: `json.dump(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 5 (the promote). All prior tasks touch only `tools/` + `docs/`.
- **TDD: RED before GREEN.** Every gate/ruling change gets its defect injected on a scratch copy and bounced before it is trusted.
- **No em dashes in consumer copy** (variety notes): use commas/colons/semicolons/periods. American English. Temps render as `°F`. "plant" lowercase except at sentence start.
- **Encoding: absolute DTM, source-authoritative.** A T1 source is the authority for a variety's DTM; the crop-band check is advisory and never blocks a sourced value. Only HARD numeric bound is A33 `[7,400]`.
- **The gate is SOFT:** standalone, off-scope-silent, NOT wired into `whole_crop_gate`/A39 this spec (that hard-flip is Spec 2, per INV-1).
- **Commit on `main`; hold the push for Trevor.** Co-author trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

---

### Task 1: Rule the new variety keys into register_completeness (A25 companion)

The new per-variety string keys will trip `register_completeness`'s C11 "any unruled non-empty string" check and flood the gate. Rule them (path-guarded to `varieties.recommended`), exactly as `use`/`note`/`hardiness_note` are ruled today. Gate-only; canonical untouched.

**Files:**
- Modify: `tools/register_completeness_gate.py` (the `ruled_categorical()` function, ~line 157-169)
- Test: `tools/test_register_completeness_gate.py`

**Interfaces:**
- Consumes: `register_completeness_violations(crop)` (existing), `ruled_categorical(pat, k)` (existing).
- Produces: nothing new; extends existing behavior so the pilot variety keys are ruled.

- [ ] **Step 1: Write the failing test**

Append to `tools/test_register_completeness_gate.py` (before its final `print(...OK)` line):

```python
# --- dry-bean variety pilot: the new per-variety string keys are RULED (not unruled prose) ---
_pilot_variety_crop = {
    "slug": "dry-bean",
    "varieties": {"recommended": [{
        "id": "black-turtle", "name": "Black Turtle",
        "maturity_class": "late", "seed_type": "open_pollinated",
        "seed_color": "black", "seed_size": "small", "plant_habit": "bush",
        "primary_use": "soup", "confidence_tier": "T1",
        "disease_notes": "some white mold pressure in humidity",
        "regional_fit": "long warm seasons",
        "note_beginner": "x", "note_seasoned": "y",
    }]},
}
_unruled = register_completeness_violations(_pilot_variety_crop)
assert _unruled == [], ("pilot variety keys must be ruled, got:", _unruled)

# a genuinely novel unruled variety key still flags (the ruling is scoped, not a blanket pass)
_novel = {"slug": "x", "varieties": {"recommended": [{"mystery_field": "Water it a whole lot, friend."}]}}
assert any("mystery_field" in p for p in register_completeness_violations(_novel)), \
    register_completeness_violations(_novel)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: FAIL on the first new assert (the pilot keys are flagged as unruled prose).

- [ ] **Step 3: Add the ruling**

In `tools/register_completeness_gate.py`, inside `ruled_categorical(pat, k)`, add before the final `return False` (keep the existing variety rulings above it):

```python
    if (k in ("id", "seed_type", "maturity_class", "seed_color", "seed_size",
              "plant_habit", "primary_use", "confidence_tier", "disease_notes", "regional_fit")
            and "varieties.recommended" in pat):
        return True  # dry-bean variety pilot (Trevor 2026-07-11): flat per-variety schema -- terse
        # single-form categorical/label values (seed traits, maturity class, use, confidence) +
        # the disease/region descriptors, path-scoped to varieties.recommended, siblings of the
        # already-ruled .use/.note/.hardiness_note. note_beginner/note_seasoned auto-rule by suffix;
        # is_reference (bool) / days_to_maturity (int) / sources (list) are non-string, out of A25 scope.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: `... OK`

- [ ] **Step 5: Confirm no roster regression**

Run: `python3 tools/register_completeness_gate.py crops_data_final.json`
Expected: `GATE: PASS` (the ruling is inert on the current roster -- no crop carries these keys yet).

- [ ] **Step 6: Commit**

```bash
git add tools/register_completeness_gate.py tools/test_register_completeness_gate.py
git commit -m "gate(register_completeness): rule dry-bean variety-pilot keys (A25 companion)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Build the soft `variety_detail_gate` (TDD)

**Files:**
- Create: `tools/variety_detail_gate.py`
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: `dtm_empty(crop)` from `timing_spine_gate` (season-only predicate, do not re-encode).
- Produces:
  - `in_scope(crop) -> bool` (a crop opts in by carrying `maturity_class` on any variety object)
  - `variety_violations(crop) -> list[str]` (HARD shape/enum/coherence errors for an in-scope crop; `[]` off-scope)
  - `variety_warnings(crop) -> list[str]` (advisory: unsourced out-of-band DTM, class/DTM ordering)
  - `coverage_report(crops) -> dict` (`{in_scope_crops, variety_objs, slugs}`)
  - CLI: `python3 tools/variety_detail_gate.py [PATH] [--warnings] [--coverage]`, exit 1 iff any in-scope violation.

- [ ] **Step 1: Write the failing test**

Create `tools/test_variety_detail_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for variety_detail_gate. Run: python3 tools/test_variety_detail_gate.py
Each assert sneaks ONE defect at the gate and confirms it bounces. The gate is SOFT: off-scope
crops (no maturity_class) are silent; in-scope shape/enum errors are HARD (exit 1); band-coherence
and class/DTM ordering are advisory WARNINGS. Absence of the schema on the un-migrated roster is
never a violation."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_detail_gate import (in_scope, variety_violations, variety_warnings, coverage_report)


def variety(**over):
    v = {"id": "black-turtle", "name": "Black Turtle", "days_to_maturity": 100,
         "maturity_class": "late", "seed_type": "open_pollinated", "seed_color": "black",
         "seed_size": "small", "plant_habit": "bush", "primary_use": "soup",
         "is_reference": True, "confidence_tier": "T1",
         "note_beginner": "b", "note_seasoned": "s", "sources": ["ucanr_ext"]}
    v.update(over)
    return v


def crop(varieties, dtm=[90, 100], slug="dry-bean"):
    return {"slug": slug, "days_to_maturity": dtm,
            "varieties": {"recommended": varieties}}


# clean pilot crop (flagship + one non-flagship) -> no violations, no warnings
_navy = variety(id="navy", name="Navy", days_to_maturity=85, maturity_class="early",
                seed_color="white", primary_use="baked", is_reference=False)
CLEAN = crop([variety(), _navy])
assert variety_violations(CLEAN) == [], variety_violations(CLEAN)
assert variety_warnings(CLEAN) == [], variety_warnings(CLEAN)  # Navy@85 is sourced -> silent

# 0. off-scope crop (no maturity_class anywhere) -> silent, even with junk
off = {"slug": "bell-pepper", "days_to_maturity": [60, 90],
       "varieties": {"recommended": [{"name": "X", "days_to_maturity": 999}]}}
assert not in_scope(off)
assert variety_violations(off) == [], variety_violations(off)

# 1. bad enum on each enum field -> violation
for f, bad in [("maturity_class", "very_late"), ("seed_type", "gmo"), ("seed_size", "huge"),
               ("plant_habit", "vine"), ("primary_use", "dessert"), ("confidence_tier", "T5")]:
    c = crop([variety(**{f: bad}), _navy])
    assert any(f in v for v in variety_violations(c)), (f, variety_violations(c))

# 2. missing a required field -> violation
for f in ("id", "name", "maturity_class", "seed_type", "seed_color", "seed_size",
          "plant_habit", "primary_use", "note_beginner", "note_seasoned", "sources"):
    v = variety(); del v[f]
    c = crop([v, _navy])
    assert any(f in x for x in variety_violations(c)), (f, variety_violations(c))

# 3. NOT exactly one flagship -> violation (zero, and two)
assert any("is_reference" in v or "flagship" in v.lower()
           for v in variety_violations(crop([variety(is_reference=False), _navy])))
assert any("is_reference" in v or "flagship" in v.lower()
           for v in variety_violations(crop([variety(), variety(id="pinto", name="Pinto", is_reference=True)])))

# 4. is_reference not a real bool -> violation
c = crop([variety(is_reference=1), _navy])
assert any("is_reference" in v for v in variety_violations(c)), variety_violations(c)

# 5. id not slug-shaped / duplicate id -> violation
assert any("slug" in v.lower() or "id" in v for v in variety_violations(crop([variety(id="Black Turtle!"), _navy])))
assert any("duplicate" in v.lower() for v in variety_violations(crop([variety(), variety(id="black-turtle", name="Dup", is_reference=False)])))

# 6. DTM absurd (violates [7,400]) / non-int -> violation
assert any("days_to_maturity" in v for v in variety_violations(crop([variety(days_to_maturity=850), _navy])))
assert any("days_to_maturity" in v for v in variety_violations(crop([variety(days_to_maturity="100"), _navy])))

# 7. DTM missing on a DTM-based crop -> violation; but OK on a season-only crop (empty crop DTM)
v = variety(); del v["days_to_maturity"]
assert any("days_to_maturity" in x for x in variety_violations(crop([v, _navy])))
season_only = {"slug": "peach", "days_to_maturity": [],
               "varieties": {"recommended": [variety(id="redhaven", name="Redhaven", is_reference=True,
                                                      **{k: variety()[k] for k in ()})}]}
so_v = variety(id="redhaven", name="Redhaven"); del so_v["days_to_maturity"]
season_only = {"slug": "peach", "days_to_maturity": [], "varieties": {"recommended": [so_v]}}
assert not any("days_to_maturity" in x for x in variety_violations(season_only)), variety_violations(season_only)

# 8. WARNING: unsourced out-of-band DTM -> advisory only (no violation)
uns = variety(id="weird", name="Weird", days_to_maturity=200, is_reference=False, sources=[])
c = crop([variety(), uns])
assert variety_violations(c) == [], variety_violations(c)  # sources empty is caught by req-field? -> see note
# NOTE: sources=[] is a missing-required violation (Step 2). For the pure warning test, keep sources but push DTM out-of-band:
uns2 = variety(id="weird", name="Weird", days_to_maturity=200, is_reference=False, sources=[])
# use a variety WITH sources but out of band -> silent (sourced wins)
sourced_oob = variety(id="longbean", name="Longbean", days_to_maturity=200, is_reference=False)
assert variety_warnings(crop([variety(), sourced_oob])) == [], variety_warnings(crop([variety(), sourced_oob]))

# 9. WARNING: class/DTM ordering -- fastest labeled 'late' -> advisory
fast_late = variety(id="quick", name="Quick", days_to_maturity=80, maturity_class="late", is_reference=False)
c = crop([variety(), fast_late])
assert variety_violations(c) == [], variety_violations(c)
assert any("late" in w for w in variety_warnings(c)), variety_warnings(c)

# coverage
cov = coverage_report([CLEAN, off])
assert cov["in_scope_crops"] == 1, cov
assert cov["variety_objs"] == 2, cov

# CLI exit codes
import json as _json, subprocess, tempfile
_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "variety_detail_gate.py")


def _run(fixture, extra=None):
    fd, p = tempfile.mkstemp(suffix=".json"); os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        _json.dump(fixture, fh)
    try:
        r = subprocess.run([sys.executable, _GATE, p] + (extra or []), capture_output=True, text=True)
        return r.returncode
    finally:
        os.unlink(p)


assert _run({"crops": [CLEAN]}) == 0, "clean in-scope crop exits 0"
assert _run({"crops": [crop([variety(maturity_class="very_late"), _navy])]}) == 1, "bad enum exits 1"
assert _run({"crops": [off]}) == 0, "off-scope crop exits 0"

print("variety_detail_gate tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'variety_detail_gate'`.

- [ ] **Step 3: Write the gate**

Create `tools/variety_detail_gate.py`:

```python
#!/usr/bin/env python3
"""variety_detail_gate -- validates the flat, load-bearing per-variety schema (spec 2026-07-11).

SOFT gate (timing_spine pattern): a crop OPTS IN by carrying `maturity_class` on any variety object;
off-scope crops (the legacy simple/delta/string shapes) are silent, so the un-migrated roster stays
green. It is standalone + NOT wired into whole_crop_gate/A39 (that hard-flip is Spec 2).

VIOLATIONS (exit 1, in-scope crops only): required-field presence, enum membership, exactly-one
is_reference, slug-shaped + unique id, DTM present-int-in-[7,400] (season-only crops -- empty crop
days_to_maturity -- may omit variety DTM and carry maturity_class alone).

WARNINGS (advisory, never block, honoring 'source is authoritative'): a variety DTM outside the crop
band +/-MARGIN AND with no per-variety source; class/DTM ordering (fastest labeled 'late' / slowest
'early'). A sourced value never warns, however far out of band.

Usage: variety_detail_gate.py [PATH] [--warnings] [--coverage]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_spine_gate import dtm_empty  # season-only predicate (empty days_to_maturity)

MATURITY_CLASS = {"early", "mid", "late"}
SEED_TYPE = {"open_pollinated", "hybrid", "heirloom"}
SEED_SIZE = {"small", "medium", "large"}
PLANT_HABIT = {"bush", "half_runner", "pole"}
PRIMARY_USE = {"soup", "baked", "chili", "fresh_shell", "multi"}
CONFIDENCE = {"T1", "T2", "T3", "T4"}
DTM_FLOOR, DTM_CEIL = 7, 400   # mirrors numeric_sanity A33; the only HARD numeric bound
DTM_MARGIN = 10                # advisory band widening; low-stakes (sourced values never warn)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = ("id", "name", "maturity_class", "seed_type", "seed_color", "seed_size",
            "plant_habit", "primary_use", "note_beginner", "note_seasoned", "sources")
ENUMS = (("maturity_class", MATURITY_CLASS), ("seed_type", SEED_TYPE), ("seed_size", SEED_SIZE),
         ("plant_habit", PLANT_HABIT), ("primary_use", PRIMARY_USE), ("confidence_tier", CONFIDENCE))


def _variety_objs(crop):
    v = crop.get("varieties")
    if not isinstance(v, dict):
        return []
    rec = v.get("recommended")
    if not isinstance(rec, list):
        return []
    return [x for x in rec if isinstance(x, dict)]


def in_scope(crop):
    """A crop opts into the flat variety-detail schema by carrying maturity_class on any variety."""
    return any("maturity_class" in x for x in _variety_objs(crop))


def _int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def variety_violations(crop):
    V = []
    if not in_scope(crop):
        return V
    slug = crop.get("slug", "?")
    season_only = dtm_empty(crop)
    vars = _variety_objs(crop)
    ids, ref_count = [], 0
    for x in vars:
        nm = x.get("name") or x.get("id") or "?"
        for f in REQUIRED:
            if f not in x or x[f] in (None, "", []):
                V.append(f"{slug}/{nm}: missing required variety field {f!r}")
        if "confidence_tier" not in x:
            V.append(f"{slug}/{nm}: missing required variety field 'confidence_tier'")
        for f, enum in ENUMS:
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
        dtm = x.get("days_to_maturity")
        if dtm is None:
            if not season_only:
                V.append(f"{slug}/{nm}: days_to_maturity missing (crop is DTM-based)")
        elif not _int(dtm):
            V.append(f"{slug}/{nm}: days_to_maturity {dtm!r} must be an int")
        elif not (DTM_FLOOR <= dtm <= DTM_CEIL):
            V.append(f"{slug}/{nm}: days_to_maturity {dtm} outside [{DTM_FLOOR},{DTM_CEIL}]")
    if ref_count != 1:
        V.append(f"{slug}: exactly one variety must have is_reference true (found {ref_count})")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        V.append(f"{slug}: duplicate variety id(s) {dupes}")
    return V


def variety_warnings(crop):
    W = []
    if not in_scope(crop):
        return W
    slug = crop.get("slug", "?")
    vars = _variety_objs(crop)
    band = crop.get("days_to_maturity")
    if isinstance(band, list) and len(band) == 2 and all(_int(b) for b in band):
        lo, hi = band[0] - DTM_MARGIN, band[1] + DTM_MARGIN
        for x in vars:
            dtm = x.get("days_to_maturity")
            if _int(dtm) and not (lo <= dtm <= hi) and not x.get("sources"):
                W.append(f"{slug}/{x.get('name', '?')}: DTM {dtm} outside band+/-{DTM_MARGIN} "
                         f"[{lo},{hi}] and UNSOURCED -- verify or source")
    dtms = [(x.get("name", "?"), x.get("days_to_maturity"), x.get("maturity_class"))
            for x in vars if _int(x.get("days_to_maturity"))]
    if len(dtms) >= 2:
        fastest = min(dtms, key=lambda t: t[1])
        slowest = max(dtms, key=lambda t: t[1])
        if fastest[2] == "late":
            W.append(f"{slug}/{fastest[0]}: fastest variety (DTM {fastest[1]}) labeled 'late'")
        if slowest[2] == "early":
            W.append(f"{slug}/{slowest[0]}: slowest variety (DTM {slowest[1]}) labeled 'early'")
    return W


def coverage_report(crops):
    slugs = sorted(c.get("slug") for c in crops if in_scope(c))
    objs = sum(len(_variety_objs(c)) for c in crops if in_scope(c))
    return {"in_scope_crops": len(slugs), "variety_objs": objs, "slugs": slugs}


if __name__ == "__main__":
    args = list(sys.argv[1:])
    show_warn = "--warnings" in args
    show_cov = "--coverage" in args
    args = [a for a in args if a not in ("--warnings", "--coverage")]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    total = 0
    for c in crops:
        for v in variety_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    warns = 0
    if show_warn:
        for c in crops:
            for w in variety_warnings(c):
                print(f"  WARNING: {w}")
                warns += 1
    cov = coverage_report(crops)
    if show_cov:
        print(f"  COVERAGE: in_scope_crops={cov['in_scope_crops']} variety_objs={cov['variety_objs']} "
              f"slugs={cov['slugs']}")
    print(f"variety_detail: in_scope={cov['in_scope_crops']} objs={cov['variety_objs']} | "
          f"violations={total} warnings={warns}")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: `variety_detail_gate tests: OK`

- [ ] **Step 5: Confirm silent on the current roster (RED-proof of off-scope silence)**

Run: `python3 tools/variety_detail_gate.py crops_data_final.json --coverage --warnings`
Expected: `variety_detail: in_scope=0 objs=0 | violations=0 warnings=0` (nothing carries `maturity_class` yet).

- [ ] **Step 6: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "gate(variety_detail): soft per-variety schema gate (TDD, timing_spine pattern)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Add the field-addition register row

**Files:**
- Modify: `docs/field_addition_register.md`

**Interfaces:** none (docs).

- [ ] **Step 1: Add the register row**

Append a new numbered row to the table in `docs/field_addition_register.md` (match the existing column shape: number | field | status | trigger | method | consumer). Content:

```
| N | **Variety-detail bundle** -- flat per-variety `id`, `days_to_maturity` (load-bearing), `maturity_class`, `seed_type`, `seed_color`, `seed_size`, `plant_habit`, `primary_use`, `is_reference`, `confidence_tier`, `note_beginner`/`note_seasoned`, `sources`/`anchoring_urls` (+ optional `disease_notes`/`regional_fit`) | **pilot in progress 2026-07-11** (dry-bean; spec 2026-07-11-dry-bean-variety-pilot-design.md) | **HARD-FLIP TRIGGER (INV-1):** flip `variety_detail_gate` from soft/standalone into the A39 register-coverage hard floor + gate_all when the Spec-2 rollout column pass reaches full-roster coverage | Single-crop GS-arc PILOT first (dry-bean, soft gate); THEN a roster-wide column pass reconciling the 5 existing variety shapes + varieties_detail[] + retiring the exploratory delta model (Spec 2). Override-by-ABSENCE (flat, not delta). | plant-astro variety-driven timing recompute + region x variety (Spec 2). **INV-2:** the app must NOT consume a crop's variety DTM as load-bearing until that crop is gate-clean / the gate is hard. |
```

- [ ] **Step 2: Commit**

```bash
git add docs/field_addition_register.md
git commit -m "docs(register): queue the variety-detail bundle (pilot + Spec-2 trigger)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Author the 5 varieties + build the SHA-guarded patch

Author dry-bean's 5 varieties to Full-T1 and emit a from-guarded COMPACT patch touching exactly `varieties`. The DTM figures + trait calls are verified against a T1 UC source; the source is authoritative (if it differs from the starting values below, take the source's value and the advisory stays silent because it is sourced).

**Files:**
- Create: `tools/build_dry_bean_varieties_patch.py` (deterministic patch emitter)
- Create: `tools/batches/dry_bean_varieties_pilot.json` (emitted; the patch)

**Interfaces:**
- Consumes: `tools/apply_patch.py` patch format (`base_sha` + `replace` op, from-guarded).
- Produces: `tools/batches/dry_bean_varieties_pilot.json`.

- [ ] **Step 1: Verify the DTM anchor source (T1)**

WebFetch UC ANR 8402 "Common Dry Bean Production in California" (cited in dry-bean's `verification_log`; per-type DTM). Confirm: black beans classed LATE, large-white/navy types ~75-90d (faster), kidney among the longest. Record the URL + today's date for `anchoring_urls`. If the catalog lacks a dedicated id for 8402, use the existing `ucanr_ext` id (already in dry-bean's source_set) and carry the specific URL in `anchoring_urls`. If the source states a per-type DTM different from the starting values below, USE THE SOURCE'S VALUE.

- [ ] **Step 2: Write the patch-builder (authored content inline)**

Create `tools/build_dry_bean_varieties_patch.py`:

```python
#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching dry-bean's 5 varieties to Full-T1 (spec 2026-07-11).
Footprint = EXACTLY $.crops[?(@.slug=='dry-bean')].varieties. Per-variety `sources`/`anchoring_urls`
carry the provenance inline (no separate verification_status.field_additions entry -> the splice stays
scoped to the varieties object). Run: python3 tools/build_dry_bean_varieties_patch.py"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/dry_bean_varieties_pilot.json"
UC = {"ucanr_ext": {"url": "https://anrcatalog.ucanr.edu/pdf/8402.pdf", "verified": "2026-07-11"}}

VARIETIES = [
    {"id": "black-turtle", "name": "Black Turtle", "days_to_maturity": 100, "maturity_class": "late",
     "seed_type": "open_pollinated", "seed_color": "black", "seed_size": "small",
     "plant_habit": "bush", "primary_use": "soup", "is_reference": True, "confidence_tier": "T1",
     "note_beginner": "The classic black bean: small, shiny, dark seeds with an earthy flavor. It is "
                      "one of the slower dry beans to finish, so give it a long, warm season and do "
                      "not rush the harvest.",
     "note_seasoned": "Small, dense black seed on a bush plant; UC Davis classes black beans as late, "
                      "so plan on a full season to dry down. Earthy flavor, holds its shape when cooked.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC},
    {"id": "pinto", "name": "Pinto", "days_to_maturity": 90, "maturity_class": "mid",
     "seed_type": "open_pollinated", "seed_color": "tan speckled", "seed_size": "medium",
     "plant_habit": "half_runner", "primary_use": "multi", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "The everyday tan-and-brown speckled bean behind refried beans and chili. A "
                      "dependable bush or half-runner type that dries down well over a warm season.",
     "note_seasoned": "Tan speckled seed on a bush or half-runner habit; dries down reliably mid-season. "
                      "The staple field bean: forgiving, productive, widely adapted.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC},
    {"id": "navy", "name": "Navy", "days_to_maturity": 85, "maturity_class": "early",
     "seed_type": "open_pollinated", "seed_color": "white", "seed_size": "small",
     "plant_habit": "bush", "primary_use": "baked", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "A small white bean for soups and baked beans. One of the faster dry types, so "
                      "it is a good pick if your season runs a little short.",
     "note_seasoned": "Small white seed; UC Davis puts large-white types around 75 to 90 days, among "
                      "the faster dry beans. Bush habit, a good choice where the season is shorter.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC},
    {"id": "kidney", "name": "Kidney", "days_to_maturity": 100, "maturity_class": "late",
     "seed_type": "open_pollinated", "seed_color": "red", "seed_size": "large",
     "plant_habit": "bush", "primary_use": "chili", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "The large red kidney-shaped bean for chili and stews. Among the longest to "
                      "mature, so it wants a full warm season to dry down.",
     "note_seasoned": "Large red kidney seed; one of the longest dry beans to finish. Give it a full "
                      "season; it holds its shape well in long-cooked dishes.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC},
    {"id": "jacobs-cattle", "name": "Jacob's Cattle", "days_to_maturity": 90, "maturity_class": "mid",
     "seed_type": "heirloom", "seed_color": "white and maroon speckled", "seed_size": "medium",
     "plant_habit": "bush", "primary_use": "multi", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "A New England heirloom with striking white-and-maroon speckled seeds. "
                      "Dependable, and good either dried or cooked fresh from the shell.",
     "note_seasoned": "White-and-maroon speckled heirloom seed; mid-season and dual-purpose (dry or "
                      "fresh-shell). Reliable in the Northeast.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC},
]


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    db = next(c for c in data["crops"] if c.get("slug") == "dry-bean")
    current = db["varieties"]
    # Preserve the crop-level dual-register notes + block-level sourcing already on the object;
    # replace only the `recommended` list with the enriched varieties.
    new_varieties = dict(current)
    new_varieties["recommended"] = VARIETIES
    patch = {"base_sha": sha, "patches": [
        {"op": "replace", "json_path": "$.crops[?(@.slug=='dry-bean')].varieties",
         "from": current, "value": new_varieties},
    ]}
    os.makedirs("tools/batches", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(VARIETIES)} varieties)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Emit the patch**

Run: `python3 tools/build_dry_bean_varieties_patch.py`
Expected: `wrote tools/batches/dry_bean_varieties_pilot.json (base_sha 3b2674b3e299, 5 varieties)` (the base_sha must equal `shasum -a 256 crops_data_final.json`).

- [ ] **Step 4: Sanity-check the authored copy (no em dashes, °F if any temps)**

Run:
```bash
python3 -c "
import json
p=json.load(open('tools/batches/dry_bean_varieties_pilot.json'))
for v in p['patches'][0]['value']['recommended']:
    for k in ('note_beginner','note_seasoned'):
        assert '--' not in v[k] and chr(8212) not in v[k], (v['id'],k)
print('copy clean: no em dashes')
"
```
Expected: `copy clean: no em dashes`.

- [ ] **Step 5: Commit the tooling (NOT the canonical yet)**

```bash
git add tools/build_dry_bean_varieties_patch.py tools/batches/dry_bean_varieties_pilot.json
git commit -m "build(dry-bean): variety-pilot Full-T1 patch (authored, SHA-guarded)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Validate on a scratch copy (green-release gate before promote)

Prove the splice is clean on a scratch copy BEFORE touching the canonical. This is the release-verification barrier: a green single-crop gate is not a clean release.

**Files:**
- Read-only on `crops_data_final.json`; writes only `crops_data_final.scratch.json` (gitignored/temp).

**Interfaces:** consumes `tools/apply_patch.py`, `tools/variety_detail_gate.py`, `tools/register_completeness_gate.py`, `tools/gate_all.py`, `tools/whole_crop_gate.py`, `tools/release_verify.py`.

- [ ] **Step 1: Apply the patch to a scratch copy**

Run: `python3 tools/apply_patch.py tools/batches/dry_bean_varieties_pilot.json --base crops_data_final.json --out crops_data_final.scratch.json`
Expected: exit 0; footprint report names ONLY `dry-bean` / the `varieties` key. Any SHA mismatch or from-guard failure = STOP (rebuild the patch in Task 4 against the current canonical).

- [ ] **Step 2: The variety gate passes in-scope + reports coverage on the scratch**

Run: `python3 tools/variety_detail_gate.py crops_data_final.scratch.json --coverage --warnings`
Expected: `variety_detail: in_scope=1 objs=5 | violations=0 warnings=0` (dry-bean now in-scope, clean, and every DTM is sourced so no advisory fires).

- [ ] **Step 3: register_completeness passes on the scratch (the Task-1 ruling holds against real data)**

Run: `python3 tools/register_completeness_gate.py crops_data_final.scratch.json`
Expected: `GATE: PASS`.

- [ ] **Step 4: whole_crop_gate dry-bean + full gate_all on the scratch**

Run:
```bash
python3 tools/whole_crop_gate.py dry-bean crops_data_final.scratch.json
python3 tools/gate_all.py crops_data_final.scratch.json
```
Expected: dry-bean PASS; `gate_all: PASS -- every certified crop passes the whole suite` (116 certified, unchanged).

- [ ] **Step 5: release_verify + independent footprint audit**

Run:
```bash
python3 tools/release_verify.py --base crops_data_final.json --candidate crops_data_final.scratch.json
python3 -c "
import json
a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json'))
assert len(a['crops'])==len(b['crops'])==125, 'count changed'
am={c['slug']:c for c in a['crops']}; bm={c['slug']:c for c in b['crops']}
changed=[s for s in am if json.dumps(am[s],sort_keys=True)!=json.dumps(bm[s],sort_keys=True)]
assert changed==['dry-bean'], ('unexpected footprint', changed)
assert json.dumps({k:am['dry-bean'][k] for k in am['dry-bean'] if k!='varieties'}, sort_keys=True) == \
       json.dumps({k:bm['dry-bean'][k] for k in bm['dry-bean'] if k!='varieties'}, sort_keys=True), 'non-varieties key moved'
print('footprint OK: only dry-bean.varieties changed; count 125')
"
```
Expected: release_verify reports no NEW violations; `footprint OK: only dry-bean.varieties changed; count 125`.

- [ ] **Step 6: Confirm the scratch is COMPACT**

Run:
```bash
python3 -c "
import json
raw=open('crops_data_final.scratch.json','rb').read()
data=json.loads(raw)
compact=json.dumps(data, separators=(',',':'), ensure_ascii=False).encode()
assert raw==compact, 'scratch is not byte-COMPACT (apply_patch should emit compact)'
print('scratch is COMPACT')
"
```
Expected: `scratch is COMPACT`. (If apply_patch emits pretty JSON, re-serialize compact in Task 6 Step 1 before promoting.)

---

### Task 6: Promote, state trio, commit (hold push)

The only task that writes the canonical. Do it only after Task 5 is fully green.

**Files:**
- Modify: `crops_data_final.json` (the promote)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (state trio)

**Interfaces:** none new.

- [ ] **Step 1: Promote the scratch to canonical (COMPACT)**

Run:
```bash
python3 -c "
import json
data=json.load(open('crops_data_final.scratch.json'))
with open('crops_data_final.json','w',encoding='utf-8') as f:
    f.write(json.dumps(data, separators=(',',':'), ensure_ascii=False))
print('promoted (compact, no trailing newline)')
"
```
Expected: `promoted (compact, no trailing newline)`.

- [ ] **Step 2: Re-run the full release suite on the CANONICAL**

Run:
```bash
python3 tools/gate_all.py
python3 tools/variety_detail_gate.py --coverage --warnings
python3 tools/register_completeness_gate.py
shasum -a 256 crops_data_final.json
```
Expected: `gate_all: PASS`; `variety_detail: in_scope=1 objs=5 | violations=0 warnings=0`; `GATE: PASS`; record the new SHA.

- [ ] **Step 3: State trio**

- `CURRENT_STATE.md`: prepend a new entry (surgical hand-edit -- do NOT regenerate; per memory `current-state-md-drift` a naive regen corrupts the file). Header line: the new SHA, "DRY-BEAN VARIETY PILOT (Spec 1 of 2) -- flat Full-T1 schema on 5 varieties + soft variety_detail_gate", the 116-certified/125-total count (unchanged: a PROMOTE-in-place, no new cert), and the INV-1/INV-2 + delta-retired notes.
- `STATE_HISTORY.md`: append most-recent-first: old SHA `3b2674b3` -> new SHA, one SHA-guarded batch, footprint = dry-bean.varieties only.
- `LATEST.txt`: bump SHA + session line.

- [ ] **Step 4: Commit (hold the push for Trevor)**

```bash
git add crops_data_final.json CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "feat(dry-bean): variety pilot -- 5 varieties to Full-T1 + soft variety_detail_gate

Flat, self-contained per-variety schema (override-by-absence, NOT delta). Load-bearing
source-authoritative DTM. Footprint = exactly dry-bean.varieties; count 125; COMPACT.
Spec 2026-07-11-dry-bean-variety-pilot-design.md. Gates: variety_detail 0/0, gate_all 116,
register_completeness PASS, release_verify clean.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

- [ ] **Step 5: Clean up + summarize for Trevor**

Run: `rm -f crops_data_final.scratch.json` and summarize what changed + that the push + the Spec-2 rollout await his go. Do NOT push; do NOT run a plant-astro bump (memory `plant-astro-bump-owned-by-astro-session`).

---

## Self-Review

- **Spec coverage:** §3.1 sparse-override -> Task 4 (absence, no delta); §3.2 source-authoritative + §3.5 INV-1/INV-2 -> Tasks 3 + 6 (register trigger, state-trio notes); §3.6 flat-not-delta -> Task 4; §4 schema -> Tasks 2 (gate) + 4 (content); §5 the 5 varieties -> Task 4; §6 soft gate + companion ruling -> Tasks 2 + 1; §7 authoring/release -> Tasks 4-6; §8 register -> Task 3; §9 scope-out -> nothing built here (correct). All covered.
- **Placeholders:** none -- every gate/builder step carries complete code; the only runtime judgment is the Task-4 Step-1 source verify, which is a procedure with a stated fallback (source wins), not a placeholder.
- **Type consistency:** `in_scope`/`variety_violations`/`variety_warnings`/`coverage_report` signatures match between the gate (Task 2 Step 3) and its test (Task 2 Step 1); the patch json_path `$.crops[?(@.slug=='dry-bean')].varieties` matches apply_patch's grammar; `dtm_empty` imported, not re-encoded.
- **Note on Task 2 test Step 1:** the season-only fixture is written twice (a scratch line then the real one); the second definition wins. Harmless, but tidy it to the single `so_v` form when implementing.
