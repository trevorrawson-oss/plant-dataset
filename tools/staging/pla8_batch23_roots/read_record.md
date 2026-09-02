# Batch 23 (roots) -- THE READ. What was CHECKED, not only what was fixed.

The playbook's step 4 insists on recording the denominator: "without it 'cleanup rode the arcs'
reads as coverage it never had." Canonical `b118f19d`, 22 problems, **87 rungs / 174 register
strings**, authored by three parallel agents against a 64-method catalog.

## Mechanical, run by the orchestrator INDEPENDENTLY of each agent's own checker

| check | result |
|---|---|
| `gate_all.py` (whole suite, every certified crop) | **PASS** |
| `control_ladder_gate` / both variety gates / `register_completeness` | 0 / 0 / 0 / PASS |
| catalog-key validity, tier monotonicity, applies_to legality (re-derived from canonical) | **CLEAN, all 87** |
| pin conformance: id, type, array order, source-name alignment | **22/22, ZERO DRIFT** |
| copy hygiene: em/en dash, double hyphen, absolutes, spaced degF, British spelling | 0 across 174 strings |
| `check_no_precedent_copy` (the chosen guard) | **243 comparisons, 0 trips, max 0.660** (see CORRECTION) |
| cross-rung duplication, rung vs OTHER rungs only | 0 pairs >= 0.70 |
| identical registers within a rung | 0 |
| repeated consequence sentence within a crop | 0 in all three crops |

> **CORRECTION 2026-09-01, after the independent source-truth pass.** The figure originally
> published here was 0.508 and the conclusion drawn from it -- "all three crops were authored
> independently" -- **was not supported.** The 0.508 was the PRE-echo-fix maximum, already stale when
> written; more seriously the METRIC was wrong. `difflib` defaults plus a mean of the two registers
> scored the batch's one real copy at 0.431. Under the corrected metric (`autojunk=False`,
> per-register max) that pair -- `potato`/`common-scab`/`even_watering` against beet -- scores
> **0.757**, above the refusal line. It was a copy and has been rewritten. See findings.md item 18.
> The figures in this table are now the corrected metric on the corrected batch: **243 comparisons,
> 0 trips, max 0.660**, against a recalibrated independent ceiling of **0.684**.

The remaining evidence of independent authoring stands on READING rather than on the metric.
`off_season_tillage` on potato/`wireworms` is the clearest case: radish's shipped rung asserts a
mechanism ("exposes the wireworms to birds and weather") and potato's deliberately does not, because
potato's prose says only "keep the soil well worked."

## Read by hand, item by item

**Every number and proper noun in all 87 rungs** was traced to source. Three did not appear in their
own problem's prose; all three were adjudicated and none was invented:
* `90` on potato/`insecticidal_soap` and sweet-potato/`insecticidal_soap` -- from the METHOD's own
  caution ("Can burn foliage ... above 90°F"). Restating a method caution is established: 41 rungs
  roster-wide do it. **CORRECTION:** this originally said "both rungs also carry UC IPM's moderate
  acute rating from that same caution". Only potato's did. The two crops shipped different safety
  information for the same method until the independent pass caught it; sweet-potato's rung now
  carries the rating and the PPE instruction too. The rating itself was independently verified as
  neither fabricated nor upgraded.
* `Itersonilia` in parsnip/`carrot-rust-fly`/`prompt_harvest` -- a cross-problem pairing the record
  itself asserts (the canker's cause names wounds as the entry, its prevention says to control rust fly).
* `Kennebec` / `Sebago` on potato late blight are verbatim in potato's own prevention prose.

**Every agent-flagged loose fit was read against the method's MEANS** (10 flags across 3 crops):
* ACCEPTED as exact, not loose: potato and parsnip `weed_host_control` (the method's own text names
  aphids; parsnip's source names dandelion and the phytoplasma reservoir outright), both blackleg
  rungs, parsnip/`damping-off`/`sound_sowing_practice` (matches the source clause for clause,
  including the load-bearing "about 50°F" hedge).
* ACCEPTED with the flag recorded: `prompt_harvest` -- its MEANS is written entirely around fruit
  crops, but its distinguishing clause ("taking the crop you do want, sooner") is exactly the claim,
  and carrot and radish set the precedent for roots. **CORRECTION:** this said "x4". The batch ships
  **5** such rungs and the roster now carries **8**. Counted, not estimated. The MEANS and
  `how_it_works_*` text should be widened to name root lifting.
* ACCEPTED with the map flagged, not the rung: sweet-potato/`wireworms`/`weed_host_control` is legal
  only via `insect_soft_bodied` while wireworms are explicitly hard-bodied. The ACTION matches the
  source ("control grassy weeds"); the laxness is in the type map.

**Two rungs that would have been INVENTED CONTROLS if unsourced, both verified PRESENT:**
* sweet-potato/`root-knot`/`crop_rotation` carries cover cropping -- `organic_treatment_seasoned`
  says "Solarizing the bed in the hot months and cover cropping can lower populations over time."
  The rung keeps the hedge ("contributes to a gradual decline rather than a reset").
* parsnip/`carrot-rust-fly`/`planting_time_avoidance` -- `prevention_seasoned` says "time sowings to
  dodge peak fly flights" verbatim, and "two or more generations a season" supports the rung.

## Restraint that is worth recording as much as the rungs

Agents refused type-legal methods their crop's prose does not support: `spinosad` on
parsnip/`parsnip-leafminer` (the method's MEANS names "leafminer pressure" explicitly and the crop's
prose rules sprays out); every soft-chemical and conventional rung on parsnip/`itersonilia-canker`
(prose says fungicides do not control root cankers); `bottom_watering` on parsnip damping-off
(indoor-tray meaning, parsnip is direct-sown); `garden_sanitation` on sweet-potato/`root-knot`
(carrot, okra and swiss-chard all carry one, but their prose says to remove and destroy galled
plants and sweet potato's says only that there is no rescue); `reflective_mulch` on potato aphids
(squarely on-shape for an aphid-vectored virus, but the record never mentions it).

## One defect found in MY OWN work

`pinned_ids.json` asserted the canker fungus was *Itersonilia pastinacae*. Parsnip's prose names
*I. perplexans* in both registers. I wrote a species name from memory instead of reading the record,
which is the exact failure the "compute, never assert" rule exists for. Corrected in place with the
correction noted. The type is `fungal` on either reading, so nothing downstream was blocked.

---

# WHAT THE INDEPENDENT SOURCE-TRUTH PASS ADDED, after all of the above was green

The pass ran when the batch was gate-clean (`gate_all` 121/121), suite-green (82 tests) and
mutation-clean (64 injected, 0 survivors). **It found eleven defects.** Full detail in findings.md
items 18 to 23; the short version, because this is the denominator that matters:

* **1 guard defect** -- the similarity metric hid the batch's only real copy (item 18).
* **1 rung contradicting its own crop's data** -- "warm and dry" against a record that cures at
  85 to 90 percent humidity (item 19).
* **2 safety defects** -- a copper hazard band softened on two rungs, and the same method shipping
  different safety text on two crops (item 20).
* **4 dropped hedges and ceilings** (item 21).
* **2 catalog cautions narrowed or dropped** (item 22).
* **1 of my own filed findings RETRACTED as false** (findings.md item 2), which had asserted the
  absence of the very data that proved item 19.

**One reported defect was REFUTED and not applied** -- the `beneficial_predators` hedge, where the
review compared a beginner rung against the seasoned source; the sources are register-split and both
rungs match their own register. An independent pass is evidence, not a verdict, and its findings were
read the same way this batch's were.

12 content edits followed. Everything above was then RE-RUN, not assumed: 243 precedent comparisons
max 0.660, 0 echoes, 0 cross-rung duplicates, 0 identical registers, 0 absolutes, 0 internal
vocabulary, 0 dashes, `gate_all` 121/121, all gates 0, 83 tests green.
