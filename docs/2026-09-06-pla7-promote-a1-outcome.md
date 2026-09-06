# PLA-7 promote A1: the read, the pins, the gauntlet -- PREPARED AND HELD

**Date:** 2026-09-06. **Task 7** of `docs/superpowers/plans/2026-09-06-pla7-promote-a1-container-path.md`.
**Canonical is UNCHANGED by this document and by the run it records.**

| | |
|---|---|
| base canonical (read-only) | `72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222` |
| scratch post-state | `d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798` |
| scratch path | `/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/195c369f-c9cf-4c42-a2dd-f9c03b87c8cf/scratchpad/pla7_a1_post.json` |
| canonical after the run | `72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222` (byte-identical to the base) |

---

## 1. The read: the eight `rootstock` rows and mulberry

Every evidence sentence below is verbatim from that crop's own `container_notes.notes_seasoned` or
`notes_beginner`, and the promote proved each one occurs EXACTLY ONCE across all of that crop's
container_notes prose leaves (`prose_leaves`, sources and anchoring_urls excluded). No sentence was
taken from `overwintering.approach_*` or `container_overwintering_*`: the suite's
`test_refuses_applicable_with_no_prose` nulls apple's overwintering prose and must not collide with
an evidence row.

| crop | path | field | evidence (verbatim) |
|---|---|---|---|
| `apple` | rootstock | `notes_seasoned` | Containers suit apple only on a true dwarfing rootstock (M9, or M27 for the smallest pots); a semi-dwarf or standard tree will outgrow any practical pot. |
| `pear-european` | rootstock | `notes_seasoned` | Containers suit pear only on a genuinely size-controlling rootstock (a quince stock, or OHxF 333); a semi-vigorous or standard tree will outgrow any practical pot. |
| `pear-asian` | rootstock | `notes_seasoned` | Containers suit Asian pear only on a genuinely size-controlling rootstock such as OHxF 333; a betulifolia or calleryana standard tree will outgrow any practical pot. |
| `orange-navel` | rootstock | `notes_seasoned` | Citrus are among the best fruit trees for containers, and a navel on Flying Dragon (a naturally dwarfing trifoliate rootstock) is well suited to a large pot. |
| `mandarin-clementine` | rootstock | `notes_seasoned` | Mandarins are excellent container citrus: the trees are naturally small, and a satsuma on Flying Dragon (a dwarfing trifoliate rootstock) is well suited to a large pot. |
| `grapefruit` | rootstock | `notes_seasoned` | Grapefruit is the largest common citrus, so container growing means a dwarfing rootstock (Flying Dragon) and a genuinely large pot; it is more demanding in a container than a compact lemon. |
| `cherry-sweet` | rootstock | `notes_beginner` | It can be done on a dwarfing rootstock like Gisela 5, but expect more hands-on care, a smaller crop, and more cracking from the wet-dry swings a pot brings. |
| `cherry-sour` | rootstock | `notes_beginner` | It can be done on a dwarfing rootstock like Gisela 5, but expect more hands-on care, a smaller crop, and more cracking from the wet-dry swings a pot brings. |
| `mulberry` | cultivar | `notes_seasoned` | A standard mulberry is far too large and vigorous for containers, so container culture means starting with a genetic-dwarf or weeping cultivar (Dwarf Everbearing and similar), which are bred for pots and bear young. |

Notes on three of them.

- **cherry-sweet, cherry-sour**: the evidence is the BEGINNER sentence, not the seasoned one. The
  seasoned register says "It works on a genetic-dwarf or Gisela 5 tree", which puts a genetic dwarf
  and a rootstock in one clause; the beginner sentence names the dwarfing rootstock alone. Per the
  controller's binding ruling both cherries are decided on **Gisela 5 alone**. The
  "Own-root / genetic dwarf (North Star, Meteor)" `rootstock_options[]` row is a cultivar mis-homed
  in the rootstock array (PLA-464); North Star and Meteor have had NO T1 read, are not the basis of
  either path, and enter no variety list. The promote never edits `rootstock_options[]`, and the
  suite pins that (`test_no_rootstock_entry_changes_anywhere`).
- **cherry-sour** carries the same evidence sentence as cherry-sweet with the crop name swapped;
  they are sibling template registers. Uniqueness is scoped to each crop's own prose block, and both
  were measured at exactly 1 hit.
- **mulberry** is `cultivar`, not `rootstock`: see section 5.

## 2. lemon and lime: both `direct`

The rule (context file, from PLA-463 and the spec's rule 2): `rootstock` ONLY if a note states a pot
is viable only on a dwarfing or trifoliate rootstock; `direct` if the note says the lemon or lime as
commonly sold grows in a pot. Both notes say the second thing.

**lemon: `direct`.**

> Lemons are among the best citrus for containers, and a dwarf-rootstock tree in a large pot is the standard approach for cold-climate growers.

> Lemons grow really well in pots, which is why people in cold areas often keep one.

The dwarf rootstock is named as "the standard approach for cold-climate growers", which is a
recommendation, not a condition of viability. The spec's `direct` row is exactly this case: "the crop
as commonly sold grows in a pot; compact cultivars may do better but are not required."
**The other defensible reading**, written down because it is not silly: the seasoned register's NEXT
sentence says "use a dwarfing or semi-dwarf tree", an imperative in a list of pot instructions, and a
reader could take that as a requirement. It is not phrased as one, no sentence says a standard lemon
fails in a pot, and the conservative call is `direct`.

**lime: `direct`.**

> Limes are excellent container subjects, and for growers outside the mildest zones a large pot is the standard, often the only, way to keep one, because limes are the most cold-tender common citrus.

> Limes grow really well in pots, and for most of the country a pot is the only way to grow one, since limes are the citrus most easily killed by frost.

The only "only" in lime's block is about the POT being the only way to grow the crop in a cold
climate, not about a rootstock. Lime's block names no rootstock at all. `direct`.
("Key lime, being small and bushy, is especially well suited to pots" is a cultivar hint, not a
condition, and lime's `container_suitable_varieties` list is empty, so rule 3 could not join it
anyway.)

Because neither went to `rootstock`, **`EXPECTED_ROOTSTOCK` stays 8** and PLA-7 defect 7 (measured
on the base: lemon has two container-suitable trifoliate entries and lime one, and all three carry
`container_size_gallons: null`) does
not become load-bearing in this promote: no consumer is sent to those entries by a path this promote
writes. It stays owed to Plan A2 / Plan E.


---

## 3. The `cultivar` read: seven crops accepted, and why the near misses were declined

**The test applied, uniformly.** The spec (section 2) defines the two values in a way that decides
this: `direct` is "the crop as commonly sold grows in a pot; compact cultivars may do better but are
not required"; `cultivar` is "a pot is viable ONLY with a compact / bush / patio / genetic-dwarf
cultivar". So a crop becomes `cultivar` only when its own notes ASSERT THE NEGATIVE: that the
full-size or vining form does not work in a pot. "Compact types do better", "are ideal", "are the
container performers", "especially good" are all `direct`.

**How the candidates were found.** The brief's scan regex
(`\b(only|choose|stick to|best on|pick|look for)\b[^.]*\b(compact|bush|patio|dwarf|determinate)\b`
over `notes_seasoned`) returned 13 crops, and IT MISSES REAL CASES: it never reads `notes_beginner`,
and it requires the verb before the size word. It missed watermelon entirely, and it missed the
acorn-squash beginner sentence that is that crop's clearest statement of the condition. The read was
redone as an exhaustive dump of every sentence containing a size word
(`compact|bush|patio|dwarf|determinate|miniature|semi-bush|short-vined|small-fruited|genetic-dwarf|weeping`)
in `notes_seasoned` or `notes_beginner` of every `container_ok` crop with dict variety entries: 47
crops printed and read by hand. The seven accepted below and the declines are that read, not the
regex's.

### Accepted: seven crops move `direct` -> `cultivar`

Each carries an evidence sentence found exactly once in its own prose, and each already has at least
one `varieties.recommended[]` entry that the mechanical migration flags `container_suitable: true`,
so gate rule 3 is satisfied on the post-state (the gate ran with presence ON inside the promote).

| crop | field | evidence (verbatim) | rule 3 join (entries flagged by the migration) |
|---|---|---|---|
| `pumpkin` | `notes_seasoned` | Only miniature, pie, or bush varieties such as Jack Be Little, Baby Bear, or Small Sugar are realistic in a pot, and they still want a big one: at least 10 gallons and 12 inches deep, larger is better. | Baby Bear, Jack Be Little |
| `watermelon` | `notes_beginner` | You can grow a watermelon in a container, but only the small icebox or bush kinds like Sugar Baby or Bush Sugar Baby, since full-size vining watermelons are far too big. | Sugar Baby, Yellow Doll |
| `cantaloupe` | `notes_beginner` | You can grow a cantaloupe in a container, but choose a small, short-vined kind like Minnesota Midget, since full-size vining types are too big. | Minnesota Midget, Sarah's Choice |
| `honeydew-melon` | `notes_seasoned` | It is workable only with the earliest, most compact variety you can find. | Earlidew |
| `butternut-squash` | `notes_beginner` | You can grow butternut in a container, but choose a compact or bush type like Butterbush, since full-size vining butternut is too big for a pot. | Butterbush, Early Butternut, Honeynut |
| `acorn-squash` | `notes_beginner` | Acorn squash grows well in a container if you choose a bush type like Table King or Honey Bear, since full-size vining kinds are too big for a pot. | Honey Bear, Table Ace, Table King |
| `spaghetti-squash` | `notes_beginner` | You can grow spaghetti squash in a container, but choose a compact or bush type like Tivoli or Small Wonder, since full-size vining spaghetti squash is too big for a pot. | Orangetti, Small Wonder, Tivoli |

All seven are large vining cucurbits, and that is not a family rule applied across crops: each was
decided on its own sentence, and the one cucurbit whose notes make the claim in the beginner register
only (acorn-squash) is in the list precisely because the sentence is there. The cucurbits whose notes
do NOT assert the negative are below, declined.

### Declined, with the sentence that declined them

| crop | the sentence read | why `direct` |
|---|---|---|
| `zucchini-courgette` | Zucchini is growable in containers but demands a big one: a 10 gallon or larger pot at least 12 inches deep, and ideally a compact or bush variety such as Raven, Astia, Bush Baby, Patio Star, or Eight Ball rather than a sprawling heirloom. | "ideally", and the beginner's "a compact variety works best", are preference, not requirement. No sentence says a sprawling zucchini fails in a 10 gallon pot. |
| `yellow-summer-squash` | Yellow summer squash is growable in containers but demands a big one: a 10 gallon or larger pot at least 12 inches deep, and ideally a compact or bush variety such as Saffron, Goldbar, Sundance, or Early Prolific Straightneck rather than a large spreading type. | Same template as zucchini, same reading. |
| `okra` | Okra is a workable container crop if you choose a dwarf variety such as Baby Bubba or a compact one like Cajun Delight and give it a big enough pot: at least 5 gallons and 12 inches deep, larger is better, one plant per container. | THE CLOSEST DECLINED CALL. This is the same conditional template as cantaloupe's accepted sentence. It is declined because okra's own note contradicts the exclusivity two sentences later: "Stake a full-size plant against wind." A note that tells you how to stake a FULL-SIZE plant in the pot does not say only a dwarf works. Both readings are recorded; if Trevor reads the conditional as governing, okra is a one-row change plus one pin. |
| `cucumber` | Cucumbers are one of the better container cucurbits, especially compact or bush types such as Spacemaster, Bush Champion, Salad Bush, or Patio Snacker, and the parthenocarpic types that fruit without pollinators suit a balcony well. | "one of the better container cucurbits, especially compact types" is a positive characterization of the crop. The beginner's "if you pick a compact or bush variety" carries no "since full-size is too big" clause. |
| `slicing-cucumber` | Slicing cucumbers are one of the better container cucurbits, especially compact or bush types such as Spacemaster, Bush Champion, or Salad Bush, and the parthenocarpic types that fruit without pollinators suit a balcony well. | Same as cucumber. |
| `pickling-cucumber` | Pickling cucumbers container well when you choose a compact bush type such as Bush Pickle or Pick a Bushel, or a small-fruited gherkin like Parisian Gherkin, and parthenocarpic types that fruit without pollinators suit a balcony. | The sentence offers a NON-compact alternative in the same breath (a small-fruited gherkin, parthenocarpic types), so it is not exclusive to compact or bush types. |
| `english-cucumber` | English cucumbers suit containers particularly well, precisely because the parthenocarpic, gynoecious types fruit without pollinators, which makes a screened balcony, patio, or sunroom a natural fit. | The stated reason the crop suits pots is POLLINATION, not size; "Choose a compact or Beit Alpha type ... over the long sprawling kinds" is a preference expressed as a comparison. |
| `elderberry` | If you must, choose a compact cultivar such as Ranch, use a 20-to-25-gallon pot of rich moisture-holding mix, water generously (elderberry is thirsty and wet-tolerant), and feed regularly; yields will be lower than in the ground and the plant will stay smaller. | The "if you must" governs the CONTAINER, not the cultivar, and the compact cultivar is one item in a list with pot size, water and feed. The note's negative is about yield in a pot, not about which cultivar. |
| `dill` | Standard dill reaches 3 to 5 feet and gets top-heavy, so choose a dwarf, slow-bolting variety such as Fernleaf for pots. | The block opens "Dill grows well in a container at least 10 inches deep to fit its taproot", and the beginner reason is "so it does not get too tall and tippy". Top-heavy is a manageability problem, not an assertion that standard dill fails. |
| `raspberry` | Use a 10-to-15-gallon pot of free-draining, compost-rich mix, choose a compact or fall-bearing cultivar so you can cut canes to the ground each winter, and stake the canes. | The stated purpose of the cultivar choice is PRUNING convenience ("so you can cut canes to the ground"), and the block opens by calling containers a practical way to grow the crop. |
| `blackberry` | Use a 10-to-15-gallon pot of free-draining, compost-rich mix, choose a compact or primocane-fruiting cultivar so you can cut canes back hard each winter, and stake or trellis the canes. | Same as raspberry. |
| `cabbage` | Cabbage is a workable container crop, especially the compact early varieties. | "especially" is preference. |
| `broad-beans-fava` | Dwarf fava varieties such as Robin Hood suit containers best; the common tall types (2 to 4 feet, sometimes taller) are workable in a large, deep, stable pot but tend to lean and need staking. | The note explicitly says the tall types ARE workable in a pot. |
| `bell-pepper` | Compact varieties such as Redskin, Mohawk, and the small-fruited snacking bells perform best, while full-size blocky bells want the larger pot and a small stake. | The note explicitly accommodates full-size bells in a pot. |
| `eggplant` | Compact, container-bred varieties such as Patio Baby and Fairy Tale, and slender Asian types such as Ichiban, perform best; full-size globe types need the larger pot and a stake. | Same shape as bell-pepper: full-size works, in a bigger pot. |
| `sugar-snap-peas` | Bush and semi-dwarf snap pea types suit containers well; tall climbing varieties like Sugar Snap are awkward in pots because of their trellis height. | "awkward" is not "unworkable", and the constraint named is trellis height, which a taller support solves. |
| `snow-peas` | Dwarf and bush snow pea types suit containers well; tall climbing varieties are awkward in pots because of their trellis height. | Same as sugar-snap-peas. |
| `blueberry` | Choose a compact or dwarf cultivar, keep the mix evenly moist, and protect the roots over winter while still meeting the cultivar's chill requirement. | The block opens "Containers are arguably the most reliable way for a first-timer to grow blueberries". ALSO JOIN-BLOCKED: none of its five `container_suitable_varieties` names matches a `varieties.recommended[]` entry, so rule 3 would refuse a `cultivar` row today. |
| `pomegranate` | Choose a genetic-dwarf ('Nana') or a standard cultivar held small by pruning, give it the largest practical free-draining pot (15-plus gallons) and full sun, and keep moisture even through fruiting. | The note itself offers a STANDARD cultivar as an alternative. ALSO JOIN-BLOCKED: no exact-name match among its three names. |
| `echinacea` | Containers suit dwarf and compact selections; full-size types get tall and are happier in the ground. | "happier in the ground" is a preference. ALSO JOIN-BLOCKED: `container_suitable_varieties` is empty and six of its seven variety entries are bare strings. |
| `sweet-potato` | Use a 15 gallon or larger tub or grow bag at least 12 inches deep with drainage holes, filled with a loose, free-draining mix; plant one or two slips of a compact bush variety (Vardaman, bush Porto Rico) and let the vines trail over the sides. | An imperative inside a how-to list, with no negative asserted about other varieties. ALSO JOIN-BLOCKED: `container_suitable_varieties` is empty, so the migration flags nothing to join to. |

Crops whose notes mention a size word purely as a property of the CROP (jalapeno, banana-pepper,
cayenne-pepper, habanero, kale, spinach, swiss-chard, kohlrabi, bok-choy, radish, green-beans-bush,
dry-bean) are `direct` without argument: they say the plant is compact, not that you must buy a
compact one.

## 4. Owed to Plan B: the string-variety crops that would be `cultivar` if they had records

Rule 3 needs a `varieties.recommended[]` DICT entry to flag. These crops store their varieties as
bare strings, so they cannot be `cultivar` in this promote no matter what their notes say. They are
left `direct` and are listed here as owed to **Plan B** (convert the string-variety crops to records,
PLA-290/346 pattern, then re-read).

| crop | the sentence | reading |
|---|---|---|
| `sunflower` | Containers suit dwarf and compact cultivars only; giants are unworkable in pots given their size and top-heaviness. | CLEAR `cultivar` on the text ("only", "unworkable"). Blocked twice over: 8 string entries and an EMPTY `container_suitable_varieties`, so Plan B owes it both a record conversion and a suitable-variety list. |
| `beefsteak-tomato` | If container growing is necessary, use compact or determinate beefsteak-type varieties (Bush Beefsteak, Bush Early Girl) in 15-20 gallon containers with heavy-duty caging. | Conditional `cultivar` on the text; the block opens "Beefsteak tomatoes are generally not well-suited to container growing" and closes "Raised beds are strongly preferred for full-size indeterminate varieties". 4 string entries; its `container_suitable_varieties` (Bush Beefsteak, Bush Early Girl, Patio) would join once converted. |
| `heirloom-tomato` | If container growing is necessary, use compact or determinate heirloom-type varieties (Stupice, Bloody Butcher) in 15-20 gallon containers with heavy-duty caging. | Same template and same reading as beefsteak-tomato. 8 string entries. |

The other string-variety crops were read and do NOT belong on that list, so Plan B inherits no
obligation for them: cherry-tomato ("Determinate or compact varieties (Tumbling Tom, Tiny Tim) are
ideal"), roma-tomato ("full-size determinates work in 10-gallon containers with a cage"),
grape-tomato ("Compact or hanging-basket grape cultivars are scarce, so plan for a tall plant", the
opposite claim), basil (no cultivar condition at all), tomatillo (its container constraint is
obligate cross-pollination, not size), and the flowers marigold, nasturtium, calendula, zinnia,
cosmos, bee-balm and sweet-pea, whose notes say dwarf and compact series "are the container
performers" and in several cases explicitly add that the tall types are workable in large containers.
lettuce-leaf, viola, borage and sweet-alyssum carry no size word in either note at all.

## 5. mulberry: a decision row for Trevor

**What the promote does:** mulberry flips to `container_ok: true`, `min_pot_gallons: 15`,
`container_recommended: false`, `container_path: cultivar`, joined to the **Dwarf Everbearing**
`varieties.recommended[]` entry, which takes `container_suitable: true` and
`container_min_gallons: 15`. This is the spec's ruling and the controller's, recorded in the ledger.

**What PLA-463 says, in tension with it:** PLA-463's Session 2 read says mulberry's `container_ok:
false` "should stand for the same reason plum's does". The spec flips it. Both prose registers state
the condition the flip rests on:

> A standard mulberry is far too large and vigorous for containers, so container culture means starting with a genetic-dwarf or weeping cultivar (Dwarf Everbearing and similar), which are bred for pots and bear young.

> A standard mulberry is far too large and vigorous for a pot, so container growing means choosing a naturally dwarf or weeping variety like Dwarf Everbearing, which is bred for it and even fruits young in a pot.

**The number, stated plainly:** the 15 gallon figure is CARRIED from the existing certified
`rootstock_options[]` entry "Genetic dwarf (e.g. Dwarf Everbearing)", which reads
`container_suitable: true`, `container_size_gallons: 15`, `sources: ["ncsu_ext"]`, anchored at the
NCSU toolbox Illinois Everbearing page (verified 2026-06-30). It was NOT re-read at T1 in this
session. If Trevor wants the flip to rest on a fresh read, that read is a Plan A2 item and the
mulberry rows come out of this promote.

Two mechanical details worth having on the record: mulberry's `container_suitable_varieties` list is
EMPTY, so the Dwarf Everbearing flag comes ENTIRELY from the spec's one explicit `variety_flags` row
(`EXPECTED_FLAGS_EXPLICIT` = 1), not from the mechanical migration; and the variety entry named
"Dwarf Everbearing" already exists in `varieties.recommended[]`, so no variety was added.

**Also honoured:** PLA-463 says do not give mulberry a path FROM THE ROOTSTOCK ARRAY (its
container_notes contain zero leaves mentioning "rootstock"). The path is `cultivar`, joined to the
VARIETY entry, and the mis-homed rootstock entry is left byte-untouched for PLA-463's follow-on.

## 6. plum: HELD, not a flip

plum stays `container_ok: false` with `container_path: null`. PLA-463 verified the Marianna 2624 size
claim against UC ANR, but the `container_suitable: true` and 25 gallon claims, and St. Julien A's
attribution, were NOT verified: that is **PLA-466**, open. The suite pins the hold
(`test_plum_is_untouched`: `container_ok` false, `container_path` null, `rootstock_options`
byte-identical), and `whole_crop_gate plum` on the scratch post-state passes.

## 7. The pins

One pin moved. `EXPECTED_CULTIVAR` / `N_CULTIVAR` / `spec.json`'s `expected.cultivar` went from **1 to
8**, changed in all three files together BEFORE any run, because the read moved seven crops from
`direct` to `cultivar` (section 3). Nothing else moved.

| pin | plan literal | shipped | why |
|---|---|---|---|
| `EXPECTED_ROWS` | 121 | 121 | unchanged |
| `EXPECTED_NON_NULL` | 110 | 110 | unchanged: a row that moves `direct` -> `cultivar` was ALREADY non-null |
| `EXPECTED_NULL` | 11 | 11 | unchanged |
| `EXPECTED_TRAY` | 8 | 8 | unchanged |
| `EXPECTED_ROOTSTOCK` | 8 | 8 | unchanged: lemon and lime both read `direct` (section 2) |
| `EXPECTED_CULTIVAR` | 1 | **8** | mulberry plus the seven crops in section 3 |
| `EXPECTED_FLIPS` | 3 | 3 | unchanged |
| `EXPECTED_FLAGS_MECHANICAL` | 134 | 134 | unchanged |
| `EXPECTED_FLAGS_EXPLICIT` | 1 | 1 | unchanged |
| `EXPECTED_GRAVEL` | 16 | 16 | unchanged |
| `EXPECTED_APPLICABLE` | 12 | 12 | unchanged |
| `EXPECTED_LEAVES` | 294 | 294 | unchanged: the container_path key is ONE leaf per crop whatever its value |

## 8. The suite, and the one driver that had to be fixed

```
$ python3 -m pytest tools/test_promote_pla7_container_path.py -q
.........................................................                [100%]
57 passed in 13.45s
```

57 passed, **0 skipped** (47 of them were skipping on the skeleton, gated behind `need_evidence()`).

**One driver was wrong and had to be fixed** (the suite, never the guard, never a count).
`BlastRadius::test_refuses_a_change_outside_the_two_blocks` set
`P.by_slug(post)["basil"]["description"] = "changed"` and expected the message
`changed outside container_notes/varieties`. basil carries no `description` key (it carries
`description_beginner` and `description_seasoned`), so the driver ADDED a key, which trips the
crop-level KEY SET check one line earlier in `verify_post`, and the guard under test was never
reached:

```
E     wanted: 'changed outside container_notes/varieties'
E     got: 'REFUSED: basil crop-level key set changed'
```

This is the `guard-tests-pass-because-an-earlier-check-fires` pattern, and it surfaced as a hard
FAILURE rather than a green vacuous pass only because `assertRefuses` pins the message. The driver
now mutates `description_beginner`, an EXISTING key, with an `assertIn` that the key is there so a
future rename cannot silently re-vacuum it. The harness then proves the fixed driver is real:
`blast/outside_change_invisible` is caught.

The defect was invisible until this task because the test skipped on the skeleton. That is the
predictable cost of `need_evidence()`, and it is worth writing down: a suite with 47 skipping tests
has not been run.

## 9. The mutation harness

```
anchor preflight: 39/39 anchors match exactly once
positive control: unmutated scratch is GREEN
sentinel: reddened as required

39 injected: 39 caught, 0 survived, 0 broken
```

Zero survivors, zero broken, so no mutation needed a driver fix beyond section 8's (which was found by
the suite run, not by the harness).

**Why 39 and not the plan's 34.** Computed, not asserted: the plan's `MUTATIONS` list carries 34
entries and the shipped harness carries 39; the five extra, by name, are
`drainage_key_set_not_compared`, `overwintering_key_set_not_compared`,
`variety_min_gallons_not_compared`, `flag_not_rederived_from_list` and `unflagged_match_invisible`.
They exist because the Task 5 review found three gaps in `verify_post` and closing them (commit
`5f33a82`: sub-dict key sets compared before their values, `container_min_gallons` compared against
the spec, and the variety migration re-derived independently from the raw
`container_suitable_varieties` list) added five new guard branches, and a new guard family ships with
a mutation or it does not ship (PLA-215). Separately, commit `6efc94d` fixed the `entry` family's
DRIVER: the plan's version asserted the `BASE_SHA` constant and never called `load_canonical`, so the
one mutation in that family could not have been caught by it. That was a driver repair, not a new
mutation, and the family is 1/1 now.

## 10. The gauntlet, on the scratch post-state

```
$ python3 tools/promote_pla7_container_path.py --out <scratch>
  spec shape        121 rows: 110 non-null / 11 null; 8 tray, 8 rootstock, 8 cultivar; 3 flips
  pre-state         121 crops read; no key present; evidence found once; flips false->; 134 exact matches; gravel/applicable sets complete
  post gates        container_path_gate (presence ON) 0; display_readiness + numeric_sanity clean on the flips
  verify post       294 leaves, nothing else

  72371c02 -> d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798
  WROTE post-state to <scratch> (canonical untouched)

$ shasum -a 256 <scratch>
d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798
```

The `--out` SHA equals the `--check` SHA.

**whole_crop_gate on the nine named crops** (last line each):

```
cherry-sweet           GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
cherry-sour            GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
mulberry               GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
apple                  GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
kale                   GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
zucchini-courgette     GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
microgreens-mix        GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
plum                   GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
lettuce-leaf           GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
```

**The roster and the standalone gates:**

```
$ python3 tools/gate_all.py <scratch> | tail -3
gate_all: ran whole_crop_gate on 121 certified crop(s)
gate_all: PASS -- every certified crop passes the whole suite

$ python3 tools/container_path_gate.py <scratch> --presence
container_path_gate: 0 violation(s); 121/128 crops carry the key; presence ARMED

$ python3 tools/register_completeness_gate.py <scratch> | tail -2
GATE: PASS -- 0 unruled prose fields (modulo 6 deferred §5 companions entries).
Every prose field on every crop is ruled-and-converted or ruled-and-deferred.
```

(`gate_all` prints two summary lines, not a `121/121` figure; the count it prints is 121 certified
crops, all passing.)

**release_verify** (`--ref avocado`, `--slug cherry-sweet`, `--expect-changed` = the other 120
certified crops, computed from the live canonical):

```
A. collateral (vs base)
  ok: only the 121 declared crops changed: [... 121 slugs ...]
  top-level(non-crops) changed: [] | catalog +none -none
  ok: reference crop avocado byte-identical
  cherry-sweet regions changed: []
B. violation-diff (vs base)
  ok: no new violations introduced
  cleared: none
Gate (candidate)
  cherry-sweet: GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
  CONCERN: reference avocado not PASS: GATE: 153 VIOLATION(S)
C. calendar coherence (filled cells)
  ok: all filled calendars coherent (no waits; heat_pause aligned)
D. user-facing dash / spelled-degrees scan
  ok: no `--`/em-dash/spelled-degrees in any user-facing string
E. exemplar key-diff (filled cells vs reference)
  CONCERN: northern_tier: novel region keys vs avocado: ['chill_basis_beginner', 'chill_basis_seasoned']
  CONCERN: se_gulf: novel region keys vs avocado: ['chill_basis_beginner', 'chill_basis_seasoned', 'plantings_provenance']
  CONCERN: ca_interior: ... (8 more regions, the same two or three keys)
F. region_notes presence
  ok: every cell with seasoned notes has beginner notes
G. exemplar value-divergence (calendar/heat_pause identity vs avocado)
  review (Step 5.5): value-IDENTICAL to avocado -- attest each as independently-derived, NOT pasted: ['northern_tier.z3.calendar']
H. shared chill-delivered table (region_chill_delivered shape)
  ok: region_chill_delivered is a well-formed region -> zone -> [lo,hi] table

  (1 review note(s) above -- Step 5/5.5 items, NON-blocking)
RELEASE-VERIFY: 11 CONCERN(S) -- block + review before promoting
```

Exit status 1, on **11 concerns, every one of which pre-exists on the live canonical**. Proven, not
assumed, by re-running the identical command with `crops_data_final.json` as the candidate:

```
$ python3 tools/release_verify.py crops_data_final.json --base crops_data_final.json --slug cherry-sweet --ref avocado --expect-changed "<same list>"
A. collateral (vs base)
  CONCERN: crops changed = [] (expected [... the 120 declared ...])
  ...
  CONCERN: reference avocado not PASS: GATE: 153 VIOLATION(S)
  ...
  E: the same ten novel-region-key CONCERNs, identical text
RELEASE-VERIFY: 12 CONCERN(S) -- block + review before promoting
```

The live run reports **12**: the same 11, plus one artifact of running a file against itself (section
A sees nothing changed while 120 crops are declared). **No concern is introduced by this promote.**
Section A on the post-state is the line that matters and it is clean: exactly the 121 declared crops
changed, the reference crop avocado is byte-identical, and nothing outside `crops` moved.

(The `avocado not PASS: 153 VIOLATION(S)` concern is the known shape of an uncertified shell being
used as the byte-identity reference. It is the same 153 on both runs.)

## 11. The A58 positive control

A58's presence floor ships DISARMED (`A58_PRESENCE_ARMED = False`, untouched by this task), so the
control exercises A58's SHAPE rule 1 on a crop that carries the key. A copy of the scratch post-state
with basil's `container_notes.container_path` set to null:

```
$ python3 tools/whole_crop_gate.py basil <copy>
  container-path violations: 1
  VIOLATION: container-path: basil: container_ok is true but container_path is null (rule 1)
GATE: 1 VIOLATION(S)
```

against the unmodified post-state:

```
$ python3 tools/whole_crop_gate.py basil <scratch> | tail -1
GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)
```

The copy was deleted. Note the brief expected the string `GATE: FAIL`; `whole_crop_gate` emits
`GATE: <n> VIOLATION(S)`, which is the same verdict in this tool's wording.

## 12. Rule 2 reads a forward-hook key that no crop carries yet

`container_path_gate`'s rule 2 reads **`rootstock_selection_axis`** and skips the check when the key
is absent (`axis = crop.get("rootstock_selection_axis"); if axis is not None and axis not in
AXIS_PERMITS_ROOTSTOCK`). Measured on the base: **0 of the 19 crops with a non-empty
`rootstock_options[]` carry `rootstock_selection_axis`**, so that clause is inert today and all eight
rootstock rows pass on the container-suitable-entry half of rule 2 alone.

The existing key is the free-text **`rootstock_selection_basis`**, present on 16 of those 19 (absent
on orange-navel, mandarin-clementine and grapefruit) with values such as `size`,
`soil_pest_tolerance`, `disease_cold_soil_tolerance`, `own_root`, `vigor_precocity_and_soil`. The
gate deliberately does NOT read it: PLA-463 locks the axis vocabulary, and pointing rule 2 at a
free-text field would bind the gate to strings PLA-463 is about to replace. **Plan E repoints rule 2
to the locked key** once PLA-463 lands. Recorded here so nobody "fixes" the gate to read `_basis`.

## 13. The Task 8 apply command (NOT run; canonical is untouched)

```bash
python3 tools/promote_pla7_container_path.py --expect-sha d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798
```

Task 8 also flips `A58_PRESENCE_ARMED` to `True` in `tools/whole_crop_gate.py` in the SAME commit as
the canonical write (gates arm off the data), and carries the state trio (`LATEST.txt`,
`STATE_HISTORY.md`, `CURRENT_STATE.md`) plus the `promote_fixture.COMMIT_FOR` pin. It runs only on
Trevor's approval.

## 14. The full tree

```
$ python3 -m pytest tools/ -q 2>&1 | tail -3
FAILED tools/test_bare_host_scan.py::test_self_pathed_population_at_this_canonical
FAILED tools/test_cited_claim_scan.py::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass
2 failed, 5433 passed, 1 skipped in 2738.87s (0:45:38)
```

The two failures are EXACTLY the two the brief names as pre-existing
(`test_bare_host_scan::test_self_pathed_population_at_this_canonical` and
`test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass`), neither
touched by this task and neither reading `container_path`. Nothing new failed, nothing was disabled.
For scale: the PLA-457 prepared-state run on this same canonical recorded 2 failed / 5,347 passed /
1 skipped in 44 minutes; the +86 passed here are this arc's suites (`container_path_gate`'s 29 plus
this promote's 57).

## 15. Follow-ons (from the plan's follow-on list, with what this task adds to each)

- **A2, sourced fills:** the five herb `_seasoned` siblings, the three citrus rootstock gallons, the
  four empty `sources`, the eight `depth_inches_min`, the `container_specific_pests` retire. **This
  task adds:** lemon's and lime's container-suitable trifoliate entries still carry
  `container_size_gallons: null` (PLA-7 defect 7); harmless now that both read `direct`, still owed.
  And mulberry's 15 gallons is carried, not re-read (section 5).
- **B, the variety list:** convert the seven string-variety crops to records, T1-read the 60 unmatched
  cultivar names, then retire `container_suitable_varieties[]` after the two consumers read the flag.
  **This task adds:** sunflower, beefsteak-tomato and heirloom-tomato are `cultivar` on their own
  prose and are blocked only by the string shape (section 4); sunflower additionally needs a
  `container_suitable_varieties` list. Re-read all three when the records land. Also join-blocked for
  a different reason: blueberry (5 names) and pomegranate (3 names) have `container_suitable_varieties`
  names that match NO variety entry, while echinacea and sweet-potato have an EMPTY list, so all four
  would fail rule 3 today even though they carry dict variety entries.
- **C, `plants_per_pot`:** unchanged by this task.
- **D, `critical_warnings` safety class:** unchanged by this task.
- **E, PLA-463 follow-on:** `container_path` for plum, apricot, nectarine, peach, persimmon, pawpaw,
  and the mulberry rootstock-entry retirement. **This task adds:** lemon and lime are DECIDED
  (`direct`), not deferred, so Plan E inherits them only if PLA-463 overrules the read; and Plan E
  owns the rule-2 repoint in section 12.
- **Open for Trevor:** okra (section 3, the closest declined call) and the mulberry decision row
  (section 5).
