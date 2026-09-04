# PLA-8 BATCH 25 -- RECORD / SOURCE PASS: **OREGANO**

Reviewer: OREGANO record reviewer. Pass date: **2026-09-04**. All fetch dates below are 2026-09-04.
Canonical read-only: `a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`. No repo file was
modified; this report is the only output.

Record under review: `tools/staging/pla8_batch25_herbs/oregano_source.json`, keys `pests[]` (2) and
`diseases[]` (3). **Neither array carries any `id` field yet** -- oregano's problems are unpinned, so
batch 25 will mint every id on this crop for the first time. Mint's record in this same batch is also
unpinned. That makes the §4f naming call below a *live* decision for this batch, not a retro-fit.

## Documents actually opened (and what happened)

| Document | Host | Result |
|---|---|---|
| UC IPM, Oregano, `ipm.ucanr.edu/home-and-landscape/oregano/` | admitted `uc_ipm` | READ |
| UC IPM, Oregano cultural tips, `.../oregano/cultural-tips/index.html` | admitted `uc_ipm` | READ |
| UC IPM Pest Notes 7405 Spider Mites | admitted `ucanr_ext_spider_mites` | READ |
| UC IPM Pest Notes 7404 Aphids | `uc_ipm` host, no pathed key | READ |
| UF/IFAS Pasco Co. blog, "Spice Up Your Life... Growing Oregano" | admitted `uf_ifas` | READ (twice) |
| Penn State Extension, "Herb Garden Plants: Oregano" | admitted `psu_ext` | READ (twice) |
| RHS, oregano grow-your-own | admitted `rhs` | READ (twice) |
| RHS, Mint rust advice profile | admitted `rhs` | READ |
| NC State Ext., "Phytophthora Blight and Root Rot on Annuals and Herbaceous Perennials" | admitted `ncsu_ext` | READ (twice) |
| NC State Plant Toolbox, *Origanum vulgare* | `plants.ces.ncsu.edu` (sibling-pathed to `ncsu_ext_lavandula_angustifolia`) | READ |
| UConn IPM, "Rust Diseases on Ornamental Crops" (Pundt, rev. 2024) | admitted `uconn_ext` (different subdomain, see note) | READ (pypdf, 10,195 chars) |
| WSU, "Management of Rust on Mint" (D. A. Johnson) | `s3.wp.wsu.edu` (sibling-pathed to `wsu_em051e`/`wsu_em057e`) | READ (full .doc text extracted) |
| UMass Ext., "Botrytis Blight of Greenhouse Crops" | `ag.umass.edu` (sibling-pathed to `umass_ext`) | READ |
| UF/IFAS EDIS PP172/PP256, "Rusts on Ornamentals in Florida" | admitted `uf_ifas_edis` | READ, 5 pp. -- **contains zero occurrences of oregano/Origanum/marjoram/mint/menthae/herb.** Ruled out. |
| Univ. of Delaware Coop. Ext., Oregano fact sheet | `udel.edu` -- NOT in catalog | READ |
| PlantVillage, oregano | `plantvillage.psu.edu` -- NOT in catalog | READ |
| PubMed 30856788 (Koike et al. 1998 abstract) | `pubmed.ncbi.nlm.nih.gov` -- NOT in catalog | READ, full abstract |
| APS: `apsjournals.apsnet.org` (3 URLs), `apsnet.org` (1 URL) | -- | **HTTP 403 on every attempt.** Not read. Per rule 5 I am reporting these as *unreadable*, not absent. |
| PNW Plant Disease Handbook, mint rust | `pnwhandbooks.org` | **HTTP 403.** Not read. |
| Illinois `extension.cropsciences.illinois.edu` "MINT RUST" PDF | -- | **TLS failure** (`unable to verify the first certificate`) on both http and https. Not read. |
| `nt.ars-grin.gov` USDA Fungus-Host DB | -- | **DNS failure** (`ENOTFOUND`). Not read. |
| Springer, "Diseases of Oregano and Marjoram" | -- | 303 to auth wall. Not read. |
| USDA PubAg | -- | 301 to a JS discovery app. Not read. |

Note on `uconn_ext`: the catalog key points at `https://ipm.cahnr.uconn.edu`; the fact sheet lives at
`ipm-cahnr.media.uconn.edu`. Same program, different media subdomain. Flagging the divergence rather
than silently treating the key as covering it.

Note on WebFetch reliability: WebFetch reported the UConn PDF as "primarily image-based (JPEG
streams) with minimal extractable text." That was **false** -- pypdf extracted 10,195 characters of
clean text from the same file. Every PDF/DOC quote in this report was extracted locally with pypdf or
a byte-level read, not taken from WebFetch's PDF summary.

---

# §4f RULING EVIDENCE

**PLA-448 §4f asks: is oregano's bare display name "Rust" an umbrella covering several rust fungi by
intent, or one specific organism nobody ever pinned?**

## Verdict: it is ONE SPECIFIC ORGANISM THAT NOBODY PINNED. Not an umbrella.

Three independent lines of evidence, all pointing the same way:

**1. Every source that names oregano's rust at all names exactly one disease, and names it "mint
rust."** Not one source I read offers a second rust on *Origanum* in the US. Three sources, two of
them catalog-admitted:

- **`psu_ext`** -- Penn State Extension, "Herb Garden Plants: Oregano",
  `https://extension.psu.edu/herb-garden-plants-oregano`, last updated April 22, 2026, fetched
  2026-09-04. Under the heading "Pests and Diseases":
  > "Oregano can be susceptible to fungal diseases such as mint rust and root rot."

  Confirmed on a second, independently prompted fetch. The page does **not** contain the words
  "Puccinia", "powdery mildew", "Botrytis", "gray mold", "airflow", "air circulation" or "overhead".

- **`rhs`** -- RHS, "Oregano / Grow Your Own", `https://www.rhs.org.uk/herbs/oregano/grow-your-own`,
  fetched 2026-09-04. Under "Problem Solving > Common Problems", heading "Mint rust":
  > "The fungal disease mint rust can affect oregano"

  and the entry body:
  > "Mint rust is a common fungal disease of garden mint, but also affects marjoram and savory. The
  > fungus causes dusty orange, yellow and black spots on l..." (truncated at fetch)

  RHS's own oregano page settles the common-name ambiguity that would otherwise defeat the RHS mint
  rust profile: it states *Origanum vulgare* is "generally referred to as oregano" although "one of
  its common names is 'wild marjoram'", and that *O. majorana* and *O. onites* are "generally
  recognised as marjoram". So the RHS mint rust profile's host list ("Garden mints, marjoram and
  savory") is *Origanum*-inclusive by RHS's own usage, and the oregano page removes any doubt by
  naming oregano directly. **The word "rust" appears exactly twice on the RHS oregano page, both in
  the "Mint rust" entry.** No second rust.

- **Univ. of Delaware Coop. Extension**, Oregano fact sheet (Rick Judd and Gail Hermenau, New Castle
  County Master Gardeners), `https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/oregano/`,
  fetched 2026-09-04. Under "Common Pests & Diseases": "Aphids", "Spider Mites", "Thrips",
  **"Mint Rust"**, "Blight". `udel.edu` is **not** in the catalog -- corroboration only, not an anchor.

**2. The primary literature reports exactly one rust binomial on *Origanum* in the US:
*Puccinia menthae*.** From the PubMed record of the California first report -- full abstract quoted
verbatim below in the Rust section -- "The rust was identified as *Puccinia menthae*." The Florida
work reaches the same binomial. I found no US report of any other rust on *Origanum*. The one
contrary lead I chased, a UK trade guide (HDC Herb Best Practice Guide, `britishherbguide.co.uk`,
content current March 2013) listing "*Puccinia menthae, Puccinia thymi*" for oregano, is (a) not a
catalog source, (b) UK-scoped, and (c) unconfirmed anywhere in the US literature I could reach. It is
a lead worth recording, not a basis for an umbrella.

**3. The record's own prose does not behave like an umbrella.** It says "**a** rust fungus favored
by..." -- singular, indefinite. Compare the record's genuinely-umbrella disease #3, whose prose says
"Foliar fungi **such as** Botrytis (gray mold) **and** powdery mildew" and whose display name carries
the umbrella in the name itself. Oregano's rust prose was written about one organism; it just never
said which one.

## What organism the literature reports on *Origanum vulgare* in the US

***Puccinia menthae*** Pers. Given by:

**Koike, S. T., Subbarao, K. V., Roelfs, A. P., Hennen, J. F., and Tjosvold, S. A. 1998. "Rust
Disease of Oregano and Sweet Marjoram in California." Plant Dis. 82(10):1172.
DOI 10.1094/PDIS.1998.82.10.1172C.** Abstract read verbatim from PubMed record 30856788
(`https://pubmed.ncbi.nlm.nih.gov/30856788/`), fetched 2026-09-04:

> "In 1996 and 1997, a rust disease was detected on commercial, field-grown oregano (Origanum
> vulgare) and sweet marjoram (Origanum majorana) in coastal California. Symptoms on both plants were
> similar and mostly consisted of small (2 to 5 mm in diameter), circular, brown, necrotic leaf spots
> that developed cinnamon brown pustules in the center of the spot or in concentric groups on the spot
> periphery. Pustules sometimes developed without spots. On sweet marjoram, leaf spots were sometimes
> surrounded by a chlorotic halo. Teliospores were not detected on either host. Ellipsoidal
> urediniospores measured 22 to 25 μm by 19 to 22μm and contained 2 to 3 germ pores in an equatorial
> configuration. **The rust was identified as Puccinia menthae.** Pathogenicity was tested by
> depositing urediniospores onto leaves of healthy plants and then incubating plants in a humidity
> chamber for 48 h. Urediniospores from oregano infected Italian (Origanum× majoricum), Sicilian
> (Origanum × marjorana), trailing (O. prostrata), and Greek (O. heracleoticum) oregano, and sweet
> marjoram. Urediniospores from sweet marjoram infected sweet marjoram and the one oregano tested,
> Italian oregano. With all inoculations, both symptoms and fungal fruiting bodies were similar to
> those observed in the field. **Neither the oregano nor the sweet marjoram isolates infected spearmint
> (Mentha spicata), which is consistent with previous studies (1,2).** This is the first report of a
> rust disease of oregano and sweet marjoram in California. Rust significantly reduced the quality and
> yield of both crops."

Note the taxon check: this is *Origanum vulgare* by name, the crop's own species. Not a common-name
match.

Second US report, **not read** (403): Stiles, C. M., and Rayside, P. A. 2006. "Host Range of Rust
Isolates on Oregano and Mint in Florida." Plant Health Progress 7(1).
DOI 10.1094/PHP-2006-0417-01-RS. Authors and year confirmed from the Semantic Scholar Graph API
record for that DOI (fetched 2026-09-04), which explicitly notes the abstract has been "elided by the
publisher". Direct fetches of `apsjournals.apsnet.org/doi/...` and `apsjournals.apsnet.org/doi/pdf/...`
both returned HTTP 403; the article body was never seen. Search-index summaries consistently render
its finding as: urediniospores collected in Gainesville, FL in April 2004 and March 2005; morphology
consistent with *P. menthae*; rust developed on oregano, sweet marjoram and Greek oregano only from
the oregano isolate and that isolate infected no *Mentha* sp.; the spearmint isolate infected
spearmint but not peppermint, oregano, sweet marjoram or Greek oregano; conclusion that the two
isolates "appear to represent different populations, 'spearmint rust' and 'oregano rust.'"
**I am labelling all of that as second-hand and unread.** It corroborates Koike but I did not see the
sentences.

## Is it the SAME organism as mint rust? Yes by binomial. No by population.

- **Same binomial.** Both mint rust and oregano rust are *Puccinia menthae*. Oregano's record and
  mint's record in this same batch would name the identical species.
- **Different host-specialized populations that do not cross-infect.** This is documented at two
  levels:

  (a) **Oregano vs mint, verbatim, from the Koike abstract above:** "Neither the oregano nor the sweet
  marjoram isolates infected spearmint (*Mentha spicata*), which is consistent with previous
  studies." The Florida study (unread, 403) is reported to have closed the reciprocal direction: the
  spearmint isolate did not infect oregano.

  (b) **Host-specialized races within *P. menthae* are documented by a T1 extension source**, which
  matters because it means this is not a lone journal curiosity. Washington State University, D. A.
  Johnson, "Management of Rust on Mint" (`https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/MintrustA.doc`,
  fetched 2026-09-04, full text extracted locally):
  > "Two principal types of races of P. menthae have been recognized. One type infects Native
  > spearmint but not peppermint and is called native spearmint rust; the other, peppermint rust,
  > infects peppermint but not Native spearmint. Both groups of races infect Scotch spearmint, but
  > native spearmint rust is more aggressive on Scotch spearmint than is peppermint rust."

  WSU applies exactly the naming convention in question -- one binomial, races named for the host they
  actually infect ("native spearmint rust", "peppermint rust") -- inside a single T1 extension
  document. That is the precedent for `mint-rust` and `oregano-rust` being two ids.

**Ruling I recommend, for the id-minting pass:** keep them as **two ids, host-scoped**
(`oregano-rust` on oregano, mint's own id on mint). The consumer-facing consequence is the reason:
these are not interchangeable. A gardener with rusty mint six feet from the oregano is not looking at
an oregano inoculum source, and vice versa; the "rip out the mint to save the oregano" advice that
one shared id would license is not supported by the evidence. Two ids is also what PLA-448 §4f's six
named-rust siblings and the `bee-balm-rust` / `sunflower-rust` host-scoped precedent already do.

**Display name: rename "Rust" to "Mint rust".** Not to "Oregano rust". The two catalog-admitted
sources that name this disease on oregano (`psu_ext`, `rhs`) both call it *mint rust*, and so does the
non-admitted UDelaware sheet and PlantVillage. "Mint rust" is what a gardener will find when they
search. A crop-scoped **id** (`oregano-rust`) under a source-faithful **display name** ("Mint rust")
satisfies §4f's join-key concern and the sourcing at the same time. If the batch prefers name/id
symmetry, "Oregano rust (mint rust)" also works, but inventing a bare "Oregano rust" that no source
uses does not.

## Can the claim be anchored to a catalog-admitted T1 source? YES -- two of them.

Not JOURNAL-ONLY. This is a hunt-before-downgrading outcome:

1. **`psu_ext`** -- `https://extension.psu.edu/herb-garden-plants-oregano` -- names mint rust on
   oregano. **`psu_ext` is already in oregano's existing citation vocabulary.**
2. **`rhs`** -- `https://www.rhs.org.uk/herbs/oregano/grow-your-own` -- names mint rust on oregano.
   `rhs` is catalog-admitted T1 but is *not* currently in oregano's vocabulary; adding it is a
   vocabulary extension, not a catalog addition.
3. Supporting detail (organism biology, control) -- **`rhs`** mint rust profile
   `https://www.rhs.org.uk/disease/mint-rust` names *Puccinia menthae* and carries the hot-water
   treatment.

**JOURNAL-ONLY components** (real, useful, unanchorable today): the binomial *tied specifically to
Origanum vulgare*, and the cross-inoculation / host-specialization evidence. No catalog-admitted
source states either about oregano. Koike 1998 (via PubMed) and Stiles & Rayside 2006 (unread) are
the only sources for it. If PLA-8 wants the record to *say* "*Puccinia menthae*", that requires a
catalog decision. Candidates, in the order I would rank them:
- **`pubmed`** (`pubmed.ncbi.nlm.nih.gov`) -- .gov, stable, gives verbatim abstracts, and would
  unblock this class of gap repeatedly across the dataset. Note it anchors an *abstract*, not a
  document the reader can read in full.
- **`udel_ext`** (`udel.edu` cooperative extension) -- T1 land-grant extension, but it only gets you
  "Mint Rust" as a name, which `psu_ext` already gives.
- **`plantvillage`** (`plantvillage.psu.edu`) -- names "Mint rust (*Puccinia menthae*)" for oregano
  with symptoms and the hot-water protocol, i.e. it is almost certainly where this record's prose came
  from originally. It is a Penn State property but a **different subdomain** from the admitted
  `psu_ext` (`extension.psu.edu`), it carries no author byline or review date, and its oregano entry
  lists **no root rot at all** despite root rot being the crop's top killer. I do **not** recommend
  admitting it.

## Does the record's current rust prose survive?

**Mostly yes on the symptoms. The cause and treatment prose is generic foliar-disease boilerplate
that misses this pathogen's actual life cycle, and one sentence is affirmatively risky.**

- **Survives.** "Small circular spots and orange or brown powdery pustules on the leaves and stems" --
  Koike: "small (2 to 5 mm in diameter), circular, brown, necrotic leaf spots that developed cinnamon
  brown pustules". "Orange" is right for the genus and is what RHS and WSU describe ("golden to
  cinnamon brown"); on *Origanum* specifically the published color is cinnamon brown. Close enough to
  stand; "orange or brown" is not wrong.
- **Survives, but only generically.** "favored by damp, crowded, poorly ventilated conditions and
  overhead watering" -- no oregano-scoped source says this. It is supported for rusts in general by
  UConn ("Mild, moist conditions favor the development of rust diseases... They need wet leaf surfaces
  to germinate and cause infection... Space plants properly to provide for good air circulation
  between plants") and for *P. menthae* specifically by WSU ("Wet, cloudy weather and prolong leaf
  wetness from irrigation, dew, and rainfall favor rust development"). Nothing in it is refuted.
- **Nothing in the prose is factually WRONG.** But two things are materially misleading by omission,
  and one is close to bad advice:
  1. **The record never mentions that this pathogen carries over in the plant.** WSU: the telial stage
     on stubble "is the source of new infections the following spring", and greenhouse outbreaks "are
     usually initiated from systemic infections and pustules on rhizomes and stem cuttings used in
     propagation". RHS: "In the case of garden mint it is also necessary to remove infected rhizomes."
     Mint's own record in this batch already says "lives over on the roots and rhizomes from year to
     year." Oregano's says nothing. A reader is left believing this is a purely weather-driven leaf
     problem that tidiness fixes. **Caveat, honestly stated:** Koike found "Teliospores were not
     detected on either host" on *Origanum* in California, so the overwintering route on oregano
     specifically is *not documented*. The right fix is to say what is known and not silently import
     mint's rhizome story.
  2. **"Caught early, pruning off affected parts can save the plant" has no anchor and points the
     opposite way from every control source I read.** RHS: "Remove affected plants promptly before the
     black resting spores are formed." WSU's non-chemical levers are burning off systemically infected
     shoots with nitrogen and heat-treating propagation material, not spot pruning. UConn: "remove all
     rust-infected leaves **and heavily infected plants**". Mint's sibling record says outright "There
     is no reliable home cure once it is established." This sentence is the single most defect-shaped
     thing in oregano's rust record.
- **`severity: "medium"` is defensible but is the low end of the evidence.** Koike: "Rust
  significantly reduced the quality and yield of both crops."

## The UC IPM record gap (reported, not acted on)

**Confirmed myself:** UC IPM's oregano page (`https://ipm.ucanr.edu/home-and-landscape/oregano/`,
fetched 2026-09-04) identifies the crop as "*Origanum vulgare*", "Family Lamiaceae (Mint family)" and
lists, under **Invertebrates**: Aphids, Leafhoppers, Spider Mites, Spittlebugs, Thrips. Under
**Environmental Disorders**: Cold Injury and Frost Damage; Common Environmental Disorders of
Vegetables. Under **Weeds and Other Unwanted Plants**: Weed Management in Vegetable Crops.
**There is no Diseases section on the page at all.**

Two consequences:

1. **Oregano's three disease records have no UC IPM basis, and never did.** The record does not claim
   one -- disease #1 cites `uf_ifas`, and #2/#3 cite nothing -- so this is not a mis-pointed key. It
   does mean UC IPM cannot be used to source any oregano disease.
2. **Record gap: Leafhoppers, Spittlebugs and Thrips.** UC IPM names three invertebrates oregano's
   record does not carry. Thrips is triple-named: UC IPM, `uf_ifas` ("it can be susceptible to certain
   insects like aphids, spider mites, and thrips"), and the UDelaware sheet. Penn State adds a fourth
   and fifth the record also lacks: "Some potential insect pests include leaf miners, thrips, and
   cutworms", and NC State's Plant Toolbox independently names leaf miners ("Susceptible to fungal
   diseases, aphids, leaf miners and spider mites"). PlantVillage resolves them to *Frankliniella
   occidentalis* (western flower thrips), *Agrotis* spp. (cutworms) and *Tetranychus urticae*.
   **Reporting only.** Worth flagging that the catalog has an admitted pathed thrips anchor sitting
   unused (`ucanr_ext_thrips`, `https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html`), so a thrips entry
   would be cheap. Spittlebugs and leafhoppers are UC-IPM-listed but low-consequence on a culinary
   herb and I would not add them without a second source.

---

# RECORD PASS -- all 5 problems

## Aphids [pests] -- severity low, type insect
STATUS: **SOURCED-OK** (existing anchor is thin but valid; two better anchors available)
ORGANISM: umbrella, aphids generally. UC IPM's oregano page names only "Aphids" with no genus.
PlantVillage resolves oregano's to *Myzus persicae* (green peach aphid) -- **not catalog-admitted, and
not corroborated by any admitted source, so do not put a binomial in this record.**
ANCHORS:
- `uc_ipm` `https://ipm.ucanr.edu/home-and-landscape/oregano/` -- verified 2026-09-04. Page confirmed
  live and confirmed to list Aphids under Invertebrates. This anchors *presence on the crop* and
  nothing else -- the page is a link index, not prose.
- **RECOMMENDED ADDITION** `psu_ext` `https://extension.psu.edu/herb-garden-plants-oregano` --
  verified 2026-09-04:
  > "Aphids, spider mites, and white flies, which are often repelled by the aroma of oregano emitted
  > by mature plants, can be a problem for young seedlings."

  This one sentence anchors *both* currently-unanchored distinctive claims in this record.
- **RECOMMENDED ADDITION** `uc_ipm` (pathed) `https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html` --
  verified 2026-09-04. Note the catalog has no aphid Pest Note key; `ucanr_ext_spider_mites` and
  `ucanr_ext_thrips` exist as pathed siblings, so a `ucanr_ext_aphids` key would be a consistent
  addition. Quotes: "Spray aphids with a strong stream of water to knock them off sturdy plants."
  / "Where aphid populations are localized on a few curled leaves or new shoots, the best control may
  be to prune out these areas and dispose of them." / "Insecticidal soaps and oils are the best
  choices for most situations" / "High levels of nitrogen fertilizer favor aphid reproduction, so
  never use more nitrogen than necessary." / "Check your plants regularly for aphids-at least twice a
  week when plants are growing rapidly-in order to catch infestations early." / "Ants protect aphids
  from natural enemies".

RECORD CLAIMS THAT HOLD:
- Aphids occur on oregano -- `uc_ipm` oregano page; also `uf_ifas` ("it can be susceptible to certain
  insects like aphids, spider mites, and thrips"), `ncsu_ext` toolbox, `psu_ext`.
- "Mature oregano's aroma tends to repel them" -- `psu_ext`, verbatim above. **This was unanchored
  before this pass and it is TRUE.**
- "most likely on young seedlings" / "mainly at the seedling stage" -- `psu_ext`, same sentence
  ("can be a problem for young seedlings"). Also previously unanchored.
- "Knock them off with a strong spray of water" -- UC IPM Pest Notes 7404.
- "use insecticidal soap or neem if numbers climb" -- UC IPM 7404 for soaps and oils. **Neem
  specifically is not named by any source I read.**
- "avoid overwatering" / lean soil -- UC IPM oregano cultural tips: "Damp soil surfaces encourage
  snails, slugs, sowbugs, and root diseases".
- Spacing for airflow -- UC IPM oregano cultural tips: "Space plants at least 18 inches apart to
  accommodate their full size." (The source's stated *reason* is mature size, not airflow.)

RECORD CLAIMS WITH NO ANCHOR:
- "Oregano has few pests overall and is typically grown with little or no pesticide." Plausible and
  echoed in tone by `uf_ifas` ("oregano is relatively pest-resistant"), but the "little or no
  pesticide" half is an unsourced practice claim.
- "neem" as a named product. No source I read names neem for oregano aphids.
- "Vigorous, unstressed oregano rarely attracts aphids." Stress/vigor language is sourced for spider
  mites (water stress) but not for aphids. UC IPM's actual aphid-vigor claim runs the other way:
  excess nitrogen and lush new growth *favor* aphids.
- "A hard harvest removes much of the infested growth at once." Reasonable but unsourced; the nearest
  real support is UC IPM's "prune out these areas and dispose of them".
- "full sun" as an aphid measure.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS the record does not carry:
- **Nitrogen is a lever.** "High levels of nitrogen fertilizer favor aphid reproduction, so never use
  more nitrogen than necessary" (UC IPM 7404). A genuine cultural rung the record omits entirely.
- **Monitoring signal, published:** check at least twice weekly during rapid growth; check leaf
  undersides; damage peaks at 65-80 °F.
- **Ants.** "Ants protect aphids from natural enemies" -- an ant-exclusion rung, which this dataset
  has precedent for (PLA-8 batch 18 blocked on exactly this).
- **Natural enemies** (parasitic wasps, lady beetles, lacewings) and the instruction to avoid
  broad-spectrum insecticides -- a biological rung the record has no trace of.
- **Soap limits:** do not use soaps on drought-stressed plants or above 90 °F. That is a safety
  qualifier on the rung the record already recommends.

---

## Spider mites [pests] -- severity low, type insect
STATUS: **SOURCED-OK** (same shape as aphids: valid but thin; better anchors available)
ORGANISM: umbrella, spider mites generally. PlantVillage gives *Tetranychus urticae* (two-spotted
spider mite) -- not admitted, do not encode.
Note: `type: "insect"` is taxonomically wrong for a mite (Arachnida, not Insecta). Whether the schema's
`type` enum has an arachnid/mite value is outside my scope; flagging it because a reviewer should
decide, not because I know the enum.
ANCHORS:
- `uc_ipm` `https://ipm.ucanr.edu/home-and-landscape/oregano/` -- verified 2026-09-04. Lists "Spider
  Mites" under Invertebrates. Presence only.
- **RECOMMENDED ADDITION** `ucanr_ext_spider_mites` `https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html`
  -- verified 2026-09-04. **Already catalog-admitted and pathed.**
  > "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants adjacent
  > to dusty roadways or at margins of gardens. Plants under water stress also are highly susceptible."
  > "In gardens and on small fruit trees, regular, forceful spraying of plants with water often will
  > reduce spider mite numbers adequately."
  > "If a treatment for mites is necessary, use selective materials, preferably insecticidal soap or
  > insecticidal oil."
  > "Broad-spectrum insecticide treatments for other pests frequently cause mite outbreaks, so avoid
  > these pesticides when possible."
  > "Be sure mites are present before you treat. Sometimes the mites will be gone by the time you
  > notice the damage; plants will often recover after mites have left."
  > "Apply water to pathways and other dusty areas at regular intervals."
- **RECOMMENDED ADDITION** `psu_ext` `https://extension.psu.edu/herb-garden-plants-oregano` -- same
  aroma/seedling sentence quoted under Aphids, which names spider mites explicitly.

RECORD CLAIMS THAT HOLD:
- Spider mites occur on oregano -- `uc_ipm`, plus `uf_ifas` and `ncsu_ext` toolbox.
- "flare in hot, dry conditions" -- Pest Note 7405 ("hot, dusty conditions"). See the wording gap
  below.
- "do not let container plants bake bone-dry in a heat wave" -- 7405: "Plants under water stress also
  are highly susceptible."
- "Rinse plants with a strong spray of water" -- 7405, verbatim support.
- "use insecticidal soap if numbers build" -- 7405, verbatim support.
- "Fine stippling or yellowing on the leaves with faint webbing" -- standard 7405 symptom description.

RECORD CLAIMS WITH NO ANCHOR:
- **"hot, dry"** where the source says **"hot, dusty"**. Not wrong, but the record has dropped the
  actionable half. Dust is the lever a gardener can pull (wet the path); "dry weather" is not.
- "on stressed or indoor plants" / "on plants grown indoors". No source I read says indoor culture.
  Plausible from general horticulture, unanchored here.
- "Oregano is generally pest-resistant" -- `uf_ifas` says "oregano is relatively pest-resistant", so
  this is anchorable if `uf_ifas` is added to this entry; today it is not cited here.
- "A hard harvest or shear removes much of the infested growth."
- "full sun and good airflow" as mite measures.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS the record does not carry:
- **A published monitoring rule that gates the whole ladder:** "Be sure mites are present before you
  treat... plants will often recover after mites have left." That is a do-nothing rung, and it is the
  least-invasive rung there is.
- **Dust suppression** as a named cultural control ("Apply water to pathways and other dusty areas at
  regular intervals").
- **Predatory mites** as a purchasable biological rung ("The purchase and release of predatory mites
  can be useful in establishing populations in large plantings or orchards" -- note the source scopes
  this to large plantings/orchards, which is a caveat for a home-garden herb).
- **Broad-spectrum insecticides cause mite outbreaks.** A conventional-rung *warning*, and it is the
  strongest argument in the record for stopping the ladder before conventional.

---

## Root and stem rot [diseases] -- severity high, type fungal
STATUS: **SOURCED-OK, and upgradeable to a named pathogen genus at an admitted T1**
ORGANISM: **cannot be resolved to a single binomial -- it is genuinely a complex.** But it is no
longer nameless: ***Phytophthora* spp.** is named on oregano by `ncsu_ext`. Note *Phytophthora* is an
oomycete, not a true fungus, which puts pressure on `type: "fungal"` (see below).
ANCHORS:
- `uf_ifas` `https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/`
  -- Julia Sirchia, posted April 2, 2024. Verified live 2026-09-04 (fetched twice, independently
  prompted):
  > "Oregano is generally resistant to diseases, but it can occasionally suffer from fungal infections
  > like powdery mildew or root rot."
  > "Root rot occurs when oregano plants are exposed to excessive moisture, leading to fungal
  > infections and root decay."
  > "Remove affected plants promptly to prevent the spread of disease."
  > "Improve soil drainage and avoid overwatering to prevent root rot."
  > "Oregano is drought-tolerant, so it will struggle if it is sitting in standing water or grown in
  > soil that is waterlogged."
- **RECOMMENDED ADDITION** `ncsu_ext` `https://content.ces.ncsu.edu/phytophthora-blight-and-root-rot-on-annuals-and-herbaceous-perennials`
  -- Inga Meadows, Suzette Sharpe, Amanda Scherer, Ella Hinchliffe, Sara Villani. Verified 2026-09-04,
  quotes confirmed on a second independently prompted fetch. **`ncsu_ext` is already in oregano's
  citation vocabulary.**
  > "Herbaceous perennials that are susceptible to *Phytophthora* include lavender, osteospermum,
  > rosemary, delphinium, epimedium, **oregano**, polemonium, hosta, heuchera, euphorbia, and others."
  > "species of *Phytophthora* present in North Carolina prefer warm, humid, and wet conditions."
  > "Prolonged irrigation or watering, poor drainage, and standing water all favor disease
  > development."
  > "Affected roots would appear brown to black or roots may be mostly decayed."
  > "The pathogen can survive in soil from season to season, so once the bed is infested the pathogen
  > cannot be eradicated without extreme measures."
  > "There is a lack of OMRI-approved products that effectively manage diseases caused by
  > *Phytophthora* species."
- **RECOMMENDED ADDITION** `ncsu_ext` (toolbox) `https://plants.ces.ncsu.edu/plants/origanum-vulgare/`
  -- verified 2026-09-04. Sibling-pathed to the admitted `ncsu_ext_lavandula_angustifolia` /
  `ncsu_ext_toolbox_*` keys, so a `ncsu_ext_toolbox_origanum_vulgare` key would be consistent.
  > "Root rot can occur in wet, poorly drained soils. Susceptible to fungal diseases, aphids, leaf
  > miners and spider mites."
- **RECOMMENDED ADDITION** `rhs` `https://www.rhs.org.uk/herbs/oregano/grow-your-own` -- verified
  2026-09-04. Anchors the **winter-wet** half of the record's causal claim, which nothing else does:
  > "It's important to protect oregano from waterlogging over winter, which will cause the roots to
  > rot."
  > "If you have heavy or damp soil, the roots are liable to rot"
  > "plant in a raised bed or a container, where drainage will be better"
- Supporting, same-key: `uc_ipm` oregano cultural tips
  (`https://ipm.ucanr.edu/home-and-landscape/oregano/cultural-tips/index.html`, verified 2026-09-04):
  > "Damp soil surfaces encourage snails, slugs, sowbugs, and root diseases; leaf spot diseases may
  > also increase."
  > "Grow in well drained soils"
  > "Also avoid areas that have had previous disease problems"
  > "Space plants at least 18 inches apart to accommodate their full size."

RECORD CLAIMS THAT HOLD:
- Root rot is the main way oregano is lost, driven by wet/poorly drained soil -- `uf_ifas` +
  `ncsu_ext` toolbox + `rhs`. (The *superlative* "main way" is unsourced; see below.)
- "brown or black decay at the base of the stems and roots" -- `ncsu_ext`: "Affected roots would
  appear brown to black or roots may be mostly decayed."
- "excess winter moisture rather than to cold" -- `rhs` verbatim above. Previously unanchored;
  **TRUE.**
- "no cure once the crown and roots are rotting; remove and discard affected plants" -- `uf_ifas`
  ("Remove affected plants promptly") + `ncsu_ext` ("Remove and destroy infected plants"; the pathogen
  "cannot be eradicated without extreme measures").
- "use a mound or raised bed" on clay -- `ncsu_ext` ("Improve drainage in areas where standing water
  occurs; use raised beds") + `rhs` ("plant in a raised bed or a container").
- "space plants for airflow" -- `uc_ipm` cultural tips (18 inches), `uf_ifas` ("Space your plants
  10-12 inches apart"). **Note the two admitted sources disagree on the number, 18 in. vs 10-12 in.**
  Not a defect in this record, which gives no number, but a reviewer should not invent one.
- "humid regions" as an aggravator -- `ncsu_ext`: *Phytophthora* "prefer warm, humid, and wet
  conditions."

RECORD CLAIMS WITH NO ANCHOR:
- "It is the main way oregano is lost" / "This is the main thing that kills oregano." A ranking claim.
  No source ranks oregano's causes of death. `uf_ifas` says the opposite in emphasis: "Oregano is
  generally resistant to diseases, but it can **occasionally** suffer from fungal infections like
  powdery mildew or root rot." I would keep the claim -- it matches every cultural instruction every
  source gives -- but it is an editorial judgment, not a sourced fact, and it should be recorded as
  such rather than left looking anchored.
- "Soilborne root and stem rots" (plural, unnamed). Now partially resolvable to *Phytophthora* via
  `ncsu_ext`; the **stem** half is still unnamed by any source.
- "full sun" as a rot measure.
- "lean" soil. `psu_ext` says "well-drained, average soil with a pH of 6.8"; `ncsu_ext` toolbox says
  "average soil including sandy loams, dry to medium moisture with good drainage". "Well-drained" is
  anchored; "lean" is not.

RECORD CLAIMS THAT ARE WRONG:
- **None factually, but `type: "fungal"` is now questionable.** The only pathogen genus any source
  names for oregano root rot is *Phytophthora*, an **oomycete**. `uf_ifas` calls it a "fungal
  infection", so the record is faithful to its own anchor; but if `ncsu_ext` is added the record will
  cite a document that treats it as *Phytophthora*. Flagging for a schema decision, not asserting the
  field is wrong.

LADDER-RELEVANT FACTS the record does not carry:
- **The pathogen persists in soil between seasons** -- `ncsu_ext`: "can survive in soil from season to
  season, so once the bed is infested the pathogen cannot be eradicated without extreme measures."
  That converts "remove the plant" into "**do not replant oregano in that spot**", which is a real,
  actionable, currently-missing rung. `uc_ipm` cultural tips independently gives the same rung:
  "Also avoid areas that have had previous disease problems."
- **No effective organic chemical rung exists.** `ncsu_ext`: "There is a lack of OMRI-approved
  products that effectively manage diseases caused by *Phytophthora* species." A PLA-8 ladder for
  this problem should terminate at cultural/physical and say so, rather than reaching for a soft
  chemical rung.
- **Sanitation of tools and containers**, and **inspecting nursery plants before buying** --
  `ncsu_ext` cultural list. Neither appears in the record.
- **Soil solarization** and **increasing organic matter** -- `ncsu_ext`. Both are plausible rungs.
- **Resistant/tolerant hosts** -- `ncsu_ext` recommends planting "*Phytophthora* resistant or tolerant
  hosts in affected areas". No oregano cultivar resistance is published anywhere I looked; this is a
  crop-rotation rung, not a variety rung. Do not let it become a `varieties[].resistance` claim.
- **Container growing as a control**, not just a convenience -- `rhs`.

---

## Rust [diseases] -- severity medium, type fungal
STATUS: **UNSOURCED-FOUND** (two catalog-admitted T1 anchors located; the binomial remains
JOURNAL-ONLY)
ORGANISM: ***Puccinia menthae***, per Koike et al. 1998, Plant Dis. 82(10):1172, read verbatim from
PubMed 30856788. Named as "mint rust" without a binomial by `psu_ext` and `rhs`. **The oregano
population is a host-specialized one that does not cross-infect *Mentha*** -- see §4f above.
ANCHORS:
- **`psu_ext`** `https://extension.psu.edu/herb-garden-plants-oregano` -- verified 2026-09-04
  (page last updated April 22, 2026). Already in oregano's vocabulary.
  > "Oregano can be susceptible to fungal diseases such as mint rust and root rot."
- **`rhs`** `https://www.rhs.org.uk/herbs/oregano/grow-your-own` -- verified 2026-09-04.
  > "The fungal disease mint rust can affect oregano"
- **`rhs`** `https://www.rhs.org.uk/disease/mint-rust` -- verified 2026-09-04. Organism, symptoms and
  the full control set:
  > causal organism: "*Puccinia menthae*"
  > hosts: "Garden mints, marjoram and savory"
  > "Dusty orange pustules on the stems and leaves. These may be followed by dusty yellow or black
  > pustules"
  > "Pale and distorted shoots in spring"
  > "Remove affected plants promptly before the black resting spores are formed"
  > "In the case of garden mint it is also necessary to remove infected rhizomes"
  > "Immerse in hot water at 44ºC (111ºF) (no higher) for 10 minutes, then cool in cold water and
  > plant"
  > "The RHS recommends that you don't use fungicides"
  > "No fungicides with activity against mint rust are available for use on mint or other herbs that
  > will be used for culinary purposes"
- Generic rust biology and management, **not oregano-scoped** -- `uconn_ext` (subdomain divergence
  noted above), Leanne Pundt, "Rust Diseases on Ornamental Crops", UConn Extension, 2013, latest
  revision July 2024, `https://ipm-cahnr.media.uconn.edu/wp-content/uploads/sites/3216/2024/07/rustornamentalplants.pdf`,
  verified 2026-09-04, text extracted locally with pypdf:
  > "Mild, moist conditions favor the development of rust diseases. Windblown spores from infected
  > plants to healthy plants spread rusts. Spores are also easily spread by splashing water. They need
  > wet leaf surfaces to germinate and cause infection."
  > "Reducing leaf wetness helps to reduce favorable conditions for rust development. Keep foliage dry
  > by proper watering practices... Space plants properly to provide for good air circulation between
  > plants."
  > "Once detected, remove all rust-infected leaves and heavily infected plants by carefully placing
  > them in a plastic bag before removing them from the greenhouse. Rust spores are easily spread in
  > air currents! Destroy infected plant material by burning, rapid-composting, or burying."
  > "At the end of the growing season, carefully clean up and destroy all infected crop debris."
  > "Select less susceptible cultivars, if available."

  **This document contains zero occurrences of oregano, Origanum, marjoram, mint, Mentha or menthae
  (verified by regex over the extracted text).** It is a greenhouse/nursery ornamentals fact sheet.
  Use it for rust *biology*, never as evidence about oregano.
- ***P. menthae*-specific biology, scoped to *Mentha*** -- Washington State University, Dennis A.
  Johnson, "Management of Rust on Mint",
  `https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/MintrustA.doc`, verified 2026-09-04, full text
  extracted locally. Host is `s3.wp.wsu.edu`, the same host as the admitted `wsu_em051e` and
  `wsu_em057e`, so a `wsu_mint_rust` key would sit on already-admitted infrastructure.
  > "Mint rust, caused by the fungus Puccinia menthae, infects Scotch spearmint and Native spearmint
  > in central Washington."
  > "Two principal types of races of P. menthae have been recognized. One type infects Native spearmint
  > but not peppermint and is called native spearmint rust; the other, peppermint rust, infects
  > peppermint but not Native spearmint."
  > "Wet, cloudy weather and prolong leaf wetness from irrigation, dew, and rainfall favor rust
  > development."
  > "Early spring infections are systemic in spearmint and infected plants are twisted and distorted,
  > and stems easily break."
  > "the disease is recycled every 8 to 10 days when favored by moisture on foliage from rain, dew or
  > sprinkler irrigation."
  > "In late summer and fall, pustules on mint stubble and foliage become dark chocolate brown. This is
  > the overwintering stage (telia) of the rust fungus and is the source of new infections the
  > following spring."
  > "Fields should be monitored regularly for rust through out the season. Infections in late fall will
  > indicate potential infections in the spring."
  > "Such rust outbreaks are usually initiated from systemic infections and pustules on rhizomes and
  > stem cuttings used in propagation."
  > "Rust on rhizomes can be eliminated by immersing rhizomes in water at 113 F (34 C) for 10 minutes
  > before planting."

  **Defect in the source, quoted as-is:** "113 F (34 C)" is internally inconsistent -- 113 °F is 45 °C,
  not 34 °C. RHS independently gives 44 °C (111 °F) "no higher"; the UK HDC guide gives 43 °C. If any
  hot-water figure is ever authored into this dataset, take the °F/°C pair from RHS, not WSU.

RECORD CLAIMS THAT HOLD:
- Rust occurs on oregano -- `psu_ext`, `rhs`. **Previously unanchored; TRUE.**
- "Small circular spots and orange or brown powdery pustules on the leaves and stems" -- Koike 1998
  (circular brown necrotic spots, cinnamon brown pustules); `rhs` mint rust (dusty orange pustules on
  stems and leaves).
- "a rust fungus favored by damp... conditions" and "when the foliage stays wet" -- `uconn_ext` (rusts
  generally, need wet leaf surfaces) + WSU (*P. menthae* specifically, prolonged leaf wetness).
- "crowded, poorly ventilated conditions" -- `uconn_ext` ("Space plants properly to provide for good
  air circulation between plants"), rusts generally.
- "overhead watering" / "water at the base rather than overhead" -- `uconn_ext` ("spread by splashing
  water", "Keep foliage dry by proper watering practices"), WSU ("sprinkler irrigation").
- "remove plant debris" -- `uconn_ext` ("carefully clean up and destroy all infected crop debris").
- "Severely infected plants are best removed to protect the rest" -- `uconn_ext` ("remove all
  rust-infected leaves and heavily infected plants") + `rhs` ("Remove affected plants promptly").
- "can spread through a planting if left unchecked" -- WSU ("recycled every 8 to 10 days"), `uconn_ext`
  ("Rust spores are easily spread in air currents!").

RECORD CLAIMS WITH NO ANCHOR:
- **"Caught early, pruning off affected parts can save the plant."** Verbatim from the record, in both
  registers ("if you catch it early, cutting off the affected parts can save the plant"). No source I
  read says this, and the control literature points the other way. See "WRONG", below.
- "site in full sun" as a rust measure. Universally good oregano advice; not a sourced rust control.
- "Prune out and destroy affected growth **promptly**" -- the "destroy" half is anchored
  (`uconn_ext`: burning, rapid-composting or burying), the "prune out" framing is not.

RECORD CLAIMS THAT ARE WRONG:
- **"Caught early, pruning off affected parts can save the plant" is not supportable and is arguably
  harmful advice.** The refuting sentences:
  - `rhs`: "Remove affected plants promptly before the black resting spores are formed." (Remove the
    *plant*, not the affected parts.)
  - `rhs`: "In the case of garden mint it is also necessary to remove infected rhizomes."
  - `uconn_ext`: "Once detected, remove all rust-infected leaves **and heavily infected plants**..."
  - WSU: outbreaks "are usually initiated from **systemic** infections and pustules on rhizomes and
    stem cuttings" -- i.e. the fungus is inside the plant, not only on the leaves it visibly marks.
  - The sibling record for mint in this same batch already states: "There is no reliable home cure
    once it is established."

  I am not claiming spot-pruning is useless; I am reporting that **no document supports "can save the
  plant"**, four documents recommend removing plants, and the record's own sibling contradicts it.
  This is the defect to fix.
- **Bare display name "Rust".** Every source that names this disease on oregano calls it "mint rust".
  See the §4f ruling: rename to "Mint rust", mint a host-scoped id.

LADDER-RELEVANT FACTS the record does not carry:
- **It carries over year to year.** WSU: overwintering telia on stubble "is the source of new
  infections the following spring"; systemic infection of rhizomes/propagation material. RHS: remove
  infected rhizomes. **Honest caveat that must be preserved:** Koike found "Teliospores were not
  detected on either host" on oregano/marjoram in California, so the *documented* overwintering route
  is for *Mentha*, not *Origanum*. The ladder should say clean-up-and-do-not-propagate-from-it
  without asserting the oregano rhizome mechanism as fact.
- **Start from clean stock.** WSU: "Source materials should be inspected and be rust-free before
  propagating stem cuttings. Monitor stem cuttings closely for rust and discard infected plants
  promptly." Oregano is routinely propagated by division and cuttings, so this is a live rung and the
  record has nothing like it.
- **The hot-water rung exists and is anchored at an admitted T1.** RHS: "Immerse in hot water at 44ºC
  (111ºF) (no higher) for 10 minutes, then cool in cold water and plant." That is a *physical* rung,
  exactly the tier PLA-8 wants between cultural and chemical, and it is currently absent. Consumer
  copy would need `°F` rendering and the "no higher" qualifier kept.
- **The ladder should terminate before conventional chemistry, and there is a T1 sentence saying so.**
  RHS: "No fungicides with activity against mint rust are available for use on mint or other herbs
  that will be used for culinary purposes" and "The RHS recommends that you don't use fungicides."
  (WSU lists Rally 40W, Headline and Amistar -- **commercial mint only, with 7-30 day preharvest
  intervals. Do not let those reach a home-garden culinary-herb ladder.**)
- **Monitoring signal, published:** late-fall infections predict spring infections (WSU). An
  end-of-season scouting rung.
- **Nearby wild/escaped host plants are an inoculum source** -- WSU: "Rust from escaped mint and
  non-cultivated mint can also be a source of rust infection in the spring." Scoped to *Mentha*;
  given host specialization, the oregano analogue would be other *Origanum*, not mint. Worth stating
  carefully or not at all.
- **Severity note:** Koike: "Rust significantly reduced the quality and yield of both crops." The
  record's `severity: "medium"` is the floor of that.
- **Rusty leaves are not good to eat** -- mint's sibling record says this; oregano's does not, and for
  a culinary herb that is the consumer-facing consequence that actually matters.

---

## Botrytis and humid-weather foliar disease [diseases] -- severity low, type fungal
STATUS: **SPLIT VERDICT.** Powdery mildew: **UNSOURCED-FOUND**. Botrytis on oregano:
**UNSOURCED-NOT-FOUND**. The entry as named is **WRONG in the name**: it leads with the one organism
no source attaches to this crop.
ORGANISM: "umbrella -- multiple organisms" is the record's intent, and that intent is legitimate. But
of the two named members, only **powdery mildew** is attested on oregano (unnamed to genus by the
source; the Lamiaceae powdery mildew is the *Golovinomyces biocellatus* complex, which I could confirm
only on other Lamiaceae hosts and in non-US reports, so **do not encode a binomial**). **Botrytis
(*Botrytis cinerea*) is attested on herbs as a class but by no document on oregano.**
ANCHORS:
- **RECOMMENDED** `uf_ifas` `https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/`
  -- verified 2026-09-04 (fetched twice). This is the *only* source I found that names a
  humid-weather foliar disease on oregano, and it is the record's own existing key on disease #1:
  > "Oregano is generally resistant to diseases, but it can occasionally suffer from fungal infections
  > like powdery mildew or root rot."
  > "Powdery mildew appears as a white, powdery coating on oregano leaves, affecting plant health and
  > appearance."
  > "To prevent powdery mildew, provide good air circulation around plants and avoid overhead
  > watering."
  > "Apply fungicidal sprays containing sulfur or copper if necessary, following label instructions."
  > "Space your plants 10-12 inches apart, this will help with air circulation and prevent extra
  > humidity"
  > "Our high temperatures and humidity can be challenging"

  **Confirmed by regex-style term check on a second fetch: the words "rust", "Botrytis", "gray mold",
  "airflow" and "winter" do not appear on this page.**
- Botrytis biology, **herbs as a class, not oregano** -- UMass Extension Greenhouse Crops and
  Floriculture (Robert L. Wick, rev. Angela Madeiras), "Botrytis Blight of Greenhouse Crops",
  `https://www.umass.edu/agriculture-food-environment/greenhouse-floriculture/fact-sheets/botrytis-blight-of-greenhouse-crops`,
  verified 2026-09-04. Host is `ag.umass.edu`/`umass.edu`, sibling to the admitted `umass_ext`
  (`https://ag.umass.edu/vegetable`) -- a path divergence, flagged not assumed.
  > "A wide variety of plants including ornamentals, vegetables, and herbs are susceptible."
  > "Germination of spores and infection of the host is dependent on a film of moisture for 8 to 12
  > hours, relative humidity 85% or greater, and temperatures 55 - 75°F."
  > "Space plants properly to allow for good air circulation"
  > "Control weeds and remove plant debris between crop cycles and during production"
  > "Avoid overfertilization, which leads to overproduction of succulent tissues"
  > "Manage insect pests, which may carry spores between plants and cause injuries"

  **"herbs" is the closest this document gets to oregano. It never names oregano or *Origanum*.**

RECORD CLAIMS THAT HOLD:
- "a powdery-white coating on the foliage" / "a powdery white film on the leaves" -- `uf_ifas`
  verbatim ("a white, powdery coating on oregano leaves").
- "powdery mildew... favored by humidity, crowding, and poor air movement" -- `uf_ifas` (prevention is
  air circulation; spacing "prevent[s] extra humidity").
- "Oregano is fairly disease-resistant, so these are mainly a humid-climate and overcrowding issue" --
  `uf_ifas`: "Oregano is generally resistant to diseases, but it can occasionally suffer from fungal
  infections like powdery mildew or root rot." Plus the Florida framing "Our high temperatures and
  humidity can be challenging". **Previously unanchored; TRUE.**
- "open up airflow, and water at the base rather than overhead" -- `uf_ifas` verbatim ("provide good
  air circulation around plants and avoid overhead watering").
- "Space plants for air circulation" -- `uf_ifas` ("Space your plants 10-12 inches apart, this will
  help with air circulation").
- "A minor issue next to root and stem rot" -- consistent with `uf_ifas` ("occasionally"), and with
  root rot being the one disease every source repeats.
- Botrytis is favored by humidity, crowding and poor air movement, **as a general fact about the
  pathogen** -- UMass.

RECORD CLAIMS WITH NO ANCHOR:
- **"Botrytis" and "Grayish moldy patches" and "gray mold", on oregano.** No document I read attaches
  Botrytis to *Origanum*. UMass gets to "herbs"; that is a class, not this crop.
- "spotting" as a distinct symptom. Unattributed to any named pathogen. `uc_ipm`'s cultural tips do
  say "leaf spot diseases may also increase" under damp conditions, which is the nearest thing, but it
  is a soil-moisture remark on a cultural page, not a disease record.
- "favor upright culinary types over dense low ones where humidity is high" / "In humid areas, more
  open upright plants handle it better than dense low mats." **This is a varietal/morphological
  recommendation and I could find nothing supporting it anywhere.** It is the kind of claim the
  "fill-the-shape" failure mode produces: the field wanted a prevention sentence and the plant's growth
  habit supplied a plausible one. If it stays, it needs a document naming oregano types by habit and
  linking habit to disease. If it goes into a variety pass it becomes a `varieties[]` claim, which
  raises the stakes.
- "A hard harvest or shear clears and renews the canopy."
- "site in full sun."

RECORD CLAIMS THAT ARE WRONG:
- **The display name is wrong for the evidence.** "Botrytis and humid-weather foliar disease" makes
  Botrytis the headline organism, and Botrytis is the member of the umbrella that **no source attaches
  to this crop**, while powdery mildew -- which the record's own `uf_ifas` key names on oregano twice
  -- is buried in the prose. If PLA-448 §4f is about display names asserting more than the record can
  carry, this name is a second instance of the same defect class on the same crop, and it is worse
  than "Rust": "Rust" under-specifies a real organism, whereas this name over-specifies an organism
  that is not attested here. **Recommend renaming to lead with powdery mildew** (e.g. "Powdery mildew
  and humid-weather foliar disease"), keeping the umbrella, and demoting Botrytis inside the prose to
  what it actually is -- a general herb/greenhouse risk in still, humid air -- or dropping it.
- Nothing else in the entry is contradicted by a document.

LADDER-RELEVANT FACTS the record does not carry:
- **A published, quantitative infection window** (Botrytis, from UMass): "a film of moisture for 8 to
  12 hours, relative humidity 85% or greater, and temperatures 55 - 75°F." That is the kind of fact a
  weather-trigger rung is built from. Note the source renders it `55 - 75°F`, already conformant.
- **A soft-chemical rung exists and is anchored on this crop:** `uf_ifas`, "Apply fungicidal sprays
  containing sulfur or copper if necessary, following label instructions." That is a real
  soft-chemical rung for powdery mildew on oregano at a T1 the record already cites, and the record
  currently recommends no product at all for this problem.
- **A published spacing number on this crop:** 10-12 inches (`uf_ifas`) -- which conflicts with
  `uc_ipm`'s "at least 18 inches". A ladder rung that says "space plants" should not silently pick one.
- **Overfertilization is a lever** (UMass: "Avoid overfertilization, which leads to overproduction of
  succulent tissues") and **insects spread spores and create entry wounds** (UMass: "Manage insect
  pests, which may carry spores between plants and cause injuries") -- the latter links this disease to
  the aphid/mite entries, which no rung currently does.
- **Debris and weed removal between cycles** (UMass). The record says "remove plant debris" only under
  Rust, not here.

---

# SUMMARY

## Counts by STATUS

| STATUS | count | entries |
|---|---|---|
| SOURCED-OK | 3 | Aphids, Spider mites, Root and stem rot |
| SOURCED-WEAK | 0 | -- |
| UNSOURCED-FOUND | 1 | **Rust** (two catalog-admitted T1 anchors located) |
| UNSOURCED-NOT-FOUND | 0 as a whole entry | -- |
| JOURNAL-ONLY | 0 as a whole entry | (the *binomial* for Rust is journal-only; see below) |
| WRONG | 1 | **Botrytis and humid-weather foliar disease** -- wrong in the display name, split verdict on contents |

Both of the crop's "no sources, no anchoring_urls" entries came back with real support. Neither was
unsourceable. Consistent with the hunt-before-downgrading rule: **2 of 2 flagged-unsupported entries
found support on a real hunt**, and in both cases at a source already inside oregano's own vocabulary
(`psu_ext` for rust, `uf_ifas` for powdery mildew).

## The single most important finding

**Oregano's "Rust" is not an umbrella. It is one organism -- *Puccinia menthae* -- that nobody pinned,
it is called "mint rust" by every source that names it, and the population on oregano does not
cross-infect mint. So `mint-rust` and `oregano-rust` are correctly TWO ids, and the reason is
epidemiological, not cosmetic: a shared id would license the advice "your rusty mint is infecting your
oregano", which the cross-inoculation evidence refutes.**

The evidence chain: `psu_ext` and `rhs` (both admitted T1, `psu_ext` already in the crop's vocabulary)
name mint rust on oregano; Koike et al. 1998 identifies the organism as *P. menthae* on *Origanum
vulgare* and states verbatim that "Neither the oregano nor the sweet marjoram isolates infected
spearmint (*Mentha spicata*), which is consistent with previous studies"; and WSU -- a T1 extension
source -- independently documents host-specialized races inside *P. menthae* that are named for the
host they infect. The binomial itself remains **JOURNAL-ONLY** for oregano and cannot be written into
the record under the current catalog.

## Decisions this pass hands to the authoring pass

1. **Rename "Rust" to "Mint rust"; mint the id host-scoped (`oregano-rust`).** Pin it now and never
   re-derive it. Mint's record is unpinned too and is in this same batch -- pin both in the same pass,
   from the same decision, so the pair is deliberate rather than emergent.
2. **Delete or rewrite "Caught early, pruning off affected parts can save the plant."** No source
   supports it; four documents and the sibling mint record point the other way.
3. **Rename "Botrytis and humid-weather foliar disease" to lead with powdery mildew.** Botrytis on
   oregano is attested by nobody; powdery mildew is attested twice by the record's own `uf_ifas` key.
4. **Add `psu_ext` to Aphids and Spider mites.** One PSU sentence anchors the aroma-repellence and
   seedling-stage claims that both entries make and neither currently supports.
5. **Add `ncsu_ext` to Root and stem rot.** It names oregano as a *Phytophthora* host, supplies the
   soil-persistence fact (do not replant in that spot) and states there is no effective OMRI-approved
   product -- which tells the ladder where to stop.
6. **Catalog decisions raised, none taken:** `pubmed` (would unblock the *P. menthae* binomial and
   this whole class of gap), `wsu_mint_rust` on the already-admitted `s3.wp.wsu.edu` host,
   `ncsu_ext_toolbox_origanum_vulgare` (sibling of existing toolbox keys), `ucanr_ext_aphids` (sibling
   of the existing `ucanr_ext_spider_mites` / `ucanr_ext_thrips` Pest Note keys). Recommended
   **against**: `plantvillage`.
7. **Record gap reported, not acted on:** UC IPM lists Leafhoppers, Spittlebugs and Thrips on oregano;
   `psu_ext` adds leaf miners and cutworms; `ncsu_ext` toolbox adds leaf miners. Thrips is named by
   three sources and has an admitted pathed anchor already sitting in the catalog
   (`ucanr_ext_thrips`).

## Consumer-copy constraint check on the existing record prose

Programmatic sweep of all 5 entries, every string field: **0 em dashes or en dashes, 0 British
spellings, 0 Celsius-only temperatures, 0 mid-sentence capitalized "Plant".** No violations to report.
The record's prose is style-clean; its problems are sourcing and substance, not house style.

Note for whoever authors the new rungs: RHS renders its hot-water figure as "44ºC (111ºF)" with a
masculine-ordinal character, and it leads with Celsius. Consumer copy must render `111°F` with a
proper degree sign, American-English, and keep RHS's "no higher" qualifier.
