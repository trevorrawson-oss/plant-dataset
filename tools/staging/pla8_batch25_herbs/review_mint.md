# PLA-8 BATCH 25 -- INDEPENDENT SOURCE-TRUTH REVIEW: MINT

Reviewer: MINT independent reviewer. I did not author `out_mint.json` and have not defended it.
All fetches 2026-09-04. No data file changed. Canonical read-only.

Subject: `tools/staging/pla8_batch25_herbs/out_mint.json` -- 9 entries (5 pests, 4 diseases),
**32 rungs and 59 `field_corrections`**, counted from the file. Five of the nine are SPLIT limbs.

## 0. Documents I opened MYSELF, and how

The record pass reported `curl` unavailable. It is: but `python3 urllib` with a browser user-agent
is not, and **every document this crop depends on opened, including both WSU `.doc` files, which I
read byte-level via `textutil` rather than from the record's transcription.** This matters: two of
my findings turn on sentences the record pass never transcribed.

| key | URL | how read |
|---|---|---|
| `usu_ext` | extension.usu.edu/yardandgarden/research/mint-in-the-garden | full HTML, incl. the FAQ block |
| `ncsu_ext` | plants.ces.ncsu.edu/plants/mentha-spicata/ | full HTML |
| `uc_ipm` | ipm.ucanr.edu/home-and-landscape/mint/ | full HTML |
| `uc_ipm` | PESTNOTES/pn7404.html (Aphids) | full text |
| `ucanr_ext_spider_mites` | PESTNOTES/pn7405.html (Spider Mites) | full text |
| `uc_ipm` | PESTNOTES/pn7406.html (Powdery Mildew on **Vegetables**) | full text |
| `uc_ipm_pn7493` | PESTNOTES/pn7493.html (Powdery Mildew on **Ornamentals**) | full text -- **not used by this record; see FIX-3** |
| `uc_ipm` | agriculture/peppermint/verticillium-wilt/ (ANR 3457) | full text |
| `uc_ipm` | agriculture/peppermint/mint-root-borer/ (ANR 3457) | full text |
| `uc_ipm` | agriculture/peppermint/webspinning-spider-mites/ (ANR 3457) | full text |
| `rhs` | rhs.org.uk/disease/mint-rust | full text |
| `wsu_ext` | s3.wp.wsu.edu/.../MintrustA.doc | **.doc downloaded and decoded, 656 words, read in full** |
| `wsu_ext` | s3.wp.wsu.edu/.../PowderyMildewMint.doc | **.doc downloaded and decoded, read in full** |

`wsu_ext` admission: not re-litigated. The coordinator closed it and the host is used 192 times in
shipped canonical.

---

# THE FIVE THINGS THE TASK ASKED ME TO SETTLE

**1. The powdery mildew / anthracnose split: CLEAN, both directions.**
UC IPM's mint page lists exactly one disease -- "Plant Diseases: Powdery Mildew on Vegetables" --
and **does not name anthracnose**, verified in the page's own text. USU's page carries "Anthracnose"
and contains the strings *powdery* and *mildew* **zero times** (grepped). The split anchors each limb
where its document is: `powdery-mildew` -> `uc_ipm` + `wsu_ext`; `anthracnose` -> `usu_ext` alone.
Powdery mildew's prevention is built on airflow, spacing, sun, thinning and nitrogen, and
`prevention_beginner` states the negative outright: *"Crowding, shade and soft, over-fed growth are
what this disease needs; whether the leaves are wet or dry makes far less difference."* No
powdery-mildew field tells the reader to keep leaves dry. **And the overcorrection did not happen**:
grepped the 123 prose strings -- no field tells a home grower to sprinkle mint overhead. The one
sprinkler sentence sits in `organic_treatment_seasoned` as a reason *not to spend effort on leaf
drying*. UC IPM's hedge is real and the author respected it: 7406, *"However, overhead sprinklers
are not usually recommended as a control method in vegetables because their use may contribute to
other pest problems."* The author also declined 7406's stronger Quick Tip, *"Wash spores off infected
plants with overhead sprinkling"* -- correct, because rust and anthracnose sit on the same plant.
**This limb is the best work in the file.**

**2. Mint rust re-pointing: VERIFIED, and I can now settle the temperature.**
NCSU's *entire* disease field is three sentences: *"Fungal diseases are common diseases in spearmint.
Two main diseases are rust and leaf spot. The plant spreads aggressively."* No *Puccinia*, no
rhizome-overwintering. USU's page carries no pathogen overwintering claim at all. Both re-points hold.
WSU verbatim: *"In late summer and fall, pustules on mint stubble and foliage become dark chocolate
brown. This is the overwintering stage (telia) of the rust fungus and is the source of new infections
the following spring."* The rewrite to stubble and fallen foliage is right. *"rusty leaves are not
good to eat"*: struck, and I confirm independently that the RHS page contains **no statement about
eating affected leaves**.

**THE HOT-WATER FIGURE, RESOLVED.** The refusal was correct, but its framing is not, and the
`unreachable_claims` instruction to *"re-read the WSU sentence and settle which number is published"*
cannot succeed. I read the WSU `.doc` byte-level. It says, verbatim:

> "Rust on rhizomes can be eliminated by immersing rhizomes in water at 113 F (34 C) for 10 minutes before planting."

**The record's transcription is exact. The contradiction is WSU's own, in the published document**, so
no amount of re-reading WSU settles it. RHS settles it, and the record pass never quoted the sentence:

> "Wash rhizomes thoroughly in early autumn and immerse in hot water at 44ºC (111ºF) **(no higher)** for 10 minutes, then cool in cold water and plant. An accurate thermometer is required, because 44ºC (111ºF) is very near **the lethal temperature for the plant**, and it may be more profitable to spend the money on some new plants."

Resolution: both agree on **10 minutes**. RHS's **44°C / 111°F** is the usable figure -- internally
consistent, home-scoped, and carrying its own ceiling and lethality warning. WSU's Celsius
parenthetical is corrupt (34°C is 93°F, not a disinfestation temperature); its 113°F is 45°C, which is
*above* RHS's stated "no higher". **Whoever builds the method should take 44°C / 111°F / 10 minutes
from RHS and must carry the "no higher" caution with it.** Note also that ADJUDICATIONS row A6 credits
the 111°F figure to WSU; that figure is RHS's, and A6's attribution is wrong.

**3. Verticillium's fabricated attribution: GONE, and nothing unanchored replaced it.**
Grepped: "Connecticut" appears **0 times** in the 123 prose strings. CAES is absent from
`source_catalog_admission.txt` (the only Connecticut key is `uconn_ext`, a different institution).
The `high` prose reads like a `high` problem: *"There is no cure for a plant once it is infected, and
the fungus stays in the ground for years after the plant is gone."* **But the entry has one WRONG
claim and one over-broad strike -- FIX-1 and FIX-4, both below, and FIX-1 is the most important
finding in this review.**

**4. Mint root borer: the commercial figures were held out correctly.**
Grepped: "2 billion" -> 0 hits, "two or more larvae" -> 0 hits, "five mites" -> 0 hits, "Murray" /
"Todds" / "flaming" -> 0 hits. The biology and calendar came across and every clause verifies against
ANR 3457. The **Sept-Oct window I ADJUDICATE AS CORRECTLY KEPT**: it is set by the insect, not by
acreage (larvae are in the rhizomes until they leave in October), and UC IPM's own method sentence is
*"Examine soil, roots, and rhizomes, and record the number of larvae found"* -- so "lift a runner and
look" is the published action at garden scale, not an invention. The threshold hanging off it is
disclosed and declined. One caveat at FIX-13.

**5. Flea beetle de-naming: COMPLETE, and stated positively.**
"mint flea beetle" -> 0 hits; "Longitarsus" -> 0 hits, across `name`, all 8 corrected fields and the
rung note. USU's row is verbatim *"Flea Beetle | Small, shiny black beetles that chew tiny holes in
leaves."* -- no species. `cause_seasoned` states the absence affirmatively: *"Flea beetles as a group
rather than one named species: Utah State's mint listing gives no binomial and no admitted document
ties a particular flea beetle to garden mint."* That is the right shape: it closes the gap instead of
leaving one a later pass fills from a non-admitted host.

**6. THE REFUSAL ON RHS's FUNGICIDE SENTENCE: RIGHT. I would have refused too.**
I read the RHS page around the sentence. It sits directly beneath: *"The products listed in the
'Fungicides for gardeners' document below are legally available for use by home gardeners in the UK."*
The sentence is a statement about **UK product registration**, full stop. It cannot be repointed into
US consumer copy, and "stronger because it says why" is exactly wrong -- the "why" is the
jurisdiction-specific part. Dropping the absolute rather than re-anchoring it was correct, and the
choice cost nothing: WSU names Rally 40W, Headline and Amistar as *registered* mint-rust materials, so
"no reliable home cure" is not even a US biological truth -- it is a US **availability** claim, and no
document read for this crop makes one. **The ladder does not leave a hole**: five cultural rungs, no
chemical rung, and no field implies a cure exists. Confirmed by grep: "fungicide" appears 0 times in
mint's prose.

---

# ENTRY-BY-ENTRY

Legend: HOLDS / WRONG / UNSUPPORTED / SYNTHESIS / STYLE / FIT, per the brief.

## Aphids (`aphids`, insect, low) -- 5 rungs, 4 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `balance_nitrogen` | HOLDS | 7404: *"High levels of nitrogen fertilizer favor aphid reproduction, so never use more nitrogen than necessary."* |
| 2 | `water_spray` | HOLDS, **incomplete -- FIX-6** | USU: *"spray plant with a forceful jet of water to dislodge the insects"*; 7404: *"Knock aphid populations off plants by shaking the plant or spraying it with a strong stream of water"*; monitoring interval verbatim: *"at least twice a week when plants are growing rapidly"* |
| 3 | `beneficial_predators` | HOLDS, one scope word STYLE | 7404 lists *"Lady beetles (ladybugs) / Lacewings / Syrphid fly larvae / Soldier beetles / Tiny parasitic wasps"*. "hoverfly larvae" for syrphid is correct common tongue. **"mint-scale aphid natural enemies" overstates scope**: 7404 is a general Pest Note and names them for aphids, not for mint. |
| 4 | `insecticidal_soap` | HOLDS | USU names insecticidal soaps for mint; 7404: *"Don't apply them to drought-stressed plants or when it is very hot."* |
| 5 | `horticultural_oil` | HOLDS | 7404: *"Apply these materials with a high volume of water, usually a 1 to 2% oil solution in water, and target the underside of leaves as well as the top."* |

Corrections: `organic_treatment_seasoned` HOLDS. `symptoms_seasoned` HOLDS and the UC IPM credit
re-point (mint listing -> Utah State) is correct and necessary given the URL slot. **`symptoms_beginner`
and `organic_treatment_beginner` carry FALSE `why` strings -- FIX-2.**

**Missing: an `ant_exclusion` rung -- FIX-8.**

## Spider mites (`spider-mites`, mite, low) -- 4 rungs, 2 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `even_watering` | HOLDS | 7405: *"Plants under water stress also are highly susceptible"*; *"Spider mites reproduce rapidly in hot weather and commonly become numerous in June through September."* |
| 2 | `water_spray` | HOLDS, **incomplete -- FIX-6** | 7405: *"In gardens and on small fruit trees, regular, forceful spraying of plants with water often will reduce spider mite numbers adequately"*; *"apply a water spray or mist to the undersides of leaves at least once a day"*; *"Be sure mites are present before you treat"*; *"you'll need a hand lens"* |
| 3 | `augmentative_release` | HOLDS | ANR 3457: *"N. fallacis can also be purchased from commercial insectaries"*; 7405: *"useful in establishing populations in large plantings or orchards"*; *"Spider mites frequently become a problem after applying insecticides."* Per-acre trigger correctly withheld. |
| 4 | `insecticidal_soap` | HOLDS | 7405: *"Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F"*; *"Oils and soaps must contact mites to kill them, so excellent coverage... is essential."* Renders `90°F`. |

Both corrections improve the prose. **Both carry FALSE `why` strings -- FIX-2.** The 90°F/water-stress
limit the record omitted is genuinely the best addition on this entry: it lands in exactly the weather
that makes the mites.

## Cutworms (`cutworms`, insect, low) -- 2 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `stem_collars` | HOLDS | USU: *"Cutworm | Larvae feed at or below ground and sever stems of seedlings or plants. | Protect individual plants with a collar or trap, use registered insecticides."* |
| 2 | `handpick` | SYNTHESIS, disclosed and acceptable | USU gives the *location* (*"at or below ground"*) but does not name handpicking. The author flagged this itself in `notes_to_orchestrator`. The dropped "at dusk" was the actual unanchored part and it is gone. |

All 8 corrections HOLD. The de-bundling is clean: no sentence from the three-organism bundle was
divided between limbs, and `prevention_beginner`'s `why` correctly refuses the debris-shelter claim as
common cutworm knowledge that this crop's documents do not carry. Disclosing USU's "registered
insecticides" option rather than silently dropping it is the right handling.

Note, not a defect: mint's `low` is the roster minority for this id (computed: 5 medium / 1 low across
6 valued crops). Defensible on a spreading perennial where the loss is per plant at establishment.

## Flea beetles (`flea-beetles`, insect, low) -- 1 rung, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `floating_row_cover` | HOLDS | USU: *"Control with registered insecticides or cover plants in spring with row covers."* |

All 8 corrections HOLD. **A one-rung ladder is correct here and is not a defect** -- USU offers exactly
two controls and one of them is an unnamed "registered insecticide". Padding this would have been the
defect. `organic_treatment_beginner` correctly replaces the bundle's unanchored *"hose or handpick flea
beetles"*: neither hosing nor handpicking appears anywhere on USU's page.

## Mint root borer (`mint-root-borer`, insect, low) -- 3 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `off_season_tillage` | HOLDS on timing, **SYNTHESIS on the action -- FIX-13** | ANR 3457 verbatim: *"Tillage can be effective in late fall or spring when the mint root borer is overwintering or before adults emerge in June."* Depth rendered from *"(2-4 cm below)"* as "an inch or so" -- accurate (0.8-1.6 in) and correctly not converted to a figure. |
| 2 | `crop_rotation` | HOLDS | ANR 3457: *"Rotation with a non-host crop is also a possibility."* |
| 3 | `beneficial_nematodes` | HOLDS | ANR 3457: *"Parasitic nematodes can be released through irrigation at 2 billion infective juveniles per acre."* Rate withheld, delivery and timing carried, reader sent to the label. Model handling of a commercial figure. |

Corrections: all 8 HOLD against ANR 3457, phrase by phrase. *"Larvae feed on leaves for 2 to 4 days
then drop to the soil surface and burrow into a rhizome"*, the October exit, spring pupation,
early-to-mid June emergence with mid-to-late July peak, one generation -- all verbatim. Finishing the
cert log's unfinished de-naming by **citing the page that carries the organism rather than deleting the
limb** is exactly right.

One anchoring gap: `prevention_seasoned` asserts a home practice ("when a home patch is lifted and
divided") on an entry whose `sources` is `["uc_ipm"]` alone. USU carries it verbatim -- *"Divide and
replant established plants in the spring before growth starts or early in the fall"* -- so add
`usu_ext`. Small, but it is an unkeyed claim, the same shape as the defects this batch is fixing.

## Mint rust (`mint-rust`, fungal, medium) -- 5 rungs, 6 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `garden_sanitation` | HOLDS, **narrowed -- FIX-10** | WSU: overwintering telia on *"mint stubble and foliage"*; RHS: *"Remove affected plants promptly before the black resting spores are formed and contaminate the soil."* |
| 2 | `airflow_spacing` | HOLDS; one SYNTHESIS clause | WSU: *"the disease is recycled every 8 to 10 days when favored by moisture on foliage"*; USU: *"thinning or dividing may be essential to maintain healthy plants."* "the lever is the number of hours a day the canopy stays wet" is an inference from the interval, not the interval's meaning; harmless. |
| 3 | `water_at_the_base` | HOLDS | USU rust row verbatim: *"Avoid wet leaves overnight. Use drip irrigation or apply overhead water before mid-day."* Both halves carried. This is where dry-foliage advice belongs and the split put it there. |
| 4 | `weed_host_control` | HOLDS | WSU: *"Rust from escaped mint and non-cultivated mint can also be a source of rust infection in the spring."* Unusually apt on a plant that escapes. |
| 5 | `certified_clean_stock` | HOLDS | WSU: *"Source materials should be inspected and be rust-free before propagating stem cuttings"*; *"Monitor stem cuttings closely for rust and discard infected plants promptly."* RHS corroborates: *"try to locate any uninfected stems and carefully dig these out and move to another location."* |

Corrections: `symptoms_seasoned`, `cause_beginner`, `cause_seasoned` and `organic_treatment_seasoned`
HOLD and are the substance of the fix. The early-spring systemic stage is a genuine addition, verbatim
WSU: *"Early spring infections are systemic in spearmint and infected plants are twisted and distorted,
and stems easily break"* and *"Infected plants in early spring are usually sparse in occurrence but are
early sources of inoculum."* **`symptoms_beginner` over-deletes -- FIX-9.** The ladder is also missing a
rung USU hands it -- **FIX-7**.

## Verticillium wilt (`verticillium-wilt`, fungal, high) -- 4 rungs, 7 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `garden_sanitation` | HOLDS | ANR 3457: *"cleaning all equipment and vehicles entering mint fields and cleaning shoes of people moving from field to field"*; *"Minimize cultivation to avoid spreading microsclerotia."* The shoe clause does scale down. |
| 2 | `balance_nitrogen` | HOLDS | USU: *"do not over fertilize plants."* Correctly restored; the record had dropped USU's third control entirely. |
| 3 | `crop_rotation` | HOLDS in this rung | ANR 3457: *"Rotation to crops that do not encourage reproduction of V. dahliae for a minimum of five years"*; *"Do not rotate to mint, potatoes, or strawberry"*; *"grass hays (orchardgrass, fescue, or timothy), corn, sudangrass, alfalfa, cereals, onions, and garlic."* **This rung has the direction right.** |
| 4 | `certified_clean_stock` | HOLDS | ANR 3457: *"use only rootstock certified to be free of V. dahliae."* The "no certification scheme exists for a garden division, so the working equivalent is provenance" translation is honest. |

Corrections: `symptoms_beginner`, `symptoms_seasoned`, `cause_seasoned`, `prevention_seasoned` HOLD;
the CAES strike is complete and correct. **`organic_treatment_beginner`, `prevention_beginner` and
`prevention_seasoned` carry an INVERTED rotation direction -- FIX-1.** **`cause_beginner` strikes a
claim its own cited document publishes -- FIX-4.**

## Powdery mildew (`powdery-mildew`, fungal, low) -- 4 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `airflow_spacing` | HOLDS; one clause UNSUPPORTED -- FIX-11 | WSU: *"Powdery mildew is often severe on mint grown in the greenhouse due to humid, shady conditions"*; *"humid conditions such as those that occur in mint canopies."* 7493 corroborates: *"locate plants in sunny areas as much as possible. Provide good air circulation."* |
| 2 | `balance_nitrogen` | HOLDS | WSU: *"The disease is most severe on young, succulent plants such as those resulting from heavy nitrogen fertilization and irrigation."* |
| 3 | `garden_sanitation` | HOLDS | WSU: *"Overwinter of the powdery mildews that infect mint are thought to be infected mint plants, stubble and wild hosts of the mint family."* |
| 4 | `sulfur` | HOLDS on what it says, **UNSAFE BY OMISSION -- FIX-5** | WSU: *"Initial applications of sulfur are usually made when plants are 4 to 6 inches tall"*; *"Sulfur should not be applied if temperatures will exceed 90F within 3 days after application"*; *"once powdery mildew becomes established it is very hard to control."* Renders `90°F`. |

All 8 corrections HOLD and the moisture correction is exactly right. `cause_seasoned`'s refusal to
hard-name the fungus is well judged and verbatim-backed: WSU says the name *Erysiphe cichoracearum*
*"should be subdivided into more than 20 species"* and that *"several species of powdery mildews attack
members of the mint family (Lamiaceae) in the Pacific Northwest. A least two appear to be species
previously unknown to science."* Naming it would have been the fabrication.

**Anchoring is weaker than it needs to be -- FIX-3.**

## Anthracnose (`anthracnose`, fungal, medium) -- 4 rungs, 8 corrections

| # | rung | grade | evidence |
|---|---|---|---|
| 1 | `garden_sanitation` | HOLDS | USU: *"Rotate planting areas, remove diseased plants, and prune healthy plants to the ground in fall."* The fall-versus-midseason distinction is real and the note makes it. |
| 2 | `airflow_spacing` | HOLDS | USU preamble: *"Most diseases can be minimized or eliminated by appropriate watering and ensuring proper sunlight to plants... thinning or dividing may be essential."* |
| 3 | `water_at_the_base` | HOLDS; one clause STYLE -- FIX-11 | USU: *"Consider drip irrigation as an excellent method to provide regular water and keep foliage dry."* |
| 4 | `crop_rotation` | HOLDS | USU: *"Rotate planting areas."* |

All 8 corrections HOLD. **This is a correctly SHORT ladder**: USU's row is the only anchor that exists,
it offers three controls, and the entry ships four rungs with no chemical tier because USU offers no
spray for this disease. `organic_treatment_seasoned` says so in plain words rather than leaving a gap.
Refusing *Sphaceloma menthae* on the same grounds as the powdery mildew binomial is consistent and
right.

---

# FIX ITEMS

## FIX-1 -- WRONG. The verticillium rotation direction is INVERTED in three live consumer fields.

**Exact text, all three:**
* `organic_treatment_beginner`: "...and **keep mint off ground that has grown potatoes or strawberries**."
* `prevention_beginner`: "Plant clean stock in ground with no history of the disease, and **keep mint out of a bed that has grown potatoes or strawberries**."
* `prevention_seasoned`: "**Keep new beds off ground that grew potatoes or strawberries**..."

**What is wrong.** UC IPM ANR 3457 -- this entry's own cited document -- names potato and strawberry in
one direction only: what **not to plant after mint**, in ground already infested with mint-adapted
strains. Every occurrence is inside the section *"Reduce Production of Microsclerotia"*, which opens
*"Once V. dahliae is discovered in a field, it is prudent to remove the mint and plant a nonhost."* The
record turned that around into a siting rule for where to put mint, and the same page contradicts it
outright.

**The sentence that settles it**, UC IPM ANR 3457, "Comments on the Pathogen":

> "Strains more specialized on other crops (e.g., **potatoes**) usually **do not attack mint**, although exceptions may occur."

And the direction as published:

> "Grower experience in the Midwest and Oregon has shown that **in fields infested with mint V. dahliae strains**, potato and red clover are poor crop rotation choices"
> "Do not rotate **to** mint, potatoes, or strawberry."

Note the entry's own `crop_rotation` rung gets it right ("keep potatoes and strawberries out too",
i.e. after mint), so the record now says both things. **Precise grades: the potato limb is WRONG
(contradicted); the strawberry limb is UNSUPPORTED-tending-SYNTHESIS** -- ANR 3457 does say
*"Certain asymptomatic hosts of this pathogen (e.g., strawberry) may allow modest reproduction of the
fungus"*, which makes strawberry-ground inoculum arguable, but the page never states the siting rule.

This is the shipped record's error inherited, not created: the author correctly trimmed tomato and
eggplant as unanchored and did not notice that the surviving pair was pointing the wrong way. The
`why` on `cause_seasoned` says "the list is trimmed to what is published" -- the *list* was, the
*direction* was not.

**What the fix should say instead.** The genuinely home-relevant sentence on this page is the one the
record never used: *"A major source of V. dahliae is infected mint rhizomes used as planting material"*
and *"any movement of infected plant material (particularly roots) can spread the fungus."* For a crop
propagated by division, that is the real siting rule.

## FIX-2 -- WRONG `why`. Four corrections strike claims their own cited documents publish.

The record pass flagged these as *"Not proven absent... Verify"*. They were not verified; they were
converted into strikes whose `why` asserts an absence. I read the documents. All four are present.

| entry / field | the `why` says | the cited document says |
|---|---|---|
| aphids `organic_treatment_beginner` and `_seasoned` | "**Neem is named on neither cited document for mint**... UC IPM's Pest Notes speaks of oils and soaps generically" | pn7404: *"Oils may include petroleum-based horticultural oils or plant-derived oils such as **neem** or canola oil"*; and *"Soaps, **neem oil**, and horticultural oil kill only aphids present on the day they are sprayed"* |
| spider mites `organic_treatment_beginner` | "**Neem is named for mites on neither cited document**" | pn7405: *"Both petroleum-based horticultural oils and plant-based oils such as **neem**, canola, or cottonseed oils are acceptable"* |
| spider mites `organic_treatment_seasoned` | "'**minute pirate bugs**' has no anchor on either cited document" | pn7405, twice, one of them in the page's Quick Tips: *"Key natural enemies include predatory thrips, lacewings, and **minute pirate bugs**"*; and *"various general predators such as **minute pirate bugs**, bigeyed bugs, and lacewing larvae"* |
| aphids `symptoms_beginner` | "'sometimes with curled, **sticky** foliage'... the record pass could not surface a honeydew sentence in either cited document" | pn7404: *"Aphids can curl leaves and produce **sticky honeydew** that may attract ants and sooty mold"*; and *"aphids can also produce large quantities of a sticky exudate known as honeydew"* |

**The prose outcomes are mostly fine** -- generalizing neem to "a horticultural oil" is safe, and
replacing minute pirate bugs with the mint-specific *Neoseiulus fallacis* is arguably an improvement.
**The `why` strings are not fine.** They are the durable record of why a claim was removed, and a later
pass reading "neem is named on neither cited document" will believe it. Two of them additionally apply
an inconsistent standard: the aphids `why` disqualifies 7404's neem sentence as "not for mint" while
the same entry carries 7404's nitrogen and virus sentences, which are equally not-for-mint.

**Minimum fix: rewrite the four `why` strings to state the real reason** (a named brand-level product
is not carried into a ladder that already has a `horticultural_oil` method; a mint-specific predator is
preferred over a general one). **The one substantive loss is "sticky"** -- honeydew is a genuine field
diagnostic, it is in the cited document twice, and it should go back into `symptoms_beginner`.

## FIX-3 -- Anchoring. `uc_ipm_pn7493` names MINT and is unused, while sage in this batch uses it.

**Exact state.** `powdery-mildew.sources` is `["uc_ipm","wsu_ext"]`, with `uc_ipm` resolving to the mint
host-index page -- a bare listing that carries no mint powdery-mildew content -- and every substantive
sentence anchored to WSU, a Columbia-Basin commercial mint-oil document.

**What is wrong.** The record pass concluded that UC IPM has no usable mint powdery-mildew document
because 7406's host list *"runs artichoke to turnip and contains no herb"*, and the author inherited
that. **It read the wrong Pest Note.** UC IPM Pest Notes **7493**, *Powdery Mildew on Ornamentals*,
which is catalog-admitted as its own key --

```
uc_ipm_pn7493  T1  university_extension  UC IPM Pest Notes: Powdery Mildew on Ornamentals (UC ANR Publication 7493)
```

-- names mint explicitly:

> "Common ornamental plants susceptible to powdery mildew include aster, deciduous azalea, tuberous begonia, California poppy, China aster, chrysanthemum, columbine, coral bells, corn flower, cosmos, crape myrtle, dahlia, delphinium, euonymus, forget-me-not, gaillardia, godetia, hydrangea, London plane tree, lupine, lilac, **mint**, monarda, oak, pansy, periwinkle, phlox, pot marigold, ranunculus, rose, rhododendron, rudbeckia, salvia, snapdragons, sweet pea, turfgrasses, verbena, and zinnia."

It also carries, for a document that names this host:

> "all powdery mildew species can germinate and infect **without water on the plant's surface**. Water on plant surfaces for extended periods **inhibits spore germination** and kills the spores of most powdery mildew fungi."
> "locate plants in sunny areas as much as possible. Provide good air circulation and avoid excess fertilizing or use a slow-release fertilizer."
> "The best time to irrigate is mid-morning, so plants dry rapidly, reducing the likelihood of infections by other fungi, such as those that cause **rust**..."

That third sentence is UC IPM independently reaching the exact judgment the author reasoned to alone --
that on a plant which also gets rust, you do not chase the sprinkler result. It is a stronger anchor
than anything currently on the entry.

**This is not hypothetical in-batch, and the key is this batch's own.** I diffed the working-tree
canonical against `HEAD`: `source_catalog` has gone 219 -> 220 entries and the **single** addition is
`uc_ipm_pn7493` (file mtime 12:29, before this review began; I changed nothing). `out_sage.json`
already anchors its `powdery-mildew` entry to that key at that URL, and the batch's own ADJUDICATIONS
row A9 quotes 7493. **So the batch minted the exact key mint's powdery mildew limb needs, for a
document that names mint, and mint's entry did not get it.** Adding it costs nothing and moves the
limb off a bare listing page and off sole reliance on a commercial oil-crop document.

## FIX-4 -- Over-broad strike. The verticillium longevity claim is published, quantified, on the cited page.

**Struck text** (from `cause_beginner`, and per its `why` also from `symptoms_seasoned`): "the disease
that most limits mint's longevity" / "the disease that shortens the life of a mint patch".

**The `why` says:** "a superlative with no document behind it".

**Half right.** The *superlative* is unanchored -- nothing ranks it against the root borer, and striking
"most" was correct. But the **claim** is published, on this entry's own cited page, with a number:

> "Verticillium wilt is a **serious disease** of peppermint in the Pacific Northwest."
> "**Useful stand longevity may be reduced from 5 years or longer to as little as 2 to 4 years.**"
> "Infected plants eventually die."

So the record struck a true, anchored, quantified, high-value claim as unanchored and replaced it with a
generic consequence. **This also matters for the severity raise**: the author reasoned to `high` from
consequence in the abstract, when the sentence that establishes `high` was sitting in the cited
document unread. Restore it without the superlative: *it shortens the useful life of a patch -- UC IPM
has infested stands dropping from five years or more to as little as two to four.*

Disclosure, adjudicated in the author's favor: the same page says the disease is *"currently found at
very low levels"* in California and that fungicide/fumigant use is uncommon *"because the occurrence of
this disease is so rare"*. That is a California-frequency statement against a PNW-severity statement.
`high` rests on consequence, which is the defensible axis, and I do not think it needs changing.

## FIX-5 -- Omission with a safety edge. The sulfur rung has no preharvest interval on a cut-and-eat herb.

**Exact text**, `sulfur.note_beginner`: "Sulfur works on powdery mildew, but only if you get in before
the coating appears. Start early in the season on a patch that gets it every year, and do not spray if
the temperature is heading above 90°F in the next three days."

**`notes_to_orchestrator` states:** "no admitted document gives a preharvest interval for sulfur on
culinary mint, so the rung carries timing and the temperature limit and no rate."

**WSU gives one, in the same paragraph as the 90°F limit the rung does carry:**

> "Sulfide from sulfur may contaminate mint oil. The time interval between sulfur application and harvest is extremely important in eliminating sulfide contamination and **sulfur should not be applied within 30 days of harvest**."

The stated reason is oil quality, not food safety, and "culinary mint" is technically not "mint oil" --
so the note is literally defensible and I am not calling it WRONG. But the effect is that a home grower
who cuts mint weekly is told to run a sulfur program with no mention that its own source keeps sulfur
off the crop for 30 days before cutting. **A rung is not finished when it omits the constraint that
makes it unusable at home.** At minimum the rung should say WSU's program is written for a crop
harvested once, and that the interval is why sulfur suits a patch you are prepared to stop picking, not
one you cut for the kitchen every week. (7405 independently: *"don't apply sulfur within 30 days of an
oil spray"* -- a second interval, not carried, less important.)

## FIX-6 -- Cross-entry incoherence. The hosing rungs contradict the same crop's disease records.

**Exact text:**
* aphids `water_spray.note_beginner`: "Hit the plant with a forceful jet of water and knock the aphids off... Look again in a few days and repeat if they are back."
* spider mites `water_spray.note_beginner`: "Wash the undersides of the leaves with a strong spray of water. Done regularly, and **in hot weather even daily**..."

Neither says *when in the day*. On the same plant, `mint-rust` now tells the reader that leaf wetness
is the driver and to water before mid-day, and `anthracnose` tells them to keep the foliage dry. The
batch's whole powdery-mildew correction is about not letting one record's moisture advice run over
another's -- and here the pest records wet the foliage, daily, with no timing, against the disease
records on the same crop.

**Two documents publish the caveat, and one of them is mint-specific:**

> USU, mint rust row: *"Avoid wet leaves overnight. **Use drip irrigation or apply overhead water before mid-day.**"*
> pn7404: *"Using water sprays **early in the day** allows plants to dry off rapidly in the sun and be less susceptible to fungal diseases."*

Both rungs need the morning clause. This is cheap, sourced, and it closes the last moisture
inconsistency on the crop.

## FIX-7 -- Omission. Mint rust has no fertility/water rung, and USU publishes one verbatim for rust.

USU's mint page, Fertilization section, in the entry's own cited document:

> "**Over watering and fertilizing promotes rust** and diminishes mint oil production."

and, Water section: *"Avoid overwatering as it leads to disease."*

That is a crop-and-disease-specific sentence naming rust by name, from a source already in
`mint-rust.sources`. `balance_nitrogen` is legal on `fungal` (`applies_to` includes `fungal_foliar`),
is `cultural` tier, and would sit at the top of the ladder as its cheapest rung. Neither the record
pass nor the author surfaced this sentence. The powdery mildew entry got its nitrogen rung; rust, which
has an explicit published one, did not.

## FIX-8 -- Omission. The aphid ladder has no ant rung, and 7404 makes ants a headline item.

pn7404, twice:

> "**Ants protect aphids from natural enemies. Keep ants off plants to help beneficial insects do their job.**"
> "**Managing ants is a key component of aphid management.**"

`ant_exclusion` exists in `control_methods.json` (tier `physical`, `applies_to` includes
`insect_soft_bodied`, so it is legal on this entry) and would slot beside `water_spray`, ahead of
`beneficial_predators`, preserving least-invasive-first. The ladder currently reaches
`beneficial_predators` and tells the reader to conserve natural enemies without mentioning the thing
7404 says is actively defeating them.

Scope note in fairness: 7404's sticky-band form is written for trees and woody plants. The form that
transfers to a mint bed is its other one: *"ant stakes or containerized baits may be used on the ground
to control ants without affecting aphids or their natural enemies."*

## FIX-9 -- Narrowed. Mint rust's earliest and most diagnostic symptom was deleted rather than relocated.

**Struck text:** "pale spots on the **upper surface**". **The `why`:** the closest admitted text is
RHS's *"Pale and distorted shoots in spring"*, which is about shoots.

The *placement* was indeed wrong, and striking "upper surface" is right. But USU's rust row -- again,
this entry's own cited document -- publishes the pale stage with the correct location:

> "Mint Rust | **Small whitish, slightly raised spots** that turn reddish orange or brown **on underside of leaves**."

The replacement `symptoms_beginner` starts at "Small orange to rust-brown powdery spots", losing the
whitish raised stage entirely -- which is the stage at which a gardener can still act before the RHS
deadline the same field then invokes. The fix is a relocation, not a deletion: *small whitish, slightly
raised spots on the undersides that turn orange then rust-brown.*

## FIX-10 -- Narrowed. The rust sanitation rung is weaker than both documents behind it.

**Exact text**, `garden_sanitation.note_beginner`: "Take the rusted leaves off as you see them, and in
fall clear the old stems and fallen foliage right off the bed."

Two published instructions are stronger than leaf-picking and stubble-clearing, and both are on cited
pages:

> RHS: *"Remove affected plants promptly before the black resting spores are formed and contaminate the soil. **In the case of garden mint it is also necessary to remove infected rhizomes.**"*
> USU, FAQ: *"**Before winter, cut each plant back to the ground to discourage pests and diseases.**"*

The RHS rhizome clause is specifically about **garden mint** and it did not survive the (correct) move
of *overwintering* off the rhizomes -- overwintering is on stubble, but RHS still says infected rhizomes
must come out. And the author's `why` on `organic_treatment_beginner` states that "cut a badly infected
patch to the ground is not what any source says for rust" -- USU's FAQ does say it for mint, for pests
and diseases generally, and before winter, which is the timing the record already prefers. The strike of
the *mid-season* cut was right; the absence claim behind it is over-broad, and USU's actual sentence is
a better anchor for the fall rung than the paraphrase now in place.

## FIX-11 -- Two rung notes describe the DATASET rather than the world.

* powdery mildew `airflow_spacing.note_seasoned`: "**Mint is one of the few crops this dataset is happy to put in part shade**, which is exactly why the siting decision carries weight here."
* anthracnose `water_at_the_base.note_seasoned`: "Unlike powdery mildew on the same plant, this is a disease where the dry-foliage instruction is the correct one, **which is precisely why the two are separate records now**."

Both are claims about the record structure, and both go stale when the structure changes -- the same
class as a rung note asserting which rungs exist. The first is also **measurably wrong**: computed from
canonical, 25 of 128 crops carry a part-shade tolerance in `sunlight` (18 "Full sun to partial shade",
6 "full sun to part shade", 1 first-year variant), about a fifth of the roster. "One of the few" does
not survive the count. Mint's own value is "Full sun to partial shade", `sunlight_hours` [4, 8]. Trim
both to plant-scoped statements.

## FIX-12 -- Register, minor.

* `mint-rust.organic_treatment_seasoned`: "**Rogue** the twisted, distorted shoots out in early spring". "Rogue" as a verb is trade jargon; the seasoned register is tolerant but this one is genuinely opaque. "Pull out" or "dig out" carries it.
* `verticillium-wilt.prevention_seasoned` uses "microsclerotia" unglossed. It is glossed in `symptoms_seasoned` ("pinhead-sized hardened bodies in the soil"), so the reader who lands on prevention first gets it cold.
* aphids `beneficial_predators.note_seasoned`: "**mint-scale** aphid natural enemies" -- 7404 names them for aphids generally, not at any mint scale. Reword.

Everything else on consumer copy is clean: I scanned all 123 prose strings programmatically -- **0 em
dashes, 0 en dashes, 0 bare-`F` temperatures (all 6 render `°F`), 0 British spellings, 0 mid-sentence
capitalized "Plant"**.

## FIX-13 -- "Turn the bed over" is ambiguous on a rhizomatous perennial.

`off_season_tillage.note_beginner`: "Turn the bed over in late fall, or in spring before June."

UC IPM's tillage is a commercial field operation between stands. On a home mint patch, "turn the bed
over" reads as either destroying the planting or chopping rhizomes -- which is how mint propagates. The
`note_seasoned` and the prevention fields make clear this is the fall lift-and-divide, and USU supports
that timing (*"Divide and replant established plants in the spring before growth starts or early in the
fall"*), so the fix is one clause in the beginner note: lift and divide, shake the soil out, replant.
Grade SYNTHESIS, not WRONG -- but a beginner should not have to reconstruct the action from the
seasoned register.

---

# SUMMARY

**Rungs (32).**

| grade | count | where |
|---|---|---|
| HOLDS | 28 | all five ladders' cultural and physical rungs verify sentence-by-sentence |
| HOLDS, incomplete (a FIX attaches) | 3 | aphids `water_spray`, spider mites `water_spray` (FIX-6); powdery mildew `sulfur` (FIX-5) |
| SYNTHESIS, disclosed/acceptable | 3 | cutworms `handpick`; rust `airflow_spacing` clause; root borer `off_season_tillage` (FIX-13) |
| WRONG | **0** | no rung note contradicts its document |
| UNSUPPORTED | 1 clause | powdery mildew `airflow_spacing` roster claim (FIX-11) |
| STYLE | 3 clauses | FIX-11 (x2), FIX-12 |

(Rows overlap where one rung takes two grades; no rung is ungraded.)

**Corrections (59).**

| grade | count |
|---|---|
| HOLDS -- needed, anchored, and the anchor carries the replacement | 51 |
| WRONG (the replacement text) | 3 -- verticillium `organic_treatment_beginner`, `prevention_beginner`, `prevention_seasoned` (FIX-1) |
| HOLDS in text, WRONG in `why` | 4 -- aphids x2, spider mites x2 (FIX-2) |
| Over-broad strike / narrowed against the record | 3 -- verticillium `cause_beginner` (FIX-4), rust `symptoms_beginner` (FIX-9), rust `organic_treatment_beginner` `why` (FIX-10) |

**Ladder caps and shape.** No cap in this crop's brief applies to mint, and nothing is padded: flea
beetles ships one rung because USU offers one usable control; anthracnose ships four cultural rungs and
no chemical rung because USU offers no spray; mint rust ships five cultural rungs and no chemical rung
for a documented reason. `validate_out.py` passes -- tier ordering least-invasive-first, `applies_to`
coherent, no repeated methods. All seven roster claims in `notes_to_orchestrator` that I could
recompute from canonical are **exactly right** (anthracnose 4 medium / 1 low; verticillium-wilt 1
valued instance at medium; powdery-mildew 16 valued spanning low/medium/high; 118 shared ids with 43
carrying mixed severities; `spider-mites` typed `mite` on all 16). Compute-never-assert was honored.

## The single most important finding

**FIX-1: the verticillium wilt entry tells a home grower, in three fields, not to plant mint where
potatoes or strawberries grew -- and its own cited document says the opposite.** UC IPM ANR 3457:
*"Strains more specialized on other crops (e.g., potatoes) usually do not attack mint, although
exceptions may occur."* The page's potato-and-strawberry sentence runs the other way: it is about what
not to plant **after** mint in mint-infested ground, in a section that opens *"Once V. dahliae is
discovered in a field, it is prudent to remove the mint and plant a nonhost."* The entry's own
`crop_rotation` rung has the direction right, so the record now asserts both. This survived because the
correction pass was aimed at the *list* (tomato and eggplant were correctly trimmed as unanchored) and
never questioned the *direction* of what was left.

Runners-up, in order: **FIX-2** (four `why` strings assert absences their cited documents refute --
neem twice, minute pirate bugs, sticky honeydew, all traceable to the record pass's "verify" items
being closed as strikes without the verification); **FIX-3** (`uc_ipm_pn7493` is catalog-admitted, names
mint by name, is used by sage in this same batch, and would move mint's powdery mildew limb off a bare
listing page); **FIX-4** (a quantified longevity claim struck as unanchored while its cited page
publishes *"Useful stand longevity may be reduced from 5 years or longer to as little as 2 to 4
years"*); **FIX-5** (the sulfur rung omits WSU's own 30-day preharvest interval on a herb cut weekly).

**What is right, and should be said.** The powdery mildew / anthracnose split is correct in both
directions and did not overcorrect. The de-namings are complete and stated positively. Every commercial
figure on ANR 3457 was held out of prose while the biology and calendar came across. The RHS
fungicide-availability refusal is right and I would have made it identically. Nothing in this file
fabricates an attribution, and the one that was live is gone.

---

# RECORD-LEVEL FINDINGS

Filed for a later pass, not fixed now.

1. **`uc_ipm_pn7493` is a key this batch just minted, with 0 uses in shipped canonical and one use in
   staged output (sage).** It names mint, monarda, salvia, sweet pea, lilac, rose and 30 other hosts
   for powdery mildew and carries the leaf-wetness physiology in its cleanest published form. The
   roster has 32 `powdery-mildew` records, several of them on hosts 7493 names by name. Worth a
   deliberate sweep once this batch lands rather than a per-crop rediscovery.

1a. **Housekeeping, flagged not fixed:** the working-tree `crops_data_final.json` is MODIFIED against
   `HEAD` -- exactly the one `source_catalog` addition above -- so `shasum -a 256` now returns
   `f6d55785...` while `LATEST.txt` still pins `a9c84847...`. The file's mtime (12:29) predates this
   review and I did not write to it, but a source-truth reviewer who checks the canonical SHA against
   `LATEST.txt` per the session protocol will find a mismatch and should know its whole content.

2. **The record pass read 7406 and concluded UC IPM has no herb-scoped powdery mildew document.** That
   is the "right document, wrong claim" pattern with an extra step: the correct document existed, in
   the catalog, one publication number away. The general lesson for future record passes is that
   `PESTNOTES` for a single disease often come in vegetable/ornamental pairs, and a herb can be in
   either.

3. **The record pass's "not proven absent -- verify" items were closed as strikes.** Four of them
   (FIX-2). Worth a convention: an item marked *verify* by a record pass must be re-read, and if it
   cannot be, the `why` must say "not re-read" rather than "no anchor".

4. **ADJUDICATIONS row A6 mis-credits the hot-water figure.** It reads "WSU... makes rhizome
   contamination removable by a 111°F / 10-minute hot-water dip". 111°F is RHS's figure; WSU publishes
   "113 F (34 C)". When the method gap is built, take **RHS: 44°C / 111°F, 10 minutes, "(no higher)"**,
   and carry RHS's warning that this is *"very near the lethal temperature for the plant"* and that
   *"it may be more profitable to spend the money on some new plants."*

5. **WSU's `MintrustA.doc` contains a published internal inconsistency** ("113 F (34 C)"). Recorded so
   a future pass does not re-open it as a transcription error. Also for the record: that document is
   the T1 source for the race structure (*"One type infects Native spearmint but not peppermint..."*)
   that §4f of the record pass leaned on, and I confirm the sentence exists verbatim.

6. **UC IPM lists Leafhoppers and Thrips for mint** and neither is in the record -- confirmed on the
   live page. `ucanr_ext_thrips` is already a catalog key and sage in this batch carries `Leafhoppers`.
   Coverage gap, not an error.

7. **UC IPM ANR 3457 names a resistant Mentha**: *"Native spearmint (Mentha spicata L.) found along
   waterways in northeastern California is considered resistant to V. dahliae."* Together with WSU's
   powdery mildew cultivar signal (Scotch spearmint susceptible, peppermint and native spearmint not),
   mint now has two published within-species susceptibility differences that would hang off
   `varieties[].resistance` if mint ever gets a variety pass.

8. **`verification_log_ref` append is owed** and the author already specified it correctly. I confirm
   the trigger: the log asserts the Connecticut credit was struck, and it was still live on
   `Verticillium wilt.symptoms_seasoned` eight weeks later. Append, do not rewrite.

9. **The `mint-rust` / `oregano-rust` pair is still not registered** under `deliberately_distinct` in
   `tools/problem_id_registry.json`. Owed, per the author's own note and the record pass's §4f.

10. **`mint-root-borer.sources` should gain `usu_ext`** so `prevention_seasoned`'s fall lift-and-divide
    claim has a key behind it. USU: *"Divide and replant established plants in the spring before growth
    starts or early in the fall."*

11. **`curl` is unavailable in this environment but `python3 urllib` with a browser user-agent is not.**
    Every document the record pass reported as 403 or TLS-blocked deserves one retry by that route
    before it is treated as unreachable -- both WSU `.doc` files decoded cleanly with `textutil`, and
    two of this review's findings came out of reading them directly rather than from the record's
    transcription.
