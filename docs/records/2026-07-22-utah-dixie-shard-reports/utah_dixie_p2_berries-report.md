# utah_dixie_p2_berries shard report

**Status: DONE**
**Shard:** `tools/staging/shards/utah_dixie_p2_berries.json` (5 cells, single zone "8", compact, no trailing newline)

## Gate summary
| crop | region_harness (whole_crop_gate) | region_cell_audit |
|---|---|---|
| raspberry | GATE: PASS (rc 0) | 0 issues |
| blackberry | GATE: PASS (rc 0) | 0 issues |
| blueberry | GATE: PASS (rc 0) | 0 issues |
| elderberry | GATE: PASS (rc 0) | 0 issues |
| strawberry | GATE: PASS (rc 0) | 0 issues |

`region_cell_audit utah_dixie` = **0 issue(s) across 5 cell(s)**. All calendars DERIVED (berry_woody_calendar / berry_calendar) and re-verified coherent. resolved_from = {last_frost "Mar 30", first_frost "Nov 1"}; resolution_method frost_anchored_resolved; zone_span ["8"]; plantings_provenance null (per guide). No em/en dashes, degF glyph only, no build-word leaks, no Nevada/foreign source ids.

## Per-crop verdicts
- **raspberry — MARGINAL, fall-bearing/low-chill steer (delta 4c).** everbearing / deciduous. bloom "July", harvest "September to October" (the load-bearing move: fruit ripens AFTER peak summer heat, avoiding sunburn, per usu_ext_raspberry — an inversion of Nevada's ripens-before-heat spring harvest). Names USU fall-bearing cultivars (Caroline, Josephine, Polana, Joan J, Polka) + low-chill desert canes (Bababerry, Dorman Red); alkaline-soil iron chlorosis -> chelated iron, afternoon shade, raised beds. Mirrors the warm_arid seasoned note, recast for the hot/low/alkaline St. George core vs the county's higher-elevation raspberry towns. sources: usu_ext_raspberry + usu_ext_wash_frost.
- **blackberry — MARGINAL.** summer_bearing / deciduous. bloom "March", harvest "May to June". Placed in the county's higher-elevation column by the Fruits page; low-chill heat-tolerant erect/semi-erect types, squeezed by late-March frost on early bloom AND summer heat on fruit. sources: usu_ext_wash_fruits + usu_ext_wash_frost.
- **blueberry — VERY marginal, container-only.** southern_highbush / deciduous. bloom "March", harvest "May to June". Alkaline Mojave-edge soil is the binding limit; not growable in open ground, container-only with acidified mix + water, two cultivars, treat as an experiment. sources: usu_ext_wash_frost.
- **elderberry — marginal (moisture/heat/alkaline).** american_elderberry / deciduous. bloom "April to May", harvest "July to August". Moisture-loving shrub, irrigation-dependent in the desert; two cultivars for cross-pollination. sources: usu_ext_wash_frost.
- **strawberry — low-elevation THRIVER (delta 4c).** grown_as perennial (matted row), self_fertile. bloom "April", harvest "May to June", renovate July. Positive verdict: the Fruits page names strawberries in the low-elevation thrive column, so authored as a multi-year June-bearing matted-row bed (cleaner than Nevada's pulled fall-set annual), carried through summer with mulch + afternoon shade. sources: usu_ext_wash_fruits + usu_ext_wash_frost.

## Judgment calls / concerns
1. **raspberry calendar `prune` token lands in June (month before the mid-summer bloom).** This is an artifact of the deciduous-tree/berry_woody deriver (prune := month before bloom) applied to a FALL-bearing cane whose real practice is a dormant-season mow. Driving the harvest to fall (Sep-Oct) — required by the task + the USU quote — forces bloom into summer, which forces prune out of dormancy. The prose (grown_as_note) states the correct practice ("cut back hard in the dormant season / cut to the ground each winter"); the coarse calendar strip cannot express that. Load-bearing message (productive in fall, after the heat) is correct. Flagging for reviewer awareness. (Nevada carried the same class of calendar-vs-prose looseness in the opposite direction.)
2. **recommended_type coverage.** Reused the Nevada/warm_arid types (everbearing raspberry, summer_bearing blackberry, southern_highbush blueberry, american_elderberry) — all already variety-covered on the crop, so the berries_woody coverage invariant passes as it does region-independently.
3. **Thin single-source cells (blueberry, elderberry) cite only usu_ext_wash_frost.** The marginal verdicts rest on universal biology (alkaline soil hostile to blueberry; elderberry's moisture need), stated as honest prose; usu_ext_wash_frost anchors the frost dates + the 100°F Jun-Aug heat reality. This mirrors the Nevada precedent (general-climate + frost source, no crop-specific citation for these two). No T1 St. George blueberry/elderberry page exists.
4. **No `bearing_habit` field invented** (raspberry is not on the berry archetype yet — prose steer only), per instruction.
5. **plantings_provenance = null** on all 5 (per guide + the cherry-tomato worked template); the controller fills it at merge.
