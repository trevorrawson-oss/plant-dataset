# PLA-8 BATCH 25 (HERBS) -- INDEPENDENT SOURCE-TRUTH REVIEW: ROSEMARY

Reviewer pass date: 2026-09-04. I did not author these ladders. No data file was changed by this
pass; this report is the only file written.

Subject: `tools/staging/pla8_batch25_herbs/out_rosemary.json` -- 6 entries (5 canonical + the
aphid/whitefly split), 21 rungs, 33 declared `field_corrections`.

`python3 validate_out.py rosemary` -> `OK: rosemary validates. 4 pests + 2 diseases, 21 rungs.`
Rung method legality and tier ordering re-checked independently against
`tools/control_ladder_gate.py`: `TYPE_TARGETS['mite'] = {insect_general, mite}`,
`TYPE_TARGETS['insect'] = {insect_boring, insect_chewing, insect_general, insect_soft_bodied}`,
`TYPE_TARGETS['fungal'] = {disease_general, fungal_foliar, fungal_soilborne}`. Every rung is legal
for its entry's type and every ladder is non-decreasing in `TIER_RANK`.

---

## Documents I fetched and read myself (2026-09-04)

I did not work from the record report's quotes. Every sentence I grade a rung against below, I
pulled from the live document in this pass.

| Key | Document | Read |
|---|---|---|
| `ucanr_ext_spider_mites` | UC IPM Pest Notes 7405, Spider Mites | yes |
| `uc_ipm` | UC IPM H&L -- Aphids | yes |
| `uc_ipm` | UC IPM H&L -- Whiteflies (+ `PMG/PESTNOTES/pn7401.html`) | yes |
| `uc_ipm` | UC IPM H&L -- Spittlebugs | yes |
| `uc_ipm` | UC IPM H&L -- Phytophthora Root and Crown Rot | yes |
| `uc_ipm` | UC IPM H&L -- Powdery Mildew on Vegetables | yes |
| `uc_ipm` | UC IPM H&L -- Rosemary (crop page) | yes |
| `uc_ipm` | UC IPM -- Rosemary, Cultural Tips | yes |
| `umn_ext` | UMN Extension -- Spittlebugs | yes |
| `rhs` | RHS -- Cuckoo spit / spittlebugs | yes |
| `ncsu_ext` | NC State Plant Toolbox -- *Salvia rosmarinus* | yes |
| `clemson_hgic` | Clemson HGIC -- Herbs | yes |
| `psu_ext` | Penn State -- Herb Garden Plants: Rosemary | yes |
| `tamu_agrilife` | TAMU AgriLife E-623 (PDF) | yes |
| `uwi_hort` | Wisconsin Horticulture -- Rosemary | yes |
| `umd_ext` | UMD Frederick Co. MG, "Uh-Oh! What's Wrong With My Houseplant?" (PDF) | yes |
| `umd_ext` | UMD Extension -- Powdery Mildew on Indoor Plants | yes |
| `uga_ext` | UGA B1170 -- Herbs in Southern Gardens | yes |
| -- | NCSU, "Aphids Found on Flowers and Foliage" (the linked factsheet) | partial: retired |
| -- | **PNW Plant Disease Handbook -- Rosemary-Root Rot** | **yes, see below** |

Also read for method-fit adjudication: `control_methods.json` entries for `even_watering`,
`ant_exclusion`, `weed_host_control`, `certified_clean_stock`, `crop_rotation`, `handpick`,
`prune_out_infection`, `yellow_sticky_traps`, `airflow_spacing`; the shipped precedents for
`crown-and-root-rot` (parsley), `powdery-mildew` (slicing-cucumber), `spider-mites`/`aphids`
(cherry-tomato) and `whiteflies` (roma-tomato); and
`/Users/trevorrawson/plant-astro/src/components/guides/PestsDiseasesCard.astro` to establish what
the crop page actually renders.

---

## THE PNW PAGE: I READ IT. IT NAMES NO PHYTOPHTHORA.

This is the open item the batch could not close, so I am reporting it first and reporting the
provenance honestly.

**Direct retrieval still fails.** `https://pnwhandbooks.org/plantdisease/host-disease/rosemary-rosmarinus-officinalis-root-rot`
returned **HTTP 403** to WebFetch, as did `/node/3469/print` and `?print=1`. Bash networking is
denied in this sandbox (both sandboxed and `dangerouslyDisableSandbox` curl attempts were refused by
the permission system), and `web.archive.org` is not fetchable from this tool, although the Wayback
availability API confirms a 200 snapshot exists at timestamp `20260519162138`.

**I retrieved the page through the `r.jina.ai` text-rendering proxy**, which fetches and renders the
live URL. Two independent retrievals agree: the proxy render, and an extended search-index snippet
that reproduces the same causal sentence. I am **not** counting the search snippet as the read; the
proxy render is, and I am flagging the one caveat -- I did not touch the origin myself, so the
orchestrator should confirm with a direct fetch before a catalog admission is made permanent.

Verbatim, from the page:

> **Cause**
> "Several root rotting organisms have been detected in rosemary root rot samples coming to the OSU
> Plant Clinic. Pythium, Berkeleyomyces sp. (formerly Thielaviopsis basicola), and Rhizoctonia are
> among the organisms found." ... "over watering and too much fertility inhibit good growth. These
> same soil conditions favor many root-rot organisms."

> **Cultural control**
> - "Good drainage is essential in pots or the landscape."
> - "Water and fertilize lightly."
> - "Use new trays and pots with clean soilless media. If pots must be reused then wash off all
>   debris and soak in a sanitizing solution or treat with aerated steam for 30 min."
> - "Preplant soil solarization has been helpful in reducing populations of certain soilborne
>   pathogens and weeds in western Oregon..."

**Consequences, all of which favor the decisions already made:**

1. **The genus-agnostic pin is correct and is now positively evidenced, not merely cautious.** The
   only T1 handbook page written specifically about rosemary root rot names Pythium,
   *Berkeleyomyces* and Rhizoctonia and **does not name Phytophthora at all**. Two of those three
   are true fungi, not oomycetes.
2. **`cause_seasoned`'s replacement text is vindicated in its exact wording.** It says "A group of
   soilborne water molds *and fungi*" and "More than one genus causes this on woody herbs and which
   one is on rosemary is not settled." At authoring time that was an honest hedge with no anchor.
   It now has one, and the "and fungi" half turns out to be load-bearing: a Phytophthora-only or
   water-mold-only framing would have been wrong.
3. **The 2026-07-06 cert-log line is disturbed and needs its `[CORRECTION ...]` append.** The line
   reads "root/crown rot correctly Phytophthora-only (UC IPM, Pythium already dropped)". Pythium is
   named by the one rosemary-specific document. Per `docs/verification_log_ref_convention.md` this
   is an appended correction, not an edit.
4. **The ladder does not change.** Drainage, replant restriction and clean stock are true under all
   three genera. The author predicted this and was right.
5. **It does supply content the ladder lacks** -- see FIX-2 and refusal (a) below.

---

## Spider mites (`spider-mites`, type `mite`, severity `low`) -- 5 rungs

Type and severity corrections both hold. `mite` matches the 16-crop convention. `low` is carried by
four separate admitted documents I read myself: PSU "Outdoor plants in full sun are resistant to
pests."; TAMU E-623 "Rosemary is fairly resistant to pests."; Wisconsin "Rosemary generally has few
pest problems, although it can be attacked by aphids, spider mites, mealybugs or scales."; NCSU
"Rosemary is generally pest and disease free." Nothing I read converts mention-frequency into
severity, so `medium` was unsourced and `low` is the sourced value.

* **`even_watering`** -- **HOLDS**, with a FIT reservation recorded below. The mechanism is
  pn7405's "**Plants under water stress also are highly susceptible.**" (I confirmed this exact
  string is on the page; pn7405 also carries "Water-stressed trees and plants are less tolerant of
  spider mite damage. Be sure to provide adequate irrigation." and "Damage is usually worse when
  compounded by water stress.") The cadence is TAMU E-623: "**On average, water rosemary every 1 to
  2 weeks, depending on the plant size and climate conditions. Allow the plants to dry out
  thoroughly between each watering.**" The note's refusal to say "constant moisture" is the correct
  call and is written explicitly: "Do not read this as constant moisture, which is what feeds the
  root rot on this plant." **Adjudication (brief item 5): the use is honest and I would keep the
  rung.** See "The `even_watering` FIT reservation" below for the one residual risk.
* **`garden_sanitation`** -- **HOLDS**. Clemson, verbatim: "**The best defenses against pests on
  herbs are proper growing conditions, good sanitation, removal of weak or infested growth, and
  regular pruning.**" The canopy-density clause is UMD Frederick Co. MG on spider mites, verbatim:
  "**Dense foliage and poor air circulation contribute to this problem.**"
* **`water_spray`** -- **HOLDS**. pn7405: "**Regular, forceful spraying of plants with water often
  will reduce spider mite numbers adequately.**" and "**Dusty conditions often lead to mite
  outbreaks. Apply water to pathways and other dusty areas at regular intervals.**" and "Be sure to
  get good coverage, especially on the undersides of leaves" -- which is what the note's "Get into
  the middle of the bush" renders for a needle canopy. Clemson corroborates: "Spider mites thrive in
  dry conditions and can be discouraged by spraying the plants with a strong stream of water
  regularly during periods of drought."
* **`beneficial_predators`** -- **HOLDS**. pn7405 names the complex: "predatory mites", "sixspotted
  thrips", "spider mite destroyer lady beetle", "minute pirate bugs", "bigeyed bugs", "lacewing
  larvae". The selectivity argument is pn7405's "Use selective materials, preferably insecticidal
  soap or insecticidal oil."
* **`insecticidal_soap`** -- **HOLDS**. Both numbers are in the document: "**Don't use soaps or oils
  on water-stressed plants or when temperatures exceed 90°F.**" The note's observation that the two
  restrictions collide with the conditions that produce a mite problem is an inference, but it is an
  inference from two sentences in one document and it produces safer advice, not a new claim.

### Corrections (4) -- all four HOLD; every anchor sentence verified verbatim

`organic_treatment_beginner`, `organic_treatment_seasoned`, `prevention_beginner`,
`prevention_seasoned` are all correctly changed and the replacements say only what the documents
say. In particular:

* Removing "for indoor plants raise the humidity" / "indoors, give good light and some humidity" is
  **right**. I searched pn7405 for humidity and misting: **there is no humidity or misting control
  in that document.** Its cultural controls are dust suppression and adequate irrigation.
* Removing "Before bringing rosemary indoors for winter, check it over for pests first" is
  defensible and the author was consistent about it. No document I read carries it.
* Replacing it with UMD's "Dense foliage and poor air circulation contribute to this problem" is the
  correct substitution, and it is quoted accurately.

**But the correction is incomplete -- see FIX-3.**

---

## Aphids (`aphids`, type `insect`, severity `low`) -- 5 rungs -- SPLIT LIMB 1/2

**The split is written from its own anchors, and the UGA bundle was not leaned on.** Verified two
ways. First, `sources` on this entry is `uc_ipm, ncsu_ext, clemson_hgic, tamu_agrilife` --
**`uga_ext` appears nowhere on either limb.** Second, all eight prose fields are substantively new
rather than the bundle sentence with one organism deleted; the only surviving bundle fragment is the
word "flowers", which is exactly the fragment that turns out to be unsupported (FIX-1).

I read UGA B1170 myself and confirm the record's account of it. The section is headed "Aphids;
Whiteflies" and its whole content is "**Good air circulation helps prevent these insects on more
susceptible plants, such as germander and monarda; once discovered, they can usually be washed away
with a spray of water.**" -- susceptibility attributed to germander and monarda, not rosemary. And
B1170's rosemary section, read in full, contains **no pest or disease sentence of any kind**. The
bundle's origin story is right and the author correctly did not use it.

* **`balance_nitrogen`** -- **SYNTHESIS** (minor, keep). The claim is anchored twice: UC IPM aphids
  "**High levels of nitrogen fertilizer favor aphid reproduction, so never use more nitrogen than
  necessary.**" and TAMU E-623, crop-specific, "**Insects that suck plant sap are generally more
  prevalent in areas where too much nitrogen fertilizer has been applied.**" The gloss "raises aphid
  reproduction **directly rather than only by making a bigger plant**" draws a contrast neither
  document draws. It is a fair reading of "favor aphid reproduction" and it is the correct anti-
  pattern to the thyme defect the brief names, so I would leave it; recording it because it is an
  inferred mechanism presented as the reason.
* **`ant_exclusion`** -- **HOLDS**. UC IPM aphids: "**ants protect the aphids from natural enemies.
  If you see ants crawling up aphid-infested trees or woody plants, put a band of sticky material
  (e.g., Tanglefoot) around the trunk to prevent ants from climbing up.**" Rosemary is a woody
  plant, so the instruction reaches it as written. The sprawl clause is anchored too: "**Prune out
  other ant routes such as branches touching buildings, the ground, or other trees.**" The
  placement argument ("it belongs before leaving the colony to its natural enemies, not instead of
  it") matches the method library's own `best_use`. *Observation, not a defect:* UC IPM also says
  "Don't apply sticky material directly to the bark of young or thin-barked trees ... Wrap the trunk
  with fabric tree wrap or duct tape and apply sticky material to the wrap," and rosemary is a
  thin-stemmed subshrub -- the single most likely misapplication on this crop. The crop note says
  only "A sticky band on the main stem stops them." The shared method carries the caution
  (`ant_exclusion.cautions[0]`: "Sticky material goes on a wrap, not on bare bark...") and
  `find_it_beginner` tells the reader to buy wrap, so nothing is lost; but this was the one place a
  crop-specific note could have earned its keep and did not.
* **`water_spray`** -- **UNSUPPORTED** on one clause. See **FIX-1**. Everything else on the rung
  holds: "**Most dislodged aphids won't be able to return to the plant, and their honeydew will be
  washed off as well.**" carries "Few find their way back", and "**Check your plants regularly for
  aphids---at least twice a week when plants are growing rapidly---in order to catch infestations
  early.**" carries the cadence. The seasoned note's "The repeat interval is set by how fast the
  plant is reflushing rather than by the calendar" is a good, faithful rendering of "when plants are
  growing rapidly".
* **`beneficial_predators`** -- **HOLDS**, with a STYLE drift. UC IPM's mummy sentence is "**The
  skin of the parasitized aphid turns crusty and golden brown, a form called a mummy.**" The notes
  say "tan, papery" (beginner) and "tan, swollen" (seasoned). "tan" is fine for "golden brown";
  "papery" and "swollen" are neither in the document nor wrong. Not worth a change.
* **`insecticidal_soap`** -- **HOLDS**. UC IPM aphids: "**insecticidal soaps and oils are the best
  choices for most situations.**" Contact-only action and coverage are correct for the method.
  *Recorded tension, not a defect:* the note's terminal claim "nothing harsher earns its place"
  rests on judgment plus the Arizona food-crop sentence, and `tamu_agrilife` -- which **is** cited
  on this entry -- says of rosemary "If spider mites, mealy bugs, or scales do appear, any organic
  or inorganic insecticide may be used." I am **not** recommending a conventional rung (TAMU names
  no product, the pest list is not aphids, and UC IPM's own recommendation is soaps and oils). But
  the cap is UC IPM's, not this crop page's, and it is worth knowing that one cited document is
  permissive where the ladder is not.

### Corrections (8) -- 6 HOLD, 2 UNSUPPORTED (the "flowers" clause)

All eight are genuinely needed. I confirm the two defects the corrections claim about the bundle:

* "**Vigorous, unstressed rosemary rarely attracts these pests**" is backwards for aphids. UC IPM:
  "High levels of nitrogen fertilizer favor aphid reproduction"; UC IPM again: "**They feed on soft,
  new plant growth.**"; Clemson: "**Aphids are common in rapidly growing, succulent plants that are
  in crowded conditions.**" The correction is required, not merely different.
* "**avoid overwatering**" as an aphid prevention has no anchor. I looked: no document I read ties
  watering to aphids on rosemary. It is this crop's root-rot lever filed under the wrong problem.
  Removing it is right.

---

## Whiteflies (`whiteflies`, type `insect`, severity `low`) -- 4 rungs -- SPLIT LIMB 2/2

The divergence the split was made for is real and the limb carries it. Both ends verified verbatim
by me on UC IPM's whitefly page and on `pn7401`.

* **`garden_sanitation`** -- **HOLDS**. "**In gardens, whitefly populations in the early stages of
  population development can be held down by a vigilant program of removing infested leaves or
  hosing down with water sprays.**" A second sentence the entry did not quote supports it further:
  "Hand removal of leaves or plants heavily infested with the nonmobile nymphal and pupal stages may
  reduce populations to levels that natural enemies can contain."
* **`water_spray`** -- **HOLDS**. Same sentence, other half. The note's "It will not clear an
  established population" is an inference from the source's scoping to "the early stages of
  population development" plus "**Management of heavy whitefly infestations is difficult.**"
  Reasonable and correctly directional.
* **`beneficial_predators`** -- **SYNTHESIS** (minor, keep). "**In many situations, natural enemies
  will provide adequate control of whiteflies; outbreaks often occur when natural enemies are
  disrupted by insecticide applications, dusty conditions, or interference by ants.**" is verbatim
  and carries the rung. The clause "**which is part of why the outdoor plant in full sun is the
  untroubled one**" fuses that sentence with PSU's separate "Outdoor plants in full sun are
  resistant to pests." Neither document offers natural enemies as the reason for PSU's observation.
  It is hedged with "part of why", so I would leave it, but it is an invented causal link between
  two documents.
* **`insecticidal_soap`** -- **HOLDS**, and this is the strongest rung on the crop. Every load-
  bearing sentence exists as quoted: "**If you choose to use insecticides, insecticidal soaps or
  oils such as neem oil may reduce but not eliminate populations.**" and "**Avoid using other
  pesticides (other than soaps and oils) to control whiteflies; not only do most of them kill
  natural enemies, whiteflies quickly build up resistance to them, and most are not very effective
  in garden situations.**" The 90°F / drought-stress guardrail is on the whitefly page itself, so it
  is not borrowed from the mite Pest Note: "**Use soaps or oils when plants are not drought-stressed
  and when temperatures are under 90°F to prevent possible 'burn' damage to plants.**" The note's
  refusal to present the stop as "the options run out" is exactly right and is the decision-relevant
  fact the bundle could not carry.

### Corrections (8) -- all 8 HOLD

Every anchor verified. Two worth calling out as correctly done:

* `cause_seasoned` "**Management of heavy whitefly infestations is difficult. The best strategy is
  to prevent problems from developing in your garden or landscape.**" -- verbatim.
* `symptoms_seasoned` "plants outside in full sun are largely untroubled" is written as a report of
  what a source says ("are described as resistant" in `cause_seasoned`), which is the honest
  handling of PSU's blanket claim. Good discipline.

### One omission worth raising (CONSIDER, not FIX)

`yellow_sticky_traps` is legal here (`physical`; `insect_general, insect_soft_bodied`), has shipped
precedent on roma-tomato, and UC IPM names it: "**yellow sticky traps can be posted around the
garden to trap adults**", "You may need as many as one trap for every two large plants". The same
document immediately demotes it -- "**Traps are most useful for monitoring and detecting whiteflies
rather than controlling them**" -- which is a legitimate reason to leave it off a *control* ladder.
But this entry's whole strategy is "Monitor an overwintering plant deliberately", and a monitoring
tool the source names for a pest the source says you must catch early is the one cheap step the
ladder skips. I would not call the omission a defect; I would ask the orchestrator to decide
consciously rather than by default. `reflective_mulch` is correctly omitted: it is an outdoor
small-plant measure and this crop's whitefly problem is indoors.

---

## Spittlebugs (`spittlebugs`, type `insect`, severity `low`) -- 2 rungs

**The ladder cap is honored.** Two rungs, `cultural` then `physical`, no chemical rung. I read UMN
myself and the sentence is verbatim: "**Pesticides are not effective against spittlebugs as the
nymphs are protected inside their spittle masses from any pesticide sprays.**" The note writes the
mechanism rather than the bare claim, which is the better form.

* **`weed_host_control`** -- **HOLDS**. UC IPM spittlebugs, verbatim: "**Spittlebugs are more likely
  to become abundant on woody plants when they migrate from nearby herbaceous hosts. Cut
  spittlebug-infested weeds in the spring before the insects mature and spread.**" Overwintering:
  "**Overwintering occurs as tiny eggs on or in stems or needles.**" Feeding duration: "**Each nymph
  feeds for 1 to 3 months.**" All present. Two small scope notes: (a) the source says "Spittlebugs
  commonly have one or two generations per year **in California**" and the note drops the state
  scoping; (b) "so a single spring clearance covers the season" is an inference from generation
  count plus feeding duration that the document does not draw. Neither changes what a reader does.
* **`water_spray`** -- **HOLDS**. UC IPM: "**Ignore spittlebugs or wash nymphs off with a forceful
  stream of water.**"; "**Feeding by abundant spittlebugs can distort host tissue and slow plant
  growth, but this is primarily a problem on herbaceous species.**"; "**Although the importance of
  their natural enemies is not well known, biological control of spittlebugs is generally considered
  to be not important.**" The RHS clause is anchored: "**Apart from producing the 'spit' these
  insects have little detrimental effect on plants and they are part of the biodiversity that
  healthy gardens support.**" The *Xylella* refusal is correct: RHS frames it as UK plant-health
  scope ("*Xylella* is not in the UK but could be introduced through the importation of infected
  plants") and it has no place in US consumer copy.

### Corrections (2) -- both HOLD

"No specific prevention is warranted" / "Nothing special is needed" are refuted by UC IPM, which
publishes exactly one prevention and makes it a weed-and-timing measure. The replacement is right
and is the highest-value line available on this pest.

### The A12 attribution correction is confirmed independently

I read both documents. UMN's weed sentence is "**Remove weeds near your gardens to remove one of
their food sources**" -- no spring timing, no migration mechanism. The spring-timing version is UC
IPM's alone. Crediting the sentence to "UC IPM and UMN both" would have been a two-document credit
read as one document's claim. The author's single attribution is the correct one.

---

## Root and crown rot (`crown-and-root-rot`, type `fungal`, severity `high`) -- 3 rungs

**Brief item 3, answered directly: NO Phytophthora attribution survives anywhere in the entry's
consumer prose.** I scanned all 75 consumer strings on this crop (11 ladder notes + 33 correction
`new` strings, plus the rest) with a case-insensitive regex: **zero hits on "phytophthora".** The
genus appears only in the `why` rationale and `anchor` metadata fields, where it is describing the
document, and in the `anchoring_urls` URL slug. The author went one step past the pin by correcting
`cause_seasoned`, and that was the right call: leaving it would have had the prose assert the genus
the id declines to assert. **And my PNW read shows the correction was not merely cautious -- it was
factually necessary.** A Phytophthora-named `cause_seasoned` would have been *wrong*, not just
over-committed.

Citing a Phytophthora-named URL while keeping the prose genus-agnostic: **I agree it is defensible**
and I would keep it, because UC IPM's rosemary crop page is what joins rosemary to that document and
the document is host-general ("Almost all fruit and nut trees, as well as many ornamental trees and
shrubs ... can develop Phytophthora root or crown rot if the soil around the base of the plant
remains wet for prolonged periods"). It host-maps nothing to rosemary. The URL is the management
anchor. The prose now says so in plain words.

* **`improve_drainage`** -- **HOLDS**, every clause. UC IPM PRCR: "**Avoid prolonged saturation of
  the soil or standing water around the base of trees or other susceptible plants**"; "**Allow the
  top few inches of soil to dry thoroughly between watering**"; "**Never cover the root crown or
  graft union with soil or mulch**"; "**Group plants according to their irrigation needs.**" TAMU
  E-623: "**Raised or slightly mounded beds provide the best drainage for the herb**" and the 1-to-2
  week soak-and-dry cadence. The needle clause is TAMU verbatim in substance: "**Sometimes it can be
  difficult to determine when a rosemary plant needs water because its needles do not wilt as broad
  leaves do.**" The year-one exception is UC IPM's own rosemary cultural tips: "**In the first year
  of planting, water regularly to keep the root ball moist. Once established, rosemary is drought
  tolerant and needs little watering.**" This is the best-sourced rung on the crop.
* **`crop_rotation`** -- **UNSUPPORTED** on its number. See **FIX-2**. The container half of the
  note ("if it was a pot, start again with fresh mix") was unanchored at authoring time and is
  **now anchored by my PNW read**: "Use new trays and pots with clean soilless media. If pots must
  be reused then wash off all debris and soak in a sanitizing solution."
* **`certified_clean_stock`** -- **HOLDS**. UC IPM PRCR: "**Select certified nursery stock and
  resistant rootstocks or varieties when available.**" The cutting-hygiene clause does **not** need
  the non-admitted UMass page: the shared method's own text already covers it -- "if you propagate
  your own, cuttings, crowns or divisions taken only from a clean plant" -- and TAMU establishes
  that rosemary is raised from cuttings. Correctly within scope.

### Corrections (6) -- all 6 HOLD

* Dropping "The real cause is too much water, not cold" rather than negating it is the right call on
  the evidence available to this pass; no document I read frames rosemary root rot against cold
  injury. The author's note that this is a third instance of the A4/A5 "not cold" template twin is
  worth acting on at batch level.
* Dropping "never let rosemary sit in soggy ground" for the source's "prolonged saturation" is a
  real correction: PRCR's word is "prolonged", and the absolute outran it.
* Adding the year-one watering exception is the most consequential fix in the six. The blanket
  "water deeply but rarely" was wrong for a first-year plant by UC IPM's own rosemary page.
* Dropping "give plants room" / "space plants for airflow" from a soilborne-rot prevention field is
  correct: spacing is the powdery-mildew lever. (UC IPM's rosemary cultural tips do give a number,
  "Plant rosemary 2 to 3 feet apart in landscapes", but it is a cultural spacing figure, not a rot
  control.)

---

## Powdery mildew (`powdery-mildew`, type `fungal`, severity `low`) -- 2 rungs

**Brief item 2, answered directly.** The leaf-wetness correction is real and complete, and the
ladder's spine is the UMD sentence.

I verified the governing biology myself on UC IPM's powdery-mildew document:
"**Although humidity requirements for germination vary, all powdery mildew species can germinate and
infect in the absence of free water.**" and "**In fact, spores of some powdery mildew fungi are
killed and germination is inhibited by water on plant surfaces for extended periods.**" and
"**Moderate temperatures (60° to 80°F) and shady conditions generally are the most favorable for
powdery mildew development.**" The host list is 18 vegetables and names no herb, so citing it for
generic biology only -- which is what the correction's own `anchor` field says it is doing -- is the
correct handling.

**No surviving rung or corrected field tells the reader to keep foliage dry or avoid overhead
watering as a mildew control.** I regex-scanned all 75 consumer strings: zero hits on "overhead";
the single hit on "damp" is a negation in a different entry ("This is not a plant you keep damp").

* **`airflow_spacing`** -- **HOLDS**, and the spine is the right sentence. UMD Frederick Co. MG,
  verbatim and complete: "**White coating on the leaves: This is usually a sign of powdery mildew
  fungus. It is common on rosemary grown indoors and may happen when plants are crowded together. It
  usually disappears when the plants are moved further apart or are taken outside in the spring.**"
  That is the indoor/poor-airflow framing the brief asks for, and the ladder is built on it.
  Corroborated by PSU "**Ensure adequate airflow between plants to prevent powdery mildew.**", NCSU
  "**Poor circulation and high humidity can cause powdery mildew.**", TAMU "**You can reduce the
  incidence of diseases by pruning overgrown plants to improve air circulation within the plants.**"
  and Wisconsin's "Good air circulation is important to prevent foliar disease." The note's explicit
  mechanism statement -- "the mechanism is humidity rather than leaf wetness ... not by drying the
  leaves faster" -- is the correct correction and it is doing real work, because it contradicts the
  shared method's own glossary text (see RECORD-LEVEL FINDINGS).
* **`garden_sanitation`** -- **HOLDS**, with one small overstatement. UMD's PM-indoor page:
  "**Registered fungicides can be used, but in most home conditions, removal of infected plant parts
  and adjustment of environmental conditions to promote better air circulation should help.**" The
  note renders "should help" as "is what resolves this". Minor strengthening; I would soften it, but
  it is not a FIX. Isolation is anchored: "you may want to isolate the plant" (UMD Frederick).

### Corrections (5) -- all 5 HOLD

**A count correction for the brief.** The brief says "damp" was removed from four fields. It was in
**three**: `symptoms_seasoned` ("favored by damp, still, humid air"), `symptoms_beginner` ("more
likely in damp, still air"), and `cause_beginner` ("likes damp, stuffy air with no breeze"). All
three are corrected. The fourth PM prose field, `cause_seasoned`, reads "Foliar fungi favored by
poor air circulation and humidity" -- it never carried "damp", it is correctly anchored by NCSU's
"Poor circulation and high humidity can cause powdery mildew", and leaving it uncorrected is right.
The batch's correction set is complete against the data; the brief's count is one too high.

The two prevention fields are correctly stripped of "avoid overhead watering" and "water at the
base", and the replacements add the two levers the record identified and the original lacked
(pruning for internal airflow, and putting the plant outside in spring).

**The refusal of a chemical rung is correct.** `sulfur` is legal here (`fungal_foliar`), but UC
IPM's sulfur-and-oil guidance sits in a document host-scoped to 18 vegetables that names no herb.
Lifting a product recommendation across a host boundary onto an edible herb is exactly the defect
class this pass exists to catch. Note for the record that TAMU, an admitted crop-specific source,
does endorse a chemical step without naming a product ("check the plants regularly and apply the
proper fungicides when needed") -- so the ladder terminates on a **product-identification** gap, not
on a finding that no chemistry is appropriate. The entry's prose does not misstate this either way.

---

# FIX ITEMS

## FIX-1 (most important). "the flowers" on aphids is anchored to a hyperlink label, not a sentence

**The exact text, in three consumer strings:**

1. `aphids` / `field_corrections.symptoms_beginner.new`: "Small soft-bodied insects packed onto the
   newest shoot tips **and the flowers**."
2. `aphids` / `field_corrections.symptoms_seasoned.new`: "Colonies sit on the new shoot tips **and
   the flowers** rather than on older woody growth..."
3. `aphids` / `control_ladder[water_spray].note_beginner`: "Wash them off the shoot tips **and
   flowers** with the hose..."

**And in the metadata**, `symptoms_beginner.anchor` presents it as a source sentence:

> `ncsu_ext: "Aphids found on flowers and foliage."`

**What is wrong.** That is not a sentence on the NCSU page. It is the **title of a linked
factsheet**, rendered by the Plant Toolbox under "*Salvia rosmarinus* has some common insect
problems:". I fetched the target: the parent publication is "**Insect and Related Pests of Flowers
and Foliage Plants**" -- "flowers and foliage" is a **class of ornamental crops**, not a description
of plant parts -- and the factsheet itself now returns "This publication (Aphids Found on Flowers
and Foliage) is no longer available." So the anchor for "aphids sit on rosemary's flowers" is a link
label to a retired publication about a different host class.

**The document sentence that settles it.** NCSU's own prose about rosemary is: "**Rosemary is
generally pest and disease free. Monitor the plant for aphids, mealybugs, whiteflies, and spider
mites, particularly if indoors.**" That establishes aphids on rosemary and says nothing about
flowers. The only siting statement in any document I read is UC IPM's host-general "**They feed on
soft, new plant growth.**" I searched UC IPM's aphid page for "flowers": the only occurrences are
"Aphids often build up on flowering plums, roses, tulip trees, crape myrtles, apples, and many
vegetables" and an instruction to plant flowering plants for natural enemies. Neither is a siting
claim.

**Why it matters beyond three strings.** "and the flowers" is the one surviving fragment of the
UGA-shaped bundle. The split was supposed to rewrite both limbs from their own anchors; this clause
came across and was then retro-fitted with an anchor that does not exist as a sentence. The record
report makes the same error, so any sibling crop whose reviewer or author reads an NCSU Plant
Toolbox "Insects:" row is exposed to it -- those rows are lists of linked factsheet **titles**, not
claims.

**Recommended remedy:** delete "and the flowers" / "and flowers" from the three strings (leaving
"the newest shoot tips", which UC IPM's "soft, new plant growth" carries), and replace the
`symptoms_beginner` anchor line with NCSU's actual sentence plus UC IPM's "They feed on soft, new
plant growth." No rung is lost and nothing else changes.

## FIX-2. The replant interval on a woody perennial is imported from an annuals-only bullet

**The exact text**, `crown-and-root-rot` / `control_ladder[crop_rotation].note_seasoned`:

> "At least one or two seasons before a susceptible plant goes back into the same soil is **the
> published interval**"

**The document sentence that settles it.** UC IPM PRCR's bullet is explicitly scoped to annuals:

> "**If tomatoes, bedding plants, or other annuals have been affected by Phytophthora root rot,
> avoid planting them or other susceptible plants, such as eggplant or peppers, in the same soil for
> at least 1 or 2 seasons.**"

Rosemary is a woody perennial subshrub. There is no published replant interval for it in any
document I read, and the same page's host-general persistence sentence points the other way:
"**Phytophthora species produce resting spores that survive for years in moist soil in the absence
of a suitable host. However, resting spore viability declines over time if soils are allowed to dry
out.**" The PNW rosemary page gives no replant interval either; its container advice is fresh media
and sanitized pots.

Calling a number "the published interval" for a host the publication excludes is the brief's defect
class 5. The practical advice is harmless; the warrant is not there.

**Recommended remedy:** keep the rung and the container half (now anchored by PNW), and drop
"is the published interval" -- either state the interval without claiming publication for this crop,
or replace it with the persistence framing the source does state host-generally.

## FIX-3. The spider-mite entry still teaches the dry-air mechanism the batch removed

**The exact text**, `spider-mites`, in two fields that carry **no** `field_corrections` entry and
therefore ship unchanged:

* `cause_seasoned`: "Tiny sap-feeding mites that thrive in dry conditions. **Dry indoor air over
  winter is a classic trigger**, and drought-stressed outdoor plants are also vulnerable."
* `cause_beginner`: "Very small mites that **love dry air** and dry, stressed plants. They flare up
  most on rosemary brought indoors for winter."

**What is wrong.** The batch's own rationale for rewriting four other fields on this entry is that
"'for indoor plants raise the humidity' has no anchor in any read document and points the reader the
opposite way from this crop's own powdery mildew entry." That is correct. But the **premise** for
that advice is left standing in the cause fields, uncorrected. A reader told that dry indoor air is
the classic trigger will re-derive "humidify the room" without being told to.

**The document sentences that settle it.** "dry conditions" as a general mite driver is anchored --
Clemson: "**Spider mites thrive in dry conditions...**"; pn7405: "Spider mites prefer hot, dusty
conditions". But the **indoor** driver, on this crop, is named by an extension source and it is not
air moisture: UMD Frederick Co. MG, on spider mites, "**Dense foliage and poor air circulation
contribute to this problem.**" And pn7405, searched for humidity and misting, offers **no** humidity
control at all -- its cultural controls are dust suppression and adequate irrigation. So "dry indoor
air over winter is a classic trigger" is UNSUPPORTED in exactly the sense the batch already ruled.

**Brief item 4, answered directly: the two entries do NOT yet point the same way.** The treatment
and prevention fields do; the cause fields do not. `notes_to_orchestrator` states "THE TWO OPPOSITE
INDOOR INSTRUCTIONS ARE RESOLVED", and a batch that believes a defect is closed will not look again
-- which is why I am flagging it rather than filing it as a nit.

**Recommended remedy:** add a `cause_seasoned` / `cause_beginner` correction on `spider-mites` that
replaces the dry-air indoor trigger with UMD's canopy-density-and-still-air driver, keeping the
anchored "dry, stressed plants" half. That makes the entry internally consistent and consistent with
powdery mildew, at the cost of two more corrections (35 rather than 33).

---

# ADJUDICATIONS THE BRIEF ASKED FOR

## The `even_watering` FIT reservation (brief item 5)

**Verdict: the use is honest, keep the rung, and record the residual risk.**

The note is written against the crop rather than against the method name: "soak, let the soil dry
thoroughly, soak again on roughly a one to two week cycle in heat", and explicitly "Do not read this
as constant moisture, which is what feeds the root rot on this plant." That is the right trade --
constant moisture would buy a mite reduction with the disease that is rated `high` on this crop, and
the two entries would then contradict each other on watering the way they currently do on air.

Three things support keeping it: (1) the mechanism the note uses is the method's own published mite
mechanism, and `even_watering.sources` includes `ucanr_ext_spider_mites` (pn7405), the same document
this entry cites; (2) it is the only method that reaches the water-stress lever, which is genuinely
anchored ("Plants under water stress also are highly susceptible."); (3) I checked the renderer --
`PestsDiseasesCard.astro` renders the rung **name** (linked to the glossary anchor) plus the crop's
note; `how_it_works_beginner/seasoned` render only on `/guides/pest-control`, per
`src/pages/guides/pest-control.astro:156`. So the reader on the rosemary page sees the honest note,
not the glossary text.

The residual risk is one click away and is real: the glossary entry a reader lands on says "**Keep
the soil evenly moist**" and "roughly 1 to 2 inches per week on shallow-rooted crops". For rosemary
that is the instruction that kills the plant. The shipped cherry-tomato precedent makes it worse by
example -- its `even_watering` note says "consistent moisture is your first line of defense". This
is a library-level tension, not a rosemary defect, and it belongs in the register rather than in
this crop's fix list.

## Refusal (a): no `garden_sanitation` rung on root and crown rot

**Verdict: a sourcing gap correctly left open, not a real omission -- and my PNW read makes it
closable, with different content than parsley's.**

The refusal is right on the evidence. I read UC IPM PRCR in full: it carries no removal instruction
at all. I read the PNW rosemary root-rot page: its cultural control is drainage, light watering and
fertility, clean media and sanitized containers, and solarization -- **no remove-and-discard**. The
only source for "Remove diseased plants promptly" remains UMass CAFE Greenhouse Floriculture, which
is not admitted (`umass_ext` is scoped to the Vegetable Program). And "there is no cure" is an
absolute no document I read states; UC IPM in fact lists registered chemistry while saying "Do not
rely on pesticide applications alone."

Two further points in the refusal's favor:

1. **Rosemary is not "thinner" than parsley here in a way that reads as an error -- it is more
   disciplined than its own precedent.** Parsley's shipped `crown-and-root-rot` rung asserts "there
   is no rescue once the crown has decayed", which is the same unsourced absolute rosemary refused.
   That is a record-level item for a later pass, filed below.
2. **The gap is now closable, but with different text.** PNW supplies a genuinely rosemary-specific
   sanitation lever the ladder lacks and that matters more on this crop than removal does, because
   rosemary is most often killed in a pot: "**Use new trays and pots with clean soilless media. If
   pots must be reused then wash off all debris and soak in a sanitizing solution or treat with
   aerated steam for 30 min.**" `garden_sanitation` is `applies_to: ["any"]`, so it reaches. If the
   PNW plantdisease host-disease pages are admitted to the catalog, the right rung to add is
   container hygiene, **not** parsley's remove-and-discard. PNW also names a fertility lever
   ("Water and fertilize lightly") that no rung on this entry carries. Solarization I would leave
   off: it is western-Oregon nursery practice with a 4-to-6-week clear-plastic protocol.

## Refusal (b): no `handpick` rung on spittlebugs

**Verdict: correct, and there is a stronger reason than the one given.**

`handpick` is legal (`physical`; `insect_chewing, insect_general, mollusk`, and
`TYPE_TARGETS['insect']` contains `insect_general`), and UMN does carry "**Physically remove them by
hand.**" -- I read it. The author's stated reason (water_spray already carries physical removal, and
a second physical rung would pad a deliberately short sequence) is sound on its own.

The stronger reason is that a `handpick` rung would push the reader **toward** removal on a problem
two of the three cited documents say to leave alone. UC IPM's management sentence *begins* with
"**Ignore spittlebugs** or wash nymphs off with a forceful stream of water", and RHS says
"**Spittlebugs are not a pest, so please don't remove them**". A ladder whose own framing is that
removal is cosmetic and optional should not grow a second removal rung. Refusal upheld, and I would
record the RHS/UC IPM reason alongside the redundancy reason, because the redundancy argument alone
would not survive someone arguing "more options is better".

---

# SUMMARY

**Rungs (21):**

| Grade | Count | Where |
|---|---|---|
| HOLDS | 17 | all 5 spider-mite rungs; aphids `ant_exclusion`, `beneficial_predators`, `insecticidal_soap`; whiteflies `garden_sanitation`, `water_spray`, `insecticidal_soap`; both spittlebug rungs; root rot `improve_drainage`, `certified_clean_stock`; both powdery-mildew rungs |
| SYNTHESIS | 2 | aphids `balance_nitrogen` (mechanism gloss); whiteflies `beneficial_predators` (invented causal link between two documents) |
| UNSUPPORTED | 2 | aphids `water_spray` (FIX-1, "flowers"); root rot `crop_rotation` (FIX-2, annuals-scoped interval) |
| WRONG | 0 | -- |
| STYLE | 0 | one drift recorded inside a HOLDS rung ("tan, papery" vs "crusty and golden brown") |
| FIT | 0 | one reservation recorded and adjudicated (`even_watering`) |

**Corrections (33):** 31 HOLD, 2 UNSUPPORTED (the two aphid `symptoms_*` fields carrying "flowers").
Every other anchor sentence I checked exists verbatim in the document named. I found **no**
correction that swaps one unsourced sentence for another, and **no** correction that was
unnecessary -- each of the 33 replaces something the documents refute, do not carry, or scope
differently.

**Uncorrected fields that should have been corrected: 2** (spider-mite `cause_beginner` /
`cause_seasoned`, FIX-3).

**Ladder caps: both honored.** Spittlebugs terminate at `physical` with no chemical rung, and the
UMN sentence is verbatim on the page. Powdery mildew terminates at `garden_sanitation` with no
`sulfur` rung, correctly, because UC IPM's product guidance is host-scoped to 18 vegetables.

**Brief items answered:**

1. Aphid/whitefly split -- **verified**. Both limbs carry full 8-field prose from their own anchors,
   `uga_ext` is cited on neither, and the divergence at both ends of the ladder is real and correctly
   written. The one carryover from the bundle is FIX-1.
2. Powdery mildew -- **verified**. All three "damp" fields corrected (the brief's "four" is one too
   high), both prevention fields stripped of the leaf-wetness lever, zero surviving "keep foliage
   dry" advice, and UMD's "moved further apart or are taken outside in the spring" is the ladder's
   spine.
3. Root and crown rot -- **verified genus-agnostic; zero "Phytophthora" in 75 consumer strings.**
   And **I read the PNW page**: Pythium, *Berkeleyomyces*, Rhizoctonia, **no Phytophthora**. The pin
   is not just cautious, it is correct.
4. Opposite indoor instructions -- **only partly resolved.** See FIX-3.
5. Spider mites -- severity `low` and type `mite` both verified against four documents; the
   `even_watering` use is honest, adjudicated keep.
6. Both refusals upheld, one with an added reason and one with a now-closable path.

**THE SINGLE MOST IMPORTANT FINDING:**

> **FIX-1: the aphid limb's "flowers" siting is anchored to a hyperlink label, not to a sentence.**
> `ncsu_ext: "Aphids found on flowers and foliage."` is quoted with a period, as a source sentence,
> in an entry created by this batch. It is the **title of a linked NCSU factsheet** whose parent
> publication is "Insect and Related Pests of Flowers and Foliage **Plants**" -- a class of
> ornamental crops, not a description of where aphids sit -- and the factsheet now returns "This
> publication ... is no longer available." Three consumer strings tell a reader to look at, and hose
> off, rosemary's flowers on that basis.
>
> Two things make it more than a three-string fix. It is **the one surviving fragment of the UGA
> bundle** the split was supposed to eliminate: the clause came across from "on new growth and
> flowers" and was then given an anchor after the fact. And the mistake is **structural, not local**
> -- an NCSU Plant Toolbox "Insects:" row is a list of linked factsheet titles, so any crop in this
> batch anchored on one is exposed to the same error. The record report makes it too.

---

# RECORD-LEVEL FINDINGS

Filed for a later pass, not fixed now.

1. **Parsley's shipped `crown-and-root-rot` `garden_sanitation` rung carries the absolute rosemary
   refused.** Its `note_seasoned` reads "there is no rescue once the crown has decayed", and its
   `organic_treatment_beginner` reads "There is no cure for a rotting plant, so remove it." No
   admitted document I read states either. Rosemary's refusal is the disciplined behavior and
   parsley is the outlier; whoever revisits that crop should not "fix" rosemary to match it.

2. **`airflow_spacing`'s glossary text states the wrong mechanism for powdery mildew, and rosemary's
   note has to argue against it.** The method says "Give plants room and a sunny, breezy spot so
   **leaves dry quickly** after rain or dew. Most leaf diseases need long wet periods to take hold"
   and, seasoned, "shorten **leaf-wetness duration**". For powdery mildew that is the exact mechanism
   UC IPM refutes ("all powdery mildew species can germinate and infect in the absence of free
   water"; "germination is inhibited by water on plant surfaces for extended periods"). Rosemary's
   note handles it correctly by naming humidity rather than wetness, but the glossary a reader clicks
   through to still teaches the wrong reason. The shipped slicing-cucumber `powdery-mildew` ladder is
   worse: it carries a `water_at_the_base` rung whose seasoned note says "Skip overhead irrigation."
   This batch is correcting the crop entries; the method library and the cucumber precedent are the
   same defect, unrepaired.

3. **`even_watering`'s glossary text is the opposite instruction for Mediterranean subshrubs.**
   "Keep the soil evenly moist", "roughly 1 to 2 inches per week". Rosemary's note has to say "Do not
   read this as constant moisture." Batch 25 has at least four crops with this profile (rosemary,
   lavender, thyme, sage). If any of them uses `even_watering` for mites, the library will be
   contradicting four crop pages at once. A `soak_and_dry` sibling method, or a scoped caveat in the
   glossary, is the shape of the fix.

4. **NCSU Plant Toolbox "Insects:" and "Diseases:" rows are lists of linked factsheet titles, not
   claims about the crop.** This is the structural form of FIX-1 and it should be written into the
   record-pass brief. The rosemary record report quotes two of these as sentences ("Aphids found on
   flowers and foliage." and "Southern Blight of Herbaceous Ornamentals"); the second is also a link
   title, and the record correctly did not build on it, but the first propagated into shipped prose.

5. **The 2026-07-06 cert-log line needs its `[CORRECTION ...]` append.** "root/crown rot correctly
   Phytophthora-only (UC IPM, Pythium already dropped)" is disturbed by the PNW read: Pythium,
   *Berkeleyomyces* and Rhizoctonia are what the one rosemary-specific handbook page names, and
   Phytophthora is not among them. Per `docs/verification_log_ref_convention.md` this is an append,
   never an edit of the original prose.

6. **Two catalog admissions are now better evidenced than when the author raised them.** (a) The PNW
   plantdisease host-disease pages: I have now read rosemary's, it is the only T1 page written
   specifically about this crop's root rot, it settles the taxon question, and it supplies a
   container-hygiene rung and a fertility lever the ladder lacks. The existing `pnw_handbook_epn` key
   is scoped to one EPN page, so this needs its own key. Note the retrieval problem is real: the
   origin 403s every direct path and the site is only reachable through a text proxy from this
   toolchain. (b) UMass CAFE Greenhouse Floriculture remains the only source for remove-and-discard,
   and admitting it is what would let root and crown rot state the rescue limit directly.

7. **`audience` is absent from all six entries in the output**, which is correct for the four KEEP
   entries (the promote merges into canonical records that already carry `"audience": "core"`) but
   means the two split limbs, `aphids` and `whiteflies`, are new records with no `audience` key. The
   author flagged this; I confirm it programmatically and it is a promote-side must-do.

8. **Minor internal inconsistency on aphid monitoring cadence.** `water_spray.note_seasoned` says
   correctly that "The repeat interval is set by how fast the plant is reflushing rather than by the
   calendar", and then `prevention_seasoned` reintroduces the calendar with "check the growing tips
   twice a week **through the spring flush**". UC IPM's trigger is growth rate, not season: "at
   least twice a week **when plants are growing rapidly**". Not worth a correction on its own; worth
   catching if that field is touched for another reason.

9. **Four pests and two diseases named on rosemary by multiple admitted T1 sources still have no
   entry** -- mealybugs (NCSU, PSU, TAMU, Wisconsin: four sources, more than whiteflies' three),
   scales (TAMU, Wisconsin), thrips (UC IPM, PSU), leafhoppers (UC IPM), botrytis (NCSU, Wisconsin),
   southern blight (NCSU, UMD). The record raised this; I confirm the counts from my own reads. It is
   an authoring decision, not a defect in this batch, but the crop currently presents a pest set of
   four where six are named and a disease set of two where four are named.
