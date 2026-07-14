# Maritime Pacific Northwest Region Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author and certify a real maritime Pacific Northwest region (`pnw`, WA/OR west of the Cascades, z8-9) across all 108 certified region-carrying crops, so the ~750 z8-9 WA/OR ZIPs stop riding generic zone dates that assume a hot summer the maritime PNW does not have.

**Architecture:** PNW is FROST-ANCHORED (the inverse of RGV's frost-free Hawaii shape). Cells reuse each crop's existing frost-anchored region-cell shape (`resolution_method="frost_anchored_resolved"`, real `resolved_from` frost dates, `cold_pause` winters), so `calendar[]` is DERIVED by the standard `tools/annual_calendar.py` from authored windows -- no deriver change, no new gate, no hand-authoring. All 108 `pnw` cells are authored OFF-canonical into per-class staging files, gated per-crop against a scratch canonical (scratch tools with `pnw` patched into `EXPECTED_SPANS`), then promoted in ONE atomic SHA-guarded batch that also adds `pnw` to `EXPECTED_SPANS` + `region_chill_delivered.pnw`. `gate_all` is green before (no `pnw` anywhere) and after (`pnw` everywhere), never mid-flip.

**Tech Stack:** Python 3 standalone gate scripts (`whole_crop_gate.py`, `gate_all.py`, `zone_span_gate.py`, `coverage_floor_gate.py`, `chill_gate.py`, `annual_calendar.py`, `apply_patch.py`), compact JSON canonical, git on `main`.

## Global Constraints

Copied verbatim from the spec + CLAUDE.md; every task's requirements implicitly include these.

- **Canonical JSON is COMPACT:** `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` until the atomic promote (Task 10).** All authoring happens in staging files under `tools/staging/`.
- **TDD: RED before GREEN.** Any new check is adversarially proven on a scratch copy before it is trusted.
- **T1-or-it-doesn't-ship.** Every authored window/verdict cites a Tier-1 source (university `.edu` extension or government agency). WSU (`wsu_ext`) and OSU (`osu_ext`) extension are the primary PNW authorities; new T1 source ids may be catalogued as needed (the rule is about tier, not the existing list). No fabricated precision -- a thin-source crop gets a conservative cell, flagged, never invented.
- **No em dashes in consumer copy** (`region_notes_*`, `suitability_note_*`, `chill_basis_*`, `cold_basis_*`): use commas/colons/semicolons/periods. `--` is fine in docs/commits/code. American English. Temps render as `°F`. "plant" lowercase except at sentence start or "Plant Pro".
- **Zone span `pnw = ["8","9"]`** (maritime WA/OR: z8 dominant Puget/Willamette lowlands, z9 milder coastal pockets). Every `pnw` cell's `resolved_by_zone` keys are EXACTLY `"8"` and `"9"` (A45 parity). The final west-side-vs-east-side ZIP resolution is an APP-side fence (Task 11), not a dataset concern.
- **PNW is FROST-ANCHORED:** `resolution_method="frost_anchored_resolved"`, `resolved_from={"last_frost":<date>,"first_frost":<date>}` (real maritime dates), `calendar[]` DERIVED by `tools/annual_calendar.py` (`calendar_basis="frost_anchored"`). `cold_pause` in winter is EXPECTED and correct. NO summer `heat_pause` for cool-season crops (summer is the growing window).
- **State trio at content release** (Task 10): CURRENT_STATE.md surgical (drift memory `current-state-md-drift`: no `---` separator, hand-maintain), STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session.
- **No plant-astro submodule bump from this session** (memory `plant-astro-bump-owned-by-astro-session`). **Trevor confirms every push.** Don't commit the canonical change until Trevor approves.
- **TWO-SESSION COLLISION RULE -- ACTIVE THIS ARC.** A concurrent **leek variety-pilot session is committing to `main` right now** (commits `6808b37`, `f0516bb`, `b8d4c36` observed 2026-07-14). Tasks 1-9 are all off-canonical (scratch/staging) and collision-SAFE. **Only Task 10 writes the canonical**, and it carries explicit coordination steps: re-read the live canonical SHA at promote time, rebase `sha256_before`, re-run `gate_all` on the ACTUAL current canonical, and do not apply while the leek session holds the canonical open. The atomic SHA-guard is the backstop -- whoever promotes second gets a SHA-mismatch abort and rebases. leek's promote touches `leek.varieties` (disjoint from `*.regions.pnw`), so the two are path-disjoint; only the SHA guard needs rebasing.

## Crop roster (the 108, by class)

Locked from canonical `d0832254` (`verification_status.status == "verified_gs_arc"` AND non-empty `regions`; identical to RGV's roster -- no certifications since):

- **frost_anchored (79):** the annual vegetable + herb roster (broccoli, lettuce-leaf, tomato family, cucurbits, roots, peas, beans, corn, etc.). Enumerate at build via the roster query below.
- **perennial_chill_gated (14):** apple, apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum, pomegranate. **(The PNW flagship -- most FRUIT here.)**
- **perennial_evergreen (5):** grapefruit, lemon, lime, mandarin-clementine, orange-navel. **(Cold-limited in PNW.)**
- **perennial_woody_ornamental (5):** lavender, oregano, rosemary, sage, thyme.
- **berries_woody (4):** blackberry, blueberry, elderberry, raspberry. **(A PNW signature.)**
- **perennial_herbaceous (1):** strawberry.

Roster query (run to get the authoritative per-class lists at build time -- re-run against the LIVE canonical in case leek's promote landed):
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

## File Structure

- `tools/staging/pnw_annuals.json` -- staged `pnw` cells for the 79 frost_anchored crops (`{slug: cell}`).
- `tools/staging/pnw_trees.json` -- staged cells for the 14 chill_gated trees (A3 FRUIT split; flagship fruiting calendars + edge-case verdicts).
- `tools/staging/pnw_citrus.json` -- staged cells for the 5 evergreen citrus (cold-limited verdicts).
- `tools/staging/pnw_perennials.json` -- staged cells for 5 woody herbs + 4 berries + 1 strawberry.
- `tools/staging/pnw_chill_band.json` -- the `region_chill_delivered.pnw` band + provenance (top-level).
- `tools/region_harness.py` -- region-GENERIC off-canonical per-crop gate harness (scratch tools + scratch canonical). Generalized from `rgv_harness.py`; takes a region id + span.
- `tools/test_region_harness.py` -- tests for the generic harness (pnw fixture).
- `tools/region_cell_audit.py` -- region-GENERIC staged-cell anomaly detector. Generalized from `rgv_cell_audit.py`; **frost model per region** (frost-anchored PNW allows `cold_pause`, requires real `resolved_from`).
- `tools/test_region_cell_audit.py` -- tests for the generic auditor.
- `tools/build_region_promote.py` -- region-GENERIC deterministic emitter: staging files -> one SHA-guarded `apply_patch` batch. Generalized from `build_rgv_promote.py`.
- `tools/test_build_region_promote.py` -- tests for the generic emitter.
- `tools/batches/pnw_region_promote.json` -- the atomic promote batch (generated).
- `docs/pnw_cell_contract.md` -- the per-archetype cell template (the column contract).
- `docs/reviews/notes/2026-07-14/pnw_sources.md` -- the T1 sourcing table (crop -> source -> windows).
- `docs/reviews/notes/2026-07-14/pnw_promote_dryrun.md` -- the scratch dry-run record.
- `docs/kickoffs/28-pnw-plant-app-zip3-fence.md` -- the paired plant-app handoff.

The three region-generic tools are NEW files (copy+generalize, leaving the shipped `rgv_*` tools untouched) -- this also avoids colliding with the concurrent leek session touching `tools/`.

---

## Task 1: Lock the cell contract + roster

**Files:**
- Create: `docs/pnw_cell_contract.md`
- Read: `crops_data_final.json` (broccoli `ca_north_coast` + `northern_tier` cells, apple `northern_tier` cell, orange-navel `ca_north_coast`/`se_gulf` cell)

**Interfaces:**
- Produces: `docs/pnw_cell_contract.md` -- the authoritative per-archetype `pnw` cell template that Tasks 4-7 author against.

- [ ] **Step 1: Extract the archetype templates from canonical**

Run:
```bash
python3 -c "
import json
d=json.load(open('crops_data_final.json'))
by={c['slug']:c for c in d['crops']}
for slug,reg in [('broccoli','ca_north_coast'),('broccoli','northern_tier'),('apple','northern_tier'),('orange-navel','ca_north_coast')]:
    r=by[slug]['regions'].get(reg)
    if not r: print('=====',slug,reg,'MISSING'); continue
    print('=====',slug,reg,'=====')
    print('region keys:',list(r.keys()))
    z=sorted(r['resolved_by_zone'])[0]
    print('zone',z,'keys:',list(r['resolved_by_zone'][z].keys()))
    print('resolution_method:',r['resolved_by_zone'][z].get('resolution_method'),'resolved_from:',r['resolved_by_zone'][z].get('resolved_from'))
"
```
Expected: confirms the **frost-anchored** annual cell (`resolution_method="frost_anchored_resolved"`, real `resolved_from` dates, `cold_pause` in winter calendar), the chill-gated tree cell (apple: adds `suitability`, `suitability_note_*`, `chill_basis_*`, `bloom`), and the citrus cell (orange-navel: adds `min_winter_temp_f`, `cold_basis_*`).

- [ ] **Step 2: Write `docs/pnw_cell_contract.md`**

Document, with a full worked JSON example per archetype:

1. **Frost-anchored annual cell** (frost_anchored, 79 crops + the non-tree perennials that carry calendars). Keys: `region_id="pnw"`, `region_label` (final wording below), `zone_span=["8","9"]`, `sources`, `plantings[]`, `resolved_by_zone` (keys `"8"`,`"9"`), `region_notes_beginner`, `region_notes_seasoned`. Each `resolved_by_zone[z]` carries: authored month windows (`plant_out`, `start_indoors` if tray-started, `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`), `calendar[]` (12 tokens, DERIVED via `tools/annual_calendar.py`), **`resolution_method="frost_anchored_resolved"`**, **`resolved_from={"last_frost":<date>,"first_frost":<date>}`** (real maritime dates), optional `second_planting` (author where a real fall cycle exists -- the deriver picks it up), optional `succession_spring`/`succession_fall`/`successions_realized`, `sources`, `anchoring_urls`, `notes`/`zone_notes`/`planting_note` (null unless authored). **NO summer `heat_pause` for cool-season crops** (summer is the growing window; the deriver renders in-season lulls as `growing`). Warm-season crops may carry a T1-backed `heat_pause` ONLY if a genuine summer heat gap is sourced (rare in the maritime PNW; default is no pause).
2. **Tree cell (fruiting)** -- the chill-gated fruit that DO fruit (the PNW flagship). Adds `suitability="fruits_reliably"`, `suitability_note_{seasoned,beginner}`, `bloom`, `chill_basis_{seasoned,beginner}`, region-level `plantings_provenance`; `calendar[]` uses the perennial vocabulary (`prune`/`bloom`/`growing`/`harvest`/`care`/`dormant`). Real bloom + harvest windows.
3. **Tree cell (edge/no-fruit)** -- pomegranate/pawpaw (heat-limited) and any late-ripening caveat crop. `suitability="survives"` / `"marginal"` / `"unsuitable"`, `suitability_note_*` explaining the cool-summer heat limit (NOT a chill limit), minimal/empty `calendar` (A32-exempt for trees; A3 governs).
4. **Citrus cell (cold-limited)** -- the 5 evergreen citrus. `suitability="survives"`/`"unsuitable"`, `min_winter_temp_f`, `cold_basis_{seasoned,beginner}` explaining the maritime PNW is too cold / too heat-poor for reliable citrus even container-protected. A32-exempt.

State the summer rule explicitly: cool-season crops render the summer as `growing` (no `heat_pause`); PNW's honesty for heat-hungry WARM annuals lives in a compressed transplant-anchored calendar + `region_notes_*`, NOT a `suitability` field (annuals have none).

Set `region_label = "Maritime Pacific Northwest: Puget Sound and Willamette Valley"` (final wording; confirm no em dash, American English).

- [ ] **Step 3: Commit**

```bash
git add docs/pnw_cell_contract.md
git commit -m "docs(pnw): per-archetype cell contract for the maritime PNW region column"
```

---

## Task 2: Build the region-generic gate harness + cell auditor

**Files:**
- Create: `tools/region_harness.py`, `tools/test_region_harness.py`
- Create: `tools/region_cell_audit.py`, `tools/test_region_cell_audit.py`
- Read: `tools/rgv_harness.py`, `tools/rgv_cell_audit.py` (the shipped originals to generalize)

**Interfaces:**
- Produces: `region_harness.gate_crop(region_id, span, slug, staged_cells: dict) -> (bool, str)` -- merges `staged_cells` (`{slug: cell}`) onto a scratch canonical, runs the REAL `whole_crop_gate.py` on `slug` via a scratch tools copy that has `region_id` in `EXPECTED_SPANS`, returns `(passed, output)`. Used by Tasks 4-7, 9.
- Produces: `region_harness.build_scratch_tools(dest, region_id, span)`, `region_harness.scratch_canonical(region_id, staged_cells, path)`.
- Produces: `region_cell_audit.audit_cells(region_id, paths) -> int` (issue count) with per-region frost model config. Used by Tasks 4-7, 9, 10.

- [ ] **Step 1: Write the failing test for the harness**

```python
# tools/test_region_harness.py
import json, region_harness

BASE = json.load(open("crops_data_final.json"))
BROC = next(c for c in BASE["crops"] if c["slug"] == "broccoli")
PNW_SPAN = ["8", "9"]

def _valid_pnw_cell():
    # a gate-valid frost-ANCHORED annual cell cloned from broccoli's ca_north_coast cell (z9),
    # re-keyed to the pnw span ["8","9"]
    src_region = BROC["regions"]["ca_north_coast"]
    cell = json.loads(json.dumps(src_region))
    cell["region_id"] = "pnw"
    cell["region_label"] = "Maritime Pacific Northwest: Puget Sound and Willamette Valley"
    cell["zone_span"] = ["8", "9"]
    z0 = sorted(cell["resolved_by_zone"])[0]
    row = cell["resolved_by_zone"][z0]
    cell["resolved_by_zone"] = {"8": json.loads(json.dumps(row)), "9": json.loads(json.dumps(row))}
    return cell

def test_valid_cell_passes():
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {"broccoli": _valid_pnw_cell()})
    assert ok, out

def test_span_key_mismatch_fails():
    cell = _valid_pnw_cell()
    del cell["resolved_by_zone"]["8"]          # span ["8","9"], keys now only ["9"]
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {"broccoli": cell})
    assert not ok and ("A45" in out or "zone_span" in out or "resolved_by_zone" in out), out

def test_missing_pnw_fails_a31():
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {})   # no pnw cell
    assert not ok and "pnw" in out, out
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_region_harness.py -v` (or `python3 test_region_harness.py` if the repo uses standalone asserts -- match the repo convention; check how `test_rgv_harness.py` runs).
Expected: FAIL with `ModuleNotFoundError: region_harness`.

- [ ] **Step 3: Implement `tools/region_harness.py`** (generalized from `rgv_harness.py`)

```python
#!/usr/bin/env python3
"""Region-generic off-canonical per-crop gate harness.

Runs the REAL whole_crop_gate.py on a single crop whose region cell is staged, against a
SCRATCH canonical + a SCRATCH copy of tools/ that has <region_id> in
zone_span_gate.EXPECTED_SPANS. The real canonical + real tools stay untouched until the
atomic promote (Task 10). Generalized from rgv_harness.py (region_id + span params)."""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")

def build_scratch_tools(dest, region_id, span):
    """Copy tools/*.py to dest, patching zone_span_gate.EXPECTED_SPANS to include region_id."""
    os.makedirs(dest, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith(".py"):
            shutil.copy(os.path.join(HERE, fn), os.path.join(dest, fn))
    zsg = os.path.join(dest, "zone_span_gate.py")
    src = open(zsg, encoding="utf-8").read()
    span_lit = ", ".join(f'"{z}"' for z in span)
    patched, n = re.subn(r"(EXPECTED_SPANS = \{\n)",
                         rf'\1    "{region_id}": [{span_lit}],\n', src, count=1)
    assert n == 1, "could not patch EXPECTED_SPANS"
    open(zsg, "w", encoding="utf-8").write(patched)
    return dest

def scratch_canonical(region_id, staged_cells, path):
    """Write CANON with each staged region cell merged into its crop's regions."""
    data = json.load(open(CANON, encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    for slug, cell in staged_cells.items():
        by[slug].setdefault("regions", {})[region_id] = cell
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    return path

def gate_crop(region_id, span, slug, staged_cells):
    """Return (passed, output) from running whole_crop_gate on slug in a scratch env."""
    with tempfile.TemporaryDirectory() as tmp:
        tools = build_scratch_tools(os.path.join(tmp, "tools"), region_id, span)
        canon = scratch_canonical(region_id, staged_cells, os.path.join(tmp, "canon.json"))
        r = subprocess.run([sys.executable, os.path.join(tools, "whole_crop_gate.py"), slug, canon],
                           capture_output=True, text=True)
        out = r.stdout + r.stderr
        # match whole_crop_gate's real success signal (confirm in Step 4 -- it may just be exit 0)
        return (r.returncode == 0, out)

if __name__ == "__main__":
    # smoke: region_harness.py <region_id> <z1,z2> <staging.json> <slug>
    rid, span = sys.argv[1], sys.argv[2].split(",")
    staged = json.load(open(sys.argv[3], encoding="utf-8"))
    slug = sys.argv[4]
    ok, out = gate_crop(rid, span, slug, {slug: staged[slug]})
    print(out); sys.exit(0 if ok else 1)
```
Note: confirm `whole_crop_gate.py`'s actual success signal in Step 4 (inspect real output). If it exits non-zero on any violation, `r.returncode == 0` is the whole signal (as written). If it always exits 0 and prints a verdict, add the `"PASS"`/`"FAIL"` string check that `rgv_harness.py` used.

- [ ] **Step 4: Run harness tests to verify they pass**

Run: `cd tools && python3 -m pytest test_region_harness.py -v`
Expected: 3 passed. If `test_valid_cell_passes` fails on a gate unrelated to the region (e.g. a ca_north_coast-cloned window tripping a coherence gate), fix the `_valid_pnw_cell` fixture to be genuinely valid -- the harness is correct; the fixture must be a clean cell.

- [ ] **Step 5: Write the failing test for the auditor**

```python
# tools/test_region_cell_audit.py
import json, region_cell_audit as rca

def _pnw_annual_cell():
    return {
        "region_id": "pnw",
        "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
        "zone_span": ["8", "9"],
        "resolved_by_zone": {
            z: {"plant_out": "Apr 1 - Jun 30", "harvest": "Jul 1 - Sep 30",
                "harvest_start": "Jul 1", "harvest_end": "Sep 30",
                "first_plant_date": "Apr 1", "last_plant_date": "Jun 30",
                "resolution_method": "frost_anchored_resolved",
                "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1"},
                "calendar": ["cold_pause","cold_pause","cold_pause","plant","plant","plant",
                             "harvest","harvest","harvest","growing","cold_pause","cold_pause"]}
            for z in ("8", "9")}}

def test_valid_frost_anchored_cell_clean():
    assert rca.audit_cell("broccoli", _pnw_annual_cell(), "pnw") == []

def test_cold_pause_allowed_for_frost_anchored():
    # the RGV auditor forbade cold_pause; the pnw (frost-anchored) auditor must ALLOW it
    cell = _pnw_annual_cell()
    assert not any("cold_pause" in v for v in rca.audit_cell("broccoli", cell, "pnw"))

def test_frost_free_resolution_method_flagged_for_pnw():
    cell = _pnw_annual_cell()
    for z in cell["resolved_by_zone"].values():
        z["resolution_method"] = "month_resolved_frost_free"
        z["resolved_from"] = {"last_frost": None, "first_frost": None}
    v = rca.audit_cell("broccoli", cell, "pnw")
    assert any("resolution_method" in x or "resolved_from" in x for x in v), v

def test_emdash_flagged():
    cell = _pnw_annual_cell()
    cell["region_notes_seasoned"] = "cool summers — long season"
    assert any("em dash" in x.lower() or "—" in x for x in rca.audit_cell("broccoli", cell, "pnw"))
```

- [ ] **Step 6: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -v`
Expected: FAIL (`region_cell_audit` missing).

- [ ] **Step 7: Implement `tools/region_cell_audit.py`** (generalized from `rgv_cell_audit.py`)

Copy `rgv_cell_audit.py` to `region_cell_audit.py` and generalize. Add a per-region config and flip the frost-model checks:

```python
# region config: the shape each region's cells must obey
REGION_CONFIG = {
    "rgv": {"label": "Rio Grande Valley: Subtropical South Texas",
            "span": ["9", "10"], "frost_model": "free"},
    "pnw": {"label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
            "span": ["8", "9"], "frost_model": "anchored"},
}
```

In `audit_cell(slug, cell, region_id)`, replace the RGV-hardcoded checks with config-driven ones:
- `cell["region_id"] == region_id`; `cell["zone_span"] == cfg["span"]`; `resolved_by_zone` keys == `set(cfg["span"])`.
- `region_label == cfg["label"]`.
- **Frost model branch:**
  - `frost_model == "free"` (RGV behavior, unchanged): `resolution_method` must be frost-FREE (`*_frost_free`); `resolved_from` nulls; **`cold_pause` in any calendar is an ERROR**.
  - `frost_model == "anchored"` (PNW): `resolution_method == "frost_anchored_resolved"`; `resolved_from` must have NON-null `last_frost` AND `first_frost`; **`cold_pause` is ALLOWED** (skip the cold_pause error entirely).
- Keep unchanged (both models): em-dash walk on consumer copy, 12-token calendars in `CAL_VOCAB`, no stray `lifted_from_zone`, the in-ground-month-tokened-`season_over` check, the start_indoors-month-tokened-`season_over` check, citation id->URL misattribution check.

Provide `audit_cells(region_id, paths) -> int` that loads each staging file (`{slug: cell}`), runs `audit_cell(slug, cell, region_id)`, prints issues, returns the total count. CLI: `region_cell_audit.py <region_id> <staging.json> [...]`, exit 1 if any issue.

- [ ] **Step 8: Run auditor tests to verify they pass**

Run: `cd tools && python3 -m pytest test_region_cell_audit.py -v`
Expected: 4 passed (cold_pause allowed for anchored; frost-free method flagged; em dash caught; valid cell clean).

- [ ] **Step 9: RED-check the generalization did not break RGV** (regression guard)

Run the generalized auditor against the shipped RGV staging (if retained) OR construct a minimal rgv cell fixture and confirm `frost_model=="free"` still forbids cold_pause. This proves the generalization preserved RGV behavior.

- [ ] **Step 10: Commit**

```bash
git add tools/region_harness.py tools/test_region_harness.py tools/region_cell_audit.py tools/test_region_cell_audit.py
git commit -m "test(pnw): region-generic gate harness + cell auditor (frost-anchored model; cold_pause allowed)"
```

---

## Task 3: T1 sourcing pass (WSU/OSU) + the chill band

**Files:**
- Create: `docs/reviews/notes/2026-07-14/pnw_sources.md`
- Create: `tools/staging/pnw_chill_band.json`

**Interfaces:**
- Produces: the sourcing table (crop/class -> T1 source id + url + month windows + frost dates) that Tasks 4-7 author from.
- Produces: `region_chill_delivered.pnw` band + provenance (drives A3 in Task 5).

- [ ] **Step 1: Web-research the T1 sources, by class**

Use WebSearch/WebFetch. Target WSU Extension (and the WSU Master Gardener / "Home Garden" series) and OSU Extension (OSU Master Gardener; the OSU "Vegetable Planting Calendar for the Willamette Valley" EM-series is a strong month-by-month table):
- Annuals: WSU / OSU maritime-PNW (west-of-the-Cascades) vegetable planting-calendar tables (sow indoors / transplant / direct-sow / harvest, by month). The Willamette Valley + Puget Sound lowland tables.
- Tree fruit: WSU / OSU home-orchard + tree-fruit-for-western-WA/OR guidance (bloom + harvest windows for apple/pear/cherry/plum/etc.; the maritime chill-hour figure).
- Berries + strawberry: WSU / OSU caneberry (raspberry/blackberry), blueberry, and strawberry-for-the-maritime-PNW guidance.
- Frost dates + chill band: WSU / OSU / NWS maritime frost-date normals (Puget/Willamette lowlands) and chill-accumulation data, **in a chill model comparable to the existing `region_chill_delivered` table** (see Step 3).

Record each as: source id (reuse/catalog `wsu_ext`, `osu_ext`, or a specific publication id), url, verified date `2026-07-14`, the crop windows it supports, and the frost dates. Confirm each is T1 (`.edu`/`.gov`). Flag any class where T1 windows are thin (that crop gets a conservative cell in its authoring task).

**PDF-extraction gotcha (RGV lesson):** extract calendar tables in THIS controller env with `pypdf`; subagent sandboxes block network/PDF tooling. If a source is a PDF table, fetch + extract here, paste the extracted rows into the sources note.

- [ ] **Step 2: Write the sourcing table**

Write `docs/reviews/notes/2026-07-14/pnw_sources.md` -- a table `crop_or_class | source_id | url | windows | frost_dates | tier | notes`. This is the single source of truth Tasks 4-7 cite. Include a top block with the z8 and z9 maritime frost-date normals (last_frost / first_frost) that every annual cell's `resolved_from` uses.

- [ ] **Step 3: Author the chill band**

From the WSU/OSU maritime chill-hour figure, write `tools/staging/pnw_chill_band.json`:
```json
{
  "region_chill_delivered.pnw": {"8": [<lo>, <hi>], "9": [<lo>, <hi>]},
  "region_chill_delivered_provenance.pnw": "<sourced note: the maritime PNW banks ~X chill hours; WSU/OSU; url; verified 2026-07-14>"
}
```
Reconcile the model to the existing table's neighbors (`northern_tier` z3 `[1000,1600]`, z7 `[700,1200]`; `ca_interior` z8 `[500,1100]`; `se_gulf` z8 `[650,1000]`). The maritime PNW clears the ~600-1000 hr fruiting threshold comfortably; the band is substantial (order of magnitude far above RGV's `[0,300]`). Verify against `chill_gate.py`'s shape (region -> {zone -> [lo,hi]}, numeric, lo<=hi). z8 (colder lowland winter) >= z9 (milder coastal) by low-bound.

- [ ] **Step 4: Commit**

```bash
git add docs/reviews/notes/2026-07-14/pnw_sources.md tools/staging/pnw_chill_band.json
git commit -m "docs(pnw): T1 sourcing table + region_chill_delivered.pnw band (WSU/OSU)"
```

---

## Task 4: Author the 79 frost_anchored annual cells

**Files:**
- Create: `tools/staging/pnw_annuals.json` (`{slug: pnw_cell}` for the 79 annuals)

**Interfaces:**
- Consumes: `docs/pnw_cell_contract.md` (annual template), `docs/reviews/notes/2026-07-14/pnw_sources.md`, `region_harness.gate_crop`, `region_cell_audit`.
- Produces: `tools/staging/pnw_annuals.json`.

This task is subagent-parallelizable: one worker per crop (or per family), each returning its crop's `pnw` cell as JSON. Author against the annual template. **Per-crop procedure (repeat for all 79):**

- [ ] **Step 1: Author the cell for crop `<slug>`**

Read the crop's existing `ca_north_coast` (cool-summer coastal analog) and `northern_tier` cells for `plantings[]` track structure (spring/fall/succession) and DTM. Author the `pnw` cell:
- `region_id="pnw"`, `region_label="Maritime Pacific Northwest: Puget Sound and Willamette Valley"`, `zone_span=["8","9"]`.
- **Season character (NOT the RGV inversion):** summer is the growing window. **Cool-season crop** (brassica, green, root, pea, cool herb) -> a long spring-through-fall run; author overwintering windows where the crop overwinters in the mild maritime winter; **no summer `heat_pause`** (the deriver renders the mid-season as `growing`). **Warm-season crop** (tomato, pepper, eggplant, melon, corn, squash, cucumber, okra, sweet potato) -> a transplant-anchored, compressed window (start indoors well ahead, set out after last frost, harvest before the cool fall); for the heat-hungry ones (melon, okra, sweet potato, long-season pepper) author the honest marginality in `region_notes_*` + a conservative short window, NOT an optimistic hot-summer calendar.
- `resolved_by_zone` keys `"8"` and `"9"` (z8 = colder lowland; z9 = milder coastal). Use the z8 / z9 frost-date normals from the sources note in `resolved_from`. If the WSU/OSU source does not distinguish z8 vs z9, author z8 == z9 windows and note it (honest: one maritime calendar), OR shift z9 slightly earlier/later per the milder frost dates if sourced.
- **`resolution_method="frost_anchored_resolved"`**, **`resolved_from={"last_frost":<z-date>,"first_frost":<z-date>}`**.
- Author `second_planting` where the crop has a real maritime fall cycle (the deriver picks it up; see the broccoli `ca_north_coast` example).
- Dual-register `region_notes_{beginner,seasoned}` in the beefsteak-tomato voice (no em dashes).
- Cite the WSU/OSU source id in `sources` + `anchoring_urls` (verified 2026-07-14).

- [ ] **Step 2: Derive the `calendar[]`**

```bash
python3 -c "
import json,sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell=json.load(open('tools/staging/pnw_annuals.json'))['<slug>']['resolved_by_zone']['8']
print(derive_annual_calendar(cell))
"
```
Set each zone's `calendar[]` to the derived 12-token array. Expected: `cold_pause` winter, `plant`/`harvest`/`growing` through the warm season, no spurious `heat_pause` for cool crops.

- [ ] **Step 3: Gate the crop in isolation**

Run: `python3 tools/region_harness.py pnw 8,9 tools/staging/pnw_annuals.json <slug>`
Expected: PASS (A45 parity on `["8","9"]`, A31/A32 satisfied, calendar coherence clean, 0 em dashes, sources T1).

- [ ] **Step 4: Audit the cell.** Run `python3 tools/region_cell_audit.py pnw tools/staging/pnw_annuals.json` (or the single-slug subset) -- expect 0 issues. Fix + re-gate until PASS + clean audit. Common failures: A24/A25 token placement (a pause on an active window), A32 empty calendar, em dash in notes, span/key mismatch, frost-anchored `resolved_from` left null.

- [ ] **Step 5: Commit the batch** (after all 79 pass)

```bash
git add tools/staging/pnw_annuals.json
git commit -m "feat(pnw): author 79 frost_anchored annual PNW cells (summer growing window, WSU/OSU)"
```

---

## Task 5: Author the 14 chill_gated tree cells (A3 FRUIT split -- the flagship)

**Files:**
- Create: `tools/staging/pnw_trees.json` (`{slug: pnw_cell}` for the 14 chill_gated trees)

**Interfaces:**
- Consumes: `docs/pnw_cell_contract.md` (tree templates), `docs/reviews/notes/2026-07-14/pnw_sources.md`, `tools/staging/pnw_chill_band.json` (the delivered band), `region_harness.gate_crop`.
- Produces: `tools/staging/pnw_trees.json`.

The PNW flagship. The A3 split runs the delivered `pnw` chill band against each crop's stated chill requirement -- and the maritime PNW clears it, so most FRUIT (the inverse of RGV).

- [ ] **Step 1: Author each tree cell** against the tree template. Read the crop's existing `northern_tier` tree cell for the fruiting-cell shape.
  - **Fruiting set** (apple, pear-european, pear-asian, cherry-sweet, cherry-sour, plum, apricot, nectarine, peach, fig, mulberry, persimmon): `suitability="fruits_reliably"`, real `bloom` + `harvest` windows from WSU/OSU, `chill_basis_{seasoned,beginner}` stating the delivered band vs the crop's requirement. Note any cool-summer ripening caveat where sourced (late-ripening peach/fig in the coolest sites) in `suitability_note_*` without downgrading the verdict if WSU/OSU confirm reliable fruit.
  - **Edge cases** (pomegranate, pawpaw): `suitability="survives"`/`"marginal"`/`"unsuitable"` per WSU/OSU -- these are HEAT-limited (cool summers), not chill-limited. `suitability_note_*` explains the summer-heat limit. Minimal/empty calendar (A32-exempt).
- [ ] **Step 2: Gate each crop** via `python3 tools/region_harness.py pnw 8,9 tools/staging/pnw_trees.json <slug>` -> PASS. Confirm A3 (`perennial_gate`) coheres: `fruits_reliably` only where the delivered band >= requirement. Audit via `region_cell_audit`.
- [ ] **Step 3: Commit**

```bash
git add tools/staging/pnw_trees.json
git commit -m "feat(pnw): author 14 chill_gated tree cells (A3 FRUIT split; flagship, WSU/OSU)"
```

---

## Task 6: Author the 5 citrus cells (cold-limited)

**Files:**
- Create: `tools/staging/pnw_citrus.json` (`{slug: pnw_cell}` for grapefruit, lemon, lime, mandarin-clementine, orange-navel)

**Interfaces:**
- Consumes: `docs/pnw_cell_contract.md` (citrus template), `region_harness.gate_crop`.
- Produces: `tools/staging/pnw_citrus.json`.

The reverse of RGV: the maritime PNW is too cold / too heat-poor for reliable citrus.

- [ ] **Step 1: Author each citrus cell** against the citrus template. Read the crop's existing `northern_tier`/`ca_north_coast` citrus cell shape. `suitability="survives"` (container-protected) or `"unsuitable"` per WSU/OSU; `min_winter_temp_f`; `cold_basis_{seasoned,beginner}` explaining the cold/heat limit honestly (even the hardiest, e.g. a container Meyer lemon or a cold-hardy mandarin, is marginal west of the Cascades and needs winter protection). A32-exempt; minimal calendar.
- [ ] **Step 2: Gate each** via `python3 tools/region_harness.py pnw 8,9 tools/staging/pnw_citrus.json <slug>` -> PASS; A3 coheres (no `fruits_reliably`). Audit via `region_cell_audit`.
- [ ] **Step 3: Commit**

```bash
git add tools/staging/pnw_citrus.json
git commit -m "feat(pnw): author 5 citrus cells (cold-limited survives/unsuitable, WSU/OSU)"
```

---

## Task 7: Author the 10 remaining perennials (woody herbs + berries + strawberry)

**Files:**
- Create: `tools/staging/pnw_perennials.json` (`{slug: pnw_cell}` for 5 woody herbs + 4 berries + 1 strawberry)

**Interfaces:**
- Consumes: `docs/pnw_cell_contract.md`, `docs/reviews/notes/2026-07-14/pnw_sources.md`, `region_harness.gate_crop`.
- Produces: `tools/staging/pnw_perennials.json`.

All frost-anchored calendar cells (A32 applies -- real calendars required).

- [ ] **Step 1: Author each cell.**
  - **Woody herbs (lavender, oregano, rosemary, sage, thyme):** real frost-anchored calendars. **Lavender THRIVES** (the maritime rain-shadow, e.g. Sequim, is prime lavender country) -- a strength note, the inverse of RGV's humidity-struggle. Rosemary/oregano/sage/thyme grow well with a cold-edge note for the coldest z8 (rosemary may need protection in a hard z8 winter -- source it).
  - **Berries (blackberry, blueberry, elderberry, raspberry):** a PNW signature. Real calendars + strong suitability notes: raspberry (WA is the #1 US red-raspberry state), blueberry (premier region -- acidic soils + chill), blackberry (marionberry an OR-bred cultivar; note the invasive-Himalayan caveat only if WSU/OSU frame it), elderberry (native/adaptable). Berries carry no `suitability` field (A32 forces a calendar), so the strength framing lives in `region_notes_*`.
  - **Strawberry:** real frost-anchored calendar (spring plant -> summer harvest; June-bearing PNW berries are strong).
- [ ] **Step 2: Gate each** via `python3 tools/region_harness.py pnw 8,9 tools/staging/pnw_perennials.json <slug>` -> PASS. Audit via `region_cell_audit`.
- [ ] **Step 3: Commit**

```bash
git add tools/staging/pnw_perennials.json
git commit -m "feat(pnw): author 10 perennial cells (woody herbs + berries + strawberry, WSU/OSU)"
```

---

## Task 8: Build the atomic promote batch

**Files:**
- Create: `tools/build_region_promote.py`, `tools/test_build_region_promote.py`
- Create: `tools/batches/pnw_region_promote.json` (generated)

**Interfaces:**
- Consumes: the four `tools/staging/pnw_*.json` cell files + `tools/staging/pnw_chill_band.json`.
- Produces: `tools/batches/pnw_region_promote.json` -- an `apply_patch` batch adding, per crop, `$.crops[slug].regions.pnw` (op `add`), plus the top-level `region_chill_delivered.pnw` + provenance. **Note:** `EXPECTED_SPANS.pnw` is a CODE edit to `tools/zone_span_gate.py` (Task 10 Step 1), applied in the same commit as the batch, NOT part of the JSON batch.

- [ ] **Step 1: Write the failing test**

```python
# tools/test_build_region_promote.py
import json, subprocess, sys
def test_pnw_batch_covers_108_plus_topcell():
    subprocess.run([sys.executable, "tools/build_region_promote.py", "pnw"], check=True)
    batch = json.load(open("tools/batches/pnw_region_promote.json"))
    ops = batch["ops"] if isinstance(batch, dict) else batch
    pnw_cells = [o for o in ops if o["json_path"].endswith(".regions.pnw")]
    assert len(pnw_cells) == 108, len(pnw_cells)
    assert any("region_chill_delivered" in o["json_path"] and o["json_path"].endswith(".pnw") for o in ops)
    assert all(o["op"] == "add" for o in ops)   # pnw is net-new everywhere
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -v`
Expected: FAIL (`build_region_promote.py` missing).

- [ ] **Step 3: Implement `tools/build_region_promote.py`** (generalized from `build_rgv_promote.py`)

```python
#!/usr/bin/env python3
"""Emit the atomic region-column promote batch from the staging files. Deterministic;
no canonical write. Usage: build_region_promote.py <region_id>. Generalized from
build_rgv_promote.py (region_id param + region-keyed staging files)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STAGING = {  # region_id -> (cell-staging files, chill-band file)
    "pnw": (["pnw_annuals.json", "pnw_trees.json", "pnw_citrus.json", "pnw_perennials.json"],
            "pnw_chill_band.json"),
}

def main(region_id):
    cell_files, band_file = STAGING[region_id]
    ops, seen = [], set()
    for fn in cell_files:
        for slug, cell in json.load(open(os.path.join(HERE, "staging", fn), encoding="utf-8")).items():
            assert slug not in seen, f"duplicate {slug}"
            seen.add(slug)
            ops.append({"op": "add", "json_path": f"$.crops[?slug={slug}].regions.{region_id}", "value": cell})
    band = json.load(open(os.path.join(HERE, "staging", band_file), encoding="utf-8"))
    for path, value in band.items():
        ops.append({"op": "add", "json_path": "$." + path, "value": value})
    assert len(seen) == 108, f"expected 108 crops, got {len(seen)}"
    out = {"sha256_before": None, "ops": ops}   # fill sha256_before at apply time
    with open(os.path.join(HERE, "batches", f"{region_id}_region_promote.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)   # the BATCH file may be pretty; canonical stays compact
    print(f"emitted {len(ops)} ops ({len(seen)} {region_id} cells + {len(band)} top-level)")

if __name__ == "__main__":
    main(sys.argv[1])
```
Confirm the `json_path` slug-selector syntax against `tools/apply_patch.py` (`normalize_path`/`tokenize`) and the shipped `tools/batches/rgv_region_promote.json` -- match their exact path form (`$.crops[?slug=...]` vs a numeric index vs `[?slug=...]`; copy whatever RGV's shipped batch used).

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools && python3 -m pytest test_build_region_promote.py -v`
Expected: PASS (108 pnw cells + the chill-band ops; all `add`).

- [ ] **Step 5: Commit** (batch generator + generated batch; canonical still untouched)

```bash
git add tools/build_region_promote.py tools/test_build_region_promote.py tools/batches/pnw_region_promote.json
git commit -m "feat(pnw): deterministic atomic-promote batch emitter (108 cells + chill band)"
```

---

## Task 9: Dry-run the promote on a scratch copy (full gate ceremony, RED-checked)

**Files:**
- Modify (scratch only): a copy of `crops_data_final.json` + `tools/zone_span_gate.py`
- Create: `docs/reviews/notes/2026-07-14/pnw_promote_dryrun.md`

**Interfaces:**
- Consumes: `tools/batches/pnw_region_promote.json`, `region_harness.build_scratch_tools`, `region_cell_audit`.
- Produces: proof that the full suite is green post-promote before touching the real canonical.

- [ ] **Step 1: Apply the batch to a scratch canonical.** Compute `sha256_before` from the real file, apply via `tools/apply_patch.py` to a COPY, confirm COMPACT + count 125 + footprint = exactly 108 `regions.pnw` + the top-level `region_chill_delivered.pnw` + provenance via a byte-diff audit (no other key touched).

- [ ] **Step 2: Add `pnw` to a scratch `EXPECTED_SPANS`** (via `region_harness.build_scratch_tools(dest, "pnw", ["8","9"])`) and run the full suite against the scratch canonical + scratch tools:
  - `gate_all.py` -> 116/116.
  - `zone_span_gate.py` (A45) -> 0.
  - `coverage_floor_gate.py` (A31/A32) -> 0 (all 108 carry `pnw`).
  - `chill_gate.py` -> 0.
  - `whole_crop_gate.py` on a per-class sample (broccoli, apple, peach, pomegranate, orange-navel, blueberry, lavender, strawberry) -> PASS.
  - `region_cell_audit.py pnw` over all four staging files -> 0 issues.
  - `release_verify.py` -> clean modulo the documented roster-wide section-A collateral (the pre-commit backstop is the binding multi-crop gate).

- [ ] **Step 3: RED-check the promote** -- stage an intentionally-broken cell (drop the `"8"` key from one crop's pnw cell on the scratch copy) and confirm A45 bounces it; restore. Also flip one fruiting tree's delivered-vs-required so A3 should object, confirm it does, restore. This proves the ceremony catches the span-parity + fruit-split defect classes at roster scale.

- [ ] **Step 4: Record the dry-run result** in `docs/reviews/notes/2026-07-14/pnw_promote_dryrun.md` (gate outputs + footprint audit + the RED-check results). Commit.

```bash
git add docs/reviews/notes/2026-07-14/pnw_promote_dryrun.md
git commit -m "test(pnw): scratch-copy promote dry-run green + A45/A3 RED-check"
```

---

## Task 10: Promote to canonical + release ceremony (THE one canonical write)

**Files:**
- Modify: `crops_data_final.json` (the atomic promote)
- Modify: `tools/zone_span_gate.py` (add `pnw` to `EXPECTED_SPANS`)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`
- Modify: `docs/region_coverage_roadmap.md`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 0: CONCURRENCY COORDINATION (leek session).** Before touching the canonical:
  - `git fetch` + `git log --oneline origin/main..main` and `git log -1 crops_data_final.json` -- determine whether the leek session has promoted since `d0832254`.
  - Re-read the LIVE canonical SHA: `shasum -a 256 crops_data_final.json`. If it is no longer `d0832254`, the leek promote landed. That is FINE (leek touches `leek.varieties`, disjoint from `*.regions.pnw`), but you MUST: (a) re-run the roster query (Roster section) against the live canonical to confirm still 108 region-carrying certified; (b) re-run each staging file through `region_harness` against the live canonical (the harness reads the live file) to confirm all cells still gate green; (c) use the LIVE SHA as `sha256_before` in Step 2.
  - Confirm the leek session is NOT mid-promote (its plan holds the canonical open only during its own atomic write). If in doubt, coordinate with Trevor before proceeding. Do NOT both hold the canonical open at once (the sweet-corn collision rule).

- [ ] **Step 1: Add `pnw` to the REAL `tools/zone_span_gate.py` `EXPECTED_SPANS`** (`"pnw": ["8","9"]`). `coverage_floor_gate` auto-derives its `CANONICAL_REGIONS`/`CANONICAL_ZONES`.

- [ ] **Step 2: Apply the batch to the REAL canonical** via `tools/apply_patch.py` with the real `sha256_before` (the LIVE SHA from Step 0). Confirm COMPACT, no trailing newline, count 125.

- [ ] **Step 3: Full release verification** (protocol #6):
  - `python3 tools/whole_crop_gate.py <slug>` on the 18 gold anchors -> 18/18 PASS.
  - `python3 tools/gate_all.py` -> 116/116.
  - `python3 tools/zone_span_gate.py` (A45), `coverage_floor_gate.py` (A31/A32), `chill_gate.py` -> 0.
  - `python3 tools/release_verify.py` -> clean (modulo documented roster-wide section-A collateral).
  - `python3 tools/region_cell_audit.py pnw tools/staging/pnw_*.json` -> 0.
  - Independent footprint audit: exactly 108 `regions.pnw` + `region_chill_delivered.pnw` + provenance changed; all else byte-identical.
  - The **pre-commit backstop** (`precommit_release_verify.py`) runs on commit -- checks ALL changed crops (watch the 9 uncertified shells: `coverage_floor` standalone will read the shells only, ~89, benign as in RGV; `gate_all`'s certified-only view is authoritative).
  - Per-batch source-truth sample: re-verify 3-4 authored windows against their cited WSU/OSU URLs.

- [ ] **Step 4: State trio** -- surgically update CURRENT_STATE.md (drift memory `current-state-md-drift`: hand-maintain, no `---`), prepend STATE_HISTORY.md (most-recent-first), bump LATEST.txt (new SHA + session line).

- [ ] **Step 5: Roadmap + register** -- mark roadmap item 4 SHIPPED; add a `docs/field_addition_register.md` row for the PNW region column.

- [ ] **Step 6: Commit** (UNPUSHED -- Trevor confirms push)

```bash
git add crops_data_final.json tools/zone_span_gate.py CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/region_coverage_roadmap.md docs/field_addition_register.md
git commit -m "feat(pnw): certify the maritime Pacific Northwest region across 108 crops"
```

---

## Task 11: Write the paired plant-app kickoff

**Files:**
- Create: `docs/kickoffs/28-pnw-plant-app-zip3-fence.md`

**Interfaces:**
- Produces: the handoff so plant-app can route the maritime WA/OR ZIPs to `pnw`.

- [ ] **Step 1: Write the kickoff** covering:
  - `REGION_STATES`: map `pnw` -> WA, OR.
  - **The west-side ZIP3 fence** (the mirror of RGV's 785xx fence): fence `pnw` to the maritime WEST-of-the-Cascades ZIP3s so hot-dry EAST-side z8 pockets (Spokane 990-992, Columbia Basin, and OR east of the Cascades) do NOT resolve to a maritime calendar. Derive the exact west-side ZIP3 allow-list (or the east-side deny-list) from `zip-zones.json`; if the east-side z8 ZIPs already have a better home (warm_arid adjacency), route them there. This is the confirm-item from spec 4.1.
  - `zone_span` confirm: `pnw` spans z8 + z9; the dataset carries both zone rows.
  - Verify the `regions.json` sync path picks up the new `pnw` region.
  - Note: dataset side is `<new canonical SHA>`; plant-astro consumes spans + chill band + the tree fruit calendars automatically.
  - Reference the RGV app kickoff (`docs/kickoffs/26-rgv-plant-app-zip3-fence.md`) as the proven template + the pipeline pilot.

- [ ] **Step 2: Commit**

```bash
git add docs/kickoffs/28-pnw-plant-app-zip3-fence.md
git commit -m "docs(kickoff): plant-app PNW west-side ZIP3 fence + REGION_STATES handoff (#28)"
```

---

## Task 12: Update memory + close out

- [ ] **Step 1:** Write memory `maritime-pnw-region` (SHIPPED, canonical SHA, 108 cells, reusable lessons: **frost-ANCHORED reuse of the standard deriver (the inverse of RGV's frost-free hand-authoring) -- the biggest de-risk**; the A45/A31 pincer -> atomic promote; the A3 FRUIT flip; the region-generic tooling generalization; the cold_pause auditor relaxation; the concurrent-leek coordination). Add the MEMORY.md pointer.
- [ ] **Step 2:** Coordinate the leek pilot's base-SHA: if leek has NOT yet promoted, its plan must rebase its base SHA onto the new PNW canonical (its promote then re-verifies its single-crop footprint against a canonical that now carries `pnw` everywhere, including on `leek`). Leave a note in the leek plan / memory `leek-variety-hardiness-archetype-ready`. If leek promoted FIRST, this arc already rebased onto it in Task 10 Step 0.
- [ ] **Step 3:** Summarize to Trevor: what shipped, the unpushed commit, the plant-app kickoff owed (#28), and that no plant-astro bump was done.

---

## Self-Review

**Spec coverage:**
- Product goal (maritime WA/OR honest calendars) -> Tasks 4-10. ✓
- Option A full roster-wide (108) -> Tasks 4-7 enumerate all 108 (79+14+5+5+4+1). ✓
- Frost-ANCHORED model + standard deriver (spec §4.2) -> Task 1 contract + Task 4 cells + Global Constraints. ✓
- zone_span ["8","9"] (spec §4.1) -> Global Constraints; east-side fence -> Task 11 (app-side). ✓
- region_chill_delivered.pnw substantial band + A3 FRUIT flip (spec §4.5, §5) -> Task 3 + Task 5. ✓
- Chill-gated trees the flagship / citrus cold-limited / berries+lavender strengths (spec §5) -> Tasks 5, 6, 7. ✓
- Sourcing T1 WSU/OSU (spec §6) -> Task 3. ✓
- Toolchain parametrized + cold_pause relaxed for pnw (spec §7) -> Task 2. ✓
- Atomic promote (A45/A31 pincer) (spec §7) -> Tasks 8-10. ✓
- Gate surface, no new gate (spec §8) -> Tasks 9-10 (no task adds a gate). ✓
- App handoff (west-side fence) (spec §9) -> Task 11. ✓
- State trio + roadmap + register + memory (spec §12) -> Tasks 10, 12. ✓
- Concurrency (spec §11 risk) -> Global Constraints + Task 10 Step 0 + Task 12 Step 2. ✓
- Non-goals (no app edits, no astro bump, no new gate, no variety work) -> honored. ✓

**Placeholder scan:** authored window VALUES are produced by Task 3 (sourcing) and consumed by Tasks 4-7 against the Task 1 template -- the data-authoring analog of "implement per spec," not a placeholder; the STRUCTURE and gate loop are fully concrete. `<slug>`, `<lo>/<hi>`, `<z-date>`, `<new canonical SHA>` are per-item substitutions, not TODOs. The chill-band numbers + frost dates are explicitly sourcing tasks (Task 3) with a stated method, flagged in the spec as build-time, not hidden.

**Type consistency:** `gate_crop(region_id, span, slug, staged_cells) -> (bool, str)` used consistently in Tasks 2/4/5/6/7/9; `audit_cell(slug, cell, region_id) -> list` / `audit_cells(region_id, paths) -> int` consistent in Tasks 2/4-7/9/10; staging files are `{slug: cell}` throughout; `build_region_promote.py <region_id>` reads exactly the four staging files + the chill band. ✓

**Open confirm-items flagged, not hidden:** the `apply_patch` `json_path` selector syntax (Task 8 Step 3), the `whole_crop_gate` success predicate (Task 2 Step 3), and the leek promote ordering (Task 10 Step 0) are marked "confirm against the real tool / live state" rather than assumed.
