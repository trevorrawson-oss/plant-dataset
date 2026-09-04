# PLA-8 BATCH 25 -- INDEPENDENT SOURCE-TRUTH REVIEW: **OREGANO**

Reviewer: independent pass. Did not author. Read `BRIEF_review.md`, `out_oregano.json`,
`record_oregano.md`, `pinned_ids.json` (oregano block), `ADJUDICATIONS.md` (A1/A4/A9/A10/B7/B8/C1),
`orchestrator_verifications.md` (V4/V6), `control_methods.json`, and canonical
`crops_data_final.json` (shipped oregano/thyme/rosemary/lavender prose, `source_catalog`).

**Documents fetched and read for this review** (all 2026-09-04, several twice with independently
framed prompts):

| key | url | read? |
|---|---|---|
| `psu_ext` | https://extension.psu.edu/herb-garden-plants-oregano | yes, x2 |
| `rhs` | https://www.rhs.org.uk/herbs/oregano/grow-your-own | yes, x2 |
| `rhs` (mint rust profile) | https://www.rhs.org.uk/disease/mint-rust | yes, x2 |
| `uf_ifas` | https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/ | yes, x3 |
| `ncsu_ext` | https://content.ces.ncsu.edu/phytophthora-blight-and-root-rot-on-annuals-and-herbaceous-perennials | yes, x2 |
| `ucanr_ext` (Pest Note 7404, aphids) | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html | yes, x2 |
| `ucanr_ext_spider_mites` (7405) | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html | yes, x3 |
| UC IPM Pest Note 7493 (powdery mildew) | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7493.html | yes |
| `uc_ipm` (oregano host page) | https://ipm.ucanr.edu/home-and-landscape/oregano/ | yes |
| `uc_ipm` (oregano cultural tips) | https://ipm.ucanr.edu/home-and-landscape/oregano/cultural-tips/index.html | yes |

Scope reviewed: **5 entries, 21 rungs, 42 declared field corrections.**

---

## 1. Aphids (`aphids`, insect, low) -- 5 rungs

| # | rung | grade |
|---|---|---|
| 1 | `balance_nitrogen` | **HOLDS** |
| 2 | `garden_sanitation` | **HOLDS** |
| 3 | `water_spray` | **SYNTHESIS** |
| 4 | `beneficial_predators` | **SYNTHESIS** |
| 5 | `insecticidal_soap` | **SYNTHESIS** |

**1. `balance_nitrogen` -- HOLDS.** Every load-bearing clause is in pn7404, read directly:
"High levels of nitrogen fertilizer favor aphid reproduction, so never use more nitrogen than
necessary." The note's "Feed in small portions rather than in one push" is the document's own
instruction: "Instead, use a less soluble form of nitrogen and apply it in small portions throughout
the season rather than all at once." The seasoned register's "tracks the soluble nitrogen in new
growth" is a fair reading of that same pair of sentences. No defect.

**2. `garden_sanitation` -- HOLDS.** The quoted instruction exists: "Where aphid populations are
localized on a few curled leaves or new shoots, the best control may be to prune out these areas."
(My fetch returned the sentence without the "and dispose of them" tail the author's anchor quotes;
the substance is unaffected and the shipped disposal instruction is standard on the page.) The
crop-specific reason -- "oregano's aphids concentrate on young growth" -- is the right shape of
inference off `psu_ext`: "Aphids, spider mites, and white flies, which are often repelled by the
aroma of oregano emitted by mature plants, can be a problem for young seedlings."

**3. `water_spray` -- SYNTHESIS.** The method holds: pn7404 twice, "Another way to reduce aphid
populations on sturdy plants is to knock off the insects with a strong spray of water." The note's
seedling caution is the inference, not the document. Asked directly whether pn7404 cautions about
water-spraying tender or young plants, the answer was that it **does not**; what the page actually
prescribes for the seedling stage is a different remedy: "Because many vegetables are susceptible to
serious aphid damage primarily during the seedling stage, reduce losses by growing seedlings under
protective covers in the garden, in a greenhouse, or inside and then transplanting them when the
seedlings are older and more tolerant of aphid feeding." The note's "a stream forceful enough to
dislodge a colony will flatten a seedling" is a plausible reading of "sturdy plants" and the advice
it produces is good, but the mechanism is authored. Not a FIX; recorded so it is not later mistaken
for a UC IPM sentence.

**4. `beneficial_predators` -- SYNTHESIS.** Two clauses hold outright. Broad-spectrum harm: pn7404,
they "kill the natural enemies that provide long-term control of aphids and other pests." Ants:
pn7404, ants "protect the aphids from natural enemies" by tending them and feeding on their
honeydew. The clause that does not hold is **"Conservation costs nothing and is why most oregano
aphid flare-ups end on their own."** That is a crop-specific frequency claim; no document read says
anything about how most oregano aphid infestations end. Low consequence, but it is the same class
the author itself struck two entries later ("It is the main way oregano is lost" -- a ranking no
source makes).

**5. `insecticidal_soap` -- SYNTHESIS. See FIX-12.** The predator clause holds precisely, and better
than expected: pn7404, "Although these materials can kill some natural enemies that are present on
the plant and hit by the spray, they leave no toxic residue so they don't kill natural enemies that
migrate in after the spray." That single sentence carries both the "kills the soft-bodied predators
it wets" clause and the "leaves no residual" clause. The temperature clause drifts (FIX-12).

### Aphid field corrections (8) -- all HOLD

All eight are correct on the documents and all eight were **needed**:

* `symptoms_*`: the deleted "stressed, crowded plants" has no anchor, and `psu_ext`'s sentence
  (quoted above) is exactly the seedling-stage claim the replacement makes. The mechanism the record
  had is inverted relative to pn7404's nitrogen finding, which is the same defect adjudication A13
  records on thyme.
* `cause_*`: "typically grown with little or no pesticide" / "rarely needs spraying" were practice
  claims with no document. `uf_ifas` carries only the resistance half, verbatim as quoted: "While
  oregano is relatively pest-resistant, it can be susceptible to certain insects like aphids, spider
  mites, and thrips."
* `organic_treatment_*`: **the neem removal is right.** I confirmed neem appears in no document read
  for this crop, and the author authored no `neem_oil` rung to replace it. Both replacement
  instructions are pn7404 verbatim.
* `prevention_*`: "Check your plants regularly for aphids-at least twice a week when plants are
  growing rapidly" is verbatim in pn7404, and it was genuinely absent from the record.

---

## 2. Spider mites (`spider-mites`, **type corrected insect -> mite**, low) -- 5 rungs

| # | rung | grade |
|---|---|---|
| 1 | `even_watering` | **HOLDS** (FIT risk noted) |
| 2 | `water_spray` | **HOLDS** |
| 3 | `augmentative_release` | **HOLDS** (provenance note) |
| 4 | `insecticidal_soap` | **HOLDS** |
| 5 | `horticultural_oil` | **WRONG -- see FIX-1** |

**1. `even_watering` -- HOLDS, and it is used honestly.** This was a specific charge to check and it
survives. The type correction is real and load-bearing: I read `control_methods.json` directly and
`even_watering.applies_to` is `["physiological", "mite", "bacterial"]`, so the rung is legal only
under `mite`. The method's own mite branch is anchored to the same document as the entry
(`ucanr_ext_spider_mites`, pn7405) and says "it holds spider mites down too, since they build up
fastest on plants that have been left dry and stressed." pn7405 verbatim: "Plants under water stress
also are highly susceptible."

The honesty test is whether the note tells a drought-adapted subshrub to be kept moist. It does not.
`note_beginner`: "Oregano likes it on the dry side, but a pot baking through a heat wave is a
different thing, so water it before it starts to wilt." `note_seasoned` draws the distinction
explicitly: "between soil that drains fast and a rootball that has actually run out. The first is
how oregano should be grown; the second is what tips a mite population into a flare." That is the
right reading, and it is consistent with `uc_ipm` cultural tips ("Oregano is heat and drought
tolerant when established and requires little to moderate water") and with the crop's own root-rot
entry.

**FIT risk, flagged not graded WRONG:** the rung note is careful, but the *method* text a consumer
may see next to it is not. `even_watering.how_it_works_beginner` opens "Keep the soil evenly moist"
and "Wild swings between wet and dry are what trigger disorders", and `best_use` gives "roughly 1 to
2 inches per week". On the one crop in this batch whose highest-severity disease is a rot caused by
soil that stays wet, that pairing is the one place the ladder can read against itself. Worth a
render check before promote; it is a method-text problem, not an authoring one.

**2. `water_spray` -- HOLDS.** pn7405 verbatim on both halves: "In gardens and on small fruit trees,
regular, forceful spraying of plants with water often will reduce spider mite numbers adequately"
and "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants
adjacent to dusty roadways or at margins of gardens." The note's move from that finding to "wetting
the paths and bare ground nearby" is the document's own instruction: "Apply water to pathways and
other dusty areas at regular intervals."

**3. `augmentative_release` -- HOLDS.** Three claims, three verbatim matches in pn7405: scope ("The
purchase and release of predatory mites can be useful in establishing populations in large plantings
or orchards, but the best results are obtained by creating favorable conditions for naturally
occurring predators"); the failure mode ("if pest mites aren't available when predatory mites are
released, the predators starve or migrate elsewhere"); the ratio ("A good guideline is that one
predator is needed for every 10 spider mites to provide control").

*Provenance note, not a defect:* the closing clause, "it closes off sulfur afterward, which harms
predatory mites that are not sulfur-resistant," is **not** in pn7405. I searched the page for
"sulfur" and got all six occurrences back; none concerns predatory mites, and the Biological Control
section contains no sentence with "resistant". The claim's actual home is the shipped `sulfur`
control method's own caution list -- "Can harm released predatory (beneficial) mites unless they are
sulfur-resistant, disrupting natural mite control" -- which is sourced to `ucanr_ext` / pn7406. That
is legitimate method-level provenance under the repo's convention, and the author invoked exactly
that convention elsewhere. Recording it so a later pass does not go looking for it in pn7405.

**4. `insecticidal_soap` -- HOLDS.** pn7405 verbatim: "Be sure mites are present before you treat.
Sometimes the mites will be gone by the time you notice the damage; plants will often recover after
mites have left." and "If a treatment for mites is necessary, use selective materials, preferably
insecticidal soap or insecticidal oil." Putting the confirm-before-you-treat rule in the *first
treatment* rung rather than losing it is the right placement given there is no monitoring method.

**5. `horticultural_oil` -- WRONG on one number.** The selective-materials framing and the
broad-spectrum warning both hold. The interval does not. **See FIX-1.**

### Spider mite field corrections (8) -- all HOLD

All eight anchor cleanly and all eight were needed. The dust finding is the important addition and
it is verbatim; the deleted "indoor plants" claim is supported by nothing read; and
`organic_treatment_*` correctly promotes the published confirm-before-you-treat rule, which was
genuinely missing and is the least invasive step on the entry.

---

## 3. Root and stem rot (`root-and-stem-rots`, fungal, high) -- 5 rungs

| # | rung | grade |
|---|---|---|
| 1 | `improve_drainage` | **SYNTHESIS** |
| 2 | `certified_clean_stock` | **UNSUPPORTED** (one clause) -- FIX-4 |
| 3 | `garden_sanitation` | **SYNTHESIS** -- FIX-6, FIX-8 |
| 4 | `crop_rotation` | **HOLDS** |
| 5 | `soil_solarization` | **HOLDS** |

**Charge 1: were the unanchored "stem rot" and "not cold" claims actually removed? YES, completely.**
I grepped every consumer string on the entry for `stem`, `cold`, `crown`, `winter`, `frost`. The word
"stem" does not appear in any consumer string on this entry. No negation about cold survives in any
register. The shipped prose that carried them --

> `cause_seasoned`: "Soilborne root and stem rots ... Waterlogged ground and wet winters, **not
> cold**, are the underlying cause"
> `symptoms_beginner`: "often with dark, rotted stems and roots at the base. ... it comes from soggy
> soil, **not cold weather**."

-- is fully replaced. The author sided with adjudication A4 over the record pass, which had ruled
"excess winter moisture rather than to cold" **TRUE**. **The author was right and the record pass was
wrong.** The RHS sentence the record leaned on is "It's important to protect oregano from
waterlogging over winter, which will cause the roots to rot" -- read directly, it carries the
positive claim and no negation whatever. See also RECORD-LEVEL FINDING R1, which makes the removal
more strongly correct than either pass realized.

**Charge 2: the `ncsu_ext` Phytophthora-host claim.** **HOLDS, verbatim, oregano named by name.**
Read directly: "Herbaceous perennials that are susceptible to *Phytophthora* include lavender,
osteospermum, rosemary, delphinium, epimedium, **oregano**, polemonium, hosta, heuchera, euphorbia,
and others." This is a taxon-and-crop match, not a common-name proximity hit.

**Charge 3: the "lack of OMRI-approved products" sentence that terminates the ladder.** **HOLDS
verbatim**: "There is a lack of OMRI-approved products that effectively manage diseases caused by
*Phytophthora* species." Using a US source's US availability statement to terminate the ladder is
sound, and refusing to pad a soft-chemical rung on top of it is the correct call. **One scope
caveat:** the sentence is scoped to *Phytophthora*, while the entry is a generically named "Root and
stem rot" umbrella whose own anchor (`uf_ifas`) attributes root rot to "fungal infections" without
naming a genus. `organic_treatment_seasoned` reads correctly in context ("the pathogen"), but
`soil_solarization`'s "NC State records a lack of OMRI-approved products that effectively manage
Phytophthora diseases, so ... there is no spray to fall back on" quietly widens a Phytophthora fact
to cover every rot the entry name admits. Low consequence, since no OMRI product is coming for
Pythium either; recorded for the taxon pass.

**1. `improve_drainage` -- SYNTHESIS.** The best-sourced clause on the crop, and better anchored than
the author claimed: "the rot organisms need free water in the soil pores to move and infect" is
directly supported by NCSU, "They are more commonly referred to as water-molds due to their ability
to produce asexual, swimming spores in the presence of water", and "swimming spores can survive and
be transmitted to healthy plants by recycled irrigation water or from plant to plant in standing or
puddled water." The grouping claim is verbatim: "Prolonged irrigation or watering, poor drainage,
and standing water all favor disease development."

Two clauses are authored. The physiological gloss "when the plant is drawing almost nothing down and
the ground holds everything it gets" appears in no document. And **the winter emphasis is
region-scoped** -- see FIX-5b below.

**2. `certified_clean_stock` -- UNSUPPORTED on one clause (FIX-4).** The inspection instruction is
NCSU's own, and strongly: "Always inspect plants (above and below ground parts) and ensure they look
healthy before purchasing or accepting them into your facility," paired with "Affected roots would
appear brown to black or roots may be mostly decayed" for the pale-versus-brown contrast the beginner
note draws. The failing clause is the comparative. See FIX-4.

**3. `garden_sanitation` -- SYNTHESIS.** "Remove and destroy any infected plants" is NCSU verbatim,
and `uf_ifas` adds "Remove affected plants promptly to prevent the spread of disease." Two clauses
overreach: the containers claim (FIX-6) and the crown claim (FIX-8).

**4. `crop_rotation` -- HOLDS. This is the best rung on the crop.** Both halves are verbatim and from
two independent admitted sources. NCSU: "The pathogen can survive in soil from season to season, so
once the bed is infested the pathogen cannot be eradicated without extreme measures." `uc_ipm`
cultural tips: "Also avoid areas that have had previous disease problems." The note's framing --
"the fact that changes the advice from remove the plant to do not replant here" -- is exactly what
those two sentences license, and it was genuinely absent from the shipped record.

**5. `soil_solarization` -- HOLDS.** NCSU carries the method: "Soil solarization of infested landscape
beds may be effective for reducing the amount of the pathogen in the soil," and the note's "it lowers
what is living down there rather than clearing it out" is the honest reading of "reducing the amount
of". The numbers I chased are **not** unwarranted: NCSU gives no duration and does not mention clear
plastic, but the shipped `soil_solarization` control method carries "four to six weeks in the hottest
part of summer", "Transparent film, not black", "the top 12 to 18 inches" and the cool-climate
caution, all sourced to `ucanr_ext` pn74145. Method-level provenance, correctly relied on.

### Root rot field corrections (8) -- 6 HOLD, 1 SYNTHESIS, 1 STYLE

**Charge 4: the de-twinning of `organic_treatment_beginner`. VERIFIED INDEPENDENTLY, and the
replacement is TRUE but NOT oregano-specific.**

I confirmed the twin myself against canonical rather than taking the author's measurement. All four
crops ship this identical string:

> "Once the base is rotting there is no fix, so pull out and throw away affected plants. The answer
> is preventing it with good drainage, not curing it."

`len(set(...)) == 1` across oregano, thyme (`Root and crown rot`), rosemary (`Root and crown rot`)
and lavender (`Phytophthora root and crown rot`). The author's claim is exact.

I also re-measured the outcome. Scoring every one of oregano's new consumer strings against every new
consumer string on the batch's other six crops, both difflib orders, **one** pair clears 0.62 and its
score is **0.654** (oregano root rot `garden_sanitation/note_beginner` vs thyme
`crown-and-root-rot/organic_treatment_beginner`). Zero byte-identical. Internal register pairs: worst
rung-note pair **0.306**, worst field pair **0.668** (aphids/symptoms). Every number the author
reported reproduces.

**But "oregano-specific" does not hold.** The replacement --

> "A plant whose roots have rotted cannot be saved. Lift it, bin it, and wash whatever touched it.
> No spray fixes this one, and the disease stays behind in that soil, so treat the spot as suspect
> rather than replanting straight into it."

-- is TRUE in every clause (no cure: NCSU "Remove and destroy any infected plants" plus "cannot be
eradicated without extreme measures"; no spray: the OMRI sentence; persists in soil: verbatim), but
every one of those facts comes from a document that names **lavender, rosemary and oregano in the
same sentence**. Substituted into thyme, rosemary or lavender it would be equally true and equally
anchored. The similarity metric is satisfied; the underlying condition -- four crops sharing one
undifferentiated paragraph -- is resolved cosmetically, not substantively. The one genuinely
crop-scoped fact available here and unused is that oregano is the crop NCSU names in that host list.

It also carries a house-style defect: **see FIX-5.**

The other seven corrections hold. `prevention_*` in particular adds the soil-persistence instruction
that is the most actionable thing NCSU publishes and that the record carried nothing like.

*One `why`-accuracy note, filed not fixed:* `prevention_seasoned`'s rationale says "'Lean' soil and
'full sun' are **not anchored**." "Lean" is correctly unanchored (`psu_ext`: "well-drained, average
soil with a pH of 6.8"). "Full sun" is not: `psu_ext` says "It grows best in full sun with
well-drained, average soil", and `uc_ipm` cultural tips says "Oregano grows best if the plant
receives full sun to partial shade (at least 4 to 6 hours a day)". What is unanchored is full sun **as
a rot measure**, which is the correct and narrower reason. The deletion is right; the stated reason
overstates and, left in the record, would license a later pass deleting a well-anchored cultural
claim.

---

## 4. Mint rust (`oregano-rust`, fungal, medium) -- 4 rungs

| # | rung | grade |
|---|---|---|
| 1 | `airflow_spacing` | **UNSUPPORTED at entry scope** |
| 2 | `water_at_the_base` | **UNSUPPORTED at entry scope** |
| 3 | `certified_clean_stock` | **SYNTHESIS** (disclosed) |
| 4 | `garden_sanitation` | **HOLDS** on removal; **UNSUPPORTED** on one clause -- FIX-3 |

### Charge 1a: was the restraint on *Puccinia menthae* right? **YES. Uphold it.**

Four reasons, and I would uphold the refusal even if the catalog question were reopened tomorrow:

1. **The condition the brief set genuinely fails.** RHS's mint-rust profile does carry the binomial
   for the disease -- I read it: "*Puccinia menthae* completes its entire life cycle on one plant
   host and produces resting spores to pass through winter." But that page **never mentions oregano
   or *Origanum***; I asked directly and the answer was explicit. Its host sentence is "Mint rust
   infects several mint species as well as some related plants including marjoram and savory."
   Writing the binomial on oregano therefore requires chaining `psu_ext` (oregano gets mint rust) to
   `rhs` (mint rust is *P. menthae*) across two documents, neither of which makes the joined claim.
   That is precisely the two-step inference the catalog discipline exists to refuse.
2. **The binomial cannot be written safely without a caveat that is journal-only.** The one thing a
   reader would actually *do* with "*Puccinia menthae*" is conclude that the rusty mint by the back
   door is inoculum for the oregano. Koike et al. 1998 refutes that -- "Neither the oregano nor the
   sweet marjoram isolates infected spearmint (*Mentha spicata*)" -- and that sentence is in no
   admitted source. `source_catalog` holds **zero** journal entries (V6, which I re-confirmed:
   `pubmed` is ABSENT from the 219-key catalog). Naming the organism without the population caveat
   is more misleading than not naming it.
3. **The consumer gains nothing.** No rung on this ladder turns on the genus. The gardener's search
   term is "mint rust", which is what the display name now says.
4. **The record's own language supports the refusal.** `record_oregano.md` rules the binomial "tied
   specifically to *Origanum vulgare*" JOURNAL-ONLY and says it "cannot be written into the record
   under the current catalog". The author quoted that ruling accurately rather than reinterpreting it.

The two-step chain and admitting `pubmed` are both catalog decisions and the author correctly kicked
them upstairs rather than taking them.

### Charge 1b: do the two anchors say what is claimed? **YES, both, verbatim.**

* `psu_ext`, read twice: **"Oregano can be susceptible to fungal diseases such as mint rust and root
  rot."** Confirmed present. Also confirmed absent from that page: "Puccinia", "Botrytis", "gray
  mold", "powdery mildew".
* `rhs` oregano grow-your-own, read twice: **"The fungal disease mint rust can affect oregano, and
  occasionally insects may feed on the leaves."** Confirmed present, under Problem Solving.
* `rhs` mint-rust profile: symptoms confirmed verbatim, all three bullets -- "Pale and distorted
  shoots in spring"; "Dusty orange pustules on the stems and leaves. These may be followed by dusty
  yellow or black pustules"; "Large areas of leaf tissue die and plants may lose leaves". The control
  sentence is confirmed verbatim and slightly longer than quoted: **"Remove affected plants promptly
  before the black resting spores are formed and contaminate the soil."** The rhizome sentence is
  confirmed and is mint-scoped exactly as the author says: "In the case of garden mint it is also
  necessary to remove infected rhizomes."

**One anchor mis-attribution -- see FIX-11b.**

### Charge 1c: was removing "Caught early, pruning off affected parts can save the plant" right? **YES.**

The documents support removal, not spot pruning. RHS's only control instruction is removal of the
whole affected plant, before the resting spores form. RHS additionally publishes the carry-over route
that makes spot pruning futile: "It is known that resting spores present in the soil or contaminating
the outside of the rhizomes can infect new shoots in spring." Nothing read anywhere prescribes
pruning a rust off a plant. The shipped sentence had no anchor and pointed against every control
source. **Removal was correct and this is the single best call in the file.**

### Charge 1d: did any RHS UK product statement leak? **NO. Clean.**

Programmatic sweep of all 84 consumer strings for `fungicid|pesticid|RHS recommend|not available|
approved for use|registered for|insecticide`. Three hits, all UC IPM broad-spectrum-insecticide
cautions written for a US reader; **zero** product-availability statements. The two RHS sentences at
risk -- "No fungicides with activity against mint rust are available for use on mint or other herbs
that will be used for culinary purposes" and "The RHS recommends that you don't use fungicides" --
appear nowhere in the file. I also confirmed the RHS *oregano* page contains no occurrence of
"fungicide" or "pesticide" at all, so that page was never a leak vector. The author's `refusals`
entry on this is accurate and the reasoning ("it ends there because nothing US-scoped supports a
chemical rung, not because RHS says so") is the right one.

*A milder region-scope issue does exist and it is on the root-rot entry, not here: see FIX-5b.*

### Rung grades

**1. `airflow_spacing` and 2. `water_at_the_base` -- UNSUPPORTED at entry scope.** Both rungs are
built entirely on leaf-wetness duration. **Neither of this entry's two anchors says anything about
leaf wetness, humidity, crowding, spacing or overhead watering.** `psu_ext` names the disease in one
clause and stops. The RHS mint-rust profile gives symptoms, the rhizome/resting-spore cycle, removal,
hot-water treatment and the UK fungicide position -- and no cultural moisture advice at all.

Method-level provenance does not close the gap either: `airflow_spacing.sources` are `ucanr_ext`
(pn7406, powdery mildew on ornamentals) and `clemson_hgic` (cole crop diseases);
`water_at_the_base.sources` are `clemson_hgic` (tomato), `ucanr_ext_bacterial_speck` and
`ucanr_ext_snails_slugs`. Not one is a rust document.

The claims are **true rust biology** -- urediniospore germination does require free water -- and the
record pass ruled the shipped prose SURVIVES on that basis, citing `uconn_ext` ("They need wet leaf
surfaces to germinate and cause infection") and WSU ("prolong leaf wetness from irrigation, dew, and
rainfall favor rust development"). But the author deliberately declined to add `uconn_ext` (it never
mentions the crop) and `wsu_mint_rust` is **ABSENT from `source_catalog`** -- I checked. So the two
top rungs of this ladder currently rest on a mechanism that no cited document states for this disease.
Grading UNSUPPORTED at entry scope rather than WRONG, because nothing refutes it. **The fix is the
catalog decision the author already recommends** (`wsu_mint_rust` on the already-admitted
`s3.wp.wsu.edu` host), not a rewrite.

Worth naming plainly: on this ladder, the two rungs with the thinnest anchoring sit above the two
that carry the documented controls.

**3. `certified_clean_stock` -- SYNTHESIS, honestly disclosed.** The note explicitly scopes the
mechanism to mint and calls clean stock "the prudent move rather than a proven mechanism," which is
the correct handling of Koike's "Teliospores were not detected on either host" caveat, and no rung
asserts an oregano rhizome mechanism. Two things to record: the source is uncatalogued (WSU),
disclosed only inside a *different* field's anchor and carried by no provenance on the rung itself;
and the scope drops a qualifier (see FIX-11a).

**4. `garden_sanitation` -- HOLDS on removal, one UNSUPPORTED clause.** "RHS's instruction is to
remove affected plants promptly, before the black resting spores form" is verbatim. The air-currents
clause is not (FIX-3), and the leaf-picking instruction sits crosswise to the entry's own prose
(FIX-9).

### Mint rust field corrections (9 incl. `name`) -- 7 HOLD, 2 anchor-attribution

* `name` -> "Mint rust": **HOLDS.** Both anchor sentences confirmed verbatim; ruled by Trevor under
  B7 option (a). Consistent with `pinned_ids.json` and with C4.
* `symptoms_*`, `organic_treatment_*`, `prevention_*`: hold, all on RHS sentences I read directly.
  `prevention_*` correctly scopes the rhizome instruction to mint and discloses the uncatalogued WSU
  corroboration by name rather than laundering it.
* `cause_seasoned` / `cause_beginner`: the claims hold; **the anchor attribution does not** -- FIX-11b.

---

## 5. Powdery mildew (`powdery-mildew`, fungal, low) -- 2 rungs

| # | rung | grade |
|---|---|---|
| 1 | `airflow_spacing` | **HOLDS** (one number, FIX-10) |
| 2 | `sulfur` | **HOLDS** |

### Charge 2a: does any gray-mold or Botrytis content survive in consumer prose? **NO -- one word.**

I regex-swept every consumer string on the entry for `botrytis|gray|grey|mold|mould|moldy`. Exactly
**one** hit, and it is not a Botrytis claim: `symptoms_seasoned`, "dense enough there to **gray** out
whole shoots." Every occurrence of "Botrytis" and "gray mold" left in the file is inside
`field_corrections.why` / `.anchor` explanatory text, which is not consumer copy. The shipped
"Grayish moldy patches, spotting, or a powdery-white coating" and "Leaf fungi like gray mold and
powdery mildew" are gone from both registers. **The de-Botrytisation is clean.** The one surviving
word is FIX-7.

I independently confirmed the premise of the rename: `uf_ifas` does not contain "Botrytis", "gray
mold" or "grey mold", and does publish exactly two diseases for the crop -- "Oregano is generally
resistant to diseases, but it can occasionally suffer from fungal infections like powdery mildew or
root rot."

### Charge 2b: does any powdery-mildew text tell the reader to keep foliage dry or avoid overhead watering? **NO.**

The opposite. The entry states the correction three times, in both registers:

> `airflow_spacing/note_seasoned`: "powdery mildew infects without free water on the surface, so
> keeping the foliage dry is not the lever it is on most leaf diseases."
> `cause_seasoned`: "Unlike most leaf diseases, powdery mildew does not need water sitting on the
> leaf in order to infect."
> `cause_beginner`: "It is not caused by wet leaves, which is what makes it different from most leaf
> diseases."

All three are correct against UC IPM Pub 7493, read directly: **"Although relative humidity
requirements for germination vary, all powdery mildew species can germinate and infect without water
on the plant's surface"** and **"Water on plant surfaces for extended periods inhibits spore
germination and kills the spores of most powdery mildew fungi."**

### Charge 2c: did the entry import the rust entry's leaf-wetness logic? **NO.** The rust rungs run on
leaf-wetness duration; the mildew rungs run on canopy humidity, and `airflow_spacing/note_seasoned`
names the distinction explicitly rather than letting the shared method blur it. That matters because
the *method*'s own text would have blurred it: `airflow_spacing.how_it_works_beginner` reads "so
leaves dry quickly after rain or dew. Most leaf diseases need long wet periods to take hold." The
rung note defuses its own method. **That is the strongest single piece of authoring on this crop.**

### Charge 2d: adjudicating the refusal of half the entry's own anchor. **THE AUTHOR IS RIGHT. Uphold it.**

`uf_ifas` verbatim, confirmed on my own fetch: **"To prevent powdery mildew, provide good air
circulation around plants and avoid overhead watering."** The author kept the first half and dropped
the second. Four reasons to uphold, one of them stronger than the author claimed:

1. UC IPM 7493's two findings above make "avoid overhead watering" mechanically backwards for this
   pathogen: free water is not required for infection, and prolonged surface water actively inhibits
   germination.
2. **7493 goes further than the author cited, in its own words rather than via 7406:** "Overhead
   sprinkling can reduce the spread of powdery mildew because it washes spores off the plant." The
   author attributed that finding to 7406; it is in 7493 itself. The refusal is on firmer ground than
   the author knew.
3. Batch adjudications A9 (sage) and A10 (rosemary) make the identical correction on the identical
   basis, so keeping it on oregano would leave three of four powdery-mildew crops corrected and one
   not.
4. The shipped `wet_foliage_discipline` method already carries the exception as an explicit caution
   -- I read it: "Powdery mildew is the exception and this does not act on it: USU notes that powdery
   mildews do not spread in rain or free water..." -- so the dataset had already ruled this once.

**And the deletion costs the reader nothing on this crop**, which is the part worth stating: oregano
also carries mint rust, a genuine leaf-wetness disease, and `water_at_the_base` sits on *that*
ladder. The advice survives where it is true and is withdrawn where it is not. Exactly right.

The author's handling deserves note independently of the outcome: it filed the conflict in `refusals`
in capitals, named the sentence it did not carry, and predicted that a reviewer would find it. I did,
and it was where the refusal said it would be. That is the behavior the pass is for.

### Rung grades

**1. `airflow_spacing` -- HOLDS.** `uf_ifas` verbatim on both halves: "To prevent powdery mildew,
provide good air circulation around plants" and "Space your plants 10-12 inches apart, this will help
with air circulation and prevent extra humidity." UC IPM 7493 corroborates the method: "Provide good
air circulation by pruning excess foliage and properly spacing plants." One number drifts (FIX-10).
"reliably keeps powdery mildew down" is a mild strengthener over "provide good air circulation";
noted, not filed.

**2. `sulfur` -- HOLDS on every clause.** Anchored on this crop: `uf_ifas`, "Apply fungicidal sprays
containing sulfur or copper if necessary, following label instructions." Protectant framing: UC IPM
7493, "Sulfur products have been used to manage powdery mildew for centuries but are effective only
when applied before the disease appears," and the shipped method's con, "Protectant only; it does not
cure existing infections." Both cautions are verbatim-correct here: 7493, **"Do not apply sulfur when
the temperature is near or higher than 90°F, and do not apply it within 2 weeks of an oil spray"** --
which is exactly the note's "near or above 90°F and at least two weeks away from any oil spray". The
same method's caution list carries both figures identically.

**Ladder length: correct, not padded.** Two rungs on a `low`-severity disease whose crop-scoped
evidence is one blog paragraph is the honest shape. The `copper_fungicide` refusal is well reasoned:
`uf_ifas` names copper in the same clause, but the shipped `copper_fungicide` method describes downy
mildew and bacterial leaf spots and claims no powdery mildew activity, so authoring it would double
the chemical end for nothing.

### Powdery mildew field corrections (9 incl. `name`) -- 6 HOLD, 1 SYNTHESIS, 2 WRONG

* `name` -> "Powdery mildew": **HOLDS**, premise verified independently (above). Reuses the existing
  32-crop id per B8.
* `symptoms_seasoned`: SYNTHESIS, FIX-7. `symptoms_beginner`: HOLDS.
* `cause_seasoned` and `cause_beginner`: **WRONG on one added word. FIX-2. This is the most important
  finding in the file.**
* `organic_treatment_*`: HOLD. Both deletions justified; the sulfur addition is anchored on the crop.
* `prevention_*`: HOLD. The deleted "favor upright culinary types over dense low ones" is a varietal
  claim with nothing behind it in any document read, and the author is right that it is the shape a
  prevention field pulls out of growth habit. Removing it before a variety pass turns it into a
  `varieties[].resistance` claim is the right sequencing.

---

# FIX ITEMS

Ordered by consequence.

### FIX-2 (HIGH) -- `powdery-mildew` / `cause_seasoned` + `cause_beginner`: "hot" was added, against the document the same field cites

**Exact text.**
> `cause_seasoned`: "Oregano is generally resistant to disease, so this is mainly a **hot,
> humid-summer** and overcrowding problem."
> `cause_beginner`: "Oregano is fairly disease-resistant, so this is mostly a **hot, humid-weather**
> and crowding problem."

**What is wrong.** "Hot" is not carried over -- it is **new**. The shipped prose read "mainly a
humid-climate and overcrowding issue" and "mostly a humid-weather problem", with no temperature
claim. The correction introduced one, and it points the wrong way.

**The sentence that settles it.** UC IPM Pest Note 7493, read directly, and cited by this very field
two sentences later for the free-water point:

> "Moderate temperatures of 60° to 80°F and shady conditions are most favorable for powdery mildew
> development."

Batch adjudication A9 records the same fact in the same words ("favoring conditions are 60-80°F **and
shade**"). The author applied A9's leaf-wetness half and wrote against its temperature half on the
same entry.

**The anchor does not carry it either.** The anchor cites `uf_ifas`, "Our high temperatures and
humidity can be challenging." I asked the page directly where that sentence sits: it is under the
heading **"Tips for the Floridian Gardener"**, alongside "Choose oregano varieties that can thrive in
hot climates." It is a general Florida-gardening remark, not a powdery mildew statement, and reading
it as one is a document-subject error.

**Why this is the most important finding.** It is the only place in 42 corrections where a *declared
correction made a field less true than the prose it replaced*, and it did so on the one entry whose
whole existence is a correction of powdery-mildew mechanism. The reader's practical loss is real: told
this is a hot-summer problem, they will stop watching for it in the mild, shaded, 60-80°F conditions
UC IPM says actually favor it.

**Suggested repair:** drop "hot" and keep the humidity and crowding claims, which `uf_ifas` does
anchor through the spacing sentence. If a temperature statement is wanted, 7493's 60-80°F band and
shade are available and are already in the batch's adjudication surface.

---

### FIX-1 (HIGH) -- `spider-mites` / `horticultural_oil` / `note_seasoned`: the oil-sulfur interval is half what this entry's own anchor gives

**Exact text.**
> "Keep oil and sulfur **at least two weeks** apart, since the combination injures foliage."

**What is wrong.** Two weeks is the *powdery mildew* figure. On a spider-mite entry the governing
document is Pest Note 7405, and it gives 30 days.

**The sentence that settles it.** `ucanr_ext_spider_mites`, Pest Note 7405 -- the entry's own listed
anchor, whose catalog url is exactly this page -- read directly:

> "Don't use sulfur if temperatures exceed 90°F, and don't apply sulfur within **30 days** of an oil
> spray."

I searched that page for every occurrence of "sulfur" and of "30 days / 2 weeks / two weeks": six
sulfur sentences, one interval sentence, and it says 30 days. The 2-week figure comes from UC IPM 7493
and from the shipped `sulfur` method's caution (sourced to pn7406), i.e. from the powdery-mildew
literature, imported onto a mite ladder. This is defect class 5, a number restated from the wrong
warrant, and it is the one place in the file where following the copy could damage a plant.

**Secondary:** "since the combination injures foliage" is in neither document. 7405 attributes burn to
sulfur alone ("This product will burn cucurbits and other plants in some cases"); the interval
sentences give no reason.

**Suggested repair:** "at least a month apart" (or state UC IPM's 30 days), and drop or re-source the
reason clause. Note the two UC documents genuinely disagree; on this entry, 7405 governs.

---

### FIX-3 (MEDIUM) -- `oregano-rust` / `garden_sanitation` / `note_seasoned`: the air-currents reason is unsupported

**Exact text.**
> "Carry what you remove out in a bag rather than shaking it over the bed, **since rust spores move
> easily on air currents**."

**What is wrong.** The action is sensible; the reason is in neither anchor. I asked the RHS mint-rust
profile directly for any sentence describing spore spread by wind, air currents or splashing and got:
"No sentence on the page describes how spores spread via wind, air currents, or splashing." `psu_ext`
names the disease and says nothing further.

**The sentence that settles it** -- and it is a different mechanism entirely. RHS publishes one
carry-over route and it is not airborne:

> "It is known that resting spores present in the soil or contaminating the outside of the rhizomes
> can infect new shoots in spring."

Airborne urediniospore dispersal is real rust biology and is presumably where this came from (the
`certified_clean_stock` note contrasts against "spores arriving on the wind"), but its likely home is
the uncatalogued WSU document. Same class as the aphid "vigorous enough to shrug off" defect
adjudication A13 records on thyme: right practice, invented reason.

**Suggested repair:** keep the bagging instruction, tie the reason to the sentence RHS does publish
(get it out before the black resting spores form and contaminate the soil), or drop the reason.

---

### FIX-4 (MEDIUM) -- `root-and-stem-rots` / `certified_clean_stock` / `note_seasoned`: an unsourced frequency comparison

**Exact text.**
> "**These pathogens arrive with the plant more often than they arrive on their own**, and a bed that
> has been infested stays infested, so the inspection at purchase buys more than anything available
> afterward."

**What is wrong.** NCSU documents both routes and ranks neither.

**The sentences that settle it.** `ncsu_ext`, read directly, gives the plant-material route --
"The pathogen can be transmitted between and among greenhouses on infected plant material" -- and,
separately, the landscape route: "In the landscape, soil can become infested when affected plants are
established." No comparative appears anywhere on the page. Note also that the transmission sentence is
scoped to greenhouses, which weakens rather than supports the home-garden generalization.

This is the same defect class the author correctly struck from this entry's `symptoms_seasoned` --
"It is the main way oregano is lost", removed with the reason "a ranking no source makes, which was
left reading as sourced." The identical construction survived one rung away.

The second half is fine: "stays infested" is verbatim ("cannot be eradicated without extreme
measures"), and "buys more than anything available afterward" is defensible given the OMRI sentence.

**Suggested repair:** state both routes without ranking them, or cut to the inspection instruction,
which NCSU gives verbatim: "Always inspect plants (above and below ground parts) and ensure they look
healthy before purchasing or accepting them into your facility."

---

### FIX-5 (MEDIUM) -- two problems in the de-twinned root-rot prose

**5a. British English.** `root-and-stem-rots` / `organic_treatment_beginner`:

> "Lift it, **bin it**, and wash whatever touched it."

"Bin it" is British. CLAUDE.md: American English. ("Lift" for dig up is also BrE gardening idiom,
though it is naturalized enough in US horticultural writing that I would not file it alone.) This is
register leakage from the batch's UK source into the one field that was rewritten specifically to end
a four-crop twin, so it will read as the new canonical sentence. **Suggested repair:** "Dig it out,
throw it away, and wash whatever touched it."

I swept all 84 consumer strings for British spellings and idiom; this is the only hard hit. "Compost
heap" appears three times on the rust entry -- acceptable in American gardening usage, flagged only
because it is the same source's register.

**5b. A UK-climate claim carried as universal.** `root-and-stem-rots` / `cause_seasoned` +
`cause_beginner` + `improve_drainage/note_seasoned`:

> "Wet ground over winter is the **hardest case**" / "the **worst of it**" / "RHS puts the same weight
> on winter"

The sole anchor for the winter emphasis is RHS, and `source_catalog`'s own entry for `rhs` warns:
"UK-centric climate guidance requires translation to USDA hardiness zones for North American
application." Winter waterlogging is a mild-wet-UK-winter framing; for a US reader in an arid or a
hard-freeze region it is not the hardest case. This is the brief's defect class 4 in its milder form,
and it is the one place RHS's UK scope actually bites on this crop -- the pesticide check came back
clean.

Mitigating: the shipped prose already said "worst over a wet winter", so this is inherited rather than
created; and adjudication A5 quotes UMD ("Excessively wet, cold soil can cause Mediterranean herbs
such as rosemary, thyme, and lavenders to die over the winter"), which supports the phenomenon in the
US -- but that sentence involves cold, which this batch deliberately dropped, and UMD is not among
this entry's sources. Filed as MEDIUM because both `cause` registers were re-declared, so it was in
scope for the correction and was carried forward unexamined.

**Suggested repair:** hold the claim at the level RHS actually states it ("waterlogging over winter
will cause the roots to rot") without the superlative, or source the US form.

---

### FIX-6 (LOW-MED) -- `root-and-stem-rots`: "containers" is not on NC State's sanitation list

**Exact text.** `garden_sanitation/note_seasoned`: "**Sanitizing both** sits on NC State's cultural
list" (the "both" being tools and containers). And `organic_treatment_seasoned`'s anchor: "plus the
same document's cultural list **for sanitizing tools and containers**."

**The sentence that settles it.** NCSU's bullet, read directly and quoted with its own typo:

> "Implement proper **santiation** practices for tools, equipment, benches, and floors."

Containers and pots are not on that list. The advice is sound and the beginner note's "Wash the pot
and the tools" is good practice, but the attribution asserts more than the document carries -- and it
does so in an `anchor` field, which is where a later pass will check.

**Suggested repair:** attribute tools and equipment to NCSU; leave the pot as unattributed practical
advice or drop the "both".

---

### FIX-7 (LOW) -- `powdery-mildew` / `symptoms_seasoned`: "gray out whole shoots"

**Exact text.**
> "...heaviest inside a crowded clump where the air sits still and dense enough there to **gray out
> whole shoots**."

Two problems in one clause. It is unanchored -- `uf_ifas` publishes "Powdery mildew appears as a
white, powdery coating on oregano leaves," and nothing read describes graying. And it is the **only**
surviving gray-vocabulary in the entry whose rename exists to remove Botrytis, sitting in the exact
field the correction targeted. A reader who knows gray mold will read it as gray mold.

It is also the weakest phrase in the file on the common-tongue rule.

**Suggested repair:** "dense enough to coat whole shoots" or "thick enough to cover whole shoots".

---

### FIX-8 (LOW) -- `root-and-stem-rots` / `garden_sanitation` / `note_seasoned`: "no rescue at the crown"

**Exact text.** "**There is no rescue at the crown**, so the only in-season decisions are..."

The correction's stated basis for stripping "stem rot" is that "no anchor on this crop describes a
stem rot; the read documents describe root decay." The same objection reaches "crown". `uf_ifas` says
root rot; `ncsu_ext`'s oregano-relevant sentence is "Affected roots would appear brown to black or
roots may be mostly decayed"; NCSU's only crown-rot sentence is about **petunias** ("a crown rot may
cause plants to wilt rapidly or partially resulting in plant collapse"). Inherited from the shipped
prose ("no cure once the crown and roots are rotting"), but it survives inside a rung the pass
re-authored on the strength of removing exactly this kind of unanchored structure.

**Suggested repair:** "There is no rescue once the roots have gone."

---

### FIX-9 (LOW) -- `oregano-rust`: the entry prose and the rung tell the reader different things

`organic_treatment_beginner`: "**Pull out badly infected plants rather than trying to cut the disease
off them**."
`garden_sanitation/note_beginner`: "**Pick the rusty leaves off as soon as you see them** and put them
in the trash... If a plant is covered in pustules, take the whole plant out."

They are reconcilable as a sequence, but the entry prose is written as a flat prohibition on cutting
the disease off and the rung opens by instructing exactly that. Separately, **leaf-picking is anchored
by neither of this entry's two documents** -- RHS's only instruction is whole-plant removal. The
record pass's support for it is `uconn_ext` ("remove all rust-infected leaves and heavily infected
plants"), which the author deliberately declined to admit because it never mentions the crop.

**Suggested repair:** make the sequence explicit in the entry prose (early marked leaves out, a
heavily infected plant out whole), or drop the leaf-picking sentence to match the anchors.

---

### FIX-10 (LOW) -- `powdery-mildew` / `airflow_spacing` / `note_seasoned`: the spacing range floor

**Exact text.** "Published spacing for oregano runs from **10 inches** up to 18 inches depending on
which extension source you read."

`uf_ifas` gives 10-12 and `uc_ipm` gives "at least 18 inches", so the ceiling is right. But `psu_ext`
-- already cited on this crop, on two other entries -- publishes "thinned to about **8-12 inches**
between plants", and RHS publishes "space it at least **20-30cm (8-12in)** from neighbouring plants".
The floor is 8, not 10.

Partially defensible: `psu_ext`'s figure is a direct-sow thinning distance rather than a mature
spacing. Filed LOW because the sentence explicitly invites the reader to compare extension sources and
then omits the two that would widen the range.

---

### FIX-11 (LOW) -- two attribution items on `oregano-rust`

**11a. A scope qualifier dropped.** `certified_clean_stock/note_seasoned`: "On mint, where this
disease is best documented, **outbreaks are usually traced** to infection already inside the rhizomes
and stem cuttings used for propagation." Per `record_oregano.md`, WSU's sentence is scoped to
**greenhouse** outbreaks: "Such rust outbreaks are usually initiated from systemic infections and
pustules on rhizomes and stem cuttings used in propagation," quoted there in a greenhouse context.
The note generalizes to outbreaks at large. Also worth recording that the rung's whole mechanism rests
on a document with **no catalog key** (I confirmed `wsu_mint_rust` is absent from the 219-entry
`source_catalog`), disclosed only inside a different field's anchor.

**11b. A quote attributed to the wrong RHS page.** `cause_seasoned` / `cause_beginner` anchor:

> "rhs, https://www.rhs.org.uk/herbs/oregano/grow-your-own: ... 'Mint rust is a common fungal disease
> of garden mint, **but also affects marjoram and savory**.'"

I fetched the oregano grow-your-own page twice, the second time asking directly whether it contains
"marjoram" or "savory". It returned four marjoram sentences and: **"The page does not contain 'savory'
or 'savoury'."** The claim is real, and I confirmed it verbatim -- on the **mint-rust profile**:
"Mint rust infects several mint species as well as some related plants including marjoram and savory."

**Caveat, stated because it matters:** the oregano page's mint-rust block truncates at fetch in every
attempt ("The fungus causes dusty orange, yellow and black spots on l..."), which is what the author
flagged too, so I cannot rule out that the sentence is behind the truncation. **Recommendation:**
re-attribute the quote to `https://www.rhs.org.uk/disease/mint-rust`, where I read it, rather than
leaving it on a page two independent fetches say does not carry it. The prose claim itself HOLDS
either way.

---

### FIX-12 (LOW) -- `aphids` / `insecticidal_soap` / `note_seasoned`: a threshold widened and a mechanism asserted

**Exact text.** "...and off any plant when the temperature is **near** 90°F, **since that is when the
foliage burns**."

pn7404 verbatim: "Also, don't use soaps or oils on water-stressed plants or when the temperature
**exceeds** 90°F." And on phytotoxicity, the page hedges where the note asserts: "These materials
**may be phytotoxic to some plants**, so check labels and test the materials on a portion of the
foliage several days before applying a full treatment."

Erring conservative on temperature is defensible; asserting that foliage burns at that threshold,
where the source says the materials may be phytotoxic to some plants, is the unsourced-reason class.
Very low consequence. Note the entry's `horticultural_oil` sibling gets this right
("above 90°F", no invented reason).

---

# SUMMARY

## Counts by grade

**Rungs (21):**

| grade | count |
|---|---|
| HOLDS | 9 |
| SYNTHESIS | 7 |
| UNSUPPORTED | 4 |
| WRONG | 1 |
| FIT | 0 |
| STYLE | 0 |

**Declared field corrections (42, including 2 `name` corrections):**

| grade | count |
|---|---|
| HOLDS | 35 |
| WRONG | 2 |
| SYNTHESIS | 2 |
| FIT (anchor mis-attribution) | 2 |
| STYLE | 1 |

**Combined (63 graded items):** HOLDS 44, SYNTHESIS 9, UNSUPPORTED 4, WRONG 3, FIT 2, STYLE 1.
**12 FIX items filed**, 2 HIGH, 4 MEDIUM/LOW-MED, 6 LOW.

## Was each correction NEEDED?

**41 of 42 yes.** Every deletion I checked removed a claim no document read supports, and I confirmed
the specific ones the brief flags: neem (absent from every document read), the vigor inversion (the
thyme A13 twin), the indoor-mite claim, the upright-versus-mat varietal claim, the stem rot, the "not
cold" negation, and Botrytis. The one correction I would grade as *not needed on its stated grounds*
is `oregano-rust` / `cause_*`, and the author labels it honestly as a rename-fit and dual-register
change rather than a sourcing fix, which is the right label -- I re-measured the shipped pair at
**0.711** and confirm it is above the batch threshold.

## The single most important finding

**FIX-2. The powdery-mildew `cause` fields added "hot" as a driver of the disease, contradicting UC
IPM Pest Note 7493 -- the document the same field cites two sentences later -- and contradicting the
batch's own adjudication A9, which records the favoring conditions as "60-80°F and shade".** The
shipped prose said only "humid-climate"; the correction introduced the error. It is the only place in
42 corrections where a declared correction made a field less true than the prose it replaced, and it
landed on the one entry that exists to correct powdery-mildew mechanism. The anchor offered for it,
`uf_ifas`'s "Our high temperatures and humidity can be challenging", sits under the heading "Tips for
the Floridian Gardener" -- a general growing-difficulty remark, read as a disease statement.

## What the pass got right, stated because it is most of the file

* Both renames are correct and both premises verified independently against the documents.
* **The `Puccinia menthae` restraint was right.** RHS's mint-rust page never mentions oregano or
  *Origanum*; the binomial reaches this crop only by a two-step chain across two documents; and the
  caveat that makes it safe to write is journal-only in a catalog with zero journal entries.
* **The "Caught early, pruning off affected parts can save the plant" removal was right** and is the
  best call in the file. Nothing read prescribes pruning a rust off a plant; RHS prescribes removal
  before the resting spores form.
* **No RHS UK product-law statement leaked.** Swept; zero hits; the two at-risk sentences appear
  nowhere.
* **The powdery-mildew de-Botrytisation is clean in consumer prose** (one word, FIX-7), and **no
  keep-the-foliage-dry advice survives anywhere on the entry.**
* **The `uf_ifas` half-sentence refusal is correct**, and better founded than the author realized:
  7493 itself, not only 7406, says overhead sprinkling can reduce powdery mildew spread. Flagging the
  conflict in `refusals` instead of burying it is the behavior this pass exists to reward.
* **`even_watering` is used honestly** on a drought-adapted subshrub, and **no sulfur rung was
  smuggled onto the mite ladder** even though I confirmed the type correction makes it legal
  (`sulfur.applies_to` includes `mite`).
* **The four-crop byte-identical twin is real** -- I reproduced it from canonical -- **and is ended.**
  Cross-crop maximum against the batch's six other new files is 0.654, zero byte-identical; internal
  register pairs top out at 0.668 (field) and 0.306 (rung note). Every measurement the author reported
  reproduces exactly.
* Ladder lengths are honest. Mint rust ends at cultural because nothing US-scoped supports a chemical
  rung; root rot ends at physical on a US availability statement; powdery mildew is two rungs. No
  padding anywhere.

---

# RECORD-LEVEL FINDINGS

Filed for a later pass, not fixed now.

### R1. `uf_ifas` DOES discuss cold and winter. Both the record pass and orchestrator verification V4 assert it does not.

`record_oregano.md` states: "Confirmed by regex-style term check on a second fetch: the words 'rust',
'Botrytis', 'gray mold', 'airflow' and **'winter'** do not appear on this page." `orchestrator_
verifications.md` V4 states the document "attributes root rot solely to excess moisture and **says
nothing about cold or winter either way**." My task brief repeats it.

Read directly, twice, with the question asked term by term, the page carries all three:

> "Oregano is a **winter**-hardy herb, and even if it dies back, it will grow back in the spring."
> "Still, it doesn't hurt to protect the plant from **frost**; temperatures in the low 40s are too
> **cold** for oregano."
> "In Florida, the best time to plant oregano is during the cooler months of fall and **winter**."

**The outcome is unaffected and in fact strengthened.** The "not cold" negation still has no anchor,
and dropping it was right -- more so, since the crop's own primary anchor makes a cold claim, so
writing "not cold" would have contradicted the entry's own source page as well as UMD. But the
verification record is wrong on a factual absence check, and a later pass reasoning from "the page
says nothing about cold" will be misled. Same shape as the cached-verdict-as-false-presence failure.
Both records should take a correction line.

### R2. `uf_ifas` contradicts itself on watering, and neither pass disclosed it.

The root-rot entry's sole crop-scoped anchor tells the reader:

> "Additionally, ensure oregano receives regular watering, **aiming to keep the soil consistently
> moist** but not waterlogged."

while the same page also says "Oregano prefers slightly dry, well-draining soil with a slightly
alkaline pH" and "Oregano is drought-tolerant, so it will struggle if it is sitting in standing water
or grown in soil that is waterlogged."

The ladder takes the second position -- `improve_drainage/note_beginner`: "Water it, then let it dry
out before watering again"; `prevention_seasoned`: "keep plants on the dry side" -- which is the
correct one and is independently supported by `uc_ipm` cultural tips ("Oregano is heat and drought
tolerant when established and requires little to moderate water"). **No correction is needed.** But
this entry's entire crop-scoped footing is one templated blog post that PART D and V4 already identify
as find-and-replace boilerplate, and an internal contradiction inside it is exactly the artifact you
would predict from a template. It belongs in the template note, not undisclosed. It also compounds the
`even_watering` FIT risk noted on the mite ladder.

### R3. Two unreachable claims the author did not list.

The `unreachable_claims` block is unusually good (six entries, each with the method it would need and
why it was not bent onto a neighbor). Two more belong on it:

**(a) Overhead sprinkling as a POSITIVE powdery-mildew step.** UC IPM 7493: "Overhead sprinkling can
reduce the spread of powdery mildew because it washes spores off the plant," with the timing rule "The
best time to irrigate is mid-morning, so plants dry rapidly, reducing the likelihood of infections by
other fungi." `water_spray.applies_to` is `["insect_soft_bodied", "mite"]`, so no fungal entry can
reach it. This is a free, documented step the ladder cannot carry -- and it is the constructive half
of the very finding the entry uses to justify a deletion.

**(b) Conservation of resident predators on a MITE entry.** UC IPM 7405: "the best results are
obtained by creating favorable conditions for naturally occurring predators."
`beneficial_predators.applies_to` is `["insect_soft_bodied", "insect_general"]` -- **no `mite`** -- so
the mite ladder cannot carry a conservation rung even though its own `augmentative_release` note says
"The predators already in your garden do more." The aphid ladder gets the rung; the mite ladder, whose
source says the same thing more strongly, cannot. Method-coverage gap, not an oregano gap.

### R4. The sulfur / predatory-mite fact is not in pn7405.

Recorded so a later pass does not go looking. Its home is the shipped `sulfur` method's caution list,
sourced to `ucanr_ext` / pn7406. Legitimate method-level provenance; noted only because the
`augmentative_release` note reads as though it were a pn7405 finding, and the same rung's other three
claims are pn7405 verbatim.

### R5. The `type` and taxon tension the author reported is real, and I confirm the direction.

NCSU calls these organisms water molds in terms -- "They are more commonly referred to as water-molds
due to their ability to produce asexual, swimming spores in the presence of water" -- while the entry
is pinned `fungal`. The author was right not to touch `type` (it is what makes `improve_drainage`,
`soil_solarization` and `certified_clean_stock` reachable, and `uf_ifas` does say "fungal infection"),
and right to report it. Add to it that the ladder's **terminator is a *Phytophthora*-scoped
availability sentence being used to close a generically-named "Root and stem rot" umbrella** whose own
anchor names no genus. Consistent with adjudication C1 recording genuinely different taxa across the
five root-rot crops. One decision for the taxon pass, not five.

### R6. Source-key conventions: verified, all three claims hold.

I checked the author's `notes_to_orchestrator` claims against canonical rather than accepting them.
`water_spray`'s shipped `anchoring_urls` really is `{"ucanr_ext": pn7404, "ucanr_ext_spider_mites":
pn7405}`, so pointing `ucanr_ext` at pn7404 follows existing repo practice. **Zero** crop-level
entries in canonical cite pn7404 or pn7405 today (I walked every `anchoring_urls` on every entry).
`ucanr_ext_spider_mites`'s catalog `url` is exactly pn7405, so that key is an exact match, not a path
assertion. And `wsu_mint_rust`, `pubmed` and `udel_ext` are all absent from the 219-key catalog, so
every source the author declined to cite really was inadmissible.

### R7. Record gaps carried forward unchanged (reported by the record pass, still open).

UC IPM's oregano page lists five invertebrates -- I confirmed: **Aphids, Leafhoppers, Spider Mites,
Spittlebugs, Thrips** -- and **no diseases section at all**. Oregano's record carries two of the five.
Thrips is named by three sources (`uc_ipm`, `uf_ifas` "aphids, spider mites, and thrips", UDelaware)
and `ucanr_ext_thrips` is already catalog-admitted and unused, so a thrips entry remains the cheapest
addition on this crop. `psu_ext` adds "leaf miners, thrips, and cutworms". Correctly out of scope for
a correction pass; recorded so it does not fall off.
