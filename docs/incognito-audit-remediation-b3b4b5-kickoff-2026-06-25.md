# Gate-Hardening Remediation, Part 2 (B3 / B4 / B5 + register wiring), Kickoff

**Date:** 2026-06-25
**Run this in a memory-ON, full-context session** (same as B1; the history matters).
**Inputs:** `docs/incognito-audit-2026-06-25.md` (findings), `docs/incognito-audit-remediation-kickoff-2026-06-25.md`
(the original remediation kickoff -- B3/B4/B5 detail lives there too), and this file.

This is the continuation of the remediation arc. **B1 is DONE** (the long pole); what
remains is the secondary hardening before scaling 18 -> ~105.

---

## State going in

- **B1 CLOSED** (commit `5f77f60`, NOT pushed -- Trevor pushes manually). A24 annual
  calendar token-PLACEMENT gate wired in `whole_crop_gate.py`; reconciled
  `annual_calendar_violations` in `annual_calendar.py`; tests in `test_annual_calendar.py`.
  18/18 still `GATE: PASS`; all four audit defects bounce. `crops_data_final.json` untouched.
- **B2 + render gap** already committed earlier (dataset `0b9afd6` A22 tree variety-chill;
  plant-astro `28a4052` certified-derived guide paths).
- Dataset content SHA `b39f1453` (repo `6c72f8b9`) -- unchanged; B1 was tooling-only.
- Mission unchanged: the armor must survive scaling 18 -> ~105 via the bot pipeline.

## The B1 pattern to reuse (do NOT relitigate)

1. **These gates are token-PLACEMENT / structural-shape checks, NOT full re-derivations.**
   Hand-authored cells legitimately drift (month-rounding, multi-cycle, etc.), so a strict
   recompute cries wolf. B1 proved this empirically (the deriver reproduces only 2/10 annuals).
2. **Design empirically, FP-first.** Before writing any gate code, write a scratch script
   that runs the candidate rule against EVERY certified crop of the relevant archetype and
   confirm **zero false positives**. Only then write the gate.
3. **Adversarial last step.** Inject the defect class into a scratch copy and confirm the gate
   FAILS it. A gate is not done until a defect bounces. (Canonical stays READ-ONLY throughout.)
4. **Add-and-wire like A22/A24:** a `*_violations(crop)` fn (own module or extend the existing
   gate), TDD in the matching test file (RED before GREEN), wire as the next A-number in
   `whole_crop_gate.py`.

## Work items, in priority order

### 1. B3 -- thermal backing for `heat_pause`
The gap: a self-consistent `heat_pause` (token + matching `heat_pause.months`) with zero
climate justification ships clean. **B1 deliberately did NOT require backing** -- A24 only
checks placement, because zucchini/green-beans ship legitimate OBJECT-LESS summer
`heat_pause` tokens today (no `heat_pause` object at all), while cherry/beefsteak/onion
desert cells carry a full `heat_pause` object (`months` + `basis_seasoned` + T1 `sources`).
So "backing" is currently UNEVEN across the certified set.

**This is not pure tooling.** Decide the backing DATUM *with Trevor* (a product/data call):
- (a) Require every `heat_pause`-token cell to carry a `heat_pause` object (months + basis
  prose + >=1 T1 source). This would currently FAIL the object-less zucchini/green-beans
  cells -- i.e. it implies an AUTHORING batch to back-fill them first, not a read-only-passable
  gate. (Mirror the chill prose-backstop pattern.)
- (b) A shared region/zone summer-heat table (like `region_chill_delivered`) that a
  `heat_pause` must reference.

**Surface the "pass all 10 vs require backing" tension to Trevor before building.** Then
TDD + wire + adversarial. The shared reader `annual_calendar.declared_heat_months()` already
normalizes nested-object vs flat `heat_pause_months`.

### 2. B4 -- photoperiod `day_length_type` -> window shape
`photoperiod_gate.py` (A9) checks enum + type coverage only; a short-day variety with a
long-day-shaped schedule is invisible. Add the window-fit rule. Onion is the only photoperiod
crop today -- use its real cells as the 0-FP corpus and get it right before more alliums arrive.

### 3. B5 + register wiring
- Extend `companion_shape_gate.py` (A19, crop-level reachability) to PER-ENTRY: a single good
  in a beginner-only bucket among seasoned-readable goods is invisible to seasoned readers.
- Wire `register_fill_gate` + `register_completeness_gate` into the always-on
  `whole_crop_gate` (today they run standalone at flip), AND fix the `register_fill` over-flag
  on structured-N/A fields (`{"applicable": false, ...}`) so it stops flagging carrot/tomato
  overwintering N/As. Get the 6/18 that currently fail `register_fill` to green (real nulls vs
  the over-flag).

## Carry forward / process armor
- Adversarially stress-test every new gate (scratch inject -> confirm bounce).
- Keep the per-batch source-truth sample (the un-gateable dates layer).
- **Fold these CONFIRMED certified-crop harvest-display nits into the NEXT authoring batch**
  (found during B1; not gate-blockable without false-positiving them):
  - `broccoli` northern_tier z5/z6/z7: a single continuous `harvest` display papers over the
    summer bolting gap; that gap is also labeled `cold_pause` when it is heat-driven.
  - `beefsteak-tomato` ca_south_coast.z9: the Dec frost cutoff is rounded into "Jul - Dec".
  - Plus the audit's ~14 MINOR date nits (S-FL bulb onion, se_gulf beefsteak Sep token, z3
    bean/carrot edges, low-desert fall succession). Combine, do not fragment.

## Discipline
- TDD throughout (RED before GREEN). READ-ONLY on `crops_data_final.json` until an authoring
  task is explicitly agreed (B3 may need one). Adversarially test each gate. Do NOT commit until
  Trevor approves. American English, no em dashes in consumer copy (docs/code may use `--`).
- At the commit that lands real dataset content, update `CURRENT_STATE.md` / `STATE_HISTORY.md`.

## Key files
- B3: `heat_pause` objects in `resolved_by_zone` cells (`months` / `basis_seasoned` / `sources`)
  + flat `heat_pause_months`; shared reader `annual_calendar.declared_heat_months()`. Shared-table
  precedent: `region_chill_delivered` + `tools/chill_gate.py`.
- B4: `tools/photoperiod_gate.py` (A9) + onion cells.
- B5: `tools/companion_shape_gate.py` (A19); `tools/register_fill_gate.py` +
  `tools/register_completeness_gate.py`; wire in `tools/whole_crop_gate.py` (mirror A22/A24).
