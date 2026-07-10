# dry-bean — T1 source research + pinned data (Task 1)

**Date:** 2026-07-09. **Purpose:** pin every dry-bean-specific value to a Tier-1 source before authoring
the GS anchor (spec `docs/superpowers/specs/2026-07-09-dry-bean-gs-anchor-design.md`, plan
`docs/superpowers/plans/2026-07-09-dry-bean-gs-anchor.md`). Same species as certified `green-beans-bush`
(*Phaseolus vulgaris*); shared culture values (spacing, sow depth, thin-to, germination temp, pH,
heat/frost thresholds, pests/diseases) are inherited from that cert and NOT re-sourced here — only the
dry-harvest deltas are.

**Source set — all Tier-1, all already in `source_catalog` (NO new catalog entries needed):**
`usu_ext`, `umn_ext`, `clemson_hgic`, `nmsu_ext`, `uga_ext`, `psu_ext` (+ the inherited shared-culture
T1 set from green-beans-bush). Fetches: USU beans-in-the-garden + USU storing-dry-beans, UMN
growing-beans, NMSU CR457, UGA/Clemson/PSU via search. (OSU backyard-bean page was 403-blocked; not
needed — USU/UMN cover the same facts.)

## Pinned values (dry-harvest deltas)

| Field | Value | T1 source | Verbatim |
|---|---|---|---|
| harvest readiness | pods fully mature + beginning to dry; beans rattle; harvest before pods shatter | usu_ext, umn_ext, uga_ext | USU: "Dry beans are harvested when the pods are fully mature and they are beginning to dry." UMN: "Harvest dry beans when the pods are dry and the beans inside are dry enough to rattle." UGA: "Harvest ... before the dry pods shatter." |
| harvest method (cure) | pull plants, lay in a row 5–7 days; shell; dry seeds further | usu_ext | "Pull up the plants and lay in a row in the garden for 5-7 days. Once plants are dry, remove the pods, shell out the seeds and allow some additional time for the seeds to dry further." |
| adverse-weather harvest | cut/pull whole plant early, hang upside-down indoors to finish drying | umn_ext | "Cut or pull the entire plant if the cold, rainy weather of autumn comes before the beans are fully mature. Then hang upside-down indoors to dry." |
| shelling / threshing | strip pods, shell by hand; larger crop: burlap sack + thresh with a stick; winnow in wind | umn_ext | "strip the pods from the plants and shell out by hand. For a larger crop, place the pods in a burlap sack and thresh by hitting the bag with a stick." |
| **dry-down watering taper** | reduce watering as seeds mature (the signature late-season dry-down) | usu_ext | "For dry beans, reduce water applications as the seeds begin to mature." |
| storage | airtight, cool, dark, dry; keeps ~1 yr in a jar, 10+ yr O2-removed; keeps "indefinitely" dry | umn_ext, usu_ext | UMN: "Store dry beans in bags, jars, or other containers in a dark, dry place." / "Dry beans keep indefinitely." USU: poly bags "1 year or more"; #10 cans/Mylar O2-removed "10 or more years"; "colder storage temperatures will increase shelf life"; moisture "should be low ... molds ... can grow." |
| yield (dry, shelled) | ~20–25 lb seed / 100 ft row → ~2–2.5 lb / 10 ft | usu_ext | "With dry beans expect about 20-25 lbs. of seed per 100 feet of row." |
| sow depth | ~1 in (consistent with inherited `[1,1.5]`) | umn_ext | "Plant seeds about an inch deep." |
| season length / cold-region suitability | needs a long frost-free run; won't finish in cool areas if planted late | usu_ext | "Dry beans planted after July 1 generally will not mature in cooler areas of Utah but will produce mature seeds in the warmer regions of Southern Utah." |

## Inherited from green-beans-bush (same species, already T1-cited at its cert — reuse, do not re-source)

`spacing_inches [2,4]`, `sow_depth_inches [1,1.5]`, `thin_to_inches [2,4]`, `germination_temp_f [60,85]`,
`ph` 5.8–6.5, `heat_threshold_f 90` + `heat_effect poor_fruit_set` (blossom drop >90°F),
`frost_tolerance_f 32` + `frost_effect killed`, `chilling_sensitivity_f null`, pests/diseases arrays,
companions, rotation, fertilizer. `propagule seed`, `dtm_anchor from_sow`, `germination_light neutral`,
`seedling_light na`, `tray_sowing na` (direct-sown; beans resent transplant), `weeks_indoors 0`.

## JUDGMENT CALL — crop-level `days_to_maturity` (needs Trevor's eyeball)

**No T1 page states a single dry-bean DTM number** — extension pages anchor the dry harvest on POD STATE
(dry/rattle/pre-shatter), and give snap-bean DTM (USU 50–60) not dry. The dry-bean DTM is therefore a
**documented synthesis**, consistent with the T1 facts:
- USU's July-1 cutoff implies a ~90–110 day frost-free requirement in cool climates.
- Home-garden dry bush beans mature ~90–100 days (navy/black at the fast end ~85–95; pinto ~90–100;
  kidney longer, ~100–110).

**Proposed:** `days_to_maturity = [90, 100]`, `days_to_maturity_mid = 95` — an honest bush-dry-bean
composite. Kidney-type stretch noted at the variety level. The `verification_log` will state the DTM is
synthesized from T1 season-length + pod-state facts (not a single cited figure), the same honest-synthesis
discipline green-beans-bush's cert used for its yield correction.

## Modeled `growth_stages` ladder (`day_range_from_sow`, from DTM + T1 cure timing)

Germination `[0,14]` → seedling `[10,21]` → vegetative `[21,40]` → flowering `[38,55]` →
pod_development `[50,70]` → **dry_down** `[70,92]` (pods brown, beans begin to rattle; reduce water) →
**harvest** (id `"harvest"`) `[90,100]` (~90% pods dry/rattle; harvest before shatter) → **cure_thresh**
`[95,112]` (USU 5–7 day row-cure + further seed drying). Mins non-decreasing through the `harvest` anchor
(0,10,21,38,50,70,90); `cure_thresh` sits past DTM (post-harvest, A40-exempt).

## Per-variety DTM (representative, bare numbers like green-beans-bush varieties — not a cited T1 claim)

Black Turtle ~95, Pinto ~95, Navy ~90, Kidney ~105 (noted as the long end), Jacob's Cattle ~90.

## Catalog

No new `source_catalog` entries required — every cited source is already present (Task 2 = `[]`).
