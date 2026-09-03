# PLA-8 batch 24 -- SOURCE TRIAGE. Ten decisions, and what the documents actually say.

**Written 2026-09-02.** Canonical `c24d7754`. **Nothing has been changed.** This is step 1 of the
record-before-advice plan: for every problem entry whose sourcing was challenged, determine whether
a supporting document exists and where.

**Method.** Five independent researchers, one per document family, each instructed to FETCH AND READ
and to treat a search summary as worthless. Roughly 40 documents read. Every verdict below carries
the exact sentence or the explicit finding of absence. Where a researcher could not read a document
it is recorded as UNREAD, never as absent.

**The 17 challenged problem entries collapse to 10 decisions**, because the allium records are
templated: onion, shallot and leek say the same thing about thrips (0.90 similar) and pink root
(0.89-0.93), and the onion-maggot decision covers all four crops.

---

## Summary of the ten

| # | claim-set | crops | verdict |
|---|---|---|---|
| 1 | onion maggot | chives, leek, onion, shallot | **REPOINT** -- content stands, citation moves |
| 2 | onion thrips | leek, onion, shallot | **CONTENT PROBLEM** -- 4 of 5 claims unsupported |
| 3 | pink root | leek, onion, shallot | **REPOINT + DROP ONE CLAIM** |
| 4 | chives aphids | chives | **ENTRY IS WEAKLY FOUNDED** -- cited page says the opposite |
| 5 | chives botrytis | chives | **TWO DIFFERENT FUNGI BUNDLED** -- rename or split |
| 6 | chives rust | chives | **REPOINT** -- a US document supports all three claims |
| 7 | leek moth | leek | **FACTUALLY WRONG FOR THE US** -- advice would fail |
| 8 | leek allium leafminer | leek | **FACTUALLY WRONG** -- cover-during vs cover-before |
| 9 | leek rust | leek | **PROBABLY NOT A US LEEK PROBLEM** |
| 10 | shallot downy mildew | shallot | **FACTUALLY WRONG** -- "tolerant varieties" |

**Four of the ten are content defects, not citation defects.** Three of those four are on leek.

---

## 1. ONION MAGGOT -- repoint (chives, leek, onion, shallot)

Current anchor `extension.umn.edu/vegetables/growing-onions` carries exactly one sentence: *"Onion
maggot bores into plant stems, causing the plants to turn yellow and wilt."* No management at all.

| claim | verdict | evidence |
|---|---|---|
| rotation away from alliums | **SUPPORTED** | UC IPM `/maggots/`: *"Avoid planting successive onion crops without rotating to other crops."* UMN root-maggots: *"Practice crop rotation to minimize this issue."* |
| remove culls | **SUPPORTED** | UC IPM: *"Remove and dispose of onion culls and volunteer onions."* UMN (home): *"Remove target plants in the fall, including their roots, and destroy them."* |
| remove crop *residue* | **CONTRADICTED** | UC IPM says the opposite: *"Thoroughly incorporate organic matter such as manure, crop residue, weeds, and cover crops into the soil well in advance of planting."* |
| floating row cover | **SUPPORTED, one source only** | UMN root-maggots: *"Row covers are an effective option to prevent adult flies from getting near the plants to lay eggs."* **UC IPM has no row-cover content at all.** Clemson has none. |
| timing "at emergence" | **NOT SUPPORTED ANYWHERE** | UMN anchors to fly activity on a Minnesota calendar: *"set up the barrier in your garden by the time adult flies are laying eggs, usually early to mid-May."* Crop emergence and fly egg-laying are different events. |

**ACTION:** repoint to `extension.umn.edu/yard-and-garden-insects/root-maggots` (+ UC IPM
`/maggots/`). Drop "at emergence" as a sourced deadline. Reword the residue claim to culls and
lifted plants, which is what the sources actually support.

**CREDIT WHERE DUE:** the row-cover trap precondition -- covering ground that grew alliums seals
emerging flies in *with* the crop -- is present in **all four** batch-24 rungs. That is the single
most dangerous thing on this problem and the authoring got it right on every crop.

---

## 2. ONION THRIPS -- a content problem (leek, onion, shallot)

The record says: *"Keep plants vigorous and watered, hose off light infestations, use reflective
mulch, and rotate away from alliums."* Four of those five claims could not be sourced.

| claim | verdict |
|---|---|
| rotate away from alliums **for thrips** | **NOT SUPPORTED.** UC IPM `/thrips/` uses "rotation" only for insecticide mode-of-action. Clemson's four-year rotation sentence sits inside its *disease* paragraph. |
| reflective mulch | **NOT SUPPORTED.** The word "mulch" does not appear on UC IPM's thrips page; "reflective" absent from Clemson. |
| hosing thrips off | **NOT SUPPORTED as hand-hosing.** UC IPM has only *"Overhead irrigation and rainfall suppress thrips numbers, but pesticide applications are often still necessary"* -- and carries its own hedge. |
| vigor / even watering | **NOT SUPPORTED.** "stress", "vigor", "drought" absent from UC IPM's page. |
| sheltering where sprays miss | **SUPPORTED.** UC IPM: *"Thorough coverage is essential for control, as most thrips feed in protected areas of the plant."* |

**ACTION:** this needs a decision, not a repoint. Either search further (Cornell and PSU publish
onion thrips guidance not yet read) or soften the record to what can be carried.

**NOTE, unshipped-vs-shipped:** garlic already ships a `reflective_mulch` rung for onion thrips
citing UMN growing-garlic and USU. Those two documents were **not** read in this pass. If reflective
mulch is unsupportable, that is a shipped defect too, and the check belongs on garlic's sources.

---

## 3. PINK ROOT -- repoint, and drop one claim (leek, onion, shallot)

Current anchor for onion and shallot is a Texas A&M **commercial onion** PDF whose entire pink-root
content is one table row: `Pink root | 1,3-Dichloropropene`. Leek's anchor (UF/IFAS HS1388) has one
sentence, about dipping transplant roots in garlic extract -- advice the dataset does not carry.

| claim | verdict |
|---|---|
| rotation "several years" | **SUPPORTED BUT CONTESTED.** UC IPM: *"Rotating to non-Allium crops for 3 to 6 years can reduce the incidence of pink root."* But NMSU: *"Crop rotation is not highly effective in controlling pink root"*; USU: *"crop rotation does not have an effect on the disease."* |
| clean / disease-free planting stock | **UNSUPPORTED IN EVERY DOCUMENT READ.** Pink root is soilborne; clean-stock is the *white rot* rule, which this same leek record cites correctly elsewhere. Reads as a claim that migrated across entries. |
| stress worsens it | **SUPPORTED.** UC IPM: *"Wounds are not necessary for infection, and weak plants are more susceptible."* |
| warm soil | **SUPPORTED as temperature, not soil temperature.** UC IPM: *"Optimal temperatures for disease development are 75° to 85°F."* USU says the same range; NMSU gives soil temperature explicitly. |
| applies to leek | **NOT ESTABLISHED.** The word "leek" does not appear on UC IPM's pink root page; it says *"Pink root is primarily a problem on onion."* No US leek-scoped document found. |

**ACTION:** repoint to UC IPM `/pink-root/` + USU, cited honestly as onion documents. **Drop the
clean-stock claim.** Carry the rotation caveat. Reconsider severity on leek.

---

## 4. CHIVES APHIDS -- the cited page asserts the opposite

`hort.extension.wisc.edu/articles/chives-allium-schoenoprasum/` says: *"Chives have no significant
insect or disease problems and are not favored by deer or rabbits."* Zero occurrences of "aphid".
UMN growing-chives has no pest section at all.

Three further documents that **enumerate** chives problems omit aphids entirely: USU *Chives in the
Garden* (thrips, root maggot, pink root, downy mildew), NC State Plant Toolbox (*"No serious
problems"*), PlantVillage. And aphids are not treated as an allium pest generally: **UC IPM's onion
and garlic guidelines have no aphid page at all.**

Aphids on chives are real (onion aphid *Neotoxoptera formosana* is an Allium specialist) but the
only chives-specific text is sub-T1: UC Marin Master Gardeners (*"Black aphids can be a problem"*)
and Ask Extension diagnoses.

**ACTION:** the Wisconsin citation is worse than dead -- it contradicts the entry it anchors. Remove
both URLs. Then decide: demote to low severity on sub-T1 sourcing, or drop the entry.

---

## 5. CHIVES BOTRYTIS -- two different fungi in one entry

The entry is named *"Botrytis (leaf blight and neck rot)"*. **These are different organisms**:
leaf blight is *Botrytis squamosa*, neck rot is *B. allii / B. aclada* (Purdue BP-23; USU; UC IPM
carries them as two separate pages). Every field in the entry describes the foliar disease.

Worse, **their spacing advice points in opposite directions**: UC IPM for leaf blight says *"Plant
with single row spacing at least 12 inches apart"*; Purdue for neck rot says *"close plant spacing
(12 plants per foot)"*.

The document for the foliar disease exists: UC IPM `/botrytis-leafspot/` supports crowding
(*"Poor air circulation in the onion canopy also favors the disease"*) and leaf wetness (*"Leaf
surfaces must be wet from dew or rain for long periods (20 or more hours)"*). It does **not**
support in-season removal of senescing leaves -- "remove", "older leaves", "senescing" are all
absent.

**ACTION:** rename the entry to Botrytis leaf blight (or split it), repoint to
`/botrytis-leafspot/`, and drop the in-season leaf-removal claim. This confirms and sharpens open
finding #2 in the alliums handoff.

---

## 6. CHIVES RUST -- a US document supports all three disputed claims

UC IPM `/rust/` does **not** support crowding, nitrogen, spacing or in-season leaf removal; its
entire management section is rotation 2-3 years, field separation, destroying volunteers, and
well-drained soils. (It does support humidity: *"Optimal conditions for infection occur around 59ºF
with 100% relative humidity for at least 4 hours."* And it names chives: *"In addition to garlic,
onion and chives can be affected severely."*)

**But the PNW Plant Disease Management Handbook garlic-rust page supports all three**, verbatim:
> *"Avoid dense plantings which favors disease."*
> *"Avoid over application of nitrogen, which enhances infections."*
> *"Avoid wetting of the leaves."*

**LIVENESS NOTE:** `pnwhandbooks.org` returns **403 to every ordinary fetch**, including mine. It is
NOT dead -- one researcher read it through a text-extraction proxy. Anyone re-verifying this with a
naive fetch will wrongly call it dead. The dataset already cites this handbook elsewhere.

**ACTION:** add the PNW garlic-rust page. Keep UC IPM for the chives-susceptibility sentence.

---

## 7. LEEK MOTH -- factually wrong for a US audience

Sole source is RHS (British). The record says two generations feeding *"May to June and August to
October"* and tells the reader to net *"during late spring and late summer"*.

| finding | evidence |
|---|---|
| **Those are LARVAL FEEDING months, not flight months.** RHS publishes no adult-flight months at all. | RHS: *"two generations during the summer with larvae feeding on the plants in May to June and August to October."* |
| **The US has 2-3 generations, not 2.** | Cornell: *"There are 2 to 3 generations per year in New York."* UNH: *"There are three generations of this pest."* |
| **US flights are mid-April to mid-August; injury June to September.** The record's August-October tail matches no US source. | Cornell: three flights, *"mid-late April"*, *"mid-June... early to mid-July"*, *"late July... mid- to late August"*. |
| **The netting advice is actively wrong.** | Cornell: *"It is important to have the row cover in place over the crop before the moths emerge from their overwintering sites in spring"* and *"Moths may emerge extremely early during warm spells in March."* Netting in May-June is after the first flight. |
| **The entry misreads its own source.** | RHS: *"The mesh should be kept in place for the entire growing season."* |
| **Geographic scope is missing.** | In the US the insect is confined to northern NY and northern New England. |

**ACTION:** replace RHS with Cornell (`rvpadmin.cce.cornell.edu/uploads/doc_764.pdf`) and UVM's 2022
fact sheet. Rewrite timing to the 50°F emergence anchor. Scope it geographically.

---

## 8. LEEK ALLIUM LEAFMINER -- cover-during vs cover-before

Leek's window (*"March to April and September to November"*) and its *"the autumn generation is
usually the most damaging"* are **RHS's sentences**: *"Peak adult activity is March to April and
September to November"*, *"this generation is usually the most damaging"*.

Its US citation is `growing-leeks-home-garden`, which **contains zero allium leafminer flight
dates** -- its whole pest section is a bare link to the dedicated page that chives and shallot
already cite.

"Two generations" is correct (unanimous across UMD, NCSU, Cornell, UMass). The window is not: US
sources give spring **late March-April** and fall **September-October**.

**The cover instruction is wrong in the same way as leek moth.** Every US source says cover
*before*: UMD *"Covering plants in February, prior to the emergence of adults"*; Cornell *"before
the flight period starts"*; NCSU *"installed before flies emerge"*. And UMass has direct leek
evidence: *"Waiting to cover leeks two weeks after the start of ALM's fall flight has been shown to
result in higher densities of ALM larvae and pupae."*

**ACTION:** repoint to UMD `allium-onion-leafminer` + Cornell IPM. Change cover-during to
cover-before. Align the window with chives and shallot.

---

## 9. LEEK RUST -- probably not a US leek problem

The record carries severity **high**, *"common from mid-summer into late autumn"*, and *"spreads in
damp, humid weather"*.

| finding | evidence |
|---|---|
| **US sources say leek is comparatively resistant.** | UC IPM: *"Leek, elephant garlic, and shallot are more resistant."* UMaine: *"Leeks, shallots, and elephant garlic have not been found to be susceptible to rust strains present in North America."* |
| **The leading US regional guide does not list rust as a leek disease.** | New England Vegetable Management Guide, leek: damping-off, downy mildew, purple blotch, white rot. |
| **The weather framing is inverted.** | UC IPM: the pathogen is a **cool-weather** organism, *"between 57º and 75ºF"*, optimum 59ºF. "Mid-summer into late autumn, damp and humid" is the UK calendar. |
| **The variety advice upgrades a supplier claim into a recommendation.** | RHS says only *"Suppliers sometimes claim a degree of resistance for certain varieties"*. |
| **The US citation is decorative.** | HS1388's entire rust content is two sentences, and its one actionable item (clover intercropping) is absent from the dataset. |

Compare the roster: garlic rust ships at severity **low**; chives rust has no severity. Leek at
**high** is the outlier, and it is the UK-sourced one.

**ACTION:** downgrade severity, invert the weather framing, drop the variety recommendation, or drop
the entry. This is a judgment call for Trevor.

---

## 10. SHALLOT DOWNY MILDEW -- "tolerant varieties" sends the reader after nothing

| claim | verdict |
|---|---|
| tolerant varieties | **FACTUALLY WRONG.** UC IPM: *"There are also currently a few red onion cultivars (for example, Calred) that are resistant to downy mildew, but this resistance is active only in the flower stalks and not the leaves."* That is **resistant** not tolerant, **red onion** not shallot, and **not in the leaves**, which is where a gardener sees it. The word "tolerant" appears in none of four allium downy mildew documents read. |
| removing infected debris | **SUPPORTED, wrong citation.** UC IPM: *"Remove and destroy material of any Allium plants, including residue from the previous crop, volunteer plants, and culls from storage."* -- and in the same list, *"Use a 3-year rotation away from Allium crops"*, so the rotation-plus-debris pairing the record claims is real, just not on the USU page. |
| spread mechanism | **WRONG.** The dataset describes splash dispersal. UC IPM: *"Spores are airborne."* Purdue: *"wind-dispersed spores"*. UW-Madison leads with wind and gives splash only for secondary plant-to-plant movement. This matters: airborne means spacing and airflow, splash means mulching. |

**ACTION:** repoint to UC IPM `/downy-mildew/`. Drop the tolerant-variety claim. Fix the mechanism.

---

## Two figures, decided

**White rot persistence.** "20 to 30 years" is **fabricated** -- six documents read give 15+, over
20, over 20, 20-40, 20-40, and up to 40. None says 20-30, including both URLs cited for it. A web
search *summary* asserts "20 to 30", which is the likely route in. It appears **exactly once** in
the dataset (shallot `cause_seasoned`). **Use "over 20 years" citing UC IPM** -- it is the exact
published wording and it converges leek and shallot onto one figure.

**White rot infection threshold.** The staged leek text says *"a handful of sclerotia"*. UC IPM:
*"As few as one sclerotium per 10 kilograms of soil can initiate disease."* UMD and UMaine publish
the US-unit version directly, so no arithmetic is needed: **one sclerotium per about 20 pounds of
soil**. Sclerotia are poppy-seed sized, so "a handful" is tens of thousands -- wrong by roughly four
orders of magnitude, in the direction that *understates* the risk and undercuts the advice it is
attached to. **Do not publish a volume equivalent** ("about two gallons"); no source read states
one, and deriving it would be exactly the defect class this pass exists to catch.

---

## A separate finding, OUTSIDE batch 24, in shipped content

The Minnesota root-maggot page carries a precondition the dataset treats inconsistently:

> *"Do not place row covers if onions or other root vegetables were planted in the same area the
> previous year... Placing a row cover will trap adults that hatch from the pupae and it will no
> longer protect the plants from the flies."*

Batch 24 gets this right on all four crops. **Shipped brassica advice does not.** Of 11 shipped
row-cover rungs on soil-pupating maggots, **7 omit the warning from the beginner register** -- the
register a novice reads -- and 2 omit it from both:

| crop | beginner | seasoned |
|---|---|---|
| broccoli | **missing** | **missing** |
| bok-choy | **missing** | **missing** |
| kale | **missing** | present |
| cabbage | **missing** | present |
| kohlrabi | **missing** | present |
| brussels-sprouts | **missing** | present |
| collards | **missing** | present |
| radish, cauliflower, turnip, spring-onion | present | present |

The house pattern is established (4 crops carry it in both registers); these 7 are the gap. Filing
as its own item -- it is live consumer advice and unrelated to the alliums.

---

## What step 1 concluded

* **6 of 10** decisions are repoints, and in most the replacement document was already cited
  elsewhere in the dataset or one click from the current one.
* **4 of 10** are content defects that a citation change will not fix, and **3 of those are leek**.
* **Leek is the outlier crop by a wide margin**: 4 of its 7 problems have content defects, two of
  them give netting advice that would fail for a US gardener, and one may not be a real US leek
  problem at all. Every leek defect traces to the same structure: a British source supplies the
  substance and a US source is bolted on as cover.
* Batch 24's authoring was **faithful**; it reproduced its inputs accurately, including their
  defects. The row-cover trap precondition is the clearest case of it getting something right that
  shipped content gets wrong.

**The decision this raises:** whether to fix leek's records as part of this arc, or split it out of
batch 24 and ship chives, onion and shallot once their repoints land.
