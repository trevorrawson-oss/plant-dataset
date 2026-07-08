# Kickoff: Seed-tray cell protocol -- `tray_sowing` + `pot_up` (register #9)

**Created 2026-07-07** (register #6 session, on Trevor's flag). Method:
`docs/gs_cross_crop_field_addition_v0.md` (the column-arc template). Register:
`docs/field_addition_register.md` entry #9. Best template to COPY: register #6
(`docs/seedling_light_contract.md` + `tools/seedling_light_gate.py`) -- #9 is the SAME shape
(mostly-standard default + a few typed exceptions, driven off the tray-started set).

## 0. The gap (Trevor, 2026-07-07 -- verified in the data)

> We don't have any thinning for seed trays. We need to advise people to put a few seeds in each cell,
> and that they'll need to thin before potting up and hardening off.

The **missing middle** of the seed -> transplant journey. Verified against the canonical:
- **Present already:** `start_method.hardening_off_*` (harden-off, structured bool/prose, correct on
  tray-started crops) and a `thinning{}` object -- but the latter is a DIFFERENT concept: **direct-sown
  seedbed/row thinning** to a final in-ground `to_spacing` (present on carrot/lettuce; ABSENT on
  tomato/pepper/broccoli).
- **Missing:** for the ~49 tray-started crops (the `seedling_light == bright_default` / `weeks_indoors
  > 0` set), there is NO structured "sow a few seeds per cell -> thin to the single strongest -> pot up"
  guidance. A tray-starter is told to harden off, but never told to over-sow each cell and cull to one.

So this is a real, well-bounded new field, NOT covered by `thin_to_inches` (in-ground final spacing),
`thinning{}` (direct-sown row thinning), or `hardening_off_*` (the harden-off step).

## 1. Proposed shape (CONFIRM in the brainstorm -- do not lock from this doc)

Mirrors seedling_light: a default value + typed exceptions, so the app messages deterministically.
- `tray_sowing` : enum
  - `multi_sow_thin_to_one` -- the DEFAULT: sow 2-3 seeds per cell, thin to the strongest one.
  - `single_sow` -- large seeds sown 1(-2) per cell (cucurbits when tray-started); little/no thinning.
  - `multisow_clump` -- deliberately sown in clusters and transplanted AS a clump, NOT thinned
    (leeks, scallions, beets, some greens). The honest "don't thin" case.
  - `na` -- direct-sown crops (no tray phase); their thinning is the existing in-ground `thinning{}`.
    Ties to `seedling_light == na` / `weeks_indoors in {0, None}`.
- `pot_up` : bool -- does the crop need an intermediate pot-up before transplant (slow/large:
  tomatoes/peppers/eggplant yes; fast brassicas often cell -> garden, no)? Decide in brainstorm whether
  this is a separate bool, folded into the enum, or gated on a size/DTM signal.

Harden-off stays where it is (`start_method.hardening_off_*`) -- do NOT duplicate it.

## 2. Design questions for the brainstorm (settle BEFORE authoring)
1. Enum values + names above -- right set? Is `single_sow` worth splitting from the default, or is it
   rare enough to fold in? Is `pot_up` a bool, or part of the enum?
2. **N-A policy + coverage states.** `na` for direct-sown (like seedling_light). Is `tray_sowing` SET
   for every tray-started crop, `na` for direct-sown + nursery stock? Does it key off `seedling_light`
   / `weeks_indoors` deterministically (likely yes -- reuse that signal)?
3. **Multisow-clump roster.** Which crops truly are clump-transplanted (leek is `wi=10`; scallions;
   beets/chard sometimes). Source per crop.
4. Consumer rendering: the plant-app seed-tray flow ("2-3 seeds per cell, thin to the strongest, pot up
   before hardening off"). Confirm it reads gracefully (present-or-omit).

## 3. Method (the column GS arc -- same as #6/#7; this IS a canonical content change)
1. **superpowers:brainstorming FIRST** -- lock the field contract with Trevor (enum values, the pot_up
   question, N-A policy, coverage-state defs). Write `docs/seed_tray_protocol_contract.md`.
2. **TDD a gate** `tools/seed_tray_gate.py` (RED before GREEN -- inject bad shapes into a SCRATCH COPY
   of the real canonical, confirm they bounce): enum membership; `pot_up` bool; a `--coverage` report;
   the `na`-iff-direct-sown coherence (reuse `seedling_light`/`weeks_indoors`). Model:
   `tools/test_seedling_light_gate.py`.
3. **C11 ruling:** `tray_sowing` (enum string) -> `register_completeness_gate.py` EXCLUDED_KEYS
   (backend enum, sibling of `seedling_light`); `pot_up` is a bool -> no ruling. Regression PASS.
4. **Diverse pilot (~6 crops incl a legit N-A):** e.g. cherry-tomato (multi_sow_thin_to_one + pot_up),
   broccoli (multi_sow_thin_to_one, no pot_up), cucumber (single_sow), leek (multisow_clump), carrot
   (na, direct-sown), apple (na, nursery). Source the clump/single-sow calls from T1.
5. **Archetype-batched rollout** across the 114 (reusable splicer, guard field absent, count 124,
   COMPACT, SHA-guard exactly the intended crops each batch). Gate per batch (seed_tray_gate +
   register_completeness + whole_crop_gate on changed + release_verify no new violations).
6. **State trio each release** (LATEST.txt SHA+session; prepend STATE_HISTORY.md; SURGICAL
   CURRENT_STATE.md -- do NOT run gen_current_state.py, memory `current-state-md-drift`).
7. **Fold into the register-coverage gate (A39).** Register #8's `tools/register_coverage_gate.py`
   (wired as `whole_crop_gate` A39) now enforces present-or-N/A for #4-#7. Once #9 rolls out, ADD
   `tray_sowing` to A39's required set (present-or-`na`), reusing the standalone gate's N-A predicate --
   so new crops cannot certify without it. (This is the payoff of having built A39.)
8. Trevor confirms every push. Commit each verified batch; hold the push.

## 4. Start here
- Read `docs/field_addition_register.md` #9 + this file.
- Confirm state: `shasum -a 256 crops_data_final.json` == `LATEST.txt`; `git log -1`; `git status -sb`.
  (Note: there may be an unpushed A39 commit `d0f01ef` from the register-coverage session -- reconcile
  before starting; do not double-push.)
- Read register #6 as the template: `docs/seedling_light_contract.md` + `tools/seedling_light_gate.py`.
- Then run `superpowers:brainstorming` to lock the #9 contract with Trevor before authoring anything.
