# Onion Variety Pilot (Photoperiod Archetype) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Intended to run in a FRESH session; start by reading the memory `onion-variety-pilot-photoperiod` + the spec.

**Goal:** Add the `photoperiod_annual` archetype to the archetype-dispatched `variety_detail_gate`, and enrich onion's 6 varieties to the flat schema (per-variety `days_to_maturity` + `day_length_type`) so the app can show the right onions per latitude with full variety detail.

**Architecture:** Onion is the third variety archetype (after dry-bean `annual_dtm` and apple `tree_fruit`). It is a DTM annual that ALSO carries a day-length class, so its archetype block = the shared DTM machinery + one distinctive field (`day_length_type`) + `use`. The gate refactor is a small 3-way dispatch; the day-length-vs-region honesty already exists in the A9 `photoperiod_gate` and is NOT duplicated. Content ships via a SHA-guarded COMPACT splice mirroring the apple builder, with a Trevor source-manifest sign-off for any non-T1 datapoint.

**Tech Stack:** Python 3 (stdlib), standalone assert-based test files (run directly, not pytest), the repo's existing gate + apply_patch tooling.

**Spec:** `docs/superpowers/specs/2026-07-12-onion-variety-pilot-design.md`
**Memory:** `onion-variety-pilot-photoperiod`, `apple-variety-pilot-tree-archetype`

## Global Constraints

- **Canonical JSON is COMPACT**: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 4 (the authoring/promote splice). Tasks 1-2 touch only tooling + tests + a scratch copy.
- **TDD: RED before GREEN.** The gate refactor gets a failing test first; adversarially proven on a scratch copy of real onion (Task 2) before content is trusted.
- **No em dashes in consumer copy** (variety prose): commas/colons/semicolons/periods. `--` is fine in code/docs/commits. American English. Temps as `°F`.
- **T1-or-it-does-not-ship** for load-bearing numbers (per-variety `days_to_maturity` + `day_length_type`). Non-T1 -> Trevor manifest sign-off before the splice. No silent drops/downgrades. Expect clean T1 (standard extension data).
- **Per-variety `sources`/`anchoring_urls` are T1-only** (whole_crop_gate E.source-tier fails any non-T1; onion is certified). Any T2 datapoint's honesty lives in `confidence_tier` + prose, never a cited non-T1 source.
- **Release verification before promote** (protocol #6): `whole_crop_gate onion` (incl A9 photoperiod: coverage + window-fit) + `gate_all` + `release_verify --slug onion` + `variety_detail_gate` + source-truth sample.
- **State trio at release:** CURRENT_STATE.md (patch surgically -- no `---` separator, `current-state-md-drift`), STATE_HISTORY.md (prepend), LATEST.txt (SHA + session).
- **Canonical count stays 125.** Onion enriches its existing 6 varieties, adds no crops. Footprint = onion's `varieties` + a new `variety_archetype` key + `verification_status.source_set`; all other crops byte-identical.
- **No plant-astro submodule bump from this session.** Trevor confirms the push.

---

## File Structure

- `tools/variety_detail_gate.py` (modify) -- add `photoperiod_annual` to the archetype dispatch (3-way traits/enums), add the `DAY_LENGTH` enum, share the DTM check across DTM archetypes.
- `tools/test_variety_detail_gate.py` (modify) -- add photoperiod fixtures + dispatch/enum/DTM asserts; keep dry-bean + apple asserts green.
- `tools/build_onion_varieties_patch.py` (create) -- emit the SHA-guarded COMPACT patch (mirror `build_apple_varieties_patch.py`).
- `tools/batches/onion_varieties_pilot.json` (create, generated) -- the patch file.
- `docs/field_addition_register.md` (modify) -- row 14 (photoperiod-variety bundle, INV-1 trigger).
- `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (modify at release).

---

## Task 1: Gate -- add the `photoperiod_annual` archetype (3-way dispatch + shared DTM)

**Files:**
- Modify: `tools/variety_detail_gate.py`
- Test: `tools/test_variety_detail_gate.py`

**Interfaces:**
- Consumes: existing `archetype()`, `_variety_objs`, `in_scope`, `_int`, `dtm_empty`, `variety_violations`, `variety_warnings`.
- Produces: `archetype(crop)` now also returns `"photoperiod_annual"`; `variety_violations` dispatches required fields/enums 3 ways and runs the DTM check for `{annual_dtm, photoperiod_annual}`. Annual + tree behavior unchanged.

- [ ] **Step 1: Write the failing tests -- a photoperiod crop validates, requires day_length_type + DTM, rejects bean/tree fields**

Add to `tools/test_variety_detail_gate.py` (after the tree fixtures):

```python
def pvar(**over):
    v = {"id": "super-star", "name": "Super Star", "maturity_class": "mid", "is_reference": True,
         "confidence_tier": "T1", "note_beginner": "b", "note_seasoned": "s", "sources": ["tamu_agrilife"],
         "days_to_maturity": 105, "day_length_type": "intermediate_day", "use": "sweet all-purpose"}
    v.update(over)
    return v

def pcrop(varieties, slug="onion"):
    return {"slug": slug, "variety_archetype": "photoperiod_annual", "days_to_maturity": [90, 120],
            "varieties": {"recommended": varieties}}

_wallawalla = pvar(id="walla-walla", name="Walla Walla", day_length_type="long_day",
                   days_to_maturity=110, use="sweet fresh-eating", is_reference=False)

# dispatch
assert archetype(pcrop([pvar()])) == "photoperiod_annual"

# clean photoperiod crop -> no violations
PP_CLEAN = pcrop([pvar(), _wallawalla])
assert variety_violations(PP_CLEAN) == [], variety_violations(PP_CLEAN)

# photoperiod does NOT require bean traits or tree fields
assert not any("seed_type" in v or "bloom_group" in v for v in variety_violations(PP_CLEAN)), variety_violations(PP_CLEAN)

# bad day_length_type enum -> violation
assert any("day_length_type" in v for v in variety_violations(pcrop([pvar(day_length_type="all_day"), _wallawalla])))

# missing required photoperiod field (day_length_type / use) -> violation
for f in ("day_length_type", "use"):
    v = pvar(); del v[f]
    assert any(f in x for x in variety_violations(pcrop([v, _wallawalla]))), (f, variety_violations(pcrop([v, _wallawalla])))

# photoperiod IS a DTM archetype: missing DTM -> violation; absurd DTM (violates [7,400]) -> violation
v = pvar(); del v["days_to_maturity"]
assert any("days_to_maturity" in x for x in variety_violations(pcrop([v, _wallawalla])))
assert any("days_to_maturity" in x for x in variety_violations(pcrop([pvar(days_to_maturity=850), _wallawalla])))

# class/DTM coherence warning applies to photoperiod too (fastest labeled 'late')
fast_late = pvar(id="q", name="Q", days_to_maturity=80, maturity_class="late", is_reference=False)
assert any("late" in w for w in variety_warnings(pcrop([pvar(), fast_late]))), variety_warnings(pcrop([pvar(), fast_late]))
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: FAIL -- `archetype(...)` returns `"annual_dtm"` for the photoperiod crop (line 55 doesn't know the token), so `PP_CLEAN` reports spurious missing `seed_type`/`seed_color`/... (bean traits) and no `day_length_type` enforcement.

- [ ] **Step 3: Implement the 3-way dispatch in `tools/variety_detail_gate.py`**

After the `TREE_ENUMS = (...)` line (currently line 49), add the photoperiod constants + dispatch tables:

```python
# photoperiod_annual (onion) archetype
DAY_LENGTH = {"long_day", "intermediate_day", "short_day"}
PHOTOPERIOD_TRAITS = ("day_length_type", "use")
PHOTOPERIOD_ENUMS = (("day_length_type", DAY_LENGTH),)

# archetype dispatch: required trait block + enum block per archetype; DTM_ARCHETYPES carry days_to_maturity
ARCHETYPE_TRAITS = {"annual_dtm": ANNUAL_TRAITS, "photoperiod_annual": PHOTOPERIOD_TRAITS, "tree_fruit": TREE_TRAITS}
ARCHETYPE_ENUMS = {"annual_dtm": ANNUAL_ENUMS, "photoperiod_annual": PHOTOPERIOD_ENUMS, "tree_fruit": TREE_ENUMS}
DTM_ARCHETYPES = ("annual_dtm", "photoperiod_annual")
```

Update `archetype()` (line 55) to admit the new token:

```python
    return a if a in ("annual_dtm", "photoperiod_annual", "tree_fruit") else "annual_dtm"
```

Replace the binary required/enums selection (lines 84-85) with the dispatch tables:

```python
    required = COMMON_CORE + ARCHETYPE_TRAITS[arch]
    enums = COMMON_ENUMS + ARCHETYPE_ENUMS[arch]
```

Replace the binary check-dispatch (lines 106-109) with a 3-way that shares the DTM check:

```python
        if arch in DTM_ARCHETYPES:
            V += _dtm_checks(slug, nm, x, season_only)
        elif arch == "tree_fruit":
            V += _tree_checks(slug, nm, x)
```

Rename `_annual_dtm_checks` -> `_dtm_checks` (line 118) and update its docstring:

```python
def _dtm_checks(slug, nm, x, season_only):
    """days_to_maturity presence/int/[7,400] for the DTM archetypes (annual_dtm + photoperiod_annual)."""
```

Do NOT change `variety_warnings`: its tree branch returns early for `tree_fruit`, and every non-tree archetype (annual_dtm AND photoperiod_annual) correctly falls through to the shared band + class/DTM warnings, which onion (crop DTM `[90,120]` + per-variety DTM + maturity_class) needs.

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 tools/test_variety_detail_gate.py`
Expected: PASS -- `variety_detail_gate tests: OK` (all existing annual/tree asserts + the new photoperiod asserts).

- [ ] **Step 5: Commit**

```bash
git add tools/variety_detail_gate.py tools/test_variety_detail_gate.py
git commit -m "feat(variety-gate): add photoperiod_annual archetype (3-way dispatch, shared DTM machinery)"
```

---

## Task 2: Adversarial RED proof on a scratch copy of real onion

Prove the photoperiod dispatch catches real defects in onion's actual shape before content is trusted (the CLAUDE.md "sneak a defect at it" bar). Verification task; no production code changes.

**Files:**
- Create (scratch, session scratchpad -- NOT git): `prove_onion_gate.py` + `onion_scratch.json`

- [ ] **Step 1: Build a scratch canonical whose onion carries a valid photoperiod schema, confirm the gate is green**

Write `prove_onion_gate.py` (in the session scratchpad) that: loads canonical, finds onion, sets `variety_archetype="photoperiod_annual"`, and rewrites onion's 6 varieties to a MINIMAL VALID photoperiod schema (id/name/maturity_class/is_reference[one true]/confidence_tier/notes/sources + days_to_maturity + day_length_type[carry the real values] + use). Dump to `onion_scratch.json`. Run:

Run: `python3 tools/variety_detail_gate.py <scratch>/onion_scratch.json --coverage`
Expected: `violations=0`; onion appears in `in_scope` count.

- [ ] **Step 2: Inject each defect class into the scratch onion and confirm each bounces**

For each, mutate a throwaway copy and re-run the gate, asserting non-zero exit + expected substring (subprocess like `test_variety_detail_gate.py::_run`):
- `day_length_type` = `"all_day"` -> violation mentions `day_length_type`.
- drop `days_to_maturity` -> violation mentions `days_to_maturity` (photoperiod is a DTM archetype).
- `days_to_maturity` = `850` -> violation mentions `days_to_maturity` (outside `[7,400]`).
- drop `use` -> violation mentions `use`.
- two varieties with `is_reference: true` -> violation mentions `is_reference`.

Encode as asserts in `prove_onion_gate.py`.

Run: `python3 <scratch>/prove_onion_gate.py`
Expected: prints `onion photoperiod-gate adversarial proof: OK` (every defect bounced).

- [ ] **Step 3: Confirm canonical untouched (READ-ONLY held)**

Run: `shasum -a 256 crops_data_final.json | cut -d' ' -f1`
Expected: `a6ead469...` (unchanged). No commit (scratch only). Paste the proof output into the Task-5 STATE_HISTORY entry as recorded RED evidence.

---

## Task 3: Author the 6 varieties + source manifest + Trevor sign-off (CHECKPOINT)

**Files:**
- Create: `tools/build_onion_varieties_patch.py` (mirror `tools/build_apple_varieties_patch.py`)
- Produce: a source manifest (markdown table) for Trevor -- ONLY the non-T1 rows need sign-off

- [ ] **Step 1: Draft the 6 variety objects in the builder**

Copy `build_apple_varieties_patch.py` to `build_onion_varieties_patch.py`; set `CANON`, `OUT="tools/batches/onion_varieties_pilot.json"`, target slug `onion`. There is NO derived-window map and NO tree block: each variety carries common core + `days_to_maturity` + `day_length_type` + `use`. Author `VARIETIES` for: `walla-walla` (long), `yellow-sweet-spanish` (long), `super-star` (intermediate, **is_reference:true**), `cimarron` (intermediate), `texas-1015y-supersweet` (short), `yellow-granex` (short). For each: add `id`, `maturity_class` (from the sourced DTM), `confidence_tier`, per-variety `days_to_maturity`, dual-register `note_beginner`/`note_seasoned` (preserve the real content of the current `recommended_note`, drop that key), per-variety T1 `sources`/`anchoring_urls`; carry `day_length_type` + `use` forward. Declare `variety_archetype:"photoperiod_annual"`. The patch ops (SHA-guarded, mirroring apple):

```python
patch = {"base_sha": sha, "patches": [
    {"op": "add", "json_path": "$.crops[?(@.slug=='onion')].variety_archetype", "value": "photoperiod_annual"},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='onion')].varieties", "from": current_varieties, "value": new_varieties},
    {"op": "replace", "json_path": "$.crops[?(@.slug=='onion')].verification_status.source_set", "from": current_ss, "value": new_ss},
]}
```

- [ ] **Step 2: Verify each load-bearing number against a T1 source; classify tier**

For every variety's `days_to_maturity` + `day_length_type`, find the source (extension onion-variety guides: Texas A&M, UMN, Utah State; the crop `photoperiod` model already cites `tamu_agrilife`+`piedmont_mg`). Prefer T1. Confirm each source id is catalogued + tier T1 (`source_catalog`); add none unless required. `day_length_type` values already exist -- verify, do not blindly carry.

- [ ] **Step 3: Produce the source manifest for Trevor (non-T1 rows need sign-off)**

Emit a markdown table: `datapoint | variety | proposed source id | tier | URL | what it backs`. T1 rows are informational; every non-T1 row is a sign-off request with the reason T1 was unavailable + the T2 candidate. Expect few/none (onion day-length + DTM are standard extension data).

- [ ] **CHECKPOINT (Trevor):** Trevor reviews the manifest and approves ship-as-T2 (recorded in `confidence_tier`) or holds. **Do not proceed to Task 4 until sign-off** (or, if all-T1, confirm with Trevor there is nothing to sign and proceed).

- [ ] **Step 4: Commit the builder (tooling only; canonical untouched)**

```bash
git add tools/build_onion_varieties_patch.py
git commit -m "build(onion): variety-pilot patch builder (6 varieties, photoperiod schema)"
```

---

## Task 4: SHA-guarded splice + full release battery (CHECKPOINT: promote)

**Files:**
- Generate: `tools/batches/onion_varieties_pilot.json`
- Modify (promote): `crops_data_final.json`

- [ ] **Step 1: Generate the patch + apply to a scratch copy**

```bash
python3 tools/build_onion_varieties_patch.py
python3 tools/apply_patch.py tools/batches/onion_varieties_pilot.json --out crops_data_final.scratch.json
```
Expected: footprint = onion's `varieties` + `variety_archetype` + source_set only; SHA gate passes (base `a6ead469`).

- [ ] **Step 2: Audit the footprint (exactly onion moved; count 125; COMPACT)**

```bash
python3 -c "import json; a=json.load(open('crops_data_final.json')); b=json.load(open('crops_data_final.scratch.json')); ca={c['slug']:c for c in a['crops']}; cb={c['slug']:c for c in b['crops']}; print('count', len(b['crops'])); print('moved', [s for s in ca if ca[s]!=cb.get(s)])"
```
Expected: `count 125`; `moved ['onion']`.

- [ ] **Step 3: Run the full release battery on the scratch candidate**

```bash
python3 tools/whole_crop_gate.py onion crops_data_final.scratch.json
python3 tools/variety_detail_gate.py crops_data_final.scratch.json --warnings --coverage
python3 tools/gate_all.py crops_data_final.scratch.json
python3 tools/release_verify.py crops_data_final.scratch.json --base crops_data_final.json --slug onion
python3 tools/source_truth_sample.py --dataset crops_data_final.scratch.json --crops onion
```
Expected: `whole_crop_gate onion` clean (incl A9 photoperiod: coverage + window-fit unchanged -- the 6 varieties still cover all 3 resolved day-length types); `variety_detail` onion in-scope, 0 violations; `gate_all` 116 certified unchanged; `release_verify` no new concern beyond pre-existing false positives (confirm any concern is identical on the base, per the apple pattern); `source_truth_sample` onion traces to approved sources. **If any register-completeness violation appears** (an unruled new string key -- not expected, but verify), add the ruling to `register_completeness_gate.py` + its test (TDD) before promoting.

- [ ] **CHECKPOINT (Trevor):** green battery + manifest sign-off = promote-eligible. On Trevor's go:

- [ ] **Step 4: Promote scratch to canonical (COMPACT) + confirm SHA**

```bash
cp crops_data_final.scratch.json crops_data_final.json
rm -f crops_data_final.scratch.json
shasum -a 256 crops_data_final.json | cut -d' ' -f1
```
Record the new SHA for the state trio. Re-run `python3 tools/whole_crop_gate.py onion` and `python3 tools/gate_all.py` on the promoted canonical -- both clean.

---

## Task 5: State trio + field-addition register + release commit

**Files:**
- Modify: `CURRENT_STATE.md` (surgical prepend), `STATE_HISTORY.md` (prepend), `LATEST.txt`, `docs/field_addition_register.md`

- [ ] **Step 1: Add the field-addition register row 14**

Add a `docs/field_addition_register.md` row 14 for the photoperiod-variety bundle (`day_length_type` as the archetype's load-bearing field, sharing `days_to_maturity` with the DTM archetypes) with the explicit INV-1 hard-flip trigger verbatim: *"flip the `variety_detail_gate` photoperiod-block checks from soft/standalone into the A39 register-coverage hard floor + `gate_all` when the Spec-2 rollout column pass reaches full-roster coverage."* Note onion = photoperiod + allium-family exemplar.

- [ ] **Step 2: State trio**

- CURRENT_STATE.md: prepend a new bold release entry (the reverse-chron log; no `---` separator -- do NOT run a naive `gen_current_state` regen, it corrupts the file per `current-state-md-drift`). New SHA, footprint, the photoperiod archetype + the shared-DTM-dispatch note.
- STATE_HISTORY.md: prepend a most-recent-first entry: SHA transition, footprint, the archetype refactor, the recorded adversarial RED proof (Task 2), the manifest sign-off summary, A9 stays green.
- LATEST.txt: bump SHA + session line.

- [ ] **Step 3: Release commit (Trevor confirms push)**

```bash
git add crops_data_final.json tools/batches/onion_varieties_pilot.json CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/field_addition_register.md
git commit -m "feat(onion): photoperiod-archetype variety pilot -- 6 varieties on the flat schema"
```
Trevor confirms the push. **No plant-astro submodule bump from this session.** App consumption (variety detail per latitude) + INV-2 on `days_to_maturity` = Spec 2.

---

## Self-Review notes (author)

- **Spec coverage:** archetype dispatch + shared DTM (Task 1), adversarial RED (Task 2), sourcing contract + manifest sign-off (Task 3), splice/battery/footprint + register-verify (Task 4), state trio + register row + INV-1 (Task 5). The A9 photoperiod honesty engine (Spec 8) is intentionally untouched; day-length-vs-region checks are NOT duplicated in `variety_detail_gate`.
- **No new validator function:** `day_length_type` is enum-only (dispatch handles it); the DTM check is shared (`_dtm_checks`). This is why there's no `_photoperiod_checks` analogous to `_tree_checks` -- correct, not a gap.
- **No new register ruling expected** (Spec 6): `day_length_type`/`use`/common-core keys already ruled. Task 4 Step 3 verifies and only adds a ruling if a key surfaces.
- **Non-obvious risk:** the A9 coverage invariant requires >=1 variety per resolved day-length type. The 6 varieties cover long/intermediate/short, so re-typing must preserve at least one of each -- the battery's `whole_crop_gate onion` catches a violation of this.
