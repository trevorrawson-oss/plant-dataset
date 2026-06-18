# Re-scope note — after `ca_interior` (the ANNUAL proof cell)

## State after this cell
Both lifecycle proof cells are now authored (claude.ai side):
- **PERENNIAL** — `northern_tier` (z3–7), RELEASED (`f880a63c`). Frost-relative windows, dormant+renovation calendar.
- **ANNUAL (interior summer-plant)** — `ca_interior` (z8, z9), THIS patch. Month-resolved windows, `resolved_from:null`, calendar deferred to the deriver.

## The map is now finer than the kickoff assumed — THREE shapes, not two
The proof revealed the "annual" branch is really two sub-shapes:

| Shape | Anchoring | Calendar character | Proof cell | Templates |
|---|---|---|---|---|
| Perennial matted-row | frost-relative | dormant + renovation cycle, never season_over | `northern_tier` ✅ released | the north |
| **Interior summer-plant annual** | **month-resolved, resolved_from:null** | summer-plant → small fall crop → main spring flush → bed persists 2–3 yr | **`ca_interior`** (this patch) | **ca_desert, low_desert_az, warm_arid** |
| Frost-free fall-plant annual (plasticulture) | month-resolved, resolved_from:null | Oct–Nov plant → winter/spring harvest → pull | **NOT YET PROVEN → `fl_peninsula`** | fl_peninsula; coastal-CA TBD |

## Recommended next scope (proof-cell-first continues)
**`fl_peninsula` (z10/z11) as the THIRD proof cell** — proves the frost-free fall-plant (true plasticulture) annual sub-shape, which `ca_interior` does NOT cover. It is also the first frost-free cell (resolved_from:null is forced by the absence of frost, not just by heat-avoidance), so it doubles as the frost-free-anchoring proof. THEN the remaining warm regions scale on the now-three proven templates.

Suggested order after fl_peninsula:
1. **Interior annuals on the ca_interior template:** ca_desert, low_desert_az, warm_arid (verify each per source — A5; the deserts likely shift the summer-plant window earlier/later, do not lift ca_interior's exact dates).
2. **Coastal-CA (`ca_north_coast` / `ca_south_coast`):** genuinely source-decided perennial-vs-annual (UC Santa Cruz / coastal guidance suggests fall-plant + periodic renewal — could be EITHER a long-lived perennial OR a fall-plant annual; read the source, do not analogize from the interior or the north).
3. **`se_gulf`** (humid-summer decline) and **`hawaii_tropical`** (elevation/niche crop) — both open `grown_as` source calls.

## Hard A5 reminder (both directions)
- Do NOT template `ca_interior`'s summer-plant Jul 20–Aug 5 window onto fl_peninsula or coastal-CA.
- Do NOT template a coastal/FL fall-plant window onto ca_desert / low_desert_az / warm_arid.
Each region's `grown_as` AND window shape is a per-region SOURCE finding.

## Then (whole-crop, after all 10 region cells)
Steps 5/5.5 (source fidelity, reliable_fruit_zone warm-edge) → Steps 6–8 (bulk prose incl. the centralized `type_selection_*` section that carries the day-neutral story — see the deferred note) → Step 9 (dash/temp sweep) → Step 11 cert + the four-flip close.

## For Claude Code at THIS apply
- Preflight full-file SHA == `f880a63c…` before applying.
- Run the `berry_herbaceous_calendar` deriver (annual branch) on z8/z9; **validate the generated calendar against the authored windows** (plant_out Jul 20–Aug 5, harvest Oct + May–Jun) and resolve the open shape question: does the interior summer-plant annual cell carry `season_over`? (Likely NO — the bed is carried over 2–3 yr, not pulled at season end; no winter dormancy either. Refine the deriver if the no-off-season shape needs it.)
- The patch leaves the planting-arm-level `anchoring_urls:{}` as-is (anchoring is per-rule-entry, matching northern_tier); confirm that's the conformant shape or relocate per the certified pattern.
