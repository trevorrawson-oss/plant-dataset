# Mid-Atlantic Region Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author and certify a real Mid-Atlantic region (`mid_atlantic`, NC/VA/MD/DC/DE/NJ/PA, z7-8) across all 111 certified region-carrying crops, so the belt stops riding generic zone dates that omit a documented fall planting cycle for warm-season annuals.

**Architecture:** Mid-Atlantic is FROST-ANCHORED (same model as PNW, the inverse of RGV's frost-free Hawaii shape). Cells reuse each crop's existing frost-anchored region-cell shape (`resolution_method="frost_anchored_resolved"`, real `resolved_from` frost dates, `cold_pause` winters), so `calendar[]` is DERIVED by the standard `tools/annual_calendar.py` from authored windows -- no deriver change, no new field, no new gate. The single differentiator from PNW: warm-season annuals carry a T1-sourced `heat_pause` + `second_planting` fall cycle (the gap the ruling found), authored against existing machinery already live in 881 `heat_pause` / 272 `second_planting` cells and gated by A43. All 111 `mid_atlantic` cells are authored OFF-canonical into per-class staging files, gated per-crop against a scratch canonical (scratch tools with `mid_atlantic` patched into `EXPECTED_SPANS`), then promoted in ONE atomic SHA-guarded batch that also adds `mid_atlantic` to `EXPECTED_SPANS` + `region_chill_delivered.mid_atlantic`. `gate_all` is green before (no `mid_atlantic` anywhere) and after (`mid_atlantic` everywhere), never mid-flip.

**Tech Stack:** Python 3 standalone gate scripts (`whole_crop_gate.py`, `gate_all.py`, `zone_span_gate.py`, `coverage_floor_gate.py`, `chill_gate.py`, `second_planting_gate.py`, `annual_calendar.py`, `apply_patch.py`), the region-generic tooling (`region_harness.py`, `region_cell_audit.py`, `build_region_promote.py` -- already built for RGV/PNW, extended not rebuilt here), compact JSON canonical, git on `main`.

## Global Constraints

Copied verbatim from the spec (`docs/superpowers/specs/2026-07-20-mid-atlantic-region-design.md`) + CLAUDE.md; every task's requirements implicitly include these.

- **Canonical JSON is COMPACT:** `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` until the atomic promote (Task 10).** All authoring happens in staging files under `tools/staging/`.
- **TDD: RED before GREEN.** No new gate ships this arc, but every tool extension (Task 2) and the promote ceremony (Task 9) is adversarially proven on a scratch copy before it is trusted. Specifically: inject a fall-spanning `second_planting` envelope into a scratch cell and confirm A43 bounces it before trusting the warm-season batch (Task 4).
- **T1-or-it-doesn't-ship.** Every authored window/verdict cites a Tier-1 source. `ncsu_ext` (NC State Extension) and `vce_426_331` (Virginia Cooperative Extension Pub. 426-331) are the primary authorities and are **already catalogued in `source_catalog`** -- expect few or no new source entries. No fabricated precision: a thin-source crop gets a conservative cell, flagged, never invented.
- **No em dashes in consumer copy** (`region_notes_*`, `suitability_note_*`, `chill_basis_*`, `zone_notes`, `notes`): use commas/colons/semicolons/periods. `--` is fine in docs/commits/code. American English. Temps render as `°F`. "plant" lowercase except at sentence start or "Plant Pro".
- **Zone span `mid_atlantic = ["7","8"]`** (DECIDED, Trevor 2026-07-20; spec 4.2). z7 = 3,131 belt ZIPs (northern VA, central MD, most NJ/eastern PA, western NC Piedmont); z8 = 1,444 (NC Coastal Plain, DC, VA Tidewater, coastal MD). Every `mid_atlantic` cell's `resolved_by_zone` keys are EXACTLY `"7"` and `"8"` (A45 parity). The z7 half's in-app delivery depends on the plant-app resolution fix (kickoff #32), NOT on this dataset build.
- **Mid-Atlantic is FROST-ANCHORED:** `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost":<date>,"first_frost":<date>}` (real dates), `calendar[]` DERIVED by `tools/annual_calendar.py` (`calendar_basis="frost_anchored"`). `cold_pause` in winter is EXPECTED and correct.
- **The fall cycle is the point.** Warm-season annuals get a T1-sourced `heat_pause` (real midsummer set-failure period) + `second_planting` (the documented fall cycle). `heat_pause` is declaration-driven in the deriver (`annual_calendar.py` emits it only for months in a cell's `heat_pause.months`), so an unsourced pause silently reshapes the calendar -- SOURCE IT PER CROP. Cool-season annuals get long spring/fall shoulders and no `heat_pause`.
- **A43 governs `second_planting` shape:** a cell carrying `second_planting` must be single-span in `start_indoors`/`plant_out`/`harvest`, and its envelope (`harvest_end` inside the FIRST harvest span, `last_plant_date` inside the FIRST `plant_out` span) must sit INSIDE the primary windows. Read `tools/second_planting_gate.py`'s docstring before authoring.
- **State trio at content release** (Task 10): CURRENT_STATE.md surgical (drift memory `current-state-md-drift`: no `---` separator, hand-maintain), STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session.
- **No plant-astro submodule bump from this session** (memory `plant-astro-bump-owned-by-astro-session`). **Trevor confirms every push.** Don't commit the canonical change until Trevor approves.
- **CONCURRENT-CHECKOUT DISCIPLINE (active this repo).** Other sessions may share this checkout (memory `subagent-resumability-and-concurrent-git-safety`). Every commit: explicit-pathspec `git add` (never `git add -A`), `git status` before, `git show --stat` after. Tasks 1-9 are off-canonical (staging/scratch/tools) and collision-safe; only Task 10 writes the canonical, SHA-guarded. Consider an isolated worktree for the authoring run.

## Crop roster (the 111, by class)

Locked from canonical `e1e01c47` (`verification_status.status == "verified_gs_arc"` AND non-empty `regions`). Re-run the query against the LIVE canonical at build start in case a concurrent session certified a crop.

- **frost_anchored (82):** the annual vegetable + herb roster. Enumerate at build via the roster query below. **Split for authoring into cool-season and warm-season sub-batches (Task 4).**
- **perennial_chill_gated (14):** apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate. **(All fruit here -- NC chill >1,000 hr clears the whole canonical variety range.)**
- **perennial_evergreen (5):** grapefruit, lemon, lime, mandarin-clementine, orange-navel. **(Cold-limited.)**
- **perennial_woody_ornamental (5):** lavender, oregano, rosemary, sage, thyme.
- **berries_woody (4):** blackberry, blueberry, elderberry, raspberry. **(Blueberry: genuine NC native highbush + rabbiteye range.)**
- **perennial_herbaceous (1):** strawberry.

Roster query (run at build start against the LIVE canonical):
```bash
python3 -c "
import json,collections
d=json.load(open('crops_data_final.json'))
g=collections.defaultdict(list)
for c in d['crops']:
    if c.get('verification_status',{}).get('status')=='verified_gs_arc' and c.get('regions'):
        g[c.get('calendar_basis')].append(c['slug'])
for k in sorted(g): print(k,len(g[k]),sorted(g[k]))
print('TOTAL region-carrying certified:', sum(len(v) for v in g.values()))
"
```
Expected: 82 frost_anchored, 14 perennial_chill_gated, 5 perennial_evergreen, 5 perennial_woody_ornamental, 4 berries_woody, 1 perennial_herbaceous; TOTAL 111.

## File Structure

- `tools/staging/mid_atlantic_annuals_cool.json` -- staged cells for the cool-season frost_anchored crops (`{slug: cell}`).
- `tools/staging/mid_atlantic_annuals_warm.json` -- staged cells for the warm-season frost_anchored crops (the `heat_pause` + `second_planting` batch).
- `tools/staging/mid_atlantic_trees.json` -- staged cells for the 14 chill_gated trees (all `fruits_reliably`).
- `tools/staging/mid_atlantic_citrus.json` -- staged cells for the 5 evergreen citrus (cold-limited verdicts).
- `tools/staging/mid_atlantic_perennials.json` -- staged cells for 5 woody herbs + 4 berries + 1 strawberry.
- `tools/staging/mid_atlantic_chill_band.json` -- the `region_chill_delivered.mid_atlantic` band + provenance (top-level).
- `tools/region_cell_audit.py` -- MODIFY: add a `mid_atlantic` entry to `REGION_CONFIG`.
- `tools/build_region_promote.py` -- MODIFY: add `mid_atlantic` to `STAGING` + `EXPECTED_CELLS`.
- `tools/batches/mid_atlantic_region_promote.json` -- the atomic promote batch (generated).
- `docs/mid_atlantic_cell_contract.md` -- the per-archetype cell template (the column contract).
- `docs/reviews/notes/2026-07-20/mid_atlantic_sources.md` -- the T1 sourcing table (crop -> source -> windows, esp. the fall windows).
- `docs/reviews/notes/2026-07-20/mid_atlantic_promote_dryrun.md` -- the scratch dry-run record.
- `docs/kickoffs/33-mid-atlantic-plant-app.md` -- the paired plant-app handoff (REGION_STATES; no ZIP3 fence).

`region_harness.py` needs NO change (it takes region_id + span as params and patches `EXPECTED_SPANS` dynamically). The `region_cell_audit.py` and `build_region_promote.py` edits are additive dict entries, not rewrites.

---

## Task 1: Lock the cell contract + roster

**Files:**
- Create: `docs/mid_atlantic_cell_contract.md`
- Read: `crops_data_final.json` (broccoli `northern_tier` z7 + `se_gulf` z8 cells, cherry-tomato `se_gulf` z8 cell, apple `northern_tier` cell, orange-navel `se_gulf` cell)

**Interfaces:**
- Produces: `docs/mid_atlantic_cell_contract.md` -- the authoritative per-archetype `mid_atlantic` cell template that Tasks 4-7 author against.

- [ ] **Step 1: Extract the archetype templates from canonical**

Run:
```bash
python3 -c "
import json
d=json.load(open('crops_data_final.json'))
by={c['slug']:c for c in d['crops']}
for slug,reg,z in [('broccoli','northern_tier','7'),('cherry-tomato','se_gulf','8'),('apple','northern_tier','7'),('orange-navel','se_gulf','8'),('blueberry','northern_tier','7')]:
    r=by[slug]['regions'].get(reg)
    if not r: print('=====',slug,reg,'MISSING'); continue
    cell=r['resolved_by_zone'].get(z,{})
    print('=====',slug,reg,z,'=====')
    print('region keys:',list(r.keys()))
    print('cell keys:',list(cell.keys()))
    print('resolution_method:',cell.get('resolution_method'),'| resolved_from:',cell.get('resolved_from'))
    print('has second_planting?', 'second_planting' in cell, '| has heat_pause?', 'heat_pause' in cell)
"
```
Expected: confirms the **frost-anchored annual with fall cycle** shape (broccoli/cherry-tomato: `resolution_method="frost_anchored_resolved"`, real `resolved_from`, `second_planting` + `heat_pause` present), the chill-gated tree cell (apple: adds `suitability`, `suitability_note_*`, `chill_basis_*`, `bloom`), the citrus cell (orange-navel: adds `min_winter_temp_f`, `cold_basis_*`), and the berry cell (blueberry: adds `recommended_type` + `type_note_*` for the highbush/rabbiteye steer).

- [ ] **Step 2: Write `docs/mid_atlantic_cell_contract.md`**

Document, with a full worked JSON example per archetype (mirror `docs/pnw_cell_contract.md`):

1. **Frost-anchored annual cell** (82 crops). Keys: `region_id="mid_atlantic"`, `region_label` (final wording below), `zone_span=["7","8"]`, `sources`, `plantings[]`, `resolved_by_zone` (keys `"7"`,`"8"`), `region_notes_beginner`, `region_notes_seasoned`. Each `resolved_by_zone[z]` carries: authored month windows (`plant_out`, `start_indoors` if tray-started, `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`), `calendar[]` (12 tokens, DERIVED via `tools/annual_calendar.py`), **`resolution_method="frost_anchored_resolved"`**, **`resolved_from={"last_frost":<date>,"first_frost":<date>}`** (real dates), `sources`, `anchoring_urls`, `notes`/`zone_notes`/`planting_note` (null unless authored). **Two sub-shapes:**
   - **Cool-season** (brassica, green, root, pea, cool herb): long spring-through-fall run, real fall/overwintering windows where sourced; **NO `heat_pause`** (the deriver renders midseason as `growing`).
   - **Warm-season** (tomato, pepper, eggplant, squash, bean, cucumber, melon, corn, okra, sweet potato): spring cycle + a T1-sourced `heat_pause` (real midsummer set-failure months) + a `second_planting` fall cycle where VCE/NC State document one. The `cherry-tomato` `se_gulf` z8 cell is the worked template. **A43 envelope rule applies** (single-span primary windows; `second_planting` envelope inside them).
2. **Tree cell (fruiting)** -- all 14 chill_gated trees. `suitability="fruits_reliably"`, `suitability_note_{seasoned,beginner}` (note NC State's 750+-hour variety preference: the real risk is premature bloom in warm winter spells, NOT chill deficit), `bloom`, `chill_basis_{seasoned,beginner}` (delivered >1,000 hr vs requirement), region-level `plantings_provenance`; `calendar[]` uses the perennial vocabulary (`prune`/`bloom`/`growing`/`harvest`/`care`/`dormant`). Real bloom + harvest windows. Pawpaw is NATIVE here (a strength, not an edge case). Any genuinely heat/humidity-limited caveat (none expected in this belt) is sourced, not assumed.
3. **Citrus cell (cold-limited)** -- the 5 evergreen citrus. `suitability="survives"` (some container culture is real in z8 Tidewater; source it) or `"unsuitable"`, `min_winter_temp_f`, `cold_basis_{seasoned,beginner}`. A32-exempt; minimal calendar.
4. **Berry cell** -- blueberry especially: use `recommended_type` + `type_note_{seasoned,beginner}` for the NC-region highbush-vs-rabbiteye steer (the existing per-zone field; blueberry already carries it in `northern_tier`). Real calendars (A32 applies).

Set `region_label = "Mid-Atlantic: Piedmont and Coastal Plain"` (final wording; confirm no em dash, American English).

- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add docs/mid_atlantic_cell_contract.md
git status
git commit -m "docs(mid_atlantic): per-archetype cell contract for the Mid-Atlantic region column"
git show --stat HEAD
```

---

## Task 2: Extend the region-generic tooling for `mid_atlantic`

**Files:**
- Modify: `tools/region_cell_audit.py` (add `mid_atlantic` to `REGION_CONFIG`)
- Modify: `tools/build_region_promote.py` (add `mid_atlantic` to `STAGING` + `EXPECTED_CELLS`)
- Test: `tools/test_region_cell_audit.py`, `tools/test_build_region_promote.py` (extend existing)

**Interfaces:**
- Consumes: the shipped region-generic tools.
- Produces: `REGION_CONFIG["mid_atlantic"]` (label, span `["7","8"]`, frost_model `"anchored"`); `STAGING["mid_atlantic"]` (the 5 staging files) + `EXPECTED_CELLS["mid_atlantic"] = 111`. `region_harness.gate_crop("mid_atlantic", ["7","8"], slug, cells)` works with no harness change.

- [ ] **Step 1: Write the failing test for the auditor config**

Append to `tools/test_region_cell_audit.py`:
```python
def test_mid_atlantic_config_present_anchored():
    import region_cell_audit as rca
    cfg = rca.REGION_CONFIG["mid_atlantic"]
    assert cfg["span"] == ["7", "8"]
    assert cfg["frost_model"] == "anchored"
    assert cfg["label"] == "Mid-Atlantic: Piedmont and Coastal Plain"

def test_mid_atlantic_cold_pause_allowed():
    import json, region_cell_audit as rca
    cell = {
        "region_id": "mid_atlantic",
        "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
        "zone_span": ["7", "8"],
        "resolved_by_zone": {
            z: {"plant_out": "Apr 8 - Jun 1", "harvest": "Jun 20 - Sep 1",
                "harvest_start": "Jun 20", "harvest_end": "Sep 1",
                "first_plant_date": "Apr 8", "last_plant_date": "Jun 1",
                "resolution_method": "frost_anchored_resolved",
                "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30"},
                "calendar": ["cold_pause","cold_pause","cold_pause","plant","plant","growing",
                             "harvest","harvest","harvest","growing","cold_pause","cold_pause"]}
            for z in ("7", "8")}}
    assert not any("cold_pause" in v for v in rca.audit_cell("broccoli", cell, "mid_atlantic"))
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k mid_atlantic -v`
Expected: FAIL with `KeyError: 'mid_atlantic'`.

- [ ] **Step 3: Add the `mid_atlantic` config entry**

In `tools/region_cell_audit.py`, add to `REGION_CONFIG` (after the `pnw` entry):
```python
    "mid_atlantic": {"label": "Mid-Atlantic: Piedmont and Coastal Plain",
                     "span": ["7", "8"], "frost_model": "anchored"},
```

- [ ] **Step 4: Run auditor tests to verify they pass**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k mid_atlantic -v`
Expected: 2 passed.

- [ ] **Step 5: Write the failing test for the promote emitter**

Append to `tools/test_build_region_promote.py` (mirror the existing pnw test; the 111 count asserts only AFTER Tasks 4-7 stage the cells, so gate this test to skip if the staging files are absent):
```python
def test_mid_atlantic_registered():
    import build_region_promote as brp
    assert "mid_atlantic" in brp.STAGING
    assert brp.EXPECTED_CELLS["mid_atlantic"] == 111
    files, band = brp.STAGING["mid_atlantic"]
    assert band == "mid_atlantic_chill_band.json"
    assert set(files) == {
        "mid_atlantic_annuals_cool.json", "mid_atlantic_annuals_warm.json",
        "mid_atlantic_trees.json", "mid_atlantic_citrus.json", "mid_atlantic_perennials.json"}
```

- [ ] **Step 6: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k mid_atlantic -v`
Expected: FAIL (`KeyError` / assertion).

- [ ] **Step 7: Add the `mid_atlantic` STAGING + EXPECTED_CELLS entries**

In `tools/build_region_promote.py`:
```python
STAGING = {
    "pnw": (["pnw_annuals.json", "pnw_trees.json", "pnw_citrus.json", "pnw_perennials.json"],
            "pnw_chill_band.json"),
    "mid_atlantic": (["mid_atlantic_annuals_cool.json", "mid_atlantic_annuals_warm.json",
                      "mid_atlantic_trees.json", "mid_atlantic_citrus.json",
                      "mid_atlantic_perennials.json"], "mid_atlantic_chill_band.json"),
}
EXPECTED_CELLS = {"pnw": 108, "mid_atlantic": 111}
```

- [ ] **Step 8: Run test to verify it passes**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k mid_atlantic -v`
Expected: PASS.

- [ ] **Step 9: Regression guard -- confirm pnw config untouched**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py test_build_region_promote.py -v`
Expected: all pass (pnw + mid_atlantic).

- [ ] **Step 10: Commit** (explicit pathspec)

```bash
git add tools/region_cell_audit.py tools/build_region_promote.py tools/test_region_cell_audit.py tools/test_build_region_promote.py
git status
git commit -m "feat(mid_atlantic): register region in cell-auditor + promote-emitter (z7-8, anchored, 111 cells)"
git show --stat HEAD
```

---

## Task 3: T1 sourcing pass (VCE 426-331 + NC State) + the chill band

**Files:**
- Create: `docs/reviews/notes/2026-07-20/mid_atlantic_sources.md`
- Create: `tools/staging/mid_atlantic_chill_band.json`

**Interfaces:**
- Produces: the sourcing table (crop/class -> source id + url + spring/FALL windows + frost dates) that Tasks 4-7 author from.
- Produces: `region_chill_delivered.mid_atlantic` band + provenance (drives A3 in Task 5).

- [ ] **Step 1: Extract the T1 sources, by class**

Primary sources are **already catalogued** (`ncsu_ext`, `vce_426_331`) -- this is extraction, not a fresh hunt. Use WebFetch + `pypdf` in THIS controller env (subagent sandboxes block PDF tooling).
- **`vce_426_331`** (`https://www.pubs.ext.vt.edu/426/426-331/426-331.html`) -- the zone-8a/8b spring AND fall planting-date tables. **Extract the FULL crop coverage, not just tomato** -- this table determines which crops get a fall cycle at all. This is the single most load-bearing document in the arc.
- **`ncsu_ext`** -- the "Central North Carolina Planting Calendar for Annual Vegetables, Fruits, and Herbs" (`https://content.ces.ncsu.edu/central-north-carolina-planting-calendar-...`) for transplant/succession windows; the Extension Gardener Handbook ch. 15 for chill (">1,000 hrs/yr", 750-hr variety-min recommendation); the home-garden blueberry guide for the highbush/rabbiteye variety steer; the frost-date table for z8 (Raleigh: last Apr 8, first Oct 30).
- **z7 frost normals** -- a northern-Piedmont / central-MD or Richmond anchor (VCE + the State Climate Office of NC/VA both publish them). z7 last frost is roughly 2-3 weeks later than z8; source the actual dates, do not interpolate blindly.
- **Chill band** -- from NC State's ">1,000 hrs/yr" figure, in a model comparable to the existing table's neighbors (`northern_tier` z7 `[700,1200]`, `se_gulf` z8 `[650,1000]`, `ca_interior` z8 `[500,1100]`).

Record each as: source id, url, verified date `2026-07-20`, the crop windows it supports (SPRING and FALL), the frost dates. Flag any crop where a T1 fall window is absent (that crop is authored spring-only, honestly, not with an invented fall cycle).

- [ ] **Step 2: Write the sourcing table**

Write `docs/reviews/notes/2026-07-20/mid_atlantic_sources.md` -- a table `crop_or_class | source_id | url | spring_window | fall_window | frost_dates | tier | notes`. Top block: the z7 and z8 frost-date normals every annual cell's `resolved_from` uses. A dedicated column marks which crops have a documented fall cycle (drives Task 4's warm sub-batch).

- [ ] **Step 3: Author the chill band**

Write `tools/staging/mid_atlantic_chill_band.json`:
```json
{
  "region_chill_delivered.mid_atlantic": {"7": [<lo>, <hi>], "8": [<lo>, <hi>]},
  "region_chill_delivered_provenance.mid_atlantic": "<sourced note: NC State Extension documents >1,000 chill hours annually across the belt; url; verified 2026-07-20>"
}
```
z7 (colder winter) low-bound >= z8. Verify against `chill_gate.py`'s shape (region -> {zone -> [lo,hi]}, numeric, lo<=hi). The band clears every canonical apple variety (max 900, McIntosh), so A3 resolves the whole tree set to `fruits_reliably` on real evidence.

- [ ] **Step 4: Commit** (explicit pathspec)

```bash
git add docs/reviews/notes/2026-07-20/mid_atlantic_sources.md tools/staging/mid_atlantic_chill_band.json
git status
git commit -m "docs(mid_atlantic): T1 sourcing table (VCE 426-331 + NC State) + chill band"
git show --stat HEAD
```

---

## Task 4: Author the 82 frost_anchored annual cells (cool + warm sub-batches)

**Files:**
- Create: `tools/staging/mid_atlantic_annuals_cool.json`, `tools/staging/mid_atlantic_annuals_warm.json` (`{slug: cell}`)

**Interfaces:**
- Consumes: `docs/mid_atlantic_cell_contract.md`, `docs/reviews/notes/2026-07-20/mid_atlantic_sources.md`, `region_harness.gate_crop`, `region_cell_audit`.
- Produces: the two annual staging files (82 cells total).

This task is the substantive one and is subagent-parallelizable: one worker per crop (or per family). Split the 82 by season-class first (from the contract / sources note). **Per-crop procedure:**

- [ ] **Step 1: Author the cell for crop `<slug>`**

Read the crop's existing `northern_tier` z7 cell (same states, the cooler edge -- the closest existing analog for `plantings[]` track structure + DTM) and, for warm-season crops, the `se_gulf` z8 cell (the fall-cycle shape). Author the `mid_atlantic` cell:
- `region_id="mid_atlantic"`, `region_label="Mid-Atlantic: Piedmont and Coastal Plain"`, `zone_span=["7","8"]`.
- `resolved_by_zone` keys `"7"` and `"8"`; `resolved_from` = the z7 / z8 frost normals from the sources note; `resolution_method="frost_anchored_resolved"`.
- **Cool-season:** long spring-through-fall run + real fall/overwintering windows where sourced; **no `heat_pause`**.
- **Warm-season:** spring cycle + a T1-sourced `heat_pause` (only the months VCE/NC State document a real set-failure gap) + a `second_planting` fall cycle **only where a T1 fall window exists** (spring-only otherwise, flagged honestly). Keep primary windows single-span; put the `second_planting` envelope inside them (A43).
- Dual-register `region_notes_{beginner,seasoned}` in the house voice (no em dashes).
- Cite `vce_426_331` / `ncsu_ext` in `sources` + `anchoring_urls` (verified 2026-07-20).

- [ ] **Step 2: Derive the `calendar[]`**

```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell=json.load(open('tools/staging/mid_atlantic_annuals_warm.json'))['<slug>']['resolved_by_zone']['8']
print(derive_annual_calendar(cell))
"
```
Set each zone's `calendar[]` to the derived 12-token array. Expected for a warm-season crop: `cold_pause` winter, spring `plant`/`growing`, a `heat_pause` at the sourced midsummer months, a fall `plant`/`harvest` reflush, `cold_pause` late fall. Confirm the deriver picks up `second_planting` (as it does for the `se_gulf` template).

- [ ] **Step 3: Gate the crop in isolation**

Run: `python3 tools/region_harness.py mid_atlantic 7,8 tools/staging/mid_atlantic_annuals_warm.json <slug>` (or the cool file)
Expected: PASS (A45 parity on `["7","8"]`, A31/A32, A43 envelope clean, calendar coherence clean, 0 em dashes, sources T1).

- [ ] **Step 4: Audit the cell.** Run `python3 tools/region_cell_audit.py mid_atlantic tools/staging/mid_atlantic_annuals_warm.json` -- expect 0 issues. Fix + re-gate until PASS + clean audit. Common failures: A43 envelope spanning the fall cycle, A24/A25 token placement, em dash, span/key mismatch, `resolved_from` left null, an unsourced `heat_pause`.

- [ ] **Step 5: RED-check A43 once** (adversarial, per Global Constraints): on a scratch copy of one warm cell, widen the `second_planting` envelope so `harvest_end` falls OUTSIDE the first harvest span; run `region_harness` and confirm A43 bounces it; discard the scratch edit. Record the result in the dry-run note (Task 9).

- [ ] **Step 6: Commit the batches** (after all 82 pass; explicit pathspec)

```bash
git add tools/staging/mid_atlantic_annuals_cool.json tools/staging/mid_atlantic_annuals_warm.json
git status
git commit -m "feat(mid_atlantic): author 82 frost_anchored annual cells (fall cycle for warm-season, VCE/NC State)"
git show --stat HEAD
```

---

## Task 5: Author the 14 chill_gated tree cells (all fruits_reliably)

**Files:**
- Create: `tools/staging/mid_atlantic_trees.json`

**Interfaces:**
- Consumes: `docs/mid_atlantic_cell_contract.md` (tree template), the sources note, `tools/staging/mid_atlantic_chill_band.json`, `region_harness.gate_crop`.
- Produces: `tools/staging/mid_atlantic_trees.json`.

NC chill >1,000 hr clears the whole canonical variety range, so the A3 split resolves every tree to `fruits_reliably` on real evidence (the opposite of RGV's no-fruit citrus story, and cleaner than PNW's edge cases).

- [ ] **Step 1: Author each tree cell** against the tree template. Read the crop's existing `northern_tier` tree cell for the fruiting-cell shape. All 14 (apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate): `suitability="fruits_reliably"`, real `bloom` + `harvest` windows from NC State/VCE, `chill_basis_{seasoned,beginner}` stating the delivered >1,000-hr band vs the crop's requirement. In apple's `suitability_note_seasoned`, note NC State's guidance to prefer 750+-hour varieties because the belt's real risk is premature bloom in warm winter spells, not chill deficit. **Pawpaw is native here** -- frame it as a genuine strength. Any real heat/humidity caveat is sourced, not assumed (none expected).
- [ ] **Step 2: Gate each crop** via `python3 tools/region_harness.py mid_atlantic 7,8 tools/staging/mid_atlantic_trees.json <slug>` -> PASS. Confirm A3 (`perennial_gate`) coheres: `fruits_reliably` requires a calendar and the delivered band >= requirement. Audit via `region_cell_audit`.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/mid_atlantic_trees.json
git status
git commit -m "feat(mid_atlantic): author 14 chill_gated tree cells (all fruits_reliably; >1,000 hr chill)"
git show --stat HEAD
```

---

## Task 6: Author the 5 citrus cells (cold-limited)

**Files:**
- Create: `tools/staging/mid_atlantic_citrus.json`

**Interfaces:**
- Consumes: `docs/mid_atlantic_cell_contract.md` (citrus template), `region_harness.gate_crop`.
- Produces: `tools/staging/mid_atlantic_citrus.json`.

- [ ] **Step 1: Author each citrus cell** (grapefruit, lemon, lime, mandarin-clementine, orange-navel) against the citrus template. Read the crop's existing `northern_tier`/`se_gulf` citrus cell shape. `suitability="survives"` (container culture is real in z8 Tidewater -- source it) or `"unsuitable"` per NC State/VCE; `min_winter_temp_f`; `cold_basis_{seasoned,beginner}` explaining the cold limit honestly. A32-exempt; minimal calendar.
- [ ] **Step 2: Gate each** via `python3 tools/region_harness.py mid_atlantic 7,8 tools/staging/mid_atlantic_citrus.json <slug>` -> PASS; A3 coheres (no `fruits_reliably`). Audit via `region_cell_audit`.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/mid_atlantic_citrus.json
git status
git commit -m "feat(mid_atlantic): author 5 citrus cells (cold-limited survives/unsuitable)"
git show --stat HEAD
```

---

## Task 7: Author the 10 remaining perennials (woody herbs + berries + strawberry)

**Files:**
- Create: `tools/staging/mid_atlantic_perennials.json`

**Interfaces:**
- Consumes: `docs/mid_atlantic_cell_contract.md`, the sources note, `region_harness.gate_crop`.
- Produces: `tools/staging/mid_atlantic_perennials.json`.

All frost-anchored calendar cells (A32 applies -- real calendars required).

- [ ] **Step 1: Author each cell.**
  - **Woody herbs (lavender, oregano, rosemary, sage, thyme):** real frost-anchored calendars. Humidity is the constraint on lavender/rosemary here (the `se_gulf` humidity-struggle framing is the closer analog than PNW's rain-shadow thriving) -- source the honest verdict. Where a herb is grown as an annual / needs winter protection at the z7 edge, use the existing `grown_as` field (as `northern_tier` does for thyme).
  - **Berries (blackberry, blueberry, elderberry, raspberry):** real calendars + strong suitability notes. **Blueberry:** use `recommended_type` + `type_note_{seasoned,beginner}` for the NC-region highbush-vs-rabbiteye steer (NC State names Duke/Jersey highbush + Premier rabbiteye for the belt -- cultivars already on the canonical list). Blackberry, raspberry, elderberry: real windows, T1-sourced.
  - **Strawberry:** real frost-anchored calendar (the mid-Atlantic runs both a matted-row and a plasticulture system; author what NC State/VCE document, `grown_as` where relevant).
- [ ] **Step 2: Gate each** via `python3 tools/region_harness.py mid_atlantic 7,8 tools/staging/mid_atlantic_perennials.json <slug>` -> PASS. Audit via `region_cell_audit`.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/mid_atlantic_perennials.json
git status
git commit -m "feat(mid_atlantic): author 10 perennial cells (woody herbs + berries + strawberry)"
git show --stat HEAD
```

---

## Task 8: Build the atomic promote batch

**Files:**
- Create: `tools/batches/mid_atlantic_region_promote.json` (generated)

**Interfaces:**
- Consumes: the five `tools/staging/mid_atlantic_*.json` cell files + `tools/staging/mid_atlantic_chill_band.json`; the Task 2 `STAGING`/`EXPECTED_CELLS` entries.
- Produces: `tools/batches/mid_atlantic_region_promote.json` -- an `apply_patch` batch adding, per crop, `$.crops[?(@.slug=='<slug>')].regions.mid_atlantic` (op `add`), plus top-level `region_chill_delivered.mid_atlantic` + provenance. `EXPECTED_SPANS.mid_atlantic` is a CODE edit to `tools/zone_span_gate.py` (Task 10 Step 1), applied in the same commit as the batch, NOT part of the JSON batch.

- [ ] **Step 1: Generate the batch**

Run: `python3 tools/build_region_promote.py mid_atlantic`
Expected stdout: `emitted 113 patches (111 mid_atlantic cells + 2 top-level) ...` (111 cells + chill band + provenance). The emitter asserts `len(seen) == 111` (from `EXPECTED_CELLS`), so a miscount aborts here.

- [ ] **Step 2: Verify the generated batch**

Run:
```bash
python3 -c "
import json
b=json.load(open('tools/batches/mid_atlantic_region_promote.json'))
ops=b['patches']
cells=[o for o in ops if o['json_path'].endswith('.regions.mid_atlantic')]
assert len(cells)==111, len(cells)
assert all(o['op']=='add' for o in ops), 'mid_atlantic is net-new everywhere'
assert any('region_chill_delivered.mid_atlantic'==o['json_path'].lstrip('\$.') for o in ops)
print('batch OK:', len(ops), 'ops,', len(cells), 'cells')
"
```
Expected: `batch OK: 113 ops, 111 cells`.

- [ ] **Step 3: Commit** (batch only; canonical still untouched; explicit pathspec)

```bash
git add tools/batches/mid_atlantic_region_promote.json
git status
git commit -m "feat(mid_atlantic): deterministic atomic-promote batch (111 cells + chill band)"
git show --stat HEAD
```

---

## Task 9: Dry-run the promote on a scratch copy (full gate ceremony, RED-checked)

**Files:**
- Modify (scratch only): a copy of `crops_data_final.json` + `tools/zone_span_gate.py`
- Create: `docs/reviews/notes/2026-07-20/mid_atlantic_promote_dryrun.md`

**Interfaces:**
- Consumes: `tools/batches/mid_atlantic_region_promote.json`, `region_harness.build_scratch_tools`, `region_cell_audit`.
- Produces: proof that the full suite is green post-promote before touching the real canonical.

- [ ] **Step 1: Apply the batch to a scratch canonical.** Compute `sha256_before` from the real file, apply via `tools/apply_patch.py` to a COPY, confirm COMPACT + count 128 + footprint = exactly 111 `regions.mid_atlantic` + the top-level `region_chill_delivered.mid_atlantic` + provenance via a byte-diff audit (no other key touched).

- [ ] **Step 2: Add `mid_atlantic` to a scratch `EXPECTED_SPANS`** (via `region_harness.build_scratch_tools(dest, "mid_atlantic", ["7","8"])`) and run the full suite against the scratch canonical + scratch tools:
  - `gate_all.py` -> 119/119.
  - `zone_span_gate.py` (A45) -> 0.
  - `coverage_floor_gate.py` (A31/A32) -> 0 (all 111 carry `mid_atlantic`).
  - `chill_gate.py` -> 0.
  - `second_planting_gate.py` (A43) -> 0 across all authored fall cycles.
  - `whole_crop_gate.py` on a per-class sample (broccoli, cherry-tomato, apple, orange-navel, blueberry, lavender, strawberry) -> PASS.
  - `region_cell_audit.py mid_atlantic` over all five staging files -> 0 issues.
  - `calendar_coherence` + `timing_spine` -> 0.
  - `release_verify.py` -> clean modulo the documented roster-wide section-A collateral (the pre-commit backstop is the binding multi-crop gate).

- [ ] **Step 3: RED-check the promote** -- on the scratch copy: (a) drop the `"7"` key from one crop's `mid_atlantic` cell and confirm A45 bounces it; restore. (b) widen a `second_planting` envelope past the first harvest span and confirm A43 bounces it; restore. This proves the ceremony catches the span-parity + fall-envelope defect classes at roster scale.

- [ ] **Step 4: Record the dry-run result** in `docs/reviews/notes/2026-07-20/mid_atlantic_promote_dryrun.md` (gate outputs + footprint audit + the RED-check results). Commit (explicit pathspec).

```bash
git add docs/reviews/notes/2026-07-20/mid_atlantic_promote_dryrun.md
git status
git commit -m "test(mid_atlantic): scratch-copy promote dry-run green + A45/A43 RED-check"
git show --stat HEAD
```

---

## Task 10: Promote to canonical + release ceremony (THE one canonical write)

**Files:**
- Modify: `crops_data_final.json` (the atomic promote)
- Modify: `tools/zone_span_gate.py` (add `mid_atlantic` to `EXPECTED_SPANS`)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`
- Modify: `docs/region_coverage_roadmap.md`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 0: CONCURRENCY COORDINATION.** Before touching the canonical:
  - `git fetch` + `git log --oneline origin/main..main` + `git log -1 crops_data_final.json` -- determine whether any concurrent session promoted since `e1e01c47`.
  - Re-read the LIVE canonical SHA: `shasum -a 256 crops_data_final.json`. If it is no longer `e1e01c47`, a concurrent promote landed. If that promote is path-disjoint from `*.regions.mid_atlantic` (e.g. a variety block or a different region), that is FINE, but you MUST: (a) re-run the roster query against the live canonical to confirm still 111 region-carrying certified; (b) re-run each staging file through `region_harness` against the live canonical to confirm all cells still gate green; (c) use the LIVE SHA as `sha256_before`.
  - Do NOT both hold the canonical open at once (the sweet-corn collision rule).

- [ ] **Step 1: Add `mid_atlantic` to the REAL `tools/zone_span_gate.py` `EXPECTED_SPANS`** (`"mid_atlantic": ["7","8"]`). `coverage_floor_gate` auto-derives its `CANONICAL_REGIONS`/`CANONICAL_ZONES`.

- [ ] **Step 2: Apply the batch to the REAL canonical** via `tools/apply_patch.py` with the real `sha256_before` (the LIVE SHA from Step 0). Confirm COMPACT, no trailing newline, count 128. (Regenerate the batch first via `build_region_promote.py mid_atlantic --base-sha <LIVE SHA>` if the emitter stamps the SHA into the batch; otherwise pass it to `apply_patch`.)

- [ ] **Step 3: Full release verification** (protocol #6):
  - `python3 tools/whole_crop_gate.py <slug>` on the 18 gold anchors -> 18/18 PASS.
  - `python3 tools/gate_all.py` -> 119/119.
  - `python3 tools/zone_span_gate.py` (A45), `coverage_floor_gate.py` (A31/A32), `chill_gate.py`, `second_planting_gate.py` (A43) -> 0.
  - `python3 tools/release_verify.py` -> clean (modulo documented roster-wide section-A collateral).
  - `python3 tools/region_cell_audit.py mid_atlantic tools/staging/mid_atlantic_*.json` -> 0.
  - Independent footprint audit: exactly 111 `regions.mid_atlantic` + `region_chill_delivered.mid_atlantic` + provenance changed; all else byte-identical; count 128.
  - The **pre-commit backstop** (`precommit_release_verify.py`) runs on commit -- checks ALL changed crops.
  - Per-batch source-truth sample: re-verify 3-4 authored windows (including at least 2 FALL windows) against their cited VCE/NC State URLs.

- [ ] **Step 4: State trio** -- surgically update CURRENT_STATE.md (drift memory `current-state-md-drift`: hand-maintain, no `---`), prepend STATE_HISTORY.md (most-recent-first), bump LATEST.txt (new SHA + session line).

- [ ] **Step 5: Roadmap + register** -- mark roadmap item 8 SHIPPED (with the new canonical SHA + commit); add a `docs/field_addition_register.md` row (#19) for the Mid-Atlantic region column.

- [ ] **Step 6: Commit** (UNPUSHED -- Trevor confirms push; explicit pathspec)

```bash
git add crops_data_final.json tools/zone_span_gate.py CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/region_coverage_roadmap.md docs/field_addition_register.md
git status
git commit -m "feat(mid_atlantic): certify the Mid-Atlantic region across 111 crops"
git show --stat HEAD
```

---

## Task 11: Write the paired plant-app kickoff

**Files:**
- Create: `docs/kickoffs/33-mid-atlantic-plant-app.md`

**Interfaces:**
- Produces: the handoff so plant-app can route the belt's ZIPs to `mid_atlantic`.

- [ ] **Step 1: Write the kickoff** covering:
  - `REGION_STATES.mid_atlantic = ['NC','VA','MD','DC','DE','NJ','PA']`.
  - `regions.json` row + `SHORT_REGION_LABEL.mid_atlantic`.
  - **No ZIP3 fence expected** -- unlike RGV/PNW/Alaska, this belt has no adjacent-but-different climate pocket sharing its state+zone signature (confirm during build). State the confirm-result explicitly.
  - **The z7 half depends on the temperate-region resolution fix (kickoff #32)** -- cross-reference it; this region is the first real consumer of that fix (3,131 z7 ZIPs). If #32 has already landed (the plant-app session was working it as of 2026-07-20), note that the z7 half should resolve immediately; if not, it delivers only the z8 half until #32 lands.
  - Note: dataset side is `<new canonical SHA>`; plant-astro consumes spans + chill band + tree calendars automatically.

- [ ] **Step 2: Commit** (explicit pathspec)

```bash
git add docs/kickoffs/33-mid-atlantic-plant-app.md
git status
git commit -m "docs(kickoff): plant-app Mid-Atlantic REGION_STATES handoff (#33)"
git show --stat HEAD
```

---

## Task 12: Update memory + close out

- [ ] **Step 1:** Update memory `mid-atlantic-region-spec` -> SHIPPED (canonical SHA, commit, 111 cells; reusable lessons: **the fall-cycle heat_pause+second_planting reuse of existing machinery -- no new gate/field**; sources already catalogued; the tooling extended by two dict entries not rebuilt; the A43 envelope as the main gate-churn source; whether the no-ZIP3-fence prediction held). Confirm the MEMORY.md pointer.
- [ ] **Step 2:** Summarize to Trevor: what shipped, the unpushed commit, the plant-app kickoff (#33) + the #32 dependency for the z7 half, and that no plant-astro bump was done. Flag that item 9 (mid-South) is next and has the identical gap shape -- this arc is its template.

---

## Self-Review

**Spec coverage:**
- Product goal (Mid-Atlantic honest calendars w/ fall cycle) -> Tasks 4-10. ✓
- Option A full roster-wide (111) -> Tasks 4-7 enumerate all 111 (82+14+5+5+4+1). ✓
- Frost-ANCHORED + standard deriver, no new field/gate (spec §2) -> Global Constraints + Task 4 (existing heat_pause/second_planting). ✓
- zone_span ["7","8"] DECIDED (spec §4.2) -> Global Constraints; z7 delivery via kickoff #32 (app-side). ✓
- The fall cycle is the substantive work (spec §4.5) -> Task 4 warm sub-batch + A43. ✓
- region_chill_delivered band clears the tree set (spec §4.6) -> Task 3 + Task 5 (all fruits_reliably). ✓
- Trees fruits_reliably / citrus cold-limited / blueberry recommended_type steer (spec §5) -> Tasks 5, 6, 7. ✓
- Sourcing T1 VCE/NC State, already catalogued (spec §6) -> Task 3. ✓
- Toolchain extended not rebuilt (spec §7) -> Task 2 (two dict entries + tests). ✓
- Atomic promote (A45/A31 pincer) (spec §7) -> Tasks 8-10. ✓
- Verification incl. A43 (spec §8) -> Tasks 9-10. ✓
- App handoff, no fence (spec §9) -> Task 11. ✓
- State trio + roadmap + register + memory (spec §12) -> Tasks 10, 12. ✓
- Non-goals (no new field/gate, no z6, no app/astro edits) -> honored. ✓

**Placeholder scan:** authored window VALUES are produced by Task 3 (sourcing) and consumed by Tasks 4-7 against the Task 1 template -- the data-authoring analog of "implement per spec," not a placeholder; the STRUCTURE and gate loop are fully concrete. `<slug>`, `<lo>/<hi>`, `<date>`, `<new canonical SHA>` are per-item substitutions. The chill-band numbers + frost dates are explicit sourcing tasks (Task 3) with a stated method + comparison neighbors.

**Type consistency:** `region_harness.gate_crop(region_id, span, slug, staged_cells) -> (bool, str)` used consistently (Tasks 4-7, 9); `region_cell_audit.audit_cell(slug, cell, region_id) -> list` / `audit_cells(region_id, paths) -> int` (Tasks 2, 4-7, 9-10); `build_region_promote.py <region_id>` reads exactly the five staging files + chill band via `STAGING["mid_atlantic"]`; `EXPECTED_CELLS["mid_atlantic"] == 111`; staging files are `{slug: cell}` throughout. ✓

**Open confirm-items flagged, not hidden:** the `build_region_promote.py` batch-key path form (Task 8 Step 2 -- confirm against the shipped `pnw_region_promote.json`), whether the emitter stamps `sha256_before` (Task 10 Step 2), the VCE fall-window crop coverage (Task 3 -- determines the warm sub-batch membership), and the concurrent-promote ordering (Task 10 Step 0) are marked "confirm against the real tool / live state," not assumed.
