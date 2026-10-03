# Roster gap review 2 -- what neither list carries (PLA-635 follow-on)

**Status:** RULED 2026-10-02 (Trevor): the buckets were taken as proposed, with the additions
recorded in §6. Nothing here authorizes authoring a crop, and nothing here re-rules the 2026-09-30
rulings (`docs/roster-gap-review.md` §0a). Read-only on the canonical and every other file.
Measured 2026-10-02 on branch `main`, HEAD == origin/main == `e00f001`, canonical `cf1d480d`
(== LATEST.txt). Committed on `23f3da9` (canonical `31b766e8`, after PLA-10 promote 2). Promote 2
left the roster's slug set unchanged (128 == 128), so the diff holds on the new base. Fetch log:
`docs/roster-gap-review-2/evidence.tsv`.

**The question:** which common or slightly uncommon backyard food crop (USDA zones 3-11,
beginner-first) is on NEITHER the 128-crop roster NOR master list v2
(`~/Documents/plant-project/08-reference/master_crop_list_v2_2026-09-30.pdf`: 231 planned parents,
40 no-source-path, 10 to-assign rows)?

**Verdict (one line):** For the temperate, beginner-first core, neither the April list nor the
September review missed anything material. Every NGA top-25 crop is on the roster, and the only
names that two or more T1 indexes carry and both lists lack are five warm-climate specialties
(chayote, luffa, ginger, jicama, leaf amaranth), every one of them from the Gulf South / Florida
publishers. There are two documentary slips worth fixing (§4).

## 0. Method

- **Known set.** The roster was computed from `crops_data_final.json` (128 slugs + names). Master v2
  was parsed from the PDF text (pypdf), and the per-bucket counts reproduce the PDF's own table
  exactly: 128 in dataset / 7 first batch / 2 ruled split / 41 later / 13 wanted / 40 April / 40
  no source path / 10 to assign. A name counts as "on a list" if it is a roster crop, any v2 row
  (any bucket, including no-source-path), or a variety v2 already lists under a parent.
- **Normalization.** Plurals, "beans - bush" / "squash, summer" inversions, slash pairs split,
  and a hand alias table (cowpea = southern pea, pak choy = bok choy, Chinese okra = luffa,
  Chinese spinach = leaf amaranth, sand pear = Asian pear, monarda = bee balm, ...). Every
  leftover NEITHER was read by hand. Group headings ("cole crops", "tree fruits", "minor fruits")
  are dropped.
- **Counting.** "On >= 2 indexes" counts **institutions**, not pages. UF/IFAS VH021 and UF
  Gardening Solutions are one publisher; Cornell's two indexes are one.
- **Evidence.** Every index was fetched from raw bytes under two user agents (the PLA-532
  convention, via a scratch wrapper over `tools/staging/pla10_promote1/fetch_evidence.py`; Safari
  headers for Clemson's Cloudflare rule). Index pages only, never crop pages. The fetch log is
  `docs/roster-gap-review-2/evidence.tsv`: 152 rows (90 fetched with HTTP 200, 62 failed), each
  with its sha256, bytes, fetch date, status codes, user-agent result, URL, final URL and content
  type. Every hash in the appendix resolves to a row there. The raw bytes themselves were not
  committed. **A name on an index is not support** (`right-document-wrong-claim`). It only shows the
  publisher has a page. "T1 availability" below means "an index links a dedicated page". No page
  was read.
- **Columns** are review 1's five: parent or variety / why a gap / T1 availability / rough cost
  (review 1 §0 tiers S/M/L, estimates) / zone and audience fit (orientation only, unsourced).

### What was covered, and what was not

| publisher | indexes fetched | names | coverage note |
|---|---|---|---|
| Cornell | vegetables A-Z (homegardening/scene0391), food-garden fruit chapters | 61 + 10 | complete |
| UMN | Gardening in Minnesota hub (vegetables A-Z, fruit), herbs | 45 + 11 + 6 | complete; the herbs page names 9 more herbs with no guide link (not counted) |
| Clemson HGIC | vegetables (8 pp), tree fruits (3 pp), small fruits (2 pp), nuts | 41 + 12 + 5 + 1 | complete; HGIC has **no herbs category** (all 404) |
| OSU (Oregon State) | gardening vegetables / berries-fruit, publications filter | 7 + 3 | **INCOMPLETE**: HTTP 429 under both UAs for ~20 min (6 retries). Missing: vegetable list p1, fruit p1-3, the article/collection filters ("Grow your own" series). Ohio State's Ohioline HYG index was fetched as well (10 + 12) |
| WSU | pubs.extension.wsu.edu gardening category (4 pp) + "home garden series" search (9 pp) | 8 + 7 | complete; archived Home Garden Series sheets recorded separately |
| UC ANR | UC IPM home-garden vegetables/melons/herbs and fruit/nuts/berries/grapes | 32 + 18 | **Partial by host**: UC Home Orchard, VRIC and ucanr.edu/sites all 403 under every UA (as recorded in `clemson-cloudflare-needs-accept-encoding`) |
| UF/IFAS | VH021 planting table; Gardening Solutions edibles (vegetables, fruits, herbs) | 40 + 79 + 34 + 20 | complete |
| TAMU | Easy Gardening series, vegetable guides + specialty, fruit & nut | 31 + 73 + 32 | complete; citrus subindex 301 not followed (its crops are linked from /fruit-nut/) |

**Coverage bias, stated plainly:** the North and Mountain West are thin (OSU incomplete, WSU's
home-garden list is short), while the Gulf South is thick (TAMU and UF are the two largest indexes).
**Northern indexes, for a re-run:** OSU is PARTIAL (429); UC ANR's Home Orchard and VRIC returned 403
(UC IPM only); WSU, UMN and Cornell were crawled in full; **UVM was not crawled at all**. A re-run
should finish OSU (throttle hard: it began returning 429 after a handful of requests, and retries
180 s apart did not clear it) and add UVM, plus a Mountain West publisher (USU or
CSU).
That is why every >= 2 hit comes from TAMU + UF. A northern cool-season crop on only Cornell's or
UMN's list would show up as a single-index row (§2), not a >= 2 row.

## 1. T1 names on >= 2 indexes, on NEITHER list

| candidate | P/V | why a gap | T1 availability | cost | zone and audience fit | proposed bucket |
|---|---|---|---|---|---|---|
| **chayote** (*Sechium edule*) | P | TAMU + UF. **Review 1's G-13 row credited it to the April list in error** (the April PDF does not contain the word), so v2 never got a row. **v2 gets a new row** (§4). | INDEXED: TAMU vegetable guides, UF Gardening Solutions vegetables (dedicated pages linked; not read) | M (perennial vine cucurbit; fruits on short days in fall; the trellis question is shared with the grape pilot) | Gulf Coast / FL / CA south, z8-11; a classic Southern backyard vine | **LATER** (ruled 2026-10-02), after the grape vine pilot |
| **luffa** (*Luffa* spp.; "Chinese okra") | P | TAMU (as Chinese okra) + UF; GrowVeg. **Same G-13 error as chayote; v2 gets a new row** (§4). | INDEXED: TAMU guides, UF GS vegetables | S-M (`warm_season_fruiting` cucurbit; one crop with two harvests, young fruit to eat or mature fruit for sponge; rule 7's use-pattern clause needs a call at authoring) | long hot season, z7-11; a popular kids' and novelty crop | **LATER** (ruled 2026-10-02) |
| **ginger** (*Zingiber officinale*) | P | TAMU (two indexes) + UF (vegetables and herbs); Territorial | INDEXED: TAMU Easy Gardening sheet, UF GS | M (rhizome; container anywhere, in-ground z8b-11; shares the herbaceous-tropical shape pineapple pilots) | a supermarket-rhizome pot project in any zone, like pineapple | **WANTED LANE (tropical)** (ruled 2026-10-02), after the pineapple pilot; turmeric (UF + Johnny's) rides with it |
| **jicama** (*Pachyrhizus erosus*) | P | TAMU + UF | INDEXED: TAMU guides, UF GS | M (short-day tuberous legume vine; **seeds, pods and foliage are toxic**, so `critical_warnings` is load-bearing) | needs a long frost-free season; weak outside z9-11 / South Texas | **LATER (low)** (ruled 2026-10-02); the toxicity is carried into authoring as a `critical_warnings` requirement |
| **leaf amaranth** ("vegetable amaranth", "Chinese spinach", callaloo) | P, or a member of the v2 `amaranth` row | Cornell + TAMU (as Chinese spinach and amaranth) + UF (amaranth under *vegetables*). v2's `amaranth` row is a **pseudo-grain** (LATER, NCSU organic guide). The indexes carry the **leaf** crop. | INDEXED: Cornell A-Z, TAMU guides, UF GS | S (`warm_season_fruiting`-style heat-loving green) | heat-tolerant summer green, z3-11 as an annual; fills the summer gap when spinach bolts | **LATER, attached to the v2 `amaranth` row as an open question**: under rule 7 (a use pattern that changes harvest), grain vs leaf is one crop or two. **Trevor's lean (2026-10-02, not a ruling): one crop, with the leaf use as the harvest shape.** That is a rule-7 call for the archetype session |

## 2. Single-index T1 names on neither list (ranked below §1)

Each has exactly one T1 index entry. Ordered by beginner fit, then by commercial corroboration.

| candidate | P/V | why a gap | T1 availability | cost | zone and audience fit | proposed bucket |
|---|---|---|---|---|---|---|
| **garden cress** (*Lepidium sativum*) | P | Cornell A-Z; **all three commercial lists** carry it | INDEXED: Cornell | S (`cool_season_annual`, very fast; also a natural microgreen) | z3-11, cool season; a kids' windowsill classic | **LATER (low)** (ruled 2026-10-02): one T1 index plus all three commercial lists is enough to list it. **It may fold into the microgreens family** rather than stand as its own garden parent |
| **cardoon** (*Cynara cardunculus*) | P (artichoke's species; grown for blanched stalks, so rule 7's use pattern) | UF GS; Territorial and Johnny's | INDEXED: UF GS | S-M (artichoke sibling) | z7-10 perennial, annual elsewhere; niche | **LATER** (rides with artichoke) |
| **claytonia** / miner's lettuce | P | Cornell; Territorial | INDEXED: Cornell | S (`cool_season_annual`) | winter salad green, z3-9 | LATER (low) |
| **wasabi** | P | WSU (gardening category); Territorial | INDEXED: WSU | M (shade, cool water; container) | PNW-only in practice | NO SOURCE PATH-adjacent: LATER (low), not proposed |
| **orach** (*Atriplex hortensis*) | P | Cornell | INDEXED: Cornell | S | z3-10 spinach substitute | LATER (low) |
| **pineapple guava / feijoa** | P | UF GS | INDEXED: UF GS | M (`evergreen_fruit_tree`) | z8-11; a common hedge-fruit shrub in CA and the Gulf | LATER (with the evergreen-tree members after avocado) |
| **roselle** (*Hibiscus sabdariffa*) | P | UF GS | INDEXED | S-M | z8-11, short-day; a tea/calyx crop | LATER (low) |
| **pigeon pea**, **winged bean** | P each | TAMU / UF GS | INDEXED | S-M | tropical legumes, z9-11 | not proposed |
| **taro**, **cassava**, **sugarcane**, **vanilla** | P each | TAMU / UF GS | INDEXED | -- | already named in review 1 §4.9 T8 ("LATER; not proposed") and not carried in v2. No change | as review 1 |
| **atemoya, sweetsop, soursop, mamey sapote, tamarind** | P each | UF GS fruits | INDEXED | M each | z10-11, South Florida | **WANTED LANE (tropical), later members**; same class as review 1 T5 |
| **mayhaw** (*Crataegus*) | P | TAMU fruit & nut | INDEXED | M | Gulf South native; jelly fruit | not proposed |
| **sesame**, **culantro**, **Cuban oregano**, **Mexican tarragon** | P each | UF GS (herbs / vegetables) | INDEXED | S | warm-climate herbs and seed crop | LATER (low); Mexican tarragon (*Tagetes lucida*) is the Gulf's tarragon substitute and pairs with the tarragon row |
| **stinging nettle** | P | OSU ("Wild Edibles") | INDEXED | -- | foraged, not a garden crop | not proposed |
| **datil pepper**, **boniato**, **Seminole pumpkin** | **VARIETY NOT PARENT** | UF GS | INDEXED | -- | -- | datil -> a hot-pepper variety (`habanero` family, *C. chinense*); boniato -> `sweet-potato`; Seminole pumpkin is already a v2 winter-squash variety to assign |
| ornamental peppers, ornamental gourds, sprouts | -- | UF GS | -- | -- | not food crops / a technique | out of scope (sprouts is a product question beside the microgreens) |

## 3. Commercial only (on zero T1 indexes; rank below §1-§2)

GrowVeg, Johnny's and Territorial are commercial, **not sources**. Rows with >= 2 commercial lists:

| candidate | P/V | lists | T1 availability | cost | zone and audience fit | proposed bucket |
|---|---|---|---|---|---|---|
| **goji berry** | P | GrowVeg, Territorial | NONE on any index; hunt owed | M (`berries_woody`) | z5-9 shrub | NO SOURCE PATH, commercial only |
| **lemon verbena** | P | GrowVeg, Territorial | NONE | S (`culinary_herb`, tender) | z8-11; a pot herb elsewhere | NO SOURCE PATH, commercial only |
| **bay laurel** | P | GrowVeg, Territorial | NONE | M (evergreen herb tree; container) | z8-10; container everywhere | NO SOURCE PATH, commercial only |
| **prickly pear** | P | GrowVeg, Territorial | NONE | M | Southwest | NO SOURCE PATH, commercial only |
| **kalettes** (kale x Brussels sprouts) | **VARIETY NOT PARENT** (proposed) | Johnny's, Territorial | -- | -- | -- | a `brussels-sprouts` variety: harvested as sprouts up the stalk. Contrast broccolini, where the harvest instruction changes |
| **loganberry** (+ tayberry, olallieberry, 1 list each) | **VARIETY NOT PARENT** | GrowVeg, Territorial | -- | -- | -- | `blackberry` varieties (boysenberry and Marionberry are already there) |
| **Italian dandelion** (a chicory) | VARIETY NOT PARENT | Johnny's, Territorial | -- | -- | -- | *Cichorium intybus*, so it belongs with the `radicchio` row |
| fenugreek, cumin, angelica | P each | 2 each | NONE | S | herbs/spices; weak beginner fit | commercial only, not proposed |
| catnip, feverfew, valerian, ginseng, nettle, hard-shell gourds | -- | 2-3 each | -- | -- | not backyard *food* crops (pet, medicinal or craft); medicinal framing would need T1 health sourcing | out of scope |

Single-list commercial names (purslane, burdock, yacon, huckleberry, saffron crocus, cranberry,
groundnut, camas, comfrey, coconut and others) are recorded in the scratchpad lists and are not
proposed.

## 3a. Grains (added at commit, Trevor 2026-10-02)

| candidate | P/V | why a gap | T1 availability | cost | zone and audience fit | proposed bucket |
|---|---|---|---|---|---|---|
| **rice** (*Oryza sativa*) | P | on neither list; joins v2's grains lane | NONE for the home garden: extension rice coverage is commercial production (UC Rice, Arkansas, Louisiana). **Lead:** Cornell's small-scale Northeast rice work (SRI) | L (rides with the cool-season-grass / grains archetype question) | small-plot or container paddy; niche | **NO SOURCE PATH**; the grains archetype session hunts it with buckwheat, quinoa and rye |

## 4. Things the diff found that are not new crops

1. **Review 1's G-13 row credited chayote and luffa to the April list in error.** Review 1 §4.8
   G-13 lists both among "the master list's remaining ~30 hot family proposals", but the April PDF
   contains neither word (pypdf over 79,575 characters; positive control: "Malabar" found 5x).
   v2's 40 April-proposal rows came from the April list, so neither got a row. **Ruled 2026-10-02:
   v2 gets two new rows, both LATER** (§1). Review 1 itself is left as written; this entry is the
   correction of record.
2. **Four no-source-path rows have a T1 index entry. Ruled 2026-10-02: these move from NO SOURCE
   PATH to "RE-MEASURE: T1 index page found".** They are not re-ruled into a candidate bucket. The
   NSP bucket was a cache measurement (review 1 §0), not a ruling, and a re-measure reads the
   linked page before anything moves further.

   | v2 NSP row | index that links a page |
   |---|---|
   | starfruit (carambola) | UF Gardening Solutions fruits |
   | miracle fruit | UF Gardening Solutions fruits |
   | lingonberry | WSU gardening category (commercial-leaning title) |
   | walking / Egyptian onion | Cornell vegetables A-Z |

   Also, **hops** (WANTED LANE, "T1 hunt owed") is on UF Gardening Solutions' herbs and vegetables
   indexes. **Recorded as a lead for the owed hunt**, not as a source path: a Florida page is a weak
   anchor for a z4-8 crop.
3. **NGA and USDA top crops: all in the roster.** NGA 2009 (Harris Interactive for NGA, Jan 2009,
   2,559 households; the 2014 "Garden to Table" top 10 repeats these figures): all 25 of the top 25
   map to roster crops. "Salad greens" (#14) maps to `lettuce-leaf`/`arugula`, and the mix itself is
   v2's `mesclun` (April list leaned no). Ranks 31-32 are napa cabbage and rutabaga, both FIRST
   BATCH. USDA's only crop-level survey is from **1975** (Kaitz & Davis, ERS/ARS, ~1,400 households):
   all 19 crops are in the roster. No current USDA/NASS home-garden crop survey exists. NASS covers
   commercial growers only.
4. **Recommendation from the survey (ruled 2026-10-02): rule the English-pea row (W5) first among
   the April proposals.** "Peas" is NGA #10 at 24% of food-gardening households, and the roster
   carries only snap and snow peas. The shelling/English pea is v2's April-proposal
   `shelling-pea-english-pea`, the one top-ten survey crop whose most common form has no roster
   crop.

## 5. Search demand: not measured here

What it would need: **Google Search Console on plant.lifestyle** (Performance > Queries over 3-12
months), filtered to queries that name a crop with no guide page. The useful cuts are "how to grow
X" / "X zone N" queries with impressions but no ranking URL, and queries landing on a sibling guide
(e.g. "cowpea" landing on `dry-bean`). Google Trends gives relative interest for candidates with no
site traffic yet. Neither was available from this repo. Review 1 §3 found no sitemap or search data
on disk, and that is unchanged. **Not measured; the rankings above are supply-side (what extension
publishes), not demand-side.**

## 6. Routing summary (into the master list's buckets)

| bucket | adds from this review |
|---|---|
All buckets were taken as proposed by Trevor on 2026-10-02, with the additions marked "ruled".

| bucket | adds from this review |
|---|---|
| FIRST BATCH | none |
| LATER | **chayote, luffa** (two new v2 rows; G-13 error), **jicama (low; toxicity noted)**, cardoon, claytonia, orach, pineapple guava, roselle, wasabi (low), sesame/culantro/Cuban oregano/Mexican tarragon (low) |
| LATER (low) | **garden cress** (may fold into the microgreens family) |
| open question on v2's `amaranth` row | **leaf amaranth**: Trevor leans one crop with leaf use as the harvest shape; rule-7 call for the archetype session |
| WANTED LANE (tropical) | **ginger (+ turmeric), after pineapple**; atemoya, sweetsop, soursop, mamey sapote, tamarind as later members |
| VARIETY NOT PARENT | kalettes -> brussels-sprouts; loganberry/tayberry/olallieberry -> blackberry; Italian dandelion -> radicchio row; datil -> hot pepper; boniato -> sweet-potato |
| NO SOURCE PATH (commercial only) | goji, lemon verbena, bay laurel, prickly pear |
| NO SOURCE PATH (grains lane) | **rice**: commercial-only extension coverage; lead is Cornell's Northeast SRI work; hunted with buckwheat, quinoa and rye (§3a) |
| **RE-MEASURE: T1 index page found** (moved out of NO SOURCE PATH, not re-ruled) | starfruit, miracle fruit, lingonberry, walking / Egyptian onion |
| lead for an owed hunt | hops: UF Gardening Solutions index |
| April-proposal priority | **rule the English-pea row (W5) first** (NGA peas #10 at 24%) |
| out of scope | non-food (catnip, feverfew, valerian, ginseng, gourds, ornamentals), sprouts |

**Net change to v2's parent count:** +2 LATER rows (chayote, luffa), plus whatever §1-§3's other
LATER rows add when the master list is next re-issued. Four rows move from NO SOURCE PATH to
RE-MEASURE.

## 7. Not done (by design)

No crop added, no canonical edit, no crop page read, and no 2026-09-30 ruling re-ruled. Shipped
with Oregon State PARTIAL (429) and UC Home Orchard / VRIC unreachable (403); see the
northern-coverage line in §0 for where a re-run should look. No zone claim here is sourced.

## Appendix: index evidence (raw bytes, sha256 first 12)

| list | index URL | sha256 | names |
|---|---|---|---|
| Cornell vegetables | http://www.gardening.cornell.edu/homegardening/scene0391.html | 089270fcf7e2 | 61 |
| Cornell fruit | https://gardening.cals.cornell.edu/garden-guidance/foodgarden/ | 7ecbc95dae10 | 10 |
| UMN vegetables + fruit | https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota | fbd1573e8850 | 45 + 11 |
| UMN herbs | .../gardening-in-minnesota/growing-herbs | 157cb583eca6 | 6 |
| Clemson vegetables | https://hgic.clemson.edu/category/vegetables/ (8 pp) | 40ca68e81ab0 +7 | 41 |
| Clemson tree fruits | https://hgic.clemson.edu/category/tree-fruits/ (3 pp) | 3edcdbed48e6 +2 | 12 |
| Clemson small fruits | https://hgic.clemson.edu/category/small-fruits/ (2 pp) | 48002b969026 +1 | 5 |
| Clemson nuts | https://hgic.clemson.edu/category/nuts/ | c9cfb193c0ac | 1 |
| OSU vegetables (partial) | extension.oregonstate.edu/topic/gardening/vegetables/resources (publications) | 4dd53cf6ed7c, 132e27a1c89c, db4bacf6e274 | 7 |
| OSU fruit (partial) | extension.oregonstate.edu/topic/gardening/berries-fruit/resources (publications) | 0a5604bac670, dde47931741d | 3 |
| Ohio State vegetables | https://ohioline.osu.edu/findafactsheet?field_ol_unique_id_value=HYG-16 | 67e54081a4b4, 740478be6948 | 10 |
| Ohio State fruit | https://ohioline.osu.edu/findafactsheet?field_ol_unique_id_value=HYG-14 | 55f9538a311c +2 | 12 |
| WSU vegetables + fruit | https://pubs.extension.wsu.edu/product-category/publications/gardening/ (+ search) | 5dedb2a6fa22 +12 | 8 + 7 |
| UC ANR vegetables | https://ipm.ucanr.edu/home-and-landscape/pests-in-gardens-and-landscapes/ (+ PMG/GARDEN/veggies.html) | a7953eccd65c, 82ec64264e99 | 32 |
| UC ANR fruit | same (+ PMG/GARDEN/fruit.html) | a7953eccd65c, 783fce995b8d | 18 |
| UF VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b | 40 |
| UF GS vegetables | https://gardeningsolutions.ifas.ufl.edu/plants/edibles/vegetables/ | 132a6b2174ee, 0e2d193112a0 | 79 |
| UF GS fruits | https://gardeningsolutions.ifas.ufl.edu/plants/edibles/fruits/ | 4bc865944751 | 34 |
| UF GS herbs | https://gardeningsolutions.ifas.ufl.edu/plants/edibles/herbs/ | e9b78ec04b88 | 20 |
| TAMU Easy Gardening | https://aggie-horticulture.tamu.edu/vegetable/easy-gardening-series/ | 7f1ce7aec900 | 31 |
| TAMU vegetable guides | https://aggie-horticulture.tamu.edu/vegetable/guides/ (+ specialty) | 17a14e63133c, 81acc1d1cbb9 | 73 |
| TAMU fruit & nut | https://aggie-horticulture.tamu.edu/fruit-nut/ (+ fact-sheets) | 9bfbddc65089, 8fff9e10cae4 | 32 |
| NGA 2009 survey | gardenresearch.com 2009 white paper (live 403; Wayback 2012 bytes) | e80cad7f93ba | 32 ranked |
| USDA 1975 survey | ageconsearch record 325763, 1977-57.pdf (live 202; Wayback bytes) | 1f980524d9af | 19 ranked |
| GrowVeg (commercial) | https://www.growveg.com/plants/us-and-canada/ | 48ed86fd6bfe | 176 |
| Johnny's (commercial) | https://www.johnnyseeds.com/ (menu tree) | 7d40aec4d7b9 | 123 |
| Territorial (commercial) | territorialseed.com/collections.json (3 pp, hand-curated crop handles) | 54aa6fab0851 +2 | 146 |
