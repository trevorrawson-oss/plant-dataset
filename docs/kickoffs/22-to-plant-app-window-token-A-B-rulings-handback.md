# To plant-app: window-vs-token A+B + rulings -- landed & pushed (2026-07-10)

**From:** the plant-dataset session, answering the post-#19 token-override-contract feedback
(`inbox-2026-07-10-from-plant-app-window-token-feedback.md`) plus Trevor's rulings on the follow-ups.
**Status:** committed AND pushed to `origin/main` (tip `7ec1c24`).

## Rebuild off this canonical

```
crops_data_final.json  sha256 = 35b5e5c6b344bfa42052b143bf6686d338386a7c37cbb212135fd02b700dcb53
```

Two commits landed (rebuild off the second):
- `aea8914` -- A+B (canonical `928c9d7c`)
- `7ec1c24` -- rulings (canonical `35b5e5c6`)  <-- **bump the submodule / rebuild guides.json off this**

Everything that changed is a **calendar TOKEN value** (all pre-existing valid tokens:
`heat_pause`/`cold_pause`/`plant` -> `indoors`/`plant`/`growing`/`season_over`) plus **one derived
integer** (`successions_realized`). No field renames, no shape changes -> no renderer change needed.

## What changed, and what your sweeps should now see

### Item A -- 7 se_gulf tomato fall set-out cells (your Signal A)
The `second_planting.plant_out` window was the authored intent; the calendar was stale. The fall
set-out month now shows `plant` (action-over-passive, like the #17 indoors flip), `heat_pause.months`
kept intact. Cells: cherry/roma/grape z8 (Jul->plant, stray Aug->growing), beefsteak/heirloom z8
(Jul->plant), beefsteak/heirloom z9 (Jul+Aug->plant, stray Sep->growing).
**Expect:** `scripts/audit-planting-windows.mjs` Signal A clears these 7 -- each now has a `plant`
token inside its `sp.plant_out` window.

### Item B -- 44 cells, indoors flips (heat + cold)
Real indoor-start windows that had no `indoors` token now show it on the pause months the window
overlaps. Heat-side: ca_desert tomatoes z9/z10, broccoli/kohlrabi se_gulf+warm_arid+northern_tier,
fl_peninsula tomato/jalapeno. Cold-side: broccoli/kohlrabi northern_tier z3-z7, cucurbit block
(slicing/pickling/english-cucumber, zucchini, yellow-summer-squash) ca_interior z9 + ca_south_coast z10.
**Expect:** your narrow "claim pause months when the row shows no indoors" exception STOPS FIRING on
these cells (the token is already `indoors` at source) -> exact parity, no app change.

### Rulings follow-ups (Trevor-approved)
- **13 more plant flips** (same action-over-passive rule, DTM-coherent): tomatoes warm_arid z8 (Jul),
  lettuce-leaf warm_arid z8 (Aug), 6 cucurbits low_desert_az z9 (Aug), jalapeno low_desert_az z9 (Aug).
- **10 drift-cell reconciles** surfaced by a new dataset gate (below): 7 northern_tier tomato cells
  now show `indoors` on their sow-window month; watermelon/cantaloupe nt z4 lost a stray early-April
  `indoors`; onion low_desert_az z9 lost a stray August `indoors`.
- **1 derived value**: lettuce-leaf warm_arid z8 `successions_realized` 7 -> 9 (the old value was an
  undercount from the calendar hiding the August sow).

### Two cells your feedback said to leave alone -- still left alone
jalapeno/ca_desert/z10 and tomatillo (ca_desert z10 / fl_peninsula z11): their tiny Jan `start_indoors`
windows sit on `plant` months and were NOT touched (the plant token still rightly wins).

## Two things worth knowing on the app side

1. **Boundary months were deliberately NOT flipped** (Trevor's "claim only on invisibility" ruling).
   If your sweep still reports a handful of pause months that overlap a window but show no indoors --
   e.g. a June before a late-May `sp.start_indoors`, or the far-boundary month of a `Mar-Apr` window --
   that is intentional: the pause stays the month's main story where the window is already visible via
   another indoors token. Your documented exception is the correct render there; keep it.

2. **New dataset-side gate A5c** now enforces that every contiguous `indoors` run traces to a real
   `start_indoors`/`second_planting.start_indoors` window (run-level, so legit multi-week nursery
   grow-out is fine). This means a future dataset edit cannot introduce an orphaned `indoors` token --
   the dataset side now guarantees what your token-override contract assumes.

## Suggested re-verify (your ritual)
`npm run build:guides` + `npx jest guides-shape guide-calendar.contract` + the #19 spot-checks, and
`scripts/audit-planting-windows.mjs` for Signal A. The contract sweep should now name zero
token-vs-render disagreements on the cells above.

## Open follow-ups (dataset side, not blocking you)
- Hawaii / potato / flowers plant-flip candidates: deferred for a per-crop look (NOT flipped).
- lemongrass `weeks_indoors` is null while `start_method.weeks_before`=8 (field-population gap; its
  `start_indoors` is prose-backed and correct -- kept).
- onion low_desert_az z9: its Sep-Dec `plant` run vs Sep-Oct `start_indoors` is murky (minimal fix applied).
