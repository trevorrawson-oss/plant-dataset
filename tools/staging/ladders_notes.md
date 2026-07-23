# Variety-resistance pest-migration: apple + strawberry control-ladder notes

Migration of apple (8 problems) and strawberry (12 problems) to the `id` + `control_ladder`
shape. `organic_treatment_beginner` / `organic_treatment_seasoned` removed; every other prose
field (`symptoms_*`, `cause_*`, `prevention_*`, `severity`, `audience`, `sources`,
`anchoring_urls`, `type`, `name`) copied VERBATIM from the canonical (checked programmatically).
Rung order and method set are exactly the skeleton's; only the notes are authored here.

## Gate status
- `control_ladder_gate` on a scratch (new catalog methods merged, arrays swapped in): **0 violations**
  once the two documented Task-9 `source_catalog` additions (`ohio_state_ext`,
  `ucanr_ext_woolly_apple_aphid`, both T1, from `variety_resist_catalog_sources.md`) are present.
- The brief's bare verify script (which does NOT patch `source_catalog`) reports 2 violations, both
  on *catalog methods* (`horticultural_oil`, `straw_mulch`), not on any ladder. These are the
  Task-4/Task-9 catalog-source dependency, outside this task's scope. Ladder + identity checks are clean.

---

## APPLE

### codling-moth (garden_sanitation, codling_moth_pheromone_trap, fruit_bagging, kaolin_clay, spinosad, pyrethroid)
- organic_treatment folded: "pick up/destroy dropped + infested fruit" -> `garden_sanitation`;
  "traps to time control" -> `codling_moth_pheromone_trap`; "bag individual fruit / paper bags or
  nylon footies" -> `fruit_bagging`; "spinosad or kaolin on a degree-day/petal-fall schedule" split
  across `kaolin_clay` and `spinosad`. Mating disruption (large-scale only) intentionally dropped as
  not a backyard rung.

### apple-maggot (garden_sanitation, red_sphere_trap, fruit_bagging, kaolin_clay, spinosad, pyrethroid)
- organic_treatment folded: "red sphere traps ~1 per 100 fruit, catch egg-laying females" ->
  `red_sphere_trap` (corrected to the source's 1-per-100-to-150 rate); "remove dropped fruit
  promptly" -> `garden_sanitation`; bagging (from prevention) -> `fruit_bagging`.

### plum-curculio (garden_sanitation, kaolin_clay, pyrethroid)
- organic_treatment folded: "jar branches over a sheet in early morning" (a physical knock-down with
  no dedicated catalog method) -> `garden_sanitation` note; the load-bearing "spray at petal fall,
  repeat ~2 weeks later" timing -> `kaolin_clay` (start at petal fall) and `pyrethroid` notes.
- **FLAG (honest deviation, not silent):** the old blob named *spinosad* at petal fall. Spinosad is
  weak on this weevil, and the skeleton deliberately omits a spinosad rung, going cultural -> kaolin
  -> conventional. Kept the petal-fall timing, dropped the spinosad claim as the honest call.

### woolly-apple-aphid (resistant_varieties, water_spray, beneficial_predators, insecticidal_soap, horticultural_oil)
- organic_treatment folded: "resistant rootstock MM106/MM111" (from prevention) -> `resistant_varieties`;
  "prune out heavily infested wood" (physical, no dedicated method) -> `water_spray` note; "encourage
  natural enemies" -> `beneficial_predators`; "spot-treat with soap or oil" -> `insecticidal_soap` +
  `horticultural_oil`.
- **Honest short ladder, correct:** NO conventional rung. Per `variety_resist_catalog_sources.md`
  (UC IPM), pyrethroids destroy this aphid's natural enemies and *cause* outbreaks, so a rescue rung
  would be actively harmful. Stated plainly in the `horticultural_oil` seasoned note.

### apple-scab (resistant_varieties, garden_sanitation, airflow_spacing, sulfur)
- organic_treatment folded: "sulfur on a protective schedule keyed to spring infection periods;
  easier to prevent than cure; too late once spots are everywhere" -> `sulfur` note (both registers).
  Rake/remove fallen leaves -> `garden_sanitation`; Liberty resistance -> `resistant_varieties`
  (the worked-example rung).

### fire-blight (resistant_varieties, garden_sanitation, prune_out_infection, copper_fungicide)
- organic_treatment folded: "cut 8-12 in below the strike, disinfect tools, dry weather, no spray
  cures it" -> `prune_out_infection` (the core control).
- **Advice-point (a) landed:** "avoid excess nitrogen / soft succulent growth is more susceptible"
  -> `garden_sanitation` note (both registers), per the task instruction.
- **Honest short ladder:** copper is named as a *limited, cautioned* bloom-time protectant that does
  NOT cure wood infection, with the copper cautions (fish, soil accumulation). Bottoms at soft_chemical.

### cedar-apple-rust (resistant_varieties, garden_sanitation, sulfur)
- organic_treatment folded: "protective spray from pink-bud through fruit set if rust has a history;
  otherwise usually cosmetic" -> the "cosmetic" honesty went into `resistant_varieties` +
  `garden_sanitation` notes; the pink-bud timing went into the `sulfur` note.
- **FLAG (honest deviation, not silent):** the old blob named *myclobutanil* (a synthetic DMI not in
  the catalog). The skeleton's soft_chemical rung is `sulfur`, which is a genuinely weaker rust
  protectant. Wrote the sulfur note to say so and to reinforce that rust is usually cosmetic and most
  gardeners never need to spray; the real fix is variety choice or removing the juniper host.

### powdery-mildew (resistant_varieties, airflow_spacing, garden_sanitation, sulfur)
- organic_treatment folded: "prune out white-coated shoots" -> `garden_sanitation`; "sulfur where it
  recurs" -> `sulfur`; "good airflow makes a big difference" -> `airflow_spacing`; "avoid
  nitrogen-pushed flushes" -> `garden_sanitation`. Clean mapping.

---

## STRAWBERRY
Strawberry problems carry NO `sources` / `anchoring_urls` in the canonical, so none were added
(nothing to preserve there; the gate does not require them on problems).

### slugs (garden_sanitation, slug_traps_barriers, iron_phosphate_slug_bait)
- organic_treatment folded: "remove damp hiding places, keep fruit off wet mulch, harvest promptly"
  -> `garden_sanitation`; "hand-pick in evening + shallow traps" -> `slug_traps_barriers`.
  iron_phosphate is the cautioned soft_chemical backup (scatter on soil, safer than metaldehyde, slow).

### spotted-wing-drosophila (garden_sanitation, swd_monitoring_traps, swd_exclusion_netting, spinosad, pyrethroid)
- organic_treatment folded: "pick frequently + completely, destroy overripe/culls" ->
  `garden_sanitation`; "fine exclusion netting on later crops" -> `swd_exclusion_netting`.
  spinosad is named as the best organic material (rotate for resistance, dusk for bees, PHI); the
  continuous-harvest PHI caveat carried on both spinosad and pyrethroid. Monitoring rung is honest
  ("warning tool, not control").

### tarnished-plant-bug (garden_sanitation, beneficial_predators, pyrethroid)
- organic_treatment folded: "keep bed + surroundings weed-free (alternate hosts), monitor flowers
  during fruiting" -> `garden_sanitation` (named the primary lever).
- **FLAG (mild, honest note not deviation):** biological control of lygus is genuinely limited (a
  mobile pest that reinvades from field edges). The `beneficial_predators` note says so plainly and
  keeps weed sanitation as the main control; pyrethroid note notes lygus is only moderately susceptible.

### aphids (balance_nitrogen, water_spray, beneficial_predators, insecticidal_soap, neem_oil, pyrethroid)
- organic_treatment folded: "strong water spray" -> `water_spray`; "encourage predators like
  ladybugs" -> `beneficial_predators` (ladybug, per rule); "insecticidal soap on heavy
  infestations" -> `insecticidal_soap`. "Clean certified plants (limit virus)" (from prevention) ->
  `balance_nitrogen` note. pyrethroid note is honest that it is usually counterproductive on aphids.

### two-spotted-spider-mite (garden_sanitation, beneficial_predators, horticultural_oil, neem_oil, sulfur)
- organic_treatment folded: "rinse foliage to raise humidity + dislodge mites" and "horticultural
  oil / soap for bad cases" -> `garden_sanitation` (water spray) + `horticultural_oil`.
- **Advice-point (b) landed:** "keep plants watered (mites flare on drought-stressed plants) + knock
  them back with a hard spray of water" -> `garden_sanitation` note (both registers), per the task.
- **Honesty tension carried:** `sulfur` (last rung) harms the predatory mites the
  `beneficial_predators` rung relies on. The sulfur note states this trade-off and reserves it as a
  true last resort.

### root-crown-weevils (crop_rotation, garden_sanitation, handpick, beneficial_nematodes, pyrethroid)
- organic_treatment folded: "inspect warm evenings + remove adults" -> `handpick`; "beneficial
  nematodes on soil larvae" -> `beneficial_nematodes`; "remove/destroy infested plants in fall" ->
  `garden_sanitation`. "Rotate to a fresh site, clean stock" (prevention) -> `crop_rotation`.
  pyrethroid note is honest that sprays cannot reach soil grubs, so it targets adults only and
  nematodes are the better tool for the larval stage.

### birds (bird_scare_deterrents, bird_netting)
- organic_treatment folded: "bird netting as fruit colors, secure edges; net before first fruit
  ripens" -> `bird_netting`. **Exclusion-only ladder, no insecticide rung** (task requirement).
  Scares are honestly framed as habituating and unreliable alone; netting is the reliable fix.

### gray-mold (straw_mulch, airflow_spacing, garden_sanitation)  [cultural-only]
- organic_treatment folded: "remove infected berries immediately" + "clean out old leaves at
  renovation/early spring" -> `garden_sanitation`; "open airy canopy, water at base" ->
  `airflow_spacing`; "keep fruit off wet soil" -> `straw_mulch`.
- **Advice-point (a) landed:** "avoid excess (spring) nitrogen / soft growth thickens canopy + traps
  moisture" -> `garden_sanitation` note, per task. **Cultural-only, no soft_chemical rung** (honest;
  the sources doc: homeowners emphasize cultural practices). Note says "no home spray cures it."

### anthracnose (resistant_varieties, straw_mulch, garden_sanitation, copper_fungicide)
- organic_treatment folded: "remove diseased fruit/plants, reduce splash (base watering + mulch),
  improve airflow" -> `garden_sanitation` + `straw_mulch`. "Certified plants, avoid overhead water,
  no recent-history ground" (prevention) -> `resistant_varieties`. copper is the cautioned
  before-infection-only protectant (fish, soil accumulation).

### powdery-mildew (resistant_varieties, airflow_spacing, sulfur)
- organic_treatment folded: "remove affected leaves + improve airflow" -> `airflow_spacing`;
  "resistant cultivars where recurring" -> `resistant_varieties`. sulfur note adds an honest
  strawberry-specific caveat (some cultivars are sulfur-sensitive, spot-test first).

### red-stele (resistant_varieties, crop_rotation)  [two-rung, no cure]
- organic_treatment folded: "no cure, remove/destroy affected plants; raised beds for drainage;
  resistant cultivars" -> the drainage / raised-beds / remove-sick-plants advice (no dedicated
  methods) went into the `crop_rotation` note; resistant-variety-on-wet-sites + certified stock into
  `resistant_varieties`. **Honest short ladder:** soilborne Phytophthora, no home chemical cure;
  resistant varieties + drainage + rotation stated as the whole game.

### verticillium-wilt (resistant_varieties, crop_rotation, garden_sanitation)  [no cure]
- organic_treatment folded: "no rescue, remove plants; manage by rotation + resistant cultivars" ->
  `garden_sanitation` (remove plants) + `resistant_varieties` + `crop_rotation`. The host-avoidance
  list (tomato/pepper/eggplant/potato/raspberry/blackberry) from prevention -> `crop_rotation` note.
  **Honest short ladder:** soilborne, no cure; site + variety are the levers.
