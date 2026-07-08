# Heat-gap `indoors` flip -- design

**Date:** 2026-07-08
**Status:** design approved (Trevor), pending spec review -> implementation plan
**Lane:** plant-dataset (calendar data + deriver + gates) with a plant-astro rendering handoff

---

## 1. Problem / origin

Trevor, on broccoli in `ca_interior` (interior valley) zone 9: *"why is it indoors in Nov but not July?"*

The cell has a summer `heat_pause` (`months = [5,6,7]`; broccoli can't form a head above ~86°F) sitting between a spring crop and a fall crop. The fall crop's indoor-start window (`second_planting.start_indoors = "Jun 20 - Aug 18"`) covers July, but the 12-month `calendar[]` shows July as `heat_pause` -- the passive "wait, too hot" state -- and never surfaces the actionable "time to start your fall seedlings indoors."

**The insight (Trevor):** keep one token per cell, but let the **actionable** token win over the **passive** one *where a real action exists*. A `heat_pause` is "do nothing"; an indoor-start is "do this now." Once the pause is understood, the useful thing to show is the action. So: during a heat pause, flip a month to `indoors` **iff** a genuine indoor-start window overlaps it. No indoor-start there -> the pause stays `heat_pause`. We never show "indoors" for a crop you don't start indoors.

This is a general **action-over-passive** principle; this spec implements the one case that matters now: `heat_pause -> indoors`.

## 2. Decisions (resolved in brainstorming)

1. **One token per cell**, not a top/bottom split. (The split was the opening idea; the token flip achieves the goal more simply and keeps the existing model.)
2. **Event-driven, not a fixed "after N months" rule.** The flip is triggered by the *real* indoor-start dates, so it self-adjusts (a 4-month pause with a late indoor start just shows `heat_pause` longer). Trevor: a fixed rule "could be wrong if some areas have 4 months of heat pause and then indoors."
3. **Core-month trigger.** A `heat_pause` month flips only if it is a **core month** (fully covered, via the existing `core_months()` month-rounding) of an indoor-start window. This reproduces "establish the pause, then flip" for free: for broccoli z9, `core_months("Jun 20 - Aug 18") = {July}`, so May/June stay `heat_pause` and July flips -- exactly Trevor's picture.
4. **Both indoor sources.** The flip reads indoor-start months from BOTH top-level `start_indoors` (e.g. Florida tomatoes, celery) AND `second_planting.start_indoors` (broccoli, kohlrabi). Uniform rule.
5. **Action must be real** (Trevor's guard): the flip fires only where `heat_pause.months` intersects the core months of a real indoor-start window. Enforced by a gate.
6. **Flip lives in canonical** (patch the stored `calendar[]`), not re-derived at render time. Dataset stays the source of truth; the app renders the stored token.
7. **Note is hybrid, app-derived.** Composed at build time from existing canonical fields (`heat_effect` + `heat_threshold_f` + the fall/`second_planting` timing), with an optional per-cell override slot for cells that read too generic. No derived prose stored in canonical.

## 3. Scope

**22 cells flip** (measured against the current canonical), across 5 crops:

| crop | cells | example |
|---|---|---|
| celery | 10 | `se_gulf` z8/z9: pause Jun-Aug, `start_indoors "Jul, Nov"` -> flip **Jul** |
| broccoli | 4 | `ca_interior` z8/z9 -> flip **Jul**; `ca_south_coast` z9/z10 -> flip **Aug** |
| kohlrabi | 4 | `ca_interior` z8/z9 -> flip **Jul**; `ca_south_coast` -> flip **Aug** |
| beefsteak-tomato | 2 | `fl_peninsula` z10/z11: pause Jun-Sep, indoor Jul 21-Jan 1 -> flip **Aug + Sep** |
| heirloom-tomato | 2 | `fl_peninsula` z10/z11 -> flip **Aug + Sep** |

All 5 crops carry `heat_threshold_f` (broccoli 86, kohlrabi/celery 75, tomatoes 92) and `heat_effect`, so the note template has its inputs.

This is **decoupled from** the `second_planting` de-multiplexing finding (`docs/2026-07-08-second-planting-demux-findings.md`): the flip only needs the indoor-start dates, which are already correct regardless of de-mux state.

## 4. Component A -- the flip rule (`derive_annual_calendar` + surgical patch)

**Rule.** In `tools/annual_calendar.py::derive_annual_calendar`, compute:
```
indoor_core = core_months(cell.start_indoors) | core_months(cell.second_planting.start_indoors)
heat        = set(heat_pause_months)
heat_flip   = heat & indoor_core          # hot months that are core indoor-start months
```
Precedence, per month `m` (highest first):
```
m in heat_flip -> "indoors"     # NEW: action overrides passive heat
m in heat      -> "heat_pause"
m in P         -> "plant"
m in H         -> "harvest"
m in I         -> "indoors"     # normal (e.g. spring) indoor-start
m in cold      -> "cold_pause"
else           -> "growing" | "wait"
```
(`heat_flip` months are never `plant_out` months -- the existing A24 gate forbids a pause on a plant month -- so there is no plant/flip conflict.)

**The deriver reproduces only simple cells; the 22 target cells are hand-authored.** So the rule is applied to existing cells by a **surgical, deterministic transform**: for each of the 22 cells, in the stored `calendar[]`, change the computed `heat_flip` months from `heat_pause` to `indoors`; touch nothing else. SHA-guarded via `tools/apply_patch.py`, footprint = exactly those cells' `calendar` arrays.

**No new token.** `indoors` is already in `ANNUAL_CALENDAR_TOKENS`.

## 5. Component B -- the note (hybrid, app-derived)

**Trigger (app, no new field needed).** A calendar `indoors` token at month `m` where `m in cell.heat_pause.months` **is** a heat-gap flip -> show the note. (A normal spring `indoors` cell -- `m` not in `heat_pause.months` -- gets no note.) The app derives this from data it already has.

**Derived template** (composed at plant-astro `build:guides`), keyed off structured fields:
- reason phrase from `heat_effect`: `crown_failure -> "form heads"`, `poor_fruit_set -> "set fruit"`, `quality_loss -> "grow well"`, `bolting -> "grow without bolting"`.
- transplant temp from `heat_threshold_f`.
- fall framing from `second_planting` (or the next harvest window).

Example (broccoli): *"Too hot for broccoli to form heads outdoors now -- start seeds indoors for a fall crop, and set them out once daytime highs cool to about 86°F."* Dual-register (`_beginner` warmer, `_seasoned` terser). The transplant temp and heat reason are **sourced by construction** (they are `heat_threshold_f` / `heat_effect`, already cited).

**Override slot (reserved, not populated now):** an optional per-cell `heat_gap_note_beginner` / `heat_gap_note_seasoned`. When present, the app uses it instead of the derived text. Added only if/when a cell reads too generic (Trevor: "if they sound too generic we can come back for b").

**Graceful fallback:** if `heat_threshold_f` is absent on some future flip crop, the note omits the temp clause. (All 5 current crops carry it.)

## 6. Component C -- gates (TDD, RED before GREEN)

**C1. A5 coherence update** (`annual_coherence_violations`, whole_crop_gate A5). Today it asserts `calendar heat_pause months == heat_pause.months` exactly. That identity now legitimately breaks (a hot month can display `indoors`). New assertion, preserving the climate fact:
```
hp        = set(cell.heat_pause.months)
cal_hp    = {m : calendar[m] == "heat_pause"}
flipped   = hp & {m : calendar[m] == "indoors"}
REQUIRE: cal_hp == hp - flipped        # every hot month shows heat_pause OR (flipped) indoors;
                                        # no heat_pause token sits outside hp
```

**C2. Flip-backing invariant** (new check; Trevor's "action must be real" guard). For each flipped month `m` (`m in hp & indoors`), require `m in core_months(start_indoors) | core_months(second_planting.start_indoors)`. An `indoors` on a hot month with no overlapping indoor-start window is a violation ("indoors shown with no indoor-start action to back it").

**TDD:** inject into a scratch copy of the real canonical -- (a) a hot month shown as `plant` (C1 must bounce); (b) a valid flip (C1/C2 must pass); (c) a flipped `indoors` on a hot month with no backing window (C2 must bounce) -- confirm each before trusting the gate. Then re-run `calendar_coherence_gate`, A24 placement, `gate_all`, `release_verify`.

## 7. Component D -- plant-astro handoff (kickoff, not built here)

1. Render the `indoors` calendar token (already supported by `SuccessionCard`/calendar).
2. For an `indoors` cell whose month is in the cell's `heat_pause.months`, compose + show the derived note (Component B template).
3. Support the optional `heat_gap_note_*` override when present.
4. Re-run `npm run build:guides` + `npx jest`.

## 8. Canonical footprint of THIS work

- **Only** the flipped `calendar[]` tokens on the 22 cells (`heat_pause -> indoors` on the computed months). Nothing else in canonical changes.
- No new required field. The override slot is documented but not populated.
- Deriver (`annual_calendar.py`) + gate updated in `tools/` (not canonical).

## 9. Out of scope

- The `second_planting` de-multiplexing correction (separate finding; orthogonal).
- The top/bottom split rendering (superseded by the token flip).
- A fully general passive/action override matrix (`cold_pause -> plant`, etc.) -- YAGNI; only `heat_pause -> indoors` now, extensible later.
- Populating any per-cell note overrides.

## 10. Risks / edge cases

- **App lag is low-risk here** (unlike de-mux): a flipped `indoors` in July is *truthful on its own* (you do start indoors then). The note only adds the "why." So the data flip can ship before the plant-astro note without misinforming.
- **Whole-pause overlap:** if an indoor window's core months cover the entire `heat_pause`, all hot months flip and the calendar shows zero `heat_pause` tokens. C1 still passes (`cal_hp == hp - flipped == {}`); the climate fact stays in `heat_pause.months` and the note still says "too hot." Accepted.
- **heat_effect wording coverage:** the template must map every `heat_effect` value that occurs on a flip crop (currently `crown_failure`, `quality_loss`, `poor_fruit_set`); assert coverage in the app, fall back to a generic "grow well" phrase otherwise.

## 11. Testing plan

- Deriver unit tests: correct flip months for broccoli z9 (Jul), broccoli `ca_south_coast` (Aug), fl_peninsula tomato (Aug+Sep), celery `se_gulf` (Jul); NO flip where no indoor window overlaps a hot month.
- Gate tests: C1 + C2 RED cases bounce on scratch copies; GREEN on the patched canonical.
- Patch: SHA-guarded, footprint = exactly the 22 cells' `calendar` arrays, only `heat_pause->indoors` on the computed months, count 124, COMPACT.
- Suite: `gate_all` 114/114, `calendar_coherence_gate`, `release_verify` clean.

## 12. Open items for the plan

- Exact home for C1/C2 (extend `annual_coherence_violations` vs a sibling function).
- Note template's precise beginner/seasoned wording per `heat_effect`.
- Whether the deriver change and the 22-cell patch land in one commit or two (rule + data).
