# persimmon -- PLA-8 batch 26 INDEPENDENT source-truth review

Reviewer: independent of the authoring agent. Read 2026-09-04. Retrieval: every document below was
fetched first-party (raw HTML via python urllib, stripped to text, quoted from the saved text; TAMU
persimmons_2015.pdf by pypdf) EXCEPT `ucd_fruitnut` (403 first-party on both hosts; read via
`r.jina.ai` proxy, marked PROXY) and the UC ANR FNRIC "Persimmon Insect, Mite & Nematode Pests" page
(403 first-party on ucanr.edu AND fruitandnuteducation.ucanr.edu; `r.jina.ai` returns the "Access
denied / You are not authorized to access this page" shell; NOT READ). WebFetch's summarizer was used
only as a first pass and every quote below was re-checked against the raw text.

Documents read: HS1389 (Tables 3 and 4, rootstock and pruning body); UGA C784; Clemson HGIC 1357;
NC State "Persimmon Psyllid"; UC IPM pn7408, pn74174, pn74133; UC IPM home-and-landscape persimmon,
leaf-spot-diseases and flatheaded-borers pages; UAEX Plant Health Clinic "Persimmon Leaf Spot";
NCSU Plant Toolbox Diospyros kaki; UF IN1149; TAMU E-611 (pypdf); UCD FNRIC scion/rootstock (PROXY).

Grades: HOLDS / WRONG / UNSUPPORTED / SYNTHESIS / STYLE / FIT per BRIEF_review.md. 18 rungs, 55
field corrections, 11 refusal groups.

---

## Scale insects [pests] `scale-insects` -- 4 rungs, 6 corrections

**Rungs**

1. `garden_sanitation` -- **HOLDS.** pn7408: "You can prune off heavily infested twigs and branches,
   if they are limited to a few parts of small plants." HS1389 Table 3: "Snow-white patches on trunk
   and limbs, easily scraped off. Most visible when males emerge during warm weather." The note's
   condition ("only a few twigs or branches ... on a small tree") is pn7408's condition, stated as such.
2. `ant_exclusion` -- **WRONG (one clause); rest HOLDS.** HOLDS: pn7408 "Armored scales do not
   produce honeydew." / "Because ants attack and feed on scale parasites and predators, control ants if
   they are tending scales. To deny ants access to plant canopies, prune branches or weeds that provide
   a bridge between buildings or the ground and apply a sticky material (Tanglefoot) to trunks. Wrap
   the trunk with a collar of fabric tree wrap, heavy paper, or masking tape to avoid injury to bark".
   Tuliptree scale is a soft scale per pn7408 ("Soft scales include black scale, brown soft scale,
   Kuno scale, lecanium scales, and tuliptree scale"). **FIX F3** below on the diagnostic sentence.
3. `beneficial_predators` -- **HOLDS.** UGA C784 verbatim: "In unsprayed situations, scale are
   generally kept under control by natural parasites, predators and diseases. Spraying for other pests
   often releases scale from natural control." HS1389 "ladybird beetles and lacewings for biological
   control." pn7408: "Foliar sprays of broad-spectrum insecticides with residues that can persist for
   weeks are not recommended for scale control in landscapes and gardens."
4. `horticultural_oil` -- **HOLDS.** UGA "Dormant oil application shortly before bud swell should
   provide good control of scale." HS1389 "3% dormant oil applied before bud break, summer oil".
   pn7408: "To control most scales overwintering on deciduous woody plants, thoroughly spray the bark
   of terminal shoots with oil during winter." / "Horticultural oil is effective in spring or summer
   on deciduous plants when sprayed soon after most crawlers have emerged and most scales are in the
   young nymph stage." / "Do not apply oil or other insecticides when it is ... hot (over 90°F)" /
   "be sure plants are well irrigated before spraying". Sticky-tape check: pn7408 "During the spring
   before crawlers begin to emerge, tightly encircle each of several scale-infested twigs or branches
   with transparent tape that is sticky on both sides". PLA-457: pn7408 carries "do not apply oil
   within 3 weeks of an application of sulfur-containing compounds"; NEITHER note states it. Correct.
   Minor: "3%" in the seasoned note is a label rate carried from HS1389; true, but a rate figure is
   the label's business (STYLE, no fix required).

**Field corrections**

* `symptoms_seasoned` -- **HOLDS.** HS1389 symptom cell verbatim; pn7408 "Armored scales do not
  produce honeydew." / "Soft scales and certain other types feed on phloem sap and excrete abundant,
  sticky honeydew, which drips on plants and surfaces underneath and promotes the growth of blackish
  sooty mold." UGA "Persimmon scale and tuliptree scale are to be expected." Correction was NEEDED:
  the old prose stated honeydew/sooty mold/ants for an entry headlined by an armored scale.
* `symptoms_beginner` -- **HOLDS.** Same anchors. "tiny winged males" is a small embellishment of
  "when males emerge" (adult male scales are winged per pn7408's crawler/male sentence); harmless.
* `cause_seasoned` -- **HOLDS.** Live HS1389 row header reads "Scale (Figures 9, 10) primarily white
  peach scale (Pseudaulacaspis pentagona)"; the anchor quote 'Scale (Pseudaulacaspis pentagona)'
  is a truncation (see R11). "primarily" supports the umbrella.
* `cause_beginner` -- **HOLDS.**
* `prevention_seasoned` -- **HOLDS.** UGA bud-swell sentence; HS1389 warm-weather cue; pn7408 tape.
  NOTE: dropping "Keep the tree vigorous" as "no persimmon anchor" was not NEEDED: pn7408, an anchor
  this entry cites, says "Provide plants with good growing conditions and proper cultural care,
  especially appropriate irrigation, so they are more resistant to scale damage." The replacement is
  not worse, so no fix; recorded so the drop is not read as a finding against the old sentence.
* `prevention_beginner` -- **HOLDS.**

---

## Mealybugs [pests] `mealybugs` -- 4 rungs, 6 corrections

**Rungs**

1. `ant_exclusion` -- **HOLDS.** pn74174: "Also keep ants out of mealybug-infested areas and plants
   because ants protect mealybugs from their natural enemies." HS1389 psylla row: "Mealy bugs may also
   be present." / "May also need to control the ants that feed on the honeydew." Band-over-wrap and
   bridge pruning are pn7408's instruction (cited on scale; same catalog method).
2. `water_spray` -- **HOLDS.** pn74174: "If mealybugs are somewhat exposed, it may be possible to
   reduce populations on sturdy plants with a high-pressure or forcible spray of water. Repeat
   applications at several-day intervals may be necessary."
3. `beneficial_predators` -- **SYNTHESIS (widened).** HOLDS: pn74174 "Fortunately most species have
   natural enemies that keep their populations below damaging levels in outdoor systems such as
   landscapes and gardens." / "The mealybug destroyer lady beetle, Cryptolaemus montrouzieri, is the
   most important of these predators in many areas." / "Preserve naturally occurring biological
   control agents by avoiding use of broad-spectrum insecticides for any pests in the area." UGA
   "relatively free of serious insect problems." **FIX F5**: the seasoned note's "its fruit-tree note
   is that outside citrus mealybugs are rarely at damaging levels" widens pn74174's "Among fruit
   trees, citrus has the most problems, but mealybugs may sometimes be found on stone fruits or pome
   fruits, although rarely at damaging levels." The document scopes the claim to stone and pome
   fruits; persimmon is neither.
4. `insecticidal_soap` -- **SYNTHESIS (technique transplanted).** HOLDS: pn74174 "Insecticidal soaps,
   horticultural oil, or neem oil insecticides applied directly on mealybugs can provide some
   suppression, especially against younger nymphs that have less wax accumulation." **FIX F6**: the
   beginner note's "dab a cotton swab dipped in it into the tight spots" is pn74174's ISOPROPYL
   ALCOHOL houseplant method ("a 70% or less solution of isopropyl (rubbing) alcohol in water may be
   dabbed directly on mealybugs with a cotton swab"), not a soap instruction. Harmless but not what
   the document says.

**Field corrections**

* `symptoms_seasoned` -- **HOLDS.** pn74174: "Most adult mealybugs are wingless females with oval,
  segmented bodies covered with wax." / "in the crown of a plant, in branch crotches, on stems near
  soil, or between the stem and touching leaves" / "Signs of an infestation might include white,
  cottony egg masses on plants, wax-covered plants, sticky honeydew, black sooty mold growing on top
  of honeydew or ants feeding on honeydew." HS1389 "Mealy bugs may also be present." TAMU (pypdf):
  "Few insect pests attack persimmons. In some summers, caterpillars may defoliate persimmon trees,
  and cases of mealy bugs, thrips, mites, ants, and fruit flies have been reported." Calyx removal:
  RIGHT. The FNRIC page 403s first-party on both hosts and the proxy returns "Access denied" (today);
  IN1149 has no calyx or fruit sentence ("The longtailed mealybug has a relatively wide host range
  that includes ... persimmon" is its only persimmon mention); pn74174's harborage list has "between
  two touching fruits" but no calyx. No admissible LIVE page read states the calyx harborage. The
  search engine's rendering of the FNRIC page does carry "Small cracks under the calyx ... exude sap
  which appeared to attract mealybugs and ants", so the claim is LOCATED-UNREAD, exactly as filed.
* `symptoms_beginner` -- **HOLDS.**
* `cause_seasoned` -- **STYLE (unscoped absence + sourcing commentary in consumer copy). FIX F13.**
  "No persimmon document names the species; the one binomial tied to persimmon in extension
  literature is the longtailed mealybug" asserts absence across all extension literature from the
  documents read; the unread FNRIC page (per the search rendering) names Gill's mealybug, Ferrisia
  gilli, as "the most prominent pest in commercial persimmon production in California". Scope it to
  the guides read, and keep document-inventory language out of a cause field.
* `cause_beginner` -- **HOLDS.**
* `prevention_seasoned` -- **HOLDS.** pn74174 conservation sentence; HS1389 psylla/ant sentences.
* `prevention_beginner` -- **HOLDS.**

---

## Persimmon psyllid [pests] `persimmon-psyllid` -- 1 rung, 4 corrections

**Rung**

1. `beneficial_predators` -- **SYNTHESIS (scope widened); otherwise HOLDS.** HOLDS: UGA verbatim
   "Psyllid are often limited by natural parasites. Don't apply insecticides until after you have
   observed damage." NC State: "Horticultural oils suppress adult and immature persimmon psyllids
   without leaving a toxic residue that might harm beneficial insects and mites." / "the pyrethroids
   are harsh on beneficials" / "Minimize shearing or clipping of terminals during the growing season."
   / "Development from egg to adult takes only a few weeks in spring." HS1389: "Best to control very
   early; sprays less effective when leaves curl." **FIX F4**: NC State's decline sentence is scoped:
   "On native persimmon, these psyllids can be temporarily abundant; but their populations soon
   decline naturally, as they are attacked by their natural enemies, including parasitic wasps." The
   beginner note ("North Carolina says its numbers soon fall on their own as parasitic wasps and other
   enemies go to work") and the seasoned note drop "On native persimmon" and apply it to the reader's
   kaki. UGA's unscoped sentence carries the practical advice on its own; attribute the NC State
   sentence at its scope or lean on UGA alone. "first spring flush" as the oil timing is an inference
   from NC State ("Psyllids become abundant in spring when temperatures warm and host plants produce
   new, tender growth") plus HS1389's curl sentence: acceptable SYNTHESIS, no fix. The seasoned note's
   characterization of HS1389's cell as "a stance written for an orchard" is the author's reading of
   a Florida grower document ("Many pesticide options"); defensible, STYLE only.
   Refusal of every spray rung and of the record's "prune off ... rolled tips": RIGHT (NC State:
   "Minimize shearing or clipping of terminals during the growing season. Shearing stimulates new
   growth preferred by psyllids for feeding and egg laying.").

**Field corrections**

* `symptoms_seasoned` -- **UNSUPPORTED (live) on one sentence. FIX F10.** HOLDS: NC State "Infested
  leaves are often misshapen." / "Nymphs secrete white fluff and also cause terminals to twist and
  become galled." / "Nymphs are flattened and less active than adults" / "Psyllids also excrete sticky
  honeydew on which dark sooty molds may grow." HS1389 "Crinkled and deformed young leaves, stunted
  growth. White-colored nymphs found within distorted leaves and black-bodied adults on leaf
  surface." UGA "Infested leaves roll and curl up on themselves." NOT on any live document: "Damage
  is largely cosmetic on an established tree but can stunt the growth of a young one." HS1389 says
  "stunted growth" without an age split; the young-tree/established-tree split is the retired ENY-803
  ("Psylla infestations stunt the growth of shoots on young trees"). The author applied the
  retired-document ruling to refuse the borer's "girdled and killed" but carried this ENY-803-only
  sentence (it was in the old prose). Inconsistent; restate as HS1389 has it.
* `symptoms_beginner` -- same finding ("On an older tree the harm is mostly looks; it can slow down
  a young one.").
* `organic_treatment_seasoned` -- **HOLDS.** UGA, NC State and HS1389 sentences above.
* `organic_treatment_beginner` -- **HOLDS.**

---

## Persimmon borer [pests] `persimmon-borer` -- 1 rung, 8 corrections

**Rung**

1. `garden_sanitation` -- **FIT, with one UNSUPPORTED sentence. FIX F7.** What HOLDS: Clemson
   verbatim "It is important to monitor the persimmon borer. If borer damage is noted on the trunk or
   exposed roots, treatment may be required." UGA verbatim "Persimmon borer is a serious pest of
   native and oriental persimmons. It has been seen attacking oriental persimmons in Georgia, although
   it is known to infest both species in other states. Its larvae attack the lower trunk and tap
   roots. Where infestations occur, preventive insecticide treatments similar to those made for
   peachtree borer will be required." HS1389 "Gummy sap, frass, or sawdust coming from small holes in
   bark, pruning cuts, or trunk near soil line." / "March through June applications best to prevent
   larvae from entering tree. Limited direct control information; controls for peachtree borer may be
   effective (imidacloprid)." UC IPM flatheaded page confirms the wire sentence lives there and only
   there: "Larvae can sometimes be killed by probing tunnels with a sharp, stiff wire. This method is
   practical only in a small infestation on small trees." UNSUPPORTED: "Keep grass, weeds and mulch
   pulled back from the bottom of the trunk so you can see the bark where it meets the soil" -- no
   persimmon document says this; it is the note's only physical action and it exists to make a
   monitoring note fit a sanitation method. FIT: the rung's content is monitoring plus a description
   of a conventional program; `garden_sanitation` ("Clear away old, diseased, or pest-ridden plants
   and debris") carries none of it. The author flagged this shape for the orchestrator; agreed, it is
   the orchestrator's call. "Nothing put on later reaches a larva already inside" is carried by the
   brief's borer hold and by HS1389's "to prevent larvae from entering tree"; acceptable.
   Trunk treatment for a home tree: NEITHER UGA C784 nor Clemson names a material or a trunk-spray
   method (UGA: "preventive insecticide treatments similar to those made for peachtree borer";
   Clemson: "treatment may be required" and "Chemical control of diseases and insects on large trees is
   usually not feasible since adequate coverage of the foliage with a pesticide cannot be achieved").
   HS1389 names imidacloprid only. The pyrethroid/carbaryl refusal is RIGHT. The `borer_stem_surgery`
   refusal is RIGHT twice over: no document describes wire probing for Sannina, and the catalog
   method is a squash-vine slit-and-mound technique.

**Field corrections**

* `symptoms_seasoned` -- **SYNTHESIS (multi-species cell attributed to one organism). FIX F8.**
  HS1389's row header is "Tree borers (Figures 13, 14) (multiple species, including Sannina
  uroceriformis)" (the anchor quote 'Tree borers (Sannina uroceriformis and multiple species)' is
  not the live wording, see R11). The symptom cell, including "pruning cuts", is written for the
  group; UGA places the persimmon borer at "the lower trunk and tap roots". Attributing holes in
  pruning cuts to a root-collar clearwing narrows a group cell onto one organism. Scope it ("the
  signs Florida lists for its tree borers as a group ...") or drop "pruning cuts". UGA and Clemson
  sentences HOLD verbatim.
* `symptoms_beginner` -- same finding.
* `cause_seasoned` -- **HOLDS on UGA/HS1389; "a clearwing moth" is UNSUPPORTED on a live document
  (F15, minor).** No live document names the family; Sesiidae/"clearwing" is ENY-835/ENY-803 (retired)
  only. It is true and it is an identity, not advice; note it as evidence-only rather than fix, but
  it is the same class the author refused elsewhere.
* `cause_beginner` -- same; the flatheaded correction-out is RIGHT (UC IPM persimmon page lists
  "Flatheaded Borers" as a separate problem; its flatheaded page never mentions persimmon).
* `organic_treatment_seasoned` -- **HOLDS.** Honest: "No documented organic control ... The organic
  contribution is monitoring." Anchors verbatim.
* `organic_treatment_beginner` -- **FIT/STYLE. FIX F9.** "where the borer is active, to run a
  preventive insecticide treatment like the one used for peachtree borer from March through June"
  prescribes a synthetic program inside the ORGANIC treatment field; the seasoned version confines
  itself to monitoring and names the program as what the guides say. Match the seasoned framing.
* `prevention_seasoned` -- **HOLDS.** The "late summer" inspection month drop is RIGHT: no document
  gives one.
* `prevention_beginner` -- **HOLDS.**

---

## Anthracnose [diseases] `anthracnose` -- 1 rung, 8 corrections

**Rung**

1. `garden_sanitation` -- **STYLE (validator-shaped consumer copy). FIX F16 (decision, not text).**
   What HOLDS: HS1389 Table 4 "Leaf and fruit spots" control cell verbatim "Proactive fungicide
   sprays in early season, and cover sprays in summer in rotation." and symptoms "Gloeosporium:
   anthracnose "bitter rot" that affects fruit and shoots. Colletotrichum: affects ripening fruit."
   TAMU (pypdf) "Persimmons are largely free of serious diseases; however, crown gall and anthracnose
   have occasionally caused problems." As consumer copy the note is a sourcing memo: "Persimmon guides
   say little ... names no product ... No persimmon guide prescribes a cleanup step for it" and then
   offers fruit removal while saying it is "not a proven cure". A reader gets no instruction with a
   document behind it. The rung exists because the validator refuses an empty ladder. Refusal of
   chlorothalonil/copper/sulfur/mancozeb/biofungicide: RIGHT. UAEX's sentence is "Abound and Daconil
   Weather Stik are both labeled for control of Cercospora leaf spot in persimmon" -- Cercospora, not
   anthracnose -- and HS1389's shared row names no material; joining them is an inference across
   documents. `clemson_hgic` drop: RIGHT (Clemson's disease list is "Fungal leaf spot", "Twig
   dieback", "Powdery mildew"; anthracnose absent). Orchestrator: either accept the honest single rung
   rewritten instruction-first (remove rotting fruit; the guides give no other home step; Florida's
   answer is an unnamed protectant program) or rule on HS1389's shared row.

**Field corrections**

* `symptoms_seasoned` -- **STYLE. FIX F11a.** "It sits in the same row as persimmon's leaf-spot fungi
  and a bacterial look-alike" describes a source table's layout in consumer prose. The bacterial
  look-alike itself HOLDS (HS1389 "Pseudomonas: "bacterial blast" leaf spots and blackened stem and
  leaf petioles."). Correction NEEDED: the old "dark, sunken lesions ... warm, wet weather" had no
  persimmon anchor.
* `symptoms_beginner` -- **HOLDS.**
* `cause_seasoned` -- **STYLE. FIX F11b.** "The persimmon literature does not describe where they
  overwinter" is an unscoped absence claim (the memory rule: absence is document-scoped). Scope to
  the guides read. Organisms HOLD (HS1389 row).
* `cause_beginner` -- **HOLDS** ("the guides do not describe" is scoped).
* `organic_treatment_seasoned` -- **HOLDS.** Correction NEEDED: "Fungicides are rarely needed ... if
  sanitation is kept up" ran against HS1389's only management sentence.
* `organic_treatment_beginner` -- **HOLDS.**
* `prevention_seasoned` -- **HOLDS** (scoped: "in any extension document read").
* `prevention_beginner` -- **STYLE. FIX F11c.** "No persimmon variety is known to resist this rot"
  is unscoped; the seasoned version's scoping is the right form.

---

## Phytophthora root and crown rot [diseases] `phytophthora-root-rot` (RENAME) -- 2 rungs, 7 corrections

**Rungs**

1. `improve_drainage` -- **HOLDS; MISSING content (F1).** UC IPM persimmon page verbatim: "They are
   tolerant of many soil types but require good drainage." pn74133 verbatim: "If it is possible to
   modify site soils, improve soil drainage before planting." / "In poorly drained soils or in an
   area where you know Phytophthora is present, consider planting trees and shrubs on mounds. The
   mounds should be 8 to 10 inches high for annuals and up to 2 feet high with a gradual slope for
   trees and perennials." / "Avoid prolonged saturation of the soil or standing water around the base
   of trees or other susceptible plants. Without causing undue stress to the plant in question, allow
   the top few inches of soil to dry thoroughly between watering." / "If using a drip system, place
   the emitters as far as practical from the trunk while still allowing roots access to water." /
   "Never cover the root crown or graft union with soil or mulch." / "do not rely on pesticide
   applications alone to control Phytophthora root and crown rot diseases." TAMU: "It thrives in sands
   to bottomland as long as the soils do not stand in water." Every sentence in both notes is on the
   page. What is MISSING: see F1.
2. `resistant_rootstock` -- **HOLDS.** TAMU (pypdf) verbatim: "The Texas persimmon resists root rot;
   the common American persimmon is moderately susceptible, and the Oriental persimmon is highly
   susceptible. It is critical that all Oriental trees be grafted or budded onto the common persimmon
   because root rot is prevalent where the tree can grow." HS1389: "It provides a tolerance of wet
   soils, is cold hardy, can withstand drought conditions, and is compatible with most scion
   cultivars." UCD FNRIC (PROXY): "D. virginiana has a fibrous root system tolerant of both drought
   and excess moisture, however trees propagated on this rootstock are not uniform and are prone to
   suckering" / "D. lotus is tolerant to Armillaria, but susceptible to crown gall and Verticillium and
   does not tolerate poorly drained soils". Uncited strengthening the author missed: pn74133 itself
   says "Select certified nursery stock and resistant rootstocks or varieties when available." and
   "Losses to Phytophthora are minimized by providing good soil drainage, appropriate irrigation,
   managing plant stress and soil salinity, and selecting resistant plants or varieties." Caveat (R2):
   TAMU's "root rot" names no genus; the note attributes its ranking to a Phytophthora-named entry.
   The relative wording ("less susceptible ... not immune") is right.

**Field corrections**

* `name` -- **HOLDS.** UC IPM persimmon page lists "Phytophthora Root and Crown Rot (Diseases)" and,
  separately, "Armillaria Root Rot". UCD (PROXY): "D. kaki is resistant to Agrobacterium and
  Armillaria". Armillaria is kept out of every field: confirmed by grep.
* `symptoms_seasoned` -- **HOLDS.** pn74133: "Leaves may turn dull green, yellow, or in some cases
  red or purplish. Trees or plants often wilt and die rapidly with the first warm weather of the
  season." / "trees affected by Phytophthora develop darkened areas in the bark around the crown and
  upper roots." / "Gum or dark sap may ooze from the margins of the diseased trunk area" / "reddish
  brown zones, often separated from healthy tissue by a dark line, can be seen in the inner bark and
  outer layer of wood." Note: the old "sparse yellowing foliage" was in fact supported ("leaves ...
  appear drought stressed ... turn ... yellow"); the replacement is more specific, so no fix.
* `symptoms_beginner` -- **HOLDS.**
* `cause_seasoned` -- **HOLDS.** pn74133 "Although technically not true fungi (Phytophthora is more
  closely related to brown algae)". "(and related)" dropped: RIGHT. "water molds": RIGHT.
* `cause_beginner` -- **HOLDS.**
* `organic_treatment_seasoned` -- **WRONG `why`; omission. FIX F1.** The `why` says "'There is no
  cure once the crown is rotting' appears in no document read". pn74133, the anchor this correction
  cites, says: "A plant with a substantial Phytophthora infection rarely recovers. Trees with lesions
  larger than about one-quarter of the tree's circumference do not typically recover, even with ideal
  care. Trees with smaller lesions can sometimes be saved by removing soil from the base of the tree
  down to the top of the main roots and allowing the crown tissue to dry out." (also in its summary
  bullets: "Remove soil from around the base of the tree down to the top of the main roots and allow
  the crown tissue to dry out."). The old prose's "no cure once the crown is rotting" was closer to
  the document than the replacement's silence. The correction dropped a true, decision-relevant
  verdict AND the one documented salvage step. Both belong in this field and the salvage step belongs
  in the `improve_drainage` note (it is drying the crown, not cutting). The remainder of the field
  HOLDS verbatim.
* `organic_treatment_beginner` -- same finding ("'there is no fixing it' is unanchored" is false).

**Refusals on this entry.** "no cure once the crown is girdled" REFUSED: **WRONG** -- see F1; the
document says it in its own terms (a lesion more than a quarter of the circumference "do not
typically recover, even with ideal care"). `prune_out_infection` (crown excision) REFUSED "and the
pn74133 sentences read do not include it": the reason is **WRONG** (the page includes crown exposure
and drying), though the METHOD refusal is right: pn74133 prescribes exposing and drying the crown,
not cutting, so `prune_out_infection` is the wrong slug and the step belongs inside
`improve_drainage`. `garden_sanitation` (remove a dead tree) refusal: fine.

---

## Leaf spot [diseases] `persimmon-leaf-spot` (SPLIT 1/2) -- 3 rungs, 8 corrections

**Rungs**

1. `garden_sanitation` -- **HOLDS.** UAEX verbatim "Clean up diseased leaves and stems." UC IPM
   leaf-spot page verbatim "Remove fallen leaves and debris promptly." "dead twigs" for "diseased ...
   stems" is a small drift (STYLE, no fix).
2. `water_at_the_base` -- **HOLDS.** UC IPM leaf-spot page verbatim: "Many of the pathogens are
   favored by moisture, so avoid overhead sprinklers and irrigate early in the day so that the foliage
   dries more quickly."
3. `chlorothalonil` -- **HOLDS (one acceptable SYNTHESIS).** UAEX verbatim: "Control can be obtained
   by applying a fungicide cover spray during full bloom and again 3 to 4 weeks later. Abound and
   Daconil Weather Stik are both labeled for control of Cercospora leaf spot in persimmon." Daconil
   Weather Stik is a chlorothalonil formulation; the notes name the active only ("chlorothalonil"),
   never the product: confirmed by grep. Timing "at full bloom and again 3 to 4 weeks later": on the
   page. UC IPM leaf-spot page verbatim "Generally, fungicide treatment is not warranted." TAMU
   "Leaf spot can lead to early defoliation, but only severe cases warrant treatment." Bee handling:
   the catalog caution for chlorothalonil reads "do not apply it, or let it drift, onto anything in
   flower including weeds, except between sunset and midnight where the label allows"; the note states
   the bloom-time collision and defers to the label window. Right. The severe-case threshold ("a tree
   that dropped its leaves in late August in past years") is built from UAEX's "Severe infections can
   cause trees to defoliate in late August as the fruit begins to ripen" plus TAMU's "only severe
   cases": a constructed prior-season signal, not a stated threshold. Acceptable inference (the spray
   must precede symptoms); no fix. Caveat carried by the note itself: the labeled product is a
   commercial formulation, and "Check that the label lists persimmon" covers the home-product gap.

**Field corrections**

* `symptoms_seasoned` -- **HOLDS.** UAEX verbatim: "Symptoms begin as small necrotic spots that
  develop into angular lesions. Lesions may coalesce to form larger blotches on the leaf. Leaves turn
  yellow and fall from the tree prematurely. Severe infections can cause trees to defoliate in late
  August as the fruit begins to ripen. Problems related to defoliation include failure for fruit sugar
  to properly accumulate, and poor fruit ripening, biennial bearing tendencies with low overall
  yields, and increased vulnerability to freeze damage. Infection occurs at shoot expansion, leaf
  formation, and flowering in the spring." TAMU "Although not deadly to adult trees, several fungi
  cause leaf spot". Describes only its organisms: yes.
* `symptoms_beginner` -- **HOLDS.**
* `cause_seasoned` -- **STYLE (anchor misquote; "principal"). FIX F14a.** The anchor quote 'The
  causal agent is identified as Pseudocercospora diospyricola' is NOT on the page. Live: "A
  significant fungal pathogen that may affect yield is leaf spot caused by Pseudocercospora
  diospyricola." (the caption reads "Persimmon Leaf Spot- Pseudocercospora diospyricola"). "identifies
  the principal fungus" ranks it above the complex; UAEX calls it "A significant fungal pathogen".
  Substance HOLDS; fix the quote and soften "principal" to "the fungus Arkansas names".
* `cause_beginner` -- **HOLDS.**
* `organic_treatment_seasoned` -- **HOLDS.** All three documents verbatim.
* `organic_treatment_beginner` -- **HOLDS.**
* `prevention_seasoned` -- **HOLDS** (scoped "in the documents read").
* `prevention_beginner` -- **UNSUPPORTED. FIX F12.** "No persimmon variety is sold as resistant to
  leaf spot." is a claim about the nursery market that no document makes. Scope it as the seasoned
  field does.

---

## Botryosphaeria twig dieback [diseases] `botryosphaeria-twig-dieback` (SPLIT 2/2) -- 2 rungs, 8 corrections

**Rungs**

1. `airflow_spacing` -- **HOLDS.** HS1389 control cell verbatim: "There is no good chemical control.
   Pruning to wide crotch angles, pruning during dry days, disinfecting tools, maintaining good airflow
   in the canopy, reducing water or nutrient stress to trees, and a good fungicide program are
   recommended to help reduce the incidence of this fungus." HS1389 body: "Heavy pruning of persimmon
   is often not required or beneficial." / "Some of these dense areas will need to be thinned out
   occasionally in order to make sure light distribution within the canopy remains adequate." "room
   from its neighbors and from walls" is generic method text, not a persimmon sentence (STYLE, no
   fix).
2. `prune_out_infection` -- **UNSUPPORTED (core action) and misattributed. FIX F2.** HOLDS: dry-day
   pruning, tool disinfection, wide crotch angles (HS1389 cell above; TAMU "Remove limbs with narrow
   crotches because they create dead areas on the limbs; preserve limbs that grow off the leader at
   wide angles."); "no good chemical control"; Clemson's large-tree caveat; the symptom sentences
   (HS1389 "Discoloration of wood and deep, elongated bark scars may be present." and the Phomopsis /
   Verticillium / B. dothidea row "May cause small leaves and fruit, and terminal twigs that are
   leafless. May also cause wilting, shoot decline, and bark cracking at limb joints."). NOT in any
   persimmon document: "Take out ... any limb with deep, long bark scars or discolored wood, cutting
   well back into healthy wood so the part you cannot see comes off too" and the seasoned note's
   fourth item, "removal of cankered and dead wood with the cut placed back in sound tissue",
   presented as one of "the pruning practices" HS1389 carries. HS1389's pruning items are HOW to prune
   (angles, dry days, clean tools), not excision of cankers. Removing dead or diseased wood is
   anchorable only as general persimmon pruning (UC IPM persimmon page "In established trees, prune
   out suckers or dead wood."; Clemson "Remove dead, injured, or crossing branches."; TAMU "Remove
   crossover, shaded, diseased, and broken branches."); "well back into healthy wood" is the catalog's
   fire-blight text and VCE's generic Botryosphaeria advice, which the record pass found does not name
   persimmon and has no admissible key. Fix: keep the rung on HS1389's own practices plus dead/diseased
   wood removal attributed to the general pruning sentences, and drop or reframe the cut-back margin
   as the method's general practice rather than Florida's instruction. "Florida ties this disease to
   bark cracking at the limb joints and asks for wide crotch angles" fuses the two HS1389 rows;
   acceptable SYNTHESIS given TAMU's crotch sentence.
   The fungicide tension: HS1389's cell says both "There is no good chemical control" and "a good
   fungicide program are recommended to help reduce the incidence". The author's handling (no
   fungicide rung, because no material is named, "no good chemical control", and Clemson's coverage
   caveat; both sentences carried verbatim in `organic_treatment_*`) is RIGHT. A fungicide rung with
   no material would be padding; the prose does not hide the program.

**Field corrections**

* `symptoms_seasoned` -- **HOLDS.** Attribution is explicit ("In the symptoms Florida attributes to
  Botryosphaeria together with Phomopsis and Verticillium"). Clemson "Twig dieback" list item and
  "Chemical control of diseases and insects on large trees is usually not feasible since adequate
  coverage of the foliage with a pesticide cannot be achieved." verbatim.
* `symptoms_beginner` -- **SYNTHESIS (acceptable).** Folds the three-organism row's symptoms into the
  Botryosphaeria limb without the attribution the seasoned field gives. Since the limb is named for
  the dieback and B. dothidea is on that row, acceptable; note only.
* `cause_seasoned` -- **HOLDS.** HS1389 organisms verbatim; persimmon wilt row verbatim ("D.
  virginiana rootstock is susceptible to this disease; D. kaki and D. lotus are immune."). Describes
  only its organisms and names the two it is NOT: yes.
* `cause_beginner` -- **HOLDS.**
* `organic_treatment_seasoned` -- **UNSUPPORTED clause. FIX F2.** "Cankered limbs and dead twigs come
  out with the cut placed back in sound wood." -- no persimmon document. Rest HOLDS verbatim.
* `organic_treatment_beginner` -- **UNSUPPORTED clause. FIX F2.** "Cut out dead twigs and scarred,
  cankered limbs back into healthy wood". Rest HOLDS.
* `prevention_seasoned` -- **HOLDS.** HS1389 cell + "Heavy pruning" sentence + 8-to-12-year
  sentence; "names no resistant cultivar or rootstock" is scoped to Florida's guide.
* `prevention_beginner` -- **HOLDS.**

---

## FIX ITEMS (exact text, what is wrong, settling sentence)

**F1. Phytophthora `organic_treatment_seasoned` / `organic_treatment_beginner`, `improve_drainage` note, and the two refusals.**
Text: `why` = "'There is no cure once the crown is rotting' appears in no document read"; refusals =
"the brief's 'no cure once the crown is girdled' REFUSED as prose. No document read says it" and
"prune_out_infection (crown excision ...) REFUSED: ... the pn74133 sentences read do not include it."
Wrong: pn74133 (the correction's own anchor) carries the verdict and the salvage step; the
replacement dropped a true statement the old prose had and omits the one documented rescue.
Settles it: pn74133 "A plant with a substantial Phytophthora infection rarely recovers. Trees with
lesions larger than about one-quarter of the tree's circumference do not typically recover, even with
ideal care. Trees with smaller lesions can sometimes be saved by removing soil from the base of the
tree down to the top of the main roots and allowing the crown tissue to dry out."
Fix: restore the verdict in pn74133's terms in both organic_treatment fields; carry the crown-exposure
step inside `improve_drainage` (it is drying, not cutting; `prune_out_infection` stays refused).

**F2. Dieback `prune_out_infection` notes and `organic_treatment_seasoned` / `_beginner`.**
Text: "any limb with deep, long bark scars or discolored wood, cutting well back into healthy wood so
the part you cannot see comes off too"; "removal of cankered and dead wood with the cut placed back in
sound tissue" (listed as an HS1389 practice); "Cankered limbs and dead twigs come out with the cut
placed back in sound wood."; "Cut out dead twigs and scarred, cankered limbs back into healthy wood".
Wrong: no persimmon document prescribes canker excision or a cut-back margin; HS1389's items are
pruning practice. Settles it: HS1389 "Pruning to wide crotch angles, pruning during dry days,
disinfecting tools, maintaining good airflow in the canopy, reducing water or nutrient stress to
trees, and a good fungicide program are recommended" (no excision); UC IPM persimmon "In established
trees, prune out suckers or dead wood."; TAMU "Remove crossover, shaded, diseased, and broken
branches."

**F3. Scale `ant_exclusion` note_beginner.** Text: "a trail of ants on a persimmon means one of the
soft scales is there instead (Georgia expects tuliptree scale)". Wrong: on this crop ants are also
drawn by psyllid and mealybug honeydew, so an ant trail is not a soft-scale diagnosis. Settles it:
HS1389 psylla row "May also need to control the ants that feed on the honeydew."; NC State "Psyllids
also excrete sticky honeydew"; pn74174 "ants feeding on honeydew". Fix: "means a honeydew producer is
there: a soft scale, mealybugs, or the psyllid".

**F4. Psyllid `beneficial_predators` note_beginner and note_seasoned.** Text: "North Carolina says its
numbers soon fall on their own as parasitic wasps and other enemies go to work" / "NC State describes
populations that are temporarily abundant and then decline". Wrong: scope dropped. Settles it: NC State
"On native persimmon, these psyllids can be temporarily abundant; but their populations soon decline
naturally". Fix: keep the scope, or carry the claim on UGA's "Psyllid are often limited by natural
parasites." alone.

**F5. Mealybug `beneficial_predators` note_seasoned.** Text: "its fruit-tree note is that outside
citrus mealybugs are rarely at damaging levels". Wrong: widened. Settles it: pn74174 "mealybugs may
sometimes be found on stone fruits or pome fruits, although rarely at damaging levels."

**F6. Mealybug `insecticidal_soap` note_beginner.** Text: "or dab a cotton swab dipped in it into the
tight spots". Wrong: the swab is pn74174's alcohol method for houseplants. Settles it: pn74174 "a 70%
or less solution of isopropyl (rubbing) alcohol in water may be dabbed directly on mealybugs with a
cotton swab". Fix: drop the swab clause; keep "spray insecticidal soap straight onto them".

**F7. Borer `garden_sanitation` note_beginner.** Text: "Keep grass, weeds and mulch pulled back from
the bottom of the trunk so you can see the bark where it meets the soil". Wrong: no document; the
rung is monitoring on a sanitation method (FIT). Settles it: Clemson "It is important to monitor the
persimmon borer. If borer damage is noted on the trunk or exposed roots, treatment may be required."
(nothing about clearing the base). Orchestrator decides the ladder shape; at minimum drop the clause.

**F8. Borer `symptoms_seasoned` / `symptoms_beginner`.** Text: "Gummy sap, frass or sawdust coming from
small holes in the bark, from pruning cuts, or on the trunk near the soil line, where the larvae work
the lower trunk and tap roots." Wrong: a group cell attributed to one organism. Settles it: HS1389 row
header "Tree borers (Figures 13, 14) (multiple species, including Sannina uroceriformis)"; UGA "Its
larvae attack the lower trunk and tap roots." Fix: attribute the sign list to Florida's tree borers as
a group, or keep only the soil-line sign for this borer.

**F9. Borer `organic_treatment_beginner`.** Text: "where the borer is active, to run a preventive
insecticide treatment like the one used for peachtree borer from March through June". Wrong: a
synthetic program prescribed inside the organic field; the seasoned field frames it as what the guides
say. Settles it: UGA "preventive insecticide treatments similar to those made for peachtree borer will
be required." (report it, do not prescribe it here).

**F10. Psyllid `symptoms_seasoned` / `symptoms_beginner`.** Text: "Damage is largely cosmetic on an
established tree but can stunt the growth of a young one." / "On an older tree the harm is mostly
looks; it can slow down a young one." Wrong: no live anchor; the split is retired ENY-803's. Settles
it: HS1389 "Crinkled and deformed young leaves, stunted growth." Fix: "can stunt growth" without the
age split, per the author's own retired-document rule.

**F11. Anthracnose STYLE trio.** (a) `symptoms_seasoned` "It sits in the same row as persimmon's
leaf-spot fungi" -- table commentary in consumer prose; (b) `cause_seasoned` "The persimmon
literature does not describe" -- unscoped absence; (c) `prevention_beginner` "No persimmon variety is
known to resist this rot" -- unscoped absence. Settles it: the seasoned prevention field's own form,
"in any extension document read".

**F12. Leaf spot `prevention_beginner`.** Text: "No persimmon variety is sold as resistant to leaf
spot." Wrong: a market claim no document makes. Fix: "none of the guides names a resistant variety".

**F13. Mealybug `cause_seasoned`.** Text: "No persimmon document names the species; the one binomial
tied to persimmon in extension literature is the longtailed mealybug". Wrong: unscoped absence and
document inventory in consumer copy; the unread FNRIC page names Ferrisia gilli on persimmon per the
search rendering. Fix: "the guides read name only the longtailed mealybug".

**F14. Anchor misquotes (three).** (a) UAEX 'The causal agent is identified as Pseudocercospora
diospyricola' -> live "A significant fungal pathogen that may affect yield is leaf spot caused by
Pseudocercospora diospyricola."; (b) HS1389 'Tree borers (Sannina uroceriformis and multiple species)'
-> live "Tree borers (Figures 13, 14) (multiple species, including Sannina uroceriformis)"; (c) HS1389
'Scale (Pseudaulacaspis pentagona)' -> live "Scale (Figures 9, 10) primarily white peach scale
(Pseudaulacaspis pentagona)". These are the record report's quotes carried forward; if `anchor` text
reaches the verification log it should be verbatim.

**F15 (minor, note).** Borer `cause_*` "a clearwing moth": true, Sesiidae, but live-unanchored
(ENY-835/ENY-803 only). Keep or mark evidence-only; consistency with the author's own rule.

**F16 (decision).** Anthracnose single `garden_sanitation` rung is validator-shaped: its note tells
the reader no document prescribes it. Orchestrator/Trevor: accept an honest rung rewritten
instruction-first, or rule on HS1389's shared "Leaf and fruit spots" program (which names no
material, so no catalog method carries it).

---

## Checks the task asked for, in order

1. SPLIT limbs: every field graded above. Leaf spot describes only leaf-spot organisms (plus the
   bacterial look-alike HS1389 puts in the same row, labeled as such). Dieback describes
   Botryosphaeria and, explicitly attributed, the Phomopsis/Verticillium/B. dothidea row; it names
   persimmon wilt and leaf spot as what it is NOT. Dieback's fungicide tension: handled RIGHT.
2. Leaf-spot `chlorothalonil`: UAEX sentence confirmed verbatim; timing "during full bloom and again
   3 to 4 weeks later" confirmed; active ingredient only, no product name in any consumer string.
3. RENAME: "(and related)" gone; "water molds" in both cause fields; Armillaria absent from every
   field (grep). `resistant_rootstock` and `improve_drainage` HOLD against HS1389, UCD (PROXY) and
   pn74133. The "no cure" refusal was WRONG (F1).
4. Borer: one organism by name; flatheaded clause corrected out (RIGHT); single monitoring-led rung
   is FIT-weak with one unanchored clause (F7); `borer_stem_surgery` refusal RIGHT; neither UGA C784
   nor Clemson names a trunk treatment or material for a home tree.
5. Anthracnose: refusal RIGHT; rung is STYLE-weak validator copy (F16); `clemson_hgic` drop RIGHT.
6. Scale: honeydew sentence scoped to soft scales per pn7408 (RIGHT); white peach scale per HS1389
   "primarily white peach scale (Pseudaulacaspis pentagona)" (RIGHT). One WRONG diagnostic (F3).
7. Mealybugs: calyx claims correctly OUT; no admissible live page read states them (FNRIC 403 on
   every route today; IN1149 and pn74174 carry no calyx sentence).
8. Psyllid: single rung on UGA's sentence, confirmed verbatim; clip-the-tips refusal RIGHT (NC State
   "Minimize shearing or clipping of terminals during the growing season."). Scope defect F4.
9. PLA-457: scan of all 91 consumer strings: no sulfur mention at all; the only interval is UAEX's
   fungicide re-spray "3 to 4 weeks later" (not an oil/sulfur spacing). The hold note names pn7408's
   3-week figure, confirmed on the page: "do not apply oil within 3 weeks of an application of
   sulfur-containing compounds, such as wettable sulfur." No em dashes; °F rendered; no stray
   capital "Plant".

---

## SUMMARY

**Rungs (18):** HOLDS 11 (scale garden_sanitation, beneficial_predators, horticultural_oil; mealybug
ant_exclusion, water_spray; phytophthora improve_drainage, resistant_rootstock; leaf spot
garden_sanitation, water_at_the_base, chlorothalonil; dieback airflow_spacing) -- WRONG 1 (scale
ant_exclusion, one diagnostic clause) -- UNSUPPORTED 1 (dieback prune_out_infection, core action) --
SYNTHESIS 3 (mealybug beneficial_predators, mealybug insecticidal_soap, psyllid beneficial_predators)
-- FIT 1 (borer garden_sanitation) -- STYLE 1 (anthracnose garden_sanitation).

**Field corrections (55):** HOLDS 39 -- WRONG-why/omission 2 (phytophthora organic_treatment x2) --
UNSUPPORTED 5 (dieback organic_treatment x2; psyllid symptoms x2; leaf-spot prevention_beginner) --
SYNTHESIS 3 (borer symptoms x2; dieback symptoms_beginner, acceptable) -- STYLE/FIT 6 (mealybug
cause_seasoned; borer organic_treatment_beginner; anthracnose symptoms_seasoned, cause_seasoned,
prevention_beginner; leaf-spot cause_seasoned anchor misquote).

**Refusals:** 10 groups RIGHT; 1 WRONG (phytophthora "no cure" / crown-exposure, F1). Retired-document
ruling applied inconsistently (F10, F15).

**FIX items: 16** (F1-F16), of which F1, F2, F3 change what a reader is told; F4-F10 and F12-F13 are
scope or wording; F14 is anchor text; F15 a note; F16 a decision.

**Single most important finding:** the Phytophthora entry's two refusals rest on an incomplete read
of pn74133, the page the entry anchors. The author wrote "the pn74133 sentences read do not include
it", and the page includes it: "A plant with a substantial Phytophthora infection rarely recovers.
Trees with lesions larger than about one-quarter of the tree's circumference do not typically
recover, even with ideal care. Trees with smaller lesions can sometimes be saved by removing soil from
the base of the tree down to the top of the main roots and allowing the crown tissue to dry out." The
correction replaced a roughly-right sentence with silence and dropped the only documented rescue.
This is the batch-25 failure shape (authored from the report's excerpt, not the page), on a rung
that otherwise holds sentence for sentence.

---

## RECORD-LEVEL FINDINGS (filed, not fixed now)

R1. **HS1389's borer row is a group row.** "Tree borers (multiple species, including Sannina
uroceriformis)" with one symptom cell and one control cell. The entry is pinned to Sannina by name;
the record now attributes a group symptom list and a group control window to it. Flatheaded borers
(UC IPM persimmon page lists them; ENY-803 couples them to Botryosphaeria scars) remain an
UNCOVERED problem, as the author filed. Ambrosia beetles (UGA) and Armillaria (UC IPM list; UCD
"D. kaki is resistant to ... Armillaria") are further uncovered problems.

R2. **TAMU's "root rot" is genus-less.** The Phytophthora entry inherits TAMU's susceptibility ranking
("Texas persimmon resists root rot; ... Oriental persimmon is highly susceptible") under a
Phytophthora name. pn74133's own "Select certified nursery stock and resistant rootstocks or
varieties when available." and HS1389's "tolerance of wet soils" carry the rootstock rung on
Phytophthora-shaped evidence; the record should note that TAMU never names the genus.

R3. **`type: fungal` on an oomycete** (author noted; pn74133 "technically not true fungi"). The
roster id already carries it; a gate-type question, not a persimmon one.

R4. **Retired-document ruling applied unevenly.** "girdled and killed" refused (ENY-835 only) while
"clearwing moth" (borer) and "stunts a young tree / cosmetic on an established tree" (psyllid) were
kept on the same ENY-835/ENY-803-only basis. Pick one rule.

R5. **Proxy-only anchor.** `ucd_fruitnut` scion/rootstock page 403s first-party (both hosts, both
user agents) and reads only through `r.jina.ai`; anchored at the live URL per the brief's proxy
ruling. Its three rootstock sentences are confirmed on the proxy text.

R6. **UC ANR FNRIC persimmon pest pages are unreadable on every route** (403 direct on ucanr.edu and
fruitandnuteducation.ucanr.edu; proxy returns the "Access denied" shell). The search engine's
rendering attributes to that page both the calyx-crack sentence and "Gills mealybugs (Ferrisia gilli)
is the most prominent pest in commercial persimmon production in California". If the page ever
opens, the mealybug entry's species (currently longtailed only, via IN1149's host list) and the
calyx harborage should be revisited; the page is commercial-leaning.

R7. **Anthracnose ladder is a validator artifact.** The schema's one-rung minimum produced a rung whose
consumer note is a sourcing memo. Same device as pawpaw's peduncle borer. A ruling on "honest empty
ladder vs. honest minimal rung" would settle both (memory: `[]` passed every gate on an earlier
crop, so the minimum is convention, not gate).

R8. **Psyllid severity/scope.** No live document says the damage is cosmetic on established trees;
HS1389 says "stunted growth" flat. Severity low is supported by UGA/NC State's do-not-treat framing,
not by a cosmetic claim.

R9. **Dieback limb folds a three-organism HS1389 row** (Phomopsis, Verticillium albo-atrum, B.
dothidea) into the Botryosphaeria limb's symptoms. Attributed in the seasoned field, not in the
beginner. Verticillium is a wilt, a different disease; if a Verticillium entry is ever minted, the
"small leaves and fruit ... wilting, shoot decline" sentence belongs to that row, not to
Botryosphaeria alone.

R10. **The leaf-spot chlorothalonil labeling is product-specific.** UAEX's sentence labels "Abound and
Daconil Weather Stik", commercial formulations. Whether a home chlorothalonil label lists persimmon
is not established by any document; the rung's "Check that the label lists persimmon" is doing
real work and must not be edited out.

R11. **Anchor quotes carried from the record report are not all verbatim** (F14). The record pass
quoted three row headers/sentences in paraphrase; the authored `anchor` fields inherited them. If
`anchor` text is written anywhere durable, re-quote from the page.

R12. **UAEX key.** The Plant Health Clinic note is anchored under the portal key `uada_ext`
(catalog: parent portal entry); `uada_ext_fruit_trees` is a different page and was correctly not
used. Fine as filed; noted so a later pass does not "repoint" it.
