# Dry-Bean GS Anchor — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author, splice, and certify a new `dry-bean` crop to gold-standard (`verified_gs_arc`),
modeled on certified `green-beans-bush`, harvested for mature/cured dry seed — the first net-new crop
carrying the full register stack from birth.

**Architecture:** Clone-and-refit from `green-beans-bush` (same species, *Phaseolus vulgaris*). Author
the record in a scratch staging file (canonical stays READ-ONLY), prove the always-on gate suite
catches injected defects in the new crop (RED), then SHA-guarded COMPACT-splice it via `apply_patch.py`
(`$.crops[N]` append) and certify with the full release suite green (GREEN). The harvest *window* the
app surfaces is the `harvest` growth stage's `day_range_from_sow`, anchored by A40 on `id: "harvest"`.

**Tech Stack:** Python 3 (offline gate tooling in `tools/`), `crops_data_final.json` (single compact
JSON store), git on `main`. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-07-09-dry-bean-gs-anchor-design.md` (read it first).

## Global Constraints

Copied verbatim from the spec + CLAUDE.md; every task inherits these.

- **Canonical is COMPACT:** written with `separators=(",",":")`, `ensure_ascii=False`, **no trailing
  newline**, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json`** until Task 6 (the splice). All authoring happens in a scratch
  staging file. Task 6's write is the only canonical mutation, SHA-guarded.
- **Splice footprint:** EXACTLY one crop object added (`dry-bean`), plus any new `source_catalog` ids.
  All 124 existing crops + every other top-level key **byte-identical**. Count 124 → **125**.
- **No em dashes in consumer copy** (commas/colons/semicolons/periods; `--` is fine in docs/comments).
  American English. Temperatures render `°F`. "plant" lowercase except sentence-start / "Plant Pro".
- **Certified crops carry ZERO non-Tier-1 sources** — university extension (`.edu`) or government only;
  seed companies / almanacs are corroboration-only, never in `source_set` / `sources`.
- **TDD / adversarial (CLAUDE.md):** before trusting any green gate, sneak the defect class at it on a
  SCRATCH copy and confirm it bounces (Task 5). No new gate is expected; if one becomes necessary, build
  it RED-before-GREEN with its own test.
- **`harvest` stage id must be literally `"harvest"`** — A40 (`timing_spine_gate._harvest_index`) anchors
  the ladder + DTM check on it; the fallback is the last stage (would wrongly anchor on `cure_thresh`).
- **Don't commit until Trevor approves; Trevor confirms every push.** Work commits locally on `main`.

**Reference records / tools:** template crop `green-beans-bush` (certified, carries the full register
stack); `tools/apply_patch.py` (SHA-guarded splicer, `op:add` on `$.crops[N]` appends at `index==len`,
reports footprint); `tools/whole_crop_gate.py` (A1-A42 incl. A39 register-coverage, A40 timing-spine);
`tools/gate_all.py` (whole_crop_gate on every certified crop); `tools/release_verify.py`;
`tools/source_truth_sample.py`; `tools/temp_scan.py`; `tools/timing_spine_gate.py`;
`tools/register_coverage_gate.py`; `tools/gen_current_state.py`.

---

### Task 1: T1 source research + data pinning

**Files:**
- Create: `docs/reviews/notes/2026-07-09/dry_bean.md` (research note — sourced data table)

**Interfaces:**
- Produces: the sourced values every later task consumes — `days_to_maturity [min,max]`,
  `sow_depth_inches [min,max]`, `thin_to_inches [min,max]`, per-stage `day_range_from_sow` (germination →
  cure), dry-down/cure guidance (moisture %, dent test), dry-shelled `yield_expectations`, per-variety
  DTMs, and each value's T1 `source_catalog` id.

- [ ] **Step 1: Fetch the T1 dry-bean sources.** Use WebFetch on the dry-bean pages of the extension
  services already in `green-beans-bush`'s `source_set` plus dry-bean-specific pages. Target set (verify
  each resolves to a live `.edu`/`.gov` dry-bean or "beans for drying / shell beans" page):
  - Clemson HGIC — snap/dry beans culture (DTM, spacing, soil temp floor, blossom-drop temp, pests)
  - UMN Extension — growing beans / dry beans (season length, harvest-when-dry guidance)
  - USU Extension — beans in the garden (DTM, soil/air temps, heat-abort)
  - UMD Extension — beans (yield, storage)
  - One dedicated dry-bean **harvest + cure + storage** T1 page (dry-down %, dent/rattle test, cure time,
    airtight dry storage) — e.g. a university "harvesting and storing dry beans" extension article.

- [ ] **Step 2: Extract + pin each number to its source.** Write `dry_bean.md` as a table: `field |
  value | T1 source (catalog id) | verbatim quote`. Cover at minimum: DTM range (expect ~`[85,100]`);
  sow depth (~`[1,1.5]`); in-row spacing / `thin_to` (~`[2,4]`); germination window (~`[7,14]`); the
  dry_down onset and harvest-window days-from-sow; cure duration + target moisture (~13–15%) + dent test;
  dry-shelled yield per 10 ft; heat/frost thresholds (expect 90 / 32); per-variety DTM for Black Turtle,
  Pinto, Navy, Kidney, Jacob's Cattle. Flag any figure where sources disagree (do NOT average silently —
  triangulate and note the call, the green-beans-bush yield-correction precedent).

- [ ] **Step 3: List catalog gaps.** In `dry_bean.md`, list which cited sources already exist in
  `source_catalog` (reuse their ids) and which need a new T1 entry (Task 2). Command to check an id:

  Run: `python3 -c "import json;print('id' in json.load(open('crops_data_final.json'))['source_catalog'])"`

- [ ] **Step 4: Commit the research note.**

```bash
git add docs/reviews/notes/2026-07-09/dry_bean.md
git commit -m "docs(dry-bean): T1 source research + pinned data table"
```

---

### Task 2: source_catalog entries for new dry-bean T1 sources

**Files:**
- Modify (staged in the Task 6 batch, NOT the canonical yet): draft `source_catalog` add-ops in a scratch
  file `scratch/dry_bean_catalog_ops.json`

**Interfaces:**
- Consumes: Task 1 Step 3's catalog-gap list.
- Produces: `add` patches of shape `{"op":"add","json_path":"$.source_catalog.<id>","value":{...}}` for
  the Task 6 splice batch.

- [ ] **Step 1: Draft each new catalog entry** matching the existing `source_catalog` value shape
  (inspect one first): `tier` must be `"T1"`, plus `publisher`/`name`/`url` per the existing schema.

  Run (inspect the shape): `python3 -c "import json;d=json.load(open('crops_data_final.json'))['source_catalog'];k=next(iter(d));import pprint;pprint.pprint({k:d[k]})"`

- [ ] **Step 2: Write the ops to `scratch/dry_bean_catalog_ops.json`** as a JSON array of `add` patches
  (one per new id). If Task 1 found no gaps (all sources already cataloged), write `[]` and skip to Task 3.

- [ ] **Step 3: No commit** (these fold into the Task 6 batch). Note the file path in the plan checklist.

---

### Task 3: Author the crop record — core (non-regional)

**Files:**
- Create: `scratch/dry_bean.json` (the full crop object under construction; NOT yet in the canonical)

**Interfaces:**
- Consumes: Task 1's pinned values.
- Produces: `scratch/dry_bean.json` — a single crop object with every top-level key `green-beans-bush`
  carries EXCEPT a populated `regions` (Task 4). `slug: "dry-bean"`.

- [ ] **Step 1: Clone the template structure.** Extract `green-beans-bush` as the skeleton:

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); c=[x for x in d['crops'] if x['slug']=='green-beans-bush'][0]; json.dump(c, open('scratch/dry_bean.json','w'), indent=2, ensure_ascii=False)"
```
  (indent=2 is fine for the SCRATCH working file; Task 6 re-emits COMPACT into the canonical.)

- [ ] **Step 2: Re-author identity + inherited-but-verified fields.** In `scratch/dry_bean.json`:
  `slug` → `"dry-bean"`; `name` → `"Dry Beans"`; re-check `category`/`type`/`difficulty`/`sunlight`/
  `water`/`spacing_inches`/`soil`/`ph`/`germination_temp_f` against Task 1 (keep template value only where
  a dry-bean T1 source confirms it). Set `weeks_indoors: 0`, `perennial: false`,
  `archetype: "warm_season_fruiting"`.

- [ ] **Step 3: Author the register stack** (from Task 1, per spec §7):
  `propagule: "seed"`, `dtm_anchor: "from_sow"`, `sow_depth_inches: [<t1>]`, `thin_to_inches: [<t1>]`,
  **omit `harvest_window_days`** (one-shot), `germination_light: "neutral"`, `seedling_light: "na"`,
  `tray_sowing: "na"` (no `pot_up` key), `heat_threshold_f: 90` + `heat_effect: <match green-beans-bush>`,
  `frost_tolerance_f: 32`, `frost_effect: "killed"`, `chilling_sensitivity_f: null`.
  Set `days_to_maturity: [<t1>]` and recompute `days_to_maturity_mid`.

- [ ] **Step 4: Author the 7-stage `growth_stages` ladder** (spec §6). Each stage carries `id`, `name`,
  `day_range_from_sow: [min,max]` (pin from Task 1; non-decreasing mins through the `harvest` anchor),
  `audience`, and dual-register `user_action_seasoned`/`user_action_beginner`,
  `what_to_look_for_seasoned`/`what_to_look_for_beginner`, `log_prompt_seasoned`/`log_prompt_beginner`
  (cherry-tomato / green-beans-bush voice; beginner = warm + one teaching aside, seasoned = terse). Ladder:

  1. `germination` `~[7,14]`
  2. `seedling`
  3. `flowering`
  4. `pod_development`
  5. `dry_down` `~[75,90]` — "pods yellowing to brown, not ready to pick; be patient until they rattle"
  6. **`harvest`** (id EXACTLY `"harvest"`) `~[85,100]` — "~90% of pods brown and rattle; harvest across
     this window before pods shatter or fall rain molds them"
  7. `cure_thresh` `~[95,115]` — "cure another 1 to 2 weeks until a bean shatters (not dents) under a
     hammer, then shell and store"

- [ ] **Step 5: Author the harvest-model deltas** (spec §5): `watering.schedule_by_stage[]` per-stage
  (steady through pod-fill, then a **dry-down taper** — stop watering to cure pods on the plant);
  `storage` → dry / airtight / cool-dry / months-to-years (thresh to ~13–15% first); `succession_policy`
  → `suitable: false` with a one-full-season reason; `yield_expectations` → dry-shelled weight (Task 1);
  re-author `harvest_ready_seasoned`/`harvest_ready_beginner` (+`harvest_ready_sources`) and
  `description_seasoned`/`description_beginner` for the dry-down/cure story.

- [ ] **Step 6: Author `varieties.recommended[]`** = Black Turtle, Pinto, Navy, Kidney, Jacob's Cattle,
  each `{name, days_to_maturity, note}` (per-variety DTM from Task 1; note pole/half-runner habit where it
  applies); plus `varieties.note_seasoned`/`note_beginner`, `varieties.sources`, `varieties.anchoring_urls`.

- [ ] **Step 7: Verify inherited arrays are still true for dry beans:** `pests`, `diseases`, `companions`,
  `rotation`, `fertilizer`, `container_notes`, `recipes`, `tips_by_stage`, `notifications`,
  `weather_triggers`, `harvest_urgency`, `moon_phase_preference`, `failure_diagnostics`, `calendar_basis`,
  `sources_summary`. Adjust any that differ (e.g. recipes, harvest_urgency = low for a storable dry crop).
  Set `verification_status` to a DRAFT stub (`status: null`) for now — Task 7 flips it to `verified_gs_arc`.

- [ ] **Step 8: Shape-check the object early** (before regions) by splicing into a throwaway scratch and
  running the register value-shape gates on it:

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); o=json.load(open('scratch/dry_bean.json')); d['crops'].append(o); json.dump(d, open('crops_data_final.scratch.json','w'), separators=(',',':'), ensure_ascii=False)"
python3 tools/timing_spine_gate.py crops_data_final.scratch.json --slugs dry-bean --warnings
```
  Expected: `violations=0` (ladder monotonic through `harvest`; enums valid). A harvest-vs-DTM WARNING is
  acceptable (advisory). Fix any VIOLATION before proceeding. Delete the throwaway scratch after.

- [ ] **Step 9: Commit the core draft.**

```bash
git add scratch/dry_bean.json docs/reviews/notes/2026-07-09/dry_bean.md
git commit -m "feat(dry-bean): author core crop record (non-regional) from green-beans-bush"
```

---

### Task 4: Author the regional calendar (`regions` + `zones`)

**Files:**
- Modify: `scratch/dry_bean.json` (populate `regions` + `zones`)

**Interfaces:**
- Consumes: `green-beans-bush`'s `regions`/`zones` structure as the template; regional T1 planting dates.
- Produces: a complete `regions{}` (all cells `green-beans-bush` carries) refit for the dry-down season.

- [ ] **Step 1: Copy the region skeleton** from `green-beans-bush` into `scratch/dry_bean.json` (same
  region keys, zones, cell structure), then refit each cell's calendar for the LONGER season: dry beans
  need a full ~85–100-day frost-free run plus cure time, so the plant-out window is narrower and the
  harvest is a **single fall dry-down** (no summer succession arms).

- [ ] **Step 2: Set suitability honestly.** In short-season cold regions where the frost-free window
  can't finish a ~95-day dry-down + cure, mark the cell `suitability` marginal / `suitable: false` with a
  sourced reason (do not fabricate a window). Warm/long-season regions carry the full calendar.

- [ ] **Step 3: Re-splice the scratch and run the calendar gates:**

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); o=json.load(open('scratch/dry_bean.json')); d['crops'].append(o); json.dump(d, open('crops_data_final.scratch.json','w'), separators=(',',':'), ensure_ascii=False)"
python3 tools/calendar_coherence_gate.py crops_data_final.scratch.json 2>&1 | tail -5
python3 tools/calendar_basis_gate.py crops_data_final.scratch.json 2>&1 | tail -5
```
  Expected: no new violations attributable to `dry-bean`. Fix, then delete the throwaway scratch.

- [ ] **Step 4: Commit the regional draft.**

```bash
git add scratch/dry_bean.json
git commit -m "feat(dry-bean): author regional planting calendar (single fall dry-down, no succession)"
```

---

### Task 5: Adversarial gate proof (RED) — prove the suite protects the new crop

**Files:**
- Create: `docs/reviews/notes/2026-07-09/dry_bean_gate_proof.md` (record each RED bounce)

**Interfaces:**
- Consumes: `scratch/dry_bean.json` (the finished draft).
- Produces: documented evidence that each defect class bounces — the CLAUDE.md "sneak a defect at it"
  discipline applied to the new crop. No canonical change.

- [ ] **Step 1: Build a clean scratch canonical with dry-bean appended** (the base for injection):

```bash
python3 -c "import json; d=json.load(open('crops_data_final.json')); o=json.load(open('scratch/dry_bean.json')); d['crops'].append(o); json.dump(d, open('crops_data_final.scratch.json','w'), separators=(',',':'), ensure_ascii=False)"
```

- [ ] **Step 2: Inject each defect into a COPY of the scratch and confirm the gate FAILS (exit 1).** For
  each, record the failing message in `dry_bean_gate_proof.md`:
  - **Non-monotonic ladder:** swap `dry_down` and `harvest` `day_range_from_sow` mins →
    `python3 tools/whole_crop_gate.py dry-bean <injected>` must report an A40 "ladder mins non-decreasing
    violated ... up to the harvest anchor" and FAIL.
  - **Missing register field:** delete `germination_light` → A39 register-coverage violation, FAIL.
  - **Absurd DTM:** set `days_to_maturity` to `[3,4]` → `numeric_sanity_gate` (`[7,400]` floor) FAIL.
  - **Em dash in copy:** insert `—` into `description_beginner` → dash scan / `release_verify` FAIL.
  - **`harvest` id renamed:** rename stage 6 id `harvest`→`pick` → confirm the anchor falls back to the
    last stage (`cure_thresh`) and the harvest-vs-DTM WARNING now points past DTM (documents WHY the id
    matters).

- [ ] **Step 3: Confirm the clean draft PASSES** the same gate (the GREEN baseline):

```bash
python3 tools/whole_crop_gate.py dry-bean crops_data_final.scratch.json
```
  Expected: PASS (0 failures). Then delete all injected copies + `crops_data_final.scratch.json`.

- [ ] **Step 4: Commit the proof.**

```bash
git add docs/reviews/notes/2026-07-09/dry_bean_gate_proof.md
git commit -m "test(dry-bean): adversarial RED proofs -- gate suite catches injected defects"
```

---

### Task 6: Splice into the canonical (SHA-guarded, COMPACT)

**Files:**
- Create: `tools/batches/dry_bean_add.json` (the apply_patch batch)
- Modify: `crops_data_final.json` (the ONLY canonical mutation in this plan)

**Interfaces:**
- Consumes: `scratch/dry_bean.json`, `scratch/dry_bean_catalog_ops.json` (Task 2), current canonical SHA.
- Produces: canonical with 125 crops; `dry-bean` present; all else byte-identical.

- [ ] **Step 1: Build the batch.** `base_sha` = current canonical SHA; `patches` = the Task 2 catalog
  add-ops FIRST, then the crop append at `index == len` (124):

```bash
python3 - <<'PY'
import json, hashlib
raw = open('crops_data_final.json','rb').read()
sha = hashlib.sha256(raw).hexdigest()
n = len(json.loads(raw)['crops'])
crop = json.load(open('scratch/dry_bean.json'))
cat = json.load(open('scratch/dry_bean_catalog_ops.json'))
batch = {"base_sha": sha, "patches": cat + [{"op":"add","json_path":f"$.crops[{n}]","value":crop}]}
json.dump(batch, open('tools/batches/dry_bean_add.json','w'), ensure_ascii=False)
print("base_sha", sha, "| appending at $.crops[%d]" % n, "| catalog ops", len(cat))
PY
```

- [ ] **Step 2: Apply to a scratch out + read the footprint report.**

```bash
python3 tools/apply_patch.py tools/batches/dry_bean_add.json --out crops_data_final.scratch.json
```
  Expected footprint: `crops changed: dry-bean` (added), `top-level (non-crops) changed: none`, and
  `catalog +<new ids>` if any. Exit 0. Any SHA mismatch / from-guard failure → stop and reconcile.

- [ ] **Step 3: Footprint audit — every prior crop byte-identical, count 125, COMPACT:**

```bash
python3 - <<'PY'
import json
old = json.load(open('crops_data_final.json'))['crops']
new = json.load(open('crops_data_final.scratch.json'))['crops']
oldmap = {c['slug']: json.dumps(c, sort_keys=True) for c in old}
newmap = {c['slug']: json.dumps(c, sort_keys=True) for c in new}
added = set(newmap) - set(oldmap)
changed = [s for s in oldmap if oldmap[s] != newmap.get(s)]
print("added:", added, "| changed existing:", changed, "| count", len(old), "->", len(new))
raw = open('crops_data_final.scratch.json','rb').read()
print("COMPACT ok:", b', "' not in raw[:200] and not raw.endswith(b'\n'))
assert added == {'dry-bean'} and not changed and len(new) == len(old)+1
print("FOOTPRINT CLEAN")
PY
```
  Expected: `added: {'dry-bean'} | changed existing: [] | count 124 -> 125` and `FOOTPRINT CLEAN`.

- [ ] **Step 4: Promote scratch → canonical** (only after the audit prints FOOTPRINT CLEAN):

```bash
mv crops_data_final.scratch.json crops_data_final.json
python3 -c "import hashlib;print('new canonical SHA', hashlib.sha256(open('crops_data_final.json','rb').read()).hexdigest())"
```

- [ ] **Step 5: Commit the splice** (canonical + batch; do NOT push).

```bash
git add crops_data_final.json tools/batches/dry_bean_add.json
git commit -m "feat(dry-bean): splice new crop into canonical (124 -> 125, additive, SHA-guarded)"
```

---

### Task 7: Certify + full release gate suite (GREEN)

**Files:**
- Modify: `crops_data_final.json` (set `dry-bean.verification_status` to certified)

**Interfaces:**
- Consumes: the spliced canonical.
- Produces: `dry-bean.verification_status.status == "verified_gs_arc"` with a real T1 `source_set` +
  `verification_log`; the whole always-on suite green including `dry-bean`.

- [ ] **Step 1: Author the certification block.** Build a `verification_status` replace op (via
  `tools/apply_patch.py`, from-guarded on the draft stub) setting `status: "verified_gs_arc"`, `phase`,
  `date: "2026-07-09"`, `source_set` (the T1 ids from Task 1, extension/gov only), a `verification_log`
  documenting the independent source-fidelity fetch + any triangulation call, and `field_additions` if
  the timing-spine provenance rule requires it (A40 requires a `field_additions` entry for a certified
  crop carrying the new timing columns — include one keyed `timing_spine` with the T1 sources).

- [ ] **Step 2: Run `whole_crop_gate` on dry-bean — the greenfield register test.**

```bash
python3 tools/whole_crop_gate.py dry-bean
```
  Expected: PASS, with A39 (register coverage) and A40 (timing-spine value shape) both 0 violations —
  proving the crop carries the full register stack natively. Fix any failure at its source.

- [ ] **Step 3: Run the whole suite on every certified crop (18 anchors must stay intact).**

```bash
python3 tools/gate_all.py
python3 tools/release_verify.py
python3 tools/temp_scan.py crops_data_final.json 2>&1 | tail -3
```
  Expected: `gate_all` PASS on all certified crops (now 115); `release_verify` clean (a single-slug
  batch-collateral note is expected/benign); `temp_scan` 0; zero em dashes in dry-bean copy.

- [ ] **Step 4: Per-batch source-truth sample.**

```bash
python3 tools/source_truth_sample.py --slugs dry-bean 2>&1 | tail -20
```
  Expected: sampled dry-bean claims trace to their cited T1 (spot-check DTM + a harvest/cure figure +
  yield against the Task 1 quotes). Record the sample result in `dry_bean.md`.

- [ ] **Step 5: Commit the certification.**

```bash
git add crops_data_final.json
git commit -m "feat(dry-bean): certify -> verified_gs_arc (full register stack native, suite green)"
```

---

### Task 8: App harvest-window verify + handoff

**Files:**
- Create (only if a gap is found): `docs/kickoffs/19-dry-bean-app-harvest-window.md` (plant-app handoff)

**Interfaces:**
- Consumes: the certified `dry-bean` ladder.
- Produces: confirmation the app can render a harvest WINDOW (not a point), or a handoff if it cannot.

- [ ] **Step 1: Verify the timing read.** Confirm `dry-bean`'s ladder resolves correctly from a sow date
  the way `crop-timing.ts` consumes it: the `dry_down` and `harvest` stages' `day_range_from_sow` land in
  fall for a July direct-sow (mirror the brussels-sprouts end-to-end spine check).

```bash
python3 tools/timing_spine_gate.py --slugs dry-bean --warnings
```
  Expected: 0 violations; the `harvest` stage min/max define the window.

- [ ] **Step 2: Check the app render.** Determine whether plant-app renders the `harvest` stage as a
  min→max date **window** or a single point (this is a plant-app repo concern — inspect its consumer, do
  not edit dataset). If it already shows a window, note it and skip Step 3.

- [ ] **Step 3: File the handoff (only if the app shows a point).** Write
  `docs/kickoffs/19-dry-bean-app-harvest-window.md`: the data ships a window (`harvest.day_range_from_sow`)
  + a `dry_down` lead-in; the app should surface "harvest window: [date] to [date]" and the "drying down
  now" card. Commit it.

```bash
git add docs/kickoffs/19-dry-bean-app-harvest-window.md
git commit -m "docs(handoff): plant-app should render dry-bean harvest window (min->max), not a point"
```

---

### Task 9: State trio + summarize for Trevor

**Files:**
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt`

**Interfaces:**
- Consumes: the certified canonical + new SHA.
- Produces: the release state trio; a summary for Trevor. NO push (Trevor confirms).

- [ ] **Step 1: Update `CURRENT_STATE.md`.** Per memory `current-state-md-drift`, a naive
  `gen_current_state.py` regen would CORRUPT the file (no `---` separator) — **hand-maintain surgically**:
  prepend a new most-recent entry (new SHA, "DRY-BEAN GS ANCHOR -- first greenfield crop on the full
  register stack; 124 -> 125; suite green; A39/A40 native"). If `gen_current_state.py` is used, verify
  the diff is ONLY the prepend before saving.

- [ ] **Step 2: Append `STATE_HISTORY.md`** (most-recent first) with the same summary + the from→to SHAs.

- [ ] **Step 3: Bump `LATEST.txt`** — new canonical SHA + `Date: 2026-07-09` + a `Session:` line
  describing the dry-bean certification. Verify the SHA matches:

```bash
shasum -a 256 crops_data_final.json && head -1 LATEST.txt
```
  Expected: the two SHAs match.

- [ ] **Step 4: Commit the state trio.**

```bash
git add CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "docs(state): release dry-bean GS anchor (124 -> 125)"
```

- [ ] **Step 5: Summarize for Trevor** — what changed (new certified `dry-bean`, register stack proven
  native, gates green, app window verified/handed-off), the local commits (unpushed), and what's next
  (the corn spec: warm-season block-planted-grass archetype + corn-family splits). Do NOT push; Trevor
  confirms the push and any plant-astro submodule bump.

---

## Self-Review

- **Spec coverage:** §1 goal → Tasks 3-7. §3 crop model → Task 3 Step 2/6. §4 approach (clone-refit) →
  Task 3 Step 1. §5 snap→dry delta → Task 3 Steps 3-6. §6 ladder + `harvest` id → Task 3 Step 4. §6a app
  window → Task 8. §7 register stack → Task 3 Step 3 + Task 7 Step 2. §8 gates/cert → Tasks 5-7. §9
  beans-family table → (documented in the spec; no build task — correct, they are decided-not-built). §10
  verification → Tasks 7-9. §11 success criteria → Tasks 6-9. §12 open items → resolved in Task 1
  (sourced values) + Task 3 (display name/heat_effect).
- **Placeholder scan:** the `<t1>` markers are genuine data dependencies produced by Task 1, not
  placeholders — each is pinned before use, and the structure/commands are complete. No "TBD/handle
  edge cases" steps.
- **Type consistency:** `scratch/dry_bean.json` is the single object handed Task 3 → 6; `harvest` stage
  id is spelled identically everywhere (Task 3 Step 4, Task 5 Step 2, Global Constraints); the splice
  op shape matches `apply_patch.py`'s documented `{op,json_path,value}` with `$.crops[N]` append.
