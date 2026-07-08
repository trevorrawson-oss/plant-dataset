# Heat-gap `indoors` flip -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** During a summer `heat_pause`, show `indoors` (the actionable "start your fall seedlings now") instead of `heat_pause` on any month that is a core month of a real indoor-start window -- so growers see "time to start indoors," not just "too hot."

**Architecture:** Encode an action-over-passive rule in the annual calendar deriver (`tools/annual_calendar.py`), enforce it with two gate checks (an updated A5 coherence + a new A5b backing invariant, both TDD RED-before-GREEN), then apply the flip to the 22 affected cells' hand-authored `calendar[]` arrays via a SHA-guarded `apply_patch` batch. The explanatory note is derived app-side (plant-astro kickoff), not stored in canonical.

**Tech Stack:** Python 3 (stdlib only), the repo's gate suite (`whole_crop_gate.py`, `gate_all.py`, `calendar_coherence_gate.py`, `release_verify.py`), `apply_patch.py` for the SHA-guarded splice.

## Global Constraints

- Canonical JSON is **COMPACT**: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it. (`apply_patch.py` already writes this form.)
- **READ-ONLY on `crops_data_final.json`** except the explicit promote in Task 4.
- **Tests-first (TDD): RED before GREEN.** Every new/changed gate must be shown to bounce an injected defect on a scratch copy of the real canonical before it is trusted.
- No em dashes in consumer copy; American English; temps render `NN°F` (no space). (`--` is fine in docs/code/commit messages.)
- **Don't commit canonical until Trevor approves; Trevor confirms every push.** Task 4's canonical promote + Task 5's state trio are prepared and held; do not `git push` without Trevor's go-ahead.
- The flip touches **only** stage-token months; **stage `id` values and `day_range_from_sow` are irrelevant here** -- this plan edits only per-zone `calendar[]` arrays.
- Reference cell for hand-checks: broccoli `ca_interior` z9 -> `heat_pause.months [5,6,7]`, `second_planting.start_indoors "Jun 20 - Aug 18"`, expected flip month = **July** (index 6).

---

### Task 1: The flip rule in the deriver

**Files:**
- Modify: `tools/annual_calendar.py` (add helper `indoor_core_months`; change `derive_annual_calendar` heat source + precedence)
- Test: `tools/test_annual_calendar.py`

**Interfaces:**
- Produces: `indoor_core_months(cell) -> set[int]` (1-12); `derive_annual_calendar(cell, calendar_basis="frost_anchored") -> list[str]` now emits `"indoors"` on a `heat_pause` month that is a core indoor-start month.
- Consumes: existing `core_months(display)`, `declared_heat_months(cell)` (reads nested `heat_pause.months` or flat `heat_pause_months`).

- [ ] **Step 1: Write the failing test**

Add to `tools/test_annual_calendar.py`:

```python
from annual_calendar import derive_annual_calendar, indoor_core_months

def test_heat_pause_flips_to_indoors_on_core_indoor_month():
    # broccoli ca_interior z9 shape: pause May-Jul, fall indoor window Jun 20 - Aug 18.
    cell = {
        "plant_out": "Dec 1 - Feb 28",
        "start_indoors": "Nov 1 - Nov 22",
        "harvest": "Mar 1 - May 1",
        "harvest_start": "Mar 1", "harvest_end": "May 1",
        "heat_pause": {"months": [5, 6, 7]},
        "second_planting": {"start_indoors": "Jun 20 - Aug 18",
                            "plant_out": "Aug 1 - Sep 30",
                            "harvest_start": "Oct 15", "harvest_end": "Dec 15"},
    }
    cal = derive_annual_calendar(cell)
    assert cal[4] == "heat_pause"   # May: pause, not a core indoor month
    assert cal[5] == "heat_pause"   # Jun: window opens the 20th -> not core
    assert cal[6] == "indoors"      # Jul: core month of Jun 20 - Aug 18 -> FLIP
    assert indoor_core_months(cell) == {7, 11}  # Jul (2nd planting) + Nov (spring)

def test_no_flip_when_no_indoor_window_overlaps_pause():
    cell = {
        "plant_out": "Sep 1 - Oct 1", "start_indoors": None,
        "harvest": "Nov 1 - Dec 1", "harvest_start": "Nov 1", "harvest_end": "Dec 1",
        "heat_pause": {"months": [6, 7, 8]},
    }
    cal = derive_annual_calendar(cell)
    assert cal[5] == cal[6] == cal[7] == "heat_pause"  # no indoor action -> no flip
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -k "heat_pause_flips or no_flip_when" -v`
Expected: FAIL -- `ImportError: cannot import name 'indoor_core_months'` (and/or assertion on `cal[6]`).

- [ ] **Step 3: Write minimal implementation**

In `tools/annual_calendar.py`, add the helper (place it just below `core_months`):

```python
def indoor_core_months(cell):
    """Core (fully day-covered) months of any REAL indoor-start window on this cell:
    top-level `start_indoors` OR `second_planting.start_indoors`. These are the months
    where an indoor-start ACTION is genuinely underway (the action-over-passive trigger)."""
    out = set(core_months(cell.get("start_indoors")))
    sp = cell.get("second_planting") or {}
    out |= core_months(sp.get("start_indoors"))
    return out
```

In `derive_annual_calendar`, change the heat source line
`heat = set(cell.get("heat_pause_months") or ())`
to read nested-or-flat and add the flip set:

```python
    heat = declared_heat_months(cell)            # nested heat_pause.months OR flat heat_pause_months
    heat_flip = heat & indoor_core_months(cell)  # action-over-passive: hot months that are core indoor months
```

Then, in the `for m in range(1, 13):` token loop, add the flip as the highest-precedence case (before the `if m in heat:` branch):

```python
    for m in range(1, 13):
        if m in heat_flip:
            cal.append("indoors")            # NEW: real indoor action overrides the passive pause
        elif m in heat:
            cal.append("heat_pause")
        elif m in P:
            cal.append("plant")
        elif m in H:
            cal.append("harvest")
        elif m in I:
            cal.append("indoors")
        elif m in cold:
            cal.append("cold_pause")
        elif calendar_basis == "frost_anchored":
            cal.append("growing")
        else:
            cal.append("wait")
```

(`active = P | H | I | heat` already covers `heat_flip` since `heat_flip <= heat`, so the `cold` computation is unchanged.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -v`
Expected: PASS (new tests + all existing `test_annual_calendar.py` tests still green).

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/annual_calendar.py tools/test_annual_calendar.py
git commit -m "feat(calendar): action-over-passive flip in derive_annual_calendar (heat_pause->indoors on core indoor month)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Update the A5 coherence gate to allow a backed flip

**Files:**
- Modify: `tools/annual_calendar.py` (`annual_coherence_violations`, the `heat_pause.months` alignment block)
- Test: `tools/test_annual_calendar.py`

**Interfaces:**
- Consumes: `annual_coherence_violations(crop) -> (hard: list[str], notes: list[str])` (unchanged signature).
- Produces: A5 now requires `calendar heat_pause months == heat_pause.months MINUS the months flipped to indoors`, preserving "no heat_pause token outside heat_pause.months" and "every hot month shows heat_pause or a flipped indoors."

- [ ] **Step 1: Write the failing test**

Add to `tools/test_annual_calendar.py`:

```python
from annual_calendar import annual_coherence_violations

def _crop_with_cell(cal, hp_months):
    return {"calendar_basis": "frost_anchored",
            "regions": {"r": {"resolved_by_zone": {"9": {
                "calendar": cal, "heat_pause": {"months": hp_months}}}}}}

def test_a5_accepts_valid_indoors_flip():
    # hot months [5,6,7]; July shown as indoors (a flip) -> coherent
    cal = ["plant","plant","harvest","harvest","heat_pause","heat_pause","indoors",
           "plant","plant","harvest","harvest","plant"]
    hard, _ = annual_coherence_violations(_crop_with_cell(cal, [5, 6, 7]))
    assert hard == []

def test_a5_rejects_hot_month_shown_as_plant():
    # a hot month rendered as plant (neither heat_pause nor a flipped indoors) -> violation
    cal = ["plant","plant","harvest","harvest","heat_pause","heat_pause","plant",
           "plant","plant","harvest","harvest","plant"]
    hard, _ = annual_coherence_violations(_crop_with_cell(cal, [5, 6, 7]))
    assert any("heat_pause" in h for h in hard)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -k "a5_accepts or a5_rejects" -v`
Expected: FAIL -- `test_a5_accepts_valid_indoors_flip` fails under the old exact-equality rule (it flags July as a mismatch).

- [ ] **Step 3: Write minimal implementation**

In `annual_coherence_violations`, replace the `hp` alignment block:

```python
            hp = (cell.get("heat_pause") or {}).get("months")
            if hp is not None:
                cal_hp = [i + 1 for i in range(12) if cal[i] == "heat_pause"]
                if sorted(hp) != sorted(cal_hp):
                    hard.append(f"{loc}: heat_pause.months {sorted(hp)} != calendar heat_pause {sorted(cal_hp)}")
```

with the flip-aware version:

```python
            hp = (cell.get("heat_pause") or {}).get("months")
            if hp is not None:
                hp = set(hp)
                cal_hp = {i + 1 for i in range(12) if cal[i] == "heat_pause"}
                flipped = hp & {i + 1 for i in range(12) if cal[i] == "indoors"}
                if cal_hp != hp - flipped:
                    hard.append(f"{loc}: calendar heat_pause {sorted(cal_hp)} != heat_pause.months "
                                f"{sorted(hp)} minus flipped-to-indoors {sorted(flipped)} "
                                f"(each hot month must show heat_pause or a backed indoors flip; "
                                f"no heat_pause token outside heat_pause.months)")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -v`
Expected: PASS (new + existing).

Then confirm the gate change does NOT break the current (unflipped) canonical -- every current cell has `flipped == {}`, so A5 is unchanged for them:
Run: `cd /Users/trevorrawson/plant-dataset && python3 tools/gate_all.py 2>&1 | tail -2`
Expected: `gate_all: PASS -- every certified crop passes the whole suite`

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/annual_calendar.py tools/test_annual_calendar.py
git commit -m "feat(gate): A5 coherence allows a backed heat_pause->indoors flip

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: The flip-backing invariant (A5b) -- "action must be real"

**Files:**
- Modify: `tools/annual_calendar.py` (new function `heat_flip_backing_violations`)
- Modify: `tools/whole_crop_gate.py` (wire A5b next to the A5 block)
- Test: `tools/test_annual_calendar.py`

**Interfaces:**
- Produces: `heat_flip_backing_violations(crop) -> list[str]`. A `heat_pause` month shown as `indoors` is a violation unless that month is in `indoor_core_months(cell)`.
- Consumes: `indoor_core_months` (Task 1), module constant `_MON_ABBR`.

- [ ] **Step 1: Write the failing test**

Add to `tools/test_annual_calendar.py`:

```python
from annual_calendar import heat_flip_backing_violations

def test_backing_accepts_flip_with_real_indoor_window():
    cell = {"calendar": ["plant","plant","harvest","harvest","heat_pause","heat_pause","indoors",
                         "plant","plant","harvest","harvest","plant"],
            "heat_pause": {"months": [5, 6, 7]},
            "second_planting": {"start_indoors": "Jun 20 - Aug 18"}}
    crop = {"calendar_basis": "frost_anchored", "regions": {"r": {"resolved_by_zone": {"9": cell}}}}
    assert heat_flip_backing_violations(crop) == []

def test_backing_rejects_flip_with_no_indoor_window():
    cell = {"calendar": ["plant","plant","harvest","harvest","heat_pause","heat_pause","indoors",
                         "plant","plant","harvest","harvest","plant"],
            "heat_pause": {"months": [5, 6, 7]}}  # NO start_indoors / second_planting -> unbacked July flip
    crop = {"calendar_basis": "frost_anchored", "regions": {"r": {"resolved_by_zone": {"9": cell}}}}
    v = heat_flip_backing_violations(crop)
    assert any("Jul" in x and "indoors" in x for x in v)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -k backing -v`
Expected: FAIL -- `ImportError: cannot import name 'heat_flip_backing_violations'`.

- [ ] **Step 3: Write minimal implementation**

Add to `tools/annual_calendar.py` (near `heat_pause_backing_violations`):

```python
def heat_flip_backing_violations(crop):
    """The action-must-be-real guard (whole_crop_gate A5b). A heat_pause month may display
    `indoors` (the action-over-passive flip) ONLY where a real indoor-start window
    (top-level start_indoors OR second_planting.start_indoors) has that month as a CORE
    month. An `indoors` on a hot month with no such backing is a fabricated action shown to
    a grower. No-op for non-frost_anchored crops. Returns a list of violation strings."""
    if crop.get("calendar_basis") != "frost_anchored":
        return []
    out = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            cal = cell.get("calendar")
            if not isinstance(cal, list) or len(cal) != 12:
                continue
            hp = (cell.get("heat_pause") or {}).get("months")
            if not hp:
                continue
            hp = set(hp)
            backed = indoor_core_months(cell)
            for i in range(12):
                if cal[i] == "indoors" and (i + 1) in hp and (i + 1) not in backed:
                    out.append(f"{rk}.z{z}: {_MON_ABBR[i]} shows `indoors` on a heat_pause month "
                               f"with no indoor-start window covering it "
                               f"(start_indoors / second_planting.start_indoors) -- unbacked flip")
    return out
```

In `tools/whole_crop_gate.py`, immediately after the A5 block (the lines that call
`annual_coherence_violations(crop)` and `fail(...)` on each `_acoh` entry), add:

```python
from annual_calendar import heat_flip_backing_violations
print("A5b. heat-gap indoors-flip backing (an `indoors` on a hot month needs a real indoor-start; no-op for non-annual)")
_hflip = heat_flip_backing_violations(crop)
print(f"  unbacked heat_pause->indoors flips: {len(_hflip)}")
for m in _hflip:
    fail(f"heat-flip-backing: {m}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/trevorrawson/plant-dataset && python3 -m pytest tools/test_annual_calendar.py -v`
Expected: PASS.
Run: `cd /Users/trevorrawson/plant-dataset && python3 tools/gate_all.py 2>&1 | tail -2`
Expected: `gate_all: PASS` (no current cell has an unbacked flip; none flip yet).

- [ ] **Step 5: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add tools/annual_calendar.py tools/whole_crop_gate.py tools/test_annual_calendar.py
git commit -m "feat(gate): A5b flip-backing invariant (indoors on a hot month must have a real indoor-start)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Apply the 22-cell flip to canonical (SHA-guarded)

**Files:**
- Create: `tools/batches/heat_gap_indoors_flip.json` (the apply_patch batch)
- Create (scratch): a builder script under the session scratchpad
- Modify (promote): `crops_data_final.json`

**Interfaces:**
- Consumes: `indoor_core_months` + `declared_heat_months` (Task 1), `tools/apply_patch.py`.
- Produces: canonical with `heat_pause -> indoors` on exactly the computed flip months of the 22 cells; nothing else changed.

- [ ] **Step 1: Write the builder (RED via a dry validation)**

Create `<scratchpad>/build_heat_flip_patch.py`:

```python
import json, hashlib, sys, os
sys.path.insert(0, "/Users/trevorrawson/plant-dataset/tools")
from annual_calendar import indoor_core_months, declared_heat_months
ROOT = "/Users/trevorrawson/plant-dataset"; SCR = os.path.dirname(os.path.abspath(__file__))
raw = open(f"{ROOT}/crops_data_final.json", "rb").read()
base_sha = hashlib.sha256(raw).hexdigest(); data = json.loads(raw)
patches, errors = [], []
for c in data["crops"]:
    for rk, rv in (c.get("regions") or {}).items():
        for z, cell in (rv.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict): continue
            cal = cell.get("calendar")
            if not isinstance(cal, list) or len(cal) != 12: continue
            heat = declared_heat_months(cell)
            flip = sorted(heat & indoor_core_months(cell))
            if not flip: continue
            new = list(cal)
            for m in flip:
                if cal[m-1] != "heat_pause":
                    errors.append(f"{c['slug']}/{rk}/z{z}: flip month {m} is {cal[m-1]!r}, not heat_pause")
                new[m-1] = "indoors"
            if new != cal:
                patches.append({"op":"replace",
                    "json_path": f"crops[?(@.slug=='{c['slug']}')].regions.{rk}.resolved_by_zone.{z}.calendar",
                    "from": cal, "value": new})
if errors:
    print("ERRORS:"); [print("  ", e) for e in errors]; sys.exit(1)
json.dump({"base_sha": base_sha, "patches": patches},
          open(f"{SCR}/heat_gap_indoors_flip.json","w"), ensure_ascii=False, indent=1)
print(f"base_sha {base_sha[:16]} | {len(patches)} cells flipped")
```

- [ ] **Step 2: Run it -- verify 22 cells, zero errors**

Run: `cd /Users/trevorrawson/plant-dataset && python3 <scratchpad>/build_heat_flip_patch.py`
Expected: `... | 22 cells flipped` and NO `ERRORS:` block. (If any "flip month is not heat_pause" error prints, STOP and surface it -- a stored calendar disagrees with its heat_pause.months and needs review, not a silent change.)

- [ ] **Step 3: Apply to a scratch copy + validate footprint**

```bash
cd /Users/trevorrawson/plant-dataset
python3 tools/apply_patch.py <scratchpad>/heat_gap_indoors_flip.json \
  --base crops_data_final.json --out <scratchpad>/crops.scratch.json
```
Then validate (run this Python):
```python
import json
a=json.load(open("crops_data_final.json")); b=json.load(open("<scratchpad>/crops.scratch.json"))
assert len(b["crops"])==124
ac={c["slug"]:c for c in a["crops"]}; bc={c["slug"]:c for c in b["crops"]}
changed=[s for s in ac if ac[s]!=bc[s]]
# every diff must be ONLY inside regions[..].resolved_by_zone[..].calendar, heat_pause->indoors
import copy
for s in changed:
    x=copy.deepcopy(ac[s]); y=copy.deepcopy(bc[s])
    # blank every calendar array, then require byte-equality
    for crop in (x,y):
        for rv in (crop.get("regions") or {}).values():
            for cell in (rv.get("resolved_by_zone") or {}).values():
                if isinstance(cell,dict): cell["calendar"]=None
    assert x==y, f"{s}: change outside calendar[]"
raw=open("<scratchpad>/crops.scratch.json","rb").read()
assert raw.count(b"\n")==0 and raw[-1:]==b"}" and raw.count(b"\\u")==0
print("footprint OK: only calendar[] tokens changed; compact; count 124")
```
Expected: `footprint OK ...`

- [ ] **Step 4: Gate the scratch copy**

```bash
cd /Users/trevorrawson/plant-dataset
python3 tools/gate_all.py <scratchpad>/crops.scratch.json 2>&1 | tail -2
python3 tools/whole_crop_gate.py broccoli <scratchpad>/crops.scratch.json 2>&1 | grep -E "A5b|GATE:"
python3 tools/calendar_coherence_gate.py <scratchpad>/crops.scratch.json 2>&1 | tail -3
python3 tools/release_verify.py <scratchpad>/crops.scratch.json 2>&1 | tail -1
```
Expected: `gate_all: PASS -- every certified crop passes the whole suite`; broccoli `A5b ... 0` + `GATE: PASS`; calendar coherence clean; `RELEASE-VERIFY: clean`.

- [ ] **Step 5: Promote to canonical + stage the batch**

```bash
cd /Users/trevorrawson/plant-dataset
cp <scratchpad>/heat_gap_indoors_flip.json tools/batches/heat_gap_indoors_flip.json
python3 tools/apply_patch.py tools/batches/heat_gap_indoors_flip.json \
  --base crops_data_final.json --out crops_data_final.json
shasum -a 256 crops_data_final.json
python3 tools/gate_all.py 2>&1 | tail -2
```
Expected: new SHA printed (record it); `gate_all: PASS`.

- [ ] **Step 6: Commit (held for Trevor's push)**

```bash
cd /Users/trevorrawson/plant-dataset
git add crops_data_final.json tools/batches/heat_gap_indoors_flip.json
git commit -m "feat(calendar): heat-gap indoors flip on 22 cells (heat_pause->indoors on core indoor month)

<OLD_SHA> -> <NEW_SHA>

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: State trio (content release)

**Files:**
- Modify: `LATEST.txt`, `CURRENT_STATE.md` (prepend, hand-maintained -- never regen; see memory `current-state-md-drift`), `STATE_HISTORY.md` (prepend below the header stack)

**Interfaces:** none (docs).

- [ ] **Step 1: Bump `LATEST.txt`** -- new SHA + a Session paragraph (dense house style) describing the flip: the action-over-passive rule, the 22 cells (celery 10 / broccoli 4 / kohlrabi 4 / tomatoes 4), the core-month trigger, `stage ids untouched` (calendar tokens only), the A5 update + A5b backing gate (TDD), gates green, and `APP HANDOFF docs/kickoffs/17-...`.

- [ ] **Step 2: Prepend a `CURRENT_STATE.md` entry** (one dense bold line at the very top, matching existing entries; SHA `<OLD>` -> `<NEW>`).

- [ ] **Step 3: Prepend a `STATE_HISTORY.md` entry** (multi-paragraph `## 2026-07-08 -- HEAT-GAP INDOORS FLIP ...` below the `---`, above the prior entry).

- [ ] **Step 4: Verify coherence**

Run: `cd /Users/trevorrawson/plant-dataset && head -1 LATEST.txt | cut -c6-21 && shasum -a 256 crops_data_final.json | cut -c1-16`
Expected: the two 16-char SHAs match.

- [ ] **Step 5: Commit (held for push)**

```bash
cd /Users/trevorrawson/plant-dataset
git add LATEST.txt CURRENT_STATE.md STATE_HISTORY.md
git commit -m "docs(heat-gap): state trio -- heat-gap indoors flip (22 cells) live

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: plant-astro kickoff (the derived note)

**Files:**
- Create: `docs/kickoffs/17-heat-gap-indoors-note.md`

**Interfaces:** none (handoff doc).

- [ ] **Step 1: Write the kickoff**

Content: what changed in the data (the 22 `indoors` tokens on hot months); the render rule -- an `indoors` calendar month whose index is in the cell's `heat_pause.months` is a *heat-gap* flip and gets the note; the derived note template keyed off `heat_effect` (`crown_failure`->"form heads", `poor_fruit_set`->"set fruit", `quality_loss`->"grow well", `bolting`->"grow without bolting") + `heat_threshold_f` (the transplant temp) + the fall/`second_planting` framing; the optional `heat_gap_note_beginner`/`_seasoned` override slot (not populated yet); dual-register; and the build steps (`npm run build:guides` + `npx jest`).

- [ ] **Step 2: Commit**

```bash
cd /Users/trevorrawson/plant-dataset
git add docs/kickoffs/17-heat-gap-indoors-note.md
git commit -m "docs(kickoff): #17 plant-astro heat-gap indoors note (derived)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:** Component A (flip rule) -> Task 1 + Task 4; Component B (note) -> Task 6 (app-derived, no canonical field, per spec); Component C (gates C1/C2) -> Task 2 (A5) + Task 3 (A5b), both TDD RED-first; Component D (handoff) -> Task 6; scope 22 cells -> Task 4 Step 2 assertion; §8 canonical footprint (only calendar tokens) -> Task 4 Step 3 validator; state trio (content release, CLAUDE.md) -> Task 5. No gaps.

**Placeholder scan:** `<scratchpad>`, `<OLD_SHA>`, `<NEW_SHA>` are runtime values filled at execution, not vague requirements. All code steps show complete code. No TBD/TODO.

**Type consistency:** `indoor_core_months(cell)` defined in Task 1, consumed in Tasks 3 & 4; `heat_flip_backing_violations(crop)` defined in Task 3, wired in Task 3 Step 3; `declared_heat_months`/`core_months`/`_MON_ABBR` are pre-existing in `annual_calendar.py`. `annual_coherence_violations` signature unchanged. Consistent.

## Notes for the executor

- Tasks 1-3 are safe on the current canonical (every existing cell has `flipped == {}`), so `gate_all` stays green after each -- the gate changes precede the data change deliberately.
- Task 4 is the only canonical edit; it and Task 5 are **held uncommitted-to-remote** until Trevor confirms the push (CLAUDE.md).
- The flip is safe to ship ahead of Task 6's app note: an `indoors` token in July is truthful on its own; the note only adds the "why."
