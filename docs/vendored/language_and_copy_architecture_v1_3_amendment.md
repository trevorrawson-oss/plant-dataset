# Language and Copy Architecture v1.3 AMENDMENT -- the register differentiation standard

**Status:** Amendment to v1.2. **Closes §10.1**, which deliberately deferred this rule pending a read-derived rate.
**Date:** 2026-08-20
**Home:** `~/Documents/plant-project/05-methodology/current/`
**Adds:** §9.1 (the differentiation test), §9.2 (contradictory pairs), §9.3 (gloss-avoidance), §9.4 (four schema shapes wearing one suffix), §9.5 (the measured rate).
**Evidence:** PLA-256 rounds 1 and 2 -- 55 pairs drawn systematically at canonical `be8a6d1e` (15 + 30 from render status A, 10 from C), read 2026-08-20, plus a full type census over all 20,168 pairs.

---

## Why this can now be written

v1.2 §10.1 held this rule open for a stated reason: the cosmetic-pair rate was unknown by two orders of magnitude. String similarity said 0.4%; a 25-pair blind read said 40%. Writing a threshold against a number nobody trusted would have meant the arcs authoring against a guess.

**Round 1 settles the direction.** Of 15 pairs read: **4 clearly cosmetic, 5 borderline, 6 clearly substantive.** That is 27% strict, 60% inclusive -- and the blind read's 40% sits inside the range.

**The 0.4% figure is not close and should not be cited again.** The reason is now specific and worth keeping: a similarity metric scores a thesaurus pass as *substantively different*, because every word changed. A reader scores it as *identical*, because nothing was learned. The metric was measuring the wrong property competently.

**What round 1 does NOT establish** is a precise rate. n=15 is a class-building batch, not an estimate. The rate is a range, and §9.5 states what would narrow it.

---

## §9.1 The differentiation test

§9 already sets the **actionability floor**: if one register carries an actionable instruction, diagnostic clue, or remedy, the other must too. That is the minimum.

This section sets the **differentiation requirement**: what makes a pair worth having at all.

### The test

> **What does the seasoned reader now know, or now be able to do, that the beginner reader does not?**
>
> **If the only answer is "the technical word for it," the pair is cosmetic.**

### The core distinction

Vocabulary substitution is **necessary but not sufficient**.

The registers exist so a first-season grower is not blocked by terminology. Substituting "white coating on the leaves" for "powdery mildew" is the register doing its job at the vocabulary layer. **But if vocabulary is the only thing that differs, the seasoned reader gained nothing by being seasoned.** Two fields were authored, two fields are maintained, and one reader is served.

That is the whole defect. It is not that cosmetic pairs are wrong -- both halves are usually accurate and well written. It is that they cost double and return single.

### Legitimate differences -- any ONE makes a pair substantive

**1. Mechanism.** The seasoned half says *why*.

> viola: beginner "keep the young plants evenly watered." seasoned adds **"shallow-rooted"** and **"to protect the crown"** -- the reason the rule exists.

**2. Named entities.** Pathogens, cultivars, equipment, standards -- things a reader can look up, buy, or search.

> parsley: beginner "soil fungi." seasoned **"Pythium, Phytophthora, Rhizoctonia."**
> sunflower-sprouts: beginner "a full tray." seasoned **"a well-sown 1020 tray."**

**3. Consequence.** What happens downstream that the other half does not mention.

> slicing-cucumber: seasoned adds that early defoliation **exposes fruit to sunscald.**

**4. An additional action.** Something to *do* that the other half omits.

> broccoli-microgreens: seasoned adds **"vented"** container and **"harvest only what you will use soon."**
> lemon: seasoned adds what IS permissible -- low, shallow-rooted plantings outside the drip line.

**5. Precision that changes a decision.** "5 to 7 days" versus "about a week" counts **only if** the difference would change what someone does. Usually it does not.

### NOT differences -- these alone make a pair cosmetic

**1. Synonym substitution.**

> mulberry, the purest case in the batch: *Plant→Site, paths→walkways, driveways→drives, yard→space, pick→choose, variety→cultivar.* Six substitutions, zero information.

**2. Register-lexicon substitution.** The subtle one, because it *looks* like register work.

> celery: "a clear cover" → **"a humidity dome."** Same object.
> english-cucumber: "got white and powdery" → **"turned white and powdery."**

**The clearest case in the dataset is not prose at all.** Six melon `soil.*_texture` pairs differ by a synonym *inside a controlled vocabulary* -- "light sandy soil" against "loamy sand," "wet, poorly drained clay" against "poorly drained clay." In prose one can argue a synonym carries register. In a controlled vocabulary the value **is** the term, so there is nothing for a register to do. See §9.4 B2.

**3. Syntactic reordering.** Same clauses, different order.

> apricot: beginner "too mild to give even low-chill apricots the cold they need" → seasoned "cannot bank enough winter chill for even low-chill apricots." Three clauses, same order, every one reworded, nothing added.

**4. Tone or hedging changes.**

> celery: "Be patient, since they are slow" → "Do not let the surface dry during the long germination window."

### Applying it

A pair passes if it carries **at least one** legitimate difference. That is a low bar on purpose -- the goal is not elaborate seasoned copy, it is that the seasoned reader learns something.

**When authoring a pair and the seasoned half will not take a legitimate difference, that is a signal**, not a failure. Either the field does not need a register pair (see §9.4), or the seasoned content has not been researched yet and the pair should wait rather than be padded.

---

## §9.2 Contradictory pairs

**A defect class distinct from cosmetic and from inversion, and worse than both.**

The two registers state the same fact differently -- not in wording, in substance.

> **lemon** `companions.note`: beginner says keep mulch **"a hand's width back from the trunk."** Seasoned says **"at least a foot."** Same risk (Phytophthora foot rot), same tree, roughly 4 inches against 12.
>
> **collards** `tips_by_stage.germination[1].text`: beginner says sow **"in late summer"** for a fall crop. Seasoned says **"mid to late summer."**

Two of 15 pairs. Neither was found by any instrument, and neither would be: both halves are individually plausible, well written, and gate-clean.

**The rule:** where both registers state a quantity, date, threshold, or distance, **they must agree.** A register may omit a number. It may round one. It may not give a different one.

**When authoring:** if the seasoned half carries a figure and the beginner half carries a plain-language version of it, check that the plain-language version is actually the same figure. "A hand's width" is not a rounding of "a foot."

---

## §9.3 Gloss-avoidance

§4 already requires that a technical term carrying real precision be **taught rather than substituted away**. This names the failure mode.

> **beet** `start_method.notes`: the beginner half describes a multigerm seedball in full -- *"each beet seed is really a little dried fruit holding several seeds"* -- and **never names it.** It does name the exception: *"Some kinds, sold as monogerm."*

So a beginner holding a packet labeled **multigerm** cannot connect it to the advice they just read, while the same field taught them the word for the case they do not have.

**The test:** if a beginner will encounter this term on a seed packet, a product label, a nursery tag, or the first page of a search, **name it and gloss it.** Substituting it away leaves the reader unable to recognize the thing when they meet it.

**This is not a pair defect.** It is a defect in the beginner half alone, and it can occur in a pair that is otherwise substantive. Check it independently.

---

## §9.4 Four schema shapes wearing one suffix

The dataset holds 84 non-string pairs plus one all-identical string family. **They are four unrelated schema problems, not one**, and a rule written for any of them gets the other two wrong.

> ⚠ **This section was rewritten 2026-08-20 after a fuller census.** The first draft ruled all 17 bool pairs as "a boolean that should never have been suffixed" and recommended dropping the suffixes. **That ruling was wrong and would have deleted 88 explanatory paragraphs.** The corrected reading is B1 below. Recorded rather than silently replaced, because the error is instructive: a type census over one type is not a census over one key.

### B1 -- `start_method.hardening_off` is one key doing two jobs

The key carries **120 pairs in three shapes**:

| beginner | seasoned | pairs |
| -- | -- | -- |
| `str` | `str` | 88 |
| `bool` | `bool` | 17 |
| **`str`** | **`bool`** | **15** |

**The mixed rows are the tell.** On those 15, the beginner side is a full paragraph explaining what hardening off is and how to do it; the seasoned side is `true`.

That is not a thin seasoned half. **It is a boolean flag and a prose field sharing a key name**, and the two have drifted crop by crop into whichever shape the author reached for.

**Ruling: split the key.** A flag (`hardening_off_required`, unsuffixed, one value) and a prose field (`hardening_off_note_beginner` / `_seasoned`, assessed under §9.1 like any other pair). The 17 identical booleans become one flag each; the 88 prose pairs keep their prose; the 15 mixed rows get whichever half they are missing.

**Do not resolve this by dropping the suffixes.** There is no beginner version of `true` -- that much was right -- but the conclusion does not follow, because most of this key is not a boolean at all.

All 120 render **A**.

### B2 -- `soil.*_texture` is TWO shapes on one key, and the first ruling covered only one

> ⚠ **Corrected 2026-08-20, during the round 2 draw.** The first version of this section ruled the key on its 45 list-typed pairs and called the differences indefensible. **The key actually carries 138 pairs in two shapes**, and the ruling was true of 45 of them and false of the other 93. Recorded rather than replaced -- this is the **third** time in this document's history that a census over one type has been mistaken for a census over one key (see B1's note). The lesson has now cost three rulings and should be treated as a standing hazard, not an anecdote.

| shape | pairs | crops | byte-identical |
| -- | -- | -- | -- |
| list-typed controlled vocabulary | 45 | -- | **39 of 45** |
| **str-typed prose register pairs** | **93** | **31** | **0 of 93** |

**The 45 list-typed pairs: not register-bearing.** These are controlled vocabulary. 39 are byte-identical. The 6 that differ are all melons, and every difference is a **synonym inside the vocabulary**:

| beginner | seasoned |
| -- | -- |
| "light sandy soil" | "loamy sand" |
| "wet, poorly drained clay" | "poorly drained clay" |

**This is the cosmetic-pair phenomenon in the one place where it cannot be argued.** In prose, a reasonable person can claim a synonym carries register. In a controlled vocabulary the value *is* the term, so there is nothing for a register to do. A vocabulary with two spellings of one member is a vocabulary with a bug.

**Ruling for the 45:** collapse to a single unsuffixed list per texture class, and reconcile the 6 melon divergences to whichever term the vocabulary defines.

**The 93 str-typed pairs: ordinary prose register pairs.** They are full prose, none byte-identical, and they are assessed under §9.1 like any other pair. **They are not covered by the ruling above and must not be collapsed.**

All 138 render **C** -- shadowed by the `_core` sibling the renderers actually read (see v1.2 §10 and the PLA-255 inventory).

### B3 -- the companion arrays are the legacy split, still unreconciled

5 list pairs surface, and they hold **different companions, not different wording**:

> **grapefruit** `companions.good_beginner` = [White clover, Nasturtium]. `companions.good_seasoned` = [Fava bean].

Different plants. Asking whether they "differ substantively" is a category error -- in the three-array model, **membership itself encodes visibility.**

**But 5 understates it.** 107 of 128 crops still carry a populated legacy `good_seasoned` / `bad_seasoned` alongside the current `good_beginner_seasoned` shape, and **only 3 also populate `good_beginner`** -- which is why just 5 rows surface as pairs. The other 104 sit inside the 683 one-side-empty exclusions.

This is the array-level split that `register_bearing_field_inventory_v1_0.md` **put out of scope at §5 in May.** It is still unreconciled. Citrus is simply where it became visible.

**Ruling: exclude from the pair population.** The real question is whether array membership is correctly assigned across 107 crops, which is a different review with a different standard, and it needs the inventory's §5 scope decision revisited first.

### ⚠ Schema shape and render status do not line up

**B1 and B3 are entirely render A. B2 is entirely render C.**

A rule keyed on schema shape will get render status wrong, and a rule keyed on render status will get schema wrong. Any ruling touching both must state which axis it is keyed on.

### Also found: 2 single-element-array prose fields

`harvest_ready` and `description` on **bee-balm** and **honeydew-melon**, where the seasoned side is prose wrapped in a one-element list. That is the type instability tracked in PLA-259, now with its crops identified. Not a register question.

### B4 -- `pests[].name` is a proper noun

8 pairs, **all 8 byte-identical**, every one "Fungus gnats" on a microgreen crop.

**A species name has no register.** There is no beginner version of a proper noun, and substituting one would make the pest harder to look up rather than easier -- the opposite of what the beginner register is for.

**Ruling: not register-bearing.** Same shape as B1's booleans. Where a beginner needs help with a pest name, the help belongs in the surrounding prose (`symptoms_beginner`, `cause_beginner`), glossed per §9.3, not in a renamed `name` field.

All 8 render **A**.

### Note on the denominator

The whole-file audit reported "77 cosmetic pairs of 20,084." **20,084 is exactly the str/str count** of the 20,168 total. Its denominator was not wrong; it was **narrower than stated**, excluding the 84 non-string rows without saying so.

## §9.5 The measured rate

**Round 2 landed 2026-08-20.** 30 pairs from render status A, 10 from C, drawn systematically at canonical `be8a6d1e` and read against §9.1.

### Rendered prose -- the product answer

Combining round 2's stratum A with round 1's 15 (also stratum A, re-ruled against this standard now that it exists):

> **13 cosmetic of 45 pairs = 29%. 95% interval roughly 17% to 44%.**

That is **~4,200 of the 14,541 rendered pairs.**

Adding the contradictory and inverted pairs, **36% of rendered pairs carry a defect of some kind.**

**The standard discriminates.** The borderline band fell from **5 of 15 in round 1 to 1 of 30 in round 2.** Round 1 had no rule and its calls were judgment; round 2 had one and they were not. That collapse is the main evidence §9.1 is usable by someone other than its author.

### Unrendered prose -- the hypothesis was wrong

**1 cosmetic of 10 = 10%.** Prose that renders nowhere is **not** worse-written than prose that renders. The concern that unrendered fields received less care is not supported.

**⚠ But this measures region prose, not unrendered prose in general.** `regions.<R> :: region_notes` is 45.8% of stratum C, and the draw returned it 7 times in 10 -- the population's actual shape, not an artifact. Region notes are long-form and have more to say, so **field family confounds render status here.** Quote this number as "region prose is not neglected," never as "unrendered prose is fine."

### What follows for the backlog

At 29%, the existing cosmetic-pair population in rendered prose is **roughly 4,200 pairs.** That is a real project and it is not the 12,000 that a 60% rate would have implied.

**This standard governs new authoring and the arcs' per-crop checks.** Whether to sweep the existing 4,200 as a separate pass is a scoping decision, not a rule question, and it belongs with the arc sequence rather than here.

---

## §9.5.1 What is still not settled

**Inversion frequency.** 2 of 40 in round 2 (A29 tomatillo, C1 asparagus), 1 of 15 in round 1, 3 of 25 in the blind read. Consistently present, consistently low, never sampled deliberately. **6 of 80 across three reads is about 7.5%** -- enough to say the class is real, not enough to price a sweep.

**Contradictory pairs.** 2 found across 55 pairs read (collards, A14 heirloom-tomato). Too rare to estimate and too consequential to ignore: both halves are individually plausible and gate-clean, so nothing but reading finds them.

**Byte-identical pairs -- now measured.** A census over all 20,168 pairs found **263 byte-identical**, confirmed under both codepoint and UTF-8 byte equality, with 0 becoming equal only under NFC normalization.

Subtracting the shapes ruled not-register-bearing in §9.4 (17 bool, 39 soil texture, 8 `pests[].name`), **199 are genuine duplicates and 161 of those render.** 152 of the 161 sit in four short-UI-string families -- `growth_stages[].log_prompt`, `failure_diagnostics[].label`, `notifications[].title`, `weather_triggers[].title` -- which is **8.5% of those 2,001 pairs.** Whether those families should be register-bearing at all is a schema question, not a prose one, and it is tracked separately.

**Zero whitespace-only differences.** Nothing was absorbed into the 263 by trimming.

**Four disguised duplicates**, all one crop and one substitution: lettuce-leaf, a comma becoming a colon in four titles. **Punctuation is not a register.**

Duplicates concentrate by crop -- tomatillo 17, lettuce-leaf 16, okra 14, the four tomato cultivars 10-11 each. **A crop with a high duplicate count is a triage signal**, not just a cleanup target.

**Stratum B.** 1,583 pairs, never drawn. All 17 B families are B for one reason: they feed Herb's LLM grounding slice and nothing else.

**The 93 str-typed `soil.*_texture` pairs** were excluded from round 2's draw as part of the 45-pair exclusion, which was correct at the time and wrong in retrospect -- see §9.4 B2. They are ordinary prose pairs and belong in any future draw.

## §9.6 Change log

- **v1.3 amendment (2026-08-20):** Closes v1.2 §10.1. Adds §9.1 the differentiation test, §9.2 contradictory pairs, §9.3 gloss-avoidance, §9.4 three schema questions wearing one suffix, §9.5 the remaining gaps. Grounded in PLA-256 round 1 (15 pairs read at canonical `be8a6d1e`) plus a full census over all 20,168 pairs. Retires the 0.4% similarity figure with the reason it was wrong.
- **§9.4 B1 rewritten same day**, before filing, after a fuller census showed the first draft's bool ruling was wrong: `start_method.hardening_off` carries 120 pairs in three shapes, not 17 booleans, and dropping its suffixes would have deleted 88 explanatory paragraphs.
- **§9.4 B2 corrected 2026-08-20** during the round 2 draw: `soil.*_texture` carries 138 pairs in two shapes, not 45, and the controlled-vocabulary ruling is false of the 93 str-typed prose pairs. **Third instance of the same error** -- a census over one type mistaken for a census over one key. Both superseded rulings are recorded in §9.4 rather than removed.
- **§9.4 B4 added and §9.5.1 updated 2026-08-20** from the byte-identical census: `pests[].name` ruled not register-bearing (8 pairs, all identical, all proper nouns), and the duplicate population measured at 263 total / 199 genuine / 161 rendering.
- **§9.5 replaced 2026-08-20** with the measured rate from round 2: **29% cosmetic in rendered prose, 95% CI 17-44%**, ~4,200 pairs. The deferred-rate placeholder is retired. Unrendered prose measured at 10%, with the region-prose confound stated.
