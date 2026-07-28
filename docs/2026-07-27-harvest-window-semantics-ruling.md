# Ruling: what a `harvest` string means, and the duration-coherence pass built on it

**Date:** 2026-07-27
**Canonical at ruling:** `02fbb5e8` (`origin/main` `7870051`).
**Brief:** `docs/2026-07-27-asparagus-harvest-duration-pass-brief.md` (§1 is the question this doc
answers; nothing was edited before it was ruled).
**Judged fresh** per the brief's §7 anchoring warning: the prior session's conclusion that the
windows are sound was treated as a claim to test, not a starting point.

---

## 1. The ruling: READING A, month-granular touch semantics — with a constraint that keeps it honest

A `harvest` string like `"Mar - May"` means **"harvest occurs somewhere within these calendar
months"** (a touch-set), not "from about March 1 to about May 31."

**Why this is the field's actual meaning, not a convenient lenient choice:**

1. **The strings are month-granular by construction.** `harvest` never carries day numbers, while
   `plant_out` on the very same cells is day-granular (`"Mar 20 - Apr 15"`). The asymmetry is
   deliberate: days are used where known, and harvest starts are soil-temperature emergence events
   the literature deliberately does not date (see
   `docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md`).
2. **The renderer is month-granular end to end, and this was verified in the plant-astro code, not
   assumed.** `src/lib/succession.ts` `monthFromString` matches `^([A-Za-z]+)(?:\s+\d+)?` — the day
   number is *optional and discarded*, so even day-granular `plant_out` strings collapse to whole
   months. `harvestWindowMonths` paints every month the window touches onto the 12-cell month grid
   in `PlantingCalendarCard.astro`. The site never promises day precision anywhere; a painted month
   claims only "this activity happens in this month."

**The constraint that comes with reading A.** A painted month is still a promise. The renderer
shows "harvest" on the whole month cell, so a month may appear in the string **only if the cell's
sourced duration can actually reach it**:

> Under the mid-month convention (starts are month-granular or modeled, so the unbiased assumption
> is mid-month), the 15th of the first named month plus the sourced duration's **top end** must
> land on or after the 1st of the last named month. Where a cited source publishes **explicit
> dates** (MU G6405 does), those govern over arithmetic.

Reading A therefore does NOT wave the nine flagged cells through. It legitimizes seven of the
brief's §2a nine and convicts the rest on their own sources — see §3.

**Consequence for the brief's reading B:** rejected. Under B every 6-8-week cell with a three-month
span is over-extended, which would force trimming `mid_atlantic` z8 and `pnw` z8 whose June ends
their own notes and sources state. B punishes the normal shape of an 8-week window that starts
mid-month, and it contradicts how the data is rendered.

---

## 2. What the fresh measurement found (it is more than the brief's table)

The brief's §2a measured only duration arithmetic under reading B. A mechanical re-measure on
`02fbb5e8` with three sub-checks (REACH: duration can reach the last field month; END: a note's
stated harvest end month equals the field's; START: a note's stated emergence month equals the
field's) found **8 findings across 6 cells** — and roster-wide, **zero findings outside
asparagus** (1,120 renderable month-granular harvest cells scanned; only asparagus notes state
week-counts/endpoints in harvest clauses at all: 15 parseable durations, 27 ends, 28 starts, all
asparagus):

| cell | finding | verdict after source read |
|---|---|---|
| `mid_south` z7 | REACH (4-6 wk can't touch Jun) + END (note "into May") | **field wrong** — MU G6405 southern-MO row: Apr 14 - May 30 |
| `mid_atlantic` z7 | REACH (6 wk can't touch Jun) + END (note "into May") | **note wrong** — it silently picked Rutgers' 6 wk while the field picked UMD's June; must carry the range |
| `northern_tier` z7 | END (note "into May", field Jun) | **field wrong** — MU's gradient: warmer zones stop EARLIER; the z7 band is Apr 14 - May 30 |
| `northern_tier` z6 | END (note "into May", field Jun) | **note wrong** — Illinois (cited on the cell): "harvested ... through May or June (as long as 8 to 10 weeks)"; UMN: "Harvest spears until June 30" |
| `northern_tier` z5 | START (note "early to mid May", field paints Apr) | **field wrong** — UMN: "about 6 to 8 weeks, from early May to late June in Minnesota" |
| `utah_dixie` z8 | END (note "through March and April", field May) | **field wrong** — USU: 6 wk yr 4 / up to 8 wk yr 5+; from an early-March St. George emergence even the top end only grazes May 1. Painting all of May for a possible few-day graze is the false promise the constraint exists for. Now matches `low_desert_az` (Mar - Apr), the same Mojave-edge climate |

The prior session's endpoint-comparison method (STATE_HISTORY 02fbb5e8 entry) predicted exactly
this: every flag had to be read, and the read decided **which half is the correct one** per cell —
four field-side repairs, two note-side repairs. Editing the note to match the field would have been
wrong in four of six cases; editing the field to match the note wrong in the other two.

## 3. The repairs (all six, whole-cell moves)

Field-side (harvest string + calendar token move together; notes already correct, untouched):

1. `mid_south` z7: `Apr - Jun` → `Apr - May`; calendar Jun `harvest` → `growing`.
2. `northern_tier` z7: `Apr - Jun` → `Apr - May`; calendar Jun `harvest` → `growing`.
3. `northern_tier` z5: `Apr - Jun` → `May - Jun`; calendar Apr `harvest` → `cold_pause`
   (mirrors z3/z4, whose April is `cold_pause`).
4. `utah_dixie` z8: `Mar - May` → `Mar - Apr`; calendar May `harvest` → `growing`.

Note-side (field + calendar already correct, untouched):

5. `mid_atlantic` z7 **carries the range** per the arc's standing rule (set when
   `harvest_ramp_weeks` year 2 was wrongly collapsed): Rutgers FS1301 says 6 weeks mature, UMD says
   8-10 — disjoint claims, both T1, both on-geography, both cited on the cell. The note now states
   six to ten weeks into June instead of silently picking Rutgers while the field silently picked
   UMD.
6. `northern_tier` z6: note's "into May" → "into June", per Illinois "through May or June (as long
   as 8 to 10 weeks)" and UMN "until June 30" — both cited on the cell. This is a prose repair
   justified by the cell's own sources, not a patch-to-match-field: the note's stated 6-8 weeks is
   NOT range-carried because UMN 6-8 and Illinois 8-10 overlap at 8 (no disjoint disagreement, so
   the Rutgers/UMD rule does not trigger).

Zone ordering after repairs (northern_tier starts: z3 May, z4 May, z5 May, z6 Apr, z7 Apr) stays
monotonic; `mid_south` z7/z8 both start April. `zone_order_gate` confirms 0.

**Sources newly read raw this session** (urllib + tag-strip, per the no-WebFetch-summaries rule):
UMN growing-asparagus, Illinois extension asparagus, UADA FSA-6002 (PDF via pypdf). MSU's
canr.msu.edu page returns an 83-char JS shell with zero asparagus content — noted as unreadable
raw; every verdict above rests on the other cited sources. Rutgers/UMD/USU/MU/UC quotes were
already in hand from the brief and were not re-fetched.

## 4. The eleven §2c cells, examined (not waved through)

Under the ruling, each was checked for END/START agreement plus duration reachability from its
sourced duration (UC's 8-10 wk mature figure carries the nine California cells — four independent
UC corroborations per the brief; crop `harvest_ramp_weeks` year-5 was [8,10] when this was ruled, widened to [6,10] on 2026-07-28 by the duration-reconciliation arc -- that only lowers the floor, so every reachability conclusion below stands unchanged):

- `ca_desert` z9 `Mar - May` ("run into May", 8-10 wk): consistent.
- `ca_desert` z10 `Mar - Apr` ("Spears follow in March and April"): consistent.
- `ca_interior` z9 `Mar - May` ("March into mid May", Delta): consistent.
- `ca_north_coast` z9, z10 `Mar - May` ("March into May"; Marin: eight weeks): mid-Mar + 10 wk =
  May 24 — consistent.
- `ca_south_coast` z9, z10, z11 `Mar - May` ("into mid May"): consistent.
- `low_desert_az` z9, z10 `Mar - Apr` ("March into April"): consistent.
- `mid_south` z8 `Apr - Jun` ("April into early June"): **explicitly sourced this session** — UADA
  FSA-6002: "Starting the fourth year, spears may be harvested from April into June." Resolved
  from unmeasured to sourced-consistent.
- `nevada` z10 `Mar - May` ("into May"): consistent.
- `pnw` z9 `Apr - Jun` ("into mid June", 6-8 wk from a late maritime April start): consistent.
- `se_gulf` z9 `Mar - May` ("into May"): consistent.

## 5. The check that ends the cycle

`tools/harvest_duration_gate.py` — REACH + END + START, roster-wide scope (measured: zero flood
outside the true positives), soft-standalone first in the `zone_order_gate` pattern, TDD with RED
proven against `02fbb5e8` from git and defect-injection on a scratch copy. Driven to 0 by the six
repairs above. Hard-flip trigger: fold into `whole_crop_gate` once the artichoke session's
uncommitted A48 lands (same constraint that kept `zone_order_gate` standalone).

**Scope note for the future:** today this gate is materially an asparagus-idiom check — only
asparagus notes state "N weeks" in harvest clauses. It is deliberately roster-wide anyway: the
moment artichoke (same archetype, same prose conventions) certifies with duration-stating notes,
it is covered with no scope change, and any crop that later adopts the idiom buys the check
automatically.

Queued, unchanged by this pass: `harvest_stop_rule` field proposal (the sweep doc's §3.2),
hardening item 1 (region-prose vs cell-rating gate), citation cleanup arc.
