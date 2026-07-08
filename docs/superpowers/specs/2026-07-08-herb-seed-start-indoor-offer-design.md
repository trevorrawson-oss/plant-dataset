# Design: the full indoor-from-seed OFFER for the seed-startable non-seed crops (register #11)

**Created 2026-07-08.** Brainstormed + scope-locked with Trevor. Supersedes the narrower framing in
`docs/kickoffs/15-herb-seed-start-method-prose.md` (which scoped "germination METHOD prose only"); the
audit surfaced a deeper data contradiction and Trevor chose the fuller, source-of-truth fix.

Register candidate **#11** in `docs/field_addition_register.md`. Like #10, this is a CONTENT +
enum-re-adjudication arc over EXISTING fields, not a new cross-crop field. On completion it graduates to
`docs/seed_start_method_contract.md` and a #11 register row.

---

## 0. The gap (verified in the canonical, 2026-07-08)

Register #6 gave 10 seed-startable non-seed crops a real `germination_light` (Trevor's source-of-truth
call: record the from-seed fact even when `propagule` recommends a transplant). But #6 keyed
`seedling_light` off "recommended path" (nursery stock -> `na`), and #9 keyed `tray_sowing` off
`seedling_light`, so BOTH cascaded to `na`. The result is a contradiction: **the data asserts an
indoor-from-seed path yet structurally withholds the tools to walk it.**

Seven certified crops carry `weeks_indoors > 0` ("start indoors") while BOTH `seedling_light == na` AND
`tray_sowing == na` ("no indoor seedling phase, no cell-tray phase"). Four of them also carry a real
`germination_light` and prose describing an indoor start (chives literally: "start it indoors 6 to 8 weeks
before the last frost and transplant the young clumps"):

| crop | propagule | wi | germ_light | contradiction |
|---|---|---|---|---|
| chives | division | 6 | neutral | asserts indoor-from-seed, offers only germ light |
| mint | division | 6 | light_required | " |
| echinacea | division | 8 | light_required | " |
| bee-balm | division | 8 | neutral | " |
| onion | set | 10 | **null** | prose ALREADY teaches from-seed ("Seeds give the biggest bulbs") -> null is a wrongly-closed door; **IN scope** (§2), germ_light null->neutral |
| shallot | set | 8 | **null** | prose ALREADY teaches from-seed ("grow shallots from seed... single bulbs") -> **IN scope**, germ_light null->neutral |
| lemongrass | division | 8 | **null (N/A)** | grass grown from division / rooted stalk, NO seed path -> null CORRECT, **deferred** (§7) |

The 5 `perennial_woody_ornamental` herbs (lavender/rosemary/oregano/sage/thyme) and pawpaw show the same
withholding a different way: `weeks_indoors` is unset even where the prose says "start indoors ~8-10 weeks
before frost" (sage), so there is no computable indoor-start date at all.

**Trevor's principle (2026-07-08):** "if we say these can be done indoors and we want to be a source of
truth, I want to be able to offer someone the ability to do it. Just because it's hard doesn't mean people
don't want to do it." (Context: Grow It ships identical boilerplate seed-start directions for every crop.
Per-crop, sourced, dual-register directions that are actually true for THAT plant are the differentiator.)

---

## 1. The decision

**Extend the `germination_light` source-of-truth principle to the rest of the from-seed path.**
`propagule` + the growth-stage timeline + the region calendar keep tracking the RECOMMENDED path (buy a
transplant/division). `start_method` + `seedling_light` + `tray_sowing` + `pot_up` + `weeks_indoors` carry
the fully-sourced ALTERNATIVE from-seed path. The app shows both: "Recommended: transplant" AND "Start from
seed indoors: [complete directions, begin ~N weeks before frost]." Recommend the easy path; never withhold
the hard one.

This re-adjudicates the #6/#9 `na`-for-nursery-stock calls for the genuinely seed-startable crops. That
rule was a rollout CONVENTION, not a gate constraint (proven in §5).

### Scope: all 12 crops, "Layer 1" (directions), per-crop and sourced

The 10 germination_light-SET non-seed crops (the herbs + pawpaw) **plus onion + shallot**, whose own prose
already teaches the from-seed method but whose `germination_light` was wrongly closed to `null` (a #6
re-adjudication, null->neutral). lemongrass stays deferred (genuine no-seed crop, §7).

Per crop that we genuinely offer indoors (all get the prose; eleven get the field flip — **pawpaw is the
honest exception**, §3):
- **Germination METHOD prose** (both registers): pre-treatment (stratify / soak / scarify where real) ->
  depth + light (surface vs barely-cover, driven by `germination_light`) -> temp -> **timing** ("start
  indoors ~N weeks before last frost") -> germination window -> grow-on / transplant -> the honest reality
  (slow / off-type where true; we don't hide it, we also tell you how).
- `seedling_light`: `na` -> `bright_default`
- `tray_sowing`: `na` -> a real value
- `pot_up`: absent -> a real value
- `weeks_indoors`: add a sourced value where unset

**`sow_depth_inches` stays PROSE-only** (kickoff Q1). `timing_spine_gate` requires it only for
`SEED_LIKE = {seed, clove, set, tuber}`; a `transplant`/`division` propagule legitimately carries none, and
adding it would muddy the propagule archetype. The surface-sow / barely-cover instruction lives in prose.

### Explicitly OUT of scope (tracked as follow-ons, NOT done here)

- **Layer 2 — growth-stage arc.** Adding a Germination -> Seedling stage prefix to the 9 crops' certified
  `growth_stages` so the app's stage TRACKER walks the indoor phase. Big authoring lift; re-opens certified
  stages. If the app needs it, its own kickoff.
- **Layer 3 — per-region indoor-start calendar.** Rebuilding `regions.plantings` with indoor-start rows +
  changing `calendar_basis` on the perennials. Destabilizes certified plant-out calendars. Avoid.

The directions + a `weeks_indoors`-computable start date deliver "the ability to do it" without either.

---

## 2. Per-crop plan

Audit verdict = the from-seed METHOD prose state today (COVERED / PARTIAL / GAP). Exact numeric values
marked *(src)* are confirmed from per-crop T1 at authoring, not invented here.

| crop | arch | germ_light | verdict | seedling_light | tray_sowing | pot_up | weeks_indoors | prose action |
|---|---|---|---|---|---|---|---|---|
| **chives** | frost_anchored | neutral | COVERED | bright_default | **multisow_clump** | not_needed | 6 (have) | light: align to the pinch-per-cell / transplant-the-clump method it already implies |
| **mint** | frost_anchored | light_required | PARTIAL | bright_default | multi_sow_thin_to_one | optional | 6 (have) | add short "if you do start from seed" clause: surface-sow (needs light), ~6 wk before frost, expect variable/off-type |
| **bee-balm** | frost_anchored | neutral | COVERED | bright_default | multi_sow_thin_to_one | optional | 8 (have) | light: barely-cover depth; the cool-moist-period note already present |
| **echinacea** | frost_anchored | light_required | PARTIAL | bright_default | multi_sow_thin_to_one | optional | 8 (have) | add the missing light instruction (barely cover / surface, light aids germ) to the existing stratify+temp+timing |
| **oregano** | woody_ornamental | light_required | COVERED | bright_default | multi_sow_thin_to_one | optional | **add ~6-8 (src)** | add indoor timing ("start indoors ~N wk before frost"); "needs light, do not cover" already present |
| **sage** | woody_ornamental | neutral | COVERED | bright_default | multi_sow_thin_to_one | optional | **add 8 (src)** | light: barely-cover depth; "indoors 8-10 wk before frost" already present |
| **thyme** | woody_ornamental | neutral | PARTIAL | bright_default | multi_sow_thin_to_one | optional | **add ~8-10 (src)** | add the indoor path: surface / barely-cover the fine seed, timing, slow/uneven (direct-sow sand tip already present) |
| **lavender** | woody_ornamental | light_required | PARTIAL | bright_default | multi_sow_thin_to_one | optional | **add ~10-12 (src)** | add "if you do start from seed" clause: surface-sow (needs light), cold-moist stratify *(src)*, ~70F, expect slow (100-200 d) + off-type; keep the honest steer |
| **rosemary** | woody_ornamental | light_required | PARTIAL | bright_default | multi_sow_thin_to_one | optional | **add ~10-12 (src)** | add "if you do start from seed" clause: surface-sow (needs light), very slow/erratic (~3 yr to size) + off-type; keep the honest steer |
| **pawpaw** | perennial_chill_gated | neutral | GAP | **na (keep)** | **na (keep)** | (absent) | keep None | AUTHOR full stratification method (prose-only); FILL `germination_temp_f` (see §3) |
| **onion** | frost_anchored | **null->neutral** | COVERED | bright_default | multi_sow_thin_to_one | optional | 10 (have) | method ALREADY authored ("Seeds give the biggest bulbs"); verify + light touch only |
| **shallot** | frost_anchored | **null->neutral** | COVERED | bright_default | multi_sow_thin_to_one | optional | 8 (have) | method ALREADY authored ("from seed... single bulbs"); verify + light touch only |

Eleven crops take the field flip; `chives` gives `multisow_clump` a **second live member** (after
spring-onion). Two crops (onion, shallot) also get `germination_light` null->neutral (the #6 re-adjudication
— their `propagule` stays `set`, so the seed-crop-can't-be-null rule does not fire). Five crops gain
`weeks_indoors`. All twelve get prose (COVERED crops a light touch, PARTIAL/GAP crops real authoring).

`pot_up` defaults to `optional` for the small-seed herbs (you CAN pot up if seedlings outgrow the cell, but
cell -> garden is fine); refined per crop from its own prose at authoring. `tray_sowing` is
`multi_sow_thin_to_one` for every small-seed herb (none are large-seed `single_sow`); chives is
`multisow_clump` (the pinch-per-cell clump it already describes).

---

## 3. pawpaw — the honest exception

pawpaw is a deciduous fruit **tree**, not a tray herb, and its from-seed path breaks the template:

- **Recalcitrant seed:** must never dry out; needs ~90-120 days cold-MOIST stratification (damp sphagnum in
  the fridge, or a fall outdoor sowing) before it germinates in warm soil the next season. Full method
  authored in **prose** (both registers), sourced primarily to the Kentucky State University pawpaw program
  (the T1 authority) + one extension `.edu`.
- **Deep brittle taproot:** one seed per TALL deep pot (rootrainer), not a cell tray; resents disturbance.
- **Shade seedling:** the young foliage burns in strong sun (the crop's own prose says so). So
  `bright_default` would MISREPRESENT it. pawpaw keeps `seedling_light = na` and `tray_sowing = na` — its
  from-seed path is a deep-pot stratification project best carried in prose, not the bright-light cell-tray
  structured fields. This is the honest call, not a withholding: `na` is TRUE for pawpaw.
- **`germination_temp_f` is empty `[]`.** Since we now describe warm-soil germination, fill it to the
  sourced warm-soil band *(src, ~[70,85])* so the structured field matches the prose. (This is the one
  register #6 structured touch on pawpaw; confirm with Trevor.)

pawpaw thus gets complete from-seed DIRECTIONS (prose + a real `germination_temp_f`) without the herb
field-flip, because forcing `bright_default` on a shade seedling would be a lie.

---

## 4. Sourcing

- Per-crop **T1**: extension `.edu` seed-starting pages + RHS; each crop's own certified prose where it
  already states the method. Pre-treatments (lavender / echinacea stratification; any soak / scarify) and
  every `weeks_indoors` number sourced individually. Accuracy over cost (the #6 bar).
- **Original prose, not copied.** Same legal model as register #10: facts and methods are not copyrightable
  (17 U.S.C. 102(b) / Feist); the wording is written from scratch. NOT sourced from the Grow It app.
- **Provenance model = contract + STATE_HISTORY**, following the #6/#9 pattern (no per-crop
  `_anchoring_urls`): the sourcing is logged in `docs/seed_start_method_contract.md` (on graduation) and the
  per-batch STATE_HISTORY source-truth sample. `weeks_indoors` and the register enums are NOT
  `timing_spine_gate.NEW_COLUMNS`, so no per-crop `field_additions` entry is gate-required; the amend is
  logged in STATE_HISTORY per the amend-not-recert discipline.

---

## 5. Gate coherence — VERIFIED by scratch spike (2026-07-08)

The design was proven on a scratch copy before any authoring (RED-phase discipline), exercising all three
architectures + the `multisow_clump` path:
- **mint** (frost_anchored division): `seedling_light` na->bright_default, `tray_sowing` na->multi_sow_thin_to_one, `pot_up` +optional
- **lavender** (perennial_woody_ornamental transplant): same flips + `weeks_indoors` +10
- **chives** (frost_anchored division): flips + `tray_sowing` na->**multisow_clump**, `pot_up` not_needed
- **onion + shallot** (frost_anchored set): `germination_light` **null->neutral** + the flip (a second spike)

Result: `seedling_light_gate` PASS, `seed_tray_gate` PASS, `timing_spine_gate` 0 violations,
`register_coverage_gate` PASS, `register_completeness_gate` PASS, `calendar_basis_gate` unchanged (12
pre-existing §E-shell violations on both baseline and spike — none added), `calendar_coherence_gate` 0,
`whole_crop_gate` PASS on all three crops, `gate_all` PASS 114/114 (identical to baseline).

**Why it holds:** `seed_tray_gate`'s only coherence rule is `real tray value <-> seedling_light ==
bright_default` (NO propagule dependency); `seedling_light_gate` has NO propagule rule for `bright_default`;
`timing_spine_gate` does not validate `weeks_indoors` and requires `sow_depth_inches` only for `SEED_LIKE`;
`woody_ornamental_gate` (A13) checks nothing about `weeks_indoors`/seedling fields;
`register_coverage_gate` (A39) requires only that the register KEYS stay present (they do); and the
`germination_light` null->neutral flip is safe because the only null rule fires on `propagule == 'seed'`,
which onion/shallot are not (`set`). No new gate is needed and no existing gate is changed.

---

## 6. Execution

Author in archetype batches (mirrors the register rollouts), **amend-not-recert**, SHA-guarded EXACTLY to
the changed crops, canonical COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline),
count 124. No em-dashes in consumer copy; American English; temps render `°F`.

- **Batch 1 — frost_anchored (have wi):** chives, mint, bee-balm, echinacea. Flips + prose; chives ->
  multisow_clump.
- **Batch 2 — steer-away light_required woody herbs:** lavender, rosemary. Flips + wi add + "if you do
  start from seed" clause (honest steer kept).
- **Batch 3 — covered/partial woody herbs:** oregano, sage, thyme. Flips + wi add + prose touch.
- **Batch 4 — pawpaw (special):** prose method + `germination_temp_f` fill; keep na/na.
- **Batch 5 — bulb-from-seed:** onion, shallot. `germination_light` null->neutral + the flip; method prose
  already authored (verify + light touch only). Drops the germ_light-null count 29 -> 27.

**Gate each batch:** `whole_crop_gate` on changed + `seed_tray_gate` + `seedling_light_gate` +
`timing_spine_gate` + `register_coverage_gate` + `register_completeness_gate` + `gate_all` (regression) +
`release_verify` (source-truth + dash/degrees). No new gate to build.

**State trio each release:** bump `LATEST.txt` (SHA + session); prepend `STATE_HISTORY.md`; SURGICALLY edit
`CURRENT_STATE.md` (do NOT run `gen_current_state.py` — memory `current-state-md-drift`).

**Tracking:** add register **#11** row to `docs/field_addition_register.md`; graduate this spec to
`docs/seed_start_method_contract.md` on completion.

**Trevor confirms every push.** Commit each verified batch; hold the push.

---

## 7. Deferred / open

- **lemongrass** shares the `na`-vs-`weeks_indoors` contradiction but is a genuine no-seed crop (a grass
  grown from division / a rooted grocery stalk — its prose teaches exactly that, no seed path), so
  `germination_light = null` is CORRECT and it stays `na`/`na`. Its `weeks_indoors = 8` is the
  division/stalk indoor-start, not a seed-start. Correctly deferred (no action). (onion + shallot, which
  looked similar, were pulled INTO scope in §2 because their prose already teaches a real from-seed method.)
- **Layer 2 (growth-stage arc)** and **Layer 3 (region calendar)** — follow-on kickoffs if the app needs the
  indoor phase in the stage tracker / per-region schedule.
- **pawpaw `germination_temp_f` fill** — confirm Trevor wants the one structured #6 touch (vs prose-only).
