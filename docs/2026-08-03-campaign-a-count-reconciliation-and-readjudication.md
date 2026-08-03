# Campaign A — the count reconciliation, and what re-verification did to the worklist

**Run:** 2026-08-03. **Canonical:** `38a579d4…` (verified: `shasum` == `LATEST.txt`).
**HEAD:** `84c7eb2` on `main` (kickoff 50 itself, one ahead of origin).
**Canonical was NOT modified.** This pass is measurement + adjudication.

Kickoff 50 made two things gating: reconcile the count before hunting, and re-verify any record
before acting on it. Both fired, and both changed the campaign.

---

## 1. The count reconciliation — the shipped tool is RIGHT

Kickoff 50 §2 flagged a conflict: `citation_provenance_scan.py --decisions` gives **167 decisions
over 32 hunts** with the California block at **76 over 8**, while an independent hand traversal in
the same session gave **77 over 7**, disagreeing sharply on two rows (`ca_desert`/`uc_mg` 2 vs 8;
`ca_south_coast`/`ucanr_ext` 21 vs 10).

**Resolved: the shipped tool is correct. There is no bug to fix in it.**

An independent re-derivation written this session — walking the canonical from scratch, *not*
importing the scan — reproduces the tool exactly: 614 SOLE pairs, 414 SOLE nodes, **167 decisions,
32 hunts**, and the California block at **76** with the identical per-hunt split
(11/10/10/10/9/9/9/8). Two further checks:

- **`region_of()` has zero attribution errors.** Its regex `regions\.([a-z0-9_]+)\.` was compared
  against a structurally-determined region (which key of `regions{}` the node descends from) on
  every node carrying `anchoring_urls`. **0 disagreements.** The `<crop-level>` bucket is genuine
  crop-level nodes, not mis-parsed region roots.
- **The SOLE definition is the right one.** The tool asks *"is every source cited at this node a
  bare host?"* The hand rule asked *"does this node's `sources` list have exactly one entry?"*

### Why the hand rule is not just different but wrong

The canonical shape that decides it: `acorn-squash.regions.ca_desert.plantings[0]` carries
`anchoring_urls` for **both** `ucanr_ext` (`https://ucanr.edu`) and `uc_mg` (`https://mg.ucanr.edu`)
— two sources, **both domain roots**. A `len(sources) == 1` rule calls that cell *sourced* because
it names two things. It names two useless things; the claim still rests on nothing citable. The
tool's definition is the one that answers the arc's actual question.

### The hand traversal's error mechanism, reproduced

The hand rule was applied to the **region root's** `sources` list, whose value most child nodes
inherit (`plantings[]` nodes carry `anchoring_urls` but **no `sources` key of their own** — measured:
61 such nodes in the CA block alone). Counting crops whose CA region root lists exactly one source
reproduces the hand traversal's three distinctive signatures that no other rule does:

| signature | hand traversal | region-root rule | tool |
|---|---|---|---|
| hunt count | **7** | **7** | 8 |
| `ca_desert`/`uc_mg` | **2** | **2** | 8 |
| `ca_interior`/`uc_mg` | *absent* | *absent* | 9 |
| `ca_south_coast`/`ucanr_ext` | 21 | 19 | 10 |

`ca_interior`/`uc_mg` vanishes because **no** `ca_interior` region root lists `uc_mg` alone — that is
the missing 8th hunt. (The node-level variant of the same rule gives 108/8, also not a match; the
residual 69-vs-77 gap is the two rules partially unioned. The mechanism is settled regardless.)

**Verdict: use `citation_provenance_scan.py`. 167 / 32 live, 158 / 28 genuinely open.** The ledger's
numbers stand unchanged.

---

## 2. Re-verification — TWO of kickoff 50's FOUR authoring decisions are already closed

CLAUDE.md's standing rule fired exactly as written. Kickoff 50 §3 inherits a table of "4 authoring
decisions, 3 of which already have answers" from the 2026-07-29 pass. Re-measured against **current**
canonical:

| # | shape | kickoff 50 says | actual state on `38a579d4` |
|---|---|---|---|
| 1 | winter-squash desert 2nd planting (9 cells) | "citation defect, data defensible — repoint at AZ1005" | **CLOSED BY RULING.** `ca_desert_fall_cycle_provenance_gap`, status **accepted** |
| 2 | pumpkin desert (5 cells) `Jan 15 - Feb 15` — **"the one real DATA-defect candidate"** | unsupported by UC and AZ1005 alike | **CLOSED BY EDIT.** `pumpkin_desert_spring_march_rederivation`, status **resolved**. The cells now read **`Mar 1 - Mar 15`** — the quoted value no longer exists |
| 3 | okra desert (3 cells) | "citation defect, data defensible" | **LIVE.** z10/z11 `Mar 1 - Apr 30`, z9 `Mar 15 - Apr 30` |
| 4 | okra north coast z9 (1 cell) | "not independently checked" | **LIVE.** `Jun 1 - Jun 30` |

**So the risk in this block is 2 authoring decisions, not 4 — and both are okra.**

Two consequences worth stating plainly, because acting on the kickoff as written would have cost
real work:

- **Shape 2 was the block's headline data-defect and it is gone.** `Jan 15 - Feb 15` was corrected
  twice (to `Feb 1 - Mar 1`, then re-derived to `Mar 1 - Mar 15`) and the finding recording it is
  marked `resolved`. This is [[stale-records-commission-phantom-work]] repeating: kickoff 50 quotes a
  value two revisions stale, exactly as kickoff 48's finding 21 did.
- **Shape 1's ruling explicitly REFUSES the move kickoff 50 recommends.** The accepted finding's
  basis reads: *"AZ1005 is cited here as a CLIMATIC ANALOGUE for the Sonoran low desert, explicitly
  NOT as a California source — trimming a Californian window to its marks would be the geography
  stretch the arc warns about."* Kickoff 50 §3 row 1 proposes AZ1005 as the repoint target. Acting on
  it would have redone work already ruled against, and committed the trap by name.

---

## 3. The re-adjudication — 92 windows against the table, read today

The UC table was re-fetched from raw bytes this session (`urllib`, 71,434 bytes, parsed by HTML
structure with a rectangularity assertion — never a WebFetch markdown parse, per
[[webfetch-markdown-table-column-shift]]). **33 rows × 6 columns, rectangular.** The region
definitions and the "planting dates are only approximate" caveat are byte-identical to the
2026-07-29 transcription, so the document has not moved.

| verdict | 2026-07-29 | **today** |
|---|---|---|
| SUPPORTED | 39 | **48** |
| DIVERGENT | 35 | **28** |
| CONTRADICTED | 18 | **16** |
| *(NO UC ROW — not previously counted)* | — | *12 decisions* |

The 16 contradicted cells are **four shapes, and twelve of the cells are already ruled**:

| shape | cells | status |
|---|---|---|
| winter squash (acorn/butternut/spaghetti) `ca_desert` 2nd planting `Jul 1 - Jul 31` vs UC `Feb-March; Aug` | 9 | ruled — `ca_desert_fall_cycle_provenance_gap` |
| pumpkin `ca_desert` 2nd planting `Jul 1 - Jul 31` vs UC `March-June` | 3 | ruled — same finding, which names pumpkin explicitly |
| okra `ca_desert` main `Mar 1 - Apr 30` / `Mar 15 - Apr 30` vs UC `May` | 3 | **LIVE** |
| okra `ca_north_coast` z9 `Jun 1 - Jun 30` vs UC `May` | 1 | **LIVE** |

---

## 4. What campaign A actually is

**76 decisions, and they are three classes, not one:**

| class | decisions | what it means |
|---|---|---|
| **CASE 1 — clean repoint** | **52** | every zone of that (crop, region) is SUPPORTED or DIVERGENT against the UC table. The pathed table genuinely supports the claim |
| **BLOCKED by a contradiction** | **12** | 8 on the ruled cucurbit fall-cycle gap, 4 on the two live okra decisions |
| **NO UC ROW** | **12** | the table cannot source these at all |

### The 12 with no UC row are the `vce_426_331` shape again

`https://ucanr.edu/…/time-planting` is **Table 13.2, a VEGETABLE table** — its 33 rows are
artichoke through watermelons. Six of campaign A's 14 crops have no row in it:

| crop | decisions | why the table cannot serve it |
|---|---|---|
| `lemon` | 4 | citrus |
| `lime` | 3 | citrus |
| `pear-asian`, `pear-european` | 1 each | tree fruit |
| `arugula` | 2 | no arugula row in Table 13.2 |
| `edamame` | 1 | soybean; `beans, snap` is *Phaseolus*, a different crop |

This is the pattern the ledger already flags for campaign D — *a tree fruit or citrus claim paired
with a vegetable planting guide*. It is live inside campaign A too, and it was not visible when the
block was priced as "one document, four regions, two source ids." **Expect CASE 2 on most of these
12.** Note `lemon` and `lime` overlap the campaign D lemon cluster, so they should be worked with it
rather than twice.

### The clean 52, by hunt

| region | `ucanr_ext` | `uc_mg` |
|---|---|---|
| `ca_interior` | 8 | 8 |
| `ca_south_coast` | 8 | 8 |
| `ca_north_coast` | 7 | 7 |
| `ca_desert` | 3 | 3 |

The eight crops these cover are acorn-squash, butternut-squash, spaghetti-squash, pumpkin,
cantaloupe, honeydew-melon, watermelon, okra.

**The repoint target is pre-adjudicated and already recorded in the data.** The basis of
`pumpkin_desert_spring_march_rederivation` states it outright:

> *"STILL AVAILABLE, not done here: ca_desert's bare ucanr.edu / mg.ucanr.edu anchors could now be
> cleanly repointed at the pathed UC table that supports this window, but mixing a value change with
> a citation change in one promote is what the arc warns against."*

That is a filed, sourced, deliberately-deferred CASE 1 repoint. It is campaign A's opening move.

---

## 5. Recommended order

1. **The 52 clean repoints** — one promote, citation-only, no value moves. `DIVERGENT` rides along:
   it is absorbed by the table's own "only approximate" caveat and is not a defect class.
2. **The 2 okra decisions** — separate promote(s), because they are value questions. UC gives okra
   `May` in all four regions while our desert cells open in March and our north-coast z9 cell opens
   in June. Worth checking whether UC's single-month okra row is simply coarse (it gives the same
   `May` to the desert and the north coast, which is implausible on its face) before moving a date.
3. **The 12 with no UC row** — CASE 2 candidates; fold `lemon`/`lime` into campaign D's lemon pass.

### One question for Trevor, not resolvable from the data

The 8 cucurbit decisions blocked by `ca_desert_fall_cycle_provenance_gap` are blocked by a
contradiction that has been **formally ruled a provenance gap, not a correctness problem**. Their
*main* windows are supported by the table; only the *second planting* is not. Repointing the pair's
anchors wholesale would leave the pathed table cited on a cell it contradicts. The options are to
leave all 8, or to repoint at node granularity (main planting repointed, second planting left bare
carrying its accepted finding). Node-granular is defensible and recovers 8 decisions, but it splits
one region's anchors across two URLs — which is what `mid_south`'s one-id-one-URL rule exists to
prevent. **Recommend leaving all 8 and revisiting if the fall-cycle gap is ever closed by edit.**

---

## 6. Ledger corrections owed

- Kickoff 50 §3's table rows 1 and 2 are **stale** and row 1 recommends a move that was ruled
  against. Corrections belong in the kickoff, not silently in the ledger.
- The four-campaign breakdown is unaffected: campaign A remains 8 hunts / 76 decisions. What changed
  is its **internal composition**, not its size.
