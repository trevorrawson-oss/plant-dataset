# Batch 26 -- verifications the ORCHESTRATOR made directly

Not taken from a reviewer's report. Each of these was fetched and read here because it is either
counterintuitive, consumer-facing, or a claim about our own shipped data. Reviewer reports are
credited where they surfaced the lead.

Canonical throughout: `ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144`.

---

## V1. UC IPM ag Soft Scales: honeydew and sooty mold "has not been observed on pomegranates" (verified 2026-09-04)

`https://ipm.ucanr.edu/agriculture/pomegranate/soft-scales/` (WebFetch, first-party):
> "The harmful honeydew and sooty mold associated with these soft scales in citrus and olives has not
> been observed on pomegranates."
> "The most important economic damage from all four soft scales is the light-colored spot left when a
> scale is removed from a fruit, where the scale has blocked sunlight and prevented fruit coloring."
> "Heavy honeydew and sooty mold in pomegranates is typically caused by aphids, whiteflies, or cherry
> leafhoppers."

Consequence: the split scale limb's symptoms prose must NOT carry the bundle's honeydew/sooty-mold
sentence; that sentence belongs to the mealybug/aphid/whitefly entries. Lead: pomegranate reviewer.

## V2. UF/IFAS HS1389: Botryosphaeria is the limiting factor (verified 2026-09-04)

`https://ask.ifas.ufl.edu/publication/HS1389` (WebFetch, first-party):
> "This disease is the limiting factor for growing persimmons in Florida and the Deep South."
> "Often this fungus limits the lifetime of Japanese persimmons to about 8 to 12 years (or less)."
> "There is no good chemical control."
> "Gloeosporium: anthracnose 'bitter rot' that affects fruit and shoots."

Consequence: the twig-dieback limb of persimmon's bundle is its own entry at HIGH severity, with a
ladder that stops at sanitation/pruning. HS1389 does NOT mention Phytophthora (the root-rot genus
rests on UC IPM's persimmon page, V6). Lead: persimmon reviewer.

## V3. UGA C997: Alternaria absent in Georgia; a California disease (verified 2026-09-04)

`https://fieldreport.caes.uga.edu/publications/C997/pomegranate-production/` (WebFetch, first-party):
> "One of the most interesting findings was that Alternaria spp. was not present."
> "Even though Alternaria spp. was not present at the Ponder Farm orchard that does not mean that it
> is not present in other production regions in the state."
> "Fruit harvested from the Ponder Farm Pomegranate Orchard displayed symptoms caused by the infection
> of Cercospora punicae and Botryosphaeria spp."
> "Other organisms that were also present on the fruit (but did not cause any symptoms) included:
> Aspergillus, Cladosporium, Colletotrichum, Epicoccum, Penicillium, Pestalotia and Phomopsis spp."

Consequence: the black-heart climate framing ("humid regions expect this to be limiting") is
backwards and is corrected; the Cercospora entry's "related fungi such as Colletotrichum and
Botryosphaeria" clause is corrected out (C997 lists Colletotrichum as symptomless and
Botryosphaeria as a separate disease). Lead: pomegranate reviewer.

## V4. OSU popcorn disease: hybrids are in the SUSCEPTIBLE class (verified 2026-09-04, PROXY)

`https://extension.okstate.edu/programs/digital-diagnostics/plant-diseases/popcorn-disease-of-mulberry.html`
still 403s first-party (as at the 2026-07-02 cert); read through the r.jina.ai text proxy:
> "White mulberry varieties and hybrids are more susceptible to popcorn disease."
> "Remove and bury the infected fruit on the trees and any ground debris as it appears during the
> growing season."

Consequence: the record's "favor red mulberry or a more resistant hybrid" steers growers toward the
susceptible class and is corrected. STANDING CAVEAT: a proxy retrieval, not a first-party read;
enough to retract an over-claim (a move toward saying less). Lead: mulberry reviewer.

## V5. MU AF1021: peduncle borer pupates in twigs; the pruning sentence is about the WEBWORM (verified 2026-09-04, PROXY)

`.../agroforestry/af1021.pdf` (r.jina.ai proxy of the PDF):
> "The first generation of adult moths emerges from twigs in April and May, often when trees are
> blooming."
> "Larvae initially feed on the anthers, then move through the floral tissue, and eventually bore
> into stems where they continue to consume tissue until they pupate and emerge from the twigs."

The fetch found NO control statement for the borer; the pawpaw reviewer confirms in context that
MU's "infested parts of the tree can be pruned and removed from the site" is about the Asimina
webworm. Consequence: the record's flower-raking prescription is corrected out, and no sourced
action remains for this borer; the author follows the no-control policy in the authoring brief.

## V6. UC IPM persimmon page: Phytophthora root and crown rot listed separately from Armillaria (verified 2026-09-04)

`https://ipm.ucanr.edu/home-and-landscape/persimmon/` (WebFetch, first-party). Diseases, verbatim
titles: "Armillaria Root Rot", "Botrytis Blight, or Gray Mold", "Leaf Spot Diseases", "Phytophthora
Root and Crown Rot (Diseases)", "Wood Decay Fungi in Landscape Trees". Invertebrates include
"Flatheaded Borers", "Mealybugs", "Scales". NO twig dieback anywhere on the page.

Consequence: persimmon's root rot joins `phytophthora-root-rot` under the UC IPM title; the old
bundle's dieback half was anchored to a page that never mentions it (V2 gives the real anchor).
Also confirms flatheaded borers are a SEPARATE UC IPM problem from the persimmon borer, so the
borer entry's prose drops them rather than bundling them.

## V7. UC IPM ag Leaffooted Bug: the 21°F figure is published (verified 2026-09-04)

`https://ipm.ucanr.edu/agriculture/pomegranate/leaffooted-bug/` (WebFetch, first-party):
> "Cold temperatures near 21°F (-6°C) will kill some exposed bugs"
> "it requires a low of approximately 21ºF for at least six hours to kill about 50% of the exposed
> population"
> "By late November, newly developed adults leave pomegranate and form overwintering aggregations on
> more sheltered plants such as citrus, juniper, cypress, and palm trees"

The home Pest Note (PN 74168) says only "Cold winters kill many adults". Consequence: the figure in
pomegranate's leaf-footed bug sanitation note is warranted by the entry's own biology anchor; the
promote's temperature guard refused it until the sentence was attached to a declared correction's
anchor, which is the guard doing its job (a figure in a note with no quoted sentence behind it).
