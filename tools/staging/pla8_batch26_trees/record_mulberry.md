# PLA-8 batch 26 -- RECORD / SOURCE PASS: mulberry (`mulberry`)

Reviewer pass date: 2026-09-04. Canonical ce98b0a6, READ-ONLY; nothing edited but this file.
Six entries: pests Birds, Whiteflies, Borers; diseases Popcorn disease, Bacterial blight, Leaf spots and
minor foliar diseases. Every document below was fetched 2026-09-04. Retrieval path is stated per anchor
because `curl` was DENIED by the session permission system on this pass (never reached any server), so
the fallback order actually available was WebFetch first-party -> WebFetch on the `r.jina.ai/` proxy.
Local `pypdf` extraction of downloaded PDFs was also denied, so the three PDFs below are proxy reads.

Documents read, keyed for the sections (path: FP = first-party WebFetch; PX = r.jina.ai proxy only):

| tag | document | path | admission |
|---|---|---|---|
| D1 | NCSU Plant Toolbox, Morus alba, https://plants.ces.ncsu.edu/plants/morus-alba/ | FP | `ncsu_ext` |
| D2 | NCSU Plant Toolbox, Morus rubra, https://plants.ces.ncsu.edu/plants/morus-rubra/ | FP | `ncsu_ext` |
| D3 | UF/IFAS Gardening Solutions, Mulberry, https://gardeningsolutions.ifas.ufl.edu/plants/edibles/fruits/mulberry/ (same text at .../trees-and-shrubs/trees/mulberry) | FP | `uf_ifas` |
| D4 | UF/IFAS Orange County blog, "Marvelous Mulberries" (H. Kalaman, 2023-09-11), https://blogs.ifas.ufl.edu/orangeco/2023/09/11/marvelous-mulberries/ | FP | `uf_ifas` |
| D5 | Texas Plant Disease Handbook, Mulberry, https://plantdiseasehandbook.tamu.edu/landscaping/trees/mulberry/ | FP (three passes; the summarizer refused a whole-page reproduction on pass 1 and returned per-sentence quotes on passes 2-3) | `tamu_agrilife` |
| D6 | OSU Digital Diagnostics, Popcorn Disease of Mulberry (published 2021-04-13), https://extension.okstate.edu/programs/digital-diagnostics/plant-diseases/popcorn-disease-of-mulberry.html | FP 403 on BOTH the `.html` and the extensionless URL; PX returned the full body | `ok_state_ext` |
| D7 | NCSU Extension, "Mulberry Whitefly" (J. Baker, 2017-03-10, rev. 2021-12-21), https://content.ces.ncsu.edu/mulberry-whitefly | FP | `ncsu_ext` |
| D8 | UAEX Reference Desk, Mulberry (Q&A page), https://www.uaex.uada.edu/yard-garden/in-the-garden/reference-desk/trees/mulberry.aspx | FP | `uada_ext` |
| D9 | UAEX Plant Health Clinic Newsletter, Issue 15, June 6 2016 (Sherrie Smith), PDF, https://www.uaex.uada.edu/yard-garden/plant-health-clinic/docs/2016_Plant_Health_Clinic_Newsletters/Plant%20Health%20Clinic%20Newsletter-Issue%2015.pdf | FP returned no text; PX extracted | `uada_ext` |
| D10 | PNW Plant Disease Management Handbook, "Mulberry (Morus spp.)-Bacterial Blight" (latest revision March 2026), https://pnwhandbooks.org/plantdisease/host-disease/mulberry-morus-spp-bacterial-blight | FP 403; PX | NEEDS-CATALOG-ADMISSION (only the scoped `pnw_handbook_epn` exists) |
| D11 | K-State Research and Extension MF2735, "Borers: Common Kansas Species" (R. Bauernfeind, Oct 2006), PDF, https://bookstore.ksre.ksu.edu/pubs/borers-common-kansas-species-home-and-horticultural-pests_MF2735.pdf | FP returned no text (image-heavy PDF); PX extracted | NEEDS-CATALOG-ADMISSION (no Kansas State key; `ksu_pawpaw` is Kentucky State) |
| D12 | OSU fact sheet, "Anthracnose and Other Common Leaf Diseases of Deciduous Shade Trees" (published 02/01/2017; number not visible in the proxied text), https://extension.okstate.edu/fact-sheets/anthracnose-and-other-common-leaf-diseases-of-deciduous-shade-trees | FP 403; PX | `ok_state_ext` |
| D13 | UC IPM Pest Notes 7401, Whiteflies (updated 09/2015), https://ipm.ucanr.edu/PMG/PESTNOTES/pn7401.html | FP | `uc_ipm`, home |
| D14 | UC IPM Pest Notes 7400, Giant Whitefly (updated 03/2024), https://ipm.ucanr.edu/PMG/PESTNOTES/pn7400.html | FP | `uc_ipm`, home |
| D15 | UC IPM home-and-landscape, Mulberry, https://ipm.ucanr.edu/PMG/GARDEN/PLANTS/mulberry.html | FP | `uc_ipm`, home, TITLE ROWS (rule 7) |
| D16 | UC IPM home-and-landscape, Bacterial Blast, Blight, and Canker, https://ipm.ucanr.edu/home-and-landscape/bacterial-blast-blight-and-canker/ | FP | `uc_ipm`, home; mulberry NOT named |
| D17 | UGA CAES C1261, Flatheaded appletree borer (Hudson, Joseph, Williamson, 2023-03-31); NCSU "Flatheaded Appletree Borer" (Baker, 2018-11-15) | FP | `uga_ext`, `ncsu_ext`; mulberry NOT named on either |
| D18 | UKY Entomology, "Common Insect Pests of Mulberry" (Townsend and Larson), https://www.uky.edu/Ag/Entomology/treepestguide/mulberry.html | FP | not in catalog |
| D19 | MSU Extension E2747, "Unusual Fruit Plants for Gardens in the North Central Region", https://www.canr.msu.edu/resources/unusual_fruit_plants_for_gardens_in_the_north_central_region_e2747 | FP returned an empty body; PX | `msu_ext` (catalog URL is https://www.canr.msu.edu/resources) |
| D20 | MSU Extension, "Managing bird damage on fruit farms" (2019-06-21), https://www.canr.msu.edu/news/managing-bird-damage-on-fruit-farms | FP empty body; PX | `msu_ext`; mulberry NOT named |
| D21 | UGA CAES, "Plant Berries for Birds in Your Wild Garden" (Jeff Jackson, Extension Forest Resources, 1996-02-26), https://fieldreport.caes.uga.edu/news/458/ | FP (via 307 from newswire) | `uga_ext` |
| D22 | Galveston County Master Gardeners GH-067, "Popcorn Disease on mulberry" (Fichtner and Goodwin, "Texas AgriLife Extension"), https://txmg.org/galveston/wp-content/blogs.dir/114/files/2022/11/GH-067-popcorn-disease-on-mulberry.pdf | FP no text; PX. The tamu.edu-hosted copy (hortipm.tamu.edu/galveston/...) 302-redirects to the Aggie Horticulture home page, i.e. dead | admission UNDECIDED: self-identifies as Texas AgriLife Extension but is hosted off tamu.edu |
| D23 | Mississippi Fruit and Nut Blog, "Popcorn Disease of Mulberry" (E. Stafne, MSU Extension, 2015-05-18), https://msfruitextension.wordpress.com/2015/05/18/popcorn-disease-of-mulberry/ | FP | `msstate_ext` by citable_for wording, but a wordpress host; weak |
| D24 | UF/IFAS EDIS ENH-567/ST-408, Morus alba Fruitless Cultivars (Gilman and Watson) | live EDIS 410 Gone; ask.ifas.ufl.edu 410; both hort.ifas.ufl.edu PDF paths 301 to the hos.ifas.ufl.edu root. NOT READ. Search snippet only: "Pests are scale and mites. Leaf spot, bacterial blight, powdery mildew, and cankers may infect this tree." Not used as an anchor | `uf_ifas_edis`, archived |
| D25 | Purdue CERIS / PestTracker, "Mulberry borer (Xylotrechus chinensis)", https://www.pesttracker.org/pest?code=INALQTA | FP | not an anchor; name-collision note only |

Unreadable on every path (absence findings are document-scoped, so recorded, not inferred from):
UMN "Bring more birds to your home with native plants" (403 FP; proxy returned an "Access denied" body).

---

## Birds [pests]  -- severity high, type pest
STATUS: SOURCED-OK
ORGANISM: vertebrate; not a single taxon. Named for THIS crop by extension: gray catbird and northern
  mockingbird (D2), cedar waxwing (D8). Robin is NOT paired with mulberry by any admissible document read.
ANCHORS:
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-alba/ -- verified 2026-09-04 -- toolbox page, but the
  quoted lines are prose fields, not the linked title rows (I checked: no word in the problems field is a link)
  > "Birds love the fruit. Also eaten by opossum, raccoon, fox squirrel, and gray squirrel; white-tailed deer browse on the leaves and twigs, while beavers gnaw on the wood."
  > "The fruits are relished by birds, but dropped fruit can cause maintenance issues such as staining concrete walkways, patios, and cars."
  > "It is resistant to drought and pollution, while also attracting songbirds."
  > "Fertilized flowers on female trees produce sweet, edible blackberry-like fruits (cylindrical drupes to 1inch long) that mature in June."
  > Attracts: "Songbirds"
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-rubra/ -- verified 2026-09-04 -- toolbox prose field (NOT in the record's anchoring_urls; add it, it is the stronger page)
  > "Its fruits are eaten by many birds, especially gray catbirds and northern mockingbirds, foxes, opossums, squirrels, and raccoons."
  > "Weedy self-seeding and messy fruit are concerns."
  uf_ifas https://gardeningsolutions.ifas.ufl.edu/plants/edibles/fruits/mulberry/ -- verified 2026-09-04 -- home
  > "Mulberry fruits are quite popular with wildlife. Visiting creatures will reduce the harvest for your personal use, but on a good sized tree there should be enough fruits for all to enjoy."
  > "When choosing a location, keep in mind that fallen fruits stain the surfaces they land on, so it's best to avoid planting over driveways, sidewalks and patios."
  > The page carries NO other pest or disease text; it does not say "birds".
  uada_ext https://www.uaex.uada.edu/yard-garden/in-the-garden/reference-desk/trees/mulberry.aspx -- verified 2026-09-04 -- home (Q&A)
  > "Cedar Waxwing birds were having a feast on the berries, which resembled a small raspberry or blackberry."
  > "Once birds start feasting, they often send some messy missiles on patio furniture and the like."
  msu_ext https://www.canr.msu.edu/resources/unusual_fruit_plants_for_gardens_in_the_north_central_region_e2747 -- verified 2026-09-04 -- PROXY read (first-party returned an empty body), home bulletin E2747
  > "Mulberry fruit is very attractive to birds, and the trees may be planted strategically to lure birds away from a high-value fruit crop."
  uga_ext https://fieldreport.caes.uga.edu/news/458/ -- verified 2026-09-04 -- home (1996)
  > "Later in the spring come red and white mulberries, followed by wild black cherry,"
  > visitors named on the page: "the mockingbird, brown thrasher, catbird, robin, cedar waxwing, red-bellied woodpecker, bluebird" -- the page does NOT pair any species with mulberry.
  msu_ext https://www.canr.msu.edu/news/managing-bird-damage-on-fruit-farms -- verified 2026-09-04 -- PROXY read; commercial fruit-farm audience, generic (mulberry not named)
  > "Excluding birds with netting is considered cumbersome and expensive by many growers"
  > "It is the most effective means to prevent fruit damage"
  > "Netting must be properly installed and maintained to completely exclude the birds"
  > "Robins generally feed as individuals, waxwings in small flocks up to 10 birds"
  The uf_ifas "Marvelous Mulberries" post (D4) that the cert log leans on carries NO bird, pest or disease text at all; it is a pollination/species anchor only.
RECORD CLAIMS THAT HOLD:
  - birds strip ripe fruit / "Birds love the fruit" -- D1, D2, D8
  - purple droppings and fruit mess on surfaces -- D8 ("messy missiles on patio furniture"); staining from dropped fruit -- D1, D3
  - catbirds, mockingbirds -- D2; waxwings -- D8
  - "one of the best wildlife trees you can plant" -- D1 wildlife list; D2
  - a big tree yields enough to share -- D3 verbatim
  - mulberry as a decoy to lure birds off prized fruit -- D19 verbatim (proxy read)
  - netting is the effective exclusion -- D20 (generic fruit-farm page, not mulberry-specific)
RECORD CLAIMS WITH NO ANCHOR:
  - "robins" as a named mulberry feeder (D21 lists robins as berry visitors but never pairs them with mulberry)
  - "flocks work the tree through the ripening weeks" / "Big flocks can show up daily"
  - "This is the number-one reason home growers lose fruit" (D3 says visiting creatures reduce the harvest; no document ranks it)
  - "harvest ripe fruit promptly each day so less hangs available" / "pick promptly"
  - "Net only small or dwarf trees" (netting is anchored generically by D20; no document scopes it to small mulberries)
RECORD CLAIMS THAT ARE WRONG: none found.
BUNDLE / GENERIC VERDICT: n/a (single problem class, vertebrate).
LADDER-RELEVANT FACTS the record does not carry:
  - vulnerable window: fruit "mature in June" (D1, M. alba, NC); the harvest-window ruling file already records the red-mulberry May-June row.
  - D20's netting economics are commercial ("may pay for itself in a year or two by doubling the harvestable yields"); the home-tree cost/benefit is not published in anything read.
  - the decoy sentence (D19) is the only extension statement found that treats the bird pressure as a FEATURE to plan around; it is from a North Central (zone 5-8) bulletin.
  - D19 hardiness line, for the region pass: "Hardy to zones 5 to 8, possibly 4 to 9."
PLA-457: none seen.

## Whiteflies [pests]  -- severity low, type pest
STATUS: SOURCED-OK
ORGANISM: umbrella of whitefly species, and the umbrella is the sources' own framing. Named for mulberry:
  Tetraleurodes mori Quaintance, the mulberry whitefly (Aleyrodidae), per D7; Aleurodicus dugesii, giant
  whitefly, with "Morus alba" in its host list per D14 (California range only).
ANCHORS:
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-alba/ -- verified 2026-09-04 -- toolbox prose field, unlinked
  > "No serious insect or disease problems. Borers and whiteflies can be problems. Bacterial blight may kill foliage/branches. Coral spot cankers may cause twig dieback."
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-rubra/ -- verified 2026-09-04 -- toolbox prose field
  > "Borers may be a problem with this plant, particularly in the South. Whiteflies mass on some trees."
  ncsu_ext https://content.ces.ncsu.edu/mulberry-whitefly -- verified 2026-09-04 -- home factsheet (THE anchor; add to anchoring_urls)
  > "The mulberry whitefly, Tetraleurodes mori, is a minor pest of shrubs and trees in North Carolina."
  > "About two weeks later, from the eggs hatch tiny yellow nymphs called crawlers that move about before settling down to insert their mouthparts to feed."
  > "With each molt, nymphs become larger, darker, and eventually are shiny black with a conspicuous white fringe."
  > "Adult mulberry whiteflies are pale gray with conspicuous darker gray spots, jagged lines, and markings on the forewings."
  > "excrete honeydew (a sweet, sticky liquid in which sooty molds often grow)."
  > "Mulberry whiteflies have been reported from American holly, avocado, boxelder, citrus, flowering dogwood, mountain laurel, mulberry, Norway maple, red maple, Virginia sweet spire, and wax myrtle."
  > "The mulberry whitefly is not particularly resistant to pesticides. Insecticidal soaps work well on adult whiteflies. Horticultural oils should give some control of the nymphs."
  > "the mulberry whitefly is usually more of a curiosity than a pest, it is probably not necessary to treat infested plant unless the whiteflies become tremendously abundant."
  uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn7400.html -- verified 2026-09-04 -- home (Pest Notes 7400, Giant Whitefly, updated 03/2024)
  > "The giant whitefly, Aleurodicus dugesii, an insect native to Mexico, was first discovered in the United States in Texas in 1991."
  > host list includes, under Moraceae, "Morus alba"
  > "The use of a strong stream of water directed to the undersides of infested leaves can be very effective in managing giant whitefly."
  > "Parasitic wasps (also called parasitoids) are the most important natural enemies of giant whitefly."
  > "If you choose to use insecticides, select least-toxic products such as insecticidal soaps or oils."
  uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn7401.html -- verified 2026-09-04 -- home (Pest Notes 7401, Whiteflies, 09/2015); GENERIC whitefly advice, mulberry not named
  > "Many beneficials or 'natural enemies' such as lacewings and lady beetles help control whiteflies."
  > "Hose adults off plants with a strong stream of water."
  > "Prune out isolated infested leaves when you first detect them."
  > "Use soaps or oils when plants are not drought-stressed and when temperatures are under 90°F to prevent possible 'burn' damage."
  > "Low levels of whiteflies are not usually damaging. Adults by themselves will not cause significant damage unless transmitting a plant pathogen."
  > "Avoid using broad spectrum pesticides such as pyrethroids, organophosphates, or neonicotinoids."
  uc_ipm https://ipm.ucanr.edu/PMG/GARDEN/PLANTS/mulberry.html -- verified 2026-09-04 -- home; TITLE ROWS ONLY (rule 7): lists "Whiteflies" and "Giant Whitefly" as linked factsheet titles under Invertebrates. Corroborates the umbrella, asserts nothing.
RECORD CLAIMS THAT HOLD:
  - tiny white flies on leaf undersides; honeydew and sooty mold -- D7
  - "including the mulberry whitefly" -- D7 names it and lists mulberry as a host
  - common but minor, cosmetic -- D7 ("minor pest", "more of a curiosity than a pest")
  - a healthy tree needs no treatment -- D7 ("probably not necessary to treat")
  - strong water spray to undersides -- D14 (giant whitefly), D13 (generic)
  - insecticidal soap -- D7, D13, D14
  - lacewings and ladybugs -- D13 (generic whiteflies, home)
  - "Natural predators usually keep them in balance outdoors" -- D13 (generic), D14 (parasitoids)
RECORD CLAIMS WITH NO ANCHOR:
  - "avoid heavy nitrogen feeding, which encourages the soft growth whiteflies favor" / "go easy on nitrogen feeding, which draws whiteflies" -- NOT in D7, D13 or D14 (D13 checked explicitly: no nitrogen or fertilizer sentence). Either find a document or drop it.
  - "lift off the undersides of leaves when disturbed" -- generic behavior; no document quoted says it (harmless, but unanchored)
RECORD CLAIMS THAT ARE WRONG: none.
BUNDLE / GENERIC VERDICT: keep as an umbrella "Whiteflies"; the anchors themselves say "whiteflies" (D1, D2) and the two named species are regional (T. mori in the Southeast, giant whitefly in California). The record's parenthetical "including the mulberry whitefly" is correct and now anchored.
LADDER-RELEVANT FACTS the record does not carry:
  - stage-specific tools: soap for adults, horticultural oil for nymphs (D7); a 90°F ceiling for soaps and oils (D13)
  - life cycle: eggs hatch in about two weeks; nymphs are sessile until adults emerge "a month or more later" (D7); the black white-fringed pupa is the ID stage
  - neighboring landscape hosts (holly, dogwood, maples, citrus, wax myrtle) are reservoirs (D7)
  - do not use pyrethroids / organophosphates / neonicotinoids, which destroy the natural enemies (D13)
  - "Prune out isolated infested leaves when you first detect them" (D13) is a physical rung the record lacks
PLA-457: none seen. Oils are named by D7 and D13 with no sulfur interval.

## Borers [pests]  -- severity low, type pest
STATUS: SOURCED-WEAK
ORGANISM: umbrella in the ADMISSIBLE literature; ONE organism is named for this crop only by a T1 that is
  not in the catalog. Dorcaschema wildii Uhler, the mulberry borer (Cerambycidae), hosts "Mulberry, Osage
  orange", per D11 (K-State MF2735, proxy read). D11 also lists mulberry as a host of the painted hickory
  borer, Megacyllene caryae. No admissible document read names ANY borer species for mulberry.
  TAXON TRAP: "mulberry borer" is also the common name of Xylotrechus chinensis, "a native of Asia" (D25,
  Purdue PestTracker), an Asian pest not the US insect. Do not resolve the entry to that binomial.
ANCHORS:
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-alba/ -- verified 2026-09-04 -- toolbox, but a PROSE field: I asked for hrefs and none of the words are hyperlinked, so this is a statement, not a factsheet title (rule 7 satisfied)
  > "No serious insect or disease problems. Borers and whiteflies can be problems."
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-rubra/ -- verified 2026-09-04 -- toolbox prose field (not in the record's anchoring_urls; add)
  > "Borers may be a problem with this plant, particularly in the South."
  NEEDS-CATALOG-ADMISSION: Kansas State Research and Extension, MF2735 "Borers: Common Kansas Species: Home and Horticultural Pests" (Robert Bauernfeind, Entomologist, October 2006), https://bookstore.ksre.ksu.edu/pubs/borers-common-kansas-species-home-and-horticultural-pests_MF2735.pdf -- verified 2026-09-04 -- PROXY read (first-party WebFetch found no extractable text; local pypdf denied) -- home/horticultural bulletin
  > "Dorcaschema wildii Uhler"
  > hosts: "Mulberry, Osage orange"
  > "5/8 to 7/8 inch long; cylindrical front thorax gives it 'necked' appearance; coat of fine gray hairs conceals dark brown body; small round bare spots give wing covers pitted appearance."
  > "Sap ooze from niches for egg-laying; fine frass from small larvae, coarse and fibrous from older larvae. Dieback on branches and part of crown during initial attacks."
  > "1 year. Larvae overwinter and beetles emerge mid-May to mid-June and live several weeks. Egg-laying continues into early July."
  > painted hickory borer "Megacyllene caryae (Gahan)", hosts "Ash, black walnut, hackberry, mulberry, oak"
  > general (not in the D. wildii entry): "Borers are considered secondary pests. They are often attracted to weakened and stressed hosts."
  > general: "Beetles deposit eggs in bark cracks and crevices and are especially attracted to wound areas."
  > general: "When adequate moisture is available small borer larvae do not survive water surging through tree vascular elements."
  > general: "Prune or remove and dispose of sick, dead, or fallen branches and limbs to deal with established borers."
  > general (shothole borers): "Applications after the fact are of little or no value"
  Checked and NOT naming mulberry: UGA C1261 flatheaded appletree borer (D17: "The FAB has a wide host range, and reportedly has attacked over 30 species of tree." -- mulberry absent); NCSU flatheaded appletree borer (D17: host sentence names apples, crabapple, crapemyrtle, dogwoods, hawthorn, linden, maples, oak -- mulberry absent); UC IPM mulberry page (D15) lists NO borer row at all; UKY "Common Insect Pests of Mulberry" (D18, not admissible) lists lace bugs, leafhoppers, twospotted spider mites, Comstock mealybugs, cottony camellia scale and NO borer.
RECORD CLAIMS THAT HOLD:
  - borers attack mulberry -- D1, D2 (D2 adds "particularly in the South", which the record does not carry)
  - entry holes / frass / oozing on trunk and limbs -- D11 D. wildii entry (inadmissible today)
  - prune out and destroy dead or infested wood -- D11 general sentence (inadmissible today)
  - no rescue spray once larvae are inside -- D11 general "Applications after the fact are of little or no value" (about shothole borers; inadmissible today)
RECORD CLAIMS WITH NO ANCHOR:
  - "Several wood-boring beetle and moth larvae can attack mulberry" -- no document read names a MOTH borer on mulberry; D11 names two beetles
  - "almost always as a secondary problem on trees weakened by drought stress, mechanical wounds, or age" / "Healthy, vigorous mulberries are seldom attacked" -- D11's stressed-host sentence is a GENERAL statement about borers; its D. wildii entry carries no such qualifier and instead describes crown dieback "during initial attacks". The UGA/NCSU stressed-tree sentences are about Chrysobothris femorata, whose host lists omit mulberry. At mulberry level this claim has NO document.
  - "water through droughts" as a control -- D11 general moisture sentence only (inadmissible)
  - "keep mowers and trimmers off the trunk" -- D11 general "especially attracted to wound areas" (inadmissible)
RECORD CLAIMS THAT ARE WRONG: none refuted; but see the unanchored "secondary on stressed trees" claim, which the only organism-level source does not make for the named mulberry borer.
BUNDLE / GENERIC VERDICT: GENUINE UMBRELLA in the admissible literature (two toolbox pages say "borers", nothing else admissible names one), with ONE pinnable organism (Dorcaschema wildii) sitting behind a catalog-admission decision. Recommendation for the orchestrator: (a) keep the id and name as an umbrella now, drop "and moth larvae", and soften the "almost always secondary" sentence to what D1/D2 say, or (b) admit K-State MF2735 and pin D. wildii as the named primary with M. caryae as a second host record, keeping "borers" as the umbrella name. Do NOT ladder a stressed-tree-only narrative from D. wildii's entry, which does not support it.
LADDER-RELEVANT FACTS the record does not carry:
  - D. wildii timing (D11): larvae overwinter in the wood; adults emerge mid-May to mid-June; egg-laying into early July -- this is the window for trunk inspection and for keeping the bark unwounded
  - egg niches ooze sap (D11): a monitoring signal the record does not give
  - crown/branch dieback is the first visible damage (D11), not the small holes the record leads with
  - "particularly in the South" (D2)
PLA-457: none seen.

## Popcorn disease [diseases]  -- severity medium, type disease
STATUS: SOURCED-OK (one prevention claim WRONG, below). The `ok_state_ext` anchor is still 403 first-party on BOTH URL forms, as at certification; it was read this pass only through the r.jina.ai proxy, which returned a complete body with no challenge page.
ORGANISM: Ciboria carunculoides (Siegler & Jenkins) Whetzel, fungus (Sclerotiniaceae), per D5, D6, D8, D9, D22 (D22 gives the full authority string).
ANCHORS:
  tamu_agrilife https://plantdiseasehandbook.tamu.edu/landscaping/trees/mulberry/ -- verified 2026-09-04 -- first-party, ornamental-tree handbook
  > "fungus – Ciboria carunculoides"
  > "This disease, known only in the southern states, is largely confined to the carpels of the fruit."
  > "It causes them to swell and remain greenish, and interferes with ripening."
  > "The disease is of little importance."
  > "It does not lessen the value of the tree as an ornamental."
  > TAMU carries NO control sentence for this disease.
  ok_state_ext https://extension.okstate.edu/programs/digital-diagnostics/plant-diseases/popcorn-disease-of-mulberry.html -- verified 2026-09-04 -- PROXY read only (403 first-party) -- home diagnostic page, published 2021-04-13
  > "The symptoms appear only on infected fruit. Carpels of the fruit are replaced by sclerotia, which enlarge and extend beyond healthy berries."
  > "White mulberry varieties and hybrids are more susceptible to popcorn disease."
  > "This disease is not considered economically important on ornamental mulberries."
  > "However, popcorn disease on mulberries propagated for fruit production can cause high yield losses."
  > "Control is achieved by taking sanitary measures. Remove and bury the infected fruit on the trees and any ground debris as it appears during the growing season."
  uada_ext https://www.uaex.uada.edu/yard-garden/in-the-garden/reference-desk/trees/mulberry.aspx -- verified 2026-09-04 -- first-party, home Q&A (add to anchoring_urls; it is a first-party sanitation anchor)
  > "It is caused by the fungus Ciboria carunculoides."
  > "Individual parts of the fruit called carpels are replaced by a fungal organism, which enlarge and extend beyond healthy berries."
  > "The resulting fruits look a bit like popped corn."
  > "Sanitation is your best method of control."
  > "Remove all the spent fruit from the tree and under it and destroy it."
  > "It wouldn't hurt to spray the tree this winter with dormant oil."
  > "While fungicides are not normally recommended there has been some success with a preventative spray of Bordeaux mix (a copper/lime fungicide) as the tree is leafing out."
  uada_ext Plant Health Clinic Newsletter Issue 15 (June 6 2016, Sherrie Smith) -- verified 2026-09-04 -- PROXY read of a PDF (first-party fetch returned no text)
  > "Popcorn Disease of Mulberry fruit is caused by the fungus, Ciboria carunculoides."
  > "Initially the carpels of the fruit swell and remain a greenish color instead of ripening."
  > "The enlarged carpels of the fruit are replaced by hardened sclerotia of the fungus."
  > "White mulberry varieties and hybrids are more susceptible than red or black mulberries."
  > "Popcorn Disease can be a problem, however, on mulberries propagated for fruit production."
  > "Sanitation is the best control option for homeowners."
  > "Clean up all fallen fruit and any diseased fruit still on the tree and remove them."
  admission UNDECIDED (Texas AgriLife Extension Galveston County MG handbook GH-067, hosted on txmg.org; the tamu.edu copy is dead) -- verified 2026-09-04 -- PROXY read
  > "Prepared by Art Fichtner, MG 2005 Camille Goodwin, MG 2008 Texas AgriLife Extension"
  > "Disease Pathogen Name : Ciboria carunculoides (Siegler & Jenkins) Whetzel"
  > "Period of Primary Occurrence : late May through July"
  > "White mulberry varieties and some hybrids are more susceptible to popcorn disease"
  > "Other types of mulberries are less susceptible"
  > "Disease carries from one season to the next so practice good garden sanitary measures"
  > "Fungicide sprays are not generally warranted for the home landscape"
  > "When control is desired, a Bordeaux mixture (originated in France) of 4-4-50 is effective"
  msstate_ext (weak host: wordpress blog of the MSU Extension fruit specialist) https://msfruitextension.wordpress.com/2015/05/18/popcorn-disease-of-mulberry/ -- verified 2026-09-04 -- first-party
  > "It occurs in late spring and early summer."
  > "The white mulberries are more susceptible to this disease."
  > "It is a serious disease if the tree is being cropped for commercial purposes; however, it does no harm to the overall health of the trees, thus homeowners do not need to worry (if the tree is only used for ornamental or shade purposes)."
  > "Spraying the tree with Bordeaux mixture may help too, but getting coverage over the entire tree may be problematic."
RECORD CLAIMS THAT HOLD:
  - swollen greenish carpels that never ripen, hard sclerotia -- D5, D6, D9
  - fruit "clings to the tree" -- D9 ("any diseased fruit still on the tree"), D6 ("infected fruit on the trees")
  - "largely a southern problem" -- D5 "known only in the southern states"
  - white mulberries most susceptible -- D6, D9, D22
  - minor on an ornamental, real fruit loss on a tree grown for eating -- D5 + D6 ("can cause high yield losses"); this closes open finding `mulberry_popcorn_severity` in favor of the record's "medium" for a fruiting audience, on a proxy-read anchor
  - sanitation: remove affected fruit on the tree, rake up fallen fruit and debris, bury or discard -- D6 ("Remove and bury"), D8 ("destroy"), D9
  - "no home spray that cures it" -- D8 ("fungicides are not normally recommended"), D22 ("not generally warranted for the home landscape"); note both name a PREVENTIVE Bordeaux spray as the exception, which the record omits
RECORD CLAIMS WITH NO ANCHOR:
  - "that is where the fungus overwinters" (fallen fruit and debris as THE overwintering site) -- D6 prescribes removing ground debris and D22 says the disease "carries from one season to the next"; no document read states the overwintering site or mentions apothecia
  - "Year-round sanitation" -- D6 says "as it appears during the growing season"
RECORD CLAIMS THAT ARE WRONG:
  - prevention_seasoned: "favor red mulberry or a more resistant hybrid over the most susceptible white types"; prevention_beginner: "choose a red mulberry or a tougher hybrid rather than the most susceptible white types". REFUTED: "White mulberry varieties and hybrids are more susceptible to popcorn disease." (D6); "White mulberry varieties and hybrids are more susceptible than red or black mulberries." (D9); "White mulberry varieties and some hybrids are more susceptible to popcorn disease" (D22). The sources put HYBRIDS in the susceptible class with white mulberry; the record invents a resistant-hybrid class. This matters because the canonical variety list (per the cert log's mid_atlantic finding) is mostly M. alba x rubra hybrids: Illinois Everbearing, Dwarf Everbearing, Silk Hope, Oscar. Only "red or black mulberries" (D9) are the less-susceptible class the record can name.
BUNDLE / GENERIC VERDICT: n/a (single organism).
LADDER-RELEVANT FACTS the record does not carry:
  - window: "late May through July" (D22), "late spring and early summer" (D23); symptoms are fruit-only (D6), so scouting is at fruit set
  - the one spray any document names is preventive Bordeaux "as the tree is leafing out" (D8), 4-4-50 (D22); whole-tree coverage is the practical limit (D23). D8 also volunteers a winter dormant-oil spray for a fungal fruit disease with no rationale; report as-is, do not carry it into a rung without a second source.
  - susceptibility gradient for the variety pass: white and hybrids > red or black (D9); no named resistant cultivar in anything read
  - no "no effective control" statement exists; every source says sanitation controls it
PLA-457: none seen. D8's "spray the tree this winter with dormant oil" names an oil with no sulfur interval.

## Bacterial blight [diseases]  -- severity low, type disease
STATUS: SOURCED-WEAK (identity and symptoms are first-party at TAMU; the pathovar is stated by two US institutions; the record's management and "cosmetic on an established tree" framing have no mulberry-level anchor, and the anchor's own control sentence contradicts the record's "no spray")
ORGANISM: Pseudomonas syringae pv. mori, bacterium, per D5 (first-party), D12 (proxy), D10 (proxy, not admissible).
ANCHORS:
  tamu_agrilife https://plantdiseasehandbook.tamu.edu/landscaping/trees/mulberry/ -- verified 2026-09-04 -- first-party
  > "bacterium – Pseudomonas syringae pv. mori"
  > "Watersoaked spots appear on leaves and shoots have black stripes."
  > "The leaves at the twig tips wilt and dry up."
  > "Some control is obtainable on young trees by pruning dead shoots in autumn and spraying with approved fungicides."
  ok_state_ext https://extension.okstate.edu/fact-sheets/anthracnose-and-other-common-leaf-diseases-of-deciduous-shade-trees -- verified 2026-09-04 -- PROXY read (403 first-party) -- home/yard-tree fact sheet, published 02/01/2017
  > "A blight of mulberry leaves is caused by a bacterium, Pseudomonas syringae pv. mori, which at first appears as water-soaked spots."
  > "The spots later become sunken and black."
  > "The leaves become distorted, and infected leaves on the twig tips wilt and die."
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-alba/ and .../morus-rubra/ -- verified 2026-09-04 -- toolbox prose field
  > "Bacterial blight may kill foliage/branches."
  msu_ext E2747 (proxy) -- verified 2026-09-04
  > "Powdery mildew can affect the leaves. Scales and two-spotted mites can be a problem, as is a bacterial blight on shoots and leaves."
  NEEDS-CATALOG-ADMISSION: PNW Plant Disease Management Handbook, "Mulberry (Morus spp.)-Bacterial Blight", latest revision March 2026, https://pnwhandbooks.org/plantdisease/host-disease/mulberry-morus-spp-bacterial-blight -- verified 2026-09-04 -- PROXY read (403 first-party); mixed audience (cultural section is general, chemical section is product/rate)
  > Cause: "Pseudomonas syringae pv. mori, a bacterium favored by cool, wet weather in spring."
  > "Young leaves are more susceptible to infection."
  > "Leaf spots are small and brown-black, usually with yellow haloes."
  > "Young shoots may show rapid necrosis and dieback. Occasional stem cankers occur, which may exude ooze."
  > "Minimize wounds to limbs and new shoots."
  > "Prune out and destroy infected shoots and branches during the late dormant season."
  > "Space plantings to provide good air circulation."
  > "The following are registered on weeping mulberry; do not use on edible types." (copper products: Badge X2, CuPRO 5000, Junction, Monterey Liqui-Cop, Nu-Cop 50 DF)
  uc_ipm https://ipm.ucanr.edu/home-and-landscape/bacterial-blast-blight-and-canker/ -- verified 2026-09-04 -- home; ORGANISM-LEVEL (P. syringae on lilac, stone fruit, apple, citrus, pear, oleander, olive); mulberry NOT named
  > "Disease development is favored by high moisture and low temperatures in spring."
  > "Pseudomonas syringae survives on plant surfaces."
  > "Prune and dispose of infected twigs and branches during the dry season."
  > "Do not wet foliage with overhead irrigation."
  > "Bactericide applications have not been found to give reliable control and spraying for P. syringae is not recommended."
RECORD CLAIMS THAT HOLD:
  - water-soaked spots turning dark; black streaks on young shoots; shoot tips die back -- D5, D12
  - the pathovar -- D5, D12
  - "may kill foliage/branches" is available from D1/D2 (stronger than the record's framing)
RECORD CLAIMS WITH NO ANCHOR (at mulberry level):
  - "spreads in cool, wet spring weather" -- only D10 (inadmissible) says it for mulberry; D16 says it for P. syringae generically
  - "Damage is usually cosmetic on an established tree" / "rarely threatens a healthy tree" / "minor mulberry disease" -- no document says so; D5 scopes its control to "young trees", D1/D2 say it "may kill foliage/branches"
  - "Prune out ... during dry weather" -- D16 (generic, "dry season"); D5 says "in autumn"; D10 says "late dormant season". Three documents, three timings, none of them "dry weather" for mulberry.
  - "avoid overhead watering that keeps foliage wet" -- D16 only (generic)
  - "Keep the canopy open" -- D10 only ("Space plantings to provide good air circulation", inadmissible)
  - "No spray is warranted on a home tree" -- supported in spirit by D16 (spraying "not recommended", generic) and by D10's "do not use on edible types"; CONTRADICTED in letter by the record's own anchor D5: "Some control is obtainable on young trees by pruning dead shoots in autumn and spraying with approved fungicides." (a fungicide prescription for a bacterium is the document's oddity; report, do not repair)
RECORD CLAIMS THAT ARE WRONG: none flatly refuted. The "cosmetic / minor" framing is the record's, not any source's.
BUNDLE / GENERIC VERDICT: n/a (single pathovar).
LADDER-RELEVANT FACTS the record does not carry:
  - vulnerable tissue: young leaves and new shoots (D10); entry through wounds (D10 "Minimize wounds")
  - pruning-timing options actually published: autumn (D5), late dormant season (D10), dry season (D16 generic)
  - copper is registered on WEEPING (ornamental) mulberry only, not edible types (D10), which is the sentence that keeps copper off a food-tree ladder
  - stem cankers with ooze on young shoots (D10) as a symptom the record lacks
PLA-457: none seen.

## Leaf spots and minor foliar diseases [diseases]  -- severity low, type disease
STATUS: SOURCED-OK (the umbrella is anchored first-party at TAMU, corroborated by OSU; the record's "cosmetic and seldom worth treating" severity gloss is NOT what the anchor says for two of the organisms)
ORGANISM: umbrella -- multiple organisms, per D5: Leaf Spots "fungi – Cercospora moricola, C. missouriensis, and Cercosporella spp."; False Mildew "fungus – Mycosphaerella mori"; Powdery Mildews "fungi – Phyllactinia corylea and Uncinula geniculata". D12 names "Cercospora moricola and Cercosporella mori". D2 and D19 add unnamed "powdery mildew".
ANCHORS:
  tamu_agrilife https://plantdiseasehandbook.tamu.edu/landscaping/trees/mulberry/ -- verified 2026-09-04 -- first-party; three SEPARATE entries
  Leaf Spots:
  > "The leaves of mulberry are spotted by these fungi in very rainy seasons."
  > "The Cercosporella fungus can cause defoliation of older trees."
  > "Valuable specimens should be sprayed with approved fungicide if leaf spots are serious."
  False Mildew:
  > "The foliage of mulberries growing in the southern states may suffer severely from attacks of this fungus."
  > "It appears in July as whitish, indefinite patches on the undersides of the leaves."
  > "Yellowish spores emerge from the stomata on the underside and spread out so as to form a white, cobweb-like coating."
  > "The infected leaves fall to the ground, and the overwintering or ascocarpic stage matures in spring on these leaves."
  > "Gather and burn all fallen leaves in autumn."
  > "Spray with approved fungicide mixture as soon as the mold appears in July."
  Powdery Mildews:
  > "The lower leaf surface is covered by a white, powdery coating of these fungi."
  > "Valuable specimens can be protected by occasionally spraying with approved fungicide."
  ok_state_ext (shade-tree leaf diseases fact sheet, D12) -- verified 2026-09-04 -- PROXY read (403 first-party) -- home/yard trees
  > "Leaves of mulberry trees are spotted by two fungi, Cercospora moricola and Cercosporella mori, which cause reddish‑brown spots."
  > "These diseases are most severe during rainy weather."
  > general Control: "Most leaf diseases of yard trees are controlled by gathering and destroying fallen, infected leaves."
  > general Control: "Trees that have been affected by leaf diseases every season should also be well fertilized and watered to maintain vigor."
  > general Control: "During very rainy springs when leaf diseases become severe, two to three fungicide applications are needed for good control."
  > general Control: "Begin when the leaves are first unfurling from the buds. Repeat when the leaves are half grown, and again when the leaves are fully developed."
  ncsu_ext https://plants.ces.ncsu.edu/plants/morus-rubra/ -- verified 2026-09-04 -- toolbox prose field
  > "Bacterial leaf scorch, powdery mildew, root rot, and witches broom may also occur."
  msu_ext E2747 (proxy) -- verified 2026-09-04
  > "Powdery mildew can affect the leaves."
RECORD CLAIMS THAT HOLD:
  - scattered fungal leaf spots in wet seasons -- D5, D12
  - whitish patches on undersides (false mildew) and powdery coating (powdery mildew) -- D5
  - "mostly late in the season": false mildew "appears in July" -- D5 (the record's "mid to late summer" is loosely that)
  - modest leaf drop on older trees in a wet season -- D5 ("defoliation of older trees"; false mildew "infected leaves fall to the ground")
  - the organism list in cause_seasoned (Cercospora, Cercosporella, false mildew, powdery mildews) -- D5, exactly
  - rake and remove fallen leaves in autumn -- D5 ("Gather and burn all fallen leaves in autumn"), D12
  - fungicides reserved for prized specimens with a serious problem -- D5 ("Valuable specimens should be sprayed ... if leaf spots are serious")
  - carryover on fallen leaves -- D5 ("the overwintering or ascocarpic stage matures in spring on these leaves")
RECORD CLAIMS WITH NO ANCHOR:
  - "keep the canopy open for airflow" / "Open-canopy pruning ... good air movement are the whole prevention program" -- no document read prescribes canopy pruning for mulberry leaf diseases; D12's prevention is leaf sanitation plus vigor
  - "Vigor and cropping are rarely affected" / "On mulberry these are cosmetic and seldom worth treating" / "carry these diseases without meaningful harm" -- no source says so; see WRONG below
RECORD CLAIMS THAT ARE WRONG (in tension with the anchor, not flatly refuted):
  - "these are cosmetic and seldom worth treating" versus D5 on false mildew: "The foliage of mulberries growing in the southern states may suffer severely from attacks of this fungus." and on Cercosporella: "The Cercosporella fungus can cause defoliation of older trees." The anchor grades two of the umbrella's members as capable of severe foliage loss in the South; the record's "cosmetic" is its own gloss. Keep severity low if the orchestrator wants, but the prose should not claim the sources say "cosmetic".
BUNDLE / GENERIC VERDICT: GENUINE UMBRELLA. The literature itself lists SEVEN named fungi across three separately headed TAMU entries and two at OSU, and no single organism dominates in any US extension document read. Management is shared across the umbrella (autumn leaf sanitation; fungicide only on valuable specimens; vigor), which is the argument for keeping one id. If a split is wanted, FALSE MILDEW (Mycosphaerella mori) is the only member with its own timing ("appears in July"), its own overwintering statement (ascocarps on fallen leaves) and its own severity grade ("may suffer severely" in the southern states), so it is the one candidate for a separate id; the Cercospora/Cercosporella spots and the two powdery mildews have nothing distinct to ladder.
LADDER-RELEVANT FACTS the record does not carry:
  - false mildew onset in July; its spores emerge from the undersides; overwintering ascocarps mature in spring on fallen leaves (D5) -- the autumn rake-up is the mechanism, not just tidiness
  - OSU's three-spray schedule for severe rainy springs (bud unfurl, half-grown, fully developed) is the only published timing for a fungicide rung; D5 gives "as soon as the mold appears in July" for false mildew
  - D12: fertilize and water to maintain vigor on trees hit every season; do not fertilize in early fall
  - no resistant cultivar named anywhere read
PLA-457: none seen.

---

## SUMMARY

STATUS counts: SOURCED-OK 4 (Birds, Whiteflies, Popcorn disease, Leaf spots and minor foliar diseases);
SOURCED-WEAK 2 (Borers, Bacterial blight); ANCHOR-MISPOINTED 0; UNSOURCED-NOT-FOUND 0; JOURNAL-ONLY 0;
WRONG entries 0, but ONE record claim is refuted (popcorn prevention) and two severity glosses are not what
their anchors say (bacterial blight "cosmetic"; leaf spots "cosmetic").

Single most important finding: the Popcorn disease prevention prose tells the grower to "favor red mulberry
or a more resistant hybrid" / "choose a red mulberry or a tougher hybrid", while all three documents that
grade susceptibility put HYBRIDS in the susceptible class with white mulberry ("White mulberry varieties and
hybrids are more susceptible to popcorn disease", OSU; "... more susceptible than red or black mulberries",
UAEX PHC). The canonical variety list is mostly M. alba x rubra hybrids (Illinois Everbearing, Dwarf
Everbearing, Silk Hope, Oscar), so the record's advice steers a grower toward the susceptible class while
claiming source support. The fix is to say red or black mulberries are less susceptible and stop there.

Second: "Borers" is a bare generic that the ADMISSIBLE literature leaves unresolved (two NCSU toolbox
prose sentences, no organism); the one US extension document that names a mulberry borer (K-State MF2735,
Dorcaschema wildii, hosts mulberry and Osage orange, adults mid-May to mid-June) is not in the catalog, its
entry does NOT say the beetle is secondary on stressed trees, and no document read names a moth borer on
mulberry. The record's "beetle and moth larvae ... almost always secondary" narrative has no mulberry-level
anchor.

Third: two anchors the record leans on are still not readable first-party. The `ok_state_ext` popcorn page
403s on both URL forms (as at certification) and was read only through the r.jina.ai proxy, which returned
a full body; the OSU shade-tree leaf-disease fact sheet is the same. Both should be flagged as proxy reads
in anchoring_urls, not marked verified as first-party.

Anchoring_urls to add (all first-party reads today): NCSU Morus rubra toolbox (Birds, Whiteflies, Borers);
NCSU "Mulberry Whitefly" factsheet (Whiteflies); UAEX Reference Desk mulberry (Birds, Popcorn); UC IPM PN
7400 and 7401 (Whiteflies, home); MSU E2747 (Birds decoy sentence; proxy read).

Catalog decisions surfaced: (1) NEEDS-CATALOG-ADMISSION Kansas State Research and Extension (MF2735),
the only organism-level mulberry borer document; (2) NEEDS-CATALOG-ADMISSION PNW Plant Disease Management
Handbook mulberry bacterial blight (the catalog has only the scoped `pnw_handbook_epn`), which carries the
"registered on weeping mulberry; do not use on edible types" copper sentence; (3) UNDECIDED whether
`tamu_agrilife` covers Galveston County MG GH-067 (self-identified Texas AgriLife Extension, hosted on
txmg.org, tamu.edu copy dead); (4) UF EDIS ST-408 is 410 Gone on every UF path, so it cannot be cited.

Problems the record does NOT carry that the documents do (for the orchestrator, not to add on this pass):
scales, mites and mealybugs (D2, D15, D18, D19); coral spot and other cankers (D1, D2, D5 lists six fungi);
cotton root rot, "White mulberry has been rated highly susceptible" (D5, Texas); stink bugs piercing fruit
(D8); bacterial leaf scorch / oleander leaf scorch, Xylella (D2, D15).

Consumer-copy check: no em dashes, no temperature strings, "plant" lowercase throughout the six entries.
Seasoned register uses "carpels", "sclerotia", "Cercospora and Cercosporella"; beginner register is
everyday-worded.

PLA-457 roll-up: no document read states a sulfur/oil interval. Oil mentions without an interval: NCSU
mulberry whitefly ("Horticultural oils should give some control of the nymphs"), UC IPM PN 7401 (soaps or
oils "under 90°F"), UAEX mulberry ("spray the tree this winter with dormant oil").

## PROPOSED TYPE
- Birds: `vertebrate` -- birds (catbirds, mockingbirds, cedar waxwings named by D2/D8); severity high stands.
- Whiteflies: `insect` -- Tetraleurodes mori (mulberry whitefly, D7), with Aleurodicus dugesii (giant whitefly, D14) in California; umbrella name kept.
- Borers: `insect` -- wood-boring beetles; Dorcaschema wildii (D11) is the only organism named for mulberry by any US extension document read; keep umbrella pending the K-State admission decision.
- Popcorn disease: `fungal` -- Ciboria carunculoides (Siegler & Jenkins) Whetzel (D5, D6, D8, D9, D22).
- Bacterial blight: `bacterial` -- Pseudomonas syringae pv. mori (D5 first-party; D12 proxy).
- Leaf spots and minor foliar diseases: `fungal` -- umbrella of Cercospora moricola, C. missouriensis, Cercosporella spp., Mycosphaerella mori, Phyllactinia corylea, Uncinula geniculata (D5).
