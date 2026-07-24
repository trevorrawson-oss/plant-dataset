# Asparagus Certification (Authoring Half) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote asparagus from honest shell to certified gold-standard crop #120 (119 -> 120 certified; 128 total unchanged) as a `herbaceous_perennial` on `frost_anchored`, by fixing two gate blockers, authoring the full agronomy + 16 regions + register fields into the staged reference, then one atomic canonical splice + full release gauntlet + state trio.

**Architecture:** Two small archetype-scoped gate carve-outs (A34/A37) make asparagus's honest spring-harvest-then-summer-fern calendar legal without perturbing the 119 certified. All content is authored T1-first into `tools/staging/asparagus_reference.json` (canonical stays READ-ONLY) and validated on scratch merges against the standalone gates; a single deterministic splice then promotes it, followed by the CLAUDE.md protocol-#6 gauntlet.

**Tech Stack:** Python 3 (stdlib only), plain-assert test scripts (`python3 tools/test_*.py`), compact JSON dataset. Sourcing via WebFetch/WebSearch of T1 extension pages (raw HTML/PDF, never a WebFetch markdown data-table).

## Global Constraints

- **Canonical `crops_data_final.json` is COMPACT** (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent`) and stays **READ-ONLY until Task 9** (the promote). All authoring lives in `tools/staging/asparagus_reference.json`.
- **TDD: RED before GREEN.** Every gate change injects the defect into a fixture and confirms it bounces, AND confirms the carve-out does not weaken enforcement for non-archetype crops, before the change is trusted.
- **T1-OR-DROP.** Every authored numeric, resistance grade, and suitability call is verified against a FETCHED T1 page (.edu / government extension) -- raw HTML or PDF, never a WebFetch markdown table (the column-shift lesson). WebSearch summaries invent pages; fetch the real page + cross-check a 2nd source. Drop rather than fabricate.
- **No em dashes in consumer copy** (commas/colons/semicolons/periods; `--` fine in docs/code/commits). **American English.** Temps render `°F`. **"ladybug" not "lady beetle".** "plant" lowercase except sentence-start / "Plant Pro".
- Base canonical: `ccf5e890` (origin/main `44b3214` -> spec commit `b78a255`). Spec: `docs/superpowers/specs/2026-07-23-asparagus-cert-authoring.md`.
- Per-task commits land on `main` local + unpushed (explicit-pathspec `git add`, `git status` before commit, `git show --stat` after -- the concurrent-git-safety lesson). The push is Trevor-gated; the plant-astro bump is a separate astro-session concern.
- `verified` date on every `anchoring_urls` entry = `"2026-07-24"`. Session tag = `asparagus_cert_gs_arc`.
- `days_to_maturity` stays `[]` (perennial N/A sentinel); NEVER add `dtm_anchor`.
- control_ladder problem `type` = `"fungal"` (not "disease"). `resistance` GRADES = {immune,resistant,tolerant,susceptible}; keys == `diseases[].id`.

## File Structure

- Modify: `tools/cross_consistency_gate.py` (Rule 2 archetype exemption), `tools/test_cross_consistency_gate.py`.
- Modify: `tools/calendar_coherence_gate.py` (Bug 1 archetype exemption), `tools/test_calendar_coherence_gate.py`.
- Modify (staging authoring): `tools/staging/asparagus_reference.json` -- extended across Tasks 2-8.
- Create: `tools/staging/asparagus_scratch_merge.py` -- a reusable helper that merges the staged reference into a scratch copy of the canonical and runs the standalone gates (Task 2; reused by Tasks 3-8).
- Create: `tools/promote_asparagus.py` -- the deterministic one-shot splice (Task 9).
- Modify (the promote, Task 9): `crops_data_final.json` (+ any `source_catalog`/`control_methods` additions).
- Create: `docs/reviews/notes/2026-07-24/asparagus_cert_verification.md` -- the gauntlet record (Task 10).
- Modify (Task 11): `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`, `docs/field_addition_register.md`.

---

### Task 1: A34/A37 archetype carve-out (TDD)

**Files:**
- Modify: `tools/cross_consistency_gate.py` (Rule 2 guard, ~line 71)
- Modify: `tools/test_cross_consistency_gate.py` (append before the final `print`)
- Modify: `tools/calendar_coherence_gate.py` (`growing_reachability_violations`, ~line 120)
- Modify: `tools/test_calendar_coherence_gate.py` (append before the final `print`)

**Interfaces:**
- Consumes: nothing.
- Produces: `cross_consistency_violations(crop)` and `growing_reachability_violations(crop)` both no-op Rule 2 / Bug 1 for `crop["archetype"] == "herbaceous_perennial"`, while still firing for every other frost_anchored crop.

- [ ] **Step 1: Write the failing tests (cross_consistency)**

Append to `tools/test_cross_consistency_gate.py` immediately BEFORE its final `print("cross_consistency_gate: all tests passed")` line:

```python
# 14. herbaceous_perennial (asparagus) carve-out: an established permanent bed's steady-state
# calendar renders spring `harvest` + summer `growing` with NO annual plant token -- legit, must NOT
# fire Rule 2 (a permanent bed is planted once at establishment, like trees/berries off frost_anchored).
_hp = {"slug": "asparagus", "calendar_basis": "frost_anchored", "archetype": "herbaceous_perennial",
       "regions": {"northern_tier": {"resolved_by_zone": {"4": {"calendar":
           ["cold_pause","cold_pause","cold_pause","cold_pause","harvest","harvest",
            "growing","growing","growing","growing","cold_pause","cold_pause"]}}}}}
assert cross_consistency_violations(_hp) == [], cross_consistency_violations(_hp)
# 14b. REGRESSION: the SAME harvest-without-plant calendar on a NON-herbaceous_perennial frost_anchored
# crop STILL bounces (the carve-out must not weaken enforcement for annuals).
_ann = dict(_hp, archetype="cool_season_annual")
assert any("plant-class token" in v for v in cross_consistency_violations(_ann)), cross_consistency_violations(_ann)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_cross_consistency_gate.py`
Expected: FAIL on assert 14 (`AssertionError` listing the `plant-class token` violation) -- the archetype is not yet exempt.

- [ ] **Step 3: Add the Rule 2 archetype exemption**

In `tools/cross_consistency_gate.py`, replace the Rule 2 guard (currently):

```python
    # RULE 2 -- harvest-requires-plant (frost_anchored only).
    if crop.get("calendar_basis") == "frost_anchored":
```

with:

```python
    # RULE 2 -- harvest-requires-plant (frost_anchored ANNUALS only). A herbaceous_perennial
    # (asparagus) is an established permanent bed planted once at establishment, not in the annual
    # month-strip -- the same reason trees/berries are exempt off frost_anchored -- so its steady-
    # state calendar legitimately renders `harvest` (spring spears) with no annual plant token.
    if (crop.get("calendar_basis") == "frost_anchored"
            and crop.get("archetype") != "herbaceous_perennial"):
```

Also update the module docstring Rule 2 line (`~line 18`) to end: `No-op off frost_anchored (trees / berries plant once at establishment) and for the herbaceous_perennial archetype (asparagus's permanent bed).`

- [ ] **Step 4: Run to verify it passes**

Run: `python3 tools/test_cross_consistency_gate.py`
Expected: PASS, ending `cross_consistency_gate: all tests passed`.

- [ ] **Step 5: Write the failing tests (calendar_coherence)**

Append to `tools/test_calendar_coherence_gate.py` immediately BEFORE its final `print("calendar_coherence_gate: all tests passed")` line:

```python
# herbaceous_perennial (asparagus) carve-out: the summer fern `growing` legitimately follows the
# spring spear `harvest` -- the frost_anchored analog of the evergreen "grows after harvest" exemption.
_hp = {"slug": "asparagus", "calendar_basis": "frost_anchored", "archetype": "herbaceous_perennial",
       "regions": {"northern_tier": {"resolved_by_zone": {"4": {"calendar":
           ["cold_pause","cold_pause","cold_pause","cold_pause","harvest","harvest",
            "growing","growing","growing","growing","cold_pause","cold_pause"]}}}}}
assert growing_reachability_violations(_hp) == [], growing_reachability_violations(_hp)
# REGRESSION: the same impossible growing-after-harvest on a NON-herbaceous_perennial frost_anchored
# crop STILL bounces.
_ann = dict(_hp, archetype="cool_season_annual")
assert growing_reachability_violations(_ann), growing_reachability_violations(_ann)
```

- [ ] **Step 6: Run to verify it fails**

Run: `python3 tools/test_calendar_coherence_gate.py`
Expected: FAIL on the herbaceous_perennial assert (the summer `growing` is flagged not-reachable) -- not yet exempt.

- [ ] **Step 7: Add the Bug 1 archetype exemption**

In `tools/calendar_coherence_gate.py`, in `growing_reachability_violations`, immediately AFTER the existing:

```python
    if crop.get("calendar_basis") != "frost_anchored":
        return []
```

insert:

```python
    if crop.get("archetype") == "herbaceous_perennial":
        return []  # asparagus: the summer fern grows AFTER the spring spear harvest -- the
        # frost_anchored analog of the evergreen "legitimately grows after harvest" exemption above.
```

Update the function docstring to note the herbaceous_perennial no-op.

- [ ] **Step 8: Run to verify it passes**

Run: `python3 tools/test_calendar_coherence_gate.py`
Expected: PASS, ending `calendar_coherence_gate: all tests passed`.

- [ ] **Step 9: Confirm no roster regression**

Run:
```bash
python3 tools/cross_consistency_gate.py crops_data_final.json
python3 tools/calendar_coherence_gate.py crops_data_final.json
python3 tools/gate_all.py crops_data_final.json
```
Expected: `cross_consistency gate: 0 violation(s)`; `calendar_coherence gate: 0 ...`; `gate_all: PASS -- every certified crop passes the whole suite` (119 certified, all unperturbed -- no certified crop carries the archetype).

- [ ] **Step 10: Commit**

```bash
git add tools/cross_consistency_gate.py tools/test_cross_consistency_gate.py tools/calendar_coherence_gate.py tools/test_calendar_coherence_gate.py
git status --short
git commit -m "fix(gate): A34/A37 archetype carve-out for herbaceous_perennial (asparagus fern-after-harvest)"
git show --stat HEAD | head -8
```

---

### Task 2: Reference structural fixes + the scratch-merge harness

**Files:**
- Modify: `tools/staging/asparagus_reference.json` (planting_layout, category, anchoring_urls `verified`)
- Create: `tools/staging/asparagus_scratch_merge.py`

**Interfaces:**
- Consumes: the staged reference, the A46 / control_ladder / variety_resistance gates.
- Produces: `tools/staging/asparagus_scratch_merge.py` -- writes `/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/<session>/scratchpad/asparagus_scratch_canonical.json` (canonical with the staged asparagus spliced in) and runs A46 + control_ladder + variety_resistance + a full `whole_crop_gate asparagus` on it, printing each result. Reused by Tasks 3-8.

- [ ] **Step 1: Fix planting_layout (A44 crash)**

In `tools/staging/asparagus_reference.json`, replace the `planting_layout` object:

```json
  "planting_layout": {
    "pattern": "rows",
    "row_spacing_inches": [48, 60],
    "in_row_spacing_inches": [8, 12]
  },
```

with the enum string (the dict form crashes A44; row/in-row spacing detail lives in prose):

```json
  "planting_layout": "row",
```

- [ ] **Step 2: Set the new category + confirm lifecycle**

In `tools/staging/asparagus_reference.json`, set `"category": "Perennial Vegetables"` (was `"Fruiting Veg"`). Confirm `"lifecycle": "perennial"` (already set in the reference; this is the reconcile from the shell's `"permanent"`).

- [ ] **Step 3: Add `verified` to every anchoring_urls entry**

Every `anchoring_urls` entry in the reference currently looks like `{"umn_ext": {"url": "..."}}`. Add `"verified": "2026-07-24"` to EACH (gate F requires `{url, verified}`). Example -- change:

```json
"anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/vegetables/growing-asparagus"}}
```
to:
```json
"anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/vegetables/growing-asparagus", "verified": "2026-07-24"}}
```

Apply to all anchoring_urls in varieties, pests, diseases, and both region cells. (Region-root `sources` need no anchoring_urls -- F excludes the region root.)

- [ ] **Step 4: Write the scratch-merge harness**

Create `tools/staging/asparagus_scratch_merge.py`:

```python
#!/usr/bin/env python3
"""Merge the staged asparagus reference into a SCRATCH copy of the canonical and run the gates on
it -- WITHOUT touching crops_data_final.json (READ-ONLY until promote). Reused by every authoring
task to validate progress. Prints A46 / control_ladder / variety_resistance / whole_crop_gate results.
Usage: python3 tools/staging/asparagus_scratch_merge.py
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRATCH = "/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad"
OUT = os.path.join(SCRATCH, "asparagus_scratch_canonical.json")

sys.path.insert(0, os.path.join(ROOT, "tools"))
from herbaceous_perennial_gate import herbaceous_perennial_violations
from control_ladder_gate import ladder_violations, identity_violations
from variety_resistance_gate import resistance_violations

def main():
    data = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
    ref = json.load(open(os.path.join(HERE, "asparagus_reference.json"), encoding="utf-8"))["crop"]
    crops = data["crops"]
    for i, c in enumerate(crops):
        if c.get("slug") == "asparagus":
            crops[i] = ref
            break
    else:
        crops.append(ref)
    os.makedirs(SCRATCH, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("A46:", herbaceous_perennial_violations(ref) or "clean")
    print("control_ladder (ladder):", ladder_violations(data, ref) or "clean")
    print("control_ladder (identity):", identity_violations(ref) or "clean")
    print("variety_resistance:", resistance_violations(ref) or "clean")
    print("--- whole_crop_gate asparagus (scratch) ---")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "whole_crop_gate.py"),
                        "asparagus", OUT], capture_output=True, text=True)
    tail = [l for l in r.stdout.splitlines() if l.startswith("GATE:") or "FAIL" in l or "violation" in l.lower()]
    print("\n".join(tail[-40:]))
    print(r.stdout.splitlines()[-1] if r.stdout else "(no output)")

if __name__ == "__main__":
    main()
```

(Confirm `ladder_violations(data, crop)` / `identity_violations(crop)` / `resistance_violations(crop)` signatures against `grep -n "^def " tools/control_ladder_gate.py tools/variety_resistance_gate.py` before first run; adjust the calls if the signatures differ.)

- [ ] **Step 5: Run the harness**

Run: `python3 tools/staging/asparagus_scratch_merge.py`
Expected: `A46: clean`, `control_ladder ...: clean`, `variety_resistance: clean`. `whole_crop_gate` will still FAIL (agronomy + 14 regions not yet authored) -- that is expected at this stage; record which A-gates fail as the authoring worklist.

- [ ] **Step 6: Commit**

```bash
git add tools/staging/asparagus_reference.json tools/staging/asparagus_scratch_merge.py
git status --short
git commit -m "fix(asparagus): reference planting_layout->row, Perennial Vegetables category, anchoring verified; scratch-merge harness"
```

---

### Task 3: Core agronomy + register fields (T1 authoring)

> **Content-authoring task.** A sourcing-capable subagent authors T1 values into `tools/staging/asparagus_reference.json`. Structure + gate requirements are fixed below; prose + numerics are authored from FETCHED T1 extension pages (UMN, MSU, UMass, Cornell, UC IPM asparagus, Rutgers, Illinois). Every sourced leaf carries `sources` (catalogued T1 ids) + `anchoring_urls` with `{url, verified:"2026-07-24"}`.

**Files:**
- Modify: `tools/staging/asparagus_reference.json`

**Interfaces:**
- Consumes: the reference, `source_catalog` ids.
- Produces: the reference with all §3f structured-numeric + §3e register fields populated. Growth-stage IDS defined here are consumed by Task 4 (watering.schedule_by_stage + tips_by_stage must key to them).

- [ ] **Step 1: Author the structured agronomy block**

Populate these keys (replace the shell's null/empty values). Each numeric T1-sourced; shapes:
- `soil`: object (texture/drainage/organic-matter prose per the shell's soil shape -- match a certified crop's `soil` keys).
- `soil_prep_beginner` / `soil_prep_seasoned`: prose (deep, well-drained, high-OM bed; trench planting).
- `ph`: `{"preferred_range":[6.5,7.5],"tolerated_range":[6.0,8.0],"note_seasoned":"...","note_beginner":"..."}` -- T1-verify the range (asparagus tolerates near-neutral to slightly alkaline; UMN/UMass). The prose stated pH MUST agree with `preferred_range` within 0.5 (A34 Rule 1).
- `sunlight`: a raw-display token (e.g. `"full_sun"`; no snake_case leak in prose -- A23). `sunlight_hours`: `[6,8]` or T1 value in [1,18].
- `water` + `watering.*`: the full watering block (frequency/amount/method/signs dual-register + `watering_method` + `drought_tolerance` raw-display tokens + `schedule_by_stage` [Task 4] + `sources`/`anchoring_urls`).
- `spacing_inches`: `[12,18]` in-row (or T1) -- positive `[lo,hi]`, <=72.
- `germination_temp_f`: `[70,85]` or T1 (asparagus seed germinates warm) -- in [32,110].
- `fertilizer`: `{"type","timing","frequency","npk_ratio":"N-P-K"?, "npk_hint_seasoned"?, ...}` -- if `npk_hint_*` present then `npk_ratio` present (A17). Asparagus: annual spring + post-harvest feeding; T1 NPK.
- `container_notes`: `{"container_ok": false, ...prose reason...}` (asparagus is a poor container/permanent-bed crop) OR true with `min_pot_gallons`/`depth_inches_min` if a T1 source supports a large deep container -- author to source.
- `sources_summary`: the T1 source roll-up prose.

- [ ] **Step 2: Author growth_stages (perennial establishment stages)**

`growth_stages`: a non-empty list. For a perennial with `days_to_maturity:[]`, OMIT `day_range_from_sow` (the ladder is skipped when dtm-empty; do not author a partial ladder -- A40 all-or-nothing). Each stage: `{"id","name","audience","what_to_look_for_seasoned","what_to_look_for_beginner","user_action_seasoned","user_action_beginner"}`. Model the asparagus arc, e.g. ids: `establishment` (year 1 crowns/ferning), `dormancy` (winter), `spear_emergence` (spring harvest), `fern_growth` (summer recharge). Every stage id must get a tip in Task 4 (A12 coverage).

- [ ] **Step 3: Author the register fields (§3e)**

- `propagule: "crown"`. Do NOT add `dtm_anchor` or `sow_depth_inches`.
- `germination_light`: T1 value for asparagus seed, or `null` (legal since propagule != seed). `seedling_light: "na"`.
- `heat_threshold_f` + `heat_effect`: T1 (likely `null` + `"heat_tolerant"` -- ferns tolerate summer heat; author to source if a threshold is named).
- `frost_tolerance_f` + `frost_effect`: the FERN is frost-tender -> a T1 foliage-frost threshold + `frost_effect:"killed"` (the fall dieback). The crown's deep hardiness lives in `hardiness_notes_*`, not this field.
- `chilling_sensitivity_f: null`. `tray_sowing: "na"`.
- Add a `verification_status.field_additions` entry (built fully in Task 8) noting the timing-spine columns with T1 `sources` (A40 amend-not-recert).

- [ ] **Step 4: Validate on scratch**

Run: `python3 tools/staging/asparagus_scratch_merge.py`
Expected: A46/ladder/resistance still clean; `whole_crop_gate` A17/A20/A33/A40/A41/A42 no longer fail (agronomy present). Remaining failures should now be only the region-coverage gates (A31/A45/A2/A32/A5/A24/A12 stage/tips/notifications) + prose gates pending later tasks. Record.

- [ ] **Step 5: T1-fidelity review + commit**

Dispatch a T1-fidelity review of every authored numeric (ph, spacing, germ temp, NPK, frost threshold) against its FETCHED source. Fix or drop any that do not verify. Then:
```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): core agronomy + register fields (T1)"
```

---

### Task 4: Stage-keyed cluster -- tips_by_stage + watering.schedule_by_stage + failure_diagnostics

> **Content-authoring task.** Depends on Task 3's `growth_stages` ids. All three fields key to those exact ids.

**Files:**
- Modify: `tools/staging/asparagus_reference.json`

**Interfaces:**
- Consumes: Task 3 `growth_stages` ids.
- Produces: `tips_by_stage` (a tip per stage id), `watering.schedule_by_stage`, `failure_diagnostics`.

- [ ] **Step 1: Author tips_by_stage**

`tips_by_stage`: a dict keyed by EVERY `growth_stages` id (A12 coverage). Each value: a list of `{"tip_id","sources","evidence_tier","author":{"type":"plant_team"},"added_in":"asparagus_cert_gs_arc","last_reviewed":"2026-07-24","audience","anchoring_urls":{...url+verified...},"text_seasoned","text_beginner"}` (match a certified crop's `tips_by_stage` entry shape exactly).

- [ ] **Step 2: Author watering.schedule_by_stage**

A non-empty list; each `{"stage_id","system","rate","frequency","level","note_seasoned","note_beginner"}` with `stage_id` in the `growth_stages` ids (A39 requires non-empty; establishment year needs steady moisture, established beds are more drought-tolerant).

- [ ] **Step 3: Author failure_diagnostics**

A non-empty list of `{"label","cause_beginner","what_happened_beginner",...}` (match a certified crop's shape). Asparagus-specific: spindly/thin spears (bed too young or over-harvested), no spears (crown too shallow/immature), fern yellowing (rust vs natural fall dieback), rot at crown (Fusarium/poor drainage).

- [ ] **Step 4: Validate on scratch + fidelity + commit**

Run: `python3 tools/staging/asparagus_scratch_merge.py` -- A12 tips-coverage + A39 watering.schedule_by_stage now satisfied. T1-fidelity review. Then:
```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): tips_by_stage + watering schedule + failure diagnostics (T1)"
```

---

### Task 5: Consumer prose + advisory fields

> **Content-authoring task.** Descriptions, hardiness, harvest, storage, notifications, weather_triggers, recipes, tasks, companions, moon_phase. Dual-register; T1 where a claim needs backing.

**Files:**
- Modify: `tools/staging/asparagus_reference.json`

**Interfaces:**
- Consumes: the variety data (for the description fold-in).
- Produces: the remaining top-level prose + advisory fields.

- [ ] **Step 1: Author descriptions with the variety fold-in**

`description_beginner` / `description_seasoned`: the crop overview folding in the recommended varieties (Millennium/Jersey/Mary Washington/Purple Passion) per the berry-pilot fold-in template.

- [ ] **Step 2: Author hardiness + harvest + storage**

`hardiness_notes_beginner`/`_seasoned` (crown deep-hardiness + the dormancy requirement -> ties to the region suitability). `harvest_ready_beginner`/`_seasoned` + `harvest_ready_sources` + `harvest_ready_anchoring_urls` (spears 6-9 in, tips tight, snap-harvest; stop cutting after 6-8 weeks) + `harvest_urgency`. `storage` (fresh spears upright in water / crisper, blanch-freeze).

- [ ] **Step 3: Author notifications + weather_triggers**

`notifications`: non-empty list (match certified shape: `title_seasoned/_beginner`, `body_seasoned/_beginner`). Asparagus: "stop cutting" reminder, first-year "don't harvest" reminder, fall fern-removal (beetle/rust sanitation). `weather_triggers`: non-empty (frost -> fern dieback expected; heat during establishment).

- [ ] **Step 4: Author companions + rotation + moon_phase + tasks/recipes**

`companions`: if authored, each `{name, why_seasoned/_beginner, provenance:{label,confidence}, timing?}` (A19/A26/A27; tomatoes + basil are the traditional asparagus companions -- provenance `traditional`/low unless a T1 trial backs it). `rotation`: already prose (permanent no-rotate). `moon_phase_preference`, `tasks`, `recipes`: conventional (not gate-blocking) -- author lightly.

- [ ] **Step 5: Validate on scratch + fidelity + commit**

Run: `python3 tools/staging/asparagus_scratch_merge.py` -- A12 notifications/weather_triggers + B/A29/A36 dual-register prose now satisfied (regions still pending). T1-fidelity review of any backed claim. Then:
```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): descriptions, hardiness, harvest, storage, notifications, companions (T1)"
```

---

### Task 6: All 16 regions -- 39 zone cells with suitability + calendars

> **Content-authoring task, the largest.** Author a full established-bed cell for every zone in every region's `EXPECTED_SPANS`, with the suitability map from the spec §5. The executor MAY sub-batch by suitability tier for reviewability, but all cells land before the task's commit.

**Files:**
- Modify: `tools/staging/asparagus_reference.json` (the `regions` object)

**Interfaces:**
- Consumes: `zone_span_gate.EXPECTED_SPANS`, the A46 suitability enum, the §5 map.
- Produces: 16 regions, 39 cells, all gate-clean.

- [ ] **Step 1: Author every region + cell**

For EACH of the 16 regions, author: `region_id`, `region_label` (from the canonical's existing region labels), `zone_span` == `EXPECTED_SPANS[region]` (strings, ascending), `plantings: [{"succession_id":1,"label":"crowns","track":"perennial"}]`, `region_notes_beginner` + `region_notes_seasoned`, `sources`. For EACH zone in the span, a `resolved_by_zone.<z>` cell:
- `suitability` per the §5 map (per-cell -- a region may mix, e.g. ca_south_coast z9/z10 `marginal`, z11 `unsuitable`).
- `calendar` (length-12): productive cells (`perennializes`/`marginal`) = `cold_pause... -> harvest (spring spears, timed to the zone's frost) -> growing (summer fern) -> cold_pause (fall dieback)`, adjusting harvest-month placement to the zone's real frost dates. `unsuitable` cells = all-`growing` (12x) -- honest "it just sits and declines," exempt from A34/A37.
- `marginal`/`unsuitable` cells: `suitability_note_seasoned` + `suitability_note_beginner` (the dormancy/heat reason).
- `resolution_method: "frost_anchored_resolved"`, optional `notes`, `sources` + `anchoring_urls` ({url, verified}).
- OMIT `plant_out`/`harvest`/`harvest_start`/`harvest_end`/`start_indoors` (established permanent bed -- no annual planting/harvest window strings; the crown-planting window lives in `start_method`/`year_one_notes`).

Suitability map (§5): perennializes = northern_tier(3-7), warm_arid(8), utah_dixie(8), mid_atlantic(7,8), mid_south(7,8), pnw(8,9), ca_interior(8,9), nevada(8,9); marginal = nevada(10), se_gulf(8,9,10 -- T1-verify whether z8 perennializes), ca_north_coast(9,10), ca_south_coast(9,10), ca_desert(9); unsuitable = ca_south_coast(11), ca_desert(10,11), low_desert_az(9,10), rgv(9,10), fl_peninsula(10,11), hawaii_tropical(10,11,12,13). Every call T1-verified; prefer the conservative tier on thin/conflicting sources and record a low-severity `open_finding` where confidence is low.

- [ ] **Step 2: Validate coverage + parity + coherence on scratch**

Run: `python3 tools/staging/asparagus_scratch_merge.py`
Then run the certified-crop gates directly on the scratch canonical:
```bash
SCRATCH=/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad/asparagus_scratch_canonical.json
python3 tools/coverage_floor_gate.py "$SCRATCH"   # A31: 16 regions
python3 tools/zone_span_gate.py "$SCRATCH"        # A45: span parity (needs status verified_gs_arc -- see Task 8; run again post-Task-8)
python3 tools/cross_consistency_gate.py "$SCRATCH" # A34: 0 (carve-out holds on real cells)
python3 tools/calendar_coherence_gate.py "$SCRATCH" # A37: 0
```
Expected: A31 satisfied (16 regions), A34/A37 = 0 on the productive cells. (A45 fully checks only once `status:"verified_gs_arc"` -- re-run after Task 8.)

- [ ] **Step 3: T1-fidelity review (suitability calls) + commit**

Dedicated T1-fidelity review of every suitability call + harvest-window month placement against FETCHED regional T1 sources (esp. the ca_interior Delta z9 = perennializes claim and every `marginal`/`unsuitable` boundary). Fix/drop unverified calls. Then:
```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): all 16 regions, 39 zone cells with suitability + calendars (T1)"
```

---

### Task 7: IPM fuller set + variety resistance keys

> **Content-authoring task.** Extend the reference's 3 ladders to ~5 (add cutworm + purple spot) and extend the variety `resistance` maps to the enlarged disease set. T1-only per grade.

**Files:**
- Modify: `tools/staging/asparagus_reference.json` (`pests`, `diseases`, `varieties.recommended[].resistance`)

**Interfaces:**
- Consumes: `control_methods` catalog ids, `diseases[].id`.
- Produces: the fuller pest/disease set + resistance maps; clean against control_ladder_gate + variety_resistance_gate.

- [ ] **Step 1: Add the cutworm pest ladder**

Append to `pests` a `{"id":"cutworm","type":"insect","name":"Cutworms","control_ladder":[...]}` using existing `control_methods` ids (`garden_sanitation`, `handpick`, `stem_collars`, `beneficial_nematodes`, `bt`/`spinosad`, `pyrethroid`). Each rung `note_beginner` (+ `note_seasoned` where useful), T1-sourced. If a rung needs a method with no catalog home, add ONE new `control_methods` entry from a FETCHED T1 page (never broaden an existing method on an unsupported claim) -- flag it for the Task 9 catalog add.

- [ ] **Step 2: Add the purple spot disease ladder**

Append to `diseases` a `{"id":"purple-spot","type":"fungal","name":"Purple spot (Stemphylium)","control_ladder":[...]}` (`resistant_varieties`?, `airflow_spacing`, `garden_sanitation` [fern removal], `sulfur` or `copper_fungicide`), T1 (MSU/UMass name it a fern + spear-blemish disease favored by wet residue).

- [ ] **Step 3: Extend variety resistance maps**

For each recommended variety, extend `resistance` to the enlarged disease id set ONLY where a T1 grade exists (keys in {`asparagus-rust`,`fusarium-crown-rot`,`purple-spot`}; grades in {immune,resistant,tolerant,susceptible}). E.g. Millennium: MSU rates it more susceptible to rust AND purple spot -> `{"asparagus-rust":"susceptible","purple-spot":"susceptible"}`; Jersey Knight class tolerance -> `tolerant` where MSU/UC IPM support it. NEVER add an unsourced grade (the design half caught a fabricated Millennium rust=resistant). Cross-check each grade on the FETCHED page (raw HTML/PDF).

- [ ] **Step 4: Validate + fidelity + commit**

Run: `python3 tools/staging/asparagus_scratch_merge.py` -- control_ladder (ladder + identity) + variety_resistance clean; all ladder `method` ids resolve; every resistance key in `diseases[].id`. T1-fidelity review of every ladder claim + resistance grade. Then:
```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): fuller IPM (cutworm + purple spot) + variety resistance (T1)"
```

---

### Task 8: Finalize verification_status + full staged whole_crop_gate PASS

**Files:**
- Modify: `tools/staging/asparagus_reference.json` (`verification_status`)

**Interfaces:**
- Consumes: the fully-authored reference (Tasks 2-7).
- Produces: a staged asparagus that passes a full `whole_crop_gate` on the scratch canonical.

- [ ] **Step 1: Author verification_status**

Set:
```json
"verification_status": {
  "status": "verified_gs_arc",
  "phase": "asparagus_herbaceous_perennial_cert_gs_arc",
  "date": "2026-07-24",
  "launch_ready_core": true,
  "launch_ready_seasoned": true,
  "last_audited": "2026-07-24",
  "source_set": [ ...every source id cited anywhere in the crop... ],
  "verification_log_ref": " ...the cert narrative: archetype, dormancy modeling, the A34/A37 carve-out, the 16-region suitability calls + their confidence, T1 resistance grades... ",
  "open_findings": [ ...any low-severity modeling flags (e.g. thin-source suitability cells); each {id, summary, severity:"low", blocks_launch:false, status:"open"}... ],
  "field_additions": [ {"field":"timing_spine","date":"2026-07-24","sources":[...T1...],"note":"propagule=crown, dtm_anchor absent (days_to_maturity empty perennial N/A)"}, {"field":"category","date":"2026-07-24","note":"new Perennial Vegetables category (UC: perennial stem vegetable, not fruiting)"} ]
}
```
No `open_findings` entry may have `blocks_launch:true` unresolved (gate G).

- [ ] **Step 2: Full staged gate PASS**

Run: `python3 tools/staging/asparagus_scratch_merge.py`
Then: 
```bash
SCRATCH=/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad/asparagus_scratch_canonical.json
python3 tools/whole_crop_gate.py asparagus "$SCRATCH" | tail -3
python3 tools/zone_span_gate.py "$SCRATCH"   # A45 now fully checks (status is verified_gs_arc)
```
Expected: `GATE: PASS` for asparagus on the scratch canonical; A45 zone_span 0 violations. If any A-gate fails, fix in the relevant field and re-run (do NOT proceed to promote until the scratch gate is green).

- [ ] **Step 3: Commit**

```bash
git add tools/staging/asparagus_reference.json
git status --short
git commit -m "content(asparagus): verification_status verified_gs_arc; full staged whole_crop_gate PASS"
```

---

### Task 9: PROMOTE -- the atomic canonical splice

**Files:**
- Create: `tools/promote_asparagus.py`
- Modify: `crops_data_final.json` (the one write) + any `source_catalog` / `control_methods` additions

**Interfaces:**
- Consumes: the finalized staged reference, the canonical.
- Produces: the canonical with asparagus certified (119 -> 120), catalog additions merged, compact-dumped.

- [ ] **Step 1: Snapshot the base canonical (for release_verify --base)**

```bash
cp crops_data_final.json /private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad/asparagus_base_ccf5e890.json
shasum -a 256 crops_data_final.json   # confirm still ccf5e890 before writing
```

- [ ] **Step 2: Write + run the splice**

Create `tools/promote_asparagus.py`: load canonical, replace the `asparagus` crop dict with the staged reference's `crop`; merge any NEW `source_catalog` ids (T1, full publisher/url) + `control_methods` ids the reference introduced; `json.dump(data, f, separators=(",",":"), ensure_ascii=False)` with NO trailing newline; print the added catalog ids + the new certified count. Run it.

- [ ] **Step 3: Confirm the footprint is asparagus-only**

```bash
python3 - <<'PY'
import json
base = json.load(open("/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad/asparagus_base_ccf5e890.json"))
new = json.load(open("crops_data_final.json"))
bc = {c["slug"]: c for c in base["crops"]}; nc = {c["slug"]: c for c in new["crops"]}
changed = [s for s in nc if s not in bc or nc[s] != bc.get(s)]
print("changed crops:", changed)   # expect ['asparagus'] only
print("certified:", sum(1 for c in new["crops"] if (c.get("verification_status") or {}).get("status")=="verified_gs_arc"))  # expect 120
print("total crops:", len(new["crops"]))  # expect 128
PY
git diff --stat crops_data_final.json
```
Expected: `changed crops: ['asparagus']`, certified 120, total 128. (Catalog additions, if any, are top-level keys -- confirm they are the only other diff.)

- [ ] **Step 4: Commit**

```bash
git add crops_data_final.json tools/promote_asparagus.py
git status --short
git commit -m "feat(asparagus): promote to certified GS crop #120 (herbaceous_perennial)"
git show --stat HEAD | head -8
```

---

### Task 10: CERT GAUNTLET + T1 source-truth sample

**Files:**
- Create: `docs/reviews/notes/2026-07-24/asparagus_cert_verification.md`

**Interfaces:**
- Consumes: the promoted canonical.
- Produces: the gauntlet record (protocol #6).

- [ ] **Step 1: Run the full gauntlet**

```bash
python3 tools/whole_crop_gate.py asparagus crops_data_final.json | tail -3        # GATE: PASS
python3 tools/gate_all.py crops_data_final.json                                    # 120/120 PASS
python3 tools/control_ladder_gate.py crops_data_final.json                         # 0 violations
python3 tools/variety_resistance_gate.py crops_data_final.json                     # 0 violations
python3 tools/cross_consistency_gate.py crops_data_final.json                      # 0 (A34 carve-out)
python3 tools/calendar_coherence_gate.py crops_data_final.json                     # 0 (A37 carve-out)
python3 tools/release_verify.py crops_data_final.json \
   --base /private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad/asparagus_base_ccf5e890.json \
   --slug asparagus
```
Expected: whole_crop_gate PASS; gate_all 120/120; ladder/resistance/A34/A37 all 0. release_verify: invariants A/B/C/D clean; the E/G exemplar checks compare asparagus cells against `lettuce-leaf`, which predates the `suitability` convention -- expect the same `suitability`/`suitability_note_*` novel-key notes trees produce; ATTEST these as the herbaceous-perennial convention (not a blocker), exactly as documented for tree cells. Record every result verbatim.

- [ ] **Step 2: Re-run the A34/A37 RED battery on the promoted shape**

Confirm the carve-out still catches the defect for annuals AND passes asparagus, on the real canonical (regression + green + scope: gate_all 120/120).

- [ ] **Step 3: T1 source-truth sample**

Sample ~8-10 authored claims across areas (a ph/spacing/germ numeric, 2-3 resistance grades, 3-4 suitability calls incl. ca_interior z9 + a marginal boundary, an IPM ladder claim). Re-FETCH each source page (raw HTML/PDF) and confirm the datum. Record pass/fix for each.

- [ ] **Step 4: Write the verification note + commit**

Create `docs/reviews/notes/2026-07-24/asparagus_cert_verification.md` recording all Step 1-3 results (the gauntlet greens, the release_verify attestations, the source-truth sample). Then:
```bash
git add docs/reviews/notes/2026-07-24/asparagus_cert_verification.md
git commit -m "docs(asparagus): cert gauntlet + T1 source-truth verification record"
```

---

### Task 11: STATE TRIO + field-addition register

**Files:**
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`, `docs/field_addition_register.md`

**Interfaces:**
- Consumes: the promoted canonical + its new SHA.
- Produces: the updated live-state surface (CLAUDE.md state-trio rule).

- [ ] **Step 1: New canonical SHA**

```bash
shasum -a 256 crops_data_final.json
```

- [ ] **Step 2: Regenerate/patch CURRENT_STATE.md**

Try `python3 tools/gen_current_state.py` -- BUT the current-state-md-drift lesson warns a naive regen can CORRUPT the hand-maintained file (no `---` separator). Diff the generated output against the current file first; if it would corrupt, hand-edit surgically (bump certified count 119 -> 120, add asparagus to the roster, update the SHA + session prose slots). Confirm the file still parses/reads correctly.

- [ ] **Step 3: Append STATE_HISTORY.md (most-recent-first) + bump LATEST.txt**

Prepend a STATE_HISTORY entry (asparagus cert #120, the A34/A37 carve-out, the 16-region map, the new category, new SHA). Update `LATEST.txt` (SHA + session line, following its existing format).

- [ ] **Step 4: Field-addition register row**

Add a `docs/field_addition_register.md` row for the new `category` value (`Perennial Vegetables`) + note the frontend-grouping handoff to the astro session. (The register also documents the A34/A37 archetype carve-out as a gate change if the register tracks gate changes; follow the file's existing convention.)

- [ ] **Step 5: Commit**

```bash
git add CURRENT_STATE.md STATE_HISTORY.md LATEST.txt docs/field_addition_register.md
git status --short
git commit -m "state(asparagus): certify #120 -- state trio + register (canonical <newsha8>)"
```

---

### Task 12: Checkpoint Trevor (push + astro bump gated)

- [ ] **Step 1: Summarize + await Trevor**

Summarize: asparagus certified #120 (120/120 gate_all, release_verify attested, T1 source-truth sampled), the A34/A37 carve-out, the new `Perennial Vegetables` category, state trio + register updated, all committed local + UNPUSHED. State the two Trevor-gated next steps: (1) the push to origin/main; (2) the plant-astro submodule bump + the new-category frontend handling (astro session -- coordinate; the new category needs graceful rendering before the bump). And the fast-follow: artichoke on the same archetype (re-homing it into Perennial Vegetables). Do NOT push or bump without Trevor's go.

---

## Self-Review

**1. Spec coverage:**
- §2 decision 1 (A34/A37 carve-out) -> Task 1. ✓
- §2 decision 2 (honest-marginal map) + §5 -> Task 6. ✓
- §2 decision 3 (Perennial Vegetables category) -> Task 2 (set) + Task 8 (field_additions) + Task 11 (register/frontend handoff). ✓
- §2 decision 4 (fuller ~5 IPM) -> Task 7. ✓
- §3b (days_to_maturity []) -> Global Constraints + Task 3 Step 3. ✓
- §3c/§3d (16 regions, cell shape) -> Task 6. ✓
- §3e (register floor) -> Task 3 Step 3 + Task 4 Step 2. ✓
- §3f (display/quality fields) -> Tasks 3-5. ✓
- §3g (planting_layout "row") -> Task 2 Step 1. ✓
- §3d anchoring_urls `verified` -> Task 2 Step 3. ✓
- §4 (carve-out + RED-proof) -> Task 1 (+ Task 10 Step 2 re-run). ✓
- §8 promote -> Task 9. ✓
- §9 gauntlet -> Task 10. ✓
- §10 state trio + register -> Task 11. ✓
- §11 sequencing -> Task order 1-12. ✓
- §12 deferred (artichoke, sex-ratio archetype, A39 hard-flip, astro bump, planner A44 dict) -> not built; Task 12 states the fast-follow. ✓

**2. Placeholder scan:** Task 1 (the only pure-code task) carries exact code + exact commands + expected output. Tasks 3-8 are content-authoring tasks: structure, field shapes, ids, gate-validation commands, and source constraints are fully specified; the prose/numerics are authoring targets (a sourcing task cannot pre-embed T1 values), the documented repo pattern (mirrors the design arc's Task 4). Every code artifact (scratch-merge harness, splice footprint check) is complete.

**3. Type consistency:** `herbaceous_perennial_violations` / `ladder_violations(data,crop)` / `identity_violations(crop)` / `resistance_violations(crop)` names match the gate modules (verified via grep; the harness Step 4 re-confirms signatures before first run). The growth_stages ids defined in Task 3 are the exact keys Task 4's tips_by_stage + watering.schedule_by_stage reference. `days_to_maturity:[]` + no `dtm_anchor` is consistent across Global Constraints + Task 3. `verified:"2026-07-24"` + session `asparagus_cert_gs_arc` consistent across Tasks 2/4/8.
