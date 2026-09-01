# BATCH 20 (berries) -- PINNED PROBLEM IDS

**Settled BEFORE fan-out. Use the id in this table. Do NOT derive one from the problem name.**

A `pests[]`/`diseases[]` `id` is a join key for `varieties[].resistance` and `ladder_delta`. Two
consecutive batches (17, 19) got ZERO id drift by pinning first. `ladder_batch merge` CANNOT enforce
this: these 39 problems carry no `id` at all, so the id-stability rule has nothing to compare
against.

Base `50bc203f`. 4 crops, 39 problems. **All 39 also carry NO `type`** -- so unlike batch 19, every
type must be SET (insect / mite / mollusk / fungal / bacterial / viral / physiological / nematode /
vertebrate), not preserved.

## A. REUSE an existing roster id

| problem name | crops | id | note |
|---|---|---|---|
| Spotted-wing drosophila (SWD) | blackberry, blueberry, raspberry | `spotted-wing-drosophila` | **NAME VARIANT.** The anchor is strawberry and cherry-sour, whose problem is named "Spotted wing drosophila" (no hyphen, no parenthetical). A name-derived slug diverges from a live key. |
| Spotted-wing drosophila and sap beetles | elderberry | `spotted-wing-drosophila` | Same reuse. **AUTHOR: check this.** The name is a COMPOSITE of two families. If the record treats sap beetles as co-equal rather than secondary, say so in your report and I will re-adjudicate; do not mint on your own. |
| Birds | blueberry, elderberry | `birds` | anchored on strawberry, cherry-sour, cherry-sweet |
| Scale insects | blueberry | `scale-insects` | anchored on the five citrus |
| Aphids | all four | `aphids` | see the ruling in section C |
| Powdery mildew | elderberry | `powdery-mildew` | broad group, many holders |
| Japanese beetle / Japanese beetles | blackberry, raspberry, elderberry | `japanese-beetles` | **PLURAL. See the roster defect in section D.** |

## B. MINT NEW -- and anthracnose is a THREE-WAY taxon trap

| problem | crops | id |
|---|---|---|
| Anthracnose | blackberry, raspberry | `cane-anthracnose` |
| Anthracnose (ripe rot) | blueberry | `blueberry-ripe-rot` |
| Phytophthora root rot | blackberry, blueberry, raspberry | `phytophthora-root-rot` |
| Cane and spur blight / Cane blight and spur blight | blackberry, raspberry | `cane-blight` |
| Orange rust | blackberry, raspberry | `orange-rust` |
| Raspberry crown borer | blackberry, raspberry | `raspberry-crown-borer` |
| Red-necked cane borer | blackberry | `red-necked-cane-borer` |
| Raspberry cane borer | raspberry | `raspberry-cane-borer` |
| Stink bugs | blackberry | `stink-bugs` |
| Rosette (double blossom) | blackberry | `rosette-double-blossom` |
| Raspberry mosaic virus complex | raspberry | `raspberry-mosaic-virus` |
| Blueberry maggot | blueberry | `blueberry-maggot` |
| Mummy berry | blueberry | `mummy-berry` |
| Botrytis blossom blight (gray mold) | blueberry | `botrytis-blossom-blight` |
| Stem blight and twig dieback | blueberry | `stem-blight` |
| Elder shoot and stem borers | elderberry | `elder-borers` |
| Elderberry rust | elderberry | `elderberry-rust` |
| Cane canker and dieback | elderberry | `cane-canker-dieback` |

### THE ANTHRACNOSE TRAP -- do NOT take the generic `anthracnose`

The roster's `anthracnose` sits on 14 vegetable crops. Read the organisms:

* **cucumber (the generic)**: *"A fungus (**Colletotrichum orbiculare**)..."*
* **blackberry and raspberry**: *"The fungus **Elsinoe veneta** (anthracnose), which overwinters on
  old canes..."* -- **a different GENUS.** Ships `cane-anthracnose`.
* **blueberry**: *"The fungus **Colletotrichum** (anthracnose), which infects during bloom... shows
  up as fruit rot at ripening"* -- same genus as the generic, different species and a different
  disease (a ripe fruit rot, not a foliar/fruit spot of cucurbits). Batch 19 already refused merging
  two *Colletotrichum* species on lime. Ships `blueberry-ripe-rot`.

One common name, three organisms. This is the `brown-rot` shape (*Monilinia* vs *Phytophthora*) and
the `pea-weevil` shape, but three-way.

### `phytophthora-root-rot` is NEW and is NOT `phytophthora-foot-rot`

Citrus carries `phytophthora-foot-rot` (trunk and crown, gummosis). The berry problem is a ROOT rot
on a different host with different controls. Same genus, different problem: the same reasoning that
kept orange-navel's `citrus-brown-rot` separate from its own `phytophthora-foot-rot`.

## C. RULING: `aphids`, the generic, IS correct here

Batch 18 and 19 REFUSED the generic for citrus, because those records describe a specific
CTV-vectoring complex. The berry records do not:

* blackberry: *"**Several aphid species** feed on blackberry sap and can transmit the viruses..."*
* blueberry: *"**Several aphid species** feed on blueberry sap..."*
* elderberry: *"**Several aphid species** feed on elderberry sap..."*
* raspberry: *"**Several aphid species** feed on raspberry sap; the large raspberry aphid **in
  particular** transmits the mosaic virus complex..."*

All four name a generic complex as the SUBJECT, which is exactly what the generic id means.
Raspberry calls out one species "in particular" WITHIN that complex; that is a detail for the rung
prose, not a redefinition of the problem. Reusing the generic here is the record-driven call, and
refusing it would be splitting on a distinction the records do not draw.

## D. A PRE-EXISTING ROSTER DEFECT, FILED -- two ids for one organism

**`japanese-beetle` (singular) is on basil. `japanese-beetles` (plural) is on marigold, zinnia and
echinacea.** Same insect (*Popillia japonica*), two join keys, already live before this batch.

blackberry and raspberry name "Japanese beetle" (singular); elderberry names "Japanese beetles"
(plural). Letting the name decide would perpetuate the split and put a third crop on each side.

**RULED: all three berries take `japanese-beetles`**, the plural, which has three holders and matches
the roster's convention for insect groups (`aphids`, `birds`, `scale-insects`, `stink-bugs`).
**basil's singular `japanese-beetle` is FILED as a defect needing a repoint** -- not fixed here,
because it is outside this batch's blast radius and a repoint is its own change.

## E. Count check (COMPUTED -- and the hand count was wrong again)

| bucket | problem instances | distinct ids |
|---|---|---|
| A reuse | 15 | 6 |
| B mint | 24 | 18 |
| **total** | **39** | **24** |

Nothing is unclassified.

Note that six distinct reused ids cover EIGHT problem-name keys, because two organisms are named two
ways across these crops: `Spotted-wing drosophila (SWD)` / `Spotted-wing drosophila and sap beetles`
both resolve to `spotted-wing-drosophila`, and `Japanese beetle` / `Japanese beetles` both resolve to
`japanese-beetles`. **That collapse is the whole point of pinning** -- it is exactly where a
name-derived slug would have split a live join key.

**The first draft of this section said 13 reuse / 26 mint / 25 distinct. All three were wrong.**
Batch 19's hand count was also wrong twice, in a way that still summed to the right total because
two errors cancelled. That is now a measured pattern, not an anecdote: **never hand-add these
buckets -- compute them, and put the computed table in the file.**
