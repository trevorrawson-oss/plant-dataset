# utah_dixie shard report -- w5 warm herbs/flowers (Shape D)

**Status: DONE**

## Slugs authored (7/7)
basil, lemongrass, cosmos, marigold, nasturtium, sunflower, zinnia

Shard: `tools/staging/shards/utah_dixie_w5_warmherbs.json`

## Gate results (per crop)
| slug | region_harness | region_cell_audit |
|---|---|---|
| basil | PASS | (rolled into the 0-issue run below) |
| lemongrass | PASS | " |
| cosmos | PASS | " |
| marigold | PASS | " |
| nasturtium | PASS | " |
| sunflower | PASS | " |
| zinnia | PASS | " |

`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_w5_warmherbs.json`
-> `region_cell_audit[utah_dixie]: 0 issue(s) across 7 cell(s) in 1 file(s)`

## Judgment calls
- **Plant date, uniform Apr 1 for all 7.** None of these 7 are USU Table 1 crops (Table 1 only
  names vegetables), so there is no explicit St. George date to cite. All 7 share
  `frost_tolerance_f = 32` (same as tomato/pepper), so I timed them with the Group D
  frost-tender spring set (last_frost +2 days -> Apr 1 - Apr 15), the same anchor the
  cherry-tomato template uses, rather than the earlier Group C (Mar 15) date reserved for
  USU's explicitly-named tender vegetables. Cited generically as "USU Extension's suggested
  planting-date guidance for St. George" (`usu_ext_veg_dates`), with an explicit note in each
  `plant_out` synthesis that the crop has no listed Table 1 date.
- **Tray-started vs direct-sown, followed the Nevada donor exactly.** basil (weeks_indoors=6)
  and lemongrass (weeks_indoors=8) get `start_indoors`; the other 5 (weeks_indoors is populated
  in the dataset but the Nevada donor direct-sows all of them, several noting the crop "resents
  transplanting"/"resents root disturbance") are direct-sow, `start_indoors: null`, matching the
  donor's structural choice over the raw `weeks_indoors` field.
- **Widened lemongrass's `start_indoors` window to 26 days** (vs. the template's 14) so it spans
  Feb-Mar and renders a continuous `indoors` chain up to the April transplant, instead of a
  derived `growing` filler token in March (an artifact of an 8-week lead landing entirely inside
  February with a 14-day window). Cosmetic-only; does not touch any gated field.
- **No heat_pause for basil, lemongrass, cosmos, marigold, sunflower, zinnia** (grow/bloom
  straight through summer to frost, per instructions and the Nevada donor).
- **nasturtium carries a heat_pause**, months `[7,8,9]` (Jul-Aug-Sep), directly following both
  the Nevada donor (same months, same crop) and the cherry-tomato reference cell's own
  heat_pause months (not the `[6,7,8]` figure in the sources bible's prose -- the actual
  gate-PASSED template uses `[7,8,9]`, which I treated as authoritative). Spring harvest is
  capped at `plant_out + 90 days` = Jun 30, cited to `usu_ext_wash_frost` (the "100°F in June,
  July, and August" heat basis); no fall replant is authored (matches the load-bearing
  no-warm-crop-fall-planting rule).
- **`successions_realized` (A8 gate).** basil, cosmos, marigold, nasturtium, sunflower, and
  zinnia all carry `succession_policy.suitable = True` at crop level (lemongrass is the one
  `suitable = False` case: "a single perennial clump ... not re-sown at intervals"). This makes
  `successions_realized` a hard-required, PURE-DERIVED field on the z8 cell for those 6. I ran
  `tools.derive_realized_successions.derive_cell_realized` against each finished cell + the
  crop's real `interval_weeks` and stored the computed value verbatim (basil=1, the rest=2) --
  not hand-picked. This did not surface on the cherry-tomato template (suitable=False) or on
  lemongrass, which is why the first harness pass on the other 6 failed "successions_realized
  missing" until this was wired in.
- **No A9 (photoperiod) exposure** -- none of these 7 are alliums; each harness run printed
  "gating_factors=[] | photoperiod violations: 0" (no-op, as expected).
- **No second_planting on any of the 7**, per the load-bearing no-warm-crop-fall-planting rule.

## Sourcing
Only two USU sub-ids cited across the whole shard: `usu_ext_veg_dates` (general planting-season
anchor, all 7) and `usu_ext_wash_frost` (heat_pause basis + harvest_end cap, nasturtium only).
No Nevada/warm_arid ids leaked in. Verified zero em dashes/en dashes, zero plain "degrees" text
(all temps use the °F glyph), zero build-word leaks (shard/delta/Shape/donor/Nevada/UNR), and all
14 region_notes_beginner/seasoned strings are distinct.

## Concerns / flags for downstream review
- The Apr 1 uniform date (vs. picking Mar 15 for some) is my judgment call in the absence of a
  USU-named date for any of these 7 -- flagging for the content reviewer in case a different
  per-crop split is preferred once the whole region is assembled and cross-checked against the
  other shards (e.g. if some other builder's flower/herb crops in a different family land on
  Mar 15, an inconsistency would be worth reconciling before promote).
- nasturtium's heat_pause months `[7,8,9]` vs. the sources bible's stated `[6,7,8]`: I followed
  the actual gate-PASSED cherry-tomato precedent over the bible's prose. Worth a quick check at
  the controller level that this is the intended convention region-wide (it would be odd if
  other builders' Shape A/D cells used `[6,7,8]` instead).
