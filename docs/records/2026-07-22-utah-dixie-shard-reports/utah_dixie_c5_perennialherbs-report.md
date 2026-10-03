# Utah Dixie -- Task C5: herbaceous perennials (bee-balm, chamomile, echinacea, mint)

**Status: DONE.** All 4 crops authored, self-gated clean on the first pass.

Shard: `tools/staging/shards/utah_dixie_c5_perennialherbs.json`

## Gate results (per crop)

| slug | `region_harness.py` | `region_cell_audit.py` |
|---|---|---|
| bee-balm | GATE: PASS | 0 issues |
| chamomile | GATE: PASS | 0 issues |
| echinacea | GATE: PASS | 0 issues |
| mint | GATE: PASS | 0 issues |

Combined `region_cell_audit.py utah_dixie <shard>`: **0 issue(s) across 4 cell(s)**.

No A9 photoperiod exposure on this shard (none of the 4 crops are day-length-gated alliums), so no A9 note applies.

## Shape summary (Nevada donor followed, re-anchored to `resolved_from {"last_frost":"Mar 30","first_frost":"Nov 1"}`, single zone "8")

- **bee-balm**: spring transplant/division (Apr 6 - Apr 30), short bloom (May 15 - May 31), `heat_pause` Jun-Aug, cold_pause the rest. Matches the Nevada donor's shape (moisture-loving perennial, desert heat is the limiting factor, not winter cold).
- **echinacea**: spring transplant/division (Apr 6 - Apr 30), long bloom (Jun 15 - Oct 1) with a "growing" gap in May, **no `heat_pause`** -- matches the Nevada donor's deliberate divergence (drought-tolerant, thrives through the desert summer once established in full sun + sharp drainage).
- **mint**: fall-established (division/cutting, Sep 1 - Oct 8), long cool-season harvest wrapping the winter (Oct 20 - May 20), `heat_pause` Jun-Aug, no cold_pause at all (mirrors the Nevada donor exactly -- St. George's z8 winter stays mild enough that mint keeps cropping right through it once the summer heat wall clears).
- **chamomile**: two cool-season sowing windows (Mar 9 - Apr 30 spring, Aug 5 - Sep 30 fall) with matching bloom windows, `heat_pause` Jun-Jul, cold_pause Nov-Feb. Uses the crop's own `succession_policy.suitable=True` comma-joined-window shape (exempt from A43 Rule B), same convention the certified Nevada/mid_atlantic/mid_south chamomile cells already use; `successions_realized` computed via `tools/derive_realized_successions.py` (returned 6, matches A8).

## Sourcing

Cited only registered utah_dixie USU sub-ids: `usu_ext_veg_dates` (general USU planting-date framework -- none of these 4 crops has a USU Table 1 row, so this backs the general spring-timing anchor, per the task instruction) on all 4; `usu_ext_wash_frost` (St. George's 100°F Jun/Jul/Aug figure) backing every `heat_pause` on bee-balm, mint, chamomile; `usu_ext_fall_veg` (Heflebower fall-gardening guidance) additionally on chamomile's fall window. No Nevada (`unr_*`) or warm_arid (`nmsu_ext`/`uariz_ext`) ids carried over; those cells were read for structure/shape only, as instructed.

## Judgment calls (flag for review)

1. **heat_pause months narrowed vs the Nevada donor for bee-balm and chamomile.** Nevada's donor gave bee-balm a 4-month heat_pause (Jun-Sep) and chamomile 2 months (Jun-Jul), both backed by a general "Southern Nevada seasonal framework" fact sheet's non-month-specific "generally above 90°F" language. Utah's actual registered source (`usu_ext_wash_frost`) instead names three *specific* months at 100°F (Jun, Jul, Aug). I set bee-balm's and mint's `heat_pause.months = [6,7,8]` to match that literal citation exactly (mint's matched the donor's own [6,7,8] anyway; bee-balm's is one month narrower than the donor's [6,7,8,9]). For chamomile I kept the donor's own [6,7] (not extending to include August) specifically because pushing the fall sowing to start in September (as a 3-month pause would force) leaves too little time to bloom before the Nov 1 first frost given the crop's ~68-day sow-to-bloom span; starting the fall cycle in August (as the donor also did) keeps the fall bloom safely inside the frost-free window. This is a defensible but real judgment call -- flagging for a content reviewer to confirm the asymmetry (3-month pause for bee-balm/mint, 2-month for chamomile) reads as intentional rather than inconsistent.
2. **No crop-specific USU source exists for any of these 4 crops.** USU's own vegetable planting-date chart (Table 1) is vegetable-only and does not table herbs or ornamental perennials, exactly as it doesn't for Nevada's UNLV/UNR chart. All 4 cells lean on the general USU planting-date/frost-date framework plus the crop's own established perennial-in-place archetype (already used identically across the Nevada/low_desert_az/warm_arid analogs), same honesty pattern the donor itself uses. Interestingly, a USU page specifically titled "Mint in the Garden" exists and is already cited (generically, as `usu_ext`) on mint's `warm_arid` cell -- but it is not among the utah_dixie region's 8 registered sub-ids, so I did not cite it here (per the shard guide's closed sub-id list); flagging in case a future pass wants to register it as a 9th sub-id for a mint-specific citation.
3. **Dates are self-consistent, not reverse-engineered from the Nevada donor's numeric offsets.** I found the Nevada donor's own `plantings[].offset_days` arithmetic does not actually reconcile with its own `resolved_by_zone` dates in several places (e.g., mint's "from last_frost" transplant arm bears no numeric relationship to its real Sep-Oct fall `plant_out`), confirming `plantings[]` is a descriptive/boilerplate scaffold, not a literally-recomputed source of `resolved_by_zone`. I built each crop's `resolved_by_zone["8"]` directly (mirroring the donor's *shape* and heat_pause decision), then derived `calendar[]` programmatically via `annual_calendar.derive_annual_calendar` (never hand-authored) and verified each by hand before writing.

No em dashes, degF glyph used throughout, no build-word leaks (checked programmatically against consumer-facing prose keys and the full document).
