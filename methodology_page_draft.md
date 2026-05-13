# How plant's planting dates work: a three-tier methodology

*Methodology version 1.3, prepared 2026-04-30, reflecting Phase 1.1 dataset state, Phase 4.2 companion-claim methodology, and Phase 4.3 source-attribution architecture.*

> **For gardeners: a 30-second orientation**
>
> The dates plant shows you (when to start seeds, when to direct-sow, when to transplant, when bolt and heat-pause warnings fire, when frost is likely) come from three different data sources, picked to fit three different kinds of question.
>
> Most planting dates come from a soil-temperature anchor: a crop won't germinate or won't grow if the soil is too cold, so the date is "when does soil typically reach the threshold for this crop, in your zone." We check those dates against actual soil-temperature measurements from a NOAA reference network. Bolt and heat-pause warnings come from a near-term forecast, so the app can tell you "this lettuce is about to bolt this week" rather than "lettuce typically bolts in June." Frost dates come from NOAA's standard 30-year climate record. Separately, plant carries roughly 500 companion-planting claims (which crops grow well together, which don't); those are labeled by how well-supported each claim is, with the strongest label reserved for claims we verified against a primary extension publication.
>
> The dates are good defaults for someone gardening in your zone with no special information about their specific yard. They are not custom-fit to your microclimate. If your spot is unusually warm (south-facing slope, urban heat) or unusually cool (north-facing, frost pocket, coastal fog), your local experience may run a few days to a few weeks off the stored date. Trust your eyes and a soil thermometer over the calendar when they disagree.
>
> The rest of this page is the technical version, written for reviewers and curious gardeners who want to verify the foundation. You are not required to read it.

---

This page documents how plant arrives at the planting dates and notification triggers it shows you. It is written for two audiences: gardeners who want to know whether they can trust the dates, and reviewers who want to verify the data foundation. We aim to be specific about what we know, what we don't know, and where each kind of date comes from.

The short version is that plant uses three different data sources for three different kinds of timing decision, because no single source is right for all of them. We call this the three-tier model:

- **Tier 1 -- Soil temperature.** When can you direct-sow carrots, transplant peppers, or set out cucumbers? These dates depend on when the soil at root depth reaches a crop-specific biological threshold. We validate plant's stored soil-temperature dates against historical observations from the NOAA U.S. Climate Reference Network (USCRN).
- **Tier 2 -- Air temperature.** When does lettuce bolt? When do peppers stop setting fruit because it's too hot? These events depend on near-term air-temperature conditions at the user's actual location. plant resolves them at runtime against Apple WeatherKit forecasts.
- **Tier 3 -- Frost dates.** When is your last spring frost and first fall frost? plant uses NOAA's 1991-2020 Climate Normals, the same dataset the National Weather Service publishes for this purpose.

Each tier has its own strengths, its own limits, and its own honest disclosures. We document them all here.

This methodology applies to plant's coverage of USDA hardiness zones 3 through 11. Tier 1 (soil-temperature validation) currently covers zones 3 through 10, since zone 11 has no soil-temperature-anchored rules in the dataset; Tiers 2 and 3 cover any zone the user is in.

We also document the kinds of mistakes data projects like this one tend to make. We call these the **three failure modes**: mechanism failure (the encoded biological fact is wrong), citation failure (right idea, wrong attribution), and protocol failure (the question we asked the data wasn't one the data could answer). The taxonomy and a worked example of each appears at the end of this page.

---

## Tier 1 -- Soil temperature

### What this tier covers

Roughly 414 of plant's planting rules across 123 crops are anchored to a soil-temperature threshold. These are the rules that tell you when to direct-sow lettuce (soil at 40F), when to transplant tomatoes (soil at 65F), or when to set out peppers and eggplants (soil at 70F). The thresholds themselves are crop biology facts, sourced from extension-service guidance: the temperature at which the seed will germinate reliably, or at which the transplant will continue growing rather than stalling.

The thresholds are constant across zones. What varies by zone is the calendar date at which the soil reaches them. plant stores a date for each zone, for each crop, for each rule.

### Why USCRN

Soil temperature at 5 to 10 cm depth is not a solved consumer-API problem. WeatherKit doesn't publish it. Other commercial weather services don't publish it at gardener-relevant depths and frequencies. Extension services publish zone-level guidance ("warm-season crops need 65F soil") but rarely a continuous observation stream behind that guidance.

USCRN is the only public, continuous, quality-controlled source of soil-temperature data at the depths and frequency plant's anchors require. It's a NOAA-operated network of 113 reference-grade stations across the contiguous United States, designed specifically to provide a long-term, climate-quality observational record. Each station carries triplicate-redundant soil-temperature sensors at five depths (5, 10, 20, 50, and 100 cm), reads hourly, and is operated to a NIST-traceable calibration standard. The network has been continuously operational since 2002.

Historical USCRN data, in other words, is the gold standard for "when does soil at this depth reach this temperature in this place."

### How we validate

For every soil-temperature-anchored rule in plant, we run the following procedure:

1. Identify the crop, the zone, the rule's stored date, the threshold (40F, 65F, or 70F), and the depth (USCRN's shallowest probe at 5 cm for almost all rules; see disclosure #8 below for one exception).
2. Pull every USCRN station that maps to that USDA hardiness zone, excluding stations we hold out for cross-validation.
3. For every station-year on record, compute the date that station's soil first crossed the threshold and stayed there. We use a "cold-start" requirement (seven consecutive days below the threshold before the first crossing counts) to filter out mid-winter false starts.
4. Aggregate across station-years to get a zone-level distribution: 10th percentile, median, 90th percentile.
5. Compare plant's stored date to the distribution. Assign a verdict.

The verdicts are five labels:

- **`within_range`** -- plant's stored date sits inside the zone's empirically observed p10-to-p90 window. The date is consistent with what USCRN has actually measured in this zone.
- **`early_of_range`** -- plant's stored date is earlier than the p10 date, by a measured amount. The rule asks the gardener to plant earlier than the earliest 10 percent of station-years would support.
- **`late_of_range`** -- plant's stored date is later than the p90 date. The rule is more conservative than the bottom 10 percent of station-years.
- **`flagged_for_review`** -- the verdict cannot be confidently assigned. Most often this means the zone has fewer than 30 station-years of coverage. The validator produced numbers but they aren't statistically robust enough to trust without review.
- **`uncovered`** -- the validator could not produce a verdict at all. This label covers two distinct sub-cases that we keep separate in our internal documentation. The **thin-coverage** sub-case is when a zone has fewer than two USCRN stations or fewer than 10 station-years available; there isn't enough data to compute a percentile distribution. The **no-signal** sub-case is when the zone has stations and station-years but the climate physics doesn't produce the signal the validator looks for -- subtropical soil that never sustains a cold period before warming up cannot tell the validator "the soil crossed from cold to warm on this date" because there is no cold-to-warm crossing to detect. The 22 deployed `uncovered` verdicts in this dataset are all the no-signal sub-case in zone 10; the thin-coverage sub-case shows up as `flagged_for_review` rather than `uncovered` for zone 3, because zone 3 has two stations rather than fewer.

For each rule, plant stores the verdict, the stored date, the USCRN p10 / median / p90 dates, the median offset in days, the spread between p10 and p90, the station count and station-year count, the year range covered, the threshold itself in plain language, and the per-zone extension-source citation. This whole block sits inside the rule object as `uscrn_validation` and is meant to be transparent: anyone reading the dataset can see exactly what the validator found and why it produced the verdict it did.

### What we found

Across the 414 soil-temperature-anchored rules:

| Verdict | Count | Percent |
|---|---|---|
| `within_range` | 257 | 62.1% |
| `flagged_for_review` | 79 | 19.1% |
| `early_of_range` | 56 | 13.5% |
| `uncovered` | 22 | 5.3% |

A 62.1% within-range result on a first systematic pass is, candidly, neither bad nor great. It tells us most rules are consistent with USCRN observations. It also tells us that roughly 38% of rules are not in straightforward agreement and deserve disclosure. We disclose the largest clusters below: zone 3 thin coverage, zones 5/6 systematic early bias, and the zones 9/10 climate-physics scope limit. Together these account for about 36.5% of the dataset. The remaining handful of `early_of_range` rules (mostly cucumbers in zones 7 and 8 sitting 1 to 3 days earlier than the zone p10) are documented in their individual `uscrn_validation` blocks and discussed in disclosure #8 below; they are not large enough as a cluster to warrant separate narrative treatment.

### Honest disclosures for Tier 1

#### 1. Zone 3 has thin USCRN coverage

Zone 3 (the coldest part of the contiguous United States outside Alaska) is covered by only two non-held-out USCRN stations. At that station count, the validator's verdicts for zone 3 carry station-year counts of 13 to 28 -- below the 30-station-year threshold we set as our confidence floor. All 57 zone-3 soil-temperature rules carry `status: "flagged_for_review"` for this reason.

What this means in practice: zone-3 stored dates are anchored to extension-calendar guidance from the University of Minnesota, North Dakota State University, and the University of Maine, rather than to USCRN-derived percentiles. We retain those dates because they reflect the published extension guidance for those climates. We disclose the limitation because we cannot independently confirm them at our usual statistical bar. This is 13.8% of the validated surface (57 rules out of 414).

If you garden in zone 3 and you find plant's dates drifting from your local experience, that drift is more likely to surface here than elsewhere. We'd want to hear about it.

#### 2. Zones 5 and 6 show a systematic early bias for warm-season crops

50 warm-season rules in zones 5 and 6 (12.1% of the validated surface) show a consistent pattern: the stored date is one to three weeks earlier than the USCRN-observed zone median. The pattern is uniform across crops -- peppers, cucumbers, summer squash, beans, melons, eggplant, sweet potato, watermelon, cantaloupe -- and uniform across the two zones.

We believe this reflects extension-calendar conservatism running in the opposite direction from what we'd expect: published planting calendars for these zones tend to give "earliest reasonable" dates rather than "typical" dates, and our stored dates appear to have inherited that bias.

We considered shifting the 50 rules to align with USCRN p10 or median dates as part of the integration session that produced this validation. We chose not to. A 50-rule shift to user-facing dates is a content change that deserves more deliberation than a write-back session, and the `uscrn_validation` block on each affected rule already documents the offset, the USCRN percentiles, and the rule's status. Anyone using this data has the information needed to decide whether to defer to the stored date or to shift toward the USCRN median for their own garden's risk tolerance.

The methodology page will be updated when this scoped pass happens.

#### 3. Zones 9 and 10 hit a climate-physics scope limitation

44 rules in zones 9 and 10 (10.6% of the validated surface) come back as either `flagged_for_review` (zone 9) or `uncovered` (zone 10). The cause is not a problem with the stored dates and not a problem with USCRN coverage. It's a question the validator can't answer in those climates.

The validator's logic for spring soil-warmup events looks for the date soil crossed a threshold from below after a sustained cold period. In subtropical climates, soil rarely or never sustains seven consecutive days below 40F. The cold-start requirement that filters mid-winter false starts in temperate climates becomes a filter that removes the entire signal in subtropical climates.

This is a real characteristic of the climate, not a bug. The validator correctly recognizes the situation as `flagged_for_review` (signal partially present, low confidence) or as the no-signal sub-case of `uncovered` (signal absent) rather than misclassifying these rules as `early_of_range` or `late_of_range`.

Stored dates for zones 9 and 10 cool-season planting remain anchored to UF/IFAS, UGA, and Clemson calendar guidance, which is the right authority for subtropical climate planting. The methodology limit applies to our validation protocol, not to the data foundation underneath it.

#### 4. USDA hardiness zones do not coherently group soil-warmup behavior

This is the methodology finding most likely to be unfamiliar to readers. USDA plant hardiness zones are defined by annual minimum winter air temperature. They are not defined by spring soil-warmup timing. In our validation pass, we found that two USCRN stations in the same parent zone can produce soil-warmup dates that differ by 60 or more days for the same threshold.

A specific way to picture this: zone 7 includes parts of coastal North Carolina, central Oklahoma, parts of Arizona, and parts of the Pacific Northwest. All of these places share the same winter minimum air temperature range (zero to ten degrees Fahrenheit). They do not share the same spring soil-warmup schedule, and an aggregate "zone 7 soil reaches 65F" date is necessarily a wide range.

This is why our `within_range` verdict is framed as "the stored date sits inside the zone's empirically observed p10-to-p90 window" rather than "the stored date matches a tight central estimate." The zones themselves are wide. Honest verdict semantics have to be wide too.

If plant's stored date for your zone seems off compared to what works in your specific microclimate, this is the most likely structural reason. The dataset is correct for the zone in aggregate; your microclimate may sit in a particular tail of the zone's distribution. The Tier 2 mechanism (real-time forecast resolution at your actual coordinates) is part of how plant compensates for this on the user-facing app side.

#### 5. One catalog has heterogeneous source attributions

Three crops (`green-beans-bush`, `edamame`, and `pole-beans`) carry direct-sow rules in zones 8 through 10 -- nine deployed rules in total -- that cite different extension sources in southern zones than in northern zones. Specifically, in zones 8 to 10, the bush bean and edamame rules cite UGA's calendar guidance; the pole bean rule cites UMN's extension guidance. In zones 3 to 7, all three crops cite UMN.

The dataset's per-zone attribution structure handles this losslessly. The `zone_citations` field on each rule's `uscrn_validation` block carries the actual extension authority for that specific rule in that specific zone, not a one-size-fits-all attribution. We disclose the heterogeneity because it's an example of the structure doing its job.

We also disclose a related implementation detail: the underlying catalog (`launch_anchors.json`) has one anchor entry where the per-zone attribution required a different shape than the rest of the catalog uses, and the integration code carries a small special-case handler to read it. We chose to preserve the irregularity rather than normalize it away, because normalization would have flattened genuine per-rule variance into a less precise cross-rule attribution. The methodology page surfaces this not because it threatens correctness (the deployed `zone_citations` arrays are verified correct) but because the project values knowing where its own irregularities live.

#### 6. Where threshold values come from versus where dates come from

For Tier 1, plant's data foundation has two distinct kinds of authority underneath every rule, and we attribute both.

The **threshold value** (the temperature in Fahrenheit, the depth in centimeters, the sustain semantics) is a crop biology fact and is constant across zones. We source these from extension publications, primarily UMN, UMD, MSU, Cornell, UGA, Clemson, and UF/IFAS depending on the crop's home territory. The threshold for "warm-season transplant" is 65F at 5 cm depth whether we're talking about Minnesota or Georgia.

The **stored date** for a given zone is then the zone-specific calendar answer to "when does soil reach that threshold here." This is informed by extension calendar guidance and validated against USCRN observation.

Each rule in `crops_data_final.json` carries both the meta-source (USCRN, the network we validated against, in `source_id`) and the per-zone extension citations (the `zone_citations` array). This separates "who measured the soil temperature" from "who published the threshold guidance" cleanly. It also means that if the threshold itself is later contested or refined, the attribution chain is visible without archeology.

#### 7. Hold-out cross-check

We hold out 11 of the network's 113 USCRN stations (roughly 10%) from the main validation pass, run the validator a second time using only those held-out stations, and compare the two verdict files. This catches a specific kind of failure: validator behavior that depends on a particular station rather than on the climate signal we're trying to capture.

Most held-out passes return low-confidence verdicts, because reducing each zone to one or two stations falls below our 30-station-year confidence floor. That's expected: the held-out cross-check produces useful agreement signals only where actionable verdicts emerge on both sides.

Where actionable verdicts emerged on both the main and held-out passes, the two passes agreed: zero verdict disagreements across all 414 rules. The drift between held-out and main median dates varied by zone: in zone 5, held-out medians ran about 3 days earlier; in zone 7, held-out medians ran 6 to 17 days later; in zone 9, held-out medians ran 22 to 31 days later than the main medians. The zone-9 drift is large and worth being explicit about. The single zone-9 held-out station happens to be on the cooler-soiling end of the zone's distribution, which is consistent with the broader USDA-zone-incoherence finding (disclosure #4 above): individual stations within the same hardiness zone can sit on dramatically different parts of the soil-warmup curve, and the held-out sample is a single station in zone 9.

We read the drift pattern as sampling variance from station selection rather than methodology drift. This is a confidence signal, not a guarantee. The honest summary is: where both passes had enough data to produce real verdicts, the verdicts agreed. Where the held-out sample produced low-confidence verdicts, that's a property of running validation against a single station per zone, not a property of the methodology.

#### 8. Cucumber rules use a 2.5 cm depth proxy

USCRN measures soil temperature at five depths: 5, 10, 20, 50, and 100 cm. The shallowest probe is 5 cm. For 390 of plant's 414 soil-temperature rules, the source extension guidance specifies a depth at or near 5 cm and the validator uses USCRN's 5 cm reading directly.

Twenty-four cucumber rules across three crops (slicing cucumber, pickling cucumber, English cucumber) and eight zones are an exception. UMN's published cucumber direct-sow guidance specifies 1 inch (2.5 cm) depth, which is shallower than USCRN's shallowest probe. The validator uses USCRN's 5 cm reading as the closest available proxy for these rules. Each of the 24 rules carries `"anchor_threshold": "soil 70F reached at 2.5cm"` in its `uscrn_validation` block to surface the source spec, but the threshold-crossing test was actually performed against 5 cm USCRN data.

We disclose this because it is a small but real protocol-vs-source mismatch, and because three of the 24 cucumber rules (in zone 7) come back as `early_of_range` by 1 day. That borderline result is consistent with the depth proxy being slightly conservative: shallow soil typically warms faster than 5 cm soil, so a 5 cm-derived crossing date is slightly later than a true 2.5 cm-derived crossing date would be. The 1-day offset is well within the noise of soil-warmup variability, but the 24 cucumber verdicts are best read with the depth proxy in mind.

#### 9. The validation pass uses 2010-2025 USCRN data

USCRN has been operational since 2002, but soil-probe deployment across the network completed in 2011 (per Bell et al. 2013). Pre-2010 USCRN soil-temperature data is sparse and uneven across the network. To produce comparable distributions across stations and zones, the validation pass uses USCRN observations from 2010 through 2025 -- a 16-year record. Every `uscrn_validation` block carries `"years_covered": "2010-2025"`.

The choice to start at 2010 rather than 2002 is itself a small methodology decision worth surfacing. A longer record (2002-2025) would include more station-years for zones with early-deployed stations, but would also bias the per-zone distribution toward whichever stations happen to have the longest record. Starting at 2010 trades record length for cross-station comparability. Sixteen years of post-deployment-completion data is a meaningful base for climate-quality percentiles.

### Tier 1 citations

Three peer-reviewed papers describe USCRN's network design and soil-moisture / soil-temperature methodology. We carry all three in plant's source catalog and reproduce them here.

> Diamond, H.J., T.R. Karl, M.A. Palecki, C.B. Baker, J.E. Bell, R.D. Leeper, D.R. Easterling, J.H. Lawrimore, T.P. Meyers, M.R. Helfert, G. Goodge, and P.W. Thorne, 2013: U.S. Climate Reference Network after One Decade of Operations: Status and Assessment. *Bulletin of the American Meteorological Society*, 94(4), 485-498. DOI: 10.1175/BAMS-D-12-00170.1.

> Bell, J.E., M.A. Palecki, C.B. Baker, W.G. Collins, J.H. Lawrimore, R.D. Leeper, M.E. Hall, J. Kochendorfer, T.P. Meyers, T. Wilson, and H.J. Diamond, 2013: U.S. Climate Reference Network Soil Moisture and Temperature Observations. *Journal of Hydrometeorology*, 14(3), 977-988. DOI: 10.1175/JHM-D-12-0146.1.

> Palecki, M.A., and J.E. Bell, 2013: U.S. Climate Reference Network Soil Moisture Observations with Triple Redundancy: Measurement Variability. *Vadose Zone Journal*, 12(2), vzj2012.0158. DOI: 10.2136/vzj2012.0158.

The USCRN data product itself is available at https://www.ncei.noaa.gov/access/crn/ and is what NOAA's own data-product pages instruct users to cite.

---

## Tier 2 -- Air temperature (bolt and heat-pause)

### What this tier covers

Roughly 480 of plant's rules across the dataset are anchored to an air-temperature event rather than a soil-temperature threshold. These are the rules that warn you when cool-season crops are about to bolt (lettuce, spinach, arugula, cilantro), when fruit set is about to drop in a heat wave (peppers, tomatoes, beans), and when those windows close again as temperatures shift back.

Each rule is one of four anchor types: `bolt_threshold_start`, `bolt_threshold_end`, `heat_pause_start`, or `heat_pause_end`.

### Why WeatherKit and not USCRN

Bolt and heat-pause notifications are most useful when they tell you about the next 10 days at your specific coordinates. "Lettuce typically bolts around June 15 in your zone" is less useful than "lettuce will likely bolt this week based on the forecast." The right data product for the second question is a forecast, not a historical record.

USCRN is excellent at "what has the climate of zone 7 looked like over the available record." It is not a forecast service, and it does not run at the spatial resolution gardeners actually live at. Apple WeatherKit, by contrast, is a forecast service operating at user-coordinate-level resolution, with hourly updates and a 10-day horizon.

We use WeatherKit, in other words, because it answers the question Tier 2 anchors are actually asking.

### How resolution works

For Tier 2 rules, plant does not store a calendar date the way Tier 1 does. Instead, the dataset stores a `resolution_source` block on each rule that identifies the anchor type (`bolt_threshold_start`, etc.), names WeatherKit as the resolution source, and notes the 10-day forecast horizon and the fallback strategy beyond that horizon.

When the app needs to fire a bolt-warning notification for a specific user, the runtime layer queries WeatherKit at that user's coordinates, applies the threshold-and-sustain semantics encoded in plant's anchor catalog, and decides whether to fire. The actual temperature threshold (the specific Fahrenheit value, the sustain window in days) lives on the app side at runtime; the dataset's job is to identify the anchor class, not to encode the runtime threshold.

### What we don't claim, and why

Tier 2 is **not validated against historical observation in this phase**. We do not claim that the WeatherKit forecast skill has been independently verified by us against USCRN or any other reference. We rely on Apple's first-party operational role and well-documented forecast-skill record.

This is an honest distinction in our three-tier framing: USCRN is a validation source for Tier 1, and WeatherKit is a resolution source for Tier 2. They do different jobs, and we're explicit about which is which.

A separate honest note: any forecast service has miss rates, particularly for short-fuse heat events where temperatures spike higher or sooner than predicted. plant's bolt and heat-pause notifications are heads-up signals, not guarantees. The user's eye on the actual conditions in the actual garden is the final check before acting on any notification.

### The 10-day horizon and what happens beyond it

Cool-season bolt anchors in warmer zones (lettuce, spinach, kale in zones 8 and 9) commonly fire 30 to 60 days out from the start of the season. That window is well outside any 10-day forecast horizon. We had three options for what to show users in that case:

- **Climatology estimate.** Re-derive an estimated date at runtime from historical climate data. Adds app-side complexity, marginally better than the alternative below.
- **No notification beyond horizon.** Means no bolt warning at all for the rules that need warnings most.
- **Stored date with explicit UI signaling.** The presentational date the app shows beyond the forecast horizon is a stored, climatology-derived date, with the app's UI labeling it as climatology rather than live forecast.

We chose the third option. It is honest, simple, and robust. The dataset stores a sensible default; the app surfaces the difference between forecast-resolved and climatology-derived dates clearly enough that users can read it. This is the methodology page's honest disclosure of what happens outside the forecast horizon: the date you see is informed by historical climate, not the next 10 days, and the app tells you which is which.

### Tier 2 citation

Apple WeatherKit's underlying service is Apple Weather. The product's documentation lives at https://developer.apple.com/weatherkit/. The 10-day forecast horizon, the hourly update cadence, and Apple's first-party operational role are all documented there.

---

## Tier 3 -- Frost dates

### What this tier covers

Every zone in plant carries last-spring-frost and first-fall-frost dates, including a/b sub-zone splits and regional variants where station density supports them. These dates anchor a substantial fraction of plant's rules: "two weeks after last frost," "six weeks before first frost," and so on.

### How we get the dates

plant's frost dates come from NOAA's 1991-2020 Climate Normals, derived from cooperative observer (COOP) station data and processed by NOAA's National Centers for Environmental Information. This is the same underlying dataset that the National Weather Service uses to publish frost / freeze probability information.

The frost-date pipeline was already complete and validated before the soil-temperature work documented above. The `zone_frost_data` block in `crops_data_final.json` carries 27 entries (parent zones plus a/b sub-zones) with 37 regional variants derived from 163 station-derived entries.

### What this tier does and doesn't do

The frost-date tier is climatology, not forecast. The "last frost date" for your zone is the date by which 50% of historical years have seen their last spring freeze. It is the right anchor for the phrase "typical last frost," and it is what every published planting calendar means by that phrase.

For the user-facing app, plant pairs the climatology-derived frost date with WeatherKit forecasts when appropriate (for example, a freeze warning the night before a transplant date). The dataset's job for Tier 3 is to provide the climatology anchor; the app composites that with real-time forecast on the user side.

### Tier 3 citation

NOAA U.S. Climate Normals, 1991-2020. https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals.

---

## Companion claims

The three tiers above cover plant's planting-date and frost data. Companion-planting claims (which crops grow well together, which don't) are a separate content surface, and they need their own provenance story.

Companion planting has a trust problem. Walk into any gardening book and you will find confident lists of what plants "love" and "hate" each other, often with no citation and no distinction between a claim backed by extension research and a claim passed down because it sounded right fifty years ago. Some of those claims hold up under verification. Most of them are harder to pin down than the confident tone suggests.

We started with 503 companion claims across 123 crops, inherited from the same lineage of gardening references that everyone else draws from. Rather than prune aggressively and pretend the remaining claims were all equally well-supported, we kept the claims and labeled them honestly. This section explains what those labels mean, what we verified, what we didn't, and where we landed on the claims that turned out to be more complicated than their usual framing suggests.

### The four labels

Every good or bad companion claim in the app carries one of four labels. They live on a small colored badge on each companion card, with the full reasoning visible when you tap the tooltip.

The labels are a trust signal, not a recommendation hierarchy. An extension-backed label is not an instruction to plant the pair; a traditional label is not an instruction to avoid it. What the labels tell you is how much the claim is asking you to take on faith.

**Extension-backed.** The pairing is named in a primary extension publication -- a university cooperative extension, USDA source, or peer-reviewed paper -- and the claim as worded holds up when we read the cited source directly. Example: borage attracts bees during bloom windows that overlap with tomato, squash, and cucumber flowering (Xerces Society, "Plants you can eat are a pollinator treat").

**Mechanistic.** The claim rests on a biological mechanism that is real and well-understood, but the specific pair has not been individually studied. Example: "beans fix nitrogen for hungry corn." Legume nitrogen fixation is textbook plant science, so the mechanism is solid, even though the specific benefit to corn from this specific bean variety in your specific bed has not been pair-tested.

**Traditional.** The claim is passed down in gardening culture without a specific mechanism or study behind it. Example: "chamomile improves onion flavor." Traditional does not mean wrong; a lot of gardening tradition encodes real observation. It means we are not going to tell you research backs it when research has not tested it.

**Disputed.** The claim is actively pushed back on by an extension source or by documented evidence. This label is rare -- the current dataset does not yet use it -- but we keep it in the system because verification continues to surface cases where extensions flag specific pairings as weak fits. When those cases land firmly on the "don't do this" side of the line, they get relabeled as disputed rather than left in a softer category.

Each label also carries a **confidence level** (high, medium, low) that reflects how cleanly the claim fits the label's criteria. An extension-backed claim at medium confidence, for instance, is one where the mechanism and the citation check out but the application protocol in the source does not perfectly match the concurrent-interplanting pattern that gardeners usually mean by "companion planting." More on that below.

### What we verified and what we didn't

Here is the honest disclosure. Of the 503 companion claims in the current dataset:

| Category | Count |
|---|---|
| Individually source-verified against primary extension publications | **82** |
| Labeled by our classification system but not individually source-checked | **421** |
| **Total** | **503** |

The 82 verified claims are the ones currently labeled extension-backed. They were each checked against the cited extension publication (or a better one found during verification). The 421 unverified claims are the ones labeled mechanistic or traditional; these were read, labeled, and preserved, but not individually source-checked. We do not think claiming otherwise would be honest.

This split came from a deliberate decision. We could not personally review 503 claims to the level a domain expert would, and paying for that review was not feasible at our stage. We could not source-verify every claim without taking months. So we asked: which claims are actually making a verifiable factual assertion? Extension-backed is the only label where the label itself is a claim about sources. Mechanistic cites general science (nitrogen fixation, pollinator attraction) rather than pair-specific research, so there is no pair-level citation to verify. Traditional openly acknowledges that the claim is cultural rather than researched. Verifying the extension-backed claims does the real work; verifying mechanistic and traditional claims would be verifying that we correctly labeled them as not-extension-backed, which is a different and much smaller job.

If a claim is labeled extension-backed in the app, someone on our side pulled up the primary source, confirmed it supports the pairing, and rewrote the attribution to cite what the source actually says. Tapping the information icon on any extension-backed card shows you the specific extension publication we verified against, not just "an extension recommends this." If a claim is labeled mechanistic or traditional, we believe the label is appropriate, but we have not individually checked it.

### Why "extension-backed" is a rigorous label rather than a formatting convention

Companion planting claims are rarely cited rigorously in the popular gardening literature that most databases draw from. When an attribution is present, it is often a "some extensions recommend" or "research has shown" that turns into a specific university name once it gets copied forward a few times. Our verification protocol requires something stricter: every extension-backed claim must cite a primary extension publication that actually supports the specific claim as worded, and the protocol the extension endorses has to match the way the app surfaces the claim to the user.

Verification surfaced the same three failure modes documented in the taxonomy section at the end of this page. Two of those modes appeared cleanly in the companion-claim work: a fabricated-citation cluster (the three citations caught and corrected during Phase 4.2) and a mechanism-error case (the chives-and-apple-scab composite claim; see the failure-mode taxonomy below for the worked example). The third pattern that surfaced in the companion work is more subtle and warrants its own treatment here, because it shapes how we use the medium-confidence label on extension-backed claims.

### Extension-backed at medium confidence: when the application differs from the protocol

Some claims invoke a real, extension-documented mechanism but pair it with an application pattern that the extension literature does not actually endorse. The mechanism is right; the citations are right; the use-context the gardener will encounter in the app is different from the use-context the extension publication studied. Two worked examples:

**Marigolds and root-knot nematodes.** French marigolds (*Tagetes patula*) release a compound called alpha-terthienyl from their roots; alpha-terthienyl is toxic to root-knot nematodes (*Meloidogyne spp.*) and prevents their eggs from hatching. This is real. Iowa State, Oklahoma State, UF/IFAS (ENY-056), UH CTAHR (PD-35), NC State, and Mississippi State Extension all document the mechanism. But the protocol every one of those extensions endorses is growing marigolds as a dense cover crop for two or more months *before* planting vegetables in the same soil, not interplanting them alongside vegetables during the season. Oklahoma State adds that the effect "occurs only in the marigold's immediate root zone," meaning even a concurrent marigold doesn't radiate its benefit through the bed. The popular "plant marigolds with your tomatoes to deter nematodes" framing is a weaker version of what the research actually supports.

**Nasturtiums and aphids.** Nasturtiums really do attract aphids; their peppery glucosinolate chemistry and sugar-rich foliage make them highly preferred by several aphid species (WSU Skagit County Extension; USU 4-H Extension). But UConn IPM, in its "Perimeter Trap Cropping for Cole Crops" page, explicitly cautions that trap cropping works best for pests of *intermediate mobility* rather than those, like aphids, that are passively dispersed by air currents. Aphids can arrive on your tomatoes directly without ever visiting the nasturtium trap. The extension-documented mechanism (aphid attraction to nasturtiums) is real; the extension-documented protocol (trap cropping) is a weaker fit for aphids than for, say, flea beetles. When the app tells you nasturtiums trap aphids off your tomatoes, we want you to know both halves of that.

For application-mismatched claims like these, we preserve the extension-backed label at medium confidence and use the reason text to name the divergence explicitly. The claim is real; the application is optimistic. A gardener who plants marigolds with their tomatoes shouldn't be told the pairing does nothing, but they also shouldn't be told the extension literature backs what is actually a home-gardening convention rather than an extension protocol.

This pattern does not fit the failure-mode taxonomy at the end of this page. It is not a mechanism failure (the mechanism is real), not a citation failure (the citations check out), and not a protocol failure in the validator-limit sense (the validator is not the layer doing the work here). It is a fourth thing: an honest gap between what the research established and how gardeners typically apply it. The medium-confidence label exists to surface that gap rather than smooth it over.

### What this looks like in the app

Every companion card shows the label as a small colored badge. Tap the information icon on any card and you see the full reason text for that pairing: what kind of evidence backs it, which extension source was consulted, and, where relevant, how the protocol in the source differs from the concurrent-interplanting pattern implied by the companion framing.

### What we don't know about companion claims

Several things are honestly uncertain in this dataset, and we would rather flag them than hide them:

The 421 mechanistic and traditional claims have not been individually source-checked. If you are an extension agent, researcher, or experienced grower who notices a specific claim we have gotten wrong, we would genuinely like to hear about it. Every companion card in the app has a feedback path for exactly this reason.

The four labels (extension-backed, mechanistic, traditional, disputed) are a simplification of a messier reality. Some claims could reasonably carry two labels at once -- a pairing might have both a mechanistic basis and a long traditional history. Where a claim straddles labels, we picked the one we thought was most honest to the user, and used the reason text to surface the complexity.

Companion planting research at the specific-pair level is thin, and that is partly because pair-level effects are difficult to isolate in field trials where soil, weather, pest pressure, and gardener behavior all vary. When we say a claim is mechanistic, we mean the underlying biology is real; we do not mean the specific pair has been proven to deliver the benefit in your bed. Gardening works at scales that rarely match the scales research funding is aimed at.

This methodology is a snapshot, not a resting place. As we complete additional verification passes, and as users, extension agents, and journalists flag specific claims for review, we will update both the dataset and this page. If a claim gets downgraded, we will say so. If new extension research surfaces that upgrades a traditional claim to extension-backed, we will say that too. The goal is not to stand behind a version of the data; the goal is to show our work honestly as the data improves.

---

## How attribution is structured in the dataset

Every claim in plant's dataset has a source. The attribution architecture has two layers, and we want to be specific about which layer carries which kind of claim.

**The planting-rule layer.** Each rule in `crops_data_final.json` (when to direct-sow, when to transplant, when to start seeds indoors, when the harvest window opens and closes) carries a `sources` array of catalog ids that point into `source_catalog`. That catalog holds the full citation for each source: publisher name, URL, source class (university extension, peer-reviewed paper, horticultural authority, and so on), and an `accessed` date.

We dereference these into a per-crop `sources_summary.primary` array at derivation time. That array is what surfaces in the website's JSON-LD Article schema source list and is what an AI crawler or a careful reviewer would consult to verify the planting dates. Today, every crop's `primary` rollup contains between 19 and 25 distinct sources -- the union of every catalog id cited across the crop's zone-level and rule-level attribution arrays.

**The field-content layer.** Beyond the planting rules, plant carries field-level content for each crop: yield expectations, failure diagnostics, stage-by-stage tips, rotation guidance, storage advice, harvest-urgency framing, moon-phase-preference labels. These are user-facing growing guidance, authored across Phase 4.3 against extension cross-checks, but at the time of this writing the per-record attribution lives in our internal audit trail (the corrections inventories from Audit 5 sessions) rather than in the per-crop record itself.

The dataset reflects this honestly. Every one of these field categories carries an empty `sources` array as a scaffolding slot. A reader inspecting `crops_data_final.json` today sees the slot but no entries inside it, which is the truthful state: the work of attaching specific extension citations to each field's content is scheduled, not yet done.

Two field categories were intentionally carved out of this attribution scaffolding rather than scheduled for Phase 3.x population. The first is `recipes`, which is plant-team-kitchen-tested or eventually licensed/user-submitted content rather than extension-cited biology -- forcing a citation slot would invent a question the content type does not answer. The second is `first_planting_notify_days`, which is a calendar-arithmetic UI scheduling parameter (a number of days before a known anchor like last frost) rather than an extension-cited biological claim. Both fields are user-facing in the app but neither is a place where the source-attribution chain belongs.

**Phase 3.x is the named phase that closes this gap.** Before Phase 5 (variety expansion) begins, Phase 3.x walks the Audit 5 corrections inventories and the underlying extension sources to populate every `sources` slot on every field for every crop. Phase 5's value depends on this foundation being attributable, which is why Phase 3.x is a hard prerequisite rather than a parallel track.

We chose to ship the empty-scaffold state visibly rather than hide it because hiding it would have meant either (a) leaving the per-record attribution invisible inside the JSON, requiring readers to consult separate audit files we don't publish, or (b) deferring the visibility question entirely until Phase 3.x lands. Neither matched the stated principle of "we are specific about what we know, what we don't know, and where each kind of date comes from." The scaffolding-with-disclosure version makes the current state legible to a reviewer reading the data file alongside this page.

### Freshness signals

Three timestamps surface in the dataset:

- **`source_catalog.{id}.accessed`** -- a uniform `2026-04` value across all 53 catalog entries, set in Phase 4.3 to indicate "verified within the current active development cycle." Before launch, every URL in the catalog will be re-verified by a person, and the `accessed` field will be updated to the actual launch month with per-source precision. We disclose the uniform-now / per-source-later progression because it is both the current state and the planned state, and because honest freshness signals matter to AI crawlers and to readers checking the data for staleness.

- **`crops.[].last_reviewed`** -- a per-crop `YYYY-MM-DD` date indicating when the crop's content was most recently touched by an audit or correction. Updated as part of every dataset-mutating session's integration. The visible result on each crop's website page: "Last reviewed: 2026-04-30" or earlier, never null for any crop.

- **`crops.[].last_reviewed_session`** -- a free-form session identifier that a reviewer can use to look up exactly which session most recently touched the crop's content. Crops not touched by any Phase 4.3 session inherit the Phase 1.1 USCRN-validation pass as their floor, which is honest at the methodology level (the soil-temperature anchor validation reached every crop) even if the validation didn't necessarily verify each crop's prose content.

### What this means for a reviewer

If you open `crops_data_final.json` and look at any crop, you should be able to trace any planting-date claim from the rule's `sources` array, through the dereferenced `sources_summary.primary` rollup, to the cited extension publication's URL in `source_catalog`. The chain has no gaps.

For field-content claims (yield expectations, failure diagnostics, rotation guidance, and so on), the chain currently terminates at "scheduled for Phase 3.x." That is what the empty `sources` arrays are signaling. We don't think this is a comfortable state to ship to launch, which is why Phase 3.x blocks Phase 5 in the project plan.

---

## What we cannot tell you from this data

The three tiers above describe what plant's data foundation can answer. There is also a real and important set of questions the dataset structurally cannot answer, and we want to name them directly. A reader who comes to plant expecting answers in this category is not asking too much of gardening, but is asking too much of the present version of plant.

**Your microclimate.** USDA hardiness zones cover broad geographic ranges. Within a single zone, two yards a few miles apart can sit on different parts of the soil-warmup distribution, the frost-risk distribution, and the heat-stress distribution. A south-facing slope warms earlier in spring than a north-facing slope in the same zone. Urban heat-island effects push first-frost dates later than the surrounding rural countryside. Coastal fog suppresses peak summer temperatures relative to inland sites in the same zone. plant's dates are zone-level defaults; if your microclimate sits in a particular tail of your zone's distribution, the right reading is "this is approximately what's typical here; my specific yard may run earlier or later by a known amount, which I can learn over a season or two."

**This year's specific weather.** Tier 1 dates are climatological (when does soil typically reach the threshold). Tier 3 frost dates are climatological (when does the last frost typically happen). Neither is a forecast for 2026 specifically. A late spring or an early heat wave will move the actual right-to-plant date for any given year off the climatological default. Tier 2 (WeatherKit) is the place where this-year forecast information enters plant, and even that is only the next 10 days. For longer-horizon decisions about a specific year, the dataset cannot tell you whether this spring will run early or late.

**Your specific soil and exposure.** USCRN measures soil temperature in a standardized open-grass setting. Your yard is not a USCRN station. Soil under heavy mulch, in a raised bed, in a black-plastic-covered tunnel, or under row cover can warm 5 to 10 degrees faster than a comparable bare-soil reading. Similarly, soils with high clay content hold cold longer in spring than sandy soils at the same site. plant's dates assume an unmodified outdoor planting context. Adjustments for season-extension techniques are not encoded in the data.

**Variety-specific differences.** plant's per-crop rules cover the typical case for each crop: a typical tomato, a typical pepper, a typical lettuce. Different varieties of the same crop can differ substantially -- a 55-day determinate tomato and an 85-day indeterminate beefsteak are both "tomatoes" but have different maturity windows and different transplant-timing optimal points. The dataset currently uses crop-level rules; variety-level granularity is on the planned roadmap but not in the present-day dataset.

**Peak-production framing on continuous-harvest crops.** Some crops do not carry a `peak_production` field because their harvest pattern is continuous rather than peaked. Most herbs, most edible flowers, and a small number of crops with strongly zone-dependent peaks are intentionally left without this field; their `harvest_urgency` and `yield_expectations` framing carries the user-facing guidance instead. Forcing a "peak window" string onto a continuously-harvested basil plant or a continuously-blooming nasturtium would invent a peak that does not exist; the absence of the field is the honest answer for those categories.

**Beyond the 10-day forecast horizon.** Tier 2 disclosed this already, and it earns a second mention here because the limit applies more broadly than to bolt and heat-pause: any forecast-driven question about specific timing in the next month or two is outside the data foundation's reach. The app uses climatology-derived defaults beyond the 10-day horizon, and signals that fact to the user, but it does not pretend to know what's actually going to happen.

### Where this is headed

Some of the items above are inherent to gardening (this year's specific weather; your variety choice if you bought seedlings without a label) and no dataset will ever close them. Others are addressable. The major addressable one is microclimate, and the path is a soil-temperature probe in the user's actual garden. plant's roadmap (v1.5 / v2.0) includes integration with consumer soil probes so that the dates the app shows can shift from "typical for your zone" to "what your yard is actually doing right now." That is the next major step in the data foundation.

Until then, the honest framing is: plant's dates are zone-level climatological defaults, accurate to within the zone's own variability. A soil thermometer in your own garden, a notebook of what worked and didn't last year, and a careful eye on this season's weather are all part of the system. plant is one input; the gardener is the other.

---

## How we think about the kinds of mistakes data projects like this one make

Three failure modes show up repeatedly in agriculture data projects, and we want to name them explicitly so we can show our work on each.

**Mechanism failure** is when the encoded biological fact is wrong. The citation might be real, the protocol might be sound, but the underlying claim isn't. This shows up two ways. The first is a wrong threshold or wrong sustain logic: a rule that says "soil at 70F sustained 5 days" when the actual extension guidance is "soil at 65F sustained 3 days." The second is a claim that invokes a biological mechanism that doesn't exist or hasn't been demonstrated: a "chives repel apple scab" component bundled into a companion claim, when there is no plausible pathway for sulfur compounds in chive roots to suppress a leaf-surface fungal pathogen in the canopy. Both subspecies break the data foundation, and both compound silently because the wrong fact gets reused everywhere the same crop or pairing appears.

**Citation failure** is when the source attribution is wrong even though the underlying data may be reasonable. The publication being cited doesn't exist, or doesn't say what we said it said, or is misnamed, or is a real-but-wrong attribution. Citation failures don't break the user experience day-to-day, but they undermine the data foundation's auditability and -- worse -- can mask mechanism failures hiding underneath them. If you can't trace a number back to its actual source, you can't tell whether the number is right.

**Protocol failure** is when the validation question we asked the data wasn't a question the data could answer. The mechanism is right, the citations are right, but the validator's logic doesn't fit the climate or the crop. Protocol failures look like signal absence; the honest response is to disclose them as scope limits, not to misclassify them as data problems.

These three modes are how we frame our own audit work. We have clean documented examples of all three from the audits completed so far. Our mechanism-failure detection has been tested most thoroughly in the companion-claims surface (where Phase 4.2's verification pass surfaced the chives-and-apple-scab composite claim documented below) and is comparatively less-tested in the planting-date surface, simply because most planting-date rules are anchored to citation-verified extension guidance and the systematic mechanism-error scan there has not yet run. A planned audit (Audit 5 in our internal sequencing) extends both the citation-fabrication scan and the mechanism check across additional field categories.

### Mechanism failure example: chives, apples, and the composite claim

During Phase 4.2's verification pass on companion claims, we caught a "chives repel aphids and scab fungus" pairing in the dataset, attached to apples (and to European pears, where the same compound claim appeared). The aphid-repellent half of the claim is mechanism-plausible: allium sulfur volatiles have documented aphid-repellent effects (Durenne and Gosset, *Insects* 2018, 9(4):112) and are described at home-gardening rigor by Mississippi State Extension and USU Extension. The scab-repellent half is mechanism-fabricated.

Apple scab is a foliar fungal disease caused by *Venturia inaequalis*. The extension-recommended controls (University of Minnesota Extension's "Apple scab of apples and crabapples"; Cornell apple IPM guidelines) are resistant-variety selection, fallen-leaf sanitation, canopy pruning for faster leaf drying, and properly timed fungicide applications. No extension source endorses chives or other alliums as a scab management tactic. There is no documented pathway by which allium volatiles released at the base of an apple tree would suppress a leaf-surface fungal pathogen that requires leaf-surface moisture to infect. The scab-repellent claim is folk-remedy framing rather than extension-backed biology.

The dataset's response was to downgrade the claim from `extension_backed` to `mechanistic` at medium confidence, with reason text that names both components honestly: the aphid half is real, the scab half is fabricated, and the composite "why" text was downgraded because mixing a real mechanism with a fabricated one in a single claim is the wrong kind of evidence to call extension-backed. The claim stays in the dataset because gardeners will continue to encounter the chive-apple pairing in older companion-planting books; quietly removing it does not stop that propagation. A reclassified-and-explained claim, with the mechanism-fabricated half called out by name in the reason text, redirects the gardener back to the extension-recommended scab controls a tap away.

This is a textbook mechanism failure with one extra wrinkle: the failure is in *part* of the claim, not the whole claim. The verification protocol now treats composite claims as needing both halves checked, because folk-remedy framing tends to bundle a real mechanism with an embellishment that rides along on the real mechanism's credibility. The chives-and-aphids half would have survived an extension-backed label on its own; the bundled scab claim was where the failure lived.

The chives-and-scab case also raises a stakes principle worth stating directly: folk-remedy claims about *pest repellence* are lower-stakes (if the repellence doesn't work, the gardener still grows their crop), but folk-remedy claims about *disease prevention* can have real consequences, because a gardener relying on chives to prevent scab might skip the sanitation practices that actually work. The reclassification preserves the claim's visibility while redirecting attention to the controls that matter.

### Citation failure example #1: the Phase 4.2 fabricated-citation cluster

During the same Phase 4.2 verification pass that surfaced the chives-and-scab mechanism error, three companion-claim citations failed verification cleanly. The most prominent was "Iowa State PM 1902" -- a publication-number-pattern citation that did not resolve to any real Iowa State publication. The underlying companion concept the rules described traced cleanly to Iowa State extension materials, but the specific numbered publication was a hallucination from earlier automated dataset work. Two further citations in the same audit ("Cornell IPM" and "UC IPM" attributions, both pointing at non-specific institutional names rather than retrievable documents) failed in the same way.

This is a textbook citation cluster: each individual fabrication was plausible-looking enough to survive casual review (Iowa State really does publish numbered PM-series documents; Cornell really does run an IPM program; UC really does run IPM), but none of the specific citations as written pointed at retrievable documents. The underlying mechanisms that the cited claims described may or may not have been correct individually; we couldn't verify them either way until we replaced the fabricated attributions with real ones, which we then did during the same audit.

Citation failures matter because they mask whatever sits underneath them. An unresolvable citation can be hiding a mechanism failure, a real-but-misattributed fact, or a wholly fabricated claim with no source at all. The verification protocol now runs a systematic check for publication-number-pattern citations and unspecific institutional attributions across the dataset; that check is part of standing project work, not a one-time exercise.

### Citation failure example #2: the Palecki correction

The architecture document that guided our USCRN soil-temperature work referred to "Palecki et al. 2013 -- USCRN soil moisture and temperature observations methodology." When we ran the formal citation-verification step before publishing, that exact paper did not resolve. Searching the literature surfaced two related papers: Bell et al. 2013, which is the actual primary methodology paper for USCRN soil-moisture and soil-temperature, and Palecki & Bell 2013, which is a companion paper on triplicate-redundancy variability.

Both real papers carry verified DOIs. Both are now cited correctly in plant's source catalog. The architecture document's working text was a placeholder that propagated through several revisions and looked plausible because Palecki is a real USCRN-program author. The verification gate caught it on the first systematic pass.

We disclose this not because it caused harm (it didn't ship; the gate caught it) but because demonstrating that the gate works is itself credibility-positive.

### Protocol failure example: zones 9 and 10 cool-season "no-signal" verdicts

The 22 zone-10 cool-season verdicts described in the Tier 1 disclosures are a clean example of protocol failure. The validator's spring-soil-warmup logic asks "when did soil cross from cold to warm." Subtropical soil rarely or never goes through that transition. The validator returns the no-signal sub-case of `uncovered` honestly: the protocol can't answer the question for this climate.

The right response to a protocol failure is to disclose the limit, not to fabricate a verdict. The zones 9 and 10 stored dates remain anchored to the right authority for those climates (UF/IFAS, UGA, Clemson calendar guidance). The validator's silence on those rules is a methodology limit, not a data limit.

### What the three examples together demonstrate

The three modes share a structural pattern: the audit only catches what the audit explicitly asks about. Citation-failure detection runs systematically because we coded a publication-number-pattern scan. Protocol-failure detection runs systematically because the validator emits an `uncovered` verdict when its question doesn't fit the data. Mechanism-failure detection runs less systematically because the question "is the encoded biological fact actually true?" requires re-reading the underlying biology rather than running a pattern match.

The chives-and-apple-scab composite-claim case surfaced because Phase 4.2's verification pass was structured to ask exactly that question for every companion claim, and to ask it for each component when the claim bundled multiple mechanisms. Audit 5 will extend that question into additional field categories (yield expectations, harvest urgency, rotation, storage, and similar fields that were authored against extension sources but have not yet had an explicit "is the underlying biology correct?" pass). What we expect from that extension is more mechanism-failure cases. The honest claim now is that we know how to catch them when we look, not that the dataset is free of them.

---

## What this means for someone using the data

If you're a gardener using plant: the dates you see are the result of an actual validation pass against actual observation data, with the limits documented openly. When the data is solid, we say so. When it isn't, we say that too. The Tier 1 verdict for any rule sits in `crops_data_final.json` next to the rule itself; the methodology you just read is how those verdicts got there.

If you're a reviewer: every claim on this page can be traced to a specific data file, a specific extension citation, or a specific peer-reviewed paper. The dataset's `source_catalog` carries the full attribution chain for every source we cite. Every soil-temperature rule's `uscrn_validation` block carries the verdict, the underlying statistics, and the per-zone extension citation. Every bolt and heat-pause rule's `resolution_source` block names WeatherKit and the fallback strategy. The frost-date tier's NOAA Climate Normals attribution sits in `zone_frost_data`.

If you find a date that doesn't match your local experience, or a citation that doesn't resolve, or a rule that looks like it has a mechanism error: please tell us. The methodology is built to be auditable for exactly that reason.
