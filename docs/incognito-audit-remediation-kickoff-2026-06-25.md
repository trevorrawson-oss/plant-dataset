# Gate-Hardening Remediation, Kickoff for a FULL-CONTEXT chat

**Date:** 2026-06-25
**Run this in a memory-ON, full-context session** (the deliberate opposite of the incognito audit).
**Inputs:** `docs/incognito-audit-2026-06-25.md` (the findings + the two tier-1 fixes already
applied) and this file.

---

## Why this is full-context, not incognito

The audit was run blind on purpose -- fresh eyes find what primed eyes confirm. Remediation is the
opposite: fixing these gates well requires the accumulated history this repo carries, because the
single biggest landmine is re-proposing something that was already tried and rejected.

**Concrete trap to avoid:** do NOT add a naive "harvest must follow plant_out within
days_to_maturity" calendar gate. The prior gs-arc audit explicitly REJECTED it because it
false-positives onion (photoperiod/overwintering), every overwintered crop, and continuous-
succession crops (one merged sow run feeding a split harvest). A fresh chat would happily build
exactly that and ship an over-flagging gate. This is why remediation is memory-on.

## State going in

- Dataset SHA `6c72f8b9` (content `b39f1453`). 18 certified + 105 shells. Foundation is sound;
  dates verified 0 wrong-season across 64 cells.
- Already CLOSED this session (test-first, not yet committed): **B2** deciduous-tree variety-chill
  type lock (`perennial_gate.py` + wired A22 in `whole_crop_gate.py`); the **website render gap**
  (`plant-astro/src/lib/built-crops.ts` derives guide paths from the certified set). See audit §7.
- The mission this armor must survive: scaling 18 -> ~105 crops via a bot pipeline (claude.ai
  authors, Claude Code releases). Every gate hole propagates x105.

## Work items, in priority order

### 1. B1 (the long pole) -- gate annual calendar token placement
The real drift defense `annual_calendar_violations()` exists in `tools/annual_calendar.py:172` but
has **zero callers**; the orchestrator runs only the weaker `annual_coherence_violations` (length +
token enum + heat_pause-month alignment). So a `cold_pause` on a plant month, a `heat_pause` on a
harvest month, an unbacked `heat_pause`, or a calendar contradicting its own `plant_out` all pass.
10/18 current crops are annuals; most of the 105 will be.

The work is NOT just wiring it in (that's one line). It is **reconciling the re-deriver with the
legitimate hand-authored annual shapes it cannot currently reproduce** so it catches real drift
without crying wolf:
- onion's `season_over` token; summer `heat_pause` cells with no `heat_pause_months`; multi-cycle
  and heat-inverted desert/Gulf cells the deriver's own docstring flags as out of scope.
- Use the audit's deriver-vs-stored diff as the test corpus: basil/zinnia reproduce exactly;
  zucchini/broccoli/onion/tomatoes/lettuce/carrot/green-beans drift for legitimate reasons. The
  gate must pass all 10 certified annuals AND fail the injected defects (pause-on-plant,
  pause-on-harvest, unbacked heat_pause).
- TDD: extend `tools/test_annual_calendar.py` first; wire into `whole_crop_gate` only once green.
- Mirror the B2 pattern (audit §7 / `perennial_gate.py` A22) for how to add + wire a sub-gate.

### 2. B3 -- require thermal backing for `heat_pause`
A fabricated summer pause (token + self-consistent `heat_pause.months`, zero climate justification)
ships clean. Decide the backing datum (a region/zone heat field) and gate that a `heat_pause` is
backed. Test-first.

### 3. B4 -- link photoperiod `day_length_type` to window shape
`photoperiod_gate.py` checks enum + type coverage only; a short-day variety with a long-day-shaped
schedule is invisible. Add the window-fit rule. (Onion is the only photoperiod crop today; get it
right before more arrive.)

### 4. B5 + register wiring
- Companion seasoned-reachability is crop-level only; a single good in a beginner-only bucket among
  seasoned-readable goods is invisible. Extend `companion_shape_gate.py` to per-entry.
- Wire `register_fill_gate` + `register_completeness_gate` into the always-on `whole_crop_gate`
  (today they run standalone at flip), AND fix the `register_fill` over-flag on structured-N/A
  fields (`{"applicable": false, ...}`) so it stops flagging carrot/tomato overwintering N/As.
  Get the 6/18 that currently fail register_fill to green (real nulls vs the over-flag).

### 5. Process armor (carry forward, don't skip)
- **Adversarially stress-test every new gate** before trusting it: in a scratch copy, inject a
  defect of the class it claims to catch and confirm it FAILS -- the method that found B1/B2.
  A gate is not "done" until a defect has been sneaked at it and bounced.
- Keep the **per-batch source-truth sample** (the un-gateable dates layer; 0 wrong-season held).
- Fold the ~14 MINOR date nits (audit §3: S-FL bulb onion, se_gulf beefsteak Sep token, z3
  bean/carrot edges, low-desert fall succession) into the NEXT authoring batch's combined push --
  not a fragmented one-off.

## Discipline
- TDD throughout (the dataset convention is tests-first; RED before GREEN).
- READ-ONLY on `crops_data_final.json` until there is an authoring task; this is gate/tooling work.
- Do NOT commit until Trevor approves (per CLAUDE.md). The two tier-1 fixes from this session are
  also uncommitted and should be reviewed/committed alongside or before this work.
- American English, no em dashes in consumer copy (docs/code may use `--`).

## Key files
- `tools/annual_calendar.py:172` (`annual_calendar_violations`, the unwired gate) + its caller-less
  state; `tools/whole_crop_gate.py` (orchestrator; `annual_coherence_violations` import is what runs
  today; A22 shows the add-and-wire pattern); `tools/test_annual_calendar.py`.
- `tools/perennial_gate.py` (B2 pattern to mirror), `tools/companion_shape_gate.py`,
  `tools/photoperiod_gate.py`, `tools/register_fill_gate.py`, `tools/register_completeness_gate.py`.
- plant-astro: `src/lib/built-crops.ts` (+ test) and `src/pages/guides/crops/[crop]/[zone].astro`
  (the render fix, for reference).
