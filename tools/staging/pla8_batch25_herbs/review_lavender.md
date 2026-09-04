# PLA-8 BATCH 25 -- INDEPENDENT SOURCE-TRUTH REVIEW: LAVENDER

Reviewer pass date: **2026-09-04**. I did not author this file. Canonical and `out_lavender.json`
both unchanged by this pass; the only artifact is this report.

Scope: 4 entries, 16 rungs, 18 `field_corrections`. Every entry was completely unsourced before this
batch, so every anchor is new and every one was checked.

**Documents I fetched and read myself** (not taken from `record_lavender.md`):

| # | URL | Used for |
|---|---|---|
| 1 | https://ipm.ucanr.edu/home-and-landscape/lavender/ | the aphid asymmetry; host association |
| 2 | https://ipm.ucanr.edu/home-and-landscape/rosemary/ | the aphid asymmetry (the control) |
| 3 | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7401.html | all 6 whitefly rungs (3 separate passes) |
| 4 | https://ppo.puyallup.wsu.edu/lavender/ | PRCR scope test (2 passes) |
| 5 | https://ipm.ucanr.edu/home-and-landscape/phytophthora-root-and-crown-rot/ | PRCR management (3 passes) |
| 6 | https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/ | mulch, spacing, wilt gradient, pathogen list |
| 7 | https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ | leaf spot, root rot, pollinator attribute |
| 8 | https://extension.umn.edu/yard-and-garden-insects/spittlebugs | the spittlebug ladder cap |
| 9 | https://ipm.ucanr.edu/home-and-landscape/spittlebugs/ | spittlebug management (2 passes) |
| 10 | https://www.rhs.org.uk/biodiversity/cuckoo-spit-spittlebugs | host list, do-not-remove position |
| 11 | https://www.rhs.org.uk/plants/282089/lavandula-angustifolia-hidcote-group/details | leaf-spot umbrella framing |
| 12 | https://extension.colostate.edu/resource/growing-lavender-in-colorado/ | drainage / root rot |

Local checks run: `validate_out.py lavender` (exit 0, "2 pests + 2 diseases, 16 rungs"), a full string
walk of the canonical lavender record for aphid residue, the 64-method catalog for method legality and
for methods the ladders skipped, and a canonical-wide check of the two anchoring-key precedents the
record leans on.

---

## THE FIVE ASSIGNED FOCUS ITEMS, ANSWERED FIRST

### 1. The aphid deletion -- VERIFIED, AND THE DELETION IS COMPLETE

**The asymmetry is real. I reproduced it myself, on both pages, in the same session.**

* `https://ipm.ucanr.edu/home-and-landscape/lavender/` -- Pests and Disorders > **Invertebrates**:
  "Leafhoppers", "Spider Mites", "Spittlebugs", "Whiteflies". The word "Aphids" does not appear
  anywhere on the page.
* `https://ipm.ucanr.edu/home-and-landscape/rosemary/` -- Pests and Disorders > **Invertebrates**:
  "**Aphids**", "Leafhoppers", "Spider Mites", "Spittlebugs", "Thrips", "Whiteflies". Aphids is the
  first entry.

Same site, same editor, same index template, two Lamiaceae subshrubs, and lavender's list is a strict
subset of rosemary's minus aphids and thrips. That is a positive editorial act, not an oversight, and
it is a sound warrant for the deletion.

**Independent corroboration I added that the record did not have:** the RHS *L. angustifolia* Hidcote
details page returns **no occurrence of "aphid" anywhere on the page**; its Pests line is exactly
"May be susceptible to rosemary beetle, and to cuckoo spit (froghopper or spittle bug nymphs)".

**Deletion completeness -- CLEAN.** I walked every string in the canonical lavender crop record. The
substring "aphid" occurs in **exactly two places**: `/pests[1]/name` ("Whiteflies and aphids") and
`/pests[1]/symptoms_seasoned` ("tiny white flies or soft aphids"). The pin table renames the first;
`field_corrections.symptoms_seasoned` rewrites the second. No aphid claim survives in `companions`,
region prose, `varieties`, `tips_by_stage`, `weather_triggers` or anywhere else. This is the
"a claim lives in FIELDS" trap and it does not fire here. In `out_lavender.json` the word survives only
inside `why` strings and `notes_to_orchestrator`, which are metadata, not consumer copy.

### 2. The whitefly split anchor chain -- HONEST, and the six rungs are covered by 7401

Both keys are admitted T1 (`uc_ipm` = "UC Statewide IPM Program (UC ANR)"; `ucanr_ext` = "University
of California Agriculture and Natural Resources"). Both URL shapes are precedented in shipped
canonical: I counted **19 shipped `ucanr_ext` anchors that already use `ipm.ucanr.edu` URLs**
(apricot, cherry, blueberry, nectarine), so pointing `ucanr_ext` at a UC IPM host index is not novel.

PN 7401 never mentions lavender. The lavender host index carries no whitefly management. **No rung
note claims lavender-specific whitefly management**, and `refusals[0]` and `notes_to_orchestrator[10]`
both say so in as many words. The chain is stated accurately. Rung-by-rung verdicts below; five of the
six rest on verbatim 7401 sentences, one inverts a 7401 sentence.

### 3. The `wsu_ext_lavender_prcr` scope test -- PASSED, and this is the best-executed part of the file

I read the WSU page independently. **Its entire body prose is seven sentences:**

> "Lavender has few pests and diseases."
> "It is often promoted as a sustainable crop because growers do not commonly need to apply pesticides and fertilizers in its production."
> "However, recently growers have been reporting plants with symptoms of *Phytophthora* root and crown rot (PRCR)."
> "*Phytophthora* species are microscopic organisms that cause disease in plants."
> "Many species have been identified as the primary causes of root and crown rot of their host plants."
> "Diagnostic services are available from the WSU Plant and Insect Diagnostic Laboratory."
> "We have also prepared a guide for a technique to test your own samples for PRCR."

Confirmed absent, each checked by name: wet conditions, drainage, saturation, irrigation,
overwatering, yellowing, a rotted or darkened crown, removing or destroying plants, any species
binomial in the page's own prose.

**Every claim is cited to the source that carries it. There is no blanket-cite to WSU.** WSU is used
for exactly two things and both are its own: the many-species statement (`cause_seasoned`,
`cause_beginner`) and the image-caption symptom picture (`symptoms_seasoned`, `symptoms_beginner`,
verified verbatim: "a lavender bunch. the interior shoots are all dead and the shoots around the
outside are pale green with their flowers drooping"). Saturation goes to `uc_ipm`, overwatering to
`ncsu_ext_lavandula_angustifolia` and `csu_ext_lavender_07245`, prognosis and mound heights and clean
stock to `uc_ipm`, removal to `ncsu_ext`. That is the correct split and it is the thing this pass
exists to check.

**"There is no cure" softening -- DONE and correctly worded.** `organic_treatment_seasoned` now opens
"A plant with a substantial infection rarely recovers", matching UC IPM 74133 verbatim: "A plant with
a substantial Phytophthora infection rarely recovers." Beginner: "A plant that far gone rarely comes
back." Both absolutes are gone from the corrected cells. (One re-assertion survives in a rung note --
see FIX-15.)

**Six-species enumeration -- VERIFIED NOT WRITTEN.** No species list appears anywhere in the file.
`cause_seasoned` says "Many Phytophthora species cause root and crown rot on their hosts", which is
WSU's own generality, not the Dlugos/Bridges/Jeffers count.

### 4. The spittlebug ladder cap -- HONORED. No chemical rung crept in.

UMN's sentence, which I read directly: **"Pesticides are not effective against spittlebugs as the
nymphs are protected inside their spittle masses from any pesticide sprays."**

The ladder is `weed_host_control` (cultural), `water_spray` (physical), `handpick` (physical). Three
rungs, zero `soft_chemical`, zero `conventional`, on a crop where six insect-reaching materials exist
in the catalog. The refutation of "No specific prevention is warranted" is correct and both
replacement anchors are verbatim: UC IPM "Cut spittlebug-infested weeds in the spring before the
insects mature and spread." and UMN "Remove weeds near your gardens to remove one of their food
sources." Organism is *Philaenus spumarius* per both RHS and UMN. **Cap verified honored.**

### 5. The two NC State mulch facts -- BOTH LANDED, and the split matches the source sentence

The source sentence has two halves and the file routes each to the half it belongs to:

> "Avoid heavy organic mulches (sawdust, wood chips) as they can increase both fungal pathogens and insect problems."

* **Insect half** -> `Whiteflies.prevention_seasoned` and `.prevention_beginner`. Correct: the sentence
  is explicitly insect-scoped, so it is not a foliar claim wearing a pest hat.
* **Fungal half** -> `Leaf spot` / `splash_barrier_mulch` (both registers).
* **White sand** ("Dr. A. O. Tucker advises using one to two inches of white sand as a mulch around
  plants to reduce fungal pathogen infection") -> both places, verbatim on the "one to two inches".

`unreachable_claims[1]` explains why the insect half went to prose rather than onto `reflective_mulch`,
and the reasoning is right: `reflective_mulch` is silver film that repels arriving adults, and hanging
a heavy-organic-mulch warning on it would bend the method rather than use it. **Verified honest.**

---

## Spittlebug (`spittlebugs`) -- 3 rungs, 4 corrections

| # | Rung | Grade |
|---|---|---|
| 1 | `weed_host_control` | **HOLDS** |
| 2 | `water_spray` | **HOLDS** (one FIX inside) |
| 3 | `handpick` | **SYNTHESIS** (one FIX inside) |

**1. `weed_host_control` -- HOLDS.** Both registers. The timing, the target and the mechanism are each
in a document. UC IPM: "Cut spittlebug-infested weeds in the spring before the insects mature and
spread." carries "while the insects inside them are still young". UC IPM: "Spittlebugs are more likely
to become abundant on woody plants when they migrate from nearby herbaceous hosts." carries "the
surrounding cover is the reservoir" and "move onto lavender from there" -- and lavender is on-archetype
for "woody plants", it is a subshrub. UMN: "Remove weeds near your gardens to remove one of their food
sources." carries the second half of the seasoned note, which paraphrases it accurately as "keep weeds
down near the garden". One note for the record: UMN's stated *reason* is food-source removal, not
migration; the author correctly attributes the reservoir framing to UC IPM and does not put it in
UMN's mouth. "the one preventive step worth doing" is a superlative, but it is the only prevention
either T1 source publishes, so it holds.

**2. `water_spray` -- HOLDS, with FIX-11.** "a forceful stream from the hose washes the young insects
off the stems" is UC IPM verbatim ("Ignore spittlebugs or wash nymphs off with a forceful stream of
water") and UMN verbatim ("Spray them with a strong blast of water to dislodge nymphs from the
plants"). The RHS position is quoted accurately and, importantly, **attributed by name** -- "the Royal
Horticultural Society asks gardeners not to remove these insects at all" against RHS's "Spittlebugs are
not a pest, so please don't remove them". That is the right handling of a UK source under defect
class 4: named, not universalized. "the masses are a late-spring event that passes on its own" is
carried by RHS "Most active - May-July" plus UMN's single generation.

**3. `handpick` -- SYNTHESIS, with FIX-12.** "you can wipe the foam away and lift the small insect out
by hand" is UMN verbatim: "Physically remove them by hand." The generation claim is a generalization:
UMN says one generation per year *in Minnesota*, UC IPM says "one or two generations per year *in
California*"; the note converts two state-scoped statements into "one generation a year in colder
regions and at most two in mild ones". Defensible, but neither document states a climate gradient, and
the conclusion drawn from it ("a single walk through the planting in late spring usually finishes the
job") is an inferred step. Low severity; recorded because it is an inference presented as a fact.

### Corrections (4) -- ALL NEEDED, ALL ANCHORED

* `prevention_seasoned` / `prevention_beginner` -- **NEEDED and correct.** Canonical asserted "No
  specific prevention is warranted." while two T1 sources publish one. Both replacement anchors
  verified verbatim. The second half of the old text ("Keeping plants spaced for airflow and not
  overwatering keeps lavender vigorous enough to shrug off minor pests") is correctly identified as an
  unsourced template sentence; I confirmed it is a template by finding near-identical prose on
  rosemary and sage (see RECORD-LEVEL FINDINGS).
* `cause_seasoned` / `cause_beginner` -- **NEEDED and correct.** I verified the load-bearing quote
  character for character: "Spittlebugs' obvious and **occasionally abundant** masses of white foam on
  foliage and stems may be annoying, but they do not seriously harm established woody plants in
  landscapes." So "Numbers are usually low" does run against the source, and UMN independently allows
  high numbers ("If too many spittlebugs are present, feeding can cause leaves to lose their shape").
  The distorted-growth replacement is RHS verbatim.

---

## Whiteflies (`whiteflies`) -- 6 rungs, 6 corrections

| # | Rung | Grade |
|---|---|---|
| 1 | `reflective_mulch` | **SYNTHESIS** (FIX-2, FIX-3) |
| 2 | `garden_sanitation` | **WRONG** (FIX-1) |
| 3 | `water_spray` | **HOLDS** |
| 4 | `yellow_sticky_traps` | **HOLDS** (FIX-7, FIX-8) |
| 5 | `beneficial_predators` | **HOLDS** (FIX-9 is an omission around it) |
| 6 | `insecticidal_soap` | **HOLDS** (FIX-6) |

**1. `reflective_mulch` -- SYNTHESIS.** The practice holds: "Shiny metallic-coated construction paper
or reflective plastic mulches can repel whiteflies, especially away from small plants." and Quick Tips
"These mulches repel whiteflies while plants are small." The note's rendering of 7401's bed protocol as
"a decision to make at planting" is fair -- 7401's procedure genuinely is a bed-establishment one ("Lay
the product on bare soil, bury its edges with soil, and insert seedlings or seeds into holes in the
mulch"). Two defects, below.

**2. `garden_sanitation` -- WRONG.** See FIX-1. The first sentence is near-verbatim 7401 and is fine;
the second sentence contradicts 7401.

**3. `water_spray` -- HOLDS.** Quick Tips verbatim: "Hose adults off plants with a strong stream of
water." Body: "Water sprays (syringing) may also be useful in dislodging adults." The note's "a
knock-back and not a control; it reaches nothing that stays behind on the foliage" is exactly right and
is the correct life-stage framing: 7401's own line is that the nymphs are "oval, legless, and don't
move" and that "Nymphs cause most of the damage."

**4. `yellow_sticky_traps` -- HOLDS on the load-bearing content.** The rate is verbatim from 7401's
Quick Tips: "Hang sticky-coated yellow traps. **Use one trap for every medium-size vegetable plant.**"
The author kept the word "vegetable" rather than silently transplanting the unit onto a subshrub, which
is the honest call. The monitoring framing is 7401 verbatim: "Traps are most useful for monitoring and
detecting whiteflies rather than controlling them." Two small unsupported additions, FIX-7 and FIX-8.
One usability flag for the orchestrator, not a defect: 7401 carries a **second and different** rate in
its body -- "You may need as many as one trap for every two large plants" -- inside a paragraph scoped
"In vegetable gardens, yellow sticky traps can be posted around the garden to trap adults." A reader
with one lavender bush cannot apply either unit. Consider dropping the number.

**5. `beneficial_predators` -- HOLDS, and it is the best-anchored rung in the entry.** Quick Tips
verbatim: "Many beneficials or 'natural enemies' such as **lacewings and lady beetles** help control
whiteflies." and "Predators and parasites often keep them under control." The pesticide-avoidance half
is 7401's own lead sentence for the section: "Avoiding the use of insecticides that kill natural
enemies is a very important aspect of whitefly management." plus "Avoid using broad spectrum pesticides
such as pyrethroids, organophosphates, or neonicotinoids."

**6. `insecticidal_soap` -- HOLDS on every mechanical claim.** Verified one by one against 7401:
"Whiteflies can be difficult to control with insecticides." / "control only those whiteflies that are
directly sprayed" / "Be sure to cover undersides of all infested leaves" / "Repeat applications might
be required." / "Use soaps or oils when plants are not drought-stressed and when temperatures are under
90°F to prevent possible 'burn' damage to plants." The tier discipline is also right: one
`soft_chemical` rung and no `conventional` one, against 7401's "Even the most toxic insecticides are
only partially effective against whiteflies." One uncited claim, FIX-6, and one precision nit: 7401
permits use "when temperatures are **under** 90°F"; the note writes the limit as "no spraying **above**
90°F", which leaves 90 itself permitted. One degree, but it is a published threshold, so match it.

### Corrections (6) -- 4 HOLD, 2 carry a placement defect

* `symptoms_seasoned` -- **HOLDS.** "one of only four invertebrates UC IPM lists for lavender" is a
  checkable claim and I checked it: the list is exactly Leafhoppers, Spider Mites, Spittlebugs,
  Whiteflies. Both defects the correction names are real (the aphid half; the unsourced stress link).
* `symptoms_beginner` -- **HOLDS.** "Lavender gets very few insect pests" carried by NCSU "Few insect
  problems have been reported on field-grown lavender." and WSU "Lavender has few pests and diseases."
* `organic_treatment_seasoned` / `organic_treatment_beginner` -- **HOLDS, and the correction was
  NEEDED.** "Removing nearby stressors and improving airflow usually resolves it" is genuinely
  unanchored for this pest on this crop. The retained water-and-soap sentence is now properly anchored
  at 7401, verified.
* `prevention_seasoned` -- **FIT defect, FIX-4.**
* `prevention_beginner` -- **FIT defect, FIX-5.**

---

## Phytophthora root and crown rot (`lavender-root-crown-rot`) -- 4 rungs, 8 corrections

| # | Rung | Grade |
|---|---|---|
| 1 | `improve_drainage` | **HOLDS** -- strongest rung in the file |
| 2 | `resistant_varieties` | **SYNTHESIS** (FIX-13, FIX-14) |
| 3 | `certified_clean_stock` | **HOLDS** (FIX-15) |
| 4 | `garden_sanitation` | **SYNTHESIS** (FIX-16, FIX-17) |

**1. `improve_drainage` -- HOLDS, every clause.** The mound numbers are verbatim and, critically, the
*right* number was selected: 74133 says "The mounds should be 8 to 10 inches high for annuals and up to
2 feet high with a gradual slope for **trees and perennials**", and the note routes lavender to the
perennial figure. "keep soil and mulch off the crown itself" is 74133 verbatim ("Never cover the root
crown or graft union with soil or mulch."). "Let the top few inches dry thoroughly between waterings"
is 74133 verbatim. "drainage is the control here and fungicides do not stand in for it" is better
supported than the anchor claims -- 74133 also says "**The most important factor in reducing the
development of Phytophthora root and crown rot diseases is appropriate water management.**", a sentence
the entry does not quote but which settles the framing outright.
*Available strengthening, not a defect:* 74133 publishes "It's important to remember that Phytophthora
diseases can develop in as little to 4 to 8 hours of soil saturation." That is a vivid, actionable,
published number this ladder does not use.

**2. `resistant_varieties` -- SYNTHESIS.** The method is independently warranted ("Select certified
nursery stock and resistant rootstocks or varieties when available.", 74133, verbatim). The *gradient*
is not warranted for this disease. Details in FIX-13 and FIX-14. One point in the author's favor that
should be recorded: NC State's second and third sentences are **not** wilt-scoped -- "Dark-flowered
cultivars are less resistant **to disease** than the pale-flowered varieties. Cultivars with gray
foliage are quite susceptible **to infection**." Only the first sentence names vascular wilts. That
narrows the objection to the lavandin-over-English half.

**3. `certified_clean_stock` -- HOLDS, and better anchored than the file knows.** 74133 carries a
sentence the entry never quotes and that directly supports the beginner note: **"When purchasing from
nurseries, inspect and choose plants carefully. Slip plants from their pots before purchase to examine
the root system."** So "look the plant over" and "inspecting at the nursery costs nothing" are
published, not inferred. Two small notes: the source says inspect **before purchase** while the
beginner note says "before it goes in the ground", which is later and weaker; and the source names a
technique (slip it from the pot, look at the roots) that is more useful than "look the plant over".
FIX-15 is the one real defect here.

**4. `garden_sanitation` -- SYNTHESIS.** "removing and destroying the affected plant" is NC State
verbatim ("If damaged plants are present, remove and destroy any infected plant material and avoid
replanting with susceptible varieties.") and "A substantial infection rarely recovers" is UC IPM
verbatim. FIX-16 and FIX-17 below.

### Corrections (8) -- ALL HOLD; two carry record-fidelity notes

All eight are NEEDED and all eight anchors were verified verbatim against the documents. The
distribution of claims across sources is correct (see focus item 3). Two items to file rather than fix:

* `organic_treatment_seasoned`'s `why` says "the removal advice is kept because NC State does publish
  it." The record was more careful: that NC State sentence "is inside the **vascular wilt** paragraph,
  not the root-rot one. So the removal advice is anchorable, **obliquely**." I confirmed the paragraph
  placement. The caveat should ride with the anchor; dropping it is a small loss of record fidelity.
* `symptoms_seasoned`'s `why` deletes the crown sign as tree-scoped. That reasoning is defensible, but
  it is not applied consistently and it has a consumer cost -- see FIX-16.

**Conventional-tier refusal -- VERIFIED CORRECT.** I checked the 64-method catalog: the only
`conventional` fungicides are `chlorothalonil` and `mancozeb`, both `applies_to: fungal_foliar`.
Neither is fosetyl-al, phosphorous acid or mefenoxam. `unreachable_claims[3]` is accurate and the
refusal is right on both grounds (no catalog match, and the source's own "do not rely on pesticide
applications alone").

---

## Leaf spot (`lavender-leaf-spot`) -- 3 rungs, 0 corrections

| # | Rung | Grade |
|---|---|---|
| 1 | `airflow_spacing` | **HOLDS** (FIX-18) |
| 2 | `splash_barrier_mulch` | **HOLDS** (SYNTHESIS on one clause) |
| 3 | `garden_sanitation` | **UNSUPPORTED, disclosed** (FIX-19) |

### The §4f umbrella ruling -- I WAS INVITED TO OVERTURN IT AND I DO NOT. It should stand.

I re-derived the evidence rather than accepting the record's:

* `ncsu_ext` New Crops publishes the only *Lavandula* pathogen list I could find at US T1. I pulled it
  and it contains eleven entries. Exactly one is a leaf spot: **"*Septoria lavandulae* -- leaf spot"**.
  It appears **in a bulk list, with no symptom description, no US distribution statement and no
  management**, alongside root rots, wilts, a stem blight, a nematode and a parasitic vine.
* `ncsu_ext_lavandula_angustifolia`, checked directly: the Problems section is "No significant problems.
  However, it is susceptible to leaf spot and root rot." and the only management sentence is "Providing
  good air circulation helps prevent leaf spot." **The page names no organism at all.**
* `rhs`, checked directly and verbatim: "May be susceptible to honey fungus, grey moulds, lavender
  shab, and **fungal leaf spots**." Plural -- an umbrella by construction. And note it lists **shab
  separately**, so the umbrella correctly does not sweep shab in.

Pinning to `septoria-leaf-spot` would assert, on the strength of one bulk-list line whose primary
description is a first-report from Croatia, that *S. lavandulae* is what a US home gardener sees on
lavender. Nothing published says that, and the entry's other admitted source pluralizes. A problem `id`
is a permanent join key that must never be re-derived, so minting a pinned pathogen id on this evidence
buys nothing and commits the dataset to a claim it cannot defend. **The umbrella is correct.** That it
is the opposite of oregano's ruling in the same batch is expected: §4f is a per-crop evidence question,
and lavender's evidence is a bulk list with no clinical content.

### Zero field_corrections -- ENDORSED

I read the canonical leaf-spot prose myself. Its two load-bearing specifics ("Good airflow is the main
defense"; "Space plants at least 2 to 3 feet apart for air circulation") match NC State in substance and
number. The residuals the author lists as knowingly left in place -- "more likely in humid weather",
"Crowding and overhead watering raise the risk", "water at the base rather than overhead", "avoid
overhead watering" -- are genuinely unanchored on lavender and genuinely not refuted. The brief asks me
to confirm a correction was needed; here the correct finding is that **none was**, and declining to
manufacture one to look thorough is the right call. Do not move NC State's 90 °F / 90% August figure
onto this entry; it is published for **vascular wilt**, which I confirmed.

**1. `airflow_spacing` -- HOLDS.** "2 to 3 feet apart" is NC State verbatim ("spacing plants 2-3 feet
apart"), given for exactly the stated reason ("In order to discourage fungal pathogens, good air
circulation is advised"), on a site NC State words the same way ("in a dry, open and sunny position").
"Trimming the lower branches through the growing season" is verbatim. "the main defense against leaf
spot" is a rank claim where the toolbox says "helps prevent" -- but it is the only preventive measure
either NC State document publishes for lavender leaf spot, so the inference from "only" to "main"
holds. FIX-18 is the trailing clause.

**2. `splash_barrier_mulch` -- HOLDS on the facts.** Both NC State sentences are verbatim and correctly
placed. Two things to record rather than fix: NC State attributes the white sand to a person ("Dr. A. O.
Tucker advises"), which the note flattens to "is the mulch recommended for lavender"; and NC State's
white-sand claim is about "fungal pathogen infection" generally, not leaf spot specifically, so applying
it here is a narrowing (reasonable on a foliar entry). The splash mechanism itself -- "a mineral layer
over the soil surface is the barrier that keeps rain splash from carrying soil onto the lowest leaves" --
is **SYNTHESIS**: NC State gives no mechanism. It reads as the catalog method's own rationale rather
than as an NC State claim, which is why it is not a FIX, but it is an authored mechanism sitting
directly beside a verbatim source fact.

**3. `garden_sanitation` -- UNSUPPORTED, disclosed.** See FIX-19.

---

## FIX ITEMS

Ordered by severity. Each gives the exact text, the defect, and the document sentence that settles it.

### FIX-1 (MATERIAL) -- the whitefly sanitation rung inverts a sentence in its own anchoring document

**Text** (`Whiteflies` / `garden_sanitation` / `note_seasoned`):
> "It is worth most at the first find and worth very little once the insects are spread through the canopy, so the value is in catching it early rather than in doing it thoroughly later."

**Settled by** PN 7401, body:
> "Hand removal of leaves or plants **heavily infested** with the nonmobile nymphal and pupal stages **may reduce populations to levels that natural enemies can contain**."

UC IPM publishes hand removal at **both** ends of the curve -- Quick Tips for the isolated first find
("Prune out isolated infested leaves when you first detect them", which the note's first sentence
correctly carries), and the body for the heavy infestation, where it states a specific payoff. The note
asserts the opposite about the heavy end. This also breaks the entry against itself: rung 2 tells the
reader sanitation is nearly worthless once whiteflies are spread, while rung 5 tells them natural
enemies do most of the work -- and the deleted sentence is precisely the bridge between the two.

**Secondary, same rung:** neither register mentions that the removable stages are the **nonmobile
nymphs and pupae on leaf undersides**. That is the reason the method works; adults fly off. A reader
told to prune "leaves where you find whiteflies" will target the flying adults they can see. This is
defect class 1 in its omission form. 7401: nymphs are "oval, legless, and don't move" and "Nymphs cause
most of the damage."

*Also minor in the beginner register:* "carry them out of the garden rather than dropping them under the
plant" is not published for leaves in 7401 (its "destroy" sentences are about whole annual and vegetable
plants). SYNTHESIS, acceptable as method-level practice.

### FIX-2 (MATERIAL) -- an invented mechanism on `reflective_mulch`

**Text** (`note_seasoned`):
> "its documented benefit is on small plants: **once foliage grows over the sheeting the effect goes**."

7401 says **when** to stop, never **why**:
> Quick Tips: "**Remove mulches when plants get large and temperatures get hot.**"
> Body: "When summertime temperatures get high, remove mulches to prevent overheating plants."

The only reason the page gives is heat. The foliage-covering mechanism appears nowhere on it. The
practice is right and the reason is authored -- defect class 3, and the reason is what the reader
learns.

### FIX-3 (MATERIAL) -- `reflective_mulch` omits the source's removal instruction

The rung never tells the reader to take the mulch up. 7401 says so twice, and the second reason is a
plant-safety one: "**Remove mulches when plants get large and temperatures get hot.**" / "When
summertime temperatures get high, remove mulches to prevent overheating plants." Lavender's own sourced
siting is "a dry, open and sunny position" (NC State), i.e. exactly the hot site where this bites. A
reflective sheet left down through a lavender summer is the failure mode the source is warning about.

### FIX-4 (MATERIAL) -- the author's own placement rule is applied to one entry and not the other

**Text** (`Whiteflies` / `prevention_seasoned`):
> "Site lavender in full sun on light, sharply drained ground, and **set plants 2 to 3 feet apart**."

**Settled by** NC State, the sentence the anchor itself cites:
> "**In order to discourage fungal pathogens**, good air circulation is advised and can be achieved by spacing plants 2-3 feet apart and trimming the lower branches throughout the growing season."

Eight fields later in this same file, the author removes spacing from `Phytophthora.prevention_seasoned`
with the reason: *"'and space plants for airflow' is attached to the wrong problem. Spacing is genuinely
sourced on this crop, but for FOLIAR fungal pathogens by way of air circulation."* That reasoning
applies identically here: the 2-to-3-foot number is published for fungal pathogens, and it now sits in a
**whitefly** prevention cell. No document read connects plant spacing to whitefly pressure on lavender.

In fairness, the two cases are not equally bad: airflow against a soilborne water mold is affirmatively
wrong, whereas spacing on a whitefly entry is merely unsourced. But the reader-facing effect is the
same, and a rule stated in a file should hold across that file. Either drop the spacing clause here or
record why this cell is exempt. The mulch half of the same correction is properly placed and should
stay -- NC State's sentence is explicitly insect-scoped.

### FIX-5 (MATERIAL) -- irrigation advice in the whitefly prevention cell runs against the whitefly document

**Text** (`Whiteflies` / `prevention_beginner`):
> "Keep lavender in full sun **with room around it**, in light soil that drains fast, **and do not overwater**."

Same spacing issue as FIX-4, plus a sharper one. The only irrigation statement in PN 7401 points the
other way:
> "**Watering can also reduce the hot, dry dusty conditions that favor whiteflies and inhibit their natural enemies.**"

This is not an argument for watering lavender more -- lavender's drainage advice is well sourced
elsewhere and should not change. It is an argument that irrigation guidance does not belong in this
cell at all: the entry's own management document treats dry, dusty conditions as *favoring* whiteflies,
so "do not overwater" reads as whitefly prevention while the source says the opposite.

### FIX-6 (MATERIAL, cheap) -- the bee caution has no anchor inside the entry

**Text** (`insecticidal_soap`, both registers):
> "Keep it off the flowers, which are full of bees" / "on a plant this heavily worked by pollinators the spray belongs on foliage rather than bloom."

PN 7401's **only** pollinator sentence is about a different material entirely:
> "Imidacloprid can have negative impacts on natural enemies, honey bees and other pollinators in the garden..."

That is a neonicotinoid, not a soap. None of the entry's four sources (`uc_ipm` PN 7401, `ucanr_ext`
lavender host index, `wsu_ext_lavender_prcr`, `ncsu_ext` New Crops) states that lavender attracts
pollinators. The claim is true and the fix is nearly free: `ncsu_ext_lavandula_angustifolia` -- already
an admitted T1 key and already used on two other entries in this same file -- carries the attribute
line **"Attracts: Butterflies, Pollinators"**. Add the key and URL to this entry's `sources` /
`anchoring_urls`. The advice runs in the protective direction so there is no safety exposure, but this
is an uncited claim on the one entry whose entire justification was honest anchoring.

### FIX-7 (minor) -- "the catch includes small beneficials" is not in PN 7401

I queried the page specifically for this and it returns nothing. 7401 does not say sticky traps catch
natural enemies. Drop the clause or anchor it elsewhere.

### FIX-8 (minor) -- "take them down afterward" is not in PN 7401

The page gives no take-down advice, and its trap paragraph implies sustained use: "**Periodic cleaning
is essential** to remove insects and debris from the boards and maintain the sticky surface." Also,
"traps remove flying adults" is firmer than 7401's own hedge, "Such traps won't eliminate damaging
populations but may reduce them somewhat" -- though the note reframes to monitoring immediately after,
which rescues it.

### FIX-9 (MATERIAL, omission) -- an available, published whitefly rung is omitted with no recorded decision

7401 publishes ant management twice:
> Quick Tips: "**Keep ants out of plants since they protect whiteflies from natural enemies.** Don't use pesticides if natural enemies are present."
> Body: "Control of dust and **ants, which protect whiteflies from their natural enemies**, can also be important, especially in citrus or other trees."

`ant_exclusion` **exists in the 64-method catalog** -- `tier: physical`, `applies_to:
insect_soft_bodied, insect_general, disease_general` -- so it is mechanically legal on this entry. The
mechanism is live here: 7401's own signs list includes "Sticky honeydew on leaves, fruit, or beneath
plants", which is what recruits ants.

The defect is not that the rung is missing; a decision to decline it is legitimate (the body sentence
scopes it "especially in citrus or other trees"). The defect is that **it is not recorded anywhere**.
`unreachable_claims` carefully records the dust half, the oils half, and the "less susceptible plants"
half of the same page, so an unrecorded omission of the ant half reads as an oversight rather than a
decision -- which is exactly the standard the author set for themselves in `unreachable_claims[4]`.

### FIX-10 (minor, omission) -- the cheapest published first step is also unrecorded

> Quick Tips: "**Inspect new plants for whiteflies before bringing them into your garden.**"
> Body: "Always inspect new plants for whiteflies and nymphs before introducing them in the greenhouse or garden."

`certified_clean_stock` has `insect_general` in its `applies_to`, and the author already uses that
method on the Phytophthora entry in this same file. Author it or record the refusal.

### FIX-11 (minor) -- the spittlebug entry contradicts itself about damage

**Text** (`water_spray` / `note_seasoned`):
> "the feeding itself **costs an established subshrub nothing**."

The entry's own corrected `cause_seasoned`, three fields away, says "a shoot tip that has been fed on
may grow distorted", anchored to RHS. UMN adds "If too many spittlebugs are present, feeding can cause
leaves to lose their shape." No source says the cost is nothing; the strongest wording available is
UC IPM's "do not seriously harm" and RHS's "little detrimental effect". Match one of those.

### FIX-12 (minor) -- an unsourced premise imported into the handpick rung

**Text** (`handpick`):
> beginner: "It is slower than the hose, but **it leaves the foliage dry**."
> seasoned: "is **the option that does not wet the canopy**."

Presented as the reason to prefer handpicking, this asserts that wetting lavender foliage carries a
cost. The author's own `notes_to_orchestrator[6]` states the opposite about the evidence: **"No lavender
document read mentions overhead watering at all."** So this is the very premise the file records as
unsourced on this crop, re-entering as a rung-note benefit. Lavender's sourced fungal advice is air
circulation, not foliage dryness.

### FIX-13 (minor) -- a superlative NC State does not use

**Text** (`resistant_varieties` / `note_beginner`):
> "cultivars with gray foliage or dark flowers are **the most susceptible**."

**Settled by** NC State:
> "Dark-flowered cultivars are **less resistant** to disease than the pale-flowered varieties. Cultivars with gray foliage are **quite susceptible** to infection."

Neither is a superlative. The seasoned register already gets this right -- "with gray-foliage and
dark-flowered cultivars at the susceptible end and pale-flowered types holding up better" -- so align
the beginner to the seasoned.

### FIX-14 (judgment call, flagged by the author) -- the varietal gradient is wilt-scoped

NC State's lavandin-over-English sentence is explicitly "more susceptible to **vascular wilts**". The
bridge to PRCR runs through a single bulk-list entry, "*Phytophthora* spp. -- wilt", which I confirmed
exists. A list-level classification is a weak bridge for a management claim: this is the
right-document-wrong-claim pattern. As written the rung tells a reader that choosing lavandin lowers
their root-and-crown-rot risk, which nothing published states.

**My recommendation, differing slightly from the author's offered exit:** keep the rung -- UC IPM's
"Select certified nursery stock and resistant rootstocks or varieties when available" independently
warrants the *method* for this disease -- but drop or heavily hedge the lavandin/English half. The
gray-foliage and dark-flower halves are on firmer ground, since NC State words those "to disease" and
"to infection" rather than to wilt.

### FIX-15 (minor) -- the softened absolute reappears one rung later

**Text** (`certified_clean_stock` / `note_seasoned`):
> "**Root and crown rot has no in-ground rescue**, so a plant that arrives already infected is a loss paid for at purchase."

The entry's `organic_treatment_*` correction exists specifically to soften "There is no cure" to UC
IPM's hedged "A plant with a substantial Phytophthora infection rarely recovers." "No in-ground rescue"
restates the absolute in a rung note. Per the safety-absolute pattern, fix every field carrying the
claim, not just the one the correction targeted.

### FIX-16 (MATERIAL) -- the entry deletes the crown symptom and then uses it twice

The `symptoms_seasoned` correction removes "a darkened, decayed crown at the soil line" on the grounds
that 74133's crown description is scoped to barked **trees**. Then:

> `garden_sanitation` / `note_beginner`: "Dig out and get rid of a lavender **whose crown has gone soft**."
> `organic_treatment_seasoned`: "...so **once the crown is rotting** the realistic move is to remove and destroy it."

The file asserts both that crown decay is unsayable on lavender and that the reader should act on it.
One of the two has to give.

**My view: the deletion over-corrected, and the rung notes are the honest half.** The disease is named
"Phytophthora root and crown **rot**"; 74133 is the entry's own cited disease document; and after the
deletion the symptoms cell reads "Shoots wilt, brown, and die back and do not recover with watering" --
which equally describes drought, winter kill and simple decline. The entry now gives the reader **no
sign that distinguishes PRCR from anything else**, which is a real loss on a `severity: high` disease
whose whole management is preventive and whose window closes at purchase. Recommend restoring a hedged
crown sign to `symptoms_*`, worded for a subshrub rather than for tree bark and anchored to 74133,
rather than stripping it from the two rung notes.

### FIX-17 (minor) -- replant advice narrowed against its source

**Text** (`garden_sanitation` / `note_seasoned`):
> "Do not put a susceptible replacement in the same spot **until the drainage that caused it has actually been fixed**."

NC State's advice is unconditional: "...and **avoid replanting with susceptible varieties**." The
condition implies that once drainage is fixed a susceptible variety is fine. *Phytophthora* persists in
soil independent of drainage, and 74133 confirms the reservoir: "Contaminated soil or water, resting
spores in decaying host tissue, and infected roots can all be sources for new infections."

*Also in this rung, minor:* "diseased tissue dropped on a compost pile can carry the problem on" is
stated in no cited document -- but 74133's "resting spores in decaying host tissue" is the mechanism,
on a page the entry already cites. SYNTHESIS; quote it and it becomes HOLDS.

### FIX-18 (minor) -- a third invented mechanism, on leaf spot

**Text** (`airflow_spacing` / `note_seasoned`):
> "the base of a maturing bush is **where the canopy closes over first**."

NC State gives the instruction with no reason: "...good air circulation is advised and can be achieved
by spacing plants 2-3 feet apart and trimming the lower branches throughout the growing season." The
explanation is authored. This is the third instance of the same pattern in this file (with FIX-2 and
the splash clause), which is worth naming as a pattern rather than three separate slips.

### FIX-19 (decision needed) -- one rung has no anchor inside its own entry

`Leaf spot` / `garden_sanitation` rests on `uconn_ext`, which the author **deliberately kept out of
`sources`** because that document never names lavender -- the right instinct, and it avoids the
mis-pointed-key defect. But the consequence is a rung whose warrant is not reachable from the entry's
own `sources` / `anchoring_urls`. It is the only such rung in the file.

The note discloses it in as many words ("This is general leaf-spot practice rather than a
lavender-specific finding"), which is the honest handling. This is not a defect to fix silently; it is a
call for the orchestrator to make deliberately, because a rung with zero in-entry anchor is the thing
`sources` exists to make impossible.

---

## SUMMARY

**Rung grades (16 rungs):**

| Grade | n | Rungs |
|---|---|---|
| **HOLDS** | 10 | spittlebug `weed_host_control`, `water_spray`; whitefly `water_spray`, `yellow_sticky_traps`, `beneficial_predators`, `insecticidal_soap`; PRCR `improve_drainage`, `certified_clean_stock`; leaf spot `airflow_spacing`, `splash_barrier_mulch` |
| **SYNTHESIS** | 4 | spittlebug `handpick`; whitefly `reflective_mulch`; PRCR `resistant_varieties`, `garden_sanitation` |
| **WRONG** | 1 | whitefly `garden_sanitation` |
| **UNSUPPORTED** | 1 | leaf spot `garden_sanitation` (disclosed) |
| STYLE | 0 | -- |
| FIT | 0 (at rung level) | -- |

**Correction grades (18 corrections):**

| Grade | n |
|---|---|
| **HOLDS** (needed, anchored, anchor verified verbatim) | 16 |
| **FIT** (true and sourced, attached to the wrong problem) | 2 -- `Whiteflies.prevention_seasoned`, `Whiteflies.prevention_beginner` |
| WRONG / UNSUPPORTED | 0 |

**FIX items: 19** -- 8 material (FIX-1, 2, 3, 4, 5, 6, 9, 16), 11 minor. Plus 4 precision nits
(the "under 90°F" boundary; inspect-before-purchase vs before-planting; the dropped wilt-paragraph
caveat on the NC State removal anchor; the flattened "Dr. A. O. Tucker advises" attribution).

**What this file gets right, stated plainly because it is most of it.** The two hardest things it was
asked to do it did well. The WSU split-citation discipline is exact: WSU is cited for the two things it
carries and for nothing else, and every drainage, prognosis, irrigation and removal claim is routed to
the document that actually publishes it. And the ladder caps are all honored with no padding -- three
of four ladders end at cultural or physical, the spittlebug cap is verified against UMN's own sentence,
the conventional refusal on PRCR is verified against the catalog (only `chlorothalonil` and `mancozeb`
exist and both are `fungal_foliar`), and the single `soft_chemical` rung on whiteflies is exactly what
7401 supports. Numbers are verbatim and correctly scoped throughout, including the one place it would
have been easy to get wrong: the mound height routes lavender to UC IPM's "trees and perennials" figure,
not the annual one.

### THE SINGLE MOST IMPORTANT FINDING

**The one rung authored from the document the orchestrator supplied to unblock the ladder is the one
rung that contradicts it.**

`Whiteflies` / `garden_sanitation` / `note_seasoned` tells the reader the step is "worth very little
once the insects are spread through the canopy." PN 7401 says the opposite, and says it with a stated
payoff:

> "Hand removal of leaves or plants **heavily infested** with the nonmobile nymphal and pupal stages **may reduce populations to levels that natural enemies can contain**."

The deleted sentence is also the bridge to the entry's own `beneficial_predators` rung, so the ladder
now contains two rungs that disagree about whether physical removal helps once an infestation is
established. This is worth naming beyond lavender: the ladder was refused, then unblocked by one
supplied document, and the rung that drifted furthest from that document is the one whose supporting
sentence sits in the body rather than in the Quick Tips box the author's other five rungs track
closely. A supplied document gets read to the depth needed to author from it, and the tail of the page
is where that depth ran out.

---

## RECORD-LEVEL FINDINGS

Filed for a later pass, not fixed now.

**R1. The cross-crop twin lead is real and BROADER than the file states.** `notes_to_orchestrator[9]`
names rosemary (one sentence) and thyme (two). I read canonical for all three siblings. All three carry
the defects, across all three classes:

* "**and space plants for airflow**" in a root-rot `prevention_seasoned`: rosemary, thyme **and sage**
  (sage's entry is `Root and stem rot`). Three crops, not one.
* "**Once the base is rotting there is no fix**" in `organic_treatment_beginner`: rosemary, thyme
  **and sage**. Three crops.
* the unanchored wet-vs-cold contrast in `cause_beginner`: thyme ("The real cause is wet soil, not cold
  weather"), rosemary ("The real cause is too much water, not cold"), sage ("The real cause is wet soil,
  not cold"). Three crops.
* "**No specific prevention is warranted.**" survives on **rosemary**'s spittlebug entry, with the same
  unsourced vigor substitute ("Good spacing, full sun, and no overwatering keep rosemary vigorous enough
  to shrug off minor pests"). Sage's variant is milder but carries the same claim ("vigorous sage shrugs
  off minor pests").
* "**There are usually only a few**" in spittlebug `cause_beginner`: rosemary **and** sage, identical to
  the lavender sentence this file refuted.

If those crops' record passes reached the same verdicts, the same corrections are owed on all of them,
and the three spittlebug entries must be fixed together since they share the newly minted `spittlebugs`
id.

**R2. A shipped mis-pointed anchoring key, found while verifying NOTE A.** Checking the record's
`ncsu_ext`-with-a-non-`content.` -subdomain precedent (which is sound -- **42 shipped anchors** use
`plants.`, `vegetables.` and `pender.ces.ncsu.edu`), one row is not NC State at all:

> `eggplant.pests["Hornworms"].anchoring_urls.ncsu_ext.url = https://hgic.clemson.edu/factsheet/eggplant-insect-pests-diseases/`

An `ncsu_ext` key pointing at a Clemson document. Cross-institution, in shipped canonical, out of scope
for this crop, and exactly the defect class this pass exists to kill.

**R3. Both anchoring-key precedents this file relies on are VERIFIED, so neither needs re-litigating:**
42 shipped `ncsu_ext` anchors on non-`content.` ces.ncsu.edu subdomains, and 19 shipped `ucanr_ext`
anchors on `ipm.ucanr.edu` URLs. The whitefly key split and the New Crops URL are both precedented.

**R4. The roster gap is confirmed and still open.** UC IPM's lavender host page lists four
invertebrates; `lavender.pests[]` carries two. Leafhoppers and spider mites are absent from the crop
entirely. After this batch the crop matches its best host-indexed source in one direction (nothing
carried that UC IPM does not list) but not the other.

**R5. Prose and ladder now disagree about overhead watering on leaf spot.** The canonical prose retains
"avoid overhead watering" and "water at the base rather than overhead" (correctly left alone, since
nothing refutes them), but `water_at_the_base` and `wet_foliage_discipline` both exist in the catalog
and both reach `fungal_foliar`, and neither was authored. The entry therefore advises in prose what its
ladder declines to encode. Defensible -- the ladder is the sourced layer -- but it is a visible
asymmetry a later pass will re-find.

**R6. The record's PRECISION notes were not acted on and not recorded as declined.** The record asked
the ladder pass to consider that UC IPM calls the foam "frothy white **excrement**" rather than a
shelter the nymph builds, and that feeding is on **xylem** fluid. The corrected `cause_seasoned` keeps
"shelter inside their own foam while feeding on plant sap". The record itself judged both acceptable
("defensible as function, not as origin"; "'plant sap' is acceptable common tongue"), so this is a
paperwork item, not a defect -- filed so nobody re-finds it.

**R7. Display-name divergence, unresolved and correctly escalated.** Lavender keeps singular
"Spittlebug" while rosemary and sage carry "Spittlebugs", all three sharing the newly minted
`spittlebugs` id. The author declined to change a pinned name mid-fan-out, which is right. It needs a
batch-level call.

**R8. Available strengthenings, none of them defects.** UC IPM 74133 publishes two sentences this file
could use and does not: "Phytophthora diseases can develop in as little to 4 to 8 hours of soil
saturation" (a vivid, actionable number for `improve_drainage`) and "Slip plants from their pots before
purchase to examine the root system" (a concrete technique for `certified_clean_stock`, better than
"look the plant over"). Also unrecorded and still owed: the PNW Handbook `lavender-root-rot` page
remains 403 to WebFetch, and per the url-liveness rule that is a block, not an absence.
