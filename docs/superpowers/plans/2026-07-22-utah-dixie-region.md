# Utah "Dixie" High-Desert Region Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author and certify a real Utah "Dixie" high-desert region (`utah_dixie`, St. George / Washington County, z8) across all 111 certified region-carrying crops, so the 15-ZIP SW-Utah belt stops riding generic zone dates that assume neither its real summer heat abort nor its real late-fall frost return.

**Architecture:** Utah Dixie is FROST-ANCHORED (`resolution_method="frost_anchored_resolved"`, real `resolved_from` frost dates, `cold_pause` winter), the same model as Nevada / mid-Atlantic / mid-South / PNW, so `calendar[]` is DERIVED by the standard `tools/annual_calendar.py` -- NO deriver change, NO new field, NO new gate. This is **the Nevada arc's near-twin** (`docs/superpowers/plans/2026-07-21-nevada-high-desert-region.md` is the direct template), with three confirmed Utah deltas and one big simplification: **a SINGLE zone (`["8"]`), not Nevada's 3** -- so A45 is single-zone parity (the `warm_arid` shape), there is no gradient derivation, and there is **NO early-Feb-indoor-start trick** (Utah's Mar 30 last frost is late enough that a normal late-Feb indoor start leaves January naturally inactive, so the deriver renders the honest winter `cold_pause` on its own; the ruling confirmed this by running the deriver). The three deltas from Nevada: (1) same warm-crop single-spring + summer `heat_pause` + NO fall replant shape, but no indoor-start workaround; (2) **apple + pear are `marginal`** (the marquee flip from Nevada's `fruits_reliably`), prose-only variety steer, plus a clean county-sourced low-elevation tree split; (3) **raspberry + blackberry `marginal` with a fall-bearing/low-chill prose steer** (mirroring the existing `warm_arid` raspberry text) and **strawberry a low-elevation thriver**. All 111 cells are authored OFF-canonical into per-class staging files, gated per-crop against a scratch canonical (scratch tools with `utah_dixie` in `EXPECTED_SPANS`), then promoted in ONE atomic SHA-guarded batch. `gate_all` is green before (no `utah_dixie`) and after (`utah_dixie` everywhere), never mid-flip.

**Tech Stack:** Python 3 standalone gate scripts (`whole_crop_gate.py`, `gate_all.py`, `zone_span_gate.py`, `coverage_floor_gate.py`, `chill_gate.py`, `second_planting_gate.py`, `photoperiod_gate.py`, `annual_calendar.py`, `second_cycle.py`, `apply_patch.py`), the region-generic tooling (`region_harness.py`, `region_cell_audit.py`, `build_region_promote.py` -- already built + source-injection-capable, extended not rebuilt), `prose_window_sweep.py`, the cloned SDD merge helper (`tools/staging/nevada_merge.py` -> `utah_dixie_merge.py`), compact JSON canonical, git on `main`.

## Global Constraints

Copied verbatim from the spec (`docs/superpowers/specs/2026-07-22-utah-dixie-region-design.md`) + CLAUDE.md; every task's requirements implicitly include these.

- **Canonical JSON is COMPACT:** `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` until the atomic promote (Task 11).** All authoring happens in staging files under `tools/staging/`.
- **TDD: RED before GREEN.** No new gate ships this arc, but every tool extension (Task 2) and the promote ceremony (Task 10) is adversarially proven on a scratch copy before it is trusted: RED-check A45 by injecting a stray non-span zone key (`resolved_by_zone["9"]`) into a single-zone `utah_dixie` cell; RED-check A43 by widening a cool-crop `second_planting` envelope past the first harvest span; RED-check A9 by flipping onion's `utah_dixie` `recommended_day_length_type` to `long_day` with a spring `plant_out`.
- **T1-or-it-doesn't-ship.** Every authored window/verdict cites a Tier-1 source (all `extension.usu.edu` USU Extension pages here, or NWS/Utah Climate Center for the frost normals). `usu_ext` is ALREADY catalogued and covers the whole USU family, so new `source_catalog` entries may be ZERO (Task 3 resolves whether to ride `usu_ext` generically or register a small set of per-pub sub-ids). No fabricated precision: a thin-source crop gets a conservative cell, flagged, never invented.
- **No em dashes in consumer copy** (`region_notes_*`, `suitability_note_*`, `chill_basis_*`, `cold_basis_*`, `zone_notes`, `notes`): use commas/colons/semicolons/periods. `--` is fine in docs/commits/code. American English. Temps render as `°F`. "plant" lowercase except at sentence start or "Plant Pro".
- **Zone span `utah_dixie = ["8"]`** (DECIDED; spec §2). SINGLE zone (15 ZIPs, a mix of 8a Santa Clara/La Verkin and 8b St. George/Washington/Hurricane). `warm_arid` (`["8"]`) is the structural precedent; A45 handles a single-zone span natively. Every `utah_dixie` cell's `resolved_by_zone` has EXACTLY the one key `"8"` (A45 parity). No `DONORS` entry (authored fresh, not zone-cloned). **NO isWarm #32 dependency** -- the whole belt is z8 (warm), so it resolves on the standard warm path once the app-side ZIP3 fence lands.
- **Utah Dixie is FROST-ANCHORED:** `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`, `calendar[]` DERIVED by `tools/annual_calendar.py`. `cold_pause` in winter is EXPECTED and correct. **Frost anchor z8: last frost Mar 30 / first frost Nov 1** (USU Extension Washington County, "Elevations for Washington County" 2020, Utah Climate Center actual-record for St. George; cross-confirmed by "Suggested Vegetable Planting Dates for Utah"). **NO early-Feb-indoor-start workaround** (the Nevada-specific fix): a normal late-Feb `start_indoors` (~6 weeks before the ~Apr 1 tomato transplant) leaves January inactive, so the deriver renders the honest `cold_pause` winter on its own. **VERIFY the derived tail in Task 4 (Jan `cold_pause`, Nov-Dec `cold_pause`) -- do not assume.**
- **The desert `heat_pause` is the point, and it must be SOURCED.** `heat_pause` is declaration-driven in the deriver (`annual_calendar.py` emits it only for a cell's declared `heat_pause` months), so an unsourced pause silently reshapes the calendar. Utah's is USU's blossom/fruit-set abort (>95degF day / <50degF night; >90degF early fruit-set abort), Jun-Aug ("often over 100 degrees in June, July, and August" -- USU frost/elevation doc). SOURCE IT.
- **A43 governs `second_planting` shape** (cool crops only here): single-span `start_indoors`/`plant_out`/`harvest`; envelope (`harvest_end` inside the FIRST harvest span, `last_plant_date` inside the FIRST `plant_out` span) INSIDE the primary windows. Read `tools/second_planting_gate.py`'s docstring; build two-window cool cells with `tools/second_cycle.py:build_two_cycle_cell(base, spring, fall)` (combine-derive-then-split; the deriver does NOT render `second_planting` directly -- memory `fall-cycle-deriver-combine-then-split`).
- **A9 (`photoperiod_gate`) WATCH:** St. George ~37degN; desert onions are intermediate-day and fall-planted, which FORBIDS an April-or-later `plant_out` (memory `onion-daylength-intermediate-a9-window-fit`). Author onion's `utah_dixie` `recommended_day_length_type` as `intermediate_day` (source it) and a FALL `plant_out`. Shallot follows onion by species identity. VERIFY A9 clean per Task 5.
- **State trio at content release** (Task 11): CURRENT_STATE.md surgical (drift memory `current-state-md-drift`: no `---` separator, hand-maintain), STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session.
- **No plant-astro submodule bump from this session** (memory `plant-astro-bump-owned-by-astro-session`). **Trevor confirms every push.** Don't commit the canonical change until Trevor approves.
- **CONCURRENT-CHECKOUT DISCIPLINE (active this repo).** Other sessions may share this checkout (memory `subagent-resumability-and-concurrent-git-safety` / `variety-region-arcs-parallel-safe`). Every commit: explicit-pathspec `git add` (never `git add -A`), `git status` before, `git show --stat` after. Tasks 1-10 are off-canonical (staging/scratch/tools) and collision-safe; only Task 11 writes the canonical, SHA-guarded.

## Crop roster (the 111, by class)

Locked from the Nevada canonical `b1045e04` (`verification_status.status == "verified_gs_arc"` AND non-empty `regions`). Re-run the query against the LIVE canonical at build start in case a concurrent session certified a crop.

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

- **frost_anchored (82):** the annual vegetable + herb roster. **Split for authoring into WARM (Task 4) and COOL/fall-planted (Task 5).** Reuse the Nevada warm-vs-cool classifier (run at build start; refine per-crop from the sources note):
  ```bash
  python3 -c "
  import json
  d=json.load(open('crops_data_final.json'))
  for c in d['crops']:
      if c.get('verification_status',{}).get('status')!='verified_gs_arc' or not c.get('regions'): continue
      if c.get('calendar_basis')!='frost_anchored': continue
      warm=False
      for rk in ('low_desert_az','se_gulf','warm_arid','ca_desert','nevada'):
          rc=c.get('regions',{}).get(rk)
          if not rc: continue
          for z,zc in (rc.get('resolved_by_zone') or {}).items():
              if 'heat_pause' in (zc.get('calendar') or []) or 'heat_pause' in zc: warm=True
      print(('WARM' if warm else 'cool'), c['slug'], 'frost_tol', c.get('frost_tolerance_f'))
  " | sort
  ```
  The fall-planted alliums (onion, garlic, shallot) fall in the COOL/fall batch (Task 5) with their delta callouts, regardless of the classifier.
- **perennial_chill_gated (14):** apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate. **Task 6.** The Washington County "Fruits" elevation split is the direct suitability authority: **apple + pear-asian + pear-european = `marginal`** (delta 4b); the low-elevation column (apricot/cherry-sour/cherry-sweet/fig/mulberry/nectarine/peach/persimmon/plum/pomegranate) = `fruits_reliably`; **pawpaw = `unsuitable`**.
- **perennial_evergreen (5):** grapefruit, lemon, lime, mandarin-clementine, orange-navel. **Task 7.** St. George is a cold-limited desert winter -> mostly `survives`/`unsuitable`.
- **perennial_woody_ornamental (5):** lavender, oregano, rosemary, sage, thyme. **Task 8.** Desert-strong (arid heat, alkaline soil).
- **berries_woody (4):** blackberry, blueberry, elderberry, raspberry. **Task 8.** raspberry/blackberry `marginal` (fall-bearing/low-chill prose steer, delta 4c); blueberry very-marginal (alkaline); elderberry marginal.
- **perennial_herbaceous (1):** strawberry. **Task 8.** A low-elevation THRIVER (USU low-elevation "Fruits" column; delta 4c).

## File Structure

- `tools/staging/utah_dixie_annuals_warm.json` -- warm-season frost_anchored cells (single spring + heat_pause, NO second_planting). `{slug: cell}`.
- `tools/staging/utah_dixie_annuals_cool.json` -- cool-season + fall-planted-allium cells (spring + fall `second_planting`; onion/garlic/shallot deltas). `{slug: cell}`.
- `tools/staging/utah_dixie_trees.json` -- 14 chill_gated trees (apple + pear delta-4b `marginal`; the low/high-elevation split).
- `tools/staging/utah_dixie_citrus.json` -- 5 evergreen citrus (cold-limited).
- `tools/staging/utah_dixie_perennials.json` -- 5 woody herbs + 4 berries + 1 strawberry (raspberry steer + strawberry thriver, delta 4c).
- `tools/staging/utah_dixie_chill_band.json` -- `region_chill_delivered.utah_dixie` + provenance (top-level).
- `tools/staging/utah_dixie_sources.json` -- the NEW `source_catalog` entries IF ANY (may be `{}` if all sourcing rides the catalogued `usu_ext`; Task 3 decides). Injected by `region_harness.scratch_canonical`; emitted as `add` patches by `build_region_promote`.
- `tools/staging/utah_dixie_merge.py` -- clone of `nevada_merge.py` (the SDD shard-merge helper).
- `tools/staging/utah_dixie_shard_guide.md` -- clone of `nevada_shard_guide.md` (the per-shard authoring brief).
- `tools/region_cell_audit.py` -- MODIFY: add a `utah_dixie` entry to `REGION_CONFIG`.
- `tools/build_region_promote.py` -- MODIFY: add `utah_dixie` to `STAGING` + `EXPECTED_CELLS`.
- `tools/batches/utah_dixie_region_promote.json` -- the atomic promote batch (generated).
- `docs/utah_dixie_cell_contract.md` -- the per-archetype cell template (the column contract).
- `docs/reviews/notes/2026-07-22/utah_dixie_sources.md` -- the T1 sourcing table + the chill-hunt result.
- `docs/reviews/notes/2026-07-22/utah_dixie_promote_dryrun.md` -- the scratch dry-run record.
- `docs/kickoffs/39-utah-dixie-plant-app.md` -- the paired plant-app handoff (confirm the next free kickoff number at build; #38 is this build's kickoff).

`region_harness.py` needs NO change (region_id + span params; patches `EXPECTED_SPANS` dynamically; already injects `staging/<region>_sources.json` -- handles an empty `{}` as zero source adds). The `region_cell_audit.py` + `build_region_promote.py` edits are additive dict entries.

---

## Task 1: Lock the cell contract + roster

**Files:**
- Create: `docs/utah_dixie_cell_contract.md`
- Read: `crops_data_final.json` (the Nevada `nevada` cells as the primary donor shape: `cherry-tomato nevada` [warm single-spring heat_pause+cold_pause], `lettuce-leaf nevada` [cool two-window], `garlic`/`onion nevada` [fall allium + A9]; `apple low_desert_az` [the `marginal` chill_basis idiom -- "high-chill varieties never fruit here"]; `apple warm_arid` [`fruits_reliably` contrast]; `raspberry warm_arid` [the fall-bearing/low-chill `region_notes_seasoned` to MIRROR]; `orange-navel nevada` [citrus])

**Interfaces:**
- Produces: `docs/utah_dixie_cell_contract.md` -- the authoritative per-archetype `utah_dixie` cell template Tasks 4-8 author against.

- [ ] **Step 1: Extract the archetype templates from canonical**

```bash
python3 -c "
import json
d=json.load(open('crops_data_final.json'))
by={c['slug']:c for c in d['crops']}
for slug,reg in [('cherry-tomato','nevada'),('lettuce-leaf','nevada'),('garlic','nevada'),('onion','nevada'),('apple','low_desert_az'),('apple','warm_arid'),('raspberry','warm_arid'),('orange-navel','nevada')]:
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
Expected: confirms (a) the **warm single-cycle heat_pause+cold_pause** shape from `cherry-tomato nevada`; (b) the cool two-window shape from `lettuce-leaf nevada`; (c) the fall-planted allium cell (`recommended_day_length_type`, fall `plant_out`) from `garlic`/`onion nevada`; (d) the `marginal` apple `chill_basis_*` idiom (`low_desert_az`) vs the `fruits_reliably` contrast (`warm_arid`); (e) the raspberry `warm_arid` `region_notes_seasoned` fall-bearing steer to mirror; (f) the citrus cell.

- [ ] **Step 2: Write `docs/utah_dixie_cell_contract.md`** (clone `docs/nevada_cell_contract.md`), with a full worked JSON example per archetype. Deltas from the Nevada contract:
  1. **Warm-season annual cell** (single spring cycle). Keys: `region_id="utah_dixie"`, `region_label="Utah: St. George Dixie (Mojave-edge high desert)"`, `zone_span=["8"]`, `sources`, `plantings[]` (ONE succession), `resolved_by_zone` (the ONE key `"8"`), `region_notes_beginner`, `region_notes_seasoned`. The `resolved_by_zone["8"]`: authored windows (`start_indoors` **late Feb**, `plant_out` ~Apr 1 per USU Group D, `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`), a declared **`heat_pause`** (Jun-Aug, SOURCED), NO `second_planting`, `calendar[]` DERIVED, `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`, `sources`, `anchoring_urls`. **NO early-Feb workaround** -- late-Feb indoor start + Mar 30 frost yields a natural January `cold_pause`. The tail after `heat_pause`: heat-tolerant crops (pepper/eggplant/okra) may render a light fall harvest resume then `cold_pause` (frost Nov 1); tomato/melon/squash render `season_over` -> `cold_pause`.
  2. **Cool-season annual cell** (two-window). Spring (Feb-Apr) + fall (`second_planting`, USU St. George fall cool-season window, built via `second_cycle.build_two_cycle_cell`), summer `heat_pause` between, `cold_pause` winter. A43 envelope. Fall-planted alliums (onion/garlic/shallot) are a sub-shape: a single FALL `plant_out`, `recommended_day_length_type=intermediate_day` for onion/shallot, garlic's USU St. George fall clove window.
  3. **Tree cell (chill-gated).** `suitability` per the Washington County "Fruits" elevation split; `chill_basis_{seasoned,beginner}`, `bloom`, real `harvest`, perennial calendar vocabulary. **apple + pear-asian + pear-european = `marginal`** (delta 4b, the exact prose in Task 6).
  4. **Citrus cell (cold-limited).** `suitability="survives"`/`"unsuitable"`, `min_winter_temp_f`, `cold_basis_{seasoned,beginner}`. A32-exempt; minimal calendar.
  5. **Berry / woody-herb / strawberry cell.** Real calendars (A32). Berries carry no suitability field -> marginality honesty in prose (raspberry fall-bearing steer). Herbs desert-strong. Strawberry a low-elevation thriver.

- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add docs/utah_dixie_cell_contract.md
git status
git commit -m "docs(utah_dixie): per-archetype cell contract for the Utah Dixie high-desert region column"
git show --stat HEAD
```

---

## Task 2: Extend the region-generic tooling for `utah_dixie`

**Files:**
- Modify: `tools/region_cell_audit.py` (add `utah_dixie` to `REGION_CONFIG`)
- Modify: `tools/build_region_promote.py` (add `utah_dixie` to `STAGING` + `EXPECTED_CELLS`)
- Test: `tools/test_region_cell_audit.py`, `tools/test_build_region_promote.py` (extend existing)

**Interfaces:**
- Consumes: the shipped region-generic tools.
- Produces: `REGION_CONFIG["utah_dixie"]` (label, span `["8"]`, frost_model `"anchored"`); `STAGING["utah_dixie"]` (the 5 cell files + band) + `EXPECTED_CELLS["utah_dixie"] = 111`. `region_harness.gate_crop("utah_dixie", ["8"], slug, cells)` works with no harness change.

- [ ] **Step 1: Write the failing test for the auditor config**

Append to `tools/test_region_cell_audit.py`:
```python
def test_utah_dixie_config_present_anchored():
    import region_cell_audit as rca
    cfg = rca.REGION_CONFIG["utah_dixie"]
    assert cfg["span"] == ["8"]
    assert cfg["frost_model"] == "anchored"
    assert cfg["label"] == "Utah: St. George Dixie (Mojave-edge high desert)"

def test_utah_dixie_single_zone_heat_pause_plus_cold_pause_allowed():
    import region_cell_audit as rca
    cell = {
        "region_id": "utah_dixie",
        "region_label": "Utah: St. George Dixie (Mojave-edge high desert)",
        "zone_span": ["8"],
        "resolved_by_zone": {
            "8": {"plant_out": "Apr 1 - May 1", "harvest": "Jun 5 - Jul 5",
                  "harvest_start": "Jun 5", "harvest_end": "Jul 5",
                  "first_plant_date": "Apr 1", "last_plant_date": "May 1",
                  "resolution_method": "frost_anchored_resolved",
                  "resolved_from": {"last_frost": "Mar 30", "first_frost": "Nov 1"},
                  "calendar": ["cold_pause","cold_pause","indoors","plant","growing","harvest",
                               "heat_pause","heat_pause","heat_pause","season_over","cold_pause","cold_pause"]}}}
    assert not any("cold_pause" in v or "heat_pause" in v
                   for v in rca.audit_cell("cherry-tomato", cell, "utah_dixie"))
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k utah_dixie -v`
Expected: FAIL with `KeyError: 'utah_dixie'`.

- [ ] **Step 3: Add the `utah_dixie` config entry** in `tools/region_cell_audit.py` `REGION_CONFIG` (after `nevada`):
```python
    "utah_dixie": {"label": "Utah: St. George Dixie (Mojave-edge high desert)",
                   "span": ["8"], "frost_model": "anchored"},
```

- [ ] **Step 4: Run auditor tests to verify they pass**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -k utah_dixie -v`
Expected: 2 passed.

- [ ] **Step 5: Write the failing test for the promote emitter**

Append to `tools/test_build_region_promote.py`:
```python
def test_utah_dixie_registered():
    import build_region_promote as brp
    assert "utah_dixie" in brp.STAGING
    assert brp.EXPECTED_CELLS["utah_dixie"] == 111
    files, band = brp.STAGING["utah_dixie"]
    assert band == "utah_dixie_chill_band.json"
    assert set(files) == {
        "utah_dixie_annuals_warm.json", "utah_dixie_annuals_cool.json",
        "utah_dixie_trees.json", "utah_dixie_citrus.json", "utah_dixie_perennials.json"}
```

- [ ] **Step 6: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k utah_dixie -v`
Expected: FAIL (`KeyError` / assertion).

- [ ] **Step 7: Add the `utah_dixie` STAGING + EXPECTED_CELLS entries** in `tools/build_region_promote.py`:
```python
    "utah_dixie": (["utah_dixie_annuals_warm.json", "utah_dixie_annuals_cool.json",
                    "utah_dixie_trees.json", "utah_dixie_citrus.json",
                    "utah_dixie_perennials.json"], "utah_dixie_chill_band.json"),
```
and add `"utah_dixie": 111` to `EXPECTED_CELLS`.

- [ ] **Step 8: Run test to verify it passes**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -k utah_dixie -v`
Expected: PASS.

- [ ] **Step 9: Regression guard -- confirm prior regions untouched**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py test_build_region_promote.py -v`
Expected: all pass (rgv/pnw/mid_atlantic/mid_south/nevada + utah_dixie).

- [ ] **Step 10: Commit** (explicit pathspec)

```bash
git add tools/region_cell_audit.py tools/build_region_promote.py tools/test_region_cell_audit.py tools/test_build_region_promote.py
git status
git commit -m "feat(utah_dixie): register region in cell-auditor + promote-emitter (z8 single-zone, anchored, 111 cells)"
git show --stat HEAD
```

---

## Task 3: T1 sourcing pass + the chill-hunt + chill band + frost anchor

**Files:**
- Create: `docs/reviews/notes/2026-07-22/utah_dixie_sources.md`
- Create: `tools/staging/utah_dixie_sources.json` (may be `{}`)
- Create: `tools/staging/utah_dixie_chill_band.json`

**Interfaces:**
- Produces: the sourcing table (crop/class -> source id + url + spring/fall windows + frost dates); `tools/staging/utah_dixie_sources.json` (new `source_catalog` entries IF ANY); `region_chill_delivered.utah_dixie` band + provenance (drives A3 in Task 6).

- [ ] **Step 1: Fetch + record the T1 sources.** Use WebFetch + `pypdf` in THIS controller env (subagent sandboxes block PDF tooling). The USU authorities (all `extension.usu.edu`; PDFs re-extract cleanly with `pypdf`), from the ruling `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md`:
  - **"Elevations for Washington County" (2020)** (`https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf`) -- frost anchor z8 Mar 30 / Nov 1 (St. George actual-record).
  - **"Suggested Vegetable Planting Dates for Utah"** (`https://extension.usu.edu/yardandgarden/research/suggested-vegetable-planting-dates-for-utah`) -- the per-crop planting-date table (St. George tomato Group D transplant Apr 1); the load-bearing window source.
  - **"How to Grow Tomatoes in Your Garden"** (`https://extension.usu.edu/yardandgarden/research/tomatoes-in-the-garden`) -- heat abort thresholds (>95degF/<50degF; >90degF fruit-set); no fall tomato.
  - **"Fall Gardening in the St. George Area"** (Heflebower, `https://extension.usu.edu/washington/files/Fall_Vegetable.pdf`) -- the fall cool-season window (broccoli/cabbage/cauliflower/lettuce/carrots/spinach/onions/turnips/beets).
  - **"Fruits" (Washington County)** (`https://extension.usu.edu/washington/gardening/fruits/`) -- the elevation fruit split (delta 4b): low-elevation apricot/cherry/fig/grape/peach/persimmon/plum/strawberry thrive; apple/pear/raspberry/blackberry higher-elevation only.
  - **"Raspberry Management for Utah"** (`https://extension.usu.edu/yardandgarden/research/raspberry-management-for-utah`) -- names "Utah's Dixie" as fall-bearing-raspberry territory (delta 4c).
- [ ] **Step 1b: THE CHILL-HUNT (hunt-once-then-flag, Trevor-confirmed).** Take ONE targeted swing at a real St.-George-specific numeric chill-hour figure before settling the band: fetch the **Utah Climate Center FGNET (Fruit Growth Network) Washington County station** page + re-check USU's "Apple Production and Variety Recommendations for the Utah Home Garden" and "How to Grow Peaches" for a St. George regional number. If a T1 number surfaces, use it for the band (Step 4). If none does (the ruling's multi-source search already found none), proceed with the elevation-bracketed `[250,450]` and the honest provenance flag. **Record the hunt outcome in the sources note either way.**

- [ ] **Step 2: Resolve source registration** -- write `tools/staging/utah_dixie_sources.json`. FIRST inspect whether the catalogued `usu_ext` entry is portal-level (covers the USU Extension family) or per-pub:
  ```bash
  python3 -c "import json;d=json.load(open('crops_data_final.json'));print(json.dumps(d['source_catalog'].get('usu_ext'),ensure_ascii=False,indent=1))"
  ```
  - If `usu_ext` is portal-level (the likely case), every USU page above rides `usu_ext` -> write `utah_dixie_sources.json` as `{}` (zero new ids; the emitter emits 0 source adds). Only the Utah Climate Center / NWS frost normal, IF it is a distinct institution not covered by an existing id, needs a new entry.
  - If per-pub granularity is the catalog norm (the `unr_sp2007`-under-`unr_ext` pattern), register a small set of USU sub-ids (e.g. `usu_ext_veg_dates`, `usu_ext_wash_fruits`, `usu_ext_raspberry`, `usu_ext_wash_frost`) matching a real neighbor entry's field shape EXACTLY (`name`/`tier`/`url`/`kind`/`verified`).
  Confirm the observed convention; do not assume.

- [ ] **Step 3: Write the sourcing table** `docs/reviews/notes/2026-07-22/utah_dixie_sources.md` -- a table `crop_or_class | source_id | url | spring_window | fall_window | frost_dates | tier | notes`. Top block: the z8 frost normal (Mar 30 / Nov 1) + **the chill-hunt outcome** (number found, or "no T1 St.-George chill figure found; band is elevation-bracketed inference"). A column marks which annuals are WARM (single spring, no fall) vs COOL (spring + fall). The garlic + onion delta rows + the apple/pear/raspberry marginal rows are called out. Any thin-source crop is flagged for a conservative cell.

- [ ] **Step 4: Author the chill band** `tools/staging/utah_dixie_chill_band.json`. First verify the CURRENT canonical neighbor bands to anchor the bracket:
  ```bash
  python3 -c "import json;d=json.load(open('crops_data_final.json'));r=d['region_chill_delivered'];print('low_desert_az',r.get('low_desert_az'));print('warm_arid',r.get('warm_arid'));print('nevada',r.get('nevada'))"
  ```
  Then (assuming the hunt found no number) write the Phoenix-bracketed band + the honest provenance flag:
```json
{
  "region_chill_delivered.utah_dixie": {"8": [250, 450]},
  "region_chill_delivered_provenance.utah_dixie": "St. George / Washington County z8 core, ~2,624 ft. No USU-published numeric chill-hour figure for St. George was found despite a targeted Utah Climate Center FGNET + USU apple/peach search (verified 2026-07-22); this band is elevation-bracketed INFERENCE, not a measured figure, set between the two existing z8/z9 desert regions that bracket St. George's elevation: low_desert_az (Phoenix, ~1,100 ft) below and warm_arid (Las Cruces, ~3,900 ft) above, leaning to the Phoenix/marginal end per Washington County Extension's own elevation-based fruit recommendation (apple only at the county's higher-elevation towns)."
}
```
  (If the hunt DID find a St.-George number, use it and rewrite the provenance to cite it.) Verify against `chill_gate.py`'s expected shape (`region -> {zone -> [lo,hi]}`, numeric, lo<=hi). Confirm the top-level path form matches the shipped `nevada_chill_band.json`.

- [ ] **Step 5: Commit** (explicit pathspec)

```bash
git add docs/reviews/notes/2026-07-22/utah_dixie_sources.md tools/staging/utah_dixie_sources.json tools/staging/utah_dixie_chill_band.json
git status
git commit -m "docs(utah_dixie): T1 USU sourcing table + chill-hunt outcome + elevation-bracketed chill band"
git show --stat HEAD
```

---

## Task 4: Author the warm-season annual cells (single spring + heat_pause, NO second_planting)

**Files:**
- Create: `tools/staging/utah_dixie_annuals_warm.json` (`{slug: cell}`)

**Interfaces:**
- Consumes: `docs/utah_dixie_cell_contract.md`, the sources note, `region_harness.gate_crop`, `region_cell_audit`, `annual_calendar.derive_annual_calendar`.
- Produces: `tools/staging/utah_dixie_annuals_warm.json`.

Subagent-parallelizable: one worker per crop (or per family), writing into the shared staging dict (controller-merged via `utah_dixie_merge.py`; no per-subagent commits). **Structural donor is the `cherry-tomato nevada` cell** (identical warm shape; re-author windows to USU + St. George frost, collapse to the single zone). **Per-crop procedure:**

- [ ] **Step 1: Author the cell for warm crop `<slug>`.** Read the crop's `nevada` cell (single-cycle heat_pause+cold_pause shape) and its `warm_arid`/`low_desert_az` cell (desert region voice + real heat months). Author the `utah_dixie` cell:
  - `region_id="utah_dixie"`, `region_label="Utah: St. George Dixie (Mojave-edge high desert)"`, `zone_span=["8"]`.
  - `resolved_by_zone` with the ONE key `"8"`; `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`; `resolution_method="frost_anchored_resolved"`.
  - **`start_indoors` in late February** (~6 weeks before the ~Apr 1 transplant). `plant_out` ~Apr 1 (USU Group D; tighter/later than Nevada's mid-March). NO early-Feb workaround needed. The late-spring succession tail belongs in `region_notes`, not stretched into the calendar to collide with the Jun heat_pause.
  - A declared **`heat_pause`** on the Jun-Aug months (SOURCED to USU's >90-95degF cutoff). NO `second_planting`.
  - Dual-register `region_notes_{beginner,seasoned}` in house voice (no em dashes): spring window, the summer heat abort, and the honest "no fall replant recommended here" (USU St. George fall guidance is cool-season only).
  - Cite the USU source ids (per Task 3) in `sources` + `anchoring_urls` (verified 2026-07-22).

- [ ] **Step 2: Derive + INSPECT the `calendar[]`:**
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell=json.load(open('tools/staging/utah_dixie_annuals_warm.json'))['<slug>']['resolved_by_zone']['8']
print(derive_annual_calendar(cell))
"
```
Set the zone's `calendar[]` to the derived array. **Assert the honest tail (NO early-Feb trick relied on):** `cold_pause` Jan-Feb (through the late-Feb indoor start), spring `plant`/`growing`/`harvest`, `heat_pause` at Jun-Aug, then EITHER a light fall `harvest` resume (heat-tolerant crops) OR `season_over` (tomato/melon/squash), then `cold_pause` Nov-Dec (frost Nov 1). **There must be NO phantom fall `plant`/`growing`, and Nov-Dec MUST be `cold_pause`.** If January comes back active (it should not, with a late-Feb start + Mar 30 frost), re-check the indoor-start month. If the deriver will not produce the honest tail, hand-author the tail tokens and confirm `calendar_coherence` accepts them (Step 3).

- [ ] **Step 3: Gate + audit the crop.** Run `python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_annuals_warm.json <slug>` -> PASS (A45 single-zone parity, A31/A32, calendar coherence, 0 em dashes, T1 sources). Run `python3 tools/region_cell_audit.py utah_dixie tools/staging/utah_dixie_annuals_warm.json` -> 0 issues. Fix + re-gate until clean. Common failures: unsourced `heat_pause`, span/key mismatch (must be exactly `"8"`), `resolved_from` null, em dash, an `in-ground-month`-tokened `season_over`.

- [ ] **Step 4: Commit the batch** (after all warm crops pass; explicit pathspec)

```bash
git add tools/staging/utah_dixie_annuals_warm.json
git status
git commit -m "feat(utah_dixie): author warm-season annual cells (single spring + heat_pause, no fall replant per USU)"
git show --stat HEAD
```

---

## Task 5: Author the cool-season + fall-planted-allium annual cells (two-window)

**Files:**
- Create: `tools/staging/utah_dixie_annuals_cool.json` (`{slug: cell}`)

**Interfaces:**
- Consumes: `docs/utah_dixie_cell_contract.md`, the sources note, `region_harness.gate_crop`, `region_cell_audit`, `second_cycle.build_two_cycle_cell`, `photoperiod_gate`.
- Produces: `tools/staging/utah_dixie_annuals_cool.json`.

Cool crops run the desert two-window (spring Feb-Apr + fall via USU's St. George fall cool-season guidance), which KEEPS the `second_planting` fall cycle. Subagent-parallelizable. **Per-crop procedure:**

- [ ] **Step 1: Author the two-window cool cell for `<slug>`** with `second_cycle.build_two_cycle_cell(base, spring, fall)`:
```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from second_cycle import build_two_cycle_cell
# base = the region-constant single-zone skeleton (region_id/label/span=['8']/sources/plantings);
# spring/fall = the authored window dicts (Feb-Apr spring, USU St. George fall window) per the sources note.
# See second_cycle.py docstring for the exact spring/fall dict shape; build the '8' cell,
# heat_pause on the summer months between the two windows.
"
```
Author `resolved_by_zone` for the ONE key `"8"`; `resolution_method="frost_anchored_resolved"`; `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`; a summer `heat_pause`; the fall `second_planting` (A43 single-span + envelope-inside). Dual-register `region_notes_*` (no em dashes).

- [ ] **Step 2: The fall-planted alliums (onion, garlic, shallot) -- the deltas.**
  - **onion / shallot:** a single FALL `plant_out` (sets/transplants), NO spring plant, harvest late spring. Set `recommended_day_length_type="intermediate_day"` (St. George ~37degN; source it; the `warm_arid`/`nevada` onion are the analogs). Fall-planted -> no April-or-later `plant_out` -> A9 window-fit satisfied by construction. Shallot cell says "follows onion" (species identity).
  - **garlic (delta):** a single FALL clove `plant_out` window per USU's St. George fall-gardening / vegetable-date guidance (source the exact window; likely Sep-Oct). Harvest the following early summer. Do NOT inherit `warm_arid`/`low_desert_az` verbatim; author St. George's own window.

- [ ] **Step 3: Derive/confirm `calendar[]`, gate + audit.** Run `python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_annuals_cool.json <slug>` -> PASS. Run `python3 tools/region_cell_audit.py utah_dixie tools/staging/utah_dixie_annuals_cool.json` -> 0. **Onion/shallot: explicitly run A9** -- `python3 tools/photoperiod_gate.py` (or the harness path that invokes it) and confirm `utah_dixie` onion/shallot = 0 violations (no forbidden spring `plant_out`).

- [ ] **Step 4: RED-check A9 once** (adversarial): on a scratch copy of the onion cell, flip `utah_dixie` `recommended_day_length_type` to `long_day` AND move `plant_out` to April; run the harness and confirm A9 bounces it; discard. Record in the dry-run note (Task 10).

- [ ] **Step 5: Commit the batch** (after all cool + allium crops pass; explicit pathspec)

```bash
git add tools/staging/utah_dixie_annuals_cool.json
git status
git commit -m "feat(utah_dixie): author cool-season + fall-allium annual cells (two-window; garlic + onion deltas)"
git show --stat HEAD
```

---

## Task 6: Author the 14 chill_gated tree cells (apple + pear delta-4b marginal; the elevation split)

**Files:**
- Create: `tools/staging/utah_dixie_trees.json`

**Interfaces:**
- Consumes: `docs/utah_dixie_cell_contract.md` (tree template), the sources note, `tools/staging/utah_dixie_chill_band.json`, `region_harness.gate_crop`.
- Produces: `tools/staging/utah_dixie_trees.json`.

**The Washington County "Fruits" elevation split is the DIRECT T1 suitability authority** (not a mechanical band-vs-`chill_hours_required` comparison; the county's field recommendation already integrates chill + heat + frost). The `[250,450]` band informs the variety-steer prose, not the suitability class.

- [ ] **Step 1: Author each tree cell.** Read the crop's `warm_arid`/`low_desert_az`/`nevada` tree cell for the desert fruiting-cell shape.
  - **apple = DELTA 4b (`marginal`, Trevor-confirmed):** `suitability="marginal"`. `chill_basis_seasoned`/`chill_basis_beginner` state the honest steer: at St. George's ~2,624 ft low-elevation Dixie core the belt banks only enough chill for the lowest-chill third, so only **Dorsett Golden (100), Anna (200), Ein Shemer (100)** crop reliably; Washington County Extension recommends apple mainly for the county's HIGHER-elevation towns (Central, Enterprise, New Harmony, 5,300+ ft) OUTSIDE the z8 belt; the mid/high-chill varieties (Gala, Fuji, Granny Smith, Honeycrisp, McIntosh, and up) do not accumulate enough chill here. Cite the Washington County "Fruits" page. No em dashes. (This is the `low_desert_az` "high-chill varieties never fruit here" idiom, and the INVERSE of Nevada's `fruits_reliably` apple.)
  - **pear-asian + pear-european = `marginal`:** grouped with apple in the county's higher-elevation column; same elevation-chill logic in `chill_basis_*`, low-chill cultivar steer where sourced.
  - **low-elevation column = `fruits_reliably`:** apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, peach, persimmon, plum, pomegranate (the county's low-elevation thrive list). Re-judged from the ARID reality (late frost + sunburn, not humid brown-rot). Where a crop's nominal chill is high (e.g. peach 500-1050), `chill_basis_*` names the low-chill variety selection the county's recommendation implies. Real `bloom` + `harvest`.
  - **pawpaw = `unsuitable`:** a humid-forest understory tree, hostile in the dry alkaline Mojave (on neither county column). Source the honesty in `chill_basis_*`/`suitability_note_*`.
  - Perennial calendar vocabulary; region-level `plantings_provenance`.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_trees.json <slug>` -> PASS; confirm A3 (`perennial_gate`) coheres (`fruits_reliably` requires a calendar; `marginal` apple/pear + `unsuitable` pawpaw handled -- the mid-Atlantic/mid-South `marginal`-tree precedent). `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/utah_dixie_trees.json
git status
git commit -m "feat(utah_dixie): author 14 chill_gated tree cells (apple + pear marginal; county elevation split)"
git show --stat HEAD
```

---

## Task 7: Author the 5 citrus cells (cold-limited)

**Files:**
- Create: `tools/staging/utah_dixie_citrus.json`

**Interfaces:**
- Consumes: `docs/utah_dixie_cell_contract.md` (citrus template), `region_harness.gate_crop`.
- Produces: `tools/staging/utah_dixie_citrus.json`.

- [ ] **Step 1: Author each citrus cell** (grapefruit, lemon, lime, mandarin-clementine, orange-navel). St. George is a cold-limited desert winter (colder than Phoenix), so citrus is `suitability="survives"` (protected/container culture where real, sourced) or `"unsuitable"`; the hardier mandarin least bad, lime/grapefruit worst. `min_winter_temp_f`; `cold_basis_{seasoned,beginner}` explaining the limit honestly (no em dashes). Re-judged fresh (the `nevada` citrus cells are the closest analog). A32-exempt; minimal calendar.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_citrus.json <slug>` -> PASS; A3 coheres (no `fruits_reliably`). `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/utah_dixie_citrus.json
git status
git commit -m "feat(utah_dixie): author 5 citrus cells (cold-limited desert winter)"
git show --stat HEAD
```

---

## Task 8: Author the 10 remaining perennials (woody herbs + berries + strawberry)

**Files:**
- Create: `tools/staging/utah_dixie_perennials.json`

**Interfaces:**
- Consumes: `docs/utah_dixie_cell_contract.md`, the sources note (esp. the `raspberry warm_arid` text to mirror), `region_harness.gate_crop`.
- Produces: `tools/staging/utah_dixie_perennials.json`.

All are frost-anchored calendar cells (A32 applies -- real calendars required).

- [ ] **Step 1: Author each cell.**
  - **Woody herbs (lavender, oregano, rosemary, sage, thyme):** desert-STRONG (arid heat + alkaline soil is their preference; the `warm_arid`/`low_desert_az`/`nevada` thriving framing). Real frost-anchored calendars; summer is the growing season. `grown_as` where a herb needs winter protection at the z8 edge.
  - **Berries -- delta 4c:** **raspberry `marginal` with the fall-bearing/low-chill steer** -- MIRROR the existing `warm_arid` raspberry `region_notes_seasoned` ("hot, low, alkaline-soil sites are marginal and need heat-tolerant, low-chill everbearing types"); name the primocane/fall-bearing types (Bababerry, Dorman Red, Caroline, Autumn Bliss, Heritage, Anne) in prose, cite the USU "Raspberry Management for Utah" page that names "Utah's Dixie." **blackberry `marginal`** (county higher-elevation column). **Blueberry very-marginal** (needs acidic soil, hostile in the alkaline Mojave -> container-only honesty, sourced). **Elderberry marginal.** Berries carry no suitability field; honesty lives in prose; A32 still forces a calendar.
  - **Strawberry -- delta 4c:** a low-elevation THRIVER (USU lists it in the low-elevation "Fruits" column; a cleaner positive verdict than Nevada's fall-set-only). Real calendar; `grown_as` where relevant.
- [ ] **Step 2: Gate + audit each** via `python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_perennials.json <slug>` -> PASS. `region_cell_audit` -> 0.
- [ ] **Step 3: Commit** (explicit pathspec)

```bash
git add tools/staging/utah_dixie_perennials.json
git status
git commit -m "feat(utah_dixie): author 10 perennial cells (desert herbs + marginal berries + strawberry thriver)"
git show --stat HEAD
```

---

## Task 9: Build the atomic promote batch

**Files:**
- Create: `tools/batches/utah_dixie_region_promote.json` (generated)

**Interfaces:**
- Consumes: the five `tools/staging/utah_dixie_*.json` cell files + `utah_dixie_chill_band.json` + `utah_dixie_sources.json`; the Task 2 `STAGING`/`EXPECTED_CELLS` entries.
- Produces: `tools/batches/utah_dixie_region_promote.json` -- an `apply_patch` batch adding, per crop, `$.crops[?(@.slug=='<slug>')].regions.utah_dixie` (op `add`), plus top-level `region_chill_delivered.utah_dixie` + provenance + any new `$.source_catalog.<id>` adds. `EXPECTED_SPANS.utah_dixie` is a CODE edit to `tools/zone_span_gate.py` (Task 11 Step 1), applied in the same commit as the batch, NOT part of the JSON batch.

- [ ] **Step 1: Generate the batch**

Run: `python3 tools/build_region_promote.py utah_dixie`
Expected stdout: `emitted <N> patches (111 utah_dixie cells + 2 top-level + <n_src> source_catalog); base_sha b1045e04...`. The emitter asserts `len(seen) == 111` (from `EXPECTED_CELLS`), so a miscount aborts here; it also asserts no `source_catalog` id collision. `<n_src>` may be 0 if all sourcing rides `usu_ext`.

- [ ] **Step 2: Verify the generated batch**

```bash
python3 -c "
import json
b=json.load(open('tools/batches/utah_dixie_region_promote.json'))
ops=b['patches']
cells=[o for o in ops if o['json_path'].endswith('.regions.utah_dixie')]
srcs=[o for o in ops if o['json_path'].startswith('\$.source_catalog.')]
assert len(cells)==111, len(cells)
assert all(o['op']=='add' for o in ops), 'utah_dixie is net-new everywhere'
assert any('region_chill_delivered.utah_dixie' in o['json_path'] for o in ops)
print('batch OK:', len(ops), 'ops,', len(cells), 'cells,', len(srcs), 'source adds, base_sha', b['base_sha'][:12])
"
```
Expected: `batch OK: <N> ops, 111 cells, <n_src> source adds, base_sha b1045e0433c7`.

- [ ] **Step 3: Commit** (batch only; canonical still untouched; explicit pathspec)

```bash
git add tools/batches/utah_dixie_region_promote.json
git status
git commit -m "feat(utah_dixie): deterministic atomic-promote batch (111 cells + chill band + source adds)"
git show --stat HEAD
```

---

## Task 10: Dry-run the promote on a scratch copy (full gate ceremony, RED-checked)

**Files:**
- Modify (scratch only): a copy of `crops_data_final.json` + `tools/zone_span_gate.py`
- Create: `docs/reviews/notes/2026-07-22/utah_dixie_promote_dryrun.md`

**Interfaces:**
- Consumes: `tools/batches/utah_dixie_region_promote.json`, `region_harness.build_scratch_tools`, `region_harness.scratch_canonical`, `region_cell_audit`.
- Produces: proof that the full suite is green post-promote before touching the real canonical.

- [ ] **Step 1: Apply the batch to a scratch canonical.** Compute `sha256_before` from the real file, apply via `tools/apply_patch.py` to a COPY, confirm COMPACT + count 128 + footprint = exactly 111 `regions.utah_dixie` cells + the top-level `region_chill_delivered.utah_dixie` + provenance + any `source_catalog` adds, via a byte-diff audit (NO other crop/key touched; all 128 else byte-identical).

- [ ] **Step 2: Build scratch tools + run the full suite** against the scratch canonical:
  - `region_harness.build_scratch_tools(dest, "utah_dixie", ["8"])` (patches `EXPECTED_SPANS`).
  - `gate_all.py` -> 119/119.
  - `zone_span_gate.py` (A45) -> 0 (single-zone parity on `"8"`).
  - `coverage_floor_gate.py` (A31/A32) -> 0 (all 111 carry `utah_dixie`).
  - `chill_gate.py` -> 0.
  - `second_planting_gate.py` (A43) -> 0 across the cool-crop fall cycles.
  - `photoperiod_gate.py` (A9) -> 0 for onion/shallot `utah_dixie`.
  - `whole_crop_gate.py` on a per-class sample (cherry-tomato, lettuce-leaf, garlic, onion, apple, peach, orange-navel, lavender, raspberry, blueberry, strawberry) -> PASS.
  - `region_cell_audit.py utah_dixie` over all five staging files -> 0.
  - `calendar_coherence` + `timing_spine` -> 0.
  - `prose_window_sweep.py` -> 0 (prose windows match the resolved windows; catches stale Phoenix/warm_arid/nevada residue in cloned prose).
  - `release_verify.py` -> clean modulo the documented roster-wide section-A collateral (the pre-commit backstop is the binding multi-crop gate).

- [ ] **Step 3: RED-check the promote** on the scratch copy (restore after each): (a) inject a stray non-span key `resolved_by_zone["9"]` into one crop's `utah_dixie` cell (with `zone_span` still `["8"]`) -> A45 parity bounces it; (b) widen a cool-crop `second_planting` envelope past the first harvest span -> A43 bounces it; (c) flip onion `utah_dixie` to `long_day` + April `plant_out` -> A9 bounces it. Proves the ceremony catches the span-parity + fall-envelope + photoperiod defect classes at roster scale.

- [ ] **Step 4: Record + commit** the dry-run result in `docs/reviews/notes/2026-07-22/utah_dixie_promote_dryrun.md` (gate outputs + footprint audit + the three RED-check results). (explicit pathspec)

```bash
git add docs/reviews/notes/2026-07-22/utah_dixie_promote_dryrun.md
git status
git commit -m "test(utah_dixie): scratch-copy promote dry-run green + A45/A43/A9 RED-check"
git show --stat HEAD
```

---

## Task 11: Promote to canonical + release ceremony (THE one canonical write)

**Files:**
- Modify: `crops_data_final.json` (the atomic promote)
- Modify: `tools/zone_span_gate.py` (add `utah_dixie` to `EXPECTED_SPANS`)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`
- Modify: `docs/region_coverage_roadmap.md`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 0: CONCURRENCY COORDINATION.** Before touching the canonical:
  - `git fetch` + `git log --oneline origin/main..main` + `git log -1 crops_data_final.json`.
  - Re-read the LIVE SHA: `shasum -a 256 crops_data_final.json`. If it is no longer `b1045e04`, a concurrent promote landed. If path-disjoint from `*.regions.utah_dixie` + any added `source_catalog` ids, that is FINE, but you MUST: (a) re-run the roster query -> still 111; (b) re-run each staging file through `region_harness` against the live canonical -> all green; (c) confirm none of `utah_dixie_sources.json`'s ids now collide; (d) regenerate the batch with the LIVE SHA (`build_region_promote.py utah_dixie` re-stamps `base_sha` from the live file, or `--base-sha <LIVE>`).
  - Do NOT hold the canonical open concurrently with another session.

- [ ] **Step 1: Add `utah_dixie` to the REAL `tools/zone_span_gate.py` `EXPECTED_SPANS`** (`"utah_dixie": ["8"]`). No `DONORS` entry (authored fresh). `coverage_floor_gate` auto-derives its `CANONICAL_REGIONS`/`CANONICAL_ZONES` from `EXPECTED_SPANS`.

- [ ] **Step 2: Apply the batch to the REAL canonical** via `tools/apply_patch.py` with the LIVE `sha256_before` (Step 0). Confirm COMPACT, no trailing newline, count 128.

- [ ] **Step 3: Full release verification** (protocol #6):
  - `python3 tools/whole_crop_gate.py <slug>` on the 18 gold anchors -> 18/18 PASS.
  - `python3 tools/gate_all.py` -> 119/119.
  - `python3 tools/zone_span_gate.py` (A45), `coverage_floor_gate.py` (A31/A32), `chill_gate.py`, `second_planting_gate.py` (A43), `photoperiod_gate.py` (A9) -> 0.
  - `python3 tools/prose_window_sweep.py` -> 0.
  - `python3 tools/release_verify.py` -> clean (modulo documented roster-wide section-A collateral).
  - `python3 tools/region_cell_audit.py utah_dixie tools/staging/utah_dixie_*.json` -> 0.
  - Independent footprint audit: exactly 111 `regions.utah_dixie` + `region_chill_delivered.utah_dixie` + provenance + any `source_catalog` adds changed; all else byte-identical; count 128.
  - The **pre-commit backstop** (`precommit_release_verify.py`) runs on commit -- checks ALL changed crops.
  - Per-batch source-truth sample: re-verify 3-4 authored windows (incl. a garlic fall window, the apple `marginal` variety line, a cool-crop fall window, and the raspberry steer) against their cited USU URLs.

- [ ] **Step 4: State trio** -- surgically update CURRENT_STATE.md (drift memory: hand-maintain, no `---`), prepend STATE_HISTORY.md (most-recent-first), bump LATEST.txt (new SHA + session line).

- [ ] **Step 5: Roadmap + register** -- mark roadmap item 11 SHIPPED (new canonical SHA + commit); add a `docs/field_addition_register.md` row (next number, ~#22) for the Utah Dixie region column.

- [ ] **Step 6: Independent content review** (before commit or as the final gate): dispatch a fresh opus content-review subagent over a per-class sample of the authored `utah_dixie` cells for factual/honesty/direction/date-consistency + em-dash + delta fidelity (apple/pear `marginal` steer exact + the lowest-chill-third list; low-elevation tree list matches the county page; raspberry fall-bearing steer mirrors `warm_arid`; strawberry thriver; garlic St. George window; warm-crop no-fall honesty; NO fabricated USU windows). Apply SHIP-WITH-FIXES corrections.

- [ ] **Step 7: Commit** (UNPUSHED -- Trevor confirms push; explicit pathspec)

```bash
git add crops_data_final.json tools/zone_span_gate.py CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/region_coverage_roadmap.md docs/field_addition_register.md
git status
git commit -m "feat(utah_dixie): certify the Utah Dixie high-desert region across 111 crops (roadmap item 11)"
git show --stat HEAD
```

---

## Task 12: Write the paired plant-app kickoff

**Files:**
- Create: `docs/kickoffs/39-utah-dixie-plant-app.md` (confirm the next free kickoff number at build; #38 is this build's kickoff)

**Interfaces:**
- Produces: the handoff so plant-app can route the belt's ZIPs to `utah_dixie`.

- [ ] **Step 1: Write the kickoff** covering:
  - `REGION_STATES.utah_dixie = ['UT']`.
  - `regions.json` row + `SHORT_REGION_LABEL.utah_dixie`.
  - **A ZIP3 fence IS needed:** UT spans the Wasatch Front (Salt Lake 840/841, Provo 846, z6-7, `northern_tier`) as well as the SW Dixie corner. Fence `utah_dixie` to the St. George Washington County ZIP3s (**847xx** only); the northern Utah ZIP3s (840/841/842/843/844/845/846) must NOT resolve to the Mojave calendar. Confirm the exact 847xx membership vs `zip-zones.json` at write time (the z8 core is only 15 ZIPs).
  - **NO isWarm #32 dependency** -- the whole belt is z8 (warm), so it resolves on the standard warm path as soon as the fence lands (same as Nevada, unlike the mid-Atlantic/mid-South z7 halves). State this explicitly.
  - Note: dataset side is `<new canonical SHA>`; plant-astro consumes the span + chill band + tree calendars automatically.

- [ ] **Step 2: Commit** (explicit pathspec)

```bash
git add docs/kickoffs/39-utah-dixie-plant-app.md
git status
git commit -m "docs(kickoff): plant-app Utah Dixie REGION_STATES + 847xx ZIP3 fence handoff (#39)"
git show --stat HEAD
```

---

## Task 13: Update memory + close out

- [ ] **Step 1:** Write/update memory `utah-dixie-region-spec` -> SHIPPED (canonical SHA, commit, 111 cells; reusable lessons: **the single-zone build is materially lighter than Nevada** -- no gradient, no early-Feb indoor-start trick (Mar 30 frost makes January naturally inactive), `usu_ext` already catalogued so ~0 new sources; **apple + pear `marginal` is the marquee flip from Nevada**, driven by the county's own elevation-based fruit recommendation, not a mechanical band judge; the county "Fruits" elevation split IS the direct tree-suitability authority; raspberry steer mirrors the pre-existing `warm_arid` text; strawberry a low-elevation thriver; whether the chill-hunt found a real St. George number or the elevation-bracketed band held). Add the MEMORY.md pointer. Cross-link `[[nevada-high-desert-region-spec]]`, `[[onion-daylength-intermediate-a9-window-fit]]`, `[[fall-cycle-deriver-combine-then-split]]`, `[[variety-region-arcs-parallel-safe]]`. Update `[[region-tier2-ruling-pass-outcome]]` if this closes the z8-belt program (only Alaska item 7 remains).
- [ ] **Step 2:** Summarize to Trevor: what shipped, the unpushed commit, the plant-app kickoff (#39 + the 847xx ZIP3 fence + the NO-isWarm-dependency note), and that no plant-astro bump was done. Flag that **Utah is the last z8 belt -- only Alaska (item 7) remains in the region program**, and that per Trevor's 2026-07-22 ruling the **raspberry `berry`-archetype migration is queued directly after Alaska** (memory `variety-region-arcs-parallel-safe`).

---

## Self-Review

**Spec coverage:**
- Product goal (Utah Dixie honest calendars: real heat abort + real Nov frost return) -> Tasks 4-11. ✓
- Roster-wide 111 cells -> Tasks 4-8 enumerate all 111 (warm+cool = 82, 14 trees, 5 citrus, 10 perennials). ✓
- zone_span ["8"] SINGLE zone, A45 single-zone parity (spec §2) -> Global Constraints + Tasks 2, 9-11 (warm_arid shape). ✓
- Frost-anchored Mar 30 / Nov 1, standard deriver, NO early-Feb trick, no new field/gate (spec §3, §4a) -> Global Constraints + Task 4 Step 2 (derive+inspect the natural cold_pause). ✓
- Delta 4a warm=single-spring+heat_pause+no-fall / cool=two-window (spec §4a) -> Tasks 4 + 5. ✓
- Delta 4b apple + pear `marginal` prose-only + county elevation split + pawpaw unsuitable (spec §4b) -> Task 3 (band) + Task 6. ✓
- Delta 4c raspberry marginal fall-bearing steer + strawberry thriver + blueberry alkaline (spec §4c) -> Task 8. ✓
- Chill band {8:[250,450]} + hunt-once-then-flag + provenance flag (spec §5) -> Task 3 Steps 1b + 4. ✓
- Onion A9 watch (intermediate_day, fall-planted) + garlic St. George window (spec §4d) -> Task 5 Steps 2-4 + Task 10 RED-check. ✓
- Class split trees/citrus/herbs/berries (spec §6) -> Tasks 6, 7, 8. ✓
- Sourcing lighter (usu_ext catalogued; 0-or-few new ids) (spec §8) -> Task 3 Step 2. ✓
- Gate ceremony incl A9/A45/chill/calendar_coherence/prose_window_sweep/footprint (spec §7) -> Tasks 10-11. ✓
- State trio + roadmap + register + content review + memory (spec §9) -> Task 11 (Steps 4-6) + Task 13. ✓
- App handoff + 847xx ZIP3 fence + NO isWarm dep (spec §9) -> Task 12. ✓
- Out of scope: no new field/gate/archetype, no plant-astro bump, raspberry-migration-after-Alaska, shallot tensions (spec §10) -> honored. ✓

**Placeholder scan:** authored window VALUES come from Task 3 (sourcing) and are consumed by Tasks 4-8 against the Task 1 template -- the data-authoring analog of "author per spec," not a placeholder; the STRUCTURE, gate loop, deriver commands, and the three deltas' exact content (apple/pear marginal steer + variety list, the county tree split, raspberry steer, band numbers, frost anchors) are concrete. `<slug>`, `<N>`, `<n_src>`, `<new canonical SHA>` are per-item substitutions. The `utah_dixie_sources.json` registration is marked "inspect `usu_ext` granularity, may be `{}`" (Task 3 Step 2), not assumed.

**Type consistency:** `region_harness.py <rid> <span-comma> <staging.json> <slug>` used with `utah_dixie 8` (single-zone span, comma-list of one) consistently (Tasks 4-8, 10-11); `region_cell_audit.audit_cell(slug, cell, region_id) -> list` (Tasks 2, 4-8) + CLI `region_cell_audit.py <rid> <staging...>`; `second_cycle.build_two_cycle_cell(base, spring, fall)` (Task 5); `build_region_promote.py utah_dixie [--base-sha SHA]` reads `STAGING["utah_dixie"]` (5 files + band) + `staging/utah_dixie_sources.json`; `EXPECTED_CELLS["utah_dixie"] == 111`; `annual_calendar.derive_annual_calendar(cell)` (Task 4); staging files are `{slug: cell}` throughout; chill band path `region_chill_delivered.utah_dixie` + provenance (Task 3, matches shipped nevada). ✓

**Open confirm-items flagged, not hidden:** whether the USU pages ride `usu_ext` or need per-pub ids (Task 3 Step 2), the chill-hunt outcome (Task 3 Step 1b -- number found vs elevation-bracketed band), the garlic St. George fall window (Task 5, source the exact dates), the warm-crop fall tail token per crop (Task 4 Step 2 derive+inspect), the exact 847xx ZIP3 fence membership (Task 12, confirm against zip-zones.json), and the concurrent-promote ordering (Task 11 Step 0) are marked "confirm against the real tool / live state / source," not assumed.
