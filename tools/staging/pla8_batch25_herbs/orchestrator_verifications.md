# Batch 25 -- verifications the ORCHESTRATOR made directly

Not taken from a reviewer's report. Each of these was fetched and read here, because it is either
counterintuitive, consumer-facing, or a claim about our own shipped data. Reviewer reports are
credited where they surfaced the lead.

Canonical throughout: `a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`.

---

## V1. UC IPM's oregano page names NO diseases (verified 2026-09-04)

`https://ipm.ucanr.edu/home-and-landscape/oregano/` lists Invertebrates (Aphids, Leafhoppers,
Spider Mites, Spittlebugs, Thrips), Environmental Disorders and Weeds. **No Diseases section.**

Consequence: oregano's three disease records have no UC IPM basis, and correctly never claimed one.
Also: Leafhoppers, Spittlebugs and Thrips are named here and absent from oregano's record.

## V2. UC IPM Pest Note 7406 does recommend overhead sprinkling (verified 2026-09-04)

`https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html`, "Pest Notes: Powdery Mildew on Vegetables":

> "Wash spores off infected plants with overhead sprinkling. To prevent other disease problems, do
> this midmorning so moisture dries rapidly."
> "Overhead sprinkling may help reduce powdery mildew because spores are washed off the plant.
> However, overhead sprinklers are not usually recommended as a control method in vegetables because
> their use may contribute to other pest problems."

Host list: artichoke, beans, beets, carrot, cucumber, eggplant, lettuce, melons, parsnips, peas,
peppers, pumpkins, radicchio, radishes, squash, tomatillo, tomatoes, turnips. **No herb.**

## V3. UC IPM's mint page names powdery mildew but NOT anthracnose (verified 2026-09-04)

`https://ipm.ucanr.edu/home-and-landscape/mint/` -- Invertebrates: Aphids, Leafhoppers, Spider Mites,
Thrips. Plant Diseases: "Powdery Mildew on Vegetables" (the 7406 link). No anthracnose, no rust, no
verticillium.

**The precise defect in mint's "Powdery mildew and anthracnose (leaf spot)" bundle** is therefore
narrower than "ships wrong advice": UC IPM does attach powdery mildew to mint at the host-index
level, so the anchor is legitimate for identification. What fails is the BUNDLE -- one prevention
string ("water at the base rather than overhead", "keep the foliage dry") cannot serve two diseases
whose sources disagree about leaf wetness, and the anthracnose half has no uc_ipm support at all.
Splitting resolves it. (Lead: mint reviewer.)

## V4. Oregano's only shipped disease anchor is find-and-replace boilerplate (verified 2026-09-04)

Oregano's `Root and stem rot` cites exactly one document:
`https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/`
-- the UF/IFAS Pasco County "Spice Up Your Life" series the thyme reviewer identified as a
find-and-replace template across herbs. Read here in full. It carries:

* Pests: Aphids, Spider Mites, **Thrips**.
* Diseases: **Powdery Mildew** ("good air circulation around plants and avoid overhead watering";
  "fungicidal sprays containing sulfur or copper") and **Root Rot** ("occurs when oregano plants are
  exposed to excessive moisture"; "Improve soil drainage and avoid overwatering"; "Remove affected
  plants promptly").

**THREE record defects trace to this one anchor:**

1. **"stem rot" is unanchored.** The document says root rot and never says stem rot. Our entry is
   named "Root and stem rot".
2. **"not cold" is an authoring addition.** Our `cause_seasoned` reads "Waterlogged ground and wet
   winters, not cold, are the underlying cause". The document attributes root rot solely to excess
   moisture. **CORRECTED 2026-09-04 (oregano reviewer): I wrote here that the document "says nothing
   about cold or winter either way." That is WRONG and the reviewer verified it twice.** The page
   does discuss cold, just not as a cause of root rot: "temperatures in the low 40s are too cold for
   oregano" and "Oregano is a winter-hardy herb". The conclusion is unaffected and in fact
   strengthened, since the document discussing cold elsewhere and NOT attributing root rot to it
   makes the record's negation more clearly an authoring addition. But an absence check I asserted
   was false, which is the defect class this file exists to catch in others. Worse, the negation is refuted for this
   plant group -- UMD: "Excessively wet, **cold** soil can cause Mediterranean herbs such as
   rosemary, thyme, and lavenders to die over the winter." (Lead: thyme reviewer.)
   **This same "not cold" construction appears on thyme's root rot, so it is a template twin
   propagating a wrong claim across crops -- exactly the failure mode the twins guard exists for.**
3. **The document's real disease content is misfiled.** Powdery mildew is what this anchor actually
   publishes for oregano, and our record buries it inside an entry named "Botrytis and humid-weather
   foliar disease" -- leading with the one organism no source attaches to oregano. (Lead: oregano
   reviewer, corroborated here.)

## V5. PNW handbook rosemary root rot: NOT READ (403), treated as unverified

`https://pnwhandbooks.org/plantdisease/host-disease/rosemary-rosmarinus-officinalis-root-rot`
returned **403** to WebFetch here, as it did for the rosemary reviewer on three URL forms. A web
search returns index text attributing **Pythium, *Berkeleyomyces* sp. (formerly *Thielaviopsis
basicola*), and Rhizoctonia** to rosemary root rot, with **no Phytophthora** -- which would partly
reopen the 2026-07-06 cert-log "Phytophthora-only" ruling for rosemary.

**This is a search-index summary, not a read document, and it is NOT citable.** Recorded as a lead
only. A cached search verdict standing in for a read is the exact shape of a false presence. Needs a
genuine read (a second user-agent, or the print view) before anything is authored on it.

## V6. Source catalog admits no journal-class entries (verified 2026-09-04)

219 entries, 210 T1 / 9 T2, every one `university_extension`, `government`, `.edu` or
`horticultural_authority`. **Zero journal entries.** So APS *Plant Disease* / *Plant Health Progress*
cross-inoculation evidence -- the best evidence that *Puccinia menthae* races do not move between
mint and oregano -- is currently INADMISSIBLE as an anchor. Both rust reviewers correctly graded that
claim JOURNAL-ONLY rather than laundering it through a paraphrase.

`rhs` IS admitted (T1, `horticultural_authority`) but its catalog entry itself warns:
"UK-centric climate guidance requires translation to USDA hardiness zones for North American
application." Its pesticide-availability statements are UK product law and must not reach US
consumer copy.

---

## V7. Authoring-pass items requiring an ORCHESTRATOR decision (collected as agents report)

### V7.1 `uc_ipm_pn7493` -- a catalog key the batch wants but does not have (sage agent, 2026-09-04)

`anchoring_urls` holds ONE url per source key, and this batch's powdery-mildew corrections rest on
TWO UC IPM documents: Pest Note **7406** (Powdery Mildew on Vegetables) and Pub **7493** (the
floriculture/ornamentals one). The sage agent pinned 7406 and therefore did NOT write three claims
that only 7493 carries:

* the dormant-season "prune out small infestations", which would justify an additional
  `garden_sanitation` rung and would restore the record's existing "remove affected leaves" advice;
* the 95°F suppression fact;
* **the only host list read anywhere in this batch that names salvia** -- i.e. the strongest
  available anchor for "sage gets powdery mildew" as opposed to "vegetables get powdery mildew".

It flagged these rather than laundering them under the 7406 URL, which is the correct behaviour.

Precedent for the addition is strong: the catalog already carries many pathed UC/UF/WSU sub-keys
(`uf_ifas_hs403`, `wsu_em051e`, `uf_ifas_hs132`, ...) for exactly this reason.

**DECISION OWED.** Four crops in this batch carry powdery mildew (mint, oregano, rosemary, sage), so
if more than one agent reports the same gap, one catalog addition unblocks all of them. NOTE a
`source_catalog` addition is a TOP-LEVEL key change, which `promote_pla8_batch25.verify_post`
refuses by design -- it would have to land as its own small catalog commit before the batch, in the
shape of the existing catalog r-rounds.

### V7.2 sage's display name is wider than sage's evidence (sage agent, 2026-09-04)

Both sage-scoped documents say **slugs**; neither says snails. The pinned id `slugs-and-snails`
stays (it is the 11-crop majority id and the join key is not the place to express this), but the
corrected prose is slug-only. Recorded so the mismatch is deliberate rather than an oversight.

### V7.3 A refusal worth keeping (sage agent, 2026-09-04)

The agent REFUSED a `sulfur` rung on spider mites. My brief told it that correcting `type` from
`insect` to `mite` makes `sulfur` and `even_watering` legal -- which is true, and which I measured.
It is not the same as anchored: no document in sage's report recommends sulfur for mites on sage
(Pest Note 7405's treatment sentence names soap or oil only), and sulfur's own catalog cautions
forbid use above 90°F or on drought-stressed plants, which is exactly the condition that produces
sage mite outbreaks. **A legal rung is not an anchored rung.** The brief created the pressure; the
agent was right to refuse it. Watch the other mite ladders for the same pressure.

### V7.4 MY OWN BRIEF WAS WRONG ABOUT `prune_out_infection` (lemongrass agent, verified here)

The authoring brief told all seven agents that `prune_out_infection` "does NOT reach `fungal_foliar`"
and to route rust and leaf-spot sanitation through `garden_sanitation` instead. **VERIFIED HERE: that
is false at the level the gate checks.**

    prune_out_infection.applies_to = {bacterial, disease_general}
    TYPE_TARGETS['fungal']         = {fungal_foliar, fungal_soilborne, disease_general}
    intersection                   = {disease_general}  -> LEGAL

The claim was true of the applies_to VALUE `fungal_foliar` and false of the problem TYPE `fungal`,
which is the only thing `control_ladder_gate` tests. Confusing a value with a type is exactly the
class of error the "import a gate's table, never retype it" rule exists to prevent, and this time
the error was in PROSE handed to a fan-out rather than in code.

**Consequence to chase in the review pass:** seven agents were steered away from a legal and often
more apt method on every fungal ladder in the batch (rust on oregano and lemongrass, leaf spot on
lavender, powdery mildew on four crops, the rots on five). The lemongrass agent followed the brief
anyway and said so, judging `garden_sanitation` the better method on its own merits, which is fine.
The others were not given the choice. **Reviewers must be told the method is available and asked
whether any ladder should carry it.**

THIRD tooling error of mine that the fan-out caught, after the inverted tier order (biological ranks
BEFORE soft_chemical) and the validator that read pinned `type`/`severity` without comparing them.
All three were found by agents exercising the tooling harder than its author did.

### V7.5 `geraniol` survived a strike that claimed to be complete (lemongrass agent)

The batch-2 cert log records striking `geraniol` from lemongrass's `pests[0]` on 2026-07-06 and
asserts a clean full-file scan. It is still live in
`companions.good_beginner_seasoned[0].provenance.reason`. Both companions `provenance.reason` fields
also assert the repellency is "a real mechanism" / "documented", which is precisely what UC MG
Solano refutes. Provenance is where a LATER pass goes looking for the warrant, so a false warrant
there is worse than in consumer prose. This is the second independent instance in this batch of a
correction applied to one field and left live in others, after mint's CAES attribution.

### V7.6 The surviving byte-identical prose is ACCEPTED, deliberately (measured 2026-09-04)

The oregano agent found by MEASUREMENT, not reading, that root rot's `organic_treatment_beginner`
was byte-identical across oregano, thyme, rosemary and lavender, and de-twinned its own. The record
pass had found nothing false in that text, so reading alone would never have surfaced it.

Measured on the full post-apply state, **two** cross-crop byte-identical prose fields remain, both on
the spittlebug entries, and **zero** batch prose is byte-identical to any non-batch crop:

* `organic_treatment_beginner` x3 -- lavender, rosemary, sage:
  "If the froth bothers you, spray it off with a hose. You usually do not need to do anything else."
* `organic_treatment_seasoned` x2 -- lavender, rosemary:
  "Knock them off with a strong spray of water if you find them unsightly. No treatment is needed for
  plant health in most cases."

**Accepted, and the reasoning matters.** These are INHERITED canonical fields that no agent declared
a correction to, so this batch did not create the twin; it merely did not dissolve it. More
importantly the text is true, anchored and identical *because the situation is identical*: all three
crops carry the same organism (*Philaenus spumarius*), and UMN publishes both halves of exactly this
advice ("Spray them with a strong blast of water to dislodge nymphs from the plants"; managing
spittlebugs is "generally unnecessary"). Forcing three agents to word the same anchored advice
differently would be manufacturing difference to satisfy a similarity metric, which is a worse defect
than the twin: it makes the prose less accurate in order to make a number look better.

The twins guard in the promote covers RUNG NOTES, where independent authoring is the whole point and
identical text means someone did not write from their own record. It deliberately does not reach
inherited record prose. Recorded here so a later pass sees a decision rather than an oversight, and
so that if these fields are ever CORRECTED they are corrected on all three crops together.

### V7.7 I HANDED AN AGENT A CURATED SUMMARY AND THE CURATION DROPPED THE LOAD-BEARING SENTENCE

The lavender authoring agent correctly refused to write a whitefly ladder with no document behind it.
I read UC IPM Pest Note 7401 and sent it the management program as a verbatim bullet list. It
authored six rungs from that list, and its reviewer then found that **the one rung authored from the
document I supplied is the one rung that contradicts it.**

The rung says sanitation is "worth very little once the insects are spread through the canopy." 7401
says:

> "Hand removal of leaves or plants **heavily infested** with the nonmobile nymphal and pupal stages
> **may reduce populations to levels that natural enemies can contain**."

My bullet list carried 7401's "Prune out isolated infested leaves when you first detect them" and
did NOT carry that sentence. So the agent had the early-detection half and not the
heavy-infestation half, and wrote the reasonable inference from what it was given. The dropped
sentence is also the bridge to the entry's own `beneficial_predators` rung, so two rungs in the
finished ladder now disagree with each other.

**The lesson is not "read the document", which I did. It is that a summary handed to an authoring
agent becomes that agent's entire universe for the claim, and any sentence the summary omits is a
sentence the agent cannot know to want.** A record report is written to be exhaustive over a claim;
an unblocking message written in a hurry is not, and it does not announce which of the two it is.
Where a document must reach an agent, send the agent to the document.

### V7.8 THE RECOMBINATION GUARD'S FIRST BRAKE WAS WRONG, AND AN AGENT CAUGHT IT BY READING

The guard's original brake exempted a donor pair when one donor's shared-gram SET nested inside the
other's. The lemongrass authoring agent ran the guard over all 47 of its own strings, found a second
refusal I had not reported, and instead of rewriting on command it READ the runs:

  three shipped notes write "the other choice at this **step**"
  english-cucumber writes  "the other choice at this **point**"

One stock sentence, one word changed between copies. The variant shifts the six-word window set by
one element, so neither set nests inside the other, and a single house phrase read as two
independent donors. A guard refusing correct input is a defect class no mutation test finds, because
the branch fires exactly as written.

**Fixed by changing the brake from set nesting to POSITIONAL OVERLAP**: the two donors' runs are
located in the batch note's own word indices, and a pair is exempt when those spans overlap. Several
shipped notes carrying one stock sentence all match the SAME span; a real assembly takes its opening
from one donor and its closing from another. Verified in both directions on the real data: the
pre-fix lemongrass note is still refused (words 8-18 from edamame, disjoint from nasturtium's span)
and the "other choice at this step" phrasing now passes.


### V7.9 THE PNW ROSEMARY PAGE WAS READ, AND IT SETTLES THE ROT PIN (rosemary reviewer, 2026-09-04)

V5 recorded this page as NOT READ after 403s on every path available here. The rosemary reviewer
retrieved it through the `r.jina.ai` text proxy, corroborated by an independent search-index extended
snippet. Verbatim Cause section:

> "Several root rotting organisms have been detected in rosemary root rot samples coming to the OSU
> Plant Clinic. **Pythium, Berkeleyomyces sp. (formerly Thielaviopsis basicola), and Rhizoctonia**
> are among the organisms found."

**No Phytophthora.** Two consequences:

1. **The genus-agnostic pin was not merely cautious, it was CORRECT.** A Phytophthora-named
   `cause_seasoned` would have been WRONG, and the rosemary authoring agent's decision to go one step
   past the pin and strip the genus from the prose was right for a reason nobody could confirm at the
   time. The catalog's "water molds **and fungi**" phrasing turns out to be load-bearing: two of the
   three organisms are true fungi, not water molds.
2. **The 2026-07-06 cert-log line needs an append.** It records rosemary's root/crown rot as
   "correctly Phytophthora-only... Pythium already dropped". Per
   `docs/verification_log_ref_convention.md` that is an APPEND-ONLY historical record, so it takes a
   `[CORRECTION 2026-09-04: ...]` line and the original prose stays byte-for-byte.

**STANDING CAVEAT, stated because it matters:** the reviewer never touched the origin directly. This
is a proxy retrieval plus a search-index snippet agreeing with each other, which is two consistent
retrievals and not a first-party read. It is strong enough to keep the id decision and to strip a
genus from prose, both of which are moves toward saying LESS. It is not strong enough to assert
Pythium, Berkeleyomyces or Rhizoctonia in consumer copy, and nothing in the batch does.

### V7.10 THE BATCH MINTED ITS OWN CROSS-CROP TWIN DEFECT, AND IT IS A SAFETY FIGURE

Five rung notes across THREE crops (lemongrass, oregano, sage) tell the reader to keep sulfur and
horticultural oil "two weeks" apart. **VERIFIED HERE against UC IPM Pest Note 7405 (Spider Mites):**

> "Don't use sulfur if temperatures exceed 90°F, and don't apply sulfur **within 30 days** of an oil
> spray."
> "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F."

Two weeks is less than half the published interval, on a combination the document warns about because
it injures foliage. Found independently by the sage and oregano reviewers; the lemongrass instance
was found here by scanning the batch for the same figure once two reviewers had named it.

**This is the batch creating a twin rather than inheriting one.** Seven agents authored in isolation
from a shared brief, and three converged on the same wrong number, which is the failure mode
`check_no_intra_batch_twins` cannot see: the notes are not byte-identical, only wrong in the same
way. A twins guard keyed on text similarity will never catch a shared misreading of a source. The
defense that did work was two independent reviewers reading the same document.
