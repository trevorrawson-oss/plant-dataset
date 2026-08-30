# PLA-8 -- the `trap_cropping` catalog round: handoff for a parallel session

**You are picking this up cold. This file is the whole brief.** The measurement below is already
done; do not redo the scan. Read `docs/ladder_batch_playbook.md` for the general procedure and
`CLAUDE.md` for the hard rules, then follow this.

Written 2026-08-28 against canonical `be444e25` (batch 10 committed and pushed at `644215b`).

---

## 1. WHY THIS ROUND EXISTS

Trap cropping is planting a sacrificial patch of a MORE preferred host to concentrate a pest,
then destroying that patch before the pest disperses onto the crop. It has no catalog key, and it
has now been the single largest unplaceable piece of advice in **two consecutive batches**
(batch 8's leafy greens, batch 10's brassicas). Every authoring agent in batch 10 flagged it
independently, five of five.

**It is genuinely distinct from every key already in the catalog, and each near-miss is wrong in
a different way:**

| near-miss | why it is not this |
| -- | -- |
| `weed_host_control` | REMOVES plants that host the pest; trap cropping deliberately ADDS one |
| `crop_rotation` | moves the crop in space; trap cropping leaves it and changes what grows beside it |
| `planting_time_avoidance` | moves the crop in time; same objection |
| `garden_sanitation` | the destroy-the-trap step looks like cleanup, but the planting step has no home |
| `beneficial_predators` | attracts a pest's ENEMIES; this attracts the PEST |

**The timing claim is the safety-bearing part.** Destroying the trap before the pest breeds or
disperses is what separates a trap from a nursery: leave it standing and you have raised the
local population and parked it next to the crop. That claim is what needs the T1 read, and it is
the sentence a reader can be harmed by if it is stated loosely.

---

## 2. THE MEASUREMENT (done; reproduce only if you doubt it)

Scan: `trap crop|trap-crop|trap planting|sacrificial`, case-insensitive, over **every string field**
of every problem on all 128 crops. **22 problems on 20 crops.** Three-way split:

> **CORRECTED 2026-08-28 by the session running this round.** The first version of this scan read
> only the eight standard prose fields and reported 20 on 18. The shell and ornamental crops carry
> their prose in `note_beginner` / `note_seasoned` instead, which hid two records --
> **nasturtium/Aphids** and **zinnia/Japanese beetles**, both INVERTED and both textbook trap
> crops, so they are exactly the records a later pass is likeliest to get wrong. Verified
> independently. The exclusion set is **six, not four**; the backfill is unchanged at 10, since
> both are unladdered.

### 2a. BACKFILL -- 10 rungs onto crops whose ladders ALREADY SHIPPED

These are the classic action and need a backfill promote. The `ends:` column is the ladder's
current last rung, which tells you where the new rung goes (trap cropping is CULTURAL, so it
belongs at or near the FRONT of each ladder, not the end).

| crop | problem id | current ladder ends |
| -- | -- | -- |
| arugula | `flea-beetles` | spinosad |
| bok-choy | `flea-beetles` | spinosad |
| bok-choy | `harlequin-bug` | neem_oil |
| cabbage | `harlequin-bug` | pyrethrin |
| cauliflower | `harlequin-bug` | pyrethrin |
| collards | `harlequin-bug` | pyrethrin |
| jalapeno | `flea-beetles` | spinosad |
| kale | `harlequin-bug` | pyrethrin |
| kohlrabi | `harlequin-bug` | pyrethrin |
| turnip | `harlequin-bug` | insecticidal_soap |

### 2b. AUTHORING -- 6 crops not yet laddered; they pick it up for free IF the method exists first

blackberry (Stink bugs), brussels-sprouts (Harlequin bug), cayenne-pepper (Flea beetles),
eggplant (Flea beetles), habanero (Flea beetles), okra (Stink bugs and leaf-footed bugs).

**This is the deadline argument.** brussels-sprouts lands in batch 12 (fall block, imminent).
The other five sit in the peppers / fruiting-veg / berries batches queued right after it. Mint
before those and the backfill stays at 10; mint after and it grows to 16 across four more crop
families.

### 2c. EXCLUDED -- 6 instances that mention trap cropping and MUST NOT get a rung

**These are deliberate refusals, not oversights. Pin them as guards or a later pass will
"finish the job" and ship four wrong rungs.**

1. **radish / `flea-beetles` -- INVERTED.** Its `cause_seasoned` says radish, arugula and mustard
   "are used as trap crops to pull beetles off other vegetables." That explains why radish gets
   hit hard; it is not advice to plant a trap FOR radish. A rung reverses the sentence.
2. **radish / `cabbage-root-maggot` -- A DIFFERENT ACTION.** "A damaged early sowing can act as a
   trap crop if removed promptly" is repurposing a sowing already lost, not establishing a
   sacrificial one.
3. **dill / Parsleyworm -- OPPOSITE INTENT.** "Handpick and relocate the larvae to a sacrificial
   dill." You are moving black swallowtail caterpillars to a spare plant to KEEP THEM ALIVE, on a
   host grown partly for the butterflies.
4. **parsley / Parsleyworm -- same as dill.** "Relocate the larvae to a sacrificial plant... many
   gardeners deliberately grow extra parsley as a swallowtail host."

5. **nasturtium / Aphids -- INVERTED, and the subtlest of the six.** "Aphids strongly prefer
   nasturtium, which is the basis of its trap-crop use. On a trap stand, monitor and pull or
   destroy the planting once it is heavily loaded." That destroy-when-loaded instruction READS
   exactly like the method, but it describes what you do when nasturtium IS the trap. This dataset
   carries nasturtium as an ornamental and edible crop, where the same prose says to treat aphids
   normally. A rung here tells a reader to destroy the crop they are growing.
6. **zinnia / Japanese beetles -- INVERTED.** "Zinnias are a known preferred host, which is part of
   their trap-crop value." Again the crop is the trap; the record's own advice is handpicking at
   dawn.

A method whose meaning ends in "then destroy the trap" is actively wrong on 3 and 4, and points at
the wrong plant entirely on 5 and 6.

---

## 3. WHAT TO BUILD

### Step 1: the T1 read
Every new method needs a real document, fetched and READ (playbook section 6). The claim that
must be anchored is the **destroy-before-dispersal timing**, not merely that trap cropping
exists. Candidate sources already in `source_catalog` and already T1: `clemson_hgic` (its cole
crop factsheets carry the harlequin bug trap-crop advice verbatim), `umn_ext`, `ncsu_ext`,
`uwi_hort`. Use `tools/ucipm_uaidb.py` only if you end up citing UC IPM's ingredient database,
which is unlikely here since this is cultural, not chemical.

**Do not mint a method you cannot anchor.** `container_culture` is still owed precisely because
its intended anchor turned out to say nothing about containers.

### Step 2: the method entry
Tier `cultural`. `applies_to` must span the pest families measured above: flea beetles
(`insect_chewing`), harlequin bug and stink bugs (`insect_general`). Write `best_use` so it is
DISTINCT from `weed_host_control` and `crop_rotation` in as many words -- the batch-10 mint
(`pyrethrin`) does this against `pyrethroid` and is the model to copy. State the destroy-the-trap
timing in the cautions, since that is the part that backfires.

### Step 3: two promotes, or one -- your call, but keep the blast radii separate in the guards
The precedent for exactly this shape is the chlorothalonil backfill: `d096415` minted the method,
`2e86279` backfilled 9 rungs onto 6 certified crops. Copy that pairing.

Non-negotiables (each exists because it was violated once):
- One `serialize()`, used by the promote and its suite.
- `post` replayed from `promote_fixture.pre_state(BASE_SHA)`, never live canonical.
- `assert set(pre) == set(post)` BEFORE any value comparison.
- **Mutation harness, PLA-215 bar**: anchor preflight, positive control, sentinel that must
  redden, one mutation per guard family. Write the `VerifyPostIsDriven` class FIRST -- it is why
  the last four batches went zero-survivor on the first run.
- **Do not compute a guard's expected value from the thing it validates.** Batch 10 shipped with
  `MINT = staged_mint()["entry"]`, which made the drift check vacuous by construction; the
  harness caught it. Inline the entry as a literal.
- Guards must pin the four EXCLUSIONS by name, in both directions: absent from the backfill, and
  refused if a later pass adds them.

---

## 4. THE SHA COLLISION PROTOCOL (read this before promoting)

The main session is running batches 11 and 12 against the same canonical. **Authoring and reading
parallelize; promotes do not.** Every promote pins `BASE_SHA` and its suite pins `POST_SHA`.

- Whoever promotes FIRST wins. Announce it.
- Whoever promotes SECOND must: re-pin `BASE_SHA` to the new canonical, re-run the promote to get
  a fresh `POST_SHA`, update the suite, and **re-run the mutation harness** (not just the tests).
  Budget ~15 minutes. It is mechanical, not risky.
- Register every landed SHA in `promote_fixture.COMMIT_FOR` immediately after committing, or the
  next suite cannot rebuild its fixture.
- **Never amend a commit that COMMIT_FOR pins.**

Also: a new roster-wide gate armed before its data lands floods the OTHER session's gauntlet.
If you add one, keep it dormant until the backfill is committed.

---

## 5. STATE AT HANDOFF

- Canonical `be444e25`, pushed through `644215b`. Roster **46 of 121 laddered**, catalog **58
  methods**.
- Fall block is 13 of 20 crops done. Batch 11 (garlic, spring-onion, dill, cilantro-coriander)
  and batch 12 (broad-beans-fava, brussels-sprouts, parsley) remain, and the main session is
  taking them.
- **plant-app owes ONE `build:guides` regen** against the final canonical once the block is done;
  every dataset commit so far carries a recorded `--no-verify` E1 bypass for that reason. Do not
  run it yourself (`plant-astro-bump-owned-by-astro-session`).
- Trevor confirms every commit and every push. Do not push without asking.
