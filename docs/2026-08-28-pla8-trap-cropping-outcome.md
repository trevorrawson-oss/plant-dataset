# PLA-8 -- the `trap_cropping` catalog round: outcome

Written 2026-08-28. Brief: `docs/2026-08-28-trap-cropping-mint-handoff.md`.
Base canonical `be444e25`; mint output `86c5396a`; backfill output `96cbc68c`.

Run in parallel with the main session's batches 11/12 under the SHA-collision protocol in the brief.
This session took slot 1 by agreement.

---

## 1. WHAT SHIPPED

Two promotes, the chlorothalonil pairing (`d096415` mint / `2e86279` backfill) applied again.

| | promote | effect |
| -- | -- | -- |
| 1 | `tools/promote_pla8_trap_cropping.py` | mints `trap_cropping`, control_methods 58 -> 59. Zero crops, zero sources, zero existing methods. |
| 2 | `tools/promote_pla8_trap_cropping_backfill.py` | 10 rungs on 9 certified crops, 20 register strings. Zero catalog change. |

Roster laddered stays **46 of 121** -- these are rungs added to ladders that already existed, not new
ladders. Catalog **58 -> 59**.

---

## 2. THE MEASUREMENT WAS WRONG, AND THE CORRECTION CHANGED THE GUARDS

The brief measured **20 problems on 18 crops**. Re-run against `be444e25` over EVERY string field
rather than the eight standard prose fields, the true figure is **22 problems on 20 crops**.

The two it missed are `nasturtium`/Aphids and `zinnia`/Japanese beetles, which carry their prose in
`note_beginner` / `note_seasoned` -- a shape used by **91 problems** on the shell and ornamental
crops and absent from the scanned field list. The main session re-scanned independently, confirmed
22/20, and corrected the brief in place.

**Both are the INVERTED class, and both are textbook trap crops**, which makes them the two records a
later pass is most likely to attach the rung to wrongly. The exclusion set went from four to six.

This is the `absence-findings-are-document-scoped` lesson in a new place: the scan was correct about
the fields it read and wrong about the population, and nothing in its output said so.

---

## 3. THE T1 READ ANCHORED THE TIMING, NOT THE PRACTICE

Trap cropping without the removal step raises the local pest population and parks it beside the crop.
That is the sentence a reader can be harmed by, so it is the one that had to be read. Four documents
fetched, three cited.

- **UGA Circular 1118**, *Trap Cropping for Small-Market Vegetable Growers* (Westerfield & Braman,
  reviewed 2022-07-13). Definition, establish-earlier, two weeks prior, 8 to 12 ft separation, and
  "After trap crops are infested with target insects, they can be controlled with timely insecticidal
  applications or mechanical removal."
- **UF/IFAS Gardening Solutions, Trap Cropping.** The dispersal half: "Once the damaging insects have
  established themselves on your trap plants, you must eradicate them to prevent them from moving on
  to the main crop." Also 5 ft perimeter minimum, and "Mustard has been an effective control of
  harlequin bugs on collards" -- which covers seven of the ten targets directly.
- **UMass Vegetable Program, Squash Bug fact sheet.** THE DEADLINE SENTENCE, and the reason the
  method could be minted at all: "The trap crop must receive an insecticide application or be
  mechanically destroyed before eggs hatch."

**Read and NOT cited, deliberately:**

- **Purdue Vegetable Crops Hotline** (Ingwell, 2025-06-26) carries the harlequin-specific obligation,
  "Action must be taken on these trap crops to manage the population and thus protect later
  plantings." It corroborates, but the article lives on `vegcropshotline.org` while the catalog's
  `purdue_ext` entry is anchored at `extension.purdue.edu`. A declared source whose anchor sits on a
  different domain from its catalog entry is the `catalog-divergence` shape, so it stayed out.
- **WVU Extension's harlequin bug page** carries the cleanest nursery warning of all ("Some type of
  control is necessary to avoid the trap crop becoming a source of infestation") and returned **403
  on both user agents**. NOT cited. A page that could not be read is not evidence, whatever a search
  summary says about it. Worth a retry in a later round; if it opens, it is the best single anchor
  for this method.

**The brief's suggested anchor did not hold.** It said Clemson's cole crop factsheets "carry the
harlequin bug trap-crop advice verbatim". The factsheet was fetched and read: it covers harlequin bug
identification, eggs and flea beetle host preference, and says **nothing about trap cropping**.
Checked rather than assumed, which is the only reason it was not cited on the strength of the brief.

---

## 4. THE TWO-GROUP SPLIT, AND WHY IT IS A GUARD

The ten split by whether the CROP'S OWN prose states the removal step:

- **DESTROY_STATED (7)** -- the harlequin bug entries. Each carries the action to its end ("then
  destroy it before the main crop is set out"; turnip: "can concentrate the bugs for removal"). These
  rungs restate the removal and attribute it with the phrase "this crop's guidance".
- **DIVERT_ONLY (3)** -- the flea beetle entries on `arugula`, `bok-choy`, `jalapeno`. Every one stops
  at the diversion ("divert beetles from the main crop", "can draw beetles off the crop"). **None
  names an endpoint.** These rungs route the removal timing through the METHOD's cautions and are
  FORBIDDEN the attribution phrase.

Saying "this crop's guidance" about a removal step a source never states would author a
recommendation, which is exactly the batch-10 `planting_time_avoidance` ruling in a different field.
`check_group_premise` verifies both directions in canonical and refuses a crop whose prose has
drifted across the line.

---

## 5. THE SPECIES GUARD, AND WHY PER-CROP TEXT

The ten name **different trap plants**: mustard on most, "arugula or mustard" on arugula,
**nasturtium** on jalapeno, "mustard, collards, or rapeseed" on collards, "mustard, kale, or
rapeseed" on kale, "mustard or another preferred crucifer" on turnip. A single shared rung text would
have put mustard on jalapeno, which is not a brassica and whose prose names nasturtium.

Measured over the four prevention/treatment fields, **exactly one pair is byte-identical: cabbage and
cauliflower.** They share one rung text; the other eight are distinct.

`check_rung_distinctness` pins the correspondence **in both directions** -- identical prose must yield
identical rungs, differing prose must yield differing rungs. One direction catches a copied rung, the
other a needlessly forked one. This is batch 3's cucumber lesson turned into a check.

---

## 6. PLACEMENT: END OF THE CULTURAL RUN

Trap cropping is cultural, and all ten ladders end at a physical or soft_chemical rung, so appending
would break tier monotonicity on every one. The rung is inserted after the existing cultural rungs and
before the first non-cultural one -- AFTER `garden_sanitation`, `weed_host_control`, `crop_rotation`
and `planting_time_avoidance`, because those cost nothing but attention while this one asks the reader
to establish and then destroy a separate planting. Least invasive still comes first WITHIN the tier.

---

## 7. THE SIX EXCLUSIONS, PINNED IN BOTH DIRECTIONS

Each carries its own reason string, because they are wrong in three different ways and a shared
message would under-explain the worst of them.

| problem | class | why no rung |
| -- | -- | -- |
| `radish`/`flea-beetles` | INVERTED | radish IS the trap crop, for other vegetables |
| `radish`/`cabbage-root-maggot` | REPURPOSED | repurposes an already-damaged sowing |
| `dill`/Parsleyworm | CONSERVATION | larvae relocated to keep them ALIVE |
| `parsley`/Parsleyworm | CONSERVATION | same; extra parsley grown as a swallowtail host |
| `nasturtium`/Aphids | INVERTED | **the most dangerous of the six** |
| `zinnia`/Japanese beetles | INVERTED | preferred host whose trap value protects other plants |

**nasturtium is the one a later pass talks itself into.** Its own text says "on a trap stand, monitor
and pull or destroy the planting once it is heavily loaded", which READS exactly like this method's
action. But the dataset carries nasturtium as an ornamental and edible crop, not as a trap stand, and
the same record goes on to say aphids get treated normally on such a planting. A rung there tells the
reader to destroy the crop they are growing.

A method whose meaning ends in "then destroy the trap" is **actively wrong**, not merely redundant, on
the two conservation entries.

Both promotes refuse if any exclusion fails to **RESOLVE** to a real problem. A typo'd slug or problem
name would leave the refusal protecting nothing while still reporting green -- the derived-guard
vacuity shape. `find_problem` matches by `id` OR `name` because the four laddered exclusions carry ids
and the two unladdered ones have none.

---

## 8. WHAT THE MUTATION HARNESSES FOUND

Both suites are replay-pinned; no RED phase claimed. Evidence is `VerifyPostIsDriven` plus the
harnesses.

### Mint: 34 injected, 34 caught, 0 survived

`tools/mutate_pla8_trap_cropping_suite.py`. Preflight 35/35 anchors matched exactly once; positive
control GREEN; sentinel RED. Seven families: disclosure 8/8, scope 6/6, blast 7/7, exclusion 5/5,
contrast 4/4, hygiene 3/3, mechanics 1/1.

### Backfill: 42 injected, 42 caught, 0 survived (run 2)

`tools/mutate_pla8_trap_cropping_backfill_suite.py`. Preflight 43/43; positive control GREEN;
sentinel RED. Eight families: placement 8/8, premise 7/7, blast 7/7, exclusion 6/6, content 5/5,
species 5/5, distinct 3/3, mechanics 1/1.

**Run 1 returned 1 survivor, and it was a real unreachable branch.** `verify_post` carried a
"the rung sits after a non-cultural rung" check. It survived being disabled, because this method is
cultural and cultural is the LOWEST tier rank: a cultural rung landing after a non-cultural one
always breaks the monotonicity check two lines below, so the branch could never fire on its own.
**Deleted** rather than kept as a forward assertion -- an unreachable branch reads as coverage while
providing none, which is the entire argument behind the PLA-215 bar. Its injection was removed with
it. The end-of-cultural-run check, which IS independently reachable, stays.

**Its driver had hedged, and that is the pattern worth carrying forward.** The test asserted
`"after a non-cultural rung" in out or "tiers decrease" in out`. A disjunction over two error
messages passes whether or not the branch under test is reachable, so it hid the masking completely.
**This is the second time in these two suites that a hedged OR concealed a masked guard** (the
mint's exclusion driver was the first). Both are now single-message assertions.

**Rule of thumb this round produced:** in a `VerifyPostIsDriven` test, an `assertTrue(a in out or b
in out)` is a smell, not a convenience. It means the author was unsure which branch answers, and
that uncertainty is exactly the signal that one of them may never answer at all.

**Run 1 of the mint harness returned 2 survivors, and both were real:**

1. **`verify_post`'s per-exclusion loop was UNREACHABLE.** The mint-only sweep (`landed = rungs_of(...)`)
   fires on ANY rung anywhere, including on an excluded problem, so it answered for the exclusion
   branch every time and that branch could never fire on its own. **The suite had already papered
   over this**: its driver asserted a disjunction, `"mints only" in out or "must never get one" in
   out`, which is how a masked guard passes review. Fixed by ordering the six before the sweep; the
   test now asserts the specific message with no hedge. This is `guard-tests-pass-because-an-earlier-check-fires`,
   caught by the harness rather than by reading.
2. **One of my own mutations was INERT.** `EXCLUSIONS = () or (...)` -- an empty tuple is falsy, so it
   evaluates straight back to the original and nothing was mutated. Same broken shape batch 10 hit.
   Replaced with a real rebinding.

**THE TWO `X or ...` SHAPES ARE NOT THE SAME, AND THE DIFFERENCE DECIDES WHETHER SHIPPED WORK IS
AFFECTED.** This round first recorded that the idiom is inert wherever it appears, including in
shipped harnesses. **That was wrong**, corrected after the main session swept every harness and
verified empirically rather than by reading. Both halves checked here directly:

- `X = () or (THE ORIGINAL PASTED BACK)` -- **truly inert**. The empty tuple is falsy, the original
  wins, nothing is mutated, and it reports SURVIVED. This is the `EXCLUSIONS` case above, and the
  main session hit the same shape twice today (batch 10 `COPPER_ON`, batch 11 `ADVICE_FIELDS`).
- `X = {} or {MANGLED FIRST KEY, ...rest unchanged}` -- **NOT inert and NOT blind**. The anchor
  replaces only the first line or two, so the result is the original table with one key RENAMED. A
  guard that subscripts `TABLE[g]` then raises `KeyError` and the suite reddens.

`mutate_pla8_chlorothalonil_backfill_suite.py` uses the second shape, and re-running it gives
**30 injected, 30 caught, 0 survived, PASS** -- including the "required-hedge table is emptied"
injection. **That shipped harness has NOT been grading nothing.** What is wrong with it is the
LABEL: the table is not emptied, it is renamed, and the `{} or` prefix does no work at all. Weak and
misnamed, not a coverage hole. The same is true of the five other files carrying the shape (batch 5,
chem_cohort x3, conventional_disclosure x2). Filed as a **labeling cleanup**, not an audit.

Recorded at length because "a shipped harness has been grading nothing" is exactly the kind of claim
that sends someone re-auditing committed work, and it does not hold. This round's own mint harness
carried the same mislabel on its disclosure-table injection and now does a real emptying instead.

A third ordering defect was found and fixed the same way in the MINT's `verify_post` before the
harness ran: the verbatim check (`cm[KEY] != METHOD`) subsumes every substantive check, so with it
first the disclosure, contrast, applies_to and tier branches were all unreachable. Caught by
`VerifyPostIsDriven` failing on two drivers at first write, which is the class of thing that class
exists to find.

---

## 9. THE GAUNTLET

Run against the replayed final state (`96cbc68c`).

- `tools/gate_all.py` -- **121/121 certified crops PASS**
- `whole_crop_gate` -- **PASS on all 9** touched crops
- `control_ladder_gate` -- **0 violations**
- `register_completeness_gate` -- **PASS**, 0 unruled prose fields
- `release_verify` -- **clean, no blocking concerns**; only the 9 declared crops changed,
  `control_methods` the only top-level change, catalog +none -none, reference `lettuce-leaf`
  byte-identical
- COMPACT preserved; no newline, no space-after-comma
- Guard suites green under **both runners**: 134 tests (61 mint + 73 backfill), direct and pytest

`release_verify` needed `--slug cabbage`. Its default pilot slug is `cherry-tomato`, which it folds
into the expected-changed set, so with the default it reports a CONCERN that cherry-tomato did not
change. That is the known `release_verify is single-crop-pilot-shaped` behavior, not a finding.

---

## 10. OWED / CARRIED FORWARD

- **`brussels-sprouts`/Harlequin bug** should take this rung when batch 12 lands; its prose names
  "cleome or mustard ... then destroy it". The main session has the note and has wired a REQUIRE
  guard for it.
- **Five more crops pick it up for free** once laddered: `blackberry` (stink bugs), `cayenne-pepper`,
  `eggplant`, `habanero` (flea beetles), `okra` (stink and leaf-footed bugs, cowpea trap). Minting
  before those batches is what keeps the backfill at 10 rather than 16.
- **WVU's harlequin bug page** (403 on both user agents) is the best unclaimed anchor for this method.
  Retry in a later round.
- **The inert `X or {...}` mutation shape** in `mutate_pla8_chlorothalonil_backfill_suite.py`, and any
  other harness using it. One fewer real injection than claimed, wherever it appears.
- `container_culture`, `certified_clean_stock` (the main session widened it to `nematode` in batch
  11), a generic pheromone/monitoring trap, and diatomaceous earth remain owed from the catalog list.
