# PLA-8 BATCH 25 -- THE HERBS: handoff

**Written 2026-09-04.** lavender, lemongrass, mint, oregano, rosemary, sage, thyme.
Verify before acting: `shasum -a 256 crops_data_final.json` against `LATEST.txt`, then `git log -1`
and `git status -sb`.

---

## 1. What this batch is, and why it is not shaped like batches 21-24

Every previous PLA-8 batch only ADDED `id`, `type` and `control_ladder` to problem entries that
already existed under names that did not change. **This one reshapes the arrays.** On Trevor's
rulings of 2026-09-04 it renames three entries, splits four bundles into nine, deletes one bundle
half, and retires two entries outright. **36 canonical problems become 38.**

It also carries its record corrections IN the same promote rather than in a preceding round, which
batch 24 did separately. That was the right call there and the wrong shape here: splitting mint's
powdery-mildew/anthracnose bundle requires writing new prose for both limbs whatever else happens,
so a separate correction round would have meant authoring the same sentences twice. The price is
`check_field_corrections_declared`: **246 declared corrections, each carrying its own reason and its
own anchoring sentence**, and a `verify_post` that refuses any prose leaf that moved without a
declaration.

| | count |
|---|---|
| crops | 7 |
| canonical problems -> target problems | 36 -> 38 |
| retired | 2 (declared, never inferred from absence) |
| renamed | 3 |
| split rows | 7 (4 bundles -> 9 limbs) |
| rungs | 141 |
| declared field corrections | 246 |
| source keys, all catalog-admitted | 130 |
| authoring refusals filed | 44 |
| unreachable claims filed | 48 |

## 2. The §4f ruling, which turned out to have two answers

PLA-448 §4f asked whether a bare display name like "Rust" is an umbrella by intent or an organism
nobody pinned. **It is not one question.** The two instances in this batch resolve opposite ways, and
a mechanical "pin every bare generic" rule would have been wrong half the time:

* **oregano's "Rust" is ONE UNPINNED ORGANISM.** *Puccinia menthae*, anchorable at T1 in two sources
  already in oregano's own vocabulary (`psu_ext`: "Oregano can be susceptible to fungal diseases such
  as mint rust and root rot"; `rhs`: "The fungal disease mint rust can affect oregano"). Renamed to
  **"Mint rust"**, which is what every source calls it. The binomial tied to *Origanum* is
  JOURNAL-ONLY and is deliberately NOT written.
* **lavender's "Leaf spot" is a GENUINE UMBRELLA.** US extension names exactly one organism on
  *Lavandula* (*Septoria lavandulae*), in a bulk pathogen list with no symptoms, distribution or
  management, while NC State's own text is itself bare. Pinning it would invent precision the
  literature does not have. Kept as an umbrella and took ZERO corrections.

**`mint-rust` and `oregano-rust` are correctly two ids**, registered in `problem_id_registry.json`.
The reason is epidemiological: WSU documents host-specialized races within *P. menthae* ("One type
infects Native spearmint but not peppermint"). The direct mint-to-oregano cross-inoculation evidence
is **JOURNAL-ONLY** (APS 403s under every fetch path available) and the registry entry says so
explicitly rather than leaning on it.

Renaming oregano's entry also had a mechanical payoff: it REMOVED three would-be collisions, because
`oregano-rust` no longer shares the bare display name "Rust" with `bee-balm-rust`, `chives-rust` and
`sunflower-rust`.

## 3. The collision guard, wired in where PLA-449 said to put it

`tools/staging/pla8_batch25_herbs/pin_and_check.py` builds a TARGET-STATE scratch and runs the
PLA-449 guard against POST-APPLY data at id-pinning time, before fan-out.

**Its pass condition is a DIFFERENCE, not a clean report**, and that distinction is the whole design.
A whole-roster `--strict` run can never go clean for this batch, because batch 25 JOINS ids that
already carry known duplicate pairs: mint joins `cutworms` (9 -> 10 crops), `flea-beetles` (34 -> 35)
and `anthracnose` (14 -> 15); sage joins `slugs-and-snails` (11 -> 12); three crops join `aphids`
(59 -> 63). Those are PLA-448 §4a's eight duplicates, whose merge is §7's fast-follow. Registering
them to quiet the gate is the one thing `problem_id_registry.json` forbids.

So the guard runs on canonical AND on the scratch and compares id-pair sets:

    pairs on canonical: 34   pairs post-apply: 37
    INTRODUCED by this batch: 3, all registered
    INHERITED (this batch only joins them): 34

Three registry entries were added, each reasoned on the taxon or the scope:
`carrot-leaf-blight`/`lemongrass-leaf-blight` (Apiaceae *Alternaria*+*Cercospora* vs Poaceae
*Curvularia*; the shared normalized name is a parenthetical-deletion artifact),
`leafhoppers`/`sage-leafhoppers` (cilantro's beet-leafhopper VECTOR entry vs sage's
Lamiaceae-specialist *Eupteryx* that vector nothing), and `mint-rust`/`oregano-rust`.

**Verified live in both directions.** Planting `leafhopper` against the live `leafhoppers` flips a
row to UNREGISTERED and exits 1; restoring gives exit 0 with the pin table byte-identical.

## 4. The five-crop root-rot decision

Shared display names hid different organisms, so the rule applied was: **reuse the existing
problem-class umbrella whose display name matches, UNLESS the crop's taxon is resolved AND narrower.**

| crop | entry | id | why |
|---|---|---|---|
| sage | Root and stem rot | `root-and-stem-rots` | unresolved umbrella, name matches |
| oregano | Root and stem rot | `root-and-stem-rots` | unresolved umbrella, name matches |
| rosemary | Root and crown rot | `crown-and-root-rot` | taxon contested; parsley's own record defines that id as exactly this umbrella ("Pythium, Phytophthora, Rhizoctonia") |
| thyme | Root and crown rot | `crown-and-root-rot` | VCE's one line giving *Pythium* is not enough to mint a one-crop join key |
| lavender | Phytophthora root and crown rot | `lavender-root-crown-rot` | THE EXCEPTION: taxon resolved and narrower (*P. nicotianae*, dedicated WSU source) and the display name already names the genus |

**The PNW page that blocked this was eventually read** (§7).

## 5. What the seven-reviewer source-truth pass found

The pass ran on the authored content BEFORE the promote, one reviewer per crop, ~210 graded items.
The coarse rules held; the defects were finer, which is the same shape batch 24 found.

1. **A correction that made a field LESS TRUE.** oregano's powdery-mildew `cause_*` added "hot" as a
   driver, with UC IPM 7493 cited in the same field two sentences later saying "Moderate temperatures
   of 60° to 80°F and shady conditions are most favorable". The only instance in the batch.
2. **A live inversion of a source.** mint's verticillium told growers to keep mint out of beds that
   grew potatoes; UC IPM says "Strains more specialized on other crops (e.g., potatoes) usually do
   not attack mint", and its potato sentence is about what not to plant AFTER mint. Mint's own
   `crop_rotation` rung had it right, so the record contradicted itself. It survived because an
   earlier fix corrected the LIST and never the DIRECTION.
3. **A fabricated attribution still live** on mint's verticillium ("The Connecticut Experiment
   Station..."), eight weeks after mint's cert log recorded striking that credit from the NEIGHBORING
   entries. Second instance in this batch of a correction applied to one field and left in others;
   lemongrass's `geraniol` is the other, also after a cert log asserted a clean full-file scan.
4. **UNVERIFIED written up as ABSENT.** Four of mint's `why` strings asserted absences their own
   cited documents refute. Those are different findings and a `why` that converts one into the other
   is what a later pass trusts.
5. **A safety figure understated**, §6.

## 6. `control_methods.horticultural_oil` understates a phytotoxicity interval -- NOT FIXED, Trevor's call

    control_methods.horticultural_oil: "Do not apply sulfur within 2 weeks of an oil spray"
    its anchor, UC IPM PN 7405:        "don't apply sulfur within 30 days of an oil spray"

`control_methods.sulfur` also says two weeks and **is faithful**, to PN 7406, which really does say
"do not apply it within 2 weeks of an oil spray". **UC IPM's own two Pest Notes disagree**, and the
catalog is faithful to one and not the other.

The batch handles this per entry, by each entry's own anchor, so oregano ships **two different
intervals on one crop on purpose** with a loud note that a harmonizing sweep would introduce an
error. Scope of the underlying defect: `horticultural_oil` is on **76 rungs across 42 crops**,
`sulfur` on 28 across 25, and **15 already-shipped rung notes** state the two-week figure in prose
(apple, apricot, cherry-sour, cherry-sweet, grape-tomato, plum, strawberry). A crop carrying both
methods can show a reader two intervals on one page. Untouched here: it is roster-wide content.

## 7. Two documents that were finally read, and one that still has not been

* **PNW Plant Disease Handbook, rosemary root rot.** 403 to every direct path. The rosemary reviewer
  retrieved it through the `r.jina.ai` text proxy, corroborated by an independent search snippet:
  "*Pythium*, *Berkeleyomyces* sp. ... and *Rhizoctonia* are among the organisms found." **No
  Phytophthora.** This makes the genus-agnostic pin correct rather than merely cautious, and the
  2026-07-06 cert-log line ("Phytophthora-only") needs a `[CORRECTION]` append.
  **STANDING CAVEAT: that is a proxy retrieval plus a snippet, not a first-party read.** Strong
  enough to keep an id decision and to strip a genus from prose, both moves toward saying LESS. NOT
  strong enough to assert those genera in consumer copy, and nothing does.
* **UC IPM PN 7401** (whiteflies) was read to unblock lavender -- see §8.
* **APS cross-inoculation literature** remains unreadable (403 under every path). The specialization
  claim stays JOURNAL-ONLY and unwritten.

## 8. Process findings worth carrying to batch 26

* **A summary handed to an authoring agent becomes that agent's whole universe for the claim.**
  Lavender correctly refused to write a whitefly ladder with no document behind it. The orchestrator
  read PN 7401 and sent a curated bullet list. The one rung authored from that list turned out to be
  the one rung contradicting the document, because the list omitted "Hand removal of leaves or plants
  heavily infested ... may reduce populations to levels that natural enemies can contain". Sending
  the agent TO the document produced a ladder of 8 rungs from 6, and three further divergences the
  list had hidden. **Where a document must reach an agent, send the agent to the document.**
* **Legal is not anchored, and gate-legal is not method-correct.** Three separate instances:
  sage refused a `sulfur` rung the type correction had made legal, because no document recommends it
  for mites on sage; mint and rosemary independently refused `prune_out_infection` on the METHOD's
  own text ("a spotted leaf picked off ... that is garden sanitation and not this") after the
  orchestrator told them the GATE permitted it; oregano refused to cite `uc_ipm_pn7493` because that
  key's own `citable_for` scopes it away from culinary crops.
* **A TITLE READS AS A SENTENCE ONCE IT IS INSIDE A RECORD REPORT.** rosemary's aphid siting claim
  was anchored to `ncsu_ext`'s "Aphids found on flowers and foliage." -- which is not a source
  sentence but the TITLE of a linked factsheet, under the parent publication "Insect and Related
  Pests of Flowers and Foliage **Plants**", i.e. a class of ornamental crops and not plant parts. The
  quote only parses as a claim about siting if you assume the wrong reading, and the report is where
  that assumption became invisible. **Structural, not local:** NCSU Toolbox `Insects:` and
  `Diseases:` rows are lists of factsheet titles, so any crop anchored on one is exposed. It was also
  the last surviving fragment of the UGA bundle the aphid/whitefly split existed to eliminate,
  retro-anchored after the split.
* **A QUOTED FRAGMENT CARRYING AN ELLIPSIS MUST BE RE-READ AT SOURCE before any number inside it is
  called published.** rosemary's root-rot replant interval came through the record as "avoid planting
  them or other susceptible plants ... in the same soil for at least 1 or 2 seasons". The scoping
  lived exactly where the ellipsis was: the bullet is annuals-only ("If tomatoes, bedding plants, or
  other annuals have been affected"), and it was applied to a woody shrub that stands in the same
  ground for a decade. No document gives a replant interval for a woody perennial.
* **A DECLARED "RESOLVED" IS WHAT A LATER PASS TRUSTS WITHOUT RE-CHECKING.** rosemary's notes
  declared an item resolved when only half of it was: the humidify ADVICE was removed and its PREMISE
  ("dry indoor air over winter is a classic trigger") left standing one field away. The reviewer
  caught it because it read the fields, not the summary. Applies to every RESOLVED claim in this
  batch's notes.
* **Ask how often the dataset already does this, before treating something as a defect.** The move
  that resolved three separate questions: mixed severities on a shared id (43 of 118 multi-crop ids
  already do it, 36%), house phrasing vs a lift ("go easy on the fertilizer." has 13 shipped donors),
  and whether unsourced records were normal (104 laddered problems shipped unsourced).
* **A note that describes the SET of steps goes false the moment the set changes.** Hit twice, once
  in a rung note and once in a handoff note. The handoff instance is more dangerous because a later
  pass reads it as current truth.

## 9. Guard changes made during the batch, all measured

* **`check_no_shipped_prose_echo` was refusing correct input.** It flagged "go easy on the
  fertilizer.", which appears on **13 shipped rungs**; 75 short strings are already duplicated inside
  canonical. Now exempts sentences with 2+ shipped donors (760 of 10491 distinct, 7.2%), keeping
  9731 single-donor sentences caught. Mint's real single-donor lift is still refused.
* **`check_no_multi_donor_recombination` is NEW**, and closes a defect the ratio cannot see: a note
  assembled from two donors resembles neither closely enough to cross 0.70. Lemongrass's real
  instance scored under threshold against both. Measured before building: "shares a rare 6-gram"
  flagged 108, mostly ordinary English; the final rule flags 1.
* **Its first brake was wrong and an agent caught it by READING.** Set-nesting was defeated by one
  stock sentence with a single word changed between copies ("at this step" vs "at this point"), which
  shifts the window set so neither nests. Replaced with POSITIONAL OVERLAP. Verified both ways.
* **`LADDER_VOCAB` was refusing "The same care applies to a division handed over the fence"** because
  it matched `applies[_ ]to` with an optional space. Narrowed to the underscore forms.
* **The suite's own tier table was inverted.** `biological` ranks BEFORE `soft_chemical`. Caught by
  importing `control_ladder_gate`'s table instead of retyping it; it would have mis-ordered every
  ladder in the batch.
