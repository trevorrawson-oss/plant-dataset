# PLA-8 batch 26 -- INDEPENDENT SOURCE-TRUTH REVIEW: pawpaw (`pawpaw`)

Reviewer: independent (did not author). Date: 2026-09-04. No data file edited; this file only.
Graded: `out_pawpaw.json` (5 rungs, 21 field corrections, 5 refusals, 5 unreachable claims) against
the documents, read by me today. Validator: `python3 validate_out.py pawpaw` -> "OK: pawpaw validates.
3 pests + 1 diseases, 5 rungs." Consumer-copy scan of every note and corrected field: no em dashes,
no British spellings, no capitalized "plant", no temperatures. Clean.

## Documents read (my own reads, not the record report's)

First-party WebFetch, verbatim sections returned: KSU Pawpaw Planting Guide (Pests section complete,
Pollination section complete); KSU enemies.php (Callaway 1990); KSU FAQ (ripeness sentences); UMD
Native Trees of Maryland (Kuder, upd. 2025-05-23); UMD Less Common Fruits for a Home Garden (Talabac /
Traunfeld, upd. 2026-04-14; pawpaw section complete); Clemson HGIC 1360 (rev. 2022-01-28; Problems
section complete); ACES ANR-3095 (Akers-Campbell, Britton, Akotsen-Mensah, July 2024; pest and disease
sections complete with paragraph boundaries); NCSU Plant Toolbox Asimina triloba (Insects/Diseases and
Wildlife Value fields complete); NCSU Lee County "Spots on My Leaves" (Bratcher 2023-06-23, upd.
2025-07-31); Cornell Small Farms (Ames 2018-01-08); UIUC Good Growing (Swihart 2024-08-02); PSU The
Native Pawpaw Tree (Esslinger, upd. 2023-09-25); UMD Maryland Grows pawpaw tag (absence test only).

PROXIED via `r.jina.ai` (PDFs WebFetch cannot extract), stated per the brief: KSU Organic Production
PBI-004 (Pomper, Crabtree, Lowe 2010); KSU Forest Production PBI-0031 (Pomper, Crabtree 2009); MU
AF1021 "Growing and Marketing Pawpaw in Missouri" (2022; complete borer, webworm, leafroller,
swallowtail, leaf spot and wildlife paragraphs returned verbatim). The Lee County article was ALSO
re-read through the proxy to get its full body text after the first-party summarizer condensed it.

Two absence tests run: WebSearch for a pawpaw extension page recommending netting or trunk baffles
(edu/extension domains, then unrestricted) -- none surfaced. That makes the author's netting
negatives UNSUPPORTED, not WRONG (see FIX-8).

Two prior readings the orchestrator asked me to check:
* `orchestrator_verifications.md` V5 (MU AF1021): HOLDS. The complete borer paragraph, verbatim
  through the proxy, carries the life cycle and NO control statement: "Larvae initially feed on the
  anthers, then move through the floral tissue, and eventually bore into stems where they continue
  to consume tissue until they pupate and emerge from the twigs." The sentence "To control this pest,
  infested parts of the tree can be pruned and removed from the site." is the last sentence of the
  Asimina webworm (Omphalocera munroei) paragraph.
* The author's ACES scope finding (notes_to_orchestrator): HOLDS. Verbatim, the sanitation sentence
  is the closing sentence of ONE paragraph: "Other pawpaw pests may include stinging rose caterpillar
  (Parasa indetermina), pawpaw sphinx moth (Dolba hyloeus), granulate ambrosia beetle (Xylosandrus
  crassiusculus), brown marmorated stink bug (Halyomorpha halys), and spotted wing drosophila
  (Drosophila suzukii). Trapping, manual removal, and orchard cleanliness and sanitation are
  recommended to combat these pests." The peduncle borer paragraph is three paragraphs earlier and
  ends "The larval stage is the most destructive, causing damage to stems, roots, and flower
  peduncles." with no control statement. The brief's description of that sentence as spanning the
  whole list is wrong; the author read it right.

Grade key (brief): HOLDS / WRONG / UNSUPPORTED / SYNTHESIS / STYLE / FIT. Each rung and correction
gets a headline grade = its worst sentence, with the sentence-level evidence under it.


## Pawpaw peduncle borer (`pawpaw-peduncle-borer`, insect, medium)

### Ladder (1 rung)

**garden_sanitation -- FIT.** Every load-bearing sentence is anchored and the note is honest, but the
note's content is "sanitation has no target here", attached to a method whose own rendered text says
"It is the backbone step for anything that spends the winter in the debris you leave behind, from
black rot ... to beetles, borers and slugs" (control_methods.garden_sanitation.best_use). A reader
sees a Garden sanitation step recommended and then a note saying it does nothing. That is the
definition of FIT. The author says so themselves ("written so the file validates"; validate_out.py
lines 114-115 refuse an empty ladder). Sentence by sentence:
* B1 "Pawpaw growers are told to leave this one alone." HOLDS -- PBI-004: "Usually, the great
  abundance of unaffected flowers on trees does not require control of this insect."
* B2 "A tree opens far more flowers than the borer spoils, and no spray is recommended against it."
  HOLDS -- same sentence; "no spray is recommended" is an absence claim but is true of all 16
  documents read (no product named anywhere; PBI-004: "Pawpaw pest problems are limited and usually
  do not require control measures.").
* B3 "Cleaning up under the tree does not reach it either: the caterpillar leaves the flower for the
  stem and twig, turns into a pupa there, and the moths come out of the twigs, the first of them
  right at bloom in April and May." Life cycle HOLDS -- MU AF1021 verbatim above, plus "The first
  generation of adult moths emerges from twigs in April and May, often when trees are blooming."
  "does not reach it" is the author's inference from that cycle (SYNTHESIS, sound). "right at bloom"
  tightens MU's "often when trees are blooming". The months are a Missouri guide's calendar (FIX-5).
* B4 "Picking up dropped flowers and fruit is ordinary orchard hygiene for a pawpaw, not a fix for
  this borer." UNSUPPORTED -- no document calls flower pick-up ordinary pawpaw hygiene; the only
  sanitation sentence (ACES) is scoped to five other pests. FIX-3.
* S1 "...the abundance of unaffected flowers usually does not require controlling this insect, and no
  product is recommended for it; a small-farm guide calls the damage too slight to be a serious
  problem." HOLDS -- PBI-004 above; Cornell SF: "Usually, however, so little damage is done that
  this is not considered a serious problem."
* S2 "Sanitation has no documented target here." HOLDS as an honest absence statement.
* S3 life cycle with "pupal cases visible on the twigs at bloom" HOLDS -- MU: "As these insects
  emerge in spring, their pupal cases are visible on twigs."
* S4 "A commercial guide recommends orchard cleanliness against pawpaw insects in general; expect it
  to do nothing in particular for the borer." WRONG on scope -- ACES's sentence covers five named
  "Other pawpaw pests", not pawpaw insects in general; the author's own scope finding says so and
  the note contradicts it. "expect it to do nothing" is inference stated as expectation. FIX-2.

### Corrections (6)

* **symptoms_seasoned -- HOLDS.** "wither and drop" (KSU PG: "causing the flower to wither and
  drop"); "about 5 millimeters" (KSU PG); "flower stalk" (NCSU: "larvae burrow into flower stalks");
  "bores on into the stem" (MU); "small brown moths about a quarter inch long with darker wing tips,
  emerge from the twigs, and their pupal cases can be seen on the twigs then" (MU: "The adults are
  brown, speckled with darker wing tips and are small (about 1/4 inch long). As these insects emerge
  in spring, their pupal cases are visible on twigs."); "majority of a tree's blossoms" (KSU PG: "In
  some years this borer is capable of destroying the majority of blossoms."); "in most years the loss
  is too small to count as a serious problem" (Cornell SF). Nits: "destroys" is stronger than KSU's
  "is capable of destroying"; "so a heavy bloom yields almost no fruit" is the record's inference
  carried over, harmless. April/May: FIX-5. Correction NEEDED: "blacken" and "small pale
  caterpillar" have no anchor in any document read (MU describes only the adult).
* **symptoms_beginner -- HOLDS.** Same anchors; "turn black" and "tiny pale caterpillar" rightly
  removed.
* **organic_treatment_seasoned -- UNSUPPORTED (one sentence).** "No product is recommended" /
  "does not require controlling it" / "too slight to be a serious problem" HOLD (PBI-004, Cornell).
  "Nothing reaches the larva once it is inside the flower or the stem" -- no document read says a
  spray cannot reach this larva; the documents say control is not required and name no product.
  This is a mechanism supplied as the reason (brief class 3). "gathering dropped flowers does not
  interrupt it" is SYNTHESIS: inferred from MU's cycle (no document says dropped flowers are
  larva-free), better founded than the record's opposite inference but still inferred. FIX-4.
  Correction NEEDED: the record's flower-sanitation prescription and "often eases the following
  year" have no anchor, and hand pollination as a borer countermeasure is an inference.
* **organic_treatment_beginner -- SYNTHESIS (mild).** "the tree opens far more flowers than the
  borer ruins" HOLDS (PBI-004). "Picking up the fallen flowers will not help either, because the
  caterpillar has moved on into the twig, where it turns into a moth" -- the cycle HOLDS (MU); "will
  not help" is the same inference as above; soften per FIX-4.
* **prevention_seasoned -- HOLDS.** "no resistant cultivar is named" true of every document read;
  moths and pupal cases at bloom (MU); swing (KSU PG, Cornell); "the tree is self-incompatible and
  usually needs pollen from a genetically different tree" (KSU PG Pollination: "pawpaw trees are
  self-incompatible, usually requiring pollen from a genetically different tree in order to be
  fertilized."); "hand pollination ... is worth doing ... but it is a pollination measure, not a
  borer control" (KSU PG: "Although it requires a little extra labor, hand pollination to ensure
  fruit set can be well worth the effort"; Clemson: "hand pollination, although laborious, can be
  worthwhile"). This is the right correction: the record's "pollination insurance" framing is an
  inference no document makes, and its raking prescription is refuted by MU's twig cycle.
* **prevention_beginner -- HOLDS.** Same anchors.

Refusal check: LADDER REFUSED is the right reading of the documents. No document leaves any method
open for this insect; ACES's sanitation sentence does not reach it (verified above); MU's pruning
sentence is the webworm's (verified above). Hand pollination refused as a borer countermeasure:
right (every document gives it for fruit set generally).


## Zebra swallowtail caterpillars (`zebra-swallowtail`, insect, low)

### Ladder (1 rung)

**handpick -- WRONG (one absolute), and the trigger clause is UNSUPPORTED as anchored.** The shape
(one rung, tolerance-led, no spray) is right and matches the brief's instruction. But:
* B1 "Leave them alone if you can." HOLDS -- UMD LCF: "Few insects feed on pawpaw foliage, and they
  do not cause enough damage to warrant treatment."; KSU PG: "more a blessing than a curse."
* B2 "a butterfly whose young can grow up on no other plant" HOLDS -- UIUC "the only host plant";
  Clemson "the exclusive larval (caterpillar) host plant". "they chew a few young leaves without ever
  coming in numbers that hurt the tree" WRONG for young trees -- MU AF1021: "On newly-planted trees
  or seedlings, larvae can devour much of the foliage, but they rarely cause severe damage on older
  trees."; ACES: "They can cause significant damage to young trees but are rarely a problem on
  mature plantings." KSU's "never in great numbers" and Clemson's "rarely results in much damage to
  mature trees" are statements about established trees. "pawpaw growers are told the feeding is not
  worth treating" HOLDS (UMD).
* B3 "If a small tree is losing more new leaves than you can spare, look over the young growth at
  the branch tips and lift the caterpillars off by hand." The trigger is NOT an invention: it is
  exactly what MU and ACES say (quoted above). But neither key is in this entry's `sources`, so as
  anchored the clause is UNSUPPORTED. "young growth" HOLDS (KSU PG "feed exclusively on young pawpaw
  foliage"; MU "Females deposit single eggs on the underside of young leaves."). Hand removal itself
  is in no document; it is the brief's parsleyworm shape, and I accept it as the least-invasive
  method with the sources' do-not-treat framing carrying the note.
* B4 "No spray is called for." HOLDS (UMD).
* S1 "Tolerance is the documented answer." HOLDS.
* S2 "feed only on young pawpaw foliage and never in great numbers, they do not affect fruit yield,
  and the extension advice for a home tree is that the damage does not warrant treatment." KSU PG
  verbatim; NCSU: "The zebra swallowtail butterfly larvae feed on young leaves, but they seldom do
  permanent damage, nor do they affect fruit yield."; UMD. HOLDS, but "never in great numbers" needs
  the same established-tree scoping (FIX-6).
* S3 "Where a young tree is losing new growth faster than it can spare, hand removal is the one
  intervention that stays selective, and the search is short because the feeding is confined to the
  new foliage." Young-tree trigger: MU/ACES (unanchored in entry); "stays selective" is the method's
  own pro; "the search is short" is inference. SYNTHESIS.
* S4 "Anything beyond that removes the sole larval host of a native butterfly for damage the pawpaw
  program rates negligible." "negligible" HOLDS (PBI-004: "this damage has been negligible"). STYLE
  nit: a spray removes the larvae, not the host plant; reword "removes the larvae of a native
  butterfly that has no other host".

### Corrections (3)

* **symptoms_seasoned -- WRONG (one absolute).** "usually only a few at a time ... feeding on the
  new foliage" HOLDS (KSU, NCSU). "the larvae never appear in numbers large enough to defoliate a
  tree" is contradicted for seedlings and newly planted trees by MU ("can devour much of the
  foliage") and ACES ("significant damage to young trees"). "they do not affect fruit yield" HOLDS
  (NCSU). "on a mature tree the feeding rarely amounts to much" HOLDS (Clemson). FIX-6. Also
  FIX-7: the correction dropped the identification aid on the ground that "no admissible document
  describes the larva's color"; MU AF1021 and ACES ANR-3095 both do (quoted in FIX-7). The original
  "green-and-black banded" was imprecise rather than wrong (MU: "green or black ringed with narrow
  green, white, blue, or yellow bands"), so the correction was needed in form but over-corrected in
  effect: the reader now has no way to recognize the caterpillar.
* **symptoms_beginner -- WRONG (same absolute).** "there are never enough of them to strip a tree"
  -- same MU/ACES sentences. "they do not cost you any fruit" HOLDS (NCSU). FIX-6, FIX-7.
* **cause_seasoned -- HOLDS.** Synonym addition anchored: Clemson and KSU PG "Eurytides marcellus";
  UMD Native Trees "Protographium marcellus". Was it needed? The original held; the addition is
  justified for findability and changes nothing else. Fine.

Refusal check: bt and every spray refused -- right; no document mentions any treatment.


## Fruit-raiding wildlife (`fruit-raiding-wildlife`, vertebrate, medium)

### Ladder (1 rung)

**prompt_harvest -- UNSUPPORTED (one absence claim); the harvest advice itself HOLDS.**
* B1 "You will not out-wait a raccoon, so pick first." STYLE flourish; substance HOLDS (UIUC: "To
  successfully harvest the fruit, diligence is necessary. The ripe fruit is prized by wildlife and
  quickly eaten.").
* B2 "ready when the flesh just starts to soften and the skin gives a little under your thumb; pick
  them then and let them finish ripening on the counter, because fruit picked hard and green never
  ripens." Softening (ACES: "Pick pawpaws off the tree when flesh first starts to soften"); skin
  gives (Clemson: "until the skin gives (indents) slightly with a finger squeeze"; UIUC: "will give
  a little under pressure"); ripens off the tree (UMD LCF: "If picked slightly under-ripe, they
  should finish ripening off the tree, but if picked too early and firm, they will not."; UIUC:
  "Immature fruit may be harvested and will ripen indoors at room temperature."). HOLDS, except the
  word "green": pawpaw skin is green when ripe (UMD LCF: "Aromatic green- or yellow-skinned fruits
  ripen late summer through early autumn."; KSU FAQ: "Color change is generally not a reliable
  indicator of ripeness."). Telling a beginner not to pick "green" fruit invites waiting for a color
  change that never comes. STYLE -> FIX-9.
* B3 "in late summer and early fall, check the tree every day, and pick up anything that has dropped,
  since deer and every other animal will clean up fallen fruit." Season (UMD LCF above); daily check
  (ACES: "Trees should be checked and harvested every day during the harvest period for the best
  fruit quality." -- commercial and for fruit quality, but scale-free, and UIUC's "diligence" backs
  it at home scale); deer on drops (KSU PG: "they will eat fruit that has dropped on the ground.";
  UMD LCF: "Various wild animals will eat fallen fruits."). Clearing drops as a wildlife control is
  in no pawpaw document; it is the method's own practice ("clear away anything that has gone over or
  dropped"). HOLDS at method level.
* S1 "no pawpaw guide describes netting or trunk baffles, and trapping the animals is an orchard
  practice." UNSUPPORTED -- a universal negative in consumer prose. It is true of all 16 documents I
  read and of two web searches, so it is not WRONG, but no document says it. "trapping" HOLDS at
  its source (MU: "These pests can be removed from the site by trapping."); that it is an orchard
  rather than a garden practice is the author's reading of MU's audience. SYNTHESIS. FIX-8.
* S2 ripeness HOLDS (Clemson, UMD LCF, as above).
* S3 "Ripening runs from August into October" (UMD NT: "its fruits (August-October)"; PBI-0031:
  "fruit ripen in late-August to early-October"); "the ground under the tree is where deer join the
  raccoons, opossums, squirrels and foxes" (UMD NT: "eaten by foxes, opossums, raccoons, and
  squirrels"; KSU PG / Clemson / ACES on deer and dropped or ripe fruit). HOLDS.

### Corrections (6)

* **symptoms_seasoned -- HOLDS.** UIUC verbatim ("prized by wildlife and quickly eaten"). "the harvest
  window is short": PBI-0031 "Fruit ripen on the same tree over about a 2-week period"; fine.
  Correction NEEDED: "often overnight" and aroma-as-cause are in no document (KSU FAQ gives the
  aroma as a ripeness sign, not as what draws animals).
* **symptoms_beginner -- HOLDS.** Same.
* **cause_seasoned -- HOLDS.** Four animals (UMD NT verbatim); "Deer avoid the foliage and twigs,
  which chemicals in the bark and leaves make unpalatable" (UMD NT: "Chemicals in the bark and
  foliage make them unpalatable to deer."); "they do eat ripe fruit that has dropped" (KSU PG:
  "Deer will not eat the leaves or twigs, but they will eat fruit that has dropped on the ground.";
  Clemson: "Deer do not feed on the leaves or twigs, but they will eat the ripe fruit."; ACES: "Deer
  will not eat leaves or twigs but will consume fallen fruit."); antler rub in winter (KSU PG: "Male
  deer occasionally damage trees by rubbing their antlers on them in winter."; UMD LCF: "bucks may
  rub antlers on trunks, potentially causing serious bark injury if trees are unprotected."). Nit:
  "ripe on the tree or fallen beneath it" -- documents say "eat the fruit" / "fallen fruits"; "on
  the tree" is inferred, harmless. Correction NEEDED: the record's "Deer ... avoid the foliage and
  fruit" is refuted on the fruit half by the crop's own program and two more T1s.
* **cause_beginner -- HOLDS.** Same anchors.
* **organic_treatment_seasoned -- UNSUPPORTED (one sentence).** Ripeness and daily check HOLD (as
  above). "pawpaw guides do not describe netting or trunk baffles, and trapping the animals is an
  orchard practice rather than a garden one" -- the netting negative is unsourced and the "rather
  than a garden one" half is a claim no document makes. The brief is explicit: a correction that
  swaps one unsourced sentence (netting helps) for another (netting is not advised) is not a
  correction. FIX-8. Correction otherwise NEEDED: "Netting or trunk baffles help where pressure is
  heavy" has no anchor.
* **organic_treatment_beginner -- UNSUPPORTED (one sentence) + STYLE.** "Netting and trunk baffles
  are not something pawpaw growers are advised to use" -- same defect, stated more strongly (FIX-8).
  "Do not pick them hard and green" -- FIX-9. The rest HOLDS (ACES, Clemson, UIUC, UMD LCF).

Refusal check: exclusion_fencing refused -- defensible; the method's text is a ground-level electric
fence around a bed against raccoons, and no pawpaw document supports fencing for a home tree (MU's
"Deer control (cages)" is a cost-table line; UMD LCF's "if trees are unprotected" names no method).
bird_netting and bird_scare_deterrents refused -- right, no document. psu_ext dropped -- right
(names no mammal; "Reports are that deer do not prefer to eat pawpaw trees or the fruit." is hedged
and contradicted by the crop program). The unreachable_claims entry for antler-rub trunk protection
is the honest place for it (see RECORD-LEVEL 2).


## Phyllosticta leaf and fruit spot (`phyllosticta-leaf-and-fruit-spot`, fungal, medium)

### Ladder (2 rungs)

**airflow_spacing -- HOLDS.**
* B1 "needs the leaves and fruit to stay wet for a long stretch, from rain or heavy dew, and it is
  worst in humid places and rainy summers" -- MU: "When foliage or fruit remains wet from rainfall or
  dew for a prolonged period of time, infection can occur."; Clemson: "occurs in humid climates";
  Cornell SF: "only during periods of high humidity and frequent rainfall"; PBI-004: "Especially
  during wet years".
* B2 "Plant the tree where air moves, leave it room, and prune out crowded growth so the canopy dries
  quickly" -- Cornell SF: "Dense foliage and lack of proper ventilation contribute to this condition,
  so proper spacing and pruning can reduce it."
* B3 "no fungicide is labeled for pawpaw" -- Clemson: "Some fungicides may control it, but there are
  no fungicides labeled for use on pawpaws." (Lee County's "There are chemical options available for
  treatment of the pathogen." is generic to the genus and names none; Clemson's pawpaw-specific
  label statement governs.)
* S1-S3 same anchors; "the wet years when the fruit spots merge and the fruit cracks" -- Clemson:
  "hard black spots to form on the fruit skin, which often merge and leads to premature cracking."
  "prevents rather than rescues" is the method's own con. HOLDS.

**garden_sanitation -- HOLDS (mild SYNTHESIS on "reservoir").**
* B1 "Rake up the fallen leaves ... as they drop ... never into the compost pile" -- Lee County: "If
  you do have Phyllosticta, it is best to remove the leaf litter from beneath the infected plants as
  the leaves fall." / "Do not compost these leaves and debris."
* B1b "the spots keep shedding spores onto healthy leaves in wet weather" -- Lee County (quoting UMass
  Extension): "The fungus produces tiny, black fruiting bodies within the necrotic tissue and spores
  are easily disseminated to healthy foliage during wet weather."
* B2 "pick those off, cleaning your hands and tools before you touch another plant" -- Lee County: "If
  it is a small infestation you can pick the leaves off, and sterilize your tools and hands between
  treatments."
* B3 "A fruit that has cracked will quickly rot" -- MU: "When the flesh is exposed from cracking, it
  quickly becomes infected with other disease organisms and insects, resulting in unmarketable
  fruit."
* S1 "leaf litter under an infected tree is the reservoir to strip" -- Lee County prescribes litter
  removal but does not say litter is the overwintering reservoir (its only seasonality statement is
  "most evident after cool, wet winter and spring periods" and "it can be bad one year and not be
  seen the next year"). Mild SYNTHESIS; the prescription is the same either way. S2, S3 HOLD ("almost
  at once" for MU's "quickly" is fine).
* Scope, stated for the record: Lee County is generic Phyllosticta-in-the-landscape advice written
  from a pawpaw case; no pawpaw-specific document prescribes litter removal. The author and record
  pass both flagged this. Acceptable.

Missing / padding check: nothing cheap skipped (spacing, pruning, litter, pick-off all present); no
chemical tier reached, correctly (Clemson label). Lee County's "If it is in a large section of the
plant, you can cut out the infected area." filed as unreachable -- right, `prune_out_infection` is
fire-blight-shaped. Removal of cracked fruit is not prescribed by any document; the notes stop at
"it is a loss", which is what MU says.

### Corrections (6)

* **symptoms_seasoned -- HOLDS on every sentence, but OVER-CORRECTS by omission (FIX-10).** Tan spots
  with brown borders darkening to black (MU verbatim); hard black spots on fruit (Clemson); merge and
  crack in a wet year (Clemson; PBI-004: "Especially during wet years, fungal spot (Phyllosticta
  species) on leaves and the surface of fruit can lead to problems; infested fruit can to split during
  development." and caption "Fungal spot (Phyllosticta) on fruit leading to cracking."); exposed flesh
  colonized (MU); "Leaves are affected too, but the tree is not killed" (Clemson verbatim); wetness
  (MU); flyspeck distinction (Clemson: "A cosmetic fungal disease known as flyspeck (Zygophiala
  jamaicensis) ... only grows on the surface of the fruit and does not prevent it from being
  edible."). Correction NEEDED: "cosmetic ... the fruit inside remains sound" is refuted by Clemson
  ("A severe fungal disease"), MU, PBI-004 and Cornell SF ("cause the fruit to crack when it expands,
  reducing quality and storability"). What is now MISSING: the crop program's own statement that
  spotted but uncracked fruit is still good -- KSU Planting Guide: "Sometimes the fruit surface may be
  covered with patches that are hard and black; this is a fungus infection, but it seldom has any
  effect on flavor or edibility." The correction's `why` assigns the cosmetic description to
  flyspeck, but "patches that are hard and black" matches Clemson's Phyllosticta ("hard black spots"),
  not flyspeck (surface specks). The record pass's own honest formulation was: superficial black
  blotching alone does not spoil the fruit; in wet years the same complex cracks the fruit and the
  cracks let rot in. The correction kept the second half and dropped the first.
* **symptoms_beginner -- HOLDS, same omission (FIX-10).**
* **organic_treatment_seasoned -- HOLDS.** Clemson label; Cornell spacing/pruning; Lee County litter,
  no compost, pick-off, sterilize; MU cracked fruit. Nit: "picking them off is enough" is a shade
  stronger than Lee County's "you can pick the leaves off". Correction NEEDED: "cosmetic issue",
  "keep the tree vigorous" (no anchor) and "fully edible" (refuted for cracked fruit).
* **organic_treatment_beginner -- HOLDS.** Same anchors.
* **prevention_seasoned -- HOLDS.** Spacing/pruning (Cornell); litter (Lee County); wet years
  (PBI-004); varieties (Cornell SF: "There appears to be some variation in susceptibility among
  varieties, but nothing comprehensive has yet been published in this regard."). Correction NEEDED:
  "avoid overhead wetting" is in no pawpaw document (the mechanism makes it a fair inference, but
  it was unsourced, and removal is the conservative call). Dated-claim note in RECORD-LEVEL 7.
* **prevention_beginner -- HOLDS.** Same.

Refusal check: copper, sulfur, biofungicide, chlorothalonil, mancozeb refused -- right (Clemson
label sentence); water_at_the_base / wet_foliage_discipline refused -- right (no anchor). PLA-457:
confirmed none; no sulfur, oil or interval anywhere on this crop.


## FIX ITEMS

**FIX-1 (borer ladder, structural FIT -- orchestrator/Trevor decision).** The `garden_sanitation`
rung is a placeholder: its content is "sanitation has no documented target here" under a method
whose rendered text names borers as a target. The author's refusal is the correct reading of the
documents (PBI-004: "Usually, the great abundance of unaffected flowers on trees does not require
control of this insect."; ACES's sanitation sentence scoped to five other pests; MU's pruning
sentence is the webworm's). Recommend shipping the refusal, flagged for Trevor, rather than the rung;
validate_out.py refuses an empty ladder (lines 114-115), so this needs a decision, not a rewrite. If
the rung must ship to validate, FIX-2 and FIX-3 apply and the FIT defect remains.

**FIX-2 (borer rung, note_seasoned S4).** Text: "A commercial guide recommends orchard cleanliness
against pawpaw insects in general; expect it to do nothing in particular for the borer." Wrong: ACES
recommends it against five named other pests, not pawpaw insects in general. Settles: ACES ANR-3095,
"Other pawpaw pests may include stinging rose caterpillar ... and spotted wing drosophila. Trapping,
manual removal, and orchard cleanliness and sanitation are recommended to combat these pests."
Rewrite: "A commercial guide recommends orchard sanitation against several other pawpaw insects; it
does not name the borer, whose cycle runs inside the twig." Or drop the sentence.

**FIX-3 (borer rung, note_beginner B4).** Text: "Picking up dropped flowers and fruit is ordinary
orchard hygiene for a pawpaw, not a fix for this borer." Unsupported: no document calls flower pick-up
ordinary pawpaw hygiene. Drop the sentence; B3 already carries the reason.

**FIX-4 (borer organic_treatment_seasoned; soften organic_treatment_beginner).** Text: "Nothing
reaches the larva once it is inside the flower or the stem, and gathering dropped flowers does not
interrupt it". Wrong class: a mechanism (no spray penetrates) no document states, given as the
reason. Settles: PBI-004 "does not require control of this insect" (no product named in any document
read); MU AF1021 life cycle "eventually bore into stems where they continue to consume tissue until
they pupate and emerge from the twigs." Rewrite: "No product is named for it in any pawpaw guide, and
gathering dropped flowers has no documented effect: the larvae leave the floral tissue, bore into the
stem, pupate in the twigs and emerge from them." Beginner: "Picking up the fallen flowers is not a
control anyone recommends, because the caterpillar bores on into the twig, where it turns into a
moth."

**FIX-5 (borer rung B3 + symptoms_seasoned + symptoms_beginner + prevention_seasoned +
prevention_beginner; STYLE, region scope).** Text: "at bloom in April and May" (five fields and the
rung). The months come from a Missouri guide (MU AF1021 is "Growing and Marketing Pawpaw in
Missouri"); MU's transferable signal is "often when trees are blooming". Settles: MU, "The first
generation of adult moths emerges from twigs in April and May, often when trees are blooming."
Rewrite: "at bloom (April and May in Missouri)" or "at bloom in spring". Low harm because the notes
couple the months to bloom, but a Gulf-state reader blooming in March will look too late.

**FIX-6 (swallowtail rung B2 and S2; symptoms_seasoned; symptoms_beginner; plus `sources`).** Texts:
"without ever coming in numbers that hurt the tree" (rung B2); "never in great numbers" (rung S2);
"the larvae never appear in numbers large enough to defoliate a tree" (symptoms_seasoned); "there are
never enough of them to strip a tree" (symptoms_beginner). Wrong for young trees. Settles: MU AF1021,
"On newly-planted trees or seedlings, larvae can devour much of the foliage, but they rarely cause
severe damage on older trees."; ACES ANR-3095, "They can cause significant damage to young trees but
are rarely a problem on mature plantings." Rewrite: scope every "never" to an established tree ("on
an established tree they never come in numbers that hurt it; a newly planted tree or seedling can
lose much of its foliage, and that is the one case for picking them off"). This also ANCHORS the
rung's trigger clause, which is currently unsupported by the entry's own sources: add `mu_ext`
(AF1021) and/or `aces_ext` (ANR-3095) to the entry's `sources` and `anchoring_urls`. Wording nit in
S4: "removes the sole larval host" -> "removes the larvae of a native butterfly that has no other
host".

**FIX-7 (swallowtail symptoms_seasoned + symptoms_beginner; and the LARVAL DESCRIPTION GAP note).**
The correction removed the identification aid ("green-and-black banded caterpillar") on the ground
"no admissible document describes the larva's color". Two do. Settles: MU AF1021, "These larvae are
green or black ringed with narrow green, white, blue, or yellow bands and are up to 2 inches long.
The head region of larvae is the widest, tapering along length of the body."; ACES ANR-3095, "Larvae
are up to 2 inches long with green, white, blue, and yellow bands." Restore a description anchored to
those (e.g. "a smooth green or black caterpillar up to 2 inches long, ringed with narrow green, white,
blue or yellow bands, widest at the head"). The note to the orchestrator pointing at the Cornell LOF
page as the only description is wrong; MU's "head region ... widest, tapering" is the same trait as
LOF's "hunchback". The record pass missed this too (it quoted only the borer paragraph from MU and
only deer/borer from ACES) -- read the documents, not the report.

**FIX-8 (wildlife rung S1; organic_treatment_seasoned; organic_treatment_beginner).** Texts: "no
pawpaw guide describes netting or trunk baffles, and trapping the animals is an orchard practice"
(S1); "pawpaw guides do not describe netting or trunk baffles, and trapping the animals is an orchard
practice rather than a garden one" (seasoned); "Netting and trunk baffles are not something pawpaw
growers are advised to use" (beginner). Unsupported: universal negatives in consumer prose that no
document states; they replace the record's unsourced positive with an unsourced negative, which the
brief says is not a correction. The absence is true of every document read and of two web searches
(so not WRONG), but a consumer sentence cannot carry a reviewer's absence finding. The "rather than a
garden one" half is a claim no document makes; MU says only "These pests can be removed from the
site by trapping." Rewrite: drop the negatives; "Prompt picking is the practical defense for a home
tree." stands on its own. If trapping is mentioned at all: "A commercial orchard guide mentions
trapping; it is not a home measure any pawpaw guide describes" is still a negative -- prefer silence.

**FIX-9 (wildlife rung B2; organic_treatment_beginner; STYLE).** Texts: "fruit picked hard and green
never ripens"; "Do not pick them hard and green, because they will not ripen." Wrong cue: pawpaw
skin is green when ripe. Settles: UMD LCF, "Aromatic green- or yellow-skinned fruits ripen late
summer through early autumn."; KSU FAQ, "Color change is generally not a reliable indicator of
ripeness."; Clemson, "fruit do not ripen properly if picked when very firm." Rewrite: "fruit picked
while still firm will not ripen" / "Do not pick them while they are still firm".

**FIX-10 (Phyllosticta symptoms_seasoned + symptoms_beginner; omission).** The correction dropped the
only sourced reassurance that spotted, uncracked fruit is still edible. Settles: KSU Planting Guide,
"Sometimes the fruit surface may be covered with patches that are hard and black; this is a fungus
infection, but it seldom has any effect on flavor or edibility." (unnamed fungus; "hard and black"
matches Clemson's Phyllosticta description, not flyspeck). Add one sentence: "Spotting alone seldom
affects flavor or edibility; it is the cracked fruit that is lost." The `ksu_pawpaw` key on this
entry is anchored to PBI-004; quote the planting guide inline in the correction's anchor as the
author did for the borer's PBI-004 sentence.


## SUMMARY

Items graded: 26 (5 rungs + 21 corrections). Headline grade = worst sentence in the item.
* HOLDS 17 (airflow_spacing; Phyllosticta garden_sanitation; borer symptoms x2, prevention x2;
  swallowtail cause_seasoned; wildlife symptoms x2, cause x2; Phyllosticta corrections x6)
* WRONG 3 (swallowtail handpick rung; swallowtail symptoms_seasoned; swallowtail symptoms_beginner
  -- all the same absolute, contradicted for young trees)
* UNSUPPORTED 4 (wildlife prompt_harvest rung; borer organic_treatment_seasoned; wildlife
  organic_treatment_seasoned; wildlife organic_treatment_beginner)
* SYNTHESIS 1 (borer organic_treatment_beginner)
* FIT 1 (borer garden_sanitation rung)
* STYLE 0 as headline; two STYLE defects ride inside other items (FIX-5 months, FIX-9 "green")

FIX items: 10 (FIX-1 is a decision, not a rewrite). Two prior readings verified: V5 HOLDS; the
author's ACES scope finding HOLDS and the brief's description of that sentence is wrong. Every
refusal was the right call. Ladder caps honored: no borer spray rung, one swallowtail rung, no
Phyllosticta chemical tier, no PLA-457 interval.

Single most important finding: the swallowtail entry's "never" is contradicted by two T1 documents
the author did not open for this entry. MU AF1021 and ACES ANR-3095 both say a newly planted tree or
seedling can lose much of its foliage, which is exactly the trigger the author wrote into the handpick
rung as an unanchored hedge, and both describe the larva, which the author removed as undescribable.
The rung's shape is right; its anchoring is one key short. Second: three wildlife fields now carry a
universal negative ("no pawpaw guide describes netting") that replaced the record's unsourced
positive with the reviewer's own absence finding dressed as consumer fact.

Verdict on the two no-control ladders: the BORER refusal is correct and the placeholder sanitation
rung should not ship as-is (FIT by construction; two sentences need FIX-2/FIX-3 regardless) -- this is
the orchestrator's call to make and flag for Trevor. The SWALLOWTAIL handpick rung is the right shape
and is fixable in place with FIX-6 and FIX-7.


## RECORD-LEVEL FINDINGS (for a later pass, not fixed now)

1. **Brief precedent misdescribed.** BRIEF_authoring.md says the parsleyworm precedent is "ONE
   `handpick` rung". Canonical parsley and dill both carry `handpick` + `bt`. The author followed the
   brief's "do NOT add a bt" instruction anyway, which is right for pawpaw (no document mentions any
   treatment), but the precedent text should be corrected before it is cited again.
2. **Catalog gap: trunk protection.** Buck antler rub is the one home-relevant deer damage on pawpaw
   (KSU PG "in winter"; UMD LCF "potentially causing serious bark injury if trees are unprotected";
   ACES "They can also damage trunks by rubbing against them."). No method reaches a trunk guard or
   tree cage; `exclusion_fencing` is bed-perimeter electric fence. Filed as unreachable here; the
   same gap will recur on every young tree in this batch.
3. **Catalog gap: tolerate-and-monitor.** validate_out.py refuses an empty ladder (lines 114-115),
   so a problem whose documented answer is "do not control" cannot validate without a rung that
   contradicts its own method label. Two of pawpaw's four problems are in this class. Either a
   tolerate/monitor method, or an explicit `no_control: true` shape the validator accepts, is owed.
4. **Record pass under-read MU and ACES.** record_pawpaw.md quotes MU only for the borer and ACES only
   for deer, borer and the sanitation sentence, and concludes "no admissible document describes the
   larva's color" and "no source says young trees are at risk either". Both are false on documents
   the pass had open. Not a defect of this review's scope, but the record pass is the upstream the
   author trusted.
5. **KSU planting guide's unnamed "fungus infection".** "patches that are hard and black ... seldom
   has any effect on flavor or edibility" is unnamed; its description matches Clemson's Phyllosticta,
   not flyspeck. The author's `why` attributes the record's cosmetic framing to flyspeck; that is an
   inference. The crop program has said two things twelve years apart (1998: seldom affects
   edibility; 2010: can lead to problems, fruit splits). Both are carried once FIX-10 lands.
6. **Label claim is time-sensitive.** "there are no fungicides labeled for use on pawpaws" is Clemson
   HGIC 1360 rev. 2022-01-28. It is carried in four fields and two rungs. A label change would
   silently falsify all six; worth a dated tag in the cert log.
7. **Dated claim.** Cornell SF (2018) "nothing comprehensive has yet been published" is carried as
   "nothing comprehensive has been published" (prevention_seasoned). Eight years old; fine today,
   but it is an absence claim with a date.
8. **ncsu_ext key scope.** The Phyllosticta entry anchors lee.ces.ncsu.edu (county article). Author
   flagged it. Also: the toolbox page now prints "Talponia plummeriana" correctly; the record report's
   "plumeriana (sic)" is either stale or a misread.
9. **Calendar months from a state guide.** MU's April-May is Missouri. No convention exists for
   carrying a state guide's months into national consumer prose; FIX-5 is the local patch.
10. **Display-name candidates** (author flagged, agreed): foxes appear in every document that names
    raccoons, opossums and squirrels; flyspeck / sooty blotch is a separate cosmetic surface problem
    (Clemson, ACES, Cornell SF) that the corrected Phyllosticta entry now distinguishes in one
    sentence but does not carry.
11. **Deer fruit claim is split in the wider literature.** Purdue HO-220-W (2001) "Deer do not feed on
    the leaves, twigs, or fruit." vs KSU PG / Clemson / ACES. The author followed the crop program;
    right call; noted so the next reader does not re-litigate it.
