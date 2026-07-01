# Pomegranate (Punica granatum, Lythraceae) -- author-fresh gold-standard pilot NOTES

Modeled on certified **peach** for the `deciduous_fruit_tree` / `perennial_chill_gated` STRUCTURE
(inherited every gate-valid shape by deep-copy), then heavily refit to pomegranate family biology.
`status = author_fresh_pilot`, launch flags false. READ-ONLY on canonical (SHA `84321950...`
unchanged); built + gated in a scratch splice.

Output: `pomegranate_crop.json` (compact-serializable; written with `ensure_ascii=False`).
Builder: `build_pomegranate.py`. Calendars are DERIVED (never hand-authored) via
`tools/tree_calendar.derive_tree_calendar(bloom, harvest)`.

## Family refits vs peach (the heavy lifts)
- **Pollination = SELF-FRUITFUL.** `self_fertile=true`, `pollination.needs_pollinizer=false`. One
  plant fruits; a 2nd is OPTIONAL and modestly improves set (noted as optional, not required).
  Inverse of the apple cross-pollination model and unlike peach's J.H. Hale exception.
- **Own-root, NO rootstock.** Pomegranate is grown from hardwood cuttings on its own roots (not
  grafted). `recommended_rootstock=null`, `rootstock_selection_basis="own_root_no_rootstock"`, and
  a single honest `rootstock_options` entry ("Own roots (cutting-grown)") explaining there is no
  rootstock system; freeze-killed plants resprout true-to-type from the base. `start_method` +
  planting tip refit: no graft union to keep above grade.
- **Low chill (~100-250h), cold-TENDER.** `chill_hours_range=[100,250]`; `hardiness_zone_min=7`,
  `max=11`; `reliable_fruit_zone 8-10`. Variety chills 100-150 -> `min_variety_chill` floor = 100.
- **Heat-loving + drought-tolerant.** `water="moderate"`, `drought_tolerance="high"`; grown as a
  multi-stem SHRUB or small tree (`spacing_inches=[120,180]`, 10-15 ft); `container_ok=true`
  (excellent container fruit -- differs from peach's container_ok=false).
- **Signature failure = FRUIT SPLIT** from irregular water / rain near ripening. Threaded through
  watering.critical_periods, a dedicated HEAVY_RAIN weather trigger (severity high), the fruit_set
  stage, storage, and a lead failure_diagnostic. Harvest urgency "medium" (pick before rains, but
  fruit itself stores for weeks-months and is NOT chill-sensitive like peach).
- **Pests:** Leaf-footed bug (THE lead pest, high -- internal aril darkening, no external cue),
  Aphids, Whitefly, Mealybugs/scale. **Diseases:** Alternaria heart rot (black heart), Botrytis
  gray mold / fruit rot, Cercospora fruit & leaf spot (the humid-Southeast limiter).
- **Bloom is LATE + extended** (`bloom_duration_days=30`, Apr-Jun) -- largely dodges spring frost;
  humidity/still air at bloom is the real threat to set (not frost).

## Region map -- HEAT-LOVING, the OPPOSITE of cherry (warm PRIME; humid/cool marginal)
PRIME `fruits_reliably` = hot, dry: **ca_interior z8/z9, ca_desert z9/z10, low_desert_az z9,
warm_arid z8, ca_south_coast z9 (warm inland SoCal).**
`marginal`: **se_gulf z8/z9** (humid Southeast -- disease + poor set + split, the documented
"fruits poorly in Georgia" case), **ca_north_coast z9/z10** (cool foggy summers -- too little heat
to color/sweeten), **ca_south_coast z10** (coastal fog), **fl_peninsula z10** (humid), **northern_tier
z7** (cold edge -- hardy Russian cultivars, protected sites only).
`unsuitable` (empty): **northern_tier z3-z6** (winter cold kills it).
`survives_no_fruit` (empty, chill-limited): **fl_peninsula z11 + hawaii_tropical z11** (frost-free
but near-zero chill lo=0 < floor 100, + humid -> no reliable dormancy/crop). Both correctly EMPTY
under the A3 no-fruit chill split (chill_lo < floor -> over-promise -> empty).
Note the key inversion vs peach/apple: pomegranate's warm-zone limits are HUMIDITY + heat-for-
ripening, NOT chill (its chill need is met almost everywhere warm); it is limited on the COLD side.

## Sources (existing catalog, T1 only)
- **uc_ipm** (UC IPM Pomegranate) -- pests (leaffooted bug, whitefly, mealybug/scale), Alternaria
  black heart, Botrytis gray mold, short-chill/frost-sensitive culture.
  https://ipm.ucanr.edu/home-and-landscape/pomegranate/ ;
  .../agriculture/pomegranate/leaffooted-bug/ ; .../alternaria-fruit-rot-black-heart/
- **ucanr_ext** (UC ANR / UCCE / Fruit & Nut Research) -- chill 150-200, self-fruitful, own-root
  hardwood-cutting propagation (bears yr 2), hardiness ~10°F, fruit split, harvest, drought,
  interior-valley PRIME, storage, diseases.
  .../ucce-central-sierra-agriculture/pomegranate-production ;
  .../sites/btfnp/fruitnutproduction/Pomegranate/Pomegranate_Propagation/ ;
  .../uc-marin-master-gardeners/...pomegranates... ; .../blogs/...postnum=43913
- **uga_ext** (UGA C997 Pomegranate Production) -- humid-Southeast poor fruiting, Cercospora/
  Botryosphaeria fruit spot, air-circulation-at-bloom, hardy to 12°F (some to 7°F), heat req
  (>85°F for 120+ days), harvest late Aug-Nov, pH 5.5-7.2, mature 10-12 ft, full production yr 5-6.
  https://fieldreport.caes.uga.edu/publications/C997/pomegranate-production/
- **tamu_agrilife** (Texas Fruit & Nut Production: Pomegranates) -- soil adaptability (clay w/
  drainage; acid or alkaline), Texas hardiness, form/sucker/propagation topic (search-snippet
  level). https://agrilifeextension.tamu.edu/asset-external/texas-fruit-and-nut-production-pomegranates/

### FLAGGED unreadable (web access; NEVER curl/wget/pdftotext -- WebFetch only)
- **uariz_ext** "Pomegranates" PDF (extension.arizona.edu/.../Pomegranates.pdf) -- returned as
  binary/encoded PDF via WebFetch; NOT readable. NOT cited for any specific claim. Desert-adaptation
  and ~10°F hardiness are instead anchored to readable ucanr_ext/uga_ext. (Search-snippet corroborated
  hardy-to-10°F + desert-suited, but I did not pin numbers to a page I could not read.)
- **tamu_agrilife** aggie-hort pomegranate page (aggie-hort.tamu.edu/citrus/pomegranate.htm) -- stuck
  in an http<->https redirect loop; not readable. tamu_agrilife is cited only for claims visible in
  the AgriLife directory/search snippet (soil adaptability), not for the aggie-hort detail.

## Gate result (scratch splice, `canonical_scratch.json`)
- **`whole_crop_gate.py pomegranate` -> GATE: PASS (exit 0)** -- every A-gate 0 violations
  (A3 perennial cert, A4 + A22 tree/variety-chill, A20/A23 display/raw, A25/A29/A36 register,
  A33/A34 numeric/cross-consistency, A19/A26/A27 companions, B dual-voice null=0, E source-tier
  4/4 catalogued T1, F anchoring gaps=0, G flip-state).
- **A37 (calendar coherence) = 0 -- NO flags** (perennial => Bug-1 no-op; single-span fall harvest
  => no Bug-2 hole). Nothing to hand-off/normalize.
- **release_verify.py -> clean, no blocking concerns.** (Its 2 `wait`-token review notes are
  pre-existing non-pomegranate annual cells; tree calendars emit no `wait`.)
- Real canonical `crops_data_final.json` SHA unchanged (`84321950...`).
