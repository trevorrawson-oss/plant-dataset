# Seed-tray cell protocol field contract (register #9) -- v1 (design locked)

**Status:** **PILOT AUTHORED + VERIFIED 2026-07-07** (7 crops spliced, all gates green); held for
Trevor's go before the ~48-crop rollout + any push. Design was brainstormed + signed off with Trevor in
two rounds: (1) initial lock -- microgreens = `na`, a separate `pot_up` field, `single_sow` kept distinct;
(2) pilot-driven refinement -- **`pot_up` is a 3-value enum** {`recommended`/`optional`/`not_needed`}
(a bool could not say "optional"), and **`multisow_clump` is RESERVED with 0 live members** (no crop's
authored prose supports seed-tray multisowing; leek/spring-onion are both authored as individual
transplants). See the PILOT section at the bottom. Follows the column-GS-arc method
(`docs/gs_cross_crop_field_addition_v0.md`) and copies the register #6 shape
(`docs/seedling_light_contract.md`): a mostly-standard default value plus a few typed exceptions, driven
deterministically off the already-validated tray-started signal, so the app messages without an LLM and
the field is gate-validatable.

**The gap this closes (Trevor 2026-07-07, verified in the canonical):** the missing middle of the
seed -> transplant journey. Tray-started crops carry `start_method.hardening_off_*` (the harden-off step,
structured) but NO structured "sow a few seeds per cell -> thin to the single strongest -> pot up before
hardening off" guidance. The existing `thinning{}` object is a DIFFERENT concept -- **direct-sown
seedbed/row thinning** to a final in-ground `to_spacing` (present on carrot/beet/lettuce; absent on
tomato/pepper/broccoli). So a tray-starter is told to harden off but never told to over-sow each cell and
cull to one. This is a real, well-bounded new field, NOT covered by `thin_to_inches` (in-ground final
spacing), `thinning{}` (direct-sown row thinning), or `hardening_off_*` (the harden-off step).

**The core insight (settled in the data survey + brainstorm -- do NOT re-derive):**
- **The tray-sowing protocol is a DEFAULT + a few typed exceptions, NOT a per-crop authored column.**
  Almost every crop started from seed in an indoor cell tray follows the same rule: sow 2-3 seeds per
  cell, thin to the strongest. The exceptions are archetype-determined, not per-crop: large seeds
  (cucurbits) are sown 1-2 per cell with little thinning.
- **The "who gets a real tray value" signal already exists and is gate-validated.** Register #6's
  `seedling_light == 'bright_default'` is EXACTLY the set of crops started from seed in an indoor cell
  tray (all 49 are `propagule == 'seed'` AND `weeks_indoors > 0`). So `tray_sowing` keys off it
  deterministically, the same way `seedling_light` keyed off `weeks_indoors` -- no new per-crop guessing
  about who has a tray phase.

**Why now:** register #6 (seedling/germination light) completed 2026-07-07 on a stable 114 roster, and it
produced the exact signal (`seedling_light`) this field reuses. Clean column pass, not a
mid-certification bolt-on. Consumer: the plant-app seed-tray flow ("put 2-3 seeds in each cell, thin to
the strongest, pot up before hardening off"), read gracefully (present-or-omitted).

---

## 1. The fields (crop-level, siblings of `seedling_light` / `germination_temp_f`)

| field | type | meaning | when absent / null |
|---|---|---|---|
| `tray_sowing` | enum | the cell-sowing + thinning protocol for a crop started from seed in an indoor tray; a default plus typed exceptions | **key absent = TODO** (uncertified §E shell, not yet reviewed); every certified crop gets a value (`na` is a real value = no cell-tray phase, not absence) |
| `pot_up` | enum | does the seedling need an intermediate pot-up (plug/small cell -> larger container) before hardening off, and how strongly | **present iff `tray_sowing` is a real tray value** (the tray-started set); **absent** for every `tray_sowing == 'na'` crop (no tray-from-seed phase, nothing to pot up) |

**`tray_sowing` in { `multi_sow_thin_to_one`, `single_sow`, `multisow_clump`, `na` }**
- `multi_sow_thin_to_one` -- the DEFAULT: sow 2-3 seeds per cell, thin to the single strongest seedling.
  The large tray-started middle (Solanaceae, brassicas, celery/parsley/basil, most flowers).
- `single_sow` -- large seeds sown 1(-2) per cell, little/no thinning; over-sowing wastes big expensive
  seed and the seedlings resent disturbance (cucurbits when tray-started; large-seed candidates like
  sunflower / nasturtium / sweet-pea -- sourced per crop at rollout).
- `multisow_clump` -- deliberately sown in a small cluster and transplanted AS a clump, NOT thinned.
  **RESERVED: 0 live members in the current roster** (see the reserved note in section 2). Kept defined
  and gate-tested (proven by a synthetic fixture) so it is ready the moment a crop needs it.
- `na` -- no sow-a-few-per-cell-thin protocol applies. Three sub-cases, one honest value:
  - direct-sown seed crops (roots, direct-sown herbs) -- their thinning is the in-ground `thinning{}`;
  - nursery / vegetative stock (bare-root trees, citrus, division herbs, sets) -- no from-seed tray phase;
  - microgreens -- broadcast-sown as a dense mat, no cells, never thinned or potted up
    (`seedling_light == 'blackout_then_bright'`).

**`pot_up` in { `recommended`, `optional`, `not_needed` }** (present only when `tray_sowing` is a real value)
- `recommended` -- pot up before hardening off; slow large-growers outgrow the plug before it is warm
  enough to plant out, and potting up prevents rootbound stunting (tomato/pepper/eggplant/tomatillo).
- `optional` -- you CAN pot up if seedlings outgrow their cells before transplant time, but cell -> garden
  is the standard path; not required (fast brassicas, many flowers).
- `not_needed` -- transplant straight from the cell; potting up is unnecessary or actively unwanted
  (cucurbits resent root disturbance; thin/grassy seedlings like leek stay small enough to hold in-cell).

**Coverage states (the honesty rule, per GS-arc section 3):**
- `tray_sowing`: `TODO` (key absent, uncertified shell) | `SET-real` (`multi_sow_thin_to_one` /
  `single_sow` / `multisow_clump`) | `na` (a real value). Every certified crop carries it.
- `pot_up`: present (one of the three enum values) on the tray-started set | absent (correct) for `na` crops.

## 2. Semantics locked

- **`na` policy keys off `seedling_light` deterministically (reuse the validated signal).** A crop gets a
  real `tray_sowing` value IFF `seedling_light == 'bright_default'` (started from seed in an indoor cell
  tray); it is `na` IFF `seedling_light in { 'na', 'blackout_then_bright' }` (direct-sown, nursery/
  vegetative, or microgreen broadcast mat). This is the same move register #6 made keying `seedling_light`
  off `weeks_indoors` -- deterministic, gate-checkable, no per-crop invention of who has a tray phase.
  The 7 vegetative-propagule crops that carry a `weeks_indoors > 0` (onion/shallot from sets;
  chives/mint/lemongrass/echinacea/bee-balm from division) are correctly `na`: they have an indoor start
  phase but no seed-in-cell step to over-sow and cull.
- **`pot_up` is a 3-value enum, not a bool (Trevor call, pilot-driven).** Broccoli exposed that a true/
  false `pot_up` cannot express "optional" -- a fast brassica does not NEED an intermediate pot-up but you
  CAN pot up if seedlings outgrow their cells. The three states (`recommended`/`optional`/`not_needed`)
  capture the reality honestly and drive three distinct, factual app messages. `pot_up` stays orthogonal
  to `tray_sowing` (present on every tray-started crop, absent on `na`), and being an enum string it is
  now ruled into `register_completeness_gate` EXCLUDED_KEYS (section 7).
- **`multisow_clump` is RESERVED (0 live members), like register #6's `photoperiod_capped` (Trevor call).**
  The value is real and defined, but NO crop in the current roster is authored as a seed-tray multisow-
  clump crop. Both candidate alliums are authored as INDIVIDUAL transplants: leek is grown to pencil-thick
  and set one-per-6-inch-dibble-hole (its whole blanching method depends on one seedling per hole);
  spring-onion is "transplanted an inch apart" / "thinned to one plant per inch" (its "clump" language is
  the mature bunching HABIT + division of established perennial clumps, not seed-tray multisowing).
  Forcing either into `multisow_clump` would CONTRADICT its own T1-sourced prose. So `multisow_clump` is
  kept defined + gate-tested (a synthetic fixture proves it) and stays empty until a crop genuinely needs
  it. **Follow-on (Trevor, if desired):** author the multisow method into a bunching onion as a separate
  content arc, to give `multisow_clump` a real, cited showcase member (RHS/Almanac/Dowding).
- **`single_sow` stays a distinct value.** Large seeds are a genuinely different protocol (sow 1-2 per
  cell, do not over-sow-and-cull); folding into the default would tell cucurbit growers to over-sow and
  thin big expensive seed, which is wrong horticulture. (Brainstorm decision: keep distinct.)
- **Microgreens (8) are `na`.** The field is the sow-few-per-cell -> thin-to-strongest -> pot-up protocol;
  microgreens have no cells, never thin to one, and never pot up (harvested at cotyledon stage as a dense
  mat). Their dense-sowing method already lives in their `growth_stages` prose and is flagged by
  `seedling_light == 'blackout_then_bright'`, so `na` is honest and the app shows no cell-thinning line.
- **Harden-off stays where it is** (`start_method.hardening_off_*`). This field is the step BEFORE it
  (over-sow the cell -> thin -> pot up); do NOT duplicate the harden-off prose.
- **Amend-not-recert.** Fields are appended to already-certified crops with the source in this contract +
  state-history, not a re-certification (same as timing-spine / watering / climate / #6 fills).
- **Provenance follows the #6 pattern:** logged in this contract's pilot/rollout tables + the STATE_HISTORY
  per-batch source-truth sample; no per-crop `_anchoring_urls` field (the `single_sow` / `pot_up`
  exceptions are the sourced claims; the `multi_sow_thin_to_one` default is documented archetype
  seed-starting behavior).

## 3. Decisions confirmed with Trevor (2026-07-07)

Round 1 (initial contract lock):
1. **Microgreens -> `na`** (most honest for a no-cell-no-thin crop; the density story stays in prose +
   `seedling_light`). NOT a distinct `broadcast_mat` value.
2. **`pot_up` is a separate field** (not folded into the `tray_sowing` enum).
3. **Keep `single_sow` distinct** from the `multi_sow_thin_to_one` default (large-seed protocol differs).
4. **`na` keys off `seedling_light`** (`bright_default` -> real value; `na`/`blackout_then_bright` -> `na`).

Round 2 (pilot-driven refinement):
5. **`pot_up` is a 3-value enum** {`recommended`/`optional`/`not_needed`}, NOT a bool (a bool cannot say
   "optional"; broccoli surfaced this). The factual "note" the user sees IS the per-value app message.
6. **`multisow_clump` is RESERVED (0 live members)** since no crop's authored prose supports seed-tray
   multisowing; **leek = `multi_sow_thin_to_one`** (matches its individual-transplant prose). The multisow
   showcase, if pursued, is a separate content follow-on.

## 4. Expected coverage (of 114 certified; the 10 uncertified §E shells stay TODO)

Deterministic from `seedling_light` (49 `bright_default` / 57 `na` / 8 `blackout_then_bright`):
- **`tray_sowing` real value: 49** (= the `bright_default` set, all `propagule == 'seed'`, all `wi > 0`).
  Within-49 split is the rollout sourcing job (rough shape): `multi_sow_thin_to_one` default (~34:
  Solanaceae, brassicas, celery/parsley/basil, most flowers, leek/spring-onion), `single_sow` (~15: 13
  cucurbits + large-seed flowers per T1), `multisow_clump` 0 (reserved).
- **`tray_sowing` na: 65** (57 `seedling_light == 'na'` + 8 microgreens).
- **`pot_up` present: 49** (the tray-started set); `recommended` (~14 Solanaceae + any slow large-growers)
  / `optional` (fast brassicas + many flowers) / `not_needed` (cucurbits + thin/grassy alliums) -- exact
  split sourced at rollout.

49 + 65 = 114. ✓

## 5. Diverse pilot (7 crops -- exercises every LIVE enum value + both N-A flavors + all 3 `pot_up` values)

| crop | `seedling_light` | `tray_sowing` | `pot_up` | basis |
|---|---|---|---|---|
| cherry-tomato | bright_default | `multi_sow_thin_to_one` | `recommended` | own prose "Ready to pot up or transplant"; Solanaceae, slow seedling, plug -> 3-4 in pot-up |
| broccoli | bright_default | `multi_sow_thin_to_one` | `optional` | own prose "thin or pot up once first true leaves"; fast brassica, cell -> garden standard, pot-up available not required |
| cucumber | bright_default | `single_sow` | `not_needed` | Johnny's "1-2 seeds/cell"; cucurbits resent disturbance, transplant direct from plug |
| leek | bright_default | `multi_sow_thin_to_one` | `not_needed` | own prose: individual pencil-thick transplant into a 6 in dibble hole (thin/grassy seedling holds in-cell, no pot-up) |
| carrot | na (wi=0 direct) | `na` | *(absent)* | direct-sown; its thinning is the in-ground `thinning{}` -- the direct-sown N-A case |
| apple | na (nursery) | `na` | *(absent)* | bare-root nursery stock, no from-seed tray phase -- the nursery N-A case |
| microgreens-mix | blackout_then_bright | `na` | *(absent)* | broadcast mat, no cells / thinning / pot-up -- the microgreen N-A case |

Coverage exercised: `multi_sow_thin_to_one` x3, `single_sow` x1, `na` x3 (direct-sown, nursery, microgreen
-- both `seedling_light` N-A branches); `pot_up` recommended x1 / optional x1 / not_needed x2 / absent x3.
`multisow_clump` is exercised only by the gate's synthetic fixture (no live crop, RESERVED).

## 6. Gate (`tools/seed_tray_gate.py`, TDD RED -> GREEN)

Per-crop shape/coherence checks (fire ONLY when a field is present -- unauthored roster stays green;
ABSENCE is a coverage TODO, never a shape violation). Model: `tools/test_seedling_light_gate.py`.
- `tray_sowing` in the enum; `pot_up` in the enum.
- **`na` <-> `seedling_light` coherence (present-only, both fields present):**
  - a real tray value (`multi_sow_thin_to_one` / `single_sow` / `multisow_clump`) requires
    `seedling_light == 'bright_default'`;
  - `tray_sowing == 'na'` requires `seedling_light in { 'na', 'blackout_then_bright' }`.
- **`pot_up` present iff `tray_sowing` is a real tray value:**
  - `pot_up` present but `tray_sowing` is `na` or absent -> orphan violation;
  - `tray_sowing` is a real value but `pot_up` absent -> missing-companion violation.
- A `--coverage` report: `tray_sowing` SET-real (by value) / `na` / TODO; `pot_up` by value / absent.

Adversarially proven before trusted (inject into a SCRATCH copy of the REAL canonical -- all bounce RED;
the clean canonical is GREEN):
1. bad `tray_sowing` enum;
2. a real tray value with `seedling_light == 'na'` (incoherent);
3. `tray_sowing == 'na'` with `seedling_light == 'bright_default'` (incoherent);
4. bad `pot_up` enum (incl. a bool `True` -- guards against regression to the old shape);
5. `pot_up` present with `tray_sowing == 'na'` (orphan);
6. a real tray value MISSING `pot_up` (missing companion).
Plus: an unauthored crop (neither field) stays GREEN; a `na` crop with `pot_up` absent stays GREEN; the
synthetic `multisow_clump` fixture stays GREEN (reserved value accepted).

## 7. C11 ruling (register_completeness_gate EXCLUDED_KEYS)

Both `tray_sowing` and `pot_up` are controlled-vocab backend enums (siblings of `seedling_light` /
`propagule` / `heat_effect`), so BOTH are ruled into `register_completeness_gate.py` EXCLUDED_KEYS -- a
C11 stop-and-ask, surfaced here for confirmation. (Note: `pot_up` became an enum in round 2; had it stayed
a bool it would have needed no ruling, like `seedling_light_cap_hours`.) Regression-check:
register_completeness still PASS after the ruling.

## 8. Rollout (held for Trevor's go)

Archetype-batched across the tray-started set + the `na` fill, from each crop's own prose + grouped T1
sourcing, via `tools/apply_tray_sowing.py` + a per-batch JSON file in `tools/batches/` (guards: field-
absent, in-memory gate pre-check, count 124, COMPACT no trailing newline, byte-diff EXACTLY the intended
crops). Gate per batch: `seed_tray_gate` + `register_completeness` + `whole_crop_gate` on changed +
`gate_all` + `release_verify` (no new violations). Suggested batches:
- **Tray-started real values:** `multi_sow_thin_to_one` default (Solanaceae + brassicas + celery/parsley/
  basil + flowers + leek/spring-onion) | `single_sow` (cucurbits + large-seed flowers, sourced per crop).
  Author `pot_up` alongside (T1: `recommended` for the Solanaceae; `not_needed` for cucurbits/alliums;
  `optional` for fast brassicas/flowers -- source per crop).
- **`na` fill:** the 57 `seedling_light == 'na'` crops + the 8 microgreens (bulk `na`, no `pot_up`).
Then fold `tray_sowing` into the per-crop GS-arc checklist and the A39 register-coverage gate (section 9).

## 9. Follow-on: fold into the register-coverage A39 gate

Once rolled out, add `tray_sowing` to `tools/register_coverage_gate.py` (wired as `whole_crop_gate`
A39): every certified crop must carry `tray_sowing` (present-or-`na`; `na` is a present value, like a
null `germination_light`). `pot_up` presence is enforced by the standalone gate's present-iff-real-value
coherence (run roster-wide by `tools/gate_all.py`), so A39 requires only the `tray_sowing` key. This is
the payoff of having built A39: a new crop cannot certify without the seed-tray protocol.

## 10. Consumer rendering (present-or-omit, reads gracefully)

The plant-app seed-tray flow reads the enums deterministically:
- `multi_sow_thin_to_one` -> "Sow 2 to 3 seeds per cell and thin to the strongest seedling."
- `single_sow` -> "Sow 1 to 2 of these large seeds per cell; they need little thinning."
- `multisow_clump` -> "Sow a small cluster per cell and transplant the whole clump; no thinning needed." (reserved)
- `na` -> omit the cell-sowing line (direct-sown crops show the in-ground `thinning{}` line instead).
- `pot_up: recommended` -> "Pot up into a larger container before hardening off; these seedlings outgrow their cells."
- `pot_up: optional` -> "You can pot up into a larger container if the seedlings outgrow their cells before transplant time, but it is not required."
- `pot_up: not_needed` / absent -> omit the pot-up line (transplant straight from the cell).

## PILOT (2026-07-07) -- 7 crops spliced, all gates green (canonical `6990f1da` -> `d0c39e80`)

Spliced via `tools/apply_tray_sowing.py` + `tools/batches/tray_sowing_pilot.json` (guards: field-absent,
in-memory gate pre-check, count 124, COMPACT no trailing newline, byte-diff EXACTLY the 7 intended crops).
Values + provenance are the section 5 table. Two authored calls involved judgment, both resolved by the
crops' own certified content:
- **leek = `multi_sow_thin_to_one`** (NOT `multisow_clump`). Its prose is unambiguously the traditional
  individual-transplant method (pencil-thick seedling into a 6 in dibble hole; the blanching method
  depends on one seedling per hole). Setting `multisow_clump` would contradict its own T1-sourced content.
- **broccoli `pot_up = optional`** -- its prose offers "thin or pot up"; the enum's `optional` captures
  that pot-up is available but a fast brassica's standard path is cell -> garden.

**Coverage after pilot (of 124):** `tray_sowing` multi_sow_thin_to_one 3 / single_sow 1 / multisow_clump 0
(reserved) / na 3 / TODO 117; `pot_up` recommended 1 / optional 1 / not_needed 2 / absent 120.

**Gates:** seed_tray_gate PASS (0 violations); register_completeness PASS (C11 ruling holds, now covering
both enums); whole_crop_gate PASS on all 7; gate_all PASS (all 114 certified); release_verify vs HEAD ->
**B. no new violations** (the A. "expected only cherry-tomato" collateral concern is the multi-crop-batch
artifact of release_verify's single-`--slug` default, expected; the calendar review notes are pre-existing
`wait` gaps on cherry-tomato's untouched regions). Byte-isolation: exactly the 7 intended crops differ
from HEAD, none added/removed, all else byte-identical.

The pilot + a 6-batch archetype rollout (see STATE_HISTORY 2026-07-07 #9) carried `tray_sowing` + `pot_up`
to all 114 certified crops (`6990f1da` -> `17ff6b67`, pushed). `multisow_clump` shipped RESERVED (0 live).

## REGISTER #10 (2026-07-07) -- multisow_clump gets its first live member (`17ff6b67` -> `00e0b6b1`)

The RESERVED `multisow_clump` value is now LIVE on **spring-onion**. #9 had left spring-onion (+ leek) as
`multi_sow_thin_to_one` because their authored prose is the individual-transplant method, so flipping the
enum alone would contradict the crop's own content. Scallions are the textbook multisow crop, so the fix
was an ADDITIVE amend: a THIRD `start_method` route authored into both registers (sow a pinch of ~6-10
seeds per cell, grow + transplant the whole clump undivided with no thinning, space clumps 4-6 in, harvest
the biggest first and let the rest size up), then `tray_sowing` -> `multisow_clump` (`pot_up` stays
`not_needed`). Sourced from RHS + Johnny's bunching-onion guide (the multisowing method popularized by
Charles Dowding); cited "(RHS)" inline to match the crop's existing "(UMN)" institutional-cite style.
**Legal (Trevor check):** facts + methods are not copyrightable (17 U.S.C. 102(b) / Feist) -- the prose is
ORIGINAL, not copied wording, and does NOT rely on the Old Farmer's Almanac (dropped from the citation).
Gates: seed_tray_gate PASS (multisow_clump 1 live / 0 reserved), whole_crop_gate spring-onion PASS,
register_completeness / register_coverage / gate_all PASS, release_verify CLEAN (only spring-onion changed).

**NOT pushed** -- #10 committed, held for Trevor's push confirmation.
