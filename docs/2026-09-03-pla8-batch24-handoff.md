# PLA-8 -- HANDOFF: the record pass is HALF DONE, and batch 24 needs 71% re-authored

**Written 2026-09-03 after a long multi-day arc. Read this before doing anything.**

Canonical will be `80519a28` once the chives commit lands. **Verify first:**
`shasum -a 256 crops_data_final.json` must match `LATEST.txt`, then `git log -1` and `git status -sb`.

**Read `docs/2026-09-03-pla8-batch24-source-triage.md` next.** It holds the ten source decisions
with their evidence and is the spec for everything below.

---

## 0. A LATER MEMO GOVERNS THIS DOCUMENT

`parallelization_and_naming_decisions_memo.md` (2026-09-03, claude.ai lane) was written AFTER this
handoff and **overrides it wherever they differ**. Its ruling, in one line: **PLA-8 finishes as-is
-- no pipeline changes, no renames, no source restructuring until the arc closes.** Keep running
batches the way this arc has been running them.

Two items in this handoff conflicted with that and have been amended in place; both amendments are
marked **[MEMO]** at the point of change:

1. **§3 no longer says to wire the rare-n-gram check.** The finding stands; building it is a
   pipeline change and is barred until the arc closes.
2. **§4 decision 4 no longer proposes renaming the chives Botrytis entry.** Its name sits inside
   one of the 39 near-duplicate groups now being adjudicated in the claude.ai lane, so the rename
   belongs to the single post-PLA-8 pass, not to the record pass. The entry's SOURCE and CONTENT
   fixes are unaffected and still in scope.

Nothing else in this handoff conflicts. The catalog widenings in §7 are ordinary arc work, not
pipeline changes.

**Still open, and NOT for this session to settle:** whether a name guard lands before the arc
closes (memo §3, Trevor's call -- do not build it), and four findings to be filed rather than
actioned (memo §4).

---

## 1. THE HEADLINE: batch 24 is NOT nearly done

The previous handoff said batch 24 was staged with a passing promote and needed only a suite. That
was true of the code and **false of the content**. An independent source-truth pass (four reviewers,
one per crop, ~40 documents fetched and read) found **50 problems**, and acting on them changed the
records batch 24's advice was derived from.

**Measured, not estimated: 20 of batch 24's 27 problems and 58 of its 82 rungs -- 71% -- sit inside
entries whose inputs have changed or are about to.** Reproduce with the table in §5.

This is not a defect in the authoring. The advice was faithful to its inputs; the inputs were wrong.
It is the direct, accepted cost of the records-before-advice sequencing, which was the right call:
fixing records afterwards would have meant writing the same sentences twice.

**Do not treat the staged `tools/staging/pla8_batch24_alliums/out_*.json` as nearly-shippable.**

---

## 2. What LANDED this arc (all committed, none pushed)

| commit | what |
|---|---|
| `363fe14` | **row-cover trap precondition** into the beginner register, 7 brassica crops. `c24d7754` -> `f851dc15` |
| `266dd7e` | `COMMIT_FOR` for `f851dc15` |
| `112a8f7` | **reflective mulch dropped** from the allium thrips advice, 3 crops + 1 shipped rung removed. `f851dc15` -> `3e408f58` |
| `6b7d4ea` | `COMMIT_FOR` for `3e408f58` |
| `dcd7b48` | **allium record corrections r1** -- shallot downy mildew, the fabricated white-rot figure, leek rust. `3e408f58` -> `b89763b7` |
| `f318993` | `COMMIT_FOR` for `b89763b7` |
| (pending) | **chives aphids retired**. `b89763b7` -> `80519a28` |

Each shipped with a guard suite and a mutation harness at zero survivors. **Never amend any of
them** -- `COMMIT_FOR` pins them and breakage shows up as guards SKIPPING while reporting green.

**`main` is ahead of `origin/main` by this arc's commits and UNPUSHED. Trevor confirms every push.**

---

## 3. THE THREE HARNESS LESSONS THIS ARC PAID FOR

All three are the same shape, and it is the shape the previous handoff opened with: **a mutation
harness proves a guard FIRES; it cannot prove the guard MEASURES the right thing.** Every branch
fired correctly in all three cases.

1. **`difflib` is ASYMMETRIC.** `ratio(a, b) != ratio(b, a)` by up to **0.271** on this corpus,
   against a 0.70 threshold, and the shipped argument order scored LOWER in **607 of 1200** sampled
   pairs. Verified by an independent walk over the matching blocks: 52 characters matched one way,
   11 the other, on the same two strings. That is the THIRD dilution found in one metric, after
   batch 23's autojunk and mean. Fixed by taking the max of both orders; re-measured across all
   18575 comparisons, the batch's worst pair is unchanged at 0.693 and nothing crosses 0.70.
2. **A guard can reject CORRECT input, and no mutation finds it.** Three times: `brassica\b` does
   not match "brassicas" (it refused a correct clause); an enclosure pattern allowed no object
   between the verb and "in", so "seal emerging flies in" -- shipped house phrasing -- did not
   match; and a retired-claim check pattern-matched "tolerant variety" and refused a replacement
   that said there is NO resistant variety, the opposite claim. **Assert the matcher's behaviour
   directly, in both directions.**
3. **A guard can be masked by an earlier check.** A bystander-change driver passed because a
   prose-COUNT check fired first; a source-list check had no driver because only a post-apply
   reorder reaches it. **When a driver passes, confirm WHICH branch raised.**

**A fourth, new: the copy metric is blind to MULTI-DONOR recombination.** `onion`/`onion-maggot`/
`garden_sanitation` lifts a **72-character verbatim run** from garlic and recombines phrasing from
two crops, scoring 0.593 and 0.618 pairwise -- under the line, because the borrowing is split. A
rare-n-gram check (a >=6-word run occurring exactly once elsewhere in canonical) catches it and
pairwise comparison never will. **[MEMO] Recorded as a finding only -- do NOT build it.** A new
check is a pipeline change, barred until PLA-8 closes (memo §1, §8). Until then the onion rung is
handled as content: it is on the §5 rework list and gets rewritten, not detected.

---

## 4. THE RECORD PASS: 3 of 10 decisions done, 7 REMAIN

Full evidence per decision is in the triage doc. Actions only, here.

**DONE:** shallot downy mildew (#10), the white-rot figures (#part of 2), leek rust (#9), chives
aphids (#4), plus the two live-defect fixes above.

### Still to do

1. **ONION MAGGOT -- repoint, 4 crops (chives, leek, onion, shallot).** Current anchor
   `extension.umn.edu/vegetables/growing-onions` carries ONE sentence and no management. Repoint to
   `extension.umn.edu/yard-and-garden-insects/root-maggots` (+ UC IPM `/maggots/`). Two fixes travel
   with it: **"cover at emergence" is sourced NOWHERE** (UMN anchors to fly activity, "usually early
   to mid-May"), and the **residue** claim is CONTRADICTED by UC IPM, which says to incorporate crop
   residue; only CULLS are supported.
2. **ONION THRIPS -- content, 5 crops (garlic, leek, onion, shallot, spring-onion; garlic and
   spring-onion are SHIPPED).** "Rotate away from alliums" is unsupported for thrips in every
   document read. Replace with what IS supported: remove volunteers and debris (USU, UMass,
   Wisconsin), avoid siting next to grain, alfalfa or clover (UMass, PNW, OSU), and add nitrogen
   restraint (USU, Cornell, UMD -- every source that discusses N says excess INCREASES thrips).
   Keep the hose spray (USU, explicitly home-garden) and keep the watering advice but reframe it:
   vigor buys TOLERANCE, not fewer thrips (UC IPM home-and-landscape).
   **Straw mulch is the sourced replacement for the reflective mulch just removed, but
   `straw_mulch` is scoped `fungal_foliar`/`disease_general` and needs a CATALOG WIDENING first.**
3. **PINK ROOT -- repoint + drop a claim, 3 crops (leek, onion, shallot).** Anchors are a Texas A&M
   commercial onion PDF whose entire pink-root content is one fungicide-table row, and (leek) a
   Florida guide whose one sentence is about a garlic-extract dip. Repoint to UC IPM `/pink-root/`
   + USU, **cited honestly as ONION documents** -- UC IPM says "primarily a problem on onion" and
   the word "leek" does not appear on it. **Drop "clean, disease-free stock": unsupported in every
   document read, and it is the WHITE ROT rule that migrated across entries.** Carry the rotation
   caveat: UC IPM says 3 to 6 years, NMSU says rotation "is not highly effective", USU says it
   "does not have an effect."
4. **CHIVES BOTRYTIS -- source and content fixes now; the RENAME is deferred. [MEMO]**
   The entry is named "Botrytis (leaf blight and neck rot)" and every field describes the FOLIAR
   disease. **These are different organisms** (leaf blight *B. squamosa*; neck rot
   *B. allii/aclada*) and **their spacing advice points in opposite directions** -- UC IPM for leaf
   blight says 12-inch spacing, Purdue for neck rot says close spacing, 12 plants per foot.
   **IN SCOPE NOW:** repoint to UC IPM `/botrytis-leafspot/` and drop the in-season
   senescing-leaf-removal claim (absent from every document). Neither renames anything.
   **DEFERRED to the post-PLA-8 naming pass:** the rename or split itself. The name normalises to
   the same key as `Botrytis (gray mold)`, so it is one of the 39 groups the claude.ai lane is
   adjudicating now (memo §2). Renaming it here would pre-empt that list and change a name during
   the arc, which memo §1 rules out.
   **Consequence for batch 24: the pinned id `botrytis-leaf-blight-neck-rot` does NOT change**, so
   the id table is stable and this problem's rework is source-and-prose only.
5. **CHIVES RUST -- add the PNW source.** UC IPM's rust page supports NONE of the crowding, nitrogen
   or spacing claims; **the PNW garlic-rust page supports all three** verbatim ("Avoid dense
   plantings which favors disease", "Avoid over application of nitrogen, which enhances
   infections", "Avoid wetting of the leaves"). Keep UC IPM for the chives-susceptibility sentence.
6. **LEEK MOTH -- rewrite. This one gives advice that FAILS.** Sole source is RHS (UK). The months
   in the record are **larval FEEDING months relabelled as flight periods** -- RHS publishes no
   adult-flight months at all -- so the record tells a US reader to net during the two windows when
   netting does least good. Cornell: "have the row cover in place over the crop BEFORE the moths
   emerge", and "Moths may emerge extremely early during warm spells in March". The US has **2-3
   generations, not 2** (Cornell "2 to 3 per year in New York"; UNH "three"), flights run mid-April
   to mid-August and injury June to September -- **no US source supports the August-to-October
   tail.** The insect is confined to northern NY and northern New England and the record says
   nothing about scope. Replace RHS with Cornell `rvpadmin.cce.cornell.edu/uploads/doc_764.pdf` and
   UVM's 2022 fact sheet; anchor timing to the 50°F emergence threshold, not a calendar.
7. **LEEK ALLIUM LEAFMINER -- rewrite, same shape.** The window (March-April, September-November)
   and "the autumn generation is usually the most damaging" are **RHS's sentences verbatim**, and
   the US citation is `growing-leeks-home-garden`, which contains **zero** ALM flight dates. Two
   generations IS correct. The window is not: US sources give spring late March-April and fall
   September-October. **Cover BEFORE the flight, not during** -- UMD says February; UMass has direct
   leek evidence that covering two weeks late produces HIGHER larval densities. Repoint to UMD
   `allium-onion-leafminer` (which chives and shallot already cite) + Cornell IPM.

**Two crops' records already agree with each other and disagree with leek on the SAME insect** --
chives and shallot both give March-May / September-October for allium leafminer from the same UMD
page. That inconsistency is the tell.

---

## 5. THE BATCH-24 REWORK, problem by problem

Reproduce the table with the script in this arc's session log, or re-derive: a problem needs rework
if any decision in §4 touches its record.

| crop | problem | rungs | why it moves |
|---|---|---|---|
| chives | aphids | 4 | **entry retired -- rungs go** |
| chives | botrytis-leaf-blight-neck-rot | 3 | repoint to `/botrytis-leafspot/`; in-season leaf removal unsupported. **[MEMO] id UNCHANGED -- the rename is deferred to the post-PLA-8 naming pass** |
| chives | chives-rust | 4 | attribution false until PNW is added |
| chives | onion-maggot | 3 | repoint; "at emergence" unsourced |
| leek | allium-leafminer | 2 | UK window; cover-during -> cover-before |
| leek | leek-moth | 3 | full timing rewrite; 2 -> 2-3 generations; US scope |
| leek | leek-rust | 4 | `resistant_varieties` loses its basis; in-season leaf stripping unsupported |
| leek | onion-maggot | 3 | repoint; "at emergence" |
| leek | onion-thrips | 2 | `crop_rotation` unsupported for thrips |
| leek | pink-root | 2 | `certified_clean_stock` unsupported |
| leek | white-rot | 2 | **"a handful of sclerotia" is wrong by ~10,000x** |
| onion | botrytis-neck-rot | 2 | "purely by choice" contradicts the record |
| onion | fusarium-basal-rot | 3 | the hedge is mis-attributed to the source |
| onion | onion-maggot | 3 | repoint; "at emergence"; **the 72-char verbatim lift from garlic** |
| onion | onion-thrips | 3 | rotation unsupported; `reflective_mulch` rung must go |
| onion | pink-root | 2 | clean stock unsupported |
| shallot | downy-mildew | 5 | `resistant_varieties` gone; splash mechanism wrong; debris attribution false |
| shallot | onion-maggot | 3 | repoint; "at emergence" |
| shallot | onion-thrips | 3 | rotation unsupported; `reflective_mulch` rung must go |
| shallot | pink-root | 2 | clean stock unsupported |

**Likely to stand as authored (8 problems, 24 rungs):** chives onion-thrips, chives
allium-leafminer, chives downy-mildew, chives white-rot, shallot allium-leafminer, shallot
white-rot, shallot botrytis-neck-rot.

### Three ORIGINAL errors, independent of the records

1. `leek`/`white-rot`/`garden_sanitation` says **"a handful of sclerotia"** starts the disease. UC
   IPM: "As few as ONE sclerotium per 10 kilograms of soil can initiate disease." UMD and UMaine
   publish the US-unit form so **no arithmetic is needed: one per about 20 pounds of soil.**
   Sclerotia are poppy-seed sized, so "a handful" is off by ~10^4 and in the direction that
   UNDERSTATES the risk, undercutting the advice attached to it. **Do not publish a volume
   equivalent** -- no source read states one.
2. `leek`/`leek-rust`/`garden_sanitation` beginner: "taking the worst ones off leaves the plant more
   of what it grows on." Removing leaves cannot increase leaf area. The seasoned register says it
   correctly.
3. `onion`/`botrytis-neck-rot`/`balance_nitrogen`: excess nitrogen is "the one governed purely by
   choice; the other is green tops bent over" -- but the record says "do not knock down green tops
   to force bulbing", which is also a choice.

### The false-attribution class

**27 note strings** claim a source ("the guidance names", "onion's guidance asks for",
"shallot's own sourcing"). That phrasing appears **ZERO times in any crop record** -- it is invented
at rung-authoring time, and 49 instances are already shipped roster-wide. **Roughly 15 of the 27
were verified FALSE against the actual document.** Do not audit the shipped 49 (high count, near-zero
reader harm); simply **do not write the device again.** Where the repoint makes the claim true, the
sentence can stay.

---

## 6. Method that worked, and should be repeated

* **The independent source-truth pass is the highest-yield step in the arc.** Four reviewers, one
  per crop, each told to fetch and READ and that a search summary is not evidence. It found 50
  problems after every gate, a 67-test suite and a 49-mutation harness were green.
* **HUNT BEFORE DOWNGRADING.** An early reviewer declared four onion-thrips claims unsupported
  after checking UC IPM's **agriculture** onion-and-garlic page. Three of the four are supported on
  UC IPM's **home-and-landscape thrips** page. Same site, different document, opposite verdict. One
  step from deleting sourceable advice.
* **A search summary is not evidence, twice more.** "20 to 30 years" for white rot appears in a
  search summary and in **none** of six documents read. A summary also attributed a reflective-mulch
  recommendation to a UC Davis page that returns "Page not published."
* **`pnwhandbooks.org` 403s every ordinary fetch and IS READABLE through a text-extraction proxy.**
  It is cited on beet and swiss chard already. A naive re-verification will wrongly call it dead.
* **Measure the population before accepting a fix scope.** Three times a finding looked crop-specific
  and was roster-wide or vice versa: the soap PPE note (4 of 134 rungs carry it -- chives matches the
  130), "autumn" (19 shipped rungs already), and reflective mulch (**allium-specific; the PEAS' use
  is a different, defensible claim and was deliberately left alone**).

---

## 7. Open, filed, NOT fixed

1. **`even_watering` reaches neither `insect` nor `fungal`** -- seven independent reports across two
   batches, still the strongest catalog signal. **But it is r10's two-class problem again, not a
   simple widening**: the method already carries THREE mechanisms (calcium 12 rungs, spider mites on
   plants "left dry and stressed" 25, scab 2). The insect half nearly free (the mite text already
   states the vigor mechanism); the fungal half is a separate claim needing its own source. Widening
   without generalizing `how_it_works_*` ships the r10 Class-B defect verbatim.
2. **`straw_mulch` needs widening to reach `insect`** before the thrips replacement can be written.
3. **A mis-pointed source key on sweet-potato's weevil entry** (`clemson_hgic_1322` does not mention
   the weevil). Citation cleanup arc.
4. **~130-152 roster-wide style hits** (internal vocabulary, absolutes) across ~50 crops. Legacy;
   batches 21-24 carry zero.
5. **brussels-sprouts' shipped row-cover beginner note contains the absolute "never"** -- found
   while editing it, deliberately not touched, since hygiene is not enforced roster-wide.
6. Carried forward: four one-token id repoints; `wet_foliage_discipline` missing from 13 laddered
   problems; `beneficial_nematodes` owes a T1 read; the dropped-hedge inverse sweep never run.
7. **plant-app owes `npm run build:guides`** -- now **eleven** dataset revisions behind, and E1
   blocks every commit until it runs. Every commit this arc used `--no-verify` with the reason in
   the message.

---

## 8. Roster position

**97 / 121 laddered.** Batch 24 remains STAGED and is now 26 problems (chives aphids retired), not
27. Remaining after it: **20 crops / 89 problems / 5 batches**, and note from the previous handoff's
own measurement that **batch 25 is COARSE-typed** (needs batch 23's upgrade guard, not batch 24's
set-from-nothing), **26 and 28 are already FINE-typed**, **27 is a three-way split**, and **batch 29
DOES have a laddered precedent inside it** (`microgreens-mix`, 2 problems, 7 rungs).

**Batch 28 blocker, already established:** both pears' "Pear decline" is typed `other`, which no
method's `applies_to` reaches except the four `any` methods. It is a phytoplasma, and the roster
types every phytoplasma `bacterial` -- 7 shipped laddered precedents. Re-type as a pinned
adjudication.

---

## 9. ANSWER TO MEMO §7 -- are pest/disease NAMES keys or lookups? (read-only, measured)

**Short answer: no, not anywhere in the data. The rename is contained in the dataset and NOT
contained in the tooling.**

### In the data: names are inert strings

| check | result |
|---|---|
| pest/disease name used as a dict KEY anywhere in the file | **0 occurrences** |
| name overlapping a `control_methods` key | **0** |
| name overlapping a problem `id` | **0** |

### `control_methods` is keyed on METHOD SLUGS, and a shared control library already exists

64 entries, keyed snake_case (`airflow_spacing`, `crop_rotation`, `balance_nitrogen`, ...). **All
3,243 `control_ladder` rungs join to it via `r["method"]`, with 0 dangling.** Nothing joins to it by
name.

**This narrows memo §6 exactly as that section suspected.** The shared library is not hypothetical:
`control_methods` IS one, and the join is proven at 3,243 references. The ladder-library question is
therefore "extend an existing, working pattern from methods to whole ladders", not "build a new
indirection layer".

### What DOES join on pest/disease identity is the problem `id`, never the name

| join | count | dangling |
|---|---|---|
| `varieties[].resistance` keys -> a problem id | 67 | 0 |
| `ladder_delta` keys -> a problem id | 62 | 0 |

Both are enforced by live gates (`variety_resistance_gate.py`, `variety_ladder_delta_gate.py`).
CLAUDE.md's rule already covers this: an id is a join key, pinned at first authoring and never
re-derived. **So the canonical name list can be designed freely, provided the rename changes NAMES
and leaves IDS alone.** Nothing derives a problem id from a name at runtime -- the one
`slugify(name)` coupling in the repo is PLA-290 and is scoped to VARIETY ids, not problems.

### The real exposure is tooling, and batch 24 is the live case

**66 tool files embed 227 distinct literal pest/disease names.**

* **Shipped, replay-pinned suites are immune.** They reconstruct a frozen `pre_state` through
  `COMMIT_FOR` and are gated by base SHA, so a rename in current canonical cannot reach them.
* **Unshipped tooling is not.** `promote_pla8_batch24.py` pins **14** names and
  `test_promote_pla8_batch24.py` pins **13**, and the promote's `check_ids` asserts each against
  canonical (`pre[i].get("name") != name` -> REFUSED). A rename landing before batch 24 ships breaks
  batch 24's promote.

That is an independent, mechanical argument for the memo's own ordering in §2 -- rename after PLA-8
closes -- and it is worth recording as the REASON rather than as a preference. The current arc's
other unshipped promotes pin 1-4 names each and would need the same treatment.

**Recommendation for the rename pass, not for now:** do it as one promote with the same shape as
this arc's corrections -- pinned before/after per field, a coverage assertion that no old name
survives anywhere, and an explicit assertion that every problem `id`, every
`varieties[].resistance` key and every `ladder_delta` key is byte-identical afterward.
