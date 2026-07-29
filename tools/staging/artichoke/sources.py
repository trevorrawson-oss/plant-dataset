#!/usr/bin/env python3
"""Artichoke GS arc -- source_catalog additions + the per-cell anchoring URLs.

R3/R4 DISCIPLINE, operationalized. `citable_for` records WHAT THE DOCUMENT IS, not just who
hosts it, because a .edu host is not a tier. Four load-bearing documents for this crop are
withdrawn, moved, or dead, and each carries its real resolving anchor here rather than a
plausible-looking live URL that 404s or silently serves different content:

  vce_438_108        withdrawn from the live VCE site -> VTechWorks ORIGINAL-bundle bitstream
                     (the DSpace DEFAULT bitstream URL returns a JPEG THUMBNAIL, not the PDF)
  rutgers_fs044      live PDF returns "Missing File" -> landing page + Wayback copy
  uf_ifas_hs1289     live EDIS page is HTTP 410 GONE -> EDIS journal archive PDF, "Archival copy"
  ucd_postharvest    live sheet 403s -> Wayback capture

DELIBERATELY NOT CATALOGUED, and why (each was consulted and rejected):
  - UC Master Gardener statewide "Artichokes" page: UNATTRIBUTED (no author, no pub number, no
    citation). Sole source of the "summer dormancy" framing, and asserts "Zones: 3-11" which is
    incompatible with a 15F crown kill. Two independent research agents rejected it.
  - UC IPM's home-garden PLANTING TABLE: a degraded copy of Master Gardener Handbook Table 13.2 --
    drops BOTH organ notes and changes Desert Valleys from Sept to July. uc_ipm stays catalogued
    and is cited for IPM ladders and cultural tips ONLY, never for a district planting window.
  - NC State Plant Toolbox: an aggregated plant-database entry, not a bulletin.
  - blogs.cornell.edu/fruition: SEED-COMPANY content on a .edu host.
  - Pima County AZ January guide: volunteer Master Gardener authored.
  - UW-Extension A2801: live but OBSOLETE ("globe artichoke ... is not grown in Wisconsin"),
    (c)1994, predates the annual-type cultivars, contradicted by UW's own research station.

WRONGLY REJECTED, THEN RESTORED (2026-07-27, corrected in this file 2026-07-28):
  - unlv_mg_svn -- the Southern Nevada Master Gardener planting guide. A research agent reported it
    as failing the tier bar ("volunteer-authored"), I relayed that without checking, dropped the
    citation, derived a window in its place, and published the false claim that University of Nevada
    Extension does not recommend artichoke. It is `tier: T1`, `source_class:
    extension_master_gardener_program`, ADMITTED 2026-07-21 explicitly to "back the nevada per-crop
    annual windows", and is cited by 67 other crops. The catalog had already ruled; the agent
    applied a stricter bar than the dataset's own recorded admission decision. See
    docs/2026-07-27-source-tier-model-kickoff.md section 2. THE RULE: check `source_catalog` BEFORE
    accepting any agent's tier rejection.
    Re-verified at source 2026-07-28 before re-anchoring. The chart's marks are DRAWN BARS with no
    text layer (the R9 hazard), so the artichoke row was recovered from PDF rectangle geometry and
    validated against known rows: garlic reads Sept through early Oct and broccoli reads Feb plus
    Aug-Oct, both matching the catalog entry's own description of the chart. Artichoke reads
    early-Feb through late-Mar with NO fall window, which is exactly what the nevada cells claim
    and is the unusual part worth citing -- every other cool-season crop on the chart gets two.

DROPPED AT URL VERIFICATION (2026-07-26) -- the R4 check earning its keep a second time:
  - lsu_agcenter_3634 -- DROPPED, THEN RESTORED 2026-07-26. The first draft carried a CONSTRUCTED
    address (/profiles/lbenedict/...) which 404'd -- precisely the self-constructed-404 failure the
    asparagus arc caught -- so the citation was removed and se_gulf fell back to derivation. Trevor
    then supplied the real address (/profiles/bneely/...), which resolves 200 with the title
    "Vegetable Gardening Tips: Artichokes", and both load-bearing sentences were re-confirmed
    present in the fetched body before re-citing. The agent's quotes were accurate all along; only
    my address was wrong. se_gulf z8/z9 are sourced again.
  - calag_1992_artichoke (California Agriculture 46(4):28-29). The calag archive URL 404s in every
    form tried, and the agent itself recovered the text only from a third-party mirror. The
    southern-California and desert windows it supports are independently carried by uc_mg_t132,
    uc_anr_7221 and ucce_imperial_artichoke, so dropping it costs nothing.

FETCH CAVEAT, not a resolution failure: tamu_agrilife (the specialty-crops brief) returns 403 to
urllib but resolves normally via a browser-class fetch, which returned its quotes verbatim. That is
a bot block, not a dead link, and it is cited.
"""

CATALOG_ADDITIONS = {
    "vce_438_108": {
        "id": "vce_438_108",
        "name": "VCE Publication 438-108, Specialty Crop Profile: Globe Artichoke (Bratsch, 2009)",
        "publisher": "Virginia Cooperative Extension / Virginia Tech",
        "url": "https://vtechworks.lib.vt.edu/server/api/core/bitstreams/"
               "bbdb933c-3d6e-49f0-94fc-28c141601776/content",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension SPECIALTY-CROP PRODUCTION PROFILE, 9 pp, Virginia Tech, reporting the "
            "author's own Blacksburg field trials. The mid-Atlantic annual-culture system: "
            "transplants set late March through April; post-transplant field vernalization of "
            "190-240 hours at or below 50F; bud production commencing 60 to 100 days after "
            "transplanting; harvest peak mid-August through September; measured overwintering "
            "survival of 30-40% under hooped vented plastic plus a floating row cover, with few "
            "plants surviving under straw, a single cover, or plastic alone; 15-25% barren "
            "first-year plants. WITHDRAWN from the live VCE site (pubs.ext.vt.edu returns 'This "
            "publication is no longer available on our website'); this URL is the VTechWorks "
            "ORIGINAL-bundle bitstream. Do NOT use the DSpace default bitstream URL, which "
            "returns a JPEG thumbnail."),
    },
    "uc_anr_7221": {
        "id": "uc_anr_7221",
        "name": "UC ANR Publication 7221, Artichoke Production in California",
        "publisher": "University of California Agriculture and Natural Resources",
        "url": "https://ucanr.edu/sites/default/files/2026-04/"
               "anrcatalog%20Artichoke%20Production%20in%20California%207221.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "ANONYMOUSLY PEER-REVIEWED extension commercial production bulletin (colophon: "
            "'anonymously peer reviewed for technical accuracy by University of California "
            "scientists'), UC Vegetable Production Series. The strongest artichoke source "
            "available. California district systems: central-coast perennials harvested year-round "
            "with peak March-April; annuals elsewhere; desert plantings August-October for "
            "December-April harvest; the cut-back cropping lever (mid-April to mid-June for fall/ "
            "winter/spring harvest, late August or September for summer); stumping at 3-4 week "
            "intervals; replanting every 5 to 10 years; perennial propagation by crown division "
            "with rooted 'stumps' in trenches 4-6 inches deep; growth optimum 75F days / 55F "
            "nights within a 45-85F range; tolerance above 86F with reduced bud quality; frost "
            "blistering the outer bracts while mature plants usually survive. NOTE: contains ZERO "
            "occurrences of vernalization, chill, dormancy or photoperiod in either edition -- do "
            "NOT cite it for a chill mechanism."),
    },
    "uc_mg_t132": {
        "id": "uc_mg_t132",
        "name": "UC Master Gardener Program, Time of Planting (California Master Gardener "
                "Handbook Table 13.2)",
        "publisher": "University of California Agriculture and Natural Resources",
        "url": "https://ucanr.edu/program/uc-master-gardener-program/time-planting",
        "source_class": "university_extension",
        "trust_tier": "medium",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "The statewide four-district home-garden planting table, reproducing California Master "
            "Gardener Handbook Table 13.2 (ANR Publication 3382). Artichoke district windows: "
            "North & North Coast (Monterey County north) Aug-Dec; South Coast (San Luis Obispo "
            "County south) May-July; Interior Valleys (Sacramento, San Joaquin) July; Desert "
            "Valleys (Imperial & Coachella) Sept. LOAD-BEARING ORGAN NOTE: the table's default is "
            "'Planting dates are for seed unless noted otherwise' and artichoke carries the "
            "asterisk overriding it -- 'Transplants, shoots, or roots are used for field "
            "planting'. PROVENANCE CAVEAT, surfaced not laundered: the table states its own "
            "lineage as 'Adapted from Vegetable Gardening Illustrated 1994' -- republished inside "
            "a peer-reviewed UC ANR handbook but NOT original UC field research, hence trust_tier "
            "medium. PREFER THIS over the UC IPM copy of the same table, which drops both organ "
            "notes and changes the Desert Valleys month."),
    },
    "ucce_imperial_artichoke": {
        "id": "ucce_imperial_artichoke",
        "name": "UCCE Imperial County Circular 104-V, Sample Cost to Establish and Produce "
                "Artichokes (Mayberry, 2000)",
        "publisher": "University of California Cooperative Extension, Imperial County",
        "url": "https://coststudyfiles.ucdavis.edu/uploads/cs_public/92/a8/"
               "92a8b901-3171-4114-956e-bb4fa624a95b/artichokes.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Farm-advisor-authored crop-culture guideline and cost study for the low desert. "
            "Fields planted late August or early September; 'Desert-grown artichokes are "
            "direct-seeded or grown from transplants. Few, if any, are grown from mother plant "
            "cuttings, a practice commonly used in coastal California'; and the season-ending "
            "heat statement, 'desert-grown chokes will seldom be marketable after early April'."),
    },
    "umaine_2075": {
        "id": "umaine_2075",
        "name": "UMaine Extension Bulletin #2075, Growing Globe Artichokes (Cynara scolymus L.) "
                "in Maine (Hutton & Ginakes)",
        "publisher": "University of Maine Cooperative Extension",
        "url": "https://extension.umaine.edu/publications/2075e/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension crop bulletin for cold-region ANNUAL culture. Controlled vernalization of "
            "seedling trays below 50F for a minimum of 3 weeks (roughly 500 hours) with 12-13 "
            "hours of light; the 4-6 true-leaf stage at 6-8 weeks; devernalization above 80F; "
            "10-20 buds per plant with the majority under 3 inches; and the statement that in "
            "Maine artichokes are grown as annuals from transplants because they are not "
            "cold-hardy enough to survive Maine winters reliably. Also the sole source of the "
            "container-overwintering method (32-35F, dark). Its 'hardy in USDA Zone 7 and "
            "greater' claim CONFLICTS with Cornell (zone 6/5) and with the measured 15F crown "
            "kill -- see the crop's open_findings; do not cite it for a zone floor."),
    },
    "umaine_highmoor": {
        "id": "umaine_highmoor",
        "name": "UMaine Extension Highmoor Farm, Artichokes for the Northeast research reports "
                "(2021, 2022, 2023) and Ginakes, Hutton & Handley 2024 HortTechnology 34(6):819-826",
        "publisher": "University of Maine Cooperative Extension / American Society for "
                     "Horticultural Science",
        "url": "https://extension.umaine.edu/highmoor/resources-by-crop/artichoke/northeast-2023/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Replicated multi-year extension field trials at Monmouth, Maine, and their "
            "PEER-REVIEWED write-up. Measured operation dates: seeding in the last third of "
            "March, transplanting 24 May to 12 June (63-80 days of seedling production), first "
            "harvest 14-29 August, final harvest 1-12 October. Measured days-after-transplanting "
            "to harvest: 88 / 83 / 63 by year, and 76-94 across eight cultivars. The vernalization "
            "dose-response that anchors the ~500-hour recommendation: 303 hours without "
            "supplemental light gave 3-33% flowering, 550 hours with light gave 68-100%. "
            "DO NOT USE the 2021 report's 'Days to Maturity' column (75/75/85/88/90) -- it states "
            "no basis, matches seed-catalog copy, and is contradicted by the trials' own 2022 "
            "measurements."),
    },
    "umass_nevmg": {
        "id": "umass_nevmg",
        "name": "New England Vegetable Management Guide, Globe Artichoke",
        "publisher": "UMass Amherst Extension and the New England land-grant universities",
        "url": "https://nevegetable.org/crops/globe-artichoke",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Regional multi-state extension commercial vegetable management guide. Vernalization "
            "at 35-50F for at least 10 days in a cooler, with 500-550 hours (about 21-32 days) "
            "greatly increasing the proportion of plants that bud; the explicit judgement that "
            "ambient field chilling is 'far less reliable than controlled vernalization in "
            "coolers'; 10-20 buds per plant of which only 2-3 are primaries; and the perennial "
            "verdict for New England, that artichokes are not cold hardy enough to survive winter "
            "reliably and must be grown annually from seed."),
    },
    "osu_oregon_veg": {
        "id": "osu_oregon_veg",
        "name": "Oregon Vegetables: Artichoke, Globe (OSU Department of Horticulture)",
        "publisher": "Oregon State University",
        "url": "https://horticulture.oregonstate.edu/oregon-vegetables/artichoke-globe",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension commercial vegetable production guide. THE SOLE SOURCE of the crown-kill "
            "threshold: 'At temperatures under 15 F severe loss of crowns would be expected even "
            "with mulch protection', alongside the 25F winter caution and straw mulching. Also "
            "the Virginia vernalization data restated (about 1300 hours under 50F to fully "
            "vernalize Green Globe and Imperial Star; 200 hours giving over 80% flowering in "
            "Imperial Star versus 25% in Green Globe; Grande Buerre and Talpiot failing to flower "
            "after 500 hours), Emerald requiring very little vernalization, the Willamette Valley "
            "recommendation to target late-summer and early-fall production, and the bud "
            "blistering that follows near-freezing temperatures. Serves 403 to WebFetch; fetch "
            "with urllib."),
    },
    "wsu_em057e": {
        "id": "wsu_em057e",
        "name": "WSU Extension EM057E, Home Vegetable Gardening in Washington (Home Garden Series)",
        "publisher": "Washington State University Extension",
        "url": "https://s3.wp.wsu.edu/uploads/sites/2071/2014/04/"
               "Home-Vegetable-Gardening-in-WA-EM057E.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Home-garden bulletin. Artichoke seeding row: planting depth 1/4-1/2 inch, 18 inches "
            "between plants, 36 inches between rows, 8-14 days to germinate, optimum soil "
            "temperature 65-82F, 6-8 weeks to transplant size. Artichoke is flagged perennial in "
            "its Table 1. CAVEATS: its 'Days to Maturity 85-120' states no basis and sits in a "
            "SEEDING table, so it is NOT usable to anchor a days-to-maturity figure; and its "
            "Table 5 season bars are a DRAWN CHART with no text layer, recovered from PDF vector "
            "geometry and cross-validated against ~30 other crops, so treat those windows as "
            "geometry-recovered rather than quoted."),
    },
    "usu_ext_artichoke": {
        "id": "usu_ext_artichoke",
        "name": "USU Extension, How to Grow Artichoke in Your Garden (Drost, April 2020)",
        "publisher": "Utah State University Extension",
        "url": "https://extension.usu.edu/yardandgarden/research/artichoke-in-the-garden",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "PEER-REVIEWED extension home-garden crop fact sheet (page states 'Peer-reviewed fact "
            "sheet'). Seed started indoors in early January, 2-3 months to transplantable size, "
            "set out 3-4 weeks before the frost-free date; germination at 70-75F; spacing 18 "
            "inches in rows 2-3 feet apart; harvest beginning late July or early August and "
            "continuing until frost; 3-5 buds per flower stalk; the cultivar split (Imperial Star "
            "excellent as an annual, Green Globe best maintained several years); heavy mulching "
            "possibly allowing overwintering in milder areas of Utah with lift-and-store in colder "
            "areas; and the failure mode, that plants often fail to flower when it is hot during "
            "flower-stalk formation. CAVEAT: the page's Summary and FAQ blocks read as later "
            "editorial additions and one contradicts the body on last-frost timing; use the body "
            "text. Its 'good disease resistance' phrase for Imperial Star NAMES NO DISEASE and is "
            "not a resistance rating."),
    },
    "tamu_eht065": {
        "id": "tamu_eht065",
        "name": "Texas A&M AgriLife EHT-065, Easy Gardening: Artichoke (Masabni & Lillard)",
        "publisher": "Texas A&M AgriLife Extension",
        "url": "https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2013/09/EHT-065.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Statewide extension home-garden single-crop fact sheet. The Texas fall-planted, "
            "summer-dormant system: seed started mid-August for a mid-October Central Texas "
            "transplant, up to 60 days to suitable size, main harvest April and May, and the "
            "cut-to-soil-level after the June harvest that puts the crown into summer dormancy "
            "with new shoots in fall. THE ONLY EXPLICIT COLD LIMIT IN THE CORPUS: 'Do not expose "
            "artichokes to temperatures below 25 degrees F in the winter', with straw, leaves, a "
            "bucket or frost blanket as protection. Also the aridity effect, that a hot dry "
            "climate causes buds to open quickly and destroys tenderness. CAVEATS: it gives NO "
            "absolute west-Texas date, only 'start seeds a few weeks earlier'; its pest photos "
            "are credited to UC Statewide IPM, so its pest list is not evidence of Texas "
            "occurrence; and a separate TAMU specialty-crops brief by the same authors gives a "
            "conflicting crown-division, Texas-coast, one-year-to-harvest account."),
    },
    "uf_ifas_hs1289": {
        "id": "uf_ifas_hs1289",
        "name": "UF/IFAS EDIS HS1289, Production Guidelines for Globe Artichoke in Florida "
                "(Agehara, 2017) -- ARCHIVED",
        "publisher": "UF/IFAS Extension",
        "url": "https://journals.flvc.org/edis/article/download/127520/127723/211706",
        "source_class": "university_extension",
        "trust_tier": "medium",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension production guideline for Florida, and the ONLY defensible basis for an "
            "`unsuitable` rating in this crop: 'plants require sufficient chilling exposure or "
            "vernalization, which is generally 250 to 500 hours of temperatures below 50F. "
            "Therefore, bud formation must be artificially induced to produce artichokes in "
            "Florida', and 'artichokes do not initiate flower-bud formation or bolting without "
            "artificial vernalization in Florida because of insufficient chilling hours'. Also "
            "the 86F bud-quality ceiling and the below-28F whole-plant caution, and the Florida "
            "annual cycle (October to May, transplants no later than mid-November, harvest early "
            "March to early May). FORMALLY ARCHIVED: the live EDIS page returns HTTP 410 Gone and "
            "this PDF is watermarked 'Archival copy: for current recommendations see "
            "http://edis.ifas.ufl.edu'. There is no current live UF/IFAS artichoke publication. "
            "Cite WITH that caveat."),
    },
    "uariz_ext_az1615": {
        "id": "uariz_ext_az1615",
        "name": "University of Arizona Extension AZ1615, Planting and Harvesting Calendar for "
                "Gardeners in Yuma County (Bealmear & Nolte, rev. 3/2020)",
        "publisher": "University of Arizona Cooperative Extension",
        "url": "https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1615-2020.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Faculty-reviewed low-desert home-garden planting and harvesting calendar for Yuma "
            "County. Artichoke planting September-October, harvest May-June. CAVEAT ON ITS OWN "
            "HEADER RULE: the calendar states 'This calendar has been made for seeds unless "
            "otherwise noted', but the same table gives asparagus an 8-inch planting depth, which "
            "is a crown depth, so the seed-unless-noted rule is demonstrably not applied "
            "perfectly to perennials in this chart."),
    },
    "lsu_agcenter_3634": {
        "id": "lsu_agcenter_3634",
        "name": "LSU AgCenter, Vegetable Gardening Tips: Artichokes",
        "publisher": "LSU AgCenter",
        "url": "https://www.lsuagcenter.com/profiles/bneely/articles/page1532008353583",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension home-garden crop guidance for the Gulf, and the only Gulf-state extension "
            "service that covers artichoke at all. Verified verbatim: 'Artichokes should be "
            "planted from October to early November'; 'If starting from seed, sow them 12 weeks "
            "before you intend to plant. For example, sow seeds in mid-July for an October "
            "planting'; 'Dig the hole as deep as the root ball and a little wider', confirming a "
            "containerized transplant rather than a bare crown; 'Space individual plants at least "
            "3 feet apart'; and the candid persistence verdict, 'Technically, artichokes are a "
            "perennial vegetable, but many times we lose them in the summer to disease... or "
            "simply treat them as an annual plant.' Also a zone claim -- 'Artichokes prefer warm "
            "temperatures and thrive in USDA Plant Hardiness Zones 7 and higher' -- which is a "
            "THRIVES statement, not a perennializes one, and which the same page contradicts two "
            "paragraphs later on summer-disease grounds. CAVEATS: LSU's flagship Louisiana "
            "Vegetable Planting Guide (Pub. 1980) omits artichoke entirely, and its P3941-A chart "
            "gives Aug 1 - Oct 31 with no organ note; Louisiana HARVEST months are not stated "
            "anywhere in T1. URL PROVENANCE: recovered by Trevor 2026-07-26 after a "
            "self-constructed address 404'd; the two load-bearing sentences were re-confirmed "
            "present at this address before citing."),
    },
    "unr_ext_fs1305": {
        "id": "unr_ext_fs1305",
        "name": "UNR Extension FS-13-05, Fruit, Flower and Seed Vegetable Varieties for the "
                "Moapa and Virgin Valleys (Bishop & Stoesser, 2013)",
        "publisher": "University of Nevada, Reno Extension",
        "url": "https://extension.unr.edu/publication.aspx?PubID=3016",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "NUMBERED UNR Extension fact sheet with named authors, scoped to the Moapa and Virgin "
            "Valleys in Clark County (Logandale, Overton, Mesquite) -- low-desert southern Nevada. "
            "It carries a dedicated Globe Artichokes section, verified verbatim: 'Globe Artichokes "
            "are a perennial plant that can be grown for both edible flower buds and showy garden "
            "flowers'; and for cultivars, 'Imperial Star will produce well-developed artichokes "
            "the first year from seed. Plants become 1 1/2-3 feet tall and have an open growth "
            "habit. Each typically produces one or two primary buds, with a diameter of 3 or 4 "
            "inches, and five to seven smaller secondary buds.' Also recommends Green Globe and "
            "Violetta. SCOPE LIMIT, load-bearing: this is a VARIETY guide, not a planting "
            "calendar -- it gives NO planting window, no harvest window and no persistence "
            "statement for Nevada, so it supports the RATING and the cultivar set, never a date. "
            "PROVENANCE: surfaced by Trevor 2026-07-27. Five research agents missed it because "
            "extension.unr.edu's search is JavaScript-rendered and they could only fetch "
            "publications by known URL, and because it is a variety guide rather than the "
            "planting-calendar class they were sweeping. It CORRECTS an earlier finding in this "
            "arc that UNR does not cover the crop."),
    },
    "rutgers_fs044": {
        "id": "rutgers_fs044",
        "name": "Rutgers NJAES FS044, Globe Artichoke Production in New Jersey "
                "(Nitzsche & Sciarappa, 2005)",
        "publisher": "Rutgers NJAES Cooperative Extension",
        "url": "https://njaes.rutgers.edu/pubs/publication.php?pid=FS044",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": "2026-07",
        "citable_for": (
            "Extension crop production fact sheet, and the source of the finding that most shapes "
            "this crop's suitability map: the NO-TREATMENT CONTROLS showing vernalization is "
            "QUANTITATIVE rather than obligate -- 'Imperial Star produced more buds (74%) with no "
            "vernalization treatment compared to Green Globe Improved (57%)', against 98% and 86% "
            "when chilled -- and the framing that vernalization PROMOTES bud initiation, with "
            "vernalized plants flowering earlier and more uniformly. Also the outlier 50-60F "
            "vernalization band (the only one whose floor sits above 50F), the explicit rejection "
            "of seed vernalization as highly variable, and field devernalization by root heat "
            "under black plastic mulch. RESOLUTION: the live PDF endpoint returns 'Missing File'; "
            "this landing page resolves and confirms the metadata, and the PDF itself was "
            "recovered from a 2010 Wayback snapshot."),
    },
    "uaex_cardoon": {
        "id": "uaex_cardoon",
        "name": "University of Arkansas Extension, Plant of the Week: Cynara cardunculus 'Cardoon' "
                "(Klingaman, 2012)",
        "publisher": "University of Arkansas System Division of Agriculture",
        "url": "https://www.uaex.uada.edu/yard-garden/resource-library/plant-week/cardoon-7-20-12.aspx",
        "source_class": "university_extension",
        "trust_tier": "low",
        "tier": "T2",
        "accessed": "2026-07",
        "citable_for": (
            "ORNAMENTAL-HORTICULTURE NEWSPAPER COLUMN by a retired extension horticulturist, NOT "
            "a vegetable production fact sheet, and the page carries a standing disclaimer: 'The "
            "University of Arkansas System Division of Agriculture does not promote, support or "
            "recommend plants featured in Plant of the Week.' It describes CARDOON, the leaf-stalk "
            "form of the same species, not var. scolymus. Admitted at T2 as the ONLY in-region "
            "overwintering observation for the mid-South, where no state extension service lists "
            "globe artichoke at all: 'reliably winter hardy only in zone 8 and south. Some "
            "references report it as hardy in zone 7, but here in Fayetteville it perhaps "
            "overwinters once in 10 years. Winter wet may be as destructive to its overwintering "
            "as the cold.' Cite ONLY for that observation, never for a planting window."),
    },
}

# Per-cell anchoring URLs: the id -> the SPECIFIC document that carries the claim. R4's operational
# rule is that truth lives here, not in the catalog id -- the asparagus failure was an anchoring URL
# pointing at a county crop report, not a wrong catalog entry.
SOURCE_URLS = {
    "vce_438_108": CATALOG_ADDITIONS["vce_438_108"]["url"],
    "uc_anr_7221": CATALOG_ADDITIONS["uc_anr_7221"]["url"],
    "uc_mg_t132": CATALOG_ADDITIONS["uc_mg_t132"]["url"],
    "ucce_imperial_artichoke": CATALOG_ADDITIONS["ucce_imperial_artichoke"]["url"],
    "umaine_2075": CATALOG_ADDITIONS["umaine_2075"]["url"],
    "umaine_highmoor": CATALOG_ADDITIONS["umaine_highmoor"]["url"],
    "umass_nevmg": CATALOG_ADDITIONS["umass_nevmg"]["url"],
    "osu_oregon_veg": CATALOG_ADDITIONS["osu_oregon_veg"]["url"],
    "wsu_em057e": CATALOG_ADDITIONS["wsu_em057e"]["url"],
    "usu_ext_artichoke": CATALOG_ADDITIONS["usu_ext_artichoke"]["url"],
    "tamu_eht065": CATALOG_ADDITIONS["tamu_eht065"]["url"],
    "uf_ifas_hs1289": CATALOG_ADDITIONS["uf_ifas_hs1289"]["url"],
    "uariz_ext_az1615": CATALOG_ADDITIONS["uariz_ext_az1615"]["url"],
    "lsu_agcenter_3634": CATALOG_ADDITIONS["lsu_agcenter_3634"]["url"],
    "unr_ext_fs1305": CATALOG_ADDITIONS["unr_ext_fs1305"]["url"],
    "rutgers_fs044": CATALOG_ADDITIONS["rutgers_fs044"]["url"],
    "uaex_cardoon": CATALOG_ADDITIONS["uaex_cardoon"]["url"],
    # already in the catalog -- pinned to the artichoke-specific document, not the umbrella host
    "uc_ipm": "https://ipm.ucanr.edu/agriculture/artichoke/",
    # the chart IS the document; there is no artichoke-specific page to pin to. Same URL the
    # catalog entry carries. Fetched 2026-07-28 (HTTP 200, application/pdf) and the artichoke row
    # read off the bar geometry -- see the header note on the rejection this reverses.
    "unlv_mg_svn": "https://www.unlv.edu/sites/default/files/page_files/27/"
                   "CampusLife_Planting-Calendar-LasVegas.pdf",
    "uariz_ext_az1005": "https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1005-2018.pdf",
    "usu_washco_dates": "https://extension.usu.edu/washington/files/planting-dates-spring.pdf",
    "uf_ifas_vh021": "https://edis.ifas.ufl.edu/publication/VH021",
    "osu_ext": "https://extension.oregonstate.edu/news/how-grow-artichokes-oregon",
    "ncsu_ext": "https://content.ces.ncsu.edu/central-north-carolina-planting-calendar-for-annual-"
                "vegetables-fruits-and-herbs",
    "cornell_ext": "https://gardening.cals.cornell.edu/garden-guidance/foodgarden/"
                   "vegetable-growing-guides/globe-artichokes-growing-guide/",
    "tamu_agrilife": "https://aggie-horticulture.tamu.edu/vegetable/guides/specialty-vegetables/"
                     "globe-artichoke/",
    "ucd_postharvest": "http://web.archive.org/web/20250207005222/"
                       "https://postharvest.ucdavis.edu/produce-facts-sheets/artichoke-globe",
}

VERIFIED = "2026-07-26"


def anchoring(ids):
    """Build an anchoring_urls block for a list of source ids."""
    out = {}
    for i in ids:
        if i in SOURCE_URLS:
            out[i] = {"url": SOURCE_URLS[i], "verified": VERIFIED}
    return out


if __name__ == "__main__":
    print(f"{len(CATALOG_ADDITIONS)} catalog additions; {len(SOURCE_URLS)} anchored ids")
    missing = [i for i in CATALOG_ADDITIONS if i not in SOURCE_URLS]
    print("additions without an anchor URL:", missing or "none")
