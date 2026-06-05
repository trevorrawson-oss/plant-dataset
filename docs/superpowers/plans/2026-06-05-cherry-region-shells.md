# Cherry-tomato region shells + second_planting structure -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build all 10 of cherry-tomato's `regions{}` cells to the ratified reference shape (M16 Step 3.5) and teach the gate the new `second_planting` structure, driving the §A2 *shape* violation classes to 0 while leaving `lettuce-leaf` byte-identical.

**Architecture:** A pure transform (`build_region_shells`) reshapes one crop's regions in memory: `northern_tier` is promoted from the verified cold `zones{}` (add `track`, strip the §3b-i nested `plantings`, re-stamp `resolution_method`, rewrite provenance); the 9 warm/CA regions get a shape-complete RULE skeleton (a `track:"beginner"` rule object with empty archetype window arrays) while their `resolved_by_zone` cells stay PENDING fill-targets for claude.ai's Step 4; the 4 `California -- X` `region_label` em-dashes become `California: X`. A SHA-gated apply runs the transform on a scratch copy with a collateral audit (only cherry changes), the gate verifies §A2 shape = 0 + lettuce still 0, then a PROMOTE close ritual writes canonical and re-pins state. No `second_planting` *data* is written here (claude.ai authors which-zones + dates at Step 4/5); this plan only defines the structure and makes the gate aware of it.

**Tech Stack:** Python 3 standard library (`json`, `hashlib`, `copy`, `subprocess`). No test framework -- tests are assert-based scripts run with `python3`. All commands run from the `~/plant-dataset` repo root.

**Reference:** spec at `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`. Start SHA `29b3aaa904a62487960c5dc53b4282538454076f696ffec039ac4ab87937801a` must equal `LATEST.txt`.

---

## Task 1: The region-shell transform

**Files:**
- Create: `tools/build_region_shells.py`
- Test: `tools/test_build_region_shells.py`

- [ ] **Step 1: Write the failing test**

Create `tools/test_build_region_shells.py`:

```python
#!/usr/bin/env python3
"""Unit test for build_region_shells -- asserts the post-transform shape.
Run from repo root: python3 tools/test_build_region_shells.py"""
import json, copy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_region_shells import build_region_shells

REGION_KEYS = {"northern_tier", "se_gulf", "ca_interior", "ca_north_coast",
               "ca_south_coast", "ca_desert", "warm_arid", "low_desert_az",
               "fl_peninsula", "hawaii_tropical"}

data = json.load(open("crops_data_final.json"))
cherry = copy.deepcopy(next(c for c in data["crops"] if c["slug"] == "cherry-tomato"))
build_region_shells(cherry)
regions = cherry["regions"]

# all 10 regions present
assert set(regions) == REGION_KEYS, f"region set: {set(regions)}"

# no stub plantings; every plantings entry is a dict with a valid track
for rk, r in regions.items():
    pl = r["plantings"]
    assert isinstance(pl, list) and pl and isinstance(pl[0], dict), f"{rk}: stub plantings"
    for p in pl:
        assert p.get("track") in {"beginner", "second_planting", "succession"}, f"{rk}: bad track {p.get('track')!r}"

# no nested plantings in any resolved_by_zone cell (the forbidden §3b-i shape)
for rk, r in regions.items():
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        assert "plantings" not in cell, f"{rk}.{z}: nested plantings survived"

# northern_tier promoted from zones
nt = regions["northern_tier"]
for z, cell in nt["resolved_by_zone"].items():
    assert cell.get("resolution_method") == "zone_promoted_verified", f"nt.{z}: not restamped"
assert isinstance(nt["plantings_provenance"], str) and "Zone-promoted" in nt["plantings_provenance"]

# region_label em-dashes resolved
for rk, r in regions.items():
    assert " -- " not in (r.get("region_label") or ""), f"{rk}: region_label still has --"

# region_notes keys present on every region (value may be null at shell stage)
for rk, r in regions.items():
    assert "region_notes_seasoned" in r and "region_notes_beginner" in r, f"{rk}: missing region_notes keys"

# warm shells: shape-complete RULE skeleton with empty archetype window arrays
for rk in ["se_gulf", "ca_interior", "hawaii_tropical"]:
    p0 = regions[rk]["plantings"][0]
    assert p0["track"] == "beginner", f"{rk}: warm track"
    for w in ["start_indoors", "plant_out", "harvest_start", "harvest_end"]:
        assert p0.get(w) == [], f"{rk}: {w} should be present-but-empty, got {p0.get(w)!r}"

print("PASS build_region_shells")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_build_region_shells.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'build_region_shells'`

- [ ] **Step 3: Write the transform**

Create `tools/build_region_shells.py`:

```python
#!/usr/bin/env python3
"""Build a crop's 10 region cells to the ratified reference shape (M16 Step 3.5).

Pure transform -- mutates the passed crop dict in place, no I/O, no SHA logic
(the apply wrapper owns that). North (northern_tier) is promoted from the
verified cold zones{}; warm/CA regions get a shape-complete RULE skeleton; the
4 `California -- X` region_label em-dashes become `California: X`.

NOT done here: no biology values invented; no second_planting data written
(claude.ai authors which-zones + dates at Step 4/5); resolved_by_zone cells of
warm regions are left as PENDING fill-targets (derived output, not rule shape).

See docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md
"""
SESSION = "m16_cherry_step3_5_region_shells"
DATE = "2026-06-05"


def build_region_shells(crop):
    """Mutate `crop` so every region cell is at reference shape. Returns crop."""
    for rk, r in (crop.get("regions") or {}).items():
        # slot scaffolding: region_notes keys present (null acceptable at admission)
        r.setdefault("region_notes_seasoned", None)
        r.setdefault("region_notes_beginner", None)
        # dash resolution on the structural label: "California -- X" -> "California: X"
        lbl = r.get("region_label")
        if isinstance(lbl, str) and " -- " in lbl:
            r["region_label"] = lbl.replace(" -- ", ": ")
        if rk == "northern_tier":
            _build_north_from_zones(r)
        else:
            _build_warm_shell(r)
    return crop


def _build_north_from_zones(r):
    # region-constant RULE layer: every plantings entry carries a track
    for p in r.get("plantings") or []:
        if isinstance(p, dict):
            p.setdefault("track", "beginner")
    # resolved layer: strip the forbidden nested plantings (§3b-i) and re-stamp
    # static_precompute -> zone_promoted_verified (these cells are promoted +
    # verified from the cold zones{}, not statically precomputed)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            cell.pop("plantings", None)
            if cell.get("resolution_method") == "static_precompute":
                cell["resolution_method"] = "zone_promoted_verified"
    # provenance: replace the Phase-A verbatim-lift string with a promotion record
    r["plantings_provenance"] = (
        "Zone-promoted and re-verified from cold zones 3-7 "
        f"({SESSION}, {DATE}). Supersedes the Phase A verbatim lift."
    )


def _build_warm_shell(r):
    # shape-complete RULE skeleton (warm_season_fruiting transplant archetype):
    # a single track:"beginner" rule object with the archetype window-rule keys
    # present-but-empty, ready for Step 4 to fill values into. resolved_by_zone
    # cells are left untouched (derived output; PENDING until Step 4 sources them).
    r["plantings"] = [{
        "succession_id": 1,
        "label": "main",
        "track": "beginner",
        "start_indoors": [],
        "plant_out": [],
        "harvest_start": [],
        "harvest_end": [],
        "anchoring_urls": {},
    }]
    # defensive: no rule-bearing structure may live in the resolved layer
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            cell.pop("plantings", None)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_build_region_shells.py`
Expected: `PASS build_region_shells`

- [ ] **Step 5: Commit**

```bash
git add tools/build_region_shells.py tools/test_build_region_shells.py
git commit -m "feat(m16): region-shell transform for cherry Step 3.5

Pure build_region_shells(crop): north promoted-from-zones (track + nested
strip + resolution_method restamp + provenance), warm shape-complete rule
skeletons, region_label dash fix. Unit-tested. No biology, no apply yet.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Teach the gate the `second_planting` structure

**Files:**
- Modify: `tools/whole_crop_gate.py` (add a validation block at the end of the §A2 section, after line 146 `fail(f"region_notes pair both null: {rk}")`)
- Test: `tools/test_gate_second_planting.py`

Context: the gate's recursive walkers already handle `second_planting` for dual-voice/dash/source/anchoring, and §A2's stale-shape check keys on the literal `"plantings"` key (so a sibling `second_planting` key is not mistaken for it). The only addition is an explicit shape check so a malformed `second_planting` (the structure claude.ai will populate at Step 4/5) is caught.

- [ ] **Step 1: Write the failing test**

Create `tools/test_gate_second_planting.py`:

```python
#!/usr/bin/env python3
"""Integration test: the gate validates the second_planting structure.
Reuses real cherry (post-transform) + injects a second_planting into a resolved
cell, runs the gate as a subprocess, and checks the specific violation string.
Run from repo root: python3 tools/test_gate_second_planting.py"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_region_shells import build_region_shells

base = json.load(open("crops_data_final.json"))
build_region_shells(next(c for c in base["crops"] if c["slug"] == "cherry-tomato"))


def run_gate_with(sp_value):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == "cherry-tomato")
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["second_planting"] = sp_value
    tmp = os.path.join(HERE, "_tmp_sp_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "whole_crop_gate.py"), "cherry-tomato", tmp],
            capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)
    return out

# missing window keys -> violation
bad = run_gate_with({"plant_out": "Aug 1 - Aug 14"})
assert "second_planting missing window keys" in bad, "expected missing-keys violation"

# non-dict -> violation
nd = run_gate_with("PENDING")
assert "second_planting not a dict" in nd, "expected not-a-dict violation"

# well-formed (all window keys present; values may be null at admission) -> no sp violation
good = run_gate_with({"plant_out": "Aug 1 - Aug 14", "start_indoors": None,
                      "harvest_start": "Oct 1", "harvest_end": "Dec 10",
                      "sources": [], "anchoring_urls": {}})
assert "second_planting missing window keys" not in good, "well-formed should not flag missing keys"
assert "second_planting not a dict" not in good, "well-formed should not flag dict"

print("PASS gate second_planting validation")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_gate_second_planting.py`
Expected: FAIL with `AssertionError: expected missing-keys violation` (the gate does not yet check `second_planting`).

- [ ] **Step 3: Add the validation block to the gate**

In `tools/whole_crop_gate.py`, immediately after the §A2 loop that ends with `fail(f"region_notes pair both null: {rk}")` (line 146), insert:

```python
# second_planting structure validation (M16): when a resolved cell carries a
# second_planting, it must be a discrete-window dict with the window field set.
# Lenient on null VALUES at admission (claude.ai sources them at Step 4/5); the
# KEYS must exist. Forward-looking -- cherry carries none at Step 3.5.
SECOND_PLANTING_KEYS = {"plant_out", "start_indoors", "harvest_start", "harvest_end"}
for rk, r in regions.items():
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        if isinstance(cell, dict) and "second_planting" in cell:
            sp = cell["second_planting"]
            if not isinstance(sp, dict):
                fail(f"second_planting not a dict: {rk}.{z}")
            elif not SECOND_PLANTING_KEYS.issubset(sp):
                missing = sorted(SECOND_PLANTING_KEYS - set(sp))
                fail(f"second_planting missing window keys {missing}: {rk}.{z}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_gate_second_planting.py`
Expected: `PASS gate second_planting validation`

- [ ] **Step 5: Regression-guard lettuce (the gate must not flag the certified crop)**

Run: `python3 tools/whole_crop_gate.py lettuce-leaf`
Expected: ends with `GATE: PASS` (lettuce has no `second_planting`; the new block does not fire). If it prints any VIOLATION, STOP -- the gate edit regressed a certified crop.

- [ ] **Step 6: Commit**

```bash
git add tools/whole_crop_gate.py tools/test_gate_second_planting.py
git commit -m "feat(m16): gate validates the second_planting structure

§A2 now checks that a resolved-cell second_planting is a discrete-window dict
with the window keys (lenient on null values at admission). Forward-looking for
claude.ai's Step 4/5 fill. Lettuce regression-guarded: still GATE: PASS.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: SHA-gated apply to scratch + verification

**Files:**
- Create: `tools/apply_region_shells.py`
- Produces: `crops_data_final.scratch.json` (gitignored scratch -- do NOT commit)

- [ ] **Step 1: Write the apply wrapper**

Create `tools/apply_region_shells.py`:

```python
#!/usr/bin/env python3
"""SHA-gated apply of build_region_shells to ONE crop, written to a scratch copy
with a collateral audit. Does NOT touch canonical -- promotion is a separate,
manual step after the gate verifies the scratch. Run from repo root:
    python3 tools/apply_region_shells.py [slug]
"""
import json, hashlib, copy, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_region_shells import build_region_shells

EXPECTED_SHA = "29b3aaa904a62487960c5dc53b4282538454076f696ffec039ac4ab87937801a"
PATH = "crops_data_final.json"
SCRATCH = "crops_data_final.scratch.json"
SLUG = sys.argv[1] if len(sys.argv) > 1 else "cherry-tomato"

raw = open(PATH, "rb").read()
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA:
    sys.exit(f"SHA mismatch: {actual} != {EXPECTED_SHA} -- STOP, reconcile against LATEST.txt")

data = json.loads(raw)
before = copy.deepcopy(data)
crop = next(c for c in data["crops"] if c["slug"] == SLUG)
build_region_shells(crop)

# collateral audit: every OTHER crop byte-identical (compared as parsed objects)
assert set(before) == set(data), "top-level key set changed"
for k in before:
    if k != "crops":
        assert before[k] == data[k], f"top-level key changed: {k}"
changed = [b["slug"] for b, a in zip(before["crops"], data["crops"]) if b != a]
assert changed == [SLUG], f"collateral change -- expected only {SLUG!r}, got {changed}"

with open(SCRATCH, "w") as f:
    json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
print(f"scratch written: {SCRATCH} (only {SLUG} changed)")
```

- [ ] **Step 2: Run the apply**

Run: `python3 tools/apply_region_shells.py cherry-tomato`
Expected: `scratch written: crops_data_final.scratch.json (only cherry-tomato changed)`
If it prints a SHA mismatch or an assertion error, STOP and reconcile.

- [ ] **Step 3: Gate the scratch for cherry -- §A2 shape classes must be 0**

Run: `python3 tools/whole_crop_gate.py cherry-tomato crops_data_final.scratch.json`
Expected: the `A2.` line reads `stub/missing plantings: 0 | null-track plantings: 0 | stale nested-cell shape (§3b-i): 0 | both region_notes null: 10`. The gate still exits non-zero overall (the residual is documented downstream claude.ai work: ~10 region_notes-null, the dual-voice siblings, source-name dash, source-tier T2, and 1 northern_tier `cornell_ext` URL gap). The Step-3.5 success condition is the three shape classes at 0, NOT the whole gate at 0.

- [ ] **Step 4: Gate the scratch for lettuce -- regression guard**

Run: `python3 tools/whole_crop_gate.py lettuce-leaf crops_data_final.scratch.json`
Expected: ends with `GATE: PASS`. Lettuce must be untouched by the cherry apply. Any violation means the apply leaked; STOP.

- [ ] **Step 5: Confirm the residual delta is exactly as expected (sanity diff)**

Run:
```bash
python3 -c "
import json
a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json'))
ca=next(c for c in a['crops'] if c['slug']=='cherry-tomato')
cb=next(c for c in b['crops'] if c['slug']=='cherry-tomato')
print('cherry top-level keys changed:', [k for k in ca if ca[k]!=cb.get(k)])
print('regions changed:', [r for r in ca['regions'] if ca['regions'][r]!=cb['regions'][r]])
"
```
Expected: `cherry top-level keys changed: ['regions']` and `regions changed:` lists all 10 region keys. Anything outside `regions` changing is a bug; STOP.

- [ ] **Step 6: Commit the apply tool (NOT the scratch data)**

```bash
echo "crops_data_final.scratch.json" >> .gitignore
git add tools/apply_region_shells.py .gitignore
git commit -m "feat(m16): SHA-gated apply for region shells (scratch + collateral audit)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: PROMOTE -- canonical write + close ritual

This is the close ritual from `CURRENT_STATE.md`. Only proceed if Task 3 verified clean on the scratch.

- [ ] **Step 1: Promote the scratch to canonical**

Run: `mv crops_data_final.scratch.json crops_data_final.json`

- [ ] **Step 2: Independent post-write re-verification (read the output only)**

Run: `python3 tools/whole_crop_gate.py cherry-tomato`
Expected: same `A2.` line as Task 3 Step 3 (`stub: 0 | null-track: 0 | stale: 0 | both region_notes null: 10`), reading the now-canonical file.
Run: `python3 tools/whole_crop_gate.py lettuce-leaf`
Expected: `GATE: PASS`.

- [ ] **Step 3: Re-pin `LATEST.txt`**

Compute the new SHA and write `LATEST.txt`:
```bash
NEWSHA=$(shasum -a 256 crops_data_final.json | cut -d' ' -f1)
printf 'SHA: %s\nDate: 2026-06-05\nSession: m16_cherry_step3_5_region_shells\n' "$NEWSHA" > LATEST.txt
cat LATEST.txt
```
Expected: a new SHA (not `29b3aaa9...`), date `2026-06-05`, session `m16_cherry_step3_5_region_shells`.

- [ ] **Step 4: Regenerate `CURRENT_STATE.md` (full file, never a delta)**

Per the session protocol, fully regenerate `CURRENT_STATE.md` from true state. Required updates (regenerate the whole file -- header, canonical pointer + predecessor chain with the new SHA, "What just happened" = the M16 cherry Step 3.5 shell build + the new `second_planting` structure + the gate change, "Active work" = cherry now at Step 3.5-complete with claude.ai owed Steps 4-8, and add a live locked decision recording the `second_planting` structure / main-flat + succession shape ratification / shape-complete-shell rule. Keep it lean per the two-doc protocol.

- [ ] **Step 5: Append to `STATE_HISTORY.md` (append-only, dated entry)**

Append a dated `2026-06-05` entry: session `m16_cherry_step3_5_region_shells`; what was built (10 cherry region shells, north promoted-from-zones, warm shape-complete skeletons, region_label dashes, the `second_planting` structure + gate validation); the gate result (cherry §A2 shape = 0, lettuce regression-guarded PASS); the spec + plan paths; the open downstream items routed to claude.ai (Steps 4-8, the `second_planting` date authoring, `cornell_ext` URL, `harvest_to_table` T2 ruling, extreme-zone record).

- [ ] **Step 6: Sync `00-current/`**

Mirror the regenerated `CURRENT_STATE.md` + `STATE_HISTORY.md` into `00-current/` per the close ritual (the claude.ai orientation surface). Run `ls 00-current/` first to confirm the destination filenames, then copy.

- [ ] **Step 7: Commit (push is the announce-then-execute moment)**

```bash
git add crops_data_final.json LATEST.txt CURRENT_STATE.md STATE_HISTORY.md 00-current/
git commit -m "feat(m16): cherry-tomato Step 3.5 region shells + second_planting structure

Built all 10 cherry region cells to reference shape: northern_tier promoted
from cold zones{} (track + nested-plantings strip + zone_promoted_verified +
provenance), 9 warm/CA regions shape-complete rule skeletons, 4 region_label
em-dashes resolved. Defined the second_planting structure + gate validation.
Lettuce byte-identical and still GATE: PASS. §A2 shape classes = 0; residual
gate count is downstream claude.ai work (Steps 4-8).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 8: Present results to Trevor, then push**

Dataset push is autonomous (announce-then-execute), but this is the first Step 3.5 + a new structure. Summarize for Trevor: the gate before/after (42 -> residual), the §A2 shape-classes-at-0 proof line, the collateral audit (only cherry changed, lettuce byte-identical), and the new SHA. Then `git push` the dataset. plant-astro stays gated (no submodule bump in this work).

---

## Notes for the executor

- **Run everything from `~/plant-dataset` repo root** (paths like `crops_data_final.json` are cwd-relative).
- **Step-3.5 "done" is NOT the whole gate at 0.** It is the three §A2 shape classes (`stub`, `null-track`, `stale nested`) at 0. The region_notes-null (10), dual-voice siblings, source-name dash, source-tier T2, and the `cornell_ext` URL gap are all documented downstream claude.ai work, not failures of this plan.
- **Never author placeholder copy** to zero the region_notes count, and **never invent biology values** in the warm shells.
- **If any collateral-audit or lettuce-regression check fails, STOP** and report -- do not promote.
