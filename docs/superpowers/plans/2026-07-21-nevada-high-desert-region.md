# Nevada High-Desert Region Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author and certify a real Nevada high-desert region (`nevada`, Las Vegas Valley / Clark County, z8-9-10) across all 111 certified region-carrying crops, so the belt stops riding generic frost-anchored zone dates whose flat back half is actively misleading (shows `growing` through the Jun-Sep >90degF fruit-set abort AND through the real Nov 25 frost return).

**Architecture:** Nevada is FROST-ANCHORED (`resolution_method="frost_anchored_resolved"`, real `resolved_from` frost dates, `cold_pause` winters), same model as mid-Atlantic / mid-South / PNW, so `calendar[]` is DERIVED by the standard `tools/annual_calendar.py` -- NO deriver change, NO new field, NO new gate. The desert differentiator: **every warm-season annual and every cool-season annual carries a summer `heat_pause` (Jun-Sep)** -- a shape already live in 289 existing `heat_pause`+`cold_pause` cells (e.g. `bell-pepper mid_south z8`). The three deltas from the humid belts: (1) **warm crops get NO `second_planting`** (UNR does not recommend a fall replant -- the inverse of mid-South's tomato), a single spring cycle + heat_pause + cold_pause; **cool crops keep a fall replant** (`second_planting` mid-Aug-Oct, built via `tools/second_cycle.py`); (2) **apple** stays `fruits_reliably` but its `chill_basis_*` prose steers varieties (Trevor-confirmed Option A); (3) **garlic** gets its own narrower Sept-mid-Oct window. All 111 cells are authored OFF-canonical into per-class staging files, gated per-crop against a scratch canonical (scratch tools with `nevada` in `EXPECTED_SPANS` + `staging/nevada_sources.json` injected into `source_catalog`), then promoted in ONE atomic SHA-guarded batch. `gate_all` is green before (no `nevada`) and after (`nevada` everywhere), never mid-flip.

**Tech Stack:** Python 3 standalone gate scripts (`whole_crop_gate.py`, `gate_all.py`, `zone_span_gate.py`, `coverage_floor_gate.py`, `chill_gate.py`, `second_planting_gate.py`, `photoperiod_gate.py`, `annual_calendar.py`, `second_cycle.py`, `apply_patch.py`), the region-generic tooling (`region_harness.py`, `region_cell_audit.py`, `build_region_promote.py` -- already built + source-injection-capable from mid-South, extended not rebuilt), `prose_window_sweep.py`, compact JSON canonical, git on `main`.

## Global Constraints

Copied verbatim from the spec (`docs/superpowers/specs/2026-07-21-nevada-high-desert-region-design.md`) + CLAUDE.md; every task's requirements implicitly include these.

- **Canonical JSON is COMPACT:** `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` until the atomic promote (Task 11).** All authoring happens in staging files under `tools/staging/`.
- **TDD: RED before GREEN.** No new gate ships this arc, but every tool extension (Task 2) and the promote ceremony (Task 10) is adversarially proven on a scratch copy before it is trusted: RED-check A45 by dropping a zone key from a 3-zone `nevada` cell; RED-check A43 by widening a cool-crop `second_planting` envelope past the first harvest span; RED-check A9 by flipping onion's `nevada` `recommended_day_length_type` to `long_day` with a spring `plant_out`.
- **T1-or-it-doesn't-ship.** Every authored window/verdict cites a Tier-1 source (`.edu`/`.gov` university extension or NWS). Nevada's sources are largely NOT pre-catalogued (like mid-South): register the new ids in `tools/staging/nevada_sources.json` (Task 3). The single Almanac.com frost cross-check is NOT registered (secondary aggregator; directional corroboration only). No fabricated precision: a thin-source crop gets a conservative cell, flagged, never invented.
- **No em dashes in consumer copy** (`region_notes_*`, `suitability_note_*`, `chill_basis_*`, `zone_notes`, `notes`): use commas/colons/semicolons/periods. `--` is fine in docs/commits/code. American English. Temps render as `°F`. "plant" lowercase except at sentence start or "Plant Pro".
- **Zone span `nevada = ["8","9","10"]`** (DECIDED; spec §2). z9 = 94 belt ZIPs (Las Vegas Valley, dominant), z8 = 15 (cooler/higher pockets), z10 = 1 (Laughlin, rides the belt verdict). Every `nevada` cell's `resolved_by_zone` keys are EXACTLY `"8"`, `"9"`, `"10"` (A45 parity). z10 gets a real cell (1 ZIP but A45/A31 require full span parity). The z8 tail's in-app delivery depends on the plant-app `isWarm` fix (kickoff #32), NOT on this dataset build.
- **Nevada is FROST-ANCHORED:** `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost":<date>,"first_frost":<date>}` (real dates per zone), `calendar[]` DERIVED by `tools/annual_calendar.py`. `cold_pause` in winter is EXPECTED and correct. **Frost anchor z9: last frost Feb 28 / first frost Nov 25** (NWS WR-235). Warm-crop indoor starts are authored to **early February** (6 weeks before UNR's mid-March transplant) so January stays `cold_pause` and the deriver renders the honest winter (a January-active cell suppresses `cold_pause` -- the ruling's finding; avoid it).
- **The desert `heat_pause` is the point, and it must be SOURCED.** `heat_pause` is declaration-driven in the deriver (`annual_calendar.py` emits it only for a cell's declared `heat_pause` months), so an unsourced pause silently reshapes the calendar. Nevada's is UNR's >90degF-day / <55degF-night fruit-set cutoff, Jun-Sep (SP-99-11 / FS-02-61). SOURCE IT.
- **A43 governs `second_planting` shape** (cool crops only here): single-span `start_indoors`/`plant_out`/`harvest`; envelope (`harvest_end` inside the FIRST harvest span, `last_plant_date` inside the FIRST `plant_out` span) INSIDE the primary windows. Read `tools/second_planting_gate.py`'s docstring; build two-window cool cells with `tools/second_cycle.py:build_two_cycle_cell(base, spring, fall)` (combine-derive-then-split; the deriver does NOT render `second_planting` directly -- memory `fall-cycle-deriver-combine-then-split`).
- **A9 (`photoperiod_gate`) WATCH:** desert onions are short-day/intermediate and fall-planted, which FORBIDS an April-or-later `plant_out` (memory `onion-daylength-intermediate-a9-window-fit`). Author onion's `nevada` `recommended_day_length_type` as `short_day` or `intermediate_day` and a FALL `plant_out` (Oct-Nov). Shallot follows onion by species identity. VERIFY A9 clean per Task 5.
- **State trio at content release** (Task 11): CURRENT_STATE.md surgical (drift memory `current-state-md-drift`: no `---` separator, hand-maintain), STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session.
- **No plant-astro submodule bump from this session** (memory `plant-astro-bump-owned-by-astro-session`). **Trevor confirms every push.** Don't commit the canonical change until Trevor approves.
- **CONCURRENT-CHECKOUT DISCIPLINE (active this repo).** Other sessions may share this checkout (memory `subagent-resumability-and-concurrent-git-safety`). Every commit: explicit-pathspec `git add` (never `git add -A`), `git status` before, `git show --stat` after. Tasks 1-10 are off-canonical (staging/scratch/tools) and collision-safe; only Task 11 writes the canonical, SHA-guarded. There is a stray untracked `tools/staging/shards/` from the mid-South run -- leave it or `rm -rf` it; do not commit it.

## Crop roster (the 111, by class)

Locked from canonical `a071f0c1` (`verification_status.status == "verified_gs_arc"` AND non-empty `regions`). Re-run the query against the LIVE canonical at build start in case a concurrent session certified a crop.

Roster query (run at build start):
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
Expected: 82 frost_anchored + 14 perennial_chill_gated + 5 perennial_evergreen + 5 perennial_woody_ornamental + 4 berries_woody + 1 perennial_herbaceous = TOTAL 111.

- **frost_anchored (82):** the annual vegetable + herb roster. **Split for authoring into WARM (Task 4) and COOL/fall-planted (Task 5).** Warm-vs-cool classifier (run at build start; refine per-crop from the sources note):
  ```bash
  python3 -c "
  import json
  d=json.load(open('crops_data_final.json'))
  for c in d['crops']:
      if c.get('verification_status',{}).get('status')!='verified_gs_arc' or not c.get('regions'): continue
      if c.get('calendar_basis')!='frost_anchored': continue
      # 'warm' if any hot-region cell already carries a summer heat_pause
      warm=False
      for rk in ('low_desert_az','se_gulf','warm_arid','ca_desert','fl_peninsula'):
          rc=c.get('regions',{}).get(rk)
          if not rc: continue
          for z,zc in (rc.get('resolved_by_zone') or {}).items():
              if 'heat_pause' in (zc.get('calendar') or []) or 'heat_pause' in zc: warm=True
      print(('WARM' if warm else 'cool'), c['slug'], 'frost_tol', c.get('frost_tolerance_f'))
  " | sort
  ```
  The fall-planted alliums (onion, garlic, shallot) fall in the COOL/fall batch (Task 5) with their delta callouts, regardless of the classifier.
- **perennial_chill_gated (14):** apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate. **Task 6.** Judged against the `[300,700]` z9 chill band; apple carries the delta-2 variety steering.
- **perennial_evergreen (5):** grapefruit, lemon, lime, mandarin-clementine, orange-navel. **Task 7.** Colder than Phoenix -> mostly `survives`/`unsuitable`.
- **perennial_woody_ornamental (5):** lavender, oregano, rosemary, sage, thyme. **Task 8.** Desert-strong (arid heat, alkaline soil).
- **berries_woody (4):** blackberry, blueberry, elderberry, raspberry. **Task 8.** Marginal (blueberry very-marginal, alkaline soil; honesty in prose).
- **perennial_herbaceous (1):** strawberry. **Task 8.** Cool-window annual.

## File Structure

- `tools/staging/nevada_annuals_warm.json` -- warm-season frost_anchored cells (single spring + heat_pause, NO second_planting). `{slug: cell}`.
- `tools/staging/nevada_annuals_cool.json` -- cool-season + fall-planted-allium cells (spring + fall `second_planting`; onion/garlic/shallot deltas). `{slug: cell}`.
- `tools/staging/nevada_trees.json` -- 14 chill_gated trees (apple delta-2 steering).
- `tools/staging/nevada_citrus.json` -- 5 evergreen citrus (cold-limited).
- `tools/staging/nevada_perennials.json` -- 5 woody herbs + 4 berries + 1 strawberry.
- `tools/staging/nevada_chill_band.json` -- `region_chill_delivered.nevada` + provenance (top-level).
- `tools/staging/nevada_sources.json` -- the NEW `source_catalog` entries (`{source_id: entry}`), injected by `region_harness.scratch_canonical` and emitted as `add` patches by `build_region_promote`.
- `tools/region_cell_audit.py` -- MODIFY: add a `nevada` entry to `REGION_CONFIG`.
- `tools/build_region_promote.py` -- MODIFY: add `nevada` to `STAGING` + `EXPECTED_CELLS`.
- `tools/batches/nevada_region_promote.json` -- the atomic promote batch (generated).
- `docs/nevada_cell_contract.md` -- the per-archetype cell template (the column contract).
- `docs/reviews/notes/2026-07-21/nevada_sources.md` -- the T1 sourcing table.
- `docs/reviews/notes/2026-07-21/nevada_promote_dryrun.md` -- the scratch dry-run record.
- `docs/kickoffs/37-nevada-plant-app.md` -- the paired plant-app handoff (REGION_STATES + ZIP3 fence).

`region_harness.py` needs NO change (region_id + span params; patches `EXPECTED_SPANS` dynamically; already injects `staging/<region>_sources.json`). The `region_cell_audit.py` + `build_region_promote.py` edits are additive dict entries.

---

## Task 1: Lock the cell contract + roster

**Files:**
- Create: `docs/nevada_cell_contract.md`
- Read: `crops_data_final.json` (`bell-pepper` `mid_south` z8 [warm heat_pause+cold_pause shape], `cherry-tomato` `low_desert_az` [desert two-window + region voice], `lettuce-leaf` `low_desert_az` [cool two-window], `apple` `low_desert_az`+`warm_arid` [chill_basis steer + suitability], `orange-navel` `low_desert_az` [citrus], `garlic`/`onion` `low_desert_az`+`warm_arid` [fall-planted allium])

**Interfaces:**
- Produces: `docs/nevada_cell_contract.md` -- the authoritative per-archetype `nevada` cell template Tasks 4-8 author against.

- [ ] **Step 1: Extract the archetype templates from canonical**

```bash
python3 -c "
import json
d=json.load(open('crops_data_final.json'))
by={c['slug']:c for c in d['crops']}
for slug,reg in [('bell-pepper','mid_south'),('cherry-tomato','low_desert_az'),('lettuce-leaf','low_desert_az'),('apple','low_desert_az'),('apple','warm_arid'),('orange-navel','low_desert_az'),('garlic','low_desert_az'),('onion','low_desert_az')]:
    r=by[slug]['regions'].get(reg)
    if not r: print('=====',slug,reg,'MISSING'); continue
    print('=====',slug,reg,'=====')
    print('region keys:',list(r.keys()))
    z=sorted((r.get('resolved_by_zone') or {}).keys())[0]
    cell=r['resolved_by_zone'][z]
    print('cell keys @z'+z+':',list(cell.keys()))
    print('resolution_method:',cell.get('resolution_method'),'| calendar:',cell.get('calendar'))
    print('recommended_day_length_type:',cell.get('recommended_day_length_type'),'| suitability:',cell.get('suitability'))
"
```
Expected: confirms (a) the **warm single-cycle heat_pause+cold_pause** shape (`bell-pepper mid_south`: `[cold_pause, indoors, indoors, plant, plant, harvest, heat_pause, heat_pause, harvest, harvest, cold_pause, cold_pause]`, no `second_planting`); (b) the desert region voice + two-window cool shape; (c) the tree cell (`chill_basis_*`, `suitability`); (d) the citrus cell (`min_winter_temp_f`/`cold_basis_*`); (e) the fall-planted allium cell (`recommended_day_length_type`, fall `plant_out`).

- [ ] **Step 2: Write `docs/nevada_cell_contract.md`** (mirror `docs/mid_south_cell_contract.md` if present, else the mid-Atlantic one), with a full worked JSON example per archetype:

1. **Warm-season annual cell** (single spring cycle). Keys: `region_id="nevada"`, `region_label="Nevada: Mojave High Desert (Las Vegas Valley)"`, `zone_span=["8","9","10"]`, `sources`, `plantings[]` (ONE succession), `resolved_by_zone` (keys `"8"`,`"9"`,`"10"`), `region_notes_beginner`, `region_notes_seasoned`. Each `resolved_by_zone[z]`: authored windows (`start_indoors` early Feb, `plant_out` mid-Mar widened, `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`), a declared **`heat_pause`** (months Jun-Sep, SOURCED), NO `second_planting`, `calendar[]` DERIVED, `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost","first_frost"}` (per-zone dates), `sources`, `anchoring_urls`. The tail after `heat_pause`: heat-tolerant crops (pepper, eggplant, okra) may render a light fall harvest resume then `cold_pause`; tomato/melon/squash render `season_over` -> `cold_pause` (UNR: harvest before the heat, no promised fall flush). Author per the sources note; DERIVE + INSPECT (Task 4).
2. **Cool-season annual cell** (two-window). Spring (Feb-Apr) + fall (`second_planting` mid-Aug-Oct, built via `second_cycle.build_two_cycle_cell`), summer `heat_pause` between, `cold_pause` winter. A43 envelope rule applies. The fall-planted alliums (onion/garlic/shallot) are a sub-shape: a single FALL `plant_out` (no spring), `recommended_day_length_type` for onion/shallot, garlic's narrow Sep-Oct window (delta 3).
3. **Tree cell (chill-gated).** `suitability` per the `[300,700]` z9 band; `chill_basis_{seasoned,beginner}`, `bloom`, real `harvest`, perennial calendar vocabulary (`prune`/`bloom`/`growing`/`harvest`/`care`/`dormant`). **Apple = delta 2** (see Task 6 for the exact reliable/flagged variety lists).
4. **Citrus cell (cold-limited).** `suitability="survives"`/`"unsuitable"`, `min_winter_temp_f`, `cold_basis_{seasoned,beginner}`. Colder than Phoenix. A32-exempt; minimal calendar.
5. **Berry / woody-herb / strawberry cell.** Real calendars (A32 applies). Berries carry no suitability field -> marginality honesty lives in prose. Herbs desert-strong.

- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add docs/nevada_cell_contract.md
git status
git commit -m "docs(nevada): per-archetype cell contract for the Nevada high-desert region column"
git show --stat HEAD
```

---

## Task 2: Extend the region-generic tooling for `nevada`

**Files:**
- Modify: `tools/region_cell_audit.py` (add `nevada` to `REGION_CONFIG`)
- Modify: `tools/build_region_promote.py` (add `nevada` to `STAGING` + `EXPECTED_CELLS`)
- Test: `tools/test_region_cell_audit.py`, `tools/test_build_region_promote.py` (extend existing)

**Interfaces:**
- Consumes: the shipped region-generic tools.
- Produces: `REGION_CONFIG["nevada"]` (label, span `["8","9","10"]`, frost_model `"anchored"`); `STAGING["nevada"]` (the 5 cell files + band) + `EXPECTED_CELLS["nevada"] = 111`. `region_harness.gate_crop("nevada", ["8","9","10"], slug, cells)` works with no harness change.

- [ ] **Step 1: Write the failing test for the auditor config**

Append to `tools/test_region_cell_audit.py`:
```python
def test_nevada_config_present_anchored():
    import region_cell_audit as rca
    cfg = rca.REGION_CONFIG["nevada"]
    assert cfg["span"] == ["8", "9", "10"]
    assert cfg["frost_model"] == "anchored"
    assert cfg["label"] == "Nevada: Mojave High Desert (Las Vegas Valley)"

def test_nevada_heat_pause_plus_cold_pause_allowed():
    import region_cell_audit as rca
    cell = {
        "region_id": "nevada",
        "region_label": "Nevada: Mojave High Desert (Las Vegas Valley)",
        "zone_span": ["8", "9", "10"],
        "resolved_by_zone": {
            z: {"plant_out": "Mar 15 - May 1", "harvest": "May 20 - Jun 20",
                "harvest_start": "May 20", "harvest_end": "Jun 20",
                "first_plant_date": "Mar 15", "last_plant_date": "May 1",
                "resolution_method": "frost_anchored_resolved",
                "resolved_from": {"last_frost": "Feb 28", "first_frost": "Nov 25"},
                "calendar": ["cold_pause","indoors","plant","growing","harvest","harvest",
                             "heat_pause","heat_pause","heat_pause","season_over","cold_pause","cold_pause"]}
            for z in ("8", "9", "10")}}
    assert not any("cold_pause" in v or "heat_pause" in v
                   for v in rca.audit_cell("cherry-tomato", cell, "nevada"))
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k nevada -v`
Expected: FAIL with `KeyError: 'nevada'`.

- [ ] **Step 3: Add the `nevada` config entry** in `tools/region_cell_audit.py` `REGION_CONFIG` (after `mid_south`):
```python
    "nevada": {"label": "Nevada: Mojave High Desert (Las Vegas Valley)",
               "span": ["8", "9", "10"], "frost_model": "anchored"},
```

- [ ] **Step 4: Run auditor tests to verify they pass**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k nevada -v`
Expected: 2 passed.

- [ ] **Step 5: Write the failing test for the promote emitter**

Append to `tools/test_build_region_promote.py`:
```python
def test_nevada_registered():
    import build_region_promote as brp
    assert "nevada" in brp.STAGING
    assert brp.EXPECTED_CELLS["nevada"] == 111
    files, band = brp.STAGING["nevada"]
    assert band == "nevada_chill_band.json"
    assert set(files) == {
        "nevada_annuals_warm.json", "nevada_annuals_cool.json",
        "nevada_trees.json", "nevada_citrus.json", "nevada_perennials.json"}
```

- [ ] **Step 6: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k nevada -v`
Expected: FAIL (`KeyError` / assertion).

- [ ] **Step 7: Add the `nevada` STAGING + EXPECTED_CELLS entries** in `tools/build_region_promote.py`:
```python
    "nevada": (["nevada_annuals_warm.json", "nevada_annuals_cool.json",
                "nevada_trees.json", "nevada_citrus.json",
                "nevada_perennials.json"], "nevada_chill_band.json"),
```
and `EXPECTED_CELLS = {"pnw": 108, "mid_atlantic": 111, "mid_south": 111, "nevada": 111}`.

- [ ] **Step 8: Run test to verify it passes**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k nevada -v`
Expected: PASS.

- [ ] **Step 9: Regression guard -- confirm prior regions untouched**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py test_build_region_promote.py -v`
Expected: all pass (rgv/pnw/mid_atlantic/mid_south + nevada).

- [ ] **Step 10: Commit** (explicit pathspec)

```bash
git add tools/region_cell_audit.py tools/build_region_promote.py tools/test_region_cell_audit.py tools/test_build_region_promote.py
git status
git commit -m "feat(nevada): register region in cell-auditor + promote-emitter (z8-9-10, anchored, 111 cells)"
git show --stat HEAD
```

---

## Task 3: T1 sourcing pass + new source_catalog + chill band + frost anchors

**Files:**
- Create: `docs/reviews/notes/2026-07-21/nevada_sources.md`
- Create: `tools/staging/nevada_sources.json`
- Create: `tools/staging/nevada_chill_band.json`

**Interfaces:**
- Produces: the sourcing table (crop/class -> source id + url + spring/fall windows + frost dates); `tools/staging/nevada_sources.json` (new `source_catalog` entries); `region_chill_delivered.nevada` band + provenance (drives A3 in Task 6).

- [ ] **Step 1: Fetch + record the T1 sources.** Use WebFetch + `pypdf` in THIS controller env (subagent sandboxes block PDF tooling; PDFs must be rendered/extracted here). The authorities (from the ruling `docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md`):
  - **NWS WR-235** "Climate of Las Vegas" (`https://www.weather.gov/media/wrh/online_publications/TMs/TM-235.pdf`) -- frost anchors z9 Feb 28 / Nov 25.
  - **UNR SP-99-11** "Growing Tomatoes in Southern Nevada" (`https://extension.unr.edu/publication.aspx?PubID=3267`) -- mid-March last frost, >90degF/<55degF fruit-set cutoff, NO fall planting, early+main variety mix.
  - **UNR/UNCE FS-02-61** "Home Vegetable Production in Southern Nevada" (`https://naes.agnt.unr.edu/PMS/Pubs/2002-3280.pdf`) -- warm-season March-May, 90degF ceiling, cool-season Feb-Apr / mid-Aug-Oct.
  - **UNLV/UNR Master Gardener** "Vegetable Planting Guide for Southern Nevada" (`https://www.unlv.edu/sites/default/files/page_files/27/CampusLife_Planting-Calendar-LasVegas.pdf`) -- warm/cool windows + garlic Sept-mid-Oct (delta 3). Render to image if the font will not extract.
  - **UNR SP-20-07** orchard trial (`https://naes.agnt.unr.edu/PMS/Pubs/2020-3713.pdf`) -- apple variety/chill evidence (delta 2). Render pages to image.
  - **z8 / z10 frost normals** -- targeted hunt for a Mesquite/Pahrump (z8) or Laughlin (z10) station normal; if none is T1-fetchable, DERIVE off z9 by the standard zone gradient (z8 last ~Mar 15-20 / first ~Nov 5-10; z10 last ~Feb 12-18 / first ~Dec 3-8) and flag as gradient-derived in the provenance. Do not interpolate silently.
  - **chill** -- the trial (Granny Smith 700hr confirmed ceiling) anchors z9; z8/z10 elevation-gradient derived.

- [ ] **Step 2: Write `tools/staging/nevada_sources.json`** -- the NEW `source_catalog` entries (ids NOT already in `source_catalog`; the emitter asserts no collision). Match the existing `source_catalog` entry shape (inspect one first: `python3 -c "import json;d=json.load(open('crops_data_final.json'));print(json.dumps(d['source_catalog']['unr_ext'],ensure_ascii=False,indent=1))"`). Candidate ids:
  ```json
  {
    "nws_vef": {"name": "NWS Las Vegas, Technical Memorandum WR-235 (Climate of Las Vegas)", "tier": 1, "url": "https://www.weather.gov/media/wrh/online_publications/TMs/TM-235.pdf", "kind": "nws", "verified": "2026-07-21"},
    "unlv_mg_svn": {"name": "UNLV / UNR Coop Ext Master Gardener, Vegetable Planting Guide for Southern Nevada", "tier": 1, "url": "https://www.unlv.edu/sites/default/files/page_files/27/CampusLife_Planting-Calendar-LasVegas.pdf", "kind": "extension_master_gardener", "verified": "2026-07-21"},
    "unr_sp2007": {"name": "UNR Extension SP-20-07, Research Orchard Fruit Evaluations for Southern Nevada (2020)", "tier": 1, "url": "https://naes.agnt.unr.edu/PMS/Pubs/2020-3713.pdf", "kind": "extension", "verified": "2026-07-21"}
  }
  ```
  For UNR SP-99-11 / FS-02-61: FIRST check whether the catalogued `unr_ext` entry is portal-level (covers the UNR Extension family) or per-pub. If portal-level, cite `unr_ext` for them (no new id). If per-pub granularity is the catalog norm, add `unr_sp9911` + `unr_fs0261`. Match the observed convention exactly (align the field keys -- `name`/`tier`/`url`/`kind`/`verified` -- to a real neighbor entry; the shape above is a template, not assumed).

- [ ] **Step 3: Write the sourcing table** `docs/reviews/notes/2026-07-21/nevada_sources.md` -- a table `crop_or_class | source_id | url | spring_window | fall_window | frost_dates | tier | notes`. Top block: the z8/z9/z10 frost normals (marking z8/z10 as gradient-derived if so). A column marks which annuals are WARM (single spring, no fall) vs COOL (spring + fall). The garlic + onion delta rows are called out. Any thin-source crop is flagged for a conservative cell.

- [ ] **Step 4: Author the chill band** `tools/staging/nevada_chill_band.json`:
```json
{
  "region_chill_delivered.nevada": {"8": [500, 900], "9": [300, 700], "10": [150, 450]},
  "region_chill_delivered_provenance.nevada": "z9 trial-anchored: UNR Extension SP-20-07 North Las Vegas Research Orchard confirms apple performance up to Granny Smith (700 chill hours, Notable Mention), the confirmed ceiling; verified 2026-07-21. z8 (cooler, higher pockets) and z10 (Laughlin, warm edge) are elevation-gradient derived off the z9 trial anchor."
}
```
Verify against `chill_gate.py`'s expected shape (`region -> {zone -> [lo,hi]}`, numeric, lo<=hi). Confirm the exact top-level path form matches the shipped `mid_south_chill_band.json` (`region_chill_delivered.<region>` + `region_chill_delivered_provenance.<region>`).

- [ ] **Step 5: Commit** (explicit pathspec)

```bash
git add docs/reviews/notes/2026-07-21/nevada_sources.md tools/staging/nevada_sources.json tools/staging/nevada_chill_band.json
git status
git commit -m "docs(nevada): T1 sourcing table (UNR/UNLV/NWS) + new source_catalog entries + chill band"
git show --stat HEAD
```

---

## Task 4: Author the warm-season annual cells (single spring + heat_pause, NO second_planting)

**Files:**
- Create: `tools/staging/nevada_annuals_warm.json` (`{slug: cell}`)

**Interfaces:**
- Consumes: `docs/nevada_cell_contract.md`, `docs/reviews/notes/2026-07-21/nevada_sources.md`, `region_harness.gate_crop`, `region_cell_audit`, `annual_calendar.derive_annual_calendar`.
- Produces: `tools/staging/nevada_annuals_warm.json`.

Subagent-parallelizable: one worker per crop (or per family), writing into the shared staging dict (controller-merged; no per-subagent commits). **Per-crop procedure:**

- [ ] **Step 1: Author the cell for warm crop `<slug>`.** Read the crop's `bell-pepper mid_south z8` analog (the single-cycle heat_pause+cold_pause shape) and its `low_desert_az` cell (desert region voice + which months are the real heat abort). Author the `nevada` cell:
  - `region_id="nevada"`, `region_label="Nevada: Mojave High Desert (Las Vegas Valley)"`, `zone_span=["8","9","10"]`.
  - `resolved_by_zone` keys `"8"`,`"9"`,`"10"`; per-zone `resolved_from` frost dates from the sources note; `resolution_method="frost_anchored_resolved"`.
  - **`start_indoors` in early February** (6 weeks before UNR's mid-March transplant) so January stays `cold_pause`. `plant_out` widened (mid-Mar through ~early/mid-May per UNR; the late-May succession tail belongs in `region_notes`, not stretched into the calendar to collide with the Jun heat_pause).
  - A declared **`heat_pause`** on the Jun-Sep months (SOURCED to UNR's >90degF cutoff). NO `second_planting`.
  - Dual-register `region_notes_{beginner,seasoned}` in house voice (no em dashes): spring window, the summer heat abort, and the honest "no fall replant recommended here" (the UNR delta from Phoenix).
  - Cite `unlv_mg_svn` / `unr_sp2007`-family / the FS/SP UNR ids in `sources` + `anchoring_urls` (verified 2026-07-21).

- [ ] **Step 2: Derive + INSPECT the `calendar[]`** (per zone):
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell=json.load(open('tools/staging/nevada_annuals_warm.json'))['<slug>']['resolved_by_zone']['9']
print(derive_annual_calendar(cell))
"
```
Set each zone's `calendar[]` to the derived array. **Assert the honest tail:** `cold_pause` Jan, spring `plant`/`growing`/`harvest`, `heat_pause` at the Jun-Sep months, then EITHER a light fall `harvest` resume (heat-tolerant crops) OR `season_over` (tomato/melon/squash), then `cold_pause` Nov-Dec. **There must be NO phantom fall `plant`/`growing` implying a fall crop, and Nov-Dec MUST be `cold_pause`** (if it is not, January is active -- move `start_indoors` fully into Feb and re-derive). If the deriver will not produce the honest tail, hand-author the tail tokens and confirm `calendar_coherence` accepts them (Step 3).

- [ ] **Step 3: Gate + audit the crop.** Run `python3 tools/region_harness.py nevada 8,9,10 tools/staging/nevada_annuals_warm.json <slug>` -> PASS (A45 3-zone parity, A31/A32, calendar coherence, 0 em dashes, T1 sources). Run `python3 tools/region_cell_audit.py nevada tools/staging/nevada_annuals_warm.json` -> 0 issues. Fix + re-gate until clean. Common failures: `cold_pause` suppressed (Jan-active -> shift indoor start to Feb), unsourced `heat_pause`, span/key mismatch (must be exactly 8/9/10), `resolved_from` null, em dash, an `in-ground-month`-tokened `season_over`.

- [ ] **Step 4: Commit the batch** (after all warm crops pass; explicit pathspec)

```bash
git add tools/staging/nevada_annuals_warm.json
git status
git commit -m "feat(nevada): author warm-season annual cells (single spring + heat_pause, no fall replant per UNR)"
git show --stat HEAD
```

---

## Task 5: Author the cool-season + fall-planted-allium annual cells (two-window)

**Files:**
- Create: `tools/staging/nevada_annuals_cool.json` (`{slug: cell}`)

**Interfaces:**
- Consumes: `docs/nevada_cell_contract.md`, the sources note, `region_harness.gate_crop`, `region_cell_audit`, `second_cycle.build_two_cycle_cell`, `photoperiod_gate`.
- Produces: `tools/staging/nevada_annuals_cool.json`.

Cool crops run the desert two-window (spring Feb-Apr + fall mid-Aug-Oct), which KEEPS the `second_planting` fall cycle (the desert delta from the warm crops). Subagent-parallelizable. **Per-crop procedure:**

- [ ] **Step 1: Author the two-window cool cell for `<slug>`** with `second_cycle.build_two_cycle_cell(base, spring, fall)`:
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from second_cycle import build_two_cycle_cell
# base = the region-constant cell skeleton (region_id/label/span/sources/plantings);
# spring/fall = the authored window dicts (Feb-Apr spring, mid-Aug-Oct fall) per the sources note.
# See second_cycle.py docstring for the exact spring/fall dict shape; build a per-zone cell,
# heat_pause on the summer months between the two windows.
"
```
Author `resolved_by_zone` for `"8"`,`"9"`,`"10"`; `resolution_method="frost_anchored_resolved"`; per-zone `resolved_from`; a summer `heat_pause`; the fall `second_planting` (A43 single-span + envelope-inside). Dual-register `region_notes_*` (no em dashes).

- [ ] **Step 2: The fall-planted alliums (onion, garlic, shallot) -- the deltas.**
  - **onion / shallot:** a single FALL `plant_out` (Oct-Nov, sets/transplants), NO spring plant, harvest late spring. Set `recommended_day_length_type` to `short_day` or `intermediate_day` (desert latitude ~36degN -- source it; low_desert_az/warm_arid onion are the analogs). Because it is fall-planted, there is no April-or-later `plant_out` -> A9 window-fit is satisfied by construction. Shallot cell says "follows onion" (species identity), matching the mid_south/mid_atlantic idiom.
  - **garlic (delta 3):** a single FALL clove `plant_out` window **Sep 1 - Oct 15** (UNLV/UNR Master Gardener), NARROWER than `warm_arid` ("late Sep-Nov") / `low_desert_az` ("mid-Sep-Nov") -- do NOT inherit either verbatim. Harvest the following early summer.

- [ ] **Step 3: Derive/confirm `calendar[]`, gate + audit.** Run `python3 tools/region_harness.py nevada 8,9,10 tools/staging/nevada_annuals_cool.json <slug>` -> PASS. Run `python3 tools/region_cell_audit.py nevada tools/staging/nevada_annuals_cool.json` -> 0. **Onion/shallot: explicitly run A9** -- `python3 tools/photoperiod_gate.py` (or the harness path that invokes it) and confirm `nevada` onion/shallot = 0 violations (no forbidden spring `plant_out`).

- [ ] **Step 4: RED-check A9 once** (adversarial, per Global Constraints): on a scratch copy of the onion cell, flip `nevada` `recommended_day_length_type` to `long_day` AND move `plant_out` to April; run the harness and confirm A9 bounces it; discard. Record in the dry-run note (Task 10).

- [ ] **Step 5: Commit the batch** (after all cool + allium crops pass; explicit pathspec)

```bash
git add tools/staging/nevada_annuals_cool.json
git status
git commit -m "feat(nevada): author cool-season + fall-allium annual cells (two-window; garlic + onion deltas)"
git show --stat HEAD
```

---

## Task 6: Author the 14 chill_gated tree cells (apple delta-2 steering)

**Files:**
- Create: `tools/staging/nevada_trees.json`

**Interfaces:**
- Consumes: `docs/nevada_cell_contract.md` (tree template), the sources note, `tools/staging/nevada_chill_band.json`, `region_harness.gate_crop`.
- Produces: `tools/staging/nevada_trees.json`.

Judge each tree against the `[300,700]` z9 band (and z8 `[500,900]` / z10 `[150,450]`).

- [ ] **Step 1: Author each tree cell.** Read the crop's `warm_arid`/`low_desert_az` tree cell for the desert fruiting-cell shape.
  - **apple = DELTA 2 (Trevor-confirmed Option A):** `suitability="fruits_reliably"`. `chill_basis_seasoned`/`chill_basis_beginner` NAME the trial-confirmed reliable picks -- **Dorsett Golden, Anna, Pink Lady, Mutsu, Fuji, Granny Smith** (UNR SP-20-07), plus the safely low-chill **Ein Shemer, Dolgo, Gala** (under the confirmed ceiling) -- and explicitly FLAG the high-chill tier as unproven for the Las Vegas Valley: **Zestar!, McIntosh, Empire, Honeycrisp, Golden Delicious, Jonagold, plus Liberty** (trial "under review"). Cite `unr_sp2007`. No em dashes.
  - **other 13 trees:** `suitability` from the band vs the crop's `chill_hours_required` (low/mid-chill pome + stone that clear ~300-700 hr = `fruits_reliably`; genuinely high-chill trees or those needing >700hr = `marginal`, flagged in `chill_basis_*`). peach/apricot/nectarine: re-judge from the ARID reality (the mid-South humid brown-rot / fruit-crack rationale does NOT carry here; likely `fruits_reliably` on chill, watch late frost -- source per crop). pomegranate/fig/persimmon/mulberry desert-strong. pawpaw is a humid-forest understory tree -> honest `marginal`/`unsuitable` in the dry Mojave (opposite of its mid-South native status; source it).
  - Real `bloom` + `harvest`; perennial calendar vocabulary; region-level `plantings_provenance`.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py nevada 8,9,10 tools/staging/nevada_trees.json <slug>` -> PASS; confirm A3 (`perennial_gate`) coheres (`fruits_reliably` requires a calendar + the band clears the requirement; `marginal`/`survives_no_fruit` where it does not). `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/nevada_trees.json
git status
git commit -m "feat(nevada): author 14 chill_gated tree cells (apple Option A variety steering)"
git show --stat HEAD
```

---

## Task 7: Author the 5 citrus cells (cold-limited)

**Files:**
- Create: `tools/staging/nevada_citrus.json`

**Interfaces:**
- Consumes: `docs/nevada_cell_contract.md` (citrus template), `region_harness.gate_crop`.
- Produces: `tools/staging/nevada_citrus.json`.

- [ ] **Step 1: Author each citrus cell** (grapefruit, lemon, lime, mandarin-clementine, orange-navel). Las Vegas is COLDER than Phoenix (the SP-20-07 evidence: colder winter nights), so citrus is MORE cold-limited than `low_desert_az`: mostly `suitability="survives"` (protected/container culture where real, sourced) or `"unsuitable"`; the hardier mandarin/kumquat least bad, lime/grapefruit worst. `min_winter_temp_f`; `cold_basis_{seasoned,beginner}` explaining the limit honestly (no em dashes). Re-judged fresh, not cloned from Phoenix's warmer verdict. A32-exempt; minimal calendar.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py nevada 8,9,10 tools/staging/nevada_citrus.json <slug>` -> PASS; A3 coheres (no `fruits_reliably`). `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/nevada_citrus.json
git status
git commit -m "feat(nevada): author 5 citrus cells (cold-limited, colder than Phoenix)"
git show --stat HEAD
```

---

## Task 8: Author the 10 remaining perennials (woody herbs + berries + strawberry)

**Files:**
- Create: `tools/staging/nevada_perennials.json`

**Interfaces:**
- Consumes: `docs/nevada_cell_contract.md`, the sources note, `region_harness.gate_crop`.
- Produces: `tools/staging/nevada_perennials.json`.

All are frost-anchored calendar cells (A32 applies -- real calendars required).

- [ ] **Step 1: Author each cell.**
  - **Woody herbs (lavender, oregano, rosemary, sage, thyme):** desert-STRONG (arid heat + alkaline soil is their preference; the `warm_arid`/`low_desert_az` thriving framing, not the humid-belt struggle). Real frost-anchored calendars; summer is the growing season. `grown_as` where a herb needs winter protection at the z8 edge (as `northern_tier` does for thyme).
  - **Berries (blackberry, blueberry, elderberry, raspberry):** MARGINAL honesty in prose (berries carry no suitability field; A32 still forces a calendar). Blackberry/raspberry marginal (heat + alkaline soil; fall-bearing/low-chill cultivar steer where sourced). **Blueberry very-marginal** (needs acidic soil, hostile in the alkaline Mojave -> container-only honesty, sourced). Elderberry marginal.
  - **Strawberry:** a cool-window annual in the desert (fall-set / winter-spring harvest per UNR), `grown_as` where relevant.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py nevada 8,9,10 tools/staging/nevada_perennials.json <slug>` -> PASS. `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/nevada_perennials.json
git status
git commit -m "feat(nevada): author 10 perennial cells (desert herbs + marginal berries + strawberry)"
git show --stat HEAD
```

---

## Task 9: Build the atomic promote batch

**Files:**
- Create: `tools/batches/nevada_region_promote.json` (generated)

**Interfaces:**
- Consumes: the five `tools/staging/nevada_*.json` cell files + `nevada_chill_band.json` + `nevada_sources.json`; the Task 2 `STAGING`/`EXPECTED_CELLS` entries.
- Produces: `tools/batches/nevada_region_promote.json` -- an `apply_patch` batch adding, per crop, `$.crops[?(@.slug=='<slug>')].regions.nevada` (op `add`), plus top-level `region_chill_delivered.nevada` + provenance + the new `$.source_catalog.<id>` adds. `EXPECTED_SPANS.nevada` is a CODE edit to `tools/zone_span_gate.py` (Task 11 Step 1), applied in the same commit as the batch, NOT part of the JSON batch.

- [ ] **Step 1: Generate the batch**

Run: `python3 tools/build_region_promote.py nevada`
Expected stdout: `emitted <N> patches (111 nevada cells + 2 top-level + <n_src> source_catalog); base_sha a071f0c1...`. The emitter asserts `len(seen) == 111` (from `EXPECTED_CELLS`), so a miscount aborts here; it also asserts no `source_catalog` id collision.

- [ ] **Step 2: Verify the generated batch**

```bash
python3 -c "
import json
b=json.load(open('tools/batches/nevada_region_promote.json'))
ops=b['patches']
cells=[o for o in ops if o['json_path'].endswith('.regions.nevada')]
srcs=[o for o in ops if o['json_path'].startswith('\$.source_catalog.')]
assert len(cells)==111, len(cells)
assert all(o['op']=='add' for o in ops), 'nevada is net-new everywhere'
assert any('region_chill_delivered.nevada' in o['json_path'] for o in ops)
print('batch OK:', len(ops), 'ops,', len(cells), 'cells,', len(srcs), 'source adds, base_sha', b['base_sha'][:12])
"
```
Expected: `batch OK: <N> ops, 111 cells, <n_src> source adds, base_sha a071f0c17201`.

- [ ] **Step 3: Commit** (batch only; canonical still untouched; explicit pathspec)

```bash
git add tools/batches/nevada_region_promote.json
git status
git commit -m "feat(nevada): deterministic atomic-promote batch (111 cells + chill band + source adds)"
git show --stat HEAD
```

---

## Task 10: Dry-run the promote on a scratch copy (full gate ceremony, RED-checked)

**Files:**
- Modify (scratch only): a copy of `crops_data_final.json` + `tools/zone_span_gate.py`
- Create: `docs/reviews/notes/2026-07-21/nevada_promote_dryrun.md`

**Interfaces:**
- Consumes: `tools/batches/nevada_region_promote.json`, `region_harness.build_scratch_tools`, `region_harness.scratch_canonical`, `region_cell_audit`.
- Produces: proof that the full suite is green post-promote before touching the real canonical.

- [ ] **Step 1: Apply the batch to a scratch canonical.** Compute `sha256_before` from the real file, apply via `tools/apply_patch.py` to a COPY, confirm COMPACT + count 128 + footprint = exactly 111 `regions.nevada` cells + the top-level `region_chill_delivered.nevada` + provenance + the `source_catalog` adds, via a byte-diff audit (NO other crop/key touched, all 128 else byte-identical).

- [ ] **Step 2: Build scratch tools + run the full suite** against the scratch canonical:
  - `region_harness.build_scratch_tools(dest, "nevada", ["8","9","10"])` (patches `EXPECTED_SPANS`).
  - `gate_all.py` -> 119/119.
  - `zone_span_gate.py` (A45) -> 0 (3-zone parity on 8/9/10).
  - `coverage_floor_gate.py` (A31/A32) -> 0 (all 111 carry `nevada`).
  - `chill_gate.py` -> 0.
  - `second_planting_gate.py` (A43) -> 0 across the cool-crop fall cycles.
  - `photoperiod_gate.py` (A9) -> 0 for onion/shallot `nevada`.
  - `whole_crop_gate.py` on a per-class sample (cherry-tomato, lettuce-leaf, garlic, onion, apple, orange-navel, lavender, blueberry, strawberry) -> PASS.
  - `region_cell_audit.py nevada` over all five staging files -> 0.
  - `calendar_coherence` + `timing_spine` -> 0.
  - `prose_window_sweep.py` -> 0 (prose windows match the resolved windows; catches stale Phoenix/warm_arid residue in cloned prose).
  - `release_verify.py` -> clean modulo the documented roster-wide section-A collateral (the pre-commit backstop is the binding multi-crop gate).

- [ ] **Step 3: RED-check the promote** on the scratch copy (restore after each): (a) drop the `"8"` key from one crop's `nevada` cell -> A45 bounces it; (b) widen a cool-crop `second_planting` envelope past the first harvest span -> A43 bounces it; (c) flip onion `nevada` to `long_day` + April `plant_out` -> A9 bounces it. Proves the ceremony catches the 3-zone-parity + fall-envelope + photoperiod defect classes at roster scale.

- [ ] **Step 4: Record + commit** the dry-run result in `docs/reviews/notes/2026-07-21/nevada_promote_dryrun.md` (gate outputs + footprint audit + the three RED-check results). (explicit pathspec)

```bash
git add docs/reviews/notes/2026-07-21/nevada_promote_dryrun.md
git status
git commit -m "test(nevada): scratch-copy promote dry-run green + A45/A43/A9 RED-check"
git show --stat HEAD
```

---

## Task 11: Promote to canonical + release ceremony (THE one canonical write)

**Files:**
- Modify: `crops_data_final.json` (the atomic promote)
- Modify: `tools/zone_span_gate.py` (add `nevada` to `EXPECTED_SPANS`)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`
- Modify: `docs/region_coverage_roadmap.md`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 0: CONCURRENCY COORDINATION.** Before touching the canonical:
  - `git fetch` + `git log --oneline origin/main..main` + `git log -1 crops_data_final.json`.
  - Re-read the LIVE SHA: `shasum -a 256 crops_data_final.json`. If it is no longer `a071f0c1`, a concurrent promote landed. If path-disjoint from `*.regions.nevada` + the added `source_catalog` ids, that is FINE, but you MUST: (a) re-run the roster query -> still 111; (b) re-run each staging file through `region_harness` against the live canonical -> all green; (c) confirm none of `nevada_sources.json`'s ids now collide; (d) regenerate the batch with the LIVE SHA (`build_region_promote.py nevada` re-stamps `base_sha` from the live file, or `--base-sha <LIVE>`).
  - Do NOT hold the canonical open concurrently with another session (the sweet-corn collision rule).

- [ ] **Step 1: Add `nevada` to the REAL `tools/zone_span_gate.py` `EXPECTED_SPANS`** (`"nevada": ["8","9","10"]`). No `DONORS` entry (authored fresh, not zone-cloned). `coverage_floor_gate` auto-derives its `CANONICAL_REGIONS`/`CANONICAL_ZONES` from `EXPECTED_SPANS`.

- [ ] **Step 2: Apply the batch to the REAL canonical** via `tools/apply_patch.py` with the LIVE `sha256_before` (Step 0). Confirm COMPACT, no trailing newline, count 128.

- [ ] **Step 3: Full release verification** (protocol #6):
  - `python3 tools/whole_crop_gate.py <slug>` on the 18 gold anchors -> 18/18 PASS.
  - `python3 tools/gate_all.py` -> 119/119.
  - `python3 tools/zone_span_gate.py` (A45), `coverage_floor_gate.py` (A31/A32), `chill_gate.py`, `second_planting_gate.py` (A43), `photoperiod_gate.py` (A9) -> 0.
  - `python3 tools/prose_window_sweep.py` -> 0.
  - `python3 tools/release_verify.py` -> clean (modulo documented roster-wide section-A collateral).
  - `python3 tools/region_cell_audit.py nevada tools/staging/nevada_*.json` -> 0.
  - Independent footprint audit: exactly 111 `regions.nevada` + `region_chill_delivered.nevada` + provenance + the `source_catalog` adds changed; all else byte-identical; count 128.
  - The **pre-commit backstop** (`precommit_release_verify.py`) runs on commit -- checks ALL changed crops.
  - Per-batch source-truth sample: re-verify 3-4 authored windows (incl. a garlic Sep-Oct window, an apple variety line, and a cool-crop fall window) against their cited UNR/UNLV/NWS URLs.

- [ ] **Step 4: State trio** -- surgically update CURRENT_STATE.md (drift memory: hand-maintain, no `---`), prepend STATE_HISTORY.md (most-recent-first), bump LATEST.txt (new SHA + session line).

- [ ] **Step 5: Roadmap + register** -- mark roadmap item 10 SHIPPED (new canonical SHA + commit); add a `docs/field_addition_register.md` row (next number, ~#21) for the Nevada region column.

- [ ] **Step 6: Independent content review** (before commit or as the final gate): dispatch a fresh opus content-review subagent over a per-class sample of the authored `nevada` cells for factual/honesty/direction/date-consistency + em-dash + the delta fidelity (apple flag-list exact; garlic window narrow; no fabricated UNR windows; warm-crop no-fall honesty). Apply SHIP-WITH-FIXES corrections. (This mirrors the mid-South arc's review that caught fabricated-window prose.)

- [ ] **Step 7: Commit** (UNPUSHED -- Trevor confirms push; explicit pathspec)

```bash
git add crops_data_final.json tools/zone_span_gate.py CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/region_coverage_roadmap.md docs/field_addition_register.md
git status
git commit -m "feat(nevada): certify the Nevada high-desert region across 111 crops (roadmap item 10)"
git show --stat HEAD
```

---

## Task 12: Write the paired plant-app kickoff

**Files:**
- Create: `docs/kickoffs/37-nevada-plant-app.md` (confirm the next free kickoff number at build; #36 is the onion-daylength note)

**Interfaces:**
- Produces: the handoff so plant-app can route the belt's ZIPs to `nevada`.

- [ ] **Step 1: Write the kickoff** covering:
  - `REGION_STATES.nevada = ['NV']`.
  - `regions.json` row + `SHORT_REGION_LABEL.nevada`.
  - **A ZIP3 fence IS needed** (unlike mid-Atlantic/mid-South): NV spans Reno/Carson/Elko z6-7 (northern, `northern_tier`) as well as the southern Mojave. Fence `nevada` to the southern Clark County ZIP3s (**889 North Las Vegas, 890/891 Las Vegas/Henderson**, incl. Laughlin 89029); northern-NV ZIP3s (895 Reno, 897 Carson City, 898 Elko, 893 Ely) must NOT resolve to the Mojave calendar. The mirror of RGV's 785xx and PNW's west-side fences. Confirm the exact NV ZIP3 list against `zip-zones.json` at write time.
  - **The z8 tail depends on the temperate-region resolution fix (kickoff #32, the `isWarm` decoupling)** -- cross-reference it; z9/z10 (warm) resolve on the standard path, the z8 pockets need #32.
  - Note: dataset side is `<new canonical SHA>`; plant-astro consumes spans + chill band + tree calendars automatically.

- [ ] **Step 2: Commit** (explicit pathspec)

```bash
git add docs/kickoffs/37-nevada-plant-app.md
git status
git commit -m "docs(kickoff): plant-app Nevada REGION_STATES + southern-NV ZIP3 fence handoff (#37)"
git show --stat HEAD
```

---

## Task 13: Update memory + close out

- [ ] **Step 1:** Write/update memory `nevada-high-desert-region-spec` -> SHIPPED (canonical SHA, commit, 111 cells; reusable lessons: **the desert heat_pause+cold_pause warm-crop shape already lived in 289 cells -- no novel mechanism**; warm crops drop `second_planting` while cool crops keep it (inverse of the humid belts); apple prose-only variety steering off a field trial; garlic narrow window; the 3-zone span reused `se_gulf`'s A45 shape; new sources registered in-batch like mid-South; a ZIP3 fence IS needed here (northern NV is a different climate); whether the z8/z10 gradient frost derivation held up in review). Add the MEMORY.md pointer. Cross-link `[[mid-south-region-spec]]`, `[[onion-daylength-intermediate-a9-window-fit]]`, `[[fall-cycle-deriver-combine-then-split]]`.
- [ ] **Step 2:** Summarize to Trevor: what shipped, the unpushed commit, the plant-app kickoff (#37 + the ZIP3 fence + the #32 dependency for z8), and that no plant-astro bump was done. Flag that item 11 (Utah "Dixie") is the last z8 belt and shares Nevada's heat/frost-return + apple-marginal gap shape -- this arc is largely its template (though Utah apple leans `marginal`, not `fruits_reliably`).

---

## Self-Review

**Spec coverage:**
- Product goal (Nevada honest calendars; the actively-misleading flat back half fixed) -> Tasks 4-11. ✓
- Roster-wide 111 cells -> Tasks 4-8 enumerate all 111 (warm+cool = 82, 14 trees, 5 citrus, 10 perennials). ✓
- zone_span ["8","9","10"], A45 3-zone (spec §2) -> Global Constraints + Tasks 2, 9-11 (se_gulf shape). ✓
- Frost-anchored, standard deriver, no new field/gate (spec §2, §6) -> Global Constraints + Task 4/5 (existing heat_pause/second_planting machinery). ✓
- Delta 1 warm=single-spring+heat_pause+no-fall / cool=two-window (spec §3.1) -> Tasks 4 + 5. ✓
- Delta 2 apple Option A + flag list + Liberty + [300,700] band (spec §3.2) -> Task 3 (band) + Task 6 (prose). ✓
- Delta 3 garlic Sep-Oct narrow window (spec §3.3) -> Task 5 Step 2. ✓
- Onion A9 watch (spec §5) -> Task 5 Steps 2-4 + Task 10 RED-check. ✓
- Frost anchors z9 Feb 28/Nov 25 + z8/z10 gradient (spec §4) -> Task 3 Step 1. ✓
- Chill table nevada {8/9/10} (spec §3.2) -> Task 3 Step 4. ✓
- Class split trees/citrus/herbs/berries (spec §5) -> Tasks 6, 7, 8 (apple fruits_reliably, citrus cold-limited colder-than-Phoenix, pawpaw re-judged marginal, blueberry container-only). ✓
- New in-batch source_catalog (spec §7) -> Task 3 Step 2 + Task 9. ✓
- Gate ceremony incl A9/A45/chill/calendar_coherence/prose_window_sweep/footprint (spec §6) -> Tasks 10-11. ✓
- State trio + roadmap + register + content review + memory (spec §8) -> Task 11 (Steps 4-6) + Task 13. ✓
- App handoff + ZIP3 fence (spec §8) -> Task 12. ✓
- Out of scope: no new field/gate/archetype, no plant-astro bump, shallot-variety tensions (spec §9) -> honored. ✓

**Placeholder scan:** authored window VALUES come from Task 3 (sourcing) and are consumed by Tasks 4-8 against the Task 1 template -- the data-authoring analog of "author per spec," not a placeholder; the STRUCTURE, gate loop, deriver commands, and the three deltas' exact content (variety lists, garlic window, band numbers, frost anchors) are concrete. `<slug>`, `<N>`, `<n_src>`, `<new canonical SHA>` are per-item substitutions. The `nevada_sources.json` id shape is marked "align to a real neighbor entry" (Task 3 Step 2), not assumed.

**Type consistency:** `region_harness.gate_crop(region_id, span, slug, staged_cells)` and its CLI `region_harness.py <rid> <span-comma> <staging.json> <slug>` used consistently (Tasks 4-8, 10-11); `region_cell_audit.audit_cell(slug, cell, region_id) -> list` (Tasks 2, 4-8) + CLI `region_cell_audit.py <rid> <staging...>`; `second_cycle.build_two_cycle_cell(base, spring, fall)` (Task 5); `build_region_promote.py nevada [--base-sha SHA]` reads `STAGING["nevada"]` (5 files + band) + `staging/nevada_sources.json`; `EXPECTED_CELLS["nevada"] == 111`; `annual_calendar.derive_annual_calendar(cell)` (Task 4); staging files are `{slug: cell}` throughout; chill band path `region_chill_delivered.nevada` + provenance (Task 3, matches shipped mid_south). ✓

**Open confirm-items flagged, not hidden:** the `source_catalog` entry field shape (Task 3 Step 2 -- align to a real neighbor), whether UNR pubs ride `unr_ext` or need per-pub ids (Task 3 Step 2), the z8/z10 frost normals (targeted source hunt, else gradient-derived + flagged, Task 3 Step 1), the warm-crop fall tail token per crop (harvest-resume vs season_over, Task 4 Step 2 derive+inspect), the exact NV ZIP3 fence list (Task 12, confirm against zip-zones.json), and the concurrent-promote ordering (Task 11 Step 0) are marked "confirm against the real tool / live state / source," not assumed.
```
