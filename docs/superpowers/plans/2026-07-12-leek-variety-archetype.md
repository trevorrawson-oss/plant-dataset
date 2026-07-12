# Leek Variety Archetype (Winter-Hardiness Engine) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Intended to run in a FRESH session; start by reading the memory `onion-variety-pilot-photoperiod` + `shallot-variety-dtm-held` + this plan's spec.

**Goal:** Add the `hardiness_annual` archetype (a 4th) to the archetype-dispatched `variety_detail_gate`, build a NEW standalone `overwinter_hardiness_gate` (the reusable winter-hardiness honesty engine), and enrich leek's 6 varieties + a crop-level `winter_hardiness` model so the app can say, per zone, which leeks you can overwinter.

**Architecture:** Leek is the 4th variety archetype (after dry-bean `annual_dtm`, apple `tree_fruit`, onion `photoperiod_annual`). Unlike onion (which REUSED the existing A9 engine), leek's honesty engine does not exist, so this is an ENGINE BUILD: a one-line `variety_detail_gate` dispatch add for the variety shape, PLUS a new standalone `overwinter_hardiness_gate` for the region-zone coupling honesty. The engine asserts overwintering viability by zone (NOT grows-or-fails), reads the region's existing USDA zone (no new region data), and is structured so garlic/artichoke inherit the zone-coupling machinery (the vernalization RULE is designed separately). Content ships via a SHA-guarded COMPACT splice mirroring the onion builder, with a Trevor source-manifest sign-off.

**Tech Stack:** Python 3 (stdlib), standalone assert-based test files (run directly, not pytest), the repo's existing gate + apply_patch tooling.

**Spec:** `docs/superpowers/specs/2026-07-12-leek-variety-archetype-design.md`
**Memory:** `onion-variety-pilot-photoperiod`, `shallot-variety-dtm-held`, `trevor-north-star-accuracy-authority`

## Global Constraints

- **Canonical JSON is COMPACT**: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 5 (the promote splice). Tasks 1-4 touch only tooling + tests + a scratch copy.
- **TDD: RED before GREEN.** Both gate pieces get failing tests first; adversarially proven on a scratch copy of real leek (Task 3) before content is trusted.
- **No em dashes in consumer copy** (variety prose + the crop-level `winter_hardiness` explainer): commas/colons/semicolons/periods. `--` is fine in code/docs/commits. American English. Temps as `°F`.
- **T1-or-it-does-not-ship** for load-bearing values (per-variety `days_to_maturity`, `cold_hardiness_class`, `min_temp_f`, the crop-level model). Non-T1 -> Trevor manifest sign-off before the splice. `min_temp_f` is **T1-sourced-or-OMITTED, never fabricated** (the shallot lesson). Leek hardiness IS sourceable (primary trait), so expect a real T1 spine.
- **Per-variety `sources`/`anchoring_urls` are T1-only** (whole_crop_gate E.source-tier fails any non-T1; leek is certified). Any T2 datapoint's honesty lives in `confidence_tier` + prose + the crop-level model, never a cited non-T1 source.
- **Separation of concerns:** `variety_detail_gate` validates the variety SHAPE (enum, `min_temp_f` band, DTM); `overwinter_hardiness_gate` validates the HONESTY (coverage, window-fit). Neither duplicates the other. Neither is wired into `whole_crop_gate`/A39 this spec (INV-1 hard-flip = Spec 2).
- **Release verification before promote** (protocol #6): `whole_crop_gate leek` + `variety_detail_gate` + `overwinter_hardiness_gate` + `gate_all` + `release_verify --slug leek` + source-truth sample.
- **State trio at release:** CURRENT_STATE.md (surgical prepend -- no `---` separator, `current-state-md-drift`), STATE_HISTORY.md (prepend), LATEST.txt (SHA + session).
- **Canonical count stays 125.** Leek enriches its existing 6 varieties, adds no crops. Footprint = leek's `varieties` + `variety_archetype` + a new crop-level `winter_hardiness` object + a `gating_factors` `winter_hardiness` token + `verification_status.source_set`; all other crops byte-identical.
- **No plant-astro submodule bump from this session.** Trevor confirms the push.

---

## File Structure

- `tools/variety_detail_gate.py` (modify) -- add `hardiness_annual` to the archetype dispatch (4-way), add the `COLD_HARDINESS` enum + `HARDINESS_TRAITS`/`HARDINESS_ENUMS`, add `hardiness_annual` to `DTM_ARCHETYPES`, add `_hardiness_checks` (min_temp_f band, allows negatives).
- `tools/test_variety_detail_gate.py` (modify) -- add hardiness fixtures + dispatch/enum/DTM/min_temp_f asserts; keep dry-bean + apple + onion asserts green.
- `tools/overwinter_hardiness_gate.py` (create) -- the NEW standalone engine gate (coverage + window-fit; opt-in via the `winter_hardiness` gating token; imports `COLD_HARDINESS`/`_variety_objs`/`_int` from `variety_detail_gate` to avoid enum duplication).
- `tools/test_overwinter_hardiness_gate.py` (create) -- coverage/window-fit/scope asserts + CLI exit-code checks.
- `tools/build_leek_varieties_patch.py` (create) -- emit the SHA-guarded COMPACT patch (mirror `build_onion_varieties_patch.py`): 6 varieties + the crop-level `winter_hardiness` model + `variety_archetype` + the `gating_factors` token.
- `tools/batches/leek_varieties_pilot.json` (create, generated) -- the patch file.
- `docs/field_addition_register.md` (modify) -- row 15 (hardiness-variety bundle + engine, INV-1 trigger).
- `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (modify at release).

---

## Task 1: `variety_detail_gate` -- add the `hardiness_annual` archetype (4-way dispatch + min_temp_f)

**Files:**
- Modify: `tools/variety_detail_gate.py`
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: existing `archetype()`, `_variety_objs`, `in_scope`, `_int`, `dtm_empty`, `variety_violations`, `variety_warnings`, the `ARCHETYPE_TRAITS`/`ARCHETYPE_ENUMS`/`DTM_ARCHETYPES` dispatch tables, `_dtm_checks`.
- Produces: `archetype(crop)` now also returns `"hardiness_annual"`; `COLD_HARDINESS = {"tender","hardy","very_hardy"}` (imported by Task 2); `variety_violations` validates `cold_hardiness_class` enum + `min_temp_f` band for `hardiness_annual` and runs the shared DTM check. Annual/photoperiod/tree behavior unchanged.

- [ ] **Step 1: Write the failing tests**

Add to `tools/test_variety_detail_gate.py` (after the photoperiod fixtures/asserts). Add `archetype` to the top-level import if not already present.

```python
def hvar(**over):
    v = {"id": "lancelot", "name": "Lancelot", "maturity_class": "mid", "is_reference": True,
         "confidence_tier": "T1", "note_beginner": "b", "note_seasoned": "s", "sources": ["cornell_ext"],
         "days_to_maturity": 110, "cold_hardiness_class": "hardy", "use": "all-purpose"}
    v.update(over)
    return v

def hcrop(varieties, slug="leek"):
    return {"slug": slug, "variety_archetype": "hardiness_annual", "days_to_maturity": [90, 150],
            "varieties": {"recommended": varieties}}

_kingrichard = hvar(id="king-richard", name="King Richard", cold_hardiness_class="tender",
                    days_to_maturity=80, maturity_class="early", use="early fresh use", is_reference=False)

# dispatch
assert archetype(hcrop([hvar()])) == "hardiness_annual"

# clean hardiness crop -> no violations
H_CLEAN = hcrop([hvar(), _kingrichard])
assert variety_violations(H_CLEAN) == [], variety_violations(H_CLEAN)

# hardiness does NOT require bean traits, tree fields, or day_length_type
assert not any(("seed_type" in v or "bloom_group" in v or "day_length_type" in v)
               for v in variety_violations(H_CLEAN)), variety_violations(H_CLEAN)

# bad cold_hardiness_class enum -> violation
assert any("cold_hardiness_class" in v
           for v in variety_violations(hcrop([hvar(cold_hardiness_class="arctic"), _kingrichard])))

# missing required hardiness field (cold_hardiness_class / use) -> violation
for f in ("cold_hardiness_class", "use"):
    v = hvar(); del v[f]
    assert any(f in x for x in variety_violations(hcrop([v, _kingrichard]))), (f,)

# hardiness IS a DTM archetype: missing DTM -> violation; absurd DTM -> violation
v = hvar(); del v["days_to_maturity"]
assert any("days_to_maturity" in x for x in variety_violations(hcrop([v, _kingrichard])))
assert any("days_to_maturity" in x for x in variety_violations(hcrop([hvar(days_to_maturity=900), _kingrichard])))

# min_temp_f: NEGATIVE is valid (very hardy), absurd out-of-band bounces
assert variety_violations(hcrop([hvar(cold_hardiness_class="very_hardy", min_temp_f=-10), _kingrichard])) == [], \
    variety_violations(hcrop([hvar(cold_hardiness_class="very_hardy", min_temp_f=-10), _kingrichard]))
assert any("min_temp_f" in v for v in variety_violations(hcrop([hvar(min_temp_f=200), _kingrichard])))

# class/DTM coherence warning applies (fastest labeled 'late')
fast_late = hvar(id="q", name="Q", days_to_maturity=80, maturity_class="late", is_reference=False)
assert any("late" in w for w in variety_warnings(hcrop([hvar(), fast_late]))), variety_warnings(hcrop([hvar(), fast_late]))
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL -- `archetype(...)` returns `"annual_dtm"` for the hardiness crop (the token is unknown), so `H_CLEAN` reports spurious missing bean traits (`seed_type` etc.) and no `cold_hardiness_class` enforcement.

- [ ] **Step 3: Add the hardiness constants + dispatch + checks in `tools/variety_detail_gate.py`**

After the photoperiod constants block (the `DAY_LENGTH`/`PHOTOPERIOD_TRAITS`/`PHOTOPERIOD_ENUMS` lines), add:

```python
# hardiness_annual (leek) archetype
COLD_HARDINESS = {"tender", "hardy", "very_hardy"}
HARDINESS_TRAITS = ("cold_hardiness_class", "use")
HARDINESS_ENUMS = (("cold_hardiness_class", COLD_HARDINESS),)
MIN_TEMP_FLOOR, MIN_TEMP_CEIL = -40, 60   # plausible low-temp band; ALLOWS negatives (very hardy)
```

Extend the dispatch tables (the `ARCHETYPE_TRAITS`/`ARCHETYPE_ENUMS`/`DTM_ARCHETYPES` lines):

```python
ARCHETYPE_TRAITS = {"annual_dtm": ANNUAL_TRAITS, "photoperiod_annual": PHOTOPERIOD_TRAITS,
                    "hardiness_annual": HARDINESS_TRAITS, "tree_fruit": TREE_TRAITS}
ARCHETYPE_ENUMS = {"annual_dtm": ANNUAL_ENUMS, "photoperiod_annual": PHOTOPERIOD_ENUMS,
                   "hardiness_annual": HARDINESS_ENUMS, "tree_fruit": TREE_ENUMS}
DTM_ARCHETYPES = ("annual_dtm", "photoperiod_annual", "hardiness_annual")
```

Update `archetype()` to admit the new token:

```python
    return a if a in ("annual_dtm", "photoperiod_annual", "hardiness_annual", "tree_fruit") else "annual_dtm"
```

Replace the check-dispatch block (currently `if arch in DTM_ARCHETYPES: ... elif arch == "tree_fruit": ...`) with:

```python
        if arch in DTM_ARCHETYPES:
            V += _dtm_checks(slug, nm, x, season_only)
        if arch == "tree_fruit":
            V += _tree_checks(slug, nm, x)
        elif arch == "hardiness_annual":
            V += _hardiness_checks(slug, nm, x)
```

Add the `_hardiness_checks` helper (beside `_tree_checks`):

```python
def _hardiness_checks(slug, nm, x):
    """min_temp_f (optional): an int in [MIN_TEMP_FLOOR, MIN_TEMP_CEIL]. ALLOWS negatives for very hardy
    types -- do NOT reuse the tree positive-int chill validator."""
    V = []
    mt = x.get("min_temp_f")
    if mt is not None and (not _int(mt) or not (MIN_TEMP_FLOOR <= mt <= MIN_TEMP_CEIL)):
        V.append(f"{slug}/{nm}: min_temp_f {mt!r} must be an int in [{MIN_TEMP_FLOOR},{MIN_TEMP_CEIL}]")
    return V
```

Do NOT change `variety_warnings`: its tree branch returns early for `tree_fruit`; every non-tree archetype (annual_dtm, photoperiod_annual, AND hardiness_annual) correctly falls through to the shared band + class/DTM warnings, which leek (crop DTM `[90,150]` + per-variety DTM + maturity_class) needs.

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS -- `variety_detail_gate tests: OK` (all existing annual/photoperiod/tree asserts + the new hardiness asserts).

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "feat(variety-gate): add hardiness_annual archetype (4-way dispatch, min_temp_f band)"
```

---

## Task 2: `overwinter_hardiness_gate` -- the winter-hardiness honesty engine (NEW standalone gate)

**Files:**
- Create: `tools/overwinter_hardiness_gate.py`
- Test: `tools/test_overwinter_hardiness_gate.py`

**Interfaces:**
- Consumes: `variety_detail_gate.COLD_HARDINESS`, `variety_detail_gate._variety_objs`, `variety_detail_gate._int` (imported, to avoid enum/logic duplication).
- Produces: `in_scope(crop)` (True iff `winter_hardiness` in `gating_factors`); `hardiness_violations(crop)` (coverage: >=2 distinct valid hardiness classes among recommended); `hardiness_warnings(crop)` (window-fit: very_hardy!=early, tender!=late); `coverage_report(crops)`; CLI exit 1 on violations.

- [ ] **Step 1: Write the failing tests**

Create `tools/test_overwinter_hardiness_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for overwinter_hardiness_gate. Run: python3 tools/test_overwinter_hardiness_gate.py

SOFT + standalone (variety_detail_gate pattern): a crop opts in via `winter_hardiness` in gating_factors;
off-scope crops are silent. Violations = coverage (an opted-in overwintering crop must recommend >=2
hardiness classes). Warnings = window-fit (a very_hardy overwintering type should not be 'early'; a tender
summer type should not be 'late'). Shape (enum/min_temp_f/DTM) is variety_detail_gate's job, NOT re-checked.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overwinter_hardiness_gate import in_scope, hardiness_violations, hardiness_warnings, coverage_report


def hv(**over):
    v = {"id": "lancelot", "name": "Lancelot", "cold_hardiness_class": "hardy", "maturity_class": "mid"}
    v.update(over)
    return v


def crop(varieties, gating=("winter_hardiness",), slug="leek"):
    return {"slug": slug, "gating_factors": list(gating), "varieties": {"recommended": varieties}}


_tender = hv(id="king-richard", name="King Richard", cold_hardiness_class="tender", maturity_class="early")
_vhardy = hv(id="bandit", name="Bandit", cold_hardiness_class="very_hardy", maturity_class="late")

# in scope only when the token is present
assert in_scope(crop([hv()])) is True
assert in_scope(crop([hv()], gating=())) is False

# off-scope crop -> silent (no violations, no warnings)
assert hardiness_violations(crop([hv()], gating=())) == []
assert hardiness_warnings(crop([hv()], gating=())) == []

# clean: spans >=2 classes, coherent windows -> no violations, no warnings
CLEAN = crop([_tender, hv(), _vhardy])
assert hardiness_violations(CLEAN) == [], hardiness_violations(CLEAN)
assert hardiness_warnings(CLEAN) == [], hardiness_warnings(CLEAN)

# coverage gap: a single hardiness class on an opted-in crop -> violation
assert any("hardiness class" in v for v in hardiness_violations(crop([hv(), hv(id="a", name="A")])))

# window-fit WARNING: very_hardy labeled 'early'
assert any("very_hardy" in w for w in hardiness_warnings(crop([_tender, hv(id="x", name="X", cold_hardiness_class="very_hardy", maturity_class="early")])))

# window-fit WARNING: tender labeled 'late'
assert any("tender" in w for w in hardiness_warnings(crop([hv(), hv(id="y", name="Y", cold_hardiness_class="tender", maturity_class="late")])))

# coverage_report counts in-scope crops + objs
cov = coverage_report([CLEAN])
assert cov["in_scope_crops"] == 1 and cov["variety_objs"] == 3, cov

print("overwinter_hardiness_gate tests: OK")
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 tools/test_overwinter_hardiness_gate.py`
Expected: FAIL -- `ModuleNotFoundError: No module named 'overwinter_hardiness_gate'` (the gate does not exist yet).

- [ ] **Step 3: Write the gate**

Create `tools/overwinter_hardiness_gate.py`:

```python
#!/usr/bin/env python3
"""overwinter_hardiness_gate -- the winter-hardiness / overwintering honesty engine (spec 2026-07-12).

SOFT + standalone (timing_spine / variety_detail pattern). A crop OPTS IN via `winter_hardiness` in
gating_factors; off-scope crops are silent. It validates that a crop's per-variety cold-hardiness data
COHERES with an overwintering claim; it does NOT generate the per-region app claim (that is plant-astro,
INV-2). The zone-coupling machinery is reusable (garlic/artichoke inherit it); the survives-cold
viability RULE here is leek-specific -- vernalization (needs-cold) is designed separately.

Separation of concerns: variety SHAPE (cold_hardiness_class enum, min_temp_f band, DTM) is
variety_detail_gate's job and is NOT re-checked here. This gate checks HONESTY only:
  VIOLATIONS (exit 1, in-scope crops): COVERAGE -- the recommended set spans >=2 distinct hardiness
    classes (so the app can recommend a grow-anywhere summer type AND at least one overwintering type).
  WARNINGS (advisory): WINDOW-FIT -- a `very_hardy` variety labeled maturity_class `early`, or a
    `tender` variety labeled `late` (hardiness class should cohere with season length).

Usage: overwinter_hardiness_gate.py [PATH] [--warnings] [--coverage]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_detail_gate import COLD_HARDINESS, _variety_objs  # reuse enum + variety extractor (DRY)


def in_scope(crop):
    """A crop opts into the hardiness engine by declaring `winter_hardiness` in gating_factors."""
    return "winter_hardiness" in (crop.get("gating_factors") or [])


def hardiness_violations(crop):
    V = []
    if not in_scope(crop):
        return V
    slug = crop.get("slug", "?")
    classes = {x.get("cold_hardiness_class") for x in _variety_objs(crop)
               if x.get("cold_hardiness_class") in COLD_HARDINESS}
    if len(classes) < 2:
        V.append(f"{slug}: overwintering crop must recommend >=2 hardiness classes (found {sorted(classes)})")
    return V


def hardiness_warnings(crop):
    W = []
    if not in_scope(crop):
        return W
    slug = crop.get("slug", "?")
    for x in _variety_objs(crop):
        nm = x.get("name") or x.get("id") or "?"
        c, mc = x.get("cold_hardiness_class"), x.get("maturity_class")
        if c == "very_hardy" and mc == "early":
            W.append(f"{slug}/{nm}: very_hardy (overwintering) variety labeled 'early' -- expected a longer season")
        if c == "tender" and mc == "late":
            W.append(f"{slug}/{nm}: tender (summer) variety labeled 'late' -- expected a fast season")
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
        for v in hardiness_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    warns = 0
    if show_warn:
        for c in crops:
            for w in hardiness_warnings(c):
                print(f"  WARNING: {w}")
                warns += 1
    cov = coverage_report(crops)
    if show_cov:
        print(f"  COVERAGE: in_scope_crops={cov['in_scope_crops']} variety_objs={cov['variety_objs']} "
              f"slugs={cov['slugs']}")
    print(f"overwinter_hardiness: in_scope={cov['in_scope_crops']} objs={cov['variety_objs']} | "
          f"violations={total} warnings={warns}")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 tools/test_overwinter_hardiness_gate.py`
Expected: PASS -- `overwinter_hardiness_gate tests: OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/overwinter_hardiness_gate.py tools/test_overwinter_hardiness_gate.py
git commit -m "feat(hardiness-gate): overwinter_hardiness_gate -- coverage + window-fit engine (leek exemplar)"
```

---

## Task 3: Adversarial RED proof on a scratch copy of real leek

Prove BOTH gate pieces catch real defects in leek's actual shape before content is trusted (the CLAUDE.md "sneak a defect at it" bar). Verification task; no production code changes.

**Files:**
- Create (scratch, session scratchpad -- NOT git): `prove_leek_gate.py` + `leek_scratch.json`

- [ ] **Step 1: Build a scratch canonical whose leek carries the hardiness schema + the winter_hardiness token, confirm both gates green**

Write `prove_leek_gate.py` (in the session scratchpad) that: loads canonical, finds leek, sets `variety_archetype="hardiness_annual"`, adds `"winter_hardiness"` to leek's `gating_factors`, and rewrites leek's 6 varieties to a MINIMAL VALID hardiness schema (id/name/maturity_class/is_reference[one true]/confidence_tier/notes/sources + days_to_maturity + cold_hardiness_class + use; spanning >=2 classes incl. one `very_hardy`/`late` and one `tender`/`early`; add `min_temp_f` on one very_hardy variety as a NEGATIVE int). Dump to `leek_scratch.json`. Run:

Run: `python3 tools/variety_detail_gate.py <scratch>/leek_scratch.json --coverage` (expect `violations=0`, leek in scope)
Run: `python3 tools/overwinter_hardiness_gate.py <scratch>/leek_scratch.json --warnings --coverage` (expect `violations=0`, leek in scope)

- [ ] **Step 2: Inject each defect class into the scratch leek and confirm each bounces**

Mirror the subprocess `_run` pattern from `test_variety_detail_gate.py`. For each, mutate a throwaway copy and assert non-zero exit + expected substring:
- variety_detail domain: `cold_hardiness_class="arctic"` -> mentions `cold_hardiness_class`; drop `days_to_maturity` -> mentions `days_to_maturity`; `days_to_maturity=900` -> mentions `days_to_maturity`; `min_temp_f=200` -> mentions `min_temp_f`; drop `use` -> mentions `use`; two `is_reference: true` -> mentions `is_reference`.
- overwinter_hardiness domain: collapse all 6 varieties to a single `cold_hardiness_class` -> `overwinter_hardiness_gate` exits 1 mentioning `hardiness class` (coverage). (Advisory window-fit: a `very_hardy`+`early` variety prints a WARNING under `--warnings` but does NOT change exit code -- assert the warning STRING appears, exit stays 0.)

Encode as asserts in `prove_leek_gate.py`. On success print `leek hardiness-gate adversarial proof: OK`.

Run: `python3 <scratch>/prove_leek_gate.py`
Expected: `leek hardiness-gate adversarial proof: OK`.

- [ ] **Step 3: Confirm canonical untouched (READ-ONLY held)**

Run: `shasum -a 256 crops_data_final.json | cut -d' ' -f1`
Expected: `e45bcf3c...` (unchanged). No commit (scratch only). Paste the proof output into the Task-6 STATE_HISTORY entry as recorded RED evidence.

---

## Task 4: Author the crop model + 6 varieties + source manifest + Trevor sign-off (CHECKPOINT)

**Files:**
- Create: `tools/build_leek_varieties_patch.py` (mirror `tools/build_onion_varieties_patch.py`)
- Produce: a source manifest (markdown table) for Trevor -- ONLY the non-T1 rows need sign-off

- [ ] **Step 1: Research leek variety hardiness + DTM + the crop-level model (T1-first)**

Dispatch research (as onion did): for each of the 6 varieties find `cold_hardiness_class` (tender/hardy/very_hardy) + `days_to_maturity` (from_transplant) + an optional `min_temp_f` where a T1 source states one. Sources: Cornell "Vegetable Varieties for Gardeners," UMN, extension overwintering guides; Johnny's-class T2 only if needed -> manifest. Also source the crop-level `winter_hardiness` explainer (the summer-vs-overwintering concept, zone dependence, mulch hedge) T1. Confirm each source id is catalogued T1 (`source_catalog`); add none unless required.

- [ ] **Step 2: Draft the builder**

Copy `build_onion_varieties_patch.py` to `build_leek_varieties_patch.py`; set `CANON`, `OUT="tools/batches/leek_varieties_pilot.json"`, target slug `leek`. Author `VARDEFS` for the 6 varieties: `king-richard` (tender/early), `lancelot` (hardy/mid, likely **is_reference:true** -- confirm at authoring), `large-american-flag` (hardy/mid), `tadorna` (hardy/mid-late), `bandit` (very_hardy/late), `giant-musselburgh` (very_hardy/late). Each: `id`, `maturity_class`, `confidence_tier`, per-variety `days_to_maturity`, `cold_hardiness_class`, optional `min_temp_f` (only where T1-sourced), dual-register `note_beginner`/`note_seasoned` (preserve the real content of the current `recommended_note` + the `season` info, then drop those keys), per-variety T1 `sources`/`anchoring_urls`, `use`. Also author the crop-level `winter_hardiness` model object (dual-register explainer + T1 sources). The patch ops (SHA-guarded, mirroring onion):

```python
patch = {"base_sha": sha, "patches": [
    {"op": "add", "json_path": "$.crops[?(@.slug=='leek')].variety_archetype", "value": "hardiness_annual"},
    {"op": "add", "json_path": "$.crops[?(@.slug=='leek')].winter_hardiness", "value": winter_hardiness_model},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].gating_factors", "from": current_gf, "value": new_gf},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].varieties", "from": current_varieties, "value": new_varieties},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].verification_status.source_set", "from": current_ss, "value": new_ss},
]}
```
where `new_gf = sorted(set(current_gf) | {"winter_hardiness"})`.

- [ ] **Step 3: Produce the source manifest for Trevor (non-T1 rows need sign-off)**

Emit a markdown table: `datapoint | variety | proposed source id | tier | URL | what it backs`. T1 rows are informational; every non-T1 row is a sign-off request with the reason T1 was unavailable + the T2 candidate. Include the crop-level `winter_hardiness` model sources + the class->zone-floor thresholds used in the explainer.

- [ ] **CHECKPOINT (Trevor):** Trevor reviews the manifest and approves ship-as-T2 (recorded in `confidence_tier`) or holds. **Do not proceed to Task 5 until sign-off** (or, if all-T1, confirm there is nothing to sign and proceed).

- [ ] **Step 4: Commit the builder (tooling only; canonical untouched)**

```bash
git add tools/build_leek_varieties_patch.py
git commit -m "build(leek): variety-pilot patch builder (6 varieties + winter_hardiness model)"
```

---

## Task 5: SHA-guarded splice + full release battery (CHECKPOINT: promote)

**Files:**
- Generate: `tools/batches/leek_varieties_pilot.json`
- Modify (promote): `crops_data_final.json`

- [ ] **Step 1: Generate the patch + apply to a scratch copy**

```bash
python3 tools/build_leek_varieties_patch.py
python3 tools/apply_patch.py tools/batches/leek_varieties_pilot.json --out crops_data_final.scratch.json
```
Expected: footprint = leek's `varieties` + `variety_archetype` + `winter_hardiness` + `gating_factors` + source_set only; SHA gate passes (base `e45bcf3c`); catalog +none (or the signed-off additions); escaped-unicode 0.

- [ ] **Step 2: Audit the footprint (exactly leek moved; count 125; COMPACT)**

```bash
python3 -c "import json; a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json')); ca={c['slug']:c for c in a['crops']}; cb={c['slug']:c for c in b['crops']}; print('count', len(b['crops'])); print('moved', [s for s in ca if ca[s]!=cb.get(s)]); print('leek keys changed', sorted(k for k in set(ca['leek'])|set(cb['leek']) if ca['leek'].get(k)!=cb['leek'].get(k)))"
```
Expected: `count 125`; `moved ['leek']`; leek keys changed = `['gating_factors','varieties','variety_archetype','verification_status','winter_hardiness']`.

- [ ] **Step 3: Run the full release battery on the scratch candidate**

```bash
python3 tools/whole_crop_gate.py leek crops_data_final.scratch.json
python3 tools/variety_detail_gate.py crops_data_final.scratch.json --warnings --coverage
python3 tools/overwinter_hardiness_gate.py crops_data_final.scratch.json --warnings --coverage
python3 tools/gate_all.py crops_data_final.scratch.json
python3 tools/release_verify.py crops_data_final.scratch.json --base crops_data_final.json --slug leek
python3 tools/source_truth_sample.py --dataset crops_data_final.scratch.json --crops leek
```
Expected: `whole_crop_gate leek` clean; `variety_detail` leek in-scope, 0 violations; `overwinter_hardiness` leek in-scope, 0 violations (window-fit warnings acceptable if the data is honest -- review each); `gate_all` 116 certified unchanged; `release_verify` no new concern beyond pre-existing false positives (confirm identical on base, per the onion pattern); `source_truth_sample` leek traces to approved sources. **If any register-completeness violation appears** (an unruled new key -- not expected, but verify), add the ruling to `register_completeness_gate.py` + its test (TDD) before promoting.

- [ ] **CHECKPOINT (Trevor):** green battery + manifest sign-off = promote-eligible. On Trevor's go:

- [ ] **Step 4: Promote scratch to canonical (COMPACT) + confirm SHA**

```bash
cp crops_data_final.scratch.json crops_data_final.json
rm -f crops_data_final.scratch.json
shasum -a 256 crops_data_final.json | cut -d' ' -f1
```
Record the new SHA for the state trio. Re-run `python3 tools/whole_crop_gate.py leek` + `python3 tools/gate_all.py` + `python3 tools/overwinter_hardiness_gate.py --warnings --coverage` on the promoted canonical -- all clean.

---

## Task 6: State trio + field-addition register + release commit

**Files:**
- Modify: `CURRENT_STATE.md` (surgical prepend), `STATE_HISTORY.md` (prepend), `LATEST.txt`, `docs/field_addition_register.md`

- [ ] **Step 1: Add the field-addition register row 15**

Add a `docs/field_addition_register.md` row 15 for the hardiness-variety bundle (`cold_hardiness_class` + optional `min_temp_f` as the archetype's load-bearing fields, sharing `days_to_maturity` with the DTM archetypes) + the new `overwinter_hardiness_gate` engine, with the explicit INV-1 hard-flip trigger: *"flip the `variety_detail_gate` hardiness-block checks + the `overwinter_hardiness_gate` from soft/standalone into the A39 register-coverage hard floor + `gate_all` when the Spec-2 rollout column pass reaches full-roster coverage."* Note leek = the hardiness-archetype exemplar; garlic + artichoke = the (separately-designed) engine inheritors.

- [ ] **Step 2: State trio**

- CURRENT_STATE.md: prepend a new bold release entry (reverse-chron; no `---` separator -- do NOT run `gen_current_state`, it corrupts the file per `current-state-md-drift`). New SHA, footprint, the hardiness archetype + the new engine + the honest overwintering-viability framing.
- STATE_HISTORY.md: prepend a most-recent-first entry: SHA transition, footprint, the archetype + engine build, the recorded adversarial RED proof (Task 3), the manifest sign-off summary, the reuse-tempering note.
- LATEST.txt: bump SHA + session line.

- [ ] **Step 3: Release commit (Trevor confirms push)**

```bash
git add crops_data_final.json tools/batches/leek_varieties_pilot.json CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/field_addition_register.md
git commit -m "feat(leek): hardiness-archetype variety pilot -- 6 varieties + overwintering engine"
```
Trevor confirms the push. **No plant-astro submodule bump from this session.** App consumption (per-zone overwintering viability) + INV-2 = Spec 2.

---

## Self-Review notes (author)

- **Spec coverage:** crop-level `winter_hardiness` model + gating token (Task 4), the `hardiness_annual` schema + 4-way dispatch + min_temp_f band incl. negatives (Task 1), the engine coverage + window-fit (Task 2), adversarial RED across BOTH gates (Task 3), sourcing contract + manifest sign-off (Task 4), splice/battery/footprint + register-verify (Task 5), state trio + register row + INV-1 (Task 6). The reuse-tempering (spec 6.4) is honored: `overwinter_hardiness_gate` is generic (opts in via the token, imports the shared enum) but its viability rule is leek-specific; vernalization is NOT built here.
- **No new register ruling expected** (spec 7): `cold_hardiness_class` enum -> EXCLUDED_KEYS candidate, `min_temp_f` int (non-string), `use`/common-core ruled, `winter_hardiness` explainer keys `_beginner`/`_seasoned`-suffixed (auto-ruled). Task 5 Step 3 verifies (A25 = 0) and only adds a ruling if a key surfaces -- most likely `cold_hardiness_class` needs EXCLUDED_KEYS like `day_length_type` did; if so, add it + its test (TDD) before promoting.
- **Separation of concerns:** `variety_detail_gate` = shape (enum/min_temp_f/DTM); `overwinter_hardiness_gate` = honesty (coverage/window-fit). No duplication -- the engine imports the enum + extractor rather than re-declaring them (avoiding the onion DAY_LENGTH-dup Minor).
- **min_temp_f sign trap:** the band `[-40, 60]` and the explicit "do NOT reuse the tree positive-int validator" note prevent a very_hardy negative temp from being wrongly rejected.
- **Non-obvious risk:** the coverage rule (>=2 classes) is deliberately SOFTER than onion's per-type coverage, matching leek biology (a summer leek grows everywhere, so no region is left with no viable leek). A single-class opted-in set is the genuine incoherence the check catches.
- **Coverage: gate proxy vs spec's region-aware wording (read before flagging a spec-plan tension).** Spec 6.2 phrases coverage as "the recommended set spans the hardiness classes the regions actually use." The gate (Task 2) implements this as the structural floor `>=2 distinct classes`, which is EQUIVALENT for leek (its regions span USDA zone 3-11, so the classes the regions use = a grow-anywhere summer type PLUS at least one overwintering type = >=2), and it deliberately keeps the soft structural gate DECOUPLED from the sourced class->zone-floor thresholds (those are authored data, Task 4, not gate logic). The full per-zone "which class is viable in zone N" mapping is APP-side (plant-astro, INV-2), not a gate check -- the gate validates that the data can SUPPORT an overwintering story; the app produces the per-zone claim. This is the correct separation, not a spec shortfall.
