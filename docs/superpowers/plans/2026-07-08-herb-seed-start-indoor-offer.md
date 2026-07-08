# Seed-startable non-seed crops: the full indoor-from-seed OFFER (register #11) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the 12 seed-startable non-seed crops (herbs + pawpaw + onion + shallot) fully offer their
indoor-from-seed path — method prose + `seedling_light`/`tray_sowing`/`pot_up`/`weeks_indoors` — so the app
can walk a user through starting them indoors, while `propagule` + the calendar keep recommending the easy
(transplant/set/division) path.

**Architecture:** A CONTENT + enum-re-adjudication amend over EXISTING register fields (#4/#6/#9), NOT a
new cross-crop field and NOT a re-certification. Author per-crop from T1 sources in five archetype batches;
apply each batch as a SHA-gated, from-guarded canonical patch via `tools/apply_patch.py`; gate every batch
with the full suite; graduate the design to a contract + register row and run the state trio once #11 is
complete. Design + gate-coherence proof: `docs/superpowers/specs/2026-07-08-herb-seed-start-indoor-offer-design.md`.

**Tech Stack:** Python 3 (stdlib only), the repo's gate suite (`tools/*_gate.py`, `gate_all.py`,
`release_verify.py`), `tools/apply_patch.py` (canonical patch applier), git on `main`.

## Global Constraints

- **Canonical JSON is COMPACT**: `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing
  newline, never `indent=2`. `apply_patch.py` already writes COMPACT — never hand-reformat the file.
- **Crop count stays 124.** Only the 12 in-scope crops change per their batch; every other crop byte-identical.
- **No em-dashes in consumer copy** (`start_method.notes_*`): use commas/colons/semicolons/periods. American
  English. Temperatures render `°F` (the degree glyph, never "70 degrees"). "plant" lowercase except at
  sentence start / "Plant Pro".
- **Amend-not-recert.** Fields are appended/flipped on already-certified crops; provenance lives in the
  contract + STATE_HISTORY (the #6/#9 pattern), NOT a per-crop `_anchoring_urls` field and NOT a re-cert.
- **Sourcing = per-crop T1** (extension `.edu` + RHS; KSU pawpaw program for pawpaw) + each crop's own
  certified prose where it already states the method. Original prose, never copied (facts/methods are not
  copyrightable — 17 U.S.C. 102(b)/Feist; same model as register #10).
- **Every apply is SHA-gated + from-guarded**: the batch patch carries `base_sha` = the CURRENT canonical
  SHA at apply time, and every `replace`/`delete` op carries a `from` matching the exact current value.
- **`sow_depth_inches` stays absent** for all 12 (prose-only; `timing_spine_gate` requires it only for
  `SEED_LIKE={seed,clove,set,tuber}` non-microgreens, and a `transplant`/`division` propagule carries none;
  onion/shallot are `set` but adding depth is out of scope for this pass — the depth lives in prose).
- **Trevor confirms every push.** Commit each verified batch; HOLD the push. Batch 1's commit also carries
  the design spec (held from brainstorming per Trevor's instruction).

---

## File Structure

- **Modify:** `crops_data_final.json` — the 12 in-scope crops, via five SHA-gated patches (never hand-edit).
- **Create:** `tools/batches/seed_start_b1_frost_herbs.json` … `_b5_bulb_from_seed.json` — the per-batch
  canonical patch files (`base_sha` + `patches[]`), one per task.
- **Create (Task 6):** `docs/seed_start_method_contract.md` — the graduated register #11 contract.
- **Modify (Task 6):** `docs/field_addition_register.md` (add the #11 row), `LATEST.txt`,
  `STATE_HISTORY.md`, `CURRENT_STATE.md` (the state trio).
- **Already created (brainstorming):** the design spec (committed with Batch 1).

### The batch patch format (`tools/apply_patch.py`)

```json
{
  "base_sha": "<sha256 of the CURRENT crops_data_final.json>",
  "patches": [
    {"op": "replace", "json_path": "crops[?(@.slug=='mint')].seedling_light", "from": "na", "value": "bright_default"},
    {"op": "replace", "json_path": "crops[?(@.slug=='mint')].tray_sowing",    "from": "na", "value": "multi_sow_thin_to_one"},
    {"op": "add",     "json_path": "crops[?(@.slug=='mint')].pot_up",                       "value": "optional"},
    {"op": "replace", "json_path": "crops[?(@.slug=='mint')].start_method.notes_beginner", "from": "<EXACT current string>", "value": "<current + appended from-seed clause>"}
  ]
}
```
`add` targets an ABSENT or empty-equivalent (`null`/`[]`) slot (used for `pot_up`, `weeks_indoors`, and
pawpaw's empty `germination_temp_f`). `replace` is from-guarded (used for the na→value flips, germ_light
null→neutral, and full-string prose swaps). Pull the exact current prose string with
`python3 -c "import json;print(json.load(open('crops_data_final.json'))['crops'][...]['start_method']['notes_beginner'])"`
at authoring time so the `from` guard matches byte-for-byte.

### The Verification Battery (run at the end of EVERY batch task; `SLUGS` = that batch's crops)

```bash
# 1. footprint: EXACTLY the batch crops changed, count still 124, still COMPACT
python3 tools/apply_patch.py tools/batches/<batch>.json          # prints the change footprint
python3 -c "import json;d=json.load(open('crops_data_final.json'));print('count',len(d['crops']))"  # -> 124
# 2. per-crop whole_crop_gate on each changed crop
for s in $SLUGS; do echo "== $s =="; python3 tools/whole_crop_gate.py $s | grep -E 'VIOLATION|GATE:'; done
# 3. register + standalone gates (all must PASS / 0 violations)
python3 tools/seed_tray_gate.py
python3 tools/seedling_light_gate.py
python3 tools/timing_spine_gate.py
python3 tools/register_coverage_gate.py
python3 tools/register_completeness_gate.py
# 4. whole-suite regression on every certified crop
python3 tools/gate_all.py                                        # -> PASS 114/114
# 5. release verify (source-truth + dash/degrees) on the changed crops
python3 tools/release_verify.py --slugs "$(echo $SLUGS | tr ' ' ',')"
```
Expected: every gate PASS / 0 violations; `gate_all` PASS 114/114; `release_verify` no NEW violations
(pre-existing calendar-review notes on untouched regions are expected). If ANY gate fails, STOP — do not
commit; fix the batch patch and re-run. (Design §5 proved the field-flip / null→neutral / wi-add changes
are gate-clean via scratch spikes, so a failure here means an authoring error, not a design flaw.)

---

## Task 1: Batch 1 — frost_anchored herbs (chives, mint, bee-balm, echinacea)

These four already carry `weeks_indoors`; Batch 1 flips the seedling/tray fields + authors the prose gaps.
`SLUGS="chives mint bee-balm echinacea"`.

**Files:**
- Create: `tools/batches/seed_start_b1_frost_herbs.json`
- Modify: `crops_data_final.json` (these 4 crops)
- Commit also: `docs/superpowers/specs/2026-07-08-herb-seed-start-indoor-offer-design.md` (held from brainstorming)

**Deterministic field values (no ambiguity — apply exactly):**
- chives: `seedling_light` na→`bright_default`; `tray_sowing` na→`multisow_clump`; `pot_up` +`not_needed`.
- mint: `seedling_light` na→`bright_default`; `tray_sowing` na→`multi_sow_thin_to_one`; `pot_up` +`optional`.
- bee-balm: `seedling_light` na→`bright_default`; `tray_sowing` na→`multi_sow_thin_to_one`; `pot_up` +`optional`.
- echinacea: `seedling_light` na→`bright_default`; `tray_sowing` na→`multi_sow_thin_to_one`; `pot_up` +`optional`.

**Interfaces:**
- Produces: canonical with these 4 crops carrying a real `tray_sowing`+`pot_up`+`bright_default`; the
  next batch reads the NEW canonical SHA as its `base_sha`.

- [ ] **Step 1: Source the prose gaps (T1).** For the two crops with a genuine prose gap, extract:
  - **mint** (germ_light `light_required`, wi 6): confirm surface-sow (seed needs light, do not cover) +
    that seed is off-type/variable, from a T1 extension mint seed-starting page (e.g. a `.edu`). The steer
    ("division/cutting, not seed") is already authored and STAYS; we add only an honest "if you do start
    from seed" clause.
  - **echinacea** (germ_light `light_required`, wi 8): confirm the missing light instruction — barely
    cover / surface-sow because light aids germination — from a T1 page (e.g. Johnny's or a `.edu`);
    stratification + 65-70°F + 10-20 day + transplant-ready 20-28 day facts are already authored.
  - chives + bee-balm are COVERED; verify their existing prose is coherent with the new `tray_sowing`
    (chives already implies pinch-per-cell/transplant-the-clump → `multisow_clump`; bee-balm already has
    the cool-moist note) and touch ONLY if incoherent.

- [ ] **Step 2: Author the prose (dual-register, both `notes_beginner` + `notes_seasoned`).** Requirements:
  - mint: append one honest clause to each register, e.g. beginner *"If you do want to try seed, press it
    onto the surface and do not cover it, since the seed needs light to sprout; start it indoors about 6
    weeks before the last frost, but expect uneven, variable plants."* Seasoned: same fact, seasoned voice,
    aligned to germ_temp 60-70°F. No em-dash; `°F` glyph if a temp is stated.
  - echinacea: insert the light instruction into the existing from-seed sentence, e.g. *"…surface-sow or
    barely cover the seed, since light aids germination…"* Keep every existing fact.
  - chives/bee-balm: only if Step 1 found an incoherence.

- [ ] **Step 3: Build the batch patch.** Set `base_sha` = current `shasum -a 256 crops_data_final.json`.
  Add the deterministic field ops (above) + any from-guarded prose `replace` ops (pull the EXACT current
  `notes_*` strings for the `from` guards). Save to `tools/batches/seed_start_b1_frost_herbs.json`.

- [ ] **Step 4: Dry-run the patch.** Run: `python3 tools/apply_patch.py tools/batches/seed_start_b1_frost_herbs.json --dry-run`
  Expected: footprint lists EXACTLY chives/mint/bee-balm/echinacea; no SHA/from-guard error. If a from-guard
  fails, the current string drifted — re-pull it. Do NOT proceed on any guard failure.

- [ ] **Step 5: Apply + run the Verification Battery** (defined above) with `SLUGS="chives mint bee-balm echinacea"`.
  Expected: all gates PASS; `gate_all` 114/114; `release_verify` no new violations; `seed_tray_gate --coverage`
  shows `multisow_clump` count 2 (spring-onion + chives). If all green, proceed; else STOP and fix.

- [ ] **Step 6: Commit (HOLD the push).**
```bash
git add crops_data_final.json tools/batches/seed_start_b1_frost_herbs.json \
        docs/superpowers/specs/2026-07-08-herb-seed-start-indoor-offer-design.md
git commit -m "feat(register-11): batch 1 frost-anchored herbs -- indoor-from-seed offer (chives/mint/bee-balm/echinacea)

chives -> multisow_clump (2nd live member); mint/bee-balm/echinacea -> multi_sow_thin_to_one.
seedling_light na->bright_default + pot_up added; mint/echinacea from-seed prose gaps authored (T1).
Design spec included. Gate battery + gate_all 114/114 + release_verify clean. SHA-guarded, COMPACT.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
  Then summarize to Trevor and HOLD for his push confirmation.

---

## Task 2: Batch 2 — steer-away woody herbs (lavender, rosemary)

The `light_required` woody herbs we deliberately steer AWAY from seed. Add `weeks_indoors` + the honest "if
you do start from seed" clause that surfaces `germination_light` without overselling. `SLUGS="lavender rosemary"`.

**Files:**
- Create: `tools/batches/seed_start_b2_steer_away_woody.json`
- Modify: `crops_data_final.json` (lavender, rosemary)

**Deterministic field values:**
- lavender: `seedling_light` na→`bright_default`; `tray_sowing` na→`multi_sow_thin_to_one`; `pot_up`
  +`optional`; `weeks_indoors` +`<N>` (source at Step 1; expected ~10-12).
- rosemary: same shape; `weeks_indoors` +`<N>` (expected ~10-12).

**Interfaces:**
- Consumes: canonical SHA after Task 1 (its `base_sha`).
- Produces: two `perennial_woody_ornamental` crops carrying `weeks_indoors` + the flip (Design §5 spike
  proved lavender clears every gate with exactly this change).

- [ ] **Step 1: Source (T1) the from-seed reality + the indoor-start timing.** Per crop extract, from an
  extension `.edu` + RHS: (a) the exact `weeks_indoors` (weeks before last frost to start indoors),
  (b) the pre-treatment — **lavender** benefits from a cold-moist stratification (~2-4 weeks); confirm from
  T1 whether it's recommended, and whether a soak is real (Trevor noted the Grow It app says soak ~15 min —
  do NOT adopt it unless a T1 source backs it), (c) that seed is slow/erratic + off-type (lavender ~100-200
  days to plantable; rosemary can take ~3 years to size; named cultivars don't come true). rosemary: no
  stratification; surface-sow (needs light), bottom heat ~70°F.

- [ ] **Step 2: Author the "if you do start from seed" clause** (both registers, both crops). Keep each
  crop's existing steer ("buy a plant / take a cutting") verbatim; APPEND an honest clause:
  - lavender beginner (illustrative shape — final wording from the sourced facts): *"If you do want to grow
    it from seed, surface-sow it because the seed needs light to sprout, chill it damp in the fridge for a
    few weeks first to improve germination, and keep it around 70°F; be patient, since it sprouts slowly and
    unevenly and the plants vary from the parent."* Seasoned: same facts, seasoned voice, include the
    `weeks_indoors` timing ("start indoors about N weeks before the last frost").
  - rosemary: parallel clause — surface-sow (needs light), warmth ~70°F, very slow/erratic (~3 years to a
    mature plant), off-type; the existing cutting method STAYS.
  - No em-dash; `°F` glyph; American English.

- [ ] **Step 3: Build the batch patch** (`base_sha` = current SHA; deterministic ops + from-guarded prose
  `replace`). Save to `tools/batches/seed_start_b2_steer_away_woody.json`.

- [ ] **Step 4: Dry-run.** `python3 tools/apply_patch.py tools/batches/seed_start_b2_steer_away_woody.json --dry-run`
  Expected: footprint = exactly lavender/rosemary; no guard error.

- [ ] **Step 5: Apply + Verification Battery** with `SLUGS="lavender rosemary"`. Expected: all green,
  including `whole_crop_gate` on both (the woody-ornamental A13/A14 branch is unaffected by these fields —
  proven in the spike). STOP on any failure.

- [ ] **Step 6: Commit (HOLD).**
```bash
git add crops_data_final.json tools/batches/seed_start_b2_steer_away_woody.json
git commit -m "feat(register-11): batch 2 steer-away woody herbs -- lavender/rosemary indoor-from-seed offer

weeks_indoors added (T1) + seedling_light/tray_sowing/pot_up flip; honest 'if you do start from seed'
clause surfaces germination_light (surface-sow/light) without overselling; existing steer kept.
Gate battery + gate_all 114/114 + release_verify clean. SHA-guarded, COMPACT.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Batch 3 — covered/partial woody herbs (oregano, sage, thyme)

Mostly-covered woody herbs needing `weeks_indoors` + a prose touch. `SLUGS="oregano sage thyme"`.

**Files:**
- Create: `tools/batches/seed_start_b3_woody_covered.json`
- Modify: `crops_data_final.json` (oregano, sage, thyme)

**Deterministic field values:**
- oregano: `seedling_light` na→`bright_default`; `tray_sowing` na→`multi_sow_thin_to_one`; `pot_up`
  +`optional`; `weeks_indoors` +`<N>` (expected ~6-8).
- sage: same shape; `weeks_indoors` +`8` (its prose already says "indoors 8-10 weeks before frost" — pick 8).
- thyme: same shape; `weeks_indoors` +`<N>` (expected ~8-10).

- [ ] **Step 1: Source (T1) the indoor-start weeks + confirm the depth/light facts.** oregano: "needs
  light, do not cover, ~4 days in warm soil" is already authored — source only the indoor-start weeks.
  sage: germ_light neutral (barely cover ~1/8-1/4 in); timing already authored, confirm wi=8. thyme:
  fine seed, germ_light neutral (surface/barely cover), slow/uneven; source the indoor-start weeks.

- [ ] **Step 2: Author the prose touch** (both registers where a gap exists):
  - oregano: add the indoor-start timing to the existing from-seed sentence ("…start indoors about N weeks
    before the last frost…"); keep "needs light, do not cover".
  - sage: add the sowing depth if absent (barely cover the seed); keep the existing 8-10 week timing.
  - thyme: add the indoor path — surface to barely cover the fine seed, start indoors ~N weeks before
    frost, expect slow/uneven germination; the direct-sow sand tip STAYS.
  - No em-dash; `°F`; American English.

- [ ] **Step 3: Build the patch** (`base_sha` = current SHA). Save `tools/batches/seed_start_b3_woody_covered.json`.
- [ ] **Step 4: Dry-run.** Expected footprint = exactly oregano/sage/thyme; no guard error.
- [ ] **Step 5: Apply + Verification Battery** with `SLUGS="oregano sage thyme"`. Expected all green.
- [ ] **Step 6: Commit (HOLD).**
```bash
git add crops_data_final.json tools/batches/seed_start_b3_woody_covered.json
git commit -m "feat(register-11): batch 3 woody herbs oregano/sage/thyme -- indoor-from-seed offer

weeks_indoors added (T1) + seedling_light/tray_sowing/pot_up flip; indoor-start timing + depth prose
touches (their germination method was largely authored). Gate battery + gate_all 114/114 + release_verify
clean. SHA-guarded, COMPACT.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Batch 4 — pawpaw (the honest exception)

pawpaw keeps `seedling_light`/`tray_sowing` = `na` (shade seedling, deep-pot single seed — NOT a bright
cell-tray crop); it gets the full stratification METHOD in prose + a filled `germination_temp_f`.
`SLUGS="pawpaw"`.

**Files:**
- Create: `tools/batches/seed_start_b4_pawpaw.json`
- Modify: `crops_data_final.json` (pawpaw)

**Deterministic field values:**
- pawpaw: `germination_temp_f` `[]`→`[<lo>,<hi>]` (source at Step 1; expected ~[70,85] warm soil after
  stratification). NO change to `seedling_light`/`tray_sowing` (stay `na`), NO `pot_up`, NO `weeks_indoors`.

- [ ] **Step 1: Source (T1, Kentucky State University pawpaw program + one extension `.edu`).** Extract:
  recalcitrant seed (must never dry out); cold-MOIST stratification duration (~90-120 days) and method
  (damp sphagnum in the fridge at ~40°F, or a fall outdoor sowing); the warm-soil germination band for
  `germination_temp_f`; the deep-taproot / tall-deep-pot / one-seed-per-container detail; that the seedling
  needs shade its first year or two. Confirm the exact stratification days + germination temps from KSU.

- [ ] **Step 2: Author the from-seed method** (both `notes_beginner` + `notes_seasoned`), APPENDED to the
  existing potted-tree narrative (which STAYS as the recommended path). Requirements: honest that it's a
  slow project; the seed must never dry out; ~3 to 4 months of cold, moist chilling before it germinates in
  warm soil; sow one seed in a tall, deep pot for the taproot; shade the seedling; most home growers buy a
  potted grafted tree. No em-dash; `°F` glyph for every temp; American English. Example seasoned shape:
  *"From seed, pawpaw is a patient project: the seed cannot be allowed to dry out and needs about 3 to 4
  months of cold, moist stratification (damp sphagnum in the refrigerator near 40°F, or a fall outdoor
  sowing) before it germinates in warm soil around 75 to 85°F the following season. It drives a deep,
  brittle taproot first, so sow one seed in a tall, deep pot and shade the seedling; most growers skip all
  this and start with a potted grafted tree."*

- [ ] **Step 3: Build the patch** (`base_sha` = current SHA): the `germination_temp_f` `add`
  (empty `[]` is empty-equivalent → `add`) + the two from-guarded prose `replace` ops. Save
  `tools/batches/seed_start_b4_pawpaw.json`.

- [ ] **Step 4: Dry-run.** Expected footprint = exactly pawpaw; no guard error. Confirm `seedling_light` +
  `tray_sowing` are NOT in the patch (they must stay `na`).

- [ ] **Step 5: Apply + Verification Battery** with `SLUGS="pawpaw"`. Additionally confirm
  `seedling_light_gate --coverage` still shows pawpaw under `na` (unchanged) and germ-light SET count
  unchanged. Expected all green.

- [ ] **Step 6: Commit (HOLD).**
```bash
git add crops_data_final.json tools/batches/seed_start_b4_pawpaw.json
git commit -m "feat(register-11): batch 4 pawpaw -- from-seed stratification method (prose) + germination_temp_f

Full cold-moist stratification method authored (KSU pawpaw program); germination_temp_f filled to the
sourced warm-soil band. seedling_light/tray_sowing stay 'na' (shade seedling, deep-pot single seed --
not a bright cell-tray crop); the honest exception. Gate battery + gate_all 114/114 + release_verify
clean. SHA-guarded, COMPACT.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Batch 5 — bulb-from-seed (onion, shallot)

The `germination_light` null→neutral re-adjudication + the flip. Their method prose already teaches
from-seed, so this is mostly the field change + a verify/light-touch. `SLUGS="onion shallot"`.

**Files:**
- Create: `tools/batches/seed_start_b5_bulb_from_seed.json`
- Modify: `crops_data_final.json` (onion, shallot)

**Deterministic field values:**
- onion: `germination_light` `null`→`neutral`; `seedling_light` na→`bright_default`; `tray_sowing` na→
  `multi_sow_thin_to_one`; `pot_up` +`optional`. (`weeks_indoors` already 10.)
- shallot: same shape. (`weeks_indoors` already 8.)

**Interfaces:**
- Consumes: canonical SHA after Task 4.
- Produces: germ-light-null count drops 29→27; both crops now offer the from-seed path they already describe.
  (Design §5 spike proved null→neutral + flip is gate-clean; the `propagule=='seed'` null rule does not fire
  on a `set` propagule.)

- [ ] **Step 1: Verify the existing prose already teaches the from-seed method** (it does: onion "Seeds
  give the biggest bulbs but take the longest"; shallot "grow shallots from seed, started indoors about 8 to
  10 weeks early, which gives single bulbs"). Confirm `germination_light=neutral` is correct (onion/shallot
  seed is covered-sown ~1/4 to 1/2 in, light-indifferent) from a T1 `.edu` allium seed page. Light touch
  ONLY if a from-seed fact (depth/light) is missing; the method itself is authored.

- [ ] **Step 2: Author any light touch** (likely none). If added, dual-register, no em-dash, `°F`.

- [ ] **Step 3: Build the patch** (`base_sha` = current SHA): per crop the germ_light `replace` null→neutral
  + seedling_light `replace` na→bright_default + tray_sowing `replace` na→multi_sow_thin_to_one + pot_up
  `add` optional (+ any prose `replace`). Save `tools/batches/seed_start_b5_bulb_from_seed.json`.

- [ ] **Step 4: Dry-run.** Expected footprint = exactly onion/shallot; the germ_light `from` guard is `null`
  (JSON null), not the string "null". No guard error.

- [ ] **Step 5: Apply + Verification Battery** with `SLUGS="onion shallot"`. Additionally confirm
  `seedling_light_gate --coverage` shows germ-light SET +2 / N-A -2. Expected all green.

- [ ] **Step 6: Commit (HOLD).**
```bash
git add crops_data_final.json tools/batches/seed_start_b5_bulb_from_seed.json
git commit -m "feat(register-11): batch 5 bulb-from-seed onion/shallot -- germination_light null->neutral + flip

Their own prose already teaches the from-seed method; germination_light was wrongly closed to null.
null->neutral (set propagule, so the seed-crop-can't-be-null rule does not fire) + seedling_light/
tray_sowing/pot_up flip. germ-light null 29->27. Gate battery + gate_all 114/114 + release_verify clean.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Finalize — contract, register row, full regression, state trio

Close register #11: graduate the design to a contract, log the register row, run the whole suite one final
time, and do the state trio. No canonical change here (docs + state files only).

**Files:**
- Create: `docs/seed_start_method_contract.md`
- Modify: `docs/field_addition_register.md`, `LATEST.txt`, `STATE_HISTORY.md`, `CURRENT_STATE.md`

- [ ] **Step 1: Full-suite final regression.** Run the Verification Battery with
  `SLUGS="chives mint bee-balm echinacea lavender rosemary oregano sage thyme pawpaw onion shallot"`
  (all 12) plus a fresh `gate_all` and `python3 tools/gate_all.py` on the whole roster. Expected: PASS
  114/114, every gate 0 violations, `release_verify` no new violations across all 12.

- [ ] **Step 2: Graduate the contract.** Write `docs/seed_start_method_contract.md` from the design spec:
  the decision (extend the germination_light source-of-truth principle), the 12-crop coverage table with
  FINAL sourced values (weeks_indoors, tray_sowing, germ_light, the pawpaw exception), the per-crop T1
  sources (the provenance record), the gate-coherence proof, and the deferred follow-ons (lemongrass,
  Layer 2 stage arc, Layer 3 region calendar).

- [ ] **Step 3: Add the register row.** Append a `#11` row to `docs/field_addition_register.md`:
  status COMPLETE, the SHA range, the 12 crops, the null→neutral re-adjudication, `multisow_clump` 2 live,
  contract pointer, follow-ons.

- [ ] **Step 4: State trio.** SURGICALLY (do NOT run `gen_current_state.py` — it corrupts the hand-
  maintained `CURRENT_STATE.md`, memory `current-state-md-drift`):
  - `LATEST.txt`: new SHA + session line ("REGISTER #11 SEED-START INDOOR OFFER -- COMPLETE (12 crops)…").
  - `STATE_HISTORY.md`: PREPEND a dated entry beneath the header (most-recent-first) with the full detail
    (the contradiction fixed, the 12 crops, per-batch source-truth sample, gate results, SHA range).
  - `CURRENT_STATE.md`: surgical edit of the live-state surface (roster/coverage lines) to reflect #11.

- [ ] **Step 5: Commit (HOLD).**
```bash
git add docs/seed_start_method_contract.md docs/field_addition_register.md \
        LATEST.txt STATE_HISTORY.md CURRENT_STATE.md
git commit -m "docs(register-11): state trio + contract + register row -- indoor-from-seed offer COMPLETE

Register #11 done: 12 seed-startable non-seed crops fully offer the indoor-from-seed path. Contract
graduated, register row added, state trio (LATEST + STATE_HISTORY + CURRENT_STATE). No canonical change.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 6: Summarize to Trevor** — the 12-crop change, the gate results, the held commits (batches 1-5
  + this finalize), and confirm the whole #11 is ready to push on his word.

---

## Self-review notes (author check against the spec)

- **Spec coverage:** all 12 in-scope crops have a task (B1 chives/mint/bee-balm/echinacea; B2
  lavender/rosemary; B3 oregano/sage/thyme; B4 pawpaw; B5 onion/shallot). pawpaw exception (na/na + prose +
  germ_temp) = Task 4. lemongrass deferral = documented in Task 6 contract, no task (correct). Layer 2/3
  deferred = documented, no task (correct). chives→multisow_clump = Task 1. germ_light null→neutral = Task 5.
- **Provenance:** contract + STATE_HISTORY (Task 6), matching the #6/#9 model — no per-crop field_additions
  (the register enums + weeks_indoors are not `timing_spine_gate.NEW_COLUMNS`, so none is gate-required).
- **Ambiguity:** every deterministic field value is exact; the `(src)`/`<N>` markers are the genuinely
  research-dependent numbers (weeks_indoors, stratification days, germ temps), each with a named T1 target
  and an expected range — resolved at the batch's Step 1, not invented.
- **Guards:** every batch is SHA-gated (`base_sha`) + from-guarded (exact current values) + footprint-checked
  (exactly the batch crops) + full-suite gated + `release_verify`d before commit; every commit is HELD.
