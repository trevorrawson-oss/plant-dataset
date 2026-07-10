# Sweet-Corn GS Arc — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify the existing `sweet-corn` shell as a `verified_gs_arc` (count stays 125), and add one net-new conditional field — `planting_layout` — with a light TDD gate, following the dry-bean greenfield playbook.

**Architecture:** Corn is a frost-anchored, direct-sown annual — it rides the existing annual gate set (calendar_basis stays `frost_anchored`; NO new archetype/structural/calendar/derive gate). The only new schema is the `planting_layout` conditional field (`block` on corn, absent elsewhere) + `pollination_block_min_rows`, guarded by a new `planting_layout_gate` wired into `whole_crop_gate` as A44 and run roster-wide by `gate_all`. Sweet-corn carries a milk-stage `harvest` ladder (no dry_down), succession `suitable:true`, and su/se/sh2 varieties.

**Tech Stack:** Python 3 (stdlib only); tests are standalone self-executing scripts (bare `assert` statements + a final `print("... OK")`, run via `python3 tools/test_X.py` -- NO pytest, per the repo's documented convention, `docs/superpowers/plans/2026-06-08-tooling-hardening.md`); the repo's gate suite (`whole_crop_gate.py`, `gate_all.py`, `release_verify.py`), `apply_patch.py` (SHA-guarded COMPACT splicer), JSONPath batches under `tools/batches/`.

**Design spec:** `docs/superpowers/specs/2026-07-10-corn-grass-archetype-design.md`. **Kickoff:** `docs/kickoffs/21-corn-grass-archetype.md`. **Primary precedent:** the dry-bean plan `docs/superpowers/plans/2026-07-09-dry-bean-gs-anchor.md`.

## Global Constraints

- **Canonical JSON is COMPACT:** written with `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it. (CLAUDE.md hard rule.)
- **READ-ONLY on `crops_data_final.json` until the explicit splice task (Task 6).** All authoring happens in scratch files first.
- **TDD: RED before GREEN.** The new gate is not trusted until every defect class in its adversarial set bounces on a SCRATCH COPY of the real canonical (Task 2 + Task 5). (CLAUDE.md hard rule.)
- **No em dashes in consumer copy** (use commas/colons/semicolons/periods). American English. Temps render as `°F`. "plant" is lowercase except at sentence start or in "Plant Pro". (`--` is fine in code/docs/commits.)
- **Release verification before promote (protocol #6):** `whole_crop_gate` PASS on sweet-corn (18/18) + `tools/gate_all.py` (whole suite on EVERY certified crop) + `tools/release_verify.py` + the source-truth sample. A green single gate is NOT a clean release.
- **State trio at content release:** update `CURRENT_STATE.md` (memory `current-state-md-drift`: no `---` separator; hand-maintain surgically, do NOT naively regen), append `STATE_HISTORY.md` (most-recent first), bump `LATEST.txt` (SHA + session).
- **Count stays 125.** `sweet-corn` already exists as a shell; this arc PROMOTES it (shell → certified). The splice is a `replace` on the existing object, NOT an `add`. Footprint = exactly sweet-corn changed, all 124 others byte-identical.
- **Commit on `main`; do NOT push.** Trevor confirms every push. Commit co-author line: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- **Re-baseline the splice `base_sha`** against the live canonical at Task 6 time (`shasum -a 256 crops_data_final.json`); do not hardcode a stale SHA.
- **`planting_layout` enum (fixed, forward-compatible with the planner arc):** `{block, row, hill, grid, single}`. Only `block` is populated in this arc; the rest are defined-but-unused.

---

### Task 1: T1 source research + data pinning

**Files:**
- Create: `docs/reviews/notes/2026-07-10/sweet_corn.md` (research note)

**Interfaces:**
- Produces: `sweet_corn.md` — a `field | value | source | source_id | url` table that every later authoring task reads. No code depends on it; it is the provenance ledger.

- [ ] **Step 1: Fetch the T1 sweet-corn sources.** Use WebFetch on university-extension / .gov sweet-corn pages (e.g. UC ANR / UMN Extension / Cornell / UGA / Univ. of Illinois sweet-corn; regional pages for the 10 regions). Capture: spacing (in-row + note that rows go in a BLOCK ≥4), DTM by sugar type (su / se / sh2), germination temp range, milk-stage harvest cue, per-stage watering (silking = the critical-moisture window), climate thresholds (heat/frost/chilling), and the cross-pollination isolation fact.

- [ ] **Step 2: Extract + pin each number to its source.** Write `sweet_corn.md` as a table: `field | value | source | source_id | url`. Include: `spacing_inches`, `days_to_maturity` (+ `_mid`, per sugar type), `germination_temp_f`, `planting_layout=block`, `pollination_block_min_rows=4`, the 7 `growth_stages` day-ranges, `heat_threshold_f`/`heat_effect`/`frost_tolerance_f`/`frost_effect`/`chilling_sensitivity_f`, and the 3+ variety DTMs (one su, one se, one sh2).

- [ ] **Step 3: List catalog gaps.** In `sweet_corn.md`, list which cited `source_id`s already exist in `crops_data_final.json`'s `source_catalog` vs. which are new (grep the catalog). New ones become `add` ops in the Task 6 batch.

- [ ] **Step 4: Commit the research note.**

```bash
git add docs/reviews/notes/2026-07-10/sweet_corn.md
git commit -m "docs(sweet-corn): T1 sources + pinned figures (block planting, milk-stage, su/se/sh2 DTM)"
```

---

### Task 2: Build `planting_layout_gate` (TDD) + wire A44

**Files:**
- Create: `tools/planting_layout_gate.py`
- Create: `tools/test_planting_layout_gate.py`
- Modify: `tools/whole_crop_gate.py` (insert the A44 block immediately after the A43 block, ~line 660)

**Interfaces:**
- Produces: `planting_layout_gate.check_crop(crop) -> list[str]` (violation strings; empty == clean). `whole_crop_gate` A44 consumes it as `from planting_layout_gate import check_crop as _layout_violations`.

- [ ] **Step 1: Write the failing test.** Create `tools/test_planting_layout_gate.py` as a standalone
self-executing script (bare `assert` + a final `print("... OK")`, run via `python3 tools/test_X.py` --
NO pytest, per the repo convention, `docs/superpowers/plans/2026-06-08-tooling-hardening.md:9`):

```python
#!/usr/bin/env python3
"""Tests for the planting_layout conditional-field gate (A44). Run:
    python3 tools/test_planting_layout_gate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from planting_layout_gate import check_crop


def C(**kw):
    base = {"slug": "x"}
    base.update(kw)
    return base


# ---- clean fixtures (-> no violations) ----
assert check_crop(C()) == [], "absent planting_layout should no-op"
assert check_crop(C(planting_layout=None)) == [], "null planting_layout should no-op"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=4)) == [], \
    "block with a valid min_rows should pass"
assert check_crop(C(planting_layout="row")) == [], "valid row with no min_rows should pass"

# ---- defect injections (-> violation) ----
assert check_crop(C(planting_layout="block")) != [], "block without min_rows should fail"
assert check_crop(C(planting_layout="blocks")) != [], "bad enum value should fail"
assert check_crop(C(planting_layout="row", pollination_block_min_rows=4)) != [], \
    "min_rows present on a non-block layout should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=1)) != [], \
    "min_rows below the floor (2) should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows="4")) != [], \
    "min_rows as a string (non-int) should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=True)) != [], \
    "min_rows as a bool should fail (bool is an int subclass -- guard it)"
assert check_crop(C(pollination_block_min_rows=4)) != [], \
    "orphan min_rows with no planting_layout should fail"

# bad enum + bad min_rows together -> enum check short-circuits -> exactly 1 violation
assert len(check_crop({"slug": "x", "planting_layout": "blocks", "pollination_block_min_rows": 1})) == 1, \
    "bad enum plus bad min_rows should short-circuit to exactly 1 violation"

print("planting_layout_gate tests: OK")
```

- [ ] **Step 2: Run the test to verify it fails.**

Run: `python3 tools/test_planting_layout_gate.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'planting_layout_gate'`.

- [ ] **Step 3: Write the gate.** Create `tools/planting_layout_gate.py`:

```python
#!/usr/bin/env python3
"""planting_layout_gate -- validates the conditional planting_layout field (spec 2026-07-10).

Fields (crop-level):
  planting_layout : enum {block, row, hill, grid, single}. Present ONLY where a crop has a
                    non-default spatial planting pattern the app should render; ABSENT (not null)
                    on every crop that uses standard row spacing. Corn is the only 'block' member
                    (wind pollination -> plant a block of short rows, not one long row).
  pollination_block_min_rows : int >= 2, present IFF planting_layout == 'block' (corn = 4).

Checks (HARD, fire ONLY when planting_layout is present -- unauthored roster stays green; ABSENCE is
never a violation, matching the divide_every_years / chill conditional-field precedent):
  - planting_layout enum membership.
  - block <-> pollination_block_min_rows coherence: 'block' requires the int (>= 2); any non-'block'
    value requires min_rows ABSENT; an orphan min_rows with no layout bounces.

The other enum values (row/hill/grid/single) are DEFINED but unpopulated in this roster -- reserved
for the future garden-planner arc (memory planner-data-model-arc), which takes planting_layout
roster-wide and adds row_spacing + height. NOT an A39 register field (stays conditional).

Usage:
  planting_layout_gate.py [PATH]        # validate (default crops_data_final.json)
  planting_layout_gate.py --coverage    # coverage report + validate
"""
import json
import sys

LAYOUTS = {"block", "row", "hill", "grid", "single"}
MIN_ROWS_FLOOR = 2


def check_crop(c):
    """Return list of violation strings for one crop (empty == clean). No-op off scope."""
    slug = c.get("slug") or c.get("id")
    v = []
    pl = c.get("planting_layout")
    has_mr = "pollination_block_min_rows" in c
    mr = c.get("pollination_block_min_rows")

    # --- no-op off scope: field absent or null ---
    if not c.get("planting_layout"):
        if has_mr and mr is not None:
            v.append(f"{slug}: pollination_block_min_rows present but planting_layout absent/null")
        return v

    # --- enum membership ---
    if pl not in LAYOUTS:
        v.append(f"{slug}: planting_layout {pl!r} not in {sorted(LAYOUTS)}")
        return v  # cannot reason about coherence on a bad enum

    # --- block <-> min_rows coherence ---
    if pl == "block":
        if not has_mr or mr is None:
            v.append(f"{slug}: planting_layout 'block' but pollination_block_min_rows missing")
        elif isinstance(mr, bool) or not isinstance(mr, int) or mr < MIN_ROWS_FLOOR:
            v.append(f"{slug}: pollination_block_min_rows {mr!r} not an int >= {MIN_ROWS_FLOOR}")
    else:
        if has_mr and mr is not None:
            v.append(f"{slug}: planting_layout {pl!r} (not 'block') but pollination_block_min_rows present")
    return v


def coverage(crops):
    cov = {k: [] for k in LAYOUTS}
    cov["absent"] = []
    for c in crops:
        slug = c.get("slug") or c.get("id")
        pl = c.get("planting_layout")
        if not pl:
            cov["absent"].append(slug)
        elif pl in cov:
            cov[pl].append(slug)
        else:
            cov["absent"].append(slug)  # bad value: check_crop flags shape; not counted here
    return cov


def main():
    args = list(sys.argv[1:])
    show_cov = "--coverage" in args
    args = [a for a in args if a != "--coverage"]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    violations = []
    for c in crops:
        violations += check_crop(c)

    if show_cov:
        cov = coverage(crops)
        print(f"COVERAGE (of {len(crops)} crops):")
        print("  planting_layout: " + " | ".join(
            f"{k} {len(cov[k])}" for k in ["block", "row", "hill", "grid", "single", "absent"]))
        for k in ["block", "row", "hill", "grid", "single"]:
            if cov[k]:
                print(f"    {k}: {sorted(cov[k])}")

    if violations:
        print(f"\nplanting_layout_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nplanting_layout_gate: PASS (0 violations)")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the test to verify it passes.**

Run: `python3 tools/test_planting_layout_gate.py`
Expected: prints `planting_layout_gate tests: OK` and exits 0 (12 assertions, all pass).

- [ ] **Step 5: Prove it no-ops on the live roster.**

Run: `python3 tools/planting_layout_gate.py --coverage`
Expected: `PASS (0 violations)` and `planting_layout: block 0 | ... | absent 125` (no crop carries the field yet).

- [ ] **Step 6: Wire A44 into `whole_crop_gate`.** In `tools/whole_crop_gate.py`, immediately AFTER the A43 block (the `for m in _dmx: fail(f"demux: {m}")` loop, ~line 660) and BEFORE the `# ---------------- A24. annual calendar token PLACEMENT` comment, insert:

```python
# ---------------- A44. planting_layout conditional field (spec 2026-07-10) ----------------
# Corn's block-planting fact, structured. No-op off scope (absent/null planting_layout). Enforces
# enum membership + block<->pollination_block_min_rows coherence. Conditional field, NOT an A39
# register requirement -- absence is never a violation (planner arc may promote it later).
from planting_layout_gate import check_crop as _layout_violations
print("A44. planting_layout conditional field (enum + block<->min_rows coherence; no-op off scope)")
_layout = _layout_violations(crop)
print(f"  planting_layout violations: {len(_layout)}")
for m in _layout:
    fail(f"planting_layout: {m}")
```

- [ ] **Step 7: Confirm the wired gate no-ops roster-wide (gate_all still green).**

Run: `python3 tools/gate_all.py`
Expected: `gate_all: ran whole_crop_gate on 115 certified crop(s)` with PASS (A44 prints `planting_layout violations: 0` for every crop; no regression).

- [ ] **Step 8: Commit the gate + wiring.**

```bash
git add tools/planting_layout_gate.py tools/test_planting_layout_gate.py tools/whole_crop_gate.py
git commit -m "feat(gate): A44 planting_layout conditional field gate (TDD; no-op off scope)"
```

---

### Task 3: Author the crop record — core (non-regional)

**Files:**
- Create: `scratch/sweet_corn.json` (the fully-authored sweet-corn object, built in the scratchpad)

**Interfaces:**
- Consumes: `sweet_corn.md` (Task 1 pinned figures); the `green-beans-bush` record as the warm-season-annual shape template.
- Produces: `scratch/sweet_corn.json` — the complete authored `sweet-corn` crop object (core fields; regions added in Task 4).

- [ ] **Step 1: Extract the current shell + the template.** Pull the exact current `sweet-corn` object (this is the Task 6 `from`-guard) and the `green-beans-bush` object (shape template) into scratch:

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); m={c['slug']:c for c in d['crops']}; \
open('scratch/sweet_corn_shell.json','w').write(json.dumps(m['sweet-corn'],ensure_ascii=False,indent=2)); \
open('scratch/green_beans_bush.json','w').write(json.dumps(m['green-beans-bush'],ensure_ascii=False,indent=2))"
```

- [ ] **Step 2: Re-author identity + inherited-but-verified fields** into `scratch/sweet_corn.json` (start from the shell, fill placeholders): set `archetype` → `"warm_season_grass"`; keep `calendar_basis` `"frost_anchored"`, `perennial` `false`; fill `spacing_inches`, `days_to_maturity` (+ `days_to_maturity_mid`), `germination_temp_f` from `sweet_corn.md`; verify `sunlight`/`ph`/`soil`/`water`/`pests`/`diseases`/`companions`/`rotation` are true for sweet corn (corrections from prose where needed).

- [ ] **Step 3: Add the `planting_layout` field.** Set `"planting_layout": "block"` and `"pollination_block_min_rows": 4` (from `sweet_corn.md`). Author the "why/how" into the spacing + soil-prep + a tips-by-stage entry (consumer voice, no em dashes): wind pollination, tassel drops pollen onto silks, plant a block of at least 4 short rows (a 4 by 4 grid beats one long row), and keep sweet corn away from popcorn or field corn so the kernels do not turn starchy.

- [ ] **Step 4: Author the register stack** (spec §7, per-field from `sweet_corn.md`): `germination_light` (neutral — large seed, not light-dependent), `seedling_light` (`na` — direct-sown; set `weeks_indoors` 0/null accordingly), `tray_sowing` (`na`) — NO `pot_up` (na has none); climate thresholds `heat_threshold_f`/`heat_effect`/`frost_tolerance_f` (`frost_effect: killed`, frost-tender)/`chilling_sensitivity_f`; `pet_safe`. Confirm each satisfies its A39/A41/A42 shape (the gates are the backstop in Task 5/7).

- [ ] **Step 5: Author the 7-stage `growth_stages` ladder** (spec §5). Ladder ids IN ORDER: `germination → seedling → vegetative → tasseling → silking → kernel_fill → harvest`. Each stage carries the STANDARD per-stage shape: `id`, `name` (humanized: Germination/Seedling/Vegetative/Tasseling/Silking/Kernel Fill/Harvest), `day_range_from_sow` (monotonic bounds -- both ends non-decreasing; adjacent windows MAY overlap, the green-beans-bush/dry-bean convention -- from `sweet_corn.md`), `audience` (`core`), `user_action_seasoned`/`user_action_beginner`, `what_to_look_for_seasoned`/`what_to_look_for_beginner`, `log_prompt_seasoned`/`log_prompt_beginner`. `harvest` = the MILK stage (squeeze a kernel, it runs milky; silks brown). The `harvest` id is the A40 anchor (ladder-monotonicity + DTM band anchor). NO `dry_down`/`cure_thresh`. Reference the cherry-tomato/beefsteak per-stage shape for the copy voice.

- [ ] **Step 6: Author the harvest-model deltas** (spec §5): `watering.schedule_by_stage[]` per-stage from sweet corn's own prose (silking/tasseling = the critical-moisture window — poor pollination + kernel fill if dry); `storage` (fresh, short window — the sugar-to-starch clock, esp. `su` types); `harvest_urgency`/`harvest_ready_*` for the milk-stage cue.

- [ ] **Step 7: Author `varieties.recommended[]`** = a representative su (standard), se (sugary-enhanced), sh2 (supersweet), each with its `days_to_maturity` and the sugar-genetics note (per the Master Crop List: su/se/sh2 is the real variety driver). Set `varieties.note_seasoned`/`note_beginner` explaining the sugar-type tradeoff (su = classic corn flavor, shorter hold; sh2 = holds sweetness longest, needs isolation + warmer soil to germinate). Fill `thinning` (block thinning to final in-row spacing).

- [ ] **Step 8: Set `succession_policy`.** `suitable: true` (green-beans model — stagger sowings or use differing-maturity varieties); fill `interval_weeks`/`window_type`/`tip_*` from prose. Note in the tip that you stagger BLOCKS, not single rows. Confirm the A43 shape: succession here is same-plant staggering, not a discrete `second_planting{}` — mirror `green-beans-bush` (no `second_planting`).

- [ ] **Step 9: Shape-check the object early** (before regions) by splicing into a throwaway scratch and running the register-shape gates (regions still absent → region gates will flag; that is expected until Task 4):

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); \
sc=json.load(open('scratch/sweet_corn.json')); \
d['crops']=[sc if c['slug']=='sweet-corn' else c for c in d['crops']]; \
json.dump(d, open('scratch/canon_core.json','w'), ensure_ascii=False, separators=(',',':'))"
python3 tools/register_completeness_gate.py scratch/canon_core.json || true
python3 tools/planting_layout_gate.py scratch/canon_core.json
```
Expected: `planting_layout_gate: PASS`; register_completeness clean for the authored fields.

- [ ] **Step 10: Commit the core draft.**

```bash
git add scratch/sweet_corn.json docs/reviews/notes/2026-07-10/sweet_corn.md
git commit -m "feat(sweet-corn): author core record (block planting, milk-stage ladder, su/se/sh2)"
```

---

### Task 4: Author the regional calendar (`regions` + `zones`)

**Files:**
- Modify: `scratch/sweet_corn.json` (add the `regions` + `zones` blocks)

**Interfaces:**
- Consumes: the `green-beans-bush` region skeleton (same warm-season direct-sow shape); `sweet_corn.md` regional sources.
- Produces: `scratch/sweet_corn.json` with all 10 regions populated + honest suitability.

- [ ] **Step 1: Copy the region skeleton** from `green-beans-bush` into `scratch/sweet_corn.json` (same 10 region keys + `resolved_by_zone` shape), then RE-TIME every calendar for corn's longer warm-season window from `sweet_corn.md` (corn needs more heat + a longer season than bush beans).

- [ ] **Step 2: Set suitability honestly (Option C).** In short-season cold regions (and the extreme-heat desert) where the frost-free window is marginal, keep the region PLANTABLE with an honest advisory in the calendar/region prose (per the dry-bean Option-C precedent — the annual region model cannot yet express a hard per-region `suitable:false`; A32 requires a non-empty calendar). Do NOT fabricate a `suitable:false`.

- [ ] **Step 3: Re-splice the scratch and run the calendar gates:**

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); \
sc=json.load(open('scratch/sweet_corn.json')); \
d['crops']=[sc if c['slug']=='sweet-corn' else c for c in d['crops']]; \
json.dump(d, open('scratch/canon_full.json','w'), ensure_ascii=False, separators=(',',':'))"
python3 tools/whole_crop_gate.py sweet-corn scratch/canon_full.json
python3 tools/calendar_coherence_gate.py scratch/canon_full.json || true
python3 tools/timing_spine_gate.py scratch/canon_full.json || true
```
Expected: `whole_crop_gate` on sweet-corn PASS (18/18); calendar_coherence 0 for sweet-corn; timing_spine 0 violations.

- [ ] **Step 4: Commit the regional draft.**

```bash
git add scratch/sweet_corn.json
git commit -m "feat(sweet-corn): author 10-region calendars (Option-C honest suitability)"
```

---

### Task 5: Adversarial gate proof (RED) — prove the suite protects sweet-corn

**Files:**
- Create: `docs/reviews/notes/2026-07-10/sweet_corn_red_proof.md` (the proof log)

**Interfaces:**
- Consumes: `scratch/canon_full.json` (the clean GREEN baseline from Task 4).
- Produces: a proof note recording each injected defect → the gate that caught it (exit 1).

- [ ] **Step 1: Confirm the clean draft PASSES (the GREEN baseline).**

```bash
python3 tools/whole_crop_gate.py sweet-corn scratch/canon_full.json; echo "exit=$?"
```
Expected: PASS, `exit=0`.

- [ ] **Step 2: Inject each defect into a COPY of the scratch and confirm the gate FAILS (exit 1).** For each defect, mutate `scratch/canon_full.json` → `scratch/canon_red.json`, run the gate, confirm exit 1, record which check fired in the proof note. Defects (each a separate run):
  1. `planting_layout` → `"blocks"` (bad enum) → A44 fires.
  2. Delete `pollination_block_min_rows` while `planting_layout=="block"` → A44 fires.
  3. Set `pollination_block_min_rows` on a fabricated `planting_layout:"row"` → A44 fires.
  4. `pollination_block_min_rows` → `1` (below floor) → A44 fires.
  5. Reorder the ladder so `harvest.day_range_from_sow` < `kernel_fill` (non-monotonic) → A40 fires.
  6. Drop a register field (e.g. `heat_threshold_f`) → A39 fires.
  7. Set `days_to_maturity` → `[7, 9]` (absurd for corn) → numeric_sanity (A33) fires.
  8. Inject an em dash into a `*_beginner` string → the dash gate (§C) fires.

Command pattern (defect 1 shown; repeat with each mutation):
```bash
python3 -c "import json; d=json.load(open('scratch/canon_full.json')); \
sc=[c for c in d['crops'] if c['slug']=='sweet-corn'][0]; sc['planting_layout']='blocks'; \
json.dump(d, open('scratch/canon_red.json','w'), ensure_ascii=False, separators=(',',':'))"
python3 tools/whole_crop_gate.py sweet-corn scratch/canon_red.json; echo "exit=$?"
```
Expected each: a VIOLATION line + `exit=1`.

- [ ] **Step 3: Commit the proof.**

```bash
git add docs/reviews/notes/2026-07-10/sweet_corn_red_proof.md
git commit -m "test(sweet-corn): adversarial RED gate proof (8 defect classes bounce)"
```

---

### Task 6: Splice into the canonical (SHA-guarded, COMPACT)

**Files:**
- Create: `tools/batches/sweet_corn_certify.json` (the SHA-guarded batch)
- Modify: `crops_data_final.json` (the ONLY task that touches the canonical)

**Interfaces:**
- Consumes: `scratch/sweet_corn.json` (the fully-authored object, INCLUDING `verification_status` set to certified — see Step 1); the current canonical SHA.
- Produces: the promoted canonical with sweet-corn certified; footprint = exactly sweet-corn changed.

- [ ] **Step 1: Set the certification block in the authored object.** In `scratch/sweet_corn.json`, set `verification_status` to `{"launch_ready_core": true, "launch_ready_seasoned": true, "status": "verified_gs_arc", "last_audited": "2026-07-10"}` (match the exact shape of a certified crop, e.g. `dry-bean`'s), and set `last_reviewed`/`last_reviewed_session` per convention.

- [ ] **Step 2: Build the batch.** Compute the live base SHA and write `tools/batches/sweet_corn_certify.json` as one `replace` op on the whole crop object (guarded by the exact current shell), plus any new `source_catalog` `add` ops from Task 1 Step 3:

```bash
BASE=$(shasum -a 256 crops_data_final.json | awk '{print $1}')
python3 -c "
import json
base=open('BASE_SHA').read().strip() if False else '$BASE'
shell=json.load(open('scratch/sweet_corn_shell.json'))   # exact current object (Task 3 Step 1)
authored=json.load(open('scratch/sweet_corn.json'))
batch={'base_sha': base, 'patches': [
  {'op':'replace','json_path':\"crops[?(@.slug=='sweet-corn')]\",'from':shell,'value':authored},
]}
json.dump(batch, open('tools/batches/sweet_corn_certify.json','w'), ensure_ascii=False)
print('base_sha', base)
"
```
(If Task 1 found new catalog sources, prepend their `add` ops to `patches`.)

- [ ] **Step 3: Apply to a scratch out + read the footprint report.**

```bash
python3 tools/apply_patch.py tools/batches/sweet_corn_certify.json --out crops_data_final.scratch.json
```
Expected: no SHA mismatch, no from-guard failure; footprint report = `crops: sweet-corn` (1 crop) and the sweet-corn top-level keys changed.

- [ ] **Step 4: Footprint audit — every OTHER crop byte-identical, count 125, COMPACT.**

```bash
python3 -c "
import json
a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json'))
ma={c['slug']:c for c in a['crops']}; mb={c['slug']:c for c in b['crops']}
assert len(mb)==125, len(mb)
changed=[s for s in ma if json.dumps(ma[s],sort_keys=True)!=json.dumps(mb.get(s),sort_keys=True)]
added=set(mb)-set(ma); removed=set(ma)-set(mb)
print('changed:',changed,'added:',added,'removed:',removed)
assert changed==['sweet-corn'] and not added and not removed, 'FOOTPRINT DIRTY'
raw=open('crops_data_final.scratch.json').read()
assert '\n' not in raw and ', ' not in raw and ': ' not in raw, 'NOT COMPACT'
print('FOOTPRINT CLEAN')
"
```
Expected: `changed: ['sweet-corn'] ... FOOTPRINT CLEAN`.

- [ ] **Step 5: Gate the scratch BEFORE promoting** (release_verify decides; operator promotes):

```bash
python3 tools/whole_crop_gate.py sweet-corn crops_data_final.scratch.json; echo "exit=$?"
python3 tools/gate_all.py crops_data_final.scratch.json; echo "exit=$?"
```
Expected: both `exit=0`; gate_all now reports 116 certified crop(s) all PASS.

- [ ] **Step 6: Promote scratch → canonical** (only after FOOTPRINT CLEAN + both gates green):

```bash
mv crops_data_final.scratch.json crops_data_final.json
```

- [ ] **Step 7: Commit the splice** (canonical + batch; do NOT push).

```bash
git add crops_data_final.json tools/batches/sweet_corn_certify.json
git commit -m "feat(sweet-corn): certify + splice (shell -> verified_gs_arc; count 125; block planting)"
```

---

### Task 7: Full release gate suite (GREEN)

**Files:** (no new files — verification run against the promoted canonical)

- [ ] **Step 1: `whole_crop_gate` on sweet-corn — the register test.**

Run: `python3 tools/whole_crop_gate.py sweet-corn`
Expected: `GATE: PASS`, 18/18, A44 `planting_layout violations: 0`, A39/A40 clean.

- [ ] **Step 2: Run the whole suite on every certified crop (the 18 anchors must stay intact).**

Run: `python3 tools/gate_all.py`
Expected: `ran whole_crop_gate on 116 certified crop(s)`, all PASS.

- [ ] **Step 3: `release_verify` + coherence + spine.**

```bash
python3 tools/release_verify.py
python3 tools/calendar_coherence_gate.py
python3 tools/timing_spine_gate.py --all-certified
```
Expected: release_verify clean (no NEW violations beyond documented pre-existing ones); calendar_coherence 0/125; timing_spine 0 violations.

- [ ] **Step 4: Source-truth sample + copy scan.** Pull 2-3 authored claims (block ≥4 rows, milk-stage cue, one variety DTM) back to their T1 sources in `sweet_corn.md`. Confirm 0 em dashes / `°F` only / "plant" lowercased in the new consumer copy:

```bash
python3 -c "import json; sc=[c for c in json.load(open('crops_data_final.json'))['crops'] if c['slug']=='sweet-corn'][0]; \
import re; s=json.dumps(sc,ensure_ascii=False); \
print('em-dash hits:', s.count(chr(8212))); print('degree-F ok:', 'degrees F' not in s and '°F' in s or '°F' not in s)"
```
Expected: `em-dash hits: 0`.

- [ ] **Step 5: No commit** (verification only; findings, if any, loop back to the relevant task).

---

### Task 8: State trio + summarize for Trevor

**Files:**
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`

- [ ] **Step 1: Update `CURRENT_STATE.md`.** Per memory `current-state-md-drift`, do NOT naively regen (no `---` separator; a regen corrupts it). Hand-insert a new most-recent entry at the top summarizing: sweet-corn certified (shell → `verified_gs_arc`, count 125 unchanged), the new A44 `planting_layout` gate (block planting, conditional, no-op off scope), the milk-stage ladder, su/se/sh2 varieties, Option-C regions, from→to SHAs, gate results. Mark the corn family follow-ons (field/pop/flint) + the planner arc as queued.

- [ ] **Step 2: Append `STATE_HISTORY.md`** (most-recent first) with the same summary + the from→to SHAs.

- [ ] **Step 3: Bump `LATEST.txt`** — new canonical SHA (`shasum -a 256 crops_data_final.json`) + `Date: 2026-07-10` + a `Session:` line describing the sweet-corn certification.

- [ ] **Step 4: Commit the state trio.**

```bash
git add CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "docs(state): certify sweet-corn (124->? -> new SHA; count 125; A44 planting_layout live)"
```

- [ ] **Step 5: Summarize for Trevor** — what changed (sweet-corn certified; A44 gate live; block-planting field shipped conditional; corn family + planner arc queued), the gate results, and that everything is committed UNPUSHED awaiting his push confirmation. Update memory: mark the corn arc anchor done + confirm `planner-data-model-arc` is the surfaced next step.

---

## Self-Review

**1. Spec coverage** (each spec section → task):
- §1 Goal (certify sweet-corn + planting_layout) → Tasks 2-7. ✓
- §2 Non-goals (no new archetype/gate; no dry corns; no planner; no roster-wide rollout) → honored: only A44 conditional gate added; dry corns/planner explicitly queued in Tasks 3/8. ✓
- §3 Crop model (archetype label, calendar_basis unchanged, regions) → Task 3 Step 2, Task 4. ✓
- §4 planting_layout field + gate → Task 2 (gate, TDD, wire A44) + Task 3 Step 3 (populate). ✓
- §5 Harvest model / growth_stages (milk-stage ladder, tasseling/silking distinct, succession, su/se/sh2, DTM) → Task 3 Steps 5-8. ✓
- §6 Region suitability (Option C) → Task 4 Step 2. ✓
- §7 Register stack → Task 3 Step 4. ✓
- §8 Corn-family table → out of scope (queued); noted Task 8 Step 1. ✓
- §9 Cert & gate strategy (TDD, release verify, SHA splice, state trio) → Tasks 5, 6, 7, 8. ✓
- §10 Verification → Task 7 Step 4. ✓
- §11 Success criteria → covered across Tasks 6-8. ✓
- §12 Open items (tomato re-baseline, DTM band, flowering-id check, planner defer) → Global Constraints (re-baseline) + Task 1 (DTM) + Task 3 Step 8 (A43 shape) + Task 8 (planner). ✓ **Flowering-id check:** the plan uses `tasseling`/`silking`/`kernel_fill` and anchors on `harvest`; Task 4 Step 3 runs `timing_spine_gate`, which would fail if any gate required a literal `flowering` id — so the check is executed, not assumed.

**2. Placeholder scan:** No "TBD/TODO/handle appropriately." Data values (DTM, day-ranges, prose) are sourced in Task 1 and referenced by pinned name — a genuine data dependency, not a placeholder (dry-bean plan precedent). Gate/tool code is complete and literal.

**3. Type consistency:** `check_crop(crop) -> list[str]` used identically in the gate, its test, and the A44 wiring (`_layout_violations`). Enum `{block,row,hill,grid,single}` and `pollination_block_min_rows` (int ≥2) are consistent across the gate, test, spec, and Task 3 population. Batch op shape (`replace` + `from`-guard + jsonpath `crops[?(@.slug=='sweet-corn')]`) matches the apply_patch interface and the onion-fix batch precedent.

**One open dependency (flagged, not a gap):** exact figures (DTM by sugar type, stage day-ranges, climate thresholds, region timings, variety set) are gathered at execution time in Task 1 from T1 sources — the plan pins WHERE each comes from and WHICH gate validates its shape, matching the dry-bean playbook.
