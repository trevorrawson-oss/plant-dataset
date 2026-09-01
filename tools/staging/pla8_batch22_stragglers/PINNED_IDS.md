# BATCH 22 (stragglers) -- PINNED PROBLEM IDS

**Settled BEFORE fan-out.** Base `fabdaae1` (batch 21). 3 crops, 26 problems.
english-cucumber, edamame, pumpkin: the three crops left over from families already laddered.

## 0. THE PREMISE, MEASURED. IT IS DIFFERENT AGAIN.

**Schema: FULL** (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`, `sources`,
`anchoring_urls`). This is the batch 17-20 shape, NOT batch 21's note schema. Do not carry batch
21's premise forward.

**Type: SPLIT BY CROP -- a fifth distinct situation in six batches.**

| crop | pre-state types |
|---|---|
| english-cucumber | all `None` (9) |
| pumpkin | all `None` (8) |
| edamame | **all COARSE**: `pest` x5, `disease` x4 |

So the type rule here is two-sided by crop: SET from nothing on two crops, UPGRADE from coarse on
the third. For the record, the six batches have needed five different type rules:

| batch | premise |
|---|---|
| 17 | uniformly coarse -> upgrade |
| 18 | mixed fine/coarse -> two-sided |
| 19 | uniformly fine -> preserve, no change permitted |
| 20, 21 | no type at all -> set from nothing |
| **22** | **split by crop: two set-from-nothing, one upgrade** |

**The type field is genuinely heterogeneous across this roster. Measure it every time.**

## 1. THE PINNING METHOD THAT FOUND THESE (fixed after batch 21)

Batch 21's pin table had three wrong entries because the scan (a) collapsed each problem name to its
alphabetically-first id, hiding the eight roster names that carry more than one, and (b) searched
only by NAME, so it could not see an id whose holder names the problem differently.

Both halves are fixed here, and both halves caught something:

**(a) Not collapsing multi-id names** surfaced three:

| problem | ids the name carries | taken |
|---|---|---|
| `Aphids` (english-cucumber, pumpkin) | `aphids`(54), `apricot-aphids`(1), `citrus-aphids`(5) | `aphids` |
| `Japanese beetle` (edamame) | `japanese-beetle`(1), `japanese-beetles`(6) | **plural**, per the standing ruling |
| `Bacterial wilt` (pumpkin) | `bacterial-wilt`(10), `southern-bacterial-wilt`(1) | **`bacterial-wilt`** -- see section 3 |

**(b) Checking each intended MINT against the roster by ID** turned three more "new" problems into
reuses:

| problem | I would have minted | actually lives on |
|---|---|---|
| `Two-spotted spider mites` (english-cucumber) | a new id | **`two-spotted-spider-mite`** (4 crops; the name is plural, the id singular) |
| `Gray mold` (english-cucumber) | a new id | **`gray-mold`** (4 crops; no crop names it exactly "Gray mold") |
| `White mold (Sclerotinia stem rot)` (edamame) | a new id | **`white-mold`** (3 bean crops; same organism, *Sclerotinia sclerotiorum*) |

Six ids that a name-only scan would have gotten wrong, in one batch.

## 2. THE TABLE

### REUSE

| problem | crop | id |
|---|---|---|
| Aphids | english-cucumber, pumpkin | `aphids` |
| Whiteflies | english-cucumber | `whiteflies` |
| Cucumber beetles | english-cucumber, pumpkin | `cucumber-beetles` |
| Powdery mildew | english-cucumber, pumpkin | `powdery-mildew` |
| Downy mildew | english-cucumber, edamame, pumpkin | `downy-mildew` |
| Gummy stem blight | english-cucumber | `gummy-stem-blight` |
| Two-spotted spider mites | english-cucumber | `two-spotted-spider-mite` |
| Gray mold | english-cucumber | `gray-mold` |
| Bean leaf beetle | edamame | `bean-leaf-beetle` |
| Stink bugs | edamame | `stink-bugs` |
| Japanese beetle | edamame | `japanese-beetles` |
| Two-spotted spider mite | edamame | `two-spotted-spider-mite` |
| White mold (Sclerotinia stem rot) | edamame | `white-mold` |
| Squash vine borer | pumpkin | `squash-vine-borer` |
| Squash bug | pumpkin | `squash-bug` |
| Bacterial wilt | pumpkin | `bacterial-wilt` |
| Phytophthora blight | pumpkin | `phytophthora-blight` |

### MINT -- only four, and all four were id-checked against the roster

| problem | crop | id |
|---|---|---|
| Cucumber mosaic virus | english-cucumber | `cucumber-mosaic-virus` |
| Soybean aphid | edamame | `soybean-aphid` |
| Bacterial blight | edamame | `bacterial-blight` |
| Soybean cyst nematode | edamame | `soybean-cyst-nematode` |

## 3. `bacterial-wilt` on pumpkin IS correct -- the mirror of batch 21's trap

Batch 21 refused `bacterial-wilt` for nasturtium because nasturtium's is *Ralstonia* (soilborne,
rotate away) while the roster id is *Erwinia tracheiphila* (survives inside cucumber beetles).

**Pumpkin is a cucurbit.** Its bacterial wilt IS the *Erwinia*, beetle-vectored disease the id was
minted for, and pumpkin also carries `cucumber-beetles` as its own problem. So the same id that was
a trap one batch ago is the correct reuse here. **The organism decides, never the name and never the
previous batch's ruling.**

## 4. `soybean-aphid` is a MINT even though `aphids` exists

Edamame carries BOTH a generic `Aphids`-shaped problem and a named `Soybean aphid`. *Aphis glycines*
is a specific species with its own biology (an overwintering buckthorn host), and edamame's record
names it. Batch 21 ruled that a generic complex takes the generic id; the converse holds here -- a
record naming ONE species takes its own id. Note edamame has no generic aphid problem, so there is
no within-crop collision.

## 5. Count check -- COMPUTED, appended below by the tool, never hand-added

| bucket | instances | distinct ids |
|---|---|---|
| A reuse | 22 | 16 |
| B mint | 4 | 4 |
| **total** | **26** | **20** |

Unclassified: none
