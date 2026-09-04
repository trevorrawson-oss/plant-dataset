# PLA-8 BATCH 25 -- RECORD / SOURCE PASS: LEMONGRASS

Reviewer pass date: 2026-09-04. Canonical read READ-ONLY at
`a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`. No file in the repo was
modified except this report.

Subject: `lemongrass` `pests[]` (2 entries) and `diseases[]` (3 entries). All 5 carry `sources`, so
this was a verification pass, not a hunt from scratch. Every cited document was fetched and read
this session; PD-57 was read page by page as an image-extracted PDF after the text layer failed.

## Documents read this session (all fetched 2026-09-04)

| catalog key | document | url | outcome |
|---|---|---|---|
| `usu_ext` | USU Extension, "How to Grow Lemongrass in Your Garden", Terra Linse and Dan Drost, Vegetable Specialist, published May 2020 | https://extension.usu.edu/yardandgarden/research/lemongrass-in-the-garden | live, full text read |
| `ncsu_ext` | NC State Extension Gardener Plant Toolbox, *Cymbopogon citratus* | https://plants.ces.ncsu.edu/plants/cymbopogon-citratus/ | live, read twice with different framings to defeat label/value shift |
| `uwi_hort` | Wisconsin Horticulture Extension, "Lemongrass", Susan Mahr, University of Wisconsin | https://hort.extension.wisc.edu/articles/lemongrass/ | live, full text read |
| `uhawaii_ctahr` | UH-CTAHR **PD-57, "Rust of Lemongrass", Scot Nelson, Dept. of Plant and Environmental Protection Sciences, Plant Disease Nov. 2008** | https://www.ctahr.hawaii.edu/oc/freepubs/pdf/PD-57.pdf | **302 redirect** to `https://www3.ctahr.hawaii.edu/oc/freepubs/pdf/PD-57.pdf`; PDF has no usable text layer, read as page images, all 4 pages |
| `uiuc_ext` | University of Illinois Extension, "Lemon grass" | https://extension.illinois.edu/herbs/lemon-grass | live, full text read |
| `uc_mg` | UC Master Gardeners of Santa Clara County, "Lemongrass" | https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/lemongrass | live, full text read |
| `uf_ifas` | UF/IFAS Gardening Solutions, "Lemongrass" | https://gardeningsolutions.ifas.ufl.edu/plants/edibles/vegetables/lemongrass/ | live; **NO PEST OR DISEASE CONTENT** |
| `uf_ifas` | UF/IFAS Extension Nassau County, "Fact sheet: Lemongrass", posted 2017-05-28, last updated 2022-03-04 | https://blogs.ifas.ufl.edu/nassauco/2017/05/28/fact-sheet-lemongrass/ | live; **is a republication of the USU document, bylined "Terra Linse and Dan Drost, Utah State University"** -- NOT independent corroboration |
| `uc_mg` | UC Master Gardeners of Solano County, "Through the garden gate: Repelling summer mosquitoes with Citronella", published 2020-07-24 | https://ucanr.edu/blog/under-solano-sun/article/through-garden-gate-repelling-summer-mosquitoes-citronella | live; found on hunt, **directly on the mechanism question** |
| `ucanr_ext_spider_mites` | UC IPM Pest Notes: Spider Mites, UC ANR Publication 7405, L.D. Godfrey, Entomology, UC Davis, updated 12/2011 | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html | live, read; available unused anchor |
| (not in catalog) | PlantVillage, "Lemon grass", hosted at plantvillage.psu.edu | https://plantvillage.psu.edu/topics/lemon-grass/infos | live; lists only rust, derived from PD-57 and from Linse & Drost. Adds nothing. Not proposed for admission. |
| (not in catalog) | APS *Plant Disease* -- Ploetz et al. 2014, first report of *P. nakanishikii* in Florida; and PDIS-10-22-2314-PDN, first report of a *Puccinia* sp. on lemongrass in Minnesota | apsjournals.apsnet.org | **403 to WebFetch (paywall), read via abstract/search metadata only.** JOURNAL-ONLY. |

Absence findings below are scoped to exactly this list.

---

## NON-PROBLEM RULING EVIDENCE

### Q1. Do usu_ext, ncsu_ext and uwi_hort support "generally pest-resistant"? Yes. Do they support AROMATIC OILS as the mechanism? No. Not one of them.

**The absence half of the claim is well supported. All three cited sources carry it.**

`usu_ext` (verbatim, from the "Pests and Disease" section):

> "Lemongrass is generally free of pests and diseases when grown correctly."

Note the qualifier the record drops: USU attributes the freedom to **"when grown correctly"**, which is a
husbandry attribution, not a chemical one.

`uwi_hort` (verbatim):

> "Lemongrass has essentially no pest problems in the Midwest."

Note the qualifier the record drops: **"in the Midwest"**. This is a region-scoped statement from a
Wisconsin author, not a universal one.

`ncsu_ext` (verbatim, the "Resistance To Challenges" attribute, confirmed on two independent fetches
with different prompt framings to guard against the WebFetch label/value shift):

> "Deer, Heat, Humidity, Insect Pests, Poor Soil, Slugs"

This is a checkbox attribute in a plant-toolbox database. It asserts resistance. It gives no
mechanism, no prose, and no citation. For completeness, the NCSU "Problems" field is
`"Problem for Cats, Problem for Dogs, Problem for Horses"` -- that is pet toxicity, not plant pests;
there is **no** "Insects/Diseases/Other Plant Problems" field on this record at all.

**The mechanism half of the claim is carried by none of the three, and is contradicted by a fourth
T1 source.**

The record asserts, in consumer prose and without hedge:

> `pests[0].symptoms_seasoned`: "an effect attributed to the citral-rich essential oils in its foliage that repel many insects"
> `pests[0].symptoms_beginner`: "Its own lemony oils keep most bugs away, so outdoor plants usually look clean."
> `pests[0].cause_beginner`: "Lemongrass makes lemony oils that many insects dislike, so it is naturally left alone."
> `pests[0].name`: "Generally pest-resistant (aromatic-oil deterrence)"

Here is every sentence about oils in the three cited documents, verbatim and in full:

`usu_ext`, in its uses/background section, nowhere near the pest section:

> "Lemongrass oil is used in soap, perfume, makeup, hair products, a cleaning agent, antifungal agent, incense and potpourri."
> "It is also used as an effective, non-toxic insect repellent."

That is a claim about **extracted oil as a manufactured product**. USU makes no causal link between
that sentence and its "generally free of pests" sentence. The record's mechanism is a weld of two
unrelated sentences from the same page.

`ncsu_ext`, the whole of what it says about oils:

> "The plant oils are used for perfumes and herbal medicines."

Perfume and medicine. Not repellency, and not the plant's own pest status.

`uwi_hort`, the whole of what it says about repellency:

> "The related citronella grass (_C. nardus_) is the source of commercial citronella oil, which is used in soaps, as a mosquito repellent in insect sprays and candles and in aromatherapy."

This is the trap the task named, and it is worse than a scope error: the sentence is about a
**different species** (*C. nardus*, which this crop's own `varieties` block correctly warns is not
the culinary plant), about a **commercial extracted oil**, and about **manufactured products**
(sprays, candles). Mahr's only other citral sentence is
`"The main constituent of both species of lemongrass, citral, has a refreshing, lemony smell is also a strong, cleansing antiseptic."`
-- antiseptic, not insecticidal.

**A T1 UC Master Gardener source refutes the growing-plant version of the mechanism outright.** UC
Master Gardeners of Solano County, 2020-07-24, verbatim:

> "just growing it may not repel one 'Skeetter', since the oil in the plant has the repellent properties, and it must be extracted to use"
> "Although the oil from Citronella grass has been shown to be effective as an ingredient in insect repellent, there are also studies that show no significant improvement"

and, on the "mosquito plant" geranium:

> "studies have shown them ineffective in repelling mosquitos"

I also hunted for any extension source stating that the growing plant deters its own pests via its
oils. Nothing. Every hit was either a commercial garden blog or peer-reviewed work on **applied**
lemongrass essential oil as a contact insecticide or topical repellent (for example the *Agrotis
ipsilon* bioassay work). Applying an extract to a target is not the same claim as a plant defending
itself in the ground, and no admitted source makes the second claim.

**Verdict on Q1: the absence claim holds on three anchors with two qualifiers the record has
stripped. The mechanism claim has zero anchors, is contradicted by a T1 UC MG document, and is an
authoring inference.**

### Q1b. This exact claim was already adjudicated once, and the fix landed in one field out of six

`verification_status.verification_log_ref`, batch-2 wave-4 cert dated 2026-07-06, says verbatim:

> "softened the pests[0] repellent line -- dropped the unsupported 'geraniol' and the 'natural insect repellents, which is why lemongrass and its relatives are used' inference -> 'aromatic oils (notably citral) are used in insect-repellent products'."

and claims:

> "NO mosquito-repellent and NO health/medicinal over-claim (full-file scan clean; ... repellent framed as products + 'traditional rather than proven')."

The softening is real and correct: `pests[0].cause_seasoned` today reads
`"The plant's aromatic oils (notably citral) are used in insect-repellent products."`, which is a
clean product claim and is anchored by the USU sentence above. But the "full-file scan clean" claim
is **false as of this canonical**. I scanned every string field in the record. The unsoftened
plant-deters-its-own-pests claim is still live in **six** fields:

| field | live text |
|---|---|
| `pests[0].name` | "Generally pest-resistant (**aromatic-oil deterrence**)" |
| `pests[0].symptoms_seasoned` | "an effect attributed to the citral-rich essential oils in its foliage that repel many insects" |
| `pests[0].symptoms_beginner` | "Its own lemony oils keep most bugs away" |
| `pests[0].cause_beginner` | "Lemongrass makes lemony oils that many insects dislike, so it is naturally left alone." |
| `description_seasoned` | "Because its own essential oils repel many insects, it is notably free of pest problems" |
| `description_beginner` | "it is rarely bothered by insects, since its own lemony oils keep many pests away" |

By contrast `companions` handles the same claim honestly, labelling it
`provenance.label: "traditional"`, `confidence: "low"`, `verified_against_sources: false`, and saying
in `note_seasoned` "treat the pest-deterrent benefit as traditional rather than proven at garden
scale". So the crop already contains the correct hedge and contradicts itself between blocks.

Per the append-only convention, the cert-dated `verification_log_ref` must NOT be rewritten into
current tense. The correct handling is to leave its prose byte-for-byte and APPEND:
`[CORRECTION 2026-09-04: the "full-file scan clean" claim did not hold -- the aromatic-oil deterrence mechanism remained live in pests[0].name, pests[0].symptoms_seasoned, pests[0].symptoms_beginner, pests[0].cause_beginner, description_seasoned and description_beginner. See batch-25 record pass.]`

### Q2. Precedent in the dataset for a non-problem entry: there is none. This is a population of one.

I walked all 128 crops and all **912** problem entries in `crops_data_final.json` (all are dict
entries; there are no legacy string entries left). Matching names against a deliberately wide net
(`general|resist|free of|rarely|few |no major|no serious|seldom|troubl|problem-free|pest-free|none|minimal|uncommon|not usually|low pest|deterren|aromatic`) returns exactly one hit:

```
('lemongrass', 'pests', 'Generally pest-resistant (aromatic-oil deterrence)', 'pest', None, False, 'low')
```

**No other crop in the roster has a problem entry that asserts absence rather than naming an
organism.** 823 of the 912 entries carry a `control_ladder`, across 101 crops. **Not one laddered
entry is an absence assertion.** So the answer to "did any such entry receive a control_ladder" is
no, because no such entry exists anywhere else to have received one.

The nearest structural neighbors are not really neighbors: physiological entries (12 across the
roster, all laddered, type `physiological`) name a real disorder with a real cause, such as blossom
end rot. An absence has no cause to ladder against.

### Q3. Recommendation: **RETIRE the entry. Merge the surviving, sourced content into prose.**

A control ladder is a least-invasive-first sequence of methods applied to an organism. This entry has
no organism, so a ladder against it has no target. The best a ladder could contain is
`even_watering` / `airflow_spacing` / `garden_sanitation` -- generic vigor advice which (a) is
already the `prevention_*` text on the entry, (b) is already the substance of the crop's `watering`
and `container_notes` blocks, and (c) would be identical to the vigor rungs on the spider-mite entry
sitting directly beneath it. That is a ladder that duplicates its neighbor and treats nothing. Building
it would also mint a permanent `id` join key for a non-organism, which `variety_resistance_gate` and
`variety_ladder_delta_gate` would then be able to point at.

There is also a live consumer-safety edge. The entry currently tells a reader in beginner register
that lemongrass repels its own pests. Sitting immediately below it is the crop's real pest, spider
mites, which is genuinely common on exactly the plants most readers will have (potted, overwintered
indoors). Leading with "bugs leave this plant alone" ahead of "your indoor plant will get mites"
inverts the advice order.

Retirement precedent exists and is recent: batch 24 retired the chives aphids entry on a comparable
finding.

**What to retire:** the entire `pests[0]` entry.

**What to keep, and where:** the sourced absence claim is real and is worth telling the reader. It
belongs in prose, with its two qualifiers restored, not as a pest record. Proposed substance for the
`description_*` fields (replacing the current oil-mechanism sentence, which must go regardless of
whether the entry is retired):

- seasoned register: lemongrass is generally free of pests and diseases when it is grown well
  (`usu_ext`), and has essentially no pest problems in the upper Midwest (`uwi_hort`); NC State rates
  it resistant to insect pests, deer and slugs (`ncsu_ext`). The problems worth watching are rust
  where the summer is warm and humid, and spider mites on plants overwintered indoors.
- beginner register: same, in everyday words, without any claim that the plant's oils do the work.

**If the authoring pass overrules retirement and keeps the entry**, then the minimum bar is: rename
to drop the mechanism (for example `Generally pest-free when grown well`), rewrite all four prose
fields to remove the oil-deterrence causal claim, restore the "when grown correctly" and "in the
Midwest" qualifiers, and give it a ladder of at most `even_watering` and `airflow_spacing` with notes
that say plainly these keep the plant vigorous rather than that they control anything. I do not
recommend this path.

**Either way, the six-field mechanism claim in Q1b must be corrected**, because five of those six
fields survive the retirement of `pests[0]`.

---

## Generally pest-resistant (aromatic-oil deterrence) [pests] -- severity low, type `pest`

STATUS: **WRONG** (split claim: the absence half is SOURCED-OK on three anchors; the mechanism half,
which is what the entry's `name` asserts, has no anchor and is refuted by a T1 UC MG document)

ORGANISM: **none -- this entry names no organism, because it asserts an absence.** Not resolvable,
and that is the finding rather than a gap.

ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/lemongrass-in-the-garden -- verified 2026-09-04
  > "Lemongrass is generally free of pests and diseases when grown correctly."
  > "Lemongrass oil is used in soap, perfume, makeup, hair products, a cleaning agent, antifungal agent, incense and potpourri."
  > "It is also used as an effective, non-toxic insect repellent."
- `uwi_hort` https://hort.extension.wisc.edu/articles/lemongrass/ -- verified 2026-09-04
  > "Lemongrass has essentially no pest problems in the Midwest."
  > "The related citronella grass (_C. nardus_) is the source of commercial citronella oil, which is used in soaps, as a mosquito repellent in insect sprays and candles and in aromatherapy."
- `ncsu_ext` https://plants.ces.ncsu.edu/plants/cymbopogon-citratus/ -- verified 2026-09-04
  > Resistance To Challenges: "Deer, Heat, Humidity, Insect Pests, Poor Soil, Slugs"
  > "The plant oils are used for perfumes and herbal medicines."
- `uc_mg` https://ucanr.edu/blog/under-solano-sun/article/through-garden-gate-repelling-summer-mosquitoes-citronella -- verified 2026-09-04 (REFUTING anchor, found on hunt, not currently cited)
  > "just growing it may not repel one 'Skeetter', since the oil in the plant has the repellent properties, and it must be extracted to use"

RECORD CLAIMS THAT HOLD:
- "Healthy in-ground lemongrass rarely shows insect damage" -- `usu_ext`, `uwi_hort`, `ncsu_ext`.
- "Extension guides describe it as essentially free of pest problems when grown well" -- `usu_ext` ("when grown correctly"), `uwi_hort` ("essentially no pest problems"). Accurate paraphrase; the plural "guides" is earned.
- `cause_seasoned`: "The plant's aromatic oils (notably citral) are used in insect-repellent products." -- `usu_ext` ("It is also used as an effective, non-toxic insect repellent"). This is the one field a prior pass already fixed, and it is correct.
- "Robust, well-watered clumps in full sun are the least attractive to pests" -- consistent with `usu_ext`'s "when grown correctly"; the full-sun and well-watered specifics are inference, not text.

RECORD CLAIMS WITH NO ANCHOR:
- `name`: "**(aromatic-oil deterrence)**" -- no source attributes the plant's pest freedom to its oils.
- "an effect **attributed to the citral-rich essential oils in its foliage that repel many insects**" -- attributed by whom? Not by any of the three cited documents. This phrasing ("attributed to") reads as reported consensus and there is none.
- "Its own lemony oils keep most bugs away" (beginner).
- "Lemongrass makes lemony oils that many insects dislike, so it is naturally left alone" (beginner).
- "Scattered chewing or a few sap-feeders may appear on stressed or crowded plants" -- no source describes chewing damage or sap-feeders on lemongrass. USU names spider mites only.
- "Remove and destroy badly damaged outer leaves" and "divide crowded clumps so air moves through them" -- reasonable culture, not in any cited document for this purpose.

RECORD CLAIMS THAT ARE WRONG:
- The oil-deterrence mechanism, as a statement about the growing plant. Refuted by `uc_mg` Solano: "just growing it may not repel one 'Skeetter', since the oil in the plant has the repellent properties, **and it must be extracted to use**". The only repellency any source attributes to the genus is to *C. nardus* commercial citronella oil in manufactured products (`uwi_hort`), which is a different species from this crop.
- Implicitly wrong by omission: the entry generalizes pest freedom to all conditions, while both supporting sources qualify it ("when grown correctly"; "in the Midwest") and USU's own table immediately names a pest that is a routine problem indoors.

LADDER-RELEVANT FACTS the record does not carry:
- None that are usable, which is the point. There is no organism, no threshold, no monitoring
  signal, no timing, no overwintering stage and no resistant variety, because there is no pest.

---

## Spider mites (indoor and hot, dry conditions) [pests] -- severity low, type `pest`

STATUS: **SOURCED-OK**

ORGANISM: family **Tetranychidae**; no document pins a binomial for lemongrass. The overwhelmingly
likely species indoors is *Tetranychus urticae*, but **no source I read names any species on
*Cymbopogon***, so it must not be asserted. `ucanr_ext_spider_mites` (Pest Notes 7405) treats
*Tetranychus urticae* as the common garden and houseplant species generally. Sibling roster entries
split between the umbrella id `spider-mites` (16 crops) and the species-pinned
`two-spotted-spider-mite` (6 crops); the umbrella is correct here.

ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/lemongrass-in-the-garden -- verified 2026-09-04, "Pests and Disease" -> "Insects" table
  > Spider Mites -- Identification: "Piercing type pest that feed on plants cell contents causing tiny yellow or white speckling. Mostly an indoor plant problem."
  > Spider Mites -- Control: "Use insecticidal soaps, registered insecticides or spray plant with a forceful jet of water to dislodge the insects."

  (The UF/IFAS Nassau County republication of this same USU text renders the identification line as
  "Problem mostly on indoor plants." Same authors, same document, so it is a wording variant, not a
  second source.)
- AVAILABLE UNUSED ANCHOR, already in the catalog and already the sibling standard on 16 crops:
  `ucanr_ext_spider_mites` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html -- verified 2026-09-04, UC ANR Pub 7405, L.D. Godfrey, updated 12/2011
  > "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants adjacent to dusty roadways or at margins of gardens. Plants under water stress also are highly susceptible."
  > "Spider mites are common pests of fruit trees, vegetables, berries, vines, houseplants, and ornamental plants."
  > "In gardens and on small fruit trees, regular, forceful spraying of plants with water often will reduce spider mite numbers adequately."
  > "If more control is required, use an insecticidal soap or oil in your spray."
  > "Spider mites have many natural enemies that often limit their numbers in many landscapes and gardens, especially when undisturbed by pesticide sprays."

RECORD CLAIMS THAT HOLD:
- "Fine stippling or a dusty, faded look on the leaf blades" -- `usu_ext` "tiny yellow or white speckling".
- "most often on plants overwintered indoors" -- `usu_ext` "Mostly an indoor plant problem". This is the record's best-anchored sentence and the scoping in the entry `name` is correct and earned.
- "hot, dry" driver -- `ucanr_ext_spider_mites` "prefer hot, dusty conditions... Plants under water stress also are highly susceptible" (needs the anchor added; `usu_ext` alone does not carry the hot/dry driver).
- "Rinse the foliage with a strong spray of water" -- `usu_ext` "spray plant with a forceful jet of water to dislodge the insects"; `ucanr_ext_spider_mites` "regular, forceful spraying of plants with water".
- "treat persistent infestations with insecticidal soap or horticultural oil" -- `usu_ext` "Use insecticidal soaps"; `ucanr_ext_spider_mites` "use an insecticidal soap or oil in your spray".

RECORD CLAIMS WITH NO ANCHOR:
- "sometimes with delicate webbing where the leaf meets the stem" -- webbing is real for Tetranychidae generally but neither cited document mentions webbing on lemongrass. `ucanr_ext_spider_mites` would carry webbing generically if added.
- "Heavy feeding bronzes and dries the foliage" -- not in `usu_ext`.
- "raise humidity around indoor plants" and "keep indoor humidity up with misting or a nearby water tray" -- not in either document. Note `usu_ext` does say, for a different reason (Utah's dry climate), "In Utah's dry climate, it should be misted and regularly watered", which is a watering instruction, not a mite control.
- "Cutting the plant back hard before bringing it indoors reduces the mite population it carries in." -- **not anchored**. `usu_ext`'s overwintering text is only "Bring potted plants indoors when temperatures cool in the fall", "After harvest or before the first fall frost, save a 6 inch section of the bulbous shoot base", and "Small container plants can be overwintered indoors." The cut-back is real practice and appears in the crop's own `container_notes.overwintering`, but no source ties it to mite reduction. This is a plausible inference stated as fact.
- "covering the leaf undersides" -- correct practice, carried by `ucanr_ext_spider_mites` if that anchor is added; not in `usu_ext`.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS the record does not carry:
- **A timing hook the ladder should use**: the risk window is the indoor overwintering period, which
  this crop already has a notification for (`notif_lemongrass_pre_frost`, first_frost minus 10 days)
  and a documented practice at (`container_notes.overwintering`). Inspect-before-bringing-in is the
  cheapest rung available and it lands on an existing calendar event.
- `usu_ext` explicitly admits "registered insecticides" as an option. The record's
  `organic_treatment_*` silently drops that. The conventional-disclosure convention should decide
  whether a conventional rung is stated with its profile rather than omitted.
- **Natural enemies / biological rung is available and unused**: `ucanr_ext_spider_mites` carries
  both the conservation statement ("many natural enemies that often limit their numbers... especially
  when undisturbed by pesticide sprays") and the release option ("The major predator mites
  commercially available for release are the western predatory mite and _Phytoseiulus_").
- Dust as a driver ("Dusty conditions often lead to mite outbreaks") is a distinct cultural rung the
  record never mentions.
- No threshold or monitoring count is published for this crop by any source.
- `container_notes.container_specific_pests` already lists `spider_mites`, so the crop's container
  block and this entry must stay consistent after any rename.

---

## Lemongrass rust [diseases] -- severity medium, type `disease`

STATUS: **SOURCED-OK** for the disease, the organism and the management. But several specific
sentences in the record are sourced from a document that is NOT cited, and one is sourced from a
journal that is not in the catalog. See below.

ORGANISM: ***Puccinia nakanishikii* Dietel**, per UH-CTAHR PD-57, which prints the binomial with its
authority. **Confirmed a different organism from the Lamiaceae rusts in this batch, on document
evidence rather than assumption** -- see the host paragraph quoted below.

ANCHORS:
- `uhawaii_ctahr` https://www.ctahr.hawaii.edu/oc/freepubs/pdf/PD-57.pdf -- verified 2026-09-04.
  **URL NOTE: this 302-redirects to https://www3.ctahr.hawaii.edu/oc/freepubs/pdf/PD-57.pdf. The
  record's stored URL still resolves, so it is not dead, but the www3 host is where the file
  actually lives and is the better stored value.** The PDF has no usable text layer; it was read as
  page images. Full citation: **"Rust of Lemongrass", Scot Nelson, Department of Plant and
  Environmental Protection Sciences, Plant Disease, Nov. 2008, PD-57, UH-CTAHR.**

  > "Lemongrass plants in Hawai'i often have an abnormal number of brown and dying leaves. Depending on climatic conditions, lemongrass can become severely infected with a rust disease caused by Puccinia nakanishikii which is often responsible for the dying leaves."

  Host (this is the paragraph that settles the Poaceae question):

  > "West Indian lemongrass, Cymbopogon citratus (DC.) Stapf. (family Poaceae), called lanpine or lukini in Hawaiian, is a densely-tufted perennial grass native to southern India and Sri Lanka. **Other reported hosts of the rust disease pathogen are Cymbopogon nardus (in Sri Lanka) and perhaps some other species of Cymbopogon.**"

  Pathogen and distribution:

  > "Puccinia nakanishikii Dietel is a fungus first reported in Hawai'i in 1985. The disease has been reported in Hawai'i, California, New Zealand, and may be established in other locations where lemongrass is cultivated. It can occur virtually everywhere lemongrass grows in Hawai'i, but it is more severe in warmer, higher-rainfall locations."
  > "The rust occurs in both the uredinial and telial states in Hawai'i, the former producing lighter brown pustules than the latter. Pustules are produced on both upper and lower leaf surfaces. Ellipsoidal urediniospores measure about 22-28 um by 22-25 um and contain three or four germ pores in an equatorial pattern."
  > "Conditions favoring disease development are high rainfall, high humidity, and warm air temperatures. Wind disseminates spores among lemongrass plants."
  > "In Brazil, another rust of lemongrass caused by another Puccinia species (Puccinia cymbopogonis) has been reported. This disease has not been reported in Hawai'i."

  Disease cycle:

  > "Very little has been published about the disease cycle of lemongrass rust. Spores (mainly urediniospores) are dispersed by wind, splashing rain, or irrigation water. The spores land on wet or moist lemongrass leaves and may infect them during periods of very high relative humidity. Infections eventually result in lesions that release more spores to further spread infections. Spores may survive on infected or fallen lemongrass leaves."

  Symptoms:

  > "Initial symptoms are tiny, light yellow spots that develop into brown and elongated, stripe-like, brown lesions that coincide with leaf veins and develop on both sides of the leaf. Lesions on the lower leaf surface erupt and develop dark, cinnamon-brown uredinial pustules. Lesion development can be substantial, with coalescing lesions forming large leaf spots or blights and causing premature death of leaves."
  > "The principal negative effects of lemongrass rust on the plant are defoliation (direct effect) and poor leaf and oil yield (indirect effect). The rust disease is normally not fatal to lemongrass plants, even though defoliation may be severe."

  Integrated management practices, complete and verbatim:

  > "Keep plants growing vigorously; use composts, mulches, and fertilizer to stimulate growth."
  > "Intercrop or polycrop lemongrass with non-hosts of the pathogen; avoid planting large numbers of lemongrass plants close to one another."
  > "Do not purchase or distribute rusted plants."
  > "Grow plants under plastic or rainproof cover to protect their leaves from rainfall."
  > "Periodically prune, cut back, or thin out diseased lemongrass plants so that disease-free re-growth can occur; destroy diseased plant material (do not use it around pruned lemongrass plants as mulch)."
  > "Keep weeds under control to reduce relative humidity in the lemongrass plant canopy."
  > "Plant lemongrass in well drained soils in a relatively dry or well ventilated area to minimize the time of leaf wetness after rainfall."
  > "Minimize overhead irrigation; lemongrass grows well in dry areas."

  Fungicides and biological control:

  > "There is only one fungicide product registered for use on lemongrass rust in Hawai'i, Trilogy (Table 1). There is no published research in Hawai'i evaluating this product for controlling lemongrass rust."
  > "A potential biological control agent, a Darluca mycoparasite species, was often observed in uredinia of diseased lemongrass in coastal counties of California (Koike, 1999). It is unknown if this mycoparasite exists in Hawai'i, nor has the extent of the mycoparasitism and whether or not it provides effective disease control been determined."

  Food safety, which is a genuinely useful consumer fact the record omits entirely:

  > "Lemongrass plants with the rust disease are safe for humans to use in cooking recipes or as teas after drying the leaves, or as flavoring for beverages, or as additives to cosmetics."

**Is this a different organism from the batch's Lamiaceae rusts? Yes, on evidence.** PD-57 prints
the host family, "Cymbopogon citratus (DC.) Stapf. (family Poaceae)", and gives the pathogen's entire
reported host range as *Cymbopogon* only. Mint rust is *Puccinia menthae* on Lamiaceae. Two different
*Puccinia* species on two different plant families. Rusts are overwhelmingly host-specialized, and
PD-57's host paragraph states this one's range explicitly rather than leaving it to inference. There
is no shared-id case. This also matches the roster convention: every rust id in the dataset is
host-scoped -- `garlic-rust`, `leek-rust`, `elderberry-rust`, `fig-rust`, `asparagus-rust`,
`bee-balm-rust`, `sunflower-rust`, `chives-rust`, `bean-rust`, `orange-rust`, `broad-bean-rust`,
`common-rust`, `cedar-apple-rust`, `white-rust`. Note `chives-rust`, `sunflower-rust` and
`bee-balm-rust` all display as the bare name "Rust" while carrying a host-scoped id, which is the
exact precedent oregano's bare "Rust" should follow.

**Is it a real concern for mainland home growers, or region-specific? Region-weighted, but not
Hawaii-only, and the mainland evidence is journal-only.**
- PD-57 itself (2008) lists the distribution as "Hawai'i, California, New Zealand" and says it "may
  be established in other locations where lemongrass is cultivated". California is already mainland.
- The Florida report is **JOURNAL-ONLY**: Ploetz et al., first report of *P. nakanishikii* on
  *Cymbopogon citratus* in Florida, *Plant Disease* 98(1):156 (2014). I could not read it directly
  (apsjournals.apsnet.org returned **403** to fetch, a paywall, not a dead URL); the details below
  come from the abstract as returned by search and must be treated as second-hand.
- A further **JOURNAL-ONLY** item: "First Report of a Rust Fungus (*Puccinia* sp.) Infecting
  Lemongrass in Minnesota", *Plant Disease*, PDIS-10-22-2314-PDN. Also 403. Notable because the
  pathogen was **not resolved to species** in the title, and because Minnesota is well outside the
  humid subtropics, which weakens any claim that this is a warm-region-only problem.
- **No admitted-catalog source outside `uhawaii_ctahr` publishes on lemongrass rust.** I checked
  UF/IFAS Gardening Solutions (no pest content at all), UF/IFAS Nassau County (a USU republication,
  no rust), USU (no rust in its disease table), Wisconsin Horticulture (no rust), UIUC (no rust),
  UC MG Santa Clara (no rust), NC State toolbox (no disease field). That is a document-scoped
  absence over eight documents, not a claim that no extension anywhere publishes it.

**Severity call.** `medium` is defensible but is anchored to Hawaii. The honest reading of PD-57 is
that the disease is common and damaging where it occurs, is "normally not fatal", and is "more
severe in warmer, higher-rainfall locations". For a US home grower the realistic exposure is the
humid Southeast, Gulf, coastal California and Hawaii, plus overwintered indoor plants anywhere.
`medium` is fine; the record's prose should stop implying it is universal.

RECORD CLAIMS THAT HOLD:
- Organism *Puccinia nakanishikii* -- PD-57, binomial with authority.
- "the University of Hawaii CTAHR documents it" -- PD-57 is exactly that.
- "favored by warm, humid weather" -- PD-57 "high rainfall, high humidity, and warm air temperatures".
- "Spores spread on wind and splashing water" -- PD-57 "dispersed by wind, splashing rain, or irrigation water".
- "Remove and destroy heavily infected leaves to reduce spore load" -- PD-57 "prune, cut back, or thin out diseased lemongrass plants... destroy diseased plant material".
- "open the clump up by dividing and thinning to improve airflow" -- PD-57 "thin out", "relatively dry or well ventilated area".
- "Water at the base rather than overhead so leaves dry quickly" / "avoid overhead irrigation in humid weather" -- PD-57 "Minimize overhead irrigation".
- "culture is the primary control" -- correct, and PD-57 supports it strongly by showing the chemical option is a single unevaluated product.
- "crowded, poorly ventilated plantings" -- PD-57 "avoid planting large numbers of lemongrass plants close to one another".

RECORD CLAIMS WITH NO ANCHOR:
- "**it has been reported on Florida lemongrass**". PD-57 predates the Florida report by six years and
  lists only "Hawai'i, California, New Zealand". The Florida claim is real but its source is the 2014
  APS note, which is **JOURNAL-ONLY and not in the catalog**. As it stands the record attributes a
  Florida claim to a document that does not make it. Either drop the Florida sentence, replace it
  with PD-57's own distribution ("Hawai'i, California, New Zealand"), or open a catalog-addition
  decision for the APS note.
- "**Small chlorotic (yellow) flecks appear on both leaf surfaces and enlarge into reddish to crimson
  streaks; on the leaf underside these rupture into powdery orange-brown pustules.**" This is not
  PD-57's symptom description. PD-57 says "tiny, light yellow spots", "brown and elongated,
  stripe-like, brown lesions", "dark, **cinnamon**-brown uredinial pustules". The words "crimson",
  "flecks", "streaks" and "rupture" track the **Florida journal abstract** ("small chlorotic flecks on
  both leaf surfaces that became crimson and enlarged to streaks ~1 cm in length. On the abaxial side
  of leaves, erumpent streaks ruptured to produce pustules"). The record's symptom prose is
  paraphrased from an uncited journal note and credited to CTAHR. This is a mis-anchored claim and
  should be rewritten off PD-57's own wording, which is both admitted and better.
- "large patches of **tan to purplish** dead tissue" -- no source uses those colors. PD-57 says
  "coalescing lesions forming large leaf spots or blights and causing premature death of leaves"; its
  photo caption says "entirely brown and blighted leaves".
- "**the most notable disease of lemongrass** in humid tropical and subtropical areas" -- PD-57 calls
  it "this common and damaging disease" and quantifies commercial impact. It never ranks it against
  other diseases. Superlative unsupported.
- "**Copper-based fungicides** can be used preventively where rust pressure is high" -- **not
  supported and arguably wrong.** PD-57 is explicit: "There is only one fungicide product registered
  for use on lemongrass rust in Hawai'i, Trilogy". Trilogy is a neem-oil product, not a copper. No
  cited source recommends copper on lemongrass. This is a generic rust reflex applied to a crop whose
  own T1 document says otherwise, and it should not survive into a ladder rung.
- "cutting yield and quality" -- close to PD-57's "poor leaf and oil yield", but PD-57 frames that as
  the commercial effect; for a home grower the effect it names is defoliation.
- "Vigorous, uncrowded plants **in full sun** resist rust best" -- vigor and spacing are PD-57's;
  "full sun" is not, and PD-57's actual siting advice is "a relatively dry or well ventilated area".

RECORD CLAIMS THAT ARE WRONG:
- The copper-fungicide recommendation, measured against PD-57's registered-product sentence quoted
  above. At minimum it is unanchored advice on a food crop; at worst it points a reader at a product
  that is not the one the crop's only T1 disease document names.

LADDER-RELEVANT FACTS the record does not carry (PD-57 is unusually rich here and the ladder should
be built from it directly):
- **Overwintering / inoculum survival**: "Spores may survive on infected or fallen lemongrass
  leaves." This makes fallen-leaf sanitation a real, sourced rung, and it makes PD-57's
  "do not use it around pruned lemongrass plants as mulch" a specific and important warning the
  record does not have.
- **Infection requirement**: "The spores land on wet or moist lemongrass leaves and may infect them
  during periods of very high relative humidity." Leaf wetness duration is the lever; this is the
  mechanism behind the base-watering rung.
- **Weed control as a disease rung**: "Keep weeds under control to reduce relative humidity in the
  lemongrass plant canopy." Entirely absent from the record and a genuinely least-invasive rung.
- **Do not import the problem**: "Do not purchase or distribute rusted plants." A zero-cost rung, and
  especially apt for a crop most people start from a bought division or a grocery stalk.
- **Polyculture rung**: "Intercrop or polycrop lemongrass with non-hosts of the pathogen." Note this
  sits awkwardly beside the crop's `companions` block, which currently justifies neighbors by an
  unsupported repellent mechanism; PD-57 gives a real, sourced reason to interplant.
- **Rain exclusion**: "Grow plants under plastic or rainproof cover to protect their leaves from
  rainfall." Probably too much for most home growers, but it is what the source recommends and it
  should be a considered omission rather than an unnoticed one.
- **Chemical rung, correctly**: Trilogy is the only registered product in Hawaii, and PD-57 states
  plainly there is "no published research in Hawai'i evaluating this product". Any chemical rung must
  carry that caveat, and must not say copper.
- **Biological rung, honestly**: the *Darluca* mycoparasite is observed, not established as control.
  PD-57's hedging is explicit and should not be laundered into a recommendation.
- **Food safety**: "Lemongrass plants with the rust disease are safe for humans to use in cooking
  recipes or as teas after drying the leaves." This is the single most useful consumer sentence in
  PD-57 and the record does not have it anywhere.
- **Prognosis**: "normally not fatal to lemongrass plants, even though defoliation may be severe."
  Sets the right expectation and argues against panic escalation.
- **A live tension with the rest of the crop record**: PD-57 says "Plant lemongrass in well drained
  soils in a relatively dry or well ventilated area" and "lemongrass grows well in dry areas", while
  the crop's `water` field is `"High"` and `watering.drought_tolerance` is `"low"` and the prose says
  "Keep the root zone consistently moist". Independently, `uc_mg` Santa Clara rates its water
  requirement as **"Moderate"**, not high. These are reconcilable (drainage and canopy dryness are
  not the same as soil moisture) but the record never reconciles them, and the rust ladder will read
  oddly next to "water deeply 2-3 times per week" unless it does.
- No resistant variety is published by any source. No monitoring threshold is published.

---

## Leaf blight [diseases] -- severity low, type `disease`

STATUS: **SOURCED-WEAK** -- the disease name is genuinely in the cited document, so this is not a
WRONG finding, but the anchor is a two-cell table row with no organism, and essentially all of the
record's prose exceeds it.

ORGANISM: **cannot be resolved from any admitted source.** `usu_ext` names no pathogen. Every
organism-level report I could find is **JOURNAL-ONLY**:
- *Curvularia affinis* causing leaf blight on *Cymbopogon citratus* in Brazil -- *Journal of Plant Pathology* (2022), doi 10.1007/s42161-022-01159-2.
- *Curvularia andropogonis* (Zimm) Boedjin, leaf blight of lemongrass, Chhattisgarh, India.
- *Curvularia nanningensis* sp. nov., described from diseased *Cymbopogon citratus* in China (PMC7033261), confirmed pathogenic on *C. citratus* leaves.
- *Curvularia cymbopogonis*, reported as causing severe disease of lemongrass in lowland Guatemala.
- EPPO lists *C. citratus* as a host of *Colletotrichum fructicola*.

The genus **Curvularia** is the consistent answer across four independent reports on three
continents, so "a *Curvularia* leaf blight" is very likely the right identification. **It cannot be
stated in the record on current admissions**, and the four reports name four different *Curvularia*
species, so even with the journals admitted the honest resolution is genus-level, not species-level.
I checked for an extension fact sheet naming an organism at USU, UF/IFAS (Gardening Solutions and
Nassau County), Wisconsin Horticulture, UIUC, UC MG Santa Clara, NC State toolbox and UH-CTAHR
PD-57. None names one. PlantVillage, which aggregates CABI plus the Linse and Drost text, does not
list leaf blight on lemongrass at all -- only rust.

Report as **JOURNAL-ONLY for the taxon** and a catalog-addition decision, not as a silent gap.

ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/lemongrass-in-the-garden -- verified 2026-09-04, "Pests and Disease" -> "Diseases" table
  > Leaf Blight -- Symptom: "Reddish brown spots on leaf tips and margins; leaves appear to prematurely dry out"
  > Leaf Blight -- Control: "Spray with registered fungicides if positively identified or hand remove blighted leaves."

  (UF/IFAS Nassau County, same authors, republished: "Reddish brown spots on leaf tips and margins;
  appear to be prematurely drying." Not independent.)

RECORD CLAIMS THAT HOLD:
- That lemongrass gets a leaf blight at all -- `usu_ext`. This is the whole of what the anchor establishes.
- "browning and drying the foliage from the tips and margins inward" -- `usu_ext` "spots on leaf tips and margins; leaves appear to prematurely dry out". Well matched.
- "Remove affected leaves" -- `usu_ext` "hand remove blighted leaves".

RECORD CLAIMS WITH NO ANCHOR:
- "**Brown, elongated lesions** develop along the leaf blades" -- `usu_ext` says "Reddish brown **spots**", and locates them at tips and margins, not along the blades. Elongated blade lesions are the description of **rust** in PD-57 ("brown and elongated, stripe-like, brown lesions that coincide with leaf veins"). The record's leaf-blight symptom prose has drifted toward its neighbor entry and should be rewritten to USU's actual words, or the two entries will describe the same thing.
- "in warm, wet weather" -- not in `usu_ext`. No cited source gives a weather driver for this disease.
- "can spread quickly through dense plantings" -- not in `usu_ext`.
- "A foliar leaf-blight fungus" -- `usu_ext` does not say fungus, and does not name an organism. (The `disease` type value cannot be upgraded to `fungal` on this document alone; see the type section below.)
- "favored by prolonged leaf wetness, high humidity, and crowding" -- not in `usu_ext`. This is rust's epidemiology from PD-57 transplanted onto a different disease.
- "**it is the second disease of note for lemongrass** grown in humid regions" -- no source ranks lemongrass diseases. USU's own table lists three, and the record carries only one of them.
- "thin or divide crowded clumps", "switch to base watering", "Avoid working in or harvesting from wet plants, which spreads spores" -- all reasonable, none in `usu_ext`.
- "**Copper-based products** can be used preventively under heavy pressure" -- unanchored, same defect as the rust entry. `usu_ext` says "Spray with registered fungicides if positively identified", which is a materially different and much more cautious instruction: it conditions spraying on a confirmed diagnosis.

RECORD CLAIMS THAT ARE WRONG: none outright, but the symptom description is closer to rust than to
the blight USU describes, and if left as written the two disease entries will not be distinguishable
by a reader.

LADDER-RELEVANT FACTS the record does not carry:
- **`usu_ext`'s control instruction is conditional on identification**: "Spray with registered
  fungicides **if positively identified**". That condition is a ladder rung in itself (diagnose before
  you spray) and it is the source's own framing.
- `usu_ext` admits registered fungicides; the record's organic-only framing drops that. Conventional
  disclosure convention applies.
- **The record omits a third disease USU publishes.** `usu_ext`'s disease table has three rows, not
  two: Spider Mites under Insects, and under Diseases both "Leaf Blight" and
  > Little Leaf or Grassy Shoot -- Symptom: "Stunted growth of normal inflorescence." Control: "Spray with registered fungicides if positively identified."

  This is a **record-completeness finding**, and I flag it with a caution: "little leaf" and "grassy
  shoot" name phytoplasma diseases in the grass literature (the sugarcane grassy shoot phytoplasma,
  16SrXI group), for which "spray with registered fungicides" is not effective advice. I could not
  find a source that resolves the organism on *Cymbopogon* in the US, and lemongrass is grown for
  leaves and stalks rather than inflorescence, so the practical relevance to a home grower is low. My
  recommendation is **do not add it**, and record here that it was seen, considered and declined,
  rather than leaving it to be re-found as a gap by a later audit.
- No threshold, no timing, no resistant variety, no overwintering information exists in any admitted
  source for this disease.

---

## Root rot (overwatering in poor drainage) [diseases] -- severity medium, type `disease`

STATUS: **SOURCED-OK** as a cultural caution. Both cited documents carry it, in almost exactly the
record's framing. Neither names an organism, and neither describes symptoms.

ORGANISM: **cannot be resolved.** Correctly an **umbrella -- multiple soilborne organisms**. No
admitted source names a pathogen; no source of any kind that I found reports a named root rot
pathogen on *Cymbopogon citratus* in a US garden context. The generic answer for a waterlogged
monocot is the usual soilborne oomycete and fungal complex (*Pythium*, *Phytophthora*, *Fusarium*),
and the roster already has an entry that says exactly that at exactly this confidence level: the
`tomatillo` entry under id `root-and-stem-rots` has
`cause_seasoned: "Soilborne oomycetes and fungi favored by waterlogging and poor drainage."` That is
the right register for lemongrass too.

**Can it share an id with the batch's Lamiaceae rots? No -- and it should not need to.** Oregano and
sage carry "Root and stem rot", rosemary and thyme "Root and crown rot", lavender "Phytophthora root
and crown rot". Lavender's is species-pinned to *Phytophthora* and must stay separate. The other four
are unpinned umbrellas on woody Lamiaceae subshrubs whose defining risk is lean, sharply drained soil
and whose management advice is "do not water it like a vegetable". Lemongrass is the opposite plant:
a monocot grass with a high water demand whose failure mode is a pot standing in a saucer. Sharing an
id would let a future `varieties[].resistance` grade or `ladder_delta` written for a Mediterranean
subshrub attach itself to a tropical grass.

The correct move is the roster's **existing generic umbrella id `root-and-stem-rots`**, already
shared by tomatillo, marigold, borage, sweet-alyssum, echinacea and sweet-pea, all of which use it
for exactly this "soilborne rot in wet soil" case and all of which ladder it with `improve_drainage`
first. That is a proven, non-colliding, precedent-backed id, and it does not force a Lamiaceae
relationship. If the authoring pass prefers host-scoping, `lemongrass-root-rot` is free (I checked all
912 entries; no collision). I recommend reusing `root-and-stem-rots`.

ANCHORS:
- `uiuc_ext` https://extension.illinois.edu/herbs/lemon-grass -- verified 2026-09-04
  > "water as needed to keep soil moist. Do not overwater as that can lead to root rot."
  > "When grown in pots use pots with ample drainage holes and filled with a prepared soil mix."
- `uc_mg` https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/lemongrass -- verified 2026-09-04
  > Water: "Moderate; do not overwater to avoid root rot"
  > Soil: "Well-drained. Fertilize regularly with nitrogen during the growing season"
- Supporting, already cited elsewhere on the crop: `uhawaii_ctahr` PD-57
  > "Plant lemongrass in well drained soils in a relatively dry or well ventilated area to minimize the time of leaf wetness after rainfall."

RECORD CLAIMS THAT HOLD:
- "It appears when a thirsty plant is grown in soil that stays waterlogged" -- `uiuc_ext` and `uc_mg` both.
- "especially in containers with poor drainage" -- `uiuc_ext` "use pots with ample drainage holes".
- "Soil-borne rot organisms take hold when drainage is poor" -- correct at genus-unspecified level; matches the roster's `root-and-stem-rots` register.
- "drainage is as important as watering volume" -- fair reading of both sources, and of PD-57.
- "Improve drainage, repot into a free-draining mix" -- `uiuc_ext` "prepared soil mix", `uc_mg` "Well-drained".

RECORD CLAIMS WITH NO ANCHOR:
- "Yellowing, wilting, and collapse of stalks despite wet soil, with soft, dark, decayed roots and stalk bases" -- **neither cited source describes any symptom at all.** Both say only "do not overwater, it can cause root rot". The entire symptom block is generic root-rot knowledge. It is not wrong, but it is unanchored and should be labelled as such rather than presented as sourced observation on this crop.
- "There is no cure once roots are extensively rotted; remove affected plants." -- generic, unanchored.
- "empty saucers after watering" / "never let the pot sit in standing water" -- not in either cited document, though it is standard and appears elsewhere in this crop's own `container_notes.drainage.saucer_practice_*`.
- "Although lemongrass demands abundant water" -- this is the record's own framing, and it sits against `uc_mg`, the source cited on this very entry, which rates the crop's water need as **"Moderate"**. See the tension note below.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS the record does not carry:
- **The first rung is settled and sourced**: `improve_drainage`, exactly as the six sibling
  `root-and-stem-rots` entries already do it. `uiuc_ext`'s "pots with ample drainage holes" is a
  container-specific version that reads well for beginners.
- PD-57 gives an unexpected second benefit for the same rung: well-drained, well-ventilated siting
  reduces **leaf wetness** and therefore rust pressure. One cultural action, two diseases. That is a
  strong ladder note.
- There is no chemical rung to offer. No source names a product, and none should be invented.
- No monitoring signal, threshold, timing or resistant variety exists in any source.
- **Cross-field tension the authoring pass must resolve, not inherit**: `water` is `"High"`,
  `watering.drought_tolerance` is `"low"`, and `watering.frequency_seasoned` says "deeply 2-3 times
  per week in heat, containers often daily", while `uc_mg` (cited on both the watering block and this
  entry) says **"Moderate"** and PD-57 says "lemongrass grows well in dry areas". The record already
  half-notices this and papers over it with "water deeply and often while never letting the root zone
  stagnate". It is outside my subject, but a rot ladder written on top of an unexamined "High" water
  value will give confusing advice, so I am flagging it rather than leaving it.

---

## TYPE VALUES: the coarse `pest` / `disease` flag

**Flagged, and the task's framing needs one correction.** Lemongrass is the only crop **in batch 25**
carrying the coarse values, but it is **not** the only crop in the roster. Computed over all 128
crops and all 912 problem entries:

| type | count |
|---|---|
| `insect` | 380 |
| `fungal` | 320 |
| `bacterial` | 73 |
| `mite` | 30 |
| *(null)* | 20 |
| **`pest`** | **16** |
| `mollusk` | 14 |
| `viral` | 13 |
| **`disease`** | **13** |
| `physiological` | 12 |
| `vertebrate` | 12 |
| `nematode` | 7 |
| `other` | 2 |

The 29 coarse-typed entries sit on **five** crops: `pomegranate` (7), `persimmon` (7), `mulberry` (6),
`pawpaw` (4) and `lemongrass` (5). Every one of those five crops is un-laddered: no `id`, no
`control_ladder`. **Zero of the 823 laddered entries anywhere in the roster carry `pest` or
`disease`.** So the coarse values are not a lemongrass defect so much as a marker of "has not been
through PLA-8 yet", and they are resolved as part of laddering. Within batch 25, the outlier worth a
separate note is `mint`, whose six entries carry `type: null` rather than a coarse value.

Within batch 25 the sibling values are:

| crop | typing |
|---|---|
| lemongrass | `pest` x2, `disease` x3 |
| mint | `null` x6 |
| oregano | `insect` x2, `fungal` x3 |
| rosemary | `insect` x3, `fungal` x2 |
| sage | `insect` x2, `mite` x1, `mollusk` x1, `fungal` x3 |
| thyme | `insect` x2, `fungal` x2 |
| lavender | `insect` x2, `fungal` x2 |

### Proposed values, with evidence

| entry | current | proposed | evidence |
|---|---|---|---|
| Generally pest-resistant (aromatic-oil deterrence) | `pest` | **n/a -- retire the entry** | no organism exists to type |
| Spider mites | `pest` | **`mite`** | Tetranychidae are Acari, not insects. `ucanr_ext_spider_mites` (Pest Notes 7405) is the standing anchor. Roster precedent, computed: 31 entries have "spider mite" in the name; **25 are typed `mite`**, and all 25 laddered spider-mite crops use `mite`. The 6 that do not are mint (`null`), thyme, rosemary, oregano and lemongrass -- five of the seven batch-25 crops -- plus nasturtium, whose combined "Whiteflies and spider mites" entry is led by whiteflies under id `whiteflies`, so `insect` is defensible there |
| Lemongrass rust | `disease` | **`fungal`** | PD-57: "a rust disease caused by Puccinia nakanishikii"; "Puccinia nakanishikii Dietel **is a fungus** first reported in Hawai'i in 1985". Roster precedent, computed: 26 rust entries sit in `diseases[]`; **all 24 that carry a specific type value are `fungal`**. The only two that do not are the two in this batch (mint `null`, lemongrass `disease`) |
| Leaf blight | `disease` | **`fungal`, but only if the authoring pass accepts the *Curvularia* genus-level reading** | `usu_ext` does not say fungus and names no organism. The four journal reports are all *Curvularia*, an ascomycete. Roster precedent, computed: 52 blight-named entries, of which **43 are `fungal` and 7 are `bacterial`**; every one of the 7 is a genuinely bacterial disease by name (fire blight x3, bacterial blights x4). The only 2 left coarse are mulberry's "Bacterial blight" and this entry. If the pass will not accept journal-derived typing, `fungal` is still the safer of the two available values, since `usu_ext` prescribes fungicides |
| Root rot (overwatering in poor drainage) | `disease` | **`fungal`** | No organism is named by any source, but the roster's identical umbrella entries all use `fungal`: `root-and-stem-rots` on tomatillo, marigold, borage, sweet-alyssum, echinacea and sweet-pea, and `crown-and-root-rot` on parsley and viola. Following the umbrella's own precedent rather than inventing a value |

### Sibling typing for the same organisms elsewhere in the dataset

- **Spider mites**: `mite` on cherry-tomato, beefsteak-tomato, heirloom-tomato, grape-tomato,
  slicing-cucumber, pickling-cucumber, english-cucumber, cucumber, eggplant, watermelon, cantaloupe,
  honeydew-melon, strawberry, artichoke, marigold, zinnia, cosmos, bee-balm, viola, sweet-pea,
  green-beans-bush, pole-beans, edamame, dry-bean, and the citrus mites. Ids split between the
  umbrella `spider-mites` (16 crops) and the pinned `two-spotted-spider-mite` (6 crops).
  **Four batch-25 siblings are miscoded**: oregano, rosemary and thyme all type spider mites as
  `insect`, and mint leaves it `null`; only sage has `mite`. Together with lemongrass that is five of
  the seven crops in this batch. That is a cross-crop defect this batch is positioned to fix, and it
  is not mine to fix alone -- flagging it for the batch owner.
- **Rusts**: `fungal` on all 24 rust `diseases[]` entries that carry a specific type, and always
  host-scoped ids -- `garlic-rust`, `leek-rust`,
  `elderberry-rust`, `fig-rust`, `asparagus-rust` (name carries the binomial: "Asparagus rust
  (Puccinia asparagi)"), `bee-balm-rust`, `sunflower-rust`, `chives-rust`, `bean-rust`,
  `orange-rust`, `broad-bean-rust`, `common-rust`, `cedar-apple-rust`, `white-rust`.
- **Leaf blights**: `fungal` for fungal blights (`carrot-leaf-blight`, `alternaria-leaf-blight`,
  `early-blight`, `late-blight`, `phomopsis-blight`, `gummy-stem-blight`, `southern-blight`,
  `ascochyta-blight`, `cane-blight`, `stem-blight`, `botrytis-blossom-blight`), `bacterial` for
  bacterial ones (`fire-blight`, `bacterial-blights`).
- **Root rots**: `fungal` for the umbrellas (`root-and-stem-rots`, `crown-and-root-rot`,
  `root-rots-damping-off`, `bean-root-rots`, `damping-off`) and for the pinned ones
  (`phytophthora-root-rot`, `phytophthora-foot-rot`, `fusarium-basal-rot`, `fusarium-crown-rot`,
  `red-stele`); `bacterial` only where the pathogen is bacterial (artichoke's
  `bacterial-crown-rot`, "Dickeya, formerly Erwinia chrysanthemi").

---

## ID PINNING NOTE (for the authoring pass)

Per the join-key rule, ids are pinned at first authoring and never re-derived. None of lemongrass's
five entries carries an `id` today, so this batch mints all of them. Collision-checked against all
912 entries in the canonical:

| entry | proposed id | status |
|---|---|---|
| Spider mites | `spider-mites` | **exists on 16 crops** -- reuse the umbrella, same organism, same register. Do not mint a lemongrass-scoped variant |
| Lemongrass rust | `lemongrass-rust` | free; matches the host-scoped rust convention and does not collide with `citrus-rust-mite` or `carrot-rust-fly` |
| Leaf blight | `lemongrass-leaf-blight` | free. Do **not** use bare `leaf-blight`; the roster scopes blights by host or pathogen and a bare id would be a magnet for future mis-joins |
| Root rot | `root-and-stem-rots` | **exists on 6 crops** as the generic wet-soil umbrella -- reuse. `lemongrass-root-rot` is free as a fallback if host-scoping is preferred |
| Generally pest-resistant | *(none)* | retire; do not mint an id for a non-organism |

Cross-batch caution for whoever owns the batch: mint rust (*Puccinia menthae*) and oregano's bare
"Rust" are being authored in the same batch as `lemongrass-rust`. Three rusts, three different
organisms, three different plant families. Pin all three ids before fan-out.

---

## CONSUMER-COPY CONSTRAINT CHECK

Scanned all `symptoms_*`, `cause_*`, `organic_treatment_*` and `prevention_*` fields on all five
entries.

- **Em dashes**: none found. Clean.
- **American English**: clean.
- **Temperatures**: no temperature appears in any of the five problem entries, so `°F` rendering is
  not exercised here. (Elsewhere in the crop, `description_seasoned` renders "40 °F" correctly.)
- **"plant" lowercase**: clean; every occurrence is mid-sentence and lowercase.
- **Everyday words**: two flags in beginner register. `pests[0].symptoms_seasoned` uses "sap-feeders"
  and "chlorotic (yellow)" appears in the rust seasoned register with a gloss, which is fine, but
  `diseases[0].symptoms_beginner` inherits "flecks" and "streaks" from the journal wording. Minor.
- **Substantive copy problem, outside the mechanical constraints**: `pests[0].symptoms_beginner`
  ("Its own lemony oils keep most bugs away") states an unsupported causal mechanism in the register
  aimed at the least experienced reader. That is the constraint that actually matters here.

---

## OPEN FINDING THAT CAN BE CLOSED

`lemongrass_pilot_finding_003` is currently `open` and reads:

> "Rust disease anchored to uhawaii_ctahr PD-57 ('Rust of Lemongrass', Puccinia nakanishikii), which is a scanned PDF confirmed to exist and to cover the claim by title but NOT machine-readable this session (PDF fetch is denied). Rust symptomology and leaf-blight detail modeled from horticultural knowledge; confirm the exact CTAHR text and consider a UF/IFAS Florida rust report co-anchor at review."

Re-verified this session rather than assumed:

1. **PD-57 was read in full.** The 302 to `www3.ctahr.hawaii.edu` resolves; the PDF has no text layer,
   but all four pages were read as images. Every quotation in the rust section above is from that
   read. The document covers the claim in substance, not just by title.
2. The finding's own admission -- "Rust symptomology and leaf-blight detail **modeled from
   horticultural knowledge**" -- is confirmed and is now specific: the symptom prose tracks the 2014
   Florida journal abstract, not PD-57, and the leaf-blight prose has drifted toward rust.
3. The finding's suggested follow-up, "consider a UF/IFAS Florida rust report co-anchor", **resolves
   to nothing admissible**. UF/IFAS publishes no lemongrass rust document that I could find: Gardening
   Solutions has no pest content, and the Nassau County fact sheet is a republication of the USU text
   with no rust. The Florida report is the APS *Plant Disease* note (Ploetz et al. 2014), which is
   **JOURNAL-ONLY** and outside the catalog.

**Recommendation**: close `003` and replace it with a narrower finding covering the two live items --
the mis-anchored symptom prose and the unsupported copper recommendation -- plus, if desired, a
catalog-addition decision on the two APS notes.

---

## SUMMARY

**Counts by STATUS (5 entries):**

| STATUS | count | entries |
|---|---|---|
| SOURCED-OK | 3 | Spider mites; Lemongrass rust; Root rot |
| SOURCED-WEAK | 1 | Leaf blight |
| WRONG | 1 | Generally pest-resistant (aromatic-oil deterrence) |
| UNSOURCED-FOUND | 0 | |
| UNSOURCED-NOT-FOUND | 0 | |
| JOURNAL-ONLY | 0 as whole entries; **2 as sub-claims** | the leaf-blight *Curvularia* taxon; the Florida and Minnesota rust distribution reports |

Documents read: 12. Live: 11. Paywalled (403, not dead): 1 host (apsjournals.apsnet.org, 2 papers).
Redirects needing a stored-URL update: 1 (`uhawaii_ctahr` PD-57 -> `www3`). Pages with no readable
text layer requiring image extraction: 1 (PD-57).

**The single most important finding:**

**"Generally pest-resistant (aromatic-oil deterrence)" is not a problem, and its mechanism is an
authoring invention that a prior pass already caught, fixed in one field, and left live in five
others.**

The absence half is genuinely sourced three ways, with two qualifiers the record has stripped ("when
grown correctly", "in the Midwest"). The mechanism half -- that the plant's own citral-rich oils
repel its pests -- is carried by none of the three cited documents and is explicitly refuted by a T1
UC Master Gardener source: "just growing it may not repel one 'Skeetter', since the oil in the plant
has the repellent properties, **and it must be extracted to use**". The only repellency any source
attributes to the genus belongs to *C. nardus* commercial citronella oil in manufactured sprays and
candles, which is a different species from this crop and a product claim rather than a plant claim.
The batch-2 cert log records that this exact inference was identified and softened in
`pests[0].cause_seasoned` on 2026-07-06, and asserts "full-file scan clean" -- but the claim is still
live and unhedged in `pests[0].name`, `pests[0].symptoms_seasoned`, `pests[0].symptoms_beginner`,
`pests[0].cause_beginner`, `description_seasoned` and `description_beginner`, while `companions`
correctly labels the same claim `traditional` / `low` / `verified_against_sources: false`. The crop
contradicts itself.

**Recommendation: RETIRE the entry** (batch 24's chives precedent), merge the sourced absence claim
into `description_*` with its qualifiers restored, and correct all six fields. It is the only
absence-assertion problem entry in 912 across 128 crops, and not one of the 823 laddered entries in
the roster is anything like it, so retiring it costs no precedent and creates none.

**Runners-up, both actionable in the same pass:**

1. The rust entry recommends **copper fungicides** on a food crop whose only T1 disease document says
   plainly "There is only one fungicide product registered for use on lemongrass rust in Hawai'i,
   Trilogy" -- a neem product, not a copper. This must not reach a ladder rung as written. Meanwhile
   PD-57 carries eight sourced cultural practices, an inoculum-survival fact, a food-safety
   reassurance and an honest biological-control hedge that the record uses none of.
2. The rust symptom prose ("chlorotic flecks... crimson streaks... rupture") is paraphrased from the
   2014 APS Florida first report and credited to CTAHR, which says something different ("tiny, light
   yellow spots... dark, cinnamon-brown uredinial pustules"). Right document cited, wrong document
   quoted. Rewrite off PD-57, and either drop the Florida sentence or open a catalog-addition
   decision on the APS note.
