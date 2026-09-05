# PLA-8 batch 26 -- RECORD / SOURCE PASS: pear-asian

Canonical ce98b0a6 (READ-ONLY). Seven entries reviewed (4 pests, 3 diseases, one of them a duplicate).
All fetches 2026-09-04. Reviewer did NOT edit any repo file except this one; no git.

## FETCH PATHS (read this before trusting any quote below)

* `curl` via Bash was DENIED by the sandbox for every attempt, so no raw-HTML first-party read exists
  for any document. Every read below is WebFetch (first-party HTML through WebFetch's extractor,
  quotes requested verbatim and returned in quotation marks) unless marked PROXY (`r.jina.ai/` prefix
  through WebFetch, weaker evidence) or PDF (bytes retrieved by WebFetch, pages read as images with
  the Read tool: a first-party read of the printed page).
* Every quote marked `>` came back inside quotation marks from the extractor. Where the extractor
  paraphrased, the text is marked "(paraphrase)" and is NOT treated as published.
* DEAD / UNREADABLE this session (each tried on at least two paths):
  - `https://content.ces.ncsu.edu/growing-pears-in-the-home-garden` (record anchor, Stink bug): 404.
  - `https://content.ces.ncsu.edu/growing-pears-in-north-carolina`: 403 direct; PROXY returns "no
    longer available".
  - `https://content.ces.ncsu.edu/producing-tree-fruit-for-home-use`: 403 direct; PROXY "no longer
    available".
  - `https://treefruit.wsu.edu/crop-protection/disease-management/pear-decline/`: 404 (no WSU Tree
    Fruit pear-decline page exists; the content lives on the psylla page and the rootstock article).
  - `https://ipm.ucanr.edu/agriculture/pear/stink-bugs/`: "No record found. Page not published."
  - `https://ipm.ucanr.edu/home-and-landscape/pears/`: 404 (the landing page is `/pear/`, singular).
  - `https://hgic.clemson.edu/factsheet/stink-bugs/`: 404 (Clemson has no crop-agnostic stink bug
    factsheet; the BMSB sheet is HGIC 2404 "in Structures").
  - `https://extension.psu.edu/pear-disease-pear-decline`: 404.
  - `https://extension.okstate.edu/fact-sheets/growing-and-producing-pears-in-oklahoma.html`: 404.
  - `https://ucanr.edu/sites/fruitandnut/dsadditions/_Asian_Pears`: 403 direct and PROXY.
  - `https://pnwhandbooks.org/...` (four pages): 403 direct, readable only via PROXY. PNW Handbooks
    have NO admissible catalog key (`pnw_handbook_epn` is scoped to entomopathogenic-nematode safety),
    so every PNW citation below is NEEDS-CATALOG-ADMISSION and used as corroboration only.

Catalog keys used and their `citable_for` checked: `uc_ipm` (portal), `wsu_ext` (portal; covers
treefruit.wsu.edu and hortsense.cahnrs.wsu.edu), `clemson_hgic` (portal), `ncsu_ext` (portal),
`ncsu_ext_handbook_tree_fruit` (the one handbook chapter, cited only for that chapter), `osu_ext`
(Oregon State portal), `psu_ext` (portal), `purdue_ext` (portal), `usu_ext` (portal), `ucanr_ext`
(portal; the cert log already anchors this crop's pollination to the same Beutel brochure under this
key), `rutgers_njaes` (portal).

---

## Codling moth [pests]  -- severity high, type insect
STATUS: SOURCED-WEAK
ORGANISM: *Cydia pomonella*, per UC IPM PN 7412 ("Codling moth, _Cydia (Laspeyresia) pomonella_, is a
serious insect pest of apples, pears, and English walnuts.") and UC IPM ag pear page ("Cydia
pomonella"). The 1989 UC ANR brochure uses the retired synonym *Carpocapsa pomonella*.
ANCHORS:
uc_ipm https://ipm.ucanr.edu/agriculture/pear/codling-moth/ -- verified 2026-09-04 -- commercial
(the record's anchor; per-acre rates, "200-400 gal water/acre"; Varela et al., text updated 05/19)
  > "Stings are entries where larvae bore into the flesh a short distance before dying. Deep entries occur when larvae penetrate the fruit skin, bore to the core, and feed in the seed cavity."
  > "one or more holes plugged with frass on the fruit's surface"
  > "Females lay eggs singly on leaves and on fruit."
  > "Remove host trees in nearby abandoned orchards (apple, pear, and walnut) to destroy reservoirs of codling moth. Also remove props, picking bins, and fruit piles from the orchard."
  > "two to three generations of codling moth each year"
  > "time to egg hatch at 200 to 250 DD" ... "Make a second application 7 to 10 days later, a third application at 600 DD, and a fourth 7 days later for a total of 4 applications per flight." (Cyd-X)
  > "Tank mixing with oil increases efficacy: oil suppresses egg hatch and spinosad kills young larvae that ingest it."
  > "Kaolin clay (Surround)" (listed as organically acceptable; the only kaolin mention on either UC page)
uc_ipm https://ipm.ucanr.edu/home-and-landscape/codling-moth/ -- verified 2026-09-04 -- home (PN 7412;
NOT cited by the record; this is the document the ladder should be built from)
  > "Codling moth, _Cydia (Laspeyresia) pomonella_, is a serious insect pest of apples, pears, and English walnuts."
  > "Codling moth overwinters as full-grown larvae within thick, silken cocoons under loose scales of bark and in soil or debris around the base of the tree."
  > "Depending on the climate, codling moth can have two, three, and sometimes four generations per year."
  > "Codling moth can be very difficult to manage, especially if the population has been allowed to build up over a season or two. It is much easier to keep moth numbers low from the start than to suppress a well-established population."
  > "In most backyard situations, the best course of action might be to combine a variety of the nonchemical and/or low toxicity chemical methods discussed below."
  > "Removing infested fruit before the larvae are old enough to crawl out and begin the next generation can be a very effective method for reducing the population."
  > "It also is important to clean up dropped fruit as soon as possible after they fall, because dropped fruit can have larvae in them."
  > "Thin the fruit to one per cluster."
  > "Be sure to examine the fruit where it touches another fruit, as this is a common place to find an entry hole."
  > "Excellent control can be achieved by enclosing young fruit in bags right on the tree to protect them from the codling moth."
  > "Bagging should be done about four to six weeks after bloom when the fruit is from 1/2 to 1 inch in diameter."
  > "Bagging is the only nonchemical control method that is effective enough to be used alone and in higher population situations."
  > "It is difficult or impossible to bag certain varieties with very short stems such as Gravenstein. Also late-developing varieties might be attacked by codling moth even before they are 1/2 inch in diameter."
  > "A traditional, nonchemical method for controlling codling moth is to trap mature larvae in a cardboard band as they climb the trunk seeking a place to pupate."
  > "However, even in the best situations, banding will control only a very small percentage of the codling moth, because many pupate elsewhere on the tree or in the ground."
  > "Additionally, if bands aren't removed and destroyed in a timely fashion, they could increase the population, so banding no longer is recommended for control in home gardens."
  > "Codling moth pheromone traps are important for monitoring flight activity of moths to help time insecticide treatments."
  > "Hanging traps in each susceptible fruit or nut tree might help to reduce codling moth populations on isolated trees but isn't a reliable way to reduce damage."
  > "The most effective way to time insecticide sprays is with a pheromone trap and a degree-day calculation."
  > "Apply as soon as the eggs of the first generation codling moth hatch... this would be 200 to 250 degree-days after you begin regularly catching male moths."
  > "Recently a new biological insecticide, CYD-X, a granulosis virus that affects only larvae (caterpillars) of the codling moth, has become available to home gardeners in California."
  > "University of California trials have shown that this product, when applied weekly during egg hatch throughout the season, is as effective as carbaryl sprays at controlling codling moth."
  > "It doesn't affect other insects, humans, pets, or wildlife" (CYD-X)
  > "Spinosad is a biological product made from a naturally occurring bacterium called _Saccharopolyspora spinosa_."
  > "The first spring generation requires three sprays applied at 10-day intervals beginning at egg hatch... No more than six sprays should be applied per season, and they shouldn't be applied within seven days of harvest." (spinosad)
  > "It remains effective for 14 to 21 days, but it is very disruptive to natural enemies and honey bees." (carbaryl)
  > "Carbaryl never should be sprayed during bloom or when bees are present."
  Kaolin clay is NOT mentioned on PN 7412 (two independent reads).
clemson_hgic https://hgic.clemson.edu/factsheet/asian-pear/ -- verified 2026-09-04 -- home (HGIC 1352,
revised Jun 6 2024; Parker, Reighard, rev. Moore-Thomas; NOT cited anywhere on this crop)
  > "Codling moths and aphids are the most common insect problems in South Carolina."
ncsu_ext_handbook_tree_fruit https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts -- verified 2026-09-04 -- home
  > "Larvae tunnel inside the apple and pear fruits leaving frass-filled holes."
  > "Bagging individual fruit four weeks to six weeks after bloom provides excellent control"
  > "Removing infected fruit immediately from the tree and the ground to maintain orchard sanitation."
  > "If chemical management is warranted, apply when larvae have just emerged from the eggs."
ucanr_ext https://ucanr.edu/sites/sfp/pubs/brochures/Asianpears/ -- verified 2026-09-04 -- small-farm
brochure (Beutel, UC Davis, Jan 1989; commercial-leaning; the cert log already cites it for pollination)
  > "Codling moth _(Carpocapsa pomonella)_ is severe on Asian pears, requiring 3 to 4 well-timed sprays at or near full dosage for control."
ncsu_ext https://plants.ces.ncsu.edu/plants/pyrus-pyrifolia-nijisseiki/ -- verified 2026-09-04 -- toolbox
  > "Susceptible to Fire Blight and Codling Moth." (this one IS a prose sentence in the cultivar description, not only the linked-title row; the row also exists, per rule 7)
RECORD CLAIMS THAT HOLD: worm tunnels to core with frass-plugged hole (ag page stings/deep entries, frass
holes; NCSU handbook); dropped fruit carry larvae (PN 7412); *Cydia pomonella* (both UC pages); eggs on
fruit and leaves (ag page); two or more generations (PN 7412, ag page); same pest attacks apple (PN
7412 host sentence); pheromone traps to time control (PN 7412); remove dropped and infested fruit (PN
7412, NCSU); bag fruit (PN 7412, NCSU); spinosad timed to egg hatch (PN 7412); mating disruption at
larger scale (ag page); nearby abandoned host trees are reservoirs (ag page: REMOVE them); degree-day
timing (PN 7412 "200 to 250 degree-days" after first sustained catch); Asian pears are attacked (Beutel
"severe on Asian pears"; Clemson 1352 "most common"; NCSU toolbox Nijisseiki "Susceptible to ...
Codling Moth").
RECORD CLAIMS WITH NO ANCHOR: "often at the calyx end" (ag page says calyx entries are hard to detect,
per extractor paraphrase only); eggs laid "near bloom" (timing not quoted anywhere); "kaolin clay on a
degree-day/petal-fall schedule" (kaolin appears ONLY on the commercial page as an organically
acceptable material, with no schedule; PN 7412 omits it); "keep nearby abandoned pear or apple trees
pruned" (the document says remove, not prune).
RECORD CLAIMS THAT ARE WRONG: `prevention_seasoned` "band trunks to catch larvae seeking pupation
sites" and `prevention_beginner` "wrap a band of cardboard around the trunk to trap crawling
caterpillars" -- PN 7412: "banding will control only a very small percentage of the codling moth,
because many pupate elsewhere on the tree or in the ground" and "banding no longer is recommended for
control in home gardens." The record prescribes, in two fields, a method the home Pest Note retires.
BUNDLE / GENERIC VERDICT: n/a (one pinned organism).
LADDER-RELEVANT FACTS the record does not carry: overwintering site (cocoons under bark scales, soil,
debris at trunk base); "much easier to keep moth numbers low from the start"; bagging is the ONLY
nonchemical method that works alone at high pressure, and the bagging window is 4-6 weeks after bloom
at 1/2-1 inch fruit (late varieties can be hit before 1/2 inch); thin to one fruit per cluster and
inspect touching fruit; traps are monitoring, not control; CYD-X weekly through egg hatch, harmless to
non-targets, "as effective as carbaryl"; spinosad three sprays at 10-day intervals from egg hatch, six
per season max, 7-day PHI; carbaryl 14-21 days residual but "very disruptive to natural enemies and
honey bees" and never during bloom (the record's bee-safety line for any conventional rung must quote
this); the ag page's spinosad + oil tank-mix rationale; Beutel's "3 to 4 well-timed sprays" is the
commercial expectation for Asian pear specifically.
PLA-457: none seen (the ag page's oil sentence is an oil + spinosad tank mix, not sulfur).

## Pear psylla [pests]  -- severity high, type insect
STATUS: ANCHOR-MISPOINTED
ORGANISM: *Cacopsylla pyricola* (Foerster), per WSU Tree Fruit ("_Cacopsylla pyricola_ [Foerster]
[Hemiptera: Psyllidae]"), UC IPM ag ("_Cacopsylla (=Psylla) pyricola_") and UC IPM home ("_Cacopsylla
pyricola_"). Beutel 1989 uses the retired *Psylla pyricola*.
ANCHORS:
wsu_ext https://treefruit.wsu.edu/web-article/pear-rootstocks/ -- verified 2026-09-04 -- commercial
(the record's anchor). Two independent reads: the page contains NO occurrence of "psylla", no
honeydew, no oil, no natural enemies. It is a rootstock catalogue. It carries nothing in this entry.
wsu_ext https://treefruit.wsu.edu/crop-protection/opm/pear-psylla/ -- verified 2026-09-04 -- commercial
("Pear Psylla Integrated Pest Management"; DuPont, Nottingham, Orpet, Hilton, May 2022; addresses "pear
block[s]" and growers with "10 to twenty acres"; degree-day (PDD) timings and lb/acre rates)
  > "Honeydew, produced by nymphs, drips or runs onto fruit, causing dark, russet blotches or streaks and downgraded fruit."
  > "exacerbated by a sooty mold fungus that colonizes the honeydew and also marks fruit"
  > "In large numbers, pear psylla can stunt and defoliate trees and cause fruit drop...These symptoms, called psylla shock, are caused by toxic saliva from feeding nymphs."
  > "Pear psylla overwinter as winterform adults in a state of reproductive diapause. They begin laying eggs when pear buds begin to swell. First, eggs are deposited on the wood, generally at the base of fruit and leaf buds."
  > "Two to four summerform generations in most pear-growing regions, with generally two complete summerform generations occurring in Washington."
  > "Particle films reduce pear psylla adult colonization and egg lay by 80–100%, which reduces pear psylla pressure for the first generation." (Surround CF/WP or Celite 610 at 50 lb/acre, 75-100 PDD, renewed at 200 PDD; commercial timing)
  > "Important biological control organisms in Washington pear orchards are the parasitic wasp *Trechnites insidiosus*; true bugs *Deraeocoris brevis*, *Campylomma verbasci*, and *Anthocoris* spp.; lacewings *Chrysoperla carnea, Chrysopa nigricornis, Hemerobius* spp.; and the earwig *Forficula auricularia*."
  > "Prune between 2100–2400 PDD to remove nymphs before they molt into third generation adults."
  > ">0.3 pear psylla nymphs per leaf results in detectable fruit russet" (commercial threshold)
  > "Pear psylla also transmit a mycoplasma disease organism (_Candidatus Phytoplasma pyri_: Pear decline phytoplasma) through its saliva. The disease damages sieve tubes in the phloem."
  > "Trees grafted on Ussurian pear (_P. ussuriensis_) and Asian pear (_P. pyrifolia_...)" are "most susceptible" (to decline); "Most pears in Washington and Oregon are grafted to tolerant _P. communis_."
wsu_ext https://hortsense.cahnrs.wsu.edu/fact-sheet/pear-pear-psylla/ -- verified 2026-09-04 -- home
(WSU Hortsense, "Last review date: 2026-08-29 08:37"; no binomial given on the page)
  > "The brownish-gray adult pear psylla is about 1⁄10″ long, with clear wings held roof-like over the body."
  > "Honeydew may attract ants and often becomes covered with a growth of dark sooty mold."
  > "The pear psylla spreads the organism which causes pear decline."
  > "Several insect predators including green lacewings, ladybird beetles, and predaceous bugs help control pear psylla populations."
  > "Avoid use of broad-spectrum insecticides which kill beneficial insects."
  > "Prune lightly, supply moderate amounts of nitrogen, and remove water sprouts and suckers."
  > "Apply oil products during the delayed-dormant season."
  > "Apply kaolin clay, insecticidal soap, or neem during the growing season."
  > "Care should be taken in timing insecticide applications to early morning/late evening."
  > "Homeowners should not make foliar applications to trees over 10 ft. tall."
  Listed home products: Bug Buster-O (pyrethrins); Garden Safe Fungicide 3 (neem oil); Safer Brand Neem Oil; Safer Brand Insect Killing Soap (potassium salts of fatty acids); Azera Gardening (azadirachtin + pyrethrins).
uc_ipm https://ipm.ucanr.edu/home-and-landscape/pear-psylla/ -- verified 2026-09-04 -- home
  > "Nymphs of the psyllid excrete sticky honeydew that drips onto fruit. This induces the growth of black sooty mold that grows on the honeydew and causes fruit skins to become russeted (darkly discolored)."
  > "This causes portions of the leaf blade to blacken and affected leaves become yellow and sometimes drop prematurely."
  > "Adults overwinter in bark crevices, under bark scales of pear trees, or on the ground in organic litter or other places near pear trees."
  > "Pear psylla has about five generations per year in California" ... "Adult females begin laying eggs on or near fruit spurs starting in late January or early February."
  > "Apply horticultural oil at least once during the dormant season and by the beginning of January. If the psyllid and its damage have been abundant, make a second dormant treatment of oil just before bloom."
  > "Loss of tree vigor and premature tree death can occur from pear decline, a phytoplasma disease that develops after the psyllid injects its pathogen-contaminated saliva while feeding."
  > "Pear psylla is a greater problem on European varieties than on Asian varieties of pear."
  Also lists, for home use, "Abamectin plus horticultural [oil] applied at petal fall" and "a systemic neonicotinoid such as imidacloprid" (conventional rungs; no soap/kaolin/natural-enemy sentences on this page).
uc_ipm https://ipm.ucanr.edu/agriculture/pear/pear-psylla/ -- verified 2026-09-04 -- commercial (UC ANR
Pub 3455; Varela, Elkins, Van Steenwyk, Ingels; text 11/12, table 02/25)
  > "There are many naturally occurring predators and parasites of pear psylla including green lacewings, brown lacewings, and minute pirate bugs. Nonselective codling moth insecticides destroy many of these beneficials, resulting in outbreaks of this pest."
  > "Honeydew, produced by psylla nymphs as they feed, drops onto fruit. A black sooty mold grows on the honeydew and the fruit skin russets"
  > "Apply during warm, sunny weather from leaf fall to start of egg laying for best results" (dormant oil) ... "Apply prebloom; may cause mite outbreaks when used later in season." (kaolin)
  > "Pear psylla is a greater problem on European varieties than on Asian varieties."
osu_ext https://extension.oregonstate.edu/catalog/pub/ec631 -- verified 2026-09-04 -- home (EC 631
"Managing diseases and insects in home orchards", Hilton, 2014-12-18; PROXY read after a 301 + 403)
  > prepink: "insecticidal soap, kaolin, or neem"; petal fall: "insecticidal soap or neem"; summer to harvest: "esfenvalerate, insecticidal soap, kaolin, or neem" (pear psylla rows)
ucanr_ext https://ucanr.edu/sites/sfp/pubs/brochures/Asianpears/ -- verified 2026-09-04 -- small-farm brochure
  > "Pear psylla _(Psylla pyricola)_ can cause sticky fruit and requires at least one delayed dormant spray."
RECORD CLAIMS THAT HOLD: honeydew, sooty mold, russet (UC IPM home, WSU, Hortsense); leaf blackening
and premature drop (UC IPM home); tree decline (WSU "psylla shock"; UC IPM home pear decline); tiny
insects clustering on shoots (WSU eggs at bud bases; Hortsense size); *Cacopsylla pyricola*;
overwinters as an adult (UC IPM home bark crevices/litter; WSU winterform diapause); several
overlapping generations (UC IPM home ~5; WSU 2-4); outbreaks follow broad-spectrum sprays (UC IPM ag
"Nonselective codling moth insecticides destroy many of these beneficials, resulting in outbreaks";
Hortsense "Avoid use of broad-spectrum insecticides"); dormant oil (UC IPM home: by early January,
second just before bloom if heavy; Hortsense: delayed-dormant; Beutel: at least one delayed dormant
spray); in-season insecticidal soap (Hortsense; EC 631); conserve anthocorids and lacewings (WSU
*Anthocoris* spp., *Chrysoperla carnea*; Hortsense lacewings); kaolin deters egg-laying (WSU 80-100%
reduction in colonization and egg lay, commercial timing; Hortsense/EC 631 list kaolin in season);
avoid lush nitrogen growth (Hortsense "supply moderate amounts of nitrogen, and remove water sprouts").
RECORD CLAIMS WITH NO ANCHOR: "summer oil" in season (no home document read lists it; UC IPM ag warns
kaolin "may cause mite outbreaks when used later in season" and puts oil at dormant/prebloom); "specific
to pear" (true by every host list read, but not stated as a sentence); "the signature pear pest" (an
editorial claim; on THIS crop the sources say the opposite, see next line).
RECORD CLAIMS THAT ARE WRONG: none refuted as written, but the record's severity "high" and "the
signature pear pest" on the Asian pear record are contradicted in weight by UC IPM (home AND ag): "Pear
psylla is a greater problem on European varieties than on Asian varieties of pear." The entry is
byte-identical to pear-european's (template inheritance); its severity was never adjudicated for
Asian pear. Clemson's Asian pear factsheet names codling moth and aphids as the common insects and
does not mention psylla at all.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry: overwintering site is bark crevices/litter AT the
pear tree (UC IPM home), so dormant oil reaches it; eggs start at bud swell (WSU) / late Jan-Feb in CA
(UC IPM home); psylla shock; the Hortsense 10-ft rule and early-morning/late-evening timing; Hortsense
product list; EC 631 prepink / petal fall / summer soap-kaolin-neem rows; UC IPM home conventional
rungs (abamectin + oil at petal fall; imidacloprid); WSU natural-enemy names; the commercial
monitoring threshold (0.3 nymphs/leaf = russet) is NOT home advice; the disease-vector role (pear
decline) is the reason psylla matters at all on a tolerant rootstock.
PLA-457: three documents state oil/sulfur constraints, none an interval:
  - WSU Tree Fruit psylla page: "A sulfur or lime sulfur application with oil can also suppress pear rust mites and spider mites in addition to pear psylla adults." (a COMBINED application, no spacing)
  - UC IPM ag pear psylla: "Do not apply lime sulfur and oil spray any sooner than November 1." (a calendar restriction on the combined spray, not an interval)
  - OSU EC 631: "Soaps and oils are not compatible with sulfurs. Mixing them together or using one right after the other can cause plant damage." (no number)

## Stink bug [pests]  -- severity medium, type insect
STATUS: ANCHOR-MISPOINTED (both anchors); claims then found at T1 on five home documents.
ORGANISM: umbrella -- multiple organisms, and the sources themselves keep it an umbrella. Brown
marmorated stink bug *Halyomorpha halys* Stål (WSU Tree Fruit BMSB page: "_Halyomorpha halys_ Stål
(Heteroptera: Pentatomidae)"; Clemson HGIC 2404: "Halyomorpha halys (Stål)"); consperse stink bug
*Euschistus conspersus* (UC IPM home Stink Bugs page; PNW pear stink bug page); *Acrosternum* spp. and
*Euschistus* spp. on pome fruit (Clemson HGIC 2001). NC State groups the damage class as "lygus bug,
stink bug, tarnished plant bug, and boxelder bug"; Beutel: "Many types of stink bugs and plant bugs".
ANCHORS:
clemson_hgic https://hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ -- verified 2026-09-04 -- home
(record anchor). Read twice; stink bugs: "None mentioned on this page." The only insects on the page are
fire blight vectors ("Honeybees can carry and spread the fire blight bacteria during pollination";
"ants, flies, aphids, and beetles"). Carries NOTHING in this entry.
ncsu_ext https://content.ces.ncsu.edu/growing-pears-in-the-home-garden -- record anchor -- 404 (dead).
wsu_ext https://hortsense.cahnrs.wsu.edu/fact-sheet/pear-brown-marmorated-stink-bug/ -- verified 2026-09-04
-- home (WSU Hortsense "Pear: Brown marmorated stink bug", last review 2026-08-29; THE pear-specific
home document; no binomial on the page)
  > "Sunken areas and deformities (catfacing) on the surface of the fruit are typical symptoms on damaged apples and pears. Damaged areas are discolored beneath the fruit's skin and become hard and pithy or corky in texture."
  > "BMSB damage that occurs close to harvest time may not be apparent, but the damaged fruit will come out of storage with brown spots."
  > "Adults overwinter in sheltered locations (including houses, where they can become a significant nuisance pest)."
  > "One or two generations of BMSB per year" (PNW) ... eggs "in groups of about 20 to 30 on the underside of leaves"
  > "Pick and destroy BMSB egg masses or groups of young nymphs" (by "net-sweeping, plant vacuuming or shaking")
  > "Some natural enemies feed on BMSB, including domestic chickens, praying mantids, and other predaceous insects."
  > "While natural enemies may not be sufficient to provide complete control, avoid use of broad-spectrum insecticides which would harm populations of beneficial insects."
  > "When practical, plants may be screened with a floating row cover or similar barrier."
  > "Chemical management of BMSB is most effective against very young nymphs (immature insects). Chemical management is NOT RECOMMENDED FOR ADULT INSECTS."
  > "CAUTION: These pesticides are toxic to bees." Listed: Ortho BugClear (bifenthrin, zeta-cypermethrin; EPA 239-2718); Azera Gardening (azadirachtin, pyrethrins; EPA 1021-1872).
uc_ipm https://ipm.ucanr.edu/home-and-landscape/stink-bugs/ -- verified 2026-09-04 -- home (names pear)
  > "The surface of feeding spots can become discolored and tissue beneath feeding spots on fruit (e.g., apples, pears, and tomatoes) becomes pithy and brown or white and remains firm as the fruit ripens."
  > "Overwintering is on the ground in liter." (sic, "litter")
  > "Eliminate groundcovers and other herbaceous vegetation such as weeds in early spring before stink bugs become abundant there and then move to alternative hosts."
  > "Handpick the bugs and their eggs from small plants."
  > "Insecticides are generally not recommended in gardens and landscapes for stink bugs. Commonly stink bug feeding damage does not become apparent until after plant tissues grow, by which time the stink bugs may no longer be present."
  Species named: *Euschistus conspersus*, *Halyomorpha halys*, *Nezara viridis* [sic], *Chlorochroa sayi*, *Murgantia histrionica*, *Bagrada hilaris*.
ncsu_ext_handbook_tree_fruit https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts -- verified 2026-09-04 -- home
  > "Catfacing is the pitting and fruit deformity caused by adult insects with piercing-sucking mouthparts, such as lygus bug, stink bug, tarnished plant bug, and boxelder bug. These insects damage both pome and stone fruits. Weeds are the primary food source for these insects, so keeping weeds to a minimum around the orchard will help manage populations. Several parasitic wasps and predatory insects, such as big-eyed bugs, assassin bug, damsel bugs, and crab spiders, attack these insects. Reducing the use of broad spectrum insecticides helps these biological predators keep pest populations in check."
ucanr_ext https://ucanr.edu/sites/sfp/pubs/brochures/Asianpears/ -- verified 2026-09-04 -- small-farm brochure
  > "Many types of stink bugs and plant bugs cause injury as hard, tan-colored spots under the flesh of Asian pears."
clemson_hgic https://hgic.clemson.edu/factsheet/apple-crabapple-insects/ -- verified 2026-09-04 -- home (HGIC 2001, May 23 2025; pome fruit)
  > "Stink bugs (_Acrosternum_ species and _Euschistus_ species) will both feed on the young fruit."
  > "As the bugs penetrate the fruit with their needle-like mouthparts, they inject saliva that kills the plant cells around the puncture. They then suck the juices from the fruit. As the fruit continues to grow, depressed areas appear around the feeding sites."
  > "Keeping early-blooming weeds cut in the area where the apple trees are growing reduces the number of plant bugs."
  > "Homeowners use sprays of cyhalothrin (gamma or lambda) or zeta cypermethrin for controlling these pests."
wsu_ext https://treefruit.wsu.edu/crop-protection/opm/brown-marmorated-stink-bug/ -- verified 2026-09-04 -- commercial (Beers & Marshall, 2017)
  > "while pears have been less studied in the eastern US, they also appear to be at risk."
  > "They are best known for their habit of overwintering in human habitations (houses, sheds, or barns), often in huge numbers."
  > "It is also considered a border pest as it invades orchard edges from nearby crops and wooded areas."
  > "In apples, a brownish depression may form around the feeding site. Damage may be visible at harvest, but becomes even more apparent during long-term storage."
  > "An exotic parasitoid, _Trissolcus japonicus_ (the samurai wasp) has very high rate of parasitism of brown marmorated stink bug, and is considered the most promising candidate for importing into the US in a classical biological control program."
psu_ext https://extension.psu.edu/tree-fruit-insect-pest-brown-marmorated-stink-bug -- verified 2026-09-04 -- commercial
  > "Early feeding injury can result in misshapen fruit, while late season feeding on maturing fruit can cause the formation of necrotic tissue (corking) close to the skin surface."
  > "Overwintering BMSB adults emerge from their winter hideouts in early spring to mid-June and immediately move to feed on available hosts."
  > "Starting from mid-July, should help with effective monitoring of BMSB adults and nymphs in orchards."
osu_ext EC 631 (above) -- home: BMSB row lists "Carbaryl, gamma-cyhalothrin, lambda-cyhalothrin, permethrin, bifenthrin, acetamiprid, kaolin (suppression), or malathion".
rutgers_njaes https://pemaruccicenter.rutgers.edu/programs/entomology/pest-management-information/brown-marmorated-stink-bug/ -- verified 2026-09-04 -- commercial (Polk, Rodriguez-Saona)
  > "they are heavily biased towards edge and border rows. In tree fruit this has resulted in higher populations near wooded borders and soybean fields."
NEEDS-CATALOG-ADMISSION: PNW Insect Management Handbook "Pear - Stink bug"
https://pnwhandbooks.org/insect/tree-fruit/pear/pear-stink-bug (PROXY): names consperse stink bug
*Euschistus conspersus* and BMSB; "depressions and corky areas"; stink bugs "may migrate into the
orchard and feed on the fruit" when broadleaf weeds dry; "a weed free orchard groundcover will deter
stink bugs" but do not mow while bugs are active (disperses them); pyrethroids "can disrupt naturally
occurring biological control".
RECORD CLAIMS THAT HOLD: BMSB included and *Halyomorpha halys* (Hortsense pear page; WSU); dimpled /
catfaced fruit with hard corky pithy brown flesh (Hortsense; UC IPM home; PSU "corking"); skin near
normal while flesh is pitted (Hortsense storage sentence; PSU corking "close to the skin surface");
worst near weedy and woodland borders (WSU "border pest"; Rutgers; NCSU "Weeds are the primary food
source"); several native stink bugs plus BMSB (all five umbrella documents); adults and nymphs feed
(Hortsense "Both life stages" per extractor; Clemson 2001); kaolin deters (EC 631 "kaolin
(suppression)"); clear weedy/brushy borders (UC IPM home; NCSU; Clemson 2001); hand-pick (Hortsense;
UC IPM home); conserve natural enemies / avoid broad-spectrum (Hortsense; NCSU); product timed to
nymphs (Hortsense "most effective against very young nymphs").
RECORD CLAIMS WITH NO ANCHOR: "feed on fruit from petal fall through harvest" (no document states the
window; PSU puts orchard monitoring from mid-July); "trap adults" / "monitor with traps from bloom on"
(traps are commercial pheromone monitoring on WSU/PSU; no home document recommends trapping; UC IPM
home says damage shows after the bugs have left); "bagging individual fruit excludes them" (Hortsense
says floating row cover / barrier; fruit bagging for stink bug is not on any page read); "hard ...
brown" (UC IPM home says "pithy and brown or white").
RECORD CLAIMS THAT ARE WRONG: none refuted outright. The two ANCHORS are wrong (one dead, one a fire
blight page), which is the finding.
BUNDLE / GENERIC VERDICT: genuine umbrella. Every home document read treats "stink bugs" as a class
(Hortsense singles out BMSB on pear; UC IPM home names six species; Clemson names two genera; NC
State names four catfacing bug groups). Keep one entry named for the class, name BMSB inside it, and
pin *Halyomorpha halys* + *Euschistus conspersus* in the cause text. Do not split.
LADDER-RELEVANT FACTS the record does not carry: UC IPM's "Insecticides are generally not
recommended in gardens and landscapes for stink bugs" (the exact wording of the no-spray position);
Hortsense's "NOT RECOMMENDED FOR ADULT INSECTS" and "CAUTION: These pesticides are toxic to bees."
for both listed products; damage near harvest is invisible until storage; adults overwinter in houses
and sheds (not in the orchard), so sanitation under the tree does nothing for BMSB; native species
overwinter "on the ground in liter" (UC IPM); weed removal must happen "in early spring before stink
bugs become abundant there" (UC IPM), and PNW warns mowing while bugs are active disperses them into
the tree; NCSU's named native predators; the samurai wasp is a classical-biocontrol program, not a
home tool; Clemson's home conventional rung is cyhalothrin or zeta-cypermethrin (apple sheet).
PLA-457: none seen.

## Pear scab [pests]  -- severity medium, type fungal   (the older copy, entered 2026-06-11; sits in pests[])
STATUS: SOURCED-WEAK
ORGANISM: *Venturia pirina* per UC IPM PN 7413 ("Pear scab, which the fungus _V. pirina_ causes, results
in similar blemishes on pear fruit.") and UC IPM ag pear scab ("_Venturia pirina_"); spelled *Venturia
pyrina* by the PNW handbook. The record's "Venturia pyrina" is a valid variant, but the cited anchor
spells it "pirina".
On *V. nashicola*: the cited UC IPM document does NOT name it. It names one pear scab fungus (V. pirina)
and says of Asian pear only: "Because Asian pears (_Pyrus pyrifolia_) are a different species, they are
less susceptible to scab than European pears (_P. communis_)." So the anchor covers Asian pear in ONE
sentence, and that sentence says the disease matters less on this crop. The Asia/US species split is
carried by: PNW Plant Disease Handbook pear scab (PROXY; NEEDS-CATALOG-ADMISSION): "scab on Asian pear
is also caused by a different species, V. nashicola, that has not been reported in the Pacific
Northwest."; UC ANR Beutel 1989 (ucanr_ext): "Also, scab is a problem in Japan, but it is not the same
scab species found in California on Bartlett pears and apples."; and peer-reviewed literature
(JOURNAL-ONLY leads, not read in full: APS Phytopathology 2020 "Pathogenic Specialization of Venturia
nashicola"; MPMI 2019 genome resource) stating V. nashicola is restricted to Asia and V. pirina to
European pear.
ANCHORS:
uc_ipm https://ipm.ucanr.edu/home-and-landscape/apple-and-pear-scab/ -- verified 2026-09-04 -- home
(PN 7413, updated 01/2011; the record's anchor for both copies)
  > "The fungus _Venturia inaequalis_ causes apple scab" ... "Pear scab, which the fungus _V. pirina_ causes, results in similar blemishes on pear fruit."
  > "Because Asian pears (_Pyrus pyrifolia_) are a different species, they are less susceptible to scab than European pears (_P. communis_)."
  > "Scab first appears as yellow, or chlorotic, spots on leaves. As the disease progresses, dark, olive-colored spots form on leaves"
  > "Scabby spots can appear on fruit later in the season. These begin as velvety or sooty, gray-black (and sometimes greasy looking) lesions that sometimes have a red halo."
  > "Fruit also can crack, which allows entry of secondary organisms."
  > "Severely affected leaves often turn yellow and drop."
  > "Both apple and pear scab pathogens overwinter primarily in infected leaves on the ground."
  > "Pear scab also can overwinter in lesions on pear twigs in high rainfall areas."
  > "Infection occurs most rapidly between 55° and 75°F, and leaves or fruit must remain wet continuously for a minimum of 9 hours for initial infection."
  > "For a single, backyard tree, removing—then composting or destroying—its dropped leaves in autumn or winter can limit the disease to tolerable levels. In plantings of several trees, additional steps might be necessary to effectively control this disease, especially in cool, moist coastal areas. These include applying zinc and fertilizer-grade urea (or some other nitrogen source) to leaves in autumn to hasten leaf fall and adding lime to leaf piles beneath the tree. In pears, apply urea by itself, because zinc can be phytotoxic. If you are using sprinklers that wet any of the tree's foliage, irrigate between sunrise and noon to allow adequate drying time, or reduce the angle of the sprinkler."
  > "European pear cultivars with negligible scab risk include Arganche, Barnett Perry, Batjarka, Brandy, Erabasma, Harrow Delight, Muscat, Orcas, and Passe Crassane."
  > "Fungicide sprays are necessary only if the weather is rainy and leaves are likely to remain wet for 9 or more hours. Fungicide applications require careful attention to timing, as preventing early infection is the most important step toward successfully controlling later fruit infections."
  > "If treatments are needed, the generally recommended time is between when buds begin to break and a month after petal fall"
  > "A second application might be needed 10 to 14 days later if it is still rainy, once you can see blossom clusters but before they have opened."
  > "These include fixed copper, Bordeaux mixtures, copper soaps (copper octanoate), sulfur, mineral or neem oils, and myclobutanil."
  > "When using sulfur-containing compounds such as wettable sulfur, never apply them within 3 weeks of an oil application or when temperatures are near or higher than 90°F."
  The cultural-control section contains NO pruning-for-airflow sentence (two reads).
uc_ipm https://ipm.ucanr.edu/agriculture/pear/pear-scab/ -- verified 2026-09-04 -- commercial (Elkins, Gubler, Adaskaveg; 11/12; per-acre rates)
  > "Scab first appears as velvety, dark olive-to-black spots on fruit, leaves, and stems."
  > "puckering and twisting and eventually tearing with age" (leaves); secondary infections "black pinpoint spots"; early fruit infection "scablike and misshapen" (extractor fragments)
  > Mills table: wetness needed ranges from 48+ hours at 33-41°F to 9 hours at 66-75°F; lime sulfur at delayed dormant; protective program from green tip at 7-10 day intervals (commercial)
  > "Do not apply within 3 weeks of an oil application" (sulfur)
osu_ext EC 631 -- home: scab rows prepink / pink / petal fall "Bonide Fruit Tree and Plant Guard"; leaf fall: "Rake and dispose of leaves by burning, burying, or completely composting"
ucanr_ext Beutel 1989: "Also, scab is a problem in Japan, but it is not the same scab species found in California on Bartlett pears and apples."
NEEDS-CATALOG-ADMISSION: PNW Plant Disease Handbook "Pear (Pyrus spp.)-Scab" (PROXY): "Venturia pyrina,
a fungus that overwinters in infected fallen leaves and, in some areas, on pear twigs"; "scab on Asian
pear is also caused by a different species, V. nashicola, that has not been reported in the Pacific
Northwest"; cultural: urea on leaves in fall, shred leaves, "Pruning infected twigs", dolomitic lime
after leaf drop, reduce irrigation wetting. PNW Asian cultivar table (PROXY) carries a Scab column
(Chojuro R, Hosui R, Niitaka R, Nijisseiki S, Shinko S, Shinseiki S, Kosui S) without saying which
*Venturia* it rates.
RECORD CLAIMS THAT HOLD: olive to black velvety spots on leaves, shoots and fruit (PN 7413 leaves/
fruit; ag page "fruit, leaves, and stems"; PN 7413 twig lesions); fruit cracks (PN 7413); leaf yellowing
and early drop (PN 7413); analog of apple scab (PN 7413 treats both, "similar blemishes"); *Venturia*
species distinct from apple scab (PN 7413 names two species); overwinters in fallen leaves (PN 7413);
wet spring infection set by wetness and temperature (PN 7413 9 h, 55-75°F); sulfur on a protective
schedule (PN 7413 lists sulfur; bud break to a month after petal fall); prevention beats cure (PN 7413
"preventing early infection is the most important step"); rake and remove fallen leaves (PN 7413; EC
631); "managed the same way" (one page, one program).
RECORD CLAIMS WITH NO ANCHOR: "prune for airflow" (absent from PN 7413; PNW says prune INFECTED TWIGS,
a different reason); "corky" (PN 7413 says velvety/sooty, cracked; ag page "scablike"); "choose
less-susceptible varieties" is anchored only for EUROPEAN cultivars (PN 7413's list) -- no admissible
document names a scab-resistant ASIAN cultivar.
RECORD CLAIMS THAT ARE WRONG: none as sentences, but severity "medium" on Asian pear contradicts the
anchor's only Asian-pear sentence ("less susceptible to scab than European pears") and the two
documents stating the Asian pear scab fungus is not present in the US West (PNW, Beutel). The record
also omits the twig-lesion overwintering PN 7413 adds for high-rainfall areas.
BUNDLE / GENERIC VERDICT: n/a; but this entry is a DUPLICATE of the diseases[] entry below and sits in
the wrong array (a fungus in pests[]).
LADDER-RELEVANT FACTS the record does not carry: the single-backyard-tree sentence (leaf removal
alone "can limit the disease to tolerable levels"); "Fungicide sprays are necessary only if the weather
is rainy and leaves are likely to remain wet for 9 or more hours"; urea alone on pears (zinc is
phytotoxic on pear); sprinkler timing; the home product list (fixed copper, Bordeaux, copper soap,
sulfur, mineral or neem oil, myclobutanil); first spray at bud break, second 10-14 days later if
still rainy, stop a month after petal fall; twig lesions in high-rainfall areas are an overwintering
site leaf raking does not reach; EC 631's leaf-fall raking row; Asian pears are less susceptible as a
species (this should be the lead sentence of the rewritten entry).
PLA-457:
  - UC IPM PN 7413 (home): "When using sulfur-containing compounds such as wettable sulfur, never apply them within 3 weeks of an oil application or when temperatures are near or higher than 90°F."
  - UC IPM ag pear scab (commercial): "Do not apply within 3 weeks of an oil application" (sulfur; extractor fragment)
  - PNW pear scab (PROXY, not admissible): sulfur label note "Do not use on 'd'Anjou', 'Comice' or 'Seckle' or with oil."
  - OSU EC 631 (home): "Soaps and oils are not compatible with sulfurs. Mixing them together or using one right after the other can cause plant damage."

## Fire blight [diseases]  -- severity high, type bacterial
STATUS: SOURCED-WEAK (anchor carries pathogen, symptoms, the 8-12 inch minimum, tool disinfection and
nitrogen; it does NOT carry the Asian-cultivar susceptibility claims, the rootstock claims, "dry
weather" or the forecast model; one cultivar claim has no source at all; one beginner figure
understates every published number)
ORGANISM: *Erwinia amylovora*, per Clemson HGIC 2208, UC IPM PN 7414, Purdue BP-30-W, WSU ("a
gram-negative, rod-shaped bacterium").
ANCHORS:
clemson_hgic https://hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ -- verified 2026-09-04 -- home
(HGIC 2208, updated July 18 2025; Doubrava & Blake; the record's anchor)
  > "_Erwinia amylovora_"
  > "Infected flowers turn black and die"; "Leaves on affected branches wilt, blacken, and remain attached"; "Slightly sunken areas, called cankers, appear on twigs"; shepherd's crook (named)
  > "Prune out blackened twigs and branches with cankers during the dormant season. Pruning during the growing season may spread the disease."
  > "Pruning cuts of twigs and branches are made a minimum of 8 to 12 inches below any sign of infected tissue."
  > "Disinfect, all pruning tools between cuts using a 10% bleach solution (1 part household bleach to 9 parts water) or 70% alcohol."
  > "Avoid excess nitrogen fertilization, which results in excess succulent growth, because if injured, succulent new growth is easily infected."
  > "There is no cure for fire blight, making disease prevention extremely important."
  > "One spray of a copper fungicide is applied immediately prior to bloom."
  > "The recommended bloom spray bactericide for susceptible apple trees is streptomycin. The first spray is applied at the beginning of bloom. Repeat this spray every 3 to 4 days, as long as flowers are present." (product: Ferti-lome Fire Blight Spray) -- written for APPLE
  > "Moderately resistant edible pears include 'Ayers', 'Keiffer', 'LeConte', 'Moonglow', 'Magness', 'Orient', 'Seckel' (somewhat resistant)."
  > "Asian pears that have some resistance to fire blight include: 'Chojuro', 'Hosui' (somewhat resistant), 'Seuri', 'Shinko'."
  > "Honeybees can carry and spread the fire blight bacteria during pollination."
  The page names NO cultivar as highly susceptible, and no rootstock.
clemson_hgic https://hgic.clemson.edu/factsheet/asian-pear/ -- verified 2026-09-04 -- home (HGIC 1352,
rev. Jun 6 2024; NOT cited by the record; the crop-specific home document)
  > "Asian pears _(Pyrus pyrifolia_) are known by many names—including Chinese, Japanese, Oriental, sand, and apple pear."
  > "Fire blight, caused by a bacterium, is the most significant problem limiting the production of Asian pears."
  > "To help manage this disease, selecting resistant cultivars, adopting suitable sanitary measures, and avoiding excess nitrogen fertilization are essential."
  > "Prune infected branches 18 inches below the affected area and burn or bury all diseased material. Clean pruning tools between cuts with a dilute solution of household bleach (one part bleach to nine parts water)."
  > "Remove blighted limbs during the dormant season when bacteria are less active."
  > "Those that show some fire blight resistance are Shinko (best), Shin Li, Olympic, and Seuri."
  > "Twentieth Century and Hosui are highly susceptible; however, Hosui is often used as a pollinator for Shinko."
  > "One species of pear that works well as a rootstock for Asian pears is the birchleaf pear _(Pyrus betulifolia)_. It is reported to be more cold hardy than _Pyrus calleryana_, another pear species used as a rootstock but has become an invasive species."
  > "_P. betulifolia_ is resistant to fire blight_._ However, it produces a very vigorous tree and produces root sprouts that have large 'thorns'."
  > "Another bacterium disease, Pseudomonas shoot blight, occurs in South Carolina and can be confused with fire blight. Management practices used for fire blight should be effective for Pseudomonas shoot blight."
  Note the INTRA-CLEMSON CONTRADICTION on Hosui: HGIC 2208 "somewhat resistant", HGIC 1352 "highly susceptible". Purdue rates Hosui Susceptible; PNW rates it 3.0 (same as Nijisseiki).
uc_ipm https://ipm.ucanr.edu/home-and-landscape/fire-blight/ -- verified 2026-09-04 -- home (PN 7414, updated 07/2011)
  > "Most pear tree varieties, including Asian pears (with the exception of Shinko) and red pear varieties, are very susceptible to fire blight."
  > "Ideal conditions for infection, disease development, and spread of the pathogen are rainy or humid weather with daytime temperatures from 75° to 85°F, especially when night temperatures stay above 55°F."
  > "Once infected, the plant will harbor the pathogen indefinitely."
  > "Rapidly advancing infections on very susceptible trees (pear, Asian pear, and some apple varieties) should be removed as soon as they appear in spring."
  > "To locate the correct cutting site, find the lower edge of the visible infection in the branch, trace that infected branch back to its point of attachment, and cut at the next branch juncture down without harming the branch collar. This will remove the infected branch and the branch to which it is attached. If a fire blight infection occurs on a trunk or major limb, the wood often can be saved by scraping off the bark down to the cambium layer in infected areas (i.e., removing both the outer and inner bark). When scraping, look for long, narrow infections that can extend beyond the margin of the canker or infection site. If any are detected, remove all discolored tissue plus 6 to 8 inches more beyond the infection. This procedure is best done in winter when trees are dormant and bacteria aren't active in the tree."
  > "In these cases, dipping shears in 10% bleach between cuts might be wise. However, the location of the cut is far more important than the cleansing of tools."
  > "Copper products are the only materials available to homeowners for fire blight control"
  > "A very weak (about 0.5%) Bordeaux mixture or other copper product applied several times as blossoms open might reduce new infections but won't eliminate all new infections or those already existing in wood...Once blossoms begin to open, make the first application when the average temperature (average of the maximum and minimum temperatures for a 24-hour period) exceeds 60°F. Apply at four- to five-day intervals during periods of high humidity and until late bloom is over. For pear trees, this might mean five to 12 applications per season. Copper products also might cause russeting or scarring of the fruit surface."
  > "The succulent tissue of rapidly growing trees is especially vulnerable; thus excess nitrogen fertilization and heavy pruning, which promote such growth, should be avoided. Trees shouldn't be irrigated during bloom."
purdue_ext https://www.extension.purdue.edu/extmedia/BP/BP-30-W.pdf -- verified 2026-09-04 -- PDF, home
orchard ("Fire Blight on Fruit Trees in the Home Orchard", Beckerman, 1/07; three pages read as images)
  > "Fire blight, caused by the bacterium Erwinia amylovora, attacks more than 70 members of the Rose (Rosaceae) family, and is a devastating disease of apples and pears."
  > "The younger the tree, the more likely it will die following infection."
  > "This disease is most severe during flowering, when warm spring weather (70-81°F, 21-27°C), coupled with rainfall and hail, provide optimum conditions for fire blight development."
  > "Prune only in dry weather, and make cuts at least 12 inches away from the site of infection and into healthy plant tissue. Delay summer pruning until the terminal bud has set and growth has ceased."
  > "Never prune to shape the tree at the same time disease management is taking place."
  > "Dispose of all infected material and sterilize pruning equipment between cuts by dipping in a solution of 10 percent bleach with a few drops of detergent. Plants that have more than 50 percent of their canopy infected should be removed."
  > "Careful nitrogen fertilization, thereby reducing succulent, susceptible growth."
  > Table 1 "Fire Blight Resistance of Apple and Pear Varieties", Asian Pears: Resistant: "Chojuro Kosui, Olympic (Korean Giant), Seuri, Shinko, Shinsui, Singo, Tse Li, Ya Li*"; Susceptible: "Hosui, Kikusui, Okusankichi, Seigyoku, 20th Century(Nijisseki), New Century (Shinseiki) Ya Li*". Pear Rootstocks: Resistant: "Old Home (OH) Old Home x Farmingdale (except OHxF 51), P. calleryana, P. betulifolaefolia seedlings"; Susceptible: "Bartlett Seedling, Quince seedling". (*= contradicting studies.) Niitaka does not appear in the table.
  > "Agri-Strep (streptomycin), is acceptable for home use, but may be difficult to obtain." ... "Make no more than three to four applications per season" ... "Confine antibiotic sprays to the bloom through petal fall period"
wsu_ext https://treefruit.wsu.edu/crop-protection/disease-management/fire-blight/ -- verified 2026-09-04 -- commercial (DuPont, Smith, Johnson, Zhao; Dec 2024)
  > "Remove infected branches 12 to 18 inches below the visibly infected tissue in wood that is two years old or older"
  > "You do not need to sterilize tools when you are cutting on fully dormant trees" ... "sterilizing shears made no difference in preventing canker formation as long as the cuts are made at the recommended distance below the visible canker"
  > "Cougar Blight is available at WSU Decision Aid System" ... "Maryblyt is another commonly used model." (risk rises "above 70°F", "optimal at 80°F")
  > "By limiting nitrogen fertilizer application, tree vigor is reduced. Moderating vigor will not prevent infection, but it can reduce damage."
osu_ext EC 631 -- home: "Remove and destroy infected branches. Make cuts 12 inches below infected branches. Disinfect pruning tools between cuts with shellac thinner (70% ethyl alcohol) or 10% bleach."
ncsu_ext_handbook_tree_fruit -- home: Asian pear cultivars "Twentieth Century (Nijisseiki), Nititaka (pollen source), Shinseiki (New Century), Chojuro" [sic "Nititaka"]; "Fire blight is the biggest concern."; European pears: "Plant only fire blight-resistant cultivars."; "Plant pears on higher sites than apples; they bloom earlier."
ucanr_ext Beutel 1989: "All Asian pear varieties except 'Shinko' may develop fireblight _(Erwinia amylovora)_." (lists 20th Century, Shinseiki, Kosui, Shinsui, Ichiban Nashi, Hosui, Kikusui, Yoinashi, Chojuro, Ya Li, Tsu Li, Dasui Li, Shin Li, Niitaka, Okusankichi as the "may develop" set); "Shinko...appears to be nearly resistant to fireblight."; growers "spray antibiotic fireblight materials (Streptomycin, Terramycin or copper) during the bloom period" (commercial).
wsu_ext pear rootstocks (record anchor for the two sibling entries): "Reimer was looking primarily for rootstocks resistant to fireblight. Both parents are highly resistant." (OHxF series)
NEEDS-CATALOG-ADMISSION: PNW "Pear, Asian Cultivar Susceptibility" table (PROXY; reviewed March 2023;
scale "10 = no blight; 1 = dead tree", USDA Plant Disease Reporter data): Shinko 7.5, Ya Li 7.0, Seuri
6.5, Chojuro 4.0, Niitaka 4.0, Kikusui 3.5, Shinseiki 3.5, Hosui 3.0, Nijisseiki (20th Century) 3.0,
Seigyoku 3.0, Bartlett 1.0?.
RECORD CLAIMS THAT HOLD: blossoms/shoot tips blacken, shepherd's crook, cankers, ooze (Clemson 2208;
PN 7414; Purdue); Asian pear highly susceptible (PN 7414; Clemson 1352; Beutel); 20th Century among
the worst (Clemson 1352 "highly susceptible"; Purdue Susceptible); can kill a young tree (Purdue);
*E. amylovora*; infects through blossoms/shoots in warm wet spring (PN 7414 75-85°F; Purdue 70-81°F,
"flowers, new leaves, small wounds"); nitrogen-pushed growth (all four home docs); prune 8 to 12
inches (Clemson 2208 "a minimum of 8 to 12 inches"); disinfect tools between cuts (Clemson 2208 10%
bleach / 70% alcohol; Purdue; EC 631); dry weather (Purdue "Prune only in dry weather"); no cure
(Clemson 2208; PN 7414 "harbor the pathogen indefinitely"); remove badly affected trees (Purdue >50%
canopy); Shinko tolerant (every document); Chojuro more tolerant (Clemson 2208 "some resistance";
Purdue Resistant; PNW 4.0); OHxF tolerant rootstock (Purdue table; WSU rootstocks "Both parents are
highly resistant"); *P. calleryana* tolerant rootstock (Purdue table Resistant); forecast model (WSU,
COMMERCIAL only: CougarBlight, Maryblyt).
RECORD CLAIMS WITH NO ANCHOR: "Niitaka among the worst" -- NO document read says this. Beutel lists
Niitaka only inside the "all except Shinko may develop fireblight" set; NC State RECOMMENDS Niitaka as
the pollen source; PNW rates Niitaka 4.0, identical to Chojuro, which the record calls tolerant; Purdue
and Clemson do not rate it. "It is the single biggest reason European pears fail in the humid South
and East" -- the nearest sentences are Clemson 1352 "the most significant problem limiting the
production of Asian pears" and NC State "Fire blight is the biggest concern"; the regional-failure
framing is not published on any page read. "kill whole limbs" (implied, not stated).
RECORD CLAIMS THAT ARE WRONG:
  - `organic_treatment_beginner` "Cut off the blackened branches well below the damage (about a hand's length past it)": a hand's length (roughly 7-8 in) is below EVERY published figure: Clemson 2208 minimum 8-12 in; OSU 12 in; Purdue "at least 12 inches"; WSU 12-18 in; Clemson's own Asian pear sheet 18 in. The seasoned copy's "8 to 12 inches" is the low end of the range across sources.
  - The record says prune "in dry weather" and says nothing about season; its own anchor says "Prune out blackened twigs and branches with cankers during the dormant season. Pruning during the growing season may spread the disease.", and Clemson 1352 and PN 7414 agree on dormant-season removal, while PN 7414 ALSO says fast-moving strikes on Asian pear "should be removed as soon as they appear in spring". The record carries neither position; the rewrite needs both (cut fast strikes in spring, do the main cleanup dormant, and dry weather either way per Purdue).
  - "(the OHxF series, or Pyrus calleryana)" as a home recommendation: Purdue rates calleryana resistant, but Clemson 1352 says it "has become an invasive species", a content/values call the orchestrator should make before consumer copy recommends it; Clemson 1352's Asian-pear rootstock is *P. betulifolia*.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry: copper is the ONLY home material (PN 7414), applied
as blossoms open when 24-h average temperature exceeds 60°F, every 4-5 days, "five to 12 applications
per season" on pear, and it "might cause russeting"; Clemson's copper is one spray immediately before
bloom; streptomycin is written for apple at Clemson (Ferti-lome), and Purdue caps it at 3-4 per season,
bloom to petal fall, with resistance warnings; cut location beats tool sterilization (PN 7414; WSU);
scrape trunk cankers 6-8 in beyond discoloration in winter (PN 7414); no irrigation during bloom (PN
7414); delay summer shaping until terminal buds set (Purdue); >50% canopy infected = remove (Purdue);
"Plant pears on higher sites than apples; they bloom earlier." (NC State); honeybees spread it (Clemson);
Pseudomonas shoot blight look-alike (Clemson 1352); *P. betulifolia* rootstock resistant but vigorous
and thorny-suckering (Clemson 1352); Hosui is planted despite susceptibility as Shinko's pollinizer
(Clemson 1352), which matters for a two-cultivar self-incompatible crop; the seasoned copy's "20th
Century" should read "Twentieth Century (Nijisseiki)" to match the cultivar names in NC State/Clemson.
PLA-457: none seen.

## Pear scab [diseases]  -- severity medium, type fungal   (the second copy, added 2026-07-02 at certification)
STATUS: SOURCED-WEAK (same anchor as the pests[] copy; duplicate)
ORGANISM: as above, *Venturia pirina* per UC IPM PN 7413 / ag page (spelled *V. pyrina* by PNW). Same
*V. nashicola* finding as above: the cited document does not name it and says Asian pears are less
susceptible.
ANCHORS: identical to the pests[] copy: uc_ipm PN 7413 (home; all quotes above), uc_ipm ag pear scab
(commercial), osu_ext EC 631 (home), ucanr_ext Beutel, PNW (NEEDS-CATALOG-ADMISSION).
RECORD CLAIMS THAT HOLD: olive to black velvety lesions on leaves and fruit (PN 7413); cracked fruit
(PN 7413); yellowing and early defoliation (PN 7413); "scabby, misshapen fruit" (ag page "scablike and
misshapen", extractor fragment; PN 7413 "Scabby spots"); *Venturia* overwinters in fallen leaves and
infects in wet spring weather with wetness/temperature (PN 7413); sulfur on a protective spring
schedule (PN 7413); prevention beats cure (PN 7413); rake and remove leaves each autumn (PN 7413; EC 631).
RECORD CLAIMS WITH NO ANCHOR: "prune for airflow" (absent, as above); "corky" (absent); "choose
less-susceptible varieties" (European list only); `prevention_beginner` "Resistant varieties rarely
need spraying" (PN 7413 says "negligible scab risk" for nine EUROPEAN cultivars and says nothing about
spraying them; on Asian pear no cultivar is named).
RECORD CLAIMS THAT ARE WRONG: same severity finding as the pests[] copy (anchor: Asian pears "less
susceptible").
BUNDLE / GENERIC VERDICT: DUPLICATE. Claim-by-claim comparison of the two copies against the documents:
  - symptoms_seasoned: pests[] copy names "leaves, shoots, and fruit" and "The pear analog of apple scab", both of which map to sentences on the anchor (twig lesions; "similar blemishes on pear fruit"); diseases[] copy names only leaves and fruit but adds "scabby, misshapen fruit" (commercial page). pests[] is better anchored; take "misshapen" from diseases[].
  - symptoms_beginner: near-identical; pests[] copy's "rough, scabby, cracked patches" is closer to "Fruit also can crack". Keep pests[].
  - cause_seasoned: pests[] copy's "Distinct from the apple-scab fungus but managed the same way" maps to the anchor naming two species on one management page; diseases[] copy is a strict subset. Keep pests[].
  - cause_beginner: identical in substance. Either.
  - organic_treatment_seasoned / beginner: identical in substance; both are anchored (sulfur, protective timing, prevention). Either; pests[] copy's "far easier to prevent than to cure once established" is closer to the anchor's "preventing early infection is the most important step".
  - prevention_seasoned: identical; both carry the unanchored "prune for airflow".
  - prevention_beginner: pests[] copy ("that is where the fungus hides over winter") is anchored; diseases[] copy's "Resistant varieties rarely need spraying" is not. Keep pests[].
  Verdict: the pests[] (older) copy is the better-anchored prose on 5 of 7 fields and equal on 2; the only sentence worth lifting from the diseases[] copy is "misshapen fruit". Keep ONE entry, in diseases[], type fungal, built from the pests[] prose, with a new lead sentence that Asian pears are less susceptible than European pears (PN 7413) and the twig-lesion overwintering note.
LADDER-RELEVANT FACTS the record does not carry: as for the pests[] copy.
PLA-457: as for the pests[] copy (PN 7413 "never apply them within 3 weeks of an oil application"; UC IPM ag "Do not apply within 3 weeks of an oil application"; EC 631 no-number incompatibility sentence; PNW label note).

## Pear decline [diseases]  -- severity medium, type other
STATUS: SOURCED-WEAK (the anchor carries the three OHxF rootstock claims by name and nothing else;
etiology, vector, symptoms and management were all found at T1 on other documents, two of them home)
ORGANISM: '*Candidatus* Phytoplasma pyri' per WSU Tree Fruit psylla page ("_Candidatus Phytoplasma
pyri_: Pear decline phytoplasma"), USU ("Pear decline is caused by _Candidatus_ Phytoplasma pyri
transmitted by pear psylla."), PNW. UC IPM (home and ag) names it only as "a phytoplasma".
ANCHORS:
wsu_ext https://treefruit.wsu.edu/web-article/pear-rootstocks/ -- verified 2026-09-04 -- commercial
(rootstock catalogue, no author/date; the record's anchor)
  > OHxF 87: "The OHxF selections are compatible with most pear varieties and are known for their tolerance to blight and decline."
  > OHxF 97: "A clonal rootstock of 'Old Home' x 'Farmingdale', this rootstock is resistant to pear decline and fireblight."
  > OHxF 333: "Its resistance to fireblight, collar rot, woolly pear aphids, and pear decline make this a very healthy stock. it is not very precocious and gives few fruit and with reduced size"
  > OHxF 40: "Resistant to fire blight, crown rot, woolly pear aphids, and pear decline."
  > "Selections shown in purple text indicate possible susceptibility to pear decline." (figure caption)
  > Bartlett seedling: "Hardy seedling rootstock Van Well Nursery uses for pear and Asian pear varieties." (the page's ONLY Asian-pear sentence)
  The page contains no phytoplasma, psylla, symptom, or management sentence. It does not discuss Asian cultivars.
uc_ipm https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/DISEASE/peardecline.html (also served at
https://ipm.ucanr.edu/home-and-landscape/pear-decline/) -- verified 2026-09-04 -- home ("Adapted from
_Integrated Pest Management for Apples and Pears_ and _Pest Management Guidelines: Pears_"; no date)
  > "Pear decline is caused by a phytoplasma, a microscopic bacterialike organism."
  > "the pear decline phytoplasma requires either a pear tree or the pear psylla (_Cacopsylla pyricola_), an aphidlike insect (psyllid) that vectors the phytoplasma"
  > "In spring, infected trees leaf out more slowly than healthy trees"; "leaves thicken, curl downward, and change color prematurely"; "Leaves of Bartlett and Bosc pears turn red to purple"; "foliage wilts rapidly and affected trees die within a few days" (quick decline)
  > "A brown line caused by death of phloem cells develops on the outside of the wood at the graft union"
  > "Pear decline can rapidly kill pear planted on Asian rootstocks: _Pyrus pyrifolia_ (=_P. serotina_) and _P. ussuriensis_."
  > "Tolerant rootstocks include Bartlett seedling, Old Home X Farmingdale rooted cutting, _Pyrus betulaefolia_, and Winter Nelis seedling."
  > "Reducing the abundance of pear psylla will reduce transmission of the phytoplasma"
  > "Trees infected with pear decline may benefit from increased nitrogen applications and frequent, light irrigations."
uc_ipm https://ipm.ucanr.edu/agriculture/pear/pear-decline/ -- verified 2026-09-04 -- commercial (Elkins, Gubler, Adaskaveg; 11/12)
  > "The phytoplasma organism that causes pear decline is transmitted by pear psylla when feeding on pear foliage."
  > "Sudden tree collapse can result from hypersensitive tissue damage at the graft union" (quick decline); "very slow decline when trees are not receiving adequate water and nutrition"; "premature reddening and upper rolling of leaves, reduced leaf and fruit size"
  > susceptible: "_Pyrus serotina_ or _P. ussuriensis_"; tolerant: "Bartlett seedling, Winter Nelis, Old Home x Farmingdale, and _Pyrus betulaefolia_"
  > "Control pear psylla"; "Maintain trees in good vigor by reducing stress"; "There is no known biological control of the pear decline phytoplasma organism"
wsu_ext treefruit psylla page (commercial; quotes above): "Pear psylla also transmit a mycoplasma disease organism (_Candidatus Phytoplasma pyri_: Pear decline phytoplasma) through its saliva. The disease damages sieve tubes in the phloem."; P. ussuriensis and P. pyrifolia rootstocks "most susceptible"; "Most pears in Washington and Oregon are grafted to tolerant _P. communis_."
wsu_ext Hortsense pear psylla (home): "The pear psylla spreads the organism which causes pear decline."
uc_ipm home pear psylla (home): "Loss of tree vigor and premature tree death can occur from pear decline, a phytoplasma disease that develops after the psyllid injects its pathogen-contaminated saliva while feeding."
usu_ext https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-decline -- verified 2026-09-04 -- extension note (no author/date)
  > "Pear decline is caused by _Candidatus_ Phytoplasma pyri transmitted by pear psylla."
  > "The phytoplasma is spread from tree to tree by feeding pear psylla. It kills phloem cells at the graft union of specific root-scion combinations, preventing the tree from transporting sugar from its top to its roots. Sugar accumulates above the graft union as stored starch while the roots die from starvation."
  > "Decline is much more prevalent on trees with rootstocks of _Pyrus ussuriensis_ or _P. pyrifolia_ than on trees propagated on domestic _P. communis_ roots."
  > "When grafting Asian pear trees over to European (_P. communis_) cultivars, graft below the union of the Asian pear with its rootstock to avoid creating a highly decline-susceptible tree"
  > "Control pear psylla."; "Remove diseased trees"
NEEDS-CATALOG-ADMISSION: PNW "Pear (Pyrus spp.)-Decline" (PROXY): "The Farold series 40, 69 or 87
(also known as 'Old Home x Farmingdale') are a highly tolerant alternative when grown on well-drained
soils."; "The dwarfing quince rootstocks have been highly tolerant of this disease."; "Remove infected
trees from nurseries and young orchards."; same USU grafting sentence. (The extractor's summary said the
phytoplasma is "a bacterium without a cell wall", but the verbatim pass did NOT return such a sentence,
so it is NOT treated as published.)
RECORD CLAIMS THAT HOLD: slow decline, weak growth, small leaves, reddish early fall color, reduced
yield, or sudden collapse (UC IPM home + ag); phytoplasma transmitted by pear psylla (WSU psylla; UC
IPM home/ag; USU; Hortsense); expressed through a sensitive rootstock (UC IPM home Asian rootstocks;
USU; WSU); "a bacteria-like organism" (UC IPM home "bacterialike"); OHxF 87/97/333 tolerant BY NAME
(WSU rootstocks, above); control psylla (UC IPM home/ag; USU); remove severely declining trees (USU
"Remove diseased trees"); avoid highly sensitive rootstocks (UC IPM home: *P. pyrifolia*, *P.
ussuriensis*).
RECORD CLAIMS WITH NO ANCHOR: "No cure" / "There is no cure once a tree has it" -- not stated on any
page read. UC IPM ag says "There is no known biological control of the pear decline phytoplasma
organism" (a different claim), and UC IPM home says infected trees "may benefit from increased nitrogen
applications and frequent, light irrigations", so slow-decline trees are nursed, not written off. "That
is the whole prevention" (beginner) overstates: psylla suppression is the other half on every page.
RECORD CLAIMS THAT ARE WRONG: none refuted. Note the type: `other` (no gate recognizes it).
BUNDLE / GENERIC VERDICT: n/a.
Asian-pear specifics: the decline-SENSITIVE rootstocks are the Asian pear species themselves (*P.
pyrifolia* = *P. serotina*, *P. ussuriensis*), so an Asian pear on its own seedling roots is the
worst case (UC IPM home: "can rapidly kill"). Beutel 1989 lists *P. serotina* and *P. ussuriensis* among
the roots Asian pears "will grow on", which is exactly the combination UC IPM warns about. No document
read discusses Asian pear CULTIVARS (scions) and decline; the WSU anchor's only Asian sentence is the
Bartlett-seedling one. USU's grafting rule (graft below the Asian-pear/rootstock union when converting
to European cultivars) is the one Asian-specific management sentence.
Fine type: propose `bacterial`. Basis: UC IPM's "a phytoplasma, a microscopic bacterialike organism" and
WSU's "mycoplasma disease organism" describe a phytoplasma; NO admissible document read calls it a
bacterium outright, so the source language supports `bacterial` only by the same convention the roster
already applies (carrot and parsnip "Aster yellows" and cherry-sweet "X-disease" are typed `bacterial`
with "bacterium-like organism" in cause_seasoned, verified in canonical this session). `bacterial` is
consistent with those three precedents and is the only type in the brief's set that fits; the honest
alternative, a `phytoplasma` type, is outside the set and would need a roster ruling.
LADDER-RELEVANT FACTS the record does not carry: the brown line at the graft union is the field
diagnostic (UC IPM home); the mechanism (phloem killed at the union, roots starve) explains why
rootstock decides everything (USU); quick decline = collapse within days on Asian roots, slow decline =
years and can be nursed with nitrogen and light frequent irrigation (UC IPM home/ag); the ladder is
entirely (1) rootstock at purchase, (2) psylla suppression, (3) vigor, (4) removal; there is no
chemical rung and "no known biological control" (UC IPM ag); OHxF tolerance holds "when grown on
well-drained soils" (PNW); Bartlett seedling, Winter Nelis and *P. betulaefolia* are the other tolerant
roots (UC IPM), and *P. betulifolia* is the one Clemson recommends for Asian pears; quince is
decline-tolerant (PNW) but not winter-hardy (OSU EC 819: "Quince isn't winter-hardy").
PLA-457: none seen.

---

## SUMMARY

Counts by STATUS (7 entries): SOURCED-OK 0; SOURCED-WEAK 5 (Codling moth, Pear scab x2, Fire blight,
Pear decline); ANCHOR-MISPOINTED 2 (Pear psylla, Stink bug); UNSOURCED-NOT-FOUND 0; JOURNAL-ONLY 0
(the *V. nashicola* species split is JOURNAL + non-admissible PNW + the 1989 UC brochure);
NEEDS-CATALOG-ADMISSION: PNW Pest Management Handbooks (four pages used as corroboration only).
Dead record anchors: 1 (NCSU growing-pears-in-the-home-garden, 404). Mis-pointed record anchors: 2
(Clemson fire blight page cited for Stink bug; WSU rootstock article cited for Pear psylla). Anchors
carrying only part of their entry: 1 (WSU rootstock article for Pear decline: OHxF only).

Single most important finding: the pest half of this record is pear-european's record with the name
changed, and the sources rate it differently on Asian pear. UC IPM (home and commercial) says "Pear
psylla is a greater problem on European varieties than on Asian varieties of pear"; PN 7413 says Asian
pears "are less susceptible to scab than European pears"; the Asian-pear scab fungus "has not been
reported in the Pacific Northwest" (PNW) and "is not the same scab species found in California" (UC
ANR). Both are severity `high`/`medium` here by inheritance, while the one disease every Asian-pear
document calls the limiting one, fire blight, carries a beginner pruning distance ("about a hand's
length") that undershoots every published figure (8-12 in minimum, 12, 12-18, 18 in), an unanchored
"Niitaka among the worst" claim that the PNW table rates equal to the record's "tolerant" Chojuro,
and no mention of the dormant-season pruning its own anchor prescribes. Second: PN 7412 retires trunk
banding for home gardens ("banding no longer is recommended for control in home gardens") and the
record prescribes it in two Codling moth fields. Third: Clemson's own Asian Pear factsheet (HGIC 1352),
uncited anywhere on this crop, is the single best home document for it (fire blight cultivars, 18-inch
cut, dormant-season timing, *P. betulifolia* rootstock, "Codling moths and aphids are the most common
insect problems"), and it does not mention psylla, scab, stink bugs or decline at all; it does name
rust and aphids, which the record lacks.

Which Pear scab copy is better anchored: the pests[] (older, 2026-06-11) copy, on 5 of 7 fields (its
"leaves, shoots, and fruit", "analog of apple scab", "Distinct from the apple-scab fungus but managed
the same way", and its beginner leaf-raking rationale all map to sentences on PN 7413); the diseases[]
copy contributes only "misshapen fruit" and carries one unanchored sentence ("Resistant varieties
rarely need spraying"). Keep one entry in diseases[] built from the pests[] prose plus "misshapen",
led by the Asian-pears-less-susceptible sentence, at a reconsidered (lower) severity.

Consumer-copy flags: no em dashes found in the seven entries; "frass" appears in beginner copy with an
inline gloss (acceptable); "phytoplasma", "psyllid", "anthocorid bugs" are seasoned-only; "20th
Century" should be "Twentieth Century (Nijisseiki)" to match the sources' cultivar naming. No °F
figures in the record; every °F figure above is quoted from a document.

## PROPOSED TYPE
Codling moth [pests]: `insect` -- *Cydia pomonella* (UC IPM PN 7412; UC IPM ag pear).
Pear psylla [pests]: `insect` -- *Cacopsylla pyricola* (WSU Tree Fruit; UC IPM home and ag).
Stink bug [pests]: `insect` -- umbrella of Pentatomidae: *Halyomorpha halys* (WSU; Clemson 2404) plus native *Euschistus conspersus* / *Euschistus* spp. / *Acrosternum* spp. (UC IPM home; PNW; Clemson 2001).
Pear scab [pests]: `fungal` -- *Venturia pirina* (UC IPM PN 7413); entry should MOVE to diseases[] and merge with the copy below.
Fire blight [diseases]: `bacterial` -- *Erwinia amylovora* (Clemson HGIC 2208; UC IPM PN 7414; Purdue BP-30-W).
Pear scab [diseases]: `fungal` -- *Venturia pirina* (UC IPM PN 7413); the surviving single entry.
Pear decline [diseases]: `bacterial` (replacing `other`) -- '*Candidatus* Phytoplasma pyri' (WSU Tree Fruit psylla page; USU), described by UC IPM as "a phytoplasma, a microscopic bacterialike organism"; typed by the roster's existing aster-yellows / X-disease convention, not by a source sentence calling it a bacterium.
