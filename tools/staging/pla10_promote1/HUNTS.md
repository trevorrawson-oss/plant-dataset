# PLA-10 promote 1: recorded spacing hunts (lane C, session 2, 2026-10-01)

Rules applied: a page counts only if (1) its publisher is in `catalog.tsv` (229 rows; catalog id recorded per page, otherwise "not catalogued"), (2) the sentence RECOMMENDS a between-plants planting distance for a home garden (inches or feet; a between-rows figure is recorded as a bonus), (3) it is not a research-trial layout, a per-acre commercial orchard density (COMMERCIAL_ONLY), a trellis density, an NCSU Toolbox footprint, a mature width/spread, a trap grid, a pollinizer distance, or a spacing for a sibling crop (sweet corn for field corn, snap bean for dry bean, peach for nectarine); group pages that NAME the crop do count, and (4) the quote is verbatim from the live page (table rows are quoted cell by cell, `|`-separated, because the raw HTML holds each cell separately). Pages the worklist already read against cached text are listed under "Already checked" and were not re-fetched unless a claim needed verifying. Fetch failures (403/404/blank PDF extraction) are recorded as such, not as "no spacing statement". Hyphens vs en dashes in quotes are as WebFetch rendered them; the re-fetch should tolerate `-`/`–` where noted.

## cosmos  (today: [12,18]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://edis.ifas.ufl.edu/publication/FP149 (301 -> https://ask.ifas.ufl.edu/publication/FP149) | uf_ifas_edis / ufifas_ext (edis.ifas.ufl.edu); ask.ifas.ufl.edu host also catalogued (ufifas_ae588) | FPS149/FP149 "Cosmos bipinnatus 'Sonata White' Sonata White Mexican Aster": "Place these plants 12 to 18 inches apart in the garden." and in Culture: "Plant spacing: 12 to 18 inches" | YES (cultivar fact sheet for the species; home-garden framing) |
| https://extension.usu.edu/yardandgarden/research/cosmos-in-the-garden.php | usu_ext | "A plant spacing of 1-2 feet apart is recommended; however, cosmos spaced closer together provide support for one another or create a screen or full backdrop in the garden." Also: "Thinning is not necessary though plant size is improved with more space." | YES (species page, home garden) |
| https://extension.psu.edu/sowing-annual-seeds | psu_ext | Table 1 "Representative spacings for annual flowering plant seeds." row: `Cosmos sp. | cosmos | 10–14` (column "Spacing (in inches)") | YES (table row; representative seed-packet spacings) |
| https://extension.illinois.edu/flowers/cosmos | uiuc_ext (extension.illinois.edu) | no spacing statement | no |
| Already checked (worklist, cached): NCSU toolbox cosmos-bipinnatus, UF gardeningsolutions cosmos, UC IPM cosmos, UMN diagnose page, EDIS EP452, UADA planting dates, UNR FS-02-61, USU dates | -- | no spacing | no |
Best page (if FOUND): https://edis.ifas.ufl.edu/publication/FP149, uf_ifas_edis, "Place these plants 12 to 18 inches apart in the garden." -> [12,18] inches; between-rows: none; scope note: names Cosmos bipinnatus (cultivar 'Sonata White' sheet, UF Environmental Horticulture), garden framing. Corroboration at species level: USU "A plant spacing of 1-2 feet apart is recommended" -> [12,24]. Judgment call: FP149 is a cultivar sheet; if a species-level page is preferred, USU gives [12,24].

## sweet-alyssum  (today: [4,8]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://extension.psu.edu/sowing-annual-seeds | psu_ext | Table 1 "Representative spacings for annual flowering plant seeds." row: `Lobularia maritima | sweet alyssum | 8–10` (column "Spacing (in inches)"); intro: "Using the optimum spacing requirements listed on the back of seed packets to determine how closely seeds can be sown (see Table 1)." | YES (table row naming the crop; home-garden seed sowing) |
| https://web.extension.illinois.edu/hortanswers/plantdetail.cfm?PlantID=10&PlantTypeID=1 | uiuc_ext (extension.illinois.edu subdomain) | no spacing statement | no |
| https://content.ces.ncsu.edu/extension-gardener-handbook/10-herbaceous-ornamentals | ncsu_ext | no alyssum spacing figure; only a generic rule "Plant tall, upright plants such as snapdragons about one-fourth as far apart as their mature height" | no |
| https://extension.msstate.edu/node/20285 | msstate_ext | HTTP 404 (search snippet claimed "6 to 8 inches apart"; page gone, unverifiable) | no |
| Already checked (worklist, cached): NCSU toolbox lobularia-maritima, UWisc hort sweet-alyssum (spread only), UF gardeningsolutions sweet-alyssum (size only), Clemson HGIC sweet-alyssum (spreads 12 in), UC SLO MG blog, Purdue vegcropshotline, Illinois flowers-fruits-frass blog | -- | no spacing | no |
Best page (if FOUND): https://extension.psu.edu/sowing-annual-seeds, psu_ext, table row `Lobularia maritima | sweet alyssum | 8–10` -> [8,10] inches; between-rows: none; scope note: names the crop (scientific + common name) in a representative-spacing table for annual flower seeds sown in the home garden. Judgment call: a table cell, not a prose sentence, and the dash is an en dash in the rendered page. Today's [4,8] is NOT supported by any page found.

## echinacea  (today: [18,24]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://edis.ifas.ufl.edu/publication/FP192 (301 -> https://ask.ifas.ufl.edu/publication/FP192) | uf_ifas_edis / ufifas_ext | FPS192/FP192 "Echinacea purpurea Purple Coneflower": "Plant spacing: 18 to 24 inches" | YES (species fact sheet, Culture section) |
| Already checked (worklist, cached): PSU purple-coneflower (no number), UF gardeningsolutions purple-coneflower (clump size), Clemson HGIC echinacea (widths), NCSU toolbox, UIUC hortanswers | -- | no spacing | no |
Best page (if FOUND): https://edis.ifas.ufl.edu/publication/FP192, uf_ifas_edis, "Plant spacing: 18 to 24 inches" -> [18,24] inches; between-rows: none; scope note: names Echinacea purpurea; UF Environmental Horticulture landscape fact sheet. Matches today's value exactly.

## cherry-sour  (today: [180,300]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://extension.illinois.edu/fruit-trees/planting | uiuc_ext (extension.illinois.edu) | "Planting | Fruit Trees for Home Gardens"; table "Recommended tree spacing", headers `Fruit or Variety | Rootstock | Spacing in Feet`; "Spacings are within row and between row spacings. For example, with a 10 x 16 spacing the trees are planted 10 feet apart in the row with the rows 16 feet apart."; rows: `Sour Cherry: Montmorency | Seedling (standard) | 14 x 22 to 20 x 26`, `Sour Cherry: Meteor | Seedling (standard) | 10 x 16 to 12 x 18`, `Sour Cherry: North Star | Seedling (standard) | 8 x 12 to 10 x 14` | YES (home-garden table naming sour cherry by variety) |
| https://extension.unh.edu/resource/growing-fruits-growing-plums-cherries-and-apricots-nh-home-orchards-fact-sheet | unh_ext | "Plant plum, apricot, and cherry trees 15 to 20 feet apart in the home orchard." Page names the crop: "Sour or pie cherries that have performed well in NH include Montmorency, North Star, and Meteor." | YES (group sentence; page names sour cherries; home orchard) |
| https://extension.umn.edu/fruit/growing-stone-fruits-home-garden | umn_ext (extension.umn.edu) | Quick facts: "Space trees 12 to 20 feet apart."; also "two trees with a mature height of 15-20 feet will need to be spaced at least 20 feet apart at planting."; names the crop: "Of all types of cherries, tart cherries (also known as pie or sour cherries) are best adapted to northern climates." | YES (group page naming tart cherries; home garden) |
| https://extension.umaine.edu/fruit/growing-fruit-trees-in-maine/spacing/ | umaine_ext | "semi-dwarf trees about 15 feet, and standard or full-sized trees about 25 feet." and "Apricot, plums, peaches and sour cherries are similar in size to semi-dwarf apple trees." (so sour cherry ~15 ft by inference) | marginal (figure reached by inference across two sentences) |
| https://ag.purdue.edu/department/hla/extension/extension-publications-library/ext-pubs/ho-9-w.html | not catalogued (host ag.purdue.edu; catalog has extension.purdue.edu) | "Traditionally, cherry trees grew very large and had to be planted far apart to allow for their full size. Tree spacing was 20-24 feet apart for tart cherries and 25-30 feet apart for sweet cherries." | no (historical description, not a recommendation; host not catalogued) |
| https://yardandgarden.extension.iastate.edu/article/2008/2-6/Cherries.html | iastate_ext | rule only: "Spacing between trees should be equal to their approximate mature height. For example, if the trees are expected to reach 15 feet tall, they should be spaced 15 feet apart." | no (rule, no crop figure) |
| https://extension.illinois.edu/tree-fruits/cherries | uiuc_ext | no between-tree spacing (only scaffold spacing) | no |
| https://cmg.extension.colostate.edu/wp-content/uploads/sites/59/2020/01/GN-770-Tree-Fruits.pdf (GardenNotes 771 inside) | csu_ext (extension.colostate.edu subdomain) | Table 1 "Typical Size of Fruit Trees": Sour Cherry Standard "18-24 feet" Typical Spread (Pruned) | no (mature spread, not a spacing) |
| https://ucanr.edu/sites/MGWTest/Gardening/Fruits_&_Nuts/Cherries/ (from homeorchard.ucanr.edu redirect) | ucanr_ext | HTTP 404 | no |
| https://ucanr.edu/site/uc-marin-master-gardeners/document/cherry | ucanr_ext | HTTP 403 | no |
| Already checked (worklist): ISU growing-cherries-home-garden (rule only), NCSU handbook Table 15-5 (no cherry row), WSU western-WA handbook, WSU cherry-rootstocks | -- | no number | no |
Best page (if FOUND): https://extension.illinois.edu/fruit-trees/planting, uiuc_ext, row `Sour Cherry: Montmorency | Seedling (standard) | 14 x 22 to 20 x 26` with the key "the trees are planted 10 feet apart in the row with the rows 16 feet apart" -> between plants [168,240] inches (Montmorency, the standard tart cherry); between rows [264,312]; Meteor [120,144] / North Star [96,120] are smaller-variety rows. Scope note: home-garden page ("Fruit Trees for Home Gardens"), names sour cherry explicitly by variety. Corroboration: UNH "Plant plum, apricot, and cherry trees 15 to 20 feet apart in the home orchard." -> [180,240]. Judgment call: UIUC is a table (cells quoted separately) and variety-keyed; UNH is a prose sentence but a stone-fruit group sentence. Either supports a narrower band than today's [180,300]; the 300 upper bound has no page.

## cherry-sweet  (today: [180,300]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://extension.illinois.edu/fruit-trees/planting | uiuc_ext | table "Recommended tree spacing" (`Spacing in Feet`) row: `Sweet Cherry | Seedling (standard) | 20 x 26`; key sentence as above | YES |
| https://extension.unh.edu/resource/growing-fruits-growing-plums-cherries-and-apricots-nh-home-orchards-fact-sheet | unh_ext | "Plant plum, apricot, and cherry trees 15 to 20 feet apart in the home orchard."; names the crop: "On warmer sites in the southern part of the state, the sweet cherry varieties Black Gold, Sam, Lapins, and Hedelfingen are good choices." | YES (group sentence; page names sweet cherries) |
| https://extension.umaine.edu/fruit/growing-fruit-trees-in-maine/spacing/ | umaine_ext | "semi-dwarf trees about 15 feet, and standard or full-sized trees about 25 feet. Pears and non-dwarf sweet cherries are larger than other types of fruit trees, and should be given an additional 5 feet." (-> 30 ft standard sweet cherry) | YES (home orchard spacing page naming sweet cherries; figure requires adding two sentences) |
| https://ag.purdue.edu/department/hla/extension/extension-publications-library/ext-pubs/ho-9-w.html | not catalogued | "Tree spacing was 20-24 feet apart for tart cherries and 25-30 feet apart for sweet cherries." (prefaced by "Traditionally") | no (historical, not catalogued) |
| https://extension.umn.edu/fruit/growing-stone-fruits-home-garden | umn_ext | "Space trees 12 to 20 feet apart." but sweet cherry is named only as a parent of Mesabi ("Mesabi is a cross between a sweet and tart cherry") | no (does not grow/name sweet cherry as a crop) |
| https://cmg.extension.colostate.edu/wp-content/uploads/sites/59/2020/01/GN-770-Tree-Fruits.pdf | csu_ext | Table 1 Sweet Cherry Standard "30 feet" Typical Spread (Pruned) | no (spread) |
| Already checked (worklist): as cherry-sour plus OSU PNW-619 (commercial 15x20 by rootstock class) | -- | commercial | no |
Best page (if FOUND): https://extension.unh.edu/resource/growing-fruits-growing-plums-cherries-and-apricots-nh-home-orchards-fact-sheet, unh_ext, "Plant plum, apricot, and cherry trees 15 to 20 feet apart in the home orchard." -> [180,240] inches; between rows: none; scope note: home-orchard fact sheet that names sweet cherry varieties. Alternatives: UIUC `Sweet Cherry | Seedling (standard) | 20 x 26` -> 240 in-row / 312 rows (single value); UMaine 25 + 5 = 30 ft (360). Judgment call: three catalogued home pages give 15-20, 20, and 30 ft; today's [180,300] is a blend no single page states. Flag for the orchestrator: pick UNH [180,240] (one sentence) or widen to [180,360] across pages.

## pomegranate  (today: [120,180]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://edis.ifas.ufl.edu/publication/MG056 (301 -> https://ask.ifas.ufl.edu/publication/MG056) | uf_ifas_edis / ufifas_ext | HS44/MG056 "The Pomegranate", section "Planting and Spacing": "The spacing of 10–16 ft (3–5 m) between plants and 13–20 ft (4‒6 m) between rows are used for orchards, and similar spacing should be maintained for dooryard trees." and "When used as a hedge, plants are spaced 6–9 ft (2–3 m) apart. Suckers will fill spaces and produce a compact hedge." | YES ("dooryard trees" = home planting; the sentence recommends the orchard spacing for them) |
| https://hgic.clemson.edu/factsheet/pomegranate/ | clemson_hgic | no spacing statement (size "12 to 20 ft tall and wide" only; home framing) | no |
| https://gardeningsolutions.ifas.ufl.edu/plants/edibles/fruits/pomegranate/ | uf_ifas_gs (gardeningsolutions.ifas.ufl.edu) | no spacing statement | no |
| https://extension.unr.edu/publication.aspx?PubID=3809 | unr_ext | "Growing Pomegranates in Southern Nevada": "After cuttings are rooted (usually 8-16 weeks), they can be planted as individual landscaping shrubs or in rows eight to ten feet apart for fruit production or wind breaks." | marginal (ambiguous whether 8-10 ft is between plants or between rows; home framing) |
| https://ucanr.edu/sites/MGWTest/Gardening/Fruits_&_Nuts/Pomegranate/ (homeorchard.ucanr.edu redirect) | ucanr_ext | HTTP 403 | no |
| https://jackson.agrilife.org/files/2020/05/Pomegranates.pdf | not catalogued (county host; redirects to agrilifeextension.tamu.edu/counties/jackson-county/, PDF gone) | not readable | no |
| Already checked (worklist): UGA C997 (orchard 18x18; 10x15 "is not a currently recommended strategy"), NCSU toolbox, UCCE Central Sierra (height), TAMU cached shells | -- | commercial / none | no |
Best page (if FOUND): https://edis.ifas.ufl.edu/publication/MG056, uf_ifas_edis, "The spacing of 10–16 ft (3–5 m) between plants and 13–20 ft (4‒6 m) between rows are used for orchards, and similar spacing should be maintained for dooryard trees." -> [120,192] inches; between rows "13–20 ft" -> [156,240]; hedge alternative "6–9 ft" -> [72,108]. Scope note: names pomegranate; "dooryard" is UF's home-planting register. Note the quote carries an en dash in "10–16 ft" and a figure dash in "(4‒6 m)"; re-fetch must preserve those bytes. Today's [120,180] upper bound (15 ft) is not what this page says (16 ft); UGA C997 explicitly disowns 10x15.

## sweet-pea  (today: [3,6]; hunt reason: W5)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://extension.oregonstate.edu/news/old-fashioned-sweet-peas-fill-garden-fragrance | osu_ext | "Sweet peas add color and fragrance to Oregon gardens" (Kym Pokorny, OSU Extension news, Mar 2025): "Sow seeds ¾–1 inch deep and 2 inches apart. Soaking seeds for 24 hours before planting can improve germination. Thin seedlings to 5–6 inches apart." | YES (home-garden sow-and-thin distances along a row; names sweet peas) |
| https://extension.psu.edu/sowing-annual-seeds | psu_ext | Table 1 row: `Lathyrus odoratus (bush type) | sweet pea | 6–8` ("Spacing (in inches)") | YES (table row; bush-type qualifier) |
| https://hgic.clemson.edu/factsheet/sweet-pea/ | clemson_hgic | HTTP 404 (no Clemson HGIC sweet pea factsheet found by site search either) | no |
| https://hort.extension.wisc.edu/articles/sweet-pea-lathyrus-odoratus/ | uwi_hort | HTTP 404 (site search finds no UWisc sweet pea article) | no |
| https://extension.oregonstate.edu/news/fragrant-sweet-peas-please-gardener-more-bee | osu_ext | HTTP 403 | no |
| https://ucanr.edu/blog/napa-master-gardener-column/article/sweet-peas | ucanr_ext | HTTP 403 | no |
| Already checked (worklist): Cornell high tunnel (trellis density), NCSU lathyrus-odoratus (width only), UC IPM, TAMU disease handbook | -- | trellis / none | no |
Best page (if FOUND): https://extension.oregonstate.edu/news/old-fashioned-sweet-peas-fill-garden-fragrance, osu_ext, between-plants: "Thin seedlings to 5–6 inches apart." -> [5,6] inches (sow distance "Sow seeds ¾–1 inch deep and 2 inches apart." -> 2); between rows: none; scope note: names sweet peas, Oregon home gardens, OSU Extension news feature (not a numbered publication). PSU table gives [6,8] for bush type. Judgment call: OSU is a news-format Extension article; if that format is not admissible, PSU's table row [6,8] is the fallback. Today's lower bound 3 has no page; today's [3,6] overlaps the OSU thin-to figure only at 5-6.

## dry-bean  (today: [2,4]; hunt reason: W3)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://wpcdn.web.wsu.edu/extension/uploads/sites/25/FS135E-Growing-dry-bean-in-home-garden-publication.pdf | wsu_ext (WSU Extension fact sheet FS135E; served from WSU's CDN host, not extension.wsu.edu itself) | "Vegetables: Growing Dry Beans in Home Gardens" (WSU Extension Fact Sheet FS135E), Crop at a Glance: "Spacing: Plant seeds 2–3 inches apart in rows spaced 2–3 feet apart"; table "Planting Guide for Bush and Pole Beans": Bush `In-row Spacing (inches) 2–3`, `Between Row Spacing (inches) 18–30`; Pole `4–6`, `36–48` | YES (crop-specific home-garden sheet) |
| https://extension.usu.edu/yardandgarden/research/beans-in-the-garden | usu_ext | "space rows 18-24 inches apart and plant seeds 1 inch deep and 2-3 inches apart in the row." and glance: "Plant seeds 1 inch deep, spaced 2-3 inches apart, in rows 18-24 inches wide."; names the crop: "For dry beans delay harvest until pods are yellow and dry." / "With dry beans expect about 20-25 lbs. of seed per 100 feet of row." | YES (group page that names dry beans) |
| https://extension.umn.edu/vegetables/growing-beans | umn_ext | "Sow bush bean seed in single or double rows, with seeds four inches apart and rows two to three feet apart."; names the crop: "Dry beans are ready for harvest when the pods and seeds have completely dried." | YES (group page naming dry beans; 4 in) |
| https://extension.umd.edu/resource/growing-beans-home-garden | umd_ext | spacing rows are labelled by type: `Bush snap 2" - 4" in-row x 24" - 30" between rows`; dry beans named only for harvest: "For dry beans (of all types), pods should remain on the bush until dry and brown." | no (the spacing row is labelled snap) |
| https://secure.caes.uga.edu/extension/publications/files/html/b577/b577plantingchart.pdf | uga_b577 | rows `Bean, bush ... 3 ft 2 to 4 in.`, `Bean, pole ... 3 ft 6 to 12 in.`, `Bean, lima ... 2–2½ ft 3 to 4 in.`; no dry-bean row | no (no row names dry beans) |
| Already checked (worklist): Clemson snap beans, UIUC snap-beans, UF VH021, NMSU CR457 (no spacing in dry section), UC Davis 80592 (commercial), MSU beans.pdf, UGA C963 | -- | snap / commercial | no |
Best page (if FOUND): https://wpcdn.web.wsu.edu/extension/uploads/sites/25/FS135E-Growing-dry-bean-in-home-garden-publication.pdf, wsu_ext, "Spacing: Plant seeds 2–3 inches apart in rows spaced 2–3 feet apart" -> [2,3] inches (bush; pole 4–6); between rows "18–30" inches (table) / "2–3 feet" -> [24,36]; scope note: dry-bean-specific, WSU Extension Home Garden Series. Judgment call: the host is wpcdn.web.wsu.edu, the CDN behind extension.wsu.edu; if that host is not accepted, USU beans-in-the-garden (usu_ext, exact host) gives the same [2,3] with rows 18-24 in and names dry beans. Today's [2,4] upper bound 4 is supported only by UMN's generic "four inches apart".

## field-corn  (today: [8,12]; hunt reason: W3)
Verdict: FOUND (judgment call; see below)
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://hgic.clemson.edu/homegrown-grits/ | clemson_hgic | "Homegrown Grits" (dent corn for grits, home garden): "smaller plantings may blow over more easily in a storm unless spaced a little further apart (2 ft) and hilled with soil." then "Otherwise, the planting dates, fertility, pests, and other cultural aspects are very similar to sweet corn. For more information, see HGIC 1308, Sweet Corn." | marginal-YES (names dent corn; 2 ft is a conditional between-plants recommendation for small home plantings; otherwise defers to sweet corn) |
| https://secure.caes.uga.edu/extension/publications/files/html/b577/b577plantingchart.pdf | uga_b577 | "Home Garden Planting Chart", row: `Corn | 80–100 | Mar. 15–June 1 | June 1–July 20 | ¼ lb. | 3–3½ ft | 12–18 in. | 2 in.` (columns "Distance between rows", "Distance between plants"); the label is "Corn" with no "sweet" qualifier anywhere on the chart | judgment (generic "Corn"; does not name field/dent corn, does not say sweet) |
| https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-ornamental-corn | iastate_ext | "Space seeds 8 to 10 inches apart within rows for small-eared cultivars and 10 to 12 inches apart for large-eared cultivars." / "Rows should be spaced 30 to 36 inches apart."; field corn named only for isolation: "Isolate ornamental corn from sweet corn and field corn to prevent cross-pollination." | no (ornamental corn, a different crop; field corn named only as a pollen source) |
| https://extension.umn.edu/vegetables/growing-popcorn | umn_ext | "Space the seeds about 8 inches apart." / "Plant in at least four rows, with 18 to 24 inches between rows."; field corn named only for isolation | no (popcorn) |
| https://www.canr.msu.edu/resources/how_to_grow_corn | msu_ext | fetched blank (no content returned, twice) | no (unreadable) |
| https://www.canr.msu.edu/uploads/files/corn.pdf | msu_ext | fetched blank | no (unreadable) |
| https://utia.tennessee.edu/publications/wp-content/uploads/sites/269/2023/10/D61.pdf | not catalogued | HTTP 404 | no |
| https://mastergardener.extension.wisc.edu/files/2015/12/IndianCorn.pdf | uwi_hort (sibling host) | HTTP 404 | no |
| Already checked (worklist): ISU sweet corn, UMN growing-sweet-corn, NCSU organic sweet corn (commercial) | -- | sweet corn | no |
Best page (if FOUND): two candidates, neither clean. (a) https://hgic.clemson.edu/homegrown-grits/, clemson_hgic, "smaller plantings may blow over more easily in a storm unless spaced a little further apart (2 ft) and hilled with soil." -> 24 inches (single value, conditional, names dent corn, home garden); rows: none. (b) https://secure.caes.uga.edu/extension/publications/files/html/b577/b577plantingchart.pdf, uga_b577, row `Corn | ... | 3–3½ ft | 12–18 in.` -> [12,18] between plants, rows [36,42]; label is the unqualified "Corn" on a home-garden chart (80–100 days to maturity, which reads more like dent than sweet, but the chart never says). Judgment call for the orchestrator: no catalogued page gives a field/dent-corn between-plants RANGE that names the crop; Clemson's "(2 ft)" is the only figure that names dent corn. Today's [8,12] is a sweet-corn figure on every page that carries it. If neither candidate is accepted, treat as NOT FOUND -> R5 waiver.

## nectarine  (today: [216,240]; hunt reason: W3)
Verdict: FOUND
Pages tried:
| url | catalog id (or "not catalogued") | states (verbatim quote or "no spacing statement") | counts? |
| -- | -- | -- | -- |
| https://extension.unh.edu/sites/default/files/migrated_unmanaged_files/Resource000586_Rep608.pdf | unh_ext | "Growing Peaches and Nectarines in the Home Garden" (UNH Cooperative Extension, William Lord and Amy Ouellette, revised November 2013): "Plant trees before their buds break. Plant peach and nectarine trees 12 to 15 feet apart." | YES (sentence names nectarine; home garden) |
| https://extension.illinois.edu/fruit-trees/planting | uiuc_ext | table "Recommended tree spacing" (`Spacing in Feet`): `Peach, Apricot. Nectarine, Plum | Seedling (standard) | 14 x 20 to 20 x 28` and `Peach, Apricot. Nectarine, Plum | St. Julian A (dwarf) | 8 x 16 to 12 x 18`; key: "the trees are planted 10 feet apart in the row with the rows 16 feet apart." | YES (names nectarine in the row label; home-garden page) |
| https://hgic.clemson.edu/factsheet/peaches-nectarines/ | clemson_hgic | VERIFIED on live page: no between-tree spacing statement. Names the crop: "Nectarines are nothing more than fuzzless peaches, and their culture is the same as peaches." | no (verified) |
| https://extension.missouri.edu/publications/g6030 | mu_ext | "Home Fruit Production: Peach and Nectarine Culture": no tree spacing statement (only fruit thinning "about 8 inches apart") | no |
| https://cmg.extension.colostate.edu/wp-content/uploads/sites/59/2020/01/GN-770-Tree-Fruits.pdf (GardenNotes 771) | csu_ext | Table 1 "Typical Size of Fruit Trees": Peach and Nectarine Standard "20 feet" Typical Spread (Pruned), Dwarf "8-10 feet" | no (mature spread, not a spacing) |
| https://ucanr.edu/sites/MGWTest/Gardening/Fruits_&_Nuts/Nectarine/ (homeorchard.ucanr.edu redirect) | ucanr_ext | HTTP 403 (search snippet claimed "8 to 12 feet apart"; unverifiable) | no |
| https://ucanr.edu/node/133881 | ucanr_ext | HTTP 403 | no |
| https://edis.ifas.ufl.edu/publication/HS1459 and MG374 | uf_ifas_edis | both 301 to ask.ifas.ufl.edu; not re-fetched after the redirect (budget); crop already cites them and the worklist read them without a nectarine spacing sentence | not re-read |
| Already checked (worklist): UGA C1063 peaches (18-20 ft; nectarine only in a guide title), NCSU Table 15-5 "Peaches 18-20", USU peaches (12-16 ft by rootstock) | -- | sibling (peach) | no |
Best page (if FOUND): https://extension.unh.edu/sites/default/files/migrated_unmanaged_files/Resource000586_Rep608.pdf, unh_ext, "Plant peach and nectarine trees 12 to 15 feet apart." -> [144,180] inches; between rows: none; scope note: the sentence itself names nectarine; home-garden fact sheet (PDF). Corroboration: UIUC table `14 x 20 to 20 x 28` -> in-row [168,240], rows [240,336], row label names nectarine. Today's [216,240] (UGA peaches 18-20 ft) is not what either nectarine-naming page says; the two pages span 12-20 ft, so [144,240] is the widest page-backed band.

## Summary

| crop | verdict | figure (inches, between plants) | page |
| -- | -- | -- | -- |
| cosmos | FOUND | [12,18] (USU species page: [12,24]) | UF/IFAS EDIS FP149 (uf_ifas_edis) |
| sweet-alyssum | FOUND | [8,10] | PSU "Sowing Annual Seeds" Table 1 (psu_ext) |
| echinacea | FOUND | [18,24] | UF/IFAS EDIS FP192 (uf_ifas_edis) |
| cherry-sour | FOUND | [168,240] (Montmorency; UNH group sentence [180,240]) | UIUC fruit-trees/planting table (uiuc_ext); UNH home orchards (unh_ext) |
| cherry-sweet | FOUND | [180,240] (UIUC 240; UMaine 360) | UNH home orchards (unh_ext) |
| pomegranate | FOUND | [120,192] (hedge [72,108]); rows [156,240] | UF/IFAS EDIS MG056 (uf_ifas_edis) |
| sweet-pea | FOUND | thin to [5,6], sow at 2 (PSU bush type [6,8]) | OSU Extension news "Sweet peas add color and fragrance to Oregon gardens" (osu_ext) |
| dry-bean | FOUND | [2,3] bush (pole [4,6]); rows [18,30] | WSU FS135E (wsu_ext, CDN host); USU beans-in-the-garden (usu_ext) same figure |
| field-corn | FOUND (judgment) | 24 (Clemson dent corn, conditional) or [12,18] (UGA B577 unqualified "Corn") | Clemson HGIC homegrown-grits (clemson_hgic); UGA B577 chart (uga_b577) |
| nectarine | FOUND | [144,180] (UIUC table [168,240]) | UNH "Growing Peaches and Nectarines in the Home Garden" (unh_ext) |


## Found pages, as staged (main session, 2026-10-01)

Each found page is on a publisher ALREADY in `source_catalog` (a catalogued publisher cited at a new URL, which the entry's
`anchoring_urls` carries; no new source is admitted, so nothing here is a PLA-532-style admission). The promote's guard 2
checks the same thing (`source {id} is not in source_catalog` refuses). field-corn's result is recorded above for session 3.

| crop | hunt | verdict | catalog id | catalog name | in catalog | page | in_row (in) |
| -- | -- | -- | -- | -- | -- | -- | -- |
| cosmos | W5 | FOUND | `usu_ext` | Utah State University Extension | YES | https://extension.usu.edu/yardandgarden/research/cosmos-in-the-garden | [12, 24] |
| sweet-alyssum | W5 | FOUND | `psu_ext` | Penn State Extension | YES | https://extension.psu.edu/sowing-annual-seeds | [8, 10] |
| echinacea | W5 | FOUND | `uf_ifas_edis` | UF/IFAS EDIS (Electronic Data Information Source) | YES | https://edis.ifas.ufl.edu/publication/FP192 | [18, 24] |
| cherry-sour | W5 | FOUND | `unh_ext` | University of New Hampshire Cooperative Extension | YES | https://extension.unh.edu/resource/growing-fruits-growing-plums-cherries-and-apricots-nh-home-orchards-fact-sheet | [180, 240] |
| pomegranate | W5 | FOUND | `uf_ifas_edis` | UF/IFAS EDIS (Electronic Data Information Source) | YES | https://edis.ifas.ufl.edu/publication/MG056 | [120, 192] |
| sweet-pea | W5 | FOUND | `osu_ext` | Oregon State University Extension | YES | https://extension.oregonstate.edu/news/old-fashioned-sweet-peas-fill-garden-fragrance | [5, 6] |
| cherry-sweet | W5 | FOUND | `unh_ext` | University of New Hampshire Cooperative Extension | YES | https://extension.unh.edu/resource/growing-fruits-growing-plums-cherries-and-apricots-nh-home-orchards-fact-sheet | [180, 240] |
| dry-bean | W3 | FOUND | `usu_ext` | Utah State University Extension | YES | https://extension.usu.edu/yardandgarden/research/beans-in-the-garden | [2, 3] |
| nectarine | W3 | FOUND | `unh_ext` | University of New Hampshire Cooperative Extension | YES | https://extension.unh.edu/sites/default/files/migrated_unmanaged_files/Resource000586_Rep608.pdf | [144, 180] |

R5 migration waiver candidates from session 2: NONE. `planting_layout_migration_known.WAIVERS` stays empty.
