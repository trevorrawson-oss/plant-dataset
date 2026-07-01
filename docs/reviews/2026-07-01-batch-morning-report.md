# Morning report — overnight authoring batch (2026-06-30 overnight)

**You wake up to 30 new crops, all coherent, staged, and verified. Canonical was never touched.**
Nothing was committed. The 30 are DRAFTS (`author_fresh_pilot`, launch flags false) staged for your
biology-fidelity review + certification — same arc that carried 18 -> 50.

Everything is in `_handoff/batch_2026-06-30/`:
- `crops/<slug>.json` — the 30 individual normalized crop records (compact).
- `BATCH_normalized.json` — the full 125-crop candidate dataset (canonical + the 30 filled + normalized).
- this report.

---

## TL;DR

- **22 overnight crops authored + 8 pilot crops re-normalized = 30 total.** Round **80 with content**
  (50 certified + 30 drafts); 45 honest shells remain.
- **29 of 30 gate-clean** (`whole_crop_gate` by exit code). The 1 holdout is **elderberry** — biology
  complete, but it needs a 3rd `berries_woody` gate sub-form (decision #1 below).
- **A37 calendar-coherence: 0 across all 125 crops** after a central normalizer pass (13 surgical
  changes / 12 cells, every one enumerated + litmus-checked below).
- **0 regressions** — nothing that passed before fails now; the 12 normalized cells are all inside the
  30 new crops.
- **0 template contamination** — the "carrot-on-turnips" bleed scan flagged 11 tokens, all confirmed
  legit sibling comparisons ("ripens earlier than peach," "same species as zucchini").
- **Canonical `crops_data_final.json` untouched** (SHA still `84321950…`, matches LATEST.txt). No commits.

---

## The 30 crops

**12 fruit trees** (`perennial_chill_gated`, off peach/apple):
apricot, cherry-sour, nectarine, plum, pear-asian, fig, persimmon, pomegranate, mulberry, pawpaw
+ (pilot) cherry-sweet, pear-european.

**3 berries** (`berries_woody`, off blueberry):
blackberry (cane) + (pilot) raspberry (cane) + **elderberry (shrub — needs sub-form, see #1)**.

**15 annuals** (`frost_anchored`):
bell-pepper, jalapeno, cayenne-pepper, roma-tomato, grape-tomato, cantaloupe, honeydew-melon,
spaghetti-squash, acorn-squash, yellow-summer-squash + (pilot) celery, potato, spring-onion,
calendula, viola.

Notable refits the agents got right (spot-check candidates for your review):
- **acorn-squash** — flipped 3 things off the butternut template: do-NOT-cure (curing hurts it),
  shortest keeper of the winter squashes (~1-2 mo), and squash-vine-borer SUSCEPTIBLE (butternut shrugs
  it off; acorn is thin-stemmed pepo and does not).
- **honeydew** vs **cantaloupe** — honeydew does NOT slip the vine (learned multi-cue ripeness: rind
  pales to creamy white, waxy/tacky surface, blossom end softens); must be cut. Cantaloupe slips clean.
- **cantaloupe** — most bacterial-wilt-susceptible cucurbit; the whole game is keeping cucumber beetles
  off young plants.
- **elderberry** — cook-before-eating safety threaded through every surface (raw berries/leaves/stems
  mildly toxic); partially self-fertile, "plant 2 different cultivars" is the biggest yield lever.
- **pawpaw** — largest edible fruit native to N. America; custard-apple family; hand-pollination note.

---

## Verification (all by exit code, never grep — the locked guardrail)

| Check | Result |
|---|---|
| `whole_crop_gate` over the 30 | **29 PASS**, 1 FAIL (elderberry, needs sub-form) |
| `whole_crop_gate` over all 125 | 79 PASS / 46 FAIL — the 46 = 45 pre-existing unfilled shells + elderberry |
| A37 calendar-coherence (all 125) | **0 residual violations** |
| Regression diff (canonical vs normalized) | **0 regressions**; 29 shells -> PASS; elderberry expected-fail |
| Template-bleed scan (30 crops, core prose) | **0 contamination** (11 tokens, all legit comparisons) |
| Canonical byte-integrity | untouched, SHA `84321950…` == LATEST.txt |

---

## The central normalizer pass (A37 fix)

Ran `tools/normalize_calendar_coherence.py` over the batch. **13 changes / 12 cells** — and 12 of the 13
are in the 4 pre-fix **pilot** crops + cantaloupe. The other 21 overnight crops were authored AFTER the
calendar fix and came out A37-clean on their own (the post-fix authoring pipeline held). Every change,
litmus-checked (fix only logically-impossible sequences; preserve legit gaps + mild-winter harvest):

| crop | cell | change | verdict |
|---|---|---|---|
| calendula | se_gulf z8 | bridge Feb harvest hole: `Nov-Jan, Mar-Apr` -> `Nov-Apr` | ✓ deep-winter continuous bloom |
| calendula | se_gulf z9 | Sep `growing` -> `season_over` | ✓ summer shoulder before fall replant |
| cantaloupe | fl_peninsula z10 | Jul `growing` -> `season_over` | ✓ FL double-crop summer bridge (= watermelon) |
| cantaloupe | fl_peninsula z11 | Jun `growing` -> `season_over` | ✓ same |
| cantaloupe | fl_peninsula z11 | Jul `growing` -> `season_over` | ✓ same |
| potato | ca_desert z9 | Nov `growing` -> `cold_pause` | ⚠ see flag below |
| potato | ca_desert z10 | Nov `growing` -> `cold_pause` | ⚠ see flag below |
| potato | fl_peninsula z10 | May `growing` -> `season_over` | ✓ summer gap after spring crop |
| potato | fl_peninsula z11 | May `growing` -> `season_over` | ✓ same |
| spring-onion | se_gulf z8 | bridge Jan harvest hole: `Feb-Mar, Oct-Dec` -> `Oct-Mar` | ✓ mild-Gulf continuous |
| spring-onion | se_gulf z9 | bridge Jan harvest hole: `Feb-Apr, Oct-Dec` -> `Oct-Apr` | ✓ mild-Gulf continuous |
| viola | ca_south_coast z9 | Aug `growing` -> `season_over` | ✓ summer heat gap before fall replant |
| viola | ca_south_coast z10 | Aug `growing` -> `season_over` | ✓ same |

No summer holes bridged, no invented harvest, no over-correction.

---

## Decisions for you (in priority order)

**1. Elderberry — build the 3rd `berries_woody` sub-form?** (my recommendation: yes)
Elderberry's biology is complete; it fails the gate on exactly one class (21 violations, all A15): it is
`self_fertile=true` (partially self-fertile) and type `american_elderberry`, and the bush/cane gate knows
neither. It fits NEITHER existing sub-form (bush=blueberry crown / cane=biennial raspberry). Recommended
design — a **SHRUB sub-form**, keyed on a new `cane_type` (e.g. `multistem_perennial`), that (a) accepts
`self_fertile=true` as a partial-self-fertility state with a strong cross-pollination recommendation, and
(b) enumerates `american_elderberry` (+ room for `european_elderberry`). I'll TDD it (RED first — inject
the defect, watch it bounce) and leave it uncommitted for your review. **~30 min once you say go.**

**2. Sign off + commit `tools/berries_woody_gate.py`** (the bush/cane generalization). Still uncommitted
from the raspberry pilot, RED/GREEN-verified. The elderberry sub-form (#1) extends it, so these two land
together.

**3. Biology-fidelity review of the 30 -> certify.** These are drafts. The cert arc is the same family-wave
review that carried 18 -> 50 (WebFetch the cited sources, confirm the numbers, watch for citation-honesty
overclaims — the one recurring catch last time). I can generate the styled per-crop HTML review report
(your preferred format, with a "decisions for you" block) on request — just confirm you still want that
layout before I spend the tokens on 30 crops.

**4. Minor flag — potato `ca_desert` Nov `cold_pause`.** The normalizer replaced an impossible `growing`
with `cold_pause` (inter-crop pause before a Jan planting). Defensible — potato foliage is frost-tender —
but the low desert in November is mild, so `season_over` is arguable. One cell, z9 + z10, your call.

**5. D8 follow-up (not blocking).** The normalizer's `_WARM_CROPS` heat_pause-tagging set is the original
4 (eggplant/watermelon/pumpkin/butternut). The new warm crops (cantaloupe, honeydew, peppers, melons)
aren't in it, so their FL/desert summer gaps normalize to `season_over` without a heat_pause tag — coherent
and honest, but candidates for the same backed-heat_pause authoring refinement later.

---

## Provenance / discipline

- Canonical `crops_data_final.json` **never written** this session (READ-ONLY held). SHA `84321950…`.
- **Nothing committed** (overnight rule). All artifacts in scratch + `_handoff/batch_2026-06-30/`.
- The 8 pilot crops' NORMALIZED records now live in `batch_2026-06-30/crops/` (supersede the pre-fix copies
  in `_handoff/pilot_crops/`).
- State trio (CURRENT_STATE / STATE_HISTORY / LATEST) NOT bumped — no content release happened; that's a
  promote-time action once you certify.

## Suggested next steps
1. You: skim this + decide #1 (elderberry sub-form) and #2 (bush/cane sign-off).
2. Me: build the elderberry sub-form (TDD), re-gate -> 30/30 clean.
3. You + me: biology-fidelity review (family waves) -> promote + certify the batch -> state trio + release
   verification -> **80 certified**.
