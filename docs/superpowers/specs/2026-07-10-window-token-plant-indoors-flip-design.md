# Window-vs-token reconciliation: plant-flip (item A) + indoors-flip overlap (item B)

**Date:** 2026-07-10
**Origin:** plant-app feedback handoff `docs/kickoffs/inbox-2026-07-10-from-plant-app-window-token-feedback.md`
(post-#19 token-override-contract sweep). Two dataset-side window/calendar contradictions.

## The two items

### A. 7 se_gulf tomato cells: `second_planting.plant_out` window carries only `heat_pause`

The fall set-out window and the `calendar[]` disagree; no `plant` token sits in the window, so a
token-faithful renderer shows no fall set-out month and the app's fall-term planner has no run to
anchor on.

**Which side is the authored intent?** The WINDOW. In every one of the 7 cells the
`sp.plant_out` span is DTM-coherent with `sp.harvest_start`:

| cell | sp.plant_out | sp.harvest_start | ~DTM from set-out | tomato DTM |
|---|---|---|---|---|
| cherry/roma/grape se_gulf z8 | Jul 6 - Jul 20 | Sep 6 | ~55-62 d | cherry ~60 |
| beefsteak/heirloom se_gulf z8 | Jul 1 - Jul 20 | Sep 29 | ~80 d | beefsteak ~80 |
| beefsteak/heirloom se_gulf z9 | Jul 25 - Aug 8 | Oct 23 | ~80 d | beefsteak ~80 |

The stray `plant` tokens the calendar DOES carry (Aug for z8 cherry/roma/grape; Sep for z9
beefsteak/heirloom) do NOT match those harvest dates -- an Aug/Sep set-out would push harvest a
month later than the sourced `sp.harvest_start`. So the mid-July hot-set set-out is the authored
(UGA-sourced, `uga_ext`) intent; the calendar tokens are stale (a de-mux-era 1-month drift).

**Fix = the `plant`-side analog of kickoff #17's action-over-passive flip.** On the fall set-out
month(s) -- the months `parse_months(sp.plant_out)` covers that currently show `heat_pause` -- the
calendar shows `plant` (the fall set-out action) instead of the passive `heat_pause`. The declared
`heat_pause.months` stays INTACT (July is still a climate-hot month; the SPRING crop still fails
there). This preserves the climate fact exactly as #17 did for `indoors`, and completes the fall
arc the app is building (start indoors -> set out). Stray `plant` tokens outside the window revert
to `growing` (in-season establishment).

Per-cell edits (calendar index, Jan=0):

- cherry/roma/grape se_gulf z8: `Jul(6) heat_pause->plant`, `Aug(7) plant->growing`.
- beefsteak/heirloom se_gulf z8: `Jul(6) heat_pause->plant`. (Jun/Aug stay heat_pause; no stray.)
- beefsteak/heirloom se_gulf z9: `Jul(6) heat_pause->plant`, `Aug(7) heat_pause->plant`,
  `Sep(8) plant->growing`.

Rejected alternative (drop July from `heat_pause.months`): climatically absurd for the
`[6,7,8]` cells -- it would declare July (peak heat) NOT hot while June and August stay hot. And it
destroys sourced climate data. #17's precedent is explicit: keep the climate fact, let the action
token win.

### B. Start-indoors windows with zero `indoors` token -- flip candidates (heat AND cold side)

Same intent as #17 (a real indoor-start window during a pause should show `indoors`), for cells
#17's CORE-month rule never reached. **Root cause of the miss:** every window here is a
mid-month-to-mid-month span (e.g. `Jul 15 - Aug 15`, `Aug 1 - Aug 21`, `Feb 15 - Mar 15`), so it
has NO strict `core_months` in the pause span -- #17's core-only trigger simply never fired. The
app's overlap-based render found them.

**Scope = exactly the handoff's enumerated cells** (curated, vetted). A blind uniform overlap
sweep across all frost_anchored cells produces 134 flips and drags in boundary-tail artifacts and
no-seed crops (lemongrass across 11 regions) -- rejected. The same-rule candidates NOT in the
handoff (June boundary months, se_gulf z9 tomato Jul, low_desert_az, ca_south_coast broccoli, etc.)
are FLAGGED for a separate ruling, not flipped here.

Heat-side (`heat_pause -> indoors`): ca_desert cherry/beefsteak/roma/heirloom/grape z9+z10 (Jul+Aug);
broccoli+kohlrabi se_gulf z8 (Jul+Aug) & z9 (Aug), warm_arid z8 (Jul), northern_tier z6 (Jul) & z7
(Aug); fl_peninsula cherry/roma/grape z10+z11 (Aug); jalapeno fl_peninsula z10 (Aug) & z11 (Jul+Aug).

Cold-side (`cold_pause -> indoors`, the #17 mirror): broccoli+kohlrabi northern_tier z3 (Mar), z4
(Mar), z5 (Feb), z6 (Feb), z7 (Jan); cucurbit block slicing/pickling/english-cucumber +
zucchini-courgette + yellow-summer-squash, ca_interior z9 (Feb) & ca_south_coast z10 (Feb).

44 distinct cells (broccoli/kohlrabi nt z6/z7 get both a heat and a cold flip).

## Gate changes (minimum to let the intended flips certify; no forced sweep)

Only two functions in `tools/annual_calendar.py` change; the deriver (`derive_annual_calendar`) is
NOT in the gate path and is left untouched.

1. **A5 `annual_coherence_violations`** -- extend the "flipped" set from `{indoors}` to
   `{indoors, plant}`: a declared heat month may legitimately show EITHER action token. Coherence
   still requires every hot month to show `heat_pause` OR a recognized action; a hot month shown as
   a non-action token (`growing`/`harvest`/`wait`) is still a violation. (Item A needs this; item B
   indoors flips already pass today.)

2. **A5b `heat_flip_backing_violations`** -- the action-must-be-real guard, kept SCOPED to declared
   heat months (a general "every indoors backed" rule over-fires on 39 legit extended nursery runs):
   - `indoors` backing relaxed CORE -> OVERLAP (`parse_months(start_indoors) | parse_months(sp.start_indoors)`).
     Overlap superset of core, so all 26 existing #17 indoors-on-heat tokens stay backed; item B's
     partial-window heat flips now back. (Item B heat side needs this.)
   - NEW: a `plant` on a declared heat month must be OVERLAPPED by
     `parse_months(plant_out) | parse_months(sp.plant_out)`. (Item A backing.)

**Cold side needs no gate change** -- `cold_pause -> indoors` passes A24 (no indoors-placement
check) and A5 (heat-only). There is no cold-side declared-months object to key a backing gate off,
and a general indoors-backing rule over-fires. A cold-side action-backing gate is a FLAGGED
follow-up, not this task.

Test division of labor (updates `test_annual_calendar.py`): the old `_a5_bad` asserted
`plant`-on-hot is an A5 violation. Under the new model an UNBACKED plant-on-hot is an **A5b**
violation; A5's negative case switches to `growing`-on-hot. Coverage is preserved, not lost.

## Verification

RED before GREEN on both gate functions; adversarial injection on a scratch canonical copy. Full
suite: `gate_all` (whole suite on every certified crop), `whole_crop_gate` incl A43,
`calendar_coherence`, `release_verify`, per-batch source-truth sample. SHA-guarded COMPACT splices,
footprint = ONLY the intended `calendar[]` arrays.
