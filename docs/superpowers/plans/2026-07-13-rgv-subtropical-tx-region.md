# RGV / Subtropical-TX Region Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author and certify a real Rio Grande Valley / subtropical-South-Texas region (`rgv`) across all 108 certified region-carrying crops, retiring the se_gulf z10 interim so McAllen/Brownsville ZIPs get honest frost-free calendars.

**Architecture:** RGV reuses the existing Hawaii/FL-z11 frost-free cell shape (no new gate, no new `calendar_basis`, no deriver change). All 108 `rgv` cells are authored OFF-canonical into per-class staging files, gated per-crop against a scratch canonical (scratch tools with `rgv` patched into `EXPECTED_SPANS`), then promoted in ONE atomic SHA-guarded batch that also adds `rgv` to `EXPECTED_SPANS` + `region_chill_delivered.rgv`. `gate_all` is green before (no `rgv` anywhere) and after (`rgv` everywhere), never mid-flip.

**Tech Stack:** Python 3 (stdlib only); the repo's existing gate suite (`tools/whole_crop_gate.py`, `tools/gate_all.py`, `tools/coverage_floor_gate.py`, `tools/zone_span_gate.py`, `tools/annual_calendar.py`, `tools/chill_gate.py`), `tools/apply_patch.py` (SHA-guarded from-guarded splices), WebSearch/WebFetch for T1 sourcing.

**Spec:** `docs/superpowers/specs/2026-07-13-rgv-subtropical-tx-region-design.md`

## Global Constraints

Copied verbatim from the spec + CLAUDE.md; every task's requirements implicitly include these.

- **Canonical JSON is COMPACT:** `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` until the atomic promote (Task 8).** All authoring happens in staging files under `tools/staging/`.
- **TDD: RED before GREEN.** Any new check is adversarially proven on a scratch copy before it is trusted.
- **T1-or-it-doesn't-ship.** Every authored window/verdict cites a Tier-1 source (university `.edu` extension or government agency). `tamu_agrilife` is already catalogued; new T1 sources may be catalogued as needed (the rule is about tier, not the existing list). No fabricated precision — a thin-source crop gets a conservative cell, flagged, never invented.
- **No em dashes in consumer copy** (`region_notes_*`, `suitability_note_*`, `chill_basis_*`): use commas/colons/semicolons/periods. `--` is fine in docs/commits/code. American English. Temps render as `°F`. "plant" lowercase except at sentence start or "Plant Pro".
- **Zone span `rgv = ["9","10"]`** (locked 2026-07-13 from `zip-zones.json`: 785xx = 56 z10 + 12 z9). Every `rgv` cell's `resolved_by_zone` keys are EXACTLY `"9"` and `"10"` (A45 parity).
- **State trio at content release** (Task 10): CURRENT_STATE.md surgical (drift memory: no `---` separator, hand-maintain), STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session.
- **No plant-astro submodule bump from this session** (owned by the astro session). **Trevor confirms every push.** Don't commit the canonical change until Trevor approves.
- **Two-session collision rule:** do not run concurrently with a session that holds the canonical open (leek pilot). Confirmed clear at kickoff.

## Crop roster (the 108, by class)

Locked from canonical `7e29f4f4` (`verification_status.status == "verified_gs_arc"` AND non-empty `regions`):

- **frost_anchored (79):** the annual vegetable + herb roster (broccoli, lettuce-leaf, tomato family, cucurbits, roots, peas, beans, corn, etc.). Enumerate at build via the roster query below.
- **perennial_evergreen (5):** grapefruit, lemon, lime, mandarin-clementine, orange-navel.
- **perennial_chill_gated (14):** apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate.
- **perennial_woody_ornamental (5):** lavender, oregano, rosemary, sage, thyme.
- **berries_woody (4):** blackberry, blueberry, elderberry, raspberry.
- **perennial_herbaceous (1):** strawberry.

Roster query (run to get the authoritative per-class lists):
```bash
python3 -c "
import json,collections
d=json.load(open('crops_data_final.json'))
g=collections.defaultdict(list)
for c in d['crops']:
    if c.get('verification_status',{}).get('status')=='verified_gs_arc' and c.get('regions'):
        g[c.get('calendar_basis')].append(c['slug'])
for k in sorted(g): print(k,len(g[k]),sorted(g[k]))
"
```

## File Structure

- `tools/staging/rgv_annuals.json` — staged `rgv` cells for the 79 frost_anchored crops (`{slug: cell}`).
- `tools/staging/rgv_citrus.json` — staged cells for the 5 evergreen citrus.
- `tools/staging/rgv_trees.json` — staged cells for the 14 chill_gated trees (A3 verdicts + low-chill fruit calendars).
- `tools/staging/rgv_perennials.json` — staged cells for 5 woody herbs + 4 berries + 1 strawberry.
- `tools/staging/rgv_chill_band.json` — the `region_chill_delivered.rgv` band + provenance (top-level).
- `tools/rgv_harness.py` — the off-canonical per-crop gate harness (scratch tools + scratch canonical).
- `tools/build_rgv_promote.py` — deterministic emitter: staging files -> one SHA-guarded `apply_patch` batch.
- `tools/batches/rgv_region_promote.json` — the atomic promote batch (generated).
- `docs/rgv_cell_contract.md` — the per-archetype cell template (the column contract).
- `docs/reviews/notes/2026-07-13/rgv_sources.md` — the T1 sourcing table (crop -> source -> windows).
- `docs/kickoffs/26-rgv-plant-app-zip3-fence.md` — the paired plant-app handoff.

---

## Task 1: Lock the cell contract + roster

**Files:**
- Create: `docs/rgv_cell_contract.md`
- Read: `crops_data_final.json` (broccoli se_gulf + hawaii_tropical cells, apple low_desert_az cell)

**Interfaces:**
- Produces: `docs/rgv_cell_contract.md` — the authoritative per-archetype `rgv` cell template that Tasks 4-7 author against.

- [ ] **Step 1: Extract the three archetype templates from canonical**

Run:
```bash
python3 -c "
import json
d=json.load(open('crops_data_final.json'))
by={c['slug']:c for c in d['crops']}
for slug,reg in [('broccoli','hawaii_tropical'),('broccoli','se_gulf'),('apple','low_desert_az')]:
    cell=by[slug]['regions'][reg]
    print('=====',slug,reg,'=====')
    print('cell keys:',list(cell.keys()))
    z=sorted(cell['resolved_by_zone'])[0]
    print('zone',z,'keys:',list(cell['resolved_by_zone'][z].keys()))
"
```
Expected: confirms the frost-free annual cell (broccoli/hawaii_tropical: `month_resolved_frost_free`, `resolved_from` nulls, `transplant_window` plantings) and the tree cell (apple: adds `suitability`, `suitability_note_*`, `chill_basis_*`, `bloom`).

- [ ] **Step 2: Write `docs/rgv_cell_contract.md`**

Document, with a full worked JSON example per archetype:

1. **Frost-free annual cell** (frost_anchored, 79 crops + the non-tree perennials that carry calendars). Keys: `region_id="rgv"`, `region_label`, `zone_span=["9","10"]`, `sources`, `plantings[]` (anchored to `transplant_window`/`plant_out` offsets, NOT frost anchors), `resolved_by_zone` (keys `"9"`,`"10"`), `region_notes_beginner`, `region_notes_seasoned`. Each `resolved_by_zone[z]` carries: authored month windows (`plant_out`, `start_indoors` if tray-started, `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`), `calendar[]` (12 tokens, DERIVED via `tools/annual_calendar.py`), `resolution_method="month_resolved_frost_free"`, `resolved_from={"last_frost":null,"first_frost":null}`, optional `second_planting`, optional `heat_pause` (only if a backed summer heat pause is authored; else the summer gap renders `season_over`), `sources`, `anchoring_urls`, `notes`/`zone_notes`/`planting_note` (null unless authored).
2. **Tree cell (fruiting)** — citrus + low-chill fruit that DO fruit. Adds `suitability="fruits_reliably"` (or `"marginal"`), `suitability_note_{seasoned,beginner}`, `bloom`, `chill_basis_{seasoned,beginner}`; `calendar[]` uses the perennial vocabulary (`prune`/`bloom`/`growing`/`harvest`/`care`/`dormant`).
3. **Tree cell (no-fruit)** — high-chill fruit. `suitability="survives_no_fruit"` or `"unsuitable"`, `suitability_note_*` explaining near-zero chill vs the requirement, minimal/empty `calendar` (A32-exempt for trees; A3 governs).

State the summer-gap rule: prefer `season_over` for the cool-crop summer gap unless a T1-backed `heat_pause` (with `months`/`classification`/`basis_seasoned`/`sources`) is authored (heat_pause-at-variety-pass discipline).

- [ ] **Step 3: Commit**

```bash
git add docs/rgv_cell_contract.md
git commit -m "docs(rgv): per-archetype cell contract for the RGV region column"
```

---

## Task 2: Build the off-canonical per-crop gate harness

**Files:**
- Create: `tools/rgv_harness.py`
- Create: `tools/test_rgv_harness.py`

**Interfaces:**
- Produces: `rgv_harness.gate_crop(slug, staged_cells: dict) -> (bool, str)` — merges `staged_cells` (`{slug: rgv_cell}`) onto a scratch canonical, runs the REAL `whole_crop_gate.py` on `slug` via a scratch tools copy that has `rgv` in `EXPECTED_SPANS`, returns `(passed, output)`. Used by Tasks 4-7.
- Produces: `rgv_harness.build_scratch_tools()`, `rgv_harness.scratch_canonical(staged_cells)`.

- [ ] **Step 1: Write the failing test**

```python
# tools/test_rgv_harness.py
import json, os, rgv_harness

BASE = json.load(open("crops_data_final.json"))
BROC = next(c for c in BASE["crops"] if c["slug"] == "broccoli")

def _valid_rgv_cell():
    # a minimal-but-gate-valid frost-free annual cell cloned from broccoli's hawaii cell,
    # re-keyed to rgv span ["9","10"]
    haw = BROC["regions"]["hawaii_tropical"]
    cell = json.loads(json.dumps(haw))
    cell["region_id"] = "rgv"
    cell["region_label"] = "Rio Grande Valley: Subtropical South Texas"
    cell["zone_span"] = ["9", "10"]
    src = json.loads(json.dumps(cell["resolved_by_zone"][sorted(cell["resolved_by_zone"])[0]]))
    cell["resolved_by_zone"] = {"9": json.loads(json.dumps(src)), "10": json.loads(json.dumps(src))}
    return cell

def test_valid_cell_passes():
    ok, out = rgv_harness.gate_crop("broccoli", {"broccoli": _valid_rgv_cell()})
    assert ok, out

def test_span_key_mismatch_fails():
    cell = _valid_rgv_cell()
    del cell["resolved_by_zone"]["9"]          # span says ["9","10"], keys now only ["10"]
    ok, out = rgv_harness.gate_crop("broccoli", {"broccoli": cell})
    assert not ok and ("A45" in out or "zone_span" in out or "resolved_by_zone" in out), out

def test_missing_rgv_fails_a31():
    ok, out = rgv_harness.gate_crop("broccoli", {})   # no rgv cell added
    assert not ok and "rgv" in out, out
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_rgv_harness.py -v` (or `python3 test_rgv_harness.py` if the repo uses standalone asserts — match the repo convention).
Expected: FAIL with `ModuleNotFoundError: rgv_harness`.

- [ ] **Step 3: Implement `tools/rgv_harness.py`**

```python
#!/usr/bin/env python3
"""Off-canonical per-crop gate harness for the RGV region column.

Runs the REAL whole_crop_gate.py on a single crop whose rgv cell is staged, against a
SCRATCH canonical + a SCRATCH copy of tools/ that has rgv in zone_span_gate.EXPECTED_SPANS.
The real canonical + real tools stay untouched until the atomic promote (Task 8)."""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
RGV_SPAN = ["9", "10"]

def build_scratch_tools(dest):
    """Copy tools/*.py to dest, patching zone_span_gate.EXPECTED_SPANS to include rgv."""
    os.makedirs(dest, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith(".py"):
            shutil.copy(os.path.join(HERE, fn), os.path.join(dest, fn))
    zsg = os.path.join(dest, "zone_span_gate.py")
    src = open(zsg, encoding="utf-8").read()
    # insert rgv into the EXPECTED_SPANS dict literal (first line after the opening brace)
    patched, n = re.subn(r"(EXPECTED_SPANS = \{\n)",
                         r'\1    "rgv":            ["9", "10"],\n', src, count=1)
    assert n == 1, "could not patch EXPECTED_SPANS"
    open(zsg, "w", encoding="utf-8").write(patched)
    return dest

def scratch_canonical(staged_cells, path):
    """Write CANON with each staged rgv cell merged into its crop's regions."""
    data = json.load(open(CANON, encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    for slug, cell in staged_cells.items():
        by[slug].setdefault("regions", {})["rgv"] = cell
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    return path

def gate_crop(slug, staged_cells):
    """Return (passed, output) from running whole_crop_gate on slug in a scratch env."""
    with tempfile.TemporaryDirectory() as tmp:
        tools = build_scratch_tools(os.path.join(tmp, "tools"))
        canon = scratch_canonical(staged_cells, os.path.join(tmp, "canon.json"))
        r = subprocess.run([sys.executable, os.path.join(tools, "whole_crop_gate.py"), slug, canon],
                           capture_output=True, text=True)
        out = r.stdout + r.stderr
        return (r.returncode == 0 and "PASS" in out.upper()
                and "FAIL" not in out.upper().split("PASS")[0], out)

if __name__ == "__main__":
    # smoke: gate one crop from a staging file: rgv_harness.py <staging.json> <slug>
    staged = json.load(open(sys.argv[1], encoding="utf-8"))
    ok, out = gate_crop(sys.argv[2], {sys.argv[2]: staged[sys.argv[2]]})
    print(out)
    sys.exit(0 if ok else 1)
```

Note: adjust the final `(passed, ...)` predicate to match `whole_crop_gate.py`'s actual success signal — confirm in Step 4 by inspecting real output (it prints per-gate counts + a final verdict). If the script exits non-zero on any violation, `r.returncode == 0` alone is the signal; simplify accordingly.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools && python3 -m pytest test_rgv_harness.py -v`
Expected: 3 passed. If `test_valid_cell_passes` fails on a gate unrelated to rgv (e.g. a hawaii-cloned window tripping a coherence gate), fix the `_valid_rgv_cell` fixture to be genuinely valid — the harness is correct; the fixture must be a clean cell.

- [ ] **Step 5: Commit**

```bash
git add tools/rgv_harness.py tools/test_rgv_harness.py
git commit -m "test(rgv): off-canonical per-crop gate harness (scratch tools + scratch canonical)"
```

---

## Task 3: T1 sourcing pass (TAMU AgriLife) + the chill band

**Files:**
- Create: `docs/reviews/notes/2026-07-13/rgv_sources.md`
- Create: `tools/staging/rgv_chill_band.json`

**Interfaces:**
- Produces: the sourcing table (crop/class -> T1 source id + url + month windows) that Tasks 4-7 author from.
- Produces: `region_chill_delivered.rgv` band + provenance (drives A3 in Task 6).

- [ ] **Step 1: Web-research the T1 sources, by class**

Use WebSearch/WebFetch. Target Texas A&M AgriLife Extension (Aggie Horticulture) LRGV / South-Texas material:
- Annuals: the South-Texas / Lower-Rio-Grande-Valley vegetable planting-date guide (month-by-month sow/transplant/harvest).
- Citrus: TAMU AgriLife South-Texas citrus (bloom + harvest calendar; grapefruit/orange/lemon/lime/mandarin).
- Fruit/chill: TAMU low-chill-fruit-for-South-Texas guidance (fig, mulberry, persimmon, pomegranate; the near-zero-chill exclusion of apple/peach/cherry/etc.) + the RGV chill-hour accumulation figure.
- Berries + strawberry: TAMU small-fruit / strawberry-for-South-Texas guidance.

Record each as: source id (reuse `tamu_agrilife` or catalog a new T1 id), url, verified date, and the crop windows it supports. Confirm each is T1 (`.edu`/`.gov`). Flag any class where T1 windows are thin (that crop gets a conservative cell in its authoring task).

- [ ] **Step 2: Write the sourcing table**

Write `docs/reviews/notes/2026-07-13/rgv_sources.md` — a table `crop_or_class | source_id | url | windows | tier | notes`. This is the single source of truth Tasks 4-7 cite.

- [ ] **Step 3: Author the chill band**

From the TAMU RGV chill-hour figure, write `tools/staging/rgv_chill_band.json`:
```json
{
  "region_chill_delivered.rgv": {"9": [<lo>, <hi>], "10": [<lo>, <hi>]},
  "region_chill_delivered_provenance.rgv": "<sourced note: RGV banks ~X chill hours; TAMU AgriLife; url; verified 2026-07-13>"
}
```
Order-of-magnitude `[0, 300]` (fl_peninsula z11 = `[0,150]`); use the sourced figure. Verify against `chill_gate.py`'s shape (region -> {zone -> [lo,hi]}, numeric, lo<=hi).

- [ ] **Step 4: Commit**

```bash
git add docs/reviews/notes/2026-07-13/rgv_sources.md tools/staging/rgv_chill_band.json
git commit -m "docs(rgv): T1 sourcing table + region_chill_delivered.rgv band (TAMU AgriLife)"
```

---

## Task 4: Author the 79 frost_anchored annual cells

**Files:**
- Create: `tools/staging/rgv_annuals.json` (`{slug: rgv_cell}` for the 79 annuals)

**Interfaces:**
- Consumes: `docs/rgv_cell_contract.md` (annual template), `docs/reviews/notes/2026-07-13/rgv_sources.md`, `rgv_harness.gate_crop`.
- Produces: `tools/staging/rgv_annuals.json`.

This task is subagent-parallelizable: one worker per crop (or per family), each returning its crop's `rgv` cell as JSON. Author against the annual template. **Per-crop procedure (repeat for all 79):**

- [ ] **Step 1: Author the cell for crop `<slug>`**

Read the crop's existing `se_gulf` cell for its `plantings[]` track structure (spring/fall/succession) and its DTM. Author the `rgv` cell:
- `region_id="rgv"`, `region_label="Rio Grande Valley: Subtropical South Texas"`, `zone_span=["9","10"]`.
- Season inversion from the TAMU LRGV windows: cool-season crop -> Oct-Mar winter windows, summer gap (`season_over` unless a backed `heat_pause`); warm-season crop -> spring + fall windows around a mid-summer pause.
- `resolved_by_zone` keys `"9"` and `"10"` (z9 = inland Valley, slightly cooler; z10 = core Valley). If the TAMU source does not distinguish, author z9 == z10 windows (honest: the Valley is one calendar) and note it.
- `resolution_method="month_resolved_frost_free"`, `resolved_from={"last_frost":null,"first_frost":null}`.
- Dual-register `region_notes_{beginner,seasoned}` in the beefsteak-tomato voice (no em dashes).
- Cite the TAMU source id in `sources` + `anchoring_urls` (verified 2026-07-13).

- [ ] **Step 2: Derive the `calendar[]`**

```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell=json.load(open('tools/staging/rgv_annuals.json'))['<slug>']['resolved_by_zone']['10']
print(derive_annual_calendar(cell))
"
```
Set each zone's `calendar[]` to the derived 12-token array. Expected: a valid token vocabulary, winter-active for cool crops.

- [ ] **Step 3: Gate the crop in isolation**

Run: `python3 tools/rgv_harness.py tools/staging/rgv_annuals.json <slug>`
Expected: PASS (A45 parity on `["9","10"]`, A31/A32 satisfied, calendar coherence clean, 0 em dashes, sources T1).

- [ ] **Step 4: Fix + re-gate until PASS.** Common failures: A24/A25 calendar token placement (a pause on an active window), A32 empty calendar, em dash in notes, span/key mismatch.

- [ ] **Step 5: Commit the batch** (after all 79 pass)

```bash
git add tools/staging/rgv_annuals.json
git commit -m "feat(rgv): author 79 frost_anchored annual RGV cells (winter-garden inversion, TAMU)"
```

---

## Task 5: Author the 5 flagship citrus cells

**Files:**
- Create: `tools/staging/rgv_citrus.json`

**Interfaces:**
- Consumes: the tree-fruiting template, the citrus sourcing rows, `rgv_harness.gate_crop`.
- Produces: `tools/staging/rgv_citrus.json` (grapefruit, lemon, lime, mandarin-clementine, orange-navel).

- [ ] **Step 1: Author each citrus cell** with `suitability="fruits_reliably"`, authored `bloom` (spring) + `harvest` windows per the TAMU South-Texas citrus calendar (grapefruit/orange: late fall-winter harvest; lemon/lime: multiple flushes), `min_winter_temp_f` (`[lo,hi]`) + `cold_basis_{seasoned,beginner}` -- citrus is `perennial_evergreen` (cold-gated, not chill-gated) and does **not** carry `chill_basis_*`; for the heat-gated three (grapefruit, orange-navel, mandarin-clementine -- NOT lemon/lime) also add `heat_summer_basis` + `heat_basis_{seasoned,beginner}` -- plus dual-register notes. Keys `"9"`,`"10"`; `resolution_method` frost-free variant. `docs/rgv_cell_contract.md` §3 is the authoritative citrus template (§3.1 sub-shape table, §3.3 heat-gated worked example, §3.4 lemon/lime delta).

- [ ] **Step 2: Gate each in isolation**

Run: `python3 tools/rgv_harness.py tools/staging/rgv_citrus.json <slug>` for each of the 5.
Expected: PASS (A3 consistent: fruits_reliably with the rgv chill band; A31 satisfied; A32-exempt but a real calendar present).

- [ ] **Step 3: Fix + re-gate until all 5 PASS.**

- [ ] **Step 4: Commit**

```bash
git add tools/staging/rgv_citrus.json
git commit -m "feat(rgv): 5 flagship citrus RGV fruiting calendars (TAMU South-Texas citrus)"
```

---

## Task 6: Author the 14 chill_gated tree cells (A3 no-fruit split)

**Files:**
- Create: `tools/staging/rgv_trees.json`

**Interfaces:**
- Consumes: the two tree templates (fruiting + no-fruit), the fruit/chill sourcing rows, `region_chill_delivered.rgv` (Task 3), `rgv_harness.gate_crop`.
- Produces: `tools/staging/rgv_trees.json` (14 crops).

- [ ] **Step 1: Split the 14 by the sourced RGV chill call**
  - **No-fruit** (high chill vs near-zero delivered): apple, apricot, cherry-sour, cherry-sweet, nectarine, peach, pear-asian, pear-european, plum, pawpaw. Author `suitability` in `{survives_no_fruit, unsuitable}` per the source (pawpaw also fails on humidity/chill -> `unsuitable`), with `suitability_note_{seasoned,beginner}` explaining the near-zero-chill exclusion, `chill_basis_*`, minimal `calendar` (A32-exempt).
  - **Low-chill fruit** (fruit in RGV per TAMU): fig, mulberry, persimmon, pomegranate. Author `suitability="fruits_reliably"` (or `"marginal"` if the source hedges) with real `bloom`/`harvest` calendars. The exact call per crop comes from the Task 3 source, not this plan.

- [ ] **Step 2: Gate each in isolation**

Run: `python3 tools/rgv_harness.py tools/staging/rgv_trees.json <slug>` for each of the 14.
Expected: PASS. Critical check: A3 (perennial no-fruit split) agrees with `region_chill_delivered.rgv` — a `survives_no_fruit`/`unsuitable` verdict where the crop's chill requirement exceeds the band; a fruiting verdict only where the low-chill evidence supports it.

- [ ] **Step 3: Fix + re-gate until all 14 PASS.**

- [ ] **Step 4: Commit**

```bash
git add tools/staging/rgv_trees.json
git commit -m "feat(rgv): 14 chill-gated tree RGV cells (A3 no-fruit split; low-chill fig/mulberry/persimmon/pomegranate fruit)"
```

---

## Task 7: Author the 10 remaining perennials (woody herbs + berries + strawberry)

**Files:**
- Create: `tools/staging/rgv_perennials.json`

**Interfaces:**
- Consumes: the annual/fruiting templates (these carry real calendars; A32 applies), sourcing rows, `rgv_harness.gate_crop`.
- Produces: `tools/staging/rgv_perennials.json` (lavender, oregano, rosemary, sage, thyme, blackberry, blueberry, elderberry, raspberry, strawberry).

- [ ] **Step 1: Author each cell** with a real `calendar[]` (A32 requires it for these bases):
  - Woody herbs: year-round growth; lavender carries an honest humidity-struggle `region_notes`/suitability note.
  - Berries: blackberry `fruits_reliably` (Texas cultivars, spring harvest); blueberry/raspberry `marginal` (chill/heat honesty note); elderberry per source.
  - Strawberry: winter-annual calendar (Oct plant -> spring harvest, per TAMU South-Texas strawberry).

- [ ] **Step 2: Gate each in isolation**

Run: `python3 tools/rgv_harness.py tools/staging/rgv_perennials.json <slug>` for each of the 10.
Expected: PASS (A31 + A32 satisfied — non-empty calendars; suitability notes coherent).

- [ ] **Step 3: Fix + re-gate until all 10 PASS.**

- [ ] **Step 4: Commit**

```bash
git add tools/staging/rgv_perennials.json
git commit -m "feat(rgv): 10 perennial RGV cells (woody herbs + berries + winter-annual strawberry)"
```

---

## Task 8: Build the atomic promote batch

**Files:**
- Create: `tools/build_rgv_promote.py`
- Create: `tools/batches/rgv_region_promote.json` (generated)
- Create: `tools/test_build_rgv_promote.py`

**Interfaces:**
- Consumes: the four `tools/staging/rgv_*.json` cell files + `tools/staging/rgv_chill_band.json`.
- Produces: `tools/batches/rgv_region_promote.json` — an `apply_patch` batch adding, per crop, `$.crops[slug].regions.rgv` (op `add`), plus the top-level `region_chill_delivered.rgv` + provenance. **Note:** `EXPECTED_SPANS.rgv` is a CODE edit to `tools/zone_span_gate.py` (Step 4), applied in the same commit as the batch, NOT part of the JSON batch.

- [ ] **Step 1: Write the failing test**

```python
# tools/test_build_rgv_promote.py
import json, subprocess, sys, os
def test_batch_covers_108_plus_topcell():
    subprocess.run([sys.executable, "tools/build_rgv_promote.py"], check=True)
    batch = json.load(open("tools/batches/rgv_region_promote.json"))
    ops = batch["ops"] if isinstance(batch, dict) else batch
    rgv_cells = [o for o in ops if o["json_path"].endswith(".regions.rgv")]
    assert len(rgv_cells) == 108, len(rgv_cells)
    assert any("region_chill_delivered" in o["json_path"] and o["json_path"].endswith(".rgv") for o in ops)
    assert all(o["op"] == "add" for o in ops)   # rgv is net-new everywhere
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_build_rgv_promote.py -v`
Expected: FAIL (`build_rgv_promote.py` missing).

- [ ] **Step 3: Implement `tools/build_rgv_promote.py`**

```python
#!/usr/bin/env python3
"""Emit the atomic RGV promote batch from the staging files. Deterministic; no canonical write."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STAGING = ["rgv_annuals.json", "rgv_citrus.json", "rgv_trees.json", "rgv_perennials.json"]

def main():
    canon = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
    ops, seen = [], set()
    for fn in STAGING:
        for slug, cell in json.load(open(os.path.join(HERE, "staging", fn), encoding="utf-8")).items():
            assert slug not in seen, f"duplicate {slug}"
            seen.add(slug)
            ops.append({"op": "add", "json_path": f"$.crops[?slug={slug}].regions.rgv", "value": cell})
    band = json.load(open(os.path.join(HERE, "staging", "rgv_chill_band.json"), encoding="utf-8"))
    for path, value in band.items():
        ops.append({"op": "add", "json_path": "$." + path, "value": value})
    assert len(seen) == 108, f"expected 108 crops, got {len(seen)}"
    out = {"sha256_before": None, "ops": ops}   # fill sha256_before at apply time
    with open(os.path.join(HERE, "batches", "rgv_region_promote.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)   # the BATCH file may be pretty; canonical stays compact
    print(f"emitted {len(ops)} ops ({len(seen)} rgv cells + {len(band)} top-level)")

if __name__ == "__main__":
    main()
```
Confirm the `json_path` slug-selector syntax against `tools/apply_patch.py` (`normalize_path`/`tokenize`) and an existing batch (`tools/batches/zonespan_widen.json`) — match their exact path form.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools && python3 -m pytest test_build_rgv_promote.py -v`
Expected: PASS (108 rgv cells + the chill-band ops; all `add`).

- [ ] **Step 5: Commit** (batch generator + generated batch; canonical still untouched)

```bash
git add tools/build_rgv_promote.py tools/test_build_rgv_promote.py tools/batches/rgv_region_promote.json
git commit -m "feat(rgv): deterministic atomic-promote batch emitter (108 cells + chill band)"
```

---

## Task 9: Dry-run the promote on a scratch copy (full gate ceremony, RED-checked)

**Files:**
- Modify (scratch only): a copy of `crops_data_final.json` + `tools/zone_span_gate.py`
- Read: all gates

**Interfaces:**
- Consumes: `tools/batches/rgv_region_promote.json`, `rgv_harness.build_scratch_tools`.
- Produces: proof that the full suite is green post-promote before touching the real canonical.

- [ ] **Step 1: Apply the batch to a scratch canonical** (compute `sha256_before` from the real file, apply via `tools/apply_patch.py` to a copy, confirm COMPACT + count 125 + footprint = exactly 108 `regions.rgv` + 3 top-level additions via a byte-diff audit).

- [ ] **Step 2: Add `rgv` to a scratch `EXPECTED_SPANS`** (via `rgv_harness.build_scratch_tools`) and run the full suite against the scratch canonical + scratch tools:
  - `gate_all.py` -> 116/116.
  - `zone_span_gate.py` (A45) -> 0.
  - `coverage_floor_gate.py` (A31/A32) -> 0.
  - `chill_gate.py` -> 0.
  - `whole_crop_gate.py` on a per-class sample (broccoli, grapefruit, apple, peach, blackberry, strawberry) -> PASS.
  - `release_verify.py` -> clean modulo the documented roster-wide section-A collateral.

- [ ] **Step 3: RED-check the promote** — stage an intentionally-broken cell (drop the `"9"` key from one crop's rgv cell on the scratch copy) and confirm A45 bounces it; restore. This proves the ceremony actually catches the span-parity defect class at roster scale.

- [ ] **Step 4: Record the dry-run result** in `docs/reviews/notes/2026-07-13/rgv_promote_dryrun.md` (gate outputs + footprint audit). Commit.

```bash
git add docs/reviews/notes/2026-07-13/rgv_promote_dryrun.md
git commit -m "test(rgv): scratch-copy promote dry-run green + A45 RED-check"
```

---

## Task 10: Promote to canonical + release ceremony (THE one canonical write)

**Files:**
- Modify: `crops_data_final.json` (the atomic promote)
- Modify: `tools/zone_span_gate.py` (add `rgv` to `EXPECTED_SPANS`)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`
- Modify: `docs/region_coverage_roadmap.md`
- Modify: `docs/field_addition_register.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Add `rgv` to the REAL `tools/zone_span_gate.py` `EXPECTED_SPANS`** (`"rgv": ["9","10"]`). `coverage_floor_gate` auto-derives its rosters.

- [ ] **Step 2: Apply the batch to the REAL canonical** via `tools/apply_patch.py` with the real `sha256_before` (= `shasum -a 256 crops_data_final.json`). Confirm COMPACT, no trailing newline, count 125.

- [ ] **Step 3: Full release verification** (protocol #6):
  - `python3 tools/whole_crop_gate.py <slug>` on the 18 gold anchors -> 18/18 PASS.
  - `python3 tools/gate_all.py` -> 116/116.
  - `python3 tools/zone_span_gate.py` (A45), `coverage_floor_gate.py`, `chill_gate.py` -> 0.
  - `python3 tools/release_verify.py` -> clean (modulo documented collateral).
  - Independent footprint audit: exactly 108 `regions.rgv` + `region_chill_delivered.rgv` + provenance changed; all else byte-identical.
  - The **pre-commit backstop** runs on commit (checks ALL changed crops — watch the empty-shell class).
  - Per-batch source-truth sample: re-verify 3-4 authored windows against their cited TAMU URLs.

- [ ] **Step 4: State trio** — regenerate/surgically-update CURRENT_STATE.md (drift memory: hand-maintain, no `---`), append STATE_HISTORY.md (most-recent-first), bump LATEST.txt (new SHA + session line).

- [ ] **Step 5: Roadmap + register** — mark roadmap item 3 SHIPPED; retire the RGV-interim + TX-fencing lines; add a `field_addition_register.md` row for the RGV region column.

- [ ] **Step 6: Commit** (UNPUSHED — Trevor confirms push)

```bash
git add crops_data_final.json tools/zone_span_gate.py CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/region_coverage_roadmap.md docs/field_addition_register.md
git commit -m "feat(rgv): certify the Rio Grande Valley subtropical-TX region across 108 crops (retire se_gulf z10 interim)"
```

---

## Task 11: Write the paired plant-app kickoff

**Files:**
- Create: `docs/kickoffs/26-rgv-plant-app-zip3-fence.md`

**Interfaces:**
- Produces: the handoff so plant-app can route RGV ZIPs to `rgv`.

- [ ] **Step 1: Write the kickoff** covering:
  - `REGION_STATES`: map `rgv` -> TX.
  - `ZIP3_REGION_HINT`: fence **785xx** (McAllen/Edinburg/Mission/Pharr/Weslaco/Harlingen/Brownsville/San Benito) to `rgv`. **Do NOT fence all TX z10** — of ~96 TX z10 ZIPs, only 56 are 785xx (RGV); the rest are 784/783 (Corpus Christi/Coastal Bend) and 775 (Galveston barrier islands), which are frost-prone coast and should stay se_gulf.
  - `zone_span` confirm: RGV spans z9 + z10 (785xx = 12 z9 + 56 z10); the dataset carries both zone rows.
  - Verify the regions.json sync path picks up the new `rgv` region.
  - Note: dataset side is `<new canonical SHA>`; plant-astro consumes spans + citrus + chill band automatically.

- [ ] **Step 2: Commit**

```bash
git add docs/kickoffs/26-rgv-plant-app-zip3-fence.md
git commit -m "docs(kickoff): plant-app RGV ZIP3 fence + REGION_STATES handoff (#26)"
```

---

## Task 12: Update memory + close out

- [ ] **Step 1:** Write/update memory `rgv-subtropical-tx-region` (SHIPPED, canonical SHA, 108 cells, reusable lessons: frost-free reuse of the Hawaii shape, the A45/A31 pincer -> atomic promote, the 785xx-not-all-TX-z10 fence correction). Add the MEMORY.md pointer.
- [ ] **Step 2:** Confirm the leek pilot's base-SHA rebase note (its plan rebases onto the new RGV canonical).
- [ ] **Step 3:** Summarize to Trevor: what shipped, the unpushed commit, the plant-app kickoff owed, and that no plant-astro bump was done.

---

## Self-Review

**Spec coverage:**
- Product goal (retire interim) -> Tasks 4-10 + roadmap retire (Task 10.5). ✓
- Option A full roster-wide (108) -> Tasks 4-7 enumerate all 108. ✓
- Frost-free model reuse -> Task 1 contract + Task 4 cells. ✓
- zone_span ["9","10"] -> locked in Global Constraints (real zip-zones data). ✓
- region_chill_delivered.rgv + A3 -> Task 3 + Task 6. ✓
- Citrus flagship -> Task 5. ✓
- Sourcing T1 -> Task 3. ✓
- Atomic promote (A45/A31 pincer) -> Tasks 8-10. ✓
- Gate surface (A45/A31/A32/A3, gate_all, release_verify, pre-commit) -> Tasks 9-10. ✓
- App handoff (785xx fence, not all TX z10) -> Task 11. ✓
- State trio + roadmap + register + memory -> Tasks 10, 12. ✓
- Non-goals (no app edits, no astro bump, no new gate) -> honored (no task adds a gate; no app/astro write). ✓

**Placeholder scan:** the authored window VALUES are produced by Task 3 (sourcing) and consumed by Tasks 4-7 against the Task 1 template — this is the data-authoring analog of "implement per spec," not a placeholder; the STRUCTURE and gate loop are fully concrete. `<lo>/<hi>/<slug>` are per-item substitutions, not TODOs.

**Type consistency:** `gate_crop(slug, staged_cells) -> (bool, str)` used consistently in Tasks 2/4/5/6/7; staging files are `{slug: cell}` throughout; the promote emitter reads exactly those four files + the chill band. ✓

**Open confirm-items flagged, not hidden:** the `apply_patch` `json_path` selector syntax (Task 8 Step 3) and `whole_crop_gate` success predicate (Task 2 Step 3) are marked "confirm against the real tool" rather than assumed.
