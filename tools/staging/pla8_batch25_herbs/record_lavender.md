# PLA-8 BATCH 25 -- RECORD / SOURCE PASS: LAVENDER

Reviewer pass date: **2026-09-04**. Canonical read-only, unchanged.
Subject: `lavender.pests[]` (2 entries) + `lavender.diseases[]` (2 entries). **All four carry no
`sources` and no `anchoring_urls`.**

---

## DOCUMENTS ACTUALLY OPENED AND READ (absence findings below are scoped to exactly these)

| # | Catalog key | URL | Outcome |
|---|---|---|---|
| 1 | `wsu_ext_lavender_prcr` | https://ppo.puyallup.wsu.edu/lavender/ | READ in full (2 passes: body text, then image captions) |
| 2 | `ncsu_ext_lavandula_angustifolia` | https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ | READ |
| 3 | `ncsu_ext` (see NOTE A) | https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/ | READ in full (2 passes) |
| 4 | `usu_ext_english_lavender` | https://extension.usu.edu/yardandgarden/research/english-lavender-in-the-garden | READ |
| 5 | `csu_ext_lavender_07245` | https://extension.colostate.edu/resource/growing-lavender-in-colorado/ | READ |
| 6 | `uc_ipm` | https://ipm.ucanr.edu/home-and-landscape/lavender/ | READ (2 passes; link URLs captured) |
| 7 | `uc_ipm` | https://ipm.ucanr.edu/home-and-landscape/spittlebugs/ | READ (2 passes) |
| 8 | `uc_ipm` | https://ipm.ucanr.edu/home-and-landscape/phytophthora-root-and-crown-rot/ (Pest Notes 74133, updated 01/2025) | READ (2 passes) |
| 9 | `uc_ipm` | https://ipm.ucanr.edu/home-and-landscape/rosemary/ | READ (differential control, see §2) |
| 10 | `uc_ipm` | https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/fungal-leaf-spots-blights-and-cankers/ | READ -- lavender ABSENT |
| 11 | `rhs` | https://www.rhs.org.uk/plants/282089/lavandula-angustifolia-hidcote-group/details | READ |
| 12 | `rhs` | https://www.rhs.org.uk/biodiversity/cuckoo-spit-spittlebugs | READ |
| 13 | `umn_ext` | https://extension.umn.edu/yard-and-garden-insects/spittlebugs | READ |
| 14 | `uconn_ext` | https://ipm.cahnr.uconn.edu/wp-content/uploads/sites/3216/2022/12/2020fungusleafspotsfactsheetfinal2.pdf | PDF text extracted locally with pypdf (WebFetch could not decode it). READ -- lavender ABSENT (checked full 3-page text) |

**NOT read (do not treat as absence):**
- `https://pnwhandbooks.org/plantdisease/host-disease/lavender-root-rot` -- **HTTP 403 on every attempt**
  (also `/node/2979/print` 403). This is a live page that WebFetch cannot reach, not a dead one. It is
  the single highest-value unread document for this crop: search snippets indicate it carries the
  OSU Plant Clinic's Lavandula pathogen list and cultural controls. **Owed: a read through a client
  that gets past the block.** Nothing below is sourced to it.
- `https://agsci.oregonstate.edu/nurspest/insects/spittlebugs` -- HTTP 403.
- `https://ipm.ucanr.edu/home-and-landscape/sage/` -- HTTP 404 (UC IPM has no `sage` host page under
  that slug; Salvia lives at `https://ipm.ucanr.edu/PMG/GARDEN/PLANTS/salvia.html`). Relevant to the
  sage reviewer, not to this crop.
- `https://www.rhs.org.uk/plants/lavandula/growing-guide` -- HTTP 404. The RHS problems text lives on
  the per-cultivar `/details` pages instead (doc 11).

**NOTE A -- the NCSU New Crops key question is already settled by shipped precedent.**
`ncsu_ext` (`name`: "NC State Extension", url `https://content.ces.ncsu.edu`, citable_for: "NC State
Extension publications, a 1862 Land Grant institution") is **already used in shipped canonical as the
key for other `ces.ncsu.edu` subdomains** -- `bell-pepper.diseases[phytophthora-blight]` and
`banana-pepper` both cite `ncsu_ext` with `anchoring_urls.ncsu_ext.url =
https://vegetables.ces.ncsu.edu/peppers-diseases/`. So doc 3 is citable **today, with no catalog
addition**, as `ncsu_ext` + the specific URL in `anchoring_urls`. (A dedicated
`ncsu_ext_newcrops_lavender` key would also match the `ncsu_ext_lavandula_angustifolia` /
`ncsu_ext_bulb_onions` sub-key precedent; either is defensible, the first needs no decision.)

---

## Spittlebug [pests] -- severity low, type insect

**STATUS: UNSOURCED-FOUND**

**ORGANISM:** *Philaenus spumarius* (meadow spittlebug), Hemiptera: Aphrophoridae -- **resolved by
combining two documents, not by one.** No US extension document names a binomial *and* lavender in the
same place. `rhs` names the organism and names lavender as a host. `umn_ext` names the organism as the
common garden species on herbaceous plants. `uc_ipm` names lavender as a spittlebug host but gives no
species on the host page, and its spittlebug page names three species (*Clastoptera lineatocollis*,
*Philaenus spumarius*, *Aphrophora permutata*) without mapping any of them to a host genus. The two
non-*Philaenus* species are excluded on host grounds (*Aphrophora permutata* is the western **pine**
spittlebug; *Clastoptera* on this page is tied to woody hosts), leaving *P. spumarius* as the only
candidate for a Lamiaceae subshrub. **State this as "meadow spittlebug, *Philaenus spumarius*" only
if a combined citation is acceptable; a single-document binomial for lavender does not exist in the
sources read.**

**ANCHORS:**

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/lavender/ -- verified 2026-09-04
> Pests and Disorders > Invertebrates: "Leafhoppers", "Spider Mites", "Spittlebugs", "Whiteflies"

(UC IPM maintains a per-host pest index; lavender's Invertebrates list is exactly those four, each a
link: `/home-and-landscape/leafhoppers/`, `/spider-mites/`, `/spittlebugs/`, `/whiteflies/`. This is
UC IPM asserting spittlebugs as a lavender pest.)

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/spittlebugs/ -- verified 2026-09-04
> "Spittlebugs' obvious and occasionally abundant masses of white foam on foliage and stems may be annoying, but they do not seriously harm established woody plants in landscapes."
> "Ignore spittlebugs or wash nymphs off with a forceful stream of water. Spittlebugs are more likely to become abundant on woody plants when they migrate from nearby herbaceous hosts. Cut spittlebug-infested weeds in the spring before the insects mature and spread."
> "Overwintering occurs as tiny eggs on or in stems or needles. Spittlebugs commonly have one or two generations per year in California."
> "In certain crops spittlebugs may be important vectors of plant pathogens, such as the *Xylella fastidiosa* bacterium."
> nymphs "surround themselves with frothy white excrement beginning during the second instar", feeding on "xylem fluid"

`rhs` https://www.rhs.org.uk/plants/282089/lavandula-angustifolia-hidcote-group/details -- verified 2026-09-04
> Pests: "May be susceptible to rosemary beetle, and to cuckoo spit (froghopper or spittle bug nymphs)"

`rhs` https://www.rhs.org.uk/biodiversity/cuckoo-spit-spittlebugs -- verified 2026-09-04
> hosts: "Many plants, including chrysanthemum, dahlia, fuchsia, lavender, rosemary, rose and willow"
> "Apart from producing the 'spit' these insects have little detrimental effect on plants."
> "Usually plant growth is unaffected" ... "if the nymph has been feeding at the shoot tip, this may cause some distorted growth."
> timing row: "Most active - May-July"
> "Spittlebugs are not a pest, so please don't remove them"

`umn_ext` https://extension.umn.edu/yard-and-garden-insects/spittlebugs -- verified 2026-09-04
(field-level fragments, quoted as returned)
> "*Philaenus spumarius*" (meadow spittlebug), "the most common of 54 spittlebug species in Minnesota"
> hosts: "ornamental grasses, roses, chrysanthemums, clover, strawberries, herbs"
> "In most cases, especially on annuals and perennials, spittlebug feeding is not damaging to plants."
> eggs "can live through the winter in leaf litter"; nymphs emerge "late April or early May"; "only one generation per year"
> "Pesticides are not effective"; "Spray them with a strong blast of water to dislodge nymphs"; "Remove weeds near your gardens"

**RECORD CLAIMS THAT HOLD:**
- "Frothy white spit-like foam on stems ... with the small nymph hidden inside" -- `uc_ipm` spittlebugs ("masses of white foam on foliage and stems"; nymphs "surround themselves with frothy white excrement"); `rhs` ("Blobs of white frothy liquid").
- "in late spring" -- `rhs` "Most active - May-July"; `umn_ext` nymphs emerge "late April or early May". Holds for both registers.
- "It looks alarming but rarely harms an established lavender plant" -- `uc_ipm` "may be annoying, but they do not seriously harm established woody plants in landscapes" (lavender is a woody subshrub, the record's own archetype is `perennial_woody_ornamental`, so this sentence is on-host); `umn_ext` "not damaging to plants"; `rhs` "little detrimental effect on plants".
- "Spittlebug nymphs, which shelter inside their own foam while feeding on plant sap" -- `uc_ipm`. Note the two small imprecisions in §PRECISION below.
- "the damage is mostly cosmetic" -- all three damage statements above.
- "Knock them off with a strong spray of water" / "spray it off with a hose" -- `uc_ipm` "wash nymphs off with a forceful stream of water"; `umn_ext` "Spray them with a strong blast of water to dislodge nymphs".
- "No treatment is needed for plant health in most cases" / "You usually do not need to do anything else" -- `uc_ipm` "Ignore spittlebugs".

**RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):**
- "Numbers are usually low" -- no document says this. `uc_ipm` says the opposite is possible ("occasionally abundant masses"), and `umn_ext` discusses heavy infestations causing "leaves to lose their shape".
- "Keeping plants spaced for airflow and not overwatering keeps lavender vigorous enough to shrug off minor pests." -- no document connects lavender spacing or irrigation to spittlebug pressure. Airflow/spacing is sourced for *fungal* pathogens (`ncsu_ext` New Crops, quoted in §Leaf spot), not for this insect. This is a real (and reused) template sentence, not a sourced claim.
- "There are usually only a few, and they do little real harm." (beginner) -- second half holds, first half does not.

**RECORD CLAIMS THAT ARE WRONG:**
- **"No specific prevention is warranted."** Refuted. Both published sources give a specific cultural
  prevention step and it is not the one the record gives:
  > `uc_ipm`: "Cut spittlebug-infested weeds in the spring before the insects mature and spread."
  > `umn_ext`: "Remove weeds near your gardens"
  The record asserts no prevention exists and then supplies an unsourced one (spacing/watering). The
  sourced prevention -- weed management, timed to spring before the nymphs mature -- is missing.

**PRECISION notes (not wrong, worth tightening at authoring):**
- The foam is excrement, not a secretion the nymph builds as shelter: `uc_ipm` "frothy white
  excrement". "shelter inside their own foam" is defensible as function, not as origin.
- Feeding is on **xylem** fluid (`uc_ipm`), which is why spittlebugs produce no honeydew and no sooty
  mold. "plant sap" is acceptable common tongue; the ladder pass should not carry honeydew or
  ant-tending language across from the aphid/whitefly template.

**LADDER-RELEVANT FACTS the record does not carry:**
- **Weed management is THE published cultural rung**, and it is time-anchored: cut infested weeds in
  spring *before the insects mature* (`uc_ipm`), remove weeds near the garden (`umn_ext`).
- **`umn_ext`: "Pesticides are not effective"** -- the spittle mass shields the nymph. This caps the
  ladder at physical/cultural and is the single most useful ladder fact available; a soft-chemical or
  conventional rung on this problem would contradict a T1 source.
- Handpicking is published: `umn_ext` "Physically remove them by hand".
- Life cycle: overwinters as eggs, one generation per year in Minnesota (`umn_ext`), one or two in
  California (`uc_ipm`). **The two sources disagree on where the eggs sit** -- `uc_ipm` "on or in stems
  or needles", `umn_ext` "in leaf litter". Do not assert an overwintering site without picking a
  source and saying which.
- Natural enemies named by `uc_ipm`: birds, assassin bugs, parasitic wasps -- with the caveat that
  their importance is "not well known". A biological rung exists but the source hedges it.
- `rhs` takes an explicit **do-not-control** position: "Spittlebugs are not a pest, so please don't
  remove them". That is in tension with the record's "spray it off with a hose" and is worth one
  sentence of honest framing (cosmetic choice, not a treatment).
- `uc_ipm` *Xylella fastidiosa* vectoring: **ladder-relevant but do NOT put it in consumer copy.**
  The sentence is scoped "in certain crops", the US home-garden lavender risk is not stated anywhere,
  and `rhs` explicitly calls them "an innocent carrier of *Xylella* outside of the UK". Carrying it
  into consumer prose would manufacture alarm the sources do not support.

---

## Whiteflies and aphids [pests] -- severity low, type insect

**STATUS: SPLIT -- UNSOURCED-FOUND (whiteflies) / UNSOURCED-NOT-FOUND (aphids)**

**ORGANISM:** Whiteflies -- family Aleyrodidae; **no species resolved for lavender** by any document
read. Aphids -- **cannot be resolved; no document read places any aphid on *Lavandula*.**

**ANCHORS:**

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/lavender/ -- verified 2026-09-04
> Pests and Disorders > Invertebrates: "Leafhoppers", "Spider Mites", "Spittlebugs", "Whiteflies"

`wsu_ext_lavender_prcr` https://ppo.puyallup.wsu.edu/lavender/ -- verified 2026-09-04
> "Lavender has few pests and diseases. It is often promoted as a sustainable crop because growers do not commonly need to apply pesticides and fertilizers in its production."

`ncsu_ext` https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/ -- verified 2026-09-04
> "Few insect problems have been reported on field-grown lavender. A defoliating moth larva has been reported in Australia."

**THE APHID ABSENCE IS ADJUDICATED, NOT ASSUMED.** Eight documents were opened. Aphids appear on
*lavender* in none of them:

| Document | What it names as lavender pests | Aphids? |
|---|---|---|
| `uc_ipm` lavender host page | leafhoppers, spider mites, spittlebugs, whiteflies | **no** |
| `uc_ipm` **rosemary** host page | **aphids**, leafhoppers, spider mites, spittlebugs, thrips, whiteflies | yes, on rosemary |
| `ncsu_ext_lavandula_angustifolia` | "No significant problems. However, it is susceptible to leaf spot and root rot." | no |
| `ncsu_ext` New Crops lavender | "Few insect problems have been reported on field-grown lavender." + a defoliating moth larva (Australia) | no |
| `usu_ext_english_lavender` | grasshoppers, browsing deer | no |
| `csu_ext_lavender_07245` | grasshoppers, browsing/trampling deer or elk | no |
| `wsu_ext_lavender_prcr` | "few pests and diseases" | no |
| `rhs` L. angustifolia details | rosemary beetle, cuckoo spit | **no** (checked explicitly: neither "aphid" nor "whitefly" appears on the page) |

The `uc_ipm` lavender/rosemary pair is the decisive one: **UC IPM's own host index lists Aphids on
rosemary and omits them from lavender.** That is a deliberate host-list difference by the same editor
on two Lamiaceae subshrubs, not an oversight. Aphids on lavender is not a hunt that failed for want of
looking; it is an assertion the literature declines to make.

**RECORD CLAIMS THAT HOLD:**
- Whiteflies occur on lavender -- `uc_ipm` lavender host page.
- "Lavender has few pests overall and is typically grown with little or no pesticide." -- `wsu_ext_lavender_prcr`, near-verbatim; also `ncsu_ext` New Crops "Few insect problems have been reported on field-grown lavender." **This is the best-anchored sentence in the whole entry.**

**RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):**
- "**or soft aphids**" / "**Whiteflies and aphids**" (the name itself) / "Now and then, tiny white flies **or small soft bugs**" -- the entire aphid half.
- "most likely on stressed or overcrowded plants in poor conditions rather than on healthy lavender" -- no document read makes a stress-susceptibility claim for lavender.
- "Rinse them off with water or use insecticidal soap if numbers climb." -- generic and almost certainly anchorable at `uc_ipm` Pest Notes 7401 (Whiteflies), which was **not read in this pass**. Flag as anchorable-but-unread rather than unsupported.
- "Removing nearby stressors and improving airflow usually resolves it."
- "Give plants full sun, lean soil, and good spacing, and avoid overwatering. Vigorous, unstressed lavender rarely attracts these pests." -- the horticultural half (sun, lean soil, drainage, 2-3 ft spacing) is independently sourced; the *causal link to pest pressure* is not.

**RECORD CLAIMS THAT ARE WRONG:**
- None demonstrably false. But the entry is **incomplete against its own best source**: `uc_ipm` names
  four lavender invertebrates and the record carries two of them. **Leafhoppers and spider mites are
  missing from `lavender.pests[]` entirely.** Given `uc_ipm` is the only host-indexed pest source for
  this crop, that is a roster gap worth surfacing before the ladder pass, not after.

**ONE PROBLEM OR TWO? (for the later id pass -- reporting, not acting)**
- **The sources treat them as two.** `uc_ipm` indexes each pest under its own page; on rosemary it
  lists "Aphids" and "Whiteflies" as two separate entries. No document read treats "whiteflies and
  aphids" as a single lavender problem.
- **Their management on lavender does not differ**, which is why they were bundled: both resolve to
  water-rinse then insecticidal soap, and the record's treatment cell is identical for both.
- Existing ids: `whiteflies` on 5 crops (roma-tomato, grape-tomato, english-cucumber, nasturtium,
  calendula); `aphids` on 59 crops. Both are established, both are un-scoped generics -- so a split
  would reuse two existing ids cleanly with **no minting and no taxon check needed** (unlike
  `pea-weevil`-class scope traps, since neither generic is species-pinned).
- **But the split is not the recommendation, because the aphid half has no source.** Two honest
  options for the ladder pass, both reportable rather than decidable here:
  (a) rename the entry to `Whiteflies` and point it at `whiteflies` -- fully sourced, drops an
      unsupported claim; or
  (b) keep the bundle and accept that half of it is unanchored -- which is exactly the defect class
      this pass exists to prevent.
  There is a third, better option if the ladder pass wants a two-pest entry that is *true*: replace
  the aphid half with **leafhoppers or spider mites**, both of which UC IPM does list for lavender.
- Note the **name-order divergence** with rosemary: lavender says "Whiteflies and aphids", rosemary
  says "Aphids and whiteflies", for prose that is otherwise a near-verbatim template twin. Whatever
  the ladder pass decides, the two crops should not end up with the same problem under two different
  names and two different ids.

---

## Phytophthora root and crown rot [diseases] -- severity high, type fungal

**STATUS: UNSOURCED-FOUND**

**ORGANISM:** Umbrella -- **multiple *Phytophthora* species** (oomycetes / water molds, not fungi).
Binomials reported on *Lavandula*:
- ***Phytophthora nicotianae*** -- per `wsu_ext_lavender_prcr`'s own publication list ("Root rot of
  lavender caused by *Phytophthora nicotianae*", M. Putnam, 1991, British Society for Plant Pathology,
  doi:10.1111/j.1365-3059.1991.tb02408.x) and per `ncsu_ext` New Crops's pathogen list
  ("*Phytophthora nicotianae* -- root rot").
- ***Phytophthora* spp.** causing wilt -- `ncsu_ext` New Crops ("*Phytophthora spp.* -- wilt").
- **Six *Phytophthora* species across three *Lavandula* species** -- Dlugos, Bridges & Jeffers
  (Clemson), "Phytophthora Root and Crown Rot of Lavender: New Host-Pathogen Relationships Involving
  Six Species of Phytophthora and Three Species of Lavandula", linked from the WSU page and published
  in APS *Plant Disease*. **JOURNAL-ONLY for the species list** -- WSU hosts the PDF and links it, but
  the WSU page itself never names the six species in its own prose, so the WSU anchor carries "many
  species", not the enumeration.

**`type: "fungal"` is taxonomically wrong but matches dataset convention.** *Phytophthora* is an
oomycete; the record's own `cause_seasoned` correctly says "Water mold pathogens", so the record
contradicts its own `type` field. However **all 16 existing *Phytophthora* entries in canonical are
typed `fungal`** (blueberry, raspberry, blackberry, 4 citrus, 6 pepper/eggplant/pumpkin, strawberry
red stele), and the disease `type` enum in use is {fungal, bacterial, viral, disease, physiological,
nematode, other} with no water-mold value. **Leave `fungal`.** Recorded here so it is a known,
deliberate convention rather than a defect someone re-finds.

### PRIORITY ITEM 1 -- exactly what `wsu_ext_lavender_prcr` does and does not carry

**ANCHOR:** `wsu_ext_lavender_prcr` https://ppo.puyallup.wsu.edu/lavender/ -- verified 2026-09-04

The page **DOES** carry, verbatim:
> "Lavender has few pests and diseases. It is often promoted as a sustainable crop because growers do not commonly need to apply pesticides and fertilizers in its production. However, recently growers have been reporting plants with symptoms of *Phytophthora* root and crown rot (PRCR)."
> "On this webpage, we aim to share information about PRCR of lavender and provide resources for managing the disease."
> "*Phytophthora* species are microscopic organisms that cause disease in plants. Many species have been identified as the primary causes of root and crown rot of their host plants."

and, in image captions only:
> "a lavender bunch. the interior shoots are all dead and the shoots around the outside are pale green with their flowers drooping"
> "Potted lavender plant with large flowers. one shoot is dead"
> "symptomatic field of lavender planted through a striped black ground cloth"

So the WSU page supports, on its own: (a) lavender has few pests and diseases and is grown with little
pesticide; (b) PRCR is the disease growers are reporting on lavender -- the disease of concern;
(c) *multiple* *Phytophthora* species cause root and crown rot; (d) a visual symptom picture of whole
shoots dying and outer shoots going pale with drooping flowers.

The page **DOES NOT** carry any of the following, and I checked for each explicitly:
- **any statement about wet conditions, drainage, soil saturation, or irrigation.** The record's
  "tied to wet conditions and poor drainage" and "Wet feet, not cold, is the underlying cause" are
  **not on this page.** It links out to a nursery BMP hub
  (`http://ppo.puyallup.wsu.edu/education/nursery/`) and to a USLGA "Soil Preparation for Lavender"
  page, and states nothing itself.
- **yellowing leaves** -- the captions give pale green and drooping, not yellowing.
- **a darkened or decayed crown at the soil line** -- absent.
- **"there is no cure" / removing and discarding affected plants** -- absent. The page never
  discusses roguing.
- **any severity, mortality, or "main disease that kills lavender" statement.**
- **any other lavender disease.** Its "Other Diseases and Pests of Lavender" heading carries exactly
  one item, and that item is a *Phytophthora* fungicide article (HortScience,
  doi:10.21273/HORTSCI18302-24). **The WSU Puyallup site publishes nothing on lavender leaf spot,
  shab, Botrytis or viruses.** (Answering the "check whether WSU covers other lavender diseases" ask:
  it does not.)

**Verdict on priority item 1:** yes, anchor `diseases[0]` to `wsu_ext_lavender_prcr` -- it is the
correct, already-admitted, lavender-specific document and its `citable_for` already describes exactly
this. **But WSU alone anchors roughly a third of the entry.** The drainage causation, the prevention
cell and the "no cure, remove it" treatment cell all need `uc_ipm` PN 74133 plus the two lavender
fact sheets below. Anchoring to WSU and stopping would leave the entry looking sourced while its
load-bearing claims are not -- the exact failure mode this brief exists to prevent.

**SUPPORTING ANCHORS:**

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/lavender/ -- verified 2026-09-04
> Plant Diseases: "Phytophthora Root and Crown Rot" (the **only** disease listed for lavender)

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/phytophthora-root-and-crown-rot/ (Pest Notes 74133, updated 01/2025) -- verified 2026-09-04
> "Avoid prolonged saturation of the soil or standing water around the base of trees or other susceptible plants."
> "Avoid planting susceptible species on poorly drained, compacted, or shallow soils"
> "If it is possible to modify site soils, improve soil drainage before planting."
> "The mounds should be 8 to 10 inches high for annuals and up to 2 feet high with a gradual slope for trees and perennials."
> "A plant with a substantial Phytophthora infection rarely recovers."
> "Select certified nursery stock and resistant rootstocks or varieties when available."
> "However, do not rely on pesticide applications alone to control Phytophthora root and crown rot diseases."

`csu_ext_lavender_07245` https://extension.colostate.edu/resource/growing-lavender-in-colorado/ -- verified 2026-09-04
> "Lavender has very few pest or disease problems, but it is susceptible to soil diseases such as Phytophthora."
> "Do not over-water or allow water to stand around plants."
> Quick Facts: "Lavender has no major pests in Colorado but can develop root rot if drainage is insufficient."

`usu_ext_english_lavender` https://extension.usu.edu/yardandgarden/research/english-lavender-in-the-garden -- verified 2026-09-04
> "Lavender has few pest or disease problems, but is susceptible to soil diseases such as Phytophtora root rot." *(the page's own spelling of the genus, reproduced as printed)*
> "Do not overwater or let water stand around the plants."

`ncsu_ext_lavandula_angustifolia` https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ -- verified 2026-09-04
> "No significant problems. However, it is susceptible to leaf spot and root rot."
> "Root rot is caused by overwatering."

`ncsu_ext` https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/ -- verified 2026-09-04
> "The most common disease problem with lavender is wilt. Vascular wilts are very destructive diseases with typical symptoms characterized by rapid wilting, browning, and dying of leaves and succulent shoots of plants followed by the death of the plant."
> "English lavender varieties are more susceptible to vascular wilts than lavandin varieties. Dark-flowered cultivars are less resistant to disease than the pale-flowered varieties. Cultivars with gray foliage are quite susceptible to infection."
> "Vascular wilts are most common in the month of August when temperatures reach 90° F and humidity reaches 90%. If damaged plants are present, remove and destroy any infected plant material and avoid replanting with susceptible varieties."
> "Dr. A. O. Tucker advises using one to two inches of white sand as a mulch around plants to reduce fungal pathogen infection."
> "Avoid heavy organic mulches (sawdust, wood chips) as they can increase both fungal pathogens and insect problems."
> "Prepare the site by mixing compost or peat moss with the top four inches of soil and preparing a raised bed."
> "Lavender grows best in light soil, sand, or gravel, in a dry, open and sunny position. It requires good drainage and prefers a warm, well-drained loam with a slope to the south or southwest."

**RECORD CLAIMS THAT HOLD:**
- "It is the disease of concern for lavender" -- `wsu_ext_lavender_prcr` (growers reporting PRCR; the
  whole page exists for it) + `uc_ipm` (the sole disease on lavender's host page). See the tension
  note below.
- "Wilting, and dieback that does not recover with watering" -- `wsu` captions (whole shoots dead,
  outer shoots pale with drooping flowers) + `ncsu_ext` New Crops ("rapid wilting, browning, and dying
  of leaves and succulent shoots ... followed by the death of the plant").
- "Water mold pathogens" -- `wsu_ext_lavender_prcr` ("*Phytophthora* species are microscopic
  organisms...") + the genus's own biology; the phrase itself is the record's, and it is correct.
- "thrive in saturated, poorly drained soil and attack the roots and crown" -- `uc_ipm` 74133
  ("Avoid prolonged saturation of the soil or standing water"; "Avoid planting susceptible species on
  poorly drained, compacted, or shallow soils") + `csu` ("root rot if drainage is insufficient") +
  `ncsu` toolbox ("Root rot is caused by overwatering").
- "severity: high" -- supportable via `ncsu_ext` New Crops ("followed by the death of the plant") and
  `uc_ipm` 74133 ("A plant with a substantial Phytophthora infection rarely recovers"). No
  lavender-specific document states lethality outright; this is a two-document inference and should be
  recorded as such.
- "Plant in sharply drained soil in full sun, water deeply but infrequently" -- `csu`, `usu`, `ncsu`
  New Crops ("light soil, sand, or gravel, in a dry, open and sunny position", "requires good
  drainage").
- "On clay, use a mound or raised bed" -- `uc_ipm` 74133 mound heights + `ncsu` New Crops ("preparing
  a raised bed").
- "never let lavender sit in wet ground" -- `csu` "Do not over-water or allow water to stand around
  plants"; `usu` "Do not overwater or let water stand around the plants".

**RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):**
- "**Yellowing, wilting**" / "**Leaves yellow**" -- no lavender document read describes yellowing.
  WSU's captions say pale green; `uc_ipm` 74133 says foliage "may turn dull green, yellow, or in some
  cases red or purplish", but that page is about trees, shrubs and vegetable crops generally, not
  lavender. Anchorable only to the generic page.
- "**often with a darkened, decayed crown at the soil line**" / "**a dark, rotted spot where the stems
  meet the ground**" -- the only support is `uc_ipm` 74133's "darkened areas in the bark around the
  crown and upper roots", which is a description of woody **trees** with bark. Nothing lavender-specific.
- "**There is no cure once the crown is rotting; remove and discard affected plants.**" -- the nearest
  sourced sentences are `uc_ipm` 74133 "A plant with a substantial Phytophthora infection **rarely
  recovers**" and `ncsu_ext` New Crops "**If damaged plants are present, remove and destroy any
  infected plant material** and avoid replanting with susceptible varieties" -- but that NCSU sentence
  is inside the **vascular wilt** paragraph, not the root-rot one. So the removal advice is
  anchorable, obliquely; the **absolute** "there is no cure" is not.
- "Wet feet, not cold, is the underlying cause." / "The real cause is wet soil, not cold weather." --
  a rhetorical contrast no document makes. Not refuted, but it is the record asserting what the
  literature does not say.
- "**and space plants for airflow**" (inside the Phytophthora prevention cell) -- spacing IS sourced
  (`ncsu` New Crops, 2-3 ft), but it is sourced **for foliar fungal pathogens**, explicitly via air
  circulation. Air circulation does nothing for a soil-borne water mold. This is a claim attached to
  the wrong problem; it belongs in the leaf-spot entry, where it already correctly appears.

**RECORD CLAIMS THAT ARE WRONG:**
- **"There is no cure"** overstates `uc_ipm` 74133's "rarely recovers" into an absolute. This is the
  safety-absolute pattern: an absolute in consumer copy that the source hedges. Recommend
  "rarely recovers" / "a plant that far gone rarely comes back".
- **"This is the main disease that kills lavender"** (beginner) -- an absolute the sources support in
  spirit but not in words, and it sits in direct tension with `ncsu_ext` New Crops: **"The most common
  disease problem with lavender is wilt."** The tension is partly nominal (NCSU's own pathogen list
  puts "*Phytophthora spp.* -- wilt", so its "wilt" bucket includes *Phytophthora*), but the record
  should not assert a rank claim that a T1 document words differently. Recommend softening to "the
  disease most likely to kill an established lavender".

**LADDER-RELEVANT FACTS the record does not carry:**
- **Two lavender-specific mulch rungs, both from `ncsu_ext` New Crops, both genuinely actionable and
  both absent from the record:** "Dr. A. O. Tucker advises using one to two inches of white sand as a
  mulch around plants to reduce fungal pathogen infection." and "Avoid heavy organic mulches (sawdust,
  wood chips) as they can increase both fungal pathogens and insect problems." The second is a
  *contra-indication* against advice most gardeners default to.
- **A resistance/varietal signal:** `ncsu_ext` New Crops -- English lavender more susceptible to
  vascular wilt than lavandin; dark-flowered cultivars less resistant than pale-flowered; gray-foliage
  cultivars "quite susceptible". If `varieties[].resistance` is ever populated for lavender this is the
  source, and it is a real differentiator (English vs lavandin is exactly the split the record's
  `varieties[]` already uses).
- **A weather/timing trigger:** `ncsu_ext` New Crops -- vascular wilts "most common in the month of
  August when temperatures reach 90° F and humidity reaches 90%". The record's
  `weather_triggers[1]` already fires on humid heat; this is the sentence that would anchor it.
- **A clean-stock rung:** `uc_ipm` 74133 "Select certified nursery stock and resistant rootstocks or
  varieties when available." Nursery stock is a documented pathway for lavender specifically
  (the PNW handbook reportedly records *P. nicotianae* from nursery stock -- **unverified, that page
  is 403**).
- **A conventional rung exists and is hedged:** `uc_ipm` 74133 lists fosetyl-al (Aliette),
  phosphorous-acid products and mefenoxam for ornamentals, with "do not rely on pesticide applications
  alone". If a conventional rung is authored, the caveat sentence must ride with it.
- **A diagnostic rung:** `wsu_ext_lavender_prcr` -- "Diagnostic services are available from the WSU
  Plant and Insect Diagnostic Laboratory" plus a published DIY sampling guide for testing your own
  plants for PRCR. A real monitoring step, lavender-specific, unique to this crop.
- **Irrigation rule:** `uc_ipm` 74133 -- let the top few inches of soil dry thoroughly between
  waterings; keep the root crown and graft union uncovered by soil or mulch.

---

## Leaf spot [diseases] -- severity low, type fungal

**STATUS: UNSOURCED-FOUND** (anchorable at T1 with no catalog addition -- see NOTE A)

**ORGANISM:** As the record uses it: **umbrella -- multiple organisms.** As US extension literature
resolves it: exactly one binomial is published on *Lavandula*, ***Septoria lavandulae***, per
`ncsu_ext` New Crops. Full evidence and the ruling recommendation in the next section.

**ANCHORS:**

`ncsu_ext` https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/ -- verified 2026-09-04
> pathogen list entry: "*Septoria lavandulae* -- leaf spot"
> "In order to discourage fungal pathogens, good air circulation is advised and can be achieved by spacing plants 2-3 feet apart and trimming the lower branches throughout the growing season."
> "Avoid heavy organic mulches (sawdust, wood chips) as they can increase both fungal pathogens and insect problems."

`ncsu_ext_lavandula_angustifolia` https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ -- verified 2026-09-04
> "No significant problems. However, it is susceptible to leaf spot and root rot."
> "Root rot is caused by overwatering. Providing good air circulation helps prevent leaf spot."

`rhs` https://www.rhs.org.uk/plants/282089/lavandula-angustifolia-hidcote-group/details -- verified 2026-09-04
> Diseases: "May be susceptible to honey fungus, grey moulds, lavender shab, and fungal leaf spots"

**RECORD CLAIMS THAT HOLD:**
- "Small spots or blotches on the foliage" -- the *existence* of leaf spot on lavender:
  `ncsu_ext_lavandula_angustifolia` ("susceptible to leaf spot") and `rhs` ("fungal leaf spots"). The
  spot morphology itself is generic and unanchored on this host (see below).
- "Foliar fungi" / "Leaf fungi" -- `rhs` "fungal leaf spots"; `ncsu_ext` New Crops names a fungal
  genus (*Septoria*).
- "It is a minor issue compared with root and crown rot." -- `ncsu_ext_lavandula_angustifolia` "No
  significant problems", and every lavender document read that ranks diseases ranks root rot or wilt
  first, never leaf spot. Holds.
- "improve airflow" / "Good airflow is the main defense" -- **`ncsu_ext_lavandula_angustifolia`
  verbatim: "Providing good air circulation helps prevent leaf spot."** This is a direct, on-host,
  same-claim sentence.
- "**Space plants at least 2 to 3 feet apart for air circulation**" -- **`ncsu_ext` New Crops
  verbatim: "spacing plants 2-3 feet apart"**, and for exactly this reason ("In order to discourage
  fungal pathogens, good air circulation is advised"). Exact numeric match.
- "site in full sun" -- `ncsu_ext` New Crops ("a dry, open and sunny position").
- "The annual cut-back also helps clear and renew the canopy." -- adjacent support: `ncsu_ext` New
  Crops pairs air circulation with "trimming the lower branches throughout the growing season". Not
  the same operation as the annual hard cut-back, so this is *adjacent*, not carried.

**RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):**
- "more likely in humid weather" / "more likely in damp weather" -- reasonable and true of leaf spots
  generally, but **no lavender document read states it.** (`ncsu_ext` New Crops does give a humidity
  threshold -- 90 °F / 90% humidity in August -- but for **vascular wilt**, not leaf spot. Do not
  move that number onto this entry.)
- "on crowded, poorly ventilated plants" -- the *remedy* is sourced (air circulation); the *risk
  factor* phrased this way is not stated on-host, though it is the obvious inverse.
- "**Crowding and overhead watering raise the risk.**" / "**water at the base rather than overhead**"
  / "**avoid overhead watering**" -- **no lavender document read mentions overhead watering at all.**
  Not one of the six lavender-specific sources. It is sound generic leaf-spot practice (`uc_ipm`
  floriculture: "Avoid using overhead sprinkler irrigation"; `uconn_ext`: "Water early in the day so
  that leaves dry by nightfall") but **both of those documents were read and neither mentions
  lavender** (checked explicitly, see the document table). Anchorable only as a cross-host generic.
- "Remove affected foliage" / "Pick off the spotted leaves" -- generic sanitation; `uconn_ext` has
  "Clean up diseased leaves in the fall to help remove overwintering spores", again with no lavender
  mention.

**RECORD CLAIMS THAT ARE WRONG:**
- **None.** The record's leaf-spot prose survives. Its two load-bearing specifics (air circulation as
  the defense, 2 to 3 feet of spacing) are the two best-anchored sentences in it, both matching NC
  State verbatim. The unanchored parts are generic-but-plausible, not false.

**LADDER-RELEVANT FACTS the record does not carry:**
- The mulch contra-indication again: `ncsu_ext` New Crops "Avoid heavy organic mulches (sawdust, wood
  chips) as they can increase both fungal pathogens and insect problems", and the white-sand mulch
  positive ("one to two inches of white sand as a mulch around plants to reduce fungal pathogen
  infection"). Lavender-specific, cultural, and absent from the record.
- "trimming the lower branches throughout the growing season" (`ncsu_ext` New Crops) -- a distinct,
  in-season physical rung the record does not have; its cut-back sentence is about the annual hard cut.
- Generic leaf-spot rungs that would need a cross-host citation: sanitation of fallen leaves, watering
  early in the day, no overhead irrigation, disease-free propagation material (`uconn_ext`, `uc_ipm`
  floriculture).
- **No fungicide is recommended for leaf spot on lavender by any source read**, and lavender's
  strongest source says growers "do not commonly need to apply pesticides" (`wsu_ext_lavender_prcr`).
  A soft-chemical or conventional rung on this problem would be inventing pressure the literature
  does not report.

---

## §4f RULING EVIDENCE

**The question: is lavender's `Leaf spot` an umbrella by intent, or one organism nobody pinned?**

### Answer: it is an umbrella in the record and in the record's actual source, and pinning it to one organism would over-claim.

**1. The record's leaf-spot entry descends from a source that is itself bare.** The record's regional
prose says where it came from, in the record's own words:
`regions.mid_atlantic.region_notes_seasoned`: "NC State's own profile of the species names root rot
from overwatering and leaf spot as the main threats." That profile is
`ncsu_ext_lavandula_angustifolia`, and its entire statement is:
> "No significant problems. However, it is susceptible to leaf spot and root rot."
> "Root rot is caused by overwatering. Providing good air circulation helps prevent leaf spot."

No organism, no symptom description, no genus. **The bareness is inherited from the source, not
introduced by the authoring pass.** (Related: `verification_status.open_findings[5]` already records
that the parallel Mid-South sentence carried a **false UAEX credit**, removed 2026-07-31, and that the
NC State number was retained unattributed. The mid_south `region_notes_seasoned` still reads "the
University of Arkansas's own profile of the species names root rot from overwatering and leaf spot as
the main threats" -- **that sentence still credits UAEX for the leaf-spot claim.** Not this pass's
subject, and I have not verified whether that specific sentence was in scope of the 2026-07-31 fix,
but it is flagged because the same finding says the credit was fabricated.)

**2. What US extension literature actually reports causing leaf spot on *Lavandula*: exactly one
organism.** `ncsu_ext` New Crops (Joe-Ann McCoy 1999; updated J.M. Davis 2017, 2021, 2025) publishes
the only *Lavandula* pathogen list found at T1 in the US. Its full contents, verbatim:

| Pathogen (verbatim) | Disease (verbatim) | Is it a leaf spot? |
|---|---|---|
| *Armillaria mellea* | root rot | no |
| *Cuscuta epithymum* | Dodder vine (parasitic flowering plant) | no |
| *Fusarium* | root rot | no |
| *Fusarium solani* | wilt | no |
| *Meloidogyne incognita* | Southern Root-knot Nematode | no |
| *Phoma lavendulae* | **stem blight** | **no -- Phoma is listed, but as a STEM BLIGHT, not a leaf spot** |
| *Phytophthora nicotianae* | root rot | no |
| *Phytophthora* spp. | wilt | no |
| *Pythium* | root rot | no |
| ***Septoria lavandulae*** | **leaf spot** | **YES -- the only one** |
| *Verticillium* | wilt | no |

Taking the brief's candidate list one at a time:
- **Septoria** -- ***Septoria lavandulae***. Named as "leaf spot" on *Lavandula* by `ncsu_ext` New
  Crops. **This is the only US T1 extension document read that names a leaf-spot organism on lavender.**
  Primary description is journal: "First Report of Septoria Leaf Spot of Lavandin Caused by *Septoria
  lavandulae* in Croatia", APS *Plant Disease*, doi:10.1094/PDIS-07-13-0735-PDN.
- **Phoma** -- ***Phoma lavendulae***, present in the NCSU list but attributed to **stem blight, not
  leaf spot**. A separate, journal-only *Phoma multirostrata* leaf blight on *L. angustifolia* is
  reported from Italy (APS *Plant Disease*, doi:10.1094/PDIS-03-17-0312-PDN). **JOURNAL-ONLY, and it
  is a blight, not the record's leaf spot.**
- **Alternaria** -- **not found on *Lavandula* in anything read.** `uc_ipm`'s floriculture "Fungal Leaf
  Spots, Blights, and Cankers" page covers *Alternaria*, *Diplocarpon*, *Cercospora*, *Cladosporium*,
  *Stemphylium*, *Ovulinia* and **never mentions lavender** (checked explicitly). `uconn_ext`'s
  "Fungal Leaf Spot Diseases on Herbaceous Ornamentals" lists Alternaria leaf spot on "dahlia, gerbera
  daisy, annual vinca, geranium and zinnia" -- **lavender does not appear anywhere in its 3 pages**
  (full text extracted and searched).
- **Colletotrichum** -- **not found on *Lavandula*.** `uconn_ext` covers *Colletotrichum* anthracnose
  generally, on Phlox; no lavender.
- **Pseudomonas** -- **not found in any document I could open.** A web search surfaced the sentence
  "Lavender plants may be susceptible to lavender leaf spot (*Septoria lavandulae*) or to bacterial
  blast (*Pseudomonas syringae*) or to *Phoma* if conditions are very wet or if plants are
  overwatered", but **I could not locate that sentence in any document I actually read**, and it is
  not on the NCSU New Crops page. **Reported as an unlocated search snippet, not as evidence.** The
  nearest real bacterial leaf spot on lavender is ***Xanthomonas hortorum*** (UK), New Disease Reports
  2014, doi:10.5197/j.2044-0588.2014.030.001 -- **JOURNAL-ONLY**, not *Pseudomonas*, and the paper
  itself notes its symptoms "can be difficult to distinguish from those caused by the fungal pathogens
  *Septoria lavandulae* and *Phomopsis lavandulae*."
- **shab / Phomopsis** -- ***Phomopsis lavandulae*** (syn. *Phoma lavandulae*), "lavender shab". Named
  by `rhs` as a lavender disease ("May be susceptible to honey fungus, grey moulds, **lavender shab**,
  and fungal leaf spots"). RHS **lists shab and fungal leaf spots as two separate items**, so RHS does
  not treat shab as a leaf spot. **Shab is a UK/European stem disease; no US extension document read
  mentions it, and the WSU Puyallup lavender pathology site -- the US program that would publish it --
  publishes nothing on it.** Primary literature is 1931 (Trans. Br. Mycol. Soc.). **Out of scope for
  this record.**

**3. Can it be anchored to a catalog-admitted T1 source? YES, and with no catalog addition.**
- The **generic** claim ("lavender gets leaf spot; air circulation prevents it") anchors to
  `ncsu_ext_lavandula_angustifolia`, already in lavender's citation vocabulary, verbatim.
- The **spacing number** and the **organism**, if wanted, anchor to `ncsu_ext` +
  `https://newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/`. Per NOTE A,
  `ncsu_ext` is **already the shipped key for non-`content.` `ces.ncsu.edu` subdomains**
  (bell-pepper and banana-pepper cite `ncsu_ext` with a `vegetables.ces.ncsu.edu` URL). No new key
  required, no catalog decision blocked.
- `rhs` (already in lavender's vocabulary) carries the plural umbrella framing: "fungal leaf spots".

**4. Does the record's prose survive? YES. Nothing in it is wrong.** Details in the entry section
above. Its two specific claims -- air circulation as the main defense, 2 to 3 feet of spacing -- both
match NC State verbatim. Its unanchored parts (humid weather, overhead watering, removing spotted
leaves) are generic leaf-spot practice that no lavender document states and no lavender document
contradicts.

### RECOMMENDATION for the §4f decision

**Keep "Leaf spot" as an umbrella. Do not rename it `septoria-leaf-spot`.** Reasons, in order of weight:

1. **Pinning would over-claim.** `Septoria lavandulae` appears in a bulk pathogen list with no symptom
   description, no US distribution statement, no management, and no indication that it is what a US
   home gardener actually sees. Its published description is a first-report from Croatia. Naming the
   record's problem after it asserts far more than the one line that supports it.
2. **The record's actual source is bare, and its severity is `low`.** Every lavender document that
   ranks diseases ranks root rot or wilt first; `ncsu_ext_lavandula_angustifolia` opens with "No
   significant problems". A pinned pathogen id on a low-severity, minor problem buys nothing and
   commits the dataset to a claim it cannot defend.
3. **RHS, the other admitted source, says "fungal leaf spot**s**" -- plural, an umbrella by
   construction.**
4. This crop is not one of the 25 the six pinned siblings cover, and no `varieties[].resistance` or
   `ladder_delta` on lavender points at any leaf-spot id today, so nothing is orphaned either way.

**Suggested id, with a collision warning for the id-pinning pass:**
- Recommended: **`leaf-spot`** (singular), minted fresh on lavender.
- **Do NOT reuse the existing `leaf-spots`.** It exists on 2 crops with **different scopes**: marigold
  "Leaf spots and powdery mildew" and echinacea "Bacterial and fungal leaf spots". Marigold's id
  covers powdery mildew; lavender's problem does not. Reusing it would be the scope-variant trap --
  a shorter shared id naming a wider problem on one crop than on another.
- **Heads-up for PLA-449's collision guard:** `leaf-spot` vs the existing `leaf-spots` is an
  edit-distance-1 / same-stem pair, exactly the class the guard was built to catch. It will very
  likely flag. That flag is **expected and correct to override**, but it must be adjudicated
  deliberately and registered, not silenced. If an override is unpalatable, the alternative that
  avoids the collision entirely is `lavender-leaf-spot`.

---

## SPITTLEBUG FAMILY: LAVENDER / ROSEMARY / SAGE (reporting for the id pass, no action taken)

**Is it the same organism on all three? Yes, on the best available evidence, and the three should
share one id.**

- No crop in canonical carries a spittlebug id today (verified against `crops_data_final.json`:
  zero ids matching `spittle`). This batch mints the family. Three crops carry it by name: lavender
  "**Spittlebug**" (singular), rosemary "**Spittlebugs**", sage "**Spittlebugs**".
- **`uc_ipm` routes all three hosts to one page.** The lavender host page and the rosemary host page
  both link "Spittlebugs" to the same `https://ipm.ucanr.edu/home-and-landscape/spittlebugs/`. UC IPM
  has no `home-and-landscape/sage/` page (404), so sage is unconfirmed at UC IPM.
- **`rhs` names one organism and all three plant types in one host list**: cuckoo spit affects "Many
  plants, including chrysanthemum, dahlia, fuchsia, **lavender**, **rosemary**, rose and willow", and
  names *Philaenus spumarius* (and *Aphrophora pectoralis*). Lavender and rosemary explicit; sage is
  the same family and the same host guild but is not named.
- **`umn_ext`** names *P. spumarius* as the common garden species and lists "herbs" among its hosts.
- **Caveat, stated plainly:** no document read names a binomial *and* a specific one of these three
  crops in the same sentence. The organism identification is a two-document join. It is strong (the
  meadow spittlebug is the polyphagous herbaceous-host species; the other two UC IPM species are
  pine/woody specialists) but it is an inference, not a quotation.
- **Recommended id: `spittlebugs`** (plural), shared by all three, matching the rosemary and sage
  names and `uc_ipm`'s own link text. **Lavender's singular "Spittlebug" should be normalized to
  "Spittlebugs"** so the three crops do not carry one problem under two display names.
- **Template-twin warning for the ladder pass.** The three entries are near-identical prose with the
  crop name swapped -- for example lavender "Frothy white spit-like foam on stems in late spring, with
  the small nymph hidden inside. It looks alarming but rarely harms an established lavender plant."
  against rosemary "...in spring, with a small nymph hidden inside. It looks alarming but rarely harms
  an established rosemary plant." and sage "...in late spring... an established sage plant." Every
  defect in one is a defect in three. In particular **the refuted "No specific prevention is
  warranted" sentence appears in the lavender and rosemary entries and must be fixed in all of them
  together**, and none of the three may inherit an anchor the others earned. Sage's prevention cell
  differs slightly ("Give plants full sun and airflow and do not overwater") and so does not carry the
  same false claim.

---

## SUMMARY

**Counts by STATUS (4 entries):**

| STATUS | n | Entries |
|---|---|---|
| SOURCED-OK | 0 | -- |
| SOURCED-WEAK | 0 | -- |
| **UNSOURCED-FOUND** | **3** | Spittlebug; Phytophthora root and crown rot; Leaf spot |
| **SPLIT: UNSOURCED-FOUND + UNSOURCED-NOT-FOUND** | **1** | Whiteflies and aphids (whitefly half found at `uc_ipm`; aphid half not found in 8 documents) |
| UNSOURCED-NOT-FOUND (whole entry) | 0 | -- |
| JOURNAL-ONLY | 0 whole entries | but the *Phytophthora* species enumeration, *Phoma multirostrata* leaf blight, *Xanthomonas hortorum* bacterial leaf spot and *Phomopsis lavandulae* shab are all JOURNAL-ONLY |
| WRONG | 0 whole entries | 3 individual claims refuted or overstated (below) |

**All four entries are anchorable at T1 with catalog keys lavender already cites, plus one
`ncsu_ext` URL that shipped precedent already permits. Zero catalog additions are required. The
"unsupported is not unsourceable" rule held again: 4 for 4.**

**Claims found refuted or overstated:**
1. Spittlebug `prevention_*`: "No specific prevention is warranted." **Refuted** -- `uc_ipm` and
   `umn_ext` both publish one (cut/remove infested weeds in spring before the nymphs mature), and the
   record replaces it with an unsourced spacing-and-watering sentence.
2. Phytophthora `organic_treatment_*`: "There is no cure" **overstates** `uc_ipm` 74133's "A plant
   with a substantial Phytophthora infection rarely recovers."
3. Phytophthora `symptoms_beginner`: "This is the main disease that kills lavender" is a rank claim in
   tension with `ncsu_ext` New Crops's "The most common disease problem with lavender is wilt."

**Consumer-copy constraints:** all 4 entries scanned programmatically -- no em dashes or en dashes, no
British spellings, no temperatures, no mis-cased "plant". Clean.

### THE SINGLE MOST IMPORTANT FINDING

**`uc_ipm` publishes a host-indexed pest list for lavender, and the record does not match it in either
direction.** `https://ipm.ucanr.edu/home-and-landscape/lavender/` lists exactly four invertebrates --
**Leafhoppers, Spider Mites, Spittlebugs, Whiteflies** -- and exactly one disease, **Phytophthora Root
and Crown Rot**. Against that list the record:

- **carries a pest UC IPM does not put on lavender: aphids.** And this is not an omission on UC IPM's
  part. **The same editor's rosemary page lists Aphids explicitly**, alongside the same spittlebugs,
  whiteflies, leafhoppers and spider mites. UC IPM decided aphids belong on rosemary and not on
  lavender. Seven other documents agree by silence, including `rhs`, which names lavender's pests and
  mentions neither aphids nor whiteflies. Half of `pests[1]` is an invention.
- **omits two pests UC IPM does put on lavender: leafhoppers and spider mites.** The record has 2 of
  the 4.

Everything else in this report is a claim-level fix. This one is a roster-level fix, and it has to be
settled **before** a ladder is authored, because a ladder built on "Whiteflies and aphids" bakes the
unsourced half into `control_methods` references and into a problem `id` that -- per the hard rule --
can never be re-derived afterward.
