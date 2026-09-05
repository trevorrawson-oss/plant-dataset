# pear-european -- PLA-8 batch 26 RECORD / SOURCE PASS

Reviewer: record/source reviewer for `pear-european` only. Canonical ce98b0a6 READ-ONLY; no repo file touched except this one.
All fetches 2026-09-04. Retrieval path is stated per document. "home" / "commercial" / "toolbox-row" / "pdf" per the brief.

## Retrieval ledger (what was opened, and how)

| doc | path that worked | kind |
|---|---|---|
| UC IPM PN 7412 Codling Moth, https://ipm.ucanr.edu/home-and-landscape/codling-moth/ (Updated 05/2011) | curl 200 + WebFetch | home |
| UC IPM Pear PMG Codling Moth, https://ipm.ucanr.edu/agriculture/pear/codling-moth/ | curl 200 | commercial |
| UC IPM PN 7413 Apple and Pear Scab, https://ipm.ucanr.edu/home-and-landscape/apple-and-pear-scab/ (Updated 01/2011) | curl 200 + WebFetch | home |
| UC IPM Pear PMG "scab", https://ipm.ucanr.edu/agriculture/pear/scab/ | curl 200 but 853 chars of nav only, NO article text | stub |
| UC IPM PN 7414 Fire Blight, https://ipm.ucanr.edu/home-and-landscape/fire-blight/ (Updated 07/2011) | curl 200 | home |
| UC IPM Pear Psylla (home), https://ipm.ucanr.edu/home-and-landscape/pear-psylla/ | curl 200 | home |
| UC IPM Pear PMG Pear Psylla, https://ipm.ucanr.edu/agriculture/pear/pear-psylla/ | curl 200 | commercial |
| UC IPM Pear PMG Pear Decline, https://ipm.ucanr.edu/agriculture/pear/pear-decline/ (UC ANR 3455, text updated 11/12) | curl 200 | commercial (biology usable) |
| UC IPM Pear landing, https://ipm.ucanr.edu/home-and-landscape/pear/ | curl 200 | home (link list) |
| WSU Rootstocks for Pear, https://treefruit.wsu.edu/web-article/pear-rootstocks/ | curl 200 + WebFetch | commercial |
| WSU FS376E Pear Psylla IPM, https://treefruit.wsu.edu/crop-protection/opm/pear-psylla/ (May 2022) | curl 200 | commercial |
| WSU Pear Psylla (Burts, Riedl, Dunley 1993), https://treefruit.wsu.edu/crop-protection/opm/pear-psylla2/ | curl 200 | commercial |
| WSU Phytoplasmas and Viroids, https://treefruit.wsu.edu/web-article/phytoplasmas-and-viroids/ | curl 200 | commercial |
| WSU FS391E Fire Blight of Apple and Pear, https://treefruit.wsu.edu/crop-protection/disease-management/fire-blight/ (Dec 2024) | curl 200 | commercial |
| WSU ".../disease-management/pear-decline/" and ".../backyard-fruit-tree-spray-schedules/" | 404 (site not-found page) | dead paths |
| Clemson HGIC 2208 Fire Blight of Fruit Trees, https://hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ (Updated Jul 18, 2025) | curl 200 + WebFetch | home |
| Clemson HGIC 1352 Asian Pear, https://hgic.clemson.edu/factsheet/asian-pear/ (Jun 6, 2024) | WebFetch | home |
| Clemson HGIC 1006 Bradford Pear, https://hgic.clemson.edu/factsheet/bradford-pear/ (Jan 9, 2020) | WebFetch | home, ornamental only |
| Clemson "/factsheet/pear-diseases/", "/factsheet/pear/", "/factsheet/pear-insects/" | curl 403 (1.5 KB WAF stub); WebFetch 404 | do not exist |
| NC State "growing-pears-in-the-home-garden" (the record's anchor) | curl 404; WebFetch 404; r.jina.ai proxy: "Oops! Looks like we don't have that resource." | DEAD |
| NC State "growing-pears-in-north-carolina" | curl 403; WebFetch 403; r.jina.ai proxy: "This publication (Growing Pears in North Carolina) is no longer available." | RETIRED |
| NC State Disease and Insect Management in the Home Orchard, https://content.ces.ncsu.edu/disease-and-insect-management-in-the-home-orchard | curl 200 | home |
| NC State Extension Gardener Handbook ch. 15, https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts | curl 200 | home |
| NC State Plant Toolbox Pyrus communis, https://plants.ces.ncsu.edu/plants/pyrus-communis/ | curl 200 | toolbox-row |
| Penn State Leaf and Fruit Spot of Pear in Home Gardens, https://extension.psu.edu/leaf-and-fruit-spot-of-pear-in-home-gardens (Updated June 10, 2026) | curl 200 | home |
| Penn State "/pear-disease-fabraea-leaf-spot", "/pear-psylla", "/pear-disease-pear-decline" | 404 | dead guesses |
| MSU Fabraea leaf spot, https://www.canr.msu.edu/ipm/diseases/fabraea_leaf_spot | curl 200 but 82 chars (JS shell); WebFetch returned empty page; r.jina.ai proxy via WebFetch WORKED (twice, consistent) | commercial; PROXY READ, weaker evidence |
| UMaine Pear Fabraea leaf spot image page, https://extension.umaine.edu/ipm/ipddl/plant-disease-images/pear-fabraea/ | curl 200 | images + binomial only |
| UMass New England Tree Fruit Management Guide, Fabraea, https://netreefruit.org/pears/diseases/fabraea-leaf-spot | curl 200 | commercial; catalog key `umass_ext` is scoped "Vegetable Program", see admission notes |
| PNW Plant Disease Handbook, Pear Scab, https://pnwhandbooks.org/plantdisease/host-disease/pear-pyrus-spp-scab | curl 200 | commercial; no admissible key (see notes) |
| PNW Handbook, Pear, Asian Fabraea, https://pnwhandbooks.org/plantdisease/host-disease/pear-asian-pyrus-spp-fabraea-leaf-spot (rev. March 2026) | curl 200 | stub: photos + "See: Quince Leaf Spot" + an Asian-pear cultivar note only |
| PNW Handbook "pear-pyrus-spp-pear-decline" | 404 | dead guess |
| UGA C742 Home Garden Pears, https://fieldreport.caes.uga.edu/publications/C742/home-garden-pears/ (redirect target of extension.uga.edu ...number=C742; "published with full review on March 4, 2026") | curl 200 | home |
| UGA Plant Disease Library, Entomosporium (PDF), https://plantpath.caes.uga.edu/content/dam/caes-subsite/plant-pathology/extension-pdfs/PDL-fungi-entomosporium.pdf | curl 200 + pypdf (2 pages) | pdf |
| UAEX Home Garden Fruit Trees, https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx | curl 200 | home |
| UAEX FSA6059 Pear Production in the Home Garden, https://www.uaex.uada.edu/publications/PDF/FSA-6059.pdf | curl 200 + pypdf (6 pages) | pdf, home |
| UAEX FSA6129 Tree Fruit Cultivar Recommendations, https://www.uaex.uada.edu/publications/PDF/FSA-6129.pdf | curl 200 + pypdf | pdf, home |
| USU The Backyard Orchard, Pear Pests, https://extension.usu.edu/planthealth/research/backyard-pear-pests (Jan 2020) | curl 200 | home |
| USU IPM note Pear Psylla, https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-psylla | curl 200 | commercial note (biology usable) |
| USU IPM note Pear Decline, https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-decline | curl 200 | commercial note (biology usable) |
| UMN Growing pears in the home garden, https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-pears (redirect target of /fruit/growing-pears-home-garden) | curl 200 | home |
| OSU EC 819 Growing Tree Fruits and Nuts in the Home Orchard, https://extension.oregonstate.edu/catalog/pub/ec-819-growing-tree-fruits-nuts-home-orchard | curl 200 | home |
| OSU "/pests-weeds-diseases/insects/pear-psylla" | 404 | dead guess |
| UMD Pears, https://extension.umd.edu/resource/pears | curl 200 | link page only, no content |
| Cornell plantclinic Fabraea PDF | 404 | dead |

Direct `curl` to the `r.jina.ai` proxy is DENIED in this sandbox; proxy reads were done as WebFetch on the proxy URL.

Catalog admission notes for the hunt documents:
* `umass_ext` is admitted as "UMass Extension Vegetable Program ... New England Vegetable Management Guide". The New England Tree Fruit Management Guide (netreefruit.org, same institution) is outside that wording. Quoted below for the biology; NEEDS-CATALOG-ADMISSION (scope widening of `umass_ext`, or a `umass_netfmg` sub-key) before it can be an anchor.
* `pnw_handbook_epn` is scoped to one entomopathogenic-nematode entry. The PNW Plant Disease Handbook pear-scab page (published by OSU, "Copyright (c) Oregon State University") has no admissible key; quoted for the PLA-457 figures and twig-overwintering only. NEEDS-CATALOG-ADMISSION if the orchestrator wants it as an anchor (`osu_ext` is the publisher but the domain differs).
* MSU page is JS-rendered: two first-party paths returned no article text; only the proxy did. Two proxy passes returned the same quotes, but treat them as proxy evidence.
* UGA C742 lives at fieldreport.caes.uga.edu (the publication's own permalink); `uga_ext` is the parent key.

---

## Codling moth [pests]  -- severity high, type insect
STATUS: SOURCED-WEAK
ORGANISM: Cydia pomonella, per UC IPM PN 7412 ("Codling moth, Cydia (Laspeyresia) pomonella, is a serious insect pest of apples, pears, and English walnuts.") and NC State Handbook ch. 15 ("Codling moth larvae (Cydia pomonella) overwinter behind loose bark...").
ANCHORS:
uc_ipm https://ipm.ucanr.edu/agriculture/pear/codling-moth/ -- verified 2026-09-04 -- commercial (the record's current anchor; Pear Pest Management Guidelines)
  > "Codling moth has the greatest potential for damage of any pear pest, yet it can be effectively controlled with properly timed treatments. It causes two types of fruit damage: stings and deep entries."
  > "Larvae may enter through the sides, stem end, or calyx (flower) end of the fruit."
  > "Codling moth has two generations, and maybe a partial third generation, each season in the pear-growing regions of California. Pears are exposed to only one and a half to two and a half generations before harvest."
  > "Remove host trees in nearby abandoned orchards (apple, pear, and walnut) to destroy reservoirs of codling moth."
  > "An option for small, organic orchards is hand thinning to remove all infested fruit during each generation, before worms leave fruit, and removal of dropped fruit. Trunk banding to provide places for the larvae to pupate can also be used to help control population levels, provided the bands are placed before pupation and removed before adult emergence."
  > "Organically acceptable tools for the control of codling moth include cultural control in conjunction with mating disruption, sprays of certain oils, codling moth granulovirus (Cyd-X, etc.), the Entrust formulations of spinosad, and kaolin clay (Surround)."
  > "Mating disruption works best in larger, uniform orchards that are relatively square. It is not recommended in orchards that are less than 3 to 5 acres in size."
uc_ipm https://ipm.ucanr.edu/home-and-landscape/codling-moth/ -- verified 2026-09-04 -- home (PN 7412; NOT currently cited by the record; pears are named on the page)
  > "Codling moth, Cydia (Laspeyresia) pomonella, is a serious insect pest of apples, pears, and English walnuts."
  > "Codling moth overwinters as full-grown larvae within thick, silken cocoons under loose scales of bark and in soil or debris around the base of the tree. The larvae pupate inside their cocoons in early spring and emerge as adult moths mid-March to early April."
  > "After mating each female deposits 30 to 70 tiny, disc-shaped eggs singly on fruit, nuts, leaves, or spurs. After the eggs hatch, young larvae seek out and bore into fruit or developing nuts."
  > "Depending on the climate, codling moth can have two, three, and sometimes four generations per year."
  > "On apples and pears, larvae penetrate into the fruit and tunnel to the core, leaving holes in the fruit that are filled with reddish-brown, crumbly droppings called frass (Figure 6)."
  > "Selecting varieties that are less susceptible to damage, such as early-maturing apples and pears and late-leafing walnuts, can greatly reduce the potential for damage."
  > "Sanitation should be the first step in any codling moth control program, and it is even more important for those wishing to use primarily nonchemical management approaches. Every week or two, beginning about six to eight weeks after bloom, check fruit on trees for signs of damage. Remove and destroy any infested fruit showing the frass-filled holes."
  > "It also is important to clean up dropped fruit as soon as possible after they fall, because dropped fruit can have larvae in them. Removing infested fruit from the tree and promptly picking up dropped fruit from the ground is most critical in May and June but should continue throughout the season."
  > "Excellent control can be achieved by enclosing young fruit in bags right on the tree to protect them from the codling moth. This is the only nonchemical control method that is effective enough to be used alone and in higher population situations."
  > "Bagging should be done about four to six weeks after bloom when the fruit is from 1/2 to 1 inch in diameter. Prepare No. 2 paper bags (the standard lunch bag size that measures 7 1/4 inches by 4 inches) by cutting a 2-inch slit in the bottom fold of each bag. Thin the fruit to one per cluster."
  > "Hanging traps in each susceptible fruit or nut tree might help to reduce codling moth populations on isolated trees but isn't a reliable way to reduce damage."
  > "Codling moth pheromone traps are important for monitoring flight activity of moths to help time insecticide treatments."
  > "Scaly-barked varieties such as Newtown Pippin and most types of pears have so many crevices on the trunk that many larva will pupate before they get to the banded area. However, even in the best situations, banding will control only a very small percentage of the codling moth, because many pupate elsewhere on the tree or in the ground. Additionally, if bands aren't removed and destroyed in a timely fashion, they could increase the population, so banding no longer is recommended for control in home gardens."
  > "Although a few predators such as spiders or carabid beetles might feed on codling moth larvae or pupae, naturally occurring biological control isn't effective."
  > "The most effective way to time insecticide sprays is with a pheromone trap and a degree-day calculation."
  > "Starting three to four weeks after bloom, check fruit at least twice a week looking for the first "stings," or tiny mounds of reddish-brown frass about 1/16 inch in diameter."
  > "Recently a new biological insecticide, CYD-X, a granulosis virus that affects only larvae (caterpillars) of the codling moth, has become available to home gardeners in California. ... University of California trials have shown that this product, when applied weekly during egg hatch throughout the season, is as effective as carbaryl* sprays at controlling codling moth in backyard trees."
  > "CYD-X also has the advantage of having no preharvest interval, so applications can be made up until the time of harvest and there are no limits on the number of times you can spray it."
  > "If you are using pheromone traps and degree day calculations as described above, this would be 200 to 250 degree-days after you begin regularly catching male moths. If you are just checking fruit, this would be when you see the first stings. Make applications weekly after that. ... Adding 1% oil to the application can improve effectiveness."
  > "Spinosad ... The first spring generation requires three sprays applied at 10-day intervals beginning at egg hatch (i.e., 250 degree-days, or when the first stings are found). For any subsequent summer generations, two sprays should suffice with the first spray applied at the beginning of each new egg hatch and the second spray applied 10 to 14 days later. No more than six sprays should be applied per season, and they shouldn't be applied within seven days of harvest. The addition of a 1% horticultural oil to the spray tank will further enhance the effectiveness of this material."
  > "Bacillus thuringiensis, pyrethrum, and pyrethrin/rotenone combinations are low toxicity materials that have been tested and haven't been found to be effective at controlling codling moth. Horticultural oil has shown variable efficacy when used alone but can be mixed with granulosis virus or spinosad to improve performance. Mating disruption products that employ large quantities of pheromone to prevent mating or pheromone plus an insecticide to attract and kill male moths have proven effective for large commercial plantings but aren't effective on small orchards of fewer than 5 acres. In fact, mating disruption can increase damage if used on small plantings or individual trees."
  > "In most backyard situations, the best course of action might be to combine a variety of the nonchemical and/or low toxicity chemical methods discussed below and accept the presence of some wormy fruit. ... It is ideal to make codling moth management a neighborhood project"
  > "*As of August 1, 2020, pesticides containing the active ingredient carbaryl are restricted use materials in California."
ncsu_ext_handbook_tree_fruit https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts -- verified 2026-09-04 -- home (corroboration, East)
  > "Moths lay many eggs on fruits, leaves, or nuts soon after petal fall. ... They tunnel inside the apple and pear fruits leaving frass-filled holes (Figure 15-40). Codling moths produce two to three generations per year and are particularly damaging to late-ripening fruit."
  > "Bagging individual fruit four weeks to six weeks after bloom provides excellent control, but bagging is a labor-intensive process only practical for small trees. Hanging sticky traps to catch adult codling moths can be part of an overall management protocol, but traps are not effective on their own. Tolerating some level of damage is also recommended, as the codling moth is nearly impossible to completely eradicate."
usu_ext https://extension.usu.edu/planthealth/research/backyard-pear-pests -- verified 2026-09-04 -- home (corroboration, Intermountain)
  > "Codling Moth. Importance as a Pest on Pear: moderate to high ... There are 2 - 3 generations per yr."
  > "Cultural practices include fruit thinning, removing infested fruits, and bagging fruit. ... Conventional insecticides include carbaryl, malathion, zeta-cypermethrin, and gamma-cyhalothrin, while spinosad is an organic option."
RECORD CLAIMS THAT HOLD:
* Larvae tunnel to the core leaving frass-filled entry holes and brown trails: PN 7412 ("tunnel to the core, leaving holes ... filled with reddish-brown, crumbly droppings called frass"), NC State ch. 15.
* Cydia pomonella; eggs on developing fruit and young leaves: PN 7412 ("eggs singly on fruit, nuts, leaves, or spurs"); "near bloom" is NC State ("soon after petal fall").
* Two or more generations per season: PN 7412, UC IPM ag (two + partial third in CA pear regions), NC State/USU (2-3).
* Same pest attacks apple: PN 7412.
* Monitor with pheromone traps to time control; degree-day / stings timing: PN 7412.
* Remove and destroy dropped and infested fruit: PN 7412 (sanitation "the first step").
* Bag individual fruit: PN 7412 (paper lunch bags, 4-6 weeks after bloom, 1/2 to 1 inch fruit).
* Spinosad on a degree-day schedule: PN 7412 (3 sprays at 10-day intervals from 250 DD, max 6/season, 7-day PHI).
* Mating disruption works at larger scale: PN 7412 (not <5 acres; can INCREASE damage on single trees), UC IPM ag (not <3-5 acres).
* Keep nearby abandoned pear or apple trees pruned or removed: UC IPM ag ("Remove host trees in nearby abandoned orchards"); PN 7412 (neighborhood project; unmanaged trees "a continual source").
* Beginner "scent traps help you know when to act": PN 7412 (traps for monitoring; NOT reliable for control).
RECORD CLAIMS WITH NO ANCHOR:
* "often at the calyx end": UC IPM ag lists "sides, stem end, or calyx (flower) end" with no frequency; no document read says "often". Drop "often".
* "infested pears drop early" / "Bad pears drop early": no document states early drop as a codling-moth symptom on pear; PN 7412 only says dropped fruit "can have larvae in them". Soften to "wormy pears often end up on the ground".
* "kaolin clay on a degree-day/petal-fall schedule": kaolin is in the UC IPM ag organically-acceptable list (commercial, "25-50 lb" per acre) and absent from PN 7412; no home schedule for kaolin against codling moth is published on either page. Either anchor to the ag list without a schedule, or drop from this entry (kaolin IS anchored for psylla, below).
RECORD CLAIMS THAT ARE WRONG:
* prevention_seasoned "band trunks to catch larvae seeking pupation sites" and prevention_beginner "wrap a band of cardboard around the trunk to trap crawling caterpillars": PN 7412 says, specifically of pears, "most types of pears have so many crevices on the trunk that many larva will pupate before they get to the banded area ... banding no longer is recommended for control in home gardens." The commercial page allows banding only "provided the bands are placed before pupation and removed before adult emergence" in "small, organic orchards". For a home tree this is the wrong rung; delete it or rewrite as "not worth doing on a pear".
BUNDLE / GENERIC VERDICT: n/a (single organism).
LADDER-RELEVANT FACTS the record does not carry:
* Overwintering stage/site: mature larvae in cocoons under loose bark and in soil/debris at the base (PN 7412, NC State). Adults emerge mid-March to early April (CA); mate when sunset temperatures exceed 62°F.
* Vulnerable window: egg hatch, 250-300 DD after first sustained trap catch, or the first "stings" 3-4 weeks after bloom; check fruit every week or two from 6-8 weeks after bloom; May-June sanitation is the critical period.
* Early-maturing pear varieties are less damaged (PN 7412); late-ripening fruit most damaged (NC State). NOTE: NC State ch. 15 also contains the sentence "Choose late-ripening apple or pear tree varieties ... as they are most resistant", which contradicts its own previous sentence and PN 7412; do not copy it.
* Physical rung with a real anchor: fruit bagging is "the only nonchemical control method that is effective enough to be used alone" (PN 7412); labor-limited to small trees (NC State).
* Biological rung: naturally occurring biocontrol "isn't effective" (PN 7412); Trichogramma releases used commercially in pears, "hasn't been tested in backyards".
* Soft-chemical rung: CYD-X granulovirus (weekly from egg hatch, no PHI, +1% oil; "won't harm beneficials or bees" per the Quick Tips) and spinosad (10-day interval, max 6/season, 7-day PHI, +1% oil). Bt, pyrethrum, pyrethrin/rotenone: "haven't been found to be effective". Oil alone: "variable efficacy".
* Conventional rung: carbaryl (14-21 day residual, disrupts natural enemies and bees, flares mites; restricted-use in California since 2020); USU lists carbaryl, malathion, zeta-cypermethrin, gamma-cyhalothrin for backyard use.
* What a home grower should NOT bother doing: trunk banding on pear (PN 7412), mating disruption on single trees (PN 7412: can increase damage), traps as a control (PN 7412, NC State).
* Exact "no control" wording: "Tolerating some level of damage is also recommended, as the codling moth is nearly impossible to completely eradicate." (NC State); "accept the presence of some wormy fruit" (PN 7412).
* Register note: the record's anchor is the COMMERCIAL guideline; PN 7412 is the home document, names pears, and carries every home control. Add PN 7412 as the primary anchor.
PLA-457: none seen on the codling moth pages (the 1% oil tank-mix with CYD-X/spinosad is an oil use, not a sulfur/oil interval).

---

## Pear psylla [pests]  -- severity high, type insect
STATUS: ANCHOR-MISPOINTED
ORGANISM: Cacopsylla pyricola (Foerster), per WSU FS376E ("Pear psylla (Cacopsylla pyricola [Foerster] [Hemiptera: Psyllidae]) is an important pest of pear in Washington.") and UC IPM ("Cacopsylla (=Psylla) pyricola").
ANCHORS:
wsu_ext https://treefruit.wsu.edu/web-article/pear-rootstocks/ -- verified 2026-09-04 -- commercial (the record's current anchor)
  > The word "psylla" does not occur on this page (grep of the full text: 0 hits; WebFetch independently reported "psylla: Does not appear"). It anchors nothing in this entry.
wsu_ext https://treefruit.wsu.edu/crop-protection/opm/pear-psylla/ -- verified 2026-09-04 -- commercial (FS376E, May 2022; the WSU page that actually carries the claims)
  > "Pear psylla (Cacopsylla pyricola [Foerster] [Hemiptera: Psyllidae]) is an important pest of pear in Washington. Honeydew produced by pear psylla causes fruit russet, and serious infestations can stunt and defoliate trees."
  > "In the Pacific Northwest, pear psylla is a pest only of pear."
  > "Pear psylla overwinter as winterform adults in a state of reproductive diapause. They begin laying eggs when pear buds begin to swell. First, eggs are deposited on the wood, generally at the base of fruit and leaf buds"
  > "Pear psylla has two to four summerform generations in most pear-growing regions, with generally two complete summerform generations occurring in Washington"
  > "Nymphs and adults are phloem feeders. Honeydew, produced by nymphs, drips or runs onto fruit, causing dark, russet blotches or streaks and downgraded fruit (Figure 6). The damage may be exacerbated by a sooty mold fungus that colonizes the honeydew and also marks fruit"
  > "In large numbers, pear psylla can stunt and defoliate trees and cause fruit drop. A carryover effect may reduce fruit set the following year. These symptoms, called psylla shock, are caused by toxic saliva from feeding nymphs"
  > "Pear psylla also transmit a mycoplasma disease organism (Candidatus Phytoplasma pyri: Pear decline phytoplasma) through its saliva."
  > "Important biological control organisms in Washington pear orchards are the parasitic wasp Trechnites insidiosus; true bugs Deraeocoris brevis, Campylomma verbasci, and Anthocoris spp.; lacewings Chrysoperla carnea, Chrysopa nigricornis, Hemerobius spp.; and the earwig Forficula auricularia."
  > "Particle films reduce pear psylla adult colonization and egg lay by 80-100%, which reduces pear psylla pressure for the first generation" [kaolin, commercial rates: "Surround CF/WP or Celite 610 at 50 lb/acre"]
  > "For organic sprays, scout and begin spraying organic insecticides weekly once young nymphs become present ... Products to use include summer oil, Cinnerate, or neem (Aza-Direct, Neemix, or Rango) ... Do not use azadirachtin products on Comice pears."
  > "For successful pear psylla integrated pest management, codling moth and mite sprays need to be compatible with pear psylla biological control."
wsu_ext https://treefruit.wsu.edu/crop-protection/opm/pear-psylla2/ -- verified 2026-09-04 -- commercial (Burts, Riedl, Dunley, 1993)
  > "As well as causing fruit russet, serious infestations can stunt, defoliate and even kill trees."
  > "In general, russeted cultivars, such as Bosc, sustain less fruit damage than smooth skinned pears. Red pears are less suitable hosts because they are generally less vigorous, and Asian pears are less prone to infestation than those of European origin."
  > "As populations of psylla increase rapidly on highly vigorous trees, avoid practices that overstimulate tree growth. Apply only enough nitrogen fertilizer to achieve adequate fruit set and good fruit size."
  > "Pulling off water sprouts or suckers growing from scaffold limbs through the center of the trees not only removes tender foliage that psylla feed on but also allows sprays to penetrate better. Pull water sprouts by hand, rather than cut them with loppers, to minimize regrowth. This should be done before sprouts develop woody attachment to limbs, normally before the end of June."
  > "Oil, in place of or combined with the first pesticide application, delays egg laying by winterform adults until green tissue appears on developing buds."
  > "Monitor nymphs as above and treat when density exceeds 0.3 per leaf."
  > "Pesticides applied to pears greatly reduce the effectiveness of natural enemies."
uc_ipm https://ipm.ucanr.edu/home-and-landscape/pear-psylla/ -- verified 2026-09-04 -- home
  > "Pear psylla (a psyllid, family Psyllidae) is an important pest of pear. In addition to damage caused by the psyllid's feeding and honeydew, it vectors a microscopic, pathogenic phytoplasma that causes pear decline disease."
  > "Adults overwinter in bark crevices, under bark scales of pear trees, or on the ground in organic litter or other places near pear trees."
  > "Adult females begin laying eggs on or near fruit spurs starting in late January or early February. ... Pear psylla has about five generations per year in California."
  > "Pear psylla is a greater problem on European varieties than on Asian varieties of pear."
  > "Nymphs of the psyllid excrete sticky honeydew that drips onto fruit. This induces the growth of black sooty mold that grows on the honeydew and causes fruit skins to become russeted (darkly discolored). The psyllids also inject a toxic saliva into trees while feeding. This causes portions of the leaf blade to blacken and affected leaves become yellow and sometimes drop prematurely."
  > "Keep trees growing vigorously with appropriate irrigation and fertilization to reduce the effect of pear psylla and pear decline. Apply horticultural oil at least once during the dormant season and by the beginning of January. If the psyllid and its damage have been abundant, make a second dormant treatment of oil just before bloom. Abamectin plus horticultural applied at petal fall can also give good control."
  > "During the growing season a systemic neonicotinoid such as imidacloprid can be applied. If using systemic insecticide, wait until trees have completed their flowering before making the application because the products can move to nectar and pollen and poison adults of honey bees, parasitoid (parasitic) wasps, and predatory insects that feed on nectar and pollen."
uc_ipm https://ipm.ucanr.edu/agriculture/pear/pear-psylla/ -- verified 2026-09-04 -- commercial (biology usable)
  > "Pear psylla is one of the most serious insect pest of pears because of its ability to develop resistance to insecticides and to vector the pathogen that causes pear decline."
  > "Pear psylla is a greater problem on European varieties than on Asian varieties."
  > "There are many naturally occurring predators and parasites of pear psylla including green lacewings, brown lacewings, and minute pirate bugs. Nonselective codling moth insecticides destroy many of these beneficials, resulting in outbreaks of this pest."
  > "If the overwintering adult population is adequately reduced before egg laying starts in late January or early February, the population can usually be kept low throughout the foliage season by petroleum oil, applied alone or added to sprays for other pests, and by natural enemies."
  > "Oil kills adult psylla but does not control eggs. It does discourage egg laying for about 1 month, however."
  > "Organically acceptable methods include biological and cultural control and sprays of approved oil, insecticidal soaps, azadirachtin, and kaolin clay."
  > "KAOLIN CLAY (Surround WP) ... COMMENTS: Apply prebloom; may cause mite outbreaks when used later in season."
  > "Repeated applications of oil at this time [petal fall] may cause tree injury."
usu_ext https://extension.usu.edu/planthealth/research/backyard-pear-pests -- verified 2026-09-04 -- home
  > "Pear psylla adults overwinter outside the orchard as adults and fly to pear trees in the early spring to lay eggs on buds and twigs. Nymphs hatch in spring and as they feed on leaves and fruit they secrete copious honeydew. Pear psylla may also transmit a disease called "pear decline" that can slowly kill trees over a number of years."
  > "Symptoms: sticky honeydew on leaves and fruit, and sometimes black sooty mold; random, scorched appearance to leaves; leaf drop and decreased fruit yields"
  > "Management: The best control is achieved with a dormant oil spray before leaves emerge in spring, to kill newly laid eggs. If the psylla population is high during the growing season, use either a 1% oil spray, insecticidal soap, or spinosad (all are organic)."
usu_ext https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-psylla -- verified 2026-09-04 -- commercial note
  > "Pear psylla is a very small sap-feeding insect and is considered the most serious insect pest of pear in the United States."
  > "Chemical control is difficult because the pear psylla rapidly develops resistance to insecticides."
  > "Avoid summer pruning which encourages shoot growth."
ncsu_ext https://content.ces.ncsu.edu/disease-and-insect-management-in-the-home-orchard -- verified 2026-09-04 -- home
  > "Pears have a few additional insect pests beyond those mentioned for apple, most notably the pear psylla. The most opportune time to control psylla on pear is before bloom with an oil application, both as a dormant and delayed dormant (when green buds begin to appear) application."
RECORD CLAIMS THAT HOLD:
* Honeydew, sooty mold, fruit russeting: WSU FS376E, UC IPM home, USU.
* Leaf scorch/blackening, premature drop, tree decline: UC IPM home ("portions of the leaf blade to blacken ... drop prematurely"), USU ("scorched appearance"), WSU (psylla shock: stunt, defoliate).
* "The signature pear pest": USU note ("the most serious insect pest of pear in the United States"), UC IPM ag ("one of the most serious").
* Cacopsylla pyricola, pear-specific: WSU ("a pest only of pear"), USU (hosts pear, quince).
* Overwinters as an adult: WSU ("winterform adults"), UC IPM home, USU.
* Several overlapping generations: WSU (2-4 summerform), UC IPM home (~5 in CA), UC IPM ag ("when generations overlap, all life stages are present").
* Outbreaks follow broad-spectrum sprays that kill natural enemies: UC IPM ag verbatim; WSU psylla2.
* Dormant-season horticultural oil: UC IPM home, USU, NC State, WSU (timing differs by region, see below).
* In-season insecticidal soap or summer oil: USU ("1% oil spray, insecticidal soap, or spinosad"), UC IPM ag (organic list), WSU (summer oil).
* Conserve anthocorid bugs and lacewings: WSU FS376E (Anthocoris spp., lacewings), UC IPM ag (lacewings, minute pirate bugs).
* Kaolin clay deters egg-laying: WSU FS376E ("reduce pear psylla adult colonization and egg lay by 80-100%") and UC IPM ag (prebloom; mite-outbreak caution). Both are commercial-scale statements; no home document read prescribes kaolin for psylla.
* Avoid lush nitrogen-pushed growth: WSU psylla2, USU note.
* Dormant oil + natural-enemy-friendly regime as the backbone: UC IPM ag verbatim.
RECORD CLAIMS WITH NO ANCHOR:
* "Nymphs feed in clusters on shoots" / "Tiny insects cluster on the new shoots": no document says "clusters"; WSU says summerform eggs go on rapidly growing leaf tissue along the mid-vein and nymphs concentrate on new growth at treetops (UC IPM ag). Reword to "on the new growth".
* "late winter" as the dormant-oil timing: UC IPM home says "by the beginning of January" (California); USU says "before leaves emerge in spring"; NC State says dormant AND delayed-dormant (green bud); WSU keys it to egg-laying at bud swell. Region-dependent; anchor the timing to the region or say "while the tree is bare, before buds swell".
RECORD CLAIMS THAT ARE WRONG:
* organic_treatment_seasoned "Dormant-season horticultural oil to smother overwintering adults and eggs" and beginner "smother the overwintering insects": UC IPM ag states "Oil kills adult psylla but does not control eggs. It does discourage egg laying for about 1 month". USU backyard says the opposite ("to kill newly laid eggs"). Two T1 documents disagree on the mechanism; the safe wording is the WSU/UC one (kills adults and delays egg laying). Do not assert that oil smothers eggs.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry:
* Monitoring signal a home grower can use: honeydew droplets on leaves/fruit; WSU's commercial threshold is 0.3 nymphs per leaf; UC IPM home gives no threshold.
* Cultural rungs with home anchors: pull (not cut) water sprouts by hand before end of June (WSU psylla2), avoid summer pruning (USU note), minimum nitrogen (WSU/USU), keep the tree vigorous but not lush (UC IPM home: "appropriate irrigation and fertilization").
* Cultivar susceptibility: russeted cultivars (Bosc) show less fruit damage; red pears and Asian pears less infested (WSU psylla2); "greater problem on European varieties" (UC IPM).
* Biological rung: named natural enemies (WSU); "Effectiveness of biological control increases in orchards where fewer codling moth treatments are applied" (USU note), so the codling-moth rung chosen affects this ladder.
* Soft-chemical rung: dormant oil (1-2 applications), summer oil 1%, insecticidal soap, spinosad (USU), neem/azadirachtin (WSU, UC IPM ag; NOT on Comice), kaolin prebloom (commercial anchors only).
* Conventional rung with a home anchor: abamectin + oil at petal fall; imidacloprid soil drench AFTER flowering with the UC IPM bee/parasitoid warning (UC IPM home). Insecticide resistance is documented (USU, UC IPM ag).
* Commercial-only statements (do not port to a home tree): honeydew washing with sprinklers, summer pruning at 2100-2400 PDD, particle film at 50 lb/acre, beat-tray sampling, economic thresholds (all WSU FS376E).
* Phytotoxicity: "Sulfur and oil sprays can be very phytotoxic to pear trees, especially when the weather is hot" (UC IPM ag); repeated petal-fall oil "may cause tree injury".
* Anchor repair: replace the rootstocks URL with FS376E (wsu_ext) plus the UC IPM home psylla page (uc_ipm); USU backyard pear pests (usu_ext) is the cleanest home-scale statement.
PLA-457:
  > UC IPM Pear PMG pear psylla (commercial), POSTHARVEST: "Sulfur and oil sprays can be very phytotoxic to pear trees, especially when the weather is hot."
  > same page, LIME SULFUR plus NARROW RANGE OIL comment: "Do not apply lime sulfur and oil spray any sooner than November 1 and only on trees not suffering from moisture stress. Phytotoxicity may occur any time the weather is hot so watch weather conditions closely."
  > WSU FS376E (commercial), Dormant/Delayed Dormant: "A sulfur or lime sulfur application with oil can also suppress pear rust mites and spider mites in addition to pear psylla adults." (a COMBINED sulfur+oil dormant spray, no interval)
  > NC State Disease and Insect Management in the Home Orchard (home), Oils: "Do not use in combination with or at least 10 days before or after a fungicide that contains sulfur or captan is applied, or severe leaf burn will occur." and, fungicide table: "DO NOT mix captan and or sulfur with oil."
  Not adjudicated.

---

## Pear scab [pests]  -- severity medium, type fungal
STATUS: SOURCED-OK
ORGANISM: Venturia pirina, per UC IPM PN 7413 ("Pear scab, which the fungus V. pirina causes, results in similar blemishes on pear fruit."); spelled Venturia pyrina by the PNW Handbook. The record's spelling ("Venturia pyrina") is the PNW form; the anchor uses "pirina". Either is defensible; note the anchor's spelling.
ANCHORS:
uc_ipm https://ipm.ucanr.edu/home-and-landscape/apple-and-pear-scab/ -- verified 2026-09-04 -- home (PN 7413, Updated 01/2011; live; carries the claims)
  > "Apple and pear scab are two different diseases that look very similar and are controlled in similar manners in home gardens and landscapes."
  > "Pear scab, which the fungus V. pirina causes, results in similar blemishes on pear fruit.The disease is most prevalent in the North Coast production area. However, V. pirina won't affect apples nor can the apple scab fungus cause problems on pears. Both have quite limited host ranges."
  > "Scab first appears as yellow, or chlorotic, spots on leaves. As the disease progresses, dark, olive-colored spots form on leaves, fruit, and--in severe cases--stems. Spots on the undersurface of leaves sometimes look velvety due to fungal growth. ... Severely affected leaves often turn yellow and drop."
  > "Scabby spots can appear on fruit later in the season. These begin as velvety or sooty, gray-black (and sometimes greasy looking) lesions that sometimes have a red halo. The lesions later become sunken and tan ... Severely infected fruit becomes distorted and usually drops from the tree. Fruit also can crack, which allows entry of secondary organisms."
  > "Both apple and pear scab pathogens overwinter primarily in infected leaves on the ground. Rainfall or sprinkler irrigation is necessary to release the spores. ... Pear scab also can overwinter in lesions on pear twigs in high rainfall areas."
  > "Infection occurs most rapidly between 55° and 75°F, and leaves or fruit must remain wet continuously for a minimum of 9 hours for initial infection to occur at these temperatures. If spring weather is dry from the green tip stage of bloom ... through fruit set, scab usually won't be a problem."
  > "Defoliation follows severe, early leaf infection. Late-season infections generally can be tolerated in backyard trees, because peeling the fruit will remove the pinpoint-sized scab lesions."
  > "For a single, backyard tree, removing--then composting or destroying--its dropped leaves in autumn or winter can limit the disease to tolerable levels. ... In pears, apply urea by itself, because zinc can be phytotoxic."
  > "If you are using sprinklers that wet any of the tree's foliage, irrigate between sunrise and noon to allow adequate drying time, or reduce the angle of the sprinkler."
  > "European pear cultivars with negligible scab risk include Arganche, Barnett Perry, Batjarka, Brandy, Erabasma, Harrow Delight, Muscat, Orcas, and Passe Crassane. Because Asian pears (Pyrus pyrifolia) are a different species, they are less susceptible to scab than European pears (P. communis)."
  > "Fungicide sprays are necessary only if the weather is rainy and leaves are likely to remain wet for 9 or more hours. Fungicide applications require careful attention to timing, as preventing early infection is the most important step toward successfully controlling later fruit infections. It is difficult to prevent secondary fruit infections once primary infections occur."
  > "Unlike peach leaf curl, treatments for scab made when trees are completely dormant aren't effective and aren't recommended. If treatments are needed, the generally recommended time is between when buds begin to break and a month after petal fall."
  > "Several fungicides are available for controlling apple and pear scab. These include fixed copper, Bordeaux mixtures, copper soaps (copper octanoate), sulfur, mineral or neem oils, and myclobutanil. All these products except myclobutanil are considered organically acceptable."
  > "Generally copper or Bordeaux sprays should be used only from green tip to full bloom. Later applications increase the risk of fruit russetting"
  > "You can apply wettable sulfur through bloom and early fruit set. When using sulfur-containing compounds such as wettable sulfur, never apply them within 3 weeks of an oil application or when temperatures are near or higher than 90°F."
[no admissible key] PNW Plant Disease Handbook, Pear (Pyrus spp.)-Scab, https://pnwhandbooks.org/plantdisease/host-disease/pear-pyrus-spp-scab -- verified 2026-09-04 -- commercial (corroboration only)
  > "Cause Venturia pyrina, a fungus that overwinters in infected fallen leaves and, in some areas, on pear twigs. Twig infection occurs sometimes in the Mosier and Medford, OR areas and commonly west of the Cascade Range and coastal British Columbia."
  > "The cultivars Forelle and Bartlett Red Sensation are very susceptible. The disease does not cause apple scab, nor can the apple scab fungus cause pear scab."
  > "Old fruit infections often crack open. Cracks are surrounded by russeted, corky tissue and then an olive-color ring of active fungus growth."
  > "Pruning out infected twigs also offers some benefit."
RECORD CLAIMS THAT HOLD:
* Olive-green to black velvety spots on leaves, shoots, fruit; corky, cracked fruit lesions; yellowing; early defoliation: PN 7413 (stems "in severe cases", "velvety", "crack", "turn yellow and drop"); PNW ("russeted, corky").
* "The pear analog of apple scab" / distinct fungus, managed the same way: PN 7413.
* Venturia pyrina; overwinters in fallen leaves; wet spring; leaf wetness and temperature: PN 7413 (55-75°F, 9 h wet).
* Sulfur on a protective schedule keyed to spring infection periods; prevention beats cure: PN 7413.
* Rake and remove fallen leaves in autumn (the overwintering source): PN 7413.
* Choose less-susceptible varieties: PN 7413 names nine European cultivars with "negligible scab risk".
* Beginner "In a bad year the tree drops its leaves early": PN 7413.
RECORD CLAIMS WITH NO ANCHOR:
* "prune for airflow" (both registers): PN 7413 prescribes leaf removal and morning-only sprinkler timing, not airflow pruning. UMN's general pear sanitation sentence ("pruning to promote good airflow through the tree") is the nearest home anchor but is not scab-specific.
RECORD CLAIMS THAT ARE WRONG: none.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry:
* Pear scab, unlike apple scab, can overwinter on TWIGS in high-rainfall areas (PN 7413; PNW: "commonly west of the Cascade Range"), so autumn leaf removal alone may not clear inoculum in a Maritime PNW / North Coast tree; PNW: "Pruning out infected twigs also offers some benefit."
* Fungicide window: green tip through about one month after petal fall; dormant sprays "aren't effective and aren't recommended"; copper/Bordeaux only green tip to full bloom (russet risk); wettable sulfur through bloom and early fruit set; stop if no scab one month after petal fall.
* Sanitation extras for pears: urea alone on leaves in autumn to hasten leaf fall (no zinc on pear).
* Tolerance statement: "Late-season infections generally can be tolerated in backyard trees, because peeling the fruit will remove the pinpoint-sized scab lesions."
* Resistant cultivar list BY NAME exists (PN 7413) and none of the record's own recommended varieties (Hood, Kieffer, Orient, Seckel, Moonglow, Ayers, Warren, Bartlett, Comice, Bosc) appears on it except none; Harrow Delight (on the roster's UAEX fire-blight list) is on it.
PLA-457:
  > UC IPM PN 7413 (home): "When using sulfur-containing compounds such as wettable sulfur, never apply them within 3 weeks of an oil application or when temperatures are near or higher than 90°F."
  > PNW Handbook pear scab (commercial): "Rex Lime Sulfur Solution (28%) at 1.5 to 2 gal/100 gal water depending on growth stage. ... Do not use on 'd'Anjou', 'Comice' or 'Seckle' or with oil."; "Microthiol Disperss (80% sulfur) at 10 to 20 lb/A. Do not use a spreader-sticker or apply to 'Anjou'."
  Not adjudicated.

---

## Fabraea leaf spot [pests]  -- severity medium, type fungal
STATUS: ANCHOR-MISPOINTED (claims mostly true and FOUND at T1; two claims are wrong)
ORGANISM: Diplocarpon mespili (Sorauer) Sutton, the current name used by MSU ("Diplocarpon mespili (Soraur) Sutton", proxy read) and the UMass NETFMG ("Fabraea leaf spot is a fungus (Diplocarpon mespili)"); synonym Fabraea maculata used by Penn State ("caused by the fungus Fabraea maculata") and UMaine; Entomosporium is the spore stage per UGA Plant Disease Library ("Entomosporium is the conidial stage of the Ascomycete fungus Fabraea (or Diplocarpon). Sometimes Entomosporium leaf spot diseases are referred to as Fabraea leaf spots in some references."). Neither NC State document nor UGA C742 gives a binomial ("Pear leaf spot (also called fabraea leaf spot)"; "Pear leafspot").
ANCHORS:
clemson_hgic https://hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ -- verified 2026-09-04 -- home (the record's current anchor)
  > HGIC 2208 contains no occurrence of "Fabraea", "Entomosporium", "leaf spot" or "Diplocarpon" (grep of the full text: 0 hits; WebFetch: "No mention of Fabraea leaf spot, Entomosporium, pear scab, or other diseases"). It anchors nothing in this entry. No Clemson HGIC factsheet on edible-pear leaf spot exists: HGIC 1352 Asian Pear does not mention leaf spot; HGIC 1006 Bradford Pear covers Entomosporium on ORNAMENTAL callery pear only and refers to HGIC 1081 Photinia for control. RETIRE clemson_hgic from this entry rather than repoint it.
ncsu_ext https://content.ces.ncsu.edu/growing-pears-in-the-home-garden -- verified 2026-09-04 -- DEAD (404 on curl, WebFetch and the jina proxy: "Oops! Looks like we don't have that resource."). The sibling title "Growing Pears in North Carolina" is retired ("This publication ... is no longer available").
ncsu_ext https://content.ces.ncsu.edu/disease-and-insect-management-in-the-home-orchard -- verified 2026-09-04 -- home (the live NC State document; repoint target)
  > "Pears are affected with many of the same diseases as apples with the exception of cedar apple rust, which does not occur on pears. Fire blight tends to be more severe on pears than apples and can kill large limbs and even entire trees of susceptible cultivars; Bartlett is highly susceptible. Pear leaf spot (also called fabraea leaf spot) can be important on some cultivars (Figure 10)."
  > "Captan is not registered for use on pears. Use thiophanate methyl at 2 teaspoons per gallon of water (6 2/3 tablespoons per 10 gallons). Use the same fungicide spray schedule for pears as described above for apples, excluding captan."
  > [the apple schedule it points to] "When flower petals begin to drop, make a fungicide and insecticide application and repeat at 2 to 3 week intervals until 3 weeks before harvest. Use a 2-week spray interval if weather conditions are wet or there have been disease or insect problems in past years."
psu_ext https://extension.psu.edu/leaf-and-fruit-spot-of-pear-in-home-gardens -- verified 2026-09-04 -- home (Updated June 10, 2026; the best home anchor found)
  > "Leaf blight and fruit spot are caused by the fungus Fabraea maculata, which infects the leaves, fruit, and shoots of pear and quince and the leaves of apple trees."
  > "The disease can build up rapidly, even in orchards where it has not been a problem. If conditions favor the disease and it goes unchecked, pear trees can be defoliated in a few weeks."
  > "Leaf spots first appear as small, purple dots on the leaves nearest the ground. They grow into circular spots and become purplish-black or brown. A small, black pimple appears in the center of the spot. ... Fruit lesions are much like those on leaves, but they are black and slightly sunken. They can be so numerous that they run together, causing the fruit to crack."
  > "Lesions on twigs occur on current-season growth. They are purple to black with indefinite margins. The lesions can run together and form a superficial canker. Early defoliation leads to small fruit, weak bud formation, and fall blossoming."
  > "The sexual spore stage develops on fallen, overwintered leaves. Conidia--asexual spores--might also develop in the spots on overwintered leaves, or they can be produced in the previous season's shoot infections. Often, the first infections do not occur until mid-June to the first of July. Secondary infections begin about 1 month later and reoccur throughout the season during periods of rain."
  > "Routine fungicide sprays normally control this disease in Pennsylvania. In the northeastern states, fungicide applications in June and July generally will control this leaf spot; however, mid-August and September applications are advisable in wet seasons, especially on late varieties such as Bosc."
uga_ext https://fieldreport.caes.uga.edu/publications/C742/home-garden-pears/ -- verified 2026-09-04 -- home (Circular 742, "published with full review on March 4, 2026")
  > "Diseases common to pears are scab, black rot, bitter rot, pear leaf spot and fire blight. The two most common diseases are pear leaf spot and fire blight."
  > "Pear leafspot begins as small purplish-black spots on the leaves or fruit. The spots gradually enlarge to form brown lesions about 1/8 to 1/4 in. in diameter. A small, black blister may appear in the center of these spots. Leafspots can only be controlled with a spray program beginning as the first leaves appear and continuing through July."
msu_ext https://www.canr.msu.edu/ipm/diseases/fabraea_leaf_spot -- verified 2026-09-04 -- commercial, PROXY READ (r.jina.ai via WebFetch; first-party paths returned no article text)
  > "Diplocarpon mespili (Soraur) Sutton"
  > "Common to all fruit-growing regions in eastern North America; most problematic in warm and humid production regions."
  > "Lesions on leaves and petioles start as small, circular purple to black pinpoint spots. They enlarge quickly to a diameter of about 10 mm, develop a dark brown to black interior, and may coalesce to form larger areas of infection." ... fruit lesions "cause the fruit to crack." ... "heavily infected leaves and fruit drop prematurely."
  > "Primary infections usually occur during the 6 weeks after petal fall."
  > "Removal or destruction of leaf litter can reduce early season disease pressure."
  > "regular applications of fungicides from white bud through late summer may be necessary to prevent disease in orchards that were severely diseased in previous years."
  > "Bosc and Seckel pears are more susceptible than Bartlett."
[NEEDS-CATALOG-ADMISSION: umass_ext scope] UMass New England Tree Fruit Management Guide, https://netreefruit.org/pears/diseases/fabraea-leaf-spot -- verified 2026-09-04 -- commercial
  > "Fabraea leaf spot is a fungus (Diplocarpon mespili) that infects primarily leaves and fruit of pear and quince."
  > "Leaf and fruit infections are most notable in the Northeast and Midwest, but in the Southeast , shoot infection can be significant."
  > "Similar to apple scab, much Fabraea overwinters in leaves on the orchard floor. Farther south, overwintering is also likely to occur in shoot cankers. Spores are released from leaves with rain from mid-May to July (in the Northeast and Midwest) and result in primary infection on fruit and foliage. Shoot cankers spread Fabraea from late-April through May (in the Southeast) with more driving rains. Length of wetting for infection to occur can range from 12 hours at 50 degrees F. to as little as 8 hours from 68 to 77 degrees F. Infections take about 7 days to become visible."
  > "Other than sanitation, there is no known biological control of Fabraea leaf spot."
  > "Flail mowing/chopping leaves and brush and removing obvious cankers on the tree may help to control Fabraea leaf spot and is recommended."
  > "Although there are some variety differences in susceptibility to Fabraea leaf spot, generally just consider the fact all European pear varieties are susceptible such that the disease will need to be controlled. Bosc and Seckel, however, appear to be especially susceptible to Fabraea."
uga_ext https://plantpath.caes.uga.edu/content/dam/caes-subsite/plant-pathology/extension-pdfs/PDL-fungi-entomosporium.pdf -- verified 2026-09-04 -- pdf (taxonomy only)
  > "Entomosporium is the conidial stage of the Ascomycete fungus Fabraea (or Diplocarpon). Sometimes Entomosporium leaf spot diseases are referred to as Fabraea leaf spots in some references."
RECORD CLAIMS THAT HOLD:
* Numerous small dark purple-to-black spots on leaves and fruit; heavy infection defoliates; pitted, cracked fruit: PSU, UGA C742, MSU.
* "Most damaging in warm, humid regions": MSU ("most problematic in warm and humid production regions"); UGA (one of the "two most common diseases" in Georgia).
* Entomosporium mespili (Fabraea maculata): PSU (F. maculata) + UGA PDL (Entomosporium = conidial stage). Current name is Diplocarpon mespili (MSU, NETFMG); consider "Diplocarpon mespili (the Fabraea/Entomosporium leaf spot fungus)".
* Overwinters in fallen leaves and infected twigs: PSU ("fallen, overwintered leaves ... or ... the previous season's shoot infections"); NETFMG.
* Spreads in warm, rainy summer weather, building late: PSU (first infections mid-June to July 1, secondary a month later, "reoccur throughout the season during periods of rain").
* Protective fungicide on a summer schedule where it has a history: PSU (June-July, plus Aug-Sept in wet years), NC State (thiophanate-methyl on the 2-3 week apple schedule), UGA (first leaves through July), MSU (white bud through late summer where previously severe).
* Rake and destroy fallen leaves: MSU ("Removal or destruction of leaf litter can reduce early season disease pressure").
* Beginner "bigger problem in hot, humid areas": MSU.
RECORD CLAIMS WITH NO ANCHOR:
* "resistant cultivar choice" / "choose a resistant variety": no admissible document names a Fabraea-resistant European pear cultivar. NETFMG: "generally just consider the fact all European pear varieties are susceptible such that the disease will need to be controlled." MSU says only that Bartlett is LESS susceptible than Bosc and Seckel. A resistant-cultivar list BY NAME does not exist in any document read (PSU, NC State x2, UGA C742, MSU, NETFMG, Clemson x3, PNW).
* "airflow pruning" / "prune so air moves through the tree": not on any Fabraea document; UMN's generic "pruning to promote good airflow" is the nearest.
RECORD CLAIMS THAT ARE WRONG:
* symptoms_seasoned "on susceptible cultivars (Bartlett, Bosc)": MSU: "Bosc and Seckel pears are more susceptible than Bartlett."; NETFMG: "Bosc and Seckel, however, appear to be especially susceptible to Fabraea."; PSU: "especially on late varieties such as Bosc". Bartlett is the LESS-susceptible cultivar in both documents that grade it; Seckel (on this crop's recommended list) is the missing name. Replace "(Bartlett, Bosc)" with "(Bosc, Seckel)".
* prevention_seasoned "the disease is far worse in the humid Southeast than in arid or northern regions": no document states a Southeast-versus-North gradient. NETFMG's own sentence runs the other way for the symptom the record describes: "Leaf and fruit infections are most notable in the Northeast and Midwest, but in the Southeast , shoot infection can be significant." PSU calls routine sprays normal in Pennsylvania. MSU's scope is "warm and humid production regions" of eastern North America, which includes the Northeast/Midwest. The "arid" half is plausible (rain-driven disease) but unstated. Rewrite as "worst in warm, humid, rainy regions of the East and South" without the North comparison.
BUNDLE / GENERIC VERDICT: n/a (single organism; "Fabraea" and "Entomosporium" are two names for one fungus).
LADDER-RELEVANT FACTS the record does not carry:
* Two inoculum sources with different timing: overwintered leaves (spores released mid-May to July, NE/Midwest) and shoot/twig cankers (late April to May, Southeast). A Southeast home tree needs twig-canker removal, not only leaf raking; NETFMG: "removing obvious cankers on the tree may help ... and is recommended".
* Primary window: "the 6 weeks after petal fall" (MSU); first visible infections often mid-June to July 1 (PSU); wetting 8-12 h; 7 days to symptoms (NETFMG).
* Late cultivars (Bosc) need protection into August-September in wet years (PSU).
* Home fungicide with an anchor: thiophanate-methyl at 2 tsp/gal, captan NOT registered on pears (NC State). Commercial: EBDCs/ziram, 77-day PHI (NETFMG). No resistance known "because contact fungicides are necessary for control".
* "no known biological control" (NETFMG, verbatim above).
* Consequences of defoliation: "small fruit, weak bud formation, and fall blossoming" (PSU).
* Cultivar susceptibility for the variety pass: Bosc and Seckel high; Bartlett lower (MSU, NETFMG).
* Prose flag: seasoned register "overwintering inoculum" (diseases copy) is fine; beginner copies use everyday words. No em dashes, no temperatures, no "plant" capitalization issues in either copy.
PLA-457: NC State Disease and Insect Management in the Home Orchard (this entry's live NC State document): "Do not use in combination with or at least 10 days before or after a fungicide that contains sulfur or captan is applied, or severe leaf burn will occur." and "DO NOT mix captan and or sulfur with oil." Not adjudicated.

---

## Fire blight [diseases]  -- severity high, type bacterial
STATUS: SOURCED-OK (two named-cultivar and one management claim need second anchors, listed below)
ORGANISM: Erwinia amylovora, per Clemson HGIC 2208 ("This is a bacterial disease caused by Erwinia amylovora") and WSU FS391E ("Fire blight is caused by Erwinia amylovora, a gram-negative, rod-shaped bacterium.").
ANCHORS:
clemson_hgic https://hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ -- verified 2026-09-04 -- home (HGIC 2208, Updated Jul 18, 2025; live; carries most claims)
  > "Fire blight is one of the most devastating and difficult-to-control diseases of many fruit trees, including apple and pear, as well as of other rosaceous ornamental plants. This is a bacterial disease caused by Erwinia amylovora, which can spread rapidly, killing individual apple and pear trees when conditions are right for disease development and if susceptible rootstocks are used."
  > "The first symptoms of fire blight occur in early spring when temperatures are above 60 °F and the weather is rainy or humid. Infected flowers turn black and die. The disease moves down the branch, resulting in death of young twigs. These blacken and curl over, giving the appearance of a "shepherd's crook." Leaves on affected branches wilt, blacken, and remain attached to the plant, giving it a fire-scorched appearance. Slightly sunken areas, called cankers, appear on twigs, branches, and the main stem. ... During wet spring weather, there may be a milky-like, sticky liquid oozing from the infected plant parts, and it contains the bacterial pathogen."
  > "In the home garden, fire blight can be very destructive to apple and pear trees. Pear trees are particularly susceptible."
  > "There is no cure for fire blight, making disease prevention extremely important. ... Prune out blackened twigs and branches with cankers during the dormant season. Pruning during the growing season may spread the disease."
  > "Moderately resistant edible pears include 'Ayers' 'Keiffer' 'LeConte' 'Moonglow' 'Magness' 'Orient' 'Seckel' (somewhat resistant)"
  > "Reduce the spread of fire blight by removing and destroying all infected plant parts. Pruning cuts of twigs and branches are made a minimum of 8 to 12 inches below any sign of infected tissue. Promptly destroy of all infected prunings by burning or burying. Disinfect, all pruning tools between cuts using a 10% bleach solution (1 part household bleach to 9 parts water) or 70% alcohol. To reduce the spread of fire blight, pruning is best done during the dormant season. Avoid excess nitrogen fertilization, which results in excess succulent growth, because if injured, succulent new growth is easily infected. Remove all suckers coming up from the base of the trees, as these are more susceptible to fire blight infection, which can then move rapidly into the trunk."
  > "Bacteria enter the plant through blossoms, fresh wounds, or natural openings. ... However, to protect all pollinating insects, do not use insecticides during bloom."
  > "Pears: Pear trees are also treated with a pre-bloom, copper fungicide spray, and then sprays of streptomycin during bloom. Apply the first spray with streptomycin as soon as the flowers open. Repeat at 3 to 4 day intervals as long as blossoms are present. The time between streptomycin application and fruit harvest must be a minimum of 50 days."
  > "NOTE: Adequate control of diseases and insects on large trees is usually not feasible, since complete coverage of the foliage with a pesticide cannot be achieved."
  > Table 1: "Copper (Do not apply after green tip reaches 1/2 inch) ... Streptomycin (Do not apply when fruit is visible) Ferti-lome Fire Blight Spray"
uc_ipm https://ipm.ucanr.edu/home-and-landscape/fire-blight/ -- verified 2026-09-04 -- home (PN 7414)
  > "Pear (Pyrus species) and quince (Cydonia) are extremely susceptible. Apple, crabapple (Malus species), and firethorns (Pyracantha species) also are frequently damaged."
  > "Open flowers are the most common infection sites and remain susceptible until petal fall."
  > "Ideal conditions for infection, disease development, and spread of the pathogen are rainy or humid weather with daytime temperatures from 75° to 85°F, especially when night temperatures stay above 55°F."
  > "Vigorously growing shoots are the most severely affected; therefore, conditions such as high soil fertility and abundant soil moisture, which favor rapid shoot growth, increase the severity of damage to trees. In general, trees are more susceptible when young and suffer less damage as they age."
  > "The succulent tissue of rapidly growing trees is especially vulnerable; thus excess nitrogen fertilization and heavy pruning, which promote such growth, should be avoided. Trees shouldn't be irrigated during bloom."
  > "Most pear tree varieties, including Asian pears (with the exception of Shinko) and red pear varieties, are very susceptible to fire blight."
  > "Successful removal of fire blight infections is done in summer or winter when the bacteria no longer are spreading through the tree. ... Rapidly advancing infections on very susceptible trees (pear, Asian pear, and some apple varieties) should be removed as soon as they appear in spring. In these cases, dipping shears in 10% bleach between cuts might be wise. However, the location of the cut is far more important than the cleansing of tools. ... To locate the correct cutting site, find the lower edge of the visible infection in the branch, trace that infected branch back to its point of attachment, and cut at the next branch juncture down without harming the branch collar."
  > "Copper products are the only materials available to homeowners for fire blight control, and they often don't provide adequate control even with multiple applications. ... For pear trees, this might mean five to 12 applications per season. Copper products also might cause russeting or scarring of the fruit surface."
uga_ext https://fieldreport.caes.uga.edu/publications/C742/home-garden-pears/ -- verified 2026-09-04 -- home (Circular 742)
  > "Because of the prevalence of fire blight in the humid eastern and southern states, however, most of the pear production has been relocated to the drier areas of the Pacific Northwest."
  > "Bartlett is the most recognized European-type pear in America and is not adapted to the Southeast and should not be planted in Georgia."
  > "Pruner's Note: Pear trees are extremely susceptible to fire blight, a disease that kills limbs and sometimes whole trees. Remove diseased branches as soon as they appear. When pruning out a diseased limb, cut at least 6 in. below the area where any infection appears. After each cut, dip the cutting surfaces of your pruners in rubbing alcohol or a 1:9 chlorine bleach:water mixture."
  > "Pear trees can be protected from fire blight by a spray program beginning at bloom and continuing through the summer. Once a tree has been infected, cut out and burn the diseased portions. Sprays will not control the disease in infected branches. Make cuts 6 to 8 in. below any dead tissue."
  > Variety table: "Orient ... Resistant to blight."; "Carrick ... Trees resistant to blight."; "Waite ... Resistant to blight. Pollen sterile."; "Kieffer ... Poor quality. Subject to blight in wet years."; "Baldwin ... Resistant to blight."; "Spalding ... Subject to blight."; "Warren ... Very high quality fruit. Resistant to blight."; Magness and Moonglow carry no blight rating in this table.
uada_ext_fruit_trees https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx -- verified 2026-09-04 -- home (confirms the catalog's citable_for text)
  > "When choosing fruit tree varieties, look for smaller varieties that can fit into a yard, and something that is fire blight resistant. Fire blight is a bacterial disease. There are sprays that can help to prevent it, but they aren't fool-proof."
  > "The two most disease resistant varieties for apples for Arkansas are William's Pride and Enterprise. For pears try Harrow Delight, Maxine, Kiefer, Magness and Moonglow."
uada_ext https://www.uaex.uada.edu/publications/PDF/FSA-6059.pdf -- verified 2026-09-04 -- pdf, home (FSA6059 Pear Production in the Home Garden)
  > "the susceptibility of European pears to fire blight limits their use."
  > "Pears often have severe problems with fire blight, and gardeners should only plant varieties with high blight tolerance. It is possible to lessen the effects of fire blight with judicious sprays, but this is difficult for homeowners to do and is not encouraged."
  > "Fire blight is the most serious pear disease in Arkansas and limits the production of pears to highly resistant varieties."
  > "Prevention through selection of resistant varieties is the most effective means of control. Chemical control of fire blight is difficult, especially in the home orchard. Chemical sprays with streptomycin (Agri-Strep) are beneficial if applied at five-day intervals beginning at first bloom."
  > "Prune out fire blight-damaged tissue anytime the disease is noted. Make cuts at least 6 inches below the diseased tissue. Sterilize pruning shears in a 10 percent solution of liquid chlorine bleach after each cut."
  > "If fire blight is a problem, discontinue fertilizer applications." ... "If fire blight becomes a serious problem, prune sparingly, since the vigorous shoots stimulated by pruning cuts are usually more susceptible to fire blight."
  > "Also, in cases of severe fire blight damage, multiple leaders offer more chances of escape from serious injury than trees with a single leader."
  > Table 1: Comice "Good fire blight resistance"; Harrow Delight "high resistance to fire blight"; Kieffer "High resistance to fire blight"; Maxine "High fire blight resistance"; Magness "High fire blight resistance"; Moonglow "High resistance to fire blight"; Seckel "Some fire blight resistance".
uada_ext https://www.uaex.uada.edu/publications/PDF/FSA-6129.pdf -- verified 2026-09-04 -- pdf, home
  > "Ayers (Ayres) ... moderately resistant to fire blight"; "Orient ... Good fire blight resistance."; (Comice, Harrow Delight, Kiefer, Magness, Maxine, Moonglow, Seckel as in FSA6059).
usu_ext https://extension.usu.edu/planthealth/research/backyard-pear-pests -- verified 2026-09-04 -- home
  > "Most importantly, all infected shoots, twigs, and limbs should be pruned out of the tree as soon as they appear (about 2 weeks after bloom). Cut 12 inches below visible symptoms into healthy wood to be certain that the bacteria are removed. Do not prune during wet conditions, as this can contribute to disease spread. During bloom, protect flowers from infection by applying an antibiotic spray just before, or 24 hours after, a rainfall."
umn_ext https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-pears -- verified 2026-09-04 -- home
  > "Too much nitrogen fertilizer, including compost, can cause fast new growth that is very susceptible to fire blight."
  > "Water sprouts or suckers should be removed promptly on susceptible varieties. Do not prune while the tree is in bloom and up to two weeks after blooming."
  > "When pruning a diseased shoot, cut at least 6 inches below where you see discolored bark. After each cut, disinfect pruning tools in a mixture of 1 part water to 3 parts denatured alcohol or a mixture of 1 part chlorine bleach to 9 parts water."
ncsu_ext https://content.ces.ncsu.edu/disease-and-insect-management-in-the-home-orchard -- verified 2026-09-04 -- home
  > "Fire blight tends to be more severe on pears than apples and can kill large limbs and even entire trees of susceptible cultivars; Bartlett is highly susceptible."
ncsu_ext_handbook_tree_fruit https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts -- verified 2026-09-04 -- home
  > "Pears Pyrus communis ... Moonglow, Magness (not a pollen source), Kieffer, Harrow Delight, Harrow Sweet, Harvest Queen, Seckel ... Plant only fire blight-resistant cultivars."
  > "Copper products are the only chemical management available to homeowners, and they are difficult to time and apply effectively."
  > "For pear varieties subject to fire blight, a multileader tree is the goal of another training system. With a multileader tree, if one leader is infected with fire blight, it is safe to remove the infected leader without compromising the tree's health."
wsu_ext https://treefruit.wsu.edu/web-article/pear-rootstocks/ -- verified 2026-09-04 -- commercial (rootstock claim)
  > "The OHxF selections are compatible with most pear varieties and are known for their tolerance to blight and decline."
wsu_ext https://treefruit.wsu.edu/crop-protection/disease-management/fire-blight/ -- verified 2026-09-04 -- commercial (FS391E)
  > "Remove infected branches 12 to 18 inches below the visibly infected tissue in wood that is two years old or older (Figure 6)."
  > "in multiple studies sterilizing shears made no difference in preventing canker formation as long as the cuts are made at the recommended distance below the visible canker"
  > "Very young infected trees, first to third leaf, should be removed and destroyed. In young, vigorous trees, bacteria move quickly through the tree, and pruning therapies are unlikely to be effective."
  > "In Washington Cougar Blight is available at WSU Decision Aid System for Tree Fruit (DAS) or in Excel format. This model calculates fire blight risk based on the temperature of the previous four days"
RECORD CLAIMS THAT HOLD:
* Shepherd's crook, blackened blossoms/shoots, scorched look, sunken oozing cankers: Clemson verbatim.
* Pear more susceptible than apple: Clemson ("particularly susceptible"), UC IPM ("extremely susceptible"), NC State home orchard ("more severe on pears than apples").
* Erwinia amylovora; infection through blossoms and tender shoots in warm, wet spring weather: Clemson (>60 °F, rainy/humid; blossoms, wounds), UC IPM (75-85°F).
* Spreads fastest on lush nitrogen-pushed growth; avoid excess nitrogen: Clemson, UC IPM, UMN, UAEX ("discontinue fertilizer applications").
* "single biggest reason European pears fail in the humid South and East": UGA C742 (production relocated because of "the prevalence of fire blight in the humid eastern and southern states"), UAEX FSA6059 ("limits their use"; "the most serious pear disease in Arkansas").
* Prune out "at least 8 to 12 inches below visible symptoms": Clemson, printed exactly as "Pruning cuts of twigs and branches are made a minimum of 8 to 12 inches below any sign of infected tissue."
* Disinfect tools between cuts: Clemson (10% bleach or 70% alcohol), UGA, UAEX, UMN.
* "no cure once established" / "no spray that cures it": Clemson ("There is no cure for fire blight"); UGA ("Sprays will not control the disease in infected branches"); UC IPM (sprays "won't eliminate wood infections").
* Resistant cultivars BY NAME: Kieffer (Clemson 'Keiffer'; UAEX "High resistance"), Orient (Clemson; UGA; UAEX FSA6129), Moonglow (Clemson; UAEX), Ayers (Clemson; UAEX FSA6129 "moderately resistant"), Magness (Clemson; UAEX), Warren (UGA C742 "Resistant to blight" ONLY; not on Clemson or UAEX).
* Tolerant rootstock (OHxF series): WSU rootstocks.
* "prune only in dry weather": USU ("Do not prune during wet conditions"). Clemson's actual prescription is dormant-season pruning; UC IPM says summer or winter, with spring removal on pears "as soon as they appear"; UGA/UAEX/USU/UMN say remove promptly. The record's "in dry weather" sits between them and is USU-anchored.
* "follow a bloom-time forecast model where available": WSU Cougar Blight (commercial tool; no home document offers one).
RECORD CLAIMS WITH NO ANCHOR:
* "remove badly affected trees": only WSU (commercial) says to remove first-to-third-leaf trees; no home document read prescribes tree removal. Keep only if anchored to WSU and scoped to young trees.
* "a single warm, wet bloom can kill whole limbs or a young tree": the parts are anchored (Clemson: kills trees; UC IPM: "trees are more susceptible when young"), the "single bloom" framing is the record's own.
* beginner "about a hand's length past it" as the gloss for 8-12 inches: a hand is roughly 7 inches; it under-reads the anchor's minimum. Say "at least 8 to 12 inches, a foot to be safe".
RECORD CLAIMS THAT ARE WRONG: none refuted. Two tensions to carry into authoring:
* Kieffer's rating disagrees across T1: UAEX "High resistance", Clemson "moderately resistant", UGA C742 "Subject to blight in wet years". State it as "resistant" with the UAEX/Clemson anchors and do not call it immune.
* The pruning distance is published at five different figures: 6 in. (UGA pruner's note, UAEX FSA6059, UMN), 6-8 in. (UGA disease section), 8-12 in. minimum (Clemson), 12 in. (USU), 12-18 in. into 2-year wood (WSU, commercial), and UC IPM's "cut at the next branch juncture down". The record's 8-12 is the Clemson figure and is defensible; do not present it as the only published number.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry:
* Overwintering site: cankers ("The bacteria survive in the cankers", Clemson; WSU 7-62% of cankers carry live cells). Winter canker removal is the sanitation rung; late-dormant copper "can enhance orchard sanitation" (WSU, commercial).
* Vulnerable stage: open flowers until petal fall (UC IPM), plus late/rat-tail bloom; shoot infections through wounds (hail, insects). Do not irrigate during bloom (UC IPM, NC State ch. 15).
* Cultural rungs with home anchors: remove suckers/water sprouts (Clemson, UMN), no pruning in bloom to two weeks after (UMN), prune sparingly when blight is active (UAEX), stop fertilizing (UAEX), multi-leader training as insurance (NC State ch. 15, UAEX FSA6059), flower removal on young non-bearing trees (WSU, commercial).
* Soft-chemical rung: copper before bloom (Clemson: not after 1/2 inch green tip; UC IPM: weak Bordeaux during bloom every 4-5 days, 5-12 sprays on pear, russet risk; "often don't provide adequate control"). Streptomycin during bloom every 3-4 days (Clemson, home product named "Ferti-lome Fire Blight Spray", 50-day PHI; UAEX 5-day intervals). UAEX's home verdict: sprays are "difficult for homeowners to do and is not encouraged".
* Exact "not feasible" wording: "Adequate control of diseases and insects on large trees is usually not feasible, since complete coverage of the foliage with a pesticide cannot be achieved." (Clemson); "Copper products are the only chemical management available to homeowners, and they are difficult to time and apply effectively." (NC State ch. 15).
* Tool sterilizing: WSU's studies found it "made no difference ... as long as the cuts are made at the recommended distance"; UC IPM: "the location of the cut is far more important than the cleansing of tools". Keep the disinfection rung but rank the cut distance above it.
* Bartlett is highly susceptible (NC State home orchard; UGA "should not be planted in Georgia"). Most pear varieties "very susceptible" (UC IPM).
* Consumer-copy flag: symptoms_seasoned "Pear is markedly MORE susceptible than apple" uses all-caps emphasis in consumer prose.
PLA-457: none seen on the fire blight documents.

---

## Pear scab [diseases]  -- severity medium, type fungal
STATUS: SOURCED-OK
ORGANISM: Venturia pirina, per UC IPM PN 7413 (see the pests copy).
ANCHORS:
uc_ipm https://ipm.ucanr.edu/home-and-landscape/apple-and-pear-scab/ -- verified 2026-09-04 -- home (same document as the pests copy; the quotes above apply; the sentences that matter for this copy's wording:)
  > "Severely infected fruit becomes distorted and usually drops from the tree. Fruit also can crack"
  > "Both apple and pear scab pathogens overwinter primarily in infected leaves on the ground. ... Pear scab also can overwinter in lesions on pear twigs in high rainfall areas."
  > "European pear cultivars with negligible scab risk include Arganche, Barnett Perry, Batjarka, Brandy, Erabasma, Harrow Delight, Muscat, Orcas, and Passe Crassane."
RECORD CLAIMS THAT HOLD:
* Olive to black velvety lesions, corky/cracked, yellowing, defoliation, "scabby, misshapen fruit": PN 7413 ("distorted", "crack").
* Venturia pyrina, fallen-leaf overwintering, wet spring, wetness/temperature infection periods: PN 7413.
* Sulfur or labeled fungicide on a protective spring schedule; prevention beats cure: PN 7413.
* Rake and remove fallen leaves; choose less-susceptible varieties: PN 7413.
* Beginner "Sulfur spray in spring before the spots appear ... Once it is widespread it is too late for that year": PN 7413 ("It is difficult to prevent secondary fruit infections once primary infections occur").
RECORD CLAIMS WITH NO ANCHOR:
* "prune for airflow": as for the pests copy.
* prevention_beginner "Resistant varieties rarely need spraying": PN 7413 says the named cultivars have "negligible scab risk"; it does not say they need no spraying. Close enough to keep if reworded to "rarely get it".
RECORD CLAIMS THAT ARE WRONG: none.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry: identical to the pests copy (twig overwintering in wet climates, fungicide window, urea-only leaf treatment on pear, late-season tolerance).
Which copy is better anchored, claim by claim (both cite the same live document):
* symptoms: EQUAL. The diseases copy's "scabby, misshapen fruit" maps to "distorted"; the pests copy's "shoots" maps to "stems in severe cases". Prefer the diseases copy's shorter symptoms_seasoned, add "early defoliation" (both have it).
* cause: PESTS copy better. Its "Distinct from the apple-scab fungus but managed the same way" is carried verbatim by PN 7413 ("V. pirina won't affect apples nor can the apple scab fungus cause problems on pears" / "controlled in similar manners"); the diseases copy dropped that sentence.
* organic_treatment: EQUAL; the pests copy's "far easier to prevent than to cure once established" is the closer paraphrase of the anchor.
* prevention: EQUAL and both carry the unanchored "prune for airflow"; the diseases copy's beginner "Resistant varieties rarely need spraying" is the only sentence in either copy with no verbatim support.
* Verdict: keep the pests copy's cause_seasoned and organic_treatment_seasoned; keep the diseases copy's symptoms_*; drop or re-anchor "prune for airflow"; add the twig-overwintering clause for wet regions. Collapse to ONE entry with ONE id.
PLA-457: as for the pests copy (PN 7413 "never apply them within 3 weeks of an oil application").

---

## Fabraea leaf spot [diseases]  -- severity medium, type fungal
STATUS: ANCHOR-MISPOINTED (same two anchors as the pests copy: a fire-blight page with no leaf-spot content and a 404)
ORGANISM: Diplocarpon mespili (syn. Fabraea maculata; anamorph Entomosporium), per MSU / NETFMG / PSU / UGA PDL as quoted in the pests copy.
ANCHORS: identical to the pests copy (clemson_hgic HGIC 2208: 0 hits; ncsu_ext growing-pears-in-the-home-garden: 404). The live documents that carry this copy's specific sentences:
psu_ext https://extension.psu.edu/leaf-and-fruit-spot-of-pear-in-home-gardens -- verified 2026-09-04 -- home
  > "Lesions on twigs occur on current-season growth. They are purple to black with indefinite margins. The lesions can run together and form a superficial canker."
  > "or they can be produced in the previous season's shoot infections. Often, the first infections do not occur until mid-June to the first of July. Secondary infections begin about 1 month later and reoccur throughout the season during periods of rain."
msu_ext https://www.canr.msu.edu/ipm/diseases/fabraea_leaf_spot -- verified 2026-09-04 -- commercial, PROXY READ
  > "Removal or destruction of leaf litter can reduce early season disease pressure."
  > "most problematic in warm and humid production regions."
uga_ext https://fieldreport.caes.uga.edu/publications/C742/home-garden-pears/ -- verified 2026-09-04 -- home
  > "The two most common diseases are pear leaf spot and fire blight."
RECORD CLAIMS THAT HOLD:
* Many small dark purple-black spots on leaves and fruit through summer; early defoliation; pitted, cracked fruit: PSU, UGA, MSU.
* "the dominant summer foliar disease of pear in warm, humid regions": UGA C742 (Georgia: one of the two most common diseases), MSU (warm and humid regions). "Dominant" is a slight overreach of "most common"; "the most common summer leaf disease" is what UGA supports.
* Entomosporium mespili; overwinters in fallen leaves and twig lesions; warm rainy summer; intensifying late: PSU verbatim (twig lesions; mid-June onset; secondary a month later).
* Protective fungicide on a summer schedule where it recurs; rigorous fall leaf removal: PSU, NC State, UGA, MSU.
RECORD CLAIMS WITH NO ANCHOR:
* "resistant cultivars" / "pick a resistant variety in hot, humid areas": no named resistant European pear cultivar exists in any document read; NETFMG says all European varieties are susceptible. Same finding as the pests copy.
* "airflow pruning": as for the pests copy.
RECORD CLAIMS THAT ARE WRONG:
* prevention_seasoned "far less of a problem in arid and northern climates": the "northern" half is contradicted by PSU (routine sprays in Pennsylvania) and NETFMG ("Leaf and fruit infections are most notable in the Northeast and Midwest"); the "arid" half is unstated. Same defect as the pests copy's "far worse in the humid Southeast".
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry: as for the pests copy.
Which copy is better anchored, claim by claim:
* symptoms: DISEASES copy better. "through summer ... early defoliation ... pitted, cracked fruit" is fully carried by PSU; the pests copy's "(Bartlett, Bosc)" is refuted by MSU and NETFMG.
* cause: DISEASES copy better. "overwinters in fallen leaves and twig lesions ... intensifying late in the season" is PSU's exact disease cycle ("Lesions on twigs occur on current-season growth"; "previous season's shoot infections"; secondary infections "reoccur throughout the season"); the pests copy's "infected twigs" is equivalent but adds "(Fabraea maculata)", which is the PSU name and worth keeping in parentheses.
* organic_treatment: DISEASES copy better. "rigorous fall leaf removal to cut the overwintering inoculum" is MSU/NETFMG; both copies' fungicide sentence is equally carried.
* prevention: BOTH WRONG on the regional comparison; the pests copy's "far worse in the humid Southeast than in arid or northern regions" and the diseases copy's "far less of a problem in arid and northern climates" are the same unsupported claim. Neither copy's "resistant cultivars" has an anchor.
* Verdict: keep the diseases copy's symptoms_*, cause_*, organic_treatment_*; from the pests copy keep only the "(Fabraea maculata)" synonym and the beginner "It is a bigger problem in hot, humid areas" (MSU-anchored). Rewrite prevention_* in one place: fall leaf removal + prune out twig cankers (NETFMG "removing obvious cankers"), warm-humid-rainy region framing without a North comparison, and replace "choose a resistant variety" with "Bosc and Seckel are the most susceptible" (MSU, NETFMG). Collapse to ONE entry with ONE id.
PLA-457: as for the pests copy (NC State 10-day oil/sulfur sentence).

---

## Pear decline [diseases]  -- severity medium, type other
STATUS: ANCHOR-MISPOINTED (the cited page carries the rootstock claims and nothing else; etiology, vector, symptoms and management are on other pages, all found)
ORGANISM: 'Candidatus Phytoplasma pyri', per WSU FS376E ("Pear psylla also transmit a mycoplasma disease organism (Candidatus Phytoplasma pyri: Pear decline phytoplasma) through its saliva."), WSU Phytoplasmas and Viroids ("Causative Agent: Phytoplasma organism (Candidatus Phytoplasma pyri) Vector: Pear psylla, or by grafting infected material to healthy trees"), and USU ("Pear decline is caused by Candidatus Phytoplasma pyri transmitted by pear psylla.").
ANCHORS:
wsu_ext https://treefruit.wsu.edu/web-article/pear-rootstocks/ -- verified 2026-09-04 -- commercial (the record's current anchor; "decline" 4 hits, "phytoplasma" 0, "psylla" 0)
  > "OHxF 40 ... Resistant to fire blight, crown rot, woolly pear aphids, and pear decline."
  > "OHxF 87 (Brooks Selection, USPP#6392) OHxF 87 makes a tree slightly smaller than Bartlett on seedling root. It is considered a semi-dwarf tree. ... The OHxF selections are compatible with most pear varieties and are known for their tolerance to blight and decline."
  > "OHxF 97 A clonal rootstock of 'Old Home' x 'Farmingdale', this rootstock is resistant to pear decline and fireblight."
  > "OHxF 333 A semi-dwarfing pear rootstock. It is 1/2 to 2/3 standard size. Its resistance to fireblight, collar rot, woolly pear aphids, and pear decline make this a very healthy stock."
  > "Selections shown in purple text indicate possible susceptibility to pear decline." [figure key; the purple text itself is not in the page text]
uc_ipm https://ipm.ucanr.edu/agriculture/pear/pear-decline/ -- verified 2026-09-04 -- commercial (UC ANR 3455; biology and management usable)
  > "Pear Decline. A phytoplasma organism"
  > "Poor shoot and spur growth, dieback of shoots, premature reddening and upper rolling of leaves, reduced leaf and fruit size, and premature leaf drop are symptoms associated with pear decline."
  > "Sudden tree collapse can result from hypersensitive tissue damage at the graft union on highly susceptible Asian rootstocks such as Pyrus serotina or P. ussuriensis. Because of this rapid tree collapse, commercial pear varieties are no longer grafted on Asian rootstocks where pear psylla, which vectors the disease, is present."
  > "The more typical symptoms of pear decline on trees grafted to tolerant rootstocks is a very slow decline when trees are not receiving adequate water and nutrition. In addition, trees on tolerant rootstocks may show mild to moderate symptoms if very high psylla numbers occur, especially during the early growing season."
  > "The phytoplasma organism that causes pear decline is transmitted by pear psylla when feeding on pear foliage. An infected pear tree is the only known host from which uninfected pear psylla can acquire the pear decline phytoplasma. The expression of the disease depends on rootstock susceptibility, tree vigor, and psylla numbers."
  > "Commercial pear rootstocks currently available, with the exception of Pyrus calleryana, are essentially tolerant to pear decline and produce excellent crops in spite of recurring pear psylla populations and exposure to pear decline. Tolerant rootstocks include Bartlett seedling, Winter Nelis, Old Home x Farmingdale, and Pyrus betulaefolia. To keep the disease in remission on susceptible rootstocks: Control pear psylla. Maintain trees in good vigor"
  > "There is no known biological control of the pear decline phytoplasma organism. Indirectly, biological control of pear psylla can reduce disease severity."
wsu_ext https://treefruit.wsu.edu/crop-protection/opm/pear-psylla/ -- verified 2026-09-04 -- commercial (FS376E)
  > "Pear psylla also transmit a mycoplasma disease organism (Candidatus Phytoplasma pyri: Pear decline phytoplasma) through its saliva. The disease damages sieve tubes in the phloem. This damage prevents nutrients from moving down the tree and results in root starvation. Trees grafted on Ussurian pear (P. ussuriensis) and Asian pear (P. pyrifolia, synonymous with P. serotina) rootstocks are the most susceptible. Trees grafted on P. communis, P. betulifolia, P. calleryana, and Cydonia oblongata (quince) rootstocks become infected but are tolerant and display reduced decline symptoms"
wsu_ext https://treefruit.wsu.edu/web-article/phytoplasmas-and-viroids/ -- verified 2026-09-04 -- commercial
  > "Pear Decline. Causative Agent: Phytoplasma organism (Candidatus Phytoplasma pyri) Vector: Pear psylla, or by grafting infected material to healthy trees ... The roots of infected trees serve as a pathogen reservoir. Trees may experience a quick or slow decline that may be rootstock and stress related. Trees may wilt and die in a few weeks; or lose vigor over several years where the leaves may roll and turn red, and foliage becomes sparse. Leaves may drop prematurely. Management: Use resistant or tolerant rootstocks. Maintain good tree vigor with proper management. Remove infected trees and roots from orchards. Control pear psylla in trees."
uc_ipm https://ipm.ucanr.edu/home-and-landscape/pear-psylla/ -- verified 2026-09-04 -- home (the only HOME page found that describes pear decline)
  > "it vectors a microscopic, pathogenic phytoplasma that causes pear decline disease."
  > "Loss of tree vigor and premature tree death can occur from pear decline, a phytoplasma disease that develops after the psyllid injects its pathogen-contaminated saliva while feeding. Pear decline has varying effects on trees depending on plant care practices, variety, rootstock, quality of the growing site, and pear psylla abundance. Symptoms of pear decline include poor shoot and spur growth, dieback of shoots, reddening and upward rolling of leaves, reduced leaf and fruit size, and premature leaf drop. Sudden tree collapse can result on highly susceptible rootstocks."
  > "Keep trees growing vigorously with appropriate irrigation and fertilization to reduce the effect of pear psylla and pear decline."
usu_ext https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-decline -- verified 2026-09-04 -- commercial note (biology usable; "Information taken from the Pacific Northwest Plant Disease Management Handbook")
  > "Pear decline is caused by Candidatus Phytoplasma pyri transmitted by pear psylla. Grafting and budding can also transmit this phytoplasma. Decline is much more prevalent on trees with rootstocks of Pyrus ussuriensis or P. pyrifolia than on trees propagated on domestic P. communis roots."
  > "Trees may wilt, scorch, and die in a few weeks, or lose vigor over several seasons ... Leaves turn red early due to starch accumulation in the upper tree."
  > "On suspect trees, use a knife to expose the cambium (just under the bark) at the graft union to look for a brown line."
  > "Use resistant or tolerant rootstocks. ... Control pear psylla. ... Remove diseased trees"
usu_ext https://extension.usu.edu/planthealth/research/backyard-pear-pests -- verified 2026-09-04 -- home
  > "Pear psylla may also transmit a disease called "pear decline" that can slowly kill trees over a number of years."
RECORD CLAIMS THAT HOLD:
* Slow decline, weak growth, small leaves with reddish autumn color, reduced yield, or sudden collapse: UC IPM ag (verbatim symptom list), USU ("Leaves turn red early"), WSU phytoplasmas.
* Phytoplasma transmitted by pear psylla, expressed through a sensitive rootstock: UC IPM ag, WSU FS376E, USU.
* Decline-tolerant OHxF series, OHxF 87/97/333 by name: WSU rootstocks (87 "tolerance to blight and decline"; 97 "resistant to pear decline"; 333 "resistance to ... pear decline"); UC IPM ag ("Old Home x Farmingdale" tolerant).
* No cure; control the vector; choose a tolerant rootstock at planting; remove severely declining trees: UC IPM ag ("no known biological control"; "Control pear psylla"), WSU phytoplasmas ("Remove infected trees and roots"), USU ("Remove diseased trees").
* Avoid highly sensitive rootstocks: UC IPM ag (P. serotina, P. ussuriensis), WSU (P. ussuriensis, P. pyrifolia), USU.
* Beginner "sometimes a sudden collapse": UC IPM ag, WSU phytoplasmas ("wilt and die in a few weeks").
RECORD CLAIMS WITH NO ANCHOR:
* "(a bacteria-like organism)": no document read calls the pathogen a bacterium; the read vocabulary is "phytoplasma organism" (UC IPM, WSU), "mycoplasma disease organism" (WSU), "microscopic, pathogenic phytoplasma" (UC IPM home), "Candidatus Phytoplasma pyri" (WSU, USU). The one T1-hosted document whose TITLE states it, "PHYTOPLASMAS: Wall-Less Bacterial Pathogens of Plants" (R. E. Davis, USDA-ARS, hosted at caps.ceris.purdue.edu), was surfaced by search only and NOT read; caps.ceris.purdue.edu is a USDA CAPS site, so `purdue_ext` would be a stretch. The gloss is correct biology but presently unquoted.
RECORD CLAIMS THAT ARE WRONG: none refuted. One source disagreement the authoring pass must not paper over:
* Pyrus calleryana rootstock: UC IPM ag says commercial rootstocks are tolerant "with the exception of Pyrus calleryana"; WSU FS376E lists "P. calleryana" among rootstocks that "become infected but are tolerant". UAEX FSA6059 says "Most pear trees sold in Arkansas are budded onto Pyrus calleryana". Because the crop's own `recommended_rootstock_note` and the mid-South region both touch calleryana, this contradiction should be recorded, not resolved here.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry:
* Mechanism: phloem sieve-tube damage at the graft union, root starvation, starch backing up above the union (WSU FS376E, USU); diagnostic brown line at the graft union (USU).
* Graft-transmissible as well as psylla-transmitted (WSU, USU): matters for anyone topworking or taking scionwood.
* The pathogen is "crushed in the phloem during dormancy and then slowly recolonizes the upper canopy in spring", so HIGH psylla numbers in late spring/early summer speed decline even on tolerant rootstocks (UC IPM ag): the psylla ladder IS the decline ladder.
* Tolerant rootstock list beyond OHxF: Bartlett seedling, Winter Nelis, P. betulaefolia (UC IPM ag); P. communis, P. betulifolia, quince (WSU). Susceptible: P. ussuriensis, P. pyrifolia/serotina.
* Trees on tolerant roots "can recover if psylla density is low" (WSU psylla2) and decline is "very slow ... when trees are not receiving adequate water and nutrition" (UC IPM ag): vigor is a control rung.
* "No effective control" wording: "There is no known biological control of the pear decline phytoplasma organism." (UC IPM ag)
* Home anchor: UC IPM's home psylla page is the only home-register document that describes decline; a home-register "Pear Decline" page is listed on UC IPM's pear landing page but resolves to the commercial guideline.
* Consumer-copy flag: "phytoplasma" appears in symptoms_seasoned and cause_seasoned (seasoned register: acceptable); beginner copies use "tiny disease organism" (good).
PLA-457: none seen on the decline documents.

---

## SUMMARY

STATUS counts (8 sections): SOURCED-OK 3 (Pear scab x2, Fire blight); SOURCED-WEAK 1 (Codling moth: anchor is the commercial guideline, home PN 7412 carries everything and refutes one claim); ANCHOR-MISPOINTED 4 (Pear psylla: rootstock page has 0 psylla mentions; Fabraea leaf spot x2: a fire-blight page with 0 leaf-spot mentions plus a 404; Pear decline: rootstock page carries the rootstock claims only). UNSOURCED-NOT-FOUND 0; JOURNAL-ONLY 0; WRONG 0 as a whole-entry status, but FOUR individual claims are refuted by T1 text (Fabraea "(Bartlett, Bosc)"; Fabraea Southeast-versus-North gradient in both copies; codling moth trunk banding on pear; psylla dormant oil "smothers ... eggs").

Single most important finding: Fabraea leaf spot is anchored to two documents that do not carry it (Clemson HGIC 2208 fire blight, and an NC State URL that returns 404 on three paths), and inside that unanchored prose sit two wrong claims: Bartlett is named as a susceptible cultivar when MSU and the UMass guide both grade it the LESS susceptible one (Bosc and Seckel are the susceptible pair, and Seckel is on this crop's recommended list), and the "far worse in the Southeast than northern regions" framing is contradicted by Penn State (routine sprays in Pennsylvania) and the UMass guide ("Leaf and fruit infections are most notable in the Northeast and Midwest"). The claims that ARE true were found at T1 on the first hunt (Penn State home page, NC State home-orchard page, UGA C742, MSU), so this is a repoint-and-correct, not a downgrade. No admissible document names a Fabraea-resistant European pear cultivar; that rung has no anchor.

Duplicate verdicts (both pairs collapse to ONE entry each; the pests[] copies are the 2026-06-11 originals):
* Pear scab: both copies cite the same live PN 7413 and are equally anchored on symptoms; the PESTS copy is better on cause ("distinct from the apple-scab fungus but managed the same way" is verbatim in PN 7413) and on organic_treatment; the DISEASES copy is tighter on symptoms. Keep pests cause/organic + diseases symptoms; drop "prune for airflow" from both (no scab anchor); add twig overwintering for wet regions.
* Fabraea leaf spot: the DISEASES copy is better anchored on symptoms, cause and organic_treatment (PSU disease cycle, MSU sanitation); the pests copy's only unique keepers are the "(Fabraea maculata)" synonym and the beginner "bigger problem in hot, humid areas". Both copies' prevention is wrong on the regional gradient and unanchored on resistant cultivars; rewrite once.

Anchor repairs the authoring pass needs: Codling moth add uc_ipm PN 7412 (home) as primary, keep the ag page for biology only. Pear psylla replace the rootstocks URL with WSU FS376E (wsu_ext) + UC IPM home pear-psylla (uc_ipm) + USU backyard pear pests (usu_ext). Fabraea retire clemson_hgic (no HGIC pear leaf-spot document exists), repoint ncsu_ext to Disease and Insect Management in the Home Orchard, add psu_ext Leaf and Fruit Spot of Pear in Home Gardens and uga_ext C742; msu_ext only as a proxy-read corroboration; NETFMG needs `umass_ext` scope widening before use. Pear decline keep wsu_ext rootstocks for the OHxF claims and add uc_ipm agriculture/pear/pear-decline (biology) + WSU FS376E or phytoplasmas article (etiology/vector) + uc_ipm home pear-psylla (the only home page). Fire blight keep clemson_hgic; add uga_ext C742 for Warren and uada_ext FSA6059/FSA6129 for the cultivar ratings; UAEX page confirmed verbatim: "For pears try Harrow Delight, Maxine, Kiefer, Magness and Moonglow."

PLA-457 figures collected (not adjudicated): UC IPM PN 7413 "never apply them within 3 weeks of an oil application"; NC State home orchard "at least 10 days before or after a fungicide that contains sulfur or captan" and "DO NOT mix captan and or sulfur with oil"; UC IPM Pear PMG psylla "Sulfur and oil sprays can be very phytotoxic to pear trees, especially when the weather is hot" and lime sulfur + oil "any sooner than November 1"; WSU FS376E prescribes a COMBINED dormant "sulfur or lime sulfur application with oil"; PNW pear scab: lime sulfur "Do not use on 'd'Anjou', 'Comice' or 'Seckle' or with oil". The catalog's `horticultural_oil` entry currently says "Do not apply sulfur within 2 weeks of an oil spray".

## PROPOSED TYPE
* Codling moth [pests]: `insect` (Cydia pomonella, Lepidoptera; UC IPM PN 7412)
* Pear psylla [pests]: `insect` (Cacopsylla pyricola, Hemiptera: Psyllidae; WSU FS376E)
* Pear scab [pests]: `fungal` (Venturia pirina; UC IPM PN 7413)
* Fabraea leaf spot [pests]: `fungal` (Diplocarpon mespili, syn. Fabraea maculata, anamorph Entomosporium; MSU/NETFMG/PSU/UGA)
* Fire blight [diseases]: `bacterial` (Erwinia amylovora; Clemson HGIC 2208, WSU FS391E "gram-negative, rod-shaped bacterium")
* Pear scab [diseases]: `fungal` (Venturia pirina; same document; collapse with the pests copy)
* Fabraea leaf spot [diseases]: `fungal` (Diplocarpon mespili; collapse with the pests copy)
* Pear decline [diseases]: `bacterial` ('Candidatus Phytoplasma pyri', a wall-less bacterium in class Mollicutes). The current `other` is recognized by no gate. Support for `bacterial`: the taxon itself (the 'Candidatus' prefix is bacterial nomenclature) and the roster precedent that already types aster yellows `bacterial`. The source LANGUAGE on every document read stops at "phytoplasma organism" / "mycoplasma disease organism" / "microscopic, pathogenic phytoplasma"; no read sentence says "bacterium". If a quoted sentence is wanted, the USDA/Purdue CAPS document "PHYTOPLASMAS: Wall-Less Bacterial Pathogens of Plants" is the lead (unread, admission unclear).
