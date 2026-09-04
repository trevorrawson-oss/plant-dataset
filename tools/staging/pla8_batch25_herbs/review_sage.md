# PLA-8 BATCH 25 -- INDEPENDENT SOURCE-TRUTH REVIEW: **sage**

Reviewer: independent pass, 2026-09-04. I did not author `out_sage.json` and I have not defended it.
Canonical read-only; no data file changed.

**Scope reviewed:** 7 entries, 27 rungs, 43 declared `field_corrections`, 6 declared refusals,
7 `unreachable_claims`.

**Method note (stated so it can be discounted):** the sandbox blocks `curl`, so every document read
below is a live WebFetch of the URL in the entry's `anchoring_urls`, prompted for verbatim sentences.
The three load-bearing pages (UC IPM 7405, 7406, 7493) were fetched twice each under different
prompts, and one claim was additionally cross-checked by web search. Sentences quoted below are what
came back verbatim on those reads.

Machine checks run locally: the mollusk/insect/mite/fungal legality of all 27 rungs by IMPORTING
`tools/control_ladder_gate.py`'s `TYPE_TARGETS` and `TIER_RANK` (never retyped), tier monotonicity,
`validate_out.py sage` (**OK: sage validates. 4 pests + 3 diseases, 27 rungs**), source-key admission
against the canonical `source_catalog`, and a consumer-copy sweep of all 97 authored strings
(no em dashes, no en dashes, every temperature renders as `NN°F`, no mid-sentence capital "Plant",
no British spellings).

---

## THE SIX ADJUDICATIONS ASKED FOR, ANSWERED FIRST

**1. Powdery mildew rewrite -- CORRECT, and the refutation is verbatim on both pages.**
UC IPM 7493: *"Although relative humidity requirements for germination vary, all powdery mildew
species can germinate and infect without water on the plant's surface."*; *"Water on plant surfaces
for extended periods inhibits spore germination and kills the spores of most powdery mildew fungi."*;
*"Overhead sprinkling can reduce the spread of powdery mildew because it washes spores off the
plant."*; *"Moderate temperatures (60° to 80°F) and shade encourage the disease."* 7406 carries the
matching pair: *"all powdery mildew species can germinate and infect in the absence of free water"*
and *"Overhead sprinkling may help reduce powdery mildew because spores are washed off the plant.
However, overhead sprinklers are not usually recommended as a control method in vegetables because
their use may contribute to other pest problems."* The rewritten strings say exactly this.
**"Water at the base" is now carried by root rot and not by mildew, in every register**: I checked
each field. `prevention_seasoned`: "that is protection against root and stem rot, the serious disease
on this plant, and it does nothing against mildew"; `prevention_beginner`: "that is to protect it from
root rot, not from mildew"; `organic_treatment_beginner`: "Keeping the leaves dry does not help against
this one"; `organic_treatment_seasoned`: "water on the foliage suppresses this particular fungus rather
than spreading it". The two entries no longer share a rationale. **Confirmed.**
**95°F: verified and correctly scoped.** 7493 carries *"temperatures above 95°F may suppress growth of
the fungus."* 7406 does **not**: it says *"Spores and fungal growth are sensitive to extreme heat
(above 90°F) and direct sunlight."* Admitting `uc_ipm_pn7493` for that figure is right.
**`garden_sanitation` dormant-season anchor: the sentence is real but it is NOT unique to 7493.**
7493 carries *"Prune out small infestations and remove infected buds during the dormant season."* --
and so does 7406, returned verbatim on two separate fetches of pn7406, and a web search finds the
same sentence across UC IPM's ornamentals, vegetables and fruits-and-berries notes. So the author's
scoping note ("both of which 7493 uniquely carries") is **half wrong**: only the 95°F figure is
7493-unique. The scoping *decision* (7406 general, 7493 for the two specific claims) still stands and
is the right shape; the justification overstates by one claim. **See FIX-5**: the bigger problem with
that rung is not which document it came from, it is that "dormant season" contradicts sage's own
sourced prune window.

**2. Verticillium wilt -- "improve drainage" is GONE from all four registers. Verified field by field.**
Canonical carried it in exactly four places: `organic_treatment_seasoned` ("Improve drainage and
airflow"), `organic_treatment_beginner` ("Better drainage and airflow help"), `prevention_seasoned`
("Plant in well-drained soil"), `prevention_beginner` ("Use well-drained soil"). All four are
rewritten and none of the replacements offers drainage; two of them now say explicitly that drainage
is not the lever. UMD verbatim: *"Fusarium and Verticillium are favored by droughty conditions"*, and
that page discusses drainage only in relation to *Phytophthora*. UC IPM's Verticillium page says
nothing at all about irrigation, drought or drainage (I asked; ABSENT). **Severity `low` -> `medium`
matches the prose**: the entry now says "expect a compromised bed to stay compromised for years",
"There is no cure", "the site, not the plant, carries this forward", and it also carries the honest
mitigation (*uwi_hort*: *"S. officinalis tends to be a short-lived perennial and is often best
replaced every few years."*), which is the strongest argument for `low`. Both sides are on the record;
`medium` is defensible.
**The binomial refusal was RIGHT.** UC IPM names *V. dahliae* and *V. albo-atrum* for the disease, but
its host list is *"dahlia, gerbera, marigold, peony, snapdragon, and vinca"* -- salvia ABSENT. UMD names
*Salvia* but no binomial. The only sage-scoped attribution is Ryan (1966), a 403. "A soil-borne
*Verticillium* fungus" carries exactly what the disease name already carries and costs the reader
nothing. Correct call. One caution on the *positive* claim it replaced drainage with: see FIX-8.

**3. Leafhoppers -- the symptom hole is FIXED, and zero vector content leaked in. Verified.**
The old strings named the insect, not the damage ("Occasional small hopping insects on the foliage").
The new ones name it: "Coarse pale speckling, or stippling, on the upper surface of the leaves, with
whitish cast skins and the insects themselves on the undersides." UC IPM: *"Leafhopper feeding causes
leaves to develop pale specks (stippling)."*, *"As nymphs molt into the next (larger) instar, they
leave whitish cast skins on the underside of foliage."* RHS: *"Coarse pale spotting on upper leaf
surface. Leafhoppers may be seen on the underside of leaves"*.
I searched all 8 leafhopper strings and all 4 rung notes for vector content: no "virus", "yellows",
"curly", "phytoplasma", "transmit", "spread disease". **Zero.** The decisive sentence is in the
entry's own UF/IFAS anchor: *"The Ligurian leafhopper specifically has not been shown to transmit any
plant pathogens."* And UC IPM's vector host lists exclude sage: curly top *"damages many vegetables,
including beans, beets, melons, potatoes, peppers, and tomatoes"*; aster yellows is spread by
*Macrosteles quadrilineatus*. Minting `sage-leafhoppers` rather than reusing cilantro's `leafhoppers`
is correct and load-bearing. One FIX on this entry (FIX-3), and it is a cross-entry contamination.

**4. Slugs -- the ladder is legal, but the struck claim survives in two fields the pass did not touch.**
Computed from the gate's own table, the `mollusk` pool is exactly 8: `crop_rotation`,
`floating_row_cover`, `garden_sanitation`, `handpick`, `iron_phosphate_slug_bait`,
`resistant_varieties`, `slug_traps_barriers`, `water_at_the_base`. The ladder uses five of them.
`airflow_spacing` is absent, and the airflow claim is gone from the corrected `prevention_seasoned`.
The corrected prose is slug-only ("Slugs feeding at night and on overcast days"), which is right:
both sage-scoped documents say "slugs" and neither says "snails".
**But** `organic_treatment_seasoned` ("...use traps or iron-phosphate bait **around vulnerable
seedlings**") and `organic_treatment_beginner` ("...**near young plants**") were left untouched, and
they carry the very young-plant scoping the pass struck from both symptom strings as unanchored. And
the untouched `prevention_beginner` still reads "Give sage a sunny, well-drained, **open spot**",
which is the airflow framing surviving in the beginner register after the seasoned register dropped
it. **FIX-4.**

**5. Spittlebugs -- no species identity asserted. Verified.**
The corrected `cause_seasoned` says "Sucking insects in the family Cercopidae" and nothing narrower;
no rung note names a species. RHS's host list is *"Many plants, including chrysanthemum, dahlia,
fuchsia, lavender, rosemary, rose and willow"* -- sage ABSENT, confirmed on a direct read, so the
inference leg the record flagged is real and the author did not walk across it. UC IPM's page never
mentions sage either. The family-level attribution is exactly what a read document gives:
*"These sucking insects (family Cercopidae) can at least occasionally be found on almost any plant."*
The no-chemical cap is honored: the ladder is cultural, cultural, physical.

**6. The sulfur refusal on spider mites -- RIGHT CALL, WRONG WARRANT. This is the finding I would
most want the orchestrator to see.**
The decision is right. The stated grounds are not, and they misread the very document they cite.
The author wrote: *"NO document in my report recommends sulfur for mites on sage: UC IPM Pest Note
7405's treatment sentence names 'insecticidal soap or insecticidal oil' and nothing else."*
Pest Note 7405 **does** carry a sulfur paragraph, returned verbatim on a direct read and corroborated
by web search:
> "Sulfur sprays can be used on some vegetables, fruit trees, and ornamentals. This product will burn
> cucurbits and other plants in some cases. Don't use sulfur unless it has been shown to be safe for
> that plant in your locality. Use liquid products such as sulfur and potash soap combinations
> (e.g., Safer Brand 3-in-1 Garden Spray) rather than sulfur dusts, which drift easily and can be
> breathed in. Don't use sulfur if temperatures exceed 90°F, and don't apply sulfur within 30 days of
> an oil spray. Sulfur is a skin irritant and eye and respiratory hazard, so always wear appropriate
> protective clothing."
The second stated ground is also mis-attributed: the author says sulfur "must not be applied ... to
drought-stressed plants". In 7405 the water-stress caution attaches to soaps and oils --
*"Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F"* -- not to sulfur.
7493 does the same: *"do not apply oils when temperatures are above 90°F or on water-stressed plants."*
**The correct warrant is inside the paragraph the author said did not exist**: *"Don't use sulfur unless
it has been shown to be safe for that plant in your locality"* (no read document shows it safe on
*Salvia officinalis*, and 7405 warns it burns some plants), plus *"Don't use sulfur if temperatures
exceed 90°F"* against a pest whose own driver is *"hot, dusty conditions"*. Same verdict, honest
reasons. Rewrite the refusal text; do not add the rung.

---

## Spittlebugs (`spittlebugs`, insect, low) -- 3 rungs, 4 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `weed_host_control` | **HOLDS** | uc_ipm verbatim, both halves: *"Cut spittlebug-infested weeds in the spring before the insects mature and spread."* and *"Spittlebugs are more likely to become abundant on woody plants when they migrate from nearby herbaceous hosts."* |
| 2 | `garden_sanitation` | **SYNTHESIS** (declared, honestly hedged) | the FACT holds verbatim: *"Overwintering occurs as tiny eggs on or in stems or needles."* The PRACTICE (dormant stem removal) is an inferred step no document recommends for spittlebugs. The note hedges it correctly: "Expect it to trim numbers, not to prevent foam, since adults also arrive from outside the bed." Acceptable; see FIX-5 on the timing word. |
| 3 | `water_spray` | **HOLDS** | uc_ipm verbatim: *"Ignore spittlebugs or wash nymphs off with a forceful stream of water."* The "cosmetic housekeeping" framing is the same document's *"may be annoying, but they do not seriously harm established woody plants in landscapes."* |

Corrections: all 4 **HOLD** and all 4 were **needed**. "Numbers are usually low" was refuted by
*"occasionally abundant"*; "vigorous sage shrugs off minor pests" was the unsourced-mechanism class
and is replaced by the weed-host lever the source actually publishes. `uwi_hort`'s *"Sage has few pests
when grown in well-drained soil."* is used as a general statement about the crop, not as a spittlebug
deterrent, which is the correct handling.

**Scope note (not a FIX):** both UC IPM sentences the entry leans on are scoped to *woody plants* --
"become abundant on woody plants", "do not seriously harm established woody plants in landscapes".
Sage is a woody subshrub (`clemson_hgic`: *"Sage is a small evergreen shrub..."*), so the transfer is
defensible, but the severity and the "cosmetic" framing both rest on it.

**Untouched-field flag (FIX-12, low):** `symptoms_seasoned` / `symptoms_beginner` still say the foam
appears "in late spring". No US document read publishes a window; RHS's *"May-July"* is UK and the
author correctly refused to import it. The author declares this out of scope as cert-era prose, which
is a legitimate declare-what-you-change position -- but the entry now carries `sources` and
`anchoring_urls`, which reads as "this entry is anchored", and one of its claims is not.

---

## Spider mites (`spider-mites`, mite, low) -- 4 rungs, 5 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `even_watering` | **HOLDS** | *"Plants under water stress also are highly susceptible."* The rung is legal only because sage types `mite`, which is correct. The "steady is not soggy" cross-reference to root and stem rot is the right coherence move on this crop. |
| 2 | `water_spray` | **HOLDS**, with one **UNSUPPORTED** interval | *"In gardens and on small fruit trees, regular, forceful spraying of plants with water often will reduce spider mite numbers adequately. Be sure to get good coverage, especially on the undersides of leaves."* The dust half holds: *"first found on trees or plants adjacent to dusty roadways or at margins of gardens."* **"every few days" is in no document on this entry**: 7405 says only "regular" (I asked for an interval; ABSENT), Clemson says *"regularly during periods of drought"*. It is inherited from the certified prose, so it is not new, but it is now repeated in a new rung note. FIX-11. |
| 3 | `insecticidal_soap` | **HOLDS**, with a **FIX for omission** | *"If a treatment for mites is necessary, use selective materials, preferably insecticidal soap or insecticidal oil."*, *"Oils and soaps must contact mites to kill them, so excellent coverage, especially on the undersides of leaves, is essential."*, *"Be sure mites are present before you treat."* All three are in the note. **Missing: the caution that governs it.** FIX-2. |
| 4 | `horticultural_oil` | **WRONG (a number)** | FIX-1. |

**FIX-1 (WRONG, the most consequential rung defect on this crop).**
Text: *"Oil behaves like soap, contact-only with coverage governing the result. Keep it off
drought-stressed plants and away from temperatures above 90°F, and leave two weeks between an oil
spray and any sulfur."*
The first two clauses hold verbatim (*"Don't use soaps or oils on water-stressed plants or when
temperatures exceed 90°F"*). **"two weeks" is wrong for this entry.** The sentence that settles it, in
this entry's own anchoring document, `ucanr_ext_spider_mites` (pn7405):
> "Don't use sulfur if temperatures exceed 90°F, and don't apply sulfur within 30 days of an oil spray."
Two weeks is the *powdery mildew* notes' figure (7493/7406: *"do not apply it within 2 weeks of an oil
spray"*), imported onto a mite rung, and it is the **less protective** of the two. Compounding it: the
mite ladder has no sulfur rung at all (the author refused it), so the clause cross-references a rung
that does not exist. Either correct it to 30 days per 7405, or drop the sulfur clause from this rung.

**FIX-2 (omission, safety-of-advice).** The `insecticidal_soap` rung carries no temperature or
water-stress caution, and neither does the catalog's `insecticidal_soap` entry (its `cons` are about
contact-only action and pest range). 7405 applies the caution to soaps as well as oils:
*"Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F."* This ladder
tells a reader to reach for soap in exactly the conditions the source forbids: the entry's own
`even_watering` rung and both symptom strings tie outbreaks to heat waves and drought-stressed plants.
The caution needs to ride on the soap rung, not only on the oil rung below it.

Corrections: all 5 **HOLD** and all 5 were **needed** ("indoor plants" and "still air" have no anchor
for sage; the sourced drivers are heat, dust and water stress, and *umd_ext*'s *"tiny, eight-legged
non-insects (related to spiders)"* is a genuine consumer gain).
**One imprecise `why` (not a data defect):** the prevention corrections justify dropping "Maintain good
airflow" with "no read document links airflow to spider mites". `ncsu_ext`, the sage-scoped document,
says *"Providing well-drained soil and good air circulation will reduce the possibility of pests and
foliar diseases."* -- a generic pest claim that does touch mites. The change is still an improvement
(it swaps a vague lever for the sourced ones); the stated absence is just not exact.

---

## Slugs and snails (`slugs-and-snails`, mollusk, low) -- 5 rungs, 5 corrections

Legality computed by importing the gate's table: all 5 methods are in the 8-wide mollusk pool;
tier ranks `[0, 0, 1, 1, 3]`, monotonic.

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `water_at_the_base` | **HOLDS** | *"Switching from sprinkler irrigation to drip irrigation will reduce humidity and moist surfaces, making the habitat less favorable for these pests."* The morning instruction also holds: *"Reduce moisture by switching to drip irrigation or by running sprinklers in the morning rather than later in the day."* and *"Irrigating near sunrise will reduce the amount of time that foliage and ground are moist."* |
| 2 | `garden_sanitation` | **HOLDS** | *"Boards, stones, debris, weedy areas around tree trunks, leafy branches growing close to the ground, and dense ground covers, such as ivy, are ideal sheltering spots."*; *"Snails and slugs are most active at night and on cloudy or foggy days."*; *"On sunny days, they seek hiding places out of the heat and bright light."* The note's "clear the shelter first" ordering is the source's own logic. |
| 3 | `handpick` | **HOLDS**, two **SYNTHESIS** clauses | *"After dark, search them out using a flashlight, pick them up ... and dispose of them in the trash."* and *"At first you should look for snails and slugs daily"* / *"After the population has noticeably declined, weekly hand-picking can be sufficient."* support the repeat regimen. "Early morning works too" is an inference (7427's morning sentences are about irrigation; the day-hiding sentence makes it sound). "A few evenings of this clears a small planting" slightly outruns *"can be very effective if done thoroughly on a regular basis"*. |
| 4 | `slug_traps_barriers` | **HOLDS**, one omission | verbatim: *"boards ... raised off the ground by 1-inch runners"*, *"Scrape off the accumulated snails and slugs daily and destroy them."*, *"copper reacts with the slime that snails and slugs secrete, causing a disruption in their nervous system"*. FIX-9: the note says a copper band is "worth its cost" without UC IPM's expiry -- *"Copper foil or tape wrapped around planting boxes, headers, or trunks will repel snails until it becomes tarnished."* The catalog method carries the caveat, so this is minor. |
| 5 | `iron_phosphate_slug_bait` | **HOLDS**, correctly hedged | *"Iron phosphate baits have the advantage of being safer for use around children, domestic animals, birds, fish, and other wildlife."* -> "the gentler choice", comparative not absolute. *"Metaldehyde baits are particularly poisonous to dogs and cats"* -> verbatim. Placement holds: *"Sprinkle them on the soil in areas that snails and slugs regularly frequent, near but not on plants that are attractive to the pests."* |

Corrections: all 5 **HOLD**. The airflow claim is genuinely gone from `prevention_seasoned` and the
irrigation-method lever the source publishes is in.

**FIX-4 (the real slug defect: an untouched field carries the struck claim).**
The pass removed "mainly on young or newly set plants" / "mostly on young plants" from both symptom
strings, on the ground that no sage-scoped document says it. Two fields it did not touch still say it:
* `organic_treatment_seasoned`: "...and use traps or iron-phosphate bait **around vulnerable seedlings**."
* `organic_treatment_beginner`: "...and use slug traps or an iron-phosphate bait ... **near young plants**."
Same unanchored scoping, still live, and now inconsistent with the entry's own symptoms. Related, lower:
the untouched `prevention_beginner` ("a sunny, well-drained, **open spot**") keeps the airflow framing in
the beginner register that the seasoned register just dropped.

---

## Leafhoppers (`sage-leafhoppers`, insect, low) -- 4 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `garden_sanitation` | **UNSUPPORTED** on one clause | FIX-3. |
| 2 | `yellow_sticky_traps` | **SYNTHESIS** | the practice is real: uf_ifas *"In Poland, herb producers reportedly vacuum plants and employ yellow sticky traps to reduce the abundance of Ligurian leafhopper"*. The monitoring framing is carried by the catalog method's own T1-sourced entry (*"Gives an early warning of a building population"*), so it is not floating. The decision rule -- "rising catches through the season are the signal to act, a card that stays clean is the signal to leave it alone" -- is authored, not published; UC IPM's leafhopper page has no monitoring or threshold content at all (I asked; ABSENT). Also note the only species-specific warrant is a second-hand report about commercial herb production in Poland, and the beginner note states it as plain fact. |
| 3 | `beneficial_predators` | **HOLDS**, one **FIT** note | rhs verbatim: *"Encourage predators and other natural enemies of leafhoppers, in the garden, such as birds, ladybirds, wasps and ground beetles"* (correctly Americanized to "ladybugs"). "Avoid the broad-spectrum sprays that would remove them" is carried by the catalog method's own cons (*"Broad-spectrum sprays and ant activity undercut them"*). FIT: UC IPM, cited on this same entry, publishes a US list -- *"assassin bugs, brown lacewings, damsel bugs, green lacewings, lady beetles, minute pirate bugs, and spiders"* -- and the note uses the UK one instead. Not wrong; a US list was available in a document already on the entry. |
| 4 | `insecticidal_soap` | **HOLDS** | uc_ipm: *"green shoots and the underside of leaves can be thoroughly sprayed with horticultural oil, insecticidal soap, or neem oil"*. The escalation trigger is that page's own *"Leaves and shoot tips fed upon by an abundance of leafhoppers may turn yellow then brown and curl and die."* |

**FIX-3 (UNSUPPORTED, and it is a cross-entry contamination).**
Text, in three places: `garden_sanitation.note_seasoned` "Most of the population overwinters as eggs
in **leaf and stem** tissue"; `note_beginner` "The eggs spend winter in last year's **leaves and
stems**"; `prevention_seasoned` "before the eggs that overwintered in **leaf and stem** tissue hatch"
(and `prevention_beginner` "the old **leaves and stems**").
Every document names **leaf tissue only**:
* uf_ifas EENY-750: *"Adult females oviposit (lay eggs) within the leaf tissues of host plants"* and *"In Italy, it is thought that most of the population overwinters as eggs."*
* VCE ENTO-412NP (read but not cited, catalog-blocked): *"Eggs that overwintered in leaf tissue hatch when warming spring temperatures reach 68° F."*
* rhs: *"These leafhoppers overwinter as eggs on host plants"* -- site unnamed.
No document says stems. **The stem-egg fact is the spittlebug entry's, on this same crop**: uc_ipm,
*"Overwintering occurs as tiny eggs on or in stems or needles."* Two entries authored in one pass, and
the neighbour's mechanism widened this one. Strike "and stem"/"and stems" in all four places; the rung
survives intact on leaves, and VCE independently supports the practice
(*"Manual removal of damaged leaves early in the infestation may temporarily reduce the Ligurian
leafhopper population by removing eggs before they hatch."*).

Corrections: all 8 **HOLD** and all 8 were **needed**. Three specifics worth recording because they
are the batch's own defect classes caught and fixed:
* removing "Rinse them off with water" was right -- I asked UC IPM's leafhopper page for any washing or hosing instruction and got **ABSENT**; it was a rung borrowed from the mite and spittlebug entries.
* removing "the plant has few serious pests" from inside a specific pest's *cause* field was right; it argued the reader out of acting.
* "They are on sage because sage is a favored host, not because a plant is weak" is the correct inversion of the old stress framing, and it is verbatim-backed: *"The Ligurian leafhopper (Eupteryx decemnotata) is a pest of mint, rosemary, sage, and other plants in the mint family (Lamiaceae)."*
The consumer-facing food-safety line ("Leaves carrying the speckling are still fine to use in the
kitchen") is rhs's *"Affected herbs are safe to eat."* -- a UK source, but a food-safety statement, not
UK product law, so the region rule does not bite.

---

## Root and stem rot (`root-and-stem-rots`, fungal, high) -- 3 rungs, 6 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `improve_drainage` | **HOLDS** | every figure checks out. pn74133: *"Raised beds can improve drainage in a vegetable garden."* and *"The mounds should be 8 to 10 inches high for annuals and up to 2 feet high with a gradual slope for trees and perennials."* D0094: *"when planting, place the root collar just at the soil surface."* and *"do not apply more than three inches of mulch around trees and shrubs"*. Neither document names sage; presence rides on `ncsu_ext` and `uwi_hort`, exactly as the author declares. |
| 2 | `garden_sanitation` | **HOLDS**, one **UNSUPPORTED** clause | D0094: *"After working with plants with root/crown rot, decontaminate tools and footwear by treating for at least 30 seconds with a 10% bleach solution or 70% alcohol"* (the note drops the "at least 30 seconds" contact time, which is the part that makes it work). clemson_hgic hot-topic: *"Some fungicides are effective, but only at suppressing these diseases, and they are often expensive"*. FIX-10: "throw it away with the household trash instead of composting it" is in no document read -- D0094 and the Clemson page are both ABSENT on removal and composting. |
| 3 | `crop_rotation` | **SYNTHESIS** (a widening) | the note says "The pathogens survive in soil for years to decades". D0094 scopes that to the water molds only: *"Water mold root rot organisms such as Pythium and Phytophtora produce thick-walled spores (called oospores) that can survive for long periods (years to decades) in soil."* The entry's umbrella also contains *Rhizoctonia* and *Fusarium*, for which no persistence figure was read. Small, and it argues in the safe direction. |

Corrections: all 6 **HOLD** and all 6 were **needed**.
* the unsourced ranking ("It is the main disease of sage") is out, replaced by `ncsu_ext` verbatim: *"It is intolerant of wet or poorly drained soils."*
* the "not cold" denial is out, and the winter-wet failure mode is in, correctly anchored to the sage-scoped document (rhs: *"In winter, excess rain can cause the roots to rot, so move plants in containers to a sheltered spot, such as in the rain-shadow of a wall."*). Note umd's *"Excessively wet, cold soil can cause Mediterranean herbs such as rosemary, thyme, and lavenders to die over the winter."* names rosemary, thyme and lavender, **not sage**, so rhs is doing the sage-scoped work here. Correctly ordered in the anchor list.
* "space plants for airflow" is out of both prevention registers, and the reason is exact: `ncsu_ext`'s air-circulation sentence is scoped to *"pests and foliar diseases"*, and a root rot is neither. Verified verbatim.
* the container rain-shadow rung is the single most actionable thing added to this crop.

---

## Powdery mildew (`powdery-mildew`, fungal, low) -- 4 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `airflow_spacing` | **HOLDS** | 7493: *"Moderate temperatures (60° to 80°F) and shade encourage the disease."* and *"Provide good air circulation by pruning excess foliage and properly spacing plants."*; 7406: *"Plant in sunny areas as much as possible, provide good air circulation, and avoid applying excess fertilizer."* |
| 2 | `balance_nitrogen` | **HOLDS**, and it is the best-authored rung on the crop | the mechanism is verbatim in both notes: *"Fertilize properly because too much nitrogen causes lush foliage and shade, providing conditions for fungal growth."* Worth flagging positively: the CATALOG method's own generic disease mechanism is leaf wetness ("A closed canopy holds leaf wetness and slows drying"), which is exactly the mechanism that does not apply to powdery mildew. The author diverged from the catalog toward the document. That is the right instinct and it is the opposite of the defect class this batch is hunting. |
| 3 | `garden_sanitation` | **HOLDS** on the claim, **FIT** on the timing | *"Prune out small infestations and remove infected buds during the dormant season."* is verbatim in 7493 (and in 7406). But see FIX-5: instructing a dormant-season tidy of sage contradicts the crop's own two sourced prune windows. |
| 4 | `sulfur` | **HOLDS**, one misattributed caution | 7493: *"Sulfur products have been used to manage powdery mildew for centuries but are effective only when applied before the disease appears."* and *"To avoid injuring plants, do not apply sulfur when the temperature is near or higher than 90°F, and do not apply it within 2 weeks of an oil spray."* Both directions of the 2-week interval are in 7493 (*"Never apply an oil within 2 weeks of a sulfur application"*), so "either side" is right. FIX-6: "and off drought-stressed foliage" is attached to sulfur; in 7493, 7406 and 7405 alike the water-stress caution belongs to OILS -- *"do not apply oils when temperatures are above 90°F or on water-stressed plants."* |

Corrections: all 8 **HOLD**. The two WRONG claims were genuinely wrong and are genuinely fixed
(quotes in the adjudication section above). Two small notes:
* `cause_seasoned` renders 7493's *"temperatures above 95°F may suppress growth of the fungus"* as "Heat above 95°F may suppress the fungus **outright**". "Outright" strengthens "suppress growth of". **STYLE**, one word.
* dropping "taints the flavor" was right: I asked 7493 directly about flavor or taste; **ABSENT**, and no other document read says it.

**FIX-7 (MISSING RUNG, and it contradicts the entry's own `unreachable_claims`).**
`out_sage.json` records: *"sulfur is the only legal soft-chemical rung and it is preventive only, which
leaves the ladder with no rung for an infection already established."* True of the soft-chemical tier,
but there is a legal **biological** rung the ladder skips. `biofungicide` is `applies_to:
["fungal_foliar"]`, tier `biological`, so it is legal here and would sit between the culturals and
sulfur with monotonicity preserved. It is anchored in the entry's own document, 7406:
> "Biological fungicides (such as Serenade) are commercially available beneficial microorganisms
> formulated into a product that, when sprayed on the plant, destroys fungal pathogens."
> "While this product functions to kill the powdery mildew organism and is nontoxic to people, pets,
> and beneficial insects, it has not proven to be as effective as the oils or sulfur in controlling
> this disease."
And the catalog's own `best_use` reads as if written for this crop: *"The first spots of a leaf fungus
on a crop you would rather not put sulfur on, applied early and repeated."* -- a culinary herb, on a
ladder whose only chemical rung is one 7405 warns can burn plants it has not been proven safe on.
This is not padding: the evidence for the rung exists and the ladder currently jumps three cultural
rungs straight to sulfur. Recommend adding it, with the "not as effective as the oils or sulfur"
honesty the source supplies.

---

## Verticillium wilt (`verticillium-wilt`, fungal, medium) -- 4 rungs, 7 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `certified_clean_stock` | **HOLDS** | uc_ipm: *"Plant only pathogen-free plants."* "Take cuttings from plants with no wilt history" is an inference, sound and cheap. |
| 2 | `crop_rotation` | **HOLDS**, verbatim on both halves | umd: *"These fungi remain in the soil for many years."* and *"Verticillium has a broader host range and so presents a more difficult problem in selecting 'non-susceptible' plants for rotation."* The note's "Treat the position as compromised for more than sage" is exactly that second sentence, and it is the honest version the old prose lacked. |
| 3 | `garden_sanitation` | **HOLDS**, with one **SYNTHESIS** and one loose anchor | uc_ipm: *"Sanitation and resistant plants are the primary strategies for managing Verticillium wilt."* The mechanism sentence ("nothing sprayed on a leaf reaches a fungus living inside the water-conducting tissue") is authored, not quoted; it is true and adjacent to umd's *"...cause stunting, wilt and death by plugging the vascular system"*. Note for a later pass: umd's explicit removal instruction, *"The best solution for bacterial wilts is to remove infected plants."*, is scoped to **bacterial** wilts, so it is not the anchor for this rung; the anchor is UC IPM's sanitation sentence. "Do not chip or compost" is unsourced. |
| 4 | `soil_solarization` | **HOLDS** | uc_ipm: *"Solarization can reduce Verticillium fungi in the upper few inches of soil."* The note correctly prefers the disease-specific "upper few inches" over the catalog method's generic "top 12 to 18 inches", and says plainly that it is a reduction, not an eradication. |

Corrections: 6 **HOLD**, 1 **SYNTHESIS**.
The symptom rewrite is verbatim-backed throughout (*"Woody plants are often affected first on one side
of the plant or only in scattered portions of the canopy."*; *"Leaves infected with Verticillium wilt and
turn yellow, first at the margins and between veins"*; umd's *"If you cut into the stem, the vascular
tissues show discoloration as tan, reddish, or dark streaking."*). Adding the cut-stem test is the
single most useful thing this pass gives the reader on sage: root rot and Verticillium look alike from
above and have opposite management.

**FIX-8 (SYNTHESIS, and I would not ship it as written).**
`cause_seasoned`: "it is favored by dry, droughty conditions **rather than by the wet soil that drives
root rot**", repeated in both treatment registers ("Drainage is not the lever here: this fungus is
favored by dry, droughty conditions").
The **removal** of drainage-as-a-control is unimpeachable and I endorse it. The **positive assertion**
is doing more work than its evidence:
* the whole load is carried by one clause in a document about wilt diseases of flowers: *"Fusarium and Verticillium are favored by droughty conditions"*. Not sage-scoped, not a sentence about *Salvia*.
* UC IPM's Verticillium page says nothing about moisture in either direction (ABSENT).
* no document says wet soil disfavors *Verticillium*; the contrast clause is the author's.
* the record itself flags a sage-scoped source that reportedly says the **opposite** (Ryan 1966: most severe on heavy clay and poorly drained areas), which nobody has been able to read (403).
Recommend keeping the negation ("drainage is not the lever against this one; that is the answer to root
rot") and either dropping the positive driver or attributing it ("extension guidance associates the
wilt fungi with droughty conditions"). A reader who acts on "favored by dry conditions" on a
Mediterranean subshrub may water more, which is the one thing sage's high-severity problem punishes.

---

## FIX-5 (CROSS-ENTRY): three prune timings for one operation, and two of them contradict sage's own sources

One crop, one annual cut, three instructions authored in one pass:
* Powdery mildew, `garden_sanitation.note_beginner`: "Do the same with affected buds when you tidy sage **in the dormant season**."
* Spittlebugs, `garden_sanitation.note_beginner`: "Take last year's dead stems off the plant **in late winter**."
* Leafhoppers, `garden_sanitation.note_beginner`: "Cut the old growth back **in early spring**."
Sage's own sourced prune window, from two documents already cited on this crop:
> `uwi_hort`: "Prune the plant in the spring and a few times through the growing season to encourage young shoots with a strong flavor and to prevent it from becoming leggy and twiggy."
> `rhs`: "Lightly prune established sage plants every year in mid- to late-spring to keep them compact and promote bushy growth of fresh new leaves."
"Dormant season" comes from 7493, which is a *woody ornamentals* note; transplanting it onto a
Mediterranean subshrub whose published prune window is spring is the region/scope class the brief warns
about. The spittlebug rung is the mildest of the three because it removes *dead* stems rather than
pruning live wood, and the leafhopper rung has a genuine mechanism for wanting to be early (eggs hatch
at spring warming). Recommend: harmonize all three to the sourced spring window, and where the timing
genuinely must be earlier, say what the trade is rather than inventing a second prune date.

---

## SUMMARY

### Counts

**Rungs (27), by primary grade**

| grade | count | which |
|---|---|---|
| **HOLDS** | 22 | spittlebugs 2/3, spider mites 3/4, slugs 5/5, leafhoppers 2/4, root rot 2/3, powdery mildew 4/4, verticillium 4/4 |
| **SYNTHESIS** | 3 | spittlebugs `garden_sanitation` (inferred practice, hedged); leafhoppers `yellow_sticky_traps` (authored decision rule); root rot `crop_rotation` (persistence widened past the water molds) |
| **UNSUPPORTED** | 1 | leafhoppers `garden_sanitation` ("leaf and stem tissue") |
| **WRONG** | 1 | spider mites `horticultural_oil` ("two weeks" where 7405 says 30 days) |
| **STYLE / FIT** | 0 as a primary grade | 3 as sub-findings (PM `garden_sanitation` timing; PM `sulfur` misattributed caution; leafhoppers `beneficial_predators` UK enemy list) |

**Corrections (43), by grade:** 42 **HOLD**, 1 **SYNTHESIS** (verticillium `cause_seasoned`).
**All 43 were needed.** Not one is a change for the sake of difference: each replaces a claim that is
either refuted by a document (powdery mildew's leaf-wetness pair, verticillium's drainage), unanchored
(the vigor and stress framings, "indoor plants", "still air", "wet mulch, crowding", the disease
ranking), or content-free (the leafhopper symptom strings). Two are arguable at the margin and I have
said which and why (spider mite airflow, slug young-plant scoping).

**Refusals (6):** 5 correct as stated. 1 -- the sulfur refusal -- correct in outcome, wrong in its
stated reading of 7405.
**Unreachable claims (7):** 6 accurate. 1 -- powdery mildew's -- overlooks a legal biological rung.
**Gate-shaped checks:** all 27 rungs legal for their problem type, all ladders monotonic softest-first,
`validate_out.py sage` OK, all 12 distinct source keys catalog-admitted at T1, consumer-copy sweep clean.

### FIX list, in the order I would fix them

| # | entry | what | severity |
|---|---|---|---|
| 1 | spider mites `horticultural_oil` | "two weeks" -> 30 days per 7405, or drop the sulfur clause (there is no sulfur rung) | **high** |
| 2 | spider mites `insecticidal_soap` | add 7405's "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F" | **high** |
| 3 | leafhoppers x4 fields | "leaf **and stem** tissue" -> leaf tissue; the stem-egg fact is the spittlebug entry's | **high** |
| 4 | slugs `organic_treatment_seasoned` + `_beginner` | still say "around vulnerable seedlings" / "near young plants", the scoping this pass struck from the symptoms | **high** |
| 5 | cross-entry | three prune timings; "dormant season" and "late winter" contradict sage's sourced spring window | medium |
| 6 | powdery mildew `sulfur` | "off drought-stressed foliage" belongs to oils, not sulfur, in all three UC documents | medium |
| 7 | powdery mildew ladder | missing `biofungicide` rung (legal, 7406-anchored, catalog best_use written for exactly this case) | medium |
| 8 | verticillium `cause_seasoned` + both treatments | soften or attribute "favored by dry, droughty conditions"; keep the negation | medium |
| 9 | slugs `slug_traps_barriers` | copper works "until it becomes tarnished"; the note implies it is permanent | low |
| 10 | root rot `garden_sanitation` | "not composting it" is unsourced; D0094's "at least 30 seconds" contact time dropped | low |
| 11 | spider mites `water_spray` | "every few days" is an interval no document on this entry publishes | low |
| 12 | spittlebugs symptoms (untouched) | "in late spring" is unanchored on an entry that now carries anchors | low |
| -- | the refusal text | rewrite the sulfur refusal onto the grounds 7405 actually gives | **high (text, not data)** |

### The single most important finding

**The sulfur refusal is right and its stated reason is false, and the same misreading of the same
paragraph produced the one WRONG rung on the crop.** The author refused sulfur on spider mites on the
ground that Pest Note 7405 "names insecticidal soap or insecticidal oil and nothing else"; 7405 in fact
carries a full sulfur paragraph, and that paragraph contains both the right reason to refuse
(*"Don't use sulfur unless it has been shown to be safe for that plant in your locality"*, against a
pest whose driver is *"hot, dusty conditions"*, with *"Don't use sulfur if temperatures exceed 90°F"*)
and the correct interval the ladder then got wrong (*"don't apply sulfur within 30 days of an oil
spray"*, written into the oil rung as "two weeks", the powdery mildew notes' number, the less
protective of the two). A refusal that reads as rigor was resting on an absence that is not there, and
the paragraph it did not read was also the one that would have corrected the rung it did write. This is
the `absence findings are document-scoped` failure at paragraph scale, inside a single document, and
it produced both a false-warrant refusal and a wrong number in the same entry.

Everything the brief singled out for checking -- the powdery mildew rewrite, the verticillium drainage
removal, the leafhopper symptom repair and vector isolation, the mollusk ladder legality, the
spittlebug species restraint -- **holds**. The defects are finer than those, which is the pattern
batch 24 established.

---

## RECORD-LEVEL FINDINGS (for a later pass, not to be fixed now)

1. **The record pass mis-reported UC IPM Pest Note 7405 the same way the author did.** The record
   calls `sulfur` "the classic soft-chemical miticide" and "a genuine miticide [that] belongs in the
   soft-chemical band" purely from the `applies_to` table, without noticing that 7405 itself has a
   sulfur paragraph with conditions attached. The document was quoted five times in the record and
   this paragraph was never surfaced. A `type`-legality argument was allowed to stand in for reading
   the treatment section.
2. **The record's 7427 hand-picking quote is not the page's sentence.** The record renders it
   "(hand-picking) search 'at night or in the early morning' with a flashlight". The page says
   *"After dark, search them out using a flashlight..."*; asked for every sentence containing
   "morning", the page returned only irrigation-timing sentences. The early-morning half is a
   paraphrase presented in quotation marks, and it propagated into the authored `handpick` note.
3. **The 7493-vs-7406 split is one claim narrower than the record and the author believe.**
   *"Prune out small infestations and remove infected buds during the dormant season."* is in 7406 as
   well as 7493 (two independent fetches of pn7406), and a search finds it across UC IPM's ornamentals,
   vegetables and fruits-and-berries notes. Only the 95°F figure is 7493-unique.
4. **Sage's crop-level vocabulary needs four keys before promote.** `sources_summary.primary` is
   `[clemson_hgic, ncsu_ext, rhs, ucanr_santa_clara_mg, uf_ifas, umd_ext, umn_ext, uwi_hort]`. The
   authored entries depend on `uc_ipm`, `uc_ipm_pn7493`, `ucanr_ext_spider_mites` and
   `ucanr_ext_snails_slugs`. All four are already in the canonical `source_catalog` at T1, including
   `uc_ipm_pn7493` -- so no new admission is required, contrary to the note that implies one.
5. **The batch's spittlebug ladder cap cites a document sage does not carry.** The review brief caps
   spittlebugs with UMN's "Pesticides are not effective." Sage's entry cites no UMN document. The cap
   is honored anyway (the ladder stops at `water_spray`), but on sage it is honored by UC IPM's
   *"Ignore spittlebugs"*, not by the sentence the brief names. Worth knowing before the same cap is
   asserted on lavender and rosemary.
6. **`uf_ifas` EENY-750 pushes against `low` severity and the entry now carries that tension well.**
   *"its feeding activity is associated with severe yellowing and branch drying of sage (Salvia
   officinalis) and rosemary"* is a commercial-herb framing; `low` is right for a garden and the
   corrected symptom string carries the escalation. No action; recording that the tension was handled,
   not buried.
7. **VCE ENTO-412NP remains the best-scoped leafhopper document and remains catalog-blocked.** It names
   sage among favored hosts, gives the 68°F egg-hatch threshold, and states the leaf-removal mechanism
   directly. The catalog admits VCE only under four publication-specific keys. A generic `vce` key, or
   a fifth publication key, would let the leafhopper entry stand on a US document instead of splitting
   between a Florida EDIS note and RHS.
