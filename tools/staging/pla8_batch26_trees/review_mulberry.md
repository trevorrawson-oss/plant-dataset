# PLA-8 batch 26 -- INDEPENDENT SOURCE-TRUTH REVIEW: mulberry (`mulberry`)

Reviewer: independent of the authoring agent. Date 2026-09-04. No data file edited; this file only.

Documents read TODAY by me, not taken from the record report. FP = first-party WebFetch; PX = read
through `r.jina.ai/` because first-party returned 403 or an empty/no-text body (the record report says
the same four are first-party-unreadable, so this is a standing condition, not a transient one):

| doc | path |
|---|---|
| NCSU Plant Toolbox, Morus rubra (https://plants.ces.ncsu.edu/plants/morus-rubra/) | FP |
| NCSU Plant Toolbox, Morus alba (https://plants.ces.ncsu.edu/plants/morus-alba/) | FP |
| UF/IFAS Gardening Solutions, Mulberry | FP |
| UAEX Reference Desk, Mulberry (Q&A) | FP |
| MSU Extension, "Managing bird damage on fruit farms" | PX (first-party empty body) |
| MSU Extension E2747 (decoy sentence only) | PX |
| NCSU Extension, "Mulberry Whitefly" factsheet | FP |
| UC IPM Pest Notes 7401 Whiteflies (two passes) | FP |
| UC IPM Pest Notes 7400 Giant Whitefly | FP |
| Texas Plant Disease Handbook, Mulberry (two passes) | FP |
| OSU Digital Diagnostics, Popcorn Disease of Mulberry | PX (403 first-party) |
| UAEX Plant Health Clinic Newsletter Issue 15 (PDF) | PX (first-party no text) |
| OSU fact sheet, Anthracnose and Other Common Leaf Diseases of Deciduous Shade Trees (two passes) | PX (403 first-party) |
| PNW Plant Disease Management Handbook, Mulberry bacterial blight (NOT catalog-admitted) | PX |
| K-State MF2735 Borers: Common Kansas Species (NOT catalog-admitted) | PX |

Method catalog text (`control_methods.json`) was read for every method used or refused.

Grades: HOLDS / WRONG / UNSUPPORTED / SYNTHESIS / STYLE / FIT, per BRIEF_review.md.

---

## Birds [pests] -- 2 rungs, 2 corrections

**bird_scare_deterrents -- HOLDS.** Both MSU sentences exist, verbatim: "Birds can be harassed with
various methods such as pyrotechnics (screamers, bangers), propane cannons, hawk kites, reflective
ribbon and scare balloons." and "Birds are intelligent and become habituated if these methods are not
varied or moved frequently." The species clause is NCSU Morus rubra verbatim: "especially gray catbirds
and northern mockingbirds". The author picked the two home-scale devices off a list that also carries
propane cannons; that is biology/behavior from a commercial page, not its program, so brief rule 6 is
satisfied. The page never names mulberry (I checked: robins and cedar waxwings only), and the note does
not claim it does. Standing: a proxy read of a generic fruit-farm page, the same standing as the netting
anchor. Grade stands at that standing.

**bird_netting -- HOLDS.** Every failure mode in the note is an MSU sentence: "It is the most effective
means to prevent fruit damage."; "Merely draping netting over the plant allows the birds to access
fruit through the net and fruit is often pulled off the plants when draped nets are removed."; "Anchor
the netting to the ground to prevent birds from entering under the net."; "Attaching the netting to a
frame allows you to work and harvest the plants without having to remove the net."; "Netting must be
properly installed and maintained to completely exclude the birds." Timing "ahead of color ... late
spring" rests on NCSU Morus rubra "Fruit displays from May to June" (NC; regional, and the note says
"late spring", not a date). The fallback is UF/IFAS verbatim: "Visiting creatures will reduce the
harvest for your personal use, but on a good sized tree there should be enough fruits for all to enjoy."

**cause_seasoned (correction) -- HOLDS with one UNSUPPORTED clause (FIX 4).** Species: NCSU rubra "Its
fruits are eaten by many birds, especially gray catbirds and northern mockingbirds, foxes, opossums,
squirrels, and raccoons." Waxwings: UAEX "Over the weekend, the Cedar Waxwing birds were having a feast
on the berries". Share: UF/IFAS as above. The correction was NEEDED: no document read pairs robins with
mulberry, and none ranks birds as the "number-one reason". BUT the replacement keeps "a mulberry is one
of the best wildlife trees you can plant", an unranked superlative of exactly the class the author
removed one sentence earlier. NCSU says "attracting songbirds" and lists the wildlife; no document says
"one of the best".

**cause_beginner (correction) -- HOLDS.** Same anchors. "such a good tree for attracting birds" is
covered by NCSU alba "while also attracting songbirds".

Refusals: `prompt_harvest` refused correctly (no document read says pick promptly; UF/IFAS carries no
harvest-timing text at all).

## Whiteflies [pests] -- 5 rungs, 2 corrections

Provenance verdict, since the orchestrator asked: rungs 1-3 are UC IPM PN 7401's general whitefly
program (mulberry not named on that page); rungs 4-5 and the treatment threshold are NCSU's mulberry
whitefly factsheet, which is on-host. Every generic rung names UC IPM in the seasoned note and none
claims mulberry-specific support, so this is disclosed, not smuggled. One on-host anchor is available
and unused: UC IPM PN 7400 (Giant Whitefly) lists "Moraceae: Ficus nitida, Morus alba" as hosts and says
"The use of a strong stream of water directed to the undersides of infested leaves can be very
effective in managing giant whitefly." That is the on-host sentence for water_spray (RECORD-LEVEL 6).

**garden_sanitation -- HOLDS.** UC IPM: "Prune out isolated infested leaves when you first detect
them." NCSU threshold: "it is probably not necessary to treat infested plant unless the whiteflies
become tremendously abundant." NCSU cohort biology: "Once they settle down, they remain in the same
spot until the new adult mulberry whiteflies emerge a month or more later." ID stage: "shiny black
with a conspicuous white fringe." Correct method FIT (the catalog puts "picking off a spotted leaf"
under garden_sanitation, not prune_out_infection).

**water_spray -- HOLDS.** UC IPM: "Hose adults off plants with a strong stream of water." Egg timing is
NCSU: "About two weeks later, from the eggs hatch tiny yellow nymphs called crawlers". Settled nymphs:
NCSU as above plus UC IPM "Later nymphal stages are immobile". The morning timing is NOT on PN 7401
(which says "Early evening ... may be a good time to spray", about products); it is the method's own
catalog caution "Spray early in the day so foliage dries quickly". Warranted by the catalog, so HOLDS.

**beneficial_predators -- HOLDS.** All verbatim on PN 7401: "Many beneficials or 'natural enemies'
such as lacewings and lady beetles help control whiteflies."; "Look for signs of parasitization by
mini-wasps, such as circular holes in nymphs"; "Avoid using broad spectrum pesticides such as
pyrethroids, organophosphates, or neonicotinoids."; "Control of dust and ants, which protect whiteflies
from their natural enemies, can also be important, especially in citrus or other trees." (the "citrus
or other trees" phrase the note attributes is really there).

**insecticidal_soap -- HOLDS.** On-host: NCSU "The mulberry whitefly is not particularly resistant to
pesticides. Insecticidal soaps work well on adult whiteflies." Limits: UC IPM "Use soaps or oils when
plants are not drought-stressed and when temperatures are under 90°F". No residual: UC IPM "Most
less-toxic products such as insecticidal soaps, neem oil, or petroleum-based oils control only those
whiteflies that are directly sprayed" plus the catalog's "there is no residual". Gloves and eye
protection: the catalog caution ("wear chemical resistant gloves, long sleeves and goggles when mixing
and spraying"), not PN 7401, which has no PPE sentence; warranted by the catalog.

**horticultural_oil -- HOLDS.** On-host: NCSU "Horticultural oils should give some control of the
nymphs." 90°F: UC IPM as above. The bee precaution ("keep it clear of anything in flower") is the
catalog's UC IPM active-ingredient-database caution, not PN 7401 (whose only bee sentence is about
imidacloprid); "UC IPM's bee precaution" is therefore correctly attributed via the catalog's anchor,
just not via the entry's anchoring URL. PLA-457: no interval stated, sulfur not mentioned. Honored.

**prevention_seasoned / prevention_beginner (corrections) -- HOLDS, both.** The correction was NEEDED:
neither PN 7401 nor the NCSU factsheet nor PN 7400 has any nitrogen or fertilizer sentence (I asked for
one explicitly). Replacement sentences all verified above; host list is NCSU verbatim ("American
holly, avocado, boxelder, citrus, flowering dogwood, mountain laurel, mulberry, Norway maple, red
maple, Virginia sweet spire, and wax myrtle"), reasonably abbreviated.

Ladder length: five rungs for a pest NCSU calls "more of a curiosity than a pest" is long, but each
rung has a document and the NCSU threshold is carried on rungs 1 and 4. Not padding by the brief's
definition. Refusals (`balance_nitrogen`, `yellow_sticky_traps`, `neem_oil`): correct as stated; PN
7401 names neem oil generically, not for this crop, which is what the refusal says.

## Borers [pests] -- 1 rung, 2 corrections

**garden_sanitation -- UNSUPPORTED (admissibility), author-disclosed; DECISION item, FIX 6.** The
admissible literature is two NCSU prose sentences and neither gives a control: Morus rubra "Borers may
be a problem with this plant, particularly in the South."; Morus alba "No serious insect or disease
problems. Borers and whiteflies can be problems." The rung's warrant is (a) the catalog's own
`best_use` text for garden_sanitation ("beetles, borers and slugs sheltering in what is still
standing"), which is method-level, and (b) K-State MF2735, which I confirmed carries the sentence
verbatim: "Prune or remove and dispose of sick, dead, or fallen branches and limbs to deal with
established borers." K-State is NOT catalog-admitted. The mechanism clauses ("so the grubs inside them
do not finish developing and return to the tree"; "where wood-boring larvae shelter and complete
development") and the signals ("frass or oozing") are K-State's too (D. wildii: "Larvae overwinter";
"Sap ooze from niches for egg-laying; fine frass from small larvae"). Nothing in the rung is WRONG; it
is a correct general practice with no admissible mulberry-level document. The author said all of this
in `refusals`. The orchestrator has two clean closes: admit MF2735 (a land-grant extension bulletin,
first-party PDF; the sentence then anchors the rung directly and the grade becomes HOLDS), or replace
the rung with a refusal. What is not clean is shipping it as-is under `sources: ["ncsu_ext"]`, which
implies NCSU warrants a control it does not give.

`borer_stem_surgery` refusal: CORRECT. The catalog text is a squash-vine salvage ("mound damp soil over
the cut ... the vine can put out fresh roots"); it cannot be performed on a trunk.

**cause_seasoned / cause_beginner (corrections) -- HOLDS, both.** NCSU sentences verified as above.
The correction was NEEDED: no document read names a moth borer on mulberry (K-State names two beetles,
Dorcaschema wildii and Megacyllene caryae), and K-State's D. wildii entry carries no stressed-host
qualifier (its stressed-host sentence is general: "Borers are considered secondary pests. They are often
attracted to weakened and stressed hosts."). STYLE observation, not a FIX: "That is as far as the
extension sources for this tree go: none names the species involved" is meta-commentary about the
literature inside consumer copy. It is honest and matches the house's authority-through-honesty aim,
but it is a register the roster does not otherwise use; the orchestrator should decide whether to keep
it.

## Popcorn disease [diseases] -- 2 rungs, 4 corrections

**resistant_varieties -- HOLDS on the gradient; one UNSUPPORTED clause (FIX 5).** Both susceptibility
sentences exist and say exactly what the note says: OSU (proxy) "White mulberry varieties and hybrids
are more susceptible to popcorn disease."; UAEX PHC Issue 15 (proxy) "White mulberry varieties and
hybrids are more susceptible than red or black mulberries." The seasoned note's "The susceptibility
gradient is published; a resistant cultivar is not" is an accurate absence statement about the
documents. The beginner's "No variety is sold as immune" is a claim about the nursery market that no
document makes. FIT: a red/black-vs-white choice is a species-class choice rather than a cultivar
choice; the catalog's "varieties a pest is less drawn to" stretches to cover it, and no better method
exists. Accept.

**garden_sanitation -- HOLDS.** OSU: "Control is achieved by taking sanitary measures. Remove and bury
the infected fruit on the trees and any ground debris as it appears during the growing season." UAEX
Reference Desk: "Sanitation is your best method of control. Remove all the spent fruit from the tree
and under it and destroy it." UAEX PHC: "Clean up all fallen fruit and any diseased fruit still on the
tree and remove them from the planting." Fruit-only symptoms: OSU "The symptoms appear only on infected
fruit." Minor SYNTHESIS, not a FIX: "Every source that manages this disease manages it the same way"
overstates slightly; UAEX Reference Desk also offers "some success with a preventative spray of
Bordeaux mix (a copper/lime fungicide) as the tree is leafing out." Sanitation is every source's
FIRST answer; "the same way" is close enough that I do not file it, but "puts sanitation first" would
be exact.

**prevention_seasoned / prevention_beginner (corrections) -- HOLDS, both. The correction was NEEDED.**
The old text steered growers to "a more resistant hybrid" / "a tougher hybrid"; both graded documents
put hybrids in the SUSCEPTIBLE class. The replacement "red or black mulberries are less susceptible
than white mulberry varieties and their hybrids" is the UAEX PHC sentence inverted and nothing more
("their" specifies white-mulberry hybrids, which is what the canonical list's alba x rubra cultivars
are; UAEX says "hybrids" unqualified; harmless). "Sanitation through the growing season" is OSU's "as it
appears during the growing season", correctly replacing the old "year-round".

**organic_treatment_seasoned / organic_treatment_beginner (corrections) -- HOLDS, both.** The
overwintering-site clause was rightly removed: OSU prescribes removing "any ground debris" and no
document read states where the fungus overwinters. "There is no home spray that cures it" is compatible
with UAEX's Bordeaux line, which is PREVENTIVE ("as the tree is leafing out") and hedged ("not normally
recommended"). Bordeaux and dormant-oil refusals are correct under the brief's popcorn hold and are
recorded in `refusals`, not lost.

## Bacterial blight [diseases] -- 1 rung, 8 corrections

**prune_out_infection -- HOLDS.** TAMU's control sentence exists, verbatim and complete: "Some control
is obtainable on young trees by pruning dead shoots in autumn and spraying with approved fungicides."
The note reports the young-tree scope, the autumn timing, and the fungicide clause without a product,
which is exactly what TAMU says. The cut-into-sound-wood and destroy-the-prunings instructions are the
METHOD's catalog text ("take the blade well below the visible damage, into tissue that is still clean
... destroying what comes off"), not TAMU's; the beginner's "That is the step Texas A&M gives" attaches
them to TAMU a little too tightly (minor, not filed).

**Copper refusal -- CORRECT.** TAMU names no product. The only product-naming document is the PNW
handbook (not admitted; proxy read), and its sentence is disqualifying on its own: "The following are
registered on weeping mulberry; do not use on edible types." UC IPM's organism-level page adds
"Bactericide applications have not been found to give reliable control and spraying for P. syringae is
not recommended." Nothing admissible supports a copper rung on a fruiting mulberry.

**symptoms_seasoned / symptoms_beginner (corrections) -- HOLDS, both.** TAMU: "Watersoaked spots
appear on leaves and shoots have black stripes. The leaves at the twig tips wilt and dry up." OSU:
"The spots later become sunken and black. The leaves become distorted, and infected leaves on the twig
tips wilt and die." NCSU: "Bacterial blight may kill foliage/branches." NEEDED: no document says
"cosmetic" or "worst in wet springs" for mulberry.

**cause_seasoned / cause_beginner (corrections) -- HOLDS, both.** TAMU "bacterium – Pseudomonas
syringae pv. mori"; OSU "A blight of mulberry leaves is caused by a bacterium, Pseudomonas syringae pv.
mori, which at first appears as water-soaked spots."; NCSU as above. NEEDED: "minor ... rarely
threatens a healthy tree" is nowhere.

**organic_treatment_seasoned / organic_treatment_beginner (corrections) -- HOLDS as written;
OVER-CORRECTED (FIX 1).** The replacement text is TAMU's sentence and nothing false. But the `why`
claims the old "avoid overhead watering that keeps foliage wet" was "(same generic-only source)" and
removed it. That is wrong about the sourcing. The entry's OWN `ok_state_ext` anchor, in its Control
section, which governs every disease on the sheet including the mulberry blight paragraph, says:
"Avoid irrigation methods that wet the lower canopy of the tree." and "Consider thinning the canopy to
allow for greater air circulation which reduces periods of leaf wetness." The "dry weather" timing and
"no spray is warranted" removals were right (TAMU says autumn; TAMU's own clause names fungicides).

**prevention_seasoned (correction) -- SYNTHESIS, narrowed (FIX 3).** "Autumn pruning of dead, blighted
shoots is the one preventive step Texas A&M's plant disease handbook gives for mulberry" is literally
true of TAMU, but the sentence is built to tell the reader the sources give one step, and the entry's
own OSU anchor gives two more (above). The `why` says the open-canopy claim rested on "the PNW
handbook's 'space plantings for air circulation', not catalog-admitted"; it also rested on OSU, which
is admitted and anchored on this very entry.

**prevention_beginner (correction) -- WRONG, narrowed against its own anchor (FIX 2).** "The
prevention the sources give is the same fall cleanup" is false: the sources this entry cites give
irrigation placement and canopy thinning as well (OSU Control, verbatim above).

**Missing rungs (FIX 1).** `airflow_spacing` (applies_to includes `bacterial`) and `water_at_the_base`
(applies_to includes `bacterial`) are both anchored by OSU for this disease. The author refused
water_at_the_base only on the UC IPM organism-level page, which was the right call about THAT page; the
OSU sheet is crop-level (it names mulberry's blight in the section its Control governs) and was not
considered. The `refusals` entry says "TAMU does not say it", which is true, and stops there.

## Leaf spots and minor foliar diseases [diseases] -- 1 rung, 8 corrections

**garden_sanitation -- HOLDS.** TAMU False Mildew, verbatim: "The infected leaves fall to the ground,
and the overwintering or ascocarpic stage matures in spring on these leaves. Gather and burn all fallen
leaves in autumn." OSU Control: "Most leaf diseases of yard trees are controlled by gathering and
destroying fallen, infected leaves."; "Trees that have been affected by leaf diseases every season
should also be well fertilized and watered to maintain vigor. Do not fertilize during early fall.
Fertilize only after the trees are dormant in late winter to early spring." All present. The vigor
sentence riding inside this rung (no method reaches it) is disclosed in `unreachable_claims`.

**`airflow_spacing` refusal -- WRONG (FIX 1).** The author wrote: "my own reads of TAMU and OSU found
no air-movement sentence." TAMU has none (confirmed: I asked for any sentence on air circulation,
canopy, pruning timing, dry weather or overhead watering, and there is none). OSU has one, in the same
Control paragraph as the fallen-leaves sentence the author quotes, one sentence before the vigor
sentence the author also quotes: "Consider thinning the canopy to allow for greater air circulation
which reduces periods of leaf wetness." The sheet's Control section is general and governs the mulberry
Cercospora/Cercosporella paragraph, which sits under "Leaf Spot Diseases" before it. The old prose's
"keep the canopy open for airflow" had an admissible anchor at exactly the standing of the OSU vigor
sentence the author added in its place. `water_at_the_base` (applies_to includes `fungal_foliar`) is
anchored by the adjacent "Avoid irrigation methods that wet the lower canopy of the tree."

**cause_seasoned / cause_beginner (corrections) -- HOLDS, both.** TAMU: "The leaves of mulberry are
spotted by these fungi in very rainy seasons."; "The Cercosporella fungus can cause defoliation of older
trees."; "The foliage of mulberries growing in the southern states may suffer severely from attacks of
this fungus."; "It appears in July as whitish, indefinite patches on the undersides of the leaves."
NEEDED: "cosmetic and seldom worth treating" is the record's gloss; two members are graded severe.

**symptoms_seasoned / symptoms_beginner (corrections) -- HOLDS, both.** OSU: "Leaves of mulberry trees
are spotted by two fungi, Cercospora moricola and Cercosporella mori, which cause reddish-brown spots."
TAMU Powdery Mildews: "The lower leaf surface is covered by a white, powdery coating of these fungi."
Plus the severity sentences above. NEEDED.

**organic_treatment_seasoned / organic_treatment_beginner (corrections) -- HOLDS as written;
OVER-CORRECTED (FIX 1).** Every sentence kept is anchored (TAMU "Gather and burn"; TAMU "Valuable
specimens should be sprayed with approved fungicide if leaf spots are serious."; OSU vigor). The `why`
says "No document read prescribes canopy pruning or air movement for mulberry leaf diseases; the sourced
prevention is leaf sanitation plus vigor." OSU prescribes canopy thinning and irrigation placement in
the same breath as the vigor sentence the author took. The removal was unwarranted.

**prevention_seasoned (correction) -- HOLDS as written, narrowed (FIX 1).** "Autumn leaf cleanup is the
prevention" sits beside OSU's canopy and irrigation sentences, which the `why` calls "(unanchored for
mulberry)". They are anchored. The old text's "whole prevention program" superlative and its "without
meaningful harm" gloss were rightly removed.

**prevention_beginner (correction) -- HOLDS.** "the main prevention" is a fair weight; nothing false.
Restore the canopy/irrigation clause alongside it when FIX 1 lands.

---

## FIX ITEMS

**FIX 1 (both disease entries) -- OVER-CORRECTION on a wrong premise; `airflow_spacing` refusal wrong.**
Texts: Bacterial blight `organic_treatment_seasoned.why` "prescribed avoiding overhead watering (same
generic-only source)"; `prevention_seasoned.why` "an open canopy ... (the PNW handbook's 'space
plantings for air circulation', not catalog-admitted, and nothing for dry weather)"; Leaf spots
`organic_treatment_seasoned.why` "No document read prescribes canopy pruning or air movement for
mulberry leaf diseases"; `prevention_seasoned.why` "'open-canopy pruning' and 'good air movement' ...
(unanchored for mulberry)"; `refusals` "my own reads of TAMU and OSU found no air-movement sentence."
What is wrong: the OSU shade-tree fact sheet, anchored as `ok_state_ext` on BOTH entries and already
quoted by the author for its vigor and fertilizer sentences, carries in its general Control section,
which governs the mulberry blight and mulberry Cercospora paragraphs: "Avoid irrigation methods that
wet the lower canopy of the tree." and "Consider thinning the canopy to allow for greater air
circulation which reduces periods of leaf wetness." Four corrected fields removed an anchored claim as
unanchored, and one refusal was based on a misread. Settling sentence: the OSU canopy sentence above.
Remedy: add `airflow_spacing` to both ladders (and `water_at_the_base` if the orchestrator wants the
irrigation sentence carried; both methods reach both types), attributed to Oklahoma State and worded as
OSU words it (thin the canopy to shorten leaf wetness; keep irrigation off the lower canopy), not as the
old "open-canopy pruning ... the whole prevention program"; restore the clause into the four
organic_treatment/prevention fields; correct the four `why` strings and the refusal.

**FIX 2 (Bacterial blight `prevention_beginner`) -- WRONG.** Text: "The prevention the sources give is
the same fall cleanup". Wrong: the entry's own `ok_state_ext` anchor gives two more preventive steps.
Settling sentence: "Consider thinning the canopy to allow for greater air circulation which reduces
periods of leaf wetness." (OSU Control).

**FIX 3 (Bacterial blight `prevention_seasoned`) -- SYNTHESIS, narrowed.** Text: "Autumn pruning of
dead, blighted shoots is the one preventive step Texas A&M's plant disease handbook gives for
mulberry". True of TAMU alone; constructed to read as the sources' only step. Settling sentence: as FIX
2. Rewrite so the TAMU step is one of the steps, not the one.

**FIX 4 (Birds `cause_seasoned`) -- UNSUPPORTED clause.** Text: "a mulberry is one of the best wildlife
trees you can plant". Wrong: an unranked superlative, the same class as "the number-one reason" the
same correction removed. Settling sentence: NCSU alba "It is resistant to drought and pollution, while
also attracting songbirds." and the rubra wildlife list; neither ranks. Say "a wildlife tree" or "a tree
NC State lists for attracting songbirds".

**FIX 5 (Popcorn `resistant_varieties.note_beginner`) -- UNSUPPORTED clause.** Text: "No variety is
sold as immune". Wrong: a market claim in no document; the documents are silent on resistant cultivars
rather than stating none is sold. Settling: UAEX PHC "White mulberry varieties and hybrids are more
susceptible than red or black mulberries." is the whole published gradient. Say "no source names a
resistant variety".

**FIX 6 (Borers `garden_sanitation`) -- UNSUPPORTED at crop level; DECISION, not a rewrite.** Text: the
whole rung, under `sources: ["ncsu_ext"]`. Wrong: NCSU gives no control ("Borers may be a problem with
this plant, particularly in the South." is the entirety). Settling sentence exists only in K-State
MF2735, not admitted: "Prune or remove and dispose of sick, dead, or fallen branches and limbs to deal
with established borers." Close it by admitting MF2735 (rung becomes HOLDS, and `sources` gains the key)
or by carrying a refusal instead of a step. Do not ship it credited to NCSU.

Refusals otherwise checked and CORRECT: borer_stem_surgery; the borers' stressed-tree narrative (at the
admissible level); copper on bacterial blight; "in dry weather" as pruning timing; Bordeaux and dormant
oil on popcorn (brief's hold; exception recorded); prompt_harvest; balance_nitrogen; sticky traps/neem.
The "keeping foliage dry, exactly as TAMU states" refusal is right about TAMU and wrong that no
crop-level document says it (OSU does; see FIX 1).

## SUMMARY

Rungs: 12 graded. HOLDS 11, UNSUPPORTED 1 (Borers garden_sanitation, admissibility, author-disclosed),
WRONG 0, SYNTHESIS 0, STYLE 0, FIT 0.
Corrections: 26 graded. HOLDS 22, WRONG 1 (Bacterial blight prevention_beginner), SYNTHESIS 2 (Bacterial
blight prevention_seasoned; Leaf spots prevention_seasoned, narrowed), UNSUPPORTED 1 (Birds
cause_seasoned, one clause). Four further corrections HOLD as written but over-corrected (Bacterial
blight and Leaf spots organic_treatment_*), counted inside HOLDS and filed under FIX 1.
Refusals: 11 checked; 1 WRONG (`airflow_spacing`), 1 right-about-TAMU-but-incomplete (`water_at_the_base`).
FIX items: 6 (FIX 1 spans two entries, four fields, one refusal).
PLA-457: HONORED. I grepped all 50 consumer strings (24 notes + 26 corrections): no "sulfur", no
N-day/N-week figure, no "interval"; oil is named on two rungs with no spacing. The only interval in play
is the catalog's own horticultural_oil caution, which is the roster-wide PLA-457 matter, not this file.
Consumer copy: no em or en dash in any consumer string; the four "90°F" figures are UC IPM PN 7401
verbatim; no mid-sentence "Plant".
The orchestrator's specific tests: Borers warrant, confirmed as the author describes it (no admissible
control; K-State carries the sentence). TAMU control sentence, exists verbatim and the rung matches it;
copper refusal right. Popcorn correction, exactly OSU/UAEX and nothing more. MSU bird sentences, exist.
Whitefly provenance, 3 generic + 2 on-host, disclosed; PN 7400 is the unused on-host water anchor.

**Single most important finding:** the author corrected "keep the canopy open for airflow" and "avoid
overhead watering" OUT of six fields across two disease entries, and refused `airflow_spacing`, on the
stated ground that no document read prescribes either for mulberry, while the OSU fact sheet the author
anchored on both entries and quoted for its vigor and fertilizer sentences says, in the same Control
paragraph, "Consider thinning the canopy to allow for greater air circulation which reduces periods of
leaf wetness." and "Avoid irrigation methods that wet the lower canopy of the tree." The corrections
were needed for the "cosmetic" glosses and the "dry weather" timing, and every replacement sentence is
anchored, but they also stripped an anchored practice and mis-stated its sourcing in four `why` strings.
This is defect class 2 (a claim narrowed against its record) with the record's own anchor as the
witness.

## RECORD-LEVEL FINDINGS (for a later pass, not fixed now)

1. **Borers, fields outside the brief's ask** (`symptoms_*`, `organic_treatment_*`, `prevention_*`) still
   carry "Healthy, vigorous mulberries are seldom attacked", "water through droughts", "keep mowers and
   trimmers off the trunk", "no spray reaches them". At the admissible level all are unanchored. If
   K-State MF2735 is admitted (FIX 6), its general sentences anchor every one of them: "Borers are
   considered secondary pests. They are often attracted to weakened and stressed hosts."; "When adequate
   moisture is available small borer larvae do not survive water surging through tree vascular
   elements."; "Beetles deposit eggs in bark cracks and crevices and are especially attracted to wound
   areas (e.g. pruning cuts or mower and string-trimmer damage at tree bases)."; "Applications after the
   fact are of little or no value." (the last is in the shothole-borer entry). The admission decision
   settles the whole entry, not just the rung.
2. **Proxy reads marked as plain "verified".** `ok_state_ext` (both URLs), `uada_ext` PHC PDF, and
   `msu_ext` bird page are unreadable first-party on every path tried on two passes and were read only
   via r.jina.ai; `anchoring_urls` carries `verified: 2026-09-04` with no proxy flag. The record report
   asked for the flag. The popcorn severity `medium` and the hybrid correction both rest on proxy text.
3. **Birds `organic_treatment_*` / `prevention_*`** still carry "pick promptly" / "harvest ripe fruit
   promptly each day" and "Net only small or dwarf trees", unanchored per the record; nothing
   contradicts them. The decoy sentence is anchored by MSU E2747 (proxy): "Mulberry fruit is very
   attractive to birds, and the trees may be planted strategically to lure birds away from a high-value
   fruit crop." E2747 is not in the entry's `anchoring_urls` (one URL per key); its URL lives in
   `unreachable_claims` only.
4. **Popcorn "no home spray" framing.** UAEX Reference Desk (first-party, admitted) carries "there has
   been some success with a preventative spray of Bordeaux mix (a copper/lime fungicide) as the tree is
   leafing out." The prose's "no home spray that cures it" is compatible (preventive, not curative), but
   a future pass should keep the wording at "no cure", never "no spray". TAMU's "The disease is of little
   importance" is an ornamental-handbook verdict and should not be read against the fruiting-audience
   severity.
5. **Bacterial blight `sources`** lists `ok_state_ext` and `ncsu_ext` but the shipped ladder uses only
   TAMU; after FIX 1 the OSU key will be load-bearing on a rung.
6. **Whiteflies on-host water anchor.** UC IPM PN 7400 (Giant Whitefly) lists "Morus alba" as a host and
   gives the strong-stream-of-water step; it is the on-host anchor for water_spray and is unused (the
   entry's one `uc_ipm` URL is the generic PN 7401). Worth swapping or recording.
7. **Whiteflies `symptoms_*`** "lift off the undersides of leaves when disturbed" remains unanchored
   (generic behavior; harmless).
8. **Problems the documents carry that the record does not:** NCSU rubra "Watch for scale, mites, and
   mealybugs."; "Coral spot cankers may cause twig dieback."; "Bacterial leaf scorch, powdery mildew,
   root rot, and witches broom may also occur."; TAMU "White mulberry has been rated highly susceptible
   to cotton root rot."; UAEX stink bug piercing damage; MSU E2747 "Scales and two-spotted mites can be a
   problem". Already listed by the record report; repeated here so the batch's close-out has it.
9. **Register observation.** The Borers cause_seasoned and garden_sanitation seasoned note tell the
   reader what the extension literature does and does not say ("That is as far as the extension sources
   for this tree go"). Honest, and in the spirit of the authority north star, but a register no other
   roster entry uses. A house decision, not a defect.
10. **Catalog `horticultural_oil` caution 2** ("Do not apply sulfur within 2 weeks of an oil spray")
    is the PLA-457 interval, living in the catalog rather than in any mulberry string. Noted so the
    roster-wide ruling knows this crop's oil rungs inherit it by reference only.
