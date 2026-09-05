# PLA-8 batch 26 -- RECORD / SOURCE PASS: pawpaw (`pawpaw`)

Reviewer pass date: 2026-09-04. Canonical ce98b0a6 READ-ONLY; nothing edited but this file.
Read paths used, in order of evidentiary weight: (1) first-party WebFetch of the HTML page;
(2) raw bytes of a PDF that WebFetch downloaded but could not extract, read locally with pypdf
(first-party bytes, my own extraction); (3) the `r.jina.ai` text proxy (weaker). `curl` was denied
by the permission system this session, so no curl path was used. Each anchor below says which path.

The cert log's open finding `pawpaw_minor_pests_uncited` said the peduncle borer and Phyllosticta
"are real but not on the sampled cited pages". Resolution of that finding, per half:
* Peduncle borer: the CITED page (KSU Pawpaw Planting Guide) names *Talponia plummeriana* by
  binomial, gives the 5 mm larva, the wither-and-drop symptom, and "the majority of blossoms" in some
  years, all verbatim (first-party read 2026-09-04). The finding was wrong about this page, or the
  page has changed since 2026-06-30; either way the borer half is CLOSED on the existing anchor.
* Phyllosticta: genuinely ABSENT from both cited pages (UIUC blog confirmed on two paths; KSU
  planting guide names only an unnamed "fungus infection"). The KSU program document that carries
  the binomial is **Organic Production of Pawpaw, PBI-004** (Pomper, Crabtree, Lowe, 2010), and it
  also carries the borer's "does not require control" sentence. That is the tightened anchor.


## Pawpaw peduncle borer [pests]  -- severity medium, type pest
STATUS: SOURCED-WEAK
ORGANISM: *Talponia plummeriana* Busck (Lepidoptera: Tortricidae), per KSU Pawpaw Planting Guide
  (binomial), KSU Organic Production PBI-004 ("Talponia plummeriana Busck"), ACES ANR-3095 ("a moth in
  the family Tortricidae"). NC State toolbox spells it "Talponia plumeriana" (sic); do not copy that.
ANCHORS:
  ksu_pawpaw https://www.kysu.edu/academics/college-ahnr/school-of-anr/pawpaw/pawpaw-planting-guide.php -- verified 2026-09-04 (first-party WebFetch, complete Pests section returned) -- home/general grower guide (Jones, Peterson, Turner, Pomper, Layne; 1998)
  > "In its native habitat the Pawpaw has few pests of any importance. The worst pest is Talponia plummeriana, the Pawpaw peduncle borer, a small moth larva (about 5 mm long) that burrows into the fleshy tissues of the flower, causing the flower to wither and drop. In some years this borer is capable of destroying the majority of blossoms."
  > "Although it requires a little extra labor, hand pollination to ensure fruit set can be well worth the effort and can be done as follows: Using a small, flexible artist's brush, transfer a quantity of fresh pollen from the anthers of the flower of one clone to the ripe stigma of the flower of another clone."
  ksu_pawpaw https://www.kysu.edu/brand-identity-approved-images/pawpaw/OrganicPawpawPBI-004.pdf -- verified 2026-09-04 (raw bytes via pypdf, cross-checked against r.jina.ai; WebFetch direct could not extract) -- pdf, organic PRODUCTION bulletin (Pomper, Crabtree, Lowe, July 2010; linked from the program's Growing Information page under "Kentucky State University Publications")
  > "The pawpaw peduncle borer (Talponia plummeriana Busck) is a small moth larva, about 5 mm long, that burrows into the fleshy tissues of the flower causing the flower to wither and drop."
  > "Usually, the great abundance of unaffected flowers on trees does not require control of this insect."
  mu_ext https://extension.missouri.edu/sites/default/files/legacy_media/wysiwyg/Extensiondata/Pub/pdf/agguides/agroforestry/af1021.pdf -- verified 2026-09-04 (raw bytes via pypdf, cross-checked against r.jina.ai) -- pdf, COMMERCIAL/agroforestry production guide AF1021 "Growing and Marketing Pawpaw in Missouri" (Byers, Cai, Gold, Krishnaswamy, Lin, Lovell, Thomas, Warmund; March 2022); biology usable, cost tables are not home advice
  > "The pawpaw peduncle borer (Talponia plummeriana) is a common pest on trees. The larval stage of this moth feeds on stems, roots, flowers, and flower parts. The first generation of adult moths emerges from twigs in April and May, often when trees are blooming. The adults are brown, speckled with darker wing tips and are small (about 1/4 inch long). As these insects emerge in spring, their pupal cases are visible on twigs. After mating, the female deposits eggs on anthers (male part of the flower) where larvae later hatch. Larvae initially feed on the anthers, then move through the floral tissue, and eventually bore into stems where they continue to consume tissue until they pupate and emerge from the twigs. Their feeding causes the flowers to wither and eventually drop. Because these borers also feed on fruit tissues, there are likely multiple generations of this insect during a growing season. When there are serious outbreaks of this pest, major crop loss occurs."
  cornell_small_farms https://smallfarms.cornell.edu/2018/01/pawpaw-a-tropical-fruit/ -- verified 2026-09-04 (first-party WebFetch) -- small-farm article (Guy K. Ames, 2018-01-08; NCAT/ATTRA material republished by Cornell Small Farms)
  > "There are a few lepidopteran pests (caterpillars), the principal one being the pawpaw peduncle borer. The peduncle borer (Talponia plummeriana) burrows into the pawpaw flower and causes it to drop. Usually, however, so little damage is done that this is not considered a serious problem."
  ncsu_ext https://plants.ces.ncsu.edu/plants/asimina-triloba/ -- verified 2026-09-04 (first-party WebFetch) -- toolbox page, but this is a PROSE sentence under "Insects, Diseases, and Other Plant Problems", not a title row
  > "The pawpaw peduncle borer (Talponia plumeriana) is a small moth whose larvae burrow into flower stalks."
  Also read (not admissible as keyed, see NEEDS-CATALOG-ADMISSION): Ohioline ANR-0207 "Important pests like the peduncle borer (Talponia plummeriana) and the Asian ambrosia beetle (Xylosandrus crassiusculus) do not have registered products for use on pawpaws."; VCE 2906-1319 "Though this damage is minor, in certain years the borer can destroy many flowers." and "Currently, with limited or no registered chemical options for pest control in pawpaw, 'organic' methods are the only option."; UKY CCD-CP-14 "Pawpaw peduncle borer larvae feed on the stems of flowers, resulting in flower drop, and also have been found boring into twigs and fruit."; Purdue HO-220-W (2001, purdue_ext-admissible, raw bytes via pypdf) repeats the KSU planting-guide sentences verbatim including "In some years this borer is capable of destroying the majority of blossoms."
RECORD CLAIMS THAT HOLD:
  * Organism = Talponia plummeriana, a small moth; larva ~5 mm; burrows in the fleshy flower tissue; flower wilts and drops instead of setting fruit -- ksu_pawpaw planting guide (verbatim), ksu_pawpaw PBI-004, ncsu_ext toolbox prose.
  * "In a bad year the borer can destroy the majority of a tree's blossoms" / "swings widely from one season to the next" -- ksu_pawpaw planting guide "In some years this borer is capable of destroying the majority of blossoms."
  * "There is no practical spray for a backyard tree" -- carried in substance by ksu_pawpaw PBI-004 "does not require control of this insect"; the stronger "no registered products" wording exists only in Ohioline ANR-0207 and VCE 2906-1319 (not keyed).
  * "tunneling in the fleshy flower stalk (the peduncle) and floral tissue" -- ncsu_ext "burrow into flower stalks"; mu_ext "move through the floral tissue, and eventually bore into stems".
  * Hand pollination is worth doing on pawpaw -- ksu_pawpaw planting guide, mu_ext (as a FRUIT-SET measure; see below).
RECORD CLAIMS WITH NO ANCHOR:
  * "gather and destroy dropped, infested flowers to reduce the local population" / "pick up and throw away the fallen, damaged flowers to lower their numbers" -- no document read prescribes flower sanitation for this borer. ACES ANR-3095 has only a blanket "Trapping, manual removal, and orchard cleanliness and sanitation are recommended to combat these pests." spanning its whole insect list (commercial). MU's only "To control this pest, infested parts of the tree can be pruned and removed from the site." is about the Asimina WEBWORM (checked in context), not the borer.
  * "lean on hand pollination of the healthy flowers to secure a crop despite the losses" / "protecting fruit set is more about pollination insurance than eradication" -- every source recommends hand pollination for FRUIT SET in general (KSU, MU, Clemson, VCE, UKY, Cornell); none frames it as a borer countermeasure. Inference, not a sourced claim.
  * "Damage is rarely fatal to the tree and often eases the following year" / "usually less of a problem the next year" -- no document says either.
  * "Open flowers wilt, blacken, and drop" -- sources say "wither and drop"; no document says blacken. "small pale caterpillar" -- no document gives larval color (MU describes only the adult).
RECORD CLAIMS THAT ARE WRONG:
  * "Keep the ground under the tree clear of fallen flowers and debris where the borer can complete its cycle" / "Rake up and remove fallen flowers so the borer cannot keep its cycle going under the tree" -- refuted by mu_ext AF1021: "Larvae initially feed on the anthers, then move through the floral tissue, and eventually bore into stems where they continue to consume tissue until they pupate and emerge from the twigs." and "As these insects emerge in spring, their pupal cases are visible on twigs." The cycle completes in the TWIG, not on the ground; raking dropped flowers is off-target. UKY corroborates ("also have been found boring into twigs and fruit"). This is the entry's whole organic-treatment and prevention block.
BUNDLE / GENERIC VERDICT: n/a (single pinned organism).
LADDER-RELEVANT FACTS the record does not carry:
  * Life cycle and monitoring signal (mu_ext): first-generation adults emerge from TWIGS in April-May at bloom; pupal cases visible on twigs then; eggs laid on the anthers; larvae feed anthers -> floral tissue -> bore into the stem; likely multiple generations; larvae also feed in fruit (UKY, MU; a journal paper in J. Kentucky Acad. Sci. 73(2) documents infestation of ripe fruit -- JOURNAL, not needed as anchor).
  * "No effective control" wording, exact: ksu_pawpaw PBI-004 "Usually, the great abundance of unaffected flowers on trees does not require control of this insect."; cornell_small_farms "so little damage is done that this is not considered a serious problem."; Ohioline ANR-0207 / VCE 2906-1319 "no registered products" / "limited or no registered chemical options" (not keyed). No document names ANY product, organic or conventional, for this borer, so the ladder has no soft-chemical or conventional rung to cite.
  * The one thing a home grower can do that a source actually says: hand-pollinate for fruit set generally (KSU planting guide gives the method: brush pollen from brown, loose, friable anthers of one clone to green, glossy stigmas of another).
  * Severity framing: sources range from "the worst pest" (KSU) / "may be the most severe pest" (VT ento, 2006) to "not considered a serious problem" (Cornell SF). "medium" is defensible; the text must carry the year-to-year swing.
  * No resistant cultivar is named anywhere.
PLA-457: none seen.


## Zebra swallowtail caterpillars [pests]  -- severity low, type pest
STATUS: SOURCED-OK (anchor carries the sole-host claim; add ksu_pawpaw + umd_ext for the "never in great numbers" and "do not treat" claims, which the UIUC page does not carry)
ORGANISM: *Protographium marcellus* (Cramer), per umd_ext (Native Trees of Maryland); the same species appears as *Eurytides marcellus* on ksu_pawpaw (planting guide, PBI-004, PBI-0031), clemson_hgic, ncsu_ext, Ohioline, VT ento, Purdue, MU, ACES. Both names are in current extension use; the record's Protographium is fine, carry Eurytides as a synonym so the id stays findable.
ANCHORS:
  uiuc_ext https://extension.illinois.edu/blogs/good-growing/2024-08-02-pawpaw-americas-tropical-treasure -- verified 2026-09-04 (first-party WebFetch; second path r.jina.ai agrees) -- home (Good Growing blog, Emily Swihart, 2024-08-02)
  > "Pawpaw is the only host plant for zebra swallowtail butterfly caterpillars."
  > "It has no serious pests or disease issues and is not preferred by deer."
  ksu_pawpaw https://www.kysu.edu/academics/college-ahnr/school-of-anr/pawpaw/pawpaw-planting-guide.php -- verified 2026-09-04 (first-party WebFetch) -- home/general
  > "Another pest is Eurytides marcellus, the zebra swallowtail butterfly, whose larvae feed exclusively on young pawpaw foliage, but never in great numbers. The adult butterfly is of such great beauty that this should be thought more a blessing than a curse."
  ksu_pawpaw https://www.kysu.edu/brand-identity-approved-images/pawpaw/OrganicPawpawPBI-004.pdf -- verified 2026-09-04 (raw bytes via pypdf + r.jina.ai) -- pdf, organic production
  > "The zebra swallowtail butterfly (Eurytides marcellus), whose larvae feed exclusively on young pawpaw foliage, will damage leaves, but this damage has been negligible."
  umd_ext https://extension.umd.edu/resource/less-common-fruits-home-garden -- verified 2026-09-04 (first-party WebFetch) -- HOME garden (Miri Talabac, reviewed Jon Traunfeld; updated 2026-04-14)
  > "Few insects feed on pawpaw foliage, and they do not cause enough damage to warrant treatment."
  > "Pawpaw is the only host plant (caterpillar food) for zebra swallowtail butterflies."
  umd_ext https://extension.umd.edu/resource/native-trees-maryland-pawpaw-asimina-triloba -- verified 2026-09-04 (first-party WebFetch + r.jina.ai) -- home/landscape (Lisa Kuder, updated 2025-05-23)
  > "They're the host plant for larvae of the zebra swallowtail butterfly (Protographium marcellus)"
  clemson_hgic https://hgic.clemson.edu/factsheet/pawpaw/ -- verified 2026-09-04 (first-party WebFetch, complete Problems section) -- home (HGIC 1360, rev. 2022-01-28)
  > "Pawpaw is the exclusive larval (caterpillar) host plant for the zebra swallowtail (Eurytides marcellus), but their feeding on leaves rarely results in much damage to mature trees."
  ncsu_ext https://plants.ces.ncsu.edu/plants/asimina-triloba/ -- verified 2026-09-04 -- toolbox page, prose sentence (not a title row)
  > "The zebra swallowtail butterfly larvae feed on young leaves, but they seldom do permanent damage."
  Also read: Ohioline ANR-0187 (not keyed) "the larvae of the Zebra swallowtail butterfly (Eurytides marcellus) feed on pawpaw foliage but seldom cause production losses. Pawpaw is the primary host plant in North America for the Zebra swallowtail butterfly"; VT ento (2006) "North of Florida, Asimina triloba is the exclusive host for the caterpillar. The caterpillar rarely feeds on the foliage in numbers great enough to reduce the yield."; UT D234-C (not keyed) "Another interesting note and reason for low insecticide use is that pawpaw is the larval host for the Zebra Swallowtail Butterfly."; cornell_ext LOF page "caterpillars of the zebra swallowtail butterfly are happy to munch on pawpaw foliage" / "Look for smooth-skinned caterpillars with a prominent hunchback".
RECORD CLAIMS THAT HOLD:
  * Sole larval host -- uiuc_ext "only host plant"; clemson_hgic "exclusive larval (caterpillar) host plant"; umd_ext "only host plant"; ksu_pawpaw "feed exclusively on young pawpaw foliage". (Nuance: VT scopes exclusivity to "North of Florida", where other Asimina species also host; Ohioline says "primary". Fine for this roster.)
  * Feeds on YOUNG foliage -- ksu_pawpaw, ncsu_ext.
  * "never appear in numbers large enough to defoliate" / "never in big numbers" -- ksu_pawpaw planting guide "but never in great numbers" (verbatim "never"; the other sources say "rarely"/"seldom"/"negligible").
  * "far more a delight than a threat" -- ksu_pawpaw "this should be thought more a blessing than a curse."
  * "No treatment is warranted" / "Do nothing" -- umd_ext Less Common Fruits "they do not cause enough damage to warrant treatment"; ksu_pawpaw PBI-004 "this damage has been negligible".
  * Damage light and cosmetic -- clemson_hgic "rarely results in much damage to mature trees"; ncsu_ext "seldom do permanent damage".
RECORD CLAIMS WITH NO ANCHOR:
  * "green-and-black banded caterpillar" / "striped green-and-black caterpillar" -- no admissible document describes the larva's color; cornell_ext's only description is "smooth-skinned caterpillars with a prominent hunchback". Either drop the color or leave it as an unsourced identification aid (low risk, but it is unanchored).
RECORD CLAIMS THAT ARE WRONG: none found.
BUNDLE / GENERIC VERDICT: n/a.
LADDER-RELEVANT FACTS the record does not carry:
  * Clemson's qualifier is "mature trees"; no source says young trees are at risk either, but the no-action advice is stated for established trees.
  * The explicit home-audience "do not treat" sentence is UMD's (Less Common Fruits, 2026), which covers ALL foliage insects on pawpaw, not this species alone; use it as the ladder's stop rung.
  * Timing: larvae feed on new/young foliage (KSU, NCSU), so spring-summer; no source gives dates or generations.
PLA-457: none seen.


## Fruit-raiding wildlife (raccoons, opossums, squirrels) [pests]  -- severity medium, type pest
STATUS: SOURCED-WEAK (umd_ext names all three animals verbatim; psu_ext names none; the netting/baffle management is unanchored; the deer sub-claim is contradicted on the fruit half by the crop's own program and two more T1s)
ORGANISM: umbrella -- multiple vertebrates. Per document: raccoons (*Procyon lotor*), opossums (*Didelphis virginiana*), squirrels, foxes, plus black bears, feral pigs, songbirds, wild turkeys, mice, and deer on dropped fruit (see per-animal table). No document gives binomials; common names only.
ANCHORS:
  umd_ext https://extension.umd.edu/resource/native-trees-maryland-pawpaw-asimina-triloba -- verified 2026-09-04 (first-party WebFetch + r.jina.ai) -- home/landscape
  > "Also, its fruits (August-October) are eaten by foxes, opossums, raccoons, and squirrels."
  > "Deer, however, generally leave pawpaws alone. Chemicals in the bark and foliage make them unpalatable to deer."
  umd_ext https://extension.umd.edu/resource/less-common-fruits-home-garden -- verified 2026-09-04 (first-party WebFetch) -- HOME garden
  > "Deer avoid browsing pawpaw foliage, but bucks may rub antlers on trunks, potentially causing serious bark injury if trees are unprotected. Various wild animals will eat fallen fruits."
  > "It is normal for ripe pawpaw fruits to be quite soft when ready for harvest. If picked slightly under-ripe, they should finish ripening off the tree, but if picked too early and firm, they will not."
  ksu_pawpaw https://www.kysu.edu/academics/college-ahnr/school-of-anr/pawpaw/enemies.php -- verified 2026-09-04 (first-party WebFetch) -- "Enemies" section of The Pawpaw (M. Brett Callaway, 1990; web conversion 1998), literature review
  > "Asimina spp. are thought to be troubled by very few pests. Birds and mammals such as foxes, opossums, squirrels, and raccoons eat the fruit."
  ksu_pawpaw https://www.kysu.edu/brand-identity-approved-images/pawpaw/ForestPawpawPBI-0031.pdf -- verified 2026-09-04 (raw bytes via pypdf + r.jina.ai) -- pdf, forest production (Pomper, Crabtree, Oct 2009)
  > "Patches serve an important role in ecosystems around rivers and streams, providing fruit and cover for animals (deer, raccoons, squirrels, etc.), reducing erosion, and enhancing insect biodiversity."
  ksu_pawpaw https://www.kysu.edu/academics/college-ahnr/school-of-anr/pawpaw/pawpaw-planting-guide.php -- verified 2026-09-04 (first-party WebFetch) -- home/general
  > "Deer will not eat the leaves or twigs, but they will eat fruit that has dropped on the ground. Male deer occasionally damage trees by rubbing their antlers on them in winter."
  clemson_hgic https://hgic.clemson.edu/factsheet/pawpaw/ -- verified 2026-09-04 (first-party WebFetch) -- home
  > "Foxes, feral pigs, opossums, and raccoons eat the fruit. Deer do not feed on the leaves or twigs, but they will eat the ripe fruit. Sap beetles, bumble bees, and butterflies are also fond of ripe fruit once it falls to the ground."
  > "The fruit should not be harvested until the skin gives (indents) slightly with a finger squeeze as fruit do not ripen properly if picked when very firm."
  ncsu_ext https://plants.ces.ncsu.edu/plants/asimina-triloba/ -- verified 2026-09-04 -- toolbox page; "Wildlife Value" is a PROSE sentence (the "Resistance To Challenges: Deer" row is a title row and is NOT used here)
  > "Its fleshy fruits are eaten by songbirds, wild turkeys, squirrels, raccoons, opossums, black bears, and foxes."
  mu_ext (AF1021, as above) -- verified 2026-09-04 (raw bytes via pypdf + r.jina.ai) -- pdf, COMMERCIAL
  > "Small mammals, including raccoons, opossums, and foxes will eat pawpaw fruit. These pests can be removed from the site by trapping. Fortunately, deer, goats, and rabbits do not usually eat pawpaw leaves or twigs."
  aces_ext https://www.aces.edu/blog/topics/crop-production/pawpaw-production-guide/ -- verified 2026-09-04 (first-party WebFetch) -- COMMERCIAL production guide ANR-3095 (Akers-Campbell, Britton, Akotsen-Mensah; 2024-07-31)
  > "Deer will not eat leaves or twigs but will consume fallen fruit."
  > "Pick pawpaws off the tree when flesh first starts to soften, since they quickly deteriorate." / "Trees should be checked and harvested every day during the harvest period for the best fruit quality."
  uiuc_ext (blog, as above) -- verified 2026-09-04 -- home
  > "To successfully harvest the fruit, diligence is necessary. The ripe fruit is prized by wildlife and quickly eaten." / "Immature fruit may be harvested and will ripen indoors at room temperature."
  psu_ext https://extension.psu.edu/the-native-pawpaw-tree -- verified 2026-09-04 (first-party WebFetch + r.jina.ai) -- home (John Esslinger; updated 2023-09-25). Names NO mammal by species; carries only:
  > "Reports are that deer do not prefer to eat pawpaw trees or the fruit. Birds and other forest animals will feed on ripe pawpaw fruit."
  Also read: Ohioline ANR-0187 (not keyed) "the fruit is often consumed and then its seeds are dispersed by wildlife including opossums, raccoons, squirrels, deer, foxes, bears, and some birds."; VT ento (2006) "Other predators of the fruit include raccons, squirrels, foxes and mice. Deer, rabbits, and goats do not feed on leaves and twigs."; Purdue HO-220-W (2001, purdue_ext, raw bytes) "Deer do not feed on the leaves, twigs, or fruit."; VCE 2906-1319 (not keyed) "Deer are not known to readily eat twigs or foliage, but bucks will use young trees to rub velvet from antlers in the fall."
PER-ANIMAL TABLE (which admissible document names which animal as a pawpaw fruit eater):
  * raccoons  -- umd_ext (Native Trees); ksu_pawpaw (Enemies 1990; Forest PBI-0031); clemson_hgic; ncsu_ext; mu_ext. [also Ohioline, VT]
  * opossums  -- umd_ext; ksu_pawpaw (Enemies 1990); clemson_hgic; ncsu_ext; mu_ext. [also Ohioline]. NOT in KSU Forest, NOT in VT.
  * squirrels -- umd_ext; ksu_pawpaw (Enemies 1990; Forest PBI-0031); ncsu_ext. [also Ohioline, VT]. NOT in Clemson, NOT in MU.
  * foxes     -- umd_ext; ksu_pawpaw (Enemies); clemson_hgic; ncsu_ext; mu_ext. [also Ohioline, VT]. The record omits foxes; every document that names the three record animals also names foxes.
  * deer (dropped/ripe fruit only) -- ksu_pawpaw planting guide; clemson_hgic; aces_ext. [also Ohioline]. Contradicted by Purdue HO-220-W (2001) and hedged by psu_ext.
  * others -- black bears (ncsu_ext; Ohioline), feral pigs (clemson_hgic), songbirds + wild turkeys (ncsu_ext), birds (psu_ext; ksu Enemies; Ohioline), mice (VT), sap beetles/bumble bees/butterflies on fallen fruit (clemson_hgic).
  * Management distinguished BY ANIMAL: only mu_ext, and only as "These pests can be removed from the site by trapping." for raccoons/opossums/foxes (commercial orchard). No document differentiates squirrels from raccoons, or gives per-species advice. No document mentions netting or trunk baffles for pawpaw.
RECORD CLAIMS THAT HOLD:
  * Raccoons, opossums, squirrels eat the fruit -- umd_ext (all three, verbatim), ksu_pawpaw Enemies (all three), ncsu_ext (all three).
  * Fruit is taken quickly as it ripens; be diligent -- uiuc_ext "prized by wildlife and quickly eaten... diligence is necessary".
  * Ripe pawpaw is strongly aromatic -- ksu_pawpaw FAQ "Ripe pawpaws usually give off a powerful fruity aroma"; uiuc_ext "an intense aroma". (No document says the aroma is what draws the animals; the record's causal link is an inference.)
  * Pick when the fruit first starts to soften and finish ripening indoors -- aces_ext "when flesh first starts to soften"; uiuc_ext "will ripen indoors at room temperature"; umd_ext "If picked slightly under-ripe, they should finish ripening off the tree". Clemson and UMD both warn that fruit picked FIRM will not ripen, so keep the record's "as they begin to soften" and never let it drift to "pick firm".
  * Check the tree daily through the harvest window -- aces_ext (commercial, for fruit quality) "checked and harvested every day during the harvest period".
  * Deer avoid the FOLIAGE -- ksu_pawpaw, clemson_hgic, aces_ext, umd_ext (both pages), mu_ext, uiuc_ext, psu_ext: unanimous.
RECORD CLAIMS WITH NO ANCHOR:
  * "Netting or trunk baffles help where pressure is heavy" / "a baffle on the trunk can help" -- no document read mentions netting or baffles on pawpaw. MU's only physical measure is trapping (commercial) and its cost table lists "Deer control (cages)".
  * "Deer ... browsers" framing and the omission of antler rubbing -- see below.
RECORD CLAIMS THAT ARE WRONG:
  * "Deer, by contrast, avoid the foliage and fruit" / "they avoid pawpaw leaves and fruit" -- the fruit half is refuted by the crop's own program and two more T1s: ksu_pawpaw planting guide "Deer will not eat the leaves or twigs, but they will eat fruit that has dropped on the ground."; clemson_hgic "Deer do not feed on the leaves or twigs, but they will eat the ripe fruit."; aces_ext "Deer will not eat leaves or twigs but will consume fallen fruit."; Ohioline ANR-0187 lists deer among fruit consumers. The only verbatim support for "not the fruit" is Purdue HO-220-W (2001) "Deer do not feed on the leaves, twigs, or fruit." (a page that otherwise reproduces the KSU planting guide word for word but with this sentence altered) and psu_ext's hedged "Reports are that deer do not prefer to eat pawpaw trees or the fruit." Sources are split 4:2 with the specialist program on the "deer eat dropped fruit" side. Recommend: deer avoid foliage and twigs; they DO scavenge dropped/ripe fruit; the real deer damage is buck antler rub on young trunks (ksu_pawpaw "Male deer occasionally damage trees by rubbing their antlers on them in winter."; umd_ext "bucks may rub antlers on trunks, potentially causing serious bark injury if trees are unprotected"; VCE "in the fall").
BUNDLE / GENERIC VERDICT: ONE problem, a genuine umbrella. Every document that names the animals names them as a group in one sentence, and no document except MU (trapping, commercial) distinguishes management by species; the home advice everywhere is the same (harvest promptly at first softening, do not leave ripe fruit on the tree or ground). Keep a single `vertebrate` entry. Two decisions for the orchestrator: (1) foxes appear in every list alongside the three named animals; add or name the group generically; (2) deer belong in this entry as dropped-fruit scavengers plus antler rub (physical trunk damage on young trees, protect with a trunk guard), NOT as "the exception that avoids the fruit". Antler rub could alternatively be its own physical problem; the sources treat it in the same breath as fruit-eating.
LADDER-RELEVANT FACTS the record does not carry:
  * Vulnerable window: fruit ripening, late Aug to early Oct depending on cultivar (ksu_pawpaw PBI-004/PBI-0031 "fruit ripen in late-August to early-October"; umd_ext "Maryland peak season is around mid-September"); each tree ripens over ~2 weeks (PBI-0031).
  * Ripeness signals to pick on: gives when squeezed like a ripe peach, pulls off with a gentle tug, powerful aroma; color change is NOT reliable (ksu_pawpaw FAQ "Color change is generally not a reliable indicator of ripeness.").
  * Storage: 5-7 days at room temperature, up to 3 weeks refrigerated (ksu_pawpaw PBI-004); uiuc_ext "up to two weeks" refrigerated unripe.
  * Physical/biological rungs a source actually names: trapping (mu_ext, commercial only); "protection from wildlife damage" and deer cages (mu_ext, commercial cost line); trunk protection against antler rub (umd_ext "if trees are unprotected"). NOTHING for netting.
  * Sap beetles, bumble bees and butterflies work fallen ripe fruit (clemson_hgic): a reason to clear drops.
PLA-457: none seen.


## Phyllosticta leaf and fruit spot [diseases]  -- severity low, type disease
STATUS: ANCHOR-MISPOINTED (organism is real and T1-anchorable, but neither cited page names it; and the record's "cosmetic, fruit inside remains sound" framing is contradicted by the documents that do name it)
ORGANISM: *Phyllosticta asiminae*, as part of a leaf-spot complex with *Mycocentrospora asiminae* and *Rhopaloconidium asiminae*, per ksu_pawpaw PBI-004, aces_ext ANR-3095, mu_ext AF1021; clemson_hgic names *Phyllosticta asiminae* alone as "bordered leaf spot"; Ohioline gives "bordered leaf spot (Phyllosticta sp.)". Distinct from flyspeck (*Zygophiala jamaicensis*) and sooty blotch, which ARE the cosmetic surface fungi (clemson_hgic, cornell_small_farms, aces_ext) and which the record appears to have merged into this entry.
ANCHORS (current):
  uiuc_ext https://extension.illinois.edu/blogs/good-growing/2024-08-02-pawpaw-americas-tropical-treasure -- verified 2026-09-04 (first-party WebFetch AND r.jina.ai: "Phyllosticta", "leaf spot", "fungus", "fungal", "fungi" each ABSENT) -- home. Carries only:
  > "It has no serious pests or disease issues and is not preferred by deer."
  > "Ripening fruit may also develop black blotches, and an intense aroma."  (this is a RIPENING sign in context, not a disease statement; do not read it as Phyllosticta)
  ksu_pawpaw planting guide -- verified 2026-09-04 (first-party) -- carries an UNNAMED fungus only:
  > "Sometimes the fruit surface may be covered with patches that are hard and black; this is a fungus infection, but it seldom has any effect on flavor or edibility."
ANCHORS (found; the sweep target):
  ksu_pawpaw https://www.kysu.edu/brand-identity-approved-images/pawpaw/OrganicPawpawPBI-004.pdf -- verified 2026-09-04 (raw bytes via pypdf + r.jina.ai) -- pdf, organic production
  > "Pawpaw leaves can exhibit leaf spot, principally a complex of Mycocentrospora asiminae, Rhopaloconidium asiminae, and Phyllosticta asiminae."
  > "Especially during wet years, fungal spot (Phyllosticta species) on leaves and the surface of fruit can lead to problems; infested fruit can to split during development."  [sic, "can to split" is in the source]
  > (photo caption) "Fungal spot (Phyllosticta) on fruit leading to cracking."
  clemson_hgic https://hgic.clemson.edu/factsheet/pawpaw/ -- verified 2026-09-04 (first-party, complete Problems section) -- home
  > "A severe fungal disease, bordered leaf spot (Phyllosticta asiminae), occurs in humid climates and infects leaves and fruit. This disease causes hard black spots to form on the fruit skin, which often merge and leads to premature cracking. Leaves are affected too, but the tree is not killed. Some fungicides may control it, but there are no fungicides labeled for use on pawpaws."
  > "A cosmetic fungal disease known as flyspeck (Zygophiala jamaicensis), has been reported on pawpaw. However, the fungus only grows on the surface of the fruit and does not prevent it from being edible."
  mu_ext AF1021 -- verified 2026-09-04 (raw bytes via pypdf + r.jina.ai) -- pdf, commercial; biology usable
  > "One of the frequent diseases found on leaves and fruit is leaf spot, which is a fungal disease caused by a complex of fungi, including Mycocentrospora asiminae, Rhopaloconidium asiminae, and Phyllosticta asiminae. When foliage or fruit remains wet from rainfall or dew for a prolonged period of time, infection can occur. Symptoms of this disease first appear as tan spots with brown borders, but later form dark brown to black lesions. Symptoms are similar on the fruit, but lesions can eventually crack open. When the flesh is exposed from cracking, it quickly becomes infected with other disease organisms and insects, resulting in unmarketable fruit."
  aces_ext ANR-3095 -- verified 2026-09-04 (first-party) -- commercial
  > "Leaf spot, a fungal disease caused by a complex of Mycocentrospora asiminae, Rhopaloconidium asiminae, and Phyllosticta asiminae, is found on leaves and fruit." / "Infection occurs when leaves remain wet for an extended period." / "The disease sooty blotch, caused by several fungi, appears as surface blemishes on the fruit."
  cornell_small_farms (Ames 2018) -- verified 2026-09-04 (first-party) -- small farm
  > "Phyllosticta and flyspeck or greasy blotch (Zygophiala jamaicensis) can be problems of pawpaw. This occurs only during periods of high humidity and frequent rainfall. Dense foliage and lack of proper ventilation contribute to this condition, so proper spacing and pruning can reduce it. Phyllosticta can infect the leaves and the surface of the fruit; it can also cause the fruit to crack when it expands, reducing quality and storability. There appears to be some variation in susceptibility among varieties, but nothing comprehensive has yet been published in this regard."
  ncsu_ext https://lee.ces.ncsu.edu/news/spots-on-my-leaves-phyllosticta-species-in-the-landscape/ -- verified 2026-09-04 (first-party) -- home/landscape county article (Amanda Bratcher, 2023-06-23, updated 2025-07-31); about Phyllosticta species generally, written from a pawpaw case. Scope note: a county site under *.ces.ncsu.edu, same domain family as the toolbox the key names.
  > "I had an old, familiar foe arrive this week: Phyllosticta on a paw paw leaf (Asimina triloba)."
  > "If you do have Phyllosticta, it is best to remove the leaf litter from beneath the infected plants as the leaves fall." / "Do not compost these leaves and debris." / "If it is a small infestation you can pick the leaves off, and sterilize your tools and hands between treatments." / "There are chemical options available for treatment of the pathogen."
  Also read: UKY CCD-CP-14 (not keyed) "Phyllosticta, a complex of several fungi, may produce a black, superficial growth that covers fruit. Phyllosticta can be especially troublesome on pawpaws in years of frequent rainfall."; UT D234-C (not keyed) "a fungal disease that can cause fruit to crack and have a black superficial growth covering the fruit"; VCE 2906-1319 (2009) still says "The only disease reported on pawpaws is fly speck or greasy blotch (Zygophiala jamaicensis)." (outdated; superseded by the 2010+ documents above); ksu_pawpaw Enemies (1990) likewise names only flyspeck.
RECORD CLAIMS THAT HOLD:
  * Fungi in the Phyllosticta group "and similar leaf-spot fungi" -- ksu_pawpaw PBI-004, aces_ext, mu_ext (a three-species complex).
  * Small tan-to-brown leaf spots; dark blotches on fruit skin -- mu_ext "tan spots with brown borders... dark brown to black lesions"; clemson_hgic "hard black spots"; ksu_pawpaw "patches that are hard and black".
  * Worst in warm, wet, humid weather; wet foliage -- ksu_pawpaw PBI-004 "Especially during wet years"; mu_ext / aces_ext "remains wet"; cornell_small_farms "high humidity and frequent rainfall"; clemson_hgic "humid climates".
  * Dense canopy favors it; give trees room and airflow -- cornell_small_farms "Dense foliage and lack of proper ventilation contribute to this condition, so proper spacing and pruning can reduce it."
  * Rake and remove fallen spotted leaves -- ncsu_ext Lee County (generic Phyllosticta advice, stated on a pawpaw case): "remove the leaf litter from beneath the infected plants as the leaves fall."
  * "does not defoliate a healthy tree" / tree not harmed -- clemson_hgic "the tree is not killed" (weaker than the record's wording, but compatible).
  * "Pawpaw is otherwise notably free of serious disease" -- clemson_hgic "Pawpaws are generally pest-free plants"; uiuc_ext "no serious pests or disease issues".
  * "No fungicide is warranted" -- holds only in the form "no fungicide is LABELED": clemson_hgic "Some fungicides may control it, but there are no fungicides labeled for use on pawpaws." Rewrite to that.
RECORD CLAIMS WITH NO ANCHOR:
  * "avoid overhead wetting of the foliage" / "avoid wetting the leaves when you water" -- no pawpaw document says it; the mechanism (prolonged leaf wetness, mu_ext/aces_ext) makes it a reasonable inference, but it is unsourced.
  * "keep the tree vigorous" -- no document ties vigor to this disease.
RECORD CLAIMS THAT ARE WRONG:
  * "The spotting is cosmetic: it does not defoliate a healthy tree or spoil the flesh, and the fruit inside remains sound." / "the spots are just on the surface, do not harm the tree, and the fruit inside is fine" / "The fruit is unaffected inside and fully edible." -- refuted for Phyllosticta by clemson_hgic ("A severe fungal disease... which often merge and leads to premature cracking"), mu_ext ("lesions can eventually crack open. When the flesh is exposed from cracking, it quickly becomes infected with other disease organisms and insects"), ksu_pawpaw PBI-004 ("infested fruit can to split during development" / "leading to cracking"), cornell_small_farms ("cause the fruit to crack when it expands, reducing quality and storability"). The cosmetic description is TRUE of flyspeck (clemson_hgic: "cosmetic... does not prevent it from being edible") and of the unnamed surface fungus in the KSU planting guide ("seldom has any effect on flavor or edibility"); the record has fused the two. The honest consumer statement: superficial black blotching alone does not spoil the fruit; in wet years the same complex cracks the fruit and the cracks let rot in.
  * "No fungicide is warranted for what is a cosmetic issue" -- the reason is wrong (see above); the conclusion survives only as "none is labeled for pawpaw".
BUNDLE / GENERIC VERDICT: not bundled as named, but the record's PROSE bundles two problems: the cracking leaf-and-fruit spot complex (Phyllosticta asiminae et al.) and the cosmetic surface fungi (flyspeck / sooty blotch). Keep the id and name for the Phyllosticta complex; decide whether flyspeck/sooty blotch deserve a separate low-severity "cosmetic surface blotch" entry or a one-line mention inside this one. Severity "low" is defensible for a home tree in a normal year; the text must say wet years crack fruit.
LADDER-RELEVANT FACTS the record does not carry:
  * No fungicide is labeled for pawpaw (clemson_hgic, home audience) -- the conventional rung is closed by label, not by choice. NCSU Lee says "There are chemical options available for treatment of the pathogen" but names none and is generic to the genus.
  * Cultural rungs a source names: spacing and pruning for ventilation (cornell_small_farms); remove leaf litter as leaves fall and do not compost it; pick off leaves in a small infestation; sterilize tools/hands (ncsu_ext Lee County).
  * Vulnerable stage: prolonged leaf/fruit wetness from rain or dew (mu_ext, aces_ext); fruit cracks "when it expands" (cornell_small_farms), i.e. during fruit sizing; wet years are the bad years (ksu_pawpaw PBI-004; UKY "years of frequent rainfall").
  * Overwintering site: not stated for pawpaw by any document read; the leaf-litter prescription (ncsu_ext) implies fallen leaves.
  * Cultivar susceptibility: "some variation... but nothing comprehensive has yet been published" (cornell_small_farms); no resistant cultivar named anywhere.
  * Secondary consequence: cracked fruit is colonized by other organisms and insects (mu_ext), so cracked fruit should be picked and removed.
PLA-457: none seen (ksu_pawpaw PBI-004 swept for sulfur, oil, copper, kaolin, neem, spinosad, Bt, fungicide, insecticide: zero hits; the only "oil" in it is "soil solarization").


## DOCUMENTS CHECKED (absence findings above are scoped to exactly these)
First-party WebFetch, readable: KSU pawpaw index; KSU Planting Guide (twice, complete Pests section); KSU FAQ (pawpaw-faq-and-contact-information.php and questions-about-pawpaw.php); KSU Description and Nutrition; KSU Growing Information (headings/links only on WebFetch, full link list via proxy); KSU "The Pawpaw" (Callaway 1990) table of contents and its enemies.php; UIUC Good Growing blog; UMD Native Trees of Maryland; UMD Less Common Fruits for a Home Garden; PSU The Native Pawpaw Tree; Ohioline ANR-0187 and ANR-0207; Clemson HGIC 1360 (twice); ACES ANR-3095 (twice); NCSU Plant Toolbox Asimina triloba; NCSU Lee County Phyllosticta article; Cornell Small Farms (Ames 2018, twice); Cornell Lake Ontario Fruit Program "Pawpaws in New York"; Cornell berries blog "Pawpaw Production Guide"; Virginia Tech Dept of Entomology "The Pawpaw" (McClanan & Pfeiffer 2006, twice); Purdue HO-220-W landing page; Purdue NewCROP factsheet (Layne 1995; KSU-authored, hosted at hort.purdue.edu).
PDF raw bytes read locally with pypdf after WebFetch saved but could not extract them: KSU Organic Production PBI-004; KSU Forest Production PBI-0031; MU AF1021; Purdue HO-220-W PDF; UT D234-C; UKY CCD-CP-14; VCE 2906-1319 (Bratsch 2009, "Specialty Crop Profile: Pawpaw, Part 2: Growing Practices").
Proxy only (r.jina.ai; weaker): WVU Extension "Pawpaw Trees" (2022-09-01; 403 first-party; carries nothing on pests or wildlife); second-path confirmations of UIUC, UMD, PSU, KSU growing-info.
Unreadable on every path tried: KSU reports-and-presentations.php (404); Pomper & Layne 2005 "The North American Pawpaw: Botany and Horticulture" PDF (>10 MB, WebFetch refused; proxy returned empty); Cornell Harvest NY "Pawpaws in NY" guide doc_215.pdf (301 to a program landing page on both paths; the LOF page still links it).
Not fetched: Virginia Tech vt_vaes AREC site (no pawpaw page surfaced); no Cornell CCE county page beyond LOF; Kentucky Academy of Science journal article on the borer in fruit (JOURNAL, not needed).

## NEEDS-CATALOG-ADMISSION (optional -- every load-bearing claim above already has an admissible anchor)
* Ohio State University Extension, Ohioline: `ohio_state_ext` exists but its `citable_for` is scoped to ONE strawberry factsheet (PLPATH-FRU-36). ANR-0187 "Pawpaws: An Alternative Fruit Crop in the Midwest" (2025) carries the full pest/disease list, and ANR-0207 carries "Important pests like the peduncle borer (Talponia plummeriana) and the Asian ambrosia beetle (Xylosandrus crassiusculus) do not have registered products for use on pawpaws." Broaden the key's scope or add a carve-out.
* Virginia Cooperative Extension publication 2906-1319 (Bratsch 2009, Specialty Crop Profile: Pawpaw): no VCE parent-portal key exists (only 426-331, 426-840, 438-108, spes_455, piedmont_mg, vt_vaes). Carries "Currently, with limited or no registered chemical options for pest control in pawpaw, 'organic' methods are the only option." and "bucks will use young trees to rub velvet from antlers in the fall."
* Virginia Tech Department of Entomology, virginiafruit.ento.vt.edu (McClanan & Pfeiffer, 2006): `vt_vaes` points at arec.vaes.vt.edu; scope call whether the entomology department's fruit site sits under it. Carries the 5 mm larva, "may be the most severe pest", the raccoon/squirrel/fox/mice list, and "Deer, rabbits, and goats do not feed on leaves and twigs."
* UT Extension D234-C "Pawpaws for Tennessee Gardens and Landscapes" (Rose & Bumgarner, 2024/2025): no Tennessee key. Home audience; carries "reason for low insecticide use is that pawpaw is the larval host for the Zebra Swallowtail Butterfly."
* University of Kentucky Center for Crop Diversification CCD-CP-14 (2018): no UKY key (distinct from KSU). Carries "also have been found boring into twigs and fruit."

## SUMMARY
STATUS counts: SOURCED-OK 1 (Zebra swallowtail caterpillars); SOURCED-WEAK 2 (Pawpaw peduncle borer; Fruit-raiding wildlife); ANCHOR-MISPOINTED 1 (Phyllosticta leaf and fruit spot); UNSOURCED-FOUND 0; UNSOURCED-NOT-FOUND 0; JOURNAL-ONLY 0; WRONG 0 as a whole-entry verdict, but three entries carry a WRONG sub-claim.
Single most important finding: the two MANAGEMENT prescriptions the record actually makes are the two things no document supports, and the documents that exist point the other way. (1) The borer entry's whole treatment/prevention block (rake up dropped flowers "where the borer can complete its cycle") is contradicted by MU AF1021's life cycle: larvae bore from the flower into the stem and pupate and emerge from the TWIGS, with pupal cases visible on twigs at bloom; the specialist program's own advice is "Usually, the great abundance of unaffected flowers on trees does not require control of this insect" and no product is registered. (2) The Phyllosticta entry is anchored to a page that never names it, and its "cosmetic, the fruit inside remains sound" framing is refuted by every document that does name it (Clemson "A severe fungal disease... premature cracking"; MU cracked flesh "quickly becomes infected"; KSU PBI-004 "infested fruit can to split"); the cosmetic description belongs to flyspeck, a different fungus. Both cert-log halves are resolved: the borer half was already on the cited KSU page; the Phyllosticta anchor is KSU Organic Production PBI-004 (plus Clemson HGIC 1360). Secondary: the deer claim is wrong on the fruit half (KSU, Clemson, ACES all say deer eat dropped/ripe fruit; only Purdue 2001 and PSU's hedge say otherwise), and the real deer damage the sources name, buck antler rub on young trunks, is missing from the record.
Consumer-copy check: no em dashes, no °F figures, no capitalized "plant" in the four entries; "5 millimeters" is fine. Nothing to flag.

## PROPOSED TYPE
* Pawpaw peduncle borer: insect -- Talponia plummeriana (Lepidoptera: Tortricidae), per ksu_pawpaw planting guide / PBI-004 and aces_ext.
* Zebra swallowtail caterpillars: insect -- Protographium (= Eurytides) marcellus (Lepidoptera: Papilionidae), per umd_ext / ksu_pawpaw / clemson_hgic.
* Fruit-raiding wildlife (raccoons, opossums, squirrels): vertebrate -- raccoon, opossum, squirrel, fox (plus deer on dropped fruit and antler rub), per umd_ext, ksu_pawpaw enemies.php / PBI-0031, clemson_hgic, ncsu_ext, mu_ext.
* Phyllosticta leaf and fruit spot: fungal -- Phyllosticta asiminae with Mycocentrospora asiminae and Rhopaloconidium asiminae, per ksu_pawpaw PBI-004, clemson_hgic, aces_ext, mu_ext.
