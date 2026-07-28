# Harvest-Duration Reconciliation + `harvest_stop_rule` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make asparagus's three disagreeing harvest-duration layers agree, structure the stop rule that governs them, and close the class with a check that returns zero.

**Architecture:** Extend the existing `tools/harvest_duration_gate.py` with five cross-layer checks (no sixth gate). Add one crop-level field (`harvest_stop_rule`) and one sparse per-cell override (`harvest_duration_weeks`). All canonical writes go through a single SHA-guarded promote script. Asparagus-only pilot; artichoke inherits at its cert.

**Tech Stack:** Python 3 stdlib only (`json`, `re`, `calendar`, `unittest`). No new dependencies. Canonical JSON is COMPACT.

**Spec:** `docs/superpowers/specs/2026-07-27-harvest-duration-reconciliation-design.md`

## Global Constraints

- **Canonical JSON is COMPACT**: `json.dumps(data, separators=(",",":"), ensure_ascii=False)`, **no trailing newline**, never `indent=2`. Never reformat it.
- **Canonical path**: `crops_data_final.json`. Expected SHA at plan start: `a995333fd2c0e15d25c6116691d82225311acb85264441e653bc74faf6bb64ce`.
- **TDD, RED before GREEN.** No production code before a failing test. Adversarially inject each defect class into a SCRATCH COPY and confirm it bounces.
- **No em dashes in consumer copy** (use commas/colons/semicolons/periods). `--` is fine in code comments and docs. American English. Temps render `°F`. "plant" is lowercase except at sentence start.
- **Never `git add -A`.** Use explicit pathspecs. `tools/whole_crop_gate.py` carries another session's uncommitted A48 and must never be staged by this work. Files belonging to the artichoke session and off-limits: `tools/whole_crop_gate.py`, `tools/carveout_dependency_audit.py`, `tools/perennial_harvest_gate.py`, `tools/test_perennial_harvest_gate.py`, `tools/promote_artichoke.py`, `tools/staging/artichoke/`, `tools/staging/shards/`.
- **Trevor approves every commit and confirms every push.** Do not push.
- **Sourcing:** raw bytes only (`urllib` + `pypdf` or tag-stripped HTML). WebFetch summaries of PDFs are NOT sourcing. Cite only documents verified to carry the claim.
- **Run from repo root** `/Users/trevorrawson/plant-dataset`. Tests import via `sys.path.insert(0, str(REPO / "tools"))`.

---

## File Structure

| File | Responsibility |
|---|---|
| `tools/harvest_duration_gate.py` (modify) | All duration-coherence checks. Existing: REACH/END/START per cell. New: RAMP-FIRST, RAMP-PROSE, STOP-SHAPE (crop-level) + OVERRIDE-REACH, OVERRIDE-PROSE (cell-level). |
| `tools/test_harvest_duration_gate.py` (modify) | Tests for all of the above. Existing 12 tests must keep passing. |
| `tools/register_completeness_gate.py` (modify) | One-line ruling: `"signal"` into `EXCLUDED_KEYS`. |
| `tools/staging/harvest_duration/authored.json` (create) | Authored values + per-value source evidence. No canonical write. |
| `tools/promote_harvest_duration_reconciliation.py` (create) | The single SHA-guarded canonical write. |
| `docs/field_addition_register.md` (modify) | New row 27; amend row 26. |
| `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (modify) | State trio. |

---

## Measured Facts (verified before this plan was written — do not re-derive)

- `release_verify` §E does **NOT** flag `harvest_duration_weeks` as a novel region key. Verified by injecting it and running `release_verify`. **No benign-list change is needed.**
- `register_completeness_gate` **HALTs** on `harvest_stop_rule.signal` ("UNRULED harvest_stop_rule.signal"), regardless of whether the value is a sentence or an enum token — the gate is key-based, not value-based. Adding bare `"signal"` to `EXCLUDED_KEYS` returns it to `GATE: PASS`. Both directions verified.
- `signal` appears **0 times** elsewhere in the canonical, so a bare-key ruling is safe. Path-scoping via `EXCLUDED_PATH_SUBSTR` would be **wrong** — it would exclude `harvest_stop_rule.note_beginner`/`note_seasoned`, which must stay checked as dual-register prose.
- `stated_duration(harvest_ready_beginner)` → `(6, 8)`. `stated_duration(harvest_ready_seasoned)` → `None` (its "roughly six-to-eight-week" hyphenated form does not match the parser). Task 2 Step 3 carries a **verified** fix for this, regression-checked across 537 roster-wide harvest clauses.
- 12 of the 15 asparagus cells that state a duration **disagree** with the ramp's mature `[8,10]`; only `ca_interior` z8, `nevada` z8, and `nevada` z9 match it. This is why Task 6 Step 1 exists.
- Asparagus `harvest_ramp_weeks` today: `[{1,[0,0]},{2,[0,2]},{3,[2,4]},{4,[6,8]},{5,[8,10]}]`; `years_to_first_harvest: [2,3]`.
- At commit `6f2b379` the ramp was `[{1,[0,0]},{2,[0,0]},{3,[2,3]},{4,[6,8]},{5,[8,10]}]` — first non-zero bed year **3**, min(`years_to_first_harvest`) **2**.
- Existing public names in `harvest_duration_gate.py`: `MONTHS`, `field_months`, `harvest_clauses`, `stated_duration`, `stated_end`, `stated_start`, `duration_violations`, `main`, `_days_mid_to_first`, `_month`, `_num`.

---

## Task 1: RAMP-FIRST — the ramp must open the door in the first possible harvest year

**Files:**
- Modify: `tools/harvest_duration_gate.py`
- Test: `tools/test_harvest_duration_gate.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `ramp_violations(crop) -> list[str]`. Later tasks call it from `main()`.

**Why "equals the minimum" and not "falls inside":** `field_addition_register.md` row 26 states this check as "must fall inside `years_to_first_harvest`". That formulation **passes on the defect it was written for** — with year 2 at `[0,0]` the first non-zero entry is 3, and 3 is inside `[2,3]`. `years_to_first_harvest: [2,3]` encodes a real source disagreement (UMN/Missouri allow a light second-spring cut; MSU/UNH say wait for year three), and `[0,0]` silently picked year three. Requiring equality with the **minimum** forces the ramp to keep year 2 open, which is what `[0,2]` honestly encodes.

- [ ] **Step 1: Write the failing tests**

Append to `tools/test_harvest_duration_gate.py`:

```python
from harvest_duration_gate import ramp_violations  # noqa: E402

RAMP_OK = [
    {"bed_year": 1, "weeks": [0, 0]}, {"bed_year": 2, "weeks": [0, 2]},
    {"bed_year": 3, "weeks": [2, 4]}, {"bed_year": 4, "weeks": [6, 8]},
    {"bed_year": 5, "weeks": [8, 10]},
]
RAMP_HISTORICAL_DEFECT = [
    {"bed_year": 1, "weeks": [0, 0]}, {"bed_year": 2, "weeks": [0, 0]},
    {"bed_year": 3, "weeks": [2, 3]}, {"bed_year": 4, "weeks": [6, 8]},
    {"bed_year": 5, "weeks": [8, 10]},
]


class RampFirstCheck(unittest.TestCase):
    def test_ramp_opening_later_than_the_earliest_possible_year_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_HISTORICAL_DEFECT,
                "years_to_first_harvest": [2, 3]}
        v = ramp_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-FIRST", v[0])

    def test_ramp_opening_in_the_earliest_possible_year_passes(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "years_to_first_harvest": [2, 3]}
        self.assertEqual(ramp_violations(crop), [])

    def test_crop_without_a_ramp_is_skipped(self):
        self.assertEqual(ramp_violations({"slug": "c"}), [])

    def test_ramp_with_no_nonzero_year_flags(self):
        crop = {"slug": "c",
                "harvest_ramp_weeks": [{"bed_year": 1, "weeks": [0, 0]}],
                "years_to_first_harvest": [2, 3]}
        v = ramp_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-FIRST", v[0])
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_harvest_duration_gate.py RampFirstCheck -v`
Expected: `ImportError: cannot import name 'ramp_violations'`

- [ ] **Step 3: Write the minimal implementation**

Add to `tools/harvest_duration_gate.py`, after `duration_violations`:

```python
def ramp_violations(crop):
    """RAMP-FIRST: the ramp's first harvestable bed year must equal the earliest
    year `years_to_first_harvest` allows. See the module header for why equality,
    not range-containment, is the correct rule."""
    ramp = crop.get("harvest_ramp_weeks")
    ytfh = crop.get("years_to_first_harvest")
    if not isinstance(ramp, list) or not ramp:
        return []
    if not (isinstance(ytfh, list) and len(ytfh) == 2 and all(isinstance(x, int) for x in ytfh)):
        return []
    nonzero = [e["bed_year"] for e in ramp
               if isinstance(e, dict) and isinstance(e.get("weeks"), list)
               and len(e["weeks"]) == 2 and e["weeks"][1] > 0
               and isinstance(e.get("bed_year"), int)]
    if not nonzero:
        return [f"RAMP-FIRST: harvest_ramp_weeks has no bed year with a non-zero max, but "
                f"years_to_first_harvest is {ytfh}, which promises a harvest."]
    first, earliest = min(nonzero), min(ytfh)
    if first != earliest:
        return [f"RAMP-FIRST: harvest_ramp_weeks first opens in bed year {first}, but "
                f"years_to_first_harvest {ytfh} allows a harvest as early as year "
                f"{earliest}. Where the establishment literature disagrees the ramp must "
                f"CARRY THE RANGE (an optional [0, N] year), not collapse to the "
                f"conservative end. This is the year-2 [0,0] defect."]
    return []
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 tools/test_harvest_duration_gate.py RampFirstCheck -v`
Expected: 4 tests PASS.

- [ ] **Step 5: Verify RED against real history**

Run:
```bash
git show 6f2b379:crops_data_final.json | python3 -c "
import json,sys; sys.path.insert(0,'tools')
from harvest_duration_gate import ramp_violations
d=json.load(sys.stdin)
a=[c for c in d['crops'] if c.get('slug')=='asparagus'][0]
print(ramp_violations(a))"
```
Expected: a one-element list containing `RAMP-FIRST`.

Run the same against the live canonical:
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from harvest_duration_gate import ramp_violations
a=[c for c in json.load(open('crops_data_final.json'))['crops'] if c['slug']=='asparagus'][0]
print(ramp_violations(a))"
```
Expected: `[]`.

- [ ] **Step 6: Commit**

```bash
git add tools/harvest_duration_gate.py tools/test_harvest_duration_gate.py
git commit -m "feat(gate): RAMP-FIRST -- the ramp must open in the first possible harvest year"
```

---

## Task 2: RAMP-PROSE — crop prose must not contradict the ramp

**Files:**
- Modify: `tools/harvest_duration_gate.py`
- Test: `tools/test_harvest_duration_gate.py`

**Interfaces:**
- Consumes: `stated_duration` (existing).
- Produces: `ramp_prose_violations(crop) -> list[str]`.

**Note on scope:** compares for **equality**, not overlap. The live contradiction is prose `[6,8]` against ramp mature `[8,10]`; those overlap at 8 but are still two different claims about the same bed. `harvest_ready_seasoned` currently returns `None` from the parser (hyphenated "six-to-eight-week"), so this check fires on the beginner register only. Step 3 extends the parser to handle the hyphenated form; if that proves noisy the check stays beginner-only and the limit is documented in the gate header. Do not silently leave it unhandled.

- [ ] **Step 1: Write the failing tests**

```python
from harvest_duration_gate import ramp_prose_violations  # noqa: E402


class RampProseCheck(unittest.TestCase):
    def test_prose_week_count_disagreeing_with_mature_ramp_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Keep harvesting for about six to eight weeks, then stop."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-PROSE", v[0])

    def test_prose_matching_mature_ramp_passes(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Keep harvesting for eight to ten weeks, then stop."}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_prose_stating_no_week_count_is_silent(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Harvest until the spears thin to pencil width."}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_hyphenated_compound_week_count_is_parsed(self):
        # the harvest_ready_seasoned shape: "a roughly six-to-eight-week spring window"
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_seasoned": "Harvest through a roughly six-to-eight-week spring window."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-PROSE", v[0])
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_harvest_duration_gate.py RampProseCheck -v`
Expected: `ImportError: cannot import name 'ramp_prose_violations'`

- [ ] **Step 3: Extend the parser, then implement**

In `tools/harvest_duration_gate.py`, replace the range branch of `stated_duration` so the hyphenated compound form parses. Current first regex:

```python
        m = re.search(rf"({_NUM_RE})\s*(?:to|-|–)\s*({_NUM_RE})\s+weeks?", seg, re.I)
```

Replace with:

```python
        # "six to eight weeks", "6-8 weeks", and the compound-adjective form
        # "a roughly six-to-eight-week window" (harvest_ready_seasoned's shape).
        # The separator must treat "-to-" as one unit: a bare `-` alternative would
        # consume only the first hyphen and then fail to match "to" as a number.
        m = re.search(rf"({_NUM_RE}){_RANGE_SEP}({_NUM_RE})[-\s]+weeks?", seg, re.I)
```

with this constant added beside the other module constants:

```python
_RANGE_SEP = r"(?:\s+to\s+|\s*-\s*to\s*-\s*|\s*[-–]\s*)"
```

**This exact regex is verified, not proposed.** Measured across the whole roster: 537 harvest
clauses scanned, and it changes exactly **one** result — `asparagus.harvest_ready_seasoned` now
parses to `(6, 8)` where the old pattern returned `None`. Zero regressions anywhere else. It also
correctly declines to match `"up to about ten weeks once the bed is four years old"`, which is a
single value and must not be read as a range.

> A naive first attempt at this fix (`(?:\s+to\s+|-|–)` as the separator) does **not** work and was
> caught by testing it before it reached this plan: the bare `-` alternative matches the first
> hyphen of "six-to-eight", after which the pattern needs "to" to be a number and fails. If you
> change the separator, re-run the roster-wide regression above.

Then add:

```python
def _mature_ramp(crop):
    """The highest authored bed_year's weeks, or None."""
    ramp = crop.get("harvest_ramp_weeks")
    if not isinstance(ramp, list) or not ramp:
        return None
    entries = [e for e in ramp if isinstance(e, dict)
               and isinstance(e.get("bed_year"), int)
               and isinstance(e.get("weeks"), list) and len(e["weeks"]) == 2]
    if not entries:
        return None
    top = max(entries, key=lambda e: e["bed_year"])
    return top["bed_year"], top["weeks"]


def ramp_prose_violations(crop):
    """RAMP-PROSE: a bare week count in the crop's harvest_ready_* prose must equal
    the ramp's mature entry. Equality, not overlap: [6,8] and [8,10] share an
    endpoint and are still two different claims about the same bed."""
    mature = _mature_ramp(crop)
    if mature is None:
        return []
    bed_year, weeks = mature
    out = []
    for reg in ("harvest_ready_beginner", "harvest_ready_seasoned"):
        text = crop.get(reg)
        if not isinstance(text, str):
            continue
        dur = stated_duration(text)
        if dur and list(dur) != list(weeks):
            out.append(
                f"RAMP-PROSE: {reg} states {dur[0]} to {dur[1]} weeks but "
                f"harvest_ramp_weeks bed year {bed_year} says {weeks[0]} to {weeks[1]}. "
                f"Two layers of the same crop make different duration claims; decide "
                f"which is sourced before editing either."
            )
    return out
```

- [ ] **Step 4: Run tests**

Run: `python3 tools/test_harvest_duration_gate.py -v`
Expected: all tests PASS **except** `LiveCanonicalClean`, which is expected RED until Task 6.

Confirm the parser change did not break the existing suite:
Run: `python3 tools/test_harvest_duration_gate.py ReachCheck EndCheck StartCheck Scope HistoricalReproduction -v`
Expected: all PASS.

- [ ] **Step 5: Verify RED on live data**

Run:
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from harvest_duration_gate import ramp_prose_violations
a=[c for c in json.load(open('crops_data_final.json'))['crops'] if c['slug']=='asparagus'][0]
[print(v) for v in ramp_prose_violations(a)]"
```
Expected: at least one `RAMP-PROSE` line (beginner `[6,8]` vs mature `[8,10]`); after the parser fix the seasoned register should also fire.

- [ ] **Step 6: Commit**

```bash
git add tools/harvest_duration_gate.py tools/test_harvest_duration_gate.py
git commit -m "feat(gate): RAMP-PROSE -- crop prose must not contradict its own ramp"
```

---

## Task 3: STOP-SHAPE, OVERRIDE-REACH, OVERRIDE-PROSE

**Files:**
- Modify: `tools/harvest_duration_gate.py`
- Test: `tools/test_harvest_duration_gate.py`

**Interfaces:**
- Consumes: `field_months`, `stated_duration`, `_days_mid_to_first`, `MONTHS` (all existing).
- Produces: `stop_rule_violations(crop) -> list[str]`; `duration_violations` gains override handling.

- [ ] **Step 1: Write the failing tests**

```python
from harvest_duration_gate import stop_rule_violations  # noqa: E402

STOP_OK = {
    "signal": "spear_diameter",
    "threshold_inches": [0.25, 0.5],
    "note_beginner": "Stop cutting when new spears come up about as thick as a pencil.",
    "note_seasoned": "End the season when most spears thin to about pencil diameter.",
    "sources": ["uada_ext"],
}


class StopShapeCheck(unittest.TestCase):
    def test_absent_stop_rule_is_silent(self):
        self.assertEqual(stop_rule_violations({"slug": "c"}), [])

    def test_wellformed_stop_rule_passes(self):
        self.assertEqual(stop_rule_violations({"slug": "c", "harvest_stop_rule": STOP_OK}), [])

    def test_unknown_signal_flags(self):
        r = dict(STOP_OK, signal="vibes")
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("STOP-SHAPE" in x and "signal" in x for x in v), v)

    def test_descending_threshold_flags(self):
        r = dict(STOP_OK, threshold_inches=[0.5, 0.25])
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("threshold_inches" in x for x in v), v)

    def test_missing_register_flags(self):
        r = dict(STOP_OK); del r["note_seasoned"]
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("note_seasoned" in x for x in v), v)

    def test_missing_sources_flags(self):
        r = dict(STOP_OK, sources=[])
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("sources" in x for x in v), v)


class OverrideCheck(unittest.TestCase):
    def test_override_unreachable_within_band_flags(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - Jun",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April.",
        }})
        v = duration_violations(c)
        self.assertTrue(any("REACH" in x for x in v), v)

    def test_override_disagreeing_with_note_flags(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - May",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April; harvest for six to eight weeks into May.",
        }})
        v = duration_violations(c)
        self.assertTrue(any("OVERRIDE-PROSE" in x for x in v), v)

    def test_override_agreeing_with_note_and_band_passes(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - May",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April; harvest for four to six weeks into May.",
        }})
        self.assertEqual(duration_violations(c), [])
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_harvest_duration_gate.py StopShapeCheck OverrideCheck -v`
Expected: `ImportError: cannot import name 'stop_rule_violations'`

- [ ] **Step 3: Implement**

Add near the top of `tools/harvest_duration_gate.py`, beside the other constants:

```python
# Observable stop signals. Extend as archetypes join; an unknown value is a defect,
# because the app dispatches display on it.
STOP_SIGNALS = {"spear_diameter"}
```

Add after `ramp_prose_violations`:

```python
def stop_rule_violations(crop):
    """STOP-SHAPE: harvest_stop_rule, where present, is well-formed. Absence is the
    legitimate N/A branch (a crop with no repeated-cutting season has no stop rule)
    and is silent."""
    rule = crop.get("harvest_stop_rule")
    if rule is None:
        return []
    if not isinstance(rule, dict):
        return ["STOP-SHAPE: harvest_stop_rule must be an object."]
    out = []
    if rule.get("signal") not in STOP_SIGNALS:
        out.append(f"STOP-SHAPE: harvest_stop_rule.signal {rule.get('signal')!r} is not one "
                   f"of {sorted(STOP_SIGNALS)}.")
    t = rule.get("threshold_inches")
    if not (isinstance(t, list) and len(t) == 2
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in t)
            and t[0] <= t[1]):
        out.append(f"STOP-SHAPE: harvest_stop_rule.threshold_inches must be [min, max] "
                   f"non-descending numbers, got {t!r}. Where sources disagree on the number "
                   f"this CARRIES THE RANGE; equal values are allowed when they agree.")
    for k in ("note_beginner", "note_seasoned"):
        if not isinstance(rule.get(k), str) or not rule[k].strip():
            out.append(f"STOP-SHAPE: harvest_stop_rule.{k} must be non-empty dual-register prose.")
    if not rule.get("sources"):
        out.append("STOP-SHAPE: harvest_stop_rule.sources must name at least one source, and only "
                   "documents verified to carry the rule.")
    return out
```

In `duration_violations`, replace the duration-selection line. Current:

```python
            dur = stated_duration(note)
            if dur and m1 != mk:
```

Replace with:

```python
            note_dur = stated_duration(note)
            ov = cell.get("harvest_duration_weeks")
            has_ov = (isinstance(ov, list) and len(ov) == 2
                      and all(isinstance(x, int) for x in ov))
            if has_ov and note_dur and list(note_dur) != list(ov):
                out.append(
                    f"{rk} z{z}: OVERRIDE-PROSE: harvest_duration_weeks is "
                    f"{ov[0]}-{ov[1]} weeks but the note states {note_dur[0]}-{note_dur[1]}. "
                    f"The structured override and the prose must agree."
                )
            # a structured override is authoritative over the note parse for REACH
            dur = tuple(ov) if has_ov else note_dur
            if dur and m1 != mk:
```

- [ ] **Step 4: Run tests**

Run: `python3 tools/test_harvest_duration_gate.py -v`
Expected: all PASS except `LiveCanonicalClean` (expected RED until Task 6).

- [ ] **Step 5: Wire the crop-level checks into `main()`**

In `main()`, replace the per-crop loop body:

```python
    for crop in data["crops"]:
        for v in duration_violations(crop):
```

with:

```python
    for crop in data["crops"]:
        crop_level = (ramp_violations(crop) + ramp_prose_violations(crop)
                      + stop_rule_violations(crop))
        for v in crop_level + duration_violations(crop):
```

- [ ] **Step 6: Run the gate standalone**

Run: `python3 tools/harvest_duration_gate.py`
Expected: non-zero violations (the RAMP-PROSE contradiction), exit 1. This is correct pre-fix state.

- [ ] **Step 7: Commit**

```bash
git add tools/harvest_duration_gate.py tools/test_harvest_duration_gate.py
git commit -m "feat(gate): STOP-SHAPE + per-cell duration overrides, wired into main"
```

---

## Task 4: Rule `signal` into `register_completeness_gate`

**Files:**
- Modify: `tools/register_completeness_gate.py:35` (the `EXCLUDED_KEYS` set)

**Interfaces:** none.

**Why a bare key and not a path:** `signal` appears 0 times elsewhere in the canonical. Path-scoping via `EXCLUDED_PATH_SUBSTR` would exclude the whole `harvest_stop_rule` subtree **including `note_beginner`/`note_seasoned`**, which must stay checked as dual-register prose. This ruling is the same class as `day_length_type`, `cold_hardiness_class`, and `bearing_habit`.

- [ ] **Step 1: Reproduce the HALT on a scratch canonical**

```bash
python3 - <<'EOF'
import json
d = json.load(open('crops_data_final.json', encoding='utf-8'))
a = [c for c in d['crops'] if c['slug'] == 'asparagus'][0]
a['harvest_stop_rule'] = {"signal": "spear_diameter", "threshold_inches": [0.25, 0.5],
                          "note_beginner": "x.", "note_seasoned": "y.", "sources": ["uada_ext"]}
open('/tmp/scratch_signal.json', 'w', encoding='utf-8', newline='').write(
    json.dumps(d, separators=(",", ":"), ensure_ascii=False))
EOF
python3 tools/register_completeness_gate.py /tmp/scratch_signal.json | grep -E "UNRULED|GATE:"
```
Expected: `UNRULED  harvest_stop_rule.signal` and `GATE: HALT`.

- [ ] **Step 2: Add the ruling**

In `tools/register_completeness_gate.py`, inside `EXCLUDED_KEYS`, next to the ENUM / CN-PRIMITIVE block:

```python
    # `harvest_stop_rule.signal` ruled 2026-07-27: an ENUM naming the observable a
    # grower watches (spear_diameter), machinery the app dispatches display on --
    # not consumer prose. The rule's consumer copy lives in the sibling dual-register
    # note_beginner/note_seasoned, which stay checked. Ruled as a BARE key (0 other
    # `signal` keys exist); a path-scoped rule would wrongly exclude those notes too.
    "signal",
```

- [ ] **Step 3: Verify GREEN**

Run: `python3 tools/register_completeness_gate.py /tmp/scratch_signal.json | grep -E "UNRULED|GATE:"`
Expected: `GATE: PASS`, no UNRULED line.

Run against the live canonical to confirm no regression:
Run: `python3 tools/register_completeness_gate.py | tail -2`
Expected: `GATE: PASS`.

- [ ] **Step 4: Commit**

```bash
git add tools/register_completeness_gate.py
git commit -m "chore(register): rule harvest_stop_rule.signal as enum machinery"
```

---

## Task 5: Source verification and authoring (NO canonical write)

**Files:**
- Create: `tools/staging/harvest_duration/authored.json`

**Interfaces:**
- Produces: a staging document consumed by Task 6's promote script, shaped:
  ```jsonc
  {
    "harvest_stop_rule": { ... },              // the crop-level object
    "ramp_mature": [6, 10],                    // proposed replacement for bed_year 5
    "harvest_ready_beginner": "...",           // repaired prose
    "harvest_ready_seasoned": "...",
    "cell_overrides": { "mid_south": { "7": [4, 6] } },   // region -> zone -> weeks
    "evidence": { "<claim-id>": {"source": "...", "url": "...", "quote": "..."} }
  }
  ```

**The 12 override candidates** (cells whose note states a duration differing from the crop ramp). A cell gets an override **only** if a cited source states a regional duration when read raw. Cells where it does not: leave absent, inheriting the crop default.

| cell | note says | cited sources |
|---|---|---|
| `mid_atlantic` z7 | 6-10 wk | `rutgers_njaes`, `umd_ext` |
| `mid_atlantic` z8 | 6-8 wk | `umd_ext`, `rutgers_njaes` |
| `mid_south` z7 | 4-6 wk | `uada_ext`, `mu_ext` |
| `northern_tier` z3 | 6 wk | `umn_ext`, `msu_ext`, `ndsu_ext`, `sdsu_ext` |
| `northern_tier` z4 | 6-8 wk | `umn_ext`, `msu_ext`, `umaine_ext` |
| `northern_tier` z5 | 6-8 wk | `umn_ext`, `msu_ext`, `iastate_ext`, `illinois_ext` |
| `northern_tier` z6 | 6-8 wk | `msu_ext`, `umn_ext`, `uconn_ext`, `illinois_ext` |
| `northern_tier` z7 | 6-8 wk | `msu_ext`, `umn_ext`, `mu_ext` |
| `pnw` z8 | 6-8 wk | `osu_ext`, `wsu_ext`, `wsu_em051e` |
| `se_gulf` z8 | 6-8 wk | `uc_ipm`, `uga_b577` |
| `utah_dixie` z8 | 6-8 wk | `usu_ext`, `usu_ext_veg_dates`, `usu_washco_dates` |
| `warm_arid` z8 | 10 wk | `nmsu_ext`, `nmsu_chart` |

Cells matching the ramp and needing no override: `ca_interior` z8, `nevada` z8, `nevada` z9.

- [ ] **Step 1: Fetch and verify the stop-rule sources raw**

Write `tools/staging/harvest_duration/fetch.py` (throwaway, not committed):

```python
import urllib.request, re, html, sys

def text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    if url.endswith(".pdf") or raw[:4] == b"%PDF":
        open("/tmp/f.pdf", "wb").write(raw)
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader("/tmp/f.pdf").pages)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw.decode("utf-8", "ignore"),
               flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))

for url in sys.argv[1:]:
    t = text(url)
    print(f"===== {url}  (asparagus mentions: {len(re.findall('asparagus', t, re.I))})")
    for s in re.split(r"(?<=[.])\s", t):
        if re.search(r"pencil|diameter|cease|stop", s, re.I) and re.search(r"spear|harvest", s, re.I):
            print("  *", s.strip()[:240])
```

Run it against every candidate. **Already confirmed to carry the rule:** `uada_ext`
(`https://www.uaex.uada.edu/publications/PDF/FSA-6002.pdf`, states it three times, e.g. *"When the diameter of the spears is less than the size of a pencil, cease harvesting."*).
**Already known problematic:** `msu_ext` (`https://www.canr.msu.edu/resources/asparagus_in_the_home_garden`) returns an 83-character JS shell with zero asparagus content when fetched raw — it CANNOT be verified this way, so it must NOT be cited on the stop rule. `umn_ext` did not state the pencil rule in the text fetched.

- [ ] **Step 2: Record every claim with its quote**

Populate `evidence` in `authored.json`. Every entry needs source id, URL, and the verbatim sentence. **A claim with no quote does not ship.** This crop has produced five confirmed instances of a real T1 document cited for a claim it does not make.

- [ ] **Step 3: Author `harvest_stop_rule`**

Dual-register, no em dashes, "plant" lowercase, American English. `threshold_inches` carries the range `[0.25, 0.5]` (NMSU ¼ in, current prose ⅜ in, UC Sonoma ½ in — three T1 institutions, three numbers). `signal` is `"spear_diameter"`.

- [ ] **Step 4: Author the cell overrides**

For each of the 12, read the cited sources raw and record either an override with its quote, or an explicit "no regional duration stated — inherits crop default" note in `evidence`. **Do not invent differentiation.** `nevada` z8/z9/z10 and `ca_interior` z8/z9 carry identical values across real gradients and are honest as labeled; they stay that way.

- [ ] **Step 5: Author the ramp-mature and prose repairs**

See Task 6 Step 1 for the ramp-mature decision, which needs Trevor's sign-off before it is written.

Repaired `harvest_ready_*` must be bed-year aware and defer to the stop rule so it states no bare flat week count (which makes RAMP-PROSE silent by design, not by accident).

- [ ] **Step 6: Commit the staging document**

```bash
git add tools/staging/harvest_duration/authored.json
git commit -m "data(asparagus): stage authored stop rule + duration overrides with per-claim evidence"
```

---

## Task 6: The guarded promote

**Files:**
- Create: `tools/promote_harvest_duration_reconciliation.py`
- Modify: `crops_data_final.json` (the single canonical write)

**Interfaces:**
- Consumes: `tools/staging/harvest_duration/authored.json`; `ramp_violations`, `ramp_prose_violations`, `stop_rule_violations`, `duration_violations` from Task 1-3; `zone_order_violations` from `tools/zone_order_gate.py`.

- [ ] **Step 1: Get Trevor's ruling on the ramp mature value — BLOCKING**

Present this and wait:

> `harvest_ramp_weeks` bed year 5 is `[8, 10]`. Across the sources the mature figure spans **6 to 10** (UMN 6-8, UGA C1026 6-8, MSU "up to 8", USU "up to 8", Illinois 8-10, UC ANR 7234 8-10, UC MG statewide "6 to 10", NMSU max 10). `[8,10]` therefore collapsed a 6-to-10 span to its upper end. That is the same false-precision error as the year-2 `[0,0]` collapse, in the same field. 12 of the 15 cells that state a duration disagree with `[8,10]`; only the three California/Nevada cells match it.
> Proposed: bed year 5 becomes `[6, 10]`, the honest national default, with regional cells narrowing it where sourced.

Do not proceed without an answer. If Trevor declines, drop the ramp change from the promote and record why in `evidence`.

- [ ] **Step 2: Write the promote script**

Model it exactly on `tools/promote_harvest_duration_pass.py` (same repo, written today). It must:
1. Assert the canonical SHA equals `a995333fd2c0e15d25c6116691d82225311acb85264441e653bc74faf6bb64ce` (or whatever HEAD is at the time — read it, do not guess) and abort otherwise.
2. Assert `len(data["crops"]) == 128` and exactly one asparagus crop.
3. Assert **every** expected pre-state value on every field it will touch, and abort on drift.
4. Assert a set of untouched reference cells (`ca_interior` z8, `nevada` z8, `nevada` z9 — the three that need no override).
5. Apply from `authored.json`.
6. Assert **after** applying, before writing, that all of these return `[]`: `ramp_violations`, `ramp_prose_violations`, `stop_rule_violations`, `duration_violations`, `zone_order_violations`.
7. Append a resolved `open_findings` entry describing the arc.
8. Write COMPACT with no trailing newline; abort if a trailing newline would be written.
9. Default to dry run; `--write` to apply.

- [ ] **Step 3: Dry run**

Run: `python3 tools/promote_harvest_duration_reconciliation.py`
Expected: SHA OK, pre-state OK, reference OK, all invariants return 0, `DRY RUN` banner, canonical unchanged (`shasum -a 256 crops_data_final.json` still the pre-state SHA).

- [ ] **Step 4: Apply, then prove the abort**

```bash
python3 tools/promote_harvest_duration_reconciliation.py --write
python3 tools/promote_harvest_duration_reconciliation.py ; echo "exit=$?"
```
Expected: first writes and prints the SHA transition; second prints `ABORT: canonical SHA ... != expected ...` and `exit=1`.

- [ ] **Step 5: Drive the gate to zero**

Run: `python3 tools/harvest_duration_gate.py`
Expected: `0 violation(s)`, exit 0.

Run: `python3 tools/test_harvest_duration_gate.py`
Expected: **all** tests PASS, including `LiveCanonicalClean`.

- [ ] **Step 6: Adversarial injection on a scratch copy**

Inject each defect into a deep copy of the repaired asparagus crop and confirm every one bounces: re-widen a repaired band; set ramp year 2 back to `[0,0]`; put a bare "six to eight weeks" back into `harvest_ready_beginner`; set an override that disagrees with its note; set `signal` to an unknown token; set `threshold_inches` to a scalar. Print CAUGHT/MISSED per injection and require 6/6.

- [ ] **Step 7: Full gauntlet**

```bash
python3 tools/whole_crop_gate.py asparagus | tail -3
python3 tools/gate_all.py | tail -2
python3 tools/harvest_duration_gate.py
python3 tools/zone_order_gate.py
python3 tools/prose_window_sweep.py | tail -2
python3 tools/register_completeness_gate.py | tail -2
git show HEAD:crops_data_final.json > /tmp/base.json
python3 tools/release_verify.py crops_data_final.json --base /tmp/base.json --slug asparagus | tail -3
```
Expected: gate PASS, 120/120, 0, 0, 0, PASS, CLEAN.

- [ ] **Step 8: Footprint diff**

Diff the pre-state canonical against the new one key-by-key and confirm **only** the intended fields moved: `harvest_stop_rule` (added), `harvest_ramp_weeks` bed year 5 (if approved), `harvest_ready_beginner`/`_seasoned`, the authored `harvest_duration_weeks` keys, and one `open_findings` append. Nothing else.

- [ ] **Step 9: Commit**

```bash
git add crops_data_final.json tools/promote_harvest_duration_reconciliation.py
git commit -m "data(asparagus): reconcile the three duration layers + structure the stop rule"
```

---

## Task 7: Register rows and the state trio

**Files:**
- Modify: `docs/field_addition_register.md`, `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`

**Interfaces:** none.

- [ ] **Step 1: Add register row 27 and amend row 26**

Row 27 (`harvest_stop_rule`): status PILOT COMPLETE asparagus-only; trigger for rollout = artichoke certifies (the archetype's only other member), authored **natively at its cert** per the method doc §2.5, not by backfill; hard-flip = fold STOP-SHAPE into A39 when the archetype has two members.

Row 26 amendment: record the **regional axis** the row missed, and correct its stated coherence check from "falls inside `years_to_first_harvest`" to "**equals the minimum of**", noting that the original formulation passes on the very defect it was written for.

- [ ] **Step 2: State trio**

`CURRENT_STATE.md` is **hand-maintained** — a naive `gen_current_state.py` regen would corrupt it (no `---` separator). Prepend the new entry at line 1 and surgically update the `- **Current SHA:**` line. Append the same entry at the top of `STATE_HISTORY.md`'s stack, below the `---`. Rewrite `LATEST.txt` with the new SHA, date, and session summary.

- [ ] **Step 3: Verify the trio agrees**

```bash
shasum -a 256 crops_data_final.json
head -2 LATEST.txt
awk 'NR==1 {print substr($0,1,80)}' CURRENT_STATE.md
```
Expected: the SHA in `LATEST.txt` matches `shasum`, and both state files lead with the new entry.

- [ ] **Step 4: Commit**

```bash
git add docs/field_addition_register.md CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "docs: register row 27 (harvest_stop_rule) + row 26 amendment + state trio"
```

- [ ] **Step 5: Hand off**

Summarize for Trevor: what changed, gauntlet results, that nothing is pushed, and that plant-app's `guides.json` needs `npm run build:guides` to pick this up. Do not push.

---

## Self-Review

**Spec coverage:** §3.1 `harvest_stop_rule` → Tasks 3, 4, 5, 6. §3.2 `harvest_duration_weeks` → Tasks 3, 5, 6. §3.3 prose repair → Tasks 2, 5, 6. §4 gate (RAMP-FIRST, RAMP-PROSE, OVERRIDE-REACH, OVERRIDE-PROSE, STOP-SHAPE) → Tasks 1, 2, 3. §4 TDD/RED-pinning → Task 1 Step 5, Task 2 Step 5. §4 adversarial injection → Task 6 Step 6. §5 scope and register → Task 7. §6 consumer → Task 7 Step 5. §7 risks → Task 5 Steps 2 and 4.

**Added beyond the spec:** the `signal` register ruling (Task 4) — discovered by measurement after the spec was written; the gate HALTs without it. And the ramp-mature repair (Task 6 Step 1) — the spec assumed the prose was the wrong half, but 12 of 15 cells and the source span both say the ramp is.

**Type consistency:** `ramp_violations`, `ramp_prose_violations`, `stop_rule_violations`, `duration_violations` all take a crop dict and return `list[str]`. `_mature_ramp` returns `(bed_year, weeks)` or `None` and is used only by `ramp_prose_violations`. `STOP_SIGNALS` is a set of str. `crop()` and `RAMP_OK`/`STOP_OK` are test helpers defined before first use.

**Known gap, deliberately recorded:** RAMP-PROSE depends on `stated_duration` parsing prose. Task 2 Step 3 extends it to the hyphenated compound form and Step 1 pins that with a test. Any prose phrasing outside those two forms is unparsed and therefore unchecked; the gate header must say so rather than implying total coverage.
