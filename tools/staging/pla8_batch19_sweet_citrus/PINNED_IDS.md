# BATCH 19 (sweet citrus) -- PINNED PROBLEM IDS

**Settled BEFORE fan-out. An authoring agent MUST use the id in this table and MUST NOT derive one
from the problem name.** A `pests[]`/`diseases[]` `id` is a join key: `varieties[].resistance` and
`varieties[].ladder_delta` point at it, so a regenerated id silently orphans every grade hanging
off it. Batch 17 pinned ids pre-fan-out and got ZERO drift; batch 13 did not and all five agents
minted the same wrong bacterial id (convergence is not correctness).

Base: `514903db` (batch 18, acid citrus). 32 problems across grapefruit / mandarin-clementine /
orange-navel.

## A. REUSE -- 20 problems, exact-name matches with acid citrus. Take the id, do not re-derive.

| problem name (sweet citrus) | id | crops |
|---|---|---|
| Scale insects | `scale-insects` | grapefruit, mandarin-clementine, orange-navel |
| Aphids | `citrus-aphids` | grapefruit, mandarin-clementine, orange-navel |
| Citrus leafminer | `citrus-leafminer` | grapefruit, mandarin-clementine, orange-navel |
| Phytophthora foot rot, root rot, and gummosis | `phytophthora-foot-rot` | all three |
| Greasy spot | `greasy-spot` | all three |
| Citrus canker | `citrus-canker` | grapefruit, orange-navel |
| Sooty mold | `sooty-mold` | grapefruit, orange-navel |

## B. REUSE ACROSS A NAME VARIANT -- 6 problems. THE NAME DIFFERS; THE ORGANISM DOES NOT.

These are the dangerous ones: a slug derived from the name would MISS the existing key.

| problem name (sweet citrus) | acid-citrus name | id | why |
|---|---|---|---|
| Asian citrus psyllid | Asian citrus psyllid **(ACP)** | `asian-citrus-psyllid` | same insect; the acid-citrus name carries a parenthetical the sweet-citrus one drops |
| Huanglongbing **(citrus greening, HLB)** | Huanglongbing **(HLB, citrus greening)** | `huanglongbing` | **the parentheses are REORDERED.** A name-derived slug diverges here |

## C. MINT NEW -- and one of these is a taxon trap

| problem | crop | id | organism, per the record's own `cause_seasoned` |
|---|---|---|---|
| Melanose | grapefruit | `melanose` | *Diaporthe citri* |
| Alternaria brown spot | mandarin-clementine | `alternaria-brown-spot` | tangerine pathotype of *Alternaria alternata* |
| Katydids and fruit-surface chewers | orange-navel | `katydids` | katydids + occasional chewers, sporadic |
| Brown rot of fruit | orange-navel | `citrus-brown-rot` | **see the trap below** |

### THE TRAP: `brown-rot` MUST NOT BE REUSED HERE

`brown-rot` already exists on the roster, minted by batch 17 on six stone fruit. Its organism, per
peach's own record: *"The fungus **Monilinia fructicola**. It overwinters in mummified fruit..."*

orange-navel's "Brown rot of fruit", per its own record: *"Soil-borne **Phytophthora** species
splash onto low fruit during rain, infecting the rind... **the same water molds that cause foot rot**
are responsible here, attacking fruit instead of trunk."*

A true fungus versus an oomycete. Same common name, unrelated organisms -- the `pea-weevil` shape
(*Bruchus pisorum* vs *Sitona*). Reusing `brown-rot` would merge them and make any future
resistance grade meaningless. **Mint `citrus-brown-rot`.**

It must ALSO not reuse `phytophthora-foot-rot`, even though the record says it is the same organism:
different organ, different symptoms, different controls (skirt pruning and fruit clearance versus
drainage and rootstock). Same pathogen, different problem.

## D. THE ONE REAL ADJUDICATION: the mites do NOT collapse into `citrus-mites`

Acid citrus carries ONE composite mite id, `citrus-mites`, and both records say so explicitly:

* lemon: *"**Several mite species** feed by puncturing leaf cells."*
* lime: *"**Several mite species** feed by puncturing leaf and rind cells."*

Sweet citrus does not. It splits them into single-species entries on different crops, and the
records assert the distinction:

* grapefruit, **Citrus rust mite**: *"The rust mite builds up on **the rind**... Warm, humid
  conditions favor it, which is why **the Southeast** sees far more russeting than the arid West."*
  (*Phyllocoptruta oleivora*, an eriophyid; rind russeting.)
* mandarin-clementine + orange-navel, **Citrus red mite**: *"Citrus red mite thrives in **heat and
  dust**... Dusty roadside trees and trees sprayed with broad-spectrum insecticides, which remove
  **predatory mites**, are the most prone."* (*Panonychus citri*, a tetranychid; foliage stippling.)

Different family, different organ, different regional driver, different monitoring. **RULED: mint
`citrus-rust-mite` (grapefruit) and `citrus-red-mite` (mandarin-clementine, orange-navel).**

Rationale: the id is a join key for `varieties[].resistance`, and a variety resistant to red mite is
not thereby resistant to rust mite. Collapsing them under the composite would make a future
resistance grade ambiguous in a way no gate could detect.

**`citrus-mites` on lemon and lime is NOT retro-split.** Those records are genuinely composite
("several mite species"), the id was pinned at first authoring one commit ago, and CLAUDE.md forbids
re-deriving it. Citrus therefore carries three mite ids, which reflects what the records say rather
than a tidier model. This is a per-batch call on these records, **not a precedent** -- the batch 16
`sweet-pea` ruling has the same shape.

## E. Count check (recomputed programmatically -- the first hand count was wrong twice)

Counted as PROBLEM INSTANCES, which is what the promote's arity check sees:

| bucket | instances | distinct ids |
|---|---|---|
| A exact-name reuse | 19 | 7 |
| B variant reuse | 6 | 2 |
| C new mint | 4 | 4 |
| D mite mint | 3 | 2 |
| **total** | **32** | **15** |

So **9 ids are reused and 6 are newly minted**, over 32 problems. Every problem classifies; there
is no residue. Any agent producing an id outside this table is a defect, and the promote will pin
the table.

(The first pass of this file said 20 in bucket A and 2 in bucket D. Both were wrong, and the total
still came to 32, which is exactly how a bad count survives a sanity check -- two errors that
cancel. Recomputed from the data, not re-added by hand.)
