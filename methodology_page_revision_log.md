# Methodology Page -- Revision Log

This file documents revisions made to `methodology_page_draft.md` after Session 10's initial draft.

## Revision 5 -- 2026-04-30, Phase 4.3 Session 16 post-audit remediation

Three small additions reflecting Phase 4.3 Session 15's audit findings and Phase 4.3 Session 16's remediation. Page version bumped from 1.2 to 1.3.

### Changes applied

1. **F3.2 / S15_010 carve-out disclosure added.** Inserted a paragraph in the "How attribution is structured in the dataset" section, after the "every one of these field categories carries an empty sources array" paragraph, naming `recipes` and `first_planting_notify_days` as the two field categories intentionally carved out of the source-array scaffolding. Recipes are plant-team-kitchen-tested or eventually licensed/user-submitted content; `first_planting_notify_days` is a UI scheduling parameter rather than an extension-cited biological claim. Closes the audit's noted gap that the page enumerated 7 scaffolded categories without naming the 2 carve-outs.

2. **Catalog count updated from 50 to 53.** Phase 4.3 Session 16's S15_008 catalog gap remediation added 3 catalog entries (uga_c963_vegetable_gardening, uga_c1206_homegrown_pumpkins, clemson_hgic_1322_sweet_potato) to close the prose-vs-catalog publication-number gap surfaced in the audit's F2.2 finding. The "Freshness signals" subsection's accessed-date claim now reads "all 53 catalog entries" rather than "all 50."

3. **F3.1 "no gaps" claim left as-is.** The audit flagged that the "What this means for a reviewer" section's claim "the chain has no gaps" was overstated given F2.2's catalog gap. Session 16 chose the remediate-now path (Trevor decision Option A on S15_008): added the 3 missing catalog entries and appended them to 37 affected rules, plus updated 2 UF/IFAS catalog name fields to disclose EDIS dual-IDs, plus fixed a wrong ENH number in 22 synthesis_note prose strings. With those fixes, the "no gaps" claim is now accurate and no methodology-page text change is needed for F3.1.

### Items deferred (consistent with Revision 4)

- Phase 3.x population work (sibling-field-beta sources arrays remain empty pre-Phase-3.x; the methodology page's "scheduled for Phase 3.x" framing is current).
- Pre-launch human-eyes per-source verification (the uniform `accessed: "2026-04"` on all 53 entries is still the disclosed state).
- Variety-level rollup type design (Phase 5 schema decision).

### Audit findings that led here

- F3.1 "the chain has no gaps" overstatement -- closed by S15_008 remediation, no page text change.
- F3.2 "recipes and first_planting_notify_days carve-outs not disclosed" -- closed by the new paragraph in the attribution section.
- F2.2 "six publication numbers cited in synthesis_note prose without catalog entries" -- closed by S15_008 dataset remediation; methodology page's catalog count updated to reflect the new 53 entries.

### Page metrics post-Revision-5

- Word count: ~6,500 (up ~100 from Revision 4)
- Honest disclosure items: 13 (one new: carve-out disclosure)
- Em-dash check: clean
- New section count: 0 (carve-out adds a paragraph within an existing section; catalog count update is a single number)

## Revision 4 -- 2026-04-30, Phase 4.3 close source-attribution architecture

Three additions reflecting the Phase 4.3 schema state and the Phase 3.x pre-Phase-5 commitment. Applied at Phase 4.3 Session 14 close. Page version stamp bumped from 1.1 to 1.2.

### Changes applied

1. **New section: "How attribution is structured in the dataset."** Inserted between the Companion-claims section and the What-we-cannot-tell-you section. Documents the two-layer attribution architecture: the planting-rule layer (rule-level `sources` arrays, dereferenced into `sources_summary.primary`, surfaced as the website's JSON-LD Article schema source list) and the field-content layer (currently scaffolded with empty `sources` arrays on `yield_expectations`, `failure_diagnostics`, `tips_by_stage_sources` (sibling), `rotation`, `storage`, `harvest_urgency_sources` (sibling), and `moon_phase_preference`). Explains the sibling-field-beta pattern for non-dict-shaped fields. States the Phase 3.x mandatory pre-Phase-5 gate explicitly.

2. **Freshness signals subsection.** Documents the three timestamp fields on the dataset (`source_catalog.{id}.accessed`, `crops.[].last_reviewed`, `crops.[].last_reviewed_session`). States the uniform `2026-04` accessed value as a current-development-cycle snapshot and discloses the pre-launch human-eyes re-verification obligation that will produce per-source timestamps.

3. **Peak-production gap disclosure** added to "What we cannot tell you from this data." Explains why some crops (most herbs, most edible flowers, three borderline cases) intentionally lack `peak_production` field content: their continuous-harvest framing makes a peak-window string an invented peak rather than a real one. Their `harvest_urgency` and `yield_expectations` framing carries the user-facing guidance instead.

### Items deferred to later sessions

- **Per-source `accessed` timestamps.** Pre-launch human-eyes pass; not a methodology-page edit.
- **Phase 3.x kickoff prompt and population strategy.** Phase 3.x scope-question; not a methodology-page edit.
- **Variety-level rollup type design.** Phase 4.3 / Phase 5 schema decision; deferred per Section G.4 of Session 13.6.

### Page metrics post-Revision-4

- Word count: ~6,400 (up from ~5,800 after Revision 3)
- Honest disclosure items: 12 (up from 9; +1 attribution architecture, +1 freshness signals, +1 peak-production gap)
- Em-dash check: clean
- New section count: 1 (How attribution is structured in the dataset)
- Two new subsections: Freshness signals; What this means for a reviewer

## Revision 3 -- 2026-04-27, companion section integration

The Phase 4.2 deliverable `methodology_page_companions_section_edited.md` (uploaded to project knowledge under that filename; the document index referenced it as `methodology_page_companions_section.md`) was integrated into the methodology page draft. This is the final pre-publication structural change. After Revision 3 the methodology page covers all of plant's content claim categories that have completed verification.

### Decisions made during the merge

The merge required reconciling two separately-authored treatments of the three-failure-mode taxonomy. The companion section was authored against the taxonomy as Phase 4.2 first developed it, with three subsections covering "the mechanism isn't real," "the citation isn't right," and "the mechanism is real, but the application is different." The Session 10 methodology page refined the taxonomy's public framing to define protocol failure specifically as a *validator-side* limit (a question the data couldn't answer) rather than a *content-side* application mismatch.

Three options were considered for resolution. The committed choice (Option C in the integration discussion) was to:

1. **Promote chives-and-apple-scab to a clean mechanism-failure worked example.** The methodology page's "On the absence of a mechanism-failure worked example" section was removed; in its place the page now documents the chives-and-apple-scab composite-claim case as the mechanism-failure worked example. The methodology page had previously asserted the absence of a clean mechanism-failure example because Session 10 considered only the planting-date surface; Phase 4.2's companion-claim verification surface had in fact already produced one. Revision 3 corrects this gap.

2. **Reframe the chives-apple-scab case as a composite claim.** Initial drafting of the worked example used the simplified "chives prevent apple scab" framing from the companion section's failure-mode-1 description. Cross-checking against the deployed dataset surfaced that the actual claim in `crops_data_final.json` is "Repel aphids and scab fungus" -- a composite claim where the aphid-repellent component is mechanism-real (Durenne and Gosset 2018; Mississippi State; USU Extension) and the scab-repellent component is mechanism-fabricated. The dataset's response was to downgrade from `extension_backed` to `mechanistic` at medium confidence (not "traditional," which the simplified draft had said), with reason text that names both components honestly. The worked example in the page now reflects the composite-claim reality, which is more nuanced than the simplified version and teaches the reader more about how the verification protocol handles bundled claims.

3. **Reframe marigold-nematode and nasturtium-aphid as extension-backed/medium examples rather than as a third-failure-mode worked example.** The companion section originally presented these as "the mechanism is real, but the application is different" -- a hybrid pattern the Phase 4.2 ROADMAP entry called "mechanism-protocol mismatch." This pattern does not fit the methodology page's three-mode taxonomy as defined: it is not a mechanism failure (the mechanism is real), not a citation failure (the citations check out), and not a protocol failure in the validator-limit sense. Rather than broaden "protocol failure" to a bigger tent (which would muddy the validator-focused definition that the existing zones-9/10 example depends on), the merge keeps both worked examples in the companion section under a new heading "Extension-backed at medium confidence: when the application differs from the protocol," and explicitly notes that this pattern does not fit the failure-mode taxonomy. This preserves the substance of what the companion section teaches without conflating two different meanings of "protocol."

4. **Reframe the PM 1902 / Cornell IPM / UC IPM citation cases to acknowledge their actual provenance.** The Session 10 methodology page presented PM 1902 as "during a recent audit" without naming Phase 4.2 as the audit, and didn't mention the Cornell IPM and UC IPM cases that came out of the same verification cycle. Revision 3 reframes citation failure example #1 as "the Phase 4.2 fabricated-citation cluster," covering all three fabrications honestly as a single audit's cluster.

### Structural changes

- **Placement.** The companion section sits between Tier 3 and "What we cannot tell you from this data," giving the page a natural reading order: data we have for planting dates (three tiers), data we have for companion pairings (companion claims), data we structurally cannot have (cannot-tell-you), how we audit ourselves (failure-mode taxonomy), what this means for the user (closing).
- **Gardener summary box.** Extended by one sentence covering companion claims, so a gardener arriving for that content gets oriented in the box.
- **Three-tier intro.** The mechanism-failure parenthetical was broadened from "wrong threshold or wrong sustain logic" to "the encoded biological fact is wrong," to cover both planting-date threshold errors and companion-claim biology errors.
- **Failure-mode taxonomy section.** Substantially rewritten. New mechanism-failure worked example (chives-apple-scab composite claim). Citation failure #1 reframed as the Phase 4.2 cluster. Citation failure #2 (Palecki) and protocol failure (zones 9/10) unchanged. New closing subsection "What the three examples together demonstrate" that names the structural pattern: the audit only catches what the audit explicitly asks about. The "On the absence of a mechanism-failure worked example" section is removed because its premise no longer holds.

### Page metrics post-Revision-3

- Word count: ~9,561 (up from ~6,500 after Revision 2)
- Sections: gardener box, three tiers, **companion claims (new)**, cannot-tell-you, failure-mode taxonomy (rewritten), closing
- Honest disclosure items (Tier 1): 9 (unchanged)
- Worked examples (failure-mode taxonomy): 4 (mechanism, citation cluster, citation Palecki, protocol)
- Em-dash check: clean (zero em or en dashes)
- Version stamp: updated to "Methodology version 1.1, prepared 2026-04-27, reflecting Phase 1.1 dataset state and Phase 4.2 companion-claim methodology."

The word count is now substantially over the original Session 10 prompt's 4,000-word ceiling. Tightening below the ceiling at this point would require cutting either honest disclosures, the companion-claim provenance story, or the gardener-friendly framing -- all of which are the wrong direction. The page is intended to be thorough and reviewable. A separate "summary" version, if one is needed for App Store-adjacent surfaces, can be derived from the gardener summary box.

### Items flagged for Trevor

- The `methodology_page_companions_section_edited.md` filename in project knowledge differs from the `methodology_page_companions_section.md` filename referenced in the ROADMAP document index. Per the integration session prompt's Item 2, the source companion section should remain in project knowledge as historical reference. Decision needed: rename the file in project knowledge to match the document index, update the document index to match the actual filename, or leave both as-is and note the discrepancy.
- The chives-and-apple-scab claim is also present on `pear-european` (European Pear) with identical provenance reason text. The methodology page worked example mentions this in passing; the dataset state is correct (downgraded on both crops). No action needed, but worth noting if Audit 5 or a future Phase 3 zone-entry sweep touches pome-fruit pages.
- The deployed dataset's chives-apple provenance has `verified_against_sources: false`. The reason text is internally rigorous (cites Durenne and Gosset 2018, MSU, USU Extension, UMN, Cornell apple IPM), but the verified_against_sources flag is false. This may be a labeling-vs-verification distinction worth surfacing in Audit 5 -- the reason text reads as if it has been verified, but the flag says it hasn't. Either the flag is wrong or the reason text overstates its evidence base.

## Revision 2 -- 2026-04-27, structural additions

Three structural additions Trevor commissioned after reviewing the post-audit revision (Revision 1). All three were items the audit's methodology-of-methodology section raised as structural questions; Revision 1 deferred them as not-audit-corrections. With the audit-driven revisions absorbed and the page in publication-ready state, the structural additions were applied as a final polish before publication.

### Additions

1. **Version stamp / date.** Single italicized line below the H1 title: "Methodology version 1.0, prepared 2026-04-27, reflecting Phase 1.1 dataset state." Establishes a stable reference for the page's content state without depending on web-copy conversion to add it.

2. **Gardener summary box.** ~235-word blockquote at the top of the page, before the technical introduction. Plain-language orientation for a reader who didn't ask for a methodology page and arrives because the app linked here. Explains what the dates are, where each kind comes from in one phrase each, what they're not (microclimate-custom), and what to do when local experience differs (trust eyes and a soil thermometer over the calendar). Explicit permission line at the end ("You are not required to read it") respects the reader's time. Renders as a markdown blockquote to set it visually apart from the technical content.

3. **"What we cannot tell you from this data" section.** Inserted between the three tier sections and the failure-mode taxonomy. Names five categories of question the dataset structurally cannot answer:
    - Your microclimate (within-zone variation)
    - This year's specific weather (climatological vs. forecast)
    - Your specific soil and exposure (mulch, raised beds, soil texture)
    - Variety-specific differences (crop-level vs. variety-level rules)
    - Beyond the 10-day forecast horizon (a Tier 2 limit consolidated here)

   The section closes with a "Where this is headed" sub-section that connects the addressable limits (primarily microclimate) to the v1.5/v2.0 probe-integration roadmap, framed honestly as "the dataset can't tell you because it isn't measuring at your location, and a soil probe is the path to fixing that." The closing line -- "plant is one input; the gardener is the other" -- pairs with the gardener-summary-box's framing.

### Page metrics post-Revision-2

- Word count: ~6,500 (up from ~5,550 after Revision 1, ~4,250 in initial draft)
- Sections: gardener box, three tiers, cannot-tell-you, failure-mode taxonomy, closing
- Honest disclosure items (Tier 1): 9
- Worked examples (failure-mode taxonomy): 3 (now correctly classified by mode)
- Em-dash check: clean

The word count is now well over the original Session 10 prompt's 4,000-word ceiling. Both audit-driven revisions and structural additions pulled the page longer, by design. Tightening below the original ceiling would require cutting either honest disclosures or the gardener-friendly framing, both of which are the wrong direction.

## Revision 1 -- 2026-04-27, post-audit

Applied seven prioritized revisions from the methodology page adversarial audit (`methodology_audit_2026-04-27.md`). All revisions were textual; no new validator runs, no new citations, no rule-level dataset modifications.

### Revisions applied

1. **Failure-mode taxonomy repaired.** The original page presented PM 1902 as a "mechanism-and-citation failure" worked example, which the audit correctly identified as a citation-failure reframed to fill the third taxonomy slot. The taxonomy section was rewritten to honestly classify both PM 1902 and the Palecki correction as citation failures (the framing Session 8's own findings used), retain zones 9/10 as the protocol-failure example, and add a section "On the absence of a mechanism-failure worked example" that names the absence directly and explains why it matters. The page now claims credibility on what the audit machinery actually demonstrates rather than on a balanced-by-construction taxonomy.

2. **Depth claim corrected.** The page previously claimed the validator works against "5 cm or 10 cm" depths. The actual deployed validator uses 5 cm for 390 rules and 2.5 cm (a USCRN 5 cm proxy) for 24 cucumber rules. No rule uses 10 cm. The phrasing was corrected, and a new disclosure (#8) was added describing the cucumber 2.5 cm proxy explicitly. This disclosure was specifically flagged in Session 6b for the methodology page and was missing from the original draft.

3. **Year range corrected.** The page previously implied USCRN observations across "24 years." The deployed `years_covered` field is 2010-2025 (16 years). The validation pass starts at 2010 because USCRN soil-probe deployment completed in 2011. A new disclosure (#9) was added explaining the 16-year window and why it was chosen over the network's full 2002-onward record.

4. **Hold-out cross-check rewritten.** The original framing characterized held-out medians as running "a few days later" than main medians; the actual zone-by-zone drift is mixed in direction and substantially larger in magnitude in zone 9 (zone 5 -3 days; zone 7 +6 to +17 days; zone 9 +22 to +31 days). The disclosure now states (a) most held-out passes return low-confidence verdicts because n=1 station per zone falls below the 30-station-year floor; (b) where actionable verdicts emerged on both sides, they agreed; (c) the actual drift pattern is mixed and larger in zone 9, consistent with sampling variance from station selection.

5. **Zone scope stated.** A one-sentence statement was added near the top: "This methodology applies to plant's coverage of USDA hardiness zones 3 through 11. Tier 1 currently covers zones 3 through 10; Tiers 2 and 3 cover any zone the user is in."

6. **`uncovered` definition split into two sub-cases.** The verdict-labels section now distinguishes the **thin-coverage** sub-case (fewer than two stations or fewer than 10 station-years) from the **no-signal** sub-case (climate physics doesn't produce a soil-warmup crossing). The 22 deployed `uncovered` verdicts are all the no-signal sub-case. The protocol-failure worked example was updated to use the named sub-case.

7. **Catalog heterogeneity disclosure tightened.** Disclosure #5 now correctly says "three crops, nine deployed rules" (was: "three rules"), and acknowledges that the underlying catalog has one anchor where the per-zone attribution required a non-standard shape, and that the integration code carries a small special-case handler to read it. The original disclosure presented Path A's structure as cleanly handling heterogeneity without surfacing that structural exception.

### Additional minor revisions applied at the same pass

- Tier 2 forecast-skill non-claim section gained a sentence noting that any forecast service has miss rates and the user is the final check before acting on a notification (audit minor #11).
- The 38% non-within-range arithmetic now explicitly notes that the named clusters account for 36.5% and the remaining ~1.5% (cucumber borderline cases) is documented in disclosure #8 (audit minor #13).
- Hold-out station count now stated exactly: "11 of the network's 113 USCRN stations" (audit minor #9).

### Items deferred from Revision 1 (now applied in Revision 2)

- Methodology-page version stamp / "last updated" line.
- "What we cannot tell you from this data" section.
- Top-of-page gardener summary box.

All three were applied in Revision 2 once Trevor confirmed they should land before publication.

### Page metrics post-Revision-1

- Word count: ~5,550 (up from ~4,250)
- Honest disclosure items: 9 (up from 7)
- Worked examples in failure-mode taxonomy: 3 (now correctly labeled by mode)
- Em-dash check: clean

## Revision 0 -- 2026-04-27, initial Session 10 draft

Initial draft produced during Session 10. Three-tier framing; seven honest disclosures; failure-mode taxonomy with three worked examples (one per mode). ~4,250 words. Not published; sent to adversarial audit.
