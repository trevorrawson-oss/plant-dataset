# PLA-8 batch 26 -- INDEPENDENT SOURCE-TRUTH REVIEW: pear-asian

Reviewer did not author this crop. Every document below was fetched and read this session
(2026-09-04) through WebFetch, first-party unless marked. OSU EC 631 was read through the
`r.jina.ai` proxy (first-party 403). Purdue BP-30-W was retrieved as PDF bytes and read page by
page as images (three pages). UC IPM ag pear decline needed a retry (ECONNRESET) and then read
clean. Every quote marked with quotation marks came back verbatim from the extractor. The record
report's quotes were NOT trusted; each load-bearing sentence was re-found on its page.

Validator: `validate_out.py pear-asian` -> "OK: pear-asian validates. 3 pests + 3 diseases, 22 rungs."
PLA-457 scan (every consumer string, sentence by sentence, for sulfur + oil + a duration): 0 hits.
`sources` == `anchoring_urls` keys on all six entries. No em dashes in consumer copy.

Grades: HOLDS / WRONG / UNSUPPORTED / SYNTHESIS / STYLE / FIT per the brief.

---

## Codling moth [pests] -- id codling-moth, insect, high

Anchors read: UC IPM PN 7412 (home) https://ipm.ucanr.edu/home-and-landscape/codling-moth/ ;
UC IPM pear guideline (commercial) https://ipm.ucanr.edu/agriculture/pear/codling-moth/ ;
NCSU handbook ch. 15 ; UC ANR Beutel 1989 brochure.

* `garden_sanitation` -- **HOLDS.** PN 7412: "Removing infested fruit before the larvae are old
  enough to crawl out and begin the next generation can be a very effective method for reducing
  the population." / "It also is important to clean up dropped fruit as soon as possible after
  they fall" / "Thin the fruit to one per cluster." / "Be sure to examine the fruit where it
  touches another fruit, as this is a common place to find an entry hole." / "Codling moth
  overwinters as full-grown larvae within thick, silken cocoons under loose scales of bark" / "It
  is much easier to keep moth numbers low from the start than to suppress a well-established
  population." Pear guideline: "Remove host trees in nearby abandoned orchards (apple, pear, and
  walnut) to destroy reservoirs of codling moth." Nit (STYLE, no fix): beginner "every week or
  so"; PN 7412 prints "Every week or two, beginning about six to eight weeks after bloom, check
  fruit on trees for signs of damage." The start point could be carried.
* `codling_moth_pheromone_trap` -- **HOLDS.** PN 7412: "Codling moth pheromone traps are
  important for monitoring flight activity of moths to help time insecticide treatments." /
  "Hanging traps in each susceptible fruit or nut tree might help to reduce codling moth
  populations on isolated trees but isn't a reliable way to reduce damage." / "200 to 250
  degree-days after you begin regularly catching male moths". Nit (SYNTHESIS inherited from the
  catalog, no fix): beginner says the trap "sets the clock for bagging"; PN 7412 times bagging
  by bloom, traps time sprays. The catalog's own method text says traps time bagging.
* `fruit_bagging` -- **HOLDS.** PN 7412: "Bagging should be done about four to six weeks after
  bloom when the fruit is from 1/2 to 1 inch in diameter." / "This is the only nonchemical
  control method that is effective enough to be used alone and in higher population
  situations." / "late-developing varieties might be attacked by codling moth even before they
  are 1/2 inch in diameter". NCSU: "Bagging individual fruit four weeks to six weeks after bloom
  provides excellent control".
* `spinosad` -- **HOLDS.** PN 7412: "three sprays applied at 10-day intervals beginning at egg
  hatch" / "No more than six sprays should be applied per season, and they shouldn't be applied
  within seven days of harvest." / "Spinosad is a biological product made from a naturally
  occurring bacterium called Saccharopolyspora spinosa." / CYD-X: "when applied weekly during
  egg hatch throughout the season, is as effective as carbaryl sprays" (record quote; my read
  returned "affects only larvae (caterpillars) of the codling moth" and "OMRI listed"). The bee
  timing (dusk, nothing in flower) is the catalog caution, not PN 7412; allowed.
* `carbaryl` -- **HOLDS.** PN 7412: "It remains effective for 14 to 21 days, but it is very
  disruptive to natural enemies and honey bees." / "Carbaryl never should be sprayed during
  bloom or when bees are present." Both registers carry the bee bar. Psylla flare: pear psylla
  guideline "Nonselective codling moth insecticides destroy many of these beneficials, resulting
  in outbreaks of this pest." Carcinogen listing is the catalog caution.

Banding: gone from the ladder and corrected out of both prevention fields. Kaolin: confirmed
absent from PN 7412 ("No mention of kaolin or Surround appears on this page"). See RECORD-LEVEL
R2 on the commercial row.

Corrections:
* `symptoms_seasoned` -- **HOLDS.** Pear guideline: "Stings are entries where larvae bore into
  the flesh a short distance before dying. Deep entries occur when larvae penetrate the fruit
  skin, bore to the core, and feed in the seed cavity." / "One or more holes plugged with frass
  on the fruit's surface is a characteristic sign". Needed: yes; "often at the calyx end" is not
  on either page (guideline: "Larvae may enter through the sides, stem end, or calyx (flower)
  end of the fruit.").
* `cause_seasoned` -- **HOLDS.** PN 7412 overwintering and "two, three, and sometimes four
  generations per year"; guideline "Females lay eggs singly on leaves and on fruit." Needed:
  yes ("near bloom" is on no page).
* `organic_treatment_seasoned` -- **HOLDS** on the replacement text. The `why` misdescribes
  the commercial kaolin row (R2), but the outcome (no home kaolin schedule) is right.
* `prevention_seasoned` -- **HOLDS.** PN 7412: "banding no longer is recommended for control in
  home gardens." Needed: yes (the record prescribed banding).
* `prevention_beginner` -- **HOLDS.** Same sentence. Needed: yes.

---

## Pear psylla [pests] -- id pear-psylla, insect, medium (lowered from high)

Anchors read: UC IPM home pear psylla ; UC IPM pear psylla guideline (commercial) ; WSU
Hortsense pear psylla (home) ; WSU Tree Fruit psylla IPM (commercial) ; OSU EC 631 (proxy).

Severity: UC IPM home "Pear psylla is a greater problem on European varieties than on Asian
varieties of pear." and guideline "Pear psylla is a greater problem on European varieties than
on Asian varieties." Clemson HGIC 1352 names codling moth and aphids as the common insects and
never mentions psylla. The lowering is sourced.

* `balance_nitrogen` -- **HOLDS / SYNTHESIS (no fix).** Hortsense: "Prune lightly, supply
  moderate amounts of nitrogen, and remove water sprouts and suckers." / "Pear psylla nymphs
  feed on leaves, preferring succulent new growth in the upper portions of the canopy." The
  seasoned reason "hard cuts provoke exactly the regrowth psylla wants" is not on the psylla
  pages; it is on this record's fire-blight anchors (PN 7414 "heavy pruning, which promote such
  growth"; Purdue "Avoid excessive winter pruning which otherwise stimulates vegetative
  growth"). Sourced on the record, fused across entries. Acceptable.
* `kaolin_clay` -- **HOLDS.** Hortsense: "Apply kaolin clay, insecticidal soap, or neem during
  the growing season as populations begin to build." Guideline (kaolin): "Apply prebloom; may
  cause mite outbreaks when used later in season." WSU Tree Fruit: "Particle films reduce pear
  psylla adult colonization and egg lay by 80–100%, which reduces pear psylla pressure for the
  first generation." The percentage is efficacy, not the PDD program; no PDD figure appears in
  any note.
* `beneficial_predators` -- **HOLDS.** WSU Tree Fruit: "Important biological control organisms
  in Washington pear orchards are the parasitic wasp Trechnites insidiosus; true bugs
  Deraeocoris brevis, Campylomma verbasci, and Anthocoris spp.; lacewings Chrysoperla carnea,
  Chrysopa nigricornis, Hemerobius spp.; and the earwig Forficula auricularia." Hortsense:
  "green lacewings, ladybird beetles, and predaceous bugs" / "Avoid use of broad-spectrum
  insecticides which kill beneficial insects." Guideline: "Nonselective codling moth
  insecticides destroy many of these beneficials, resulting in outbreaks of this pest."
* `horticultural_oil` -- **HOLDS.** Guideline: "Oil kills adult psylla but does not control
  eggs." / "It does discourage egg laying for about 1 month, however." / "Apply during warm,
  sunny weather from leaf fall to start of egg laying for best results". UC IPM home: "Apply
  horticultural oil at least once during the dormant season and by the beginning of January. If
  the psyllid and its damage have been abundant, make a second dormant treatment of oil just
  before bloom." / "Adults overwinter in bark crevices, under bark scales of pear trees, or on
  the ground in organic litter". WSU Tree Fruit: "They begin laying eggs when pear buds begin to
  swell." Note: Hortsense's own timing word is "delayed-dormant"; the rung attributes its
  earlier timing to UC IPM, correctly. The seasoned sentence "discourages egg laying for about
  a month" names oil and a duration but not sulfur: not a PLA-457 hit.
* `insecticidal_soap` -- **HOLDS.** Hortsense: "Homeowners should not make foliar applications
  to trees over 10 ft. tall." / "Care should be taken in timing insecticide applications to
  early morning/late evening to minimize potential for leaf burn." EC 631 pear psylla rows:
  prepink "insecticidal soap, kaolin, or neem"; petal fall "insecticidal soap or neem"; summer
  to harvest "esfenvalerate, insecticidal soap, kaolin, or neem". Nit: "leaf undersides" is
  not stated by either WSU page (Hortsense says upper canopy new growth).

Refusals on this entry: conventional rungs refused on the sources' own natural-enemy reasoning
(guideline sentence above; Hortsense "Avoid use of broad-spectrum insecticides") -- RIGHT.
PDD timings and the 0.3 nymphs/leaf threshold not written -- RIGHT (commercial). neem declined
as a duplicate contact material -- defensible, and filed for the orchestrator.

Corrections:
* `symptoms_seasoned` -- **HOLDS.** UC IPM home Asian/European sentence; WSU Tree Fruit "In
  large numbers, pear psylla can stunt and defoliate trees and cause fruit drop...These
  symptoms, called psylla shock, are caused by toxic saliva from feeding nymphs." Needed: yes
  ("The signature pear pest" contradicts the anchor on this crop).
* `organic_treatment_seasoned` -- **HOLDS.** Guideline oil/eggs sentences; UC IPM home dormant
  timing; Hortsense growing-season materials. Needed: yes ("smother overwintering adults and
  eggs" contradicts "does not control eggs"; "summer oil" is on no home page). STYLE nit: kaolin
  is listed twice in the one field.
* `organic_treatment_beginner` -- **HOLDS.** UC IPM home "by the beginning of January"; WSU
  "begin laying eggs when pear buds begin to swell". Needed: yes.

**MISSING correction -- FIX F4.** `prevention_beginner` is untouched and still reads "A good
dormant oil spray in late winter and going easy on harsh sprays and fertilizer keep this
pear-specific pest in check." The author's own `why` on `organic_treatment_beginner` retires
"in late winter" ("postdates egg laying in mild climates"); the same phrase survives one field
over. Settling sentences: UC IPM home "Apply horticultural oil at least once during the dormant
season and by the beginning of January."; WSU Tree Fruit "They begin laying eggs when pear buds
begin to swell." A claim lives in fields; correct every field carrying it.

---

## Stink bug [pests] -- id stink-bugs, insect, medium

Anchors read: WSU Hortsense pear BMSB (home) ; UC IPM home Stink Bugs ; NCSU handbook ch. 15 ;
OSU EC 631 (proxy) ; PSU BMSB (commercial) ; also WSU Tree Fruit BMSB and Rutgers (both
commercial, both named in a note).

Anchor repoint verified: Clemson HGIC 2208 (the record's old anchor) -- "No mention of stink
bugs appears in this document." The five new anchors each carry what is attached to them:
Hortsense (handpick, row cover, natural enemies, chemical caution, overwintering, storage);
UC IPM home (weeds in early spring, insecticides not recommended, damage after the bugs leave,
species list, litter); NCSU (weeds primary food, predator list, broad-spectrum); EC 631
("kaolin (suppression)" verbatim in the BMSB row); PSU (emergence "in early spring to mid-June",
biology only).

* `weed_host_control` -- **HOLDS on content; FIX F5 on anchoring.** UC IPM home: "Eliminate
  groundcovers and other herbaceous vegetation such as weeds in early spring before stink bugs
  become abundant there." NCSU: "Weeds are the primary food source for these insects, so
  keeping weeds to a minimum around the orchard will help manage populations." WSU Tree Fruit:
  "It is also considered a border pest as it invades orchard edges from nearby crops and wooded
  areas." Rutgers: "In tree fruit this has resulted in higher populations near wooded borders
  and soybean fields." The Rutgers sentence exists, but `rutgers_njaes` is on neither `sources`
  nor `anchoring_urls`: a named institution in consumer copy with no anchor on the entry.
* `handpick` -- **HOLDS.** Hortsense: "Light green to white eggs are laid in groups of about 20
  to 30 on the underside of leaves." / "Pick and destroy BMSB egg masses or groups of young
  nymphs" / "Catching adults and nymphs can be facilitated through net-sweeping, plant vacuuming
  or shaking the infested plant over a drop cloth." UC IPM home: "Commonly stink bug feeding
  damage does not become apparent until after plant tissues grow, by which time the stink bugs
  may no longer be present." WSU Tree Fruit: adults "are capable of long-distance flight".
  STYLE nit: "barrel-shaped" is on no page read.
* `floating_row_cover` -- **HOLDS.** Hortsense, in full: "When practical, plants may be
  screened with a floating row cover or similar barrier. Row covers must be in place BEFORE
  stink bugs are present; however, for best fruit production, row covers should be placed after
  pollination has occurred." The note's "after the flowers are finished and the fruit has set"
  is the document's own after-pollination clause. Row-cover-instead-of-bagging: RIGHT; no page
  read names fruit bags for stink bug (Hortsense: "The document contains no mentions of traps,
  kaolin, weeds, or fruit bagging"; UC IPM home: no "row cover", "trap", "kaolin", "bag").
* `kaolin_clay` -- **HOLDS.** EC 631 BMSB row: "Carbaryl, gamma-cyhalothrin, lambda-cyhalothrin,
  permethrin, bifenthrin, acetamiprid, kaolin (suppression), or malathion". Proxy read, live
  URL anchored, noted by the author. The "suppression" qualifier is carried in both registers.
* `beneficial_predators` -- **HOLDS.** NCSU: "Several parasitic wasps and predatory insects,
  such as big-eyed bugs, assassin bug, damsel bugs, and crab spiders, attack these insects.
  Reducing the use of broad spectrum insecticides helps these biological predators keep pest
  populations in check." Hortsense: "Natural enemies may not be sufficient to provide complete
  control, avoid use of broad-spectrum insecticides which would harm populations" / "Chemical
  management is NOT RECOMMENDED FOR ADULT INSECTS." / "These pesticides are toxic to bees." UC
  IPM home: "Insecticides are generally not recommended in gardens and landscapes for stink
  bugs."

Refusals: fruit_bagging refused (RIGHT, above); traps not authored (RIGHT: PSU "Although traps
by themselves will not control BMSB, they can capture adults and nymphs and serve as an early
warning system in orchards", commercial); pyrethroid refused on UC IPM home + Hortsense (RIGHT;
the Clemson apple-sheet overrule is correctly flagged).

Corrections:
* `cause_seasoned` -- **HOLDS.** Hortsense overwintering and storage sentences; PSU emergence
  sentence ("Under normal conditions, overwintering BMSB adults emerge from their winter
  hideouts in early spring to mid-June and immediately move to feed on available hosts."); UC
  IPM home "Overwintering is on the ground in liter." and the species list incl. Euschistus
  conspersus. "petal fall" appears on no page (PSU: "does not appear anywhere on this page").
  Needed: yes.
* `organic_treatment_seasoned` -- **HOLDS with FIX F8 (STYLE/narrowing).** "the home products
  WSU lists act only on very young nymphs" overstates Hortsense: "Chemical management of BMSB is
  most effective against very young nymphs (immature insects). Chemical management is NOT
  RECOMMENDED FOR ADULT INSECTS." "Most effective against" is not "act only on". Everything
  else in the field is on its anchors.
* `organic_treatment_beginner` -- **HOLDS.** Hortsense row cover and egg-mass sentences; UC IPM
  home damage-after sentence. Needed: yes (fruit bags unanchored).
* `prevention_seasoned` -- **HOLDS.** UC IPM home weeds; NCSU predators; Hortsense row cover.
  Needed: yes (traps, bags unanchored).
* `prevention_beginner` -- **HOLDS.** Same. Needed: yes.

---

## Fire blight [diseases] -- id fire-blight, bacterial, high

Anchors read: Clemson HGIC 1352 (Asian pear, rev. Jun 6 2024) ; Clemson HGIC 2208 (updated Jul
18 2025) ; UC IPM PN 7414 ; Purdue BP-30-W (PDF, 3 pages read as images, 1/07) ; WSU Tree
Fruit fire blight (commercial, named in a note) ; OSU EC 631 ; NCSU handbook.

* `resistant_varieties` -- **HOLDS.** HGIC 1352: "Fire blight, caused by a bacterium, is the
  most significant problem limiting the production of Asian pears." / "Those that show some fire
  blight resistance are Shinko (best), Shin Li, Olympic, and Seuri." / "Twentieth Century and
  Hosui are highly susceptible." / "Hosui is often used as a pollinator for Shinko" / "One
  species of pear that works well as a rootstock for Asian pears is the birchleaf pear (Pyrus
  betulifolia)." / "P. betulifolia is resistant to fire blight." / "However, it produces a very
  vigorous tree and produces root sprouts that have large 'thorns'." / "To help manage this
  disease, selecting resistant cultivars, adopting suitable sanitary measures, and avoiding
  excess nitrogen fertilization are essential." HGIC 2208: "'Chojuro', 'Hosui' (somewhat
  resistant), 'Seuri', 'Shinko'" (the intra-Clemson Hosui split is real and the note reports it).
  PN 7414: "Most pear tree varieties, including Asian pears (with the exception of Shinko)...are
  very susceptible to fire blight." Purdue Table 1, Asian Pears, Resistant: "Chojuro Kosui,
  Olympic (Korean Giant), Seuri, Shinko, Shinsui, Singo, Tse Li, Ya Li*"; Susceptible: "Hosui,
  Kikusui, Okusankichi, Seigyoku, 20th Century(Nijisseki), New Century (Shinseiki) Ya Li*"; Pear
  Rootstocks, Resistant: "Old Home (OH) Old Home x Farmingdale (except OHxF 51), P. calleryana,
  P. betulifolaefolia seedlings"; Susceptible: "Bartlett Seedling, Quince seedling". Every name
  in both registers matches the printed table (Ya Li correctly left out as starred).
* `prune_out_infection` -- **HOLDS on content; FIX F6 on anchoring.** Distances: HGIC 2208
  "Pruning cuts of twigs and branches are made a minimum of 8 to 12 inches below any sign of
  infected tissue."; Purdue "Prune only in dry weather, and make cuts at least 12 inches away
  from the site of infection and into healthy plant tissue. Delay summer pruning until the
  terminal bud has set and growth has ceased."; WSU Tree Fruit "Remove infected branches 12 to
  18 inches below the visibly infected tissue in wood that is two years old or older"; HGIC 1352
  "Prune infected branches 18 inches below the affected area and burn or bury all diseased
  material." Season: HGIC 1352 "Remove blighted limbs during the dormant season when bacteria
  are less active."; HGIC 2208 "Prune out blackened twigs and branches with cankers during the
  dormant season. Pruning during the growing season may spread the disease."; Purdue "Prune in
  late winter while trees are dormant to minimize the risk of infection."; PN 7414 "Rapidly
  advancing infections on very susceptible trees (pear, Asian pear, and some apple varieties)
  should be removed as soon as they appear in spring." Cut placement: PN 7414 "find the lower
  edge of the visible infection in the branch, trace that infected branch back to its point of
  attachment, and cut at the next branch juncture down without harming the branch collar" /
  "the location of the cut is far more important than the cleansing of tools." / scraping
  "remove all discolored tissue plus 6 to 8 inches more beyond the infection. This procedure is
  best done in winter when trees are dormant."; WSU "sterilizing shears made no difference in
  preventing canker formation as long as the cuts are made at the recommended distance". Tools:
  HGIC 1352 "one part bleach to nine parts water"; HGIC 2208 "10% bleach solution ... or 70%
  alcohol"; Purdue "10 percent bleach with a few drops of detergent". Removal: Purdue "Plants
  that have more than 50 percent of their canopy infected should be removed." Purdue "Never
  prune to shape the tree at the same time disease management is taking place." "so 12 is a
  floor" is the author's conservative reading of an 8-to-12 minimum (SYNTHESIS, harmless). The
  seasoned note names WSU twice; `wsu_ext` is not on this entry's `sources`/`anchoring_urls`.
* `copper_fungicide` -- **beginner WRONG by scope (FIX F3); seasoned HOLDS.** PN 7414: "Copper
  products are the only materials available to homeowners for fire blight control" (a UC IPM /
  California statement) / "A very weak (about 0.5%) Bordeaux mixture...applied several times as
  blossoms open might reduce new infections but won't eliminate all new infections" / "make the
  first application when the average temperature...exceeds 60°F. Apply at four- to five-day
  intervals" / "For pear trees, this might mean five to 12 applications per season." / "Trees
  shouldn't be irrigated during bloom." HGIC 2208: "One spray of a copper fungicide is applied
  immediately prior to bloom." The beginner's flat "Copper is the only spray a home grower can
  buy for fire blight" is contradicted by two anchors on this same entry: Purdue "Agri-Strep
  (streptomycin), is acceptable for home use, but may be difficult to obtain." and HGIC 2208
  "Pear trees are also treated with a pre-bloom, copper fungicide spray, and then sprays of
  streptomycin during bloom." The seasoned note handles this correctly ("Streptomycin ... capped
  by Purdue at three to four bloom sprays where it can be obtained at all": Purdue "Make no more
  than three to four applications per season" / "Confine antibiotic sprays to the bloom through
  petal fall period"). Region-scoped advice presented as universal (brief class 4).

Refusals: forecast model removed (RIGHT: WSU commercial "Cougar Blight is available at WSU
Decision Aid System"); garden_sanitation not split out (defensible); resistant_rootstock carried
inside resistant_varieties on the method's soilborne text (defensible, mirrors the twin).
Pyrus calleryana dropped: HGIC 1352 verbatim "It is reported to be more cold hardy than Pyrus
calleryana, another pear species used as a rootstock but has become an invasive species." The
invasive reason is Clemson's, confirmed. Purdue Table 1 rates P. calleryana Resistant, so the
content/values call is correctly left to the orchestrator.

Corrections:
* `symptoms_seasoned` -- **HOLDS.** PN 7414 Shinko sentence; HGIC 1352 Twentieth Century;
  Purdue "The younger the tree, the more likely it will die following infection." Niitaka:
  Purdue's table does not list it; HGIC 1352/2208 do not rate it; NCSU lists "Nititaka (pollen
  source)". Needed: yes.
* `cause_seasoned` -- **HOLDS.** PN 7414 "rainy or humid weather with daytime temperatures from
  75° to 85°F, especially when night temperatures stay above 55°F." / "Once infected, the plant
  will harbor the pathogen indefinitely."; HGIC 1352 limiting-problem sentence. Needed: yes
  (the regional-failure sentence was about European pears and is on no page).
* `cause_beginner` -- **HOLDS.** Same anchors. Needed: yes.
* `organic_treatment_beginner` -- **HOLDS.** Figures carried exactly: "at least 12 inches"
  (Purdue "at least 12 inches") and "18 inches" (HGIC 1352 "18 inches"); "1-to-9 bleach mix"
  (HGIC 1352); dormant season + spring exception (HGIC 1352; PN 7414); "burn or bury" (HGIC
  1352). Needed: yes ("a hand's length" undershoots every published figure; no season given
  while the anchor prescribes dormant).
* `organic_treatment_seasoned` -- **HOLDS.** "at least 8 to 12 inches" (HGIC 2208 "a minimum of
  8 to 12 inches"); "Purdue and OSU say 12" (Purdue above; EC 631 "Make cuts 12 inches below
  infected branches."); "WSU 12 to 18 in older wood"; "Clemson's Asian pear guide 18"; next
  juncture, 10 percent bleach or 70 percent alcohol, cut placement over sterilization, dormant
  removal, >50 percent canopy: all verbatim above. Needed: yes.
* `prevention_seasoned` -- **HOLDS except one sentence (FIX F3).** Cultivar list (HGIC 1352 +
  Chojuro from HGIC 2208/Purdue), P. betulifolia and OHxF (HGIC 1352; Purdue table), nitrogen
  and heavy pruning and bloom irrigation (PN 7414) all hold. "Copper at bloom is the only
  protective spray available to home growers" repeats the beginner's scope error; Purdue and
  HGIC 2208 on this entry describe homeowner streptomycin.

---

## Pear scab [diseases] -- id pear-scab, fungal, low (lowered from medium; pests[] copy retired)

Anchor read: UC IPM PN 7413 (updated 01/2011) ; also UC IPM pear scab guideline (commercial) and
EC 631 for cross-checks.

Severity: PN 7413 "Because Asian pears (Pyrus pyrifolia) are a different species, they are less
susceptible to scab than European pears (P. communis)." The anchor's only Asian-pear sentence
says the disease matters less on this crop. Low is sourced.

* `garden_sanitation` -- **HOLDS.** PN 7413: "Both apple and pear scab pathogens overwinter
  primarily in infected leaves on the ground." / "Pear scab also can overwinter in lesions on
  pear twigs in high rainfall areas." / "For a single, backyard tree, removing—then composting or
  destroying—its dropped leaves in autumn or winter can limit the disease to tolerable levels.
  In plantings of several trees, additional steps might be necessary to effectively control this
  disease, especially in cool, moist coastal areas. These include applying zinc and
  fertilizer-grade urea (or some other nitrogen source) to leaves in autumn to hasten leaf fall
  and adding lime to leaf piles beneath the tree. In pears, apply urea by itself, because zinc
  can be phytotoxic." Sprinkler sentence (sunrise to noon) is in the same paragraph per the
  record pass; folded here rather than given a `water_at_the_base` rung, which the author
  disclosed.
* `sulfur` -- **HOLDS; PLA-457 honored.** PN 7413: "Fungicide sprays are necessary only if the
  weather is rainy and leaves are likely to remain wet for 9 or more hours." / "If treatments
  are needed, the generally recommended time is between when buds begin to break and a month
  after petal fall" / "A second application might be needed 10 to 14 days later if it is still
  rainy, once you can see blossom clusters but before they have opened." / "Infection occurs
  most rapidly between 55° and 75°F, and leaves or fruit must remain wet continuously for a
  minimum of 9 hours" / "These include fixed copper, Bordeaux mixtures, copper soaps (copper
  octanoate), sulfur, mineral or neem oils, and myclobutanil." / "When using sulfur-containing
  compounds such as wettable sulfur, never apply them within 3 weeks of an oil application or
  when temperatures are near or higher than 90°F." The notes say "never mix it with oil or
  spray it close to an oil spray" and "Sulfur and oil are never combined or applied close
  together": no interval, and the "3 weeks" figure is filed in `notes_to_orchestrator` under
  PLA-457 with the document named. Correct handling.

"prune for airflow": gone from both corrected prevention fields; PN 7413 on my read: "No
sentences mention pruning, airflow, air circulation, or canopy management." Confirmed absent.

Ladder length (2 here vs 4 on pear-european): JUSTIFIED by this crop's documents. The twin's
`resistant_varieties` is PN 7413's European list ("European pear cultivars with negligible scab
risk include Arganche, Barnett Perry, ..."), which does not apply to an Asian pear, and no
admissible page names a scab-resistant Asian cultivar: the refusal is right. The twin's
`water_at_the_base` rests on the same PN 7413 sprinkler sentence, which does apply here; this
author folded it into `garden_sanitation` and told the orchestrator. That is a shape choice,
not a defect; the orchestrator may want parity. Copper declined on a low-severity problem: fine.

Corrections:
* `symptoms_seasoned` -- **HOLDS.** PN 7413 "Fruit also can crack, which allows entry of
  secondary organisms." / "Severely affected leaves often turn yellow and drop." / "Pear scab,
  which the fungus V. pirina causes, results in similar blemishes on pear fruit."; guideline, in
  full: "When infections occur early, fruit spots become scablike with age and the fruit may
  become misshapen." "corky" dropped: on neither page. Needed: yes (the Asian-pear sentence was
  missing from both copies).
* `symptoms_beginner` -- **HOLDS.** Same anchors. Needed: yes (adds the Asian-pear sentence).
* `cause_seasoned` -- **HOLDS.** PN 7413 spells "V. pirina"; twig-lesion and 55-75°F / 9 hours
  sentences verbatim above. Needed: yes.
* `prevention_seasoned` -- **HOLDS.** Single-backyard-tree and rainy-weather sentences. Needed:
  yes ("prune for airflow" unanchored; "less-susceptible varieties" European-only).
* `prevention_beginner` -- **HOLDS.** Same. Needed: yes ("Resistant varieties rarely need
  spraying" is on no page).

---

## Pear decline [diseases] -- id pear-decline, bacterial (from other), medium

Anchors read: WSU Tree Fruit pear rootstocks ; UC IPM home pear decline ; UC IPM pear decline
guideline (commercial) ; USU pear decline ; WSU Tree Fruit psylla IPM (organism name).

* `resistant_rootstock` -- **HOLDS on rootstock content; SYNTHESIS/FIT on two clauses (FIX F2,
  F7).** UC IPM home: "Pear decline can rapidly kill pear planted on Asian rootstocks: Pyrus
  pyrifolia (=P. serotina) and P. ussuriensis." / "Tolerant rootstocks include Bartlett seedling,
  Old Home X Farmingdale rooted cutting, Pyrus betulaefolia, and Winter Nelis seedling." / "A
  brown line caused by death of phloem cells develops on the outside of the wood at the graft
  union." / "During hot weather, infected trees on Asian rootstock may develop quick decline;
  foliage wilts rapidly and affected trees die within a few days." / "Reducing the abundance of
  pear psylla will reduce transmission of the phytoplasma." USU: "It kills phloem cells at the
  graft union of specific root-scion combinations, preventing the tree from transporting sugar
  from its top to its roots." / "Sugar accumulates above the graft union as stored starch while
  the roots die from starvation." / "When grafting Asian pear trees over to European (P.
  communis) cultivars, graft below the union of the Asian pear with its rootstock to avoid
  creating a highly decline-susceptible tree". WSU rootstocks: OHxF 87 "The OHxF selections are
  compatible with most pear varieties and are known for their tolerance to blight and decline.";
  OHxF 97 "this rootstock is resistant to pear decline and fireblight."; OHxF 40 "Resistant to
  fire blight, crown rot, woolly pear aphids, and pear decline." (OHxF 333's resistance sentence
  is quoted by the record pass; my extractor returned only its size sentence -- not
  re-confirmed by me, see R7.) Two defects: (a) "psylla is what carries the disease in" states
  psylla as the sole route; USU, an anchor on this entry: "Grafting and budding can also
  transmit this phytoplasma." (b) "Ask for a tree on ... Bartlett seedling" on a crop whose
  limiting disease is fire blight, where Purdue Table 1 (an anchor on this record) prints
  Bartlett Seedling under Pear Rootstocks, Susceptible.
* `garden_sanitation` -- **HOLDS.** USU: "Remove diseased trees"; guideline: "There is no known
  biological control of the pear decline phytoplasma organism." / "Sudden tree collapse can
  result from hypersensitive tissue damage at the graft union on highly susceptible Asian
  rootstocks such as Pyrus serotina or P. ussuriensis." / "a very slow decline when trees are
  not receiving adequate water and nutrition" / "Maintain trees in good vigor by reducing
  stress caused by inadequate irrigation, nutrient deficiency, weed competition, lack of
  pruning, and pest damage."; UC IPM home: "Trees infected with pear decline may benefit from
  increased nitrogen applications and frequent, light irrigations." / "To survive, the pear
  decline phytoplasma requires either a pear tree or the pear psylla." STYLE nit: "kept going
  for years" extends "may benefit". Removal-of-a-collapsed-tree is garden sanitation by the
  catalog's own text ("a plant too far gone to save pulled out, that is garden sanitation").

**REFUSAL WRONG -- FIX F1.** `certified_clean_stock` was refused: "no document in the record
report says anything about certified, tested or clean nursery stock, budwood or scion source
for pear decline; the phytoplasma arrives by psylla". True of the REPORT, false of the DOCUMENT.
USU (this entry's own anchor, https://extension.usu.edu/planthealth/ipm/notes_ag/fruit-pear-decline)
prints: "Grafting and budding can also transmit this phytoplasma." and "On suspect trees, use a
knife to expose the cambium (just under the bark) at the graft union to look for a brown line."
That is the method's exact domain (catalog `certified_clean_stock`: "viruses carried in
cuttings, crowns or divisions ... Set once, at purchase or propagation"; a phytoplasma travels
in wood the same way). The twin (pear-european) authored this rung from the same USU page. The
brief's rule "Where the report quotes a document, and the claim matters, GO TO THE DOCUMENT"
applies with more force to a refusal that asserts a document's silence. Ladder length 2 vs the
twin's 3 is therefore NOT justified on this problem: the third rung is anchored on this crop's
own anchor.

"No cure" replacement (both `organic_treatment_*` fields): **HOLDS** on anchors; needed only
partly. Neither UC IPM page nor USU prints "cure" (each extractor confirmed the word is absent),
so the replacement says what the pages say, and the real gain is the removal-versus-nursing
split (UC IPM home nursing sentence; USU "Remove diseased trees"). The original "No cure" was not
false; the `why` overstates the defect. Acceptable correction.

Corrections:
* `symptoms_seasoned` -- **HOLDS.** UC IPM home symptom sentences verbatim above ("In spring,
  infected trees leaf out more slowly than healthy trees"; "leaves thicken, curl downward, and
  change color prematurely"; brown line). Needed: yes (adds the field diagnostic).
* `cause_seasoned` -- **SYNTHESIS (narrowed) -- FIX F2.** "carried by pear psylla, which injects
  it while feeding" is the only transmission route given; USU "Grafting and budding can also
  transmit this phytoplasma." The rest holds (WSU Tree Fruit "Candidatus Phytoplasma pyri";
  USU mechanism; UC IPM home Asian rootstocks).
* `organic_treatment_seasoned` -- **HOLDS.** Guideline "no known biological control"; UC IPM
  home tolerant list and nursing; USU "Control pear psylla." / "Remove diseased trees".
* `organic_treatment_beginner` -- **HOLDS.** Same.
* `prevention_seasoned` -- **HOLDS with FIX F7.** UC IPM home; USU grafting rule; WSU OHxF. The
  "Bartlett seedling ... also rate tolerant" clause is true of decline and silent on fire blight.
* `prevention_beginner` -- **HOLDS with FIX F7.** "or Bartlett seedling" in a buy instruction.

---

## FIX ITEMS

**F1. Pear decline: missing `certified_clean_stock` rung (refusal WRONG).** Exact refusal text:
"Pear decline certified_clean_stock rung: REFUSED. The brief prescribes it, but no document in
the record report says anything about certified, tested or clean nursery stock, budwood or scion
source for pear decline; the phytoplasma arrives by psylla". Wrong because the entry's own USU
anchor prints: "Grafting and budding can also transmit this phytoplasma." and "On suspect trees,
use a knife to expose the cambium (just under the bark) at the graft union to look for a brown
line." Fix: author the rung (cultural tier; take scionwood only from a tree with a clean union;
buy nursery trees rather than propagate from a declining pear), anchored on usu_ext; the twin's
rung shows the shape.

**F2. Pear decline `cause_seasoned` correction + `resistant_rootstock` note_beginner: vector
narrowed.** Exact text: "carried by pear psylla, which injects it while feeding" (correction) and
"psylla is what carries the disease in" (rung). Wrong because USU: "Grafting and budding can also
transmit this phytoplasma." Fix: add "and by grafting or budding from an infected tree".

**F3. Fire blight `copper_fungicide` note_beginner + `prevention_seasoned` correction: UC IPM's
scope universalized.** Exact text: "Copper is the only spray a home grower can buy for fire
blight" and "Copper at bloom is the only protective spray available to home growers, and it is
partial." PN 7414's sentence is "Copper products are the only materials available to homeowners
for fire blight control" (California). Contradicted on this entry by Purdue "Agri-Strep
(streptomycin), is acceptable for home use, but may be difficult to obtain." and HGIC 2208 "Pear
trees are also treated with a pre-bloom, copper fungicide spray, and then sprays of streptomycin
during bloom." Fix: "Copper is the one fire blight spray most home growers can buy (UC IPM);
streptomycin is sold for home use in some states but is hard to find, and Purdue caps it at
three to four bloom sprays."

**F4. Pear psylla `prevention_beginner` (uncorrected): "A good dormant oil spray in late
winter".** The author retired "in late winter" from `organic_treatment_beginner` on UC IPM home
"Apply horticultural oil at least once during the dormant season and by the beginning of
January." and WSU "They begin laying eggs when pear buds begin to swell.", and left it here.
Fix: declare a correction: "A dormant oil spray before the buds swell".

**F5. Stink bug `weed_host_control` note_seasoned names Rutgers with no key.** Exact text: "The
brown marmorated stink bug is an edge invader that WSU and Rutgers both record moving in from
wooded borders and neighboring crops". The Rutgers sentence exists ("In tree fruit this has
resulted in higher populations near wooded borders and soybean fields.") but `rutgers_njaes` is
on neither `sources` nor `anchoring_urls`. Fix: add the key and URL
(https://pemaruccicenter.rutgers.edu/programs/entomology/pest-management-information/brown-marmorated-stink-bug/)
or drop "and Rutgers".

**F6. Fire blight `prune_out_infection` note_seasoned names WSU twice with no key.** Exact text:
"both UC IPM and WSU report that cut placement matters more than tool sterilization" and "WSU's
12 to 18 in wood two years old or older". Both sentences exist on
https://treefruit.wsu.edu/crop-protection/disease-management/fire-blight/ ("Remove infected
branches 12 to 18 inches below the visibly infected tissue in wood that is two years old or
older"; "sterilizing shears made no difference in preventing canker formation as long as the
cuts are made at the recommended distance"), but `wsu_ext` is not on the entry. Fix: add
wsu_ext with that URL (biology/practice from a commercial page, usable) or drop the attributions.

**F7. Pear decline: "Bartlett seedling" in three buy instructions.** Exact text: note_beginner
"Ask for a tree on an Old Home x Farmingdale rootstock (OHxF 87, 97, 333 or 40) ... or on
Bartlett seedling or birchleaf pear (Pyrus betulifolia)"; `prevention_seasoned` "Bartlett
seedling or Pyrus betulifolia also rate tolerant"; `prevention_beginner` "the OHxF series, or
Bartlett seedling or birchleaf pear". True of decline (UC IPM home "Tolerant rootstocks include
Bartlett seedling"), but this record's fire blight rung tells the same buyer to buy on a
fire-blight-resistant root, and Purdue BP-30-W Table 1, Pear Rootstocks, prints "Susceptible:
Bartlett Seedling, Quince seedling". Fix: keep Bartlett seedling in the seasoned tolerant LIST;
drop it from the "ask for / buy" instructions or add "though Purdue rates it fire-blight
susceptible; OHxF or P. betulifolia covers both diseases".

**F8. Stink bug `organic_treatment_seasoned` correction: "act only on very young nymphs".**
Hortsense: "Chemical management of BMSB is most effective against very young nymphs (immature
insects). Chemical management is NOT RECOMMENDED FOR ADULT INSECTS." Fix: "work best on very
young nymphs, are not recommended against adults, and are toxic to bees".

---

## SUMMARY

Rungs (22): **HOLDS 19**, **SYNTHESIS 2** (pear psylla `balance_nitrogen`, no fix; pear decline
`resistant_rootstock`, F2/F7), **WRONG 1** (fire blight `copper_fungicide` beginner, scope,
F3). Two HOLDS rungs carry an anchoring FIX (F5, F6). **Missing rung 1** (pear decline
`certified_clean_stock`, F1).

Corrections (30): **HOLDS 25**, **WRONG-scope 1** (fire blight `prevention_seasoned`, F3),
**SYNTHESIS 1** (pear decline `cause_seasoned`, F2), **FIT 2** (pear decline
`prevention_seasoned`/`prevention_beginner`, F7), **STYLE 1** (stink bug
`organic_treatment_seasoned`, F8). Uncorrected field carrying a retired claim: 1 (F4).

FIX items: 8 (F1-F8). Refusals: 17 graded RIGHT, 1 WRONG (F1).

Verified as asked: (1) pruning-distance corrections carry the anchors' figures exactly (Purdue
"at least 12 inches"; HGIC 1352 "18 inches"; HGIC 2208 "a minimum of 8 to 12 inches"; WSU "12
to 18"; EC 631 "12 inches"); dormant-season pruning is on HGIC 1352, HGIC 2208 and Purdue, with
PN 7414's spring exception carried; the invasive-species reason for dropping P. calleryana is
HGIC 1352's verbatim. (2) Banding is gone; kaolin is absent from PN 7412; carbaryl carries
"Carbaryl never should be sprayed during bloom or when bees are present." in both registers.
(3) Both psylla oil sentences are on the UC IPM guideline; no note carries a PDD program.
(4) Every stink bug anchor carries what is attached to it; row cover is Hortsense's own
measure, with its after-pollination clause. (5) Scab low rests on PN 7413's Asian-pear
sentence; "prune for airflow" is gone and absent from PN 7413. (6) The "no cure" replacement
holds; the `certified_clean_stock` refusal does not (F1). (7) No sulfur/oil interval anywhere;
PN 7413's "3 weeks" is filed. (8) Scab 2 vs 4: justified. Decline 2 vs 3: NOT justified.

**Single most important finding:** the pear decline `certified_clean_stock` refusal asserts a
silence that the entry's own USU anchor breaks ("Grafting and budding can also transmit this
phytoplasma."). The author refused on the record report instead of the document, and the same
narrowing (psylla as sole vector) then propagated into the `cause_seasoned` correction and the
`resistant_rootstock` note. The twin authored the rung from the same page.

---

## RECORD-LEVEL FINDINGS (filed, not fixed here)

* **R1. `control_methods.prune_out_infection` prints "6 to 8 inches" as the cut distance** ("You
  must cut 6 to 8 inches below visible damage"; "cutting 6 to 8 inches beyond the visible
  margin"). That figure is PN 7414's bark-SCRAPING margin ("remove all discolored tissue plus 6
  to 8 inches more beyond the infection"), not a pruning distance; every pruning distance read
  is 8-12 minimum (HGIC 2208), 12 (Purdue, EC 631), 12-18 (WSU), 18 (HGIC 1352). The method text
  renders on every fire blight ladder (apple, both pears) and undershoots all of them.
* **R2. Codling moth kaolin refusal: right outcome, wrong description.** The refusal and the
  `organic_treatment_seasoned` `why` say the commercial guideline lists kaolin "with no sentence
  on efficacy or timing" / "with no schedule". The row reads: "Serves primarily as a barrier to
  oviposition and to prevent larvae from entering the fruit, so early application and good
  coverage are important. Make the first application at 100 DD after the biofix, and reapply in
  7 to 14 days ... May cause outbreaks of European red mites." It is a commercial DD program
  (FIT-refused correctly); the record's old "degree-day/petal-fall schedule" was a commercial
  program in home prose, which is the actual defect. The catalog's own `kaolin_clay` text
  already rates it "fair to moderate" on codling moth, so the orchestrator could still choose a
  rung on catalog text + a home document, if one is found; PN 7412 has none.
* **R3. Process: a refusal that asserts a document's silence must be checked against the
  document, not the report.** F1 is the case. The record report for this crop did not quote
  USU's grafting sentence; the twin's report did.
* **R4. PLA-457.** `control_methods.horticultural_oil` and `sulfur` cautions both print "2
  weeks"; PN 7413 prints "3 weeks" (filed in the author's notes). Known, pending the ruling.
* **R5. Pear decline typed `bacterial`** makes copper, prune_out_infection, even_watering etc.
  gate-legal on a phytoplasma; none authored. The author's `phytoplasma`-type observation is
  worth a roster ruling; no output defect.
* **R6. Clemson HGIC 1352** (the crop's best home document, newly anchored) names "Codling moths
  and aphids are the most common insect problems in South Carolina." and "Another common
  problem prominent among pear trees is rust disease." Neither aphids nor rust is on the record
  (already flagged by the record pass).
* **R7. WSU rootstocks, OHxF 333:** my extractor returned only "A semi-dwarfing pear rootstock.
  It is 1/2 to 2/3 standard size."; the record pass quotes "Its resistance to fireblight, collar
  rot, woolly pear aphids, and pear decline make this a very healthy stock." Not re-confirmed
  on my read; the seasoned note's "333" claim rests on the record pass.
* **R8. Hortsense psylla says "delayed-dormant"** for oil; the rung's "before the buds swell /
  dormant / by January" is UC IPM's and WSU Tree Fruit's timing, attributed correctly. The two
  home documents differ by a bud stage; not a defect, but a reader in Washington following
  Hortsense will spray later than the note says.
* **R9. Style nits, no fix required:** psylla `organic_treatment_seasoned` correction lists
  kaolin twice; stink bug `handpick` "barrel-shaped" is on no page; codling `garden_sanitation`
  "every week or so" vs PN 7412 "Every week or two, beginning about six to eight weeks after
  bloom"; decline `garden_sanitation` "kept going for years" extends "may benefit".
* **R10. Purdue's copper sentence** ("For plants with a history of infection, apply a copper
  based pesticide like Bordeaux mixture or another dormant spray mixture before bud break") is
  a third copper timing (dormant, pre-bud-break) alongside PN 7414 (bloom, 4-5 day intervals)
  and HGIC 2208 (one spray immediately prior to bloom). The rung carries the UC IPM and Clemson
  programs; Purdue's is not carried. Not a defect; noted for the copper rung's completeness.
