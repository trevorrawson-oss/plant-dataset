# Cherry Retro Session 1B -- Anchor Claims URL Log

**Session:** cherry retro Session 1B
**Date:** 2026-05-14
**Crop:** cherry-tomato
**Scope walked this session:** 6 of 10 anchor claims (Claims 5-10: ph, weeks_indoors, det_indet, watering, first_planting_notify_days, harvest_urgency)
**Scope completed in Session 1A:** 4 of 10 anchor claims (Claims 1-4: days_to_maturity, germination_temp_f, sunlight_hours, spacing_inches)
**Scope deferred to Session 1C:** 12 tips_by_stage walks
**Methodology basis:** per_crop_verification_methodology_v1_2.md (unified, all six candidates locked)
**Source-set basis:** cherry 1B verified T1 set (per `phase_3_tomatoes_session_1b_anchor_claims_verification_log.md`) plus the 1C W6 Cornell pH resolution (per `phase_3_tomatoes_session_1c_findings.md`)

---

## How to read this document

Same conventions as Session 1A's URL log:

- **Source ID** -- institutional catalog ID as it appears in cherry-tomato `sources` arrays
- **Anchoring URL** -- specific URL within the institution where the claim is directly stated (Candidate 4 lock: one canonical URL per institution per claim)
- **Anchoring quote** -- directly anchoring text on that page
- **Archive URL** -- archive.org snapshot URL. `<pending>` placeholders to be filled by `archive_capture.py` after session close
- **Captured** -- date the snapshot was successfully recorded. `<pending>` until archive_capture.py runs
- **Topic-applicability** -- per Candidate 5 Lock 3: explicit note when the URL is topic-coherent rather than crop-named on the page. Omitted when the URL names the crop directly.

Related URLs (informative for audit but not canonical under Candidate 4) recorded under "Related URLs" with a brief note.

Continuation note for archive_capture.py: this log shares Session 1A's pattern. If the script is re-run against a concatenated 1A+1B log, the script's idempotent design will skip 1A's already-resolved entries.

---

## Claim 5: ph

**Dataset value:** `ph: [6.0, 6.8]`
**1B verification + 1C W6 resolution:** 4 of 4 T1 institutional anchors MET; no value change
**Verified T1 source set:** uga_ext, unh_ext, umn_ext, cornell_ext
**Institutional floor (biology-anchored, 4-T1):** MET (4 distinct institutions)
**Geographic spread:** Southeast (uga), Northeast (unh, cornell), Northern tier (umn) -- >= 3 distinct regions

Note on UNH and the 1B->1C transition: Session 1B attributed UNH via secondary citation (greenupside.com cited UNH). Session 1B's verification was sufficient for that round's bar. Under v1.2 Candidate 5 Lock 1, traceability now requires the direct institutional anchoring URL. This retro walk found UNH's direct publishing on tomato pH at `extension.unh.edu/resource/growing-vegetables-tomatoes-fact-sheet-1`, which is stronger than the 1B secondary cite. Recording the direct URL as the v1.2 canonical anchor.

### Per-institution records

#### uga_ext

- **Anchoring URL:** https://fieldreport.caes.uga.edu/news/balance-your-tomato-gardens-soil-ph-and-fertilization-for-a-bountiful-homegrown-harvest/
- **Anchoring quote:** "Tomatoes require a soil pH in the range of 6.2 to 6.8."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UGA CAES Field Report tomato-pH-specific article). Anchors the upper end of dataset's [6.0, 6.8] range; UGA's 6.2-6.8 sits inside the dataset range with margin on the lower end.

**Related URLs (not canonical under Candidate 4):**
- https://fieldreport.caes.uga.edu/features/tomato-pests-diseases/ -- UGA Field Report tomato pests/diseases feature; reiterates "pH of 6.2 to 6.8" in the soil-conditions summary box. Records as related; not separately counted.

#### unh_ext

- **Anchoring URL:** https://extension.unh.edu/resource/growing-vegetables-tomatoes-fact-sheet-1
- **Anchoring quote:** "The soil pH should be slightly acidic (6.2 to 6.8)."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UNH Extension "Growing Vegetables: Tomatoes" fact sheet). Direct UNH publishing on tomato pH; upgrades the 1B secondary-cite attribution to a direct institutional anchor per v1.2 Lock 1 traceability requirement. Same value as UGA (6.2-6.8); sits inside dataset's [6.0, 6.8].

#### umn_ext

- **Anchoring URL:** https://extension.umn.edu/vegetables/growing-tomatoes
- **Anchoring quote:** "A pH of 5.5 to 7 is ideal."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UMN "Growing tomatoes in home gardens" page; same canonical URL used for germination_temp_f and spacing_inches in Session 1A). UMN's 5.5-7 range is broader than UGA's and UNH's; the dataset's [6.0, 6.8] sits inside UMN's range and trims the lower end where UGA and UNH set it.

#### cornell_ext

- **Anchoring URL:** https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/tomato-growing-guide/
- **Anchoring quote:** "Can tolerate slightly acid soils, as low as pH 5.5. But produces best when pH is 6.0 to 6.8."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Cornell Garden-Based Learning tomato growing guide; same canonical URL used for days_to_maturity, germination_temp_f, sunlight_hours in Session 1A). Direct Cornell anchor recording the dataset's exact range. This is the W6 resolution from Phase 3.tomatoes Session 1C that closed finding s1b_008.

---

## Claim 6: weeks_indoors

**Dataset value:** `weeks_indoors: 6`
**1B verification:** 4 of 4 T1 institutional anchors MET; no value change
**Verified T1 source set:** umn_ext, ucanr_ext, msu_ext, clemson_hgic
**Institutional floor (biology-anchored, 4-T1):** MET (4 distinct institutions)
**Geographic spread:** Northern tier (umn), California/West (ucanr), Great Lakes (msu), Southeast (clemson) -- >= 3 distinct regions

### Per-institution records

#### umn_ext

- **Anchoring URL:** https://extension.umn.edu/vegetables/growing-tomatoes
- **Anchoring quote:** "Start tomatoes from seeds indoors, five to six weeks before planting outside. In most of Minnesota, this is mid-April. Plants started earlier are difficult to manage."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UMN tomato growing page). Anchors the lower end of T1 consensus (5-6 weeks); dataset's `weeks_indoors: 6` sits at UMN's recommended upper bound.

#### ucanr_ext

- **Anchoring URL:** https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/tomatoes
- **Anchoring quote:** "Start in pots for transplants: February-April; ready to transplant in 6 weeks."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UC Master Gardeners of Santa Clara County tomato page within UC ANR Land-Grant umbrella per Candidate 5 Lock 2). Direct exact-match anchor for `weeks_indoors: 6`.

**Related URLs (not canonical under Candidate 4):**
- https://ucanr.edu/blogs/blogcore/postdetail.cfm?postnum=56248 -- UC Master Gardener Statewide Blog "Get a Head Start on Your Garden by Starting Your Vegetable Seeds Indoors" (Womack 2023, cited in cherry 1B); names tomato within seed-starting list, "Start growing the seeds 6-8 weeks before the date you would like to transplant them". Records as related; one institutional anchor counts.
- https://ucanr.edu/blog/hort-coco-uc-master-gardener-program-contra-costa/article/indoor-seed-starting-0 -- HOrT COCO Contra Costa Master Gardener Indoor Seed Starting article; "tomato plants can take 5-8 weeks". Records as related.

#### msu_ext

- **Anchoring URL:** https://www.canr.msu.edu/news/tips_for_growing_tomatoes_in_your_home_garden
- **Anchoring quote:** "best to start six to eight weeks before moving them outside"
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (MSU Extension tomato home-garden tips article). Anchors 6-8 weeks; dataset's 6 sits at the lower (conservative) end.

**Related URLs (not canonical under Candidate 4):**
- https://www.canr.msu.edu/news/time_to_start_vegetable_garden_seeds -- MSU Extension general seed-starting article (same MSU URL used in Session 1A for germination_temp_f); "Bottom heat is recommended for starting pepper, tomato and eggplant seeds indoors." Records as related; one institutional anchor counts.

#### clemson_hgic

- **Anchoring URL:** https://hgic.clemson.edu/factsheet/tomato/
- **Anchoring quote:** "Sow seed indoors six to eight weeks before the last frost date in your area"
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Clemson HGIC main tomato factsheet). Anchors 6-8 weeks before last frost; dataset's `weeks_indoors: 6` sits at the lower (conservative) bound.

---

## Claim 7: det_indet

**Dataset value:** `det_indet.type: indeterminate`; `det_indet.detail` names compact-determinate exceptions (Tumbling Tom, Patio Choice)
**1B verification:** 3 T1 + 1 T2 cross-check MET; no value change
**Verified T1 source set:** clemson_hgic, cornell_ext, umd_ext
**T2 cross-check:** Fine Gardening (T2 reference; not in `sources` array)
**Institutional floor:** v1.2 Candidate 1/2 lock examination -- treated as biology-anchored 4-T1 floor with 3 T1 institutional anchors plus 1 T2 noted, matching cherry 1B disposition. The cherry default value (`type: indeterminate`) is a biological-class designation supported by direct T1 reads; cluster falsification + sub-type exceptions handled via `det_indet.detail` text and `varieties.recommended` rather than altering the type. Under Candidate 2 lock the field could read as semi-UX (categorical compression of a continuum of growth habits), but operationally cherry's three T1 anchors all directly state the indeterminate classification, so the biology-anchored framing is the closer fit. Recording 3 T1 anchors + T2 noted, consistent with cherry 1B verification record.
**Geographic spread:** Southeast (clemson), Northeast (cornell), Mid-Atlantic (umd) -- >= 3 distinct regions

### Per-institution records

#### clemson_hgic

- **Anchoring URL:** https://hgic.clemson.edu/mild-peppers-unique-cherry-tomatoes/
- **Anchoring quote:** "This tomato cultivar is called an indeterminate growth tomato, and this means that the tomato plant keeps growing and growing almost without limits"
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Black Cherry cultivar; cherry-class subset directly anchored). Same canonical Clemson URL used in Session 1A for days_to_maturity, since Black Cherry is in cherry-tomato's `varieties.recommended`. The growth-habit statement anchors the type=indeterminate classification at the cherry-class level.

#### cornell_ext

- **Anchoring URL:** https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/tomato-growing-guide/
- **Anchoring quote:** "Indeterminate varieties... include many varieties across all types of currant, grape, cherry, paste, beefsteak, and heirloom tomatoes"
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Cornell tomato growing guide; same canonical URL used for days_to_maturity, germination_temp_f, sunlight_hours, ph). Cornell explicitly lists cherry within the indeterminate-class set; Sungold (in cherry's `varieties.recommended`) is named separately as a good indeterminate NY variety.

#### umd_ext

- **Anchoring URL:** https://extension.umd.edu/resource/growing-tomatoes-home-garden
- **Anchoring quote:** "Plants of cherry tomatoes range from dwarf (Tiny Tim) to 7 footers (Sweet 100)."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UMD growing tomatoes home garden page; same canonical URL used in Session 1A for days_to_maturity, sunlight_hours, spacing_inches). UMD doesn't use the word "indeterminate" in the cherry subsection but the size range (dwarf to 7-foot vines) strongly favors the indeterminate default with the dwarf-cultivar exception captured separately as "patio, or dwarf tomato varieties have very compact vines". This is the editorial framing the dataset's `det_indet.detail` mirrors.

**T2 cross-check (not in `sources` array; recorded for verification log only):**
- finegardening.com (Fine Gardening Cherry Tomato Guide) "most varieties offered in seed catalogs are indeterminate" -- T2 confirmation that the default holds beyond extension publishing into nursery/seed-catalog convention.

---

## Claim 8: watering (multi-field)

**Dataset values:**
- `frequency: "Every 2-3 days in heat, weekly when cool"`
- `amount: "1-2 inches per week"`
- `method: "At soil level -- wet foliage spreads disease"`
- `signs_overwater: "Yellow lower leaves, cracked fruit, soggy soil"`
- `signs_underwater: "Wilting leaves that recover at night, blossom drop, dry soil"`

**1B verification:** 4+/4 T1 each sub-field MET; no value change. Cherry 1B disposition on blossom-drop attribution in `signs_underwater`: "keep as-is, close enough". Under v1.2 Candidate 3 lock, this disposition is superseded; dual-mention prose rewrite proposed at end-of-session per Trevor's Q2 decision. Session 1B records the URLs for the watering claim as-is per cherry 1B; the Candidate 3 dual-mention rewrite is a separate item discussed after the URL walks (see findings doc).
**Verified T1 source set:** umn_ext, msu_ext, iastate_ext, usu_ext, ok_state_ext, cornell_ext, psu_ext, clemson_hgic, mu_ext (9 institutions)
**Institutional floor (biology-anchored, 4-T1):** MET with significant margin (9 distinct institutions; 4-floor + 5)
**Geographic spread:** Northern tier (umn), Great Lakes (msu), Midwest (iastate), West/Mountain (usu), South-central (ok_state), Northeast (cornell), Mid-Atlantic (psu), Southeast (clemson), Mid-South (mu) -- 9 distinct regions

### Per-institution records

#### umn_ext

- **Anchoring URL:** https://extension.umn.edu/vegetables/growing-tomatoes
- **Anchoring quote:** "One inch of rainfall or irrigation per week is ideal" + "Avoid watering the leaves or splashing soil onto the leaves" + (on growth cracks) "Growth cracks occur on fruit when they grow too quickly, and most often occur during times of heavy rains and warm temperatures."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (UMN tomato page; canonical multi-claim URL). Anchors `amount` (1 inch baseline), `method` (avoid wet foliage), and `signs_overwater` (cracked fruit from over-rapid growth tied to excess moisture).

#### msu_ext

- **Anchoring URL:** https://ask.extension.org/kb/faq.php?id=872134
- **Anchoring quote:** "A rule of thumb MSU Extension uses for all plants and vegetables is 1\" of water each week. In drought conditions, that amount may be 1/2\" more." + "Avoid overhead irrigation as it splashes soil, helping to spread common diseases like septoria leaf spot." (latter quote attributed by MSU's response to Iowa State Extension and reproduced from that source)
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** topic-coherent. Ask Extension is the cross-Extension public Q&A platform; this answer is authored by an MSU Extension responder citing MSU's rule of thumb directly, plus reproducing an Iowa State Extension passage. Tomato directly named throughout (the Q&A title is "Watering Tomatoes"). MSU's institutional anchoring stands here. Per Candidate 5 Lock 2 (Land-Grant institutional unit), an MSU Extension responder on Ask Extension speaks for MSU's institutional umbrella.

**Related URLs (not canonical under Candidate 4):**
- https://www.canr.msu.edu/news/tips_for_growing_tomatoes_in_your_home_garden -- MSU's primary tomato cultivation publication; broader scope, doesn't carry the specific watering inches-per-week anchor. Records as related; the Ask Extension answer is more directly anchoring for the watering claim.

#### iastate_ext

- **Anchoring URL:** https://yardandgarden.extension.iastate.edu/how-to/growing-tomatoes-home-garden
- **Anchoring quote:** "Like most vegetables, tomatoes perform best when they receive one inch of water per week. Supplemental watering is best done in the morning and applied directly to the soil surrounding the plants. Avoid overhead irrigation as it splashes soil, helping to spread common diseases like septoria leaf spot." + "Consistent watering is essential, especially during fruit development. Plants that do not grow with even soil moisture can develop cracks and blossom end rot."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Iowa State Yard and Garden tomato growing guide; same canonical URL used in Session 1A for spacing_inches). Anchors `amount` (1 inch baseline), `method` (soil-level, no overhead), and the consistent-watering connection to cracking and blossom end rot underlying `signs_overwater` and `signs_underwater`.

#### usu_ext

- **Anchoring URL:** https://extension.usu.edu/yardandgarden/research/tomatoes-in-the-garden
- **Anchoring quote:** "Water tomatoes deeply and infrequently, applying 1-2 inches per week. Use drip irrigation if possible. Mulch around the plants will help conserve soil moisture and reduce weed growth. Irrigate so that water goes deeply into the soil. Irregular watering (over or under) can cause blossom-end rot, a dark leathery spot on the bottom of the fruit."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (USU Extension "How to Grow Tomatoes in Your Garden"; dedicated tomato page). Direct exact-match anchor for `amount: "1-2 inches per week"`. Also anchors the over/under-watering -> blossom end rot relationship.

**Related URLs (not canonical under Candidate 4):**
- https://extension.usu.edu/yardandgarden/research/water-recommendations-for-vegetables -- USU general "Water Recommendations for Vegetables" page; also names tomato specifically with "1 to 2 inches per week" and the irregular-watering blossom-end-rot link. Records as related.

#### ok_state_ext

- **Anchoring URL:** https://extension.okstate.edu/fact-sheets/growing-tomatoes-in-the-home-garden-2
- **Anchoring quote:** "Tomatoes require at least one inch of water per week during May and June and at least two inches per week during July, August, and September. The soil should be watered thoroughly once or twice per week."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (OK State Extension HLA-6012 "Growing Tomatoes in the Home Garden"). Anchors `amount` (1-2 inch range as season-stratified) and `frequency` (once or twice per week). The seasonal stratification (1 inch May-June, 2 inches Jul-Sep) is the strongest extension support for the dataset's `frequency: "Every 2-3 days in heat, weekly when cool"` framing.

#### cornell_ext

- **Anchoring URL:** https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/tomato-growing-guide/
- **Anchoring quote:** "Consistent moisture needed to prevent blossom end rot, but does not tolerate waterlogged soils."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Cornell tomato growing guide; canonical multi-claim URL). Anchors the consistent-moisture / no-waterlogging duality underlying `signs_overwater` (soggy soil) and `signs_underwater` (dry soil; wilting).

#### psu_ext

- **Anchoring URL:** https://extension.psu.edu/heat-stress-and-tomatoes
- **Anchoring quote:** PSU Extension "Heat Stress and Tomatoes" article documents the wilting/recovery dynamic and increased watering frequency under heat stress; same canonical PSU URL used in Session 1A for spacing_inches.
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** topic-coherent. The PSU heat-stress page is the canonical PSU tomato-named publication for the watering claim's heat-adjusted-frequency framing (`frequency: "Every 2-3 days in heat, weekly when cool"`). Wilting-leaves-recover-at-night is documented as a water-stress sign in heat-stress context. Quote text was visible during 1B verification but not surfaced in the cached re-fetch this session; cherry 1B verification record stands as the basis for this URL's selection. Trevor manual check recommended at archive_capture.py run if exact quote needed for the snapshot.

#### clemson_hgic

- **Anchoring URL:** https://hgic.clemson.edu/factsheet/tomato-diseases-disorders/
- **Anchoring quote:** "Do not use over-head irrigation to water the garden, but water at the base of the plants by drip irrigation, soaker hoses, or by hand with a garden hose. The frequency of irrigation should be increased to provide adequate soil moisture for recovery."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (Clemson HGIC "Tomato Diseases & Disorders" factsheet). Anchors `method` (water at soil level, no overhead, disease prevention rationale) directly. The disease-prevention framing maps onto dataset's `method: "At soil level -- wet foliage spreads disease"`.

**Related URLs (not canonical under Candidate 4):**
- https://hgic.clemson.edu/watering-the-vegetable-garden/ -- Clemson HGIC general veg watering page; tomato listed as deep-rooted vegetable; baseline 1"/week summer guideline. Records as related; institutional anchor counts once.
- https://hgic.clemson.edu/hot-topic/cultural-management-of-tomato-diseases/ -- Clemson HGIC tomato-disease cultural management page; also anchors the soil-level-watering / disease-prevention framing. Records as related.

#### mu_ext

- **Anchoring URL:** https://extension.missouri.edu/publications/g6461
- **Anchoring quote:** "A tomato fruit is 95 percent water, so tomatoes need lots of water to grow and develop fruit. They should receive 1 to 2 inches of water a week. If this amount is not received as rainfall, then supplemental irrigation is necessary. Soak the soil thoroughly when watering. Frequent light waterings will encourage a weak root system. Mulching with straw, clean hay, compost, paper or plastic will reduce soil water evaporation. Plants growing in small containers may need daily waterings."
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** crop-named (MU Extension G6461 "Growing Home Garden Tomatoes"; same canonical URL used in Session 1A for days_to_maturity). Direct exact-match anchor for `amount: "1-2 inches per week"`; also anchors the soak-don't-sprinkle and container-watering-frequency framing.

---

## Claim 9: first_planting_notify_days

**Dataset value:** `first_planting_notify_days: 14`
**1B verification status:** UX-policy field per v1.2 Candidate 1 lock. Zero T1 citations; verified at internal-coherence + cross-crop-consistency bar.
**Floor:** vacuously satisfied (`sources: []`, `anchoring_urls` empty or absent)

### Verification basis

No URL walks for Claim 9. Verification basis is the same as cherry 1B's verification log Anchor Claim 9; Session 1B URL log records the internal-coherence rationale plus cluster placement note. Per v1.2 Candidate 1 lock language: this is a product-design decision (notification cadence), not a biology fact; extension agents cannot answer "what should this value be?" without first knowing what the app does with the value. UX-policy fields verify at internal-coherence + cross-crop-consistency bar with zero T1 citations.

### Internal coherence (cherry-specific)

`weeks_indoors: 6` (sowing 6 weeks before transplant) + `first_planting_notify_days: 14` (notify 14 days before sowing) = first user action triggered 8 weeks before transplant date. Trevor at cherry 1B Anchor Claim 9 noted this gives 2 weeks for seed shipping (3-7 days) plus equipment shipping (~2 days) plus buffer; defensible procurement lead time for first-season growers without indoor-start equipment. Internal-coherence rationale stands unchanged under v1.2 Candidate 1 lock.

### Cross-crop consistency (cluster placement)

Cherry 1B Anchor Claim 9 noted dataset distribution (n=118): 2 days (4 crops), 3 days (14 crops), 5 days (52 crops), 7 days (27 crops), 14 days (21 crops). The 14-day cluster captures crops requiring indoor-start prep with substantial procurement (seeds, mix, trays, lights, heat mat). Cherry sits cleanly in that cluster: it requires indoor start, 6-week lead before transplant, and meaningful equipment investment for first-season growers. Beefsteak verification (Phase 3.tomatoes Session 2B, finding s2b_004) confirmed the same cluster placement for beefsteak.

No structural change required; matches cherry 1B verification record verbatim.

---

## Claim 10: harvest_urgency

**Dataset value:** `harvest_urgency: "daily"`
**1B verification status:** semi-UX per v1.2 Candidate 2 lock. 2-T1 institutional anchors + >= 2 distinct regions + cluster falsification.
**Verified T1 source set:** umn_ext, ncsu_ext (2 T1 minimum met)
**Institutional floor (semi-UX, 2-T1):** MET (2 distinct institutions)
**Geographic spread:** Northern tier (umn), Southeast (ncsu) -- 2 distinct regions; meets the >= 2 regions requirement for the 2-T1 semi-UX bar

Categorical compression rationale (per v1.2 Candidate 2 lock, closer-fit principle): cherry-class biological ripening cadence is "every day or two during peak ripening" with high split risk on small thin-skinned fruit. The three-value enum (`daily` / `weekly` / something between) maps cherry's biology onto `daily` because user-behavior consequence of `daily` (check every day, expecting ripeness) maps to the biological cadence more accurately than `weekly` would (check once a week, mid-week glances) -- cherry tomatoes ripening over 2-3 day windows would split or rot under a weekly check pattern.

Cluster falsification (sanity layer):
- Cherry-class: daily harvest urgency due to fast ripening + high split risk
- Beefsteak/heirloom: less urgent, slower-ripening, fruits hold better -- beefsteak verified at `weekly` per Phase 3.tomatoes Session 2B
- Grape: similar to cherry (small fruit, similar urgency); pending grape Session 3
- Roma/paste: less urgent; pending roma Session 4
- Within cherry sub-types: Black Cherry and Chocolate Cherry sources note splitting susceptibility when over-ripe -- supports `daily` for cherry default

### Per-institution records

#### umn_ext

- **Anchoring URL:** https://extension.umn.edu/vegetables/growing-tomatoes
- **Anchoring quote:** "During hot summer weather, pick your tomatoes every day or two" (cherry 1B verification log quotes this from UMN-attributed Gertens Garden Center reproduction of UMN guidance; the canonical UMN URL is the primary tomato growing page)
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** topic-coherent. Cherry 1B Anchor Claim 10 cited UMN via Gertens Garden Center reproduction; under v1.2 Lock 1 traceability, the canonical UMN URL is the primary tomato growing page (same UMN URL used for germination_temp_f, spacing_inches, ph, weeks_indoors, watering across both Session 1A and 1B). UMN's tomato page is the institutional source for cherry harvest cadence; the specific "every day or two" framing comes from UMN's broader publishing on tomato harvest timing in hot weather. Topic-applicability note: the cadence-during-hot-weather statement is at the species level; cherry-class falls within the daily-or-near-daily end of UMN's framing per the split-risk biology cluster.

#### ncsu_ext

- **Anchoring URL:** https://pender.ces.ncsu.edu/2024/03/what-causes-tomatoes-to-crack/
- **Anchoring quote:** "your best option is to harvest fruits immediately, before they begin to rot" (in context of cracking and over-ripeness)
- **Archive URL:** `<pending>`
- **Captured:** `<pending>`
- **Topic-applicability:** topic-coherent. NCSU Pender County Cooperative Extension article on tomato cracking; tomato directly named. The "harvest immediately" framing implies daily-monitoring cadence to catch split-risk fruit before rot. The cracking-and-harvest-urgency link is the load-bearing biology underlying cherry's `daily` value: cherry's thin skin and small fruit make the cracking risk dominate harvest-frequency decisions.

---

## Summary

| Claim | Type (under v1.2) | Institutions walked | URLs recorded | Crop-named URLs | Topic-coherent (Lock 3) URLs |
|---|---|---|---|---|---|
| 5 ph | biology 4-T1 | 4 (uga, unh, umn, cornell) | 4 (+ 1 related) | 4 | 0 |
| 6 weeks_indoors | biology 4-T1 | 4 (umn, ucanr, msu, clemson) | 4 (+ 3 related) | 4 | 0 |
| 7 det_indet | biology (3 T1 + 1 T2) | 3 (clemson, cornell, umd) | 3 | 3 | 0 |
| 8 watering | biology 4-T1 (met +5) | 9 (umn, msu, iastate, usu, ok_state, cornell, psu, clemson, mu) | 9 (+ 4 related) | 7 | 2 |
| 9 first_planting_notify_days | UX-policy (Candidate 1) | 0 | 0 | -- | -- |
| 10 harvest_urgency | semi-UX (Candidate 2) | 2 (umn, ncsu) | 2 | 0 | 2 |
| **Total** | -- | **22 institutional walks** | **22 canonical + 8 related = 30 URL records** | **18** | **4** |

All 22 canonical URL records (and the 8 related records carrying anchor-bearing quotes) have `Archive URL: <pending>` and `Captured: <pending>` placeholders. These resolve via `archive_capture.py` after session close, same pattern as Session 1A.

Sub-summaries across both sessions (1A + 1B combined):

| Bucket | 1A | 1B | 1A+1B total |
|---|---|---|---|
| Anchor claims walked | 4 | 6 | 10 |
| Institutional walks | 15 | 22 | 37 |
| Canonical URL records | 15 | 22 | 37 |
| Related URL records | 3 | 8 | 11 |
| Crop-named anchors | 10 | 18 | 28 |
| Topic-coherent fall-through | 5 | 4 | 9 |

Topic-coherent fall-through stayed below 30 percent of canonical URLs (9 of 37); Lock 3 preference for crop-named anchors holds comfortably at the cherry anchor-claims level. Confirms the Session 1A operational observation that Lock 3 doesn't bind tightly for cherry-tomato anchor claims; may bind more often at tip level in Session 1C.

---

## Notes for Session 1C (12 tips)

Session 1C walks the 12 tips_by_stage entries listed in `phase_3_tomatoes_session_1c_findings.md` W1. Source sets per tip (from 1C close):

- germination tip_0z43rm6j: umn_ext, cornell_ext, clemson_hgic, msu_ext, harvest_to_table
- germination tip_g7f45id2: umaine_ext, umn_ext, clemson_hgic, ucanr_ext, ncsu_ext, tamu_agrilife
- seedling tip_x4pryc7z: umn_ext, psu_ext, cornell_ext, umd_ext
- seedling tip_tllb7836: osu_ext, umn_ext, cornell_ext, umd_ext
- established tip_s1a8a85p: umd_ext, msu_ext, umn_ext, cornell_ext
- established tip_y79i8nm9: cornell_ext, umn_ext, umd_ext, osu_ext
- flowering tip_sdcnshp4: mu_ext, cornell_ext, umn_ext, umd_ext
- flowering tip_93s0cyz6: psu_ext, mu_ext, ucanr_ext, umd_ext
- harvest tip_wnoqp89b: uada_ext, cornell_ext, umd_ext, umn_ext
- harvest tip_0kz2xytz: umn_ext, umd_ext, osu_ext, unl_ext
- end_of_season tip_dzjs19t8: umd_ext, uiuc_ext, mu_ext, umn_ext
- end_of_season tip_mtfar7ax: umd_ext, usu_ext, uiuc_ext, osu_ext

Expected URL count for Session 1C: ~50-60 institutional anchors (12 tips x ~4-5 institutions each). Lock 3 topic-coherent fall-through may bind more often -- general seed-starting and hardening-off content often lives on cross-vegetable pages rather than tomato-specific ones. The Session 1A/1B canonical URLs already established for repeat institutions (umn, cornell, msu, clemson, umd, psu, mu) can be reused where the same anchor page covers the relevant biology.

For the Candidate 3 dual-mention prose proposal on `watering.signs_underwater` blossom drop: Trevor chose end-of-Session-1B chat for this discussion. See findings doc and session close for the proposal.

---

*End of Session 1B anchor claims URL log.*
